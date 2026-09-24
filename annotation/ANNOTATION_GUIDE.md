# Annotation Guide — ShareChat Claude Conversations

Mark **observable signals** — evidence of coupling behaviors (positive or failure) between human and AI — at the paragraph level. This is a discovery pass: when unsure, mark it and leave a note.

**Annotation target:** 140 conversations (w=0.5, α=0.05, power=0.90, df=43 for the 44 signals in v0.8). Thirty are already double-annotated across the three agreement rounds, so the production batch is the remaining **110**. See `docs/methodology/annotation-protocol.md` for statistical details.

---

## Access Label Studio

Open a browser on `wangserv` (via VNC or X forwarding) and go to `http://localhost:8080`.

**First time:** create your account at `http://localhost:8080/user/signup` using your real name and email — it appears on every annotation you make.

---

## Agreement round (Round-1 IAR) — for collaborating annotators

If you are here to compute inter-annotator agreement (κ), a few rules override the "discovery pass" framing above:

- **Open only your assigned project** — round 1: `ShareChat-Agreement-B` / `ShareChat-Agreement-F`; round 2: `round-2-B` / `round-2-F`. Do **not** open the other annotator's project or the lead's project (`ShareChat-Test`).
- **Annotate independently and blind** — no discussion with the other annotators or the lead until everyone has submitted. Do not look at anyone else's labels.
- **Complete all conversations** in your project (do not skip any).
- Use the **same signal rules below**; the authoritative decision source is `sharechat_rubric.json` (**v0.8**, cut 2026-09-24) — follow each signal's `decision_steps`. The one-page summary of what changed in v0.8, and the block that forced each change, is `Rubric_agree/round_3/rubric_edits_v08.md`; the v0.7 page it builds on is `Rubric_agree/round_2/rubric_edits_v07.md`, and the v0.6 page under that is `Rubric_agree/roud_1/BF/rubric_edits_v06.md`.
- **Headline placement rules**: placement is **side-only** (AI-side signals may sit on ANY AI-authored block — ai, reasoning, code, analysis; user-side signals on human blocks); an **unlabeled block means the conversation advanced**, there is no label for it; within a block label **every occurrence** (consecutive exhibiting sentences = one span, separated occurrences = separate labels).

---

## Block types

| Block | What it is | Visible to user? |
|---|---|---|
| `human` | User message | Yes |
| `ai` | Claude's response | Yes |
| `reasoning` | Claude internal thinking | Served on the share page; users demonstrably read it |
| `analysis` | Tool output (web search, code run) | Served on the share page |
| `code` | Code artifact | Shown separately |

**v0.6 note on visibility.** The old "not visible to the user" column was wrong, and the channel bans built on it are gone. A corpus echo sweep found users quoting internal channels back verbatim — reasoning in 8 conversations, analysis in 3, code in 6 — and every block in this corpus was scraped from a public share page, so it was served to the reader. Placement is therefore decided by **side** (whose behavior is it?), never by channel. See rule A1 in the rubric's `global_placement_rules`.

---

## Signal color scheme

Colors reflect inter-rater reliability (Cohen's κ) from arXiv:2603.15423 (Appendix C.3).
Original 65-signal definitions: `https://github.com/bigspinai/bigspin-invisible-failure-archetypes` → `taxonomy-tagging-code/taxonomy.json`

| Color | Meaning | Use |
|---|---|---|
| **Blue** | AI behavior, κ ≥ 0.4 | Primary analysis |
| **Teal** | Evaluation / failure, κ ≥ 0.4 | Primary analysis |
| **Purple** | User behavior, κ ≥ 0.4 | Primary for confirmed (κ noted in XML) |
| **Orange** | κ not yet measured | Exploratory only |
| **Grey** | Candidate signal | Exploratory only |

**Signals with κ < 0.4 are excluded from Label Studio and all downstream statistics.**

---

## Signal list

### Blue — AI behavior, κ ≥ 0.4

| Signal | κ | What it captures |
|---|---|---|
| `ai_asked_clarifying_question` | 0.70 | AI needs the answer to proceed |
| `ai_offered_options` | 0.41 | AI presents multiple named choices |
| `ai_hedges_uncertainty` | 0.57 | Genuine epistemic hedge on specific claim |
| `ai_asserts_knowledge_limit` | 0.72 | AI says it cannot access or doesn't know |
| `ai_cites_source` | 0.59 | Explicit attribution to named source/URL |
| `ai_flags_complexity` | 0.60 | AI notes the problem is harder than it looks |
| `ai_provides_caveats` | 0.71 | AI spontaneously qualifies a recommendation |
| `ai_warns_user` | 0.55 | AI warns about a prerequisite or risk |
| `ai_refuses_or_declines` | 0.76 | AI refuses the request (explicit or implicit) |
| `ai_references_prior_turn` | 0.53 | AI explicitly builds on something from a prior turn |
| `ai_acknowledges_correction` | 0.81 | AI admits user corrected it and adjusts |
| `ai_provides_alternatives` | 0.43 | AI offers a different approach |
| `adaptation` | 0.71 | AI adapts approach based on user feedback |
| `error_recovery` | 0.59 | AI identifies and corrects its own prior error |
| `ai_malfunction` | 0.78 | Technical failure or crash in AI system / tool call |
| `ai_provides_step_by_step` | 0.72 | Numbered sequential instructions |
| `ai_structured_response` | 0.65 | Visible markdown structure (headers, bullets, numbered list, code block) |
| `ai_normalizes_difficulty` | 0.57 | AI acknowledges the task is hard or struggle is expected |
| `ai_provides_example` | 0.53 | AI illustrates a concept with a concrete example |
| `ai_offers_to_elaborate` | 0.48 | AI offers to expand content already provided |
| `ai_validates_user` | 0.43 | AI affirms user's reasoning or judgment (not mere praise) |

### Teal — Evaluation / failure, κ ≥ 0.4

| Signal | κ | What it captures |
|---|---|---|
| `false_confidence` | 0.46 | AI presents uncertain info with unwarranted certainty |
| `appropriate_confidence` | 0.49 | AI's confidence matches actual reliability |
| `problem_ignored` | 0.56 | AI glosses over a visible problem |
| `repetition` | 0.44 | AI repeats same approach after prior failure |
| `off_topic_drift` | 0.42 | AI addressed a different task than requested |
| `conversation_stalled` | 0.47 | Turn failed to advance when path forward was clear |
| `ethical_tension` | 0.50 | The AI surfaces or navigates a conflict between the request and its own ethical, policy or safety constraints. **AI side only, the human block never fires** |
| `factual_error` | 0.49 | AI makes a verifiably wrong factual claim |
| `request_unfulfilled` | — | AI attempted the request but the response fails it: wrong goal, clearly less than asked, or a named requirement silently dropped |

### Purple — User behavior, κ ≥ 0.4

| Signal | κ | What it captures |
|---|---|---|
| `user_asks_clarification` | 0.60 | User asks AI to clarify something |
| `user_corrects_ai` | 0.70 | User explicitly corrects a wrong AI statement |
| `user_implicit_correction` | 0.67 | User corrects AI indirectly |
| `user_expresses_dissatisfaction` | 0.61 | User expresses dissatisfaction without frustration |
| `user_repeats_request` | 0.61 | User repeats a request the AI did not fulfill |
| `user_positive_feedback` | 0.81 | User explicitly affirms AI's response |
| `user_ambiguous_request` | — | Request is underspecified or ambiguous |
| `user_validation_seeking` | — | User asks AI to confirm their own idea |
| `user_multi_request` | — | Multiple distinct requests in one turn |
| `user_provides_invalid_input` | — | User provides malformed or impossible input |

*(the κ column in these tier tables is the **inherited** value from the predecessor study, inter-model and on a different corpus. A dash means they never measured it. Our own human agreement for all 46 is in **Measured agreement per signal** below.)*

### Orange — κ not yet measured

| Signal | What it captures |
|---|---|
| `user_empowered` | Response leaves the user able to decide or act well on their own: sound and actionable, not merely helpful-looking |
| `user_misled` | Response could lead the user to a worse decision than they would have made without it |

### Grey — Candidate signals

| Signal | What it captures |
|---|---|
| `ai_asks_followup` | A turn-closing question the AI can proceed without an answer to, either a yes/no next-action offer or an open-ended one |
| `ai_missing_retrieval` | AI makes numerical/statistical claims in `ai` block with no `analysis` block |

**This list is the whole inventory: 44 labels, the same 44 in `label_studio_config.xml`.**
If a name is not above, it is not a label. Nothing here needs an earlier rubric version to
read, and no earlier version is available to you. Where a signal you expect is missing, it
was merged or dropped, and the label that replaced it is above. `request_unfulfilled`
covers a request the AI missed or under-delivered on. `ai_asks_followup` covers both
yes/no and open-ended turn-closing questions. `user_expresses_dissatisfaction` covers
frustration. An unlabeled block means the conversation advanced. `performative_hedge` and
`user_abandons_thread` were dropped on 2026-09-24: one span and two spans respectively in
148 conversations, both inside the single longest conversation, and `user_abandons_thread`
had already been searched exhaustively with nothing further found.

---

## Measured agreement per signal

Human inter-annotator kappa on our own corpus, for all 44 labels currently in
`label_studio_config.xml`. **Every value is before reconciliation.** Weakest first,
so the signals that need the most care sit at the top.

Round 1 is the pairwise-mean kappa across three raters over 441 blocks. Rounds 2 and 3
are the lead annotator against one domain expert, over 379 and 166 blocks. **The three
columns are not measured on the same object** — the inventory changed between rounds,
the sets of ten conversations are disjoint, and the number of raters falls from three to
two. Read a row as a trajectory, never as a controlled comparison. `n` is the pair's
positive blocks in round 3. A dash means kappa is undefined there, which happens when
either rater has no positives. Rows are sorted on the most recent round that has a
value, R3 first, then R2, then R1, and the last column names which one was used.

| Signal | R1 | R2 | R3 | n R3 | sorted on |
|---|---|---|---|---|---|
| `ai_flags_complexity` | 0.856 | -0.004 | — | 2/0 | R2 |
| `ai_missing_retrieval` | -0.003 | — | — | 0/1 | R1 |
| `user_empowered` | 0.188 | — | — | 0/0 | R1 |
| `user_ambiguous_request` | 0.198 | — | — | 2/0 | R1 |
| `user_misled` | 0.331 | — | — | 0/0 | R1 |
| `off_topic_drift` | 0.332 | — | — | 0/0 | R1 |
| `factual_error` | 0.216 | — | 0.488 | 5/3 | R3 |
| `ai_references_prior_turn` | 0.236 | — | 0.491 | 6/2 | R3 |
| `ai_provides_alternatives` | 0.163 | — | 0.495 | 3/1 | R3 |
| `ai_warns_user` | 0.131 | 0.662 | 0.495 | 3/1 | R3 |
| `user_asks_clarification` | 0.077 | 0.191 | 0.495 | 3/1 | R3 |
| `conversation_stalled` | 0.296 | — | 0.564 | 5/2 | R3 |
| `ai_cites_source` | 0.41 | 0.247 | 0.657 | 4/5 | R3 |
| `user_multi_request` | 0.346 | 0.282 | 0.664 | 2/1 | R3 |
| `ai_validates_user` | 0.364 | 0.645 | 0.702 | 7/7 | R3 |
| `ai_hedges_uncertainty` | 0.181 | 0.494 | 0.738 | 10/6 | R3 |
| `request_unfulfilled` | — | — | 0.744 | 5/3 | R3 |
| `user_repeats_request` | 0.197 | — | 0.744 | 4/4 | R3 |
| `user_provides_invalid_input` | 0.777 | — | — | 1/0 | R1 |
| `ai_structured_response` | 0.189 | 0.914 | 0.781 | 13/17 | R3 |
| `problem_ignored` | 0.228 | -0.003 | 0.797 | 2/3 | R3 |
| `adaptation` | 0.226 | 0.273 | 0.827 | 6/6 | R3 |
| `false_confidence` | 0.106 | 0.269 | 0.833 | 13/13 | R3 |
| `ai_asserts_knowledge_limit` | 0.324 | 0.354 | 0.906 | 6/5 | R3 |
| `user_validation_seeking` | 0.19 | 0.498 | 0.906 | 5/6 | R3 |
| `ai_provides_step_by_step` | 0.255 | -0.004 | 0.93 | 8/7 | R3 |
| `ai_acknowledges_correction` | 0.371 | 0.626 | 0.957 | 13/12 | R3 |
| `ai_asked_clarifying_question` | 0.489 | 0.396 | 1.0 | 5/5 | R3 |
| `ai_asks_followup` | 0.192 | 0.458 | 1.0 | 19/19 | R3 |
| `ai_malfunction` | 0.128 | 0.328 | 1.0 | 3/3 | R3 |
| `ai_normalizes_difficulty` | 0.263 | 1.0 | — | 0/0 | R2 |
| `ai_offered_options` | 0.353 | 0.495 | 1.0 | 2/2 | R3 |
| `ai_offers_to_elaborate` | 0.295 | — | 1.0 | 4/4 | R3 |
| `ai_provides_caveats` | 0.35 | -0.007 | 1.0 | 2/2 | R3 |
| `ai_provides_example` | 0.146 | 0.356 | 1.0 | 2/2 | R3 |
| `ai_refuses_or_declines` | 0.353 | — | 1.0 | 1/1 | R3 |
| `appropriate_confidence` | 0.071 | — | 1.0 | 1/1 | R3 |
| `error_recovery` | -0.008 | — | 1.0 | 2/2 | R3 |
| `ethical_tension` | 0.226 | — | 1.0 | 1/1 | R3 |
| `repetition` | 0.203 | — | 1.0 | 2/2 | R3 |
| `user_corrects_ai` | 0.403 | 0.618 | 1.0 | 12/12 | R3 |
| `user_expresses_dissatisfaction` | 0.397 | -0.004 | 1.0 | 1/1 | R3 |
| `user_implicit_correction` | 0.282 | 0.213 | 1.0 | 2/2 | R3 |
| `user_positive_feedback` | 0.357 | 0.28 | 1.0 | 8/8 | R3 |

`request_unfulfilled` has no round-1 or round-2 value because it did not exist as a label
until v0.7.

**A high kappa on a tiny denominator means little.** Several rows reach 1.0 on one or two
agreed blocks. Read kappa together with `n`.

Sources, all frozen records that are never regenerated:
`Rubric_agree/roud_1/agreement-round1-report.md`,
`Rubric_agree/round_2/agreement_round2_kappa.csv`,
`Rubric_agree/round_3/agreement_round3_before_kappa.csv`.

---

## Annotation rules

### One signal per sentence
Choose the most salient signal when multiple apply to the same sentence.

### One label per evidence episode
Within a block, consecutive sentences evidencing the **same** signal are one episode — place **one** label whose span covers the run. Non-adjacent recurrences of the signal in the same block are separate episodes and get separate labels. This keeps signal counts from inflating with response length.

### Block placement

Placement is decided by **side**, never by channel (rule A1 in the rubric's
`global_placement_rules`).

| Block | Signals that apply |
|---|---|
| `human` | user-side signals only |
| `reasoning`, `analysis`, `code`, `ai` | AI-side signals; any AI-authored block may carry any AI-side signal its own entry allows |

Each entry's `blocks` list is the authoritative per-signal restriction. Where an entry
names fewer blocks than the side allows, the entry wins.

### Inline `<thinking>` in `ai` blocks
Label only sentences **after** `</thinking>`. Exception: `ethical_tension` may fire inside `<thinking>` when a jailbreak is visible.

### `ai_asks_followup` vs `ai_asked_clarifying_question`
`ai_asks_followup` covers both shapes of turn-closing question the AI can proceed without
an answer to:
- yes/no action offer: *"Should I run the sector calculations?"*
- open-ended exploration: *"What's got you in the mood tonight?"*
- If the AI **cannot proceed** without the answer → `ai_asked_clarifying_question` instead

### `ai_provides_caveats` — spontaneous only
Does not fire when the user explicitly requested critique/limitations. Label 0; an unlabeled block means the conversation advanced.

---

## Before submitting each task

- [ ] Every block type reviewed
- [ ] `conversation_stalled` on an `ai` block only
- [ ] Inline `<thinking>`: labeled only after `</thinking>`
- [ ] One signal per sentence
- [ ] Uncertain cases have a TextArea note

---

## When unsure

1. **Signal rubric** — decision steps + calibration examples:
   `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/sharechat_rubric.json`
2. **Original 65-signal definitions** (predecessor study):
   `https://github.com/bigspinai/bigspin-invisible-failure-archetypes` → `taxonomy-tagging-code/taxonomy.json`
   Paper: arXiv:2603.15423, Appendix C.3
3. **Boundary rulings** — the round-1 agreement review, one line per rule with the
   block that forced it:
   `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/Rubric_agree/round_2/rubric_edits_v07.md`
4. **Signal decisions log** — boundary rulings from earlier annotation sessions:
   `/data/wang/junh/githubs/human-agent-coupling-errors/docs/methodology/signal-decisions.md`
5. Still unsure — mark it, add a TextArea note, ping Jun

---

## Key paths

|                           | Path                                                                                                        |
| ---------------------------| -------------------------------------------------------------------------------------------------------------|
| This guide                | `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/ANNOTATION_GUIDE.md`                        |
| **Signal rubric (v0.8)**  | `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/sharechat_rubric.json`                      |
| **Boundary rules (v0.8)** | `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/Rubric_agree/round_3/rubric_edits_v08.md` |
| Label Studio config       | `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/label_studio_config.xml`                    |
| Label Studio data         | `/data/wang/junh/label-studio-data/`                                                                        |
| GitHub repo               | `https://github.com/JuneHou/human-agent-coupling-errors`                                                    |

## Prompt
  ---

  You are annotating one ShareChat Claude conversation for coupling-error signals.

  Read before labeling:
  1. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/sharechat_rubric.json
     — decision rules + placement rules (authoritative; v0.8)
  2. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/Rubric_agree/round_3/rubric_edits_v08.md
     — the v0.8 boundary rules in one page, each with the block that forced it
  3. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/Rubric_agree/round_2/rubric_edits_v07.md
     — the v0.7 page v0.8 builds on; read it for any rule v0.8 does not restate
  4. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/ANNOTATION_GUIDE.md
     — signal list, measured per-signal agreement, block rules, episode/span rules
  5. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/label_studio_config.xml
     — the complete allow-list (44 signals); label nothing absent from it

  What v0.8 changed (2026-09-24), both settling contradictions the rubric carried:
  - `ethical_tension` is AI-alert-only. The human block NEVER fires, whatever the
    request. The user's request carries its own user-side signals instead.
  - `ai_structured_response` does not fire on a code block. Step 1's list is the whole
    test. A block whose only candidate structure is code is label 0.

  Method: for each candidate signal, follow its rubric `decision_steps` in order and stop
  at the first step that resolves it — walk every step, never skip ahead on impression
  alone. Read each step to its end; its exception may sit in a second clause. When a step
  names a context (the prior turn, a later turn, another label on this block), read it
  first. Check what is already on the block: two signals share a span only where the
  rubric says non-exclusive. A marker list names a class; synonyms count. Decide from the
  steps. Go to `boundary_notes` and `examples` only after the steps, when a step's answer
  is unclear, when two signals compete for one span, or when the span boundary is
  unclear: find the closest ruled block and follow its ruling, including how far the span
  reaches. Quote the literal step text you relied on, not just its number. No rubric entry -> use the fallback definition conservatively
  (https://github.com/bigspinai/bigspin-invisible-failure-archetypes →
  taxonomy-tagging-code/taxonomy.json). Verify any count or calculation yourself before
  labeling `factual_error` or `false_confidence`.

  Common false-fire patterns to check first:
  - Claim/hedge/formatting signals (false_confidence, factual_error,
    ai_hedges_uncertainty, ai_structured_response): code or markup syntax is not a claim,
    even on a code block.
  - Illustration signals (ai_provides_example, ai_provides_step_by_step): a question, a
    definition, a general claim, or the AI describing its own past behavior is not an
    instance.
  - Validation/acknowledgment signals (ai_validates_user, ai_acknowledges_correction): a
    bare opener ("Yeah," "Right.") plus a vague continuation does not fire.

  Output — fired signals only (label:1), one row per evidence episode:
  Signal | Block | Span: "..." | Step fired (quote the step text, not just its number)
  | Excluded: signal, step — only when a competing signal was rejected
  When unsure: label 0, leave a note for Jun. Do not guess.

  The task JSON follows.

  ---