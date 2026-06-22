"""Generate a flow-tuning curve for the PyGame chapter."""

from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_DIR = Path("assets/ch07/web")
PREVIEW = OUTPUT / "ch07_flow_tuning_curve.png"
REPORT = REPORTS / "ch07_flow_tuning_curve.md"


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


def make_report() -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第7章心流难度调参曲线",
        "",
        "教学小游戏的目标不是把学生难住，而是让任务停在“够得着，但需要认真”的位置。",
        "",
        "| 区域 | 学生体验 | 调参建议 |",
        "| --- | --- | --- |",
        "| 低挑战 | 太容易，容易走神 | 缩短目标反应时，增加新刺激 |",
        "| 心流区 | 有压力但可完成 | 保持清晰反馈，逐步加一点变化 |",
        "| 高挑战 | 挫败、乱按、放弃 | 降低速度，增加提示或练习轮 |",
        "",
        "## 复盘问题",
        "",
        "- 你的小游戏现在更像低挑战、心流区，还是高挑战？",
        "- 失败时，程序有没有给出下一步提示？",
        "- 如果玩家连续三次失败，你会降低速度、给提示，还是只扣分？",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT


def point_on_curve(x: float) -> float:
    return math.exp(-((x - 0.52) ** 2) / 0.055)


def make_preview() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 830), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "Flow Tuning Curve", fill="#162033", font=font(52, True))

    chart = (210, 250, 1290, 675)
    x1, y1, x2, y2 = chart
    d.line((x1, y2, x2, y2), fill="#CBD5E1", width=5)
    d.line((x1, y1, x1, y2), fill="#CBD5E1", width=5)
    d.text((x1, y2 + 28), "low challenge", fill="#64748B", font=font(22))
    d.text((x2 - 145, y2 + 28), "high challenge", fill="#64748B", font=font(22))
    d.text((x1 - 35, y1 - 36), "engagement", fill="#64748B", font=font(22))

    flow_left = x1 + int((x2 - x1) * 0.35)
    flow_right = x1 + int((x2 - x1) * 0.70)
    d.rounded_rectangle((flow_left, y1 + 40, flow_right, y2 - 20), radius=22, fill="#ECFDF5", outline="#A7F3D0", width=3)
    d.text((flow_left + 88, y1 + 66), "FLOW", fill="#047857", font=font(38, True))

    curve = []
    for i in range(101):
        t = i / 100
        x = x1 + int((x2 - x1) * t)
        y = y2 - int((y2 - y1 - 30) * point_on_curve(t))
        curve.append((x, y))
    d.line(curve, fill="#2F6BFF", width=9, joint="curve")

    zones = [
        (0.18, "boredom", "#F28C28"),
        (0.52, "flow", "#24A06B"),
        (0.83, "anxiety", "#E84C61"),
    ]
    for t, label, color in zones:
        x = x1 + int((x2 - x1) * t)
        y = y2 - int((y2 - y1 - 30) * point_on_curve(t))
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=color)
        d.text((x - 46, y - 58), label, fill=color, font=font(24, True))

    metrics = [("Target", "620 ms"), ("Accuracy", "82%"), ("Retry", "high")]
    start_x = 330
    for i, (label, value) in enumerate(metrics):
        x = start_x + i * 285
        d.rounded_rectangle((x, 720, x + 230, 780), radius=18, fill="#F8FAFC", outline="#E2E8F0", width=2)
        d.text((x + 24, 733), label, fill="#64748B", font=font(20))
        d.text((x + 128, 728), value, fill="#162033", font=font(26, True))

    im.save(PREVIEW, optimize=True, quality=95)
    return PREVIEW


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    report = make_report()
    preview = make_preview()
    copy_assets()
    print("created flow tuning curve:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
