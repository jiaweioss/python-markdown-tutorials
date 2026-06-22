# 第5章对象模型报告

## 类与职责

| 类 | 职责 | 典型属性 | 典型方法 |
| --- | --- | --- | --- |
| LearningCard | 保存一张学习卡片 | topic, question, answer, tags | preview() |
| CardDeck | 管理一组卡片 | name, cards | add(), summary() |
| Trial | 保存一次实验试次 | participant, stimulus, response, reaction_time_ms | is_fast() |

## 当前对象

- 第5章复习盒: 2 张卡片
- 试次：S001, RED/blue, j, 438.5 ms
- 是否快速反应：True