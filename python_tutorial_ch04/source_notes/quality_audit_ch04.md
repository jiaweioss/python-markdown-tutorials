# 第4章质量检查记录

检查日期：2026-06-22

## 检查范围

- `chapters/ch04_tkinter_gui.md`
- `assets/ch04/`
- `code/ch04/`
- `scripts/generate_ch04_visuals.py`
- `scripts/check_links.py`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch04.md`

## 本轮修复目标

用户要求从第4章开始修复大量无用图片，并完全参照 ch01 标准细修 ch04。因此本轮不只替换图片，也重建了正文结构。

## ch01 标准对照

| 对照项 | ch04 当前记录 | 状态 |
| --- | --- | --- |
| 有清晰导读 | 正文包含“本章导读”“学习目标”“本章分区导航” | 已完成 |
| 有明确章节分界 | 正文拆成五个部分：窗口通电、控件表单、事件反馈、项目成果、排错自查 | 已完成 |
| 图片服务教学动作 | 正文引用 26 张图，分别对应 GUI 历史、路线、步骤、代码映射、真实窗口、表单、反馈、成果、排错和运行记录 | 已完成 |
| 去掉无意义图标拼贴 | 旧版核心图、封面、路线图、常见坑图、项目图等已由结构化步骤图替换 | 已完成 |
| 图片文字不越界 | 新版 `generate_ch04_visuals.py` 使用中文换行和字号适配；抽查路线图、最小窗口图、可用性图无溢出 | 已完成 |
| 真实运行记录 | 保留 3 张 Tkinter 窗口截图，并保留 GUI 可用性、反馈检查、交互记录、卡片成果、旅程图和运行记录图 | 已完成 |
| 学生阅读口吻 | 旧稿重复模板句已改为“运行脚本、看截图、查记录、完成项目”的直接任务口吻 | 已完成 |
| 代码可检查 | `code/ch04/*.py` 和 `scripts/*.py` 均通过 `py_compile` | 已完成 |

## 当前结果

- 正文字数：18606
- 正文图片引用数：26
- 正文 `<figure>` 数：26
- 正文 `<figcaption>` 数：26
- `assets/ch04/` 图片文件数：43
- `code/ch04/` 文件数：11
- 正式图片生成脚本：`scripts/generate_ch04_visuals.py`

## 本轮主要改动

- 重写 `chapters/ch04_tkinter_gui.md`，对齐 ch01 的导读、分区导航、学习记录链和复盘结构。
- 重新穿插 Engelbart、Xerox Alto、Macintosh、Susan Kare、Don Norman 和 HyperCard 等 GUI 人文背景图，使历史素材贴着概念讲。
- 重写 `scripts/generate_ch04_visuals.py`，替换旧的无文字图标拼贴，生成可复现的结构化步骤图。
- 更新 `04_gui_usability_check.py`、`05_make_gui_feedback_lab.py`、`06_make_interaction_receipt.py`、`07_make_card_factory_delivery.py`、`09_make_gui_journey_storyboard.py` 和 `10_make_gui_runtime_evidence.py` 的图片文案，使脚本产物图改为自然中文。
- 保留真实 Tkinter 窗口截图和脚本生成的项目记录图。
- 更新 `README.md` 与 `manifest.json` 的统计和说明。

## 检查动作

- 运行 `python scripts/generate_ch04_visuals.py`，重新生成正式图片。
- 运行 `python scripts/check_links.py`，确认 Markdown 图片链接有效。
- 对 `code/ch04/*.py` 与 `scripts/*.py` 做 `py_compile` 语法检查。
- 用 PIL 打开 `assets/ch04/` 下所有 PNG/JPG 图片。
- 生成临时总览图检查图片构图与排版，并人工抽查 `ch04_roadmap.png`、`ch04_minimal_demo.png`、`ch04_gui_usability_check.png`。

## 当前检查结果

- `scripts/check_links.py`：通过，检查 26 个本地图片引用，0 个缺失链接。
- Python 语法检查：通过，覆盖 12 个 `.py` 文件。
- 图片 PIL 打开检查：通过，43 张 PNG/JPG 图片均可打开。
- 非交互生成脚本烟测：`04_gui_usability_check.py` 到 `10_make_gui_runtime_evidence.py` 均通过。
- 正式图片脚本烟测：`scripts/generate_ch04_visuals.py` 通过。
- 临时总览图人工检查：通过，新版核心图、路线图、最小窗口图、常见坑图、项目面板图和可用性图没有文字越界。
