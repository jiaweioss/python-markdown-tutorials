"""Build a teaching-feedback game plan from the memory review cards.

Run after:
    python ../python_tutorial_ch06/code/ch06/09_make_memory_review_curve.py
or simply run this script; it will use a small fallback queue if ch6 output is absent.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch07").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
BOOK_ROOT = ROOT.parent
CH06_MEMORY_PLAN = BOOK_ROOT / "python_tutorial_ch06" / "output" / "ch06_memory_review_plan.json"
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch07" / "web"
PLAN_JSON = OUTPUT / "ch07_teaching_feedback_game.json"
REPORT = REPORTS / "ch07_teaching_feedback_game.md"
PREVIEW = OUTPUT / "ch07_teaching_feedback_game.png"


FALLBACK_QUEUE = [
    {"topic": "变量", "review_after_days": 1, "rt_ms": 520, "done": "yes"},
    {"topic": "列表", "review_after_days": 2, "rt_ms": 610, "done": "yes"},
    {"topic": "字典", "review_after_days": 1, "rt_ms": 720, "done": "no"},
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


def load_memory_queue() -> list[dict]:
    if CH06_MEMORY_PLAN.exists():
        data = json.loads(CH06_MEMORY_PLAN.read_text(encoding="utf-8"))
        return data.get("schedule", FALLBACK_QUEUE)
    return FALLBACK_QUEUE


def difficulty_for(card: dict) -> str:
    if card.get("done") == "no":
        return "support"
    if int(card.get("rt_ms", 650)) > 600:
        return "practice"
    return "flow"


def build_game_plan(queue: list[dict]) -> dict:
    cards = []
    for index, card in enumerate(queue[:6], start=1):
        band = difficulty_for(card)
        cards.append(
            {
                "round": index,
                "topic": card["topic"],
                "key": str(index),
                "difficulty": band,
                "feedback": {
                    "flow": "Correct. Add one tiny challenge.",
                    "practice": "Good effort. Repeat once with a hint.",
                    "support": "Slow down. Show the clue first.",
                }[band],
                "review_after_days": int(card.get("review_after_days", 1)),
                "rt_ms": int(card.get("rt_ms", 650)),
            }
        )
    return {
        "project": "teaching-feedback card game",
        "source": str(CH06_MEMORY_PLAN) if CH06_MEMORY_PLAN.exists() else "fallback",
        "round_count": len(cards),
        "core_loop": ["show card", "press key", "instant feedback", "write result"],
        "cards": cards,
    }


def write_outputs(plan: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    PLAN_JSON.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第7章教学反馈小游戏计划",
        "",
        "Skinner teaching machine 的启发很朴素：学习者做出反应以后，要立刻得到反馈。PyGame 让这个机制变得可编程：显示卡片、读取按键、更新状态、记录结果。",
        "",
        "| 轮次 | 卡片 | 按键 | 难度带 | 反馈 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for card in plan["cards"]:
        lines.append(
            f"| {card['round']} | {card['topic']} | {card['key']} | "
            f"{card['difficulty']} | {card['feedback']} |"
        )
    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "- 把 `cards` 写入 PyGame 主循环，逐张显示。",
            "- 每次按键后立即显示对错、提示或鼓励。",
            "- 把反应时和结果继续保存，交给 ch6 或 ch10 做报告。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_card(d: ImageDraw.ImageDraw, xy, title: str, body: str, color: str) -> None:
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=22, fill="#FFFFFF", outline="#D8E0EC", width=2)
    d.rounded_rectangle((x1, y1, x2, y1 + 12), radius=6, fill=color)
    d.text((x1 + 24, y1 + 24), title, fill="#162033", font=font(24, True))
    d.text((x1 + 24, y1 + 56), body, fill="#526071", font=font(20))


def draw_preview(plan: dict) -> None:
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((80, 65, 1420, 850), radius=32, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((135, 120), "Teaching Feedback Game", fill="#162033", font=font(49, True))
    d.text((138, 184), "Memory cards become a tiny PyGame practice loop.", fill="#526071", font=font(25))

    queue_x = 140
    d.text((queue_x, 265), "Review Queue", fill="#243047", font=font(29, True))
    colors = {"flow": "#2F6BFF", "practice": "#F28C28", "support": "#E84C61"}
    for i, card in enumerate(plan["cards"][:4]):
        y = 318 + i * 96
        draw_card(
            d,
            (queue_x, y, queue_x + 360, y + 82),
            f"{card['key']}. {card['topic']}",
            f"{card['difficulty']} · {card['rt_ms']} ms",
            colors[card["difficulty"]],
        )

    mid_x = 585
    d.rounded_rectangle((mid_x, 320, mid_x + 340, 610), radius=28, fill="#101827", outline="#101827")
    d.text((mid_x + 45, 365), "Prompt", fill="#93C5FD", font=font(24, True))
    prompt = plan["cards"][0]["topic"] if plan["cards"] else "Card"
    d.text((mid_x + 45, 425), prompt, fill="#FFFFFF", font=font(58, True))
    d.rounded_rectangle((mid_x + 45, 520, mid_x + 220, 575), radius=20, fill="#2F6BFF")
    d.text((mid_x + 83, 535), "press 1", fill="#FFFFFF", font=font(24, True))

    d.line((515, 455, 565, 455), fill="#98A5B8", width=6)
    d.polygon([(565, 455), (535, 438), (535, 472)], fill="#98A5B8")
    d.line((945, 455, 995, 455), fill="#98A5B8", width=6)
    d.polygon([(995, 455), (965, 438), (965, 472)], fill="#98A5B8")

    feedback_x = 1030
    d.text((feedback_x, 265), "Instant Feedback", fill="#243047", font=font(29, True))
    feedback_rows = [
        ("Correct", "score +1"),
        ("Hint", "show clue"),
        ("Log", "save trial"),
    ]
    for i, (label, body) in enumerate(feedback_rows):
        y = 330 + i * 105
        draw_card(d, (feedback_x, y, feedback_x + 310, y + 82), label, body, ["#24A06B", "#F28C28", "#7A5AF8"][i])

    d.rounded_rectangle((250, 720, 1250, 780), radius=22, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((315, 737), "output/ch07_teaching_feedback_game.json", fill="#8A5A00", font=font(24, True))
    d.rounded_rectangle((250, 800, 1250, 855), radius=22, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((350, 815), "Report: reports/ch07_teaching_feedback_game.md", fill="#465263", font=font(22))

    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    plan = build_game_plan(load_memory_queue())
    write_outputs(plan)
    draw_preview(plan)
    copy_asset()
    print(f"created {PLAN_JSON.relative_to(ROOT)}")
    print(f"created {REPORT.relative_to(ROOT)}")
    print(f"created {PREVIEW.relative_to(ROOT)}")
    print(f"synced {WEB_DIR.relative_to(ROOT) / PREVIEW.name}")


if __name__ == "__main__":
    main()
