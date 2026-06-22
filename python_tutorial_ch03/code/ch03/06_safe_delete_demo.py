"""Chapter 03 demo: safe deletion inside a known workspace only."""

from pathlib import Path
import shutil


ROOT = Path("workspace_ch03").resolve()
TRASH = ROOT / "trash_demo"


def ensure_inside_workspace(path: Path) -> Path:
    resolved = path.resolve()
    if ROOT not in resolved.parents and resolved != ROOT:
        raise ValueError(f"Refuse to delete outside workspace: {resolved}")
    return resolved


def main() -> None:
    TRASH.mkdir(parents=True, exist_ok=True)
    demo_file = TRASH / "delete_me.txt"
    demo_file.write_text("This file is safe to delete.\n", encoding="utf-8")

    target = ensure_inside_workspace(TRASH)
    print("About to remove:", target)
    shutil.rmtree(target)
    print("Removed safely:", target)


if __name__ == "__main__":
    main()
