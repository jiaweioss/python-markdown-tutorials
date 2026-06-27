"""Chapter 03 project extension: create a reproducible archive manifest."""

from __future__ import annotations

from pathlib import Path
import hashlib
import shutil


ROOT = Path("workspace_ch03")
INBOX = ROOT / "inbox"
ORGANIZED = ROOT / "organized"
OUTPUT = ROOT / "output"
REPORT = OUTPUT / "ch03_archive_manifest.md"
PREVIEW = OUTPUT / "ch03_archive_manifest_preview.png"
PREVIEW_ASSET = Path("assets/ch03/web/ch03_archive_manifest_preview.png")


SAMPLES = {
    "experiment_notes.txt": "participant notes\ncondition A\ncondition B\n",
    "scores.csv": "name,score\n小美,92\n小明,86\n小东,78\n",
    "summary.md": "# Summary\n\nThe archive is ready for review.\n",
    "figure.png": "fake image bytes for file-operation demo\n",
}


def suffix_folder(path: Path) -> str:
    return path.suffix[1:] if path.suffix else "no_suffix"


def ensure_demo_archive() -> None:
    """Create the same safe demo archive used by the chapter project."""
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


def role_for(path: Path) -> str:
    first = path.relative_to(ROOT).parts[0]
    if first == "data":
        return "raw data"
    if first == "inbox":
        return "source"
    if first == "organized":
        return "archived copy"
    if first == "output":
        return "report"
    return "workspace"


def collect_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    skip = {REPORT.resolve(), PREVIEW.resolve()}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.resolve() in skip:
            continue
        relative = path.relative_to(ROOT).as_posix()
        rows.append(
            {
                "path": relative,
                "suffix": path.suffix or "(none)",
                "size": path.stat().st_size,
                "role": role_for(path),
                "sha256": sha256_prefix(path),
            }
        )
    return rows


def write_markdown(rows: list[dict[str, str | int]]) -> None:
    lines = [
        "# Chapter 03 Archive Manifest",
        "",
        "This manifest records the demo archive files generated in `workspace_ch03`.",
        "",
        "| Path | Role | Suffix | Size | SHA-256 prefix |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['path']}` | {row['role']} | `{row['suffix']}` | {row['size']} | `{row['sha256']}` |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_demo_archive()
    rows = collect_rows()
    write_markdown(rows)

    print(f"Wrote {REPORT}")
    print(f"Files recorded: {len(rows)}")


if __name__ == "__main__":
    main()
