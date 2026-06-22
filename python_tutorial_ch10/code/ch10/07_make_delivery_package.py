"""Package generated office artifacts and write a delivery receipt."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image, ImageDraw, ImageFont


REPORTS = Path("reports")
PACKAGE = REPORTS / "ch10_delivery_package.zip"
RECEIPT = REPORTS / "delivery_receipt.md"
PREVIEW = REPORTS / "delivery_receipt_preview.png"
ASSET_COPY = Path("assets/ch10/web/delivery_receipt_preview.png")

FILES = [
    "final_report.md",
    "final_report.docx",
    "final_report.xlsx",
    "final_slides.pptx",
    "final_report_preview.png",
    "excel_workbook_preview.png",
    "delivery_index.md",
    "course_portfolio.csv",
    "course_portfolio.md",
    "course_portfolio_preview.png",
    "final_showcase_board.md",
    "final_showcase_board.png",
    "capstone_handoff_dossier.md",
    "capstone_handoff_dossier.png",
]


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


def collect_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for name in FILES:
        path = REPORTS / name
        rows.append(
            {
                "file": name,
                "status": "ready" if path.exists() else "missing",
                "size": path.stat().st_size if path.exists() else 0,
            }
        )
    return rows


def make_zip(rows: list[dict[str, str | int]]) -> None:
    ready_files = [REPORTS / str(row["file"]) for row in rows if row["status"] == "ready"]
    with ZipFile(PACKAGE, "w", compression=ZIP_DEFLATED) as zf:
        for path in ready_files:
            zf.write(path, arcname=path.name)


def write_receipt(rows: list[dict[str, str | int]]) -> None:
    lines = [
        "# 第10章交付回执",
        "",
        "这份回执由 Python 生成，用来记录最终打包前的文件状态。",
        "",
        f"- 交付包：`{PACKAGE.as_posix()}`",
        f"- 包大小：{PACKAGE.stat().st_size if PACKAGE.exists() else 0} bytes",
        "",
        "| 文件 | 状态 | 大小 bytes |",
        "| --- | --- | ---: |",
    ]
    for row in rows:
        lines.append(f"| `{row['file']}` | {row['status']} | {row['size']} |")
    RECEIPT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(rows: list[dict[str, str | int]]) -> None:
    image = Image.new("RGB", (1700, 1260), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((90, 70, 1610, 1175), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.text((150, 125), "Delivery Receipt", fill="#162033", font=font(52, True))
    draw.text((150, 200), "打包前检查文件状态，给交付物留一张回执。", fill="#5F6673", font=font(28))

    y = 290
    for row in rows:
        color = "#24A06B" if row["status"] == "ready" else "#E84C61"
        draw.rounded_rectangle((150, y, 1550, y + 44), radius=14, fill="#F1F5F9", outline="#E2E8F0", width=2)
        draw.ellipse((180, y + 14, 198, y + 32), fill=color)
        draw.text((225, y + 8), str(row["file"]), fill="#162033", font=font(20))
        draw.text((1020, y + 8), str(row["status"]), fill=color, font=font(20, True))
        draw.text((1250, y + 8), f"{row['size']} bytes", fill="#5F6673", font=font(20))
        y += 52

    draw.rounded_rectangle((250, 1045, 1450, 1095), radius=18, fill="#FFF7E8", outline="#F2B84B", width=2)
    draw.text((440, 1057), "Package: reports/ch10_delivery_package.zip", fill="#8A5A00", font=font(20))

    image.save(PREVIEW, optimize=True, quality=95)
    ASSET_COPY.parent.mkdir(parents=True, exist_ok=True)
    image.save(ASSET_COPY, optimize=True, quality=95)


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    rows = collect_rows()
    make_zip(rows)
    write_receipt(rows)
    write_preview(rows)
    print(f"已生成 {PACKAGE}")
    print(f"已生成 {RECEIPT}")
    print(f"已生成 {PREVIEW}")


if __name__ == "__main__":
    main()
