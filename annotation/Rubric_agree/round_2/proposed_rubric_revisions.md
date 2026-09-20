# Proposed rubric revisions — for Michelle and Priya to review

Both agreement reviews are finished. Across the three of us, **43 disagreements
remain out of the ten conversations, and every single one falls under one of the four
questions below.** No block is unexamined, and none is waiting on anything other than
these four decisions.

> **Update, 2026-09-19 — after your replies.** You both agreed to all four. Questions 1,
> 3 and 4 are adopted and go into rubric v0.7. **Question 2 is held**, not adopted,
> although you agreed to it. Widening the `ai_structured_response` entry test is what
> makes `ai_provides_step_by_step` sit inside it, and that nesting is the span-prediction
> problem behind the separate decision to leave the two signals alone for now. Applying
> the widening would take the blocks carrying both from 4 to 24 in Jun's corpus, which
> multiplies the case that decision is about. Both halves wait until annotation is
> finished and the blocks can be counted.
>
> So the six differences under question 2 stay open: 757 b24/b26/b28, 757 b1/b30 and
> 764 b2. The other 37 close.

| question | differences |
|---|---|
| 1. merge `ai_asks_followup` + `ai_asked_probing_question` | 20 |
| 2. `ai_structured_response` Step 1 → marker **or** step-by-step actions | 6 |
| 3. merge `intent_missed` + `under_delivered` | 9 |
| 4. merge `user_expresses_frustration` + `user_expresses_dissatisfaction` | 8 |

Questions 1, 3 and 4 replace two signals with one. **Question 2 does not merge
anything** — it widens the entry test of one signal, and both signals stay in the
rubric with their own spans.

This document sets out those questions. Each section gives the problem, the evidence,
the proposed change, exactly which blocks it resolves, and Jun's position. You are being
asked to agree or object, not to pick from a neutral menu — but an objection with a
reason is worth more than assent, and two of these reverse rulings you were part of.

**Jun's position on all four, stated once so it doesn't have to be repeated:** adopt
the change — merge on 1, 3 and 4, widen the entry test on 2.
The reason leads with the pipeline, not the statistics. Stage 1's labels are training
and validation data for an automated annotator that has to predict *where* a signal
occurs, span by span (methods §3.2.5). Two signals that can sit on the same span, with
no rule that reliably separates them, are not something a span predictor can resolve —
it is being asked to make a distinction the annotation guide itself cannot make
consistently. Poor agreement is the symptom; unresolvable overlap is the defect.

**About the numbers below.** B and F are the two annotators from round 1. Every one is read from a recorded source — round-1
values from `roud_1/agreement-round1-report.md`, round-2 values from the committed
`agreement_round2_kappa.csv`. None were recomputed from the current database, which
holds post-reconciliation labels and would give a flattering and meaningless number.
"Blind" means before any disagreement was worked.

---

## 1. Merge `ai_asks_followup` and `ai_asked_probing_question`

**The problem.** The rubric routes a turn-closing question by grammatical form: a yes/no
action offer is `ai_asks_followup`, an open-ended invitation is
`ai_asked_probing_question`, and only one of them may be used per question. In practice the
three of us route the same sentences differently and consistently — Priya used
`ai_asked_probing_question` for every closing question and `ai_asks_followup` not once
in ten conversations.

**Evidence.**

| | round 1: Jun–B / Jun–F / B–F | round 2: Jun–Michelle | times used (round 1) |
|---|---|---|---|
| `ai_asks_followup` | 0.297 / 0.220 / **0.058** | 0.458 | 8 / 36 / 9 |
| `ai_asked_probing_question` | 0.847 / 0.133 / 0.184 | 0.777 | 44 / 51 / 7 |

`ai_asks_followup` is the weakest signal in the round-1 set for the pair who did not
write the rubric (B–F = 0.058). Both signals map to the identical taxonomy block —
`support_feature_AI2H`, no control operation — so nothing downstream distinguishes them.

This pair has been merged before. Decision 6 absorbed probing into followup as the
"exploration subtype", on the principled ground that the load-bearing test is "the AI
can proceed without the answer" and whether the reply is yes/no or open-ended is a
surface feature. Decision 8 reversed it, on the strength of a κ of 0.59 — but that
number is the predecessor study's **inter-model** agreement, not human agreement, and
should not have settled it.

**Proposal.** One signal for a turn-closing question the AI can proceed without.
`ai_asked_clarifying_question` (the AI needs the answer) and `ai_offered_options` (a
choice between named actions) stay separate — both carry a real control operation.

**Resolves 20 differences.** Eight blocks where Jun and Michelle have followup and Priya has
probing (759 b8/b13/b19/b22, 760 b7, 761 b35, 763 b14, 766 b1), plus 760 b67 and b101,
where Jun has probing and Michelle has followup.

**Michelle — this is the one that touches your open objection,** and it is now the only
block type still open on it. 760 b67 and b101 are the two blocks you disputed. A merge
removes the distinction those blocks turn on, so the question stops being which of you
read the sentence correctly. (Your third disputed block, 775 b2, is settled: the
`ai_asserts_knowledge_limit` Step 3 quotes that sentence as its own negative example.)

---

## 2. `ai_structured_response` Step 1 → visible marker **OR** clear step-by-step actions

> **HELD, 2026-09-19.** Not adopted, for the reason in the update at the top of this
> document. Step 1 stays markers-only in v0.7. The section below is the proposal as it
> was put to you, kept as the record of what was argued.

**This is not a merge.** `ai_provides_step_by_step` and `ai_structured_response` both
stay. What changes is the entry test of `ai_structured_response`, so that a procedure
written without surviving bullet glyphs counts as structured. It is a definition fix,
and it comes from an inconsistency inside the current rubric.

The definition and `block_notes` say the signal requires **visible formatting markers**
in the parsed plain_text. But Step 3's final sentence says "Short line-separated items
still count as a list when the export strips the bullet glyphs (C7 b1)." Those two
cannot both be applied. The strict reading was used when reviewing Priya's labels, and
36 of her fires were removed for lacking a visible marker.

Then the data made the contradiction unavoidable. In Jun's 148-conversation corpus,
`ai_provides_step_by_step` fires **24 times, and only 4 of those blocks also carry
`ai_structured_response`** — because the other 20 are procedures written without
surviving glyphs:

```
task  52 b4    Save the above code to ~/.config/fish/completions/rustywind.fish
               Make sure the file is executable: chmod +x …
               Restart your fish shell or run source …

task 108 b5    To use this code:  Save it as SudokuSolver.java
               Compile with javac SudokuSolver.java
               Run with java SudokuSolver
```

Those are structured. They are also exactly the shape removed from Priya's set. If a
step-by-step sequence is always a structured response — which it is, conceptually — then
the strict marker rule makes that entailment false in this corpus.

**Proposal (Jun's formulation).** Make Step 1 a disjunction: a visible formatting marker
**or** a clear sequence of step-by-step actions.

`ai_provides_step_by_step` then sits **inside** `ai_structured_response` rather than
beside it: wherever step-by-step fires, structured fires too, and the extra question
step-by-step answers is "is this structure a procedure the reader carries out?" Both
labels are still applied, on their own spans — structured covers the formatted passage,
step-by-step covers the procedure within it. In the four blocks of Jun's corpus that
already carry both, the two spans differ every time; at task 11 block 1 structured runs
221–1976 and step-by-step runs 633–1135, and at task 71 block 30 the two do not overlap
at all. So the change does not put two labels on one target. It closes the overlap
instead of leaving two signals competing for the same span.

**What it would change.** `ai_provides_step_by_step` fires on 24 blocks in Jun's
corpus and 4 of them already carry `ai_structured_response`, so **the other 20 gain
it**. Two of the 36 spans removed from Priya come back — 758 b14
("four logical stages: Initial setup and lentil soaking / leek preparation / Main
cooking / Finishing with the greens") and 758 b23 (the interleaved-prep workflow) —
because they are procedures. The other 34 stay out; ingredient lists, patch-note
summaries and colon-label prose are not procedures.

**The risk, stated plainly.** `ai_structured_response` was the worst signal in round 1
(Jun–B −0.006) and is now one of the best (Jun–Michelle **0.914**) — and what fixed it was exactly
the narrowing to visible markers. Loosening it again puts that at some risk. The
counter-argument is that the loosening here is narrow and testable ("does the reader
perform these in sequence?"), not a return to the colon-label-plus-prose cases whose
removal produced the 0.914.

**Resolves 6 differences.** 757 b24/b26/b28 (Priya has step-by-step, Jun and Michelle don't)
and 757 b1/b30, 764 b2 (they have it, she doesn't).

---

## 3. Merge `intent_missed` and `under_delivered`

**The problem.** The stated boundary is clear — a wrong goal for the whole response
versus the right goal delivered partially. Nobody applies it.

**Evidence.**

| | round 1: Jun–B / Jun–F / B–F | round 2: Jun–Michelle | times used (round 1) |
|---|---|---|---|
| `under_delivered` | **−0.003 / −0.003 / −0.002** | undefined — Michelle never used it | 2 / 1 / 1 |
| `intent_missed` | 0.666 / 0.666 / 1.0 | undefined | 2 / 1 / 1 |

`under_delivered` scored **zero agreement between every pair of round-1 annotators** — three raters
each used it once or twice and never on the same block. Usage is disjoint by person:
Michelle fired `under_delivered` 4 times and `intent_missed` never; Priya fired
`intent_missed` 5 times and `under_delivered` never. Across all five annotators and the
whole corpus the two have **zero co-occurrences**. Both map to the same taxonomy block
(`H2AI, act_execute, failure, coupling`).

**The case neither definition houses.** In task 763 the user asked for the tutorial
rewritten in clean LaTeX and said "avoid bulletpoints and lists". The AI produced the
document — right goal, full scope — with bullet lists throughout, worsening across four
revisions. That is a **violated constraint**. It is not a different goal, and it is not
less scope. It currently lands in `under_delivered` by convention, not by definition.

**Proposal.** One signal for a response that fails the request while attempting it,
with the violated-constraint case written into it explicitly.

**Resolves 9 differences.** 763 b1/b4/b7/b10 (Jun and Michelle `under_delivered`, Priya
`intent_missed`) and 758 b20.

---

## 4. Merge `user_expresses_frustration` and `user_expresses_dissatisfaction`

**The problem.** This one was already reopened during the Jun/Michelle review, and there
is a structural reason for it that was only found later: **`user_expresses_frustration`
has no entry in `sharechat_rubric.json` at all.** The file defines 48 signals and only
`user_expresses_dissatisfaction` is among them. Frustration exists in the Label Studio
config and as a single line in `signal_checklist.csv` — "Did the user express
frustration or strong negative emotion about the AI's response?" — and nowhere else.

So there are no decision steps, no calibration examples, and no boundary against its
neighbour. Annotators calibrated together in round 1 apply it consistently; those who
joined later do not.

**Evidence.**

| | round 1: Jun–B / Jun–F / B–F | round 2: Jun–Michelle |
|---|---|---|
| `user_expresses_frustration` | 0.932 / 0.192 / 0.357 | −0.004 |
| `user_expresses_dissatisfaction` | 0.397 / n/a / n/a (F never fired it) | −0.004 |

Identical control mapping for both: `H2AI, recover_repair, escalation, coupling`.

At the five held blocks, every rater reaches for a different member — at 758 b30 Jun has
`user_expresses_dissatisfaction`, Michelle has `user_expresses_frustration`, Priya has
neither.

**Proposal.** One signal, with a written entry: definition, decision steps, calibration
examples, and a boundary against `user_corrects_ai` (with which it is non-exclusive).
If the pair is kept instead, frustration must get a rubric entry either way — the
current state, where a signal is annotated with no definition, cannot stand.

**Resolves 9 differences.** 758 b30, 759 b14, 759 b23, 763 b12, 757 b13.

---

## What happens after you review

A merge, and equally a change to a signal's entry test, is a **rubric revision**, and under the annotation pipeline
(`docs/methodology/annotation-plan-mast-aligned.md`, following MAST, Cemri et al. 2025
§3.2) a revision has a fixed consequence: a new rubric version, **re-annotation of the
agreement conversations**, and κ measured on that round. A merged label is a new label,
so its reliability has to be measured, never estimated by collapsing the labels we
already have — those were made under the old distinction and tell us nothing about
whether the new one can be applied.

There is also a re-scan owed. Seven rubric changes made on 14 September during the
Jun/Michelle review have not yet been propagated to the other 138 annotated
conversations. Whatever is adopted here joins them, and **all of it discharges in one
re-scan rather than several** — which is the practical reason to settle these four
questions together rather than one at a time.

Full ledger in `docs/methodology/signal-decisions.md`, Decision 19.
