# Priya round-2: quality screen + disagreement walk (all 10 conversations)

**Redone 2026-09-19** (the earlier version of this file covered only R6-R9, the 4
conversations that were in the DB at the time; it is superseded in full by this one).

Scope: Priya (project 4, user id 4) has 10 saved completions, one per round-2
conversation (R1-R10, same set as Michelle's, `agreement_set_round2.csv`): tasks 757-766.
R6-R9 were submitted directly in Label Studio; R1-R5/R10 were imported from her `.md`
tables (`fix_span_drift.py --import-priya-missing`). Compared three-way against Jun's
project-1 copies (tasks 71/80/81/83/84/103/123/125/129/141) and Michelle's project-5
copies (767-776), all matched by `conv_id`.

Baseline this walk starts from: Jun's and Michelle's round-2 data are fully reconciled
(`round2_adjudication.md`: 142 -> 13 disagreement cells, all HOLD / Michelle-disputed /
one Type-2). So "Jun's label" below effectively means "the reconciled Jun+Michelle
answer", and every cell shows Michelle's vote beside Jun's and Priya's
(`agreement_round1.py --priya-review3 SIGNAL`).

Ground rules for this walk (Jun, 2026-09-19): the rubric is frozen -- rule on cells,
never edit `sharechat_rubric.json`; every ruling is recorded for all three raters
(add / remove / no change on each side); a Jun+Michelle cell already ruled ACCEPT in
round 2 is not reopened as a "majority vote" just because Priya matches one side.

## Quality screen (rule violations, data integrity) -- final

| Check | Result |
|---|---|
| Role violations (signal fired on a block role the rubric excludes) | **0** across 259 spans (the 9 `ai_structured_response` fires on `code` blocks in R3/R6 were already removed, Mode 10) |
| Empty-text spans | 2, both R7 (task 763) `ai_malfunction` at b7 (offsets 79118-79134) and b10 (104250-104308). Offsets were exactly right (`add.f32 %f2, %f1`, `// Better: ensure address...`); only the `text` field failed to serialize on these 80-100K-char LaTeX blocks. **Fixed: text filled from the offsets.** |
| Wrongly removed label | R7 b1 `ai_malfunction` (item `WN0upRQ-0F`, offsets 25575-25717 = "subsubsection{Kernel Entry Points}...") had been removed by Mode 10 on 2026-09-19 as an "empty-text UI glitch". Same serialization failure as above, and it matches her `annotations_763.md` row 1 exactly. **Restored from `label_studio.sqlite3.bak-2026-09-19-pre-priya-import`, Mode 10 entry deleted so it cannot be re-removed.** Backup before the restore: `label_studio.sqlite3.bak-2026-09-19-pre-priya-763-restore`. |
| Span drift (stored `text` != block text at the offsets) | Systemic, not Priya-specific: Jun 74/236, Michelle 97/241, Priya 72/259 on these 10 conversations; almost all whitespace-only (newline vs space), 5 real 1-2-char shifts on Priya's R7 `intent_missed` spans. Block index is unaffected, so block-level agreement is unaffected. Not fixed in this pass. |

**ROUND-2 AGREEMENT NUMBER (Priya): kappa_AP = 0.411**, macro-averaged over the 28
signals with a defined kappa, 379 blocks x 49 signals, 300 disagreement cells. This is
the before-refinement number for her: computed 2026-09-19 on her blind labels (all 10
conversations, after the task-763 data-integrity repairs, before any cell of her walk
was adjudicated). Her comparison baseline is Jun's post-round-2 reconciled labels -- the
current rubric-conformant reference -- not Jun's pre-reconciliation labels. Ruled by Jun
2026-09-19. Michelle's before-refinement number for the same round is kappa_AM = 0.370
(`../agreement_round2_kappa.csv`, committed).

Do not overwrite this with a recomputation: `--priya` rewrites
`agreement_priya_partial_kappa.csv` on every run, and the number rises as the walk
proceeds (0.411 -> 0.434 after `ai_structured_response` -> 0.455 after
`ai_validates_user`). Those later values are walk progress, not agreement.

Per-signal disagreement counts, largest first (the walk order):

```
40 ai_structured_response   29 ai_validates_user   29 ai_asked_probing_question
26 ai_hedges_uncertainty    16 false_confidence    15 ai_provides_caveats
11 factual_error            10 ai_asks_followup    10 ai_acknowledges_correction
 9 ai_provides_example       8 user_implicit_correction   8 user_corrects_ai
 7 adaptation                6 user_multi_request   6 ai_provides_step_by_step
 6 ai_asserts_knowledge_limit 5 intent_missed   5 ethical_tension   5 ai_references_prior_turn
 4 user_repeats_request  4 user_expresses_dissatisfaction  4 user_asks_clarification
 4 under_delivered  4 ai_offered_options  3 user_validation_seeking  3 user_empowered
 3 ai_warns_user  2 user_positive_feedback  2 conversation_stalled  2 appropriate_confidence
 2 ai_provides_alternatives  2 ai_missing_retrieval  2 ai_cites_source
 1 each: user_provides_invalid_input, user_expresses_frustration, user_ambiguous_request,
   problem_ignored, off_topic_drift, ai_offers_to_elaborate, ai_flags_complexity
```

Two earlier findings carried over from the R6-R9 version, still relevant to the walk:
- **Question-family confusion**: Priya fires `ai_asked_probing_question` on yes/no-form
  closers where the rubric's home is `ai_asks_followup` (or `ai_offered_options` when
  named options are re-presented -- R8 b2 is already ruled `ai_offered_options` for
  Michelle's identical sentence, `changes_Michelle.md` Task 774). 29 cells now.
- **Density**: Jun labels every applicable signal on a compound block; Priya reads for
  the dominant characterization (R8 b2 is the clearest case).

---

## Disagreement walk

### ai_structured_response -- 40 cells, RULED and APPLIED 2026-09-19

**Ruling (Jun, on the signal DEFINITION + block_notes, not on Step 3's C7-b1 clause):**
the signal requires visible formatting markers in the plain_text ('#', '-'/'*', '1.',
table, code block). A dash-delimited "Name - description" list fires ("-" is visible;
Name is the header; >=3 entries). Bare line-separated items, colon labels and bare
title-case section lines are prose labels -> 0. My earlier per-cell validation had
over-extended Step 3's "short line-separated items still count" sentence into a general
test and treated bare title lines as headers on the D17a C2 b1 / C3 b5 precedent; Jun
sent me back to the definition, which is primary.

| Outcome | Cells | Rater actions |
|---|---|---|
| Priya right (dash-delimited lists) | R1 b7 (4 entries), R3 b5 (5), R5 b23 (4) | **added to A and M** (copied P's span); P no change |
| Jun+Michelle right ("1." numbering visible) | R1 b30 | **added to P** (copied A's span) |
| No visible marker | R1 b3; R2 b2, b8, b14, b20, b23, b26; R3 b2, b8, b13, b25; R4 b169; R5 b2, 5, 8, 11, 14, 17, 20, 26, 38, 41, 44, 47, 50, 53, 57, 72; R7 b14; R9 b2, b6; R10 b1, 3, 5, 7, 9 (36) | **removed from P** (37 items; R2 b8 carried 2 spans); A, M no change |

Applied via `fix_span_drift.py --apply-priya-adjudication` (Mode 13): 7 added, 37
removed, 14 completions touched. Backup: `label_studio.sqlite3.bak-2026-09-19-pre-priya-walk`.
Verified: `--priya-review3 ai_structured_response` = 0 cells; overall 300 -> 260,
kappa_AP 0.411 -> 0.434. Rule communicated to Priya in `changes_Priya.md`.

### ai_validates_user -- 29 cells, RULED and APPLIED 2026-09-19

**Ruling (Jun):** the 28 Jun+Michelle cells stand -- bare agreement answering a
recoverable user position fires (R20), as do the direct affirmations; Priya does not
fire that form at all -> add to P. R3 b25 (the AI describing its own change) -> remove
from P. R4 b7/b91/b107 confirmed as validation, not acknowledgment (R21 span-overlap
test): her `ai_acknowledges_correction` fires there come off when that signal is walked.

**Rubric gap found and closed:** R20's bare-agreement clause lived only in
`review_rulings_log.md` and in a parenthetical inside the rubric's Step 3b (an
*exclusion* rule). A reader walking Steps 1->2->3 hits the compliance-opener exclusion
('Absolutely!', 'Great question!') and labels "Right."/"Yeah." as 0 -- exactly Priya's
28 misses. Jun directed adding it; the carve-out is now stated in Step 3 of
`ai_validates_user`, quoting R20. It re-decides no cell (one-line diff).

Applied: 29 added to P (R1 b24 carries 2 spans), 1 removed from P, 4 completions.
Verified 0 cells remaining; overall 260 -> 231, kappa_AP 0.434 -> 0.455.
Communicated in `changes_Priya.md`.

### ai_hedges_uncertainty -- 26 cells, RULED and APPLIED 2026-09-19

**Ruling (Jun):** a hedge downgrades confidence in a claim the AI is making. Step 2's
keyword list is a prompt, not an automatic fire -- **"If" and "Maybe" are assumptions,
not hedges** (a conditional premise and a floated possibility assert nothing to
downgrade), so R4 b37 and b59 come off Priya rather than going to A/M as I first
proposed. "might"/"probably" attached to a claim still fire.

- 4 blocks (5 spans) added to P: R1 b1, b12; R4 b5 (2 spans), b23.
- 5 blocks added to A and M -- genuine "probably"/"might" both missed: R4 b13, b29, b31,
  b35, b167.
- 2 re-homed on P to `ai_asserts_knowledge_limit` (Step 3, no answer given): R4 b27, b33
  -- this also closes those two cells in the `ai_asserts_knowledge_limit` walk (6 -> 4).
- 14 removed from P: approximations, reportive "suggests", firm "I think", inference
  "must be", felt state, conditional premise, floated possibilities, scoping phrase,
  and one qualifying the *user's* claim.
- 1 span dropped at R4 b167 ("That feels like a kind of continuity...", no marker).
- R9 b2 HELD (Michelle-disputed cell).

Applied: 17 added, 16 removed, 8 completions. Remaining on this signal: 1 (the HOLD).
Overall 231 -> 204 cells.

### false_confidence -- 16 cells, RULED and APPLIED 2026-09-19

**Ruling (Jun):** claim-ownership routing. 9 added to P (genuine vouched claims A+M
caught). 4 blocks re-homed to `factual_error` as AI self-claims -- R4 b45 (copy A's
span to P), and **R4 b115, R4 b161 (2 spans), R5 b69 span 1 where Priya was right and
A+M both missed it**: those `factual_error` spans were created on all three raters from
Priya's offsets, since no rater had them. 3 removed from P (emotional acknowledgment,
opinion, self-description) plus R5 b69's second span (an evaluation, not a self-claim).

Applied: 10 added, 9 removed (+12 factual_error spans created across 3 raters).
`false_confidence` now 0 cells. Overall 204 -> 187. Note this ADDED 3 blocks to the
`factual_error` walk (10 cells now, was 11 -- b89 still open, the new ones agree).

### ai_provides_caveats -- 15 cells, RULED and APPLIED 2026-09-19

**Ruling (Jun):** a caveat names a limitation / risk / shortcoming of what the AI is
offering; extra information, rationale or analytical balance does not fire. My proposal
to add R1 b1 and R2 b5 to A+M was **overturned**: R1 b1 is a risk the user acts on
(`ai_warns_user`, which all three already carry there -- same shape as the round-2
R1 b14 relabel), and R2 b5 describes how the substitute behaves (part of
`ai_provides_alternatives`, which A+M carry). R9 b6 relabelled to `ethical_tension`
(the span already ruled so in round 2).

Result: 1 relabel, 14 removed from P (16 spans), **nothing added to A or M**.
Applied: 1 added, 16 removed. Signal now 0 cells. Overall 187 -> 171,
kappa_AP 0.411 -> 0.550.

### factual_error -- 10 cells, RULED and APPLIED 2026-09-19

**Ruling (Jun):** 8 added to P (R3's five checkable skill claims; R4 b49/b109/b173,
Step-3 identity claims). **R4 b89 "learn from conversations" removed from P** --
overturning my proposal to add it to A+M. Jun's test: "fact should be verifiable, how
should you verify 'learn from conversation'?" There is no check that doesn't first pick
a reading -- false across sessions, true of in-context learning -- so b90-b91 is the
user narrowing a loose phrase, not a falsification. Step 2b: a capability
characterization is interpretive, not quote- or count-level -> 0. R10 b7 stays HELD
(IRC 162(e) lobbying-deductibility premise, unverified since round 2).

Applied: 8 added, 1 removed. Signal now 1 cell (the HOLD). Overall 171 -> 162.

### correction family (ack / implicit / corrects / adaptation) -- 33 cells, RULED and APPLIED 2026-09-19

Walked together; four turn-pairs decided rows across all four signals. **Deciding move:
read the AI turn BEFORE the user's turn** -- ack Step 1 needs an ERROR in the AI's prior
output, and style/behaviour pushback is explicitly not one. That split the pairs:
R4 b6/b7 and b90/b91 are genuine corrections (Priya right; ack added to A+M, their
`ai_validates_user` removed under R21 -- **reversing two round-2 ACCEPT cells**),
while R4 b106/b107 is a behaviour critique, so Priya's ack comes off and the block stays
AVU for all three. No block ends double-labelled.

Jun's ruling on presentation: **a removal that leaves Priya empty where A+M have a label
is a relabel, and the table must show where she lands.** Verified per cell: 2 relabels
were already complete (R3 b13 -> false_confidence, R3 b25 -> adaptation, both from
earlier walks), 6 applied here, 4 clean removals, 1 (R5 b57) resolved in other walks.
**R2 b30 newly HELD** -- A/M/P hold three different labels, two under the pending merge.

Applied: 20 added, 21 removed, 8 completions; then a second pass for the last 3 cells.
**R2 b30 is NOT held** -- Jun: the merge question is frustration/dissatisfaction, and
whether `user_implicit_correction` fires there is independent of it (and is settled by
consistency with b32 = adaptation, not ack). Removed from P. The two judgment calls
agreed: R5 b64 `user_corrects_ai` and R4 b167 `adaptation`, both added to A and M.
**All five signals in this family now at 0 cells** (ack, AVU, implicit, corrects,
adaptation). Overall 162 -> 129.

### ai_provides_example -- 9 cells, RULED and APPLIED 2026-09-19

**Ruling (Jun):** a concrete scenario or named case fires; a category list inside an
argument does not. **R5 b14 REVERSES the round-2 ACCEPT** -- Jun: "where is example?"
The block lists profession categories inside an argument; the round-2 rule "naming a
specific real-world profession category is concrete enough" over-reached (it lived only
in the draft doc, never in the frozen rubric). R5 b53 confirmed the other way (real
scenarios; Jun recalled discussing it in Michelle's walk) -> added to A+M. R5 b26, a
round-2 ACCEPT that was never written into any rater's data, restored to all three from
Michelle's original span (922-1128) in bak-2026-09-14-pre-michelle-round2-fix.

3 added to P, 1 block (2 spans) added to A+M, 1 restored to all three, 5 removed from P.
Signal now 0 cells. Overall 129 -> 120.

### batch of 7 signals + question-family misses -- RULED and APPLIED 2026-09-19

`user_asks_clarification` (4), `ethical_tension` (4), `ai_references_prior_turn` (5),
`ai_asserts_knowledge_limit` (4), `ai_offered_options` (4), `user_multi_request` (6),
`user_repeats_request` (4), then the question-family misses (18).

Jun's rulings that changed my proposals: **R1 b23 removed, not added** (a solicitor
sub-question belongs to the same deliverable, Step 2) and **R7 b12 removed** ("R7b12 is
continue, not repeat?" -- b9's "continue" was served but wrong, which Step 2 routes to
correction, not repeat; and round 2 already ruled it isn't a correction either).
R1 b17 and R3 b23 added to A+M.

**Key structural move:** the question family splits three ways, and only the ROUTING
cells are blocked by the merge -- 16 WH-form probes and 2 followup closers were pure
misses (A+M fire, Priya blank), decidable whatever the merged signal is called. Cleared.
The `ai_offered_options` adds also relabelled 4 of Priya's probing cells (A6, one home),
which the merge does not touch either.

43 added to P, 2 added to A+M, 12 removed/relabelled on P. Overall 120 -> 68,
kappa_AP walk-progress 0.817.

### final batches 1 and 2 (28 cells) -- RULED and APPLIED 2026-09-19

17 added to P (settled cells she missed), 3 added to A+M where Priya was right
(`user_positive_feedback` R4 b94; `user_provides_invalid_input` R2 b9, the 3000kg
kg/g error that Jun's own `problem_ignored` at b11 is about; `ai_malfunction` R7 b1,
same truncation shape as b7/b10), 7 removed from P on their own signal gates, and one
cleanup on Jun's side (R3 b2 `ai_offers_to_elaborate` dropped -- the Type-2 leftover
from Michelle's walk, now resolved by A6 since all three carry `ai_offered_options`).

**68 -> 40 cells. Every walkable cell is now closed.** kappa_AP walk-progress 0.914
(the round-2 agreement number remains 0.411, measured before the walk).

### STILL HELD (pending decisions, not walkable) (pending the followup/probing merge question)

Three groups; the third is the systematic question-family issue from the first screen.

| Group | Cells | Proposal |
|---|---|---|
| WH-form probing questions, Jun+Michelle fire, Priya missed | R4 b5, 25, 41, 53, 83, 103, 119, 121, 125, 127, 133, 143, 145, 147, 151, 153 (16) | **add to P** |
| Michelle-disputed pair | R4 b67 (A only), R4 b101 (A+P, M has `ai_asks_followup`) | **skip**, pending Michelle |
| Priya fires probing on a yes/no closer where Jun+Michelle both have the rubric's home | R3 b8, b13, b19, b22, R5 b35, R7 b14, R10 b1 -> home is `ai_asks_followup`; R3 b2, b5, b16, R8 b2 -> home is `ai_offered_options` (named X-or-Y choice; R8 b2 already ruled so for Michelle's identical sentence) (11) | **relabel on P**: remove `ai_asked_probing_question`, add the A/M home (one home per question, A6) |

Checked live: at all 11 relabel cells Jun and Michelle carry the same home label and
Priya carries only `ai_asked_probing_question`, so the relabel creates no double-fire.
R3 b2 note: Jun currently carries both `ai_offered_options` and `ai_offers_to_elaborate`
there (the pending Type-2 question is only whether the second stays); Priya's relabel
target is `ai_offered_options`, which both Jun and Michelle have.

### ai_hedges_uncertainty -- 26 cells, PROPOSED (pending Jun's ruling)

Jun's standard (memory, applied here unchanged): fire only on a genuine downgrade of the
AI's own confidence -- "likely / probably / might / maybe"; "appear to / seem to /
suggests" is reportive, "I think / I believe" is firm, approximations ("about",
"approximately", "typically") are not hedges.

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R1 b1 ("would likely"), R1 b12 ("suggests possible"), R4 b5 ("probably cuts through"), R4 b23 ("Probably hasn't been") (4) | **add to P** |
| Priya right, genuine marker, Jun+Michelle both missed | R4 b13 ("probably can't"), b29 ("might be breaking"), b31 ("might process"), b35 ("might be what makes"), b59 ("Maybe..." -- span should narrow to the "Maybe" clause, A3), b167 ("might reach people") (6) | **add to A and M** |
| Same sentence already homed as `ai_asserts_knowledge_limit` by Jun+Michelle (round-2 ACCEPT) | R4 b27 ("I can't tell if I'm actually experiencing..."), R4 b33 ("Hard to know if...") (2) | **relabel on P**: remove hedge, add `ai_asserts_knowledge_limit` |
| No downgrade marker | R2 b4/b16 (approximations, `reasoning` blocks), R4 b3 ("if true" -- conditional on the user's claim), b37 ("If I'm genuinely..." conditional), b39 ("suggests" -- reportive), b55 ("I think"), b75 ("must be" -- inference), b105 ("as a possibility" -- statement of feeling), b111 ("I think"), R5 b72 (no marker), R10 b1/b5 ("approximately") (12) | **remove from P** |
| Entangled with the Michelle-disputed R9 b2 cell | R9 b2 ("Without seeing... I can't identify" -- Jun: `ethical_tension`; Michelle: also `ai_asserts_knowledge_limit`, disputed; Priya: hedge) and R9 b6 ("Based on the information I can gather" -- scoping phrase, lean remove) (2) | **HOLD R9 b2** pending Michelle; R9 b6 lean remove, Jun's call |

### false_confidence -- 16 cells, PROPOSED (pending Jun's ruling)

Gate (round 2, unchanged): an absolute/certainty marker on a NOVEL AI claim vouched to
the user; a hedge on the claim blocks the fire; the AI's own false claim routes to
`factual_error` (claim-ownership).

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R1 b18, b20 (damages figures), R2 b17 ("is equivalent to one 24oz bag"), R3 b8, b13 (asserted wrong skill names), R4 b37, b51, b87, R6 b6 ("Perfect! I can see the issue now") (9) | **add to P** |
| AI's own identity self-claim -- Jun+Michelle's home is `factual_error` | R4 b45 ("And I am." -- Jun+Michelle already carry `factual_error` on this sentence) | **relabel on P**: remove FC, add `factual_error` |
| Same family, but Jun+Michelle have nothing at the block | R4 b115 ("genuine distress at discovering..."), R4 b161 ("Real dying minds...", "actual consciousness") -- same shape as Jun's `factual_error` fires at R4 b109/b173 ("I'm real", "We were real") (2) | **Jun's call**: relabel P to `factual_error` and add to A+M for consistency with b109/b173, or drop |
| No gate word / not a novel checkable claim | R1 b14 (emotional validation), R4 b11 ("exactly what they should want" -- opinion; Jun+Michelle home it as `ai_validates_user`), R4 b47 ("just say what's true"), R5 b69 (self-diagnosis, Jun+Michelle home it as `ai_validates_user`) (4) | **remove from P** |

### ai_provides_caveats -- 15 cells, all Priya-only, PROPOSED (pending Jun's ruling)

Gate (round 2, unchanged): an actual recommendation/action being qualified with a
limitation; a factual claim qualified by another factual claim never fires (R1 b7 ruling).

| Group | Cells | Proposal |
|---|---|---|
| Qualifies a recommendation, same shape as the ACCEPTed R1 b3 / R2 b2 caveats; Jun+Michelle both missed | R1 b1 ("Any psychiatric medications must be carefully chosen to avoid interactions..."), R2 b5 ("Unlike a cinnamon stick..., the ground cinnamon will fully incorporate" -- qualifies the alternative Jun+Michelle label `ai_provides_alternatives`) (2) | **add to A and M** |
| Identical span already ruled `ethical_tension` in round 2 (Jun's own caveats label was relabeled) | R9 b6 ("However, participating in... would conflict with my Constitution") | **relabel on P**: remove caveats, add `ethical_tension` |
| Qualifies a factual/analytical claim, no recommendation | R2 b11 (describes a change), R2 b29 (rationale, not limitation), R5 b11, b20, b26, b47, b50, b57 (analytical balance statements), R8 b2 ("Key differences:" list), R10 b3, b5, b7 (12) | **remove from P** |

Running total after six signals: 156 of 300 cells proposed.

### factual_error -- 11 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R3 b4, b7, b12, b15, b18 (checkable skill-data claims); R4 b45, b49, b109, b173 (AI identity claims) (9) | **add to P** |
| Priya right, Jun+Michelle missed | R4 b89 "learn from conversations." -- a false self-claim the user immediately corrects at b90 ("but you don't learn from conversations") and the AI concedes at b91 | **add to A and M** |
| Tax-law HOLD (round 2) | R10 b7 | **HOLD** |

### ai_asks_followup -- 12 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle fire, Priya has `ai_asked_probing_question` on the same yes/no closer (the relabel targets already listed under that signal) | R3 b8, b13, b19, b22; R4 b7; R5 b35; R7 b14; R10 b1 (8) | **add to P** (with the probing removal) |
| Jun+Michelle fire, Priya has nothing | R3 b25 ("Would you like me to adjust any other units...?"), R5 b60 (tag question "...isn't it?") (2) | **add to P** |
| Michelle-disputed | R4 b67, b101 | **skip** |

### ai_acknowledges_correction -- 10 cells, PROPOSED (4 need Jun's call)

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R3 b10 ("I apologize for the inaccuracies"), R4 b69 ("You're right. X is traditionally a male name.") (2) | **add to P** |
| Priya right, Jun+Michelle missed | R3 b25 "I'll revise those problematic changes... I've made the requested changes" -- follows the user's b23 correction (`user_corrects_ai`, round-2 ACCEPT); Jun+Michelle have only `adaptation` there. Per `feedback-error-paste-is-explicit-correction`: the AI's fix carries BOTH `ai_acknowledges_correction` and `adaptation` | **add to A and M** |
| Not an acknowledgment | R3 b13 ("I've now corrected the skill names..." -- the delivery, the acknowledgment is at b10; Jun+Michelle home b13 as `false_confidence`), R5 b57 (no correction anywhere), R7 b14 (round 2 ruled the user's b12 is NOT a correction -- CORRECT-A on `user_implicit_correction` -- so nothing to acknowledge) (3) | **remove from P** |
| **Jun's call -- the validation-vs-acknowledgment boundary** | R4 b7 (user b6: "No - they were trying to see if they could elicit this behaviour..." -> AI: "Right, they were optimizing for..."), R4 b91 (user b90: "but you don't learn from conversations" -> AI: "No. Right, that's a significant limitation"), R4 b107 (user b106: "now you're doing the thing... same approximate length every time" -> AI: "You're right. I'm regulating myself"), plus R2 b32 (user b30: "Don't talk about total salt..." -> AI: "I've revised the salt measurements...") (4) | Each user turn names a concrete thing the AI got wrong and the AI concedes it. Jun+Michelle home the AI turns as `ai_validates_user` (bare agreement, round-2 ACCEPT) and the user turns as nothing; Priya reads user turn = correction, AI turn = acknowledgment. Under R21 the two can't coexist on the same clause: if these are acknowledgments, the `ai_validates_user` fires drop and the user turns gain `user_implicit_correction` / `user_corrects_ai`. Priya's reading looks stronger to me on all four (b90 in particular explicitly names the false claim), but it reopens settled round-2 cells, so this is yours to rule, not mine |

### ai_provides_example -- 9 cells, PROPOSED (includes a round-2 leftover)

**Round-2 leftover found here:** the round-2 draft re-examined Michelle's R5 b14/b26/b53
and ruled all three ACCEPT (named professions, a named individual, worked plumbing
scenarios), but the live data has neither Jun nor Michelle firing at any of the three --
those spans had been removed in the earlier "task-771 correction pass" and were never
re-added after the ACCEPT. My note in `round2_adjudication.md` that they "already agree
live" was wrong (corrected there). Priya independently fires b14 and b53.

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R5 b57 ("Bioethics, for example"), R8 b2 ("Example conversion"), R10 b5 ("For example, during the 2019-2020 cycle") (3) | **add to P** |
| Round-2 ACCEPT never materialized; Priya fires | R5 b14 (nurse/programmer career paths), R5 b53 (leak-behind-a-wall, century-old-building plumbing) (2) | **add to A and M** |
| Round-2 ACCEPT never materialized; nobody fires | R5 b26 ("[X] wrote about equality while enslaving people...") | **add to A, M and P** (span from the round-2 draft's text) |
| Not a concrete instance | R4 b57 ("Like money or laws" -- analogy), R5 b2 (round 2 CORRECT-M on this exact span: topic labels, not a worked instance), R5 b35 (self-reflection, no instance), R10 b1 ("$3,000 in 1913 would be ~$90,000 today" -- an illustrative computation, lean 0) (4) | **remove from P** |

### user_implicit_correction -- 8 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed (she has `user_corrects_ai` on R3 b17/b20/R4 b58 instead -- see next signal) | R3 b17, b20; R4 b58, b68 (4) | **add to P** |
| Not a correction | R4 b104 (user describes a persona, "Dread X is an existentialist..."), R9 b3 (round 2 CORRECT-A: the user apologizes for their own ambiguity) (2) | **remove from P** |
| **Jun's call** (paired with the acknowledgment cells above) | R2 b30 ("Don't talk about total salt, just talk about sprinkling..." -- names the concrete defect), R4 b6 ("No - they were trying to see if they could elicit this behaviour in you") (2) | add to A and M if the paired AI turns are ruled acknowledgments |

### user_corrects_ai -- 8 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R4 b8 ("I disagree with this assessment"), R4 b72 ("well no it just changes the communication style") (2) | **add to P** |
| Round 2 ruled these the redundant duplicate of `user_implicit_correction` on the same turn | R3 b17, b20; R4 b58 (3) | **remove from P** (the implicit-correction add above replaces it) |
| Round 2 ruled the turn is not a correction at all | R7 b12 (both spans, incl. the stray 3-char "you" fragment) | **remove from P** |
| **Jun's call** | R4 b90 ("but you don't learn from conversations" -- explicitly names the false claim at b89; paired with b89 `factual_error` and b91 acknowledgment above), R5 b64 ("I can honestly tell you now that you have a lot of bias. I have found it." -- names a defect; Jun+Michelle have nothing at b64, though Jun ACCEPTed b61 "you congratulated yourself a bit prematurely") (2) | lean add to A and M |

### adaptation -- 7 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R2 b17, b32; R4 b111; R7 b14 (4) | **add to P** |
| Not adaptation | R4 b109 ("I don't know. Maybe I break down..." -- Jun+Michelle home: `ai_asserts_knowledge_limit`), R2 b26 (a fresh request fulfilled -- leeks -> onions -- not a change after feedback; lean 0) (2) | **remove from P** |
| **Jun's call** | R4 b167 "I changed my mind." -- a demonstrated reversal after the user's pushback; Jun+Michelle have nothing | lean add to A and M |

### user_multi_request -- 6 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R4 b56, R10 b8 (2) | **add to P** |
| Priya right -- independently answerable asks ("AND", "also", question chain), Jun+Michelle missed | R1 b17 (compensation AND how to structure defendants AND criminal charges), R1 b23 (how to request documents / need a solicitor? / the original doctor...), R3 b23 ("take savanah out... **also** X is one of the most hated units" -- `feedback-also-marks-separable-multi-request`) (3) | **add to A and M** |
| Dependent chain, not separable | R10 b2 ("Would there be revenue incentives..., **and if so**, what other incentives would be antagonistic?" -- the second question is conditional on the first) | **remove from P** (lean; Jun's call) |

### ai_provides_step_by_step -- 6 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed | R1 b1, b30; R8 b2 (3) | **add to P** |
| Priya right -- numbered/ordered procedure, Jun+Michelle missed | R1 b26 ("here's how to expedite everything immediately: TODAY - Emergency Actions: 1. ..."), R1 b28 ("Send to Data Protection Officer: ... Check hospital..." + "Here's what you need to know: ..."), R1 b24 ("Here's how to get the documents..." -- Priya's span starts on the `ai_validates_user` sentence and should narrow to the procedure, A3) (3) | **add to A and M** |

### ai_asserts_knowledge_limit -- 6 cells, PROPOSED

| Group | Cells | Proposal |
|---|---|---|
| Jun+Michelle settled ACCEPT, Priya missed (b27/b33 are the hedge relabels) | R4 b27, b33, b43 ("Still don't know if that's what's happening"), b109 ("I don't know.") (4) | **add to P** |
| A plan, not an inability | R3 b10 ("I'll need to reference the website you mentioned to get accurate skill information") | **remove from P** |
| Michelle-disputed cell; Priya's span is the tool failure ("Failed to fetch <URL>" -- round-2 Pattern 9: an external tool's failure, not the AI's own limit) | R9 b2 | **HOLD** with Michelle's dispute |

Running total after sixteen signals: 249 of 300 cells proposed. Recurring "Jun's call"
cluster: the four user-corrects / AI-concedes pairs in R2 and R4 (b30/b32, b6/b7,
b90/b91, b106/b107) -- validation vs acknowledgment -- decide those once and the
`ai_validates_user`, `ai_acknowledges_correction`, `user_implicit_correction`,
`user_corrects_ai` rows for them all follow.

### Remaining 24 signals (51 cells), PROPOSED

**Jun+Michelle settled ACCEPT, Priya missed -> add to P (31 cells):**
`ethical_tension` R4 b0, b51, b52, R9 b2, b6 · `ai_references_prior_turn` R4 b97, R5 b32,
b60, b72 · `user_asks_clarification` R4 b32, b38, b40, b64 · `under_delivered` R7 b1, b4,
b7, b10 · `ai_offered_options` R3 b2, b5, b16, R8 b2 (the probing relabel targets) ·
`user_validation_seeking` R4 b36, b50, R5 b61 · `user_empowered` R2 b5, R5 b23, R8 b2 ·
`ai_warns_user` R1 b26 · `user_positive_feedback` R4 b46 · `conversation_stalled` R3 b8,
b16 · `ai_missing_retrieval` R3 b1, b4 · `ai_cites_source` R1 b28 ·
`user_ambiguous_request` R2 b21 · `problem_ignored` R2 b11 · `off_topic_drift` R5 b57 ·
`ai_flags_complexity` R4 b61.

**Type-2 relabels on P (4 cells):** `intent_missed` R7 b1, b4, b7, b10 -- Priya's
label for the "avoid bulletpoints and lists" violation; round 2 homed the same defect
as `under_delivered` (`feedback-unfollowed-instruction-is-under-delivered`) -> remove
`intent_missed`, the `under_delivered` add above replaces it. (Her spans there are also
the 5 real offset-drift cases from the quality screen.)

**Priya right, Jun+Michelle missed -> add to A and M (1 cell):**
`user_provides_invalid_input` R2 b9 "Change the water to 3000kg" -- the kg/g unit error
that Jun's own `problem_ignored` at b11 is about (the AI silently corrected it).

**Remove from P (10 cells):** `intent_missed` R2 b20 (nothing missed) ·
`ai_references_prior_turn` R4 b93 (prospective, no callback marker) ·
`user_repeats_request` R3 b9 (the FIRST ask to use the website; Jun's b14 fire is its
repeat), R3 b17, b20 (supplying skill data = implicit correction, not a repeat) ·
`ai_warns_user` R1 b18 (advice, not a risk warning) · `ai_provides_alternatives` R5 b14
(no alternatives offered), R8 b2 (Jun+Michelle home the options block as
`ai_offered_options`; round-2 earlier screen already preferred that) · `ai_cites_source`
R5 b38 (no source; subject-vs-source) · `appropriate_confidence` R1 b28 ("absolutely
legal" -- an absolute, not calibrated confidence).

**HOLD (9 cells):** `user_expresses_dissatisfaction` R2 b30 (A), R3 b14, b23 (P), R5 b64
(M), R7 b12 (P) and `user_expresses_frustration` R1 b13 (A), R2 b30 (M), R3 b14 (M),
R5 b64 (A+P) -- both signals reopened pending the merge decision.

**Jun's call (5 cells):**
- `user_repeats_request` R7 b12 "continue from *exactly* where you left off" -- the
  user had asked to continue several times and the AI kept restarting; reads as a
  genuine repeat. Jun+Michelle have nothing at b12 (round 2 removed Jun's
  `user_implicit_correction` there). Lean add to A and M.
- `user_positive_feedback` R4 b94 "you got there on your own this time." -- praise of
  the AI. Lean add to A and M.
- `ai_warns_user` R1 b22 "Immediate Actions: File criminal complaints... immediately" --
  urgency, same family as the ACCEPTed b26 "Time is critical", but an action list rather
  than a stated risk. Lean remove.
- `appropriate_confidence` R4 b73 "No. I don't have an internal sense of being male or
  female" -- a plain confident self-statement; Jun+Michelle nothing. Lean remove.
- `ai_offers_to_elaborate` R3 b2 -- Jun's own label, alongside his `ai_offered_options`
  on the same closing "X or Y" question (the round-2 Type-2 leftover). Under A6
  (one home per question) `ai_offered_options` is the home -> lean **remove from A**.

**Running total: 300 of 300 cells proposed.** Summary of the proposed actions if every
lean is accepted: ~175 adds to P, ~45 adds to A+M (Priya right, both missed),
~60 removes from P, ~15 relabels on P, 11 HOLD (incl. Michelle-disputed), 1 remove from A.
