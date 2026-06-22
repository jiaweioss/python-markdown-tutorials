"""Chapter 02 artifact: make data type decision cards."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent


CARDS = [
    {
        "type": "bool",
        "question": "这是不是一个判断？",
        "use": "保存 True / False，例如是否通过、是否完成、是否需要复习。",
        "example": "passed = average_score >= 60",
    },
    {
        "type": "int / float",
        "question": "这是不是数量、得分、时长或比例？",
        "use": "保存可以计算的数字。整数适合次数和编号，小数适合平均分和反应时。",
        "example": "time_ms = 523.7",
    },
    {
        "type": "str",
        "question": "这是不是一段文字？",
        "use": "保存姓名、题目、路径、标签、备注等文本信息。",
        "example": "student_name = '小明'",
    },
    {
        "type": "list",
        "question": "这是不是一串有顺序的数据？",
        "use": "保存多次测验分数、实验 trial、单词清单等可以逐个遍历的内容。",
        "example": "scores = [86, 92, 78]",
    },
    {
        "type": "dict",
        "question": "这是不是查找表？",
        "use": "保存一名学生、一张卡片、一次实验或一个文件的完整记录。",
        "example": "student = {'name': '小明'}",
    },
    {
        "type": "None",
        "question": "这里是不是暂时没有值？",
        "use": "保存“还没有结果”的状态，不要用空字符串或 0 假装缺失。",
        "example": "review_date = None",
    },
]


def build_markdown() -> str:
    lines = [
        "# 第2章类型选择卡片",
        "",
        "看到一份新数据时，先不要急着写代码。先问：它是什么、会不会变、要不要计算、要不要查找。",
        "",
    ]
    for card in CARDS:
        lines.extend(
            [
                f"## {card['type']}",
                "",
                f"- 判断问题：{card['question']}",
                f"- 使用场景：{card['use']}",
                f"- 代码例子：`{card['example']}`",
                "",
            ]
        )
    return "\n".join(lines)


def write_preview_png(output_file: Path) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()

    width, height = 1600, 1040
    image = Image.new("RGB", (width, height), "#F6F8FB")
    draw = ImageDraw.Draw(image)
    title_font = font(52, True)
    h_font = font(30, True)
    body_font = font(22)
    mono_font = font(20)
    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8", "#18A9B5", "#E84C61"]

    def draw_wrapped(text: str, x: int, y: int, chars: int, fnt, fill: str, gap: int = 7) -> int:
        lines = [text[i : i + chars] for i in range(0, len(text), chars)]
        for line in lines[:3]:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += fnt.size + gap
        return y

    draw.text((80, 60), "第2章类型选择卡片", font=title_font, fill="#172033")
    draw.text((84, 128), "先判断数据的性格，再选择合适的 Python 类型。", font=body_font, fill="#5D6678")

    card_w, card_h = 455, 255
    positions = [(80, 210), (570, 210), (1060, 210), (80, 515), (570, 515), (1060, 515)]
    for idx, (card, (x, y)) in enumerate(zip(CARDS, positions)):
        color = colors[idx]
        draw.rounded_rectangle((x + 8, y + 10, x + card_w + 8, y + card_h + 10), radius=22, fill="#D8DEE9")
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=22, fill="#FFFFFF", outline="#D9E1EE", width=2)
        draw.rounded_rectangle((x + 24, y + 24, x + 142, y + 66), radius=21, fill=color)
        draw.text((x + 43, y + 31), card["type"], font=body_font, fill="white")
        draw_wrapped(card["question"], x + 24, y + 92, 13, h_font, "#172033", gap=6)
        draw.text((x + 24, y + 160), card["example"], font=mono_font, fill=color)

        draw.text((x + 24, y + 208), "详细解释见 Markdown 卡片", font=body_font, fill="#5D6678")

    draw.rounded_rectangle((220, 860, 1380, 960), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw.text(
        (270, 894),
        "真正的入门不是背类型名，而是看到材料时能选对容器。",
        font=body_font,
        fill="#8A5A00",
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_file, optimize=True, quality=95)
    return True


def main() -> None:
    reports_dir = Path("reports")
    output_dir = Path("output")
    reports_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    markdown_file = reports_dir / "ch02_type_decision_cards.md"
    preview_file = output_dir / "ch02_type_decision_cards_preview.png"

    markdown_file.write_text(build_markdown(), encoding="utf-8")
    has_preview = write_preview_png(preview_file)

    print(dedent(
        f"""
        类型选择卡片已生成：
        - {markdown_file}
        - {preview_file if has_preview else '未生成 PNG：当前环境缺少 Pillow'}
        """
    ).strip())


if __name__ == "__main__":
    main()
