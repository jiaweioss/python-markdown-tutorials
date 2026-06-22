# 第 3 章质量验收记录

验收日期：2026-06-19

## 验收范围

本次验收范围是 `python_tutorial_ch03` 包，重点包括：

- `chapters/ch03_file_io_folder_management.md`
- `assets/ch03/`
- `scripts/generate_ch03_visuals.py`
- `scripts/check_links.py`
- `code/ch03/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch03.md`
- `source_notes/beginner_practice_report_ch03.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 基于原 Python 课件改写 | 正文覆盖文件读写、路径、编码、`os`、`pathlib`、`shutil` 和文件夹管理 | 已完成 |
| 面向初学者、语言生动 | 正文使用档案盒、文件柜、信息线索、自动关门阅览室、资料归档器等类比 | 已完成 |
| 图文并茂 | 正文引用 26 张本地正式配图，含真实照片、真实 PowerShell 截图、运行产物预览、跨章节文件交接回执、归档证据板、资料入库登记册、章末复盘图、练习证据工作台、GUI 交接桥和核心操作图 | 已完成 |
| 图片全部居中 | 正文 26 张图片全部使用 `<figure align="center">` 与 `margin:0 auto` 居中显示 | 已完成 |
| 图片图注清晰 | 正文 26 张图片全部配有 `<figcaption>`，图注显示标题和学习提示 | 已完成 |
| 图片少放解释文字 | 核心概念图已重新生成，只保留短标签和视觉关系，长解释放在 Markdown 正文和图注中 | 已完成 |
| 学生阅读口吻 | 正文面向学生，不写“教师应该如何讲” | 已完成 |
| 真实运行环境 | `ch03_powershell_file_operations_run.png` 展示 ch3 脚本在 PowerShell 中真实运行 | 已完成 |
| 故事与知识点穿插 | 档案盒对应资料归档，Vannevar Bush 对应信息线索，文件柜与档案库对应路径和层级，Rosetta Stone 对应文本编码 | 已完成 |
| 图片平均穿插 | 章末新增 `ch03_review_checkpoint.png`、`ch03_practice_evidence_workbench.png` 与 `ch03_gui_handoff_bridge.png`，最大图片间隔从 248 行降到 151 行 | 已完成 |
| 图文顺序统一 | 26 张图前均有正文讲解、任务设置或过渡句，统一为“先叙述，再图片和图注” | 已完成 |
| 学以致用 | 13 个可运行脚本逐步生成示例资料、报告、清单、归档回执、路径安全体检回执、ch2 数据交接回执、归档证据板和资料入库登记册 | 已完成 |
| 初学者实操报告 | `source_notes/beginner_practice_report_ch03.md` 从学生视角记录运行路线、结果产物、常见踩坑和复验结论 | 已完成 |
| 项目交付闭环 | `08_make_archive_manifest.py`、`09_make_archive_receipt.py`、`10_make_path_safety_receipt.py`、`11_make_ch02_stroop_file_handoff.py`、`12_make_archive_evidence_board.py`、`13_make_material_intake_register.py` 让资料整理从“能跑”走到“可检查、可登记、可交付” | 已完成 |
| 跨章节项目连续性 | `11_make_ch02_stroop_file_handoff.py` 读取第2章 Stroop JSON/CSV 数据包，复制进 ch3 安全工作区并生成文件交接回执 | 已完成 |
| 文件操作安全 | 示例脚本只在 `workspace_ch03` 或临时目录中操作，并提供删除路径保护与路径安全体检 | 已完成 |
| 图片引用不缺失 | `python scripts/check_links.py` 已检查 26 个本地图片引用，0 缺失 | 已完成 |
| 代码与脚本可检查 | `py_compile` 已检查 15 个 `.py` 文件，含 13 个代码脚本和 2 个检查/生成脚本 | 已完成 |
| 图片可打开 | PIL 已打开验证 `assets/`、`workspace_ch03/`、`reports/` 下 46 张 PNG/JPG/GIF 图片 | 已完成 |
| 示例 PNG 有效 | `workspace_ch03/inbox/figure.png` 与 `workspace_ch03/organized/png/figure.png` 均为真实 PNG，不再是文本伪图片 | 已完成 |
| ch03 当前一致性 | ch03 扫描通过：26 个 figure、26 个 img、26 个 figcaption、26 个本地图片引用、0 缺图、0 PIL 错误、0 fake image bytes、0 临时总览图残留 | 已完成 |

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

## 验收命令

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
- `py_compile` 覆盖：15 个 `.py` 文件，包含 13 个代码脚本和 2 个检查/生成脚本
- PIL 图片打开检查通过：46 张图片，其中 38 张为 `assets/` 素材图，8 张为 `workspace_ch03/` 与 `reports/` 的运行产物图
- 图文顺序扫描通过：26 张图前均有正文讲解、任务设置或过渡句，未再出现标题后直接贴图、分隔线后直接贴图或代码块后无解释直接贴图的问题
- `workspace_ch03/inbox/figure.png` 与 `workspace_ch03/organized/png/figure.png` 已验证为真实 PNG，大小 76 bytes，可由 PIL 打开
- 临时总览图人工检查通过，26 张正式教学图无空白、明显越界或错位；检查图已删除，未留在项目资产中
- ch03 当前一致性扫描：通过，26 个 figure、26 个 img、26 个 figcaption、26 个本地图片引用，0 个缺失本地图片链接，0 个 PIL 错误，0 个 fake image bytes，0 个旧 SVG 残留，0 个临时总览图残留

## 剩余边界

本章已经按当前图文标准继续扩充。后续若继续精修，可增加更多真实科研资料场景、文件异常案例、跨平台路径案例和跨章节数据流。
