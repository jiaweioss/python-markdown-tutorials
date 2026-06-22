"""Resize and grayscale an image."""
from pathlib import Path
from PIL import Image

src = Path("output/demo_card_image.png")
im = Image.open(src)
small = im.resize((240, 150))
gray = small.convert("L")
gray.save("output/demo_card_image_gray.png")
print("已生成 output/demo_card_image_gray.png")
