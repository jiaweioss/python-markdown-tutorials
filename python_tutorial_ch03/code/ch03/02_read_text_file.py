"""Chapter 03 demo: read text with Path and with open."""

from pathlib import Path


ROOT = Path("workspace_ch03")
RAW_FILE = ROOT / "data" / "raw_notes.txt"


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError("Run 01_create_sample_files.py first.")

    print("Current working directory:", Path.cwd())

    text = RAW_FILE.read_text(encoding="utf-8")
    print("\nRead with Path.read_text():")
    print(text)

    print("Read line by line with with open():")
    with RAW_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            print(line_number, line.strip())


if __name__ == "__main__":
    main()
