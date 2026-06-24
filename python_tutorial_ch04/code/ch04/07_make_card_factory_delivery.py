"""Generate a learning-output card for the Tkinter card factory project."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CARD = {
    "topic": "工作记忆负荷",
    "question": "为什么界面按钮和提示语会影响学习体验？",
    "summary": [
        "界面越清楚，学生留给任务本身的注意力越多。",
        "按钮、标签和反馈不是装饰，而是在降低认知负荷。",
        "保存后的可见结果，可以让学习从“我好像会了”变成“我确实做出来了”。",
    ],
    "preview_summary": [
        "界面清楚，注意力留给任务。",
        "按钮、标签和反馈降低认知负荷。",
        "保存结果让学习变成作品。",
    ],
    "next_action": "把卡片表单连接到 ch3 的文件整理目录。",
}


def project_root() -> Path:
    here = Path.cwd()
    if (here / "manifest.json").exists() and (here / "assets" / "ch04").exists():
        return here
    return Path(__file__).resolve().parents[2]


ROOT = project_root()
CARDS = ROOT / "cards"
REPORTS = ROOT / "reports"
OUTPUT = ROOT / "output"
WEB_DIR = ROOT / "assets" / "ch04" / "web"
CARD_FILE = CARDS / "working_memory_load_card.md"
REPORT_FILE = REPORTS / "ch04_card_factory_delivery.md"
PREVIEW = OUTPUT / "ch04_card_factory_delivery.png"


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


def write_card() -> None:
    CARDS.mkdir(exist_ok=True)
    lines = [
        f"# {CARD['topic']}",
        "",
        f"**核心问题**：{CARD['question']}",
        "",
        "## 卡片摘要",
        "",
    ]
    lines.extend(f"- {item}" for item in CARD["summary"])
    lines.extend(
        [
            "",
            f"**下一步**：{CARD['next_action']}",
            "",
            "> 这张卡片由第 4 章 GUI 项目生成，用来证明窗口背后真的能留下文件成果。",
        ]
    )
    CARD_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report() -> None:
    REPORTS.mkdir(exist_ok=True)
    card_rel = CARD_FILE.relative_to(ROOT).as_posix()
    preview_rel = PREVIEW.relative_to(ROOT).as_posix()
    lines = [
        "# 第 4 章卡片工厂学习成果",
        "",
        "这份记录展示 GUI 小项目的真实成果：一张可打开、可继续编辑的 Markdown 学习卡片。",
        "",
        "| 项目 | 结果 |",
        "| --- | --- |",
        f"| 卡片主题 | {CARD['topic']} |",
        f"| 核心问题 | {CARD['question']} |",
        f"| 卡片路径 | `{card_rel}` |",
        f"| 预览图 | `{preview_rel}` |",
        "",
        "下一步可以把 Tkinter 表单输入、ch3 文件管理和 ch6 数据分析继续串起来，让卡片工厂从“能保存一张卡”升级成“能整理一批素材”。",
    ]
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def draw_preview() -> None:
    OUTPUT.mkdir(exist_ok=True)
    im = Image.new("RGB", (1500, 930), "#F7F8FB")
    d = ImageDraw.Draw(im)

    d.rounded_rectangle((90, 70, 1410, 850), radius=28, fill="#FFFFFF", outline="#D8E0EC", width=3)
    d.text((150, 125), "卡片工厂学习成果", fill="#162033", font=font(50, True))
    d.text((152, 195), "Tkinter 项目生成的一张真实 Markdown 学习卡片。", fill="#5F6673", font=font(26))

    d.rounded_rectangle((150, 275, 570, 735), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    d.text((190, 315), "输入", fill="#28517A", font=font(28, True))
    d.text((190, 365), "主题", fill="#162033", font=font(24, True))
    d.text((190, 405), CARD["topic"], fill="#162033", font=font(32, True))
    d.text((190, 480), "问题", fill="#162033", font=font(24, True))
    d.text((190, 520), "界面怎样降低", fill="#465263", font=font(25))
    d.text((190, 555), "认知负荷？", fill="#465263", font=font(25))

    d.line((620, 505, 790, 505), fill="#98A5B8", width=6)
    d.polygon([(790, 505), (760, 488), (760, 522)], fill="#98A5B8")

    d.rounded_rectangle((830, 275, 1350, 735), radius=24, fill="#ECFDF3", outline="#8EE3B0", width=3)
    d.text((870, 315), "输出", fill="#166534", font=font(28, True))
    d.text((870, 365), "cards/working_memory_load_card.md", fill="#162033", font=font(24, True))

    y = 430
    for item in CARD["preview_summary"]:
        d.rounded_rectangle((875, y, 1305, y + 48), radius=16, fill="#FFFFFF", outline="#D8E0EC", width=2)
        d.ellipse((900, y + 17, 914, y + 31), fill="#24A06B")
        d.text((930, y + 10), item, fill="#465263", font=font(19))
        y += 70

    d.rounded_rectangle((255, 790, 1245, 845), radius=20, fill="#FFF7E8", outline="#F2B84B", width=2)
    d.text((320, 805), "记录：已生成学习卡片和复盘报告", fill="#8A5A00", font=font(22, True))

    im.save(PREVIEW, optimize=True, quality=95)


def copy_asset() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, WEB_DIR / PREVIEW.name)


def main() -> None:
    write_card()
    write_report()
    draw_preview()
    copy_asset()
    print(f"已生成 {CARD_FILE.relative_to(ROOT)}")
    print(f"已生成 {REPORT_FILE.relative_to(ROOT)}")
    print(f"已生成 {PREVIEW.relative_to(ROOT)}")
    print(f"已同步 {WEB_DIR.relative_to(ROOT) / PREVIEW.name}")


if __name__ == "__main__":
    main()
