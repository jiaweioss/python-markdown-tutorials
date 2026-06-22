"""Chapter 02 artifact: build a small Stroop dataset pack with Python types."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path
from statistics import mean
from textwrap import dedent


TRIALS = [
    {
        "trial_id": 1,
        "participant": "S001",
        "word": "RED",
        "ink_color": "blue",
        "response_key": "j",
        "correct_key": "j",
        "reaction_time_ms": 612.4,
        "note": None,
    },
    {
        "trial_id": 2,
        "participant": "S001",
        "word": "GREEN",
        "ink_color": "green",
        "response_key": "f",
        "correct_key": "f",
        "reaction_time_ms": 538.2,
        "note": "congruent",
    },
    {
        "trial_id": 3,
        "participant": "S001",
        "word": "BLUE",
        "ink_color": "red",
        "response_key": "f",
        "correct_key": "f",
        "reaction_time_ms": 701.8,
        "note": "incongruent",
    },
    {
        "trial_id": 4,
        "participant": "S001",
        "word": "RED",
        "ink_color": "red",
        "response_key": "f",
        "correct_key": "f",
        "reaction_time_ms": 487.6,
        "note": "fast",
    },
]


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch02").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def enrich_trials() -> list[dict]:
    enriched: list[dict] = []
    for trial in TRIALS:
        record = dict(trial)
        record["correct"] = record["response_key"] == record["correct_key"]
        record["congruent"] = record["word"].lower() == record["ink_color"]
        enriched.append(record)
    return enriched


def summarize(trials: list[dict]) -> dict:
    reaction_times = [trial["reaction_time_ms"] for trial in trials]
    accuracy = sum(1 for trial in trials if trial["correct"]) / len(trials)
    congruent_trials = [trial for trial in trials if trial["congruent"]]
    incongruent_trials = [trial for trial in trials if not trial["congruent"]]
    return {
        "participant": trials[0]["participant"],
        "trial_count": len(trials),
        "accuracy": accuracy,
        "mean_reaction_time_ms": mean(reaction_times),
        "fastest_reaction_time_ms": min(reaction_times),
        "slowest_reaction_time_ms": max(reaction_times),
        "congruent_count": len(congruent_trials),
        "incongruent_count": len(incongruent_trials),
    }


def write_csv(path: Path, trials: list[dict]) -> None:
    fields = [
        "trial_id",
        "participant",
        "word",
        "ink_color",
        "response_key",
        "correct_key",
        "correct",
        "congruent",
        "reaction_time_ms",
        "note",
    ]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(trials)


def build_report(trials: list[dict], summary: dict) -> str:
    rows = [
        "| trial | word | ink | response | correct | congruent | rt(ms) |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for trial in trials:
        rows.append(
            "| {trial_id} | {word} | {ink_color} | {response_key} | {correct} | {congruent} | {reaction_time_ms:.1f} |".format(
                **trial
            )
        )

    return dedent(
        f"""
        # 第2章 Stroop 数据类型包

        这份小数据包把 ch1 的极简 Stroop 任务继续往前推进：一次实验 trial 不是一行散乱文字，而是一条结构清楚的 `dict`；多次 trial 组成 `list`；整份数据可以保存成 JSON、CSV 和 Markdown 报告。

        ## 汇总

        - 被试编号：{summary["participant"]}
        - trial 数量：{summary["trial_count"]}
        - 正确率：{summary["accuracy"]:.0%}
        - 平均反应时：{summary["mean_reaction_time_ms"]:.1f} ms
        - 最快反应时：{summary["fastest_reaction_time_ms"]:.1f} ms
        - 最慢反应时：{summary["slowest_reaction_time_ms"]:.1f} ms
        - 一致 trial：{summary["congruent_count"]}
        - 冲突 trial：{summary["incongruent_count"]}

        ## trial 表

        {chr(10).join(rows)}

        ## 类型说明

        - `str`：保存被试编号、刺激词、墨水颜色和按键。
        - `int`：保存 trial 编号和数量。
        - `float`：保存反应时与平均值。
        - `bool`：保存是否正确、词义和颜色是否一致。
        - `None`：保存暂时没有备注的状态。
        - `dict`：保存一条 trial 的完整记录。
        - `list`：保存多条 trial，方便循环、统计和导出。
        """
    ).strip() + "\n"


def write_preview_png(path: Path, trials: list[dict], summary: dict) -> bool:
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

    width, height = 1600, 1000
    image = Image.new("RGB", (width, height), "#F6F8FB")
    draw = ImageDraw.Draw(image)

    title_font = load_font(50, True)
    h_font = load_font(30, True)
    body_font = load_font(23)
    small_font = load_font(19)
    mono_font = load_font(21)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    blue = "#2F6BFF"
    green = "#24A06B"
    orange = "#F28C28"
    purple = "#7A5AF8"
    red = "#E84C61"
    cyan = "#18A9B5"

    def rounded(xy, fill="#FFFFFF", outline=line, radius=22, width=2):
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

    def shadow(xy, radius=22):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        rounded(xy, radius=radius)

    def pill(x: int, y: int, text: str, color: str, w: int = 130):
        draw.rounded_rectangle((x, y, x + w, y + 42), radius=21, fill=color)
        draw.text((x + 20, y + 8), text, font=small_font, fill="white")

    draw.text((80, 58), "Stroop 数据类型包", font=title_font, fill=ink)
    draw.text((84, 125), "一组心理学 trial，正好演示 str、int、float、bool、None、dict 和 list 如何一起工作。", font=body_font, fill=muted)
    draw.line((80, 178, 1520, 178), fill=line, width=3)

    cards = [
        ("Trials", str(summary["trial_count"]), "list[dict]", blue),
        ("Accuracy", f"{summary['accuracy']:.0%}", "bool 统计", green),
        ("Mean RT", f"{summary['mean_reaction_time_ms']:.1f} ms", "float", orange),
        ("Conflict", str(summary["incongruent_count"]), "bool 分组", purple),
    ]
    for idx, (label, value, note, color) in enumerate(cards):
        x = 80 + idx * 380
        shadow((x, 230, x + 330, 390))
        pill(x + 28, 260, label, color, 126)
        draw.text((x + 30, 312), value, font=h_font, fill=ink)
        draw.text((x + 30, 352), note, font=small_font, fill=muted)

    shadow((80, 455, 1520, 720))
    draw.text((125, 500), "trial 记录表", font=h_font, fill=ink)
    headers = ["id", "word", "ink", "key", "ok", "same", "rt"]
    xs = [130, 260, 465, 650, 805, 955, 1135]
    for x, header in zip(xs, headers):
        draw.text((x, 555), header, font=mono_font, fill=blue)
    y = 600
    for trial in trials:
        values = [
            str(trial["trial_id"]),
            trial["word"],
            trial["ink_color"],
            trial["response_key"],
            str(trial["correct"]),
            str(trial["congruent"]),
            f"{trial['reaction_time_ms']:.1f}",
        ]
        for x, value in zip(xs, values):
            draw.text((x, y), value, font=small_font, fill=ink)
        y += 32

    shadow((80, 780, 1520, 915))
    draw.text((125, 825), "类型拆解", font=h_font, fill=ink)
    type_notes = [
        (blue, "str", "文字标签"),
        (orange, "int", "编号/数量"),
        (purple, "float", "反应时"),
        (green, "bool", "正确/一致"),
        (red, "None", "暂无备注"),
        (cyan, "dict/list", "记录与批量"),
    ]
    x = 300
    for color, type_name, note in type_notes:
        pill(x, 830, type_name, color, 130)
        draw.text((x - 4, 884), note, font=small_font, fill=muted)
        x += 190

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True, quality=95)
    return True


def main() -> None:
    root = project_root()
    output_dir = root / "output"
    reports_dir = root / "reports"
    web_dir = root / "assets" / "ch02" / "web"
    output_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    web_dir.mkdir(parents=True, exist_ok=True)

    trials = enrich_trials()
    summary = summarize(trials)

    json_file = output_dir / "ch02_stroop_dataset_pack.json"
    csv_file = output_dir / "ch02_stroop_dataset_pack.csv"
    png_file = output_dir / "ch02_stroop_dataset_pack.png"
    report_file = reports_dir / "ch02_stroop_dataset_pack.md"

    json_file.write_text(
        json.dumps({"summary": summary, "trials": trials}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(csv_file, trials)
    report_file.write_text(build_report(trials, summary), encoding="utf-8")
    has_preview = write_preview_png(png_file, trials, summary)
    if has_preview:
        shutil.copy2(png_file, web_dir / png_file.name)

    print("Stroop 数据类型包已生成：")
    print("-", json_file)
    print("-", csv_file)
    print("-", report_file)
    print("-", png_file if has_preview else "未生成 PNG：当前环境缺少 Pillow")


if __name__ == "__main__":
    main()
