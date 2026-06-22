# 第 9 章：Python 图像处理

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
  <img src="../assets/ch09/ch09_cover.png" alt="第9章封面" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-1 本章封面</strong>：图片不是一整块魔法布，它是像素组成的矩阵。理解像素，图像处理就从玄学变成手工活。</figcaption>
</figure>

> 本章一句话：图片不是一整块魔法布，它是像素组成的矩阵。理解像素，图像处理就从玄学变成手工活。

第9章继续推进“科研卡片工厂”的视觉能力。前面几章让 Python 能整理文字、表格和报告；这一章开始处理图片。对教程、心理学实验和科研展示来说，图片不是装饰边角料，而是信息本身：刺激材料要统一尺寸，报告配图要清楚，结果图要能复查。

这一章的目标也很朴素：让你知道一张图片在程序眼里是什么，怎么安全地改它，怎么把处理结果留下来。

---

## 9.0 本章学习目标

学完本章，你应该能够：

1. 用自己的话解释本章核心概念。
2. 运行本章配套脚本，看到明确输出。
3. 把概念和“科研卡片工厂”的连续项目联系起来。
4. 识别本章最常见的新手错误。
5. 完成本章小项目：**学习卡片配图处理器**。

---

## 9.1 开场故事：先有画面，再有术语

图片不是一整块魔法布，它是像素组成的矩阵。理解像素，图像处理就从玄学变成手工活。 这句话不是为了热闹，而是为了把本章的知识放进真实使用场景。初学者最怕一上来就被术语包围，像走进一个所有门牌都用缩写写成的楼层。我们先从画面进入，再慢慢把画面翻译成代码。

<figure align="center">
  <img src="../assets/ch09/ch09_niepce_photo_story.png" alt="Niépce 早期摄影作品" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-2 Niépce 的早期摄影作品</strong>：图像处理的前提是“图像能被记录”；今天我们用 Python 处理像素，其实是在接续摄影史里的记录与再加工。</figcaption>
</figure>

早期摄影让光影第一次稳定地留在介质上。到了数字图像时代，照片不再只是纸面或底片，而是一张可以被程序读取、缩放、裁剪、转灰度、统计颜色的像素表。你可以把一张图片想成一座由很多小格子搭成的城市：每个格子有位置，也有颜色。

<figure align="center">
  <img src="../assets/ch09/ch09_first_digital_scan_story.png" alt="第一张数字扫描图像" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-3 早期数字扫描图像</strong>：数字图像的关键一步，是把连续画面拆成一个个可以存储、计算和修改的像素。</figcaption>
</figure>

1957 年，Russell Kirsch 团队扫描出一张婴儿照片，它常被用来讲早期数字图像史。照片本身不大，但意义很大：一旦图像被拆成像素，程序就能对它做计算。灰度、裁剪、锐化、压缩、识别，全都从“图像可以被数字表示”开始。

<figure align="center">
  <img src="../assets/ch09/ch09_edwin_land_color_story.png" alt="Edwin Land照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-4 Edwin Land照片</strong>：颜色不是简单地“存在于图片里”，它还和光照、背景、人眼判断有关。理解这一点，才能更谨慎地处理 RGB、灰度和增强。</figcaption>
</figure>

Edwin Land 的故事适合放在图像处理章里。他不仅和即时成像有关，也研究过人如何在复杂光照下判断颜色。对 Python 初学者来说，这能带来一个重要提醒：图像处理不是把滑块拉到“好看”为止，而是要知道颜色、亮度和对比度会怎样影响理解。

<figure align="center">
  <img src="../assets/ch09/ch09_story_scene.png" alt="故事场景图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-5 故事场景</strong>：图像像彩色方格纸：坐标决定位置，RGB 决定颜色，滤镜就是批量修改格子的规则。</figcaption>
</figure>

这个画面对应本章的核心比喻：图像像彩色方格纸：坐标决定位置，RGB 决定颜色，滤镜就是批量修改格子的规则。 如果你能先记住这个比喻，后面的概念就不再是干巴巴的定义。

---

## 9.2 知识路线

<figure align="center">
  <img src="../assets/ch09/ch09_roadmap.png" alt="知识路线图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-6 知识路线</strong>：先建立直觉，再运行代码，最后完成一个可展示的小项目。</figcaption>
</figure>

本章路线如下：

| 顺序 | 主题 | 你要完成的动作 |
| --- | --- | --- |
| 1 | 像素和坐标 | 把一张图看成有行列位置的小格子 |
| 2 | RGB/RGBA | 读懂颜色通道，知道透明度从哪里来 |
| 3 | Pillow 打开保存 | 用 Python 打开图片、查看属性、保存副本 |
| 4 | 缩放裁剪 | 改变尺寸和视野，观察信息有没有丢失 |
| 5 | 滤镜和灰度 | 生成灰度、锐化和增强结果，比较视觉差异 |
| 6 | 批量处理 | 让一组图片按同一规则进入卡片工厂 |
| 7 | 视觉感知与图像解释 | 判断处理是否帮助理解，还是改变了判断 |

---

## 9.3 核心概念：从人话到术语

<figure align="center">
  <img src="../assets/ch09/ch09_core_metaphor.png" alt="核心比喻图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-7 核心比喻</strong>：用一个稳定画面记住本章最重要的概念关系。</figcaption>
</figure>

先用人话说：图像像彩色方格纸：坐标决定位置，RGB 决定颜色，滤镜就是批量修改格子的规则。

<figure align="center">
  <img src="../assets/ch09/ch09_real_photo_source.png" alt="Fronalpstock 风景照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-8 本章真实处理素材</strong>：用真实风景照片做输入，比只看抽象示意图更容易理解缩放、灰度和裁剪的效果。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch09/ch09_pillars_science_image_story.png" alt="NASA 创生之柱科学图像" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-9 科学图像与视觉表达</strong>：科学图像常常需要增强、裁剪和配色；处理得好，是让信息更清楚，不是让事实变花哨。</figcaption>
</figure>

NASA 的“创生之柱”常被用来说明科学图像的表达力量。很多科学图片并不是相机随手一拍就完事，而是要经过校正、合成、增强和说明。这里有一个重要边界：图像处理可以帮你看清结构，但不能为了好看而误导事实。学习卡片和报告配图也是一样：清楚第一，漂亮第二；漂亮必须服务于理解。

再用术语说，本章要掌握这些内容：

- **像素和坐标**：每个像素都有位置，裁剪、绘制和取色都从坐标开始。
- **RGB/RGBA**：颜色由通道组成，透明度决定图片能不能自然叠到其他背景上。
- **Pillow 打开保存**：先保留原图，再生成副本；不要让一次实验覆盖证据。
- **缩放裁剪**：缩放改变尺寸，裁剪改变视野；二者都会影响别人看到什么。
- **滤镜和灰度**：滤镜不是越重越好，灰度能帮你检查明暗结构和信息层次。
- **批量处理**：同一批素材要用一致规则处理，卡片和报告才不会忽大忽小。
- **视觉感知与图像解释**：程序改的是像素，人理解的是场景；处理前后都要问“会不会误导判断”。

术语不是用来吓人的，它只是为了让大家交流时不用每次都讲一长串故事。你先用故事建立直觉，再用术语压缩表达，这样学得稳。

---

## 9.4 最小可运行示例

<figure align="center">
  <img src="../assets/ch09/ch09_minimal_demo.png" alt="最小示例图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-10 最小示例</strong>：先跑通最小代码，再逐步增加功能，学习会稳很多。</figcaption>
</figure>

本章第一件事不是背参数，而是运行一个最小例子。打开终端，进入本章目录后运行：

```bash
python code/ch09/01_create_demo_image.py
```

如果你能看到输出，说明这一章的入口已经打通。后面所有复杂功能，都是在这个入口上慢慢加能力。

<figure align="center">
  <img src="../assets/ch09/ch09_before_after_result.png" alt="真实照片处理前后对比" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-11 真实照片处理结果</strong>：`04_real_photo_before_after.py` 会生成无文字四宫格，对比原图、缩放、灰度和裁剪效果。</figcaption>
</figure>

这张图的重点不是“滤镜好看”，而是让处理动作可检查：缩放改变尺寸，灰度改变颜色通道，裁剪改变视野，锐化会让局部边缘更清楚。图像处理的学习一定要看结果，否则代码只是空转。

<figure align="center">
  <img src="../assets/ch09/ch09_powershell_image_run.png" alt="PowerShell 运行 ch9 图像处理脚本截图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-12 PowerShell 真实运行结果</strong>：本章脚本会在 `output/` 和 `reports/` 里留下 demo 图、灰度图、真实照片对比图和图像处理报告。</figcaption>
</figure>

图像处理不怕步骤多，怕的是只留下一个“最终版”，却说不清它从哪里来。下面这张运行证据图把本章关键产物排成清单：原始卡片、灰度图、真实照片处理、视觉实验、质量总览、ch8 素材入库、处理故事板和视觉证据档案都要能被检查到。

<figure align="center">
  <img src="../assets/ch09/ch09_image_runtime_evidence.png" alt="PowerShell 风格的图像处理运行证据总览" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-13 PowerShell 风格的图像处理运行证据</strong>：`11_make_image_runtime_evidence.py` 检查本章关键图片和报告是否全部生成，让“我跑过了”变成可复盘、可交付的证据。</figcaption>
</figure>

---

## 9.5 与心理学和科研图片的连接

<figure align="center">
  <img src="../assets/ch09/ch09_psychology_link.png" alt="心理学和科研图片连接图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-14 心理学连接</strong>：把本章能力放进实验、记录、分析和学习分享的真实任务里。</figcaption>
</figure>

这一章把例子贴近心理学、科研记录和学习分享，因为这些任务天然需要清晰流程：图片来自哪里，处理做了什么，结果存到哪里，别人能不能复现。

在本章里，你可以这样理解项目价值：

- 它不是孤立练习，而是科研卡片工厂的一台新设备。
- 它处理的材料可以是课程笔记、实验记录、问卷结果、图片、网页资料或报告模板。
- 它最终要留下可检查的结果，而不是只在屏幕上闪一下。

<figure align="center">
  <img src="../assets/ch09/ch09_helmholtz_perception_story.png" alt="Hermann von Helmholtz照片" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-15 Hermann von Helmholtz照片</strong>：视觉不是摄像头式复制，人眼会根据经验、背景和对比做判断；图像处理要尊重这种感知特点。</figcaption>
</figure>

Helmholtz 的视觉研究可以帮你理解一件事：图片处理不仅发生在电脑里，也发生在观看者的脑子里。两块同样的灰色，放在不同背景上可能看起来完全不同；一张图片被裁掉边缘后，观看者的注意力也会被重新引导。做科研配图时，这不是小事。

<figure align="center">
  <img src="../assets/ch09/ch09_checker_shadow_illusion_story.png" alt="Adelson 棋盘阴影错觉图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-16 Adelson 棋盘阴影错觉</strong>：图片里的 A 和 B 看起来一深一浅，但经典错觉的妙处就在于：眼睛会把阴影、背景和经验一起算进去。</figcaption>
</figure>

这张图像是在给图像处理“泼一杯清醒水”。Python 看到的是像素值，人看到的是场景。你把亮度调高一点，程序觉得只是数值变化；观看者可能会觉得“证据更强了”。你裁掉一个边角，程序觉得只是坐标变了；别人可能会失去判断上下文。图像处理越强大，越要诚实。

---

## 9.6 关键概念拆解表

| 概念 | 人话理解 | 本章落点 |
| --- | --- | --- |
| 像素和坐标 | 图片是很多小格子，每个格子都有位置 | 裁剪时用 `(left, top, right, bottom)` 指定区域 |
| RGB/RGBA | RGB 是颜色，A 是透明度 | 生成卡片图时要知道图片模式是 `RGB` 还是 `L` |
| Pillow 打开保存 | Pillow 像图像处理工作台，负责读图和写图 | `Image.open()`、`im.save()` 是本章最小闭环 |
| 缩放裁剪 | 缩放改变尺寸，裁剪改变视野 | `02_resize_grayscale.py` 和 `04_real_photo_before_after.py` 都会用到 |
| 滤镜和灰度 | 灰度是去掉颜色信息，滤镜是批量改像素 | `convert("L")` 生成灰度图，`ImageFilter.SHARPEN` 强化局部边缘 |
| 批量处理 | 一张张手改会累，程序适合批量处理 | `03_batch_image_report.py` 读取文件夹中的多张 PNG |
| 视觉感知与图像解释 | 人眼会受背景、对比和经验影响 | `06_make_visual_perception_lab.py` 生成小实验 |
| 图像质量检查 | 好图不是越亮越锐，而是适合任务 | `07_make_image_quality_contact_sheet.py` 生成无文字处理效果总览 |
| 素材入库体检 | 从网页采集来的图，要先看尺寸、格式和比例，再决定能不能进卡片 | `08_make_ch08_image_intake.py` 扫描 ch8 图片素材并生成体检单 |
| 处理故事板 | 把原图、灰度、裁剪、增强和卡片成品连成一条可复盘路径 | `10_make_processing_storyboard.py` 生成图像处理流水线故事板 |

这张表的作用，是把“我好像懂了”变成“我知道它在哪用”。学习编程时，最危险的状态不是完全不会，而是听解释时点头，自己动手时发呆。每学一个概念，都要强迫自己问一句：它在本章项目里负责哪一段工作？

---

## 9.7 配套代码逐个导览

### 脚本 1：`01_create_demo_image.py`

运行方式：

```bash
python code/ch09/01_create_demo_image.py
```

阅读时重点看三件事：输入从哪里来，处理步骤在哪里，结果输出到哪里。不要只盯着语法，要把它当成一条小流水线。

### 脚本 2：`02_resize_grayscale.py`

运行方式：

```bash
python code/ch09/02_resize_grayscale.py
```

阅读时重点看三件事：输入从哪里来，处理步骤在哪里，结果输出到哪里。不要只盯着语法，要把它当成一条小流水线。

### 脚本 3：`03_batch_image_report.py`

运行方式：

```bash
python code/ch09/03_batch_image_report.py
```

阅读时重点看三件事：输入从哪里来，处理步骤在哪里，结果输出到哪里。不要只盯着语法，要把它当成一条小流水线。

### 脚本 4：`04_real_photo_before_after.py`

运行方式：

```bash
python code/ch09/04_real_photo_before_after.py
```

它会读取 `assets/ch09/web/fronalpstock_sample.jpg`，生成：

```text
output/fronalpstock_before_after.png
```

这一张图把原图、缩放、灰度和裁剪放在一起。请重点观察：尺寸、颜色和视野发生了什么变化。图像处理不要只看“代码成功运行”，要打开输出文件，确认结果真的符合目的。

### 脚本 5：`05_make_image_processing_report.py`

运行方式：

```bash
python code/ch09/05_make_image_processing_report.py
```

这个脚本会读取前面生成的图像结果，并生成：

```text
reports/ch09_image_processing_report.md
reports/ch09_image_processing_report_preview.png
```

它的作用是把处理结果整理成一份报告：哪些图片被处理了，尺寸是多少，颜色模式是什么，用途是什么。图像处理最怕“文件夹里一堆图但不知道哪张是最终版”，报告能帮你把结果说清楚。

第一次运行时不要急着改代码。先原样运行，确认能看到输出；第二次再改一个最小参数；第三次再尝试把输出写入 `output/` 或 `reports/`。这种节奏比“一上来就大改”更稳。

### 脚本 6：`06_make_visual_perception_lab.py`

运行方式：

```bash
python code/ch09/06_make_visual_perception_lab.py
```

这个脚本会生成：

```text
reports/ch09_visual_perception_lab.md
output/ch09_visual_perception_lab.png
```

它把同一张图放进几个不同处理条件里：原图、灰度、锐化、RGB 均值和同色错觉。请注意，这个实验不是为了炫技，而是为了训练一种谨慎感：图像处理既能帮助看清结构，也可能改变观看者的判断。每一次增强、裁剪、配色，都应该能说清楚目的。

### 脚本 7：`07_make_image_quality_contact_sheet.py`

运行方式：

```bash
python code/ch09/07_make_image_quality_contact_sheet.py
```

这个脚本会生成：

```text
reports/ch09_image_quality_contact_sheet.md
output/ch09_image_quality_contact_sheet.png
```

它不会在图片里塞解释文字，只把不同处理结果放在同一张总览图里。这样做很像把几张照片摊在桌上比较：哪张适合卡片封面，哪张适合报告插图，哪张看起来“很猛”但其实过度处理。说明写在报告里，图片负责让眼睛先看见差异。

### 脚本 8：`08_make_ch08_image_intake.py`

运行方式：

```bash
python code/ch09/08_make_ch08_image_intake.py
```

这个脚本读取 ch8 的 `assets/ch08/web/` 图片素材，生成格式、尺寸、颜色模式和入库建议。它把“图片能打开”继续推进成“图片适不适合学习卡片和报告使用”。从网上找到一张图只是第一步，真正进入卡片工厂之前，还要看它够不够清楚、比例是否极端、是否需要裁剪、有没有保留原始来源。

### 脚本 9：`09_make_visual_evidence_archive.py`

运行方式：

```bash
python code/ch09/09_make_visual_evidence_archive.py
```

这个脚本会把本章几个关键输出集中成一份视觉证据档案：

```text
reports/ch09_visual_evidence_archive.md
output/visual_evidence_archive.png
```

它的作用不是再制造一张“好看的图”，而是把原始卡片、灰度版本、真实照片处理、知觉实验台、质量总览、处理故事板和 ch8 素材入库结果放到一起。做图像处理时，最怕只留下一个最终文件，却说不清它从哪里来、经过了什么处理、有没有被过度裁剪。证据档案就是给每张图留下来龙去脉。如果你运行了下面的 `10_make_processing_storyboard.py`，可以再回头运行一次这个脚本，让档案刷新到最新状态。

### 脚本 10：`10_make_processing_storyboard.py`

运行方式：

```bash
python code/ch09/10_make_processing_storyboard.py
```

这个脚本会读取同一张真实风景照片，生成一张从“原图”到“卡片素材”的处理故事板：

```text
reports/ch09_processing_storyboard.md
output/ch09_processing_storyboard.png
```

它训练的是图像处理里最重要的作品意识：每一步都要留下文件，每一步都要能解释目的。原图负责保留证据，灰度负责检查明暗，裁剪负责选择焦点，增强负责让细节更清楚，卡片版负责最终交付。处理图片不是在滤镜商店里随便试衣服，而是在给一个真实任务做合适的版式。

### 脚本 11：`11_make_image_runtime_evidence.py`

运行方式：

```bash
python code/ch09/11_make_image_runtime_evidence.py
```

这个脚本会检查本章关键输出是否都已经生成，并整理成一张 PowerShell 风格的运行证据图：

```text
reports/ch09_image_runtime_evidence.md
output/ch09_image_runtime_evidence.png
assets/ch09/web/ch09_image_runtime_evidence.png
```

它的作用像一张“图像处理验收单”：不是继续加工图片，而是确认加工结果、报告、故事板和证据档案都在正确位置。以后做课程分享或科研报告时，这一步很有用，因为它把“我记得跑过”变成“我能拿出证据”。

---

## 9.8 常见坑

<figure align="center">
  <img src="../assets/ch09/ch09_pitfall_map.png" alt="常见坑地图" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-17 常见坑地图</strong>：错误不是判决，而是提醒你该检查路径、输入、状态或依赖。</figcaption>
</figure>

本章常见坑：

- 覆盖原图
- 比例失真
- 路径写错
- 忽略透明通道

遇到问题时，先看报错信息，再看文件路径，最后看输入数据。不要一报错就重装环境。重装是最后手段，不是第一反应。

---

## 9.9 本章小项目：学习卡片配图处理器

<figure align="center">
  <img src="../assets/ch09/ch09_project_dashboard.png" alt="项目仪表盘" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-18 本章项目</strong>：完成“学习卡片配图处理器”，给科研卡片工厂增加一项新能力。</figcaption>
</figure>

项目目标：打开图片、缩放、裁剪、转灰度、加边框，并批量导出卡片配图，最后生成一份图像处理报告。

<figure align="center">
  <img src="../assets/ch09/ch09_image_processing_report_preview.png" alt="Python 生成的图像处理报告预览" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-19 Python 生成的图像处理报告预览</strong>：生成图、灰度图、真实照片对比和科学图像素材放在一起，方便检查尺寸、模式和用途。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch09/ch09_visual_perception_lab.png" alt="Python 生成的视觉感知小实验预览" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-20 Python 生成的视觉感知小实验</strong>：同一张图经过灰度、锐化、RGB 摘要和错觉对比后，能提醒你：像素变化和人眼感受不是一回事。</figcaption>
</figure>

<figure align="center">
  <img src="../assets/ch09/ch09_image_quality_contact_sheet.png" alt="Python 生成的无文字图像质量检查总览" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-21 Python 生成的图像质量检查总览</strong>：同一张风景图被裁剪、灰度化、增强和风格化后，差异直接摆在眼前；解释文字放在报告和正文中。</figcaption>
</figure>

这张图来自 `07_make_image_quality_contact_sheet.py`。它提醒你：图像处理的审美不是“滤镜越重越高级”，而是看任务。学习卡片需要清楚、稳定、少干扰；实验刺激需要尺寸统一、可复现；报告配图需要别人一眼看出重点。图片可以漂亮，但不能漂亮到把事实带偏。

<figure align="center">
  <img src="../assets/ch09/ch09_processing_storyboard.png" alt="Python 生成的图像处理故事板" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-22 Python 生成的图像处理故事板</strong>：`10_make_processing_storyboard.py` 把原图、灰度、裁剪、增强和卡片成品排成一条可复盘流水线，帮助你说清每一步为什么存在。</figcaption>
</figure>

这张故事板把图像处理从“我调了几个参数”变成“我完成了一条交付路径”。原图不要删，因为它是证据；灰度不是退回黑白电视，而是帮你检查明暗结构；裁剪不是随手切一刀，而是决定观看者先看哪里；增强不是越猛越好，而是让关键信息更清楚；卡片成品才是最后要进入科研卡片工厂的材料。

如果你已经完成 ch8 的公开资料采集，本章还可以直接扫描 ch8 下载和生成的图片素材。这样，图片不是散落在文件夹里的“看着还行”，而是先过一遍入库体检：格式是什么，尺寸够不够，比例是否适合卡片，是否需要复查。

运行方式：

```bash
python code/ch09/08_make_ch08_image_intake.py
```

运行后会生成：

```text
output/ch09_ch08_image_intake.json
reports/ch09_ch08_image_intake.md
output/ch09_ch08_image_intake.png
```

<figure align="center">
  <img src="../assets/ch09/ch09_ch08_image_intake.png" alt="Python 生成的 ch8 图像素材入库体检单" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-23 Python 生成的 ch8 图像素材入库体检单</strong>：`08_make_ch08_image_intake.py` 扫描 ch8 的公开资料图片素材，检查格式、尺寸、比例和入库建议。</figcaption>
</figure>

这一步把 ch8 和 ch9 接起来：ch8 负责把公开资料带回来，ch9 负责判断图片能不能稳定进入卡片、报告和学习展示。很多图片不是“坏”，只是用途不对。小图别硬放大，长图别硬塞方框，处理过的图别覆盖原图。图像处理真正专业的地方，不是把图变得更花，而是让每张图有合适的位置。

<figure align="center">
  <img src="../assets/ch09/ch09_visual_evidence_archive.png" alt="Python 生成的视觉证据档案" style="zoom:50%; display:block; margin:0 auto;" />
  <figcaption><strong>图9-24 Python 生成的视觉证据档案</strong>：`09_make_visual_evidence_archive.py` 把本章关键输出集中成一张可复盘总览，方便检查原图、处理图、处理故事板、质量总览和跨章节素材入库结果。</figcaption>
</figure>

这张图是本章的“证据桌面”。想象你正在给一组科研图片做整理：如果只留下最终版，过几天你很可能会忘记它是怎么裁的、为什么变灰、有没有过度锐化、原图是否还在。视觉证据档案把这些产物摆在一起，让你能顺着路径追回去。

这也是图像处理最容易被忽视的审美：不是每张图都要更亮、更锐、更有冲击力，而是每个处理动作都要能回答“我为什么这样改”。心理学实验里，一个不小心的裁剪可能改变被试看见的线索；学习卡片里，一个过度滤镜可能让人盯着效果忘了概念；科研报告里，一个没有记录来源的图，很难让别人复现你的材料。

项目结构可以这样安排：

```text
python_card_factory/
├── code/
│   └── ch09/
├── input/
├── output/
├── reports/
└── assets/
```

本章配套脚本：

- `code/ch09/01_create_demo_image.py`
- `code/ch09/02_resize_grayscale.py`
- `code/ch09/03_batch_image_report.py`
- `code/ch09/04_real_photo_before_after.py`
- `code/ch09/05_make_image_processing_report.py`
- `code/ch09/06_make_visual_perception_lab.py`
- `code/ch09/07_make_image_quality_contact_sheet.py`
- `code/ch09/08_make_ch08_image_intake.py`
- `code/ch09/09_make_visual_evidence_archive.py`
- `code/ch09/10_make_processing_storyboard.py`
- `code/ch09/11_make_image_runtime_evidence.py`

完成标准：

1. 能按顺序运行 `01_create_demo_image.py` 到 `10_make_processing_storyboard.py`，重新运行 `09_make_visual_evidence_archive.py` 刷新证据档案，再运行 `11_make_image_runtime_evidence.py` 生成运行证据。
2. 能解释脚本输入、处理、输出分别是什么。
3. 把生成结果保存到 `output/` 或 `reports/`。
4. 在 README 或学习记录中写下运行命令。
5. 能生成 `reports/ch09_image_processing_report.md` 和 `reports/ch09_image_processing_report_preview.png`。
6. 能生成 `reports/ch09_visual_perception_lab.md` 和 `output/ch09_visual_perception_lab.png`。
7. 能生成 `reports/ch09_image_quality_contact_sheet.md` 和 `output/ch09_image_quality_contact_sheet.png`，并解释哪一种处理更适合学习卡片。
8. 能生成 `reports/ch09_ch08_image_intake.md` 和 `output/ch09_ch08_image_intake.json`，并说明 ch8 的图片素材怎样进入 ch9 的质量检查流程。
9. 能生成 `reports/ch09_visual_evidence_archive.md` 和 `output/visual_evidence_archive.png`，并解释为什么图像处理要保留证据链。
10. 能生成 `reports/ch09_processing_storyboard.md` 和 `output/ch09_processing_storyboard.png`，并说明原图、灰度、裁剪、增强和卡片成品各自解决什么问题。
11. 能生成 `reports/ch09_image_runtime_evidence.md` 和 `output/ch09_image_runtime_evidence.png`，并说明哪些产物已经 ready、哪些还需要补跑。

动手步骤：

1. **准备目录**：确认 `python_card_factory/` 下有 `code/`、`input/`、`output/`、`reports/`。
2. **运行最小脚本**：先运行本章第一个脚本，得到一个确定反馈。
3. **记录环境**：把 Python 版本、运行命令和输出截图或输出文本写进 `reports/`。
4. **连接真实材料**：把课程笔记、实验记录、图片、网页或 CSV 放进 `input/`。
5. **生成作品**：让脚本在 `output/` 中留下处理结果，在 `reports/` 中留下图像处理报告。
6. **观察感知差异**：运行 `06_make_visual_perception_lab.py`，记录灰度、锐化和错觉图分别改变了什么。
7. **检查图像质量**：运行 `07_make_image_quality_contact_sheet.py`，比较不同处理结果，选出最适合学习卡片的一版。
8. **制作处理故事板**：运行 `10_make_processing_storyboard.py`，把原图到卡片成品的路径摆出来。
9. **体检采集素材**：运行 `08_make_ch08_image_intake.py`，检查 ch8 图片素材是否适合进入学习卡片。
10. **刷新证据档案**：运行 `09_make_visual_evidence_archive.py`，把关键输出集中成可复盘总览。
11. **生成运行证据**：运行 `11_make_image_runtime_evidence.py`，检查本章关键产物是否全部落盘。
12. **写复盘**：说明这章让卡片工厂多了什么能力，哪些地方还容易出错。

---

## 9.10 练习任务

1. 修改一个输入参数，观察输出变化。
2. 把脚本生成的结果保存成文件。
3. 故意制造一个小错误，记录报错信息和修复方式。
4. 把本章项目和前面章节连接起来，例如读取 ch03 整理出的文件，或使用 ch02 的数据结构保存结果。
5. 找一张自己的学习卡片配图，生成灰度版和裁剪版，并说明哪一种更适合报告。
6. 运行 `07_make_image_quality_contact_sheet.py`，把其中一种处理替换成你自己的版本，例如降低饱和度、加边框或生成缩略图。
7. 运行 `10_make_processing_storyboard.py`，把其中一个阶段替换成你自己的处理方式，并说明它是为了学习卡片、实验还是报告服务。
8. 打开 `reports/ch09_ch08_image_intake.md`，挑一张标记为 `review` 的图片，写出它需要复查或重新处理的原因。
9. 运行 `09_make_visual_evidence_archive.py`，把自己新增的处理结果也放进视觉证据档案，并说明它解决了什么问题。
10. 运行 `11_make_image_runtime_evidence.py`，检查是否还有 missing 项；如果有，写下应该补跑哪一个脚本。

---

## 9.11 自测问题

1. 本章最重要的三个概念是什么？请用人话解释，不要只背术语。
2. 本章第一个脚本的输入、处理、输出分别是什么？
3. 如果脚本运行失败，你第一步会检查路径、环境、依赖还是语法？为什么？
4. 本章项目和“科研卡片工厂”有什么关系？
5. 你能不能把本章项目改成一个心理学或学习分享场景的小任务？

参考回答不唯一。判断自己是否真的理解，可以看你能不能把答案讲给一个完全没学过本章的人听。

---

## 9.12 学习复盘模板

可以在 `reports/ch09_review.md` 中写下：

```markdown
# 第9章复盘

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

## 9.13 与后续章节的连接

本章不是孤岛。它和整套教程的关系可以这样理解：

- 前面章节提供基础：环境、数据结构、文件管理。
- 本章提供一项新能力：学习卡片配图处理器，并能把处理路径整理成可复盘故事板。
- 后面章节会把这项能力继续接到数据分析、资料采集、报告生成和办公自动化里。

所以不要只问“这一章考试考什么”。更好的问题是：它能帮我少做哪一类重复劳动？它能让我的学习材料、实验记录或报告更稳定吗？

---

## 9.14 本章总结

Python 图像处理的关键不是“记住所有 API”，而是理解它解决的问题。你已经从概念、图像、代码和小项目四个角度接触了本章内容。下一次复习时，不要只问“我会不会背”，而要问：

- 我能不能讲出这个概念的比喻？
- 我能不能运行一个最小脚本？
- 我能不能把结果放进项目目录？
- 我能不能说清楚它在科研卡片工厂里增加了什么能力？

如果答案是肯定的，这一章就不是看过了，而是真的进入你的工具箱了。
