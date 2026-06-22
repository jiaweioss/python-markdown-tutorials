"""Chapter 03 demo: create a safe file-workspace for later examples."""

from pathlib import Path


ROOT = Path("workspace_ch03")
DATA = ROOT / "data"
OUTPUT = ROOT / "output"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    (DATA / "raw_notes.txt").write_text(
        "Python file demo\n"
        "line 1: read files safely\n"
        "line 2: write results clearly\n"
        "line 3: keep raw data untouched\n",
        encoding="utf-8",
    )
    (DATA / "scores.csv").write_text(
        "name,score\n"
        "小美,92\n"
        "小明,86\n"
        "小东,78\n",
        encoding="utf-8",
    )

    print("Created:", DATA.resolve())
    print("Created:", OUTPUT.resolve())


if __name__ == "__main__":
    main()
