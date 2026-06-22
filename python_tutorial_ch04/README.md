# Python Markdown 教程书：第4章

本包是第4章《Tkinter 图形界面编程》的 Markdown 教材交付。

## 内容

- `chapters/`：教材正文
- `assets/ch04/`：本章正式图片，含统一版式教学图、互联网 GUI 历史照片、真实 Tkinter 窗口截图和脚本生成成果图
- `code/ch04/`：可运行示例代码
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查
- `scripts/generate_ch04_visuals.py`：本章图片生成脚本
- `source_notes/`：来源记录和质量验收
- `manifest.json`：交付清单

## 本章项目

科研卡片工厂控制面板：做一个能输入主题、生成学习卡片草稿并保存文件的 Tkinter 小窗口，并用交付回执和交互旅程图证明它确实完成了从输入到文件的闭环。

## 本轮优化重点

- 正文扩展为 26 张正式配图，新增 Xerox Alto、Engelbart 原型鼠标、Macintosh 128K、HyperCard、Susan Kare、Don Norman、门的可发现性示意图、3 张真实 Tkinter 运行截图、PowerShell 风格 GUI 运行证据图、GUI 目标与反馈实验图、GUI 交互回执图、卡片工厂交付回执图、GUI 交互旅程图和 ch3 数据 GUI 面板预览图。
- 把泛化讲解改成具体 Tkinter 心智模型：`Tk()`、控件、布局、回调、`mainloop()`。
- 加强心理学 Stroop 任务例子，突出刺激、按键反应和反应时记录。
- 新增 `04_gui_usability_check.py`、`05_make_gui_feedback_lab.py`、`06_make_interaction_receipt.py`、`07_make_card_factory_delivery.py`、`08_make_ch03_data_gui_panel.py`、`09_make_gui_journey_storyboard.py` 和 `10_make_gui_runtime_evidence.py`，生成 GUI 可用性检查清单、目标与反馈实验图、反馈检查卡、交互回执、卡片工厂交付回执、GUI 交互旅程图、ch3 数据浏览面板预览和 GUI 运行证据清单，把“界面是否好用、是否留下成果、是否能接住前面章节的数据、是否有运行证据链”变成可检查、可复盘的问题。
- 新增 `output/ch04_ch03_data_gui_panel.json`、`reports/ch04_ch03_data_gui_panel.md` 和 `output/ch04_ch03_data_gui_panel.png`，把 ch2 的 Stroop 数据和 ch3 的文件整理成果接入 ch4 的 GUI 设计。
- 新增 `cards/working_memory_load_card.md` 与 `reports/ch04_card_factory_delivery.md`，让本章从“能弹出窗口”推进到“能交付一张学习卡片”。
- 新增 `reports/ch04_gui_journey_storyboard.md` 与 `output/ch04_gui_journey_storyboard.png`，把打开窗口、输入内容、点击按钮、看到反馈和得到文件连成一条用户旅程。
- 新增 `reports/ch04_gui_runtime_evidence.md` 与 `output/ch04_gui_runtime_evidence.png`，核对 Tkinter 窗口截图、可用性报告、交互回执、卡片交付物、ch3 数据面板和交互旅程图是否已经 ready。
- 新增 `ch04_norman_door_affordance.png`，用“推板/拉手”的视觉故事解释 GUI 控件为什么需要清楚的可发现性和反馈。
- 继续修正文口吻：把后台式“本教程”说明改成学生正在完成的 GUI 任务，把路线表和核心概念表从模板句改成具体可执行动作。
- 新增来源记录，互联网图片与真实截图均保存到 `assets/ch04/web/`，正式正文只引用整理后的本地图片。
