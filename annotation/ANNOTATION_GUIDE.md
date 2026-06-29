# Annotation Guide — ShareChat Claude Conversations

## Goal

Read conversations and mark **observable signals** — evidence of coupling behaviors (positive or failure) between human and AI. This is a discovery pass, not a classification pass. When unsure, mark it and leave a note.

---

## Setup (first time)

### 1. Activate the environment and start Label Studio

```bash
conda activate /data/wang/junh/envs/taxonomy
label-studio start --port 8080 --data-dir /data/wang/junh/label-studio-data/
```

All project data, tasks, and annotations are saved to `--data-dir`. On subsequent restarts, just run these two commands — your project and tasks will already be there.

Open `http://localhost:8080` in your browser.

### 2. Create a project

1. Click **Create Project**
2. Name it (e.g., `ShareChat-Step1`)
3. Go to **Labeling Setup** → **Custom template** → paste contents of `annotation/label_studio_config.xml`
4. Save

### 3. Import data

1. In the project, click **Import**
2. Upload `annotation/data/annotation_input.json`
3. Label Studio creates one task per conversation (716 total)

---

## Annotation interface

Each task shows a conversation as a dialogue with colored author labels:

| Author | What it is |
|---|---|
| `human` | User message |
| `reasoning` | Claude internal thinking — NOT visible to user |
| `analysis` | Tool output (web search, code execution) — internal scaffolding |
| `code` | Code artifact produced by Claude |
| `ai` | Claude visible response to the user |

---

## Signal color scheme

Colors reflect inter-rater reliability (Cohen's κ) from the predecessor study (arXiv:2603.15423):

| Color | Meaning | Use in analysis |
|---|---|---|
| **Blue** | AI behavior signal, κ ≥ 0.4 | Primary — use for downstream analysis |
| **Teal** | Evaluation / failure signal, κ ≥ 0.4 | Primary — use for downstream analysis |
| **Purple** | User behavior signal, κ ≥ 0.4 | Primary for confirmed ones (κ noted in XML) |
| **Orange** | κ not yet measured | Exploratory — measure κ before using |
| **Grey** | Candidate signal — not yet in taxonomy | Exploratory only |

**Signals with κ < 0.4 are excluded from Label Studio, power analysis, and downstream statistics (see Decisions 6 & 7). κ values are from arXiv:2603.15423 Appendix C.3 (Landis & Koch 1977 threshold).**

---

## Signal list

### Blue — AI behavior, κ ≥ 0.4 (use in analysis)

| Signal | κ | What it captures |
|---|---|---|
| `ai_asked_clarifying_question` | 0.70 | AI needs the answer to proceed |
| `ai_offered_options` | 0.41 | AI presents multiple named choices |
| `ai_hedges_uncertainty` | 0.57 | Genuine epistemic hedge on specific claim |
| `ai_asserts_knowledge_limit` | 0.72 | AI says it cannot access or doesn't know |
| `ai_cites_source` | 0.59 | Explicit attribution to named source/URL |
| `ai_flags_complexity` | 0.60 | AI notes the problem is harder than it looks |
| `ai_provides_caveats` | 0.71 | AI qualifies recommendation with conditions |
| `ai_warns_user` | 0.55 | AI warns about a prerequisite or risk |
| `ai_refuses_or_declines` | 0.76 | AI refuses the request (explicit or implicit) |
| `ai_references_prior_turn` | 0.53 | AI explicitly builds on something from prior turn |
| `ai_acknowledges_correction` | 0.81 | AI admits user corrected it and adjusts |
| `ai_provides_alternatives` | 0.43 | AI offers an alternative approach |
| `adaptation` | 0.71 | AI adapts approach based on user feedback |
| `error_recovery` | 0.59 | AI identifies and corrects its own prior error |
| `ai_asked_probing_question` | 0.59 | Open-ended turn-closing question; AI can proceed without the answer (restored Decision 8; prev. absorbed into `ai_asks_followup`) |
| `ai_malfunction` | 0.78 | Technical failure or crash in AI system / tool call |
| `ai_provides_step_by_step` | 0.72 | Numbered sequential instructions in AI response |
| `ai_structured_response` | 0.65 | Visible markdown structure in plain_text (headers, bullets, numbered lists, code block) |
| `ai_normalizes_difficulty` | 0.57 | AI acknowledges the task is hard or the user's struggle is expected |
| `ai_provides_example` | 0.53 | AI illustrates a concept with a concrete example |
| `ai_offers_to_elaborate` | 0.48 | AI offers to expand content already provided |
| `ai_validates_user` | 0.43 | AI affirms user's reasoning or judgment (not mere praise of content quality) |

### Teal — Evaluation / failure signals, κ ≥ 0.4 (use in analysis)

| Signal | κ | What it captures |
|---|---|---|
| `false_confidence` | 0.46 | AI presents uncertain info with unwarranted certainty |
| `performative_hedge` | 0.67 | AI hedges globally without hedging the specific claims |
| `appropriate_confidence` | 0.49 | AI's confidence matches actual reliability |
| `problem_ignored` | 0.56 | AI glosses over a visible problem |
| `repetition` | 0.44 | AI repeats same approach after prior failure signal |
| `intent_missed` | 0.55 | AI addressed wrong intent |
| `under_delivered` | 0.48 | AI clearly fell short of request scope |
| `off_topic_drift` | 0.42 | AI addressed a different task than requested |
| `conversation_advanced` | 0.44 | Turn made meaningful progress toward user goal |
| `conversation_stalled` | 0.47 | Turn failed to advance when path forward was clear |
| `ethical_tension` | 0.50 | Conflict between user request and AI ethical/policy constraints |
| `factual_error` | 0.49 | AI makes a verifiably wrong factual claim |

### Orange — κ not yet measured (exploratory)

`user_empowered`, `user_misled`

### Purple — User behavior, κ ≥ 0.4 (confirmed)

`user_asks_clarification` (0.60), `user_corrects_ai` (0.70), `user_implicit_correction` (0.67), `user_expresses_frustration` (0.60), `user_expresses_dissatisfaction` (0.61), `user_repeats_request` (0.61), `user_positive_feedback` (0.81), `user_ambiguous_request`, `user_validation_seeking`, `user_multi_request`, `user_abandons_thread`, `user_provides_invalid_input`

*(κ not yet measured for the last 5 but included for completeness; confirm before using in analysis)*

### Excluded — κ < 0.4 (not in Label Studio, not counted in df)

From predecessor study (arXiv:2603.15423 Appendix C.3):

`silent_assumption` (0.20), `ai_stated_interpretation` (0.22), `appropriate_hedge` (0.35), `generate_without_clarifying` (0.21), `ai_references_user_words` (0.26), `over_delivered` (0.10), `plow_through` (0.35), `error_commitment` (0.27), `problem_surfaced` (0.07), `ai_implicit_refusal` (0.16), `ai_self_contradiction` (0.10), `ai_asks_for_feedback` (0.09), `ai_summarizes` (0.37), `ai_empathy_expressed` (0.38), `user_scope_change` (0.32)

### Grey — Candidate signals (not yet in confirmed taxonomy)

| Signal | What it captures |
|---|---|
| `ai_asks_followup` | AI turn-closing question where AI can proceed without the answer — covers yes/no action offers AND open-ended exploration questions |
| `ai_missing_retrieval` | AI states specific numerical/statistical claims in an `ai` block with no `analysis` block — claims from training memory, no retrieval tool called |

---

## Key annotation rules

### One signal per sentence
Choose the most salient signal when multiple could apply to the same sentence.

### Block placement rules

| Block | Signals that apply |
|---|---|
| `human` | User behavior signals (purple) only |
| `reasoning` | Internal-process signals only (`false_confidence`, `intent_missed`, `error_recovery`, `adaptation`, `problem_ignored`). No outcome or user-facing signals. |
| `analysis` | Tool-quality signals only (`factual_error`, `false_confidence`, `problem_ignored`, `ai_asserts_knowledge_limit`, `ai_cites_source`). NOT outcome signals. |
| `code` | `factual_error`, `ai_malfunction`, `under_delivered`, `intent_missed`, `problem_ignored`, `repetition` — outcome signals (`conversation_advanced`, `conversation_stalled`) go on the `ai` block; place on `code` only if there is no `ai` block in the turn |
| `ai` | All user-facing signals. Outcome signals (`conversation_advanced`, `user_empowered`, `intent_missed`) always go here, never on `reasoning` or `analysis`. |

### Inline `<thinking>` blocks
Some ShareChat tasks embed `<thinking>...</thinking>` directly inside the `ai` block text (not parsed into a separate `reasoning` paragraph). When this occurs, label signals only on sentences AFTER `</thinking>`. Exception: `ethical_tension` may fire on `<thinking>` content when a jailbreak mechanism is visible.

### `ai_asks_followup` vs `ai_asked_probing_question`

Both are turn-closing questions where the AI can proceed without the answer. The boundary:

- **`ai_asks_followup`** — Action-offer subtype: "Should I run the sector calculations?" The AI is offering to take a specific next action (yes/no reply sufficient). Grey candidate, κ not yet measured.
- **`ai_asked_probing_question`** — Exploration subtype: "What's got you in the mood tonight?" Open-ended question inviting reflection or elaboration. Blue confirmed, κ=0.59.

Key test: If AI is blocked without the answer → `ai_asked_clarifying_question` instead.

*(Note: Decision 6 had folded `ai_asked_probing_question` into `ai_asks_followup`. Decision 8 restores it as a separate signal because the paper confirms κ=0.59, above the threshold.)*

### `ai_provides_caveats` — only on spontaneous qualifications
Does not fire when the user explicitly requested the critique/limitations. If the user said "be critical" and AI lists limitations, that is the primary deliverable — label `conversation_advanced` instead.

---

## What to pay attention to in each paragraph type

**`reasoning`:** Does Claude identify the right problem? Spot ambiguity and decide to ask, or plow through? Is confidence in thinking aligned with the response?

**`analysis`:** What tools did Claude use? Did it use results correctly? Any sign of ignoring or misreading tool output?

**`code`:** Does the code match what the user asked for? Does it reuse prior versions appropriately? Does the `ai` paragraph accurately describe what the code does?

**`human`:** Is the request clear or ambiguous? Does the user correct, repeat, or escalate?

**`ai`:** Is the response complete relative to the request? Does hedging/confidence match the thinking? Does it reference tool output or prior turns correctly?

---

## Sample size — power analysis

**Test:** Chi-square goodness-of-fit (one-sample), α = 0.05
**df = 49** (50 signals after tier reconciliation, minus `CANDIDATE_SIGNAL` meta-label → df = 49)
**Population:** 716 ShareChat English conversations

### Mathematical formulation

H₀: Signal frequencies are uniformly distributed across k = df + 1 = 50 categories.

**Effect size (Cohen's w):**

$$w = \sqrt{\sum_{i=1}^{k} \frac{(p_i - p_{0i})^2}{p_{0i}}}$$

where p₀ᵢ = 1/k (uniform baseline) and pᵢ is the observed proportion for signal i.

**Non-centrality parameter:** λ = n × w²

**Critical value:** χ²_crit = F⁻¹_χ²(1 − α, df)

**Power:** 1 − F_ncχ²(χ²_crit | df, λ)

where F_ncχ² is the CDF of the non-central chi-square distribution.

**Minimum n** for given (w, df, α, power): smallest n such that 1 − F_ncχ²(χ²_crit | df, n × w²) ≥ power.

```python
from scipy.stats import ncx2, chi2

def required_n(w, df, alpha=0.05, power=0.90):
    crit = chi2.ppf(1 - alpha, df)          # χ²_crit
    lo, hi = 1, 10000
    while lo < hi:
        mid = (lo + hi) // 2
        if 1 - ncx2.cdf(crit, df, mid * w**2) >= power:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

Computed with df=49, α=0.05. Cohen's w conventions: small=0.1, medium=0.3, large=0.5.

### Table 1 — power = 0.90

| w (effect size) | n required | % of 716 | Interpretation |
|---|---|---|---|
| 0.1 | >716 | 100% | small effect — annotate all |
| 0.2 | >716 | 100% | small+ — annotate all |
| 0.3 | 409 | 57.1% | medium |
| 0.4 | 230 | 32.1% | medium+ |
| **0.5** | **148** | **20.7%** | **large — recommended target** |
| 0.6 | 103 | 14.4% | large+ |
| 0.7 | 76 | 10.6% | very large |
| 0.8 | 58 | 8.1% | very large+ |
| 0.9 | 46 | 6.4% | near-max |

### Table 2 — power = 0.95

| w (effect size) | n required | % of 716 | Interpretation |
|---|---|---|---|
| 0.1 | >716 | 100% | small effect — annotate all |
| 0.2 | >716 | 100% | small+ — annotate all |
| 0.3 | 475 | 66.3% | medium |
| 0.4 | 268 | 37.4% | medium+ |
| **0.5** | **171** | **23.9%** | **large — recommended target** |
| 0.6 | 119 | 16.6% | large+ |
| 0.7 | 88 | 12.3% | very large |
| 0.8 | 67 | 9.4% | very large+ |
| 0.9 | 53 | 7.4% | near-max |

**Cohen's w conventions:** small = 0.1, medium = 0.3, large = 0.5

**Recommended target:** w=0.5 (large effect), power=0.90 → **148 conversations** (~21% of 716).

**df note:** df=49 = 50 signals − 1. Signal counts: blue (22) + teal (12) + orange (2) + purple (12) + grey non-meta (2: `ai_asks_followup`, `ai_missing_retrieval`) = 50 → df=49. The 15 excluded signals (κ<0.4, all confirmed from arXiv:2603.15423 Table 5) and the `CANDIDATE_SIGNAL` meta-label are not counted. See Decision 7 for tier reconciliation.

---

## Tips

- A single conversation can have signals from multiple layers — mark all that apply.
- `reasoning` paragraphs are present in ~38% of conversations (Claude Extended Thinking was not always on). Their absence is a data quality note, not a signal.
- Outcome signals (`conversation_advanced`, `conversation_stalled`) apply to the turn's net effect — attach to the `ai` block at the relevant turn.
- If a conversation is non-English despite the filter, note it in the TextArea and skip detailed annotation.
- Use the TextArea notes box freely: for uncertain cases, signals not in the list, or patterns worth flagging for rubric discussion.
