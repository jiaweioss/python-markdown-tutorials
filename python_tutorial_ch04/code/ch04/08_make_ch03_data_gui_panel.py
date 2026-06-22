"""Build a GUI-style preview panel from the chapter 3 Stroop data handoff."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from statistics import mean

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch04").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
BOOK_ROOT = ROOT.parent
CH3_ROOT = BOOK_ROOT / "python_tutorial_ch03"
CH3_SCRIPT = CH3_ROOT / "code" / "ch03" / "11_make_ch02_stroop_file_handoff.py"
SOURCE_JSON = CH3_ROOT / "workspace_ch03" / "organized" / "json" / "ch02_stroop_dataset_pack.json"

OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch04" / "web"

SPEC_FILE = OUTPUT / "ch04_ch03_data_gui_panel.json"
REPORT_FILE = REPORTS / "ch04_ch03_data_gui_panel.md"
PREVIEW_FILE = OUTPUT / "ch04_ch03_data_gui_panel.png"


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


def ensure_ch3_data() -> dict:
    if SOURCE_JSON.exists():
        return json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    if CH3_SCRIPT.exists():
        subprocess.run([sys.executable, str(CH3_SCRIPT)], cwd=CH3_ROOT, check=False, timeout=20)
    if SOURCE_JSON.exists():
        return json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    return FALLBACK_DATA


def compute_summary(data: dict) -> dict:
    trials = data.get("trials", [])
    summary = dict(data.get("summary", {}))
    if not trials:
        return summary
    summary.setdefault("trial_count", len(trials))
    summary.setdefault("accuracy", sum(1 for t in trials if t.get("correct")) / len(trials))
    summary.setdefault("mean_reaction_time_ms", mean(float(t.get("reaction_time_ms", 0)) for t in trials))
    summary.setdefault("congruent_count", sum(1 for t in trials if t.get("congruent")))
    summary.setdefault("incongruent_count", sum(1 for t in trials if not t.get("congruent")))
    summary.setdefault("participant", trials[0].get("participant", "S001"))
    return summary


def build_spec(data: dict) -> dict:
    summary = compute_summary(data)
    trials = data.get("trials", [])
    return {
        "panel_title": "Stroop 数据浏览面板",
        "source": SOURCE_JSON.relative_to(BOOK_ROOT).as_posix() if SOURCE_JSON.exists() else "fallback/sample",
        "metrics": {
            "participant": summary.get("participant", "S001"),
            "trial_count": int(summary.get("trial_count", 0)),
            "accuracy_percent": round(float(summary.get("accuracy", 0)) * 100, 1),
            "mean_reaction_time_ms": round(float(summary.get("mean_reaction_time_ms", 0)), 1),
            "conflict_trials": int(summary.get("incongruent_count", 0)),
        },
        "actions": ["加载数据", "查看试次", "导出卡片", "生成报告"],
        "trial_preview": trials[:4],
    }


def write_spec(spec: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    SPEC_FILE.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report(spec: dict) -> None:
    REPORTS.mkdir(exist_ok=True)
    metrics = spec["metrics"]
    lines = [
        "# 第4章：ch3 数据 GUI 面板交接报告",
        "",
        "这个报告说明第4章已经接住前面章节的真实成果：ch2 生成 Stroop 数据，ch3 把数据整理到项目文件夹，ch4 把这份数据做成一个可视化控制面板的雏形。",
        "",
        "| 项目 | 结果 |",
        "| --- | --- |",
        f"| 数据来源 | `{spec['source']}` |",
        f"| 被试编号 | {metrics['participant']} |",
        f"| 试次数 | {metrics['trial_count']} |",
        f"| 正确率 | {metrics['accuracy_percent']}% |",
        f"| 平均反应时 | {metrics['mean_reaction_time_ms']} ms |",
        f"| 冲突试次 | {metrics['conflict_trials']} |",
        f"| 面板规格 | `{SPEC_FILE.relative_to(ROOT).as_posix()}` |",
        f"| 面板预览图 | `{PREVIEW_FILE.relative_to(ROOT).as_posix()}` |",
        "",
        "下一步可以把这个静态面板改成真正的 Tkinter 窗口：左侧读取文件，右侧显示试次，按钮负责导出学习卡片或生成报告。",
    ]
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_button(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, fill: str) -> None:
    draw.rounded_rectangle(box, radius=18, fill=fill, outline="#D8E0EC", width=2)
    draw.text((box[0] + 26, box[1] + 18), label, fill="#FFFFFF", font=font(24, True))


def draw_metric(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, value: str, color: str) -> None:
    draw.rounded_rectangle(box, radius=20, fill="#FFFFFF", outline="#D8E0EC", width=2)
    draw.ellipse((box[0] + 24, box[1] + 26, box[0] + 54, box[1] + 56), fill=color)
    draw.text((box[0] + 72, box[1] + 22), title, fill="#5F6673", font=font(20))
    draw.text((box[0] + 72, box[1] + 58), value, fill="#162033", font=font(30, True))


def draw_preview(spec: dict) -> None:
    metrics = spec["metrics"]
    trials = spec["trial_preview"]
    im = Image.new("RGB", (1600, 980), "#ECF2F8")
    d = ImageDraw.Draw(im)

    d.rounded_rectangle((70, 70, 1530, 910), radius=28, fill="#FFFFFF", outline="#CAD7E6", width=3)
    d.rectangle((70, 70, 1530, 150), fill="#162033")
    d.text((120, 92), spec["panel_title"], fill="#FFFFFF", font=font(36, True))
    d.text((950, 102), "ch2 数据 → ch3 文件夹 → ch4 界面", fill="#BBD7FF", font=font(22))

    d.text((120, 178), f"数据来源：{spec['source']}", fill="#5F6673", font=font(22))

    metric_boxes = [
        ((120, 230, 400, 345), "被试", str(metrics["participant"]), "#2F6BFF"),
        ((430, 230, 710, 345), "试次数", str(metrics["trial_count"]), "#24A06B"),
        ((740, 230, 1020, 345), "正确率", f"{metrics['accuracy_percent']}%", "#F28C28"),
        ((1050, 230, 1330, 345), "平均反应时", f"{metrics['mean_reaction_time_ms']} ms", "#7A5AF8"),
    ]
    for box, title, value, color in metric_boxes:
        draw_metric(d, box, title, value, color)

    d.rounded_rectangle((120, 390, 980, 820), radius=24, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((160, 422), "试次预览", fill="#162033", font=font(30, True))
    headers = ["ID", "WORD", "INK", "KEY", "RT", "OK"]
    xs = [165, 255, 430, 600, 705, 845]
    for x, header in zip(xs, headers):
        d.text((x, 475), header, fill="#5F6673", font=font(18, True))

    y = 520
    ink_colors = {"red": "#E84C61", "blue": "#2F6BFF", "green": "#24A06B"}
    for trial in trials:
        d.rounded_rectangle((150, y - 10, 940, y + 48), radius=14, fill="#FFFFFF", outline="#E2E8F0", width=1)
        values = [
            str(trial.get("trial_id", "")),
            str(trial.get("word", "")),
            str(trial.get("ink_color", "")),
            str(trial.get("response_key", "")),
            f"{float(trial.get('reaction_time_ms', 0)):.1f}",
            "yes" if trial.get("correct") else "no",
        ]
        for x, value in zip(xs, values):
            color = ink_colors.get(value.lower(), "#162033") if x == xs[2] else "#162033"
            d.text((x, y), value, fill=color, font=font(22, x in [xs[1], xs[2]]))
        y += 70

    d.rounded_rectangle((1030, 390, 1420, 820), radius=24, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((1070, 422), "面板动作", fill="#162033", font=font(30, True))
    button_colors = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]
    for i, (label, color) in enumerate(zip(spec["actions"], button_colors)):
        draw_button(d, (1080, 490 + i * 78, 1370, 548 + i * 78), label, color)

    d.rounded_rectangle((120, 850, 1420, 895), radius=16, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((150, 860), "下一步：把这个静态预览改成可点击的 Tkinter 数据浏览窗口。", fill="#8A5A00", font=font(22, True))

    PREVIEW_FILE.parent.mkdir(exist_ok=True)
    im.save(PREVIEW_FILE, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW_FILE, WEB_DIR / PREVIEW_FILE.name)


def main() -> None:
    data = ensure_ch3_data()
    spec = build_spec(data)
    write_spec(spec)
    write_report(spec)
    draw_preview(spec)
    copy_asset()
    print(f"已生成：{SPEC_FILE.relative_to(ROOT)}")
    print(f"已生成：{REPORT_FILE.relative_to(ROOT)}")
    print(f"已生成：{PREVIEW_FILE.relative_to(ROOT)}")
    print(f"已同步：{(WEB_DIR / PREVIEW_FILE.name).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
