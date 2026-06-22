"""Chapter 02 artifact: make a Python data type compass."""

from __future__ import annotations

import shutil
from pathlib import Path
from textwrap import dedent


COMPASS_ITEMS = [
    {
        "label": "text",
        "type": "str",
        "question": "这是一段要展示、查找或切片的文字吗？",
        "example": "student_name = '小明'",
    },
    {
        "label": "sequence",
        "type": "list",
        "question": "这是一串有顺序、会逐个处理的数据吗？",
        "example": "scores = [86, 92, 78]",
    },
    {
        "label": "lookup",
        "type": "dict",
        "question": "这是不是一份需要按名字查找的信息表？",
        "example": "student = {'name': '小明'}",
    },
    {
        "label": "truth",
        "type": "bool",
        "question": "这是不是一个判断结果或开关状态？",
        "example": "passed = average >= 60",
    },
    {
        "label": "number",
        "type": "int / float",
        "question": "这是不是要参与计算的数量、分数或时间？",
        "example": "reaction_time = 523.7",
    },
    {
        "label": "missing",
        "type": "None",
        "question": "这里是不是暂时还没有值？",
        "example": "review_date = None",
    },
]


def project_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "manifest.json").exists() and (cwd / "assets" / "ch02").exists():
        return cwd
    return Path(__file__).resolve().parents[2]


def build_markdown() -> str:
    lines = [
        "# 第2章类型选择罗盘",
        "",
        "数据类型不是背诵题，而是一组选择题。看到一份新数据时，先别急着写代码，先问它要完成什么任务。",
        "",
        "| 判断线索 | 推荐类型 | 例子 |",
        "| --- | --- | --- |",
    ]
    for item in COMPASS_ITEMS:
        lines.append(f"| {item['question']} | `{item['type']}` | `{item['example']}` |")
    lines.extend(
        [
            "",
            "## 使用方法",
            "",
            "1. 如果数据要计算，先考虑 `int` 或 `float`。",
            "2. 如果数据是一段文字，先考虑 `str`。",
            "3. 如果数据是一串有顺序的材料，先考虑 `list`。",
            "4. 如果数据需要用名字、编号或标签查找，先考虑 `dict`。",
            "5. 如果数据只是一个判断，先考虑 `bool`。",
            "6. 如果数据暂时缺失，不要用 `0` 或空字符串假装有值，先考虑 `None`。",
            "",
            "类型选对以后，代码会少很多别扭的转换；类型选错以后，程序就会像把钥匙塞进耳机孔，努力但方向不对。",
            "",
        ]
    )
    return "\n".join(lines)


def make_preview(output_file: Path) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def load_font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()

    width, height = 1500, 900
    image = Image.new("RGB", (width, height), "#F7F9FC")
    draw = ImageDraw.Draw(image)
    title_font = load_font(58, True)
    small_font = load_font(26)
    type_font = load_font(34, True)
    label_font = load_font(24, True)

    colors = {
        "str": "#2F6BFF",
        "list": "#24A06B",
        "dict": "#F28C28",
        "bool": "#7A5AF8",
        "int / float": "#18A9B5",
        "None": "#E84C61",
    }

    draw.text((80, 58), "Type Compass", font=title_font, fill="#172033")
    draw.text((84, 132), "Choose by task, not by memory.", font=small_font, fill="#5D6678")

    center = (750, 470)
    positions = [
        ("str", "text", (330, 245)),
        ("list", "sequence", (750, 185)),
        ("dict", "lookup", (1170, 245)),
        ("bool", "truth", (1170, 650)),
        ("int / float", "number", (750, 715)),
        ("None", "missing", (330, 650)),
    ]

    for type_name, label, (x, y) in positions:
        color = colors[type_name]
        draw.line((center[0], center[1], x, y), fill="#B7C3D7", width=6)
        draw.rounded_rectangle((x - 170, y - 86, x + 170, y + 86), radius=24, fill="#FFFFFF", outline=color, width=5)
        draw.rounded_rectangle((x - 140, y - 66, x + 140, y - 25), radius=20, fill=color)
        draw.text((x - 52, y - 62), label, font=label_font, fill="white")
        bbox = draw.textbbox((0, 0), type_name, font=type_font)
        text_w = bbox[2] - bbox[0]
        draw.text((x - text_w // 2, y - 5), type_name, font=type_font, fill="#172033")

    draw.ellipse((center[0] - 120, center[1] - 120, center[0] + 120, center[1] + 120), fill="#111827")
    draw.text((center[0] - 76, center[1] - 43), "data", font=title_font, fill="white")

    draw.rounded_rectangle((270, 805, 1230, 865), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw.text((330, 820), "Ask what the data must do, then choose the container.", font=small_font, fill="#8A5A00")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_file, optimize=True, quality=95)
    return True


def main() -> None:
    root = project_root()
    reports_dir = root / "reports"
    output_dir = root / "output"
    web_dir = root / "assets" / "ch02" / "web"
    reports_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    web_dir.mkdir(parents=True, exist_ok=True)

    markdown_file = reports_dir / "ch02_type_compass.md"
    preview_file = output_dir / "ch02_type_compass_preview.png"
    web_preview_file = web_dir / "ch02_type_compass_preview.png"

    markdown_file.write_text(build_markdown(), encoding="utf-8")
    has_preview = make_preview(preview_file)
    if has_preview:
        shutil.copyfile(preview_file, web_preview_file)

    print(
        dedent(
            f"""
            类型选择罗盘已生成：
            - {markdown_file.relative_to(root)}
            - {preview_file.relative_to(root) if has_preview else '未生成 PNG：当前环境缺少 Pillow'}
            - {web_preview_file.relative_to(root) if has_preview else '未复制预览图'}
            """
        ).strip()
    )


if __name__ == "__main__":
    main()
