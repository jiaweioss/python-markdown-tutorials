"""Draw Anscombe's quartet to show why charts matter.

Run after entering the chapter directory:
    python code/ch06/05_anscombe_quartet.py
"""

from pathlib import Path
import shutil
from statistics import mean

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "assets" / "ch06").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output" / "ch06_anscombe_quartet.png"
WEB_COPY = ROOT / "assets" / "ch06" / "web" / "ch06_anscombe_quartet_output.png"

DATASETS = {
    "I": [
        (10, 8.04),
        (8, 6.95),
        (13, 7.58),
        (9, 8.81),
        (11, 8.33),
        (14, 9.96),
        (6, 7.24),
        (4, 4.26),
        (12, 10.84),
        (7, 4.82),
        (5, 5.68),
    ],
    "II": [
        (10, 9.14),
        (8, 8.14),
        (13, 8.74),
        (9, 8.77),
        (11, 9.26),
        (14, 8.10),
        (6, 6.13),
        (4, 3.10),
        (12, 9.13),
        (7, 7.26),
        (5, 4.74),
    ],
    "III": [
        (10, 7.46),
        (8, 6.77),
        (13, 12.74),
        (9, 7.11),
        (11, 7.81),
        (14, 8.84),
        (6, 6.08),
        (4, 5.39),
        (12, 8.15),
        (7, 6.42),
        (5, 5.73),
    ],
    "IV": [
        (8, 6.58),
        (8, 5.76),
        (8, 7.71),
        (8, 8.84),
        (8, 8.47),
        (8, 7.04),
        (8, 5.25),
        (19, 12.50),
        (8, 5.56),
        (8, 7.91),
        (8, 6.89),
    ],
}


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


def draw_panel(draw: ImageDraw.ImageDraw, box, name: str, points, color: str):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=20, fill="#FFFFFF", outline="#D8E0EC", width=2)
    left, top, right, bottom = x1 + 70, y1 + 70, x2 - 45, y2 - 70
    draw.line((left, bottom, right, bottom), fill="#8A94A6", width=3)
    draw.line((left, top, left, bottom), fill="#8A94A6", width=3)

    def sx(value):
        return left + int((value - 3) / 17 * (right - left))

    def sy(value):
        return bottom - int((value - 2) / 12 * (bottom - top))

    for x, y in points:
        px, py = sx(x), sy(y)
        draw.ellipse((px - 7, py - 7, px + 7, py + 7), fill=color)

    draw.text((x1 + 28, y1 + 22), f"数据集 {name}", fill="#162033", font=font(25, True))
    mx = mean(x for x, _ in points)
    my = mean(y for _, y in points)
    draw.text((x1 + 28, y2 - 45), f"x 均值={mx:.1f}，y 均值={my:.1f}", fill="#5F6673", font=font(18))


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    im = Image.new("RGB", (1600, 1050), "#F7F8FB")
    draw = ImageDraw.Draw(im)
    draw.text((80, 55), "Anscombe 四重奏", fill="#162033", font=font(54, True))
    draw.text((82, 125), "摘要统计很接近，图形结构却完全不同。", fill="#5F6673", font=font(28))

    boxes = [(80, 210, 760, 570), (840, 210, 1520, 570), (80, 630, 760, 990), (840, 630, 1520, 990)]
    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]
    for (name, points), box, color in zip(DATASETS.items(), boxes, colors):
        draw_panel(draw, box, name, points, color)

    im.save(OUTPUT, optimize=True)
    WEB_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUT, WEB_COPY)
    print("已生成", OUTPUT.relative_to(ROOT))
    print("已同步", WEB_COPY.relative_to(ROOT))


if __name__ == "__main__":
    main()
