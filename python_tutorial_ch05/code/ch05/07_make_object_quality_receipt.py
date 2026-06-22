"""Generate an object-quality receipt for the OOP chapter."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CHECKS = [
    ("单一职责", "通过", "每个类都有清楚边界。"),
    ("数据贴近方法", "通过", "对象把状态和行为放在一起。"),
    ("消息清楚", "通过", "对象协作用命名动作表达。"),
    ("组合优先", "通过", "CardDeck 拥有 cards，而不是继承 card。"),
    ("万能类风险", "留意", "避免一个类同时做文件、GUI、统计和导出。"),
]


def project_root() -> Path:
    here = Path.cwd()
    if (here / "assets" / "ch05").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
OUTPUT = ROOT / "output"
REPORTS = ROOT / "reports"
WEB_DIR = ROOT / "assets" / "ch05" / "web"
RECEIPT = OUTPUT / "ch05_object_quality_receipt.png"
RECEIPT_MD = REPORTS / "ch05_object_quality_receipt.md"


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


def draw_receipt() -> None:
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 70, 1410, 850), radius=26, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "对象质量回执", fill="#162033", font=font(52, True))
    d.text((152, 200), "给卡片工厂对象模型做一次可提交的设计检查。", fill="#5F6673", font=font(27))

    panels = [
        ("LearningCard", "保存一张卡片", "#EEF6FF", "#2F6BFF"),
        ("CardDeck", "管理一组卡片", "#ECFDF3", "#24A06B"),
        ("Trial", "记录一次反应", "#FFF7E8", "#F28C28"),
    ]
    for i, (name, role, fill, color) in enumerate(panels):
        x1 = 150 + i * 415
        d.rounded_rectangle((x1, 270, x1 + 360, 430), radius=24, fill=fill, outline=color, width=2)
        d.text((x1 + 32, 305), name, fill=color, font=font(29, True))
        d.text((x1 + 32, 358), role, fill="#162033", font=font(27, True))

    y = 500
    colors = {"通过": "#24A06B", "留意": "#F28C28"}
    for label, status, note in CHECKS:
        d.rounded_rectangle((150, y, 1350, y + 52), radius=16, fill="#F1F5F9", outline="#E2E8F0", width=2)
        d.rounded_rectangle((180, y + 11, 300, y + 41), radius=15, fill=colors[status])
        d.text((206, y + 15), status, fill="#FFFFFF", font=font(17, True))
        d.text((340, y + 12), label, fill="#162033", font=font(22, True))
        d.text((610, y + 14), note, fill="#465263", font=font(20))
        y += 61

    d.rounded_rectangle((260, 815, 1240, 860), radius=18, fill="#F8FAFC", outline="#D8E0EC", width=2)
    d.text((430, 826), "报告：reports/ch05_object_quality_receipt.md", fill="#465263", font=font(20))
    OUTPUT.mkdir(exist_ok=True)
    im.save(RECEIPT, optimize=True, quality=95)


def write_report() -> None:
    REPORTS.mkdir(exist_ok=True)
    ok_count = sum(1 for _, status, _ in CHECKS if status == "通过")
    watch_count = len(CHECKS) - ok_count
    lines = [
        "# 第5章对象质量回执",
        "",
        "写出 `class` 只是起点。对象质量回执用来检查：每个类是不是有明确职责，对象之间是不是靠清楚消息协作，项目里有没有开始长出万能类。",
        "",
        f"- 已通过检查：{ok_count} 项",
        f"- 需要盯住：{watch_count} 项",
        "",
        "| 检查项 | 状态 | 证据 |",
        "| --- | --- | --- |",
    ]
    for label, status, note in CHECKS:
        lines.append(f"| {label} | {status} | {note} |")
    lines.extend(
        [
            "",
            "下一步建议：一旦某个类同时负责读文件、管界面、做统计和导出报告，就先拆职责，而不是继续往里面塞方法。",
            "这份回执可以和对象模型报告、类职责卡片、对象协作消息图一起提交。",
        ]
    )
    RECEIPT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RECEIPT, WEB_DIR / RECEIPT.name)


def main() -> None:
    draw_receipt()
    write_report()
    copy_asset()
    print(f"已生成 {RECEIPT.relative_to(ROOT)}")
    print(f"已生成 {RECEIPT_MD.relative_to(ROOT)}")
    print(f"已同步 {WEB_DIR.relative_to(ROOT) / RECEIPT.name}")


if __name__ == "__main__":
    main()
