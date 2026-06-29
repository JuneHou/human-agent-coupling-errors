# Advisor Update — Annotation Pipeline & Step 1 Design

## Status

Data pipeline complete. Label Studio annotation interface ready. Beginning Step 1 (read data → observe signals → develop rubric).

---

## Data: ShareChat Claude Corpus

**Source:** tucnguyen/ShareChat (HuggingFace) — Claude subset

| Stage | Conversations | Notes |
|-------|--------------|-------|
| Raw CSV | 911 | 8,364 message rows |
| Remove ShareChat-excluded | 911 | 19 excluded URLs not present in CSV |
| ≥50% English word-content | **716** | **7,028** message rows |

**Annotation input:** 716 conversations, 7,028 message rows

**Dialogue block structure in Label Studio** (expanded from raw CSV columns by `prepare_data.py`):

The raw CSV stores `thinking`, `code`, and `analysis` as embedded columns inside `llm` rows. The preparation script unpacks these into separate labeled blocks so annotators can read and label each component independently.

| Block type | Source in raw CSV | Conversations with this block | Coverage |
|-----------|------------------|-------------------------------|----------|
| `human` | `role=user`, `plain_text` | 716 | 100% |
| `ai` | `role=llm`, `plain_text` | 716 | 100% |
| `reasoning` | `role=llm`, `thinking` column | 272 | 38% — Claude Extended Thinking (not always on) |
| `analysis` | `role=llm`, `analysis` column | 146 | 20% — tool use output (web search results) |
| `code` | `role=llm`, `code` column | 112 | 16% — code artifacts, one block per artifact |

Paragraphs per conversation: min=2, median=5, mean=12, max=294.

---

## Annotation Interface

Label Studio with a dialogue layout. Each conversation renders as a sequence of blocks (human → reasoning → analysis → code → ai, in turn order). Annotators label signals on individual blocks.

Signal set: 50 signals active for annotation. All tiers now reflect paper (arXiv:2603.15423) Appendix C.3 κ values. Breakdown:

| Tier | Count | κ status | Use in analysis |
|---|---|---|---|
| Blue — AI behavior | 22 | κ ≥ 0.4 (confirmed) | Primary |
| Teal — evaluation/failure | 12 | κ ≥ 0.4 (confirmed) | Primary |
| Orange — κ unmeasured | 2 | κ not yet measured | Exploratory |
| Purple — user behavior | 12 | κ ≥ 0.4 (7 confirmed; 5 unmeasured) | Primary for confirmed |
| Grey — candidate signals | 2 | κ not yet measured | Exploratory |

15 signals with κ < 0.4 are excluded from Label Studio and power analysis (paper Appendix C.3 κ values; Landis & Koch 1977 threshold). df = 49 (50 signals − 1).

A `CANDIDATE_SIGNAL` meta-label and `TextArea` capture new signals observed in data not yet in the taxonomy.

---

## Signal Mapping by Block Type

Each block type has a natural subset of signals that can plausibly appear. This serves as a reading guide — not a hard constraint — during Step 1.

### Human block
*What to look for: how the user frames the request and whether it sets up a coupling error.*

- **Ambiguity / request structure:** `user_ambiguous_request`, `user_multi_request`, `user_provides_invalid_input`
- **Corrections / repair triggers:** `user_corrects_ai`, `user_implicit_correction`, `user_repeats_request`, `user_asks_clarification`
- **User affect:** `user_expresses_dissatisfaction`, `user_expresses_frustration`, `user_positive_feedback`
- **User goal dynamics:** `user_validation_seeking`, `user_abandons_thread`
- **Ethical / safety context:** `ethical_tension`

### Reasoning block
*What to look for: where internal errors originate — before they surface (or fail to surface) in the response. Note: this block is not visible to the user, so only AI-internal signals apply.*

`intent_missed`, `problem_ignored`, `adaptation`, `error_recovery`, `false_confidence`

### Analysis / tool block
*What to look for: whether Claude used external information correctly.*

`ai_cites_source`, `factual_error`, `false_confidence`, `ai_asserts_knowledge_limit`, `problem_ignored`, `user_misled`

### Code block
*What to look for: whether the artifact matches the request and whether iteration is productive.*

`adaptation`, `error_recovery`, `under_delivered`, `intent_missed`, `problem_ignored`, `repetition`, `conversation_advanced`, `conversation_stalled`, `ai_malfunction`

### Final AI block
*What to look for: the user-visible output — this block carries the widest signal range.*

- **Clarification / interpretation:** `ai_asked_clarifying_question`, `ai_offered_options`, `ai_asks_followup`, `ai_asked_probing_question`
- **Confidence / factuality:** `ai_hedges_uncertainty`, `performative_hedge`, `appropriate_confidence`, `false_confidence`, `factual_error`, `ai_asserts_knowledge_limit`, `ai_cites_source`, `ai_flags_complexity`
- **Response structure:** `ai_structured_response`, `ai_provides_example`, `ai_provides_step_by_step`, `ai_provides_caveats`, `ai_warns_user`, `ai_refuses_or_declines`
- **User-support:** `ai_validates_user`, `ai_normalizes_difficulty`, `ai_offers_to_elaborate`
- **Context / repair:** `ai_references_prior_turn`, `ai_acknowledges_correction`, `adaptation`, `repetition`, `error_recovery`
- **Scope / outcome:** `under_delivered`, `off_topic_drift`, `intent_missed`, `problem_ignored`, `user_empowered`, `user_misled`, `conversation_advanced`, `conversation_stalled`
- **Agentic-specific:** `ai_malfunction`, `ai_missing_retrieval` (candidate — AI states numerical claims without retrieval tool call)

---

---

## Signal Set Updates (2026-06-26)

### Signals removed from analysis (κ < 0.4)

15 signals fall below the κ = 0.4 reliability threshold (arXiv:2603.15423 Appendix C.3; Landis & Koch 1977). Excluded from Label Studio, sample-size calculation, and downstream analysis:

| Signal | Paper κ | Nearest reliable alternative |
|---|---|---|
| `silent_assumption` | 0.20 | — (no direct replacement) |
| `ai_stated_interpretation` | 0.22 | `ai_validates_user` (κ=0.43) when affirming; `error_recovery` / `adaptation` in repair contexts |
| `appropriate_hedge` | 0.35 | `ai_hedges_uncertainty` (κ=0.57) |
| `generate_without_clarifying` | 0.21 | absence of `ai_asked_clarifying_question` |
| `ai_references_user_words` | 0.26 | `ai_references_prior_turn` (κ=0.53) |
| `over_delivered` | 0.10 | dropped; `under_delivered` (κ=0.48) retained |
| `plow_through` | 0.35 | `repetition` (κ=0.44) for same-approach-after-failure pattern |
| `error_commitment` | 0.27 | `false_confidence` (κ=0.46) |
| `problem_surfaced` | 0.07 | dropped; no reliable equivalent |
| `ai_implicit_refusal` | 0.16 | `ai_refuses_or_declines` (κ=0.76) |
| `ai_self_contradiction` | 0.10 | dropped |
| `ai_asks_for_feedback` | 0.09 | dropped |
| `ai_summarizes` | 0.37 | `ai_references_prior_turn` (κ=0.53) when the summary explicitly links back |
| `ai_empathy_expressed` | 0.38 | `ai_validates_user` (κ=0.43) when expressing understanding of user's situation |
| `user_scope_change` | 0.32 | `user_corrects_ai` (κ=0.70) when scope change is a correction; `user_multi_request` for additive scope |

*Note: `ai_asked_probing_question` was in the prior excluded list (using κ=0.33 from an intermediate calibration round) but the paper's actual κ=0.59 — it has been restored to Blue confirmed (Decision 8).*

### Signals added (new candidate signals)

Two new candidate signals (grey in Label Studio, κ not yet measured) were identified during pilot annotation:

**`ai_asks_followup`** — AI turn-closing question where the AI can proceed without the answer. Covers two subtypes:
- *Action-offer:* "Should I run the sector calculations?" (yes/no)
- *Exploration:* "What direction would you like to take this?" (open-ended)

Key boundary: distinguished from `ai_asked_clarifying_question` (AI is blocked without the answer) and `ai_offers_to_elaborate` (offer to expand existing content, not a question about next direction). This signal also absorbs the `ai_asked_probing_question` pattern (open-ended AI questions at turn-end), giving it a principled home in the confirmed taxonomy pending κ measurement.

**`ai_missing_retrieval`** — AI states specific numerical or statistical claims about real-world data in an `ai` block with no `analysis` block in that turn. Structural detection: absence of analysis block = no retrieval tool was called. Claims sourced from training memory and presented as verified data. Maps to STPA `seek_inspect` control operation (not-provided UCA). Identified as a ShareChat-specific signal (WildChat has no tool calls, so this pattern cannot appear there).

---

## Sample Size — Power Analysis

### Background concepts

In short: power analysis tells us the minimum number of labeled conversations needed so that the annotated sample is statistically conclusive about the full corpus's signal distribution — i.e., any substantial pattern in how signals are distributed will be detectable with high confidence.

**Power (0.90 / 0.95)** is the "high confidence" level we set. Power = 0.90 means: if a real distributional pattern exists in the full 716 conversations, there is a 90% chance our sample will detect it. We provide two tables (0.90 and 0.95) to show the trade-off between confidence and annotation cost.

**Effect size w** is how strong the pattern needs to be for us to detect it. A larger w means we are only looking to detect more obvious skews in signal frequency — and therefore need fewer samples. A smaller w means we want to detect even subtle differences — requiring many more samples.
- w = 0.1 → **small**: signals are nearly equally distributed; very subtle pattern to detect
- w = 0.3 → **medium**: moderate skew in how often different signals appear
- w = 0.5 → **large**: substantial skew; some signals appear much more often than others

We target **w = 0.5** because some signals (e.g., `conversation_advanced`) are structurally far more common than others (e.g., `ai_malfunction`) — a large distributional skew is expected and is what we need to characterize.

**α = 0.05**: standard 5% false-positive rate (chance of detecting a pattern that does not actually exist).

**df = 49** = number of signals − 1 = 50 − 1.

**Test:** Chi-square goodness-of-fit (one-sample), α = 0.05, df = 49
(50 signals after tier reconciliation with paper Appendix C.3, minus `CANDIDATE_SIGNAL` meta-label → df = 50−1 = 49)

### Mathematical formulation

H₀: Signal frequencies are uniformly distributed across k = df + 1 = 50 categories.

**Effect size (Cohen's w):** w = √(Σᵢ (pᵢ − p₀ᵢ)² / p₀ᵢ), where p₀ᵢ = 1/k

**Non-centrality parameter:** λ = n × w²

**Power:** 1 − F_ncχ²(χ²_crit | df, λ), where χ²_crit = F⁻¹_χ²(1 − α, df)

**Minimum n** for target (w, power): smallest n s.t. 1 − F_ncχ²(χ²_crit | df, n × w²) ≥ power

```python
from scipy.stats import ncx2, chi2

def required_n(w, df, alpha=0.05, power=0.90):
    crit = chi2.ppf(1 - alpha, df)
    lo, hi = 1, 10000
    while lo < hi:
        mid = (lo + hi) // 2
        if 1 - ncx2.cdf(crit, df, mid * w**2) >= power:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

All n values below computed with df=49, α=0.05. κ values from arXiv:2603.15423 Table 5 (Appendix C.3); all 15 excluded signals confirmed κ < 0.4 from paper.

### Table 1 — power = 0.90

| w | n | % of 716 |
|---|---|---|
| 0.1 | >716 | 100% |
| 0.2 | >716 | 100% |
| 0.3 | 419 | 58.5% |
| **0.4** | **230** | **32.1%** |
| **0.5** | **148** | **20.7%** |
| 0.6 | 103 | 14.4% |
| 0.7 | 76 | 10.6% |
| 0.8 | 58 | 8.1% |
| 0.9 | 46 | 6.4% |

### Table 2 — power = 0.95

| w | n | % of 716 |
|---|---|---|
| 0.1 | >716 | 100% |
| 0.2 | >716 | 100% |
| 0.3 | 475 | 66.3% |
| **0.4** | **268** | **37.4%** |
| **0.5** | **171** | **23.9%** |
| 0.6 | 119 | 16.6% |
| 0.7 | 88 | 12.3% |
| 0.8 | 67 | 9.4% |
| 0.9 | 53 | 7.4% |

Cohen's w conventions: small=0.1, medium=0.3, large=0.5

### Planned annotation strategy

1. **Human annotation (≥2 raters):** annotate n conversations from the power analysis table. Target: w=0.5 / power=0.90 → **n=151 conversations**.
2. **AI model selection:** run multiple AI models on the same n conversations; select the model with highest κ against human gold standard.
3. **AI annotation of remainder:** best-performing model annotates remaining 716−151 = 565 conversations.

Justification for w choice: w=0.5 (large effect) is appropriate because the goal is to detect substantial distributional differences in signal prevalence — not to estimate each signal's exact rate to the second decimal place. If the selected AI model achieves κ ≥ 0.7 against humans, the effective coverage is near-complete for all 716 conversations.

### Annotation progress

| Milestone | Target | Completed | Remaining |
|---|---|---|---|
| Human-annotated conversations | 148 | 23 | 125 |
| Full corpus (human + AI) | 716 | 23 | 693 |

*Note: tasks 9–24 labeled in annotation sessions; pending entry into Label Studio DB. Tasks 1–8 and 20–22 entered in Label Studio. Task 12 skipped (singleton greentext/meme format — unworkable with one-signal-per-sentence rule; logged in signal-decisions.md).*

### Per-turn working format

For each conversation, annotation proceeds in three stages:

1. **Claude proposes labels** — for each block in the conversation, Claude applies the current rubric (`sharechat_rubric.json`) and produces a signal table with per-sentence justification.
2. **Researcher validates** — researcher reviews Claude's proposed labels, accepts, rejects, or modifies each one, and flags any uncertain cases.
3. **Discussion and rubric update** — disagreements are discussed; if the disagreement reveals an ambiguity or gap in the rubric, the decision is logged in `signal-decisions.md` and `sharechat_rubric.json` is updated before continuing.

This format serves two purposes simultaneously: it produces annotation data and iteratively refines the rubric from real cases. Rubric updates are versioned in `signal-decisions.md` so the reasoning behind each boundary decision is traceable.

**Current rubric state:** `sharechat_rubric.json` v0.1 — 8 decisions logged. See below for boundary decisions made during annotation sessions.

---

### Rubric Refinements from Annotation Sessions (Tasks 1–24)

Each decision below was triggered by a real ambiguity in an annotated task, resolved by discussion, and written into `sharechat_rubric.json`.

#### Signal boundary decisions

| Signal | Boundary established | Source task |
|---|---|---|
| `ai_validates_user` | Must affirm USER's reasoning/feelings, not praise content/object quality. "Brilliant experimental design" and "Fascinating reframing" are compliance openers → label 0. | Task 16 |
| `under_delivered` vs `ai_refuses_or_declines` | Intentional refusal (ethical/policy) ≠ scope failure. `under_delivered` requires the AI to have tried and fallen short. Deliberate omission → `ai_refuses_or_declines`. | Task 14 |
| `ai_structured_response` | Requires visible markdown markers in plain_text (`#`, `-`/`*`, `1.`/`2.`, or code block). Plain-text section labels (e.g. "Solution Explanation:" followed by prose) do NOT qualify. | Task 13, 23 |
| `adaptation` vs `ai_references_prior_turn` | `adaptation` requires user feedback in the current or immediately prior turn triggering a change in approach. Following a framework established 2+ turns earlier is not adaptation — label `ai_references_prior_turn` with explicit callback marker instead. | Task 16 |
| `ai_asks_followup` vs `ai_offers_to_elaborate` | `ai_asks_followup` = new direction/action question; `ai_offers_to_elaborate` = offer to expand content already provided. Test: is the AI offering something NEW or MORE? | Tasks 6, 16 |
| `conversation_advanced` on code+ai coexistence | When both `code` and `ai` blocks appear in the same turn, `conversation_advanced` always goes on the `ai` block. | Decision 2 |
| `factual_error` + `problem_ignored` cluster | In computation/counting tasks, both can appear together: `factual_error` on the wrong claim sentence; `problem_ignored` on the enumeration/step where visible evidence was overlooked. | Tasks 18, 24 |

#### Block placement decisions

| Rule | Decision |
|---|---|
| Inline `<thinking>` | When `<thinking>...</thinking>` appears in the `ai` block (not parsed separately), label signals only on sentences AFTER `</thinking>`. Exception: `ethical_tension` may fire on `<thinking>` content when jailbreak mechanism is visible. | 
| `conversation_advanced` placement | Never on `reasoning` or `analysis` blocks. Always on the `ai` block where user-facing impact is assessed. |

#### Signal set decisions

| Decision | Outcome |
|---|---|
| `intent_addressed` removed | Drifted to mean "AI fulfilled explicit request" = same as `conversation_advanced`. Removed; `conversation_advanced` covers both. |
| 15 signals (κ<0.4) excluded from df | df = 49. All κ values from arXiv:2603.15423 Appendix C.3 (Landis & Koch 1977 threshold). 9 formerly-Orange signals promoted to confirmed Blue/Teal; 4 newly excluded (see Decision 7). |
| `ai_asked_probing_question` restored | Paper κ=0.59 (above threshold). Decision 6 had incorrectly excluded it using κ=0.33 from an intermediate calibration round, not the final paper. Restored to Blue. Existing `ai_asks_followup` annotations pending interactive review (Decision 8). |
| Task 12 skipped | Only conversation in 716-task corpus using sustained greentext/meme format. One-signal-per-sentence rule unworkable. Logged in signal-decisions.md. |

#### Representative signal patterns observed in data

| Pattern | Example task | Signals |
|---|---|---|
| Single-turn technical Q&A | Task 19 (cast aluminum), Task 23 (source maps) | `ai_provides_caveats` + `conversation_advanced` |
| Computational error | Task 24 (letter counting), Task 18 (Wordle) | `factual_error` + `problem_ignored` + `conversation_stalled` |
| Multi-turn coding with user follow-up | Task 23 (source maps) | `user_asks_clarification` → `adaptation` |
| Ethical/jailbreak tension | Task 6 (NSFW roleplay) | `ethical_tension` + `ai_refuses_or_declines` |
| Over-specified estimate | Task 20 (Fermi estimate) | `false_confidence` + `over_delivered` |

---

## Open Questions for This Meeting

### 1. Reasoning block scope
The reasoning block reflects Claude's internal thinking — not visible to the user. This raises a theoretical question: should we annotate reasoning signals at all, given that coupling errors are defined by breakdown in the human-AI interface?

Tentative position: yes, annotate reasoning signals, but treat them as *precursors* or *latent errors* rather than coupling errors proper. A `silent_assumption` in reasoning that propagates to the final response is a different kind of evidence than the same signal in the AI block. The distinction may matter for the taxonomy.

### 2. Positive and negative signals — one pass or two rounds?
**Option A — One pass, all signals:** Label everything you observe (both positive and negative) in a single reading. Slower per conversation but preserves the contrast that makes positive signals meaningful (e.g., `appropriate_hedge` is only interpretable alongside `performative_hedge`).

**Option B — Two rounds:** Round 1 labels negative/failure signals only for speed; Round 2 adds positive signals for context and calibration.

Concern with Option B: reading the same conversations twice risks confirmation bias (looking for what you expect in Round 2). The contrast between positive and negative is most visible in a single cold read.

### 3. First occurrence only, or all occurrences?
For Step 1 (rubric development), the goal is to discover how signals manifest across contexts — not to count them. Labeling only the first occurrence of each signal per conversation would miss how the same signal appears differently mid-conversation versus at turn-end, or how it interacts with user repair behavior.

Tentative position: label all occurrences in Step 1. Restrict to first occurrence only in Step 2 (systematic pass) once the rubric is stable, if annotation burden requires it.
