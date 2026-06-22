# 第5章：GUI 面板对象模型报告

这份报告把 ch4 生成的 GUI 面板规格拆成对象：面板模型负责统筹，指标对象负责显示数字，动作对象负责按钮，试次对象负责一行实验记录。

| 对象 | 数量 | 职责 |
| --- | --- | --- |
| DataPanelModel | 1 | 统筹数据来源、指标、按钮动作和试次行 |
| PanelMetric | 5 | 显示一个关键指标 |
| PanelAction | 4 | 把用户点击变成方法调用 |
| TrialRow | 4 | 保存并展示一行 Stroop 试次 |

## 对象消息

- `DataPanelModel.load_source()`
- `PanelMetric.render()`
- `TrialRow.display_status()`
- `PanelAction.call()`
- `DataPanelModel.export_report()`

对象总数：14
JSON 交付物：`output/ch05_gui_panel_object_model.json`
预览图：`output/ch05_gui_panel_object_model.png`

下一步：如果继续进入 ch6，可以读取这个 JSON，把试次对象整理成表格，再分析正确率、反应时和冲突效应。
