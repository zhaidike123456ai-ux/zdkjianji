#!/usr/bin/env python3
"""Inspect video delivery properties with ffprobe and print recommendations."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if not args.video.is_file():
        parser.error(f"file does not exist: {args.video}")
    if shutil.which("ffprobe") is None:
        raise SystemExit("ffprobe is required")

    command = [
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(args.video),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(result.stdout)
    video = next((s for s in payload["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in payload["streams"] if s["codec_type"] == "audio"), None)
    if video is None:
        raise SystemExit("no video stream found")

    width = int(video["width"])
    height = int(video["height"])
    portrait = height >= width
    hd = [1080, 1920] if portrait else [1920, 1080]
    two_k = [1440, 2560] if portrait else [2560, 1440]
    recommended_height = 720 if height >= 720 else 480
    source_supports_hd = width >= hd[0] and height >= hd[1]
    source_supports_two_k = width >= two_k[0] and height >= two_k[1]
    if source_supports_two_k:
        recommended_master = two_k
        master_options = [two_k, hd]
        upscale_warning = None
    elif source_supports_hd:
        recommended_master = hd
        master_options = [hd]
        upscale_warning = None
    else:
        recommended_master = [width, height]
        master_options = [[width, height], hd]
        upscale_warning = (
            "A 1080P canvas is possible, but scaling cannot restore source detail."
        )
    report = {
        "path": str(args.video.resolve()),
        "video": {
            "codec": video.get("codec_name"),
            "width": width,
            "height": height,
            "frame_rate": video.get("avg_frame_rate"),
            "pixel_format": video.get("pix_fmt"),
            "color_range": video.get("color_range"),
            "color_space": video.get("color_space"),
            "color_transfer": video.get("color_transfer"),
            "color_primaries": video.get("color_primaries"),
        },
        "audio": None if audio is None else {
            "codec": audio.get("codec_name"),
            "sample_rate": audio.get("sample_rate"),
            "channels": audio.get("channels"),
        },
        "duration_seconds": float(payload["format"].get("duration", 0)),
        "recommendation": {
            "proxy_height": recommended_height,
            "recommended_master": recommended_master,
            "master_options": master_options,
            "ask_user_before_render": True,
            "upscale_warning": upscale_warning,
        },
    }

    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"source: {width}x{height} @ {video.get('avg_frame_rate')} fps")
        print(f"duration: {report['duration_seconds']:.3f}s")
        print(
            "color: "
            f"{video.get('pix_fmt')} / {video.get('color_range')} / "
            f"{video.get('color_space')}"
        )
        print(f"proxy: {recommended_height}p CFR")
        print(
            "recommended master: "
            f"{recommended_master[0]}x{recommended_master[1]} "
            "(confirm with user before rendering)"
        )
        if upscale_warning:
            print(f"warning: {upscale_warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
