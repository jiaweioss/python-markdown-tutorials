"""Generate an image-processing report preview for the chapter project."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "reports"
OUTPUT = ROOT / "output"
WEB = ROOT / "assets" / "ch09" / "web"


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def ensure_inputs():
    required = [
        OUTPUT / "demo_card_image.png",
        OUTPUT / "demo_card_image_gray.png",
        OUTPUT / "fronalpstock_before_after.png",
        WEB / "pillars_of_creation.jpg",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        names = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"请先运行前面的图像处理脚本，缺少：{names}")
    return required


def image_info(path: Path):
    with Image.open(path) as im:
        return im.size, im.mode


def make_markdown(paths):
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第9章图像处理报告",
        "",
        "| 文件 | 尺寸 | 模式 | 用途 |",
        "| --- | --- | --- | --- |",
    ]
    uses = {
        "demo_card_image.png": "程序生成的学习卡片配图",
        "demo_card_image_gray.png": "灰度转换结果",
        "fronalpstock_before_after.png": "真实照片处理前后对比",
        "pillars_of_creation.jpg": "科学图像素材，用于理解图像增强和表达",
    }
    for path in paths:
        size, mode = image_info(path)
        lines.append(f"| {path.name} | {size[0]}x{size[1]} | {mode} | {uses[path.name]} |")
    report = REPORTS / "ch09_image_processing_report.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    return report


def paste_contained(base, src_path, box):
    x1, y1, x2, y2 = box
    with Image.open(src_path) as src:
        src = ImageOps.exif_transpose(src).convert("RGB")
        resampling = getattr(Image, "Resampling", Image).LANCZOS
        shown = ImageOps.contain(src, (x2 - x1, y2 - y1), method=resampling)
    x = x1 + (x2 - x1 - shown.width) // 2
    y = y1 + (y2 - y1 - shown.height) // 2
    base.paste(shown, (x, y))


def make_preview(paths):
    REPORTS.mkdir(exist_ok=True)
    im = Image.new("RGB", (1600, 980), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1510, 910), radius=30, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "学习卡片配图处理报告", fill="#162033", font=font(52, True))
    d.text((150, 200), "生成图、灰度图、真实照片对比和科学图像素材，一次性复查。", fill="#5F6673", font=font(29))

    boxes = [
        (150, 300, 520, 535),
        (560, 300, 930, 535),
        (970, 300, 1390, 535),
        (150, 610, 520, 835),
    ]
    labels = ["生成卡片", "灰度转换", "真实照片对比", "科学图像素材"]
    for box, path, label in zip(boxes, paths, labels):
        d.rounded_rectangle(box, radius=20, fill="#F1F5F9", outline="#E2E8F0", width=2)
        paste_contained(im, path, (box[0] + 18, box[1] + 18, box[2] - 18, box[3] - 58))
        d.text((box[0] + 22, box[3] - 42), label, fill="#162033", font=font(23, True))

    d.rounded_rectangle((560, 610, 1390, 835), radius=22, fill="#EFF6FF", outline="#BFDBFE", width=2)
    notes = [
        "检查顺序：尺寸 -> 色彩模式 -> 视野变化 -> 是否覆盖原图",
        "科研用途：刺激材料统一尺寸，报告配图统一风格，原始图保留备份",
        "审美原则：结果要清楚，不要为了滤镜牺牲信息",
    ]
    y = 645
    for note in notes:
        d.text((600, y), note, fill="#1E3A8A", font=font(26))
        y += 58

    preview = REPORTS / "ch09_image_processing_report_preview.png"
    im.save(preview, optimize=True, quality=95)
    return preview


def main():
    paths = ensure_inputs()
    report = make_markdown(paths)
    preview = make_preview(paths)
    print("已生成图像处理报告：")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
