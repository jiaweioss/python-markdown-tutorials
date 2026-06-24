# 第7章质量检查记录

检查日期：2026-06-15

## 检查范围

- `chapters/`
- `assets/ch07/`
- `code/ch07/`
- `output/`
- `reports/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch07.md`

## 目标对照

| 需求 | 当前记录 | 状态 |
| --- | --- | --- |
| 符合 ch0/ch1 图文标准 | 正文约 19563 字，包含 `[TOC]`、本章导读、分区导航、五个清晰部分、Tennis for Two、Pong、Magnavox Odyssey、Spacewar、Csikszentmihalyi、Stroop、Skinner teaching machine、反馈回路操场、真实 PyGame 窗口、PowerShell 运行图、心流难度调参曲线、教学反馈小游戏计划、游戏运行记录、代码、项目、练习与总结 | 已完成 |
| 图片居中且有图注 | 正文 25 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片内部不堆解释文字 | 整理图不新增解释性长文字，说明放在正文和图注；真实历史图、心理学素材和脚本生成成果图保留自身内容 | 已完成 |
| 故事与知识点穿插 | Tennis for Two 对应交互起点，Pong 对应反馈，Odyssey 对应家庭场景，Spacewar 对应游戏循环，Csikszentmihalyi 对应心流，Stroop 对应反应时任务，Skinner teaching machine 与反馈回路操场对应即时反馈和重试循环；路线表、核心概念和脚本导读已改成学生视角的可执行动作 | 已完成 |
| 线上开放范围统一 | 网站构建脚本保持 `PUBLIC_CHAPTER_MAX = 6`，ch07 仅作为本地后续章节整理，不推进线上开放范围 | 已完成 |
| 真实运行环境截图 | 包含本机 PyGame 窗口截图和 PowerShell 运行图 | 已完成 |
| 学以致用 | 本章项目为“关键词反应小游戏”，新增反应报告、难度调参报告、心流难度调参曲线、反馈循环卡、数据驱动调参记录、教学反馈小游戏计划、游戏运行记录和多张预览图 | 已完成 |
| 代码可检查 | 示例脚本均为 ASCII 文件名，可进行 AST 语法检查 | 已完成 |

## 当前结果

- 正文字符数：19563
- 正文图片引用数：25
- manifest 素材数：41
- 本章代码清单项：11
- Markdown 图片语法数量：0
- 图注数量：25

## 运行结果

本机已运行：

```bash
python code/ch07/01_pygame_check.py
python code/ch07/03_score_model.py
python code/ch07/04_make_reaction_report.py
python code/ch07/05_make_game_balance_report.py
python code/ch07/06_make_game_feedback_loop.py
python code/ch07/07_make_flow_tuning_curve.py
python code/ch07/08_make_data_driven_tuning.py
python code/ch07/09_make_teaching_feedback_game.py
python code/ch07/10_make_game_runtime_evidence.py
```

生成文件：

- `reports/ch07_reaction_report.md`
- `reports/ch07_reaction_report_preview.png`
- `reports/ch07_game_balance_report.md`
- `output/ch07_game_balance_preview.png`
- `reports/ch07_game_feedback_loop.md`
- `output/ch07_game_feedback_loop.png`
- `reports/ch07_flow_tuning_curve.md`
- `output/ch07_flow_tuning_curve.png`
- `output/ch07_data_driven_tuning.json`
- `reports/ch07_data_driven_tuning.md`
- `output/ch07_data_driven_tuning.png`
- `output/ch07_teaching_feedback_game.json`
- `reports/ch07_teaching_feedback_game.md`
- `output/ch07_teaching_feedback_game.png`
- `reports/ch07_game_runtime_evidence.md`
- `output/ch07_game_runtime_evidence.png`

## 检查动作

- 运行 `python scripts/generate_ch07_visuals.py`，重新生成 25 张正式图片。
- 运行 `python scripts/check_links.py`，确认 Markdown 图片链接有效。
- 对 `code/ch07/*.py` 与 `scripts/*.py` 做 AST 语法检查。
- 用 PIL 打开所有 PNG/JPG/GIF 图片。
- 生成临时总览图检查构图与排版，确认后删除临时文件。
- 全书一致性扫描：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个 PIL 图片错误，0 个临时文件残留。

当前补充检查结果：

- `scripts/check_links.py`：通过，检查 25 个本地图片引用
- Python 语法检查：通过，AST 覆盖 12 个 `.py` 文件
- 图片 PIL 打开检查：通过，41 张图片均可打开
- 学生视角语言检查：通过，路线表、核心概念和脚本导读已改成可执行、可观察的游戏任务
- 运行脚本：`01_pygame_check.py`、`03_score_model.py`、`04_make_reaction_report.py`、`05_make_game_balance_report.py`、`06_make_game_feedback_loop.py`、`07_make_flow_tuning_curve.py`、`08_make_data_driven_tuning.py`、`09_make_teaching_feedback_game.py`、`10_make_game_runtime_evidence.py` 均通过，其中运行记录显示 `14/14 ready`
- 临时总览图人工检查：通过，新增游戏运行记录图居中且无越界；检查后已删除临时图
