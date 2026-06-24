"""Generate a runtime record for the PyGame chapter."""

from __future__ import annotations

import datetime as _dt
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CHECKS = [
    ("反应报告", "reports/ch07_reaction_report.md"),
    ("反应预览", "reports/ch07_reaction_report_preview.png"),
    ("平衡报告", "reports/ch07_game_balance_report.md"),
    ("平衡预览", "output/ch07_game_balance_preview.png"),
    ("反馈报告", "reports/ch07_game_feedback_loop.md"),
    ("反馈预览", "output/ch07_game_feedback_loop.png"),
    ("心流报告", "reports/ch07_flow_tuning_curve.md"),
    ("心流曲线", "output/ch07_flow_tuning_curve.png"),
    ("调参报告", "reports/ch07_data_driven_tuning.md"),
    ("调参 JSON", "output/ch07_data_driven_tuning.json"),
    ("调参图", "output/ch07_data_driven_tuning.png"),
    ("教学游戏报告", "reports/ch07_teaching_feedback_game.md"),
    ("教学游戏 JSON", "output/ch07_teaching_feedback_game.json"),
    ("教学游戏图", "output/ch07_teaching_feedback_game.png"),
]


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch07").exists():
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
        "# 第7章游戏运行记录",
        "",
        f"- 检查时间：{_dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 运行产物：{ready}/{total} ready",
        "- 说明：这份报告检查关键词反应小游戏、难度平衡、反馈循环、心流调参、数据驱动调参和教学反馈小游戏计划是否已经生成。",
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
        lines.append("结论：本章关键游戏产物已经生成，可以进入复盘和二次改造。")
    else:
        lines.append("结论：仍有游戏产物缺失，请先运行对应脚本。")
    return "\n".join(lines) + "\n"


def draw_image(path: Path, rows: list[dict[str, str | int | bool]]) -> None:
    width, height = 1800, 1120
    im = Image.new("RGB", (width, height), "#F6F8FB")
    d = ImageDraw.Draw(im)

    title = font(54, True)
    subtitle = font(27)
    h2 = font(30, True)
    body = font(24)
    mono = font(22)
    small = font(18)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    dark = "#101827"
    green = "#24A06B"
    red = "#E84C61"
    blue = "#2F6BFF"
    orange = "#F28C28"
    purple = "#7A5AF8"

    def shadow_box(xy, fill="#FFFFFF", radius=26):
        x1, y1, x2, y2 = xy
        d.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        d.rounded_rectangle(xy, radius=radius, fill=fill, outline=line, width=2)

    ready = sum(1 for row in rows if row["exists"])
    total = len(rows)

    d.text((92, 70), "PyGame 章节运行记录", font=title, fill=ink)
    d.text(
        (96, 144),
        "小游戏不只要窗口能打开，还要让报告、调参和反馈计划都能复查。",
        font=subtitle,
        fill=muted,
    )
    d.line((96, 206, 1704, 206), fill=line, width=3)

    shadow_box((95, 260, 825, 980), fill=dark, radius=28)
    command_lines = [
        "PS C:\\PythonMarkdown\\python_tutorial_ch07>",
        "python code\\ch07\\04_make_reaction_report.py",
        "python code\\ch07\\05_make_game_balance_report.py",
        "python code\\ch07\\06_make_game_feedback_loop.py",
        "python code\\ch07\\07_make_flow_tuning_curve.py",
        "python code\\ch07\\08_make_data_driven_tuning.py",
        "python code\\ch07\\09_make_teaching_feedback_game.py",
        "python code\\ch07\\10_make_game_runtime_evidence.py",
        "",
        f"游戏产物：{ready}/{total} 就绪",
        "状态：可以试玩，也可以复查文件",
    ]
    y = 306
    for line_text in command_lines:
        color = "#BEE3F8"
        if line_text.startswith("游戏产物"):
            color = "#A7F3D0" if ready == total else "#FDE68A"
        if line_text.startswith("状态"):
            color = "#A7F3D0" if ready == total else "#FCA5A5"
        d.text((132, y), line_text, font=mono, fill=color)
        y += 48 if line_text else 24

    # A tiny no-text game scene keeps the image playful without becoming a dense explanation card.
    d.rounded_rectangle((240, 835, 680, 955), radius=28, fill="#F8FAFC", outline="#CBD5E1", width=3)
    d.ellipse((290, 872, 350, 932), fill=blue)
    d.rounded_rectangle((395, 862, 500, 942), radius=20, fill=orange)
    d.polygon([(590, 862), (660, 902), (590, 942)], fill=purple)

    shadow_box((875, 260, 1705, 980), radius=28)
    d.text((925, 308), "产物检查清单", font=h2, fill=ink)
    d.text((928, 356), "每个结果都能重新打开，游戏循环才真正适合学习。", font=body, fill=muted)

    for i, row in enumerate(rows):
        col = i // 7
        slot = i % 7
        x = 925 + col * 385
        y = 425 + slot * 72
        exists = bool(row["exists"])
        color = green if exists else red
        d.rounded_rectangle((x, y - 8, x + 98, y + 34), radius=21, fill=color)
        d.text((x + 18, y), "就绪" if exists else "缺失", font=small, fill="white")
        file_name = Path(str(row["path"])).name
        if len(file_name) > 28:
            file_name = file_name[:25] + "..."
        d.text((x + 112, y - 2), str(row["label"])[:20], font=body, fill=ink)
        d.text((x + 112, y + 28), file_name, font=small, fill=muted)

    d.rounded_rectangle((95, 1015, 1705, 1082), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    d.text(
        (140, 1033),
        "经验提醒：小游戏好不好，不只看能不能玩，也要看反馈、调参和报告能否复查。",
        font=body,
        fill="#8A5A00",
    )

    im.save(path, optimize=True, quality=95)


def main() -> None:
    root = project_root()
    reports = root / "reports"
    output = root / "output"
    web = root / "assets" / "ch07" / "web"
    reports.mkdir(exist_ok=True)
    output.mkdir(exist_ok=True)
    web.mkdir(parents=True, exist_ok=True)

    rows = collect_rows(root)
    report_file = reports / "ch07_game_runtime_evidence.md"
    image_file = output / "ch07_game_runtime_evidence.png"
    web_file = web / "ch07_game_runtime_evidence.png"

    report_file.write_text(build_report(rows), encoding="utf-8")
    draw_image(image_file, rows)
    shutil.copy2(image_file, web_file)

    ready = sum(1 for row in rows if row["exists"])
    print(f"第7章游戏运行记录：{ready}/{len(rows)} 就绪")
    print(f"report: {report_file}")
    print(f"image: {image_file}")


if __name__ == "__main__":
    main()
