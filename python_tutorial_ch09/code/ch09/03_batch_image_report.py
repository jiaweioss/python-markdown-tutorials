"""List image sizes in a folder."""
from pathlib import Path
from PIL import Image

for path in Path("output").glob("*.png"):
    with Image.open(path) as im:
        print(path.name, im.size, im.mode)
