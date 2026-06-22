"""Chapter 02 artifact: create a visual cabinet for Python data types."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from statistics import mean
from textwrap import dedent


TRIALS = [
    {
        "trial_id": 1,
        "word": "RED",
        "ink_color": "blue",
        "response_key": "j",
        "correct": True,
        "reaction_time_ms": 612.4,
        "note": None,
    },
    {
        "trial_id": 2,
        "word": "GREEN",
        "ink_color": "green",
        "response_key": "f",
        "correct": True,
        "reaction_time_ms": 538.2,
        "note": "congruent",
    },
    {
        "trial_id": 3,
        "word": "BLUE",
        "ink_color": "red",
        "response_key": "f",
        "correct": True,
        "reaction_time_ms": 701.8,
        "note": "conflict",
    },
]


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch02").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def summary() -> dict:
    return {
        "participant": "S001",
        "trial_count": len(TRIALS),
        "mean_rt": round(mean(trial["reaction_time_ms"] for trial in TRIALS), 1),
        "accuracy": round(sum(1 for trial in TRIALS if trial["correct"]) / len(TRIALS), 2),
        "type_names": ["bool", "int", "float", "str", "list", "dict", "None"],
        "trial_record": TRIALS[0],
    }


def build_report(data: dict) -> str:
    return dedent(
        f"""
        # 第2章数据类型标本柜

        这份小作品把第2章的核心类型放进同一个任务里：一个极简 Stroop 学习记录。

        ## 本章类型如何合作

        | 类型 | 在本作品里的角色 |
        | --- | --- |
        | `str` | 保存被试编号、刺激词、墨水颜色和按键 |
        | `int` | 保存 trial 编号和 trial 数量 |
        | `float` | 保存反应时与平均反应时 |
        | `bool` | 保存是否正确、是否通过判断 |
        | `None` | 表示暂时没有备注 |
        | `dict` | 保存一条 trial 的完整记录 |
        | `list` | 保存多条 trial，以及类型清单 |

        ## 小结

        - 被试：{data["participant"]}
        - trial 数量：{data["trial_count"]}
        - 平均反应时：{data["mean_rt"]} ms
        - 正确率：{data["accuracy"]:.0%}

        数据类型不是背诵清单，而是给真实材料分格子。格子分清楚，后面才方便统计、画图、导出报告。
        """
    ).strip() + "\n"


def draw_png(path: Path, data: dict) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()

    width, height = 1800, 1120
    image = Image.new("RGB", (width, height), "#F6F8FB")
    draw = ImageDraw.Draw(image)

    title = font(58, True)
    subtitle = font(26)
    h2 = font(32, True)
    body = font(24)
    mono = font(23)
    small = font(19)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    colors = {
        "bool": "#2F6BFF",
        "int": "#24A06B",
        "float": "#F28C28",
        "str": "#7A5AF8",
        "list": "#18A9B5",
        "dict": "#E84C61",
        "None": "#6B7280",
    }

    def shadow_box(xy, radius: int = 24):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        draw.rounded_rectangle(xy, radius=radius, fill="#FFFFFF", outline=line, width=2)

    def pill(x: int, y: int, text: str, color: str, w: int = 126):
        draw.rounded_rectangle((x, y, x + w, y + 42), radius=21, fill=color)
        draw.text((x + 22, y + 8), text, font=small, fill="white")

    draw.text((94, 72), "Data Type Specimen Cabinet", font=title, fill=ink)
    draw.text((98, 146), "A tiny Stroop record, sorted by Python types.", font=subtitle, fill=muted)
    draw.line((96, 206, 1704, 206), fill=line, width=3)

    summary_cards = [
        ("participant", data["participant"], "str", colors["str"]),
        ("trials", str(data["trial_count"]), "int", colors["int"]),
        ("mean rt", f"{data['mean_rt']} ms", "float", colors["float"]),
        ("accuracy", f"{data['accuracy']:.0%}", "bool", colors["bool"]),
    ]
    for i, (label, value, type_name, color) in enumerate(summary_cards):
        x = 95 + i * 420
        shadow_box((x, 260, x + 360, 425))
        pill(x + 28, 292, type_name, color, 112)
        draw.text((x + 30, 348), label, font=small, fill=muted)
        draw.text((x + 160, 336), value, font=h2, fill=ink)

    type_cards = [
        ("bool", "True / False", "decision"),
        ("int", "1, 2, 3", "count"),
        ("float", "612.4 ms", "measure"),
        ("str", "'RED'", "label"),
        ("list", "[trial, ...]", "sequence"),
        ("dict", "{key: value}", "record"),
        ("None", "no note", "missing"),
    ]
    positions = [
        (110, 500),
        (475, 500),
        (840, 500),
        (1205, 500),
        (292, 750),
        (657, 750),
        (1022, 750),
    ]
    for (type_name, sample, role), (x, y) in zip(type_cards, positions):
        shadow_box((x, y, x + 300, y + 170))
        pill(x + 24, y + 26, type_name, colors[type_name], 112)
        draw.text((x + 28, y + 84), sample, font=mono, fill=ink)
        draw.text((x + 28, y + 124), role, font=small, fill=muted)

    shadow_box((1370, 700, 1690, 955))
    draw.text((1410, 740), "trial_record", font=h2, fill=ink)
    trial = data["trial_record"]
    lines = [
        "word: RED",
        "ink: blue",
        "key: j",
        "ok: True",
        "note: None",
    ]
    y = 790
    for line_text in lines:
        draw.text((1415, y), line_text, font=mono, fill=muted)
        y += 30

    draw.rounded_rectangle((330, 980, 1470, 1060), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw.text((405, 1006), "Choose the box before writing the code.", font=body, fill="#8A5A00")

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True, quality=95)
    return True


def main() -> None:
    root = project_root()
    output_dir = root / "output"
    report_dir = root / "reports"
    web_dir = root / "assets" / "ch02" / "web"
    output_dir.mkdir(exist_ok=True)
    report_dir.mkdir(exist_ok=True)
    web_dir.mkdir(parents=True, exist_ok=True)

    data = summary()
    json_file = output_dir / "ch02_data_type_specimen_cabinet.json"
    image_file = output_dir / "ch02_data_type_specimen_cabinet.png"
    report_file = report_dir / "ch02_data_type_specimen_cabinet.md"

    json_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_file.write_text(build_report(data), encoding="utf-8")
    has_image = draw_png(image_file, data)
    if has_image:
        shutil.copy2(image_file, web_dir / image_file.name)

    print("Data type specimen cabinet generated:")
    print("-", json_file)
    print("-", report_file)
    print("-", image_file if has_image else "PNG skipped because Pillow is unavailable")


if __name__ == "__main__":
    main()
