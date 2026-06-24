# 第7章来源记录

## 主来源

- `第七章_PyGame游戏开发2025.pptx`

本章依据原课件主题重构为《PyGame 游戏开发》，并延续“科研卡片工厂”主线。MATLAB 教材仅作为“讲故事、放图片、做任务、跑代码、看成果”的组织方式参考，不迁移 MATLAB 技术内容。

## 互联网与真实运行素材

本章互联网图片全部先保存到 `assets/ch07/web/`，再由 `scripts/generate_ch07_visuals.py` 整理成正式教材图。整理图内部不新增解释文字，说明统一写在 Markdown 正文和图注中。

| 用途 | 原图 | 本地原图 | 正式图片 | 来源、作者与授权 |
| --- | --- | --- | --- | --- |
| 早期交互游戏 | Tennis for Two - Modern recreation | `assets/ch07/web/tennis_for_two_recreation.jpg` | `assets/ch07/ch07_tennis_for_two_story.png` | Wikimedia Commons |
| 即时反馈与街机游戏 | Atari Pong arcade game cabinet | `assets/ch07/web/atari_pong_arcade_game_cabinet.jpg` | `assets/ch07/ch07_pong_arcade_story.png` | Wikimedia Commons |
| 游戏进入家庭客厅 | Magnavox-Odyssey-Console-Set | `assets/ch07/web/magnavox_odyssey_console_set.jpg` | `assets/ch07/ch07_magnavox_odyssey_story.png` | Wikimedia Commons；Evan-Amos；Public domain |
| 游戏循环历史 | Spacewar!/PDP-1 | `assets/ch07/web/spacewar_pdp1.jpg` | `assets/ch07/ch07_spacewar_pdp1_story.png` | Wikimedia Commons |
| 心流与游戏体验 | Mihaly Csikszentmihalyi | `assets/ch07/web/mihaly_csikszentmihalyi.jpg` | `assets/ch07/ch07_csikszentmihalyi_flow_story.png` | Wikimedia Commons；Ehirsh；Public domain |
| 反应时任务 | Stroop effect example | `assets/ch07/web/stroop_effect_example.png` | `assets/ch07/ch07_stroop_reaction_story.png` | Wikimedia Commons |
| 即时反馈与教学机器 | Skinner teaching machine 01 | `assets/ch07/web/skinner_teaching_machine.jpg` | `assets/ch07/ch07_skinner_teaching_machine_story.png` | Wikimedia Commons |

原始链接：

- https://commons.wikimedia.org/wiki/File:Tennis_for_Two_-_Modern_recreation.jpg
- https://commons.wikimedia.org/wiki/File:Atari_Pong_arcade_game_cabinet.jpg
- https://commons.wikimedia.org/wiki/File:Magnavox-Odyssey-Console-Set.jpg
- https://commons.wikimedia.org/wiki/File:Spacewar!-PDP-1-20070512.jpg
- https://commons.wikimedia.org/wiki/File:Mihaly_Csikszentmihalyi.jpg
- https://commons.wikimedia.org/wiki/File:Stroop_effect_example.png
- https://commons.wikimedia.org/wiki/File:Skinner_teaching_machine_01.jpg

## 真实运行与生成素材

- `assets/ch07/web/pygame_ch07_reaction_window.png`：本机运行 `02_reaction_game_skeleton.py` 后截取的 PyGame 窗口。
- `assets/ch07/web/powershell_ch07_pygame_run.png`：本机运行 `01_pygame_check.py`、`03_score_model.py` 和 `04_make_reaction_report.py` 后整理的运行图。
- `assets/ch07/web/ch07_reaction_report_preview.png`：本机运行 `04_make_reaction_report.py` 生成的反应报告预览图。
- `assets/ch07/web/ch07_game_balance_preview.png`：本机运行 `05_make_game_balance_report.py` 生成的小游戏难度调参预览图。
- `assets/ch07/web/ch07_game_feedback_loop.png`：本机运行 `06_make_game_feedback_loop.py` 生成的游戏反馈循环预览图。
- `assets/ch07/web/ch07_flow_tuning_curve.png`：本机运行 `07_make_flow_tuning_curve.py` 生成的心流难度调参曲线。
- `assets/ch07/web/ch07_data_driven_tuning.png`：本机运行 `08_make_data_driven_tuning.py` 生成的数据驱动调参记录。
- `assets/ch07/web/ch07_teaching_feedback_game.png`：本机运行 `09_make_teaching_feedback_game.py` 生成的教学反馈小游戏计划图。
- `assets/ch07/web/ch07_game_runtime_evidence.png`：本机运行 `10_make_game_runtime_evidence.py` 生成的游戏运行记录图。
- `reports/ch07_game_runtime_evidence.md`：游戏运行记录 Markdown 报告，检查本章 14 个关键产物。
- `output/ch07_game_runtime_evidence.png`：游戏运行记录输出图。

## 生成素材

本章包含 25 张正文正式图片、7 张互联网原图/素材、1 张本机 PyGame 窗口截图、1 张本机 PowerShell 运行图、1 张无文字反馈回路类比图和 8 张脚本生成预览/记录图。

正式图片：

- `ch07_cover.png`
- `ch07_tennis_for_two_story.png`
- `ch07_pong_arcade_story.png`
- `ch07_magnavox_odyssey_story.png`
- `ch07_story_scene.png`
- `ch07_roadmap.png`
- `ch07_core_metaphor.png`
- `ch07_spacewar_pdp1_story.png`
- `ch07_csikszentmihalyi_flow_story.png`
- `ch07_minimal_demo.png`
- `ch07_pygame_window_run.png`
- `ch07_powershell_pygame_run.png`
- `ch07_psychology_link.png`
- `ch07_stroop_reaction_story.png`
- `ch07_skinner_teaching_machine_story.png`
- `ch07_feedback_playground_loop.png`
- `ch07_pitfall_map.png`
- `ch07_project_dashboard.png`
- `ch07_reaction_report_preview.png`
- `ch07_game_balance_preview.png`
- `ch07_flow_tuning_curve.png`
- `ch07_game_feedback_loop.png`
- `ch07_data_driven_tuning.png`
- `ch07_teaching_feedback_game.png`
- `ch07_game_runtime_evidence.png`

图片内部不新增解释性长文字，说明统一写在 Markdown 正文和图注中。真实历史图、心理学素材、软件截图和脚本生成报告图保留素材自身内容。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 每张图片都有 `<figcaption>`。
- 故事图片穿插在对应知识点附近，不集中堆在开头。
- 示例代码与项目任务围绕“科研卡片工厂”连续推进。
- 路线表、核心概念和脚本导读使用学生视角，直接说明要运行、观察和完成的动作。
- 正文已补充 `[TOC]`、本章导读、分区导航和五个部分，确保 ch07 本地内容达到 ch06 同类结构标准，但不进入当前线上开放范围。
