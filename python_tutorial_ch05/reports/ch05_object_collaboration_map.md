# 第5章对象协作消息图

面向对象不是把代码切成很多孤岛，而是让每个对象只承担清楚的职责，再通过消息协作。

| 发送方向 | 消息 | 意义 |
| --- | --- | --- |
| LearningCard -> CardDeck | add | 一张卡片进入卡片盒 |
| CardDeck -> Trial | draw | 从卡片盒抽出一次练习材料 |
| Trial -> ReportBuilder | record | 试次把反应结果交给报告整理员 |
| ReportBuilder -> LearningCard | summarize | 报告反过来帮助卡片复习与改进 |

## 观察提示

如果一条消息说不清楚，通常说明职责边界还没想清楚。先改设计，再急着写代码。
