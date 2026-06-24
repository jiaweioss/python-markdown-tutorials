# 第9章质量检查记录

检查日期：2026-06-15

## 检查范围

- `chapters/`
- `assets/ch09/`
- `code/ch09/`
- `output/`
- `reports/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch09.md`

## 目标对照

| 需求 | 当前记录 | 状态 |
| --- | --- | --- |
| 符合 ch0/ch1 图文标准 | 正文约 20182 字，包含 `[TOC]`、本章导读、五个大部分、摄影史、数字图像史、Edwin Land、图像处理人文脉络图、真实风景图、NASA 科学图像、Helmholtz、Adelson 棋盘阴影错觉、处理前后对比、视觉感知实验、图像质量总览、处理故事板、视觉记录档案、运行记录总览、ch8 图像素材入库体检、PowerShell 运行图、代码、项目、练习与总结 | 已完成 |
| 图片居中且有图注 | 正文 25 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片内部不堆解释文字 | 整理图不新增解释性长文字，说明放在正文和图注；真实历史图、科学图像、人物照和脚本生成成果图保留自身内容；新增图像质量总览图内部无解释文字 | 已完成 |
| 真实运行环境截图 | PowerShell 运行图展示图像处理脚本的运行路径与生成结果；新增 PowerShell 风格运行记录总览检查 16 项关键产物 ready 状态；新增脚本在本轮命令行验证中覆盖 | 已完成 |
| 故事与知识点穿插 | Niépce 对应图像记录，早期数字扫描对应像素表示，Land 对应颜色判断，NASA 科学图像对应科研表达边界，Helmholtz 和 Adelson 对应视觉感知；路线表、核心概念和项目步骤已改成学生视角的可执行图像处理动作 | 已完成 |
| 学以致用 | 本章项目为“学习卡片配图处理器”，新增图像处理报告、视觉感知小实验、图像质量检查总览、处理故事板、视觉记录档案、运行记录总览、ch8 图像素材入库体检和预览图 | 已完成 |
| 代码可检查 | 示例脚本均为 ASCII 文件名，可进行 AST 语法检查 | 已完成 |

## 当前结果

- 正文字符数：20182
- 正文图片引用数：25
- manifest 素材数：41
- 本章代码文件数：12，其中 Python 脚本 11 个
- Markdown 图片语法数量：0
- 图注数量：25

## 运行结果

本机已运行：

```bash
python code/ch09/01_create_demo_image.py
python code/ch09/02_resize_grayscale.py
python code/ch09/04_real_photo_before_after.py
python code/ch09/05_make_image_processing_report.py
python code/ch09/06_make_visual_perception_lab.py
python code/ch09/07_make_image_quality_contact_sheet.py
python code/ch09/10_make_processing_storyboard.py
python code/ch09/08_make_ch08_image_intake.py
python code/ch09/09_make_visual_evidence_archive.py
python code/ch09/11_make_image_runtime_evidence.py
```

生成文件：

- `output/demo_card_image.png`
- `output/demo_card_image_gray.png`
- `output/fronalpstock_before_after.png`
- `reports/ch09_image_processing_report.md`
- `reports/ch09_image_processing_report_preview.png`
- `reports/ch09_visual_perception_lab.md`
- `output/ch09_visual_perception_lab.png`
- `reports/ch09_image_quality_contact_sheet.md`
- `output/ch09_image_quality_contact_sheet.png`
- `reports/ch09_processing_storyboard.md`
- `output/ch09_processing_storyboard.png`
- `output/ch09_ch08_image_intake.json`
- `reports/ch09_ch08_image_intake.md`
- `output/ch09_ch08_image_intake.png`
- `reports/ch09_visual_evidence_archive.md`
- `output/visual_evidence_archive.png`
- `reports/ch09_image_runtime_evidence.md`
- `output/ch09_image_runtime_evidence.png`
- `assets/ch09/web/ch09_image_runtime_evidence.png`

## 检查动作

- 运行 `python scripts/generate_ch09_visuals.py`，重新生成 25 张正式图片。
- 运行 `python scripts/check_links.py`，确认 Markdown 图片链接有效。
- 对 `code/ch09/*.py` 与 `scripts/*.py` 做 AST 语法检查。
- 用 PIL 打开所有 PNG/JPG/GIF 图片。
- 生成临时总览图检查构图与排版，确认后删除临时文件。
- `scripts/check_links.py`：通过，检查 25 个本地图片引用。
- Python 语法检查：通过，AST 覆盖 13 个 `.py` 文件，包括 11 个代码脚本和 2 个检查/生成脚本。
- 图片 PIL 打开检查：通过，41 张 PNG/JPG/GIF 图片均可打开。
- 运行全书交叉检查：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图片/图注数量不一致，0 个 manifest 字数或图片计数错配，0 个 PIL 图片错误，0 个临时文件残留。

当前补充检查结果：

- `scripts/check_links.py`：通过，检查 25 个本地图片引用
- Python 语法检查：通过，AST 覆盖 13 个 `.py` 文件，包括 11 个代码脚本和 2 个检查/生成脚本
- 图片 PIL 打开检查：通过，41 张 PNG/JPG/GIF 图片均可打开
- 学生视角语言检查：通过，路线表、核心概念、心理学/科研图片连接和项目步骤已改成可执行、可观察的图像处理任务
- 新增章节结构检查：通过，正文包含 `[TOC]`、本章导读、分区导航和五个大部分
- 新增人文脉络图检查：通过，`ch09_human_context_gallery.png` 只使用图片、编号和连接线，没有解释性长文字越界
- 临时总览图人工检查：通过，25 张正文图居中且无明显越界；检查后已删除临时图
