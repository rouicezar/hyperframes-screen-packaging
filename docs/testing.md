# Cross-conversation stability calibration test record

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
