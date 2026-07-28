# Semantic narrative revision design

## Storyboard contract

Use one JSON object per output with canvas safe-zone dimensions and an ordered list of beats. Every beat declares:

- narration and frame interval;
- semantic object, action, state change, and result;
- narrative mode and batch lifecycle;
- density, alignment, and measured effective foreground bounds;
- primary visual, core action duration, and stable hold;
- forbidden substitute and qualitative review status.

Backgrounds, grids, glows, scan lines, subtitle bars, and decorative progress indicators do not count toward effective foreground coverage.

## Gate design

`scripts/validate_semantic_storyboard.py` reports all violations together and exits non-zero. It validates:

- required fields and ordered non-overlapping intervals;
- batch reveal/retention/group-exit consistency;
- dense and sparse layout thresholds;
- semantic action timing;
- primary visual diversity and forbidden component types;
- completion of normal-speed qualitative review.

## Skill routing

`SKILL.md` loads `references/semantic-storytelling.md` before workflow design. `references/workflow.md` requires a validated storyboard before slot implementation and a representative prototype before full rendering.

## Confirmed narration-driven component design (2026-07-28)

Extend each storyboard beat with:

- `spoken_trigger`: the exact word or short clause that initiates the visual action;
- `component_entry_seconds`: duration of the component's structural entrance;
- `container_strategy`: `new`, `retain-update`, or `shared-batch`;
- `exit_mode`: `transition`, `state-replace`, `group-exit`, `hold-to-cut`, or `none-final`;
- existing `stable_hold_seconds`: readable result time after the meaningful action.

The validator checks field presence, numeric timing bounds, and enum validity. It keeps `core_action_seconds` separate: entrance establishes the component, while the core action enacts the spoken meaning.

The reference-derived timing defaults are guidance rather than palette-specific styling:

- structural entrance: normally `0.25–0.55s`;
- individual card/node reveal: normally `0.20–0.35s`;
- state replacement inside a retained container: normally `0.20–0.30s`;
- readable completed state: normally at least `0.60s`, adjusted to the actual narration window.

Layout and narrative patterns:

- evidence occupies the main field while metrics or interpretation remain secondary and visibly attached;
- batch cards use equal dimensions, a shared baseline/container, cumulative reveal, and a completed group state;
- before/after claims reserve a visible migration path between stable panels;
- one scene has one primary visual subject;
- top metadata, central semantic field, and subtitle zone remain separate layers.
