# 第 5 章：面向对象程序设计

[TOC]

<figure align="center">
  <img src="../assets/ch05/ch05_cover.png" alt="第5章 面向对象程序设计封面" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-1 第5章封面</strong>：本章把散落变量收进对象，让职责、协作和交付证据都能看见。</figcaption>
</figure>

> 本章一句话：  
> **面向对象不是把代码写得更“高级”，而是给数据和动作划清边界。一个好对象知道自己保存什么、能做什么、不该管什么，也知道需要把请求交给哪个对象。**

第4章我们用 Tkinter 做了一个能点击、能反馈、能生成文件的 GUI 小项目。窗口代码一旦继续变长，就会出现一个新问题：输入框、按钮、保存函数、报告生成、实验试次、文件路径全挤在一起，修改一个功能很容易碰坏另一个功能。

第5章要解决的正是这个问题。我们不急着学一堆术语，也不把“类”“继承”“多态”当作背诵任务。先从一个很小的 `LearningCard` 开始：一张学习卡片应该保存主题、问题、答案和标签，也应该能生成自己的预览。这个边界跑通以后，再引入 `CardDeck`和`Trial`，把对象之间的协作画出来、生成报告。

这一章的读法和 ch01/ch04 保持一致：**先跑脚本，再看证据图，最后把概念拆成能复查的动作**。你不需要一开始就把 OOP 学成“设计模式大全”。先让小对象真的工作起来，再逐步把职责边界收紧。

---

## 本章导读：先分职责，再写 `class`

### 5.0 本章学习目标

学完本章，你应该能够做到：

1. 用自己的话解释类、对象、属性、方法、`self`、封装、组合和对象协作。
2. 运行 `01_learning_card_class.py`，创建一个 `LearningCard` 对象，并说明它的属性和方法分别负责什么。
3. 运行 `02_card_deck.py`，理解 `CardDeck` 为什么应该“拥有多张卡片”，而不是继承一张卡片。
4. 运行 `03_trial_object.py`，把心理学实验中的一次试次建模成对象。
5. 使用类职责卡片判断一个类该管什么、不该管什么。
6. 读懂对象协作消息图，说明 `LearningCard`、`CardDeck`、`Trial` 和 `ReportBuilder` 如何互相请求。
7. 学习设计卡片和质量回执。
8. 把 ch04 的 GUI 面板规格拆成 ch05 的对象模型，为后续数据分析章节做准备。

### 本章分区导航

| 分区 | 对应小节 | 你要抓住的主线 | 产出证据 |
| --- | --- | --- | --- |
| 第一部分：从变量到对象 | 5.1-5.3 | 代码变长后，职责边界比语法更重要 | 最小类、真实运行截图 |
| 第二部分：类、属性、方法与组合 | 5.4-5.7 | 对象保存状态，方法处理自己的状态，组合表达拥有关系 | 心智模型、Trial 对象、对象小剧场 |
| 第三部分：对象协作与职责检查 | 5.8, 5.10-5.12 | 类不是孤岛，要通过清楚消息合作 | 职责卡片、协作图、质量回执 |
| 第四部分：面向对象程序设计示例 | 5.13-5.15 | 用一个完整例子串联 OOP 思想 | Stroop GUI 面板的 OOP 版本 |
| 第五部分：排错、练习与验收 | 5.16-5.20 | 用固定路线排查 OOP 常见问题并留下证据 | 常见坑地图、运行证据、复盘模板 |

<figure align="center">
  <img src="../assets/ch05/ch05_roadmap.png" alt="第5章学习路线图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-2 本章学习路线</strong>：先写最小类，再拆职责、看协作，最后交付可复查的对象项目。</figcaption>
</figure>

---

## 第一部分：从散装变量到对象模型

### 5.1 代码变长后，真正难的是职责边界

刚开始写 Python 时，把数据放在几个变量里很自然：

```python
topic = "OOP"
question = "类是什么？"
answer = "类像图纸，描述对象应该有什么。"
tags = ["类", "对象"]
```

如果只有一张卡片，这样写没问题。问题出现在需求变多以后：你想给卡片生成预览、保存 Markdown、按标签筛选、放进卡片盒、导出报告。函数越写越多，参数越传越长，最后你很难判断“主题、问题、答案、标签”到底属于谁。

<figure align="center">
  <img src="../assets/ch05/ch05_story_scene.png" alt="从散装变量到有职责的对象" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-3 从散装变量到有职责的对象</strong>：OOP 的第一步不是换一种写法，而是把数据和动作放回合适的边界里。</figcaption>
</figure>

在这里可以看出面向对象设计的价值：如果一张卡片本来就拥有主题、问题、答案和标签，那它也可以拥有 `preview()` 这样的方法。对象把“状态”和“动作”放在一起，读代码的人更容易看懂任务边界。

这一章我们会反复问三个问题：

1. 这个类保存什么数据？
2. 这个类提供什么动作？
3. 这个类不应该管什么？

能回答这三个问题，比一开始背“封装、继承、多态”更重要。

你可能也会好奇：对象思想到底从哪来的？

面向对象并不是从“高级语法”里凭空长出来的。Simula 这个名字就带着它的源头：simulation，仿真。早期研究者想描述船、港口、队列、事件这类不断互动的系统，仅靠一堆变量和过程很快就不够用了。把“东西”建成对象，让它们保存状态、响应动作、互相发送消息，是为了让复杂世界在程序里有更清楚的边界。

<figure align="center">
  <img src="../assets/ch05/ch05_simula_origin_story.png" alt="Simula 语言标识" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S1 Simula 与对象思想源头</strong>：对象思想最早和仿真、事件、复杂系统联系在一起，不是为了把代码写得神秘。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch05/ch05_kristen_nygaard_story.png" alt="Kristen Nygaard 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S2 Kristen Nygaard</strong>：OOP 的人文背景里有一个朴素问题：当世界由许多互相影响的实体组成，程序怎样表达它们的状态和关系？</figcaption>
</figure>

### 5.2 最小类：先跑通 `01_learning_card_class.py`

进入第5章目录后，先运行第一个脚本：

```bash
python code/ch05/01_learning_card_class.py
```

脚本核心代码如下：

```python
from dataclasses import dataclass


@dataclass
class LearningCard:
    topic: str
    question: str
    answer: str
    tags: list[str]

    def preview(self) -> str:
        return f"[{self.topic}] {self.question} -> {self.answer[:20]}..."


card = LearningCard("Python", "变量是什么？", "变量像贴在数据上的标签。", ["基础", "比喻"])
print(card.preview())
```

<figure align="center">
  <img src="../assets/ch05/ch05_minimal_demo.png" alt="LearningCard 最小类代码与对象对照图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-4 最小类代码与对象对照</strong>：`class` 定义图纸，属性保存状态，方法提供动作，`self` 指向当前这个对象。</figcaption>
</figure>

这里先抓住四个点：

| 代码 | 人话解释 | 如果漏掉会怎样 |
| --- | --- | --- |
| `class LearningCard:` | 定义一种对象的图纸 | 代码里没有“卡片”这个概念 |
| `topic: str` 等字段 | 规定对象保存哪些状态 | 数据仍然散落在外部变量里 |
| `def preview(self)` | 给对象一个动作 | 预览逻辑只能写在外部函数里 |
| `self.topic` | 访问当前对象自己的主题 | 方法不知道该拿哪张卡片的数据 |

<figure align="center">
  <img src="../assets/ch05/ch05_powershell_oop_run.png" alt="PowerShell 中运行第5章 OOP 脚本" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-5 第5章真实运行截图</strong>：先让最小对象脚本跑起来，再逐步增加卡片盒、试次对象和交付证据。</figcaption>
</figure>

第一次运行时，不要急着修改。先确认终端输出里能看到卡片预览。这个输出说明三件事：类定义成功，对象创建成功，方法调用成功。

### 5.3 `dataclass` 不是魔法，只是在少写样板代码

本章大量使用 `@dataclass`。对于面向对象设计，这种写法是非必要的，这是Python提供的简便写法。没有 `dataclass` 时，你通常要手写：

```python
class LearningCard:
    def __init__(self, topic, question, answer, tags):
        self.topic = topic
        self.question = question
        self.answer = answer
        self.tags = tags
```

有了 `@dataclass`，你可以把精力放在“对象应该保存什么”上：

```python
@dataclass
class LearningCard:
    topic: str
    question: str
    answer: str
    tags: list[str]
```

它会自动帮你生成初始化方法，也会让打印对象时更清楚。初学阶段可以把 `dataclass` 理解成：**适合用来定义主要保存数据、再带一点方法的小对象**。

---

## 第二部分：类、属性、方法与组合

### 5.4 类、对象、属性、方法、`self`

很多 OOP 术语听起来抽象，其实都可以落回一个小例子：

<figure align="center">
  <img src="../assets/ch05/ch05_core_metaphor.png" alt="OOP 最小心智模型" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-6 OOP 最小心智模型</strong>：类定义共同结构，对象保存具体状态，属性是对象的数据，方法是对象的动作，`self` 指向当前对象。</figcaption>
</figure>

| 术语 | 在本章中的例子 | 你可以这样理解 |
| --- | --- | --- |
| 类 | `LearningCard` | 一种对象的规则说明 |
| 对象 | `card = LearningCard(...)` | 按规则创建出来的具体成员 |
| 属性 | `card.topic` | 对象身上的数据 |
| 方法 | `card.preview()` | 对象能执行的动作 |
| `self` | `self.topic` | 方法里指向“当前这个对象” |

关键是不要把类和对象混在一起。`LearningCard` 是图纸，`card` 才是一张具体卡片。图纸不会有某个具体主题；对象才会有 `"Python"`、`"变量是什么？"` 这些具体值。

工程图纸把桥梁的共同结构固定下来，真正的桥才承受具体重量、风、车辆和时间。类也是这样：它定义对象应该有什么属性、能做什么动作；对象才带着具体数据参与程序运行。

<figure align="center">
  <img src="../assets/ch05/ch05_blueprint_class_story.png" alt="桥梁蓝图照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S3 蓝图与类</strong>：类像图纸，对象像按图纸建出来的具体作品；别把规则本身和具体实例混在一起。</figcaption>
</figure>

Alan Kay 后来谈对象时，经常强调“消息”比“类层级”更重要。这个提醒对初学者很有价值：不要把 OOP 学成继承树比赛。对象真正有生命力的地方，是它们能各自负责一小块事情，并通过清楚的消息合作。

<figure align="center">
  <img src="../assets/ch05/ch05_alan_kay_oop_story.png" alt="Alan Kay 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S4 Alan Kay 与对象消息</strong>：对象不是孤立的数据盒子，而是可以通过消息协作的小角色。</figcaption>
</figure>

### 5.5 方法应该靠近它使用的数据

如果一个函数总是需要同一组参数，它很可能适合变成对象的方法。比如下面这个外部函数：

```python
def preview_card(topic: str, question: str, answer: str) -> str:
    return f"[{topic}] {question} -> {answer[:20]}..."
```

它每次都要拿 `topic`、`question`、`answer`。如果这些数据本来就属于一张卡片，就可以写成：

```python
def preview(self) -> str:
    return f"[{self.topic}] {self.question} -> {self.answer[:20]}..."
```

区别不是少写了几个参数，而是职责变清楚了：预览一张卡片，是卡片自己的能力。

判断一个函数是否应该变成方法，可以问：

| 问题 | 如果答案是“是” |
| --- | --- |
| 这个函数总是处理某个对象的数据吗？ | 可以考虑放进这个类 |
| 这个函数会改变某个对象的状态吗？ | 通常应该由这个对象的方法完成 |
| 这个函数需要访问很多无关对象吗？ | 可能说明边界还没拆清楚 |

### 5.6 `CardDeck`：组合比继承更自然

运行第二个脚本：

```bash
python code/ch05/02_card_deck.py
```

脚本里定义了一个卡片盒：

```python
@dataclass
class CardDeck:
    name: str
    cards: list[str] = field(default_factory=list)

    def add(self, card: str) -> None:
        self.cards.append(card)

    def summary(self) -> str:
        return f"{self.name}: {len(self.cards)} 张卡片"
```

`CardDeck` 和 `LearningCard` 的关系不是“卡片盒也是一张卡片”，而是“卡片盒拥有多张卡片”。这叫组合。组合通常比继承更符合初学阶段的直觉。

| 关系 | 人话判断 | 本章例子 |
| --- | --- | --- |
| 组合 has-a | A 拥有 B | `CardDeck` 拥有多张 `LearningCard` |
| 继承 is-a | A 是一种 B | “错题卡”也许是一种 `LearningCard` |

如果你说不清 `A is a B`，先别写继承。很多初学者一上来就想设计复杂继承树，结果类之间关系越写越乱。本章优先使用组合：对象之间互相拥有、互相请求，边界更容易看清。

组合可以用乐高来理解：你不是把轮子“继承成”车，也不是把车“继承成”房子；你是把合适的部件组合起来，让整体承担新的功能。程序里的 `CardDeck` 也是这样，它不需要成为一张卡片，它只需要拥有多张卡片，并负责集合层面的动作。

<figure align="center">
  <img src="../assets/ch05/ch05_lego_composition_story.png" alt="乐高积木照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S5 组合优先于继承</strong>：组合让对象像部件一样协作，关系更直观，也更容易替换和扩展。</figcaption>
</figure>

### 5.7 `Trial`：心理学试次为什么适合对象

运行第三个脚本：

```bash
python code/ch05/03_trial_object.py
```

心理学实验里，一次试次通常包含被试、刺激、反应和反应时：

```python
@dataclass
class Trial:
    participant: str
    stimulus: str
    response: str
    reaction_time_ms: float

    def is_fast(self) -> bool:
        return self.reaction_time_ms < 500
```

<figure align="center">
  <img src="../assets/ch05/ch05_psychology_link.png" alt="心理学试次对象示意图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-7 心理学试次对象</strong>：`Trial` 把一次刺激、一次反应和一次反应时收在同一个对象边界里。</figcaption>
</figure>

这样写的好处很直接：以后你要判断快速反应、导出 CSV、计算正确性，都可以围绕 `Trial` 这个对象展开，而不是让一堆列表互相对齐。

| 散装写法 | 对象写法 |
| --- | --- |
| `participants[i]`、`stimuli[i]`、`responses[i]` | `trial.participant`、`trial.stimulus`、`trial.response` |
| 需要小心多个列表长度一致 | 一次试次的数据天然在一起 |
| 判断快慢要传入 `reaction_time_ms` | `trial.is_fast()` 自己判断 |

这不是说所有实验数据都要立刻改成对象。正式统计分析时，表格和 DataFrame 很重要。第5章的重点是：当你在写实验流程、界面逻辑或交付对象时，用对象保存“同一件事”的状态，会让代码更稳。

把“同一件事”收进一个边界，这个思路在心理学里也能找到呼应。人理解世界时，会把分散信息组织成可重复使用的结构，Piaget 把这种结构叫作“图式”（schema）。把一次试次收成一个对象，和这个道理有一点相通。Piaget 研究儿童认知发展时关心的正是这种结构如何形成、调整和迁移。写代码当然不是照搬心理学理论，但这个类比能提醒我们：好对象不是一堆字段，而是一个有边界、有意义、能参与后续动作的认知单元。

<figure align="center">
  <img src="../assets/ch05/ch05_piaget_schema_story.png" alt="Jean Piaget 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S6 Piaget 与认知图式</strong>：对象可以帮助我们把分散信息组织成稳定结构，方便理解、复用和继续扩展。</figcaption>
</figure>

---

## 第三部分：对象协作与职责检查

### 5.8 对象不是孤岛：先看小剧场

对象如果只保存自己的数据，这是不够的。项目里通常有多个对象协作：卡片进入卡片盒，卡片盒抽出练习材料，试次记录反应，报告整理员汇总结果。

<figure align="center">
  <img src="../assets/ch05/ch05_object_theater_story.png" alt="对象协作小剧场" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-8 对象协作小剧场</strong>：每个对象只演自己的角色，通过消息把任务交给下一个对象。</figcaption>
</figure>

设计对象时，可以先不写代码，只写一句话：

```text
LearningCard 准备内容，CardDeck 管理集合，Trial 记录一次反应，ReportBuilder 整理证据。
```

如果这句话说不清，代码通常也会混乱。类名不是越多越好，边界清楚才有价值。

对象之间如何协作，在 OOP 历史上有一个更核心的说法——"消息传递"（message passing）。一个对象不是直接操作另一个对象的内部数据，而是通过发送消息请求对方做某件事。这种理念让协作关系更清晰，也让每个对象的边界更容易守住。

Smalltalk在 OOP 的历史里之所以重要，不只是因为它影响了语法和环境，更因为它把"对象之间发送消息"做成了可以探索、可以观看、可以修改的学习空间。Adele Goldberg 等人推动的 Smalltalk 教育传统提醒我们：对象不是书本术语，它应该能帮助学习者观察系统如何一步步工作。

<figure align="center">
  <img src="../assets/ch05/ch05_adele_goldberg_story.png" alt="Adele Goldberg 照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S7 Adele Goldberg 与 Smalltalk 教育传统</strong>：OOP 不是只给大型工程师用的术语，也可以成为学习者理解系统协作的方式。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch05/ch05_smalltalk_environment_story.png" alt="Smalltalk/Squeak 环境截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S8 Smalltalk 环境</strong>：对象、窗口、消息和工具在同一个环境里互相呼应，这种“可探索性”影响了后来许多编程学习工具。</figcaption>
</figure>

### 5.10 类职责卡片

类职责卡片用于在编码前理清每个类的职责边界。下图展示了类职责卡片的设计：

<figure align="center">
  <img src="../assets/ch05/ch05_design_cards_preview.png" alt="类职责卡片预览图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-11 类职责卡片</strong>：写类之前，先写清楚它保存什么、会做什么、不该管什么。</figcaption>
</figure>

职责卡片最重要的一栏是“不该管什么”。如果一个类的不该管范围写不出来，它很容易变成万能类。比如：

| 类 | 应该管 | 不该管 |
| --- | --- | --- |
| `LearningCard` | 一张卡片的主题、问题、答案、预览 | 管理整盒卡片 |
| `CardDeck` | 卡片集合、添加、统计、筛选 | 保存单次实验反应 |
| `Trial` | 一次试次的刺激、反应、反应时 | 负责 GUI 和报告排版 |
| `ReportBuilder` | 汇总段落、写入报告 | 修改原始实验数据 |

这张表能帮你在写代码前先降噪。类不是越“能干”越好，而是越清楚越好。

### 5.11 对象协作消息图

对象协作消息图展示了对象之间如何通过消息互相协作。下图是各个对象之间的协作关系：

<figure align="center">
  <img src="../assets/ch05/ch05_object_collaboration_map.png" alt="对象协作消息图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-12 对象协作消息图</strong>：对象不是各写各的，而是通过"加入、抽取、记录、汇总"这样的消息完成同一件事。</figcaption>
</figure>

读这张图时，不要只看箭头。要问箭头背后的请求是否清楚：

| 消息 | 方向 | 含义 |
| --- | --- | --- |
| 加入 `add()` | `LearningCard -> CardDeck` | 一张卡片进入卡片盒 |
| 抽取 `draw()` | `CardDeck -> Trial` | 卡片盒给一次练习提供材料 |
| 记录 `record()` | `Trial -> ReportBuilder` | 试次把反应结果交给报告整理员 |
| 汇总 `summarize()` | `ReportBuilder -> LearningCard` | 报告反过来帮助卡片复习与改进 |

如果一条消息说不清，通常说明职责边界还没想清楚。先改设计，再急着写代码。

### 5.12 对象质量回执

对象质量回执用于检查对象设计是否合理。下图展示了质量回执的结构：

<figure align="center">
  <img src="../assets/ch05/ch05_object_quality_receipt.png" alt="对象质量回执" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-13 对象质量回执</strong>：用单一职责、数据贴近方法、消息清楚、组合优先和万能类风险检查对象设计。</figcaption>
</figure>

这份回执可以用来提醒你：OOP 失败时，问题经常不是语法，而是边界。一个项目里如果出现 `ProjectManager`、`Helper`、`Everything` 这种类名，要格外小心。它们可能正在吞掉太多职责。

xkcd 的“代码质量”梗图很好笑，是因为它戳中了所有程序员都经历过的尴尬：代码能跑，不代表它好理解；今天自己觉得“先凑合一下”的地方，明天可能变成别人接手时的迷宫。OOP 的职责卡片和质量回执，就是为了尽早发现这种迷宫入口。

<figure align="center">
  <img src="../assets/ch05/ch05_xkcd_code_quality.png" alt="xkcd 代码质量漫画" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-S9 xkcd：代码质量</strong>：幽默背后是真问题：如果对象边界不清楚，代码迟早会变成连作者自己都要绕路的迷宫。</figcaption>
</figure>

---

## 第四部分：面向对象程序设计示例

前三部分从最小类、属性方法、组合、对象协作到职责检查，逐步建立了 OOP 的基本概念。这一部分用一个完整的真实例子来串联这些概念：把第 4 章的 Stroop 数据浏览面板用面向对象的方式重写一遍。

打开并运行：

```bash
python code/ch05/04_make_stroop_gui_oop.py
```

你会看到一个和第 4 章一样的 GUI 窗口，但代码的写法完全不同了。原来的版本把数据加载、数据处理、界面绘制全部写在一个 `main()` 函数里。而新的版本把它拆成了 6 个职责清晰的类。

### 5.13 六个类，六个职责

| 类名 | 职责 | 对应第 4 章原函数中的哪一段 |
| --- | --- | --- |
| `StroopDataLoader` | 加载数据（JSON 文件或后备数据） | `load_data()` 函数 |
| `StroopProcessor` | 从原始数据计算指标和整理试次 | `build_panel_data()` 函数 |
| `MetricsDisplay` | 在面板上绘制指标卡片 | 指标卡片区的 Frame 和 Label |
| `TrialTable` | 在面板上绘制试次表格 | 试次表格区的 Treeview |
| `ActionBar` | 创建底部按钮行 | 按钮区的 Frame 和 Button |
| `StroopDashboard` | 主面板，组合所有子组件并启动 GUI | `main()` 中的窗口创建和组件组装 |

这个表格回答了本章最核心的问题：**一个类该管什么，不该管什么？**

- `StroopDataLoader` 只负责"从什么地方拿到数据"，不关心数据长什么样子。
- `StroopProcessor` 只负责"把原始数据算成面板需要的格式"，不关心怎么显示。
- `MetricsDisplay` 只负责"把指标画成卡片"，不关心数据从哪里来。
- `TrialTable` 只负责"把试次画成表格"，不关心指标的计算。
- `ActionBar` 只负责"创建按钮"，不关心按钮点击后做什么（现阶段按钮是禁用的）。
- `StroopDashboard` 负责"把上面五个对象组合起来"，但它自己不做具体的数据处理或界面绘制。

### 5.14 从代码中读出 OOP 思想

#### 5.14.1 封装：每个类有自己的数据和方法

在 `StroopDataLoader` 中，数据源路径 `_source` 和后备数据 `_fallback` 是内部状态。外部调用者只需要知道 `load()` 返回字典，`source_label` 返回文字说明，不需要知道文件具体在哪里。

```python
loader = StroopDataLoader()
raw = loader.load()           # 拿到数据，不关心数据来自文件还是后备
label = loader.source_label   # 拿到来源说明，不关心路径计算
```

这就是**封装**：对象隐藏内部细节，对外提供清晰的接口。

#### 5.14.2 组合：大对象拥有小对象

`StroopDashboard` 没有继承任何 UI 组件类，而是"拥有"它们：

```python
class StroopDashboard:
    def __init__(self) -> None:
        self._loader = StroopDataLoader()
        raw = self._loader.load()
        self._processor = StroopProcessor(raw)
        ...
    def run(self) -> None:
        MetricsDisplay(self._root, self._metrics).build()
        TrialTable(self._root, self._trials).build()
        ActionBar(self._root).build()
```

Dashboard 在 `run()` 中创建 `MetricsDisplay`、`TrialTable` 和 `ActionBar`，把窗口对象 `self._root` 传进去让它们绘制自己。Dashboard 知道这些组件存在，但组件之间互不知道——这就是**组合**的优势：替换或修改一个组件不会影响其他组件。

#### 5.14.3 `self` 的作用：区分"谁的"数据

在 `MetricsDisplay.build()` 中：

```python
class MetricsDisplay:
    def __init__(self, parent, metrics):
        self._parent = parent
        self._metrics = metrics

    def build(self):
        frame = tk.Frame(self._parent)   # self._parent 是这个对象的 parent
        ...
```

如果没有 `self`，方法就不知道 `_parent` 和 `_metrics` 属于哪个对象。`self` 让每个对象拥有自己的状态副本。创建两个 `MetricsDisplay` 对象时，它们各自记住自己的 `_parent` 和 `_metrics`，互不干扰。

#### 5.14.4 单一职责原则

回头对比第 4 章的 `main()` 函数：它既加载数据，又计算指标，又创建 Label、Frame、Treeview、Button。如果你要修改数据来源，你要在同一个函数里找到对应的那几行，还不能碰坏 GUI 代码。

而 OOP 版本中，修改数据来源只需要改 `StroopDataLoader`，其他五个类完全不需要动。这就是**单一职责原则**的价值：**一个类只有一个让它改变的理由。**

### 5.15 面向对象不是"多写几个文件"

有人会把 OOP 误解成"把一个大函数拆成好几个文件"。但真正重要的是拆分的**依据**。这个例子中的拆分依据是**职责边界**：

- 数据加载是一类职责
- 数据处理是另一类职责
- 指标卡片显示是一类职责
- 表格显示是一类职责
- 按钮区是一类职责
- 组合管理是全局职责

如果让 `StroopDataLoader` 也负责画表格，或者让 `TrialTable` 也负责加载数据，你会发现修改一个功能时又要动另一个功能——那就回到了第 4 章的问题。

运行 `04_make_stroop_gui_oop.py` 看到的窗口和第 4 章一样，但代码的组织方式完全不同。这正是本章想传达的核心：**面向对象的目的是让代码更容易理解、更容易修改、更容易测试，而不是让代码看起来"高级"。**

---

## 第五部分：排错、练习与验收

### 5.16 常见坑：先按职责边界排查

<figure align="center">
  <img src="../assets/ch05/ch05_pitfall_map.png" alt="第5章 OOP 常见坑排查图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图5-16 第5章常见坑排查</strong>：OOP 报错和设计混乱，通常可以从 `self`、对象身份、万能类、继承、数据行为分离和职责重叠排查。</figcaption>
</figure>

| 问题 | 典型现象 | 优先检查 |
| --- | --- | --- |
| 忘记 `self` | 方法里找不到属性，或变量名未定义 | 方法参数有没有 `self`，属性访问是否写成 `self.xxx` |
| 把类当对象 | 直接拿 `LearningCard.topic` 当具体主题 | 你是否创建了 `card = LearningCard(...)` |
| 万能大类 | 一个类越来越长，什么都管 | 能不能拆成卡片、卡片盒、试次、报告 |
| 过早继承 | 继承关系说不出“是一种” | 先改成组合 |
| 数据行为分离 | 函数之间传一大串参数 | 是否应该让对象自己保存状态并提供方法 |
| 职责重叠 | 两个类都在改同一份核心数据 | 回到职责卡片，重新划边界 |

遇到 OOP 问题时，先不要马上重写所有类。建议按这个顺序缩小范围：

1. 先用一个对象跑通最小例子。
2. 打印对象，确认属性值是否正确。
3. 单独调用一个方法，确认返回结果。
4. 再让两个对象协作。
5. 最后才加文件、GUI、报告和导出。

### 5.17 练习任务

1. 给 `LearningCard` 增加一个 `difficulty: int` 属性，表示卡片难度。
2. 修改 `preview()`，让它同时显示主题和难度。
3. 把 `CardDeck.cards` 从 `list[str]` 改成 `list[LearningCard]`，再运行测试。
4. 给 `CardDeck` 增加一个 `filter_by_tag(tag: str)` 方法。
5. 给 `Trial` 增加 `correct: bool` 属性，并写一个 `status()` 方法。
6. 打开 `code/ch05/04_make_stroop_gui_oop.py`，找到 `StroopDataLoader` 类，给它增加一个属性 `self.version = "1.0"`，然后在 `source_label` 末尾加上版本号。运行脚本观察面板顶部的数据来源文字变化。
7. 在 `StroopDashboard.run()` 中，在 `self._root.title("Stroop 数据浏览面板（OOP 版本）")` 这一行里把标题改成你自己的名字，运行脚本观察窗口标题变化。然后找到 `ActionBar` 类，把其中一个按钮的文字从"加载数据"改成"刷新数据"，观察按钮文字变化。

### 5.18 自测问题

1. 类和对象有什么区别？请用 `LearningCard` 举例。
2. 属性和方法分别负责什么？
3. 为什么方法里要写 `self.topic`，而不是直接写 `topic`？
4. `CardDeck` 和 `LearningCard` 为什么更适合组合，而不是继承？
5. `Trial` 对象适合保存哪些心理学实验信息？
6. 什么是万能类？它为什么危险？
7. 对象协作消息图里，“消息”代表什么？

### 5.19 学习复盘模板

可以在 `reports/ch05_review.md` 中写下：

```markdown
# 第5章复盘

## 我新增的能力
- 

## 我跑通的对象
- LearningCard：
- CardDeck：
- Trial：

## 我生成的证据文件
- 

## 我遇到的 OOP 问题
- 报错或现象：
- 原因：
- 修复方式：

## 我重新划清的职责
- 这个类应该管：
- 这个类不该管：

## 我准备迁移到后续章节
- GUI：
- 文件：
- 数据分析：
```

复盘可以把下一次调试的路标留下来。你现在把对象、职责、消息和输出文件写清楚，后面做综合项目时就不会重新猜。

### 5.20 本章总结

第5章的重点是学会用对象管理复杂度：

1. 类定义一种对象的共同结构。
2. 对象是按类创建出来的具体实例。
3. 属性保存对象状态。
4. 方法让对象使用自己的状态完成动作。
5. `self` 指向当前这个对象。
6. 组合表达“拥有”，通常比过早继承更稳。
7. 对象之间通过清楚消息协作。
8. 类职责卡片和质量回执能帮助你提前发现边界混乱。

在下一章，你会把对象交付包里的卡片和试次整理成更适合分析的数据结构。也就是说，第5章不是孤立地学 `class`，而是在给后续的数据分析、GUI 扩展和综合项目打地基。
