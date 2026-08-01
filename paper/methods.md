## 3. Method

We derive a taxonomy of **human–agent coupling errors** in two stages. Stage 1 produces a reliable, low-inference layer of **observable behavioural signals** over real conversations. Stage 2 treats those signals as evidence and derives **error types** through a control-theoretic incident analysis. The separation is deliberate: the two stages have different epistemic status, different annotators, and different validation criteria, and conflating them is the principal way taxonomies of this kind become unfalsifiable.

**Why two stages rather than one.** A single-pass scheme that asks annotators to read a transcript and name a failure type confounds *what happened* with *why it counts as a failure*. Stage 1 asks only the first question and is validated by inter-annotator agreement. Stage 2 asks the second and is validated by agreement on its theory-supplied fields plus a held-out replication. Hybrid coding designs already place a reliability test between building a code template and applying it (Fereday & Muir-Cochrane, 2006); we make that step a stage of its own, with three annotators and per-signal agreement over a full inventory, because the layer being tested is the evidence base for everything above it. This mirrors the two-stage design of Potts & Sudhof (2026), whose own ablation found that annotators given only the signal report agreed substantially better ($\kappa = 0.84$) than annotators given the raw transcript ($\kappa = 0.62$) — evidence that the signal layer is a sufficient basis for the interpretation layer above it. We reuse their stage-1 vocabulary and replace their stage 2.

---

### 3.1 Corpus

We annotate **ShareChat-Claude**, a corpus of conversations voluntarily published by users.

| Stage | Count |
|---|---|
| Raw message rows | 8,364 |
| Raw conversations | 911 |
| Non-English excluded (<50% English word content on either side) | 208 |
| **Annotation frame** | **703** |
| **Human-annotated (development set)** | **148** |
| Remaining, for the automated annotator | 555 |

Paragraphs per conversation: min 2, median 5, mean 12.1, max 294.

#### Why ShareChat rather than WildChat or LMSYS

ShareChat is not a convenience choice. It is, to our knowledge, the only public corpus of real human–AI interaction that exposes **model-internal blocks** alongside the visible exchange:

| Block type | Blocks (in 148) | Conversations (of 148) | % of 148 | % of all 703 |
|---|---|---|---|---|
| `human` | 689 | 148 | 100.0 | 100.0 |
| `ai` | 689 | 148 | 100.0 | 100.0 |
| `reasoning` (model-internal) | 171 | 59 | 39.9 | 38.0 |
| `code` (artifact) | 104 | 34 | 23.0 | 15.8 |
| `analysis` (tool output) | 55 | 32 | 21.6 | 20.5 |

This matters for a reason internal to our theory, developed in §3.3.1: when a human directs an agent, the human's only window onto the agent's state is the agent's own report, so an analyst reading only the visible exchange has no independent measurement either. The `reasoning`, `analysis` and `code` blocks supply what the user did not read but the analyst can — and without them, claims about divergence between an agent's internal state and its report cannot be grounded. WildChat and LMSYS are chat-only and offer no such channel; multi-agent trace corpora (Cemri et al., 2025) offer internals but contain no human controller.

**Limitation to state.** ShareChat conversations are self-selected for publication, which skews toward resolved threads. Direct evidence: `user_abandons_thread` carries $\kappa = 0.72$ in the source study — among its highest — yet appears in only 1 of our 148 conversations after an exhaustive screen of all 81 structurally eligible conversations (§3.2.3).

#### Sampling

All 703 conversations were imported into the annotation instrument in **randomized order** and annotated in sequence, so the annotated set is a **simple random sample** of $n = 148$ from the frame of 703. Randomization is verified rather than asserted: Spearman $\rho = -0.025$ between annotation order and corpus order.

Representativeness follows from the design. The sample proportion is an unbiased estimator of the corpus proportion for every signal, and the sampling variation is quantified by the intervals below; no balance adjustment or post-hoc weighting is applied, and none is warranted.

#### Sample size

Because a conversation may exhibit several coupling-error signals at once, the task is **multi-label binary annotation**, not assignment to mutually exclusive classes. For each signal $s$, a conversation is coded $Y_s = 1$ if the signal is present and $Y_s = 0$ otherwise. We therefore justify the sample **at the per-signal binary level**, where the relevant test is a one-sample proportion test — equivalently a goodness-of-fit $\chi^2$ on a single signal with $df = 1$.

At $\alpha = 0.05$ and $N = 148$:

| Cohen's $w$ | $\lambda = Nw^2$ | Power |
|---|---|---|
| 0.10 (small) | 1.48 | 22.9% |
| 0.20 | 5.92 | 68.2% |
| **0.266** | **10.47** | **90.0%** |
| 0.30 (medium) | 13.32 | **95.4%** |
| 0.50 (large) | 37.00 | **99.998%** |

$N = 148$ gives at least 90% power for $w \geq 0.266$ — that is, for medium effects by Cohen's convention ($w = 0.30$, power 95.4%) — and effectively certain detection at large effects ($w = 0.50$, power $> 99.99\%$). 80% power is reached at $w \geq 0.230$.

For a binary signal, Cohen's $w$ has a direct reading: $w = |p_1 - p_0| / \sqrt{p_0(1-p_0)}$, the prevalence deviation in units of the reference standard deviation. The detectable deviation at 90% power is therefore:

| Reference prevalence $p_0$ | detectable $|p_1 - p_0|$ |
|---|---|
| 0.05 | 0.058 |
| 0.10 | 0.080 |
| 0.15 | 0.095 |
| 0.25 | 0.115 |
| 0.50 | 0.133 |

The human annotation set is thus powered to detect **medium-to-large conversation-level prevalence deviations for individual signals**; rare signals and small effects are treated as exploratory and reported as such.

The same $N$ also fixes reporting precision. Wilson 95% interval half-widths at $n = 148$ are ±0.036 at $p = 0.05$, ±0.049 at 0.10, ±0.057 at 0.15, ±0.069 at 0.25, and ±0.080 at $p = 0.50$ — so no per-signal prevalence estimate is reported with a half-width wider than ±8 points. Reaching ±5 points would require $N = 381$, beyond feasible human annotation, which is what motivates the validated automated annotator of §3.2.5 rather than a larger human sample.

---

### 3.2 Stage 1 — behavioural signal annotation

**Figure 1: Stage 1.** From 911 published ShareChat-Claude conversations, 703 form the annotation frame after non-English exclusion. Randomized import order makes the 148 annotated conversations a simple random sample ($\rho = -0.025$). A single annotator develops the rubric over those 148 across five versions; every revision triggers a re-scan of all previously annotated conversations. Three annotators then code 10 conversations selected by greedy set-cover so that all 50 signals occur at least once, and the rubric is refined against their disagreements. Pairwise Cohen's $\kappa$ is reported per signal before and after refinement. The resulting gold labels validate an LLM annotator — accuracy, precision, recall, F1 and $\kappa$ — which is then applied to the remaining 555. The annotation unit throughout is the content block, with sentence spans as evidence.

#### 3.2.1 Signal inventory

We adopt the behavioural vocabulary of Potts & Sudhof (2026), which contains 65 signals across three layers, of which 63 carry published reliability estimates.

**Signals are filtered on reliability: we retain those with prior $\kappa \geq 0.4$.** Of the 63 estimated signals, 47 meet the threshold and 16 fall below it; all 16 are dropped, and the lowest retained value is 0.41, so the cut is clean rather than negotiated at the margin. One signal above the threshold, `intent_addressed` ($\kappa = 0.47$), is additionally excluded on conceptual rather than reliability grounds, with the supporting measurement reported in Appendix A. The two signals present in the source's released code but absent from its agreement table (`user_empowered`, `user_misled`) are carried as **unmeasured**, as are our two additions (`ai_missing_retrieval`, `ai_asks_followup`). This yields an active set of **50**: 46 inherited above threshold, 4 unmeasured. The prior estimates are **inter-*model* agreement** (Opus 4.6 vs GPT-5.4) rather than human inter-annotator agreement — the source's annotation is LLM-only — so we use them as a selection filter, not as a reliability claim we inherit; our own human agreement is measured in §3.2.4.

Reusing a published vocabulary is a deliberate methodological choice. It makes our reliability figures comparable to a prior baseline, and — because the vocabulary was designed for a *different* research question — it forecloses the objection that we defined our observables so as to produce the categories we wanted.

#### 3.2.2 Unit of annotation

**The annotation unit is the content block.** We use the term in its Messages-API sense: a turn carries a role, and its content decomposes into typed blocks. In an agentic conversation a single assistant turn routinely comprises several — a `thinking` block, one or more `tool_result` blocks, an emitted artifact, and the user-facing text — which is exactly the structure a turn-level unit cannot express. Our five block types map onto that vocabulary as `human` (user text), `ai` (assistant text), `reasoning` (thinking), `analysis` (tool result) and `code` (artifact).

| Level | What it is | Role here |
|---|---|---|
| Conversation | the full trajectory | unit of **prevalence reporting** (§3.1) |
| Turn | one role-bearing contribution | not annotated; may contain several blocks |
| **Content block** | one typed element of a turn | **the annotation unit** |
| Sentence span | a contiguous text range inside a block | the **evidence** for a label |

A label answers, for each signal $s$ and each block, whether $s$ is present, so annotation is multi-label binary at the block level. **Sentence spans are evidence, not units:** each label is anchored to the span that warrants it, which makes the decision auditable — a second annotator sees not only *that* a signal was assigned but *on what basis*, so disagreements trace to the text rather than to unstated impressions.

We avoid the term *step*, which in the agent literature denotes one iteration of a perceive–decide–act loop and therefore bundles several content blocks; our unit is finer than a step, not equal to one.

Placement rules constrain which signals may appear on which block type: user-behaviour signals on `human` blocks, outcome signals on `ai` blocks, conversation-level signals never on model-internal blocks.

The content block is finer than the unit used by Potts & Sudhof (2026) — "single AI response with full conversation context, plus the preceding user turn," which bundles a user turn and a response into one tagging event and exposes no internal blocks to separate — and far finer than the whole-trajectory unit of Cemri et al. (2025). The cost is that our agreement figures are **not numerically comparable** to either, and we report them as such.

Instrument: Label Studio v1.23.0 Community, self-hosted; the 50-signal configuration is released.

#### 3.2.3 Rubric development

Annotators are Ph.D. candidates who are domain experts, all co-authors or direct collaborators. No crowdsourcing.

**We adopt the predecessor's signal vocabulary, not its operationalization.** Definitions calibrated to agentic conversation, block-placement rules and boundary criteria were developed on our own corpus by iterated annotation, following the grounded-theory protocol of Cemri et al. (2025, §3). The result is released as two artifacts covering all 50 signals: an annotation guide, and a decision-step rubric in which a signal carries ordered gates with calibration examples and neighbour discriminators wherever annotation produced a boundary dispute (32 signals, 84.5% of placements). Development produced 18 signal decisions and 23 boundary rulings across five rubric versions, each recorded with the conversation that forced it.

#### 3.2.4 Inter-annotator agreement (IAA) study

Inter-annotator agreement (IAA) studies validate a rubric: when different annotators annotate the same cases under the same rubric, they should reach the same conclusions.

We sample 10 conversations (441 content blocks) from the 148 by **coverage sampling**, a greedy set-cover over the annotated corpus that selects the smallest set containing at least one instance of every signal, with a depth-preferring tie-break; every one of the 50 signals occurs at least once in the resulting set. Coverage sampling replaces random sampling here because signal prevalence varies widely and a random 10 conversations would leave roughly a third of the inventory with no instance to agree or disagree about.

The rubric entering this round was developed by a single annotator over the 148 conversations. **The round's purpose is to expose that rubric to annotators who did not build it and to adjust it where they diverge**, following Cemri et al. (2025): the three annotators annotate the 10 conversations independently, using the definitions, block-placement rules and decision steps of the rubric and without access to one another's labels; every disagreement is then recorded and traced to the decision step that produced it, the rubric revised. The fixed rubric is then used by the three annotators to annotate the 148 conversations serve as gold labels.

We report pairwise Cohen's $\kappa$ for all three annotator pairs per signal, together with the pairwise average and the pairwise minimum, both before and after refinement.

Before refinement the average Cohen's $\kappa$ is ___, with a pairwise minimum of ___; after refinement ___ and ___. Per-signal values are given in Appendix ___.

#### 3.2.5 Automated annotator and scale-up

The 148 human-annotated conversations serve as gold labels for validating an LLM annotator, which is then applied to the remaining 555. 

The annotator is evaluated against the gold labels on accuracy, precision, recall, F1 and $\kappa$, following Cemri et al. (2025, §3.4); it attains ___.

The two measurements answer different questions and are not interchangeable. $\kappa$ on the human set asks whether the *instrument* is reliable — two fallible raters, no ground truth. The precision/recall family on the automated set asks whether the *predictor* is valid against a fixed reference, where over- and under-firing are different problems.

---

### 3.3 Stage 2 — deriving coupling errors

Stage 1 yields *what was observably done*. Stage 2 asks *why each party's behaviour made sense to it at the time, and what property of the exchange let their understandings come apart and stay apart*. We answer it with a control-theoretic analysis grounded in STAMP (Leveson, 2004) and performed with **STPA** (Leveson & Thomas, 2018): the control structure is instantiated in §3.3.1, the hazards the analysis is run against are stated in §3.3.2, and our adaptations are declared in §3.3.3.

**Figure 2: Stage 2.** Hazards H1–H3 fix what the analysis is about. The control actions available to each controller are enumerated from the control structure and crossed with STPA's four unsafe types to identify **unsafe control actions** — an action unsafe in a given context; events on the feedback and execution paths are recorded in the same five-part form without being called unsafe control actions. Every event we report is *witnessed*: at least one paired turn in the corpus instantiates it, anchored to signal placements. **Loss scenarios** explain why the event occurred, and it is these, not the event statements, that the coupling-error types are abstracted from by open coding, iterating until the objective and subjective ending conditions of Nickerson et al. (2013) hold together. Validation applies the frozen codebook to unseen occurrences by a coder outside the derivation. Stage 2 is manual throughout.

#### 3.3.1 The control structure and what the theory supplies

STAMP models a system as a hierarchy of control loops. Effecting control requires four conditions (Leveson, 2004, §3.2, after Ashby): the controller must have a goal, must be able to affect the state of the system, "must be (or contain) a model of the system," and must be able to ascertain that state. That third condition is the **process model**, and "accidents, particularly system accidents, frequently result from inconsistencies between the model of the process used by the controllers (both human and automated) and the actual process state" (Leveson et al., 2003). Losses arise from **inadequate control**, not component failure.

The structure we analyse is the theory's own: Leveson (2004, Fig. 3) models a human supervisor controlling an automated controller, each holding a process model of what it controls. A human directing an LLM agent instantiates that figure, with no metaphorical stretching. Recent work carries the same move into AI explicitly, modelling components whose controller/controlled roles shift with context (Rismani et al., 2024).

Instantiating it maps the corpus's block types onto control-structure roles. The five block types resolve into **three functional groups**:

| Group | Blocks | Control-structure role |
|---|---|---|
| Human | `human` | the human controller's control actions, and their process model where expressed |
| Report | `ai` | the feedback channel to the human controller — curated, user-facing |
| Internal | `reasoning`, `analysis`, `code` | the controlled process and its instrumentation |

The third group is not homogeneous, and the distinction inside it carries the argument. `reasoning` is the agent's own account of its own operation — model-authored, and in this corpus a summary rather than the raw trace. `analysis` (tool return) and `code` (executable artifact) are different in kind: **machine-returned or independently checkable**, and therefore the only genuinely independent measurements of the process anywhere in the loop.

This yields the asymmetry we argue is the defining property of the human–AI case:

> An independent sensor does exist — tool returns and executable artifacts genuinely measure what the agent did. **But it terminates at the agent, not at the human.** Every channel through which the human can observe the process is authored by the process under control. The agent is its own instrumentation, and the one channel that is not is one the human does not read.

This structural fact predicts the phenomenon the prior literature observed but did not explain — that most AI failures leave no user reaction (Potts & Sudhof, 2026). It also makes the corpus requirement a consequence of the theory rather than a convenience: distinguishing "the agent reported incorrectly" from "no report could have existed" requires knowing what the agent held, which requires the internal group. The sharpest single case the corpus supports is a tool return in an `analysis` block that the adjacent `ai` block does not surface to the user — an independent sensor reading that reached the agent and stopped there.

#### 3.3.2 Hazards

STPA is run against **hazards** — "a system state or set of conditions that, together with a particular set of worst-case environmental conditions, will lead to a loss" (Leveson & Thomas, 2018). The hazards are supplied by the analyst rather than by the theory, and every downstream claim traces to them. Ours are states of the joint human–agent work, written to the handbook's own constraints: a hazard names a state rather than a cause, refers to the system rather than to its components, and specifies the condition instead of restating that it is unsafe.

The three are cut by **direction of coupling**, which is the taxonomy's top-level distinction, and the third is a property of the trajectory rather than of any one exchange.

| | Hazard | State | Assigned at |
|---|---|---|---|
| **H1** | human to agent | The agent proceeds on a task specification inconsistent with the human's current valid intent or constraint. | paired turn |
| **H2** | agent to human | The human's basis for supervising the agent misrepresents the agent's actual state, capability or output. | paired turn |
| **H3** | the loop | Each party's basis for acting is out of step with the other's, and each successive turn is conditioned on the other's divergence. | conversation |

H2 is invisible failure in control terms: the only channel that could correct the human's basis for supervision is authored by the process being supervised (§3.3.1).

**H3 exists because a coupling failure need not be one-directional.** A conversation can hold divergence in both directions at once, each sustaining the other, and neither H1 nor H2 alone describes that; it is the state the word *coupling* is doing work for. Because a loop cannot be constituted inside a single exchange, H3 is a **conversation-level** hazard while H1 and H2 are assigned per paired turn. A conversation in H3 therefore contains paired turns in H1 and in H2; this is not double counting, because the objects being classified are different — a trajectory and an exchange — and prevalence for H3 is reported over conversations and never placed in the same column as the other two.

H3 requires more than the co-presence of H1 and H2 in one conversation. It is admitted only when at least two exchanges alternate in direction *and* each divergence is traceable to the preceding turn's, so that the coupling is mutual rather than parallel. `[Rule proposed here; requires sign-off before coding.]`

Entering one of these states is what makes an occurrence a coupling error. What may follow from it — the human adopts an output that does not serve their goal, the task is not accomplished and the human does not learn this, effort accumulates without progress, an action takes effect that the exchange never authorized — is why the states matter, and is not a separate object we detect or report.

#### 3.3.3 Why STPA, and what we adapt

STPA proceeds in four steps: define the purpose of the analysis, model the control structure, identify **unsafe control actions**, and identify **loss scenarios** — the causal factors that produce them. Its constructs have been carried into AI systems in recent work, which found that unsafe-control-action identification "could be applied to AI systems with minimal modification," while the losses, the control structure and the loss scenarios required adaptation (Rismani et al., 2024).

We take the same position — adapt, not adopt — and declare four adaptations.

**Every reported event is witnessed.** STPA is generative: crossing each control action with the four unsafe types yields every variant the structure permits, including variants that never occur. We report only those instantiated in the corpus, each anchored to signal placements in at least one paired turn. This is the substantive departure from STPA as ordinarily practised, and it is deliberate: the contribution is a taxonomy of coupling errors that occur in real interaction, not an enumeration of those that could. We therefore claim observed coverage, not completeness, and word the claim that way throughout.

**Hazards without a loss list.** STPA links each hazard to a stakeholder loss, and what is to be prevented is usually physical. Whether a loss follows a hazard here depends on whether the human relies on the output, executes it, or checks it independently — conditions outside the transcript and not recoverable from a corpus of published conversations. We therefore analyse to the hazardous state and stop, establishing that an exchange entered a state that could produce a loss under credible downstream conditions rather than that a loss occurred. This is a stated boundary of the analysis, and §3.3.6 records the unobservable term explicitly instead of estimating it.

**Controller roles are fixed by block provenance, not fluid.** A control action is attributed to the human or the agent by which side produced the block, so role assignment is mechanical rather than a per-context judgment — the one place we do not follow the role fluidity that AI adaptations of STPA accommodate.

**The five-part statement is extended beyond the control path.** The handbook prescribes it for unsafe control actions; we use the same five semantic elements for feedback- and execution-path events, which the handbook treats as scenario material rather than as statements in their own right (§3.3.5).

#### 3.3.4 Unit and evidentiary base

Stage 2 works at three levels, and separating them is what keeps the analysis anchored.

| Level | What it is | Role in Stage 2 |
|---|---|---|
| Conversation | the full trajectory | **H3**; whether the divergence had consequences; repair and persistence |
| **Human–AI paired turn** | one human control action and the agent's response, including any `reasoning`, `analysis` or `code` blocks between them | **the occurrence of a coupling event**; H1 and H2 |
| Block · span | one typed element; a sentence range inside it | the Stage-1 placements, which are the evidence |

The paired turn is the unit because the object of study is a coupling: the control action and the response it produced must be in the same unit for the relationship between them to be visible at all. The internal blocks fall inside it, so an `analysis` return and the `ai` block that did or did not surface it are compared within one unit rather than across units.

The conversation level is not decorative, and it carries a hazard of its own. A paired turn cannot express that the user never found out, nor that each party's divergence was sustaining the other's — whether the divergence had consequences, whether repair ever came, how long it persisted, and whether the exchange closed into a loop are all properties of the trajectory. The event is located in the pair; H3 and what followed from the event are determined across the conversation. Error types under H3 are open-coded like the others, but their occurrences are trajectories rather than exchanges.

Signal placements are the evidence at both levels. An event is admitted only when the placements in its paired turn instantiate it, so every coupling error we report points at observable behaviour that a second annotator agreed was present, and the occurrence set is recoverable from the released labels.

**The incident is the counting unit.** One hazardous transition often admits more than one sufficient event statement (§3.3.5). Statements are therefore grouped into an **incident** — one transition, its evidence, and every statement that describes it — and prevalence is reported over incidents. Counting statements instead would make prevalence a function of how many formulations an analyst produced.

#### 3.3.5 Identifying coupling events

The control actions available to each controller are enumerated from the control structure. Each is then crossed with STPA's four unsafe types — the action is not provided when needed, is provided when it should not be, is provided too early, too late or out of order, or is stopped too soon or applied too long — and each resulting cell is tested against the corpus.

Two properties of this step matter for our design. It is **enumerative rather than symptom-triggered**: coverage comes from walking the control actions, not from waiting for a failure signal to appear, so conversations carrying no failure signal are examined on the same footing as those that do. And it enumerates control-action *types* rather than instances, so the analysis does not scale with corpus size; the corpus supplies contexts and evidence for a fixed grid.

**The hazards are fixed in advance; the hazard link is assigned per occurrence.** The set H1–H3 is declared before coding begins and is not revised against what the corpus turns out to contain, so a transition cannot be admitted by inventing a hazard that fits it. Within a single occurrence the order runs the other way: the coder reconstructs the event, writes the statement, and determines which hazard it created or maintained as the statement's fifth part. An occurrence that instantiates none of the three is recorded as such and reported with the residual (§3.3.7) rather than assigned to the nearest hazard.

**The statement form, and why it is the reason to use STPA here.** An unsafe control action is recorded in the handbook's five parts — source, unsafe type, control action, context, and the hazard it links to. Beyond conforming to the method, this fixed form does the work that makes an interpretive analysis auditable: two coders describing the same moment fill the same five slots, so a disagreement localizes to a slot rather than diffusing across two prose accounts, and agreement can be computed slot by slot (§3.3.7). It also bounds where interpretation enters. Everything up to the statement is description that a second coder can check against the transcript; exactly one later step — explaining why the event occurred (§3.3.6) — is interpretive, and we report how much agreement it attracts rather than asserting that it is objective. This is the substantive reason to run a safety-engineering method over conversation data, rather than its lineage.

These five parts are semantic requirements rather than a grammatical template: "UCAs are often written with each part in the same order shown above, but in some cases it may be clearer or more natural to use a different ordering. The ordering is not critical. The key point is that UCAs contain these five parts" (Leveson & Thomas, 2018). The type may be carried by the verb, and the context may hold one condition or a conjunction of them. For AI systems, unsafeness "frequently depends on sociotechnical context rather than on the technical timing or sequencing of a control action" (Rismani et al., 2024), which is why the context term is carried explicitly: the same action is safe or unsafe according to the state of the exchange when it is issued.

**The context is the true state, never a belief.** STPA requires that the context "specify the actual (true) state or condition that would make the control action unsafe, not a particular controller process model or belief (which may or may not be true)" (Leveson & Thomas, 2018). Two consequences are load-bearing in this corpus. First, an agent's context window supplies information to its process model but is not that model, and a transcript does not expose the model directly; a coder therefore records the observable inconsistency — that a subsequent output remains inconsistent with an active constraint — and not an inferred internal state. Second, an unstated human intention is not an observable context either, so a request whose hazard lies in what the human means by it is characterised through observable request properties, the capabilities it asks for, the authorization on record and the state of the environment. Explanation at the level of what a party held is admissible only at the loss-scenario step (§3.3.6), and is marked there as inference.

**Not every coupling event is an unsafe control action.** STPA distinguishes two kinds of scenario — why an unsafe control action occurs, and why a control action is "improperly executed or not executed" — and places inadequate feedback among the causes of the first. Coupling events accordingly fall on three paths. Control-path events are unsafe control actions. **Feedback-path** events concern what one party reported to the other; **execution-path** events concern what became of a control action that was issued adequately. The latter two are recorded in the same five elements but are not called unsafe control actions, because the four unsafe types are defined over control actions, and an adequately issued action is not made unsafe by what the receiving side did with it. Keeping the paths distinct is what allows a report and the state it reports on to be separated, which the internal blocks make observable here (§3.3.1).

**Alternative formulations of one incident.** A single transition frequently satisfies more than one unsafe type, since a required action not provided and an action provided out of order can describe the same moment. All sufficient statements are recorded, one as primary and the rest as alternatives, and the incident is counted once (§3.3.4). Where two genuinely different minimal contexts make the same action hazardous, they are distinct patterns rather than alternatives; contextual detail that does not bear on hazardousness is excluded from the context clause.

#### 3.3.6 From causal explanation to coupling errors

An event statement records *what* occurred and which hazard it created or maintained. STPA's next step asks *why* it occurred — its **loss scenarios**, "the causal factors that can lead to the unsafe control actions and to hazards" (Leveson & Thomas, 2018), which for us are explanations of how the two parties' understandings came apart — and it is at this level that our error types are formed. STPA's causal factors for an inadequate process model are the ones our data exercises: the controller receives incorrect feedback; receives correct feedback but interprets it incorrectly or ignores it; does not receive feedback when needed; or the necessary feedback does not exist at all. The fourth is the structural case the asymmetry of §3.3.1 predicts, and it is the one that cannot be repaired by either party inside the conversation. This is also the only step at which an explanation may refer to what a party held rather than to what the transcript shows, and such an explanation is marked as inference.

Stage 2 therefore produces four levels, and holding them apart is what keeps the taxonomy from collapsing into a relabelling of its own evidence:

| | Fixes | Declared or discovered |
|---|---|---|
| **Hazard** | which of H1–H3 the occurrence instantiates | declared before coding |
| **Path** | control, feedback or execution | read off the control structure |
| **Mechanism** | how the hazardous state was created or maintained | **discovered by open coding** |

An **error type is a cell in this cross-product**, not any one column. Only the mechanism dimension is derived from the data, and it is the one the contribution rests on; the other two can be assigned in advance and are what make an occurrence comparable across coders.

**Why the type cannot be the hazard, the statement or the incident.** A type must be more abstract than an occurrence, more specific than the criterion admitting occurrences, and always an error. The hazard fails the second — it *is* the admission test, so if it were also the type, nothing could pass the gate and fail to fit, the residual would be empty by construction, and the taxonomy could not turn out to be incomplete. The event statement fails the first: it carries an occurrence-specific context clause, so every occurrence yields a different statement. Stripping that context to obtain a repeatable class fails the third instead — an action such as clarification not being provided is not an error, only an error *in a context*, so what would have to be dropped to make it repeatable is exactly what made it an error. An incident is an occurrence with its evidence, hence an instance rather than a type. The mechanism is what remains: abstracted from occurrences, finer than the hazard, and instantiated only by occurrences already admitted.

The hazard establishes *why* an occurrence counts as a coupling error; the open code names *how*. A hazard is therefore a family: several distinct mechanisms can leave the agent proceeding on a specification inconsistent with the human's current constraint, and they are different error types. Hazards may be refined into sub-hazards to sharpen the admission decision, but only by state — refining them by cause would make them loss scenarios carrying a hazard's number, and no depth of state refinement reaches a mechanism, since two occurrences in the finest sub-state can still differ in how they arrived there.

**Context is recorded at three grains, of which only two are observable here.** The task domain; the interaction context that makes the action hazardous — repair phase, an unresolved specification, a correction on record, authority withdrawn; and the downstream conditions that would turn the hazard into a loss, namely whether the human relies on, executes or independently checks the output. The third is normally not recoverable from a published conversation and is recorded as unknown rather than estimated, which is the boundary declared in §3.3.3.

Coders work a single integrated pass in which theory-supplied and data-supplied fields are recorded together, following hybrid thematic analysis (Fereday & Muir-Cochrane, 2006) and directed content analysis (Hsieh & Shannon, 2005), which establish that a template of prior-theory categories may be applied while new categories are allowed to emerge where observations do not fit. The order is theirs as well: the template is developed *a priori*, the data are described before the template is applied to them, and additional coding happens in the same pass. The theory supplies the frame for the explanation; the categories within it are abstracted from the coded occurrences.

**The taxonomy's purpose is descriptive, and the types are formed empirically.** Taxonomy development alternates conceptual-to-empirical iterations, which derive categories from theory, with empirical-to-conceptual iterations, which abstract them from observed objects; a descriptive taxonomy weights the latter (Nickerson et al., 2013). Ours does. The theory supplies the hazards and the form of an event statement and is not revised against the corpus; every error type is abstracted from coded occurrences and must survive constant comparison against them.

**The known failure mode of this design is confirmation, and we say so.** Directed content analysis carries the standing risk that "researchers are more likely to find evidence that is supportive of the theory" (Hsieh & Shannon, 2005), restated independently as the "unintentional, unconscious 'seeing' of data that researchers expect to find" (Fereday & Muir-Cochrane, 2006). Three features of the design answer it, and none is optional: coders are blind to the directional prediction (§3.3.7); occurrences that fit no type are reported as a residual rather than absorbed into the nearest one; and an occurrence instantiating none of H1–H3 is recorded as such rather than assigned to the closest hazard (§3.3.5).

**Open coding sits above the frame, not inside it.** The **meta-characteristic** (Nickerson et al., 2013) — the single question every category in the taxonomy must be a logical consequence of — is: *what property of the exchange allowed this divergence to arise, or to go uncorrected?* For each occurrence the coder records that explanation, a concise open code naming it, constant comparison against previously coded occurrences, and a memo for every merge, split or renaming. Comparison runs from the inside out, as in Boeije (2002): within a conversation first — whether a later block corrected the divergence, whether an internal block contradicts the report — and only then across conversations. Every code carries the three parts Boyatzis (1998) requires of one: a label, a definition of what it concerns, and a description of how to know when it occurs. We hold the third to a stricter standard, requiring the structural features separating a code from its nearest neighbour to be stated in computable terms; a type whose discriminator cannot be stated that way is not yet a type.

**Coders do not consult the predecessor's archetypes while coding.** We inherit the signal vocabulary and nothing above it: the rubric is our own (§3.2.3), and the open coding runs against our own research question. The comparison against their eight archetypes is performed after the codebook is frozen and reported as positioning, not used as an input — which is what allows it to bear on whether our types are independently derived rather than inherited.

The inference from evidence to error type is **abductive** (Timmermans & Tavory, 2012): coders move between the observed trajectory and the control structure to select the most plausible explanation, and observations that resist the frame are recorded as such rather than forced. The residual — occurrences no code fits — is reported rather than eliminated.

Typing is **interpretive during derivation and mechanical at application**. A signal combination alone is a symptom pattern: `false_confidence` with no user reaction has one explanation when an `analysis` block held a contradicting tool return the response never surfaced, and a different one when no such return exists anywhere in the trajectory. What separates them lies in the block structure, not the signal set — the symptom/root-cause distinction Cemri et al. (2025) draw when they note that "different root causes may produce similar surface behaviors." Once the separating features are identified they are computable from the annotation, so the frozen mapping is defined over signal placements together with block-structure features and applies without further interpretation. The features are necessary rather than convenient: the 148 conversations yield 127 distinct signal combinations, 118 of them occurring once, so a mapping keyed on combinations alone would not generalize beyond the development set.

#### 3.3.7 Convergence and validation

Stage 2 is validated on stated terms, not on narrative plausibility:

1. **Calibration.** Three coders independently code a shared subset; disagreements are resolved by consensus, and revisions are logged with the occurrence that forced each one.
2. **Clustering and naming.** Recurring open codes are clustered into candidate error types; each type must be evidenced by occurrences from more than one conversation and must state its discriminator against its nearest neighbour.
3. **Ending conditions** follow Nickerson et al. (2013): objectively, every occurrence is assigned to at least one type, no type is empty, and no two types collapse; subjectively, the taxonomy is concise, robust, comprehensive, extendible and explanatory. Iteration stops only when all hold at once.
4. **Held-out validation, reported slot by slot.** The frozen codebook is applied by a coder who did not participate in its derivation, to occurrences not used in derivation; the frozen mapping is applied mechanically to the same occurrences from their annotation alone. Because the statement form fixes the fields, agreement is reported per field rather than as a single figure: $\kappa$ on **source**, **path**, **unsafe type** and **hazard**, which are categorical and admit chance correction; consensus-level agreement on the **assigned error type**, the one interpretive field; agreement between computed and coded type, which tests whether the structural features carry the distinctions the coding claimed; and the **residual rate** — the proportion of occurrences no type covers, with whether any new type emerged. We expect the interpretive field to agree less well than the four descriptive ones and report both rather than a pooled number, since a pooled figure would let the reliable fields conceal the field the contribution rests on.
5. **A theory-derived prediction, tested.** Because H2 has no independent sensor while H1 does — a wrong output is visible to the user, who knows their own goal, in a way a wrong internal state is not — the theory predicts that occurrences of H2 show **lower repair rates and longer persistence** than occurrences of H1, both measured at the conversation level. The prediction comes from the control structure, not from the data, and is falsifiable against the annotated corpus. Coders do not see it before coding.

Stage 2 is performed manually throughout. We do not apply an automated annotator to the interpretive layer: scoring it with a model invites the objection that the taxonomy is whatever a model says it is, and the mapping from evidence to error type *is* the contribution. Stage 1 is where scale is bought; Stage 2 is where judgment is exercised, and the two are validated differently by design.

---

### 3.4 Reproducibility

We release the signal inventory with decision steps, the full decision and ruling log with the conversation that forced each entry, the Stage-2 coding worksheet and frozen codebook, per-signal agreement figures, the annotator prompts and validation metrics, and conversation-level identifiers for the corpus.

Annotation was performed in Label Studio v1.23.0 Community. The Community edition provides neither overlap control nor annotator roles, so a single shared project would expose each annotator's labels to the others; the agreement round therefore ran as one project per annotator, each holding the identical 10 conversations imported in the same order, with the three label sets merged on conversation identifier rather than on instrument-internal task identifiers, which differ across imports. The two stages are released separately so the signal layer is reusable under a different interpretive frame — which is the use we ourselves made of the prior work, and which we tested by changing our own.
