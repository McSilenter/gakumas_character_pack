"""把学园偶像大师的 ADV 剧本（GakumasTranslationData 的 resource/*.txt）转成剧情库能导入的 CSV。

每个剧本一份 CSV，列是 `id,name,text,trans`，最后一行 `info` 写剧本编号（就是文件名，例如
adv_dear_ttmr_001），和 SCTranslationData 的格式一样，`eidolon story import-csv` 直接能读。
文件放在「<卡名或活动名>/<话名>.csv」，导入器把目录名当作卡名、文件名当作话名。

日文原文和说话人以游戏的原版剧本为准（给了 --original 时，是 DreamGallery/Campus-adv-txts 的
Resource 目录）：汉化版把一部分说话人翻成了中文（「琴音」原文是「ことね」），日文的标点也改过
（「――」变成「——」）。两版按日文原文逐句对齐，原版的说话人和日文、汉化版的中文译文合成一行；
对不上的台词用汉化版的，报告里列出来。原版有、汉化版还没有的剧本（新剧情）也转，只有日文，
和闪耀色彩没翻译的镜像剧情一样（ADR-0004）。原版的注音（<r\\=よみ>漢字</r>）只留汉字，着重（<em>）
只留文字。没给原版时全用汉化版。

规则和闪耀色彩的导入一致：
- 只要 [message] 和 [narration]：日文进 text，中文译文进 trans；多段之间的换行写成 \\n。
- 制作人 {user} 写成「プロデューサー」；旁白没有说话人。
- 选项（[choicegroup]）不收，选项之后的反应全都保留。学马仕的选项只有译文，没有日文原文。
- 失败结局（文件名带 failure）不转，列在报告里。

卡名、话名先查 masterTrans 的中文译名；没有译名的用游戏 master 里的日文原名（给了 --jp-master
时，是 vertesan/gakumasu-diff 的 YAML 所在目录，要 ProduceStory、Story、Character、IdolCard、
SupportCard、StoryEvent 这几张表，读它们需要 PyYAML）；都没有的用文件名拼一个看得懂的名字。
人名（卡名目录里的偶像名）和说话人一样，原作是日文的就用日文。
最后打印报告：每类剧本的数量、标题查到的比例、跳过的文件，和需要人看一眼的异常。

用法：python -I gakumas_convert.py <local-files 目录> <输出目录> [--jp-master 目录] [--original 目录]
"""

import argparse
import csv
import difflib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PRODUCER = "プロデューサー"

_TAG = re.compile(r"^\[(\w+)")
_PAIR = re.compile(r"<r\\=(.*?)>(.*?)</r>", re.S)
_EMPHASIS = re.compile(r"<em(?:\\=[^>]*)?>|</em>")  # 着重：<em\=・・・>筋トレ、<em>ライバル</em>
_RUBY = re.compile(r"<r\\=[^>]*>(.*?)</r>", re.S)  # 原版的注音：<r\=りゅうげつまき>龍月真希</r>
_NAME = re.compile(r" name=(.+?)(?= \w+=|\]$)")
_TEXT_END = re.compile(r" (?:name|se|hide|isInner|clip|voice|thinking|wait|speaker|speed)=")
_UNSAFE = re.compile(r'[\\/:*?"<>|]')


def _rows(master: Path, table: str) -> list[dict]:
    path = master / f"{table}.json"
    return json.loads(path.read_text(encoding="utf-8"))["data"] if path.exists() else []


def _yaml_rows(master: Path | None, table: str) -> list[dict]:
    if master is None or not (path := master / f"{table}.yaml").exists():
        return []
    import yaml  # 只有给了日文 master 才需要

    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


class Titles:
    """卡名、话名：中文译名（masterTrans）优先，没有译名的用日文原名（游戏的 master，
    vertesan/gakumasu-diff 的 YAML），都没有的由调用方用文件名拼。"""

    def __init__(self, master: Path, jp_master: Path | None) -> None:
        self.names = {r["id"]: f'{r["lastName"]}{r["firstName"]}' for r in _rows(master, "Character")}
        self.produce = {r["id"]: r["title"] for r in _rows(master, "ProduceStory") if r.get("title")}
        self.story = {r["id"]: r["title"] for r in _rows(master, "Story") if r.get("title")}
        self.idol_cards = {r["id"]: r["name"] for r in _rows(master, "IdolCard") if r.get("name")}
        self.chapters = {r["id"]: f'{r["title"]} {r.get("description", "")}'.strip()
                         for r in _rows(master, "MainStoryChapter")}
        self.growth = {(r["characterId"], r["number"]): r["title"]
                       for r in _rows(master, "ProduceEventCharacterGrowth")}
        self.events = {r["id"]: r["title"] for r in _rows(master, "StoryEvent") if r.get("title")}
        # 日文：剧本编号 → (master 里的编号, 标题)；卡名、活动名
        self.jp_episodes = {r["advAssetId"]: (r["id"], r.get("title") or "")
                            for table in ("ProduceStory", "Story")
                            for r in _yaml_rows(jp_master, table) if r.get("advAssetId")}
        self.jp_names = {r["id"]: f'{r["lastName"]}{r["firstName"]}' for r in _yaml_rows(jp_master, "Character")}
        self.jp_idol_cards = {r["id"]: r["name"] for r in _yaml_rows(jp_master, "IdolCard") if r.get("name")}
        self.jp_support_cards = {r["id"]: r["name"] for r in _yaml_rows(jp_master, "SupportCard") if r.get("name")}
        self.jp_events = {r["id"]: r["title"] for r in _yaml_rows(jp_master, "StoryEvent") if r.get("title")}

    def name(self, cid: str) -> str:
        """偶像名：原作是日文，日文优先。"""
        return self.jp_names.get(cid) or self.names.get(cid) or cid

    def episode(self, stem: str, *zh_keys: str) -> tuple[str, str]:
        """这一话的标题和它的语言（"zh"、"ja"，查不到是 ("", "")）。中文译名按日文 master
        里的编号查，没有日文 master 时按 zh_keys 猜。"""
        jp_id, jp_title = self.jp_episodes.get(stem, ("", ""))
        for key in (jp_id, *zh_keys):
            if key and (zh := self.produce.get(key) or self.story.get(key)):
                return zh, "zh"
        return (jp_title, "ja") if jp_title else ("", "")


def _named(label: str, title: str) -> str:
    return f"{label} {title}" if title else label


def place(stem: str, t: Titles) -> tuple[str, str, str]:
    """剧本的卡名（目录）、话名（文件名），以及话名的来源："zh" 中文译名、"ja" 日文原名、
    "" 只有文件名拼的编号。"""
    if m := re.fullmatch(r"adv_pstory_(\d+)_([a-z]+)_(.+)", stem):
        sid, cid, rest = m.groups()
        title, lang = t.episode(stem, f"p_story_{sid}_{cid}_{rest}")
        return f"{t.name(cid)} 培育剧情 {sid}", _named(rest, title), lang
    if m := re.fullmatch(r"adv_pevent_(\d+)_([a-z]+)_([a-z]+)_(.+)", stem):
        sid, cid, kind, n = m.groups()
        key = "business" if kind == "sales" else kind
        title, lang = t.episode(stem, f"p_story-event-{sid}_{cid}_{key}-{n}", f"p_story-event-{sid}_{cid}_{key}_{n}")
        return f"{t.name(cid)} 培育事件 {sid} {kind}", _named(n, title), lang
    if m := re.fullmatch(r"adv_pgrowth_(\d+)_([a-z]+)_(\d+)", stem):
        sid, cid, n = m.groups()
        if title := t.growth.get((cid, int(n))):
            return f"{t.name(cid)} 成长剧情 {sid}", _named(n, title), "zh"
        title, lang = t.episode(stem)
        return f"{t.name(cid)} 成长剧情 {sid}", _named(n, title), lang
    if m := re.fullmatch(r"adv_dear_([a-z]+)_(\d+)(?:-(\d+))?", stem):
        cid, n, half = m.groups()
        return f"{t.name(cid)} 亲爱度剧情", f"第{int(n)}{'.5' if half else ''}话", "zh"
    if m := re.fullmatch(r"adv_cidol-([a-z]+)-(\d+-\d+)_(\d+)", stem):
        cid, card, ep = m.groups()
        name = t.idol_cards.get(f"i_card-{cid}-{card}") or t.jp_idol_cards.get(f"i_card-{cid}-{card}") or card
        title, lang = t.episode(stem)
        return f"P卡 {t.name(cid)}【{name}】", _named(f"第{int(ep)}话", title), lang
    if m := re.fullmatch(r"adv_csprt-(\d+-\d+)_(\d+)", stem):
        card, ep = m.groups()
        name = t.jp_support_cards.get(f"s_card-{card}")
        title, lang = t.episode(stem, f"p_story-s_card-{card}-{ep}")
        return f"S卡 {card}{'【' + name + '】' if name else ''}", _named(f"第{int(ep)}话", title), lang
    if m := re.fullmatch(r"adv_unit_(\d+)-(\d+)_(\d+)", stem):
        part, chap, ep = m.groups()
        chapter = t.chapters.get(f"story-main-{part}-{chap}", f"{int(chap)}章")
        title, lang = t.episode(stem, f"story-main-{part}-{chap}-{ep}")
        return f"主线 第{int(part)}部 {chapter}", title or f"第{int(ep)}话", lang
    if m := re.fullmatch(r"adv_event_(\d+)_(.+)", stem):
        n, rest = m.groups()
        event = t.events.get(f"story-event-{n}") or t.jp_events.get(f"story-event-{n}")
        title, lang = t.episode(stem)
        return f"活动 {n}{' ' + event if event else ''}", _named(rest, title), lang
    title, lang = t.episode(stem)
    if m := re.fullmatch(r"adv_([a-z]+(?:-[a-z]+)*)[_-](.+)", stem):
        return f"其他 {m[1]}", _named(m[2], title), lang
    return "其他", _named(stem, title), lang


def parse(path: Path) -> tuple[list[tuple[str, str, str]], Counter]:
    """剧本里的台词 (说话人, 日文, 中文)，和需要人看一眼的异常计数。"""
    lines, odd = [], Counter()
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        m = _TAG.match(raw)
        if not m or m[1] not in ("message", "narration"):
            continue
        start = raw.index("text=") + len("text=") if "text=" in raw else None
        if start is None:
            odd["没有 text 的台词标签（空帧）"] += 1
            continue
        end = _TEXT_END.search(raw, start)
        value = _EMPHASIS.sub("", raw[start : end.start() if end else len(raw) - 1])
        pairs = _PAIR.findall(value)
        if pairs:
            ja = "\n".join(j for j, _ in pairs)
            zh = "\n".join(z for _, z in pairs)
            if _PAIR.sub("", value).replace("\\r\\n", "").strip():
                odd["译文标记之外还有文字"] += 1
        else:
            ja, zh = value.replace("\\r\\n", "\n"), ""
            odd["没有译文"] += 1
        if "<" in ja or "<" in zh:
            odd["文字里留有标记"] += 1
        speaker = ""
        if m[1] == "message" and (n := _NAME.search(raw, end.start() if end else 0)):
            speaker = PRODUCER if n[1] == "{user}" else n[1]
        if ja.strip():
            lines.append((speaker, ja.strip(), zh.strip()))
        else:
            odd["空台词"] += 1
    return lines, odd


def parse_original(path: Path) -> list[tuple[str, str]]:
    """原版剧本的台词 (说话人, 日文)。"""
    lines = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        m = _TAG.match(raw)
        if not m or m[1] not in ("message", "narration") or "text=" not in raw:
            continue
        start = raw.index("text=") + len("text=")
        end = _TEXT_END.search(raw, start)
        value = raw[start : end.start() if end else len(raw) - 1]
        ja = _RUBY.sub(r"\1", _EMPHASIS.sub("", value)).replace("\\r\\n", "\n").replace("\\n", "\n").strip()
        speaker = ""
        if m[1] == "message" and (n := _NAME.search(raw, end.start() if end else 0)):
            speaker = PRODUCER if n[1] == "{user}" else n[1]
        if ja:
            lines.append((speaker, ja))
    return lines


def _key(ja: str) -> str:
    """对齐用：抹掉两版之间改过的标点和空白。"""
    return re.sub(r"[\s―—─\-－~～〜]", "", ja)


def merge(translated: list[tuple[str, str, str]], original: list[tuple[str, str]], odd: Counter) -> list[tuple[str, str, str]]:
    """汉化版和原版逐句对齐：说话人和日文用原版，中文用汉化版。日文一致的直接对上；
    一段对不上的，两边句数相同就按顺序对上（记为「对齐但日文不同」），否则用汉化版。"""
    a, b = [_key(ja) for _, ja, _ in translated], [_key(ja) for _, ja in original]
    merged = list(translated)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for i, j in zip(range(i1, i2), range(j1, j2)):
                merged[i] = (original[j][0], original[j][1], translated[i][2])
            if op == "replace":
                odd["对齐但日文不同"] += i2 - i1
        elif i2 > i1:
            odd["对不上原版、用了汉化版"] += i2 - i1
    return merged


def write_csv(path: Path, stem: str, lines: list[tuple[str, str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "text", "trans"])
        for i, (speaker, ja, zh) in enumerate(lines, 1):
            w.writerow([f"{i:04d}", speaker, ja.replace("\n", "\\n"), zh.replace("\n", "\\n")])
        w.writerow(["info", stem, "", ""])


def safe(name: str) -> str:
    return _UNSAFE.sub("_", name).strip().rstrip(".") or "_"


def main(local_files: Path, out: Path, jp_master: Path | None, original: Path | None) -> int:
    titles = Titles(local_files / "masterTrans", jp_master)
    scripts = sorted((local_files / "resource").glob("adv_*.txt"))
    if original is not None:  # 汉化版还没有的新剧情：只有原版
        have = {p.name for p in scripts}
        scripts = sorted([*scripts, *(p for p in original.glob("adv_*.txt") if p.name not in have)],
                         key=lambda p: p.name)
    untranslated = 0
    kinds, skipped, odd_files = Counter(), [], defaultdict(list)
    titled: dict[str, Counter] = defaultdict(Counter)
    used: set[Path] = set()
    total_lines = 0
    renamed: Counter = Counter()
    for path in scripts:
        stem = path.stem
        kind = re.match(r"adv_([a-z]+)", stem)[1]
        if "failure" in stem:
            skipped.append(f"{stem}（失败结局）")
            continue
        if original is not None and path.parent == original:
            lines, odd = [(speaker, ja, "") for speaker, ja in parse_original(path)], Counter()
            untranslated += bool(lines)
        else:
            lines, odd = parse(path)
        if original is not None and path.parent != original:
            if (orig := original / path.name).exists():
                before = [speaker for speaker, _, _ in lines]
                lines = merge(lines, parse_original(orig), odd)
                renamed.update((b, s) for b, (s, _, _) in zip(before, lines) if b != s)
            else:
                odd["没有原版"] += 1
        for what, n in odd.items():
            odd_files[what].append(f"{stem}×{n}")
        if not lines:
            skipped.append(f"{stem}（没有台词）")
            continue
        source, title, lang = place(stem, titles)
        target = out / safe(source) / f"{safe(title)}.csv"
        if target in used:  # 同名的话：带上剧本编号区分
            target = target.with_name(f"{safe(title)} {stem}.csv")
        used.add(target)
        write_csv(target, stem, lines)
        kinds[kind] += 1
        titled[kind][lang or "none"] += 1
        total_lines += len(lines)

    print(f"转换 {sum(kinds.values())} 个剧本，{total_lines} 行台词，输出到 {out}")
    if original is not None:
        print(f"其中 {untranslated} 个汉化版还没有，只有日文")
    for kind, n in kinds.most_common():
        c = titled[kind]
        print(f"  {kind}: {n} 个，标题用中文 {c['zh']}、日文 {c['ja']}、只有编号 {c['none']}")
    print(f"跳过 {len(skipped)} 个：")
    for s in skipped:
        print(f"  {s}")
    for what, files in odd_files.items():
        print(f"{what}：{len(files)} 个剧本，例如 {'、'.join(files[:5])}")
    if renamed:
        print("说话人按原版改回日文（汉化版 → 原版，行数）：")
        for (before, after), n in renamed.most_common():
            print(f"  {before or '（旁白）'} → {after or '（旁白）'}：{n}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("local_files", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--jp-master", type=Path)
    parser.add_argument("--original", type=Path)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(args.local_files, args.out, args.jp_master, args.original))
