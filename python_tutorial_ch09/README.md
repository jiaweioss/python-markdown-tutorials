# Python Markdown 教程书：第9章

本包是第9章《Python 图像处理》的 Markdown 教材交付。

## 内容

- `chapters/`：教材正文
- `assets/ch09/`：本章正式图片，全部本地化、居中显示、图注在下
- `assets/ch09/web/`：摄影史图片、数字图像史图片、人物照片、视觉错觉素材、科学图像素材、真实风景照片、处理结果图、处理故事板、视觉证据档案、ch8 素材入库体检图、PowerShell 运行图、运行证据总览和报告预览图
- `code/ch09/`：可运行示例代码
- `output/`：脚本生成的图像处理结果
- `reports/`：脚本生成的图像处理报告、视觉感知实验记录、图像质量检查记录、处理故事板报告、视觉证据档案、运行证据报告和素材入库体检单
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查
- `scripts/generate_ch09_visuals.py`：本章图片生成脚本
- `source_notes/`：来源记录和质量验收
- `manifest.json`：交付清单

## 本章项目

学习卡片配图处理器：打开图片、缩放、裁剪、转灰度、加边框，批量导出卡片配图，并生成图像处理报告、视觉感知小实验、图像质量检查总览、处理故事板、视觉证据档案、运行证据总览和 ch8 图片素材入库体检单。

## 本轮增强

- 增加 Edwin Land、Hermann von Helmholtz 等人物素材，用真实历史和视觉心理学解释颜色、感知和图像表达边界。
- 增加 Edward H. Adelson 的棋盘阴影错觉素材，把“像素值”和“人眼感受”的差异讲得更直观。
- 新增 `06_make_visual_perception_lab.py`，生成 `reports/ch09_visual_perception_lab.md` 和 `output/ch09_visual_perception_lab.png`。
- 新增 `07_make_image_quality_contact_sheet.py`，生成 `reports/ch09_image_quality_contact_sheet.md` 和 `output/ch09_image_quality_contact_sheet.png`；图片内部无解释文字，说明放在报告和正文里。
- 新增 `08_make_ch08_image_intake.py`，扫描 ch8 公开资料图片素材，生成 `reports/ch09_ch08_image_intake.md`、`output/ch09_ch08_image_intake.json` 和 `output/ch09_ch08_image_intake.png`。
- 新增 `09_make_visual_evidence_archive.py`，生成 `reports/ch09_visual_evidence_archive.md` 和 `output/visual_evidence_archive.png`，把本章关键图像处理产物集中成可复盘证据档案。
- 新增 `10_make_processing_storyboard.py`，生成 `reports/ch09_processing_storyboard.md` 和 `output/ch09_processing_storyboard.png`，把原图、灰度、裁剪、增强和卡片成品连成一条可复盘流水线。
- 更新 `09_make_visual_evidence_archive.py`，把处理故事板纳入视觉证据档案。
- 新增 `11_make_image_runtime_evidence.py`，生成 `reports/ch09_image_runtime_evidence.md`、`output/ch09_image_runtime_evidence.png` 和 `assets/ch09/web/ch09_image_runtime_evidence.png`，把本章关键产物整理成运行证据总览。
- 保留 PowerShell 真实运行图，并新增 PowerShell 风格运行证据图，方便学生检查每个输出是否 ready。
- 正文 24 张图片全部使用居中的 `<figure>` 结构和清晰图注。
- 继续收紧正文口吻：路线表、核心概念、心理学/科研图片连接和项目步骤改成学生可执行、可观察的图像处理任务。
