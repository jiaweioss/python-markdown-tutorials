# 第 4 章：Tkinter 图形界面编程

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
  <img src="../assets/ch04/ch04_cover.png" alt="第4章封面" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-1 本章封面</strong>：命令行像后厨，GUI 像前台。用户不想进后厨看你切菜，他只想点按钮上菜。</figcaption>
</figure>

> 本章一句话：命令行像后厨，GUI 像前台。用户不想进后厨看你切菜，他只想点按钮上菜。

第4章继续推进“科研卡片工厂”的能力建设。前面几章让 Python 能运行、能管理数据、能处理文件；这一章开始把能力放进更具体的应用场景里。学习时不要把知识点当成散装零件，而要始终问：它能帮我的卡片工厂多做哪一件真实的事？

---

## 4.0 本章学习目标

学完本章，你应该能够：

1. 用自己的话解释本章核心概念。
2. 运行本章配套脚本，看到明确输出。
3. 把概念和“科研卡片工厂”的连续项目联系起来。
4. 识别本章最常见的新手错误。
5. 完成本章小项目：**科研卡片工厂控制面板**。

---

## 4.1 开场故事：先有画面，再有术语

命令行像后厨，GUI 像前台。用户不想进后厨看你切菜，他只想点按钮上菜。 这句话不是为了热闹，而是为了把本章的知识放进真实使用场景。初学者最怕一上来就被术语包围，像走进一个所有门牌都用缩写写成的楼层。我们先从画面进入，再慢慢把画面翻译成代码。

<figure align="center">
  <img src="../assets/ch04/ch04_story_scene.png" alt="故事场景图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-2 故事场景</strong>：GUI 像给程序穿衣服：窗口是外套，按钮是门铃，输入框是表单，回调函数是按下门铃后真正发生的动作。</figcaption>
</figure>

这个画面对应本章的核心比喻：GUI 像给程序穿衣服：窗口是外套，按钮是门铃，输入框是表单，回调函数是按下门铃后真正发生的动作。 如果你能先记住这个比喻，后面的概念就不再是干巴巴的定义。

<figure align="center">
  <img src="../assets/ch04/ch04_history_xerox_alto.png" alt="Xerox Alto计算机照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-3 Xerox Alto计算机照片</strong>：图形界面的历史提醒我们，窗口、鼠标和按钮不是装饰品，而是为了让人更自然地操作计算机。</figcaption>
</figure>

GUI 的故事不是“让程序好看一点”这么简单。

早期计算机更像一台严肃的机器：你要输入命令，等待结果，再输入下一条命令。后来窗口、图标、鼠标和菜单开始出现，人和计算机之间多了一层“可看见、可点击、可试错”的界面。对初学者来说，这层界面尤其重要：它把“我会不会敲命令”改成了“我能不能完成任务”。

本章使用 Tkinter，不是为了追求最炫的界面，而是为了让你第一次把 Python 写成一个别人可以点击的小工具。

<figure align="center">
  <img src="../assets/ch04/ch04_engelbart_mouse_story.png" alt="Engelbart原型鼠标照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-4 Engelbart原型鼠标照片</strong>：鼠标把“输入命令”变成了“指向并点击”；Tkinter 的按钮和回调函数，也是在延续这种交互思想。</figcaption>
</figure>

一个按钮看起来很小，但它改变了程序的使用方式。用户不需要知道函数名，也不需要记住命令格式，只要点一下“保存卡片”，程序就执行对应的函数。

这就是 GUI 的核心：把函数包装成可操作的界面动作。

<figure align="center">
  <img src="../assets/ch04/ch04_macintosh_gui_story.png" alt="Macintosh 128K 电脑照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-5 Macintosh 128K</strong>：当图形界面进入普通人的桌面，计算机不再只像工程机器，也开始像可以探索的工作台。</figcaption>
</figure>

Macintosh 128K 的历史意义，不只是“它是一台经典电脑”。它代表一种交互思想：用户可以通过窗口、菜单、图标和鼠标去探索系统，而不是先背一大串命令。对初学者来说，这种变化很重要，因为 GUI 把“我记不记得命令”变成了“我能不能看懂并完成动作”。

Tkinter 的窗口很朴素，当然不能和成熟商业软件相比。但朴素有朴素的好处：你能清楚看到一个窗口怎样被创建，一个按钮怎样绑定函数，一个输入框怎样把用户内容交给程序。它像一间小木屋，结构看得见，适合学习怎么盖房子。

<figure align="center">
  <img src="../assets/ch04/ch04_hypercard_story.png" alt="HyperCard 软件照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-6 HyperCard</strong>：卡片式界面让很多非专业程序员第一次感到，自己也能组织信息、设计交互、做出作品。</figcaption>
</figure>

HyperCard 的名字今天听起来可能有点陌生，但它的思想很接近这一章要做的“科研卡片工厂控制面板”：把信息组织成一张张卡片，用按钮、链接和脚本把卡片串起来。你可以把它理解成早期的“低门槛交互创作工具”。很多人不是从大型工程开始接触编程，而是从“我想做一个能点的卡片”开始的。

这也解释了为什么本章项目不是一上来做复杂系统，而是做一个学习卡片表单。表单很小，但它已经包含 GUI 的关键能力：输入、保存、反馈。卡片工厂如果有了图形界面，就不再只服务会敲命令的人，也能服务想专心整理材料的人。

<figure align="center">
  <img src="../assets/ch04/ch04_susan_kare_icon_story.png" alt="Susan Kare 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-7 Susan Kare</strong>：好图标像一盏小路灯，把抽象命令变成用户能立刻识别的动作。</figcaption>
</figure>

Susan Kare 参与设计了早期 Macintosh 的许多经典图标。图标的价值不只是“可爱”，而是降低理解成本：垃圾桶让删除变得可见，磁盘让保存变得可见，笑脸让系统状态变得亲切。一个好图标能让用户少读一行说明，少猜一次操作。

Tkinter 初学阶段未必马上设计复杂图标，但这个故事很有用：按钮文字、窗口标题、提示语，本质上都在做同一件事——把程序内部动作翻译成人能理解的信号。界面不是给程序穿花衣服，而是给用户铺路。

<figure align="center">
  <img src="../assets/ch04/ch04_don_norman_story.png" alt="Don Norman 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-8 Don Norman</strong>：好界面不是把功能藏得很高级，而是让用户知道能做什么、做完后发生了什么。</figcaption>
</figure>

Don Norman 在设计和用户体验领域影响很大。他反复强调的一个核心思想是：好的设计应该让人少猜。门把手应该暗示推还是拉，按钮应该暗示能不能点，操作之后应该有反馈。换到 Tkinter 里，就是标签要说明输入框是什么，按钮文字要具体，保存成功要给提示。

<figure align="center">
  <img src="../assets/ch04/ch04_norman_door_affordance.png" alt="门的可发现性示意图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-9 门的可发现性</strong>：一个推板、一个拉手，不用解释太多，身体已经知道该怎么做。GUI 里的按钮、输入框和状态提示也应该有这种“看一眼就知道下一步”的线索。</figcaption>
</figure>

你一定见过那种门：一边装着大把手，却偏偏要推；另一边贴着说明，却越看越心虚。这类门后来常被拿来调侃为“Norman door”。它好笑，是因为每个人都在门前短暂怀疑过自己；它重要，是因为它说明一个朴素原则：**用户迟疑的地方，就是界面应该多给线索的地方**。

写 GUI 时，`Button(text="确定")` 不一定够好。确定什么？保存到哪里？失败会不会覆盖旧文件？如果按钮旁边有明确文案、点击后有反馈、保存后显示路径，用户的大脑就少背一件事。好的界面不是让人显得聪明，而是让人不用把注意力浪费在猜谜上。

所以本章写 GUI 时，不要只问“按钮能不能运行”，还要问“用户看见它会不会懂”。如果一个窗口能运行，但用户不知道下一步该点哪里，它就像一个沉默的服务员：菜做得出来，但菜单写得像谜语。

---

## 4.2 知识路线

<figure align="center">
  <img src="../assets/ch04/ch04_roadmap.png" alt="知识路线图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-10 知识路线</strong>：先建立直觉，再运行代码，最后完成一个可展示的小项目。</figcaption>
</figure>

本章路线如下：

| 顺序 | 主题 | 你要完成的动作 |
| --- | --- | --- |
| 1 | 窗口与主循环 | 先让一个窗口真正停在屏幕上 |
| 2 | Label/Button/Entry/Text | 再把文字、按钮和输入区摆进窗口 |
| 3 | 布局管理 | 让控件有秩序，不挤成一团 |
| 4 | 事件与回调 | 点击按钮后，让函数真的开始工作 |
| 5 | 消息框 | 保存成功或出错时，给用户明确反馈 |
| 6 | 小型 GUI 项目 | 做出科研卡片工厂的第一块控制面板 |

---

## 4.3 核心概念：从人话到术语

<figure align="center">
  <img src="../assets/ch04/ch04_core_metaphor.png" alt="核心比喻图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-11 核心比喻</strong>：用一个稳定画面记住本章最重要的概念关系。</figcaption>
</figure>

先用人话说：GUI 像给程序穿衣服：窗口是外套，按钮是门铃，输入框是表单，回调函数是按下门铃后真正发生的动作。

再用术语说，本章要掌握这些内容：

- **窗口与主循环**：窗口是舞台，`mainloop()` 让舞台不要刚亮灯就关掉。
- **Label/Button/Entry/Text**：这些控件负责显示、点击和收集输入，是 GUI 里的基本家具。
- **布局管理**：决定控件摆在哪里，避免按钮和输入框像临时堆在桌角。
- **事件与回调**：用户点击或按键后，程序调用对应函数。
- **消息框**：操作完成后给出反馈，让用户知道“刚才那一下到底有没有成功”。
- **小型 GUI 项目**：把前面这些控件合成一个能保存卡片的小工具。

术语不是用来吓人的，它只是为了让大家交流时不用每次都讲一长串故事。你先用故事建立直觉，再用术语压缩表达，这样学得稳。

Tkinter 的最小心智模型可以压成四句话：

1. `Tk()` 创建一个窗口。
2. 控件负责显示或收集信息。
3. 布局管理器决定控件摆在哪里。
4. `mainloop()` 让窗口持续响应用户动作。

```python
import tkinter as tk

root = tk.Tk()
root.title("科研卡片工厂控制台")

label = tk.Label(root, text="第一块 GUI 面板已经亮灯")
label.pack()

root.mainloop()
```

这里最容易漏掉的是 `mainloop()`。没有它，窗口就像刚开灯又立刻关灯，你甚至来不及看清屋里有什么。

---

## 4.4 最小可运行示例

<figure align="center">
  <img src="../assets/ch04/ch04_minimal_demo.png" alt="最小示例图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-12 最小示例</strong>：先跑通最小代码，再逐步增加功能，学习会稳很多。</figcaption>
</figure>

本章第一件事不是背参数，而是运行一个最小例子。打开终端，进入本章目录后运行：

```bash
python code/ch04/01_hello_window.py
```

如果你能看到输出，说明这一章的入口已经打通。后面所有复杂功能，都是在这个入口上慢慢加能力。

<figure align="center">
  <img src="../assets/ch04/ch04_tkinter_hello_window_screenshot.png" alt="Tkinter最小窗口真实截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-13 Tkinter最小窗口真实截图</strong>：这就是 `01_hello_window.py` 真实弹出的窗口，标题、文字和按钮都来自 Python 代码。</figcaption>
</figure>

看到这个窗口时，可以顺手做一个小拆解：

- 标题栏来自 `root.title("科研卡片工厂控制台")`。
- 中间那行文字来自 `tk.Label(...)`。
- “收到”按钮来自 `tk.Button(...)`。
- 点击按钮后窗口关闭，是因为按钮的 `command` 绑定了 `root.destroy`。

GUI 的神秘感就从这里消失了：窗口里的每个东西，都能在代码里找到它的来源。

---

## 4.5 与心理学和科研任务的连接

<figure align="center">
  <img src="../assets/ch04/ch04_psychology_link.png" alt="心理学和科研任务连接图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-14 心理学连接</strong>：把本章能力放进实验、记录、分析和学习分享的真实任务里。</figcaption>
</figure>

这一章会把例子贴近心理学、科研记录和学习分享。因为这些任务天然需要清晰流程：刺激是什么，反应是什么，数据存到哪里，结果如何展示，别人能不能复现。

在本章里，你可以这样理解项目价值：

- 它不是孤立练习，而是科研卡片工厂的一台新设备。
- 它处理的材料可以是课程笔记、实验记录、问卷结果、图片、网页资料或报告模板。
- 它最终要留下可检查的结果，而不是只在屏幕上闪一下。

---

## 4.6 关键概念拆解表

| 概念 | 人话理解 | 本章落点 |
| --- | --- | --- |
| 窗口与主循环 | 窗口是舞台，`mainloop()` 是持续开场的剧场灯 | `01_hello_window.py` 创建根窗口并保持响应 |
| Label | 只负责显示文字，像贴在界面上的说明牌 | 显示“主题”“要点”“点击开始后看刺激” |
| Entry | 单行输入框，适合主题、姓名、编号这类短文本 | 输入学习卡片主题 |
| Text | 多行输入区，适合笔记、要点、实验说明 | 输入学习卡片正文 |
| Button | 用户点击以后触发一个函数 | “保存卡片”按钮调用 `save_card()` |
| 布局管理 | 决定控件摆放位置，像安排桌面上的工具 | 本章先用 `pack()`，后续可以再学 `grid()` |
| 事件与回调 | 用户动作发生后，程序执行对应函数 | 按钮点击、键盘 `f` / `j` 响应 |
| 消息框 | 操作完成后给用户一个确认反馈 | 保存卡片后弹出“已保存”提示 |
| 交互旅程 | 用户从打开窗口到拿到文件的完整路径 | `09_make_gui_journey_storyboard.py` 生成旅程图 |

这张表的作用，是把“我好像懂了”变成“我知道它在哪用”。学习编程时，最危险的状态不是完全不会，而是听解释时点头，自己动手时发呆。每学一个概念，都要强迫自己问一句：它在本章项目里负责哪一段工作？

---

## 4.7 配套代码逐个导览

### 脚本 1：`01_hello_window.py`

运行方式：

```bash
python code/ch04/01_hello_window.py
```

阅读时重点看三件事：输入从哪里来，处理步骤在哪里，结果输出到哪里。不要只盯着语法，要把它当成一条小流水线。

### 脚本 2：`02_card_form.py`

运行方式：

```bash
python code/ch04/02_card_form.py
```

阅读时重点看三件事：输入从哪里来，处理步骤在哪里，结果输出到哪里。不要只盯着语法，要把它当成一条小流水线。

<figure align="center">
  <img src="../assets/ch04/ch04_tkinter_card_form_screenshot.png" alt="Tkinter学习卡片表单真实截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-15 Tkinter学习卡片表单真实截图</strong>：`Entry` 收集主题，`Text` 收集要点，按钮把内容写入本地 Markdown 卡片。</figcaption>
</figure>

这个窗口就是“科研卡片工厂控制面板”的雏形：左看很朴素，右看很有用。你输入主题和要点，点击保存，程序就在 `cards/` 目录下生成一张 Markdown 卡片。

对应的关键代码是：

```python
topic = topic_entry.get().strip() or "未命名主题"
idea = idea_text.get("1.0", "end").strip()
file.write_text(f"# {topic}\n\n{idea}\n", encoding="utf-8")
```

这里能同时复习 ch2 和 ch3：字符串负责文本，路径负责文件位置，写入操作负责留下成果。

### 脚本 3：`03_stroop_gui_preview.py`

运行方式：

```bash
python code/ch04/03_stroop_gui_preview.py
```

阅读时重点看三件事：输入从哪里来，处理步骤在哪里，结果输出到哪里。不要只盯着语法，要把它当成一条小流水线。

<figure align="center">
  <img src="../assets/ch04/ch04_tkinter_stroop_screenshot.png" alt="Tkinter Stroop窗口真实截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-16 Tkinter Stroop窗口真实截图</strong>：心理学实验界面通常需要刺激、按键反应和反应时记录；这个小窗口先把交互骨架跑通。</figcaption>
</figure>

Stroop 任务是心理学里很经典的冲突任务：你看到一个词，例如 `RED`，但它可能用蓝色墨水显示。此时真正要判断的是墨水颜色，而不是词义。这个例子非常适合 GUI 入门，因为它天然包含三个交互元素：

1. 程序显示刺激。
2. 用户按键反应。
3. 程序记录反应是否正确和反应时。

在代码里，`root.bind("f", ...)` 和 `root.bind("j", ...)` 就是在告诉窗口：当用户按下某个键时，调用哪个函数。

建议第一次运行时不要急着改代码。先原样运行，确认能看到输出；第二次再改一个最小参数；第三次再尝试把输出写入 `output/` 或 `reports/`。这种节奏比“一上来就大改”更稳。


GUI 章尤其需要一张“运行证据图”。因为窗口截图只能证明界面长什么样，运行证据才能证明窗口、检查报告、交互回执和跨章节面板都已经落成文件。

<figure align="center">
  <img src="../assets/ch04/ch04_gui_runtime_evidence.png" alt="GUI 运行证据图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-17 PowerShell 风格的 GUI 运行证据</strong>：`10_make_gui_runtime_evidence.py` 会核对 Tkinter 窗口截图、可用性报告、交互回执、卡片交付物、ch3 数据面板和交互旅程图，让“窗口能弹出”升级为“项目有证据链”。</figcaption>
</figure>

这张图的价值不是再添一张漂亮截图，而是帮你建立工程习惯：每做完一个 GUI 小工具，都能回答三个问题：用户看到了什么，点击后发生了什么，最后有哪些文件留下来。GUI 学习一旦有了证据链，就不再只是控件摆放练习，而是能被复查、能被交付的小系统。

### 脚本 4：`04_gui_usability_check.py`

运行方式：

```bash
python code/ch04/04_gui_usability_check.py
```

这个脚本不会弹出新窗口，而是生成一份 GUI 可用性检查清单：

```text
reports/ch04_gui_usability_check.md
output/ch04_gui_usability_check.png
```

它的作用是把“界面好不好用”变成可以逐条检查的问题。比如：用户能不能看懂窗口用途？输入框标签是否清楚？主按钮是否容易找到？保存后有没有反馈？这比一句“界面要友好”更可执行。

### 脚本 5：`05_make_gui_feedback_lab.py`

运行方式：

```bash
python code/ch04/05_make_gui_feedback_lab.py
```

这个脚本继续追问一个更细的问题：**窗口能用了以后，用户用得舒服吗？** GUI 初学者很容易把注意力放在“控件有没有出现”，但真实使用中，另一些细节更要命：按钮是不是太小，按钮之间是不是挤成一团，用户点击后有没有看到反馈，出错时能不能恢复。

<figure align="center">
  <img src="../assets/ch04/ch04_target_feedback_lab.png" alt="GUI目标大小与反馈实验图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-18 GUI目标大小与反馈实验</strong>：同样是按钮，目标大小、间距和操作反馈会直接影响用户是否紧张、是否误点、是否敢继续操作。</figcaption>
</figure>

你可以把这张图看成一个小小的“界面心理学实验”。左侧的按钮太小、太挤，用户每点一次都像在夹娃娃机里夹最后一枚硬币；右侧按钮更大、间距更清楚，并且保存后有状态提示，用户就会更安心。

这不是审美洁癖，而是认知负荷。用户已经在思考任务本身了，界面就不要再让他额外猜：“我该点哪里？”“刚才成功了吗？”“点错了能回来吗？” 一个好 GUI 的温柔，常常体现在它少让人猜几次。

<figure align="center">
  <img src="../assets/ch04/ch04_gui_feedback_scorecard.png" alt="GUI反馈检查卡" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-19 GUI反馈检查卡</strong>：把 Target、Spacing、State、Error、Copy 当成五个检查点，窗口交给别人前先自己过一遍。</figcaption>
</figure>

脚本运行后会生成：

```text
output/ch04_target_feedback_lab.png
output/ch04_gui_feedback_scorecard.png
reports/ch04_gui_feedback_scorecard.md
```

这三个文件让本章项目多了一层“验收感”：不仅能做窗口，还能用一张检查卡判断窗口是否真的适合给别人使用。

### 脚本 6：`06_make_interaction_receipt.py`

运行方式：

```bash
python code/ch04/06_make_interaction_receipt.py
```

这个脚本把本章 GUI 小项目最后整理成一张“交互回执”。窗口能弹出来只是开门，交互回执说明用户真正走进去以后有没有路标、按钮、反馈和出口。对初学者来说，这一步特别重要：它把“我做了一个界面”推进到“我能证明这个界面被检查过”。

<figure align="center">
  <img src="../assets/ch04/ch04_interaction_receipt.png" alt="GUI交互回执预览图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-20 Python 生成的 GUI 交互回执</strong>：`06_make_interaction_receipt.py` 会生成一张交互回执，把运行脚本、保存证据和下一步改进放在同一张图里。</figcaption>
</figure>

脚本运行后会生成：

```text
output/ch04_interaction_receipt.png
reports/ch04_interaction_receipt.md
```

这张回执故意保留一个 `FIX`：空标题提示还需要更友好。真实项目不是每次都满分，真正有价值的是知道下一步该改哪里。GUI 学习也一样，能发现问题，已经比“看起来差不多”更接近工程实践。

---

## 4.8 常见坑

<figure align="center">
  <img src="../assets/ch04/ch04_pitfall_map.png" alt="常见坑地图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-21 常见坑地图</strong>：错误不是判决，而是提醒你该检查路径、输入、状态或依赖。</figcaption>
</figure>

本章常见坑：

- 忘记 mainloop()
- 回调函数写成了立即执行
- 控件创建了但没有布局
- 界面逻辑和业务逻辑混在一起

遇到问题时，先看报错信息，再看文件路径，最后看输入数据。不要一报错就重装环境。重装是最后手段，不是第一反应。

---

## 4.9 本章小项目：科研卡片工厂控制面板

<figure align="center">
  <img src="../assets/ch04/ch04_project_dashboard.png" alt="项目仪表盘" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-22 本章项目</strong>：完成“科研卡片工厂控制面板”，给科研卡片工厂增加一项新能力。</figcaption>
</figure>

项目目标：做一个能输入主题、生成学习卡片草稿并保存文件的 Tkinter 小窗口。

但 GUI 的终点不是“窗口弹出来了”。窗口只是柜台，真正的交付物是柜台后面生成的卡片、报告和证据。为了让本章项目更像一个能交付的小作品，本章再补一个非交互脚本：它会生成一张“工作记忆负荷”学习卡片，并把卡片路径、摘要和下一步改进整理成项目回执。

运行方式：

```bash
python code/ch04/07_make_card_factory_delivery.py
```

运行后会生成：

```text
cards/working_memory_load_card.md
reports/ch04_card_factory_delivery.md
output/ch04_card_factory_delivery.png
```

<figure align="center">
  <img src="../assets/ch04/ch04_card_factory_delivery.png" alt="卡片工厂交付回执" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-23 卡片工厂交付回执</strong>：GUI 项目最后要留下可打开的卡片和报告；界面负责收集输入，Python 负责把输入变成真实文件。</figcaption>
</figure>

这张回执把 ch0 的“科研卡片工厂”主线往前推进了一步：前几章已经会运行代码、处理数据和管理文件；到本章，程序终于有了一个面向用户的入口。用户不必知道文件写入函数叫什么，只要把主题和要点填进去，程序就能在 `cards/`、`reports/` 和 `output/` 里留下成果。

<figure align="center">
  <img src="../assets/ch04/ch04_gui_journey_storyboard.png" alt="Python 生成的 GUI 交互旅程图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-24 Python 生成的 GUI 交互旅程图</strong>：`09_make_gui_journey_storyboard.py` 把打开窗口、输入内容、点击按钮、看到反馈和得到文件连成一条用户旅程。</figcaption>
</figure>

这张旅程图提醒你：GUI 的好坏不只看窗口截图漂不漂亮，而要看用户能不能完成一个闭环。打开窗口时知道要做什么，输入时知道填哪里，点击时知道哪个按钮是主动作，完成后看到反馈，最后还能找到生成的文件。一个小窗口如果能把这五步照顾好，就已经从“控件摆放练习”变成了“可交付工具”的雏形。

不过，真正的科研工具不能只会“新建一张卡片”。它还应该能接住前面章节已经生产出来的材料。第2章做过 Stroop 数据包，第3章把它整理进 `workspace_ch03/organized/json/`，现在第4章要给这份数据做一个界面雏形：左侧看试次，右侧放按钮，顶部显示被试、正确率和反应时。

这一步像把图书馆后台的索引柜搬到前台：文件仍然在文件夹里，但用户看到的是能浏览、能点击、能导出的控制面板。脚本 `08_make_ch03_data_gui_panel.py` 不会弹出真正窗口，而是先生成一个静态 GUI 预览图和规格文件。先把界面想清楚，再让 Tkinter 真正动起来，学习会稳很多。

运行方式：

```bash
python code/ch04/08_make_ch03_data_gui_panel.py
```

运行后会生成：

```text
output/ch04_ch03_data_gui_panel.json
reports/ch04_ch03_data_gui_panel.md
output/ch04_ch03_data_gui_panel.png
```

<figure align="center">
  <img src="../assets/ch04/ch04_ch03_data_gui_panel.png" alt="ch3 数据 GUI 面板预览图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-25 ch3 数据 GUI 面板预览</strong>：ch2 的 Stroop 数据经过 ch3 文件整理后，在 ch4 被改造成一个 GUI 浏览面板雏形；界面负责让数据变得可看、可点、可继续导出。</figcaption>
</figure>

这张图的意义不是“现在已经做完了完整软件”，而是把项目下一步画出来。你可以把它看成界面设计草图：数据从哪里来、用户先看什么、按钮应该做什么、结果要写到哪里。GUI 学习到这里，终于从“按钮会响”走向“工具有工作流”。

建议项目结构：

```text
python_card_factory/
├── code/
│   └── ch04/
├── cards/
├── input/
├── output/
├── reports/
└── assets/
```

本章配套脚本：

- `code/ch04/01_hello_window.py`
- `code/ch04/02_card_form.py`
- `code/ch04/03_stroop_gui_preview.py`
- `code/ch04/04_gui_usability_check.py`
- `code/ch04/05_make_gui_feedback_lab.py`
- `code/ch04/06_make_interaction_receipt.py`
- `code/ch04/07_make_card_factory_delivery.py`
- `code/ch04/08_make_ch03_data_gui_panel.py`
- `code/ch04/09_make_gui_journey_storyboard.py`
- `code/ch04/10_make_gui_runtime_evidence.py`

完成标准：

1. 至少运行一个脚本。
2. 能解释脚本输入、处理、输出分别是什么。
3. 把生成结果保存到 `output/` 或 `reports/`。
4. 在 README 或学习记录中写下运行命令。
5. 能用可用性检查清单说明：这个窗口是否让用户少猜、少错、少迷路。
6. 能用反馈检查卡说明：按钮大小、控件间距、操作状态、错误恢复和按钮文案是否清楚。
7. 能用交互回执说明：当前窗口已经通过哪些检查，下一步还要改进什么。
8. 能打开 `cards/working_memory_load_card.md`，确认 GUI 项目确实留下了一张可继续编辑的学习卡片。
9. 能打开 `reports/ch04_ch03_data_gui_panel.md`，说明 ch2/ch3 的数据如何进入 ch4 的界面设计。
10. 能打开 `reports/ch04_gui_journey_storyboard.md`，说明一个 GUI 工具从输入到交付文件需要哪些反馈证据。
11. 能打开 `reports/ch04_gui_runtime_evidence.md`，说明 GUI 项目已经留下窗口截图、报告、回执和跨章节面板证据。

<figure align="center">
  <img src="../assets/ch04/ch04_gui_usability_check.png" alt="GUI可用性检查清单预览图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-26 Python 生成的 GUI 可用性检查清单</strong>：`04_gui_usability_check.py` 会生成一份检查清单，提醒你从用户视角审视窗口。</figcaption>
</figure>

这张图来自 `04_gui_usability_check.py`。它不是为了把 GUI 设计变复杂，而是为了提醒你：界面学习不能只停在“能弹出窗口”。一个小工具真正可用，至少要让用户知道它是做什么的、该在哪里输入、按钮会触发什么、保存后有没有反馈、出错后能不能恢复。

这就像心理学实验界面：被试不应该花精力猜规则，界面应该清楚地呈现任务、收集反应、给出必要反馈。GUI 设计越清楚，用户越能把注意力放在任务本身。

动手步骤：

1. **准备目录**：确认 `python_card_factory/` 下有 `code/`、`input/`、`output/`、`reports/`。
2. **运行最小脚本**：先运行本章第一个脚本，得到一个确定反馈。
3. **记录环境**：把 Python 版本、运行命令和输出截图或输出文本写进 `reports/`。
4. **连接真实材料**：把课程笔记、实验记录、图片、网页或 CSV 放进 `input/`。
5. **生成作品**：让脚本在 `output/` 或 `reports/` 中留下文件。
6. **检查界面体验**：运行 `04_gui_usability_check.py` 和 `05_make_gui_feedback_lab.py`，用清单检查窗口是否让用户少猜、少错、少迷路。
7. **生成交互回执**：运行 `06_make_interaction_receipt.py`，把通过项和待改进项记录下来。
8. **生成卡片交付物**：运行 `07_make_card_factory_delivery.py`，确认 `cards/` 中有一张真实 Markdown 卡片。
9. **生成交互旅程图**：运行 `09_make_gui_journey_storyboard.py`，检查窗口、输入、按钮、反馈和文件是否形成闭环。
10. **连接 ch3 数据**：运行 `08_make_ch03_data_gui_panel.py`，确认 Stroop 数据能变成界面面板预览。
11. **生成运行证据**：运行 `10_make_gui_runtime_evidence.py`，确认窗口截图、报告、回执和面板证据都已经 ready。
12. **写复盘**：说明这章让卡片工厂多了什么能力，哪些地方还容易出错。

---

## 4.10 练习任务

1. 修改一个输入参数，观察输出变化。
2. 把脚本生成的结果保存成文件。
3. 故意制造一个小错误，记录报错信息和修复方式。
4. 把本章项目和前面章节连接起来，例如读取 ch03 整理出的文件，或使用 ch02 的数据结构保存结果。
5. 运行 `04_gui_usability_check.py`，把清单中的 5 个问题逐条用于检查 `02_card_form.py`。
6. 运行 `05_make_gui_feedback_lab.py`，选一个按钮或输入框，写出它在 Target、Spacing、State、Error、Copy 中最需要改进的一项。
7. 运行 `06_make_interaction_receipt.py`，把 `FIX` 项改写成你自己的下一步优化计划。
8. 运行 `09_make_gui_journey_storyboard.py`，把其中一个阶段替换成你自己的 GUI 项目步骤，并说明它解决了哪个用户疑问。
9. 运行 `08_make_ch03_data_gui_panel.py`，把面板里的一个按钮文案改得更像真实科研工具，例如把“生成报告”改成“导出被试报告”。
10. 运行 `10_make_gui_runtime_evidence.py`，故意临时移走一个输出文件，观察证据图里的 `missing` 如何提醒你补交付物；检查后把文件恢复。

---

## 4.11 自测问题

1. 本章最重要的三个概念是什么？请用人话解释，不要只背术语。
2. 本章第一个脚本的输入、处理、输出分别是什么？
3. 如果脚本运行失败，你第一步会检查路径、环境、依赖还是语法？为什么？
4. 本章项目和“科研卡片工厂”有什么关系？
5. 你能不能把本章项目改成一个心理学或教学场景的小任务？
6. 为什么 GUI 里“有反馈”比“按钮很好看”更重要？

参考回答不唯一。判断自己是否真的理解，可以看你能不能把答案讲给一个完全没学过本章的人听。

---

## 4.12 学习复盘模板

可以在 `reports/ch04_review.md` 中写下：

```markdown
# 第4章复盘

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
- 教学分享：
- 科研资料整理：
```

复盘不是写作文，而是给未来的自己留路标。你现在记录清楚，后面做综合项目时就不用重新从记忆里翻箱倒柜。

---

## 4.13 与后续章节的连接

本章不是孤岛。它和整套教程的关系可以这样理解：

- 前面章节提供基础：环境、数据结构、文件管理。
- 本章提供一项新能力：科研卡片工厂控制面板，并能用交互旅程图检查用户是否真的走到交付物。
- 后面章节会把这项能力继续接到数据分析、图像处理、爬虫或办公自动化里。

所以不要只问“这一章考试考什么”。更好的问题是：它能帮我少做哪一类重复劳动？它能让我的学习材料、实验记录或报告更稳定吗？

---

## 4.14 本章总结

Tkinter 图形界面编程的关键不是“记住所有 API”，而是理解它解决的问题。你已经从概念、图像、代码和小项目四个角度接触了本章内容。下一次复习时，不要只问“我会不会背”，而要问：

- 我能不能讲出这个概念的比喻？
- 我能不能运行一个最小脚本？
- 我能不能把结果放进项目目录？
- 我能不能说清楚它在科研卡片工厂里增加了什么能力？

如果答案是肯定的，这一章就不是看过了，而是真的进入你的工具箱了。

更进一步，界面不是“能点”就结束了。一个真正适合教学和科研的小工具，还要让用户少猜、少错、少迷路。按钮大小、控件间距、保存后的状态提示、错误恢复方式、按钮文案，这些看似细小的东西，会决定别人愿不愿意继续用你的程序。

下一章进入面向对象。到那时你会发现，GUI 程序越来越适合用类来组织：窗口是对象，按钮是对象，卡片表单也可以是对象。Tkinter 是通往 OOP 的一座很好的桥。
