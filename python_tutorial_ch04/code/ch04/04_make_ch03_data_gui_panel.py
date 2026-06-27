"""Display Stroop data in a Tkinter GUI panel."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
import tkinter as tk
from tkinter import ttk

BOOK_ROOT = Path(__file__).resolve().parents[3]
SOURCE_JSON = (
    BOOK_ROOT
    / "python_tutorial_ch03"
    / "workspace_ch03"
    / "organized"
    / "json"
    / "ch02_stroop_dataset_pack.json"
)

FALLBACK_DATA = {
    "summary": {
        "participant": "S001",
        "trial_count": 4,
        "accuracy": 1.0,
        "mean_reaction_time_ms": 585.0,
        "congruent_count": 2,
        "incongruent_count": 2,
    },
    "trials": [
        {"trial_id": 1, "word": "RED", "ink_color": "blue", "response_key": "j", "correct": True, "congruent": False, "reaction_time_ms": 612.4},
        {"trial_id": 2, "word": "GREEN", "ink_color": "green", "response_key": "f", "correct": True, "congruent": True, "reaction_time_ms": 538.2},
        {"trial_id": 3, "word": "BLUE", "ink_color": "red", "response_key": "f", "correct": True, "congruent": False, "reaction_time_ms": 701.8},
        {"trial_id": 4, "word": "RED", "ink_color": "red", "response_key": "f", "correct": True, "congruent": True, "reaction_time_ms": 487.6},
    ],
}


def load_data() -> dict:
    if SOURCE_JSON.exists():
        return json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    return FALLBACK_DATA


def build_panel_data(data: dict) -> dict:
    trials = data.get("trials", [])
    summary = dict(data.get("summary", {}))
    if trials and not summary.get("trial_count"):
        summary["trial_count"] = len(trials)
        summary["accuracy"] = sum(1 for t in trials if t.get("correct")) / len(trials)
        summary["mean_reaction_time_ms"] = mean(
            float(t.get("reaction_time_ms", 0)) for t in trials
        )
        summary["congruent_count"] = sum(1 for t in trials if t.get("congruent"))
        summary["incongruent_count"] = sum(1 for t in trials if not t.get("congruent"))
        summary["participant"] = trials[0].get("participant", "S001")
    return {
        "metrics": summary,
        "trials": trials,
    }


class StroopDataPanel:
    def __init__(self) -> None:
        data = load_data()
        panel = build_panel_data(data)
        self.metrics = panel["metrics"]
        self.trials = panel["trials"]

        self.root = tk.Tk()
        self.root.title("Stroop 数据浏览面板")
        self.root.geometry("900x600")

        source_text = (
            SOURCE_JSON.relative_to(BOOK_ROOT).as_posix()
            if SOURCE_JSON.exists()
            else "fallback/sample"
        )
        tk.Label(
            self.root,
            text=f"数据来源：{source_text}",
            anchor="w",
            font=("Microsoft YaHei", 11),
            fg="#666666",
        ).pack(fill="x", padx=20, pady=(12, 4))

        self._build_metrics_area()
        self._build_trial_table()
        self._build_action_buttons()

    def _build_metrics_area(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=20, pady=8)
        items = [
            ("参与被试", self.metrics.get("participant", "—")),
            ("试次总数", str(self.metrics.get("trial_count", 0))),
            ("正确率", f"{round(float(self.metrics.get('accuracy', 0)) * 100, 1)}%"),
            ("平均反应时", f"{round(float(self.metrics.get('mean_reaction_time_ms', 0)), 1)} ms"),
            ("冲突试次", str(self.metrics.get("incongruent_count", 0))),
        ]
        for label, value in items:
            card = tk.Frame(frame, relief="groove", bd=1, padx=10, pady=6)
            card.pack(side="left", fill="x", expand=True, padx=4)
            tk.Label(card, text=label, font=("Microsoft YaHei", 9), fg="#888888").pack()
            tk.Label(card, text=value, font=("Microsoft YaHei", 14, "bold")).pack()

    def _build_trial_table(self) -> None:
        columns = ("id", "word", "ink", "key", "rt", "correct", "congruent")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)

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

        for t in self.trials:
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

    def _build_action_buttons(self) -> None:
        frame = tk.Frame(self.root)
        frame.pack(pady=16)
        for text in ("加载数据", "查看试次", "导出卡片", "生成报告"):
            tk.Button(frame, text=text, width=12, state="disabled").pack(side="left", padx=6)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    StroopDataPanel().run()


if __name__ == "__main__":
    main()
