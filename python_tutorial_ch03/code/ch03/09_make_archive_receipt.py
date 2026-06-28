"""Chapter 03 project extension: create an archive delivery receipt."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import shutil


ROOT = Path("workspace_ch03")
INBOX = ROOT / "inbox"
ORGANIZED = ROOT / "organized"
OUTPUT = ROOT / "output"
RECEIPT = OUTPUT / "ch03_archive_receipt.md"


SAMPLES = {
    "experiment_notes.txt": "participant notes\ncondition A\ncondition B\n",
    "scores.csv": "name,score\n小美,92\n小明,86\n小东,78\n",
    "summary.md": "# Summary\n\nThe archive is ready for review.\n",
    "figure.png": "fake image bytes for file-operation demo\n",
}


def suffix_folder(path: Path) -> str:
    return path.suffix[1:] if path.suffix else "no_suffix"


def ensure_demo_archive() -> None:
    INBOX.mkdir(parents=True, exist_ok=True)
    ORGANIZED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    for name, content in SAMPLES.items():
        source = INBOX / name
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
        (OUTPUT / "ch03_archive_manifest.md").resolve(),
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

def main() -> None:
    ensure_demo_archive()
    paths = collect_files()
    summary = summarize(paths)
    write_markdown(summary)

    print(f"Wrote {RECEIPT}")
    print(f"Files summarized: {summary['file_count']}")

if __name__ == "__main__":
    main()
