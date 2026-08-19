#!/usr/bin/env python3
"""Validate SRT structure, ordering, overlaps, line count, and text length."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TIMECODE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> "
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})$"
)


def milliseconds(parts: tuple[str, ...]) -> int:
    hours, minutes, seconds, millis = map(int, parts)
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("srt", type=Path)
    parser.add_argument("--max-lines", type=int, default=2)
    parser.add_argument("--max-chars", type=int, default=22)
    args = parser.parse_args()

    blocks = re.split(r"\n\s*\n", args.srt.read_text(encoding="utf-8-sig").strip())
    errors: list[str] = []
    previous_end = 0
    for expected, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        if len(lines) < 3:
            errors.append(f"block {expected}: incomplete")
            continue
        if lines[0].strip() != str(expected):
            errors.append(f"block {expected}: unexpected index {lines[0]!r}")
        match = TIMECODE.match(lines[1].strip())
        if match is None:
            errors.append(f"block {expected}: invalid timecode")
            continue
        start = milliseconds(match.groups()[:4])
        end = milliseconds(match.groups()[4:])
        if start < previous_end:
            errors.append(f"block {expected}: overlaps previous caption")
        if end <= start:
            errors.append(f"block {expected}: non-positive duration")
        previous_end = end
        text_lines = lines[2:]
        if len(text_lines) > args.max_lines:
            errors.append(f"block {expected}: more than {args.max_lines} text lines")
        if any(len(line.replace(" ", "")) > args.max_chars for line in text_lines):
            errors.append(f"block {expected}: line exceeds {args.max_chars} characters")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(blocks)} captions, ordered with no overlaps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

