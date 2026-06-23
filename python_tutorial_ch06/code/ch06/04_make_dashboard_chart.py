"""Create a small learning-dashboard image from the sample CSV.

Run after:
    python code/ch06/01_make_sample_csv.py
"""

import csv
import shutil
from pathlib import Path
from statistics import mean

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "assets" / "ch06").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
INPUT = ROOT / "input" / "learning_records.csv"
OUTPUT = ROOT / "output" / "ch06_learning_dashboard.png"
WEB_COPY = ROOT / "assets" / "ch06" / "web" / "ch06_learning_dashboard_output.png"


def load_rows(path: Path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_bar(draw: ImageDraw.ImageDraw, x: int, y: int, width: int, label: str, value: int, color: str):
    draw.text((x, y - 34), label, fill="#243047", font=font(24, bold=True))
    draw.rounded_rectangle((x, y, x + 680, y + 34), radius=17, fill="#E9EEF6")
    draw.rounded_rectangle((x, y, x + width, y + 34), radius=17, fill=color)
    draw.text((x + 704, y - 2), f"{value} 分钟", fill="#243047", font=font(24))


def main():
    rows = load_rows(INPUT)
    minutes = [int(row["minutes"]) for row in rows]
    reaction = [int(row["rt_ms"]) for row in rows]
    done_count = sum(row["done"] == "yes" for row in rows)

    OUTPUT.parent.mkdir(exist_ok=True)
    im = Image.new("RGB", (1400, 880), "#F7F8FB")
    draw = ImageDraw.Draw(im)

    draw.rounded_rectangle((70, 60, 1330, 820), radius=34, fill="#FFFFFF", outline="#D8E0EC", width=2)
    draw.text((120, 110), "学习卡片统计仪表盘", fill="#162033", font=font(44, bold=True))
    draw.text((122, 166), "由 Python 读取 CSV 后自动生成，数据和图表可以重新检查。", fill="#526071", font=font(24))

    cards = [
        ("记录数", len(rows), "#2F6BFF"),
        ("已完成", done_count, "#24A06B"),
        ("平均时长", round(mean(minutes), 1), "#F28C28"),
        ("平均反应", round(mean(reaction)), "#7A5AF8"),
    ]
    for i, (label, value, color) in enumerate(cards):
        x = 120 + i * 300
        draw.rounded_rectangle((x, 235, x + 250, 365), radius=24, fill="#F1F5F9")
        draw.ellipse((x + 24, 264, x + 72, 312), fill=color)
        draw.text((x + 92, 258), label, fill="#526071", font=font(23, bold=True))
        draw.text((x + 92, 298), str(value), fill="#162033", font=font(34, bold=True))

    max_minutes = max(minutes)
    colors = ["#2F6BFF", "#24A06B", "#F28C28"]
    for i, row in enumerate(rows):
        value = int(row["minutes"])
        width = int(680 * value / max_minutes)
        draw_bar(draw, 150, 465 + i * 105, width, row["topic"], value, colors[i % len(colors)])

    draw.text((150, 760), "读图提示：每张图最好只帮助读者完成一个关键比较。", fill="#526071", font=font(24))
    im.save(OUTPUT, optimize=True)
    WEB_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUT, WEB_COPY)
    print("已生成", OUTPUT.relative_to(ROOT))
    print("已同步", WEB_COPY.relative_to(ROOT))


if __name__ == "__main__":
    main()
