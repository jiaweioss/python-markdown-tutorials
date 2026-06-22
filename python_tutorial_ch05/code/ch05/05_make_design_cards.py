"""Generate responsibility cards for the OOP chapter."""
from dataclasses import dataclass
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch05").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch05" / "web"


@dataclass
class ResponsibilityCard:
    class_name: str
    metaphor: str
    stores: list[str]
    does: list[str]
    avoid: str

    def markdown_row(self) -> str:
        stores = "、".join(self.stores)
        does = "、".join(self.does)
        return f"| {self.class_name} | {self.metaphor} | {stores} | {does} | {self.avoid} |"


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/msyhbd.ttc") if bold else Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def build_cards() -> list[ResponsibilityCard]:
    return [
        ResponsibilityCard(
            "LearningCard",
            "一张卡片",
            ["主题", "问题", "答案", "标签"],
            ["生成预览", "导出文本"],
            "不要管理整盒卡片",
        ),
        ResponsibilityCard(
            "CardDeck",
            "一个卡片盒",
            ["名称", "卡片列表"],
            ["添加卡片", "统计数量", "筛选标签"],
            "不要保存单次实验反应",
        ),
        ResponsibilityCard(
            "Trial",
            "一次实验试次",
            ["被试", "刺激", "反应", "反应时"],
            ["判断快慢", "生成记录"],
            "不要负责界面和报告",
        ),
        ResponsibilityCard(
            "ReportBuilder",
            "一名报告整理员",
            ["标题", "段落", "图表路径"],
            ["汇总结果", "写入文件"],
            "不要修改原始数据",
        ),
    ]


def make_markdown(cards: list[ResponsibilityCard]) -> Path:
    REPORTS.mkdir(exist_ok=True)
    lines = [
        "# 第5章类职责卡片",
        "",
        "写类之前，先写职责卡片。每个类只回答五个问题：它是谁、像什么、保存什么、会做什么、不该管什么。",
        "",
        "| 类 | 比喻 | 保存什么 | 会做什么 | 不该管什么 |",
        "| --- | --- | --- | --- | --- |",
    ]
    lines.extend(card.markdown_row() for card in cards)
    lines.extend(
        [
            "",
            "## 使用提醒",
            "",
            "- 如果一个类的“不该管什么”写不出来，它很可能会变成万能大类。",
            "- 如果两个类都在保存同一份核心数据，需要检查职责是否重叠。",
            "- 如果继承关系说不清楚，先尝试组合。",
        ]
    )
    path = REPORTS / "ch05_design_cards.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def multiline(draw: ImageDraw.ImageDraw, xy, text: str, fill: str, size: int, max_chars: int = 13, bold: bool = False):
    x, y = xy
    chunks = [text[i : i + max_chars] for i in range(0, len(text), max_chars)]
    for i, chunk in enumerate(chunks):
        draw.text((x, y + i * (size + 9)), chunk, fill=fill, font=font(size, bold))


def make_preview(cards: list[ResponsibilityCard]) -> Path:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1600, 980), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((80, 70, 1520, 910), radius=34, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((140, 125), "类职责卡片", fill="#162033", font=font(56, True))
    d.text((140, 198), "先分清职责，再写 class。OOP 的清爽感，往往从边界开始。", fill="#5F6673", font=font(28))

    palette = ["#2F6BFF", "#24A06B", "#F28C28", "#7A5AF8"]
    for i, card in enumerate(cards):
        col = i % 2
        row = i // 2
        x = 140 + col * 700
        y = 290 + row * 285
        d.rounded_rectangle((x + 8, y + 10, x + 620, y + 235), radius=24, fill="#DEE5EF")
        d.rounded_rectangle((x, y, x + 620, y + 225), radius=24, fill="#F8FAFC", outline="#E2E8F0", width=2)
        d.rounded_rectangle((x, y, x + 620, y + 18), radius=9, fill=palette[i])
        d.text((x + 30, y + 42), card.class_name, fill="#162033", font=font(32, True))
        d.text((x + 30, y + 88), card.metaphor, fill=palette[i], font=font(24, True))
        multiline(d, (x + 30, y + 128), "存：" + "、".join(card.stores), "#334155", 22)
        multiline(d, (x + 335, y + 128), "做：" + "、".join(card.does), "#334155", 22)
        d.text((x + 30, y + 188), "边界：" + card.avoid, fill="#64748B", font=font(20))

    path = OUTPUT / "ch05_design_cards_preview.png"
    im.save(path, optimize=True, quality=95)
    return path


def copy_asset(preview: Path) -> Path:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    target = WEB_DIR / preview.name
    shutil.copyfile(preview, target)
    return target


def main():
    cards = build_cards()
    markdown = make_markdown(cards)
    preview = make_preview(cards)
    web_copy = copy_asset(preview)
    print("已生成类职责卡片：")
    print(f"- {markdown.relative_to(ROOT)}")
    print(f"- {preview.relative_to(ROOT)}")
    print(f"- {web_copy.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
