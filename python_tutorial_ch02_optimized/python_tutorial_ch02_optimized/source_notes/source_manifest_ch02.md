# 第2章来源记录

## 主来源

- `第二章_Python编程基础_数据类型2025.pptx`

本章内容依据原课件的课程主线重构，重点吸收以下内容：

1. Python 内置常量与关键字。
2. 变量定义方式，以及 Python 与 C / Java 等语言在变量声明上的差异。
3. 变量“盒子模型”和 Python 引用/标签模型的区别。
4. Python 常见数据类型：布尔、数值、字符串、列表、字典等。
5. 布尔逻辑中的 `and`、`or`、`not`。
6. 数值类型与 `round()`、`math.ceil()`、`math.floor()`。
7. 字符串创建、类型转换、拼接、查找、替换、切片和切割。
8. 列表索引、切片、嵌套、合并、追加、删除和乘法。
9. 字典定义、查询、增添、删除和 value 替换。

## 参考来源

- MATLAB 基础语法与矩阵操作资料仅作为教学组织方式参考：借鉴其“先介绍数据材料，再介绍操作方法，再进入小案例”的讲法。
- MATLAB 文件与数据处理资料仅作为任务驱动风格参考，没有迁移 MATLAB 技术内容作为本章主题。

## 互联网图片来源

本章互联网图片全部先保存到 `assets/ch02/web/`，再由 `scripts/generate_ch02_visuals.py` 整理成正式教材图。图片内部不新增解释文字，说明放在 Markdown 正文和图注中。

| 用途 | 原图 | 本地原图 | 正式图片 | 来源与授权记录 |
| --- | --- | --- | --- | --- |
| 信息表示与编码故事 | Claude Shannon 肖像 | `assets/ch02/web/claude_shannon_mfo3807.jpg` | `assets/ch02/ch02_information_history_claude_shannon.png` | Wikimedia Commons：`File:ClaudeShannon MFO3807.jpg`，Konrad Jacobs / MFO，CC BY-SA 2.0 de |
| 布尔逻辑历史故事 | George Boole 肖像 | `assets/ch02/web/george_boole_color.jpg` | `assets/ch02/ch02_history_george_boole.png` | Wikimedia Commons：`File:George Boole color.jpg`，页面标记为 Public domain / Public Domain Mark |
| 心理学记忆数据故事 | Hermann Ebbinghaus 肖像 | `assets/ch02/web/hermann_ebbinghaus2.jpg` | `assets/ch02/ch02_psychology_ebbinghaus_memory.png` | Wikimedia Commons：`File:Ebbinghaus2.jpg`，页面标记为 Public domain / Public Domain Mark |
| 嵌套列表类比 | Matryoshka dolls | `assets/ch02/web/matryoshka_dolls.jpg` | `assets/ch02/ch02_nested_data_matryoshka.png` | Wikimedia Commons：`File:Matryoshka dolls.jpg`，Wayiran，Public domain |
| 字典检索类比 | Copyright Card Catalog Drawer | `assets/ch02/web/copyright_card_catalog_drawer.jpg` | `assets/ch02/ch02_dictionary_card_catalog_photo.png` | Wikimedia Commons：`File:Copyright Card Catalog Drawer.jpg`，作者 Michael Holley / Swtpc6800，页面标记为 Public domain / copyright holder release |
| 批量数据分拣故事 | IBM 080 Card Sorter | `assets/ch02/web/ibm_080_card_sorter.jpg` | `assets/ch02/ch02_punch_card_sorter_photo.png` | Wikimedia Commons：`File:IBM 080 Card Sorter.jpg`，作者 Pargon，CC BY 2.0 |

原始链接：

- https://commons.wikimedia.org/wiki/File:ClaudeShannon_MFO3807.jpg
- https://commons.wikimedia.org/wiki/File:George_Boole_color.jpg
- https://commons.wikimedia.org/wiki/File:Ebbinghaus2.jpg
- https://commons.wikimedia.org/wiki/File:Matryoshka_dolls.jpg
- https://commons.wikimedia.org/wiki/File:Copyright_Card_Catalog_Drawer.jpg
- https://commons.wikimedia.org/wiki/File:IBM_080_Card_Sorter.jpg

## 真实运行与脚本生成素材

- `assets/ch02/web/powershell_ch02_data_types_run.png`：本地 PowerShell 真实窗口截图，运行 `python code/ch02/02_variables_labels.py`、`python code/ch02/06_learning_record_project.py` 和快速 `type()` 检查。
- `assets/ch02/ch02_powershell_data_type_run.png`：由生成脚本整理后的正式教材图。
- `output/ch02_type_decision_cards_preview.png`：由 `python code/ch02/07_make_type_decision_cards.py` 生成的类型选择卡片预览。
- `assets/ch02/web/ch02_type_decision_cards_preview.png`：类型选择卡片预览的本地整理源。
- `output/ch02_type_compass_preview.png`：由 `python code/ch02/08_make_type_compass.py` 生成的类型选择罗盘预览。
- `assets/ch02/web/ch02_type_compass_preview.png`：类型选择罗盘预览的本地整理源。
- `output/ch02_data_type_lab_receipt.png`：由 `python code/ch02/09_make_data_type_lab_receipt.py` 生成的数据类型实验回执预览。
- `assets/ch02/web/ch02_data_type_lab_receipt.png`：数据类型实验回执预览的本地整理源。
- `output/ch02_stroop_dataset_pack.png`：由 `python code/ch02/10_make_stroop_dataset_pack.py` 生成的 Stroop 数据类型包预览。
- `assets/ch02/web/ch02_stroop_dataset_pack.png`：Stroop 数据类型包预览的本地整理源。
- `output/ch02_stroop_dataset_pack.json`：Stroop trial 数据包，保存汇总信息和多条 trial 记录。
- `output/ch02_stroop_dataset_pack.csv`：Stroop trial 表格数据，便于后续数据分析章节读取。
- `output/ch02_data_type_specimen_cabinet.png`：由 `python code/ch02/11_make_data_type_specimen_cabinet.py` 生成的数据类型标本柜预览。
- `output/ch02_data_type_specimen_cabinet.json`：数据类型标本柜的结构化摘要。
- `assets/ch02/web/ch02_data_type_specimen_cabinet.png`：数据类型标本柜预览的本地整理源。
- `output/ch02_data_type_runtime_evidence.png`：由 `python code/ch02/12_make_data_type_runtime_evidence.py` 生成的数据类型运行证据图，检查本章 14 个关键产物。
- `assets/ch02/web/ch02_data_type_runtime_evidence.png`：数据类型运行证据图的本地整理源。
- `reports/ch02_type_decision_cards.md`：类型选择卡片 Markdown 报告。
- `reports/ch02_type_compass.md`：类型选择罗盘 Markdown 报告。
- `reports/ch02_data_type_lab_receipt.md`：数据类型实验回执 Markdown 报告。
- `reports/ch02_stroop_dataset_pack.md`：Stroop 数据类型包 Markdown 报告。
- `reports/ch02_data_type_specimen_cabinet.md`：数据类型标本柜 Markdown 报告。
- `reports/ch02_data_type_runtime_evidence.md`：数据类型运行证据 Markdown 报告。

## 生成素材

本章正式版图片采用 1800px 宽画布、统一字体、留白、色彩和图文外框构图。当前包含 27 张正文配图。本轮重新生成变量标签、路线图、数据类型地图、布尔逻辑、字符串切片、列表、字典和小项目等核心概念图，减少图内长解释文字；并在数字到字符串之间新增 `ch02_string_material_workbench.png`，把实验说明、被试编号、刺激词、文件路径和日志备注这些真实文本材料接到字符串知识点上；尾部继续保留报错线索卡、练习工作台与数据类型到文件管理的过渡图，让复盘、练习和下一章预告不再长时间无图。故事、比喻、判断理由和操作步骤统一放在 Markdown 正文与图注中。

- `ch02_cover.png`
- `ch02_roadmap.png`
- `ch02_variable_label_metaphor.png`
- `ch02_powershell_data_type_run.png`
- `ch02_data_type_runtime_evidence.png`
- `ch02_data_type_atlas.png`
- `ch02_information_history_claude_shannon.png`
- `ch02_type_compass_preview.png`
- `ch02_history_george_boole.png`
- `ch02_bool_logic_switchboard.png`
- `ch02_number_rounding_chart.png`
- `ch02_string_material_workbench.png`
- `ch02_string_slice_ruler.png`
- `ch02_psychology_ebbinghaus_memory.png`
- `ch02_list_workbench.png`
- `ch02_punch_card_sorter_photo.png`
- `ch02_practice_workbench.png`
- `ch02_nested_data_matryoshka.png`
- `ch02_dictionary_card_catalog_photo.png`
- `ch02_dict_mapping_card.png`
- `ch02_mini_project_dashboard.png`
- `ch02_data_type_lab_receipt.png`
- `ch02_stroop_dataset_pack.png`
- `ch02_data_type_specimen_cabinet.png`
- `ch02_type_decision_cards_preview.png`
- `ch02_error_clue_cards.png`
- `ch02_type_to_file_bridge.png`

这些图片用于解释变量标签模型、真实运行证据、数据类型选择、类型选择罗盘、布尔逻辑、数值取整、字符串材料、字符串切片、列表操作、早期打孔卡分拣、嵌套结构、字典映射、本章综合项目、数据类型实验回执、Stroop 数据类型包、数据类型标本柜、常见报错线索、练习任务收束和下一章文件管理衔接。正式 Markdown 只引用本地整理图，无远程图片依赖。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 图片本体使用 `<img ... style="zoom:50%; display:block; margin:0 auto;" />` 居中显示。
- 每张图片下方都有 `<figcaption>` 图注，图注负责标题、情境说明和学习提示。
- 生成图尽量少放解释性文字；故事、比喻和操作说明放在 Markdown 正文中。
