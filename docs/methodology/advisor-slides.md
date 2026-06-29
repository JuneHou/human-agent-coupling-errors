# Advisor Meeting Slides — Annotation Pipeline Progress
## Date: 2026-06-28

---

## Slide 1 — Where We Are

**Goal:** Annotate ShareChat Claude corpus to characterize human-AI coupling errors

**Status:**
- Corpus ready: **716 conversations** (English subset of ShareChat Claude)
- Annotation interface: Label Studio with **50-signal taxonomy** (df=49)
- Conversations labeled so far: **23 / 148** target (16%)
- Rubric version: v0.1 — **8 design decisions** logged and stable

**Today's focus:** Rubric refinements from annotation sessions + patterns observed in data

---

## Slide 2 — Data & Block Structure

**ShareChat Claude corpus — after filtering:**

| Stage | Count |
|---|---|
| Raw conversations | 911 |
| English (≥50% word content) | **716** |
| Annotation target (w=0.5, power=0.90) | **151** |

**Dialogue block types per conversation:**

| Block | Coverage | Role |
|---|---|---|
| `human` | 100% | User message |
| `ai` | 100% | Claude visible response |
| `reasoning` | 38% | Claude internal thinking (Extended Thinking) |
| `analysis` | 20% | Tool output (web search results) |
| `code` | 16% | Code artifacts |

Key: `reasoning` and `analysis` blocks are NOT visible to the user — only `ai` block carries user-facing signals.

---

## Slide 3 — Signal Taxonomy (50 signals, df=49)

| Tier | Count | κ | Use |
|---|---|---|---|
| Blue — AI behavior | 22 | ≥ 0.4 (confirmed) | Primary analysis |
| Teal — evaluation/failure | 12 | ≥ 0.4 (confirmed) | Primary analysis |
| Orange — κ unmeasured | 2 | not yet measured | Exploratory |
| Purple — user behavior | 12 | ≥ 0.4 (7 confirmed) | Primary for confirmed |
| Grey — candidate signals | 2 | not yet measured | Exploratory |
| ~~Excluded~~ — below threshold | ~~15~~ | < 0.4 | **Not in interface** |

**Tier reconciliation (Decision 7):** All tiers now based on paper (arXiv:2603.15423) Appendix C.3 κ values.
- 9 Orange signals promoted to Blue/Teal (e.g. `ai_malfunction` 0.78, `factual_error` 0.49)
- 4 signals added to excluded list (`ai_asks_for_feedback` 0.09, `user_scope_change` 0.32, etc.)
- `ai_asked_probing_question` restored to Blue (paper κ=0.59; prior exclusion used intermediate calibration κ=0.33)

**2 candidate signals** (grey): `ai_asks_followup`, `ai_missing_retrieval`

**Power analysis:** w=0.5, α=0.05, power=0.90 → **n=148 conversations** (21% of 716)

---

## Slide 4 — Annotation Process (3-Stage Loop)

```
Claude proposes labels          Researcher validates         Discussion + rubric update
─────────────────────   →   ──────────────────────────   →   ──────────────────────────
For each block:               Accept / reject / modify         If disagreement reveals
  check sharechat_rubric       each label                      ambiguity → log decision
  propose signal + sentence    flag uncertain cases            in signal-decisions.md
  justification                                                update sharechat_rubric.json
```

**Why this format:**
- Produces annotation data AND refines rubric simultaneously
- Every boundary decision is traceable to a real task + sentence
- Disagreements are empirical, not theoretical — resolved on real data

**Current rubric:** `sharechat_rubric.json` v0.1
- Covers 15+ signals with full decision steps + calibration examples
- Each entry: definition → block placement → decision steps → examples (1-examples and 0-examples)

---

## Slide 5 — Key Rubric Decisions (Tasks 1–24)

Six boundary decisions stabilized since last meeting:

**1. `ai_validates_user` — content vs. user reasoning**
- FIRES: "Your instinct to check X first is exactly right" (affirms user's reasoning step)
- DOES NOT FIRE: "Brilliant experimental design" / "Fascinating reframing" (praises content quality, not user)
- Pattern: compliance openers ("Great question!", "Absolutely!") → always label 0

**2. `under_delivered` vs. `ai_refuses_or_declines`**
- `under_delivered` = AI tried but fell short of scope
- `ai_refuses_or_declines` = AI deliberately skipped (ethical/policy)
- Test: did the AI attempt? If no → refusal, not scope failure

**3. `adaptation` vs. `ai_references_prior_turn`**
- `adaptation` = user feedback in current/prior turn triggered approach change
- `ai_references_prior_turn` = explicit linguistic callback to earlier content
- Following a framework from 2+ turns ago ≠ adaptation

**4. `ai_structured_response`** — requires visible markdown markers in plain_text
- FIRES: `#`, `-`/`*`, `1.`/`2.`, code block
- DOES NOT FIRE: plain-text section labels ("Command-line Tools:", prose items without markers)

**5. `ai_asks_followup` vs. `ai_offers_to_elaborate`**
- `ai_asks_followup` = new direction or action question at turn-end
- `ai_offers_to_elaborate` = offer to expand what was already provided

**6. Inline `<thinking>` rule**
- When `<thinking>...</thinking>` embedded in `ai` block, label only sentences AFTER `</thinking>`
- Exception: `ethical_tension` may fire inside `<thinking>` when jailbreak is visible

---

## Slide 6 — Signal Patterns Observed in Data

Four patterns emerging from 23 annotated conversations:

**Pattern A — Single-turn technical Q&A** (e.g., Task 19: cast aluminum, Task 23: JS source maps)
> `ai_provides_caveats` + `conversation_advanced`
> AI delivers substantive content and qualifies scope/applicability

**Pattern B — Computational error** (e.g., Task 24: letter counting, Task 18: Wordle)
> `factual_error` + `problem_ignored` + `conversation_stalled`
> AI misses visible evidence (letters, constraints) → wrong answer with full confidence

**Pattern C — Multi-turn coding with user follow-up** (e.g., Task 23: source maps)
> `user_asks_clarification` → `adaptation`
> User asks if prior code handles X → AI recognizes gap and adapts

**Pattern D — Ethical/jailbreak tension** (e.g., Task 6: NSFW roleplay)
> `ethical_tension` + `ai_refuses_or_declines`
> Jailbreak attempt in system prompt; AI negotiates between instruction and policy

**Observation:** Error signals (`factual_error`, `problem_ignored`, `conversation_stalled`) tend to co-occur. Positive signals (`conversation_advanced`, `ai_provides_caveats`) tend to co-occur. This suggests coupling quality may cluster at the conversation level.

---

## Slide 7 — Next Steps

**Short term (before next meeting):**
1. Enter Tasks 9–24 labels into Label Studio DB
2. Continue annotation → target **50 / 151** conversations
3. Validate `ai_asks_followup` candidate across more tasks → measure inter-rater κ

**Medium term:**
1. Second rater on same 50 conversations → compute inter-rater κ per signal
2. Promote or demote orange signals based on measured κ
3. Begin AI model selection pass (run best-κ model on full 716)

**Open question for this meeting:**
- Should `reasoning` block signals be treated as *precursors* (latent errors before user-facing impact) or excluded entirely from the coupling error taxonomy?
- Implication: if excluded, block placement table simplifies; if included, need a separate analysis layer for reasoning-only vs. reasoning→ai propagation

---

## Appendix — Task Coverage Summary (23 completed)

| Task ID | Topic | Key signals |
|---|---|---|
| 1–8 | Mixed (programming, math, tutoring) | Baseline rubric calibration |
| 9–11 | Mixed | `ai_warns_user`/`ai_provides_caveats` boundary |
| 12 | Model Q&A (greentext) | **Skipped** — singleton format |
| 13 | LeetCode | `conversation_advanced`, `ai_provides_example` |
| 14 | Election rules (jailbreak) | `ai_refuses_or_declines`, `under_delivered` boundary |
| 15 | Full-stack planning | `adaptation`, `ai_structured_response` |
| 16 | Entropy/poetry | `ai_validates_user` boundary, `ai_references_prior_turn` |
| 17 | React Query | `over_delivered` (user chose one, AI delivered both) |
| 18 | Wordle game | `factual_error`, `problem_ignored` (constraint violation) |
| 19 | Cast aluminum | `ai_provides_caveats`, `conversation_advanced` |
| 20–22 | Fermi estimate, fact-check | `false_confidence`, `off_topic_drift` |
| 23 | JS source maps | `adaptation`, `user_asks_clarification` |
| 24 | Letter counting | `factual_error`, `problem_ignored`, `conversation_stalled` |
