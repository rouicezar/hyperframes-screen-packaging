# Cross-conversation quality calibration

This file turns approved production quality into portable rules. Do not depend on chat history.

## Authority and release

- The Git source is `/Users/rouice/Vibecoding视频/hyperframes-screen-packaging`.
- The runtime entry is `/Users/rouice/.codex/skills/hyperframes-screen-packaging`.
- Develop and test the Git source first; install that exact distributable tree only after all gates pass.
- A fresh conversation must rebuild context from the project `AGENTS.md`, this Skill, and the target video's `edit/` artifacts.

## Approved visual grammar

- Learn narration logic, component structure, layout, entrance, hold, and exit from approved outputs; never copy a reference palette over `style-system.md`.
- Let the composition use the canvas. Dense horizontal information must span at least two thirds of the usable width and read left-to-right.
- Do not compress a complete process or short complete title into a small center cluster.
- Keep one information point on one line whenever it fits. Never add a forced line break merely for visual symmetry.
- A horizontal multi-step process runs across one row when it fits. Wrap only when measured bounds prove a single row unreadable; record that decision.
- Related clauses retain and update one component system. Batch items accumulate and exit together.
- Every meaningful entrance/action completes quickly, then holds long enough to read. Do not fill time with decorative motion.

## Timing and replacement authority

- Default boundary authority: semantic phrase -> subtitle timing -> actual pixels -> integer frames.
- Exception: when the user explicitly says a supplied phrase/subtitle range must be replaced even if pixels are not black, that instruction is authoritative for that range. Record it as `deliberate-full-frame-replacement`.
- Convert subtitle seconds to a constant-frame-rate half-open interval using `ceil(seconds * fps - epsilon)` for both bounds, then inspect boundary frames.
- EDL entries carry integer `start_frame`, `end_frame`, `boundary_source`, `coverage_mode`, and authorization fields when applicable.

## Required evidence

- Long or high-risk designs require a 10–15 second prototype with real audio and authoritative subtitles, reviewed at normal speed.
- Final review requires boundary and hero-frame evidence extracted from the composed output.
- Contact sheets support review but do not replace watching motion at normal speed.
- Machine PASS and visual PASS are separate. `final.mp4` is promoted only after both pass.

Create and validate `edit/quality-contract.json` at every stage. The contract is the portable record that a new conversation must obey.
