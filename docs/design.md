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
