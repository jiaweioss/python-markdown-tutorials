# 第5章质量验收记录

验收日期：2026-06-22

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
| 对标 ch01/ch04 图文标准 | 正文重写为 `[TOC]`、本章导读、分区导航、五个学习部分、运行证据、练习、自测和复盘模板 | 已完成 |
| 图片有明确教学意义 | 正文 26 张图片覆盖路线图、代码对照图、心智模型、对象协作图、质量回执、交付包、运行证据，以及 Simula、Smalltalk、认知图式和代码文化背景 | 已完成 |
| 图片居中且有图注 | 正文 26 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片文字不越界 | 重建生成器后检查接触表，并满尺寸检查最小类、质量回执、对象协作图和运行证据图 | 已完成 |
| 学生阅读口吻 | 删除旧模板里的历史堆叙述和机械说明，改为“先跑脚本、再看证据、最后划清职责”的学习路线 | 已完成 |
| 真实运行环境 | `ch05_powershell_oop_run.png` 与 `ch05_oop_runtime_evidence.png` 展示本章脚本运行和交付物就绪状态 | 已完成 |
| 学以致用 | 本章项目为“学习卡片对象模型”，包含对象模型报告、类职责卡片、对象协作消息图、对象质量回执、对象交付包和 ch4 GUI 面板对象模型 | 已完成 |
| 代码可检查 | 示例脚本均为 ASCII 文件名，可进行语法检查和脚本烟测 | 已完成 |

## 当前结果

- 正文字符数：20837
- 正文图片引用数：26
- manifest 素材数：43
- 本章代码文件数：11，其中 Python 脚本 10 个
- Markdown 图片语法数量：0
- 图注数量：26
- 标题数量：38，其中二级标题 12 个、三级标题 24 个

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
python scripts/generate_ch05_visuals.py
```

生成或更新文件：

- `reports/ch05_oop_model_report.md`
- `reports/ch05_oop_model_preview.png`
- `assets/ch05/web/ch05_oop_model_preview.png`
- `reports/ch05_design_cards.md`
- `output/ch05_design_cards_preview.png`
- `assets/ch05/web/ch05_design_cards_preview.png`
- `reports/ch05_object_collaboration_map.md`
- `output/ch05_object_collaboration_map.png`
- `assets/ch05/web/ch05_object_collaboration_map.png`
- `reports/ch05_object_quality_receipt.md`
- `output/ch05_object_quality_receipt.png`
- `assets/ch05/web/ch05_object_quality_receipt.png`
- `output/ch05_object_delivery_package.json`
- `reports/ch05_object_delivery_package.md`
- `output/ch05_object_delivery_package.png`
- `assets/ch05/web/ch05_object_delivery_package.png`
- `output/ch05_gui_panel_object_model.json`
- `reports/ch05_gui_panel_object_model.md`
- `output/ch05_gui_panel_object_model.png`
- `assets/ch05/web/ch05_gui_panel_object_model.png`
- `reports/ch05_oop_runtime_evidence.md`
- `output/ch05_oop_runtime_evidence.png`
- `assets/ch05/web/ch05_oop_runtime_evidence.png`

## 验收动作

- 运行 `python scripts/check_links.py`，确认 Markdown 图片链接有效，检查 26 个本地图片引用。
- 运行 `python scripts/generate_ch05_visuals.py`，重新生成本章正式图片。
- 对 `code/ch05/*.py` 与 `scripts/*.py` 做 Python 语法检查。
- 用 PIL 打开 `assets/ch05/` 下 43 张 PNG/JPG 图片。
- 生成临时总览图检查构图与排版，确认后删除临时文件。
- 做 ch05 本章一致性扫描：正文计数、图片引用、图注数量与 manifest 同步，0 个缺失本地图片链接。

## 已知边界

仓库级扫描仍能看到 ch01 的既有 manifest 字数漂移和部分 README 中的图注片段不匹配；这些不是本轮 ch05 改动产生，未在本次提交中处理。
