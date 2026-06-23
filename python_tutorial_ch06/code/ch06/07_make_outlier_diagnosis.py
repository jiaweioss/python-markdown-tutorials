"""Generate an outlier-diagnosis card for chapter 06."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from statistics import median

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
WEB_DIR = ROOT / "assets" / "ch06" / "web"
PREVIEW = OUTPUT / "ch06_outlier_diagnosis.png"
REPORT = REPORTS / "ch06_outlier_diagnosis.md"


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


def ensure_sample_csv() -> None:
    if INPUT.exists():
        return
    INPUT.parent.mkdir(exist_ok=True)
    INPUT.write_text(
        "\n".join(
            [
                "date,topic,minutes,done,reaction_time_ms",
                "2026-01-01,变量,25,yes,520",
                "2026-01-02,列表,35,yes,610",
                "2026-01-03,字典,42,yes,590",
                "2026-01-04,循环,30,no,760",
                "2026-01-05,函数,55,yes,640",
                "2026-01-06,文件,95,no,980",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def load_minutes() -> list[int]:
    ensure_sample_csv()
    with INPUT.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    values = [int(row["minutes"]) for row in rows]
    if len(values) < 5:
        values = values + [35, 38, 115]
    return values


def quartiles(values: list[int]) -> tuple[float, float, float]:
    values = sorted(values)
    q2 = median(values)
    middle = len(values) // 2
    lower = values[:middle]
    upper = values[-middle:]
    return median(lower), q2, median(upper)


def make_report(values: list[int]) -> Path:
    REPORTS.mkdir(exist_ok=True)
    q1, q2, q3 = quartiles(values)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    outliers = [v for v in values if v < low or v > high]
    lines = [
        "# 第6章异常值诊断卡",
        "",
        "探索性数据分析的第一步，不是立刻下结论，而是先看看数据有没有奇怪的地方。",
        "",
        "注：如果原始 CSV 记录不足 5 条，本脚本会临时加入几个“复盘日”演示值，只用于说明异常值诊断，不会改写原始 CSV。",
        "",
        f"- Q1：{q1:g}",
        f"- 中位数：{q2:g}",
        f"- Q3：{q3:g}",
        f"- IQR：{iqr:g}",
        f"- 低界：{low:g}",
        f"- 高界：{high:g}",
        f"- 可疑值：{', '.join(map(str, outliers)) if outliers else '暂无'}",
        "",
        "## 复盘问题",
        "",
        "- 这个异常值是记录错误，还是一次真实的困难学习？",
        "- 如果它是真实记录，下一步是否要回看当天任务？",
        "- 图表是否把异常值标出来，而不是悄悄平均掉？",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT


def x_for(value: float, min_v: float, max_v: float, left: int, right: int) -> int:
    return int(left + (value - min_v) / (max_v - min_v) * (right - left))


def make_preview(values: list[int]) -> Path:
    OUTPUT.mkdir(exist_ok=True)
    q1, q2, q3 = quartiles(values)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    whisker_low = min(v for v in values if v >= low)
    whisker_high = max(v for v in values if v <= high)
    outliers = [v for v in values if v < low or v > high]

    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 830), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "异常值诊断卡", fill="#162033", font=font(52, True))

    left, right = 220, 1280
    min_v = min(min(values), low) - 8
    max_v = max(max(values), high) + 8
    axis_y = 510
    d.line((left, axis_y, right, axis_y), fill="#CBD5E1", width=5)
    for tick in range(20, 111, 15):
        x = x_for(tick, min_v, max_v, left, right)
        d.line((x, axis_y - 16, x, axis_y + 16), fill="#94A3B8", width=3)
        d.text((x - 22, axis_y + 28), str(tick), fill="#64748B", font=font(18))

    x_low = x_for(whisker_low, min_v, max_v, left, right)
    x_q1 = x_for(q1, min_v, max_v, left, right)
    x_q2 = x_for(q2, min_v, max_v, left, right)
    x_q3 = x_for(q3, min_v, max_v, left, right)
    x_high = x_for(whisker_high, min_v, max_v, left, right)

    d.line((x_low, axis_y, x_q1, axis_y), fill="#2F6BFF", width=8)
    d.line((x_q3, axis_y, x_high, axis_y), fill="#2F6BFF", width=8)
    d.line((x_low, axis_y - 52, x_low, axis_y + 52), fill="#2F6BFF", width=6)
    d.line((x_high, axis_y - 52, x_high, axis_y + 52), fill="#2F6BFF", width=6)
    d.rounded_rectangle((x_q1, axis_y - 78, x_q3, axis_y + 78), radius=18, fill="#DBEAFE", outline="#2F6BFF", width=5)
    d.line((x_q2, axis_y - 78, x_q2, axis_y + 78), fill="#1D4ED8", width=6)

    for value in values:
        if value in outliers:
            continue
        x = x_for(value, min_v, max_v, left, right)
        d.ellipse((x - 9, axis_y - 9, x + 9, axis_y + 9), fill="#24A06B")
    for value in outliers:
        x = x_for(value, min_v, max_v, left, right)
        d.ellipse((x - 17, axis_y - 17, x + 17, axis_y + 17), fill="#E84C61")
        d.text((x - 45, axis_y - 70), f"{value} 分钟", fill="#E84C61", font=font(24, True))

    stats = [
        ("Q1", q1),
        ("中位数", q2),
        ("Q3", q3),
        ("四分位距", iqr),
        ("可疑值", len(outliers)),
    ]
    x = 190
    for label, value in stats:
        d.rounded_rectangle((x, 650, x + 210, 735), radius=20, fill="#F8FAFC", outline="#E2E8F0", width=2)
        d.text((x + 28, 666), label, fill="#64748B", font=font(22))
        d.text((x + 28, 696), f"{value:g}", fill="#162033", font=font(28, True))
        x += 240

    im.save(PREVIEW, optimize=True, quality=95)
    return PREVIEW


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    values = load_minutes()
    report = make_report(values)
    preview = make_preview(values)
    copy_assets()
    print("已生成异常值诊断：")
    print(f"- {report.relative_to(ROOT)}")
    print(f"- {preview.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
