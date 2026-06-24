# Python Markdown 教程书：第2章详细版

本包是第2章《Python 编程基础：数据类型》的 Markdown 教材包。

## 内容

- `chapters/ch02_python_data_types.md`：第2章 Markdown 教材正文
- `assets/ch02/`：第2章正式版配图素材，含统一版式学习图、互联网历史照片和真实 PowerShell 运行截图
- `code/ch02/`：第2章可运行 Python 示例代码
- `source_notes/source_manifest_ch02.md`：来源线索记录
- `source_notes/quality_audit_ch02.md`：第2章质量检查记录
- `scripts/check_links.py`：Markdown 图片链接检查脚本
- `scripts/generate_ch02_visuals.py`：第2章正式版图片生成脚本
- `manifest.json`：文件清单

## 本轮优化重点

- 基于 `第二章_Python编程基础_数据类型2025.pptx` 的 58 页课件，重构为适合初学者阅读和学习分享的 Markdown 教程。
- 正文扩展为 27 张正式配图，覆盖变量标签模型、真实运行记录、数据类型地图、类型选择罗盘、信息论历史、布尔逻辑、数值取整、字符串材料工作台、字符串切片、IBM 打孔卡分拣机、列表嵌套、字典、本章小项目、数据类型实验记录、Stroop 数据类型包、数据类型标本柜、报错线索卡、练习工作台和下一章文件管理过渡图。
- 重新生成变量标签、路线图、数据类型地图、布尔逻辑、字符串切片、列表、字典和小项目等核心概念图，减少图片里的长解释文字，把故事、操作说明和判断理由放回 Markdown 正文与图注。
- 新增 Claude Shannon 肖像、George Boole 肖像、Hermann Ebbinghaus 肖像、图书馆卡片目录照片、IBM 080 打孔卡分拣机照片和套娃照片，让数据类型、布尔值、列表、字典和批量数据整理的讲解更有历史感和画面感。
- 新增真实 PowerShell 运行截图，展示 `02_variables_labels.py` 和 `06_learning_record_project.py` 的实际运行效果。
- 新增 `ch02_number_rounding_chart.png`，用 Python 生成的图表解释 `round`、`floor`、`ceil` 的区别。
- 新增 `ch02_string_material_workbench.png`，在数字和字符串之间补入无解释文字的“文字材料工作台”，把被试编号、刺激词、路径和日志备注这些真实文本材料接到字符串知识点上。
- 新增 12 个示例脚本，让常量、变量、布尔、数值、字符串、列表、字典、类型选择卡片、类型选择罗盘、数据类型实验记录、Stroop 数据包、数据类型标本柜和本章运行记录总览都能现场运行。
- 新增 `08_make_type_compass.py`，生成 `reports/ch02_type_compass.md` 和 `output/ch02_type_compass_preview.png`，把“看到数据先选类型”落成可复习的小工具。
- 新增 `09_make_data_type_lab_receipt.py`，生成 `reports/ch02_data_type_lab_receipt.md` 和 `output/ch02_data_type_lab_receipt.png`，把学习记录和心理学 trial 做成可视化记录。
- 新增 `10_make_stroop_dataset_pack.py`，生成 JSON、CSV、Markdown 和 PNG，把 ch1 的 Stroop 任务延伸成 `list[dict]` 数据包，让 `str`、`int`、`float`、`bool`、`None`、`dict` 和 `list` 在真实小任务里一起工作。
- 新增 `11_make_data_type_specimen_cabinet.py`，生成 JSON、Markdown 和 PNG，把同一组 Stroop 记录拆成“数据类型标本柜”，作为本章压轴成果图。
- 新增 `12_make_data_type_runtime_evidence.py`，检查本章 14 个关键产物是否生成，并输出 `reports/ch02_data_type_runtime_evidence.md` 与 `output/ch02_data_type_runtime_evidence.png`，让数据类型学习有一张可复盘的运行记录板。
- 新增 `ch02_error_clue_cards.png`、`ch02_practice_workbench.png` 和 `ch02_type_to_file_bridge.png`，把尾部的报错复盘、练习收束和下一章预告接成更自然的图文过渡。
- 保留 MATLAB 教材作为章节组织方式参考，但正文技术内容全部改写为 Python。

## 推荐阅读方式

先打开 `chapters/ch02_python_data_types.md`，按正文顺序阅读；遇到代码示例时，在本包根目录运行：

```bash
python code/ch02/01_constants_keywords.py
python code/ch02/02_variables_labels.py
python code/ch02/03_bool_numbers.py
python code/ch02/04_string_playground.py
python code/ch02/05_list_dict_workshop.py
python code/ch02/06_learning_record_project.py
python code/ch02/07_make_type_decision_cards.py
python code/ch02/08_make_type_compass.py
python code/ch02/09_make_data_type_lab_receipt.py
python code/ch02/10_make_stroop_dataset_pack.py
python code/ch02/11_make_data_type_specimen_cabinet.py
python code/ch02/12_make_data_type_runtime_evidence.py
```

第2章代码仅使用 Python 标准库，不需要额外安装第三方库。

## 图片来源补充

新增互联网图片已保存到 `assets/ch02/web/`，正式教材只引用脚本整理后的本地图片。详细来源、授权和用途见 `source_notes/source_manifest_ch02.md`。
