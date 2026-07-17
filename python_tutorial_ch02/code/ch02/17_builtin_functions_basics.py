"""第 2 章：零基础常用内置函数。"""

scores = [86, 92, 78]

score_count = len(scores)
total_score = sum(scores)
lowest_score = min(scores)
highest_score = max(scores)
average_score = round(total_score / score_count, 1)

print("数据类型：", type(scores))
print("人数：", score_count)
print("总分：", total_score)
print("最低分：", lowest_score)
print("最高分：", highest_score)
print("平均分：", average_score)

print("A", "B", sep=" | ")
