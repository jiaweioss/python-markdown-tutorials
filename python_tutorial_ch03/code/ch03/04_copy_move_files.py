"""Chapter 03 demo: copy and move files inside a safe workspace."""

from pathlib import Path
import shutil


ROOT = Path("workspace_ch03")
DATA = ROOT / "data"
OUTPUT = ROOT / "output"
ARCHIVE = ROOT / "archive"


def main() -> None:
    source = DATA / "raw_notes.txt"
    if not source.exists():
        raise FileNotFoundError("Run 01_create_sample_files.py first.")

    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    copied = OUTPUT / "raw_notes_copy.txt"
    shutil.copyfile(source, copied)
    print("Copied:", copied)

    moved = ARCHIVE / "raw_notes_copy_archived.txt"
    if moved.exists():
        moved.unlink()
    shutil.move(str(copied), str(moved))
    print("Moved:", moved)


if __name__ == "__main__":
    main()
