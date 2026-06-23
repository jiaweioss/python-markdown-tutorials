# 第6章来源记录

## 主要来源

- `第六章_数据分析与可视化2025.pptx`

本章依据 ch0 的“科研卡片工厂”主线展开，主题为数据分析与可视化。MATLAB 教材仅作为“讲故事、放图片、做任务、跑代码、看成果”的组织方式参考，不迁移 MATLAB 技术内容。

## 生成素材

本章资产目录包含 27 张正式图片，均由 `scripts/generate_ch06_visuals.py` 生成或整理。当前正文引用全部 27 张正式图片；历史图、人物图和数据可视化史素材已经重新进入正文，但都贴在对应知识点附近，用 Nightingale、John Snow、Playfair、Anscombe、Minard、Du Bois、Ebbinghaus 和 Hans Rosling 解释数据分析为什么要服务判断、公共问题、记忆和讲述。

新增 `ch06_analysis_runtime_evidence.png`：由 `11_make_analysis_runtime_evidence.py` 先生成 `output/ch06_analysis_runtime_evidence.png`，复制到 `assets/ch06/web/ch06_analysis_runtime_evidence.png`，再由 `generate_ch06_visuals.py` 整理为正式正文图。它用于展示本章 CSV、图表、报告、JSON 和跨章节分析产物是否齐全。

## 互联网与真实运行素材

- Florence Nightingale 死亡原因图：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Nightingale-mortality.jpg>
- William Playfair 时间序列图：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Playfair_TimeSeries-2.png>
- Minard 拿破仑远征俄国图：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Minard.png>
- W.E.B. Du Bois 数据肖像：Wikimedia Commons / Library of Congress，Public domain  
  <https://commons.wikimedia.org/wiki/File:A_series_of_statistical_charts_illustrating_the_condition_of_the_descendants_of_former_African_slaves_now_in_residence_in_the_United_States_of_America_LCCN2013650371.jpg>
- John Snow 霍乱地图：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Snow-cholera-map-1.jpg>
- Anscombe 四重奏示意图：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Anscombe%27s_quartet_3_cropped.jpg>
- Hans Rosling 演讲照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Hans_Rosling_1.jpg>
- Hermann Ebbinghaus 肖像：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Ebbinghaus.jpg>
- PowerShell 运行图：本机运行第6章完整链路后，根据当前 `input/` 和 `output/` 真实文件列表整理生成。
- Python 生成图表：由 `04` 到 `11` 脚本读取本地数据后生成，所有输出均保存在 `output/` 或 `reports/`，并复制到 `assets/ch06/web/` 作为正式配图来源。

## 当前正文引用图片

- `ch06_cover.png`
- `ch06_roadmap.png`
- `ch06_story_scene.png`
- `ch06_nightingale_mortality_story.png`
- `ch06_snow_cholera_map_story.png`
- `ch06_minimal_demo.png`
- `ch06_powershell_analysis_run.png`
- `ch06_core_metaphor.png`
- `ch06_playfair_timeseries_story.png`
- `ch06_generated_dashboard_chart.png`
- `ch06_anscombe_quartet_output.png`
- `ch06_anscombe_quartet_story.png`
- `ch06_chart_makeover_output.png`
- `ch06_visual_check_preview.png`
- `ch06_minard_napoleon_story.png`
- `ch06_dubois_data_portrait_story.png`
- `ch06_outlier_diagnosis.png`
- `ch06_ch05_handoff_analysis.png`
- `ch06_psychology_link.png`
- `ch06_memory_review_plan.png`
- `ch06_ebbinghaus_story.png`
- `ch06_hans_rosling_story.png`
- `ch06_chart_style_clinic.png`
- `ch06_project_dashboard.png`
- `ch06_pitfall_map.png`
- `ch06_analysis_runtime_evidence.png`
- `ch06_data_detective_desk.png`

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 每张图片都有 `<figcaption>`。
- 图片中不新增解释性长文字；故事、判断和教学说明写在正文与图注中。
- 示例代码与项目任务围绕“科研卡片工厂”连续推进。
- 本轮继续做学生视角修订：正文重写为 `[TOC]`、五大分区和多级标题；历史素材重新穿插进概念讲解，结构化步骤图、证据图和验收图继续承担操作说明。
