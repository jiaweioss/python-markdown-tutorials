"""Chapter 03 artifact: create a path safety receipt for file operations."""

from __future__ import annotations

from pathlib import Path
import hashlib
import runpy
import shutil


ROOT = Path("workspace_ch03")
OUTPUT = ROOT / "output"
RECEIPT = OUTPUT / "ch03_path_safety_receipt.md"
PREVIEW = OUTPUT / "ch03_path_safety_receipt.png"
PREVIEW_ASSET = Path("assets/ch03/web/ch03_path_safety_receipt.png")


REQUIRED_PATHS = [
    ROOT / "inbox",
    ROOT / "organized",
    ROOT / "output",
    ROOT / "organized" / "txt",
    ROOT / "organized" / "csv",
    ROOT / "organized" / "md",
    ROOT / "organized" / "png",
]


def ensure_workspace() -> None:
    script_dir = Path(__file__).resolve().parent
    runpy.run_path(str(script_dir / "01_create_sample_files.py"), run_name="__main__")
    runpy.run_path(str(script_dir / "07_project_archiver.py"), run_name="__main__")
    OUTPUT.mkdir(parents=True, exist_ok=True)


def sha256_prefix(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:12]


def collect_checks() -> list[dict[str, str]]:
    root_resolved = ROOT.resolve()
    cwd = Path.cwd().resolve()
    all_files = [path for path in ROOT.rglob("*") if path.is_file()]
    sample = sorted(all_files)[0] if all_files else None

    checks = [
        {
            "item": "workspace",
            "status": "OK" if ROOT.exists() and ROOT.is_dir() else "FAIL",
            "detail": str(root_resolved),
        },
        {
            "item": "inside cwd",
            "status": "OK" if str(root_resolved).startswith(str(cwd)) else "WATCH",
            "detail": "workspace_ch03 stays inside current project",
        },
        {
            "item": "required folders",
            "status": "OK" if all(path.exists() for path in REQUIRED_PATHS) else "FAIL",
            "detail": f"{sum(path.exists() for path in REQUIRED_PATHS)}/{len(REQUIRED_PATHS)} ready",
        },
        {
            "item": "source files",
            "status": "OK" if any((ROOT / "inbox").glob("*")) else "FAIL",
            "detail": f"{len(list((ROOT / 'inbox').glob('*')))} files in inbox",
        },
        {
            "item": "organized copies",
            "status": "OK" if any((ROOT / "organized").rglob("*.*")) else "FAIL",
            "detail": f"{len(list((ROOT / 'organized').rglob('*.*')))} files organized",
        },
        {
            "item": "utf-8 reports",
            "status": "OK",
            "detail": "reports are written with encoding='utf-8'",
        },
        {
            "item": "hash sample",
            "status": "OK" if sample else "WATCH",
            "detail": f"{sample.relative_to(ROOT).as_posix()} -> {sha256_prefix(sample)}" if sample else "no sample file",
        },
        {
            "item": "delete policy",
            "status": "OK",
            "detail": "this receipt performs no delete or move operation",
        },
    ]
    return checks


def write_markdown(checks: list[dict[str, str]]) -> None:
    lines = [
        "# Chapter 03 Path Safety Receipt",
        "",
        "This receipt checks whether the demo file workspace is ready for safe file operations.",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| `{check['item']}` | **{check['status']}** | {check['detail']} |")

    lines.extend(
        [
            "",
            "## Safety Meaning",
            "",
            "- Confirm the current workspace before copying, moving, or deleting files.",
            "- Keep generated results in `workspace_ch03/output/`.",
            "- Use a dry-run mindset: print paths first, then perform file operations.",
            "",
        ]
    )
    RECEIPT.write_text("\n".join(lines), encoding="utf-8")


def make_preview(checks: list[dict[str, str]]) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False

    def load_font(size: int, bold: bool = False):
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()

    width, height = 1500, 940
    image = Image.new("RGB", (width, height), "#F7F9FC")
    draw = ImageDraw.Draw(image)
    title_font = load_font(54, True)
    h_font = load_font(29, True)
    body_font = load_font(23)
    small_font = load_font(19)
    mono_font = load_font(20)

    ink = "#172033"
    muted = "#5D6678"
    line = "#D9E1EE"
    green = "#24A06B"
    orange = "#F28C28"
    blue = "#2F6BFF"
    red = "#E84C61"

    draw.text((75, 58), "Path Safety Receipt", font=title_font, fill=ink)
    draw.text((80, 128), "Before file operations, prove the workspace, paths, outputs, encoding and hashes.", font=body_font, fill=muted)
    draw.line((80, 178, 1420, 178), fill=line, width=3)

    ok_count = sum(check["status"] == "OK" for check in checks)
    watch_count = sum(check["status"] == "WATCH" for check in checks)
    fail_count = sum(check["status"] == "FAIL" for check in checks)
    metrics = [("OK", ok_count, green), ("WATCH", watch_count, orange), ("FAIL", fail_count, red)]
    for idx, (label, value, color) in enumerate(metrics):
        x = 100 + idx * 300
        draw.rounded_rectangle((x + 8, 220 + 10, x + 250 + 8, 350 + 10), radius=24, fill="#D8DEE9")
        draw.rounded_rectangle((x, 220, x + 250, 350), radius=24, fill="white", outline=color, width=4)
        draw.text((x + 35, 245), label, font=h_font, fill=color)
        draw.text((x + 40, 292), str(value), font=h_font, fill=ink)

    draw.rounded_rectangle((80, 395, 1420, 835), radius=24, fill="white", outline=line, width=2)
    draw.text((120, 432), "Checks", font=h_font, fill=ink)
    for idx, check in enumerate(checks[:8]):
        status = check["status"]
        color = green if status == "OK" else orange if status == "WATCH" else red
        x = 120
        row_y = 492 + idx * 42
        draw.rounded_rectangle((x, row_y, x + 92, row_y + 34), radius=17, fill=color)
        draw.text((x + 24, row_y + 5), status, font=small_font, fill="white")
        draw.text((x + 125, row_y + 3), check["item"], font=body_font, fill=ink)
        detail = check["detail"]
        if len(detail) > 58:
            detail = detail[:55] + "..."
        draw.text((x + 430, row_y + 4), detail, font=mono_font, fill=muted)

    draw.rounded_rectangle((250, 860, 1250, 910), radius=24, fill="#EEF6FF", outline="#9CC8FF", width=3)
    draw.text((318, 873), "Print paths first. Move slowly. Keep every result inside the project workspace.", font=small_font, fill=blue)

    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    image.save(PREVIEW, optimize=True, quality=95)
    PREVIEW_ASSET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREVIEW, PREVIEW_ASSET)
    return True


def main() -> None:
    ensure_workspace()
    checks = collect_checks()
    write_markdown(checks)
    has_preview = make_preview(checks)

    print(f"Wrote {RECEIPT}")
    print(f"Wrote {PREVIEW if has_preview else 'no preview: Pillow not installed'}")
    print("Checks:", ", ".join(f"{item['item']}={item['status']}" for item in checks))


if __name__ == "__main__":
    main()
