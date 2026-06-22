"""Generate a source-quality scorecard for chapter 08."""

from __future__ import annotations

import shutil
from csv import DictReader
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_DIR = Path("assets/ch08/web")
LINKS_CSV = OUTPUT / "links.csv"
PREVIEW = OUTPUT / "ch08_source_quality_scorecard.png"
REPORT = REPORTS / "ch08_source_quality_scorecard.md"


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
                "Wikimedia Commons,https://commons.wikimedia.org/",
            ]
        ),
        encoding="utf-8",
    )


def load_links() -> list[dict[str, str]]:
    ensure_sample_csv()
    with LINKS_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(DictReader(f))
    links = []
    for row in rows:
        title = row.get("text") or row.get("title") or "未命名来源"
        url = row.get("url") or row.get("href") or ""
        if url:
            links.append({"title": title.strip(), "url": url.strip()})
    fallback = [
        {"title": "Python 包索引", "url": "https://pypi.org/"},
        {"title": "Python robots", "url": "https://www.python.org/robots.txt"},
        {"title": "Wikimedia Commons", "url": "https://commons.wikimedia.org/"},
    ]
    seen = {item["url"] for item in links}
    for item in fallback:
        if len(links) >= 5:
            break
        if item["url"] not in seen:
            links.append(item)
            seen.add(item["url"])
    return links


def score_link(url: str) -> tuple[int, list[str]]:
    domain = urlparse(url).netloc.lower()
    score = 0
    reasons = []
    if url.startswith("https://"):
        score += 1
        reasons.append("HTTPS")
    if "python.org" in domain or domain.endswith(".edu"):
        score += 2
        reasons.append("官方/教育")
    elif "wikipedia.org" in domain or "wikimedia.org" in domain:
        score += 1
        reasons.append("需复核")
    else:
        reasons.append("待检查")
    if "/robots.txt" in url:
        score += 1
        reasons.append("边界页")
    return min(score, 4), reasons


def make_markdown(links: list[dict[str, str]]) -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第8章来源可信度评分卡",
        "",
        f"检查日期：{date.today().isoformat()}",
        "",
        "爬虫采集完成后，不要让链接直接躺进报告。先给每个来源做一次小体检：它是不是 HTTPS？是不是官方或教育来源？是否需要交叉验证？是否保存了边界信息？",
        "",
        "| 标题 | 域名 | 分数 | 复查理由 |",
        "| --- | --- | --- | --- |",
    ]
    for item in links:
        domain = urlparse(item["url"]).netloc
        score, reasons = score_link(item["url"])
        lines.append(f"| {item['title']} | {domain} | {score}/4 | {'、'.join(reasons)} |")
    lines.extend(
        [
            "",
            "## 使用提醒",
            "",
            "- 分数不是判决书，只是提醒你下一步该怎么复查。",
            "- 官方文档也可能过期，普通网页也可能有价值，关键是写清来源、时间和用途。",
            "- 做心理学或教学资料整理时，宁可少抓一点，也要让每一条材料能回头查。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT


def make_preview(links: list[dict[str, str]]) -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 920), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "Source Quality Scorecard", fill="#162033", font=font(50, True))
    d.text((150, 195), "把链接从“能打开”检查到“能引用”。", fill="#5F6673", font=font(28))

    colors = ["#E84C61", "#F28C28", "#E6A600", "#24A06B", "#2F6BFF"]
    y = 290
    for item in links[:5]:
        score, reasons = score_link(item["url"])
        domain = urlparse(item["url"]).netloc
        color = colors[score]
        d.rounded_rectangle((150, y, 1350, y + 88), radius=20, fill="#F8FAFC", outline="#E2E8F0", width=2)
        d.text((180, y + 18), item["title"][:20], fill="#162033", font=font(25, True))
        d.text((180, y + 52), domain[:32], fill="#64748B", font=font(19))
        d.rounded_rectangle((720, y + 24, 900, y + 64), radius=20, fill=color)
        d.text((778, y + 29), f"{score}/4", fill="#FFFFFF", font=font(22, True))
        d.text((935, y + 29), " / ".join(reasons)[:24], fill="#334155", font=font(22))
        y += 102

    d.rounded_rectangle((210, 790, 1290, 830), radius=18, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((250, 800), "采集口诀：能打开只是开始，能复查才算入库。", fill="#1D4ED8", font=font(22, True))
    im.save(PREVIEW, optimize=True, quality=95)
    return PREVIEW


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    links = load_links()
    report = make_markdown(links)
    preview = make_preview(links)
    copy_assets()
    print("created source quality scorecard:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
