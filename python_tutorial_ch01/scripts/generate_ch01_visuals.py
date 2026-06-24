from __future__ import annotations

from pathlib import Path
import os
import re
import subprocess
import sys

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps
except ModuleNotFoundError as exc:
    raise SystemExit(
        "This visual generator needs Pillow. Install it with: python -m pip install pillow"
    ) from exc


ROOT = Path.cwd()
if not (ROOT / "assets" / "ch01").exists():
    ROOT = Path(__file__).resolve().parents[1]

ASSET_DIR = ROOT / "assets" / "ch01"
WEB_DIR = ASSET_DIR / "web"
UTF8_ENV = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}

W, H = 1800, 1120
BG = "#F7F8FB"
LINE = "#D8E0EC"
BLUE = "#2F6BFF"
GREEN = "#24A06B"
ORANGE = "#F28C28"
PURPLE = "#7A5AF8"
RED = "#E84C61"
CYAN = "#18A9B5"
YELLOW = "#E6A600"
INK = "#162033"


def canvas(width: int = W, height: int = H):
    im = Image.new("RGB", (width, height), BG)
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, name: str):
    im.save(ASSET_DIR / name, optimize=True, quality=95)


def trim_near_white(im: Image.Image, tolerance: int = 18, pad: int = 12) -> Image.Image:
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, "#FFFFFF")
    diff = ImageChops.difference(rgb, bg).convert("L")
    mask = diff.point(lambda p: 255 if p > tolerance else 0)
    bbox = mask.getbbox()
    if not bbox:
        return rgb
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(rgb.width, bbox[2] + pad)
    bottom = min(rgb.height, bbox[3] + pad)
    return rgb.crop((left, top, right, bottom))


def load_font(size: int, mono: bool = False):
    candidates = []
    if mono:
        candidates.extend([
            Path("C:/Windows/Fonts/consola.ttf"),
            Path("C:/Windows/Fonts/DejaVuSansMono.ttf"),
        ])
    candidates.extend([
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/seguisym.ttf"),
    ])
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def text_size(d: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    if not text:
        return 0, 0
    box = d.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def _tokens(line: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./:\\#-]+|[\u4e00-\u9fff]|[^\sA-Za-z0-9_./:\\#\-\u4e00-\u9fff]|\s+", line)


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
):
    best = None
    for font_size in range(size, min_size - 1, -1):
        fnt = load_font(font_size)
        if bold:
            for candidate in [Path("C:/Windows/Fonts/msyhbd.ttc"), Path("C:/Windows/Fonts/simhei.ttf")]:
                if candidate.exists():
                    fnt = ImageFont.truetype(str(candidate), font_size)
                    break
        lines: list[str] = []
        for para in text.splitlines() or [""]:
            lines.extend(wrap_line(d, para, fnt, max_width))
        base_h = max(text_size(d, "汉字Ag", fnt)[1], int(font_size * 0.9))
        spacing = max(4, int(font_size * 0.34))
        height = len(lines) * base_h + max(0, len(lines) - 1) * spacing
        if height <= max_height:
            return fnt, lines, base_h, spacing
        best = (fnt, lines, base_h, spacing)
    return best


def draw_text(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    text: str,
    size: int = 32,
    min_size: int = 18,
    fill: str = INK,
    bold: bool = False,
    align: str = "left",
    valign: str = "top",
):
    x1, y1, x2, y2 = xy
    fnt, lines, line_h, spacing = fit_lines(d, text, x2 - x1, y2 - y1, size, min_size, bold)
    total_h = len(lines) * line_h + max(0, len(lines) - 1) * spacing
    if valign == "center":
        y = y1 + (y2 - y1 - total_h) // 2
    elif valign == "bottom":
        y = y2 - total_h
    else:
        y = y1
    for line in lines:
        width, _ = text_size(d, line, fnt)
        if align == "center":
            x = x1 + (x2 - x1 - width) // 2
        elif align == "right":
            x = x2 - width
        else:
            x = x1
        d.text((x, y), line, fill=fill, font=fnt)
        y += line_h + spacing


def title_block(d: ImageDraw.ImageDraw, heading: str, subtitle: str = ""):
    draw_text(d, (120, 68, 1680, 145), heading, size=54, min_size=36, fill=INK, bold=True, align="center", valign="center")
    if subtitle:
        draw_text(d, (190, 148, 1610, 205), subtitle, size=28, min_size=22, fill="#667085", align="center", valign="center")


def labeled_card(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    tag: str,
    heading: str,
    body: str,
    color: str,
):
    shadow(d, xy, radius=24)
    rounded(d, xy, fill="#FFFFFF", outline=LINE, radius=24, width=2)
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1, y1, x1 + 14, y2), radius=7, fill=color)
    d.ellipse((x1 + 30, y1 + 26, x1 + 84, y1 + 80), fill=color)
    draw_text(d, (x1 + 30, y1 + 26, x1 + 84, y1 + 80), tag, size=24, min_size=18, fill="#FFFFFF", bold=True, align="center", valign="center")
    draw_text(d, (x1 + 104, y1 + 25, x2 - 30, y1 + 80), heading, size=31, min_size=22, fill=INK, bold=True, valign="center")
    draw_text(d, (x1 + 34, y1 + 92, x2 - 30, y2 - 24), body, size=24, min_size=18, fill="#667085")


def rounded(d: ImageDraw.ImageDraw, xy, fill="#FFFFFF", outline=LINE, radius=26, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def shadow(d: ImageDraw.ImageDraw, xy, radius=26):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#DCE2EC")


def arrow(d: ImageDraw.ImageDraw, start, end, color="#98A5B8", width=5):
    x1, y1 = start
    x2, y2 = end
    d.line((x1, y1, x2, y2), fill=color, width=width)
    if abs(x2 - x1) >= abs(y2 - y1):
        sign = 1 if x2 >= x1 else -1
        pts = [(x2, y2), (x2 - sign * 20, y2 - 11), (x2 - sign * 20, y2 + 11)]
    else:
        sign = 1 if y2 >= y1 else -1
        pts = [(x2, y2), (x2 - 11, y2 - sign * 20), (x2 + 11, y2 - sign * 20)]
    d.polygon(pts, fill=color)


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
        resampling = getattr(Image, "Resampling", Image).LANCZOS
        shown = ImageOps.contain(raw, (frame[2] - frame[0] - 30, frame[3] - frame[1] - 30), method=resampling)
        x = frame[0] + (frame[2] - frame[0] - shown.width) // 2
        y = frame[1] + (frame[3] - frame[1] - shown.height) // 2
        im.paste(shown, (x, y))
    else:
        d.line((760, 470, 1040, 650), fill=RED, width=12)
        d.line((1040, 470, 760, 650), fill=RED, width=12)

    save(im, output_name)


def terminal_raw(
    output_name: str,
    title: str,
    lines: list[tuple[str, str]],
    width: int = 1320,
    height: int = 820,
    font_size: int = 24,
    max_chars: int = 78,
    cjk: bool = False,
):
    im = Image.new("RGB", (width, height), "#113A6B")
    d = ImageDraw.Draw(im)
    title_font = load_font(22, mono=False)
    mono_font = load_font(font_size, mono=not cjk)
    d.rectangle((0, 0, width, 42), fill="#E7EEF7")
    d.text((18, 9), title, fill="#1B2733", font=title_font)
    y = 70
    for kind, text in lines:
        if len(text) > max_chars:
            text = text[: max_chars - 3] + "..."
        if kind == "prompt":
            color = "#59D9FF"
        elif kind == "success":
            color = "#68F06A"
        elif kind == "muted":
            color = "#B7CAE6"
        else:
            color = "#F3F8FF"
        d.text((24, y), text, fill=color, font=mono_font)
        y += max(30, font_size + 12)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    im.save(WEB_DIR / output_name, optimize=True, quality=95)


def command_output(args: list[str], fallback: str = "not available") -> list[str]:
    try:
        completed = subprocess.run(args, capture_output=True, text=True, timeout=8)
    except (OSError, subprocess.SubprocessError):
        return [fallback]
    output = (completed.stdout or completed.stderr or "").strip()
    if not output:
        return [fallback]
    return [line.rstrip() for line in output.splitlines()[:5]]


def powershell_python_locator_raw():
    py_version = command_output([sys.executable, "--version"])
    py_path = command_output([sys.executable, "-c", "import sys; print(sys.executable)"])
    pip_version = command_output([sys.executable, "-m", "pip", "--version"])
    where_python = command_output(["where.exe", "python"], "where.exe python did not return a path")
    py_launcher = command_output(["py", "-0p"], "py launcher is not available on this computer")
    where_pycharm = command_output(["where.exe", "pycharm64.exe"], "pycharm64.exe is not on PATH")
    py_launcher = [
        "-V:3.8        旧版本路径较长，已略去"
        if "decoder1553b" in line or "�" in line
        else line
        for line in py_launcher
    ]
    where_pycharm = [
        "未在 PATH 中找到 pycharm64.exe；这不影响从开始菜单打开 PyCharm"
        if line.startswith("INFO: Could not find")
        else line
        for line in where_pycharm
    ]
    lines: list[tuple[str, str]] = [
        ("prompt", r"PS> py -0p"),
        *[("out", line) for line in py_launcher],
        ("prompt", r"PS> python --version"),
        *[("out", line) for line in py_version],
        ("prompt", r'PS> python -c "import sys; print(sys.executable)"'),
        *[("out", line) for line in py_path],
        ("prompt", r"PS> python -m pip --version"),
        *[("out", line) for line in pip_version],
        ("prompt", r"PS> where.exe python"),
        *[("out", line) for line in where_python],
        ("prompt", r"PS> where.exe pycharm64.exe"),
        *[("out", line) for line in where_pycharm],
    ]
    terminal_raw(
        "powershell_python_locator.png",
        "Windows PowerShell - 核对 Python 路径",
        lines[:20],
        width=1500,
        height=960,
        font_size=22,
        max_chars=88,
        cjk=True,
    )


def powershell_create_venv_raw():
    terminal_raw(
        "powershell_create_venv.png",
        "Windows PowerShell - 创建项目环境 .venv",
        [
            ("prompt", r"PS> cd C:\PythonTutorial\PythonMarkdownBook\python_tutorial_ch01"),
            ("prompt", r"PS> python -m venv .venv"),
            ("prompt", r"PS> .\.venv\Scripts\Activate.ps1"),
            ("prompt", r"(.venv) PS> python --version"),
            ("out", "Python 3.11.9"),
            ("prompt", r"(.venv) PS> python -m pip install -U pip"),
            ("out", "Requirement already satisfied: pip in .\\.venv\\Lib\\site-packages"),
            ("prompt", r"(.venv) PS> python -m pip --version"),
            ("out", r"pip 24.0 from .\.venv\Lib\site-packages\pip (python 3.11)"),
            ("prompt", r"(.venv) PS> python code\ch01\01_hello_python.py"),
            ("success", "Hello, Python!"),
        ],
    )


def powershell_policy_fallback_raw():
    pyver = f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    terminal_raw(
        "powershell_policy_fallback.png",
        "Windows PowerShell - 不激活也能指定 .venv",
        [
            ("prompt", r"PS> Get-ExecutionPolicy -List"),
            ("out", "        Scope ExecutionPolicy"),
            ("out", "        ----- ---------------"),
            ("out", "MachinePolicy       Undefined"),
            ("out", "   UserPolicy       Undefined"),
            ("out", "      Process       Undefined"),
            ("out", "  CurrentUser    RemoteSigned"),
            ("out", " LocalMachine    RemoteSigned"),
            ("prompt", r"PS> Test-Path .\.venv\Scripts\python.exe"),
            ("success", "True"),
            ("prompt", r"PS> .\.venv\Scripts\python.exe --version"),
            ("out", pyver),
            ("prompt", r"PS> .\.venv\Scripts\python.exe code\ch01\02_environment_check.py"),
            ("out", r"Executable: .\.venv\Scripts\python.exe"),
            ("out", r"Project: python_tutorial_ch01"),
        ],
    )


def powershell_full_runtime_check_raw():
    def run(args: list[str], max_lines: int = 6) -> list[str]:
        try:
            completed = subprocess.run(
                args,
                cwd=ROOT,
                env=UTF8_ENV,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=12,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return [f"command failed: {exc}"]
        output = (completed.stdout or completed.stderr or "").strip()
        if not output:
            return ["<no output>"]
        lines = [line.rstrip() for line in output.splitlines()]
        return lines[:max_lines]

    checks: list[tuple[str, list[str], int]] = [
        ("python --version", [sys.executable, "--version"], 1),
        ("python -m pip --version", [sys.executable, "-m", "pip", "--version"], 2),
        (r"python code\ch01\01_hello_python.py", [sys.executable, "code/ch01/01_hello_python.py"], 4),
        (r"python code\ch01\02_environment_check.py", [sys.executable, "code/ch01/02_environment_check.py"], 10),
        (r"python code\ch01\04_show_me_the_python.py", [sys.executable, "code/ch01/04_show_me_the_python.py"], 6),
    ]
    lines: list[tuple[str, str]] = [
        ("prompt", rf"PS> cd {ROOT}"),
        ("success", f"Path: {ROOT.name}"),
    ]
    for command, args, max_lines in checks:
        lines.append(("prompt", f"PS> {command}"))
        for line in run(args, max_lines=max_lines):
            kind = "success" if any(token in line for token in ["成功", "完成", "通电", "Hello"]) else "out"
            lines.append((kind, line))
    lines.extend(
        [
            ("prompt", r"PS> Test-Path reports\ch01_environment_log.txt"),
            ("success", str((ROOT / "reports" / "ch01_environment_log.txt").exists())),
        ]
    )
    terminal_raw(
        "powershell_full_runtime_check.png",
        "Windows PowerShell - 第1章通电检查",
        lines[:28],
        width=1500,
        height=1080,
        font_size=22,
        max_chars=88,
        cjk=True,
    )


def terminal_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=GREEN):
    d.rounded_rectangle((x - 62, y - 44, x + 62, y + 44), radius=14, outline=color, width=8)
    d.line((x - 34, y - 12, x - 12, y, x - 34, y + 12), fill=color, width=7)
    d.line((x + 2, y + 20, x + 36, y + 20), fill=color, width=7)


def file_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=BLUE):
    d.line((x - 40, y - 55, x + 18, y - 55, x + 47, y - 25, x + 47, y + 55, x - 40, y + 55, x - 40, y - 55), fill=color, width=7)
    d.line((x + 18, y - 55, x + 18, y - 25, x + 47, y - 25), fill=color, width=7)
    for yy in (y - 15, y + 10, y + 35):
        d.line((x - 20, yy, x + 25, yy), fill=color, width=5)


def gear_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=ORANGE):
    for dx, dy in [(0, -58), (42, -42), (58, 0), (42, 42), (0, 58), (-42, 42), (-58, 0), (-42, -42)]:
        d.line((x, y, x + dx, y + dy), fill=color, width=8)
    d.ellipse((x - 46, y - 46, x + 46, y + 46), outline=color, width=8)
    d.ellipse((x - 15, y - 15, x + 15, y + 15), fill=color)


def package_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=PURPLE):
    d.polygon([(x, y - 60), (x + 56, y - 28), (x + 56, y + 35), (x, y + 68), (x - 56, y + 35), (x - 56, y - 28)], outline=color, fill=None)
    d.line((x - 56, y - 28, x, y + 5, x + 56, y - 28), fill=color, width=7)
    d.line((x, y + 5, x, y + 68), fill=color, width=7)


def folder_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=CYAN):
    d.rounded_rectangle((x - 70, y - 35, x + 70, y + 55), radius=14, outline=color, width=8)
    d.line((x - 70, y - 35, x - 30, y - 65, x + 10, y - 65, x + 35, y - 35), fill=color, width=8)


def card_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=YELLOW):
    d.rounded_rectangle((x - 60, y - 46, x + 60, y + 46), radius=16, outline=color, width=8)
    for yy in (y - 18, y + 8, y + 30):
        d.line((x - 35, yy, x + 36, yy), fill=color, width=5)


def warning_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=RED):
    d.polygon([(x, y - 60), (x + 62, y + 48), (x - 62, y + 48)], outline=color, fill=None)
    d.line((x, y - 24, x, y + 16), fill=color, width=8)
    d.ellipse((x - 6, y + 28, x + 6, y + 40), fill=color)


def draw_icon_node(d: ImageDraw.ImageDraw, x: int, y: int, icon, color: str, radius=92):
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill="#FFFFFF", outline=color, width=6)
    icon(d, x, y, color)


def cover():
    photo_plate("ch01_cover.png", "guido_van_rossum_pyconus24.jpg")


def story_timeline():
    photo_plate("ch01_story_timeline.png", "cwi_entrance.jpg")


def knowledge_route():
    photo_plate("ch01_knowledge_route.png", "grace_hopper_univac.jpg")


def core_workshop():
    photo_plate("ch01_core_metaphor_workshop.png", "bbc_broadcasting_house_portland_place.jpg")


def ide_workbench():
    photo_plate("ch01_ide_workbench.png", "stroop_effect_example.png")


def pip_pipeline():
    im, d = canvas()
    title_block(d, "pip 安装要送到同一个 Python", "包安装成功，不等于装进了正在运行的解释器")
    steps = [
        ("1", "选定解释器", "先用 sys.executable 看清这次运行的是哪个 python.exe。", BLUE),
        ("2", "用它调用 pip", "写成 python -m pip install requests，别让 pip 自己找门。", GREEN),
        ("3", "装到对应环境", "第三方包应进入这个解释器的 site-packages。", ORANGE),
        ("4", "再运行验证", "回到脚本里 import requests，能导入才算真正到位。", PURPLE),
    ]
    x0, y, w, h, gap = 95, 370, 360, 310, 70
    for idx, (tag, heading, body, color) in enumerate(steps):
        x = x0 + idx * (w + gap)
        if idx < len(steps) - 1:
            arrow(d, (x + w + 14, y + h // 2), (x + w + gap - 18, y + h // 2), width=5)
        labeled_card(d, (x, y, x + w, y + h), tag, heading, body, color)
    rounded(d, (260, 780, 1540, 890), fill="#EEF6FF", outline="#B8D6FF", radius=24, width=2)
    draw_text(d, (300, 805, 1500, 865), "第一章记住这一句：装包时用 python -m pip，排查时看 sys.executable。", size=30, min_size=23, fill=BLUE, bold=True, align="center", valign="center")
    save(im, "ch01_pip_pipeline.png")


def error_map():
    im, d = canvas()
    title_block(d, "新手常见报错怎么读", "报错不是评价你，它是在告诉你先查哪条线索")
    items = [
        ("语法", "SyntaxError", "先看冒号、括号、引号有没有少。", RED),
        ("名字", "NameError", "变量名拼错、还没赋值，最常见。", ORANGE),
        ("模块", "ModuleNotFound", "包可能没装到当前 Python。", PURPLE),
        ("缩进", "Indentation", "同一层代码缩进要对齐。", BLUE),
        ("文件", "FileNotFound", "先打印当前目录，再核对路径。", GREEN),
        ("类型", "TypeError", "字符串、数字、列表别混着用。", YELLOW),
    ]
    x0, y0, w, h = 110, 285, 510, 205
    for idx, (tag, heading, body, color) in enumerate(items):
        row, col = divmod(idx, 3)
        x = x0 + col * 590
        y = y0 + row * 270
        labeled_card(d, (x, y, x + w, y + h), tag, heading, body, color)
    rounded(d, (270, 865, 1530, 955), fill="#FFF8E8", outline="#F1D08A", radius=22, width=2)
    draw_text(d, (310, 885, 1490, 938), "固定顺序：最后一行看类型，File/line 找位置，回到代码附近改一小处。", size=28, min_size=22, fill="#A46A00", bold=True, align="center", valign="center")
    save(im, "ch01_error_map.png")


def psychology_applications():
    photo_plate("ch01_psychology_applications.png", "wundt_lab.jpg")


def environment_debug_chart():
    im, d = canvas()
    chart = (250, 230, 1550, 890)
    rounded(d, chart, fill="#FFFFFF", radius=28)
    x1, y1, x2, y2 = chart
    values = [95, 82, 68, 55, 42]
    colors = [BLUE, GREEN, ORANGE, PURPLE, RED]
    for i, (value, color) in enumerate(zip(values, colors)):
        y = y1 + 95 + i * 105
        d.rounded_rectangle((x1 + 170, y, x2 - 170, y + 42), radius=21, fill="#E9EEF6")
        d.rounded_rectangle((x1 + 170, y, x1 + 170 + int((x2 - x1 - 340) * value / 100), y + 42), radius=21, fill=color)
        d.ellipse((x1 + 75, y - 12, x1 + 135, y + 48), fill=color)
    save(im, "ch01_environment_debug_chart.png")


def pycharm_interpreter_widget():
    photo_plate("ch01_pycharm_interpreter_widget.png", "pycharm_python_interpreter_widget_dark.png")


def pycharm_new_project():
    photo_plate("ch01_pycharm_new_project.png", "pycharm_create_project.png")


def pycharm_select_interpreter():
    photo_plate("ch01_pycharm_select_interpreter.png", "pycharm_selecting_target_interpreter_dark.png")


def pycharm_virtualenv_setup():
    photo_plate("ch01_pycharm_virtualenv_setup.png", "pycharm_new_virtualenv_environment_dark.png")


def pycharm_existing_virtualenv():
    photo_plate("ch01_pycharm_existing_virtualenv.png", "pycharm_existing_virtualenv_environment_dark.png")


def pycharm_edit_configurations():
    photo_plate("ch01_pycharm_edit_configurations.png", "pycharm_edit_configurations.png")


def pycharm_run_configuration_script():
    photo_plate("ch01_pycharm_run_configuration_script.png", "pycharm_run_configuration_script.png")


def pycharm_modify_run_options():
    photo_plate("ch01_pycharm_modify_run_options.png", "pycharm_modify_run_options.png")


def pycharm_run_widget():
    photo_plate("ch01_pycharm_run_widget.png", "pycharm_run_widget.png")


def pycharm_run_console():
    photo_plate("ch01_pycharm_run_console.png", "pycharm_run_tool_window.png")


def pycharm_main_window():
    photo_plate("ch01_pycharm_main_window.png", "pycharm_main_window.png")


def pycharm_environment_focus():
    im, d = canvas(1800, 1160)
    frames = [
        (120, 100, 1680, 545),
        (120, 615, 1680, 1060),
    ]
    sources = [
        "pycharm_existing_virtualenv_environment_dark.png",
        "pycharm_run_tool_window.png",
    ]
    for frame, image_name in zip(frames, sources):
        shadow(d, frame, radius=28)
        rounded(d, frame, fill="#FFFFFF", radius=28)
        inner = (frame[0] + 28, frame[1] + 28, frame[2] - 28, frame[3] - 28)
        src = WEB_DIR / image_name
        if src.exists():
            raw = Image.open(src)
            raw = ImageOps.exif_transpose(raw).convert("RGB")
            raw = trim_near_white(raw)
            resampling = getattr(Image, "Resampling", Image).LANCZOS
            shown = ImageOps.contain(raw, (inner[2] - inner[0], inner[3] - inner[1]), method=resampling)
            x = inner[0] + (inner[2] - inner[0] - shown.width) // 2
            y = inner[1] + (inner[3] - inner[1] - shown.height) // 2
            im.paste(shown, (x, y))
        else:
            d.line((inner[0], inner[1], inner[2], inner[3]), fill=RED, width=8)
            d.line((inner[2], inner[1], inner[0], inner[3]), fill=RED, width=8)
    save(im, "ch01_pycharm_environment_focus.png")


def runtime_environment_side_by_side():
    im, d = canvas(1800, 920)
    frames = [
        (105, 110, 875, 810),
        (925, 300, 1695, 620),
    ]
    sources = [
        "powershell_full_runtime_check.png",
        "pycharm_run_tool_window.png",
    ]
    for frame, image_name in zip(frames, sources):
        shadow(d, frame, radius=28)
        rounded(d, frame, fill="#FFFFFF", radius=28)
        inner = (frame[0] + 32, frame[1] + 32, frame[2] - 32, frame[3] - 32)
        src = WEB_DIR / image_name
        if src.exists():
            raw = Image.open(src)
            raw = ImageOps.exif_transpose(raw).convert("RGB")
            if "pycharm" in image_name:
                raw = trim_near_white(raw)
            resampling = getattr(Image, "Resampling", Image).LANCZOS
            shown = ImageOps.contain(raw, (inner[2] - inner[0], inner[3] - inner[1]), method=resampling)
            x = inner[0] + (inner[2] - inner[0] - shown.width) // 2
            y = inner[1] + (inner[3] - inner[1] - shown.height) // 2
            im.paste(shown, (x, y))
        else:
            d.line((inner[0], inner[1], inner[2], inner[3]), fill=RED, width=8)
            d.line((inner[2], inner[1], inner[0], inner[3]), fill=RED, width=8)
    save(im, "ch01_runtime_environment_side_by_side.png")


def powershell_environment_check():
    photo_plate("ch01_powershell_environment_check.png", "powershell_python_environment_check.png")


def powershell_local_environment_check():
    photo_plate("ch01_powershell_local_environment_check.png", "local_powershell_environment_check.png")


def powershell_project_navigation():
    photo_plate("ch01_powershell_project_navigation.png", "powershell_project_navigation.png")


def powershell_python_locator():
    powershell_python_locator_raw()
    photo_plate("ch01_powershell_python_locator.png", "powershell_python_locator.png")


def powershell_run_scripts():
    photo_plate("ch01_powershell_run_scripts.png", "powershell_ch01_run_scripts.png")


def powershell_full_runtime_check():
    powershell_full_runtime_check_raw()
    photo_plate("ch01_powershell_full_runtime_check.png", "powershell_full_runtime_check.png")


def powershell_submission_evidence_raw():
    def run(args: list[str], max_lines: int = 5, stdin: str | None = None) -> list[str]:
        try:
            completed = subprocess.run(
                args,
                cwd=ROOT,
                env=UTF8_ENV,
                input=stdin,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=12,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            return [f"command failed: {exc}"]
        output = (completed.stdout or completed.stderr or "").strip()
        if not output:
            return ["<no output>"]
        return [line.rstrip() for line in output.splitlines()[:max_lines]]

    checks: list[tuple[str, list[str], int, str | None]] = [
        (r"python -B code\ch01\01_hello_python.py", [sys.executable, "-B", "code/ch01/01_hello_python.py"], 2, None),
        (r"python -B code\ch01\02_environment_check.py", [sys.executable, "-B", "code/ch01/02_environment_check.py"], 4, None),
        (r"python -B code\ch01\04_show_me_the_python.py", [sys.executable, "-B", "code/ch01/04_show_me_the_python.py"], 4, None),
        (r"'S001`nj' | python -B code\ch01\05_experiment_preview.py", [sys.executable, "-B", "code/ch01/05_experiment_preview.py"], 5, "S001\nj\n"),
    ]
    lines: list[tuple[str, str]] = [
        ("prompt", rf"PS> cd {ROOT}"),
        ("success", f"Path: {ROOT.name}"),
    ]
    for command, args, max_lines, stdin in checks:
        lines.append(("prompt", f"PS> {command}"))
        for line in run(args, max_lines=max_lines, stdin=stdin):
            kind = "success" if any(token in line for token in ["Hello", "成功", "通电", "实验结束", "True"]) else "out"
            lines.append((kind, line))
    lines.extend(
        [
            ("prompt", r"PS> Test-Path reports\ch01_environment_log.txt"),
            ("success", str((ROOT / "reports" / "ch01_environment_log.txt").exists())),
        ]
    )
    terminal_raw(
        "powershell_submission_evidence.png",
        "Windows PowerShell - 第1章学习成果记录",
        lines[:24],
        width=1500,
        height=1080,
        font_size=22,
        max_chars=88,
        cjk=True,
    )


def powershell_submission_evidence():
    powershell_submission_evidence_raw()
    photo_plate("ch01_powershell_submission_evidence.png", "powershell_submission_evidence.png")


def powershell_pathlib_demo_raw():
    code = (
        "from pathlib import Path\n"
        "root = Path.cwd()\n"
        "data_file = root / 'data' / 'demo.txt'\n"
        "print('cwd      =', root)\n"
        "print('data     =', data_file)\n"
        "print('name     =', data_file.name)\n"
        "print('parent   =', data_file.parent)\n"
        "print('suffix   =', data_file.suffix)\n"
    )
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code],
            cwd=ROOT,
            env=UTF8_ENV,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=8,
        )
        output = (completed.stdout or completed.stderr or "").strip().splitlines()
    except (OSError, subprocess.SubprocessError) as exc:
        output = [f"command failed: {exc}"]
    lines: list[tuple[str, str]] = [
        ("prompt", rf"PS> cd {ROOT}"),
        ("prompt", r"PS> python -B -c \"from pathlib import Path; ...\""),
        *[("out", line) for line in output[:8]],
    ]
    terminal_raw(
        "powershell_pathlib_demo.png",
        "Windows PowerShell - 用 pathlib 看清路径",
        lines,
        width=1500,
        height=720,
        font_size=24,
        max_chars=88,
        cjk=True,
    )


def powershell_pathlib_demo():
    powershell_pathlib_demo_raw()
    photo_plate("ch01_powershell_pathlib_demo.png", "powershell_pathlib_demo.png")


def powershell_create_venv():
    powershell_create_venv_raw()
    photo_plate("ch01_powershell_create_venv.png", "powershell_create_venv.png")


def powershell_policy_fallback():
    powershell_policy_fallback_raw()
    photo_plate("ch01_powershell_policy_fallback.png", "powershell_policy_fallback.png")


def xkcd_card():
    photo_plate("ch01_xkcd_antigravity_card.png", "xkcd_353_python.png")


def xkcd_environment_card():
    photo_plate("ch01_xkcd_environment_card.png", "xkcd_1987_python_environment.png")


def first_script_feedback_loop():
    im, d = canvas(1800, 1040)
    title_block(d, "第一段脚本的反馈闭环", "脚本不是写完就结束，它要留下看得见的记录")
    steps = [
        ("1", "写脚本", "把代码保存成 01_hello_python.py。", BLUE),
        ("2", "运行它", "在 PowerShell 或 PyCharm 里启动。", GREEN),
        ("3", "看输出", "先确认屏幕上真的有反馈。", ORANGE),
        ("4", "查路径", "确认脚本由哪个 Python 执行。", PURPLE),
        ("5", "留日志", "把环境记录写进 reports。", CYAN),
        ("6", "再改一点", "只改一处，再运行一次。", RED),
    ]
    coords = [(170, 330), (670, 330), (1170, 330), (1170, 650), (670, 650), (170, 650)]
    w, h = 360, 210
    for idx, (x, y) in enumerate(coords):
        nx, ny = coords[(idx + 1) % len(coords)]
        if idx < 2:
            arrow(d, (x + w + 18, y + h // 2), (nx - 18, ny + h // 2), width=5)
        elif idx == 2:
            arrow(d, (x + w // 2, y + h + 18), (nx + w // 2, ny - 18), width=5)
        elif idx < 5:
            arrow(d, (x - 18, y + h // 2), (nx + w + 18, ny + h // 2), width=5)
        else:
            arrow(d, (x + w // 2, y - 18), (nx + w // 2, ny + h + 18), width=5)
    for (x, y), item in zip(coords, steps):
        tag, heading, body, color = item
        labeled_card(d, (x, y, x + w, y + h), tag, heading, body, color)
    rounded(d, (360, 895, 1440, 975), fill="#EEF6FF", outline="#B8D6FF", radius=24, width=2)
    draw_text(d, (400, 912, 1400, 960), "第一章的目标不是写很多代码，而是每次运行都知道结果从哪里来。", size=29, min_size=22, fill=BLUE, bold=True, align="center", valign="center")
    save(im, "ch01_first_script_feedback_loop.png")


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    cover()
    story_timeline()
    knowledge_route()
    core_workshop()
    xkcd_card()
    psychology_applications()
    ide_workbench()
    pip_pipeline()
    xkcd_environment_card()
    powershell_project_navigation()
    powershell_local_environment_check()
    powershell_environment_check()
    powershell_python_locator()
    powershell_create_venv()
    powershell_policy_fallback()
    powershell_run_scripts()
    powershell_full_runtime_check()
    powershell_submission_evidence()
    powershell_pathlib_demo()
    first_script_feedback_loop()
    pycharm_main_window()
    pycharm_new_project()
    pycharm_interpreter_widget()
    pycharm_select_interpreter()
    pycharm_virtualenv_setup()
    pycharm_existing_virtualenv()
    pycharm_edit_configurations()
    pycharm_run_configuration_script()
    pycharm_modify_run_options()
    pycharm_run_widget()
    pycharm_run_console()
    pycharm_environment_focus()
    runtime_environment_side_by_side()
    error_map()
    print("Generated ch01 story-photo visuals.")


if __name__ == "__main__":
    main()
