# Human–Agent Coupling Errors

Research project on **coupling errors** in human-AI / human-agent workflows: failures that
emerge from the *interaction loop* between human intention, agent interpretation, agent
action, human understanding, and repair.

This is **not** a human-error or user-error taxonomy (well-studied in HCI / human factors /
human reliability analysis). The target is the *coupling* — the loop itself.

## Core research question

> What additional error types emerge when an AI system is embedded in a human interaction
> loop (with tool use / agent traces), rather than used as a standalone chatbot or an
> autonomous agent?

## Three axes of coupling

- **Human → AI** — does the AI capture human goals, constraints, corrections, preferences?
- **AI → Human** — does the human understand the AI's plan, rationale, state, uncertainty,
  and the consequences of its actions?
- **Shared control / repair** — does the interaction repair mismatches through
  clarification, explanation, confirmation, escalation, or rollback?

## Relationship to prior work

Direct predecessor: Potts & Sudhof, *"Invisible Failures in Human–AI Interactions"*
([arXiv:2603.15423](https://arxiv.org/abs/2603.15423)). We **inherit** its loop framing
(failures as loop properties; the visible/invisible-failure distinction) and its **method**
(per-step signals → derived classifications → archetypes, via LLM annotation with
inter-annotator κ calibration). We do **not** inherit its chat-only taxonomy — see
[`DECISIONS.md`](DECISIONS.md).

## Status

Phase 0 — scoping. See [`DECISIONS.md`](DECISIONS.md) for the methodology and open questions,
and [`docs/`](docs/) for exploration notes.

## Layout

```
docs/        exploration notes, dataset analyses, the eventual collection spec
data/        datasets (gitignored; large files not committed)
notebooks/   exploratory analysis
src/         annotation / analysis code
```
# Current Task summary
  Project: Building a sentence-level signal labeling rubric for the ShareChat Claude corpus (716 English
  conversations, agentic with tool use) to support taxonomy development on human-agent coupling errors.

  What we are doing: Annotating conversations from annotation/data/annotation_input.json by discussing signal
  assignments, debating disagreements, and recording decisions into a growing rubric file at
  annotation/sharechat_rubric.json.

  Workflow: I show you a task JSON excerpt → we discuss which signals apply to which blocks → disagreements are
  resolved → confirmed rules and examples are written into sharechat_rubric.json in calibration.json format.

  Rubric format (annotation/sharechat_rubric.json):
  Per signal: blocks (which block types), block_notes (block-specific rules), decision_steps (if/then tree),
  examples ({turn_id, block, label, category, rationale}). Turn IDs use task{id}_{turn}_{blocktype} convention.

  Tasks discussed so far: Task 2 (avatar editor, 5-exchange coding conversation), Task 5 (Space Blaster truncated
  game code), Task 13 (LeetCode container water), Task 20 (Fermi estimate US GDP video content).

  Key rules established (all written into rubric):
  - ai_stated_interpretation fires on ai block only — reasoning-only interpretation → silent_assumption on ai
  block
  - ai_malfunction on code = truncated mid-statement; on ai block = does NOT fire when AI claims artifact without
  producing it (→ false_confidence or under_delayed)
  - Outcome signals (conversation_advanced, user_empowered, etc.) go on ai block, not analysis block
  - ai_structured_response requires visible markdown markers in plain_text — prose section labels don't count
  - over_delivered has two triggers: scope excess, or unrequested cross-validation at end
  - error_recovery (AI catches own error) vs ai_acknowledges_correction (user told AI it was wrong)
  - One signal per sentence maximum

  One candidate signal identified: narrated_without_implementing — AI describes code changes as complete without
  producing the artifact.

  Reference files:
  - annotation/sharechat_rubric.json — our growing rubric (11 signals so far)
  - annotation/signal_checklist.csv — 86 check questions by block×signal
  - /data/wang/junh/githubs/bigspin-invisible-failure-archetypes/taxonomy-tagging-code/calibration.json —
  upstream calibration reference (WildChat, not ShareChat)