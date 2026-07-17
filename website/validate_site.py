from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attribute = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else ""
        if not attribute:
            return
        values = dict(attrs)
        value = values.get(attribute)
        if value:
            self.links.append(value)


def local_target(page: Path, link: str) -> Path | None:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    target = (PUBLIC / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    target = target.resolve()
    if target.is_dir() or path.endswith("/"):
        target /= "index.html"
    return target


def main() -> int:
    errors: list[str] = []
    manifest = json.loads((PUBLIC / "site_manifest.json").read_text(encoding="utf-8"))
    function_data = json.loads((PUBLIC / "functions/functions.json").read_text(encoding="utf-8"))
    function_page = (PUBLIC / "functions/index.html").read_text(encoding="utf-8")

    if manifest["chapter_count"] != 11 or manifest["open_chapter_count"] != 11:
        errors.append("site manifest must expose all 11 chapters")
    if manifest["public_chapter_max"] != 10:
        errors.append("public_chapter_max must be 10")
    if manifest["function_reference"]["entry_count"] != len(function_data):
        errors.append("function JSON count does not match the manifest")
    if function_page.count("data-function-entry") != len(function_data):
        errors.append("function page entry count does not match function JSON")

    chapter_pages = sorted((PUBLIC / "chapters").glob("ch*.html"))
    if len(chapter_pages) != 11:
        errors.append(f"expected 11 chapter pages, found {len(chapter_pages)}")
    for page in chapter_pages:
        content = page.read_text(encoding="utf-8")
        if "chapter-function-guide" not in content:
            errors.append(f"missing function guide: {page.relative_to(PUBLIC)}")
        if "locked-hero" in content:
            errors.append(f"chapter is unexpectedly locked: {page.relative_to(PUBLIC)}")

    for index in range(11):
        archive = PUBLIC / "downloads" / f"python_tutorial_ch{index:02d}.zip"
        if not archive.is_file() or archive.stat().st_size == 0:
            errors.append(f"missing chapter archive: {archive.name}")

    checked_links = 0
    for page in PUBLIC.rglob("*.html"):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for link in parser.links:
            target = local_target(page, link)
            if target is None:
                continue
            checked_links += 1
            if not target.exists():
                errors.append(
                    f"broken link in {page.relative_to(PUBLIC)}: {link} -> {target.relative_to(PUBLIC)}"
                )

    print(f"Validated {len(chapter_pages)} chapter pages, {len(function_data)} function entries, and {checked_links} local links.")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Site validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
