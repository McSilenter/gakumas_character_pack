"""学マス剧情库的下载和转换：story-sync.sh 在一次性容器里运行它，之后再由后端的
`eidolon story import-csv` 导入。只用标准库（转换时读日文 master 要 PyYAML，后端镜像里有）。

用法：python sync.py <剧情目录>     （容器里是 /corpus）

剧情目录里：
- sources/    三份来源的下载（不进仓库，ADR-0003 的做法），和记下各自版本的 versions.json：
  - GakumasTranslationData：chinosk6/GakumasTranslationData 发布版里的 local-files（中文译文、
    中文卡名话名）；
  - Campus-adv-txts：DreamGallery/Campus-adv-txts 的 Resource（日文原文和说话人）；
  - gakumasu-diff：vertesan/gakumasu-diff 里转换要用的几张表（日文卡名、话名）。
- csv/        转换好的剧情 CSV，后端从 /corpus/csv 导入。

每次先问 GitHub 三份各自的最新版本，和上次下载的一样就不再下载；三份都没变、csv/ 也在时不重新转换。
不用 GitHub 的 API（没登录时每个 IP 每小时只有 60 次，共用代理节点时常常早被别人用完）：发布版的最新 tag
看 releases/latest 跳转到哪里，仓库的最新提交问 git 自己的接口（git ls-remote 用的那个），下载走
releases/download、codeload 和 raw，这几处都不受 API 的限额。
想固定在某个版本时设环境变量：GAKUMAS_GTD_TAG（发布版的 tag，如 v2.3.69）、GAKUMAS_ADV_REF、
GAKUMAS_MASTER_REF（完整的提交号，或分支名、tag）。
访问 GitHub 要代理时，设 GAKUMAS_SYNC_PROXY（只给剧情同步用，不影响后端；容器里访问本机的代理写
host.docker.internal，如 http://host.docker.internal:7890）。

退出码：0 成功（含没有新内容）；2 下载出错，但上次转换的 csv/ 还在，可以照常导入；
3 下载或转换出错，而且没有可导入的 csv/。
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

GTD = "chinosk6/GakumasTranslationData"
GTD_ZIP = "GakumasTranslationData.zip"
ADV = "DreamGallery/Campus-adv-txts"
MASTER = "vertesan/gakumasu-diff"
MASTER_TABLES = ("Character", "IdolCard", "ProduceStory", "Story", "StoryEvent", "SupportCard")
UA = "gakumas-character-pack-story-sync"
_proxy = os.environ.get("GAKUMAS_SYNC_PROXY")
_open = urllib.request.build_opener(
    *([urllib.request.ProxyHandler({"http": _proxy, "https": _proxy})] if _proxy else [])
).open
HERE = Path(__file__).resolve().parent


class SyncError(RuntimeError):
    pass


def say(message: str) -> None:
    print(f"[剧情同步] {message}", flush=True)


def _request(url: str, tries: int = 3):
    """打开 url（跟着跳转），连不上或服务器出错时隔几秒再试，共 tries 次。"""
    for attempt in range(1, tries + 1):
        try:
            return _open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120)
        except urllib.error.HTTPError as e:
            if e.code == 404 or (e.code < 500 and e.code != 429) or attempt == tries:
                raise SyncError(f"打开 {url} 失败：HTTP {e.code}") from None
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt == tries:
                raise SyncError(f"连不上 {url}：{e}。访问 GitHub 要代理时设 GAKUMAS_SYNC_PROXY") from None
        time.sleep(5 * attempt)
    raise AssertionError


def fetch(url: str) -> bytes:
    with _request(url) as r:
        return r.read()


def latest_tag(repo: str) -> str:
    """发布版的最新 tag：releases/latest 跳转到 releases/tag/<tag>。"""
    with _request(f"https://github.com/{repo}/releases/latest") as r:
        final = r.geturl()
    if not (m := re.search(r"/releases/tag/([^/?#]+)$", final)):
        raise SyncError(f"{repo} 还没有发布版，或者 GitHub 的页面变了（releases/latest 跳到了 {final}）")
    return urllib.parse.unquote(m[1])


def commit_of(repo: str, ref: str) -> str:
    """ref（分支、tag 或完整的提交号）现在指向的提交，问 git 自己的接口（和 git ls-remote 一样）。"""
    if re.fullmatch(r"[0-9a-f]{40}", ref):
        return ref
    refs = fetch(f"https://github.com/{repo}.git/info/refs?service=git-upload-pack").decode("utf-8", "replace")
    found = dict((name, sha) for sha, name in re.findall(r"([0-9a-f]{40}) (refs/\S+?)(?:\^\{\})?(?=[\s\x00])", refs))
    for name in (f"refs/heads/{ref}", f"refs/tags/{ref}"):
        if name in found:
            return found[name]
    raise SyncError(f"{repo} 里找不到 {ref}（分支、tag 或完整的提交号）")


def unzip_part(data: bytes, part: str, target: Path) -> int:
    """把 zip 里第一层目录下的 `part`（如 Resource/）解压到 target，先清空；返回文件数。"""
    tmp = target.with_name(target.name + ".new")
    shutil.rmtree(tmp, ignore_errors=True)
    count = 0
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            name = info.filename
            # 发布版的 zip 和 codeload 的 zip 都可能多一层目录，找到 part 所在的位置
            i = name.find(part)
            if info.is_dir() or i < 0 or (i > 0 and name[i - 1] != "/"):
                continue
            dest = tmp / name[i + len(part):]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(z.read(info))
            count += 1
    if count == 0:
        shutil.rmtree(tmp, ignore_errors=True)
        raise SyncError(f"下载的 zip 里没有 {part}，来源的目录结构可能变了")
    shutil.rmtree(target, ignore_errors=True)
    tmp.rename(target)
    return count


def sync_gtd(sources: Path, have: dict) -> str:
    tag = os.environ.get("GAKUMAS_GTD_TAG") or latest_tag(GTD)
    target = sources / "GakumasTranslationData"
    if have.get("gtd") == tag and (target / "resource").is_dir():
        say(f"中文译文 {GTD} {tag}：和上次一样，不下载")
        return tag
    say(f"中文译文 {GTD} {tag}：下载 {GTD_ZIP}")
    data = fetch(f"https://github.com/{GTD}/releases/download/{urllib.parse.quote(tag)}/{GTD_ZIP}")
    say(f"  {len(data) // 1_000_000} MB")
    n = unzip_part(data, "local-files/", target)
    say(f"  解压 {n} 个文件")
    return tag


def sync_adv(sources: Path, have: dict) -> str:
    sha = commit_of(ADV, os.environ.get("GAKUMAS_ADV_REF") or "main")
    target = sources / "Campus-adv-txts"
    if have.get("adv") == sha and target.is_dir():
        say(f"日文原文 {ADV}@{sha[:8]}：和上次一样，不下载")
        return sha
    say(f"日文原文 {ADV}@{sha[:8]}：下载")
    n = unzip_part(fetch(f"https://codeload.github.com/{ADV}/zip/{sha}"), "Resource/", target)
    say(f"  解压 {n} 个文件")
    return sha


def sync_master(sources: Path, have: dict) -> str:
    sha = commit_of(MASTER, os.environ.get("GAKUMAS_MASTER_REF") or "main")
    target = sources / "gakumasu-diff"
    if have.get("master") == sha and all((target / f"{t}.yaml").exists() for t in MASTER_TABLES):
        say(f"日文 master {MASTER}@{sha[:8]}：和上次一样，不下载")
        return sha
    say(f"日文 master {MASTER}@{sha[:8]}：下载 {len(MASTER_TABLES)} 张表")
    tmp = target.with_name(target.name + ".new")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    for table in MASTER_TABLES:
        (tmp / f"{table}.yaml").write_bytes(fetch(f"https://raw.githubusercontent.com/{MASTER}/{sha}/{table}.yaml"))
    shutil.rmtree(target, ignore_errors=True)
    tmp.rename(target)
    return sha


def convert(sources: Path, out: Path) -> None:
    """转换到 csv.new，成功了再换掉 csv/：转换中途出错时，上次的 csv/ 不受影响。"""
    new = out.with_name(out.name + ".new")
    shutil.rmtree(new, ignore_errors=True)
    command = [
        sys.executable, str(HERE / "gakumas_convert.py"),
        str(sources / "GakumasTranslationData"), str(new),
        "--jp-master", str(sources / "gakumasu-diff"),
        "--original", str(sources / "Campus-adv-txts"),
    ]
    report = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    if report.returncode != 0:
        shutil.rmtree(new, ignore_errors=True)
        raise SyncError(f"转换出错：\n{report.stderr[-2000:]}")
    (new.parent / "convert-report.txt").write_text(report.stdout, encoding="utf-8")
    old = out.with_name(out.name + ".old")
    shutil.rmtree(old, ignore_errors=True)
    if out.exists():
        out.rename(old)
    new.rename(out)
    shutil.rmtree(old, ignore_errors=True)
    say((report.stdout.splitlines()[0] if report.stdout else "转换完成").replace(str(new), str(out)))
    say(f"  报告：{new.parent.name}/convert-report.txt")


def main(root: Path) -> int:
    sources, out = root / "sources", root / "csv"
    sources.mkdir(parents=True, exist_ok=True)
    versions_file = sources / "versions.json"
    have = json.loads(versions_file.read_text(encoding="utf-8")) if versions_file.exists() else {}
    try:
        now = {"gtd": sync_gtd(sources, have), "adv": sync_adv(sources, have), "master": sync_master(sources, have)}
    except SyncError as e:
        say(f"下载出错：{e}")
        if out.is_dir():
            say("上次转换的 csv/ 还在，照常导入那一份")
            return 2
        return 3
    if now == have.get("converted") and out.is_dir():
        say("三份来源都没有更新，不重新转换")
        versions_file.write_text(json.dumps(now | {"converted": now}, ensure_ascii=False, indent=1), encoding="utf-8")
        return 0
    # 先记下下载好的版本：转换出错时，下次不用重新下载
    versions_file.write_text(json.dumps(now | {"converted": have.get("converted")}, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        convert(sources, out)
    except SyncError as e:
        say(str(e))
        return 2 if out.is_dir() else 3
    versions_file.write_text(json.dumps(now | {"converted": now}, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(3)
    sys.exit(main(Path(sys.argv[1])))
