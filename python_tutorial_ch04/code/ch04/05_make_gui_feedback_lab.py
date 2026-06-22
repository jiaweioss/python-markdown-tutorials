"""Generate GUI feedback and target-size visuals for chapter 04."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_DIR = Path("assets/ch04/web")
TARGET_LAB = OUTPUT / "ch04_target_feedback_lab.png"
SCORECARD = OUTPUT / "ch04_gui_feedback_scorecard.png"
SCORECARD_MD = REPORTS / "ch04_gui_feedback_scorecard.md"


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


def draw_button(draw: ImageDraw.ImageDraw, xy, label: str, fill: str, outline: str = "#D8E0EC") -> None:
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=3)
    x1, y1, x2, y2 = xy
    draw.text((x1 + 22, y1 + (y2 - y1 - 28) // 2), label, fill="#162033", font=font(24, True))


def make_target_lab() -> None:
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "GUI 目标与反馈实验", fill="#162033", font=font(48, True))
    d.text((150, 195), "按钮太小，用户会紧张；反馈太少，用户会怀疑。", fill="#5F6673", font=font(27))

    d.text((165, 285), "紧张模式", fill="#9F1239", font=font(30, True))
    for i, label in enumerate(["保存", "取消", "导出", "重置"]):
        x = 170 + i * 105
        draw_button(d, (x, 350, x + 82, 398), label, "#FFF1F2", "#FDA4AF")
    d.text((165, 450), "小按钮 + 挤在一起", fill="#7F1D1D", font=font(24))

    d.text((780, 285), "安心模式", fill="#166534", font=font(30, True))
    draw_button(d, (785, 345, 1045, 415), "保存卡片", "#DCFCE7", "#86EFAC")
    draw_button(d, (1075, 345, 1335, 415), "导出报告", "#E0F2FE", "#7DD3FC")
    d.rounded_rectangle((785, 470, 1335, 545), radius=18, fill="#F1F5F9", outline="#E2E8F0", width=2)
    d.text((820, 492), "状态：已保存到 cards/topic_card.md", fill="#166534", font=font(24, True))

    d.rounded_rectangle((210, 690, 1290, 765), radius=22, fill="#EEF6FF", outline="#9CC8FF", width=2)
    d.text((285, 711), "可用性经验：目标清楚、间距足够、操作后有反馈。", fill="#28517A", font=font(27, True))

    OUTPUT.mkdir(exist_ok=True)
    im.save(TARGET_LAB, optimize=True, quality=95)


def make_scorecard() -> None:
    checks = [
        ("目标", "按钮够大，手不抖"),
        ("间距", "控件之间有呼吸"),
        ("状态", "保存后有明确反馈"),
        ("错误", "出错时能恢复"),
        ("文案", "按钮文字像人话"),
    ]
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "GUI 反馈检查卡", fill="#162033", font=font(50, True))
    d.text((150, 198), "一个小窗口交给别人前，先过这五关。", fill="#5F6673", font=font(27))
    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8", "#18A9B5"]
    y = 305
    for i, (label, tip) in enumerate(checks):
        d.rounded_rectangle((150, y, 1350, y + 70), radius=16, fill="#F1F5F9", outline="#E2E8F0", width=2)
        d.ellipse((185, y + 20, 215, y + 50), fill=colors[i])
        d.text((245, y + 17), label, fill=colors[i], font=font(25, True))
        d.text((520, y + 17), tip, fill="#162033", font=font(25))
        y += 84
    d.rounded_rectangle((270, 790, 1230, 845), radius=20, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((350, 804), "报告：reports/ch04_gui_feedback_scorecard.md", fill="#8A5A00", font=font(22))
    im.save(SCORECARD, optimize=True, quality=95)

    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第4章 GUI 反馈检查卡",
        "",
        "| 检查项 | 判断问题 |",
        "| --- | --- |",
    ]
    for label, tip in checks:
        lines.append(f"| {label} | {tip} |")
    SCORECARD_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TARGET_LAB, WEB_DIR / TARGET_LAB.name)
    shutil.copyfile(SCORECARD, WEB_DIR / SCORECARD.name)


def main() -> None:
    make_target_lab()
    make_scorecard()
    copy_assets()
    print(f"已生成 {TARGET_LAB}")
    print(f"已生成 {SCORECARD}")
    print(f"已生成 {SCORECARD_MD}")


if __name__ == "__main__":
    main()
