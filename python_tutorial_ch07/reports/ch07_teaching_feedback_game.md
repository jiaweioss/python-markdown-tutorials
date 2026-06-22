# 第7章教学反馈小游戏计划

Skinner teaching machine 的启发很朴素：学习者做出反应以后，要立刻得到反馈。PyGame 让这个机制变得可编程：显示卡片、读取按键、更新状态、记录结果。

| 轮次 | 卡片 | 按键 | 难度带 | 反馈 |
| --- | --- | --- | --- | --- |
| 1 | 变量 | 1 | flow | Correct. Add one tiny challenge. |
| 2 | 列表 | 2 | flow | Correct. Add one tiny challenge. |
| 3 | 字典 | 3 | support | Slow down. Show the clue first. |

## 下一步

- 把 `cards` 写入 PyGame 主循环，逐张显示。
- 每次按键后立即显示对错、提示或鼓励。
- 把反应时和结果继续保存，交给 ch6 或 ch10 做报告。
