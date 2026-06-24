# 第10章来源记录

## 主来源

- `第十章_Python办公自动化2025.pptx`

本章依据原课件主题重构为《Python 办公自动化》，并延续“科研卡片工厂”主线。MATLAB 教材仅作为“讲故事、放图片、做任务、跑代码、看成果”的组织方式参考，不迁移 MATLAB 技术内容。

## 参考来源与互联网素材

- Hollerith 制表机历史照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:HollerithMachine.CHM.jpg>
- 打字机办公历史照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Secretary_at_typewriter_1912_(3192197470).jpg>
- Margaret Hamilton 与阿波罗导航软件代码清单照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Margaret_Hamilton_-_restoration.jpg>
- Bletchley Park 建筑照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Bletchley_Park.jpg>
- Xerox Alto 电脑照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Xerox_Alto_mit_Rechner.JPG>
- VisiCalc 电子表格截图：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Visicalc.png>；作者 User:Gortu；Public domain；来源 apple2history.org
- Ebbinghaus 遗忘曲线图：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Ebbinghaus_Forgetting_Curve.jpg>
- 办公自动化历史脉络图：由本章既有 Hollerith 制表机、打字机、Margaret Hamilton、Bletchley Park、Xerox Alto、VisiCalc 和 Ebbinghaus 本地素材合成，不新增互联网来源
- PyCharm 解释器配置截图：JetBrains 官方 PyCharm 帮助文档  
  <https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html>
- PowerShell 运行图：本机运行第10章完整链路后，根据当前 `reports/` 真实文件列表整理生成，用于展示 Word、Excel、PPT、预览图、交付回执和 zip 交付包
- 报告预览图：本机运行 `04_generate_office_pack.py` 生成 `reports/final_report_preview.png`
- 交付索引预览图：本机运行 `05_generate_delivery_index.py` 生成 `reports/delivery_index_preview.png`
- Excel 工作簿预览图：本机运行 `06_make_excel_preview.py` 生成 `reports/excel_workbook_preview.png`
- 交付回执预览图：本机运行 `07_make_delivery_package.py` 生成 `reports/delivery_receipt_preview.png`
- 交付包目录清单预览图：本机运行 `10_make_delivery_package_manifest.py` 打开 `reports/ch10_delivery_package.zip` 后生成 `reports/delivery_package_manifest.png`
- 全书课程作品集预览图：本机运行 `08_make_course_portfolio.py` 生成 `reports/course_portfolio_preview.png`
- 结课展示墙预览图：本机运行 `09_make_final_showcase_board.py` 生成 `reports/final_showcase_board.png`，用于把本章最终交付物摆成一张可分享总览
- 结课交付档案图：本机运行 `09_make_final_showcase_board.py` 生成 `reports/capstone_handoff_dossier.md` 和 `reports/capstone_handoff_dossier.png`，用于把 ch0-ch10 的学习路线和最终交付包收束成一张可讲述的成果图
- 最终运行证据图：本机运行 `11_make_final_runtime_evidence.py` 生成 `reports/final_runtime_evidence.md` 和 `reports/final_runtime_evidence.png`，用于检查 CSV、Word、Excel、PPT、zip、作品集、展示墙和结课交付档案是否齐全

## 生成素材

本章包含 24 张正文正式图片、7 张 Wikimedia 原图、1 张由既有素材合成的办公史脉络图、1 张 JetBrains 官方截图、1 张本机 PowerShell 运行图，以及 9 张脚本生成的预览/回执/作品集/展示墙/结课交付档案/交付包目录/最终运行证据图：

- `ch10_cover.png`
- `ch10_hollerith_tabulator_story.png`
- `ch10_typewriter_office_story.png`
- `ch10_margaret_hamilton_quality_story.png`
- `ch10_bletchley_teamwork_story.png`
- `ch10_xerox_alto_office_story.png`
- `ch10_visicalc_spreadsheet_story.png`
- `ch10_ebbinghaus_memory_story.png`
- `ch10_office_history_gallery.png`
- `ch10_roadmap.png`
- `ch10_pycharm_interpreter_real.png`
- `ch10_powershell_office_run.png`
- `ch10_core_metaphor.png`
- `ch10_generated_report_preview.png`
- `ch10_excel_workbook_preview.png`
- `ch10_pitfall_map.png`
- `ch10_project_dashboard.png`
- `ch10_delivery_index_preview.png`
- `ch10_delivery_receipt_preview.png`
- `ch10_delivery_package_manifest.png`
- `ch10_course_portfolio_preview.png`
- `ch10_final_showcase_board.png`
- `ch10_capstone_handoff_dossier.png`
- `ch10_final_runtime_evidence.png`
- `web/hollerith_tabulating_machine.jpg`
- `web/secretary_typewriter_1912.jpg`
- `web/margaret_hamilton_apollo_code.jpg`
- `web/bletchley_park_mansion.jpg`
- `web/xerox_alto_computer.jpg`
- `web/visicalc_screenshot.png`
- `web/ebbinghaus_forgetting_curve.jpg`
- `web/pycharm_python_interpreter_widget_dark.png`
- `web/powershell_ch10_office_run.png`
- `web/final_report_preview.png`
- `web/delivery_index_preview.png`
- `web/excel_workbook_preview.png`
- `web/delivery_receipt_preview.png`
- `web/delivery_package_manifest.png`
- `web/course_portfolio_preview.png`
- `web/final_showcase_board.png`
- `web/capstone_handoff_dossier.png`
- `web/final_runtime_evidence.png`

图片内部不放解释性长文字，说明统一写在 Markdown 正文和图注中。历史照片、软件截图、曲线图和脚本生成成果图自带的文字属于素材或产物本身内容。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 图片本体使用 `<img ... style="zoom:50%; display:block; margin:0 auto;" />` 居中显示。
- 每张图片下方都有 `<figcaption>` 图注。
- 本章减少抽象流程图，增加真实历史照片、真实 PyCharm 截图、真实 PowerShell 截图、心理学素材和脚本生成成果图。
- 新增办公史脉络图只使用图片、编号和连接线，不在图片内部放长段中文说明；完整解释放在正文和图注中。
- 模板故事、交付场景、项目结构和复盘迁移使用学生视角，直接说明要生成、检查、打包和复核的动作。
