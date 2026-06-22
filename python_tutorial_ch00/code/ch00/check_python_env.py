"""
check_python_env.py
第0章配套脚本：检查 Python 是否能正常运行。
运行方式：python check_python_env.py
"""
from pathlib import Path
import sys
import platform
import math

print("=" * 60)
print("Python 环境体检报告")
print("=" * 60)
print(f"Python 版本      : {sys.version.split()[0]}")
print(f"Python 可执行文件: {sys.executable}")
print(f"操作系统          : {platform.system()} {platform.release()}")
print(f"当前工作目录      : {Path.cwd()}")
print(f"圆周率 math.pi    : {math.pi}")

try:
    import tkinter  # noqa: F401
    print("Tkinter           : 可用，后面可以做 GUI 小窗口")
except Exception as exc:
    print(f"Tkinter           : 暂不可用，原因：{exc}")

print("=" * 60)
print("如果你看到了这份报告，说明：Python 至少已经能跑起来。")
print("恭喜，你已经把新手村大门推开了一条缝。")
