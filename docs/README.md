# docs/ — map

CouplingBench Phase-1 documentation. Layer-1 is settled: **2 step-level categories** — H→AI (uptake) /
AI→H (legibility); **common ground is the conversation-level ablation, not a category**. Layer-2 was an
open fork (Clark grounding acts vs STPA control operations), resolved empirically — see `comparison.md`.

## Paper scope (decided 2026-06-19)

Two papers, two different benchmark types:

| | Paper 1 (current) | Paper 2 (future) |
|---|---|---|
| **Model** | MAST-style: taxonomy + naturalistic annotated corpus + LLM tagger | τ-bench-style: designed task suite + oracle-labeled agentic traces + LLM scores |
| **Data** | Existing traces (WildChat, ShareChat) annotated with coupling taxonomy | New collection: real humans in controlled agentic tasks, designed to elicit gap-cell failures |
| **Annotated corpus** | WildChat ~100K turns (predecessor 65-signal labels + our (op × direction) mapping); ShareChat 278 agentic turns (preliminary coupling labels) | Designed scenarios with oracle labels per benchmark-gap cell |
| **Artifact** | Taxonomy (8 ops × 2 directions, STPA-derived) + 3-model tagger + 16-cell completeness grid | Task suite, evaluation harness, LLM baseline scores |
| **Claim** | Theory-derived taxonomy is deployable on real data; 4 cells are benchmark gaps (falsifiable prediction) | Gap cells fill on agentic data; LLM X achieves Y% coupling-safe interaction rate |

**Key distinction — annotated data vs. designed scenarios.** Paper 1 annotates *existing naturalistic* traces (like MAST). Paper 2 constructs *designed task scenarios* with a known oracle (like τ-bench). Paper 1 does NOT need designed scenarios or real human data collection to publish.

**Paper 1 is NOT an LLM-evaluation benchmark.** No LLM is being scored on a task. The tagger labels coupling failures in any trace; the taxonomy and completeness grid are the contribution. Paper 2 is where different LLMs are compared on coupling-safe performance.

**Conversation-level extension (flagged 2026-06-19, collaborator input).** The current taxonomy is step-level (per turn-pair). A conversation-level tier is the natural extension: frustration accumulation, convergence failure, and the `escalate_handoff` decision (agent gives up and redirects user to act directly). This is motivated by human-human teaming norms (Cannon-Bowers shared mental models; Sheridan variable autonomy) which do not transfer automatically to human-agent interaction. Scoped to paper 2 or as a named extension in paper 1's limitations.

See `reference/motivation.md` (§6 contributions) and `reference/related_works.md` (§8 differentiation table) for the full positioning.

---

## Top level

| file | what |
|---|---|
| `comparison.md` | **The head-to-head**: both Layer-2 schemes applied to real data. Clark = 0% / control = 100% agentic coverage; complementary verdict. Backed by `src/taxonomy_compare.py`. |
| `shared-findings.md` | **Framework-agnostic numbers** both lenses cite (κ spine, W2 divergence rates, W3 no-reaction/triggers/repair, W2b/Stage-A agentic facts). Numbers live here once; lens docs reference them. |

## The two lenses (each: W1 codebook + thin W2/W3, W2b/Stage-A, W4 recodings)

| folder | Layer-2 | one-line fit |
|---|---|---|
| `communication/` | Clark's 5 grounding acts (present/clarify/accept/repair/maintain) | fits the communication channel (0 empty acts); action column empty (0% tool calls) |
| `safety/` | 8 control operations × UCA guidewords | fits the action channel (100% tool calls); seek/confirm/stop empty on chat, fill on agentic |

Recommended end state: **control as the primary backbone**, **Clark as the communication-channel
sub-model**.

## methodology/

| file | what |
|---|---|
| `derivation.md` | how the taxonomy was built: abductive-within-frame; the 3→2 Layer-1 decision; retiring the four-channel scheme + the dissolved 7 judgment calls; the Clark-vs-control resolution; the reliability spine. |
| `triggers_and_covariates.md` | the **mechanism layer** (single-side defects, human triggers, outcome markers, style) — explicitly **not** the taxonomy. |
| `advisor-update.md` | Phase-1 checkpoint memo for the advisor. |

## reference/ (framework-agnostic, corpus + prior-work)

`dataset-stats.md` · `wildchat-vs-sharechat.md` · `invisible-failures-summary.md` (predecessor
recompute) · `tau-bench-relation.md` · `related_works.md` · `motivation.md`.

## Code that produces these numbers

`src/taxonomy_compare.py` (comparison) · `src/predecessor_agreement.py` (κ) · `src/w3_coupling_stats.py`
(W3) · `src/thinking_divergence.py` (W2) · `src/w2b_agentic_turns.py` + `src/build_sharechat_agentic.py`
(W2b / Stage-A) · `src/coupling_lens.py` (retired four-channel MAP, kept for join-validation).
