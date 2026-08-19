#!/usr/bin/env python3
"""Create a lightweight CFR H.264 proxy while preserving aspect ratio."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--height", type=int, choices=(480, 720), default=720)
    parser.add_argument("--fps", type=int, choices=(24, 25, 30, 50, 60), default=30)
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"file does not exist: {args.input}")
    if args.output.exists():
        parser.error(f"refusing to overwrite: {args.output}")
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-hide_banner", "-i", str(args.input),
        "-vf", f"scale=-2:{args.height},fps={args.fps},format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
        "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
        "-movflags", "+faststart", str(args.output),
    ]
    subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

