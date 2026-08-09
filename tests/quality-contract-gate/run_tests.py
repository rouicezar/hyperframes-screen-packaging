#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_quality_contract.py"


def run(payload: dict, stage: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for name in ("manifest.json", "prototype.mp4", "boundaries.jpg", "heroes.jpg"):
            (root / name).write_bytes(b"fixture")
        contract = root / "quality-contract.json"
        contract.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(["python3", str(VALIDATOR), str(contract), "--stage", stage], text=True, capture_output=True, check=False)


valid = {
    "version": 1,
    "source_manifest": "manifest.json",
    "subtitle_authority": "provided-srt",
    "boundary_authority": "subtitle-locate-pixel-confirm-frame",
    "user_overrides": [{"spoken_text": "完整跑通一次", "instruction": "单行横向布局"}],
    "layout": {
        "dense_min_width_ratio": 0.667,
        "sparse_min_width_ratio": 0.333,
        "sparse_min_height_ratio": 0.333,
        "single_line_information_points": True,
        "no_unnecessary_forced_breaks": True,
        "no_center_blob": True,
        "actual_pixel_review_required": True,
    },
    "prototype": {
        "required": True,
        "file": "prototype.mp4",
        "real_audio": True,
        "authoritative_subtitles": True,
        "normal_speed_review": "pass",
    },
    "final_review": {
        "boundary_evidence": "boundaries.jpg",
        "hero_evidence": "heroes.jpg",
        "visual_review": "pass",
        "subtitle_review": "pass",
        "layout_review": "pass",
    },
}

assert run(valid, "plan").returncode == 0
assert run(valid, "prototype").returncode == 0
assert run(valid, "final").returncode == 0

invalid = json.loads(json.dumps(valid))
invalid["layout"]["no_unnecessary_forced_breaks"] = False
invalid["layout"]["no_center_blob"] = False
invalid["prototype"]["normal_speed_review"] = "pending"
invalid["final_review"]["layout_review"] = "pending"
result = run(invalid, "final")
assert result.returncode != 0
for expected in ("no_unnecessary_forced_breaks", "no_center_blob", "normal_speed_review", "layout_review"):
    assert expected in result.stdout, result.stdout

print("quality-contract-gate: PASS")
