# 第3章 ch2 Stroop 文件交接记录

        这份记录证明：第2章生成的数据包没有停留在内存里，而是被第3章读取、复制、归档并留下路径记录。

        ## 来源

        - JSON 来源：`C:/Users/84763/Desktop/Python教程/python_tutorial_ch02/output/ch02_stroop_dataset_pack.json`
        - CSV 来源：`C:/Users/84763/Desktop/Python教程/python_tutorial_ch02/output/ch02_stroop_dataset_pack.csv`

        ## 数据摘要

        - 被试编号：S001
        - trial 数量：4
        - 正确率：100%
        - 平均反应时：585.0 ms
        - 一致 / 冲突 trial：2 / 2

        ## 文件清单

        | 文件 | 位置 | 大小 | SHA256 前 12 位 |
| --- | --- | --- | --- |
| `inbox_json` | `C:/Users/84763/Desktop/Python教程/python_tutorial_ch03/workspace_ch03/inbox/ch02_stroop_dataset_pack.json` | 1418 bytes | `6bc28f91a067` |
| `inbox_csv` | `C:/Users/84763/Desktop/Python教程/python_tutorial_ch03/workspace_ch03/inbox/ch02_stroop_dataset_pack.csv` | 282 bytes | `db8ead933f3c` |
| `organized_json` | `C:/Users/84763/Desktop/Python教程/python_tutorial_ch03/workspace_ch03/organized/json/ch02_stroop_dataset_pack.json` | 1418 bytes | `6bc28f91a067` |
| `organized_csv` | `C:/Users/84763/Desktop/Python教程/python_tutorial_ch03/workspace_ch03/organized/csv/ch02_stroop_dataset_pack.csv` | 282 bytes | `db8ead933f3c` |

        ## 本章要点

        - `Path` 负责描述文件位置。
        - `read_text()` 读取 JSON 文本。
        - `shutil.copy2()` 复制数据文件并保留基础元数据。
        - `sha256` 摘要用于抽查文件是否被意外改动。
        - 输出报告放在 `workspace_ch03/output/`，不覆盖原始数据。
