# Rubric-revision meeting 1 — agenda (v0.5 → v0.6)

With zhenyub (B) and yif (F). Pre-reads sent before the session: `cluster_pack_meeting1.md` (the working document, structured as the three review parts: Part 1 candidate rubric changes D1–D6 · Part 2 A-only clusters · Part 3 (B+F)-only clusters) and `v06_changelog_draft.md` (full D1–D6 text with the channel-visibility and granularity evidence). Working data: `meeting1_cells.csv`. Estimated 2–2.5 hours; items are ranked so a shorter session still covers what matters most.

**Ground rules (say these first)**
- We react to drafted rules against cells; we do not derive rules from scratch or debate definitions in the abstract.
- No definition changes post-hoc to vindicate anyone's existing labels — including A's. Where the fault is the rubric text (see `ethical_tension`), we say so and record it that way.
- The κ produced by the post-discussion update (B·F 0.735) is negotiated agreement — useful working feedback, never the paper's number. The reportable "after" κ comes from the blind re-annotation under v0.6.
- Record as we go: accept/modify per candidate rule; `diverged_at_step` in the CSV for walked cells; rulings to `annotation/review_rulings_log.md`; one v0.6 changelog entry per change.

---

## 0. Numbers recap (10 min, Jun presents)

- Where we are: blind round 1 macro κ 0.296 (B·F 0.222) → after F's adoption of 304 of B's labels, the remaining 693 no-consensus cells split into **A vs your consensus (475)** and **B≠F residual (218)**.
- Today's three verbal decisions already clear 132 cells (dropping `conversation_advanced`).
- The mechanical triage says most of the rest is convention, not concept: of the 561 still-open cells, placement + boundary + granularity account for 350; only 211 are presence-level disagreements.

## 1. Part 1 — candidate rubric changes D1–D6 (30 min) — `v06_changelog_draft.md`

1. **D1 + D4 together (~10 min) — the channel model.** Present the evidence first (C4 quartet: reasoning b4 → user b6 verbatim quotes → AI's false b7 claim → b8 denial; C10 code-paste echoes): users demonstrably read reasoning and code. Then the proposed addressed-vs-visible model; decide the two open consequences — content-accessibility signals on reasoning, and the checklist rows (`reasoning, false_confidence`; `reasoning, ai_hedges_uncertainty`). Record the two re-adjudications (C4 b7, C4 b8).
2. **D2 drop `conversation_advanced`** — approve incl. bookkeeping (49-signal universe, "dropped: unit mismatch" in the κ tables, Label Studio UI change after freeze).
3. **D3 `user_ambiguous_request` objectified steps** — run 3–4 of its 14 open cells through the proposed steps live (predictions in the pack: C3 b4 "context report" → 1; C9 b27 "make it better" → 0). Approve or amend from what the live run shows.
4. **D5 firing granularity** — the two-part rule (every block where the behavior occurs; within a block **label every occurrence** — advisor decision 2026-08-05: consecutive exhibiting sentences = one span, separated occurrences = separate labels; κ still computed on block presence). Show the I2 numbers: count agreement already near-perfect for the question signals, within-block multiplicity rare outside `ai_validates_user`, so the rule costs little.
5. **D6 `ethical_tension` AI-alert-only rewrite** — rubric-text bug fix; walk the calibration set (C4 b4 positive; C4 b12/b15/b18 negative; task-150 silent compliance never fires). Settles the appendix's largest cluster too.
6. Close Part 1 by restating the already-ruled conventions (placement, act-block, question-signal discriminators) — not discussion items unless someone objects.

## 2. Part 2 — A-only clusters (30–40 min, ranked) — 195 cells

A fires, the B+F consensus does not. Each item = read the exemplars, accept or modify the candidate rule, note the calibration example for v0.6.

1. **`ai_validates_user` (29)** — per-occurrence mid-block endorsements vs comprehension echoes.
2. **`false_confidence` (15)** — factual_error non-exclusivity + per-claim completion fires.
3. **`conversation_stalled` (16)** — goal-distance test incl. false-progress turns.
4. **`ai_offered_options` (12) + `ai_offers_to_elaborate` (8)** — the option-list and elaborate halves of the question-signal discriminator.
5. **`ai_hedges_uncertainty` (11)** — answer-with-downgrade vs cannot-know.
6. **The correction family**: `user_corrects_ai` (5) + `user_implicit_correction` (5) + `ai_acknowledges_correction` (8) — one shared naming test.
7. **Remaining sections**: `user_repeats_request` (9), `ai_cites_source` (6), `user_ambiguous_request` (6 — feeds D3), `user_empowered` (6); then the 59-cell long tail as a batch.

## 3. Part 3 — (B+F)-only clusters (30–40 min, ranked) — 166 cells

The consensus fires, A does not — the mirror question, plus the D4 flips.

1. **`ai_asks_followup` (21) + `ai_asked_probing_question` (9)** — the remaining halves of the question-signal discriminator (yes/no comprehension closers fire followup; needs-it test beats WH-form).
2. **`false_confidence` (13)** — incl. C4 b7 under D4, and the roleplay-frame boundary (C8 b70).
3. **`factual_error` (9)** — cheap-check expectation; C4 b8 re-adjudicated under D4.
4. **`ai_references_prior_turn` (13)** — explicit backward-pointer test (genuine definitional cluster; count agreement is low here, unlike the granularity cases).
5. **`ai_asserts_knowledge_limit` (6)** — cannot-know fires, cannot-do does not.
6. **Remaining sections**: `ai_provides_step_by_step` (7), `ai_provides_example` (6), `ai_hedges_uncertainty` (5), `user_implicit_correction` (5), `ethical_tension` (5 — pointer to D6); then the 67-cell long tail as a batch.

## 4. Appendix disposition (10 min) — the 200 B≠F residual cells

One question per cluster first: **discussed and disputed, or never reviewed?** Disputed → the rule decided today covers it; never reviewed → B does a normal pass before re-annotation. (Largest: `ethical_tension` 16 — resolved by D6; `false_confidence` 16; `ai_asks_followup` 15 — resolved by item 3.1.)

## 5. Close (10 min)

1. Confirm the v0.6 change list — every accepted rule gets its changelog entry + calibration example, tied to the cells that forced it.
2. Timeline: Jun applies v0.6 → freeze → **all three re-annotate the same 10 conversations blind under v0.6** → re-run `agreement_round1.py` → the reportable "after" κ.
3. Re-annotation is independent: no discussing specific blocks until submitted — the update-from-each-other step we did this round is exactly what the blind pass must not repeat.
4. After the round: B and F receive their allocation of the 148.

---

*Session outputs checklist:* accept/modify verdict per candidate rule · `diverged_at_step` filled for walked cells · rulings appended to `review_rulings_log.md` · v0.6 changelog confirmed (incl. D1–D6) · appendix per-cluster disposition · re-annotation deadline agreed.
