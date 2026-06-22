"""Inspect image assets collected in chapter 08 and create an intake sheet."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch09").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
BOOK_ROOT = ROOT.parent
CH08_WEB = BOOK_ROOT / "python_tutorial_ch08" / "assets" / "ch08" / "web"
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch09" / "web"
INTAKE_JSON = OUTPUT / "ch09_ch08_image_intake.json"
REPORT = REPORTS / "ch09_ch08_image_intake.md"
PREVIEW = OUTPUT / "ch09_ch08_image_intake.png"


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


def image_files() -> list[Path]:
    suffixes = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    if not CH08_WEB.exists():
        return []
    files = [p for p in sorted(CH08_WEB.iterdir()) if p.suffix.lower() in suffixes]
    return files


def status_for(width: int, height: int) -> tuple[str, str]:
    long_side = max(width, height)
    short_side = min(width, height)
    ratio = width / height if height else 1
    if long_side < 700:
        return "review", "resolution"
    if short_side < 360:
        return "review", "thin crop"
    if ratio > 2.4 or ratio < 0.42:
        return "review", "extreme ratio"
    return "ready", "card source"


def collect_metadata() -> list[dict]:
    items = []
    for path in image_files():
        try:
            with Image.open(path) as im:
                im = ImageOps.exif_transpose(im)
                width, height = im.size
                status, note = status_for(width, height)
                items.append(
                    {
                        "file": path.name,
                        "format": im.format or path.suffix.upper().lstrip("."),
                        "mode": im.mode,
                        "width": width,
                        "height": height,
                        "status": status,
                        "note": note,
                    }
                )
        except Exception as exc:
            items.append(
                {
                    "file": path.name,
                    "format": "unknown",
                    "mode": "unknown",
                    "width": 0,
                    "height": 0,
                    "status": "error",
                    "note": str(exc)[:40],
                }
            )
    return items


def write_outputs(items: list[dict]) -> None:
    OUTPUT.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    INTAKE_JSON.write_text(json.dumps({"source": str(CH08_WEB), "images": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第9章 ch8 图像素材入库体检单",
        "",
        "这份体检单读取 ch8 的公开资料图片素材，检查格式、尺寸、比例和入库建议。图片进入教程前，不只要能打开，还要适合投屏、报告、卡片和后续处理。",
        "",
        "| 文件 | 格式 | 尺寸 | 模式 | 状态 | 提醒 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| `{item['file']}` | {item['format']} | {item['width']}x{item['height']} | "
            f"{item['mode']} | {item['status']} | {item['note']} |"
        )
    lines.extend(
        [
            "",
            "## 入库提醒",
            "",
            "- 尺寸太小的图，不适合放大投屏。",
            "- 比例极端的图，进入卡片前要先决定裁剪策略。",
            "- 所有图片都要保留来源记录，处理后的版本不要覆盖原图。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_preview(items: list[dict]) -> None:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((80, 65, 1420, 850), radius=32, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((135, 115), "Image Intake Sheet", fill="#162033", font=font(50, True))
    d.text((138, 178), "Chapter 08 source images checked before entering cards.", fill="#526071", font=font(24))

    selected = items[:6]
    if not selected:
        d.text((200, 420), "No images found in chapter 08 web assets.", fill="#E84C61", font=font(32, True))
    positions = [(135, 260), (540, 260), (945, 260), (135, 540), (540, 540), (945, 540)]
    for item, (x, y) in zip(selected, positions):
        d.rounded_rectangle((x, y, x + 330, y + 230), radius=22, fill="#F8FAFC", outline="#E2E8F0", width=2)
        source = CH08_WEB / item["file"]
        try:
            raw = Image.open(source)
            raw = ImageOps.exif_transpose(raw).convert("RGB")
            shown = ImageOps.contain(raw, (290, 128), method=getattr(Image, "Resampling", Image).LANCZOS)
            px = x + 20 + (290 - shown.width) // 2
            py = y + 18 + (128 - shown.height) // 2
            d.rounded_rectangle((x + 20, y + 18, x + 310, y + 146), radius=14, fill="#FFFFFF", outline="#D8E0EC", width=1)
            im.paste(shown, (px, py))
        except Exception:
            d.rounded_rectangle((x + 20, y + 18, x + 310, y + 146), radius=14, fill="#FEE2E2")
        color = "#24A06B" if item["status"] == "ready" else "#F28C28"
        d.rounded_rectangle((x + 20, y + 162, x + 118, y + 198), radius=18, fill=color)
        d.text((x + 42, y + 170), item["status"], fill="#FFFFFF", font=font(18, True))
        d.text((x + 135, y + 164), f"{item['width']}x{item['height']}", fill="#162033", font=font(21, True))
        d.text((x + 135, y + 194), item["format"], fill="#64748B", font=font(18))

    d.rounded_rectangle((250, 795, 1250, 840), radius=19, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((380, 806), "reports/ch09_ch08_image_intake.md", fill="#1D4ED8", font=font(22, True))
    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    items = collect_metadata()
    write_outputs(items)
    draw_preview(items)
    copy_asset()
    print(f"created {INTAKE_JSON.relative_to(ROOT)}")
    print(f"created {REPORT.relative_to(ROOT)}")
    print(f"created {PREVIEW.relative_to(ROOT)}")
    print(f"synced {WEB_DIR.relative_to(ROOT) / PREVIEW.name}")


if __name__ == "__main__":
    main()
