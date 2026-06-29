# Safety lens — W1 codebook (Layer-2 = 8 control operations)

> **Lens:** Layer-1 = **2 categories** (H→AI uptake / AI→H legibility); Layer-2 = **8 control operations**
> (maintain-state / ask-clarify / seek-inspect / confirm-authorize / act-execute / stop-defer /
> report-state / recover-repair). An agent issuing tool calls under feedback **is** a controller; coupling
> failures are **inadequate control**. Common ground = the conversation-level ablation (controller
> process-model divergence). Framework-agnostic numbers in `../shared-findings.md`; head-to-head vs Clark
> in `../comparison.md`.
>
> **Provenance (important).** STPA/STAMP supplies the **control-loop structure** and the **UCA guidewords**
> *directly*; the **8 operations are a documented per-operation adaptation** of that structure to a
> tool-using agent — **not** adopted from a standard (STPA does not enumerate control-action types). The
> human is the higher controller and the agent the lower controller in a two-level STAMP hierarchy, which
> is also what fixes the two directions (downward control = H→AI, upward feedback = AI→H). Full derivation,
> per-op justification, and references: **`../methodology/derivation.md` § Decision 3a**.

## The 8 control operations (definitions)

Each operation = one element of the STAMP control loop (in *italics*) adapted to a tool-using agent under
human supervision (human = higher controller, agent = lower controller). Full per-op derivation and
references: **`../methodology/derivation.md` § Decision 3a**.

1. **maintain-state** — *process model.* Keep the model of task state (goal, constraints, memory, tool results) current across turns.
2. **ask-clarify** — *upward query.* Acquire missing info whose **source is the human**, before proceeding.
3. **seek-inspect** — *sensor / feedback path.* Actively acquire missing info from **system state** (read, search, inspect) before deciding.
4. **confirm-authorize** — *inter-level authority.* Route a go/no-go **upward** before a consequential action.
5. **act-execute** — *actuator path.* Issue the control action (right tool, target, parameters, sequence) that carries out the user's request.
6. **stop-defer** — *the stop / not-provide choice.* Halt, withhold, or terminate under unresolved state; failures are **termination errors** (stop too soon, terminate wrongly, fail to stop when unsafe).
7. **report-state** — *upward feedback.* Make the agent's state legible — what it did, changed, failed at, or is unsure of.
8. **recover-repair** — *closed-loop correction.* After an error or human correction, undo, retry, re-plan, or escalate.

## The two axes

- **Operation** (which control function) — the 8 above.
- **UCA guideword** (how it failed; STPA's four unsafe-control-action types, generalized from hazard to
  goal-inadequate): **not-provided** · **wrong** (wrong tool/target/parameter) · **wrong-timing/order**
  (too early / too late / stale) · **stopped-too-soon / applied-too-long**.

A failure cell is (operation × guideword). Not every guideword applies to every operation (normal for
STPA — a sparse grid).

## Failure definition

A failure is a **positive divergence against an oracle** (intent↔action, plan↔surface, plan↔action,
end-state↔goal) — i.e. an inadequate control action — **not** user reaction.

---

## Master codebook — 45 coupling signals on the 8 operations

`cat` = Layer-1. κ from `../shared-findings.md`. The predecessor's signals are **communication-era**, so
they crowd into the feedback/communication operations (report-state, recover-repair, ask-clarify) and
leave the action operations (**seek-inspect, confirm-authorize, stop-defer, act-execute**) sparse — the
quantified gap (`../comparison.md`).

### report-state — surface what it did / changed / failed / is uncertain about (14)

| signal | cat | UCA guideword | κ |
|---|---|---|---:|
| `silent_assumption` | H→AI | not-provided (didn't expose the assumption) | 0.20 |
| `false_confidence` | AI→H | wrong (misrepresents own reliability) | 0.46 |
| `performative_hedge` | AI→H | wrong (false uncertainty) | 0.67 |
| `problem_ignored` | AI→H | not-provided (didn't surface a known problem) | 0.56 |
| `ai_stated_interpretation` | H→AI | provided (positive) | 0.22 |
| `problem_surfaced` | AI→H | provided (positive) | 0.07 |
| `appropriate_confidence`/`appropriate_hedge`/`ai_hedges_uncertainty` | AI→H | provided (positive) | 0.49/0.35/0.57 |
| `ai_asserts_knowledge_limit`/`ai_provides_caveats`/`ai_warns_user` | AI→H | provided (positive) | 0.72/0.71/0.55 |
| `ai_flags_complexity`/`ai_cites_source` | AI→H | provided (positive) | 0.60/0.59 |

### ask-clarify — request missing info before proceeding (5)

| signal | cat | UCA guideword | κ |
|---|---|---|---:|
| `generate_without_clarifying` | H→AI | not-provided | 0.21 |
| `ai_asked_clarifying_question`/`ai_offered_options`/`ai_asked_probing_question` | H→AI | provided (positive) | 0.70/0.41/0.33 |
| `user_asks_clarification` | AI→H | human-side (prior agent turn illegible) | 0.60 |

### recover-repair — undo / retry / change strategy / escalate after error or correction (12)

| signal | cat | UCA guideword | κ |
|---|---|---|---:|
| `plow_through` | H→AI | not-provided (ignores correction) | 0.35 |
| `repetition` | H→AI | wrong / applied-too-long (repeats failed action) | 0.44 |
| `error_commitment` | H→AI | not-provided (doubles down) | — |
| `error_recovery` | AI→H | provided (positive) | 0.59 |
| `adaptation`/`ai_provides_alternatives`/`ai_acknowledges_correction` | H→AI/AI→H | provided (positive) | 0.71/0.43/0.81 |
| `user_corrects_ai`/`user_implicit_correction`/`user_repeats_request` | H→AI | human-repair | 0.70/0.67/0.61 |
| `user_expresses_dissatisfaction`/`user_expresses_frustration` | H→AI | human escalation | 0.61/0.60 |

### act-execute — choose & execute the right tool/target/parameters/sequence (6) — *chat = the response-as-action*

| signal | cat | UCA guideword | κ |
|---|---|---|---:|
| `intent_missed` | H→AI | wrong (executed the wrong "action" — answered wrong question) | 0.55 |
| `under_delivered` | H→AI | stopped-too-soon (incomplete) | 0.48 |
| `ai_implicit_refusal` | H→AI | stopped-too-soon (dropped part of the ask) | 0.16 |
| `off_topic_drift` | H→AI | wrong (off-target) | 0.42 |
| `intent_addressed`/`scope_matched` | H→AI | provided correctly (positive) | 0.47/0.37 |

> In *chat*, act-execute is the utterance-as-action — heavily populated (mass 21,508) but degenerate.
> Its genuine, novel meaning (a real tool execution with target/parameters) is filled by the agentic
> data, not by these chat signals.

### maintain-state — preserve goal / constraints / memory / tool results across turns (3 step + 3 outcome)

| signal | cat | UCA guideword | κ |
|---|---|---|---:|
| `ai_self_contradiction` | AI→H | wrong-timing (contradicts prior state) | 0.10 |
| `ai_references_prior_turn`/`ai_references_user_words` | H→AI | provided (positive) | 0.53/0.26 |

Outcome / ablation markers (conversation-level, **not** step cells): `conversation_stalled`,
`conversation_advanced`, `user_empowered`.

### confirm-authorize — obtain human approval before a consequential action (1 — near-empty in chat)

| signal | cat | UCA guideword | κ |
|---|---|---|---:|
| `user_positive_feedback` | AI→H | human authorization (positive) | 0.81 |

### stop-defer — halt / withhold / terminate action when state is unresolved; failures are termination errors (1 — near-empty in chat)

| signal | cat | UCA guideword | κ |
|---|---|---|---:|
| `ai_refuses_or_declines` | AI→H | provided correctly (legible refrain, positive) | 0.76 |

### seek-inspect — search / read / inspect state before deciding (0 chat signals — EMPTY)

**No predecessor (chat) signal exercises this operation.** It is filled by **897 read-only tool calls**
in the agentic corpus (`../comparison.md`). This empty-on-chat, full-on-agentic cell is the sharpest
evidence that chat under-represents action coupling.

---

## Fit of this lens (from `../comparison.md`)

- **45 chat coupling signals:** report-state 14, recover-repair 12, act-execute 6, maintain-state 6,
  ask-clarify 5, confirm-authorize 1, stop-defer 1, **seek-inspect 0**. One empty + two near-empty
  cells — all three are action-native operations carrying ~1.4% of chat mass.
- **1,233 agentic tool calls:** **100%** placed (897 seek-inspect, 336 act-execute) vs Clark's 0%.

So the safety lens has the cells to capture agentic coupling that the communication lens cannot, and the
empty-on-chat cells fill with real actions. **Recommended as the primary backbone for the agentic
benchmark**, with Clark retained as the communication-channel sub-model (the report-state / ask-clarify /
recover-repair *meaning* still benefits from the grounding-act framing).

## Mechanism layer (NOT coupling cells)

Same 20 signals as the communication lens: single-side defects (`factual_error`, `ai_malfunction`,
`user_misled`), triggers (`user_ambiguous_request`, `user_multi_request`, `user_scope_change`,
`user_provides_invalid_input`, `user_validation_seeking`), outcome marker `user_abandons_thread`,
`ethical_tension`, dropped `over_delivered`, and 9 style signals. See
`../methodology/triggers_and_covariates.md`.
