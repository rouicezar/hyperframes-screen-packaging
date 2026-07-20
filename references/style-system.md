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

## Motion

- Compact entrance: 0.25–0.55 seconds.
- Major switch: 0.45–0.75 seconds.
- Complex explanatory draw: 2–3 seconds when narration allows.
- Hold the readable result before exit.
- Use non-linear easing.
- Avoid full-frame sweep flashes and excessive simultaneous reveals.
- Reveal independent information sequentially.

## Typography

- Prefer PingFang SC, Hiragino Sans GB, or another reliable CJK font.
- Keep one information point on one line when possible.
- Reduce wording or recompose before allowing awkward wraps.
- Test long subtitles and mixed Chinese/English strings on the final canvas.

## Anti-patterns

- Applying the same composition to portrait and landscape.
- Covering a face, gesture, UI proof, cursor target, or product.
- Adding a graphic that merely repeats the subtitle.
- Leaving an overlay after the scene, crop, subject, or UI state changes.
- Using orange remnants in light, shadow, gradients, or glow.
- Trusting code coordinates without checking output frames.
