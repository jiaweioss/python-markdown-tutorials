"""Create a polished chart-style clinic board for chapter 06."""

from __future__ import annotations

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
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
CLINIC = OUTPUT / "ch06_chart_style_clinic.png"
REPORT = REPORTS / "ch06_chart_style_clinic.md"
WEB_COPY = ROOT / "assets" / "ch06" / "web" / "ch06_chart_style_clinic.png"


INK = "#162033"
MUTED = "#64748B"
BLUE = "#2F6BFF"
GREEN = "#24A06B"
ORANGE = "#F28C28"
RED = "#E84C61"
PURPLE = "#7A5AF8"
LINE = "#D8E0EC"


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def load_rows() -> list[dict[str, str]]:
    if not INPUT.exists():
        raise FileNotFoundError("请先运行 code/ch06/01_make_sample_csv.py。")
    with INPUT.open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def rounded(draw: ImageDraw.ImageDraw, box, fill="#FFFFFF", outline=LINE, radius=24, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_panel_title(draw: ImageDraw.ImageDraw, x: int, y: int, title: str, note: str) -> None:
    draw.text((x, y), title, fill=INK, font=font(25, True))
    draw.text((x, y + 34), note, fill=MUTED, font=font(17))


def draw_trend(draw: ImageDraw.ImageDraw, box, rows: list[dict[str, str]]) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box)
    draw_panel_title(draw, x1 + 28, y1 + 24, "趋势", "少量点也要能看出走向")
    values = [int(row["minutes"]) for row in rows]
    max_v = max(values)
    min_v = min(values)
    top = y1 + 120
    bottom = y2 - 74
    left = x1 + 70
    right = x2 - 60
    for gy in range(4):
        y = top + gy * (bottom - top) // 3
        draw.line((left, y, right, y), fill="#E8EEF6", width=2)
    pts = []
    for i, value in enumerate(values):
        x = left + i * (right - left) // max(len(values) - 1, 1)
        scale = (value - min_v) / max(max_v - min_v, 1)
        y = bottom - int(scale * (bottom - top))
        pts.append((x, y))
    draw.line(pts, fill=BLUE, width=6)
    for (x, y), row in zip(pts, rows):
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill="#FFFFFF", outline=BLUE, width=5)
        draw.text((x - 24, y - 42), f"{row['minutes']}分", fill=INK, font=font(17, True))
        draw.text((x - 22, bottom + 22), row["topic"], fill="#334155", font=font(17))


def draw_bars(draw: ImageDraw.ImageDraw, box, rows: list[dict[str, str]]) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box)
    draw_panel_title(draw, x1 + 28, y1 + 24, "重点", "一眼看出时间投给了谁")
    values = [int(row["minutes"]) for row in rows]
    max_v = max(values)
    base = y2 - 72
    left = x1 + 72
    gap = 132
    for i, row in enumerate(rows):
        value = int(row["minutes"])
        h = int(value / max_v * 210)
        x = left + i * gap
        color = BLUE if row["done"] == "yes" else "#94A3B8"
        draw.rounded_rectangle((x, base - h, x + 72, base), radius=14, fill=color)
        draw.text((x + 5, base - h - 30), f"{value}", fill=INK, font=font(18, True))
        draw.text((x - 2, base + 22), row["topic"], fill="#334155", font=font(17))
    avg = mean(values)
    y_avg = base - int(avg / max_v * 210)
    draw.line((x1 + 52, y_avg, x2 - 50, y_avg), fill=ORANGE, width=4)
    draw.text((x2 - 170, y_avg + 8), f"平均 {avg:.1f}", fill="#9A5A00", font=font(16, True))


def draw_completion(draw: ImageDraw.ImageDraw, box, rows: list[dict[str, str]]) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box)
    draw_panel_title(draw, x1 + 28, y1 + 24, "完成", "完成率先说清楚")
    done = sum(row["done"] == "yes" for row in rows)
    total = len(rows)
    pct = done / total
    cx, cy = x1 + 165, y1 + 220
    r = 86
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#F1F5F9", outline="#E2E8F0", width=8)
    draw.pieslice((cx - r, cy - r, cx + r, cy + r), start=-90, end=-90 + int(360 * pct), fill=GREEN)
    inner = r - 28
    draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner), fill="#FFFFFF")
    draw.text((cx - 52, cy - 22), f"{pct:.0%}", fill=INK, font=font(32, True))
    y = y1 + 152
    for row in rows:
        color = GREEN if row["done"] == "yes" else RED
        label = "完成" if row["done"] == "yes" else "待补"
        draw.ellipse((x1 + 300, y + 8, x1 + 318, y + 26), fill=color)
        draw.text((x1 + 332, y + 2), row["topic"], fill=INK, font=font(18, True))
        draw.text((x1 + 410, y + 2), label, fill=color, font=font(18, True))
        y += 54


def draw_reaction(draw: ImageDraw.ImageDraw, box, rows: list[dict[str, str]]) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box)
    draw_panel_title(draw, x1 + 28, y1 + 24, "反应时", "反应时像认知负荷温度计")
    values = [int(row["rt_ms"]) for row in rows]
    min_v, max_v = min(values), max(values)
    left = x1 + 92
    right = x2 - 175
    y = y1 + 155
    for row in rows:
        value = int(row["rt_ms"])
        scale = (value - min_v) / max(max_v - min_v, 1)
        x = left + int(scale * (right - left))
        color = RED if value == max_v else PURPLE
        draw.line((left, y + 14, right, y + 14), fill="#E2E8F0", width=5)
        draw.ellipse((x - 14, y, x + 14, y + 28), fill=color)
        draw.text((x1 + 34, y - 2), row["topic"], fill=INK, font=font(18, True))
        draw.text((x2 - 140, y - 2), f"{value} ms", fill=color, font=font(18, True))
        y += 62


def write_image(rows: list[dict[str, str]]) -> None:
    image = Image.new("RGB", (1700, 1120), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.text((100, 70), "图表审美诊所", fill=INK, font=font(56, True))
    draw.text((100, 138), "同一份学习记录，换成四张干净小图，结论会更愿意自己走出来。", fill=MUTED, font=font(27))
    draw.rounded_rectangle((1180, 72, 1550, 134), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=2)
    draw.text((1210, 90), "干净图表包", fill="#28517A", font=font(23, True))

    draw_trend(draw, (100, 220, 790, 570), rows)
    draw_bars(draw, (910, 220, 1600, 570), rows)
    draw_completion(draw, (100, 650, 790, 1000), rows)
    draw_reaction(draw, (910, 650, 1600, 1000), rows)
    draw.text((560, 1040), "由 code/ch06/10_make_chart_style_clinic.py 生成", fill="#5F6673", font=font(20))

    OUTPUT.mkdir(exist_ok=True)
    image.save(CLINIC, optimize=True, quality=95)


def write_report(rows: list[dict[str, str]]) -> None:
    minutes = [int(row["minutes"]) for row in rows]
    done = sum(row["done"] == "yes" for row in rows)
    slowest = max(rows, key=lambda row: int(row["rt_ms"]))
    lines = [
        "# 第6章图表审美诊所",
        "",
        "这份诊断单由 `10_make_chart_style_clinic.py` 根据 `input/learning_records.csv` 生成。",
        "",
        f"- 主题数：{len(rows)}",
        f"- 平均学习时长：{mean(minutes):.1f} min",
        f"- 完成率：{done / len(rows):.0%}",
        f"- 反应时最高主题：{slowest['topic']} ({slowest['rt_ms']} ms)",
        "",
        "图表建议：先让读者看见趋势，再看主题差异；用完成率回答进度问题，用反应时提示哪里可能需要复习。",
        "",
    ]
    REPORTS.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def copy_asset() -> None:
    WEB_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CLINIC, WEB_COPY)


def main() -> None:
    rows = load_rows()
    write_image(rows)
    write_report(rows)
    copy_asset()
    print(f"已生成 {CLINIC.relative_to(ROOT)}")
    print(f"已生成 {REPORT.relative_to(ROOT)}")
    print(f"已复制 {WEB_COPY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
