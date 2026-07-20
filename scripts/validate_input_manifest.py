#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


VALID_SCOPES = {"full", "sample"}
VALID_MODES = {"independent", "mixed"}
VALID_ROLES = {"talking-head", "screen-recording", "mixed-source", "other"}
VALID_AUDIO_ROLES = {"authoritative", "muted", "supporting", "none"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Block invalid source-to-output mappings before video packaging."
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    base = manifest_path.parent
    errors: list[str] = []
    notes: list[str] = []

    scope = data.get("delivery_scope")
    if scope not in VALID_SCOPES:
        fail(errors, f"delivery_scope must be one of {sorted(VALID_SCOPES)}")

    sources = data.get("sources")
    outputs = data.get("outputs")
    if not isinstance(sources, list) or not sources:
        fail(errors, "sources must be a non-empty array")
        sources = []
    if not isinstance(outputs, list) or not outputs:
        fail(errors, "outputs must be a non-empty array")
        outputs = []

    source_by_id: dict[str, dict] = {}
    for index, source in enumerate(sources):
        prefix = f"sources[{index}]"
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.strip():
            fail(errors, f"{prefix}.id must be a non-empty string")
            continue
        if source_id in source_by_id:
            fail(errors, f"duplicate source id: {source_id}")
            continue
        source_by_id[source_id] = source
        if not isinstance(source.get("theme"), str) or not source["theme"].strip():
            fail(errors, f"{prefix}.theme must be explicit")
        if not isinstance(source.get("story_id"), str) or not source["story_id"].strip():
            fail(errors, f"{prefix}.story_id must be explicit")
        if source.get("role") not in VALID_ROLES:
            fail(errors, f"{prefix}.role must be one of {sorted(VALID_ROLES)}")
        if source.get("audio_role") not in VALID_AUDIO_ROLES:
            fail(errors, f"{prefix}.audio_role must be one of {sorted(VALID_AUDIO_ROLES)}")
        file_value = source.get("file")
        if not isinstance(file_value, str) or not file_value.strip():
            fail(errors, f"{prefix}.file must be a non-empty string")
        elif not (base / file_value).resolve().exists():
            fail(errors, f"{prefix}.file does not exist: {file_value}")
        if not isinstance(source.get("deliver"), bool):
            fail(errors, f"{prefix}.deliver must be true or false")

    output_ids: set[str] = set()
    covered_sources: set[str] = set()
    for index, output in enumerate(outputs):
        prefix = f"outputs[{index}]"
        output_id = output.get("id")
        if not isinstance(output_id, str) or not output_id.strip():
            fail(errors, f"{prefix}.id must be a non-empty string")
        elif output_id in output_ids:
            fail(errors, f"duplicate output id: {output_id}")
        else:
            output_ids.add(output_id)

        mode = output.get("mode")
        if mode not in VALID_MODES:
            fail(errors, f"{prefix}.mode must be one of {sorted(VALID_MODES)}")

        source_ids = output.get("source_ids")
        if not isinstance(source_ids, list) or not source_ids:
            fail(errors, f"{prefix}.source_ids must be a non-empty array")
            source_ids = []
        if len(source_ids) != len(set(source_ids)):
            fail(errors, f"{prefix}.source_ids contains duplicates")
        unknown = [source_id for source_id in source_ids if source_id not in source_by_id]
        if unknown:
            fail(errors, f"{prefix}.source_ids contains unknown ids: {unknown}")
        covered_sources.update(source_id for source_id in source_ids if source_id in source_by_id)
        file_value = output.get("file")
        if not isinstance(file_value, str) or not file_value.strip():
            fail(errors, f"{prefix}.file must declare the final output path")

        if mode == "independent" and len(source_ids) != 1:
            fail(errors, f"{prefix}: independent output must use exactly one source")

        if mode == "mixed":
            if len(source_ids) < 2:
                fail(errors, f"{prefix}: mixed output must use at least two sources")
            authorization = output.get("mixed_authorization")
            story_ids = {
                source_by_id[source_id].get("story_id")
                for source_id in source_ids
                if source_id in source_by_id
            }
            if len(story_ids) != 1:
                fail(errors, f"{prefix}: mixed sources must share one story_id")
            if not isinstance(authorization, dict):
                fail(errors, f"{prefix}.mixed_authorization is required")
            else:
                if authorization.get("user_explicit") is not True:
                    fail(errors, f"{prefix}: mixed output requires explicit user authorization")
                if authorization.get("same_story") is not True:
                    fail(errors, f"{prefix}: mixed sources must belong to the same story")
                alignment = authorization.get("alignment_evidence")
                if not isinstance(alignment, str) or len(alignment.strip()) < 12:
                    fail(errors, f"{prefix}: mixed output requires concrete alignment_evidence")
                if authorization.get("alignment_verified") is not True:
                    fail(errors, f"{prefix}: mixed alignment must be verified from actual media")
                audio_master = authorization.get("audio_master_source_id")
                if audio_master not in source_ids:
                    fail(errors, f"{prefix}: audio_master_source_id must name one mixed source")

        output_scope = output.get("scope", scope)
        if output_scope not in VALID_SCOPES:
            fail(errors, f"{prefix}.scope must be one of {sorted(VALID_SCOPES)}")
        if scope == "full" and output_scope != "full":
            fail(errors, f"{prefix}: a full delivery cannot be downgraded to a sample")
        if output_scope == "sample":
            sample_reason = output.get("sample_reason")
            if not isinstance(sample_reason, str) or len(sample_reason.strip()) < 8:
                fail(errors, f"{prefix}: sample output requires sample_reason")

    required_sources = {
        source_id for source_id, source in source_by_id.items() if source.get("deliver") is True
    }
    missing = sorted(required_sources - covered_sources)
    if missing:
        fail(errors, f"deliverable sources without an output: {missing}")

    extra = sorted(covered_sources - required_sources)
    if extra:
        notes.append(f"non-deliverable sources used as supporting material: {extra}")

    passed = not errors
    lines = [
        "# Input manifest validation",
        "",
        f"- Manifest: `{manifest_path}`",
        f"- Result: {'PASS' if passed else 'FAIL'}",
        f"- Delivery scope: `{scope}`",
        f"- Declared sources: {len(sources)}",
        f"- Declared outputs: {len(outputs)}",
        f"- Required source coverage: {len(required_sources - set(missing))}/{len(required_sources)}",
        "",
        "## Errors",
        "",
    ]
    lines.extend([f"- {message}" for message in errors] or ["- None"])
    lines.extend(["", "## Notes", ""])
    lines.extend([f"- {message}" for message in notes] or ["- None"])
    text = "\n".join(lines) + "\n"

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
