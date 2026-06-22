"""Check local image links in markdown files."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
md_files = list(root.rglob("*.md"))
missing = []
markdown_image_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
html_image_pattern = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)

for md in md_files:
    text = md.read_text(encoding="utf-8")
    links = []
    links.extend(match.group(1) for match in markdown_image_pattern.finditer(text))
    links.extend(match.group(1) for match in html_image_pattern.finditer(text))
    for link in links:
        link = link.split("#", 1)[0]
        if link.startswith(("http://", "https://")):
            continue
        target = (md.parent / link).resolve()
        if not target.exists():
            missing.append((md.relative_to(root), link))

if missing:
    print("Missing image links:")
    for md, link in missing:
        print(f"- {md}: {link}")
    sys.exit(1)

print(f"OK: checked {len(md_files)} markdown files; all local image links exist.")
