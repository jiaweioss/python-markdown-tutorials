# 第 3 章初学者实操检测报告

检测日期：2026-06-19

## 检测目标

本次检测从初学者视角重新运行第 3 章《文件读写与文件夹管理》：先进入章节根目录，再按正文顺序运行示例脚本，确认文件确实被创建、读取、复制、归档、登记和可视化。重点检查三件事：

1. 学生照着命令运行时不会碰到真实资料目录。
2. 所有运行结果都能在 `workspace_ch03/` 或 `reports/` 中找到。
3. 教程中的图片顺序保持“先文字讲解，再图片和图注”，不会让图片突然抢在解释前面。

## 运行路线

从 `python_tutorial_ch03` 目录运行：

```bash
python code/ch03/01_create_sample_files.py
python code/ch03/02_read_text_file.py
python code/ch03/03_write_report.py
python code/ch03/04_copy_move_files.py
python code/ch03/05_walk_folder_report.py
python code/ch03/06_safe_delete_demo.py
python code/ch03/07_project_archiver.py
python code/ch03/08_make_archive_manifest.py
python code/ch03/09_make_archive_receipt.py
python code/ch03/10_make_path_safety_receipt.py
python code/ch03/11_make_ch02_stroop_file_handoff.py
python code/ch03/12_make_archive_evidence_board.py
python code/ch03/13_make_material_intake_register.py
```

## 结果摘要

| 检测项 | 结果 |
| --- | --- |
| 13 个 ch03 示例脚本 | 全部运行通过 |
| 视觉生成脚本 | `python scripts/generate_ch03_visuals.py` 运行通过 |
| Markdown 图片链接 | `python scripts/check_links.py` 通过，26 个本地图片引用 0 缺失 |
| Python 语法检查 | 13 个示例脚本 + 2 个工具脚本通过 `py_compile` |
| 图片完整性 | `assets/`、`workspace_ch03/`、`reports/` 下 46 张 PNG/JPG/GIF 均可由 PIL 打开 |
| 图文顺序 | 26 张图前均有文字讲解、任务说明或过渡句 |
| 损坏 PNG 修复 | `workspace_ch03/inbox/figure.png` 与 `workspace_ch03/organized/png/figure.png` 已改为真实 PNG，可打开 |

## 学生能看到的关键产物

- `workspace_ch03/data/raw_notes.txt`：练习用原始文本。
- `workspace_ch03/output/score_report.txt`：读取 CSV 后生成的成绩报告。
- `workspace_ch03/output/file_inventory.md`：遍历文件夹后生成的文件清单。
- `workspace_ch03/output/archive_report.md`：资料归档器生成的归档报告。
- `workspace_ch03/output/ch03_archive_manifest.md`：带角色、后缀、大小和哈希摘要的正式清单。
- `workspace_ch03/output/ch03_archive_receipt.md`：项目交付前可检查的归档回执。
- `workspace_ch03/output/ch03_path_safety_receipt.md`：批量文件操作前的路径安全体检。
- `workspace_ch03/output/ch03_ch02_stroop_file_handoff.md`：第 2 章 Stroop 数据包进入第 3 章工作区的交接记录。
- `reports/ch03_archive_evidence_board.md`：归档证据板报告。
- `reports/ch03_material_intake_register.md`：资料入库登记册报告。

## 初学者最容易踩的坑

1. **工作目录不对**：如果没有站在 `python_tutorial_ch03` 根目录，很多相对路径会找不到。正文已提醒先观察 `Path.cwd()`。
2. **误以为文件丢了**：`FileNotFoundError` 更常见的原因是“站错房间”，不是文件真的消失。
3. **覆盖原始资料**：正文强调原始资料进 `data/`，输出结果进 `output/`，不直接用 `"w"` 写原始文件。
4. **删除操作太快**：`06_safe_delete_demo.py` 与 `10_make_path_safety_receipt.py` 都把删除前的路径边界检查单独拿出来讲。
5. **只看代码不看结果**：本章要求学生检查真实生成的文件、清单、回执和图片，而不是只记住 API 名字。

## 教程呈现检查

本次已把图 3-5、图 3-7、图 3-9、图 3-10、图 3-11、图 3-12、图 3-13、图 3-14、图 3-15、图 3-16、图 3-19、图 3-21、图 3-23、图 3-24、图 3-26 等位置统一整理为“先叙述，后图片”。图片用于承接故事、展示环境或呈现运行结果，长解释留在 Markdown 正文和图注中。

## 结论

第 3 章当前已经可以作为初学者实操章节交付：它不是单纯罗列 `open()`、`os`、`pathlib`、`shutil`，而是让学生通过“资料归档器”把文件读写、文件夹管理、运行截图、清单、回执和项目证据串成一个可检查的小系统。
