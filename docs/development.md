# Semantic narrative revision development plan

## Component expression update (2026-09-10)

Implemented 12 original expression recipes and a worked four-clause token-budget sequence in `references/component-expression.md`. Linked the recipes from Skill discovery, template selection, semantic planning, and workflow. Kept existing palette, renderer, storyboard schema, and production gates unchanged. No third-party source/assets were imported. Existing manifest, semantic, and quality-contract tests and Skill quick validation pass. Release synchronization and commit/push are recorded in the task delivery.

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

## Peer-layout and connector topology implementation (2026-08-27)

1. Add balance, equal-peer geometry, connector closure, and stale-element exit rules to the Skill contract and references.
2. Extend `validate_quality_contract.py` with plan-stage topology declarations and final-stage topology review passes.
3. Extend quality-contract regression fixtures with missing/failed topology cases.
4. Run all repository tests, Python compilation, Skill quick validation, diff checks, source/runtime parity, then commit and push.
