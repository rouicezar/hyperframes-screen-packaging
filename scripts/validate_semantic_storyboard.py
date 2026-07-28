#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


VALID_MODES = {"batch", "singleton", "transformation"}
VALID_DENSITIES = {"dense", "sparse"}
VALID_CONTAINER_STRATEGIES = {"new", "retain-update", "shared-batch"}
VALID_EXIT_MODES = {
    "transition",
    "state-replace",
    "group-exit",
    "hold-to-cut",
    "none-final",
}
FORBIDDEN_PRIMARY = {
    "corner-status-card",
    "corner-microcard",
    "jitter",
    "shake",
    "decorative-progress-bar",
    "background-only-motion",
    "continuous-scan-line",
}


def nonempty(beat: dict, key: str, errors: list[str], prefix: str) -> None:
    if not isinstance(beat.get(key), str) or not beat[key].strip():
        errors.append(f"{prefix}.{key} must be a non-empty string")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate sentence-level semantic enactment before video rendering."
    )
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--stage", choices=("plan", "reviewed"), default="plan")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    path = args.storyboard.resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    notes: list[str] = []

    canvas = data.get("canvas")
    if not isinstance(canvas, dict):
        errors.append("canvas must be an object")
        canvas = {}
    for field in ("width", "height", "safe_width", "safe_height"):
        value = canvas.get(field)
        if not isinstance(value, (int, float)) or value <= 0:
            errors.append(f"canvas.{field} must be positive")

    beats = data.get("beats")
    if not isinstance(beats, list) or not beats:
        errors.append("beats must be a non-empty array")
        beats = []

    seen_ids: set[str] = set()
    previous_end: int | None = None
    batch_members: dict[str, list[tuple[int, dict]]] = {}
    primary_runs: list[tuple[str, int]] = []

    defaults = data.get("beat_defaults", {})
    if not isinstance(defaults, dict):
        errors.append("beat_defaults must be an object when provided")
        defaults = {}

    for index, raw_beat in enumerate(beats):
        if not isinstance(raw_beat, dict):
            errors.append(f"beats[{index}] must be an object")
            continue
        beat = {**defaults, **raw_beat}
        prefix = f"beats[{index}]"
        beat_id = beat.get("id")
        if not isinstance(beat_id, str) or not beat_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif beat_id in seen_ids:
            errors.append(f"duplicate beat id: {beat_id}")
        else:
            seen_ids.add(beat_id)

        start = beat.get("start_frame")
        end = beat.get("end_frame")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            errors.append(f"{prefix} requires integer 0 <= start_frame < end_frame")
        elif previous_end is not None and start < previous_end:
            errors.append(f"{prefix} overlaps the preceding beat")
        if isinstance(end, int):
            previous_end = end

        for key in (
            "spoken_text",
            "spoken_trigger",
            "semantic_object",
            "semantic_action",
            "state_change",
            "result_state",
            "visual_translation",
            "forbidden_substitute",
        ):
            nonempty(beat, key, errors, prefix)

        if beat.get("main_composition_changes") is not True:
            errors.append(f"{prefix}.main_composition_changes must be true")

        mode = beat.get("mode")
        if mode not in VALID_MODES:
            errors.append(f"{prefix}.mode must be one of {sorted(VALID_MODES)}")
        if mode == "batch":
            batch_id = beat.get("batch_id")
            order = beat.get("reveal_order")
            retain = beat.get("retain_until_frame")
            group_exit = beat.get("group_exit_frame")
            if not isinstance(batch_id, str) or not batch_id.strip():
                errors.append(f"{prefix}.batch_id is required for batch mode")
            elif isinstance(order, int):
                batch_members.setdefault(batch_id, []).append((order, beat))
            if not isinstance(order, int) or order < 1:
                errors.append(f"{prefix}.reveal_order must be a positive integer")
            if not isinstance(retain, int) or not isinstance(end, int) or retain < end:
                errors.append(f"{prefix}.retain_until_frame must be >= end_frame")
            if not isinstance(group_exit, int) or not isinstance(retain, int) or group_exit < retain:
                errors.append(f"{prefix}.group_exit_frame must be >= retain_until_frame")
        else:
            for field in ("batch_id", "reveal_order", "retain_until_frame", "group_exit_frame"):
                if field in beat:
                    errors.append(f"{prefix}.{field} is only valid in batch mode")

        density = beat.get("density")
        alignment = beat.get("alignment")
        bounds = beat.get("effective_bounds")
        if density not in VALID_DENSITIES:
            errors.append(f"{prefix}.density must be one of {sorted(VALID_DENSITIES)}")
        if not isinstance(bounds, dict):
            errors.append(f"{prefix}.effective_bounds must be an object")
            bounds = {}
        width_ratio = bounds.get("width_ratio")
        height_ratio = bounds.get("height_ratio")
        if not isinstance(width_ratio, (int, float)) or not 0 < width_ratio <= 1:
            errors.append(f"{prefix}.effective_bounds.width_ratio must be in (0, 1]")
        if not isinstance(height_ratio, (int, float)) or not 0 < height_ratio <= 1:
            errors.append(f"{prefix}.effective_bounds.height_ratio must be in (0, 1]")
        if density == "dense":
            if alignment != "left":
                errors.append(f"{prefix}: dense content must use left alignment")
            if isinstance(width_ratio, (int, float)) and width_ratio < 0.667:
                errors.append(f"{prefix}: dense effective width must be >= 0.667")
        if density == "sparse":
            if alignment != "center-both":
                errors.append(f"{prefix}: sparse content must use center-both alignment")
            if isinstance(width_ratio, (int, float)) and width_ratio < 0.333:
                errors.append(f"{prefix}: sparse effective width must be >= 0.333")
            if isinstance(height_ratio, (int, float)) and height_ratio < 0.333:
                errors.append(f"{prefix}: sparse effective height must be >= 0.333")

        primary = beat.get("primary_visual")
        if not isinstance(primary, str) or not primary.strip():
            errors.append(f"{prefix}.primary_visual must be a non-empty string")
        else:
            normalized = primary.strip().lower()
            if normalized in FORBIDDEN_PRIMARY:
                errors.append(f"{prefix}.primary_visual is forbidden: {primary}")
            if primary_runs and primary_runs[-1][0] == normalized:
                primary_runs[-1] = (normalized, primary_runs[-1][1] + 1)
            else:
                primary_runs.append((normalized, 1))

        action_seconds = beat.get("core_action_seconds")
        if not isinstance(action_seconds, (int, float)) or not 0.2 <= action_seconds <= 0.5:
            errors.append(f"{prefix}.core_action_seconds must be between 0.2 and 0.5")
        entry_seconds = beat.get("component_entry_seconds")
        if not isinstance(entry_seconds, (int, float)) or not 0.2 <= entry_seconds <= 0.55:
            errors.append(
                f"{prefix}.component_entry_seconds must be between 0.2 and 0.55"
            )
        hold_seconds = beat.get("stable_hold_seconds")
        if not isinstance(hold_seconds, (int, float)) or hold_seconds < 0.4:
            errors.append(f"{prefix}.stable_hold_seconds must be at least 0.4")

        container_strategy = beat.get("container_strategy")
        if container_strategy not in VALID_CONTAINER_STRATEGIES:
            errors.append(
                f"{prefix}.container_strategy must be one of "
                f"{sorted(VALID_CONTAINER_STRATEGIES)}"
            )
        if mode == "batch" and container_strategy != "shared-batch":
            errors.append(f"{prefix}: batch mode must use shared-batch container_strategy")
        if mode != "batch" and container_strategy == "shared-batch":
            errors.append(
                f"{prefix}: shared-batch container_strategy is only valid in batch mode"
            )

        exit_mode = beat.get("exit_mode")
        if exit_mode not in VALID_EXIT_MODES:
            errors.append(f"{prefix}.exit_mode must be one of {sorted(VALID_EXIT_MODES)}")
        if mode == "batch" and exit_mode != "group-exit":
            errors.append(f"{prefix}: batch mode must use group-exit exit_mode")
        if mode != "batch" and exit_mode == "group-exit":
            errors.append(f"{prefix}: group-exit exit_mode is only valid in batch mode")
        if exit_mode == "state-replace" and container_strategy != "retain-update":
            errors.append(
                f"{prefix}: state-replace exit_mode requires retain-update "
                "container_strategy"
            )

        review = beat.get("normal_speed_review")
        if args.stage == "reviewed" and review != "pass":
            errors.append(f"{prefix}.normal_speed_review must be pass at reviewed stage")
        elif args.stage == "plan" and review not in {"pending", "pass"}:
            errors.append(f"{prefix}.normal_speed_review must be pending or pass")

    for batch_id, members in batch_members.items():
        members.sort(key=lambda item: item[0])
        orders = [order for order, _ in members]
        if orders != list(range(1, len(orders) + 1)):
            errors.append(f"batch {batch_id}: reveal_order must be contiguous from 1")
        exits = {beat.get("group_exit_frame") for _, beat in members}
        retains = {beat.get("retain_until_frame") for _, beat in members}
        if len(exits) != 1:
            errors.append(f"batch {batch_id}: all members must share group_exit_frame")
        if len(retains) != 1:
            errors.append(f"batch {batch_id}: all members must share retain_until_frame")
        if members:
            final_end = max(beat.get("end_frame", -1) for _, beat in members)
            shared_retain = next(iter(retains))
            if isinstance(shared_retain, int) and shared_retain < final_end:
                errors.append(f"batch {batch_id}: retain_until_frame must include final reveal")

    for primary, count in primary_runs:
        if count >= 3:
            errors.append(
                f"primary visual '{primary}' repeats for {count} consecutive beats; "
                "change the main composition or justify a shared transforming system"
            )

    passed = not errors
    lines = [
        "# Semantic storyboard validation",
        "",
        f"- Storyboard: `{path}`",
        f"- Stage: `{args.stage}`",
        f"- Result: {'PASS' if passed else 'FAIL'}",
        f"- Beats: {len(beats)}",
        f"- Batches: {len(batch_members)}",
        "",
        "## Errors",
        "",
    ]
    lines.extend([f"- {message}" for message in errors] or ["- None"])
    lines.extend(["", "## Notes", ""])
    lines.extend([f"- {message}" for message in notes] or ["- None"])
    report = "\n".join(lines) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    print(report, end="")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
