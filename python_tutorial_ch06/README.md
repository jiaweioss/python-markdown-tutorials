# Python Markdown 教程书：第6章

本包是第6章《数据分析与可视化》的 Markdown 教材交付。

## 内容

- `chapters/`：教材正文。
- `assets/ch06/`：本章正式图片，全部本地化、居中显示，并配有图注。
- `assets/ch06/web/`：真实历史图片、本机 PowerShell 运行图和代码生成图表原图。
- `code/ch06/`：可运行示例代码。
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查。
- `scripts/generate_ch06_visuals.py`：本章图片生成与整理脚本。
- `source_notes/`：来源记录和质量验收。
- `manifest.json`：交付清单。

## 本章项目

学习卡片统计仪表盘：读取学习记录 CSV，统计主题数量、完成率和反应时，生成仪表盘、Anscombe 四重奏、图表改造对比、异常值诊断、记忆复习计划、跨章节对象包分析、图表审美诊所和最终运行证据总览。

## 本轮增强

- 正文扩展到 27 张居中图片，所有图片均使用 `<figure>` 与 `<figcaption>`。
- 保留 Florence Nightingale、John Snow、William Playfair、Minard、W.E.B. Du Bois、Anscombe、Hermann Ebbinghaus、Hans Rosling 等图文故事素材。
- 新增 `11_make_analysis_runtime_evidence.py`，生成 `reports/ch06_analysis_runtime_evidence.md`、`output/ch06_analysis_runtime_evidence.png` 和 `assets/ch06/web/ch06_analysis_runtime_evidence.png`。
- 新增正式配图 `assets/ch06/ch06_analysis_runtime_evidence.png`，作为图6-27，用于展示本章数据分析项目的全链路运行证据。
- 重新运行 `01_make_sample_csv.py` 到 `11_make_analysis_runtime_evidence.py`，确认运行证据为 `16/16 ready`。
- 重新运行 `scripts/generate_ch06_visuals.py`，确认正式图片总数为 27。
- 继续修正文口吻：把后台式“本教程”说明改成学生正在完成的数据分析任务，把路线表、核心概念列表和前三个脚本导读从模板句改成具体的数据读取、统计和分组动作。

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

## 验收状态

- 正文字符数：20169
- 正文图片引用数：27
- 图注数：27
- 素材图片数：45
- code 文件数：12
- Python 脚本运行：`01` 到 `11` 已通过
- 链接检查：已通过
- 运行证据：`16/16 ready`
