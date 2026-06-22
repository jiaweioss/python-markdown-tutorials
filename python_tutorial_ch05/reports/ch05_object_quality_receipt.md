# 第5章对象质量回执

写出 `class` 只是起点。对象质量回执用来检查：每个类是不是有明确职责，对象之间是不是靠清楚消息协作，项目里有没有开始长出万能类。

- 已通过检查：4 项
- 需要盯住：1 项

| 检查项 | 状态 | 证据 |
| --- | --- | --- |
| Single Job | OK | Each class has a clear responsibility. |
| Data + Method | OK | Object keeps data close to behavior. |
| Messages | OK | Collaboration uses named actions. |
| Composition | OK | CardDeck has cards instead of inheriting card. |
| God Object | WATCH | Avoid one class doing file, GUI, stats and export. |

下一步建议：一旦某个类同时负责读文件、管界面、做统计和导出报告，就先拆职责，而不是继续往里面塞方法。
这份回执可以和对象模型报告、类职责卡片、对象协作消息图一起提交。
