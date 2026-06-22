# Python Markdown 教程书：第 3 章详细版

本包是第 3 章《文件读写与文件夹管理》的 Markdown 教材交付。

## 内容

- `chapters/ch03_file_io_folder_management.md`：第 3 章 Markdown 教材正文
- `assets/ch03/`：第 3 章正式版配图素材，包含互联网真实照片、真实 PowerShell 运行截图、Python 生成成果图和概念图
- `code/ch03/`：第 3 章可运行 Python 示例代码
- `source_notes/source_manifest_ch03.md`：素材来源、授权和生成线索记录
- `source_notes/quality_audit_ch03.md`：第 3 章质量验收记录
- `source_notes/beginner_practice_report_ch03.md`：第 3 章初学者实操检测报告
- `scripts/check_links.py`：Markdown 图片链接检查脚本
- `scripts/generate_ch03_visuals.py`：第 3 章正式版图片生成脚本
- `manifest.json`：交付清单

## 本轮优化重点

- 正文扩展为 26 张正式配图，所有图片居中显示，图注统一放在图片下方。
- 新增 `10_make_path_safety_receipt.py`，在批量复制、移动、删除前生成“路径安全体检回执”，帮助学生养成先检查路径边界的习惯。
- 新增 `ch03_path_safety_receipt.png`，展示真实运行产物，而不是只讲概念。
- 新增 `11_make_ch02_stroop_file_handoff.py`，读取第2章生成的 Stroop JSON/CSV 数据包，复制到 ch3 安全工作区，按后缀归档并生成文件交接回执。
- 新增 `ch03_ch02_stroop_file_handoff.png`，把跨章节数据交接可视化，让文件读写从“打开文件”升级为“交付资料”。
- 新增 `12_make_archive_evidence_board.py` 和 `ch03_archive_evidence_board.png`，把输入区、整理区、输出区、归档清单、交付回执、路径安全和 ch2 数据交接状态汇总成一张可检查的证据板。
- 新增 `13_make_material_intake_register.py` 和 `ch03_material_intake_register.png`，把 `inbox/`、`organized/`、`output/`、`reports/` 四个区域和关键登记文件汇总成资料入库登记册。
- 新增 `ch03_review_checkpoint.png`、`ch03_practice_evidence_workbench.png` 和 `ch03_gui_handoff_bridge.png`，在核心概念复盘、练习收束和下一章 GUI 过渡处补入无文字解释图，把章末最大无图间隔从 248 行降到 151 行。
- 保留档案盒、文件柜、Rosetta Stone、Vannevar Bush、档案库货架等真实照片，把路径、编码、文件索引、资料归档讲成有记忆点的故事。
- 保留真实 PowerShell 运行截图，展示脚本如何在本机环境中创建、整理和检查 `workspace_ch03`。
- 统一正文图片顺序为“先文字讲解，再图片和图注”，避免运行截图、概念图或故事图抢在说明前出现。
- 重新生成封面、路线图、路径地图、读写流水线、`open()` 模式、读取方法、`with open()`、文件夹管理、文件夹体检、删除安全卡和资料归档器等核心概念图，减少图内长解释文字，把说明留在 Markdown 正文和图注中。
- 本章脚本全部限制在 `workspace_ch03` 练习目录内，避免学生在文件操作章节误删真实资料。
- 修复 `workspace_ch03/inbox/figure.png` 与 `workspace_ch03/organized/png/figure.png`，示例图片现在是真实 PNG 文件，可被 PIL 打开验证。
- 新增初学者实操检测报告，记录 13 个示例脚本、图片链接、语法检查、PIL 图片打开检查和图文顺序检查结果。

## 推荐阅读方式

先打开 `chapters/ch03_file_io_folder_management.md`，按正文顺序阅读。遇到代码示例时，在本包根目录运行：

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
```

第 3 章代码只使用 Python 标准库，不需要额外安装第三方库。

## 运行后会得到

- `workspace_ch03/data/`：练习用原始资料
- `workspace_ch03/output/`：脚本生成的报告、清单和预览图
- `workspace_ch03/output/ch03_archive_manifest.md`：可复现档案清单
- `workspace_ch03/output/ch03_archive_receipt.md`：资料归档回执
- `workspace_ch03/output/ch03_path_safety_receipt.md`：路径安全体检回执
- `workspace_ch03/output/ch03_ch02_stroop_file_handoff.md`：ch2 到 ch3 文件交接回执
- `workspace_ch03/output/ch03_archive_evidence_board.png`：归档证据板
- `workspace_ch03/output/ch03_material_intake_register.png`：资料入库登记册
- `reports/ch03_archive_evidence_board.md`：归档证据板 Markdown 报告
- `reports/ch03_material_intake_register.md`：资料入库登记册 Markdown 报告

## 图片来源补充

互联网图片、真实运行截图和脚本生成成果图都已保存到 `assets/ch03/web/`，正式教材只引用脚本整理后的本地图片。详细来源、授权和用途见 `source_notes/source_manifest_ch03.md`。
