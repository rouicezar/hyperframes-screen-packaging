#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path


BLACK_RE = re.compile(
    r"black_start:(?P<start>\d+(?:\.\d+)?)\s+"
    r"black_end:(?P<end>\d+(?:\.\d+)?)\s+"
    r"black_duration:(?P<duration>\d+(?:\.\d+)?)"
)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def timecode_seconds(value: str) -> float:
    hours, minutes, rest = value.split(":")
    seconds, milliseconds = rest.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000


def read_srt(path: Path | None) -> list[dict]:
    if not path:
        return []
    cues = []
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip())
    for block in blocks:
        lines = block.splitlines()
        timing = next((line for line in lines if "-->" in line), None)
        if not timing:
            continue
        start, end = [timecode_seconds(part.strip()) for part in timing.split("-->")]
        index = lines.index(timing)
        cues.append({"start": start, "end": end, "text": " ".join(lines[index + 1 :])})
    return cues


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect video specs and black-screen candidates.")
    parser.add_argument("video", type=Path)
    parser.add_argument("--srt", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--black-duration", type=float, default=0.08)
    args = parser.parse_args()

    probe = run([
        "ffprobe", "-v", "error",
        "-show_entries",
        "format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
        "-of", "json", str(args.video),
    ])
    if probe.returncode:
        raise SystemExit(probe.stderr)
    spec = json.loads(probe.stdout)
    video_stream = next(stream for stream in spec["streams"] if stream["codec_type"] == "video")
    fps = Fraction(video_stream["r_frame_rate"])
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    canvas = "landscape" if width > height else "portrait" if height > width else "square"

    detected = run([
        "ffmpeg", "-hide_banner", "-i", str(args.video),
        "-vf", f"blackdetect=d={args.black_duration}:pix_th=0.08:pic_th=0.96",
        "-an", "-f", "null", "-",
    ])
    cues = read_srt(args.srt)
    intervals = []
    for match in BLACK_RE.finditer(detected.stderr):
        start = float(match.group("start"))
        end = float(match.group("end"))
        start_frame = round(start * float(fps))
        end_frame = round(end * float(fps))
        overlapping = [
            cue for cue in cues
            if cue["start"] < end and cue["end"] > start
        ]
        intervals.append({
            "candidate_start": start,
            "candidate_end": end,
            "candidate_duration": float(match.group("duration")),
            "candidate_start_frame": start_frame,
            "candidate_end_frame": end_frame,
            "candidate_frame_count": end_frame - start_frame,
            "subtitle_cues": overlapping,
            "requires_frame_confirmation": True,
        })

    result = {
        "source": str(args.video.resolve()),
        "subtitle": str(args.srt.resolve()) if args.srt else None,
        "canvas": canvas,
        "aspect_ratio": f"{width}:{height}",
        "fps": {"numerator": fps.numerator, "denominator": fps.denominator, "float": float(fps)},
        "probe": spec,
        "black_candidates": intervals,
        "notes": [
            "Black detection generates candidates only.",
            "Confirm final boundaries by inspecting actual frames.",
            "No candidates does not mean no packaging; use the continuous-picture route.",
        ],
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
