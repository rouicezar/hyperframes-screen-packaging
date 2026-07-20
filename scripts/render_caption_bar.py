#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def seconds(value: str) -> float:
    hour, minute, rest = value.split(":")
    second, millisecond = rest.split(",")
    return int(hour) * 3600 + int(minute) * 60 + int(second) + int(millisecond) / 1000


def read_srt(path: Path) -> list[tuple[float, float, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        timing = next((line for line in lines if "-->" in line), None)
        if not timing:
            continue
        start, end = [seconds(part.strip()) for part in timing.split("-->")]
        index = lines.index(timing)
        cues.append((start, end, " ".join(lines[index + 1 :])))
    return cues


def parse_color(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an SRT as a bottom caption-bar video.")
    parser.add_argument("srt", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True, help="Full source-video height.")
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--fps", type=float, required=True)
    parser.add_argument("--bar-height", type=int)
    parser.add_argument("--font", default="/System/Library/Fonts/Hiragino Sans GB.ttc")
    parser.add_argument("--font-size", type=int)
    parser.add_argument("--color", default="#00A9CD")
    args = parser.parse_args()

    bar_height = args.bar_height or max(64, round(args.height * 0.078125))
    font_size = args.font_size or max(28, round(bar_height * 0.46))
    cues = read_srt(args.srt)
    total_frames = round(args.duration * args.fps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{args.width}x{bar_height}", "-r", str(args.fps), "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    cue_index = 0
    for frame in range(total_frames):
        timestamp = frame / args.fps
        while cue_index < len(cues) and timestamp >= cues[cue_index][1]:
            cue_index += 1
        text = ""
        if cue_index < len(cues) and cues[cue_index][0] <= timestamp < cues[cue_index][1]:
            text = cues[cue_index][2]
        image = Image.new("RGB", (args.width, bar_height), (0, 0, 0))
        if text:
            draw = ImageDraw.Draw(image)
            size = font_size
            while size >= max(28, round(font_size * 0.68)):
                font = ImageFont.truetype(args.font, size)
                box = draw.textbbox((0, 0), text, font=font, stroke_width=3)
                if box[2] - box[0] <= args.width * 0.92:
                    break
                size -= 4
            x = (args.width - (box[2] - box[0])) / 2
            y = (bar_height - (box[3] - box[1])) / 2 - box[1]
            draw.text((x, y), text, font=font, fill=parse_color(args.color), stroke_width=3, stroke_fill=(0, 0, 0))
        process.stdin.write(image.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("caption-bar render failed")


if __name__ == "__main__":
    main()
