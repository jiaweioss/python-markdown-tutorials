# 第 3 章质量检查记录

检查日期：2026-06-17

## 检查范围

本次检查范围是 `python_tutorial_ch03` 包，重点包括：

- `chapters/ch03_file_io_folder_management.md`
- `assets/ch03/`
- `scripts/generate_ch03_visuals.py`
- `scripts/check_links.py`
- `code/ch03/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch03.md`

## 目标对照

| 需求 | 当前记录 | 状态 |
| --- | --- | --- |
| 基于原 Python 课件改写 | 正文覆盖文件读写、路径、编码、`os`、`pathlib`、`shutil` 和文件夹管理 | 已完成 |
| 面向初学者、语言生动 | 正文使用档案盒、文件柜、信息线索、自动关门阅览室、资料归档器等类比 | 已完成 |
| 图文并茂 | 正文引用 26 张本地正式配图，含真实照片、真实 PowerShell 截图、运行产物预览、跨章节文件交接记录、归档记录板、资料入库登记册、章末复盘图、练习记录工作台、GUI 交接桥和核心操作图 | 已完成 |
| 图片全部居中 | 正文 26 张图片全部使用 `<figure align="center">` 与 `margin:0 auto` 居中显示 | 已完成 |
| 图片图注清晰 | 正文 26 张图片全部配有 `<figcaption>`，图注显示标题和学习提示 | 已完成 |
| 图片少放解释文字 | 核心概念图已重新生成，只保留短标签和视觉关系，长解释放在 Markdown 正文和图注中 | 已完成 |
| 学生阅读口吻 | 正文面向学生，不写“后台教学说明” | 已完成 |
| 真实运行环境 | `ch03_powershell_file_operations_run.png` 展示 ch3 脚本在 PowerShell 中真实运行 | 已完成 |
| 故事与知识点穿插 | 档案盒对应资料归档，Vannevar Bush 对应信息线索，文件柜与档案库对应路径和层级，Rosetta Stone 对应文本编码 | 已完成 |
| 人文背景补强 | 新增“外置记忆”叙事，把 `open()`、`Path`、`shutil`、`os.walk()` 和哈希摘要连接到保存、定位、追踪资料的长期人类问题 | 已完成 |
| 图片平均穿插 | 章末新增 `ch03_review_checkpoint.png`、`ch03_practice_evidence_workbench.png` 与 `ch03_gui_handoff_bridge.png`，最大图片间隔从 248 行降到 151 行 | 已完成 |
| 学以致用 | 13 个可运行脚本逐步生成示例资料、报告、清单、归档记录、路径安全体检记录、ch2 数据交接记录、归档记录板和资料入库登记册 | 已完成 |
| 项目收尾闭环 | `08_make_archive_manifest.py`、`09_make_archive_receipt.py`、`10_make_path_safety_receipt.py`、`11_make_ch02_stroop_file_handoff.py`、`12_make_archive_evidence_board.py`、`13_make_material_intake_register.py` 让资料整理从“能跑”走到“可检查、可登记、可复查” | 已完成 |
| 跨章节项目连续性 | `11_make_ch02_stroop_file_handoff.py` 读取第2章 Stroop JSON/CSV 数据包，复制进 ch3 安全工作区并生成文件交接记录 | 已完成 |
| 文件操作安全 | 示例脚本只在 `workspace_ch03` 或临时目录中操作，并提供删除路径保护与路径安全体检 | 已完成 |
| 图片引用不缺失 | `python scripts/check_links.py` 已检查 26 个本地图片引用，0 缺失 | 已完成 |
| 代码与脚本可检查 | AST 已检查 15 个 `.py` 文件，含 13 个代码脚本和 2 个检查/生成脚本 | 已完成 |
| 图片可打开 | PIL 已打开验证 38 张 PNG/JPG/GIF 图片 | 已完成 |
| 全书一致性 | 全书扫描通过：11 个章节包、130 个 Python 文件、108 个 code Python 脚本、278 个 Markdown 图片引用，0 缺图，0 图注不匹配，0 manifest 计数不一致，0 PIL 错误，0 临时总览图残留 | 已完成 |

## 当前素材清单

正式教学图：

- `ch03_cover.png`
- `ch03_roadmap.png`
- `ch03_archive_box_project_story.png`
- `ch03_information_trail_vannevar_bush.png`
- `ch03_file_io_pipeline.png`
- `ch03_card_filing_cabinet_path_index.png`
- `ch03_archive_storage_shelves.png`
- `ch03_powershell_file_operations_run.png`
- `ch03_open_mode_matrix.png`
- `ch03_rosetta_encoding_story.png`
- `ch03_with_context_door.png`
- `ch03_read_methods_comparison.png`
- `ch03_path_map.png`
- `ch03_folder_tree_operations.png`
- `ch03_file_size_chart.png`
- `ch03_safe_delete_warning.png`
- `ch03_path_safety_receipt.png`
- `ch03_ch02_stroop_file_handoff.png`
- `ch03_mini_project_archiver.png`
- `ch03_archive_manifest_preview.png`
- `ch03_archive_receipt_preview.png`
- `ch03_archive_evidence_board.png`
- `ch03_material_intake_register.png`
- `ch03_review_checkpoint.png`
- `ch03_practice_evidence_workbench.png`
- `ch03_gui_handoff_bridge.png`

## 检查命令

在 `python_tutorial_ch03` 目录下运行：

```bash
python code/ch03/01_create_sample_files.py
python code/ch03/02_read_text_file.py
python code/ch03/03_write_report.py
python code/ch03/04_copy_move_files.py
python code/ch03/05_walk_folder_report.py
python code/ch03/06_safe_delete_demo.py
python code/ch03/07_project_archiver.py
python code/ch03/08_make_archive_manifest.py
python code/ch03/09_make_archive_receipt.py
python code/ch03/10_make_path_safety_receipt.py
python code/ch03/11_make_ch02_stroop_file_handoff.py
python code/ch03/12_make_archive_evidence_board.py
python code/ch03/13_make_material_intake_register.py
python scripts/generate_ch03_visuals.py
python scripts/check_links.py
```

当前复验结果：

- 正文图片引用数：26
- 正文 figure 数：26
- 正文 figcaption 数：26
- manifest 图片资产数：38
- `code/ch03` 文件数：14，其中包含 13 个 `.py` 示例脚本和 1 个 `requirements.txt`
- AST 覆盖：15 个 `.py` 文件，包含 13 个代码脚本和 2 个检查/生成脚本
- 13 个示例脚本运行通过
- `scripts/generate_ch03_visuals.py` 运行通过
- `scripts/check_links.py` 运行通过
- PIL 图片打开检查通过：38 张图片
- 临时总览图人工检查通过，新增复盘检查点、练习记录工作台、GUI 交接桥与原有封面、路线图、路径地图、读写流水线、`open()` 模式、读取方法、`with open()`、文件夹管理、文件夹体检、删除安全卡、资料归档器、路径安全体检记录图、ch2 到 ch3 文件交接记录图、归档记录板和资料入库登记册居中无越界；检查图保存在系统临时目录，未写入项目资产。
- 全书一致性扫描：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、278 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个 PIL 错误，0 个旧 SVG 残留，0 个旧 audit 临时图。

## 剩余边界

本章已经按当前图文标准继续扩充。后续若继续精修，可增加更多真实科研资料场景、文件异常案例、跨平台路径案例和跨章节数据流。
