# 第9章来源记录

## 主来源

- `第九章_Python图像处理2025.pptx`

本章依据原课件主题重构为《Python 图像处理》，并延续“科研卡片工厂”主线。MATLAB 教材仅作为“讲故事、放图片、做任务、跑代码、看成果”的组织方式参考，不迁移 MATLAB 技术内容。

## 互联网与真实运行素材

本章互联网图片全部先保存到 `assets/ch09/web/`，再由 `scripts/generate_ch09_visuals.py` 整理成正式教材图。整理图内部不新增解释文字，说明统一写在 Markdown 正文和图注中。

| 用途 | 原图 | 本地原图 | 正式图片 | 来源与授权 |
| --- | --- | --- | --- | --- |
| 摄影史 | View from the Window at Le Gras | `assets/ch09/web/niepce_window_le_gras.jpg` | `assets/ch09/ch09_niepce_photo_story.png` | Wikimedia Commons |
| 数字图像史 | NBS first scan image restored | `assets/ch09/web/first_digital_scan_nist.jpg` | `assets/ch09/ch09_first_digital_scan_story.png` | Wikimedia Commons |
| 颜色与视觉判断 | Edwin H. Land, founder, Polaroid (cropped) | `assets/ch09/web/edwin_land_polaroid_cropped.jpg` | `assets/ch09/ch09_edwin_land_color_story.png` | Wikimedia Commons |
| 图像处理人文脉络 | 既有摄影史、数字扫描、颜色、视觉心理学、错觉和科学图像素材 | `assets/ch09/web/*.jpg` | `assets/ch09/ch09_human_context_gallery.png` | 由本章既有本地来源素材合成，不新增互联网来源 |
| 真实处理素材 | Fronalpstock big | `assets/ch09/web/fronalpstock_sample.jpg` | `assets/ch09/ch09_real_photo_source.png` | Wikimedia Commons |
| 科学图像表达 | Pillars of Creation | `assets/ch09/web/pillars_of_creation.jpg` | `assets/ch09/ch09_pillars_science_image_story.png` | Wikimedia Commons / NASA |
| 视觉心理学 | Hermann von Helmholtz 1894 | `assets/ch09/web/hermann_von_helmholtz_1894.jpg` | `assets/ch09/ch09_helmholtz_perception_story.png` | Wikimedia Commons |
| 视觉错觉与亮度判断 | Checker shadow illusion | `assets/ch09/web/checker_shadow_illusion.jpg` | `assets/ch09/ch09_checker_shadow_illusion_story.png` | MIT Perceptual Science Group；Edward H. Adelson；页面说明图片可自由复制和分发 |

原始链接：

- https://commons.wikimedia.org/wiki/File:View_from_the_Window_at_Le_Gras,_Joseph_Nic%C3%A9phore_Ni%C3%A9pce.jpg
- https://commons.wikimedia.org/wiki/File:NBSFirstScanImageRestored.jpg
- https://commons.wikimedia.org/wiki/File:Edwin_H._Land,_founder,_Polaroid_(cropped).jpg
- https://commons.wikimedia.org/wiki/File:Fronalpstock_big.jpg
- https://commons.wikimedia.org/wiki/File:Pillars_of_Creation.jpeg
- https://commons.wikimedia.org/wiki/File:Hermann_von_Helmholtz_1894.jpg
- https://persci.mit.edu/gallery/checkershadow/

## 真实运行与生成素材

- `assets/ch09/web/fronalpstock_before_after.png`：本机运行 `04_real_photo_before_after.py` 后生成的真实照片处理结果。
- `assets/ch09/web/ch09_image_processing_report_preview.png`：本机运行 `05_make_image_processing_report.py` 后生成的图像处理报告预览图。
- `assets/ch09/web/ch09_visual_perception_lab.png`：本机运行 `06_make_visual_perception_lab.py` 后生成的视觉感知小实验图。
- `assets/ch09/web/ch09_image_quality_contact_sheet.png`：本机运行 `07_make_image_quality_contact_sheet.py` 后生成的无文字图像质量检查总览。
- `assets/ch09/web/ch09_ch08_image_intake.png`：本机运行 `08_make_ch08_image_intake.py` 后生成的 ch8 图像素材入库体检单。
- `assets/ch09/web/ch09_processing_storyboard.png`：本机运行 `10_make_processing_storyboard.py` 后生成的图像处理故事板。
- `assets/ch09/web/visual_evidence_archive.png`：本机运行 `09_make_visual_evidence_archive.py` 后生成的视觉证据档案总览。
- `assets/ch09/web/ch09_image_runtime_evidence.png`：本机运行 `11_make_image_runtime_evidence.py` 后生成的图像处理运行证据总览。
- `assets/ch09/web/powershell_ch09_image_processing_run.png`：本机运行图像处理脚本后整理的 PowerShell 运行图。

## 生成素材

本章包含 25 张正文正式图片、7 张互联网原图/素材、1 张真实照片处理结果、1 张本机 PowerShell 运行图、1 张由既有素材合成的人文脉络图和 7 张脚本生成预览/证据图。

正式图片：

- `ch09_cover.png`
- `ch09_niepce_photo_story.png`
- `ch09_first_digital_scan_story.png`
- `ch09_edwin_land_color_story.png`
- `ch09_human_context_gallery.png`
- `ch09_story_scene.png`
- `ch09_roadmap.png`
- `ch09_core_metaphor.png`
- `ch09_real_photo_source.png`
- `ch09_pillars_science_image_story.png`
- `ch09_minimal_demo.png`
- `ch09_before_after_result.png`
- `ch09_powershell_image_run.png`
- `ch09_image_runtime_evidence.png`
- `ch09_psychology_link.png`
- `ch09_helmholtz_perception_story.png`
- `ch09_checker_shadow_illusion_story.png`
- `ch09_pitfall_map.png`
- `ch09_project_dashboard.png`
- `ch09_image_processing_report_preview.png`
- `ch09_visual_perception_lab.png`
- `ch09_image_quality_contact_sheet.png`
- `ch09_processing_storyboard.png`
- `ch09_ch08_image_intake.png`
- `ch09_visual_evidence_archive.png`

图片内部不新增解释性长文字，说明统一写在 Markdown 正文和图注中。真实历史图、科学图像、人物照片和软件截图保留素材自身内容。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 每张图片都有 `<figcaption>`。
- 故事图片穿插在对应知识点附近，不集中堆在开头。
- 新增人文脉络图只使用图片、编号和连接线，不在图片内部放长段中文说明；完整解释放在正文和图注中。
- 示例代码与项目任务围绕“科研卡片工厂”连续推进。
- 路线表、核心概念和项目步骤使用学生视角，直接说明要打开、处理、比较、入库和复盘的动作。
