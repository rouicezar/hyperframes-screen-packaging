# End-to-end packaging workflow

## Table of contents

1. Project layout
2. Input discovery
3. Source relationship and delivery contract
4. Source analysis
5. Choose black/blank or continuous-picture route
6. Semantic planning
7. Implementation
8. Composition
9. Self-evaluation
10. Delivery

## 1. Project layout

Keep source files untouched. Place all generated work inside the video's `edit/` directory:

```text
<video-folder>/
├── <source-video>
├── <subtitle-file>
└── edit/
    ├── requirements.md
    ├── design.md
    ├── project.md
    ├── input-manifest.json
    ├── input-manifest-validation.md
    ├── source-inspection.json
    ├── edl.json
    ├── compose-filter.txt
    ├── animations/slot_<id>/
    ├── verify/
    ├── validation.md
    ├── preview.mp4
    └── final.mp4
```

## 2. Input discovery

Search the video folder before asking the user:

- source video and alternate versions;
- SRT, ASS, transcript, or voiceover notes;
- explicit black-screen phrases;
- previous `edit/` plans and rendered slots;
- local helpers.

The user often supplies black-screen phrases in chat. Preserve them verbatim in `requirements.md`.

## 3. Source relationship and delivery contract

Do not treat a folder as one edit merely because it contains multiple videos. Build a source map before visual classification:

| Source | Topic | Audio ownership | Role | Deliver? | Target output |
|---|---|---|---|---|---|
| file A | one-line claim | own / mute / external | talking-head / screen / other | true / false | output id |

Default rules:

- one source file is one independent work;
- similar canvas, matching duration, or complementary footage type is not proof of a relationship;
- a talking-head source plus a screen recording is not automatically mixed footage;
- do not combine unrelated sources to satisfy “test portrait, screen, and mixed”;
- if no same-story source pair exists, mark the mixed test unavailable;
- do not use a short sample when the request says full, complete, entire, final, or equivalent.

Create `input-manifest.json`:

```json
{
  "delivery_scope": "full",
  "sources": [
    {
      "id": "source-a",
      "file": "../source-a.mp4",
      "theme": "explicit one-line topic",
      "story_id": "stable-story-id",
      "role": "talking-head",
      "audio_role": "authoritative",
      "deliver": true
    }
  ],
  "outputs": [
    {
      "id": "source-a-final",
      "file": "finals/source-a-final.mp4",
      "source_ids": ["source-a"],
      "mode": "independent",
      "scope": "full"
    }
  ]
}
```

For `mode=mixed`, additionally require:

```json
{
  "mixed_authorization": {
    "user_explicit": true,
    "same_story": true,
    "alignment_evidence": "Verified slate plus matching speech landmarks near start, middle, and end",
    "alignment_verified": true,
    "audio_master_source_id": "source-a"
  }
}
```

For mixed sources, verify the claimed alignment against actual media. Matching duration alone is insufficient. Use a slate/audio transient and distributed transcript or waveform landmarks to detect offset and drift. Declare exactly one audio master so duplicate narration cannot survive composition.

Run `scripts/validate_input_manifest.py`. A failing manifest blocks requirements sign-off and all rendering.

## 4. Source analysis

Use `scripts/inspect_source.py` for the first pass. Confirm:

- duration, resolution, frame rate, aspect ratio, codecs;
- black/blank candidates;
- subtitle lines overlapping every candidate;
- first two seconds;
- protected UI regions;
- cursor and page-state changes.

Black detection is only a candidate generator and is optional. Examine frames immediately before, at, and after every detected boundary. Snap confirmed times to integer frames:

```text
time = frame_index / fps
slot_frames = end_frame - start_frame
```

Use a half-open interval `[start_frame, end_frame)`.

## 5. Choose the route

### Black/blank route

Use when real empty frames exist. Full-frame semantic replacement is normally safe inside the confirmed interval.

### Continuous-picture route

Use when the picture never goes black or the visible footage remains meaningful throughout.

Create a coverage map:

| Mode | Use when |
|---|---|
| preserve | face, gesture, UI proof, product, or action is already valuable |
| lightweight overlay | negative space exists and a short cue improves comprehension |
| focus/reframe | the evidence is present but too small or visually weak |
| picture-in-picture | person and screen/product both matter |
| B-roll insert | narration describes something not visible in the source |
| deliberate full-frame replacement | an abstract explanation is more valuable than the source at that moment and the user has authorized replacement |
| subtitle/grade only | any additional graphic would reduce clarity |

No black frames does not mean no packaging. It means packaging must be evidence-aware rather than boundary-driven.

## 6. Semantic planning

Create a segment table with:

| Field | Meaning |
|---|---|
| spoken meaning | Exact claim made in this interval |
| frame range | Confirmed half-open interval |
| visual mode | raw, focus, full-frame, transparent overlay, subtitle-only |
| template | Selected template ID |
| reason | Why the template expresses this meaning |
| evidence target | UI element that must remain visible |
| safe area | Region available for packaging |
| timing | entrance, reveal order, hold, exit |

Select the template by claim structure, not surface appearance. A list of tools converging on one model is a concept/relationship, not automatically a ranking. Dates imply a timeline. A prerequisite and later stage imply status/flow, not numerical comparison.

## 7. Implementation

Adapt source rather than sample video:

- match final width, height, fps, and duration;
- center actual visible bounds;
- reserve the subtitle zone;
- reduce background grid/glow brightness;
- keep information hierarchy to title, main relation, support text;
- prevent badges, checks, and icons from covering cards;
- complete the main entrance in 0.25–0.55 seconds;
- keep a readable hero frame before the cut.

When a slot is very short, simplify content rather than accelerate an unreadable template.

## 8. Composition

Compose visual inserts on the unchanged source timeline. Use frame-derived timestamps and `setpts`.

Rules:

- use one encoder process per output path;
- use a new temporary output on every attempt;
- never reuse an incomplete/corrupt target;
- place boundary-driven full-frame inserts only inside confirmed black frames;
- for deliberate continuous-picture replacement, record explicit rationale and authorization in the EDL;
- place subtitles last;
- copy audio packets when no audio edit is requested;
- keep EDL frame counts equal to rendered slot frame counts.

## 9. Self-evaluation

Review rendered output, not only slot sources:

- first 2 seconds;
- one frame before, first frame, final inserted frame, and first frame after every slot;
- each hero frame;
- every subtitle style and long line;
- the last 2 seconds.
- one identity frame from every bound source;
- source-to-output count and topic consistency.

Look for:

- overlap or flash at black/non-black transitions;
- text/glyph corruption;
- components shifted right or outside canvas;
- foreground/background hierarchy collapse;
- subtitle coverage;
- stale normal-screen annotations;
- evidence hidden by a caption bar;
- warm/orange pixels.
- unrelated picture or audio from another source;
- a sample mislabeled as a full output;
- a deliverable source without a final file.

Cap blind rerender loops. Diagnose the failure class before retrying.

## 10. Delivery

Run the delivery validator once per output and save one report per output. For `scope=full`, require source/final duration equality within one frame. Confirm all `deliver=true` sources are covered by real final files. Do not hand off a file that merely opens in a player. Require continuous decode with no errors.

Update `project.md`. If the folder is not a Git repository, state that commit and push are unavailable instead of pretending they were completed.
