#!/usr/bin/env python3
"""Lightweight README completeness check for github-repo-publisher."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    ("what this solves", ("what this solves", "problem", "purpose")),
    ("why it matters", ("why it matters", "value", "impact")),
    ("who it is for", ("who it is for", "who uses it", "audience")),
    ("how it works", ("how it works", "architecture", "technical")),
    ("quick start", ("quick start", "getting started", "local development")),
    ("commands", ("commands", "scripts")),
    ("configuration", ("configuration", "environment")),
    ("testing", ("testing", "testing and verification")),
    ("deployment/release", ("deployment", "release")),
    ("troubleshooting", ("troubleshooting", "known issues")),
    ("support", ("support", "help", "ownership", "operational notes")),
    ("security", ("security", "access and data")),
    ("status", ("status", "maintenance status", "roadmap")),
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"lorem ipsum",
    r"PROJECT_NAME",
    r"SHORT_DESCRIPTION",
    r"OWNER_OR_",
    r"Example symptom",
    r"Example cause",
    r"Example fix",
    r"your[-_ ]?(api[-_ ]?)?key",
]


def headings(markdown: str) -> list[str]:
    found: list[str] = []
    for line in markdown.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            found.append(match.group(1).strip().lower())
    return found


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: readme-completeness.py path/to/README.md", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"README not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    found_headings = headings(text)
    lower = "\n".join(found_headings)

    missing = []
    for label, aliases in REQUIRED_SECTIONS:
        if not any(alias in lower for alias in aliases):
            missing.append(label)

    placeholders = []
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            placeholders.append(pattern)

    command_blocks = len(re.findall(r"```(?:bash|sh|shell|zsh)\b", text, flags=re.IGNORECASE))
    score = max(0, 100 - len(missing) * 6 - len(placeholders) * 8)

    print(f"README completeness score: {score}/100")
    print(f"Command blocks: {command_blocks}")
    if missing:
        print("Missing sections:")
        for item in missing:
            print(f"- {item}")
    if placeholders:
        print("Placeholder-like text found:")
        for item in placeholders:
            print(f"- {item}")

    if score < 85 or placeholders:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
