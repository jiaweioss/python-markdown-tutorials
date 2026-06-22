# 第2章质量验收记录

验收日期：2026-06-17

## 验收范围

本次验收范围是 `python_tutorial_ch02` 包，重点包括：

- `chapters/ch02_python_data_types.md`
- `assets/ch02/`
- `scripts/generate_ch02_visuals.py`
- `scripts/check_links.py`
- `code/ch02/`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch02.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 基于原 Python 课件改写 | 第2章正文覆盖课件中的常量、变量、布尔、数值、字符串、列表和字典 | 已完成 |
| 面向初学者、语言生动 | 正文使用变量标签、类型容器、红绿灯、抽屉、查表系统等比喻 | 已完成 |
| 图文并茂 | 正文引用 27 张本地正式配图，含历史照片、心理学人物照片、IBM 打孔卡分拣机、套娃嵌套照片、检索照片、真实 PowerShell 截图、类型选择罗盘、字符串材料工作台、脚本生成成果图、本章运行证据总览、报错线索卡、练习工作台和下一章过渡图 | 已完成 |
| 图片少放解释文字 | 变量标签、路线图、数据类型地图、布尔逻辑、字符串切片、列表、字典和小项目等核心概念图已重新生成，删减图内长解释文字，说明放回正文和图注 | 已完成 |
| 图片全部居中 | 正文 27 张图片全部使用 `<figure align="center">` 与 `display:block; margin:0 auto` 居中显示 | 已完成 |
| 图片图注清晰 | 正文 27 张图片全部配有 `<figcaption>`，图注显示图片标题和学习提示 | 已完成 |
| 学生阅读口吻 | 已将“给老师的提醒”“课堂练习”等教师视角文字改成学生自学口吻 | 已完成 |
| 图表审美在线 | `ch02_number_rounding_chart.png` 由 Python 脚本生成，并经肉眼检查修正图例挤压 | 已完成 |
| 字符串段落补图 | 新增 `ch02_string_material_workbench.png`，图片内部不放解释文字，正文用被试编号、刺激词、文件路径和日志备注解释为什么“文字也是数据” | 已完成 |
| 真实运行环境 | 新增 `ch02_powershell_data_type_run.png`，展示 ch2 脚本在 PowerShell 中真实运行 | 已完成 |
| 故事与知识点穿插 | Claude Shannon 对应信息编码，George Boole 对应布尔值，Hermann Ebbinghaus 对应列表与记忆数据，IBM 分拣机对应批量数据整理，套娃对应嵌套结构，卡片目录对应字典检索 | 已完成 |
| 学以致用 | 新增 12 个可运行脚本、学习记录整理小项目、类型选择卡片、类型选择罗盘、数据类型实验回执、Stroop 数据类型包、数据类型标本柜成果图和运行证据报告 | 已完成 |
| 类型判断工具 | 新增 `08_make_type_compass.py`，生成 `reports/ch02_type_compass.md` 和 `output/ch02_type_compass_preview.png`，把“看到数据先选类型”做成练习闭环 | 已完成 |
| 项目成果回执 | 新增 `09_make_data_type_lab_receipt.py`，生成 `reports/ch02_data_type_lab_receipt.md` 和 `output/ch02_data_type_lab_receipt.png`，把学习记录和心理学 trial 的类型选择做成可视化成果 | 已完成 |
| 心理学数据包 | 新增 `10_make_stroop_dataset_pack.py`，生成 JSON、CSV、Markdown 报告和 PNG 预览，把 ch1 的 Stroop trial 延伸成 `list[dict]` 数据包 | 已完成 |
| 数据类型标本柜 | 新增 `11_make_data_type_specimen_cabinet.py`，生成 JSON、Markdown 报告和 PNG 预览，把同一组 Stroop 记录拆成类型角色展示 | 已完成 |
| 运行证据总览 | 新增 `12_make_data_type_runtime_evidence.py`，检查本章 14 个关键产物并生成 Markdown 报告、输出图和正文正式图 | 已完成 |
| 图片平均穿插 | 在数字到字符串之间新增 `ch02_string_material_workbench.png`，并保留尾部 `ch02_error_clue_cards.png`、`ch02_practice_workbench.png` 与 `ch02_type_to_file_bridge.png`；最大图片间隔从 197 行降到 161 行 | 已完成 |
| 图片引用不缺失 | `python scripts/check_links.py` 同时检查 Markdown 图片和 HTML `<img>` 图片，检查通过 | 已完成 |
| 代码与脚本可检查 | AST 语法解析检查通过，且不生成 `__pycache__` 缓存 | 已完成 |
| 来源可追溯 | README、source manifest 与 manifest 均记录主课件和 MATLAB 参考角色 | 已完成 |

## 当前素材清单

正式教材图：

- `ch02_cover.png`
- `ch02_roadmap.png`
- `ch02_variable_label_metaphor.png`
- `ch02_powershell_data_type_run.png`
- `ch02_data_type_runtime_evidence.png`
- `ch02_data_type_atlas.png`
- `ch02_information_history_claude_shannon.png`
- `ch02_type_compass_preview.png`
- `ch02_history_george_boole.png`
- `ch02_bool_logic_switchboard.png`
- `ch02_number_rounding_chart.png`
- `ch02_string_material_workbench.png`
- `ch02_string_slice_ruler.png`
- `ch02_psychology_ebbinghaus_memory.png`
- `ch02_list_workbench.png`
- `ch02_punch_card_sorter_photo.png`
- `ch02_practice_workbench.png`
- `ch02_nested_data_matryoshka.png`
- `ch02_dictionary_card_catalog_photo.png`
- `ch02_dict_mapping_card.png`
- `ch02_mini_project_dashboard.png`
- `ch02_data_type_lab_receipt.png`
- `ch02_stroop_dataset_pack.png`
- `ch02_data_type_specimen_cabinet.png`
- `ch02_type_decision_cards_preview.png`
- `ch02_error_clue_cards.png`
- `ch02_type_to_file_bridge.png`

## 验收命令

在 `python_tutorial_ch02` 目录下运行：

```bash
python scripts/generate_ch02_visuals.py
python scripts/check_links.py
@'
import ast
from pathlib import Path
files = list(Path('code/ch02').glob('*.py')) + list(Path('scripts').glob('*.py'))
for p in files:
    ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
print('AST syntax OK:', len(files))
'@ | python -
```

当前结果：

- Markdown 与 HTML 本地图片链接：通过，检查 1 个 Markdown 文件，0 个缺失本地图片链接
- Python 语法检查：通过，AST 覆盖 14 个 `.py` 文件
- 12 个示例脚本运行检查：通过，其中 `12_make_data_type_runtime_evidence.py` 显示 `14/14 ready`
- 正文字符数：29065
- 正文图片引用数：27
- 正文 figure 数：27
- 正文 figcaption 数：27
- manifest 素材数：40（27 张正式图 + 13 张本地原图/截图/脚本成果图）
- Python 语法覆盖：通过，包括 12 个代码脚本和 2 个检查/生成脚本
- PIL 图片打开检查：通过，40 张图片均可打开
- 临时总览图人工检查：通过；27 张 ch2 正文图均居中展示，新增字符串材料工作台无说明文字堆叠、无越界，后续图号和图注连续。
- 全书一致性扫描：通过；11 个章节目录、130 个 Python 文件、108 个 `code/` 脚本、280 个正文图片引用，0 个缺失本地图片、0 个图注数量不一致、0 个 manifest 不一致、0 个 PIL 打开错误、0 个旧 `_audit*` 残留。

## 剩余边界

本章已经按当前图文标准继续扩充。后续仍可继续围绕更真实的数据来源、更多学科场景和跨章节项目衔接继续增强。
