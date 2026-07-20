# Acceptance result

## Overall result

**PASS after one required boundary correction.**

All three final samples pass continuous decode, expected geometry, frame rate, exact duration and audio packet identity checks. The final videos and nine visual checkpoints are committed with the HyperFrames sources.

## Results by sample

| Gate | Portrait talking head | Landscape screen | Mixed |
| --- | --- | --- | --- |
| HyperFrames lint | PASS, 0 errors | PASS, 0 errors | PASS, 0 errors |
| HyperFrames validate | PASS | PASS | PASS |
| HyperFrames inspect | PASS, 0 layout issues | PASS, 0 layout issues | PASS, 0 layout issues |
| Continuous decode | PASS | PASS | PASS |
| Canvas / fps | 1080×1920 / 30 | 1920×1280 / 30 | 1920×1080 / 30 |
| Duration | 8.000 s | 10.000 s | 10.000 s |
| Original selected audio | exact packet match | exact packet match | exact packet match |
| 1 fps motion sample | 8/8 unique | 10/10 unique | 10/10 unique |
| Unexpected black interval | none | none | none after correction |
| Warm/orange source token | none | none | none |
| Visual protection | face, mic and active hand preserved | central document evidence remains visible | PiP and screen evidence remain separated |

## Strict visual review

### Portrait

- The presenter remains the dominant layer.
- The top label and left rail use negative space.
- The final conclusion card covers only the lower leg zone, not the face, mouth, microphone or active hand.
- The first useful overlay is visible in under 0.5 s.

### Screen

- The source remains full-size and readable.
- The cyan focus treatment is transparent and does not replace the evidence.
- The annotation is compact and anchored to a screen edge.
- No content is shifted off-screen.

### Mixed

- Presenter and screen are independently bounded.
- Presenter PiP is fully inside frame and does not overlap the central evidence zone.
- Only the screen-recording narration is retained; the PiP is muted.
- The process rail and caption stay in safe margins.

## Defects found and resolved

1. **Sparse intermediate keyframes:** the first screen and mixed renders produced a HyperFrames seek-risk warning. The affected intermediates were re-encoded at 30 fps with a 30-frame GOP and rendered again.
2. **Mixed sample hit a black-screen boundary:** the first mixed selection began at 44.7 s and rendered a black main screen. It was rejected during key-frame review. The accepted interval is 34.5–44.5 s, ending about 0.18 s before the known boundary near 44.68 s.
3. **Nested timed video:** the first mixed HyperFrames source nested a timed video inside a timed PiP wrapper. Lint rejected it. The media element and decorative frame were separated into sibling tracks.
4. **Potential PiP label occlusion:** inspect flagged the label inside the intentional frame overlay. Explicit intentional occlusion metadata was added and the final layout re-inspected with zero issues.

## Non-blocking validator note

HyperFrames emitted contrast advisories for several antialiased white-on-dark labels while reporting zero validation errors. Direct review of all nine exported key frames confirms the labels use opaque navy/black backing, white type and cyan structural accents. The advisories are retained here rather than hidden.

## Checksums

- Portrait: `ffdbcf60467c361b8280ee745692e5e0578a561abe1f230b255da9b37e5f83b8`
- Screen: `bc7308fc6ba0e628b6bc12959149c291d45abbbfbeeb4144339866dd04ee1305`
- Mixed: `5e583da728d4473248224574f6b9c88b73f78cee1da4642d1e169a7630b594a3`

