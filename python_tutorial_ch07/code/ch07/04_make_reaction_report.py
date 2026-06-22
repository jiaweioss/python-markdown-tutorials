"""Generate a small reaction-game report for the chapter project."""
from pathlib import Path
from statistics import mean

from PIL import Image, ImageDraw, ImageFont


REPORTS = Path("reports")
TRIALS = [
    {"word": "BLUE", "correct": True, "reaction_ms": 438},
    {"word": "GREEN", "correct": True, "reaction_ms": 512},
    {"word": "RED", "correct": False, "reaction_ms": 690},
    {"word": "YELLOW", "correct": True, "reaction_ms": 476},
    {"word": "PURPLE", "correct": True, "reaction_ms": 455},
]


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def make_markdown():
    REPORTS.mkdir(exist_ok=True)
    accuracy = sum(1 for trial in TRIALS if trial["correct"]) / len(TRIALS)
    avg_rt = mean(trial["reaction_ms"] for trial in TRIALS if trial["correct"])
    lines = [
        "# 第7章关键词反应小游戏报告",
        "",
        f"- 试次数：{len(TRIALS)}",
        f"- 正确率：{accuracy:.0%}",
        f"- 正确试次平均反应时：{avg_rt:.1f} ms",
        "",
        "| 目标词 | 是否正确 | 反应时 ms |",
        "| --- | --- | --- |",
    ]
    for trial in TRIALS:
        result = "正确" if trial["correct"] else "错误"
        lines.append(f"| {trial['word']} | {result} | {trial['reaction_ms']} |")
    path = REPORTS / "ch07_reaction_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def make_preview():
    REPORTS.mkdir(exist_ok=True)
    accuracy = sum(1 for trial in TRIALS if trial["correct"]) / len(TRIALS)
    avg_rt = mean(trial["reaction_ms"] for trial in TRIALS if trial["correct"])

    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 830), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "关键词反应小游戏报告", fill="#162033", font=font(52, True))
    d.text((150, 200), "窗口负责交互，报告负责复盘。", fill="#5F6673", font=font(30))

    cards = [
        ("试次数", str(len(TRIALS)), "#2F6BFF"),
        ("正确率", f"{accuracy:.0%}", "#24A06B"),
        ("平均反应时", f"{avg_rt:.0f} ms", "#F28C28"),
    ]
    for i, (label, value, color) in enumerate(cards):
        x = 150 + i * 390
        d.rounded_rectangle((x, 290, x + 330, 430), radius=22, fill="#F1F5F9", outline="#E2E8F0", width=2)
        d.rounded_rectangle((x, 290, x + 330, 302), radius=6, fill=color)
        d.text((x + 28, 325), label, fill="#5F6673", font=font(24))
        d.text((x + 28, 365), value, fill="#162033", font=font(38, True))

    y = 500
    for trial in TRIALS:
        width = min(760, int(trial["reaction_ms"] * 0.9))
        color = "#24A06B" if trial["correct"] else "#E84C61"
        d.text((150, y - 4), trial["word"], fill="#162033", font=font(24, True))
        d.rounded_rectangle((290, y, 290 + width, y + 28), radius=14, fill=color)
        d.text((1090, y - 4), f"{trial['reaction_ms']} ms", fill="#5F6673", font=font(23))
        y += 55

    d.rounded_rectangle((150, 755, 1350, 795), radius=18, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((180, 763), "复盘提示：先看正确率，再看反应时；游戏分数背后也可以是实验记录。", fill="#1D4ED8", font=font(23))
    path = REPORTS / "ch07_reaction_report_preview.png"
    im.save(path, optimize=True, quality=95)
    return path


def main():
    report = make_markdown()
    preview = make_preview()
    print("已生成关键词反应小游戏报告：")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
