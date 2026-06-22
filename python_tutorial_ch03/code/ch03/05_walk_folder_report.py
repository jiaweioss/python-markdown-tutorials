"""Chapter 03 demo: walk a folder tree and write a file-size report."""

from pathlib import Path


ROOT = Path("workspace_ch03")
REPORT = ROOT / "output" / "file_inventory.md"


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def main() -> None:
    if not ROOT.exists():
        raise FileNotFoundError("Run 01_create_sample_files.py first.")

    lines = ["# File Inventory", ""]
    for path in iter_files(ROOT):
        relative = path.relative_to(ROOT)
        size = path.stat().st_size
        lines.append(f"- `{relative}`: {size} bytes")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
