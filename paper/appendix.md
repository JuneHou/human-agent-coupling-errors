# Appendix material

Detail supporting the methods section. Every number measured and re-runnable; sources named per section.

---

## A. Signal-merge justification — `intent_addressed` into `conversation_advanced`

**Claim for the paper.** The predecessor taxonomy's `intent_addressed` is retained as merged into `conversation_advanced` rather than carried as a separate signal. The merge is justified on evidence, not convenience.

### A.1 The two definitions are distinct

| | `conversation_advanced` | `intent_addressed` |
|---|---|---|
| Structural gate | GOAL PRESENT — user has an identifiable goal | **INTENT GAP** — "must be a gap between literal request and underlying intent. *If they're the same, just a correct answer.*" |
| Boundary test | PROGRESS — is the user closer to their goal? | INTENT INFERENCE — does the response show understanding of the goal *behind* the question? |
| Explicit non-example | social pleasantries | **"clear question gets direct answer"** |

Source: `taxonomy-tagging-code/taxonomy.json`. The definitions are separable in principle: a clear request correctly answered fires the first and is explicitly excluded from the second.

### A.2 In the predecessor corpus the two are near-coextensive

Predecessor annotations over WildChat (n = 10,000 conversations; `wildchat/data/wildchat-1m/derived/middle_step_10k_signals.csv`):

| Quantity | Value |
|---|---|
| `intent_addressed` prevalence | **84.8%** (8,479) |
| `conversation_advanced` prevalence | **86.0%** (8,600) |
| Both | 8,302 |
| `intent_addressed` **only** | 177 (**2.1%** of its fires) |
| `conversation_advanced` only | 298 |
| `intent_addressed` nested inside `conversation_advanced` | **97.9%** |

A strict INTENT GAP GATE cannot fire on 85% of conversations. The prevalence therefore indicates the annotator was applying "the AI fulfilled the request," not the gate — i.e. the construct had collapsed into its neighbour in practice. The two signals also carry near-identical agreement in the source study ($\kappa = 0.47$ for `intent_addressed`, 0.44 for `conversation_advanced`), which is what a collapsed distinction looks like: the merged signal is no harder to agree on than its neighbour.

### A.3 Applying the original gate strictly to our corpus

Exhaustive screen of **all 689 `ai` blocks** across the 148 human-annotated conversations, four independent annotator agents, each given the original definition verbatim plus a proposed operationalization to test and explicit permission to reject it.

| Result | Value |
|---|---|
| Fires | **14** blocks across 12 conversations (**8.1%** of conversations) |
| Borderline | 40 |
| Fires also carrying `conversation_advanced` | **12 / 14 (86%)** |
| Fires without it | 2 — **both artifacts**, see A.4 |

The strict gate produces markedly better separation than the source study achieved (8.1% vs 84.8% prevalence; 86% vs 97.9% nesting) — but the signal remains predominantly nested, and unresolved borderline cases outnumber clear fires.

**Caveat on the borderline count.** Agents were explicitly instructed to *"mark BORDERLINE liberally rather than forcing a call,"* because the borderline rate was itself a target measurement. The ratio is therefore **not comparable** to screens of other signals, where accept/reject was requested. It should be read as evidence that the gate is decidable at the extremes and mushy in the middle — consistent with three of four agents independently reporting that pattern — not as a calibrated disagreement rate.

### A.4 The two apparent decouplings are artifacts

Tasks 66 and 71 are 2 of only **7 conversations in 148 that carry no `conversation_advanced` label anywhere**. In 5 of those 7 the label was withheld because the content was judged misleading, wrong, or stalled:

| Task | Why no `conversation_advanced` |
|---|---|
| 66 | `user_misled` |
| 71 | `user_misled` + `false_confidence` |
| 24 | `factual_error` |
| 56, 115 | `conversation_stalled` |

So `intent_addressed` did not come apart from `conversation_advanced`; it fired in two conversations where annotators had deliberately withheld the progress label. Both are `user_misled`. Task 71 is the sharp case: the AI correctly inferred the underlying need (emergency triage rather than psychiatric prescribing) and its response was still flagged misleading.

**This exposes a defect in the construct as originally defined: it has no soundness condition and therefore credits well-targeted misinformation.** The same defect was found and repaired in `user_empowered`, which required an explicit soundness step (Decision 17). `intent_addressed` would require the equivalent before it could be used.

### A.5 Nesting alone is not disqualifying

Co-occurrence with `conversation_advanced` on the same block, among retained signals (n = 148 conversations, 1,996 placements):

| Signal | Blocks | % nested in `conversation_advanced` |
|---|---|---|
| `appropriate_confidence` | 14 | **100%** |
| `user_empowered` | 35 | 91% |
| `ai_provides_step_by_step` | 22 | 91% |
| `ai_provides_caveats` | 43 | 91% |
| `ai_cites_source` | 30 | 90% |
| `ai_validates_user` | 150 | 89% |
| *(`intent_addressed` would be)* | *14* | *86%* |

High nesting is the norm for signals that co-occur with progress, and is not by itself grounds for exclusion — `appropriate_confidence` is fully nested and is retained. The merge rests on A.2 and A.4, **not** on nesting.

### A.6 Conclusion as it should appear in the paper

> The predecessor taxonomy distinguishes `intent_addressed` from `conversation_advanced` by an intent-gap gate. In the predecessor corpus the two are 97.9% coextensive (84.8% vs 86.0% prevalence), consistent with the signal's reported inter-annotator κ of 0.05. Applying the original gate strictly to our corpus yields 8.1% prevalence with 86% still nested, borderline cases outnumbering clear fires, and — because the construct carries no soundness condition — fires on two responses independently annotated as misleading. We therefore retain the merge into `conversation_advanced`, and treat intent-inference failures through the negative pole (`intent_missed`), which is separately labeled.

**Correction to record in the decision log.** Decision 1's original rationale stated that `intent_addressed` was "essentially just `conversation_advanced`." That is accurate of *our drifted operationalization* and of the predecessor's labeling in practice, but not of the original definition, which is distinct. The rationale should be restated on the evidence above.

---

## B. Agreement-set selection — two decisions

The agreement round samples 10 of the 148 annotated conversations by greedy set-cover (Method §3.2.4). Two choices in that selection are worth recording.

**The pool is all 148, not a subset held back from rubric development.** The risk that matters for agreement is a *stale label* — one carrying an obsolete reading — not development history as such, and the re-scan practice removes it: every rubric change triggers re-annotation of all prior conversations, so all 148 are current-rubric. A conversation that once generated a boundary ruling is arguably a better agreement datapoint than one that did not, because it directly tests whether the resulting rule is written clearly enough for another annotator to reach the same label without the original deliberation. Restricting the pool to conversations annotated after the last rubric change would also cap coverage at 40 of 50 signals.

**Full coverage was chosen over a smaller set.** An alternative of 286 content blocks — dropping the single largest conversation — reaches 48 of 50 signals, losing `performative_hedge` and `user_abandons_thread` entirely. That conversation costs 155 blocks but is the only long-form relational/roleplay thread in the corpus, and that genre is 12.8% of conversations and **20.7% of the corpus by block volume**. Excluding it would bias the round away from a fifth of the data and leave two active signals permanently unmeasured.

---

## C. Screens of low-prevalence signals

Detail lives in `annotation/appropriate_confidence_screen.md` and `annotation/zero_instance_signals_screen.md`; summarized here for the appendix.

| Signal | Before | After | Coverage achieved |
|---|---|---|---|
| `appropriate_confidence` | 1/148 | 14/148 | domain-partitioned screen of all 148 |
| `ai_normalizes_difficulty` | 0 | 7 spans / 4 convs | all 689 `ai` blocks |
| `user_abandons_thread` | 0 | 2 / 1 conv | all 81 eligible convs + 369 untruncated pivot turns |
| `user_empowered` | 0 | 35 / 24 convs | all 689 human→ai pairs |

Each began because a signal's count was implausible given its prior reliability, and each required exhaustive rather than sampled coverage to distinguish *absence of the phenomenon* from *absence of a search*. Two recall gaps were found and closed mid-screen: a keyword prefilter covering 128 of 689 blocks, and an 800-character truncation that could have concealed unresolved threads. Both re-scans returned no new instances, converting an assumption about recall into a measurement.
