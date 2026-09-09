# Cross-conversation stability calibration test record

## Component expression update (2026-09-10)

- Manifest fixtures: PASS, 5/5.
- Semantic storyboard fixtures: PASS.
- Quality-contract fixtures: PASS.
- Skill quick validation: PASS.
- `git diff --check`: PASS.
- `references/style-system.md`: unchanged from HEAD; palette preserved.
- Reviewed recipe template IDs against the existing 20-template router; the new guidance explicitly distinguishes construction recipes from prebuilt assets.
- Scope: documentation/workflow improvement only. No new component renders or production-video acceptance are claimed; real-audio prototype and final visual gates remain required when applying the recipes.
- Installed the five changed production files; full source/install production-tree SHA256 parity: PASS (ignoring `.DS_Store` and Python caches). Installed Skill quick validation: PASS with Python 3.12.6; the repository-selected Python lacked PyYAML, so the already available runtime was used.

Date: 2026-08-09

## Automated gates

- Input manifest fixtures: PASS, 5/5.
- Semantic storyboard fixtures: PASS.
- Portable quality-contract fixtures: PASS at plan/prototype/final plus expected failures.
- Python compilation for all validators/tests: PASS.
- Skill quick validation with isolated PyYAML dependency: PASS.
- `git diff --check`: PASS.

## Real-artifact forward test

Baseline: `/Users/rouice/Vibecoding视频/让codex指挥KIMI code做一个我的工作台/edit/final.mp4`

- Portable final quality contract: PASS.
- Continuous decode: PASS.
- Canvas/FPS and full duration: PASS.
- Audio packet MD5 unchanged: PASS.
- Three overlay intervals use exact integer half-open bounds: PASS.
- Slot frame counts: 241/241, 164/164, 78/78.
- Subtitle-authoritative full-frame replacement authorization: PASS for all three slots.
- EDL overlap check: PASS.
- Final SHA256: `ad9107f3e2ffb9a7fe99f88bd6f3a4693cf73bf8272475f243d87ce5bf375081`.

## Release gate

- Tested distributable tree installed at `/Users/rouice/.codex/skills/hyperframes-screen-packaging`: PASS.
- Source/install comparison for `SKILL.md`, `agents`, `assets`, `references`, `scripts`, and `tests`: PASS; the installed tests directory contains only one extra inert `.DS_Store`.
- Installed manifest, semantic-storyboard, and quality-contract gates: PASS.
- Installed Skill quick validation: PASS.

## Peer-layout and connector topology regression (2026-08-27)

- Input manifest fixtures: PASS, 5/5.
- Semantic storyboard fixtures: PASS.
- Quality-contract fixtures: PASS, including expected rejection of missing peer balance, connector closure, and final topology-review passes.
- Python compilation: PASS.
- Skill quick validation with isolated PyYAML: PASS.
- `git diff --check`: PASS.
