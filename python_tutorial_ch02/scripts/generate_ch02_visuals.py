from __future__ import annotations

import math
import re
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ModuleNotFoundError as exc:
    raise SystemExit(
        "This visual generator needs Pillow. Install it with: python -m pip install pillow"
    ) from exc


ROOT = Path.cwd()
if not (ROOT / "assets" / "ch02").exists():
    ROOT = Path(__file__).resolve().parents[1]

ASSET_DIR = ROOT / "assets" / "ch02"
WEB_DIR = ASSET_DIR / "web"

W, H = 1800, 1120
BG = "#F6F8FB"
PAPER = "#FFFFFF"
PANEL = "#EEF3F8"
LINE = "#D8E2EE"
INK = "#182235"
MUTED = "#687386"
BLUE = "#356DFF"
GREEN = "#25A06A"
ORANGE = "#F28B2E"
PURPLE = "#7A5AF8"
RED = "#E64B63"
TEAL = "#18A7A8"
YELLOW = "#D99A00"
GRAY = "#9AA6B6"


def canvas(width: int = W, height: int = H):
    im = Image.new("RGB", (width, height), BG)
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, name: str):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    im.save(ASSET_DIR / name, optimize=True, quality=95)


def font(size: int, *, bold: bool = False, mono: bool = False):
    candidates: list[Path] = []
    if mono:
        candidates.extend(
            [
                Path("C:/Windows/Fonts/consola.ttf"),
                Path("C:/Windows/Fonts/CascadiaMono.ttf"),
            ]
        )
    if bold:
        candidates.extend(
            [
                Path("C:/Windows/Fonts/msyhbd.ttc"),
                Path("C:/Windows/Fonts/simhei.ttf"),
            ]
        )
    candidates.extend(
        [
            Path("C:/Windows/Fonts/msyh.ttc"),
            Path("C:/Windows/Fonts/simsun.ttc"),
            Path("C:/Windows/Fonts/arial.ttf"),
        ]
    )
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def text_size(d: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    if not text:
        return 0, 0
    box = d.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def tokens(line: str) -> list[str]:
    return re.findall(
        r"[A-Za-z0-9_./:\\#%+\-=<>]+|[\u4e00-\u9fff]|[^\sA-Za-z0-9_./:\\#%+\-=<>\u4e00-\u9fff]|\s+",
        line,
    )


def wrap_line(d: ImageDraw.ImageDraw, line: str, fnt, max_width: int) -> list[str]:
    parts = tokens(line)
    lines: list[str] = []
    current = ""
    for part in parts:
        if part.isspace():
            part = " "
        candidate = (current + part).strip() if not current else current + part
        if not candidate.strip():
            continue
        if text_size(d, candidate, fnt)[0] <= max_width:
            current = candidate
            continue
        if current.strip():
            lines.append(current.strip())
            current = part.strip()
        else:
            piece = ""
            for ch in part:
                if text_size(d, piece + ch, fnt)[0] <= max_width:
                    piece += ch
                else:
                    if piece:
                        lines.append(piece)
                    piece = ch
            current = piece
    if current.strip():
        lines.append(current.strip())
    return lines


def wrap_text(d: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
        else:
            lines.extend(wrap_line(d, paragraph, fnt, max_width))
    return lines


def truncate_line(d: ImageDraw.ImageDraw, line: str, fnt, max_width: int) -> str:
    if text_size(d, line, fnt)[0] <= max_width:
        return line
    line = line.rstrip()
    while line and text_size(d, line + "...", fnt)[0] > max_width:
        line = line[:-1]
    return (line.rstrip() + "...") if line else "..."


def text_box(
    d: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    size: int,
    *,
    fill: str = INK,
    bold: bool = False,
    mono: bool = False,
    max_lines: int | None = None,
    line_gap: int = 9,
    align: str = "left",
    valign: str = "top",
):
    x0, y0, x1, y1 = box
    max_width = max(10, x1 - x0)
    max_height = max(10, y1 - y0)
    chosen_size = size
    chosen_font = font(chosen_size, bold=bold, mono=mono)
    lines = wrap_text(d, text, chosen_font, max_width)

    while chosen_size > 13:
        line_height = chosen_size + line_gap
        limited = lines[: max_lines or len(lines)]
        total_height = len(limited) * line_height - line_gap
        if total_height <= max_height and (max_lines is None or len(lines) <= max_lines):
            break
        chosen_size -= 2
        chosen_font = font(chosen_size, bold=bold, mono=mono)
        lines = wrap_text(d, text, chosen_font, max_width)

    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = truncate_line(d, lines[-1], chosen_font, max_width)

    line_height = chosen_size + line_gap
    max_fit = max(1, (max_height + line_gap) // line_height)
    if len(lines) > max_fit:
        lines = lines[:max_fit]
        lines[-1] = truncate_line(d, lines[-1], chosen_font, max_width)

    total_height = len(lines) * line_height - line_gap
    if valign == "middle":
        y = y0 + max(0, (max_height - total_height) // 2)
    elif valign == "bottom":
        y = y1 - total_height
    else:
        y = y0

    for line in lines:
        w, _ = text_size(d, line, chosen_font)
        if align == "center":
            x = x0 + (max_width - w) // 2
        elif align == "right":
            x = x1 - w
        else:
            x = x0
        d.text((x, y), line, fill=fill, font=chosen_font)
        y += line_height


def shadow_box(
    d: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    fill: str = PAPER,
    outline: str = LINE,
    radius: int = 26,
    shadow: str = "#E5EBF3",
    width: int = 2,
):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + 10, y0 + 12, x1 + 10, y1 + 12), radius=radius, fill=shadow)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def title_block(d: ImageDraw.ImageDraw, title: str, subtitle: str | None = None):
    text_box(d, (90, 62, 1710, 128), title, 52, bold=True, max_lines=1)
    if subtitle:
        text_box(d, (92, 135, 1710, 184), subtitle, 28, fill=MUTED, max_lines=1)
    d.line((90, 198, 1710, 198), fill=LINE, width=2)


def arrow(
    d: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    *,
    fill: str = GRAY,
    width: int = 5,
):
    d.line((*start, *end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 18
    p1 = (
        end[0] - size * math.cos(angle - math.pi / 6),
        end[1] - size * math.sin(angle - math.pi / 6),
    )
    p2 = (
        end[0] - size * math.cos(angle + math.pi / 6),
        end[1] - size * math.sin(angle + math.pi / 6),
    )
    d.polygon([end, p1, p2], fill=fill)


def pill(
    d: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    *,
    fill: str,
    ink: str = PAPER,
    size: int = 24,
):
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill)
    text_box(d, (box[0] + 18, box[1] + 4, box[2] - 18, box[3] - 3), text, size, fill=ink, bold=True, align="center", valign="middle")


def card(
    d: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    *,
    accent: str = BLUE,
    tag: str | None = None,
):
    shadow_box(d, box, radius=24)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0, y0, x1, y0 + 16), radius=24, fill=accent)
    d.rectangle((x0, y0 + 8, x1, y0 + 16), fill=accent)
    if tag:
        pill(d, (x0 + 24, y0 + 30, x0 + 132, y0 + 70), tag, fill=accent, size=20)
        title_left = x0 + 150
    else:
        title_left = x0 + 26
    text_box(d, (title_left, y0 + 28, x1 - 24, y0 + 78), title, 30, bold=True, max_lines=1)
    text_box(d, (x0 + 26, y0 + 92, x1 - 26, y1 - 26), body, 24, fill=MUTED, max_lines=4)


def mini_badge(d: ImageDraw.ImageDraw, center: tuple[int, int], text: str, color: str):
    x, y = center
    d.ellipse((x - 34, y - 34, x + 34, y + 34), fill="#EEF3FF", outline=color, width=4)
    text_box(d, (x - 50, y - 19, x + 50, y + 19), text, 20, fill=color, bold=True, align="center", valign="middle", max_lines=1)


def cover():
    im, d = canvas()
    title_block(d, "第2章 数据类型", "不是背名词，而是学会判断：这份数据应该用什么形状保存？")
    shadow_box(d, (120, 250, 1680, 440), fill="#FCFDFE", radius=30)
    text_box(d, (170, 282, 690, 348), "先看材料", 42, bold=True, align="center", max_lines=1)
    text_box(d, (1110, 282, 1630, 348), "再选类型", 42, bold=True, align="center", max_lines=1)
    arrow(d, (720, 346), (1080, 346), fill=BLUE, width=7)
    text_box(d, (520, 372, 1280, 420), "姓名、分数、反应时、是否正确、一次完整记录", 25, fill=MUTED, align="center", max_lines=1)

    items = [
        ("bool", "判断题", "只有真或假：是否通过、是否匹配、开关是否打开。", BLUE),
        ("number", "可计算的量", "分数、次数、反应时；需要加减乘除或比较大小。", ORANGE),
        ("str", "原样保存的文字", "姓名、刺激词、路径片段；重点是展示和匹配。", PURPLE),
        ("list", "按顺序排队", "一串分数、多次 trial；关心第几个和整体顺序。", TEAL),
        ("dict", "用 key 查 value", "学生记录、一次实验 trial；字段名要稳定清楚。", GREEN),
        ("None", "暂时没有", "还没提交、暂无备注；它不是 0，也不是空字符串。", RED),
    ]
    x0, y0 = 120, 520
    for i, (tag, title, body, color) in enumerate(items):
        row, col = divmod(i, 3)
        x = x0 + col * 520
        y = y0 + row * 245
        card(d, (x, y, x + 460, y + 185), title, body, accent=color, tag=tag)
    save(im, "ch02_cover.png")


def roadmap():
    im, d = canvas()
    title_block(d, "第2章结构图", "目录按学习任务分区：从“认识材料”走到“能整理一份记录”。")
    steps = [
        ("导读", "本章路线", "先建立判断问题：看到数据，先问它是什么形状。", BLUE),
        ("第一部分", "变量与类型地图", "常量、关键字、变量名，以及数据类型的总览。", GREEN),
        ("第二部分", "基础类型", "bool、数值和字符串：判断、计算、保存文字。", ORANGE),
        ("第三部分", "容器类型", "list 与 dict：一串数据和一条完整记录。", PURPLE),
        ("第四部分", "项目与复盘", "用学习记录、Stroop 数据包和报错地图串起来。", TEAL),
        ("第五部分", "走向文件", "把类型整理好的结构，交给下一章的文件系统。", RED),
    ]
    y = 300
    w = 245
    gap = 35
    for i, (tag, title, body, color) in enumerate(steps):
        x = 80 + i * (w + gap)
        card(d, (x, y, x + w, y + 300), title, body, accent=color, tag=tag)
        if i < len(steps) - 1:
            arrow(d, (x + w + 6, y + 150), (x + w + gap - 8, y + 150), fill=GRAY, width=4)
    shadow_box(d, (210, 760, 1590, 930), fill="#FCFDFE", radius=24)
    text_box(
        d,
        (260, 800, 1540, 895),
        "读这一章时，不必把每个方法都背成清单。更重要的是：你能说清楚一份数据为什么适合某种类型。",
        31,
        fill=INK,
        align="center",
        valign="middle",
        max_lines=2,
    )
    save(im, "ch02_roadmap.png")


def variable_label_metaphor():
    im, d = canvas()
    title_block(d, "变量像标签，不像盒子", "名字贴到对象上；重新赋值时，是标签移动，不是把旧对象倒进新盒子。")
    left = (120, 260, 850, 930)
    right = (950, 260, 1680, 930)
    shadow_box(d, left, radius=30)
    shadow_box(d, right, radius=30)
    text_box(d, (165, 300, 805, 350), "1. a = 2；b = a", 34, bold=True, max_lines=1)
    d.ellipse((430, 455, 540, 565), fill="#FFF6E8", outline=ORANGE, width=5)
    text_box(d, (430, 485, 540, 535), "2", 42, fill=ORANGE, bold=True, align="center", valign="middle", max_lines=1)
    for label, y in [("a", 415), ("b", 620)]:
        d.rounded_rectangle((210, y, 310, y + 64), radius=16, fill="#EFF4FF", outline=BLUE, width=3)
        text_box(d, (210, y + 10, 310, y + 52), label, 34, fill=BLUE, bold=True, align="center", valign="middle", max_lines=1)
        arrow(d, (310, y + 32), (430, 510), fill=BLUE, width=4)
    text_box(d, (165, 720, 805, 840), "两个名字同时指向整数对象 2。先别急着想“复制盒子”，先看箭头指向哪里。", 28, fill=MUTED, max_lines=3)

    text_box(d, (995, 300, 1635, 350), "2. a = \"hi\"", 34, bold=True, max_lines=1)
    d.ellipse((1110, 455, 1220, 565), fill="#FFF6E8", outline=ORANGE, width=5)
    text_box(d, (1110, 485, 1220, 535), "2", 42, fill=ORANGE, bold=True, align="center", valign="middle", max_lines=1)
    d.rounded_rectangle((1425, 455, 1555, 565), radius=22, fill="#F0FBF8", outline=GREEN, width=5)
    text_box(d, (1425, 485, 1555, 535), "\"hi\"", 36, fill=GREEN, bold=True, align="center", valign="middle", max_lines=1)
    d.rounded_rectangle((1040, 610, 1140, 674), radius=16, fill="#EFF4FF", outline=BLUE, width=3)
    text_box(d, (1040, 620, 1140, 662), "b", 34, fill=BLUE, bold=True, align="center", valign="middle", max_lines=1)
    arrow(d, (1140, 642), (1110, 530), fill=BLUE, width=4)
    d.rounded_rectangle((1320, 610, 1420, 674), radius=16, fill="#EFF4FF", outline=BLUE, width=3)
    text_box(d, (1320, 620, 1420, 662), "a", 34, fill=BLUE, bold=True, align="center", valign="middle", max_lines=1)
    arrow(d, (1420, 642), (1455, 555), fill=BLUE, width=4)
    text_box(d, (995, 720, 1635, 840), "重新赋值只让 a 这张标签移到新对象上；b 仍然贴在原来的 2 上。", 28, fill=MUTED, max_lines=3)
    save(im, "ch02_variable_label_metaphor.png")


def data_type_atlas():
    im, d = canvas()
    title_block(d, "数据类型地图", "一张速查图：先看数据想表达什么，再决定把它放进哪种结构。")
    items = [
        ("bool", "判断是否成立", "是否通过、是否一致、是否完成。", BLUE),
        ("int / float", "保存可计算的量", "分数、次数、反应时、比例。", ORANGE),
        ("str", "保存文字标签", "姓名、刺激词、路径、备注。", PURPLE),
        ("list", "保存有顺序的一串", "多次分数、多条 trial、步骤队列。", TEAL),
        ("tuple", "固定组合", "坐标、不可随意改动的小组值。", YELLOW),
        ("dict", "保存一条记录", "用字段名直接找到对应信息。", GREEN),
        ("None", "表示暂时没有", "缺失备注、还没产生的结果。", RED),
        ("type()", "先确认再操作", "不确定时先看类型，再选方法。", GRAY),
    ]
    for i, (tag, title, body, color) in enumerate(items):
        row, col = divmod(i, 4)
        x = 95 + col * 420
        y = 270 + row * 320
        card(d, (x, y, x + 360, y + 235), title, body, accent=color, tag=tag)
    save(im, "ch02_data_type_atlas.png")


def bool_logic_switchboard():
    im, d = canvas()
    title_block(d, "布尔逻辑：把条件说清楚", "`and`、`or`、`not` 不是口号，它们分别回答三种不同的问题。")
    panels = [
        ("and", "两件事都成立", "分数 >= 60 并且 已提交。只要缺一项，结果就是 False。", GREEN, [(True, True), (True, False)]),
        ("or", "至少有一件事成立", "完成练习 或 通过测验。只要有一个 True，就能继续。", TEAL, [(True, False), (False, False)]),
        ("not", "把判断反过来", "not submitted 表示“还没提交”。它常用来写提醒。", RED, [(False, True)]),
    ]
    for i, (op, title, body, color, states) in enumerate(panels):
        x = 115 + i * 560
        y = 275
        shadow_box(d, (x, y, x + 480, y + 585), radius=28)
        pill(d, (x + 40, y + 42, x + 155, y + 90), op, fill=color, size=24)
        text_box(d, (x + 180, y + 42, x + 440, y + 92), title, 32, bold=True, max_lines=1)
        text_box(d, (x + 42, y + 118, x + 438, y + 220), body, 25, fill=MUTED, max_lines=3)
        for j, state in enumerate(states):
            sy = y + 285 + j * 135
            if len(state) == 2 and op != "not":
                labels = ["条件 A", "条件 B"]
                for k, value in enumerate(state):
                    cx = x + 120 + k * 150
                    d.ellipse((cx - 28, sy - 28, cx + 28, sy + 28), fill=GREEN if value else "#CBD5E1")
                    text_box(d, (cx - 70, sy + 38, cx + 70, sy + 75), labels[k], 18, fill=MUTED, align="center", max_lines=1)
                arrow(d, (x + 320, sy), (x + 390, sy), fill=color, width=4)
                result = (state[0] and state[1]) if op == "and" else (state[0] or state[1])
            else:
                cx = x + 170
                value = state[0]
                d.ellipse((cx - 30, sy - 30, cx + 30, sy + 30), fill=GREEN if value else "#CBD5E1")
                arrow(d, (cx + 50, sy), (x + 365, sy), fill=color, width=4)
                result = not value
            d.rounded_rectangle((x + 365, sy - 32, x + 445, sy + 32), radius=16, fill="#F7FAFC", outline=color, width=3)
            text_box(d, (x + 365, sy - 20, x + 445, sy + 22), str(result), 20, fill=color, bold=True, align="center", valign="middle", max_lines=1)
    save(im, "ch02_bool_logic_switchboard.png")


def number_rounding_chart():
    im, d = canvas()
    title_block(d, "取整不是一件事", "`round`、`floor`、`ceil` 看起来都在变整数，但它们回答的问题不同。")
    chart = (130, 270, 1120, 860)
    shadow_box(d, chart, radius=28)
    x0, y0, x1, y1 = chart
    plot = (x0 + 90, y0 + 70, x1 - 70, y1 - 90)
    px0, py0, px1, py1 = plot
    d.line((px0, py1, px1, py1), fill=LINE, width=3)
    d.line((px0, py0, px0, py1), fill=LINE, width=3)
    for i in range(-2, 6):
        x = px0 + (i + 2) / 7 * (px1 - px0)
        d.line((x, py0, x, py1), fill="#EEF2F7", width=1)
        text_box(d, (int(x) - 35, py1 + 18, int(x) + 35, py1 + 52), str(i), 18, fill=MUTED, align="center", max_lines=1)
    for j in range(-2, 7):
        y = py1 - (j + 2) / 8 * (py1 - py0)
        d.line((px0, y, px1, y), fill="#EEF2F7", width=1)
        text_box(d, (px0 - 56, int(y) - 12, px0 - 12, int(y) + 12), str(j), 18, fill=MUTED, align="right", max_lines=1)

    def map_point(x: float, y: float) -> tuple[int, int]:
        return (
            int(px0 + (x + 2) / 7 * (px1 - px0)),
            int(py1 - (y + 2) / 8 * (py1 - py0)),
        )

    series = [
        ("floor", BLUE, math.floor),
        ("round", GREEN, round),
        ("ceil", ORANGE, math.ceil),
    ]
    for name, color, func in series:
        points = [map_point(v / 10, func(v / 10)) for v in range(-20, 51)]
        d.line(points, fill=color, width=5)
    for i, (name, color, _) in enumerate(series):
        y = y0 + 72 + i * 50
        d.line((x1 - 260, y, x1 - 210, y), fill=color, width=6)
        text_box(d, (x1 - 195, y - 17, x1 - 80, y + 18), name, 20, fill=INK, max_lines=1)

    notes = [
        ("floor", "向下找整数", "适合“不能超过”的场景。", BLUE),
        ("ceil", "向上补到整数", "适合“至少需要几个”的场景。", ORANGE),
        ("round", "按规则四舍五入", "展示结果可以用，边界值要小心。", GREEN),
    ]
    for i, (tag, title, body, color) in enumerate(notes):
        card(d, (1210, 270 + i * 205, 1680, 430 + i * 205), title, body, accent=color, tag=tag)
    save(im, "ch02_number_rounding_chart.png")


def string_material_workbench():
    im, d = canvas()
    title_block(d, "字符串工作台", "字符串不是“随便一段字”，它常常负责保存标签、路径、刺激词和备注。")
    shadow_box(d, (105, 255, 1695, 485), fill="#FCFDFE", radius=28)
    samples = [
        ("student_name", "\"小明\"", BLUE),
        ("trial_code", "\"stroop_red_001\"", GREEN),
        ("raw_note", "\"  need review  \"", ORANGE),
    ]
    for i, (name, value, color) in enumerate(samples):
        x = 175 + i * 500
        d.rounded_rectangle((x, 325, x + 420, 408), radius=18, fill="#F7FAFC", outline=color, width=3)
        text_box(d, (x + 18, 337, x + 180, 380), name, 22, fill=color, bold=True, max_lines=1)
        text_box(d, (x + 185, 337, x + 405, 380), value, 22, fill=INK, max_lines=1)

    tools = [
        (".strip()", "清掉两端空格", "把输入先收拾干净，再进入后面的判断。", BLUE),
        (".lower()", "统一大小写", "同一个标签不要因为大小写变成两个值。", GREEN),
        ("f-string", "拼出可读报告", "把数值、判断结果和文字放进一句话。", PURPLE),
        (".split()", "按分隔符拆开", "路径、编号和 CSV 行经常需要拆成字段。", ORANGE),
    ]
    for i, (tag, title, body, color) in enumerate(tools):
        x = 105 + i * 405
        y = 615
        arrow(d, (315 + i * 380, 488), (x + 195, y - 25), fill="#B6C2D2", width=4)
        card(d, (x, y, x + 350, y + 235), title, body, accent=color, tag=tag)
    save(im, "ch02_string_material_workbench.png")


def string_slice_ruler():
    im, d = canvas()
    title_block(d, "字符串切片：左闭右开", "起点包含，终点不包含。记住这个规则，索引就不再像猜谜。")
    word = "psychology"
    x0, y0 = 210, 410
    cell = 135
    for i, ch in enumerate(word):
        x = x0 + i * cell
        fill = "#EFF5FF" if 0 <= i < 5 else PAPER
        outline = BLUE if 0 <= i < 5 else LINE
        d.rounded_rectangle((x, y0, x + 100, y0 + 100), radius=18, fill=fill, outline=outline, width=4)
        text_box(d, (x, y0 + 22, x + 100, y0 + 78), ch, 42, fill=INK, bold=True, align="center", valign="middle", max_lines=1)
        text_box(d, (x, y0 - 58, x + 100, y0 - 24), str(i), 24, fill=MUTED, align="center", max_lines=1)
        text_box(d, (x, y0 + 118, x + 100, y0 + 152), str(i - len(word)), 22, fill=MUTED, align="center", max_lines=1)

    start_x = x0
    stop_x = x0 + 5 * cell - 35
    d.line((start_x + 50, y0 + 205, stop_x, y0 + 205), fill=GREEN, width=8)
    arrow(d, (start_x + 50, y0 + 205), (stop_x, y0 + 205), fill=GREEN, width=6)
    text_box(d, (start_x, y0 + 238, stop_x + 70, y0 + 292), 'word[0:5]  ->  "psych"', 30, fill=GREEN, bold=True, align="center", max_lines=1)
    shadow_box(d, (230, 795, 1570, 935), fill="#FCFDFE", radius=24)
    text_box(d, (280, 825, 1520, 900), "切片里的 5 是停下的位置，不会取到索引 5 对应的字母 o。", 31, fill=INK, align="center", valign="middle", max_lines=2)
    save(im, "ch02_string_slice_ruler.png")


def list_workbench():
    im, d = canvas()
    title_block(d, "列表：一排有顺序的抽屉", "列表适合保存一串同类材料；顺序、长度和索引都很重要。")
    values = [86, 92, 78, 88]
    x0, y0, cell = 310, 325, 230
    for i, value in enumerate(values):
        x = x0 + i * cell
        d.rounded_rectangle((x, y0, x + 170, y0 + 130), radius=22, fill=PAPER, outline=BLUE if i < 3 else GREEN, width=4)
        text_box(d, (x, y0 + 34, x + 170, y0 + 86), str(value), 42, fill=INK, bold=True, align="center", valign="middle", max_lines=1)
        text_box(d, (x, y0 - 50, x + 170, y0 - 16), f"index {i}", 20, fill=MUTED, align="center", max_lines=1)
    pill(d, (1125, 355, 1355, 420), "append(88)", fill=GREEN, size=25)
    arrow(d, (1070, 390), (1120, 390), fill=GREEN, width=5)
    ops = [
        ("读取", "scores[0]", "取第一个分数。", BLUE),
        ("添加", "append()", "把新值放到末尾。", GREEN),
        ("删除", "del scores[1]", "按位置删掉一个元素。", RED),
        ("统计", "sum(scores) / len(scores)", "列表可以继续交给计算。", ORANGE),
    ]
    for i, (title, code, body, color) in enumerate(ops):
        x = 120 + i * 420
        card(d, (x, 650, x + 360, 860), title, f"{code}\n{body}", accent=color)
    save(im, "ch02_list_workbench.png")


def dict_mapping_card():
    im, d = canvas()
    title_block(d, "字典：用 key 找 value", "字典不是一堆散点，它是一张有字段名的记录卡。")
    shadow_box(d, (150, 260, 1650, 900), fill="#FCFDFE", radius=30)
    text_box(d, (210, 310, 650, 365), "student = { ... }", 36, bold=True, max_lines=1)
    pairs = [
        ("name", "\"小明\"", BLUE),
        ("scores", "[86, 92, 78]", GREEN),
        ("passed", "True", ORANGE),
        ("note", "None", PURPLE),
    ]
    for i, (key, value, color) in enumerate(pairs):
        y = 430 + i * 105
        d.rounded_rectangle((245, y, 535, y + 70), radius=18, fill=PAPER, outline=color, width=3)
        d.rounded_rectangle((1040, y, 1425, y + 70), radius=18, fill=PAPER, outline=color, width=3)
        text_box(d, (265, y + 14, 515, y + 54), key, 26, fill=color, bold=True, align="center", valign="middle", max_lines=1)
        text_box(d, (1060, y + 14, 1405, y + 54), value, 26, fill=INK, align="center", valign="middle", max_lines=1)
        arrow(d, (540, y + 35), (1030, y + 35), fill=color, width=4)
    text_box(d, (610, 735, 990, 805), 'student["scores"]', 30, fill=GREEN, bold=True, align="center", max_lines=1)
    text_box(d, (575, 805, 1025, 850), "看到 key，直接找到对应 value。", 24, fill=MUTED, align="center", max_lines=1)
    save(im, "ch02_dict_mapping_card.png")


def mini_project_dashboard():
    im, d = canvas()
    title_block(d, "本章小项目：学习记录整理器", "数据类型第一次合在一起做事：输入、整理、判断、输出。")
    steps = [
        ("输入材料", "姓名、分数、技能、备注", BLUE),
        ("列表", "scores = [86, 92, 78]", GREEN),
        ("字典", "student = {name, scores, skills}", PURPLE),
        ("报告", "平均分、是否通过、下一步建议", ORANGE),
    ]
    for i, (title, body, color) in enumerate(steps):
        x = 120 + i * 415
        card(d, (x, 330, x + 340, 575), title, body, accent=color)
        if i < len(steps) - 1:
            arrow(d, (x + 350, 450), (x + 405, 450), fill=GRAY, width=4)
    shadow_box(d, (220, 740, 1580, 900), fill="#FCFDFE", radius=24)
    text_box(
        d,
        (270, 775, 1530, 865),
        "小项目的价值不在“代码很长”，而在把零散值整理成能解释、能检查、能继续保存的结构。",
        31,
        align="center",
        valign="middle",
        max_lines=2,
    )
    save(im, "ch02_mini_project_dashboard.png")


def error_clue_cards():
    im, d = canvas()
    title_block(d, "报错线索卡", "先缩小范围，再改代码。第2章的报错大多能从类型、名字、索引和 key 找到线索。")
    items = [
        ("NameError", "名字没定义", "查拼写；看赋值语句是不是在前面。", BLUE),
        ("TypeError", "类型不合适", "先 print(type(x))，再决定能不能相加、切片或查询。", RED),
        ("ValueError", "值不能转换", '例如 int("abc")；先检查内容，再转换。', ORANGE),
        ("IndexError", "位置越界", "用 len() 看长度；最后一个索引是 len(x)-1。", PURPLE),
        ("KeyError", "key 不存在", "先用 in 判断，或用 get() 给默认值。", GREEN),
        ("SyntaxError", "语法没写完整", "重点看冒号、括号、引号，以及报错定位行。", TEAL),
    ]
    for i, (tag, title, body, color) in enumerate(items):
        row, col = divmod(i, 3)
        x = 115 + col * 560
        y = 285 + row * 310
        card(d, (x, y, x + 480, y + 235), title, body, accent=color, tag=tag)
    save(im, "ch02_error_clue_cards.png")


def practice_workbench():
    im, d = canvas()
    title_block(d, "本章练习工作台", "练习的顺序不是随机刷题，而是从命名、操作到生成记录。")
    items = [
        ("1", "变量命名", "把 a、b、c 改成看得懂的名字。", BLUE),
        ("2", "字符串切片", "用索引取字符和片段。", GREEN),
        ("3", "列表操作", "添加、删除、平均分。", ORANGE),
        ("4", "字典操作", "新增字段、修改值、get 默认值。", PURPLE),
        ("5", "类型罗盘", "为真实数据选择类型并写理由。", TEAL),
        ("6", "Stroop 数据包", "改 trial，观察正确率和缺失值。", RED),
        ("7", "运行记录", "检查报告是否 14/14 ready。", YELLOW),
    ]
    for i, (num, title, body, color) in enumerate(items):
        row = 0 if i < 4 else 1
        col = i if i < 4 else i - 4
        x = 100 + col * 420 + (0 if row == 0 else 210)
        y = 280 + row * 305
        card(d, (x, y, x + 355, y + 230), title, body, accent=color, tag=num)
    shadow_box(d, (300, 915, 1500, 1015), fill="#FCFDFE", radius=24)
    text_box(d, (340, 938, 1460, 990), "推荐节奏：改一点，跑一次，看输出；最后留下可复查的文件记录。", 29, fill=INK, align="center", valign="middle", max_lines=1)
    save(im, "ch02_practice_workbench.png")


def type_to_file_bridge():
    im, d = canvas()
    title_block(d, "从数据类型走向文件", "第2章把材料整理成结构；第3章会把结构保存到路径和文件里。")
    left_tags = [
        ("str", "姓名 / 刺激词", BLUE),
        ("list", "多次分数 / 多条 trial", GREEN),
        ("dict", "一条完整记录", PURPLE),
        ("bool", "是否正确 / 是否通过", ORANGE),
        ("None", "暂时没有备注", RED),
    ]
    for i, (tag, body, color) in enumerate(left_tags):
        y = 280 + i * 115
        pill(d, (120, y, 245, y + 58), tag, fill=color, size=24)
        text_box(d, (270, y + 8, 575, y + 50), body, 25, fill=INK, max_lines=1)
    arrow(d, (610, 560), (760, 560), fill=GRAY, width=6)
    shadow_box(d, (790, 330, 1120, 790), fill="#FCFDFE", radius=28)
    text_box(d, (825, 375, 1085, 425), "结构化记录", 34, bold=True, align="center", max_lines=1)
    text_box(
        d,
        (835, 470, 1075, 700),
        '{\n  "name": "小明",\n  "scores": [86, 92, 78],\n  "passed": True,\n  "note": None\n}',
        24,
        fill=INK,
        max_lines=7,
    )
    arrow(d, (1145, 560), (1295, 560), fill=GRAY, width=6)
    files = [("JSON", "保存结构", BLUE), ("CSV", "保存表格", GREEN), ("TXT / MD", "保存报告", ORANGE)]
    for i, (title, body, color) in enumerate(files):
        y = 325 + i * 160
        card(d, (1325, y, 1665, y + 118), title, body, accent=color)
    shadow_box(d, (455, 910, 1345, 1010), fill="#FCFDFE", radius=24)
    text_box(d, (495, 933, 1305, 986), "下一章关注的问题会变成：这些结构应该放在哪个文件里？路径怎么写才可靠？", 28, align="center", valign="middle", max_lines=1)
    save(im, "ch02_type_to_file_bridge.png")


def photo_plate(output_name: str, image_name: str, title: str, caption: str):
    im, d = canvas(1800, 1180)
    title_block(d, title, caption)
    frame = (140, 250, 1660, 860)
    shadow_box(d, (110, 220, 1690, 900), fill=PAPER, radius=32)
    d.rounded_rectangle(frame, radius=24, fill=PANEL, outline=LINE, width=2)

    src = WEB_DIR / image_name
    if src.exists():
        raw = Image.open(src)
        raw = ImageOps.exif_transpose(raw).convert("RGB")
        resampling = getattr(Image, "Resampling", Image).LANCZOS
        shown = ImageOps.contain(raw, (frame[2] - frame[0] - 36, frame[3] - frame[1] - 36), method=resampling)
        x = frame[0] + (frame[2] - frame[0] - shown.width) // 2
        y = frame[1] + (frame[3] - frame[1] - shown.height) // 2
        im.paste(shown, (x, y))
    else:
        d.line((780, 470, 1020, 650), fill=RED, width=12)
        d.line((1020, 470, 780, 650), fill=RED, width=12)
        text_box(d, (500, 700, 1300, 750), f"缺少图片：{image_name}", 28, fill=RED, align="center", max_lines=1)

    shadow_box(d, (180, 940, 1620, 1085), fill="#FCFDFE", radius=24)
    text_box(d, (230, 975, 1570, 1048), caption, 30, fill=INK, align="center", valign="middle", max_lines=2)
    save(im, output_name)


def copy_output_preview(source_name: str):
    src = ROOT / "output" / source_name
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / source_name, optimize=True, quality=95)


def information_history_claude_shannon():
    photo_plate(
        "ch02_information_history_claude_shannon.png",
        "claude_shannon_mfo3807.jpg",
        "信息论的提醒",
        "信息可以被编码、传输和校验；数据类型做的是更小尺度的整理。",
    )


def history_george_boole():
    photo_plate(
        "ch02_history_george_boole.png",
        "george_boole_color.jpg",
        "布尔判断的来源",
        "布尔值只保留 True 和 False，适合回答能被明确判断的问题。",
    )


def psychology_ebbinghaus_memory():
    photo_plate(
        "ch02_psychology_ebbinghaus_memory.png",
        "hermann_ebbinghaus2.jpg",
        "实验记录里的类型",
        "记忆实验背后也需要文字标签、数值测量、时间记录和判断结果。",
    )


def dictionary_card_catalog_photo():
    photo_plate(
        "ch02_dictionary_card_catalog_photo.png",
        "copyright_card_catalog_drawer.jpg",
        "字典像一张可查的卡片",
        "key 的价值在于直接定位 value，而不是从头翻完整个列表。",
    )


def punch_card_sorter_photo():
    photo_plate(
        "ch02_punch_card_sorter_photo.png",
        "ibm_080_card_sorter.jpg",
        "从排序机器到列表操作",
        "列表关心顺序、位置和批量处理；这和早期数据整理工具的思路是相通的。",
    )


def nested_data_matryoshka():
    photo_plate(
        "ch02_nested_data_matryoshka.png",
        "matryoshka_dolls.jpg",
        "嵌套结构：里面还能继续放结构",
        "列表里可以放列表，字典里也可以放列表；关键是每一层都要有清楚的角色。",
    )


def data_type_lab_receipt():
    copy_output_preview("ch02_data_type_lab_receipt.png")
    photo_plate(
        "ch02_data_type_lab_receipt.png",
        "ch02_data_type_lab_receipt.png",
        "数据类型实验记录",
        "同一份记录里，字符串、列表、字典、浮点数、布尔值和 None 各自承担不同任务。",
    )


def stroop_dataset_pack():
    copy_output_preview("ch02_stroop_dataset_pack.png")
    photo_plate(
        "ch02_stroop_dataset_pack.png",
        "ch02_stroop_dataset_pack.png",
        "Stroop 数据包",
        "多条 trial 用 list 排队；每条 trial 用 dict 保存字段，便于后续统计和导出。",
    )


def data_type_specimen_cabinet():
    copy_output_preview("ch02_data_type_specimen_cabinet.png")
    photo_plate(
        "ch02_data_type_specimen_cabinet.png",
        "ch02_data_type_specimen_cabinet.png",
        "数据类型标本柜",
        "把一条记录拆开看，能更清楚地发现每种类型在任务里的位置。",
    )


def data_type_runtime_evidence():
    copy_output_preview("ch02_data_type_runtime_evidence.png")
    photo_plate(
        "ch02_data_type_runtime_evidence.png",
        "ch02_data_type_runtime_evidence.png",
        "运行记录板",
        "学习结果不只停在文字说明里；脚本、报告和输出文件都应该能被复查。",
    )


def powershell_data_type_run():
    photo_plate(
        "ch02_powershell_data_type_run.png",
        "powershell_ch02_data_types_run.png",
        "PowerShell 运行截图",
        "截图用于证明脚本确实跑过；概念图负责解释，运行图负责留证。",
    )


def type_decision_cards_preview():
    copy_output_preview("ch02_type_decision_cards_preview.png")
    photo_plate(
        "ch02_type_decision_cards_preview.png",
        "ch02_type_decision_cards_preview.png",
        "类型选择卡片",
        "把“选类型”拆成几个判断问题，帮助你从背概念转向做设计。",
    )


def type_compass_preview():
    copy_output_preview("ch02_type_compass_preview.png")
    photo_plate(
        "ch02_type_compass_preview.png",
        "ch02_type_compass_preview.png",
        "类型选择罗盘",
        "面对新数据时，先判断它是文字、数量、判断、一串材料，还是一条记录。",
    )


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    WEB_DIR.mkdir(parents=True, exist_ok=True)

    cover()
    roadmap()
    variable_label_metaphor()
    powershell_data_type_run()
    data_type_atlas()
    information_history_claude_shannon()
    history_george_boole()
    bool_logic_switchboard()
    number_rounding_chart()
    string_material_workbench()
    string_slice_ruler()
    psychology_ebbinghaus_memory()
    list_workbench()
    nested_data_matryoshka()
    dictionary_card_catalog_photo()
    punch_card_sorter_photo()
    dict_mapping_card()
    mini_project_dashboard()
    data_type_lab_receipt()
    stroop_dataset_pack()
    data_type_specimen_cabinet()
    data_type_runtime_evidence()
    type_decision_cards_preview()
    type_compass_preview()
    error_clue_cards()
    practice_workbench()
    type_to_file_bridge()

    if (ROOT / "output_ch02_contact_sheet.png").exists():
        (ROOT / "output_ch02_contact_sheet.png").unlink()
    print("Generated ch02 structured visuals.")


if __name__ == "__main__":
    main()
