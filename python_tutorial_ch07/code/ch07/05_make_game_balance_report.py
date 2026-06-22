"""Generate a small game-balance report for the PyGame chapter."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPORTS = Path("reports")
OUTPUT = Path("output")

ROUNDS = [
    {"round": 1, "target_ms": 900, "avg_ms": 720, "accuracy": 0.96, "challenge": "warm-up"},
    {"round": 2, "target_ms": 750, "avg_ms": 640, "accuracy": 0.90, "challenge": "steady"},
    {"round": 3, "target_ms": 620, "avg_ms": 610, "accuracy": 0.82, "challenge": "flow"},
    {"round": 4, "target_ms": 520, "avg_ms": 570, "accuracy": 0.66, "challenge": "too hard"},
]


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


def make_markdown() -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第7章小游戏难度调参报告",
        "",
        "一个好玩的教学小游戏，不是越难越好，也不是越简单越好。目标是让玩家停在“够得着但需要专注”的区域。",
        "",
        "| 轮次 | 目标反应时 ms | 平均反应时 ms | 正确率 | 状态 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in ROUNDS:
        lines.append(
            f"| {item['round']} | {item['target_ms']} | {item['avg_ms']} | {item['accuracy']:.0%} | {item['challenge']} |"
        )
    lines.extend(
        [
            "",
            "## 调参建议",
            "",
            "- 正确率高且反应快：可以略微提高难度。",
            "- 正确率下降但仍愿意继续：可能正接近心流区。",
            "- 正确率明显下降：先给提示或放慢节奏，不要只惩罚玩家。",
        ]
    )
    path = REPORTS / "ch07_game_balance_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def make_preview() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 830), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "小游戏难度调参图", fill="#162033", font=font(52, True))
    d.text((150, 198), "让目标、反馈、难度一起服务学习，而不是只追求刺激。", fill="#5F6673", font=font(28))

    chart = (165, 295, 1325, 660)
    x1, y1, x2, y2 = chart
    d.line((x1, y2, x2, y2), fill="#CBD5E1", width=4)
    d.line((x1, y1, x1, y2), fill="#CBD5E1", width=4)
    d.text((x1, y2 + 24), "低难度", fill="#64748B", font=font(22))
    d.text((x2 - 95, y2 + 24), "高难度", fill="#64748B", font=font(22))
    d.text((x1 - 20, y1 - 34), "投入感", fill="#64748B", font=font(22))

    flow_poly = [(420, 610), (590, 395), (770, 315), (960, 385), (1130, 610)]
    d.line(flow_poly, fill="#24A06B", width=14, joint="curve")
    d.rounded_rectangle((610, 350, 950, 515), radius=28, fill="#ECFDF5", outline="#A7F3D0", width=3)
    d.text((665, 386), "心流区", fill="#047857", font=font(34, True))
    d.text((650, 438), "目标清楚", fill="#047857", font=font(24))
    d.text((790, 438), "反馈及时", fill="#047857", font=font(24))

    palette = {"warm-up": "#2F6BFF", "steady": "#24A06B", "flow": "#F28C28", "too hard": "#E84C61"}
    for i, item in enumerate(ROUNDS):
        x = 360 + i * 245
        y = 610 - int(item["accuracy"] * 230)
        color = palette[item["challenge"]]
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=color)
        d.text((x - 42, y - 54), f"R{item['round']}", fill="#162033", font=font(22, True))
        d.text((x - 58, y + 28), f"{item['accuracy']:.0%}", fill="#64748B", font=font(20))

    d.rounded_rectangle((150, 710, 1350, 775), radius=22, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((182, 728), "调参口诀：太顺就加一点挑战，太挫就先给提示；游戏的目标是让人愿意再试一次。", fill="#1D4ED8", font=font(24))

    path = OUTPUT / "ch07_game_balance_preview.png"
    im.save(path, optimize=True, quality=95)
    return path


def main():
    report = make_markdown()
    preview = make_preview()
    print("created game balance report:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
