"""Generate a data-driven tuning card for the PyGame reaction game."""

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
CH06_SUMMARY = BOOK_ROOT / "python_tutorial_ch06" / "output" / "ch06_ch05_handoff_summary.json"
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch07" / "web"
TUNING_JSON = OUTPUT / "ch07_data_driven_tuning.json"
REPORT = REPORTS / "ch07_data_driven_tuning.md"
PREVIEW = OUTPUT / "ch07_data_driven_tuning.png"


FALLBACK_SUMMARY = {
    "source": "fallback",
    "card_count": 2,
    "tag_counts": {"OOP": 1, "class": 1, "object": 1, "composition": 1},
    "avg_question_length": 24.5,
    "trial_reaction_time_ms": 438.5,
    "trial_is_fast": True,
}


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


def load_summary() -> dict:
    if CH06_SUMMARY.exists():
        return json.loads(CH06_SUMMARY.read_text(encoding="utf-8"))
    return FALLBACK_SUMMARY


def build_tuning(summary: dict) -> dict:
    rt = float(summary["trial_reaction_time_ms"])
    card_count = int(summary["card_count"])
    tag_count = len(summary["tag_counts"])

    if rt < 450:
        difficulty = "flow"
        spawn_interval_ms = 950
        target_window_ms = 620
        advice = "保持节奏，增加少量新词。"
    elif rt < 650:
        difficulty = "practice"
        spawn_interval_ms = 1150
        target_window_ms = 760
        advice = "先稳定正确率，再逐步加速。"
    else:
        difficulty = "support"
        spawn_interval_ms = 1400
        target_window_ms = 920
        advice = "降低速度，增加提示和复盘。"

    return {
        "source": summary["source"],
        "card_count": card_count,
        "tag_count": tag_count,
        "reaction_time_ms": rt,
        "difficulty_band": difficulty,
        "spawn_interval_ms": spawn_interval_ms,
        "target_window_ms": target_window_ms,
        "round_cards": max(3, card_count + tag_count),
        "advice": advice,
    }


def write_outputs(tuning: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    TUNING_JSON.write_text(json.dumps(tuning, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 第 7 章数据驱动游戏调参记录",
        "",
        "这份记录读取 ch6 的跨章节数据分析摘要，把反应时和卡片信息转换成小游戏难度建议。",
        "",
        "| 指标 | 结果 |",
        "| --- | --- |",
        f"| 数据来源 | {tuning['source']} |",
        f"| 卡片数 | {tuning['card_count']} |",
        f"| 标签种类 | {tuning['tag_count']} |",
        f"| 反应时 | {tuning['reaction_time_ms']} ms |",
        f"| 难度带 | {tuning['difficulty_band']} |",
        f"| 出题间隔 | {tuning['spawn_interval_ms']} ms |",
        f"| 目标反应窗口 | {tuning['target_window_ms']} ms |",
        f"| 一轮卡片数 | {tuning['round_cards']} |",
        f"| 调参建议 | {tuning['advice']} |",
        "",
        "下一步可以把这些参数写入 PyGame 主循环，让游戏根据真实学习数据调整节奏。",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_preview(tuning: dict) -> None:
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "数据驱动游戏调参", fill="#162033", font=font(48, True))
    d.text((152, 195), "学习数据会变成 PyGame 的难度设置。", fill="#5F6673", font=font(26))

    d.rounded_rectangle((150, 285, 610, 610), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    d.text((190, 325), "数据", fill="#28517A", font=font(30, True))
    d.text((190, 385), f"cards: {tuning['card_count']}", fill="#162033", font=font(27, True))
    d.text((190, 440), f"tags: {tuning['tag_count']}", fill="#465263", font=font(25))
    d.text((190, 495), f"rt: {tuning['reaction_time_ms']} ms", fill="#465263", font=font(25))

    d.line((660, 445, 805, 445), fill="#98A5B8", width=6)
    d.polygon([(805, 445), (775, 428), (775, 462)], fill="#98A5B8")

    d.rounded_rectangle((850, 285, 1350, 610), radius=24, fill="#ECFDF3", outline="#8EE3B0", width=3)
    d.text((890, 325), "调参", fill="#166534", font=font(30, True))
    rows = [
        ("band", tuning["difficulty_band"]),
        ("spawn", f"{tuning['spawn_interval_ms']} ms"),
        ("window", f"{tuning['target_window_ms']} ms"),
        ("round", f"{tuning['round_cards']} cards"),
    ]
    y = 382
    for label, value in rows:
        d.rounded_rectangle((890, y, 1305, y + 42), radius=17, fill="#FFFFFF", outline="#D8E0EC", width=2)
        d.text((918, y + 8), label, fill="#166534", font=font(21, True))
        d.text((1110, y + 8), value, fill="#162033", font=font(21, True))
        y += 56

    d.rounded_rectangle((250, 700, 1250, 760), radius=20, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((340, 717), "output/ch07_data_driven_tuning.json", fill="#8A5A00", font=font(25, True))
    d.rounded_rectangle((250, 790, 1250, 845), radius=20, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((375, 805), "记录：reports/ch07_data_driven_tuning.md", fill="#465263", font=font(22))

    OUTPUT.mkdir(exist_ok=True)
    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    tuning = build_tuning(load_summary())
    write_outputs(tuning)
    draw_preview(tuning)
    copy_asset()
    print(f"已生成 {TUNING_JSON.relative_to(ROOT)}")
    print(f"已生成 {REPORT.relative_to(ROOT)}")
    print(f"已生成 {PREVIEW.relative_to(ROOT)}")
    print(f"已同步 {WEB_DIR.relative_to(ROOT) / PREVIEW.name}")


if __name__ == "__main__":
    main()
