from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import markdown
from pygments.formatters import HtmlFormatter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public"
SITE_SRC = ROOT / "website"
ASSET_OUT = OUT / "assets"
CHAPTER_OUT = OUT / "chapters"
FILES_OUT = OUT / "files"


@dataclass
class Chapter:
    index: int
    key: str
    folder: Path
    markdown: Path
    title: str
    page_name: str
    cover: str
    summary: str
    image_count: int
    code_count: int
    report_count: int
    headings: list[dict[str, str | int]]
    html_body: str = ""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def clean_title(text: str) -> str:
    text = re.sub(r"^#+\s*", "", text).strip()
    text = re.sub(r"\s+\{#[^}]+\}\s*$", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_]", "", text)
    return html.unescape(text).strip()


def plain_text(md: str) -> str:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"<style.*?</style>", " ", md, flags=re.S | re.I)
    md = re.sub(r"<figure.*?</figure>", " ", md, flags=re.S | re.I)
    md = re.sub(r"<[^>]+>", " ", md)
    md = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", md)
    md = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", md)
    md = re.sub(r"[#>*_`|:-]", " ", md)
    md = re.sub(r"\s+", " ", md)
    return md.strip()


def extract_summary(md: str) -> str:
    body = "\n".join(line for line in md.splitlines() if not line.startswith("#"))
    text = plain_text(body)
    return text[:110] + ("..." if len(text) > 110 else "")


def chapter_number(folder: Path) -> int | None:
    match = re.fullmatch(r"python_tutorial_ch(\d{2})", folder.name)
    return int(match.group(1)) if match else None


def discover_chapters() -> list[Chapter]:
    chapters: list[Chapter] = []
    for folder in sorted(ROOT.glob("python_tutorial_ch*")):
        if not folder.is_dir():
            continue
        number = chapter_number(folder)
        if number is None:
            continue
        markdown_files = sorted((folder / "chapters").glob("*.md"))
        if not markdown_files:
            continue
        md_path = markdown_files[0]
        md = read_text(md_path)
        title_line = next((line for line in md.splitlines() if line.startswith("# ")), folder.name)
        title = clean_title(title_line)
        image_count = len(re.findall(r"<img\s|!\[[^\]]*\]\(", md))
        cover = find_cover(md, number)
        code_count = len(list((folder / "code").rglob("*.py"))) if (folder / "code").exists() else 0
        report_count = len(list((folder / "reports").glob("*.md"))) if (folder / "reports").exists() else 0
        chapters.append(
            Chapter(
                index=number,
                key=f"ch{number:02d}",
                folder=folder,
                markdown=md_path,
                title=title,
                page_name=f"{md_path.stem}.html",
                cover=cover,
                summary=extract_summary(md),
                image_count=image_count,
                code_count=code_count,
                report_count=report_count,
                headings=[],
            )
        )
    return sorted(chapters, key=lambda item: item.index)


def find_cover(md: str, number: int) -> str:
    raw = re.search(r'<img\s+[^>]*src="([^"]+)"', md)
    if raw:
        return raw.group(1).replace("../", "")
    inline = re.search(r"!\[[^\]]*\]\(([^)]+)\)", md)
    if inline:
        return inline.group(1).replace("../", "")
    return f"assets/ch{number:02d}/ch{number:02d}_cover.png"


def heading_id(prefix: str, count: int) -> str:
    return f"{prefix}-section-{count:02d}"


def add_heading_ids(md: str, prefix: str) -> tuple[str, list[dict[str, str | int]]]:
    in_fence = False
    count = 0
    headings: list[dict[str, str | int]] = []
    output: list[str] = []
    for line in md.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            output.append(line)
            continue
        match = re.match(r"^(#{1,4})\s+(.+?)\s*$", line)
        if match and not in_fence:
            level = len(match.group(1))
            title = clean_title(match.group(2))
            count += 1
            hid = heading_id(prefix, count)
            headings.append({"level": level, "title": title, "id": hid})
            output.append(f"{match.group(1)} {match.group(2)} {{#{hid}}}")
        else:
            output.append(line)
    return "\n".join(output), headings


def render_markdown(md: str, prefix: str) -> tuple[str, list[dict[str, str | int]]]:
    processed, headings = add_heading_ids(md, prefix)
    renderer = markdown.Markdown(
        extensions=[
            "extra",
            "attr_list",
            "toc",
            "md_in_html",
            "sane_lists",
            "codehilite",
        ],
        extension_configs={
            "toc": {"permalink": False},
            "codehilite": {"guess_lang": False, "linenums": False},
        },
        output_format="html5",
    )
    body = renderer.convert(processed)
    body = body.replace("zoom:50%;", "").replace("zoom: 50%;", "")
    return body, headings


def copytree_clean(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "output_*contact_sheet*.png")
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)


def copy_public_assets(chapters: Iterable[Chapter]) -> None:
    ASSET_OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SITE_SRC / "site.css", ASSET_OUT / "site.css")
    shutil.copy2(SITE_SRC / "site.js", ASSET_OUT / "site.js")
    write_text(ASSET_OUT / "pygments.css", HtmlFormatter().get_style_defs(".codehilite"))
    for chapter in chapters:
        copytree_clean(chapter.folder / "assets" / chapter.key, ASSET_OUT / chapter.key)
        chapter_files = FILES_OUT / chapter.folder.name
        for name in ["chapters", "code", "reports", "output", "source_notes", "scripts"]:
            copytree_clean(chapter.folder / name, chapter_files / name)
        for name in ["README.md", "manifest.json"]:
            src = chapter.folder / name
            if src.exists():
                chapter_files.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, chapter_files / name)
    archive = ROOT / "python_tutorial_ch02_optimized.zip"
    if archive.exists():
        (FILES_OUT / "archives").mkdir(parents=True, exist_ok=True)
        shutil.copy2(archive, FILES_OUT / "archives" / archive.name)


def chapter_nav(chapters: list[Chapter], active: int | None, depth: str = "") -> str:
    items = []
    for chapter in chapters:
        href = f"{depth}chapters/{chapter.page_name}" if depth else f"chapters/{chapter.page_name}"
        if depth == "../":
            href = chapter.page_name
        cls = "active" if active == chapter.index else ""
        items.append(
            f'<a class="{cls}" href="{html.escape(href)}">'
            f'<span class="chapter-number">{chapter.key.upper()}</span>'
            f'<span class="chapter-name">{html.escape(short_title(chapter.title))}</span>'
            "</a>"
        )
    return '<nav class="chapter-nav">' + "\n".join(items) + "</nav>"


def short_title(title: str) -> str:
    title = re.sub(r"^第\s*\d+\s*章[：:\s　-]*", "", title).strip()
    title = title.replace("Python ", "").replace("Python", "")
    return title or "课程章节"


def topbar(depth: str = "") -> str:
    return f"""
<header class="topbar">
  <a class="brand" href="{depth}index.html" aria-label="Python教程首页">
    <span class="brand-mark">Py</span>
    <span>Python教程</span>
  </a>
  <div class="top-actions">
    <a class="button" href="{depth}files/">配套文件</a>
    <button class="icon-button" data-theme-toggle title="切换明暗主题" aria-label="切换明暗主题">◐</button>
  </div>
</header>
"""


def layout_page(title: str, body: str, depth: str = "") -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} - Python教程</title>
  <link rel="stylesheet" href="{depth}assets/site.css" />
  <link rel="stylesheet" href="{depth}assets/pygments.css" />
</head>
<body>
{body}
<script src="{depth}assets/site.js"></script>
</body>
</html>
"""


def build_home(chapters: list[Chapter]) -> None:
    total_images = sum(chapter.image_count for chapter in chapters)
    total_code = sum(chapter.code_count for chapter in chapters)
    cards = []
    for chapter in chapters:
        cards.append(
            f"""
<a class="chapter-card" data-search-card href="chapters/{chapter.page_name}">
  <img src="{html.escape(chapter.cover)}" alt="{html.escape(chapter.title)}封面" loading="lazy" />
  <span class="chapter-card-body">
    <span class="meta-row">
      <span class="meta-pill">{chapter.key.upper()}</span>
      <span class="meta-pill">{chapter.image_count} 张图</span>
      <span class="meta-pill">{chapter.code_count} 个脚本</span>
    </span>
    <h2>{html.escape(short_title(chapter.title))}</h2>
    <p>{html.escape(chapter.summary)}</p>
  </span>
</a>
"""
        )
    body = f"""
{topbar()}
<div class="site-shell">
  <aside class="sidebar">
    <div class="sidebar-inner">
      <p class="sidebar-title">课程目录</p>
      {chapter_nav(chapters, None)}
    </div>
  </aside>
  <main class="home-main">
    <section class="course-header">
      <div>
        <h1 class="course-title">Python教程</h1>
        <p class="course-copy">从环境、数据类型、文件、GUI、面向对象，到数据分析、游戏、爬虫、图像处理和办公自动化。每章都包含正文、配图、代码和可复查输出。</p>
      </div>
      <div class="stat-board" aria-label="课程统计">
        <div class="stat"><strong>{len(chapters)}</strong><span>正式章节</span></div>
        <div class="stat"><strong>{total_images}</strong><span>正文图片</span></div>
        <div class="stat"><strong>{total_code}</strong><span>代码脚本</span></div>
        <div class="stat"><strong>静态站点</strong><span>HTML / CSS / JS</span></div>
      </div>
    </section>
    <div class="tool-row">
      <input class="search" data-search type="search" placeholder="搜索章节关键词，例如 文件、GUI、爬虫" />
      <a class="button primary" href="chapters/{chapters[0].page_name}">开始阅读</a>
    </div>
    <section class="chapter-grid" aria-label="章节列表">
      {''.join(cards)}
    </section>
    <p class="footer">本页由本地教程 Markdown 自动生成。</p>
  </main>
</div>
"""
    write_text(OUT / "index.html", layout_page("首页", body))


def build_files_index(chapters: list[Chapter]) -> None:
    rows = []
    for chapter in chapters:
        base = f"{chapter.folder.name}"
        rows.append(
            f"""
<a class="chapter-card" data-search-card href="{html.escape(base)}/chapters/{html.escape(chapter.markdown.name)}">
  <span class="chapter-card-body">
    <span class="meta-row">
      <span class="meta-pill">{chapter.key.upper()}</span>
      <span class="meta-pill">{chapter.code_count} 个脚本</span>
      <span class="meta-pill">{chapter.report_count} 份报告</span>
    </span>
    <h2>{html.escape(short_title(chapter.title))}</h2>
    <p>{html.escape(chapter.folder.name)}</p>
  </span>
</a>
"""
        )
    archive_link = ""
    if (FILES_OUT / "archives" / "python_tutorial_ch02_optimized.zip").exists():
        archive_link = '<a class="button" href="archives/python_tutorial_ch02_optimized.zip">ch02 optimized zip</a>'
    body = f"""
{topbar("../")}
<main class="home-main">
  <section class="course-header">
    <div>
      <h1 class="course-title">配套文件</h1>
      <p class="course-copy">每章的 Markdown 原文、代码、报告、输出文件和脚本都按章节保留在这里。</p>
    </div>
    <div class="stat-board">
      <div class="stat"><strong>{len(chapters)}</strong><span>章节文件夹</span></div>
      <div class="stat"><strong>{sum(c.code_count for c in chapters)}</strong><span>代码脚本</span></div>
    </div>
  </section>
  <div class="tool-row">
    <input class="search" data-search type="search" placeholder="搜索文件章节" />
    {archive_link}
  </div>
  <section class="chapter-grid" aria-label="配套文件列表">
    {''.join(rows)}
  </section>
</main>
"""
    write_text(FILES_OUT / "index.html", layout_page("配套文件", body, "../"))


def file_links(chapter: Chapter) -> str:
    base = f"../files/{chapter.folder.name}"
    links: list[str] = []
    chapter_raw = f"{base}/chapters/{chapter.markdown.name}"
    links.append(link(chapter_raw, "本章 Markdown"))
    code_dir = chapter.folder / "code"
    if code_dir.exists():
        for path in sorted(code_dir.rglob("*.py"))[:10]:
            rel = path.relative_to(chapter.folder).as_posix()
            links.append(link(f"{base}/{rel}", rel))
    reports = chapter.folder / "reports"
    if reports.exists():
        for path in sorted(reports.glob("*.md"))[:6]:
            rel = path.relative_to(chapter.folder).as_posix()
            links.append(link(f"{base}/{rel}", rel))
    return '<div class="file-links">' + "\n".join(links) + "</div>"


def link(href: str, label: str) -> str:
    return f'<a href="{html.escape(href)}" title="{html.escape(label)}">{html.escape(label)}</a>'


def toc_links(chapter: Chapter) -> str:
    items = []
    for heading in chapter.headings:
        level = int(heading["level"])
        if level == 1 or level > 4:
            continue
        items.append(
            f'<li><a class="level-{level}" href="#{html.escape(str(heading["id"]))}">'
            f'{html.escape(str(heading["title"]))}</a></li>'
        )
    return "<ol>" + "\n".join(items) + "</ol>"


def build_chapter_pages(chapters: list[Chapter]) -> None:
    for i, chapter in enumerate(chapters):
        md = read_text(chapter.markdown)
        chapter.html_body, chapter.headings = render_markdown(md, chapter.key)
        prev_chapter = chapters[i - 1] if i > 0 else None
        next_chapter = chapters[i + 1] if i + 1 < len(chapters) else None
        pager = ['<nav class="pager" aria-label="章节切换">']
        pager.append(
            f'<a href="{prev_chapter.page_name}">上一章<br><strong>{html.escape(short_title(prev_chapter.title))}</strong></a>'
            if prev_chapter
            else '<span></span>'
        )
        pager.append(
            f'<a class="next" href="{next_chapter.page_name}">下一章<br><strong>{html.escape(short_title(next_chapter.title))}</strong></a>'
            if next_chapter
            else '<span></span>'
        )
        pager.append("</nav>")
        body = f"""
{topbar("../")}
<div class="chapter-shell">
  <aside class="sidebar">
    <div class="sidebar-inner">
      <p class="sidebar-title">课程目录</p>
      {chapter_nav(chapters, chapter.index, "../")}
    </div>
  </aside>
  <main class="article-main">
    <header class="article-head">
      <p class="article-kicker">{chapter.key.upper()}</p>
      <h1>{html.escape(chapter.title)}</h1>
      <div class="article-actions">
        <a class="button primary" href="../files/{chapter.folder.name}/chapters/{chapter.markdown.name}">Markdown 原文</a>
        <a class="button" href="#chapter-files">配套文件</a>
        <a class="button" href="../index.html">返回目录</a>
      </div>
    </header>
    <article class="chapter-content">
      {chapter.html_body}
    </article>
    <section class="file-panel" id="chapter-files">
      <h2>配套文件</h2>
      {file_links(chapter)}
    </section>
    {''.join(pager)}
  </main>
  <aside class="toc-panel">
    <div class="toc-inner">
      <p class="toc-title">本页目录</p>
      {toc_links(chapter)}
    </div>
  </aside>
</div>
"""
        write_text(CHAPTER_OUT / chapter.page_name, layout_page(chapter.title, body, "../"))


def build_manifest(chapters: list[Chapter]) -> None:
    payload = {
        "title": "Python教程",
        "chapter_count": len(chapters),
        "chapters": [
            {
                "key": c.key,
                "title": c.title,
                "page": f"chapters/{c.page_name}",
                "markdown": str(c.markdown.relative_to(ROOT)).replace("\\", "/"),
                "images": c.image_count,
                "code_files": c.code_count,
            }
            for c in chapters
        ],
    }
    write_text(OUT / "site_manifest.json", json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    chapters = discover_chapters()
    if not chapters:
        raise SystemExit("No chapter markdown files found.")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    copy_public_assets(chapters)
    build_chapter_pages(chapters)
    build_home(chapters)
    build_files_index(chapters)
    build_manifest(chapters)
    print(f"Built {len(chapters)} chapters into {OUT}")


if __name__ == "__main__":
    main()
