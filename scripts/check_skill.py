#!/usr/bin/env python3
"""Run dependency-free structural checks for the zdkjianji repository."""

from __future__ import annotations

import argparse
import py_compile
import re
from pathlib import Path


REQUIRED_PATHS = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/caption-rules.md",
    "references/quality-gates.md",
    "references/resolution-policy.md",
    "references/visual-design.md",
    "references/workflow.md",
    "scripts/make_proxy.py",
    "scripts/probe_media.py",
    "scripts/validate_srt.py",
    "assets/knowledge-card/layout.ts",
    "assets/knowledge-card/theme.tsx",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        if not skill.startswith("---\n"):
            errors.append("SKILL.md must start with YAML frontmatter")
        if not re.search(r"(?m)^name:\s*zdkjianji\s*$", skill):
            errors.append("SKILL.md frontmatter must declare name: zdkjianji")
        if not re.search(r"(?m)^description:\s*.+$", skill):
            errors.append("SKILL.md frontmatter must include a description")
        for reference in re.findall(r"\((references/[^)]+\.md)\)", skill):
            if not (root / reference).is_file():
                errors.append(f"broken SKILL.md reference: {reference}")

    for script in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as error:
            errors.append(f"invalid Python script {script.name}: {error.msg}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: zdkjianji repository structure is valid ({root})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

