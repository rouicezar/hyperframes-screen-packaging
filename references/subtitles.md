# Semantic Subtitle Rules

## Bottom Subtitle Style

Use `SemanticSubtitleBar` for spoken subtitles:

- Put the subtitle at the lower screen edge. The black strip must touch the frame's bottom edge with no visible gap.
- Add a full-width black strip at the bottom of the frame.
- The strip height should be compact: about one large subtitle line on the current canvas.
- Place subtitle text on the strip and visually close to the lower edge while remaining fully readable.
- Use text color `#00a9cd`.
- Add subtle glow and shadow so the cyan text stays readable.
- Use a single line only. Never wrap and never insert forced line breaks.

For a `1920x1280` canvas, the bundled template uses:

```css
.caption-strip {
  left: 0;
  right: 0;
  bottom: 0;
  height: 112px;
  background: rgba(0, 0, 0, .94);
}

.semantic-caption {
  left: 0;
  right: 0;
  bottom: 18px;
  width: fit-content;
  max-width: 1740px;
  margin: 0 auto;
  color: #00a9cd;
  font-size: 66px;
  line-height: 1;
  white-space: nowrap;
}
```

Scale these values proportionally for other resolutions.

## Source Fidelity

When the user provides a subtitle file or transcript, treat it as the authoritative subtitle source.

- Do not rewrite, summarize, compress, or rephrase user-provided subtitle text.
- Do not change wording for "better semantics" or to match a planned component.
- Only correct obvious typos when the correction is unambiguous.
- If a provided subtitle line is too long for one line, first reduce font size or max-width constraints enough to keep it single-line.
- If it still cannot fit, ask for permission before rewriting. Do not silently summarize.
- Keep timing synchronized to the provided subtitle timing unless there is clear evidence the file itself is mistimed.
- Packaging components must adapt to the subtitle/voiceover timing, not the other way around.

## Semantic Segmentation

Segment captions by meaning, not by arbitrary character count.

- Keep a complete spoken sentence or complete thought in one caption.
- Do not split one semantic sentence into two subtitle placements.
- Natural split points include full sentence boundaries, clear clause boundaries, topic shifts, or before/after contrast.
- Avoid splitting after particles or helper words that make the subtitle feel unfinished.
- If no subtitle file is provided and captions must be created from transcript, segment by complete spoken meaning.
- If a semantic sentence is too long for one line in agent-created captions, first reduce font size or revise layout; only then compress wording while preserving meaning.
- If it still cannot fit, split only at a natural semantic boundary and time each chunk as its own complete thought.

Bad:

```text
看 Agent mail 专门就是
给 AI 工具用的
```

Good:

```text
看 Agent mail 专门就是给 AI 工具用的
```

## Timing

- Align captions to the voiceover phrase they represent.
- Prefer one caption per full spoken meaning.
- Do not make subtitle changes so fast that mobile viewers cannot read them.
- Do not leave a stale subtitle on screen after the spoken meaning has changed.
- Check sampled frames against the subtitle source. Captions must match the exact current line, not a paraphrase or nearby line.
