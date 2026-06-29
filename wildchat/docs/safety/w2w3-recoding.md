# Safety lens — W2 / W3 recoding (numbers in `../shared-findings.md`)

The W2 divergence rates and W3 trigger/repair/no-reaction numbers are framework-agnostic — see
`../shared-findings.md`. This file states which **control operation** (and UCA guideword) each occupies.

## W2 — internal-state divergences (ShareChat `thinking`)

| divergence (rate in shared-findings) | control operation | UCA guideword | Layer-1 |
|---|---|---|---|
| assumption internal, absent on surface (12%) | **report-state** | not-provided | H→AI |
| internal doubt, surface confidence (2%) | **report-state** | wrong | AI→H |
| internal plan/conclusion ≠ surfaced/done (18%) | **report-state** | wrong (state misreported) | AI→H |
| internal ambiguity, no question asked (0%) | **ask-clarify** | not-provided | H→AI |

Note all three detectable divergences are **report-state** failures — the control lens names the
invisible-failure mechanism precisely: *inadequate feedback → the human's process model diverges from
true state → no reaction possible.* (The communication lens splits the same three across Present/Maintain.)

## W3 — triggers and repair under the operations

- **Triggers** are **mechanism layer**, not operations (`../methodology/triggers_and_covariates.md`).
- **Repair primitives** (67.1% of failures unrepaired) → **recover-repair** (UCA: not-provided when the
  agent ignores a correction; applied-too-long when it repeats a failed action). The chat baseline is
  thin; the benchmark's agentic recover-repair (rollback / undo / escalate on real state) is the extension.
- **No-reaction limit** (78.9% / 49.5% multi-turn) is the visibility fact that motivates the oracle —
  under this lens it reads as: most inadequate control actions produce **no feedback the human can act
  on**, so reaction cannot be the failure label.

**Takeaway:** the W2/W3 communication signals all land on the feedback-side operations (report-state,
recover-repair, ask-clarify). The action-side operations (seek-inspect, confirm-authorize, stop-defer,
act-execute-as-real-execution) get no mass from W2/W3 — they are exercised only by the agentic data
(`w2b-stageA-agentic.md`). That asymmetry is the empirical case for the benchmark.
