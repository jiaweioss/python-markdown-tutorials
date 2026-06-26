# 第 8 章：网络爬虫开发实战

[TOC]

<style>
figure {
  margin: 1.2em auto 1.8em;
  text-align: center;
}
figure img {
  max-width: 100%;
  display: block;
  margin: 0 auto;
}
figcaption {
  margin-top: 0.45em;
  color: #5f6673;
  font-size: 0.92em;
  line-height: 1.55;
}
figcaption strong {
  color: #2d3748;
}
</style>


<figure align="center">
  <img src="../assets/ch08/ch08_cover.png" alt="第8章封面" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-1 本章封面</strong>：浏览器是人类上网，爬虫是程序替你上网。但程序上网也要守规矩。</figcaption>
</figure>

> 本章一句话：
> **浏览器是人类上网，爬虫是程序替你上网。但程序上网也要守规矩。**

第8章继续推进“科研卡片工厂”的资料采集能力。前面几章已经能整理文件、生成图表、处理图片；这一章要做的事更像给工厂装上一扇“公开资料窗口”：从网页中识别标题、链接和规则，把能复查的材料保存下来。

这一章不追求“抓得多”，而追求“抓得对”。初学爬虫最容易兴奋过头，像第一次进大型图书馆就想把整排书架搬回家。真正成熟的做法是：先看目录和借阅规则，再拿走自己有权使用、确实需要的那几本。

---

## 本章导读：先看边界，再谈采集

### 8.0 本章学习目标

学完本章，你应该能够：

1. 用“地址、请求、结构、边界、来源记录”解释爬虫的最小工作链路。
2. 运行 `01_local_html_parser.py`，先从本地 HTML 中提取链接，避免一开始就对真实网站乱试。
3. 说清楚 Tim Berners-Lee、Vannevar Bush、WorldWideWeb、Mosaic 和 Internet Archive 为什么适合放在爬虫章。
4. 运行 `02_fetch_python_homepage.py`，理解为什么采集前要先看 `robots.txt` 和请求边界。
5. 运行本章脚本，生成链接 CSV、采集报告、来源卡片、礼仪检查卡、来源质量评分、公开资料包、来源追踪档案和运行证据。
6. 完成本章小项目：**公开资料采集器**，并能解释它如何接住 ch7 的复习卡片。

### 本章分区导航

| 分区 | 对应小节 | 你要抓住的主线 | 产出证据 |
| --- | --- | --- | --- |
| 第一部分：Web 的公共空间和采集边界 | 8.1-8.3 | 爬虫不是乱抓网页，而是在地址、文档、链接和规则之间工作 | Web 历史图、核心比喻、边界故事 |
| 第二部分：把爬虫跑起来 | 8.4-8.5 | 先解析本地 HTML，再把规则、来源和证据接进科研资料整理 | PowerShell 运行图、运行证据、礼仪检查卡 |
| 第三部分：概念表与脚本导览 | 8.6-8.7 | 每个爬虫概念都要对应到可运行脚本和可复查文件 | 概念表、脚本清单、报告输出 |
| 第四部分：排错、项目与来源证据 | 8.8-8.9 | 公开资料采集器要能保存来源、评估可信度、形成追踪档案 | 坑地图、项目面板、来源卡片、追踪档案 |
| 第五部分：练习、复盘与后续连接 | 8.10-8.14 | 把采集能力迁移到学习卡片、心理学资料和报告生成 | 练习记录、自测答案、复盘模板 |

---

## 第一部分：Web 的公共空间和采集边界

### 8.1 开场故事：先有画面，再有术语

浏览器是人类上网，爬虫是程序替你上网。但程序上网也要守规矩。这句话不是为了热闹，而是为了把本章的知识放进真实使用场景。初学者最怕一上来就被术语包围，像走进一个所有门牌都用缩写写成的楼层。我们先从画面进入，再慢慢把画面翻译成代码。

<figure align="center">
  <img src="../assets/ch08/ch08_tim_berners_lee_office_story.png" alt="Tim Berners-Lee 在 CERN 的办公室" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-2 Tim Berners-Lee 的 CERN 办公室</strong>：Web 的早期故事不是“到处乱抓”，而是让文档可以被地址访问、被链接连接、被人类和程序共同读取。</figcaption>
</figure>

网页最迷人的地方，是它既给人读，也能给程序读。浏览器把 HTML 渲染成漂亮页面；爬虫则更像戴着放大镜读原始结构：哪里是标题，哪里是链接，哪里是正文。真正合格的爬虫不是“手快”，而是知道边界、知道频率、知道哪些页面不该碰。

<figure align="center">
  <img src="../assets/ch08/ch08_tim_berners_lee_portrait_story.png" alt="Tim Berners-Lee照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-3 Tim Berners-Lee照片</strong>：Web 的伟大之处不只是“能访问”，更是让文档、地址和链接形成了可共享、可引用、可复查的知识网络。</figcaption>
</figure>

Tim Berners-Lee 的故事适合放在爬虫章开头，因为它能把初学爬虫时那种“什么都想抓回来”的兴奋感拉回正轨：Web 不是一座无人看管的仓库，而是一套用地址和链接组织知识的公共空间。爬虫要做的，不是把公共空间搬空，而是把公开、允许、必要的材料整理成可复查记录。

<figure align="center">
  <img src="../assets/ch08/ch08_vannevar_bush_story.png" alt="Vannevar Bush 1938 年肖像" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-4 Vannevar Bush 肖像</strong>：在 Web 出现之前，Bush 就想象过一种能沿着“关联路径”查资料的机器；今天的链接、收藏、引用和来源卡片，都有这条思想线的影子。</figcaption>
</figure>

1945 年，Vannevar Bush 写下《As We May Think》，想象一种叫 Memex 的知识机器：人不是按一本本书线性翻，而是沿着关联线索跳转、记录、再返回。爬虫课把这个故事接过来，并不是为了考历史，而是提醒你：链接不是“随手点的蓝色文字”，它是知识之间的道路。程序沿着道路采集资料时，也要留下路标，否则下一次回头就会迷路。

<figure align="center">
  <img src="../assets/ch08/ch08_worldwideweb_browser_story.png" alt="WorldWideWeb 早期浏览器截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-5 WorldWideWeb 早期浏览器</strong>：早期浏览器把“地址、文档、链接”放在同一个画面里；爬虫正是沿着这些结构读取公开资料。</figcaption>
</figure>

如果把网页想象成城市，URL 就是门牌号，HTML 是房屋结构，链接是街道。人类用浏览器逛街，Python 用代码按门牌访问。区别在于：程序不会自动懂礼貌，所以礼貌要写进流程里。

<figure align="center">
  <img src="../assets/ch08/ch08_story_scene.png" alt="故事场景图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-6 故事场景</strong>：爬虫像守规矩的资料借阅员：先看地址和规则，再请求页面，取出标题和链接，最后留下可复查记录。</figcaption>
</figure>

这个画面对应本章的核心比喻：爬虫像守规矩的资料借阅员：先看地址和规则，再请求页面，取出标题和链接，最后留下可复查记录。 如果你能先记住这个比喻，后面的概念就不再是干巴巴的定义。

---

### 8.2 知识路线

<figure align="center">
  <img src="../assets/ch08/ch08_roadmap.png" alt="知识路线图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-7 知识路线</strong>：先建立直觉，再运行代码，最后完成一个可展示的小项目。</figcaption>
</figure>

本章路线如下：

| 顺序 | 主题 | 你要完成的动作 |
| --- | --- | --- |
| 1 | HTTP 请求 | 用 Python 拿着 URL 去敲门，先确认服务器愿意回应 |
| 2 | HTML 结构 | 把网页从“漂亮页面”看成一棵标签树 |
| 3 | robots 和边界 | 采集前先读规则，知道哪些地方该停下 |
| 4 | 解析标题与链接 | 从 `<a>` 标签里拆出标题、地址和可复查线索 |
| 5 | 保存 CSV | 把链接清单落到文件里，避免资料只停在屏幕上 |
| 6 | 异常处理 | 给网络失败、页面变化和空结果预留退路 |
| 7 | 来源卡片 | 把链接变成有标题、域名、用途和提醒的资料卡 |
| 8 | 来源可信度 | 判断“能打开”之外，还能不能引用和复查 |

---

### 8.3 核心概念：从人话到术语

<figure align="center">
  <img src="../assets/ch08/ch08_core_metaphor.png" alt="核心比喻图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-8 核心比喻</strong>：用一个稳定画面记住本章最重要的概念关系。</figcaption>
</figure>

先用人话说：爬虫像守规矩的资料借阅员：先看地址和规则，再请求页面，取出标题和链接，最后留下可复查记录。

<figure align="center">
  <img src="../assets/ch08/ch08_first_web_server_story.png" alt="CERN 第一台 Web 服务器" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-9 CERN 第一台 Web 服务器</strong>：网页请求的背后，是客户端向服务器索取资源；爬虫只是把这件事写成程序。</figcaption>
</figure>

看到服务器照片时，可以把一次请求想象成一次非常正式的借阅：你拿着 URL 去找服务器，服务器根据规则把资源交给你。你不应该把图书馆书架整排抱走，也不应该无视门口写着“此处请勿进入”的提示。爬虫的技术能力和伦理边界必须一起学。

<figure align="center">
  <img src="../assets/ch08/ch08_mosaic_browser_story.png" alt="NCSA Mosaic 浏览器截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-10 NCSA Mosaic 浏览器</strong>：浏览器负责把结构渲染成人类友好的页面；爬虫则读取结构本身，适合提取标题、链接和表格。</figcaption>
</figure>

Mosaic 让早期 Web 更容易被普通人使用。对 Python 来说，页面的漂亮外观不是重点，重点是背后的标签结构。你看到网页上的蓝色链接，程序看到的是 `<a href="...">`；你看到标题很大，程序看到的是 `<h1>`、`<h2>`。这一层“从画面回到结构”的转换，就是爬虫学习的关键。

再用术语说，本章要掌握这些内容：

- **HTTP 请求**：程序拿着 URL 去服务器取资源，先看回应是否正常，再决定下一步。
- **HTML 结构**：网页不是一张整图，而是一棵标签树；标题、链接和表格都藏在结构里。
- **robots 和边界**：采集前先看门口规则，能访问不代表应该批量抓取。
- **解析标题与链接**：从页面结构里取出真正需要的资料，像从文献里摘出题名和出处。
- **保存 CSV**：把采集结果写成文件，后面才能复查、清洗、分析和引用。
- **异常处理**：网络会断、网页会改、编码会怪，程序要给失败留一条可读的说明。
- **来源卡片**：给每条链接贴上标题、域名、用途和提醒，让资料不再是一串孤零零的网址。
- **来源可信度**：先问“来自哪里、有没有边界、能否交叉验证”，再决定能不能入库。

术语不是用来吓人的，它只是为了让大家交流时不用每次都讲一长串故事。你先用故事建立直觉，再用术语压缩表达，这样学得稳。

---

## 第二部分：把爬虫跑起来

### 8.4 最小可运行示例

<figure align="center">
  <img src="../assets/ch08/ch08_minimal_demo.png" alt="最小示例图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-11 最小示例</strong>：先跑通最小代码，再逐步增加功能，学习会稳很多。</figcaption>
</figure>

本章第一件事不是背参数，而是运行一个最小例子。打开终端，进入本章目录后运行：

```bash
python code/ch08/01_local_html_parser.py
```

如果你能看到输出，说明这一章的入口已经打通。后面所有复杂功能，都是在这个入口上慢慢加能力。

<figure align="center">
  <img src="../assets/ch08/ch08_powershell_scraper_run.png" alt="PowerShell 运行 ch8 爬虫脚本截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-12 PowerShell 真实运行结果</strong>：先解析本地 HTML，再读取 `robots.txt`，保存 CSV，并生成公开资料采集报告与来源卡片。</figcaption>
</figure>

这张截图故意把 `robots.txt` 放进最小示例里。因为爬虫第一课不应该是“怎么快”，而应该是“先看规则”。只有当你知道网页结构、请求边界和保存结果，后面的自动化采集才不会变成莽撞点击器。

跑完脚本以后，还需要确认这些结果真的留下来了。下面这张图像一张采集任务的出库清单：链接 CSV、采集报告、来源卡片、礼仪检查卡、来源质量评分、公开资料包和来源追踪档案都要能被找到。爬虫学习最怕“屏幕上滚过去一堆字，然后什么证据都没留下”，所以本章把证据也做成一个可运行脚本。

<figure align="center">
  <img src="../assets/ch08/ch08_scraper_runtime_evidence.png" alt="PowerShell风格的爬虫运行证据" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-13 PowerShell 风格的爬虫运行证据</strong>：`10_make_scraper_runtime_evidence.py` 检查链接 CSV、采集报告、来源卡片、礼仪检查卡、来源质量评分、公开资料包和来源追踪档案是否都已经生成。</figcaption>
</figure>

这张图的价值不在“好看”，而在“可查”。以后你采集心理学资料、课程网页或科研公告时，也可以让程序最后输出一张这样的证据清单：我采了什么，保存在哪里，来源是否记录，能不能复查。

---

### 8.5 与心理学和科研资料的连接

<figure align="center">
  <img src="../assets/ch08/ch08_psychology_link.png" alt="心理学和科研资料连接图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-14 心理学连接</strong>：把本章能力放进实验、记录、分析和学习分享的真实任务里。</figcaption>
</figure>

这一章把例子贴近心理学、科研记录和学习分享，因为这些任务天然需要清晰流程：材料来自哪里，采集边界是什么，数据存到哪里，结果如何展示，别人能不能复查。

在本章里，你可以这样理解项目价值：

- 它不是孤立练习，而是科研卡片工厂的一台新设备。
- 它处理的材料可以是课程笔记、实验记录、问卷结果、图片、网页资料或报告模板。
- 它最终要留下可检查的结果，而不是只在屏幕上闪一下。

<figure align="center">
  <img src="../assets/ch08/ch08_internet_archive_story.png" alt="Internet Archive 总部照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-15 Internet Archive 总部</strong>：公开资料采集不只是“拿到链接”，更重要的是保留来源、时间和可复查线索。</figcaption>
</figure>

科研资料最怕“我好像在哪里见过”。链接、标题、访问时间、来源说明，都是未来复查的路标。整理心理学或课程素材时，爬虫脚本不应该只把内容吸走，还要把来源写清楚。否则今天看起来很聪明，明天写报告时就会变成考古现场。

<figure align="center">
  <img src="../assets/ch08/ch08_xkcd_wisdom_story.png" alt="xkcd Wisdom of the Ancients漫画" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-16 xkcd Wisdom of the Ancients漫画</strong>：互联网上最痛的瞬间之一，是终于找到答案，却发现页面、图片或上下文已经消失了。</figcaption>
</figure>

这张梗图适合提醒本章最重要的习惯：抓取结果必须带着来源一起保存。只保存“答案”很危险，因为答案离开上下文之后，很快会变成一句来路不明的传言。保存标题、URL、访问时间、采集边界和使用提醒，才像科研材料。

<figure align="center">
  <img src="../assets/ch08/ch08_crawl_etiquette_card.png" alt="Python 生成的爬虫礼仪检查卡" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-17 Python 生成的爬虫礼仪检查卡</strong>：公开资料采集前先过 Rules、Pace、Scope、Source、Stop 五关，程序才像研究助手，而不是乱闯资料室的脚本。</figcaption>
</figure>

把爬虫想成一次进图书馆查资料，会更容易理解边界：进门先看公告，走路轻一点，只拿任务需要的资料，摘录时写清来源，遇到“禁止进入”的牌子就停下。网络采集也是一样。`robots.txt`、请求频率、采集范围、来源记录和停止条件，不是给初学者增加难度，而是让你的程序从第一天开始就有分寸。

---

## 第三部分：概念表与脚本导览

### 8.6 关键概念拆解表

| 概念 | 人话理解 | 本章落点 |
| --- | --- | --- |
| HTTP 请求 | 程序拿着 URL 去服务器取资源——就像你给图书馆打电话说"请把这本书递给我"，对方收到请求后把内容传回来 | `02_fetch_python_homepage.py` 使用 `urllib.request` 发起请求 |
| HTML 结构 | 网页不是一张图，而是一棵可以用标签拆开的树——`<a>` 表示链接，`<h1>` 表示标题，`<p>` 表示段落。爬虫做的事就是在这棵树里找到你需要的那根树枝 | `01_local_html_parser.py` 从 `<a>` 标签里取出链接 |
| robots 和边界 | 先看门口规则，再决定能不能进入——每个网站根目录下通常有一个 `robots.txt` 文件，相当于贴在门口的告示："哪些区域欢迎爬虫，哪些区域禁止进入" | 示例读取 `https://www.python.org/robots.txt` |
| 解析标题与链接 | 从网页包裹里拆出真正需要的信息 | 本章先解析链接，后续可以扩展到标题、摘要、图片地址 |
| 保存 CSV | 采集结果要落到文件里，才能复查和分享 | `03_save_links_csv.py` 保存 `output/links.csv` |
| 异常处理 | 网络会失败，网页会变化，程序要留退路 | 后续可加入超时、状态码、重试和日志 |
| 来源卡片 | 链接要变成可判断、可引用、可复查的材料 | `05_make_source_cards.py` 生成来源卡片 |
| 爬虫礼仪 | 能抓不等于该抓，采集前要过边界检查 | `06_make_crawl_etiquette_card.py` 生成礼仪检查卡 |
| 来源可信度 | 能打开只是开始，能复查才算入库 | `07_make_source_quality_scorecard.py` 生成评分卡 |
| 公开资料采集包 | 复习卡片需要可信资料，不能只靠搜索框临时乱找 | `08_make_public_source_bundle.py` 把 ch7 复习卡片转换成可复查的采集任务 |

这张表的作用，是把“我好像懂了”变成“我知道它在哪用”。学习编程时，最危险的状态不是完全不会，而是听解释时点头，自己动手时发呆。每学一个概念，都要强迫自己问一句：它在本章项目里负责哪一段工作？

上表中"HTTP 请求""HTML 结构""robots 和边界"这三个概念涉及网络协议和网页技术，可能听起来有些陌生。简单来说——**HTTP 请求**就是你的程序向远程电脑发出"请把网页内容传给我"的信号，就像你在浏览器地址栏按回车键时，浏览器替你做的第一件事；**HTML**是一套标记语言，用成对出现的标签（如 `<a>...</a>`）把网页内容组织成树状结构，爬虫程序就是沿着这棵树的树枝找到链接和文字；**`robots.txt`** 是网站管理者放在根目录下的一份简短文本文件，相当于贴在门口的告示，告诉访问者哪些区域允许访问、哪些区域禁止访问。这三个概念不理解也没关系，跟着 8.7 节的脚本动手跑一遍，看到输出结果后再回头读这个表，你会觉得它们突然变亲切了。

---

### 8.7 配套代码逐个导览

#### 脚本 1：`01_local_html_parser.py`

运行方式：

```bash
python code/ch08/01_local_html_parser.py
```

**代码做了什么**

这个脚本是本章的"零号动作"——**先不联网，只解析本地 HTML**。它内部直接定义了一段 HTML 字符串（包含一个标题和两个链接），然后用 Python 内置的 `HTMLParser` 类来解析这段字符串。

**代码结构逐段看**

1. **HTML 数据**（第 5-10 行）：脚本开头直接写了一段简短的 HTML，包含一个 `<h1>` 标题和两个 `<a>` 链接。之所以写死在代码里而不是从网络获取，是为了让初学者先排除"网络不通"这个变量，只聚焦于解析本身。
2. **自定义解析器**（第 12-17 行）：定义了一个 `LinkParser` 类，它继承自 `HTMLParser`。这个类只重写了一个方法 `handle_starttag(self, tag, attrs)`——每当解析器遇到一个 HTML 开始标签（比如 `<a>`），就会自动调用这个方法。方法内部判断：如果标签是 `a`，就把 `href` 属性值（即链接地址）添加到 `self.links` 列表中。
3. **执行解析**（第 19-20 行）：创建 `LinkParser` 实例，调用 `parser.feed(HTML)` 就像把 HTML 文本"喂"给解析器，解析器会自动遍历所有标签，遇到 `<a>` 就把链接地址收进列表。

**预期输出**

```
['https://www.python.org/', 'https://docs.python.org/3/']
```

程序会打印出从 HTML 中提取到的两个链接地址。输出虽然简单，但验证了一个核心能力：程序可以从结构化的文本中准确提取指定信息。这个能力是所有爬虫工作的起点。

**为什么放在第一个**

初学者对"爬虫"的第一反应往往是要连接真实网站。但这个脚本故意不联网，只在本地操作。它像先在纸质样张上练习摘录，确认动作稳定后再去真实网页。如果这个脚本能跑通，说明你的 Python 环境是完整的，可以继续往下走。

#### 脚本 2：`02_fetch_python_homepage.py`

运行方式：

```bash
python code/ch08/02_fetch_python_homepage.py
```

**代码做了什么**

这个脚本第一次让 Python **真正联网**——向 Python 官方网站的 `robots.txt` 地址发送请求，并把服务器返回的内容打印出来。

**代码结构逐段看**

1. **导入模块**（第 3 行）：`from urllib.request import Request, urlopen`——这是 Python 标准库中用于发送网络请求的模块，不需要额外安装。
2. **构造请求**（第 5-9 行）：创建一个 `Request` 对象，传入目标 URL `https://www.python.org/robots.txt`，并通过 `headers` 参数设置 `User-Agent`（告诉服务器"我是一个学习爬虫的 Python 脚本"）和 `Accept-Encoding`（告诉服务器"请用原始格式传输，不要压缩"）。设置请求头是一个好习惯，相当于主动打招呼，而不是偷偷摸摸地访问。
3. **发送请求并读取响应**（第 11-15 行）：`urlopen(request, timeout=10)` 向服务器发送请求并等待响应，`timeout=10` 表示最多等 10 秒，超时就报错。成功后，`response` 对象包含三个重要信息：
   - `response.status`：HTTP 状态码，200 表示成功，403 或 404 表示被拒绝或不存在。
   - `response.headers.get("Content-Type")`：返回的内容类型，`text/plain` 表示纯文本，`text/html` 表示网页。
   - `response.read(800).decode("utf-8", errors="replace")`：读取最多 800 字节的响应体，用 UTF-8 解码成可读文字。

**预期输出**

```
状态码： 200
内容类型： text/plain
User-agent: *
Disallow: /  
Allow: /
...
```

状态码是 200，表示请求成功；内容类型是 `text/plain`，说明返回的是纯文本；后面的内容就是 `robots.txt` 的具体规则，它告诉爬虫哪些路径允许访问、哪些不允许。

**为什么要请求 `robots.txt`**

这个脚本故意请求的是 `robots.txt` 而不是首页。`robots.txt` 是网站管理者放在网站根目录下的一个文本文件，相当于贴在门口的告示："哪些区域欢迎爬虫，哪些区域禁止进入"。爬虫开发的第一原则不是"能不能抓"，而是"让不让抓"——`robots.txt` 就是回答这个问题的第一步。

#### 脚本 3：`03_save_links_csv.py`

运行方式：

```bash
python code/ch08/03_save_links_csv.py
```

**代码做了什么**

前两个脚本分别完成了"解析 HTML"和"请求网页"的练习。但这个脚本回答了一个更实际的问题：**采集到的链接怎么保存**？它的做法是把链接写入 CSV 文件——一种可以用 Excel、WPS 或记事本打开的表格格式。

**代码结构逐段看**

1. **准备数据**（第 4-7 行）：在代码中定义了一个包含两个字典的列表，每个字典有 `title`（链接标题）和 `url`（链接地址）两个字段。在实际项目中，这些数据应该来自解析结果，这里先用固定数据演示保存流程。
2. **创建目录**（第 8 行）：`Path("output").mkdir(exist_ok=True)` 确保 `output/` 目录存在。如果目录已存在，`exist_ok=True` 不会报错。
3. **写入 CSV**（第 9-12 行）：用 `csv.DictWriter` 写入 CSV 文件：
   - `fieldnames=["title", "url"]` 定义了两列的表头。
   - `writer.writeheader()` 把表头写入第一行。
   - `writer.writerows(links)` 把列表中的每条数据依次写入后续行。
   - `newline=""` 和 `encoding="utf-8"` 是为了避免中文乱码和多余空行。

**预期输出**

控制台打印 `已保存 output/links.csv`，同时 `output/` 目录下会生成一个 `links.csv` 文件，内容大致如下：

```csv
title,url
Python 官网,https://www.python.org/
Python 文档,https://docs.python.org/3/
```

**为什么 CSV 比直接打印更有用**

直接 `print(links)` 也能看到结果，但关闭终端后就消失了。写入 CSV 文件意味着：数据可以被后续脚本读取、可以被其他工具打开、可以被存档复查。爬虫不是看到链接就结束，只有把结果落到文件里，资料才真正进入卡片工厂。

**建议节奏**

第一次运行时不要急着改代码。先原样运行，确认能看到输出；第二次再改一个最小参数，比如增加一条链接；第三次再尝试把输出写入 `output/` 或 `reports/`。这种节奏比"一上来就大改"更稳。

#### 脚本 4：`04_make_crawl_report.py`

运行方式：

```bash
python code/ch08/04_make_crawl_report.py
```

**代码做了什么**

前一个脚本（`03_save_links_csv.py`）已经能把链接保存为 CSV。但这个脚本走得更远一步：**读取 CSV 文件，生成一份格式化的采集报告**（Markdown 文档 + 预览图片）。

**代码结构逐段看**

1. **读取 CSV**（`load_links` 函数，第 15-18 行）：用 `csv.DictReader` 读取 `output/links.csv` 文件，返回一个字典列表。注意这里先检查文件是否存在——如果不存在，会提示你先运行前一个脚本。这是工程中很重要的"前置依赖检查"。
2. **生成 Markdown 报告**（`make_markdown_report` 函数，第 32-51 行）：在报告中写入采集边界说明（先解析本地 HTML、先看 robots.txt 等），然后以表格形式列出所有链接的标题和 URL。Markdown 文件保存在 `reports/ch08_crawl_report.md`，可以用任何文本编辑器或网页浏览器查看。
3. **生成预览图片**（`make_preview` 函数，第 53-83 行）：用 `PIL`（Pillow 库）创建一个 1500×900 像素的图片。代码中逐行绘制背景、标题、副标题、链接卡片（每个链接带序号、标题和 URL），最后加上检查点提示。这张图片可以让报告"一眼看到全貌"，适合放在学习笔记或项目文档中。

**预期输出**

- `reports/ch08_crawl_report.md`：一个 Markdown 文件，包含采集边界说明和链接表格。
- `reports/ch08_crawl_report_preview.png`：一张预览图片，用卡片样式展示每个链接。

**为什么报告比 CSV 更重要**

CSV 适合给程序读取，但 Markdown 报告和预览图片更适合给**人**阅读。它的意义是把"我抓到了几个链接"升级为"我留下了一份可复查的采集报告"。报告里会写清采集边界、链接清单和检查点，这比单独一个 CSV 更像真正的科研资料整理流程。

#### 脚本 5：`05_make_source_cards.py`

运行方式：

```bash
python code/ch08/05_make_source_cards.py
```

**代码做了什么**

这个脚本在"采集报告"的基础上再往前走一步：**给每条链接打上可信度标签**。它读取 `output/links.csv`，根据链接的域名自动分类——是官方文档、教育机构、开放百科，还是普通网页——然后生成来源卡片式的报告和预览图片。

**代码结构逐段看**

1. **读取链接**（`load_links` 函数，第 45-57 行）：从 `output/links.csv` 读取数据，兼容 `text` 或 `title`、`url` 或 `href` 等不同的列名。如果 CSV 文件不存在，会自动创建一个示例 CSV（`ensure_sample_csv` 函数），方便首次运行时也能看到效果。
2. **自动分类**（`classify` 函数，第 59-65 行）：用 `urlparse` 提取链接的域名，然后按规则判断：
   - `python.org` 或 `.edu` 结尾 → "高可信"（官方/教育来源）
   - `wikipedia.org` 或 `wikimedia.org` → "需交叉验证"（开放百科来源）
   - 其他 → "待检查"（普通网页来源）
   
   这个分类逻辑虽然简单，但它演示了一个关键思维：**不是所有链接的可信度都一样**。在心理学等学科的资料采集中，区分来源类型是第一步。
3. **生成 Markdown 卡片**（`make_markdown` 函数，第 67-87 行）：以表格形式列出每条链接的标题、域名、可信度、使用提醒和 URL，并在末尾附上"采集前自检"的三个问题。
4. **生成预览图片**（`make_preview` 函数，第 89-120 行）：用不同颜色区分可信度（绿色=高可信、橙色=需交叉验证、紫色=待检查），让分类结果一目了然。

**预期输出**

- `reports/ch08_source_cards.md`：来源卡片报告，每行一条链接带可信度标签。
- `output/ch08_source_cards_preview.png`：卡片样式的预览图，颜色区分可信度。

**为什么需要来源卡片**

它把"链接列表"升级成"来源卡片"：标题是什么、域名是什么、可信度如何、引用前要注意什么。对学习者来说，这一步很像给资料贴标签；对科研写作来说，这一步是在给未来的引用和复查铺路。

#### 脚本 6：`06_make_crawl_etiquette_card.py`

运行方式：

```bash
python code/ch08/06_make_crawl_etiquette_card.py
```

**代码做了什么**

前面几个脚本都在处理"能抓什么"，而这个脚本专门处理**"该不该抓"**。它生成一份爬虫礼仪检查卡，把抽象的网络道德拆解成五个可检查、可执行的动作。

**代码结构逐段看**

1. **五个检查点**（`CHECKS` 常量，第 17-23 行）：脚本核心是一个固定的检查清单，包含五项：
   - **Rules（规则）**：先看 `robots.txt` 和网站说明，确认哪些路径允许访问。
   - **Pace（节奏）**：请求要慢一点，别把网站当跑步机——频繁请求会给服务器造成负担。
   - **Scope（范围）**：只取本章任务需要的公开信息，不贪婪。
   - **Source（来源）**：保留标题、URL、访问时间和用途，确保可追溯。
   - **Stop（停止）**：遇到拒绝、错误或敏感数据就停下，不硬闯。
   
   这五个词（Rules, Pace, Scope, Source, Stop）可以当作任何爬虫项目的"起飞前检查清单"。
2. **生成 Markdown 报告**（`make_markdown` 函数，第 42-57 行）：以表格形式列出五个检查点及对应的操作提醒，末尾附上一句话原则。
3. **生成预览图片**（`make_preview` 函数，第 59-88 行）：用五种不同的颜色区分五个检查点，视觉上像一张护照检查卡。
4. **同步到网页目录**（`copy_assets` 函数，第 90-93 行）：把生成的图片复制到 `assets/ch08/web/` 目录，供网页版展示。

**预期输出**

- `reports/ch08_crawl_etiquette_card.md`：礼仪检查卡报告。
- `output/ch08_crawl_etiquette_card.png`：五色检查卡预览图。
- `assets/ch08/web/ch08_crawl_etiquette_card.png`：同步到网页素材目录的副本。

**为什么礼仪检查卡很重要**

它把"爬虫要守规矩"拆成五个可检查动作。以后你写任何采集脚本，都可以先把这五项贴在旁边。它们不是漂亮口号，而是防止脚本失控、材料失真、报告失源的安全带。对心理学学习者来说，这一点尤为重要——采集公开资料时，尊重来源网站的规则和边界，是学术规范的基本素养。

#### 脚本 7：`07_make_source_quality_scorecard.py`

运行方式：

```bash
python code/ch08/07_make_source_quality_scorecard.py
```

**代码做了什么**

这个脚本继续推进"来源可信度"这个主题——**给每条链接打一个质量分数**。它从 `output/links.csv` 读取数据，根据 HTTPS、域名类型、是否为边界页等维度给出 0-4 分的评分，并给出复查理由。

**代码结构逐段看**

1. **评分逻辑**（`score_link` 函数，第 50-62 行）：对每条链接检查三项：
   - 是否使用 HTTPS 协议（+1 分）——加密传输，更安全。
   - 是否是官方/教育来源，如 `python.org` 或 `.edu` 域名（+2 分），或是开放百科如 `wikipedia.org`（+1 分）。
   - 是否包含 `robots.txt` 这类边界页（+1 分）——说明采集者有边界意识。
   
   最高 4 分。分数不是判决书，而是一张复查提醒卡：分数低的链接不一定不能用，但要先说明为什么保留。
2. **生成 Markdown 评分卡**（`make_markdown` 函数，第 64-82 行）：以表格列出每条链接的标题、域名、分数和复查理由。
3. **生成预览图片**（`make_preview` 函数，第 84-119 行）：用颜色区分分数等级（红色=0分，蓝色=4分，渐变表示可信度从低到高）。

**预期输出**

- `reports/ch08_source_quality_scorecard.md`：可信度评分卡报告。
- `output/ch08_source_quality_scorecard.png`：评分卡预览图。

**为什么需要评分卡**

它把"能打开的链接"再往前推进一步：能不能引用？需不需要交叉验证？有没有保存来源和访问时间？爬虫真正进入科研卡片工厂时，链接不能只是蓝色下划线，它要变成能被未来的自己查回去的证据。对心理学学习者来说，区分"看起来像真的"和"有证据是真的"是一项核心学术能力。

#### 脚本 8：`08_make_public_source_bundle.py`

运行方式：

```bash
python code/ch08/08_make_public_source_bundle.py
```

**代码做了什么**

这个脚本是本章跨章节协作的典型例子——**它读取 ch7 的教学反馈小游戏输出，把需要复习的卡片转换成 ch8 可执行的公开资料采集任务**。如果 ch7 的输出文件不存在，它会用一组备用卡片（变量、列表、字典）来演示功能。

**代码结构逐段看**

1. **读取 ch7 输出**（`load_cards` 函数，第 56-63 行）：尝试读取 `python_tutorial_ch07/output/ch07_teaching_feedback_game.json`。如果文件存在且包含卡片数据，就使用它；否则使用 `FALLBACK_CARDS`（变量、列表、字典三个基础概念）。
2. **匹配推荐来源**（`SOURCE_HINTS` 常量，第 33-38 行）：为每个可能的复习主题预置了对应的官方文档链接。例如"变量"对应 Python 官方教程的变量与赋值页面，"字典"对应数据结构页面。如果主题不在预置列表中，会自动生成一条搜索链接。
3. **构建采集包**（`build_bundle` 函数，第 67-85 行）：为每张卡片生成一条采集任务，包含：主题、推荐来源标题和 URL、采集边界（只读页面标题和标题）、入库提醒（保存标题、URL、访问日期和摘要）。
4. **输出 JSON 和 Markdown**（`write_outputs` 函数，第 87-114 行）：同时生成 JSON 格式（供程序读取）和 Markdown 格式（供人阅读）的输出。
5. **生成预览图**（`draw_preview` 函数，第 116-153 行）：用"卡片→来源→规则"的三列流程图展示转换关系，箭头表示"一张复习卡片对应一个采集任务"。

**预期输出**

- `output/ch08_public_source_bundle.json`：结构化的采集包数据，供程序处理。
- `reports/ch08_public_source_bundle.md`：可读的采集包报告。
- `output/ch08_public_source_bundle.png`：预览图。

**为什么这个脚本重要**

它把 ch7 和 ch8 接得更紧：前一章让你和卡片互动，这一章负责给卡片补充可靠来源。一个概念如果答错了，下一步不是随便搜一篇文章，而是优先回到可复查的公开资料。它像一个很冷静的资料管理员：先写清楚要找什么，再决定去哪里找，最后把来源、用途和规则一并保存。

真正的科研资料整理，不是把链接越攒越多，而是让每一条链接都有出处、有用途、有再次检查的理由。

#### 脚本 9：`09_make_source_provenance_archive.py`

运行方式：

```bash
python code/ch08/09_make_source_provenance_archive.py
```

**代码做了什么**

这个脚本扮演**"资料档案管理员"**的角色——它把前面多个脚本的产出（链接 CSV、来源卡片、评分卡、公开资料采集包）整合成一份统一的来源追踪档案，给每条链接补上"身份证"信息。

**代码结构逐段看**

1. **收集数据**（`collect_rows` 函数，第 66-98 行）：同时从两个地方读取数据——`output/links.csv` 中的链接记录，以及 `output/ch08_public_source_bundle.json` 中的采集包记录。对每条记录调用 `score_url` 函数（第 54-64 行）计算可信度分数（HTTPS +2、官方域名 +3、具体路径 +1），并去重合并。
2. **生成 Markdown 档案**（`write_report` 函数，第 100-122 行）：以表格列出每条资料的标题、域名、类型、分数和复查提醒，末尾附上四条使用提醒。
3. **生成预览图片**（`draw_preview` 函数，第 134-183 行）：在图片顶部展示四个统计指标（来源总数、HTTPS 数量、可信来源数量、需复查数量），下方用表格展示每条记录的详情。

**预期输出**

- `reports/ch08_source_provenance_archive.md`：来源追踪档案报告。
- `output/ch08_source_provenance_archive.png`：档案预览图。
- `assets/ch08/web/ch08_source_provenance_archive.png`：同步到网页素材目录。

**为什么需要来源追踪档案**

它的作用是给链接补上"身份证"：标题、URL、域名、来源类型、可信度线索和复查提醒。网络资料最容易出现一种幻觉：只要链接能打开，好像就已经可靠。真正进入学习卡片和科研报告前，还要问清楚它来自哪里、为什么可信、下次能不能查回去。心理学学习里尤其容易遇到"看起来很像知识"的材料——来源追踪档案提醒你先慢下来：先看出处，再看证据，再决定是否进入卡片工厂。

#### 脚本 10：`10_make_scraper_runtime_evidence.py`

运行方式：

```bash
python code/ch08/10_make_scraper_runtime_evidence.py
```

这个脚本会把本章后半段的产物集中检查一遍：

```text
reports/ch08_scraper_runtime_evidence.md
output/ch08_scraper_runtime_evidence.png
assets/ch08/web/ch08_scraper_runtime_evidence.png
```

**代码做了什么**

这个脚本扮演**"成果验收员"**的角色——它不负责"多抓一点网页"，而是负责检查本章所有脚本的产出文件是否已经生成。

**代码结构逐段看**

1. **检查清单**（`CHECKS` 常量，第 32-43 行）：定义了一个包含 10 项产出的清单，从 `output/links.csv`（脚本 3）到 `reports/ch08_source_provenance_archive.md`（脚本 9），覆盖了本章后半段的核心输出。
2. **逐项检查**（`collect_rows` 函数，第 77-86 行）：遍历检查清单中的每个文件路径，用 `path.exists()` 判断文件是否存在，用 `stat().st_size` 获取文件大小。结果分为两种状态：`ready`（已生成）或 `missing`（缺失）。
3. **生成 Markdown 证据清单**（`write_markdown` 函数，第 88-107 行）：以表格列出每个环节的状态、大小和路径，并统计通过项的数量（如 `通过项：8/10`）。
4. **生成预览图片**（`write_preview` 函数，第 109-147 行）：模拟一个终端窗口的外观，用绿色圆点表示"已就绪"，红色圆点表示"缺失"。

**预期输出**

- `reports/ch08_scraper_runtime_evidence.md`：运行证据清单报告，包含通过/缺失统计。
- `output/ch08_scraper_runtime_evidence.png`：模拟终端界面的预览图。
- `assets/ch08/web/ch08_scraper_runtime_evidence.png`：同步到网页素材目录。

**为什么需要运行证据**

它不负责"多抓一点网页"，而是负责确认已经抓到、整理好、能复查的东西有没有保存下来。对爬虫来说，这一步很关键：没有运行证据，采集结果很容易从"资料"退化成"我印象里好像跑过"。就像做实验要写实验日志一样，做爬虫也要保留运行证据——这样一周后回头看，你还能清楚地知道哪些脚本跑成功了、产出了哪些文件。

---

## 第四部分：排错、项目与来源证据

### 8.8 常见坑

<figure align="center">
  <img src="../assets/ch08/ch08_pitfall_map.png" alt="常见坑地图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-18 常见坑地图</strong>：错误不是判决，而是提醒你该检查路径、输入、状态或依赖。</figcaption>
</figure>

本章常见坑：

- 无视网站规则
- 请求太频繁
- 把页面显示和 HTML 源码混为一谈
- 编码处理不当

遇到问题时，先看报错信息，再看文件路径，最后看输入数据。不要一报错就重装环境。重装是最后手段，不是第一反应。

---

### 8.9 本章小项目：公开资料采集器

<figure align="center">
  <img src="../assets/ch08/ch08_project_dashboard.png" alt="项目仪表盘" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-19 本章项目</strong>：完成“公开资料采集器”，给科研卡片工厂增加一项新能力。</figcaption>
</figure>

项目目标：用本地 HTML 练习解析，理解如何请求网页、保存标题和链接，并生成一份可复查的采集报告。

<figure align="center">
  <img src="../assets/ch08/ch08_crawl_report_preview.png" alt="Python 生成的公开资料采集报告预览" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-20 Python 生成的采集报告预览</strong>：这张图由 `04_make_crawl_report.py` 生成，展示链接清单和采集边界检查点。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch08/ch08_source_cards_preview.png" alt="Python 生成的公开资料来源卡片预览" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-21 Python 生成的来源卡片预览</strong>：来源卡片让链接从“能点开”变成“能判断、能引用、能复查”。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch08/ch08_source_quality_scorecard.png" alt="Python 生成的来源可信度评分卡" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-22 Python 生成的来源可信度评分卡</strong>：链接不是越多越好，真正能入库的资料要经得起来源、边界和复查理由的检查。</figcaption>
</figure>

这张图来自 `07_make_source_quality_scorecard.py`。它把“资料判断”做成一个可执行动作：先看域名，再看协议，再看来源类型，最后写下为什么需要复查。对心理学和课程材料来说，这一步很重要：一个看起来很顺眼的网页，如果没有来源、时间和边界说明，就像没有标签的实验样本，暂时能用，长期会乱。

如果你已经运行过 ch7 的 `09_make_teaching_feedback_game.py`，本章还可以直接读取上一章的复习卡片，把它们转换成一份公开资料采集包。这样，小游戏里需要复习的概念不会停在屏幕上，而是继续进入“找资料、留来源、做卡片”的工作流。

运行方式：

```bash
python code/ch08/08_make_public_source_bundle.py
```

运行后会生成：

```text
output/ch08_public_source_bundle.json
reports/ch08_public_source_bundle.md
output/ch08_public_source_bundle.png
```

<figure align="center">
  <img src="../assets/ch08/ch08_public_source_bundle.png" alt="Python 生成的公开资料采集包" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-23 Python 生成的公开资料采集包</strong>：`08_make_public_source_bundle.py` 读取 ch7 的复习卡片，把每张卡片连接到来源、采集边界和入库提醒。</figcaption>
</figure>

这一步把 ch7 和 ch8 接得更紧：前一章让你和卡片互动，这一章负责给卡片补充可靠来源。一个概念如果答错了，下一步不是随便搜一篇文章，而是优先回到可复查的公开资料。学习卡片工厂因此多了一项很重要的能力：不是只会“收集”，而是会“有证据地收集”。

运行 `09_make_source_provenance_archive.py` 后，本章会再生成一份来源追踪档案：

```text
reports/ch08_source_provenance_archive.md
output/ch08_source_provenance_archive.png
```

<figure align="center">
  <img src="../assets/ch08/ch08_source_provenance_archive.png" alt="Python 生成的来源追踪档案" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图8-24 Python 生成的来源追踪档案</strong>：`09_make_source_provenance_archive.py` 把链接、域名、来源类型、可信度线索和复查提醒集中到一张可检查总览里。</figcaption>
</figure>

这张图是本章的“资料出入库记录”。如果把网页链接当成图书馆里的书，来源追踪档案就像借书卡：书名、位置、编号、是否可靠、以后怎么找回来，都要写清楚。没有这一步，爬虫很容易变成“今天抓到一堆，明天忘了哪堆能用”。

心理学学习里尤其容易遇到“看起来很像知识”的材料：一张漂亮的信息图、一段流畅的解释、一个转发很多的结论。它们可能有用，也可能只是包装得很顺眼。来源追踪档案提醒你先慢下来：先看出处，再看证据，再决定是否进入卡片工厂。

项目结构可以这样安排：

```text
python_card_factory/
├── code/
│   └── ch08/
├── input/
├── output/
├── reports/
└── assets/
```

本章配套脚本：

- `code/ch08/01_local_html_parser.py`
- `code/ch08/02_fetch_python_homepage.py`
- `code/ch08/03_save_links_csv.py`
- `code/ch08/04_make_crawl_report.py`
- `code/ch08/05_make_source_cards.py`
- `code/ch08/06_make_crawl_etiquette_card.py`
- `code/ch08/07_make_source_quality_scorecard.py`
- `code/ch08/08_make_public_source_bundle.py`
- `code/ch08/09_make_source_provenance_archive.py`
- `code/ch08/10_make_scraper_runtime_evidence.py`

完成标准：

1. 能按顺序运行 `01_local_html_parser.py` 到 `10_make_scraper_runtime_evidence.py`。
2. 能解释脚本输入、处理、输出分别是什么。
3. 把生成结果保存到 `output/` 或 `reports/`。
4. 在 README 或学习记录中写下运行命令。
5. 能说明为什么 `robots.txt`、来源记录和采集报告都很重要。
6. 能生成 `reports/ch08_source_cards.md` 和 `output/ch08_source_cards_preview.png`。
7. 能生成 `reports/ch08_crawl_etiquette_card.md`，并说明 Rules、Pace、Scope、Source、Stop 分别检查什么。
8. 能生成 `reports/ch08_source_quality_scorecard.md` 和 `output/ch08_source_quality_scorecard.png`，并解释至少一条链接为什么需要复查。
9. 能生成 `reports/ch08_public_source_bundle.md` 和 `output/ch08_public_source_bundle.json`，并说明 ch7 的复习卡片怎样变成 ch8 的采集任务。
10. 能生成 `reports/ch08_source_provenance_archive.md` 和 `output/ch08_source_provenance_archive.png`，并说明为什么“能打开”不等于“能引用”。
11. 能生成 `reports/ch08_scraper_runtime_evidence.md` 和 `output/ch08_scraper_runtime_evidence.png`，并用它检查本章采集结果是否齐全。

动手步骤：

1. **准备目录**：确认 `python_card_factory/` 下有 `code/`、`input/`、`output/`、`reports/`。
2. **运行最小脚本**：先运行本章第一个脚本，得到一个确定反馈。
3. **记录环境**：把 Python 版本、运行命令和输出截图或输出文本写进 `reports/`。
4. **连接真实材料**：把课程笔记、实验记录、图片、网页或 CSV 放进 `input/`。
5. **生成作品**：让脚本在 `output/` 或 `reports/` 中留下文件。
6. **制作来源卡片**：运行 `05_make_source_cards.py`，检查每条链接是否有标题、域名和使用提醒。
7. **检查采集边界**：运行 `06_make_crawl_etiquette_card.py`，把礼仪检查卡写进本章复盘。
8. **评估来源质量**：运行 `07_make_source_quality_scorecard.py`，说明哪些链接可以直接引用，哪些需要交叉验证。
9. **生成采集包**：运行 `08_make_public_source_bundle.py`，把 ch7 的复习卡片转换成公开资料采集计划。
10. **生成来源追踪档案**：运行 `09_make_source_provenance_archive.py`，把链接变成可复查证据。
11. **生成运行证据**：运行 `10_make_scraper_runtime_evidence.py`，检查 CSV、报告、来源卡片、评分卡、采集包和追踪档案是否齐全。
12. **写复盘**：说明这章让卡片工厂多了什么能力，哪些地方还容易出错。

---

## 第五部分：练习、复盘与后续连接

### 8.10 练习任务

1. 修改一个输入参数，观察输出变化。
2. 把脚本生成的结果保存成文件。
3. 故意制造一个小错误，记录报错信息和修复方式。
4. 把本章项目和前面章节连接起来，例如读取 ch03 整理出的文件，或使用 ch02 的数据结构保存结果。
5. 把 `links.csv` 换成 3 个心理学公开资料链接，再重新生成采集报告。
6. 给每条链接加一句“为什么值得采集”，再重新生成来源卡片。
7. 运行 `06_make_crawl_etiquette_card.py`，给自己的采集任务写一句停止条件：遇到什么情况必须停下？
8. 运行 `07_make_source_quality_scorecard.py`，挑一条低分链接，写出你会怎样交叉验证它。
9. 打开 `output/ch08_public_source_bundle.json`，给其中一张卡片补充一个更适合学习分享的公开资料链接。
10. 运行 `09_make_source_provenance_archive.py`，挑一条低分来源，写出它缺少哪类证据。
11. 运行 `10_make_scraper_runtime_evidence.py`，如果某一项变成 `missing`，追踪它对应的是哪一个脚本或文件路径。

---

### 8.11 自测问题

1. 本章最重要的三个概念是什么？请用人话解释，不要只背术语。
2. 本章第一个脚本的输入、处理、输出分别是什么？
3. 如果脚本运行失败，你第一步会检查路径、环境、依赖还是语法？为什么？
4. 本章项目和“科研卡片工厂”有什么关系？
5. 你能不能把本章项目改成一个心理学或学习分享场景的小任务？

参考回答不唯一。判断自己是否真的理解，可以看你能不能把答案讲给一个完全没学过本章的人听。

---

### 8.12 学习复盘模板

可以在 `reports/ch08_review.md` 中写下：

```markdown
# 第8章复盘

## 我新增的能力
- 

## 我跑通的脚本
- 

## 我遇到的报错
- 报错信息：
- 原因：
- 修复方式：

## 我能迁移到哪里
- 心理学实验：
- 学习分享：
- 科研资料整理：
```

复盘不是写作文，而是给未来的自己留路标。你现在记录清楚，后面做综合项目时就不用重新从记忆里翻箱倒柜。

---

### 8.13 与后续章节的连接

本章不是孤岛。它和整套教程的关系可以这样理解：

- 前面章节提供基础：环境、数据结构、文件管理。
- 本章提供一项新能力：公开资料采集器。
- 后面章节会把这项能力继续接到数据分析、图像处理、报告生成和办公自动化里。

所以不要只问“这一章考试考什么”。更好的问题是：它能帮我少做哪一类重复劳动？它能让我的学习材料、实验记录或报告更稳定吗？

---

### 8.14 本章总结

网络爬虫开发实战的关键不是“记住所有 API”，而是理解它解决的问题。你已经从概念、图像、代码和小项目四个角度接触了本章内容。下一次复习时，不要只问“我会不会背”，而要问：

- 我能不能讲出这个概念的比喻？
- 我能不能运行一个最小脚本？
- 我能不能把结果放进项目目录？
- 我能不能说清楚它在科研卡片工厂里增加了什么能力？

如果答案是肯定的，这一章就不是看过了，而是真的进入你的工具箱了。

真正会写爬虫的人，不只是会把网页内容拿下来，还知道什么时候慢一点、少一点、停一下。能抓到链接是技术，能保留来源是习惯，能尊重边界是专业。公开资料采集器最好的状态，不是“抓得多”，而是“抓得清楚、抓得有据、抓得让未来的自己能复查”。
