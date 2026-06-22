"""Create a small crawl report from collected public links."""
import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
LINKS_CSV = OUTPUT / "links.csv"


def load_links():
    if not LINKS_CSV.exists():
        raise FileNotFoundError("请先运行 code/ch08/03_save_links_csv.py 生成 output/links.csv")
    with LINKS_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def font(size):
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def make_markdown_report(links):
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第8章公开资料采集报告",
        "",
        "## 采集边界",
        "- 先解析本地 HTML，避免一开始就频繁请求网站。",
        "- 请求公开网页前先查看 robots.txt。",
        "- 保存标题和链接，方便后续复查来源。",
        "",
        "## 链接清单",
        "",
        "| 标题 | URL |",
        "| --- | --- |",
    ]
    for item in links:
        lines.append(f"| {item['title']} | {item['url']} |")
    path = REPORTS / "ch08_crawl_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def make_preview(links):
    REPORTS.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 830), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "公开资料采集报告", fill="#162033", font=font(54))
    d.text((150, 205), "先看规则，再取链接，最后保存可复查结果。", fill="#5F6673", font=font(30))

    y = 310
    for i, item in enumerate(links, start=1):
        d.rounded_rectangle((150, y, 1350, y + 86), radius=18, fill="#F1F5F9", outline="#E2E8F0", width=2)
        d.ellipse((180, y + 25, 216, y + 61), fill="#2F6BFF")
        d.text((192, y + 29), str(i), fill="#FFFFFF", font=font(20))
        d.text((245, y + 16), item["title"], fill="#162033", font=font(28))
        d.text((245, y + 50), item["url"], fill="#5F6673", font=font(22))
        y += 112

    d.rounded_rectangle((150, 690, 1350, 765), radius=18, fill="#FFF7ED", outline="#FDBA74", width=2)
    d.text((185, 710), "检查点：来源是否公开？robots.txt 是否允许？结果是否已经落盘？", fill="#9A3412", font=font(25))
    path = REPORTS / "ch08_crawl_report_preview.png"
    im.save(path, optimize=True, quality=95)
    return path


def main():
    links = load_links()
    report = make_markdown_report(links)
    preview = make_preview(links)
    print("已生成公开资料采集报告：")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
