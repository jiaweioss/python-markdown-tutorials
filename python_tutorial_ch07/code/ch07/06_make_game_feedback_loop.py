"""Generate a game feedback-loop card for chapter 07."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path("output")
REPORTS = Path("reports")
WEB_DIR = Path("assets/ch07/web")
PREVIEW = OUTPUT / "ch07_game_feedback_loop.png"
REPORT = REPORTS / "ch07_game_feedback_loop.md"

STEPS = [
    ("Goal", "目标清楚：看到目标词时按 Space"),
    ("Input", "输入明确：只监听需要的按键"),
    ("Update", "状态更新：分数、提示、反应记录同步变化"),
    ("Feedback", "反馈及时：画面和文字立刻回应玩家"),
    ("Retry", "愿意再试：难度让人觉得够得着"),
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


def make_markdown() -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第7章游戏反馈循环卡",
        "",
        "一个小游戏真正让人愿意继续玩，靠的不是复杂特效，而是清楚目标、明确输入、及时反馈和合适难度。",
        "",
        "| 环节 | 检查问题 |",
        "| --- | --- |",
    ]
    for label, tip in STEPS:
        lines.append(f"| {label} | {tip} |")
    lines.extend(
        [
            "",
            "## 复盘提示",
            "",
            "每次改小游戏时，先问：玩家知道要做什么吗？按键有反馈吗？分数变化可见吗？失败后还想再试一次吗？",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return REPORT


def make_preview() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 920), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "Game Feedback Loop", fill="#162033", font=font(52, True))
    d.text((150, 198), "让小游戏从“能运行”变成“愿意再试”。", fill="#5F6673", font=font(28))

    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8", "#18A9B5"]
    center = (750, 520)
    points = [(750, 285), (1035, 405), (930, 700), (570, 700), (465, 405)]
    for i, (label, tip) in enumerate(STEPS):
        x, y = points[i]
        color = colors[i]
        d.line((center[0], center[1], x, y), fill="#CBD5E1", width=4)
        d.ellipse((x - 78, y - 78, x + 78, y + 78), fill="#FFFFFF", outline=color, width=6)
        d.text((x - 44, y - 36), label, fill=color, font=font(23, True))
        d.text((x - 145, y + 92), tip, fill="#334155", font=font(20))

    d.ellipse((center[0] - 118, center[1] - 118, center[0] + 118, center[1] + 118), fill="#EFF6FF", outline="#93C5FD", width=4)
    d.text((center[0] - 70, center[1] - 38), "Loop", fill="#1D4ED8", font=font(38, True))
    d.text((center[0] - 82, center[1] + 12), "60 FPS", fill="#1D4ED8", font=font(26, True))

    d.rounded_rectangle((210, 795, 1290, 838), radius=20, fill="#FFF7ED", outline="#FDBA74", width=2)
    d.text((275, 805), "游戏反馈口诀：目标清楚，按键有用，变化可见，失败还想再来。", fill="#9A3412", font=font(22, True))
    im.save(PREVIEW, optimize=True, quality=95)
    return PREVIEW


def copy_assets() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    report = make_markdown()
    preview = make_preview()
    copy_assets()
    print("created game feedback loop:")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
