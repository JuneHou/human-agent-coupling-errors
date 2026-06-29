# Project decisions & methodology

Living record of decisions made while scoping the human–agent coupling-errors project.
Newest context at the top of each section. Dates are absolute.

## 1. Framing (settled 2026-05-30)

- Study **coupling errors**, not human/user error. Coupling errors emerge from the
  interaction loop across three axes: **Human → AI** (capture of goals/constraints/
  corrections/preferences), **AI → Human** (understanding of plan/rationale/state/
  uncertainty/consequences), **Shared control / repair** (clarification, explanation,
  confirmation, escalation, rollback).
- Core RQ: *what additional error types emerge when AI is embedded in a human interaction
  loop (with tool use / agent traces), not used as a standalone chatbot or autonomous agent?*

## 2. Relationship to the predecessor (settled 2026-05-30)

Predecessor = Potts & Sudhof, "Invisible Failures in Human–AI Interactions"
(arXiv:2603.15423; 100K WildChat chats; 79% of failures invisible; 8 failure archetypes).

Three separable things — we take the first two, not the third:

| From the predecessor | Take it? |
|---|---|
| **(a) Loop framing** — failures are loop properties; visible vs. invisible distinction | **Yes** |
| **(b) Method pipeline** — per-step signals → derived classifications → archetypes; LLM annotation + inter-annotator κ calibration | **Yes** |
| **(c) The ~50-signal taxonomy itself** — built bottom-up from features of a single chat message; no tool use, no action, no state | **No** — build our own |

Rationale for (c): their taxonomy is chat-shaped (tagging unit = "single AI response +
preceding user turn"). Bolting "action/state/consequence" signals onto it makes our work read
as an appendix to theirs. Our organizing principle is a *loop with stages where action and
state are first-class*. Where a coupling phenomenon genuinely coincides with one of their
signals (e.g. `silent_assumption`, `intent_missed`), we may reuse that single κ-tested
*operational definition* — borrow definitions, not the category skeleton.

> Caveat to budget for: many predecessor signals are tier-2 / low-κ (e.g.
> `generate_without_clarifying` κ=0.22 with extreme cross-model asymmetry). Adapting any
> definition means re-calibrating.

## 3. The taxonomy is an OUTPUT, not an input (settled 2026-05-30)

**The taxonomy is concluded empirically from the human data we collect — it is NOT drafted
top-down upfront.** The coupling-loop axes are the conceptual *lens* for reading the data, not
a pre-written list of categories. (This corrected an earlier "draft the taxonomy first, then
probe data against it" plan.)

## 4. Methodology / sequence (settled 2026-05-30)

Bottom-up and empirical:

1. **Explore existing data first** — WildChat and ShareChat, possibly τ-bench. Learn what
   coupling phenomena actually look like, and — crucially — what existing data *cannot*
   show. The deliverable of this phase is understanding that **informs how and what human
   data to collect**, not a results paper.
2. **Design the human-data collection** using what we learned (what loop conditions, tool
   use, and human signals existing data is missing).
3. **Collect** human-in-the-loop data (with real tool use / agent traces).
4. **Conclude the taxonomy** from the collected data.

### Why existing data can't just be used directly

Existing datasets give either the human side **or** the tool side, almost never both:

- **Human-in-loop, no tools** — WildChat (unsolicited/unfiltered; low selection bias),
  LMSYS-Chat-1M. Won't surface action/state coupling errors.
- **Tool use, no real human** — SWE-bench, WebArena, AgentBench, ToolBench. Autonomous; no
  human turns, so most coupling errors can't occur.
- **Both, but human is simulated (LLM)** — τ-bench / τ²-bench, MINT. Best loop proxy, but the
  "human" can't *genuinely* misunderstand, lose track of state, or abandon/repair
  authentically.

### Datasets in play for phase 1

- **WildChat** — predecessor's substrate; real users, chat only. Baseline for comparability.
- **ShareChat** (arXiv:2512.17843) — 142,808 convs / 660,293 turns from publicly shared URLs
  across ChatGPT/Perplexity/Grok/Gemini/Claude, 101 languages, Apr 2023–Oct 2025. Preserves
  **thinking traces** and citations.
  - *Upgrade vs. WildChat:* thinking traces expose AI internal state vs. what was surfaced →
    instruments the **AI → Human** axis; multi-platform enables cross-model comparison.
  - *Caveats:* (1) "tool use" is thin/inconsistent (Perplexity citations = retrieval; Claude
    analysis/code) — NOT a real tool-call→observation→state→action loop; (2) **post-hoc shared
    = serious selection bias** (people share impressive/funny/dramatic conversations), which
    likely distorts the visible/invisible failure ratio. Flag loudly if used.
- **τ-bench / τ²-bench** (maybe) — LLM-simulated user + tools + DB + ground-truth success.
  The one substrate with a full action loop, but the human is simulated.

## 5. Repo separation (settled 2026-05-30)

Built as a **new standalone repo**, NOT inside the predecessor's clone at
`/data/wang/junh/githubs/bigspin-invisible-failure-archetypes` — that directory's `origin` is
`github.com/bigspinai/...` (the predecessor team's published artifact repo). The predecessor
repo is treated as **read-only reference**.

## 6. Paper structure and role of WildChat work (settled 2026-06-22)

**There is one paper.** It follows the MAST-style model: a theory-derived taxonomy of
human-agent coupling failures, validated on real agentic traces, with an LLM tagger as the
reusable artifact.

**Structure of the paper:**

| Section role | Data / work | Status |
|---|---|---|
| **Motivation + preliminary results** | WildChat analysis: predecessor signal mapping, completeness grid, direction-span analysis | Done — shows the gap |
| **Primary contribution** | ShareChat agentic traces: direct signal annotation, taxonomy validation, LLM tagger | To be done |

**What the WildChat preliminary results demonstrate:**
- Predecessor's 65 signals map onto our 8-op × 2-direction taxonomy (methodology is compatible)
- In a chat-only substrate, 4 benchmark-gap cells are empty — substrate necessity, not data
  sparsity (those signals require tool calls, consequential actions, or tool errors to manifest)
- 4 structural-zero cells remain empty by definition (authority flows the wrong direction, or
  collapses into another op)
- Empirical gap: chat data cannot surface the failure types that matter most in agentic deployment

This is the motivation for why agentic annotation is needed, and it sets up the falsifiable
prediction the primary contribution tests: benchmark-gap cells fill on agentic data; structural-zero
cells stay empty.

**The paper is NOT an LLM evaluation benchmark.** No LLM is scored on a task. The tagger labels
coupling failures in any trace; the taxonomy and annotated agentic corpus are the contribution.

## 8. Annotation methodology (settled 2026-06-22)

Advisor-approved 4-step sequence (signal-first, then taxonomy):

1. **Read and observe** — researcher reads 50–100 ShareChat agentic turn-sequences without
   codebook; writes raw observation notes; identifies recurring phenomena
2. **Develop signal rubric** — reconcile observations against existing 42 signals; write
   definitions + 1–2 examples per signal; add any new agentic signals not in the current set
3. **Annotate signals** — human annotators apply the rubric to ShareChat agentic corpus;
   label at signal level ("this turn shows `false_confidence`"), NOT at taxonomy-cell level;
   compute inter-annotator κ on calibration batch; iterate on rubric until stable
4. **Conclude taxonomy** — map annotated signals → (op, direction) cells; validate or prune
   the 2×8 grid empirically; cells with zero signal support are dropped or reclassified;
   then train/prompt LLM tagger on the validated signal rubric

Key principle: signals are observable phenomena annotators can reliably identify; the
taxonomy mapping is a researcher-level interpretation step done after annotation. Annotators
do not need to know the control-op framework to label reliably.

## 9. Annotation tool: Label Studio (settled 2026-06-22)

Tool: **Label Studio** (open source, self-hosted — https://github.com/HumanSignal/label-studio)

Rationale over Doccano:
- `Paragraphs layout="dialogue"` renders each conversation turn as a separate visual row —
  native dialogue structure; annotators see the conversation as a conversation, not a text blob
- `ParagraphLabels choice="multiple"` supports multi-label per turn (one turn can exhibit
  multiple signals simultaneously)
- "When the error happens" is captured by paragraph index in the output — no manual step
  labeling needed; the structure does it automatically
- Can embed annotation guidelines panel directly in the labeling interface

Document unit: one conversation per task, formatted as a JSON array of turns:
```json
{"dialogue": [
  {"author": "human",  "text": "..."},
  {"author": "ai",     "text": "..."},
  {"author": "tool",   "text": "search_flights({...})"},
  {"author": "result", "text": "Found 3 flights: ..."}
]}
```

Output: JSONL with `paragraph_index → [signal_labels]` per annotator — paragraph index maps
back to turn position; "when" is answered without extra annotation work.

Inter-annotator κ: not built into the open-source tier; computed externally from exported
JSONL using Python (`sklearn.metrics.cohen_kappa_score` per signal).

## Open questions

- Exact Stage-A ShareChat slice to use for annotation (can the 278-turn set be expanded by
  relaxing the agentic filter? full Claude CSV has 8,364 rows)
- Whether τ-bench enters Phase 2 or is used only as a reference for Paper 2 design
- Conversation-level extension (frustration accumulation, `escalate_handoff`) — scope to
  Paper 2 or Paper 1 limitations section (flagged from collaborator input 2026-06-19)
