"""组装学マス实例的角色目录（compose 的 characters-init 服务每次启动时运行）。

用法：python build_characters.py --upstream <eidolon-sc/characters> --pack <扩展包/characters>
                                 --patches <overlay/patches/characters.json> --out <输出目录>

1. 从用户本机的 eidolon-sc 复制各角色通用的目录（礼物、饮品、工作、酒吧、地点、信的配乐），
   这样原项目更新这些清单时，学マス实例也跟着更新；
2. 按 patches/characters.json 把里面写死的 283 说法换成学园的（每条必须精确命中，否则报错）；
3. 地点池去掉 283 的圣地标注（idols、source 两行）：那些是 283 的卡面取景地，和学マス的偶像无关；
4. 最后放上扩展包自己的文件：角色配置、人设、资料、头像、世界设定、读音。

输出目录先清空再写，原仓库和扩展包里的文件都只读不写。
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

from apply_patches import PatchError, apply

SHARED = {
    # 文件名: 原项目缺这个文件时是否报错
    "gifts.toml": True,
    "drinks.toml": False,  # 没有饮品目录时酒吧整个不开
    "jobs.toml": True,
    "places.toml": True,
    "letter_music.toml": False,
    "bar_lines.toml": False,
    "bar_visits.toml": False,
    "bar_audio.json": False,
}
HOLY_PLACE = re.compile(r"^(idols|source)\s*=.*\n", re.M)


def fail(message: str) -> None:
    print(f"\n[学マス扩展包] 组装角色目录失败：{message}\n", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", required=True)
    ap.add_argument("--pack", required=True)
    ap.add_argument("--patches", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    upstream, pack, out = Path(a.upstream), Path(a.pack), Path(a.out)
    if not (upstream / "characters.toml").exists():
        fail(f"{upstream} 不像 eidolon-sc 的 characters 目录（没有 characters.toml）。请检查 .env 里的 EIDOLON_SC_DIR")
    if not (pack / "characters.toml").exists():
        fail(f"{pack} 里没有扩展包的 characters.toml")

    out.mkdir(parents=True, exist_ok=True)
    for child in out.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()

    for name, required in SHARED.items():
        if (upstream / name).exists():
            shutil.copyfile(upstream / name, out / name)
        elif required:
            fail(f"原项目的 characters 目录里没有 {name}")
        else:
            print(f"[学マス扩展包] 原项目没有 {name}，跳过")

    try:
        n = apply(out, Path(a.patches), quiet=True)
    except PatchError as e:
        fail(str(e))
    places = out / "places.toml"
    text = places.read_text(encoding="utf-8")
    holy = len(HOLY_PLACE.findall(text))
    places.write_text(HOLY_PLACE.sub("", text), encoding="utf-8")

    shutil.copytree(pack, out, dirs_exist_ok=True)
    print(f"[学マス扩展包] 角色目录已组装：通用清单 {len(SHARED)} 个、补丁 {n} 条、去掉圣地标注 {holy} 行")


if __name__ == "__main__":
    main()
