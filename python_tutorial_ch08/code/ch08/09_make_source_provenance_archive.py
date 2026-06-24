"""Create a source provenance archive for chapter 08 outputs."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch08" / "web"

LINKS = OUTPUT / "links.csv"
BUNDLE = OUTPUT / "ch08_public_source_bundle.json"
PREVIEW = OUTPUT / "ch08_source_provenance_archive.png"
REPORT = REPORTS / "ch08_source_provenance_archive.md"
ASSET_COPY = WEB_DIR / "ch08_source_provenance_archive.png"


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


def read_links() -> list[dict[str, str]]:
    if not LINKS.exists():
        return []
    with LINKS.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_bundle() -> dict:
    if not BUNDLE.exists():
        return {"items": []}
    return json.loads(BUNDLE.read_text(encoding="utf-8"))


def score_url(url: str) -> tuple[int, str]:
    parsed = urlparse(url)
    score = 0
    notes = []
    if parsed.scheme == "https":
        score += 2
        notes.append("https")
    if any(key in parsed.netloc for key in ["python.org", "edu", "w3.org", "archive.org"]):
        score += 3
        notes.append("trusted domain")
    if parsed.path and parsed.path != "/":
        score += 1
        notes.append("specific page")
    if not notes:
        notes.append("needs review")
    return score, ", ".join(notes)


def collect_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for item in read_links():
        url = item.get("url") or item.get("link") or ""
        title = item.get("title") or url
        score, note = score_url(url)
        rows.append(
            {
                "title": title,
                "url": url,
                "domain": urlparse(url).netloc or "local",
                "type": "link",
                "score": score,
                "note": note,
            }
        )

    bundle = read_bundle()
    for item in bundle.get("items", []):
        url = item.get("url", "")
        score, note = score_url(url)
        rows.append(
            {
                "title": item.get("source_title", item.get("topic", url)),
                "url": url,
                "domain": urlparse(url).netloc or "local",
                "type": item.get("source_type", "bundle"),
                "score": score,
                "note": note,
            }
        )

    unique: dict[str, dict[str, str | int]] = {}
    for row in rows:
        key = str(row["url"]) or str(row["title"])
        unique[key] = row
    return list(unique.values())[:8]


def write_report(rows: list[dict[str, str | int]]) -> None:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第8章来源追踪档案",
        "",
        f"生成日期：{date.today().isoformat()}",
        "",
        "这份档案把本章采集到的链接、来源卡片和公开资料采集包集中到一起，检查每条资料是否有标题、URL、域名、可信度线索和复查提醒。",
        "",
        "| 标题 | 域名 | 类型 | 分数 | 复查提醒 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        title = str(row["title"]).replace("|", " ")
        lines.append(f"| {title} | {row['domain']} | {row['type']} | {row['score']} | {row['note']} |")

    lines.extend(
        [
            "",
            "## 使用提醒",
            "",
            "- 能打开的网页不等于能引用，先记录来源，再决定是否入库。",
            "- 官方文档、教育机构和明确署名的资料优先进入学习卡片。",
            "- 分数低的资料不一定不能用，但要先做交叉验证，并写明为什么保留。",
            "- 采集脚本应该遵守网站规则、控制频率，并保留访问日期。",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def truncate(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt) -> str:
    if draw.textlength(text, font=fnt) <= max_width:
        return text
    text = text.strip()
    while text and draw.textlength(text + "...", font=fnt) > max_width:
        text = text[:-1]
    return text + "..."


def draw_preview(rows: list[dict[str, str | int]]) -> None:
    OUTPUT.mkdir(exist_ok=True)
    image = Image.new("RGB", (1600, 1050), "#F7F8FB")
    draw = ImageDraw.Draw(image)
    title_font = font(52, True)
    subtitle_font = font(24)
    head_font = font(22, True)
    row_font = font(20)
    small_font = font(18)

    draw.rounded_rectangle((80, 70, 1520, 970), radius=30, fill="#FFFFFF", outline="#D8E0EC", width=3)
    draw.text((140, 120), "来源追踪档案", fill="#162033", font=title_font)
    draw.text((142, 185), "链接要变成可追踪来源，而不是散落书签。", fill="#64748B", font=subtitle_font)

    stats = [
        ("Sources", len(rows), "#2F6BFF"),
        ("HTTPS", sum(1 for r in rows if str(r["url"]).startswith("https://")), "#24A06B"),
        ("Trusted", sum(1 for r in rows if int(r["score"]) >= 5), "#F28C28"),
        ("Review", sum(1 for r in rows if int(r["score"]) < 5), "#7A5AF8"),
    ]
    x = 140
    for label, value, color in stats:
        draw.rounded_rectangle((x, 250, x + 300, 350), radius=20, fill="#F1F5F9", outline="#E2E8F0", width=2)
        draw.text((x + 24, 273), label, fill="#64748B", font=small_font)
        draw.text((x + 24, 302), str(value), fill=color, font=font(34, True))
        x += 335

    draw.rounded_rectangle((140, 410, 1460, 860), radius=22, fill="#FBFCFF", outline="#D8E0EC", width=2)
    headers = [("Title", 170), ("Domain", 710), ("Type", 1010), ("Score", 1220), ("Note", 1320)]
    for label, hx in headers:
        draw.text((hx, 435), label, fill="#334155", font=head_font)
    draw.line((170, 475, 1430, 475), fill="#D8E0EC", width=2)

    y = 495
    for i, row in enumerate(rows[:7]):
        fill = "#FFFFFF" if i % 2 == 0 else "#F6F8FC"
        draw.rounded_rectangle((160, y - 7, 1440, y + 39), radius=10, fill=fill)
        score = int(row["score"])
        score_color = "#24A06B" if score >= 5 else "#F28C28"
        draw.text((170, y), truncate(draw, str(row["title"]), 500, row_font), fill="#162033", font=row_font)
        draw.text((710, y), truncate(draw, str(row["domain"]), 250, row_font), fill="#475569", font=row_font)
        draw.text((1010, y), truncate(draw, str(row["type"]), 180, row_font), fill="#475569", font=row_font)
        draw.text((1240, y), str(score), fill=score_color, font=row_font)
        draw.text((1320, y), truncate(draw, str(row["note"]), 115, row_font), fill="#64748B", font=row_font)
        y += 50

    draw.rounded_rectangle((255, 900, 1345, 940), radius=18, fill="#EFF6FF", outline="#BFDBFE", width=2)
    draw.text((440, 908), "由 code/ch08/09_make_source_provenance_archive.py 生成", fill="#1D4ED8", font=small_font)
    image.save(PREVIEW, optimize=True, quality=95)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, ASSET_COPY)


def main() -> None:
    rows = collect_rows()
    write_report(rows)
    draw_preview(rows)
    print(f"created {REPORT.relative_to(ROOT)}")
    print(f"created {PREVIEW.relative_to(ROOT)}")
    print(f"synced {ASSET_COPY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
