"""Chapter 03 artifact: hand off the ch02 Stroop dataset through files."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path
from textwrap import dedent


ROOT = Path("workspace_ch03")
INBOX = ROOT / "inbox"
ORGANIZED = ROOT / "organized"
OUTPUT = ROOT / "output"
REPORT = OUTPUT / "ch03_ch02_stroop_file_handoff.md"
PREVIEW = OUTPUT / "ch03_ch02_stroop_file_handoff.png"
PREVIEW_ASSET = Path("assets/ch03/web/ch03_ch02_stroop_file_handoff.png")


FALLBACK_DATA = {
    "summary": {
        "participant": "S001",
        "trial_count": 4,
        "accuracy": 1.0,
        "mean_reaction_time_ms": 585.0,
        "fastest_reaction_time_ms": 487.6,
        "slowest_reaction_time_ms": 701.8,
        "congruent_count": 2,
        "incongruent_count": 2,
    },
    "trials": [
        {"trial_id": 1, "word": "RED", "ink_color": "blue", "correct": True, "congruent": False, "reaction_time_ms": 612.4},
        {"trial_id": 2, "word": "GREEN", "ink_color": "green", "correct": True, "congruent": True, "reaction_time_ms": 538.2},
        {"trial_id": 3, "word": "BLUE", "ink_color": "red", "correct": True, "congruent": False, "reaction_time_ms": 701.8},
        {"trial_id": 4, "word": "RED", "ink_color": "red", "correct": True, "congruent": True, "reaction_time_ms": 487.6},
    ],
}


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch03").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def ch02_root(ch03_root: Path) -> Path:
    return ch03_root.parent / "python_tutorial_ch02"


def ensure_ch02_outputs(ch03_root: Path) -> tuple[Path, Path, dict]:
    source_root = ch02_root(ch03_root)
    json_file = source_root / "output" / "ch02_stroop_dataset_pack.json"
    csv_file = source_root / "output" / "ch02_stroop_dataset_pack.csv"
    if json_file.exists() and csv_file.exists():
        return json_file, csv_file, json.loads(json_file.read_text(encoding="utf-8"))

    generated = source_root / "code" / "ch02" / "10_make_stroop_dataset_pack.py"
    if generated.exists():
        import runpy
        import os

        old_cwd = Path.cwd()
        try:
            os.chdir(source_root)
            runpy.run_path(str(generated), run_name="__main__")
        finally:
            os.chdir(old_cwd)

    if json_file.exists() and csv_file.exists():
        return json_file, csv_file, json.loads(json_file.read_text(encoding="utf-8"))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    fallback_json = OUTPUT / "fallback_ch02_stroop_dataset_pack.json"
    fallback_csv = OUTPUT / "fallback_ch02_stroop_dataset_pack.csv"
    fallback_json.write_text(json.dumps(FALLBACK_DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(fallback_csv, FALLBACK_DATA["trials"])
    return fallback_json, fallback_csv, FALLBACK_DATA


def write_csv(path: Path, trials: list[dict]) -> None:
    fields = sorted({key for trial in trials for key in trial})
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(trials)


def sha256_prefix(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:12]


def copy_into_workspace(json_file: Path, csv_file: Path) -> dict:
    INBOX.mkdir(parents=True, exist_ok=True)
    (ORGANIZED / "json").mkdir(parents=True, exist_ok=True)
    (ORGANIZED / "csv").mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    inbox_json = INBOX / json_file.name
    inbox_csv = INBOX / csv_file.name
    organized_json = ORGANIZED / "json" / json_file.name
    organized_csv = ORGANIZED / "csv" / csv_file.name
    for source, target in [
        (json_file, inbox_json),
        (csv_file, inbox_csv),
        (json_file, organized_json),
        (csv_file, organized_csv),
    ]:
        shutil.copy2(source, target)

    return {
        "inbox_json": inbox_json,
        "inbox_csv": inbox_csv,
        "organized_json": organized_json,
        "organized_csv": organized_csv,
    }


def build_report(data: dict, copied: dict, source_json: Path, source_csv: Path) -> str:
    summary = data["summary"]
    rows = [
        "| 文件 | 位置 | 大小 | SHA256 前 12 位 |",
        "| --- | --- | --- | --- |",
    ]
    for label, path in copied.items():
        rows.append(
            f"| `{label}` | `{path.as_posix()}` | {path.stat().st_size} bytes | `{sha256_prefix(path)}` |"
        )

    return dedent(
        f"""
        # 第3章 ch2 Stroop 文件交接记录

        这份记录证明：第2章生成的数据包没有停留在内存里，而是被第3章读取、复制、归档并留下路径记录。

        ## 来源

        - JSON 来源：`{source_json.as_posix()}`
        - CSV 来源：`{source_csv.as_posix()}`

        ## 数据摘要

        - 被试编号：{summary["participant"]}
        - trial 数量：{summary["trial_count"]}
        - 正确率：{summary["accuracy"]:.0%}
        - 平均反应时：{summary["mean_reaction_time_ms"]:.1f} ms
        - 一致 / 冲突 trial：{summary["congruent_count"]} / {summary["incongruent_count"]}

        ## 文件清单

        {chr(10).join(rows)}

        ## 本章要点

        - `Path` 负责描述文件位置。
        - `read_text()` 读取 JSON 文本。
        - `shutil.copy2()` 复制数据文件并保留基础元数据。
        - `sha256` 摘要用于抽查文件是否被意外改动。
        - 输出报告放在 `workspace_ch03/output/`，不覆盖原始数据。
        """
    ).strip() + "\n"


def write_preview_png(path: Path, data: dict, copied: dict) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def load_font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()

    width, height = 1600, 960
    image = Image.new("RGB", (width, height), "#F6F8FB")
    draw = ImageDraw.Draw(image)
    title_font = load_font(48, True)
    h_font = load_font(30, True)
    body_font = load_font(23)
    small_font = load_font(18)
    mono_font = load_font(20)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    blue = "#2F6BFF"
    green = "#24A06B"
    orange = "#F28C28"
    purple = "#7A5AF8"
    red = "#E84C61"

    def rounded(xy, fill="#FFFFFF", outline=line, radius=22, width=2):
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

    def shadow(xy, radius=22):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        rounded(xy, radius=radius)

    def pill(x: int, y: int, text: str, color: str, w: int = 130):
        draw.rounded_rectangle((x, y, x + w, y + 42), radius=21, fill=color)
        draw.text((x + 20, y + 8), text, font=small_font, fill="white")

    summary = data["summary"]
    draw.text((80, 58), "ch2 -> ch3 文件交接记录", font=title_font, fill=ink)
    draw.text((84, 123), "数据离开上一章，进入安全工作区；路径、大小和哈希都留下记录。", font=body_font, fill=muted)
    draw.line((80, 178, 1520, 178), fill=line, width=3)

    cards = [
        ("source", "ch02/output", "读取上一章", blue),
        ("inbox", "workspace/inbox", "接收副本", green),
        ("organized", "json + csv", "分类归档", orange),
        ("receipt", "output/report", "留下记录", purple),
    ]
    for idx, (label, value, note, color) in enumerate(cards):
        x = 80 + idx * 380
        shadow((x, 230, x + 330, 385))
        pill(x + 26, 260, label, color, 130)
        draw.text((x + 28, 313), value, font=h_font, fill=ink)
        draw.text((x + 28, 352), note, font=small_font, fill=muted)

    shadow((80, 455, 760, 770))
    draw.text((125, 500), "数据摘要", font=h_font, fill=ink)
    facts = [
        ("participant", summary["participant"]),
        ("trials", str(summary["trial_count"])),
        ("accuracy", f"{summary['accuracy']:.0%}"),
        ("mean_rt", f"{summary['mean_reaction_time_ms']:.1f} ms"),
        ("conflict", str(summary["incongruent_count"])),
    ]
    y = 560
    for key, value in facts:
        draw.text((130, y), key, font=mono_font, fill=blue)
        draw.text((360, y), value, font=body_font, fill=ink)
        y += 40

    shadow((840, 455, 1520, 770))
    draw.text((885, 500), "文件记录", font=h_font, fill=ink)
    y = 560
    for label in ["organized_json", "organized_csv"]:
        path_item = copied[label]
        pill(890, y - 5, path_item.suffix.upper().strip("."), green if path_item.suffix == ".json" else orange, 95)
        draw.text((1010, y), path_item.name, font=small_font, fill=ink)
        draw.text((1010, y + 30), f"{path_item.stat().st_size} bytes  sha {sha256_prefix(path_item)}", font=small_font, fill=muted)
        y += 82

    rounded((260, 830, 1340, 900), fill="#FFF7E8", outline="#F2B84B", radius=24, width=3)
    draw.text((315, 851), "文件操作口诀：先复制到安全工作区，再整理，再生成可复查的清单。", font=body_font, fill="#8A5A00")

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True, quality=95)
    return True


def main() -> None:
    root = project_root()
    global ROOT, INBOX, ORGANIZED, OUTPUT, REPORT, PREVIEW, PREVIEW_ASSET
    ROOT = root / "workspace_ch03"
    INBOX = ROOT / "inbox"
    ORGANIZED = ROOT / "organized"
    OUTPUT = ROOT / "output"
    REPORT = OUTPUT / "ch03_ch02_stroop_file_handoff.md"
    PREVIEW = OUTPUT / "ch03_ch02_stroop_file_handoff.png"
    PREVIEW_ASSET = root / "assets" / "ch03" / "web" / "ch03_ch02_stroop_file_handoff.png"

    source_json, source_csv, data = ensure_ch02_outputs(root)
    copied = copy_into_workspace(source_json, source_csv)
    REPORT.write_text(build_report(data, copied, source_json, source_csv), encoding="utf-8")
    has_preview = write_preview_png(PREVIEW, data, copied)
    if has_preview:
        PREVIEW_ASSET.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PREVIEW, PREVIEW_ASSET)

    print("ch2 Stroop 文件交接记录已生成：")
    print("-", REPORT)
    print("-", PREVIEW if has_preview else "未生成 PNG：当前环境缺少 Pillow")
    print("-", copied["organized_json"])
    print("-", copied["organized_csv"])


if __name__ == "__main__":
    main()
