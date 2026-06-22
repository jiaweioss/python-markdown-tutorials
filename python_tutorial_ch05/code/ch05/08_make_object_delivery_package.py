"""Generate a reusable object-delivery package for chapter 05."""

from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass
class LearningCard:
    topic: str
    question: str
    answer: str
    tags: list[str]

    def preview(self) -> str:
        return f"{self.topic}: {self.question}"


@dataclass
class CardDeck:
    name: str
    cards: list[LearningCard] = field(default_factory=list)

    def add(self, card: LearningCard) -> None:
        self.cards.append(card)

    def summary(self) -> str:
        return f"{self.name}: {len(self.cards)} cards"


@dataclass
class Trial:
    participant: str
    stimulus: str
    response: str
    reaction_time_ms: float

    def is_fast(self) -> bool:
        return self.reaction_time_ms < 500


@dataclass
class ReportBuilder:
    title: str
    sections: list[str] = field(default_factory=list)

    def add_section(self, section: str) -> None:
        self.sections.append(section)


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch05").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch05" / "web"
JSON_FILE = OUTPUT / "ch05_object_delivery_package.json"
REPORT_FILE = REPORTS / "ch05_object_delivery_package.md"
PREVIEW = OUTPUT / "ch05_object_delivery_package.png"


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


def build_package() -> dict:
    deck = CardDeck("科研卡片工厂 OOP 盒")
    deck.add(
        LearningCard(
            "类与对象",
            "为什么类像图纸，对象像作品？",
            "类描述共同结构；对象保存具体状态并执行方法。",
            ["OOP", "class", "object"],
        )
    )
    deck.add(
        LearningCard(
            "组合",
            "为什么 CardDeck 拥有 LearningCard，而不是继承 LearningCard？",
            "卡片盒管理多张卡片，组合比继承更贴近真实职责。",
            ["composition", "responsibility"],
        )
    )
    trial = Trial("S001", "RED/blue", "j", 438.5)
    report = ReportBuilder("第5章对象交付包")
    report.add_section("类模型可以导出为 JSON，供 GUI、文件管理和数据分析继续使用。")
    report.add_section("对象职责越清楚，后续章节复用越轻松。")
    return {
        "deck": {
            "name": deck.name,
            "summary": deck.summary(),
            "cards": [asdict(card) for card in deck.cards],
        },
        "trial": asdict(trial) | {"is_fast": trial.is_fast()},
        "report": asdict(report),
        "handoff": {
            "next_chapter": "ch06 数据分析",
            "next_action": "读取这个 JSON，把卡片和试次对象整理成小表格。",
        },
    }


def write_json(package: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    JSON_FILE.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_report(package: dict) -> None:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第 5 章对象交付包",
        "",
        "这份报告说明：对象模型不只是写在脑子里的结构，也可以被导出成后续章节能继续读取的数据。",
        "",
        "| 项目 | 结果 |",
        "| --- | --- |",
        f"| 卡片盒 | {package['deck']['summary']} |",
        f"| 实验试次 | {package['trial']['participant']} / {package['trial']['reaction_time_ms']} ms / fast={package['trial']['is_fast']} |",
        f"| JSON 交付物 | `{JSON_FILE.relative_to(ROOT).as_posix()}` |",
        f"| 预览图 | `{PREVIEW.relative_to(ROOT).as_posix()}` |",
        "",
        "下一步：ch6 可以读取这个 JSON，把卡片和试次对象整理成表格，再继续做可视化分析。",
    ]
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def panel(draw: ImageDraw.ImageDraw, xy, title: str, lines: list[str], fill: str, outline: str) -> None:
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=24, fill=fill, outline=outline, width=3)
    draw.text((x1 + 34, y1 + 30), title, fill="#162033", font=font(28, True))
    y = y1 + 88
    for line in lines:
        draw.rounded_rectangle((x1 + 34, y, x2 - 34, y + 42), radius=15, fill="#FFFFFF", outline="#D8E0EC", width=2)
        draw.text((x1 + 58, y + 10), line, fill="#465263", font=font(19))
        y += 58


def draw_preview(package: dict) -> None:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "对象交付包", fill="#162033", font=font(50, True))
    d.text((152, 195), "把 Python 对象导出成后续章节能继续读取的数据。", fill="#5F6673", font=font(26))

    panel(
        d,
        (150, 285, 675, 640),
        "对象模型",
        ["LearningCard", "CardDeck", "Trial", "ReportBuilder"],
        "#EEF6FF",
        "#9CC8FF",
    )
    panel(
        d,
        (825, 285, 1350, 640),
        "交付内容",
        [package["deck"]["summary"], "试次：438.5 ms", "导出：JSON", "交给：ch06"],
        "#ECFDF3",
        "#8EE3B0",
    )

    d.line((705, 465, 795, 465), fill="#98A5B8", width=6)
    d.polygon([(795, 465), (765, 448), (765, 482)], fill="#98A5B8")

    d.rounded_rectangle((250, 705, 1250, 765), radius=20, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((330, 722), "output/ch05_object_delivery_package.json", fill="#8A5A00", font=font(25, True))

    d.rounded_rectangle((250, 790, 1250, 845), radius=20, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((405, 805), "报告：reports/ch05_object_delivery_package.md", fill="#465263", font=font(22))

    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    package = build_package()
    write_json(package)
    write_report(package)
    draw_preview(package)
    copy_asset()
    print(f"已生成 {JSON_FILE.relative_to(ROOT)}")
    print(f"已生成 {REPORT_FILE.relative_to(ROOT)}")
    print(f"已生成 {PREVIEW.relative_to(ROOT)}")
    print(f"已同步 {WEB_DIR.relative_to(ROOT) / PREVIEW.name}")


if __name__ == "__main__":
    main()
