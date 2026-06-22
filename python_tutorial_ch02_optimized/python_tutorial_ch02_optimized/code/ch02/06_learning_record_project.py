"""Chapter 02 mini project: organize learning records with data types."""

from pathlib import Path


def build_report(student: dict) -> str:
    scores = student["scores"]
    average_score = sum(scores) / len(scores)
    passed = average_score >= 60
    status = "通过" if passed else "需要继续练习"
    skills = "、".join(student["skills"])

    return (
        f"姓名：{student['name']}\n"
        f"练习次数：{len(scores)}\n"
        f"平均分：{average_score:.1f}\n"
        f"掌握技能：{skills}\n"
        f"状态：{status}\n"
    )


def main() -> None:
    student = {
        "name": "小明",
        "scores": [86, 92, 78],
        "skills": ["字符串", "列表", "字典"],
        "notes": "索引从 0 开始，切片左闭右开。",
    }

    report = build_report(student)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "ch02_learning_report.txt"
    output_file.write_text(report, encoding="utf-8")

    print(report)
    print("Saved to:", output_file)


if __name__ == "__main__":
    main()
