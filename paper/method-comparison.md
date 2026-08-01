# Method comparison — our annotation plan vs. Invisible Failures and MAST

> **Scope note, updated 2026-07-30.** Stage 2's backing theory is **STPA, adapted** (`methods.md` §3.3). Sections written against the earlier *8 control operations* mapping (§2 table) are superseded and retained only as a record. Everything about Stage 1 — vocabulary overlap (§3), corpus and sampling (§7.1), the metric split (§6.3), the human-agreement contribution (§1, §6) — is unaffected, because the signal layer does not depend on the theory above it.

Positioning and gap analysis against the two closest methodological templates.
Every number here is either quoted from the source or computed from our own DB (`label_studio.sqlite3`, project 1, 148 conversations / 1,996 placements).

**Sources**
- **Invisible Failures** — Potts & Sudhof, *Invisible failures in human–AI interactions*, arXiv:2603.15423**v2**. Signal vocabulary and archetype rules also read from the local `bigspin-invisible-failure-archetypes/taxonomy-tagging-code/taxonomy.json`.
- **MAST** — Cemri et al., *Why Do Multi-Agent LLM Systems Fail?*, arXiv:2503.13657. §3 (Grounded Theory + IAA), §3.4 (LLM annotator).

---

## 1. The three studies at a glance

| | **MAST** | **Invisible Failures** | **Ours** |
|---|---|---|---|
| Research question | Why do multi-agent LLM systems fail? (root cause, for debugging) | How often do AI failures go **unnoticed by the user**? | **Where** does the human–agent control coupling break down, and **in which direction**? |
| Object of the taxonomy | failure *modes* (root causes) | failure *archetypes* (episode shapes) | failure *cells* (control function × direction) |
| Categories | 14 modes / 3 categories | 8 archetypes | 8 control operations × 2 directions = 16 cells |
| Vocabulary origin | built from scratch (open coding) | 65 signals in 3 layers (24/24/17) | **48 of their 65** + 2 added = 50 |
| Unit of annotation | one trace (~15k lines) | one **turn** (AI response + preceding user turn) | one **sentence span inside a typed block** |
| Internal-state access | full agent traces | none (chat only) | reasoning / analysis / code blocks |
| Annotators | **3 humans**, 20 h+ each | **LLMs only** (Opus 4.6, GPT-5.4) | **humans** (lead + 2 collaborators), LLM for scale |
| Agreement reported | human–human Cohen κ, 3 rounds: **0.24 → 0.92 → 0.84**; out-of-domain 0.79 | **inter-model** κ: archetypes 0.84 micro / 0.74 macro; signals 0.47 macro (AI) / 0.58 macro (user) | human–human κ, 1 round, 10 conversations, 50/50 signal coverage |
| Human validation at scale | yes (the 3 annotators *are* the gold) | **none** — "we sampled 100 transcripts for manual review by each of us" during taxonomy development only | 148 human-gold conversations |
| Automated annotator | o1 few-shot vs. human gold: κ 0.77, acc 0.94, F1 0.80 | the LLM *is* the annotator; no human gold to validate against | planned: validate against the 148 gold |
| Scale | 150 traces (GT) → 1,600+ annotated | 100K conversations | 148 gold + 555 automated |

---

## 2. The core claim — same vocabulary, different stage 2

Jun's framing is correct and, more importantly, **the predecessor's own design licenses it.**

Invisible Failures is explicitly two-stage (§3.2): stage 1 tags turn-level signals; stage 2 assigns an archetype. In their released code the stage-2 layer is **a deterministic rule layer over stage-1 signals** — not a second judgment:

```
"The confidence trap":       false_confidence fires on 1+ turns
"The drift":                 off_topic_drift fires on 1+ turns
"The death spiral":          repetition fires on 1+ turns
"The contradiction unravel": ai_self_contradiction fires
"The walkaway":              user_abandonment is true
"The silent mismatch":       intent_missed OR silent_assumption OR factual_error
"The partial recovery":      recovery is true
"The mystery failure":       goal_failure true but no AI failure signal fired
```
*(`taxonomy.json → archetypes.rules`; gated by `goal_failure ∧ ¬visible_failure`.)*

Two consequences.

**(a) The signal layer is separable by construction.** Their Table 1 compares three inputs for stage 2 and finds **Signals-only** best (κ 0.84 micro / 0.74 macro, 94% agreement) — ahead of Signals+Transcript (0.77) and Transcript-only (0.62). Their own result is that the signal report carries the interpretation, and that adding the raw transcript *hurts*. That is the strongest available warrant for reusing stage 1 under a different stage 2.

> **Honest caveat to keep in the paper.** Higher agreement on a compressed input is partly an artifact — two annotators given the same short summary have less to disagree about. Their Table 1 supports separability; it does not prove sufficiency. State it as "the authors' own protocol treats the signal layer as the sufficient statistic for interpretation," not as a proof.

**(b) Their archetypes are near-isomorphic to single signals.** Four of the eight are one-signal triggers. The archetype layer supplies a gate and a name, not a structure. Ours supplies a structure: 50 signals map **many-to-one** into 16 (operation × direction) cells, each with a positive and a failure pole. That is a genuinely different mapping type, not a relabeling — which is the objection a reviewer will raise the moment they see "8 archetypes" next to "8 operations."

| | Invisible Failures archetypes | Our control operations |
|---|---|---|
| Kind of object | trajectory/outcome shape of a conversation | function the coupling was performing |
| Assignment | conversation level, gated on invisible failure, residual catch-all | (signal × block) placement; multiple ops co-occur |
| Polarity | failure only | **paired** — positive and failure pole per cell |
| Derivation | boolean rule over signals | STAMP control-loop element per op (`derivation.md` Decision 3a) |
| Empty cells | none (catch-all absorbs) | **predicted and confirmed at the signal-pairing layer** (`confirm_authorize`·AI→H = 0, `act_execute`·AI→H = 0, `stop_defer`·H→AI = 0) — a conclusion about the vocabulary, reported as such |

---

## 3. Vocabulary overlap — measured

| | Count |
|---|---|
| Predecessor signals in `taxonomy.json` | **65** (layer 1: 24, layer 2: 24, layer 3: 17) |
| Predecessor signals with published κ (Table 5) | **63** — `user_empowered` and `user_misled` are in the code but **not in the paper's agreement table** |
| Our active signals | **50** |
| Ours inherited from the predecessor | **48** (19 layer-1, 15 layer-2, 14 layer-3) |
| Ours newly added | **2** — `ai_missing_retrieval`, `ai_asks_followup` (grey) |
| Predecessor signals we dropped | **17** |

Dropped: `ai_asks_for_feedback`, `ai_empathy_expressed`, `ai_implicit_refusal`, `ai_references_user_words`, `ai_self_contradiction`, `ai_stated_interpretation`, `ai_summarizes`, `appropriate_hedge`, `error_commitment`, `generate_without_clarifying`, `intent_addressed`, `over_delivered`, `plow_through`, `problem_surfaced`, `scope_matched`, `silent_assumption`, `user_scope_change`.

**The four signals carrying no published κ are exactly our four non-blue/teal/purple labels** — orange `user_empowered` / `user_misled` (predecessor code, unmeasured) and grey `ai_missing_retrieval` / `ai_asks_followup` (ours). The colour coding already encodes provenance correctly; say so in the paper rather than letting a reviewer discover it.

---

## 4. Why we replace their interpretation layer

The argument is structural, and needs no measurement on our corpus.

**Four of their eight archetypes are single-signal triggers** (`taxonomy.json → archetypes.rules`): the confidence trap is `false_confidence`, the drift is `off_topic_drift`, the death spiral is `repetition`, the contradiction unravel is `ai_self_contradiction`. A layer in which half the categories are renamings of one signal supplies a **gate and a name, not a structure**.

**It answers a different question.** Their archetypes describe the *shape* an invisible failure took. We ask which direction the coupling failed in, and by what mechanism. Different question, different layer — this does not require their layer to be deficient, and we do not claim it is.

Two facts about their vocabulary do bear on us directly, and are reported as scope rather than as criticism: **two of their eight archetypes cannot be evaluated on our signal set at all** (`ai_self_contradiction` and `goal_failure` are not in our 50), and their rule layer is gated on a `goal_failure ∧ ¬visible_failure` derivation we do not reproduce.

> **Removed 2026-07-30.** This section previously reported that their archetype rules fire on 37.8% of our 148 and leave 62% uncovered, and called it "the empirical argument for the re-mapping." The figure reproduces exactly, but it does not support that claim and was withdrawn: only 38.5% of the 148 contain any failure signal, so the layer is being scored against a denominator in which most conversations *should* produce no archetype. Restricted to failure-bearing conversations its coverage is 75.4% (64.9% excluding a proxy rule), and 13 of the 56 fires occur in conversations with no failure signal at all — noise from our own proxies. The full check is recorded in `docs/methodology/methods-open-items.md`.

## 5. Where we follow Invisible Failures

| Element | Adopted | Note |
|---|---|---|
| Two-stage architecture (behavioural signals → higher construct) | **yes** | the reusable core; stage 2 is ours |
| Signal vocabulary | **yes**, 48/65 | keeps our κ comparable to a published baseline |
| Real in-the-wild human–AI conversations (not benchmark traces) | **yes** | ShareChat vs. their WildChat |
| Failure without user protest as the central phenomenon | **yes** | their "invisible" ≈ our AI→H legibility failure |
| Turn-level tagging unit | **no** — we use sentence spans inside typed blocks | needed for (signal × block) cells; **makes our κ non-comparable to theirs in magnitude** |
| LLM-only annotation | **no** | we produce human gold first |
| Archetype rule layer | **no** | replaced by the operation × direction grid |

## 6. Where we follow MAST

| Element | Status |
|---|---|
| Human annotators, real inter-annotator agreement | **adopted** — and this is where we beat the predecessor, which has none |
| Documented codebook evolution (definitions changed / split / merged / erased) | **adopted** — 18 signal decisions, 23 rulings, rubric v0.1→v0.5 |
| A failure taxonomy meant to be **diagnostic** rather than descriptive | **adopted** — control operations are functions, like MAST's modes are causes |
| LLM annotator validated against human gold with a stated threshold | **planned**, not done |
| **Round 1 → refine → Round 2 on unseen data → Round 3** | **not adopted** — we run one round |
| Theoretical sampling of the corpus | **partly** — set-cover for the agreement set only; the 148 are sequential (see §7) |

### 6.1 The one-round decision — how to defend it

MAST's credibility rests on the arc 0.24 → refine → **0.92 on new traces** → 0.84. We are running a single round, by decision. That is defensible, but only with the right framing:

> Our single agreement round is the analogue of MAST's **Round 2/3**, not Round 1. MAST's Round 1 exists to expose an untested taxonomy; ours was already exposed and revised through 148 development conversations, 18 signal decisions and 23 boundary rulings, with every rubric change re-applied retroactively to all prior labels. What we have not done is subject the rubric to *three independent annotators* before this round — so the round tests transmissibility of a refined rubric, which is exactly what MAST's Round 2 tests.

**Pre-commit to the response now, before the numbers arrive**, so the reporting choice is not post-hoc:

| Round-1 result | Action |
|---|---|
| avg κ ≥ 0.6, all primary signals ≥ 0.4 | report and proceed — a MAST-Round-2-equivalent result |
| avg κ ≥ 0.6, some signals < 0.4 | report per-signal; demote the failing signals to unmeasured/candidate rather than deleting them |
| avg κ < 0.6 | run MAST's refinement loop: disagreement log → rubric revision → **re-annotate the same 10** → Round 2 on 10 unseen |

### 6.2 Copy MAST's LLM-annotator reporting format exactly

MAST §3.4 reports, against human gold: accuracy 0.89 / recall 0.62 / precision 0.68 / F1 0.64 / **κ 0.58** for o1 zero-shot, versus 0.94 / 0.77 / 0.83 / 0.80 / **κ 0.77** few-shot — and accepts the few-shot version on that basis. Two things to carry over:

1. **Report the same five columns**, not κ alone. κ collapses precision and recall, and for rare signals recall is the number that decides whether the 555 automated conversations are usable.
2. **Few-shot is what made it work** (0.58 → 0.77). Our analogue of MAST's in-context examples is the rubric's ordered `decision_steps` plus calibration examples — richer than anything MAST gave o1. Run the zero-shot arm anyway: the delta is a result about how much operationalization buys, which MAST reports and no one else has for this vocabulary.

### 6.3 Which metric belongs to which part of the corpus

The two measurements answer different questions and are **not interchangeable**:

| | **The 148 gold** | **The 555 LLM-annotated** |
|---|---|---|
| Question | Is the *instrument* reliable? | Is the *predictor* valid? |
| Comparison | human ↔ human, no ground truth | LLM ↔ gold, gold treated as truth |
| Statistic | **Cohen's κ** (+ percent agreement for high-prevalence signals) | **accuracy · precision · recall · F1 · κ** |
| Why | with two fallible raters and no reference, only chance-corrected agreement is meaningful | with a fixed reference, error is directional — over- vs under-firing are different problems |

Three refinements that matter more here than they did for MAST:

- **Keep κ in the LLM arm too.** With 50 signals over typed blocks, most (signal × block) cells are absent, so a model that predicts "no signal" scores high accuracy. κ and positive-class F1 are the honest headline; accuracy alone is not.
- **Recall is the gate for the 555.** Under-firing a rare signal does not look like an error in the output — it looks like a clean zero, and it silently deflates prevalence. Set a **per-signal recall floor**, not just a global κ threshold, and report **macro** (per-signal, unweighted) alongside micro. Micro is dominated by `conversation_advanced` alone (553 of 1,996 placements).
- **Split hygiene.** The 148 gold were all used to develop the rubric — "train" from the *rubric's* perspective, though not from the LLM's, which never saw the labels. Cleanest design: hold out a fixed slice of the gold for LLM validation and draw few-shot examples only from the remainder, so the exemplars do not come from the conversations being scored.

---

## 7. Gaps this comparison opens

**7.1 The 148 are a random sample of 703, annotated in order.** All 703 conversations were imported into Label Studio in **randomized order**, then annotated sequentially from the top. Verified: Spearman ρ between Label Studio task order and corpus order = **−0.025** (0 ⇒ randomized). The annotated set is tasks 1–150 minus 2 skipped (12, 47) = 148.

This is a **simple random sample**, not a convenience sample, so representativeness follows from the design: the sample proportion is an unbiased estimator of the corpus proportion for every signal, and the sampling variation is already carried by the Wilson intervals reported per signal.

**One line closes the sampling question** — "conversations were randomized at import and annotated in order; ρ = −0.025 against corpus order." Nothing further is needed, and a post-hoc balance check would be worse than nothing: significance-testing sample-versus-population differences under known randomization tests a null that the design guarantees, and it invites a reader to interpret ordinary sampling variation as bias. Composition of the annotated set is reported descriptively in `methods.md` §3.1 alongside the corpus figures, without inferential comparison.

**7.2 Our κ will not be numerically comparable to theirs.** Different unit (span-in-block vs. turn), different rater type (human–human vs. model–model). Say this explicitly in the κ table caption; otherwise a reader will read our number against their 0.47/0.58 macro-κ as if it were the same measurement.

**7.3 We have no conversation-level failure/visibility judgment.** Their headline (79% of failures invisible) rests on a four-value conversation-level field — `none` / `visible` / `invisible` / `mixed` — judged, not derived. We cannot currently reproduce or contest that number.

**7.4 Missing from our plan, present in both templates: a generalization test.** MAST re-ran the frozen taxonomy on two unseen frameworks (κ 0.79). Invisible Failures re-ran their protocol on Future-2K. We have 555 unannotated conversations — an out-of-sample check is available at no annotation cost once the LLM annotator is validated.

---

## 8. An opportunity worth flagging (not yet scoped)

Invisible Failures §5.1 builds **Future-2K** by re-prompting 2K WildChat prompts through frontier models to simulate "the future," and reports that failure rates fall from ~42% to <10% while invisible failures stay >85% of what remains. They name three limitations of that design themselves: single-turn only, raw API rather than the real product, and no account of evolved user behaviour.

**Our corpus is the un-simulated version of their counterfactual**: real 2026 conversations with a frontier model, multi-turn, in-product, with tool use and visible reasoning. Adding the conversation-level failure/visibility field (§7.3) — four values, applied to 148 conversations — would let us test their central prediction on real rather than synthetic future data, and would give the paper a direct, quantitative point of contact with the predecessor's headline result.

**Recommendation: defer.** It is a rubric change and would break the freeze with the agreement round already live in both collaborator projects. Revisit after Round 1 κ is computed.

---

## 9. Two sentences for the paper

> We adopt the behavioural signal vocabulary of Potts & Sudhof (2026) — 48 of their 65 signals — but replace their second stage. Where their rule layer maps signals to eight archetypes describing the *shape* an invisible failure takes, we map the same signals to eight control operations crossed with two coupling directions, describing *which coordination function failed and in which direction*; and where their reliability evidence is inter-model agreement between two LLM annotators, we contribute the first human inter-annotator agreement on this vocabulary, following the three-annotator protocol of Cemri et al. (2025).
