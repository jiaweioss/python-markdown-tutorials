"""Create a runtime record overview for chapter 09 image processing."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch09").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch09" / "web"

PREVIEW = OUTPUT / "ch09_image_runtime_evidence.png"
REPORT = REPORTS / "ch09_image_runtime_evidence.md"
ASSET_COPY = WEB_DIR / "ch09_image_runtime_evidence.png"

CHECKS = [
    ("示例原图", OUTPUT / "demo_card_image.png"),
    ("灰度图", OUTPUT / "demo_card_image_gray.png"),
    ("真实照片对比", OUTPUT / "fronalpstock_before_after.png"),
    ("处理报告", REPORTS / "ch09_image_processing_report.md"),
    ("报告预览", REPORTS / "ch09_image_processing_report_preview.png"),
    ("视觉实验报告", REPORTS / "ch09_visual_perception_lab.md"),
    ("视觉实验图", OUTPUT / "ch09_visual_perception_lab.png"),
    ("质量报告", REPORTS / "ch09_image_quality_contact_sheet.md"),
    ("质量总览", OUTPUT / "ch09_image_quality_contact_sheet.png"),
    ("第8章素材报告", REPORTS / "ch09_ch08_image_intake.md"),
    ("第8章素材 JSON", OUTPUT / "ch09_ch08_image_intake.json"),
    ("第8章素材图", OUTPUT / "ch09_ch08_image_intake.png"),
    ("流程故事板报告", REPORTS / "ch09_processing_storyboard.md"),
    ("流程故事板图", OUTPUT / "ch09_processing_storyboard.png"),
    ("记录档案报告", REPORTS / "ch09_visual_evidence_archive.md"),
    ("记录档案图", OUTPUT / "visual_evidence_archive.png"),
]


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


def status_rows() -> list[dict[str, str | int]]:
    rows = []
    for label, path in CHECKS:
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        rows.append(
            {
                "label": label,
                "path": path.relative_to(ROOT).as_posix(),
                "status": "就绪" if exists else "缺失",
                "bytes": size,
            }
        )
    return rows


def draw_preview(rows: list[dict[str, str | int]]) -> None:
    OUTPUT.mkdir(exist_ok=True)
    image = Image.new("RGB", (1760, 1320), "#F7F8FB")
    draw = ImageDraw.Draw(image)

    title_font = font(46, True)
    mono_font = font(25)
    small_font = font(21)

    draw.rounded_rectangle((85, 70, 1675, 1245), radius=34, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.rectangle((145, 130, 1615, 184), fill="#E7EEF7")
    draw.text((165, 143), "Windows PowerShell - 第9章图像运行记录", fill="#1B2733", font=small_font)
    draw.rectangle((145, 184, 1615, 1140), fill="#113A6B")

    y = 220
    draw.text((170, y), "PS> cd python_tutorial_ch09", fill="#59D9FF", font=mono_font)
    y += 38
    draw.text((170, y), "PS> 运行图像处理脚本 01..11", fill="#59D9FF", font=mono_font)
    y += 54

    ok_count = sum(1 for row in rows if row["status"] == "就绪")
    draw.text((170, y), f"运行产物： {ok_count}/{len(rows)} 就绪", fill="#68F06A", font=title_font)
    y += 72

    for row in rows:
        status = str(row["status"])
        color = "#68F06A" if status == "就绪" else "#FFB4B4"
        bytes_count = int(row["bytes"])
        size_text = f"{bytes_count / 1024:7.1f} KB" if bytes_count else "   --   "
        line = f"[{status:<7}] {row['label']:<24} {size_text}  {row['path']}"
        if len(line) > 102:
            line = line[:99] + "..."
        draw.text((170, y), line, fill=color if status != "就绪" else "#F3F8FF", font=mono_font)
        y += 43

    draw.text((170, 1165), "由 code/ch09/11_make_image_runtime_evidence.py 生成", fill="#64748B", font=small_font)
    image.save(PREVIEW, optimize=True, quality=95)


def write_report(rows: list[dict[str, str | int]]) -> None:
    REPORTS.mkdir(exist_ok=True)
    ready = sum(1 for row in rows if row["status"] == "就绪")
    lines = [
        "# 第9章图像处理运行记录",
        "",
        f"本报告由 `11_make_image_runtime_evidence.py` 生成，用来检查第9章关键图像处理产物是否已经落盘。当前状态：{ready}/{len(rows)} 就绪。",
        "",
        "| 项目 | 文件 | 状态 | 大小 |",
        "| --- | --- | --- | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['label']} | `{row['path']}` | {row['status']} | {int(row['bytes'])} |"
        )
    lines.extend(
        [
            "",
            "## 复盘提醒",
            "",
            "- 图像处理不要只留下最终图，也要留下原图、灰度图、处理报告和记录档案。",
            "- 图片进入教程、报告或课件前，至少检查尺寸、视野、清晰度和来源记录。",
            "- 如果某个项目显示 missing，先运行对应脚本，再重新运行本脚本。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, ASSET_COPY)


def main() -> None:
    rows = status_rows()
    draw_preview(rows)
    write_report(rows)
    copy_asset()
    print("已生成第9章图像运行记录：")
    print(f"- {REPORT}")
    print(f"- {PREVIEW}")
    print(f"- {ASSET_COPY}")


if __name__ == "__main__":
    main()
