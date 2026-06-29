from __future__ import annotations

import html
import json
import re
import shutil
import zipfile
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
DOWNLOADS_OUT = OUT / "downloads"

PUBLIC_CHAPTER_MAX = 10
PUBLIC_RELEASE_NOTE = "当前 ch00-ch10 全部章节正文已开放，整章材料包也已同步开放下载。"
ASSET_VERSION = "20260629-main-18973e4"
MATERIAL_FOLDERS = ["chapters", "code", "reports", "output", "source_notes", "scripts"]
MATERIAL_FILES = ["README.md", "manifest.json"]


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


def short_title(title: str) -> str:
    title = re.sub(r"^第\s*\d+\s*章\s*[：:、\-\s]*", "", title).strip()
    title = title.replace("Python ", "").replace("Python", "").strip()
    return title or "课程章节"


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
    return text[:118] + ("..." if len(text) > 118 else "")


def chapter_number(folder: Path) -> int | None:
    match = re.fullmatch(r"python_tutorial_ch(\d{2})", folder.name)
    return int(match.group(1)) if match else None


def find_cover(md: str, number: int) -> str:
    raw = re.search(r'<img\s+[^>]*src="([^"]+)"', md)
    if raw:
        return raw.group(1).replace("../", "")
    inline = re.search(r"!\[[^\]]*\]\(([^)]+)\)", md)
    if inline:
        return inline.group(1).replace("../", "")
    return f"assets/ch{number:02d}/ch{number:02d}_cover.png"


def version_asset_src(src: str) -> str:
    if src.startswith(("http://", "https://", "data:")):
        return src
    if "?v=" in src or "&v=" in src:
        return src
    normalized = src[3:] if src.startswith("../") else src
    if normalized.startswith("assets/"):
        joiner = "&" if "?" in src else "?"
        return f"{src}{joiner}v={ASSET_VERSION}"
    return src


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
        chapters.append(
            Chapter(
                index=number,
                key=f"ch{number:02d}",
                folder=folder,
                markdown=md_path,
                title=title,
                page_name=f"{md_path.stem}.html",
                cover=find_cover(md, number),
                summary=extract_summary(md),
                image_count=len(re.findall(r"<img\s|!\[[^\]]*\]\(", md)),
                code_count=len(list((folder / "code").rglob("*.py"))) if (folder / "code").exists() else 0,
                report_count=len(list((folder / "reports").glob("*.md"))) if (folder / "reports").exists() else 0,
                headings=[],
            )
        )
    return sorted(chapters, key=lambda item: item.index)


def is_public(chapter: Chapter) -> bool:
    return chapter.index <= PUBLIC_CHAPTER_MAX


def open_chapters(chapters: Iterable[Chapter]) -> list[Chapter]:
    return [chapter for chapter in chapters if is_public(chapter)]


def upcoming_chapters(chapters: Iterable[Chapter]) -> list[Chapter]:
    return [chapter for chapter in chapters if not is_public(chapter)]


def release_range_label() -> str:
    return f"CH00-CH{PUBLIC_CHAPTER_MAX:02d}"


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
            visible_title = re.sub(r"\s+\{#[^}]+\}\s*$", "", match.group(2)).strip()
            title = clean_title(visible_title)
            count += 1
            hid = heading_id(prefix, count)
            headings.append({"level": level, "title": title, "id": hid})
            output.append(f"{match.group(1)} {visible_title} {{#{hid}}}")
        else:
            output.append(line)
    return "\n".join(output), headings


def render_markdown(md: str, prefix: str) -> tuple[str, list[dict[str, str | int]]]:
    processed, headings = add_heading_ids(md, prefix)
    renderer = markdown.Markdown(
        extensions=["extra", "attr_list", "toc", "md_in_html", "sane_lists", "codehilite"],
        extension_configs={
            "toc": {"permalink": False},
            "codehilite": {"guess_lang": False, "linenums": False},
        },
        output_format="html5",
    )
    body = renderer.convert(processed)
    body = body.replace("zoom:50%;", "").replace("zoom: 50%;", "")
    body = re.sub(
        r'(<img\b[^>]*\bsrc=)(["\'])([^"\']+)\2',
        lambda match: (
            f"{match.group(1)}{match.group(2)}"
            f"{html.escape(version_asset_src(html.unescape(match.group(3))))}"
            f"{match.group(2)}"
        ),
        body,
        flags=re.I,
    )
    return body, headings


def copytree_clean(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "output_*contact_sheet*.png")
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=ignore)


def should_skip_material(path: Path) -> bool:
    if "__pycache__" in path.parts:
        return True
    if path.suffix == ".pyc":
        return True
    return "contact_sheet" in path.name


def material_items(chapter: Chapter, folder_name: str) -> list[str]:
    folder = chapter.folder / folder_name
    if not folder.exists():
        return []
    return [
        path.relative_to(chapter.folder).as_posix()
        for path in sorted(folder.rglob("*"))
        if path.is_file() and not should_skip_material(path)
    ]


def material_file_count(chapter: Chapter) -> int:
    total = sum(1 for name in MATERIAL_FILES if (chapter.folder / name).exists())
    for folder_name in MATERIAL_FOLDERS:
        total += len(material_items(chapter, folder_name))
    return total


def make_chapter_package(chapter: Chapter) -> Path:
    DOWNLOADS_OUT.mkdir(parents=True, exist_ok=True)
    package = DOWNLOADS_OUT / f"{chapter.folder.name}.zip"
    with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in MATERIAL_FILES:
            src = chapter.folder / name
            if src.exists() and src.is_file():
                archive.write(src, name)
        for folder_name in MATERIAL_FOLDERS:
            folder = chapter.folder / folder_name
            if not folder.exists():
                continue
            for path in sorted(folder.rglob("*")):
                if path.is_file() and not should_skip_material(path):
                    archive.write(path, path.relative_to(chapter.folder).as_posix())
    return package


def copy_site_assets(chapters: Iterable[Chapter]) -> None:
    ASSET_OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SITE_SRC / "site.css", ASSET_OUT / "site.css")
    shutil.copy2(SITE_SRC / "site.js", ASSET_OUT / "site.js")
    write_text(ASSET_OUT / "pygments.css", HtmlFormatter().get_style_defs(".codehilite"))

    for chapter in chapters:
        copytree_clean(chapter.folder / "assets" / chapter.key, ASSET_OUT / chapter.key)
        chapter_files = FILES_OUT / chapter.folder.name
        for folder_name in MATERIAL_FOLDERS:
            copytree_clean(chapter.folder / folder_name, chapter_files / folder_name)
        for name in MATERIAL_FILES:
            src = chapter.folder / name
            if src.exists():
                chapter_files.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, chapter_files / name)
        make_chapter_package(chapter)

    archive = ROOT / "python_tutorial_ch02_optimized.zip"
    if archive.exists():
        (FILES_OUT / "archives").mkdir(parents=True, exist_ok=True)
        shutil.copy2(archive, FILES_OUT / "archives" / archive.name)


def human_size(path: Path) -> str:
    if not path.exists():
        return "生成中"
    size = float(path.stat().st_size)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return "生成中"


def status_label(chapter: Chapter) -> str:
    return "已开放" if is_public(chapter) else "敬请期待"


def status_class(chapter: Chapter) -> str:
    return "open" if is_public(chapter) else "soon"


def link(href: str, label: str, css_class: str = "") -> str:
    class_attr = f' class="{html.escape(css_class)}"' if css_class else ""
    return f'<a{class_attr} href="{html.escape(href)}" title="{html.escape(label)}">{html.escape(label)}</a>'


def topbar(depth: str = "") -> str:
    return f"""
<header class="topbar">
  <button class="icon-button nav-toggle" data-nav-toggle title="打开课程目录" aria-label="打开课程目录" aria-controls="course-sidebar" aria-expanded="false">目录</button>
  <a class="brand" href="{depth}index.html" aria-label="Python 教程首页">
    <span class="brand-mark">Py</span>
    <span class="brand-text">Python 教程</span>
  </a>
  <div class="top-actions">
    <a class="button ghost" href="{depth}files/">材料下载</a>
    <button class="icon-button" data-theme-toggle title="切换明暗主题" aria-label="切换明暗主题">Aa</button>
  </div>
</header>
"""


def nav_group(label: str, chapters: list[Chapter], active: int | None, depth: str, same_dir: bool) -> str:
    if not chapters:
        return ""
    items = [f'<section class="nav-group" aria-label="{html.escape(label)}">', f'<h2 class="nav-section-label">{html.escape(label)}</h2>']
    for chapter in chapters:
        href = chapter.page_name if same_dir else f"{depth}chapters/{chapter.page_name}"
        classes = ["nav-chapter", status_class(chapter)]
        if active == chapter.index:
            classes.append("active")
        current = ' aria-current="page"' if active == chapter.index else ""
        items.append(
            f'<a class="{" ".join(classes)}" href="{html.escape(href)}" '
            f'data-chapter-index="{chapter.index}"{current}>'
            f'<span class="chapter-number">{chapter.key.upper()}</span>'
            f'<span class="chapter-name">{html.escape(short_title(chapter.title))}</span>'
            f'<span class="chapter-status {status_class(chapter)}">{status_label(chapter)}</span>'
            "</a>"
        )
    items.append("</section>")
    return "\n".join(items)


def chapter_nav(chapters: list[Chapter], active: int | None, depth: str = "", same_dir: bool = False) -> str:
    opened = nav_group("已开放章节", open_chapters(chapters), active, depth, same_dir)
    upcoming = nav_group("敬请期待章节", upcoming_chapters(chapters), active, depth, same_dir)
    return f'<nav class="chapter-nav">{opened}{upcoming}</nav>'


def course_sidebar(chapters: list[Chapter], active: int | None, depth: str = "", same_dir: bool = False) -> str:
    return f"""
  <aside class="course-sidebar" id="course-sidebar" aria-label="课程目录">
    <div class="course-sidebar-inner">
      <div class="course-sidebar-brand">
        <span class="course-sidebar-mark">Py</span>
        <div>
          <p>Python 教程</p>
          <small>{release_range_label()} 正文开放</small>
        </div>
      </div>
      <div class="course-sidebar-summary">
        <span>当前开放</span>
        <strong>{release_range_label()}</strong>
        <small>ch00-ch10 全部正文已开放，整章材料包同步提供下载。</small>
      </div>
      <a class="course-sidebar-materials" href="{depth}files/">材料中心与整章下载</a>
      {chapter_nav(chapters, active, depth, same_dir)}
    </div>
  </aside>
"""


def layout_page(title: str, body: str, depth: str = "") -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} - Python 教程</title>
  <link rel="stylesheet" href="{depth}assets/site.css?v={ASSET_VERSION}" />
  <link rel="stylesheet" href="{depth}assets/pygments.css?v={ASSET_VERSION}" />
</head>
<body>
<div class="read-progress" aria-hidden="true"><span data-read-progress></span></div>
<div class="nav-backdrop" data-nav-backdrop></div>
{body}
<button class="back-to-top" data-back-top title="回到顶部" aria-label="回到顶部">↑</button>
<div class="image-lightbox" data-lightbox hidden>
  <button class="icon-button lightbox-close" data-lightbox-close title="关闭图片预览" aria-label="关闭图片预览">×</button>
  <img alt="" data-lightbox-img />
  <p data-lightbox-caption></p>
</div>
<script src="{depth}assets/site.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def hero_gallery(chapters: list[Chapter]) -> str:
    covers = chapters[:3]
    return "".join(
        f'<img src="{html.escape(version_asset_src(chapter.cover))}" alt="{html.escape(short_title(chapter.title))} 封面" loading="lazy" />'
        for chapter in covers
    )


def chapter_card(chapter: Chapter) -> str:
    locked = not is_public(chapter)
    package = DOWNLOADS_OUT / f"{chapter.folder.name}.zip"
    summary = (
        "正文页暂未开放，材料包已经可以下载。适合提前预习文件结构、示例代码和后续项目素材。"
        if locked
        else chapter.summary
    )
    return f"""
<article class="chapter-card {status_class(chapter)}" data-search-card>
  <a class="chapter-cover" href="chapters/{html.escape(chapter.page_name)}">
    <img src="{html.escape(version_asset_src(chapter.cover))}" alt="{html.escape(chapter.title)} 封面" loading="lazy" />
  </a>
  <div class="chapter-card-body">
    <div class="meta-row">
      <span class="meta-pill strong">{chapter.key.upper()}</span>
      <span class="meta-pill {status_class(chapter)}">{status_label(chapter)}</span>
      <span class="meta-pill">{chapter.image_count} 张图</span>
      <span class="meta-pill">{chapter.code_count} 个脚本</span>
    </div>
    <h2>{html.escape(short_title(chapter.title))}</h2>
    <p>{html.escape(summary)}</p>
    <div class="card-actions">
      <a class="button primary" href="chapters/{html.escape(chapter.page_name)}">{'查看占位页' if locked else '阅读章节'}</a>
      <a class="button" href="downloads/{html.escape(chapter.folder.name)}.zip">下载整章包</a>
      <span class="download-size">{human_size(package)}</span>
    </div>
  </div>
</article>
"""


def build_home(chapters: list[Chapter]) -> None:
    released = open_chapters(chapters)
    total_images = sum(chapter.image_count for chapter in chapters)
    total_code = sum(chapter.code_count for chapter in chapters)
    cards = "".join(chapter_card(chapter) for chapter in chapters)
    first_page = chapters[0].page_name
    body = f"""
{topbar()}
<div class="site-shell">
  {course_sidebar(chapters, None)}
  <main class="home-main">
    <section class="course-hero">
      <div class="hero-copy">
        <div class="hero-eyebrow">
          <span>本科生 Python 入门</span>
          <span>{release_range_label()} 正文开放</span>
          <span>全章节材料可下载</span>
        </div>
        <h1>Python 教程</h1>
        <p>从学习路线、运行环境、数据类型，到文件、界面、对象、数据分析、游戏、爬虫、图像处理与办公自动化。全部章节现在都可以直接阅读，并保留整章材料包下载入口。</p>
        <div class="hero-actions">
          <a class="button primary large" href="chapters/{html.escape(first_page)}">开始学习</a>
          <a class="button large" href="files/">进入材料中心</a>
        </div>
      </div>
      <div class="hero-panel" aria-label="课程预览">
        <div class="hero-gallery">{hero_gallery(chapters)}</div>
        <div class="stat-board compact">
          <div class="stat"><strong>{len(chapters)}</strong><span>章节总数</span></div>
          <div class="stat"><strong>{len(released)}</strong><span>正文开放</span></div>
          <div class="stat"><strong>{total_images}</strong><span>课程图片</span></div>
          <div class="stat"><strong>{total_code}</strong><span>代码脚本</span></div>
        </div>
      </div>
    </section>
    <section class="workspace-bar">
      <div>
        <strong>学习工作台</strong>
        <p>{html.escape(PUBLIC_RELEASE_NOTE)}</p>
      </div>
      <div class="tool-row">
        <input class="search" data-search type="search" placeholder="搜索章节、主题、关键词" />
      </div>
    </section>
    <section class="chapter-grid" aria-label="章节列表">
      {cards}
    </section>
    <p class="footer">站点由本地 Markdown 教程自动生成。</p>
  </main>
</div>
"""
    write_text(OUT / "index.html", layout_page("首页", body))


def material_group(title: str, description: str, items: list[str]) -> str:
    if not items:
        return ""
    links = []
    for rel in items:
        links.append(
            f'<a href="{html.escape(rel)}">'
            f'<span>{html.escape(Path(rel).name)}</span>'
            f'<small>{html.escape(rel)}</small>'
            "</a>"
        )
    return f"""
<section class="material-group">
  <div class="material-group-head">
    <div>
      <h2>{html.escape(title)}</h2>
      <p>{html.escape(description)}</p>
    </div>
    <span class="meta-pill strong">{len(items)} 个文件</span>
  </div>
  <div class="material-list">{''.join(links)}</div>
</section>
"""


def build_chapter_file_index(chapter: Chapter, chapters: list[Chapter]) -> None:
    package = DOWNLOADS_OUT / f"{chapter.folder.name}.zip"
    root_items = [name for name in MATERIAL_FILES if (chapter.folder / name).exists()]
    groups = [
        material_group("章节原文", "Markdown 正文，适合离线阅读或二次编辑。", material_items(chapter, "chapters")),
        material_group("代码脚本", "本章可运行示例、练习脚本和生成脚本。", material_items(chapter, "code")),
        material_group("实验报告", "运行结果、检查记录和整理说明。", material_items(chapter, "reports")),
        material_group("输出文件", "示例程序生成的图片、数据或文本输出。", material_items(chapter, "output")),
        material_group("整理备注", "素材来源、修订记录和辅助说明。", material_items(chapter, "source_notes")),
        material_group("构建脚本", "生成图片、报告或章节资源时使用的脚本。", material_items(chapter, "scripts")),
        material_group("章节说明", "根目录 README 与 manifest。", root_items),
    ]
    availability = "正文已开放" if is_public(chapter) else "正文敬请期待，材料包可先下载"
    body = f"""
{topbar("../../")}
<div class="site-shell">
  {course_sidebar(chapters, chapter.index, "../../")}
  <main class="home-main">
    <section class="download-hero">
      <div>
        <p class="article-kicker">{chapter.key.upper()} 材料</p>
        <h1>{html.escape(short_title(chapter.title))}</h1>
        <p>{html.escape(availability)}。所有配套文件已按用途分组；需要离线保存时，直接下载整章材料包。</p>
      </div>
      <div class="download-actions">
        <a class="button primary large" href="../../downloads/{html.escape(chapter.folder.name)}.zip">下载整章材料包</a>
        <a class="button large" href="../../chapters/{html.escape(chapter.page_name)}">查看章节页面</a>
        <span class="meta-pill strong">{human_size(package)}</span>
      </div>
    </section>
    <section class="materials-grid" aria-label="材料文件分组">
      {''.join(groups)}
    </section>
  </main>
</div>
"""
    write_text(FILES_OUT / chapter.folder.name / "index.html", layout_page(f"{chapter.key.upper()} 材料", body, "../../"))


def download_card(chapter: Chapter) -> str:
    package = DOWNLOADS_OUT / f"{chapter.folder.name}.zip"
    locked = not is_public(chapter)
    summary = (
        "正文页暂未开放，但整章材料包已经生成。可以提前下载代码、报告、图片与原始 Markdown。"
        if locked
        else chapter.summary
    )
    return f"""
<article class="download-card {status_class(chapter)}" data-search-card>
  <div class="chapter-card-body">
    <div class="meta-row">
      <span class="meta-pill strong">{chapter.key.upper()}</span>
      <span class="meta-pill {status_class(chapter)}">{status_label(chapter)}</span>
      <span class="meta-pill">{material_file_count(chapter)} 个文件</span>
      <span class="meta-pill">{human_size(package)}</span>
    </div>
    <h2>{html.escape(short_title(chapter.title))}</h2>
    <p>{html.escape(summary)}</p>
    <div class="download-actions">
      <a class="button primary" href="../downloads/{html.escape(chapter.folder.name)}.zip">下载整包</a>
      <a class="button" href="{html.escape(chapter.folder.name)}/">查看文件</a>
      <a class="button" href="../chapters/{html.escape(chapter.page_name)}">{'查看开放状态' if locked else '阅读章节'}</a>
    </div>
  </div>
</article>
"""


def build_files_index(chapters: list[Chapter]) -> None:
    for chapter in chapters:
        build_chapter_file_index(chapter, chapters)
    archive_link = ""
    if (FILES_OUT / "archives" / "python_tutorial_ch02_optimized.zip").exists():
        archive_link = '<a class="button" href="archives/python_tutorial_ch02_optimized.zip">ch02 优化包</a>'
    body = f"""
{topbar("../")}
<div class="site-shell">
  {course_sidebar(chapters, None, "../")}
  <main class="home-main">
    <section class="download-center-hero">
      <div>
        <p class="article-kicker">材料中心</p>
        <h1>按章节打包下载</h1>
        <p>ch00-ch10 正文与整章材料包都已经开放。需要备课、离线学习或复查代码时，可以直接按章下载。</p>
      </div>
      <div class="stat-board compact">
        <div class="stat"><strong>{len(chapters)}</strong><span>可下载章节</span></div>
        <div class="stat"><strong>{sum(material_file_count(c) for c in chapters)}</strong><span>材料文件</span></div>
        <div class="stat"><strong>{sum(c.code_count for c in chapters)}</strong><span>代码脚本</span></div>
        <div class="stat"><strong>{len(open_chapters(chapters))}</strong><span>正文开放</span></div>
      </div>
    </section>
    <section class="workspace-bar">
      <div>
        <strong>下载提示</strong>
        <p>{html.escape(PUBLIC_RELEASE_NOTE)}</p>
      </div>
      <div class="tool-row">
        <input class="search" data-search type="search" placeholder="搜索章节或材料关键词" />
        {archive_link}
      </div>
    </section>
    <section class="download-grid" aria-label="材料下载列表">
      {''.join(download_card(chapter) for chapter in chapters)}
    </section>
  </main>
</div>
"""
    write_text(FILES_OUT / "index.html", layout_page("材料下载", body, "../"))


def file_links(chapter: Chapter) -> str:
    base = f"../files/{chapter.folder.name}"
    links: list[str] = [
        link(f"../downloads/{chapter.folder.name}.zip", "下载整章材料包"),
        link(f"{base}/", "查看完整材料清单"),
        link(f"{base}/chapters/{chapter.markdown.name}", "本章 Markdown"),
    ]
    code_dir = chapter.folder / "code"
    if code_dir.exists():
        for path in sorted(code_dir.rglob("*.py"))[:8]:
            rel = path.relative_to(chapter.folder).as_posix()
            links.append(link(f"{base}/{rel}", rel))
    reports = chapter.folder / "reports"
    if reports.exists():
        for path in sorted(reports.glob("*.md"))[:4]:
            rel = path.relative_to(chapter.folder).as_posix()
            links.append(link(f"{base}/{rel}", rel))
    note = '<p class="file-panel-note">这里放高频入口；完整代码、输出和整理脚本请进入材料清单页查看。</p>'
    return note + '<div class="file-links">' + "\n".join(links) + "</div>"


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
    if not items:
        return '<p class="toc-empty">本页暂无正文目录。</p>'
    return "<ol>" + "\n".join(items) + "</ol>"


def pager_link(chapter: Chapter | None, label: str, css_class: str = "") -> str:
    if chapter is None:
        return "<span></span>"
    return (
        f'<a class="{html.escape(css_class)}" href="{html.escape(chapter.page_name)}">'
        f'<small>{html.escape(label)}</small><strong>{html.escape(short_title(chapter.title))}</strong></a>'
    )


def build_chapter_pages(chapters: list[Chapter]) -> None:
    for i, chapter in enumerate(chapters):
        locked = not is_public(chapter)
        if locked:
            chapter.headings = []
            chapter.html_body = ""
        else:
            md = read_text(chapter.markdown)
            chapter.html_body, chapter.headings = render_markdown(md, chapter.key)

        prev_chapter = chapters[i - 1] if i > 0 else None
        next_chapter = chapters[i + 1] if i + 1 < len(chapters) else None
        pager = (
            '<nav class="pager" aria-label="章节切换">'
            f'{pager_link(prev_chapter, "上一章")}'
            f'{pager_link(next_chapter, "下一章", "next")}'
            "</nav>"
        )

        if locked:
            body = f"""
{topbar("../")}
<div class="chapter-shell">
  {course_sidebar(chapters, chapter.index, "../", same_dir=True)}
  <main class="article-main">
    <section class="locked-hero" id="top">
      <p class="article-kicker">{chapter.key.upper()} · 正文待开放</p>
      <h1>敬请期待</h1>
      <p>{html.escape(short_title(chapter.title))} 的网页正文正在整理完善。当前正文开放范围是 {release_range_label()}；本章材料包已生成，可以先下载代码、报告、图片与 Markdown 原文。</p>
      <div class="locked-actions">
        <a class="button primary large" href="../downloads/{html.escape(chapter.folder.name)}.zip">下载本章材料包</a>
        <a class="button large" href="../files/{html.escape(chapter.folder.name)}/">查看材料清单</a>
        <a class="button large" href="{prev_chapter.page_name if prev_chapter else '../index.html'}">阅读上一章</a>
      </div>
    </section>
    {pager}
  </main>
  <aside class="toc-panel">
    <div class="toc-inner">
      <p class="toc-title">本页目录</p>
      <ol><li><a class="level-2" href="#top">敬请期待</a></li></ol>
    </div>
  </aside>
</div>
"""
        else:
            body = f"""
{topbar("../")}
<div class="chapter-shell">
  {course_sidebar(chapters, chapter.index, "../", same_dir=True)}
  <main class="article-main">
    <header class="article-head">
      <p class="article-kicker">{chapter.key.upper()} · 正文已开放</p>
      <h1>{html.escape(chapter.title)}</h1>
      <p>{html.escape(chapter.summary)}</p>
      <div class="article-actions">
        <a class="button primary" href="../downloads/{html.escape(chapter.folder.name)}.zip">下载材料包</a>
        <a class="button" href="../files/{html.escape(chapter.folder.name)}/">材料清单</a>
        <a class="button" href="../files/{html.escape(chapter.folder.name)}/chapters/{html.escape(chapter.markdown.name)}">Markdown 原文</a>
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
    {pager}
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
        "title": "Python 教程",
        "chapter_count": len(chapters),
        "open_chapter_count": len(open_chapters(chapters)),
        "public_chapter_max": PUBLIC_CHAPTER_MAX,
        "public_range": release_range_label(),
        "release_note": PUBLIC_RELEASE_NOTE,
        "downloads_available_for_all_chapters": True,
        "chapters": [
            {
                "key": c.key,
                "title": c.title,
                "page": f"chapters/{c.page_name}",
                "files_page": f"files/{c.folder.name}/",
                "download": f"downloads/{c.folder.name}.zip",
                "markdown": str(c.markdown.relative_to(ROOT)).replace("\\", "/"),
                "images": c.image_count,
                "code_files": c.code_count,
                "material_files": material_file_count(c),
                "is_public": is_public(c),
                "content_status": "open" if is_public(c) else "coming_soon",
                "download_status": "available",
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
    copy_site_assets(chapters)
    build_chapter_pages(chapters)
    build_home(chapters)
    build_files_index(chapters)
    build_manifest(chapters)
    print(f"Built {len(chapters)} chapters into {OUT}")


if __name__ == "__main__":
    main()
