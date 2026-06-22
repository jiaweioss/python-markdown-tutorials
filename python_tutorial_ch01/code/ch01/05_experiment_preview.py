"""A tiny Stroop-like psychology experiment preview.

This is NOT a precise experiment framework. It is only a Chapter 1 preview.
"""

import time

participant_id = input("请输入被试编号（例如 S001）：").strip() or "S001"
stimulus_word = "RED"
ink_color = "blue"
correct_key = "j"

print("\n实验开始")
print("被试编号：", participant_id)

print("\n请注视屏幕中央：+")
time.sleep(0.5)

print("\n请判断词的墨水颜色，而不是词义。")
print("如果是红色按 f，如果是蓝色按 j。")
print("刺激词：", stimulus_word)
print("墨水颜色：", ink_color)

start = time.perf_counter()
response = input("请输入你的反应（f/j）：").strip()
end = time.perf_counter()

reaction_time_ms = round((end - start) * 1000, 2)

print("\n实验结束")
print("你的反应是：", response)
print("是否正确：", response == correct_key)
print("粗略反应时：", reaction_time_ms, "毫秒")
print("说明：这只是入门演示，正式实验需要更严格的计时和数据保存。")
