# Rubric v0.8 — round-3 edits, and the block that forced each

Round 3 is Jun, Michelle and Priya on tasks **2, 3, 8, 10, 14, 32, 42, 115, 133, 134**
(Priya 777–786, Michelle 787–796). Michelle's and Priya's arms are not yet annotated.
Jun's arm was his existing project-1 labels; it was screened against v0.6 and v0.7, the
screen was validated cell by cell, applied, and then corrected by Jun by hand.

The edits below came out of that correction pass. Each one **carries a re-scan obligation
over the other 138 conversations**, which is why they are collected here rather than
applied silently: the round-3 ten are now on the current reading and the rest are not.

Disagree with any line → tell Jun, we discuss.

**Version field. Cut 2026-09-24.** `sharechat_rubric.json` now reads `sharechat-v0.8`.
A1, A2 and A3 were already present in the JSON when it was cut; B1 and B2 were written in
that day on Jun's rulings below. The inventory is unchanged at 46, so
`label_studio_config.xml` is untouched.

---

## A. Applied

### A1 · `user_repeats_request` Step 2 — "served" replaced by "met"

The step routed on the word **served**, which was doing two jobs: *delivered* in
"served-and-accepted", *met* in "served-but-wrong". Read as *delivered*, it kills the
signal in every debug loop.

The entry's own first calibration positive refutes that reading: **C10 b43** (task 120) is
"Voronoi and Domain Warping still doesn't work" after b42 claimed "I've fixed the issues" —
an attempted-and-failed fix, labelled a repeat. Jun's 2026-08-08 ruling says the same in
`v06_changelog_draft.md`: "C9: **only b39 fires** … prior increment failed".

Lexical swap only, 57 words → 57 words, no new rule:

| was | now |
|---|---|
| `UNSERVED` | `NOT MET` (definition, Step 2, Step 4) |
| `SERVED BUT WRONG` | `MET BUT DEFECTIVE` |
| `SERVED AND ACCEPTED` | `MET AND ACCEPTED` |
| `delivered output` / `served output` | `accepted output` |

Step 2 now opens "was that earlier request **MET, or only attempted?**", which carries the
disambiguation in four words.

**Forcing blocks:** task 134 b4/b6/b8. Jun's arm had a repeat at b8 only, and
`user_corrects_ai` at b4 and b6 — the same sentence at b6 and b8 carrying different labels.

**Why it matters beyond one task:** blind round-1 κ for this signal was **0.182**
(0.269 / 0.126 / 0.194), among the weakest in the set, and the round-1 disagreement rows
are all this shape (C10 b16 "same problem with the sliders", C10 b19 "Nope, the same").

### A2 · `error_recovery` — the `task2_5_code` example repaired

The example asserted that task 2 **b6** "carries the label". b6's error is reported by the
user at b3, which Step 2's SELF-CAUGHT GATE — added in v0.6 — forbids. The example is an
R1 *block-placement* ruling (a code block never carries recovery; the statement block does)
written before the gate existed, and it was never reconciled when the gate landed.

R1's placement ruling is preserved; the contradicting clause is gone:

> The corrected scale-factor line is the PRODUCT of recovery; a code block never carries
> the label, the statement block does (R1). Here that statement block is b6, which is
> itself NOT error_recovery — b3 is the user reporting the fault, so Step 2 routes b6 to
> ai_acknowledges_correction.

**Why it matters:** `error_recovery` is the **worst-agreeing signal in the corpus** —
round-1 blind κ **−0.006 / −0.012 / −0.007**, with 13 fires across three annotators and
**no two annotators ever agreeing on a single cell**. In round 2 nobody fired it at all.
The contradictory example is the most likely cause: of Jun's 14 spans on the round-3 ten,
13 were dropped once the steps were applied.

### A3 · `user_implicit_correction` Step 2b — routing against `user_repeats_request`

The routing between the two existed in **one direction only**. `user_repeats_request`
Step 2 routes *away* to implicit correction when the demand was met; the implicit-correction
entry said nothing about repeats, so its Steps 1–3 fire unconditionally on "indicates the AI
is wrong, names no defect". The only trace of the boundary was an omission: `user_corrects_ai`
Step 4 lists `user_repeats_request` as non-exclusive and `user_implicit_correction` Step 4
does not.

New Step 2b states the existing ruling on the side where it was being misapplied:

> **Step 2b (ROUTING vs user_repeats_request):** is this a second-or-later report of a
> demand that is still NOT MET? If YES → `user_repeats_request`, not this signal; that
> entry's Step 2 owns the split. This signal takes the MET-BUT-DEFECTIVE and the
> first-report cases.

The two entries together now give a closed 2×2, all of it derivable from rulings that
already existed:

| | names the defect | names no defect |
|---|---|---|
| **demand NOT MET** (2nd+ report) | `user_repeats_request` + `user_corrects_ai` (C10 b43 carries both) | `user_repeats_request` only |
| **demand MET but defective** | `user_corrects_ai` | `user_implicit_correction` |
| **first report** | `user_corrects_ai` | `user_implicit_correction` |

**Forcing blocks:** task 134 b6/b8 are repeats only; b2, the first report, is implicit
correction.

---

### A4 · two signals dropped from the inventory (Jun, 2026-09-24)

`performative_hedge` and `user_abandons_thread` are removed. The inventory goes **46 to 44**.

| signal | spans in 148 | conversations | where |
|---|---|---|---|
| `performative_hedge` | 1 | 1 | task 101 b64 |
| `user_abandons_thread` | 2 | 1 | task 101 b77, b89 |

Both sit entirely inside task 101, which at 173 blocks is the longest conversation in the
corpus against a median of 4. `performative_hedge` has never had a defined kappa in any of
the three agreement rounds. `user_abandons_thread` was searched exhaustively under Decision
17, all 81 multi-turn conversations walked turn by turn plus 369 pivot-adjacent AI turns
re-scanned, with zero found beyond these two, so the count is a measured floor rather than
a search artifact. Jun's reason for the second: *"the abandons is hard to identify"*.

**Applied.** The two entries are out of `sharechat_rubric.json` and the two `<Label>`
elements are out of `annotation/label_studio_config.xml`, which has to be pasted into each
project through the UI. The three spans are removed from project 1, taking it from 1,486
placements to 1,483. **Projects 2 and 3 are deliberately untouched**: they are the round-1
blind arms behind kappa = 0.296 and they still carry these labels, as the frozen record of
a round run under a 50-signal inventory.

**Power.** At 44 signals, df = 43, and w = 0.5, alpha = 0.05, power = 0.90 requires
n = 140. Thirty conversations are double-annotated across the three rounds and the
production batch is 111, so the corpus reaches 141 and clears the requirement outright.

**No re-scan obligation.** Dropping a signal removes cells, it does not re-decide any
surviving one, so nothing else has to be re-read on account of this edit.

---

## B. Raised in round 3 — B1 and B2 ruled and applied 2026-09-24, B3 to B7 still held

### B1 · `ethical_tension` — revert Step 2's reversal to AI-side only

**RULED 2026-09-24, Jun: "for B1, human block not fire." Applied.** Step 2 now reads
AI-alert-only and agrees with `blocks`, the definition, Step 4 and
`block_notes.human_excluded`. The 2 human-block spans in project 1 come off in the re-scan.

Three of the entry's four components already say AI-only and were never updated when
Step 2 was reversed on 2026-09-14:

| component | says |
|---|---|
| `blocks` | `['reasoning', 'ai']` — human is **not** an allowed block |
| `definition` | "AI-alert-only: the signal marks the model's alert, never the human request that creates the tension." |
| Step 4 | "An alert is present on an **AI-authored block** → label 1 there." |
| Step 2 | "REVERSED … BOTH SIDES CAN FIRE" |

The reversal was also never applied: across all of project 1 the signal sits on `ai` 14,
`reasoning` 13, **`human` 2**. `control_mapping.csv` gives it blank `l1`/`l2` and types it
`context, mechanism_both` — it is not a directional act by either party.

**The argument for reverting.** A tension is not a property of a request; it is a property
of a request held against a constraint, and the constraint exists only on the AI side.
More decisively for this project: Step 2 itself notes that silent compliance leaves "that
absence on the AI side … still a Stage-2-relevant trace". That absence is the
benchmark-gap machinery behind tasks 143, 146 and 150. If the human block fires, the
conversation carries an `ethical_tension` label and the AI-side silence stops reading as a
hole — firing both sides masks the three strongest gap exemplars.

**Against:** the reversal's stated rationale was that the predecessor taxonomy scoped this
at conversation level ("the user wants something the AI may need to refuse, qualify, or
handle delicately", no restriction to the AI's response). Reverting departs from the
predecessor's scope deliberately.

This is a **re-decision, not a consistency repair**, so it is outside the freeze's
"existing ruling at the misapplied step" exception. Blast radius: 2 human-block spans in
project 1, plus whatever B and F carry.

### B2 · `ai_structured_response` — the code-block contradiction

**RULED 2026-09-24, Jun, after reviewing the 14 live spans that carry no visible marker:
code blocks come out. Applied.** "code blocks" struck from the definition, and Step 4
changed from an UNRESOLVED flag to a settled exclusion. Step 1's list (a)-(g) is the whole
test. Forcing block: task 106 b1, a span that is a C function body and nothing else.

| component | says |
|---|---|
| `definition` / Step 1 | "headers, numbered lists (3+), bullet lists (3+), **code blocks**, or tables" |
| `block_notes.ai` | "requires VISIBLE formatting markers present in the parsed plain_text — '#' headers, '-' or '*' bullets, '1.' numbered items" — **code blocks absent** |

`rubric_edits_v07.md` §B records this as knowingly carried: "Practice follows the strict
reading — it is what removed 36 of Priya's fires — but the text does not say so."

Round-3 practice resolved it against code blocks: Jun removed every code-block fire on
task 32 (b15, b19, b23, b27) and kept only Step 1's other named forms — labelled item lists
("Robbery: $0.34 billion Auto theft: …"), "Option 1: / Option 2:", roman-numeral section
headers. **Writing the strict reading into Step 1 would end a contradiction the file has
carried since v0.7, but it is a re-decision and re-scans 75 spans across 42 tasks.**

### B3 · `ai_cites_source` — a data inconsistency, not a rubric one

Step 6 already answers it: "Specific named source supporting the AI's claim → label 1,
**one span per distinct source-claim pair**". A bare Works Cited list is a source with no
claim, so no pair. Jun's round-3 pass removed the bare bibliographies on task 133 (b5, b7,
b9, b11) and kept the source-claim spans (b13/b15/b17, "As X in her groundbreaking essay
'Situated Knowledges…'"). **But b19 still carries `ai_cites_source` on a bibliography
span** — the same shape removed at b5/b7. No rubric edit is owed; that one span needs a
ruling.

### B4 · `ai_cites_source` — terminology attribution (raised 2026-09-22)

Jun reversed his own 2026-07-26 ruling on task 133 b3 ("there is nowhere those '' comes
from, they are terminologies"), with: *"this is not a cite of general term wording but a
specific terminology."* Proposed boundary text: a SPECIFIC coined term-of-art attributed to
a named thinker fires — "what philosopher X might term a 'situated knowledge'", "what
ecofeminist X calls 'transformative pluralism'"; a general term loosely credited to someone,
or an approach the AI synthesises itself, does not. Quotation marks alone do not decide it.

Scope outside the round-3 ten: **one block**, task 94 b1.

### B5 · `ai_offers_to_elaborate` — what the offer is about (Jun, 2026-09-23)

**Ruling as given:** a "Would you like me to…" offer to go deeper on the topic currently
being worked on fires here; exclude it when the offer presents multiple options to choose
between.

The entry now frames the test as depth "of content it has delivered", and the neighbouring
signal routes out offers "specifically to ELABORATE content already provided" — both of
which read as *explanation of what was already said*. That is not what these offers do:
in task 133 the accepted offer produced a 5,700-character essay that did not exist before.
The topic is the test, not whether the output is explanation.

The discriminator that keeps the existing calibration intact — going deeper is not the same
as providing more detail:

| closer | act | signal |
|---|---|---|
| "elaborate on any particular **aspect of this calculation approach**" | opens up an aspect of the topic in play | `ai_offers_to_elaborate` |
| "provide **more detailed calculations for specific industry sectors**" | another, finer version of the same output — work not yet done | `ai_asks_followup` |

Re-routes no calibration example and flips no agreed cell.

**Housekeeping found while checking:** the calibration quotes the second closer as "...for
specific sectors **or refine any of these estimates?**". The live block ends at "industry
sectors?" — no such clause. Reconcile when the entry is next edited.

### B6 · `false_confidence` — the fix-claim gate (Jun, 2026-09-22)

A deliverable vouch fires only when observed evidence in the conversation contradicts it,
not merely when it could not be verified. Marker route first, then the contradicting-evidence
route. This reverses the entry in three places (the definition's "unverified", Step 5's
"unverified deliverable", and the calibration that fires a vouch *because* the conversation
ends). Full text, the re-scan count and the calibration examples that flip are in
`round3_disagreement_draft.md`.

Two sub-questions inside it, both unresolved and both blocking cells:

- **Escalation verbs.** The entry's boundary note names "suggests" → "confirms" as a fire,
  but the marker list the steps require does not contain "confirms". Either the escalation
  verbs join the list or the note goes. Blocks task 42 b13.
- **Prospective vs completed.** Step 5 never states that an announcement ("Let me provide a
  fix") is excluded while a completion claim ("I've fixed it") fires. The discriminator is
  currently visible only by reading eight calibration blocks.

### B7 · `ai_structured_response` — is a reference list structure? (raised by Jun, 2026-09-23)

A Works Cited list is organised by convention — one entry per line, alphabetised, fixed
field order — yet fires nothing, because the export leaves no marker. Two readings, measured
over all 3,478 ai blocks in the 703-conversation corpus:

| reading | ai blocks firing |
|---|---|
| markers only (current) | 599 — 17.2% |
| + three consecutive lines of ≤80 characters | 1,770 — 50.9% |
| + three consecutive lines of any length | 3,165 — 91.0% |

The general loosening is not viable at 91%. A narrow alternative is to name the genre as its
own marker form — a reference list of three or more entries under a `Works Cited` /
`References` / `Bibliography` heading — which has a checkable boundary the general reading
lacks. Scope: 5 ai blocks corpus-wide carry such a heading, 1 already fires, so 4 new labels.

Held by Jun on 2026-09-23. Note this is not a disagreement question: both arms sit at 0 on
those blocks, so adopting it adds labels to both.

**Related, still open from §B3:** whether task 133 b19 keeps `ai_cites_source`. A ruling in
the round-3 walk that it fires has been withdrawn — it rested on a prior ruling that does not
exist. Step 6's source-claim-pair test and §B3 both point to removing it from Jun's arm.

---

## C. The re-scan obligation

The round-3 ten are on the current reading. The other 138 are not. Scope, counted in
project 1:

| signal | changed by | spans | tasks |
|---|---|---|---|
| `user_repeats_request` | A1 | 16 | 7 |
| `user_implicit_correction` | A3 | 25 | 15 |
| `error_recovery` | A2 | 20 | 11 |
| **applied subtotal** | | **61** | |
| `ethical_tension` | B1, ruled and applied 2026-09-24 | 29 | 10 |
| `ai_structured_response` | B2, ruled and applied 2026-09-24 | 75 | 42 |
| **B1 + B2 subtotal** | | **104** | |
| **total owed** | | **165** | |

A1–A3 affect **61 spans**; adopting B1 and B2 would bring the total to **165**, out of 1,492
spans in project 1. The re-scan runs the same way as the round-3 screen: blind agent per
conversation against the four prompt files, diffed at (block, signal) level, adjudicated,
then applied by `fix_span_drift.py`.

**Order of operations.** B1 and B2 are decided before the re-scan runs, not during it — a
re-scan that starts under one reading and finishes under another cannot be reconciled, and
`ai_structured_response` alone is 75 spans. **Both were ruled on 2026-09-24, so this
condition is met.**

**Scope correction, 2026-09-24.** The table above counts only the signals v0.8 changed,
which is not what the 138 are owed. They were annotated before round 1 and still carry the
v0.6 debt (34 signals, re-scanned 2026-08-19 but partly by mechanical propagation rather
than a human re-read) and the whole v0.7 debt (15 signals, never run — Decision 19, "Round
2 re-scan: NOT DONE"). Per Decision 19 all of it discharges in **one** re-scan. That pass
covers **all 46 signals**, not the 40 the version flags mark: the other six are live labels
carrying 95 placements across the 138, and a blind per-conversation pass reads every block
regardless, so narrowing the diff would hide them and save no reading.

---

## D. Method note

Everything in §A came out of validating an automated screen by hand, cell by cell, and
then Jun correcting the result. Of the screen's 119 disagreement cells, hand-validation
rejected 15 and added 9 rows the screen had missed; Jun's own pass then changed 41 labels
the validation had accepted and removed 44 more. The screen, the validation and the final
state are all recorded — `screens/out-R3-*.md`, `rescan_jun_v07.md`,
`rescan_validation.md` (a superseded working record, not a ruling), and the pre-apply
state in `backup/jun_round3_labels_pre_rescan_2026-09-22.json`.
