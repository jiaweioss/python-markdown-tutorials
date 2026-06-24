# Python Markdown 教程书：第8章

本包是第8章《网络爬虫开发实战》的 Markdown 教材交付。

## 内容

- `chapters/`：教材正文
- `assets/ch08/`：本章正式图片，全部本地化、居中显示、图注在下
- `assets/ch08/web/`：Web 历史图片、超链接思想史人物图、xkcd 梗图、本机 PowerShell 运行图和脚本生成的预览/来源追踪/运行证据图
- `code/ch08/`：可运行示例代码
- `output/`：脚本生成的链接 CSV
- `reports/`：脚本生成的公开资料采集报告、来源卡片、爬虫礼仪检查卡、来源可信度评分卡、公开资料采集包、来源追踪档案和爬虫运行证据
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查
- `scripts/generate_ch08_visuals.py`：本章图片生成脚本
- `source_notes/`：来源记录和质量验收
- `manifest.json`：交付清单

## 本章项目

公开资料采集器：用本地 HTML 练习解析，读取 `robots.txt` 理解规则边界，保存标题和链接，并生成可复查的采集报告、来源卡片、礼仪检查卡、来源可信度评分卡、面向学习卡片的公开资料采集包、来源追踪档案和运行证据清单。

## 本轮增强

- 增加 Tim Berners-Lee、Vannevar Bush、WorldWideWeb、NCSA Mosaic、Internet Archive 和 xkcd 等 Web 历史、超链接思想与公开资料场景图片。
- 将示例请求保留为读取 `https://www.python.org/robots.txt`，强调爬虫边界和规则意识。
- 新增 `05_make_source_cards.py`，生成 `reports/ch08_source_cards.md` 和 `output/ch08_source_cards_preview.png`。
- 新增 `06_make_crawl_etiquette_card.py`，生成 `reports/ch08_crawl_etiquette_card.md` 和 `output/ch08_crawl_etiquette_card.png`，把 robots、频率、范围、来源和停止条件变成可检查动作。
- 新增 `07_make_source_quality_scorecard.py`，生成 `reports/ch08_source_quality_scorecard.md` 和 `output/ch08_source_quality_scorecard.png`，把来源可信度变成可复查动作。
- 新增 `08_make_public_source_bundle.py`，读取 ch7 的反馈小游戏复习计划，生成 `reports/ch08_public_source_bundle.md`、`output/ch08_public_source_bundle.json` 和 `output/ch08_public_source_bundle.png`。
- 新增 `09_make_source_provenance_archive.py`，生成 `reports/ch08_source_provenance_archive.md` 和 `output/ch08_source_provenance_archive.png`，把链接、域名、来源类型和复查提醒整理成来源追踪档案。
- 新增 `10_make_scraper_runtime_evidence.py`，生成 `reports/ch08_scraper_runtime_evidence.md`、`output/ch08_scraper_runtime_evidence.png` 和正文图 `ch08_scraper_runtime_evidence.png`，集中检查采集报告、来源卡片、评分卡、公开资料包和来源追踪档案是否齐全。
- 更新本机 PowerShell 运行图，展示本地 HTML 解析、robots.txt 请求、CSV 保存、报告生成和来源卡片生成。
- 正文 24 张图片全部使用居中的 `<figure>` 结构和清晰图注。
- 继续收紧正文口吻：路线表、核心概念和脚本导读改成学生可执行、可观察的公开资料采集动作。
- 新增 `[TOC]`、本章导读、分区导航和五个清晰部分：Web 公共空间、爬虫运行、概念脚本、来源证据、练习复盘。
- 本章继续作为本地后续章节整理，不改变网站发布边界；线上仍只开放到 ch06。
