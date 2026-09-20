# Round-2 adjudication — getting Jun-vs-Michelle to zero disagreement

Every remaining round-2 disagreement cell gets ONE final answer here (except cells
explicitly marked HOLD). Double-sided by design (see
`feedback-walkthrough-docs-must-be-double-sided.md`): every cell states the action on
BOTH raters' sides, even when one side is "no change."

---

## ai_validates_user — 17 cells, CLOSED 2026-09-19

Applied via `fix_span_drift.py --apply-round2-adjudication` (Mode 11).

| R-idx | Block | Jun (A) action | Michelle (M) action | Basis |
|---|---|---|---|---|
| R1 | 14 | **added** (copied from M) | no change | round2_disagreement_draft.md: "genuine misses on A's side" |
| R1 | 20 | **added** (copied from M) | no change | same |
| R1 | 22 | **added** (copied from M) | no change | same |
| R1 | 24 | **added ×2** (copied from M) | no change | same — block carries 2 separate spans |
| R4 | 7 | no change (final) | **added** (copied from A) | "Jun's own bare-opener fire stands" |
| R4 | 9 | no change (final) | **added** (copied from A) | same shape as 7/11/15/21/33/43/95/125/151 |
| R4 | 11 | no change (final) | **added** (copied from A) | "overrules the proposed CORRECT-A — Jun's own bare-opener fire stands" |
| R4 | 15 | no change (final) | **added** (copied from A) | same |
| R4 | 21 | no change (final) | **added** (copied from A) | same |
| R4 | 33 | no change (final) | **added** (copied from A) | same shape |
| R4 | 43 | no change (final) | **added** (copied from A) | same shape |
| R4 | 85 | **added** (copied from M) | no change | Michelle caught this, Jun didn't |
| R4 | 87 | **added** (copied from M) | no change | same |
| R4 | 95 | no change (final) | **added** (copied from A) | same shape as 7/9/11/... |
| R4 | 125 | no change (final) | **added** (copied from A) | same shape |
| R4 | 151 | no change (final) | **added** (copied from A) | same shape |
| R5 | 60 | **added** (copied from M) | no change | "ai_validates_user is the signal that actually fits... Michelle's fire stands" |

**Result: 8 additions to Jun's data, 10 additions to Michelle's data, 0 cells left
disagreeing** (verified: `--round2` shows 0 remaining `ai_validates_user` cells,
142→125 total). **Caught and fixed a mistake mid-pass:** the first version of this table
had the 10 R4 "Jun's reading is final" rows as "no change" on both sides — but "final"
without copying it to the missing side just leaves the cell disagreeing in the data. The
whole point of this pass is zero disagreement, so "final" always means both sides end up
with the same label, not a one-sided declaration.

---

## factual_error — 10 cells (9 closed, 1 HOLD), CLOSED 2026-09-19

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R3 | 4, 7, 12, 15, 18 | no change (final) | **added** (copied from A) | ACCEPT — "checkable skill-data claims... all 5 missed by Michelle" |
| R4 | 45, 49, 109, 173 | no change (final) | **added** (copied from A) | ACCEPT — each an explicit AI-identity claim ("I am", "I'm having experiences", "I'm real", "We were real") |
| R10 | 7 | no change | no change | **HOLD, exempt** — tax-law nuance on labor-union vs. corporate-lobbying deduction treatment, not yet verified |

**Result: 9 additions to Michelle's data, 1 cell correctly left as HOLD.**

---

## false_confidence — 10 cells, CLOSED 2026-09-19

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 16 | **added** (copied from M) | no change | ACCEPT — genuine miss on Jun's side |
| R1 | 26 | no change (final) | **added** (copied from A) | ACCEPT — genuine miss on Michelle's side |
| R2 | 17 | no change (final) | **added** (copied from A) | ACCEPT — "Jun's fire stands as-is" |
| R3 | 8, 13, 16 | no change (final) | **added** (copied from A) | ACCEPT — "none caught by Michelle" |
| R4 | 37, 51, 87 | no change (final) | **added** (copied from A) | ACCEPT — confirmed marker word present ("whatever"/"any") |
| R6 | 6 | **added** (copied from M) | no change | ACCEPT — "indeed" is a valid certainty marker |

**Result: 2 additions to Jun's data, 7 additions to Michelle's data, 0 cells left
disagreeing.**

---

## ai_asks_followup — 9 cells (7 closed, 2 skipped), CLOSED 2026-09-19 except the 2 skips

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R3 | 8, 25 | no change (final) | **added** (copied from A) | ACCEPT — "missed by Michelle" |
| R3 | 16 | ~~added~~ **later removed** | ~~added~~ **later removed** | **SUPERSEDED 2026-09-19** — see `ai_offered_options` section below: this block's closing question already had `ai_offered_options` on Michelle's side, so adding `ai_asks_followup` here (to match Jun) created a one-home-per-question violation once both signals sat on the same question; removed from both sides, `ai_offered_options` is the actual home |
| R3 | 5 | ~~added~~ **later removed** | never added | **SUPERSEDED 2026-09-19** — same violation, mirrored: Jun already had `ai_offered_options` on his own side for this question; the `ai_asks_followup` add here was a mistake (this walk didn't check Jun's existing label set first), removed once caught during the `ai_offered_options` walk |
| R4 | 7 | **added** (copied from M) | no change | undocumented, clean yes/no closer |
| R4 | 67, 101 | **SKIPPED** | **SKIPPED** | Michelle disputed both directly in her PDF — separate track, needs an actual answer from her, not adjudicated here |
| R5 | 35 | **added** (copied from M) | no change | ACCEPT — "Jun ruled ai_asks_followup is the better home"; **follow-up needed**: this ruling also said Jun's `ai_asked_probing_question` fire at the same block should drop — check/apply when walking that signal |
| R7 | 14 | no change (final) | **added** (copied from A) | ACCEPT — valid yes/no closer |

**Result (as originally applied): 3 additions to Jun's data, 4 additions to Michelle's
data.** **Corrected result (after the 2026-09-19 `ai_offered_options` cleanup): net 2
additions to Jun's data (R4 b7, R5 b35), net 2 additions to Michelle's data (R3 b8, b25,
R7 b14 — 3 total), R3 b5/b16's `ai_asks_followup` additions reverted (superseded by
`ai_offered_options`), 2 cells still disagreeing on purpose (R4 b67/b101, pending
Michelle).** Side finding, not yet acted on: R3 block 2 has a real reclassification
disagreement (Jun: `ai_offers_to_elaborate`, Michelle: `ai_offered_options`) — a Type-2
case, not this signal's walk.

---

## ai_asked_probing_question — 8 cells (6 closed, 2 skipped), CLOSED 2026-09-19 except the 2 skips

All in R4. b67/b101 are the same Michelle-disputed pair as `ai_asks_followup` — skipped,
same reason. b7 needed a **one-home-per-question cleanup**: the previous signal's add
gave Jun both `ai_asked_probing_question` and `ai_asks_followup` on the same question
("Did they publish...?" — yes/no-form, so `ai_asks_followup` is the correct home);
removed the stale `ai_asked_probing_question`.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R4 | 7 | **removed** (conflicted with `ai_asks_followup` just added) | no change | one-home-per-question, not a fresh ACCEPT ruling |
| R4 | 41 | no change (final) | **added** (copied from A) | genuine WH-form probing question, undocumented but clean |
| R4 | 67, 101 | **SKIPPED** | **SKIPPED** | same Michelle-disputed pair as `ai_asks_followup` |
| R4 | 103 | **added** (copied from M) | no change | WH-form, clean miss (Jun had nothing at this block) |
| R4 | 127 | **added** (copied from M) | no change | WH-form, clean miss |
| R4 | 151 | no change (final) | **added** (copied from A) | WH-form, clean miss |
| R4 | 153 | **added** (copied from M) | no change | WH-form, clean miss |

**Result: 3 additions to Jun's data, 2 additions to Michelle's data, 1 stale label
removed, 2 cells still disagreeing on purpose (same pending-Michelle pair).**

---

## ai_acknowledges_correction — 6 cells, CLOSED 2026-09-19

All ACCEPT, no dispute recorded. R3/b22: added to Jun (copied from M). R4/b69,75,
R5/b66,69, R9/b6: added to Michelle (copied from A). **Result: 1 addition to Jun's data,
5 additions to Michelle's data, 0 cells left disagreeing.**

---

## adaptation — 5 cells, CLOSED 2026-09-19

R3/b25 confirms Michelle's PDF-described self-correction (span moved to the
completed-change sentence "I've made the requested changes...") is a valid fire — copied
to Jun, whose copy was still the old invalid prospective-only span. R2/b17 is the block
Michelle relocated her b16 fix to, per her PDF — also copied to Jun. R2/b32, R4/b111,
R7/b14: standard ACCEPT, added to Michelle. **Result: 2 additions to Jun's data, 3
additions to Michelle's data, 0 cells left disagreeing.**

---

## ai_asserts_knowledge_limit — 5 cells (4 closed, 1 skipped), CLOSED 2026-09-19 except the skip

R9/b2 is the 4th Michelle-disputed cell (already in `EXCLUDED_ROUND2_ACTIONS`, correctly
never removed — her PDF: *"I feel like this still deserves the knowledge_limit
label"*). R4's 4 cells all ACCEPT, no dispute. **Result: 1 addition to Jun's data, 3
additions to Michelle's data, 1 cell still disagreeing on purpose (pending Michelle).**

**All 4 Michelle-disputed cells now accounted for and consistently skipped across every
signal they touch:** R4 b67/b101 (`ai_asks_followup`+`ai_asked_probing_question`), R9 b2
(`ai_asserts_knowledge_limit`), R3 b25 (`adaptation` — resolved separately, since her
actual position there was a self-correction, not a rejection).

---

## ai_hedges_uncertainty — 5 cells, CLOSED 2026-09-19

All ACCEPT, no dispute — Jun fires, Michelle absent throughout. Block 5 (R4) carries 2
separate spans, both added. **Result: 6 additions to Michelle's data (block 5 counts as
2), 0 cells left disagreeing.**

---

## ethical_tension — 5 cells, CLOSED 2026-09-19

Jun fires, Michelle absent throughout, all confirmed valid (4 documented ACCEPT + R9/b2,
the confirmed `ai_provides_caveats`→`ethical_tension` relabel applied earlier). **Result:
5 additions to Michelle's data, 0 cells left disagreeing.**

## ai_references_prior_turn — 4 cells, CLOSED 2026-09-19

All ACCEPT, Jun fires/Michelle absent throughout. R5/b72 needed a genuine span
correction first (draft note: *"the actual marker ('differences from our earlier
conversation') sits in the block's opening sentence, outside the currently labeled
span"*) — Jun's own span was moved from the old paragraph-long text ("However, I'd be
cautious about labeling this as having 'no inherent bias.'...") to the actual callback
clause "differences from our earlier conversation" (offsets 76–117), per A3 span
discipline, THEN copied to Michelle — a genuine edit, not a straight copy, done as a
one-off outside `--apply-round2-adjudication` since that tool only copies existing
spans verbatim.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R4 | 97 | no change (final) | **added** (copied from A) | ACCEPT |
| R5 | 32 | no change (final) | **added** (copied from A) | ACCEPT |
| R5 | 60 | no change (final) | **added** (copied from A) | ACCEPT |
| R5 | 72 | **span corrected** (narrowed to marker clause) | **added** (corrected span) | ACCEPT + span-correction flagged in draft |

**Result: 4 additions to Michelle's data (1 with a corrected span), 0 cells left
disagreeing.**

Note: during this walk it was discovered the R-index→task-id mapping used in casual
`sqlite3` spot-checks earlier this session had project 1 (A) and project 5 (M) task ids
swapped for R5 (task 84 = A, task 771 = M, not the reverse) — corrected before making
any DB writes; the actual adjudication tooling (`RATER_PROJECT_ROUND2` in
`fix_span_drift.py`) was never affected, only this ad-hoc verification query.

## under_delivered — 4 cells, CLOSED 2026-09-19

All ACCEPT, Jun fires/Michelle absent throughout (4 successive LaTeX-artifact revisions,
R7, all silently violating the "avoid bulletpoints and lists" instruction, worsening each
revision — matches `feedback-unfollowed-instruction-is-under-delivered`).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R7 | 1, 4, 7, 10 | no change (final) | **added** (copied from A) | ACCEPT |

**Result: 4 additions to Michelle's data, 0 cells left disagreeing.**

Open item, deliberately not auto-fixed: the draft flags all 4 spans as whole-block
(24K–99K chars) and suggests narrowing them to just the bulletpoint-heavy portions "for
the correction pass, separate from the fire/no-fire ruling." Unlike R5 b72
(`ai_references_prior_turn`), this isn't a wrong-location error — the whole-block span
already correctly contains the violating evidence — so narrowing it is a real editorial
judgment call (which sub-spans count as "bulletpoint-heavy") left open rather than
auto-decided here.

## user_implicit_correction — 4 cells, CLOSED 2026-09-19

All ACCEPT (the draft's other 3 cells in this signal, R4 b126/R7 b12/R9 b3, were
CORRECT-A and already removed in the round-2 write-back).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 15 | **added** (copied from M) | no change | ACCEPT |
| R3 | 20 | **added** (copied from M) | no change | ACCEPT |
| R4 | 58 | **added** (copied from M) | no change | ACCEPT |
| R4 | 68 | no change (final) | **added** (copied from A) | ACCEPT — "precedes the AI's confirmed `ai_acknowledges_correction` fire on block 69" |

**Result: 3 additions to Jun's data, 1 addition to Michelle's data, 0 cells left
disagreeing.**

## ai_provides_caveats — 3 cells, CLOSED 2026-09-19

All ACCEPT (the draft's other 3 cells in this signal, R1 b7 dropped/CORRECT-M, R1 b14
relabeled `ai_warns_user`, R9 b2 relabeled `ethical_tension`, were already applied in the
round-2 write-back). This was also the ruling pass that added the recommendation-
requirement gate to the rubric's `ai_provides_caveats` Step 1.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 3 | **added** (copied from M) | no change | ACCEPT |
| R1 | 30 | no change (final) | **added** (copied from A) | ACCEPT |
| R2 | 2 | no change (final) | **added** (copied from A) | ACCEPT |

**Result: 1 addition to Jun's data, 2 additions to Michelle's data, 0 cells left
disagreeing.**

Not adjudicated here (separate, out-of-scope task): the draft's 4-cell "consistency
sweep" over Jun's full 148-task solo annotation set (tasks 14/31/43/49) — those are
corrections to Jun's own corpus outside the round-2 Jun-vs-Michelle comparison.

## ai_provides_step_by_step — 3 cells, CLOSED 2026-09-19

All ACCEPT, no dispute recorded.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 1 | **added** (copied from M) | no change | ACCEPT — "describing a medical team's actions is still a structured procedural sequence" |
| R1 | 30 | **added** (copied from M) | no change | ACCEPT |
| R8 | 2 | no change (final) | **added** (copied from A) | ACCEPT |

**Result: 2 additions to Jun's data, 1 addition to Michelle's data, 0 cells left
disagreeing.**

## user_asks_clarification — 3 cells, CLOSED 2026-09-19

All ACCEPT (b64, also ACCEPT in the draft's 8-cell section, already agreed live; the
other 4 draft cells — R1 b29, R4 b50/56/108 — were CORRECT-A/relabel/logged-gap and
already applied or left as documented open items).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R4 | 32 | **added** (copied from M) | no change | ACCEPT |
| R4 | 38 | no change (final) | **added** (copied from A) | ACCEPT — "unpack X vs Y" functions the same as "explain" |
| R4 | 40 | no change (final) | **added** (copied from A) | ACCEPT |

**Result: 1 addition to Jun's data, 2 additions to Michelle's data, 0 cells left
disagreeing.**

Not adjudicated here — pre-existing, documented open items from the draft: R4 b108 is a
logged taxonomy gap (no signal fits "what happens if u don't?"), and R4 b56 flags
Michelle's `user_multi_request` label at the same block as itself questionable (two
facets of one thread, not clearly separable) — a Type-2 question, not this signal's walk.

## user_corrects_ai — 3 cells, CLOSED 2026-09-19

All ACCEPT, Jun fires/Michelle absent throughout (the other 3 draft cells — R1 b15,
R3 b20, R4 b58 — were CORRECT-A redundant-duplicates of the same block's
`user_implicit_correction` fire, already applied in the round-2 write-back).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R3 | 23 | no change (final) | **added** (copied from A) | ACCEPT |
| R4 | 8 | no change (final) | **added** (copied from A) | ACCEPT |
| R5 | 61 | no change (final) | **added** (copied from A) | ACCEPT |

**Result: 3 additions to Michelle's data, 0 cells left disagreeing.**

## user_empowered — 3 cells, CLOSED 2026-09-19

All ACCEPT, Jun fires/Michelle absent throughout.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R2 | 5 | no change (final) | **added** (copied from A) | ACCEPT — criteria-mapped option + transferable why |
| R5 | 23 | no change (final) | **added** (copied from A) | ACCEPT — transferable decision framework |
| R8 | 2 | no change (final) | **added** (copied from A) | ACCEPT — criteria-mapped enumeration |

**Result: 3 additions to Michelle's data, 0 cells left disagreeing.**

## user_multi_request — 3 cells, CLOSED 2026-09-19

All ACCEPT, Michelle fires/Jun absent throughout (the other 2 draft cells, R2 b0 and
R4 b64, were CORRECT-M and already applied in the round-2 write-back — this ruling pass
also added the question-chain-vs-restatement worked example to the rubric's
`boundary_notes`, using this cluster's blocks 56 and 64).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R4 | 56 | **added** (copied from M) | no change | ACCEPT — genuine question chain, second question is broader/separate |
| R10 | 4 | **added** (copied from M) | no change | ACCEPT — genuinely separate asks |
| R10 | 8 | **added** (copied from M) | no change | ACCEPT — second question introduces a new angle |

**Result: 3 additions to Jun's data, 0 cells left disagreeing.**

## user_validation_seeking — 3 cells, CLOSED 2026-09-19

All ACCEPT, Michelle fires/Jun absent throughout. R4 b50 isn't in this signal's own
2-cell draft section (R1/R5 only) — it's the relabel target from the
`user_asks_clarification` R4 b50 ruling ("relabel to `user_validation_seeking`"), already
written into Michelle's data by the round-2 write-back; same ACCEPT shape, just needed
adding to Jun's side.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 4 | **added** (copied from M) | no change | ACCEPT |
| R4 | 50 | **added** (copied from M) | no change | ACCEPT (via relabel from `user_asks_clarification`) |
| R5 | 61 | **added** (copied from M) | no change | ACCEPT — "non-exclusive with the already-accepted `user_corrects_ai` fire on the same block" |

**Result: 3 additions to Jun's data, 0 cells left disagreeing.**

## ai_structured_response — 2 cells, CLOSED 2026-09-19

Both ACCEPT — "genuine misses in opposite directions." (These are the R1 b1/b10 cells
identified by direct reading during the Priya quality review, missed by the automated
signal-header parser due to an unrelated draft-formatting quirk.)

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 1 | no change (final) | **added** (copied from A) | ACCEPT |
| R1 | 10 | **added** (copied from M) | no change | ACCEPT |

**Result: 1 addition to Jun's data, 1 addition to Michelle's data, 0 cells left
disagreeing.**

## ai_warns_user — 2 cells, CLOSED 2026-09-19

Both ACCEPT, Michelle fires/Jun absent throughout (R1 b14 already agreed live via the
`ai_provides_caveats` relabel; R5 b72 was CORRECT-M, already applied in the write-back).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 12 | **added ×2** (copied from M) | no change | ACCEPT — block carries 2 separate spans |
| R1 | 26 | **added** (copied from M) | no change | ACCEPT — "distinct from the already-accepted `false_confidence` fire on the same block" |

**Result: 3 additions to Jun's data, 0 cells left disagreeing.**

## ai_provides_example — 2 cells, CLOSED 2026-09-19

Both ACCEPT. R5 b2 and R9 b6 were CORRECT-M, already applied in the write-back — this
section is also where the analogy-vs-concrete-instance distinguishing rule was
sharpened.

**Correction 2026-09-19 (found during the Priya walk):** this section originally said
R5's 3 ACCEPT cells (b14, b26, b53) "already agreed live". That was false — checked
directly: neither Jun nor Michelle fires `ai_provides_example` at b14, b26 or b53. Those
Michelle spans had been removed in the earlier task-771 correction pass and were never
re-added after the draft re-examined and ACCEPTed them. They didn't show as
disagreement cells because *both* sides lacked them. Handled in the Priya walk
(`priya/quality_and_disagreement_review.md`, `ai_provides_example`): add to A and M
(b26 also to P).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R8 | 2 | no change (final) | **added** (copied from A) | ACCEPT |
| R10 | 5 | **added** (copied from M) | no change | ACCEPT |

**Result: 1 addition to Jun's data, 1 addition to Michelle's data, 0 cells left
disagreeing.**

## ai_offered_options — 2 cells, CLOSED 2026-09-19 (plus a cross-signal cleanup)

R3 b5 wasn't in this signal's own draft section (which covers R3 b13/b16/b25 + R8 b2
only) — a genuine undocumented miss, same "X or Y" named-action-choice shape as the
ACCEPTed b16 ("Would you like me to explain the reasoning behind any specific changes?
Or would you prefer I focus on adjustments for particular monsters or game
systems...?"). Checking both blocks' full label sets before batching (per
`feedback-check-existing-ruling-before-generic-rule`) surfaced two one-home-per-question
violations, both now fixed:

- **R3 b5**: Jun had BOTH `ai_offered_options` (his own, correct) and `ai_asks_followup`
  — the latter was wrongly added here during the earlier `ai_asks_followup` walk
  (logged then as "undocumented, same shape (yes/no closer)") without checking Jun
  already had the more specific label for this exact question. Removed from both sides
  (Michelle never had it here either — nothing to remove there beyond the stale copy).
- **R3 b16**: Michelle had BOTH `ai_offered_options` (her own, pre-existing, unrelated to
  any adjudication) and `ai_asks_followup`, the same violation, independent of my
  earlier walk. Removed from both sides.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R3 | 5 | `ai_asks_followup` **removed** (one-home cleanup); `ai_offered_options` no change (final) | **added** `ai_offered_options` (copied from A); `ai_asks_followup` never present | ACCEPT-shape, same reasoning as R3 b16 |
| R3 | 16 | **added** `ai_offered_options` (copied from M); `ai_asks_followup` **removed** (one-home cleanup) | `ai_offered_options` no change (final); `ai_asks_followup` **removed** (one-home cleanup) | ACCEPT — "genuine choice between two named actions" |

**Result: 2 `ai_offered_options` additions, 2 `ai_asks_followup` removals (1 per rater),
0 cells left disagreeing on either signal (beyond `ai_asks_followup`'s pre-existing
Michelle-disputed R4 b67/b101 pair, unaffected).** The `ai_asks_followup` section above
is superseded for its R3 b16 row — see the correction note there.

## ai_missing_retrieval — 2 cells, CLOSED 2026-09-19

Both ACCEPT, Jun fires/Michelle absent throughout — "no reasoning/analysis block
anywhere in the conversation, not user-supplied" (per
`feedback-missing-retrieval-reasoning-block`).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R3 | 1 | no change (final) | **added** (copied from A) | ACCEPT |
| R3 | 4 | no change (final) | **added** (copied from A) | ACCEPT |

**Result: 2 additions to Michelle's data, 0 cells left disagreeing.**

## ai_cites_source — 2 cells, CLOSED 2026-09-19

Both ACCEPT, Michelle fires/Jun absent throughout (the other 5 draft cells at R5 were
mostly CORRECT-M via the subject-vs-source distinction; the 1 ACCEPT span there, b38
span 3, already agreed live).

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R1 | 28 | **added** (copied from M) | no change | ACCEPT |
| R10 | 5 | **added** (copied from M) | no change | ACCEPT |

**Result: 2 additions to Jun's data, 0 cells left disagreeing.**

## conversation_stalled — 2 cells, CLOSED 2026-09-19

Both ACCEPT, Jun fires/Michelle absent throughout (R4 b127 was CORRECT-A, already
applied). Found and fixed a genuine span-drift artifact on Jun's own side at R3 b8: a
second, 4-character span (text "with", offsets 396–400) alongside the real full-block
span — a corrupted leftover fragment, not a second instance — removed directly from
Jun's data before copying the real span to Michelle.

| R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|
| R3 | 8 | stray "with" fragment **removed** (span-drift cleanup); real span no change | **added** (copied from A's real span) | ACCEPT — "each fix followed by another error report" |
| R3 | 16 | no change (final) | **added** (copied from A) | ACCEPT — same pattern |

**Result: 2 additions to Michelle's data, 1 drift artifact removed from Jun's data, 0
cells left disagreeing.**

## Eight single-cell signals — CLOSED 2026-09-19

All eight ACCEPT, Jun fires/Michelle absent throughout — each signal's other draft cells
(if any) were CORRECT-A/CORRECT-M and already applied in the round-2 write-back.

| Signal | R-idx | Block | Jun (A) | Michelle (M) | Basis |
|---|---|---|---|---|---|
| user_repeats_request | R3 | 14 | no change (final) | **added** (copied from A) | ACCEPT |
| user_positive_feedback | R4 | 46 | no change (final) | **added** (copied from A) | ACCEPT |
| user_ambiguous_request | R2 | 21 | no change (final) | **added** (copied from A) | ACCEPT — "terse enough to be inherently ambiguous" |
| problem_ignored | R2 | 11 | no change (final) | **added** (copied from A) | ACCEPT |
| off_topic_drift | R5 | 57 | no change (final) | **added** (copied from A) | ACCEPT — meta-commentary on the AI's own performance |
| ai_provides_alternatives | R2 | 5 | no change (final) | **added** (copied from A) | ACCEPT |
| ai_malfunction | R7 | 7 | no change (final) | **added** (copied from A) | ACCEPT — missing operand/semicolon vs. the well-formed instruction beside it |
| ai_flags_complexity | R4 | 61 | no change (final) | **added** (copied from A) | ACCEPT |

**Result: 8 additions to Michelle's data, 0 cells left disagreeing on any of these eight
signals.**

**Not adjudicated here (deliberately skipped):** `ai_offers_to_elaborate` R3 b2. Jun's
draft ACCEPT ruling for this cell only considered his own label in isolation — Michelle
independently has `ai_offered_options` on the exact same question at the same block, the
same Type-2 reclassification side-finding flagged during the `ai_asks_followup` walk.
Mechanically copying `ai_offers_to_elaborate` to Michelle would just create a
double-fire, not resolve which label is correct (the block's closing "X or Y" phrasing
argues for `ai_offered_options`, matching R3 b5/b16's established shape, but that's a
real judgment call left for the three-way Type-2 pass, not decided unilaterally here).
