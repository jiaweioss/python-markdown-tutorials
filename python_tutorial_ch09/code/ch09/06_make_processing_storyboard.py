"""Create an image-processing storyboard for chapter 09."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


SOURCE = Path("assets/ch09/web/fronalpstock_sample.jpg")
OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_COPY = Path("assets/ch09/web/ch09_processing_storyboard.png")
STORYBOARD = OUTPUT / "ch09_processing_storyboard.png"
REPORT = REPORTS / "ch09_processing_storyboard.md"

INK = "#162033"
MUTED = "#64748B"
BLUE = "#2F6BFF"
GREEN = "#24A06B"
ORANGE = "#F28C28"
PURPLE = "#7A5AF8"
LINE = "#D8E0EC"


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


def load_source() -> Image.Image:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing source image: {SOURCE}")
    return ImageOps.exif_transpose(Image.open(SOURCE)).convert("RGB")


def fit_image(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    return ImageOps.fit(image, size, method=resampling)


def contain_image(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    resampling = getattr(Image, "Resampling", Image).LANCZOS
    return ImageOps.contain(image, size, method=resampling)


def make_steps(source: Image.Image) -> list[tuple[str, Image.Image, str]]:
    small = contain_image(source, (360, 220))
    gray = ImageOps.grayscale(source).convert("RGB")
    square = fit_image(source, (420, 420))
    enhanced = ImageEnhance.Contrast(source).enhance(1.28)
    enhanced = ImageEnhance.Color(enhanced).enhance(1.12).filter(ImageFilter.UnsharpMask(radius=1.4, percent=120))
    card = Image.new("RGB", (420, 420), "#F8FAFC")
    card_draw = ImageDraw.Draw(card)
    thumb = fit_image(enhanced, (360, 250))
    card.paste(thumb, (30, 35))
    card_draw.rounded_rectangle((30, 315, 390, 382), radius=18, fill="#FFFFFF", outline="#CBD5E1", width=2)
    card_draw.text((55, 332), "图片卡片", fill=INK, font=font(26, True))
    card_draw.text((55, 362), "已生成", fill=GREEN, font=font(18, True))
    return [
        ("原图", small, "保留原始记录。"),
        ("灰度", contain_image(gray, (360, 220)), "检查明暗。"),
        ("裁剪", square, "保留重点。"),
        ("增强", contain_image(enhanced, (360, 220)), "突出细节。"),
        ("卡片", card, "整理为素材。"),
    ]


def draw_step(draw: ImageDraw.ImageDraw, canvas: Image.Image, x: int, y: int, title: str, image: Image.Image, note: str, color: str) -> None:
    draw.rounded_rectangle((x, y, x + 270, y + 360), radius=26, fill="#FFFFFF", outline=LINE, width=2)
    draw.text((x + 24, y + 22), title, fill=INK, font=font(28, True))
    draw.text((x + 24, y + 58), note, fill=MUTED, font=font(17))
    frame = (x + 24, y + 98, x + 246, y + 306)
    draw.rounded_rectangle(frame, radius=20, fill="#F1F5F9", outline="#E2E8F0", width=2)
    shown = contain_image(image, (frame[2] - frame[0] - 12, frame[3] - frame[1] - 12))
    px = frame[0] + (frame[2] - frame[0] - shown.width) // 2
    py = frame[1] + (frame[3] - frame[1] - shown.height) // 2
    canvas.paste(shown, (px, py))
    draw.rounded_rectangle((x + 24, y + 322, x + 246, y + 342), radius=10, fill=color)


def write_storyboard(source: Image.Image) -> None:
    image = Image.new("RGB", (1700, 1000), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.text((100, 78), "图像处理流程故事板", fill=INK, font=font(56, True))
    draw.text((100, 146), "一张图片经过可回溯步骤，变成可用于卡片的素材。", fill=MUTED, font=font(25))

    steps = make_steps(source)
    xs = [100, 410, 720, 1030, 1340]
    colors = [BLUE, PURPLE, ORANGE, GREEN, "#0EA5E9"]
    for index, ((title, step_image, note), x, color) in enumerate(zip(steps, xs, colors), 1):
        draw_step(draw, image, x, 245, title, step_image, note, color)
        if index < len(steps):
            draw.line((x + 277, 425, x + 303, 425), fill="#94A3B8", width=5)
            draw.polygon([(x + 303, 425), (x + 289, 415), (x + 289, 435)], fill="#94A3B8")

    draw.rounded_rectangle((560, 720, 1140, 775), radius=24, fill="#FFFFFF", outline=LINE, width=2)
    draw.text((700, 736), "原图 -> 卡片素材", fill=INK, font=font(23, True))
    draw.text((610, 885), "由 code/ch09/10_make_processing_storyboard.py 生成", fill=MUTED, font=font(20))
    OUTPUT.mkdir(exist_ok=True)
    image.save(STORYBOARD, optimize=True, quality=95)


def write_report(source: Image.Image) -> None:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第9章图像处理故事板",
        "",
        "这份故事板由 `10_make_processing_storyboard.py` 生成，用同一张真实风景照片演示图像处理的连续步骤。",
        "",
        f"- 原图尺寸：{source.width} x {source.height}",
        "- 步骤：保留原图、灰度检查、裁剪主体、增强细节、导出卡片素材。",
        "- 原则：先保存原图，再生成派生图；每一步都应该能说清用途，而不是为了滤镜而滤镜。",
        "",
        "图像处理不是把照片变得更炫，而是让图片更适合它要完成的任务：讲解、比较、记录或分享。",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_asset() -> None:
    WEB_COPY.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(STORYBOARD, WEB_COPY)


def main() -> None:
    source = load_source()
    write_storyboard(source)
    write_report(source)
    copy_asset()
    print(f"已生成 {STORYBOARD}")
    print(f"已生成 {REPORT}")
    print(f"已复制 {WEB_COPY}")


if __name__ == "__main__":
    main()
