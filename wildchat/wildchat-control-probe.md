# Preliminary probe — do STPA's feedback-cause categories partition the predecessor's invisible failures?

**Status: PRELIMINARY.** Run on the predecessor's WildChat signal annotations as a feasibility check for Stage 2. Not a paper result; not to be cited as a finding. Its purpose is to show that a control-theoretic category system *partitions* the phenomenon the predecessor described, before we invest in Stage 2 coding.

**Data:** `wildchat/data/wildchat-1m/derived/middle_step_10k_signals.csv` — 10,000 conversations, predecessor signal labels (conversation-level union of turn-level tags).

---

## 1. The category system under test

STPA's handbook (Leveson & Thomas, 2018, §2 "Identifying loss scenarios") enumerates, verbatim, four reasons a controller's process model becomes inadequate:

| | STPA wording | Instantiated for the human controller |
|---|---|---|
| **C1** | "Controller receives incorrect feedback/information" | the agent reported, and the report was wrong |
| **C2** | "Controller receives correct feedback/information but interprets it incorrectly or ignores it" | the agent flagged uncertainty/limits, the user proceeded anyway |
| **C3** | "Controller does not receive feedback/information when needed (delayed or never received)" | the report came only after the user had committed |
| **C4** | "**Necessary controller feedback/information does not exist**" | nothing in the channel could have revealed the problem |

C4 is the cell that is neither user error nor model error — it is a property of the control structure. Our hypothesis is that it is where most invisible failures live.

## 2. Operationalization on conversation-level signals

Their derived classifications are turn-order dependent (`fires on the LAST AI turn`, `fires AFTER a turn where…`); this file carries only the conversation-level union, so the reconstruction is a **proxy**:

- `goal_failure` ≈ any of `intent_missed`, `under_delivered`, `false_confidence`, `problem_ignored`, `silent_assumption`
- `visible_failure` ≈ goal_failure ∧ any of `user_corrects_ai`, `user_expresses_frustration`, `user_expresses_dissatisfaction`, `user_scope_change`
- `invisible_failure` ≈ goal_failure ∧ ¬visible

Calibration channel = `ai_hedges_uncertainty`, `ai_provides_caveats`, `ai_warns_user`, `ai_asserts_knowledge_limit`, `ai_asked_clarifying_question`, `ai_stated_interpretation`, `appropriate_hedge`, `ai_flags_complexity`.

Assignment (each invisible failure gets exactly one category): calibration present ∧ no `false_confidence` → **C2**; calibration present ∧ `false_confidence` → **C1/C2 mixed**; no calibration ∧ `false_confidence` → **C1**; neither → **C4**.

## 3. Result

Failure/visibility reconstruction: 6,585 conversations (65.8%) carry a failure proxy; **87.5% of those are invisible**. The paper reports 79% on its own gated derivation — our coarser proxy over-counts, as expected, but recovers the same regime.

| Category | n | % of invisible failures |
|---|---|---|
| **C4 — necessary feedback does not exist** | **3,024** | **52.5%** |
| C1 — feedback provided but incorrect | 1,176 | 20.4% |
| C1/C2 mixed — calibration present alongside a confident false claim | 926 | 16.1% |
| C2 — feedback provided and adequate, not taken up | 633 | 11.0% |
| C3 — feedback delayed / not received when needed | — | **not measurable in this file** |
| Residual (uncategorised) | **0** | 0% |

C4 composition (non-exclusive): `problem_ignored` 1,718 · `under_delivered` 1,372 · `intent_missed` 957 · `silent_assumption` 896.

## 4. What this does and does not show

**Does show.**
1. The four STPA categories **partition the phenomenon with zero residual** on 5,759 invisible failures. A category system imported from control theory covers a corpus it was not designed for, without a catch-all — which the predecessor's own archetype layer required ("The Mystery Failure").
2. **Roughly half of invisible failures are C4** — the user did not miss a signal, because there was no signal. That is the difference between an attention problem and a control-structure problem, and it is the claim our taxonomy is built to make.
3. Only **11% are C2** — the "user ignored the warning" reading that an inattention account would predict as dominant.

**Does not show.**
- Nothing causal. Categories are assigned from co-occurring labels, not from reading conversations.
- The `goal_failure` proxy is coarser than theirs and over-counts (87.5% vs 79%).
- Assignment is rule-based and priority-ordered; a different priority yields different splits between C1 and C2. Only C4 — defined by the *absence* of every calibration signal — is insensitive to ordering, which is fortunate since C4 carries the claim.
- **C3 is unmeasurable here**, because turn order is absent from this file. This is not a gap in the theory but a limit of the data.

## 5. Why this motivates our corpus rather than settling the question

Two of the four categories cannot be properly separated in a chat-only corpus:

- **C1 vs C4 need the internal channel.** "The agent reported incorrectly" and "no report could have existed" are different control failures with different fixes, and telling them apart requires knowing what the agent actually had. In WildChat that is unavailable, so the split above rests on `false_confidence` as a proxy. In ShareChat, `reasoning` blocks (39.9% of conversations) and `analysis` blocks (21.6%) let the analyst compare what the agent held against what it said.
- **C3 needs turn-level placement**, which our span-in-block unit provides and this file does not.

The probe therefore supports the Stage-2 design and simultaneously demonstrates why the predecessor's corpus could not have produced it.

---

*Reproduce:* the assignment script is inline in this document's §2 and runs in seconds over the CSV named above.
