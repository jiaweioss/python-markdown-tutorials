# 第8章来源记录

## 主来源

- `第八章_网络爬虫开发实战2025.pptx`

本章依据原课件主题重构为《网络爬虫开发实战》，并延续“科研卡片工厂”主线。MATLAB 教材仅作为“讲故事、放图片、做任务、跑代码、看成果”的组织方式参考，不迁移 MATLAB 技术内容。

## 互联网与真实运行素材

本章互联网图片全部先保存到 `assets/ch08/web/`，再由 `scripts/generate_ch08_visuals.py` 整理成正式教材图。整理图内部不新增解释文字，说明统一写在 Markdown 正文和图注中。

| 用途 | 原图 | 本地原图 | 正式图片 | 来源、作者与授权 |
| --- | --- | --- | --- | --- |
| Web 起源场景 | Tim Berners-Lee Office at CERN | `assets/ch08/web/tim_berners_lee_office_cern.jpg` | `assets/ch08/ch08_tim_berners_lee_office_story.png` | Wikimedia Commons |
| Web 发明者人物 | Tim Berners-Lee | `assets/ch08/web/tim_berners_lee_portrait.jpg` | `assets/ch08/ch08_tim_berners_lee_portrait_story.png` | Wikimedia Commons；Uldis Bojārs；CC BY-SA 2.5 |
| 超链接思想史 | Vannevar Bush, 1938, Harris & Ewing (cropped) | `assets/ch08/web/vannevar_bush_1938.jpg` | `assets/ch08/ch08_vannevar_bush_story.png` | Wikimedia Commons；Harris & Ewing；Public domain |
| 早期浏览器 | WorldWideWeb | `assets/ch08/web/worldwideweb_browser.png` | `assets/ch08/ch08_worldwideweb_browser_story.png` | Wikimedia Commons |
| 浏览器普及史 | NCSA Mosaic Browser Screenshot | `assets/ch08/web/ncsa_mosaic_browser_screenshot.png` | `assets/ch08/ch08_mosaic_browser_story.png` | Wikimedia Commons |
| 客户端/服务器 | CERN first server | `assets/ch08/web/cern_first_web_server.jpg` | `assets/ch08/ch08_first_web_server_story.png` | Wikimedia Commons |
| 来源复查意识 | Internet Archive headquarters | `assets/ch08/web/internet_archive_headquarters.jpg` | `assets/ch08/ch08_internet_archive_story.png` | Wikimedia Commons |
| 失效链接梗图 | xkcd 979: Wisdom of the Ancients | `assets/ch08/web/xkcd_wisdom_of_the_ancients.png` | `assets/ch08/ch08_xkcd_wisdom_story.png` | xkcd；Randall Munroe；CC BY-NC 2.5 |
| 规则边界 | Python.org robots.txt | 无图片 | 脚本 `02_fetch_python_homepage.py` | https://www.python.org/robots.txt |

原始链接：

- https://commons.wikimedia.org/wiki/File:Tim_Berners-Lee_Office_at_CERN.jpg
- https://commons.wikimedia.org/wiki/File:Tim_Berners-Lee.jpg
- https://commons.wikimedia.org/wiki/File:Vannevar_Bush,_1938,_Harris_%26_Ewing_(cropped).jpg
- https://commons.wikimedia.org/wiki/File:WorldWideWeb.png
- https://commons.wikimedia.org/wiki/File:NCSA_Mosaic_Browser_Screenshot.png
- https://commons.wikimedia.org/wiki/File:CERN-first-server-p1030757.jpg
- https://commons.wikimedia.org/wiki/File:Internet_Archive_-_5079018246.jpg
- https://xkcd.com/979/
- https://www.python.org/robots.txt

## 真实运行与生成素材

- `assets/ch08/web/powershell_ch08_scraper_run.png`：本机运行结果整理图，覆盖本地 HTML 解析、robots.txt 检查、CSV 保存、采集报告和来源卡片。
- `assets/ch08/web/ch08_crawl_report_preview.png`：本机运行 `04_make_crawl_report.py` 生成的采集报告预览图。
- `assets/ch08/web/ch08_source_cards_preview.png`：本机运行 `05_make_source_cards.py` 生成的来源卡片预览图。
- `assets/ch08/web/ch08_crawl_etiquette_card.png`：本机运行 `06_make_crawl_etiquette_card.py` 生成的爬虫礼仪检查卡。
- `assets/ch08/web/ch08_source_quality_scorecard.png`：本机运行 `07_make_source_quality_scorecard.py` 生成的来源可信度评分卡。
- `assets/ch08/web/ch08_public_source_bundle.png`：本机运行 `08_make_public_source_bundle.py` 生成的公开资料采集包。
- `assets/ch08/web/ch08_source_provenance_archive.png`：本机运行 `09_make_source_provenance_archive.py` 生成的来源追踪档案。
- `assets/ch08/web/ch08_scraper_runtime_evidence.png`：本机运行 `10_make_scraper_runtime_evidence.py` 生成的爬虫运行证据图，用于检查链接 CSV、采集报告、来源卡片、礼仪检查卡、来源质量评分、公开资料包和来源追踪档案是否齐全。
- `reports/ch08_scraper_runtime_evidence.md`：本机运行 `10_make_scraper_runtime_evidence.py` 生成的运行证据清单。
- `output/ch08_scraper_runtime_evidence.png`：本机运行 `10_make_scraper_runtime_evidence.py` 生成的运行证据预览图。

## 生成素材

本章包含 24 张正文正式图片、8 张互联网原图/截图/漫画、1 张本机 PowerShell 运行图和 7 张脚本生成预览/来源追踪/运行证据图。

正式图片：

- `ch08_cover.png`
- `ch08_tim_berners_lee_office_story.png`
- `ch08_tim_berners_lee_portrait_story.png`
- `ch08_vannevar_bush_story.png`
- `ch08_worldwideweb_browser_story.png`
- `ch08_story_scene.png`
- `ch08_roadmap.png`
- `ch08_core_metaphor.png`
- `ch08_first_web_server_story.png`
- `ch08_mosaic_browser_story.png`
- `ch08_minimal_demo.png`
- `ch08_powershell_scraper_run.png`
- `ch08_psychology_link.png`
- `ch08_internet_archive_story.png`
- `ch08_xkcd_wisdom_story.png`
- `ch08_crawl_etiquette_card.png`
- `ch08_pitfall_map.png`
- `ch08_project_dashboard.png`
- `ch08_crawl_report_preview.png`
- `ch08_source_cards_preview.png`
- `ch08_source_quality_scorecard.png`
- `ch08_public_source_bundle.png`
- `ch08_source_provenance_archive.png`
- `ch08_scraper_runtime_evidence.png`

图片内部不新增解释性长文字，说明全部放在 Markdown 正文和图注中。真实历史图、浏览器截图、xkcd 漫画、软件截图和脚本生成图保留素材自身内容。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 每张图片都有 `<figcaption>`。
- 故事图片穿插在对应知识点附近，不集中堆在开头。
- 示例代码与项目任务围绕“科研卡片工厂”连续推进。
- 路线表、核心概念和脚本导读使用学生视角，直接说明要请求、解析、保存、复查和入库的动作。
