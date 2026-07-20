---
name: hyperframes-screen-packaging
description: Package landscape or portrait videos—including talking-head footage, screen recordings, mixed person-and-screen edits, tutorials, explainers, and rough cuts—into validated final videos with HyperFrames motion graphics, semantic visual routing, protected subjects and evidence, authoritative subtitles, frame-accurate inserts, and verified audio/video delivery. Use when the user asks to package, beautify, finish, enhance, or review a spoken video or reusable video-packaging workflow.
---

# HyperFrames Screen Packaging

Turn rough-cut spoken videos into polished deliverables. Adapt the workflow to the footage and canvas; never assume the source is a landscape screen recording.

## Read before acting

1. Read `references/style-system.md`.
2. Read `references/footage-archetypes.md`.
3. Read `references/workflow.md`.
4. Read `references/motion-library.md` when abstract, data, process, concept, or blank-screen packaging is needed.
5. Read `references/boundary-and-compositing.md` before inserting full-frame or timed overlays.
6. Read `references/subtitles.md` when subtitles exist or must be created.
7. Read `references/failure-recovery.md` before final rendering.
8. Inspect project-local helpers and existing `edit/` artifacts.

## Non-negotiable contract

- Classify canvas and footage first: landscape/portrait; talking-head/screen/mixed/other.
- Preserve source aspect ratio, frame rate, order, timing, subtitles, and audio unless the user requests editorial changes.
- Protect the evidence appropriate to the footage:
  - talking head: face, eyes, mouth, hands, gestures, and body silhouette;
  - screen recording: visible UI target, cursor, labels, and state;
  - mixed footage: protect both subject and screen evidence.
- Make every graphic express the current spoken meaning. Decoration alone is not packaging.
- Use HyperFrames as the primary motion engine.
- Match suitable abstract/data/process/concept segments against the 20-template router before creating a new component. Do not force those templates onto footage where they do not fit.
- Treat user-provided voiceover and subtitle text as authoritative.
- When black or blank intervals exist, use subtitles to locate their meaning and actual pixels to determine frame-accurate in/out points.
- Do not require black frames. For videos with no black/blank interval, package with safe overlays, reframing, focus treatments, lower thirds, picture-in-picture, B-roll, or deliberate semantic replacement based on the source evidence.
- Default coverage tolerance is zero frames. Allow one frame only when the user explicitly permits slight coverage.
- Use the user's cyan identity (`#00A9CD`) by default and do not introduce orange or warm-orange neighboring colors.
- Complete compact component entrances in 0.25–0.55 seconds; give explanatory graphics enough readable hold time.
- Apply subtitles after every visual overlay.
- Permit only one encoder process per output path. Render to a unique temporary filename, validate it, then replace the final path.
- Do not claim completion until continuous decode, representative frames, boundaries, actual-pixel layout, subtitle placement, and audio integrity pass.

## Stage gates

### 1. Inventory and classify

Create `<video-folder>/edit/`. Run:

```bash
python3 scripts/inspect_source.py <source-video> --srt <subtitle.srt> --output <edit>/source-inspection.json
```

Record:

- landscape or portrait;
- talking-head, screen, mixed, or other;
- subject/evidence safe zones;
- first two seconds;
- black/blank candidates when present.

Choose one route:

- black/blank route: use frame-accurate full-frame replacement where appropriate;
- continuous-picture route: create a coverage map and decide per segment between preserve, overlay, reframe, B-roll, or deliberate replacement.

### 2. Requirements

Write `<edit>/requirements.md` before implementation:

- source specification and footage class;
- target platform and unchanged/changed aspect ratio;
- subtitle authority;
- protected subject/evidence;
- user-provided black-screen phrases, if applicable;
- allowed coverage tolerance;
- brand and output requirements.

### 3. Design

Write `<edit>/design.md` and a segment table. For every segment record:

- spoken meaning;
- time/frame range;
- visual mode;
- component/template and semantic reason;
- subject/evidence safe area;
- entrance, reveal, hold, and exit timing;
- subtitle zone.

Prefer no overlay over one that covers a face, gesture, cursor target, or proof.

For continuous-picture footage, “preserve” does not mean “do nothing.” It may still use subtitles, controlled crop, color/contrast correction, sound-supported emphasis, lightweight accents, or a transition into a semantic insert.

### 4. Slot implementation

Create isolated folders:

```text
<edit>/animations/slot_<id>/
```

Adapt every slot to the final canvas. Portrait layouts must be re-composed, not scaled-down landscape designs. Build independent slots in parallel when possible.

For each HyperFrames slot run:

```bash
npx --yes hyperframes lint .
npx --yes hyperframes validate .
npx --yes hyperframes inspect . --samples 15
npx --yes hyperframes render . -o render.mp4
```

Then continuously decode the slot and inspect entrance, hero, and final frames.

### 5. Composition

Create `<edit>/edl.json`. Use frame-derived timestamps and `setpts=PTS-STARTPTS+START/TB` for timed overlays.

Preserve audio with stream copy when no audio edit is requested. Apply subtitles last. When FFmpeg lacks subtitle filters, use `scripts/render_caption_bar.py`.

### 6. Delivery validation

Render to a unique temporary file:

```bash
python3 scripts/validate_delivery.py \
  --source <source-video> \
  --final <temporary-final> \
  --edl <edit>/edl.json \
  --report <edit>/validation.md
```

Inspect opening, ending, every transition/boundary, each hero frame, and subject/evidence safety. Rename to `<edit>/final.mp4` only after validation passes.

Update `<edit>/project.md`.

## Handoff

Report final path, planning documents, EDL, progress and validation paths, canvas/footage classification, inserted frame ranges, templates/components, codec and duration, decode and audio results, warnings/fallbacks, version-control status, and the next step.
