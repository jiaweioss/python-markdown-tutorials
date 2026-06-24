"""Generate a runtime record snapshot for the chapter 08 web-scraping workflow."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch08").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch08" / "web"

EVIDENCE_MD = REPORTS / "ch08_scraper_runtime_evidence.md"
EVIDENCE_PNG = OUTPUT / "ch08_scraper_runtime_evidence.png"
ASSET_COPY = WEB_DIR / "ch08_scraper_runtime_evidence.png"

CHECKS = [
    ("links csv", "output/links.csv"),
    ("crawl report", "reports/ch08_crawl_report.md"),
    ("crawl preview", "reports/ch08_crawl_report_preview.png"),
    ("source cards", "reports/ch08_source_cards.md"),
    ("source card preview", "output/ch08_source_cards_preview.png"),
    ("etiquette card", "reports/ch08_crawl_etiquette_card.md"),
    ("quality scorecard", "reports/ch08_source_quality_scorecard.md"),
    ("public bundle json", "output/ch08_public_source_bundle.json"),
    ("public bundle report", "reports/ch08_public_source_bundle.md"),
    ("provenance archive", "reports/ch08_source_provenance_archive.md"),
]


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/consolab.ttf") if bold else Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def collect_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for label, rel_path in CHECKS:
        path = ROOT / rel_path
        rows.append(
            {
                "stage": label,
                "path": rel_path,
                "status": "ready" if path.exists() else "missing",
                "size": str(path.stat().st_size) if path.exists() else "-",
            }
        )
    return rows


def write_markdown(rows: list[dict[str, str]]) -> None:
    REPORTS.mkdir(exist_ok=True)
    ready = sum(row["status"] == "ready" for row in rows)
    lines = [
        "# 第8章爬虫运行记录清单",
        "",
        "这份清单由 Python 生成，用来确认链接 CSV、采集报告、来源卡片、爬虫礼仪卡、来源质量评分、公开资料包和来源追踪档案都已经留下可复查文件。",
        "",
        f"- 通过项：{ready}/{len(rows)}",
        "",
        "| 环节 | 状态 | 大小 bytes | 文件路径 |",
        "| --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['stage']} | {row['status']} | {row['size']} | `{row['path']}` |")
    lines.extend(
        [
            "",
            "复盘提示：爬虫不是把网页内容搬回来就结束，而是要能说明来源、规则、用途和保存路径。",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(exist_ok=True)
    image = Image.new("RGB", (1760, 1240), "#F7F8FB")
    draw = ImageDraw.Draw(image)

    title_font = font(50, True)
    body_font = font(24)
    row_font = font(21)
    code_font = font(18)

    draw.rounded_rectangle((90, 70, 1670, 1165), radius=30, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.text((150, 125), "Windows PowerShell - 爬虫运行记录", fill="#162033", font=title_font)
    draw.text((150, 198), "使用采集来源前，先检查本地爬虫输出。", fill="#5F6673", font=body_font)

    terminal = (150, 270, 1610, 1035)
    draw.rounded_rectangle(terminal, radius=24, fill="#0B1B3A", outline="#102A56", width=2)
    draw.rectangle((150, 270, 1610, 325), fill="#102A56")
    draw.ellipse((182, 290, 202, 310), fill="#F87171")
    draw.ellipse((215, 290, 235, 310), fill="#FBBF24")
    draw.ellipse((248, 290, 268, 310), fill="#34D399")
    draw.text((300, 287), r"python code\ch08\10_make_scraper_runtime_evidence.py", fill="#DCEBFF", font=code_font)

    y = 360
    commands = [
        r"PS> python code\ch08\03_save_links_csv.py",
        r"PS> python code\ch08\08_make_public_source_bundle.py",
        r"PS> python code\ch08\10_make_scraper_runtime_evidence.py",
    ]
    for command in commands:
        draw.text((190, y), command, fill="#93C5FD", font=code_font)
        y += 34
    y += 18

    for row in rows:
        status_color = "#34D399" if row["status"] == "ready" else "#F87171"
        draw.rounded_rectangle((190, y, 1570, y + 44), radius=12, fill="#102A56", outline="#1E3A8A", width=1)
        draw.ellipse((220, y + 13, 240, y + 33), fill=status_color)
        draw.text((270, y + 10), row["stage"], fill="#EAF2FF", font=row_font)
        draw.text((610, y + 10), row["status"], fill=status_color, font=row_font)
        draw.text((790, y + 12), row["path"], fill="#BFD7FF", font=code_font)
        draw.text((1410, y + 12), row["size"], fill="#D1FAE5", font=code_font)
        y += 56

    ready = sum(row["status"] == "ready" for row in rows)
    draw.rounded_rectangle((360, 1085, 1400, 1138), radius=18, fill="#ECFDF5", outline="#34D399", width=2)
    draw.text((760, 1101), f"就绪文件： {ready}/{len(rows)}", fill="#047857", font=body_font)

    image.save(EVIDENCE_PNG, optimize=True, quality=95)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(EVIDENCE_PNG, ASSET_COPY)


def main() -> None:
    rows = collect_rows()
    write_markdown(rows)
    write_preview(rows)
    print(f"generated {EVIDENCE_MD.relative_to(ROOT)}")
    print(f"generated {EVIDENCE_PNG.relative_to(ROOT)}")
    print(f"copied {ASSET_COPY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
