"""Generate a visual-perception mini lab for the image-processing chapter."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ASSETS = Path("assets/ch09/web")
OUTPUT = Path("output")
REPORTS = Path("reports")
SOURCE_IMAGE = ASSETS / "fronalpstock_sample.jpg"


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def sample_image() -> Image.Image:
    if SOURCE_IMAGE.exists():
        raw = Image.open(SOURCE_IMAGE)
        return ImageOps.exif_transpose(raw).convert("RGB")
    im = Image.new("RGB", (960, 620), "#DDEBFF")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 380, 960, 620), fill="#5A8F55")
    d.polygon([(0, 420), (260, 170), (520, 420)], fill="#F8FAFC")
    d.polygon([(350, 430), (610, 130), (960, 430)], fill="#E2E8F0")
    return im


def make_illusion() -> Image.Image:
    im = Image.new("RGB", (520, 360), "#F7F8FB")
    d = ImageDraw.Draw(im)
    dark = "#4B5563"
    light = "#E5E7EB"
    same = "#9CA3AF"
    for row in range(6):
        for col in range(8):
            fill = dark if (row + col) % 2 == 0 else light
            d.rectangle((col * 65, row * 60, col * 65 + 65, row * 60 + 60), fill=fill)
    d.rectangle((135, 78, 255, 158), fill=same)
    d.rectangle((265, 198, 385, 278), fill=same)
    d.rectangle((135, 78, 255, 158), outline="#111827", width=4)
    d.rectangle((265, 198, 385, 278), outline="#111827", width=4)
    return im


def make_channel_panel(im: Image.Image) -> Image.Image:
    small = ImageOps.contain(im, (360, 250))
    panel = Image.new("RGB", (520, 360), "#FFFFFF")
    panel.paste(small, ((520 - small.width) // 2, 30))
    d = ImageDraw.Draw(panel)
    pixels = im.resize((1, 1)).getpixel((0, 0))
    labels = [("R", pixels[0], "#EF4444"), ("G", pixels[1], "#22C55E"), ("B", pixels[2], "#3B82F6")]
    x = 80
    for label, value, color in labels:
        d.rounded_rectangle((x, 300 - value, x + 80, 300), radius=12, fill=color)
        d.text((x + 22, 310), f"{label}:{value}", fill="#334155", font=font(18, True))
        x += 135
    return panel


def make_preview() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = sample_image()
    gray = ImageOps.grayscale(im)
    sharpen = im.filter(ImageFilter.SHARPEN)
    illusion = make_illusion()
    channel_panel = make_channel_panel(im)

    W, H = 1600, 1000
    out = Image.new("RGB", (W, H), "#F7F8FB")
    d = ImageDraw.Draw(out)
    d.rounded_rectangle((70, 55, 1530, 940), radius=34, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((130, 105), "视觉感知小实验", fill="#162033", font=font(56, True))
    d.text((130, 178), "同一张图，不同处理方式，会改变你注意到的信息。", fill="#5F6673", font=font(28))

    panels = [
        ("原图", ImageOps.contain(im, (520, 320))),
        ("灰度", ImageOps.contain(gray.convert("RGB"), (520, 320))),
        ("锐化", ImageOps.contain(sharpen, (520, 320))),
        ("同色错觉", illusion),
        ("RGB 均值", channel_panel),
    ]
    positions = [(130, 260), (610, 260), (1090, 260), (270, 615), (810, 615)]
    for (label, panel), (x, y) in zip(panels, positions):
        d.rounded_rectangle((x, y, x + 390, y + 245), radius=22, fill="#F1F5F9", outline="#E2E8F0", width=2)
        shown = ImageOps.contain(panel, (360, 190))
        out.paste(shown, (x + (390 - shown.width) // 2, y + 20))
        d.text((x + 24, y + 205), label, fill="#162033", font=font(24, True))

    d.rounded_rectangle((130, 895, 1470, 925), radius=15, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((160, 899), "提醒：图像处理能帮助看清结构，也可能制造误导。每一次增强、裁剪和配色，都要能解释目的。", fill="#1D4ED8", font=font(20))
    path = OUTPUT / "ch09_visual_perception_lab.png"
    out.save(path, optimize=True, quality=95)
    return path


def make_markdown() -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第9章视觉感知小实验",
        "",
        "本实验用同一张图片生成原图、灰度、锐化、RGB 均值和同色错觉图，帮助你区分“图像像素变化”和“人眼感知变化”。",
        "",
        "## 观察问题",
        "",
        "- 灰度图让哪些信息更突出？",
        "- 锐化是否真的增加了信息，还是只让边缘更强？",
        "- 同色错觉中两个色块像不像不同颜色？为什么？",
        "- 做科研配图时，哪些处理必须在图注或报告里说明？",
    ]
    path = REPORTS / "ch09_visual_perception_lab.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main():
    preview = make_preview()
    report = make_markdown()
    print("created visual perception lab:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
