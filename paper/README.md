# Paper folder

Working record of the paper's methodology. Everything here must be traceable to a file or a re-runnable computation — no placeholder numbers.

*Snapshot: 2026-07-27.*

## The three files

| File | Contents |
|---|---|
| **`methods.md`** | **The Method section.** Two-stage design · corpus, sampling, sample size · Stage 1 (signal inventory, unit, rubric, prior-κ provenance, agreement design, automated annotator) · Stage 2 (control structure, hazards, coupling events, open coding, validation) · reproducibility. **Figures 1 and 2 live here**, in §3.2 and §3.3. Working notes are fenced at the end under "Notes to ourselves" and are **not** paper text. |
| **`appendix.md`** | Appendix material. **A.** `intent_addressed` merge justification (predecessor comparison + strict-gate screen) · **B.** agreement-set selection · **C.** low-prevalence signal screens. |
| **`method-comparison.md`** | Positioning against Potts & Sudhof (arXiv:2603.15423v2) and Cemri et al. / MAST (arXiv:2503.13657): vocabulary overlap, their archetype rules applied to our 148, corpus representativeness, the metric split, the one-round agreement defence. |

**Nothing else belongs in this folder.** Working documents — coding protocols, worked examples, advisor agendas — go to `docs/methodology/`. Related: `docs/methodology/advisor-questions-open-coding.md`, plus `stage2-coding-protocol.md` and `stage2-worked-example.md` — both **superseded**, written under CAST and awaiting rewrite.

**No WildChat-derived material appears in the paper.** That work was a preliminary, subjective feasibility check; it is not a result, not a method we cite, and it now lives in `wildchat/` (`wildchat-control-probe.md`, moved out of this folder 2026-07-30).

## Status

| Component | State |
|---|---|
| Corpus funnel (8,364 → 703 → 148) | **Documented** — measured |
| Why ShareChat (block-type evidence) | **Documented** — measured |
| Sampling: randomized import order, verified | **Documented** — simple random sample, ρ = −0.025 |
| Sample-size justification | **Documented** — per-signal binary power (α=.05, N=148 ⇒ 90% power at w≥0.266) + Wilson reporting precision |
| Annotation unit, placement rules, rubric versioning | **Documented** |
| Re-scan practice; exhaustive screens | **Documented** |
| Agreement-set selection + rationale | **Documented** |
| One-project-per-annotator design | **Documented** |
| Prior-κ provenance + single-source rule | **Documented** |
| Our own κ | **Awaiting Round 1** |
| LLM-annotator procedure | **Designed**, not written up as a runnable protocol |
| Stage 2 (STPA, adapted) | **Designed**, not run |

## Source-of-truth files this draws on
- `annotation/data/filter_report.txt`, `prepare_stats.txt` — corpus funnel
- `annotation/sharechat_rubric.json` (v0.5) — decision rules
- `annotation/label_studio_config.xml` — the 50-signal set
- `annotation/kappa_paper_table5.csv` — the only citable prior κ
- `docs/methodology/kappa-provenance.md` — single-source rule
- `docs/methodology/signal-decisions.md` — Decisions 1–18
- `annotation/review_rulings_log.md` — rulings R1–R23
- `annotation/agreement_set_convid_map.csv` — C1–C10 map
- Leveson & Thomas (2018) *STPA Handbook* — Stage-2 method; verified verbatim, see `methods.md` source-verification note

## Open items
1. **Advisor sign-off on hazards H1–H3** — cut by direction: H1 human→agent and H2 agent→human at the paired turn, H3 the loop at the conversation level. STPA requires them; the content is ours and everything downstream traces to it. There is no loss list, by decision (`methods.md` §3.3.3). H3's admission rule is proposed, not agreed.
2. **The control-action list** for the human and the agent — must be fixed before enumeration starts; the whole UCA grid rests on it.
3. **Incident selection rule for Stage 2** — must be fixed before coding starts; not adjustable afterwards.
4. **LLM-annotator protocol** — written procedure and validation design against the 148 gold.
5. **Decision 1's `intent_addressed` rationale** in `docs/methodology/signal-decisions.md` still needs restating on the evidence in `appendix.md` §A.6.
