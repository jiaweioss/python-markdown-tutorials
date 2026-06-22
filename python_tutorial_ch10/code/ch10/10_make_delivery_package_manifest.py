"""Inspect the final zip package and render a delivery manifest preview."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw, ImageFont


REPORTS = Path("reports")
PACKAGE = REPORTS / "ch10_delivery_package.zip"
MANIFEST_MD = REPORTS / "delivery_package_manifest.md"
MANIFEST_PNG = REPORTS / "delivery_package_manifest.png"
ASSET_COPY = Path("assets/ch10/web/delivery_package_manifest.png")


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


def package_rows() -> list[dict[str, str | int]]:
    if not PACKAGE.exists():
        raise FileNotFoundError("请先运行 code/ch10/07_make_delivery_package.py 生成交付包。")

    rows: list[dict[str, str | int]] = []
    with ZipFile(PACKAGE) as zf:
        for info in sorted(zf.infolist(), key=lambda item: item.filename.lower()):
            rows.append(
                {
                    "file": info.filename,
                    "size": info.file_size,
                    "type": Path(info.filename).suffix.lower().lstrip(".") or "file",
                }
            )
    return rows


def write_manifest(rows: list[dict[str, str | int]]) -> None:
    lines = [
        "# 第10章交付包目录清单",
        "",
        "这份清单由 Python 打开 zip 交付包后生成，用来确认压缩包内部到底包含哪些文件。",
        "",
        f"- 交付包：`{PACKAGE.as_posix()}`",
        f"- 包内文件数：{len(rows)}",
        f"- 包大小：{PACKAGE.stat().st_size} bytes",
        "",
        "| 文件 | 类型 | 原始大小 bytes |",
        "| --- | --- | ---: |",
    ]
    for row in rows:
        lines.append(f"| `{row['file']}` | {row['type']} | {row['size']} |")
    MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(rows: list[dict[str, str | int]]) -> None:
    image = Image.new("RGB", (1700, 1320), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((90, 70, 1610, 1245), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)

    title_font = font(52, True)
    body_font = font(24)
    row_font = font(20)
    small_font = font(18)

    draw.text((150, 125), "Delivery Package Manifest", fill="#162033", font=title_font)
    draw.text((150, 200), "打开 zip 交付包，核对包内文件、类型和大小。", fill="#5F6673", font=body_font)

    package_size = PACKAGE.stat().st_size if PACKAGE.exists() else 0
    draw.rounded_rectangle((150, 255, 1550, 315), radius=18, fill="#EFF6FF", outline="#BFDBFE", width=2)
    draw.text((190, 270), f"Package: {PACKAGE.as_posix()}    Files: {len(rows)}    Size: {package_size} bytes", fill="#1E3A8A", font=small_font)

    y = 365
    headers = [("file", 180), ("type", 1030), ("size", 1240)]
    for label, x in headers:
        draw.text((x, y), label.upper(), fill="#64748B", font=font(18, True))
    y += 38

    colors = {
        "md": "#2F6BFF",
        "docx": "#2563EB",
        "xlsx": "#24A06B",
        "pptx": "#E6A600",
        "png": "#7A5AF8",
        "csv": "#18A9B5",
    }
    for row in rows[:14]:
        file_name = str(row["file"])
        file_type = str(row["type"])
        color = colors.get(file_type, "#64748B")
        draw.rounded_rectangle((150, y, 1550, y + 48), radius=14, fill="#F8FAFC", outline="#E2E8F0", width=2)
        draw.ellipse((180, y + 15, 200, y + 35), fill=color)
        draw.text((225, y + 11), file_name, fill="#162033", font=row_font)
        draw.rounded_rectangle((1025, y + 10, 1125, y + 38), radius=14, fill=color)
        draw.text((1050, y + 13), file_type, fill="#FFFFFF", font=small_font)
        draw.text((1240, y + 11), f"{row['size']} bytes", fill="#475569", font=row_font)
        y += 58

    if len(rows) > 14:
        draw.text((150, y + 10), f"... 还有 {len(rows) - 14} 个文件写入 Markdown 清单", fill="#64748B", font=small_font)

    draw.rounded_rectangle((150, 1145, 1550, 1202), radius=18, fill="#FFF7E8", outline="#F2B84B", width=2)
    draw.text((350, 1160), "交付前最后一问：压缩包里真的装了该交付的文件吗？", fill="#8A5A00", font=body_font)

    MANIFEST_PNG.parent.mkdir(parents=True, exist_ok=True)
    image.save(MANIFEST_PNG, optimize=True, quality=95)
    ASSET_COPY.parent.mkdir(parents=True, exist_ok=True)
    image.save(ASSET_COPY, optimize=True, quality=95)


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    rows = package_rows()
    write_manifest(rows)
    write_preview(rows)
    print(f"已生成 {MANIFEST_MD}")
    print(f"已生成 {MANIFEST_PNG}")


if __name__ == "__main__":
    main()
