from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
if not (ROOT / "assets" / "ch00").exists():
    ROOT = Path(__file__).resolve().parents[1]

ASSET_DIR = ROOT / "assets" / "ch00"
WEB_DIR = ASSET_DIR / "web"

W, H = 1800, 1120
BG = "#F7F8FB"
INK = "#162033"
MUTED = "#667085"
LINE = "#D8E0EC"
BLUE = "#2F6BFF"
GREEN = "#24A06B"
ORANGE = "#F28C28"
PURPLE = "#7A5AF8"
RED = "#E84C61"
CYAN = "#18A9B5"


def canvas(width: int = W, height: int = H):
    im = Image.new("RGB", (width, height), BG)
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, name: str):
    im.save(ASSET_DIR / name, optimize=True, quality=95)


def rounded(d: ImageDraw.ImageDraw, xy, fill="#FFFFFF", outline=LINE, radius=26, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def shadow(d: ImageDraw.ImageDraw, xy, radius=26):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill="#DCE2EC")


def arrow(d: ImageDraw.ImageDraw, start, end, color="#98A5B8", width=5):
    x1, y1 = start
    x2, y2 = end
    d.line((x1, y1, x2, y2), fill=color, width=width)
    sign = 1 if x2 >= x1 else -1
    d.polygon([(x2, y2), (x2 - sign * 20, y2 - 11), (x2 - sign * 20, y2 + 11)], fill=color)


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


def draw_map_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=BLUE):
    d.line((x - 35, y + 30, x - 10, y - 35, x + 18, y + 25, x + 40, y - 28), fill=color, width=8)
    d.ellipse((x - 48, y - 48, x + 48, y + 48), outline=color, width=5)


def draw_tool_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=GREEN):
    d.line((x - 35, y + 32, x + 32, y - 35), fill=color, width=12)
    d.ellipse((x + 12, y - 48, x + 52, y - 8), outline=color, width=8)
    d.ellipse((x - 52, y + 10, x - 12, y + 50), outline=color, width=8)


def draw_base_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=ORANGE):
    d.polygon([(x - 52, y + 12), (x, y - 45), (x + 52, y + 12)], outline=color, fill=None)
    d.line((x - 38, y + 12, x - 38, y + 50, x + 38, y + 50, x + 38, y + 12), fill=color, width=8)
    d.line((x - 52, y + 12, x, y - 45, x + 52, y + 12), fill=color, width=8)


def draw_loop_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=PURPLE):
    d.arc((x - 50, y - 50, x + 50, y + 50), 35, 310, fill=color, width=8)
    d.polygon([(x + 48, y - 8), (x + 68, y - 4), (x + 54, y + 12)], fill=color)


def draw_star_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=RED):
    pts = [(x, y - 55), (x + 14, y - 15), (x + 56, y - 15), (x + 22, y + 8), (x + 35, y + 50), (x, y + 24), (x - 35, y + 50), (x - 22, y + 8), (x - 56, y - 15), (x - 14, y - 15)]
    d.polygon(pts, outline=color, fill=None)
    d.line(pts + [pts[0]], fill=color, width=6)


def draw_terminal_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=GREEN):
    d.rounded_rectangle((x - 55, y - 40, x + 55, y + 40), radius=12, outline=color, width=7)
    d.line((x - 28, y - 10, x - 8, y, x - 28, y + 10), fill=color, width=6)
    d.line((x + 2, y + 18, x + 32, y + 18), fill=color, width=6)


def draw_file_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=PURPLE):
    d.line((x - 38, y - 52, x + 18, y - 52, x + 44, y - 24, x + 44, y + 52, x - 38, y + 52, x - 38, y - 52), fill=color, width=7)
    d.line((x + 18, y - 52, x + 18, y - 24, x + 44, y - 24), fill=color, width=7)


def draw_script_icon(d: ImageDraw.ImageDraw, x: int, y: int, color=CYAN):
    d.rounded_rectangle((x - 50, y - 54, x + 50, y + 54), radius=14, outline=color, width=7)
    for yy in (y - 24, y, y + 24):
        d.line((x - 26, yy, x + 28, yy), fill=color, width=5)


def draw_safe_symbol(d: ImageDraw.ImageDraw, x: int, y: int, color, shape: str):
    if shape == "dot":
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=color)
    elif shape == "ring":
        d.ellipse((x - 34, y - 34, x + 34, y + 34), outline=color, width=10)
    elif shape == "bar":
        d.rounded_rectangle((x - 46, y - 16, x + 46, y + 16), radius=16, fill=color)
    elif shape == "square":
        d.rounded_rectangle((x - 30, y - 30, x + 30, y + 30), radius=10, fill=color)
    elif shape == "triangle":
        d.polygon([(x, y - 36), (x + 38, y + 30), (x - 38, y + 30)], fill=color)
    else:
        pts = [(x, y - 42), (x + 12, y - 12), (x + 44, y - 12), (x + 18, y + 8), (x + 28, y + 40), (x, y + 20), (x - 28, y + 40), (x - 18, y + 8), (x - 44, y - 12), (x - 12, y - 12)]
        d.polygon(pts, fill=color)


def cover():
    im, d = canvas()
    points = [
        (340, 600, draw_map_icon, BLUE),
        (635, 460, draw_tool_icon, GREEN),
        (930, 600, draw_base_icon, ORANGE),
        (1225, 460, draw_loop_icon, PURPLE),
        (1520, 600, draw_star_icon, RED),
    ]
    for i in range(len(points) - 1):
        arrow(d, (points[i][0] + 80, points[i][1]), (points[i + 1][0] - 80, points[i + 1][1]))
    for x, y, icon, color in points:
        d.ellipse((x - 88, y - 88, x + 88, y + 88), fill="white", outline=color, width=6)
        icon(d, x, y, color)
    save(im, "ch00_cover.png")


def automation_card():
    photo_plate(
        "ch00_xkcd_automation_card.png",
        "xkcd_1205_is_it_worth_the_time.png",
    )


def history_ada_card():
    photo_plate(
        "ch00_history_ada_lovelace_card.png",
        "ada_lovelace_portrait.jpg",
    )


def history_babbage_card():
    photo_plate(
        "ch00_history_babbage_difference_engine.png",
        "babbage_difference_engine.jpg",
    )


def history_guido_card():
    photo_plate(
        "ch00_history_guido_van_rossum.png",
        "guido_van_rossum.jpg",
    )


def history_jacquard_card():
    photo_plate(
        "ch00_history_jacquard_card.png",
        "jacquard_loom_cards.jpg",
    )


def history_bug_card():
    photo_plate(
        "ch00_history_first_bug_card.png",
        "first_computer_bug_1947.jpg",
    )


def history_apollo_card():
    photo_plate(
        "ch00_history_apollo_software_card.png",
        "margaret_hamilton_apollo_code.jpg",
    )


def history_eniac_card():
    photo_plate(
        "ch00_history_eniac_programmers.png",
        "eniac_programmers.gif",
    )


def factory_card_catalog():
    photo_plate(
        "ch00_factory_card_catalog.png",
        "card_catalog_drawer.jpg",
    )


def factory_lab_notebook():
    photo_plate(
        "ch00_factory_lab_notebook.png",
        "lab_notebook.jpg",
    )


def factory_conveyor():
    photo_plate(
        "ch00_factory_conveyor.png",
        "belt_conveyor_handling.jpg",
    )


def city():
    im, d = canvas()
    center = (900, 560)
    d.ellipse((665, 325, 1135, 795), fill="white", outline=BLUE, width=7)
    draw_base_icon(d, 900, 560, BLUE)
    nodes = [
        (230, 300, draw_map_icon, BLUE),
        (1560, 300, draw_tool_icon, GREEN),
        (230, 830, draw_base_icon, ORANGE),
        (1560, 830, draw_loop_icon, PURPLE),
        (900, 930, draw_star_icon, RED),
    ]
    for x, y, icon, color in nodes:
        d.line((center[0], center[1], x, y), fill="#B8C2D4", width=4)
        d.ellipse((x - 86, y - 86, x + 86, y + 86), fill="white", outline=color, width=6)
        icon(d, x, y, color)
    save(im, "python_city_metaphor.png")


def roadmap():
    im, d = canvas()
    y = 560
    xs = [180 + i * 144 for i in range(11)]
    for i in range(10):
        arrow(d, (xs[i] + 55, y), (xs[i + 1] - 55, y), width=4)
    colors = [BLUE, GREEN, ORANGE, PURPLE, CYAN, GREEN, BLUE, RED, ORANGE, PURPLE, RED]
    for i, x in enumerate(xs):
        d.ellipse((x - 58, y - 58, x + 58, y + 58), fill="white", outline=colors[i], width=6)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=colors[i])
    save(im, "course_roadmap.png")


def project_ladder():
    im, d = canvas()
    colors = [BLUE, GREEN, ORANGE, PURPLE]
    base_x, base_y = 350, 820
    step_w, step_h = 280, 120
    for idx, color in enumerate(colors):
        x1 = base_x + idx * step_w
        y1 = base_y - idx * step_h
        x2 = x1 + step_w
        y2 = base_y + 80 - idx * step_h
        d.rectangle((x1, y1, x2, y2), fill="#FFFFFF", outline=color, width=6)
        d.ellipse((x1 + step_w / 2 - 20, y1 + 40, x1 + step_w / 2 + 20, y1 + 80), fill=color)
    save(im, "project_ladder.png")


def env_pipeline():
    im, d = canvas()
    xs = [250, 575, 900, 1225, 1550]
    colors = [BLUE, GREEN, ORANGE, PURPLE, CYAN]
    icons = [draw_tool_icon, draw_terminal_icon, draw_map_icon, draw_file_icon, draw_script_icon]
    for i in range(4):
        arrow(d, (xs[i] + 100, 560), (xs[i + 1] - 100, 560), width=5)
    for x, color, icon in zip(xs, colors, icons):
        d.ellipse((x - 90, 470, x + 90, 650), fill="white", outline=color, width=6)
        icon(d, x, 560, color)
    save(im, "env_pipeline.png")


def error_map():
    im, d = canvas()
    colors = [BLUE, ORANGE, PURPLE, GREEN, RED, CYAN]
    shapes = ["dot", "ring", "bar", "square", "triangle", "star"]
    positions = [(380, 370), (900, 370), (1420, 370), (380, 760), (900, 760), (1420, 760)]
    for color, shape, (x, y) in zip(colors, shapes, positions):
        shadow(d, (x - 170, y - 80, x + 170, y + 80), radius=24)
        rounded(d, (x - 170, y - 80, x + 170, y + 80), fill="white", radius=24)
        draw_safe_symbol(d, x, y, color, shape)
    save(im, "error_map.png")


def learning_loop():
    im, d = canvas()
    center = (900, 590)
    r = 310
    colors = [BLUE, GREEN, ORANGE, RED, PURPLE]
    shapes = ["dot", "ring", "bar", "star", "square"]
    coords = [
        (900, 250),
        (1230, 480),
        (1110, 845),
        (690, 845),
        (570, 480),
    ]
    for i in range(len(coords)):
        arrow(d, coords[i], coords[(i + 1) % len(coords)], width=4)
    for color, shape, (x, y) in zip(colors, shapes, coords):
        d.ellipse((x - 70, y - 70, x + 70, y + 70), fill="white", outline=color, width=6)
        draw_safe_symbol(d, x, y, color, shape)
    d.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), outline="#E2E8F0", width=3)
    save(im, "learning_loop.png")


def learning_momentum_chart():
    im, d = canvas()
    chart = (220, 260, 1500, 880)
    x1, y1, x2, y2 = chart
    rounded(d, chart, fill="white", radius=24)
    for k in range(5):
        y = y1 + 90 + k * 105
        d.line((x1 + 80, y, x2 - 80, y), fill="#E7EDF5", width=2)
    d.line((x1 + 90, y2 - 95, x2 - 70, y2 - 95), fill="#9AA7BD", width=3)
    d.line((x1 + 90, y1 + 70, x1 + 90, y2 - 95), fill="#9AA7BD", width=3)
    points = [(0, 18), (1, 25), (2, 21), (3, 36), (4, 43), (5, 40), (6, 58), (7, 66), (8, 72), (9, 84)]
    curve = []
    for i, v in points:
        curve.append((x1 + 130 + i * 120, y2 - 110 - v * 4.7))
    area = [(curve[0][0], y2 - 95)] + curve + [(curve[-1][0], y2 - 95)]
    d.polygon(area, fill="#DCEBFF")
    d.line(curve, fill=BLUE, width=8)
    for x, y in curve:
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill="white", outline=BLUE, width=4)
    save(im, "learning_momentum_chart.png")


def tech_stack_workbench():
    im, d = canvas()
    bench = (250, 700, 1550, 825)
    d.rounded_rectangle(bench, radius=28, fill="#E8EEF7", outline=LINE, width=3)
    positions = [
        (360, 560, draw_terminal_icon, GREEN),
        (560, 500, draw_file_icon, PURPLE),
        (760, 560, draw_script_icon, CYAN),
        (980, 500, draw_map_icon, BLUE),
        (1180, 560, draw_tool_icon, ORANGE),
        (1400, 500, draw_base_icon, RED),
    ]
    for i, (x, y, icon, color) in enumerate(positions):
        shadow(d, (x - 86, y - 86, x + 86, y + 86), radius=22)
        d.ellipse((x - 84, y - 84, x + 84, y + 84), fill="white", outline=color, width=6)
        icon(d, x, y, color)
        if i < len(positions) - 1:
            nx, ny = positions[i + 1][0], positions[i + 1][1]
            arrow(d, (x + 90, y), (nx - 90, ny), color="#B8C2D4", width=4)
    save(im, "tech_stack_workbench.png")


def chapter_blueprint_bridge():
    im, d = canvas()
    left_x, right_x = 250, 1550
    y_top, y_bottom = 330, 790
    colors = [BLUE, GREEN, ORANGE, PURPLE, CYAN, RED]
    anchors = []
    for idx, color in enumerate(colors):
        y = y_top + idx * ((y_bottom - y_top) // (len(colors) - 1))
        anchors.append((left_x, y, color))
        anchors.append((right_x, y, color))
    for idx, (x, y, color) in enumerate(anchors):
        d.ellipse((x - 42, y - 42, x + 42, y + 42), fill="white", outline=color, width=6)
        draw_safe_symbol(d, x, y, color, ["dot", "ring", "bar", "square", "triangle", "star"][idx % 6])
    for idx in range(0, len(anchors), 2):
        lx, ly, color = anchors[idx]
        rx, ry, _ = anchors[idx + 1]
        d.line((lx + 50, ly, rx - 50, ry), fill="#C5D0E0", width=4)
    for step, x in enumerate([520, 760, 1000, 1240]):
        y = 560 + (30 if step % 2 else -30)
        shadow(d, (x - 92, y - 62, x + 92, y + 62), radius=20)
        rounded(d, (x - 92, y - 62, x + 92, y + 62), fill="white", radius=20)
        draw_script_icon(d, x, y, colors[step % len(colors)])
        if step < 3:
            arrow(d, (x + 105, y), ([760, 1000, 1240][step] - 105, 560 + (-30 if step % 2 else 30)), width=4)
    save(im, "chapter_blueprint_bridge.png")


def chapter_relay_station():
    im, d = canvas()
    d.rounded_rectangle((120, 145, 1680, 975), radius=42, fill="#FFFFFF", outline=LINE, width=3)
    d.rounded_rectangle((210, 245, 1590, 875), radius=34, fill="#F1F5FA", outline="#E2E8F0", width=3)

    # Two arcs of chapter stations, linked through a central handoff table.
    left_nodes = [
        (360, 395, draw_terminal_icon, GREEN),
        (560, 315, draw_file_icon, PURPLE),
        (760, 395, draw_script_icon, CYAN),
        (560, 610, draw_map_icon, BLUE),
    ]
    right_nodes = [
        (1040, 395, draw_tool_icon, ORANGE),
        (1240, 315, draw_base_icon, RED),
        (1440, 395, draw_loop_icon, PURPLE),
        (1240, 610, draw_star_icon, BLUE),
    ]
    colors = [GREEN, PURPLE, CYAN, BLUE, ORANGE, RED, PURPLE, BLUE]
    nodes = left_nodes + right_nodes
    for i, (x, y, icon, color) in enumerate(nodes):
        shadow(d, (x - 74, y - 74, x + 74, y + 74), radius=22)
        d.ellipse((x - 72, y - 72, x + 72, y + 72), fill="white", outline=color, width=6)
        icon(d, x, y, color)
        if i < len(nodes) - 1 and i != 3:
            nx, ny = nodes[i + 1][0], nodes[i + 1][1]
            arrow(d, (x + 78, y), (nx - 78, ny), color="#AEBBCD", width=4)

    # Handoff table: no words, just incoming materials turning into outputs.
    table = (710, 690, 1090, 810)
    d.rounded_rectangle((table[0] + 8, table[1] + 10, table[2] + 8, table[3] + 10), radius=28, fill="#DCE2EC")
    rounded(d, table, fill="#FFFFFF", outline=LINE, radius=28, width=3)
    for i, color in enumerate([BLUE, GREEN, ORANGE, PURPLE]):
        x = 760 + i * 80
        d.rounded_rectangle((x, 720, x + 48, 774), radius=12, outline=color, width=5)
        if i < 3:
            arrow(d, (x + 55, 747), (x + 72, 747), color="#B8C2D4", width=4)

    arrow(d, (655, 610), (760, 690), color="#AEBBCD", width=5)
    arrow(d, (1045, 690), (1165, 610), color="#AEBBCD", width=5)
    arrow(d, (760, 395), (860, 690), color="#AEBBCD", width=4)
    arrow(d, (1040, 395), (955, 690), color="#AEBBCD", width=4)

    save(im, "chapter_relay_station.png")


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
    print("Generated ch00 lightweight visuals.")


if __name__ == "__main__":
    main()
