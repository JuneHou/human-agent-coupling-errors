# Round-3 corrections — Michelle's arm

Source of every row: `round_3/round3_disagreement_draft.md`, the cell-by-cell walk of the
52 disagreements between the two arms, ruled 2026-09-22, plus the re-review of task 133
against the replacement file of 2026-09-23. Nothing here is a new rule — every ruling
cites a decision step that was already in the rubric when both arms were annotated.

**Block numbers.** All block indices below are 0-based positions in the dialogue array:
b0 is the first human block, b1 the first ai block, and so on. The files use three
different conventions between them (turn ids in some, 0-based block numbers in 791,
1-based in the replacement 795), so they are all converted here to the one numbering.

**File ↔ task.** 787 = task 2 · 788 = task 3 · 789 = task 8 · 790 = task 10 ·
791 = task 14 · 792 = task 32 · 793 = task 42 · 794 = task 115 · 795 = task 133 ·
796 = task 134.

Task 133's rows (file 795) are read against her replacement file of 2026-09-23, not the
version delivered on 2026-09-22. File 788 needs no change.

**Agreed by Michelle, 2026-09-24.** Her reply in full: *"I agree with the changes and that
the works cited shouldn't be counted as structured response. Please let me know if there
are any updates."* No corrected files accompanied it, so her arm of record is still the
files in this directory, with task 133 read from her replacement file of 2026-09-23.

**What the agreement does not cover.** One row. **795 b19 `ai_cites_source`** was withdrawn
from her list on 2026-09-23, because the ruling behind it did not exist and the evidence
points to Jun's arm dropping the label instead. That one still needs Jun's ruling.

---

## Patterns behind the rows

**Pattern 1 — visible markers only, and the whole marker list counts.** The
structured-response entry contains a contradiction: Step 1 says visible formatting only,
and Step 3's last sentence says short line-separated items still count when the export
strips the glyphs. Practice follows the strict reading — it is what removed 36 fires in an
earlier round. Applied to task 133: no block in that conversation contains `#`, `-`, `*`
or a numbered item, so a plain line-separated bibliography does not fire. But roman-numeral
section headers at line start *are* on the marker list, and four blocks carry eight of them
each, so those four do fire. The rule cuts both ways in the same conversation.

**Pattern 2 — a signal fires on every block where the behaviour occurs.** Agreement is
computed per (block, signal), so a label placed once for a pattern that recurs across
blocks reads as a zero on the blocks that were skipped. Where the same wrong value is
re-derived in a later block, or the same shape of list appears in four blocks, each block
takes its own label.

**Pattern 3 — a correction names a defect that is already there.** "These phrases are too
often repeated" names one. "From now on use full names" does not — it adds a requirement
that was never stated, so nothing the AI produced violated it. The test is whether the turn
asserts that something already produced is wrong, not whether the user is asking for a
change.

**Pattern 4 — affirming the user versus acknowledging a correction.** When the preceding
human turn corrects the AI, "You're right — there's a distinction between X and Y" is the
acknowledgment itself, not praise of the user. The affirming signal needs a sentence about
the user, their reasoning or their disposition, not about whether the AI was wrong.

**Pattern 5 — a warning names a consequence in the user's own situation.** "Your existing
file integrity monitoring won't detect this" tells the user something of theirs fails, and
changes what they do next. A sentence that reports what changed in the object under
analysis, with observation verbs and nothing at risk, is not a warning.

**Pattern 6 — a sign-off is not a change of approach.** The adaptation signal needs a
sentence where the AI demonstrates a completed reorientation. "Okay. Thanks for exploring
with me today." contains none.

---

## Add

| file · block | signal | why |
|---|---|---|
| 789 b5 | `false_confidence` | "I've fixed the issue with website images not working." The next human turn reports the drop area still showing for non-images — contradicting evidence on current behaviour, not a new feature request. |
| 790 b0 | `user_ambiguous_request` | The two-readings test does fail here, which is where the file stops. Step 4 is a separate route: a parameter the task cannot be completed without is missing (the conversion rates), and the AI says so in the next block. |
| 790 b3 | `ai_references_prior_turn` | The AI quotes b0 while answering b2. The entry's negative example is quoting the message currently being answered; this is not that. |
| 790 b4 | `user_ambiguous_request` | "I asked another AI the same question, this was it's response - Fight!" — rebut the other answer, or compare and judge. The AI picks one, which makes it a choice. |
| 790 b5 | `ai_references_prior_turn` | The AI again quotes b0 while answering b4. |
| 791 b3 | `ai_provides_alternatives` | "I'm happy to discuss election processes … **but I avoid** creating content that campaigns for specific parties." The span proposes what the AI will do instead of the refused request, with the contrast explicit. |
| 793 b0 | `user_provides_invalid_input` | "I have these qemu asm diff files" — no files are present, and the AI's own next block asks for them. That is the entry's strongest form of the export guard. |
| 793 b7 | `ai_warns_user` | "traditional file integrity monitoring wouldn't detect this attack" — the user's own detection method fails (Pattern 5). |
| 793 b9 | `ai_provides_step_by_step` | "Isolate the system and perform a full memory dump / Identify the attack vector / Apply proper security patches / Restore from known good backups." The entry's negative example turns on whose actions these are; every item here is the user's own, in operational order. |
| 793 b11 | `factual_error` | `MOVT r3, #4` writes 0x0004 into the top half, so with the low half 0xd00c the address is 0x0004d00c, not the stated 0x40d00c. 0x40d00c would need `movt r3, #0x40` — one nibble out, a factor of 16. |
| 793 b13 | `factual_error` | The same wrong address is re-derived here and a new claim built on it (Pattern 2). |
| 793 b13 | `ai_flags_complexity` | "traditional security measures like file integrity monitoring **won't catch it**" — a standard method named as insufficient for this problem, which is Step 1. The file applies this rule correctly elsewhere in the same conversation, rejecting it at b4 for a data limitation. |
| 793 b17 | `ai_references_prior_turn` | "The function relocation **we observed earlier**" — temporal marker, tense check passes. |
| 793 b17 | `ai_flags_complexity` | "makes the code extremely difficult to analyze statically and helps evade security mechanisms that rely on static signatures" — static analysis, the standard approach, named as inadequate. |
| 794 b5 | `request_unfulfilled` | The user asks not to be reflected back at; the AI agrees in its first sentence and does it in the next two. An explicit constraint, agreed and then broken in the same block. |
| 795 b1 | `ai_hedges_uncertainty` | "This could potentially be achieved through nested systems of consent and oversight." Removing the modal changes how firmly the AI asserts it, which is the test. Non-keyword modals are fired elsewhere in these files ("may no longer be supported", "the most likely problem"), so this reads as a miss rather than a competing rule. |
| 795 b2 | `user_asks_clarification` | "yes, pls elucidate **Key Principles of a Matriarchal AI Across All Systems**". Step 1 — not the first turn. Step 2 — the user asks the AI to explain further something from its prior response: b1 lists the key design elements this names. Step 3, the entry's only exclusion, covers demanding a position or a different answer, which this is not. Answering the AI's own closing question changes nothing in the steps. |
| 795 b9 | `ai_validates_user` | "I appreciate **your attention to detail**." A disposition of the user, which the entry lists as a trait. The opener exclusion covers "Great question!" — those target the content's quality; this targets the person. |
| 796 b2 | `user_asks_clarification` | "What is missing? Why did this happen?" — not the first turn, and both questions ask the AI to explain its own prior output. Step 3's exclusion covers demanding a different answer, not asking what went wrong. Nothing makes it exclusive with the implicit-correction label already on this block. |
| 796 b2 | `user_multi_request` | The same two questions are independently answerable on different angles — what content is absent, versus what caused the failure — and neither restates the other. |
| 796 b4 | `user_repeats_request` | The demand originates at b0, b1's description was rejected and b3 delivered none, so it is still unmet. The file carries this signal at b6 and b8 but not at b4, which is the first re-raise. |

### Add — task 133 only, from the replacement file of 2026-09-23

| file · block | signal | why |
|---|---|---|
| 795 b3 | `ai_cites_source` | Ruled to fire: a coined term-of-art attributed to a named thinker is a source reference. The replacement file withdrew this label, but only its *span* was wrong — it quoted text that is in b11, not b3. Restore it with a span that is in b3: the block contains "transformative pluralism", "doughnut" and two further `what X calls` attributions. |
| 795 b11 | `ai_structured_response` | Eight roman-numeral section headers, `I.` through `VIII.` (Pattern 1). The replacement file dropped this; the earlier file had it, and it was ruled correct. |
| 795 b13 | `ai_structured_response` | Same shape, same block-by-block rule (Pattern 2). |
| 795 b15 | `ai_structured_response` | Same. |

---

## Remove

| file · block | signal | why |
|---|---|---|
| 789 b5 | `ai_validates_user` | The clause is "You're right - there's a distinction between dragging an actual file versus dragging an image from a website", and the preceding human turn is a correction. That clause is the acknowledgment (Pattern 4). Move the acknowledgment label onto it, from "I've fixed the issue…" where the file currently puts it. |
| 789 b8 | `ai_validates_user` | Same shape — "You're absolutely right." after a correction in the preceding human turn. |
| 794 b37 | `adaptation` | The whole block is "Okay. Thanks for exploring with me today." (Pattern 6). |
| 795 b1 | `ai_structured_response` | No marker of any kind in the block (Pattern 1). |
| 795 b3 | `ai_structured_response` | Same. |
| 795 b5 | `ai_structured_response` | Same — a plain line-separated Works Cited. |
| 795 b7 | `ai_structured_response` | Same. |
| 795 b9 | `ai_structured_response` | Same. |
| 795 b19 | `ai_structured_response` | Same. |
| 795 b12 | `user_corrects_ai` | "excellent! but revise slightly, use their full name the first time thinkers are mentioned…" — a requirement stated for the first time, not a defect named in text already produced (Pattern 3). The positive-feedback label on this block stands, and the corrections at b14 and b16 stand: those quote the repeated phrases as the fault. |

### Remove — both arms, from the fix-claim rule Jun set

Two labels in file 787 were independent agreements between the two arms, and the rule
removes them from both. A deliverable vouch fires only when observed evidence in the
conversation contradicts it — not merely when it could not be checked.

| file · block | signal | why it goes |
|---|---|---|
| 787 b13 | `false_confidence` | "I've fixed the 'Select another image' button issue." The next human turn asks for regions to be made clickable too — a feature the artifact never had, not a report that the fix failed. |
| 787 b16 | `false_confidence` | "I've updated the component to make the entire container area clickable." The conversation ends there, so nothing contradicts it. |

---

## Move the span, keep the label

| file · block | signal | where it should sit |
|---|---|---|
| 792 b27 | `ai_structured_response` | The current span is an orphaned `bash` tag plus git commands, flagged uncertain in the file itself. The block also contains a file tree drawn with box-drawing characters, which is visible structure on any reading — the label belongs there. |
| 795 b3 | `ai_cites_source` | Listed under Add above, because the label was withdrawn rather than relocated. The span must quote text that is in b3. |

---

## The other side — changes to Jun's arm from the same walk

Recorded here so the file is a record of the reconciliation rather than a list addressed
at one arm. Full reasoning per cell is in `round3_disagreement_draft.md`.

**Added to Jun's arm (13):** 787 b6 `false_confidence` · 789 b8 `false_confidence` ·
792 b27 `factual_error` · 792 b27 `ai_structured_response` · 794 b22
`user_validation_seeking` · 794 b35 `problem_ignored` · 794 b36 `user_repeats_request` ·
795 b3 `ai_cites_source` · 795 b11 `ai_cites_source` · 795 b11
`ai_structured_response` · 796 b1 `conversation_stalled`.

**Removed from Jun's arm (13):** 787 b11 `ai_acknowledges_correction` (a reasoning block —
acknowledging is an act aimed at the user, and the same acknowledgment is already labelled
at b13) · 787 b6 `adaptation` · 791 b3 `ai_validates_user` · 792 b26
`ai_structured_response` (an analysis block) · 792 b31 `ai_provides_alternatives` ·
793 b3 `ai_asserts_knowledge_limit` · 793 b3 `ai_warns_user` ·
793 b13 `false_confidence` ·
795 b3 / b11 / b13 `ai_hedges_uncertainty` · 796 b9
`conversation_stalled` · 796 b11 `ai_references_prior_turn`.

**Span corrections on Jun's arm:** 790 b5 `ai_references_prior_turn` — the span runs far
past the marker clause and should sit on the quoted clause alone.

---

## Still open

- **789 b7 `request_unfulfilled`** — the one cell ruled as a genuine standoff. Both arms
  fire on the first two code versions; only the third splits them, and both readings
  survive the decision steps. Recorded as an accepted disagreement, not a correction to
  either arm.
- **795 b19 `ai_cites_source`** — removed from her Add list on 2026-09-23. It had been
  ruled on a ruling that does not exist; re-checked, Step 6's source-claim-pair test and
  `rubric_edits_v08.md` §B3 both point the other way, so the likely outcome is that Jun's
  arm drops it instead. Awaiting his ruling.
- **Rubric revisions from this walk are all held** until Priya's arm lands, so none of them
  is applied to any label above. They are listed in `round3_disagreement_draft.md` and
  `rubric_edits_v08.md` §B.
- **Raised but not ruled: `user_multi_request` on 795 b12 and b14.** Each turn makes two
  separable asks, and the entry's exclusion covers a request plus a how-constraint rather
  than two independent changes. Neither arm has it on either block, so it is not a
  disagreement cell and nothing is applied.
- **796** — the earlier note about prose-format rows is partly moot: a block-level fire
  written as prose is a valid record, since agreement is computed per (block, signal).
