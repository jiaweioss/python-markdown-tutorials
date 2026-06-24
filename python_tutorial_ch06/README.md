# Python Markdown 教程书：第6章

本包是第6章《数据分析与可视化》的 Markdown 教材包。

## 内容

- `chapters/`：教材正文。
- `assets/ch06/`：本章正式图片，全部本地化、居中显示，并配有图注。
- `assets/ch06/web/`：真实历史图片、本机 PowerShell 运行图和代码生成图表原图。
- `code/ch06/`：可运行示例代码。
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查。
- `scripts/generate_ch06_visuals.py`：本章图片生成与整理脚本。
- `source_notes/`：来源记录和质量检查。
- `manifest.json`：文件清单。

## 本章项目

学习卡片统计仪表盘：读取学习记录 CSV，统计主题数量、完成率和反应时，生成仪表盘、Anscombe 四重奏、图表改造对比、异常值诊断、记忆复习计划、跨章节对象包分析、图表审美诊所和最终运行记录总览。

## 本轮增强

- 正文重写为 `[TOC]` + 五大分区 + 多级标题结构，清楚区分“CSV 到第一张图、摘要与判断、异常值与复习、项目成果、排错自查”。
- 正文保留 27 张正式图，全部使用 `<figure>` 与 `<figcaption>`；历史人物和数据可视化史素材重新进入正文，用来解释图表如何参与公共问题、记忆、判断和讲述。
- 修复 `04` 到 `11` 脚本的图中文字：去掉机械英文标签，改成自然中文；同时修正脚本从不同目录运行时的路径定位。
- 修复图像字体回退问题，避免中文出现在代码块、运行记录图中时变成方块字。
- 重新运行 `01_make_sample_csv.py` 到 `11_make_analysis_runtime_evidence.py`，确认运行记录为 `16/16 就绪`。
- 重新运行 `scripts/generate_ch06_visuals.py`，正式图片总数为 27，正文当前引用 27 张。

## 运行方式

```bash
python code/ch06/01_make_sample_csv.py
python code/ch06/02_basic_statistics.py
python code/ch06/03_optional_pandas_summary.py
python code/ch06/04_make_dashboard_chart.py
python code/ch06/05_anscombe_quartet.py
python code/ch06/06_make_chart_makeover.py
python code/ch06/07_make_outlier_diagnosis.py
python code/ch06/08_make_ch05_handoff_analysis.py
python code/ch06/09_make_memory_review_curve.py
python code/ch06/10_make_chart_style_clinic.py
python code/ch06/11_make_analysis_runtime_evidence.py
python scripts/generate_ch06_visuals.py
python scripts/check_links.py
```

## 检查状态

- 正文字符数：16184
- 正文图片引用数：27
- 图注数：27
- 素材图片数：45
- code 文件数：12
- Python 脚本运行：`01` 到 `11` 已通过
- 链接检查：已通过
- 运行记录：`16/16 就绪`
