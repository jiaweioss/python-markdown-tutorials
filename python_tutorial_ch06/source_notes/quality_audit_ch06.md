# 第6章质量验收记录

验收日期：2026-06-15

## 验收范围

- `chapters/ch06_data_analysis_visualization.md`
- `assets/ch06/`
- `assets/ch06/web/`
- `code/ch06/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch06.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 图文并茂、故事穿插 | 正文包含数据可视化历史、心理学记忆曲线、真实运行图、Python 生成图表、异常值诊断、跨章节分析和项目复盘 | 已完成 |
| 图片居中且有图注 | 正文 27 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片内部不堆解释文字 | 新增图片只呈现运行证据与文件清单，解释放在正文和图注；历史图与运行截图保留自身内容 | 已完成 |
| 学生阅读口吻 | 已去掉后台式“本教程”说明，路线表、核心概念列表和脚本导读改成学生可直接观察和执行的数据分析动作 | 已完成 |
| 真实运行环境证据 | `ch06_powershell_analysis_run.png` 展示 PowerShell 运行链路，`ch06_analysis_runtime_evidence.png` 展示 16 个运行产物检查结果 | 已完成 |
| 代码可复现 | `01_make_sample_csv.py` 到 `11_make_analysis_runtime_evidence.py` 已本机运行通过 | 已完成 |
| 学以致用 | 本章项目产出 CSV、仪表盘、图表改造、异常值诊断、记忆复习计划、跨章节对象包分析、图表审美诊所和运行证据总览 | 已完成 |

## 当前结果

- 正文字符数：20169
- 正文图片引用数：27
- 正文图注数：27
- Markdown 图片语法数量：0
- manifest 素材数：45
- 本章 code 文件数：12
- 运行证据：`16/16 ready`

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

新增生成文件：

- `reports/ch06_analysis_runtime_evidence.md`
- `output/ch06_analysis_runtime_evidence.png`
- `assets/ch06/web/ch06_analysis_runtime_evidence.png`
- `assets/ch06/ch06_analysis_runtime_evidence.png`

## 验收命令

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

## 当前补充验收结果

- `scripts/check_links.py`：通过，检查 27 个本地图片引用。
- Python 语法检查：通过，AST 覆盖全书 129 个 Python 文件，其中 107 个为 `code/` 下的 Python 脚本。
- 图片 PIL 打开检查：通过，全书素材图均可打开。
- 临时总览图人工检查：通过，历史数据图、真实运行截图、仪表盘、图表改造、异常值诊断、图表审美诊所和运行证据总览无明显越界、错位或长文字挤压；检查图保存在系统临时目录，未写入项目资产。
- 全书一致性扫描：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个临时文件残留。
