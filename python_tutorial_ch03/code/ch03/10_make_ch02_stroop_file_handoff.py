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
        # 第3章 ch2 Stroop 文件交接回执

        这份回执证明：第2章生成的数据包没有停留在内存里，而是被第3章读取、复制、归档并留下路径证据。

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

def main() -> None:
    root = project_root()
    global ROOT, INBOX, ORGANIZED, OUTPUT, REPORT, PREVIEW, PREVIEW_ASSET
    ROOT = root / "workspace_ch03"
    INBOX = ROOT / "inbox"
    ORGANIZED = ROOT / "organized"
    OUTPUT = ROOT / "output"
    REPORT = OUTPUT / "ch03_ch02_stroop_file_handoff.md"

    source_json, source_csv, data = ensure_ch02_outputs(root)
    copied = copy_into_workspace(source_json, source_csv)
    REPORT.write_text(build_report(data, copied, source_json, source_csv), encoding="utf-8")

    print("ch2 Stroop 文件交接回执已生成：")
    print("-", REPORT)
    print("-", copied["organized_json"])
    print("-", copied["organized_csv"])

if __name__ == "__main__":
    main()
