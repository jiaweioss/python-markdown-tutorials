# Python Markdown 教程书：第7章

本包是第7章《PyGame 游戏开发》的 Markdown 教材包。

## 内容

- `chapters/`：教材正文
- `assets/ch07/`：本章正式图片，全部本地化、居中显示、图注在下
- `assets/ch07/web/`：游戏史图片、心流与心理学素材、Skinner 教学机器、本机 PyGame 窗口截图、PowerShell 运行图、游戏运行记录图和脚本生成的预览图
- `code/ch07/`：可运行示例代码
- `reports/`：脚本生成的关键词反应小游戏报告、难度调参报告、心流难度调参曲线、反馈循环卡、教学反馈小游戏计划和游戏运行记录报告
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查
- `scripts/generate_ch07_visuals.py`：本章图片生成脚本
- `source_notes/`：来源记录和质量检查
- `manifest.json`：文件清单

## 本章项目

关键词反应小游戏：做一个能呈现刺激、接收按键、记录得分的复习小游戏，并生成可复盘的反应报告、难度调参报告、心流难度调参曲线、游戏反馈循环卡、教学反馈小游戏计划和运行记录总览。

## 本轮增强

- 增加 Tennis for Two、Atari Pong、Magnavox Odyssey 和 Spacewar!/PDP-1 真实历史图片，用游戏史解释窗口、输入、状态更新和反馈。
- 增加 Csikszentmihalyi 心流人物图、Stroop 效应素材和 Skinner teaching machine，把 PyGame 游戏开发和心理学反应时任务、即时反馈机制联系起来。
- 新增 `ch07_feedback_playground_loop.png`，用无文字“反馈回路操场”类比图解释目标、输入、反馈和重试如何连成学习循环。
- 新增 `05_make_game_balance_report.py`，生成 `reports/ch07_game_balance_report.md` 和 `output/ch07_game_balance_preview.png`。
- 新增 `06_make_game_feedback_loop.py`，生成 `reports/ch07_game_feedback_loop.md` 和 `output/ch07_game_feedback_loop.png`，帮助学生检查目标、输入、状态更新、反馈和重试意愿。
- 新增 `07_make_flow_tuning_curve.py`，生成 `reports/ch07_flow_tuning_curve.md` 和 `output/ch07_flow_tuning_curve.png`，把“太简单会无聊、太难会焦虑、刚刚好才进入心流”落成可检查的图表成果。
- 新增 `08_make_data_driven_tuning.py`，读取 ch6 的数据摘要，生成 `reports/ch07_data_driven_tuning.md`、`output/ch07_data_driven_tuning.json` 和 `output/ch07_data_driven_tuning.png`。
- 新增 `09_make_teaching_feedback_game.py`，读取 ch6 的记忆复习计划，生成 `reports/ch07_teaching_feedback_game.md`、`output/ch07_teaching_feedback_game.json` 和 `output/ch07_teaching_feedback_game.png`。
- 新增 `10_make_game_runtime_evidence.py`，检查本章 14 个关键游戏产物，生成 `reports/ch07_game_runtime_evidence.md`、`output/ch07_game_runtime_evidence.png` 和正文图 `ch07_game_runtime_evidence.png`。
- 更新 PowerShell 运行截图，展示 pygame 检查、计分逻辑和反应报告生成。
- 正文 25 张图片全部使用居中的 `<figure>` 结构和清晰图注。
- 继续收紧正文口吻：路线表、核心概念和脚本导读改成学生能直接执行和观察的游戏任务，减少模板化说明。
- 新增 `[TOC]`、本章导读、分区导航和五个清晰部分：交互游戏史、PyGame 运行、概念脚本、项目记录、练习复盘。
- 本章继续作为本地后续章节整理，不改变网站发布边界；线上仍只开放到 ch06。
