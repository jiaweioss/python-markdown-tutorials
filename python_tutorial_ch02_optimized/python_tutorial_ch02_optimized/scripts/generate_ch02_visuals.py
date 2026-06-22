from __future__ import annotations

import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
if not (ROOT / "assets" / "ch02").exists():
    ROOT = Path(__file__).resolve().parents[1]

ASSET_DIR = ROOT / "assets" / "ch02"
WEB_DIR = ASSET_DIR / "web"

W, H = 1800, 1120
BG = "#F6F8FB"
INK = "#172033"
MUTED = "#5D6678"
LINE = "#D9E1EE"
NAVY = "#1D2A44"
BLUE = "#2F6BFF"
GREEN = "#24A06B"
ORANGE = "#F28C28"
PURPLE = "#7A5AF8"
RED = "#E84C61"
CYAN = "#18A9B5"
GOLD = "#D99B00"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
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


F_TITLE = font(58, True)
F_SUBTITLE = font(28)
F_H2 = font(34, True)
F_BODY = font(25)
F_SMALL = font(20)
F_TINY = font(17)
F_MONO = font(24)


def canvas(width: int = W, height: int = H) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(im)
    return im, d


def rounded(d: ImageDraw.ImageDraw, xy, fill, outline=LINE, radius=24, width=3):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def shadow_box(d: ImageDraw.ImageDraw, xy, fill="#FFFFFF", outline=LINE, radius=24):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#D8DEE9")
    rounded(d, xy, fill=fill, outline=outline, radius=radius, width=2)


def draw_text(
    d: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    fnt: ImageFont.FreeTypeFont = F_BODY,
    fill: str = INK,
    max_chars: int | None = None,
    line_gap: int = 9,
) -> int:
    x, y = xy
    lines: list[str] = []
    for paragraph in text.splitlines():
        if paragraph:
            lines.extend(textwrap.wrap(paragraph, max_chars or 28, break_long_words=True, replace_whitespace=False))
        else:
            lines.append("")
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def title_block(d: ImageDraw.ImageDraw, title: str, subtitle: str):
    d.text((92, 72), title, font=F_TITLE, fill=INK)
    d.text((96, 148), subtitle, font=F_SUBTITLE, fill=MUTED)
    d.line((96, 206, 1704, 206), fill=LINE, width=3)


def pill(d, x, y, text, color, width=110):
    d.rounded_rectangle((x, y, x + width, y + 42), radius=21, fill=color)
    d.text((x + 24, y + 7), text, font=F_SMALL, fill="white")


def arrow(d, start, end, color="#A9B6CA", width=6):
    d.line((start, end), fill=color, width=width)
    x2, y2 = end
    x1, y1 = start
    if abs(x2 - x1) >= abs(y2 - y1):
        sign = 1 if x2 > x1 else -1
        pts = [(x2, y2), (x2 - sign * 22, y2 - 12), (x2 - sign * 22, y2 + 12)]
    else:
        sign = 1 if y2 > y1 else -1
        pts = [(x2, y2), (x2 - 12, y2 - sign * 22), (x2 + 12, y2 - sign * 22)]
    d.polygon(pts, fill=color)


def card(d, xy, tag, title, desc, color, tag_width=110):
    x1, y1, x2, y2 = xy
    shadow_box(d, xy)
    pill(d, x1 + 26, y1 + 24, tag, color, width=tag_width)
    d.text((x1 + 158, y1 + 23), title, font=F_H2, fill=INK)
    draw_text(d, desc, (x1 + 34, y1 + 96), F_BODY, MUTED, max_chars=22)


def save(im: Image.Image, name: str):
    im.save(ASSET_DIR / name, optimize=True, quality=95)


def photo_plate(output_name: str, image_name: str):
    im, d = canvas(1800, 1180)
    shadow_box(d, (110, 90, 1690, 1050), fill="#FFFFFF", outline=LINE, radius=34)
    frame = (160, 140, 1640, 930)
    d.rounded_rectangle(frame, radius=26, fill="#F2F4F8", outline=LINE, width=2)

    src = WEB_DIR / image_name
    if src.exists():
        raw = Image.open(src)
        raw = ImageOps.exif_transpose(raw).convert("RGB")
        resampling = getattr(Image, "Resampling", Image).LANCZOS
        shown = ImageOps.contain(raw, (frame[2] - frame[0] - 30, frame[3] - frame[1] - 30), method=resampling)
        x = frame[0] + (frame[2] - frame[0] - shown.width) // 2
        y = frame[1] + (frame[3] - frame[1] - shown.height) // 2
        im.paste(shown, (x, y))
    else:
        d.line((760, 470, 1040, 650), fill=RED, width=12)
        d.line((1040, 470, 760, 650), fill=RED, width=12)

    save(im, output_name)


def cover():
    im, d = canvas()
    d.rounded_rectangle((70, 56, 1730, 220), radius=28, fill=NAVY)
    d.text((118, 92), "第 2 章  Python 编程基础：数据类型", font=F_TITLE, fill="white")
    d.text((124, 164), "变量像标签，类型像工具盒；先认识材料，再开始搭作品。", font=F_SUBTITLE, fill="#D6E1F5")
    shadow_box(d, (155, 305, 1645, 820), fill="#FFFFFF")
    rounded(d, (690, 380, 1110, 690), fill="#111827", outline="#111827", radius=20)
    code = [
        "score = 95",
        "name = 'Python 新手'",
        "passed = score >= 60",
        "tools = ['str', 'list', 'dict']",
    ]
    for i, line in enumerate(code):
        d.text((740, 430 + i * 58), line, font=F_MONO, fill=["#A7F3D0", "#FDE68A", "#93C5FD", "#C4B5FD"][i])
    topics = [
        ((215, 375, 565, 500), "VAR", "变量", "把名字贴到对象上", BLUE),
        ((215, 595, 565, 720), "BOOL", "布尔", "判断真假与条件", GREEN),
        ((1235, 375, 1585, 500), "STR", "字符串", "文本、索引、切片", ORANGE),
        ((1235, 595, 1585, 720), "LIST", "列表", "顺序容器，可增删", PURPLE),
    ]
    for xy, tag, title, desc, color in topics:
        card(d, xy, tag, title, desc, color, tag_width=104)
    d.text((178, 908), "本章目标：会选类型、会读索引、会改列表和字典，并用一个小项目把数据整理成可复用结构。", font=F_SUBTITLE, fill=MUTED)
    save(im, "ch02_cover.png")


def roadmap():
    im, d = canvas()
    title_block(d, "第 2 章知识路线图", "这章不是背名词，而是学会给数据选择合适的容器。容器选对，代码就清爽一半。")
    steps = [
        ("1", "常量与关键字", "True / False / None\nkeyword.kwlist", BLUE),
        ("2", "变量与引用", "变量不是盒子\n更像贴在对象上的标签", GREEN),
        ("3", "布尔与数值", "and / or / not\nint / float / round", ORANGE),
        ("4", "字符串", "创建、转换、拼接\n查找、替换、切片", PURPLE),
        ("5", "列表", "索引、切片、嵌套\nappend / del / 合并", CYAN),
        ("6", "字典", "key 找 value\n增删改查", RED),
    ]
    positions = [(120, 300), (610, 300), (1100, 300), (1100, 620), (610, 620), (120, 620)]
    for i in range(len(positions) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        arrow(d, (x1 + 395, y1 + 105), (x2 - 35 if x2 > x1 else x2 + 435, y2 + 105))
    for (num, title, desc, color), (x, y) in zip(steps, positions):
        card(d, (x, y, x + 430, y + 220), num, title, desc, color, tag_width=92)
    d.rounded_rectangle((360, 925, 1440, 1038), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    draw_text(d, "通关标准：看到一份数据，能说出它适合用字符串、列表还是字典，并能写出基本操作。", (430, 957), F_BODY, "#28517A", max_chars=42, line_gap=7)
    save(im, "ch02_roadmap.png")


def variable_label_metaphor():
    im, d = canvas()
    title_block(d, "变量不是盒子，更像贴在对象上的标签", "这张图专门纠正初学者最容易误会的一点：赋值不是搬家，而是把名字指向对象。")
    shadow_box(d, (130, 310, 760, 825), fill="#FFFFFF")
    d.text((180, 355), "很多教材里的盒子想象", font=F_H2, fill=INK)
    rounded(d, (230, 470, 420, 650), fill="#EEF2FF", outline=BLUE, radius=18)
    d.text((282, 535), "a", font=F_TITLE, fill=BLUE)
    d.text((300, 595), "2", font=F_H2, fill=INK)
    rounded(d, (500, 470, 690, 650), fill="#EEF2FF", outline=GREEN, radius=18)
    d.text((552, 535), "b", font=F_TITLE, fill=GREEN)
    d.text((570, 595), "2", font=F_H2, fill=INK)
    draw_text(d, "容易误解成：a 和 b 是两个独立盒子，各自装着一份值。", (190, 705), F_BODY, MUTED, max_chars=24)

    shadow_box(d, (925, 310, 1670, 825), fill="#FFFFFF")
    d.text((975, 355), "Python 更接近标签模型", font=F_H2, fill=INK)
    d.ellipse((1235, 500, 1435, 700), fill="#FFF7E8", outline=ORANGE, width=5)
    d.text((1290, 565), "对象\n2", font=F_H2, fill=INK, spacing=8)
    pill(d, 1035, 500, "a", BLUE, width=72)
    pill(d, 1035, 610, "b", GREEN, width=72)
    arrow(d, (1110, 522), (1230, 575), width=4)
    arrow(d, (1110, 632), (1230, 625), width=4)
    draw_text(d, "更准确地说：a 和 b 都是名字，它们可以同时指向同一个对象。重新赋值，就是把标签贴到新对象上。", (1000, 735), F_BODY, MUTED, max_chars=32)

    d.rounded_rectangle((330, 920, 1470, 1030), radius=24, fill="#F1FFF7", outline=GREEN, width=3)
    draw_text(d, "课堂金句：变量名不是保险箱，而是便签纸。便签纸贴在哪里，Python 就去哪里找值。", (400, 952), F_BODY, "#176342", max_chars=42)
    save(im, "ch02_variable_label_metaphor.png")


def data_type_atlas():
    im, d = canvas()
    title_block(d, "Python 数据类型地图：不同材料，放进不同容器", "别急着记所有类型，先记住它们各自擅长解决什么问题。")
    items = [
        ((100, 300, 570, 485), "BOOL", "布尔 bool", "只有 True / False\n适合做判断、开关、条件", BLUE),
        ((665, 300, 1135, 485), "NUM", "数值 int / float", "整数、浮点数、复数\n适合计算、统计、计分", GREEN),
        ((1230, 300, 1700, 485), "STR", "字符串 str", "文字、姓名、路径、问卷题目\n适合查找、替换、切片", ORANGE),
        ((100, 625, 570, 810), "LIST", "列表 list", "有顺序的一串数据\n适合追加、删除、遍历", PURPLE),
        ((665, 625, 1135, 810), "TUP", "元组 tuple", "稳定的一组值\n适合坐标、固定配置", CYAN),
        ((1230, 625, 1700, 810), "DICT", "字典 dict", "key 对应 value\n适合查表、记录对象信息", RED),
    ]
    for xy, tag, title, desc, color in items:
        card(d, xy, tag, title, desc, color, tag_width=105)
    d.rounded_rectangle((300, 930, 1500, 1038), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw_text(d, "选类型的口诀：单个判断用 bool，连续文本用 str，有顺序用 list，按名字查信息用 dict。", (370, 962), F_BODY, "#8A5A00", max_chars=46)
    save(im, "ch02_data_type_atlas.png")


def information_history_claude_shannon():
    photo_plate("ch02_information_history_claude_shannon.png", "claude_shannon_mfo3807.jpg")


def bool_logic_switchboard():
    im, d = canvas()
    title_block(d, "布尔逻辑开关台：and、or、not 到底在问什么？", "逻辑运算不是玄学，它只是把条件组合成一盏能亮或不亮的灯。")
    shadow_box(d, (120, 300, 1680, 820), fill="#FFFFFF")
    gates = [
        ((180, 405, 600, 635), "and", "两个条件都满足\n灯才亮", BLUE, [True, True], True),
        ((690, 405, 1110, 635), "or", "至少一个条件满足\n灯就亮", GREEN, [True, False], True),
        ((1200, 405, 1620, 635), "not", "把结果反过来\n真变假，假变真", ORANGE, [False], True),
    ]
    for xy, name, desc, color, inputs, output in gates:
        x1, y1, x2, y2 = xy
        rounded(d, xy, fill="#F8FAFC", outline=LINE, radius=24)
        pill(d, x1 + 35, y1 + 30, name, color, width=110)
        draw_text(d, desc, (x1 + 35, y1 + 92), F_BODY, MUTED, max_chars=16)
        for j, value in enumerate(inputs):
            y = y1 + 150 + j * 48
            d.ellipse((x1 + 250, y, x1 + 284, y + 34), fill=GREEN if value else RED)
            d.text((x1 + 300, y + 2), str(value), font=F_SMALL, fill=INK)
        d.ellipse((x2 - 110, y1 + 80, x2 - 40, y1 + 150), fill=GREEN if output else RED)
        d.text((x2 - 97, y1 + 158), str(output), font=F_SMALL, fill=INK)
    d.rounded_rectangle((330, 905, 1470, 1030), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    draw_text(d, "优先级提醒：not 先算，and 其次，or 最后。写复杂条件时，宁愿多加括号，也不要让读者猜。", (400, 940), F_BODY, "#28517A", max_chars=42)
    save(im, "ch02_bool_logic_switchboard.png")


def history_george_boole():
    photo_plate("ch02_history_george_boole.png", "george_boole_color.jpg")


def number_rounding_chart():
    im, d = canvas()
    title_block(d, "数值取整图表：round、floor、ceil 的性格不同", "这是一张由 Python 脚本生成的教学图表，用来解释“看起来都像取整，其实规则不一样”。")
    shadow_box(d, (135, 300, 1220, 875), fill="#FFFFFF")
    x0, y0, w, h = 230, 780, 650, 340
    d.line((x0, y0, x0 + w, y0), fill="#94A3B8", width=3)
    d.line((x0, y0, x0, y0 - h), fill="#94A3B8", width=3)
    for n in range(0, 5):
        x = x0 + int(n / 4 * w)
        d.line((x, y0 - 8, x, y0 + 8), fill="#94A3B8", width=2)
        d.text((x - 8, y0 + 18), str(n), font=F_TINY, fill=MUTED)
    for n in range(0, 5):
        y = y0 - int(n / 4 * h)
        d.line((x0 - 8, y, x0 + 8, y), fill="#94A3B8", width=2)
        d.text((x0 - 40, y - 12), str(n), font=F_TINY, fill=MUTED)

    xs = [i / 10 for i in range(0, 41)]
    series = [
        ("floor", [math.floor(x) for x in xs], BLUE),
        ("round", [round(x) for x in xs], GREEN),
        ("ceil", [math.ceil(x) for x in xs], ORANGE),
    ]
    for name, ys, color in series:
        pts = []
        for x, y in zip(xs, ys):
            px = x0 + int(x / 4 * w)
            py = y0 - int(y / 4 * h)
            pts.append((px, py))
        d.line(pts, fill=color, width=5)
    d.text((230, 820), "x 从 0 到 4；y 是不同函数的取整结果", font=F_SMALL, fill=MUTED)

    rounded(d, (930, 385, 1135, 555), fill="#F8FAFC", outline=LINE, radius=18)
    legend_x = 960
    for i, (name, _, color) in enumerate(series):
        yy = 420 + i * 48
        d.rounded_rectangle((legend_x, yy, legend_x + 70, yy + 18), radius=9, fill=color)
        d.text((legend_x + 88, yy - 8), name, font=F_BODY, fill=INK)

    shadow_box(d, (1290, 330, 1645, 835), fill="#FFFFFF")
    d.text((1330, 380), "课堂怎么用", font=F_H2, fill=INK)
    tips = [
        "round(x)：四舍五入，注意银行家舍入",
        "floor(x)：向下取整",
        "ceil(x)：向上取整",
        "处理时间、得分、索引时，不要混用",
    ]
    yy = 450
    for tip in tips:
        d.text((1338, yy), "•", font=F_H2, fill=BLUE)
        yy = draw_text(d, tip, (1375, yy), F_SMALL, MUTED, max_chars=18, line_gap=7) + 16
    save(im, "ch02_number_rounding_chart.png")


def string_slice_ruler():
    im, d = canvas()
    title_block(d, "字符串切片尺：左闭右开不是口号，是边界规则", "切片最难的不是语法，而是想清楚从哪里开始、到哪里停下。")
    word = "huawei"
    start_x = 330
    y = 430
    cell = 170
    for i, ch in enumerate(word):
        x = start_x + i * cell
        rounded(d, (x, y, x + 145, y + 145), fill="#FFFFFF", outline=BLUE, radius=18)
        d.text((x + 48, y + 38), ch, font=F_TITLE, fill=INK)
        d.text((x + 56, y - 45), str(i), font=F_BODY, fill=BLUE)
        d.text((x + 48, y + 168), str(i - len(word)), font=F_BODY, fill=ORANGE)
    d.text((170, y - 45), "正向索引", font=F_BODY, fill=BLUE)
    d.text((170, y + 168), "反向索引", font=F_BODY, fill=ORANGE)
    d.line((start_x, y + 255, start_x + 2 * cell + 145, y + 255), fill=GREEN, width=8)
    d.polygon([(start_x, y + 255), (start_x + 28, y + 238), (start_x + 28, y + 272)], fill=GREEN)
    d.polygon([(start_x + 2 * cell + 145, y + 255), (start_x + 2 * cell + 117, y + 238), (start_x + 2 * cell + 117, y + 272)], fill=GREEN)
    d.text((start_x + 75, y + 285), "word[0:3] -> 'hua'", font=F_H2, fill=GREEN)
    d.rounded_rectangle((300, 870, 1500, 1015), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw_text(d, "左闭右开：包含起点，不包含终点。好处是长度很好算：word[0:3] 的长度就是 3 - 0。", (370, 912), F_BODY, "#8A5A00", max_chars=44)
    save(im, "ch02_string_slice_ruler.png")


def list_workbench():
    im, d = canvas()
    title_block(d, "列表工作台：有顺序的数据，就像一排可调整的抽屉", "列表适合保存一串同类或相关的数据。它可以取、切、加、删、合并，也可以嵌套。")
    shadow_box(d, (120, 310, 1680, 805), fill="#FFFFFF")
    items = ["I", "love", "Python", "and", "data"]
    start_x = 245
    y = 420
    cell_w = 230
    for i, item in enumerate(items):
        x = start_x + i * cell_w
        rounded(d, (x, y, x + 190, y + 130), fill="#F8FAFC", outline=[BLUE, GREEN, ORANGE, PURPLE, CYAN][i], radius=18)
        d.text((x + 45, y + 36), item, font=F_H2, fill=INK)
        d.text((x + 82, y + 148), str(i), font=F_SMALL, fill=MUTED)
    ops = [
        ("索引", "my_list[1] -> 'love'", BLUE),
        ("切片", "my_list[0:2] -> ['I', 'love']", GREEN),
        ("追加", "my_list.append('!')", ORANGE),
        ("删除", "del my_list[3]", RED),
    ]
    for i, (title, code, color) in enumerate(ops):
        x = 205 + i * 390
        rounded(d, (x, 665, x + 330, 765), fill="#FFFFFF", outline=color, radius=18)
        pill(d, x + 20, 690, title, color, width=92)
        d.text((x + 125, 693), code, font=F_SMALL, fill=INK)
    d.rounded_rectangle((330, 910, 1470, 1030), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    draw_text(d, "列表口诀：位置从 0 开始，切片左闭右开；append 加到最后，del 删除指定位置。", (400, 945), F_BODY, "#28517A", max_chars=42)
    save(im, "ch02_list_workbench.png")


def nested_data_matryoshka():
    photo_plate("ch02_nested_data_matryoshka.png", "matryoshka_dolls.jpg")


def psychology_ebbinghaus_memory():
    photo_plate("ch02_psychology_ebbinghaus_memory.png", "hermann_ebbinghaus2.jpg")


def dictionary_card_catalog_photo():
    photo_plate("ch02_dictionary_card_catalog_photo.png", "copyright_card_catalog_drawer.jpg")


def punch_card_sorter_photo():
    photo_plate("ch02_punch_card_sorter_photo.png", "ibm_080_card_sorter.jpg")


def dict_mapping_card():
    im, d = canvas()
    title_block(d, "字典映射卡：用 key 找 value，像查学生档案", "列表靠位置，字典靠名字。只要 key 设计得清楚，代码就像查表一样自然。")
    shadow_box(d, (150, 310, 760, 855), fill="#FFFFFF")
    d.text((205, 360), "favorite_color", font=F_H2, fill=INK)
    pairs = [("小美", "粉色"), ("小明", "黄色"), ("小东", "绿色"), ("小红", "紫色")]
    for i, (key, value) in enumerate(pairs):
        y = 450 + i * 85
        rounded(d, (220, y, 390, y + 52), fill="#EEF6FF", outline=BLUE, radius=14)
        rounded(d, (520, y, 690, y + 52), fill="#F1FFF7", outline=GREEN, radius=14)
        d.text((260, y + 10), key, font=F_SMALL, fill=INK)
        d.text((560, y + 10), value, font=F_SMALL, fill=INK)
        arrow(d, (395, y + 26), (515, y + 26), width=4)
    shadow_box(d, (920, 310, 1650, 855), fill="#FFFFFF")
    d.text((970, 360), "四个基础动作", font=F_H2, fill=INK)
    actions = [
        ("查", "favorite_color['小美']", BLUE),
        ("增", "favorite_color['小红'] = '紫色'", GREEN),
        ("改", "favorite_color['小明'] = '绿色'", ORANGE),
        ("删", "del favorite_color['小东']", RED),
    ]
    for i, (tag, code, color) in enumerate(actions):
        y = 460 + i * 82
        pill(d, 990, y, tag, color, width=70)
        d.text((1090, y + 6), code, font=F_MONO, fill=INK)
    d.rounded_rectangle((330, 930, 1470, 1030), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw_text(d, "字典适合表达“谁对应什么”。例如学生姓名对应分数、单词对应释义、文件名对应路径。", (400, 962), F_BODY, "#8A5A00", max_chars=44)
    save(im, "ch02_dict_mapping_card.png")


def mini_project_dashboard():
    im, d = canvas()
    title_block(d, "本章小项目：把一份学习记录整理成数据结构", "学完类型以后，不要只会写零散例子；把它们组合起来，才会变成真正能用的小工具。")
    shadow_box(d, (120, 300, 1680, 865), fill="#FFFFFF")
    columns = [
        ("原始输入", "name = '小明'\nscore = 86\nmood = '稳定'", BLUE),
        ("整理成列表", "scores = [86, 92, 78]\n平均数、最高分\n都可以计算", GREEN),
        ("整理成字典", "student = {\n  'name': '小明',\n  'score': 86\n}", ORANGE),
        ("输出报告", "小明本周平均 85.3\n建议：继续保持\n写入 learning_log.txt", PURPLE),
    ]
    xs = [160, 555, 950, 1345]
    for i, (title, text, color) in enumerate(columns):
        x = xs[i]
        rounded(d, (x, 390, x + 315, 735), fill="#F8FAFC", outline=color, radius=22)
        pill(d, x + 32, 425, str(i + 1), color, width=70)
        d.text((x + 115, 425), title, font=F_H2, fill=INK)
        draw_text(d, text, (x + 35, 510), F_SMALL, MUTED, max_chars=18, line_gap=8)
        if i < 3:
            arrow(d, (x + 325, 560), (xs[i + 1] - 35, 560), width=5)
    d.rounded_rectangle((310, 930, 1490, 1030), radius=24, fill="#F1FFF7", outline=GREEN, width=3)
    draw_text(d, "项目标准：至少使用 str、bool、int/float、list、dict 五类数据，并能解释为什么这么选。", (380, 962), F_BODY, "#176342", max_chars=44)
    save(im, "ch02_mini_project_dashboard.png")


def type_decision_cards_preview():
    photo_plate("ch02_type_decision_cards_preview.png", "ch02_type_decision_cards_preview.png")


def type_compass_preview():
    photo_plate("ch02_type_compass_preview.png", "ch02_type_compass_preview.png")


def data_type_lab_receipt():
    src = ROOT / "output" / "ch02_data_type_lab_receipt.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch02_data_type_lab_receipt.png", optimize=True, quality=95)
    photo_plate("ch02_data_type_lab_receipt.png", "ch02_data_type_lab_receipt.png")


def stroop_dataset_pack():
    src = ROOT / "output" / "ch02_stroop_dataset_pack.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch02_stroop_dataset_pack.png", optimize=True, quality=95)
    photo_plate("ch02_stroop_dataset_pack.png", "ch02_stroop_dataset_pack.png")


def data_type_specimen_cabinet():
    src = ROOT / "output" / "ch02_data_type_specimen_cabinet.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch02_data_type_specimen_cabinet.png", optimize=True, quality=95)
    photo_plate("ch02_data_type_specimen_cabinet.png", "ch02_data_type_specimen_cabinet.png")


def data_type_runtime_evidence():
    src = ROOT / "output" / "ch02_data_type_runtime_evidence.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch02_data_type_runtime_evidence.png", optimize=True, quality=95)
    photo_plate("ch02_data_type_runtime_evidence.png", "ch02_data_type_runtime_evidence.png")


def powershell_data_type_run():
    photo_plate("ch02_powershell_data_type_run.png", "powershell_ch02_data_types_run.png")


def clean_header(d: ImageDraw.ImageDraw, title: str):
    d.rounded_rectangle((90, 72, 1710, 172), radius=28, fill="#FFFFFF", outline=LINE, width=2)
    d.text((130, 96), title, font=F_H2, fill=INK)


def mini_type_badge(d: ImageDraw.ImageDraw, xy, label: str, color: str):
    x1, y1, x2, y2 = xy
    shadow_box(d, xy, fill="#FFFFFF", outline=LINE, radius=24)
    d.ellipse((x1 + 44, y1 + 44, x1 + 116, y1 + 116), fill=color)
    d.text((x1 + 145, y1 + 56), label, font=F_H2, fill=INK)


def cover():
    im, d = canvas()
    clean_header(d, "Python 数据类型：给信息选择容器")
    rounded(d, (155, 285, 1645, 820), fill="#FFFFFF", outline=LINE, radius=34)
    colors = [BLUE, GREEN, ORANGE, PURPLE, CYAN, RED]
    labels = ["bool", "int", "float", "str", "list", "dict"]
    positions = [(270, 380), (560, 380), (850, 380), (1140, 380), (705, 610), (995, 610)]
    for (x, y), label, color in zip(positions, labels, colors):
        d.rounded_rectangle((x, y, x + 190, y + 120), radius=28, fill="#F8FAFC", outline=color, width=5)
        d.ellipse((x + 28, y + 32, x + 82, y + 86), fill=color)
        d.text((x + 102, y + 42), label, font=F_H2, fill=INK)
    save(im, "ch02_cover.png")


def roadmap():
    im, d = canvas()
    clean_header(d, "本章路线：从标签到数据结构")
    centers = [(250, 360), (560, 360), (870, 360), (1180, 360), (1490, 360), (870, 700)]
    colors = [BLUE, GREEN, ORANGE, PURPLE, CYAN, RED]
    labels = ["变量", "bool", "number", "str", "list", "dict"]
    for a, b in zip(centers, centers[1:5]):
        arrow(d, (a[0] + 110, a[1]), (b[0] - 110, b[1]), width=5)
    arrow(d, (1490, 470), (980, 665), width=5)
    for (x, y), label, color in zip(centers, labels, colors):
        d.ellipse((x - 96, y - 96, x + 96, y + 96), fill="#FFFFFF", outline=color, width=7)
        d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=color)
        d.text((x - 54, y + 120), label, font=F_BODY, fill=INK)
    save(im, "ch02_roadmap.png")


def variable_label_metaphor():
    im, d = canvas()
    clean_header(d, "变量像标签，不像盒子")
    shadow_box(d, (160, 290, 780, 815), fill="#FFFFFF", outline=LINE, radius=32)
    for x, color, label in [(305, BLUE, "a"), (515, GREEN, "b")]:
        d.rounded_rectangle((x, 430, x + 150, 610), radius=24, fill="#EEF2FF", outline=color, width=6)
        d.text((x + 55, 495), label, font=F_TITLE, fill=color)
    shadow_box(d, (970, 290, 1640, 815), fill="#FFFFFF", outline=LINE, radius=32)
    d.ellipse((1215, 455, 1415, 655), fill="#FFF7E8", outline=ORANGE, width=7)
    d.text((1280, 515), "2", font=F_TITLE, fill=INK)
    for y, color, label in [(435, BLUE, "a"), (600, GREEN, "b")]:
        d.rounded_rectangle((1040, y, 1140, y + 62), radius=22, fill=color)
        d.text((1077, y + 9), label, font=F_BODY, fill="white")
        arrow(d, (1145, y + 31), (1215, 555), width=5)
    save(im, "ch02_variable_label_metaphor.png")


def data_type_atlas():
    im, d = canvas()
    clean_header(d, "数据类型地图")
    items = [
        ((170, 300, 470, 470), "bool", BLUE),
        ((565, 300, 865, 470), "int / float", GREEN),
        ((960, 300, 1260, 470), "str", ORANGE),
        ((1335, 300, 1635, 470), "list", PURPLE),
        ((365, 630, 665, 800), "tuple", CYAN),
        ((755, 630, 1055, 800), "dict", RED),
        ((1145, 630, 1445, 800), "None", GOLD),
    ]
    for xy, label, color in items:
        mini_type_badge(d, xy, label, color)
    save(im, "ch02_data_type_atlas.png")


def bool_logic_switchboard():
    im, d = canvas()
    clean_header(d, "布尔逻辑：开关、合流、反转")
    gates = [
        ((170, 350, 520, 650), "and", BLUE, [1, 1], 1),
        ((725, 350, 1075, 650), "or", GREEN, [1, 0], 1),
        ((1280, 350, 1630, 650), "not", ORANGE, [0], 1),
    ]
    for xy, label, color, inputs, output in gates:
        x1, y1, x2, y2 = xy
        shadow_box(d, xy, fill="#FFFFFF", outline=LINE, radius=32)
        d.text((x1 + 125, y1 + 40), label, font=F_H2, fill=INK)
        for i, value in enumerate(inputs):
            yy = y1 + 130 + i * 72
            d.ellipse((x1 + 70, yy, x1 + 126, yy + 56), fill=GREEN if value else RED)
            arrow(d, (x1 + 135, yy + 28), (x1 + 210, y1 + 180), width=5)
        d.ellipse((x2 - 120, y1 + 150, x2 - 50, y1 + 220), fill=GREEN if output else RED)
    save(im, "ch02_bool_logic_switchboard.png")


def string_slice_ruler():
    im, d = canvas()
    clean_header(d, "字符串切片：用边界取片段")
    word = "huawei"
    start_x = 335
    y = 420
    cell = 170
    for i, ch in enumerate(word):
        x = start_x + i * cell
        rounded(d, (x, y, x + 145, y + 145), fill="#FFFFFF", outline=BLUE, radius=18)
        d.text((x + 48, y + 38), ch, font=F_TITLE, fill=INK)
        d.text((x + 56, y - 45), str(i), font=F_BODY, fill=BLUE)
    d.line((start_x, y + 235, start_x + 2 * cell + 145, y + 235), fill=GREEN, width=10)
    d.polygon([(start_x, y + 235), (start_x + 28, y + 218), (start_x + 28, y + 252)], fill=GREEN)
    d.polygon([(start_x + 2 * cell + 145, y + 235), (start_x + 2 * cell + 117, y + 218), (start_x + 2 * cell + 117, y + 252)], fill=GREEN)
    d.text((start_x + 90, y + 270), "word[0:3]", font=F_H2, fill=GREEN)
    save(im, "ch02_string_slice_ruler.png")


def string_material_workbench():
    im, d = canvas(1800, 1120)
    d.rounded_rectangle((95, 95, 1705, 1015), radius=40, fill="#FFFFFF", outline=LINE, width=3)
    d.rounded_rectangle((160, 180, 1640, 930), radius=32, fill="#F8FAFC", outline="#E6ECF5", width=3)

    # Notebook sheet with abstract text lines.
    d.rounded_rectangle((235, 250, 690, 820), radius=26, fill="#FFFDF7", outline="#E4D7B6", width=3)
    for y in range(320, 760, 62):
        d.line((290, y, 625, y), fill="#D5C79F", width=4)
    d.ellipse((290, 280, 332, 322), fill=BLUE)
    d.ellipse((350, 280, 392, 322), fill=GREEN)

    # Loose stimulus cards.
    card_specs = [
        (805, 275, 1115, 410, RED),
        (1170, 300, 1480, 435, BLUE),
        (825, 510, 1135, 645, PURPLE),
        (1180, 545, 1490, 680, ORANGE),
    ]
    for x1, y1, x2, y2, color in card_specs:
        d.rounded_rectangle((x1 + 9, y1 + 12, x2 + 9, y2 + 12), radius=22, fill="#D8DEE9")
        d.rounded_rectangle((x1, y1, x2, y2), radius=22, fill="#FFFFFF", outline=color, width=5)
        d.rectangle((x1 + 30, y1 + 34, x2 - 30, y1 + 56), fill=color)
        d.line((x1 + 35, y1 + 82, x2 - 40, y1 + 82), fill="#CBD5E1", width=5)
        d.line((x1 + 35, y1 + 108, x1 + 190, y1 + 108), fill="#CBD5E1", width=5)

    # ID badge and barcode-like marks.
    d.rounded_rectangle((270, 850, 630, 960), radius=26, fill="#FFFFFF", outline=CYAN, width=5)
    d.ellipse((305, 878, 365, 938), fill=CYAN)
    bx = 410
    for w in [6, 10, 5, 14, 6, 9, 4, 12, 7, 5]:
        d.rectangle((bx, 876, bx + w, 938), fill=NAVY)
        bx += w + 10

    # Magnifier over text material.
    d.ellipse((745, 760, 920, 935), outline="#475569", width=12)
    d.line((890, 900, 1015, 995), fill="#475569", width=16)
    d.line((790, 820, 875, 820), fill="#94A3B8", width=6)
    d.line((790, 860, 850, 860), fill="#94A3B8", width=6)

    # Output folder and label strips.
    d.rounded_rectangle((1140, 780, 1535, 970), radius=30, fill="#EAF7F0", outline=GREEN, width=5)
    d.polygon([(1140, 780), (1285, 780), (1335, 825), (1535, 825), (1535, 970), (1140, 970)], fill="#EAF7F0", outline=GREEN)
    for i, color in enumerate([BLUE, ORANGE, PURPLE]):
        y = 850 + i * 36
        d.rounded_rectangle((1205, y, 1465, y + 18), radius=9, fill=color)

    save(im, "ch02_string_material_workbench.png")


def list_workbench():
    im, d = canvas()
    clean_header(d, "列表：一排有顺序的抽屉")
    items = ["0", "1", "2", "3", "4"]
    colors = [BLUE, GREEN, ORANGE, PURPLE, CYAN]
    start_x, y, cell_w = 300, 390, 240
    for i, (item, color) in enumerate(zip(items, colors)):
        x = start_x + i * cell_w
        rounded(d, (x, y, x + 180, y + 150), fill="#FFFFFF", outline=color, radius=22)
        d.ellipse((x + 55, y + 32, x + 125, y + 102), fill=color)
        d.text((x + 76, y + 112), item, font=F_BODY, fill=INK)
    for i in range(4):
        arrow(d, (start_x + i * cell_w + 184, y + 75), (start_x + (i + 1) * cell_w - 8, y + 75), width=4)
    save(im, "ch02_list_workbench.png")


def dict_mapping_card():
    im, d = canvas()
    clean_header(d, "字典：用 key 找 value")
    keys = ["name", "score", "done", "note"]
    values = ["小明", "86", "True", "None"]
    colors = [BLUE, GREEN, ORANGE, PURPLE]
    for i, (key, value, color) in enumerate(zip(keys, values, colors)):
        y = 310 + i * 145
        rounded(d, (360, y, 650, y + 90), fill="#FFFFFF", outline=color, radius=24)
        rounded(d, (1080, y, 1370, y + 90), fill="#FFFFFF", outline=color, radius=24)
        d.text((410, y + 25), key, font=F_BODY, fill=INK)
        d.text((1130, y + 25), value, font=F_BODY, fill=INK)
        arrow(d, (660, y + 45), (1070, y + 45), color=color, width=6)
    save(im, "ch02_dict_mapping_card.png")


def mini_project_dashboard():
    im, d = canvas()
    clean_header(d, "小项目：学习记录整理器")
    centers = [(280, 520), (650, 520), (1020, 520), (1390, 520)]
    labels = ["输入", "列表", "字典", "报告"]
    colors = [BLUE, GREEN, ORANGE, PURPLE]
    for i, ((x, y), label, color) in enumerate(zip(centers, labels, colors)):
        d.rounded_rectangle((x - 120, y - 120, x + 120, y + 120), radius=32, fill="#FFFFFF", outline=color, width=6)
        d.ellipse((x - 38, y - 55, x + 38, y + 21), fill=color)
        d.text((x - 45, y + 50), label, font=F_BODY, fill=INK)
        if i < 3:
            arrow(d, (x + 130, y), (centers[i + 1][0] - 130, y), width=6)
    save(im, "ch02_mini_project_dashboard.png")


def error_clue_cards():
    im, d = canvas()
    positions = [(330, 360), (680, 360), (1030, 360), (1380, 360), (505, 720), (855, 720), (1205, 720)]
    colors = [RED, ORANGE, PURPLE, BLUE, GREEN, CYAN, GOLD]
    for i, ((x, y), color) in enumerate(zip(positions, colors)):
        shadow_box(d, (x - 125, y - 95, x + 125, y + 95), fill="#FFFFFF", outline=LINE, radius=26)
        if i == 0:
            d.polygon([(x, y - 58), (x + 62, y + 50), (x - 62, y + 50)], outline=color, fill=None)
            d.line((x, y - 25, x, y + 18), fill=color, width=9)
            d.ellipse((x - 6, y + 32, x + 6, y + 44), fill=color)
        elif i == 1:
            d.arc((x - 70, y - 60, x - 10, y + 60), 95, 265, fill=color, width=9)
            d.arc((x + 10, y - 60, x + 70, y + 60), -85, 85, fill=color, width=9)
        elif i == 2:
            d.ellipse((x - 72, y - 44, x + 4, y + 32), outline=color, width=9)
            d.line((x - 5, y - 5, x + 72, y + 72), fill=color, width=9)
            d.line((x + 35, y + 35, x + 62, y + 8), fill=color, width=8)
        elif i == 3:
            for j, width in enumerate([122, 92, 64]):
                yy = y - 48 + j * 44
                d.rounded_rectangle((x - width // 2, yy, x + width // 2, yy + 28), radius=14, outline=color, width=7)
        elif i == 4:
            d.polygon([(x, y - 66), (x + 68, y - 28), (x + 68, y + 40), (x, y + 78), (x - 68, y + 40), (x - 68, y - 28)], outline=color, fill=None)
            d.line((x - 68, y - 28, x, y + 10, x + 68, y - 28), fill=color, width=8)
            d.line((x, y + 10, x, y + 78), fill=color, width=8)
        elif i == 5:
            d.rounded_rectangle((x - 75, y - 35, x + 75, y + 62), radius=18, outline=color, width=8)
            d.line((x - 75, y - 35, x - 32, y - 66, x + 12, y - 66, x + 40, y - 35), fill=color, width=8)
        else:
            d.ellipse((x - 56, y - 56, x + 56, y + 56), outline=color, width=8)
            d.line((x - 32, y, x + 32, y), fill=color, width=8)
            d.line((x, y - 32, x, y + 32), fill=color, width=8)
    save(im, "ch02_error_clue_cards.png")


def type_to_file_bridge():
    im, d = canvas()
    y = 560
    nodes = [(230, BLUE), (470, GREEN), (710, ORANGE), (950, PURPLE)]
    for i, (x, color) in enumerate(nodes):
        d.ellipse((x - 76, y - 76, x + 76, y + 76), fill="#FFFFFF", outline=color, width=8)
        if i == 0:
            d.line((x - 36, y, x + 36, y), fill=color, width=8)
            d.line((x - 36, y - 28, x + 36, y - 28), fill=color, width=8)
            d.line((x - 36, y + 28, x + 36, y + 28), fill=color, width=8)
        elif i == 1:
            for j in range(4):
                d.rounded_rectangle((x - 46 + j * 28, y - 42, x - 28 + j * 28, y + 42), radius=8, outline=color, width=6)
        elif i == 2:
            d.rounded_rectangle((x - 48, y - 50, x + 48, y + 50), radius=18, outline=color, width=8)
            d.line((x - 22, y - 18, x + 22, y - 18), fill=color, width=7)
            d.line((x - 22, y + 18, x + 22, y + 18), fill=color, width=7)
        else:
            d.ellipse((x - 44, y - 44, x + 44, y + 44), outline=color, width=8)
            d.line((x - 25, y, x - 2, y + 25, x + 32, y - 28), fill=color, width=8)
        if i < len(nodes) - 1:
            arrow(d, (x + 90, y), (nodes[i + 1][0] - 90, y), width=6)
    arrow(d, (1045, y), (1215, y), width=7)
    d.polygon([(1220, y - 110), (1390, y - 40), (1390, y + 40), (1220, y + 110)], outline=CYAN, fill=None)
    arrow(d, (1405, y), (1535, y), width=7)
    d.rounded_rectangle((1535, y - 92, 1685, y + 92), radius=24, outline=GOLD, width=8)
    d.line((1575, y - 38, 1645, y - 38), fill=GOLD, width=7)
    d.line((1575, y, 1645, y), fill=GOLD, width=7)
    d.line((1575, y + 38, 1645, y + 38), fill=GOLD, width=7)
    save(im, "ch02_type_to_file_bridge.png")


def practice_workbench():
    im, d = canvas()
    positions = [(330, 360), (680, 360), (1030, 360), (1380, 360), (500, 725), (850, 725), (1200, 725)]
    colors = [BLUE, ORANGE, PURPLE, GREEN, CYAN, GOLD, RED]
    for i, ((x, y), color) in enumerate(zip(positions, colors)):
        shadow_box(d, (x - 122, y - 98, x + 122, y + 98), fill="#FFFFFF", outline=LINE, radius=26)
        if i == 0:
            d.rounded_rectangle((x - 58, y - 42, x + 58, y + 42), radius=18, outline=color, width=8)
            d.line((x - 32, y, x + 32, y), fill=color, width=8)
            d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=color)
        elif i == 1:
            for j, ch_y in enumerate([y - 36, y, y + 36]):
                d.line((x - 52, ch_y, x + 52, ch_y), fill=color, width=8)
                d.ellipse((x - 72, ch_y - 7, x - 58, ch_y + 7), fill=color)
        elif i == 2:
            for j in range(4):
                d.rounded_rectangle((x - 68 + j * 40, y - 46, x - 34 + j * 40, y + 46), radius=10, outline=color, width=7)
        elif i == 3:
            for yy in [y - 42, y, y + 42]:
                d.rounded_rectangle((x - 62, yy - 18, x + 62, yy + 18), radius=12, outline=color, width=7)
        elif i == 4:
            d.ellipse((x - 62, y - 62, x + 62, y + 62), outline=color, width=8)
            d.line((x, y, x + 42, y - 38), fill=color, width=8)
            d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color)
        elif i == 5:
            d.rounded_rectangle((x - 58, y - 58, x + 58, y + 58), radius=20, outline=color, width=8)
            d.line((x - 30, y - 20, x + 30, y - 20), fill=color, width=7)
            d.line((x - 30, y + 10, x + 30, y + 10), fill=color, width=7)
            d.line((x - 30, y + 40, x + 12, y + 40), fill=color, width=7)
        else:
            d.ellipse((x - 56, y - 56, x + 56, y + 56), outline=color, width=8)
            d.line((x - 26, y, x - 4, y + 25, x + 36, y - 30), fill=color, width=8)
        if i < 3:
            arrow(d, (x + 128, y), (positions[i + 1][0] - 128, y), width=5)
        if i in {4, 5}:
            arrow(d, (x + 128, y), (positions[i + 1][0] - 128, y), width=5)
    save(im, "ch02_practice_workbench.png")


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
    print("Generated ch02 formal visuals.")


if __name__ == "__main__":
    main()
