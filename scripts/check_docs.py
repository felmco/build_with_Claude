#!/usr/bin/env python3
"""Check the course Markdown: every ```python block must parse, and every
relative link must point at an existing file.

Usage: python scripts/check_docs.py [root]
Exit code 0 when clean, 1 when problems are found.
"""
import ast
import os
import re
import sys

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}
FENCE = re.compile(r"```python\n(.*?)```", re.S)
LINK = re.compile(r"\]\((?!https?:|#|mailto:)([^)\s#]+)")


def markdown_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def check(root="."):
    problems, blocks = [], 0
    for path in markdown_files(root):
        text = open(path, encoding="utf-8").read()
        for m in FENCE.finditer(text):
            blocks += 1
            try:
                ast.parse(m.group(1))
            except SyntaxError as e:
                line = text[: m.start()].count("\n") + 1 + (e.lineno or 1)
                problems.append(f"{path}:{line}: python block does not parse: {e.msg}")
        for m in LINK.finditer(text):
            target = m.group(1)
            if re.fullmatch(r"[a-z]\w*,?", target):  # prose like "[a, b]", not a link
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), target))):
                problems.append(f"{path}: broken relative link: {target}")
    return blocks, problems


if __name__ == "__main__":
    blocks, problems = check(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"checked {blocks} python blocks")
    for p in problems:
        print(p)
    sys.exit(1 if problems else 0)
