"""学マス的唱片、歌曲和演出同步（独立脚本，只用标准库）。

用法：python -I gakumas_world_sync.py <world.json> [--cache 缓存目录]
读入 world.json 里的偶像和组合，从下面的来源重新生成 releases / songs / lives，写回同一个文件，
并在旁边写 sync-report.md。偶像、职员、组合这几部分不动。

来源（和 scchat 的 `eidolon world sync` 对 283 的做法对应）：
- 唱片：学マス官方厂牌站 gakuen-label.idolmaster-official.jp 的 DISCOGRAPHY（实体 CD 和数字发行都收）。
  标题、发售日、曲目以它为准。它没有品番，所以唱片的编号用它的条目 ID，写成 label:<id>。
- 每首歌谁唱：ふじわらはじめ（api.fujiwarahaji.me）同一张唱片的曲目。对不上的写进报告，不写歌。
- 演出：官方门户 CMS 的 LIVE-EVENT 里品牌为 GAKUEN 的条目决定有哪些演出、哪几天、在哪里；
  每天谁上台、唱了什么，取 ふじわらはじめ 同一天的演出记录（出演者 = 曲目单里唱过歌的偶像）。
  官方条目在 ふじわらはじめ 里一天都对不上的（电视节目、展会、检定等），不当作演出。
- 不在偶像名单里的人唱的歌（賀陽燐羽、白草月花等，或别的品牌的偶像）不算她们的歌，报告里列出。
"""

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

LABEL = "https://gakuen-label.idolmaster-official.jp/"
LABEL_DISCO = LABEL + "discography"
FUJI = "https://api.fujiwarahaji.me/v4/"
CMS = "https://cmsapi-frontend.idolmaster-official.jp/sitern/api/"
PORTAL = "https://idolmaster-official.jp/"
UA = "Mozilla/5.0 (compatible; scchat-gakumas-sync)"
BRANDS = {
    "as": "765PRO ALLSTARS", "cg": "シンデレラガールズ", "ml": "ミリオンライブ！", "sidem": "SideM",
    "sc": "シャイニーカラーズ", "876": "ディアリースターズ", "joint": "THE IDOLM@STERシリーズ",
    "cover": "カバー曲",
}
NO_SONG = re.compile(r"instrumental|off\s*vocal|karaoke|game\s*size|カラオケ|ドラマ|トーク", re.I)
VERSION = re.compile(r"\s*(?:\[[^\]]*\]|［[^］]*］|[（(][^（()）]*ver\.?[)）])\s*$", re.I)
JST = timedelta(hours=9)


class Fetcher:
    def __init__(self, cache: Path | None):
        self.cache = cache
        if cache:
            cache.mkdir(parents=True, exist_ok=True)

    def text(self, url: str) -> str:
        key = re.sub(r"[^\w.-]", "_", url)[-150:]
        if self.cache and (self.cache / key).exists():
            return (self.cache / key).read_text(encoding="utf-8")
        time.sleep(0.3)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8")
        if self.cache:
            (self.cache / key).write_text(body, encoding="utf-8")
        return body

    def json(self, url: str):
        return json.loads(self.text(url))


def key(text: str) -> str:
    text = html.unescape(text)
    return re.sub(r"[\W_]", "", unicodedata.normalize("NFKC", text)).casefold()


def base_title(title: str) -> str:
    """曲名去掉版本标注：「初 [月村手毬 Solo ver.]」→「初」。"""
    while (m := VERSION.search(title)) and m.start() > 0:
        title = title[: m.start()]
    title = re.sub(r"(?<=[）)])[^（()）]*solo\s*ver\.?\s*$", "", title, flags=re.I)  # 「…（…）花海咲季 Solo ver」
    return title.strip()


# 唱片


def tag_names(title: str, idols: list[str]) -> list[str]:
    """曲名版本标注里写到的偶像，按出现顺序：「標［倉本千奈・篠澤 広 ver.］」→ 倉本千奈、篠澤広。"""
    tag = key(title[len(base_title(title)):])
    if not tag and re.search(r"ver\.?\s*$", title, re.I):  # 标注不在括号里：「…（FOR WONDERFUL STORY）花海咲季 Solo ver」
        tag = key(title)
    found = [(tag.find(key(i)), i) for i in idols if key(i) in tag]
    return [i for _, i in sorted(found)]


def label_releases(f: Fetcher) -> list[dict]:
    page = f.text(LABEL_DISCO)
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', page, re.S)
    rsc = "".join(json.loads('"' + c + '"') for c in chunks)
    at = rsc.find('"contents":[')
    if at == -1:
        sys.exit(f"{LABEL_DISCO} 上找不到唱片列表，页面结构可能变了")
    contents, _ = json.JSONDecoder().raw_decode(rsc, at + len('"contents":'))
    return contents


def jst_day(stamp: str) -> date:
    return (datetime.fromisoformat(stamp.replace("Z", "+00:00")) + JST).date()


class Fuji:
    def __init__(self, f: Fetcher):
        self.f = f
        self.songs = f.json(FUJI + "list?type=music&music_type=gakuen&limit=1000")
        self.discs: dict[str, dict] = {}  # key(name) -> disc json
        self.song_json: dict[str, list[dict]] = defaultdict(list)  # key(title) -> songs
        for s in self.songs:
            d = f.json(s["api"])
            self.song_json[key(s["name"])].append(d)
            for disc in d.get("disc") or []:
                k = key(disc["name"])
                if k not in self.discs:
                    self.discs[k] = f.json(disc["api"])

    def disc(self, title: str) -> dict | None:
        k = key(re.sub(r"【[^】]*】", "", title))
        if k in self.discs:
            return self.discs[k]
        cands = [d for dk, d in self.discs.items() if dk.startswith(k) or k.startswith(dk)]
        return cands[0] if len(cands) == 1 else None


def members(entry: dict) -> tuple[list[str], list[str]]:
    names = [m.get("name", "") for m in entry.get("member") or []]
    units = []
    for u in entry.get("unit") or []:
        if u.get("name"):
            units.append(u["name"])
        names += [m.get("name", "") for m in u.get("member") or []]
    return list(dict.fromkeys(n for n in names if n)), units


def build_releases(f: Fetcher, fuji: Fuji, idols: set[str], units: dict, report: dict, idol_order: list[str]):
    releases, songs = [], {}
    ids: set[str] = set()

    def song_for(title: str, singers: list[str], special: str | None, catalog: str, src: list[str]):
        k = (key(base_title(title)), frozenset(singers))
        s = songs.get(k)
        if s is None:
            sid, n = base_title(title), 1
            while sid in ids:
                n += 1
                sid = f"{base_title(title)} #{n}"
            ids.add(sid)
            s = songs[k] = {"id": sid, "title": base_title(title), "singers": singers,
                            "special_unit": special, "releases": [], "sources": []}
        if catalog not in s["releases"]:
            s["releases"].append(catalog)
        s["sources"] += [u for u in src if u not in s["sources"]]
        return s["id"]

    def classify(entry: dict, where: str) -> tuple[list[str] | None, str | None]:
        names, unit_names = members(entry)
        if not names:
            return None, None
        strangers = [n for n in names if n not in idols]
        if strangers:
            report["unmatched"].append(f"{where}：{'、'.join(strangers)}")
            return None, None
        special = None
        for u in unit_names:
            if u in units and set(units[u]) == set(names):
                continue
            if "初星学園" in u or "学園アイドルマスター" in u:
                continue
            special = u
        return names, special

    for r in sorted(label_releases(f), key=lambda r: (r.get("release_date") or "9", r["title"])):
        title = html.unescape(r["title"]).strip()
        url = f"{LABEL}discography/{r['id']}"
        if not r.get("release_date"):
            report["no_date"].append(f"{title}（{url}）")
            continue
        if re.search(r"music\s*video|blu-?ray|dvd", title, re.I):
            report["video"].append(f"{title}（{url}）")
            continue
        catalog = f"label:{r['id']}"
        day = jst_day(r["release_date"])
        digital = r["category"] == ["Streaming&DL"]
        tracks = [html.unescape(t["name"]).strip() for t in sorted((t for t in r.get("tracks") or [] if t.get("name")), key=lambda t: int(t.get("index") or 0))]
        if digital and not tracks:
            tracks = [title]
        disc = fuji.disc(title)
        fan_tracks = [s for s in (disc or {}).get("song") or [] if not {"offvocal", "gamever"} & set(s.get("flag") or [])]
        out = []
        for n, t in enumerate(tracks, 1):
            where = f"《{title}》第 {n} 首「{t}」"
            if NO_SONG.search(t):
                out.append({"title": t, "song": None})
                continue
            tagged_idols = tag_names(t, idol_order)
            if tagged_idols:
                out.append({"title": t, "song": song_for(t, tagged_idols, None, catalog, [url])})
                continue
            cands = [s for s in fan_tracks if key(s["name"]) == key(base_title(t))]
            if len(cands) > 1:  # 同名的几种版本，曲名没有标注：取原版
                orig = [s for s in cands if "orig" in (s.get("flag") or [])]
                if len(orig) == 1:
                    cands = orig
                elif len({frozenset(members(s)[0]) for s in cands}) == 1:
                    cands = cands[:1]
                else:
                    most = max(len(members(s)[0]) for s in cands)
                    top = [s for s in cands if len(members(s)[0]) == most]
                    cands = top[:1] if len(top) == 1 else cands
            singers = special = None
            src = [url]
            if len(cands) == 1:
                singers, special = classify(cands[0], where)
                src.append(disc.get("link", ""))
            disc_silent = len(cands) == 1 and not members(cands[0])[0]
            if singers is None and (not cands or disc_silent):
                # ふじわらはじめ 没有这张唱片、这首不在上面、或唱片上没写演唱者时，用曲名唯一对应的歌
                same = fuji.song_json.get(key(base_title(t)), [])
                if len(same) == 1:
                    singers, special = classify(same[0], where)
                    src.append(same[0].get("link", ""))
            if singers is None:
                if not any(where in u for u in report["unmatched"]):
                    report["unknown"].append(f"{where}（{url}）")
                out.append({"title": t, "song": None})
                continue
            out.append({"title": t, "song": song_for(t, singers, special, catalog, src)})
        releases.append({"catalog": catalog, "title": title, "date": day.isoformat(), "tracks": out,
                         "sources": [url] + ([disc["link"]] if disc and disc.get("link") else [])})
    return releases, list(songs.values())


# 演出


_DATE = re.compile(r"(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日")
_MORE = re.compile(r"^\s*(?:\([^)]*\)|（[^）]*）)?\s*[、・]\s*(\d{1,2})\s*日")


def dates_in(text: str) -> list[date]:
    found = []
    for m in _DATE.finditer(text):
        y, mo, d = map(int, m.groups())
        found.append(date(y, mo, d))
        rest = text[m.end():]
        while more := _MORE.match(rest):
            found.append(date(y, mo, int(more.group(1))))
            rest = rest[more.end():]
    return found


def cms_articles(f: Fetcher) -> list[dict]:
    token = f.json(CMS + "cmsbase/Token/get")["data"]["token"]
    arts: list[dict] = []
    while True:
        q = {"site": "jp", "ip": "idolmaster", "token": token,
             "data": json.dumps({"category": ["LIVE-EVENT"]}), "limit": 100, "start": len(arts)}
        req = urllib.request.Request(CMS + "idolmaster/Article/list?" + urllib.parse.urlencode(q),
                                     headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            page = json.loads(r.read().decode("utf-8"))["data"]
        arts += page["article_list"]
        if not page["article_list"] or len(arts) >= int(page["total_count"]):
            return arts


def official_lives(arts: list[dict]) -> list[dict]:
    """每个官方条目拆成一场或几场演出：{name, days: [(date, venue)], source}。"""
    lives = []
    for a in arts:
        if not any(b.get("code") == "GAKUEN" for b in a.get("brand") or []) or a.get("article_type") == "lp_detail":
            continue
        title = re.sub(r"\s+", " ", html.unescape(a.get("title") or "")).strip()
        if a.get("article_type") == "detail_page" and a.get("url_name"):
            source = f"{PORTAL}live_events/{a['url_name']}"
        else:
            source = re.sub(r"(?<!:)//+", "/", a.get("event_url") or f"{PORTAL}live_event/")
        dsp, place = a.get("event_dspdate") or "", a.get("event_place") or ""
        d_secs = [s.strip() for s in re.split(r"\n\s*\n", dsp) if s.strip()]
        p_secs = [s.strip() for s in re.split(r"\n\s*\n", place) if s.strip()]
        named = len(d_secs) > 1 and all(not _DATE.search(s.splitlines()[0]) for s in d_secs)
        for i, sec in enumerate(d_secs if named else [dsp]):
            lines = sec.splitlines()
            name = lines[0].strip() if named else title
            psec = p_secs[i] if named and i < len(p_secs) else place
            plines = [l.strip() for l in psec.splitlines() if l.strip()]
            if named and plines and plines[0] == name:
                plines = plines[1:]
            by_date = {}
            for l in plines:
                ds = dates_in(l)
                if ds:
                    by_date[ds[0]] = _DATE.sub("", l).split(")", 1)[-1].split("）", 1)[-1].strip()
            default = plines[0] if plines and not dates_in(plines[0]) else ""
            days = [(d, by_date.get(d, default)) for d in dict.fromkeys(dates_in(sec))]
            if days:
                lives.append({"name": name, "days": days, "source": source})
    return lives


def build_lives(f: Fetcher, idols: set[str], report: dict):
    fuji_lives = f.json(FUJI + "list?type=live&limit=2000")
    by_day: dict[date, list[dict]] = defaultdict(list)
    for l in fuji_lives:
        if m := re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", l.get("date") or ""):
            by_day[date(*map(int, m.groups()))].append(l)
    used: set[int] = set()
    lives = []
    for off in official_lives(cms_articles(f)):
        days = []
        for d, venue in off["days"]:
            shows = []
            for l in by_day.get(d, []):
                detail = f.json(l["api"])
                if any(n in idols for s in detail.get("song") or [] for n in members(s)[0]):
                    shows.append(detail)
            if not shows:
                continue
            if "延期" in shows[0]["name"] and all("延期" in s["name"] and "延期公演" not in s["name"] for s in shows):
                report["called_off"].append(f"{off['name']} {d}：{shows[0]['link']}")
                continue
            used.update(s["tax_id"] for s in shows)
            performers: list[str] = []
            for s in shows:
                for song in s.get("song") or []:
                    performers += [n for n in members(song)[0] if n in idols and n not in performers]
            setlist = []
            if len(shows) == 1:
                for song in shows[0].get("song") or []:
                    names = [n for n in members(song)[0] if n in idols]
                    if not names:
                        continue
                    brand = None if song.get("music_type") == "gakuen" else BRANDS.get(song.get("music_type"), song.get("music_type"))
                    setlist.append({"title": html.unescape(song.get("name") or song.get("song_text") or "（曲名不明）"), "singers": names, "dancers": [], "brand": brand})
            days.append({"date": d.isoformat(), "venue": venue or shows[0].get("place") or "",
                         "performers": performers, "absent": [],
                         "sources": [s["link"] for s in shows], "setlist": setlist})
        okey = key(re.sub(r"\s*学園アイドルマスター\s*", "", off["name"]))
        late = defaultdict(list)
        for l in fuji_lives:
            if "延期公演" in l["name"] and okey and okey in key(l["name"]) and l["tax_id"] not in used:
                if m := re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", l.get("date") or ""):
                    late[date(*map(int, m.groups()))].append(f.json(l["api"]))
        for d, shows in sorted(late.items()):
            used.update(s["tax_id"] for s in shows)
            performers = []
            for s in shows:
                for song in s.get("song") or []:
                    performers += [n for n in members(song)[0] if n in idols and n not in performers]
            days.append({"date": d.isoformat(), "venue": shows[0].get("place") or "", "performers": performers,
                         "absent": [], "sources": [s["link"] for s in shows], "setlist": []})
            report["postponed"].append(f"{off['name']}：延期公演 {d}（{shows[0]['link']}）")
        days.sort(key=lambda d: d["date"])
        if days:
            lives.append({"name": off["name"], "days": days, "sources": [off["source"]]})
        else:
            report["official_only"].append(f"{off['name']}（{'、'.join(str(d) for d, _ in off['days'])}）：{off['source']}")
    for l in fuji_lives:
        if l["tax_id"] in used or not l.get("date"):
            continue
        if any(k in l["name"] for k in ("学園アイドルマスター", "初星学園")) and "初星宴舞" not in l["name"]:
            report["fuji_only"].append(f"{l['name']}（{l['date']}）：{l['link']}")
    lives.sort(key=lambda l: (l["days"][0]["date"], l["name"]))
    return lives


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("world")
    ap.add_argument("--cache")
    a = ap.parse_args()
    path = Path(a.world)
    world = json.loads(path.read_text(encoding="utf-8"))
    idols = {i["name"] for i in world["idols"]}
    units = {u["name"]: u["members"] for u in world["units"]}
    f = Fetcher(Path(a.cache) if a.cache else None)
    report = defaultdict(list)
    fuji = Fuji(f)
    world["releases"], world["songs"] = build_releases(f, fuji, idols, units, report, [i["name"] for i in world["idols"]])
    world["lives"] = build_lives(f, idols, report)
    path.write_text(json.dumps(world, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    titles = {
        "no_date": "厂牌站上没有发售日的发行（没有写入）",
        "video": "影像作品，不算唱片（没有写入）",
        "unknown": "说不出谁唱的曲目（没有写成歌）",
        "unmatched": "有偶像名单以外的人唱的曲目（没有写成歌）",
        "called_off": "延期或取消的演出日（没有写入）",
        "postponed": "延期公演（按 ふじわらはじめ 写入原演出，会场取它的记录）",
        "official_only": "官方有、ふじわらはじめ 里没有学マス偶像出演记录的条目（不当作演出）",
        "fuji_only": "ふじわらはじめ 有、官方条目里没有的学マス演出（没有写入）",
    }
    out = [f"# 学マス世界数据同步报告（{date.today()}）", "",
           f"唱片 {len(world['releases'])} 张，歌曲 {len(world['songs'])} 首，"
           f"演出 {len(world['lives'])} 场 / {sum(len(l['days']) for l in world['lives'])} 天。", ""]
    for k, t in titles.items():
        out += [f"## {t}（{len(report[k])}）", ""] + [f"- {x}" for x in report[k]] + [""]
    (path.parent / "sync-report.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out[:3]))


if __name__ == "__main__":
    main()
