# Notebooks — reproducible statistics

Each documented statistic in `docs/` is regenerated here by importing a pure `compute()` function
from `src/` (no logic is duplicated in the notebooks). The scripts still print the same numbers from
their CLI (`python src/<x>.py`); the notebooks call the same functions and render tables/charts.

Run a notebook from anywhere — the first cell puts `src/` on the path. Headless:

```
jupyter nbconvert --to notebook --execute --inplace notebooks/0*.ipynb
```

## Notebook → backing scripts → source docs

| Notebook | Reproduces (headline numbers) | `src/` functions | Source docs |
|---|---|---|---|
| **01_datasets** | WildChat 837,989 convs; ShareChat 129,584 / claude 911 (thinking 28.6%); reasoning ratio **0.84** (43%) vs 2.02 artifact | `dataset_stats.compute`, `thinking_divergence.reasoning_ratio`, `coupling_examples.thinking_gap` | `reference/dataset-stats.md`, `reference/wildchat-vs-sharechat.md`, `shared-findings.md` |
| **02_reliability_w1** | signal κ tiers (silent_assumption 0.20 … ai_acknowledges_correction 0.81); archetype κ MACRO 0.55 / MICRO 0.81; failure_visibility κ A/B/C | `predecessor_agreement.{signal_kappa, archetype_kappa, failure_visibility_kappa}` | `safety/w1-codebook.md`, `communication/w1-codebook.md`, `reference/invisible-failures-summary.md`, `methodology/{triggers_and_covariates,derivation}.md` |
| **03_invisible_failures_w3** | 62.6% failure, **78.9% invisible**, multi-turn 49.5%; archetypes; domain×archetype PPMI; triggers + lift; **67.1%** no-repair | `predecessor_stats.compute`, `w3_coupling_stats.compute` | `safety/w2w3-recoding.md`, `shared-findings.md` (W3), `reference/invisible-failures-summary.md` |
| **04_thinking_divergence_w2** | heuristic rates (false_confidence 18.6% …); LLM-judge n=50 (silent_assumption **12%**, reasoning_surface_mismatch **18%**) | `thinking_divergence.compute` + saved `data/derived/thinking_divergence.json` | `shared-findings.md` (W2), `communication/w1-codebook.md` |
| **05_agentic_stageA_w2b** | **278 turns / 162 convs**; reconstruction **248 turns / 1,233 calls** (897/336); feedback gap **17.6%**, **14/16** | `w2b_agentic_turns.compute`, `taxonomy_compare.load_agentic`, `build_sharechat_agentic.summarize`, `feedback_gap.compute` | `safety/w2b-stageA-agentic.md`, `shared-findings.md` (W2b), `reference/wildchat-vs-sharechat.md` |
| **06_taxonomy_mapping** | 65-signal mapping (coupling 42, by-op, L1 45); **full signal-pairing analysis** — contrast **6/16**, holes 7/10 AI→H, polarity poles, direction contrast, verdicts (benchmark_gap 4 / structural_zero 4 / set_aside 2), masking (3) & position (2) curated layers; Clark vs control **0%/100%**; each section ends in a *"What we conclude"* cell (+2 bar charts) | `build_control_mapping.compute`, `pair_analysis.compute`, `taxonomy_compare.compute` | `criteria/signal-pairing.md`, `comparison.md`, `methodology/advisor-update.md` |

## Notes

- **`compute()` is side-effect-free.** Running a notebook does not overwrite any `docs/` or `data/`
  file — the CSV/JSON/MD writes live only in each script's `main()`.
- **01 is heavy.** It loads the cached `docs/dataset-stats.json` (written by `python src/dataset_stats.py`);
  the recompute path reads ~3.2 GB of parquet + raw ShareChat CSVs.
- **04 makes no LLM call.** The heuristic judge runs live; the LLM-judge (n=50) numbers are loaded from
  the cached verdicts, not re-generated.
- **Predecessor data.** Notebooks 02 & 03 read the predecessor repo at
  `/data/wang/junh/githubs/bigspin-invisible-failure-archetypes` (path hard-coded in the scripts).
