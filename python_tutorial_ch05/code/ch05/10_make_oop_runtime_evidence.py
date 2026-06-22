"""Generate a runtime evidence snapshot for the chapter 05 OOP workflow."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch05").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch05" / "web"

EVIDENCE_MD = REPORTS / "ch05_oop_runtime_evidence.md"
EVIDENCE_PNG = OUTPUT / "ch05_oop_runtime_evidence.png"
ASSET_COPY = WEB_DIR / "ch05_oop_runtime_evidence.png"

CHECKS = [
    ("对象模型报告", "reports/ch05_oop_model_report.md"),
    ("对象模型预览图", "reports/ch05_oop_model_preview.png"),
    ("类职责卡片", "reports/ch05_design_cards.md"),
    ("对象协作消息图", "reports/ch05_object_collaboration_map.md"),
    ("对象质量回执", "reports/ch05_object_quality_receipt.md"),
    ("交付包 JSON", "output/ch05_object_delivery_package.json"),
    ("交付包报告", "reports/ch05_object_delivery_package.md"),
    ("GUI 对象模型 JSON", "output/ch05_gui_panel_object_model.json"),
    ("GUI 对象模型报告", "reports/ch05_gui_panel_object_model.md"),
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
        status = "就绪" if (ROOT / rel_path).exists() else "缺失"
        rows.append({"stage": label, "path": rel_path, "status": status})
    return rows


def write_markdown(rows: list[dict[str, str]]) -> None:
    REPORTS.mkdir(exist_ok=True)
    ready = sum(row["status"] == "就绪" for row in rows)
    lines = [
        "# 第5章 OOP 运行证据清单",
        "",
        "这份清单由 Python 生成，用来确认对象模型报告、职责卡片、协作图、质量回执、交付包和 GUI 面板对象模型都已经留下可复查文件。",
        "",
        f"- 通过项：{ready}/{len(rows)}",
        "",
        "| 环节 | 状态 | 证据路径 |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['stage']} | {row['status']} | `{row['path']}` |")
    lines.extend(
        [
            "",
            "复盘提示：面向对象不是只写出 `class`，而是让对象职责、协作消息和可交付文件都能被看见。",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(exist_ok=True)
    image = Image.new("RGB", (1700, 1180), "#F7F8FB")
    draw = ImageDraw.Draw(image)

    title_font = font(52, True)
    body_font = font(24)
    row_font = font(22)
    code_font = font(19)

    draw.rounded_rectangle((90, 70, 1610, 1095), radius=30, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.text((150, 125), "Windows PowerShell - OOP 运行证据", fill="#162033", font=title_font)
    draw.text((150, 200), "运行第5章脚本后，检查对象模型相关交付物是否都存在。", fill="#5F6673", font=body_font)

    terminal = (150, 270, 1550, 1010)
    draw.rounded_rectangle(terminal, radius=24, fill="#0B1B3A", outline="#102A56", width=2)
    draw.rectangle((150, 270, 1550, 325), fill="#102A56")
    draw.ellipse((182, 290, 202, 310), fill="#F87171")
    draw.ellipse((215, 290, 235, 310), fill="#FBBF24")
    draw.ellipse((248, 290, 268, 310), fill="#34D399")
    draw.text((300, 287), r"python code\ch05\10_make_oop_runtime_evidence.py", fill="#DCEBFF", font=code_font)

    y = 360
    commands = [
        r"PS> python code\ch05\06_make_object_collaboration_map.py",
        r"PS> python code\ch05\08_make_object_delivery_package.py",
        r"PS> python code\ch05\10_make_oop_runtime_evidence.py",
    ]
    for command in commands:
        draw.text((190, y), command, fill="#93C5FD", font=code_font)
        y += 36
    y += 22

    for row in rows:
        status_color = "#34D399" if row["status"] == "就绪" else "#F87171"
        draw.rounded_rectangle((190, y, 1510, y + 44), radius=12, fill="#102A56", outline="#1E3A8A", width=1)
        draw.ellipse((220, y + 13, 240, y + 33), fill=status_color)
        draw.text((270, y + 10), row["stage"], fill="#EAF2FF", font=row_font)
        draw.text((610, y + 10), row["status"], fill=status_color, font=row_font)
        draw.text((800, y + 12), row["path"], fill="#BFD7FF", font=code_font)
        y += 56

    ready = sum(row["status"] == "就绪" for row in rows)
    draw.rounded_rectangle((310, 1040, 1390, 1088), radius=18, fill="#ECFDF5", outline="#34D399", width=2)
    draw.text((610, 1054), f"就绪文件：{ready}/{len(rows)}", fill="#047857", font=body_font)

    image.save(EVIDENCE_PNG, optimize=True, quality=95)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(EVIDENCE_PNG, ASSET_COPY)


def main() -> None:
    rows = collect_rows()
    write_markdown(rows)
    write_preview(rows)
    print(f"已生成 {EVIDENCE_MD.relative_to(ROOT)}")
    print(f"已生成 {EVIDENCE_PNG.relative_to(ROOT)}")
    print(f"已同步 {ASSET_COPY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
