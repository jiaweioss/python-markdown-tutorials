# 第 4 章：Tkinter 图形界面编程

[TOC]

<figure align="center">
  <img src="../assets/ch04/ch04_cover.png" alt="第4章 Tkinter 图形界面编程封面" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-1 第4章封面</strong>：这一章把函数放到窗口里，让用户通过输入框、按钮和反馈完成一个真实任务。</figcaption>
</figure>

> 本章一句话：  
> **GUI 不是给程序贴一层漂亮皮肤，而是把输入、动作、反馈和文件结果摆到用户面前。窗口能弹出来只是开始，能让用户少猜、少错、能拿到结果，才算真正有用。**

第4章继续推进"科研卡片工厂"。前面几章已经打通了环境、数据类型和文件管理；现在我们要给这些能力做一个前台入口。用户不需要记住 `Path.write_text()`，也不需要知道脚本内部函数名，只要在窗口里填内容、点按钮、看到反馈，最后能在 `cards/` 或 `reports/` 里找到结果。

本章的读法和第1章保持一致：**先跑真实脚本，再看截图证据，最后把概念拆成能复查的动作**。不要一上来背 Tkinter API。先让一个窗口真的停在屏幕上，再逐步问：窗口是谁创建的，控件从哪里来，按钮点下去之后到底调用了哪个函数，保存结果在哪里。

---

## 本章导读：先让窗口亮起来，再证明它真的能做事

### 4.0 本章学习目标

学完本章，你应该能够做到：

1. 用自己的话解释 GUI、Tkinter、窗口、控件、布局、事件和回调函数的关系。
2. 运行 `01_hello_window.py`，看到最小 Tkinter 窗口，并能指出代码和界面元素的对应关系。
3. 运行 `02_card_form.py`，理解 `Entry`、`Text`、`Button` 和 `messagebox` 如何组成一个学习卡片表单。
4. 解释 `command=save_card` 与 `command=save_card()` 的区别，避免回调函数提前执行。
5. 理解键盘事件的绑定方式，能用 `bind()` 为窗口注册按键响应函数。
6. 使用可用性检查清单判断一个小窗口是否让用户少猜、少错、少迷路。
7. 完成本章小项目：**科研卡片工厂控制面板**，并留下卡片、报告、输出图和运行证据。

### 本章分区导航

| 分区 | 对应小节 | 你要抓住的主线 | 产出证据 |
| --- | --- | --- | --- |
| 第一部分：窗口通电与心智模型 | 4.1-4.3 | GUI 是把函数包装成用户能操作的动作 | 最小窗口截图、代码与界面对照图 |
| 第二部分：控件、布局与表单 | 4.4-4.6 | 控件负责收集输入，布局负责让它们有秩序 | 学习卡片表单窗口、保存函数 |
| 第三部分：事件、回调与反馈 | 4.7-4.11 | 点击、按键和消息框形成交互闭环 | 键盘事件演示、Stroop 预告、可用性检查、反馈检查卡 |
| 第四部分：项目交付与跨章连接 | 4.12-4.13 | GUI 项目最后要留下文件、报告和用户旅程证据 | 交互回执、ch3 数据面板 |
| 第五部分：排错、练习与验收 | 4.14-4.19 | 用固定路线排查 GUI 常见问题 | 常见坑地图、运行证据清单、复盘报告 |

<figure align="center">
  <img src="../assets/ch04/ch04_roadmap.png" alt="第4章学习路线图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-2 本章学习路线</strong>：先跑窗口，再拆控件，最后用截图、报告和输出文件证明 GUI 项目真的完成。</figcaption>
</figure>

---

## 第一部分：窗口展示与 Tkinter 心智模型

### 4.1 GUI 是把函数放到前台

命令行像后厨，GUI 像前台。后厨里有函数、路径、参数和文件写入；前台上有标签、输入框、按钮和状态提示。两边做的是同一件事，只是入口不同。

<figure align="center">
  <img src="../assets/ch04/ch04_story_scene.png" alt="从命令行后厨到 GUI 前台" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-3 从命令行后厨到 GUI 前台</strong>：GUI 不只是“好看一点”，而是把命令、函数和文件操作改造成用户能看见、能点击、能确认的任务入口。</figcaption>
</figure>

在命令行里，用户要知道脚本路径：

```bash
python code/ch04/02_card_form.py
```

还要理解输出会写到哪里：

```python
Path("cards").mkdir(exist_ok=True)
file.write_text(...)
```

而在 GUI 里，用户看到的是“主题”“要点”“保存卡片”。这些文字不是装饰，而是在帮用户理解任务。一个好窗口会替用户回答三件事：

1. 我现在要输入什么？
2. 我按这个按钮会发生什么？
3. 刚才那一下到底成功了吗？

这件事不是 Tkinter 才有的新问题。1960 年代，Douglas Engelbart 做鼠标、超文本和协作系统演示时，想解决的也不是“让屏幕更花”，而是让人可以直接操作屏幕上的对象，把想法、文本和命令组织成更顺手的工作方式。后来图形界面一路发展到 Alto、Macintosh 和 HyperCard，核心都没有离开这条线：**把计算机内部的动作，翻译成人能看懂、敢点击、能纠错的界面。**

<figure align="center">
  <img src="../assets/ch04/ch04_engelbart_mouse_story.png" alt="Douglas Engelbart 早期鼠标原型复制品" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-S1 Engelbart 鼠标原型</strong>：鼠标的意义不只是多了一个外设，而是让人可以把手上的动作映射到屏幕对象上。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch04/ch04_history_xerox_alto.png" alt="Xerox Alto 图形界面计算机" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-S2 Xerox Alto</strong>：窗口、图标、鼠标和桌面隐喻把计算机从命令文本带向可直接操作的工作空间。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch04/ch04_macintosh_gui_story.png" alt="Macintosh 128K 透明机身照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-S3 Macintosh 128K</strong>：GUI 真正改变学习门槛的地方，是让更多普通用户不用先背命令，也能开始完成任务。</figcaption>
</figure>

这一章的重点就是把这三件事做清楚。我们先从最小窗口开始，不做大而全的软件。

### 4.2 最小窗口：先跑通 `01_hello_window.py`

进入第4章目录后，先运行最小窗口脚本：

```bash
python code/ch04/01_hello_window.py
```

你应该看到一个小窗口，里面有一句提示和一个“收到”按钮。这个脚本的意义不是炫技，而是证明本机的 Tkinter 可以创建窗口、显示控件、响应按钮。

<figure align="center">
  <img src="../assets/ch04/ch04_minimal_demo.png" alt="Tkinter 最小窗口代码与界面对照图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-4 最小窗口代码与界面对照</strong>：`root.title()` 控制标题栏，`Label` 显示文字，`Button` 接收点击，`mainloop()` 让窗口持续响应。</figcaption>
</figure>

对应代码如下：

```python
import tkinter as tk

root = tk.Tk()
root.title("科研卡片工厂控制台")
root.geometry("360x180")

label = tk.Label(root, text="第一块 GUI 面板已经亮灯")
label.pack(pady=30)

button = tk.Button(root, text="收到", command=root.destroy)
button.pack()

root.mainloop()
```

这段代码只需要抓住四个点：

| 代码 | 人话解释 | 如果漏掉会怎样 |
| --- | --- | --- |
| `root = tk.Tk()` | 创建窗口 | 没有舞台，控件没地方放 |
| `tk.Label(...)` | 放一行说明文字 | 用户不知道窗口想说什么 |
| `tk.Button(..., command=...)` | 放一个可点击动作 | 用户无法触发函数 |
| `root.mainloop()` | 让窗口持续响应 | 窗口可能一闪而过 |

<figure align="center">
  <img src="../assets/ch04/ch04_tkinter_hello_window_screenshot.png" alt="Tkinter 最小窗口真实截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-5 Tkinter 最小窗口真实截图</strong>：这是本章第一个脚本弹出的真实窗口。先让它跑起来，后面再谈表单、事件和文件保存。</figcaption>
</figure>

如果窗口没有出现，先不要改代码。按这个顺序查：

1. 你是不是在 `python_tutorial_ch04` 目录里运行？
2. 脚本路径是不是 `code/ch04/01_hello_window.py`？
3. 终端有没有报错？
4. 有没有远程环境或无图形界面环境导致窗口无法显示？

这和第1章查环境是同一套思路：先找证据，再改问题。

### 4.3 Tkinter 的五个角色

Tkinter 的概念很多，但初学阶段先压成五个角色：

<figure align="center">
  <img src="../assets/ch04/ch04_core_metaphor.png" alt="Tkinter 最小心智模型" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-6 Tkinter 最小心智模型</strong>：窗口、控件、布局、回调和反馈组成一个小型 GUI 程序的基本骨架。</figcaption>
</figure>

| 角色 | 代码里常见写法 | 负责什么 |
| --- | --- | --- |
| 窗口 | `tk.Tk()` | 创建顶层窗口，像一张工作台 |
| 控件 | `Label`、`Entry`、`Text`、`Button` | 显示文字、收集输入、触发动作 |
| 布局 | `.pack()`、`.grid()`、`.place()` | 决定控件摆在哪里 |
| 回调 | `command=save_card` | 用户点击后调用哪个函数 |
| 反馈 | `messagebox.showinfo(...)` | 告诉用户操作结果 |

这五个角色不是背诵表，而是读代码时的检查顺序。以后看到一个 GUI 程序，你可以先问：

1. 窗口在哪里创建？
2. 控件有哪些？
3. 它们怎么摆放？
4. 用户动作绑定到哪个函数？
5. 函数执行后有没有反馈或文件结果？

---

## 第二部分：控件、布局与表单

### 4.4 控件不是零件堆

Tkinter 控件看起来像零件表，但它们要服务同一个任务。第4章不要求你把所有控件背下来，先掌握最常用的四个：

| 控件 | 适合放什么 | 本章用法 |
| --- | --- | --- |
| `Label` | 固定说明文字 | 告诉用户这里要填“主题”还是“要点” |
| `Entry` | 单行短输入 | 输入卡片主题、被试编号、文件名 |
| `Text` | 多行长输入 | 输入笔记、实验说明、学习要点 |
| `Button` | 用户主动触发的动作 | 保存卡片、开始试次、导出报告 |

控件本身不等于界面好用。`Entry` 如果旁边没有标签，用户不知道该填什么；`Button` 如果只写“确定”，用户不知道确定什么。GUI 设计的第一步不是追求华丽，而是把任务说清楚。

早期图形界面之所以能降低陌生感，很大一部分靠“可识别的符号”。Susan Kare 为 Macintosh 设计的图标之所以经典，不只是像素画漂亮，而是把“保存、文件夹、警告、垃圾桶”这些抽象动作变成用户一眼能猜到的形状。你写 Tkinter 时没有必要做整套图标，但要学会同一种态度：控件文字、按钮位置和反馈文案都要帮用户少猜。

<figure align="center">
  <img src="../assets/ch04/ch04_susan_kare_icon_story.png" alt="Susan Kare 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-S4 Susan Kare 与图标设计</strong>：好图标和好按钮文案一样，都是在替用户把“这是什么、能做什么”说清楚。</figcaption>
</figure>

### 4.5 学习卡片表单：`02_card_form.py`

现在运行本章第二个脚本：

```bash
python code/ch04/02_card_form.py
```

这个窗口比最小例子多了两类输入：一个单行主题输入框，一个多行要点输入区。点击“保存卡片”以后，程序会把内容写入 `cards/` 目录。

<figure align="center">
  <img src="../assets/ch04/ch04_project_dashboard.png" alt="脚本功能展示图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-7 脚本功能展示</strong>：表单负责收集输入，`save_card()` 负责把输入变成 Markdown 文件和可复查报告。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch04/ch04_tkinter_card_form_screenshot.png" alt="Tkinter 学习卡片表单真实截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-8 Tkinter 学习卡片表单真实截图</strong>：`Entry` 收集主题，`Text` 收集要点，按钮把内容写入本地 Markdown 卡片。</figcaption>
</figure>

关键函数是 `save_card()`：

```python
def save_card():
    topic = topic_entry.get().strip() or "未命名主题"
    idea = idea_text.get("1.0", "end").strip()
    out = Path("cards")
    out.mkdir(exist_ok=True)
    file = out / f"{topic.replace(' ', '_')}_card.md"
    file.write_text(f"# {topic}\n\n{idea}\n", encoding="utf-8")
    messagebox.showinfo("已保存", f"卡片已写入：{file}")
```

这段函数把前面章节的知识连起来了：

| 来自哪一章 | 在这里怎么用 |
| --- | --- |
| 第2章 | `strip()` 清理输入，f-string 组合文本 |
| 第3章 | `Path("cards")` 创建目录并写入文件 |
| 第4章 | `Entry.get()` 和 `Text.get()` 收集用户输入 |
| 第4章 | `messagebox.showinfo()` 告诉用户保存成功 |

这里有一个很重要的学习点：窗口里看起来是“点按钮”，代码里其实是“调用函数”。GUI 把函数包装成了用户可操作的动作。

### 4.6 布局：先用 `pack()`，再认识 `grid()`

本章脚本主要使用 `pack()`，因为它简单、适合纵向表单：

```python
tk.Label(root, text="主题").pack(anchor="w", padx=16, pady=(12, 4))
topic_entry.pack(fill="x", padx=16)
idea_text.pack(fill="both", expand=True, padx=16)
tk.Button(root, text="保存卡片", command=save_card).pack(pady=14)
```

先把 `pack()` 理解成“按顺序把控件放进窗口”。几个常用参数很有用：

| 参数 | 人话解释 | 常见用途 |
| --- | --- | --- |
| `padx` | 左右留白 | 输入框不要贴着窗口边缘 |
| `pady` | 上下留白 | 标签和输入框之间有呼吸 |
| `fill="x"` | 横向撑满 | 让 `Entry` 更好输入 |
| `fill="both"` | 横向纵向都撑开 | 让 `Text` 有足够空间 |
| `expand=True` | 窗口变大时一起扩展 | 多行输入区更自然 |

`grid()` 更像表格，适合复杂表单。你可以先不急着用它。第4章的目标是理解 GUI 的基本闭环，不是在布局语法里迷路。

---

## 第三部分：事件、回调与反馈

### 4.7 回调函数：按钮不是现在执行，而是等用户点击

Tkinter 里最容易犯的错误之一是：

```python
tk.Button(root, text="保存卡片", command=save_card())
```

这行看着很像正确写法，但它会在创建按钮时立刻执行 `save_card()`。按钮还没被用户点，函数已经跑完了。正确写法是：

```python
tk.Button(root, text="保存卡片", command=save_card)
```

少了括号，意思变了：不是现在调用函数，而是把函数交给按钮，等用户点击时再调用。

可以这样记：

| 写法 | 什么时候执行 |
| --- | --- |
| `command=save_card` | 用户点击按钮时执行 |
| `command=save_card()` | 创建按钮时立刻执行 |

#### 为什么这个区别特别重要？

你可以把函数理解成一张"操作说明书"。写 `command=save_card`，相当于把说明书放到按钮旁边，等用户点击按钮时，按钮再翻开说明书去执行里面的步骤。写 `command=save_card()`，则相当于在制作按钮的那一刻，就直接翻开说明书把步骤做完了——按钮还没被点击，操作就已经结束了。

用一个心理学的类比来帮助记忆：

> **有括号 = 直接执行**，就像实验者对被试说"现在按反应键"——被试立刻按键。
>
> **无括号 = 做好准备等信号**，就像实验者给被试下达任务指令："接下来看到红色按左键，看到绿色按右键"——被试记住了指令，但不会在听完指令的那一刻就立刻按键，而是等刺激真正出现时才执行。

回到代码里：

- `command=save_card` —— 这是"告诉按钮该做什么"，按钮记住了，等你点击它才做。
- `command=save_card()` —— 这是"现在就做"，按钮还没生成完，函数已经跑完了。

你还可以用 Python 交互式环境亲手验证这个区别。先定义一个简单函数：

```python
def say_hello():
    print("函数被执行了！")
```

然后在交互环境里分别输入以下两行，观察不同：

```python
say_hello   # 只输出 <function say_hello at 0x...>，没有执行
say_hello() # 输出 函数被执行了！
```

第一行只是"提到"函数的名字，函数本身没有被调用；第二行加上了括号，函数才真正执行。Tkinter 按钮的 `command` 参数正是利用了这一点：你给它函数名（不要括号），它先存着，等用户点击再来调用这个函数。

这不是语法小细节，而是 GUI 程序的核心思路。命令行脚本通常从上到下一次执行，所有动作立刻发生。GUI 程序则不同：大部分时间它只是"等着"，等用户点按钮、按键盘、关闭窗口，才去执行对应的函数。这种"等事件发生再响应"的模式，就叫**事件驱动**。`command=save_card` 就是把函数注册为一个事件的响应动作——函数现在不跑，但按钮被点击的那一刻它会跑。

### 4.8 键盘事件：让窗口响应按键

按钮点击不是 GUI 唯一的事件来源。用户按下键盘时，程序同样可以捕捉按键并做出响应。Tkinter 用 `bind()` 方法把按键和函数联系起来。

基本写法是：

```python
root.bind("<KeyPress>", lambda event: print(f"你按下了 {event.keysym}"))
```

这行代码的意思是：用户在窗口中按下任意键时，打印出按键的名称。尖括号里写事件类型，`<KeyPress>` 表示"按键按下"；后面的函数则定义了按下后做什么。

更常见的做法是指定特定的按键：

```python
root.bind("f", lambda event: print("你按了 f 键"))
root.bind("j", lambda event: print("你按了 j 键"))
root.bind("<Return>", lambda event: print("你按了回车键"))
root.bind("<Escape>", lambda event: print("你按了退出键"))
```

这里有几个要点：

| 写法 | 匹配的按键 |
| --- | --- |
| `"f"` | 字母 f 键 |
| `"j"` | 字母 j 键 |
| `"<Return>"` | 回车（Enter）键 |
| `"<Escape>"` | 退出键（Esc） |
| `"<Shift_L>"` | 左边的 Shift 键 |
| `"<Control-a>"` | Ctrl + A 组合键 |
| `"<Up>"` | 上方向键 |
| `"<space>"` | 空格键 |

`bind()` 的第二个参数是一个函数，这个函数必须接受一个 `event` 参数。`event` 对象携带了按键的详细信息，比如 `event.keysym`（按键名称）、`event.char`（字符）、`event.keycode`（按键码）等。

键盘事件的意义在于：GUI 不只能让用户"点"，还能让用户"按"。用户不需要离开键盘去操作鼠标，就能触发程序中的动作。这在需要快速反应的场景下尤其有用——用户的手始终在键盘上，程序随时等待按键信号。

理解键盘事件后，你也能用一个简单的测试脚本来感受一下：

```python
import tkinter as tk

def on_key(event):
    label.config(text=f"你按下了: {event.keysym}")

root = tk.Tk()
root.title("键盘事件演示")
root.geometry("300x200")

label = tk.Label(root, text="按任意键试试", font=("Arial", 16))
label.pack(expand=True)

root.bind("<KeyPress>", on_key)

root.mainloop()
```

这个窗口运行后，你在键盘上按任意键，标签上的文字就会更新成你按的键名。

这种"等事件发生再响应"的机制，再一次印证了 4.7 节的核心思想：GUI 程序不是顺序执行的，而是先注册好各种事件的响应函数，然后进入等待状态——用户按了什么键，程序就调用对应的函数去处理。这就是**事件驱动**在键盘输入上的体现。

### 4.9 反馈：用户需要知道刚才发生了什么

很多新手窗口能运行，但用户点完按钮以后什么都不知道。文件到底保存了吗？保存到哪里了？标题为空会怎样？失败了能不能重新输入？

<figure align="center">
  <img src="../assets/ch04/ch04_gui_usability_check.png" alt="GUI 可用性检查清单" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-9 GUI 可用性检查清单</strong>：一个小窗口交给别人之前，至少要检查用途、标签、主按钮、保存反馈和错误恢复。</figcaption>
</figure>

这份清单并不是让 GUI 设计变复杂，而是把“友好一点”拆成能检查的问题：

1. 用户一眼能看出窗口是做什么的吗？
2. 标签离对应输入框够近吗？
3. 主按钮是否清楚、容易点？
4. 保存以后有没有确认反馈？
5. 用户填错或漏填时能不能恢复？

### 4.10 按钮大小、间距、状态和文案

<figure align="center">
  <img src="../assets/ch04/ch04_target_feedback_lab.png" alt="GUI 目标大小与反馈实验" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-10 GUI 目标大小与反馈实验</strong>：按钮太小、太挤、没有状态提示，用户就会紧张；按钮清楚、间距足够、保存后有反馈，用户才敢继续操作。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch04/ch04_gui_feedback_scorecard.png" alt="GUI 反馈检查卡" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-11 GUI 反馈检查卡</strong>：用 Target、Spacing、State、Error、Copy 五个检查点，判断窗口是否真的适合交给别人使用。</figcaption>
</figure>

界面设计里有一个朴素原则：用户迟疑的地方，就是界面应该多给线索的地方。

<figure align="center">
  <img src="../assets/ch04/ch04_norman_door_affordance.png" alt="推板和拉手的界面线索示意图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-12 界面线索</strong>：推板、拉手和按钮文案都在回答同一个问题：用户看一眼能不能知道下一步怎么做。</figcaption>
</figure>

Don Norman 写“诺曼门”的故事时，批评的不是某一扇门，而是设计把责任推给了用户：明明门没有给出清楚线索，却让用户以为是自己笨。GUI 也一样。一个学生填错路径、点错按钮、保存后找不到文件，未必是他不认真，也可能是界面没有给出足够清楚的提示。

<figure align="center">
  <img src="../assets/ch04/ch04_don_norman_story.png" alt="Don Norman 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-S5 Don Norman 与可用性</strong>：可用性不是锦上添花，而是在替用户减少猜测、减少自责、减少犯错成本。</figcaption>
</figure>

换到 Tkinter 里，线索可以很具体：

| 模糊写法 | 更清楚的写法 |
| --- | --- |
| 按钮写“确定” | 按钮写“保存卡片” |
| 标签写“内容” | 标签写“学习要点” |
| 保存后无提示 | 弹出“已保存到 cards/xxx.md” |
| 空标题悄悄替换 | 提示"标题为空，已使用未命名主题" |

---

### 4.11 例子 Stroop GUI：把事件、回调和反馈串成一个完整实验

前几节分别讲了回调、键盘事件和反馈。现在用一个真实脚本把它们串起来：`03_stroop_gui_preview.py`。

这个脚本模拟了一个极简的 Stroop 实验界面：被试点击"开始"按钮，屏幕上出现一个颜色词（例如用蓝色墨水写的"RED"），然后通过按键盘上的 F 或 J 键来判断墨水颜色。程序会记录按键是否正确以及反应时间。

运行这个脚本：

```bash
python code/ch04/03_stroop_gui_preview.py
```

你会看到一个窗口，包含一段提示文字、一个刺激标签、一个结果显示标签和一个"开始"按钮。这个窗口虽然小，但已经具备了实验程序最关键的三块骨架。

先看完整代码，再逐段拆解：

```python
import time
import tkinter as tk

TRIAL = {"word": "RED", "ink": "blue", "correct": "j"}

def start_trial():
    global start
    prompt.config(text="判断墨水颜色：红色按 F，蓝色按 J")
    stimulus.config(text=TRIAL["word"], fg=TRIAL["ink"])
    start = time.perf_counter()

def respond(key: str):
    rt = round((time.perf_counter() - start) * 1000, 2)
    ok = key == TRIAL["correct"]
    result.config(text=f"反应：{key}  正确：{ok}  反应时：{rt} ms")

root = tk.Tk()
root.title("Stroop GUI 预告")
root.geometry("520x300")
start = time.perf_counter()

prompt = tk.Label(root, text="点击开始后看刺激", font=("Microsoft YaHei", 13))
prompt.pack(pady=16)
stimulus = tk.Label(root, text="", font=("Arial", 36, "bold"))
stimulus.pack(pady=18)
result = tk.Label(root, text="")
result.pack(pady=12)
tk.Button(root, text="开始", command=start_trial).pack()
root.bind("f", lambda event: respond("f"))
root.bind("j", lambda event: respond("j"))
root.mainloop()
```

#### 回调：按钮把"开始实验"交给用户决定

脚本中的按钮是这样写的：

```python
tk.Button(root, text="开始", command=start_trial).pack()
```

`command=start_trial` 没有括号。按钮创建时 `start_trial()` 不会执行，只有用户点击"开始"按钮后，函数才会被调用。这正是 4.7 节反复强调的"有括号立刻执行，无括号等用户点"。

点击后，`start_trial()` 做了三件事：

1. 把提示文字改成具体操作指令："判断墨水颜色：红色按 F，蓝色按 J"
2. 把刺激标签的文字设为 `"RED"`，颜色设为 `"blue"`——Stroop 冲突的核心就在这里：词义（RED）和墨水颜色（blue）不一致
3. 用 `time.perf_counter()` 记录当前时间，作为反应时的起点

#### 事件：键盘按键触发响应

脚本用两行 `bind()` 注册了键盘事件：

```python
root.bind("f", lambda event: respond("f"))
root.bind("j", lambda event: respond("j"))
```

用户在键盘上按下 F 或 J 时，`respond()` 函数会被自动调用。这和 4.8 节的键盘事件示例写法完全一致——按键时不需要用鼠标点击按钮，程序自动捕捉按键并做出响应。

这种设计在实验程序中很常见：被试的眼睛盯着屏幕上的刺激，手放在键盘上，不需要在鼠标和键盘之间来回切换。按键延迟更短，反应时记录也更准确。

#### 反馈：结果标签实时更新

`respond()` 函数被调用后，会计算反应时并更新界面：

```python
def respond(key: str):
    rt = round((time.perf_counter() - start) * 1000, 2)
    ok = key == TRIAL["correct"]
    result.config(text=f"反应：{key}  正确：{ok}  反应时：{rt} ms")
```

`result.config(text=...)` 把结果显示在窗口底部的标签上。用户按完键后，能立即看到自己的按键是否正确，还能看到精确到毫秒的反应时——这就是 4.9 节讨论的"用户需要知道刚才发生了什么"。

#### 三块骨架如何配合

| 概念 | 在 Stroop 脚本中的体现 | 背后原理 |
| --- | --- | --- |
| **事件** | 用户按下 F 或 J 键触发 | `root.bind("f", ...)` 注册键盘监听 |
| **回调** | 用户点击"开始"按钮后调用 `start_trial()` | `command=start_trial` 把函数交给按钮 |
| **反馈** | 按键后标签更新为"正确：True/False 反应时：xxx ms" | `result.config(text=...)` 实时刷新界面 |

这三个概念不是独立的知识点。把它们放到一起，才能构成真正的交互闭环：

> **用户点击按钮 → 程序显示刺激 → 用户按键 → 程序记录并反馈结果**

这个闭环在 Stroop 任务中是"试次（trial）"的基本结构，在更广泛的 GUI 程序中则是"输入—处理—输出"的用户体验循环。

#### Stroop 任务与 GUI 交互

Stroop 效应是心理学最经典的实验范式之一：当词义和墨水颜色不一致时（例如蓝色墨水写的"RED"），被试的反应时显著变长，错误率也更高。这个脚本只模拟了单个试次，但它展示了 GUI 如何为实验程序服务：

- 刺激呈现在窗口中央，字体大而醒目
- 被试通过键盘按键快速反应，无需鼠标
- 反应时被精确记录到毫秒
- 正确性可以即时判断

如果你继续往这个方向扩展，可以加入更多试次、记录完整数据到文件、计算平均反应时和正确率——这就是把第2章（数据类型）、第3章（文件保存）和第4章（GUI 交互）连起来的完整路径。

---

## 第四部分：项目交付与跨章连接

### 4.12 交互回执：证明窗口不是只会弹出来

窗口能弹出来只是第一步。一个 GUI 程序真正要回答的问题是：用户操作它之后，到底有没有留下可复查的证据？

**交互回执**就是把这个问题变成一张可检查的清单。它把窗口的用途、输入字段有哪些、主按钮做什么、点击后有什么反馈、以及还有哪些待改进项，集中到一个文件中。这样你不需要重新打开窗口或翻代码，只看回执就能判断这个窗口是否完成了它的任务。

<figure align="center">
  <img src="../assets/ch04/ch04_interaction_receipt.png" alt="GUI 交互回执" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-13 GUI 交互回执</strong>：交互回执把窗口用途、输入字段、主按钮、反馈和待改进项集中到一张可复查证据里。</figcaption>
</figure>

交互回执的意义在于：它把"这个窗口好不好用"从一个主观感受，变成一组可以逐条核对的事实。你在后续练习中每改一个窗口，都可以生成一张新回执，对比改进前后的差异。
### 4.13 接住 ch02 和 ch03 的数据：用一个 Tkinter 窗口浏览 Stroop 数据

第4章不是孤岛。第2章做过 Stroop 数据结构，第3章整理过文件和 JSON；第4章可以把这些数据直接装进一个可交互的 Tkinter 窗口。

运行：

```bash
python code/ch04/04_make_ch03_data_gui_panel.py
```

你会看到一个名为"Stroop 数据浏览面板"的窗口，包含三个区域：

**指标卡片区**：顶部横向排列五个指标卡片——参与被试、试次总数、正确率、平均反应时和冲突试次数。这些数据来自 ch2 的 Stroop 实验结果，经过 ch3 整理后，在这里以可视化方式呈现。

**试次表格区**：中间是一个表格，逐行列出每个试次的 ID、词、墨水色、按键、反应时、是否正确、是否一致。你可以直观地看到每一试次的原始记录，对比一致试次和冲突试次在反应时上的差异。

**动作按钮区**：底部预留了四个按钮（加载数据、查看试次、导出卡片、生成报告），当前为占位状态。这些按钮可以作为后续扩展的入口，把"只看数据"推进到"操作数据"。

这个窗口把前几章的工作串成了一条完整的动手链路：ch2 生成的数据结构，ch3 保存为 JSON 文件，ch4 读取并呈现为 GUI 表格。这条链路本身就说明了"学完 Python 基础能做什么"。

提示：如果没有数据被展示出来，可能是什么原因？

---

## 第五部分：排错、练习与验收

### 4.14 常见坑：先按线索排查

<figure align="center">
  <img src="../assets/ch04/ch04_pitfall_map.png" alt="第4章 GUI 常见坑排查图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图4-14 第4章常见坑排查</strong>：GUI 报错通常可以从窗口生命周期、回调函数、布局、路径和反馈五个方向排查。</figcaption>
</figure>

| 问题 | 典型现象 | 优先检查 |
| --- | --- | --- |
| 忘记 `mainloop()` | 窗口一闪而过或根本看不到 | 最后一行有没有 `root.mainloop()` |
| `command=func()` | 还没点按钮，函数已经执行 | `command` 后面是否写了括号 |
| 控件没有布局 | 创建了控件但窗口里没有显示 | 有没有调用 `.pack()`、`.grid()` 或 `.place()` |
| 工作目录不对 | 保存文件找不到或写到奇怪位置 | 打印 `Path.cwd()` |
| 没有反馈 | 用户不知道保存是否成功 | 用 `messagebox` 或状态栏提示 |
| 逻辑混在一起 | 代码越来越难读 | 把保存、检查、绘图拆成函数 |

遇到 GUI 问题时，先不要大改。先把问题缩到最小脚本里：一个窗口、一个标签、一个按钮、一个回调。最小版本能跑，再把功能加回来。

### 4.15 上机路线与运行证据

第一次学习本章时，建议按这个顺序运行：

```bash
python code/ch04/01_hello_window.py
python code/ch04/02_card_form.py
python code/ch04/03_stroop_gui_preview.py
python code/ch04/04_make_ch03_data_gui_panel.py
```

运行证据可以按下面这张表整理：

| 运行证据 | 要看到什么 |
| --- | --- |
| 最小窗口 | `01_hello_window.py` 能弹出窗口 |
| 卡片表单 | `02_card_form.py` 能保存一张 Markdown 卡片 |
| Stroop GUI展示 | `03_stroop_gui_preview.py` 能正常工作 |
| 数据展示面板 | `04_make_ch03_data_gui_panel.py` 能展示信息 |

### 4.16 练习任务

1. 把 `01_hello_window.py` 的窗口标题改成你的项目名，运行并截图。
2. 在 `02_card_form.py` 中增加一个“标签”输入框，例如“实验记录”“课程笔记”“论文摘录”。
3. 修改 `save_card()`，让保存文件名包含日期。
4. 故意把 `command=save_card` 写成 `command=save_card()`，观察发生了什么，再改回来。
5. 参考 4.8 节的键盘事件示例，自己写一个窗口，按下不同按键时在标签上显示不同的提示文字。
6. 修改 `03_stroop_gui_preview.py`，使得字体颜色改为红色，文字内容改为`BLUE`。
7. 修改 `04_make_ch03_data_gui_panel.py`，把文案改得更像真实科研工具。

### 4.17 自测问题

1. `tk.Tk()`、控件、布局、回调和 `mainloop()` 分别负责什么？
2. 为什么 `command=save_card` 和 `command=save_card()` 结果不同？
3. `Entry.get()` 和 `Text.get("1.0", "end")` 分别适合拿什么输入？
4. 保存卡片以后，为什么要给用户反馈？
5. 一个 GUI 小项目的提交证据应该包含哪些文件？
6. 如果窗口没有出现，你会按什么顺序排查？

判断自己是否真的学会，可以看你能不能把 `02_card_form.py` 讲给同学听：窗口里有什么，用户怎么操作，点击后哪个函数执行，最后文件保存到哪里。

### 4.18 学习复盘模板

可以在 `reports/ch04_review.md` 中写下：

```markdown
# 第4章复盘

## 我新增的能力
- 

## 我跑通的窗口
- 

## 我生成的文件证据
- 

## 我遇到的 GUI 问题
- 报错或现象：
- 原因：
- 修复方式：

## 我准备继续改进
- 输入提示：
- 按钮文案：
- 保存反馈：
- 错误恢复：
```

复盘不是写作文，而是给下一次调试留路标。你现在把窗口、函数、路径和输出写清楚，后面做综合项目时就不用重新猜。

### 4.19 本章总结

Tkinter 入门的关键不是把所有参数背下来，而是理解 GUI 程序的基本闭环：

1. `Tk()` 创建窗口。
2. 控件收集输入或显示信息。
3. 布局让控件有秩序。
4. 事件触发回调函数。
5. 回调函数处理数据、写入文件或更新界面。
6. 用户得到反馈，并能找到结果。

这一章让“科研卡片工厂”多了一块前台面板。前几章的能力还在后厨：字符串、列表、路径、文件写入；第4章把它们搬到窗口里，让用户通过输入和按钮完成任务。

下一章会进入面向对象。到那时你会发现，GUI 程序很适合用类来组织：窗口是对象，按钮是对象，卡片表单也可以成为一个对象。第4章先把“能点击、能保存、能反馈”的闭环跑通，第5章再学习怎样把这些部件组织得更稳。
