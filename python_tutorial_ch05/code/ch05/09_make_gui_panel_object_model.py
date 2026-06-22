"""Turn the chapter 4 GUI panel spec into an object model."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch05").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
BOOK_ROOT = ROOT.parent
CH4_ROOT = BOOK_ROOT / "python_tutorial_ch04"
CH4_SCRIPT = CH4_ROOT / "code" / "ch04" / "08_make_ch03_data_gui_panel.py"
CH4_SPEC = CH4_ROOT / "output" / "ch04_ch03_data_gui_panel.json"

OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch05" / "web"

JSON_FILE = OUTPUT / "ch05_gui_panel_object_model.json"
REPORT_FILE = REPORTS / "ch05_gui_panel_object_model.md"
PREVIEW = OUTPUT / "ch05_gui_panel_object_model.png"


@dataclass
class PanelMetric:
    name: str
    value: str
    responsibility: str = "显示一个关键指标"


@dataclass
class PanelAction:
    label: str
    method_name: str
    responsibility: str = "把用户点击变成方法调用"


@dataclass
class TrialRow:
    trial_id: int
    word: str
    ink_color: str
    response_key: str
    reaction_time_ms: float
    correct: bool

    def display_status(self) -> str:
        return "ok" if self.correct else "check"


@dataclass
class DataPanelModel:
    title: str
    source: str
    metrics: list[PanelMetric]
    actions: list[PanelAction]
    rows: list[TrialRow]

    def object_count(self) -> int:
        return 1 + len(self.metrics) + len(self.actions) + len(self.rows)

    def messages(self) -> list[str]:
        return [
            "DataPanelModel.load_source()",
            "PanelMetric.render()",
            "TrialRow.display_status()",
            "PanelAction.call()",
            "DataPanelModel.export_report()",
        ]


FALLBACK_SPEC = {
    "panel_title": "Stroop 数据浏览面板",
    "source": "fallback/sample",
    "metrics": {
        "participant": "S001",
        "trial_count": 4,
        "accuracy_percent": 100.0,
        "mean_reaction_time_ms": 585.0,
        "conflict_trials": 2,
    },
    "actions": ["加载数据", "查看试次", "导出卡片", "生成报告"],
    "trial_preview": [
        {"trial_id": 1, "word": "RED", "ink_color": "blue", "response_key": "j", "reaction_time_ms": 612.4, "correct": True},
        {"trial_id": 2, "word": "GREEN", "ink_color": "green", "response_key": "f", "reaction_time_ms": 538.2, "correct": True},
    ],
}


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf") if bold else Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf") if bold else Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def ensure_ch4_spec() -> dict:
    if CH4_SPEC.exists():
        return json.loads(CH4_SPEC.read_text(encoding="utf-8"))
    if CH4_SCRIPT.exists():
        subprocess.run([sys.executable, str(CH4_SCRIPT)], cwd=CH4_ROOT, check=False, timeout=20)
    if CH4_SPEC.exists():
        return json.loads(CH4_SPEC.read_text(encoding="utf-8"))
    return FALLBACK_SPEC


def method_name(label: str) -> str:
    mapping = {
        "加载数据": "load_data",
        "查看试次": "select_trial",
        "导出卡片": "export_card",
        "生成报告": "build_report",
    }
    return mapping.get(label, "handle_action")


def build_model(spec: dict) -> DataPanelModel:
    metrics = spec.get("metrics", {})
    metric_objects = [
        PanelMetric("participant", str(metrics.get("participant", "S001"))),
        PanelMetric("trial_count", str(metrics.get("trial_count", 0))),
        PanelMetric("accuracy", f"{metrics.get('accuracy_percent', 0)}%"),
        PanelMetric("mean_rt", f"{metrics.get('mean_reaction_time_ms', 0)} ms"),
        PanelMetric("conflict", str(metrics.get("conflict_trials", 0))),
    ]
    actions = [PanelAction(label=label, method_name=method_name(label)) for label in spec.get("actions", [])]
    rows = [
        TrialRow(
            trial_id=int(row.get("trial_id", 0)),
            word=str(row.get("word", "")),
            ink_color=str(row.get("ink_color", "")),
            response_key=str(row.get("response_key", "")),
            reaction_time_ms=float(row.get("reaction_time_ms", 0)),
            correct=bool(row.get("correct", False)),
        )
        for row in spec.get("trial_preview", [])
    ]
    return DataPanelModel(
        title=str(spec.get("panel_title", "数据浏览面板")),
        source=str(spec.get("source", "unknown")),
        metrics=metric_objects,
        actions=actions,
        rows=rows,
    )


def write_json(model: DataPanelModel) -> None:
    OUTPUT.mkdir(exist_ok=True)
    payload = asdict(model) | {
        "object_count": model.object_count(),
        "messages": model.messages(),
        "handoff": {
            "from": "ch04 GUI panel spec",
            "to": "ch05 object model",
            "next": "ch06 can analyze exported rows as data",
        },
    }
    JSON_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_report(model: DataPanelModel) -> None:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第5章：GUI 面板对象模型报告",
        "",
        "这份报告把 ch4 生成的 GUI 面板规格拆成对象：面板模型负责统筹，指标对象负责显示数字，动作对象负责按钮，试次对象负责一行实验记录。",
        "",
        "| 对象 | 数量 | 职责 |",
        "| --- | --- | --- |",
        "| DataPanelModel | 1 | 统筹数据来源、指标、按钮动作和试次行 |",
        f"| PanelMetric | {len(model.metrics)} | 显示一个关键指标 |",
        f"| PanelAction | {len(model.actions)} | 把用户点击变成方法调用 |",
        f"| TrialRow | {len(model.rows)} | 保存并展示一行 Stroop 试次 |",
        "",
        "## 对象消息",
        "",
    ]
    lines.extend(f"- `{message}`" for message in model.messages())
    lines.extend(
        [
            "",
            f"对象总数：{model.object_count()}",
            f"JSON 交付物：`{JSON_FILE.relative_to(ROOT).as_posix()}`",
            f"预览图：`{PREVIEW.relative_to(ROOT).as_posix()}`",
            "",
            "下一步：如果继续进入 ch6，可以读取这个 JSON，把试次对象整理成表格，再分析正确率、反应时和冲突效应。",
        ]
    )
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str, lines: list[str], color: str) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=22, fill="#FFFFFF", outline=color, width=3)
    draw.rectangle((x1, y1, x2, y1 + 58), fill=color)
    draw.text((x1 + 24, y1 + 17), title, fill="#FFFFFF", font=font(22, True))
    y = y1 + 84
    for line in lines:
        draw.text((x1 + 28, y), line, fill="#162033", font=font(19))
        y += 34


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int]) -> None:
    draw.line((*start, *end), fill="#98A5B8", width=5)
    x2, y2 = end
    draw.polygon([(x2, y2), (x2 - 20, y2 - 12), (x2 - 20, y2 + 12)], fill="#98A5B8")


def draw_preview(model: DataPanelModel) -> None:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1600, 980), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((70, 70, 1530, 910), radius=30, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((120, 115), "GUI Panel Object Model", fill="#162033", font=font(48, True))
    d.text((122, 180), "ch4 panel spec -> ch5 classes and objects", fill="#5F6673", font=font(25))

    box(
        d,
        (120, 260, 510, 505),
        "DataPanelModel",
        ["source", "metrics[]", "actions[]", "rows[]"],
        "#2F6BFF",
    )
    box(
        d,
        (620, 240, 1010, 500),
        "PanelMetric",
        [f"{item.name}: {item.value}" for item in model.metrics[:4]],
        "#24A06B",
    )
    box(
        d,
        (1090, 240, 1480, 500),
        "PanelAction",
        [f"{a.label} -> {a.method_name}()" for a in model.actions[:4]],
        "#F28C28",
    )
    box(
        d,
        (620, 565, 1010, 825),
        "TrialRow",
        [f"#{row.trial_id} {row.word}/{row.ink_color} {row.display_status()}" for row in model.rows[:4]],
        "#7A5AF8",
    )
    box(
        d,
        (1090, 565, 1480, 825),
        "Object Messages",
        model.messages()[:4],
        "#18A9B5",
    )

    arrow(d, (510, 382), (620, 370))
    arrow(d, (510, 382), (620, 690))
    arrow(d, (1010, 370), (1090, 370))
    arrow(d, (1010, 690), (1090, 690))

    d.rounded_rectangle((120, 835, 1480, 880), radius=16, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((150, 846), f"Export: {JSON_FILE.relative_to(ROOT).as_posix()}  |  objects: {model.object_count()}", fill="#8A5A00", font=font(22, True))
    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    spec = ensure_ch4_spec()
    model = build_model(spec)
    write_json(model)
    write_report(model)
    draw_preview(model)
    copy_asset()
    print(f"已生成：{JSON_FILE.relative_to(ROOT)}")
    print(f"已生成：{REPORT_FILE.relative_to(ROOT)}")
    print(f"已生成：{PREVIEW.relative_to(ROOT)}")
    print(f"已同步：{(WEB_DIR / PREVIEW.name).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
