# Production failure recovery

## Table of contents

1. Glyph or image breakage
2. Corrupt final container
3. Hardware encoder rejection
4. Missing subtitle filters
5. Wrong placement
6. Validation warnings

## 1. Glyph or image breakage

Symptoms:

- fragmented Chinese glyphs;
- blocks or torn regions;
- correct early frames but broken late frames.

Actions:

1. Reject the render.
2. Verify slot source and hero frame separately.
3. Reduce HyperFrames capture workers to one.
4. If late frames alone are unstable, render the validated entrance and hold/freeze a clean hero frame for the remainder.
5. Run continuous decode and inspect the final frame.

Do not label a visibly broken render as a harmless warning.

## 2. Corrupt final container

Symptoms:

- invalid NAL sizes;
- AAC decode errors after audio stream copy;
- MD5 mismatch despite an unchanged audio plan;
- `moov atom not found`.

Likely cause: two processes wrote the same output path or an interrupted process left an incomplete file.

Actions:

1. Stop or wait for all encoders.
2. Confirm the old file size and modification time are stable.
3. Render to a brand-new filename.
4. Run continuous decode.
5. Compare audio packet MD5.
6. Rename only the validated file.

## 3. Hardware encoder rejection

Symptoms:

- VideoToolbox error `-12908`;
- cannot create compression session;
- non-standard 4K canvas such as 3840×2560 is rejected.

Actions:

1. Do not change the source aspect ratio merely to satisfy hardware encoding.
2. Fall back to software `libx265` or `libx264`.
3. Prefer HEVC/hvc1 when compatibility and quality require it.
4. Re-run full decode; software output is not automatically valid.

## 4. Missing subtitle filters

Check:

```bash
ffmpeg -filters | rg 'subtitles|ass|drawtext'
```

If unavailable, use `scripts/render_caption_bar.py` to produce a full-duration black bottom strip with timed cyan text, then overlay it after every other component.

## 5. Wrong placement

Symptoms:

- content is visually shifted right;
- a component runs outside the frame;
- source coordinates look centered but rendered pixels are not.

Actions:

1. Extract a hero frame from the actual rendered video.
2. Measure visible pixel bounds.
3. Re-layout the component group, not just the root coordinate.
4. Keep safe margins and subtitle space.

## 6. Validation warnings

`gsap_studio_edit_blocked` is expected when registered timelines own element positions. It does not excuse layout or render failures.

Treat `timeline_track_too_dense`, missing `.clip`, overflow, contrast, duration mismatch, and decode errors as actionable until resolved or explicitly documented.
