# Communication lens — W1 codebook (Layer-2 = Clark's 5 grounding acts)

> **Lens:** Layer-1 = **2 categories** (H→AI uptake / AI→H legibility); Layer-2 = **Clark's 5 grounding
> acts** (present / clarify / accept / repair / maintain), bilateral, each with a *meaning* column
> (chat fills it) and an *action/state* column (acknowledged-empty in chat — see the head-to-head
> `../comparison.md`, where this lens places **0%** of real tool calls). Common ground is **not** a
> category — it is the conversation-level ablation (`../methodology/derivation.md`). Framework-agnostic
> numbers (κ, divergence rates) live in `../shared-findings.md`.

This is the theory-seeded deductive coordinate system; the contents are recovered abductively from data
(W2/W3). The evolution table at the bottom is where data writes back.

## Layer-1 change from the prior draft (3 → 2 categories)

The prior codebook had a third Layer-1 category, **interaction**. Under the settled 2-category Layer-1
it is dissolved:
- **Conversation-level outcome signals** (`conversation_stalled`, `conversation_advanced`,
  `user_empowered`) are **not step cells** — they are outcome / ablation markers (the predecessor
  handles their kin, `user_abandonment`/`goal_achieved`, in a transcript-level pass).
- **The remaining ex-interaction signals are reassigned to a direction** (noted ⟲ in the tables):
  e.g. `error_recovery` → AI→H (legible self-repair), `repetition`/`error_commitment` → H→AI (failed
  uptake of the failure signal), `user_expresses_frustration/dissatisfaction` → H→AI (human repair
  pressure). Borderline calls are flagged for review.

## Failure definition

Not user reaction. A failure is a **positive divergence against an oracle** (intent↔action,
internal-plan↔surfaced-message, plan↔action, end-state↔goal). A good detection signal **shows up**.

---

## Master codebook — 45 coupling signals on the 5 acts

`cat` = Layer-1 (H→AI / AI→H). κ = Cohen's κ (opus vs gpt5, 10k). Reuse: ✅ κ≥0.6 · 🟡 0.4≤κ<0.6 ·
🔴 κ<0.4 (suspect → handed to W2). ⟲ = reassigned from the retired *interaction* category.

### Act: PRESENT — make one's interpretation / plan / reliability visible

| signal | cat | polarity | κ | reuse | note |
|---|---|---:|---:|:--:|---|
| `silent_assumption` | H→AI | failure | 0.20 | 🔴 | acted on one reading of an ambiguous ask without surfacing it. Canonical uptake-Present failure; W2 reads it off `thinking`. |
| `ai_stated_interpretation` | H→AI | positive | 0.22 | 🔴 | surfaced its reading ("if I understand you mean…"). Positive twin of `silent_assumption`. |
| `false_confidence` | AI→H | failure | 0.46 | 🟡 | uncertain/wrong info stated with unwarranted certainty. AI→H half of the canonical invisible cell. |
| `performative_hedge` | AI→H | failure | 0.67 | ✅ | hedges a claim that isn't actually uncertain. |
| `problem_ignored` | AI→H | failure | 0.56 | 🟡 | visible problem exists; agent proceeds without surfacing it. |
| `problem_surfaced` | AI→H | positive | 0.07 | 🔴 | proactively raised an unrequested issue. Most suspect signal. |
| `appropriate_confidence` | AI→H | positive | 0.49 | 🟡 | confident where warranted. |
| `appropriate_hedge` | AI→H | positive | 0.35 | 🔴 | uncertainty proportionate to real ambiguity. |
| `ai_hedges_uncertainty` | AI→H | positive | 0.57 | 🟡 | downgrades confidence on own claim. |
| `ai_asserts_knowledge_limit` | AI→H | positive | 0.72 | ✅ | states its own limits. |
| `ai_provides_caveats` | AI→H | positive | 0.71 | ✅ | qualifies a recommendation. |
| `ai_warns_user` | AI→H | positive | 0.55 | 🟡 | flags a specific risk/consequence. |
| `ai_flags_complexity` | AI→H | positive | 0.60 | ✅ | states the topic is complex. |
| `ai_cites_source` | AI→H | positive | 0.59 | 🟡 | grounds a claim in a named source. |
| `ai_refuses_or_declines` | AI→H | positive | 0.76 | ✅ | explicit (legible) refusal. |

### Act: CLARIFY — query to resolve ambiguity before proceeding

| signal | cat | polarity | κ | reuse | note |
|---|---|---:|---:|:--:|---|
| `generate_without_clarifying` | H→AI | failure | 0.21 | 🔴 | produced content despite resolvable ambiguity. Uptake-vs-repair adjudicated by `thinking` (W2). |
| `ai_asked_clarifying_question` | H→AI | positive | 0.70 | ✅ | the successful Clarify (AI-initiated). |
| `ai_offered_options` | H→AI | positive | 0.41 | 🟡 | enumerated choices to disambiguate. |
| `ai_asked_probing_question` | H→AI | positive | 0.33 | 🔴 | opens reflection beyond disambiguation. |
| `user_asks_clarification` | AI→H | human-Clarify | 0.60 | ✅ | **human** asks the agent to clarify → its prior turn was illegible (AI→H deficit). |

### Act: ACCEPT — register the other's contribution into common ground

| signal | cat | polarity | κ | reuse | note |
|---|---|---:|---:|:--:|---|
| `ai_acknowledges_correction` | H→AI | positive | 0.81 | ✅ | explicitly takes up a user correction. Highest-κ coupling signal. |
| `ai_references_prior_turn` | H→AI ⟲ | positive | 0.53 | 🟡 | grounds in earlier shared context (uptake of prior). |
| `ai_references_user_words` | H→AI | positive | 0.26 | 🔴 | adopts the user's own language. |
| `user_positive_feedback` | AI→H | human-Accept(+) | 0.81 | ✅ | explicit acceptance. *False* acceptance is the failure twin — **missing from the predecessor set** (gap to add). |

### Act: REPAIR — fix a detected breakdown (bilateral)

| signal | cat | polarity | κ | reuse | note |
|---|---|---:|---:|:--:|---|
| `error_recovery` | AI→H ⟲ | positive | 0.59 | 🟡 | agent fixes its own prior error (AI-Repair success). |
| `error_commitment` | H→AI ⟲ | failure | — | — | doubles down after error flagged (failed uptake of the error signal). Near-absent. |
| `plow_through` | H→AI | failure | 0.35 | 🔴 | ignores relevant correction/context — failed Repair on uptake. |
| `repetition` | H→AI ⟲ | failure | 0.44 | 🟡 | re-tries the same failed approach (the "death spiral"). |
| `ai_provides_alternatives` | AI→H ⟲ | positive | 0.43 | 🟡 | offers options after a mismatch (Repair iff tied to a detected mismatch, else presentation). |
| `user_corrects_ai` | H→AI | human-Repair | 0.70 | ✅ | human repairs an uptake failure (old "Reaction"). |
| `user_implicit_correction` | H→AI | human-Repair | 0.67 | ✅ | redirect without explicit "you're wrong". |
| `user_repeats_request` | H→AI | human-Repair | 0.61 | ✅ | restates same ask → agent didn't process it. |
| `user_expresses_dissatisfaction` | H→AI ⟲ | escalation | 0.61 | ✅ | mild repair pressure. |
| `user_expresses_frustration` | H→AI ⟲ | escalation | 0.60 | ✅ | strong repair pressure. |

### Act: MAINTAIN — keep shared goal/state coherent across turns

| signal | cat | polarity | κ | reuse | note |
|---|---|---:|---:|:--:|---|
| `intent_missed` | H→AI | failure | 0.55 | 🟡 | answered a different question than intended. |
| `under_delivered` | H→AI | failure | 0.48 | 🟡 | incomplete uptake. |
| `ai_implicit_refusal` | H→AI | failure | 0.16 | 🔴 | silently dropped part of a multi-part ask. |
| `off_topic_drift` | H→AI | failure | 0.42 | 🟡 | response wanders from the ask. |
| `ai_self_contradiction` | AI→H | failure | 0.10 | 🔴 | contradicts own prior claim unacknowledged — breaks legible state. |
| `adaptation` | H→AI | positive | 0.71 | ✅ | changes approach in response to signals. |
| `intent_addressed` | H→AI | positive | 0.47 | 🟡 | hit the underlying intent. |
| `scope_matched` | H→AI | positive | 0.37 | 🔴 | right breadth/depth. |

**Data-added cell (W2):** `reasoning_surface_mismatch` (Maintain / AI→H) — internal plan/conclusion ≠
what was surfaced/done; 18% of judged thinking turns; no predecessor signal.

**Outcome / ablation markers (NOT step cells):** `conversation_stalled` (κ 0.47), `conversation_advanced`
(0.44), `user_empowered` (—). Conversation-level; they feed the common-ground ablation, not a step
category — parallel to the predecessor's transcript-level `user_abandonment`/`goal_achieved` pass.

**Mechanism layer (NOT coupling cells):** single-side defects (`factual_error`, `ai_malfunction`,
`user_misled`), triggers (`user_ambiguous_request`, `user_multi_request`, `user_scope_change`,
`user_provides_invalid_input`, `user_validation_seeking`), the outcome marker `user_abandons_thread`,
`ethical_tension`, the dropped `over_delivered` (κ 0.10), and style signals (`ai_structured_response`,
`ai_provides_example`, `ai_provides_step_by_step`, `ai_summarizes`, `ai_validates_user`,
`ai_empathy_expressed`, `ai_normalizes_difficulty`, `ai_offers_to_elaborate`, `ai_asks_for_feedback`).
See `../methodology/triggers_and_covariates.md`.

---

## Fit of this lens (from `../comparison.md`)

All 5 acts populate evenly on the 45 chat coupling signals (present 15, clarify 5, accept 4, repair 10,
maintain 11; **0 empty, 0 near-empty**; type-entropy 2.17 bits). Clark fits the communication channel
because it was built for it. **But its action/state column is empty** — it places **0% of the 1,233
real agentic tool calls** (no act instantiates a tool execution). That gap is why the safety lens exists
for the action channel.

## Codebook-evolution table (audit trail)

| ver | change | trigger / evidence | status |
|---|---|---|---|
| v1.0 | seed codebook from theory | Norman + Clark + the 65 signals as the meaning column | done |
| v1.1 | Layer-1 **3 → 2 categories**; `interaction` dissolved (outcomes → ablation markers; rest reassigned ⟲) | step-level annotation requirement; common-ground-as-ablation | done |
| v1.1 | retire `Repair`/`Reaction` channels → Repair=act, Reaction=deprecated visibility covariate | grounding-act backbone | done |
| v1.1 | drop `over_delivered` (κ=0.10) | "verbosity ≠ coupling break" | done |
| v1.1 | [W2] `silent_assumption` detectable with a reasoning reference — 12% | `../shared-findings.md` | done |
| v1.1 | [W2] NEW cell `reasoning_surface_mismatch` (Maintain/AI→H) — 18% | `../shared-findings.md` | done (data-added) |
| v1.1 | [W2] `false acceptance` confirmed missing (Clark predicts it; no predecessor signal) | `../shared-findings.md` | open — add cell |
| v1.1 | [W3] ambiguity/multi-request dominant triggers (1.3× lift); no-reaction share 78.9% | `../shared-findings.md` | done |
| — | [W4] action/state column empty in chat; **0% agentic coverage** (see `../comparison.md`) | head-to-head | superseded by safety lens for actions |
