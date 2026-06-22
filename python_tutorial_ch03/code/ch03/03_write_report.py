"""Chapter 03 demo: write a text report from a CSV-like file."""

from pathlib import Path


ROOT = Path("workspace_ch03")
DATA_FILE = ROOT / "data" / "scores.csv"
REPORT_FILE = ROOT / "output" / "score_report.txt"


def load_scores(path: Path) -> list[tuple[str, int]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    records: list[tuple[str, int]] = []
    for line in lines[1:]:
        name, score_text = line.split(",")
        records.append((name, int(score_text)))
    return records


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError("Run 01_create_sample_files.py first.")

    records = load_scores(DATA_FILE)
    average = sum(score for _, score in records) / len(records)
    best_name, best_score = max(records, key=lambda item: item[1])

    report = [
        "第3章成绩报告",
        f"记录数量：{len(records)}",
        f"平均分：{average:.1f}",
        f"最高分：{best_name} {best_score}",
    ]
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(REPORT_FILE.read_text(encoding="utf-8"))
    print("Saved to:", REPORT_FILE)


if __name__ == "__main__":
    main()
