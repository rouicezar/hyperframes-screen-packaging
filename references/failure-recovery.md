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

## 6. Silent single-frame corruption

Symptoms (observed 2026-08-15 on a 3840x2560 deliverable):

- isolated frames show macroblock garbage, gray corruption blocks, or green smearing;
- the frames before and after are completely normal;
- `ffmpeg -v error -i final -f null -` exits 0 with zero output (the decoder happily decodes corrupted pixels);
- the corruption appears in untouched source-footage regions, and the source frames at the same indices are clean — the damage is introduced by the composition encode, not by the source or the overlays.

Root causes:

1. High-resolution multi-input filter graphs (several `setpts`+`overlay` branches plus a caption-bar overlay and swscale conversions) can race under multi-threaded filtering and hand a corrupted frame to x264, which encodes it without any error. No log, no non-zero exit.
2. Process gap: decode-exit-0 plus a handful of fixed spot frames (first/middle/last/hero/boundary) cannot detect isolated bad frames; a full-timeline pixel scan was never mandatory.

Mandatory prevention (all required before promoting any final):

1. Suppress filter-graph threading in the composition command: add `-filter_complex_threads 1` (with `-threads` still free for x264). This removes the known race source at 4K canvas sizes.
2. Full-timeline corruption scan on the composed final — decode exit codes prove nothing:

   ```bash
   # mid-band frame-delta scan catches partial-frame garbage that whole-frame scene detection misses
   ffmpeg -i final.mp4 -vf "crop=iw:ih*0.4:0:ih*0.35,select='gt(scene,0.10)',metadata=print" -f null - 2>&1 | grep -oE "pts_time:[0-9.]+"
   ffmpeg -i final.mp4 -vf blackdetect=d=0.05:pix_th=0.05 -an -f null - 2>&1 | grep blackdetect
   ```

   Whitelist expected hits (slot boundaries, genuine scene cuts), then extract every remaining hit as a frame and inspect it visually. Any garbage/macroblock/green frame rejects the deliverable; re-compose and rescan.
3. Never treat `continuous decode: zero errors` as evidence of pixel integrity — it only proves the bitstream is parseable.
4. Keep one encoder per unique temp output path (existing rule); a re-compose must reuse the scan before rename.

Repair path (manual or re-compose): replace the damaged frame(s) with neighboring good frames (freeze/interpolate), or re-compose with `-filter_complex_threads 1` and rescan.
