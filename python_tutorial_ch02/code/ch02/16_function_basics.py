"""Chapter 02 demo: package repeatable work in functions."""


def score_level(score):
    if score >= 90:
        return "优秀"
    if score >= 60:
        return "通过"
    return "需要复习"


def greeting(name):
    return f"你好，{name}！"


print(greeting("小明"))
print("86 分：", score_level(86))
print("58 分：", score_level(58))
