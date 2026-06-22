from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


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
    path = ASSET_DIR / name
    if path.suffix.lower() == ".png":
        im.save(path, format="PNG")
    else:
        im.save(path, quality=95)


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
    path = WEB_DIR / output_name
    if path.suffix.lower() == ".png":
        im.save(path, format="PNG")
    else:
        im.save(path, quality=95)


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
        "Windows PowerShell - locate Python and PyCharm",
        lines[:20],
        width=1500,
        height=960,
        font_size=22,
        max_chars=88,
    )


def powershell_create_venv_raw():
    terminal_raw(
        "powershell_create_venv.png",
        "Windows PowerShell - create .venv",
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
        "Windows PowerShell - .venv fallback check",
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
        "Windows PowerShell - ch01 full runtime check",
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
    xs = [260, 620, 980, 1340]
    colors = [BLUE, GREEN, ORANGE, PURPLE]
    icons = [folder_icon, package_icon, gear_icon, terminal_icon]
    for a, b in zip(xs, xs[1:]):
        arrow(d, (a + 110, 560), (b - 110, 560), width=5)
    for x, color, icon in zip(xs, colors, icons):
        shadow(d, (x - 120, 430, x + 120, 690), radius=28)
        rounded(d, (x - 120, 430, x + 120, 690), fill="#FFFFFF", radius=28)
        icon(d, x, 560, color)
    save(im, "ch01_pip_pipeline.png")


def error_map():
    im, d = canvas()
    colors = [RED, ORANGE, PURPLE, BLUE, GREEN, YELLOW]
    icons = [warning_icon, file_icon, package_icon, terminal_icon, folder_icon, gear_icon]
    positions = [(350, 360), (900, 360), (1450, 360), (350, 760), (900, 760), (1450, 760)]
    for (x, y), icon, color in zip(positions, icons, colors):
        shadow(d, (x - 150, y - 95, x + 150, y + 95), radius=24)
        rounded(d, (x - 150, y - 95, x + 150, y + 95), fill="#FFFFFF", radius=24)
        icon(d, x, y, color)
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
        "Windows PowerShell - ch01 submission evidence",
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
        "Windows PowerShell - pathlib path check",
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
    nodes = [
        (300, 380, file_icon, BLUE),
        (650, 380, terminal_icon, GREEN),
        (1000, 380, card_icon, ORANGE),
        (1350, 380, file_icon, PURPLE),
        (1350, 690, folder_icon, CYAN),
        (1000, 690, card_icon, YELLOW),
        (650, 690, terminal_icon, RED),
        (300, 690, folder_icon, INK),
    ]
    for i in range(len(nodes)):
        x1, y1 = nodes[i][0], nodes[i][1]
        x2, y2 = nodes[(i + 1) % len(nodes)][0], nodes[(i + 1) % len(nodes)][1]
        if i == len(nodes) - 1:
            arrow(d, (x1, y1 - 95), (x2, y2 - 95), "#B8C4D6", width=5)
        else:
            arrow(d, (x1 + 125 if x2 > x1 else x1 - 125, y1), (x2 - 125 if x2 > x1 else x2 + 125, y2), "#B8C4D6", width=5)
    for x, y, icon, color in nodes:
        shadow(d, (x - 120, y - 105, x + 120, y + 105), radius=28)
        rounded(d, (x - 120, y - 105, x + 120, y + 105), fill="#FFFFFF", radius=28)
        icon(d, x, y, color)
    d.rounded_rectangle((350, 885, 1450, 965), radius=38, fill="#EEF6FF", outline="#9CC8FF", width=4)
    for x in range(460, 1360, 150):
        d.ellipse((x - 17, 925 - 17, x + 17, 925 + 17), fill="#FFFFFF", outline=GREEN, width=4)
        d.line((x - 9, 925, x - 1, 934, x + 14, 909), fill=GREEN, width=5)
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
