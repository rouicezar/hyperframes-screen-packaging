# Semantic narrative revision design

## Component expression update (2026-09-10)

Add `references/component-expression.md` as design guidance for abstract/process inserts. Each recipe names suitable existing template seeds, visible objects, state progression, retained result, and likely failure. Recipes are construction instructions, not claims of new prebuilt templates. Record recipe choice and object handoff in the existing design document; keep the validated storyboard schema unchanged. Link the reference from the Skill, motion router guidance, and semantic workflow. Use original HyperFrames implementations when a production slot needs a missing primitive.

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

## Cross-conversation stability calibration design (2026-08-09)

### Portable quality contract

Each output owns `edit/quality-contract.json`. It records source/manifest binding, subtitle and boundary authority, explicit user overrides, layout invariants, prototype evidence, and final visual evidence. `scripts/validate_quality_contract.py` exposes three gates:

- `plan`: authority and layout invariants are explicit;
- `prototype`: real audio/subtitles and normal-speed review are complete, or a low-risk waiver has a reason;
- `final`: boundary/hero evidence exists and visual, subtitle, and layout reviews are all `pass`.

### EDL strengthening

Every overlay uses integer `start_frame` and `end_frame` as canonical half-open bounds. Optional seconds must equal frames divided by FPS within a small tolerance. Intervals cannot overlap. A `deliberate-full-frame-replacement` over visible footage requires `user_authorized=true`, `boundary_source=subtitle-authoritative`, and a non-empty authorization note.

### Release parity

The Git source is developed and tested first. Only after all gates pass is the same distributable tree installed at `/Users/rouice/.codex/skills/hyperframes-screen-packaging`. A recursive comparison of `SKILL.md`, `agents`, `assets`, `references`, `scripts`, and `tests` is the release gate.

## Peer-layout and connector topology design (2026-08-27)

Add portable layout invariants to `quality-contract.json`:

- `peer_components_balanced`: peer nodes must share a deliberate geometric system;
- `equal_peer_geometry`: equal semantic peers use equal dimensions and consistent alignment/spacing;
- `connector_closure_required`: connectors terminate on actual rendered component boundaries;
- `stale_elements_must_exit`: a state transition removes undeclared elements from the previous state.

At final stage require independent `pass` values for `balance_review`, `connector_review`, and `stale_element_review`. These are human/actual-pixel gates because a generic DOM overlap scan cannot infer relationship topology or optical balance. HyperFrames layout inspection remains necessary but is not sufficient.

Preferred three-peer pattern on a wide canvas: one centered parent above three equal peer cards on one baseline, connected by one shared horizontal bus and equal vertical branches. Alternative layouts are allowed only when their semantic hierarchy and optical balance are explicit.
