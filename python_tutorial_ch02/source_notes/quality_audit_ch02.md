# 第2章优化版质量验收记录

验收日期：2026-06-18

## 验收范围

本次验收范围是 `python_tutorial_ch02_optimized` 包，重点包括：

- `chapters/ch02_python_data_types.md`
- `assets/ch02/`
- `code/ch02/`
- `reports/`
- `output/`
- `README.md`
- `manifest.json`
- `source_notes/ch02_user_experience_review.md`

## 关键修改验收

| 项目 | 结果 |
| --- | --- |
| 图文顺序 | 已调整为“路线 - 概念 - 单类型 - 组合项目 - 运行证据 - 报错 - 练习 - 下一章” |
| 图片编号 | 27 张图，图2-1 至图2-27 连续 |
| PowerShell 运行图 | 已从变量章节后移到本章小项目之后 |
| 运行证据总览图 | 已从前置位置移到全部项目脚本介绍完成后 |
| 布尔逻辑图 | 已移动到 `and/or/not` 小节表格后 |
| IBM 分拣机图 | 已移动到列表操作之后、字典章节之前，作为过渡 |
| 来源视角语言 | 已删除或改写“课件里”“参考 MATLAB 教材”等表达 |
| 新手易错点 | 已补充 `type()`、`float()`、`replace()` 返回值、`round(2.5)` 特例、`append()` 原地修改、字典 key 限制等说明 |
| 练习反馈 | 练习 2-4 已补充参考代码 |
| 配套文件树 | 已按正文图号顺序更新图片清单 |

## 验收命令与结果

在项目根目录运行：

```bash
python scripts/check_links.py
python - <<'PY'
import ast
from pathlib import Path
files = list(Path('code/ch02').glob('*.py')) + list(Path('scripts').glob('*.py'))
for p in files:
    ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
print('AST syntax OK:', len(files))
PY
for f in code/ch02/*.py; do python "$f" >/tmp/"$(basename "$f")".out; done
```

当前结果：

- Markdown 与 HTML 本地图片链接：通过，检查 1 个 Markdown 文件，0 个缺失本地图片链接。
- Python 语法检查：通过，AST 覆盖 14 个 `.py` 文件。
- 示例脚本运行检查：通过，`01` 至 `12` 均可运行。
- 运行证据脚本输出：`14/14 ready`。
- 正文字符数：31363。
- 正文图片引用数：27。
- 正文 figure 数：27。
- 正文 figcaption 数：27。
- PIL 图片打开检查：通过，正文引用的 27 张图片均可打开。

## 剩余建议

当前章节深度适合第2章初学者。后续章节可继续承接两条线：

1. 在函数章节正式解释可变对象、变量绑定与参数传递。
2. 在文件章节把本章 `list[dict]` 的 Stroop 数据包继续接到 CSV/JSON 读写、文件路径和报告生成。
