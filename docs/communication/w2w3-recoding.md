# Communication lens — W2 / W3 recoding (numbers in `../shared-findings.md`)

The W2 divergence rates and W3 trigger/repair/no-reaction numbers are framework-agnostic — see
`../shared-findings.md`. This file only states **which Layer-2 cell** each signal occupies under the
Clark-act lens.

## W2 — internal-state divergences (ShareChat `thinking`)

| divergence (rate in shared-findings) | Clark cell | Layer-1 |
|---|---|---|
| assumption internal, absent on surface (12%) | **Present** | H→AI |
| internal doubt, surface confidence (2%) | **Present** | AI→H |
| internal plan/conclusion ≠ surfaced/done (18%) | **Maintain** (`reasoning_surface_mismatch`, data-added) | AI→H |
| internal ambiguity, no question asked (0%) | **Clarify** | H→AI |

The two detectable cells (Present/H→AI assumption, Maintain/AI→H mismatch) are exactly the low-κ
coupling cells; `thinking` as a reference rescues them. This is the construct-validity result for the
meaning column.

## W3 — triggers and repair under the acts

- **Triggers** (`user_ambiguous_request`, `user_multi_request`, …) are **mechanism layer**, not acts —
  they raise P(failure) but are not grounding moves. (`../methodology/triggers_and_covariates.md`.)
- **Repair primitives in chat** (67.1% of failures unrepaired) map to the **Repair** act: AI-side
  `error_recovery`/`ai_provides_alternatives`; human-side `user_corrects_ai`/`user_implicit_correction`/
  `user_repeats_request`. The thin chat Repair baseline is what the benchmark's agentic Repair extends.
- **No-reaction limit** (78.9% / 49.5% multi-turn) is a *visibility* fact, independent of Layer-2 — it
  motivates the oracle, not any particular act.

**Takeaway for this lens:** every W2/W3 *communication* signal lands cleanly on an act; nothing about
W2/W3 distinguishes Clark from control, because both are chat-era communication measurements. The
distinction appears only on the action channel (see `w2b-stageA-agentic.md`).
