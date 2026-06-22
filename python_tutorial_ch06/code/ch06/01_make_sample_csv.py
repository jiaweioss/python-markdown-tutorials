"""Create a small learning-data CSV."""
import csv
from pathlib import Path

rows = [
    {"topic": "变量", "minutes": 18, "done": "yes", "rt_ms": 520},
    {"topic": "列表", "minutes": 25, "done": "yes", "rt_ms": 480},
    {"topic": "字典", "minutes": 22, "done": "no", "rt_ms": 610},
]
Path("input").mkdir(exist_ok=True)
with open("input/learning_records.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print("已生成 input/learning_records.csv")
