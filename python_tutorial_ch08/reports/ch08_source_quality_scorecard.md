# 第8章来源可信度评分卡

检查日期：2026-06-14

爬虫采集完成后，不要让链接直接躺进报告。先给每个来源做一次小体检：它是不是 HTTPS？是不是官方或教育来源？是否需要交叉验证？是否保存了边界信息？

| 标题 | 域名 | 分数 | 复查理由 |
| --- | --- | --- | --- |
| Python 官网 | www.python.org | 3/4 | HTTPS、官方/教育 |
| Python 文档 | docs.python.org | 3/4 | HTTPS、官方/教育 |
| Python 包索引 | pypi.org | 1/4 | HTTPS、待检查 |
| Python robots | www.python.org | 4/4 | HTTPS、官方/教育、边界页 |
| Wikimedia Commons | commons.wikimedia.org | 2/4 | HTTPS、需复核 |

## 使用提醒

- 分数不是判决书，只是提醒你下一步该怎么复查。
- 官方文档也可能过期，普通网页也可能有价值，关键是写清来源、时间和用途。
- 做心理学或教学资料整理时，宁可少抓一点，也要让每一条材料能回头查。
