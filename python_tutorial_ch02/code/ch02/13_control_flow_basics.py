"""Chapter 02 demo: make choices with if, elif, and else."""

score = 86

if score >= 90:
    level = "优秀"
elif score >= 60:
    level = "通过"
else:
    level = "需要复习"

print("分数：", score)
print("结果：", level)

student = {"name": "小明"}
if "age" in student:
    print("年龄：", student["age"])
else:
    print("年龄：尚未记录")
