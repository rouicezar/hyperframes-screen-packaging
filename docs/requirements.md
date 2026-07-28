# Semantic narrative revision requirements

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
