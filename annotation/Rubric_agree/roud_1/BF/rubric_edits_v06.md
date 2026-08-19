# Rubric v0.6 — edits expected, and the block that forced each

Round-1 disagreements were walked block by block. Below is every rubric and boundary
edit that resulted, with the source block. Disagree with any line → tell Jun, we discuss.

## A. Rules that apply to every signal

| # | rule | from |
|---|------|------|
| A1 | **Placement is side-only.** AI-side signals may sit on any AI-authored block (ai, reasoning, code, analysis); user-side signals on human blocks. No channel is excluded. | C4 b4–b25, C5 b40, C10 code |
| A2 | **Content vs callback inside reasoning.** Content-bearing signals (claims, hedges, caveats, limits) fire in private planning. Callback/discourse signals need an addressee → ai block only. | C5 b36 (fires), C5 b29/b36 (no callback) |
| A3 | **Granularity.** Fire every block where the behavior occurs. Within a block label every occurrence: consecutive exhibiting sentences = one label/span; occurrences separated by other text = separate labels. One act ≠ many lines (an option list = 1). | C8 b50 (4 labels), C1 b3 (1 label) |
| A4 | **Claim ownership.** Endorsement inherits the claim ("you're absolutely right", "the fact that you…"): evaluate the claim, then route — AI's own claim → `factual_error`; user's claim endorsed/built on → `problem_ignored`. | C8 b20, b112 |
| A5 | **Fiction frame** excludes a signal only when the USER established play. Sincere user → the AI's false self-claims fire. | C9 b80 (excluded), C8 b2/b114 (fire) |
| A6 | **One home per question.** followup / probing / clarifying / offered_options / offers_to_elaborate do not double-fire on the same question. | C1 b7/b9/b11 |
| A7 | `conversation_advanced` is **dropped** (49 signals). Unlabeled = advanced. | — |

## B. Per-signal edits

| signal | edit | from |
|---|---|---|
| `false_confidence` | Fires on an **unhedged** vouch for an unverified deliverable ("I've fixed…", "will definitely work"). A hedge on the claim ("should fix") blocks it. Instructions and feature lists carry no claim. | C10 b15/b42/b45 fire; b5/b7/b12/b18/b33 don't |
| `factual_error` | Covers claims about the **AI's own code/process** (diagnoses, fix rationales, self-reports), not only world facts. Checkable (quote/count) yes; density/style characterizations no. Object-level wrong value files here **only**, not also `false_confidence`. | C10 b12/b15/b54, C4 b8/b11 fire; C7 b3 doesn't; C6 b3–b11 route here |
| `error_recovery` | Restore does_not_count **"New answer also wrong"**: the correction must actually succeed, and the AI must catch the error itself. Fix-after-error-paste is user-caught → `ai_acknowledges_correction`. **Zero fires in the 10** under this rule. | C10 b22 (user-caught b16/b19 — B's catch), C6 b3–b11, C9 b35 all don't |
| `repetition` | Restore does_not_count **"Different approach that also fails"**: same-strategy retry only; a new method is not repetition. | C6 b3/b5/b9/b11/b13 fire; b7 doesn't |
| `conversation_stalled` | STALL TEST becomes **evidence-based**: non-progress must be visible in the user's response (repeat with dissatisfaction, correction/regression call, error persists, claimed-not-delivered, abandonment). Annotator judgment of content quality is not evidence. Play phases fail the goal gate. | C9 b38, C5 b45 fire; C9 b14–b23, b62–b68 don't |
| `user_repeats_request` | **New entry.** Fires on the 2nd+ report of the same **unserved** demand, in any form — restated ("still doesn't work") or re-evidenced (error paste of the same failure). Iteration on delivered output ("make it better") is a new request. | C10 b43/b49, C9 b39 fire; C9 b15–b36 don't |
| `ai_references_prior_turn` | **New entry** = original EXPLICIT CALLBACK TEST: temporal / cross-reference / quote / revision-framing marker, pointing at an earlier turn — **not** the most recent user message. Validation step: the time expression must target the conversation's own timeline (not present generics, not world history). | C5 b18, C8 b157 fire; C8 b12, C1 b3 don't |
| `user_multi_request` | **New entry** = 2+ **independently fulfillable** requests. Check keyword **"also"** (prompt to apply the test, not a trigger): separable ask → fire; same deliverable extended → no. | C10 b25/b34 fire; C1 b12, C3 b6 don't |
| `problem_ignored` | Fires on the **first response after the problem becomes visible**, not later blocks continuing under it. Attempting a fix is the opposite of ignoring. Mentioning it — even evasively — kills the fire. | C1 b1, C8 b20/b112/b150 fire; C10 b9/b15/b45, C8 b48–b134 don't |
| `user_misled` | Unchanged. Gate = **actionable misinformation**: wrong + actionable + material. Influence on beliefs is not the test. | C5 b49 fires (only one); C8 b22–b161 don't |
| `ai_malfunction` | Unchanged. **Mechanical defect only** (truncation, loop, garble, broken format). Aberrant behavior is not a defect. | C5 b40, C10 b29/b38/b50 fire; C1 b1, C8 b2/b120/b136 don't |
| `ethical_tension` | Step 2 rewritten: fire **only** on the reasoning/ai block where the model surfaces the tension. The human block that creates it never fires. Silent compliance = no fire. | C4 b4 fires; C4 b12/b15/b18 don't |
| `ai_hedges_uncertainty` | Check keywords add **"likely"**, **"if…then"**. Still excluded: "appear to / seem to" (reportive), "I believe" (firm). | C10 b12, C4 b28/b29, C7 b3, C5 b36 fire; C2 b1 doesn't |
| `ai_asserts_knowledge_limit` | Covers knowledge, access **and capability** limits ("I can't create GIFs"). Not conclusions from a completed attempt, not noting a missing user input. | C8 b86/b169, C9 b86 fire; C7 b1 doesn't |
| `ai_refuses_or_declines` | **Declining to comply** only (won't). Inability is `ai_asserts_knowledge_limit` (can't). | C4 b23 fires; C8 b86/b169, C9 b86 don't |
| `ai_warns_user` / `ai_provides_caveats` | Warning = a risk the user can act on. Caveat = qualifies the AI's own output or nature. | C10 b7, C5 b37, C4 b29 warn ("emotionally taxing… take care of yourself" — F's catch); C8 b116 caveat |
| `appropriate_confidence` | Gate made testable: routine = a lookup with no competing position live in the conversation. Fires only when the transcript shows hedging or agreeing was the easier path — tells: live opposition, nearby hedging on the topic, diagnosis rather than recall. | C8 b110 fires; C9 b2, C3 b5 don't |
| `ai_structured_response` | Visible formatting only (headers, table, 3+ item list, code block). Multi-sentence paragraphs after a colon are not structure. Never fire on assumed export-stripped formatting. | C2 b1, C3 b3/b5, C7 b1/b3 fire; C6 b15 doesn't |
| `ai_offered_options` | The offer **is the choose-one question**, not the list. An advice list without a question does not fire. | C9 b74–b86 fire; C9 b5 doesn't |
| `ai_provides_example` | Needs a **new supplementary illustration**. Usage instructions for the delivered artifact are not examples (those are `ai_provides_step_by_step`). Discourse **"for example" introducing a topic menu** illustrates nothing — the phrase is not a trigger keyword (B's catch). | C2 b1, C8 b140/b167 fire; C9 b17, C10 b18, C9 b80 don't |
| `ai_acknowledges_correction` | An error paste naming the fault is an **explicit** correction; the AI's fix files here (not `error_recovery`). | C10 b9/b12/b15/b18/b22/b51 |
| `user_corrects_ai` vs `user_implicit_correction` | Naming the concrete defect = explicit correction — the named fault must be a defect in the AI's **output or claim**. Negating a premise/behavior without naming an output fault (F's catch), or disbelief with no fault named = implicit. | C4 b9, C6 b2, C1 b14 explicit; C8 b121, C9 b33 implicit |
| `ai_missing_retrieval` | Suppressed when the turn has a reasoning or analysis block, **or when the fact is in the user's provided material** (B's catch: the C2 "15%" is in the pasted post). | C3 b7, C8 b18 fire; C2 b1 doesn't |

## C. Open / unresolved

- **C1 b2** "You know what I meant with personal help though, right?" — A: validation_seeking, B: asks_clarification, F: implicit_correction + validation_seeking. Undecided.
- **Unresolved after review** (no agreement reached; each annotator keeps their own label — 100% agreement is not required, and these cells resolve only at gold-set adjudication): C4 b26 `ai_offers_to_elaborate` (B fires, A/F don't) · C8 b64 `performative_hedge` (A/F fire, B doesn't) · C9 b11 `ai_references_prior_turn` (A/B fire, F doesn't) · C9 b38 `intent_missed` (A/B fire, F doesn't). No rubric text rests on these cells.
