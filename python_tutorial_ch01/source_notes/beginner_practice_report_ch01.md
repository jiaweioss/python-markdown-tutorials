# 第 1 章初学者实操检测报告

检测日期：2026-06-19

## 检测目标

本次从初学者视角复跑第 1 章《Python 基础知识与工作环境》。目标不是证明“代码能在作者电脑上跑”，而是确认学生照着教程时，能一步步看清楚：

1. 当前站在哪个项目目录。
2. 正在使用哪个 Python 解释器。
3. pip 是否属于同一个 Python。
4. PowerShell 和 PyCharm 应该核对哪些证据。
5. 第一个脚本、环境检查脚本、通电日志和极简 Stroop 预告能否实际运行。

## 推荐实操路线

从 `python_tutorial_ch01` 目录运行：

```bash
python --version
python -m pip --version
python code/ch01/01_hello_python.py
python code/ch01/02_environment_check.py
python code/ch01/03_import_this.py
python code/ch01/04_show_me_the_python.py
python code/ch01/05_experiment_preview.py
python code/ch01/06_common_error_examples.py
```

其中 `05_experiment_preview.py` 会要求输入两次。本次检测使用：

```text
S001
j
```

## 运行结果

| 检测项 | 结果 |
| --- | --- |
| 6 个 ch01 示例脚本 | 全部运行通过 |
| `05_experiment_preview.py` 交互输入 | 使用 `S001` 和 `j` 跑通，能输出反应、正确性和粗略反应时 |
| 通电日志 | `reports/ch01_environment_log.txt` 已生成 |
| 视觉生成脚本 | `python scripts/generate_ch01_visuals.py` 运行通过 |
| Markdown 图片链接 | `python scripts/check_links.py` 通过，34 个本地图片引用 0 缺失 |
| Python 语法检查 | 6 个示例脚本 + 2 个工具脚本通过 `py_compile` |
| 图片完整性 | `assets/` 与 `reports/` 下 63 张 PNG/JPG/GIF 均可由 PIL 打开 |
| 图文顺序 | 34 张图前均有文字讲解、任务说明或过渡句 |

## 本轮修复记录

- 将第 1 张 Guido van Rossum 图片从标题后直接出现，移动到导语说明之后。
- 为执行策略备用运行、xkcd 梗图、Wundt 实验室、pip 管线、Python 环境梗图、报错地图等图片补充前置讲解。
- 修复 `scripts/generate_ch01_visuals.py` 的 PNG 保存方式，避免 `ch01_cover.png` 出现 PNG 校验不干净的问题。
- 重新生成第 1 章图片后，63 张 PNG/JPG/GIF 均通过 PIL 校验。

## 初学者最容易踩的坑

1. **目录不对**：脚本路径写对了，但 PowerShell 当前目录不在 `python_tutorial_ch01`，就会找不到文件。
2. **pip 送错地方**：直接写 `pip install` 可能装到另一个 Python，教程推荐 `python -m pip`。
3. **PowerShell 激活失败就慌**：执行策略拦住 `Activate.ps1` 时，可以直接调用 `.venv\Scripts\python.exe`。
4. **只看 PyCharm 绿色按钮**：按钮能点不等于配置正确，要看 Script path、Working directory 和解释器路径。
5. **看到报错就重装**：第一章强调先读报错最后一行，确认是路径、名字、模块还是缩进问题。

## 结论

第 1 章当前可以作为“小白环境通电章”使用：先用 PowerShell 拿到硬证据，再让 PyCharm 使用同一个解释器，最后用脚本输出、日志文件和运行截图证明环境真的跑通。图片顺序已经统一为先讲解再展示，适合学生按步骤操作和核对。
