"""Generate a runtime record for the chapter 02 data type workflow."""

from __future__ import annotations

import datetime as _dt
import shutil
from pathlib import Path


CHECKS = [
    ("学习记录", "output/ch02_learning_report.txt"),
    ("类型选择报告", "reports/ch02_type_decision_cards.md"),
    ("类型选择预览", "output/ch02_type_decision_cards_preview.png"),
    ("类型罗盘报告", "reports/ch02_type_compass.md"),
    ("类型罗盘预览", "output/ch02_type_compass_preview.png"),
    ("实验记录报告", "reports/ch02_data_type_lab_receipt.md"),
    ("实验记录图", "output/ch02_data_type_lab_receipt.png"),
    ("Stroop 报告", "reports/ch02_stroop_dataset_pack.md"),
    ("Stroop JSON", "output/ch02_stroop_dataset_pack.json"),
    ("Stroop CSV", "output/ch02_stroop_dataset_pack.csv"),
    ("Stroop 图", "output/ch02_stroop_dataset_pack.png"),
    ("标本柜报告", "reports/ch02_data_type_specimen_cabinet.md"),
    ("标本柜 JSON", "output/ch02_data_type_specimen_cabinet.json"),
    ("标本柜图", "output/ch02_data_type_specimen_cabinet.png"),
]


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch02").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def collect_status(root: Path) -> list[dict[str, str | int | bool]]:
    rows = []
    for label, rel_path in CHECKS:
        path = root / rel_path
        exists = path.exists()
        rows.append(
            {
                "label": label,
                "path": rel_path,
                "exists": exists,
                "size": path.stat().st_size if exists else 0,
            }
        )
    return rows


def build_report(rows: list[dict[str, str | int | bool]]) -> str:
    ready = sum(1 for row in rows if row["exists"])
    total = len(rows)
    lines = [
        "# 第2章数据类型运行记录",
        "",
        f"- 检查时间：{_dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 运行产物：{ready}/{total} ready",
        "- 说明：这份报告检查第2章的学习记录、类型选择工具、Stroop 数据包和数据类型标本柜是否已经生成。",
        "",
        "| 状态 | 产物 | 路径 | 大小 |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        status = "就绪" if row["exists"] else "缺失"
        size = f'{row["size"]} bytes' if row["exists"] else "-"
        lines.append(f'| {status} | {row["label"]} | `{row["path"]}` | {size} |')
    lines.append("")
    if ready == total:
        lines.append("结论：本章关键产物已经生成，可以把数据类型学习成果拿出来复盘。")
    else:
        lines.append("结论：仍有产物缺失，请先运行对应脚本。")
    return "\n".join(lines) + "\n"


def draw_runtime_image(path: Path, rows: list[dict[str, str | int | bool]]) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()

    width, height = 1800, 1120
    image = Image.new("RGB", (width, height), "#F6F8FB")
    draw = ImageDraw.Draw(image)

    title = font(54, True)
    subtitle = font(27)
    h2 = font(30, True)
    body = font(24)
    mono = font(22)
    small = font(18)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    ps_blue = "#062B58"
    green = "#24A06B"
    orange = "#F28C28"
    red = "#E84C61"

    def shadow_box(xy, fill="#FFFFFF", radius=26):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=line, width=2)

    ready = sum(1 for row in rows if row["exists"])
    total = len(rows)

    draw.text((92, 70), "PowerShell - 第2章数据类型运行记录", font=title, fill=ink)
    draw.text(
        (96, 144),
        "一章一张运行记录板：脚本、报告、JSON/CSV 和项目图片一起检查。",
        font=subtitle,
        fill=muted,
    )
    draw.line((96, 206, 1704, 206), fill=line, width=3)

    shadow_box((95, 260, 825, 980), fill=ps_blue, radius=28)
    terminal_lines = [
        "PS C:\\PythonMarkdown\\python_tutorial_ch02>",
        "python code\\ch02\\07_make_type_decision_cards.py",
        "python code\\ch02\\08_make_type_compass.py",
        "python code\\ch02\\09_make_data_type_lab_receipt.py",
        "python code\\ch02\\10_make_stroop_dataset_pack.py",
        "python code\\ch02\\11_make_data_type_specimen_cabinet.py",
        "python code\\ch02\\12_make_data_type_runtime_evidence.py",
        "",
        f"运行产物： {ready}/{total} ready",
        "状态：可以复查" if ready == total else "状态：仍有文件缺失",
    ]
    y = 306
    for line_text in terminal_lines:
        color = "#BEE3F8"
        if line_text.startswith("Runtime"):
            color = "#A7F3D0" if ready == total else "#FDE68A"
        if line_text.startswith("状态"):
            color = "#A7F3D0" if ready == total else "#FCA5A5"
        draw.text((132, y), line_text, font=mono, fill=color)
        y += 52 if line_text else 26

    shadow_box((875, 260, 1705, 980), radius=28)
    draw.text((925, 308), "产物检查清单", font=h2, fill=ink)
    draw.text((928, 356), "数据类型能落成文件，才真正能复查。", font=body, fill=muted)

    for i, row in enumerate(rows):
        col = i // 7
        slot = i % 7
        x = 925 + col * 385
        y = 425 + slot * 72
        exists = bool(row["exists"])
        status_color = green if exists else red
        draw.rounded_rectangle((x, y - 8, x + 98, y + 34), radius=21, fill=status_color)
        draw.text((x + 18, y), "就绪" if exists else "缺失", font=small, fill="white")
        file_name = Path(str(row["path"])).name
        if len(file_name) > 28:
            file_name = file_name[:25] + "..."
        draw.text((x + 112, y - 2), str(row["label"])[:20], font=body, fill=ink)
        draw.text((x + 112, y + 28), file_name, font=small, fill=muted)

    draw.rounded_rectangle((95, 1015, 1705, 1082), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw.text(
        (140, 1033),
        "经验提醒：数据类型练习要能留下文件、报告和数据，才算真正落地。",
        font=body,
        fill="#8A5A00",
    )

    if ready != total:
        draw.rounded_rectangle((1460, 70, 1705, 130), radius=30, fill=orange)
        draw.text((1512, 86), "检查", font=body, fill="white")

    image.save(path, optimize=True, quality=95)
    return True


def main() -> None:
    root = project_root()
    report_dir = root / "reports"
    output_dir = root / "output"
    web_dir = root / "assets" / "ch02" / "web"
    report_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    web_dir.mkdir(parents=True, exist_ok=True)

    rows = collect_status(root)
    report_file = report_dir / "ch02_data_type_runtime_evidence.md"
    image_file = output_dir / "ch02_data_type_runtime_evidence.png"
    web_file = web_dir / "ch02_data_type_runtime_evidence.png"

    report_file.write_text(build_report(rows), encoding="utf-8")
    image_ok = draw_runtime_image(image_file, rows)
    if image_ok:
        shutil.copy2(image_file, web_file)

    ready = sum(1 for row in rows if row["exists"])
    print(f"第2章运行记录：{ready}/{len(rows)} 就绪")
    print(f"report: {report_file}")
    if image_ok:
        print(f"image: {image_file}")


if __name__ == "__main__":
    main()
