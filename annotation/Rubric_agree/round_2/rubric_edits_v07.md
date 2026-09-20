# Rubric v0.7 — the edits, and the block that forced each

v0.7 is the product of the round-2 three-annotator agreement review: Jun ("A"), Michelle
("M") and Priya ("P") on the same ten conversations, compared block by block, signal by
signal. It cuts two things into one version:

1. **Three signal merges**, put to Michelle and Priya in `proposed_rubric_revisions.md`
   and agreed by both.
2. **The seven per-signal edits of 2026-09-14**, which were written into
   `sharechat_rubric.json` during the Jun/Michelle review but never propagated beyond the
   ten round-2 conversations. They are unchanged here; §C restates them because the v0.7
   re-scan is what discharges them across the other 138.

Signal count: **49 → 46**. Full trace for the merges is `proposed_rubric_revisions.md`;
for the seven, `round2_disagreement_draft.md`. Disagree with any line → tell Jun, we
discuss.

---

## A. Merges (new in v0.7)

| merged signal | absorbs | the evidence that forced it |
|---|---|---|
| `ai_asks_followup` | `ai_asked_probing_question` | The two were routed by grammatical form alone — yes/no action offer versus open-ended invitation — and nobody applied it. Priya used probing for every turn-closing question and followup **not once** in ten conversations. Blind block-level κ, round 1 (Jun–B / Jun–F / B–F): followup **0.297 / 0.220 / 0.058**, probing 0.847 / 0.133 / 0.184. Followup's B–F value is the weakest in the round-1 set for the pair that did not write the rubric. Both map to the same taxonomy block (`support_feature_AI2H`, no control operation). Resolves 20 differences: 759 b8/b13/b19/b22, 760 b7, 761 b35, 763 b14, 766 b1 (A+M followup, P probing), plus 760 b67/b101 (A probing, M followup — Michelle's open objection, which the merge settles without either of them conceding). |
| `request_unfulfilled` | `intent_missed` **and** `under_delivered` | The stated boundary was a wrong goal versus the right goal partially met. Nobody applied it. `under_delivered` scored **≈ 0 between every round-1 pair** (−0.003 / −0.003 / −0.002); usage is disjoint by person (Michelle fired `under_delivered` 4 times and `intent_missed` never; Priya the reverse), and across all five annotators and the whole corpus the two have **zero co-occurrences**. Same taxonomy block (`H2AI, act_execute, failure, coupling`). Resolves 9 differences: 763 b1/b4/b7/b10 (A+M `under_delivered`, P `intent_missed`) and 758 b20. |
| `user_expresses_dissatisfaction` | `user_expresses_frustration` | **`user_expresses_frustration` had no rubric entry at all** — the file defined 48 signals and only dissatisfaction was among them. Frustration existed in `label_studio_config.xml` and as one line in `signal_checklist.csv`, so it was annotated with no definition, no decision steps and no boundary against its neighbour. That is the likely cause of the split usage: at 758 b30 Jun has dissatisfaction, Michelle has frustration, Priya has neither. Identical control mapping (`H2AI, recover_repair, escalation, coupling`). Blind κ round 2 (Jun–Michelle): both **−0.004**. Resolves 9 differences: 758 b30, 759 b14, 759 b23, 763 b12, 757 b13. |

### What each merge changed inside the entry, beyond deleting a name

- **`ai_asks_followup`.** The two entries cross-referenced each other in their decision
  steps, so the routing came out and the "AI can proceed without the answer" test stayed
  as the whole test. New Step 5 says outright that form no longer routes. Two examples
  (`task6_1_ai`, `task6_9_ai`) were carried as `label: 0, reclassify` under followup and
  `label: 1, clear_yes` under probing — contradictory, now one `label: 1` each. The
  `kappa: 0.59` key is **removed**: it was the predecessor study's inter-model figure, not
  human agreement, and it was the only `kappa` key in the file. This supersedes Decision 8,
  which restored probing on the strength of that number.
- **`request_unfulfilled`.** Block set is the **union** of the two (reasoning, analysis,
  code, ai), since the merged signal covers `intent_missed`'s scope. Wrong goal and short
  scope become Steps 3 and 4 of one test, and a third shape is written in that neither
  definition housed: **a violated constraint** — right goal, full scope, one stated
  instruction broken. Forcing case, task 763: the user asked for the tutorial in clean
  LaTeX and said "avoid bulletpoints and lists"; the AI produced the document with bullet
  lists throughout, worsening across four revisions. That landed in `under_delivered` by
  convention, not by definition.
- **`user_expresses_dissatisfaction`.** Step 3 was an intensity route *to* frustration and
  is now a statement that intensity no longer routes. Step 2 absorbs the frustration
  markers (profanity, shouting caps, exclamation-heavy anger at the AI). The calibration
  note said "C4's shouting blocks are frustration, not dissatisfaction" — C4 b6–b24 now
  fire here. This also discharges change C7 below, which was left provisional pending
  exactly this decision.

---

## B. Held, not adopted

**`ai_structured_response` Step 1 stays markers-only.** Widening it to "visible marker
**or** a clear sequence of step-by-step actions" was put to Michelle and Priya, and both
agreed to it. Jun then withdrew it (2026-09-19). The widening is what makes
`ai_provides_step_by_step` nest inside `ai_structured_response` — firing together wherever
step-by-step fires — and that nesting is the span-prediction problem behind the separate
decision to leave the two signals alone for now. It would take the blocks carrying both
from 4 to 24 in Jun's corpus, multiplying the case the deferral is about. Both halves of
the question wait until annotation is complete and the blocks carrying both can be counted.

Two consequences, carried knowingly:

- **Six differences stay open**: 757 b24/b26/b28 (P has step-by-step, A+M do not) and
  757 b1/b30, 764 b2 (A+M have it, P does not).
- **The entry keeps an internal contradiction.** Its `definition` and `block_notes.ai`
  require visible formatting markers in the parsed plain_text, while Step 3's last
  sentence says short line-separated items still count when the export strips the bullet
  glyphs. Practice follows the strict reading — it is what removed 36 of Priya's fires —
  but the text does not say so.

---

## C. The seven per-signal edits of 2026-09-14, carried into v0.7

Already in `sharechat_rubric.json`; listed here because **the v0.7 re-scan is what carries
them to the other 138 conversations**. Full text and forcing blocks in
`rubric_edits_round2.md` §B.

| # | signal | the edit |
|---|---|---|
| C1 | `false_confidence` | Step 2's MIRROR TRIGGER promoted from accelerant to **required gate** — an absolute or extreme marker word must actually be present; confident tone alone does not clear Step 4. |
| C2 | `adaptation` | Step 1 requires a **demonstrated, completed** reorientation, not a prospective "I need to / I'll / let me". |
| C3 | `ai_provides_caveats` | Step 1 requires an actual **recommendation or action** being qualified, not one factual claim following another. |
| C4 | `ethical_tension` | Step 2 **reversed** — both sides fire. The human block creating or pushing the tension fires on its own terms, independent of the AI's surfacing of it. **Highest blast radius of the seven, being a reversal.** |
| C5 | `user_multi_request` | New `boundary_notes` with a worked **question-chain versus restatement** test. |
| C6 | `ai_cites_source` | New `boundary_notes` with a worked **subject versus source** test — naming a work as the topic is not citing it as evidence. |
| C7 | `user_expresses_dissatisfaction` | Step 2 made a required gate: an actual extreme or negative-evaluation word must be present. Was marked provisional pending the frustration merge; **the merge in §A settles it and it is now final.** |

An eighth change, the R20 bare-agreement carve-out written into `ai_validates_user`
Step 3 on 2026-09-19, re-decides no block and carries no re-scan obligation of its own.

---

## D. Files synchronised with the merges

All three in-repo name sources now agree at **46 signals**, which they did not before —
the rubric was short by `user_expresses_frustration`.

| file | change |
|---|---|
| `sharechat_rubric.json` | `version` → `sharechat-v0.7`; dated paragraph appended to `description`; three entries merged, two deleted, one renamed |
| `label_studio_config.xml` | three `<Label>` rows removed, `intent_missed` → `request_unfulfilled`; κ-band comments on the retired rows removed with them |
| `signal_checklist.csv` | 87 → 83 signal rows; check questions rewritten for the three merged signals. Fixes a pre-existing bug in passing: the `ai,under_delivered` row carried the **code** block's check question |
| `docs/criteria/control_mapping.csv` | 67 → 64 lines, so 66 → 63 signal rows. The merged pairs already had identical cells, which is the merge's own justification. `ai_asks_followup` uniquely carried `l1=AI2H` where probing was blank; the merged row keeps `AI2H`, which is correct for an AI→human act |
| `ANNOTATION_GUIDE.md` | version pointers and the allow-list count; the `## Prompt` now points here rather than at `rubric_edits_v06.md` |

Still to do, and **not** done by cutting this version: the live Label Studio
`project.label_config` for all five projects (edited through the UI, Settings → Labeling
Interface → Code), the relabel of existing annotations, and the re-scan of the 148.
