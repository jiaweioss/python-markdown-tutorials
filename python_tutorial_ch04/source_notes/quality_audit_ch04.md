# 第4章质量验收记录

验收日期：2026-06-15

## 验收范围

- `chapters/`
- `assets/ch04/`
- `code/ch04/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch04.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 符合 ch0/ch1 图文标准 | 正文约 19446 字，包含 GUI 历史、真实截图、PowerShell 风格运行证据、设计心理学、门的可发现性故事、交互旅程图、跨章节数据面板、代码、项目、练习与总结 | 已完成 |
| 图片居中且有图注 | 正文 26 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片内部不堆解释文字 | 整理图不新增解释性长文字，故事和说明放在正文与图注 | 已完成 |
| 真实历史素材 | 增加 Xerox Alto、Engelbart 鼠标、Macintosh 128K、HyperCard、Susan Kare、Don Norman 等真实素材 | 已完成 |
| 真实运行环境 | 包含 3 张本地 Tkinter 窗口截图、1 张 PowerShell 风格 GUI 运行证据图、1 张可用性检查图、2 张 GUI 目标与反馈实验成果图、1 张交互回执图、1 张卡片工厂交付回执图、1 张 GUI 交互旅程图和 1 张 ch3 数据 GUI 面板图 | 已完成 |
| 故事与知识点穿插 | GUI 历史、交互设备、卡片式界面、Don Norman 可用性心理学和门的可发现性故事分别嵌入知识点前后 | 已完成 |
| 学生阅读口吻 | 已去掉后台式“本教程”说明，路线表和核心概念表改成学生可直接执行的 GUI 小任务 | 已完成 |
| 学以致用 | 本章项目为“科研卡片工厂控制面板”，并补充界面可用性检查脚本、GUI 反馈检查卡、交互回执、真实 Markdown 卡片交付物、GUI 交互旅程图、GUI 运行证据清单和 ch2/ch3 数据面板交接物 | 已完成 |
| 代码可检查 | 示例脚本均为 ASCII 文件名，可进行 AST 语法检查 | 已完成 |

## 当前结果

- 正文字数：19446
- 正文图片引用数：26
- manifest 素材数：43（26 张正式生成图/整理图 + 17 张本地原图/截图/脚本产物）
- 本章代码文件数：11
- 新增脚本：`code/ch04/04_gui_usability_check.py`、`code/ch04/05_make_gui_feedback_lab.py`、`code/ch04/06_make_interaction_receipt.py`、`code/ch04/07_make_card_factory_delivery.py`、`code/ch04/08_make_ch03_data_gui_panel.py`、`code/ch04/09_make_gui_journey_storyboard.py`、`code/ch04/10_make_gui_runtime_evidence.py`
- 新增脚本输出：`reports/ch04_gui_usability_check.md`、`output/ch04_gui_usability_check.png`、`reports/ch04_gui_feedback_scorecard.md`、`output/ch04_target_feedback_lab.png`、`output/ch04_gui_feedback_scorecard.png`、`reports/ch04_interaction_receipt.md`、`output/ch04_interaction_receipt.png`、`cards/working_memory_load_card.md`、`reports/ch04_card_factory_delivery.md`、`output/ch04_card_factory_delivery.png`、`reports/ch04_ch03_data_gui_panel.md`、`output/ch04_ch03_data_gui_panel.json`、`output/ch04_ch03_data_gui_panel.png`、`reports/ch04_gui_journey_storyboard.md`、`output/ch04_gui_journey_storyboard.png`、`reports/ch04_gui_runtime_evidence.md`、`output/ch04_gui_runtime_evidence.png`

## 验收动作

- 运行 `python scripts/generate_ch04_visuals.py`，重新生成正式图片。
- 运行 `python scripts/check_links.py`，确认 Markdown 图片链接有效。
- 对 `code/ch04/*.py` 与 `scripts/*.py` 做 AST 语法检查。
- 用 PIL 打开 manifest 中记录的所有 PNG/JPG/GIF 图片。
- 生成临时总览图检查构图与排版，确认后删除临时文件。

当前结果：

- `scripts/check_links.py`：通过，检查 26 个本地图片引用，0 个缺失链接。
- Python 语法检查：通过，AST 覆盖 12 个 `.py` 文件，包括 10 个代码脚本和 2 个检查/生成脚本。
- 图片 PIL 打开检查：通过，43 张 PNG/JPG 图片均可打开。
- 非交互生成脚本烟测：`04_gui_usability_check.py`、`05_make_gui_feedback_lab.py`、`06_make_interaction_receipt.py`、`07_make_card_factory_delivery.py`、`08_make_ch03_data_gui_panel.py`、`09_make_gui_journey_storyboard.py`、`10_make_gui_runtime_evidence.py` 均通过。
- 临时总览图人工检查：通过，GUI 历史照片、真实 Tkinter 窗口截图、GUI 运行证据图、目标与反馈实验图、交互旅程图和 ch3 数据 GUI 面板无文字遮挡、无越界；检查图保存在系统临时目录，未写入项目资产。
- 全书一致性扫描：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个临时文件残留。
