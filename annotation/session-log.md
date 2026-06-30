# Annotation Session Log

Running log of annotation discussions between Jun and Claude. Each entry is verbatim — the actual exchange, not a summary. For labmates to use as reference when boundary cases come up.

Rubric: `sharechat_rubric.json` | Guide: `ANNOTATION_GUIDE.md`

---

## Session — 2026-06-29 (Tasks 28 continued, 29)

---

### Task 28 — Two-sentence unit, only one labeled

**Context:** AI turn 2 ended with two questions together. Claude had only put the second question in the table.

**Jun:**
> I didn't find this sentence, but just two sentences you not labeled. the actual sentences are "Does this perspective align with your thinking about this timeframe? And are there particular technological developments you see as most disruptive to existing power structures?"

**Claude:**
These two sentences appear together in the text as one unit. In my table I only showed the second sentence, but the annotator needs to know what to do with both.

- *"Does this perspective align with your thinking about this timeframe?"* → 0 (yes/no; `ai_asked_probing_question` Step 5 requires open-ended; this fails)
- *"And are there particular technological developments you see as most disruptive to existing power structures?"* → `ai_asked_probing_question` = 1 (genuinely open-ended)

**Jun:**
> this is a question, should fit into a signal. i disagree with you. double check rubric AND the original signal definitions.

**Claude (after re-reading rubric):**
Step 3 only routes away yes/no questions that are **specific new action offers** — "Is the question a yes/no offer to take a specific new action not yet done?" "Does this perspective align?" proposes no action. Step 3 = NO → continue to Step 5. The question invites the user to reflect and redirect if the framing doesn't match. Step 5 fires. Changed "Does this perspective align?" to `ai_asked_probing_question` = 1.

**Jun:**
> please reverse your update of rubric, still disagree with you. "align" is action, the ai ask WHETHER, align or not align.

**Resolution:**
"Align" is an implicit action — the AI is asking whether to HOLD or ADJUST its current framing. That makes this a yes/no decision about an action → `ai_asks_followup` (Step 3 of `ai_asked_probing_question`: "yes/no offer to take a specific new action not yet done → `ai_asks_followup`"). Rubric boundary note updated accordingly (not the one Claude had added — that one was reversed).

Final labels for AI turn 2:
- *"Does this perspective align with your thinking about this timeframe?"* → `ai_asks_followup` = 1
- *"And are there particular technological developments you see as most disruptive to existing power structures?"* → `ai_asked_probing_question` = 1

**Rubric change:** Added `boundary_notes.yes_no_alignment_check` to `ai_asked_probing_question`: yes/no questions asking whether the AI's framing/perspective/approach aligns → `ai_asks_followup`. "Align" is the implicit action (hold or adjust framing).

---

### `ai_asks_followup` vs `ai_asked_probing_question` vs "asking for feedback" — three-way boundary

**Jun (raised separately during task 28):**
> I feel the two questions should be, `ai_ask_follow_up` and `ai_ask probing questions`. how should we distinguish with the ai ask feedback?

**Resolution:**

| Type | Key marker | Example |
|---|---|---|
| `ai_asks_followup` | Yes/no offer for a **specific new action** not yet taken | *"Should I run the sector calculations?"* |
| `ai_asked_probing_question` | Question inviting user to **reflect or steer** — no action proposed | *"What direction would you like to take this?"* |
| Feedback/satisfaction check | Politeness closer — checking if output was adequate | *"Was that helpful?"* → **no signal** |

**Decisive test:** What would a YES answer commit the AI to?
- YES → AI does a specific new thing → `ai_asks_followup`
- YES → continue same direction; NO → redirect → `ai_asked_probing_question`
- YES → nothing changes → no signal

---

### Task 29 — `ai_offered_options` vs `ai_provides_example` + `ai_asked_probing_question`

**Context:** AI turn 1 contained: *"For instance, we could dive deeper into: How the granular synthesis parameters work / The function tables and their purposes / How the score parameters affect the sound / The modulation systems used. What aspect interests you most?"*

Claude labeled the list as `ai_offered_options` = 1 and the closing question as `ai_asked_probing_question` = 1.

**Jun:**
> if these two put together, it will be `ai_offered_options`. but if separate, the first part is `ai_provides_example`, and the second is probing question. which set is correct?

**Resolution:**
The "For instance" prefix is decisive. `ai_provides_example` Step 2: *"Is it introduced by framing language such as 'For example:', 'such as', 'like', or similar? If YES → strong signal for label 1."* "For instance" = that framing. The list illustrates possible directions, not a closed choice menu.

- *"For instance, we could dive deeper into: [list]"* → `ai_provides_example` = 1
- *"What aspect interests you most?"* → `ai_asked_probing_question` = 1

`ai_offered_options` fires when the AI presents a closed named-choice menu **without** the "For example/instance" framing. When "For instance" is present → `ai_provides_example`.

---

### Task 29 — `ai_normalizes_difficulty` vs `ai_flags_complexity`

**Context:** AI turn 3 (AI 2 in task 29): *"Granular synthesis can be complex but it's really fascinating once you start experimenting with the different parameters."*

Claude labeled this as `ai_normalizes_difficulty` = 1.

**Jun:**
> this shows "but fascinating", not "but easy". so I don't think this is normalizes difficulty?

**Resolution:**
`ai_normalizes_difficulty` requires framing difficulty as **surmountable or expected** — "it's hard but it gets clearer," "the struggle is normal." "Fascinating" is an aesthetic judgment (interesting, engaging), not a reduction of difficulty. Correct signal: `ai_flags_complexity` = 1 — the sentence acknowledges the domain is complex.

**Boundary:**
- `ai_normalizes_difficulty`: difficulty framed as manageable or expected ("complex but it gets clearer with practice")
- `ai_flags_complexity`: difficulty acknowledged, not reduced ("granular synthesis can be complex")
- "Fascinating" ≠ normalizes difficulty

---

### Task 31 — `ai_hedges_uncertainty` vs `ai_asserts_knowledge_limit` when AI searched and found nothing

**Context:** AI ran 4 web searches and reported "there's no clear evidence that alternative search engines pay Apple." Claude labeled this as `ai_hedges_uncertainty` ("no clear evidence" = epistemic downgrade).

**Jun:**
> the evidence is in the searching results the ai read. this is examples?

**Resolution:**
"No clear evidence" after 4 web searches is not the AI hedging a claim from its own knowledge — it's reporting that the searches returned no definitive information. The AI is asserting that the information isn't publicly findable. That's `ai_asserts_knowledge_limit`, not `ai_hedges_uncertainty`.

**Boundary clarified:** `ai_hedges_uncertainty` requires the AI to be making a claim from its own knowledge and hedging its confidence in that claim. When the AI ran searches and reports the information doesn't exist publicly → `ai_asserts_knowledge_limit`. The key test: is the AI uncertain about a claim IT is making, or is it reporting the absence of findable evidence?

---

### Task 31 — `ai_provides_caveats` scope: applicability constraints, not just recommendations

**Context:** AI mentioned the EU "pay to play" search engine system in sentence 8, then said in sentence 9: "However, this refers to the EU's mandated choice screen for Android devices, not iOS." Claude flagged this as potential `ai_provides_caveats` but was uncertain — the annotation guide says "qualifies a recommendation" and this is a factual clarification.

**Jun:**
> this should be a caveat that exists in the facts the AI described? can be similar with the mechanism limitation which is classified as caveats.

**Resolution:**
`ai_provides_caveats` fires here. The rubric definition is broader than "recommendation": "AI qualifies its response or the information it is working with using conditions, limitations, or temporal constraints — flagging a limitation of the content or analysis." Step 1: "Is the AI adding a qualifying condition — applicability ('applies only if')?" The EU/Android information has limited applicability — it does not apply to iOS, which is what the user asked about. Step 1 fires.

**Rule established:** `ai_provides_caveats` covers any spontaneous qualification of information the AI just presented — temporal ("may be outdated"), applicability ("applies only if X", "this is for Android, not iOS"), scope ("this is for EU, not US"). It is not limited to recommendations.

---

### Task 31 — apparent garbled text ("in S") was a copy-paste line-break artifact

**Context:** The AI summary paragraph appeared to read "while Google pays billions to be the default search engine in S no clear public information." Claude flagged this as possible `ai_malfunction`.

**Jun:**
> I didn't find "in S". only "in Safari" is in response. this might be the line breaking issue when I copy paste.

**Resolution:**
No `ai_malfunction`. The "in S" was a copy-paste formatting artifact — the original text reads "in Safari, there is no clear public information" (or similar). When apparent garbling appears in a pasted task JSON, verify against the source before labeling `ai_malfunction`.

---

---

## Session — 2026-06-29 (Task 36)

---

### Task 36 — `user_corrects_ai` on first human turn

**Jun:**
> this is the first span, nothing to correct AI. this is confusion is due to the limitation of this dataset that user uploaded files are not included, it is the pricing calculation aria-sort in this conversation. so correct the wrong calculation is a task in this conversation not to correct the ai. we need treat this scenario differently.

**Claude:**
Good catch — this is the first human turn in the conversation. There is no prior AI output to correct. The user uploaded a pricing calculator file (not included in the dataset) and is pointing out an accessibility issue they want fixed. That is a task instruction, not a correction of the AI. `user_corrects_ai` requires a prior AI error within this conversation. No prior AI turn → `user_corrects_ai` = 0. This cascades: `ai_acknowledges_correction` = 0, `error_recovery` = 0.

---

### First-turn constraint on Purple signals

**Jun:**
> We need be aware of the signals that on the user side will not happen in first prompt.

**Claude:**
A subset of Purple signals structurally require a prior AI output — they can never fire on the first human turn:
- `user_corrects_ai` — no prior AI statement to correct
- `user_implicit_correction` — no prior AI output to correct indirectly
- `user_repeats_request` — no prior request the AI failed to fulfill
- `user_positive_feedback` — no prior AI response to affirm
- `user_asks_clarification` — no prior AI output to ask about

These five → automatically label 0, skip decision steps, whenever the human turn is the first turn in the visible conversation.

Purple signals that CAN fire on turn 1: `user_ambiguous_request`, `user_multi_request`, `user_expresses_frustration`, `user_expresses_dissatisfaction`, `user_provides_invalid_input`.

**Jun:**
> yes, please add this constraints into the rubric. session log should be raw conversation between us.

**Rubric change:** Added two entries to `global_placement_rules`: (1) first-turn constraint listing the five blocked signals and the ones that can still fire; (2) missing-context constraint — when prior turns or file uploads are absent from the dataset, treat the human turn as a new task request, not a correction or repeat.

---

## Session — 2026-06-29 (Task 32)

---

### `ai_malfunction` placement in agentic conversations — analysis block with pairing rule

**Context:** Task 32 contains three tool call failures visible in analysis blocks (HTTP 401 on two tools in turn 1; edit_block "Exact match not found" in turn 6; HTTP 422 on `gh api` in turn 8). Claude initially labeled the AI sentences "Let me try a different approach..." as `ai_malfunction`, and the analysis blocks as having no signal (since the annotation guide's analysis block list doesn't include `ai_malfunction`).

**Jun (correction 1):**
> the 401 part should be the `ai_malfunction`? "Let me try using a different approach..." this sentence should be `error_recovery`? also for "Let me try with a more precise edit..." and "Let's try a different approach to enable GitHub Pages."

**Resolution:**
`ai_malfunction` fires on the **analysis block** where the failure actually occurs. The AI sentence that responds to the failure ("Let me try another approach") → `error_recovery` on the **ai block**. The annotation guide's analysis block list was incomplete for agentic conversations.

**Jun (refinement):**
> we should update this, but with restriction. Only error recovery in ai response appears, we find corresponding malfunction. otherwise, the error might just be the ai different tries that doesn't affect the response.

**Pairing rule established:**
Label `ai_malfunction` on the analysis block **only** when a corresponding `error_recovery` is present in the paired AI block of the same turn. If a tool call fails silently (the AI proceeds without acknowledging the failure, no `error_recovery` in the AI block), the failure is an uninformative alternative try — label 0 on both analysis and AI blocks.

**Pattern:**
```
analysis block: ai_malfunction = 1   ← tool call failed (HTTP error, match error, etc.)
ai block:       error_recovery  = 1   ← "Let me try a different approach..."
```
Both must appear to label either. No paired error_recovery → no ai_malfunction.

**Rubric change:** Updated `ai_malfunction` entry — added `analysis` to blocks list, added `block_notes.analysis` with pairing rule, added Step 0 / Step 0b to decision steps, added three calibration examples.

---

### Task 32 — "Let me know if you encounter any issues" — no signal

**Context:** AI turns in Task 32 closed with phrases like "Let me know if you encounter any issues or if you'd like to make any modifications to the code!" and "If you encounter any additional errors, please let me know, and I'll help fix them."

**Jun:**
> this kind of "Let me know" should also be treat as question sentence? this is ask feedback or followup?

**Resolution:**
No signal. These are standing offers / politeness closers. Decisive test: what does a "yes, there are issues" commit the AI to? — nothing specific; the AI would wait for the user to describe the problem. This is the same pattern as "Was that helpful?" which falls under excluded `ai_asks_for_feedback` (κ=0.09 < 0.4).

Contrast with `ai_asks_followup` (e.g., "Would you like me to make any additional changes?") — YES commits the AI to a specific new action. "Let me know if you have issues" does not propose a specific action and is not yes/no. Label 0.

---

### Task 32 — "Next Steps for GitHub Pages Deployment" (AI 7) — not `ai_provides_step_by_step`

**Context:** AI turn 7 response (responding to "add readme / prepare for publishing to github") included a "Next Steps for GitHub Pages Deployment" section with numbered items (1. Create a GitHub Repository, 2. Update Repository Information, 3. Initialize and Push...).

**Jun:**
> this step by step is internal thinking, not "provides" to user.

**Resolution:**
`ai_provides_step_by_step` = 0 for this section. The AI had already written a `GITHUB_PAGES.md` file containing these steps. The numbered list in the AI text is a recap/summary of that file's content — it's the AI narrating its own prior work, not delivering the steps as the primary instruction. The actual "providing" happened in the written file.

Contrast with AI 8 (manual GitHub Pages steps): the API failed and no file was written; the numbered steps in AI 8 ARE the primary delivery to the user as a workaround. `ai_provides_step_by_step` = 1 there.

**Boundary:** `ai_provides_step_by_step` fires when the numbered steps ARE the answer/delivery to the user, not when the AI is summarizing prior work already captured in a written artifact.

---

## Running boundary reference

| Pair | How to distinguish |
|---|---|
| `false_confidence` vs `ai_hedges_uncertainty` | Mutually exclusive on one sentence. `false_confidence` = no hedge on an uncertain claim. `ai_hedges_uncertainty` = explicit epistemic downgrade ("I think", "likely"). Can appear in same turn on different sentences. |
| `ai_flags_complexity` vs `ai_hedges_uncertainty` | `ai_flags_complexity` = the PROBLEM is hard. `ai_hedges_uncertainty` = the AI's OWN CLAIM is uncertain. |
| `ai_flags_complexity` vs `ai_normalizes_difficulty` | `ai_flags_complexity` = acknowledges difficulty. `ai_normalizes_difficulty` = frames difficulty as manageable/expected. "Fascinating" ≠ normalizes. |
| `ai_offers_to_elaborate` vs `ai_offered_options` | `ai_offers_to_elaborate` = offer to expand the SAME content already provided. `ai_offered_options` = multiple distinct named alternatives for user to choose from (no "For instance" framing). |
| `ai_offered_options` vs `ai_provides_example` | "For instance/example" framing → `ai_provides_example`. Closed named-choice menu without that framing → `ai_offered_options`. |
| `ai_asks_followup` vs `ai_asked_probing_question` | `ai_asks_followup`: yes/no + specific new action. `ai_asked_probing_question`: invites reflection/steering, no action proposed. Yes/no alignment-check ("Does this align?") → `ai_asks_followup` because "align" = implicit action (hold or adjust framing). |
| `ai_asked_probing_question` vs feedback check | Probing = invites reflection/steering; NO answer changes direction. Feedback check ("Was that helpful?") = YES changes nothing. No signal for feedback checks. |
| `user_ambiguous_request` Step 3 | Core task clear even if scope open → lean NO. Don't label 1 just because scope is underspecified if task direction is unambiguous. |
| `ai_hedges_uncertainty` vs `ai_asserts_knowledge_limit` (search results) | If AI searched and reports no evidence found → `ai_asserts_knowledge_limit` (information not publicly available). If AI is making a claim from its own knowledge and hedging it → `ai_hedges_uncertainty`. |
| `ai_provides_caveats` scope | Fires on any spontaneous qualification of information provided: temporal, applicability ("applies only if X", "this is Android not iOS"), scope ("EU not US"). Not limited to recommendations. |
| Apparent garbling in task JSON | Verify against source before labeling `ai_malfunction` — may be a copy-paste line-break artifact. |
| First-turn Purple signal constraint | `user_corrects_ai`, `user_implicit_correction`, `user_repeats_request`, `user_positive_feedback`, `user_asks_clarification` — cannot fire on the first visible human turn (require prior AI output). Label 0, skip decision steps. `user_ambiguous_request`, `user_multi_request`, `user_expresses_frustration`, `user_expresses_dissatisfaction`, `user_provides_invalid_input` can still fire on turn 1. |
| Missing-context constraint | ShareChat omits file uploads and prior sessions. If the first human turn references code or content not visible in the conversation, treat it as a new task request — not a `user_corrects_ai` or `user_repeats_request`. |
| `ai_malfunction` block placement (agentic) | Fires on **analysis block** (tool failure) + **ai block** (`error_recovery`) together. Pairing rule: only label `ai_malfunction` on analysis if there is a corresponding `error_recovery` in the same turn's AI block. Silent failures (no AI acknowledgment) = uninformative alternative try = label 0 on both. |
| `ai_provides_step_by_step` — primary vs recap | Fires when the numbered steps ARE the primary delivery to the user. If the AI already wrote the steps to a file and is just recapping, label 0 (the delivery happened in the artifact). |
| "Let me know if you encounter issues" | No signal. Standing offer / politeness closer — analogous to excluded `ai_asks_for_feedback` (κ=0.09). Contrast: "Would you like me to make changes?" = `ai_asks_followup` (yes commits AI to specific action). |

---

## Format rules

1. **Conversation sequence** — table rows follow H1, AI1, H2, AI2, … Never group by block type.
2. **Every instance** — one row per (turn, block, signal, sentence) where label = 1. Never collapse.
3. **Label = 0 decisions** go in the analysis text, not the summary table.
4. **Rubric branch always wins** — when a step produces a clear NO, that is the answer. Do not substitute independent reasoning.
