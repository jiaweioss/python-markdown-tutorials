"""Generate a small object-model report for the OOP chapter."""
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPORTS = Path("reports")


@dataclass
class LearningCard:
    topic: str
    question: str
    answer: str
    tags: list[str]

    def preview(self) -> str:
        return f"[{self.topic}] {self.question}"


@dataclass
class CardDeck:
    name: str
    cards: list[LearningCard] = field(default_factory=list)

    def add(self, card: LearningCard) -> None:
        self.cards.append(card)

    def summary(self) -> str:
        return f"{self.name}: {len(self.cards)} 张卡片"


@dataclass
class Trial:
    participant: str
    stimulus: str
    response: str
    reaction_time_ms: float

    def is_fast(self) -> bool:
        return self.reaction_time_ms < 500


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def build_model():
    deck = CardDeck("第5章复习盒")
    deck.add(LearningCard("OOP", "类是什么？", "类像图纸，描述对象应该有什么。", ["类", "图纸"]))
    deck.add(LearningCard("OOP", "对象是什么？", "对象是按图纸创建出来的具体实例。", ["对象", "实例"]))
    trial = Trial("S001", "RED/blue", "j", 438.5)
    return deck, trial


def make_markdown(deck: CardDeck, trial: Trial):
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第5章对象模型报告",
        "",
        "## 类与职责",
        "",
        "| 类 | 职责 | 典型属性 | 典型方法 |",
        "| --- | --- | --- | --- |",
        "| LearningCard | 保存一张学习卡片 | topic, question, answer, tags | preview() |",
        "| CardDeck | 管理一组卡片 | name, cards | add(), summary() |",
        "| Trial | 保存一次实验试次 | participant, stimulus, response, reaction_time_ms | is_fast() |",
        "",
        "## 当前对象",
        "",
        f"- {deck.summary()}",
        f"- 试次：{trial.participant}, {trial.stimulus}, {trial.response}, {trial.reaction_time_ms} ms",
        f"- 是否快速反应：{trial.is_fast()}",
    ]
    path = REPORTS / "ch05_oop_model_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def make_preview(deck: CardDeck, trial: Trial):
    REPORTS.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 900), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 830), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "学习卡片对象模型", fill="#162033", font=font(52, True))
    d.text((150, 200), "把散落变量整理成有职责、有状态、有动作的对象。", fill="#5F6673", font=font(30))

    boxes = [
        ("LearningCard", "一张卡片", "topic / question / answer / tags", "#2F6BFF"),
        ("CardDeck", "一组卡片", "name / cards / add() / summary()", "#24A06B"),
        ("Trial", "一次实验试次", "stimulus / response / reaction_time", "#F28C28"),
    ]
    for i, (name, role, attrs, color) in enumerate(boxes):
        x = 150 + i * 400
        d.rounded_rectangle((x, 300, x + 345, 520), radius=22, fill="#F1F5F9", outline="#E2E8F0", width=2)
        d.rounded_rectangle((x, 300, x + 345, 314), radius=7, fill=color)
        d.text((x + 24, 338), name, fill="#162033", font=font(30, True))
        d.text((x + 24, 386), role, fill="#5F6673", font=font(24))
        d.text((x + 24, 430), attrs, fill="#334155", font=font(21))

    d.line((495, 410, 550, 410), fill="#98A5B8", width=5)
    d.polygon([(550, 410), (526, 396), (526, 424)], fill="#98A5B8")
    d.line((895, 410, 950, 410), fill="#98A5B8", width=5)
    d.polygon([(950, 410), (926, 396), (926, 424)], fill="#98A5B8")

    d.rounded_rectangle((150, 600, 1350, 755), radius=22, fill="#EFF6FF", outline="#BFDBFE", width=2)
    d.text((185, 625), deck.summary(), fill="#1D4ED8", font=font(28, True))
    d.text((185, 675), f"Trial: {trial.participant} / {trial.stimulus} / {trial.response} / {trial.reaction_time_ms} ms", fill="#1E3A8A", font=font(25))
    d.text((185, 718), f"快速反应：{trial.is_fast()}", fill="#1E3A8A", font=font(25))
    path = REPORTS / "ch05_oop_model_preview.png"
    im.save(path, optimize=True, quality=95)
    return path


def main():
    deck, trial = build_model()
    report = make_markdown(deck, trial)
    preview = make_preview(deck, trial)
    print("已生成对象模型报告：")
    print(f"- {report}")
    print(f"- {preview}")


if __name__ == "__main__":
    main()
