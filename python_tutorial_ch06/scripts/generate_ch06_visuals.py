from __future__ import annotations

from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "ch06"
WEB_DIR = ASSET_DIR / "web"

W, H = 1800, 1120
BG = "#F7F8FB"
SURFACE = "#FFFFFF"
SOFT = "#F1F5F9"
LINE = "#D8E0EC"
INK = "#162033"
MUTED = "#667085"
BLUE = "#2F6BFF"
GREEN = "#24A06B"
ORANGE = "#F28C28"
PURPLE = "#7A5AF8"
RED = "#E84C61"
CYAN = "#18A9B5"
YELLOW = "#E6A600"


def canvas(width: int = W, height: int = H) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (width, height), BG)
    return image, ImageDraw.Draw(image)


def save(image: Image.Image, name: str) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    image.save(ASSET_DIR / name, optimize=True, quality=95)


def load_font(size: int, bold: bool = False, mono: bool = False):
    candidates: list[Path] = []
    if mono:
        candidates.extend(
            [
                Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
                Path("C:/Windows/Fonts/simhei.ttf"),
                Path("C:/Windows/Fonts/CascadiaMono.ttf"),
                Path("C:/Windows/Fonts/consolab.ttf") if bold else Path("C:/Windows/Fonts/consola.ttf"),
            ]
        )
    candidates.extend(
        [
            Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
            Path("C:/Windows/Fonts/simhei.ttf"),
            Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
            Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
        ]
    )
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    if not text:
        return 0, 0
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def tokens(line: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./:\\()=,'\"#-]+|[\u4e00-\u9fff]|[^\sA-Za-z0-9_./:\\()=,'\"#\-\u4e00-\u9fff]|\s+", line)


def wrap_line(draw: ImageDraw.ImageDraw, line: str, font, max_width: int) -> list[str]:
    output: list[str] = []
    current = ""
    for token in tokens(line):
        if token.isspace():
            token = " "
        candidate = (current + token).strip() if not current else current + token
        if not candidate.strip():
            continue
        if text_size(draw, candidate, font)[0] <= max_width:
            current = candidate
            continue
        if current.strip():
            output.append(current.strip())
            current = token.strip()
            continue
        piece = ""
        for char in token:
            attempt = piece + char
            if text_size(draw, attempt, font)[0] <= max_width:
                piece = attempt
            else:
                if piece:
                    output.append(piece)
                piece = char
        current = piece
    if current.strip():
        output.append(current.strip())

    punctuation = set("，。；：、,.!?！？)]）")
    cleaned: list[str] = []
    for item in output:
        if cleaned and item and item[0] in punctuation:
            cleaned[-1] += item[0]
            if item[1:].strip():
                cleaned.append(item[1:].strip())
        else:
            cleaned.append(item)
    return cleaned or [""]


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, max_height: int, size: int, min_size: int = 18, bold: bool = False, mono: bool = False):
    fallback = None
    for font_size in range(size, min_size - 1, -1):
        font = load_font(font_size, bold=bold, mono=mono)
        lines: list[str] = []
        for para in text.splitlines() or [""]:
            lines.extend(wrap_line(draw, para, font, max_width))
        base_h = max(text_size(draw, "汉字Ag", font)[1], int(font_size * 0.92))
        spacing = max(4, int(font_size * 0.32))
        height = len(lines) * base_h + max(0, len(lines) - 1) * spacing
        fallback = (font, lines, base_h, spacing)
        if height <= max_height:
            return fallback
    return fallback


def draw_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, size: int = 30, min_size: int = 18, fill: str = INK, bold: bool = False, mono: bool = False, align: str = "left", valign: str = "top") -> None:
    x1, y1, x2, y2 = box
    font, lines, line_h, spacing = fit_text(draw, text, x2 - x1, y2 - y1, size, min_size, bold, mono)
    total_h = len(lines) * line_h + max(0, len(lines) - 1) * spacing
    if valign == "center":
        y = y1 + max(0, (y2 - y1 - total_h) // 2)
    elif valign == "bottom":
        y = y2 - total_h
    else:
        y = y1
    for line in lines:
        width, _ = text_size(draw, line, font)
        if align == "center":
            x = x1 + max(0, (x2 - x1 - width) // 2)
        elif align == "right":
            x = x2 - width
        else:
            x = x1
        draw.text((x, y), line, fill=fill, font=font)
        y += line_h + spacing


def rounded(draw: ImageDraw.ImageDraw, xy, fill: str = SURFACE, outline: str = LINE, radius: int = 26, width: int = 2) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def shadow(draw: ImageDraw.ImageDraw, xy, radius: int = 26) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle((x1 + 9, y1 + 11, x2 + 9, y2 + 11), radius=radius, fill="#DCE2EC")


def title(draw: ImageDraw.ImageDraw, heading: str, subtitle: str = "") -> None:
    draw_text(draw, (120, 62, 1680, 134), heading, size=54, min_size=36, bold=True, align="center", valign="center")
    if subtitle:
        draw_text(draw, (180, 142, 1620, 205), subtitle, size=27, min_size=21, fill=MUTED, align="center", valign="center")


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = "#98A5B8", width: int = 5) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    if abs(x2 - x1) >= abs(y2 - y1):
        sign = 1 if x2 >= x1 else -1
        pts = [(x2, y2), (x2 - sign * 22, y2 - 12), (x2 - sign * 22, y2 + 12)]
    else:
        sign = 1 if y2 >= y1 else -1
        pts = [(x2, y2), (x2 - 12, y2 - sign * 22), (x2 + 12, y2 - sign * 22)]
    draw.polygon(pts, fill=color)


def card(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], tag: str, heading: str, body: str, color: str) -> None:
    shadow(draw, xy, radius=24)
    rounded(draw, xy, fill=SURFACE, outline=LINE, radius=24)
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle((x1, y1, x1 + 14, y2), radius=7, fill=color)
    draw.ellipse((x1 + 28, y1 + 24, x1 + 82, y1 + 78), fill=color)
    draw_text(draw, (x1 + 28, y1 + 24, x1 + 82, y1 + 78), tag, size=23, min_size=16, fill="#FFFFFF", bold=True, align="center", valign="center")
    draw_text(draw, (x1 + 100, y1 + 24, x2 - 24, y1 + 80), heading, size=29, min_size=20, bold=True, valign="center")
    draw_text(draw, (x1 + 32, y1 + 93, x2 - 28, y2 - 22), body, size=23, min_size=17, fill=MUTED)


def data_table(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], rows: list[list[str]], color: str = BLUE) -> None:
    x1, y1, x2, y2 = xy
    shadow(draw, xy, radius=24)
    rounded(draw, xy, fill=SURFACE, outline=LINE, radius=24)
    row_h = (y2 - y1 - 28) // len(rows)
    y = y1 + 14
    for i, row in enumerate(rows):
        fill = "#EEF6FF" if i == 0 else ("#F8FAFC" if i % 2 else "#FFFFFF")
        draw.rounded_rectangle((x1 + 18, y, x2 - 18, y + row_h - 8), radius=12, fill=fill, outline="#E2E8F0", width=1)
        col_w = (x2 - x1 - 60) // len(row)
        x = x1 + 32
        for cell in row:
            draw_text(draw, (x, y + 6, x + col_w - 12, y + row_h - 14), cell, size=18, min_size=12, fill=color if i == 0 else INK, bold=i == 0, valign="center")
            x += col_w
        y += row_h


def chart_box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], heading: str, color: str, mode: str = "bar") -> None:
    x1, y1, x2, y2 = xy
    shadow(draw, xy, radius=24)
    rounded(draw, xy, fill=SURFACE, outline=LINE, radius=24)
    draw_text(draw, (x1 + 32, y1 + 24, x2 - 32, y1 + 68), heading, size=28, min_size=20, bold=True, fill=color, valign="center")
    left, top, right, bottom = x1 + 70, y1 + 100, x2 - 48, y2 - 60
    draw.line((left, bottom, right, bottom), fill="#94A3B8", width=3)
    draw.line((left, top, left, bottom), fill="#94A3B8", width=3)
    if mode == "line":
        pts = [(left, bottom - 35), (left + 95, bottom - 110), (left + 190, bottom - 80), (left + 285, bottom - 190), (right, bottom - 155)]
        draw.line(pts, fill=color, width=6)
        for x, y in pts:
            draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill="#FFFFFF", outline=color, width=4)
    elif mode == "scatter":
        points = [(left + 40, bottom - 55), (left + 90, bottom - 110), (left + 140, bottom - 92), (left + 190, bottom - 180), (left + 245, bottom - 140), (right - 30, bottom - 220)]
        for x, y in points:
            draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=color)
    else:
        for i, h in enumerate([86, 145, 108, 205]):
            x = left + 45 + i * 82
            draw.rounded_rectangle((x, bottom - h, x + 48, bottom), radius=12, fill=color)


def photo_plate(output_name: str, image_name: str) -> None:
    image, draw = canvas()
    shadow(draw, (110, 90, 1690, 1050), radius=34)
    rounded(draw, (110, 90, 1690, 1050), fill=SURFACE, radius=34)
    frame = (160, 140, 1640, 930)
    rounded(draw, frame, fill="#F2F4F8", outline=LINE, radius=26)
    src = WEB_DIR / image_name
    if src.exists():
        raw = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        resampling = getattr(Image, "Resampling", Image).LANCZOS
        shown = ImageOps.contain(raw, (frame[2] - frame[0] - 30, frame[3] - frame[1] - 30), method=resampling)
        x = frame[0] + (frame[2] - frame[0] - shown.width) // 2
        y = frame[1] + (frame[3] - frame[1] - shown.height) // 2
        image.paste(shown, (x, y))
    else:
        draw.line((760, 470, 1040, 650), fill=RED, width=12)
        draw.line((1040, 470, 760, 650), fill=RED, width=12)
    save(image, output_name)


def cover() -> None:
    image, draw = canvas()
    title(draw, "第6章 数据分析与可视化", "把学习记录变成表格、指标、图表和下一步行动")
    rows = [["topic", "minutes", "done", "rt_ms"], ["变量", "18", "yes", "520"], ["列表", "25", "yes", "480"], ["文件", "55", "no", "980"]]
    data_table(draw, (120, 300, 670, 750), rows, BLUE)
    chart_box(draw, (770, 300, 1220, 750), "分析图表", GREEN, "bar")
    chart_box(draw, (1320, 300, 1680, 750), "复盘线索", ORANGE, "line")
    arrow(draw, (680, 525), (760, 525), width=7)
    arrow(draw, (1230, 525), (1310, 525), width=7)
    rounded(draw, (305, 900, 1495, 985), fill="#EEF6FF", outline="#B8D6FF", radius=24)
    draw_text(draw, (340, 918, 1460, 970), "本章自查目标：CSV 能生成，摘要能解释，图表能复现，结论能回到学习行动。", size=30, min_size=22, fill=BLUE, bold=True, align="center", valign="center")
    save(image, "ch06_cover.png")


def story_scene() -> None:
    image, draw = canvas()
    title(draw, "从记录表到可解释图表", "数据分析不是神奇按钮，而是一条能复查的学习记录流水线")
    panels = [
        (120, 300, 560, 760, "输入数据", ["learning_records.csv", "topic / minutes", "done / rt_ms"], BLUE),
        (690, 300, 1110, 760, "统计摘要", ["记录数", "平均学习时长", "完成率"], GREEN),
        (1240, 300, 1680, 760, "图表行动", ["趋势", "异常值", "复习计划"], ORANGE),
    ]
    for x1, y1, x2, y2, head, lines, color in panels:
        shadow(draw, (x1, y1, x2, y2), radius=28)
        rounded(draw, (x1, y1, x2, y2), fill=SURFACE, radius=28)
        draw.rounded_rectangle((x1, y1, x2, y1 + 78), radius=28, fill=color)
        draw.rectangle((x1, y1 + 44, x2, y1 + 78), fill=color)
        draw_text(draw, (x1 + 30, y1 + 15, x2 - 30, y1 + 65), head, size=30, min_size=20, fill="#FFFFFF", bold=True, align="center", valign="center")
        y = y1 + 132
        for line in lines:
            rounded(draw, (x1 + 42, y, x2 - 42, y + 62), fill=SOFT, outline="#E2E8F0", radius=16)
            draw_text(draw, (x1 + 66, y + 10, x2 - 66, y + 52), line, size=23, min_size=16, fill=INK, align="center", valign="center")
            y += 88
    arrow(draw, (570, 530), (680, 530), width=7)
    arrow(draw, (1120, 530), (1230, 530), width=7)
    rounded(draw, (315, 910, 1485, 990), fill="#FFF7E8", outline="#F2B84B", radius=24)
    draw_text(draw, (350, 928, 1450, 974), "先问问题，再算摘要，最后用图表检查：结论有没有被数据支持。", size=30, min_size=22, fill="#8A5A00", bold=True, align="center", valign="center")
    save(image, "ch06_story_scene.png")


def roadmap() -> None:
    image, draw = canvas()
    title(draw, "本章学习路线", "从 CSV 到图表，从图表到判断，再把判断交给复习计划")
    items = [
        ("一", "生成 CSV", "用脚本创建一份可复查的学习记录表。", BLUE),
        ("二", "计算摘要", "记录数、平均值、完成率先回答基本问题。", GREEN),
        ("三", "画仪表盘", "把主题、时长、完成状态放进一张图。", ORANGE),
        ("四", "看见分布", "Anscombe 与异常值提醒你别只看平均数。", PURPLE),
        ("五", "图表改造", "减少噪音，让图表主动说出重点。", CYAN),
        ("六", "复习行动", "把 ch05 对象成果包和记忆曲线接起来。", RED),
    ]
    coords = [(125, 280), (650, 280), (1175, 280), (125, 640), (650, 640), (1175, 640)]
    for (x, y), item in zip(coords, items):
        tag, head, body, color = item
        card(draw, (x, y, x + 430, y + 230), tag, head, body, color)
    for start, end in [((555, 395), (635, 395)), ((1080, 395), (1160, 395)), ((1390, 515), (1390, 625)), ((1160, 755), (1080, 755)), ((635, 755), (555, 755))]:
        arrow(draw, start, end, width=4)
    save(image, "ch06_roadmap.png")


def core_metaphor() -> None:
    image, draw = canvas()
    title(draw, "数据分析最小心智模型", "一条分析链通常包含数据、清洗、摘要、图表、解释和行动")
    nodes = [
        ((120, 280, 480, 470), "1", "数据 Data", "CSV、JSON 或表格，是分析的原料。", BLUE),
        ((570, 280, 930, 470), "2", "摘要 Summary", "平均数、完成率、计数先压缩信息。", GREEN),
        ((1020, 280, 1380, 470), "3", "图表 Chart", "让趋势、差异和异常值被看见。", ORANGE),
        ((120, 650, 480, 840), "4", "语境 Context", "数据从哪来、代表什么、不能说明什么。", PURPLE),
        ((570, 650, 930, 840), "5", "判断 Insight", "用数据回答问题，而不是只报数字。", CYAN),
        ((1020, 650, 1380, 840), "6", "行动 Action", "改复习计划、回看异常记录、补数据。", RED),
    ]
    for xy, tag, head, body, color in nodes:
        card(draw, xy, tag, head, body, color)
    for start, end in [((480, 375), (570, 375)), ((930, 375), (1020, 375)), ((1200, 475), (1200, 640)), ((1020, 745), (930, 745)), ((570, 745), (480, 745))]:
        arrow(draw, start, end, width=4)
    rounded(draw, (1460, 310, 1690, 810), fill="#EEF6FF", outline="#B8D6FF", radius=24)
    draw_text(draw, (1490, 345, 1660, 775), "口诀：\n先看数据来源，\n再算摘要，\n再画图，\n最后回到行动。", size=28, min_size=20, fill=BLUE, bold=True, align="center", valign="center")
    save(image, "ch06_core_metaphor.png")


def minimal_demo() -> None:
    image, draw = canvas()
    title(draw, "最小分析：CSV -> 摘要 -> 图表", "第6章先跑通这条最小链，再谈 pandas、图表审美和异常值")
    code = [
        "import csv",
        "from statistics import mean",
        "",
        "with open('input/learning_records.csv', encoding='utf-8') as f:",
        "    rows = list(csv.DictReader(f))",
        "",
        "minutes = [int(row['minutes']) for row in rows]",
        "done = sum(row['done'] == 'yes' for row in rows)",
        "",
        "print('平均学习时长:', mean(minutes))",
        "print('完成率:', done / len(rows))",
    ]
    shadow(draw, (105, 260, 880, 910), radius=28)
    rounded(draw, (105, 260, 880, 910), fill="#111827", outline="#111827", radius=28)
    y = 310
    for line in code:
        draw_text(draw, (155, y, 835, y + 32), line, size=20, min_size=13, fill="#EAF2FF", mono=True, valign="center")
        y += 45
    data_table(draw, (990, 300, 1670, 565), [["topic", "minutes", "done"], ["变量", "18", "yes"], ["列表", "25", "yes"], ["文件", "55", "no"]], BLUE)
    chart_box(draw, (990, 635, 1670, 910), "生成图表", GREEN, "bar")
    arrow(draw, (880, 565), (975, 435), width=6)
    arrow(draw, (1330, 570), (1330, 625), width=6)
    save(image, "ch06_minimal_demo.png")


def psychology_link() -> None:
    image, draw = canvas()
    title(draw, "心理学学习记录如何进入数据分析", "学习时长、完成状态和反应时可以变成复习计划的依据")
    steps = [
        ("1", "记录学习", "topic、minutes、done 写入 CSV。", BLUE),
        ("2", "记录反应", "rt_ms 近似提示认知负荷。", GREEN),
        ("3", "看趋势", "学习时长和完成率先回答进度。", ORANGE),
        ("4", "安排复习", "困难主题更早回看，稳定主题拉长间隔。", PURPLE),
    ]
    x0, y0, w, h, gap = 110, 350, 370, 270, 75
    for i, item in enumerate(steps):
        x = x0 + i * (w + gap)
        card(draw, (x, y0, x + w, y0 + h), *item)
        if i < len(steps) - 1:
            arrow(draw, (x + w + 8, y0 + h // 2), (x + w + gap - 16, y0 + h // 2), width=4)
    rounded(draw, (410, 755, 1390, 900), fill="#ECFDF3", outline="#8EE3B0", radius=24)
    draw_text(draw, (450, 782, 1350, 870), "数据分析不是为了给自己排名，而是为了决定下一次该复习什么、何时复习、为什么复习。", size=31, min_size=22, fill="#087443", bold=True, align="center", valign="center")
    save(image, "ch06_psychology_link.png")


def pitfall_map() -> None:
    image, draw = canvas()
    title(draw, "第6章常见坑：别让图表替你乱下结论", "数据分析排错要同时看数据、代码、图表和解释")
    items = [
        ("坑1", "只看平均数", "平均值相同，图形可能完全不同。", RED),
        ("坑2", "缺少来源", "图表不说明数据从哪来，结论就站不稳。", ORANGE),
        ("坑3", "颜色太多", "颜色没有含义时，只会增加阅读负担。", PURPLE),
        ("坑4", "忽略异常值", "异常可能是错误，也可能是故事入口。", BLUE),
        ("坑5", "图表不保存", "没有输出文件，就无法复查和提交。", GREEN),
        ("坑6", "结论离开语境", "数据只能回答它能回答的问题。", CYAN),
    ]
    coords = [(110, 280), (650, 280), (1190, 280), (110, 640), (650, 640), (1190, 640)]
    for (x, y), item in zip(coords, items):
        card(draw, (x, y, x + 500, y + 230), *item)
    save(image, "ch06_pitfall_map.png")


def project_dashboard() -> None:
    image, draw = canvas()
    title(draw, "学习卡片统计仪表盘成果链", "本章项目要把学习记录加工成图表、报告、JSON 和复习计划")
    data_table(draw, (115, 315, 565, 705), [["input/", "learning_records.csv"], ["字段", "topic"], ["字段", "minutes"], ["字段", "rt_ms"]], BLUE)
    chart_box(draw, (690, 280, 1120, 725), "统计仪表盘", GREEN, "bar")
    outputs = [
        ("报告", "ch06_analysis_runtime_evidence.md", ORANGE),
        ("JSON", "ch06_ch05_handoff_summary.json", PURPLE),
        ("图片", "ch06_memory_review_plan.png", CYAN),
    ]
    x = 1250
    y = 260
    for folder, filename, color in outputs:
        card(draw, (x, y, 1740, y + 145), folder, "学习成果", filename, color)
        y += 180
    arrow(draw, (575, 510), (680, 510), width=7)
    arrow(draw, (1130, 510), (1240, 510), width=7)
    rounded(draw, (315, 875, 1485, 965), fill="#FFF7E8", outline="#F2B84B", radius=24)
    draw_text(draw, (350, 895, 1450, 940), "第6章的项目自查，不看图表是否花哨，而看数据、代码、输出和解释是否能重新打开。", size=28, min_size=20, fill="#8A5A00", bold=True, align="center", valign="center")
    save(image, "ch06_project_dashboard.png")


def main() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    cover()
    story_scene()
    roadmap()
    core_metaphor()
    minimal_demo()
    psychology_link()
    pitfall_map()
    project_dashboard()
    photo_plate("ch06_powershell_analysis_run.png", "powershell_ch06_data_analysis_run.png")
    photo_plate("ch06_generated_dashboard_chart.png", "ch06_learning_dashboard_output.png")
    photo_plate("ch06_anscombe_quartet_output.png", "ch06_anscombe_quartet_output.png")
    photo_plate("ch06_chart_makeover_output.png", "ch06_chart_makeover.png")
    photo_plate("ch06_visual_check_preview.png", "ch06_visual_check_preview.png")
    photo_plate("ch06_outlier_diagnosis.png", "ch06_outlier_diagnosis.png")
    photo_plate("ch06_ch05_handoff_analysis.png", "ch06_ch05_handoff_analysis.png")
    photo_plate("ch06_memory_review_plan.png", "ch06_memory_review_plan.png")
    photo_plate("ch06_chart_style_clinic.png", "ch06_chart_style_clinic.png")
    photo_plate("ch06_analysis_runtime_evidence.png", "ch06_analysis_runtime_evidence.png")
    photo_plate("ch06_nightingale_mortality_story.png", "nightingale_mortality.jpg")
    photo_plate("ch06_snow_cholera_map_story.png", "snow_cholera_map.jpg")
    photo_plate("ch06_playfair_timeseries_story.png", "playfair_timeseries.png")
    photo_plate("ch06_minard_napoleon_story.png", "minard_napoleon_map.png")
    photo_plate("ch06_dubois_data_portrait_story.png", "dubois_data_portrait.jpg")
    photo_plate("ch06_anscombe_quartet_story.png", "anscombe_quartet_cropped.jpg")
    photo_plate("ch06_hans_rosling_story.png", "hans_rosling.jpg")
    photo_plate("ch06_ebbinghaus_story.png", "ebbinghaus_portrait.jpg")
    print(f"Generated structured ch06 visuals in {ASSET_DIR}.")


if __name__ == "__main__":
    main()
