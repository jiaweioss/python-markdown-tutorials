"""
learning_passport.py
第0章小作品：生成一张科研卡片工厂启动卡。
运行方式：python learning_passport.py
"""
from pathlib import Path
from datetime import date

print("欢迎启动科研卡片工厂。")
print("请填写一张项目启动卡，先把目标、原料和投入时间写清楚。")

name = input("你的名字或昵称：").strip() or "匿名学习者"
goal = input("你最想用 Python 做什么：").strip() or "做一个能跑的小作品"
material = input("你最想整理的材料类型：").strip() or "课堂笔记"
weekly_hours = input("每周预计学习小时数：").strip() or "3"

skills = ["环境体检", "原料入库", "卡片字段设计", "运行日志记录"]
start_card_text = f"""# 科研卡片工厂启动卡

姓名：{name}

启动日期：{date.today()}

工厂目标：{goal}

第一批原料：{material}

每周投入：{weekly_hours} 小时

## 第一阶段启动清单

"""

for skill in skills:
    start_card_text += f"- [ ] {skill}\n"

start_card_text += """
## 给未来自己的留言

今天你只是建了一个空工厂。没关系，真正厉害的系统，都是从第一张能保存下来的卡片开始的。
"""

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "factory_start_card.md"
output_file.write_text(start_card_text, encoding="utf-8")

print(f"已生成：{output_file.resolve()}")
print("启动卡已生成。下一步：把第一份原料放进 input/，让工厂真的开工。")
