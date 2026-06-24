from __future__ import annotations

from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "ch04"
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


def small_window(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], heading: str, fields: list[str], button: str, color: str = BLUE) -> None:
    x1, y1, x2, y2 = xy
    rounded(draw, xy, fill=SURFACE, outline="#B8C4D6", radius=24, width=3)
    draw.rectangle((x1, y1, x2, y1 + 48), fill="#EAF2FF")
    for i, dot in enumerate(["#F87171", "#FBBF24", "#34D399"]):
        draw.ellipse((x1 + 22 + i * 28, y1 + 17, x1 + 38 + i * 28, y1 + 33), fill=dot)
    draw_text(draw, (x1 + 110, y1 + 10, x2 - 20, y1 + 43), heading, size=20, min_size=15, fill=INK, bold=True, valign="center")
    y = y1 + 82
    for item in fields:
        draw_text(draw, (x1 + 36, y, x1 + 138, y + 34), item, size=19, min_size=14, fill=INK, bold=True, valign="center")
        rounded(draw, (x1 + 145, y, x2 - 36, y + 38), fill=SOFT, outline="#CBD5E1", radius=10, width=2)
        y += 62
    rounded(draw, (x1 + 170, y2 - 76, x2 - 170, y2 - 30), fill=color, outline=color, radius=14)
    draw_text(draw, (x1 + 170, y2 - 76, x2 - 170, y2 - 30), button, size=20, min_size=15, fill="#FFFFFF", bold=True, align="center", valign="center")


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
    title(draw, "第4章 Tkinter 图形界面编程", "把函数包装成窗口动作，把点击变成可检查的文件结果")
    small_window(draw, (135, 300, 655, 790), "科研卡片工厂控制面板", ["主题", "要点"], "保存卡片", BLUE)
    steps = [
        ("输入", "Entry/Text 收集主题与要点"),
        ("回调", "Button.command 调用函数"),
        ("反馈", "messagebox 告诉用户结果"),
        ("成果", "cards/ 与 reports/ 留下学习记录"),
    ]
    x = 770
    for i, (head, body) in enumerate(steps):
        y = 290 + i * 150
        card(draw, (x, y, 1590, y + 116), str(i + 1), head, body, [GREEN, ORANGE, PURPLE, CYAN][i])
        if i < len(steps) - 1:
            arrow(draw, (1180, y + 120), (1180, y + 145), width=4)
    rounded(draw, (315, 910, 1485, 985), fill="#FFF7E8", outline="#F2B84B", radius=24)
    draw_text(draw, (350, 925, 1450, 970), "本章自查目标：窗口能运行，界面看得懂，点击有反馈，最后能找到保存文件。", size=30, min_size=22, fill="#8A5A00", bold=True, align="center", valign="center")
    save(image, "ch04_cover.png")


def story_scene() -> None:
    image, draw = canvas()
    title(draw, "从命令行后厨到 GUI 前台", "同一段 Python 能力，换成用户能看见、能点击、能确认的入口")
    panels = [
        (110, 280, 810, 825, "命令行后厨", "用户需要记命令、路径和参数", ["python code/ch04/02_card_form.py", "Path('cards').mkdir()", "file.write_text(...)"], GREEN),
        (990, 280, 1690, 825, "GUI 前台", "用户看到标签、输入框、按钮和反馈", ["主题输入框", "要点文本框", "保存卡片按钮"], BLUE),
    ]
    for x1, y1, x2, y2, head, body, rows, color in panels:
        shadow(draw, (x1, y1, x2, y2), radius=28)
        rounded(draw, (x1, y1, x2, y2), fill=SURFACE, radius=28)
        draw_text(draw, (x1 + 40, y1 + 36, x2 - 40, y1 + 88), head, size=36, min_size=24, bold=True, fill=color, valign="center")
        draw_text(draw, (x1 + 40, y1 + 92, x2 - 40, y1 + 150), body, size=25, min_size=18, fill=MUTED)
        yy = y1 + 190
        for row in rows:
            rounded(draw, (x1 + 46, yy, x2 - 46, yy + 64), fill=SOFT, outline="#E2E8F0", radius=16)
            draw_text(draw, (x1 + 74, yy + 8, x2 - 74, yy + 56), row, size=24, min_size=17, fill=INK, mono=row.startswith("python"), valign="center")
            yy += 88
    arrow(draw, (840, 550), (960, 550), BLUE, width=8)
    draw_text(draw, (780, 450, 1020, 510), "包装成界面", size=27, min_size=19, fill=BLUE, bold=True, align="center")
    rounded(draw, (300, 910, 1500, 990), fill="#EEF6FF", outline="#B8D6FF", radius=24)
    draw_text(draw, (340, 928, 1460, 974), "GUI 不是换皮肤，而是把任务入口、输入规则、操作结果都摆到用户面前。", size=30, min_size=22, fill=BLUE, bold=True, align="center", valign="center")
    save(image, "ch04_story_scene.png")


def roadmap() -> None:
    image, draw = canvas()
    title(draw, "本章学习路线", "先跑窗口，再拆控件，最后用记录证明 GUI 项目真的完成")
    items = [
        ("一", "窗口通电", "运行最小 Tkinter 窗口，确认 mainloop 留住界面。", BLUE),
        ("二", "控件布局", "认识 Label、Entry、Text、Button 与 pack/grid。", GREEN),
        ("三", "事件回调", "点击按钮后调用函数，保存后给用户反馈。", ORANGE),
        ("四", "卡片项目", "把表单输入写成 Markdown 学习卡片。", PURPLE),
        ("五", "体验检查", "检查按钮大小、间距、状态、错误恢复和文案。", CYAN),
        ("六", "自查收尾", "用报告、截图和输出文件确认自己跑通。", RED),
    ]
    coords = [(125, 280), (650, 280), (1175, 280), (125, 640), (650, 640), (1175, 640)]
    for (x, y), item in zip(coords, items):
        tag, head, body, color = item
        card(draw, (x, y, x + 430, y + 230), tag, head, body, color)
    for start, end in [((555, 395), (635, 395)), ((1080, 395), (1160, 395)), ((1390, 515), (1390, 625)), ((1160, 755), (1080, 755)), ((635, 755), (555, 755))]:
        arrow(draw, start, end, width=4)
    save(image, "ch04_roadmap.png")


def core_metaphor() -> None:
    image, draw = canvas()
    title(draw, "Tkinter 最小心智模型", "一个窗口能跑起来，通常只需要看清这五个角色")
    center = (690, 380, 1110, 745)
    small_window(draw, center, "root = tk.Tk()", ["Label", "Entry", "Button"], "mainloop()")
    nodes = [
        ((130, 270, 500, 430), "1", "窗口 Tk()", "创建顶层窗口，设置标题和大小。", BLUE),
        ((130, 610, 500, 770), "2", "控件 Widget", "显示文字、收集输入、提供按钮。", GREEN),
        ((1300, 270, 1670, 430), "3", "布局 Layout", "决定控件按什么秩序摆放。", ORANGE),
        ((1300, 610, 1670, 770), "4", "回调 Callback", "点击按钮后真正执行的函数。", PURPLE),
        ((715, 850, 1085, 1010), "5", "反馈记录", "弹窗、状态文字或写入文件。", CYAN),
    ]
    for xy, tag, head, body, color in nodes:
        card(draw, xy, tag, head, body, color)
    for start, end in [((500, 350), (690, 430)), ((500, 690), (690, 620)), ((1300, 350), (1110, 430)), ((1300, 690), (1110, 620)), ((900, 745), (900, 850))]:
        arrow(draw, start, end, width=4)
    save(image, "ch04_core_metaphor.png")


def minimal_demo() -> None:
    image, draw = canvas()
    title(draw, "最小窗口：代码和界面一一对应", "先跑通这 6 行，再逐步增加输入框、按钮和保存逻辑")
    shadow(draw, (115, 270, 820, 880), radius=28)
    rounded(draw, (115, 270, 820, 880), fill="#111827", outline="#111827", radius=28)
    code = [
        "import tkinter as tk",
        "",
        "root = tk.Tk()",
        "root.title('科研卡片工厂控制台')",
        "tk.Label(root, text='第一块 GUI 面板已经亮灯').pack()",
        "tk.Button(root, text='收到', command=root.destroy).pack()",
        "root.mainloop()",
    ]
    y = 325
    for line in code:
        draw_text(draw, (165, y, 770, y + 34), line, size=22, min_size=14, fill="#EAF2FF", valign="center")
        y += 50
    small_window(draw, (1240, 360, 1720, 760), "科研卡片工厂控制台", ["第一块 GUI 面板已经亮灯"], "收到", BLUE)
    mappings = [
        ("root.title", "标题栏文字"),
        ("Label", "窗口里的说明文字"),
        ("Button", "用户可点击动作"),
        ("mainloop", "窗口持续响应"),
    ]
    x = 900
    y = 330
    for key, value in mappings:
        rounded(draw, (865, y, 1018, y + 52), fill="#EEF6FF", outline="#B8D6FF", radius=16)
        draw_text(draw, (877, y + 7, 1006, y + 45), key, size=20, min_size=14, fill=BLUE, bold=True, align="center", valign="center")
        rounded(draw, (1040, y, 1215, y + 52), fill=SOFT, outline="#E2E8F0", radius=16)
        draw_text(draw, (1055, y + 7, 1200, y + 45), value, size=20, min_size=14, fill=INK, align="center", valign="center")
        y += 86
    arrow(draw, (820, 560), (860, 560), width=6)
    arrow(draw, (1220, 560), (1240, 560), width=6)
    save(image, "ch04_minimal_demo.png")


def psychology_link() -> None:
    image, draw = canvas()
    title(draw, "GUI 如何接入心理学实验流程", "Stroop 小窗口把刺激、反应、正确性和反应时放进同一条交互链")
    steps = [
        ("1", "显示刺激", "`Label` 呈现 RED，但文字颜色是 blue。", BLUE),
        ("2", "收集反应", "`bind('f')` / `bind('j')` 监听按键。", GREEN),
        ("3", "计算反应时", "`time.perf_counter()` 记录开始和结束。", ORANGE),
        ("4", "写入结果", "正确性、按键和 RT 后续可保存为 CSV。", PURPLE),
    ]
    x0, y0, w, h, gap = 110, 355, 365, 270, 80
    for i, item in enumerate(steps):
        x = x0 + i * (w + gap)
        card(draw, (x, y0, x + w, y0 + h), *item)
        if i < len(steps) - 1:
            arrow(draw, (x + w + 8, y0 + h // 2), (x + w + gap - 16, y0 + h // 2), width=4)
    small_window(draw, (550, 735, 1250, 980), "Stroop GUI 预告", ["刺激 RED / 蓝色", "按 F 或 J"], "开始")
    save(image, "ch04_psychology_link.png")


def pitfall_map() -> None:
    image, draw = canvas()
    title(draw, "第4章常见坑：先按线索排查", "GUI 报错通常不是玄学，先看窗口生命周期、回调、布局和路径")
    items = [
        ("坑1", "忘记 mainloop()", "窗口一闪而过；确认最后调用 root.mainloop()。", RED),
        ("坑2", "command=save_card()", "函数提前执行；按钮里应写 command=save_card。", ORANGE),
        ("坑3", "控件没有布局", "创建了 Label/Entry 但没 pack/grid/place。", PURPLE),
        ("坑4", "路径站错目录", "保存失败先打印 Path.cwd()。", BLUE),
        ("坑5", "没有用户反馈", "保存后用 messagebox 或状态栏告诉结果。", GREEN),
        ("坑6", "界面逻辑混成一团", "先把 save_card() 单独写成函数。", CYAN),
    ]
    coords = [(110, 280), (650, 280), (1190, 280), (110, 640), (650, 640), (1190, 640)]
    for (x, y), item in zip(coords, items):
        card(draw, (x, y, x + 500, y + 230), *item)
    save(image, "ch04_pitfall_map.png")


def project_dashboard() -> None:
    image, draw = canvas()
    title(draw, "科研卡片工厂控制面板", "第4章项目不是摆控件，而是完成从输入到 Markdown 文件的闭环")
    small_window(draw, (115, 320, 635, 760), "学习卡片表单", ["主题", "要点"], "保存卡片", BLUE)
    outputs = [
        ("cards/", "working_memory_load_card.md", GREEN),
        ("reports/", "ch04_card_factory_delivery.md", ORANGE),
        ("output/", "ch04_card_factory_delivery.png", PURPLE),
    ]
    x = 1040
    y = 290
    for folder, filename, color in outputs:
        card(draw, (x, y, 1660, y + 130), folder, "学习成果", filename, color)
        y += 180
    arrow(draw, (650, 540), (1015, 540), width=8)
    rounded(draw, (710, 475, 980, 605), fill="#EEF6FF", outline="#B8D6FF", radius=22)
    draw_text(draw, (735, 494, 955, 586), "save_card()\n写入文件并弹出反馈", size=26, min_size=18, fill=BLUE, bold=True, align="center", valign="center")
    save(image, "ch04_project_dashboard.png")


def norman_door_affordance() -> None:
    image, draw = canvas()
    title(draw, "界面线索：看一眼就知道下一步", "推板、拉手和按钮文案都在回答同一个问题：用户该怎么做？")
    shadow(draw, (150, 235, 1650, 890), radius=34)
    rounded(draw, (150, 235, 1650, 890), fill=SURFACE, radius=34)
    for x, label, color in [(500, "推", BLUE), (1180, "拉", GREEN)]:
        rounded(draw, (x - 170, 330, x + 170, 815), fill="#EFE3D1", outline="#A87C5A", radius=18, width=8)
        if label == "推":
            rounded(draw, (x - 92, 520, x + 92, 650), fill="#D7DEE8", outline="#9CA8B8", radius=20, width=6)
        else:
            rounded(draw, (x - 95, 575, x + 95, 620), fill="#7C4A2F", outline="#4B2E22", radius=20, width=6)
            draw.ellipse((x + 66, 558, x + 126, 636), fill="#B87942", outline="#4B2E22", width=5)
        draw.ellipse((x - 42, 250, x + 42, 334), fill=color)
        draw_text(draw, (x - 42, 250, x + 42, 334), label, size=36, min_size=24, fill="#FFFFFF", bold=True, align="center", valign="center")
    arrow(draw, (720, 565), (960, 565), width=8)
    arrow(draw, (1080, 640), (840, 640), width=8)
    rounded(draw, (390, 930, 1410, 1000), fill="#FFF7E8", outline="#F2B84B", radius=24)
    draw_text(draw, (430, 945, 1370, 984), "换成 Tkinter：标签说明输入框，按钮写清动作，保存后给状态反馈。", size=28, min_size=20, fill="#8A5A00", bold=True, align="center", valign="center")
    save(image, "ch04_norman_door_affordance.png")


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
    norman_door_affordance()

    photo_plate("ch04_history_xerox_alto.png", "xerox_alto_1973.jpg")
    photo_plate("ch04_engelbart_mouse_story.png", "engelbart_mouse_replica.jpg")
    photo_plate("ch04_macintosh_gui_story.png", "macintosh_128k_transparency.png")
    photo_plate("ch04_hypercard_story.png", "hypercard.jpg")
    photo_plate("ch04_susan_kare_icon_story.png", "susan_kare_2019.jpg")
    photo_plate("ch04_don_norman_story.png", "don_norman_cropped.jpg")
    photo_plate("ch04_tkinter_hello_window_screenshot.png", "tkinter_hello_window.png")
    photo_plate("ch04_tkinter_card_form_screenshot.png", "tkinter_card_form_window.png")
    photo_plate("ch04_tkinter_stroop_screenshot.png", "tkinter_stroop_window.png")
    photo_plate("ch04_gui_runtime_evidence.png", "ch04_gui_runtime_evidence.png")
    photo_plate("ch04_gui_usability_check.png", "ch04_gui_usability_check_output.png")
    photo_plate("ch04_target_feedback_lab.png", "ch04_target_feedback_lab.png")
    photo_plate("ch04_gui_feedback_scorecard.png", "ch04_gui_feedback_scorecard.png")
    photo_plate("ch04_interaction_receipt.png", "ch04_interaction_receipt.png")
    photo_plate("ch04_card_factory_delivery.png", "ch04_card_factory_delivery.png")
    photo_plate("ch04_ch03_data_gui_panel.png", "ch04_ch03_data_gui_panel.png")
    photo_plate("ch04_gui_journey_storyboard.png", "ch04_gui_journey_storyboard.png")
    print(f"Generated structured ch04 visuals in {ASSET_DIR}.")


if __name__ == "__main__":
    main()
