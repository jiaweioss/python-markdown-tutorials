"""Generate a runtime evidence snapshot for the chapter 04 GUI workflow."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch04" / "web"

EVIDENCE_MD = REPORTS / "ch04_gui_runtime_evidence.md"
EVIDENCE_PNG = OUTPUT / "ch04_gui_runtime_evidence.png"
ASSET_COPY = WEB_DIR / "ch04_gui_runtime_evidence.png"

CHECKS = [
    ("最小窗口截图", "assets/ch04/web/tkinter_hello_window.png"),
    ("卡片表单截图", "assets/ch04/web/tkinter_card_form_window.png"),
    ("Stroop 窗口截图", "assets/ch04/web/tkinter_stroop_window.png"),
    ("可用性报告", "reports/ch04_gui_usability_check.md"),
    ("反馈检查卡", "reports/ch04_gui_feedback_scorecard.md"),
    ("交互记录", "reports/ch04_interaction_receipt.md"),
    ("卡片成果记录", "reports/ch04_card_factory_delivery.md"),
    ("ch3 数据面板", "reports/ch04_ch03_data_gui_panel.md"),
    ("交互旅程图", "reports/ch04_gui_journey_storyboard.md"),
]


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/consolab.ttf") if bold else Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def collect_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for label, rel in CHECKS:
        path = ROOT / rel
        rows.append(
            {
                "stage": label,
                "path": rel,
                "status": "就绪" if path.exists() else "缺失",
            }
        )
    return rows


def write_markdown(rows: list[dict[str, str]]) -> None:
    REPORTS.mkdir(exist_ok=True)
    ready = sum(1 for row in rows if row["status"] == "就绪")
    lines = [
        "# 第4章 GUI 运行记录清单",
        "",
        "这份清单由 Python 生成，用来确认 Tkinter 窗口截图、可用性报告、交互记录和跨章节 GUI 面板是否已经留下学习记录。",
        "",
        f"- 通过项：{ready}/{len(rows)}",
        "",
        "| 环节 | 状态 | 文件路径 |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['stage']} | {row['status']} | `{row['path']}` |")
    lines.extend(
        [
            "",
            "复盘提示：GUI 学习不是只看窗口弹出，而是要能证明窗口、输入、反馈和输出文件形成了闭环。",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_preview(rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(exist_ok=True)
    image = Image.new("RGB", (1700, 1180), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((90, 70, 1610, 1095), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)

    title = font(52, True)
    body = font(24)
    row_font = font(20)
    code_font = font(18)

    draw.text((150, 125), "Windows PowerShell - GUI 运行记录", fill="#162033", font=title)
    draw.text((150, 198), "Tkinter 窗口、检查报告、交互记录和跨章节面板都要能复查。", fill="#5F6673", font=body)

    terminal = (150, 270, 1550, 1010)
    draw.rounded_rectangle(terminal, radius=24, fill="#0B1B3A", outline="#102A56", width=2)
    draw.rectangle((150, 270, 1550, 325), fill="#102A56")
    draw.ellipse((182, 290, 202, 310), fill="#F87171")
    draw.ellipse((215, 290, 235, 310), fill="#FBBF24")
    draw.ellipse((248, 290, 268, 310), fill="#34D399")
    draw.text((300, 287), "python code\\ch04\\10_make_gui_runtime_evidence.py", fill="#DCEBFF", font=code_font)

    y = 360
    draw.text((190, y), "PS> python code\\ch04\\04_gui_usability_check.py", fill="#93C5FD", font=code_font)
    y += 34
    draw.text((190, y), "PS> python code\\ch04\\06_make_interaction_receipt.py", fill="#93C5FD", font=code_font)
    y += 34
    draw.text((190, y), "PS> python code\\ch04\\10_make_gui_runtime_evidence.py", fill="#93C5FD", font=code_font)
    y += 52

    for row in rows:
        color = "#34D399" if row["status"] == "就绪" else "#F87171"
        draw.rounded_rectangle((190, y, 1510, y + 42), radius=12, fill="#102A56", outline="#1E3A8A", width=1)
        draw.ellipse((220, y + 13, 238, y + 31), fill=color)
        draw.text((265, y + 10), row["stage"], fill="#EAF2FF", font=row_font)
        draw.text((650, y + 10), row["status"], fill=color, font=row_font)
        draw.text((850, y + 11), row["path"], fill="#BFD7FF", font=code_font)
        y += 55

    draw.rounded_rectangle((260, 1040, 1440, 1088), radius=18, fill="#FFF7E8", outline="#F2B84B", width=2)
    draw.text((410, 1054), "GUI 的最后一步：别只说能弹窗，要能找到自己的运行记录。", fill="#8A5A00", font=body)

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
