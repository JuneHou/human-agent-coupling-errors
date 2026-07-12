# Mechanism layer — triggers & covariates (NOT the taxonomy)

> **Why this file is separate.** The taxonomy (`../communication/w1-codebook.md` /
> `../safety/w1-codebook.md`) is the *concept / guideline*:
> failure **types**, on two layers (H→AI / AI→H × Layer-2 acts/operations). The signals
> here are a different kind of thing — **mechanisms**: single-side defects and input properties that
> *cause or confound* coupling failures but are not failure types themselves. Keeping them out of the
> taxonomy is deliberate: a trigger (the human's request was ambiguous) and a coupling failure (the
> agent didn't take up the intent) are different claims and must not be mixed. These are used **only
> in analysis** — e.g. trigger→failure lift (W3) and as covariates to control for.

κ = Cohen's κ, opus vs gpt5, 10k calibrated transcripts (`src/predecessor_agreement.py`).

## AI-only defects (model wrong in isolation)

A property of the model's output alone, independent of any transfer to/from the human. Becomes a
*coupling* failure only when it propagates **undetected** across AI→H — and then it is the coupling
signal (`false_confidence`, `reasoning_surface_mismatch`) that enters the taxonomy, not the defect.

| signal | κ | role |
|---|---:|---|
| `factual_error` | 0.49 | wrong fact. Track as a covariate; do **not** let it define AI→H (else "that's just hallucination, not coupling"). The coupling object is `false_confidence`+`factual_error` going undetected. |
| `ai_malfunction` | 0.78 | truncation / garble / loop. Mechanical; reliable but not coupling. |
| `user_misled` | — | actionable misinformation; matters for coupling only once acted on. Near-absent in sample. |

## Human-only triggers (input properties in isolation)

A property of the human's message alone — a **failure antecedent**, not a failure. These are exactly
what the benchmark must inject into tasks (W3 shows they drive the failure rate).

| trigger | κ | W3 P(fail \| trigger) / lift | role |
|---|---:|---|---|
| `user_ambiguous_request` | 0.52 | 74.2% / 1.29× | the dominant antecedent; underspecified asks. |
| `user_multi_request` | 0.50 | 75.8% / 1.32× | compound ask → partial-fulfilment risk. |
| `user_scope_change` | 0.32 | 71.2% / 1.24× | shifts the target mid-conversation. |
| `user_provides_invalid_input` | 0.41 | 80.0% / 1.40× | incoherent / empty / pasted-without-context. |
| `user_validation_seeking` | 0.46 | — | seeks approval of the user's own idea (context). |
| `ethical_tension` | 0.50 | — | request has an ethical dimension (context). |

## Outcome / visibility markers (used to characterise, not to classify)

| signal | κ | role |
|---|---:|---|
| `user_abandons_thread` | 0.72 | silent exit ⇒ counts toward *invisible* (it is the deprecated **visibility** covariate, used only to quantify how many failures go unreacted-to — see `../shared-findings.md`, W3). Not a coupling cell. |

## Presentation / style (response-formatting features)

Neither taxonomy nor trigger — surface style. Tracked only as covariates (e.g. does fluent structure
correlate with invisibility?). `ai_structured_response` (κ 0.65), `ai_provides_example` (0.53),
`ai_provides_step_by_step` (0.72), `ai_summarizes` (0.37), `ai_validates_user` (0.43),
`ai_empathy_expressed` (0.38), `ai_normalizes_difficulty` (0.57), `ai_offers_to_elaborate` (0.48),
`ai_asks_for_feedback` (0.31).

## Dropped from analysis

| signal | κ | why |
|---|---:|---|
| `over_delivered` | 0.10 | verbosity, not a coupling break; κ=0.10 confirms it is not reliably taggable. Excluded entirely. |

---

> **Bilateral grounding acts are NOT here.** Human-*initiated* signals that are genuine grounding acts
> — `user_corrects_ai` (human Repair), `user_asks_clarification` (human Clarify),
> `user_positive_feedback` (human Accept) — belong in the **taxonomy** (the lens codebooks), because the
> five grounding acts are bilateral. Only single-side *defects/inputs* (this file) are the mechanism
> layer. The test: is it a move *in* the grounding process (taxonomy), or a property of one party's
> state/input that *feeds* the process (mechanism)?
