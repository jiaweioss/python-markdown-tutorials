# 第0章来源记录

## 主来源

- Python 课程整体 PPT 与章节规划。
- 第0章现有 Markdown 教程正文：`chapters/ch00_course_start.md`。

本章内容依据课程总路线重构，重点包括：

1. AI 时代为什么仍需要学习 Python。
2. Python 课程不是语法背诵课，而是作品生产课。
3. 从第0章到第10章的课程总路线图。
4. 初学者需要先认识解释器、终端、IDE、项目目录。
5. 用环境体检脚本、科研卡片工厂工作区、工厂启动卡建立第一轮反馈。
6. 用报错地图和学习闭环降低初学者焦虑。
7. 用七张计算史与 Python 史照片讲清“程序、自动化、报错、工程、语言起源、机器步骤、运行环境”的入门心智，并分别穿插到对应知识点中。
8. 用图书馆卡片目录、实验笔记本、传送带三张真实场景照片建立“科研卡片工厂”的项目直觉。

## 参考来源

- MATLAB 教材仅作为课程组织方式参考：借鉴其“课程地图、工具环境、命令窗口、脚本和当前路径”的入门结构，不迁移 MATLAB 技术内容作为本章主题。
- MATLAB 教程的图文排版方式作为本章视觉重绘参考：图片尽量呈现截图、照片、结果图或简洁示意，解释文字放在 Markdown 正文中。
- xkcd 1205《Is It Worth the Time?》  
  <https://xkcd.com/1205/>
- xkcd 授权说明：CC BY-NC 2.5  
  <https://xkcd.com/license.html>
- Ada Lovelace portrait, Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Ada_Lovelace_portrait.jpg>
- Babbage difference engine, Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Babbages_difference_engine_1832.jpg>
- Guido van Rossum portrait, Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Guido_van_Rossum_(6984267183)_(cropped).jpg>
- Python 官方 FAQ：Why is it called Python?  
  <https://docs.python.org/3/faq/general.html#why-is-it-called-python>
- Jacquard loom cards, Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Jacquard_loom_cards.jpg>
- Two women operating ENIAC, Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Two_women_operating_ENIAC.gif>
- First Computer Bug, 1947, Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:First_Computer_Bug,_1947.jpg>
- Margaret Hamilton, NASA Science  
  <https://science.nasa.gov/people/margaret-hamilton/>
- Copyright Card Catalog Drawer, Wikimedia Commons, public domain  
  <https://commons.wikimedia.org/wiki/File:Copyright_Card_Catalog_Drawer.jpg>
- Lab Notebook.jpg, Wikimedia Commons, CC BY 4.0  
  <https://commons.wikimedia.org/wiki/File:Lab_Notebook.jpg>
- Belt-conveyor-handling2.jpg, Wikimedia Commons, public domain  
  <https://commons.wikimedia.org/wiki/File:Belt-conveyor-handling2.jpg>

## 生成素材

本章正式版图片已经统一重绘或整理，采用统一画布、留白和简洁构图。当前正文引用 19 张正式图片，并保留 11 张下载的互联网原图：

- `ch00_cover.png`
- `ch00_history_ada_lovelace_card.png`
- `ch00_history_babbage_difference_engine.png`
- `ch00_history_guido_van_rossum.png`
- `ch00_history_jacquard_card.png`
- `ch00_history_eniac_programmers.png`
- `ch00_history_first_bug_card.png`
- `ch00_history_apollo_software_card.png`
- `ch00_factory_card_catalog.png`
- `ch00_factory_lab_notebook.png`
- `ch00_factory_conveyor.png`
- `course_roadmap.png`
- `python_city_metaphor.png`
- `env_pipeline.png`
- `learning_loop.png`
- `learning_momentum_chart.png`
- `project_ladder.png`
- `error_map.png`
- `ch00_xkcd_automation_card.png`
- `tech_stack_workbench.png`
- `chapter_relay_station.png`
- `chapter_blueprint_bridge.png`
- `web/xkcd_1205_is_it_worth_the_time.png`
- `web/ada_lovelace_portrait.jpg`
- `web/babbage_difference_engine.jpg`
- `web/guido_van_rossum.jpg`
- `web/jacquard_loom_cards.jpg`
- `web/eniac_programmers.gif`
- `web/first_computer_bug_1947.jpg`
- `web/margaret_hamilton_apollo_code.jpg`
- `web/card_catalog_drawer.jpg`
- `web/lab_notebook.jpg`
- `web/belt_conveyor_handling.jpg`

这些图片用于辅助理解课程地图、科研卡片工厂、环境流水线、项目阶梯、学习闭环、学习反馈曲线、技术栈工作台、章节接力中继站、章节蓝图接力、报错地图、自动化投入产出，以及 Ada Lovelace、Babbage 差分机、Guido van Rossum、Jacquard 打孔卡、ENIAC、第一张著名 bug 照片、Apollo 软件工程等历史故事。历史照片、真实场景照片和漫画尽量只展示图像本体，解释文字放在 Markdown 正文中；正文也保留来源与授权说明。

正文中的 19 张图片均使用 `figure` 与 `figcaption` 组织图注，图注包含“图0-x”编号、短标题和一句说明。这样既能在 Markdown 中清晰显示图片标题，也避免把解释文字重新塞回图片内部。

2026-06-20 复验中，正文 19 张图片已统一为“先叙述，再图片和图注”。每张图前都保留课程场景、历史故事、任务说明或过渡句，图片只承担视觉锚点、历史照片、真实场景或成果示意的作用。

## 实操检测记录

- `source_notes/beginner_practice_report_ch00.md`：从初学者视角记录本章 4 个脚本的运行路线、`learning_passport.py` 的示例输入、关键产物、常见踩坑、图片顺序检查和 PIL 图片有效性检查。
- 2026-06-20 复验确认：`python scripts/generate_ch00_visuals.py`、`python scripts/check_links.py`、6 个 Python 文件 `py_compile`、33 张 PNG/JPG/GIF 的 PIL 打开检查均通过。
