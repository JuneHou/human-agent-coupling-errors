# Derivation — how the taxonomy was built (method + decision trail)

Consolidates the method narrative and the audit trail (formerly `signal_coordinate_map.md` +
`coupling-lens-notes.md` method bits). The **mechanism layer** is kept separate in
`triggers_and_covariates.md`; the Phase-1 advisor checkpoint is `advisor-update.md`.

## Method — abductive-within-frame

Theory proposes the coordinates (deductive); data populates and revises the cells (abductive). Neither
impose-buckets-and-read-co-occurrence (pure A) nor pure bottom-up (pure B). The reliability table
(`src/predecessor_agreement.py`) gates reuse and surfaces the spine finding. The audit trail (the
codebook-evolution tables + this file) is what earns the "abductively recovered taxonomy" claim.

## Decision 1 — Layer-1: 3 → 2 categories; common ground becomes an ablation

The taxonomy must be **observable and annotated at the step level** (one unit = one AI response + its
preceding user turn, following the predecessor's per-turn tagging). H→AI and AI→H are local, per-turn
transfers — they qualify. **Common ground does not**: it only exists across the whole conversation, so
it cannot be tagged on a single turn. It is therefore **not a Layer-1 category** — it is the
**conversation-level ablation** over the two directions (under what conditions an H→AI failure and an
AI→H failure compound). This mirrors the predecessor, which pulled its only conversation-level signals
(`user_abandonment`, `goal_achieved`) out of the per-turn taxonomy into a separate transcript-level pass.

The arrow in H→AI / AI→H is **direction of transferred information, not blame**. Under the control lens
(Decision 3), common ground = **controller process-model divergence** (STAMP's "inadequate coordination
among controllers").

## Decision 2 — retire the four-channel scheme (provenance)

The first-draft lens used four channels: H→AI / AI→H / **Repair** / **Reaction** (still encoded in
`src/coupling_lens.py:MAP`, kept runnable for its join-validation). Two were wrong as top-level
coordinates:
- **Repair** is not a channel — it is a **grounding act** (Clark), bilateral (AI: `error_recovery`;
  human: `user_corrects_ai`). It moved to Layer-2.
- **Reaction** (human pushback) is not a coordinate — it is the deprecated **visibility** label, the
  very thing we reject as a failure definition (failure = positive divergence against an oracle). Kept
  only as a covariate for the predecessor comparison (W3).

The old "Option A vs B" bucketing fork is closed by the abductive-within-frame method above.

### The 7 judgment calls — dissolved, not voted on

`generate_without_clarifying` → failed Clarify / ask-clarify (uptake-vs-repair adjudicated by `thinking`,
W2); `under_delivered` → H→AI / `over_delivered` → dropped (κ 0.10); `problem_ignored` → AI→H Present /
report-state; `factual_error` → AI-only covariate (mechanism layer); `user_abandons_thread` → outcome
marker (invisible); `ai_provides_alternatives` → Repair-iff-mismatch; `off_topic_drift` /
`ai_refuses_or_declines` → Maintain failure / legible refrain.

## Decision 3 — Layer-2 is an open fork, resolved empirically (Clark vs control)

Two candidate Layer-2 schemes were applied to the real data rather than argued:
- **Communication lens** — Clark's 5 grounding acts (`../communication/`). Theoretical roots: Clark &
  Schaefer 1989 (contribution model: presentation/acceptance) + Clark & Brennan 1991; extended to joint
  action in Clark 1996.
- **Safety lens** — 8 control operations + UCA guidewords (`../safety/`). STPA supplies the
  **control-loop structure and the UCA guidewords directly**; the **8 operations are a documented
  per-operation adaptation** of that structure to a tool-using agent — derived in **Decision 3a** below,
  *not* lifted from a standard (STPA does not enumerate control-action types). Roots: Leveson's STAMP/STPA
  (an agent issuing tool calls under feedback is a controller; coupling failure = inadequate control;
  common ground = process-model divergence).

**Result (`../comparison.md`, `src/taxonomy_compare.py`):** Clark fits the communication channel (45
chat signals spread evenly, 0 empty acts) but places **0%** of 1,233 real tool calls — its action column
is empty by construction. Control covers the action channel (**100%** of tool calls; first-class
seek/act/confirm/stop cells) and its empty-on-chat cells (seek-inspect 0, confirm-authorize/stop-defer
near-empty) fill with agentic actions — quantifying that chat under-represents action coupling.

**Resolution: complementary, not winner-take-all.** Adopt **control operations as the primary backbone**
for the agentic benchmark (action-native, matches the agent-eval venue, gives a completeness story via
the UCA guidewords and a mechanistic invisibility argument: inadequate feedback → process-model
divergence → no reaction). **Retain Clark as the communication-channel sub-model** for the meaning
column (report-state / ask-clarify / recover-repair *meaning*), where it strictly dominates. The data
does not support flattening to the two directions alone (act/seek/confirm/stop carry distinct mass).

Honest caveat: the signal→cell mappings are author-assigned; the *direction* of the result follows from
the predecessor's signals being communication-era, but a handful of borderline placements affect exact
per-cell counts (documented in `../comparison.md`).

## Decision 3a — Theoretical derivation of the 8 control operations

Decision 3 keeps **control operations** as the primary backbone; this section makes their provenance
explicit, because the categories are **not** adopted from a standard. STPA deliberately does *not*
enumerate control-action types — it directs the analyst to identify the control actions specific to the
system under study [Leveson & Thomas 2018]. What we take **directly** from STPA/STAMP is the
**control-loop structure** and the **UCA guidewords**; the **8 operations are a documented domain
adaptation** of that structure to a tool-using LLM agent under human supervision, justified per operation.

**The control structure (taken directly — standards-supported).** STAMP models a system as a
*hierarchical control structure*: a higher controller issues **downward control/constraints**, a lower
controller returns **upward feedback**, each controller maintains a **process model** of what it
controls, and accidents are *inadequate control between levels* (feedback missing/late/incorrect upward,
command inadequate downward) [Leveson 2011; Leveson & Thomas 2018]. A human directing a tool-using agent
instantiates this as a **two-level control structure**: the **human is the higher controller**, the
**agent is the lower controller**. This fixes Layer-1 with no added assumptions — **H→AI = the downward
control channel** (does the agent take up the human's intent) and **AI→H = the upward feedback channel**
(is the agent's state legible upward). Norman's execution/evaluation gulfs [Norman 1986] name the same two
channels from the user's side and are cited as corroboration, not as the source.

**The operations (adaptation — justified per op).** An *adequate* lower controller must perform a fixed
set of functions across the loop's elements (sensor path · process model · control algorithm · actuator
path · upward feedback · loop correction). Instantiating each element for an LLM agent yields the 8
operations; each row states the STPA element **taken** and the adaptation **made**:

| Operation | STPA/STAMP element (taken) | Adaptation for an LLM agent (made) | UCA dimension exposed |
|---|---|---|---|
| **seek-inspect** | feedback / sensor path | acquisition is an *active control action* (agent must call a read tool), not passively received | feedback not-provided / stale |
| **maintain-state** | process model | model *updating across turns* from prior context + tool results | wrong / stale process model |
| **act-execute** | control-action (actuator) path | the control action is a tool call with target / parameters / sequence | wrong action; wrong timing/order |
| **confirm-authorize** | inter-level authority (lower seeks command from higher) | agent routes a go/no-go *upward* before a consequential act | action provided without authority |
| **stop-defer** | the control choice to **stop / not-provide** an action | unilateral halt / withhold / terminate / escalate under unresolved state; failure is a **termination error** — stop too soon, terminate wrongly, or fail to stop when unsafe — *independent of authorization* | stopped-too-soon / applied-too-long |
| **report-state** | upward feedback in the hierarchy | agent surfaces what it did / failed / is uncertain about to the human controller | feedback missing / incorrect (eval gulf) |
| **ask-clarify** | upward query (the higher controller holds the missing info) | acquisition whose *source is the human* — split from seek-inspect because the source sets the coupling direction | proceeding without required input |
| **recover-repair** | closed-loop correction after inadequate control | undo / retry / re-plan, incl. responding to a human correction from above | correction not-provided / inadequate |

**Where the originals come from (adaptation *of what list?*).** There is **no original list of 8** to
adopt — STPA provides none. The operations descend from STAMP/STPA's own *canonical* structures, and each
is independently corroborated by an established category list from an adjacent theory:

- **STAMP control-loop elements** (the structure the operations enumerate): *control algorithm · process
  model · actuator (control-action path) · sensor (feedback path) · downward command / upward feedback
  between levels · coordination among controllers* [Leveson 2011].
- **STPA's 4 UCA types** (the failure axis = the right-hand column): *not-provided · provided-unsafe ·
  wrong-timing/order · stopped-too-soon/applied-too-long* [Leveson & Thomas 2018].
- **STAMP control-flaw classes** (why control is inadequate): *flawed control algorithm · inconsistent/
  incomplete/incorrect process model · inadequate actuation · missing/delayed/incorrect feedback ·
  inadequate coordination among controllers.*

Mapping each operation back to the original category it descends from:

| Operation | Original STAMP loop element | Corroborating original list (theory) |
|---|---|---|
| **seek-inspect** | sensor / feedback path | info-acquisition stage [Parasuraman–Sheridan–Wickens 2000]; SA L1 perception [Endsley 1995] |
| **maintain-state** | process model | info-analysis stage [P-S-W 2000]; SA L2 comprehension [Endsley 1995] |
| **act-execute** | control action / actuator | action-implementation stage [P-S-W 2000] |
| **confirm-authorize** | inter-level authority (commands between levels) | decision/action-selection stage [P-S-W 2000]; supervisory control / levels of automation [Sheridan] |
| **stop-defer** | the "not-provide / stop" control choice (UCA types 1 & 4) | decision/action-selection stage [P-S-W 2000] |
| **report-state** | upward feedback in the hierarchy | gulf of evaluation [Norman 1986]; observability [Klein et al. 2004] |
| **ask-clarify** | upward query (human holds the info) | grounding [Clark 1996]; directability [Klein et al. 2004] |
| **recover-repair** | closed-loop correction / coordination | grounding repair [Clark & Brennan 1991] |

So the **theory** is Leveson's STAMP/STPA; the **original categories** are its control-loop elements + the
4 UCA types (not an operations list); and the **derivation** is ours — enumerate the control function
required at each loop element. The P-S-W stages, Endsley SA levels, and Clark/Klein joint-activity
requirements partition the *same* loop independently and converge on the same set, which is the
cross-theory support for "why these 8."

Two design choices a reviewer will probe — both **motivated by the phenomenon, not convenience**:

1. **Acquisition is split** into `seek-inspect` (source = system/tools) and `ask-clarify` (source =
   human), because the *source of the missing information* is exactly what sets the coupling direction —
   the distinction this paper is about. Endsley's SA Level-1 (perception) [Endsley 1995] and the
   information-acquisition stage of Parasuraman–Sheridan–Wickens [2000] corroborate acquisition as a
   first-class control function.
2. **`confirm-authorize` and `stop-defer` are kept separate**, not merged into one "gate": they are
   different STPA phenomena. `confirm-authorize` solicits a go/no-go *upward* (authority / coordination,
   expects a response); `stop-defer` is a *unilateral termination/withholding* whose failure mode is
   STPA's own stopped-too-soon / applied-too-long — a **termination error**, not a missing authorization.
   They also populate different cells in the agentic data.

The three *coordination* operations (`ask-clarify`, `report-state`, `recover-repair`) are **inter-level
acts in the STAMP hierarchy** — which is why single-controller intuitions overlook them; their *meaning*
is then carried by Clark's grounding sub-model [Clark 1996; Clark & Brennan 1991] (the complementarity of
Decision 3), and joint-activity requirements — mutual directability, observability [Klein et al. 2004] —
motivate why a human+agent *team* needs them as explicit operations.

**How the set was actually produced (three steps).**

1. **Deductive adaptation** — the table above: the STAMP control structure → candidate operations, each
   with a stated adaptation and citation.
2. **Abductive confirmation** — every operation is checked against real signals / tool calls; cells empty
   in chat are reported as *predictions*, not omissions (e.g. `seek-inspect` 0 chat signals / 897 agentic
   read-only calls; `../comparison.md`). Merges/splits are made **only** when the data forces them, and
   logged here.
3. **Reliability** — inter-coder κ (`src/predecessor_agreement.py`) shows independent annotators reproduce
   the categories — the evidence that the distinctions are *real and codeable*, not author artifacts. The
   remaining author-assigned placements are the target of the calibration round (task 13).

## Decision 3b — Why not adopt an existing AI control / safety taxonomy?

§3a *derives* the 8 operations rather than adopting them. This is deliberate, against two existing
strands — and neither can be adopted directly, for reasons of **kind, not quality**.

**Strand A — STPA applied to AI.** STPA *has* reached LLM systems: Mylius [2025] runs STPA on a
frontier-AI control scenario; Doshi et al. [2026] use STPA to derive information-flow safety specs for
MCP tool use; earlier work applies it to ML-powered systems and to ChatGPT-assisted analysis. But each
uses STPA as a **per-system hazard-analysis process**, outputting **system-specific UCA / loss lists for
one deployment**, with failure defined as **stakeholder-unacceptable losses** (top-down threat model),
produced manually, with no labelled corpus.

| | Strand A (STPA-for-AI) | Ours (CouplingBench) |
|---|---|---|
| Output unit | system-specific UCA / hazard list (one deployment) | reusable taxonomy of control *operations*, codeable on any transcript |
| Generality | single-system case study (re-run STPA per system) | cross-corpus, cross-agent |
| Failure definition | stakeholder-defined losses (hypothesized, top-down) | positive divergence vs ground-truth oracle (measured, bottom-up) |
| Interaction model | narrow (AI→human deception as *a* hazard) | bidirectional H→AI uptake / AI→H legibility as the spine |
| Data / reliability | qualitative analyst artifacts; no labels, no κ | annotated benchmark + inter-annotator κ |
| Process | manual expert STPA workshop per system | scalable turn-level coding (human / LLM judge) |

**Why it cannot be adopted directly (category mismatch).** STPA is a *method* whose products are
*instances* (this system's UCAs), not a *schema* (operations any transcript is coded against). Adopting
the outputs gives a non-transferable single-system hazard list; adopting the method still leaves the
operations to be invented — which is exactly §3a. The failure epistemics are also incompatible:
stakeholder-loss hazards (hypothesized) are not κ-codeable against real traces, whereas oracle-divergence
is. So Strand A **confirms the gap rather than filling it** — even the works that bring STPA to LLM agents
stop at per-system hazard analysis and never yield a reusable, bidirectional, oracle-grounded coupling
taxonomy.

**Strand B — agent failure-mode taxonomies** (MAST [Cemri et al. 2025]; Microsoft AI Red Team [2025];
trace-clustered fault taxonomies). These are **empirically clustered** from traces or red-team ops — flat
lists with no completeness guarantee (no UCA-style guidewords) — and they target the **agent's own faults**
(reasoning / tool / memory / orchestration) or **security risk**, not the **human↔agent coupling** against
an oracle. They are valuable *methodological* priors (MAST's seed-annotate → consolidate → scale-with-LLM
pattern is the workflow we reuse; `../reference/related_works.md` §4), but they are not a *control*
taxonomy and cannot supply the generative, bidirectional structure §3a needs.

**Net.** We take STPA's structural primitives (control loop + UCA guidewords + inadequate-control failure
stance) because they give the *generative completeness* Strand B lacks, and we derive the 8 operations
ourselves because Strand A shows no reusable AI coupling-operation taxonomy exists to adopt. Full
benchmark-level positioning against all lines of work: `../reference/related_works.md`.

### References

- Cemri, M., Pan, M. Z., Yang, S., Agrawal, L. A., Chopra, B., Tiwari, R., Keutzer, K., Parameswaran, A., Klein, D., Ramchandran, K., Zaharia, M., Gonzalez, J. E., & Stoica, I. (2025). Why Do Multi-Agent LLM Systems Fail? *arXiv:2503.13657.*
- Clark, H. H. (1996). *Using Language.* Cambridge University Press.
- Clark, H. H., & Brennan, S. E. (1991). Grounding in communication. In *Perspectives on Socially Shared Cognition* (pp. 127–149). APA.
- Doshi, A., Hong, Y., Xu, C., Kang, E., Kapravelos, A., & Kästner, C. (2026). Towards Verifiably Safe Tool Use for LLM Agents. *ICSE-NIER 2026.* arXiv:2601.08012.
- Endsley, M. R. (1995). Toward a theory of situation awareness in dynamic systems. *Human Factors*, 37(1), 32–64.
- Klein, G., Woods, D. D., Bradshaw, J. M., Hoffman, R. R., & Feltovich, P. J. (2004). Ten challenges for making automation a "team player" in joint human–agent activity. *IEEE Intelligent Systems*, 19(6), 91–95.
- Leveson, N. G. (2011). *Engineering a Safer World: Systems Thinking Applied to Safety.* MIT Press.
- Leveson, N. G., & Thomas, J. P. (2018). *STPA Handbook.* MIT.
- Microsoft AI Red Team (2025). *Taxonomy of Failure Modes in Agentic AI Systems* (v2.0 update 2026). Microsoft.
- Mylius, S. (2025). Systematic Hazard Analysis for Frontier AI using STPA. *arXiv:2506.01782.*
- Norman, D. A. (1986). Cognitive engineering. In D. A. Norman & S. W. Draper (Eds.), *User Centered System Design* (pp. 31–61). Lawrence Erlbaum.
- Parasuraman, R., Sheridan, T. B., & Wickens, C. D. (2000). A model for types and levels of human interaction with automation. *IEEE Transactions on Systems, Man, and Cybernetics – Part A*, 30(3), 286–297.
- Sheridan, T. B. (1992). *Telerobotics, Automation, and Human Supervisory Control.* MIT Press.

## The reliability spine (drives W2 and W4)

Reliability tracks surface-observability; the coupling-critical signals are the least reliable (κ:
`silent_assumption` 0.20, `generate_without_clarifying` 0.21, `problem_surfaced` 0.07,
`ai_self_contradiction` 0.10). You cannot read coupling failures off the transcript — the distinguishing
evidence is in the model's internal state. Hence W2 (use `thinking` as a reference) and W4 (log internal
plan + oracle). The predecessor has only LLM-vs-LLM κ; the benchmark must add LLM-vs-human κ. Numbers in
`../shared-findings.md`.
