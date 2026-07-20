#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def probe(path: Path) -> dict:
    result = run([
        "ffprobe", "-v", "error",
        "-show_entries",
        "format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
        "-of", "json", str(path),
    ])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def stream(spec: dict, kind: str) -> dict:
    return next(item for item in spec["streams"] if item["codec_type"] == kind)


def packet_md5(path: Path) -> str | None:
    result = run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"])
    if result.returncode:
        return None
    return result.stdout.strip().removeprefix("MD5=")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a packaged video before final handoff.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--edl", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--allow-spec-change", action="store_true")
    parser.add_argument("--allow-audio-change", action="store_true")
    args = parser.parse_args()

    source_spec = probe(args.source)
    final_spec = probe(args.final)
    source_video = stream(source_spec, "video")
    final_video = stream(final_spec, "video")
    source_duration = float(source_spec["format"]["duration"])
    final_duration = float(final_spec["format"]["duration"])
    fps = float(Fraction(final_video["r_frame_rate"]))
    checks: list[tuple[str, bool, str]] = []

    decode = run(["ffmpeg", "-v", "error", "-i", str(args.final), "-f", "null", "-"])
    checks.append(("continuous decode", decode.returncode == 0 and not decode.stderr.strip(), decode.stderr.strip() or "zero errors"))

    same_canvas = (
        source_video.get("width") == final_video.get("width")
        and source_video.get("height") == final_video.get("height")
        and source_video.get("r_frame_rate") == final_video.get("r_frame_rate")
    )
    checks.append(("canvas and fps", args.allow_spec_change or same_canvas, f"{final_video.get('width')}x{final_video.get('height')} @ {final_video.get('r_frame_rate')}"))
    duration_ok = abs(source_duration - final_duration) <= 1 / fps + 0.001
    checks.append(("duration", duration_ok, f"source={source_duration:.6f}, final={final_duration:.6f}"))

    source_audio_md5 = packet_md5(args.source)
    final_audio_md5 = packet_md5(args.final)
    audio_ok = args.allow_audio_change or (source_audio_md5 is not None and source_audio_md5 == final_audio_md5)
    checks.append(("audio packet MD5", audio_ok, f"source={source_audio_md5}, final={final_audio_md5}"))

    edl_notes = []
    if args.edl:
        edl = json.loads(args.edl.read_text(encoding="utf-8"))
        for overlay in edl.get("overlays", []):
            start = float(overlay["start"])
            end = float(overlay["end"])
            frames = round(end * fps) - round(start * fps)
            file_value = overlay.get("file")
            note = f"{overlay.get('id', '?')}: [{start:.6f}, {end:.6f}) = {frames} frames"
            if file_value:
                slot_path = (args.edl.parent / file_value).resolve()
                if slot_path.exists():
                    slot_duration = float(probe(slot_path)["format"]["duration"])
                    slot_frames = round(slot_duration * fps)
                    ok = slot_frames == frames
                    checks.append((f"slot {overlay.get('id', '?')} frame count", ok, f"EDL={frames}, render={slot_frames}"))
            edl_notes.append(note)

    passed = all(ok for _, ok, _ in checks)
    lines = [
        "# Video packaging validation",
        "",
        f"- Source: `{args.source}`",
        f"- Final: `{args.final}`",
        f"- Result: {'PASS' if passed else 'FAIL'}",
        f"- Final SHA256: `{hashlib.sha256(args.final.read_bytes()).hexdigest()}`",
        "",
        "## Checks",
        "",
    ]
    for name, ok, detail in checks:
        lines.append(f"- [{'x' if ok else ' '}] {name}: {detail}")
    if edl_notes:
        lines.extend(["", "## EDL intervals", "", *[f"- {note}" for note in edl_notes]])
    text = "\n".join(lines) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
