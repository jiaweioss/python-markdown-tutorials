"""Create a public-source bundle for cards from the chapter 07 game plan."""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch08").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
BOOK_ROOT = ROOT.parent
CH07_GAME_PLAN = BOOK_ROOT / "python_tutorial_ch07" / "output" / "ch07_teaching_feedback_game.json"
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch08" / "web"
BUNDLE_JSON = OUTPUT / "ch08_public_source_bundle.json"
REPORT = REPORTS / "ch08_public_source_bundle.md"
PREVIEW = OUTPUT / "ch08_public_source_bundle.png"


FALLBACK_CARDS = [
    {"topic": "变量", "difficulty": "flow"},
    {"topic": "列表", "difficulty": "practice"},
    {"topic": "字典", "difficulty": "support"},
]

SOURCE_HINTS = {
    "变量": ("Python 官方教程：变量与赋值", "https://docs.python.org/zh-cn/3/tutorial/introduction.html"),
    "列表": ("Python 官方教程：列表", "https://docs.python.org/zh-cn/3/tutorial/datastructures.html"),
    "字典": ("Python 官方教程：字典", "https://docs.python.org/zh-cn/3/tutorial/datastructures.html#dictionaries"),
    "循环": ("Python 官方教程：流程控制", "https://docs.python.org/zh-cn/3/tutorial/controlflow.html"),
    "函数": ("Python 官方教程：定义函数", "https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions"),
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


def load_cards() -> list[dict]:
    if CH07_GAME_PLAN.exists():
        data = json.loads(CH07_GAME_PLAN.read_text(encoding="utf-8"))
        cards = data.get("cards", [])
        if cards:
            return cards
    return FALLBACK_CARDS


def make_search_url(topic: str) -> str:
    query = quote(f"Python {topic} site:docs.python.org")
    return f"https://www.google.com/search?q={query}"


def build_bundle(cards: list[dict]) -> dict:
    items = []
    for card in cards[:6]:
        topic = card["topic"]
        title, url = SOURCE_HINTS.get(topic, (f"Python {topic} 官方资料检索", make_search_url(topic)))
        items.append(
            {
                "topic": topic,
                "source_title": title,
                "url": url,
                "source_type": "official docs" if "docs.python.org" in url else "search task",
                "crawl_rule": "read page title and headings only",
                "reuse_note": "save title, url, access date and summary before adding to a learning card",
                "difficulty_from_game": card.get("difficulty", "practice"),
            }
        )
    return {
        "project": "public-source bundle for learning cards",
        "created": date.today().isoformat(),
        "source": str(CH07_GAME_PLAN) if CH07_GAME_PLAN.exists() else "fallback",
        "items": items,
    }


def write_outputs(bundle: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    BUNDLE_JSON.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 第8章公开资料采集包",
        "",
        "这份采集包读取 ch7 的教学反馈小游戏计划，把需要复习的卡片变成可复查的公开资料采集任务。爬虫在这里不是“到处抓”，而是像研究助理一样：先明确任务，再记录来源，最后留下边界说明。",
        "",
        f"生成日期：{bundle['created']}",
        "",
        "| 卡片 | 推荐来源 | 采集边界 | 入库提醒 |",
        "| --- | --- | --- | --- |",
    ]
    for item in bundle["items"]:
        lines.append(
            f"| {item['topic']} | [{item['source_title']}]({item['url']}) | "
            f"{item['crawl_rule']} | {item['reuse_note']} |"
        )
    lines.extend(
        [
            "",
            "## 使用提醒",
            "",
            "- 每条资料都要保存 URL、标题、访问日期和一句用途说明。",
            "- 官方文档适合作为概念卡片的底稿；博客和问答材料要先交叉验证。",
            "- 这份清单是采集计划，不是批量抓取授权。真正联网前仍要查看 robots 和网站条款。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_preview(bundle: dict) -> None:
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((80, 65, 1420, 850), radius=32, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((135, 120), "Public Source Bundle", fill="#162033", font=font(50, True))
    d.text((138, 184), "Learning cards become traceable source tasks.", fill="#526071", font=font(25))

    left_x, mid_x, right_x = 140, 560, 1010
    d.text((left_x, 265), "Cards", fill="#243047", font=font(30, True))
    d.text((mid_x, 265), "Sources", fill="#243047", font=font(30, True))
    d.text((right_x, 265), "Rules", fill="#243047", font=font(30, True))

    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]
    for i, item in enumerate(bundle["items"][:4]):
        y = 325 + i * 96
        color = colors[i % len(colors)]
        d.rounded_rectangle((left_x, y, left_x + 310, y + 72), radius=20, fill="#FFFFFF", outline="#D8E0EC", width=2)
        d.rounded_rectangle((left_x, y, left_x + 310, y + 10), radius=5, fill=color)
        d.text((left_x + 24, y + 24), item["topic"], fill="#162033", font=font(25, True))
        d.text((left_x + 24, y + 50), item["difficulty_from_game"], fill="#64748B", font=font(18))

        d.line((left_x + 330, y + 36, mid_x - 28, y + 36), fill="#98A5B8", width=5)
        d.polygon([(mid_x - 28, y + 36), (mid_x - 54, y + 21), (mid_x - 54, y + 51)], fill="#98A5B8")

        d.rounded_rectangle((mid_x, y, mid_x + 360, y + 72), radius=20, fill="#F8FAFC", outline="#E2E8F0", width=2)
        d.text((mid_x + 22, y + 19), item["source_type"], fill="#166534", font=font(23, True))
        d.text((mid_x + 22, y + 48), "title + url + date", fill="#64748B", font=font(18))

        d.line((mid_x + 380, y + 36, right_x - 28, y + 36), fill="#98A5B8", width=5)
        d.polygon([(right_x - 28, y + 36), (right_x - 54, y + 21), (right_x - 54, y + 51)], fill="#98A5B8")

        d.rounded_rectangle((right_x, y, right_x + 330, y + 72), radius=20, fill="#FFF7E8", outline="#F2B84B", width=2)
        d.text((right_x + 22, y + 19), "polite crawl", fill="#8A5A00", font=font(22, True))
        d.text((right_x + 22, y + 48), "scope + source", fill="#8A5A00", font=font(18))

    d.rounded_rectangle((250, 725, 1250, 780), radius=21, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((315, 740), "output/ch08_public_source_bundle.json", fill="#1D4ED8", font=font(24, True))
    d.rounded_rectangle((250, 795, 1250, 842), radius=19, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((405, 806), "reports/ch08_public_source_bundle.md", fill="#465263", font=font(21))
    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    bundle = build_bundle(load_cards())
    write_outputs(bundle)
    draw_preview(bundle)
    copy_asset()
    print(f"created {BUNDLE_JSON.relative_to(ROOT)}")
    print(f"created {REPORT.relative_to(ROOT)}")
    print(f"created {PREVIEW.relative_to(ROOT)}")
    print(f"synced {WEB_DIR.relative_to(ROOT) / PREVIEW.name}")


if __name__ == "__main__":
    main()
