# 第2章小白实操检测报告

检测日期：2026-06-18

## 检测目标

本报告按初学者第一次跟做第2章的方式检查：能否从章节根目录进入、按顺序运行脚本、看懂每一步输出、找到生成文件，并最终确认本章 14 个关键产物全部 ready。

第2章不是要求学生背完所有类型方法，而是确认一条实践路线能跑通：

1. 先认识常量、关键字、变量标签、布尔、数值、字符串、列表和字典。
2. 再运行配套脚本，看见每种类型在终端里的真实输出。
3. 最后生成学习记录、类型选择工具、Stroop 数据包、类型标本柜和运行证据。

## 操作环境

| 项目 | 检测结果 |
| --- | --- |
| 当前目录 | `python_tutorial_ch02` |
| Python | 本机 `python` 命令可用 |
| 依赖 | 第2章脚本只使用标准库，不需要额外安装第三方包 |
| 图片生成 | `python scripts/generate_ch02_visuals.py` 已成功运行 |
| 链接检查 | `python scripts/check_links.py` 已通过 |

## 学生跟做路线

第一步，进入第2章目录：

```powershell
cd C:\Users\你的用户名\Desktop\Python教程\PythonMarkdown教程书\python_tutorial_ch02
```

如果命令提示路径不存在，先检查桌面文件夹名字是否和本机一致。初学者最容易在这里卡住：不是 Python 错了，而是当前目录不对。

第二步，从最小脚本开始运行：

```powershell
python code\ch02\01_constants_keywords.py
python code\ch02\02_variables_labels.py
python code\ch02\03_bool_numbers.py
python code\ch02\04_string_playground.py
python code\ch02\05_list_dict_workshop.py
python code\ch02\06_learning_record_project.py
```

这 6 个脚本负责建立基本手感。学生应该能看到常量、关键字、变量 `id()`、布尔判断、取整、字符串切片、列表和字典的输出。

第三步，运行项目成果脚本：

```powershell
python code\ch02\07_make_type_decision_cards.py
python code\ch02\08_make_type_compass.py
python code\ch02\09_make_data_type_lab_receipt.py
python code\ch02\10_make_stroop_dataset_pack.py
python code\ch02\11_make_data_type_specimen_cabinet.py
python code\ch02\12_make_data_type_runtime_evidence.py
```

这 6 个脚本会把“数据类型知识”变成可检查的文件。最后一个脚本应输出：

```text
ch02 runtime evidence: 14/14 ready
```

如果不是 `14/14 ready`，不要重装 Python。先看报告里哪一项是 `MISSING`，回到对应脚本补跑一次。

## 本次实操结果

| 步骤 | 命令或脚本 | 观察结果 | 状态 |
| --- | --- | --- | --- |
| 1 | `01_constants_keywords.py` | 打印 `True`、`False`、`None`、`math.pi` 和关键字数量 | 通过 |
| 2 | `02_variables_labels.py` | `a` 和 `b` 先指向同一对象，`b = 3` 后指向不同对象 | 通过 |
| 3 | `03_bool_numbers.py` | 打印 `and`、`or`、`not` 结果，并展示 `round/floor/ceil` 差异 | 通过 |
| 4 | `04_string_playground.py` | 展示字符串拼接、大小写、替换、索引、切片和 `split()` | 通过 |
| 5 | `05_list_dict_workshop.py` | 展示列表取值、切片、追加、删除，以及字典增删改查 | 通过 |
| 6 | `06_learning_record_project.py` | 生成 `output/ch02_learning_report.txt` | 通过 |
| 7 | `07_make_type_decision_cards.py` | 生成类型选择卡片 Markdown 和预览图 | 通过 |
| 8 | `08_make_type_compass.py` | 生成类型选择罗盘 Markdown 和预览图 | 通过 |
| 9 | `09_make_data_type_lab_receipt.py` | 生成数据类型实验回执 Markdown 和 PNG | 通过 |
| 10 | `10_make_stroop_dataset_pack.py` | 生成 JSON、CSV、Markdown 和 PNG 数据包 | 通过 |
| 11 | `11_make_data_type_specimen_cabinet.py` | 生成类型标本柜 JSON、Markdown 和 PNG | 通过 |
| 12 | `12_make_data_type_runtime_evidence.py` | 检查 14 个关键产物，输出 `14/14 ready` | 通过 |

## 关键产物检查

本次实操确认以下文件已经生成：

```text
output/ch02_learning_report.txt
reports/ch02_type_decision_cards.md
output/ch02_type_decision_cards_preview.png
reports/ch02_type_compass.md
output/ch02_type_compass_preview.png
reports/ch02_data_type_lab_receipt.md
output/ch02_data_type_lab_receipt.png
output/ch02_stroop_dataset_pack.json
output/ch02_stroop_dataset_pack.csv
reports/ch02_stroop_dataset_pack.md
output/ch02_stroop_dataset_pack.png
reports/ch02_data_type_specimen_cabinet.md
output/ch02_data_type_specimen_cabinet.json
output/ch02_data_type_specimen_cabinet.png
```

这些文件构成第2章的“实操证据链”。学生不只是看懂 `str/list/dict/bool/float/None`，而是能看到这些类型如何合在一起生成学习记录和心理学数据包。

## 小白风险点

| 风险点 | 表现 | 建议 |
| --- | --- | --- |
| 当前目录不对 | 提示找不到 `code\ch02\...` | 先运行 `Get-Location`，确认在 `python_tutorial_ch02` |
| 把命令复制到 Python 交互窗口 | 出现 `SyntaxError` | `python code\...` 要在 PowerShell 里运行，不是在 `>>>` 后面运行 |
| 生成文件找不到 | 以为脚本没有结果 | 按正文给出的 `output/` 和 `reports/` 路径找 |
| `14/14 ready` 不出现 | 运行证据报告出现 `MISSING` | 根据缺失文件名补跑对应脚本 |
| 中文显示异常 | 终端编码不稳定 | 优先使用 Windows Terminal / PowerShell，并确认脚本本身保存为 UTF-8 |

## 阅读体验检查

本轮已按 ch01 标准调整正文顺序：先叙述任务、故事、操作或判断理由，再展示对应图片和图注。重点修正了封面、路线图、变量标签、真实运行图、数据类型地图、Shannon、Boole、取整、字符串、切片、列表、字典、小项目、报错地图和练习工作台等位置。

当前正文共有 27 张图片，27 个图注，图片均使用居中 `<figure>` 结构。检查结果显示，本地图片链接无缺失。

## 结论

第2章可以按小白实操路线顺利完成。学生只要站在正确目录，按正文顺序运行脚本，就能从“认识数据类型”走到“生成可复盘的数据类型成果包”。本章当前最重要的通过证据是：`12_make_data_type_runtime_evidence.py` 输出 `14/14 ready`。
