from __future__ import annotations

import ast
import re
import sys
from collections import defaultdict
from pathlib import Path

from function_reference import FUNCTION_REFERENCES, references_for_chapter


ROOT = Path(__file__).resolve().parents[1]
PYTHON_FENCE = re.compile(r"```(?:python|py)\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)


def chapter_index(path: Path) -> int:
    return int(path.name.removeprefix("python_tutorial_ch"))


def dotted_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    if isinstance(node, ast.Call):
        return dotted_name(node.func)
    return ""


def parse_source(source: str, label: str) -> ast.AST | None:
    try:
        return ast.parse(source)
    except SyntaxError:
        # A few teaching snippets intentionally show incomplete lines or errors.
        print(f"SKIP non-runnable teaching snippet: {label}")
        return None


def collect_tree(tree: ast.AST, calls: set[str], definitions: set[str]) -> None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.add(node.name)
        elif isinstance(node, ast.Call):
            name = dotted_name(node.func)
            if name:
                calls.add(name)


def reference_tokens() -> set[str]:
    tokens: set[str] = set()
    for reference in FUNCTION_REFERENCES:
        for part in reference.name.split("/"):
            identifiers = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", part)
            if identifiers:
                tokens.add(identifiers[-1])
    return tokens


def main() -> int:
    chapter_calls: dict[int, set[str]] = defaultdict(set)
    chapter_definitions: dict[int, set[str]] = defaultdict(set)
    parse_skips = 0

    chapter_dirs = sorted(ROOT.glob("python_tutorial_ch[0-9][0-9]"))
    for folder in chapter_dirs:
        index = chapter_index(folder)
        for markdown_path in folder.glob("chapters/*.md"):
            text = markdown_path.read_text(encoding="utf-8")
            for block_number, source in enumerate(PYTHON_FENCE.findall(text), start=1):
                tree = parse_source(source, f"{markdown_path.name} block {block_number}")
                if tree is None:
                    parse_skips += 1
                    continue
                collect_tree(tree, chapter_calls[index], chapter_definitions[index])
        # Only audit learner-facing scripts. Figure builders and validation tools
        # use implementation APIs that never appear in the lesson workflow.
        for script_path in folder.glob("code/**/*.py"):
            if "__pycache__" in script_path.parts:
                continue
            tree = parse_source(
                script_path.read_text(encoding="utf-8-sig"),
                str(script_path.relative_to(ROOT)),
            )
            if tree is None:
                parse_skips += 1
                continue
            collect_tree(tree, chapter_calls[index], chapter_definitions[index])

    documented = reference_tokens()
    unresolved: dict[int, list[str]] = {}
    for index, calls in sorted(chapter_calls.items()):
        missing = sorted(
            call
            for call in calls
            if call.rsplit(".", 1)[-1] not in documented
            and call.rsplit(".", 1)[-1] not in chapter_definitions[index]
        )
        if missing:
            unresolved[index] = missing

    total_calls = sum(len(calls) for calls in chapter_calls.values())
    print(f"Function reference entries: {len(FUNCTION_REFERENCES)}")
    print(f"Unique chapter call spellings: {total_calls}")
    print(f"Non-runnable teaching snippets skipped: {parse_skips}")
    for index in range(11):
        print(
            f"ch{index:02d}: {len(chapter_calls[index])} calls, "
            f"{len(references_for_chapter(index))} reference entries"
        )

    if unresolved:
        print("\nUnresolved calls:")
        for index, calls in unresolved.items():
            print(f"ch{index:02d}: {', '.join(calls)}")
        return 1

    print("All calls are covered by the function library or defined in their chapter.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
