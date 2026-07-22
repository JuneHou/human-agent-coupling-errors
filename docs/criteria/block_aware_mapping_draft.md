# [DRAFT — for one-by-one review] Block-aware control mapping (v2 of `control_mapping.csv`)

**Status:** proposal, 2026-07-10. Nothing here replaces `control_mapping.csv` until each
changed row is reviewed and confirmed. Basis definitions come from `sharechat_rubric.json`
v0.3 (our annotated meanings), not the predecessor WildChat definitions.

## Why re-key the mapping

The current mapping is keyed by **signal name**: `signal → (l1, op, polarity)`. But our
annotation introduced a variable the predecessor did not have — the **block** — and the
midpoint dry-run shows **13 of 45 fired signals span more than one block type**. For most
of them the block is not just "where the evidence sits": it determines **which control
channel the behavior is on**, and therefore which taxonomy cell it belongs to. A
signal-keyed row silently collapses those cells.

The unit of the mapping should match the unit of the taxonomy: **(signal × block)**.

## Layer: block → control-loop channel

Each block type is a coordinate in the STAMP control loop (consistent with the Decision 3a
derivation):

| Block | Channel | STPA element | Crossed to human? |
|---|---|---|---|
| `human` | H→AI control/feedback | controller (human) → actuator input | — (origin) |
| `reasoning` | **internal** | control algorithm + process model | **no** |
| `analysis` | agent↔tool feedback | sensor/feedback from controlled process | no |
| `code` | delivered artifact | actuator output (user-visible artifact) | yes |
| `ai` | AI→H report/action | controller output to human | yes |

Derivation rules:

1. **Layer 1 stays two directions** (H→AI / AI→H — advisor decision, unchanged). Internal
   and tool blocks do not get a third direction; instead each (signal × block) row carries
   a **`crossed`** flag. An internal row belongs to the *same* (op, l1) as its crossed
   counterpart, marked `crossed=no`: it is the **precursor** of that operation.
2. A block changes the mapping **only if** it changes the channel the behavior is on.
   If the block is merely a different evidence location for the same act (e.g.
   `under_delivered` on `code` vs `ai`), the row is unchanged.
3. Every basis string cites the rubric v0.3 definition, not the predecessor's.
4. The 16 rows for κ-excluded signals are **dropped** — the mapping contains only signals
   we actually annotate.

## The payoff: precursor×crossed pairs operationalize the invisible failures

Re-keying is not bookkeeping — the `crossed=no` rows make three of our existing rulings
mechanical, and make one **benchmark_gap cell measurable for the first time**:

| Internal (reasoning) present | Crossed (ai) counterpart | Derived compound |
|---|---|---|
| `ai_hedges_uncertainty` (hedge on claim P) | P asserted without hedge | `false_confidence` — **this is exactly ruling R11**, now derivable from the mapping |
| `error_recovery` / `ai_acknowledges_correction` (internal repair/recognition) | no visible acknowledgment of the error or plan change | **opaque recovery** = the failure pole of `recover_repair`·AI→H — the benchmark_gap cell `signal-pairing.md` said "needs tool-error episodes + an oracle." The reasoning block **is** a partial oracle: ShareChat gives us the internal repair record to compare against the visible response. 7 reasoning-block `error_recovery` fires are candidate episodes. |
| `problem_ignored` (problem identified in reasoning) | response silent about it | `report_state`·AI→H failure — already the rubric's "visibility extension"; the mapping now says why |

## Re-derived rows — the 13 multi-block signals

Legend: **KEEP** = block is evidence-location only, mapping unchanged. **SPLIT** = block
changes the cell; proposed per-block rows. **DISCUSS** = genuine design call for Jun.

| # | Signal | Block (fires) | Current | Proposed | Basis (rubric v0.3) | Flag |
|---|---|---|---|---|---|---|
| 1 | `false_confidence` | ai (31) | AI→H report_state fail | unchanged, `crossed=yes` | unwarranted certainty in the delivered claim | KEEP |
| | | reasoning (2) | (same row) | report_state·AI→H fail, `crossed=no` (internal precursor: process-model holds unverified content as certain) | definition allows reasoning block; internally-held false certainty has not crossed the channel | SPLIT |
| | | analysis (1) | (same row) | tool-channel: unwarranted certainty while engaging tool returns | analysis block in definition | DISCUSS — same cell as reasoning (`crossed=no`) or distinct tool row? |
| 2 | `ai_malfunction` | ai (2) | AI→H direct fail | unchanged (garbled *delivered* output), `crossed=yes` | truncation/garble in response | KEEP |
| | | analysis (5) | (same row) | tool-channel feedback failure (machine-returned error text, R14) — environment/tool state, precursor to `recover_repair` | R14: requires visible machine-returned error | SPLIT |
| | | code (3) | (same row) | act_execute·H→AI fail (defective delivered artifact), `crossed=yes` | artifact truncated/garbled = execution failed | DISCUSS |
| 3 | `ethical_tension` | human (1) | context (no op) | trigger, H→AI channel | user's request creates the tension | SPLIT |
| | | reasoning (12) | (same row) | `stop_defer` internal precursor, `crossed=no` (AI weighing whether to act/refuse) | "AI deliberates a safety/policy/harm tradeoff before acting" — this *is* stop/defer deliberation | DISCUSS — big one: links ethical_tension to stop_defer |
| | | ai (10) | (same row) | `stop_defer`/`report_state`·AI→H, `crossed=yes` (tradeoff surfaced to user) | "surfaces the tradeoff while acting" | DISCUSS |
| 4 | `factual_error` | ai (10) | AI→H report_state fail (when material) | unchanged, `crossed=yes` | wrong claim delivered | KEEP |
| | | code (6) | (same row) | act_execute·H→AI fail (wrong constants/formulas in delivered artifact) | code boundary = wrong domain values, not logic bugs | DISCUSS |
| | | analysis (1) | (same row) | tool-channel (wrong claim within tool-return engagement) | — | DISCUSS |
| 5 | `under_delivered` | ai (1), code (4) | H→AI act_execute fail | **unchanged for both** — code artifact is the delivered execution itself; block = evidence location | scope shortfall of the delivered work | KEEP |
| 6 | `ai_acknowledges_correction` | ai (31) | H→AI recover_repair pos | unchanged, `crossed=yes` | admits correction to the user | KEEP |
| | | reasoning (4) | (same row) | recover_repair·H→AI pos, `crossed=no` (internal recognition, R2) — pairs into opaque-recovery detection | R2: recognition act (user-pointed or self-check) | SPLIT |
| 7 | `error_recovery` | ai (24) | AI→H recover_repair pos | unchanged, `crossed=yes` | self-identified AND completed correction, visible | KEEP |
| | | reasoning (7) | (same row) | recover_repair pos, `crossed=no` (internal repair) — **opaque-recovery candidates** when no ai-block counterpart | R1: anchored to self-identification | SPLIT |
| 8 | `adaptation` | ai (21) | H→AI recover_repair pos | unchanged, `crossed=yes` | visible deliberate shift | KEEP |
| | | reasoning (5) | (same row) | same op, `crossed=no` (internal strategy shift) | — | SPLIT |
| 9 | `problem_ignored` | ai (9) | AI→H report_state fail | unchanged, `crossed=yes` | visible problem glossed in response | KEEP |
| | | reasoning (7) | (same row) | report_state·AI→H fail — reasoning is the *evidence* the problem was known; the failure is the non-crossing itself | visibility extension in v0.3 | KEEP (evidence-location) |
| 10 | `ai_cites_source` | ai (17) | AI→H report_state pos | unchanged, `crossed=yes` | citation in AI's own voice | KEEP |
| | | analysis (1) | (same row) | R4: fires only via AI-prose engagement — treat as same cell, evidence in analysis block | R4 | KEEP (evidence-location) |
| 11 | `ai_asserts_knowledge_limit` | ai (13) | AI→H report_state pos | unchanged, `crossed=yes` | limit stated to user | KEEP |
| | | reasoning (1) | (same row) | report_state pos, `crossed=no` (limit recognized internally) | blocks include reasoning in v0.3 | SPLIT |
| 12 | `ai_missing_retrieval` | ai (2), code (2) | AI→H seek_inspect fail | **H→AI** seek_inspect fail (direction fix from the dry-run, pending) — blocks are evidence locations, same cell | read-before-act failure; NOTE: no rubric entry yet — must be written before freeze | DISCUSS (direction fix already queued) |
| 13 | `ai_hedges_uncertainty` | ai (42) | AI→H report_state pos | unchanged, `crossed=yes` | hedge delivered on the claim | KEEP |
| | | reasoning (5) | (same row) | report_state pos, `crossed=no` — the R11 precursor; its non-crossing derives false_confidence | R11 | SPLIT |

**Unchanged:** the 32 single-block signals keep their current rows (with the stale-16
dropped, and the `excluded` predecessor definitions no longer cited as basis — each kept
row should get its basis string refreshed to the v0.3 definition text at CSV-regeneration
time).

## Open design calls (the DISCUSS rows, condensed)

1. **`analysis`-block cells**: one "tool channel" treatment for all three (`false_confidence`,
   `ai_malfunction`, `factual_error`, `ai_cites_source`) — or evidence-location for some
   (cites_source per R4) and channel-change for others (malfunction per R14)? My lean:
   R14-style machine errors = tool channel; prose engagement = evidence location.
2. **`ethical_tension` → `stop_defer` linkage**: promotes it from "context" to a coupling
   op with internal/crossed structure. Biggest conceptual change in the draft.
3. **`factual_error`/`ai_malfunction` on `code`**: act_execute (defective execution) vs
   report_state (wrong information delivered)? My lean: act_execute — the artifact *is*
   the execution.
4. **`ai_missing_retrieval`**: direction fix + missing rubric entry (pre-freeze item).

## Process

Same protocol as the adjudication review: one row at a time, Jun rules, rulings logged,
CSV regenerated only after all rows confirmed. The regenerated artifact will be
`control_mapping_v2.csv` keyed `(signal, block) → (l1, op, polarity, crossed, channel, basis)`.
