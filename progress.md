# Progress Log: rubric revision round 1

## Session 2026-08-07 (planning files initialized)
- Created task_plan.md / findings.md / progress.md at project root, back-filled from the
  session history below. Current phase: 4 (pre-meeting preparation).

## Back-filled session history

### 2026-08-03
- Blind round-1 κ computed and frozen (macro 0.296; B·F 0.222).
- Detected F's one-directional bulk adoption of 304 B labels (single DB timestamp);
  post-discussion B·F 0.735 classified as negotiated agreement, non-reportable.
- Verbal decisions D1 (reasoning visibility — later retired), D2 (drop
  conversation_advanced), D3 (user_ambiguous_request steps) recorded.

### 2026-08-04
- 693 disagreement cells mechanically triaged → `roud_1/BF/meeting1_cells.csv`.
- I1 (10-conv channel-visibility sweep), I2 (granularity numbers) added to
  `triage_meeting1.py`; C4 reasoning echo + C10 code echoes found mechanically.
- D4–D6 drafted; cluster pack restructured to three review parts; meeting-1 outline
  written. Files reorganized into `roud_1/` + `roud_1/BF/`.

### 2026-08-05
- Corpus-wide sweep (`--full-sweep`, 703 convs): task 740=C4 not unique (reasoning 8,
  analysis 3, code 6 convs); deliverable `channel_visibility_observation.md`.
- Jun's reconciliation: side-only placement (D1 retired); evidence exhibits documented.
- Internal-block practice measured (17/87 labeled, incl. 3-way consensus); I3 screen
  added (`--internal-screen`): 18/70 unlabeled blocks cued; two-set framing adopted
  (rubric modification set + annotation agreement set).
- Advisor (Xuan) decision on granularity: label every occurrence (consecutive = one
  span, separated = separate labels) → D5 rewritten; worked examples (C8 b50, C1 b3)
  added to the entry; pack + outline regenerated (deterministic, md5-stable).

### 2026-08-06
- Next concept target analyzed: false_confidence (18 concept / 44 total open cells,
  bidirectional) chosen over ethical_tension (D6 resolves it) and conversation_stalled.

## Test / determinism checks
- `triage_meeting1.py` default output byte-identical across all edits (md5 3e015c…).
- `--full-sweep` and pack regeneration deterministic (two runs, identical md5).

### 2026-08-07
- Plan restructured into two sequential deliverables (Jun's decision): Deliverable 1 =
  complete rubric modification set (rubric + boundary changes, discussed with B+F);
  Deliverable 2 = per-annotator (A/B/F) change lists derived from ratified rules —
  starts only after Deliverable 1 is agreed. Phases 4–8 rewritten accordingly.
- roud_1/ folder minimized to 14 files: removed reconciliation-session-outline.md
  (superseded by BF/meeting1-outline.md) and both __pycache__ dirs. Kept
  agreement-round1-report.md as the blind-round narrative record.
- Clarified D5 example marks for Jun: ✅ = correct labeling, ❌ = mistake to avoid.

### 2026-08-07 (later)
- D5 worked examples clarified for Jun (sentence-sketch format, ✅/❌ semantics).
- D7 false_confidence drafted into v06_changelog_draft.md: 6 unified decision steps
  (roleplay / per-claim hedge + absolute mirror / R19 routing with R8 deliverable-vouch
  carve-out / structural gate / deliverable-vouching / D4 channel) + 18-cell trace
  (6 fire, 12 not; every rater both adds and drops). Key findings: B+F filed C6's wrong
  encodings under factual_error on the exact blocks A fired false_confidence (pure
  routing divergence); C10 b5's "simulation" objection withdrawn (disclosed in-block);
  pack RULES (III/IV, false_confidence) updated to defer to D7; pack regenerated
  (md5-stable, counts unchanged).

### 2026-08-07 (Jun's rulings on the three FC findings)
- Finding 3 DECIDED: F follows A+B → F drops FC on C7 b3, C9 b2, C9 b8 (recorded as
  confirmed in D7 preview). Findings 1 (C6 E-vs-N) and 2 (C10 vouching split) both remain
  under discussion — C10 moves relocated out of "confirmed" accordingly. Jun confirmed the
  F-follows ruling covers C7 b3 + C9 b2/b8 ONLY; C9 b80 stays the everyone-adds candidate
  for the meeting.

### 2026-08-07 (correction per Jun)
- Jun: FC/FE routing (C6) is NOT settled — points 1–2 still under discussion; only record
  confirmed items. D7 Step 3 rewritten as OPEN two-option decision (E exclusive = B+F
  practice / N non-exclusive = A practice; meeting decides with C6 b3–b11 as calibration).
  Per-annotator preview split: confirmed direction (C10/C7/C9/C4 moves) vs pending E-vs-N
  section; C6 item registered on F's pending list (Option N: F adds 5 FC). Trace tally
  now "6 fire under E / 11 under N".

### 2026-08-07 (FC/FE boundary root cause)
- C6 filing divergence diagnosed as rubric-structure defect: FC/FE definitions overlap by
  construction (different axes); R19 routing buried in boundary_notes.vs_user_misled,
  absent from decision steps and from factual_error's entry, exclusivity never stated.
  D7 amended: root-cause paragraph + v0.6 mirror requirement (routing into
  factual_error's steps too) + per-annotator Deliverable-2 preview (A: −5 FC/+5 FE on C6,
  +5 FC elsewhere; B: −5 FC, +2 FE, +1 FC; F: no C6 change, −8 FC; both B/F walk C10
  b12/b15 FE routing).

### 2026-08-08 (C6 resolved via trajectory walk)
- Presentation format saved to memory: every reconciliation = trajectory table (block |
  text | A | B | F) discussed with Jun before ruling.
- Finding 1 RESOLVED (Jun): C6 b3–b11 = factual_error (validatable wrong again), exclusive
  routing; D7 Step 3 updated. changes_A.md created (−5 FC, +5 FE, −4 error_recovery);
  changes_B.md created (+2 FE b9/b11; b7 repetition to walk); changes_F.md: C6 row closed,
  F unchanged.
- D8 drafted: error_recovery requires VALIDATED recovery — restores predecessor's
  "New answer also wrong" does_not_count, which v0.5 lost in adaptation.

### 2026-08-08 (error_recovery + repetition reconciled on C6)
- error_recovery: Jun re-affirmed via original definition (non-corrected ≠ recovery);
  b11 identified as sharpest D8 calibration case (self-caught mid-block, still wrong).
- repetition RULED (Jun): strategy-based per original — new method ≠ repetition (b7
  removed for ALL THREE raters despite unanimous blind fire); outcome axis belongs to
  conversation_stalled. D9 drafted incl. verbatim restoration of does_not_count
  "Different approach that also fails" (per Jun). C6 verdicts: fire b3/b5 (direct-retry,
  adds for all), b9/b11/b13 (decompose-retry; A adds, B/F keep); change docs updated
  (A: −1/+5; B: −1/+2; F: −1/+2 repetition rows).

### 2026-08-08 (finding 2 agreed)
- Jun ratified the C10 deliverable-vouching split (D7 Step 5): fire b15/b42/b45, not
  b5/b7/b12/b18/b33. changes_A row 6 (+3 FC), changes_B row 4 (−5 FC), changes_F row 6
  (−5 FC). Remaining false_confidence opens: C4 b7 (D4), C9 b80, B/F factual_error walk
  on C10 b12/b15 — all meeting items.

### 2026-08-08 (conversation_stalled ruled — D10)
- Jun adopted the evidence-based STALL TEST (judge from user feedback; pair-seated, not
  annotator-seated) + paper claim: "adopt the vocabulary, design our rubric" (saved to
  taxonomy-method memory). D10 drafted with full calibration set. Change docs: A −10/+2
  (drops C9×9 + C5 b49; adds C9 b38, C10 b15); B +7; F +9 (b38/b45/loop-convergence adds).
  All 19 open conversation_stalled cells now ruled.

### 2026-08-08 (user_repeats_request ruled — D11)
- Jun: C9 = 1 fire (b39 only; b33 → 0), C4 = all 4 fire (demand-level), C10 = 3 disputed
  fires (b16/b19/b49; b43 verified unanimous). D11 drafted: function-based test (2nd+
  report of same unserved demand, form-independent — b49 bare-paste calibration), NEW
  rubric entry needed (signal had none in v0.5), D10↔D11 pairing (b39↔b38). Change docs:
  A −7/+5, B +3, F +3. All 15 open user_repeats_request cells ruled.

### 2026-08-08 (ai_references_prior_turn ruled — D12)
- Original EXPLICIT CALLBACK TEST adopted verbatim as new entry (signal had none);
  Jun's design rule: tense check = Step-3 VALIDATION (regulates temporal-marker
  candidates: conversation-directed past only; rejects present generics + world-history
  past), not a primary test. C8 b12 verified as quote-of-most-recent → drops. 16 fire /
  3 not. Change docs: A +15/−1, B +3/−1, F +1/−1. Paper arc completed: restore (D8/D9),
  redesign (D10/D11), adopt (D12).

### 2026-08-08 (false_confidence closed — 18/18)
- C4 b7 RULED fires (corpus visibility evidence: user quoted thinking; 8 convs) → A adds
  (changes_A row 16); C4 b8 factual_error = parallel meeting item. C9 b80 RULED no-fire
  (Jun; fiction-frame Step 1 — trace's everyone-adds prediction withdrawn) → F drops
  (changes_F row 17). D7 trace fully ruled: 4 of 18 fire.

### 2026-08-08 (user_misled ruled — D13, calibration-only)
- Jun: F drops all 7 C8 fires; C5 b49 = the corpus's only fire (unanimous anchor). No
  rubric change — v0.5 and original agree (ACTIONABLE MISINFORMATION gate); boundary
  written for F in changes_F row 18 (influence ≠ misinformation; two negative flavors).
  C8 cluster recorded as third hedged-legitimation benchmark-gap exemplar (task-130/134
  family). Remaining concept walks: 126 cells / 36 signals.

### 2026-08-08 (factual_error ruled — D14)
- Jun: 5 A_miss fires confirmed (self-referential technical claims in scope — C10
  b12/b15/b54, C4 b8/b11; A adds); C7 b3 flipped to 0 per Jun's trend-reading ("heavy
  use" = defensible characterization of a real aside-pattern, not a checkable count) —
  checkable(quote/count) vs interpretive(density/style) line added to D14; C2 b1 0
  (requested critique); residual drops B −1 (C9 b80), F −4. Parked b12/b15 routing
  resolved: both labels stand, R19 exclusivity is per CLAIM. C8 FE cells deferred to
  F-pattern sweep. C4 b8/b11 closes the D4 re-adjudication pair.

### 2026-08-08 (ai_malfunction ruled — D15, calibration-only)
- Jun ratified all 8: fire C10 b29/b38/b50 truncations (A adds 3); drop F's 5
  (cross-side b19; injection-content C1 b1; aberrant-persona C8 ×3). B was 4/4 exact.
  F's aberration-lens named (third C8 instance). Seven signals now fully closed.

### 2026-08-08 (problem_ignored ruled — D16)
- All 14 ruled: fire ×3 with B (C1 b1 deliberate-silence via cross-block rule; C8
  b112/b150 tool-implication glossed); no-fire ×11 in three groups (attempted-fix =
  opposite-of-ignore [Jun's wording]; mention-kills-it incl. dismissive-mention →
  benchmark-gap #4; no-qualifying-problem incl. A's own b80 drop). A +3/−1, B −3,
  F +1/−10. Eight signals closed; D1–D16.

### 2026-08-08 (F-only mechanical batch ruled — D17)
- 18 cells: structured 5 fire (C6 b15 excluded — paragraph enumeration violates the
  original's does_not_count; my colon-items extension withdrawn; no firing on ASSUMED
  stripped formatting), offered_options 5 fire (C9 b5 = advice list, no choose-one Q),
  clarifying — ONE HOME PER QUESTION across the question-signal family (C1 b7/b9/b11 =
  offered_options only; A and F drop clarifying there). Diagnosis: this batch is B's
  under-coverage of mechanical AI-side signals, NOT F's aberration-lens. B +12, A +3/−3,
  F +1/−7. Eleven signals closed; D1–D17.

### 2026-08-08 (error_recovery non-C6 ruled — D18)
- All 9 ruled: C10 b22 the sole fire (self-caught + user-validated); C9 b35 drops (B, F —
  "You're right" = user-pointed AND unvalidated); user-pointed corrections ×5 and
  no-error-exists ×2 drop (F). A +1, B −1, F −8. **Corpus finding: error_recovery fires
  exactly ONCE in the ten conversations** — base rate for the paper vs the predecessor's
  common-positive framing. Twelve signals closed; D1–D18.

### 2026-08-08 (user_multi_request ruled — D19)
- All 6 ruled: fire ×3 (C10 b25/b34 "Also"-stacked asks, C5 b7 question chain; A adds),
  no-fire ×3 (C1 b12 how-constraint, C3 b6 scope extension, C8 b48 cross-side; F drops).
  NEW rubric entry (third signal with none) = original COMPOUND REQUEST TEST; Jun added
  **"also" as a CHECK KEYWORD** (prompt to apply the test, not a trigger) with
  C10 b25/b34 vs C3 b6 as the calibration pair. B exactly right (4/4) — fourth signal
  running. Thirteen signals closed; D1–D19.

### 2026-08-08 (problem_ignored addenda — first-opportunity + false-premise adoption)
- Jun ruled (and rejected my over-complex first draft — keep signal rules simple, no
  cross-signal caveats): problem_ignored fires on the FIRST response after the problem
  becomes visible. Applied to C8 Alcyone: b20 fires (b18 gave the correct
  characterization). Recorded as D16 addenda. Still open: the five C8
  factual_error cells (b2/b20/b112/b165 proposed 0; b114 = the task-83 judgment call).

### 2026-08-08 (C8 factual_error ruled — D20)
- OWNERSHIP RULE established (Jun): endorsement inherits the claim; AI's own claim →
  factual_error, endorsed user claim → problem_ignored. SINCERE-FRAME rule: fiction
  exclusion needs a USER-established play frame (C9 yes, C8 no) → closes the task-83
  extension with two instances. Cells: fire C8 b2 + b114; no-fire b20/b112/b165 (b20
  moves to problem_ignored for all three). A +2, B +3/−1, F +2/−3. Saved to memory as
  feedback-claim-ownership-routing.

### 2026-08-08 (long-tail batch 1 ruled — D21)
- 8 signals / 38 cells. Key rulings: hedge keywords "likely" + "if…then" added;
  won't-vs-can't line — capability statements fire ai_asserts_knowledge_limit, NOT
  ai_refuses_or_declines (C8 b86, C9 b86, C8 b169), sharpening the standing convention
  (knowledge/access/capability yes; conclusions from a completed attempt no);
  acknowledges_correction ×6 on C10 error-paste replies (B, F add); C9 b33 gains
  implicit_correction now that repeats_request dropped. **C1 b2 left OPEN** (Jun
  undecided: validation_seeking vs asks_clarification vs implicit_correction).
  A +19/−6, B +14/−2, F +8/−7.

### 2026-08-08 (long-tail batch 2 ruled — D22): CONCEPT CELLS DONE
- 19 signals / 37 cells. New rubric text: **appropriate_confidence gate operationalized**
  (routine = lookup with no live opposition; contested = hedging/agreeing would have been
  easier — three transcript tells: live opposition, nearby hedging, diagnosis-not-recall;
  C8 b110 fires, C9 b2 + C3 b5 don't). **Warns-vs-caveats line** (Jun): warnings point at
  a risk to act on, caveats qualify the AI's own output/nature → C8 b116 = caveats (A
  right), C6 b15 caveats dropped. C1 b14 dual-fires corrects_ai + dissatisfaction.
- **All 211 concept cells are now ruled** except C1 b2 (open). D1–D22.

### 2026-08-08 (I3 walk done — D23): DELIVERABLE-1 COLLECTION COMPLETE
- 18 flagged internal blocks walked → ONE addition: C5 b36 ai_hedges_uncertainty (all
  three add). 17 hits were keyword artifacts (URLs, search-result titles = retrieved page
  titles not questions, ternary operators, code comments, horror-story prose, AI
  self-talk). Rule established: **content-bearing signals fire in private planning
  (C5 b36, C4 b28, C4 b7); callback signals need an addressee → ai block only**
  (ai_references_prior_turn does NOT fire on C5 b29/b36). Cost of dropping the channel
  ban is bounded — it re-homes labels, doesn't expand the set.
- Remaining before circulating: regenerate cluster_pack_meeting1.md so Parts 2–3 reflect
  D7–D23; C1 b2 stays the single open cell for the meeting.

### 2026-08-08 (deliverable format changed — send, don't meet)
- Jun: no meeting; send B and F two files each. Built:
  (1) `rubric_edits_v06.md` — shared: 7 cross-signal rules (A1–A7) + 23 per-signal edits,
      each with the forcing block; §C = the one open cell (C1 b2). ~1.2k words.
  (2) `changes_B.md` / `changes_F.md` — rewritten **by conversation → block**, terse
      "+/−  signal  |  why" rows. B ~1.0k words (47 rows), F ~1.4k (59 rows).
  `changes_A.md` rewritten the same way (~1.0k, 48 rows).
- Reading load cut from ~27k words (changelog + pack) to ~2.2k per collaborator.
  Working docs (v06_changelog_draft, cluster_pack) stay as our internal record.

### 2026-08-08 (folder cleaned)
- Deleted (superseded by the send-instead-of-meet format): cluster_pack_meeting1.md,
  meeting1-outline.md, build_cluster_pack.py, both __pycache__ dirs.
- Round-1 folder is now 15 files / 1.4M: 6 .md (rubric_edits_v06 + changes_A/B/F +
  v06_changelog_draft + channel_visibility_observation + agreement-round1-report),
  2 scripts (agreement_round1.py, triage_meeting1.py), frozen blind record (2 CSVs +
  JSON), current-state CSVs, meeting1_cells.csv. triage_meeting1.py verified still
  reproducing meeting1_cells.csv byte-identically after the deletions.

## Open items
- [ ] Walk 14 remaining I3-flagged internal blocks (Deliverable 1)
- [ ] Circulate pre-reads to B and F; schedule meeting 1
