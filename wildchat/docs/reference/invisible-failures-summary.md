# Invisible Failures in Human–AI Interactions — detailed summary

> **Predecessor.** Potts, Christopher & Moritz Sudhof. 2026. *Invisible Failures in Human–AI
> Interactions.* arXiv:2603.15423. Repo: `bigspin-invisible-failure-archetypes` (read-only reference).
>
> This is our working summary across four lenses: **motivation**, **method**, **findings**, and
> **analysis (hints for us)**. All numbers below are **recomputed by us** from their data files:
> the 100K conversation-level annotations (`wildchat_annotations_opus_v2.json.gz`, condition C, opus
> tagger), the 10K calibrated signal summaries (`score_10k_{opus,gpt5}_calibrated_transcripts.jsonl.gz`),
> and the 10K quality files across **conditions A/B/C × annotators opus/gpt5/sonnet**
> (`score_10k_quality_*.jsonl.gz`) — via `src/predecessor_stats.py` (distributions, co-occurrence,
> depth, walkaway) and `src/predecessor_agreement.py` (inter-annotator κ). Where our recomputed
> numbers differ from the arXiv text, it is because this is the **v2 100K** release and the paper
> headline used a different (smaller / differently sampled) cut; we flag those.

---

## 1. Motivation

The paper's claim is that the dangerous failures in human–AI conversation are not the loud ones
(the model errors and the user pushes back) but the **silent** ones: the model fails to meet the
user's goal and **the user never reacts** — they accept the answer, rephrase once and give up, or
simply walk away. Because nothing in the transcript looks like a complaint, these failures are
**invisible** to the usual signals (thumbs-down, explicit correction, regeneration) that product
teams and RLHF pipelines rely on. If most failures are invisible, then satisfaction metrics and
preference data systematically **under-count** failure, and the field is optimizing against a
biased signal.

The contribution is therefore (a) a **taxonomy** for detecting failure from conversational signals
rather than from user complaints, (b) a measurement that **most failures are invisible**, and (c) a
set of recurring **archetypes** describing *how* invisible failures unfold.

**Why this is our direct predecessor:** it is the only prior work (in the AI/agent-error domain)
that reads *both* the AI's behavior and the user's reaction off naturalistic traces, and that makes
the **visible-vs-invisible** distinction its object. That distinction is exactly the
"loud-failure / silent-failure" axis our **repair** dimension generalizes. We inherit its
**pipeline shape**, not its category list.

---

## 2. Method

**Data.** Naturalistic WildChat conversations (real users ↔ GPT-3.5/4, 2023–24), annotated by an
LLM tagger (opus) under a calibrated protocol. The release we analyze is **100,000 conversations**,
condition C.

**Three-layer signal taxonomy (50 signals used; 65 defined incl. calibration candidates).** Tagging
unit = a single AI response with full conversation context; user-behavior signals are tagged on the
preceding user turn.
- **Layer 1 — self-evident AI behaviors (24):** e.g. `ai_asked_clarifying_question`,
  `ai_hedges_uncertainty`, `ai_cites_source`, `ai_provides_caveats`, `ai_refuses_or_declines`.
- **Layer 2 — constructed/judgment AI signals (24):** e.g. `false_confidence`, `silent_assumption`,
  `intent_missed`, `under_delivered`, `over_delivered`, `problem_ignored`, `factual_error`,
  `generate_without_clarifying`, `error_recovery`, `conversation_advanced/stalled`.
- **Layer 3 — user/interaction signals (17):** e.g. `user_corrects_ai`, `user_expresses_frustration`,
  `user_abandons_thread`, `user_ambiguous_request`, `user_multi_request`, `ai_self_contradiction`,
  `ai_malfunction`.

**Derived classifications — as *defined* in the taxonomy** (`goal_failure`, `task_success`,
`partial_success`, `recovery`, `user_abandonment`), with the two that matter most:
- **visible_failure** = `goal_failure` is true **AND** the user reacted (`user_corrects_ai`,
  `user_expresses_frustration/dissatisfaction`, repeated `user_asks_clarification`, corrective
  `user_scope_change`).
- **invisible_failure** = `goal_failure` is true **AND** `visible_failure` is **not** — the AI made
  errors but the user did not push back.

The taxonomy frames these as deterministic functions of the per-turn signals. **In the released 100K,
however, `quality` / `failure_visibility` / `archetypes` were not computed in code — they were
produced by a second, transcript-level LLM pass** (condition C; see §2.1), which is why each carries a
free-text rationale and why two LLM taggers can disagree on them (the §3.5 κ).

**Archetypes (8) — assigned only to invisible failures**, by rule over the per-turn signals:
the_confidence_trap (`false_confidence`), the_silent_mismatch (`intent_missed`/`silent_assumption`/
`factual_error`), the_drift (`off_topic_drift`), the_death_spiral (`repetition`),
the_contradiction_unravel (`ai_self_contradiction`), the_walkaway (`user_abandonment`),
the_mystery_failure (goal_failure with no specific cause), the_partial_recovery (`recovery`).

**Calibration / reliability.** A two-pass design: 42 signals tagged "naive," 8 promoted to a
"calibrated" pass only when calibration produced **positive Δκ on held-out 10K** (Fleiss' κ **between
LLM taggers**, sonnet + gpt5; tuned on a 1K set, validated on 10K). The biggest calibration win is
`performative_hedge` (10K Δκ = +0.45); several signals were *demoted* because calibration hurt
agreement (e.g. `ai_summarizes` Δκ = −0.21). This is the inter-annotator-agreement backbone we'd
reuse — but note (§2.1) the "annotators" are all LLMs, so this measures **inter-LLM** consistency, not
human-validated accuracy.

### 2.1 The pipeline as a reusable template (what we'd inherit)

> **Crucial caveat on what "human" and "κ" mean here.** Humans *were* substantively involved in
> **developing** the taxonomy: the two authors manually reviewed ~100 WildChat transcripts each
> (guided by heuristic Sonnet labels) to converge on the failure modes and their definitions, and
> that review produced **108 human-labeled worked examples across 93 conversations** (the
> `clear_yes` / `clear_no` / `boundary` items in `calibration.json`). **But those human labels are
> used as in-prompt few-shot exemplars and to author the rubric — a *development/calibration* set —
> not as a held-out human-labeled *evaluation* set.** The full 100K (and the 10K/1K validation sets)
> are **LLM-tagged**, and **every reported κ — including §3.5 — is *inter-LLM* agreement
> (model-vs-model, e.g. opus-vs-gpt5), never LLM-vs-human accuracy.** So there is a **human-anchored
> rubric**, but **no held-out human gold standard** measuring whether the LLM labels are *correct* —
> and because the 93 human-labeled conversations sit *inside* the prompt, they cannot double as an
> unbiased test set. (Implication for us in §4.4–4.5: add the piece this pipeline lacks — a **held-out
> human-labeled eval set**, distinct from any in-prompt exemplars.)

A concrete blueprint for our own future annotation, end to end:
1. **Per-turn tagging (LLM).** Each AI response (with full context) is tagged for the ~50 signals by
   an LLM. **Two passes:** PASS1 is a flat "naive" prompt over all signals; PASS2 re-tags 8 hard
   signals with a **calibration block** per signal — an operational `definition`, a 5–7-step
   `decision_steps` decision tree, and **human-labeled worked examples** (`clear_yes` / `clear_no` /
   `boundary`, with rationales — the product of the authors' manual review, 108 examples / 93 convs)
   embedded in the prompt as **few-shot exemplars** (in `calibration.json`, produced across iterative
   "rounds"). The final per-turn label **cherry-picks**:
   PASS1 for signals where the naive prompt already agreed better, PASS2 for the 8 where the
   calibration block improved held-out *inter-LLM* κ.
2. **Majority vote** across ≥2 independent **LLM** taggers (opus / sonnet / gpt5) per signal — this is
   the closest thing to "ground truth" here, and it is a consensus *of models*, not of humans.
3. **Aggregate** per-turn signals into transcript-level summaries (signal→count, trajectory,
   first-negative).
4. **Transcript-level judgment — a *second* LLM pass (not a deterministic rule).** A separate LLM
   call reads the whole conversation under one of three input **conditions** — **A** = transcript text
   only, **B** = transcript + inline signals, **C** = signal profile only (no text) — and **outputs**
   the conversation-level labels `quality` (good/acceptable/poor/critical), `failure_visibility`
   (none/visible/invisible/mixed), and `archetypes` (each with evidence turns + a free-text
   rationale). The taxonomy *defines* these as deterministic functions of the per-turn signals (its
   `derived_classifications` + archetype rules — goal_failure, visible/invisible, recovery…), **but in
   production they are LLM-judged, not computed in code** — which is why each carries a rationale, and
   why annotators can *disagree* on them (that disagreement is the §3.5 κ). The 100K release uses
   **condition C**; the A/B/C contrast measures how much the signal layer alone carries the judgment.
   (The intermediate notions like goal_failure/recovery are rubric scaffolding — they are not separate
   output columns.)
5. **Gate on inter-LLM κ — this is a consistency check, *not* validation against truth.** κ is
   conventionally a *human* inter-annotator metric; here it is repurposed for **LLM-vs-LLM**
   agreement. The Δκ promotion gate keeps a calibration block only if it raises **model-vs-model**
   agreement on a held-out *LLM-tagged* set. **No LLM-vs-human κ is ever computed:** the only human
   labels in the entire pipeline are the **108 in-prompt exemplars** (exactly 3 per calibrated signal
   × 36 signals; 96 turns / 93 convs; 22 clear-yes / 35 clear-no / **51 boundary**), and because they
   are hand-picked teaching cases *embedded in the prompt*, they cannot serve as a held-out human test
   set. The lesson we take is the *Δκ-on-held-out discipline*, **not** that high κ certifies
   correctness — and not the specific signal list.

---

## 3. Findings (recomputed on the 100K v2 file)

### 3.1 Most failures are invisible — the headline
| | count | of all 100K | of failures |
|---|---:|---:|---:|
| no failure (`none`) | 37,443 | 37.4% | — |
| **invisible** | 49,368 | 49.4% | **78.9%** |
| visible | 7,632 | 7.6% | 12.2% |
| mixed | 5,557 | 5.6% | 8.9% |
| **any failure** | **62,557** | **62.6%** | 100% |

→ **78.9% of failures are invisible** (matches the paper's ~79%). Visible failures are a **1-in-8**
minority. Quality grades: good 36.9% / acceptable 41.0% / poor 18.2% / critical 3.9%.

### 3.2 Archetype prevalence (share of the 62,557 failures)
| Archetype | n | % of failures |
|---|---:|---:|
| the_walkaway | 58,995 | **94.3%** |
| the_silent_mismatch | 34,454 | 55.1% |
| the_confidence_trap | 21,868 | 35.0% |
| (none assigned) | 36,598 | 58.5% |
| the_partial_recovery | 8,386 | 13.4% |
| the_death_spiral | 3,464 | 5.5% |
| the_drift | 2,916 | 4.7% |
| the_contradiction_unravel | 301 | 0.5% |
| the_mystery_failure | 8 | 0.0% |

Archetypes co-occur (mean 1.67 per labeled conv; 2 archetypes is the modal count). The dominant
pairs are **silent_mismatch + walkaway** (33,229; P(walkaway | silent_mismatch) = 0.56) and
**confidence_trap + walkaway** (20,090; 0.34) — *walkaway* is the umbrella nearly every other
archetype rides under (see §4.2 for the precise reading). Note the co-occurrence **PPMI ≈ 0** for the
big three: they are individually so prevalent that they co-occur at roughly chance, so the pairings
are not a *special* association — just a consequence of high base rates. The real PPMI structure is
in **domain × archetype**: translation_language ~ mystery_failure (PPMI 2.39), personal_lifestyle ~
mystery_failure (2.02), software_development ~ death_spiral (0.83), general_knowledge ~
confidence_trap (0.57) — i.e. *which* failure mode dominates is domain-dependent.

### 3.3 Signal prevalence (10K calibrated summaries, conversation-level)
- **AI problem signals are common:** `generate_without_clarifying` 44.1%, `false_confidence` 26.6%,
  `problem_ignored` 26.2%, `under_delivered` 26.1%, `factual_error` 22.8%, `intent_missed` 22.4%,
  `silent_assumption` 20.2%.
- **User reaction signals are rare:** `user_corrects_ai` 3.4%, `user_expresses_dissatisfaction`
  1.8%, `user_expresses_frustration` 0.9%. (`user_abandons_thread` 8.3% is the most common "reaction,"
  and it is a *non-reaction*.)
- Positive/normal signals dominate overall: `conversation_advanced` 86.0%, `intent_addressed` 84.8%,
  `scope_matched` 73.2%.

**The invisibility mechanism, in one line:** AI problems fire at **20–44%** while explicit user
pushback fires at **<4%** — the gap between "something went wrong" and "the user said so" *is* the
invisible-failure rate.

### 3.4 Domain & depth
- **Verticals** are skewed to open-ended generative tasks: creative_writing 22.9%, design_ux 13.1%,
  software_development 10.7%, education_academic 9.5%, general_knowledge 5.4%.
- **Depth:** mean 2.14 turns, median 1, max 78; 63.4% single-turn. Failure rate *rises* with depth
  (58.1% at 1 turn → 88.1% at ≥10 turns), while the invisible *share* of failures *falls* sharply
  with depth — the central confound, quantified in §4.1.

### 3.5 Reliability — inter-annotator κ (the decision-relevant table)
Computed pairwise across the 10K interannotator files (`src/predecessor_agreement.py`). **All three
annotators are LLMs (opus / gpt5 / sonnet), so every κ below is *inter-LLM* agreement, not agreement
with a human gold standard** (see §2.1).
- **failure_visibility κ rises with signal grounding:** condition **A** (transcript only) κ = **0.45**;
  **B** (transcript + signals) **0.69–0.73**; **C** (signals only) **0.81–0.83** (three-way,
  opus/gpt5/sonnet). The 100K release is condition **C**, so the **invisible/visible label itself is
  reliable** (κ ≈ 0.81+). Grounding the judgment in the signal layer, not raw text, is what buys the
  agreement.
- **Archetype κ (condition C, opus vs gpt5):** the *frequent* archetypes are solid —
  confidence_trap **0.92**, walkaway **0.81**, death_spiral **0.80**, silent_mismatch **0.73**,
  "none" 0.86 — while the *rare* ones are noise: partial_recovery 0.43, drift 0.32,
  contradiction_unravel 0.54, mystery_failure 0.06. MACRO 0.55 / **MICRO 0.81**.
- **Signal κ (60 signals, opus vs gpt5):** median **0.50**; 18 signals ≥ 0.6, 28 in 0.4–0.6, 14 < 0.4.
  - **Reliable (κ ≥ 0.6):** ai_acknowledges_correction 0.81, ai_malfunction 0.78,
    ai_refuses_or_declines 0.76, ai_asserts_knowledge_limit 0.72, user_abandons_thread 0.72,
    user_corrects_ai 0.70, ai_asked_clarifying_question 0.70, performative_hedge 0.67,
    user_implicit_correction 0.67, ai_structured_response 0.65.
  - **Unreliable (κ < 0.4):** silent_assumption **0.20**, generate_without_clarifying **0.21**,
    over_delivered **0.10**, ai_self_contradiction 0.10, problem_surfaced 0.07, ai_implicit_refusal
    0.16, ai_stated_interpretation 0.22, ai_references_user_words 0.26.
  - These κ's track the predecessor's own calibration notes (their big win `performative_hedge` is
    solid here; `silent_assumption`, which they flagged as problematic, is near the bottom). The
    low-κ signals show a **systematic prevalence gap** — opus tags `silent_assumption` 20.2% vs gpt5
    5.6%, `over_delivered` 21.3% vs 1.7% — i.e. they are not noise-symmetric but **tagger-dependent
    judgments.**

---

## 4. Analysis — hints for our project

### 4.1 The "invisible" rate is largely a **single-turn artifact** (most important hint)
By construction, a failure can only be *visible* if the user takes another turn to react. The
invisible share of failures therefore **declines monotonically with depth**:

| turns | n | failure rate | invisible / failures |
|---|---:|---:|---:|
| 1 | 63,398 | 58.1% | **99.4%** |
| 2 | 14,746 | 60.6% | 66.0% |
| 3 | 7,506 | 69.5% | 51.9% |
| 4–9 | 12,092 | 79.1% | 37.9% |
| ≥10 | 2,258 | 88.1% | 25.0% |
| **multi-turn (≥2)** | 36,602 | 70.2% | **49.5%** |

In single-turn conversations (63% of the corpus) almost **everything** is "invisible" (99.4%) —
there is no second user turn in which to be visible. The headline **78.9% collapses to 49.5% on
multi-turn-only**, and to 25% in long sessions. So "most failures are invisible" is partly a
statement about *how short the conversations are*. **Hint:** our benchmark must not inherit this
confound. We need a **failure label independent of whether the user happened to take another turn** —
an *oracle* (private reference intent and/or task-success state), not "did the user react." This is
the strongest argument for our collection design over reusing their derivation rule directly.

### 4.2 Walkaway is the **visibility marker**, not the cause
A sharper reading than "it's all walkaway": `the_walkaway` is present in **98.0% of invisible
failures**, but **walkaway-*only* (no other failure archetype) is just 9.3%** — and only **8.1% of
all failures** have no cause signal beyond walkaway/none. So in ~90% of cases walkaway co-occurs with
a substantive cause archetype (silent_mismatch 55%, confidence_trap 35%). The right interpretation:
**walkaway is doing the *invisibility* labeling** (it is the operational stand-in for "the user
didn't react"), while a *separate* archetype carries the *cause*. **Hint:** this is good news and a
warning. Good: the predecessor *does* record cause (via the co-archetype), so cause/consequence are
not hopelessly entangled. Warning: because walkaway is near-universal in the invisible class, it is
**doing the same work as the depth confound in §4.1** — "no follow-up turn" gets read as both
*invisible* and *walkaway*. Our taxonomy should keep the **cause channel (H→AI vs AI→H)** explicitly
separate from the **consequence (abandon / repair-not-taken)**, and not let "no further turn" alone
define either.

### 4.3 Their signals already pre-sort onto our two channels — but imperfectly
The Layer-2/3 signals split naturally: `intent_missed` / `silent_assumption` /
`generate_without_clarifying` lean **H→AI (uptake)**; `false_confidence` / `performative_hedge` /
`problem_ignored` lean **AI→H (legibility)**; `error_recovery` / `ai_asked_clarifying_question` lean
**repair**. This is why reusing their signals as a *navigation layer* is attractive. **But** several
signals are genuinely cross-cutting (`generate_without_clarifying` is as much a missed-repair as an
uptake failure; `factual_error` is arguably orthogonal correctness, not coupling) — which is exactly
the **bucketing question** (since resolved — `../methodology/derivation.md`). The numbers above
also show *why the bucketing matters*: `generate_without_clarifying` alone (44.1%) would dominate any
H→AI rate, so where it lands materially moves the story.

### 4.4 The signals we'd most want for the **H→AI channel are the least reliable** (κ-grounded)
The §3.5 reliability table lands directly on the bucketing question. The candidate anchors for the
**uptake (H→AI)** channel — `silent_assumption` (κ **0.20**), `generate_without_clarifying` (κ
**0.21**), `over_delivered` (κ **0.10**), `intent_missed` (0.55) — are exactly the **noisiest**
signals, and tagger-dependent (opus tags them 2–4× more than gpt5). By contrast, several **AI→H** and
**repair/abandonment** signals are reliable: `performative_hedge` 0.67, `ai_asserts_knowledge_limit`
0.72, `ai_acknowledges_correction` 0.81, `ai_asked_clarifying_question` 0.70, `user_abandons_thread`
0.72, `user_corrects_ai` 0.70. **Hints:** (a) this is independent evidence to **keep direct bucketing
paused** — building an uptake-failure rate on κ≈0.2 signals would be measuring tagger idiosyncrasy,
not coupling; (b) a κ-weighted or κ-thresholded reuse (drop/down-weight signals below ~0.4) is the
minimum bar if we *do* reuse them as features; (c) the asymmetry says our own collection should
prefer an **oracle/operational definition of uptake** (private reference intent) over an
LLM-judged "did it understand?" signal, which is precisely where agreement breaks down.

### 4.5 The visibility label *is* trustworthy — but it measures reaction, not failure
Counterpoint to the cautions above: the failure_visibility judgment is **reliable** under condition C
(κ ≈ 0.81–0.83, three-way), and the frequent archetypes are reliable too (confidence_trap 0.92,
walkaway 0.81). So the predecessor's *headline construct* is well-measured; our quarrel (§4.1, §4.2)
is not with its reliability but with what it **operationalizes** — user *reaction*, which is
confounded by depth/abandonment. **Hint:** we can safely *reuse the reliable signals/archetypes as a
navigation and feature layer*; what we must *replace* is the **failure definition** (reaction →
oracle), not the annotation machinery. **One added caveat:** "reliable" here is *inter-LLM* (§2.1) —
κ ≈ 0.81 means two LLMs agree, not that they are right. The authors' ~100-transcript manual review
grounded the *rubric and few-shot exemplars*, but those human labels sit inside the prompt, so no
held-out LLM-vs-human accuracy is ever measured. Since our project hinges on subtle cross-channel
judgments (exactly the signals that already disagree at κ ≈ 0.2 *between LLMs*, §4.4), our pipeline
should add the thing this work omits: a **held-out human-labeled eval set** (separate from any
in-prompt exemplars) to validate the taggers, rather than trusting inter-LLM agreement alone.

### 4.6 Structural ceilings we must break (the gap that motivates collection)
The corpus is **chat-only, 2023-era models, heavily single-turn, open-ended-generative** (creative
writing #1). It has **no tool actions, no shared state, no consequences**, and **no private
ground-truth goal** — so it can show *that* a loop broke (via walkaway) but never *whether the agent
took the right action in the world* or *whether the human understood the agent's plan before a
consequential step*. Those are precisely the agentic coupling cells our benchmark targets, and they
are **structurally absent** here. The predecessor proves the phenomenon (silent failure is the norm)
and hands us the pipeline; the **action/consequence + real-human + cross-channel** combination is the
hole we fill.

---

## 5. One-paragraph takeaway for the advisor

The predecessor establishes — and we independently reproduced (78.9% invisible of 62,557 failures on
100K) — that **silent failure is the norm** in real human–AI chat, gives us a **validated 50-signal,
3-layer pipeline** (per-turn signals → derived classifications → 8 archetypes, with κ calibration),
and shows the two channels we care about already latent in its signals. Our recomputation adds three
things that **shape our design**: (1) the invisible rate is **largely a depth artifact** — it falls
from 99.4% (single-turn) to 49.5% (multi-turn) to 25% (≥10 turns), because "visible" requires a
follow-up turn; (2) `the_walkaway` is present in **98%** of invisible failures but is the
*visibility marker*, not the cause (walkaway-only is 9.3%) — a substantive cause archetype usually
co-occurs; (3) the visibility label and frequent archetypes are **reliably measured** (κ ≈ 0.81–0.92
under condition C), **but the very signals we'd want for the H→AI/uptake channel are the least
reliable** (`silent_assumption` 0.20, `generate_without_clarifying` 0.21). The convergent implication:
keep the annotation machinery and the reliable signals as a **feature/navigation layer**, but
**replace the failure definition** — from "did the user react" to an **oracle** label (private
reference intent / task-success state) with **explicit cross-channel cause attribution** (H→AI vs
AI→H), realized on **tool actions / shared state with a real human** — the combination no existing
corpus, this one included, provides. *(We are deliberately **not** computing coupling-coordinate
"bucketed" statistics yet; the κ evidence above is part of why that decision is paused.)*
