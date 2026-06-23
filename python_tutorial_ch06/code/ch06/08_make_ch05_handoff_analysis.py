"""Analyze the chapter 05 object-delivery package for chapter 06."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path
from statistics import mean

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch06").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
BOOK_ROOT = ROOT.parent
CH05_PACKAGE = BOOK_ROOT / "python_tutorial_ch05" / "output" / "ch05_object_delivery_package.json"
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch06" / "web"
SUMMARY_JSON = OUTPUT / "ch06_ch05_handoff_summary.json"
REPORT = REPORTS / "ch06_ch05_handoff_analysis.md"
PREVIEW = OUTPUT / "ch06_ch05_handoff_analysis.png"


FALLBACK_PACKAGE = {
    "deck": {
        "name": "科研卡片工厂 OOP 盒",
        "summary": "科研卡片工厂 OOP 盒: 2 cards",
        "cards": [
            {
                "topic": "类与对象",
                "question": "为什么类像图纸，对象像作品？",
                "answer": "类描述共同结构；对象保存具体状态并执行方法。",
                "tags": ["OOP", "class", "object"],
            },
            {
                "topic": "组合",
                "question": "为什么 CardDeck 拥有 LearningCard？",
                "answer": "卡片盒管理多张卡片，组合比继承更贴近真实职责。",
                "tags": ["composition", "responsibility"],
            },
        ],
    },
    "trial": {
        "participant": "S001",
        "stimulus": "RED/blue",
        "response": "j",
        "reaction_time_ms": 438.5,
        "is_fast": True,
    },
    "handoff": {
        "next_chapter": "第6章：数据分析与可视化",
        "next_action": "读取这份 JSON，把卡片和试次对象整理成可以分析的小表。",
    },
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


def load_package() -> tuple[dict, str]:
    if CH05_PACKAGE.exists():
        return json.loads(CH05_PACKAGE.read_text(encoding="utf-8")), "ch05"
    return FALLBACK_PACKAGE, "fallback"


def analyze_package(package: dict, source: str) -> dict:
    cards = package["deck"]["cards"]
    tag_counts = Counter(tag for card in cards for tag in card.get("tags", []))
    question_lengths = [len(card["question"]) for card in cards]
    trial = package["trial"]
    return {
        "source": source,
        "card_count": len(cards),
        "tag_counts": dict(tag_counts),
        "avg_question_length": round(mean(question_lengths), 1) if question_lengths else 0,
        "trial_reaction_time_ms": trial["reaction_time_ms"],
        "trial_is_fast": trial["is_fast"],
        "next_chapter": package["handoff"]["next_chapter"],
    }


def write_outputs(summary: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    tag_text = "、".join(f"{tag}={count}" for tag, count in summary["tag_counts"].items())
    lines = [
        "# 第 6 章跨章节数据分析回执",
        "",
        "这份回执读取第 5 章导出的对象交付包，把对象模型转换成可以分析的摘要数据。",
        "",
        "| 指标 | 结果 |",
        "| --- | --- |",
        f"| 数据来源 | {summary['source']} |",
        f"| 学习卡片数 | {summary['card_count']} |",
        f"| 标签计数 | {tag_text} |",
        f"| 平均问题长度 | {summary['avg_question_length']} 字 |",
        f"| 试次反应时 | {summary['trial_reaction_time_ms']} ms |",
        f"| 是否快速反应 | {summary['trial_is_fast']} |",
        f"| 下一章交接 | {summary['next_chapter']} |",
        "",
        "这一步说明：前一章的类和对象不只是课堂概念，也可以变成后一章的数据分析输入。",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_preview(summary: dict) -> None:
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "第5章到第6章：对象交接数据", fill="#162033", font=font(50, True))
    d.text((152, 195), "上一章导出的对象包，在本章变成可分析的表格线索。", fill="#5F6673", font=font(26))

    d.rounded_rectangle((150, 285, 575, 625), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    d.text((190, 325), "输入", fill="#28517A", font=font(30, True))
    d.text((190, 385), "对象交付包", fill="#162033", font=font(28, True))
    d.text((190, 445), f"卡片数：{summary['card_count']}", fill="#465263", font=font(25))
    d.text((190, 495), f"试次反应：{summary['trial_reaction_time_ms']} ms", fill="#465263", font=font(25))

    d.line((625, 455, 785, 455), fill="#98A5B8", width=6)
    d.polygon([(785, 455), (755, 438), (755, 472)], fill="#98A5B8")

    d.rounded_rectangle((835, 285, 1350, 625), radius=24, fill="#ECFDF3", outline="#8EE3B0", width=3)
    d.text((875, 325), "分析", fill="#166534", font=font(30, True))
    tag_items = list(summary["tag_counts"].items())[:4]
    y = 390
    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]
    for idx, (tag, count) in enumerate(tag_items):
        width = 110 + count * 95
        d.rounded_rectangle((875, y, 875 + width, y + 34), radius=17, fill=colors[idx % len(colors)])
        d.text((1000, y + 4), f"{tag}: {count}", fill="#162033", font=font(22, True))
        y += 54

    d.rounded_rectangle((250, 705, 1250, 765), radius=20, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((320, 722), "output/ch06_ch05_handoff_summary.json", fill="#8A5A00", font=font(25, True))
    d.rounded_rectangle((250, 790, 1250, 845), radius=20, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((350, 805), "报告：reports/ch06_ch05_handoff_analysis.md", fill="#465263", font=font(22))

    OUTPUT.mkdir(exist_ok=True)
    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    package, source = load_package()
    summary = analyze_package(package, source)
    write_outputs(summary)
    draw_preview(summary)
    copy_asset()
    print(f"已生成 {SUMMARY_JSON.relative_to(ROOT)}")
    print(f"已生成 {REPORT.relative_to(ROOT)}")
    print(f"已生成 {PREVIEW.relative_to(ROOT)}")
    print(f"已同步 {WEB_DIR.relative_to(ROOT) / PREVIEW.name}")


if __name__ == "__main__":
    main()
