#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_semantic_storyboard.py"


def beat(beat_id: str, start: int, end: int, **updates: object) -> dict:
    value = {
        "id": beat_id,
        "start_frame": start,
        "end_frame": end,
        "spoken_text": "示例口播",
        "semantic_object": "坐标与曲线",
        "semantic_action": "曲线快速转为陡峭直线",
        "state_change": "缓慢增长变为直线增长",
        "result_state": "陡峭直线上升",
        "mode": "transformation",
        "density": "sparse",
        "alignment": "center-both",
        "effective_bounds": {"width_ratio": 0.62, "height_ratio": 0.54},
        "primary_visual": f"visual-{beat_id}",
        "core_action_seconds": 0.35,
        "stable_hold_seconds": 0.8,
        "visual_translation": "坐标中曲线在关键词处快速变直并上升",
        "forbidden_substitute": "缓慢进度条",
        "main_composition_changes": True,
        "normal_speed_review": "pass",
    }
    value.update(updates)
    return value


def run(payload: dict, stage: str = "reviewed") -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "storyboard.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(path), "--stage", stage],
            text=True,
            capture_output=True,
            check=False,
        )


canvas = {"width": 1920, "height": 1080, "safe_width": 1728, "safe_height": 864}
valid = {
    "canvas": canvas,
    "beats": [
        beat(
            "b1",
            0,
            30,
            mode="batch",
            batch_id="three-points",
            reveal_order=1,
            retain_until_frame=90,
            group_exit_frame=96,
            density="dense",
            alignment="left",
            effective_bounds={"width_ratio": 0.72, "height_ratio": 0.5},
        ),
        beat(
            "b2",
            30,
            60,
            mode="batch",
            batch_id="three-points",
            reveal_order=2,
            retain_until_frame=90,
            group_exit_frame=96,
            density="dense",
            alignment="left",
            effective_bounds={"width_ratio": 0.72, "height_ratio": 0.5},
        ),
        beat(
            "b3",
            60,
            90,
            mode="batch",
            batch_id="three-points",
            reveal_order=3,
            retain_until_frame=90,
            group_exit_frame=96,
            density="dense",
            alignment="left",
            effective_bounds={"width_ratio": 0.72, "height_ratio": 0.5},
        ),
    ],
}
assert run(valid).returncode == 0, run(valid).stdout

invalid = {
    "canvas": canvas,
    "beats": [
        beat(
            "bad",
            0,
            30,
            primary_visual="corner-microcard",
            density="dense",
            alignment="center-both",
            effective_bounds={"width_ratio": 0.2, "height_ratio": 0.1},
            core_action_seconds=1.5,
            main_composition_changes=False,
            normal_speed_review="pending",
        )
    ],
}
result = run(invalid)
assert result.returncode != 0
for expected in (
    "main_composition_changes",
    "dense content must use left alignment",
    "dense effective width",
    "primary_visual is forbidden",
    "core_action_seconds",
    "normal_speed_review",
):
    assert expected in result.stdout, result.stdout

print("semantic-storyboard-gate: PASS")
