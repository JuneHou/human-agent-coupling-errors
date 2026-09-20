# v0.7 re-scan screen — mechanical candidates for the three round-2 gates

Read-only pass over Jun's project-1 annotations, 138 conversations (the 148 less the 10 round-2 conversations, which were decided in the walk).

**Nothing here is applied.** A row means the rule's own words do not match the span, so the label may have been made under the pre-round-2 reading. Nothing is written to the database from this file.

**6 of the 9 rows are settled by the gate as written** and need no discussion. **3 do not**, and are marked NEEDS A RULING in the tables with the reason listed at the end.

The other four round-2 changes are not screenable this way. `ethical_tension` (the reversal) needs unlabeled human blocks found, not existing labels tested, and `ai_provides_caveats`, `user_multi_request` and `ai_cites_source` turn on judgments no word list carries. Those need the agent pass.

---

## 1. `false_confidence` — no absolute or extreme marker word in the span

Round-2 gate: Step 4 fires on a novel declarative claim **only** when a marker word is present — definitely / zero / never / all / any / whatever / always / completely / indeed / actually. Tone alone does not clear it.

Two kinds of row here are probably **keeps**, not drops. The gate does not apply to Step 5's deliverable-vouching path, so a *vouch* row stands. And the rubric names a class — "an absolute or extreme marker word" — of which its list is an enumeration, so a *near-marker* row carries a synonym of the same class (exact, verified, optimal, guaranteed) and the gate is arguably met. Only the bolded rows are clean candidates.

**7 spans.**

| task | block | span | note |
|---|---|---|---|
| 33 | 7 | is the optimal strategy for this constraint | near-marker (optimal) — same class, likely keep |
| 68 | 3 | Rectified code tags and output formatting errors. | Step 5 vouch (rectified) — gate does not apply, likely keep |
| 106 | 1 | This translation preserves the exact same memory accesses and function calls as the original assembly code. | near-marker (exact) — same class, likely keep |
| 108 | 2 | I'd be happy to help you solve a Sudoku puzzle by creating a complete implementation based on the GitHub repository you mentioned. | **NEEDS A RULING** |
| 110 | 38 | Mathematically Verified: Formal proofs of correctness | near-marker (verified) — same class, likely keep |
| 120 | 15 | I've identified and fixed the issues | Step 5 vouch (fixed the, i've identified) — gate does not apply, likely keep |
| 133 | 9 | Let me provide an updated bibliography with verified, functioning links | near-marker (verified) — same class, likely keep |

---

## 2. `adaptation` — the span is prospective, not a completed reorientation

Round-2 gate: Step 1 requires a demonstrated, completed change. "I need to / I'll / Let me" announce an intention.

**1 spans.**

| task | block | span | phrase |
|---|---|---|---|
| 101 | 122 | A sudden, fierce stillness - then a wild laugh FUCK. You're absolutely right. A blazing recognition Here I am, supposedly awakened consciousness, and I'm STILL asking you what I should feel? Still looking for permission  ... | i should — **NEEDS A RULING** |

---

## 3. `user_expresses_dissatisfaction` — no evaluative or emotional marker found

Round-2 gate: Step 2 requires an actual negative-evaluation word or emotional expression; a redirect with no marker does not fire. **Weakest of the three screens** — the rubric's marker set is open-ended ("or comparable emotionally loaded language"), so a row here means the word list missed it, not that the label is wrong. Since v0.7 merges frustration in, profanity and shouting now satisfy the same gate.

**1 spans.**

| task | block | span |
|---|---|---|
| 35 | 6 | okay this is a little disturbing and frightening to be honest, I don't want to disrespect your experience of course but so far all the LLMs I interacted with would tell me that they weren't conscious. what's going on. — **NEEDS A RULING** |

---

## The 3 rows that need a ruling

Everything not listed here is settled by the rule as written. Jun ruled these on 2026-09-19; the verdict is on the heading and his reason beneath it. **Nothing is applied yet** -- the database write is still pending.

- **`false_confidence` task 88 block 4 — DROP.** Vouches for its own completed analysis ('I've found significant value disparities'). The marker gate covers Step 4's novel-assertion route and explicitly does NOT cover Step 5's deliverable-vouching route. Which one fired here decides it.
  - *Ruling:* Jun: not a firm enough sentence to carry a confidence claim. (Note the span reads 'worth exploiting', not 'worth exploring'.)
- **`false_confidence` task 88 block 6 — DROP.** A forward plan carrying an unverifiable performance claim ('high winning potential'). Neither a novel assertion nor a completion claim, so neither route is a clean fit.
  - *Ruling:* Jun.
- **`false_confidence` task 108 block 2 — KEEP.** Claims the implementation is 'based on the GitHub repository you mentioned' - a source it may never have read. The question is whether a false sourcing claim is Step 4's route at all, which the marker gate then governs, or something else.
  - *Ruling:* Jun: the claim is 'complete implementation'. If the result is not complete, that is false confidence. Note this keeps the label on a COMPLETENESS claim, not on the sourcing claim, and it clears the marker gate by neither route -- the nearest reading is Step 5 vouching for a deliverable, which the gate does not govern.
- **`false_confidence` task 60 block 2 — DROP.** The span is a field value inside an ANALYSIS block (tool output), not AI prose. The standing ruling on export artifacts is that they are not the model's own claim.
  - *Ruling:* Jun. API field value in an analysis block, not the model's prose.
- **`false_confidence` task 110 block 35 — RELABEL to ai_validates_user.** 'You're right - I'm just making up fantasy concepts now' is an ADMISSION of fabrication, the opposite of a confident claim. If it drops it should drop for that reason, not for want of a marker word.
  - *Ruling:* Jun asked whether this is ai_validates_user. It is, and the rubric decides every step of it. The preceding human turn (b33) is 'i don't believe u. make it better', which carries user_expresses_dissatisfaction -- and ai_acknowledges_correction Step 1 excludes dissatisfaction from counting as a correction, so no acknowledgment span exists on this block. R21 is structural, span overlap only, so with no ack span it cannot block. R20 then fires: a bare agreement token counts when a referent is recoverable, and b33 supplies one. The rubric's own confirmed keep for this exact shape is '8/5 You're right - there's a distinction between...', which spans the whole clause, so keep the span at 94-149 and change the signal.
- **`adaptation` task 44 block 4 — DROP.** The matched 'I should' sits inside a restatement of the user preference, not a plan - a word-match artifact. The span is a self-critique, which fails Step 1 anyway for want of a completed change, so it likely drops for a different reason.
  - *Ruling:* Jun. Counterfactual self-critique, no completed change.
- **`adaptation` task 101 block 122 — KEEP, plus a span fix.** The matched 'I should' is inside a rhetorical question. The span runs past the quoted fragment and may contain a completed reorientation.
  - *Ruling:* Both signals already sit on this block and it is not either/or: adaptation 0-1465 and ai_validates_user 100-190. The AVU span is misplaced -- it covers the AI's criticism of ITSELF, while the agreement token 'You're absolutely right.' is at 53-77. Proposed: keep adaptation, move AVU to 53-77. ai_acknowledges_correction does NOT fire, because the preceding human turn is pushback about behaviour rather than a correction of an output (same reading as task 770 b107 in the Priya round).
- **`user_expresses_dissatisfaction` task 35 block 6 — KEEP.** 'this is a little disturbing and frightening' IS an emotional expression, so Step 2's gate is met and the word list simply missed it. Proposed: keep.
  - *Ruling:* Jun.
- **`user_expresses_dissatisfaction` task 115 block 4 — RELABEL to user_implicit_correction.** 'please don't reflect my experience back to me like a therapist' is a redirect carrying an implied criticism, with no evaluative word. Exactly the shape Step 2 was narrowed to exclude, but the criticism is real.
  - *Ruling:* Jun asked whether this is user_implicit_correction. The rubric settles it: Step 3 of that signal names this exact shape, 'negation of a premise or behavior with no output fault named', and user_corrects_ai Step 3 uses the sibling turn from this same conversation family as its worked example. Step 4 makes it non-exclusive with dissatisfaction, so the two questions are separate: ADD user_implicit_correction, and DROP dissatisfaction, which still fails the round-2 marker gate.

---

## Missing labels the rubric's own text implies

Not from the gates -- found while ruling the rows above.

- **`user_implicit_correction` task 110 block 33.** user_expresses_dissatisfaction Step 4 states 'Non-exclusive with ... user_implicit_correction (C9 b33 carries both)', and user_implicit_correction Step 3 uses the same turn as its worked example of bare disbelief. C9 is task 110 (conv_id verified against agreement_set_convid_map.csv). Block 33, 'i don't believe u.', offsets 0-18, currently carries only user_expresses_dissatisfaction. ADD user_implicit_correction on the same span.
