# 第 3 章来源记录

## 主来源

- `第三章_文件读写与文件夹管理2025.pptx`

本章内容依据原 Python 课件重构，重点吸收以下主题：

1. 打开文件、读取文件、写入文件、复制、移动和删除文件。
2. `open(name, mode, buffering)` 的基本参数。
3. `read()`、`readline()`、`readlines()` 与逐行读取。
4. `write()`、`writelines()` 与文件关闭。
5. 使用 `with open(...) as ...` 简化文件关闭流程。
6. `os`、`os.path`、`pathlib` 在跨平台文件操作中的作用。
7. `shutil.copyfile()`、`shutil.move()` 等高级文件操作。
8. 创建、遍历、删除、复制和移动文件夹。
9. `os.walk()`、`os.rmdir()`、`shutil.rmtree()`、`shutil.copytree()` 等函数。

## 参考来源

- MATLAB 文件与文件夹操作资料仅作教学组织方式参考：借鉴其“先讲文件，再讲文件夹，再讲批量处理”的结构。
- MATLAB 数据分析资料仅作任务驱动风格参考，没有迁移 MATLAB 技术内容作为本章主题。

## 互联网图片来源

本章互联网图片全部先保存到 `assets/ch03/web/`，再由 `scripts/generate_ch03_visuals.py` 整理为正式教材图。图片内部不新增解释文字，说明全部放在 Markdown 正文和图注中。

本轮继续重生成封面、路线图、路径地图、读写流水线、`open()` 模式、读取方法、`with open()`、文件夹管理、文件夹体检、删除安全卡和资料归档器等核心概念图。新版概念图只保留必要标签与视觉关系，避免把长解释直接写进图片；知识点说明改由 Markdown 正文和图注承担。

本轮尾部新增 `ch03_review_checkpoint.png`、`ch03_practice_evidence_workbench.png` 和 `ch03_gui_handoff_bridge.png`。三张图均由 `scripts/generate_ch03_visuals.py` 生成，图片内部不写解释文字，只用文件夹、文件、终端、勾选、窗口等符号打断章末长段文字，并把故事、练习提示和下一章过渡说明放在 Markdown 正文与图注中。

| 用途 | 原图 | 本地原图 | 正式图片 | 来源、作者与授权 |
| --- | --- | --- | --- | --- |
| 资料归档故事 | Archival carton, 01 | `assets/ch03/web/archival_carton_01.jpg` | `assets/ch03/ch03_archive_box_project_story.png` | Wikimedia Commons：`File:Archival carton, 01.jpg`；作者 Daniel Baránek；CC BY-SA 4.0 |
| 路径索引类比 | Card Filing Cabinet | `assets/ch03/web/card_filing_cabinet.jpg` | `assets/ch03/ch03_card_filing_cabinet_path_index.png` | Wikimedia Commons：`File:Card Filing Cabinet.jpg`；作者 Watty62；CC BY-SA 4.0 |
| 文本编码故事 | Rosetta Stone | `assets/ch03/web/rosetta_stone.jpg` | `assets/ch03/ch03_rosetta_encoding_story.png` | Wikimedia Commons：`File:Rosetta Stone.JPG`；作者 Hans Hillewaert；CC BY-SA 4.0 |
| 信息线索故事 | Vannevar Bush portrait | `assets/ch03/web/vannevar_bush_portrait.jpg` | `assets/ch03/ch03_information_trail_vannevar_bush.png` | Wikimedia Commons：`File:Vannevar Bush portrait.jpg`；Public domain |
| 档案层级类比 | Archive storage (Unsplash) | `assets/ch03/web/archive_storage_unsplash.jpg` | `assets/ch03/ch03_archive_storage_shelves.png` | Wikimedia Commons：`File:Archive storage (Unsplash).jpg`；作者 Samuel Zeller；CC0 |

原始链接：

- https://commons.wikimedia.org/wiki/File:Archival_carton,_01.jpg
- https://commons.wikimedia.org/wiki/File:Card_Filing_Cabinet.jpg
- https://commons.wikimedia.org/wiki/File:Rosetta_Stone.JPG
- https://commons.wikimedia.org/wiki/File:Vannevar_Bush_portrait.jpg
- https://commons.wikimedia.org/wiki/File:Archive_storage_(Unsplash).jpg

## 真实运行截图与脚本成果图

- `assets/ch03/web/powershell_ch03_file_operations_run.png`：本地 PowerShell 真实窗口截图，运行 `python code/ch03/01_create_sample_files.py`、`python code/ch03/07_project_archiver.py`，并用 `Get-ChildItem workspace_ch03 -Recurse -File` 列出真实生成文件。
- `assets/ch03/ch03_powershell_file_operations_run.png`：由生成脚本整理后的正式教材图。
- `assets/ch03/web/ch03_archive_manifest_preview.png`：运行 `python code/ch03/08_make_archive_manifest.py` 生成的档案清单预览图。
- `assets/ch03/ch03_archive_manifest_preview.png`：正式教材中的档案清单图。
- `assets/ch03/web/ch03_archive_receipt_preview.png`：运行 `python code/ch03/09_make_archive_receipt.py` 生成的归档记录预览图。
- `assets/ch03/ch03_archive_receipt_preview.png`：正式教材中的归档记录图。
- `assets/ch03/web/ch03_path_safety_receipt.png`：运行 `python code/ch03/10_make_path_safety_receipt.py` 生成的路径安全体检预览图。
- `assets/ch03/ch03_path_safety_receipt.png`：正式教材中的路径安全体检记录图。
- `assets/ch03/web/ch03_ch02_stroop_file_handoff.png`：运行 `python code/ch03/11_make_ch02_stroop_file_handoff.py` 生成的 ch2 到 ch3 文件交接预览图。
- `assets/ch03/ch03_ch02_stroop_file_handoff.png`：正式教材中的跨章节文件交接记录图。
- `assets/ch03/web/ch03_archive_evidence_board.png`：运行 `python code/ch03/12_make_archive_evidence_board.py` 生成的归档记录板预览图。
- `assets/ch03/ch03_archive_evidence_board.png`：正式教材中的归档记录板图。
- `assets/ch03/web/ch03_material_intake_register.png`：运行 `python code/ch03/13_make_material_intake_register.py` 生成的资料入库登记册预览图。
- `assets/ch03/ch03_material_intake_register.png`：正式教材中的资料入库登记册图。
- `workspace_ch03/output/ch03_archive_manifest.md`：可复现档案清单。
- `workspace_ch03/output/ch03_archive_receipt.md`：归档记录 Markdown 报告。
- `workspace_ch03/output/ch03_path_safety_receipt.md`：路径安全体检 Markdown 报告。
- `workspace_ch03/output/ch03_ch02_stroop_file_handoff.md`：ch2 Stroop 数据包进入 ch3 工作区后的交接 Markdown 报告。
- `workspace_ch03/output/ch03_archive_evidence_board.json`：归档记录板结构化摘要。
- `workspace_ch03/output/ch03_archive_evidence_board.png`：归档记录板预览图。
- `reports/ch03_archive_evidence_board.md`：归档记录板 Markdown 报告。
- `workspace_ch03/output/ch03_material_intake_register.json`：资料入库登记册结构化摘要。
- `workspace_ch03/output/ch03_material_intake_register.png`：资料入库登记册预览图。
- `reports/ch03_material_intake_register.md`：资料入库登记册 Markdown 报告。
- `workspace_ch03/organized/json/ch02_stroop_dataset_pack.json`：从第2章复制并归档的 JSON 数据包。
- `workspace_ch03/organized/csv/ch02_stroop_dataset_pack.csv`：从第2章复制并归档的 CSV 数据包。
- `assets/ch03/ch03_review_checkpoint.png`：脚本生成的文件读写复盘检查点，用无文字图形串起路径、文件、检查、终端、输出和复核。
- `assets/ch03/ch03_practice_evidence_workbench.png`：脚本生成的练习记录工作台，用无文字图形呈现输入目录、输出目录、检查清单和终端运行结果。
- `assets/ch03/ch03_gui_handoff_bridge.png`：脚本生成的文件到 GUI 交接桥，用无文字图形衔接第3章文件资料和第4章窗口界面。

## 正式教材图片

本章当前包含 26 张正式教材配图：

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

正式 Markdown 只引用本地整理图，无远程图片依赖。
