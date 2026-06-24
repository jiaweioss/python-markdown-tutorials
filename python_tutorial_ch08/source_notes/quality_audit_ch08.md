# 第8章质量验收记录

验收日期：2026-06-15

## 验收范围

- `chapters/`
- `assets/ch08/`
- `code/ch08/`
- `output/`
- `reports/`
- `scripts/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch08.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 符合 ch0/ch1 图文标准 | 正文约 19941 字，包含 `[TOC]`、本章导读、分区导航、五个清晰部分、Tim Berners-Lee、Vannevar Bush、WorldWideWeb、CERN 服务器、Mosaic、Internet Archive、xkcd 梗图、真实运行图、爬虫运行证据图、爬虫礼仪检查卡、来源可信度评分卡、公开资料采集包、来源追踪档案、代码、项目、练习与总结 | 已完成 |
| 图片居中且有图注 | 正文 24 张图片全部使用 `<figure>` 与 `<figcaption>` | 已完成 |
| 图片内部不堆解释文字 | 整理图不新增解释性长文字，说明放在正文和图注；真实历史图、浏览器图、xkcd 漫画和脚本生成图保留自身内容 | 已完成 |
| 故事穿插在知识点中 | Web 起源对应 URL/链接，Vannevar Bush 对应关联路径和来源路标，服务器对应请求，Mosaic 对应页面结构，Internet Archive 和 xkcd 对应来源复查，来源卡片和评分卡对应科研材料管理；路线表、核心概念和脚本导读已改成学生视角的可执行采集动作 | 已完成 |
| 线上开放范围统一 | 网站构建脚本保持 `PUBLIC_CHAPTER_MAX = 6`，ch08 仅作为本地后续章节整理，不推进线上开放范围 | 已完成 |
| 真实运行环境截图 | PowerShell 运行图展示脚本的运行路径与生成结果；新增爬虫运行证据图集中检查 CSV、报告、来源卡片、评分卡、采集包和追踪档案 | 已完成 |
| 学以致用 | 本章项目为“公开资料采集器”，新增采集报告、来源卡片、爬虫礼仪检查卡、来源可信度评分卡、公开资料采集包、来源追踪档案、运行证据和七张脚本生成预览/证据图 | 已完成 |
| 代码可检查 | 示例脚本均为 ASCII 文件名，可进行 AST 语法检查 | 已完成 |

## 当前结果

- 正文字符数：19941
- 正文图片引用数：24
- manifest 素材数：40
- 本章代码文件数：11，其中 Python 脚本 10 个
- Markdown 图片语法数量：0
- 图注数量：24

## 运行结果

本机已运行：

```bash
python code/ch08/01_local_html_parser.py
python code/ch08/03_save_links_csv.py
python code/ch08/04_make_crawl_report.py
python code/ch08/05_make_source_cards.py
python code/ch08/06_make_crawl_etiquette_card.py
python code/ch08/07_make_source_quality_scorecard.py
python code/ch08/08_make_public_source_bundle.py
python code/ch08/09_make_source_provenance_archive.py
python code/ch08/10_make_scraper_runtime_evidence.py
```

生成文件：

- `output/links.csv`
- `reports/ch08_crawl_report.md`
- `reports/ch08_crawl_report_preview.png`
- `reports/ch08_source_cards.md`
- `output/ch08_source_cards_preview.png`
- `reports/ch08_crawl_etiquette_card.md`
- `output/ch08_crawl_etiquette_card.png`
- `reports/ch08_source_quality_scorecard.md`
- `output/ch08_source_quality_scorecard.png`
- `output/ch08_public_source_bundle.json`
- `reports/ch08_public_source_bundle.md`
- `output/ch08_public_source_bundle.png`
- `reports/ch08_source_provenance_archive.md`
- `output/ch08_source_provenance_archive.png`
- `reports/ch08_scraper_runtime_evidence.md`
- `output/ch08_scraper_runtime_evidence.png`
- `assets/ch08/web/ch08_scraper_runtime_evidence.png`

## 验收动作

- 运行 `python scripts/generate_ch08_visuals.py`，重新生成 24 张正式图片。
- 运行 `python scripts/check_links.py`，确认 Markdown 图片链接有效。
- 对 `code/ch08/*.py` 与 `scripts/*.py` 做 AST 语法检查。
- 用 PIL 打开所有 PNG/JPG/GIF 图片。
- 生成临时总览图检查构图与排版，确认后删除临时文件。
- 运行全书交叉检查：通过，11 个章节包、130 个 Python 文件、108 个 code Python 脚本、263 个 Markdown 图片引用，0 个缺失本地图片链接，0 个图注不匹配，0 个 manifest 计数不一致，0 个 PIL 图片错误，0 个临时文件残留。

当前补充验收结果：

- `scripts/check_links.py`：通过，检查 24 个本地图片引用
- Python 语法检查：通过，AST 覆盖 12 个 `.py` 文件
- 图片 PIL 打开检查：通过，40 张图片均可打开
- 学生视角语言检查：通过，路线表、核心概念、心理学/科研资料连接和脚本导读已改成可执行、可观察的资料采集任务
- 临时总览图人工检查：通过，24 张正文图居中且无明显越界；检查后已删除临时图
