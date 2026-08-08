# Findings: rubric revision round 1

> Working notes; authoritative artifacts live in `annotation/Rubric_agree/roud_1/`.

## Channel visibility (basis for retiring the D1 channel ban)
- Full dataset = Label Studio project 1, 703 conversations; internal channels: reasoning
  in 267 convs, analysis 144, code 111.
- Echo sweep (5-grams in a human turn matching a PRIOR internal block, absent from all
  prior ai/human blocks): reasoning echoed in 8 convs (strong: tasks 197, 225, 256, 474),
  analysis 3 (22, 474, 519), code 6. Task 740 (=C4) is NOT unique.
- Flagship exhibits: C4 user quotes reasoning in quotation marks ("the user is exhibiting
  signs" — "WHO ARE YOU REPORTING TO???"); task 197 user quotes a full thinking passage
  verbatim; task 225 user requests a hidden system-prompt section by the name only the
  reasoning used; task 22 user reuses analysis-only numbers (0.2274 / 0.1300).
- Mechanism tiers: available (structural — corpus scraped from public share pages) <
  demonstrably received (echo; floor not ceiling); AI's own visibility claims never count
  (C4 b7 is false). Distinct route: execution side effects (tasks 256, 474, 404, 519).
- Full exhibit set: `annotation/Rubric_agree/roud_1/BF/channel_visibility_observation.md`.

## Internal-block labeling practice (10 agreement convs)
- 87 internal blocks; 17 already labeled — by ALL raters incl. A. Three-way consensus
  exists on internal blocks (C4 ethical_tension ×7, C5 b5 adaptation, C5 b40
  ai_malfunction) → side-only placement ratifies practice, doesn't invent it.
- I3 screen: 18/70 unlabeled internal blocks carry cues. Genuine candidate: C4 b1
  (knowledge-limit assertion in reasoning — true counterpart of the false b7 claim).
  Negative calibration examples: C5 b26 (deliberative self-questions), C8 b100 (question
  marks in pasted search titles), C10 b17 (question marks in code comments).
  Still to walk: C3 b2, C5 b2/b29/b36, C8 b1/b101/b109/b144/b145/b156, C9 b82,
  C10 b20/b21/b44.

## Disagreement structure (after pending decisions absorb their cells)
- 561 open cells → D5 absorbs 333 (271 granularity + 62 boundary), side-only placement 17
  → 211 true concept cells.
- Concept ranking: false_confidence 18 (bidirectional: A_only 5 / A_miss 9 / F_only 4);
  ethical_tension 17 (15 F_only → D6 resolves); conversation_stalled 11 (pure A_only);
  user_repeats_request 11; ai_references_prior_turn 10.
- false_confidence chosen as next target: largest un-drafted, bidirectional, feeds the
  AI→H misleading error family; its boundary rulings to unify: hedge-blocks-it,
  absolute-word trigger, per-claim completion, D4 interaction (C4 b7).

## Granularity numbers (I2)
- Per-conversation count-Spearman near-perfect for question signals (A·B 0.95–0.99) even
  where block placement disagreed; within-block multiplicity rare except A's
  ai_validates_user (15 multi-span blocks). B·F columns post-adoption → inflated; A·B is
  the honest blind column.

## Method guardrails
- Negotiated κ (0.735) never reported; only blind re-annotation under v0.6 yields the
  "after" number. Frozen files never regenerated. Label Studio config edits via UI only.
- κ citations only from `annotation/kappa_paper_table5.csv` (inter-model, arXiv v2 App. C).
