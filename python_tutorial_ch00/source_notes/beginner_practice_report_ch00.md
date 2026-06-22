# 第0章初学者实操检测报告

检测日期：2026-06-20

## 检测目标

本次从初学者视角复跑第0章《课程地图、入门仪式与学习方法》。第0章不是语法章，而是“把新手带进门”的启动章，所以检测重点是：

1. 学生能不能先确认 Python 已经能运行。
2. 学生能不能看懂课程地图。
3. 学生能不能创建一个干净的科研卡片工厂工作区。
4. 学生能不能生成一张属于自己的工厂启动卡。
5. 图片是否按“先叙述，再图片和图注”的顺序出现，不让读者还没理解就先被图砸中。

## 推荐实操路线

从 `python_tutorial_ch00` 目录运行：

```bash
python code/ch00/check_python_env.py
python code/ch00/print_course_map.py
python code/ch00/create_learning_base.py
python code/ch00/learning_passport.py
```

其中 `learning_passport.py` 会要求输入四次。本次检测使用：

```text
小白学生
整理课堂笔记
课堂笔记和文献摘录
4
```

## 运行结果

| 检测项 | 结果 |
| --- | --- |
| `check_python_env.py` | 运行通过，能显示 Python 版本、解释器路径、操作系统、当前目录、`math.pi` 和 Tkinter 状态 |
| `print_course_map.py` | 运行通过，能打印 ch00 到 ch10 的课程地图 |
| `create_learning_base.py` | 运行通过，生成 `python_card_factory/` 工作区 |
| `learning_passport.py` | 使用示例输入运行通过，生成 `output/factory_start_card.md` |
| 视觉生成脚本 | `python scripts/generate_ch00_visuals.py` 运行通过 |
| Markdown 图片链接 | `python scripts/check_links.py` 通过，8 个 Markdown 文件中本地图片链接均存在 |
| Python 语法检查 | 4 个示例脚本 + 2 个工具脚本通过 `py_compile` |
| 图片完整性 | `assets/`、`output/`、`python_card_factory/` 下 33 张 PNG/JPG/GIF 均可由 PIL 打开 |
| 图文顺序 | 19 张图前均有文字讲解、任务说明或过渡句 |
| 临时总览图 | 已人工检查 19 张正式图，无空白、明显错位或越界；检查后已删除临时图 |

## 学生能看到的关键产物

- `python_card_factory/README.md`：自动生成的科研卡片工厂说明。
- `python_card_factory/input/source_materials.csv`：第一批示例原料表。
- `python_card_factory/reports/factory_log.md`：工厂运行日志。
- `output/factory_start_card.md`：交互脚本生成的个人启动卡。

## 本轮修复记录

- 为图0-6、图0-9、图0-11 增加前置讲解，避免二级/三级标题后直接贴图。
- 重新扫描正文 19 张图片，确认每张图前都有叙述、任务铺垫或过渡句。
- 从用户视角实际运行第0章 4 个脚本，确认启动章的“环境体检、课程地图、工作区、启动卡”闭环可用。
- 生成并人工检查临时图片总览图，确认没有空白、错位、越界或旧文字卡片残留。

## 初学者最容易踩的坑

1. **站错目录**：第0章脚本建议在 `python_tutorial_ch00` 根目录运行，否则生成的 `output/` 和 `python_card_factory/` 会跑到别的地方。
2. **看到交互输入就卡住**：`learning_passport.py` 不是报错，而是在等你输入名字、目标、材料类型和每周学习时间。
3. **误把工作区当教程源码**：`python_card_factory/` 是脚本生成的练习工作区，`chapters/` 和 `code/` 才是教程本体。
4. **只读不运行**：第0章的重点不是“看懂课程介绍”，而是亲手让 Python 生成一个可见的目录和一张启动卡。

## 结论

第0章当前已经具备“小白启动章”的基本闭环：先用环境体检确认 Python 能跑，再用课程地图建立方向感，接着创建科研卡片工厂工作区，最后生成个人启动卡。图片顺序已经统一为先讲解再展示，适合学生按教程一步步操作。
