"""Save collected links to CSV."""
import csv
from pathlib import Path

links = [
    {"title": "Python 官网", "url": "https://www.python.org/"},
    {"title": "Python 文档", "url": "https://docs.python.org/3/"},
]
Path("output").mkdir(exist_ok=True)
with open("output/links.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "url"])
    writer.writeheader()
    writer.writerows(links)
print("已保存 output/links.csv")
