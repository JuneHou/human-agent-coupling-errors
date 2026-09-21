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
| `ai_references_user_words` | 0.26 | teal |
| `over_delivered` | 0.10 | orange |
| `plow_through` | 0.35 | orange |
| `error_commitment` | 0.27 | orange |
| `problem_surfaced` | 0.07 | orange |
| `ai_implicit_refusal` | 0.16 | red |
| `ai_self_contradiction` | 0.10 | red |

> κ values here are from arXiv:2603.15423v2 Appendix C, Table 5 — see `annotation/kappa_paper_table5.csv` and `docs/methodology/kappa-provenance.md`.

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

Turn 18 (human) carried `ai_validates_user` (an AI-behavior signal) and turn 20 (ai) carried `user_expresses_frustration` (a user-behavior signal). Verified against the text: turn 20 does not quote the user; turn 18's frustration label is correct and already present. The two stray labels were one accidental cross-selection on adjacent turns. **Fix in Label Studio:** remove `ai_validates_user` from task 41 turn 18 and `user_expresses_frustration` from task 41 turn 20.

**STATUS: APPLIED** (verified 2026-07-22). Both removals are in the DB. Task 41 now
carries `user_expresses_frustration` on b18 (human, `aA9tNlRLwi`) and
`ai_validates_user` on b20 (ai, `py94bsPK-g`) — each on the block matching its
direction. A DB-wide check found **0** `ai_validates_user` spans on non-`ai` blocks
(58/58 endpoints on `ai`).

**Standing guard:** `annotation/validation_sweep.py` re-checks this invariant on every
run (BLOCK CHECK section) and exits non-zero if any `ai_validates_user` span lands on
a non-`ai` block. The signal name asserts the direction — *the AI validates the user* —
so a human-block placement is always a cross-selection error.

---

## Decision 16 — Confidence-axis operationalization (`appropriate_confidence` entry added; `false_confidence` Step 3 generalized to the original calibration gate)

*(2026-07-26, Jun. Rubric v0.3 → v0.4. Breaks the R21 freeze — restart the 10-task freeze count.)*

**Trigger.** Audit of the 148-task labeled set found `appropriate_confidence` fired **1/148 (0.68%)** vs a predecessor operating prevalence of ~13% (WildChat, preliminary) — and it had **no rubric entry at all** (checklist one-liner only). It is a primary teal signal (config κ=0.49), so ~0 instances would make its agreement-round κ meaningless.

**Root cause.** No decision-steps were ever written. The original bigspin `taxonomy.json` defines it with a **complexity gate** ("Only fires when the question was complex/contested enough that hedging would be tempting. Routine factual answers don't qualify") + a COMPLEXITY-PLUS-CONFIDENCE test — none of which was operationalized in our rubric.

**Resolution.**
1. **`appropriate_confidence`** given a faithful-narrow entry: Step 1 complexity gate → Step 2 decisive/unhedged → Step 3 warrant by **verifiability only** (the downstream-user-acceptance route was considered and deliberately NOT adopted) → Step 5 mutual exclusion with `false_confidence` on one claim. Accept example = complex debugging correctly diagnosed (task-149 style); reject example = routine correct fact (144's M7.7).
2. **`false_confidence` Step 3 generalized.** The old narrow Step 3 (double-counted-estimate-validated) is replaced by the **original structural gate + calibration test**: the span must contain a claim that is verifiably wrong / unverified-unsupported / structurally flawed AND certainty must exceed reliability; confident/absolute/interpretive phrasing on a warranted-correct claim → 0. The double-count case is retained as an *example*. (See R22.)
3. **κ source (verified 2026-07-26).** `appropriate_confidence` **κ = 0.49**, from **arXiv:2603.15423v2, Appendix C, Table 5** ("Invisible failures in human-AI interactions", Potts & Sudhof; the agreement appendix exists only in v2). **Caveat for the paper:** Table 5 κ is **model-vs-model agreement (Opus 4.6 vs GPT-5.4)**, not human inter-annotator agreement, and must be described as such. Full provenance and the single-source rule: `docs/methodology/kappa-provenance.md`.

**Data edits (gold, LS DB).** Tone-firing audit of the 62 `false_confidence` instances removed 6 that rested on confident/interpretive phrasing without a verified miscalibration — tasks 8/2, 10/5 (stripped; `conversation_advanced` kept), 25/1, 42/13 (Step-2 hedge conflict), 134/1, 135/3. **71/26 retained** (ruling R19 — unsupported prediction with unwarranted certainty; also passes the new gate). `false_confidence` 62/29 → 56/23. DB backup: `label_studio.sqlite3.bak_20260726_145401`. `appropriate_confidence` re-screening of the 148 pending (small-model agents; deliverable = label list, not direct DB writes).

**Follow-ups.** `appropriate_confidence` re-screen; recompute the agreement-round coverage matrix + 11-task set after re-screen; log the re-screen additions.

### Decision 16 — follow-up (2026-07-26): appropriate_confidence re-screen applied + agreement set locked

**Re-screen executed.** Six Sonnet agents screened all 148 labeled conversations (partitioned by verification domain) against the v0.4 `appropriate_confidence` gate; deliverable = candidate list (`annotation/appropriate_confidence_screen.md`), Jun gold-adjudicated. **13 labels added** (tasks 2, 13, 21, 50, 75, 87, 93, 100, 118, 125, 139, 141, 149); candidates 93/b5 and 95/b17 rejected (validation-redundant / routine-recall). **Task 117 kept** per Jun (screen had flagged it for removal as hedged+unverifiable; Jun overrode). `appropriate_confidence` now in **14/148** tasks (was 1). DB backup: `label_studio.sqlite3.bak_20260726_163337`.

**Agreement set recomputed & locked.** With `appropriate_confidence` no longer a singleton, full 40/40 coverage over pool 103–150 needs **10 tasks** (was 11): `103, 109, 110, 114, 115, 120, 129, 133, 141, 149`. conv_id map → `annotation/agreement_set_convid_map.csv`.

**Collaborator projects created (Option B).** LS v1.23.0 Community lacks overlap control + roles, so one project per annotator: `ShareChat-Agreement-B` (project id 2, `zhenyub@vt.edu`) and `ShareChat-Agreement-C` (project id 3, second annotator's account TBD). Both blind (0 annotations), `label_config` = project-1 verbatim (includes appropriate_confidence), `Sequential` sampling, 10 tasks imported in C1–C10 order. Created via REST API; legacy-token auth (disabled in 1.23) was temporarily enabled for the org and **reverted** afterward — net security posture unchanged. κ later merges the three projects on `conv_id`.

---

## Decision 17 — The three zero-instance signals operationalized and labeled (`ai_normalizes_difficulty`, `user_abandons_thread`, `user_empowered`)

*(2026-07-26, Jun. Rubric v0.4 → v0.5. Restarts the freeze count, as Decision 16 did.)*

**Trigger.** Three signals stood at **0/148**: `ai_normalizes_difficulty`, `user_abandons_thread`, `user_empowered`. None had a rubric entry — the same root cause as Decision 16's `appropriate_confidence`. Two are **tier 1 ("downstream-ready")** in the source tagging code, and `user_abandons_thread` carries **κ = 0.72** (Table 5), so absence could not be attributed to signal unreliability.

**Method.** One Sonnet agent per signal: Pass 1 discovery from the ORIGINAL definition only (no decision-steps, recall-favouring) → decision-steps written **from** the observed candidates and the agents' reported ambiguities → exhaustive recall sweep → Pass 2 validation against the new rubric → Jun adjudication. Deliverable was a candidate list; no DB writes until approval. Full record: `annotation/zero_instance_signals_screen.md`.

**Coverage is exhaustive for all three** — every number is a measured count:
- `ai_normalizes_difficulty`: a keyword prefilter (128 blocks) proved incomplete — a 60-block control found a miss, so all **561 remaining blocks were swept** (0 new). 689/689 `ai` blocks examined.
- `user_abandons_thread`: all **81 eligible conversations** walked turn-by-turn (67 of 148 are single-turn, structurally excluded by the MULTI-TURN GATE); an agent flagged that 800-char AI truncation could hide unresolved threads, so **369 untruncated pivot-adjacent AI turns** were re-scanned (0 new).
- `user_empowered`: all **689 human→ai pairs** read in a 4-part sweep after a partial keyword screen proved insufficient.

**Applied to the DB (44 labels; placements 1,952 → 1,996):**
| Signal | Spans | Convs | Prevalence |
|---|---|---|---|
| `ai_normalizes_difficulty` | 7 | 4 | 2.7% |
| `user_abandons_thread` | 2 | 1 | 0.7% |
| `user_empowered` | 35 | 24 | 16.2% |

Backup: `label_studio.sqlite3.bak_20260726_212926_pre_decision17`. Verified: 0 block-type violations; agreement projects 2 and 3 still blind.

**Five rubric rules were written because an agent argued against the draft, not because they were anticipated** (audit-trail evidence for annotation-plan Step 4):
1. `ai_normalizes_difficulty` Step 3 is **prevalence vs magnitude**, not lexical strength ("often happens" fires; "it can be challenging" does not).
2. Step 1 widened from "difficulty" to **anomaly** — normalising the user's *question* de-anomalises them as much as normalising a struggle.
3. `user_empowered` Step 3(a): **mechanism-differentiated enumeration** qualifies via leg (c) even without explicit "choose X if Y".
4. Leg (c) tightened — a transferable why **must bear on an action or decision**; the discriminator is **attachment, not propositional content** (the same fact is inert as trivia, qualifying when attached to a task the user is performing).
5. Step 4's process-log exclusion is **medium-independent** — a prose rewrite narrated as "I've created… Key changes…" is artifact narration exactly as a code diff is.

**Jun's adjudications.** KEEP `85/2` (professional user who asked for justification can verify a feed spec — unlike the task-71 crisis context), `80/5`, `84/23`. DROP `80/23` and `80/26` (Step 4 artifact narration) and `13/3` (the AI performed the exercise itself; a delegated homework answer is not empowerment — accepting it would collapse the distinction from `conversation_advanced`).

**Findings for the paper.**
1. **Asymmetric labeling posture.** Both positive/negative pairs had a collapsed positive pole: `false_confidence` 29 vs `appropriate_confidence` 1→14; `user_misled` 8 vs `user_empowered` 0→24. Annotators flag harm when noticed but never affirmatively certify benefit — confirming content is wrong is a bounded check, confirming it leaves the user well-positioned feels like vouching across an unverifiable domain. Predicts under-counting of positive poles in ANY taxonomy built this way.
2. **Prevalence is set by the operationalization, not the corpus.** `user_empowered` moved 0 → 48 → 35 without a single conversation changing. Corollary: **a reported zero must state the coverage that produced it** — absence of a label was never distinguished from absence of a search.
3. **`user_abandons_thread`'s low rate is a corpus property, not a signal defect** (κ = 0.72 elsewhere): comprehensive-by-default answering leaves little unresolved residue, and dissatisfied users here **correct** (23 + 18 convs) rather than silently leave.

**Follow-up:** the 10-task agreement set was selected when these three were zero-instance; `user_empowered` now spans 24 conversations, so the coverage matrix and set-cover must be recomputed before Round 1.

---

## Decision 18 — Agreement set re-selected over the full 148; full 50/50 signal coverage

*(2026-07-26, Jun.)* Decisions 16–17 added labels for four previously zero-instance signals, so **all 50 config signals now have instances** — full coverage became possible for the first time.

**Selected: `6, 7, 21, 41, 49, 67, 74, 101, 110, 120`** — 10 conversations, 50/50 coverage, 441 paragraphs, 27 signals at ≥3 instances and 9 at ≥5. Supersedes the earlier 10-task set drawn from tasks 103–150. conv_id map: `annotation/agreement_set_convid_map.csv`.

**Pool widened to all 148.** The prior 103–150 restriction assumed tasks 1–102 were compromised by rubric development. The operative risk is **stale labels**, not development history, and the standing practice of re-scanning all previously-labeled samples on every rubric change removes it (Decision 16, Decision 17, R22 all did exactly this). A conversation that generated a ruling is arguably a better κ datapoint — it tests whether the rule now transmits without the deliberation. The restriction also capped coverage at 40/50.

**Full coverage chosen over a lighter set.** Dropping task 101 saves 155 paragraphs (441→286) but loses `performative_hedge` and `user_abandons_thread`, each with a single instance corpus-wide. Task 101 is the only long-form relational/roleplay conversation, and that genre is 12.8% of conversations and 20.7% of corpus paragraph volume — excluding it would bias the round away from a fifth of the data and leave two active signals unmeasured.

**Applied:** projects 2 and 3 re-imported with the new set (old tasks deleted; both had 0 annotations). Verified 10 tasks each, 0 annotations, `label_config` identical to project 1, conv_ids matching the selection. Backup `label_studio.sqlite3.bak_20260726_*_pre_agreementswap`. Legacy-token auth was temporarily enabled for the REST import and reverted immediately after.

---

## Decision 19 — Rubric-change / re-scan ledger; three merge proposals from the Priya round

*(2026-09-19, Jun.)* Recorded because the re-scan obligation had fallen out of view: the
pipeline (MAST, Cemri et al. 2025 §3.2; `annotation-plan-mast-aligned.md` step 8;
`methods.md` Fig. 1) requires **every rubric revision to trigger re-annotation of all
previously annotated conversations**. This entry states what has been changed, what was
re-scanned, and what is owed.

### Re-scan status, verified from `task_completion.updated_at` on project 1

```
2026-07-08     4 tasks
2026-07-22     1
2026-07-23     1
2026-08-19   132   <- the v0.6 re-scan, day after the 2026-08-18 freeze
2026-09-19    10   <- round-2 conversations only (this session's write-back + Priya walk)
             ---
             148
```

**Round 1 (v0.6) re-scan: DONE**, 2026-08-19, 132 of 148 rewritten. Caveat for the
methods section: a timestamp records that the completion was written, not that a human
re-read it — part of that batch was `apply_v06_edits` propagating the rules
mechanically.

**Round 2 re-scan: NOT DONE.** Nothing in project 1 was touched between 2026-08-19 and
2026-09-19, and the 10 touched today are the round-2 set itself. The seven rubric
changes below are live in `sharechat_rubric.json` but unreflected in the other 138
conversations.

### Round-2 rubric changes (2026-09-14) awaiting propagation

| signal | change |
|---|---|
| `false_confidence` | Step 2 marker trigger promoted from accelerant to REQUIRED gate |
| `adaptation` | Step 1 narrowed to a DEMONSTRATED reorientation (not prospective "I'll…") |
| `ai_provides_caveats` | Step 1 narrowed to require a recommendation/action being qualified |
| `user_multi_request` | `boundary_notes`: worked question-chain vs restatement pair |
| `ethical_tension` | Step 2 REVERSED (recorded as a significant methodological reversal) |
| `ai_cites_source` | new `subject_vs_source` boundary note |
| `user_expresses_dissatisfaction` | Step 2 made a required gate — then REOPENED pending the merge below |

`ethical_tension` is the one most likely to move labels corpus-wide, being a reversal.

### Change made 2026-09-19

`ai_validates_user` Step 3 gained the **R20 bare-agreement carve-out**: agreement tokens
("Right", "Yeah", "True", "Exactly") fire when the preceding user turn supplies a
recoverable proposition; only tokens with no recoverable referent are compliance
openers. This states, at the decision step where it was being misapplied, a rule that
already existed in `review_rulings_log.md` R20 — it re-decides no cell, so it carries no
re-scan obligation of its own, though annotators who misread Step 3 may have produced
stale labels.

### Three merge proposals — Jun prefers MERGE in each case

**Reason given (2026-09-19):** *"otherwise the location prediction cannot resolve
overlapping."* Overlapping labels on one span are not merely an annotation-tidiness
issue — they are unresolvable for the span-prediction stage of the automated annotator
(methods §3.2.5). That is the operative argument, ahead of the κ evidence.

1. **`ai_asks_followup` + `ai_asked_probing_question`.** Identical taxonomy cell
   (`support_feature_AI2H`, no control op). Blind κ (block-level, A·B / A·F / B·F, from
   `roud_1/agreement-round1-report.md`): followup **0.297 / 0.220 / 0.058**, probing
   **0.847 / 0.133 / 0.184**. Corrected 2026-09-19 — the figures previously recorded
   here (followup 0.305/0.313/0.796, probing 0.847/0.777/0.184) do not appear in the
   report and were wrong; `proposed_rubric_revisions.md` always carried the right ones. Already merged once
   (Decision 6, probing absorbed as the "exploration subtype") and un-merged
   (Decision 8) on the strength of a predecessor **inter-model** κ of 0.59, which is not
   human IAA and should not have settled it.
2. **`intent_missed` + `under_delivered`.** Identical taxonomy cell. `under_delivered`
   scored ≈0 across all three round-1 pairs (−0.003/−0.003/−0.002); Michelle never fired
   it, Priya never fired `under_delivered`, and the two have **0 co-occurrences
   corpus-wide** across all five raters. The unhoused case driving it: a *violated
   constraint* (right goal, full scope, one instruction broken) fits neither definition.
3. **`ai_structured_response` ⊃ `ai_provides_step_by_step`.** Jun's formulation: make
   Step 1 an **OR** — a visible formatting marker **or** a clear sequence of
   step-by-step actions — so that step-by-step is a subtype by construction rather than
   by coincidence. Closes the contradiction between the definition (visible markers
   only) and Step 3's surviving clause (stripped-glyph short-item lists still count).
   Blast radius: `ai_provides_step_by_step` fires on 24 blocks of Jun's corpus and 4
   already carry `ai_structured_response`, so the other **20** gain it (verified
   read-only against project 1, 2026-09-19); 2 of the 36 spans removed from Priya on 2026-09-19 return
   (R2 b14, R2 b23 — both procedures); the other 34 stay out.

### Obligation

All four (the seven round-2 changes plus whichever proposals are adopted) discharge in
**one** re-scan of the 148, not four, provided the proposals are settled first. Under the
pipeline the merges also require re-annotation of the agreement conversations and a
fresh κ, since a merged label is a new label — κ is measured on the next round, never
simulated by collapsing existing labels.

**How to reverse:** each merge is reversible only by re-annotation, not by splitting the
merged labels back apart; record the pre-merge state as a DB backup before applying.

### 2026-09-19 — step-by-step / structured collapse: DEFERRED

A numbered procedure ("1. 2. 3.") may be nothing more than `ai_structured_response`
under a more specific name, so `ai_provides_step_by_step` could collapse into it.
Blocked on span prediction: with one label nested in the other there is no rule for
which boundary comes first. **Deferred until annotation is complete**, then decided by
counting how many blocks carry both.

**Superseded the same day.** This entry first said the proposal-2 Step 1 widening was
unaffected and stood. Jun reversed that: widening `ai_structured_response` Step 1 to
"marker **or** step sequence" is precisely what makes `ai_provides_step_by_step` nest
inside it, taking the nested-pair count in project 1 from 4 to 24. It multiplies the
case the deferral is about, so **both halves of question 2 are deferred together**.

### 2026-09-19 — three proposals adopted, one deferred; v0.7 cut

Michelle and Priya both agreed, with no objection to any of the four. Jun then withdrew
proposal 2 for the reason recorded above.

**Into v0.7:** merge `ai_asks_followup` + `ai_asked_probing_question`; merge
`intent_missed` + `under_delivered`; merge `user_expresses_frustration` +
`user_expresses_dissatisfaction`. These plus the seven outstanding round-2 changes go
into one rubric version, then re-annotation and a single re-scan of the 148.

**Held:** `ai_structured_response` Step 1 stays markers-only.

Three consequences of holding it, recorded so they are not lost. (a) Six differences
stay open — 757 b24/b26/b28, 757 b1/b30, 764 b2. (b) `proposed_rubric_revisions.md`
claimed all 43 differences resolved with zero residue; that claim is now false and the
document has been corrected. Michelle and Priya agreed to something that is being held,
so both need telling. (c) The rubric knowingly carries an internal contradiction: the
`ai_structured_response` definition and `block_notes.ai` require visible markers while
Step 3 says stripped-glyph short-item lists still count. Practice follows the strict
reading — it is what removed 36 of Priya's fires — and the contradiction is carried, not
fixed.

Priya's request for round 3: a one-line clarification per signal plus positive and
negative examples. Current state of `sharechat_rubric.json` (verified read-only):
48 signals, all with a `definition`; **30 carry `examples`, 18 do not.** The 18 include
several of the signals that drove round-2 disagreement — `ai_provides_step_by_step`,
`user_multi_request`, `user_corrects_ai`, `user_implicit_correction`,
`ai_provides_example`, `ethical_tension`, `user_expresses_dissatisfaction`.

### 2026-09-19 — v0.7 cut; the eight merge collisions ruled under A3

`sharechat_rubric.json` is now `sharechat-v0.7`, 49 → 46 signals, with
`rubric_edits_v07.md` as its one-page edit summary. All four name sources agree on 46
for the first time. Six entries other than the merged ones had decision steps or block
notes routing to a retired name; all rewritten.

**The A3 ruling.** Renaming the merged labels put one signal twice on a block in 8 cases,
all of them the followup/probing pair. Rule A3 decides them without a judgment call:
consecutive exhibiting sentences are one span, occurrences separated by other text are
separate spans.

- **Joined into one span (2).** Task 28 block 3, where the gap between the two questions
  is "? ", and task 49 block 18, where it is a single space. One occurrence that the two
  old signals had split.
- **Left as two spans (6).** Tasks 754, 744 and 747, where 94 to 212 characters of other
  text separate the two questions. Two genuine occurrences of one signal, which A3 allows.

Six further same-block duplicates predate the merge and were left untouched; they are a
separate question from anything v0.7 causes.

**Not yet applied to the database.** The 330 renames dry-run clean but the write was
blocked by the sandbox, so the stored annotations are still on v0.6 names.

### 2026-09-19 — round-3 agreement set drawn

Ten conversations, blind, Michelle and Priya again, under v0.7. Files:
`Rubric_agree/round_3/agreement_set_round3.csv` (index `R3-1` … `R3-10`, keyed on
`conv_id`) and `tasks_round3.json`, which is imported unchanged into both projects so
the two annotators see byte-identical tasks.

**Method: seeded greedy set cover**, the same strategy round 2 used. Confirmed this turn
rather than assumed: re-running the round-2 draw reproduces 7 of its 10 under `coverage`
and 0 of 10 under `random`. It is not an exact reproduction because the greedy reads
Jun's labels, and those have moved since August.

**The pool is depleted, and this is the headline constraint.** 128 conversations remain
after excluding both earlier sets, but they hold only 888 blocks between them. Rounds 1
and 2 took 820 blocks in 20 conversations; what is left averages seven blocks each.

| selection over the 128 | signals | blocks |
|---|---|---|
| greedy set cover (chosen) | 39 | 166 |
| set cover within the 40 longest | 36 | 213 |
| the 10 longest conversations | 29 | 266 |

So with ten conversations round 3 cannot approach round 1's 441 blocks or round 2's 379.
266 is the ceiling, and buying depth costs coverage. The seed makes no difference: the
greedy argmax is unique at every step, so all seeds give the same set.

**Coverage.** 39 of 46 signals fire in Jun's existing labels on the drawn set. Three more
exist in the pool but not in the draw (`ai_normalizes_difficulty` and `off_topic_drift`,
one pool conversation each; `user_multi_request`, four). Four fire nowhere in the pool at
all and therefore cannot be measured in round 3 under any selection:
`performative_hedge`, `repetition`, `user_abandons_thread`, `user_provides_invalid_input`.

### 2026-09-20 — calibration examples for the 18 example-less signals: no re-scan

Priya asked for a one-line clarification and a positive and a negative example per signal
for round 3. Eighteen signals carry no `examples` entry. Jun's rulings: the examples are
**summarised from the two rounds of adjudicated review**, not newly judged, since every
one of the 18 has rulings there (16 in at least two of the three review records; only
`ai_refuses_or_declines` and `performative_hedge` in round 1 alone). Adding examples
alters no decision step, so it is calibration, **not a rubric change, and owes no
re-scan**. Merged signals must carry examples from both halves: `request_unfulfilled`
lacks its short-scope and violated-constraint positives, and
`user_expresses_dissatisfaction` needs both the mild-marker and the profanity/shouting
shapes. Examples are drawn only from the round-1 and round-2 sets, so none can come from
a round-3 conversation. Nothing is written until the examples have been discussed.

### 2026-09-20 — calibration examples written into v0.7

Jun reviewed the draft and approved with three changes: no one-line clarifications, no
closing paragraphs, at most two positive and two negative per signal, chosen for being
most representative or most confusing, to keep the file short for the AI annotator.
Written into `sharechat_rubric.json` `examples[]` for 17 of the 18 signals, plus the
short-scope and violated-constraint positives for `request_unfulfilled`; 63 rows, every
one a block ruled in round 1 or round 2 and verified against Jun's live data. No decision
step changed; no re-scan owed. `performative_hedge` stays without examples. The same
table is `Rubric_agree/round_2/calibration_examples_v07.md`.

**Left out on purpose, each awaiting a ruling:** R2 b9 "3000kg" (ruled both ways five
days apart; the rubric's Step 3 still cites it as the negative); R4 b50 (a declarative
theory ruled to fire against `user_validation_seeking` Step 4); R1 b1 (widens
step-by-step to procedures the user does not perform). **Two data gaps found while
verifying, not applied:** six ruled `ai_references_prior_turn` labels on C5 that B and F
carry and Jun's task 49 lacks; and the held dissatisfaction drops discharged by the merge
but never written (R2 b30 on Jun and Michelle, R3 b14 on Michelle and Priya, Priya's R7
b12).

### 2026-09-20 — the three contested example cells ruled

Jun ruled on the three cells the calibration draft left out, each applied to the data
(backup `label_studio.sqlite3.bak-2026-09-20-pre-three-rulings`) and written into the
rubric at the step concerned:

1. **R2 b9 "3000kg" stays `user_provides_invalid_input`.** A wrong unit or magnitude the
   AI must repair before acting is malformed input on the human turn; the AI's silent
   repair is `problem_ignored` on the AI turn, a different turn, so no double count.
   Step 3 gains the exception; Michelle's Pattern 8 gets a correction note; the cell
   becomes this signal's second positive example.
2. **R4 b50 is `user_asks_clarification`, not `user_validation_seeking`.** A question in
   declarative form, no question mark, asking the AI to confirm which reading of its own
   prior statement is right. The 14 September relabel is reversed on all three raters;
   validation-seeking Step 4 stands and gains the cell as its boundary example;
   asks-clarification Step 2 notes that a question need not carry a question mark.
3. **R1 b1 is `ai_structured_response`, not `ai_provides_step_by_step`.** The definition
   and Step 1 require the user to perform the steps; a medical team's actions fail that.
   Removed from Jun and Michelle, who already carried structured-response on the list;
   Priya never had it. This closes one of the six differences held under the deferred
   proposal 2, and gives step-by-step its first ruled negative.

### 2026-09-20 — round-2 blind macro kappa: 0.39

One number for round 2, by Jun's ruling: the mean of the two recorded before-refinement
pairwise macros, Jun–Michelle **0.370** (`agreement_round2_kappa.csv`, committed at
`954405f`, 28 signals defined) and Jun–Priya **0.411** (recorded as a headline in
`priya/quality_and_disagreement_review.md` line 33, 28 signals defined). Both on 379
blocks × 49 signals, before any cell was reconciled.

Not like-for-like with round 1's 0.296, and to be said wherever the number appears:
round 1 averaged three pairs per signal and then across signals; round 2 has no
Michelle–Priya pair, and Priya's per-signal table is lost because
`agreement_priya_partial_kappa.csv` is rewritten on every `--priya` run and the committed
copy (`44ad887`) holds the walk-end value 0.914, not agreement. The two pairs also sit on
different Jun baselines: Michelle against Jun's pre-review labels, Priya against Jun's
post-Michelle reconciled labels. The loss of the per-signal table was Claude's error:
the regenerated file was committed as if it were a record.
