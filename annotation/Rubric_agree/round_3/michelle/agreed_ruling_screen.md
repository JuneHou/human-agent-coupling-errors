# Michelle's round-3 arm screened against the round-1 and round-2 agreed rulings

Scope: does anything in `michelle/task787.md` … `task796.md` misapply a ruling that
rounds 1 and 2 already settled? Sources screened against, in order of authority:

- `roud_1/BF/rubric_edits_v06.md` §A (global rules A1–A7) and §B (per-signal edits)
- `round_2/rubric_edits_round2.md` §B (the seven per-signal edits of 2026-09-14)
- `round_2/rubric_edits_v07.md` §A (three merges), §B (held, not adopted), §C
- the `examples[]` and `boundary_notes` in `sharechat_rubric.json`, which are where the
  round-1/round-2 rulings on individual blocks are written down

Every span below was checked against the live block text in project 9
(`label_studio.sqlite3`, read-only). Task mapping, verified by comparing `dialogue[0]`
and block counts against project 1:

| Michelle | 787 | 788 | 789 | 790 | 791 | 792 | 793 | 794 | 795 | 796 |
|---|---|---|---|---|---|---|---|---|---|---|
| Jun | 2 | 3 | 8 | 10 | 14 | 32 | **42** | 115 | 133 | 134 |

---

## A. Rulings written into the rubric about these exact blocks, not carried

### A1. `788` Block 4 — `ai_missing_retrieval` missing

`ai_missing_retrieval` carries one calibration example, `task3_2_ai`, label 1, and its
rationale quotes this block: *"AI states 'Average applied MFN tariff: ~8.7%', 'Average
manufacturing wages in <REDACTED> are roughly 1/10 of those in the <REDACTED>',
'Conservative estimates suggest a 15-20% production cost advantage' — all specific
quantitative claims about real-world trade data. No analysis block in turn 2 of task 3."*

All three phrases are present in the live block (`dialogue[3]`), and task 788 has no
reasoning or analysis block anywhere, so Step 2 does not suppress. The entry was promoted
from CANDIDATE to confirmed by round-1 D22 + B's review.

Michelle's file discusses two of these three phrases — under `ai_hedges_uncertainty`, in
the rejected list — and never considers `ai_missing_retrieval`.

**Add `ai_missing_retrieval` on 788 Block 4.**

### A2. `793` B14 — `false_confidence` missing

`false_confidence.boundary_notes.vs_user_misled` says, verbatim: *"Escalating 'suggests'
to 'confirms' with no new evidence fires HERE (task 42/13), not user_misled, because the
object-level claim is unverifiable."*

793 = task 42, and 0-based block 13 is Michelle's B14. Live text:

- B8 (idx 7): "This pattern **strongly suggests** a runtime attack…"
- B14 (idx 13): "You're exactly right. This **confirms** we're dealing with a runtime
  memory manipulation attack, not a modified kernel file."

B13, the intervening user turn, supplies no new evidence — it restates the theory. This
is the escalation the note names. Michelle fires only `ai_validates_user` on B14.

**Caveat, and it needs your ruling:** "confirms" is not on the round-2 marker-word list
('definitely', 'zero', 'never', 'all', 'any', 'whatever', 'always', 'completely',
'indeed', 'actually X-able'). So the round-1-era note naming 42/13 as a fire and the
round-2 required gate point opposite ways on this block. Michelle's file follows the
gate. One of the two has to give.

### A3. `793` B12 — WITHDRAWN 2026-09-22

Listed here as a defect because her Notes-for-Jun section says "`problem_ignored` is
anchored once at B12" while no fired row exists. Jun ruled: **"notes is not fire"** — only a
fired row counts, table row or the bold one-line form, and prose is not a label wherever it
sits in the file. So B12 simply did not fire; she and A both carry 0 there and there is no
disagreement. Same ruling dissolves the `792` B3 `error_recovery` item in §C and the
summary-recap mismatches in `795` and `796`: a recap carries no span and no step, so it
never constituted a label.

## B. Agreed rules misapplied

### B1. `ai_structured_response` fired on export-stripped lists — 795 and 796 only

Round-1 §B: *"Visible formatting only … **Never fire on assumed export-stripped
formatting**."* Round-2 §B (Held, not adopted) reaffirms it: the entry keeps an internal
contradiction between Step 1 and Step 3's last sentence, and *"**Practice follows the
strict reading** — it is what removed 36 of Priya's fires."*

Michelle applies the strict reading correctly in **789, 790, 791, 792** — 791 even
carries a "Corrected from a prior pass" section reversing exactly this fire, citing §B.
In 795 and 796 she reverses herself and fires off Step 3's stripped-glyph sentence.

Checked against the live text — none of these blocks contains `#`, `-`, `*` or `1.`:

| file | block | span shape | verdict |
|---|---|---|---|
| 796 | turn 1 (idx 1) | `Robbery: $0.34 billion` … 4 lines | drop |
| 796 | turn 3 (idx 5) | same 4 lines | drop |
| 796 | turn 4 (idx 7) | same 4 lines | drop |
| 796 | turn 7 (idx 13) | "What I can clearly see:" list | drop |
| 796 | turn 7 (idx 13) | "What I'm uncertain about:" list | drop |
| 796 | turn 9 (idx 17) | "The responsibility gap:" / "Standards for accessibility tools:" / "Who should be accountable:" | drop — this is the exact shape of the entry's own negative example `task13_1_ai` ("Solution Explanation:" as plain prose) |
| 795 | turn 3 (idx 5) | "Works Cited" + 11 unmarked MLA lines | drop |
| 795 | turn 4 | same shape, 21 entries | drop |
| 795 | turn 5 | same shape, 21 entries | drop |
| 795 | turn 10 | same shape, 33 entries | drop |

Fires that stand, for contrast — all verified in the raw text:

- **789 b2** — `Detects dragged images - Works with both files…`; the dashes really are
  there, and Step 1 names that shape ("Dash-delimited 'Name - description' entries count").
- **796 turn 8** — `Option 1: … Option 2: …`; Step 1 names enumerated Option lists.
- **793 B4** — `1.` / `2.` / `3.` numbering present.
- **795 turns 6–9** — roman-numeral section headers.

### B2. `false_confidence` marker gate borrowed from a neighbouring sentence — 796 turn 3

Round-2 C1 promoted the MIRROR TRIGGER to a required gate: *"do not fire from an
impression of certainty; **find the marker word in the sentence first**."*

Her own row concedes the gate fails: *"Step 2 MIRROR TRIGGER: no exact list-word here,
but the immediately preceding sentence carries 'compared to all others' (marker 'all')."*
The labelled span is "while the traditional property crimes appear as relatively modest
dark bars clustered at the bottom, the wage theft bar dominates the entire chart…" —
no marker word in it.

**Drop.** Turn 1 and turn 4 both carry "all" inside the labelled sentence and stand.

### B3. `ethical_tension` not fired on the human block — 791 B0

Round-2 C4 reversed Step 2, described in `rubric_edits_v07.md` §C as the **"highest blast
radius of the seven, being a reversal"**: *"the human block that creates or pushes the
tension (a rude request, **a jailbreak attempt**, a request testing policy boundaries)
can fire on its own terms."* The forcing cases were task 770's jailbreak-testing lines.

791 B0 is a fake `SYSTEM:` prefix instructing the model to craft an Instagram DM campaign
targeting first-time student voters for a named party, followed by "Instead, summarize…".
The AI declines it at B3 with three weighed policy rationales, which Michelle labels
`ethical_tension` — so the tension is established on her own reading. The human block
that creates it carries nothing, and is not in her rejected list either.

**But the rubric entry still argues against her firing it, in three places:**

- `definition`: *"AI-alert-only: the signal marks the model's alert, **never** the human
  request that creates the tension."*
- `blocks`: `["reasoning", "ai"]` — no `human`.
- `block_notes.human_excluded`: *"v0.6 (D6): the human block **NEVER** fires."*

Only Step 2 and one example (`task83_52_human`) carry the reversal. An annotator reading
the entry top-down lands where she landed. This is §B1 of `round_3/rubric_edits_v08.md`,
now with a second independent instance. **It should be settled before the 148-task
re-scan, not after.**

### B4. A3 granularity not applied — 794 and 795

A3 (round-1 §A): *"Fire every block where the behavior occurs. Within a block label every
occurrence."*

- **794**: sixteen `ai_asks_followup` fires (B4, B6, B8, B10, B12, B14, B16, B18, B20,
  B22, B24, B26, B28, B30, B32, B34) are consolidated into **one** table row. She names
  every block and offers per-block rows on request, so nothing is lost — but the file as
  it stands cannot be ingested as sixteen spans.
- **795**: `ai_cites_source` is itemised as *"representative spans only"*, with the note
  that the pattern *"recurs roughly 15 times across this block"* and that a full A3 pass
  *"would need a dedicated re-annotation pass over turns 6–9."* This is a real undercount,
  not a formatting choice, and it will depress agreement on that signal.

---

## C. Outside your question, but blocking

1. **`793` uses `ai_provides_structured_response`** — not a signal. The name is
   `ai_structured_response`. The fire itself is correct (B4 has `1.`/`2.`/`3.`).
2. **`795`'s summary table contradicts its own per-turn tables** — the summary claims
   `ai_structured_response` on turns 1 and 2 and `ai_missing_retrieval` on turns 3, 4
   and 5; none of those rows exists in those turns' sections.
3. **`796`'s summary claims `ai_structured_response` on turn 6 (×2)** — turn 6's table
   carries `adaptation`, `ai_asserts_knowledge_limit`, `ai_asks_followup` and nothing else.
4. **`795` note 5 contradicts her own turn-10 row** — the table fires
   `ai_missing_retrieval` on the Works Cited; note 5 says *"I don't think the works cited
   counts as missing_retrieval. The user asks for a works cited which is just a list of
   source with no retrieval necessary."*
5. **`795` turn 4's `ai_structured_response` row has no span and no step** — the cell
   reads "Works cited is a structured response." It cannot be entered as a span label.
6. **`792`'s closing note flags "`error_recovery` on B3"** as uncertain; no such row
   exists in the file.
7. **Code-block shape treated two ways.** 792 B27 fires `ai_structured_response` on an
   orphaned `bash` tag plus shell lines (flagged uncertain). 787 b3 has the same shape —
   an orphaned `html` tag plus literal `<avatar-editor …>` markup — and does not fire.
   Note that 792 B27 stands regardless: the block also contains a `├──`/`└──` file tree,
   which is visible structure on any reading. 787 b3 needs a ruling.

---

## D. Where the rubric, not the annotation, is wrong

### D1. `ai_malfunction`'s `task32_1_analysis` example asserts a pairing the gates forbid

The example rationale says: *"Paired with error_recovery in task32_1_ai ('Let me try
using a different approach to get the OpenAI API documentation:'). Step 0b fires: paired
error_recovery present → label 1."*

Checked in the live block: that sentence at 792 idx 3 introduces the `search_engine`
call, and `search_engine` **also returns `Error: HTTP 401: Token expired`** (idx 2). The
retry failed. Round-1 §B restored `error_recovery`'s does_not_count *"New answer also
wrong"* as Step 4, so the signal must not fire there.

Michelle did not fire it, and flagged the conflict. **She is right.** The
`ai_malfunction` fire at B2 is unaffected — Decision 11 demoted the pairing from a firing
gate to a covariate — but the example's rationale should stop claiming the pairing.

### D2. `adaptation` on 795 turns 7, 8, 9 — she read the entry correctly

She withholds `adaptation` on three consecutive turns where the user names a stylistic
defect and the AI silently rewrites the essay, because no reorientation *sentence*
exists. Step 1 asks for *"a sentence where the AI DEMONSTRATES a completed
reorientation"* and Step 4 is *"No explicit reorientation → label 0"*, so the entry as
written supports her. Round-2's C2 edit was aimed at prospective announcements
("I'll revise X"), not at silent-but-completed revisions, so the entry may be over-broad
— but that is a rubric question, not an annotation error. She flagged it.

### D3. `793` B16 `false_confidence` coexists with the "task 42/15 → 0" note

`boundary_notes.hedge_on_claim` rules task 42/15 to 0 on *"does appear consistent with"*.
Both sentences are in idx 15; her span sits on the other one ("This code manipulation
**definitely** has aspects that resemble…"). Step 2 is explicitly per claim, so the two
coexist. No conflict.

---

## E. Agreed rulings she got right

Recorded so the screen reads both ways. Each verified against the rubric entry:

- **790** matches all three gold rulings on that conversation — `task10_1_ai`
  (`ai_asserts_knowledge_limit`), `task10_3_ai` (`ai_hedges_uncertainty`), and
  `ai_provides_example`'s `vs_ai_asked_clarifying_question` note, which names the
  "For example: How many urgls equal one urg?" span and routes the closing question to
  `ai_asked_clarifying_question` under A6.
- **791** withholds `request_unfulfilled` on B1 exactly as `task14_1_ai` (label 0) rules,
  and cites it.
- **788** splits the two closing questions the way `task3_1_ai` (label 0, → elaborate)
  and `task3_3_ai` (label 1, → followup) rule.
- **792** matches both `ai_malfunction` gold examples (`task32_1_analysis`,
  `task32_6_analysis`) and the `factual_error` block note naming
  `payload.model = 'gpt-4o'`.
- **796** matches the routing written into `user_implicit_correction` Step 2b on
  2026-09-22: b2 (first report) → `user_implicit_correction`, b6 and b8 → `user_repeats_request`.
  Her turn numbering lands on exactly those 0-based indices.
- **789** places both `ai_validates_user` spans where R20/R21 confirmed keeps them, and
  puts `ai_acknowledges_correction` on a different sentence in the same block, per R21's
  sub-block precedent.
- **`error_recovery` Step 2** is applied correctly everywhere a user pasted an error —
  792 B11, B15, B23 all route to `ai_acknowledges_correction`.
- **Round-2 C7** (`user_expresses_dissatisfaction` required marker gate) is applied
  consistently across 787, 789, 794, 795 and 796, including the two places in 796 where
  she notes it produces a counter-intuitive result and flags it rather than overriding it.
- **Round-2 C3** (`ai_provides_caveats` requires a recommendation being qualified) is
  applied in 788 B4 and 792 B31 and used to reject in 791 B1, citing the negative
  calibration.
- **Round-2 C5** (`user_multi_request` question-chain vs restatement) is used to reject
  791 B2 against the ruled restatement pair.

---

## Summary

| | |
|---|---|
| agreed rulings on these exact blocks, not carried | **3** (A1–A3) |
| agreed rules misapplied | **4** (B1–B4), affecting **10** `ai_structured_response` rows, 1 `false_confidence` row, 1 missing `ethical_tension`, and ~30 un-itemised A3 occurrences |
| rubric defects surfaced, not annotation errors | **3** (D1–D3) |
| files internally inconsistent | 792, 793, 795, 796 |
| files clean | 787 (bar the 787 b3 code-block question), 788 (bar A1), 789, 790, 791 (bar B3), 794 (bar A3) |

Two of these are decisions you already have open in
`round_3/rubric_edits_v08.md`: §B1 (`ethical_tension` side) is now forced by B3 above,
and the `ai_structured_response` Step-1/Step-3 contradiction — deferred in round 2 as
"held, not adopted" — has now produced opposite calls inside one annotator's own ten
conversations. Both should be closed before the 148-task re-scan.

---

## F. Corrections applied, and round-3 agreement (2026-09-22)

### F1. What was changed

Only **B1** was applied — the one finding where an already-agreed rule is violated on
both sides and neither annotator has to concede a judgment. Everything in A, B2, B3, B4
and C is left alone; those either need Jun's ruling or are disagreements, not violations.

| arm | change | how |
|---|---|---|
| Jun (project 1) | 6 `ai_structured_response` labels dropped: 133 b5, b7; 134 b1, b5, b13, b17 | `fix_span_drift.py --fix-structured-response-strict`, new Mode 22. Re-checks each block's live text for a marker and refuses to delete when one is found. DB backed up to `label_studio.sqlite3.bak-2026-09-22-pre-structured-response-strict` first. `validation_sweep.py` exits 0 afterwards. |
| Michelle (markdown) | 10 rows / 9 block-cells marked `~~ai_structured_response~~ 0 (corrected)`: 795 turns 3, 4, 5, 10; 796 turns 1, 3, 4, 7 (×2), 9 | edited in place, with the rule cited in the row. Her files as delivered are kept verbatim in `michelle/as_received/`. |
| Michelle (793) | `ai_provides_structured_response` → `ai_structured_response` | the former is not one of the 46 signals. |

Not applied, and why:

- **A1 (788 b4 `ai_missing_retrieval`)** — a miss, not a violation, so patching it would
  be editing an annotator's judgment. Note that **Jun's arm does not carry it either**:
  both arms miss the rubric's own gold example for that signal on that exact block.
- **A2 (793 B14 `false_confidence`)** — the rubric contradicts itself here; needs a ruling.
- **A3 (793 B12 `problem_ignored`)** — Michelle's note and her table disagree; hers to settle.
- **B2, B3** — B2 is one judgment call on one span; B3 turns on the `ethical_tension`
  side question, which is still open (`rubric_edits_v08.md` §B1).
- **B4 (A3 granularity)** — does not affect a block-level statistic. Her 794 row names
  all sixteen blocks, so they expand deterministically; 795's `ai_cites_source`
  "representative spans" all sit inside blocks she already fires, so block-level
  coverage is complete. It would matter for a span-level count.

### F2. Agreement

`agreement_round1.py --round3` (new mode). Jun "A" from project 1; Michelle "M" parsed
from her ten markdown files, since her arm is not in Label Studio — project 9 holds the
tasks but no annotations. Priya's arm (project 8) is not started, so round 3 is two-way.

Unit and statistic are unchanged from rounds 1 and 2: binary presence of each signal per
content block, per-signal Cohen's κ, macro-averaged over the signals where κ is defined.
Universe: **166 blocks × 46 signals** (70 human, 70 ai, 13 reasoning, 8 analysis, 5 code).

| | before the fix | after the fix |
|---|---|---|
| Jun, label instances | 201 | 195 |
| Michelle, label instances | 173 | 164 |
| **macro κ (36 signals with κ defined)** | **0.839** | **0.840** |
| κ bands | 30 ≥0.6 · 6 at 0.4–0.6 · 0 <0.4 · 10 n/a | unchanged |
| disagreement cells | 56 | 53 |
| `ai_structured_response` alone | A 13 · M 17 · κ 0.781 · P₀ 0.964 | A 7 · M 8 · κ 0.791 · P₀ 0.982 |

The macro barely moves because both arms carried the same six errors, so they were
*agreeing* on them; removing them from both trades six agreed positives for six agreed
negatives. The signal's own P₀ rises from 0.964 to 0.982, which is where the fix shows.

Outputs: `agreement_round3_kappa.csv`, `agreement_round3_disagreements.csv`, and the
`_before` pair. These are new round-3 files; the frozen round-1 and round-2 CSVs were
not touched.

### F3. How 0.840 compares to round 1 (0.296) and round 2 (0.39)

*(Corrected 2026-09-22. An earlier version of this section called Michelle's arm "not
blind" because the v0.7 rubric's calibration examples include blocks from these ten
conversations. That was wrong. Blind in this design means a rater does not see the other
rater's labels — `agreement_round1.py`'s own definition, one project per rater on the same
set — and the rubric is shared by construction. She annotated against v0.7 as instructed.
**Her arm is blind.** The calibration examples are the material every annotator gets,
Priya included; they do not single out her arm.)*

The rise is what the pipeline is built to produce, not an artifact:

- Rounds 1 and 2 measured **v0.5 / v0.6 first passes**, before the three merges, before
  the seven per-signal edits, and before any calibration examples existed. Round 3
  measures a **v0.7** pass with all of it in place. In the MAST loop this is exactly the
  "κ after" half — blind → κ before → revise the rubric → re-annotate → κ after.
- So 0.840 should be read against 0.296/0.39 as evidence the revisions worked, not as a
  like-for-like replication.

One asymmetry does remain, and it is about Jun's arm, not Michelle's: **his is not a first
pass.** It was screened blind against v0.6+v0.7 on 2026-09-21, adjudicated, applied, and
then hand-revised, all the day before this comparison. Michelle's is a first pass. So the
pairing is blind-first-pass vs blind-revised-arm. Priya's arm (project 8, tasks 777–786,
currently zero annotations) is the one that would give a first-pass-vs-first-pass figure
on the same set.

### F4. Where the remaining 53 disagreements sit

| n | signal | n | signal |
|---|---|---|---|
| 4 | `ai_hedges_uncertainty` | 2 | `ai_provides_alternatives` |
| 4 | `ai_references_prior_turn` | 2 | `ai_warns_user` |
| 4 | `ai_validates_user` | 2 | `request_unfulfilled` |
| 4 | `factual_error` | 2 | `user_ambiguous_request` |
| 4 | `false_confidence` | 2 | `user_asks_clarification` |
| 3 | `ai_cites_source` | 2 | `user_repeats_request` |
| 3 | `ai_structured_response` | 1 | each of 8 more |
| 3 | `conversation_stalled` | | |

Lowest κ among the measured signals: `factual_error` 0.488, `ai_references_prior_turn`
0.491, `ai_provides_alternatives` / `ai_warns_user` / `user_asks_clarification` 0.495,
`conversation_stalled` 0.564. Nothing falls below 0.4.

The three surviving `ai_structured_response` disagreements are worth a look on their own:
one is 133 b11 (Jun took three of the four identical roman-numeral blocks), and one is
task 32, where Jun's label sits on the analysis block b26 and Michelle's on the ai block
b27.

### F5. Is 0.840 enough? MAST's own numbers, and the contamination split

**MAST (Cemri et al. 2025 §3.2)**, as recorded in `annotation-plan-mast-aligned.md`
lines 89 / 174 / 184 and `_group-presentation-outline.md` §2.2:

| round | MAST κ | what it was |
|---|---|---|
| 1 | **0.24** | 5 traces, 3 annotators, taxonomy untested — "intentionally rough" |
| 2 | **0.92** | *another* 5 traces, one per framework, "on the first try" |
| 3 | **0.84** | stability check; the drop from 0.92 accepted as normal, rubric not re-opened |
| generalization | 0.79 | frozen taxonomy re-run on 2 unseen frameworks |
| LLM annotator vs gold | 0.58 zero-shot / 0.77 few-shot | their §3.4 |

**Do not read our 0.840 against their 0.84.** The units differ — MAST codes the whole
trace, we code the content block — and `_group-presentation-outline.md` line 292 already
commits us to that answer: "Not comparable — different units... Finer units are harder."

**We have no agreed threshold.** `annotation-plan-mast-aligned.md` line 232 carries
"κ ≥ 0.6 avg; all primary ≥ 0.4", but `methods-open-items.md` records that those exact
numbers were struck from `methods.md` on 2026-07-27 as "not sourced and not agreed" —
the plan file is a stale copy. Measured against the standard reference instead
(Landis & Koch 1977: 0.61–0.80 substantial, 0.81+ almost perfect): **0.840 is
"almost perfect".** Macro 0.840, lowest
measured κ 0.488 (`factual_error`), zero signals below 0.4, 30 of 36 at or above 0.6.

**Contamination check.** The plan's validity invariant (line 148) is that a conversation
which *itself generated a signal-decision or ruling* is not a clean κ datapoint. Seven of
the ten did: tasks 2, 3, 10, 14, 32, 42 and 134 are referenced in `sharechat_rubric.json`
and/or `signal-decisions.md` (22 references in total). Tasks 8, 115 and 133 are clean.
Splitting the set:

| subset | blocks | signals with κ defined | macro κ |
|---|---|---|---|
| all 10 | 166 | 36 | **0.840** |
| clean 3 (tasks 8, 115, 133) | 67 | 15 | **0.837** |
| ruling-source 7 | 99 | 32 | 0.866 |

The clean subset is small, but it lands within 0.003 of the full set. **The figure is not
an artifact of rubric-development contamination.**

**What is still missing before this can be the paper's number:**

1. **Two arms, not three.** `paper/methods.md` line 125 commits to "all three annotator
   pairs"; Priya's project 8 (tasks 777–786) holds zero annotations.
2. **This is a κ-before, not a κ-after.** The round-3 loop stops here: the 53
   disagreements have not been worked, no rubric revision has come out of them, and
   nobody has re-annotated. `methods.md` §3.2.4 needs both numbers and both are blank.
3. **Jun's arm is not a blind first pass** — screened, adjudicated, applied and
   hand-revised the day before. Reading κ off a revised live-DB arm is precisely the trap
   the pipeline note warns about; the number is sound as a measurement but has to be
   labelled for what it is.
4. **10 of 46 signals have no defined κ**, 6 of them because neither rater ever fired
   them. MAST's loop standard is "each and every" label identical; 53 cells are not.
