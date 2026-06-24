# Python Markdown 教程书：第10章

本包是第10章《Python 办公自动化》的 Markdown 教材包。

## 内容

- `chapters/`：教材正文
- `assets/ch10/`：本章正式图片，全部本地化、居中显示、图注在图下
- `assets/ch10/web/`：互联网原图、本机 PowerShell 截图和脚本生成的报告、作品集、展示墙、结课成果档案、成果包目录清单、最终运行记录预览图
- `code/ch10/`：可运行示例代码
- `input/`：脚本生成的 CSV 原料
- `reports/`：脚本生成的 Markdown、Word、Excel、PPT、课程作品集、结课展示墙、成果记录、成果包目录清单和预览图
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查
- `scripts/generate_ch10_visuals.py`：本章图片生成脚本
- `source_notes/`：来源记录和质量检查
- `manifest.json`：文件清单

## 本章项目

科研卡片工厂结课报告：从 CSV 数据出发，自动生成 Markdown、Word、Excel、PPT、预览图、成果索引、全书课程作品集、结课展示墙、结课成果档案、成果记录、zip 成果包、成果包目录清单和最终运行记录，理解办公自动化的“输入、处理、输出、检查、汇总、展示、打包、复核、检查”闭环。

## 本轮优化重点

- 从 15 张正文图扩展到 18 张正文图，新增 VisiCalc 电子表格截图、Excel 工作簿预览图、成果记录预览图。
- 新增 `05_generate_delivery_index.py`，自动扫描 `reports/` 目录并生成 `delivery_index.md` 与 `delivery_index_preview.png`。
- 新增 `06_make_excel_preview.py` 和 `07_make_delivery_package.py`，把办公自动化主线从“生成文件”扩展为“生成、预览、检查、打包、成果、复盘”的完整闭环。
- 继续扩展到 19 张正文图，新增 `08_make_course_portfolio.py`，把 ch0-ch10 的正文图片、Python 脚本和素材汇总成 `course_portfolio.csv`、`course_portfolio.md` 和作品集预览图。
- 上一轮扩展到 20 张正文图，新增 `09_make_final_showcase_board.py`，把报告预览、Excel 预览、课程作品集、成果索引、Word 报告和 PPT 展示整理成结课展示墙。
- 修复 `07_make_delivery_package.py` 成果记录预览图的底部布局，让 12 个成果文件条目和 package 信息完整分离显示，避免正式配图中出现压行或越界。
- 继续扩展到 21 张正文图，新增 `10_make_delivery_package_manifest.py`，打开 zip 成果包并生成 `delivery_package_manifest.md`、`delivery_package_manifest.png` 和正文图 `ch10_delivery_package_manifest.png`，让成果包内部内容可复查。
- 此前新增 `11_make_final_runtime_evidence.py`，生成 `final_runtime_evidence.md`、`final_runtime_evidence.png` 和正文图 `ch10_final_runtime_evidence.png`，把 CSV、Word、Excel、PPT、zip、作品集和展示墙纳入最终运行检查。
- 继续扩展到 23 张正文图，增强 `09_make_final_showcase_board.py`，新增 `capstone_handoff_dossier.md`、`capstone_handoff_dossier.png` 和正文图 `ch10_capstone_handoff_dossier.png`，把 ch0-ch10 的学习路线与最终成果包收束成一张结课档案图。
- 本轮继续扩展到 24 张正文图，新增 `ch10_office_history_gallery.png`，把制表机、打字机、软件工程、协作现场、图形界面、电子表格和记忆曲线合成一张无长文字脉络图，并在正文中补充办公自动化的人文背景故事。
- 保持图片居中和图注规则：图片内部不新增解释性长文字，故事与说明放在 Markdown 正文和图注中。
- 正文新增 `[TOC]`、本章导读、分区导航和五个大部分，让网页侧栏能清楚显示章节分界。
- 继续收紧正文口吻：模板故事、成果整理场景、项目结构和复盘迁移改成学生自己的报告整理任务，减少对象错位。
- 更新来源记录、manifest 和质量检查记录，记录新增图片来源和新增脚本。
