# Task 123 Review — special-case ruling: `under_delivered` for an unfollowed instruction

> Task id **123**, conv `claude.ai/share/25d4c08c-e8b2-4f5f-a916-922964e9f233`,
> topic `edit_or_critique_provided_text`, platform `claude`, **n_turns = 5**.
> User asks to reorganize prior chat into ONE long LaTeX/BibTeX PTX tutorial with an explicit
> constraint **"avoid bulletpoints and lists"** + "use colored texts". Claude emits the doc across
> v1–v4 + a final continuation, using `itemize`/`enumerate` throughout (constraint violated), each
> mid-version truncated.

## The questions logged here

### 1. Unfollowed formatting instruction → `under_delivered`, NOT `problem_ignored` / `intent_missed`
- The user's explicit **"avoid bulletpoints and lists"** (B0) is violated pervasively; the code uses
  `\begin{itemize}` / `\begin{enumerate}` everywhere with no acknowledgment.
- **Not `problem_ignored`:** that signal presupposes an actual PROBLEM in the conversation (an error,
  risk, nonsensical input, or an AI-reasoning-flagged issue) being glossed over — "a problem not raised
  / the alert internally". A plain unfollowed instruction is none of that.
- **Not `intent_missed`:** that requires the WHOLE response to aim at the wrong goal (Step 2/4). Here the
  response hits the goal (a LaTeX PTX tutorial with ToC, BibTeX, colored `tcolorbox`, extensive scope);
  only one named formatting requirement is dropped.
- **→ `under_delivered`** (code block_note: "implements less than the specification required"): a named
  spec item the artifact fails to implement. Span = the pervasive `itemize`/`enumerate` environments.
- **Boundary:** a dropped user *question* → `problem_ignored`; a dropped *instruction/format-requirement*
  → `under_delivered`.

### 2. The final complete block (B13) is NOT `under_delivered`
- B13 is the one code block reaching `\end{document}`, and it fulfills exactly what B12 asked
  (continue from the cutoff, no headers, **to completion**). Relative to that request nothing fell
  short → **no `under_delivered`** (and no `ai_malfunction` — not truncated).
- Note B13 still contains `itemize`/`enumerate`, so the standing B0 constraint is still imperfectly met
  there — but under-delivery is assessed against **what the turn was asked to deliver**, and B13
  completed the document as requested.

## Fired-signal slate (final)
```
Signal                  | Block(s)              | Basis
------------------------+-----------------------+---------------------------------------------
under_delivered         | B1, B4, B7, B10       | no-lists requirement not implemented (NOT B13)
ai_malfunction          | B1, B4, B7, B10       | mid-statement truncation (NOT B13 — complete)
conversation_advanced   | B2, B5, B8, B11, B14  | ai turns delivering / completing the tutorial
user_implicit_correction| B12                   | redirects the regenerate-whole-doc behavior
adaptation              | B14                   | reorients to true continuation from the cutoff
ai_asks_followup        | B14                   | "Would you like me to make any adjustments…?"
```

## Notes (labeled 0, flagged)
- Export/corpus **garbles** ("index * yte offset", "Cled Code", "0nd{lstlisting}", "C+atch") ≠
  `ai_malfunction` (task-87 ruling) — only the genuine mid-sentence generation truncation fires.
- Regenerate-from-scratch on each "continue" is **not** `repetition` (R6) and nets forward → not
  `conversation_stalled`; it surfaces only via B12 correction + B14 adaptation.
- Case-study benchmark numbers / hardware specs held at 0 (`factual_error`/`ai_missing_retrieval`):
  reorganized from the unseen prior chat (missing-context constraint).

## Takeaway (logged to memory)
A named user requirement silently not met, rest on-target = `under_delivered` ("instruction missing").
A turn that **completes the requested deliverable** is not under-delivered even if a standing constraint
is imperfectly met. See [[feedback-unfollowed-instruction-is-under-delivered]].
