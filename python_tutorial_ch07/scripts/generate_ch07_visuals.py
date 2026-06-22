from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "ch07"
WEB_DIR = ASSET_DIR / "web"

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

VISUALS = ['ch07_cover.png', 'ch07_story_scene.png', 'ch07_roadmap.png', 'ch07_core_metaphor.png', 'ch07_minimal_demo.png', 'ch07_psychology_link.png', 'ch07_pitfall_map.png', 'ch07_project_dashboard.png']


def canvas():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, name: str):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    im.save(ASSET_DIR / name, optimize=True, quality=95)


def photo_plate(output_name: str, image_name: str):
    im = Image.new("RGB", (1800, 1180), BG)
    d = ImageDraw.Draw(im)
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


def rounded(d: ImageDraw.ImageDraw, xy, fill="#FFFFFF", outline=LINE, radius=30, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def shadow(d: ImageDraw.ImageDraw, xy, radius=30):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle((x1 + 10, y1 + 12, x2 + 10, y2 + 12), radius=radius, fill="#DCE2EC")


def arrow(d: ImageDraw.ImageDraw, start, end, color="#98A5B8", width=5):
    x1, y1 = start
    x2, y2 = end
    d.line((x1, y1, x2, y2), fill=color, width=width)
    sign = 1 if x2 >= x1 else -1
    d.polygon([(x2, y2), (x2 - sign * 22, y2 - 12), (x2 - sign * 22, y2 + 12)], fill=color)


def icon_terminal(d, x, y, color=GREEN):
    d.rounded_rectangle((x - 70, y - 48, x + 70, y + 48), radius=16, outline=color, width=8)
    d.line((x - 38, y - 13, x - 14, y, x - 38, y + 13), fill=color, width=7)
    d.line((x + 5, y + 20, x + 42, y + 20), fill=color, width=7)


def icon_file(d, x, y, color=BLUE):
    d.line((x - 48, y - 62, x + 18, y - 62, x + 55, y - 25, x + 55, y + 62, x - 48, y + 62, x - 48, y - 62), fill=color, width=7)
    d.line((x + 18, y - 62, x + 18, y - 25, x + 55, y - 25), fill=color, width=7)
    for yy in (y - 12, y + 16, y + 42):
        d.line((x - 25, yy, x + 32, yy), fill=color, width=5)


def icon_card(d, x, y, color=YELLOW):
    d.rounded_rectangle((x - 72, y - 50, x + 72, y + 50), radius=18, outline=color, width=8)
    for yy in (y - 20, y + 8, y + 34):
        d.line((x - 42, yy, x + 44, yy), fill=color, width=5)


def icon_chart(d, x, y, color=BLUE):
    for i, h in enumerate([48, 82, 62, 112]):
        x0 = x - 70 + i * 44
        d.rounded_rectangle((x0, y + 60 - h, x0 + 28, y + 60), radius=10, fill=color)
    d.line((x - 90, y + 62, x + 95, y + 62), fill="#64748B", width=5)


def icon_window(d, x, y, color=CYAN):
    d.rounded_rectangle((x - 82, y - 58, x + 82, y + 58), radius=16, outline=color, width=8)
    d.line((x - 82, y - 22, x + 82, y - 22), fill=color, width=8)
    d.ellipse((x - 60, y - 45, x - 45, y - 30), fill=color)
    d.ellipse((x - 35, y - 45, x - 20, y - 30), fill=color)


def icon_image(d, x, y, color=PURPLE):
    d.rounded_rectangle((x - 76, y - 56, x + 76, y + 56), radius=15, outline=color, width=8)
    d.ellipse((x - 45, y - 30, x - 18, y - 3), outline=color, width=6)
    d.line((x - 60, y + 35, x - 18, y - 8, x + 12, y + 22, x + 44, y - 18, x + 65, y + 35), fill=color, width=7)


def icon_package(d, x, y, color=PURPLE):
    d.polygon([(x, y - 66), (x + 62, y - 30), (x + 62, y + 42), (x, y + 78), (x - 62, y + 42), (x - 62, y - 30)], outline=color)
    d.line((x - 62, y - 30, x, y + 6, x + 62, y - 30), fill=color, width=7)
    d.line((x, y + 6, x, y + 78), fill=color, width=7)


def icon_warning(d, x, y, color=RED):
    d.polygon([(x, y - 68), (x + 70, y + 54), (x - 70, y + 54)], outline=color)
    d.line((x, y - 28, x, y + 18), fill=color, width=8)
    d.ellipse((x - 7, y + 30, x + 7, y + 44), fill=color)


def node(d, x, y, icon, color, r=98):
    d.ellipse((x - r, y - r, x + r, y + r), fill="#FFFFFF", outline=color, width=6)
    icon(d, x, y, color)


ICONS = [icon_window, icon_terminal, icon_file, icon_card, icon_chart, icon_image, icon_package, icon_warning]
COLORS = [BLUE, GREEN, ORANGE, PURPLE, CYAN, YELLOW, RED]


def visual(name: str, index: int):
    im, d = canvas()
    pattern = index % 6
    if pattern == 0:
        shadow(d, (150, 120, 1650, 980))
        rounded(d, (150, 120, 1650, 980))
        for x, icon, color in zip([360, 650, 940, 1230, 1520], ICONS, COLORS):
            node(d, x, 560, icon, color, 88)
        for x1, x2 in zip([448, 738, 1028, 1318], [562, 852, 1142, 1432]):
            arrow(d, (x1, 560), (x2, 560), width=4)
    elif pattern == 1:
        shadow(d, (210, 160, 1590, 930))
        rounded(d, (210, 160, 1590, 930))
        for i in range(5):
            x = 360 + i * 270
            y = 360 if i % 2 == 0 else 720
            node(d, x, y, ICONS[(index + i) % len(ICONS)], COLORS[i % len(COLORS)], 82)
            if i:
                arrow(d, (360 + (i - 1) * 270, 360 if (i - 1) % 2 == 0 else 720), (x, y), width=4)
    elif pattern == 2:
        for i, y in enumerate([250, 405, 560, 715, 870]):
            d.rounded_rectangle((330, y, 1470, y + 54), radius=27, fill="#E9EEF6")
            d.rounded_rectangle((330, y, 330 + 180 + i * 170, y + 54), radius=27, fill=COLORS[i % len(COLORS)])
            d.ellipse((240, y - 12, 320, y + 68), fill="#FFFFFF", outline=COLORS[i % len(COLORS)], width=6)
    elif pattern == 3:
        for i, (x, y) in enumerate([(370, 330), (900, 330), (1430, 330), (370, 760), (900, 760), (1430, 760)]):
            shadow(d, (x - 150, y - 100, x + 150, y + 100), radius=24)
            rounded(d, (x - 150, y - 100, x + 150, y + 100), radius=24)
            ICONS[(index + i) % len(ICONS)](d, x, y, COLORS[i % len(COLORS)])
    elif pattern == 4:
        center = (900, 560)
        node(d, center[0], center[1], ICONS[index % len(ICONS)], BLUE, 125)
        for i, (x, y) in enumerate([(300, 260), (1500, 260), (300, 860), (1500, 860), (900, 180), (900, 940)]):
            arrow(d, center, (x, y), width=4)
            node(d, x, y, ICONS[(index + i + 1) % len(ICONS)], COLORS[i % len(COLORS)], 78)
    else:
        shadow(d, (240, 150, 1560, 940))
        rounded(d, (240, 150, 1560, 940))
        rounded(d, (320, 240, 680, 840), fill="#F1F5F9")
        rounded(d, (740, 240, 1480, 840), fill="#111827", outline="#111827")
        for i, color in enumerate(COLORS[:5]):
            d.rounded_rectangle((800, 330 + i * 82, 1390, 355 + i * 82), radius=13, fill=color)
        for i in range(6):
            d.rounded_rectangle((380, 310 + i * 72, 610, 332 + i * 72), radius=11, fill="#CBD5E1")
    save(im, name)


def feedback_playground_loop():
    im, d = canvas()
    shadow(d, (125, 95, 1675, 1005), radius=34)
    rounded(d, (125, 95, 1675, 1005), fill="#FFFFFF", radius=34)

    d.rounded_rectangle((250, 220, 830, 640), radius=32, fill="#101827", outline="#0F172A", width=8)
    d.rounded_rectangle((300, 280, 780, 560), radius=22, fill="#F8FAFC", outline="#CBD5E1", width=5)
    d.ellipse((505, 370, 575, 440), fill=BLUE)
    d.rounded_rectangle((602, 355, 705, 455), radius=22, fill=ORANGE)
    d.rounded_rectangle((430, 505, 650, 535), radius=15, fill=GREEN)
    d.rectangle((510, 640, 570, 730), fill="#64748B")
    d.rounded_rectangle((410, 725, 675, 770), radius=20, fill="#CBD5E1")

    d.rounded_rectangle((1040, 235, 1435, 565), radius=34, fill="#F8FAFC", outline="#CBD5E1", width=6)
    for i, color in enumerate([BLUE, GREEN, ORANGE, PURPLE]):
        x = 1105 + i * 74
        d.rounded_rectangle((x, 345, x + 48, 455), radius=16, fill=color)
    d.rounded_rectangle((1120, 490, 1345, 520), radius=15, fill="#DDE6F2")

    d.rounded_rectangle((975, 700, 1500, 860), radius=34, fill="#F8FAFC", outline="#CBD5E1", width=5)
    for i, color in enumerate([GREEN, BLUE, ORANGE]):
        x = 1035 + i * 155
        d.ellipse((x, 740, x + 64, 804), fill=color)
        d.rounded_rectangle((x + 80, 760, x + 150, 784), radius=12, fill="#DDE6F2")

    d.rounded_rectangle((300, 735, 690, 880), radius=34, fill="#F8FAFC", outline="#CBD5E1", width=5)
    d.ellipse((350, 777, 415, 842), fill=PURPLE)
    d.ellipse((452, 777, 517, 842), fill=CYAN)
    d.ellipse((554, 777, 619, 842), fill=YELLOW)

    arrow(d, (835, 430), (1035, 400), color=BLUE, width=9)
    arrow(d, (1235, 570), (1235, 690), color=GREEN, width=9)
    arrow(d, (970, 780), (700, 805), color=ORANGE, width=9)
    arrow(d, (485, 730), (485, 650), color=PURPLE, width=9)
    d.arc((575, 245, 1155, 825), start=215, end=330, fill="#CBD5E1", width=10)
    d.arc((575, 245, 1155, 825), start=35, end=150, fill="#CBD5E1", width=10)
    save(im, "ch07_feedback_playground_loop.png")


def main():
    for i, name in enumerate(VISUALS):
        visual(name, i)
    photo_plate("ch07_tennis_for_two_story.png", "tennis_for_two_recreation.jpg")
    photo_plate("ch07_pong_arcade_story.png", "atari_pong_arcade_game_cabinet.jpg")
    photo_plate("ch07_magnavox_odyssey_story.png", "magnavox_odyssey_console_set.jpg")
    photo_plate("ch07_spacewar_pdp1_story.png", "spacewar_pdp1.jpg")
    photo_plate("ch07_csikszentmihalyi_flow_story.png", "mihaly_csikszentmihalyi.jpg")
    photo_plate("ch07_stroop_reaction_story.png", "stroop_effect_example.png")
    photo_plate("ch07_skinner_teaching_machine_story.png", "skinner_teaching_machine.jpg")
    feedback_playground_loop()
    photo_plate("ch07_pygame_window_run.png", "pygame_ch07_reaction_window.png")
    photo_plate("ch07_powershell_pygame_run.png", "powershell_ch07_pygame_run.png")
    photo_plate("ch07_reaction_report_preview.png", "ch07_reaction_report_preview.png")
    photo_plate("ch07_game_balance_preview.png", "ch07_game_balance_preview.png")
    photo_plate("ch07_flow_tuning_curve.png", "ch07_flow_tuning_curve.png")
    photo_plate("ch07_game_feedback_loop.png", "ch07_game_feedback_loop.png")
    photo_plate("ch07_data_driven_tuning.png", "ch07_data_driven_tuning.png")
    photo_plate("ch07_teaching_feedback_game.png", "ch07_teaching_feedback_game.png")
    photo_plate("ch07_game_runtime_evidence.png", "ch07_game_runtime_evidence.png")
    print(f"Generated {len(VISUALS) + 17} visuals for {ASSET_DIR.name}.")


if __name__ == "__main__":
    main()
