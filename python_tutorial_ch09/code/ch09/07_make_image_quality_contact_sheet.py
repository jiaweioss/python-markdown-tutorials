"""Create a no-text image quality contact sheet for chapter 09."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ASSETS = Path("assets/ch09/web")
OUTPUT = Path("output")
REPORTS = Path("reports")
SOURCE_IMAGE = ASSETS / "fronalpstock_sample.jpg"
PREVIEW = OUTPUT / "ch09_image_quality_contact_sheet.png"
REPORT = REPORTS / "ch09_image_quality_contact_sheet.md"


def load_source() -> Image.Image:
    if SOURCE_IMAGE.exists():
        raw = Image.open(SOURCE_IMAGE)
        return ImageOps.exif_transpose(raw).convert("RGB")

    fallback = Image.new("RGB", (1200, 800), "#DDEBFF")
    return fallback


def frame(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    shown = ImageOps.fit(im, size, method=getattr(Image, "Resampling", Image).LANCZOS)
    panel = Image.new("RGB", (size[0] + 48, size[1] + 48), "#FFFFFF")
    panel.paste(shown, (24, 24))
    return panel


def make_preview() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = load_source()

    crop = ImageOps.fit(im, (900, 620), method=getattr(Image, "Resampling", Image).LANCZOS)
    gray = ImageOps.grayscale(im).convert("RGB")
    balanced = ImageEnhance.Color(im).enhance(1.15)
    balanced = ImageEnhance.Contrast(balanced).enhance(1.12)
    overdone = ImageEnhance.Contrast(im).enhance(1.75).filter(ImageFilter.SHARPEN)

    panels = [
        frame(im, (560, 360)),
        frame(crop, (560, 360)),
        frame(gray, (560, 360)),
        frame(balanced, (560, 360)),
        frame(overdone, (560, 360)),
        frame(ImageOps.posterize(im, 3), (560, 360)),
    ]

    out = Image.new("RGB", (1880, 1320), "#F7F8FB")
    positions = [(100, 80), (660, 80), (1220, 80), (100, 640), (660, 640), (1220, 640)]
    for panel, (x, y) in zip(panels, positions):
        out.paste(panel, (x, y))
    out.save(PREVIEW, optimize=True, quality=95)
    return PREVIEW


def make_report() -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第9章图像质量检查清单",
        "",
        "这张总览图故意不在图片里写解释文字。请先观察画面，再回到报告里复盘：",
        "",
        "| 观察点 | 复盘问题 |",
        "| --- | --- |",
        "| 尺寸 | 图片是否适合放进学习卡片，边缘有没有被裁掉关键信息？ |",
        "| 明暗 | 画面是否足够清楚，暗部和亮部有没有丢失层次？ |",
        "| 颜色 | 颜色增强是否服务信息表达，而不是单纯追求刺激？ |",
        "| 锐化 | 边缘是否更清楚，还是出现了不自然的噪点？ |",
        "| 复现 | 处理步骤是否能用代码重新生成，而不是靠手动试出来？ |",
        "",
        "图像处理不是给图片化妆到认不出自己，而是让材料更适合学习、实验和报告。",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT


def copy_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, ASSETS / PREVIEW.name)


def main() -> None:
    preview = make_preview()
    report = make_report()
    copy_assets()
    print("created image quality contact sheet:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
