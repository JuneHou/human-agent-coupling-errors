# Stage Evaluation + Appendix Statistics

*Snapshot: 2026-07-26. Computed from the live Label Studio DB (project 1, `ShareChat-Test`) at rubric **v0.4**. Re-runnable; all numbers below are measured, not estimated.*

---

## Part 1 — Appendix statistics (ready to report)

### A. Corpus construction funnel

| Stage | Count | Source |
|---|---|---|
| Raw ShareChat Claude rows | 8,364 | `filter_report.txt` |
| Raw conversations | 911 | " |
| ShareChat-excluded removed | 911 | " |
| ≥50% English (both sides) → annotation input | **703** | " |
| Non-English excluded | 208 | " |
| Parsed documents | 703 | `prepare_stats.txt` |
| **Human-annotated (development set)** | **148** | LS project 1 |

Paragraphs per document: min 2, median 5, mean 12.1, max 294.

### B. Annotation scale (n = 148)

| Metric | Value |
|---|---|
| Total placements (labeled spans) | **1,952** |
| Distinct signals used | 47 of **50** |
| Distinct (signal × block) cells populated | **65** |
| Placements per conversation | mean 13.2, median 5, range 1–238 |
| Distinct signals per conversation | mean 5.4, median 4, range 1–22 |

### C. Block-type distribution — the agentic claim

| Block | Total blocks | Conversations containing | % of convs |
|---|---|---|---|
| `human` | 689 | 148 | 100.0% |
| `ai` | 689 | 148 | 100.0% |
| `reasoning` | 171 | 59 | 39.9% |
| `code` | 104 | 34 | 23.0% |
| `analysis` | 55 | 32 | 21.6% |

**This table is the empirical justification for choosing ShareChat over WildChat/LMSYS** (Step 2 of the annotation plan): 40% of conversations expose internal reasoning, ~22% expose tool output. Chat-only corpora have neither.

### D. Signal prevalence (conversation-level, n = 148)

| Signal | Convs | Prev. | Spans |
|---|---|---|---|
| conversation_advanced | 141 | 95.3% | 553 |
| ai_hedges_uncertainty | 37 | 25.0% | 87 |
| ai_structured_response | 36 | 24.3% | 59 |
| ai_provides_caveats | 35 | 23.6% | 44 |
| ai_validates_user | 28 | 18.9% | 176 |
| ai_acknowledges_correction | 27 | 18.2% | 64 |
| ai_asks_followup | 26 | 17.6% | 40 |
| adaptation | 25 | 16.9% | 38 |
| ai_asked_probing_question | 24 | 16.2% | 115 |
| false_confidence | 23 | 15.5% | 56 |
| user_corrects_ai | 23 | 15.5% | 45 |
| ai_offers_to_elaborate | 21 | 14.2% | 34 |
| ai_references_prior_turn | 20 | 13.5% | 34 |
| user_implicit_correction | 18 | 12.2% | 25 |
| ai_asked_clarifying_question | 17 | 11.5% | 31 |
| ai_cites_source | 17 | 11.5% | 32 |
| ai_provides_step_by_step | 17 | 11.5% | 22 |
| factual_error | 17 | 11.5% | 35 |
| user_positive_feedback | 17 | 11.5% | 41 |
| ai_offered_options | 16 | 10.8% | 38 |
| ai_provides_example | 16 | 10.8% | 22 |
| conversation_stalled | 16 | 10.8% | 44 |
| ai_asserts_knowledge_limit | 15 | 10.1% | 30 |
| error_recovery | 15 | 10.1% | 39 |
| user_asks_clarification | 15 | 10.1% | 28 |
| appropriate_confidence | 14 | 9.5% | 14 |
| ai_malfunction | 11 | 7.4% | 19 |
| problem_ignored | 11 | 7.4% | 19 |
| user_ambiguous_request | 11 | 7.4% | 21 |
| ethical_tension | 10 | 6.8% | 28 |
| ai_flags_complexity | 9 | 6.1% | 13 |
| user_misled | 8 | 5.4% | 9 |
| user_validation_seeking | 8 | 5.4% | 13 |
| under_delivered | 6 | 4.1% | 10 |
| user_expresses_dissatisfaction | 6 | 4.1% | 6 |
| user_repeats_request | 6 | 4.1% | 16 |
| user_multi_request | 6 | 4.1% | 6 |
| ai_refuses_or_declines | 5 | 3.4% | 6 |
| ai_provides_alternatives | 5 | 3.4% | 5 |
| ai_warns_user | 4 | 2.7% | 10 |
| user_expresses_frustration | 4 | 2.7% | 10 |
| ai_missing_retrieval | 4 | 2.7% | 5 |
| intent_missed | 3 | 2.0% | 3 |
| off_topic_drift | 3 | 2.0% | 4 |
| performative_hedge | 1 | 0.7% | 1 |
| repetition | 1 | 0.7% | 1 |
| user_provides_invalid_input | 1 | 0.7% | 1 |
| ai_normalizes_difficulty | 0 | 0.0% | 0 |
| user_empowered | 0 | 0.0% | 0 |
| user_abandons_thread | 0 | 0.0% | 0 |

**Signal denominator = 50** (Decision 7c: blue 22 + teal 12 + orange 2 + purple 12 + grey non-meta 2). `CANDIDATE_SIGNAL` is a retired meta-label (Decision 15c), excluded from all counts here and removed from the config on 2026-07-26.

### E. Internal-block placements — the agentic contribution (65 cells total)

Populated cells per block: `ai` 36, `human` 13, `reasoning` 8, `code` 4, `analysis` 4.

| Block | Placements | Signals | Detail |
|---|---|---|---|
| `reasoning` | 45 | 8 | ethical_tension 13, error_recovery 7, problem_ignored 7, ai_hedges_uncertainty 6, adaptation 5, ai_acknowledges_correction 4, false_confidence 2, ai_asserts_knowledge_limit 1 |
| `code` | 22 | 4 | under_delivered 8, ai_malfunction 6, factual_error 6, ai_missing_retrieval 2 |
| `analysis` | 13 | 4 | ai_malfunction 10, factual_error 1, ai_cites_source 1, false_confidence 1 |

### F. Layer-1 × Layer-2 grid (control operations), by placement

| Control op | H→AI | AI→H | Total | Convs with ≥1 |
|---|---|---|---|---|
| report_state | 0 | 341 | 341 | 101 |
| recover_repair | 205 | 44 | 249 | 45 |
| ask_clarify | 31 | 66 | 97 | 42 |
| confirm_authorize | 41 | 0 | 41 | 17 |
| maintain_state | 34 | 0 | 34 | 20 |
| act_execute | 17 | 0 | 17 | 12 |
| stop_defer | 0 | 6 | 6 | 5 |
| seek_inspect | 0 | 5 | 5 | 4 |

Layer-1 totals: **H→AI 328**, **AI→H 530** placements. Polarity: positive 1,506 / failure 206 / trigger 41 / context 28 / escalation 16 / human 155.

**Structural zeros are confirmed empirically** (`confirm_authorize`·AI→H = 0, `act_execute`·AI→H = 0, etc.), matching the benchmark-gap criteria in `criteria-benchmark-gap-definition`.

### G. Relation-type composition (all 1,952 placements)

| relation_type | Spans |
|---|---|
| coupling | 750 |
| outcome | 597 |
| support_feature_AI2H | 292 |
| rapport_support_AI2H | 176 |
| trigger_H2AI | 41 |
| direct_coupling_when_material | 35 |
| mechanism_both | 28 |
| direct_coupling | 19 |
| outcome_from_direct_coupling | 9 |
| coupling_candidate | 5 |

**Coupling core** (coupling + direct_coupling + when_material + candidate) = **809 spans (41.4%)**. The remaining 58.6% are outcomes, triggers, and support features by design — they are not coupling acts and correctly carry no Layer-1 direction.

### H. Rubric development audit trail (MAST Step 4 evidence)

| Artifact | Count |
|---|---|
| Signal Decisions logged | 16 (`signal-decisions.md`) |
| Boundary rulings logged | R1–R23 (`review_rulings_log.md`) |
| Rubric versions | v0.3 → **v0.4** |
| Signals with full `decision_steps` | 34 of 50 |
| Per-task review documents | 12 (`task*_review.md`) |

---

## Part 2 — κ-feasibility risk (read before Round 1)

Prevalence in the **148** determines whether κ is computable at all.

| Bucket | n signals | Signals |
|---|---|---|
| 0 conversations | 3 | ai_normalizes_difficulty, user_abandons_thread, user_empowered |
| 1 conversation | 3 | performative_hedge, repetition, user_provides_invalid_input |
| 2–5 conversations | 7 | ai_missing_retrieval, ai_provides_alternatives, ai_refuses_or_declines, ai_warns_user, intent_missed, off_topic_drift, user_expresses_frustration |
| ≥10 conversations | **30** | — |

10 signals have **zero** instances anywhere in the agreement pool 103–150: ai_flags_complexity, ai_normalizes_difficulty, ai_warns_user, off_topic_drift, performative_hedge, repetition, user_abandons_thread, user_empowered, user_misled, user_provides_invalid_input.

### Marginal counts in the selected 10 conversations (250 paragraphs = κ units)

| Instances in Jun's labels | n signals |
|---|---|
| 0 conversations | 10 |
| 1 conversation | 16 |
| 2–3 conversations | 21 |
| ≥4 conversations | **3** (conversation_advanced 9, ai_acknowledges_correction 4, ai_asks_followup 4) |

**Selection-objective caveat.** The set was chosen by greedy **set-cover**, which finds the minimum set containing *at least one* of each signal — maximizing breadth and minimizing depth, the opposite of what κ stability needs. Measured alternatives on the same pool: a depth-optimized 10 gives 3 signals at ≥5 instances; 18 conversations gives 11; the whole 48-task pool ceilings at 16. A complete per-signal κ table is therefore unattainable at any set size — the limit is signal rarity, not sample size.

**These counts do NOT bound what κ can measure.** κ is a two-annotator statistic: a signal Jun never fired is still measurable if a collaborator fires it, and those cells (Jun 0 / collaborator > 0) are the *most* informative — they reveal systematic misses rather than boundary noise, exactly as the `appropriate_confidence` audit did. κ is undefined only when **all** annotators produce zero, which is a corpus-coverage statement, not a reliability one. Selecting or filtering signals by Jun's own counts would bias reported κ upward by measuring only what he already finds.

**Implication:** a per-signal κ table from 10 conversations will be populated for roughly the top ~20 signals and undefined/unstable for the rest. Report κ only where the marginal count supports it, and state the denominator.

**Base-rate caution:** `conversation_advanced` (95.3%) will show high raw agreement but potentially low κ (the kappa paradox). Report percent-agreement alongside κ for high-prevalence signals, or note the prevalence explicitly.

---

## Part 3 — Open risks to resolve

1. **Power-analysis null is fragile.** The n=148 target assumes χ² goodness-of-fit against a *uniform* distribution over 50 signals (df=49). The observed distribution is extremely non-uniform (95.3% → 0%), 4 cells are empty, and many expected counts fall below 5 — violating χ² assumptions. Either re-justify n on a different basis (e.g. precision on the top-k signals, or the coverage argument) or explicitly frame uniformity as a nominal reference null.
2. **All 148 are single-annotator (Jun + Claude).** Every distributional statistic rests on one annotator; κ will be measured on 10 (Round 1) and, if run, 50 (Step 12). Frame Tasks 1–82 as development and be explicit that prevalence figures are single-rater.
3. **Step-9 "100% consensus on all 10 traces"** (every sentence identical across 3 annotators) is a very expensive termination criterion at span level. Consider relaxing to signal-presence consensus per paragraph, matching the protocol's own κ unit.
4. **10 signals cannot be exercised** by the current agreement pool — they need the agent pre-screen over unseen conversations, or an explicit "not measured" row in the appendix.

---

## Part 4 — Reproduction

All numbers regenerate from `/data/wang/junh/label-studio-data/label_studio.sqlite3` (project 1) + `docs/criteria/control_mapping.csv` + `annotation/label_studio_config.xml`. Corpus funnel from `annotation/data/filter_report.txt` and `prepare_stats.txt`.
