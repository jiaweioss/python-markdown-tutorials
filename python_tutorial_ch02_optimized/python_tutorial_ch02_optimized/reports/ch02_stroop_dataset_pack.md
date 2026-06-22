# 第2章 Stroop 数据类型包

        这份小数据包把 ch1 的极简 Stroop 任务继续往前推进：一次实验 trial 不是一行散乱文字，而是一条结构清楚的 `dict`；多次 trial 组成 `list`；整份数据可以保存成 JSON、CSV 和 Markdown 报告。

        ## 汇总

        - 被试编号：S001
        - trial 数量：4
        - 正确率：100%
        - 平均反应时：585.0 ms
        - 最快反应时：487.6 ms
        - 最慢反应时：701.8 ms
        - 一致 trial：2
        - 冲突 trial：2

        ## trial 表

        | trial | word | ink | response | correct | congruent | rt(ms) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | RED | blue | j | True | False | 612.4 |
| 2 | GREEN | green | f | True | True | 538.2 |
| 3 | BLUE | red | f | True | False | 701.8 |
| 4 | RED | red | f | True | True | 487.6 |

        ## 类型说明

        - `str`：保存被试编号、刺激词、墨水颜色和按键。
        - `int`：保存 trial 编号和数量。
        - `float`：保存反应时与平均值。
        - `bool`：保存是否正确、词义和颜色是否一致。
        - `None`：保存暂时没有备注的状态。
        - `dict`：保存一条 trial 的完整记录。
        - `list`：保存多条 trial，方便循环、统计和导出。
