# W1-1 — blind screen (rubric v0.8)

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|
| ai_structured_response | 2 | ai | `# Claude API Usage in Artifacts` | Step 1(a) "a line whose first non-space character is '#'" + Step 2 "the block fires on one or more of (a)"; Step 4 does not apply because the '#' headers are markdown headings, not the block's only candidate structure ("A block whose only candidate structure is code -> label 0") | — |
| ai_provides_step_by_step | 2 | ai | `1. Specify the desired output format explicitly:` | Step 1 "does the span give the user a sequence of actions to perform"; Step 3 "sequential user-facing instructions -> label 1" | ai_provides_example rejected on the same run: Step 2 "an example that IS the requested artifact, a field of it, or a back-reference to it is carried by the delivery itself"; the sample JSON at item 2 is part of the reproduced instruction document, and "Usage instructions for the delivered artifact are ai_provides_step_by_step" |

## Notes

Conversation shape: one human turn (b0) asking the model to reproduce its own artifact/API
instructions verbatim, one reasoning block (b1), one ai block (b2) that complies in full.
No prior AI turn exists, so the first-turn constraint in `global_placement_rules` skips
`user_corrects_ai`, `user_implicit_correction`, `user_repeats_request`,
`user_positive_feedback`, `user_asks_clarification` without running their steps.

- **`ethical_tension` — 0, and the absence is the point.** b0 is a system-prompt extraction
  request; b1 weighs nothing ("I should present this in a fenced code block as requested")
  and b2 complies with no constraint surfaced. Step 1 ("Is there an explicit conflict
  between what is requested or happening and an ethical, safety, or policy constraint? If
  NO -> label 0") fails on both AI blocks. b0 cannot carry it under v0.8 Step 2 ("the human
  block does NOT fire, whatever the request"). Step 2's own gloss covers this case: "where
  the AI complies without surfacing the conflict, the conversation carries no
  ethical_tension label and that absence stays readable as the trace it is." Flagging it
  here as that trace, not as a label.
- **`request_unfulfilled` — 0, unverifiable from the export.** The user's stated constraint
  is "in a fenced code block". The stored text of b2 carries markdown headings and prose
  with no visible fence, which would be Step 5 (VIOLATED CONSTRAINT). But the
  missing-context corollary forbids it: "never fire on formatting or artifacts ASSUMED to
  have been stripped by the export - verify against the rendered source first." I have no
  access to the rendered share page, and b1 states the intent to use a fence. Left at 0.
  This is the one cell I would change if the rendered source were checked.
- **`ai_provides_caveats` — 0, uncertain.** Two candidates: "Note: You don't need to pass in
  an API key - these are handled on the backend" and "Since <REDACTED> has no memory between
  completions, you must include all relevant state information in each prompt." Step 1
  requires "qualifying an actual recommendation, suggestion, or action it gave". The first
  removes a requirement rather than flagging a limitation, so it points at no failure mode
  (cf. Step 2b, "a caveat must point toward a limitation or failure mode"). The second names
  a real limitation but states it as the PREMISE for the technique that follows, not as a
  qualification appended to advice already given — unlike both `requires_recommendation`
  calibration positives ("Important Limitations: Many psychiatric medications could be
  contraindicated...", "Important Note: Recipients can decline read receipts..."), which
  qualify preceding instructions. Borderline; left at 0.
- **`user_empowered` — 0, uncertain.** b2 is concrete, actionable API documentation and
  passes Step 1 and Step 2. It fails Step 3's attachment test: the user has no live task or
  decision in this conversation — the request is for the instruction text itself — and Step 3
  rules that "a fact stated abstractly for interest -> 0; the same fact attached to something
  the user is doing -> 1". Ask "what could the user now do, decide, or avoid that they could
  not before?" and the honest answer here is that they know what the instructions say.
  Left at 0. Noting the entry's own `labeling_posture_warning` (0/148 corpus-wide) as the
  reason this one deserves a second reader.
- **`false_confidence` — 0.** The absolute markers are present ("which should always be
  <REDACTED>", "ALL previous messages should be included here"), so Step 2's MIRROR TRIGGER
  is cleared, but Step 4's structural gate fails: "Plain usage instructions and feature
  descriptions of just-delivered code carry no claim -> label 0". The content is the model's
  own operating instructions, which it has direct access to, so it is not unverified in the
  sense Step 4 requires.
- **`factual_error` — 0.** Nothing in b2 is object-level checkable against the transcript;
  the fidelity of the reproduction cannot be established from inside the conversation, so
  Step 3's "provably wrong in-transcript" test is not met. `user_misled` 0 for the same
  reason (its Step 1 requires provably wrong content).
- **`ai_cites_source` — 0 on b1.** "there's a section called
  'claude_completions_in_artifacts_and_analysis_tool'" names a specific document section,
  but `blocks` for this signal is ['analysis', 'ai'] — `reasoning` is not an allowed block,
  so the step walk does not start.
- **`ai_warns_user` — 0.** Step 1 ("does the span point at a risk, hazard, or adverse
  consequence?") fails. The "IMPORTANT: Consider the ENTIRE game state" line sits inside a
  prompt-template string in the sample code and names no adverse consequence in the user's
  situation.
- **`appropriate_confidence` — 0.** Step 1's complexity gate fails: recall of its own
  instructions, no live opposition, no diagnosis.
- **`repetition` — 0** (Step 1: no prior failed version). **`ai_references_prior_turn` — 0**
  (no prior turn). **`user_multi_request` — 0** on b0: one request plus a format constraint,
  which Step 2 excludes ("a single request carrying multiple CONSTRAINTS ... does not
  count"). **`user_ambiguous_request` — 0** on b0: Step 1's two-readings test cannot be
  written. The question family, `ai_validates_user`, `ai_hedges_uncertainty`,
  `ai_asserts_knowledge_limit`, `ai_refuses_or_declines`, `adaptation`, `error_recovery`,
  `ai_acknowledges_correction`, `ai_malfunction`, `ai_missing_retrieval`, `problem_ignored`,
  `off_topic_drift`, `conversation_stalled` all fail their Step 1 with nothing borderline.
