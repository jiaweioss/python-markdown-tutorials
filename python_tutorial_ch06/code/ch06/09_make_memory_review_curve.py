"""Create a memory-review curve for the learning-card factory.

Run after:
    python code/ch06/01_make_sample_csv.py
"""

from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


INPUT = Path("input/learning_records.csv")
OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_DIR = Path("assets/ch06/web")
JSON_PATH = OUTPUT / "ch06_memory_review_plan.json"
REPORT_PATH = REPORTS / "ch06_memory_review_plan.md"
PREVIEW_PATH = OUTPUT / "ch06_memory_review_plan.png"


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


def ensure_sample_csv() -> None:
    if INPUT.exists():
        return
    INPUT.parent.mkdir(exist_ok=True)
    INPUT.write_text(
        "\n".join(
            [
                "topic,minutes,done,rt_ms",
                "变量,18,yes,520",
                "列表,25,yes,480",
                "字典,22,no,610",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def load_rows() -> list[dict[str, str]]:
    ensure_sample_csv()
    with INPUT.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        raise ValueError("input/learning_records.csv is empty")
    return rows


def next_gap(row: dict[str, str]) -> int:
    done = row.get("done", "").strip().lower() == "yes"
    rt = int(row.get("rt_ms", row.get("reaction_time_ms", "650")))
    minutes = int(row.get("minutes", "25"))
    if not done:
        return 1
    if rt > 600 or minutes > 35:
        return 2
    return 4


def build_plan(rows: list[dict[str, str]]) -> dict:
    today = date.today()
    schedule = []
    for row in rows:
        gap = next_gap(row)
        schedule.append(
            {
                "topic": row["topic"],
                "minutes": int(row["minutes"]),
                "done": row["done"],
                "rt_ms": int(row.get("rt_ms", row.get("reaction_time_ms", "650"))),
                "review_after_days": gap,
                "review_date": (today + timedelta(days=gap)).isoformat(),
            }
        )
    curve = [
        {"day": day, "no_review": round(math.exp(-day / 7) * 100, 1)}
        for day in [0, 1, 2, 4, 7, 14, 30]
    ]
    return {
        "project": "learning-card memory review plan",
        "created": today.isoformat(),
        "curve": curve,
        "schedule": schedule,
    }


def write_outputs(plan: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    JSON_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第6章记忆复习计划",
        "",
        "艾宾浩斯遗忘曲线提醒我们：刚学会不等于已经稳固。学习卡片工厂不能只负责生成卡片，还要提醒你什么时候回来复习。",
        "",
        "## 下一轮复习",
        "",
    ]
    for item in plan["schedule"]:
        lines.append(
            f"- {item['topic']}：{item['review_after_days']} 天后复习，日期 {item['review_date']}，"
            f"本次记录 {item['minutes']} 分钟，反应时 {item['rt_ms']} ms。"
        )
    lines.extend(
        [
            "",
            "## 使用提示",
            "",
            "- 没完成的主题优先明天回看。",
            "- 反应时偏高的主题不要急着加难度，先做一次短复习。",
            "- 图表只负责提醒，真正的解释要回到当天的学习记录。",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_preview(plan: dict) -> None:
    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((80, 65, 1420, 835), radius=32, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((135, 115), "Memory Review Curve", fill="#162033", font=font(50, True))
    d.text((138, 178), "A Python-generated review plan for learning cards.", fill="#526071", font=font(24))

    left, top, right, bottom = 150, 280, 930, 700
    d.line((left, bottom, right, bottom), fill="#94A3B8", width=4)
    d.line((left, top, left, bottom), fill="#94A3B8", width=4)

    days = [point["day"] for point in plan["curve"]]
    values = [point["no_review"] for point in plan["curve"]]
    max_day = max(days)

    def xy(day: int, value: float) -> tuple[int, int]:
        x = left + int(day / max_day * (right - left))
        y = bottom - int(value / 100 * (bottom - top))
        return x, y

    for value in [25, 50, 75, 100]:
        y = bottom - int(value / 100 * (bottom - top))
        d.line((left, y, right, y), fill="#E5EAF2", width=2)
        d.text((100, y - 14), f"{value}%", fill="#64748B", font=font(18))

    points = [xy(day, value) for day, value in zip(days, values)]
    d.line(points, fill="#E84C61", width=7, joint="curve")
    for x, y in points:
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill="#E84C61")

    review_days = [1, 2, 4, 7, 14]
    ladder_points = []
    for day in review_days:
        retained = max(42, math.exp(-day / 11) * 100)
        ladder_points.append(xy(day, retained))
    d.line(ladder_points, fill="#2F6BFF", width=7, joint="curve")
    for x, y in ladder_points:
        d.ellipse((x - 11, y - 11, x + 11, y + 11), fill="#2F6BFF")
        d.line((x, y, x, y - 48), fill="#2F6BFF", width=3)

    for day in days:
        x, _ = xy(day, 0)
        d.line((x, bottom - 8, x, bottom + 8), fill="#94A3B8", width=3)
        d.text((x - 14, bottom + 24), str(day), fill="#64748B", font=font(18))
    d.text((left + 275, bottom + 66), "days after learning", fill="#64748B", font=font(20))

    legend_x = 1010
    d.rounded_rectangle((legend_x, 278, 1350, 510), radius=22, fill="#F8FAFC", outline="#E2E8F0", width=2)
    d.ellipse((legend_x + 32, 325, legend_x + 56, 349), fill="#E84C61")
    d.text((legend_x + 75, 319), "no review", fill="#243047", font=font(24, True))
    d.ellipse((legend_x + 32, 393, legend_x + 56, 417), fill="#2F6BFF")
    d.text((legend_x + 75, 387), "spaced review", fill="#243047", font=font(24, True))
    d.text((legend_x + 30, 455), "复习不是补救，是给记忆续航。", fill="#526071", font=font(22))

    d.rounded_rectangle((legend_x, 550, 1350, 720), radius=22, fill="#F0FDF4", outline="#BBF7D0", width=2)
    d.text((legend_x + 30, 578), "Next cards", fill="#166534", font=font(25, True))
    for i, item in enumerate(plan["schedule"][:3]):
        y = 622 + i * 31
        d.text(
            (legend_x + 30, y),
            f"{item['topic']}  +{item['review_after_days']}d",
            fill="#166534",
            font=font(21),
        )

    im.save(PREVIEW_PATH, optimize=True, quality=95)


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW_PATH, WEB_DIR / PREVIEW_PATH.name)


def main() -> None:
    rows = load_rows()
    plan = build_plan(rows)
    write_outputs(plan)
    make_preview(plan)
    copy_assets()
    print("created memory review plan:")
    print(f"- {JSON_PATH}")
    print(f"- {REPORT_PATH}")
    print(f"- {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
