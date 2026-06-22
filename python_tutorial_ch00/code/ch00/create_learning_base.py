"""
create_learning_base.py
第0章项目任务：创建一个干净的科研卡片工厂工作区。
运行方式：python create_learning_base.py
"""
from pathlib import Path
from datetime import datetime

base = Path("python_card_factory")
folders = [
    "code/ch00",
    "input",
    "cards",
    "output",
    "reports",
    "assets",
]

for folder in folders:
    path = base / folder
    path.mkdir(parents=True, exist_ok=True)

readme = base / "README.md"
readme.write_text(
    "# Python Card Factory\n\n"
    "这是由第0章脚本自动创建的科研卡片工厂工作区。\n\n"
    "## 文件夹说明\n\n"
    "- code/：放 Python 脚本。\n"
    "- input/：放原料，例如文献摘录、课堂笔记、CSV 表格。\n"
    "- cards/：放生成后的学习卡片。\n"
    "- output/：放程序输出结果，例如图表、临时结果和导出文件。\n"
    "- reports/：放报告、运行日志和复盘记录。\n"
    "- assets/：放图片、图标等素材。\n",
    encoding="utf-8",
)

sample_csv = base / "input" / "source_materials.csv"
sample_csv.write_text(
    "title,source,keyword,note\n"
    "Python入门目标,课堂笔记,目标,把模糊想法拆成可运行步骤\n"
    "自动化判断,xkcd漫画,自动化,重复且容易出错的任务才值得脚本化\n"
    "项目目录,第0章,工程习惯,原料、卡片、成品和报告要分开放\n",
    encoding="utf-8",
)

log = base / "reports" / "factory_log.md"
log.write_text(
    f"# 科研卡片工厂运行日志\n\n"
    f"创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    "今天我完成了：\n\n"
    "- [ ] 运行 Python 环境检查脚本\n"
    "- [ ] 创建科研卡片工厂工作区\n"
    "- [ ] 检查 input/ 里的原料表\n"
    "- [ ] 规划第一张学习卡片\n"
    "- [ ] 记录一个自己遇到的报错或疑问\n",
    encoding="utf-8",
)

print(f"科研卡片工厂工作区已创建：{base.resolve()}")
print("原料、卡片、成品和报告已经分仓入库。下一步，就可以让 Python 开始加工第一张卡片。")
