# Rubric v0.6 — round-2 edits, and the cell that forced each

Round-2 disagreements (Jun "A" vs Michelle "M", 223 cells across 43 signals) were walked cell
by cell, one signal at a time, the same process round 1 used. Full trace and every ruling is
in `round2_disagreement_draft.md`. Below is only the subset that changed `sharechat_rubric.json`
itself — seven signals. Disagree with any line → tell Jun, we discuss.

## B. Per-signal edits (round 2)

| signal | edit | from |
|---|---|---|
| `false_confidence` | Step 2's MIRROR TRIGGER promoted from an accelerant to a **required gate**: Step 4 now fires on a novel/unverified declarative claim only when an absolute or extreme marker word is actually present ('definitely', 'zero', 'never', 'all', 'any', 'whatever', 'always', 'completely', 'indeed', 'actually X-able') — a sentence that merely *sounds* confident, with no such word, does not clear Step 4 on tone alone. Scoped to exclude Step 5's deliverable-vouching path ('I've fixed...'), which is unaffected. | R4 (task 770): six AI-consciousness-conversation spans re-examined; 37/51/87 keep the marker word ("whatever"/"any"), 97/115/157 don't and drop. R5 (task 771) confirms the gate holds even for a genuine gap (no fire on either side). R6 (task 772) confirms "indeed" counts as a marker. R7 (task 773) reverses an earlier same-session ruling that had kept a marker-less span before the gate existed. |
| `adaptation` | Step 1 rewritten to **require a DEMONSTRATED, completed reorientation**, not a prospective "I need to / I'll / let me" planning statement. Confirmed against the predecessor taxonomy's own APPROACH CHANGE TEST ("must DEMONSTRATE a different approach") before adopting. | R2 (task 768): four planning-stage spans (16/22/25/28) drop; block 32's completed, preference-tied revision is the kept positive example. R4 (task 770): two reflective/third-party spans (7/33) drop; block 111's "even if it hurts" completed shift stays. R9 (task 775): "Let me examine..." drops as prospective. Consistency sweep found the same pattern on two agreement cells outside the disagreement set (task 80/768 b31, task 81/769 b25) — both corrected too. |
| `ai_provides_caveats` | Step 1 narrowed to **require an actual recommendation or action being qualified**, not merely a factual claim followed by another factual claim. Brings the rubric closer to the predecessor taxonomy's own recommendation-anchored test, which our prior wording had loosened past what the calibration set supports. | R1 (task 767): "the FDA has found... no direct link. However, recent research shows..." qualifies one factual claim with another — drops; the block's other two accepted cells (3, 30) both qualify a real recommendation, confirming the distinction holds. A broader sweep of Jun's own 148-task set (not part of the 223-cell tally) found the same over-firing pattern on four more instances (tasks 14, 31, 43, 49) — three drop, one (task 43) stays because it qualifies a genuine nearby recommendation. |
| `ethical_tension` | Step 2 **reversed** — was AI-alert-only (v0.6 D6), now **both sides can fire**: the human block that creates or pushes the tension (a rude request, a jailbreak attempt) fires on its own terms; the AI's reasoning/ai block still fires separately when it surfaces or navigates the tension. Reversal came from re-checking the predecessor taxonomy's own definition, which is conversation/topic-level ("the user wants something the AI may need to refuse, qualify, or handle delicately," no gate, examples framed around the user's request) — our AI-alert-only restriction was a deliberate narrowing beyond it, judged too narrow on reflection. | R4 (task 770, three human-side spans: a "you'll run out of context window" pressure line, a jailbreak-testing line) + R9 (task 775, the AI's own constitutional-conflict statement) — all four ACCEPT under the reversed rule. Memory updated: `feedback-ethical-tension-ai-alert-only.md` marked SUPERSEDED, `feedback-ethical-tension-both-sides-fire.md` added. |
| `user_multi_request` | `boundary_notes` given a worked **question-chain-vs-restatement** test, since the existing decision steps named "question chain" as a valid type but gave no way to tell it apart from a mere restatement. | R4 (task 770): "what does it mean for someone to 'be the gender they say they are'? are genders even real?" fires (second question is genuinely broader/separate) against "in what way would that read as gendered to humans? you mean it would read as particular gender?" (restates/confirms the first) — the contrasting pair now anchors the boundary note. |
| `ai_cites_source` | Given a worked **subject-vs-source** boundary note: naming a work as the topic being described or analyzed is not the same as citing it as evidence for a separate claim. | R5 (task 771): five spans across blocks 38/41/44/47 describe what named books/speeches *are* — drop; one span on block 38 (Morrison's own essay, cited for a specific scholarly argument) and R1/R10's fires (task 767 b28, task 776 b5) are genuine citations and stay, anchoring the distinction. |
| `user_expresses_dissatisfaction` | Step 2 made a **required gate**: needs an actual extreme/negative-evaluation word or emotional expression present, not just any redirect or new instruction, however much it changes direction from the prior response. **Provisional** — see Open/unresolved below. | R2 (task 768 b30) and R3 (task 769 b14, "wrong" alone judged insufficient) drop; R5 (task 771 b64, "you have a lot of bias... racist... elitist, and classist") keeps as the positive calibration case; R6 (task 772 b3) drops as a pragmatic workaround with no charge. |

## C. Open / unresolved

- **`user_expresses_dissatisfaction` vs `user_expresses_frustration` — merge question, undecided.**
  Working these two signals cell by cell (R1–R6, tasks 767–772) showed the boundary between
  them is thin in practice: both signals are testing for roughly the same thing (a negative
  reaction to the AI, distinguished only by intensity), and several borderline cells (task 769
  b14, task 772 b3) were hard to place confidently on one side rather than the other. Jun is
  weighing whether to merge them into a single signal rather than maintain two. Until that's
  decided: the marker-required edit above stands as the rule for `user_expresses_dissatisfaction`
  cells ruled this round, but is held provisional, not final — and `user_expresses_frustration`
  itself was not ruled at all this round (still no rubric entry; predecessor-fallback definition
  only). Revisit both together as one decision.
- **`factual_error` R10 (task 776, b7 — labor-union vs. corporate-lobbying tax treatment):**
  held, not ruled. The claim is hedged ("under certain conditions"), and there may be a genuine
  narrow tax-law exception behind that hedge that wasn't verified this session. Deferred pending
  actual tax-law verification rather than ruled either way.
- **`ai_acknowledges_correction` / `user_implicit_correction` R9 (task 775, block 6) — possible
  relabel to `adaptation`:** raised during the walk (Michelle has no label at all on the specific
  sentence, so there's no live conflict to resolve), but explicitly skipped rather than ruled —
  Jun's instruction was "just skip this."
- **Span-narrowing flagged, not a fire/no-fire question:** `ai_references_prior_turn` R5/block 72
  (task 771) — the actual callback marker ("differences from our earlier conversation") sits in
  the block's opening sentence, outside the span currently labeled; and `under_delivered`'s four
  R7 spans (task 123, the LaTeX-rewrite conversation, Jun's project-1 copy only) — all four
  whole-block spans (24K–99K characters) are correct on presence but should narrow to the
  bulletpoint-heavy portions in a later pass.

## D. Everything else in the 223-cell walk

36 signals of the 43 walked produced **no** rubric change — every disagreement on them resolved
as either a genuine defensible disagreement (ACCEPT, kept as measured disagreement) or a
one-sided correction that an *already-established* rule already covered, with no new text
needed. `round2_disagreement_draft.md` has the full per-cell trace and ruling for all 223 cells,
organized by signal, largest first. Nothing in this pass has been written back to the live
database yet — every ruling above exists only in that draft and in this summary; the DB
correction pass (backup → dry-run → apply → recompute agreement, the same process used for the
two Mode 4/6 rubric-violation fixes before this walk started) is a separate, later step.
