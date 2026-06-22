"""Check whether pygame is available."""
try:
    import pygame
except ImportError:
    print("未安装 pygame。可运行：python -m pip install pygame")
else:
    print("pygame 版本：", pygame.version.ver)
