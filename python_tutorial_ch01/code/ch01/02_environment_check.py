"""Check the local Python environment.

Run:
    python 02_environment_check.py
"""

import platform
import sys
from pathlib import Path

print("=" * 60)
print("Python 环境检查")
print("=" * 60)
print("Python 版本：", sys.version)
print("Python 可执行文件：", sys.executable)
print("操作系统：", platform.platform())
print("当前工作目录：", Path.cwd())
print("\n当前目录下的文件和文件夹：")
for item in Path.cwd().iterdir():
    print(" -", item.name)
print("\n环境检查完成：如果你能看到这些信息，说明 Python 已经成功运行。")
