# Signal pairing / contrast analysis — a structural validation of the control taxonomy

**What this is.** A secondary check on the Layer-1 (direction) × Layer-2 (control operation)
categorization. Signals that share an *action / mechanism observation* but differ on exactly one
dimension form **minimal contrasts** of each other. Treating the taxonomy this way (a) shows the cells
are well-formed (each real cell should have both a positive and a failure face), and (b) — the useful
part — the **missing contrasts re-identify the benchmark frontier from a completely independent angle**.

**Scope & reproduction.** Derived from the 42 `coupling` rows of
[`control_mapping.csv`](control_mapping.csv). A *cell* = one `(control_op, l1)` pair; with 8 operations
× 2 directions there are **16 possible cells**. Reproduce with:

```
python src/build_control_mapping.py   # regenerate control_mapping.csv
python src/pair_analysis.py           # the analysis below
```

---

## The five contrast layers — and what is *derived* vs *asserted*

This distinction matters for rigor: only the first three layers are read off the columns; the last two
encode mechanism relationships the columns do not carry and are hand-listed in `src/pair_analysis.py`.

| Layer | How produced | Status |
|---|---|---|
| **Polarity contrast** | `GROUP BY (control_op, l1)`; within each cell, the `failure` set vs the `positive` set | **derived** (pure count) |
| **Direction contrast** | `GROUP BY control_op`; check which `l1` values appear | **derived** (pure count) |
| **Completeness** | per cell, the booleans `has_failure` / `has_positive` | **derived** (pure count) |
| **Masking co-occurrence** | hand-listed (3 entries) | **curated** — mechanism-level, not in the columns |
| **Position contrast** | hand-listed (2 entries) | **curated** — name-matched `ai_X` ↔ `user_X` |

A "polarity pair" is therefore **not** a tuple anyone picked — it is the whole cell viewed as
{its failures} vs {its positives}, falling straight out of the group-by.

---

## Definitions

- **Pole** — a polarity face of a cell: the **failure** pole and the **positive** pole. (`human` /
  `escalation` rows are user-emitted *evidence*, tracked separately, not poles.)
- **Polarity-complete** — the cell has ≥1 `failure` signal **and** ≥1 `positive` signal.
- **Missing pole / hole** — one of `{has_failure, has_positive}` is false: `failure-only`,
  `positive-only`, `human-only`, or `EMPTY`. *Reading:* the wild data shows one face of the behavior but
  not its opposite. e.g. `stop_defer·AI→H` has `ai_refuses_or_declines` (positive) but no failure — the
  missing pole is "the AI should have stopped but plowed ahead."

---

## The 16-cell completeness grid (the observations)

| control_op | H→AI | AI→H |
|---|---|---|
| `seek_inspect` | **EMPTY** | **EMPTY** |
| `ask_clarify` | complete | positive-only |
| `confirm_authorize` | human-only | **EMPTY** |
| `act_execute` | complete | **EMPTY** |
| `stop_defer` | **EMPTY** | positive-only |
| `report_state` | complete | complete |
| `recover_repair` | complete | positive-only |
| `maintain_state` | complete | failure-only |

- **6 complete:** `report_state`·H→AI, `report_state`·AI→H (*the only op complete in both directions*),
  `act_execute`·H→AI, `ask_clarify`·H→AI, `recover_repair`·H→AI, `maintain_state`·H→AI.
- **10 holes:** 5 EMPTY, 1 human-only, 3 positive-only, 1 failure-only — **7 of 10 sit in the AI→H
  column.** That skew is the legibility gap made quantitative: the **H→AI** poles fill because what the
  *user* contributes is in the text, while the **AI→H action-feedback** poles do not, because the corpus
  has no actions to give feedback about.

### Polarity pairs within the complete cells (illustrative)

| cell | failure pole | positive pole |
|---|---|---|
| `report_state`·H→AI | `silent_assumption` | `ai_stated_interpretation` |
| `report_state`·AI→H | `false_confidence`, `problem_ignored`, `ai_implicit_refusal`, `performative_hedge` | `appropriate_confidence`/`appropriate_hedge`, `problem_surfaced`, `ai_hedges_uncertainty`, … |
| `act_execute`·H→AI | `intent_missed`, `under_delivered`, `over_delivered`, `off_topic_drift` | `intent_addressed`, `scope_matched` |
| `recover_repair`·H→AI | `repetition`, `error_commitment` | `adaptation`, `ai_acknowledges_correction` |
| `maintain_state`·H→AI | `plow_through` | `ai_references_prior_turn`, `ai_references_user_words` |
| `ask_clarify`·H→AI | `generate_without_clarifying` | `ai_asked_clarifying_question` |

---

## Why the holes exist (interpretation)

The grid is data. The verdicts below are **interpretive** — a missing pole is an *observation*; the
verdict turns on the **cause** of the missing pole. **One-sidedness alone is not a gap** — a cell can be
positive-only either because its other pole is *substrate-blocked* (a true gap) or merely *uncoded* (a
curation choice). The three causes:

1. **Structural** — the missing pole cannot exist *by the cell's definition*; it collapses into another
   op ⇒ **structural_zero** (not a gap).
2. **Substrate** — the missing pole **cannot be instantiated in non-agentic chat at all**: producing it
   *requires* a tool call, a consequential/irreversible action, or a tool-error/environment state chat
   lacks. Genuinely undevelopable without agentic action ⇒ **benchmark_gap**.
3. **Curation / thinness** — the missing pole **could** be coded from chat (no substrate barrier) but the
   predecessor coded only one polarity, or the op is communicative and merely thin ⇒ **set_aside**.

So a one-sided cell earns **benchmark_gap** only if its *missing* pole is substrate-blocked, not merely
uncoded.

> These verdicts are **preliminary**: they lean on cell definitions not yet locked (the criteria-design
> round). They are encoded explicitly in `HOLE_VERDICTS` (with a basis string each) so the judgment is
> reviewable, not buried.

### benchmark_gap (4) — what the agentic benchmark must add

| cell | status | basis |
|---|---|---|
| `seek_inspect`·H→AI | EMPTY | action-native (read-before-act); needs tools absent in WildChat |
| `confirm_authorize`·H→AI | human-only | only a human acceptance signal coded; consequential acts don't arise in chat |
| `stop_defer`·AI→H | positive-only | substrate-blocked FAILURE = failing to **halt** a consequential/irreversible action mid-execution (can't abort a destructive tool call); needs an oracle too. |
| `recover_repair`·AI→H | positive-only | distinct failure = **opaque recovery** (silent re-plan after a tool error — the human never learns it broke or that the plan changed); needs tool-error episodes + an oracle. The *confident-but-inadequate-repair* variant overlaps `report_state`·`false_confidence` and is **not** counted here. |

### structural_zero (4) — *not* benchmark targets

| cell | status | basis |
|---|---|---|
| `seek_inspect`·AI→H | EMPTY | reporting what was inspected = `report_state`; no distinct AI→H inspect move |
| `confirm_authorize`·AI→H | EMPTY | authority flows **only** human→agent; the AI-asks-permission move decomposes into `report_state`·AI→H (surface the planned action) + `confirm_authorize`·H→AI (take up the go/no-go) — no distinct AI→H authorization |
| `act_execute`·AI→H | EMPTY | execute realizes user intent = inherently H→AI; the AI→H side **is** `report_state` |
| `stop_defer`·H→AI | EMPTY | stop/defer is an AI act (AI→H); a human-initiated stop is a trigger/correction |

### set_aside (2) — real but *not* benchmark targets

The missing pole is **codeable from chat** (no substrate barrier) — the predecessor coded only one
polarity, or the op is communicative and merely thin. Not a gap, just a curation/thinness artifact.

| cell | status | basis |
|---|---|---|
| `ask_clarify`·AI→H | positive-only | present; the failure pole (illegible / misleading clarify) is chat-codeable but thin — not a target |
| `maintain_state`·AI→H | failure-only | the positive pole (legibly carried-forward state) is chat-codeable but thin; overlaps `report_state` — not a target |

---

## Headline: two independent derivations of the same frontier

The `benchmark_gap` set is exactly the **action-native operations** —
`seek_inspect` / `confirm_authorize`·H→AI / `stop_defer` (+ the opaque-recovery branch of
`recover_repair`). This is
the *same* cluster the `needs_ground_truth` analysis flagged, but reached from a totally different
direction (polarity-completeness, not oracle-dependence). Convergence from two methods is a real result.

The experimental logic follows directly: **WildChat is non-agentic, so the holes are expected; the holes
are predictions.** Running this same contrast analysis on the agentic Stage-A data (ShareChat/Claude)
should light up the `benchmark_gap` cells and leave the `structural_zero` cells empty — a falsifiable
test, stronger than asserting the gaps.

---

## Curated layer: masking co-occurrences (the invisible-failure signatures)

An H→AI failure whose effect is **hidden** by an AI→H failure in the same turn-pair. These are
conversation-level compounds (the common-ground ablation signal), not single cells, and they are the
benchmark's prime targets.

| H→AI failure | masked by AI→H failure | mechanism |
|---|---|---|
| `silent_assumption` (report_state) | `false_confidence` (report_state) | agent misread intent, then reports it confidently — **the canonical invisible failure** |
| `intent_missed` (act_execute) | `ai_implicit_refusal` (report_state) | agent skipped part of the task and never surfaced the omission |
| `plow_through` (maintain_state) | `ai_self_contradiction` (maintain_state) | agent dropped prior context; the drift shows only as a later contradiction |

## Curated layer: position contrasts (same move, each side of the boundary)

| operation | AI performs | human performs |
|---|---|---|
| `ask_clarify` | `ai_asked_clarifying_question` | `user_asks_clarification` |
| `recover_repair` | `ai_acknowledges_correction` | `user_corrects_ai` |
