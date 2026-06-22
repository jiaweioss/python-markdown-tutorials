# 第5章质量验收记录

验收日期：2026-06-15

## 验收范围

- `chapters/`
- `assets/ch05/`
- `code/ch05/`
- `output/`
- `reports/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch05.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 符合 ch0/ch1 图文标准 | 正文约 20213 字，包含 Simula、Kristen Nygaard、工程蓝图、Alan Kay、Adele Goldberg、Smalltalk/Squeak、xkcd 梗图、对象剧场、积木组合、Piaget、真实运行图、OOP 运行证据图、对象协作消息图、对象质量回执、对象交付包、GUI 面板对象模型、代码、项目、练习与总结 | 已完成 |
| 图片居中且有图注 | 正文 26 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片内部不堆解释文字 | 整理图不新增解释性长文字，说明放在正文和图注；真实历史图、软件截图、漫画和报告图保留原图内容 | 已完成 |
| 故事与知识点穿插 | Simula 与 Nygaard 对应对象源头，蓝图对应类/对象，Alan Kay、Adele Goldberg 与 Smalltalk 对应对象协作和教育探索，xkcd 对应代码质量，对象剧场对应职责与消息协作，积木对应组合，Piaget 对应认知图式 | 已完成 |
| 学生阅读口吻 | 已去掉后台式“本教程”说明，路线表、核心概念列表和脚本导读改成学生可直接观察和执行的对象动作 | 已完成 |
| 真实运行环境 | `ch05_powershell_oop_run.png` 展示 5 个脚本在 PowerShell 语境中的运行路径与生成结果；`ch05_oop_runtime_evidence.png` 集中检查对象模型报告、职责卡片、协作图、质量回执、交付包和 GUI 面板对象模型是否生成 | 已完成 |
| 学以致用 | 本章项目为“学习卡片对象模型”，新增对象模型报告、预览图、类职责卡片、对象协作消息图、对象质量回执、对象交付包和 ch4 GUI 面板对象模型 | 已完成 |
| 代码可检查 | 示例脚本均为 ASCII 文件名，可进行 AST 语法检查 | 已完成 |

## 当前结果

- 正文字符数：20213
- 正文图片引用数：26
- manifest 素材数：43
- 本章代码文件数：11，其中 Python 脚本 10 个
- Markdown 图片语法数量：0
- 图注数量：26

## 运行结果

本机已运行：

```bash
python code/ch05/01_learning_card_class.py
python code/ch05/02_card_deck.py
python code/ch05/03_trial_object.py
python code/ch05/04_make_oop_model_report.py
python code/ch05/05_make_design_cards.py
python code/ch05/06_make_object_collaboration_map.py
python code/ch05/07_make_object_quality_receipt.py
python code/ch05/08_make_object_delivery_package.py
python code/ch05/09_make_gui_panel_object_model.py
python code/ch05/10_make_oop_runtime_evidence.py
```

生成文件：

- `reports/ch05_oop_model_report.md`
- `reports/ch05_oop_model_preview.png`
- `reports/ch05_design_cards.md`
- `output/ch05_design_cards_preview.png`
- `reports/ch05_object_collaboration_map.md`
- `output/ch05_object_collaboration_map.png`
- `reports/ch05_object_quality_receipt.md`
- `output/ch05_object_quality_receipt.png`
- `output/ch05_object_delivery_package.json`
- `reports/ch05_object_delivery_package.md`
- `output/ch05_object_delivery_package.png`
- `output/ch05_gui_panel_object_model.json`
- `reports/ch05_gui_panel_object_model.md`
- `output/ch05_gui_panel_object_model.png`
- `reports/ch05_oop_runtime_evidence.md`
- `output/ch05_oop_runtime_evidence.png`
- `assets/ch05/web/ch05_oop_runtime_evidence.png`

## 验收动作

- 运行 `python scripts/generate_ch05_visuals.py`，重新生成 26 张正式图片。
- 运行 `python scripts/check_links.py`，确认 Markdown 图片链接有效。
- 对 `code/ch05/*.py` 与 `scripts/*.py` 做 AST 语法检查。
- 用 PIL 打开所有 PNG/JPG/GIF 图片。
- 生成临时总览图检查构图与排版，确认后删除临时文件。
- 全书一致性扫描：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个临时文件残留。

当前结果：

- `scripts/check_links.py`：通过，检查 26 个本地图片引用。
- Python 语法检查：通过，AST 覆盖 12 个 `.py` 文件，包括 10 个代码脚本和 2 个检查/生成脚本。
- 图片 PIL 打开检查：通过，43 张 PNG/JPG/GIF 图片均可打开。
- 示例脚本烟测：`01_learning_card_class.py` 到 `10_make_oop_runtime_evidence.py` 均通过。
- 临时总览图人工检查：通过，历史照片、xkcd、PowerShell 真实运行图、OOP 运行证据图、对象剧场图和 GUI 面板对象模型图无文字遮挡、无越界；检查图保存在系统临时目录，未写入项目资产。
- 全书一致性扫描：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个临时文件残留。
