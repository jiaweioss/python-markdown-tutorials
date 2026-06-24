"""Create a GUI journey storyboard for chapter 04."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
WEB_DIR = ROOT / "assets" / "ch04" / "web"
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
STORYBOARD = OUTPUT / "ch04_gui_journey_storyboard.png"
REPORT = REPORTS / "ch04_gui_journey_storyboard.md"
WEB_COPY = WEB_DIR / "ch04_gui_journey_storyboard.png"

CARD_FORM = WEB_DIR / "tkinter_card_form_window.png"
DELIVERY = WEB_DIR / "ch04_card_factory_delivery.png"

INK = "#162033"
MUTED = "#64748B"
LINE = "#D8E0EC"
BLUE = "#2F6BFF"
GREEN = "#24A06B"
ORANGE = "#F28C28"
PURPLE = "#7A5AF8"
RED = "#E84C61"


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


def load_image(path: Path, fallback_color: str) -> Image.Image:
    if path.exists():
        return ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    image = Image.new("RGB", (420, 260), "#F8FAFC")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((40, 40, 380, 220), radius=28, fill="#FFFFFF", outline=fallback_color, width=5)
    draw.line((105, 130, 315, 130), fill=fallback_color, width=8)
    return image


def contain(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    return ImageOps.contain(image, size, method=resampling)


def draw_arrow(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.line((x, y, x + 38, y), fill="#94A3B8", width=5)
    draw.polygon([(x + 38, y), (x + 23, y - 10), (x + 23, y + 10)], fill="#94A3B8")


def draw_step(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    title: str,
    subtitle: str,
    image: Image.Image,
    color: str,
) -> None:
    draw.rounded_rectangle((x, y, x + 275, y + 365), radius=28, fill="#FFFFFF", outline=LINE, width=2)
    draw.text((x + 24, y + 24), title, fill=INK, font=font(29, True))
    draw.text((x + 24, y + 63), subtitle, fill=MUTED, font=font(17))
    frame = (x + 24, y + 105, x + 251, y + 292)
    draw.rounded_rectangle(frame, radius=22, fill="#F1F5F9", outline="#E2E8F0", width=2)
    thumb = contain(image, (frame[2] - frame[0] - 14, frame[3] - frame[1] - 14))
    canvas.paste(thumb, (frame[0] + (frame[2] - frame[0] - thumb.width) // 2, frame[1] + (frame[3] - frame[1] - thumb.height) // 2))
    draw.rounded_rectangle((x + 24, y + 320, x + 251, y + 342), radius=11, fill=color)


def simple_window(kind: str) -> Image.Image:
    image = Image.new("RGB", (430, 280), "#F8FAFC")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((34, 28, 396, 252), radius=28, fill="#FFFFFF", outline="#CBD5E1", width=3)
    draw.rectangle((34, 28, 396, 68), fill="#EFF6FF")
    draw.ellipse((56, 42, 70, 56), fill="#E84C61")
    draw.ellipse((80, 42, 94, 56), fill="#F2B84B")
    draw.ellipse((104, 42, 118, 56), fill="#24A06B")
    if kind == "type":
        draw.rounded_rectangle((72, 100, 360, 140), radius=12, fill="#F8FAFC", outline="#CBD5E1", width=2)
        draw.rounded_rectangle((72, 160, 360, 214), radius=12, fill="#F8FAFC", outline="#CBD5E1", width=2)
        draw.line((94, 121, 228, 121), fill=BLUE, width=5)
        draw.line((94, 185, 305, 185), fill=PURPLE, width=5)
    elif kind == "click":
        draw.rounded_rectangle((120, 132, 310, 190), radius=18, fill=BLUE)
        draw.polygon([(285, 172), (328, 208), (307, 213), (318, 239), (302, 244), (292, 218), (273, 232)], fill=INK)
    elif kind == "feedback":
        draw.rounded_rectangle((82, 118, 348, 180), radius=18, fill="#ECFDF5", outline="#A7F3D0", width=2)
        draw.ellipse((105, 139, 125, 159), fill=GREEN)
        draw.line((145, 149, 300, 149), fill=GREEN, width=6)
    return image


def write_storyboard() -> None:
    card_form = load_image(CARD_FORM, BLUE)
    delivery = load_image(DELIVERY, GREEN)
    steps = [
        ("打开", "窗口", card_form, BLUE),
        ("输入", "内容", simple_window("type"), PURPLE),
        ("点击", "按钮", simple_window("click"), ORANGE),
        ("反馈", "状态", simple_window("feedback"), GREEN),
        ("文件", "保存", delivery, RED),
    ]
    image = Image.new("RGB", (1720, 980), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.text((100, 72), "GUI 交互旅程图", fill=INK, font=font(56, True))
    draw.text((100, 140), "打开窗口  输入内容  点击按钮  看到反馈  得到文件", fill=MUTED, font=font(25))
    xs = [95, 415, 735, 1055, 1375]
    y = 245
    for idx, ((title, subtitle, step_image, color), x) in enumerate(zip(steps, xs)):
        draw_step(image, draw, x, y, title, subtitle, step_image, color)
        if idx < len(steps) - 1:
            draw_arrow(draw, x + 282, y + 184)
    draw.rounded_rectangle((575, 720, 1145, 775), radius=24, fill="#FFFFFF", outline=LINE, width=2)
    draw.text((704, 736), "输入 -> 动作 -> 结果", fill=INK, font=font(23, True))
    draw.text((600, 875), "由 code/ch04/09_make_gui_journey_storyboard.py 生成", fill=MUTED, font=font(20))
    OUTPUT.mkdir(exist_ok=True)
    image.save(STORYBOARD, optimize=True, quality=95)


def write_report() -> None:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第4章 GUI 交互旅程图",
        "",
        "这份故事板由 `09_make_gui_journey_storyboard.py` 生成，用来检查一个 Tkinter 小工具是否完成了清晰的用户旅程。",
        "",
        "- 打开窗口：用户能看见自己要做什么。",
        "- 输入内容：表单字段清楚，不让用户猜。",
        "- 点击按钮：动作入口明确。",
        "- 收到反馈：系统告诉用户已经发生了什么。",
        "- 得到文件：界面操作最终留下真实学习成果。",
        "",
        "GUI 不是给代码贴一层漂亮皮肤，而是让真实任务变得可完成、可确认、可复盘。",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_asset() -> None:
    WEB_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(STORYBOARD, WEB_COPY)


def main() -> None:
    write_storyboard()
    write_report()
    copy_asset()
    print(f"已生成 {STORYBOARD}")
    print(f"已生成 {REPORT}")
    print(f"已复制 {WEB_COPY}")


if __name__ == "__main__":
    main()
