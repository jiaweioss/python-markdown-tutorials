"""Chapter 03 project extension: create an archive delivery receipt."""

from __future__ import annotations

from base64 import b64decode
from collections import Counter
from pathlib import Path
import hashlib
import shutil


ROOT = Path("workspace_ch03")
INBOX = ROOT / "inbox"
ORGANIZED = ROOT / "organized"
OUTPUT = ROOT / "output"
RECEIPT = OUTPUT / "ch03_archive_receipt.md"
PREVIEW = OUTPUT / "ch03_archive_receipt_preview.png"
PREVIEW_ASSET = Path("assets/ch03/web/ch03_archive_receipt_preview.png")
DEMO_PNG = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAIAAAAmkwkpAAAAE0lEQVR4nGPUz/7PAANMcBZeDgBQFgGhOmjLnwAAAABJRU5ErkJggg=="
)


SAMPLES = {
    "experiment_notes.txt": "participant notes\ncondition A\ncondition B\n",
    "scores.csv": "name,score\n小美,92\n小明,86\n小东,78\n",
    "summary.md": "# Summary\n\nThe archive is ready for review.\n",
    "figure.png": DEMO_PNG,
}


def suffix_folder(path: Path) -> str:
    return path.suffix[1:] if path.suffix else "no_suffix"


def ensure_demo_archive() -> None:
    INBOX.mkdir(parents=True, exist_ok=True)
    ORGANIZED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    for name, content in SAMPLES.items():
        source = INBOX / name
        if isinstance(content, bytes):
            source.write_bytes(content)
        else:
            source.write_text(content, encoding="utf-8")
        target_dir = ORGANIZED / suffix_folder(source)
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target_dir / source.name)


def sha256_prefix(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:12]


def collect_files() -> list[Path]:
    skip = {
        RECEIPT.resolve(),
        PREVIEW.resolve(),
        (OUTPUT / "ch03_archive_manifest.md").resolve(),
        (OUTPUT / "ch03_archive_manifest_preview.png").resolve(),
    }
    return [
        path
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.resolve() not in skip
    ]


def summarize(paths: list[Path]) -> dict[str, object]:
    suffix_counts = Counter(path.suffix.lower() or "(none)" for path in paths)
    role_counts = Counter(path.relative_to(ROOT).parts[0] for path in paths)
    total_size = sum(path.stat().st_size for path in paths)
    organized_files = [p for p in paths if p.relative_to(ROOT).parts[0] == "organized"]
    source_files = [p for p in paths if p.relative_to(ROOT).parts[0] == "inbox"]
    return {
        "file_count": len(paths),
        "source_count": len(source_files),
        "organized_count": len(organized_files),
        "type_count": len(suffix_counts),
        "total_size": total_size,
        "suffix_counts": suffix_counts,
        "role_counts": role_counts,
        "sample_hashes": [(p.relative_to(ROOT).as_posix(), sha256_prefix(p)) for p in organized_files[:4]],
    }


def write_markdown(summary: dict[str, object]) -> None:
    suffix_counts: Counter[str] = summary["suffix_counts"]  # type: ignore[assignment]
    sample_hashes: list[tuple[str, str]] = summary["sample_hashes"]  # type: ignore[assignment]

    lines = [
        "# Chapter 03 Archive Receipt",
        "",
        "This receipt is a compact delivery note for the demo archive in `workspace_ch03`.",
        "",
        "## Summary",
        "",
        f"- Source files: {summary['source_count']}",
        f"- Organized copies: {summary['organized_count']}",
        f"- File types: {summary['type_count']}",
        f"- Total recorded size: {summary['total_size']} bytes",
        "",
        "## File Types",
        "",
        "| Suffix | Count |",
        "| --- | ---: |",
    ]
    for suffix, count in sorted(suffix_counts.items()):
        lines.append(f"| `{suffix}` | {count} |")

    lines.extend(["", "## Hash Spot Check", "", "| Path | SHA-256 prefix |", "| --- | --- |"])
    for path, digest in sample_hashes:
        lines.append(f"| `{path}` | `{digest}` |")

    lines.extend(
        [
            "",
            "## Delivery Meaning",
            "",
            "A manifest answers: what exact files are present?",
            "A receipt answers: can this archive be handed to another person for review?",
            "",
        ]
    )
    RECEIPT.write_text("\n".join(lines), encoding="utf-8")


def make_preview(summary: dict[str, object]) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def load_font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()

    width, height = 1500, 920
    image = Image.new("RGB", (width, height), "#F7F9FC")
    draw = ImageDraw.Draw(image)
    title_font = load_font(54, True)
    h_font = load_font(30, True)
    body_font = load_font(24)
    small_font = load_font(20)
    mono_font = load_font(21)

    colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]
    draw.text((75, 58), "Archive Receipt", font=title_font, fill="#172033")
    draw.text((80, 128), "A compact delivery note for the organized workspace.", font=body_font, fill="#5D6678")

    metrics = [
        ("source", summary["source_count"]),
        ("copies", summary["organized_count"]),
        ("types", summary["type_count"]),
        ("bytes", summary["total_size"]),
    ]
    for idx, (label, value) in enumerate(metrics):
        x = 80 + idx * 350
        draw.rounded_rectangle((x + 8, 205 + 10, x + 300 + 8, 355 + 10), radius=24, fill="#D8DEE9")
        draw.rounded_rectangle((x, 205, x + 300, 355), radius=24, fill="white", outline=colors[idx], width=4)
        draw.rounded_rectangle((x + 25, 230, x + 130, 270), radius=20, fill=colors[idx])
        draw.text((x + 48, 237), label, font=small_font, fill="white")
        draw.text((x + 36, 288), str(value), font=h_font, fill="#172033")

    suffix_counts: Counter[str] = summary["suffix_counts"]  # type: ignore[assignment]
    max_count = max(suffix_counts.values()) if suffix_counts else 1
    draw.rounded_rectangle((80, 420, 700, 760), radius=24, fill="white", outline="#D9E1EE", width=2)
    draw.text((120, 455), "File Types", font=h_font, fill="#172033")
    y = 520
    for idx, (suffix, count) in enumerate(sorted(suffix_counts.items())):
        color = colors[idx % len(colors)]
        bar_w = int(360 * count / max_count)
        draw.text((125, y - 5), suffix, font=mono_font, fill="#172033")
        draw.rounded_rectangle((245, y, 245 + bar_w, y + 24), radius=12, fill=color)
        draw.text((625, y - 5), str(count), font=small_font, fill="#5D6678")
        y += 48

    sample_hashes: list[tuple[str, str]] = summary["sample_hashes"]  # type: ignore[assignment]
    draw.rounded_rectangle((780, 420, 1420, 760), radius=24, fill="white", outline="#D9E1EE", width=2)
    draw.text((820, 455), "Hash Spot Check", font=h_font, fill="#172033")
    y = 520
    for path, digest in sample_hashes:
        short_path = path if len(path) <= 33 else "..." + path[-30:]
        draw.text((820, y), short_path, font=small_font, fill="#172033")
        draw.text((1180, y), digest, font=mono_font, fill="#2F6BFF")
        y += 52

    draw.rounded_rectangle((250, 815, 1250, 872), radius=22, fill="#F1FFF7", outline="#9BD7B7", width=2)
    draw.text((320, 830), "Manifest records the files. Receipt tells whether the archive is ready to hand over.", font=small_font, fill="#176342")

    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    image.save(PREVIEW, optimize=True, quality=95)
    PREVIEW_ASSET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, PREVIEW_ASSET)
    return True


def main() -> None:
    ensure_demo_archive()
    paths = collect_files()
    summary = summarize(paths)
    write_markdown(summary)
    has_preview = make_preview(summary)

    print(f"Wrote {RECEIPT}")
    print(f"Wrote {PREVIEW if has_preview else 'no preview: Pillow not installed'}")
    print(f"Files summarized: {summary['file_count']}")


if __name__ == "__main__":
    main()
