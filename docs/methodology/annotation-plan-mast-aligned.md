# Annotation Methodology — MAST-Aligned Taxonomy Development Plan

*For the coupling-errors paper (ICLR submission). Methods section reference and advisor review.*
*Aligned with MAST (Cemri et al., 2025, Section 3.2) — the closest process template for our work.*

---

## Execution log (updated 2026-07-07)

| Plan step | Status |
|---|---|
| 1–5 scope / corpus / derivation / audit trail / operationalization | Documented. Rubric now **v0.3** after the agentic block coverage audit: (signal × block) cells as the taxonomy unit, cross-block evidence rule, internal-block signal subsets, review rulings R1–R19 (Decisions 9–15 in `signal-decisions.md`; authoritative record `annotation/review_rulings_log.md`). `signal_checklist.csv` synced; final signal set = `label_studio_config.xml` (51 signals). |
| 6 pilot (tasks 1–82) | Done, plus the internal-block re-annotation applied to the Label Studio DB (Decision 14: +75/−9 labels; Decision 15: 8 candidate fixes). Corpus: 886 placements across 79 submitted annotations; internal blocks now substantively labeled (reasoning 43, analysis 8, code 15 placements). |
| 7 freeze | **IN PROGRESS.** Freeze criterion restarted under v0.3: Jun annotates tasks 83→~100; 10 consecutive tasks with no new signal decision → strip `CANDIDATE_SIGNAL` from the live config, tag v1.0-freeze (Signal Decision). Calibration material for B/C is ready: `annotation/label_review_context.md` (every boundary case, PREV/LABELED/NEXT context, bolded evidence). Housekeeping before B/C access: delete the 13 excluded tasks. |
| 8 Round-1 IAR | **Sample size resolved (Xuan, 2026-07-07):** "5–10 conversations is OK, but we may need to pick the samples specifically so that all the failure cases are included." Selection procedure (our theoretical-sampling analog, to be documented in the paper): agent pre-screen of ~30 unseen conversations → coverage matrix of failure-signal families per conversation → greedy set-cover pick of 8–10 jointly covering every failure category. |
| 9–14 | As planned below. Annotators B and C recruited. Ordering fixed: freeze → IAR Rounds 1–2 → B/C independent annotation → n=148 → LLM annotator (IAR precedes bulk labeling; the IAR batch counts toward 148). |

---

## Overview

MAST's workflow: theoretical sampling → open coding → taxonomy derivation →
operationalization → 3 IAR rounds → automated annotator.

Our workflow follows the same validation pipeline but differs at the derivation stage:
theory-bootstrapped (STPA + Norman + Clark), not purely inductive. This document traces each
MAST step, identifies our gap, and states the solution.

**Reference:** Cemri, M. et al. (2025). *Why Do Multi-Agent LLM Systems Fail?* arXiv:2503.13657.
Section 3.2 (Inter-annotator Agreement Study and Iterative Refinement).

---

## Step 1 — Research scope

| | |
|---|---|
| **MAST** | Failure modes *internal* to multi-agent LLM systems: reasoning, tool use, memory, orchestration. Agent-only faults. 150+ MAS traces from agentic pipelines. |
| **Our gap** | Our scope is **bidirectional coupling** (H→AI uptake + AI→H legibility) — extends beyond MAST's agent-internal focus. The boundary and its justification were not explicitly documented. |
| **Solution** | Scope justification is in `derivation.md §3b` (why not MAST/STPA-for-AI; why coupling; why single-agent+tools is paper-1 scope). This must be cited in the methods section. |

---

## Step 2 — Corpus construction

| | |
|---|---|
| **MAST** | "theoretical sampling" from 150+ traces — deliberate curation to stress-test different taxonomy cells. Per round: "each from a different MAS." |
| **Our gap** | ShareChat is a **convenience sample** — not theoretically sampled. No documented rationale for choosing ShareChat over WildChat or LMSYS. English filter (716→703) not framed as a corpus construction choice. |
| **Solution** | (1) Justify ShareChat as **agentic-representative**: the only public corpus with reasoning blocks, analysis blocks (tool outputs), multi-turn agentic tasks — not available in WildChat or LMSYS (both chat-only). (2) The **stratified sampling** for IAR rounds (Step 8) is our per-round "each from a different MAS" analog. (3) Acknowledge convenience-sample limitation in the paper. |

---

## Step 3 — Taxonomy derivation

| | |
|---|---|
| **MAST** | "theoretical sampling and open coding" — bottom-up from traces. Read traces, identify failure instances, name and group them. No prior theoretical framework imposed. ~20 failure modes derived inductively from data. |
| **Our approach (aligned with MAST)** | We follow the same bottom-up direction: (1) observe agentic traces; (2) label observable behaviors with signals (vocabulary from predecessor study, 65 signals); (3) observe that the labeled signals naturally organize into two levels — Layer 1 (direction of transfer: H→AI vs. AI→H) and Layer 2 (type of operation: 8 control operations). The two-level taxonomy is **read off from the labeled data**, not imposed a priori. This matches MAST's open coding in spirit: traces → labeled instances → grouped structure. |
| **Gap vs. MAST** | MAST derives failure modes from scratch (no prior vocabulary). We start with the predecessor study's 65 signals as the initial vocabulary — analogous to MAST beginning with an initial taxonomy list rather than blank labels. The question for the paper is: does the two-level structure emerge from the signal labels, or was it assumed? The answer must be shown empirically, not claimed. |
| **Solution** | Present the derivation in bottom-up exposition order (following MAST): *signals observed on traces → signals cluster by transfer direction (Layer 1) → signals cluster by operation type (Layer 2) → the resulting structure matches theoretical predictions from STPA + Norman (validates both the data clustering and the theory).* The theoretical framework (`derivation.md §3a`) is cited as post-hoc validator of the data-observed structure, not as the source. The abductive audit trail (Step 4) provides the evidence that this clustering actually happened in the data. |

---

## Step 4 — Abductive audit trail

| | |
|---|---|
| **MAST** | No equivalent — open coding is inherently inductive; data-driven claim is implicit. IAR rounds serve as validation. |
| **Our gap** | Because derivation is theory-first, we must prove data **changed** the taxonomy. Without this, a reviewer dismisses it as "Clark relabeled" or "STPA imposed." ICLR requirement (`taxonomy-method-abductive.md`): (1) codebook-evolution table; (2) ≥1 "data changed taxonomy" moment; (3) per-cell κ + held-out human eval; (4) theory-derived prediction tested. |
| **Solution** | All four requirements before submission: (1) **Codebook-evolution table**: `derivation.md` Decisions 1–3a → format as v1→final table with trace evidence for every add/merge/kill. (2) **"Data changed taxonomy" moments** (three banked): `reasoning_surface_mismatch` (new cell, 18% CoT turns, not in predecessor); `silent_assumption` detectable with reasoning reference; `false acceptance` confirmed absent. Cite explicitly in paper. (3) IAR rounds (Steps 8–12) deliver κ + held-out eval. (4) Test ≥1 grounding prediction (e.g., completed repair → lower invisible-failure persistence in subsequent turns). |

---

## Step 5 — Operationalization

| | |
|---|---|
| **MAST** | Annotators receive "failure modes and definitions." Simple definitions per mode. Refinement can change definitions, merge, split, add, erase. |
| **Our gap** | (1) Our rubric (`sharechat_rubric.json`) exceeds MAST: decision steps, calibration examples, block-placement rules — a strength. (2) But κ values are **borrowed from predecessor study** (arXiv:2603.15423), not measured on our corpus. (3) Rubric evolved through 8 signal-decisions (June 25–28); earlier annotations may be based on superseded definitions. (4) Four signals remain unresolved: `ai_asks_followup` (Grey candidate), `ai_asks_confirmation` (proposed, not added), `ai_missing_retrieval` (1 task validated), 5 pending reclassifications (Decision 8). |
| **Solution** | (1) Declare **v2.0 frozen** after Phase 1 (Tasks 83–100). (2) Version rubric: v1.0 = predecessor-aligned; v1.x = Decisions 1–8; v2.0 = frozen for IAR. Log each version in `signal-decisions.md`. (3) Resolve 4 open items before freeze. (4) Acknowledge in paper that predecessor κ values are initial estimates; final κ measured on our corpus in IAR rounds. |

---

## Step 6 — Pilot annotation (development phase)

| | |
|---|---|
| **MAST** | No explicit pilot. Open coding process itself serves as the derivation pass. Round 1 is intentionally rough (κ=0.24) because taxonomy is untested. |
| **Our gap** | Tasks 1–82 are the pilot. Rubric evolved during these tasks (8 signal-decisions). Done by single annotator + Claude — risk of rubric calibrated to one annotator's judgment. |
| **Solution** | Frame Tasks 1–82 as **development/pilot phase** in the paper — equivalent of MAST's open coding. State: "Tasks 1–82 = development phase; IAR begins at Task 101 with conversations not seen during rubric development." Tasks 1–82 contribute to signal frequency distributions but not to κ claims. |

---

## Step 7 — Rubric freeze and calibration set *(our addition — no MAST analog)*

| | |
|---|---|
| **MAST** | No analog. Refinement happens reactively through IAR disagreements. |
| **Our gap** | Without a declared freeze, the rubric can change after IAR rounds begin, invalidating κ. |
| **Solution (Phase 1, Tasks 83–100)** | Annotators: Jun + Claude. ~18 conversations. **Goals:** (1) Resolve 4 open items. (2) Confirm stability: no new `signal-decisions.md` entries after Task 100. (3) Produce **calibration set**: 5 tasks (Tasks 96–100), Jun's gold labels + per-sentence rationales, for training Annotators B and C. **Freeze criterion:** zero new signal-decisions entries in last 10 consecutive tasks. **Output:** `sharechat_rubric.json` v2.0 (frozen), calibration set. |

---

## This week — agreement round (Steps 8–9)

| # | Step | Who | Output |
|---|---|---|---|
| 1 | One Label Studio project per annotator — same 10 conversations, same import order, no shared view | Jun | 2 projects (B, C) |
| 2 | Hand over the round rubric: `ANNOTATION_GUIDE.md` + `sharechat_rubric.json` v0.5, unchanged for the duration | Jun | rubric frozen for the round |
| 3 | **B and C annotate the 10 independently** (441 blocks each) | B, C | 2 label sets |
| 4 | **Compute κ before refinement and work the disagreements together** — pairwise A·B, A·C, B·C per signal plus average and minimum; every disagreement traced to the decision step that produced it | Jun, B, C | κ table 1 + revision list |
| 5 | Revise rubric → v0.6 | Jun | changelog entry per revision |
| 6 | **All three re-annotate the same 10** under v0.6 | Jun, B, C | 3 label sets |
| 7 | Compute κ **after** refinement | Jun, B, C | κ table 2 → methods §3.2.4 |
| 8 | Re-scan the 148 for anything v0.6 changed | Jun | 148 on current rubric |
| 9 | B and C begin their allocation of the 148 | B, C | gold labels in progress |

Steps 1–2 are prep, 3–7 are the agreement round proper, 8–9 start the gold phase.

**A·B and A·C are not independent the way B·C is** — Jun wrote the rubric. Report all three pairs plus the pairwise minimum; B·C is the number that carries the most weight.

**Steps 8–9 may spill past the week.** Steps 3–7 are what must stay intact.

## Step 8 — Round 1: Initial multi-annotator IAR

| | |
|---|---|
| **MAST** | "5 different MAS traces... three annotators annotate... Cohen's Kappa score of 0.24." |
| **Our gaps** | (1) "5 different MAS" = stratified — no strategy specified for us. (2) 3 annotators required, not optional — with 2, every disagreement goes to Jun, reintroducing solo bias. (3) 5 tasks too small for 40+ signals; rare signals may have zero instances. (4) No pairwise κ reporting structure. |
| **Solution** | Annotators: Jun + B + C (**3 required**), independent. Sample: **5–10 unseen conversations per Xuan's guidance (2026-07-07): "we may need to pick the samples specifically so that all the failure cases are included."** Selection is coverage-driven, not stratum-count-driven: |

**Coverage-driven selection procedure (theoretical-sampling analog, documented for the paper):**
1. Agent pre-screen of ~30 unseen conversations (never annotated, outside tasks 1–~100) for structural features and candidate failure-signal families.
2. Build a coverage matrix: conversation × failure-signal family (which failure categories each conversation likely exhibits).
3. Greedy set-cover: pick 8–10 conversations that jointly include **every failure category**, preferring conversations that also cover the structural strata below.

| Stratum (secondary preference) | Coupling coverage |
|---|---|
| Coding tasks (code blocks present) | `factual_error`, `under_delivered`, `ai_malfunction` in code blocks |
| Agentic + tool calls + reasoning blocks | `reasoning`/`analysis` block placement; cross-block evidence rule |
| Multi-turn ≥4 human turns | `user_corrects_ai`, `adaptation`, `user_repeats_request` |
| Single-turn | Baseline; AI-output signals in isolation |
| Tool error in analysis block | `ai_malfunction` (Decision 11); `error_recovery` |

B and C read calibration set + rubric v2.0 independently (no discussion with Jun). All 3 annotate via Label Studio. Compute all 3 pairwise κ per signal (Jun-B, Jun-C, B-C). Report: pairwise average, pairwise minimum, count of signals below 0.4. **Output:** complete disagreement log (signal × sentence × both annotators' labels × which decision step diverged).

**Selection refinement (2026-07-24 — validity invariant + sequencing).** The κ-validity property is *rubric-development contamination*, **not** whether a conversation was previously labeled: a conversation labeled under the frozen rubric that did not itself generate a signal-decision/ruling is a valid κ datapoint, identical in status to a never-seen one scored by the current rubric. Since the rubric's last structural change was R21 (task-102), tasks **103+** are clean frozen-rubric data — their existing labels give a *real* coverage matrix, so the agent pre-screen (procedure step 1) is only needed to reach signals the clean pool still lacks, and Jun's existing labels can serve as his κ arm (B and C label the same tasks blind). **Sequencing:** finish the development annotation first (toward 148), *then* run the set-cover over the enlarged clean pool — a larger pool yields better candidates for the rare failure signals. Guard: any new ruling during the remaining labeling breaks the freeze (exclude that task, restart the 10-task freeze count). Provisional set-cover over the current clean pool (tasks 103–119) → 110, 109, 106, 108, 115, 116, 114, 119, 103, 117 (35/48 signals; absent: under_delivered, user_misled, user_implicit_correction, repetition, off_topic_drift, ethical_tension, performative_hedge, +7 singleton) — a fallback only, superseded once the pool grows. **LOCKED (2026-07-26, revised after Decisions 16–17), pool = ALL 148, rubric v0.5:** **`6, 7, 21, 41, 49, 67, 74, 101, 110, 120`** — 10 conversations, **full 50/50 signal coverage**, 441 paragraphs. Depth: 27 signals at ≥3 instances, 9 at ≥5. conv_id map (C1–C10) in `annotation/agreement_set_convid_map.csv`.

*Why the pool widened from 103–150 to all 148.* The earlier restriction assumed tasks 1–102 were compromised as κ datapoints by rubric development. The operative risk is actually **stale labels** — a task carrying an obsolete reading — and our standing practice removes it: every rubric change triggers a re-scan and update of all previously-labeled samples (Decision 16 re-screened all 148 for `appropriate_confidence`; Decision 17 swept all 148 for three signals; R22 triggered an audit of every existing `false_confidence` span). A conversation that once generated a ruling is arguably a *better* κ datapoint: it directly tests whether the resulting rule is now written clearly enough for another annotator to reach the same label without the deliberation. Restricting to 103–150 would also cap coverage at 40/50 — ten signals have no instances in that range.

*Why full coverage was chosen over a lighter set.* A 286-paragraph alternative (dropping task 101) reaches only 48/50, losing `performative_hedge` and `user_abandons_thread`. Task 101 costs 173 paragraphs but is the **only long-form relational/roleplay conversation** in the corpus, and that genre is 12.8% of conversations and **20.7% of the corpus by paragraph volume**. Excluding it would bias the agreement round away from a fifth of the data for convenience, and would leave reviewers able to ask why two active signals were never measured (Jun, 2026-07-26).

**Option B live:** LS projects `ShareChat-Agreement-B` (id 2, `zhenyub@vt.edu`) and `ShareChat-Agreement-C` (id 3, account TBD) hold this set, blind (0 annotations), `label_config` identical to project 1, Sequential import in C1–C10 order. κ merges the three projects on `conv_id`.

**Label Studio setup — Option B (decided 2026-07-24; instance is LS v1.23.0 Community).** The running server exposes **no** overlap control (`maximum_annotations`) in the UI (Enterprise-only) and has **no annotator roles**, so on a shared project the peers could see/edit each other's annotations (κ leakage). Decision for this round: **one Label Studio project per annotator, each holding the same 10 tasks** (default `maximum_annotations=1` — the setting is unnecessary here). Blind isolation is structural: each project contains no foreign annotations. Compute pairwise κ by merging the three projects on `conv_id`. Cross-annotator reference uses a stable **C1–C10 map keyed on `conv_id`**, never LS `task.id` (differs across the three separate imports) or `inner_id`/UI "#" (aligns only under identical import order — so import the 10 in identical order and set `sampling = Sequential`). Option A (single shared project, `maximum_annotations = 3` set via REST `PATCH /api/projects/{id}` since the UI lacks it) is **deferred to the later full ~148 independent labeling**, not this agreement round.

---

## Step 9 — Round 1 refinement: iterate to consensus

| | |
|---|---|
| **MAST** | "iteratively changing the taxonomy **until we converge to a consensus regarding whether each and every failure mode existed... in all 5 of the collected traces**." Changes allowed: definitions, split, merge, add, erase. |
| **Our gaps** | (1) "Discuss disagreements" ≠ convergence — no termination criterion. (2) No re-annotation verification: rubric could be revised but still produce disagreement on Round 1 traces. |
| **Solution** | (1) Review disagreement log; for each case, identify which decision step diverged. (2) Revise rubric: update decision steps, add calibration examples, merge/split/demote signals. (3) **All 3 annotators re-annotate the original 10 Round 1 traces** under the revised rubric. (4) Repeat until all 3 annotators label every sentence identically in all 10 traces — MAST's "each and every" standard. Disallowed: changing definitions to post-hoc fit one annotator's labels. **Output:** `sharechat_rubric.json` v3.0, `signal-decisions.md` Decisions 9+. |

---

## Step 10 — Round 2: Post-refinement validation

| | |
|---|---|
| **MAST** | "another set of 5 traces, each from a different MAS... κ=0.92 among each other... on the first try." |
| **Our gaps** | (1) No stratification for Round 2. (2) No pairwise structure — high average can mask one weak pair. (3) Missing ordering constraint: B and C must finish overlap set before independent annotation. |
| **Solution** | Annotators: Jun + B + C, independent. Sample: **10 NEW conversations, Tasks 111–120**, same stratification — none from Round 1 or Tasks 1–100. Compute all 3 pairwise κ + average + minimum per signal. **Decision gate:** avg κ ≥ 0.6 AND all primary signals ≥ 0.4 → proceed; signal still below 0.4 → demote to Orange/Grey, recheck df; avg still below 0.6 → run Round 3. **Ordering constraint:** B and C complete all 50 overlap-set tasks before receiving independent-set assignments. |

---

## Step 11 — Round 3: Stability confirmation *(conditional)*

| | |
|---|---|
| **MAST** | "Round 3... κ=0.84." Decrease from 0.92 to 0.84 accepted as normal. Rubric not re-opened. Round 3 = stability check, not a quality gate. |
| **Our gap** | Treated as optional. MAST treats it as standard when Round 2 required changes. |
| **Solution** | **Conditional**: run if Round 2 required rubric changes; skip if no changes were needed. Annotators: Jun + B + C. Sample: 10 NEW conversations, Tasks 121–130, same stratification. Slight κ decrease from Round 2 = acceptable (do not re-open rubric unless a primary signal drops below 0.4). |

---

## Step 12 — Full overlap annotation *(our addition)*

| | |
|---|---|
| **MAST** | No direct analog. 15 traces across 3 rounds served as both validation and κ basis. |
| **Our gap** | 40+ signals need more instances than 20–30 IAR traces for stable per-signal κ. MAST reports trace-level κ; we need sentence-span-level per-signal κ for the appendix table. |
| **Solution** | Annotators: Jun + B + C, independent. Sample: **50 conversations, Tasks 101–150** (includes IAR round traces — labels already recorded, no re-annotation). Compute per-signal κ on 50-conversation base. Report all 3 pairwise κ + average + minimum per signal. This is the appendix κ table. Ordering constraint: B and C complete before independent annotation. |

---

## Step 13 — Independent annotation: reaching n=148

| | |
|---|---|
| **MAST** | Not explicitly documented in Section 3.2. |
| **Solution** | Jun: Tasks 1–100 (development phase; independent set for coverage, not κ). Annotator B: Tasks 151–200 (~50, solo, after overlap complete). Annotator C: Tasks 201–250 (~50, solo, after overlap complete). Total: 100 + 50 + 50 + 50 ≈ 150 conversations. **Paper framing:** Tasks 1–100 = development phase; Tasks 101–150 = overlap set (κ); Tasks 151–250 = independent sets. |

---

## Step 14 — LLM annotator validation *(MAST Section 3.4 analog)*

| | |
|---|---|
| **MAST** | "automated MAST annotator using an LLM-as-a-judge pipeline" validated against human labels. |
| **Our gaps** | (1) No validation threshold. (2) No reporting format. (3) Self-referential bias unaddressed: Claude annotating Claude outputs may under-label its own failure signals. MAST had no self-reference issue. |
| **Solution** | Run Claude through frozen rubric v3.0 on 50-conversation overlap set after gold labels adjudicated. Compute per-signal κ (Claude vs. human gold). **Threshold:** κ ≥ 0.6 = usable for automated annotation; below 0.6 = requires human. **Reporting:** side-by-side table with human-human κ in appendix. **Self-reference as finding:** "Does Claude under-label its own failure signals?" — report direction and magnitude of systematic divergence per signal as a result, not only a limitation. |

---

## Summary table

| Step | MAST analog | Annotators | Sample | Target / Output |
|---|---|---|---|---|
| 1. Scope | MAST scope framing | — | `derivation.md §3b` | Documented in methods section |
| 2. Corpus | MAST theoretical sampling | — | ShareChat 703 conv. | ShareChat justified; stratified sampling = IAR analog |
| 3. Taxonomy derivation | MAST open coding | — | `derivation.md §3a` | 8 ops + Layer-1 documented |
| 4. Abductive audit trail | (none — MAST inductive) | — | 3 documented moments | Codebook-evolution table; "data changed taxonomy" evidence |
| 5. Operationalization | MAST failure mode definitions | — | `sharechat_rubric.json` | v1.x rubric; predecessor κ as initial estimate |
| 6. Pilot annotation | MAST open coding (extended) | Jun + Claude | Tasks 1–82 | Rubric development; paper = development phase |
| 7. Rubric freeze | (our addition) | Jun + Claude | Tasks 83–100 | v2.0 frozen rubric; calibration set |
| 8. Round 1 IAR | MAST Round 1 (κ=0.24) | Jun + B + C | 10 stratified (101–110) | Initial κ; disagreement log |
| 9. Round 1 refinement | MAST iterative refinement | Jun + B + C | Re-annotate Round 1 | 100% consensus on all 10 traces |
| 10. Round 2 IAR | MAST Round 2 (κ=0.92) | Jun + B + C | 10 stratified (111–120) | κ ≥ 0.6 avg; all primary ≥ 0.4 |
| 11. Round 3 (conditional) | MAST Round 3 (κ=0.84) | Jun + B + C | 10 stratified (121–130) | Stability confirmation |
| 12. Full overlap | (our addition — paper κ table) | Jun + B + C | 50 (Tasks 101–150) | Per-signal κ for appendix |
| 13. Independent annotation | MAST implied broader corpus | B (151–200), C (201–250) | ~50 each | Coverage toward n=148 |
| 14. LLM annotator | MAST Section 3.4 | Claude vs. human gold | 50 overlap set | Side-by-side κ; self-reference bias audit |

---

## Gaps resolved

| # | MAST element | Gap | Resolution |
|---|---|---|---|
| 1 | Theoretical sampling | Convenience corpus, no justification | ShareChat justified as agentic-representative; stratified IAR sampling = "different MAS" |
| 2 | Open coding data-driven claim | Theory-first derivation unproven | Abductive audit trail: codebook-evolution table + 3 "data changed taxonomy" moments |
| 3 | "Each from a different MAS" | No IAR sampling strategy | Stratified 10-conv sample across 5 coupling scenarios per round |
| 4 | "Each and every... all traces" | Discussion ≠ convergence | Re-annotate Round 1 traces after refinement; stop only at 100% consensus |
| 5 | "Three annotators" | Third annotator optional | 3 required for IAR; enables majority vote before Jun adjudication |
| 6 | "Average κ among each other" | No pairwise reporting | All 3 pairwise κ + average + minimum per signal |
| 7 | Train/test separation | Ordering unspecified | B and C complete overlap set before independent assignments |
| 8 | LLM pipeline validated | No threshold or format | κ ≥ 0.6 threshold; side-by-side table; self-reference bias = finding |
| 9 | Clean pre-IAR derivation | Derivation interleaved with annotation | Tasks 1–82 = development phase; IAR starts at Task 101 |
| 10 | Rubric stability before IAR | No freeze declaration | v2.0 frozen after Task 100; versioned in `signal-decisions.md` |
