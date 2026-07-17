from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionReference:
    name: str
    chapters: tuple[int, ...]
    kind: str
    purpose: str
    inputs: str
    output: str
    changes: str
    example: str
    pitfall: str = ""

    @property
    def slug(self) -> str:
        stem = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
        return f"fn-{stem}"


def R(
    name: str,
    chapters: tuple[int, ...],
    kind: str,
    purpose: str,
    inputs: str,
    output: str,
    changes: str,
    example: str,
    pitfall: str = "",
) -> FunctionReference:
    return FunctionReference(name, chapters, kind, purpose, inputs, output, changes, example, pitfall)


FUNCTION_REFERENCES = [
    # 全书基础函数与类型转换
    R("print", tuple(range(11)), "内置函数", "把文字和变量显示在终端或运行窗口。", "零个或多个值；可用 sep、end 调整分隔和结尾。", "返回 None；可见结果是屏幕输出。", "不修改传入值。", 'print("分数：", 86)', "它负责显示，不等于把结果返回给程序。"),
    R("input", (1, 2, 4), "内置函数", "显示提示并等待用户键盘输入。", "可选的提示字符串。", "始终返回 str，即使用户输入的是数字。", "不修改外部对象，但会暂停程序等待输入。", 'name = input("请输入姓名：")', "参与计算前通常要用 int() 或 float() 转换。"),
    R("type", (2,), "内置函数", "查看一个值当前属于什么类型。", "任意一个 Python 值。", "返回类型对象，例如 str、int、list。", "不修改原值。", 'kind = type("86")'),
    R("len", (2, 5, 6, 8, 10), "内置函数", "统计字符串、列表、字典等对象包含多少项。", "一个支持长度统计的对象。", "返回非负整数 int。", "不修改原对象。", "count = len(scores)", "不能直接用于整数或浮点数。"),
    R("sum", (2, 6, 10), "内置函数", "把一组数值依次相加。", "数值序列；可选起始值。", "返回数值总和。", "不修改原序列。", "total = sum(scores)", "包含字符串或 None 时会出现 TypeError。"),
    R("min", (2, 6), "内置函数", "找出一组可比较值中的最小值。", "一个非空序列，或多个独立参数。", "返回其中最小的那个值。", "不修改原数据。", "lowest = min(scores)", "空列表没有最小值。"),
    R("max", (2, 6), "内置函数", "找出一组可比较值中的最大值。", "一个非空序列，或多个独立参数。", "返回其中最大的那个值。", "不修改原数据。", "highest = max(scores)", "不要把数字和字符串混在一起比较。"),
    R("round", (1, 2, 4, 6), "内置函数", "对数字取整或保留指定小数位。", "数字；可选的小数位数 ndigits。", "返回新的 int 或 float。", "不修改原数字。", "score = round(85.333, 1)", "它采用银行家舍入，2.5 不一定按传统方式变成 3。"),
    R("int", (2, 6, 7, 10), "类型转换", "把合适的字符串或数值转换成整数。", "整数、浮点数或符合格式的字符串。", "返回 int。", "不修改输入值。", 'age = int("18")', 'int("18.5") 会报错，要先转 float 或重新检查输入。'),
    R("float", (2, 6), "类型转换", "把合适的字符串或数值转换成浮点数。", "数字或数字格式字符串。", "返回 float。", "不修改输入值。", 'seconds = float("0.75")'),
    R("str", (2, 8, 10), "类型转换", "把值转换成适合显示或写文件的字符串。", "任意 Python 值。", "返回 str。", "不修改输入值。", 'label = str(86)'),
    R("bool", (2,), "类型转换", "把值按 Python 的真假规则转换成布尔值。", "任意 Python 值。", "返回 True 或 False。", "不修改输入值。", "ready = bool(records)", 'bool("False") 仍是 True，因为它是非空字符串。'),
    R("list", (2, 6, 10), "容器构造", "创建列表，或把可迭代对象收集成列表。", "可选的可迭代对象。", "返回可修改的 list。", "新建列表，不修改输入对象。", "values = list(rows)"),
    R("tuple", (2,), "容器构造", "创建元组，适合保存不打算修改的一组值。", "可选的可迭代对象。", "返回 tuple。", "新建元组。", 'point = tuple([3, 5])'),
    R("set", (2,), "容器构造", "创建不重复元素的集合。", "可选的可迭代对象。", "返回 set。", "新建集合并去除重复项。", "unique = set(tags)", "空集合必须写 set()，因为 {} 是空字典。"),
    R("dict", (2, 6), "容器构造", "创建 key 到 value 的映射。", "映射、键值对序列或关键字参数。", "返回 dict。", "新建字典。", 'student = dict(name="小明", score=86)'),
    R("range", (2, 7), "循环工具", "生成按规律变化的整数范围，常与 for 配合。", "stop，或 start、stop、step。", "返回 range 对象。", "不创建完整列表，也不修改外部数据。", "for i in range(1, 4):", "停止值不包含在结果中。"),
    R("enumerate", (2, 9, 10), "循环工具", "遍历时同时得到编号和当前值。", "可迭代对象；可选 start。", "返回逐项产生 (编号, 值) 的迭代器。", "不修改原对象。", "for index, value in enumerate(values, start=1):"),
    R("zip", (2, 9), "循环工具", "把多个序列按相同位置配对。", "两个或更多可迭代对象。", "返回逐项产生元组的迭代器。", "不修改原序列。", "for name, score in zip(names, scores):", "默认在最短序列结束时停止。"),
    R("sorted", (3, 6), "内置函数", "按顺序返回一个新的列表。", "可迭代对象；可选 key 和 reverse。", "返回新 list。", "不修改原对象。", "ordered = sorted(files)", "和 list.sort() 不同，它不会原地排序。"),
    R("help", (2,), "内置函数", "在控制台查看函数、类型或模块的帮助。", "函数或对象本身，不要提前加括号执行。", "返回 None；帮助文字显示在控制台。", "不修改查询对象。", "help(len)"),
    R("id", (2,), "内置函数", "查看对象在当前运行过程中的身份编号。", "任意 Python 对象。", "返回 int。", "不修改对象。", "identity = id(value)", "这个数字不适合保存为长期编号。"),
    R("chr / ord", (2,), "编码函数", "在 Unicode 编码值和单个字符之间转换。", "chr 接收整数；ord 接收长度为 1 的字符串。", "chr 返回 str；ord 返回 int。", "不修改输入。", 'letter = chr(65)\ncode = ord("A")'),

    # 字符串、列表与字典方法
    R("str.upper", (1, 2), "字符串方法", "返回全部转成大写字母的新字符串。", "无参数。", "返回新的 str。", "字符串不可变，原字符串不变。", 'upper_name = name.upper()'),
    R("str.strip", (1, 3, 4, 8), "字符串方法", "去掉字符串首尾的空白或指定字符。", "可选的字符集合。", "返回新的 str。", "原字符串不变。", "clean = line.strip()", "它不会删除句子中间的空格。"),
    R("str.lower", (2, 3, 8), "字符串方法", "返回转成小写字母的新字符串。", "无参数。", "返回新的 str。", "原字符串不变。", "suffix = path.suffix.lower()"),
    R("str.find", (2,), "字符串方法", "查找子字符串第一次出现的位置。", "要找的文字；可选起止位置。", "找到返回索引，找不到返回 -1。", "原字符串不变。", 'position = text.find("Python")'),
    R("str.replace", (2, 4), "字符串方法", "把指定片段替换成新片段。", "旧文字、新文字；可选替换次数。", "返回新的 str。", "原字符串不变。", 'clean = text.replace("Matlab", "Python")'),
    R("str.split", (2, 3), "字符串方法", "按分隔符把字符串切成多段。", "可选分隔符和最大切割次数。", "返回 list[str]。", "原字符串不变。", 'parts = line.split(",")'),
    R("str.join", (2, 9, 10), "字符串方法", "用指定分隔符连接多段字符串。", "只包含字符串的可迭代对象。", "返回新的 str。", "原序列不变。", 'text = "、".join(skills)', "序列中有整数时要先转成字符串。"),
    R("str.startswith", (2, 8), "字符串方法", "判断字符串是否以指定内容开头。", "前缀字符串或前缀元组。", "返回 bool。", "原字符串不变。", 'is_http = link.startswith("http")'),
    R("str.format", (2,), "字符串方法", "把参数填进字符串中的花括号位置。", "位置参数或关键字参数。", "返回新的 str。", "模板字符串不变。", 'text = "{} 分".format(score)', "新代码通常优先使用 f-string。"),
    R("bytes.decode", (8,), "字节方法", "按指定编码把网络字节转换成字符串。", "编码名称；可选错误处理策略。", "返回 str。", "原 bytes 不变。", 'html = data.decode("utf-8", errors="replace")'),
    R("list.append", (2, 3, 5, 8, 9, 10), "列表方法", "在列表末尾追加一个元素。", "一个任意类型的值。", "返回 None。", "原列表会改变。", "records.append(row)", "不要写 records = records.append(row)。"),
    R("list.extend", (2,), "列表方法", "把另一批元素逐项追加到列表末尾。", "一个可迭代对象。", "返回 None。", "原列表会改变。", "lines.extend(more_lines)"),
    R("dict.get", (2, 4, 5, 8), "字典方法", "安全读取 key，不存在时使用默认值。", "key；可选默认值。", "返回对应 value 或默认值。", "不修改字典。", 'score = row.get("score", 0)', "它不会把默认值自动写回字典。"),
    R("dict.items", (3,), "字典方法", "同时遍历字典的 key 和 value。", "无参数。", "返回键值对视图。", "不修改字典。", "for name, value in data.items():"),

    # 路径、文件、时间与标准库
    R("Path", (1, 3, 4, 6, 8, 9, 10), "路径构造", "把路径文字转换成 pathlib 路径对象。", "一个或多段路径信息。", "返回 Path；不会自动创建文件。", "不修改磁盘。", 'path = Path("data/report.csv")'),
    R("Path.cwd", (1, 3, 6), "路径方法", "获取程序当前工作目录。", "无参数。", "返回 Path。", "不修改磁盘。", "folder = Path.cwd()"),
    R("Path.resolve", (2, 3, 6, 8), "路径方法", "把路径整理成绝对路径。", "通常无参数。", "返回新的 Path。", "不修改磁盘。", "absolute = path.resolve()"),
    R("Path.exists", (2, 3, 6, 9, 10), "路径方法", "检查路径当前是否存在。", "无参数。", "返回 bool。", "不修改磁盘。", "if path.exists():"),
    R("Path.mkdir", (1, 3, 4, 6, 9, 10), "路径方法", "创建文件夹。", "可选 parents、exist_ok。", "返回 None。", "会修改磁盘。", "output.mkdir(parents=True, exist_ok=True)", "它只创建目录，不会创建文件。"),
    R("Path.read_text", (3, 4, 5), "路径方法", "一次读取整个文本文件。", "常用 encoding。", "返回 str。", "不修改文件。", 'text = path.read_text(encoding="utf-8")', "文件不存在会出现 FileNotFoundError。"),
    R("Path.write_text", (1, 3, 4, 8, 9, 10), "路径方法", "把字符串写进文本文件。", "文本；常用 encoding。", "返回写入的字符数 int。", "会创建或覆盖文件。", 'path.write_text(text, encoding="utf-8")', "父文件夹必须先存在。"),
    R("Path.open", (2, 3, 6, 8, 10), "路径方法", "以指定模式打开路径对应的文件。", "mode、encoding 等。", "返回文件对象。", "读取模式不改文件；写入模式会改磁盘。", 'with path.open("r", encoding="utf-8") as file:'),
    R("Path.rglob", (3,), "路径方法", "递归查找当前目录及子目录中的路径。", "通配模式，例如 * 或 *.py。", "返回可迭代路径对象。", "不修改磁盘。", 'for path in root.rglob("*.txt"):'),
    R("Path.is_file", (3,), "路径方法", "判断路径是否指向普通文件。", "无参数。", "返回 bool。", "不修改磁盘。", "if path.is_file():"),
    R("Path.stat", (3,), "路径方法", "读取文件大小、时间等状态信息。", "无参数。", "返回 stat_result。", "不修改磁盘。", "size = path.stat().st_size"),
    R("Path.unlink", (3,), "路径方法", "删除文件或符号链接。", "可选 missing_ok。", "返回 None。", "会删除磁盘内容。", "path.unlink()", "删除前必须打印并确认目标路径。"),
    R("Path.rmdir", (3,), "路径方法", "删除空文件夹。", "无参数。", "返回 None。", "会删除空目录。", "folder.rmdir()", "非空目录不能用它删除。"),
    R("open", (1, 3, 8, 10), "内置函数", "打开文件并建立文件对象。", "路径、模式；文本文件常写 encoding。", "返回文件对象。", "写入模式可能创建、清空或修改文件。", 'with open("data.txt", "r", encoding="utf-8") as file:', "优先配合 with 自动关闭。"),
    R("file.read", (3, 8), "文件方法", "读取文件剩余的全部内容或指定数量。", "可选字符数或字节数。", "文本模式返回 str，二进制模式返回 bytes。", "会推进文件读取位置。", "text = file.read()"),
    R("file.readline", (3,), "文件方法", "读取下一行。", "可选最大长度。", "返回 str；文件结束时返回空字符串。", "会推进读取位置。", "line = file.readline()"),
    R("file.readlines", (3,), "文件方法", "一次读取所有剩余行。", "可选大小提示。", "返回 list[str]。", "会推进读取位置。", "lines = file.readlines()"),
    R("file.write", (3,), "文件方法", "向文件写入一段字符串或字节。", "与打开模式匹配的 str 或 bytes。", "返回写入数量 int。", "会修改文件。", 'file.write("完成\n")'),
    R("file.writelines", (3,), "文件方法", "依次写入多段字符串。", "字符串可迭代对象。", "返回 None。", "会修改文件。", "file.writelines(lines)", "它不会自动补换行符。"),
    R("file.close", (3,), "文件方法", "释放文件对象占用的系统资源。", "无参数。", "返回 None。", "关闭后不能继续读写该对象。", "file.close()", "使用 with 时通常不用手动调用。"),
    R("os.getcwd", (3,), "标准库函数", "获取当前工作目录的字符串写法。", "无参数。", "返回 str。", "不修改磁盘。", "folder = os.getcwd()"),
    R("os.path.join", (3,), "标准库函数", "按当前操作系统规则拼接路径片段。", "两个或更多路径片段。", "返回路径字符串。", "不修改磁盘。", 'path = os.path.join("data", "scores.csv")'),
    R("shutil.copyfile", (3,), "标准库函数", "复制一个文件的内容。", "来源路径、目标路径。", "返回目标路径。", "会创建或覆盖目标文件。", "shutil.copyfile(source, target)", "目标文件夹必须先存在。"),
    R("shutil.move", (3,), "标准库函数", "移动文件或目录，也可用于改名。", "来源路径、目标路径。", "返回最终目标路径。", "会改变磁盘位置。", "shutil.move(source, target)"),
    R("shutil.rmtree", (3,), "标准库函数", "递归删除非空目录。", "目录路径。", "返回 None。", "会永久删除整个目录树。", "shutil.rmtree(folder)", "只在受控练习目录中使用，并先打印目标。"),
    R("time.sleep", (1, 8), "标准库函数", "让当前程序暂停指定秒数。", "秒数，可为小数。", "返回 None。", "不改数据，但会阻塞当前线程。", "time.sleep(0.5)"),
    R("time.perf_counter", (1, 4), "标准库函数", "读取适合测量时间间隔的高精度计时值。", "无参数。", "返回 float 秒数。", "不修改数据。", "start = time.perf_counter()", "这个数本身不是日期，要用两次结果相减。"),
    R("datetime.now / strftime", (1, 2), "日期时间", "取得当前时间，并按模板转换成文字。", "now() 通常无参数；strftime 接收格式字符串。", "now 返回 datetime；strftime 返回 str。", "不修改系统时间。", 'stamp = datetime.now().strftime("%Y-%m-%d")'),
    R("platform.platform", (1,), "标准库函数", "读取当前操作系统和平台摘要。", "通常无参数。", "返回 str。", "不修改系统。", "system_info = platform.platform()"),
    R("math.floor / math.ceil", (2,), "数学函数", "分别向下和向上取整。", "一个实数。", "返回整数结果。", "不修改输入。", "lower = math.floor(3.8)\nupper = math.ceil(3.2)"),

    # Tkinter 与面向对象
    R("tk.Tk", (4,), "Tkinter 构造器", "创建应用的主窗口。", "通常无参数。", "返回 Tk 窗口对象。", "创建 GUI 资源。", "root = tk.Tk()", "一个简单应用通常只创建一个主窗口。"),
    R("window.title / geometry", (4,), "Tkinter 方法", "设置窗口标题和初始尺寸。", "标题字符串；尺寸字符串如 520x360。", "返回 None。", "修改窗口配置。", 'root.title("学习卡片")\nroot.geometry("520x360")'),
    R("tk.Label", (4,), "Tkinter 构造器", "创建显示文字或图片的标签控件。", "父容器；text、font 等选项。", "返回 Label 对象。", "创建控件。", 'label = tk.Label(root, text="准备就绪")'),
    R("tk.Button", (4,), "Tkinter 构造器", "创建可点击按钮并绑定回调。", "父容器；text、command 等选项。", "返回 Button 对象。", "创建控件。", 'button = tk.Button(root, text="保存", command=save_card)', "command 要传函数名，不要写 save_card()。"),
    R("tk.Entry / tk.Text", (4,), "Tkinter 构造器", "创建单行或多行文本输入控件。", "父容器和尺寸、字体等选项。", "返回 Entry 或 Text 对象。", "创建可编辑控件。", "entry = tk.Entry(root)\nnotes = tk.Text(root, height=6)"),
    R("widget.pack / grid", (4,), "Tkinter 布局", "把控件安排到窗口中。", "间距、方向、行列等布局参数。", "返回 None。", "修改控件布局状态。", "label.pack(pady=8)", "同一个父容器中不要混用 pack 和 grid。"),
    R("widget.get", (4,), "Tkinter 方法", "读取输入控件当前内容。", "Entry 无参数；Text 常用起止位置。", "返回 str。", "不清空控件。", 'topic = entry.get().strip()'),
    R("widget.config", (4,), "Tkinter 方法", "修改已创建控件的文字、颜色或状态。", "要更新的关键字选项。", "返回 None。", "修改控件状态。", 'label.config(text="保存成功")'),
    R("window.bind", (4,), "Tkinter 方法", "把键盘或鼠标事件绑定到回调函数。", "事件描述字符串、回调函数。", "返回绑定标识字符串。", "修改事件绑定。", 'root.bind("<Key>", on_key)', "事件回调通常要接收 event 参数。"),
    R("window.mainloop", (4,), "Tkinter 方法", "启动事件循环，让窗口持续响应用户操作。", "无参数。", "通常直到窗口关闭才返回。", "进入 GUI 循环。", "root.mainloop()", "它通常放在窗口构建完成后的最后一行。"),
    R("messagebox.showinfo", (4,), "Tkinter 对话框", "弹出信息提示框。", "标题、正文。", "返回用户确认结果字符串。", "显示模态对话框。", 'messagebox.showinfo("完成", "卡片已保存")'),
    R("@dataclass", (5,), "类工具", "自动生成初始化、显示和比较等常见样板方法。", "装饰一个主要保存数据的类。", "返回加工后的类。", "改变类定义，不改变实例数据。", "@dataclass\nclass Trial:\n    score: int"),
    R("dataclasses.field", (5,), "类工具", "为数据类字段配置默认工厂等规则。", "default、default_factory 等。", "返回字段描述对象。", "影响实例字段初始化。", "cards: list = field(default_factory=list)", "可变默认值应使用 default_factory。"),
    R("ClassName(...) 构造对象", (5,), "对象构造", "根据类定义创建一个独立对象。", "对应 __init__ 或数据类字段的参数。", "返回类的实例。", "创建新对象。", 'card = LearningCard("循环", "重复处理")'),
    R("object.method(...) 方法调用", (5,), "对象方法", "让某个对象使用自己的数据完成动作。", "self 由 Python 自动传入，其余参数由调用者提供。", "由方法中的 return 决定；没有 return 时为 None。", "可能读取或修改对象属性。", "deck.add(card)", "调用时不要手动传 self。"),

    # 数据分析与绘图
    R("csv.DictReader", (6, 8, 10), "CSV 读取", "按表头把 CSV 每行读成字典。", "已打开的文本文件；可选字段和方言。", "返回可迭代 DictReader。", "会推进文件读取位置。", "reader = csv.DictReader(file)"),
    R("csv.DictWriter", (2, 8, 10), "CSV 写入", "按字段名把字典写入 CSV。", "文件对象、fieldnames 等。", "返回 DictWriter。", "后续写入会修改文件。", "writer = csv.DictWriter(file, fieldnames=fields)"),
    R("writer.writeheader / writerows", (2, 8, 10), "CSV 写入", "写入表头或多行字典记录。", "writeheader 无参数；writerows 接收字典序列。", "返回 None。", "修改 CSV 文件。", "writer.writeheader()\nwriter.writerows(rows)"),
    R("pd.read_csv", (6,), "pandas 函数", "把 CSV 读成表格型 DataFrame。", "文件路径；可选编码、列类型等。", "返回 DataFrame。", "不修改源文件。", 'df = pd.read_csv("learning_records.csv")'),
    R("DataFrame.groupby", (6,), "pandas 方法", "按一列或多列把数据分组。", "列名；可选排序、缺失值规则。", "返回 GroupBy 对象。", "不修改原 DataFrame。", 'grouped = df.groupby("topic")'),
    R("GroupBy.mean", (6,), "pandas 方法", "计算每组数值列的平均值。", "通常无参数；可选择 numeric_only。", "返回 Series 或 DataFrame。", "不修改原数据。", "averages = grouped.mean(numeric_only=True)"),
    R("statistics.mean / median", (6,), "统计函数", "计算算术平均数或中位数。", "非空数值序列。", "返回数值。", "不修改序列。", "average = mean(values)\nmidpoint = median(values)"),
    R("ImageFont.truetype", (6, 9), "Pillow 字体", "从字体文件加载指定字号的字体。", "字体路径、字号。", "返回 FreeTypeFont。", "读取字体文件。", "font = ImageFont.truetype(font_path, 28)", "字体文件不存在会报 OSError。"),
    R("ImageFont.load_default", (6, 9), "Pillow 字体", "加载 Pillow 自带的默认字体作为后备。", "通常无参数。", "返回字体对象。", "不修改图片。", "font = ImageFont.load_default()"),

    # PyGame
    R("pygame.init", (7,), "PyGame 初始化", "初始化常用的 PyGame 子模块。", "无参数。", "返回成功数和失败数的元组。", "初始化音频、显示等资源。", "pygame.init()"),
    R("pygame.display.set_mode", (7,), "PyGame 显示", "创建游戏窗口和绘图表面。", "尺寸元组；可选 flags。", "返回 Surface。", "创建显示资源。", "screen = pygame.display.set_mode((800, 600))"),
    R("pygame.display.set_caption", (7,), "PyGame 显示", "设置窗口标题。", "标题字符串。", "返回 None。", "修改窗口标题。", 'pygame.display.set_caption("接球游戏")'),
    R("pygame.event.get", (7,), "PyGame 事件", "取出当前等待处理的事件。", "通常无参数。", "返回 Event 列表。", "会清空已取出的事件队列。", "for event in pygame.event.get():"),
    R("pygame.key.get_pressed", (7,), "PyGame 输入", "读取当前每个键是否按下。", "无参数。", "返回可按键索引查询的布尔序列。", "读取输入状态。", "keys = pygame.key.get_pressed()"),
    R("pygame.draw.rect / circle", (7,), "PyGame 绘图", "在 Surface 上画矩形或圆。", "目标 Surface、颜色、位置尺寸。", "返回包围绘图区域的 Rect。", "直接修改目标 Surface 的像素。", "pygame.draw.rect(screen, color, player_rect)"),
    R("Surface.fill / blit", (7,), "PyGame 绘图", "填充画面，或把另一张 Surface 贴到目标上。", "fill 接收颜色；blit 接收来源和位置。", "返回 Rect。", "直接修改目标 Surface。", "screen.fill(background)\nscreen.blit(text_surface, (20, 20))"),
    R("pygame.font.SysFont / Font", (7,), "PyGame 字体", "创建用于渲染文字的字体对象。", "字体名或字体文件、字号。", "返回 Font。", "加载字体资源。", "font = pygame.font.SysFont(None, 32)"),
    R("Font.render", (7,), "PyGame 字体", "把文字渲染成可绘制的 Surface。", "文字、抗锯齿开关、颜色。", "返回新的 Surface。", "不修改字体对象。", 'label = font.render("得分：10", True, white)'),
    R("pygame.time.Clock / tick", (7,), "PyGame 计时", "创建帧率时钟，并限制循环运行速度。", "Clock 无参数；tick 接收目标 FPS。", "Clock 返回时钟；tick 返回距上次调用的毫秒数。", "tick 会让循环在必要时短暂停顿。", "clock = pygame.time.Clock()\nclock.tick(60)"),
    R("random.randint", (7,), "随机函数", "生成包含两端的随机整数。", "最小值、最大值。", "返回 int。", "不修改参数。", "x = random.randint(0, width)"),
    R("pygame.display.flip", (7,), "PyGame 显示", "把刚绘制的整张画面更新到窗口。", "无参数。", "返回 None。", "刷新显示。", "pygame.display.flip()"),
    R("pygame.quit", (7,), "PyGame 清理", "关闭已初始化的 PyGame 模块。", "无参数。", "返回 None。", "释放游戏资源。", "pygame.quit()"),

    # 网络请求与 HTML
    R("urllib.request.Request", (8,), "网络请求", "创建带 URL、请求头等信息的请求对象。", "URL；可选 headers、method、data。", "返回 Request。", "不发送网络请求。", "request = Request(url, headers={\"User-Agent\": agent})"),
    R("urllib.request.urlopen", (8,), "网络请求", "发送请求并打开服务器响应。", "URL 或 Request；可选 timeout。", "返回响应对象。", "会进行网络访问。", "with urlopen(request, timeout=10) as response:", "必须处理超时、网络错误和 HTTP 错误。"),
    R("response.read", (8,), "网络响应", "读取响应正文。", "可选最大字节数。", "返回 bytes。", "会推进响应读取位置。", "data = response.read()"),
    R("response.headers.get", (8,), "网络响应", "安全读取某个响应头。", "响应头名称；可选默认值。", "返回 str 或默认值。", "不修改响应头。", 'content_type = response.headers.get("Content-Type", "")'),
    R("HTMLParser.feed", (8,), "HTML 解析", "把一段 HTML 文本交给解析器处理。", "HTML 字符串。", "返回 None。", "会更新解析器内部状态并触发回调。", "parser.feed(html)"),
    R("urlparse", (8,), "URL 解析", "把 URL 拆成协议、域名、路径、查询等部分。", "URL 字符串。", "返回 ParseResult。", "不修改原字符串。", "parsed = urlparse(link)"),
    R("ssl.create_default_context", (8,), "HTTPS 工具", "创建采用系统默认安全设置的 TLS 上下文。", "通常无参数。", "返回 SSLContext。", "读取系统证书配置。", "context = ssl.create_default_context()"),
    R("certifi.where", (8,), "证书工具", "取得 certifi 证书包文件路径。", "无参数。", "返回路径字符串。", "不修改系统。", "cafile = certifi.where()"),
    R("random.uniform", (8,), "随机函数", "生成两个端点之间的随机浮点数。", "下限、上限。", "返回 float。", "不修改参数。", "delay = random.uniform(1.0, 2.0)"),

    # Pillow 图像处理
    R("Image.open", (9,), "Pillow 图像", "打开图像文件并创建图像对象。", "文件路径或文件对象。", "返回 Image。", "按需读取文件，不修改原图。", 'image = Image.open("photo.jpg")', "推荐配合 with，或及时 close。"),
    R("Image.new", (2, 9), "Pillow 图像", "创建指定模式、尺寸和背景的新图像。", "模式、尺寸、可选颜色。", "返回 Image。", "创建内存中的新图。", 'canvas = Image.new("RGB", (800, 600), "white")'),
    R("Image.convert", (9,), "Pillow 图像", "转换颜色模式，例如 RGB 或 L。", "目标模式字符串。", "返回新的 Image。", "原图对象不变。", 'gray = image.convert("L")'),
    R("Image.resize", (9,), "Pillow 图像", "把图像缩放到精确尺寸。", "目标尺寸；可选重采样算法。", "返回新的 Image。", "原图不变。", "small = image.resize((400, 300))", "强制尺寸可能拉伸变形。"),
    R("Image.crop", (9,), "Pillow 图像", "按矩形边界裁剪图像。", "(left, top, right, bottom)。", "返回新的 Image。", "原图不变。", "part = image.crop((0, 0, 300, 200))"),
    R("Image.filter", (9,), "Pillow 图像", "对图像应用滤镜。", "一个 ImageFilter 滤镜对象。", "返回新的 Image。", "原图不变。", "sharp = image.filter(ImageFilter.UnsharpMask())"),
    R("Image.save", (2, 6, 9), "Pillow 图像", "把当前图像编码并写入文件。", "目标路径；可选 format、quality 等。", "返回 None。", "创建或覆盖磁盘文件。", 'image.save("output.png")'),
    R("Image.paste", (9,), "Pillow 图像", "把另一张图或颜色粘贴到目标图指定区域。", "来源图、位置；可选遮罩。", "返回 None。", "直接修改目标 Image。", "canvas.paste(photo, (20, 20))"),
    R("ImageOps.exif_transpose", (9,), "Pillow 图像", "依据 EXIF 方向信息纠正照片朝向。", "Image。", "返回方向正确的 Image。", "通常返回新对象。", "image = ImageOps.exif_transpose(image)"),
    R("ImageOps.fit / contain", (9,), "Pillow 图像", "按比例适配目标尺寸；fit 会裁剪，contain 会完整保留。", "Image、目标尺寸。", "返回新的 Image。", "原图不变。", "thumb = ImageOps.contain(image, (320, 240))"),
    R("ImageOps.grayscale", (9,), "Pillow 图像", "把图像转换为灰度。", "Image。", "返回灰度 Image。", "原图不变。", "gray = ImageOps.grayscale(image)"),
    R("ImageEnhance.Contrast / Color", (9,), "Pillow 增强", "创建对比度或色彩增强器。", "Image。", "返回增强器对象。", "不立即修改图像。", "enhancer = ImageEnhance.Contrast(image)"),
    R("enhancer.enhance", (9,), "Pillow 增强", "按系数生成增强或减弱后的图像。", "浮点系数，1.0 表示原效果。", "返回新的 Image。", "原图不变。", "stronger = enhancer.enhance(1.3)"),
    R("ImageFilter.UnsharpMask", (9,), "Pillow 滤镜", "创建反锐化遮罩滤镜配置。", "radius、percent、threshold 等。", "返回滤镜对象。", "不修改图像。", "filter_ = ImageFilter.UnsharpMask(radius=2, percent=130)"),
    R("ImageDraw.Draw", (2, 6, 9), "Pillow 绘图", "为现有图像创建绘图上下文。", "目标 Image。", "返回 ImageDraw 对象。", "后续绘图会直接修改目标图像。", "draw = ImageDraw.Draw(canvas)"),
    R("draw.text / rounded_rectangle", (2, 6, 9), "Pillow 绘图", "在图像上写文字或画圆角矩形。", "位置、内容或边界、颜色、字体等。", "通常返回 None。", "直接修改目标图像。", 'draw.text((20, 20), "报告", font=font, fill="black")'),

    # Office 自动化
    R("openpyxl.Workbook", (10,), "Excel 构造器", "创建新的 Excel 工作簿。", "通常无参数。", "返回 Workbook。", "创建内存中的工作簿。", "wb = Workbook()"),
    R("openpyxl.load_workbook", (10,), "Excel 读取", "打开已有的 xlsx 工作簿。", "文件路径；可选 data_only、read_only。", "返回 Workbook。", "读取文件；保存前通常不改磁盘。", 'wb = load_workbook("report.xlsx")'),
    R("worksheet.append", (10,), "Excel 方法", "在工作表末尾追加一行。", "列表、元组或字典形式的一行数据。", "返回 None。", "修改内存中的工作表。", "ws.append([name, score])"),
    R("worksheet.iter_rows", (10,), "Excel 方法", "按行遍历单元格。", "可选范围、values_only。", "返回行迭代器。", "不修改工作表。", "for row in ws.iter_rows(values_only=True):"),
    R("workbook.save", (10,), "Excel 方法", "把工作簿写成 xlsx 文件。", "目标文件路径。", "返回 None。", "创建或覆盖 Excel 文件。", 'wb.save("final_report.xlsx")'),
    R("openpyxl.styles.Font / PatternFill", (10,), "Excel 样式", "创建字体或填充样式对象。", "颜色、粗体、填充模式等关键字参数。", "返回样式对象。", "不直接改工作表，赋给单元格后生效。", 'cell.font = Font(bold=True)'),
    R("docx.Document", (10,), "Word 构造器", "创建新 Word 文档或打开已有文档。", "可选 docx 文件路径。", "返回 Document。", "创建或读取文档对象。", "doc = Document()"),
    R("Document.add_heading / add_paragraph", (10,), "Word 方法", "向文档末尾添加标题或段落。", "文字；标题还接收 level。", "返回段落对象。", "修改内存中的文档。", 'doc.add_heading("学习报告", level=1)\ndoc.add_paragraph(summary)'),
    R("Document.add_table", (10,), "Word 方法", "向文档添加表格。", "行数、列数；可选样式。", "返回 Table。", "修改内存中的文档。", "table = doc.add_table(rows=1, cols=3)"),
    R("Table.add_row", (10,), "Word 方法", "在 Word 表格末尾增加一行。", "无参数。", "返回新 Row。", "修改表格。", "row = table.add_row()"),
    R("Document.save", (10,), "Word 方法", "把文档写成 docx 文件。", "目标路径。", "返回 None。", "创建或覆盖 Word 文件。", 'doc.save("final_report.docx")'),
    R("pptx.Presentation", (10,), "PowerPoint 构造器", "创建演示文稿或打开已有 pptx。", "可选 pptx 路径。", "返回 Presentation。", "创建或读取演示文稿对象。", "prs = Presentation()"),
    R("slides.add_slide", (10,), "PowerPoint 方法", "按指定版式添加一页幻灯片。", "SlideLayout。", "返回 Slide。", "修改演示文稿。", "slide = prs.slides.add_slide(prs.slide_layouts[1])"),
    R("shapes.add_textbox", (10,), "PowerPoint 方法", "在幻灯片指定位置创建文本框。", "left、top、width、height。", "返回 Shape。", "修改幻灯片。", "box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(6), Inches(1))"),
    R("Presentation.save", (10,), "PowerPoint 方法", "把演示文稿写成 pptx 文件。", "目标路径。", "返回 None。", "创建或覆盖 PowerPoint 文件。", 'prs.save("final_slides.pptx")'),
    R("Inches / Pt", (10,), "Office 尺寸", "把英寸或磅转换成 Office 文件使用的长度单位。", "数字。", "返回整数长度值。", "不修改文档。", "left = Inches(1)\nsize = Pt(18)"),
]


# 学员脚本中会直接遇到的补充调用。它们单独列出，避免把“文件怎么走、
# 对象怎么变、结果去哪儿”藏在综合示例里。
FUNCTION_REFERENCES.extend(
    [
        R("Path.iterdir / glob", (1, 3, 9), "路径方法", "列出目录中的内容，或按模式寻找文件。", "iterdir 无参数；glob 接收如 '*.png' 的模式。", "返回可迭代对象，每项都是 Path。", "只读取目录，不修改文件。", 'for path in folder.glob("*.png"):\n    print(path.name)', "结果不会自动排序；需要稳定顺序时再用 sorted。"),
        R("Path.relative_to / as_posix", (2, 3, 4, 5, 6), "路径方法", "把完整路径改写成相对路径，并用正斜杠表示。", "relative_to 接收基准目录；as_posix 无参数。", "relative_to 返回 Path；as_posix 返回 str。", "不修改原路径和文件。", 'relative = file_path.relative_to(project_root)\ntext = relative.as_posix()', "relative_to 只接受确实包含该路径的基准目录，否则会报 ValueError。"),
        R("textwrap.dedent", (2, 3), "文本工具", "统一去掉多行字符串公共的左侧缩进。", "一个多行字符串。", "返回清理后的新字符串。", "不修改原字符串。", 'template = dedent("""\n    姓名,分数\n    小林,86\n""").strip()'),
        R("json.dumps / loads", (2, 3, 4, 5), "JSON 转换", "在 Python 对象与 JSON 文本之间转换。", "dumps 接收 Python 对象；loads 接收 JSON 字符串。", "dumps 返回 str；loads 返回字典、列表等 Python 对象。", "不自动读写文件。", 'text = json.dumps(data, ensure_ascii=False)\ndata = json.loads(text)', "文件读写要另用 read_text、write_text 或 open；load、dump 与 loads、dumps 也不要混淆。"),
        R("shutil.copy2", (2, 3), "文件工具", "复制文件，同时尽量保留修改时间等元数据。", "源文件路径和目标路径。", "返回目标路径字符串。", "会在磁盘创建或覆盖目标文件。", 'copied_to = shutil.copy2(source, destination)'),
        R("collections.Counter", (3,), "计数工具", "统计序列中每个值出现了多少次。", "任意可迭代对象或映射。", "返回类似字典的 Counter 对象。", "不修改输入序列。", 'counts = Counter(path.suffix for path in files)'),
        R("FileNotFoundError / ValueError", (3, 6, 8, 9), "异常类型", "表示文件不存在，或值的内容不符合要求。", "作为异常创建时可传错误说明；也常写在 except 后。", "创建异常对象；被 raise 时会中断当前流程。", "不会自动修复文件或数值。", 'except FileNotFoundError:\n    print("请检查文件路径")', "捕获异常后要给出可执行的解决办法，不要只写 except: pass。"),
        R("hashlib.sha256 / update / hexdigest", (3,), "摘要工具", "为文件内容计算可复查的 SHA-256 摘要。", "sha256 可接收初始 bytes；update 继续接收 bytes。", "sha256 返回哈希对象；hexdigest 返回十六进制字符串。", "只计算摘要，不修改文件。", 'digest = hashlib.sha256()\ndigest.update(data)\ncode = digest.hexdigest()'),
        R("iter", (3,), "内置函数", "取得对象的迭代器，供 next 或循环逐项读取。", "一个可迭代对象。", "返回迭代器。", "通常不修改原对象，但迭代器会记录读取位置。", 'iterator = iter(records)'),
        R("os.chdir", (3,), "目录操作", "修改当前进程的工作目录。", "目标目录路径。", "返回 None。", "会影响后续所有相对路径的解释方式。", 'os.chdir(project_root)', "对初学者更推荐用明确的 Path 拼接路径，减少全局工作目录变化。"),
        R("runpy.run_path", (3,), "脚本执行", "像运行脚本一样执行指定的 Python 文件。", "脚本路径；可选 run_name。", "返回脚本结束时的全局变量字典。", "会执行脚本中的读写和打印等副作用。", 'result = runpy.run_path("code/ch03/check_files.py")'),
        R("tk.Frame / ttk.Treeview", (4, 5), "Tkinter 控件", "创建分组容器或表格树控件。", "父容器，以及列、标题、尺寸等选项。", "返回控件对象。", "创建内存中的控件；布局后才显示。", 'frame = tk.Frame(root)\ntree = ttk.Treeview(frame, columns=("name", "score"))'),
        R("Treeview.column / heading / insert", (4, 5), "Tkinter 方法", "设置表格列、表头，并向表格加入一行。", "列标识和配置；insert 还接收父项、位置和值。", "column、heading 通常返回配置或 None；insert 返回新项目标识。", "修改 Treeview 的结构或内容。", 'tree.heading("name", text="姓名")\ntree.insert("", "end", values=("小林", 86))'),
        R("dict.keys", (6, 10), "字典方法", "取得字典当前所有键的动态视图。", "无参数。", "返回 dict_keys 视图。", "不修改字典；字典后续变化会反映在视图中。", 'columns = list(record.keys())'),
        R("map", (6,), "内置函数", "把同一个函数依次应用到每个元素。", "函数和一个或多个可迭代对象。", "返回惰性的 map 迭代器。", "不修改输入序列。", 'numbers = list(map(float, text_values))', "初学阶段列表推导式通常更直观；map 的结果需要迭代或转成 list 才能看到。"),
        R("ImageDraw.line / rectangle / ellipse / polygon / pieslice", (2, 6, 8, 9), "Pillow 绘图", "在图片上绘制线、矩形、椭圆、多边形或扇形。", "坐标或边界、填充色、描边色和宽度等。", "通常返回 None。", "直接修改 Draw 所关联的图片。", 'draw.rectangle((20, 20, 220, 100), fill="white", outline="navy")'),
        R("ImageDraw.textbbox", (2, 6), "Pillow 绘图", "在真正画字前测量文字将占据的边界。", "起点、文字；可选字体等。", "返回 (left, top, right, bottom)。", "只测量，不修改图片。", 'left, top, right, bottom = draw.textbbox((0, 0), title, font=font)'),
        R("pygame.key.name", (7,), "PyGame 输入", "把按键编号转换为便于阅读的按键名称。", "一个按键编号。", "返回字符串。", "不改变键盘状态。", 'key_name = pygame.key.name(event.key)'),
        R("csv.writer / writer.writerow", (8,), "CSV 写入", "创建按序列写入 CSV 的工具，并写入单行。", "writer 接收已打开文件；writerow 接收一行序列。", "writer 返回写入器；writerow 返回底层写入结果。", "writerow 会修改已打开的 CSV 文件。", 'writer = csv.writer(file)\nwriter.writerow(["标题", "链接"])'),
        R("str.endswith", (8,), "字符串方法", "判断字符串是否以指定后缀结束。", "一个后缀，或多个后缀组成的元组。", "返回 bool。", "不修改原字符串。", 'is_page = url.lower().endswith((".html", ".htm"))'),
        R("str.splitlines", (3,), "字符串方法", "按不同系统的换行符把多行文字拆成多行。", "可选 keepends，决定是否保留换行符。", "返回字符串列表。", "不修改原字符串。", 'lines = path.read_text(encoding="utf-8").splitlines()'),
        R("super", (8,), "面向对象工具", "取得父类方法的代理，常用于子类初始化时复用父类逻辑。", "Python 3 的类方法中通常不传参数。", "返回 super 代理对象。", "调用其方法时可能修改当前对象。", 'super().__init__()'),
        R("getattr", (9,), "内置函数", "按字符串形式的属性名读取对象属性。", "对象、属性名；可选默认值。", "返回属性值或默认值。", "只读取属性。", 'method = getattr(image, method_name, None)', "属性名固定时直接写 image.size 更清楚；只有名称来自变量时才需要 getattr。"),
    ]
)


def references_for_chapter(chapter: int) -> list[FunctionReference]:
    return [item for item in FUNCTION_REFERENCES if chapter in item.chapters]


def validate_references() -> None:
    slugs = [item.slug for item in FUNCTION_REFERENCES]
    if len(slugs) != len(set(slugs)):
        duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
        raise ValueError(f"Duplicate function reference slugs: {duplicates}")
    for item in FUNCTION_REFERENCES:
        if not item.chapters:
            raise ValueError(f"Function reference has no chapter: {item.name}")
        if any(chapter < 0 or chapter > 10 for chapter in item.chapters):
            raise ValueError(f"Invalid chapter for {item.name}: {item.chapters}")
        if not all((item.purpose, item.inputs, item.output, item.changes, item.example)):
            raise ValueError(f"Incomplete function reference: {item.name}")


validate_references()
