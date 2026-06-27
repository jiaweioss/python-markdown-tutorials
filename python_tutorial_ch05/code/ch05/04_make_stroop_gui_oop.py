"""将 Stroop 数据浏览面板改写为面向对象版本。

职责划分：
  - StroopDataLoader：负责加载数据（JSON 或后备数据）
  - StroopProcessor：负责从原始数据计算指标和整理试次
  - MetricsDisplay：负责在面板上展示指标卡片
  - TrialTable：负责在面板上展示试次表格
  - ActionBar：负责创建底部操作按钮
  - StroopDashboard：主面板，组合所有子组件并启动 GUI
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
import tkinter as tk
from tkinter import ttk


# ── 第 1 个类：专门负责数据加载 ──────────────────────────────

class StroopDataLoader:
    """从 JSON 文件或后备数据加载 Stroop 实验数据。"""

    def __init__(self) -> None:
        book_root = Path(__file__).resolve().parents[3]
        self._source = (
            book_root
            / "python_tutorial_ch03"
            / "workspace_ch03"
            / "organized"
            / "json"
            / "ch02_stroop_dataset_pack.json"
        )
        self._fallback = {
            "summary": {
                "participant": "S001",
                "trial_count": 4,
                "accuracy": 1.0,
                "mean_reaction_time_ms": 585.0,
                "congruent_count": 2,
                "incongruent_count": 2,
            },
            "trials": [
                {"trial_id": 1, "word": "RED", "ink_color": "blue",
                 "response_key": "j", "correct": True, "congruent": False,
                 "reaction_time_ms": 612.4},
                {"trial_id": 2, "word": "GREEN", "ink_color": "green",
                 "response_key": "f", "correct": True, "congruent": True,
                 "reaction_time_ms": 538.2},
                {"trial_id": 3, "word": "BLUE", "ink_color": "red",
                 "response_key": "f", "correct": True, "congruent": False,
                 "reaction_time_ms": 701.8},
                {"trial_id": 4, "word": "RED", "ink_color": "red",
                 "response_key": "f", "correct": True, "congruent": True,
                 "reaction_time_ms": 487.6},
            ],
        }

    def load(self) -> dict:
        """返回原始数据字典。优先读 JSON，失败时返回后备数据。"""
        if self._source.exists():
            return json.loads(self._source.read_text(encoding="utf-8"))
        return self._fallback

    @property
    def source_label(self) -> str:
        """返回数据来源的文字描述，用于 GUI 顶部显示。"""
        if self._source.exists():
            return self._source.relative_to(
                Path(__file__).resolve().parents[3]
            ).as_posix()
        return "fallback/sample"


# ── 第 2 个类：专门负责数据处理 ──────────────────────────────

class StroopProcessor:
    """从原始字典计算出面板需要的指标和试次列表。"""

    def __init__(self, raw: dict) -> None:
        self._raw = raw

    def compute_metrics(self) -> dict:
        """返回包含 participant / trial_count / accuracy 等的指标字典。"""
        trials = self._raw.get("trials", [])
        summary = dict(self._raw.get("summary", {}))
        if trials and not summary.get("trial_count"):
            summary["trial_count"] = len(trials)
            summary["accuracy"] = (
                sum(1 for t in trials if t.get("correct")) / len(trials)
            )
            summary["mean_reaction_time_ms"] = mean(
                float(t.get("reaction_time_ms", 0)) for t in trials
            )
            summary["congruent_count"] = sum(
                1 for t in trials if t.get("congruent")
            )
            summary["incongruent_count"] = sum(
                1 for t in trials if not t.get("congruent")
            )
            summary["participant"] = trials[0].get("participant", "S001")
        return summary

    def get_trials(self) -> list[dict]:
        """返回原始试次列表。"""
        return self._raw.get("trials", [])


# ── 第 3 个类：专门负责指标卡片 UI ──────────────────────────

class MetricsDisplay:
    """在父容器中创建一排指标卡片。"""

    def __init__(self, parent: tk.Frame, metrics: dict) -> None:
        self._parent = parent
        self._metrics = metrics

    def build(self) -> None:
        """在父容器中绘制卡片。"""
        frame = tk.Frame(self._parent)
        frame.pack(fill="x", padx=20, pady=8)

        items = [
            ("参与被试", self._metrics.get("participant", "—")),
            ("试次总数", str(self._metrics.get("trial_count", 0))),
            ("正确率", f"{round(float(self._metrics.get('accuracy', 0)) * 100, 1)}%"),
            ("平均反应时",
             f"{round(float(self._metrics.get('mean_reaction_time_ms', 0)), 1)} ms"),
            ("冲突试次", str(self._metrics.get("incongruent_count", 0))),
        ]
        for label, value in items:
            card = tk.Frame(frame, relief="groove", bd=1, padx=10, pady=6)
            card.pack(side="left", fill="x", expand=True, padx=4)
            tk.Label(card, text=label,
                     font=("Microsoft YaHei", 9), fg="#888888").pack()
            tk.Label(card, text=value,
                     font=("Microsoft YaHei", 14, "bold")).pack()


# ── 第 4 个类：专门负责试次表格 UI ──────────────────────────

class TrialTable:
    """在父容器中创建带表头的试次表格。"""

    def __init__(self, parent: tk.Frame, trials: list[dict]) -> None:
        self._parent = parent
        self._trials = trials

    def build(self) -> None:
        """在父容器中绘制 Treeview 表格。"""
        columns = ("id", "word", "ink", "key", "rt", "correct", "congruent")
        tree = ttk.Treeview(self._parent, columns=columns,
                            show="headings", height=10)

        headings = [
            ("id", "ID", 40),
            ("word", "词", 80),
            ("ink", "墨水色", 80),
            ("key", "按键", 60),
            ("rt", "反应时(ms)", 100),
            ("correct", "正确", 60),
            ("congruent", "一致", 60),
        ]
        for col, heading, width in headings:
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="center")

        for t in self._trials:
            tree.insert(
                "",
                "end",
                values=(
                    t.get("trial_id", ""),
                    t.get("word", ""),
                    t.get("ink_color", ""),
                    t.get("response_key", ""),
                    f"{float(t.get('reaction_time_ms', 0)):.1f}",
                    "是" if t.get("correct") else "否",
                    "是" if t.get("congruent") else "否",
                ),
            )

        tree.pack(fill="both", expand=True, padx=20, pady=8)


# ── 第 5 个类：专门负责底部按钮区 UI ────────────────────────

class ActionBar:
    """在父容器底部创建一组操作按钮。"""

    def __init__(self, parent: tk.Frame) -> None:
        self._parent = parent

    def build(self) -> None:
        """绘制按钮行。"""
        btn_frame = tk.Frame(self._parent)
        btn_frame.pack(pady=16)
        for text in ("加载数据", "查看试次", "导出卡片", "生成报告"):
            tk.Button(btn_frame, text=text, width=12,
                      state="disabled").pack(side="left", padx=6)


# ── 第 6 个类：主面板，组合所有子组件 ──────────────────────

class StroopDashboard:
    """Stroop 数据浏览主面板。

    职责：创建窗口，组合子组件（数据来源标签、指标卡片、表格、按钮），
    并启动 Tkinter 事件循环。自己不处理数据，也不直接操作表格细节。
    """

    def __init__(self) -> None:
        self._loader = StroopDataLoader()
        raw = self._loader.load()
        self._processor = StroopProcessor(raw)
        self._metrics = self._processor.compute_metrics()
        self._trials = self._processor.get_trials()

        self._root = tk.Tk()
        self._root.title("Stroop 数据浏览面板（OOP 版本）")
        self._root.geometry("900x600")

    def _build_source_label(self) -> None:
        """在窗口顶部显示数据来源。"""
        tk.Label(
            self._root,
            text=f"数据来源：{self._loader.source_label}",
            anchor="w",
            font=("Microsoft YaHei", 11),
            fg="#666666",
        ).pack(fill="x", padx=20, pady=(12, 4))

    def run(self) -> None:
        """构建所有 UI 组件并启动事件循环。"""
        self._build_source_label()
        MetricsDisplay(self._root, self._metrics).build()
        TrialTable(self._root, self._trials).build()
        ActionBar(self._root).build()
        self._root.mainloop()


# ── 入口 ────────────────────────────────────────────────────

if __name__ == "__main__":
    dashboard = StroopDashboard()
    dashboard.run()
