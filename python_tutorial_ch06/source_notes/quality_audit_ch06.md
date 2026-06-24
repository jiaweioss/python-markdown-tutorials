# 第6章质量检查记录

检查日期：2026-06-23

## 检查范围

- `chapters/ch06_data_analysis_visualization.md`
- `assets/ch06/`
- `assets/ch06/web/`
- `code/ch06/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch06.md`

## 目标对照

| 需求 | 当前记录 | 状态 |
| --- | --- | --- |
| 结构清晰 | 正文已重写为 `[TOC]`、五大分区、多级标题，分区边界清楚 | 已完成 |
| 图片有意义 | 正文引用 27 张正式图，覆盖路线、最小链路、运行记录、仪表盘、异常值、复习计划、检查，以及数据可视化史与人物故事 | 已完成 |
| 去掉杂乱堆图 | 历史图片与人物素材重新进入正文，但按概念分散穿插，不集中堆放 | 已完成 |
| 图中文字自然 | `04` 到 `11` 输出脚本的图中文字已改成中文标签，去掉机械英文状态词 | 已完成 |
| 中文不溢出不变方块 | 已修复生成脚本和运行记录脚本的字体优先级，抽检核心图、最小示例图、项目成果图和运行记录图 | 已完成 |
| 真实运行环境记录 | `ch06_powershell_analysis_run.png` 展示运行链路，`ch06_analysis_runtime_evidence.png` 展示 16 个运行产物检查结果 | 已完成 |
| 代码可复现 | `01_make_sample_csv.py` 到 `11_make_analysis_runtime_evidence.py` 已本机运行通过 | 已完成 |
| 学以致用 | 本章项目产出 CSV、仪表盘、图表改造、异常值诊断、记忆复习计划、跨章节对象包分析、图表审美诊所和运行记录总览 | 已完成 |

## 当前结果

- 正文字符数：16184
- 正文图片引用数：27
- 正文图注数：27
- Markdown 图片语法数量：0
- manifest 素材数：45
- 本章 code 文件数：12
- 运行记录：`16/16 就绪`

## 运行结果

本机已运行：

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
```

生成与同步重点：

- `output/ch06_learning_dashboard.png`
- `assets/ch06/web/ch06_learning_dashboard_output.png`
- `output/ch06_anscombe_quartet.png`
- `assets/ch06/web/ch06_anscombe_quartet_output.png`
- `reports/ch06_analysis_runtime_evidence.md`
- `output/ch06_analysis_runtime_evidence.png`
- `assets/ch06/web/ch06_analysis_runtime_evidence.png`
- `assets/ch06/ch06_analysis_runtime_evidence.png`

## 检查命令

```bash
python scripts/check_links.py
```

语法、图片和清单检查：

```bash
@'
from pathlib import Path
from PIL import Image
import ast, json, re
root = Path.cwd()
text = (root / "chapters/ch06_data_analysis_visualization.md").read_text(encoding="utf-8")
assert len(text) == 16184
assert len(re.findall(r"<img\b", text)) == 27
assert len(re.findall(r"<figcaption>", text)) == 27
assert not re.findall(r"!\[[^\]]*\]\(", text)
for py in list((root / "code").rglob("*.py")) + list((root / "scripts").rglob("*.py")):
    ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
for img in (root / "assets").rglob("*"):
    if img.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
        with Image.open(img) as im:
            im.verify()
data = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
assert data["chapter"]["character_count"] == len(text)
assert data["chapter"]["image_refs"] == 27
assert data["chapter"]["asset_count"] == 45
assert data["chapter"]["code_count"] == 12
assert data["validation"]["figcaption_count"] == 27
print("ch06 quality audit OK")
'@ | python -
```

## 当前补充检查结果

- 临时联系表人工检查：通过，正文引用的 27 张图排布清楚，关键图片已全尺寸抽检。
- 字体问题复查：通过，`ch06_minimal_demo.png` 与 `ch06_analysis_runtime_evidence.png` 的中文不再显示为方块字。
- 项目成果图复查：通过，`ch06_project_dashboard.png` 中右侧标签不再被路径文字挤断。
- 最终命令复核：通过，`scripts/check_links.py` 检查 27 个本地图片引用；13 个 Python 文件通过不落盘语法检查；45 个素材图片通过 PIL 打开检查；临时联系表已清理。
