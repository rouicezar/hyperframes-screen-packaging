#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_input_manifest.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_case(name: str, expected_code: int) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        case_dir = Path(temporary)
        data = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
        for source in data["sources"]:
            (case_dir / source["file"]).touch()
        manifest = case_dir / "input-manifest.json"
        shutil.copyfile(FIXTURES / name, manifest)
        result = subprocess.run(
            ["python3", str(SCRIPT), str(manifest)],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != expected_code:
            raise AssertionError(
                f"{name}: expected {expected_code}, got {result.returncode}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )


def main() -> None:
    run_case("independent-pass.json", 0)
    run_case("authorized-mixed-pass.json", 0)
    run_case("unauthorized-mixed-fail.json", 1)
    run_case("missing-output-fail.json", 1)
    run_case("full-downgrade-fail.json", 1)
    print("manifest gate: 5/5 cases passed")


if __name__ == "__main__":
    main()
