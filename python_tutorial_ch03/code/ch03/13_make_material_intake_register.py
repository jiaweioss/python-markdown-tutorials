"""Chapter 03 artifact: build a material intake register for the archive workflow."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch03").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def suffix_counts(path: Path) -> dict[str, int]:
    if not path.exists():
        return {}
    counter: Counter[str] = Counter()
    for item in path.rglob("*"):
        if item.is_file():
            counter[item.suffix.lower() or "[none]"] += 1
    return dict(sorted(counter.items()))


def collect_summary(root: Path) -> dict:
    workspace = root / "workspace_ch03"
    inbox = workspace / "inbox"
    organized = workspace / "organized"
    output = workspace / "output"
    reports = root / "reports"
    required = {
        "inventory": output / "file_inventory.md",
        "manifest": output / "ch03_archive_manifest.md",
        "receipt": output / "ch03_archive_receipt.md",
        "safety": output / "ch03_path_safety_receipt.md",
        "handoff": output / "ch03_ch02_stroop_file_handoff.md",
        "evidence": output / "ch03_archive_evidence_board.png",
    }
    zones = {
        "inbox": inbox,
        "organized": organized,
        "output": output,
        "reports": reports,
    }
    return {
        "workspace": str(workspace),
        "zones": {
            name: {
                "path": str(path),
                "files": count_files(path),
                "suffixes": suffix_counts(path),
            }
            for name, path in zones.items()
        },
        "required": {name: path.exists() for name, path in required.items()},
        "required_paths": {name: str(path) for name, path in required.items()},
    }


def build_report(summary: dict) -> str:
    zone_rows = []
    for name, data in summary["zones"].items():
        suffix_text = ", ".join(f"{key}:{value}" for key, value in data["suffixes"].items()) or "-"
        zone_rows.append(f"| {name} | {data['files']} | `{data['path']}` | {suffix_text} |")
    evidence_rows = []
    for name, exists in summary["required"].items():
        status = "ready" if exists else "missing"
        evidence_rows.append(f"| {name} | {status} | `{summary['required_paths'][name]}` |")
    lines = [
        "# 第3章资料入库登记册",
        "",
        "这份登记册由 `13_make_material_intake_register.py` 生成，用来记录第3章资料归档工作流中的入口区、整理区、输出区和报告区。",
        "",
        "## 区域统计",
        "",
        "| 区域 | 文件数 | 路径 | 后缀分布 |",
        "| --- | ---: | --- | --- |",
        *zone_rows,
        "",
        "## 关键登记文件",
        "",
        "| 证据 | 状态 | 路径 |",
        "| --- | --- | --- |",
        *evidence_rows,
        "",
        "文件读写不是把资料从一个文件夹搬到另一个文件夹就结束。真正可靠的资料管理，要能说清楚：材料从哪里进入、被分到哪里、哪些报告证明它已经登记、归档、交接和复核。",
    ]
    return "\n".join(lines) + "\n"


def draw_register(path: Path, summary: dict) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def load_font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
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

    title = load_font(56, True)
    subtitle = load_font(26)
    h2 = load_font(28, True)
    body = load_font(22)
    mono = load_font(20)
    small = load_font(17)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    blue = "#2F6BFF"
    green = "#24A06B"
    orange = "#F28C28"
    purple = "#7A5AF8"
    red = "#E84C61"
    cyan = "#18A9B5"

    def shadow_box(xy, fill="#FFFFFF", radius=26):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=line, width=2)

    def tag(x: int, y: int, text: str, color: str, w: int = 126):
        draw.rounded_rectangle((x, y, x + w, y + 40), radius=20, fill=color)
        draw.text((x + 18, y + 7), text, font=small, fill="#FFFFFF")

    draw.text((92, 70), "Material Intake Register", font=title, fill=ink)
    draw.text((96, 144), "A file workflow starts at the gate and ends with evidence.", font=subtitle, fill=muted)
    draw.line((96, 206, 1704, 206), fill=line, width=3)

    zone_colors = {
        "inbox": blue,
        "organized": green,
        "output": orange,
        "reports": purple,
    }
    zone_positions = {
        "inbox": (110, 285),
        "organized": (505, 285),
        "output": (900, 285),
        "reports": (1295, 285),
    }
    for name, (x, y) in zone_positions.items():
        data = summary["zones"][name]
        color = zone_colors[name]
        shadow_box((x, y, x + 330, y + 230))
        tag(x + 26, y + 28, name, color, 132)
        draw.text((x + 235, y + 35), str(data["files"]), font=title, fill=ink)
        draw.text((x + 30, y + 92), "files", font=body, fill=muted)
        suffix_items = list(data["suffixes"].items())[:4]
        sy = y + 136
        for suffix, count in suffix_items:
            draw.ellipse((x + 32, sy + 5, x + 48, sy + 21), fill=color)
            draw.text((x + 62, sy), f"{suffix}  {count}", font=small, fill=ink)
            sy += 28

    for start, end in [("inbox", "organized"), ("organized", "output"), ("output", "reports")]:
        x1, y1 = zone_positions[start]
        x2, y2 = zone_positions[end]
        draw.line((x1 + 340, y1 + 115, x2 - 12, y2 + 115), fill="#C9D4E5", width=5)
        draw.polygon([(x2 - 12, y2 + 115), (x2 - 34, y2 + 101), (x2 - 34, y2 + 129)], fill="#C9D4E5")

    shadow_box((140, 610, 1660, 930))
    draw.text((190, 660), "Evidence ledger", font=h2, fill=ink)
    evidence = list(summary["required"].items())
    for idx, (name, exists) in enumerate(evidence):
        col = idx % 3
        row = idx // 3
        x = 190 + col * 480
        y = 720 + row * 82
        color = green if exists else red
        draw.rounded_rectangle((x, y, x + 112, y + 40), radius=20, fill=color)
        draw.text((x + 18, y + 7), "ready" if exists else "miss", font=small, fill="#FFFFFF")
        draw.text((x + 132, y + 5), name, font=body, fill=ink)
        file_name = Path(summary["required_paths"][name]).name
        if len(file_name) > 28:
            file_name = file_name[:25] + "..."
        draw.text((x + 132, y + 36), file_name, font=small, fill=muted)

    draw.rounded_rectangle((280, 990, 1520, 1050), radius=22, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw.text((560, 1008), "Generated by code/ch03/13_make_material_intake_register.py", font=mono, fill="#8A5A00")

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
    json_file = output_dir / "ch03_material_intake_register.json"
    image_file = output_dir / "ch03_material_intake_register.png"
    report_file = reports_dir / "ch03_material_intake_register.md"

    json_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_file.write_text(build_report(summary), encoding="utf-8")
    has_image = draw_register(image_file, summary)
    if has_image:
        shutil.copy2(image_file, web_dir / image_file.name)

    print("Material intake register generated:")
    print("-", json_file)
    print("-", report_file)
    print("-", image_file if has_image else "PNG skipped because Pillow is unavailable")


if __name__ == "__main__":
    main()
