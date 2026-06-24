"""Generate source cards from the scraped-link CSV."""
from csv import DictReader
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
LINKS_CSV = OUTPUT / "links.csv"


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def ensure_sample_csv() -> None:
    OUTPUT.mkdir(exist_ok=True)
    if LINKS_CSV.exists():
        return
    LINKS_CSV.write_text(
        "\n".join(
            [
                "text,url",
                "Python 官方文档,https://docs.python.org/zh-cn/3/",
                "Python 包索引,https://pypi.org/",
                "Python robots.txt,https://www.python.org/robots.txt",
            ]
        ),
        encoding="utf-8",
    )


def load_links() -> list[dict[str, str]]:
    ensure_sample_csv()
    with LINKS_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(DictReader(f))
    cleaned = []
    for row in rows:
        title = row.get("text") or row.get("title") or "未命名来源"
        url = row.get("url") or row.get("href") or ""
        if url:
            cleaned.append({"title": title.strip(), "url": url.strip()})
    return cleaned


def classify(url: str) -> tuple[str, str]:
    domain = urlparse(url).netloc.lower()
    if "python.org" in domain or domain.endswith(".edu"):
        return "高可信", "官方/教育来源"
    if "wikipedia.org" in domain or "commons.wikimedia.org" in domain:
        return "需交叉验证", "开放百科来源"
    return "待检查", "普通网页来源"


def make_markdown(cards: list[dict[str, str]]) -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第8章来源卡片",
        "",
        "采集链接之后，不要急着复制进报告。先把它变成来源卡片：标题、域名、可信度、使用提醒，都写清楚。",
        "",
        "| 标题 | 域名 | 可信度 | 使用提醒 | URL |",
        "| --- | --- | --- | --- | --- |",
    ]
    for card in cards:
        domain = urlparse(card["url"]).netloc
        trust, note = classify(card["url"])
        lines.append(f"| {card['title']} | {domain} | {trust} | {note} | {card['url']} |")
    lines.extend(
        [
            "",
            "## 采集前自检",
            "",
            "- 能不能说明这个链接为什么要采集？",
            "- 有没有保留来源标题、URL 和访问边界？",
            "- 如果网页明天变化，报告里是否还能看出当时抓了什么？",
        ]
    )
    path = REPORTS / "ch08_source_cards.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def shorten(text: str, max_len: int = 21) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "..."


def make_preview(cards: list[dict[str, str]]) -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 830), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "公开资料来源卡片", fill="#162033", font=font(52, True))
    d.text((150, 198), "爬虫不是只拿链接，而是留下能复查的学习记录链。", fill="#5F6673", font=font(28))

    palette = {"高可信": "#24A06B", "需交叉验证": "#F28C28", "待检查": "#7A5AF8"}
    visible = cards[:4]
    for i, card in enumerate(visible):
        row = i // 2
        col = i % 2
        x = 150 + col * 610
        y = 285 + row * 235
        trust, note = classify(card["url"])
        color = palette[trust]
        domain = urlparse(card["url"]).netloc
        d.rounded_rectangle((x + 8, y + 10, x + 545, y + 185), radius=22, fill="#DEE5EF")
        d.rounded_rectangle((x, y, x + 545, y + 175), radius=22, fill="#F8FAFC", outline="#E2E8F0", width=2)
        d.rounded_rectangle((x, y, x + 545, y + 16), radius=8, fill=color)
        d.text((x + 26, y + 40), shorten(card["title"], 20), fill="#162033", font=font(28, True))
        d.text((x + 26, y + 82), domain, fill="#64748B", font=font(22))
        d.rounded_rectangle((x + 26, y + 120, x + 160, y + 150), radius=15, fill=color)
        d.text((x + 42, y + 123), trust, fill="#FFFFFF", font=font(18, True))
        d.text((x + 184, y + 122), note, fill="#334155", font=font(20))

    d.rounded_rectangle((150, 735, 1350, 785), radius=20, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((180, 748), "来源卡片口诀：标题要有，链接要留，边界要写，引用前要再看一眼。", fill="#1D4ED8", font=font(24))
    path = OUTPUT / "ch08_source_cards_preview.png"
    im.save(path, optimize=True, quality=95)
    return path


def main():
    cards = load_links()
    report = make_markdown(cards)
    preview = make_preview(cards)
    print("created source cards:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
