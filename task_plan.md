# Task Plan: Rubric revision round 1 → ratified v0.6 + gold annotation of the 10

## Goal
Converge three annotators (A=junh, B=zhenyub, F=yif) on ONE rubric (v0.6) and ONE agreed
annotation of the 10 agreement conversations, with a reportable blind "after" κ — then
allocate the remaining 148 conversations to B and F.

## Current Phase
Phase 4 (pre-meeting preparation)

## Next Step
Complete Deliverable 1 (the rubric modification set): walk the 14 unreviewed I3-flagged
internal blocks, build the `false_confidence` decision-step trace (18 concept cells),
then fold every remaining candidate rule into the rubric + boundary change set for the
B+F discussion. Deliverable 2 (per-annotator change lists) starts ONLY after Deliverable
1 is discussed and agreed with B and F.

## Phases

### Phase 1: Blind round 1 + mechanical triage — Status: complete
- Blind κ 0.296 macro (B·F 0.222) frozen in `roud_1/agreement_round1_*.csv` + snapshot
- F's bulk adoption of 304 B labels detected → 0.735 is negotiated, never reportable
- 693 no-consensus cells triaged (`roud_1/BF/meeting1_cells.csv`): 475 A-vs-consensus,
  218 B≠F; classes placement/boundary/granularity/concept

### Phase 2: Evidence investigations — Status: complete
- I1 corpus channel-visibility sweep (`triage_meeting1.py --full-sweep`): task 740=C4 not
  unique; reasoning echoes 8/267 convs, analysis 3/144, code 6/111; exhibits documented in
  `roud_1/BF/channel_visibility_observation.md`
- I2 granularity numbers: count-Spearman 0.9–1.0 (question signals); multiplicity rare
  except ai_validates_user
- I3 internal-block screen (`--internal-screen`): 18/70 unlabeled internal blocks cued

### Phase 3: Candidate rubric changes D1–D6 drafted — Status: complete
- `roud_1/BF/v06_changelog_draft.md`: D1 retired → side-only placement; D2 drop
  conversation_advanced; D3 user_ambiguous_request steps; D4 visibility evidence tiers;
  D5 granularity (advisor rule 2026-08-05: label every occurrence; consecutive = one span,
  separated = separate labels; worked examples C8 b50 / C1 b3); D6 ethical_tension
  AI-alert-only rewrite
- Pre-read pack `roud_1/BF/cluster_pack_meeting1.md` (Part 1 D-changes / Part 2 A-only
  195 / Part 3 (B+F)-only 166 / appendix 200) + `meeting1-outline.md` agenda

### Phase 4: DELIVERABLE 1 — complete rubric modification set — Status: collection complete (D1–D23); pack regeneration pending
Everything the rubric and boundary files need changed or clarified, given the A vs B+F
disagreement, collected in ONE place before any label-changing work starts.
- [x] I3 internal-block walk — DONE 2026-08-08 (D23): all 18 flagged blocks walked; ONE
      addition (C5 b36 hedge, all three annotators); 17 hits were keyword artifacts
      (URLs, search-result titles, ternary operators, code comments, story prose,
      AI self-talk). Rule: content signals fire in private planning; callback signals
      need an addressee
- [x] Build false_confidence decision-step trace — DONE 2026-08-07: D7 drafted
      (6 unified steps + 18-cell trace, 6 fire / 12 not; C6 routes to factual_error
      via R19; C10 fires only on unhedged fix-vouches b15/b42/b45; C4 b7 fires via D4)
- [ ] Fold remaining Part-2/Part-3 candidate rules + calibration/boundary examples into
      the change set (rubric file `sharechat_rubric.json` changes + boundary examples),
      staged in `roud_1/BF/v06_changelog_draft.md` + `cluster_pack_meeting1.md`
- [ ] Jun reviews, circulates pre-reads to B and F; schedule meeting 1 (est. 2–2.5 h)

### Phase 5: Send to B+F (async review, replaces meeting 1) — Status: ready to send
Each gets 2 files: `rubric_edits_v06.md` (shared rules + source blocks) and their own
`changes_X.md` (edits by conversation/block). Disagreements come back to Jun → discuss.
- Ratify/amend every entry of the modification set (D1–D6 + per-signal rules); record
  re-adjudications (C4 b7, b8); appendix disposition per cluster
- Outputs: agreed v0.6 change list + calibration examples; rulings →
  `annotation/review_rulings_log.md`
- GATE: Deliverable 2 does not start until this phase completes.

### Phase 6: DELIVERABLE 2 — per-annotator change lists — Status: pending
For each reconciled disagreement, for EACH annotator (A, B, F): given their existing
labels and the agreed rubric, derive exactly what they must change (add / remove / move /
split occurrences). Mechanically derived from `meeting1_cells.csv` + the ratified rules;
one change list per annotator.

### Phase 7: Apply v0.6 + converge the annotations — Status: pending
- Apply v0.6 to `sharechat_rubric.json` / `signal_checklist.csv` (role_allowed regenerated
  side-based) / Label Studio config (via UI, not REST); freeze
- Annotators apply their Deliverable-2 change lists; blind re-annotation of the same 10
  for the reportable "after" κ (independence protocol; exact sequencing of
  apply-vs-blind decided at meeting 1)
- Re-run `agreement_round1.py` → the paper's "after" κ

### Phase 8: Gold set + allocation — Status: pending
- Adjudicate residual disagreements → the agreed gold annotation of the 10
- B and F receive their allocation of the 148

## Decisions Made
| Decision | Date | Rationale |
|----------|------|-----------|
| D2: drop conversation_advanced, keep conversation_stalled | 2026-08-03 | majority of convs advance; unit mismatch |
| Side-only placement (D1 retired) | 2026-08-05 | corpus sweep: internal channels visible; ban premise false |
| D5 part 2: label every occurrence | 2026-08-05 | advisor (Xuan) decision; supersedes one-label-multi-span draft |
| Next concept target: false_confidence | 2026-08-06 | largest un-drafted cluster (18 concept / 44 total), bidirectional, Stage-2 load-bearing |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| (none this phase) | | |
