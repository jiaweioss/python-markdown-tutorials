"""Create a demo image with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw

Path("output").mkdir(exist_ok=True)
im = Image.new("RGB", (480, 300), "#f8fafc")
d = ImageDraw.Draw(im)
for i, color in enumerate(["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]):
    d.rounded_rectangle((40 + i * 100, 80, 110 + i * 100, 220), radius=18, fill=color)
im.save("output/demo_card_image.png")
print("已生成 output/demo_card_image.png")
