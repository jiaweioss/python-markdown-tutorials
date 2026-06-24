"""Build a course portfolio summary from all chapter manifests."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
BOOK_ROOT = ROOT.parent
REPORTS = ROOT / "reports"
ASSET_COPY = ROOT / "assets" / "ch10" / "web" / "course_portfolio_preview.png"

CSV_OUT = REPORTS / "course_portfolio.csv"
MD_OUT = REPORTS / "course_portfolio.md"
PREVIEW_OUT = REPORTS / "course_portfolio_preview.png"


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


def chapter_number(path: Path) -> int:
    match = re.search(r"ch(\d+)$", path.name)
    return int(match.group(1)) if match else 999


def read_manifest(chapter_dir: Path) -> dict:
    manifest = chapter_dir / "manifest.json"
    if not manifest.exists():
        return {}
    return json.loads(manifest.read_text(encoding="utf-8"))


def count_markdown_images(text: str) -> int:
    html_count = len(re.findall(r"<img\b", text))
    markdown_count = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", text))
    return html_count + markdown_count


def collect_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for chapter_dir in sorted(BOOK_ROOT.glob("python_tutorial_ch*"), key=chapter_number):
        if not chapter_dir.is_dir():
            continue

        data = read_manifest(chapter_dir)
        chapter = data.get("chapter", {})
        md_rel = chapter.get("markdown", "")
        md_path = chapter_dir / md_rel if md_rel else None
        text = md_path.read_text(encoding="utf-8") if md_path and md_path.exists() else ""

        code_dir = chapter_dir / "code"
        py_scripts = sorted(code_dir.rglob("*.py")) if code_dir.exists() else []
        asset_dir = chapter_dir / "assets"
        assets = [p for p in asset_dir.rglob("*") if p.is_file()] if asset_dir.exists() else []

        chapter_id = chapter.get("id") or chapter_dir.name.replace("python_tutorial_", "")
        title = chapter.get("title") or chapter_dir.name
        rows.append(
            {
                "chapter": str(chapter_id),
                "title": str(title),
                "characters": len(text),
                "images": count_markdown_images(text),
                "python_scripts": len(py_scripts),
                "assets": len(assets),
                "status": "ready" if text and count_markdown_images(text) else "check",
            }
        )
    return rows


def write_csv(rows: list[dict[str, str | int]]) -> None:
    REPORTS.mkdir(exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["chapter", "title", "characters", "images", "python_scripts", "assets", "status"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str | int]]) -> None:
    total_images = sum(int(row["images"]) for row in rows)
    total_scripts = sum(int(row["python_scripts"]) for row in rows)
    total_assets = sum(int(row["assets"]) for row in rows)

    lines = [
        "# Python 教程课程作品集总览",
        "",
        "这份总览由第10章脚本自动生成，用来把 ch0-ch10 的教程正文、配图、脚本和素材数量汇总成一张结课文件清单。",
        "",
        f"- 章节数量：{len(rows)}",
        f"- 正文图片：{total_images}",
        f"- Python 脚本：{total_scripts}",
        f"- 素材文件：{total_assets}",
        "",
        "| 章节 | 标题 | 正文图片 | Python脚本 | 素材 | 状态 |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['chapter']} | {row['title']} | {row['images']} | "
            f"{row['python_scripts']} | {row['assets']} | {row['status']} |"
        )
    lines.extend(
        [
            "",
            "使用建议：把这份作品集当作结课汇报的目录页，先看每章是否有正文、图片和脚本，再回到对应章节补齐薄弱环节。",
        ]
    )
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def truncate(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt) -> str:
    if draw.textlength(text, font=fnt) <= max_width:
        return text
    ellipsis = "..."
    while text and draw.textlength(text + ellipsis, font=fnt) > max_width:
        text = text[:-1]
    return text + ellipsis


def draw_preview(rows: list[dict[str, str | int]]) -> None:
    image = Image.new("RGB", (1600, 1120), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    title_font = font(54, True)
    subtitle_font = font(24)
    metric_font = font(36, True)
    small_font = font(20)
    head_font = font(22, True)
    row_font = font(20)

    draw.rounded_rectangle((80, 65, 1520, 1045), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.text((135, 115), "Python Course Portfolio", fill="#162033", font=title_font)
    draw.text((137, 185), "ch0-ch10 课程作品集成果总览", fill="#5F6673", font=subtitle_font)

    total_images = sum(int(row["images"]) for row in rows)
    total_scripts = sum(int(row["python_scripts"]) for row in rows)
    total_assets = sum(int(row["assets"]) for row in rows)
    metrics = [
        ("Chapters", len(rows), "#2F6BFF"),
        ("Images", total_images, "#24A06B"),
        ("Python", total_scripts, "#F28C28"),
        ("Assets", total_assets, "#7A5AF8"),
    ]
    x = 135
    for label, value, color in metrics:
        draw.rounded_rectangle((x, 245, x + 300, 360), radius=20, fill="#F1F5F9", outline="#E2E8F0", width=2)
        draw.text((x + 28, 268), label, fill="#64748B", font=small_font)
        draw.text((x + 28, 300), str(value), fill=color, font=metric_font)
        x += 340

    table = (135, 420, 1465, 975)
    draw.rounded_rectangle(table, radius=18, fill="#FBFCFF", outline="#D8E0EC", width=2)
    headers = [("Chapter", 165), ("Title", 310), ("Images", 930), ("Py", 1070), ("Assets", 1195), ("Status", 1330)]
    for label, hx in headers:
        draw.text((hx, 445), label, fill="#334155", font=head_font)
    draw.line((165, 485, 1430, 485), fill="#D8E0EC", width=2)

    y = 505
    for i, row in enumerate(rows):
        fill = "#FFFFFF" if i % 2 == 0 else "#F6F8FC"
        draw.rounded_rectangle((155, y - 8, 1445, y + 36), radius=10, fill=fill)
        status_color = "#24A06B" if row["status"] == "ready" else "#E84C61"
        title = truncate(draw, str(row["title"]), 570, row_font)
        draw.text((165, y), str(row["chapter"]), fill="#162033", font=row_font)
        draw.text((310, y), title, fill="#162033", font=row_font)
        draw.text((950, y), str(row["images"]), fill="#2F6BFF", font=row_font)
        draw.text((1085, y), str(row["python_scripts"]), fill="#F28C28", font=row_font)
        draw.text((1220, y), str(row["assets"]), fill="#7A5AF8", font=row_font)
        draw.ellipse((1335, y + 7, 1353, y + 25), fill=status_color)
        draw.text((1365, y), str(row["status"]), fill=status_color, font=row_font)
        y += 45

    draw.rounded_rectangle((220, 1000, 1380, 1040), radius=18, fill="#FFF7E8", outline="#F2B84B", width=2)
    draw.text((365, 1008), "由 code/ch10/08_make_course_portfolio.py 生成", fill="#8A5A00", font=small_font)

    image.save(PREVIEW_OUT, optimize=True, quality=95)
    ASSET_COPY.parent.mkdir(parents=True, exist_ok=True)
    image.save(ASSET_COPY, optimize=True, quality=95)


def main() -> None:
    rows = collect_rows()
    write_csv(rows)
    write_markdown(rows)
    draw_preview(rows)
    print(f"已生成：{CSV_OUT}")
    print(f"已生成：{MD_OUT}")
    print(f"已生成：{PREVIEW_OUT}")
    print(f"已复制：{ASSET_COPY}")


if __name__ == "__main__":
    main()
