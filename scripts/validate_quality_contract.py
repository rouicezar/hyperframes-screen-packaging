#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


STAGES = {"plan": 1, "prototype": 2, "final": 3}
PASS = "pass"


def resolve(base: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate portable video packaging quality gates.")
    parser.add_argument("contract", type=Path)
    parser.add_argument("--stage", choices=STAGES, default="plan")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    data = json.loads(args.contract.read_text(encoding="utf-8"))
    base = args.contract.parent
    errors: list[str] = []

    if data.get("version") != 1:
        errors.append("version must be 1")
    for field in ("source_manifest", "subtitle_authority", "boundary_authority"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be non-empty")

    layout = data.get("layout") if isinstance(data.get("layout"), dict) else {}
    if float(layout.get("dense_min_width_ratio", 0)) < 0.667:
        errors.append("dense_min_width_ratio must be at least 0.667")
    if float(layout.get("sparse_min_width_ratio", 0)) < 0.333 or float(layout.get("sparse_min_height_ratio", 0)) < 0.333:
        errors.append("sparse minimum width and height ratios must be at least 0.333")
    for field in ("single_line_information_points", "no_unnecessary_forced_breaks", "no_center_blob", "actual_pixel_review_required"):
        if layout.get(field) is not True:
            errors.append(f"layout.{field} must be true")

    overrides = data.get("user_overrides", [])
    if not isinstance(overrides, list):
        errors.append("user_overrides must be a list")
    else:
        for index, item in enumerate(overrides):
            if not isinstance(item, dict) or not item.get("spoken_text") or not item.get("instruction"):
                errors.append(f"user_overrides[{index}] must preserve spoken_text and instruction")

    if STAGES[args.stage] >= STAGES["prototype"]:
        prototype = data.get("prototype") if isinstance(data.get("prototype"), dict) else {}
        required = prototype.get("required") is not False
        if not required and not prototype.get("waiver_reason"):
            errors.append("prototype waiver requires waiver_reason")
        if required:
            file_path = resolve(base, prototype.get("file"))
            if file_path is None or not file_path.is_file():
                errors.append("prototype.file must exist")
            if prototype.get("real_audio") is not True:
                errors.append("prototype.real_audio must be true")
            if prototype.get("authoritative_subtitles") is not True:
                errors.append("prototype.authoritative_subtitles must be true")
            if prototype.get("normal_speed_review") != PASS:
                errors.append("prototype.normal_speed_review must be pass")

    if STAGES[args.stage] >= STAGES["final"]:
        review = data.get("final_review") if isinstance(data.get("final_review"), dict) else {}
        for field in ("boundary_evidence", "hero_evidence"):
            evidence = resolve(base, review.get(field))
            if evidence is None or not evidence.exists():
                errors.append(f"final_review.{field} must exist")
        for field in ("visual_review", "subtitle_review", "layout_review"):
            if review.get(field) != PASS:
                errors.append(f"final_review.{field} must be pass")

    passed = not errors
    lines = [
        "# Packaging quality contract validation",
        "",
        f"- Contract: `{args.contract}`",
        f"- Stage: `{args.stage}`",
        f"- Result: {'PASS' if passed else 'FAIL'}",
        "",
        "## Findings",
        "",
    ]
    lines.extend(["- No violations."] if passed else [f"- {error}" for error in errors])
    output = "\n".join(lines) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output, end="")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
