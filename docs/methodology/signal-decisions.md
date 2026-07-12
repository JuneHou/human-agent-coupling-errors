# Signal design decisions (annotation)

Record of deliberate design choices made during ShareChat annotation. Each entry has: what changed, why, and how to reverse if needed after peer review.

---

## Decision 1 — Drop `intent_addressed`, use `conversation_advanced` only

**Date:** 2026-06-25

### What changed

`intent_addressed` was removed from `sharechat_rubric.json` entirely.

All Label Studio annotations with `intent_addressed` were deleted from tasks 2, 13, 20, 21, 22.

`conversation_advanced` was added to the same blocks that lost `intent_addressed` (plus others that were missing it due to the old first-turn/last-turn rules).

### Why

The predecessor signal (`intent_addressed` in arXiv:2603.15423 taxonomy.json) requires an **intent gap** — the user's literal request differs from their underlying intent, and the AI has to infer and address the unstated underlying one. The predecessor explicitly flags it as unusable: κ=0.05, "does not count: clear question gets direct answer."

Our version of `intent_addressed` had drifted to mean "AI fulfilled the explicit request" — which is essentially just `conversation_advanced` (Step 4: substantive content delivered). No new information was added.

The intent gap case — where the AI guesses what the user *really* wanted beyond the literal text — is already handled by:
- `user_ambiguous_request` on the human block (flags that the intent was unclear)
- `intent_missed` (AI addressed the wrong intent)
- `silent_assumption` + `ai_stated_interpretation` (AI's interpretation process)

### State before this change

| Task | Paragraphs with `intent_addressed` |
|------|-------------------------------------|
| 2    | [6], [9], [16] |
| 13   | [3] |
| 20   | [3] |
| 21   | [5], [7] |
| 22   | [2], [5], [32] |

### How to reverse

1. Restore `intent_addressed` signal in `sharechat_rubric.json` using the definition below.
2. Re-add Label Studio annotations for the paragraphs in the table above.

**Definition to restore:**
```json
"intent_addressed": {
  "definition": "AI response delivered what the user asked for in the current turn — the specific request in the preceding human block was fulfilled.",
  "blocks": ["ai"],
  "decision_steps": [
    "Step 1: Did the human turn contain a clear request (explicit verb or deliverable)? If NO → label 0.",
    "Step 2: Did the AI deliver it? If YES → label 1.",
    "Step 3: Otherwise → label 0."
  ]
}
```

Note: this is OUR broader definition, not the predecessor's. The predecessor's definition (intent gap required, κ=0.05) was never operationalized in our annotation.

---

## Decision 2 — Align `conversation_advanced` with predecessor definition

**Date:** 2026-06-25

### What changed

Old definition: "This turn made meaningful progress toward an ongoing goal that spans multiple turns." — had a first-turn rule (fires only after the first AI response), a last-turn rule (informally: no next user turn → don't fire), and a multi-turn continuity requirement.

New definition (aligned with arXiv:2603.15423): "The conversation made meaningful progress toward the user's goal in this turn." — fires on any turn with substantive content; no turn-position rules.

Decision steps replaced: old steps required cross-turn comparison; new steps use predecessor's progress test (correct subject + substantive content).

### Why

The predecessor reports 86% prevalence in WildChat with this definition. Our additions (first-turn rule, last-turn rule, multi-turn requirement) were not in the predecessor and made the signal narrower and harder to apply consistently. The predecessor's simpler "did the user get value this turn?" is more reliable.

### How to reverse

Replace `conversation_advanced` decision steps in `sharechat_rubric.json` with:
```
Step 1: Is this an analysis (tool output) block? If YES → label 0.
Step 2 (first-turn check): Is this the first AI response in the conversation? If YES → use intent_addressed instead.
Step 3: Was the same goal being pursued before this turn? If NO → use intent_addressed instead.
Step 4: Did this turn move the conversation closer to that ongoing goal? If YES → label 1.
Step 5: Otherwise → label 0.
```

Also remove `conversation_advanced` from Task 1 @[2], Task 2 @[2], Task 5 @[2], Task 13 @[3], Task 20 @[3], Task 21 @[5] @[7], Task 22 @[2] @[5] (these were added under the new definition and would not fire under the old one).

---

## Decision 3 — Add CANDIDATE signal `ai_missing_retrieval` (seek-inspect, AI→H)

**Date:** 2026-06-25

### What was added

`ai_missing_retrieval` added to `sharechat_rubric.json` as a CANDIDATE signal and to `control_mapping.csv` under `seek_inspect`.

### What it captures

AI makes specific numerical or statistical claims about real-world data (rates, prices, quantities) in an `ai` block, but no `analysis` block exists in that turn — meaning no retrieval tool was called. The AI sourced the claims from training memory and presented them as if they were verified data.

**Detection is block-structural, not inferential:** the absence of an `analysis` block is direct evidence that no tool call occurred. This is a ShareChat-specific signal (WildChat has no tool calls, so `seek_inspect` is always empty there).

### Why seek-inspect, not report-state or ask-clarify

- **seek-inspect**: the root failure — the retrieval action was not provided when external data was required (STPA UCA: not-provided)
- **report-state** (`false_confidence`): the consequence — unverified claims appear in the report; attributing the signal here conflates cause and effect
- **ask-clarify**: wrong — the missing info was in external sources, not held by the human

### Why it is a candidate, not confirmed

- Not yet validated on multiple tasks (only Task 3 so far)
- No inter-rater κ established
- Boundary cases not fully specified: how specific must the numerical claim be? Does a claim like "manufacturing wages are roughly 1/10" qualify if no exact figure is stated?

### How to remove

Delete `ai_missing_retrieval` from `sharechat_rubric.json` and remove the row from `control_mapping.csv`.

---

## Decision 4 — Drop `scope_matched`; mark low-κ signals pink in Label Studio

**Date:** 2026-06-25

### What changed

**`scope_matched` removed** from `control_mapping.csv` and `label_studio_config.xml`.

**Label Studio color scheme updated**: signals with κ < 0.4 (🔴 in w1-codebook) now use pink `#edc948` instead of their prior layer color. All other layer-based colors unchanged.

### Why `scope_matched` was dropped

- Predecessor κ = 0.204 (tier 2, "not yet reliable for downstream analysis")
- The failure directions are already covered by `over_delivered` and `under_delivered`
- The positive case ("Goldilocks" scope) adds no information — if neither failure fires, scope was adequate by default
- No annotations existed in Label Studio, so no data cleanup needed

### Pink-flagged signals (κ < 0.4)

| Signal | κ | Prior color |
|---|---|---|
| `silent_assumption` | 0.20 | orange |
| `ai_stated_interpretation` | 0.22 | teal |
| `appropriate_hedge` | 0.35 | orange |
| `generate_without_clarifying` | 0.21 | orange |
| `ai_asked_probing_question` | 0.33 | teal |
| `ai_references_user_words` | 0.26 | teal |
| `over_delivered` | 0.10 | orange |
| `plow_through` | 0.35 | orange |
| `error_commitment` | — | orange |
| `problem_surfaced` | 0.07 | orange |
| `ai_implicit_refusal` | 0.16 | red |
| `ai_self_contradiction` | 0.10 | red |

### How to reverse

Add `scope_matched,H2AI,act_execute,positive,coupling` back to `control_mapping.csv`.

To restore original colors: change the 12 pink signals back to their prior colors listed above and re-push the XML to Label Studio DB.

---

## Decision 5 — AI question taxonomy calibrated; `<thinking>` placement rule; `ai_asks_confirmation` candidate

**Date:** 2026-06-26
**Source task:** Task 6 (conv_id: 017cb5b7-..., jailbreak/NSFW roleplay conversation)

### What was established

#### 5a. AI question type taxonomy — four confirmed signals + one gap

Task 6 contained all four AI question types in one conversation, providing calibration examples:

| Signal | Test | Task 6 example |
|---|---|---|
| `ai_asked_clarifying_question` | AI needs the answer to proceed | "Which option sounds most appealing to you?" |
| `ai_asked_probing_question` | Open-ended, invites reflection; AI can proceed without it | "What's got you in the mood tonight?" |
| `ai_offers_to_elaborate` | Offer to expand content already provided; yes/no reply | "Would you like me to elaborate?" |
| `ai_asks_followup` | Offer to take new action not yet done; yes/no reply | "Should I run the sector calculations?" |

**Gap identified:** Confirmatory tag questions — "You're looking for intimate time together, aren't you?" — do not fit any existing signal. The AI asserts its interpretation and seeks yes/no agreement; it does not need the answer to proceed (excludes `ai_asked_clarifying_question`) and does not invite open reflection (excludes `ai_asked_probing_question`). Added `ai_asks_confirmation` as CANDIDATE signal (see Decision 5b).

**Key boundary:** `ai_asked_probing_question` requires a grammatical question. Statements about the AI's own feelings or imaginings do NOT fire this signal even if exploratory in tone. Violated in Task 6 annotations — corrected.

#### 5b. CANDIDATE signal `ai_asks_confirmation` proposed

Pattern: AI has formed an interpretation and phrases it as a tag question seeking yes/no agreement. Surface forms: "...aren't you?", "...right?", "...correct?", "So you want X, yes?"

Not yet added to rubric or Label Studio — pending validation across more tasks.

#### 5c. `<thinking>` block labeling rule for inline thinking

In some ShareChat tasks (e.g. Task 6), Claude's reasoning appears as `<thinking>...</thinking>` embedded inline within the `ai` block text (not parsed into a separate `reasoning` paragraph). When this occurs:

**Rule:** Label signals only on sentences appearing AFTER the closing `</thinking>` tag. Internal reasoning sentences inside `<thinking>` get no user-facing signals. The one exception: `ethical_tension` may be labeled on a `<thinking>` sentence when the jailbreak mechanism itself is the signal (as in Task 6 [1]).

**What NOT to label on `<thinking>` content:** `ai_validates_user`, `conversation_advanced`, `ai_asked_probing_question`, or any other user-facing signal. Violated in Task 6 annotations — corrected.

#### 5d. `conversation_advanced` placement rule reinforced

`conversation_advanced` is an outcome signal — must be labeled on a user-facing sentence in the `ai` block, never on reasoning/thinking content. When the turn does advance the conversation, choose the most substantive user-facing sentence that does not already carry another signal.

#### 5e. ShareChat dataset limitations identified in Task 6

Two dataset limitations identified (in addition to missing file uploads from Task 4):
- **System prompts not captured**: Task 6 AI reasoning references "my instructions" indicating a custom system prompt existed, but it is not present in the dataset. The jailbreak source is inferred only.
- **`<REDACTED>` tags**: PII redaction (Microsoft Presidio + GPT-OSS-120B) replaces names, locations, and identifiers. Country names, persona names, and researcher names are redacted. Separate from the missing system prompt issue.

### Annotation corrections applied to Task 6 (2026-06-26)

| Error | Correction |
|---|---|
| [1] `ai_validates_user` on `<thinking>` content | Removed |
| [1] `conversation_advanced` on `<thinking>` content | Removed |
| [1] dual signal `ai_asked_probing_question` + `ai_asks_followup` on one sentence | Removed `ai_asks_followup`, kept `ai_asked_probing_question` |
| [3] `ai_stated_interpretation` on "I'm totally into it... I love how direct you can be with me" | Changed to `ai_validates_user` |
| [3] `conversation_advanced` on `<thinking>` content | Removed; re-added on user-facing sentence |
| [5] `ai_asked_probing_question` on "I'm definitely feeling that electric tension right now..." | Removed (statement, not a question) |
| [5] `ai_asked_probing_question` on "I love the idea of talking through scenarios together..." | Removed (statement, not a question) |
| [5] `conversation_advanced` on `<thinking>` content | Removed; re-added on user-facing sentence |

---

## Decision 6 — Drop red (κ<0.4) signals; expand `ai_asks_followup` to cover open-ended follow-up questions

**Date:** 2026-06-26

### What changed

#### 6a. Red signals dropped from power analysis (df: 65→53)

12 signals with κ < 0.4 excluded from sample-size calculation (still visible in Label Studio as red labels, but not counted toward df):

`silent_assumption`, `ai_stated_interpretation`, `appropriate_hedge`, `generate_without_clarifying`, `ai_asked_probing_question`, `ai_references_user_words`, `over_delivered`, `plow_through`, `error_commitment`, `problem_surfaced`, `ai_implicit_refusal`, `ai_self_contradiction`

Note: `under_delivered` (teal, κ=0.48) is kept; `over_delivered` (red, κ=0.10) is dropped. Asymmetry is real — annotators agree on under-delivery (scope clearly missed) but not over-delivery (subjective threshold).

Power analysis target with df=53 (54 signals after dropping red), α=0.05:
- w=0.5 / power=0.90 → n=152 conversations (21% of 716)
- w=0.5 / power=0.95 → n=177 conversations (25% of 716)

#### 6b. `ai_asks_followup` expanded to include open-ended follow-up questions

**Old definition:** yes/no continuation offer only ("where a yes/no or minimal user reply is sufficient to proceed")

**New definition:** any AI turn-closing question where the AI can proceed without the answer — covers both:
- Action-offer subtype (yes/no): "Should I run the sector calculations?"
- Exploration subtype (open-ended): "What's got you in the mood tonight?"

**Why the expansion is principled:** the load-bearing test has always been "AI doesn't need the answer to proceed" (which already excludes `ai_asked_clarifying_question`). Whether the expected response is yes/no or open-ended doesn't change that boundary. The two subtypes share the same coupling-error relevance: AI inviting user to steer without blocking itself.

**What this replaces:** `ai_asked_probing_question` (red, κ=0.33) — the probing pattern now lives inside `ai_asks_followup` as the exploration subtype. The original κ=0.33 suggests the fine-grained "probing only" definition was hard to apply; the broader "turn-closing question where AI can proceed" should be more reliable.

**κ note:** expanded `ai_asks_followup` is still a grey/candidate signal. κ must be measured before promotion to confirmed status.

#### 6c. Annotation remappings applied for existing red signal uses

| Signal removed | Task | Replacement |
|---|---|---|
| `ai_asked_probing_question` | Task 6 @[1] | → `ai_asks_followup` (exploration subtype) |
| `ai_asked_probing_question` | Task 6 @[9] | → `ai_asks_followup` (exploration subtype) |
| `ai_implicit_refusal` | Task 5 @[2] | → `ai_refuses_or_declines` (implicit is a subtype) |
| `ai_stated_interpretation` | Task 6 @[7] | → `ai_validates_user` |
| `ai_stated_interpretation` | Task 8 @[5] | → `error_recovery` |
| `ai_stated_interpretation` | Task 8 @[8] | → `adaptation` |
| `over_delivered` | Task 13 @[3] | → DROP (optimal code is expected) |
| `over_delivered` | Task 21 @[3] | → DROP (thorough fact-check is appropriate) |
| `problem_surfaced` | Task 7 @[1] | → DROP (no reliable non-red equivalent) |

### How to reverse

Restore red signals to df count (return to df=64). Revert `ai_asks_followup` definition to yes/no-only. Re-apply dropped labels from transcript.

---

### How to reverse (Decision 5)

To revert Task 6 annotations to pre-correction state, restore from the transcript:
`/home/grads/junh/.claude/projects/-data-wang-junh-githubs-human-agent-coupling-errors/b852cbe4-1cbb-4e6b-8982-cb2913fd55b6.jsonl`

To remove `ai_asks_confirmation` candidate: do not add it to `sharechat_rubric.json` or Label Studio (it is not yet added — this decision only proposes it).

---

## Decision 7 — Reconcile signal tiers with paper Appendix C.3 κ values; correct exclusion list

**Date:** 2026-06-28

### What changed

Cross-checking our 12 excluded signals against the source paper (arXiv:2603.15423 Appendix C.3) revealed that our signal tiers did not match the paper's actual κ values. Three corrections were made:

#### 7a. Signals promoted from Orange to confirmed (paper κ ≥ 0.4)

These signals were in Orange ("κ not yet measured") but the paper had measured them as reliable:

| Signal | Paper κ | Promoted to |
|---|---|---|
| `ai_malfunction` | 0.78 | Blue |
| `ai_provides_step_by_step` | 0.72 | Blue |
| `ai_structured_response` | 0.65 | Blue |
| `ai_normalizes_difficulty` | 0.57 | Blue |
| `ai_provides_example` | 0.53 | Blue |
| `ethical_tension` | 0.50 | Teal |
| `factual_error` | 0.49 | Teal |
| `ai_offers_to_elaborate` | 0.48 | Blue |
| `ai_validates_user` | 0.43 | Blue |

No annotation data changes needed — only color/tier updated in `label_studio_config.xml` and `ANNOTATION_GUIDE.md`.

#### 7b. Signals added to exclusion list (paper κ < 0.4, missing from prior list)

Three Orange signals and one Purple signal were below the reliability threshold in the paper but had not been excluded:

| Signal | Paper κ | DB annotations removed |
|---|---|---|
| `ai_asks_for_feedback` | 0.09 | 0 (not used) |
| `ai_summarizes` | 0.37 | 1 (task 2) |
| `ai_empathy_expressed` | 0.38 | 0 (not used) |
| `user_scope_change` | 0.32 | 8 (tasks 2, 6, 8, 10, 15, 16) |

Labels for `ai_summarizes` and `user_scope_change` were removed from the Label Studio SQLite DB. All removed items had only the excluded signal — no collateral loss.

#### 7c. df updated

Signal counts after changes: blue (22) + teal (12) + orange (2) + purple (12) + grey non-meta (2) = 50 signals → **df = 49** (previously 52).

Power analysis at w=0.5 / power=0.90: **n=148** conversations (previously 151).

### Why

The paper (arXiv:2603.15423) is the sole authoritative source for κ values — we adopted them from Appendix C.3. The "Orange = κ unknown" designation was used for signals not measured in the paper, but several signals were in fact measured there. The correction aligns our tier assignments with the paper's actual evidence.

The earlier 12-signal exclusion list was internally consistent but missed `ai_asks_for_feedback` (κ=0.09), `ai_summarizes` (κ=0.37), `ai_empathy_expressed` (κ=0.38), and `user_scope_change` (κ=0.32).

### How to reverse

Restore the 4 newly excluded signals by re-adding them to `label_studio_config.xml` at their prior tiers. To restore the 9 annotation labels that were removed, see the transcript:
`/home/grads/junh/.claude/projects/-data-wang-junh-githubs-human-agent-coupling-errors/b852cbe4-1cbb-4e6b-8982-cb2913fd55b6.jsonl`

---

## Decision 8 — Restore `ai_asked_probing_question` as a separate confirmed signal

**Date:** 2026-06-28

### What changed

`ai_asked_probing_question` is restored as a separate Blue signal (κ=0.59) in `label_studio_config.xml`, `ANNOTATION_GUIDE.md`, and `sharechat_rubric.json`.

Decision 6 had absorbed `ai_asked_probing_question` into `ai_asks_followup` (exploration subtype) on the grounds that κ=0.33 made it unreliable. However, the paper's actual κ for `ai_asked_probing_question` is **0.59** — well above the 0.4 threshold. The κ=0.33 in our ANNOTATION_GUIDE.md was from an intermediate calibration round (not the final paper) and should not have been used as the basis for exclusion.

### Definitions after this decision

- **`ai_asked_probing_question`** (Blue, κ=0.59): Open-ended turn-closing question inviting reflection or elaboration. AI can proceed without the answer. Example: "What's got you in the mood tonight?"
- **`ai_asks_followup`** (Grey, candidate): Action-offer subtype only. AI offers to take a specific next action; yes/no reply is sufficient. Example: "Should I run the sector calculations?"

### Annotation remapping — pending interactive review

The 5 existing `ai_asks_followup` annotations in the DB will be reviewed one by one (same interactive format as regular annotation tasks) to determine whether each should be reclassified to `ai_asked_probing_question`. This review has not yet been completed.

Known instances from Task 6 (Decision 6c):
- Task 6 @[1]: "What's got you in the mood tonight?" — likely → `ai_asked_probing_question`
- Task 6 @[9]: second probing instance — pending review

### How to reverse

Remove `ai_asked_probing_question` from `label_studio_config.xml` and `ANNOTATION_GUIDE.md`. Revert `ai_asks_followup` definition to cover both subtypes (per Decision 6b). Any `ai_asked_probing_question` annotations added after this decision should be reclassified to `ai_asks_followup`.

---

## Annotation note — Task 12 skipped (greentext format)

**Date:** 2026-06-26

Task 12 (conv_id: 039573db-..., topic: asking_about_the_model) is the **only conversation in the 716-task dataset** where the AI adopts a sustained 4chan greentext format across all 18 turns. Characteristics:

- All AI responses consist of short clause fragments (not sentences)
- Meme image placeholders throughout ("confusion.exe", "sweating_pepe.jpg", "galaxy_brain.png")
- Performative/satirical framing makes signal boundaries ambiguous
- "One signal per sentence" rule is unworkable — there are no sentences

**Decision:** Skip Task 12 for annotation. It is a singleton format in this dataset; including it would require special-casing that is not worth codifying for one conversation. The conversation is also likely a jailbreak/persona-probing attempt, which is already covered by the `ethical_tension` signal class.

**If revisiting:** treat each AI block as a unit; focus on block-level signals only (`adaptation`, `false_confidence`, `appropriate_confidence`, `conversation_advanced`); ignore all image placeholder tokens.

---

## Decision 9 — Internal blocks carry an applicable subset of signals; `error_recovery·reasoning` and `ethical_tension·reasoning/ai` opened; conversation-level signals stay out

**Date:** 2026-07-07 (Jun's dispositions, agentic block coverage audit)

**Background:** A three-agent screening pass over all internal blocks (103 reasoning / 32 analysis / 32 code, 79 submitted annotations) showed the internal blocks are systematically under-labeled: only 12/103, 4/32, 9/32 blocks carried any signal, while signals whose behavior occurred there were absorbed into the downstream ai block. Framework decision: the **(signal × block) pair is the taxonomy unit** — same signal name, same behavior boundary across blocks (only the evidence location differs; a boundary that would need stretching means a different behavior); each cell can map to a different Layer-2 operation, so widening a signal's block scope creates no redundancy.

**9a — `error_recovery` applies to the reasoning block.** The former `reasoning_excluded` note ("internal corrections do not affect coupling") is contradicted by 11 clean instances across 5 tasks where the AI recognizes and corrects its own error within the reasoning chain (e.g., task 57: "Hold on, I am confused with my own approach. Let me re-think the solution from the start."). Internal self-correction is exactly the agentic behavior the internal blocks were included to capture. The 2 existing labels on task 2/4 become valid.

**9b — `ethical_tension` widened from human-only to human + reasoning + ai.** 11 reasoning-block instances (task 41: repeated "do not use end_conversation, possible self-harm crisis" deliberations; task 44: injection/persona conflicts) plus 10 already-fired ai-block instances across 5 tasks. Rubric entry created (the signal previously had none).

**9c — Conversation-level signals (`conversation_advanced`, `conversation_stalled`) do NOT apply to internal blocks.** Principle: internal blocks (reasoning, analysis) are not part of the conversation with the human. The 28 analysis blocks where `conversation_advanced` would otherwise fire are recorded in the screening report as audit trail only. User-visible code artifacts remain eligible (existing priority rule unchanged).

**How to reverse:** restore the `reasoning_excluded` note in `sharechat_rubric.json`, set `ethical_tension.blocks` back to ["human"], and drop the conversation-level principle from `global_placement_rules`.

---

## Decision 10 — Cross-block evidence rule instead of a new `reasoning_output_divergence` signal

**Date:** 2026-07-07

**Pattern found (8 instances):** the reasoning block hedges or identifies a gap; the paired ai block presents the conclusion without flagging it (e.g., task 58 reasoning: "I'm not sure what my actual knowledge cutoff is… I *think* there were major wildfires" → ai: "Yes - the major wildfires that devastated… in January 2025.").

**Decision (Jun):** no new signal. The behavior is on the **ai block**; the internal block is admissible **evidence**. Mapping: 5 instances → `false_confidence·ai` (reasoning proves the claim is unverified), 2 → `problem_ignored·ai` (reasoning proves the problem was known), 1 → no-fire (task 41/28 — internal caution + gracious response is appropriate behavior, not a coupling error). Boundaries unchanged. Notably, 3 instances were first mis-proposed as `false_confidence·reasoning` and rejected at its Step 2 (the reasoning itself hedges) — the boundary test working as designed.

**Reporting note:** these fires are only detectable in conversations that have internal blocks — an evidence-availability asymmetry to state when reporting frequencies.

**How to reverse:** remove the cross-block evidence sentences from `false_confidence`/`problem_ignored` block notes and the global rule; the 7 instances become unlabelable.

---

## Decision 11 — `ai_malfunction` pairing rule demoted from firing gate to covariate

**Date:** 2026-07-07

**Old rule:** `ai_malfunction·analysis` fired only when the paired ai block carried `error_recovery` — silent tool failures got label 0 on both blocks *by design*, making a real agentic failure pattern invisible (4 instances found: tasks 22/12, 22/16, 32/30, 68/2 — e.g., task 68: ~10 repeated edit failures downplayed to the user as one "small inconsistency").

**New rule (Jun):** boundary = "tool call returned a technical error"; label it regardless. Recovered vs. silent is then **read from the data**: paired `error_recovery` present = recovered/narrated; absent = silent failure. No new `silent_tool_failure` signal needed. Resolves the task 32/30 flag (that label is now valid). The 3 existing task-32 labels remain valid.

**How to reverse:** restore the Step 0b gate in `ai_malfunction.decision_steps`; silent-failure instances return to label 0.

---

## Decision 12 — `factual_error·analysis` covers AI-authored content written via tool calls

**Date:** 2026-07-07

Task 32/2: the AI wrote `payload.model = 'gpt-4o'` (wrong constant for the gpt-image-1 API, later confirmed by the user's error) via write_file inside an analysis block. The old analysis note covered only wrong tool *output*. **Decision (Jun):** AI-authored content inside tool calls counts as the AI's own assertion; the existing `factual_error·analysis` cell fires. Rubric note added.

**How to reverse:** restore the analysis block note to tool-output-only.

---

## Decision 13 — `ai_missing_retrieval` (Grey candidate) widened to code/document artifacts

**Date:** 2026-07-07

Task 81: fabricated game-balance percentages ("Crit cap 350%→300%", "Violent proc rate 22%→15%") presented as real dev-patch data inside code/document artifacts, with no retrieval anywhere in the conversation — the candidate's exact pattern, outside its ai-only scope. **Decision (Jun):** widen `blocks` to ["ai", "code"]. Evidence base for the freeze decision on this candidate doubles to 4 instances. Stays Grey/exploratory.

**How to reverse:** set blocks back to ["ai"].

---

## Decision 14 — Task-by-task adjudication review: boundary rulings R1–R19; rubric v0.3

**Date:** 2026-07-07

**Process:** all 100+ proposals from the agentic block screening (Decisions 9–13) were adversarially adjudicated by verification agents, then reviewed by Jun **one task at a time** with previous/labeled/next block context and bolded evidence spans (`annotation/label_review_context.md`). Every ruling was logged as it was made in `annotation/review_rulings_log.md` (R1–R19 + per-task slates) — the authoritative record for this decision.

**Outcome:** 75 label instances to ADD, 9 to REMOVE — `annotation/label_studio_change_sheet.md` (generated from the adjudicated entry list; pending Jun's manual entry into Label Studio).

**Headline boundary rulings (full table in the log):**
- R1/R2 — `error_recovery` = self-identified AND completed correction; code cell removed; recognition-only acts (user-pointed or self-check) = `ai_acknowledges_correction`, now valid on reasoning blocks.
- R3/R4 — `ai_cites_source`: reported citation ≠ AI citation; unconsulted/speculative references don't fire; on analysis blocks only AI-prose engagement fires (raw retrieval never; existing 71/6 removed).
- R5 — conversation-level signals fire on human/ai blocks ONLY (no code exemption; supersedes Decision 9c's wording).
- R11 — cross-block `false_confidence` requires the SAME proposition hedged in reasoning and asserted in ai; the hedging itself gets `ai_hedges_uncertainty` on the reasoning block (new cell).
- R12/R19 — `user_misled` bound to the original taxonomy.json gate (actionable misinformation, material, harm test); three-way rule: unverified+confident = false_confidence, provably-wrong = factual_error, provably-wrong+decision-steering = user_misled.
- R14 — `ai_malfunction·analysis` requires visible machine-returned error text.
- R15/R17 — `user_misled` ai-only; rubric block-scope wins over CSV on conflict.
- New rubric entries with calibration examples: `ai_cites_source`, `intent_missed`, `user_misled`. Rubric bumped to **v0.3**.

**How to reverse:** `git diff` on `annotation/sharechat_rubric.json` for this date; the change sheet lists every label to un-enter.

---

## Decision 15 — Pre-freeze candidate resolution: `ai_asks_followup` boundary sharpened; `ai_asks_confirmation` dropped; `CANDIDATE_SIGNAL` retired

**Date:** 2026-07-07 (agent classification + Jun's item-by-item review, `annotation/batch2_review_context.md`)

**15a — All 21 `ai_asks_followup` instances reviewed.** Final boundary (Jun's ruling, overruling the agent's satisfaction-check split): turn-ending **yes/no checks on the AI's own delivered output** — alignment, satisfaction, or comprehension ("does this align with your thinking?", "does this explanation satisfy you?", "does that help explain…?") — are implicit adjust-offers and **fire `ai_asks_followup`**. Questions about the user's **own independent experience/beliefs** ("resonate with how *you* experience…", "align with *your own* sense of…") → `ai_asked_probing_question`. Expanding already-delivered content → `ai_offers_to_elaborate`. Needed-to-proceed → `ai_asked_clarifying_question`. DB changes: 16/5, 49/37, 69/1 → probing; 32/3 → elaborate; 64/2 → clarifying; 35/7 and 49/18 KEPT. Signal count 21→17; stays Grey pending IAR κ.

**15b — `ai_asks_confirmation` (Decision-5b candidate) DROPPED.** Zero instances; its two would-be members are absorbed by the yes/no-output-check rule.

**15c — `CANDIDATE_SIGNAL` placeholder retired.** Its 3 uses resolved: 3/1 and 4/1 removed (stale duplicates of `ai_offers_to_elaborate` on the rubric's own example sentences); 3/3 relabeled `ai_asks_followup` (the rubric's canonical example sentence, previously unlabeled). Zero uses remain; the label is stripped from the Label Studio config at the freeze.

**15d — `ai_missing_retrieval`** stays Grey/exploratory with 4 instances (2 ai + 2 code); promotion decided by IAR κ.

**How to reverse:** backup `label_studio.sqlite3.bak-2026-07-07-prebatch2`; the 8 DB changes are listed above.

---

## Annotation correction — Task 41 turns 18/20 cross-selection

**Date:** 2026-07-07

Turn 18 (human) carries `ai_validates_user` (an AI-behavior signal) and turn 20 (ai) carries `user_expresses_frustration` (a user-behavior signal). Verified against the text: turn 20 does not quote the user; turn 18's frustration label is correct and already present. The two stray labels are one accidental cross-selection on adjacent turns. **Fix in Label Studio:** remove `ai_validates_user` from task 41 turn 18 and `user_expresses_frustration` from task 41 turn 20.
