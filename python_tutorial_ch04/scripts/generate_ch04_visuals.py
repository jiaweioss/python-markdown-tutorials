from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "ch04"
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

VISUALS = ['ch04_cover.png', 'ch04_story_scene.png', 'ch04_roadmap.png', 'ch04_core_metaphor.png', 'ch04_minimal_demo.png', 'ch04_psychology_link.png', 'ch04_pitfall_map.png', 'ch04_project_dashboard.png']


def canvas():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


def save(im: Image.Image, name: str):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    im.save(ASSET_DIR / name, optimize=True, quality=95)


def photo_plate(output_name: str, image_name: str):
    im, d = canvas()
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


def norman_door_affordance():
    im, d = canvas()
    shadow(d, (150, 120, 1650, 980), radius=34)
    rounded(d, (150, 120, 1650, 980), fill="#FFFFFF", radius=34)

    floor = (230, 835, 1570, 900)
    d.rounded_rectangle(floor, radius=28, fill="#E9EEF6", outline="#E9EEF6")
    for x in (500, 1180):
        d.rounded_rectangle((x - 170, 230, x + 170, 835), radius=18, fill="#E6D8C4", outline="#A87C5A", width=8)
        d.rectangle((x - 138, 270, x + 138, 805), fill="#EFE3D1")
        d.line((x - 138, 505, x + 138, 505), fill="#D2B898", width=5)
        d.line((x, 270, x, 805), fill="#D2B898", width=5)

    d.rounded_rectangle((410, 445, 590, 615), radius=20, fill="#D7DEE8", outline="#9CA8B8", width=6)
    d.rounded_rectangle((1090, 505, 1275, 550), radius=20, fill="#7C4A2F", outline="#4B2E22", width=6)
    d.ellipse((1246, 491, 1300, 565), fill="#B87942", outline="#4B2E22", width=5)

    d.arc((700, 310, 1080, 690), start=205, end=335, fill="#94A3B8", width=12)
    d.polygon([(1085, 502), (1025, 468), (1028, 536)], fill="#94A3B8")
    d.arc((700, 310, 1080, 690), start=25, end=155, fill="#94A3B8", width=12)
    d.polygon([(695, 498), (755, 464), (752, 532)], fill="#94A3B8")

    for x, color in [(500, BLUE), (1180, GREEN)]:
        d.ellipse((x - 38, 112, x + 38, 188), fill=color)
        d.rectangle((x - 12, 180, x + 12, 220), fill=color)
    save(im, "ch04_norman_door_affordance.png")


def main():
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(VISUALS):
        visual(name, i)
    photo_plate("ch04_history_xerox_alto.png", "xerox_alto_1973.jpg")
    photo_plate("ch04_engelbart_mouse_story.png", "engelbart_mouse_replica.jpg")
    photo_plate("ch04_macintosh_gui_story.png", "macintosh_128k_transparency.png")
    photo_plate("ch04_hypercard_story.png", "hypercard.jpg")
    photo_plate("ch04_susan_kare_icon_story.png", "susan_kare_2019.jpg")
    photo_plate("ch04_don_norman_story.png", "don_norman_cropped.jpg")
    norman_door_affordance()
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
    print(f"Generated {len(VISUALS) + 18} visuals for {ASSET_DIR.name}.")


if __name__ == "__main__":
    main()
