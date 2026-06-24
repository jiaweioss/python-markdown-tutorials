"""Chapter 03 artifact: build an archive evidence board from generated files."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from textwrap import dedent


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch03").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def collect_summary(root: Path) -> dict:
    workspace = root / "workspace_ch03"
    output = workspace / "output"
    organized = workspace / "organized"
    inbox = workspace / "inbox"
    required = {
        "manifest": output / "ch03_archive_manifest.md",
        "receipt": output / "ch03_archive_receipt.md",
        "safety": output / "ch03_path_safety_receipt.md",
        "handoff": output / "ch03_ch02_stroop_file_handoff.md",
    }
    return {
        "workspace": str(workspace),
        "inbox_files": count_files(inbox),
        "organized_files": count_files(organized),
        "output_files": count_files(output),
        "required": {name: path.exists() for name, path in required.items()},
        "required_paths": {name: str(path) for name, path in required.items()},
    }


def build_report(summary: dict) -> str:
    required_rows = [
        f"| {name} | {'ready' if exists else 'missing'} | `{summary['required_paths'][name]}` |"
        for name, exists in summary["required"].items()
    ]
    return dedent(
        f"""
        # 第3章归档记录板

        这份记录把第3章的文件操作成果集中到一页：输入区、整理区、输出区，以及四份关键记录文件。

        ## 文件计数

        - inbox 文件数：{summary["inbox_files"]}
        - organized 文件数：{summary["organized_files"]}
        - output 文件数：{summary["output_files"]}

        ## 关键记录

        | 记录 | 状态 | 路径 |
        | --- | --- | --- |
        {chr(10).join(required_rows)}

        文件读写不是“代码跑了一下”就结束。真正可靠的文件项目，应该能说清楚：材料从哪里来、被整理到哪里、输出了什么、路径是否安全、跨章节数据是否交接成功。
        """
    ).strip() + "\n"


def draw_png(path: Path, summary: dict) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def load_font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
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

    title = load_font(58, True)
    subtitle = load_font(26)
    h2 = load_font(32, True)
    body = load_font(24)
    small = load_font(19)
    mono = load_font(22)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    blue = "#2F6BFF"
    green = "#24A06B"
    orange = "#F28C28"
    purple = "#7A5AF8"
    red = "#E84C61"
    cyan = "#18A9B5"

    def shadow_box(xy, radius: int = 24):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        draw.rounded_rectangle(xy, radius=radius, fill="#FFFFFF", outline=line, width=2)

    def pill(x: int, y: int, text: str, color: str, w: int = 128):
        draw.rounded_rectangle((x, y, x + w, y + 42), radius=21, fill=color)
        draw.text((x + 18, y + 8), text, font=small, fill="white")

    draw.text((94, 72), "资料归档记录板", font=title, fill=ink)
    draw.text((98, 146), "输入区、归档区、输出区、安全检查和跨章交接集中复查。", font=subtitle, fill=muted)
    draw.line((96, 206, 1704, 206), fill=line, width=3)

    count_cards = [
        ("待整理区", summary["inbox_files"], blue),
        ("归档区", summary["organized_files"], green),
        ("输出区", summary["output_files"], orange),
    ]
    for idx, (label, value, color) in enumerate(count_cards):
        x = 110 + idx * 540
        shadow_box((x, 270, x + 440, 445))
        pill(x + 30, 304, label, color, 140)
        draw.text((x + 250, 324), str(value), font=title, fill=ink)
        draw.text((x + 30, 378), "个文件", font=body, fill=muted)

    evidence = [
        ("manifest", "归档清单", blue),
        ("receipt", "归档记录", green),
        ("safety", "路径检查", red),
        ("handoff", "第2章数据", purple),
    ]
    tag_labels = {
        "manifest": "清单",
        "receipt": "记录",
        "safety": "安全",
        "handoff": "衔接",
    }
    for idx, (name, label, color) in enumerate(evidence):
        x = 140 + (idx % 2) * 780
        y = 545 + (idx // 2) * 200
        shadow_box((x, y, x + 650, y + 140))
        pill(x + 30, y + 32, tag_labels[name], color, 150)
        draw.text((x + 210, y + 30), label, font=h2, fill=ink)
        status = "就绪" if summary["required"][name] else "缺失"
        status_color = green if status == "就绪" else red
        draw.text((x + 210, y + 82), status, font=mono, fill=status_color)

    shadow_box((425, 950, 1375, 1040))
    draw.text((470, 980), "文件不是装饰，记录才方便复查。", font=body, fill="#8A5A00")

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True, quality=95)
    return True


def main() -> None:
    root = project_root()
    output_dir = root / "workspace_ch03" / "output"
    reports_dir = root / "reports"
    web_dir = root / "assets" / "ch03" / "web"
    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    web_dir.mkdir(parents=True, exist_ok=True)

    summary = collect_summary(root)
    json_file = output_dir / "ch03_archive_evidence_board.json"
    image_file = output_dir / "ch03_archive_evidence_board.png"
    report_file = reports_dir / "ch03_archive_evidence_board.md"

    json_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_file.write_text(build_report(summary), encoding="utf-8")
    has_image = draw_png(image_file, summary)
    if has_image:
        shutil.copy2(image_file, web_dir / image_file.name)

    print("资料归档记录板已生成：")
    print("-", json_file)
    print("-", report_file)
    print("-", image_file if has_image else "PNG skipped because Pillow is unavailable")


if __name__ == "__main__":
    main()
