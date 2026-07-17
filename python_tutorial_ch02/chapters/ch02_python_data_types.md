# 第 2 章：Python 编程基础：数据、流程与函数

[TOC]

如果说第1章是在搭工作台，那么第2章就是开始认识材料。

木匠做桌子，要知道木板、螺丝、胶水、砂纸分别适合做什么。Python 也一样：程序里流动的东西不是一团模糊的“数据”，而是有性格、有用途、有边界的数据类型。

字符串适合保存文字，列表适合保存一串有顺序的东西，字典适合保存“名字对应信息”的结构，布尔值适合做判断，数值适合计算。学会选择容器以后，还要学会让程序根据条件选择、逐项循环，并把重复动作收进函数。类型选得对，代码会像整理好的桌面；类型选错，后面每一步都像在抽屉里翻耳机线。

本章的目标不是把所有函数背下来，而是建立一种判断力：

> 看到一份数据，我应该把它放进哪种容器里；接下来，程序应该选择、重复还是复用哪一步？

<figure align="center">
  <img src="../assets/ch02/ch02_cover.png" alt="第2章封面" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-1 第2章封面</strong>：数据类型像不同容器；先判断材料是什么，再决定用 `bool`、数值、字符串、列表还是字典。</figcaption>
</figure>

---

## 2.1 本章路线

本章按“常量、变量、布尔、条件、字符串、容器、循环、函数”这条路线展开，但不把它们当成孤立名词来背，而是放进真实任务里理解：

1. 先认识常量和关键字：哪些名字是 Python 自己保留的。
2. 再理解变量：变量不是盒子，更像标签。
3. 再学习布尔和条件：程序如何判断真假，并据此选择下一步。
4. 然后进入字符串：文字如何创建、拼接、查找、替换和切片。
5. 接着创建列表、元组、集合和字典：先把多份资料放进合适的容器。
6. 再学习列表和字典的常用操作：取、切、加、删、查。
7. 学习 `for`、`while` 和函数：让程序逐项处理资料，并把重复动作收好。
8. 用一个小项目把数据、条件、循环和函数组合起来。

这章会反复强调一个动作：先观察数据，再选择结构。不要先急着写代码。

阅读时建议保持一个节奏：先看图，明白这一节要解决什么问题；再读代码；最后自己运行配套脚本。图片负责建立直觉，代码负责验证直觉。

<figure align="center">
  <img src="../assets/ch02/ch02_roadmap.png" alt="第2章知识路线图" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-2 第2章知识路线图</strong>：从常量和变量出发，先理解数据与容器，再让条件、循环和函数真正处理这些资料。</figcaption>
</figure>

---

## 2.2 常量：Python 早就准备好的几个固定角色

Python 里有一些值很特殊，它们不是你随便起的名字，而是语言自带的固定角色。

初学阶段先抓住三个最常见的内置常量：

| 常量 | 含义 | 常见用途 |
| --- | --- | --- |
| `True` | 真 | 条件成立、开关打开 |
| `False` | 假 | 条件不成立、开关关闭 |
| `None` | 空值 | 目前还没有结果、暂时没有数据 |

另外还有 `Ellipsis` 和 `NotImplemented` 这类高级对象。现在只要知道它们也是 Python 自带的特殊值，不需要在本章背用法。

请注意大小写：Python 里的 `True` 和 `False` 首字母要大写。写成 `true` 或 `false`，Python 会把它当成普通变量名，然后发现你并没有定义它。

```python
passed = True
failed = False
answer = None

print(passed)
print(failed)
print(answer)
```

`None` 很有用。它像一张写着“还没有”的占位卡。

例如你正在记录学生的第一次练习成绩，但这个学生还没提交：

```python
first_score = None
```

这不是 0。0 是一个真实分数，`None` 表示“现在还没有分数”。这两者在程序里差别很大。

配套脚本：

```bash
python code/ch02/01_constants_keywords.py
```

---

## 2.3 关键字：Python 语言自己的保留词

关键字是 Python 已经拿去当语法用的词。你不能把它们当变量名。

例如：

```python
if = 10
```

这行代码会报错，因为 `if` 是条件判断语法的一部分，不是给你随便贴标签的名字。

你可以用标准库 `keyword` 打印 Python 当前版本的关键字：

```python
import keyword

print(keyword.kwlist)
print(len(keyword.kwlist))
```

这里第一次出现了 `len()`。`keyword.kwlist` 是一个保存关键字的列表，`len(keyword.kwlist)` 会返回列表里有多少项。外层的 `print(...)` 再把这个数字显示出来。嵌套调用要从里面往外读，下面两种写法结果相同：

```python
keyword_count = len(keyword.kwlist)
print(keyword_count)
```

初学时更推荐拆成两行，因为你能看见中间结果，也更容易判断是哪一步出错。

可以把关键字理解成“城市里的路牌”。路牌已经承担交通规则了，你不能把自己的书包也命名为“红绿灯”。

变量名应该避开关键字，也尽量避开容易误解的内置函数名，例如 `list`、`dict`、`str`、`sum`。不是绝对不能写，但初学阶段最好不要把这些词拿来当变量名。

更好的命名方式：

```python
scores = [86, 92, 78]
student_name = "小明"
favorite_color = "green"
```

---

## 2.4 变量：不是盒子，更像标签

很多人第一次学变量，会听到一句话：

> 变量就是一个盒子，里面装着值。

这个比喻对入门有一点帮助，但也容易误导。它会让人以为：

```python
a = 2
b = a
```

就是把 `a` 盒子里的 2 复制一份，放进 `b` 盒子。

在 Python 里，更准确的说法是：

> 变量名是贴在对象上的标签。

`a = 2` 的意思是：把名字 `a` 绑定到对象 `2` 上。

`b = a` 的意思是：让 `b` 也指向 `a` 当前指向的那个对象。

你可以运行下面的脚本观察：

```bash
python code/ch02/02_variables_labels.py
```

它会打印 `id(a)` 和 `id(b)`。`id()` 可以粗略理解成对象在内存中的身份编号。

```python
a = 2
b = a

print(id(a))
print(id(b))
```

你会发现，在这个例子里，`a` 和 `b` 一开始指向同一个对象。

然后我们重新赋值：

```python
b = 3
```

这不是把原来的 2 改成 3，而是让 `b` 这个标签改贴到对象 `3` 上。`a` 仍然指向 2。

这件事在后面学习列表、字典、函数参数时非常重要。现在先记住一句话：

> 变量名不是保险箱，而是便签纸。便签纸贴在哪里，Python 就去哪里找值。

<figure align="center">
  <img src="../assets/ch02/ch02_variable_label_metaphor.png" alt="变量标签模型" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-3 变量标签模型</strong>：左边是容易误会的“盒子感”，右边是更接近 Python 的“标签感”：名字可以指向同一个对象，也可以重新贴到新对象上。</figcaption>
</figure>

---

## 2.5 变量命名：名字要像路标，不要像谜语

变量名最重要的功能不是“让电脑看懂”。电脑其实不在乎你叫它 `x` 还是 `student_score`。变量名真正服务的是人，包括未来的你。

不建议：

```python
a = 86
b = 92
c = 78
```

更建议：

```python
math_score = 86
english_score = 92
python_score = 78
```

常见命名规则：

1. 可以包含字母、数字、下划线。
2. 不能以数字开头。
3. 不能使用 Python 关键字。
4. 区分大小写，`score` 和 `Score` 是两个名字。
5. 多个单词通常用小写加下划线：`student_name`。

可以给自己一个小练习：把下面这些坏名字改成好名字。

| 不推荐 | 问题 | 更推荐 |
| --- | --- | --- |
| `a` | 太模糊 | `reaction_time` |
| `data1` | 不知道是什么数据 | `pre_test_scores` |
| `list` | 覆盖内置类型名 | `word_list` |
| `myVeryLongVariableName` | 风格不统一 | `learning_days` |

变量名像路标。路标写得清楚，程序就像城市地图；路标乱写，代码就像没有门牌号的小区。

---

## 2.6 数据类型地图：先看材料，再选容器

如果把第2章比作材料仓库，数据类型地图就是货架平面图。它不会替你搬箱子，但会告诉你：文字放哪里、数字放哪里、判断放哪里、一串记录放哪里、带标签的完整记录放哪里。

Python 里能表示的材料很多：字符串、布尔、整数、浮点数、列表、元组、字典、集合、日期等。

初学阶段不用一次吃完。先抓住最常用的几类：

| 类型 | Python 名称 | 适合保存什么 |
| --- | --- | --- |
| 布尔 | `bool` | 判断结果：真或假 |
| 整数 | `int` | 次数、人数、分数、编号 |
| 浮点数 | `float` | 小数、时间、比例、平均值 |
| 字符串 | `str` | 文字、路径、姓名、题目 |
| 列表 | `list` | 一串有顺序的数据 |
| 元组 | `tuple` | 一组不打算修改的数据 |
| 字典 | `dict` | key 对应 value 的信息表 |
| 集合 | `set` | 去重、集合运算 |

本章重点讲 `bool`、`int`、`float`、`str`、`list`、`dict`。

新手最容易混淆的是“看起来像数字”和“真的能计算的数字”。请先会用 `type()` 看证据：

```python
score_text = "86"
score_number = 86

print(type(score_text))    # <class 'str'>
print(type(score_number))  # <class 'int'>
```

`type()` 接收一个值，返回这个值的类型。它只负责查看，不会修改原变量。`"86"` 是文字，适合展示；`86` 是整数，适合计算。

### 2.6.1 调用函数时，先看输入和输出

第 1 章已经见过 `print()` 和 `input()`。从这一章开始，函数会越来越多，但读法始终一样：

```python
rounded_score = round(86.666, 1)
```

按顺序拆开：

1. 函数名是 `round`，任务是取整或保留小数。
2. 第一个参数 `86.666` 是要处理的数字。
3. 第二个参数 `1` 表示保留 1 位小数。
4. 函数返回 `86.7`，赋值语句把结果保存到 `rounded_score`。

看到陌生函数时，不要只问“这行怎么抄”，而要问：它需要什么参数、返回什么类型、会不会修改原数据。后面每个新函数都可以用这三个问题拆开。

### 2.6.2 零基础常用内置函数工具箱

“内置函数”是 Python 安装好就能直接使用的函数，不需要先 `import`。下面这些会在后续章节反复出现：

| 函数 | 主要用途 | 返回什么 | 简单例子 |
| --- | --- | --- | --- |
| `print(...)` | 把内容显示到屏幕 | 主要看它产生的输出 | `print("完成")` |
| `input(...)` | 显示提示并等待键盘输入 | 字符串 `str` | `name = input("姓名：")` |
| `type(value)` | 查看值的类型 | 类型信息 | `type(86)` |
| `len(value)` | 计算字符串或容器里有多少项 | 整数 `int` | `len([86, 92])` |
| `sum(numbers)` | 把一组数字相加 | 数值 | `sum([86, 92])` |
| `min(numbers)` | 找最小值 | 容器中的一个值 | `min([86, 92])` |
| `max(numbers)` | 找最大值 | 容器中的一个值 | `max([86, 92])` |
| `round(number, digits)` | 取整或保留小数 | 新数字 | `round(86.666, 1)` |

把它们放进同一个成绩例子：

```python
scores = [86, 92, 78]

score_count = len(scores)
total_score = sum(scores)
lowest_score = min(scores)
highest_score = max(scores)
average_score = round(total_score / score_count, 1)

print("人数：", score_count)
print("总分：", total_score)
print("最低分：", lowest_score)
print("最高分：", highest_score)
print("平均分：", average_score)
```

输出：

```text
人数： 3
总分： 256
最低分： 78
最高分： 92
平均分： 85.3
```

这里故意没有写成 `round(sum(scores) / len(scores), 1)`。一行塞进三个函数虽然更短，但初学时不利于检查。先把每一步交给一个清楚的变量，熟练以后再决定是否合并。

`input()` 有一个必须提前知道的规则：**无论键盘输入看起来像姓名还是数字，它返回的都是字符串。**如果要计算，需要转换类型：

```python
age_text = input("请输入年龄：")
age = int(age_text)
print("明年年龄：", age + 1)
```

输入 `18` 时，`age_text` 是字符串 `"18"`，`int(age_text)` 才得到整数 `18`。输入无法转换的文字时会出现 `ValueError`，这不是电脑坏了，而是材料不适合这个转换工具。

### 2.6.3 内置函数、方法和模块函数不是一回事

它们都带圆括号，但所属位置不同：

```python
scores = [86, 92, 78]
print(len(scores))          # 内置函数：直接写名字
scores.append(88)           # 方法：由列表 scores 提供

import math
print(math.floor(3.8))      # 模块函数：由 math 工具箱提供
```

- `len(scores)` 不属于某一个列表对象，Python 可以用它统计多种容器。
- `scores.append(88)` 属于列表，点号左边决定了有哪些方法可以用。
- `math.floor(3.8)` 属于 `math` 模块，所以要先 `import math`。

关键字参数会写成 `名字=值`，例如：

```python
print("A", "B", sep=" | ")
```

这里 `sep=" | "` 指定多个输出之间用什么分隔。它不是在创建变量，而是在明确告诉 `print()`：这一次把参数隔开的文字是什么。

忘记函数用途时，可以在终端或 Python 控制台中查看帮助：

```python
help(len)
```

注意这里写 `help(len)`，不是 `help(len())`。前者把函数本身交给 `help()` 查询；后者会先尝试执行缺少参数的 `len()`，反而先报错。

配套脚本：

```bash
python code/ch02/17_builtin_functions_basics.py
```

先把这张函数地图放在脑子里：它不是知识点海报，而是后面所有例子的导航牌。

<figure align="center">
  <img src="../assets/ch02/ch02_data_type_atlas.png" alt="数据类型地图" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-4 数据类型地图</strong>：图里只保留类型节点；具体怎么选，交给正文里的任务和例子来判断。</figcaption>
</figure>

Claude Shannon 曾把通信问题讲得非常直接：消息要经过编码、传输、解码，最后被接收者理解。Python 里的数据类型也有类似的味道。`"86"` 和 `86` 看起来只差一对引号，但前者是文字，后者是数字；一个适合展示，一个适合计算。类型不是装饰，而是程序理解信息的方式。

所以本章不是在背一串单词，而是在练一种判断：这份信息到底应该以什么形态进入程序？

<figure align="center">
  <img src="../assets/ch02/ch02_information_history_claude_shannon.png" alt="Claude Shannon 肖像" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-5 Claude Shannon</strong>：信息论把“消息”变成可以度量、编码和传输的对象；学习数据类型，也是在学习如何给信息选择合适的表示方式。</figcaption>
</figure>

这时可以想象自己拿着一只“类型选择罗盘”。罗盘不会替你写代码，但它会先把方向指清楚：这份数据是要计算、要展示、要按顺序保存、要按名字查找、要判断真假，还是暂时没有值？

<figure align="center">
  <img src="../assets/ch02/ch02_type_compass_preview.png" alt="类型选择罗盘预览" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-6 类型选择罗盘</strong>：看到新数据时，先问它要完成什么任务，再选择 `str`、`list`、`dict`、`bool`、数值类型或 `None`。</figcaption>
</figure>

选择类型时，可以先问自己六个问题：

1. 这是一个判断吗？如果是，用 `bool`。
2. 这是要计算的数量吗？如果是，用 `int` 或 `float`。
3. 这是一段文字吗？如果是，用 `str`。
4. 这是一串有顺序的数据吗？如果是，用 `list`。
5. 这是“名字对应信息”的查找表吗？如果是，用 `dict`。
6. 这里是不是暂时没有值？如果是，用 `None`，不要用 `0` 或空字符串假装有结果。

数据类型像工具箱里的工具。锤子、剪刀、尺子都很有用，但拿剪刀去敲钉子，场面就会变得很有教育意义。Python 也是一样：类型选错，后面就会出现很多别扭的转换和报错；类型选对，代码会顺着数据本身的形状往前走。

---

## 2.7 布尔类型：程序里的红绿灯

19 世纪的 George Boole 想做一件有点大胆的事：把人的逻辑推理变成可以计算的符号系统。换句话说，他想让“如果……那么……”“同时满足”“至少满足一个”这些判断，像加减乘除一样被严肃处理。很多年以后，计算机把这个思想变成了 `True` 和 `False`。

<figure align="center">
  <img src="../assets/ch02/ch02_history_george_boole.png" alt="George Boole肖像" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-7 George Boole肖像</strong>：布尔值的名字来自数学家 George Boole；今天的 `True` 和 `False`，背后是把复杂推理压缩成“真/假”判断的思想。</figcaption>
</figure>

所以当你写下：

```python
score = 86
passed = score >= 60
```

你不是在写一个小玩具，而是在使用一套已经流进现代计算机血液里的逻辑语言。分数够了，`passed` 就是 `True`；分数不够，`passed` 就是 `False`。这里的 `passed` 不是分数本身，而是一次判断的结果。

布尔类型只有两个值：

```python
True
False
```

它适合表达判断。

```python
score = 86
passed = score >= 60

print(passed)
```

这里 `score >= 60` 会得到一个布尔值。分数大于等于 60，结果就是 `True`；否则就是 `False`。

布尔值经常配合 `if` 使用：

```python
if passed:
    print("通过")
else:
    print("继续练习")
```

布尔值像程序里的红绿灯。灯亮，程序走这条路；灯不亮，程序换另一条路。

---

## 2.8 and、or、not：把多个条件组合起来

三个常见逻辑运算：

| 运算 | 含义 | 例子 |
| --- | --- | --- |
| `and` | 两边都为真，结果才真 | `has_id and has_ticket` |
| `or` | 至少一边为真，结果就真 | `is_admin or is_teacher` |
| `not` | 反过来 | `not is_late` |

<figure align="center">
  <img src="../assets/ch02/ch02_bool_logic_switchboard.png" alt="布尔逻辑开关台" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-8 布尔逻辑开关台</strong>：`and` 像两盏灯都要亮，`or` 像至少亮一盏，`not` 像把结果翻面。</figcaption>
</figure>

例子：

```python
has_homework = True
has_finished = False

print(has_homework and has_finished)
print(has_homework or has_finished)
print(not has_finished)
```

配套脚本：

```bash
python code/ch02/03_bool_numbers.py
```

优先级要记住：

```text
not > and > or
```

不过真正写代码时，不要把优先级当智力题。复杂条件里直接加括号。

```python
can_join = (age >= 18 and has_ticket) or is_staff
```

括号不是丢人，是给未来读代码的人留灯。

### 2.8.1 条件语句：让程序根据情况做选择

到这里你已经能得到 `True` 和 `False`。条件语句要解决的下一件事是：**结果不同，程序接下来该做什么？**

先从最常见的比较开始：

```python
score = 72

print(score >= 60)  # True
print(score == 100) # False
```

`>=` 表示“大于或等于”，`==` 表示“是否相等”。注意，`=` 是把值交给变量，`==` 才是在比较两个值是否相等。

如果分数达到 60，就显示“通过”；否则显示“继续练习”：

```python
score = 72

if score >= 60:
    print("通过")
else:
    print("继续练习")
```

这里有三条必须一次记住的规则：

1. `if`、`elif`、`else` 这一行末尾要有英文冒号 `:`。
2. 下一行向右缩进 4 个空格，表示“这几行归这个条件管”。
3. 缩进结束，程序就回到外层继续往下执行；不要混用 Tab 和空格。

分数不只有“通过”和“不通过”时，可以用 `elif` 增加中间分支：

```python
score = 86

if score >= 90:
    level = "优秀"
elif score >= 60:
    level = "通过"
else:
    level = "需要复习"

print(level)
```

条件也常用来先确认资料是否存在。这个写法会在访问字典前先问一句，避免突然遇到 `KeyError`：

```python
student = {"name": "小明"}

if "age" in student:
    print(student["age"])
else:
    print("还没有年龄记录")
```

配套脚本：

```bash
python code/ch02/13_control_flow_basics.py
```

第一次运行前，先猜一猜三个分数会落进哪个分支；运行后把其中一个分数改成 `59`，再看输出如何变化。代码不是背出来的，分支的手感来自“改一个条件，看到一条不同的路”。

---

## 2.9 数值类型：整数、浮点数和复数

Python 常见数值类型包括：

| 类型 | 说明 | 例子 |
| --- | --- | --- |
| `int` | 整数 | `10`、`-3`、`0` |
| `float` | 浮点数 | `3.14`、`0.5` |
| `complex` | 复数 | `1 + 2j` |

有些旧资料会提到 `long`。在 Python 3 里，`int` 已经可以表示任意精度整数，日常学习不需要单独区分 `long`。

常见计算：

```python
fixation_duration_ms = 600
trial_count = 24
total_time_ms = fixation_duration_ms * trial_count

print(total_time_ms)
```

如果你做心理学实验，`fixation_duration_ms = 600` 可以表示注视点持续 600 毫秒。把单位写进变量名，后面就不容易把毫秒、秒和次数混在一起。

---

## 2.10 取整：round、floor、ceil 不是一回事

Python 里有三个常见取整方法：

| 方法 | 含义 |
| --- | --- |
| `round(x)` | 四舍五入，但 Python 的舍入规则要注意 |
| `math.floor(x)` | 向下取整 |
| `math.ceil(x)` | 向上取整 |

三种方法看起来都在“去掉小数”，但它们面对的是三种不同任务：显示一个近似值、保守地向下取、保证够用地向上取。先把区别看清楚，再写代码会稳很多。

<figure align="center">
  <img src="../assets/ch02/ch02_number_rounding_chart.png" alt="数值取整图表" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-9 数值取整图表</strong>：取整不是随便抹零，向上、向下和四舍五入各有自己的规则。</figcaption>
</figure>

例子：

```python
import math

value = 2.7

print(round(value))
print(math.floor(value))
print(math.ceil(value))
```

输出大致是：

```text
3
2
3
```

不要把它们混用。比如：

- 处理索引位置时，通常要非常小心，不能随便四舍五入。
- 处理得分显示时，可能用 `round()`。
- 处理分页数量时，经常用 `ceil()`，因为剩下一点点也要多一页。

Python 的 `round()` 还有一个细节：当正好遇到 `.5` 时，它采用“银行家舍入”的规则，不总是简单向上。你可以运行 `round(2.5)` 和 `round(3.5)` 看看：结果分别是 `2` 和 `4`。初学阶段先知道这件事；真正遇到金额、实验计时或统计精度时，再细查舍入规则。

---

## 2.11 字符串：文字也是数据

数字能回答“多少”，字符串负责回答“是谁、叫什么、写了什么、放在哪里”。做一个 Stroop 小实验时，反应时可以是 `523.4`，正确与否可以是 `True`，但刺激词、被试编号、实验条件和输出文件名都离不开字符串。

所以不要把字符串理解成“给程序加点装饰文字”。它更像实验记录本上的标签纸：没有标签，数据就只剩下一堆孤零零的数字；标签清楚，后面才能检索、统计、复盘和写报告。

<figure align="center">
  <img src="../assets/ch02/ch02_string_material_workbench.png" alt="字符串材料工作台" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-10 字符串材料工作台</strong>：实验说明、被试编号、刺激词、文件路径和日志备注，看起来都是“文字”，在程序里却都是需要认真保存、查找、替换和切片的数据。</figcaption>
</figure>

字符串用来保存文本。

```python
country_name = "China"
student_name = "小明"
message = "Hello, Python!"
```

单引号和双引号都可以：

```python
name1 = 'Python'
name2 = "Python"
```

如果字符串本身包含引号，可以换一种引号包起来：

```python
sentence = "I'm learning Python."
```

多行字符串可以用三个引号：

```python
intro = """第一行
第二行
第三行"""
```

字符串不是“装饰品”，它经常保存非常关键的信息：文件路径、实验说明、被试编号、题目文本、网页内容、日志信息。

---

## 2.12 字符串类型转换：str、int、float、chr、ord

常见转换：

```python
age = 18
age_text = str(age)

score_text = "95"
score = int(score_text)

reaction_time_text = "523.4"
reaction_time = float(reaction_time_text)
```

如果你把字符串和数字直接相加，Python 会困惑：

```python
age = 18
print("年龄：" + age)
```

这会报错，因为字符串不能直接和整数拼接。

你可以写：

```python
age = 18
print("年龄：" + str(age))
```

或者更推荐：

```python
age = 18
print(f"年龄：{age}")
```

`chr()` 和 `ord()` 可以在字符和编码之间转换，初学阶段了解即可：

```python
print(chr(65))
print(ord("A"))
```

输出：

```text
A
65
```

配套脚本：

```bash
python code/ch02/04_string_playground.py
```

---

## 2.13 字符串格式化：从 `%` 到 f-string

常见字符串格式化方式有三种：

```python
str_name = "Pony"
int_age = 49

text1 = "My name is %s and my age is %d!" % (str_name, int_age)
text2 = "My name is {} and my age is {}!".format(str_name, int_age)
text3 = f"My name is {str_name} and I am {int_age} years old."
```

现在更推荐 f-string，因为它最直观。

```python
name = "小明"
score = 86

report = f"{name} 的本次练习分数是 {score}。"
print(report)
```

f-string 像在句子里挖了一个小窗口，窗口里可以直接放变量。

---

## 2.14 字符串查找与替换

`find()` 和 `replace()` 都是字符串方法，读法是“让点号左边这段字符串执行一个动作”。字符串本身不能原地修改，所以这些方法要么返回位置，要么返回一段新字符串。

查找：

```python
info = "abca"

print(info.find("a"))
print(info.find("a", 1))
print(info.find("333"))
```

`find()` 的第一个参数是要找的文字，第二个可选参数是从哪个索引开始找。找到就返回第一次出现的索引，找不到就返回 `-1`；它不会返回 `True` 或 `False`。

替换：

```python
message = "I like Matlab."
message = message.replace("Matlab", "Python")

print(message)
```

输出：

```text
I like Python.
```

注意：`replace()` 不会把原字符串原地改掉，而是返回一个新字符串。所以更稳妥的写法是把结果重新赋值给变量，或者赋值给一个新名字。字符串替换常用于批量更新旧术语、旧路径、旧实验说明。

---

## 2.15 字符串切片：左闭右开

字符串可以按索引取值：

```python
word = "huawei"

print(word[0])
print(word[1])
print(word[-1])
```

正向索引从 0 开始：

```text
h  u  a  w  e  i
0  1  2  3  4  5
```

反向索引从 -1 开始：

```text
h   u   a   w   e   i
-6 -5  -4  -3  -2  -1
```

切片最容易让新手迷糊的地方，是数字标的不是“格子本身”，而是字符之间的边界。先把这把尺子看懂，再写 `start:end` 会轻松很多。

<figure align="center">
  <img src="../assets/ch02/ch02_string_slice_ruler.png" alt="字符串切片尺" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-11 字符串切片尺</strong>：数字标的是边界，不是“格子本身”；切片要学会看起点和终点。</figcaption>
</figure>

切片语法：

```python
word[start:end]
```

规则是左闭右开：包含 `start`，不包含 `end`。

```python
word = "huawei"
print(word[0:3])
```

输出：

```text
hua
```

为什么不包含右边界？一个好处是长度很好算：

```text
word[0:3] 的长度 = 3 - 0 = 3
```

这件事在列表里也一样。取单个字符时，如果索引超过范围，会出现 `IndexError`；切片超过范围通常不会报错，但结果可能比你想象的短。

---

## 2.16 字符串切割：split

如果你有一段文本：

```python
my_string = "song huan gong"
```

可以用 `split()` 切成列表：

```python
str_list = my_string.split(" ")
print(str_list)
```

输出：

```text
['song', 'huan', 'gong']
```

如果不写分隔符，`split()` 默认按空白字符切：

```python
print(my_string.split())
```

这在处理问卷数据、日志、用户输入时很常见。

这里要把输入和输出分清：`my_string` 是字符串，`split(" ")` 接收一个分隔符，返回一个新列表。它不会修改原字符串。空括号的 `split()` 不是“什么都不做”，而是使用默认规则：连续空格、制表符和换行都可以作为分隔位置。

---

### 2.16.1 数据结构先从“创建”开始

“数据结构”并不神秘，它只是把多个值按某种规则放在一起。初学时先把四种最常用的容器认全：

| 容器 | 创建一个有内容的容器 | 创建空容器 | 先记住什么 |
| --- | --- | --- | --- |
| `list` 列表 | `[86, 92, 78]` | `[]` 或 `list()` | 有顺序，可以修改 |
| `tuple` 元组 | `("P001", 19)` | `()` 或 `tuple()` | 有顺序，创建后不改 |
| `set` 集合 | `{"Python", "文件"}` | `set()` | 不重复，不保证位置 |
| `dict` 字典 | `{"name": "小明"}` | `{}` 或 `dict()` | 用 key 找 value |

把它们放在一起看会更清楚：

```python
scores = [86, 92, 78]                  # 列表：一串有顺序的分数
participant = ("P001", 19)            # 元组：一组固定的信息
skills = {"Python", "文件", "Python"}  # 集合：重复的 "Python" 只会保留一次
student = {"name": "小明", "age": 19}  # 字典：字段和值配对
```

两个新手最容易踩到的细节：

```python
empty_dict = {}      # 这是空字典
empty_set = set()    # 空集合必须这样写，{} 不是集合

one_item_tuple = ("Python",)  # 逗号不能省；("Python") 只是一个字符串
```

现在不用急着记住所有方法。先问数据本身：它有没有顺序？以后要不要改？会不会重复？是不是“字段对应信息”？容器是为了把真实资料放稳，不是为了把括号背得更花。

配套脚本：

```bash
python code/ch02/14_container_creation.py
```

---

## 2.17 列表：一排可调整的抽屉

如果要把列表讲得有一点心理学味道，可以从 Hermann Ebbinghaus 说起。

他研究记忆时，会反复记录“过了多久还能记住多少”。这类数据天然有顺序：第 1 次测试、第 2 次测试、第 3 次测试；或者 5 分钟后、1 小时后、1 天后。Python 的列表特别适合装这种数据。

<figure align="center">
  <img src="../assets/ch02/ch02_psychology_ebbinghaus_memory.png" alt="Hermann Ebbinghaus肖像" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-12 Hermann Ebbinghaus肖像</strong>：记忆研究里经常会收集一串测试结果；这种“有顺序的一排数据”，正是列表最擅长处理的材料。</figcaption>
</figure>

```python
retention_rates = [1.00, 0.82, 0.65, 0.48, 0.36]
test_times = ["刚学完", "20分钟后", "1小时后", "1天后", "1周后"]
```

你不需要一开始就会画遗忘曲线。先会把这些结果整齐放进列表，再会取出、追加、计算平均值，就已经迈过了“把心理学材料变成可计算数据”的第一步。

<figure align="center">
  <img src="../assets/ch02/ch02_list_workbench.png" alt="列表工作台" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-13 列表工作台</strong>：列表像一排有顺序的抽屉，位置从 0 开始；取值、切片、追加和删除都围绕顺序展开。</figcaption>
</figure>

列表用来保存一串有顺序的数据，而且列表可以被修改。

```python
my_list = ["I", "love", "you", "my", "dear"]
```

列表也从 0 开始索引：

```python
print(my_list[1])
```

输出：

```text
love
```

列表切片：

```python
print(my_list[0:2])
```

输出：

```text
['I', 'love']
```

再次提醒：左闭右开。

配套脚本：

```bash
python code/ch02/05_list_dict_workshop.py
```

---

## 2.18 列表嵌套：列表里还能放列表

先看一个并列列表的例子：

```python
number_list = [5, 2, 1]
word_list = ["I", "love", "you"]
nested_list = [number_list, word_list]

print(nested_list)
```

输出：

```text
[[5, 2, 1], ['I', 'love', 'you']]
```

这就是嵌套列表：列表里的元素仍然可以是列表。

它像一个柜子里有两层抽屉，也像套娃一层套一层：

<figure align="center">
  <img src="../assets/ch02/ch02_nested_data_matryoshka.png" alt="套娃照片" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-14 套娃与嵌套结构</strong>：嵌套列表就像套娃，一层里面还有一层；它很有用，但层数太多时也会让人找不着出口。</figcaption>
</figure>

```python
print(nested_list[0])
print(nested_list[0][1])
```

`nested_list[0]` 先取出第一层里的第一个列表，`nested_list[0][1]` 再从这个子列表里取第 2 个元素。

初学阶段不要滥用嵌套。两层还好，三层以上就要考虑是否应该换成字典、表格或类。真正成熟的写法不是“能套多深”，而是“别人一眼能不能看懂你在第几层”。

---

## 2.19 列表合并、添加、删除和乘法

合并：

```python
list1 = ["5", "2", "0"]
list2 = ["I", "love", "you"]

print(list1 + list2)
```

添加：

```python
my_list = ["I", "love", "you"]
my_list.append("Python")

print(my_list)
```

`append()` 会直接修改原列表，不需要写成 `my_list = my_list.append("Python")`。

把它按函数调用的四个问题拆开：点号左边是要修改的列表，括号里是要追加的一个值，动作发生在列表末尾，返回值是 `None`。因此下面这种写法会把变量变成 `None`：

```python
# 错误示范：不要这样写
my_list = my_list.append("Python")
```

删除：

```python
del my_list[2]
print(my_list)
```

乘法：

```python
letters = ["a", "b"]
print(letters * 3)
```

输出：

```text
['a', 'b', 'a', 'b', 'a', 'b']
```

列表有加法和乘法，但没有“列表减法”。你不能写：

```python
list1 - list2
```

如果要删除某个元素，要用 `del`、`remove()` 或列表推导式等方法。

这台 IBM 080 打孔卡分拣机看起来像一排机械抽屉：卡片从入口进去，机器根据打孔位置把它们分到不同槽里。它提醒我们一件事：数据从来不是“随便堆着就行”。学生记录、实验 trial、单词卡片、文件清单，只要数量一多，就需要顺序、索引、分类和检索。

列表像一叠按顺序排好的卡片，适合“第 1 次、第 2 次、第 3 次”这种材料；字典像给每张卡片贴上清楚标签，适合“被试编号对应哪条记录”这种查找。理解了这台老机器，再看 Python 的列表和字典，就不再像抽象语法，而像给科研卡片工厂安装了两种分拣装置。

<figure align="center">
  <img src="../assets/ch02/ch02_punch_card_sorter_photo.png" alt="IBM 080 打孔卡分拣机照片" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-15 IBM 080 打孔卡分拣机</strong>：在电子表格和数据库普及之前，数据也要按字段分拣、排序和归档；今天的 `list` 与 `dict`，其实是在用代码接管这套整理工作。</figcaption>
</figure>

---

## 2.20 字典：用 key 找 value

在没有搜索框的年代，图书馆靠一张张卡片组织知识。你想找一本书，不会从第一张卡片开始数到第一万张，而是按作者、题名或主题去检索。

Python 的字典也有这种气质。列表问的是：“第几个元素是什么？”字典问的是：“这个 key 对应什么 value？”

<figure align="center">
  <img src="../assets/ch02/ch02_dictionary_card_catalog_photo.png" alt="图书馆卡片目录抽屉" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-16 图书馆卡片目录抽屉</strong>：字典像一套检索系统，不是靠“第几个”去找，而是靠清楚的 key 直接找到对应信息。</figcaption>
</figure>

如果你做心理学问卷整理，字典会非常自然：

```python
participant = {
    "id": "P001",
    "age": 19,
    "condition": "stroop_conflict",
    "mean_reaction_time": 612.5,
}
```

这份记录不需要背位置。你要年龄，就查 `"age"`；要实验条件，就查 `"condition"`。代码读起来像在翻一张资料卡。

<figure align="center">
  <img src="../assets/ch02/ch02_dict_mapping_card.png" alt="字典映射卡" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-17 字典映射卡</strong>：左边是 key，右边是 value；字典最重要的能力，就是不用数位置，直接按名字查信息。</figcaption>
</figure>

字典的英文是 dictionary，也常被理解为 map。它最重要的特点是：

> 每个元素都有一个 key 和对应的 value。

列表靠位置找东西，字典靠 key 找东西。

```python
favorite_color = {
    "小美": "粉色",
    "小明": "黄色",
    "小东": "绿色",
}
```

查询：

```python
print(favorite_color["小美"])
```

输出：

```text
粉色
```

这就像查字典：你用“词”去查“解释”。在程序里，你用 key 去查 value。初学阶段，key 先优先使用字符串或数字；不要把列表拿来当 key。

---

## 2.21 字典的增、删、改、查

新增：

```python
favorite_color["小红"] = "紫色"
```

修改：

```python
favorite_color["小明"] = "绿色"
```

删除：

```python
del favorite_color["小东"]
```

查询：

```python
color = favorite_color["小美"]
```

完整例子：

```python
favorite_color = {
    "小美": "粉色",
    "小明": "黄色",
    "小东": "绿色",
}

favorite_color["小红"] = "紫色"
favorite_color["小明"] = "绿色"
del favorite_color["小东"]

print(favorite_color)
```

字典适合表达“谁对应什么”：

| 场景 | key | value |
| --- | --- | --- |
| 学生成绩 | 姓名 | 分数 |
| 单词表 | 英文单词 | 中文解释 |
| 文件索引 | 文件名 | 文件路径 |
| 实验记录 | 被试编号 | 反应数据 |

---

## 2.22 字典常见坑：key 不存在

如果你访问一个不存在的 key：

```python
favorite_color = {"小美": "粉色"}

print(favorite_color["小明"])
```

会出现 `KeyError`。

你可以先判断：

```python
if "小明" in favorite_color:
    print(favorite_color["小明"])
else:
    print("还没有记录小明的颜色")
```

也可以使用 `get()`：

```python
color = favorite_color.get("小明", "未知")
print(color)
```

`get()` 的第一个参数是要查询的 key，第二个参数是找不到时使用的默认值。如果 key 存在就返回对应 value，不存在就返回默认值。它只负责读取，不会把 `"小明": "未知"` 自动写进字典。

---

## 2.23 循环与函数：让程序处理一批资料

到目前为止，程序大多只处理一个值。真实资料往往是一组分数、一批文件或多位学生记录；这时不该把同样的代码复制十遍，而要让程序重复做同一类动作。

### 2.23.1 `for` 循环：依次处理容器里的每一项

`for` 最自然的读法是：“对于列表里的每一个分数，做一次缩进中的动作。”

```python
scores = [86, 92, 78]

for score in scores:
    print("正在检查：", score)
```

每轮循环，变量 `score` 会依次取到 `86`、`92`、`78`。它只是当前这一项的临时名字，不需要事先创建，也不该在循环外依赖它。

当需要按次数重复时，用 `range()`：

```python
for attempt in range(1, 4):
    print(f"第 {attempt} 次练习")
```

`range()` 常用的三种写法是：

| 写法 | 产生的整数 |
| --- | --- |
| `range(4)` | `0、1、2、3` |
| `range(1, 4)` | `1、2、3` |
| `range(1, 6, 2)` | `1、3、5` |

它们都不包含停止位置。第三个参数是步长，表示每次增加多少。想同时得到“第几项”和“内容”时，再用 `enumerate()`：

```python
for index, score in enumerate(scores, start=1):
    print(f"第 {index} 次分数：{score}")
```

`enumerate()` 接收一个可遍历的对象，这里是列表 `scores`；它每轮提供“编号和值”这一对结果。`start=1` 是关键字参数，表示编号从 1 开始，默认本来是从 0 开始。`index, score` 用两个变量分别接住这一对结果。

### 2.23.2 把条件放进循环：累积、筛选与 `append()`

下面这段就是后面读文件、遍历目录时会反复遇到的骨架：逐项查看，满足条件时收集结果。

```python
scores = [86, 55, 92, 48]
passed_scores = []
total = 0

for score in scores:
    total += score
    if score >= 60:
        passed_scores.append(score)

average_score = total / len(scores)
print("通过的分数：", passed_scores)
print("平均分：", average_score)
```

`total` 是累积器，`passed_scores` 是收集结果的列表。`total += score` 是 `total = total + score` 的简写：用旧总数加上当前分数，再把新结果放回 `total`。`append()` 的意思不是“生成一个新列表”，而是把当前项追加到已有列表末尾。

### 2.23.3 `while` 循环：只在“条件还成立”时继续

`for` 适合“我手上已经有一批东西”；`while` 适合“我不知道还要几轮，只知道什么时候该停”。初学阶段先用一个会变化的计数器，避免无意间写出无限循环：

```python
remaining = 3

while remaining > 0:
    print(f"还剩 {remaining} 次练习")
    remaining -= 1

print("本轮结束")
```

如果忘记 `remaining -= 1`，条件会一直为真，程序就不会停下来。第一次写 `while` 时，先在纸上写出“哪个变量会改变、什么条件会结束”。

### 2.23.4 函数：给一段可复用动作取名字

循环解决“重复做”，函数解决“把一段动作收好，以后再用”。函数要先定义，之后才调用：

```python
def score_level(score):
    if score >= 90:
        return "优秀"
    if score >= 60:
        return "通过"
    return "需要复习"

print(score_level(86))
```

定义函数时写在括号里的 `score` 叫**形参**，它像函数预留的一张收件单；调用 `score_level(86)` 时真正传进去的 `86` 叫**实参**。`return` 把计算结果交还给调用处，并立刻结束本次函数运行。函数里的 `score` 只在函数内部使用，不会自动改掉外面的同名变量。

最好把“计算”和“显示”分开：

```python
level = score_level(86)
print(level)
```

这样 `level` 后面还能继续参加判断、写入文件或放进字典。如果函数内部只 `print()` 却不 `return`，屏幕上虽然能看到文字，调用处拿到的返回值却是 `None`。

函数也可以有多个参数和默认值：

```python
def greet(name, punctuation="！"):
    return "你好，" + name + punctuation

message1 = greet("小明")
message2 = greet("小美", punctuation="。")

print(message1)
print(message2)
```

`name` 没有默认值，调用时必须提供；`punctuation` 默认使用中文感叹号，需要改变时可以用关键字参数明确指定。

配套脚本：

```bash
python code/ch02/15_loop_basics.py
python code/ch02/16_function_basics.py
```

跑完以后，回到 ch03 再看到 `for line in file:`、`if path.is_file():` 或 `records.append(...)` 时，它们就不再是凭空出现的符号，而是在处理另一种容器：文件和路径。

---

## 2.24 本章小项目：学习记录整理器

现在把本章内容串起来。

我们要整理一位学生的学习记录：

- 姓名：字符串 `str`
- 分数：列表 `list`
- 是否通过：布尔 `bool`
- 平均分：浮点数 `float`
- 技能清单：列表 `list`
- 完整记录：字典 `dict`

把这些材料连起来，就得到一条很小但很真实的数据流水线：先有输入，再整理成结构，最后生成报告。

<figure align="center">
  <img src="../assets/ch02/ch02_mini_project_dashboard.png" alt="本章小项目" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-18 本章小项目</strong>：输入、列表、字典、报告连成一条小流水线，数据类型第一次合在一起做事。</figcaption>
</figure>

配套脚本：

```bash
python code/ch02/06_learning_record_project.py
```

核心结构：

```python
student = {
    "name": "小明",
    "scores": [86, 92, 78],
    "skills": ["字符串", "列表", "字典"],
    "notes": "索引从 0 开始，切片左闭右开。",
}
```

用函数、循环和条件整理分数：

```python
def build_report(student):
    total = 0
    passed_scores = []

    for score in student["scores"]:
        total += score
        if score >= 60:
            passed_scores.append(score)

    average_score = total / len(student["scores"])
    if average_score >= 60:
        status = "通过"
    else:
        status = "需要继续练习"

    return average_score, passed_scores, status
```

这个小项目的意义不是“写一个多厉害的软件”，而是让你第一次看见：数据结构、条件、循环和函数会一起工作。后面 ch03 的文件内容、ch04 的用户输入、ch05 的对象属性，都会接上同一条思路。

现在再看终端运行图，就不会觉得它突然了。图中第一段运行的是变量标签脚本：`a` 和 `b` 先指向同一个整数对象，`b = 3` 以后，`b` 改贴到新对象上。第二段运行的是学习记录小项目：字符串保存姓名，列表保存分数，字典保存整份记录；`for` 逐项处理分数，`if` 判断是否通过，函数把报告生成过程收起来。

这张图要传达的不是“终端长什么样”，而是：数据类型最终要能在真实脚本里跑起来、打印出来、保存下来。

<figure align="center">
  <img src="../assets/ch02/ch02_powershell_data_type_run.png" alt="PowerShell真实运行数据类型脚本" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-19 PowerShell真实运行数据类型脚本</strong>：在终端里运行变量脚本和学习记录项目，能看到 `id()`、`dict`、`list` 与输出文件一起出现，数据类型不再只是纸面概念。</figcaption>
</figure>

---

## 2.25 本章常见报错地图

如果把程序想象成一张实验记录表，报错就像红笔批注。红笔不是为了嘲笑你，而是在说：“这里有个线索，请回头看一眼。”第2章的报错大多和“类型不合适”“名字没定义”“位置不存在”“key 找不到”或“缩进没对齐”有关。看到红字时，先不要重写整段代码，先缩小范围。

<figure align="center">
  <img src="../assets/ch02/ch02_error_clue_cards.png" alt="数据类型报错线索卡" width="82%" style="max-width:900px; display:block; margin:0 auto;" />
  <figcaption><strong>图2-20 数据类型报错线索卡</strong>：报错不是突然冒出来的怪事，它通常在提醒你：括号、key、索引、类型、路径或取值边界有一处没对齐。</figcaption>
</figure>

| 报错 | 常见原因 | 处理方式 |
| --- | --- | --- |
| `NameError` | 变量名没定义或拼错 | 检查变量名是否一致 |
| `TypeError` | 类型不匹配 | 用 `type()` 看数据类型 |
| `ValueError` | 值不适合转换 | 例如 `int("abc")` |
| `IndexError` | 列表或字符串索引越界 | 检查长度和索引范围 |
| `KeyError` | 字典里没有这个 key | 用 `in` 或 `get()` |
| `SyntaxError` | 引号、括号、冒号写错 | 看报错最后一行和定位行 |
| `IndentationError` | `if`、`for` 或函数后的缩进不一致 | 统一用 4 个空格检查代码块 |
| `AttributeError` | 这个类型没有你调用的方法 | 先用 `type()` 确认对象类型 |

初学者看到报错时，不要急着怀疑自己。先问三个问题：

1. 这个值是什么类型？
2. 我是不是用错了操作？
3. 我取的位置或 key 是否存在？
4. 条件、循环或函数后面的代码，缩进是否一致？

这三个问题能解决本章大多数错误。

---

## 2.26 本章核心概念复盘

| 概念 | 一句话解释 | 新手比喻 |
| --- | --- | --- |
| 常量 | Python 自带的固定值 | 固定角色 |
| 关键字 | Python 保留的语法词 | 路牌 |
| 变量 | 指向对象的名字 | 便签纸 |
| 布尔 | 真或假 | 红绿灯 |
| 条件语句 | 根据 `True`/`False` 选择一条路 | 分岔路口 |
| 数值 | 用于计算的数据 | 计分器 |
| 字符串 | 文本数据 | 一串字符珠子 |
| 切片 | 取出一段序列 | 切一段尺子 |
| 列表 | 有顺序的数据容器 | 一排抽屉 |
| 元组 | 创建后不修改的有序记录 | 封好的信息卡 |
| 集合 | 不重复的一组值 | 去重篮子 |
| 字典 | key 对应 value | 查表系统 |
| `for` 循环 | 依次处理一批项目 | 逐张检查卡片 |
| `while` 循环 | 条件成立时继续重复 | 倒计时器 |
| 函数 | 把可复用动作收起来 | 有名字的小工具 |

---

## 2.27 本章练习

下面这些练习可以按顺序做，也可以当作调试清单来用。每完成一题，都尽量运行一次代码、看一次输出。数据类型的手感不是靠默念概念长出来的，而是在“改一点、跑一下、看结果”里慢慢稳定下来。

### 练习 1：变量命名

把下面变量名改得更清楚：

```python
a = "小明"
b = 86
c = [78, 92, 88]
```

参考答案：

```python
student_name = "小明"
current_score = 86
practice_scores = [78, 92, 88]
```

### 练习 2：字符串切片

给定：

```python
word = "psychology"
```

请写出代码：

1. 取第一个字符。
2. 取最后一个字符。
3. 取前 5 个字符。
4. 判断 `"log"` 是否出现在字符串中。

参考代码：

```python
word = "psychology"

print(word[0])
print(word[-1])
print(word[:5])
print("log" in word)
```

### 练习 3：列表操作

给定：

```python
scores = [86, 92, 78]
```

请完成：

1. 添加一个新分数 `88`。
2. 删除第 2 个分数，也就是索引为 `1` 的元素。
3. 计算平均分。
4. 打印最高分。

参考代码：

```python
scores = [86, 92, 78]
scores.append(88)
del scores[1]
average_score = sum(scores) / len(scores)

print(scores)
print(average_score)
print(max(scores))
```

### 练习 4：字典操作

给定：

```python
student = {
    "name": "小明",
    "score": 86,
}
```

请完成：

1. 新增 `"city": "Beijing"`。
2. 把 `score` 改成 `90`。
3. 用 `get()` 查询 `"age"`，如果没有就返回 `"未知"`。

参考代码：

```python
student = {
    "name": "小明",
    "score": 86,
}

student["city"] = "Beijing"
student["score"] = 90
age = student.get("age", "未知")

print(student)
print(age)
```

### 练习 5：条件分支

给定分数 `score = 58`，请用 `if`、`elif`、`else` 输出三类结果：

- 90 分及以上：`优秀`
- 60 到 89 分：`通过`
- 60 分以下：`需要复习`

参考代码：

```python
score = 58

if score >= 90:
    print("优秀")
elif score >= 60:
    print("通过")
else:
    print("需要复习")
```

### 练习 6：用循环收集通过分数

给定：

```python
scores = [86, 55, 92, 48, 76]
```

请用 `for`、`if` 和 `append()` 建立一个 `passed_scores` 列表，只保留不低于 60 的分数；再打印这份新列表。

参考代码：

```python
scores = [86, 55, 92, 48, 76]
passed_scores = []

for score in scores:
    if score >= 60:
        passed_scores.append(score)

print(passed_scores)
```

### 练习 7：类型选择罗盘

运行：

```bash
python code/ch02/08_make_type_compass.py
```

然后打开：

```text
reports/ch02_type_compass.md
```

请任选 6 条真实学习数据，为每条数据选择合适类型，并写出一句理由。可以参考下面这种格式：

| 数据 | 推荐类型 | 理由 |
| --- | --- | --- |
| 学生姓名 | `str` | 它是一段文字，需要展示和保存 |
| 最近 7 次练习分数 | `list` | 它是一串有顺序的数据，可以计算平均分 |
| 是否通过本章测验 | `bool` | 它只有真或假两种结果 |

---

## 2.28 给自己的提醒：不要让类型变成背诵题

第2章最容易讲成“函数清单”。比如字符串有 `find()`、`replace()`、`split()`，列表有 `append()`、`del`，字典有查询、增删改。

这些都重要，但更重要的是让自己形成一个判断：

> 我面对的数据是什么形状？

自学时可以多问这种问题：

1. 如果要保存一个学生姓名，用什么类型？
2. 如果要保存一周 7 天的练习分数，用什么类型？
3. 如果要保存“学生姓名对应分数”，用什么类型？
4. 如果要判断是否通过考试，用什么类型？
5. 如果要把每一条成绩都检查一遍，用 `for` 还是 `while`？为什么？
6. 如果同一段判断逻辑会重复出现，应该把它收进什么？

你能回答这些问题，就已经不是在死背语法，而是在开始设计程序。

到这里，数据已经不再是一堆散落的词和数字。它们开始有形状：字符串像标签，列表像队列，元组像封好的信息卡，集合像去重篮子，字典像记录卡，布尔值像判断灯。条件语句负责选择，循环负责逐项处理，函数负责把动作收好。下一步很自然：把这些结构放进文件，让它们离开一次运行，变成可以保存、复查和交接的材料。

---

## 2.29 下一章预告：文件不是“在电脑里”，而是在路径里

下一章会进入文件读写与文件夹管理。

这会是初学者从“会写几行代码”走向“能处理真实资料”的关键一步。因为真实世界的数据不会自己排队走进程序，它们通常躺在某个文件夹里，名字可能很长，路径可能很乱，格式可能还不太听话。

下一章我们会学习：如何创建文件、读取文件、写入文件、管理文件夹、理解当前工作目录，并让 Python 开始真正处理你电脑里的资料。
