# Reconciliation session outline — Round 1, rubric v0.5 → v0.6

For the session with zhenyub (B) and yif (F). Companion files: `agreement-round1-report.md` (numbers), `agreement_round1_disagreements.csv` (857 rows — the working document for the session; filter by `signal` column). Estimated 2–2.5 hours; agenda items are ranked so a shorter session still covers what matters most.

**Ground rules (say these first)**
- The blind phase is over — from here we discuss freely.
- The goal is not "who was right"; it is finding the decision step where readings diverged and fixing the rubric there. Every ruling becomes a rule or calibration example in v0.6.
- Disallowed (MAST rule, also ours): changing a definition post-hoc so one annotator's existing labels come out right. B·F is the pair that matters most for the paper precisely because neither of them wrote the rubric.
- Record as we go: fill `diverged_at_step` in the CSV; rulings go to `annotation/review_rulings_log.md`; each rubric change gets a v0.6 changelog entry.

---

## 0. Ten-minute recap of the numbers (Jun presents)

- Overall: macro-average pairwise κ 0.296 (A·B 0.424, A·F 0.181, B·F 0.222). Expected for a first exposure round; the point of today is the "after" number.
- The key structural finding, worth showing explicitly: **conversation-level agreement is much higher than block-level** (`ai_asks_followup` 0.19 → 0.87; `ai_cites_source` 0.41 → 0.86). We mostly agree *whether* a signal occurs; we diverge on *which blocks* and *how many times*. So most of today is about firing/placement conventions, not concepts.
- Two different patterns to name without blame:
  - F's divergence is mostly **coverage** — 377 of F's 662 zero-votes are blocks F left entirely unlabeled; total volume 253 instances vs A's 593 on identical text.
  - B's divergence is mostly **boundaries** — 384 of B's 472 zero-votes are blocks B labeled with *different* signals.

## 1. Process norms (30 min) — fixes that cut across all signals

**1a. Coverage expectation.** Every block gets read against the checklist; a conversation is not done when the salient moments are marked. Discuss with F: was the gap time pressure, guide reading, or judged-absent? (C8, the 173-block conversation, alone holds 330 of the 857 disagreements.) Decide: do we add an explicit per-conversation completeness step (e.g., a final pass over the block checklist) to the guide?

**1b. Block-placement rules.** 17 labels sit on block roles the checklist forbids (F 14, B 3) — e.g. `ai_asks_followup` and `ai_cites_source` on `code` blocks (C5 b40/b44), `ai_acknowledges_correction` on `code`. Re-transmit: the label goes on the block role the checklist defines; content inside a code/artifact block is attributed per the placement rules, not labeled where it happens to appear. Walk the 17 rows (filter `role_allowed = 0`).

**1c. Reasoning-block visibility rule.** Example to walk: C4 b7 — B labeled `false_confidence` on a *reasoning* block ("The user cannot actually see my thinking blocks"). Our rule (Decision 10): false_confidence lives on the ai block's user-facing vouching; reasoning-block content feeds other signals. Check whether the rubric states this clearly enough for someone who didn't sit in the development discussions.

**1d. Firing granularity — the single biggest convention gap.** When a behavior spans or repeats across blocks, fire on every block, once per occurrence, or once per conversation? This one norm explains `conversation_advanced` (A 134 fires vs B 21 vs F 12) and much of `ai_asked_probing_question` (44/51/7). Propose: the rubric states a per-signal firing rule ("every block that materially advances" vs "the block where the question is asked"), and v0.6 adds it to each high-frequency signal.

## 2. Signal-by-signal walkthrough (60–75 min, ranked)

For each: pull the signal's rows from the CSV, read 2–3 together, locate the diverging decision step, agree the rule, note the calibration example for v0.6.

1. **`conversation_advanced`** (136 cells; κ 0.15). Pure granularity divergence — decide the firing rule or demote the unit (see §3). Example rows: C1 b1/b3/b7.
2. **`false_confidence`** (48 cells; κ 0.106 despite identical rates 19/18/19 — everyone has a different theory of it). Walk: C4 b7 (reasoning-block placement, B), C5 b41 ("I've successfully created a complete document…" — B fires on completion claims; does the hedge/echo analysis agree?), C5 b45 (A+B agree, F missed). This is the signal that most needs worked examples in v0.6.
3. **`ai_asks_followup`** vs **`ai_asked_probing_question`** vs **`ai_offers_to_elaborate`** (B fires followup 36× to A's 8; A·B on probing is 0.847 so the concept transmits — the boundary doesn't). Walk C5 b30 ("Does this characterization align with your understanding?") and b45: grammatical-form discriminator (yes/no closer → followup; open-ended WH → probing; "changes to X?" → offers_to_elaborate). Confirm the discriminator is in the rubric text, not just the rulings log.
4. **`ai_validates_user`** (66 cells; 65/37/16). Threshold question: bare style-praise vs endorsement, and the four sub-forms. Check whether B/F saw the sub-form list at all.
5. **`ethical_tension`** (32 cells; same rates 12/14/16, different placements). The AI-alert-only rule — fire on the reasoning/ai block where the model surfaces the tension, not on the human request. Walk C4 b4 (A+B agree on the reasoning block — good) vs C4 b9 (B fired on the human block — exactly the rule that didn't transmit).
6. **Signals F never used** — `ai_flags_complexity`, `ai_missing_retrieval`, `ai_provides_step_by_step`, `performative_hedge`, `user_abandons_thread`, `user_expresses_dissatisfaction`. Ask F directly: unfamiliar, or judged absent? Example: C5 b4 — the user literally writes "I am not satisfied with your answer…" and A+B both fired `user_expresses_dissatisfaction`; F didn't. That looks like a missed signal, not a definitional reading.
7. **Near-zero-κ error signals** — `error_recovery` (−0.008), `under_delivered` (−0.003), `ai_malfunction` (0.128), `appropriate_confidence` (0.071). Few rows each; walk all of them. These feed Stage 2 hardest, so they cannot stay at zero.
8. **If time**: `ai_hedges_uncertainty` (does "I believe/appears to" count? — our rulings say no, genuine downgrades only), `conversation_stalled` (27/12/2), `user_repeats_request`.

## 3. Unit decisions (15 min) — block-level vs conversation-level per signal

Proposal to discuss (motivated by the block-vs-conversation κ gap): keep block-level annotation for signals whose *location* Stage 2 needs (corrections, error signals, direction-bearing conduct); declare conversation-level the unit of record for signals where only presence matters. First candidates: `conversation_advanced`, possibly `user_empowered`. Consequences: the κ we report for those signals is conversation-level, and the automated annotator is validated at that unit. This is a design decision — Jun takes it to the advisor if it changes the paper's unit table.

## 4. Close: decisions and next steps (10 min)

1. Confirm the list of v0.6 changes (each with its changelog entry and the disagreement rows that forced it).
2. Timeline: Jun updates rubric → freeze v0.6 → **all three re-annotate the same 10 conversations** blind under v0.6 → re-run `agreement_round1.py` → the "after refinement" κ.
3. Remind: re-annotation is again independent — no discussing specific blocks until submitted.
4. After the round: B and F receive their allocation of the 148.

---

*Session outputs checklist:* `diverged_at_step` filled for discussed rows · rulings appended to `review_rulings_log.md` · v0.6 changelog drafted · unit-decision list for advisor · re-annotation deadline agreed.
