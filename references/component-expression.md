# Components that enact narration

Use this reference for abstract concepts, mechanisms, comparisons, and process inserts after selecting the footage route. It supplements the 20-template router in `motion-library.md`; it does not authorize covering source evidence.

## 1. Design the object before its container

Select the thing the viewer should follow: a document being divided, a request moving through a system, a budget being consumed, or a result being selected. A card is a surface for that object, not an explanation by itself.

For each related sequence, add a compact table to the existing `edit/design.md`:

| Spoken trigger | Recipe / template seed | Main object and initial state | Visible operation and result | Retain / remove / hand off |
|---|---|---|---|---|

Use the same object IDs across clauses. A document that becomes an input in the next clause keeps its shape, label, and content identity during the handoff. Record the exact trigger frame from real audio; subtitle start alone may precede the actionable word.

Populate the existing storyboard fields from this table: `semantic_object`, `semantic_action`, `state_change`, `result_state`, `spoken_trigger`, `container_strategy`, and `exit_mode`. The table adds design specificity, not a second validator schema.

## 2. Component construction vocabulary

These are recipes for HyperFrames HTML/SVG/GSAP construction, not shipped executable components. Read a matching template's source before implementing. Reuse the current library's geometry and styling where suitable; extend only the missing behavior.

| Object | Visible structure | Useful states and operations |
|---|---|---|
| Document / content block | Page silhouette with meaningful sections | Whole → selected section → separated blocks; preserve section identity |
| Processor | Clearly labeled input/output ports and processing area | Ready → receives object → transforms it → releases result |
| Candidate set / filter | Aligned items and a selection boundary | Unselected → assessed → retained or excluded; selected items remain traceable |
| Budget / capacity | Finite set of units with a fixed total | Available → consumed → remaining; counters agree with visible units |
| Relationship node | Named object with boundary anchors | Idle → active → completed or blocked; edges represent real dependencies |
| Evidence pair | Source excerpt and attached interpretation | Source appears → relevant part highlighted → supported result appears |
| Layered structure | Aligned planes with explicit level labels | Enter level → follow connection → arrive at target; depth expresses hierarchy |
| Comparison system | Equal starting conditions on a common axis | Same input → different operation → comparable outcomes |

Scale objects from the actual safe area, not a borrowed 720p pixel threshold. Use `style-system.md` unchanged. Establish the primary object through size, placement, contrast, and the existing cyan accent; continuous glow, camera movement, and decorative particles are not required.

## 3. Expression recipes

The template names below are existing seeds, not promises that a template already implements the full mechanism. If no seed supports the needed topology, build that behavior in the slot and document the gap.

| Recipe / spoken meaning | Template seeds to inspect | Visible expression process | Retained result / common failure |
|---|---|---|---|
| **process-transform** — “把输入转换成结果” | `three-step-flow`, `cause-chain` | Establish input, processor, output positions; move the input into the processor on the verb; change its structure; release the transformed object | Keep input/output identity traceable. Reject three labeled boxes with no transformation |
| **split-preserve** — “拆成几个部分” | `concept-spotlight`, `three-step-flow` | Show one whole; mark meaningful boundaries; separate the parts into equal slots while preserving their content; activate each as explained | Keep earlier parts through the group conclusion. Reject unrelated cards appearing without showing their origin |
| **filter-select** — “筛出相关内容” | `top-rank-list`, `cause-chain` | Establish candidate set; move candidates through a visible criterion; excluded items exit the main field; survivors settle into a readable result | Preserve survivor identity. Ranking and filtering are different: reorder only if narration describes ranking |
| **merge-inputs** — “几路结果汇总” | `cause-chain`, `three-step-flow` | Place peer inputs in equal geometry; trace equal branches toward one destination; show their contributions forming the output | Keep the merged output for the next beat. Reject topology that makes one input the parent of another |
| **consume-budget** — “调用消耗额度” | `before-after-stat`, `number-counter` | Show a finite budget; each completed call removes or transfers units from the same budget; the remaining amount settles after each call | Retain the depleted state. Do not refill between clauses or invent measured costs; label illustrative quantities “示意” |
| **remove-detour** — “省去中间步骤” | `cause-chain`, `status-split` | Establish the original route; remove the unnecessary node and its edges; connect the surviving endpoints; send the same request down the shorter route | Hold the new path. Do not merely cross out a label while the old route remains active |
| **grow-dependencies** — “复杂度随依赖增加” | `cause-chain`, `concept-spotlight` | Start with a short chain; add nodes and their actual dependencies on spoken triggers; re-layout the group to expose the growing structure | Preserve meaningful branches. Random lines or an unsupported numeric growth curve do not explain complexity |
| **locate-in-layers** — “逐层找到目标” | `concept-spotlight`, `three-step-flow` | Establish labeled levels; follow a path through them; enlarge or isolate the found item without losing its location context | Retain target and enough context to explain where it came from. Depth alone must not imply an unstated hierarchy |
| **loop-with-exit** — “执行、检查，不通过就重试” | `cause-chain`, `checklist-pop` | Establish execution and check nodes; route a failed result back once when narrated; advance state on the next attempt; take the explicit success exit | End the loop at success. Reject endless orbit as a substitute for execution or extra retries not in the narration |
| **compare-outcomes** — “同样任务，结果不同” | `before-after-stat`, `horizontal-bar-compare`, `stat-duel` | Show equal inputs and a common scale; apply each method; settle the resulting time, cost, or quality side by side | Preserve equal task scope and metric units. If there are no numbers, use observable state differences rather than invented percentages |
| **claim-with-evidence** — “这个结果有依据” | `source-citation-card`, `big-number-card` | Show the actual source or faithfully labeled excerpt; highlight the relevant evidence; attach the claim or metric to that location | Hold source and claim together long enough to inspect. Reject fabricated product screens or citation cards unrelated to the claim |
| **analogy-to-mechanism** — “就像……所以……” | `concept-spotlight`, `myth-fact-swap` | Introduce a familiar object; act out the matching behavior; map its parts to the technical objects; resolve into the actual mechanism | Preserve only the relationships supported by the analogy. A decorative metaphor beside a title is insufficient |

## 4. Timing, focus, and handoff

- Use quick semantic action → stable readable result → next change. Compact actions take `0.2–0.5s`; establish structure in `0.25–0.55s`. For a long process, use successive meaningful beats instead of stretching one decorative animation.
- Move the existing object to a secondary position when its role changes. Keep it readable until the next main object is established. Use `retain-update`; update the contents rather than recreating a nearly identical card.
- In a `shared-batch`, reserve the completed group's geometry from the start. Reveal items on their own triggers, retain them through the last explanation, then exit together.
- Keep a short readable hold after the result; normally target at least `0.60s`, within the actual narration window. If space or time is insufficient, simplify the mechanism. Do not extend the source or violate slot boundaries.
- Use focus changes only to clarify a detail, a handoff, or a spatial relationship. A camera move has no quota and cannot move subtitles or protected source evidence.
- A major conclusion can use a stronger composition, such as a large remaining budget beside its cause. Do not prepend an unrelated light show or reveal the answer before the spoken trigger.
- Derive moving connector endpoints from current object bounds. At a state change, remove obsolete paths, labels, and highlights explicitly. Never reuse a connector whose relationship has ended.

## 5. Worked sequence: unnecessary calls consume tokens

Illustrative design only: adapt the exact wording and timing to the user's source. No numerical measurement is implied.

| Clause / trigger | Main composition change | Continuity |
|---|---|---|
| “每次调用都会消耗 token” / “消耗” | A request passes through a model; units transfer from a finite token budget to a consumed area | Establish `request-A`, `model-A`, `budget-A`; use `consume-budget` |
| “重复调用会继续增加开销” / “重复调用” | A second request follows the same path and removes more units; the first consumed units remain | Retain all three objects and depleted budget; do not reset the count |
| “把不必要的步骤去掉” / “去掉” | Reveal the identified redundant step only if supported by the source; remove it with its obsolete edges; close the direct path | Use `remove-detour`; maintain model and request identities |
| “同样任务，就能少消耗一些” / “少消耗” | Compare the original and simplified routes with equal starting budgets; show the supported difference, or clearly labeled illustrative remaining units | Reintroduce the baseline explicitly as a comparison, not a silent budget refill; hold both outcomes |

For implementation, derive slot-local frames as `global_frame - slot_start_frame`; clip all visibility to `[0, slot_end_frame - slot_start_frame)`. Keep source FPS and integer half-open bounds. Do not copy absolute frame numbers from another film.

## 6. Review this mechanism, not just its appearance

In a representative prototype with real audio and subtitles, verify:

1. Muting explanatory labels still leaves the direction of the action understandable.
2. Each action occurs on the spoken trigger and reaches a readable result.
3. Objects retain their identity across split, merge, handoff, and comparison.
4. Batch members, consumed units, and completed steps remain until their semantic role ends.
5. Equal peers remain balanced; connectors close and stale elements disappear.
6. The source's evidence and subtitle zone remain visible throughout motion, including entrances.

Record failures as a specific beat and operation, then fix that mechanism. Still frames can prove layout but cannot prove narration alignment or normal-speed comprehension. These recipes have not themselves passed production-video acceptance; validate each adapted slot under the existing prototype and final gates.

## Reference provenance

Design study: [anything2explainer](https://github.com/Vincentwei1021/anything2explainer), reviewed at commit `734964ea65682efbdac048acefc58f4b7b50ab68`, particularly its concept-to-shot routing and object handoff examples. This reference is original guidance for our existing workflow; no upstream code, assets, or sample frames are bundled. Its toolkit uses PolyForm Noncommercial and states that commercial use requires author authorization; do not treat this design study as permission to copy its implementation. Our palette and production gates remain authoritative.
