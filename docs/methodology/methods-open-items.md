# Method section — open items and provenance

Working notes for `paper/methods.md`. **Nothing here is paper text**; it was carried at the end of `methods.md` until 2026-07-30 and moved out so that file is the Method section and nothing else.

**Status.** §3.1, §3.2.1–3.2.3 and §3.2.5 describe work done or fully specified. §3.2.4 is designed and live but unmeasured. §3.3 is designed, not yet run. Nothing above states a Stage-2 result.

### Open — the κ adequacy threshold

§3.2.4 now leaves the attained κ blank and states no numeric gate. An earlier draft asserted "average κ ≥ 0.6, all primary signals ≥ 0.4" — **those numbers were not sourced and not agreed**; removed 2026-07-27.

Two options once the round is run:
- **Report and refine, no threshold** (what Cemri et al. actually did — they reported 0.24 → 0.92 → 0.84 and refined where needed, without a pre-declared gate). Simplest and matches the comparator.
- **Declare a threshold with a source.** The only defensible anchor is Landis & Koch's bands, which we already use implicitly: 0.41–0.60 "moderate", 0.61–0.80 "substantial". Our signal-selection filter (κ ≥ 0.4) sits on the lower boundary, so reusing 0.4 for our own κ is at least internally consistent. Anything above that needs justifying, not asserting.

Decide after seeing the numbers; do not back-fill a threshold that the observed values happen to clear.

### Open decisions before Stage 2 starts

1. **Hazards H1–H3 need the advisor's sign-off.** Jun fixed the set at three on 2026-07-30, cut by **direction**: H1 human→agent, H2 agent→human (both per paired turn), H3 the loop (per conversation). The earlier authority hazard is dropped as a hazard and becomes a candidate *mechanism* under H1. **H3's admission rule — two alternating exchanges with each divergence traceable to the preceding turn's — is proposed by Claude and not yet agreed.** STPA requires the analyst to supply them, so writing them is mandated — but their content is ours, and every downstream claim traces to it.
2. **The control-action list for the human and the agent** must be fixed before enumeration starts; the whole UCA grid rests on it.
3. **Deferred by Jun, 2026-07-30:** worked event statements and the detailed usage of the five UCA components. §3.3 states the machinery and carries no example sentence; the incident record and a worked pass belong in `docs/methodology/stage2-coding-protocol.md` and `stage2-worked-example.md`, both still marked SUPERSEDED until that discussion happens.

### Empirical check — can a signal combination be the error type? (2026-07-27)

| Level | Units with ≥1 signal | Distinct combinations | Seen exactly once |
|---|---|---|---|
| Conversation, all signals | 148 | **127** | 93% |
| Conversation, failure signals only | 64 | 36 | 64% |
| Span-group, all signals | 938 | 312 | 69% |

Naming combinations directly yields 127 types over 148 conversations. Restricted to failure signals, 36 over 64 — and the most frequent "combinations" are **single signals** (`factual_error` ×7, `false_confidence` ×6, `ai_malfunction` ×5), so the scheme degenerates into naming individual signals, which is the predecessor's archetype architecture — a layer in which four of eight categories are single-signal triggers (`method-comparison.md` §4). At span level recurrence improves (68% covered by combinations seen ≥3×) but the frequent patterns are the prevalent positive ones (`conversation_advanced` alone ×109) — frequent because common, not because they are errors. **Combinations can identify incidents; they cannot type them.**

### Source verification (2026-07-27)

Verified verbatim from PDFs: Leveson (2004) *Safety Science* 42(4) §3.2 — Ashby's four conditions, "must be (or contain) a model of the system", Fig. 3 (human supervisor over an automated controller, each with a process model); Leveson, Daouk, Dulac & Marais (2003) — "Any controller—human or automated—must contain a model of the system being controlled… inconsistencies between the model of the process used by the controllers… and the actual process state"; Rismani, Dobbe & Moon (2024) arXiv:2410.22526 — UCA identification "could be applied to AI systems with minimal modification", unsafeness "frequently depends on sociotechnical context rather than on the technical timing or sequencing of a control action", role fluidity in the control diagram, loss-scenario classes including incorrect process models. **Corrected 2026-07-30** — the second quote had been recorded as "often depend[s] … rather than purely technical timing or sequencing", which is not the source wording; both occurrences fixed. The PDF extracts in two interleaved columns, which is what let the paraphrase pass an earlier substring check.

**Method-literature verification (2026-07-30).** The Stage-2 sequence was checked against the open-coding literature; extraction, verbatim quotes and findings are in `docs/methodology/stage2-sequence-validation.md`. Verified verbatim from PDFs: Fereday & Muir-Cochrane (2006) six stages and the Boyatzis three-part code format; Boeije (2002) within-case-first comparison order; Hsieh & Shannon's stated limitation of directed content analysis; Kundisch et al. (2022) *BISE* on Nickerson iteration direction. **Still unverified:** Nickerson et al. (2013) "logical consequence" wording for the meta-characteristic (EJIS paywalled; secondary source has only "must relate to"), and the objective-ending-conditions list, which §3.3.7 gives as a three-item paraphrase of a longer original.

**Not verifiable in-repo:** Cemri et al. (2025), "different root causes may produce similar surface behaviors" (§3.3.6) — no local copy. Check against the published version before submission.

**Leveson & Thomas (2018) *STPA Handbook*, verified verbatim 2026-07-30** against the extracted text. Page numbers are the handbook's own: hazard definition and the `<System> & <Unsafe Condition> & <Link to Losses>` form with the three writing rules (pp. 16–19); the four unsafe types and the five UCA parts with "The ordering is not critical. The key point is that UCAs contain these five parts" (p. 36); "The UCA context should specify the actual (true) state or condition that would make the control action unsafe, not a particular controller process model or belief (which may or may not be true)" with the handbook's own correct/incorrect contrast (p. 40); loss-scenario definition and the two scenario types, "Why would control actions be improperly executed or not executed", Fig. 2.17 (p. 42); the four inadequate-process-model causes (p. 44); causes of inadequate feedback (pp. 46–47); the control path, Fig. 2.19 (pp. 48–49).

### Scope decision — WildChat-derived work excluded (2026-07-27, tightened 2026-07-30)

With STPA as the backing theory, error types are derived from loss scenarios over the Stage-1 signals. **Not carried forward**: the 8 control operations and the Layer-1 × Layer-2 grid, and the parts of `method-comparison.md` §2/§4 that contrast their archetypes against the 8-op grid.

**Nothing WildChat-derived enters the paper** (Jun, 2026-07-30) — it was a preliminary, subjective feasibility check, so it is excluded as method as well as result. `wildchat-control-probe.md` moved to `wildchat/`. One use remains to resolve: `appendix.md` §A cites the predecessor's own WildChat annotations as the prevalence comparison behind the `intent_addressed` merge (Decision 1). That is their released data rather than our probe, but it is still a WildChat number in the paper and needs a ruling.

**What survives untouched.** The Stage-1 layer is theory-neutral by construction — 148 conversations, 1,996 placements, 50 signals, the rubric, the decision and ruling log, the agreement set, the automated-annotator plan. None of it depends on which theory sits above it. Worth one sentence in the paper: *the signal layer is released separately because it is reusable under a different interpretive frame — a claim we can make because we changed ours.*

**The one idea worth keeping is already in §3.3.6, sourced from the handbook rather than from the probe.** Classifying occurrences by which of STPA's four inadequate-process-model conditions holds, and reporting the residual, is a candidate validation to run on our own 148 after Stage 2 has categories — where it is strictly better than it was on WildChat, because the internal blocks let "received incorrect feedback" and "necessary feedback does not exist" be separated by evidence rather than by proxy.

### Risks a reviewer will raise

- *"STPA is a design method; this is post-hoc storytelling."* Mitigated by the witnessed-only rule — every reported event is instantiated in the corpus and anchored to signal placements — and by the held-out replication. §3.3.7 must not be softened.
- *"n = 148 is small for ICLR."* Mitigated by the precision framing, the automated scale-up to 703, and by the contribution being a validated instrument plus a falsifiable structural claim rather than a prevalence table.
- *"The error types are the predecessor's archetypes relabeled."* Mitigated by the structural argument in `method-comparison.md` §4 — four of their eight archetypes are single-signal triggers — and by the set-aside paragraph in §3.3.6.
- *"Post-refinement κ is measured on the same conversations used to refine."* This is the real cost of running **one** round. Cemri et al. refined on Round 1 and then validated on **new** traces in Round 2 — "in order not to fall into the fallacy of using training data as test data." With a single round our post-refinement number is in-sample, and must be reported as convergence on the refinement set, never as generalization. Two ways to answer it if a reviewer presses, in order of cost: run a small second round on unseen conversations (the cheapest real fix), or lean on the automated annotator's validation against the 148 gold as the out-of-sample evidence. Worth deciding before submission rather than in rebuttal.

### References to verify before submission

**Leveson (2004) *Safety Science* 42(4):237–270** · Leveson, Daouk, Dulac & Marais (2003) *Applying STAMP in Accident Analysis* · Leveson (2012) *Engineering a Safer World*, MIT Press · Leveson & Thomas (2018) *STPA Handbook* · **Rismani, Dobbe & Moon (2024) arXiv:2410.22526** · Rismani et al. (2023) CHI · Thomas (2021) *Enhancing Human Factors Analysis with STPA* · Nickerson, Varshney & Muntermann (2013) *EJIS* 22(3):336–359 · Shelby, Diaz & Prabhakaran (2025) *Taxonomy of User Needs and Actions*, arXiv:2510.06124 · Fereday & Muir-Cochrane (2006) *IJQM* 5(1):80–92 · Hsieh & Shannon (2005) *Qual Health Res* 15(9):1277–1288 · Timmermans & Tavory (2012) *Sociological Theory* 30(3):167–186 · Cemri et al. (2025) arXiv:2503.13657, NeurIPS D&B · Potts & Sudhof (2026) arXiv:2603.15423v2.

### Withdrawn measurement — archetype coverage (2026-07-30)

`method-comparison.md` §4 previously reported their archetype rules firing on **37.8%** of our 148, leaving 62% uncovered, and called it "the empirical argument for the re-mapping." Re-run from `label_studio.sqlite3` this session, the figures reproduce **exactly** (33/23/20/3/1/1; 56 fire, 92 do not). They were withdrawn anyway, because they do not support the claim:

- **Only 57 of 148 conversations (38.5%) carry any failure signal.** Their layer is gated on `goal_failure`, so it is *supposed* to produce nothing on the rest. The 148 denominator scores it on conversations where firing would be wrong.
- **Restricted to failure-bearing conversations, coverage is 43/57 = 75.4%** — 37/57 = 64.9% excluding the partial-recovery proxy. Respectable, not damning.
- **13 of the 56 fires occur in conversations with no failure signal**, i.e. the partial-recovery proxy misfiring. Part of the headline was our noise.
- The re-implementation is degraded in three rules (`silent_assumption`, `user_abandonment`, `recovery` are all absent from our 50) and **two of the eight archetypes are unmeasurable** — the earlier write-up admitted one.

Do not reinstate. The replacement argument in §4 is structural and does not depend on our corpus.
