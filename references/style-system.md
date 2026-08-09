# Adaptive visual system

## Brand defaults

- Accent: `#00A9CD`
- Soft cyan: `#5FD2E6`
- Dark stage: `#05090D`
- Surface: `#0C1A20`
- Foreground: `#F5FBFD`
- Secondary: `#8FA7B2`

Do not use orange, amber, or warm-orange neighboring colors. Use additional cool hues only when a real semantic distinction requires them.

## Adapt to source

The cyan system is a brand layer, not a demand for a dark full-frame card on every shot.

- Talking head: use lighter-weight accents, readable captions, and graphics that respect skin tones and clothing.
- Screen recording: use thin focus elements and compact glass callouts.
- Full-frame explanation: use the dark stage and stronger component hierarchy.
- Bright source footage: add local contrast backing rather than dimming the entire shot without reason.

## Layout

- Preserve source ratio unless explicitly changed.
- Center actual rendered pixel bounds, not source coordinates.
- Detect and use negative space.
- Reserve platform UI and subtitle safe zones.
- Keep information hierarchy to at most three levels.
- Avoid PPT-like oversized blocks and decorative grids competing with foreground.
- Do not let badges, checks, icons, or connectors overlap card text or borders.
- Measure effective foreground bounds without backgrounds, grids, glows, subtitle bars, or decorative progress.
- Dense/long compositions are left-aligned and occupy at least two thirds of usable width.
- Sparse/short compositions are centered on both axes and occupy at least one third of usable width and height.
- A wide canvas must not collapse a complete process into a compact center blob. When a short multi-step process fits horizontally, run it in one row and use the safe width.

## Motion

- Compact entrance: 0.25–0.55 seconds.
- Major switch: 0.45–0.75 seconds.
- Complex explanatory draw: 2–3 seconds when narration allows.
- Hold the readable result before exit.
- Use non-linear easing.
- Avoid full-frame sweep flashes and excessive simultaneous reveals.
- Reveal independent information sequentially.
- Prefer a decisive 0.2–0.5 second semantic action followed by a stable hold.
- Do not use jitter, repeated pulse, corner-card re-entry, or a slow progress bar to fake activity.

## Typography

- Prefer PingFang SC, Hiragino Sans GB, or another reliable CJK font.
- Keep one information point on one line when possible.
- Keep one complete information point on one line when measured space permits; never add a forced break for symmetry.
- For user-provided subtitles, reduce type size or recompose first and ask before changing wording.
- Test long subtitles and mixed Chinese/English strings on the final canvas.

## Anti-patterns

- Applying the same composition to portrait and landscape.
- Covering a face, gesture, UI proof, cursor target, or product.
- Adding a graphic that merely repeats the subtitle.
- Leaving an overlay after the scene, crop, subject, or UI state changes.
- Using orange remnants in light, shadow, gradients, or glow.
- Trusting code coordinates without checking output frames.
