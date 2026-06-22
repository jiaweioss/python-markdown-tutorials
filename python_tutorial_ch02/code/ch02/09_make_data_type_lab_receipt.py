"""Chapter 02 artifact: generate a data type lab receipt."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent


TRIAL = {
    "participant": "S001",
    "word": "RED",
    "ink_color": "blue",
    "response_key": "j",
    "correct": True,
    "reaction_time_ms": 612.4,
}

STUDENT = {
    "name": "小明",
    "scores": [86, 92, 78],
    "skills": ["字符串", "列表", "字典"],
    "next_review": None,
}


def build_markdown() -> str:
    average = sum(STUDENT["scores"]) / len(STUDENT["scores"])
    passed = average >= 60
    return dedent(
        f"""
        # 第2章数据类型实验回执

        ## 学习记录

        - 学生：{STUDENT["name"]}
        - 分数列表：{STUDENT["scores"]}
        - 平均分：{average:.1f}
        - 是否通过：{passed}
        - 已练习技能：{"、".join(STUDENT["skills"])}
        - 下次复习时间：{STUDENT["next_review"]}

        ## 心理学 trial 记录

        - 被试编号：{TRIAL["participant"]}
        - 刺激词：{TRIAL["word"]}
        - 墨水颜色：{TRIAL["ink_color"]}
        - 反应键：{TRIAL["response_key"]}
        - 是否正确：{TRIAL["correct"]}
        - 反应时：{TRIAL["reaction_time_ms"]} ms

        ## 类型选择说明

        - `str`：保存姓名、刺激词、墨水颜色和反应键。
        - `float`：保存反应时和平均分。
        - `bool`：保存是否通过、是否正确。
        - `list`：保存多次练习分数和技能清单。
        - `dict`：保存一名学生或一次 trial 的完整记录。
        - `None`：保存暂时还没有安排的下次复习时间。
        """
    ).strip() + "\n"


def write_preview_png(output_file: Path) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def load_font(size: int, bold: bool = False):
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

    width, height = 1600, 1000
    image = Image.new("RGB", (width, height), "#F6F8FB")
    draw = ImageDraw.Draw(image)
    title_font = load_font(50, True)
    h_font = load_font(30, True)
    body_font = load_font(23)
    mono_font = load_font(21)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    blue = "#2F6BFF"
    green = "#24A06B"
    orange = "#F28C28"
    purple = "#7A5AF8"
    red = "#E84C61"

    def rounded(xy, fill="#FFFFFF", outline=line, radius=22, width=2):
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

    def shadow(xy, radius=22):
        x1, y1, x2, y2 = xy
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
        rounded(xy, radius=radius)

    draw.text((80, 58), "第2章数据类型实验回执", font=title_font, fill=ink)
    draw.text((84, 125), "同一份小数据，背后藏着 str、float、bool、list、dict 和 None。", font=body_font, fill=muted)
    draw.line((80, 178, 1520, 178), fill=line, width=3)

    shadow((80, 235, 760, 570))
    draw.text((125, 285), "学习记录", font=h_font, fill=ink)
    learning_rows = [
        ("name", STUDENT["name"], "str"),
        ("scores", str(STUDENT["scores"]), "list"),
        ("average", f"{sum(STUDENT['scores']) / len(STUDENT['scores']):.1f}", "float"),
        ("passed", str(sum(STUDENT["scores"]) / len(STUDENT["scores"]) >= 60), "bool"),
        ("next_review", str(STUDENT["next_review"]), "None"),
    ]
    y = 345
    for key, value, type_name in learning_rows:
        draw.text((130, y), key, font=mono_font, fill=blue)
        draw.text((335, y), value, font=body_font, fill=ink)
        draw.rounded_rectangle((615, y - 4, 715, y + 34), radius=19, fill="#EEF6FF")
        draw.text((640, y), type_name, font=body_font, fill=blue)
        y += 45

    shadow((840, 235, 1520, 570))
    draw.text((885, 285), "心理学 trial", font=h_font, fill=ink)
    trial_rows = [
        ("word", TRIAL["word"], "str"),
        ("ink_color", TRIAL["ink_color"], "str"),
        ("response", TRIAL["response_key"], "str"),
        ("correct", str(TRIAL["correct"]), "bool"),
        ("rt_ms", f"{TRIAL['reaction_time_ms']:.1f}", "float"),
    ]
    y = 345
    for key, value, type_name in trial_rows:
        draw.text((890, y), key, font=mono_font, fill=purple)
        draw.text((1110, y), value, font=body_font, fill=ink)
        draw.rounded_rectangle((1375, y - 4, 1475, y + 34), radius=19, fill="#F2EFFF")
        draw.text((1400, y), type_name, font=body_font, fill=purple)
        y += 45

    shadow((80, 640, 1520, 850))
    draw.text((125, 690), "类型选择结论", font=h_font, fill=ink)
    conclusions = [
        (blue, "str", "保存文字标签"),
        (green, "list", "保存一串分数"),
        (orange, "dict", "保存完整记录"),
        (purple, "float", "保存反应时"),
        (red, "bool", "保存判断结果"),
    ]
    x = 125
    for color, type_name, note in conclusions:
        draw.rounded_rectangle((x, 760, x + 245, 812), radius=26, fill=color)
        draw.text((x + 26, 771), type_name, font=body_font, fill="white")
        draw.text((x + 20, 822), note, font=body_font, fill=muted)
        x += 275

    draw.rounded_rectangle((280, 900, 1320, 960), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw.text((325, 916), "看到数据先问：它是文字、数字、判断、一串东西，还是一张查找表？", font=body_font, fill="#8A5A00")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_file, optimize=True, quality=95)
    return True


def main() -> None:
    reports_dir = Path("reports")
    output_dir = Path("output")
    reports_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    markdown_file = reports_dir / "ch02_data_type_lab_receipt.md"
    preview_file = output_dir / "ch02_data_type_lab_receipt.png"
    markdown_file.write_text(build_markdown(), encoding="utf-8")
    has_preview = write_preview_png(preview_file)

    print("数据类型实验回执已生成：")
    print("-", markdown_file)
    print("-", preview_file if has_preview else "未生成 PNG：当前环境缺少 Pillow")


if __name__ == "__main__":
    main()
