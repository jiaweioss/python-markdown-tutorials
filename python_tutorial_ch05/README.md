# Python Markdown 教程书：第5章

本包是第5章《面向对象程序设计》的 Markdown 教材交付。

## 内容

- `chapters/`：教材正文
- `assets/ch05/`：本章正式图片，全部本地化、居中显示、图注在下
- `assets/ch05/web/`：OOP 历史图片、Smalltalk 教育人物图、真实运行图、运行证据图、xkcd 梗图、心理学素材和脚本生成的预览图
- `code/ch05/`：可运行示例代码
- `reports/`：脚本生成的对象模型报告、类职责卡片、对象协作消息图、对象质量回执和对象交付包报告
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查
- `scripts/generate_ch05_visuals.py`：本章图片生成脚本
- `source_notes/`：来源记录和质量验收
- `manifest.json`：交付清单

## 本章项目

学习卡片对象模型：用类封装学习卡片、卡片盒和实验试次，让代码从散装零件变成可维护模型，并生成对象模型报告、类职责卡片、对象协作消息图、对象质量回执、可复用对象交付包和 OOP 运行证据清单。

## 本轮优化重点

- 正文扩展为 26 张正式配图，新增 Kristen Nygaard、Adele Goldberg、xkcd Code Quality、对象剧场、积木组合、Jean Piaget、类职责卡片预览图、对象协作消息图、对象质量回执、对象交付包、GUI 面板对象模型图和 PowerShell 风格 OOP 运行证据图。
- 把面向对象历史故事穿插到知识点中：Simula/Nygaard 对应真实系统模拟，Alan Kay、Adele Goldberg 和 Smalltalk 对应对象协作与教育探索，Piaget 对应学习图式。
- 新增 `05_make_design_cards.py`，生成 `reports/ch05_design_cards.md` 和 `output/ch05_design_cards_preview.png`。
- 新增 `06_make_object_collaboration_map.py`，生成 `reports/ch05_object_collaboration_map.md` 和 `output/ch05_object_collaboration_map.png`。
- 更新 PowerShell 运行图，展示 OOP 脚本完整运行路径与生成结果，并新增 `07_make_object_quality_receipt.py` 把“避免万能类”变成可检查证据。
- 新增 `08_make_object_delivery_package.py`，生成 `output/ch05_object_delivery_package.json`、`reports/ch05_object_delivery_package.md` 和 `output/ch05_object_delivery_package.png`，把对象模型交给后续章节继续使用。
- 新增 `09_make_gui_panel_object_model.py`，读取 ch4 的 GUI 数据面板规格，生成 `output/ch05_gui_panel_object_model.json`、`reports/ch05_gui_panel_object_model.md` 和 `output/ch05_gui_panel_object_model.png`，把上一章的界面成果拆成对象职责。
- 新增 `10_make_oop_runtime_evidence.py`，生成 `reports/ch05_oop_runtime_evidence.md`、`output/ch05_oop_runtime_evidence.png` 和 `assets/ch05/web/ch05_oop_runtime_evidence.png`，集中检查本章后半段产物是否齐全。
- 新增 `ch05_object_theater_story.png`，用无文字舞台类比图解释“对象不是孤岛，而是有职责、有消息、有合作关系的角色”。
- 继续修正文口吻：把后台式“本教程”说明改成学生正在完成的 OOP 任务，把路线表、核心概念列表和前三个脚本导读从模板句改成具体对象动作。
- 保持图片居中、有图注，图片内部不新增解释性长文字。
