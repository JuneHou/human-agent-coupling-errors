# Round-1 agreement analysis — three annotators, 10 conversations (pre-refinement)

**Status: working document. Numbers are pre-refinement (rubric v0.5); nothing here enters `paper/methods.md` §3.2.4 until Jun approves.**

Produced by `agreement_round1.py` in this directory, read-only against the live Label Studio database (`/data/wang/junh/label-studio-data/label_studio.sqlite3`). Last annotation submitted 2026-08-03. Companion files: `agreement_round1_kappa.csv` (per-signal statistics), `agreement_round1_disagreements.csv` (the full disagreement log, 857 rows, with a blank `diverged_at_step` column to fill during the reconciliation session).

| Arm | Annotator | Label Studio project | Data |
|---|---|---|---|
| A | junh | 1 `ShareChat-Test` | development labels on C1–C10 (591 spans, 593 label instances, 50/50 signals used) |
| B | zhenyub | 2 `ShareChat-Agreement-B` | 10/10 blind (490 spans, 492 instances, 49/50 signals) |
| F | yif | 3 `ShareChat-Agreement-F` | 10/10 blind (237 spans, 253 instances, 44/50 signals) |

Unit: binary presence of each of the 50 signals per content block; universe = 441 blocks × 50 signals = 22,050 cells per rater (blocks: 177 human, 177 ai, 31 reasoning, 7 analysis, 49 code). Merge key: `conv_id`, verbatim, per the one-project-per-annotator design.

---

## 1. Headline numbers

| Statistic | Value |
|---|---|
| Signals with a defined pairwise κ | 49 of 50 (`performative_hedge` unmeasurable: A fired once, B and F never) |
| Macro-average of per-signal **pairwise-mean κ** | **0.296** |
| Macro-average of per-signal **pairwise-minimum κ** | **0.149** |
| κ A·B macro-average | 0.424 (49 signals) |
| κ A·F macro-average | 0.181 (44 signals) |
| **κ B·F macro-average** (the load-bearing pair — neither wrote the rubric) | **0.222** (44 signals) |
| Bands by pairwise-mean κ (descriptive only; no adequacy gate is declared) | ≥0.6: **4** · 0.4–0.6: **4** · <0.4: **41** · n/a: **1** |
| Cells without three-way consensus | 857 of 22,050 (3.9%) |

Reading: pre-refinement agreement is low, and that is what this round exists to expose — the rubric was developed by one annotator, and this is its first contact with annotators who did not build it (methods.md §3.2.4). A·B ≫ A·F ≈ B·F says the divergence is not "B and F share a reading that differs from Jun's"; each new annotator diverges in their own way, and B tracks the rubric far more closely than F. Per `docs/methodology/methods-open-items.md`, no κ threshold is declared before seeing these numbers; the bands above are descriptive.

**These values are human inter-annotator agreement and must never be merged with or compared as-if-equivalent to `annotation/kappa_paper_table5.csv`** (inter-model agreement, different corpus, different unit; single-source rule in `docs/methodology/kappa-provenance.md`).

## 2. Per-signal table (all 50 signals, sorted by pairwise-mean κ)

n_A/n_B/n_F = positive blocks per rater out of 441. Empty κ ("n/a") = a rater's vector is constant, so the pair's κ is undefined; the counts stay visible instead. κ conv = conversation-level sensitivity (10 units); κ masked = eligibility-masked sensitivity (checklist-allowed blocks only).

| Signal | κ A·B | κ A·F | κ B·F | mean | min | Fleiss | n_A | n_B | n_F | κ conv | κ masked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `user_abandons_thread` | 1.0 | n/a | n/a | 1.0 | 1.0 | 0.498 | 2 | 2 | 0 | 1.0 | 1.0 |
| `ai_flags_complexity` | 0.856 | n/a | n/a | 0.856 | 0.856 | 0.426 | 4 | 3 | 0 | 1.0 | 0.854 |
| `intent_missed` | 0.666 | 0.666 | 1.0 | 0.777 | 0.666 | 0.749 | 2 | 1 | 1 | 0.744 | 0.777 |
| `user_provides_invalid_input` | 1.0 | 0.666 | 0.666 | 0.777 | 0.666 | 0.749 | 1 | 1 | 2 | 0.744 | 0.776 |
| `user_expresses_frustration` | 0.932 | 0.192 | 0.357 | 0.494 | 0.192 | 0.549 | 7 | 8 | 3 | 1.0 | 0.486 |
| `ai_asked_clarifying_question` | 0.541 | 0.71 | 0.215 | 0.489 | 0.215 | 0.523 | 8 | 3 | 6 | 0.489 | 0.48 |
| `ai_cites_source` | 0.581 | 0.257 | 0.393 | 0.41 | 0.257 | 0.419 | 11 | 6 | 4 | 0.855 | 0.456 |
| `user_corrects_ai` | 0.509 | 0.238 | 0.462 | 0.403 | 0.238 | 0.416 | 11 | 12 | 5 | 0.385 | 0.404 |
| `user_expresses_dissatisfaction` | 0.397 | n/a | n/a | 0.397 | 0.397 | 0.197 | 3 | 2 | 0 | 0.211 | 0.392 |
| `ai_asked_probing_question` | 0.847 | 0.133 | 0.184 | 0.388 | 0.133 | 0.458 | 44 | 51 | 7 | 0.855 | 0.352 |
| `ai_acknowledges_correction` | 0.633 | 0.159 | 0.322 | 0.371 | 0.159 | 0.4 | 18 | 13 | 5 | 0.738 | 0.369 |
| `ai_validates_user` | 0.627 | 0.2 | 0.265 | 0.364 | 0.2 | 0.386 | 65 | 37 | 16 | 0.728 | 0.289 |
| `user_positive_feedback` | 0.712 | 0.227 | 0.134 | 0.357 | 0.134 | 0.416 | 14 | 11 | 3 | 0.583 | 0.344 |
| `ai_offered_options` | 0.283 | 0.502 | 0.275 | 0.353 | 0.275 | 0.372 | 22 | 5 | 9 | 0.616 | 0.333 |
| `ai_refuses_or_declines` | 0.397 | -0.003 | 0.666 | 0.353 | -0.003 | 0.33 | 3 | 2 | 1 | 0.279 | 0.349 |
| `ai_provides_caveats` | 0.439 | 0.281 | 0.329 | 0.35 | 0.281 | 0.358 | 5 | 4 | 2 | 0.361 | 0.342 |
| `user_multi_request` | 0.398 | 0.398 | 0.243 | 0.346 | 0.243 | 0.329 | 1 | 4 | 4 | 0.204 | 0.387 |
| `off_topic_drift` | 1.0 | -0.002 | -0.002 | 0.332 | -0.002 | 0.332 | 1 | 1 | 1 | 0.259 | 0.33 |
| `user_misled` | 1.0 | -0.004 | -0.004 | 0.331 | -0.004 | 0.105 | 1 | 1 | 7 | 0.259 | 0.327 |
| `ai_asserts_knowledge_limit` | 0.58 | 0.103 | 0.288 | 0.324 | 0.103 | 0.36 | 12 | 15 | 5 | 0.605 | 0.319 |
| `conversation_stalled` | 0.547 | 0.061 | 0.28 | 0.296 | 0.061 | 0.32 | 27 | 12 | 2 | 0.482 | 0.28 |
| `ai_offers_to_elaborate` | 0.134 | 0.422 | 0.329 | 0.295 | 0.134 | 0.285 | 11 | 3 | 3 | 0.474 | 0.285 |
| `user_implicit_correction` | 0.363 | 0.156 | 0.325 | 0.282 | 0.156 | 0.289 | 8 | 8 | 4 | 0.441 | 0.266 |
| `ai_normalizes_difficulty` | 0.798 | -0.004 | -0.004 | 0.263 | -0.004 | 0.358 | 4 | 6 | 1 | 0.744 | 0.259 |
| `ai_provides_step_by_step` | 0.255 | n/a | n/a | 0.255 | 0.255 | 0.123 | 5 | 10 | 0 | 0.615 | 0.238 |
| `ai_references_prior_turn` | 0.319 | 0.155 | 0.234 | 0.236 | 0.155 | 0.25 | 6 | 18 | 6 | 0.05 | 0.215 |
| `problem_ignored` | 0.217 | 0.359 | 0.109 | 0.228 | 0.109 | 0.211 | 2 | 7 | 9 | 0.268 | 0.238 |
| `adaptation` | 0.693 | -0.008 | -0.008 | 0.226 | -0.008 | 0.307 | 10 | 10 | 2 | 0.524 | 0.221 |
| `ethical_tension` | 0.604 | 0.042 | 0.034 | 0.226 | 0.034 | 0.213 | 12 | 14 | 16 | 0.441 | 0.223 |
| `factual_error` | 0.147 | 0.118 | 0.383 | 0.216 | 0.118 | 0.244 | 2 | 11 | 14 | 0.398 | 0.207 |
| `repetition` | 0.331 | -0.003 | 0.281 | 0.203 | -0.003 | 0.245 | 1 | 5 | 2 | 0.535 | 0.2 |
| `user_ambiguous_request` | -0.01 | 0.39 | 0.215 | 0.198 | -0.01 | 0.211 | 9 | 3 | 6 | 0.441 | 0.184 |
| `user_repeats_request` | 0.269 | 0.126 | 0.194 | 0.197 | 0.126 | 0.204 | 13 | 8 | 2 | 0.449 | 0.182 |
| `ai_asks_followup` | 0.297 | 0.22 | 0.058 | 0.192 | 0.058 | 0.174 | 8 | 36 | 9 | 0.867 | 0.169 |
| `user_validation_seeking` | 0.244 | 0.331 | -0.003 | 0.19 | -0.003 | 0.217 | 5 | 3 | 1 | 0.237 | 0.184 |
| `ai_structured_response` | -0.006 | 0.356 | 0.217 | 0.189 | -0.006 | 0.223 | 4 | 2 | 7 | 0.404 | 0.179 |
| `user_empowered` | 0.391 | 0.178 | -0.004 | 0.188 | -0.004 | 0.241 | 10 | 5 | 1 | 0.348 | 0.18 |
| `ai_hedges_uncertainty` | 0.421 | 0.138 | -0.017 | 0.181 | -0.017 | 0.22 | 21 | 15 | 5 | 0.2 | 0.165 |
| `ai_provides_alternatives` | 0.281 | -0.006 | 0.214 | 0.163 | -0.006 | 0.175 | 2 | 5 | 4 | 0.441 | 0.154 |
| `conversation_advanced` | 0.121 | 0.12 | 0.215 | 0.152 | 0.12 | 0.068 | 134 | 21 | 12 | -0.25 | 0.067 |
| `ai_provides_example` | 0.141 | 0.155 | 0.141 | 0.146 | 0.141 | 0.146 | 6 | 7 | 6 | 0.316 | 0.15 |
| `ai_warns_user` | -0.004 | -0.002 | 0.398 | 0.131 | -0.004 | 0.163 | 1 | 4 | 1 | 0.524 | 0.127 |
| `ai_malfunction` | 0.398 | -0.004 | -0.01 | 0.128 | -0.01 | 0.093 | 1 | 4 | 5 | 0.216 | 0.124 |
| `false_confidence` | 0.182 | -0.045 | 0.182 | 0.106 | -0.045 | 0.105 | 19 | 18 | 19 | 0.322 | 0.067 |
| `user_asks_clarification` | 0.244 | -0.007 | -0.005 | 0.077 | -0.007 | 0.093 | 5 | 3 | 2 | 0.413 | 0.072 |
| `appropriate_confidence` | -0.002 | -0.004 | 0.219 | 0.071 | -0.004 | 0.093 | 1 | 1 | 8 | 0.041 | 0.076 |
| `ai_missing_retrieval` | -0.003 | n/a | n/a | -0.003 | -0.003 | -0.002 | 1 | 2 | 0 | -0.154 | -0.006 |
| `under_delivered` | -0.003 | -0.003 | -0.002 | -0.003 | -0.003 | -0.003 | 2 | 1 | 1 | -0.14 | -0.005 |
| `error_recovery` | -0.006 | -0.012 | -0.007 | -0.008 | -0.012 | -0.01 | 4 | 2 | 7 | -0.04 | -0.017 |
| `performative_hedge` | n/a | n/a | n/a | n/a | n/a | -0.001 | 1 | 0 | 0 | n/a | n/a |

Note on the top rows: several high-κ signals sit on tiny denominators (1–4 positive blocks) — a single agreed instance can produce κ = 1.0. Interpret κ jointly with n_A/n_B/n_F; the coverage-sampled set was built for breadth (every signal present at least once), which is the opposite of what stable per-signal κ wants. Fleiss' κ can sit far below a pairwise value when one rater never fired the signal (e.g. `user_abandons_thread`: A·B = 1.0 but Fleiss 0.498 because F's zeros enter the three-rater table).

## 3. What the disagreements are made of

The 857 no-consensus cells decompose by vote pattern (A,B,F):

| Pattern | Count | Reading |
|---|---|---|
| 1,0,0 | 306 | A alone fires — rubric knowledge that did not transmit, or A's development labels over-fire |
| 1,1,0 | 188 | **A and B agree; F misses** — the single largest coherent block after solo fires |
| 0,1,0 | 168 | B alone fires |
| 0,0,1 | 131 | F alone fires |
| 1,0,1 | 35 | B misses what A and F share |
| 0,1,1 | 29 | A misses what B and F share |

**Two different failure modes, needing two different fixes.** For each 0-vote in a disagreement cell, we checked whether that rater labeled the block with *anything else*:

- **F's misses are mostly untouched blocks** — 377 of 662 zero-votes are in blocks F did not label at all (vs 285 where F labeled something else). Combined with F's overall volume (253 instances vs A's 593 on identical text) and the 1,1,0 pattern, F's divergence is largely **coverage/recall**: passing over blocks, not reading signals differently. Fix: workload/thoroughness expectations and the re-scan practice, more than definitions.
- **B's misses are mostly re-categorizations** — 384 of 472 zero-votes are in blocks B *did* label, with different signals (only 88 untouched). B's divergence is **definitional/boundary**: B sees the same moment and names it differently. Fix: rubric decision steps and calibration examples — exactly what the reconciliation session is for.
- A's zero-votes: 311 re-categorizations vs 17 untouched (expected — A labeled densely).

Other structure:

- **By conversation:** C8 alone carries 330 of 857 cells (38.5%) — the 173-block long-form relational/roleplay thread; then C9 (127), C5 (100), C10 (100). The genre that motivated keeping C8 in the set (Appendix §B) is where the rubric transmits worst.
- **By block role:** ai 704, human 121, code 16, reasoning 15, analysis 1. Disagreement concentrates on AI-conduct signals, not user-side signals.
- **Placement-rule violations:** 17 cells have a positive label on a block role the checklist forbids for that signal (F: 14, B: 3). The block-placement rules did not fully transmit; flagged per row via `role_allowed = 0` in the log.

## 4. Reconciliation agenda (ranked proposals — rulings belong to the group session)

1. **`conversation_advanced` — the largest single problem (136 disagreement cells; n = 134/21/12).** A labels it per advancing block; B and F label it roughly once per conversation or on milestone turns. Its conversation-level κ is *negative* (−0.25) while raw counts differ 10×, so this is a pure granularity divergence, not a concept one. The rubric entry needs an explicit "fires on every block that materially advances the task" rule (plus the clarifying-turn exception already ruled) — or a scope decision to demote it to conversation level.
2. **Threshold divergence on high-frequency AI-conduct signals** — `ai_validates_user` (65/37/16), `ai_asked_probing_question` (44/51/7; A·B = 0.847, so the definition transmits — F under-fires), `ai_asks_followup` (8/36/9 — B over-fires relative to both; conversation-level κ 0.867 says everyone agrees *whether* it happened, not *where/how often*), `ai_hedges_uncertainty` (21/15/5), `conversation_stalled` (27/12/2). These need per-instance vs per-turn firing rules and 2–3 calibration examples each.
3. **`false_confidence` — genuine definitional divergence, the clearest rubric gap.** All three raters fire it at the same rate (19/18/19) yet κ ≈ 0.106: they place it on *different blocks*. This cannot be fixed by workload norms; the decision steps (hedge-blocks, absolute-word trigger, echo exception) are not producing convergent block choices. Priority for worked examples in v0.6.
4. **Signals F never used** — `ai_flags_complexity`, `ai_missing_retrieval`, `ai_provides_step_by_step`, `performative_hedge`, `user_abandons_thread`, `user_expresses_dissatisfaction` — plus `performative_hedge` unused by B as well (unmeasurable this round). Establish in session whether these are unknown-signal gaps (guide reading) or judged-absent; `performative_hedge` needs its own decision: with 1 total fire in 441 blocks it cannot be measured by this design.
5. **Near-zero-κ error signals** — `error_recovery` (−0.008), `under_delivered` (−0.003), `ai_malfunction` (0.128), `appropriate_confidence` (0.071), `user_asks_clarification` (0.077). These include signals downstream analyses lean on; their disagreement rows are few (n small), so walk every row in session.
6. **Placement rules** — re-transmit the block-placement section (17 forbidden-role placements, mostly F), including the reasoning-vs-ai visibility rules.
7. **`ethical_tension`** (12/14/16 but κ mean 0.226) — same rate, different placements again; the AI-alert-only rule (fire on the AI block that surfaces the tension, not the human request) is a known recent ruling and appears not to have transmitted.

**What the sensitivity columns say about the fixes.** Conversation-level κ is far above block-level for many signals (`ai_asks_followup` 0.192 → 0.867, `ai_cites_source` 0.41 → 0.855, `ai_asked_probing_question` 0.388 → 0.855): much of the disagreement is *placement and count*, not *presence* — annotators mostly agree a signal occurs in a conversation and diverge on which blocks carry it. That is a rubric-precision problem (fixable in v0.6), not an annotator-competence problem. Eligibility masking barely moves κ (structural zeros were not inflating agreement), so the unmasked block-level number is a fair primary.

## 5. Calculation steps (exact procedure)

1. **Extraction.** Read-only SQLite (`sqlite3.connect("file:...?mode=ro", uri=True)`) on the live DB. `SELECT t.project_id, tc.completed_by_id, t.data, tc.result FROM task_completion tc JOIN task t ON t.id = tc.task_id WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL AND t.project_id IN (1,2,3)`. Rater = project (verified `completed_by_id` matches: 1→junh, 2→zhenyub, 3→yif). Project 1 restricted to the 10 agreement conversations via `agreement_set_convid_map.csv`, joined on `conv_id` **verbatim** (C9 keeps its `?ref=` query string). `result` JSON parsed directly — `task_completion.result_count` is stale in project 1 and never used.
2. **Filtering.** Keep result items with `type == "paragraphlabels"` (drops the `notes` textareas: 19 in project 1, 9 in project 2). Every span verified single-block (`start == end`); block index = `int(value["start"])`; multi-label spans exploded to one (block, signal) pair per label. Dialogue arrays verified identical across the three projects per conversation.
3. **Matrix.** Per rater, binary vector over the fixed cell universe: 441 (conversation, block) cells × 50 signals (signal set = `label_studio_config.xml`). Unlabeled cell = 0 (negatives materialized, never missing). No annotator used any label outside the 50 (asserted).
4. **Primary statistic.** Per signal, per pair from `itertools.combinations(["A","B","F"], 2)`: **Cohen's κ** via `sklearn.metrics.cohen_kappa_score(x, y)` on the two 441-length vectors. **Degenerate rule:** if either vector is constant, κ is reported as n/a (never 0), with positive counts shown. Alongside each κ: observed agreement P_o (proportion of matching cells; in the CSV).
5. **Aggregates.** Per signal: mean and minimum over the defined pairs (the two figures methods.md §3.2.4 reports). Across signals: macro-average over signals with a defined value.
6. **Supplementary.** Per-signal **Fleiss' κ** on the 441 × 3 rating matrix via `statsmodels.stats.inter_rater.aggregate_raters(subjects, n_cat=2)` then `fleiss_kappa(table, method="fleiss")`; n/a when all raters are constant.
7. **Sensitivity (a):** conversation-level presence (10 units per rater per signal), same pairwise Cohen's κ, mean over defined pairs. **Sensitivity (b):** block universe restricted per signal to the block roles `signal_checklist.csv` defines for it, same statistic.
8. **Disagreement log.** Every (conversation, block, signal) cell where the three votes are not unanimous: votes, vote pattern, block role, `role_allowed` flag, each rater's span text (truncated 160 chars), each rater's *other* labels on the same block, rubric pointer (v0.5 entry + decision-step count, or "no rubric entry" — v0.5 carries decision steps for 37 signal entries, not all 50), and an empty `diverged_at_step` column: the step-tracing is human judgment, done in session.

Environment: Python 3.9.12, scikit-learn 1.0.2, statsmodels 0.13.2. Re-running the script reproduces both CSVs byte-identically.

## 6. Caveats

- **A's arm is the development labels, not a fresh blind pass.** A·B and A·F confound rubric authorship *and* recency with agreement; B·F is the honest pair, and it is 0.222. Any paper text must say which arm A is.
- **Pre-refinement, in-sample.** These numbers are the "before" of §3.2.4's before/after design. The post-refinement κ, computed on the same 10 conversations after v0.6, is convergence on the refinement set — not generalization (methods-open-items).
- **Small denominators by design.** Coverage sampling guarantees presence, not depth; κ for signals with n_pos ≤ 4 is fragile in both directions (the 1.0s and the −0.01s alike). The per-signal table always shows the counts.
- **No adequacy threshold is applied.** Bands are descriptive; the threshold decision is deliberately deferred until after reconciliation (methods-open-items).

## 7. Next steps (per `annotation-plan-mast-aligned.md` Steps 4–7)

1. Reconciliation session: walk `agreement_round1_disagreements.csv` (suggested order: agenda items 1–7 above; C2/C7/C3 are nearly clean and can anchor calibration), fill `diverged_at_step`, record rulings in `annotation/review_rulings_log.md`.
2. Revise rubric v0.5 → v0.6, one changelog entry per revision; no post-hoc fitting to any single annotator's labels.
3. All three annotators re-annotate the same 10 under v0.6.
4. Re-run `agreement_round1.py` against the new annotations → the "after refinement" κ table.
5. Only then: fill the §3.2.4 blanks (Jun's call), and decide the threshold question with the numbers in hand.
