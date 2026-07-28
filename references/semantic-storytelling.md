# Semantic storytelling protocol

Packaging must enact narration. Movement without a new meaning is not a visual beat.

## 1. Parse meaning before choosing components

For every sentence or independently meaningful clause, write:

1. **object** — what exists on screen;
2. **action** — what happens to it;
3. **state change** — what becomes different;
4. **result** — the readable end state.

Use this counterfactual check: if all explanatory text disappeared, could a viewer still infer the direction of the claim? If not, redesign the primary visual.

Do not begin with a favorite template. Match the sentence to one of these modes:

- `batch`: an announced set, sequence, comparison, list, or grouped argument;
- `singleton`: one independent claim that should appear and leave alone;
- `transformation`: a before/after, cause/effect, growth, compression, branching, convergence, or other state change.

## 2. Batch lifecycle

When narration announces multiple related points:

1. create one stable group container or spatial system;
2. reveal the current item on its keyword;
3. retain every earlier item;
4. show the completed group after the last reveal;
5. exit all group members together at the semantic boundary.

Never remove point one while point two is still being explained. Declare `batch_id`, `reveal_order`, `retain_until_frame`, and `group_exit_frame` in the storyboard.

Use `singleton` only when the claim is not part of an accumulating set. A sequence of sentences is not automatically a batch; shared enumeration or shared conclusion is the test.

## 3. Layout from information density

Measure effective foreground content only. Exclude the background, grid, glow, vignette, scan line, subtitle area, player chrome, and decorative progress indicators.

### Dense or long content

- left-align the primary composition and its internal reading edge;
- keep it inside the usable safe zone;
- occupy at least `0.667` of usable width;
- use the main field, not a corner;
- preserve a clear reading path and at most three hierarchy levels.

### Sparse or short content

- center the group horizontally and vertically;
- align the elements inside the group;
- occupy at least `0.333` of usable width and `0.333` of usable height;
- scale the semantic object, not empty containers, to satisfy coverage.

These are minimum effective bounds, not instructions to stretch every component. Split an unreadable dense scene into meaningful beats instead of shrinking it.

## 4. Expand spoken semantics into action

Translate language into a visual mechanism:

| Spoken meaning | Primary enactment |
|---|---|
| straight-line growth | coordinate axes; a curve rapidly resolves into a steep straight rising line |
| complexity rises | a short chain gains nodes and branches; dependencies visibly multiply |
| calls consume tokens | each call removes token units from a finite budget |
| concise output | verbose blocks compress into a small clear result |
| no filler | redundant bubbles are deleted while the useful core remains |
| hit the target | competing paths disappear and the surviving path reaches a marked target |
| save cost | two equal tasks finish with visibly different remaining budgets |
| three points | three items accumulate in one batch and exit together |
| prerequisite missing | a broken socket blocks flow; installing the dependency closes the circuit |
| direct use | an unnecessary detour is bypassed by a short active path |
| long-running task | the timeline or knowledge structure expands while state is retained |

Prefer object behavior over text duplication. Labels may clarify the enacted relation but cannot be the only relation.

For “straight-line growth,” complete the curve-to-steep-line change in about `0.25–0.45` seconds. A slow chart draw weakens the meaning.

## 5. Timing grammar

Use:

```text
fast meaningful change → stable readable result → next semantic change
```

- align action onset to the spoken keyword or clause;
- complete compact semantic actions in `0.2–0.5` seconds;
- allow longer construction only when the narration itself describes a process;
- hold the result long enough to read;
- use direct, decisive easing;
- do not bounce, tremble, pulse continuously, or repeatedly re-enter the same component.

One sentence normally requires one meaningful change in the main composition. Several short clauses may share a scene when each clause visibly updates the same semantic system.

## 6. Forbidden substitutes

Reject the design when any of these is used to simulate narrative activity:

- repeated lower-right or corner status cards;
- a tiny moving element while the main field stays empty;
- jitter, shake, bounce, or “breathing” as the only change;
- a slow progress bar when narration is not about progress or completion;
- continuous scan lines or decorative sweeps;
- background-only motion;
- text replacement inside an otherwise unchanged composition;
- an oversized empty frame counted as foreground coverage.

Progress bars are permitted only when measurable progress, loading, completion, or quota is the spoken subject.

## 7. Required storyboard fields

Write `<edit>/semantic-storyboard.json`. Every beat must include:

- `id`, `start_frame`, `end_frame`, `spoken_text`;
- `semantic_object`, `semantic_action`, `state_change`, `result_state`;
- `mode`;
- batch fields when `mode=batch`;
- `density`, `alignment`;
- `effective_bounds` measured relative to the usable safe zone;
- `primary_visual`, `core_action_seconds`, `stable_hold_seconds`;
- `visual_translation`, `forbidden_substitute`;
- `main_composition_changes`;
- `normal_speed_review`.

Validate it:

```bash
python3 scripts/validate_semantic_storyboard.py \
  <edit>/semantic-storyboard.json \
  --stage plan \
  --report <edit>/semantic-storyboard-validation.md
```

A failing storyboard blocks animation implementation.

## 8. Prototype and qualitative gate

Before rendering a long or risky sequence:

1. render a representative 10–15 second sample with real narration and subtitles;
2. watch it at normal speed;
3. verify that each spoken beat changes the main composition;
4. verify that batch retention and exit are correct;
5. verify that meaningful objects fill the intended field;
6. reject motion that merely keeps pixels moving.

Contact sheets and frame-difference metrics support review but cannot replace normal-speed viewing. Record the result as `normal_speed_review: "pass"` for each beat only after qualitative review.

Then rerun the validator with `--stage reviewed`. A failed reviewed-stage report blocks the full render.
