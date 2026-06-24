"""Create a chart makeover and a visual-audit checklist for chapter 06."""

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
MAKEOVER = OUTPUT / "ch06_chart_makeover.png"
CHECK_MD = OUTPUT / "ch06_visual_check.md"
CHECK_PREVIEW = OUTPUT / "ch06_visual_check_preview.png"
WEB_DIR = ROOT / "assets" / "ch06" / "web"


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


def load_rows() -> list[dict[str, str]]:
    if not INPUT.exists():
        raise FileNotFoundError("请先运行 code/ch06/01_make_sample_csv.py。")
    with INPUT.open(encoding="utf-8") as file:
        return list(csv.DictReader(file))


def draw_bad_chart(draw: ImageDraw.ImageDraw, box, rows: list[dict[str, str]]) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill="#FFF1F2", outline="#FDA4AF", width=2)
    draw.text((x1 + 36, y1 + 30), "改造前", fill="#9F1239", font=font(32, True))
    draw.text((x1 + 36, y1 + 78), "太吵：颜色多、标签乱、重点不清", fill="#7F1D1D", font=font(21))

    colors = ["#EF4444", "#F97316", "#EAB308", "#22C55E", "#06B6D4", "#8B5CF6"]
    base = y2 - 70
    left = x1 + 80
    max_value = max(int(row["minutes"]) for row in rows)
    for i, row in enumerate(rows):
        x = left + i * 150
        h = int(int(row["minutes"]) / max_value * 340)
        draw.rectangle((x, base - h, x + 95, base), fill=colors[i % len(colors)], outline="#111827", width=3)
        draw.text((x - 14, base + 16), row["topic"], fill=colors[(i + 2) % len(colors)], font=font(22, True))
        draw.text((x + 5, base - h - 32), row["minutes"] + "分", fill="#111827", font=font(22, True))
    for gy in range(base - 330, base + 1, 55):
        draw.line((left - 25, gy, x2 - 55, gy), fill="#FCA5A5", width=2)


def draw_good_chart(draw: ImageDraw.ImageDraw, box, rows: list[dict[str, str]]) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill="#FFFFFF", outline="#D8E0EC", width=2)
    draw.text((x1 + 36, y1 + 30), "改造后", fill="#166534", font=font(32, True))
    draw.text((x1 + 36, y1 + 78), "干净：一条主色、直接标注、保留空白", fill="#365A46", font=font(21))

    base = y2 - 78
    left = x1 + 90
    max_value = max(int(row["minutes"]) for row in rows)
    for gy in range(base - 300, base + 1, 75):
        draw.line((left - 20, gy, x2 - 90, gy), fill="#E2E8F0", width=2)
    for i, row in enumerate(rows):
        x = left + i * 165
        value = int(row["minutes"])
        h = int(value / max_value * 300)
        color = "#2F6BFF" if row["done"] == "yes" else "#94A3B8"
        draw.rounded_rectangle((x, base - h, x + 92, base), radius=14, fill=color)
        draw.text((x + 14, base - h - 34), f"{value} 分", fill="#162033", font=font(22, True))
        draw.text((x - 8, base + 18), row["topic"], fill="#334155", font=font(22))
    avg = mean(int(row["minutes"]) for row in rows)
    y_avg = base - int(avg / max_value * 300)
    draw.line((left - 20, y_avg, x2 - 90, y_avg), fill="#F28C28", width=4)
    draw.rounded_rectangle((x2 - 250, y_avg + 10, x2 - 95, y_avg + 42), radius=12, fill="#FFF7E8", outline="#F2B84B", width=2)
    draw.text((x2 - 236, y_avg + 15), f"平均 {avg:.1f} 分", fill="#9A5A00", font=font(18, True))


def write_makeover(rows: list[dict[str, str]]) -> None:
    image = Image.new("RGB", (1600, 940), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.text((90, 62), "图表改造前后对比", fill="#162033", font=font(50, True))
    draw.text((90, 126), "同一份数据，换一种设计，信息密度和阅读压力完全不同。", fill="#5F6673", font=font(26))
    draw_bad_chart(draw, (90, 205, 760, 850), rows)
    draw_good_chart(draw, (840, 205, 1510, 850), rows)
    OUTPUT.mkdir(exist_ok=True)
    image.save(MAKEOVER, optimize=True, quality=95)


def write_audit(rows: list[dict[str, str]]) -> None:
    minutes = [int(row["minutes"]) for row in rows]
    lines = [
        "# 第6章图表审美检查单",
        "",
        "这份检查单由 Python 根据 `input/learning_records.csv` 生成。",
        "",
        f"- 数据行数：{len(rows)}",
        f"- 平均学习时长：{mean(minutes):.1f} 分钟",
        "- 主图建议：减少颜色数量，保留直接标注，突出平均线。",
        "- 检查问题：标题是否说人话？坐标是否可读？颜色是否真的有意义？",
        "",
        "| 检查项 | 当前建议 |",
        "| --- | --- |",
        "| 标题 | 写结论，不只写变量名 |",
        "| 颜色 | 一种主色 + 一种强调色 |",
        "| 标签 | 数据点少时直接标注 |",
        "| 网格 | 只保留帮助比较的浅色线 |",
        "| 输出 | 保存到 `output/`，方便复现 |",
    ]
    CHECK_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_audit_preview() -> None:
    image = Image.new("RGB", (1500, 930), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((90, 70, 1410, 850), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.text((150, 125), "图表审美检查单", fill="#162033", font=font(50, True))
    draw.text((150, 198), "一张图发布或归档前，先问这五个问题。", fill="#5F6673", font=font(27))
    rows = [
        ("标题", "写结论，不只写变量名"),
        ("颜色", "一主色 + 一强调色"),
        ("标注", "少量数据直接标注"),
        ("网格", "浅色辅助，不抢戏"),
        ("输出", "保存文件，方便复现"),
    ]
    y = 305
    for label, tip in rows:
        draw.rounded_rectangle((150, y, 1350, y + 70), radius=16, fill="#F1F5F9", outline="#E2E8F0", width=2)
        draw.text((190, y + 17), label, fill="#2F6BFF", font=font(25, True))
        draw.text((420, y + 17), tip, fill="#162033", font=font(25))
        y += 84
    draw.rounded_rectangle((270, 790, 1230, 845), radius=20, fill="#EEF6FF", outline="#9CC8FF", width=2)
    draw.text((340, 804), "报告：output/ch06_visual_check.md", fill="#28517A", font=font(22))
    image.save(CHECK_PREVIEW, optimize=True, quality=95)


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(MAKEOVER, WEB_DIR / MAKEOVER.name)
    shutil.copyfile(CHECK_PREVIEW, WEB_DIR / CHECK_PREVIEW.name)


def main() -> None:
    rows = load_rows()
    write_makeover(rows)
    write_audit(rows)
    write_audit_preview()
    copy_assets()
    print(f"已生成 {MAKEOVER.relative_to(ROOT)}")
    print(f"已生成 {CHECK_MD.relative_to(ROOT)}")
    print(f"已生成 {CHECK_PREVIEW.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
