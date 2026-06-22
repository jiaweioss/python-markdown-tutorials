"""Create a delivery index for generated office automation artifacts."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPORTS = Path("reports")
EXPECTED = [
    ("final_report.md", "Markdown quick review"),
    ("final_report.docx", "Word formal report"),
    ("final_report.xlsx", "Excel data workbook"),
    ("final_slides.pptx", "PPT presentation"),
    ("final_report_preview.png", "visual report preview"),
]


def font(size):
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def collect_rows():
    rows = []
    for name, purpose in EXPECTED:
        path = REPORTS / name
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        rows.append(
            {
                "file": name,
                "purpose": purpose,
                "status": "ready" if exists else "missing",
                "size": size,
            }
        )
    return rows


def write_markdown(rows):
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第10章交付索引",
        "",
        "这份索引由 Python 自动扫描 `reports/` 目录生成，用来确认办公自动化成果是否齐全。",
        "",
        "| 文件 | 用途 | 状态 | 大小 bytes |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['file']} | {row['purpose']} | {row['status']} | {row['size']} |")
    lines.extend(
        [
            "",
            "复盘提示：办公自动化不是只生成文件，还要留下可检查的交付记录。",
        ]
    )
    path = REPORTS / "delivery_index.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_preview(rows):
    im = Image.new("RGB", (1500, 980), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 900), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "第10章交付索引", fill="#162033", font=font(54))
    d.text((150, 205), "Python 自动扫描 reports/，确认成品文件是否齐全。", fill="#5F6673", font=font(28))

    x0, y0 = 150, 300
    widths = [360, 430, 160, 190]
    headers = ["文件", "用途", "状态", "大小"]
    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]
    x = x0
    for header, width, color in zip(headers, widths, colors):
        d.rounded_rectangle((x, y0, x + width, y0 + 58), radius=12, fill=color)
        d.text((x + 22, y0 + 13), header, fill="#FFFFFF", font=font(25))
        x += width + 12

    for r, row in enumerate(rows):
        y = y0 + 88 + r * 78
        values = [row["file"], row["purpose"], row["status"], str(row["size"])]
        x = x0
        for value, width in zip(values, widths):
            fill = "#ECFDF5" if value == "ready" else "#FEF2F2"
            if value not in {"ready", "missing"}:
                fill = "#F1F5F9"
            d.rounded_rectangle((x, y, x + width, y + 56), radius=12, fill=fill, outline="#E2E8F0", width=2)
            d.text((x + 18, y + 14), value, fill="#162033", font=font(22))
            x += width + 12

    path = REPORTS / "delivery_index_preview.png"
    im.save(path, optimize=True, quality=95)
    return path


def main():
    rows = collect_rows()
    md = write_markdown(rows)
    preview = write_preview(rows)
    print("已生成交付索引：")
    print(f"- {md}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
