# Primary 20-Template Motion Library

## Canonical Paths

- Library: `/Users/rouice/Vibecoding视频/hyperframes-motion-library-main`
- Human workflow: `/Users/rouice/Vibecoding视频/hyperframes-motion-library-main/VIDEO_PACKAGING_INTEGRATION.md`
- Machine router: `/Users/rouice/Vibecoding视频/hyperframes-motion-library-main/packaging-template-router.json`

## Mandatory Selection Rule

Before designing any new packaging graphic, read the router and match the current voiceover meaning against all 20 templates. Reuse the matching template source and render it with the current video's text, data, aspect ratio, duration, and export mode. Default samples are previews, not final insert assets.

Only create a new component when no template matches. If the new component is reusable, add it to the library rather than leaving it isolated in one video project.

## Semantic Groups

- Numbers and data: `bar-chart-grow`, `number-counter`, `line-chart-draw`, `metric-pulse`, `big-number-card`, `before-after-stat`, `horizontal-bar-compare`, `top-rank-list`, `turning-point-line`.
- Evidence and comparison: `source-citation-card`, `stat-duel`, `status-split`, `number-impact`.
- Knowledge explanation: `concept-spotlight`, `three-step-flow`, `myth-fact-swap`, `key-point-marker`, `checklist-pop`, `timeline-scan`, `cause-chain`.

## Production Boundaries

- User-provided black-screen voiceover is the semantic timing source. Use subtitles to locate it, then verify the actual black/non-black boundaries frame by frame.
- Do not let a template follow the subtitle past the end of the real black interval.
- On normal screen recordings, use transparent overlays only when they do not cover UI evidence.
- Preserve source aspect ratio. Re-layout the template for the source canvas instead of stretching a 16:9 sample.
- Center the component group's actual rendered pixel bounds and keep safe margins. Verify with output-frame screenshots, not source coordinates alone.
- Use the cyan design system already stored in the library. Do not restore the previous warm/orange palette.
- Main component entrances should normally complete in 0.25–0.55 seconds.
- Run template validation, representative-frame visual checks, boundary checks, and continuous final-video decode before handoff.
