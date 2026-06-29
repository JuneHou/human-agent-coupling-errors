# Human Annotation Protocol — ShareChat Claude Corpus

*For ICLR methods section and reproducibility supplement.*

---

## 1. Task and annotators

**Annotation task:** Signal-level labeling of observable coupling behaviors in human-AI conversations. Each annotator reads one conversation and marks spans (sentence-level) with signals from the taxonomy. A signal is an observable behavior — not an interpretation — so that two annotators reading the same sentence should reach the same label.

**Annotators:** Graduate students in computer science with experience in NLP and human-computer interaction. All annotators are co-authors or direct collaborators on the project, ensuring domain familiarity with AI system behavior. No crowdsourcing platform was used.

**Training:** Each annotator completes the following before labeling live data:
1. Read `ANNOTATION_GUIDE.md` in full (~30 min)
2. Read `sharechat_rubric.json` for all signals to be labeled
3. Complete a 5-task calibration set (pre-labeled by the lead annotator with adjudicated gold labels)
4. Discuss boundary disagreements from the calibration set before proceeding

---

## 2. Corpus and task assignment

**Corpus:** 716 English conversations from the ShareChat Claude dataset (HuggingFace), filtered from 911 raw conversations by ≥50% English word content.

**Annotation target:** 148 conversations (w=0.5, power=0.90; see power analysis in `advisor-update.md`).

**Task assignment:**

| Phase | Conversations | Annotators per task | Purpose |
|---|---|---|---|
| Calibration | 5 | All annotators | Training; not included in analysis |
| Overlap set | 50 | All annotators independently | Inter-annotator agreement (κ computation) |
| Independent set | ~93 per annotator | 1 | Coverage toward n=148 |

The 50-conversation **overlap set** is annotated independently — annotators do not see each other's labels until after submission. These are used to compute per-signal Cohen's κ.

---

## 3. Annotation interface

Label Studio (v1.x), self-hosted on a shared university server. Each annotator has an individual account; Label Studio records which account submitted each annotation and timestamps every label.

Each task presents one conversation as a dialogue with paragraph-typed blocks (`human`, `ai`, `reasoning`, `analysis`, `code`). Annotators highlight sentence spans and select a signal from the taxonomy palette. A free-text TextArea is available for notes and uncertain cases.

Block placement rules enforce which signal categories are available per block type (e.g., user behavior signals appear only on `human` blocks; outcome signals only on `ai` blocks).

---

## 4. Inter-annotator agreement

**Metric:** Cohen's κ per signal, computed on the 50-conversation overlap set.

**Threshold:** κ ≥ 0.4 (Landis & Koch 1977 "moderate agreement") for inclusion in primary analysis. Signals below threshold are excluded from downstream statistics (not used for hypothesis testing or distribution analysis).

**κ computation unit:** Binary presence/absence per paragraph per conversation (not span-exact match). Two annotators agree on a signal for a conversation if both mark it present at least once in the same paragraph type.

**Reporting:** Mean κ across all primary signals, plus per-signal κ table in appendix. Signals with κ ≥ 0.6 (substantial) reported separately.

**Prior κ values:** Initial κ estimates come from the predecessor study (arXiv:2603.15423, Appendix C.3), which used the same signal set on a different corpus. These inform signal design and tier assignment but are not substituted for our measured κ.

---

## 5. Gold label adjudication

Gold labels are produced from the 50-conversation overlap set using the following protocol:

**Step 1 — Automatic agreement:** For each (conversation, paragraph, signal) triple, if all annotators agree (all mark or all skip), the label is accepted as gold directly.

**Step 2 — Majority vote:** If annotators disagree but a strict majority (>50%) agrees on presence or absence, the majority label is used.

**Step 3 — Adjudication:** Remaining disagreements (no majority) are resolved by the lead annotator (Jun) after reviewing all annotators' justifications and the relevant rubric entry. The adjudication decision and reasoning are logged in `signal-decisions.md`.

**Step 4 — Rubric update:** If adjudication reveals an ambiguous boundary not covered by the existing rubric, the rubric is updated before proceeding to the next batch. Annotators re-label any prior tasks affected by the clarification.

---

## 6. Quality control

**Per-task checks (before submission):**
- Every paragraph type reviewed
- Outcome signals (`conversation_advanced`, `conversation_stalled`) placed on `ai` block only
- Inline `<thinking>` content inside `ai` blocks: labeled only after `</thinking>` tag
- One signal per sentence span; uncertain cases have TextArea notes

**Batch-level checks (after every 10 tasks):**
- Lead annotator reviews signal frequency distribution for implausible shifts
- Any signal with zero occurrences in a batch flagged for rubric review
- Annotators discuss TextArea notes to surface emerging boundary cases

**Signal stability:** If measured κ for a signal falls below 0.4 on our corpus (despite prior κ ≥ 0.4), the signal definition is revisited. If κ remains below threshold after rubric revision, the signal is demoted to exploratory (Orange) and excluded from primary analysis. Demotion decisions are logged in `signal-decisions.md`.

---

## 7. Ethical considerations

All conversations in the ShareChat Claude dataset are user-generated and publicly released by the dataset authors under their stated license. No personally identifiable information beyond what is present in the original dataset is collected. No new human subjects are recruited for annotation beyond the research team.

---

## 8. Reproducibility

All annotation artifacts are versioned in the project GitHub repository:
- `annotation/label_studio_config.xml` — labeling interface (signal palette, block type rules)
- `annotation/sharechat_rubric.json` — per-signal decision rubric with examples
- `annotation/ANNOTATION_GUIDE.md` — full annotator guide
- `docs/methodology/signal-decisions.md` — log of all design decisions with rationale
- `annotation/data/annotation_input.json` — processed input tasks (716 conversations)

Label Studio annotation exports (JSON) will be released alongside the paper.

---

## 9. Annotation statistics (to be filled in)

| Metric | Value |
|---|---|
| Total annotators | TBD |
| Conversations in overlap set | 50 |
| Total labeled conversations | 148 (target) |
| Mean κ across primary signals | TBD |
| Signals above κ=0.6 (substantial) | TBD |
| Signals 0.4–0.6 (moderate) | TBD |
| Signals below κ=0.4 (excluded) | 15 (from predecessor study) + TBD new |
| Adjudicated disagreements | TBD |
| Mean annotation time per conversation | TBD |
