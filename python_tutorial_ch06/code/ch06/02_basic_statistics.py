"""Analyze the sample CSV with the standard library."""
import csv
from statistics import mean

with open("input/learning_records.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

minutes = [int(row["minutes"]) for row in rows]
rt = [int(row["rt_ms"]) for row in rows]
done = [row for row in rows if row["done"] == "yes"]

print("记录数：", len(rows))
print("平均学习时长：", round(mean(minutes), 2))
print("平均反应时：", round(mean(rt), 2))
print("完成率：", f"{len(done) / len(rows):.0%}")
