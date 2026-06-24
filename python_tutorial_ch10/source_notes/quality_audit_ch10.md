# 第10章质量检查记录

检查日期：2026-06-16

## 检查范围

- `chapters/ch10_office_automation.md`
- `assets/ch10/`
- `assets/ch10/web/`
- `code/ch10/`
- `input/`
- `reports/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch10.md`

## 目标对照

| 需求 | 当前记录 | 状态 |
| --- | --- | --- |
| 精简与 ch0 重复内容 | 正文聚焦办公自动化任务，不重复启动章工作区总论 | 已完成 |
| 增加图文叙事 | 新增 Margaret Hamilton、Bletchley Park、Xerox Alto、VisiCalc、Ebbinghaus 遗忘曲线、办公自动化历史脉络图和结课成果档案等故事段落 | 已完成 |
| 增加真实运行环境截图 | 保留 PyCharm 解释器配置图、本机 PowerShell 运行截图和最终运行记录图 | 已完成 |
| 增加真实历史/心理学图片 | 正文新增办公自动化历史脉络图，并保留 Hollerith、打字机、Margaret Hamilton、Bletchley Park、Xerox Alto、VisiCalc、Ebbinghaus 等素材 | 已完成 |
| 减少流程图堆叠 | 正文 24 张图中以真实照片、真实软件截图、历史脉络合成图和脚本生成成果图为主 | 已完成 |
| 图片居中且有图注 | 正文 24 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片内部不堆解释文字 | 故事与说明写在 Markdown 中，生成概念图不加解释性长文字 | 已完成 |
| 办公自动化可运行 | 脚本生成 CSV、Markdown、Word、Excel、PPT、报告预览、Excel 预览、成果索引、全书课程作品集、结课展示墙、结课成果档案、成果记录、zip 成果包、成果包目录清单和最终运行记录 | 已完成 |
| 学生视角语言 | 模板故事、成果整理场景、项目结构和复盘迁移已改成学生自己的报告整理任务，减少“课堂/教学”对象错位 | 已完成 |
| 代码可检查 | 本章 11 个代码脚本与 2 个工具脚本可进行 AST 语法检查 | 已完成 |

## 当前结果

- 正文字符数：21447
- 正文图片引用数：24
- manifest 素材数：42
- 本章代码文件数：12，其中 Python 脚本 11 个
- Markdown 图片语法数量：0
- 图注数量：24

## 运行结果

本机已运行：

```bash
python code/ch10/01_make_report_data.py
python code/ch10/02_generate_markdown_report.py
python code/ch10/03_optional_docx_hint.py
python code/ch10/04_generate_office_pack.py
python code/ch10/05_generate_delivery_index.py
python code/ch10/06_make_excel_preview.py
python code/ch10/08_make_course_portfolio.py
python code/ch10/09_make_final_showcase_board.py
python code/ch10/07_make_delivery_package.py
python code/ch10/10_make_delivery_package_manifest.py
python code/ch10/11_make_final_runtime_evidence.py
```

生成文件：

- `input/report_data.csv`
- `reports/final_report.md`
- `reports/final_report.docx`
- `reports/final_report.xlsx`
- `reports/final_slides.pptx`
- `reports/final_report_preview.png`
- `reports/delivery_index.md`
- `reports/delivery_index_preview.png`
- `reports/excel_workbook_preview.png`
- `reports/course_portfolio.csv`
- `reports/course_portfolio.md`
- `reports/course_portfolio_preview.png`
- `reports/final_showcase_board.md`
- `reports/final_showcase_board.png`
- `reports/capstone_handoff_dossier.md`
- `reports/capstone_handoff_dossier.png`
- `reports/delivery_receipt.md`
- `reports/delivery_receipt_preview.png`
- `reports/ch10_delivery_package.zip`
- `reports/delivery_package_manifest.md`
- `reports/delivery_package_manifest.png`
- `reports/final_runtime_evidence.md`
- `reports/final_runtime_evidence.png`
- `assets/ch10/web/capstone_handoff_dossier.png`
- `assets/ch10/web/final_runtime_evidence.png`

## 检查命令

```bash
python scripts/generate_ch10_visuals.py
python scripts/check_links.py
```

语法、图片和清单检查：

```bash
@'
from pathlib import Path
from PIL import Image
import ast, json, re
root = Path.cwd()
text = (root / "chapters/ch10_office_automation.md").read_text(encoding="utf-8")
assert len(re.findall(r"<img\b", text)) == 24
assert len(re.findall(r"<figcaption>", text)) == 24
assert not re.findall(r"!\[[^\]]*\]\(", text)
for py in list((root / "code").rglob("*.py")) + list((root / "scripts").rglob("*.py")):
    ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
for img in (root / "assets").rglob("*"):
    if img.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
        with Image.open(img) as im:
            im.verify()
data = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
assert data["chapter"]["character_count"] == len(text)
assert data["chapter"]["image_refs"] == 24
assert data["chapter"]["asset_count"] == 42
assert data["validation"]["figcaption_count"] == 24
print("ch10 quality audit OK")
'@ | python -
```

## 本轮补充检查

- 新增 `08_make_course_portfolio.py`，生成 `reports/course_portfolio.csv`、`reports/course_portfolio.md` 和 `reports/course_portfolio_preview.png`。
- 新增正式正文图 `assets/ch10/ch10_course_portfolio_preview.png`，并在 10.16 节加入“全书作品集”图文段落。
- 增强 `09_make_final_showcase_board.py`，生成 `reports/final_showcase_board.md`、`reports/final_showcase_board.png`、`reports/capstone_handoff_dossier.md` 和 `reports/capstone_handoff_dossier.png`。
- 新增正式正文图 `assets/ch10/ch10_final_showcase_board.png` 和 `assets/ch10/ch10_capstone_handoff_dossier.png`，并在 10.17 节加入“结课展示墙”和“结课成果档案”图文段落。
- 新增 `10_make_delivery_package_manifest.py`，读取 `reports/ch10_delivery_package.zip`，生成 `reports/delivery_package_manifest.md` 和 `reports/delivery_package_manifest.png`。
- 新增正式正文图 `assets/ch10/ch10_delivery_package_manifest.png`，并在 10.15 节加入“成果包目录清单”图文段落，用于核对 zip 包内文件、类型和大小。
- 新增 `11_make_final_runtime_evidence.py`，生成 `reports/final_runtime_evidence.md`、`reports/final_runtime_evidence.png` 和 `assets/ch10/web/final_runtime_evidence.png`。
- 新增正式正文图 `assets/ch10/ch10_final_runtime_evidence.png`，并在 10.17 节加入“最终运行记录”图文段落，用于核对 CSV、Word、Excel、PPT、zip、作品集、展示墙和结课成果档案是否齐全；当前结果为 `14/14 ready`。
- `07_make_delivery_package.py` 已把课程作品集、结课展示墙和结课成果档案文件纳入 `reports/ch10_delivery_package.zip`，并修复 14 个成果文件条目时的记录图底部压行问题。
- 临时总览图人工检查：通过，新增结课成果档案图、成果记录图和最终运行记录图无明显错位、压行或越界；检查后已删除临时总览图。
- 全书一致性扫描：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个 PIL 图片错误，0 个临时文件残留。

当前补充检查结果：

- `scripts/check_links.py`：通过，检查 24 个本地图片引用
- Python 语法检查：通过，AST 覆盖 13 个 `.py` 文件，包括 11 个代码脚本和 2 个检查/生成脚本
- 图片 PIL 打开检查：通过，42 张 PNG/JPG 图片均可打开
- 学生视角语言检查：通过，模板故事、成果整理场景、项目结构和复盘迁移已改成学生自己的报告整理任务
- 新增章节结构检查：通过，正文包含 `[TOC]`、本章导读、分区导航和五个大部分
- 新增办公史脉络图检查：通过，`ch10_office_history_gallery.png` 只使用图片、编号和连接线，没有解释性长文字越界
- 临时总览图人工检查：通过，24 张正文图居中且无明显越界；检查后已删除临时图
