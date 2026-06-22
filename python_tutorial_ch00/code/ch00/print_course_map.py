"""
print_course_map.py
打印课程地图。这个脚本用列表和字典存储课程安排，后面第2章会详细讲。
"""
chapters = [
    {"id": 0, "title": "课程地图与入门仪式", "project": "启动科研卡片工厂"},
    {"id": 1, "title": "Python基础与工作环境", "project": "跑通第一个脚本"},
    {"id": 2, "title": "数据类型与变量", "project": "设计学习卡片字段"},
    {"id": 3, "title": "文件读写与文件夹管理", "project": "整理原料文件夹"},
    {"id": 4, "title": "Tkinter图形界面", "project": "情绪评分小窗口"},
    {"id": 5, "title": "面向对象程序设计", "project": "封装卡片对象"},
    {"id": 6, "title": "数据分析与可视化", "project": "卡片统计图表"},
    {"id": 7, "title": "PyGame游戏开发", "project": "复习小游戏"},
    {"id": 8, "title": "网络爬虫", "project": "公开资料采集器"},
    {"id": 9, "title": "图像处理", "project": "卡片配图处理"},
    {"id": 10, "title": "办公自动化", "project": "导出Word/PPT报告"},
]

print("Python科研卡片工厂课程地图")
print("-" * 48)
for chapter in chapters:
    print(f"Ch{chapter['id']:02d} | {chapter['title']:<18} | {chapter['project']}")
