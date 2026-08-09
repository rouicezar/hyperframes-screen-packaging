# Semantic narrative revision development plan

1. Add the semantic storytelling reference.
2. Add the storyboard validator.
3. Integrate both into the Skill contract and workflow.
4. Add automated passing and failing validator tests.
5. Run the Skill quick validator and repository tests.
6. Install the tested Skill copy.
7. Rebuild Pi from a new semantic storyboard.
8. Render and inspect a representative first-segment prototype.
9. Complete all six inserts, composite once, and validate delivery.
10. Commit and push the Skill only after tests pass.

## Confirmed reference-video learning implementation (2026-07-28)

Completed:

- added exact spoken triggers to the required storyboard contract;
- separated component entrance, semantic action, and readable hold timing;
- added `new`, `retain-update`, and `shared-batch` container strategies;
- added transition, state replacement, group exit, hold-to-cut, and final-hold exit modes;
- documented evidence-first, shared-baseline batch, and before/after migration layouts;
- preserved `style-system.md` as palette authority;
- extended the semantic storyboard validator and its pass/fail fixtures.

Verification:

- `python3 tests/semantic-storyboard-gate/run_tests.py` — PASS
- `python3 tests/manifest-gate/run_tests.py` — PASS, 5/5 cases
- Python compile check for delivery and storyboard validators — PASS
- `git diff --check` — PASS

## Cross-conversation stability calibration implementation (2026-08-09)

Planned sequence:

1. Audit Git source, installed copy, approved-output evidence, and conflicting guidance.
2. Add the portable quality contract, validator, fixtures, and calibration reference.
3. Strengthen delivery EDL checks and align all documentation and component guidance.
4. Run unit gates, Python compilation, Skill quick validation, and a real-artifact forward test.
5. Install the tested distributable tree and prove source/install parity.
6. Commit and push only after every release gate passes.
