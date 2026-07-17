"""Chapter 02 demo: repeat work with for and while."""

scores = [86, 55, 92, 48]
passed_scores = []
total = 0

for score in scores:
    total += score
    if score >= 60:
        passed_scores.append(score)

print("通过的分数：", passed_scores)
print("平均分：", total / len(scores))

for attempt in range(1, 4):
    print(f"第 {attempt} 次练习")

remaining = 3
while remaining > 0:
    print(f"还剩 {remaining} 次练习")
    remaining -= 1

print("本轮结束")
