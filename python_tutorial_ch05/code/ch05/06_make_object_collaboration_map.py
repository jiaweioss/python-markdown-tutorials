"""Generate an object-collaboration map for chapter 05."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_DIR = Path("assets/ch05/web")
PREVIEW = OUTPUT / "ch05_object_collaboration_map.png"
REPORT = REPORTS / "ch05_object_collaboration_map.md"

NODES = [
    ("LearningCard", (255, 345), "#2F6BFF"),
    ("CardDeck", (715, 345), "#24A06B"),
    ("Trial", (1165, 345), "#F28C28"),
    ("ReportBuilder", (715, 675), "#7A5AF8"),
]

MESSAGES = [
    ("add", (410, 345), (560, 345)),
    ("draw", (870, 345), (1010, 345)),
    ("record", (1115, 470), (820, 620)),
    ("summarize", (610, 620), (360, 470)),
]


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def make_markdown() -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第5章对象协作消息图",
        "",
        "面向对象不是把代码切成很多孤岛，而是让每个对象只承担清楚的职责，再通过消息协作。",
        "",
        "| 发送方向 | 消息 | 意义 |",
        "| --- | --- | --- |",
        "| LearningCard -> CardDeck | add | 一张卡片进入卡片盒 |",
        "| CardDeck -> Trial | draw | 从卡片盒抽出一次练习材料 |",
        "| Trial -> ReportBuilder | record | 试次把反应结果交给报告整理员 |",
        "| ReportBuilder -> LearningCard | summarize | 报告反过来帮助卡片复习与改进 |",
        "",
        "## 观察提示",
        "",
        "如果一条消息说不清楚，通常说明职责边界还没想清楚。先改设计，再急着写代码。",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=5)
    dx = 1 if x2 >= x1 else -1
    dy = 1 if y2 >= y1 else -1
    draw.polygon([(x2, y2), (x2 - dx * 24, y2 - dy * 10), (x2 - dx * 10, y2 - dy * 24)], fill=color)


def make_preview() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 920), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "Object Collaboration Map", fill="#162033", font=font(50, True))

    for label, start, end in MESSAGES:
        arrow(d, start, end, "#94A3B8")
        mx = (start[0] + end[0]) // 2
        my = (start[1] + end[1]) // 2
        d.rounded_rectangle((mx - 72, my - 22, mx + 72, my + 22), radius=18, fill="#FFFFFF", outline="#CBD5E1", width=2)
        d.text((mx - 48, my - 15), label, fill="#334155", font=font(21, True))

    for name, (x, y), color in NODES:
        d.rounded_rectangle((x - 140, y - 72, x + 140, y + 72), radius=26, fill="#F8FAFC", outline=color, width=5)
        d.text((x - 95, y - 18), name, fill=color, font=font(26, True))

    d.rounded_rectangle((225, 780, 1275, 825), radius=20, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((265, 792), "协作口诀：类管职责，对象发消息，边界不清先回到设计卡。", fill="#1D4ED8", font=font(22, True))
    im.save(PREVIEW, optimize=True, quality=95)
    return PREVIEW


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    report = make_markdown()
    preview = make_preview()
    copy_assets()
    print("created object collaboration map:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
