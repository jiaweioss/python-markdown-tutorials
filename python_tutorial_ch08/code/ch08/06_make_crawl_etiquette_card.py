"""Generate a crawl etiquette checklist for chapter 08."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_DIR = Path("assets/ch08/web")
PREVIEW = OUTPUT / "ch08_crawl_etiquette_card.png"
REPORT = REPORTS / "ch08_crawl_etiquette_card.md"

CHECKS = [
    ("Rules", "先看 robots.txt 和网站说明"),
    ("Pace", "请求要慢一点，别把网站当跑步机"),
    ("Scope", "只取本章任务需要的公开信息"),
    ("Source", "保留标题、URL、访问时间和用途"),
    ("Stop", "遇到拒绝、错误或敏感数据就停下"),
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
        "# 第8章爬虫礼仪检查卡",
        "",
        "爬虫不是“能访问就拿走”。公开资料采集要先确认边界，再保存可复查记录。",
        "",
        "| 检查点 | 操作提醒 |",
        "| --- | --- |",
    ]
    for label, tip in CHECKS:
        lines.append(f"| {label} | {tip} |")
    lines.extend(
        [
            "",
            "## 一句话原则",
            "",
            "像进入图书馆一样使用网页：看公告、轻声走、只拿需要的资料、写清来源，用完能归档。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT


def make_preview() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 920), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "Crawl Etiquette Card", fill="#162033", font=font(52, True))
    d.text((150, 198), "公开资料采集前，先过这五关。", fill="#5F6673", font=font(28))

    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8", "#18A9B5"]
    y = 305
    for i, (label, tip) in enumerate(CHECKS):
        color = colors[i % len(colors)]
        d.rounded_rectangle((150, y, 1350, y + 72), radius=18, fill="#F1F5F9", outline="#E2E8F0", width=2)
        d.ellipse((185, y + 22, 215, y + 52), fill=color)
        d.text((245, y + 18), label, fill=color, font=font(25, True))
        d.text((520, y + 17), tip, fill="#162033", font=font(25))
        y += 86

    d.rounded_rectangle((220, 775, 1280, 828), radius=20, fill="#FFF7ED", outline="#FDBA74", width=2)
    d.text((270, 788), "礼貌口诀：先看规则，慢慢请求，留下来源，随时停手。", fill="#9A3412", font=font(24, True))
    im.save(PREVIEW, optimize=True, quality=95)
    return PREVIEW


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    report = make_markdown()
    preview = make_preview()
    copy_assets()
    print("created crawl etiquette card:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
