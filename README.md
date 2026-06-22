# Python Markdown 教程书

这是一套面向初学者的 Python Markdown 教程工程，当前包含第 0 章到第 10 章的完整章节包、配图、示例代码、报告和来源记录。

已部署的网页阅读入口：

- <http://39.106.48.40/>

## 章节目录

| 章节 | 主题 | 正文入口 |
| --- | --- | --- |
| ch00 | 课程地图、入门仪式与学习方法 | [ch00_course_start.md](python_tutorial_ch00/chapters/ch00_course_start.md) |
| ch01 | Python 基础知识与工作环境 | [ch01_python_basics_work_env.md](python_tutorial_ch01/chapters/ch01_python_basics_work_env.md) |
| ch02 | Python 编程基础：数据类型 | [ch02_python_data_types.md](python_tutorial_ch02/chapters/ch02_python_data_types.md) |
| ch03 | 文件读写与文件夹管理 | [ch03_file_io_folder_management.md](python_tutorial_ch03/chapters/ch03_file_io_folder_management.md) |
| ch04 | Tkinter 图形界面编程 | [ch04_tkinter_gui.md](python_tutorial_ch04/chapters/ch04_tkinter_gui.md) |
| ch05 | 面向对象程序设计 | [ch05_oop.md](python_tutorial_ch05/chapters/ch05_oop.md) |
| ch06 | 数据分析与可视化 | [ch06_data_analysis_visualization.md](python_tutorial_ch06/chapters/ch06_data_analysis_visualization.md) |
| ch07 | PyGame 游戏开发 | [ch07_pygame_game.md](python_tutorial_ch07/chapters/ch07_pygame_game.md) |
| ch08 | 网络爬虫开发实战 | [ch08_web_scraping.md](python_tutorial_ch08/chapters/ch08_web_scraping.md) |
| ch09 | Python 图像处理 | [ch09_image_processing.md](python_tutorial_ch09/chapters/ch09_image_processing.md) |
| ch10 | Python 办公自动化 | [ch10_office_automation.md](python_tutorial_ch10/chapters/ch10_office_automation.md) |

## 网页站点

站点生成器位于 [website/build_site.py](website/build_site.py)。它会把 ch00-ch10 的 Markdown 自动渲染成静态 HTML，并生成首页、章节导航、页内目录、配套文件入口和阅读交互。

当前网页体验包含：

- 首页章节搜索和结果计数。
- 桌面端左侧课程目录、右侧页内目录。
- 移动端课程目录抽屉。
- 阅读进度条和回到顶部按钮。
- 代码块一键复制。
- 章节图片点击放大预览。
- 明暗主题切换。

本地构建：

```bash
python -m pip install -r website/requirements.txt
python website/build_site.py
python -m http.server 8124 --directory public
```

`public/` 是生成产物，默认不纳入 Git 管理。

## 质量记录

每章保留：

- `source_notes/source_manifest_*.md`：外部素材与生成素材来源。
- `source_notes/quality_audit_*.md`：章节验收和修订记录。
- `scripts/check_links.py`：检查本章 Markdown 图片链接。
- `scripts/generate_chXX_visuals.py`：生成或整理本章正式图片。

## GitHub 协作

仓库协作、分支建议和发布检查见 [GITHUB_MANAGEMENT.md](GITHUB_MANAGEMENT.md)。

