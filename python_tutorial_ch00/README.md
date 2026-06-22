# Python Markdown Tutorial - Chapter 00 Detailed

这是第0章交付包：课程地图、科研卡片工厂启动章、配套素材与可运行代码。

## 文件说明

- `chapters/ch00_course_start.md`：第0章 Markdown 正文。
- `assets/ch00/`：第0章正式版配图素材，已统一整理为无解释文字图片，故事和说明放在 Markdown 正文中。
- `assets/ch00/web/`：从 xkcd、Wikimedia Commons、NASA Science 与 Python 官方文档相关来源整理的互联网原图和资料链接，正文中已保留来源与授权说明。
- `code/ch00/`：第0章配套 Python 示例代码。
- `source_notes/source_manifest_ch00.md`：来源与改写说明。
- `source_notes/quality_audit_ch00.md`：第0章质量验收记录。
- `scripts/check_links.py`：Markdown 图片链接检查脚本。
- `scripts/generate_ch00_visuals.py`：第0章正式版图片生成脚本。

## 本轮优化重点

- 删除正文中的远程知乎图片引用，改为本地正式图片，避免外链失效和显示不稳定。
- 新增 `ch00_xkcd_automation_card.png`，用 xkcd 1205《Is It Worth the Time?》解释“什么时候值得自动化”。
- 新增 7 张历史照片：Ada Lovelace、Babbage 差分机、Guido van Rossum、Jacquard 打孔卡、ENIAC、第一张著名 bug 照片、Apollo 软件工程；图片只展示对象本身，解释写在正文中。
- 新增 3 张真实场景照片：图书馆卡片目录、实验笔记本、传送带，用于建立“科研卡片工厂”的任务直觉；图片里不新增解释文字。
- 为正文 19 张图片统一添加 `figure/figcaption` 图注，标题和说明显示在图片下方，图片本体继续保持干净。
- 新增 `learning_momentum_chart.png`，用 Python 生成的反馈曲线图强化“运行、修改、修复带来信心”的学习情绪。
- 新增 `chapter_relay_station.png`，把第1章到第10章的学习蓝图改成更有节奏的接力画面，打断后半章过长的纯文字章节目录。
- 重绘封面、课程路线图、Python 之城、环境流水线、项目阶梯、学习闭环和报错地图。
- 将 `create_learning_base.py` 的运行结果升级为 `python_card_factory/`，目录统一为 `input/` 原料、`cards/` 卡片、`output/` 成品、`reports/` 报告、`assets/` 素材。
- 将 `learning_passport.py` 的语义升级为科研卡片工厂启动卡，默认生成 `output/factory_start_card.md`。
- 新增 `source_notes/source_manifest_ch00.md` 与 `source_notes/quality_audit_ch00.md`，让来源、授权和验收结果可追溯。

## 建议阅读方式

先打开 `chapters/ch00_course_start.md` 阅读正文，再运行：

```bash
python code/ch00/check_python_env.py
python code/ch00/create_learning_base.py
python code/ch00/print_course_map.py
```

`learning_passport.py` 是交互脚本，会要求输入学习目标和第一批材料类型：

```bash
python code/ch00/learning_passport.py
```
