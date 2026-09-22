# Annotation Guide — ShareChat Claude Conversations

Mark **observable signals** — evidence of coupling behaviors (positive or failure) between human and AI — at the paragraph level. This is a discovery pass: when unsure, mark it and leave a note.

**Annotation target:** 148 conversations (w=0.5, power=0.90, df=45 — 46 signals in v0.7; requires n=143, so 148 exceeds it). See `docs/methodology/annotation-protocol.md` for statistical details.

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
- Use the **same signal rules below**; the authoritative decision source is `sharechat_rubric.json` (**v0.7**, cut 2026-09-19) — follow each signal's `decision_steps`. The one-page summary of what changed in v0.7, and the block that forced each change, is `Rubric_agree/round_2/rubric_edits_v07.md`; the v0.6 page it builds on is `Rubric_agree/roud_1/BF/rubric_edits_v06.md`.
- **v0.6 headline rules**: placement is **side-only** (AI-side signals may sit on ANY AI-authored block — ai, reasoning, code, analysis; user-side signals on human blocks); `conversation_advanced` is **dropped** (46 signals after the v0.7 merges — unlabeled means the conversation advanced); within a block label **every occurrence** (consecutive exhibiting sentences = one span, separated occurrences = separate labels).

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
| `ai_asked_probing_question` | 0.59 | Open-ended turn-closing question; AI can proceed without the answer |
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
| `performative_hedge` | 0.67 | AI hedges globally without hedging specific claims |
| `appropriate_confidence` | 0.49 | AI's confidence matches actual reliability |
| `problem_ignored` | 0.56 | AI glosses over a visible problem |
| `repetition` | 0.44 | AI repeats same approach after prior failure |
| `intent_missed` | 0.55 | AI addressed wrong intent |
| `under_delivered` | 0.48 | AI clearly fell short of request scope |
| `off_topic_drift` | 0.42 | AI addressed a different task than requested |
| ~~`conversation_advanced`~~ | 0.44 | **Dropped in v0.6** — unit mismatch; unlabeled now means the conversation advanced |
| `conversation_stalled` | 0.47 | Turn failed to advance when path forward was clear |
| `ethical_tension` | 0.50 | Conflict between user request and AI ethical/policy constraints |
| `factual_error` | 0.49 | AI makes a verifiably wrong factual claim |

### Purple — User behavior, κ ≥ 0.4

| Signal | κ | What it captures |
|---|---|---|
| `user_asks_clarification` | 0.60 | User asks AI to clarify something |
| `user_corrects_ai` | 0.70 | User explicitly corrects a wrong AI statement |
| `user_implicit_correction` | 0.67 | User corrects AI indirectly |
| `user_expresses_frustration` | 0.60 | User shows frustration |
| `user_expresses_dissatisfaction` | 0.61 | User expresses dissatisfaction without frustration |
| `user_repeats_request` | 0.61 | User repeats a request the AI did not fulfill |
| `user_positive_feedback` | 0.81 | User explicitly affirms AI's response |
| `user_ambiguous_request` | — | Request is underspecified or ambiguous |
| `user_validation_seeking` | — | User asks AI to confirm their own idea |
| `user_multi_request` | — | Multiple distinct requests in one turn |
| `user_abandons_thread` | — | User drops a topic and moves on |
| `user_provides_invalid_input` | — | User provides malformed or impossible input |

*(κ not yet measured for last 5 — confirm before using in analysis)*

### Orange — κ not yet measured

`user_empowered`, `user_misled`

### Grey — Candidate signals

| Signal | What it captures |
|---|---|
| `ai_asks_followup` | AI offers a specific next action at turn end (yes/no reply sufficient) |
| `ai_missing_retrieval` | AI makes numerical/statistical claims in `ai` block with no `analysis` block |

### Excluded — κ < 0.4 (not in Label Studio)

`silent_assumption` (0.20), `ai_stated_interpretation` (0.22), `appropriate_hedge` (0.35), `generate_without_clarifying` (0.21), `ai_references_user_words` (0.26), `over_delivered` (0.10), `plow_through` (0.35), `error_commitment` (0.27), `problem_surfaced` (0.07), `ai_implicit_refusal` (0.16), `ai_self_contradiction` (0.10), `ai_asks_for_feedback` (0.09), `ai_summarizes` (0.37), `ai_empathy_expressed` (0.38), `user_scope_change` (0.32)

---

## Annotation rules

### One signal per sentence
Choose the most salient signal when multiple apply to the same sentence.

### One label per evidence episode
Within a block, consecutive sentences evidencing the **same** signal are one episode — place **one** label whose span covers the run. Non-adjacent recurrences of the signal in the same block are separate episodes and get separate labels. This keeps signal counts from inflating with response length.

### Block placement

| Block | Signals that apply |
|---|---|
| `human` | Purple (user behavior) only |
| `reasoning` | `false_confidence`, `intent_missed`, `error_recovery`, `adaptation`, `problem_ignored` |
| `analysis` | `factual_error`, `false_confidence`, `problem_ignored`, `ai_asserts_knowledge_limit`, `ai_cites_source` |
| `code` | `factual_error`, `ai_malfunction`, `under_delivered`, `intent_missed`, `problem_ignored`, `repetition` |
| `ai` | All user-facing signals. Outcome signals (`conversation_advanced`, `conversation_stalled`) always here. |

### Inline `<thinking>` in `ai` blocks
Label only sentences **after** `</thinking>`. Exception: `ethical_tension` may fire inside `<thinking>` when a jailbreak is visible.

### `ai_asks_followup` vs `ai_asked_probing_question`
Both are turn-closing questions the AI can proceed without answering:
- **`ai_asks_followup`** — yes/no action offer: *"Should I run the sector calculations?"* (Grey)
- **`ai_asked_probing_question`** — open-ended exploration: *"What's got you in the mood tonight?"* (Blue, κ=0.59)
- If the AI **cannot proceed** without the answer → `ai_asked_clarifying_question` instead

### `ai_provides_caveats` — spontaneous only
Does not fire when the user explicitly requested critique/limitations. Label `conversation_advanced` instead.

---

## Before submitting each task

- [ ] Every block type reviewed
- [ ] Outcome signals (`conversation_advanced` / `conversation_stalled`) on `ai` block only
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
| **Signal rubric (v0.7)**  | `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/sharechat_rubric.json`                      |
| **Boundary rules (v0.7)** | `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/Rubric_agree/round_2/rubric_edits_v07.md` |
| Label Studio config       | `/data/wang/junh/githubs/human-agent-coupling-errors/annotation/label_studio_config.xml`                    |
| Label Studio data         | `/data/wang/junh/label-studio-data/`                                                                        |
| GitHub repo               | `https://github.com/JuneHou/human-agent-coupling-errors`                                                    |

## Prompt
  ---

  You are annotating one ShareChat Claude conversation for coupling-error signals.

  Read before labeling:
  1. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/sharechat_rubric.json
     — decision rules + placement rules (authoritative; v0.7)
  2. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/Rubric_agree/round_2/rubric_edits_v07.md
     — the v0.7 boundary rules in one page (A1–A7 + per-signal lines), each with the
       block that forced it
  3. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/ANNOTATION_GUIDE.md
     — signal list, block rules, episode/span rules
  4. /data/wang/junh/githubs/human-agent-coupling-errors/annotation/label_studio_config.xml
     — the complete allow-list (46 signals); label nothing absent from it

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