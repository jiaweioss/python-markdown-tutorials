"""Create a before/after image-processing sheet from a real photo."""

from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


SOURCE = Path("assets/ch09/web/fronalpstock_sample.jpg")
OUTPUT = Path("output/fronalpstock_before_after.png")


def fit(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    fitted = ImageOps.contain(im, size)
    canvas = Image.new("RGB", size, "#F2F4F8")
    x = (size[0] - fitted.width) // 2
    y = (size[1] - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    return canvas


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    raw = Image.open(SOURCE).convert("RGB")
    small = raw.resize((raw.width // 2, raw.height // 2))
    gray = ImageOps.grayscale(raw).convert("RGB")
    w, h = raw.size
    crop = raw.crop((w // 4, h // 4, w * 3 // 4, h * 3 // 4)).filter(ImageFilter.SHARPEN)

    panels = [raw, small, gray, crop]
    sheet = Image.new("RGB", (1400, 900), "#F7F8FB")
    positions = [(70, 70), (720, 70), (70, 480), (720, 480)]
    for panel, pos in zip(panels, positions):
        framed = fit(panel, (610, 340))
        sheet.paste(framed, pos)

    sheet.save(OUTPUT, optimize=True)
    print("已生成", OUTPUT)


if __name__ == "__main__":
    main()
