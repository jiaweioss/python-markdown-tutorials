from __future__ import annotations

from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "ch05"
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
                Path("C:/Windows/Fonts/consolab.ttf") if bold else Path("C:/Windows/Fonts/consola.ttf"),
                Path("C:/Windows/Fonts/CascadiaMono.ttf"),
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


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_height: int,
    size: int,
    min_size: int = 18,
    bold: bool = False,
    mono: bool = False,
):
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


def draw_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    size: int = 30,
    min_size: int = 18,
    fill: str = INK,
    bold: bool = False,
    mono: bool = False,
    align: str = "left",
    valign: str = "top",
) -> None:
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


def card(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    tag: str,
    heading: str,
    body: str,
    color: str,
) -> None:
    shadow(draw, xy, radius=24)
    rounded(draw, xy, fill=SURFACE, outline=LINE, radius=24)
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle((x1, y1, x1 + 14, y2), radius=7, fill=color)
    draw.ellipse((x1 + 28, y1 + 24, x1 + 82, y1 + 78), fill=color)
    draw_text(draw, (x1 + 28, y1 + 24, x1 + 82, y1 + 78), tag, size=23, min_size=16, fill="#FFFFFF", bold=True, align="center", valign="center")
    draw_text(draw, (x1 + 100, y1 + 24, x2 - 24, y1 + 80), heading, size=29, min_size=20, bold=True, valign="center")
    draw_text(draw, (x1 + 32, y1 + 93, x2 - 28, y2 - 22), body, size=23, min_size=17, fill=MUTED)


def object_box(draw: ImageDraw.ImageDraw, xy, title_text: str, lines: list[str], color: str) -> None:
    x1, y1, x2, y2 = xy
    shadow(draw, xy, radius=24)
    rounded(draw, xy, fill=SURFACE, outline=color, radius=24, width=4)
    draw.rounded_rectangle((x1, y1, x2, y1 + 64), radius=24, fill=color)
    draw.rectangle((x1, y1 + 38, x2, y1 + 64), fill=color)
    draw_text(draw, (x1 + 24, y1 + 12, x2 - 24, y1 + 54), title_text, size=25, min_size=18, fill="#FFFFFF", bold=True, align="center", valign="center")
    y = y1 + 90
    for line in lines:
        rounded(draw, (x1 + 30, y, x2 - 30, y + 48), fill=SOFT, outline="#E2E8F0", radius=14)
        draw_text(draw, (x1 + 46, y + 8, x2 - 46, y + 40), line, size=20, min_size=15, fill=INK, valign="center")
        y += 62


def code_panel(draw: ImageDraw.ImageDraw, xy, lines: list[str]) -> None:
    x1, y1, x2, y2 = xy
    shadow(draw, xy, radius=28)
    rounded(draw, xy, fill="#111827", outline="#111827", radius=28)
    y = y1 + 44
    for line in lines:
        draw_text(draw, (x1 + 44, y, x2 - 42, y + 34), line, size=22, min_size=14, fill="#EAF2FF", mono=True, valign="center")
        y += 48


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
    title(draw, "第5章 面向对象程序设计", "把散落变量收进对象，让职责、协作和交付证据都能看见")
    object_box(draw, (120, 320, 510, 760), "LearningCard", ["topic", "question", "answer", "preview()"], BLUE)
    object_box(draw, (705, 320, 1095, 760), "CardDeck", ["name", "cards[]", "add(card)", "summary()"], GREEN)
    object_box(draw, (1290, 320, 1680, 760), "Trial", ["participant", "stimulus", "response", "is_fast()"], ORANGE)
    arrow(draw, (520, 540), (690, 540), width=8)
    arrow(draw, (1110, 540), (1280, 540), width=8)
    rounded(draw, (350, 900, 1450, 984), fill="#EEF6FF", outline="#B8D6FF", radius=24)
    draw_text(draw, (385, 918, 1415, 968), "本章验收标准：能写类，能创建对象，能解释对象协作，并能交付报告、JSON 和运行证据。", size=29, min_size=21, fill=BLUE, bold=True, align="center", valign="center")
    save(image, "ch05_cover.png")


def story_scene() -> None:
    image, draw = canvas()
    title(draw, "从散装变量到有职责的对象", "代码变长以后，真正难的是让数据和动作住在合适的地方")
    panels = [
        (105, 285, 805, 830, "散装变量", "topic、question、answer、tags 到处传，函数越来越难改。", ["topic = 'OOP'", "question = '类是什么？'", "tags = ['class', 'object']", "preview_card(topic, question)"], RED),
        (995, 285, 1695, 830, "对象模型", "LearningCard 自己保存状态，也自己提供 preview()。", ["card.topic", "card.question", "card.tags", "card.preview()"], BLUE),
    ]
    for x1, y1, x2, y2, head, body, rows, color in panels:
        shadow(draw, (x1, y1, x2, y2), radius=28)
        rounded(draw, (x1, y1, x2, y2), fill=SURFACE, radius=28)
        draw_text(draw, (x1 + 42, y1 + 36, x2 - 42, y1 + 88), head, size=36, min_size=24, bold=True, fill=color, valign="center")
        draw_text(draw, (x1 + 42, y1 + 96, x2 - 42, y1 + 162), body, size=25, min_size=18, fill=MUTED)
        y = y1 + 205
        for row in rows:
            rounded(draw, (x1 + 50, y, x2 - 50, y + 62), fill=SOFT, outline="#E2E8F0", radius=16)
            draw_text(draw, (x1 + 78, y + 7, x2 - 78, y + 54), row, size=23, min_size=16, fill=INK, mono=True, valign="center")
            y += 82
    arrow(draw, (835, 555), (965, 555), BLUE, width=8)
    draw_text(draw, (790, 455, 1010, 515), "封装职责", size=28, min_size=20, fill=BLUE, bold=True, align="center")
    rounded(draw, (305, 915, 1495, 990), fill="#FFF7E8", outline="#F2B84B", radius=24)
    draw_text(draw, (340, 930, 1460, 975), "OOP 的第一步不是炫技，而是把“谁保存什么、谁负责什么”说清楚。", size=30, min_size=22, fill="#8A5A00", bold=True, align="center", valign="center")
    save(image, "ch05_story_scene.png")


def roadmap() -> None:
    image, draw = canvas()
    title(draw, "本章学习路线", "先写最小类，再拆职责、看协作，最后交付可复查的对象项目")
    items = [
        ("一", "类与对象", "用 LearningCard 跑通 class、对象、属性和方法。", BLUE),
        ("二", "属性方法", "理解对象保存状态，方法负责读取、更新和导出。", GREEN),
        ("三", "封装组合", "让 CardDeck 拥有卡片，少写万能函数。", ORANGE),
        ("四", "对象协作", "用消息图看清对象之间怎么互相请求。", PURPLE),
        ("五", "项目交付", "导出报告、JSON、质量回执和跨章对象模型。", CYAN),
        ("六", "运行证据", "用脚本检查本章输出是否全部存在。", RED),
    ]
    coords = [(125, 280), (650, 280), (1175, 280), (125, 640), (650, 640), (1175, 640)]
    for (x, y), item in zip(coords, items):
        tag, head, body, color = item
        card(draw, (x, y, x + 430, y + 230), tag, head, body, color)
    for start, end in [((555, 395), (635, 395)), ((1080, 395), (1160, 395)), ((1390, 515), (1390, 625)), ((1160, 755), (1080, 755)), ((635, 755), (555, 755))]:
        arrow(draw, start, end, width=4)
    save(image, "ch05_roadmap.png")


def core_metaphor() -> None:
    image, draw = canvas()
    title(draw, "OOP 最小心智模型", "类像规则说明，对象是具体成员；方法让对象用自己的数据做事")
    center = (645, 360, 1155, 760)
    object_box(draw, center, "card = LearningCard(...)", ["card.topic", "card.answer", "card.preview()", "card.to_markdown()"], BLUE)
    nodes = [
        ((120, 260, 500, 430), "1", "类 class", "定义共同结构：对象该有什么、会做什么。", GREEN),
        ((120, 620, 500, 790), "2", "对象 object", "按类创建出来的具体实例，保存自己的状态。", BLUE),
        ((1300, 260, 1680, 430), "3", "属性 attribute", "对象身上的数据，例如 topic、answer、tags。", ORANGE),
        ((1300, 620, 1680, 790), "4", "方法 method", "对象身上的动作，例如 preview()、add()。", PURPLE),
        ((650, 860, 1150, 1015), "5", "self", "方法里用 self 访问当前对象自己的数据。", CYAN),
    ]
    for xy, tag, head, body, color in nodes:
        card(draw, xy, tag, head, body, color)
    for start, end in [((500, 345), (645, 450)), ((500, 705), (645, 650)), ((1300, 345), (1155, 450)), ((1300, 705), (1155, 650)), ((900, 760), (900, 860))]:
        arrow(draw, start, end, width=4)
    save(image, "ch05_core_metaphor.png")


def minimal_demo() -> None:
    image, draw = canvas()
    title(draw, "最小类：代码和对象一一对应", "先让 LearningCard 跑起来，再谈继承、设计模式和大型项目")
    code = [
        "from dataclasses import dataclass",
        "",
        "@dataclass",
        "class LearningCard:",
        "    topic: str",
        "    question: str",
        "    answer: str",
        "",
        "    def preview(self) -> str:",
        "        return f'[{self.topic}] {self.question}'",
    ]
    code_panel(draw, (110, 270, 860, 900), code)
    object_box(draw, (1170, 330, 1670, 710), "card", ["topic = 'OOP'", "question = '类是什么？'", "answer = '对象图纸'", "preview()"], BLUE)
    mappings = [
        ("class", "定义图纸"),
        ("属性", "保存状态"),
        ("方法", "提供动作"),
        ("self", "指向当前对象"),
    ]
    x = 910
    y = 345
    for key, value in mappings:
        rounded(draw, (910, y, 1050, y + 54), fill="#EEF6FF", outline="#B8D6FF", radius=16)
        draw_text(draw, (925, y + 8, 1035, y + 46), key, size=20, min_size=15, fill=BLUE, bold=True, align="center", valign="center")
        rounded(draw, (1070, y, 1148, y + 54), fill=SOFT, outline="#E2E8F0", radius=16)
        draw_text(draw, (1078, y + 8, 1140, y + 46), value, size=18, min_size=13, fill=INK, align="center", valign="center")
        y += 86
    arrow(draw, (860, 580), (900, 580), width=6)
    arrow(draw, (1150, 580), (1170, 580), width=6)
    rounded(draw, (1090, 795, 1740, 885), fill="#ECFDF3", outline="#8EE3B0", radius=22)
    draw_text(draw, (1125, 815, 1705, 862), "对象不是一包变量，而是一组状态和动作的边界。", size=26, min_size=19, fill="#087443", bold=True, align="center", valign="center")
    save(image, "ch05_minimal_demo.png")


def psychology_link() -> None:
    image, draw = canvas()
    title(draw, "心理学试次为什么适合对象", "Trial 把一次刺激、一次反应和一次反应时收在同一个边界里")
    steps = [
        ("1", "呈现刺激", "stimulus = RED / ink_color = blue", BLUE),
        ("2", "收集反应", "response_key = 'j'", GREEN),
        ("3", "记录反应时", "reaction_time_ms = 438.5", ORANGE),
        ("4", "判断状态", "trial.is_fast() 返回 True/False", PURPLE),
    ]
    x0, y0, w, h, gap = 110, 350, 370, 270, 75
    for i, item in enumerate(steps):
        x = x0 + i * (w + gap)
        card(draw, (x, y0, x + w, y0 + h), *item)
        if i < len(steps) - 1:
            arrow(draw, (x + w + 8, y0 + h // 2), (x + w + gap - 16, y0 + h // 2), width=4)
    object_box(draw, (570, 725, 1230, 980), "Trial 对象", ["participant", "stimulus", "response", "reaction_time_ms", "is_fast()"], CYAN)
    save(image, "ch05_psychology_link.png")


def pitfall_map() -> None:
    image, draw = canvas()
    title(draw, "第5章常见坑：先看职责边界", "OOP 报错和设计混乱，通常都能从 self、对象身份和职责范围排查")
    items = [
        ("坑1", "忘记 self", "方法里访问属性时，要写 self.topic。", RED),
        ("坑2", "把类当对象", "LearningCard 是图纸，card 才是具体卡片。", ORANGE),
        ("坑3", "万能大类", "一个类同时管文件、GUI、统计和导出，很快会失控。", PURPLE),
        ("坑4", "过早继承", "说不清 is-a 时，先尝试组合。", BLUE),
        ("坑5", "数据行为分离", "如果数据到处传，考虑让对象自己提供方法。", GREEN),
        ("坑6", "职责重叠", "两个类管同一份核心状态时，先重新画职责卡。", CYAN),
    ]
    coords = [(110, 280), (650, 280), (1190, 280), (110, 640), (650, 640), (1190, 640)]
    for (x, y), item in zip(coords, items):
        card(draw, (x, y, x + 500, y + 230), *item)
    save(image, "ch05_pitfall_map.png")


def project_dashboard() -> None:
    image, draw = canvas()
    title(draw, "科研卡片工厂的对象交付链", "对象设计最后要变成报告、JSON、图片和下一章能继续读取的数据")
    object_box(draw, (115, 300, 465, 650), "LearningCard", ["topic", "question", "answer", "preview()"], BLUE)
    object_box(draw, (535, 300, 885, 650), "CardDeck", ["cards[]", "add()", "summary()", "export()"], GREEN)
    object_box(draw, (955, 300, 1305, 650), "Trial", ["stimulus", "response", "rt", "is_fast()"], ORANGE)
    arrow(draw, (465, 475), (535, 475), width=5)
    arrow(draw, (885, 475), (955, 475), width=5)
    outputs = [
        ("reports/", "ch05_oop_model_report.md", PURPLE),
        ("output/", "ch05_object_delivery_package.json", CYAN),
        ("assets/", "ch05_oop_runtime_evidence.png", RED),
    ]
    x = 1380
    y = 250
    for folder, filename, color in outputs:
        card(draw, (x, y, 1740, y + 150), folder, "交付物", filename, color)
        y += 190
    arrow(draw, (1305, 475), (1370, 475), width=7)
    rounded(draw, (360, 820, 1440, 910), fill="#FFF7E8", outline="#F2B84B", radius=24)
    draw_text(draw, (400, 840, 1400, 888), "第5章的项目验收，不看“有没有写 class”，而看对象职责和输出证据是否清楚。", size=29, min_size=21, fill="#8A5A00", bold=True, align="center", valign="center")
    save(image, "ch05_project_dashboard.png")


def object_theater_story() -> None:
    image, draw = canvas()
    title(draw, "对象协作小剧场", "每个对象只演自己的角色，通过消息把任务交给下一个对象")
    actors = [
        ("LearningCard", "准备内容", "preview()", BLUE),
        ("CardDeck", "管理集合", "add(card)", GREEN),
        ("Trial", "记录一次反应", "is_fast()", ORANGE),
        ("ReportBuilder", "整理证据", "write()", PURPLE),
    ]
    x = 135
    y = 380
    for i, (name, role, method, color) in enumerate(actors):
        object_box(draw, (x, y, x + 345, y + 280), name, [role, method], color)
        if i < len(actors) - 1:
            arrow(draw, (x + 350, y + 140), (x + 430, y + 140), width=5)
        x += 430
    rounded(draw, (260, 820, 1540, 910), fill="#EEF6FF", outline="#B8D6FF", radius=24)
    draw_text(draw, (300, 840, 1500, 888), "设计时先问“这个请求应该发给谁”，比先写一堆函数更稳。", size=30, min_size=22, fill=BLUE, bold=True, align="center", valign="center")
    save(image, "ch05_object_theater_story.png")


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
    object_theater_story()

    photo_plate("ch05_powershell_oop_run.png", "powershell_ch05_oop_run.png")
    photo_plate("ch05_oop_model_preview.png", "ch05_oop_model_preview.png")
    photo_plate("ch05_design_cards_preview.png", "ch05_design_cards_preview.png")
    photo_plate("ch05_object_collaboration_map.png", "ch05_object_collaboration_map.png")
    photo_plate("ch05_object_quality_receipt.png", "ch05_object_quality_receipt.png")
    photo_plate("ch05_object_delivery_package.png", "ch05_object_delivery_package.png")
    photo_plate("ch05_gui_panel_object_model.png", "ch05_gui_panel_object_model.png")
    photo_plate("ch05_oop_runtime_evidence.png", "ch05_oop_runtime_evidence.png")

    photo_plate("ch05_simula_origin_story.png", "simula_logo.png")
    photo_plate("ch05_kristen_nygaard_story.png", "kristen_nygaard.png")
    photo_plate("ch05_blueprint_class_story.png", "university_bridge_blueprint.jpg")
    photo_plate("ch05_alan_kay_oop_story.png", "alan_kay.jpg")
    photo_plate("ch05_smalltalk_environment_story.png", "squeak_morphic_interface_screenshot.png")
    photo_plate("ch05_xkcd_code_quality.png", "xkcd_code_quality.png")
    photo_plate("ch05_lego_composition_story.png", "lego_color_bricks.jpg")
    photo_plate("ch05_piaget_schema_story.png", "jean_piaget.png")
    photo_plate("ch05_adele_goldberg_story.png", "adele_goldberg_pycon_2007.jpg")
    print(f"Generated structured ch05 visuals in {ASSET_DIR}.")


if __name__ == "__main__":
    main()
