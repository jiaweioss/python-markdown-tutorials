"""Chapter 03 mini project: organize files by suffix and create a report."""

from pathlib import Path
import shutil


ROOT = Path("workspace_ch03")
INBOX = ROOT / "inbox"
ARCHIVE = ROOT / "organized"
REPORT = ROOT / "output" / "archive_report.md"


def seed_inbox() -> None:
    INBOX.mkdir(parents=True, exist_ok=True)
    samples = {
        "experiment_notes.txt": "participant notes\n",
        "scores.csv": "name,score\n小美,92\n",
        "summary.md": "# Summary\n",
        "figure.png": "fake image bytes for demo\n",
    }
    for name, content in samples.items():
        (INBOX / name).write_text(content, encoding="utf-8")


def suffix_folder(path: Path) -> str:
    return path.suffix[1:] if path.suffix else "no_suffix"


def main() -> None:
    seed_inbox()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    rows = ["# Archive Report", ""]
    for source in sorted(INBOX.iterdir()):
        if not source.is_file():
            continue
        folder = ARCHIVE / suffix_folder(source)
        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / source.name
        shutil.copyfile(source, destination)
        rows.append(f"- `{source.name}` -> `{destination.relative_to(ROOT)}`")

    REPORT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
