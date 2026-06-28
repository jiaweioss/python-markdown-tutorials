# Python Markdown 教程书：第2章优化版

本包是第2章《Python 编程基础：数据类型》的优化后 Markdown 教材交付。

## 内容

- `chapters/ch02_python_data_types.md`：第2章 Markdown 教材正文，已完成图文顺序与新手阅读体验优化
- `assets/ch02/`：第2章正式版配图素材，含统一版式学习图、历史照片和真实 PowerShell 运行截图
- `code/ch02/`：第2章可运行 Python 示例代码
- `reports/`：项目脚本生成的 Markdown 报告
- `output/`：项目脚本生成的 PNG、JSON、CSV、TXT 产物
- `source_notes/source_manifest_ch02.md`：来源线索记录
- `source_notes/quality_audit_ch02.md`：优化后质量验收记录
- `source_notes/ch02_user_experience_review.md`：真实用户体验审阅与修改说明
- `scripts/check_links.py`：Markdown 图片链接检查脚本
- `scripts/generate_ch02_visuals.py`：第2章正式版图片生成脚本
- `manifest.json`：交付清单

## 本轮优化重点

- 调整图片与正文顺序：把 PowerShell 运行图和运行证据图从变量章节后移到本章小项目之后，避免读者还没学到列表、字典和项目产物就提前看总览图。
- 把布尔逻辑图移动到 `and/or/not` 小节，把 IBM 打孔卡分拣机图移动到列表操作和字典之间，增强图文一一对应关系。
- 删除或改写“课件里”“参考 MATLAB 教材”等来源视角表达，让正文保持正式教程口吻。
- 新增 `type()` 检查示例，帮助初学者区分 `"86"` 和 `86`。
- 补充 `float()` 转换、`replace()` 返回新字符串、`round(2.5)` 与 `round(3.5)` 的舍入差异、列表 `append()` 原地修改等新手易错点。
- 优化嵌套列表示例，把 `list1/list2/my_list` 改成更清楚的 `number_list/word_list/nested_list`，并避免把数字写成字符串造成误解。
- 给练习 2-4 增加参考代码，方便自学者完成后自查。
- 更新配套文件树，使图片清单与正文图号顺序一致。

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

## 质量检查

在本包根目录运行：

```bash
python scripts/check_links.py
python code/ch02/12_make_data_type_runtime_evidence.py
```

当前优化版已检查通过：正文 27 张图片链接有效，图号连续，示例脚本可运行，运行证据脚本显示 `14/14 ready`。

## 图片来源补充

互联网图片已保存到 `assets/ch02/web/`，正式教材只引用整理后的本地图片。详细来源、授权和用途见 `source_notes/source_manifest_ch02.md`。
