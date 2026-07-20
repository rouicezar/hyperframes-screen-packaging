# Visual acceptance requirements

## Goal

Use the supplied real footage to verify that `hyperframes-screen-packaging` works for three independent packaging archetypes:

1. portrait talking head;
2. landscape screen recording;
3. mixed talking head plus screen recording.

## Sources

- Portrait: `粗剪真人口播稿.mov`, 1080 × 1920, 30 fps, 51.033 s.
- Screen: `LLM apps.mp4`, 3840 × 2560, 30 fps, 66.766 s.

`7月20日.mov` has the same duration and stream shape as the portrait source and is not treated as a separate archetype.

## Required deliverables per sample

- final H.264/AAC MP4;
- HyperFrames source slot;
- entrance, hero and final key frames;
- machine-readable probe result;
- decode, geometry, duration, audio, color and visual-protection acceptance result.

## Global acceptance gates

- No orange or orange-adjacent accent is allowed; primary accent is `#00A9CD`.
- Entry motion is 0.25–0.55 s and the first useful visual appears within 2 s.
- No unexpected crop, off-screen card, broken frame, black-gap overlap or duplicate source audio.
- Each final MP4 decodes continuously with FFmpeg.
- Output width, height, frame rate and audio follow the sample design.
- Titles and accents remain inside safe margins.
- Overlays preserve the subject or evidence region appropriate to the archetype.
- Every HyperFrames slot passes lint, validate and inspect before render.

## Archetype-specific gates

### Portrait talking head

- Preserve face, eyes, mouth, chest microphone and active hand gesture.
- Use edge-aligned information rather than a central blocking card.
- Keep original portrait canvas and source audio.

### Landscape screen recording

- Preserve the central document/IDE evidence region.
- Use a restrained focus ring and compact annotation, not a full-screen replacement.
- Keep the source 3:2 canvas and source audio.

### Mixed

- Preserve the screen evidence region and the presenter simultaneously.
- The presenter PiP must remain fully inside the frame and may not cover the highlighted evidence.
- Use one authoritative audio source only.

