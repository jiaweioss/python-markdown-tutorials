# 第5章来源记录

## 主来源

- `第五章_面向对象程序设计2025.pptx`

本章依据原课件主题重构为《面向对象程序设计》，并延续“科研卡片工厂”主线。MATLAB 教材仅作为“讲故事、放图片、做任务、跑代码、看成果”的组织方式参考，不迁移 MATLAB 技术内容。

## 互联网图片来源

本章互联网图片全部先保存到 `assets/ch05/web/`，再由 `scripts/generate_ch05_visuals.py` 整理成正式教材图。图片内部不新增解释文字，说明全部放在 Markdown 图注和正文中。xkcd 漫画保留原图文字。

| 用途 | 原图 | 本地原图 | 正式图片 | 来源、作者与授权 |
| --- | --- | --- | --- | --- |
| Simula 与对象思想源头 | Simula logo | `assets/ch05/web/simula_logo.png` | `assets/ch05/ch05_simula_origin_story.png` | Wikimedia Commons |
| OOP 源头人物 | Kristen-Nygaard-SBLP-1997-head | `assets/ch05/web/kristen_nygaard.png` | `assets/ch05/ch05_kristen_nygaard_story.png` | Wikimedia Commons；Jorge Stolfi；Public domain |
| 类/图纸比喻 | Seattle - University Bridge blueprint, 1915 | `assets/ch05/web/university_bridge_blueprint.jpg` | `assets/ch05/ch05_blueprint_class_story.png` | Wikimedia Commons；Seattle Municipal Archives；CC BY 2.0 |
| 面向对象思想人物 | Computer scientist Alan Kay | `assets/ch05/web/alan_kay.jpg` | `assets/ch05/ch05_alan_kay_oop_story.png` | Wikimedia Commons；作者 Ryan Johnson；CC BY-SA 4.0 |
| Smalltalk 教育与对象探索 | Adele Goldberg at PyCon 2007 | `assets/ch05/web/adele_goldberg_pycon_2007.jpg` | `assets/ch05/ch05_adele_goldberg_story.png` | Wikimedia Commons |
| Smalltalk/Squeak 环境 | Squeak 5.1 morphic interface screenshot | `assets/ch05/web/squeak_morphic_interface_screenshot.png` | `assets/ch05/ch05_smalltalk_environment_story.png` | Wikimedia Commons |
| 代码质量梗图 | xkcd 1513: Code Quality | `assets/ch05/web/xkcd_code_quality.png` | `assets/ch05/ch05_xkcd_code_quality.png` | xkcd；Randall Munroe；CC BY-NC 2.5 |
| 组合优先于继承 | Lego Color Bricks | `assets/ch05/web/lego_color_bricks.jpg` | `assets/ch05/ch05_lego_composition_story.png` | Wikimedia Commons；Alan Chia；CC BY-SA 2.0 |
| 认知图式与学习心理学 | Jean Piaget in Ann Arbor | `assets/ch05/web/jean_piaget.png` | `assets/ch05/ch05_piaget_schema_story.png` | Wikimedia Commons；1968 Michiganensian；Public domain in the United States |

原始链接：

- https://commons.wikimedia.org/wiki/File:Simula_-_logo.png
- https://commons.wikimedia.org/wiki/File:Kristen-Nygaard-SBLP-1997-head.png
- https://commons.wikimedia.org/wiki/File:Seattle_-_University_Bridge_blueprint,_1915_(49781358396).jpg
- https://commons.wikimedia.org/wiki/File:Computer_scientist_Alan_Kay.jpg
- https://commons.wikimedia.org/wiki/File:Adele_Goldberg_at_PyCon_2007.jpg
- https://commons.wikimedia.org/wiki/File:Squeak_51_morphic_interface_screenshot.png
- https://xkcd.com/1513/
- https://commons.wikimedia.org/wiki/File:Lego_Color_Bricks.jpg
- https://commons.wikimedia.org/wiki/File:Jean_Piaget_in_Ann_Arbor.png

## 真实运行与生成素材

- `assets/ch05/ch05_object_theater_story.png`：由 `scripts/generate_ch05_visuals.py` 生成的无文字“对象剧场”类比图，用于解释对象职责和消息协作。
- `assets/ch05/web/powershell_ch05_oop_run.png`：基于本地运行结果整理的 PowerShell 运行图，覆盖 5 个 OOP 脚本。
- `assets/ch05/web/ch05_oop_runtime_evidence.png`：本地运行 `10_make_oop_runtime_evidence.py` 生成的 OOP 运行证据图，集中检查报告、图片和 JSON 是否齐全。
- `reports/ch05_oop_runtime_evidence.md`：本地运行 `10_make_oop_runtime_evidence.py` 生成的运行证据清单。
- `output/ch05_oop_runtime_evidence.png`：本地运行 `10_make_oop_runtime_evidence.py` 生成的运行证据预览图。
- `assets/ch05/web/ch05_oop_model_preview.png`：本地运行 `04_make_oop_model_report.py` 生成的对象模型预览图。
- `assets/ch05/web/ch05_design_cards_preview.png`：本地运行 `05_make_design_cards.py` 生成的类职责卡片预览图。
- `assets/ch05/web/ch05_object_collaboration_map.png`：本地运行 `06_make_object_collaboration_map.py` 生成的对象协作消息图。
- `assets/ch05/web/ch05_object_quality_receipt.png`：本地运行 `07_make_object_quality_receipt.py` 生成的对象质量回执。
- `assets/ch05/web/ch05_object_delivery_package.png`：本地运行 `08_make_object_delivery_package.py` 生成的对象交付包预览图。
- `output/ch05_object_delivery_package.json`：本地运行 `08_make_object_delivery_package.py` 导出的对象模型 JSON。
- `reports/ch05_object_delivery_package.md`：本地运行 `08_make_object_delivery_package.py` 生成的对象交付包报告。
- `assets/ch05/web/ch05_gui_panel_object_model.png`：本地运行 `09_make_gui_panel_object_model.py` 读取 ch4 GUI 面板规格后生成的对象模型预览图。
- `output/ch05_gui_panel_object_model.json`：本地运行 `09_make_gui_panel_object_model.py` 导出的 GUI 面板对象模型 JSON。
- `reports/ch05_gui_panel_object_model.md`：本地运行 `09_make_gui_panel_object_model.py` 生成的 GUI 面板对象模型报告。
- `assets/ch05/ch05_powershell_oop_run.png`、`assets/ch05/ch05_oop_runtime_evidence.png`、`assets/ch05/ch05_oop_model_preview.png`、`assets/ch05/ch05_design_cards_preview.png`、`assets/ch05/ch05_object_collaboration_map.png`、`assets/ch05/ch05_object_quality_receipt.png`、`assets/ch05/ch05_object_delivery_package.png`：由生成脚本整理后的正式教材图。

## 生成素材

本章包含 26 张正文正式图片、9 张互联网原图、2 张本机运行/证据图和 6 张脚本生成预览图。正式图片如下：

- `ch05_cover.png`
- `ch05_simula_origin_story.png`
- `ch05_kristen_nygaard_story.png`
- `ch05_story_scene.png`
- `ch05_blueprint_class_story.png`
- `ch05_alan_kay_oop_story.png`
- `ch05_adele_goldberg_story.png`
- `ch05_smalltalk_environment_story.png`
- `ch05_xkcd_code_quality.png`
- `ch05_object_theater_story.png`
- `ch05_roadmap.png`
- `ch05_core_metaphor.png`
- `ch05_lego_composition_story.png`
- `ch05_minimal_demo.png`
- `ch05_powershell_oop_run.png`
- `ch05_oop_runtime_evidence.png`
- `ch05_psychology_link.png`
- `ch05_piaget_schema_story.png`
- `ch05_pitfall_map.png`
- `ch05_project_dashboard.png`
- `ch05_oop_model_preview.png`
- `ch05_design_cards_preview.png`
- `ch05_object_collaboration_map.png`
- `ch05_object_quality_receipt.png`
- `ch05_object_delivery_package.png`
- `ch05_gui_panel_object_model.png`

图片内部不放解释性长文字，说明统一写在 Markdown 正文和图注中。真实历史图、软件截图、漫画和脚本生成报告图保留素材自身内容。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 每张图片都有 `<figcaption>`。
- 故事图片穿插在对应知识点附近，不集中堆在开头。
- 示例代码与项目任务围绕“科研卡片工厂”连续推进。
- 本轮继续做学生视角修订：正文不再使用“本教程会……”这类后台口吻，路线表、核心概念列表和脚本导读改成学生可直接执行和观察的对象动作。
