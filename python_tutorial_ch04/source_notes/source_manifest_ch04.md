# 第4章来源记录

## 主来源

- `第四章_Python GUI设计2025.pptx`

本章依据 ch0 课程路线进行扩展，主题为《Tkinter 图形界面编程》。MATLAB 教材仅作为“讲故事、放图片、做任务、跑代码、看成果”的组织方式参考，不迁移 MATLAB 技术内容。

## 新增互联网图片来源

互联网图片全部先保存到 `assets/ch04/web/`，再由 `scripts/generate_ch04_visuals.py` 整理成正式教材图。整理图内部不新增解释文字，说明放在 Markdown 正文和图注中。

| 用途 | 原图 | 本地原图 | 正式图片 | 来源、作者与授权 |
| --- | --- | --- | --- | --- |
| GUI 历史故事 | Xerox Alto I, 1973, Computer History Museum | `assets/ch04/web/xerox_alto_1973.jpg` | `assets/ch04/ch04_history_xerox_alto.png` | Wikimedia Commons：`File:Xerox Alto I, 1973, Computer History Museum.jpg`；作者 The wub；CC BY-SA 4.0 |
| 交互设备历史 | Replica of prototype Engelbart mouse | `assets/ch04/web/engelbart_mouse_replica.jpg` | `assets/ch04/ch04_engelbart_mouse_story.png` | Wikimedia Commons：`File:Replica of prototype Engelbart mouse, circa 1964, Computer History Museum.jpg`；作者 The wub；CC BY-SA 4.0 |
| GUI 进入普通人桌面 | Macintosh 128k transparency | `assets/ch04/web/macintosh_128k_transparency.png` | `assets/ch04/ch04_macintosh_gui_story.png` | Wikimedia Commons：`File:Macintosh 128k transparency.png`；作者 Grm wnr / All About Apple Museum；CC BY-SA 2.5 IT、CC BY-SA 3.0、GFDL |
| 卡片式界面历史 | HyperCard | `assets/ch04/web/hypercard.jpg` | `assets/ch04/ch04_hypercard_story.png` | Wikimedia Commons：`File:HyperCard.jpg`；作者 Sandra Becker 01；CC BY-SA 4.0 |
| 图标与可识别性 | Susan Kare portrait | `assets/ch04/web/susan_kare_2019.jpg` | `assets/ch04/ch04_susan_kare_icon_story.png` | Wikimedia Commons：`File:SusanKare2019photo.jpg`；来源 Cooper Hewitt；CC BY 3.0 |
| 可用性与设计心理学 | Don Norman portrait | `assets/ch04/web/don_norman_cropped.jpg` | `assets/ch04/ch04_don_norman_story.png` | Wikimedia Commons：`File:MMG - Don Norman - 5552663659 (cropped).jpg`；作者 Meet the media Guru，photo by Paolo Sacchi；CC BY-SA 2.0 |

原始链接：

- https://commons.wikimedia.org/wiki/File:Xerox_Alto_I,_1973,_Computer_History_Museum.jpg
- https://commons.wikimedia.org/wiki/File:Replica_of_prototype_Engelbart_mouse,_circa_1964,_Computer_History_Museum.jpg
- https://commons.wikimedia.org/wiki/File:Macintosh_128k_transparency.png
- https://commons.wikimedia.org/wiki/File:HyperCard.jpg
- https://commons.wikimedia.org/wiki/File:SusanKare2019photo.jpg
- https://commons.wikimedia.org/wiki/File:MMG_-_Don_Norman_-_5552663659_(cropped).jpg

## 真实运行截图与脚本产物

- `assets/ch04/web/tkinter_hello_window.png`：本地实际运行 `python code/ch04/01_hello_window.py` 后捕获的 Tkinter 窗口。
- `assets/ch04/web/tkinter_card_form_window.png`：本地实际运行 `python code/ch04/02_card_form.py` 后捕获的学习卡片表单窗口。
- `assets/ch04/web/tkinter_stroop_window.png`：本地实际运行 `python code/ch04/03_stroop_gui_preview.py` 后捕获的 Stroop GUI 预告窗口。
- `assets/ch04/web/ch04_gui_usability_check_output.png`：本地运行 `python code/ch04/04_gui_usability_check.py` 生成的界面可用性检查图。
- `assets/ch04/web/ch04_target_feedback_lab.png`：本地运行 `python code/ch04/05_make_gui_feedback_lab.py` 生成的 GUI 目标与反馈实验图。
- `assets/ch04/web/ch04_gui_feedback_scorecard.png`：本地运行 `python code/ch04/05_make_gui_feedback_lab.py` 生成的 GUI 反馈检查卡。
- `assets/ch04/web/ch04_interaction_receipt.png`：本地运行 `python code/ch04/06_make_interaction_receipt.py` 生成的 GUI 交互回执。
- `assets/ch04/web/ch04_card_factory_delivery.png`：本地运行 `python code/ch04/07_make_card_factory_delivery.py` 生成的卡片工厂交付回执。
- `assets/ch04/web/ch04_ch03_data_gui_panel.png`：本地运行 `python code/ch04/08_make_ch03_data_gui_panel.py` 读取 ch3 整理后的 Stroop JSON 数据后生成的 GUI 数据浏览面板预览。
- `assets/ch04/web/ch04_gui_journey_storyboard.png`：本地运行 `python code/ch04/09_make_gui_journey_storyboard.py` 生成的 GUI 交互旅程图。
- `assets/ch04/web/ch04_gui_runtime_evidence.png`：本地运行 `python code/ch04/10_make_gui_runtime_evidence.py` 生成的 GUI 运行证据图，用于核对窗口截图、报告、回执和跨章节 GUI 面板是否 ready。
- `cards/working_memory_load_card.md`：本地运行 `python code/ch04/07_make_card_factory_delivery.py` 生成的 Markdown 学习卡片。
- `reports/ch04_card_factory_delivery.md`：本地运行 `python code/ch04/07_make_card_factory_delivery.py` 生成的项目交付报告。
- `reports/ch04_ch03_data_gui_panel.md`：本地运行 `python code/ch04/08_make_ch03_data_gui_panel.py` 生成的跨章节数据面板交接报告。
- `output/ch04_ch03_data_gui_panel.json`：本地运行 `python code/ch04/08_make_ch03_data_gui_panel.py` 生成的 GUI 面板规格文件。
- `reports/ch04_gui_journey_storyboard.md`：本地运行 `python code/ch04/09_make_gui_journey_storyboard.py` 生成的交互旅程说明。
- `reports/ch04_gui_runtime_evidence.md`：本地运行 `python code/ch04/10_make_gui_runtime_evidence.py` 生成的运行证据清单。

这些素材分别整理为 `ch04_tkinter_hello_window_screenshot.png`、`ch04_tkinter_card_form_screenshot.png`、`ch04_tkinter_stroop_screenshot.png`、`ch04_gui_runtime_evidence.png`、`ch04_gui_usability_check.png`、`ch04_target_feedback_lab.png`、`ch04_gui_feedback_scorecard.png`、`ch04_interaction_receipt.png`、`ch04_card_factory_delivery.png`、`ch04_ch03_data_gui_panel.png` 和 `ch04_gui_journey_storyboard.png`；新生成的无文字类比图为 `ch04_norman_door_affordance.png`。

## 生成素材

本章包含 26 张正式图片，均由 `scripts/generate_ch04_visuals.py` 生成或整理。图片内部不放解释性长文字，说明统一写在 Markdown 正文和图注中；脚本生成的 GUI 结果图保留界面自身文字，用于展示真实产物。新增的 `ch04_norman_door_affordance.png` 用推板和拉手的无文字示意图承接 Don Norman 的可用性故事；GUI 交互旅程图把打开窗口、输入内容、点击按钮、看到反馈和得到文件连成闭环；GUI 运行证据图把窗口截图、报告、回执和跨章节面板的 ready 状态集中到一张 PowerShell 风格证据板；ch3 数据 GUI 面板把 ch2 的 Stroop 数据、ch3 的文件整理和 ch4 的界面设计连成一个连续项目。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 每张图片都有 `<figcaption>`。
- 示例代码与项目任务围绕“科研卡片工厂”连续推进。
- 本轮继续做学生视角修订：正文不再用“本教程会……”这类后台口吻，路线表和核心概念表改成学生可直接执行的 GUI 小任务。
