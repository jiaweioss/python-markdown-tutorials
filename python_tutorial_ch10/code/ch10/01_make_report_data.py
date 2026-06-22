"""Create small report data for the office automation chapter."""
import csv
from pathlib import Path

Path("input").mkdir(exist_ok=True)
rows = [
    {"chapter": "ch01", "status": "done", "artifact": "environment log", "score": "92"},
    {"chapter": "ch02", "status": "done", "artifact": "data cards", "score": "88"},
    {"chapter": "ch03", "status": "done", "artifact": "file archiver", "score": "90"},
    {"chapter": "ch06", "status": "done", "artifact": "learning dashboard", "score": "95"},
    {"chapter": "ch09", "status": "done", "artifact": "image report", "score": "91"},
]
with open("input/report_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print("已生成 input/report_data.csv")
