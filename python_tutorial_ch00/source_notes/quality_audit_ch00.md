# 第0章质量验收记录

验收日期：2026-06-20

## 验收范围

本次验收范围是 `python_tutorial_ch00` 包，重点包括：

- `chapters/ch00_course_start.md`
- `assets/ch00/`
- `assets/ch00/web/`
- `scripts/generate_ch00_visuals.py`
- `scripts/check_links.py`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch00.md`
- `source_notes/beginner_practice_report_ch00.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 优化教程入口文字 | 正文保留课程地图、AI 时代学习意义、项目路线、学习闭环和课程蓝图，并将自动化投入产出故事、七个计算史/Python 史故事、科研卡片工厂真实场景故事穿插到对应知识点中 | 已完成 |
| 统一学生视角 | 删除正文和图片中的备课视角表达，改为直接面向学习者的说明 | 已完成 |
| 增加故事和互联网梗图 | 下载 xkcd 1205、Ada Lovelace、Babbage 差分机、Guido van Rossum、Jacquard 打孔卡、ENIAC、第一张著名 bug 照片、Margaret Hamilton/Apollo 软件照片，以及图书馆卡片目录、实验笔记本、传送带三张真实场景照片，并以原图展示为主 | 已完成 |
| 图片正式、漂亮、可学习 | 正文 19 张图片均由脚本统一整理，历史照片、真实场景照片和漫画只展示图像本体，解释文字放回 Markdown 正文 | 已完成 |
| 图片图注清晰 | 正文 19 张图片均使用 `figure/figcaption` 添加“图0-x + 标题 + 一句说明”，图注位于图片下方 | 已完成 |
| 图片居中显示 | 正文 19 张图片均使用 `figure align="center"`，并在图片样式中加入 `display:block; margin:0 auto;` | 已完成 |
| 图文顺序统一 | 19 张图前均有正文讲解、任务说明或过渡句，统一为“先叙述，再图片和图注” | 已完成 |
| 章节蓝图更有节奏 | 新增 `chapter_relay_station.png`，放在第4章和第5章蓝图之间，把后半段最长无图间隔从 208 行降到 188 行 | 已完成 |
| 图片内不写解释文字 | 生成脚本已移除文字绘制逻辑，示意图改为符号、路径、曲线和色块表达，说明文字全部放在正文图片下方 | 已完成 |
| 修复图片越界 | 重绘 `error_map.png` 与 `learning_loop.png` 的内部符号，移除会超出彩色容器的小图标，改为稳定几何符号 | 已完成 |
| 修复远程/不稳定图片 | 删除正文中的远程知乎图片引用，改为本地正式图 | 已完成 |
| 图片引用不缺失 | `python scripts/check_links.py` 检查通过 | 已完成 |
| 代码与脚本可检查 | `py_compile` 检查通过，覆盖 4 个示例脚本和 2 个工具脚本 | 已完成 |
| 初学者实操报告 | `source_notes/beginner_practice_report_ch00.md` 记录运行路线、交互输入、关键产物、常见踩坑和复验结果 | 已完成 |
| 图片可打开 | PIL 已打开验证 `assets/`、`output/`、`python_card_factory/` 下 33 张 PNG/JPG/GIF 图片 | 已完成 |
| 脚本实跑 | 4 个示例脚本均在 `python_tutorial_ch00` 根目录运行通过，`learning_passport.py` 使用示例输入生成启动卡 | 已完成 |
| 来源和授权可追溯 | 正文、source manifest 与 manifest 均记录 xkcd、Wikimedia Commons 与 NASA Science 来源 | 已完成 |

## 当前素材清单

正式图片：

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

下载的互联网原图：

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

## 外部来源

- xkcd 1205：<https://xkcd.com/1205/>
- xkcd 授权说明：<https://xkcd.com/license.html>
- Ada Lovelace portrait：<https://commons.wikimedia.org/wiki/File:Ada_Lovelace_portrait.jpg>
- Babbage difference engine：<https://commons.wikimedia.org/wiki/File:Babbages_difference_engine_1832.jpg>
- Guido van Rossum portrait：<https://commons.wikimedia.org/wiki/File:Guido_van_Rossum_(6984267183)_(cropped).jpg>
- Python 官方 FAQ：<https://docs.python.org/3/faq/general.html#why-is-it-called-python>
- Jacquard loom cards：<https://commons.wikimedia.org/wiki/File:Jacquard_loom_cards.jpg>
- Two women operating ENIAC：<https://commons.wikimedia.org/wiki/File:Two_women_operating_ENIAC.gif>
- First Computer Bug, 1947：<https://commons.wikimedia.org/wiki/File:First_Computer_Bug,_1947.jpg>
- Margaret Hamilton, NASA Science：<https://science.nasa.gov/people/margaret-hamilton/>
- Copyright Card Catalog Drawer：<https://commons.wikimedia.org/wiki/File:Copyright_Card_Catalog_Drawer.jpg>
- Lab Notebook.jpg：<https://commons.wikimedia.org/wiki/File:Lab_Notebook.jpg>
- Belt-conveyor-handling2.jpg：<https://commons.wikimedia.org/wiki/File:Belt-conveyor-handling2.jpg>

## 验收命令

在 `python_tutorial_ch00` 目录下运行：

```bash
python scripts/check_links.py
@'
import ast
from pathlib import Path
files = [
    Path('code/ch00/check_python_env.py'),
    Path('code/ch00/create_learning_base.py'),
    Path('code/ch00/learning_passport.py'),
    Path('code/ch00/print_course_map.py'),
    Path('scripts/generate_ch00_visuals.py'),
    Path('scripts/check_links.py'),
]
for p in files:
    ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
print('AST syntax OK:', len(files))
'@ | python -
```

当前结果：

- Markdown 与 HTML 本地图片链接：通过，`scripts/check_links.py` 检查 9 个 Markdown 文件
- Python `py_compile` 语法检查：通过，覆盖 6 个 `.py` 文件
- `check_python_env.py`、`print_course_map.py`、`create_learning_base.py`、`learning_passport.py` 运行测试：通过
- `learning_passport.py` 交互输入：通过，示例输入为“小白学生 / 整理课堂笔记 / 课堂笔记和文献摘录 / 4”
- 正文图片引用数：19
- 正文 `figure` 数：19
- 正文 `figcaption` 数：19
- manifest 素材数：33
- 互联网来源数：13
- PIL 图片打开检查：通过，33 张 PNG/JPG/GIF 均可打开
- 图文顺序扫描：通过，19 张图前均有正文讲解、任务说明或过渡句
- 临时总览图人工检查：通过，19 张正式图无空白、明显错位或越界；检查图已删除
- ch00 当前一致性扫描：19 个 figure、19 个 img、19 个 figcaption、19 个本地图片引用，0 个缺失本地图片链接，0 个 PIL 错误，0 个图文顺序问题。

## 剩余边界

本次验收证明 `ch00` 已按当前图文标准完成入口章节优化。当前第4章到第10章的章节包也已创建；后续若继续精修，可逐章增加更多真实场景图片、软件截图和课堂案例。
