from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
if not (ROOT / "assets" / "ch03").exists():
    ROOT = Path(__file__).resolve().parents[1]

ASSET_DIR = ROOT / "assets" / "ch03"
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
    d.text((x + 22, y + 7), text, font=F_SMALL, fill="white")


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
    d.text((118, 92), "第 3 章  文件读写与文件夹管理", font=F_TITLE, fill="white")
    d.text((124, 164), "让 Python 真的碰到电脑里的资料：读、写、找、搬、删。", font=F_SUBTITLE, fill="#D6E1F5")
    shadow_box(d, (150, 300, 1650, 825), fill="#FFFFFF")
    rounded(d, (690, 380, 1110, 690), fill="#111827", outline="#111827", radius=20)
    code = [
        "from pathlib import Path",
        "p = Path('data/note.txt')",
        "text = p.read_text(encoding='utf-8')",
        "print(text)",
    ]
    for i, line in enumerate(code):
        d.text((735, 420 + i * 58), line, font=F_MONO, fill=["#A7F3D0", "#FDE68A", "#93C5FD", "#C4B5FD"][i])
    topics = [
        ((210, 375, 570, 500), "OPEN", "打开", "让程序拿到文件句柄", BLUE),
        ((210, 600, 570, 725), "READ", "读取", "把内容读进变量", GREEN),
        ((1230, 375, 1590, 500), "WRITE", "写入", "把结果保存成文件", ORANGE),
        ((1230, 600, 1590, 725), "MOVE", "管理", "复制、移动、删除", PURPLE),
    ]
    for xy, tag, title, desc, color in topics:
        card(d, xy, tag, title, desc, color, tag_width=112)
    d.text((175, 912), "本章目标：会安全读写文本文件，能创建项目目录，并能用 Python 批量整理文件夹。", font=F_SUBTITLE, fill=MUTED)
    save(im, "ch03_cover.png")


def roadmap():
    im, d = canvas()
    title_block(d, "第 3 章知识路线图", "文件不是“在电脑里”这么简单，它在某条路径里；路径理清，读写才会稳定。")
    steps = [
        ("1", "路径", "相对路径 / 绝对路径\nPath.cwd()", BLUE),
        ("2", "打开文件", "open(name, mode)\n文件句柄", GREEN),
        ("3", "读取", "read / readline\nreadlines / for line", ORANGE),
        ("4", "写入", "write / writelines\nencoding='utf-8'", PURPLE),
        ("5", "文件管理", "remove / copyfile\nmove", CYAN),
        ("6", "文件夹管理", "mkdir / walk\ncopytree / rmtree", RED),
    ]
    positions = [(120, 300), (610, 300), (1100, 300), (1100, 620), (610, 620), (120, 620)]
    for i in range(len(positions) - 1):
        x1, y1 = positions[i]
        x2, y2 = positions[i + 1]
        arrow(d, (x1 + 395, y1 + 105), (x2 - 35 if x2 > x1 else x2 + 435, y2 + 105))
    for (num, title, desc, color), (x, y) in zip(steps, positions):
        card(d, (x, y, x + 430, y + 220), num, title, desc, color, tag_width=92)
    d.rounded_rectangle((360, 925, 1440, 1038), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    draw_text(d, "通关标准：能创建 data/output 目录，读入一个文本文件，处理后写出结果，并解释当前工作目录。", (430, 957), F_BODY, "#28517A", max_chars=42, line_gap=7)
    save(im, "ch03_roadmap.png")


def file_io_pipeline():
    im, d = canvas()
    title_block(d, "文件读写流水线：从磁盘到变量，再从变量回到磁盘", "读写文件不是魔法，它只是让电脑里的内容进入程序，再把程序结果保存回去。")
    steps = [
        ("DISK", "磁盘文件", "data/raw.txt\n真实内容躺在文件里", BLUE),
        ("OPEN", "打开文件", "open(...)\n或 Path.read_text()", GREEN),
        ("VAR", "变量处理", "text / lines\n查找、清洗、统计", ORANGE),
        ("OUT", "写出结果", "output/report.txt\n让结果留下来", PURPLE),
    ]
    xs = [140, 545, 950, 1355]
    for i, (tag, title, desc, color) in enumerate(steps):
        card(d, (xs[i], 410, xs[i] + 320, 680), tag, title, desc, color, tag_width=105)
        if i < len(steps) - 1:
            arrow(d, (xs[i] + 330, 545), (xs[i + 1] - 35, 545), width=5)
    d.rounded_rectangle((300, 850, 1500, 1005), radius=24, fill="#F1FFF7", outline=GREEN, width=3)
    draw_text(d, "记住：读文件，是把外面的文字请进程序；写文件，是把程序的结果送回世界。", (380, 895), F_BODY, "#176342", max_chars=42)
    save(im, "ch03_file_io_pipeline.png")


def archive_box_project_story():
    photo_plate("ch03_archive_box_project_story.png", "archival_carton_01.jpg")


def information_trail_vannevar_bush():
    photo_plate("ch03_information_trail_vannevar_bush.png", "vannevar_bush_portrait.jpg")


def powershell_file_operations_run():
    photo_plate("ch03_powershell_file_operations_run.png", "powershell_ch03_file_operations_run.png")


def open_mode_matrix():
    im, d = canvas()
    title_block(d, "open() 模式速查表：不同钥匙，开不同门", "mode 写错，轻则读不到，重则覆盖原文件。新手要先认识这几把钥匙。")
    modes = [
        ("r", "只读", "文件必须存在\n适合读取资料", BLUE),
        ("w", "写入", "会覆盖旧内容\n适合生成新结果", RED),
        ("a", "追加", "写到文件末尾\n适合日志记录", GREEN),
        ("x", "新建", "文件已存在会报错\n适合避免误覆盖", ORANGE),
        ("b", "二进制", "图片、音频等\n常与 rb/wb 组合", PURPLE),
        ("+", "读写", "读写都要\n初学少用，谨慎", CYAN),
    ]
    positions = [(100, 300), (650, 300), (1200, 300), (100, 620), (650, 620), (1200, 620)]
    for (mode, title, desc, color), (x, y) in zip(modes, positions):
        shadow_box(d, (x, y, x + 500, y + 220))
        pill(d, x + 32, y + 32, mode, color, width=76)
        d.text((x + 135, y + 26), title, font=F_H2, fill=INK)
        draw_text(d, desc, (x + 36, y + 98), F_BODY, MUTED, max_chars=22)
    d.rounded_rectangle((300, 920, 1500, 1030), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw_text(d, "安全建议：不确定时先用 r 读；写文件前确认输出路径，避免把原始数据覆盖掉。", (380, 954), F_BODY, "#8A5A00", max_chars=44)
    save(im, "ch03_open_mode_matrix.png")


def rosetta_encoding_story():
    photo_plate("ch03_rosetta_encoding_story.png", "rosetta_stone.jpg")


def with_context_door():
    im, d = canvas()
    title_block(d, "with open()：像会自动关门的阅览室", "open 后忘记 close，是文件读写里最常见也最隐蔽的坏习惯。with 会帮你把门关上。")
    shadow_box(d, (120, 315, 790, 830), fill="#FFFFFF")
    d.text((180, 360), "手动开关门", font=F_H2, fill=INK)
    rounded(d, (235, 475, 520, 685), fill="#EEF2FF", outline=BLUE, radius=18)
    d.text((280, 540), "open()", font=F_H2, fill=BLUE)
    d.text((290, 595), "read()", font=F_BODY, fill=INK)
    d.text((285, 650), "close()", font=F_BODY, fill=GREEN)
    draw_text(d, "如果中间报错，close() 可能执行不到。", (185, 735), F_BODY, MUTED, max_chars=24)

    shadow_box(d, (980, 315, 1680, 830), fill="#FFFFFF")
    d.text((1040, 360), "with 自动关门", font=F_H2, fill=INK)
    rounded(d, (1070, 480, 1585, 690), fill="#111827", outline="#111827", radius=18)
    code = [
        "with open(path) as f:",
        "    text = f.read()",
        "# 离开缩进后自动关闭",
    ]
    for i, line in enumerate(code):
        d.text((1115, 525 + i * 48), line, font=F_MONO, fill=["#A7F3D0", "#FDE68A", "#93C5FD"][i])
    draw_text(d, "推荐写法：代码更短，也更安全。文件读写优先用 with。", (1045, 735), F_BODY, MUTED, max_chars=30)
    d.rounded_rectangle((310, 930, 1490, 1030), radius=24, fill="#F1FFF7", outline=GREEN, width=3)
    draw_text(d, "记住：with 不是高级装饰，而是文件读写的安全带。", (390, 962), F_BODY, "#176342", max_chars=38)
    save(im, "ch03_with_context_door.png")


def read_methods_comparison():
    im, d = canvas()
    title_block(d, "读取方法对比：read、readline、readlines、逐行循环", "读取文件有几种姿势。选哪一种，取决于你想一次读多少。")
    methods = [
        ("read()", "一次读全部", "适合小文件\n得到一个字符串", BLUE),
        ("readline()", "一次读一行", "适合只看开头\n每次向下移动一行", GREEN),
        ("readlines()", "全部行列表", "适合小文件\n得到 list[str]", ORANGE),
        ("for line in f", "逐行处理", "适合大文件\n最常用也最稳", PURPLE),
    ]
    xs = [115, 520, 925, 1330]
    for i, (name, title, desc, color) in enumerate(methods):
        shadow_box(d, (xs[i], 335, xs[i] + 355, 725))
        pill(d, xs[i] + 30, 370, str(i + 1), color, width=72)
        d.text((xs[i] + 120, 365), name, font=F_H2, fill=INK)
        d.text((xs[i] + 35, 450), title, font=F_BODY, fill=color)
        draw_text(d, desc, (xs[i] + 35, 505), F_BODY, MUTED, max_chars=16)
    d.rounded_rectangle((330, 875, 1470, 1025), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    draw_text(d, "建议：先掌握 read_text() 和 for line in f；能处理小文件，也能迁移到大文件。", (400, 920), F_BODY, "#28517A", max_chars=42)
    save(im, "ch03_read_methods_comparison.png")


def path_map():
    im, d = canvas()
    title_block(d, "路径地图：当前工作目录决定 Python 从哪里找文件", "很多 FileNotFoundError 不是文件丢了，而是你站错房间找东西。")
    shadow_box(d, (120, 300, 1680, 835), fill="#FFFFFF")
    boxes = [
        ((210, 415, 520, 540), "项目根目录", "my_project/", BLUE),
        ((650, 335, 960, 460), "数据目录", "data/raw.txt", GREEN),
        ((650, 575, 960, 700), "代码目录", "code/main.py", ORANGE),
        ((1090, 415, 1400, 540), "输出目录", "output/report.txt", PURPLE),
    ]
    for xy, title, desc, color in boxes:
        rounded(d, xy, fill="#F8FAFC", outline=color, radius=18)
        x1, y1, x2, y2 = xy
        d.text((x1 + 32, y1 + 28), title, font=F_H2, fill=INK)
        d.text((x1 + 32, y1 + 82), desc, font=F_SMALL, fill=MUTED)
    arrow(d, (520, 478), (650, 397), width=5)
    arrow(d, (520, 478), (650, 637), width=5)
    arrow(d, (960, 397), (1090, 478), width=5)
    d.rounded_rectangle((350, 900, 1450, 1030), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw_text(d, "排错口诀：先 print(Path.cwd())，确认自己站在哪个房间；再检查相对路径从这里能不能走到文件。", (420, 940), F_BODY, "#8A5A00", max_chars=42)
    save(im, "ch03_path_map.png")


def card_filing_cabinet_path_index():
    photo_plate("ch03_card_filing_cabinet_path_index.png", "card_filing_cabinet.jpg")


def archive_storage_shelves():
    photo_plate("ch03_archive_storage_shelves.png", "archive_storage_unsplash.jpg")


def folder_tree_operations():
    im, d = canvas()
    title_block(d, "文件夹管理：创建、遍历、删除、复制、移动", "文件夹操作像整理书架：先建架子，再扫一遍目录，最后决定搬、复制还是清空。")
    ops = [
        ("mkdir", "创建目录", "Path('data').mkdir()", BLUE),
        ("walk", "遍历目录", "os.walk(path)", GREEN),
        ("copy", "复制文件夹", "shutil.copytree()", ORANGE),
        ("move", "移动文件夹", "shutil.move()", PURPLE),
        ("delete", "删除目录", "rmdir / rmtree", RED),
    ]
    xs = [90, 425, 760, 1095, 1430]
    for i, (tag, title, code, color) in enumerate(ops):
        shadow_box(d, (xs[i], 380, xs[i] + 285, 690))
        pill(d, xs[i] + 28, 420, tag, color, width=112)
        d.text((xs[i] + 32, 495), title, font=F_H2, fill=INK)
        draw_text(d, code, (xs[i] + 32, 560), F_SMALL, MUTED, max_chars=16)
        if i < len(ops) - 1:
            arrow(d, (xs[i] + 292, 535), (xs[i + 1] - 30, 535), width=4)
    d.rounded_rectangle((285, 850, 1515, 1018), radius=24, fill="#F1FFF7", outline=GREEN, width=3)
    draw_text(d, "安全提醒：删除目录前先打印将要删除的路径。尤其是 shutil.rmtree()，它不会替你心疼文件。", (360, 895), F_BODY, "#176342", max_chars=44)
    save(im, "ch03_folder_tree_operations.png")


def file_size_chart():
    im, d = canvas()
    title_block(d, "文件夹体检图表：用 Python 统计不同文件大小", "这是一张由脚本生成的结果图：遍历目录后，把结果画出来，文件管理就从盲找变成观察。")
    shadow_box(d, (145, 305, 1220, 875), fill="#FFFFFF")
    files = ["raw.txt", "clean.csv", "plot.png", "report.md", "backup.zip"]
    sizes = [12, 34, 82, 28, 64]
    colors = [BLUE, GREEN, ORANGE, PURPLE, RED]
    x0, y0 = 280, 780
    max_h = 360
    bar_w = 105
    gap = 70
    for i, (name, size, color) in enumerate(zip(files, sizes, colors)):
        x = x0 + i * (bar_w + gap)
        h = int(size / 90 * max_h)
        d.rounded_rectangle((x, y0 - h, x + bar_w, y0), radius=14, fill=color)
        d.text((x + 20, y0 - h - 38), f"{size}KB", font=F_SMALL, fill=INK)
        d.text((x - 10, y0 + 22), name, font=F_TINY, fill=MUTED)
    d.line((230, y0, 1080, y0), fill="#94A3B8", width=3)
    d.text((250, 385), "文件大小分布", font=F_H2, fill=INK)
    d.text((250, 430), "示例数据：遍历文件夹后得到的文件大小", font=F_SMALL, fill=MUTED)
    shadow_box(d, (1285, 345, 1645, 820), fill="#FFFFFF")
    d.text((1325, 390), "怎么使用", font=F_H2, fill=INK)
    tips = [
        "先用 os.walk 收集路径",
        "再用 stat().st_size",
        "取得文件大小",
        "最后把结果写入报告",
        "这就是文件管理小项目",
    ]
    yy = 465
    for tip in tips:
        d.text((1332, yy), "•", font=F_H2, fill=BLUE)
        yy = draw_text(d, tip, (1370, yy), F_SMALL, MUTED, max_chars=16, line_gap=8) + 16
    save(im, "ch03_file_size_chart.png")


def safe_delete_warning():
    im, d = canvas()
    title_block(d, "删除操作安全卡：先看路径，再动手", "文件删除很快，恢复很慢。写删除代码时，谨慎不是胆小，是专业。")
    shadow_box(d, (150, 300, 760, 835), fill="#FFFFFF")
    d.text((205, 360), "高风险写法", font=F_H2, fill=RED)
    rounded(d, (210, 465, 700, 650), fill="#FFF1F2", outline=RED, radius=18)
    d.text((245, 520), "shutil.rmtree(path)", font=F_MONO, fill=INK)
    draw_text(d, "直接删除整个目录。路径错了，后果会很扎心。", (210, 710), F_BODY, MUTED, max_chars=22)

    shadow_box(d, (950, 300, 1650, 835), fill="#FFFFFF")
    d.text((1005, 360), "安全流程", font=F_H2, fill=GREEN)
    steps = [
        ("1", "打印路径", BLUE),
        ("2", "确认在项目目录内", GREEN),
        ("3", "先移动到 trash", ORANGE),
        ("4", "最后再清理", PURPLE),
    ]
    for i, (num, text, color) in enumerate(steps):
        y = 450 + i * 82
        pill(d, 1015, y, num, color, width=70)
        d.text((1110, y + 6), text, font=F_BODY, fill=INK)
    d.rounded_rectangle((330, 930, 1470, 1030), radius=24, fill="#FFF7E8", outline="#F2B84B", width=3)
    draw_text(d, "记住：删除前多打印一行路径，胜过删除后写一百行忏悔。", (405, 962), F_BODY, "#8A5A00", max_chars=38)
    save(im, "ch03_safe_delete_warning.png")


def mini_project_archiver():
    im, d = canvas()
    title_block(d, "本章小项目：把杂乱资料整理成项目档案", "文件管理不是为了炫技，而是把真实资料变成可以复现、可以提交、可以分享的结构。")
    columns = [
        ("原始资料", "downloads/\n一堆 txt/csv/png", BLUE),
        ("扫描文件", "os.walk()\n收集路径和大小", GREEN),
        ("分类复制", "shutil.copyfile()\n按类型放进目录", ORANGE),
        ("生成报告", "output/report.md\n记录整理结果", PURPLE),
    ]
    xs = [155, 550, 945, 1340]
    for i, (title, text, color) in enumerate(columns):
        shadow_box(d, (xs[i], 390, xs[i] + 320, 735))
        pill(d, xs[i] + 32, 425, str(i + 1), color, width=70)
        d.text((xs[i] + 115, 425), title, font=F_H2, fill=INK)
        draw_text(d, text, (xs[i] + 35, 510), F_SMALL, MUTED, max_chars=18, line_gap=8)
        if i < 3:
            arrow(d, (xs[i] + 330, 560), (xs[i + 1] - 35, 560), width=5)
    d.rounded_rectangle((310, 910, 1490, 1030), radius=24, fill="#F1FFF7", outline=GREEN, width=3)
    draw_text(d, "项目标准：不覆盖原始资料；所有输出进入 output；整理过程能重复运行。", (380, 948), F_BODY, "#176342", max_chars=44)
    save(im, "ch03_mini_project_archiver.png")


def check_mark(d, x, y, color):
    d.line((x - 28, y, x - 8, y + 22, x + 34, y - 34), fill=color, width=11, joint="curve")


def magnifier_icon(d, x, y, color):
    d.ellipse((x - 52, y - 52, x + 52, y + 52), outline=color, width=8)
    d.line((x + 38, y + 38, x + 90, y + 90), fill=color, width=10)


def terminal_icon(d, x, y, color):
    rounded(d, (x - 92, y - 62, x + 92, y + 62), fill="#111827", outline=color, radius=16, width=5)
    d.line((x - 55, y - 18, x - 28, y, x - 55, y + 18), fill="#A7F3D0", width=7)
    d.line((x - 10, y + 28, x + 52, y + 28), fill="#93C5FD", width=7)


def window_icon(d, x, y, color):
    rounded(d, (x - 112, y - 76, x + 112, y + 76), fill="#FFFFFF", outline=color, radius=18, width=6)
    d.line((x - 112, y - 34, x + 112, y - 34), fill=color, width=5)
    for i, c in enumerate([RED, ORANGE, GREEN]):
        d.ellipse((x - 88 + i * 28, y - 60, x - 72 + i * 28, y - 44), fill=c)


def review_checkpoint():
    im, d = canvas()
    centers = [(290, 360), (620, 360), (950, 360), (1280, 360), (1510, 710), (1180, 710), (850, 710), (520, 710)]
    colors = [BLUE, GREEN, ORANGE, PURPLE, RED, CYAN, GOLD, NAVY]
    for i in range(len(centers) - 1):
        arrow(d, centers[i], centers[i + 1], "#B8C4D6", width=5)
    icons = [
        lambda x, y, c: folder_icon(d, x - 78, y - 58, 156, 120, c),
        lambda x, y, c: file_icon(d, x - 58, y - 76, 116, 152, c),
        lambda x, y, c: magnifier_icon(d, x, y, c),
        lambda x, y, c: terminal_icon(d, x, y, c),
        lambda x, y, c: folder_icon(d, x - 78, y - 58, 156, 120, c),
        lambda x, y, c: file_icon(d, x - 58, y - 76, 116, 152, c),
        lambda x, y, c: check_mark(d, x, y, c),
        lambda x, y, c: magnifier_icon(d, x, y, c),
    ]
    for (x, y), color, icon in zip(centers, colors, icons):
        shadow_box(d, (x - 120, y - 120, x + 120, y + 120), fill="#FFFFFF", outline=LINE, radius=32)
        icon(x, y, color)
    d.rounded_rectangle((230, 930, 1570, 1015), radius=36, fill="#EEF6FF", outline="#9CC8FF", width=4)
    for x in range(330, 1500, 180):
        d.ellipse((x - 18, 972 - 18, x + 18, 972 + 18), fill="#FFFFFF", outline=BLUE, width=4)
        check_mark(d, x, 972, BLUE)
    save(im, "ch03_review_checkpoint.png")


def practice_evidence_workbench():
    im, d = canvas()
    shadow_box(d, (145, 185, 1655, 950), fill="#FFFFFF", outline=LINE, radius=34)
    folder_positions = [(250, 335, BLUE), (250, 610, GREEN), (1280, 335, ORANGE), (1280, 610, PURPLE)]
    for x, y, color in folder_positions:
        folder_icon(d, x, y, 210, 160, color)
    board = (610, 280, 1190, 820)
    rounded(d, board, fill="#F8FAFC", outline="#CBD5E1", radius=28, width=4)
    for row, color in enumerate([BLUE, GREEN, ORANGE, PURPLE, RED]):
        y = 350 + row * 85
        d.ellipse((680, y, 730, y + 50), fill="#FFFFFF", outline=color, width=5)
        check_mark(d, 705, y + 25, color)
        d.rounded_rectangle((775, y + 8, 1100, y + 42), radius=17, fill="#E8EEF8")
    for x, y, color in folder_positions:
        start = (x + 210, y + 80) if x < 600 else (x, y + 80)
        end = (board[0], y + 80) if x < 600 else (board[2], y + 80)
        arrow(d, start, end, "#B8C4D6", width=5)
    terminal_icon(d, 900, 875, CYAN)
    save(im, "ch03_practice_evidence_workbench.png")


def gui_handoff_bridge():
    im, d = canvas()
    left = [(230, 360, BLUE), (230, 610, GREEN)]
    mid = [(630, 485, ORANGE), (900, 485, PURPLE)]
    right = [(1320, 485, CYAN)]
    for x, y, color in left:
        folder_icon(d, x - 105, y - 78, 210, 160, color)
    for x, y, color in mid:
        file_icon(d, x - 62, y - 82, 124, 164, color)
    for x, y, color in right:
        window_icon(d, x, y, color)
    arrow(d, (350, 440), (555, 485), "#B8C4D6", width=6)
    arrow(d, (350, 690), (555, 525), "#B8C4D6", width=6)
    arrow(d, (700, 485), (825, 485), "#B8C4D6", width=6)
    arrow(d, (970, 485), (1190, 485), "#B8C4D6", width=6)
    for x in [500, 780, 1080]:
        d.ellipse((x - 18, 640 - 18, x + 18, 640 + 18), fill="#FFFFFF", outline=GREEN, width=4)
        check_mark(d, x, 640, GREEN)
    d.rounded_rectangle((260, 900, 1540, 990), radius=40, fill="#F1FFF7", outline=GREEN, width=4)
    for x in range(390, 1430, 170):
        file_icon(d, x - 28, 928, 56, 44, GREEN)
    save(im, "ch03_gui_handoff_bridge.png")


def archive_manifest_preview():
    photo_plate("ch03_archive_manifest_preview.png", "ch03_archive_manifest_preview.png")


def archive_receipt_preview():
    photo_plate("ch03_archive_receipt_preview.png", "ch03_archive_receipt_preview.png")


def path_safety_receipt():
    src = ROOT / "workspace_ch03" / "output" / "ch03_path_safety_receipt.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch03_path_safety_receipt.png", optimize=True, quality=95)
    photo_plate("ch03_path_safety_receipt.png", "ch03_path_safety_receipt.png")


def ch02_stroop_file_handoff():
    src = ROOT / "workspace_ch03" / "output" / "ch03_ch02_stroop_file_handoff.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch03_ch02_stroop_file_handoff.png", optimize=True, quality=95)
    photo_plate("ch03_ch02_stroop_file_handoff.png", "ch03_ch02_stroop_file_handoff.png")


def archive_evidence_board():
    src = ROOT / "workspace_ch03" / "output" / "ch03_archive_evidence_board.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch03_archive_evidence_board.png", optimize=True, quality=95)
    photo_plate("ch03_archive_evidence_board.png", "ch03_archive_evidence_board.png")


def material_intake_register():
    src = ROOT / "workspace_ch03" / "output" / "ch03_material_intake_register.png"
    if src.exists():
        WEB_DIR.mkdir(parents=True, exist_ok=True)
        Image.open(src).save(WEB_DIR / "ch03_material_intake_register.png", optimize=True, quality=95)
    photo_plate("ch03_material_intake_register.png", "ch03_material_intake_register.png")


def center_text(d, text, box, fnt, fill=INK):
    x1, y1, x2, y2 = box
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2), text, font=fnt, fill=fill)


def file_icon(d, x, y, w, h, color, fill="#FFFFFF"):
    rounded(d, (x, y, x + w, y + h), fill=fill, outline=color, radius=18, width=4)
    fold = min(w, h) * 0.22
    d.polygon([(x + w - fold, y), (x + w, y + fold), (x + w, y)], fill="#EAF0FA")
    d.line((x + w - fold, y, x + w, y + fold), fill=color, width=3)


def folder_icon(d, x, y, w, h, color, fill="#FFFFFF"):
    d.rounded_rectangle((x, y + h * 0.18, x + w, y + h), radius=22, fill=fill, outline=color, width=4)
    d.rounded_rectangle((x + w * 0.08, y, x + w * 0.48, y + h * 0.3), radius=14, fill=fill, outline=color, width=4)
    d.line((x + w * 0.08, y + h * 0.3, x + w * 0.95, y + h * 0.3), fill=color, width=4)


def station(d, xy, label, color):
    shadow_box(d, xy, fill="#FFFFFF", outline=LINE, radius=26)
    x1, y1, x2, y2 = xy
    d.ellipse((x1 + 34, y1 + 38, x1 + 114, y1 + 118), fill=color)
    center_text(d, label, (x1 + 135, y1 + 40, x2 - 26, y2 - 34), F_H2, INK)


def cover():
    im, d = canvas()
    d.rounded_rectangle((70, 56, 1730, 220), radius=28, fill=NAVY)
    center_text(d, "第 3 章  文件读写与文件夹管理", (90, 72, 1710, 145), F_TITLE, "white")
    center_text(d, "读 · 写 · 找 · 搬 · 删", (90, 150, 1710, 205), F_SUBTITLE, "#D6E1F5")

    shadow_box(d, (150, 310, 1650, 805), fill="#FFFFFF")
    folder_icon(d, 245, 455, 230, 185, BLUE)
    center_text(d, "data/", (235, 650, 485, 710), F_H2, BLUE)

    rounded(d, (680, 385, 1120, 700), fill="#111827", outline="#111827", radius=24)
    d.rectangle((720, 435, 1080, 445), fill="#334155")
    d.rectangle((720, 510, 1015, 520), fill="#334155")
    d.rectangle((720, 585, 1060, 595), fill="#334155")
    d.ellipse((735, 630, 805, 700), fill=GREEN)
    center_text(d, "Python", (795, 625, 1065, 700), F_H2, "#A7F3D0")

    folder_icon(d, 1325, 455, 230, 185, PURPLE)
    center_text(d, "output/", (1305, 650, 1575, 710), F_H2, PURPLE)

    arrow(d, (505, 548), (650, 548), BLUE, width=7)
    arrow(d, (1150, 548), (1295, 548), PURPLE, width=7)
    center_text(d, "安全工作区", (390, 890, 1410, 960), F_SUBTITLE, MUTED)
    save(im, "ch03_cover.png")


def roadmap():
    im, d = canvas()
    title_block(d, "第 3 章知识路线图", "先找到文件，再读写内容，最后把资料整理成可检查的项目档案。")
    nodes = [
        ("1", "路径", BLUE),
        ("2", "打开", GREEN),
        ("3", "读取", ORANGE),
        ("4", "写入", PURPLE),
        ("5", "管理", CYAN),
        ("6", "归档", RED),
    ]
    positions = [(210, 430), (480, 640), (810, 430), (1080, 640), (1410, 430), (810, 840)]
    for i in range(len(positions) - 1):
        arrow(d, positions[i], positions[i + 1], "#B8C4D6", width=5)
    for num, label, color in nodes:
        x, y = positions[int(num) - 1]
        d.ellipse((x - 72, y - 72, x + 72, y + 72), fill="white", outline=color, width=7)
        center_text(d, num, (x - 70, y - 68, x + 70, y - 12), F_H2, color)
        center_text(d, label, (x - 110, y + 2, x + 110, y + 86), F_BODY, INK)
    save(im, "ch03_roadmap.png")


def file_io_pipeline():
    im, d = canvas()
    title_block(d, "文件读写流水线", "文件进入程序，程序处理资料，再把结果保存回项目。")
    stations = [
        ((150, 430, 405, 670), "文件", BLUE),
        ((555, 430, 810, 670), "读取", GREEN),
        ((960, 430, 1215, 670), "处理", ORANGE),
        ((1365, 430, 1620, 670), "写出", PURPLE),
    ]
    for i, (xy, label, color) in enumerate(stations):
        station(d, xy, label, color)
        if label == "文件":
            file_icon(d, xy[0] + 48, xy[1] + 118, 82, 96, color)
        elif label == "写出":
            folder_icon(d, xy[0] + 45, xy[1] + 128, 92, 72, color)
        else:
            d.arc((xy[0] + 48, xy[1] + 122, xy[0] + 126, xy[1] + 200), 30, 330, fill=color, width=7)
        if i < 3:
            arrow(d, (xy[2] + 32, 550), (stations[i + 1][0][0] - 35, 550), "#B8C4D6", width=6)
    center_text(d, "data/  →  Python  →  output/", (420, 870, 1380, 950), F_H2, MUTED)
    save(im, "ch03_file_io_pipeline.png")


def open_mode_matrix():
    im, d = canvas()
    title_block(d, "open() 模式速查", "不同模式像不同钥匙：读、写、追加、新建、二进制、读写。")
    modes = [("r", "读", BLUE), ("w", "写", RED), ("a", "追加", GREEN), ("x", "新建", ORANGE), ("b", "二进制", PURPLE), ("+", "读写", CYAN)]
    key_x, key_y = 875, 500
    d.ellipse((760, 385, 990, 615), outline="#B8C4D6", width=18)
    for i, (mode, label, color) in enumerate(modes):
        x = 185 + i * 280
        y = 740 if i % 2 else 285
        d.line((key_x, key_y, x + 80, y + 70), fill="#CDD6E5", width=5)
        d.ellipse((x, y, x + 160, y + 140), fill="white", outline=color, width=6)
        center_text(d, mode, (x, y + 8, x + 160, y + 75), F_TITLE, color)
        center_text(d, label, (x - 30, y + 76, x + 190, y + 138), F_BODY, INK)
        d.rectangle((x + 138, y + 54, x + 226, y + 82), fill=color)
        d.rectangle((x + 202, y + 70, x + 226, y + 104), fill=color)
    save(im, "ch03_open_mode_matrix.png")


def with_context_door():
    im, d = canvas()
    title_block(d, "with open()：自动关门", "把文件打开，也要让它可靠关闭。")
    shadow_box(d, (220, 340, 740, 810), fill="#FFFFFF")
    center_text(d, "手动", (250, 385, 710, 445), F_H2, RED)
    rounded(d, (380, 500, 595, 735), fill="#FFF1F2", outline=RED, radius=16)
    d.arc((532, 595, 578, 642), 260, 95, fill=RED, width=8)
    center_text(d, "open", (310, 462, 665, 520), F_BODY, INK)
    center_text(d, "close", (310, 728, 665, 780), F_BODY, INK)

    shadow_box(d, (1060, 340, 1580, 810), fill="#FFFFFF")
    center_text(d, "with", (1090, 385, 1550, 445), F_H2, GREEN)
    rounded(d, (1205, 500, 1420, 735), fill="#F1FFF7", outline=GREEN, radius=16)
    d.arc((1360, 595, 1402, 642), 260, 95, fill=GREEN, width=8)
    center_text(d, "auto close", (1110, 725, 1530, 785), F_BODY, GREEN)
    arrow(d, (770, 575), (1030, 575), "#B8C4D6", width=7)
    save(im, "ch03_with_context_door.png")


def read_methods_comparison():
    im, d = canvas()
    title_block(d, "读取方法对比", "同一个文件，可以整段读，也可以一行一行读。")
    methods = [("read()", BLUE), ("readline()", GREEN), ("readlines()", ORANGE), ("for line", PURPLE)]
    for i, (label, color) in enumerate(methods):
        x = 145 + i * 410
        shadow_box(d, (x, 380, x + 320, 760), fill="#FFFFFF")
        file_icon(d, x + 100, 455, 120, 155, color)
        if i == 0:
            d.rectangle((x + 128, 500, x + 192, 512), fill=color)
            d.rectangle((x + 128, 535, x + 192, 547), fill=color)
            d.rectangle((x + 128, 570, x + 192, 582), fill=color)
        elif i == 1:
            d.rectangle((x + 128, 535, x + 192, 547), fill=color)
        elif i == 2:
            for yy in [498, 532, 566]:
                d.rectangle((x + 128, yy, x + 192, yy + 11), fill=color)
        else:
            d.line((x + 98, 520, x + 220, 520), fill=color, width=8)
            d.line((x + 98, 560, x + 220, 560), fill=color, width=8)
        center_text(d, label, (x + 10, 650, x + 310, 725), F_BODY, INK)
    save(im, "ch03_read_methods_comparison.png")


def path_map():
    im, d = canvas()
    title_block(d, "路径地图", "相对路径从当前工作目录出发。")
    shadow_box(d, (170, 300, 1630, 850), fill="#FFFFFF")
    rounded(d, (245, 385, 1555, 785), fill="#F8FAFC", outline="#CBD5E1", radius=18, width=4)
    center_text(d, "my_project/", (260, 405, 560, 465), F_H2, NAVY)
    folders = [
        (400, 555, "data/", BLUE),
        (770, 555, "code/", ORANGE),
        (1140, 555, "output/", PURPLE),
    ]
    for x, y, label, color in folders:
        folder_icon(d, x, y, 180, 135, color)
        center_text(d, label, (x - 20, y + 145, x + 200, y + 205), F_BODY, color)
    d.ellipse((760, 395, 920, 555), fill="#EEF6FF", outline=BLUE, width=6)
    center_text(d, "cwd", (760, 410, 920, 540), F_H2, BLUE)
    for x, y, _, color in folders:
        arrow(d, (840, 550), (x + 90, y - 20), color, width=5)
    save(im, "ch03_path_map.png")


def folder_tree_operations():
    im, d = canvas()
    title_block(d, "文件夹管理", "先建目录，再遍历，再复制、移动或清理。")
    root_x, root_y = 815, 310
    folder_icon(d, root_x, root_y, 170, 125, NAVY)
    center_text(d, "root", (root_x - 10, root_y + 135, root_x + 180, root_y + 185), F_BODY, NAVY)
    ops = [("mkdir", 280, 655, BLUE), ("walk", 585, 655, GREEN), ("copy", 890, 655, ORANGE), ("move", 1195, 655, PURPLE), ("delete", 1500, 655, RED)]
    for label, x, y, color in ops:
        arrow(d, (900, 470), (x + 60, y - 30), "#B8C4D6", width=4)
        d.ellipse((x, y, x + 120, y + 120), fill="white", outline=color, width=6)
        center_text(d, label, (x - 50, y + 126, x + 170, y + 185), F_BODY, INK)
    save(im, "ch03_folder_tree_operations.png")


def file_size_chart():
    im, d = canvas()
    title_block(d, "文件夹体检图表", "遍历目录后，把文件大小画出来。")
    shadow_box(d, (190, 285, 1610, 900), fill="#FFFFFF")
    files = ["txt", "csv", "png", "md", "zip"]
    sizes = [12, 34, 82, 28, 64]
    colors = [BLUE, GREEN, ORANGE, PURPLE, RED]
    x0, y0 = 405, 760
    max_h = 360
    bar_w = 130
    gap = 125
    d.line((300, y0, 1500, y0), fill="#94A3B8", width=4)
    d.line((300, 345, 300, y0), fill="#94A3B8", width=4)
    for i, (name, size, color) in enumerate(zip(files, sizes, colors)):
        x = x0 + i * (bar_w + gap)
        h = int(size / 90 * max_h)
        d.rounded_rectangle((x, y0 - h, x + bar_w, y0), radius=14, fill=color)
        center_text(d, f"{size}KB", (x - 15, y0 - h - 60, x + bar_w + 15, y0 - h - 12), F_SMALL, INK)
        center_text(d, name, (x - 20, y0 + 20, x + bar_w + 20, y0 + 70), F_BODY, MUTED)
    save(im, "ch03_file_size_chart.png")


def safe_delete_warning():
    im, d = canvas()
    title_block(d, "删除操作安全卡", "删除前，先看清路径和范围。")
    d.polygon([(900, 315), (620, 785), (1180, 785)], fill="#FFF7E8", outline=ORANGE)
    d.line((900, 450, 900, 615), fill=RED, width=20)
    d.ellipse((885, 665, 915, 695), fill=RED)
    steps = [("打印路径", BLUE), ("确认范围", GREEN), ("移到 trash", ORANGE), ("再清理", PURPLE)]
    for i, (label, color) in enumerate(steps):
        x = 205 + i * 350
        y = 865
        d.ellipse((x, y, x + 92, y + 92), fill="white", outline=color, width=6)
        center_text(d, str(i + 1), (x, y, x + 92, y + 92), F_H2, color)
        center_text(d, label, (x - 80, y + 102, x + 172, y + 155), F_BODY, INK)
        if i < 3:
            arrow(d, (x + 110, y + 46), (x + 260, y + 46), "#B8C4D6", width=5)
    save(im, "ch03_safe_delete_warning.png")


def mini_project_archiver():
    im, d = canvas()
    title_block(d, "本章小项目：资料归档器", "把杂乱文件整理成可复查的项目材料。")
    stations = [
        ((150, 445, 405, 690), "inbox", BLUE),
        ((555, 445, 810, 690), "scan", GREEN),
        ((960, 445, 1215, 690), "organize", ORANGE),
        ((1365, 445, 1620, 690), "report", PURPLE),
    ]
    for i, (xy, label, color) in enumerate(stations):
        station(d, xy, label, color)
        if i == 0:
            folder_icon(d, xy[0] + 50, xy[1] + 128, 90, 72, color)
        elif i == 1:
            d.ellipse((xy[0] + 55, xy[1] + 130, xy[0] + 132, xy[1] + 207), outline=color, width=8)
            d.line((xy[0] + 118, xy[1] + 196, xy[0] + 160, xy[1] + 232), fill=color, width=8)
        elif i == 2:
            folder_icon(d, xy[0] + 38, xy[1] + 124, 72, 58, color)
            folder_icon(d, xy[0] + 115, xy[1] + 145, 72, 58, color)
        else:
            file_icon(d, xy[0] + 58, xy[1] + 120, 84, 108, color)
        if i < 3:
            arrow(d, (xy[2] + 32, 568), (stations[i + 1][0][0] - 35, 568), "#B8C4D6", width=6)
    save(im, "ch03_mini_project_archiver.png")


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    cover()
    roadmap()
    archive_box_project_story()
    information_trail_vannevar_bush()
    file_io_pipeline()
    powershell_file_operations_run()
    open_mode_matrix()
    rosetta_encoding_story()
    with_context_door()
    read_methods_comparison()
    path_map()
    card_filing_cabinet_path_index()
    archive_storage_shelves()
    folder_tree_operations()
    file_size_chart()
    safe_delete_warning()
    path_safety_receipt()
    ch02_stroop_file_handoff()
    mini_project_archiver()
    archive_manifest_preview()
    archive_receipt_preview()
    archive_evidence_board()
    material_intake_register()
    review_checkpoint()
    practice_evidence_workbench()
    gui_handoff_bridge()
    print("Generated ch03 formal visuals.")


if __name__ == "__main__":
    main()
