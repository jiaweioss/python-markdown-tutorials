"""Generate a final runtime record snapshot for the office automation chapter."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch10").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch10" / "web"

EVIDENCE_MD = REPORTS / "final_runtime_evidence.md"
EVIDENCE_PNG = REPORTS / "final_runtime_evidence.png"
ASSET_COPY = WEB_DIR / "final_runtime_evidence.png"

CHECKS = [
    ("source csv", "input/report_data.csv"),
    ("markdown report", "reports/final_report.md"),
    ("word report", "reports/final_report.docx"),
    ("excel workbook", "reports/final_report.xlsx"),
    ("slides", "reports/final_slides.pptx"),
    ("report preview", "reports/final_report_preview.png"),
    ("excel preview", "reports/excel_workbook_preview.png"),
    ("成果索引", "reports/delivery_index.md"),
    ("打包记录", "reports/delivery_receipt.md"),
    ("成果 zip", "reports/ch10_delivery_package.zip"),
    ("zip 目录", "reports/delivery_package_manifest.md"),
    ("course portfolio", "reports/course_portfolio.md"),
    ("showcase board", "reports/final_showcase_board.png"),
    ("capstone dossier", "reports/capstone_handoff_dossier.png"),
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
        "# 第10章最终运行记录清单",
        "",
        "这份清单由 Python 生成，用来确认办公自动化章从输入数据到 Word、Excel、PPT、作品集、展示墙和 zip 成果包都已经留下可复查文件。",
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
            "复盘提示：办公自动化的最后一步不是生成一个文件，而是确认该打包的文件都能被找到、打开、解释和复用。",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(rows: list[dict[str, str]]) -> None:
    REPORTS.mkdir(exist_ok=True)
    image = Image.new("RGB", (1800, 1360), "#F7F8FB")
    draw = ImageDraw.Draw(image)

    title_font = font(50, True)
    body_font = font(24)
    row_font = font(21)
    code_font = font(18)

    draw.rounded_rectangle((90, 70, 1710, 1280), radius=30, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.text((150, 125), "Windows PowerShell - 最终运行记录", fill="#162033", font=title_font)
    draw.text((150, 197), "打包最终成果前，先集中检查办公自动化输出。", fill="#5F6673", font=body_font)

    terminal = (150, 265, 1650, 1188)
    draw.rounded_rectangle(terminal, radius=24, fill="#0B1B3A", outline="#102A56", width=2)
    draw.rectangle((150, 265, 1650, 320), fill="#102A56")
    draw.ellipse((182, 285, 202, 305), fill="#F87171")
    draw.ellipse((215, 285, 235, 305), fill="#FBBF24")
    draw.ellipse((248, 285, 268, 305), fill="#34D399")
    draw.text((300, 282), r"python code\ch10\11_make_final_runtime_evidence.py", fill="#DCEBFF", font=code_font)

    y = 352
    commands = [
        r"PS> python code\ch10\04_generate_office_pack.py",
        r"PS> python code\ch10\07_make_delivery_package.py",
        r"PS> python code\ch10\11_make_final_runtime_evidence.py",
    ]
    for command in commands:
        draw.text((190, y), command, fill="#93C5FD", font=code_font)
        y += 34
    y += 14

    for row in rows:
        status_color = "#34D399" if row["status"] == "ready" else "#F87171"
        draw.rounded_rectangle((190, y, 1610, y + 42), radius=12, fill="#102A56", outline="#1E3A8A", width=1)
        draw.ellipse((220, y + 12, 240, y + 32), fill=status_color)
        draw.text((270, y + 9), row["stage"], fill="#EAF2FF", font=row_font)
        draw.text((585, y + 9), row["status"], fill=status_color, font=row_font)
        draw.text((760, y + 11), row["path"], fill="#BFD7FF", font=code_font)
        draw.text((1390, y + 11), row["size"], fill="#D1FAE5", font=code_font)
        y += 46

    ready = sum(row["status"] == "ready" for row in rows)
    draw.rounded_rectangle((360, 1225, 1440, 1276), radius=18, fill="#ECFDF5", outline="#34D399", width=2)
    draw.text((780, 1240), f"就绪文件： {ready}/{len(rows)}", fill="#047857", font=body_font)

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
