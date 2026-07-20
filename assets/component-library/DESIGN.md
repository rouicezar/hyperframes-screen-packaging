# Palmier Tech Screen Packaging Component Library

## Style Prompt

Build a premium Chinese tech-video packaging system for screen-recording tutorials and AI workflow explainers. The visual language is dark cinematic glassmorphism: floating translucent cards, glowing hairline borders, compact central layouts, precise connector lines, active nodes, pill labels, 3D card depth, and screen-focus overlays. The system must feel like a reusable video component library, not a slide deck. Components should be readable on mobile, rhythmically quick, and able to act out spoken meaning when later synced to narration.

## Colors

- Brand cyan: `#00a9cd` for the current focus, main flow, key edge glow, and primary card accents.
- Soft cyan: `#5fd2e6` for secondary connector lines and hover-like highlights.
- Purple blue: `#7c5cff` for AI analysis, context reading, and reasoning states.
- Success green: `#69d98f` for passed checks, completed nodes, and positive results.
- Brand cyan: `#00a9cd` for key steps, warnings, and attention markers.
- Rose: `#ff5fa2` for pain points, errors, and negative contrast, only in small areas.
- Dark stage: `#06080d`, `#091018`, `#0e1622`.
- Glass fill base: `rgba(255,255,255,.08)` and `rgba(8,18,28,.58)`.
- Colored glass fills: cyan, purple, green, and rose must appear inside the component fill as translucent gradients, not only on borders.

Rules:
- A frame may use one primary highlight plus at most two auxiliary highlight colors.
- No flat saturated blocks. Every colored card, pill, node, line, prototype frame, and connector must have colored translucent fill plus glass material, depth, or glow.
- Bright colors are semi-transparent material fields, not solid backgrounds.
- Backgrounds stay dark and blurred so foreground information remains readable.

## Typography

- Chinese UI text: `"PingFang SC"`, `"Hiragino Sans GB"`, `"Heiti SC"`, sans-serif.
- Technical labels and paths: `"SF Mono"`, `"Menlo"`, monospace.
- Display titles: 72px to 96px, 800 to 900 weight.
- Card titles: 34px to 48px, 750 to 850 weight.
- Body text: 24px to 32px, 400 to 520 weight.
- Pills and node labels: 22px to 28px, 650 to 800 weight.
- Prefer one-line Chinese information points. Compress text before wrapping.

## Layout

- Composition test canvas is `1920x1280`, matching the source video's 3:2 ratio.
- Every component group is centered by its full bounding box, not by a single child.
- Component proportions should respond to the video frame. Avoid square-looking boards on the 3:2 canvas; prefer horizontal cards, wide rows, and spacing that uses the frame without crowding.
- Checklist and multi-component overview layouts should use 3 columns by 2 rows on the 3:2 canvas when showing six items. Do not collapse six components into 2 columns by 3 rows because it over-concentrates content in the middle and wastes horizontal frame space.
- Single cards should normally occupy 34% to 48% of the frame width, with emphasis cards capped at 54%.
- Two-card groups center the combined width plus gap on the screen center.
- Three-card groups use horizontal rhythm, depth, offset, and scale, not oversized square panels.
- Text in cards defaults to centered alignment. Left alignment is reserved for code, file trees, and real screen annotations.
- Screen-focus components can use the video as test material, but the library must remain reusable for other videos.

## Subtitle Bar

- Bottom subtitles sit at the lower screen edge, above a full-width black strip.
- The black strip spans the full frame width and uses a compact vertical height, equivalent to about one large subtitle line on the current canvas.
- Subtitle text floats on the black strip, centered horizontally, with `#00a9cd` text color and a subtle glow/shadow.
- Subtitle text must stay on one line. Do not wrap or insert forced line breaks.
- Subtitle segmentation is semantic: keep each complete spoken sentence or complete thought together. Do not split one semantic sentence into two subtitle placements.
- If a sentence is too long for one line, first rewrite/compress the subtitle while preserving meaning. If it still cannot fit, split only at a natural semantic boundary into separate timed captions.

## Motion

- Every component has an entrance animation.
- Flow nodes must reveal from the left-most node to the right. Connector lines must draw in the same direction, segment by segment; no tail segment may appear first.
- Component entrances should be compact: 0.25s to 0.55s.
- Major component switches should complete in 0.45s to 0.75s.
- Advanced motions such as orbit, depth lift, connector tracing, and magnifier emphasis should last 2s to 3s.
- No static hero state should last more than 6s.
- Use non-linear GSAP eases: `power2.out`, `power3.out`, `expo.out`, `sine.inOut`, and `back.out(1.2)`.

## Component Set

- `GlassCard`: floating glass card with gradient fill, glow edge, inner highlight, and depth shadow.
- `GlassPill`: compact glass capsule for tool names, states, and tags.
- `Node`: circular or rounded node with idle, active, and completed states.
- `ConnectorLine`: animated glowing line with a moving light bead.
- `OrbitCardStack`: 3D surrounding card group where the spoken item can rotate to the front.
- `ScreenFocus`: blurred background video, lifted foreground screen, focus ring, callout, and magnifier.
- `SemanticSubtitleBar`: full-width bottom black strip with one-line cyan subtitle, segmented by full semantic sentences.

## What Not To Do

- Do not continue making full-video packaging before this component library is accepted.
- Do not treat H5 as the final implementation path; it is only fallback or reference.
- Do not use huge PPT-style blocks, flat labels, default blue UI, or generic card grids.
- Do not use unnecessary line breaks in short Chinese information points.
- Do not hide subtitles or reserve no space for future subtitle overlays.
- Do not build components that only work for `cc反向`; that video is only test footage.
- Do not use full-frame sweep-light transitions. They create a flashing illusion and add visual noise. Prefer quieter scene transitions, local component entrances, depth changes, or soft focus shifts.
