from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
md_files = list((ROOT / "chapters").glob("*.md"))
markdown_image_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
html_image_pattern = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)

missing = []
for md in md_files:
    text = md.read_text(encoding="utf-8")
    links = []
    links.extend(markdown_image_pattern.findall(text))
    links.extend(html_image_pattern.findall(text))
    for match in links:
        if match.startswith("http://") or match.startswith("https://"):
            continue
        target = (md.parent / match).resolve()
        if not target.exists():
            missing.append((md.relative_to(ROOT), match))

if missing:
    print("Missing image links:")
    for md, link in missing:
        print(f" - {md}: {link}")
    sys.exit(1)

print(f"OK: checked {len(md_files)} markdown file(s), no missing local image links.")
