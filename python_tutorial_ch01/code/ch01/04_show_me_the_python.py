"""A tiny Chapter 1 project: power on the research card factory.

This script prints basic environment information and writes an environment log.
"""

from pathlib import Path
import datetime
import sys

print("=" * 60)
print("科研卡片工厂通电检查")
print("=" * 60)

print("当前 Python：", sys.executable)
print("当前目录：", Path.cwd())

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

log_file = report_dir / "ch01_environment_log.txt"
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

content = f"""科研卡片工厂通电日志
时间：{now}
状态：第一章环境测试成功
当前 Python：{sys.executable}
当前工作目录：{Path.cwd()}

提醒：
解释器、项目目录和输出位置要对齐，工厂才不会把材料送错仓库。
"""

log_file.write_text(content, encoding="utf-8")

print("学习日志已生成：", log_file)
print("恭喜，科研卡片工厂已经通电。")
