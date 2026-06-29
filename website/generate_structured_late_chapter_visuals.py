from __future__ import annotations

import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]

W, H = 1600, 1000

BG = "#F6F8FB"
PAPER = "#FFFFFF"
INK = "#182033"
MUTED = "#607086"
SOFT = "#EEF3FA"
LINE = "#D8E1EF"
BLUE = "#2563EB"
CYAN = "#0891B2"
GREEN = "#16A34A"
ORANGE = "#F97316"
PURPLE = "#7C3AED"
RED = "#DC2626"
YELLOW = "#FBBF24"
DARK = "#111827"


FONT_CACHE: dict[tuple[int, bool], ImageFont.FreeTypeFont | ImageFont.ImageFont] = {}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    key = (size, bold)
    if key in FONT_CACHE:
        return FONT_CACHE[key]
    names = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for name in names:
        path = Path(name)
        if path.exists():
            FONT_CACHE[key] = ImageFont.truetype(str(path), size)
            return FONT_CACHE[key]
    FONT_CACHE[key] = ImageFont.load_default()
    return FONT_CACHE[key]


def text_wh(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    if not text:
        return 0, 0
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./:+#%-]+|[\u4e00-\u9fff]|[^\u4e00-\u9fffA-Za-z0-9_./:+#%-]", text)


def wrap_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    fnt: ImageFont.ImageFont,
    max_width: int,
    max_lines: int | None = None,
) -> list[str]:
    out: list[str] = []
    current = ""
    truncated = False
    parts = text.split("\n")
    for part_index, raw_part in enumerate(parts):
        part_tokens = tokens(raw_part)
        for token_index, tk in enumerate(part_tokens):
            if tk == "\n":
                continue
            candidate = current + tk
            if current and text_wh(draw, candidate, fnt)[0] > max_width:
                out.append(current.strip())
                current = tk.lstrip()
                if max_lines and len(out) >= max_lines:
                    truncated = token_index < len(part_tokens) - 1 or bool(current.strip()) or part_index < len(parts) - 1
                    current = ""
                    break
            else:
                current = candidate
        if current and (not max_lines or len(out) < max_lines):
            out.append(current.strip())
        elif current:
            truncated = True
        current = ""
        if max_lines and len(out) >= max_lines:
            if part_index < len(parts) - 1:
                truncated = True
            break
    if max_lines and len(out) > max_lines:
        truncated = True
        out = out[:max_lines]
    if truncated and out:
        last = out[-1]
        while text_wh(draw, last + "...", fnt)[0] > max_width and last:
            last = last[:-1]
        out[-1] = last + "..." if last else "..."
    return [line for line in out if line]


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    fill: str = INK,
    max_width: int | None = None,
    line_gap: int = 8,
    max_lines: int | None = None,
    align: str = "left",
) -> int:
    x, y = xy
    if max_width is None:
        draw.text((x, y), text, font=fnt, fill=fill)
        return y + text_wh(draw, text, fnt)[1]
    line_height = text_wh(draw, "学习", fnt)[1] + line_gap
    for line in wrap_lines(draw, text, fnt, max_width, max_lines):
        tw, _ = text_wh(draw, line, fnt)
        dx = 0
        if align == "center":
            dx = max(0, (max_width - tw) // 2)
        elif align == "right":
            dx = max(0, max_width - tw)
        draw.text((x + dx, y), line, font=fnt, fill=fill)
        y += line_height
    return y


def canvas() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, W, 80):
        d.line((x, 0, x, H), fill="#EDF2F8", width=1)
    for y in range(0, H, 80):
        d.line((0, y, W, y), fill="#EDF2F8", width=1)
    return img


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str = PAPER,
    outline: str = LINE,
    radius: int = 28,
    width: int = 2,
    shadow: bool = True,
) -> None:
    x1, y1, x2, y2 = box
    if shadow:
        draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#DCE5F0")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def pill(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, fg: str = "#FFFFFF") -> int:
    x, y = xy
    fnt = font(28, True)
    tw, th = text_wh(draw, text, fnt)
    pad_x, pad_y = 20, 9
    draw.rounded_rectangle((x, y, x + tw + pad_x * 2, y + th + pad_y * 2), radius=22, fill=fill)
    draw.text((x + pad_x, y + pad_y - 2), text, font=fnt, fill=fg)
    return x + tw + pad_x * 2 + 14


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = BLUE, width: int = 6) -> None:
    draw.line((start[0], start[1], end[0], end[1]), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 18
    left = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    right = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([end, left, right], fill=color)


def label_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    accent: str,
    number: str | None = None,
) -> None:
    rounded(draw, box, fill=PAPER, outline=LINE, radius=24)
    x1, y1, x2, _ = box
    if number:
        draw.ellipse((x1 + 24, y1 + 24, x1 + 78, y1 + 78), fill=accent)
        draw_text(draw, (x1 + 41, y1 + 30), number, font(30, True), "#FFFFFF")
        tx = x1 + 94
    else:
        draw.rounded_rectangle((x1 + 24, y1 + 28, x1 + 36, y1 + 82), radius=6, fill=accent)
        tx = x1 + 56
    title_width = x2 - tx - 24
    title_font = font(31, True)
    if text_wh(draw, title, title_font)[0] > title_width:
        title_font = font(27, True)
    title_bottom = draw_text(draw, (tx, y1 + 25), title, title_font, INK, max_width=title_width, max_lines=2)
    body_y = max(y1 + 90, title_bottom + 8)
    draw_text(draw, (x1 + 30, body_y), body, font(24), MUTED, max_width=x2 - x1 - 60, max_lines=3)


def header(draw: ImageDraw.ImageDraw, chapter: str, title: str, subtitle: str, accent: str) -> None:
    draw.rounded_rectangle((70, 54, 220, 108), radius=22, fill=accent)
    draw_text(draw, (95, 61), chapter, font(30, True), "#FFFFFF")
    draw_text(draw, (70, 140), title, font(70, True), INK, max_width=760, max_lines=2)
    draw_text(draw, (73, 305), subtitle, font(34), MUTED, max_width=650, max_lines=2)


def draw_mini_window(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, accent: str) -> None:
    rounded(draw, box, fill=DARK, outline="#1F2937", radius=30, shadow=True)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1, x2, y1 + 70), radius=30, fill="#1F2937")
    draw.rectangle((x1, y1 + 44, x2, y1 + 70), fill="#1F2937")
    for i, color in enumerate([RED, YELLOW, GREEN]):
        draw.ellipse((x1 + 28 + i * 34, y1 + 24, x1 + 48 + i * 34, y1 + 44), fill=color)
    draw_text(draw, (x1 + 140, y1 + 22), title, font(24, True), "#E5E7EB", max_width=x2 - x1 - 180, max_lines=1)


def save(img: Image.Image, rel_path: str) -> None:
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    print(path.relative_to(ROOT).as_posix())


def ch07_cover() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    header(d, "CH07", "PyGame 游戏开发", "把键盘、规则和反馈连成一个可玩的系统。", BLUE)
    x = 72
    y = 430
    for t, c in [("事件循环", BLUE), ("碰撞判定", GREEN), ("即时反馈", ORANGE)]:
        x = pill(d, (x, y), t, c)

    draw_mini_window(d, (820, 95, 1510, 670), "catch_the_ball.py", BLUE)
    d = ImageDraw.Draw(img)
    d.text((870, 195), "Score  12      Lives  3", font=font(30, True), fill="#E5E7EB")
    d.rounded_rectangle((900, 570, 1190, 603), radius=16, fill=BLUE)
    d.ellipse((1190, 270, 1270, 350), fill=ORANGE, outline="#FED7AA", width=6)
    d.line((1230, 350, 1160, 570), fill="#94A3B8", width=3)
    for cx, cy, r, c in [(990, 300, 13, CYAN), (1360, 220, 10, GREEN), (1060, 435, 8, PURPLE), (1410, 480, 11, YELLOW)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
    d.text((912, 620), "←  →  控制挡板", font=font(25), fill="#CBD5E1")

    steps = [("输入", "键盘事件"), ("更新", "位置速度"), ("判定", "碰撞得分"), ("绘制", "下一帧")]
    sx, sy = 790, 750
    for i, (a, b) in enumerate(steps):
        box = (sx + i * 195, sy, sx + i * 195 + 150, sy + 112)
        rounded(d, box, fill=PAPER, outline=LINE, radius=22, shadow=False)
        draw_text(d, (box[0], box[1] + 20), a, font(30, True), INK, max_width=150, align="center")
        draw_text(d, (box[0], box[1] + 60), b, font(22), MUTED, max_width=150, align="center")
        if i < len(steps) - 1:
            arrow(d, (box[2] + 12, sy + 56), (box[2] + 43, sy + 56), BLUE, 4)
    d.arc((806, 715, 1456, 905), 0, 350, fill=GREEN, width=5)
    arrow(d, (812, 810), (800, 790), GREEN, 5)
    save(img, "python_tutorial_ch07/assets/ch07/ch07_cover.png")


def ch07_story_scene() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (80, 70), "从街机到课堂: 游戏让反馈变得可见", font(58, True), INK)
    draw_text(d, (82, 145), "这一章不是只画动画，而是理解“玩家行动 -> 程序判断 -> 画面回应”的学习闭环。", font(31), MUTED, max_width=1180, max_lines=2)
    events = [
        ("1958", "Tennis for Two", "用物理轨迹把互动搬到屏幕上"),
        ("1972", "Pong", "极简规则也能形成可玩体验"),
        ("1962", "Spacewar!", "程序员文化中的实时互动实验"),
        ("今天", "PyGame", "本科生可以直接写出反馈系统"),
    ]
    colors = [BLUE, ORANGE, PURPLE, GREEN]
    x0, y0 = 90, 255
    for i, (year, title, body) in enumerate(events):
        x = x0 + i * 365
        label_box(d, (x, y0, x + 315, y0 + 210), title, f"{year}: {body}", colors[i], str(i + 1))
        if i < 3:
            arrow(d, (x + 325, y0 + 105), (x + 357, y0 + 105), colors[i], 4)

    rounded(d, (95, 560, 1505, 895), fill="#FDFEFF", outline=LINE, radius=32)
    draw_text(d, (140, 598), "游戏主循环", font(42, True), INK)
    nodes = [
        ("输入", "键盘、鼠标、关闭窗口", BLUE),
        ("状态", "坐标、速度、分数", GREEN),
        ("规则", "边界、碰撞、胜负", ORANGE),
        ("反馈", "画面、声音、提示", PURPLE),
    ]
    centers = [(370, 735), (650, 735), (930, 735), (1210, 735)]
    for (title, body, color), (cx, cy) in zip(nodes, centers):
        d.ellipse((cx - 86, cy - 86, cx + 86, cy + 86), fill=color)
        draw_text(d, (cx - 80, cy - 42), title, font(32, True), "#FFFFFF", max_width=160, align="center")
        draw_text(d, (cx - 84, cy + 2), body, font(21), "#FFFFFF", max_width=168, max_lines=2, align="center")
    for a, b in zip(centers, centers[1:]):
        arrow(d, (a[0] + 95, a[1]), (b[0] - 95, b[1]), DARK, 5)
    d.arc((290, 625, 1295, 875), 15, 345, fill=CYAN, width=5)
    arrow(d, (305, 760), (292, 738), CYAN, 5)
    save(img, "python_tutorial_ch07/assets/ch07/ch07_story_scene.png")


def ch07_feedback_loop() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (78, 68), "反馈回路: 玩家的每一步都被看见", font(58, True), INK)
    draw_text(d, (82, 143), "好的小游戏不是元素多，而是每个动作都得到及时、清楚、可记录的回应。", font(31), MUTED, max_width=1180)
    steps = [
        ("目标", "接住落球"),
        ("输入", "左右移动"),
        ("判定", "是否碰到"),
        ("反馈", "得分或失误"),
        ("再试", "难度微调"),
    ]
    colors = [BLUE, CYAN, ORANGE, GREEN, PURPLE]
    x0, y0 = 95, 300
    for i, (a, b) in enumerate(steps):
        box = (x0 + i * 285, y0, x0 + i * 285 + 220, y0 + 170)
        label_box(d, box, a, b, colors[i], str(i + 1))
        if i < len(steps) - 1:
            arrow(d, (box[2] + 15, y0 + 85), (box[2] + 55, y0 + 85), colors[i], 5)

    rounded(d, (135, 590, 735, 855), fill=PAPER, outline=LINE, radius=28)
    draw_text(d, (175, 628), "设计检查单", font(39, True), INK)
    checklist = [("及时", "动作后立刻变化"), ("清楚", "分数、生命值可见"), ("可记录", "每轮结果能复盘")]
    for i, (a, b) in enumerate(checklist):
        y = 695 + i * 54
        d.ellipse((178, y, 212, y + 34), fill=GREEN)
        d.line((186, y + 17, 195, y + 26, 207, y + 8), fill="#FFFFFF", width=4)
        d.text((230, y - 3), a, font=font(29, True), fill=INK)
        d.text((315, y - 1), b, font=font(27), fill=MUTED)

    rounded(d, (845, 590, 1465, 855), fill="#111827", outline="#1F2937", radius=28)
    d.text((890, 632), "score += 1", font=font(32, True), fill="#93C5FD")
    d.text((890, 694), "speed += 0.25", font=font(32, True), fill="#86EFAC")
    d.text((890, 756), "draw_text('Nice!')", font=font(32, True), fill="#FDBA74")
    d.text((1212, 790), "反馈写进代码", font=font(25), fill="#CBD5E1")
    save(img, "python_tutorial_ch07/assets/ch07/ch07_feedback_playground_loop.png")


def ch07_catch_the_ball() -> None:
    img = Image.new("RGB", (1400, 900), "#F6F8FB")
    d = ImageDraw.Draw(img)
    rounded(d, (80, 60, 1320, 820), fill="#0F172A", outline="#1E293B", radius=34)
    d.rounded_rectangle((80, 60, 1320, 130), radius=34, fill="#111827")
    d.rectangle((80, 105, 1320, 130), fill="#111827")
    for i, c in enumerate([RED, YELLOW, GREEN]):
        d.ellipse((120 + i * 36, 88, 142 + i * 36, 110), fill=c)
    d.text((240, 84), "catch_the_ball.py", font=font(28, True), fill="#E5E7EB")
    d.text((140, 165), "Score: 12", font=font(34, True), fill="#E5E7EB")
    d.text((1080, 165), "Lives: 3", font=font(34, True), fill="#E5E7EB")
    d.rounded_rectangle((505, 718, 895, 756), radius=18, fill=BLUE)
    d.ellipse((720, 318, 800, 398), fill=ORANGE, outline="#FED7AA", width=6)
    d.line((760, 398, 705, 718), fill="#94A3B8", width=4)
    for cx, cy, r, c in [(305, 260, 10, CYAN), (1120, 300, 12, GREEN), (410, 520, 8, PURPLE), (1010, 560, 11, YELLOW)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c)
    d.text((540, 775), "←  →  移动挡板", font=font(30), fill="#CBD5E1")

    callouts = [
        ((760, 318), (960, 255), "落球", "每一帧向下移动"),
        ((700, 718), (250, 690), "挡板", "键盘事件改变 x 坐标"),
        ((140, 165), (250, 235), "分数", "碰撞成功立即反馈"),
        ((1080, 165), (955, 235), "生命值", "漏接时扣减并重置"),
    ]
    for start, pos, title, body in callouts:
        px, py = pos
        rounded(d, (px, py, px + 260, py + 118), fill=PAPER, outline=LINE, radius=20)
        d.text((px + 22, py + 18), title, font=font(27, True), fill=INK)
        draw_text(d, (px + 22, py + 55), body, font(22), MUTED, max_width=215, max_lines=2)
        arrow(d, (px + 130, py + 118), start, CYAN, 3)
    img.save(ROOT / "python_tutorial_ch07/assets/ch07/ch07_catch_the_ball.png", "PNG", optimize=True)
    print("python_tutorial_ch07/assets/ch07/ch07_catch_the_ball.png")


def ch08_cover() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    header(d, "CH08", "Web 爬虫与数据采集", "从网页请求到结构化数据，先学规则，再写代码。", CYAN)
    x = 72
    for t, c in [("尊重 robots", GREEN), ("限速访问", ORANGE), ("记录来源", PURPLE)]:
        x = pill(d, (x, 430), t, c)

    nodes = [
        ((780, 155, 1035, 315), "网页", "HTML 文档", BLUE),
        ((1130, 155, 1435, 315), "请求", "requests.get()", CYAN),
        ((780, 500, 1035, 660), "解析", "BeautifulSoup", ORANGE),
        ((1130, 500, 1435, 660), "保存", "CSV / JSON", GREEN),
    ]
    for box, title, body, color in nodes:
        label_box(d, box, title, body, color)
    arrow(d, (1038, 235), (1120, 235), CYAN, 6)
    arrow(d, (1280, 320), (1280, 488), CYAN, 6)
    arrow(d, (1120, 580), (1045, 580), CYAN, 6)
    arrow(d, (905, 488), (905, 330), CYAN, 6)

    rounded(d, (720, 740, 1480, 885), fill="#111827", outline="#1F2937", radius=26)
    d.text((760, 780), "title = soup.select_one('h1').get_text(strip=True)", font=font(28, True), fill="#93C5FD")
    d.text((760, 830), "writer.writerow({'title': title, 'source': url})", font=font(28, True), fill="#86EFAC")
    save(img, "python_tutorial_ch08/assets/ch08/ch08_cover.png")


def ch08_story_scene() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (78, 68), "一张网页怎样变成一行数据", font(58, True), INK)
    draw_text(d, (82, 143), "爬虫不是“偷网页”，而是按公开规则读取信息、抽取字段、留下来源。", font(31), MUTED, max_width=1180)

    draw_mini_window(d, (90, 255, 560, 660), "example.edu/news", BLUE)
    d.rectangle((135, 360, 515, 400), fill="#E5E7EB")
    d.rectangle((135, 430, 470, 455), fill="#CBD5E1")
    d.rectangle((135, 485, 520, 510), fill="#CBD5E1")
    d.rectangle((135, 540, 390, 565), fill="#CBD5E1")
    d.text((140, 305), "浏览器看到的是页面", font=font(26, True), fill="#E5E7EB")

    label_box(d, (665, 255, 990, 420), "请求", "带上 User-Agent，控制访问频率", CYAN, "1")
    label_box(d, (665, 495, 990, 660), "解析", "用选择器找到标题、链接、时间", ORANGE, "2")
    label_box(d, (1095, 375, 1470, 540), "数据表", "一行记录包含字段和来源 URL", GREEN, "3")
    arrow(d, (575, 455), (650, 340), CYAN, 6)
    arrow(d, (825, 425), (825, 485), ORANGE, 6)
    arrow(d, (1000, 575), (1080, 470), GREEN, 6)

    rounded(d, (170, 730, 1430, 885), fill=PAPER, outline=LINE, radius=28)
    draw_text(d, (220, 767), "人文线索", font(38, True), INK)
    draw_text(
        d,
        (420, 762),
        "Web 的初衷是共享知识。写爬虫时，同样要把“可获得”与“可尊重”分清楚。",
        font(31),
        MUTED,
        max_width=850,
        max_lines=2,
    )
    save(img, "python_tutorial_ch08/assets/ch08/ch08_story_scene.png")


def ch08_pitfall_map() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (80, 68), "爬虫常见坑: 先判断，再请求", font(58, True), INK)
    draw_text(d, (83, 143), "每个问题都对应一个可执行的修复动作，避免把网络波动误当成代码能力问题。", font(31), MUTED, max_width=1180)
    items = [
        ("robots.txt", "先查看站点规则", BLUE),
        ("请求太快", "加 sleep 与重试", ORANGE),
        ("JS 渲染", "先找接口或静态数据", PURPLE),
        ("乱码", "检查 encoding", GREEN),
        ("超时", "设置 timeout", CYAN),
        ("路径混乱", "统一输出目录", RED),
    ]
    for i, (title, body, color) in enumerate(items):
        row, col = divmod(i, 3)
        x, y = 95 + col * 500, 255 + row * 285
        label_box(d, (x, y, x + 430, y + 210), title, body, color, str(i + 1))
    rounded(d, (260, 850, 1340, 925), fill="#111827", outline="#1F2937", radius=24)
    draw_text(d, (300, 867), "原则: 慢一点、清楚一点、可复现一点。", font(34, True), "#E5E7EB", max_width=1000, max_lines=1, align="center")
    save(img, "python_tutorial_ch08/assets/ch08/ch08_pitfall_map.png")


def ch09_cover() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    header(d, "CH09", "图像处理", "把照片拆成像素，再用程序完成可复查的变化。", PURPLE)
    x = 72
    for t, c in [("像素矩阵", BLUE), ("颜色通道", GREEN), ("批量处理", ORANGE)]:
        x = pill(d, (x, 430), t, c)

    rounded(d, (780, 110, 1470, 720), fill=PAPER, outline=LINE, radius=30)
    for r in range(8):
        for c in range(10):
            color = ["#2563EB", "#16A34A", "#F97316", "#7C3AED", "#FBBF24"][(r + c) % 5]
            d.rounded_rectangle((835 + c * 48, 180 + r * 48, 875 + c * 48, 220 + r * 48), radius=8, fill=color)
    d.text((820, 610), "像素不是装饰，是可以计算的数据。", font=font(31, True), fill=INK)
    steps = [("打开", BLUE), ("像素", GREEN), ("变换", ORANGE), ("保存", PURPLE)]
    for i, (name, color) in enumerate(steps):
        x0 = 760 + i * 190
        rounded(d, (x0, 790, x0 + 145, 880), fill=PAPER, outline=LINE, radius=22, shadow=False)
        draw_text(d, (x0, 810), name, font(31, True), color, max_width=145, align="center")
        if i < len(steps) - 1:
            arrow(d, (x0 + 155, 835), (x0 + 185, 835), color, 4)
    save(img, "python_tutorial_ch09/assets/ch09/ch09_cover.png")


def ch09_story_scene() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (78, 68), "从相机到像素: 图像是可计算的证据", font(56, True), INK)
    draw_text(d, (82, 143), "这一章把视觉经验、科学图像和 Pillow 代码放在同一条线索里。", font(31), MUTED, max_width=1180)
    events = [
        ("早期摄影", "把现实留在介质上", BLUE),
        ("数字扫描", "把画面转成采样点", CYAN),
        ("颜色研究", "理解通道与感知", ORANGE),
        ("Pillow", "用代码批量复现处理", GREEN),
    ]
    for i, (title, body, color) in enumerate(events):
        x, y = 105 + i * 365, 265
        label_box(d, (x, y, x + 315, y + 200), title, body, color, str(i + 1))
        if i < 3:
            arrow(d, (x + 325, y + 100), (x + 357, y + 100), color, 4)

    rounded(d, (135, 575, 1465, 875), fill=PAPER, outline=LINE, radius=30)
    draw_text(d, (180, 615), "处理流程", font(40, True), INK)
    panels = [
        ("原图", "#93C5FD"),
        ("裁剪", "#86EFAC"),
        ("增强", "#FDBA74"),
        ("对比报告", "#C4B5FD"),
    ]
    for i, (name, color) in enumerate(panels):
        x = 300 + i * 260
        d.rounded_rectangle((x, 700, x + 170, 800), radius=20, fill=color)
        draw_text(d, (x, 727), name, font(29, True), DARK, max_width=170, align="center")
        if i < 3:
            arrow(d, (x + 180, 750), (x + 240, 750), MUTED, 4)
    save(img, "python_tutorial_ch09/assets/ch09/ch09_story_scene.png")


def ch09_roadmap() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (80, 68), "第9章学习路线: 从一张图到一份报告", font(56, True), INK)
    draw_text(d, (83, 143), "路线图按真实任务顺序排列，先能跑通，再追求批量和美观。", font(31), MUTED, max_width=1180)
    steps = [
        ("打开图片", "Image.open"),
        ("读取信息", "尺寸、模式"),
        ("裁剪缩放", "保持比例"),
        ("颜色处理", "灰度、滤镜"),
        ("批量循环", "处理文件夹"),
        ("前后对比", "证明效果"),
        ("生成报告", "交付结果"),
    ]
    colors = [BLUE, CYAN, GREEN, ORANGE, PURPLE, RED, DARK]
    for i, (title, body) in enumerate(steps):
        row = 0 if i < 4 else 1
        col = i if i < 4 else i - 4
        x = 90 + col * 365
        y = 265 + row * 300
        label_box(d, (x, y, x + 305, y + 200), title, body, colors[i], str(i + 1))
        if i in [0, 1, 2, 4, 5]:
            arrow(d, (x + 315, y + 100), (x + 355, y + 100), colors[i], 4)
        if i == 3:
            arrow(d, (x + 150, y + 210), (90 + 2 * 365 + 150, y + 285), colors[i], 4)
    save(img, "python_tutorial_ch09/assets/ch09/ch09_roadmap.png")


def ch09_pitfall_map() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (80, 68), "图像处理常见坑: 保护原图，验证结果", font(56, True), INK)
    draw_text(d, (83, 143), "看见结果不等于处理正确，务必让代码留下可检查的证据。", font(31), MUTED, max_width=1180)
    items = [
        ("覆盖原图", "输出到新目录", RED),
        ("比例变形", "用 thumbnail 或等比缩放", ORANGE),
        ("通道模式", "RGBA 转 RGB 再保存", PURPLE),
        ("路径错误", "先 mkdir 再写入", BLUE),
        ("文件太大", "控制尺寸与质量", CYAN),
        ("没有复核", "生成前后对比图", GREEN),
    ]
    for i, (title, body, color) in enumerate(items):
        row, col = divmod(i, 3)
        x, y = 95 + col * 500, 255 + row * 285
        label_box(d, (x, y, x + 430, y + 210), title, body, color, str(i + 1))
    save(img, "python_tutorial_ch09/assets/ch09/ch09_pitfall_map.png")


def ch10_cover() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    header(d, "CH10", "Office 自动化", "把重复办公变成可复查、可交付的文档流水线。", GREEN)
    x = 72
    for t, c in [("Word", BLUE), ("Excel", GREEN), ("PPT", ORANGE), ("打包交付", PURPLE)]:
        x = pill(d, (x, 430), t, c)
    nodes = [
        ((760, 170, 995, 330), "数据", "CSV / Excel", CYAN),
        ((1095, 170, 1395, 330), "Python", "读取、清洗、生成", BLUE),
        ((745, 535, 960, 700), "Word", "实验报告", PURPLE),
        ((1000, 535, 1215, 700), "Excel", "统计表", GREEN),
        ((1255, 535, 1470, 700), "PPT", "汇报页", ORANGE),
    ]
    for box, title, body, color in nodes:
        label_box(d, box, title, body, color)
    arrow(d, (1005, 250), (1085, 250), CYAN, 6)
    for x2 in [855, 1110, 1365]:
        arrow(d, (1245, 340), (x2, 525), BLUE, 5)
    rounded(d, (765, 790, 1465, 895), fill="#111827", outline="#1F2937", radius=26)
    d.text((805, 820), "一份数据，多种文档；一次生成，多处复核。", font=font(33, True), fill="#E5E7EB")
    save(img, "python_tutorial_ch10/assets/ch10/ch10_cover.png")


def ch10_roadmap() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (80, 68), "第10章路线: 自动化交付，不只是生成文件", font(56, True), INK)
    draw_text(d, (83, 143), "每一步都对应一个产物，方便本科生检查哪里成功、哪里需要返工。", font(31), MUTED, max_width=1180)
    steps = [
        ("准备数据", "students.xlsx"),
        ("设计模板", "报告结构"),
        ("生成 Word", "docx 报告"),
        ("生成 Excel", "统计工作簿"),
        ("生成 PPT", "汇报演示"),
        ("打包复核", "zip + 清单"),
    ]
    colors = [CYAN, BLUE, PURPLE, GREEN, ORANGE, RED]
    for i, (title, body) in enumerate(steps):
        row, col = divmod(i, 3)
        x, y = 125 + col * 475, 260 + row * 300
        label_box(d, (x, y, x + 390, y + 205), title, body, colors[i], str(i + 1))
        if col < 2:
            arrow(d, (x + 400, y + 102), (x + 455, y + 102), colors[i], 4)
        elif row == 0:
            arrow(d, (x + 190, y + 215), (125 + 2 * 475 + 190, y + 285), colors[i], 4)
    save(img, "python_tutorial_ch10/assets/ch10/ch10_roadmap.png")


def ch10_core_metaphor() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (80, 68), "核心比喻: Python 是小型文档工坊", font(58, True), INK)
    draw_text(d, (83, 143), "不要把办公自动化想成魔法按钮，它更像一条看得见的生产线。", font(31), MUTED, max_width=1180)
    stations = [
        ("原料区", "数据表、图片、文字", CYAN),
        ("模板台", "标题、表格、占位符", BLUE),
        ("生成器", "docx / xlsx / pptx", GREEN),
        ("质检台", "打开预览、核对数量", ORANGE),
        ("交付箱", "压缩包、材料清单", PURPLE),
    ]
    y = 360
    for i, (title, body, color) in enumerate(stations):
        x = 70 + i * 300
        rounded(d, (x, y, x + 245, y + 240), fill=PAPER, outline=LINE, radius=28)
        d.rounded_rectangle((x + 30, y + 30, x + 95, y + 95), radius=18, fill=color)
        draw_text(d, (x + 115, y + 38), title, font(31, True), INK, max_width=110, max_lines=1)
        draw_text(d, (x + 32, y + 120), body, font(25), MUTED, max_width=180, max_lines=3)
        if i < len(stations) - 1:
            arrow(d, (x + 255, y + 120), (x + 292, y + 120), color, 5)
    rounded(d, (205, 730, 1395, 855), fill="#111827", outline="#1F2937", radius=28)
    draw_text(d, (245, 766), "判断标准: 同一份输入重复运行，能得到同样清楚的输出。", font(34, True), "#E5E7EB", max_width=1100, align="center")
    save(img, "python_tutorial_ch10/assets/ch10/ch10_core_metaphor.png")


def ch10_pitfall_map() -> None:
    img = canvas()
    d = ImageDraw.Draw(img)
    draw_text(d, (80, 68), "Office 自动化常见坑: 生成之后一定要验收", font(56, True), INK)
    draw_text(d, (83, 143), "办公文件看似生成成功，也可能字段错、路径错、文件被占用。用清单兜住风险。", font(31), MUTED, max_width=1180)
    items = [
        ("文件被占用", "关闭 Word/Excel 再写入", RED),
        ("路径写错", "统一 output 目录", BLUE),
        ("模板字段不一致", "先列字段清单", PURPLE),
        ("数据缺失", "生成前做校验", ORANGE),
        ("顺序不可复现", "固定排序规则", CYAN),
        ("没有打开验收", "抽查生成文件", GREEN),
    ]
    for i, (title, body, color) in enumerate(items):
        row, col = divmod(i, 3)
        x, y = 95 + col * 500, 255 + row * 285
        label_box(d, (x, y, x + 430, y + 210), title, body, color, str(i + 1))
    save(img, "python_tutorial_ch10/assets/ch10/ch10_pitfall_map.png")


def main() -> None:
    ch07_cover()
    ch07_story_scene()
    ch07_feedback_loop()
    ch07_catch_the_ball()
    ch08_cover()
    ch08_story_scene()
    ch08_pitfall_map()
    ch09_cover()
    ch09_story_scene()
    ch09_roadmap()
    ch09_pitfall_map()
    ch10_cover()
    ch10_roadmap()
    ch10_core_metaphor()
    ch10_pitfall_map()


if __name__ == "__main__":
    main()
