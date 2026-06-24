from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ModuleNotFoundError as exc:
    raise SystemExit(
        "This visual generator needs Pillow. Install it with: python -m pip install pillow"
    ) from exc


ROOT = Path.cwd()
if not (ROOT / "assets" / "ch00").exists():
    ROOT = Path(__file__).resolve().parents[1]

ASSET_DIR = ROOT / "assets" / "ch00"
WEB_DIR = ASSET_DIR / "web"

W, H = 1800, 1120
BG = "#F6F8FB"
PANEL = "#FFFFFF"
PANEL_2 = "#F0F4FA"
INK = "#172033"
MUTED = "#667085"
LINE = "#D7DFEA"
GRID = "#E7EDF5"
BLUE = "#2563EB"
GREEN = "#059669"
ORANGE = "#EA7A18"
PURPLE = "#7C3AED"
RED = "#DC3545"
CYAN = "#0891B2"
YELLOW = "#D99A00"
COLORS = [BLUE, GREEN, ORANGE, PURPLE, CYAN, RED, YELLOW]


def canvas(width: int = W, height: int = H):
    im = Image.new("RGB", (width, height), BG)
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, name: str):
    im.save(ASSET_DIR / name, optimize=True, quality=95)


def _font_paths(bold: bool = False) -> list[Path]:
    if bold:
        names = [
            "msyhbd.ttc",
            "simhei.ttf",
            "NotoSansCJKsc-Bold.otf",
            "Arialbd.ttf",
        ]
    else:
        names = [
            "msyh.ttc",
            "simhei.ttf",
            "NotoSansCJKsc-Regular.otf",
            "arial.ttf",
        ]
    windows = Path("C:/Windows/Fonts")
    return [windows / name for name in names]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in _font_paths(bold):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def text_size(d: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    if not text:
        return 0, 0
    box = d.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def _tokens(line: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./:+#-]+|[\u4e00-\u9fff]|[^\sA-Za-z0-9_./:+#\-\u4e00-\u9fff]|\s+", line)


def wrap_line(d: ImageDraw.ImageDraw, line: str, fnt, max_width: int) -> list[str]:
    tokens = _tokens(line)
    lines: list[str] = []
    current = ""
    for token in tokens:
        if token.isspace():
            token = " "
        candidate = (current + token).strip() if not current else current + token
        if not candidate.strip():
            continue
        if text_size(d, candidate, fnt)[0] <= max_width:
            current = candidate
            continue
        if current.strip():
            lines.append(current.strip())
            current = token.strip()
        else:
            current = ""
            piece = ""
            for ch in token:
                candidate_piece = piece + ch
                if text_size(d, candidate_piece, fnt)[0] <= max_width:
                    piece = candidate_piece
                else:
                    if piece:
                        lines.append(piece)
                    piece = ch
            current = piece
    if current.strip():
        lines.append(current.strip())
    punctuation = set("，。；：、,.!?！？)]）")
    cleaned: list[str] = []
    for line in lines:
        if cleaned and line and all(ch in punctuation for ch in line):
            cleaned[-1] += line
        elif cleaned and line and line[0] in punctuation:
            cleaned[-1] += line[0]
            if line[1:].strip():
                cleaned.append(line[1:].strip())
        else:
            cleaned.append(line)
    return cleaned or [""]


def fit_lines(
    d: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_height: int,
    size: int,
    min_size: int = 18,
    bold: bool = False,
    spacing_ratio: float = 0.38,
):
    best = None
    for font_size in range(size, min_size - 1, -1):
        fnt = font(font_size, bold=bold)
        lines: list[str] = []
        for para in text.splitlines() or [""]:
            lines.extend(wrap_line(d, para, fnt, max_width))
        base_h = max(text_size(d, "汉字Ag", fnt)[1], int(font_size * 0.9))
        spacing = max(3, int(font_size * spacing_ratio))
        height = len(lines) * base_h + max(0, len(lines) - 1) * spacing
        if height <= max_height:
            return fnt, lines, base_h, spacing
        best = (fnt, lines, base_h, spacing)
    return best


def draw_text(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    text: str,
    size: int = 34,
    min_size: int = 18,
    fill: str = INK,
    bold: bool = False,
    align: str = "left",
    valign: str = "top",
):
    x1, y1, x2, y2 = xy
    max_width = max(10, x2 - x1)
    max_height = max(10, y2 - y1)
    fnt, lines, line_h, spacing = fit_lines(d, text, max_width, max_height, size, min_size, bold)
    total_h = len(lines) * line_h + max(0, len(lines) - 1) * spacing
    if valign == "center":
        y = y1 + (max_height - total_h) // 2
    elif valign == "bottom":
        y = y2 - total_h
    else:
        y = y1
    for line in lines:
        width, _ = text_size(d, line, fnt)
        if align == "center":
            x = x1 + (max_width - width) // 2
        elif align == "right":
            x = x2 - width
        else:
            x = x1
        d.text((x, y), line, font=fnt, fill=fill)
        y += line_h + spacing


def rounded(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    fill: str = PANEL,
    outline: str = LINE,
    radius: int = 24,
    width: int = 2,
):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def shadow(d: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], radius: int = 24):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#DDE4EF")


def arrow(
    d: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: str = "#A8B4C7",
    width: int = 5,
):
    x1, y1 = start
    x2, y2 = end
    d.line((x1, y1, x2, y2), fill=color, width=width)
    dx, dy = x2 - x1, y2 - y1
    length = max(1, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    size = width * 3.6
    head = [
        (x2, y2),
        (x2 - ux * size + px * size * 0.45, y2 - uy * size + py * size * 0.45),
        (x2 - ux * size - px * size * 0.45, y2 - uy * size - py * size * 0.45),
    ]
    d.polygon(head, fill=color)


def badge(d: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str, color: str):
    rounded(d, xy, fill="#FFFFFF", outline=color, radius=20, width=3)
    draw_text(d, (xy[0] + 16, xy[1] + 6, xy[2] - 16, xy[3] - 6), text, size=24, min_size=16, fill=color, bold=True, align="center", valign="center")


def title(d: ImageDraw.ImageDraw, text: str, subtitle: str = ""):
    draw_text(d, (110, 70, 1690, 145), text, size=54, min_size=36, fill=INK, bold=True, align="center", valign="center")
    if subtitle:
        draw_text(d, (180, 148, 1620, 205), subtitle, size=28, min_size=22, fill=MUTED, align="center", valign="center")


def step_card(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    label: str,
    heading: str,
    body: str,
    color: str,
    number: str | None = None,
):
    shadow(d, xy, radius=22)
    rounded(d, xy, fill=PANEL, outline=LINE, radius=22, width=2)
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1, y1, x1 + 14, y2), radius=7, fill=color)
    if number:
        d.ellipse((x1 + 28, y1 + 22, x1 + 84, y1 + 78), fill=color)
        draw_text(d, (x1 + 28, y1 + 22, x1 + 84, y1 + 78), number, size=28, min_size=20, fill="#FFFFFF", bold=True, align="center", valign="center")
        text_x = x1 + 104
    else:
        text_x = x1 + 34
    draw_text(d, (text_x, y1 + 18, x2 - 28, y1 + 48), label, size=20, min_size=16, fill=color, bold=True, valign="center")
    draw_text(d, (text_x, y1 + 54, x2 - 28, y1 + 100), heading, size=31, min_size=22, fill=INK, bold=True, valign="center")
    draw_text(d, (x1 + 34, y1 + 104, x2 - 28, y2 - 18), body, size=24, min_size=18, fill=MUTED)


def photo_plate(output_name: str, image_name: str):
    im, d = canvas(1800, 1180)
    shadow(d, (110, 90, 1690, 1050), radius=34)
    rounded(d, (110, 90, 1690, 1050), fill="#FFFFFF", radius=34)
    frame = (160, 140, 1640, 930)
    d.rounded_rectangle(frame, radius=26, fill="#F2F4F8", outline=LINE, width=2)

    src = WEB_DIR / image_name
    if src.exists():
        raw = Image.open(src)
        raw = ImageOps.exif_transpose(raw).convert("RGB")
        shown = ImageOps.contain(raw, (frame[2] - frame[0] - 30, frame[3] - frame[1] - 30), method=Image.Resampling.LANCZOS)
        x = frame[0] + (frame[2] - frame[0] - shown.width) // 2
        y = frame[1] + (frame[3] - frame[1] - shown.height) // 2
        im.paste(shown, (x, y))
    else:
        d.line((760, 470, 1040, 650), fill=RED, width=12)
        d.line((1040, 470, 760, 650), fill=RED, width=12)

    save(im, output_name)


def cover():
    im, d = canvas()
    title(d, "第0章：Python 入门地图", "先建立方向感，再开始写第一行代码")
    rounded(d, (135, 245, 1665, 910), fill="#FFFFFF", outline=LINE, radius=30, width=2)
    steps = [
        ("地图", "课程路线", "知道每章学什么，以及为什么按这个顺序走。", BLUE),
        ("环境", "运行现场", "认清解释器、终端、IDE、脚本文件之间的关系。", GREEN),
        ("工厂", "项目目录", "把 input、cards、output、reports 放在清楚位置。", ORANGE),
        ("闭环", "运行反馈", "先跑通，再改一点，出错后顺着线索修复。", PURPLE),
        ("作品", "可复查结果", "每章留下一个能复用的小工具或小报告。", RED),
    ]
    xs = [245, 555, 865, 1175, 1485]
    y = 575
    for i, (label, heading, body, color) in enumerate(steps):
        if i < len(steps) - 1:
            arrow(d, (xs[i] + 118, y), (xs[i + 1] - 118, y), width=5)
        step_card(d, (xs[i] - 118, 405, xs[i] + 118, 745), label, heading, body, color, str(i))
    draw_text(d, (270, 795, 1530, 860), "本章目标：把“我想学 Python”变成“我知道从哪里开始、怎么验证、如何继续”。", size=31, min_size=24, fill=INK, bold=True, align="center", valign="center")
    save(im, "ch00_cover.png")


def automation_card():
    photo_plate("ch00_xkcd_automation_card.png", "xkcd_1205_is_it_worth_the_time.png")


def history_ada_card():
    photo_plate("ch00_history_ada_lovelace_card.png", "ada_lovelace_portrait.jpg")


def history_babbage_card():
    photo_plate("ch00_history_babbage_difference_engine.png", "babbage_difference_engine.jpg")


def history_guido_card():
    photo_plate("ch00_history_guido_van_rossum.png", "guido_van_rossum.jpg")


def history_jacquard_card():
    photo_plate("ch00_history_jacquard_card.png", "jacquard_loom_cards.jpg")


def history_bug_card():
    photo_plate("ch00_history_first_bug_card.png", "first_computer_bug_1947.jpg")


def history_apollo_card():
    photo_plate("ch00_history_apollo_software_card.png", "margaret_hamilton_apollo_code.jpg")


def history_eniac_card():
    photo_plate("ch00_history_eniac_programmers.png", "eniac_programmers.gif")


def factory_card_catalog():
    photo_plate("ch00_factory_card_catalog.png", "card_catalog_drawer.jpg")


def factory_lab_notebook():
    photo_plate("ch00_factory_lab_notebook.png", "lab_notebook.jpg")


def factory_conveyor():
    photo_plate("ch00_factory_conveyor.png", "belt_conveyor_handling.jpg")


def draw_relation(d: ImageDraw.ImageDraw, center: tuple[int, int], items: Iterable[tuple[int, int, str, str, str]]):
    cx, cy = center
    for x, y, _, _, color in items:
        arrow(d, (cx + int((x - cx) * 0.18), cy + int((y - cy) * 0.18)), (x - int((x - cx) * 0.22), y - int((y - cy) * 0.22)), color="#C0CAD8", width=4)
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=color)


def city():
    im, d = canvas()
    title(d, "Python 之城入门地图", "新手先找地图、交通和营地，再探索复杂街区")
    rounded(d, (160, 230, 1640, 935), fill="#FFFFFF", outline=LINE, radius=32, width=2)
    center = (900, 575)
    d.ellipse((center[0] - 145, center[1] - 145, center[0] + 145, center[1] + 145), fill="#EEF5FF", outline=BLUE, width=5)
    draw_text(d, (center[0] - 105, center[1] - 75, center[0] + 105, center[1] + 75), "Python\n入口广场", size=38, min_size=26, fill=BLUE, bold=True, align="center", valign="center")
    items = [
        (390, 350, "地图站", "课程路线、章节目标", BLUE),
        (1410, 350, "交通站", "解释器、终端、IDE", GREEN),
        (390, 780, "营地", "项目目录与文件收纳", ORANGE),
        (1410, 780, "练习场", "运行、修改、复盘", PURPLE),
        (900, 875, "急救站", "读懂报错，定位问题", RED),
    ]
    draw_relation(d, center, items)
    for x, y, heading, body, color in items:
        step_card(d, (x - 170, y - 95, x + 170, y + 95), "", heading, body, color)
    save(im, "python_city_metaphor.png")


def roadmap():
    im, d = canvas()
    title(d, "整套课程路线图", "基础、组织、应用、项目成果逐步接力")
    chapters = [
        ("0", "地图", "学习方法"),
        ("1", "环境", "运行代码"),
        ("2", "数据", "变量类型"),
        ("3", "文件", "读写整理"),
        ("4", "界面", "窗口按钮"),
        ("5", "对象", "组织代码"),
        ("6", "分析", "表格图表"),
        ("7", "游戏", "动画交互"),
        ("8", "爬虫", "网页资料"),
        ("9", "图像", "像素处理"),
        ("10", "办公", "文档成果"),
    ]
    x0, y0 = 85, 310
    card_w, card_h = 245, 170
    gap_x, gap_y = 35, 70
    positions = []
    for idx, item in enumerate(chapters):
        row = 0 if idx < 6 else 1
        col = idx if idx < 6 else idx - 6
        x = x0 + col * (card_w + gap_x)
        y = y0 + row * (card_h + gap_y)
        if row == 1:
            x += 135
        positions.append((x, y, item))
    for idx, (x, y, item) in enumerate(positions):
        color = COLORS[idx % len(COLORS)]
        if idx < len(positions) - 1:
            nx, ny, _ = positions[idx + 1]
            start = (x + card_w, y + card_h // 2)
            end = (nx, ny + card_h // 2)
            if idx == 5:
                start = (x + card_w // 2, y + card_h)
                end = (positions[idx + 1][0] + card_w // 2, positions[idx + 1][1])
            arrow(d, start, end, color="#B8C4D4", width=4)
        number, heading, body = item
        step_card(d, (x, y, x + card_w, y + card_h), f"第{number}章", heading, body, color)
    save(im, "course_roadmap.png")


def project_ladder():
    im, d = canvas()
    title(d, "项目阶梯：从空目录到可复查", "小台阶比大口号更可靠")
    steps = [
        ("01", "建目录", "先分清 input、cards、output、reports。", BLUE),
        ("02", "放原料", "课程笔记、数据、图片各归其位。", GREEN),
        ("03", "写脚本", "让重复动作有稳定入口。", ORANGE),
        ("04", "生成结果", "输出报告、卡片或运行记录。", PURPLE),
        ("05", "复盘改进", "记录问题，下一章继续接上。", RED),
    ]
    base_y = 875
    step_w = 285
    step_h = 175
    x0 = 160
    for idx, (num, heading, body, color) in enumerate(steps):
        x = x0 + idx * 305
        y = base_y - idx * 105
        step_card(d, (x, y - step_h, x + step_w, y), "", heading, body, color, num)
        if idx < len(steps) - 1:
            arrow(d, (x + step_w + 8, y - step_h // 2), (x + 305 - 18, y - 105 - step_h // 2), color="#AEBBCD", width=4)
    draw_text(d, (170, 935, 1630, 1000), "判断一个项目是否开始成形：看它有没有清楚的目录、可运行的脚本和可检查的输出。", size=30, min_size=24, fill=INK, bold=True, align="center", valign="center")
    save(im, "project_ladder.png")


def env_pipeline():
    im, d = canvas()
    title(d, "Python 环境流水线", "代码不是飘在屏幕上的字，它有清楚的运行现场")
    steps = [
        ("解释器", "真正执行 Python 指令", "python", BLUE),
        ("终端", "发出运行命令并显示结果", "cmd", GREEN),
        ("IDE", "写代码、管理项目、点运行", "IDE", ORANGE),
        ("文件与路径", "告诉程序脚本和素材在哪里", ".py", PURPLE),
        ("脚本输出", "把结果保存为文本、图片或报告", "out", CYAN),
    ]
    x0, y, w, h, gap = 120, 420, 290, 290, 55
    for idx, (heading, body, code, color) in enumerate(steps):
        x = x0 + idx * (w + gap)
        if idx < len(steps) - 1:
            arrow(d, (x + w + 8, y + h // 2), (x + w + gap - 12, y + h // 2), width=5)
        step_card(d, (x, y, x + w, y + h), code, heading, body, color, str(idx + 1))
    rounded(d, (240, 800, 1560, 910), fill="#EEF5FF", outline="#C9DAFF", radius=24, width=2)
    draw_text(d, (280, 820, 1520, 890), "最小运行句式：在正确目录打开终端，执行 python code/ch00/check_python_env.py", size=29, min_size=22, fill=BLUE, bold=True, align="center", valign="center")
    save(im, "env_pipeline.png")


def error_map():
    im, d = canvas()
    title(d, "常见报错线索图", "先看错误类型，再看文件名和行号")
    items = [
        ("SyntaxError", "语法写法不完整", "检查括号、冒号、引号", BLUE),
        ("NameError", "名字还没有定义", "检查变量名是否拼错", GREEN),
        ("TypeError", "类型用法不匹配", "确认字符串和数字别混用", ORANGE),
        ("FileNotFound", "文件路径找不到", "打印当前目录再核对路径", PURPLE),
        ("ModuleNotFound", "库没有安装或环境不对", "确认 pip 装在同一个解释器", CYAN),
        ("IndentationError", "缩进层级混乱", "统一空格，别混 Tab", RED),
    ]
    x0, y0 = 120, 270
    w, h = 500, 210
    gap_x, gap_y = 80, 65
    for idx, (name, cause, fix, color) in enumerate(items):
        row, col = divmod(idx, 3)
        x = x0 + col * (w + gap_x)
        y = y0 + row * (h + gap_y)
        step_card(d, (x, y, x + w, y + h), cause, name, fix, color)
    save(im, "error_map.png")


def learning_loop():
    im, d = canvas()
    title(d, "学习闭环：让程序动起来", "理解不是一次读完，而是一圈圈获得反馈")
    center = (900, 585)
    r = 335
    steps = [
        (900, 255, "读", "读懂目标", BLUE),
        (1225, 480, "跑", "先跑通", GREEN),
        (1100, 855, "改", "只改一点", ORANGE),
        (700, 855, "错", "记录报错", RED),
        (575, 480, "修", "定位修复", PURPLE),
    ]
    for idx, (x, y, _, _, _) in enumerate(steps):
        nx, ny = steps[(idx + 1) % len(steps)][0], steps[(idx + 1) % len(steps)][1]
        arrow(d, (x, y), (nx, ny), color="#B7C3D4", width=4)
    d.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), outline="#DDE6F2", width=3)
    for x, y, short, body, color in steps:
        d.ellipse((x - 92, y - 92, x + 92, y + 92), fill="#FFFFFF", outline=color, width=5)
        draw_text(d, (x - 45, y - 55, x + 45, y - 5), short, size=40, min_size=30, fill=color, bold=True, align="center", valign="center")
        draw_text(d, (x - 70, y + 5, x + 70, y + 58), body, size=23, min_size=18, fill=INK, bold=True, align="center", valign="center")
    draw_text(d, (710, 520, 1090, 650), "运行\n修改\n反馈", size=44, min_size=32, fill=INK, bold=True, align="center", valign="center")
    save(im, "learning_loop.png")


def learning_momentum_chart():
    im, d = canvas()
    title(d, "学习反馈曲线", "信心通常来自一次次可验证的小成功")
    chart = (210, 255, 1510, 845)
    x1, y1, x2, y2 = chart
    rounded(d, chart, fill="#FFFFFF", outline=LINE, radius=24, width=2)
    for k in range(6):
        y = y1 + 85 + k * 80
        d.line((x1 + 95, y, x2 - 90, y), fill=GRID, width=2)
    d.line((x1 + 100, y2 - 95, x2 - 85, y2 - 95), fill="#94A3B8", width=4)
    d.line((x1 + 100, y1 + 70, x1 + 100, y2 - 95), fill="#94A3B8", width=4)
    points = [
        ("运行", 18),
        ("小改", 25),
        ("报错", 20),
        ("定位", 36),
        ("修复", 44),
        ("再改", 41),
        ("作品", 58),
        ("复盘", 66),
        ("复用", 74),
        ("成果", 86),
    ]
    curve = []
    for i, (_, v) in enumerate(points):
        curve.append((x1 + 140 + i * 118, y2 - 108 - int(v * 4.25)))
    area = [(curve[0][0], y2 - 95)] + curve + [(curve[-1][0], y2 - 95)]
    d.polygon(area, fill="#DCEBFF")
    d.line(curve, fill=BLUE, width=7)
    for (label, _), (x, y) in zip(points, curve):
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill="#FFFFFF", outline=BLUE, width=4)
        draw_text(d, (x - 45, y2 - 82, x + 45, y2 - 45), label, size=20, min_size=16, fill=MUTED, align="center", valign="center")
    draw_text(d, (95, 430, 190, 575), "掌控感", size=24, min_size=18, fill=MUTED, align="center", valign="center")
    draw_text(d, (1515, 455, 1670, 585), "每一小步都要有可检查结果", size=25, min_size=20, fill=BLUE, bold=True, align="center", valign="center")
    save(im, "learning_momentum_chart.png")


def tech_stack_workbench():
    im, d = canvas()
    title(d, "技术栈工作台", "工具按任务摆放，需要时再拿起来")
    groups = [
        ("先跑起来", "Python 标准库\npathlib / os / shutil", BLUE),
        ("整理资料", "numpy\npandas\nopenpyxl", GREEN),
        ("画成图表", "matplotlib\nPillow / OpenCV", ORANGE),
        ("做出交互", "tkinter\npygame\nrequests", PURPLE),
        ("最终作品", "python-docx\npython-pptx\n报告与演示", CYAN),
    ]
    x0, y0, w, h, gap = 90, 320, 290, 350, 38
    labels = ["基础", "数据", "图表", "交互", "成果"]
    for idx, (heading, body, color) in enumerate(groups):
        x = x0 + idx * (w + gap)
        step_card(d, (x, y0, x + w, y0 + h), labels[idx], heading, body, color)
    bench = (170, 780, 1630, 905)
    rounded(d, bench, fill="#EAF0F8", outline=LINE, radius=28, width=2)
    draw_text(d, (220, 807, 1580, 875), "第0章先把工具放到脑海里的正确位置；真正用到时，再逐个拿起来。", size=31, min_size=24, fill=INK, bold=True, align="center", valign="center")
    save(im, "tech_stack_workbench.png")


def chapter_relay_station():
    im, d = canvas()
    title(d, "章节接力中继站", "前四章先把环境、数据、文件和界面接起来")
    top = [
        ("0", "课程地图", "学习方法", BLUE),
        ("1", "工作环境", "跑通脚本", GREEN),
        ("2", "数据类型", "组织信息", ORANGE),
        ("3", "文件管理", "整理材料", PURPLE),
        ("4", "图形界面", "做出窗口", CYAN),
    ]
    bottom = [
        ("5", "对象", "封装代码", RED),
        ("6", "分析", "表格图表", BLUE),
        ("7", "游戏", "动画交互", GREEN),
        ("8", "爬虫", "公开资料", ORANGE),
        ("9-10", "图像/办公", "最终成果", PURPLE),
    ]
    x0, w, gap = 90, 290, 40
    for idx, item in enumerate(top):
        x = x0 + idx * (w + gap)
        num, heading, body, color = item
        step_card(d, (x, 280, x + w, 465), f"第{num}章", heading, body, color)
        if idx < len(top) - 1:
            arrow(d, (x + w + 6, 372), (x + w + gap - 12, 372), width=4)
    rounded(d, (615, 525, 1185, 625), fill="#FFF8E8", outline="#F5D08A", radius=24, width=2)
    draw_text(d, (655, 545, 1145, 605), "共同产线：科研卡片工厂", size=32, min_size=24, fill=YELLOW, bold=True, align="center", valign="center")
    arrow(d, (900, 465), (900, 525), color="#C0CAD8", width=5)
    arrow(d, (900, 625), (900, 680), color="#C0CAD8", width=5)
    for idx, item in enumerate(bottom):
        x = x0 + idx * (w + gap)
        num, heading, body, color = item
        step_card(d, (x, 680, x + w, 865), f"第{num}章", heading, body, color)
        if idx < len(bottom) - 1:
            arrow(d, (x + w + 6, 772), (x + w + gap - 12, 772), width=4)
    save(im, "chapter_relay_station.png")


def chapter_blueprint_bridge():
    im, d = canvas()
    title(d, "章节蓝图接力", "每章留下材料，下一章继续加工")
    chapters = [
        ("0", "地图", "方向感", BLUE),
        ("1", "环境", "运行入口", GREEN),
        ("2", "数据", "卡片字段", ORANGE),
        ("3", "文件", "原料整理", PURPLE),
        ("4", "界面", "录入窗口", CYAN),
        ("5", "对象", "卡片类", RED),
        ("6", "分析", "数据报告", BLUE),
        ("7", "游戏", "互动复习", GREEN),
        ("8", "爬虫", "资料采集", ORANGE),
        ("9", "图像", "批量配图", PURPLE),
        ("10", "办公", "Word/PPT", CYAN),
    ]
    positions: list[tuple[int, int, tuple[str, str, str, str]]] = []
    card_w, card_h = 230, 155
    x0, gap = 90, 45
    for idx, ch in enumerate(chapters):
        if idx < 6:
            x = x0 + idx * (card_w + gap)
            y = 300
        else:
            x = x0 + (10 - idx) * (card_w + gap)
            y = 680
        positions.append((x, y, ch))
    for idx, (x, y, ch) in enumerate(positions):
        if idx < len(positions) - 1:
            nx, ny, _ = positions[idx + 1]
            if idx == 5:
                arrow(d, (x + card_w // 2, y + card_h + 8), (nx + card_w // 2, ny - 8), width=4)
            else:
                start = (x + card_w + 6, y + card_h // 2) if y == ny else (x - 6, y + card_h // 2)
                end = (nx - 12, ny + card_h // 2) if y == ny and nx > x else (nx + card_w + 12, ny + card_h // 2)
                arrow(d, start, end, width=4)
        num, heading, body, color = ch
        step_card(d, (x, y, x + card_w, y + card_h), f"第{num}章", heading, body, color)
    rounded(d, (520, 510, 1280, 600), fill="#EEF5FF", outline="#C9DAFF", radius=24, width=2)
    draw_text(d, (560, 530, 1240, 580), "主线目标：把学习材料加工成可复用作品", size=31, min_size=23, fill=BLUE, bold=True, align="center", valign="center")
    save(im, "chapter_blueprint_bridge.png")


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    cover()
    automation_card()
    factory_card_catalog()
    history_ada_card()
    history_babbage_card()
    history_guido_card()
    city()
    history_jacquard_card()
    roadmap()
    project_ladder()
    factory_lab_notebook()
    history_apollo_card()
    history_eniac_card()
    env_pipeline()
    factory_conveyor()
    error_map()
    history_bug_card()
    learning_loop()
    learning_momentum_chart()
    tech_stack_workbench()
    chapter_relay_station()
    chapter_blueprint_bridge()
    print("Generated ch00 structured visuals.")


if __name__ == "__main__":
    main()
