# Frame boundaries and composition

## Authority order

1. User-provided black-screen voiceover text defines semantic intent.
2. Subtitle timing locates the likely interval.
3. Actual pixels define the final boundary.
4. Integer frame indices define the EDL.

Never reverse this order.

## Half-open frame intervals

Represent every insert as `[start_frame, end_frame)`.

For constant frame rate:

```text
start_time = start_frame / fps
end_time = end_frame / fps
frame_count = end_frame - start_frame
```

Render exactly `frame_count` frames. Do not round an end time upward and create one extra frame.

## Boundary verification

Inspect:

- `start_frame - 1`: original non-black or transition frame;
- `start_frame`: first valid replacement frame;
- `end_frame - 1`: last valid replacement frame;
- `end_frame`: first original frame after replacement.

The replacement must never appear on `start_frame - 1` or `end_frame`.

## Overlay timing

Shift each slot from local time zero:

```text
setpts=PTS-STARTPTS+START/TB
```

Use a half-open enable condition:

```text
gte(t, START) * lt(t, END)
```

Do not have two encoder processes write the same output path. Use names such as:

```text
final-attempt-01.mp4
final-attempt-02.mp4
```

Validate the successful attempt, then rename it to `final.mp4`.

## Audio

When the timeline and audio are unchanged, copy the source audio stream. Compare packet MD5 between source and final. If audio is edited, compare decoded duration and listen around boundaries instead.

## Subtitles

Subtitles are the last visual layer. If the local FFmpeg build lacks `subtitles`, `ass`, and `drawtext`, render a separate timed caption-bar video and overlay it last.
