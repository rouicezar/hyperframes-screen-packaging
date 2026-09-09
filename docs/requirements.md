# Semantic narrative revision requirements

## Component expression update (2026-09-10)

User request: learn from anything2explainer's components and expression process while keeping our colors unchanged. Improve the existing Skill, retaining HyperFrames, source audio/timing, and current acceptance gates.

Acceptance: provide actionable component/state recipes linked to the existing 20-template router; show how related clauses retain objects and change their roles; include a worked narration example. Keep the current palette file byte-identical. Do not import third-party source, assets, fixed-resolution thresholds, or decorative motion requirements. Verify Skill discovery, existing gates, source/install parity, and record that these recipes still require real-footage prototype review when used.

## Goal

Make spoken-video packaging behave like video storytelling rather than animated slides. The main composition must enact the current spoken meaning and change at sentence-level semantic beats.

## Required behavior

1. Classify each beat as `batch`, `singleton`, or `transformation`.
2. In a batch, reveal items one by one, retain previous items, and exit the batch only after the final item completes.
3. For dense or long content, left-align the composition in the safe zone and make effective foreground content occupy at least two thirds of the usable width.
4. For sparse or short content, center the composition on both axes and make effective foreground content occupy at least one third of usable width and height.
5. Translate narration into object, action, state change, and result. Text repetition is supporting evidence, not the primary visual.
6. Align the meaningful action to the spoken keyword. Complete compact semantic changes in 0.2–0.5 seconds, then hold the readable result.
7. Reject corner-only activity, jitter, repeated status cards, fake progress bars, and decorative continuous motion.
8. Require a representative normal-speed prototype before a long or risky full render.

## Acceptance

- A portable storyboard validator blocks missing semantics, invalid batch lifecycles, inadequate layout coverage, and forbidden substitutes.
- The Skill entrypoint and workflow require the semantic narrative reference and validator.
- Valid and invalid fixtures prove the gate accepts and rejects as intended.
- The Pi re-edit uses the revised protocol and passes both machine and visual review.

## Confirmed reference-video learning requirements (2026-07-28)

The user confirmed that the reusable learning target is the relationship between narration and the visual system, not the reference video's colors or literal content.

Required additions:

1. Every semantic beat identifies the exact spoken trigger that starts the meaningful visual action.
2. Every beat declares component entrance duration, readable hold duration, container continuation strategy, and exit mode.
3. Batch items share one spatial system, retain earlier items, reach a completed group state, and exit together.
4. Repeated examples may preserve one container while replacing its internal state; rebuilding an almost identical scene for every example is discouraged.
5. Evidence layouts bind the claim or metric to its visible source.
6. Before/after narration must produce spatial migration or structural change, not text replacement alone.
7. Component structure, layout, and timing may be learned from a reference; its palette must not override the project's style system.

Acceptance:

- The storyboard validator rejects missing or invalid narration-motion timing fields.
- Tests cover the new fields and container/exit modes.
- `SKILL.md`, `references/semantic-storytelling.md`, and `references/workflow.md` all require the confirmed protocol.

## Cross-conversation stability calibration requirements (2026-08-09)

Goal: a fresh conversation working under `/Users/rouice/Vibecoding视频` must reproduce the approved packaging quality without relying on hidden chat history.

Required additions:

1. The installed Skill and the Git source must expose the same tested production files; source/install drift is a release failure.
2. Every project must create `edit/quality-contract.json` before implementation and validate it at plan, prototype, and final stages.
3. The contract must preserve authoritative subtitle/voiceover text, explicit user timing overrides, frame-boundary authority, single-line information points, and the ban on unnecessary forced wrapping or compact center blobs.
4. User-authorized subtitle ranges may deliberately replace non-black footage, but the EDL must record the authorization, subtitle authority, and integer half-open frame range.
5. Long or high-risk work must include a real-audio, real-subtitle prototype watched at normal speed.
6. Final acceptance must include existing boundary and hero-frame evidence plus explicit visual, subtitle, and layout review passes.
7. Machine validation is necessary but never substitutes for actual-pixel and normal-speed review.

Acceptance:

- A portable quality-contract validator rejects missing authority, forbidden line-break/layout choices, unreviewed prototypes, and absent final evidence.
- Delivery validation rejects overlapping EDL ranges, time/frame disagreement, and unauthorized deliberate full-frame replacement.
- Skill entrypoint, workflow, boundary, subtitle, style, and component-library guidance agree on the same rules.
- Repository tests, Skill quick validation, a real-artifact forward test, install-source parity, commit, and push all pass.

## Peer-layout and connector topology requirements (2026-08-27)

Observed failure: three peer platform cards were placed on different axes around one method card; connector segments were positioned independently, leaving gaps or inconsistent closure; a previous-stage arrow remained visible behind the new scene.

Required additions:

1. Peer components in one semantic group use equal dimensions, a shared baseline or a deliberately symmetric radial system, and optically equal spacing.
2. The completed group balances around the canvas or safe-zone geometric axis; visual weight may not drift because one peer is placed on a separate row without semantic reason.
3. Every connector starts and ends on the actual rendered boundary of its source and target. Gaps, border overlap, line penetration, and mixed closure grammar reject the scene.
4. Connectors express the declared relationship consistently. Peer relationships may use a shared bus or equal branches; they may not imply a false hierarchy.
5. Elements from the preceding state must exit when the new state begins unless the storyboard explicitly retains and reuses them.
6. Final quality validation separately records peer balance, connector closure, and stale-element review.

Acceptance:

- The quality-contract validator rejects contracts that omit topology invariants or final topology review passes.
- Style, semantic, workflow, and calibration references describe the same rule.
- Regression fixtures prove valid contracts pass and the three failure classes block release.
