"""Chapter 06 artifact: collect runtime evidence for data analysis outputs."""

from __future__ import annotations

import datetime as _dt
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CHECKS = [
    ("样例 CSV", "input/learning_records.csv"),
    ("仪表盘图", "output/ch06_learning_dashboard.png"),
    ("Anscombe 图", "output/ch06_anscombe_quartet.png"),
    ("图表改造图", "output/ch06_chart_makeover.png"),
    ("审美检查单", "output/ch06_visual_check.md"),
    ("检查单预览", "output/ch06_visual_check_preview.png"),
    ("异常值报告", "reports/ch06_outlier_diagnosis.md"),
    ("异常值图", "output/ch06_outlier_diagnosis.png"),
    ("交接报告", "reports/ch06_ch05_handoff_analysis.md"),
    ("交接 JSON", "output/ch06_ch05_handoff_summary.json"),
    ("交接图", "output/ch06_ch05_handoff_analysis.png"),
    ("复习报告", "reports/ch06_memory_review_plan.md"),
    ("复习 JSON", "output/ch06_memory_review_plan.json"),
    ("复习曲线", "output/ch06_memory_review_plan.png"),
    ("审美诊所报告", "reports/ch06_chart_style_clinic.md"),
    ("审美诊所图", "output/ch06_chart_style_clinic.png"),
]


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch06").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/consolab.ttf") if bold else Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def collect_rows(root: Path) -> list[dict[str, str | int | bool]]:
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
        "# 第6章数据分析运行记录",
        "",
        f"- 检查时间：{_dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 运行产物：{ready}/{total} 就绪",
        "- 说明：这份报告检查本章 CSV、仪表盘、图表改造、异常值诊断、记忆复习计划、跨章节交接和图表审美诊所是否已经生成。",
        "",
        "| 状态 | 产物 | 路径 | 大小 |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        status = "就绪" if row["exists"] else "缺失"
        size = f'{row["size"]} 字节' if row["exists"] else "-"
        lines.append(f'| {status} | {row["label"]} | `{row["path"]}` | {size} |')
    lines.append("")
    if ready == total:
        lines.append("结论：本章关键数据分析产物已经生成，可以进入复盘、展示和报告整理。")
    else:
        lines.append("结论：仍有数据分析产物缺失，请先运行对应脚本。")
    return "\n".join(lines) + "\n"


def draw_image(path: Path, rows: list[dict[str, str | int | bool]]) -> None:
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
    ps_blue = "#082B57"
    green = "#24A06B"
    red = "#E84C61"
    blue = "#2F6BFF"
    orange = "#F28C28"
    purple = "#7A5AF8"

    def shadow_box(xy, fill="#FFFFFF", radius=26):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=line, width=2)

    ready = sum(1 for row in rows if row["exists"])
    total = len(rows)

    draw.text((92, 70), "第6章数据分析运行记录", font=title, fill=ink)
    draw.text(
        (96, 144),
        "CSV、图表、报告、JSON 与跨章交接结果集中检查。",
        font=subtitle,
        fill=muted,
    )
    draw.line((96, 206, 1704, 206), fill=line, width=3)

    shadow_box((95, 260, 825, 980), fill=ps_blue, radius=28)
    command_lines = [
        "PS C:\\PythonMarkdown\\python_tutorial_ch06>",
        "python code\\ch06\\04_make_dashboard_chart.py",
        "python code\\ch06\\05_anscombe_quartet.py",
        "python code\\ch06\\06_make_chart_makeover.py",
        "python code\\ch06\\07_make_outlier_diagnosis.py",
        "python code\\ch06\\09_make_memory_review_curve.py",
        "python code\\ch06\\10_make_chart_style_clinic.py",
        "python code\\ch06\\11_make_analysis_runtime_evidence.py",
        "",
        f"分析产物：{ready}/{total} 就绪",
        "状态：可以进入复盘" if ready == total else "状态：仍有文件缺失",
    ]
    y = 306
    for line_text in command_lines:
        color = "#BEE3F8"
        if line_text.startswith("分析产物"):
            color = "#A7F3D0" if ready == total else "#FDE68A"
        if line_text.startswith("状态"):
            color = "#A7F3D0" if ready == total else "#FCA5A5"
        draw.text((132, y), line_text, font=mono, fill=color)
        y += 47 if line_text else 24

    draw.rounded_rectangle((230, 805, 690, 920), radius=28, fill="#F8FAFC", outline="#CBD5E1", width=3)
    base_y = 875
    for i, (value, color) in enumerate([(76, blue), (122, green), (96, orange), (145, purple)]):
        x = 285 + i * 92
        draw.rounded_rectangle((x, base_y - value, x + 48, base_y), radius=12, fill=color)
    draw.line((265, base_y, 670, base_y), fill="#64748B", width=5)
    draw.ellipse((590, 782, 635, 827), outline=red, width=8)

    shadow_box((875, 260, 1705, 980), radius=28)
    draw.text((925, 308), "产物检查清单", font=h2, fill=ink)
    draw.text((928, 356), "图表要能复查，结论才站得住。", font=body, fill=muted)

    for i, row in enumerate(rows):
        col = i // 8
        slot = i % 8
        x = 925 + col * 385
        y = 425 + slot * 62
        exists = bool(row["exists"])
        status_color = green if exists else red
        draw.rounded_rectangle((x, y - 8, x + 98, y + 34), radius=21, fill=status_color)
        draw.text((x + 20, y), "就绪" if exists else "缺失", font=small, fill="white")
        file_name = Path(str(row["path"])).name
        if len(file_name) > 27:
            file_name = file_name[:24] + "..."
        label = str(row["label"])
        draw.text((x + 112, y - 2), label[:20], font=body, fill=ink)
        draw.text((x + 112, y + 27), file_name, font=small, fill=muted)

    draw.rounded_rectangle((95, 1015, 1705, 1082), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw.text(
        (140, 1033),
        "自查口径：好看的图必须能回到数据、代码和报告，才算真正可用。",
        font=body,
        fill="#8A5A00",
    )

    image.save(path, optimize=True, quality=95)


def main() -> None:
    root = project_root()
    reports = root / "reports"
    output = root / "output"
    web = root / "assets" / "ch06" / "web"
    reports.mkdir(exist_ok=True)
    output.mkdir(exist_ok=True)
    web.mkdir(parents=True, exist_ok=True)

    rows = collect_rows(root)
    report_file = reports / "ch06_analysis_runtime_evidence.md"
    image_file = output / "ch06_analysis_runtime_evidence.png"
    web_file = web / "ch06_analysis_runtime_evidence.png"

    report_file.write_text(build_report(rows), encoding="utf-8")
    draw_image(image_file, rows)
    shutil.copy2(image_file, web_file)

    ready = sum(1 for row in rows if row["exists"])
    print(f"第6章运行记录：{ready}/{len(rows)} 就绪")
    print(f"报告：{report_file.relative_to(root)}")
    print(f"图片：{image_file.relative_to(root)}")


if __name__ == "__main__":
    main()
