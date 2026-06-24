# Python Markdown 教程书：第4章

本包是第4章《Tkinter 图形界面编程》的 Markdown 教材包。

## 内容

- `chapters/`：教材正文
- `assets/ch04/`：本章正式图片，含统一版式步骤图、真实 Tkinter 窗口截图和脚本生成成果图
- `code/ch04/`：可运行示例代码
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查
- `scripts/generate_ch04_visuals.py`：本章图片生成脚本
- `source_notes/`：来源记录和质量检查
- `manifest.json`：文件清单

## 本章项目

科研卡片工厂控制面板：做一个能输入主题、生成学习卡片草稿并保存文件的 Tkinter 小窗口，并用学习成果记录和交互旅程图证明它确实完成了从输入到文件的闭环。

## 本轮优化重点

- 正文重排为对标 ch01 的结构：本章导读、学习目标、分区导航、五个部分、上机路线、学习成果记录、自测问题和复盘模板。
- 正文保留 26 张有明确教学作用的配图，删去旧稿中成串的无信息量图标拼贴；GUI 历史图片重新贴着概念穿插，服务“输入设备、窗口、图标、可用性、步骤、真实截图、成果记录”。
- 重写 `scripts/generate_ch04_visuals.py`，用可复现的 Pillow 绘图生成结构化步骤图，支持中文自动换行与字号适配，避免文字越界。
- 把泛化讲解改成具体 Tkinter 心智模型：`Tk()`、控件、布局、回调、`mainloop()`、反馈和文件记录。
- 加强心理学 Stroop 任务例子，突出刺激、按键反应、正确性和反应时记录。
- 新增 `04_gui_usability_check.py`、`05_make_gui_feedback_lab.py`、`06_make_interaction_receipt.py`、`07_make_card_factory_delivery.py`、`08_make_ch03_data_gui_panel.py`、`09_make_gui_journey_storyboard.py` 和 `10_make_gui_runtime_evidence.py`，生成 GUI 可用性检查清单、目标与反馈实验图、反馈检查卡、交互记录、卡片工厂学习成果记录、GUI 交互旅程图、ch3 数据浏览面板预览和 GUI 运行记录清单，把“界面是否好用、是否留下成果、是否能接住前面章节的数据、是否有运行记录链”变成可检查、可复盘的问题。
- 新增 `output/ch04_ch03_data_gui_panel.json`、`reports/ch04_ch03_data_gui_panel.md` 和 `output/ch04_ch03_data_gui_panel.png`，把 ch2 的 Stroop 数据和 ch3 的文件整理成果接入 ch4 的 GUI 设计。
- 新增 `cards/working_memory_load_card.md` 与 `reports/ch04_card_factory_delivery.md`，让本章从“能弹出窗口”推进到“能生成一张学习卡片”。
- 新增 `reports/ch04_gui_journey_storyboard.md` 与 `output/ch04_gui_journey_storyboard.png`，把打开窗口、输入内容、点击按钮、看到反馈和得到文件连成一条用户旅程。
- 新增 `reports/ch04_gui_runtime_evidence.md` 与 `output/ch04_gui_runtime_evidence.png`，核对 Tkinter 窗口截图、可用性报告、交互记录、卡片成果文件、ch3 数据面板和交互旅程图是否已经 ready。
- 更新 `ch04_norman_door_affordance.png`，用“推板/拉手”的视觉故事解释 GUI 控件为什么需要清楚的可发现性和反馈。
- 修正文口吻：减少模板句和工具腔表达，把每节内容落到学生能直接运行、检查、复盘的 GUI 小任务。
- 新增来源记录，互联网图片与真实截图均保存到 `assets/ch04/web/`，正式正文只引用整理后的本地图片。
