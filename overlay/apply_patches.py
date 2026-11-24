"""把学マス扩展包的补丁打到 eidolon-sc 文件的一份副本上（构建镜像、组装角色目录时运行，不碰原仓库）。

用法：python apply_patches.py <目录> <补丁清单.json> [--lock upstream.lock --dockerfile Dockerfile]

补丁清单是 {"patches": [{"file", "old", "new", "count", "why"}]}：在 <目录>/<file> 里，
old 必须正好出现 count 次，全部换成 new。任何一条对不上（原项目改过这段），立即报错退出——
宁可起不来，也不带着 283 的设定跑。

--lock 给出 upstream.lock：扩展包的 Dockerfile 照抄了原项目 Dockerfile 的构建步骤，
原项目的 Dockerfile 变了，就要人工核对一遍再更新 lock 里的 sha256。
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


class PatchError(RuntimeError):
    pass


def fail(message: str) -> None:
    print(f"\n[学マス扩展包] 补丁失败：{message}\n", file=sys.stderr)
    sys.exit(1)


def check_dockerfile(root: Path, lock_path: Path, name: str = "Dockerfile") -> None:
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    actual = hashlib.sha256((root / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    if actual not in set(lock["dockerfiles"].values()):
        raise PatchError(
            f"原项目的 {name} 和扩展包测试过的版本不一样（sha256 {actual[:12]}…）。"
            "扩展包的 Dockerfile 照抄了它的构建步骤，请先对照原项目的 Dockerfile 更新扩展包，"
            f"再把新的 sha256 写进 upstream.lock。扩展包测试过的原项目提交：{lock.get('tested_commit')}"
        )


def apply(root: Path, spec_path: Path, quiet: bool = False) -> int:
    """打上 spec_path 里的全部补丁；有一条对不上就抛 PatchError，已经改过的文件不回滚（它们是副本）。"""
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    for n, p in enumerate(spec["patches"], 1):
        path = root / p["file"]
        if not path.exists():
            raise PatchError(f"{spec_path.name} 第 {n} 条：找不到 {p['file']}（{p.get('why', '')}）")
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        found = text.count(p["old"])
        if found != p["count"]:
            raise PatchError(
                f"{spec_path.name} 第 {n} 条：{p['file']} 里「{p['old'][:60]}」应出现 {p['count']} 次，"
                f"实际 {found} 次。原项目可能改过这里（{p.get('why', '')}）。"
            )
        path.write_text(text.replace(p["old"], p["new"]), encoding="utf-8")
        if not quiet:
            print(f"[学マス扩展包] {n:02d} {p['file']}：{p.get('why', '')}")
    return len(spec["patches"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("patches")
    ap.add_argument("--lock")
    ap.add_argument("--dockerfile", default="Dockerfile")
    a = ap.parse_args()
    try:
        if a.lock:
            check_dockerfile(Path(a.root), Path(a.lock), a.dockerfile)
        n = apply(Path(a.root), Path(a.patches))
    except PatchError as e:
        fail(str(e))
    print(f"[学マス扩展包] {n} 条补丁全部打上")


if __name__ == "__main__":
    main()
