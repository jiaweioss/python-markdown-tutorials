"""Generate a Markdown report from CSV."""
import csv
from pathlib import Path

Path("reports").mkdir(exist_ok=True)
with open("input/report_data.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

average_score = sum(int(row["score"]) for row in rows) / len(rows)

lines = [
    "# 科研卡片工厂结课报告",
    "",
    f"- 章节数量：{len(rows)}",
    f"- 平均完成分：{average_score:.1f}",
    "",
    "| 章节 | 状态 | 作品 | 完成分 |",
    "| --- | --- | --- | --- |",
]
for row in rows:
    lines.append(f"| {row['chapter']} | {row['status']} | {row['artifact']} | {row['score']} |")
Path("reports/final_report.md").write_text("\n".join(lines), encoding="utf-8")
print("已生成 reports/final_report.md")
