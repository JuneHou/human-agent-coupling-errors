# κ Provenance — the single authoritative source

*Established 2026-07-26. Supersedes every other κ value in this repository.*

## The authoritative source

**arXiv:2603.15423v2**, "Invisible failures in human-AI interactions" (Potts & Sudhof), **Appendix C — "Detailed annotation agreement reports"**, **Table 5 — "Signal annotation agreement reports"**.

- **Table 5a** = AI signals (50 rows + Macro/Micro) · **Table 5b** = user signals (13 rows + Macro/Micro). **63 signals total.**
- Transcribed verbatim to **`annotation/kappa_paper_table5.csv`** (columns: `signal, kappa, agreement, table, source`).

### Two things to know about these values

1. **They are in v2, not v1.** v1 (16 Mar 2026) has *no* agreement appendix at all — its Appendix C is "Complete domain distribution" and it contains only Table 1. The agreement appendix was added in **v2 (12 May 2026)**. Citations must specify **v2**.
2. **They are model-vs-model agreement, not human IAA.** Paper §3.2: *"The annotators are Opus 4.6 and GPT-5.4. Micro-κ gives the global Cohen κ across all categories, Macro-κ is the mean of all the category-level κ values."* The paper must describe them as **inter-model** agreement — calling them inter-annotator agreement would misstate the source. Reported aggregates: Table 5a Macro-κ 0.47 / Micro-κ 0.65; Table 5b Macro-κ 0.58 / Micro-κ 0.59.

## Validation of our signal set against Table 5 (50 active signals)

| Check | Result |
|---|---|
| Active signals with paper κ **< 0.4** | **0 violations** ✓ |
| Config κ comments vs paper values | **all match exactly** ✓ |
| Signals κ < 0.4 correctly excluded | 16 ✓ |
| Active signals with **no** paper κ | 4 — see below |
| Table-5 signals κ ≥ 0.4 **not** in our set | 1 — `intent_addressed` (0.47) |

**The 4 active signals absent from Table 5** are correctly flagged as unmeasured in our config:
`user_empowered`, `user_misled` (Orange = "κ not yet measured") · `ai_missing_retrieval`, `ai_asks_followup` (Grey candidates).

**`intent_addressed` (κ = 0.47)** clears the threshold but was dropped by **Decision 1** for a conceptual reason (merged into `conversation_advanced`), not for reliability. That remains valid — but the drop must be justified on conceptual grounds in the paper, never as a κ exclusion.

## Other κ lineages in this repository — do NOT cite

### 1. `r3_kappa` (bigspin tagging code)
`/data/wang/junh/githubs/bigspin-invisible-failure-archetypes/taxonomy-tagging-code/taxonomy.json` records `r3_kappa` for **16 of its 65 signals** — every one flagged `"tier": 2, "tier_note": "Not yet reliable for downstream analysis. Included for calibration improvement."` All 16 values are < 0.4.

This is an **earlier, internal calibration measurement from tagging-code development**, not the published value, and it is recorded there *only* to document why a signal was benched. It is **not** a competing estimate of the Table 5 κ. **Never cite an `r3_kappa` value as κ, and never use one to apply the κ≥0.4 threshold** — doing so once caused a confirmed signal to be wrongly benched.

*Usable as a qualitative hypothesis only:* seven signals that the tagging code benches as tier 2 are primary in our set — `appropriate_confidence`, `problem_ignored`, `ai_normalizes_difficulty`, `ai_offers_to_elaborate`, `ai_provides_alternatives`, `ai_asked_probing_question`, `user_provides_invalid_input`. Three of those are among our lowest-prevalence signals, so the tier flag may predict "hard to label consistently." Treat as a hypothesis to watch in our own κ round — not as evidence, and not as a number.

### 2. `wildchat/` W1 LLM–LLM κ
Preliminary and excluded from tiering by standing decision. Its codebook κ values appear to be copies of the same published values; no conflicts were found. Not authoritative.

## Repo-wide consistency (verified 2026-07-26)

Every κ stated anywhere in this repository now matches `annotation/kappa_paper_table5.csv`. Verified by scanning all `.md`/`.xml` files for markdown-table and inline `κ=` forms and diffing against the CSV — **0 disagreements**. `label_studio_config.xml` κ comments match Table 5 exactly for all 41 signals that carry one.

Re-run that check after any edit that touches a κ value. Superseded values are removed rather than annotated: a stale κ left in a decision record gets reused.

Everything else that a loose scan flags is a false positive: several decision tables have a *"replacement signal (κ=X)"* second column, so a naive regex attributes the replacement's κ to the row's signal. Those files state the correct values.

**Verified clean:** `label_studio_config.xml` κ comments match Table 5 exactly for all 41 signals that carry one.

## Documentation gap — 5 user signals have κ but don't record it

These carry published κ yet show no κ in `label_studio_config.xml` / `ANNOTATION_GUIDE.md`:

| Signal | Paper κ | Instances in our 148 |
|---|---|---|
| **`user_abandons_thread`** | **0.72** | **0** |
| `user_ambiguous_request` | 0.52 | 11 |
| `user_multi_request` | 0.50 | 6 |
| `user_validation_seeking` | 0.46 | 8 |
| `user_provides_invalid_input` | 0.41 | 1 |

`user_abandons_thread` at **κ = 0.72** is among the most reliable signals in the entire table — and we have labeled it **zero times in 148 conversations**, while our guide lists its κ as "—". This sharpens the earlier diagnosis: its absence is not signal unreliability, it is our gap (no rubric entry) and/or a genuine corpus property (ShareChat = conversations users *chose to share*, skewing toward resolved threads). Worth reporting either way.

## Rule going forward

Cite κ **only** from `annotation/kappa_paper_table5.csv`, always as arXiv:2603.15423**v2** Appendix C Table 5, and always described as **inter-model (Opus 4.6 vs GPT-5.4)** agreement. Our own measured κ, when available, is reported separately and never merged with these.
