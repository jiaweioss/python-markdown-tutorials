# GitHub 管理说明

## 仓库范围

本仓库用于维护 Python Markdown 教程书的正式内容，包括：

- `python_tutorial_ch00` 到 `python_tutorial_ch10` 的正文、配图、示例代码、报告和来源记录。
- 每章的 `source_notes` 质量验收记录。
- 每章的 `scripts/check_links.py` 和视觉生成脚本。
- `website/` 静态站点生成器、样式和部署脚本。

不纳入普通 Git 管理的内容：

- 本机缓存、虚拟环境、编辑器配置和临时文件。
- `public/` 等由脚本生成的网页发布目录。
- 部署压缩包和本机临时上传包。
- 上级目录中的 Matlab 参考 PDF、原始 PPT 课件和本机 Codex 启动脚本。

## 分支建议

- `main`：稳定可阅读版本。
- `content/chXX-topic`：某一章的大修或补图。
- `fix/chXX-links`：图片链接、路径、错别字等小修。
- `site/ui-polish`：网页阅读体验与交互优化。
- `release/vYYYY.MM.DD`：阶段性课程发布。

## 提交流程

1. 修改章节正文、配图、代码或站点生成器。
2. 若修改章节，运行对应章节的链接检查脚本。
3. 若修改网页，运行 `python website/build_site.py` 并检查 `public/` 的 HTML 引用。
4. 确认没有新增缓存、临时文件、账号、密钥、令牌或服务器密码。
5. 提交信息使用简短中文或英文，例如 `完善第 6 章图表验收记录`。

## 发布检查

每次推送到 GitHub 前建议检查：

- 章节入口链接是否可点击。
- 图片是否使用相对路径并能在 GitHub Markdown 中显示。
- 单个文件是否小于 GitHub 普通仓库限制。
- `source_notes` 是否记录新增图片或外部素材来源。
- 示例代码是否能在本地最小环境运行。
- 网页首页、至少一个章节页和配套文件页是否能正常打开。

## 后续可加的自动化

- GitHub Actions：批量运行各章 `check_links.py`。
- Releases：按课程阶段打包发布。
- Issues：收集错别字、图片缺失、代码运行失败和教学反馈。
- Projects：按章节跟踪“待补图、待校对、待试讲、已发布”状态。

