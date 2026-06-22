"""Generate an interaction receipt for the Tkinter card factory panel."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CHECKS = [
    ("Goal", "OK", "Window purpose is visible."),
    ("Input", "OK", "Title and note fields are labeled."),
    ("Action", "OK", "Primary save button is easy to find."),
    ("Feedback", "OK", "Saved state is shown after click."),
    ("Recovery", "FIX", "Empty title needs a friendlier warning."),
]


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch04").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch04" / "web"
RECEIPT = OUTPUT / "ch04_interaction_receipt.png"
RECEIPT_MD = REPORTS / "ch04_interaction_receipt.md"


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


def draw_receipt() -> None:
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)

    d.rounded_rectangle((90, 70, 1410, 850), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "Interaction Receipt", fill="#162033", font=font(52, True))
    d.text((152, 200), "Generated after checking the Tkinter card panel.", fill="#5F6673", font=font(27))

    d.rounded_rectangle((150, 270, 520, 440), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=2)
    d.text((190, 305), "Run", fill="#28517A", font=font(27, True))
    d.text((190, 355), "card_form.py", fill="#162033", font=font(34, True))

    d.rounded_rectangle((565, 270, 935, 440), radius=24, fill="#ECFDF3", outline="#8EE3B0", width=2)
    d.text((605, 305), "Evidence", fill="#166534", font=font(27, True))
    d.text((605, 355), "saved card", fill="#162033", font=font(34, True))

    d.rounded_rectangle((980, 270, 1350, 440), radius=24, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((1020, 305), "Next", fill="#8A5A00", font=font(27, True))
    d.text((1020, 355), "better warning", fill="#162033", font=font(34, True))

    colors = {"OK": "#24A06B", "FIX": "#F28C28"}
    y = 495
    for label, status, note in CHECKS:
        d.rounded_rectangle((150, y, 1350, y + 50), radius=16, fill="#F1F5F9", outline="#E2E8F0", width=2)
        d.rounded_rectangle((180, y + 10, 275, y + 40), radius=15, fill=colors[status])
        d.text((206, y + 14), status, fill="#FFFFFF", font=font(17, True))
        d.text((320, y + 11), label, fill="#162033", font=font(23, True))
        d.text((520, y + 13), note, fill="#465263", font=font(20))
        y += 60

    d.rounded_rectangle((260, 815, 1240, 860), radius=18, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((335, 826), "Report: reports/ch04_interaction_receipt.md", fill="#465263", font=font(20))

    OUTPUT.mkdir(exist_ok=True)
    im.save(RECEIPT, optimize=True, quality=95)


def write_report() -> None:
    REPORTS.mkdir(exist_ok=True)
    ok_count = sum(1 for _, status, _ in CHECKS if status == "OK")
    fix_count = sum(1 for _, status, _ in CHECKS if status != "OK")
    lines = [
        "# 第4章 GUI 交互回执",
        "",
        "窗口能弹出来只是开门，交互回执说明用户走进去以后有没有路标、按钮、反馈和出口。",
        "",
        f"- 已通过检查：{ok_count} 项",
        f"- 需要继续打磨：{fix_count} 项",
        "",
        "| 检查项 | 状态 | 证据 |",
        "| --- | --- | --- |",
    ]
    for label, status, note in CHECKS:
        lines.append(f"| {label} | {status} | {note} |")
    lines.extend(
        [
            "",
            "下一步建议：优先改进空标题、空内容和保存失败时的提示文案。",
            "这份回执可以附在本章作业后面，作为 GUI 小作品的可用性证据。",
        ]
    )
    RECEIPT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RECEIPT, WEB_DIR / RECEIPT.name)


def main() -> None:
    draw_receipt()
    write_report()
    copy_asset()
    print(f"已生成 {RECEIPT.relative_to(ROOT)}")
    print(f"已生成 {RECEIPT_MD.relative_to(ROOT)}")
    print(f"已同步 {WEB_DIR.relative_to(ROOT) / RECEIPT.name}")


if __name__ == "__main__":
    main()
