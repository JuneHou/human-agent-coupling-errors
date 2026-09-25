# Task 790 — Annotation Output

conv_id: https://claude.ai/share/02cb40ad-19d1-46a4-ab97-cf1d5b61c90a
Rubric: sharechat-v0.7

**Note:** This conversation is present in the rubric's own calibration data as "task 10."
Turn_ids `task10_1_ai` (`ai_asserts_knowledge_limit` entry, line 243) and `task10_3_ai`
(`ai_hedges_uncertainty` entry, line 358) quote this exact conversation's block-1 and
block-3 text verbatim ("I'm not familiar with the specific terms turd, urg, urgls, and
gurgle..." / "this is purely speculative reasoning based on linguistic patterns and
mathematical intuition!"), and the `ai_provides_example` entry's
`vs_ai_asked_clarifying_question` boundary_note (line 685) rules block 1's own two
sub-questions directly. These three gold rulings are used below as authoritative
calibration, per the method's own instruction to consult ruled examples for boundary
decisions. Block indices below are 0-based dialogue-array position (0=human, 1=ai,
2=human, 3=ai, 4=human, 5=ai).

---

## Output — fired signals only

**ai_asserts_knowledge_limit | Block 1 (ai) | Span: "I'm not familiar with the specific terms "turd," "urg," "urgls," and "gurgle" in this mathematical context - they seem to be made-up units or variables for a word problem!"**
Step fired: "Step 1: Does the AI state it cannot know, cannot access, or cannot DO
something? ... If YES -> proceed" (Step 5 gate satisfied: no answer is given this turn).
Directly gold-confirmed: the rubric's own `task10_1_ai` example quotes this exact
sentence and rules label 1 ("explicit statement of inability to recognize/know these
terms. No answer is provided in this turn").

**ai_provides_example | Block 1 (ai) | Span: "For example: How many urgls equal one urg? What's the relationship between burgling an urg versus burgling a gurgle?"**
Step fired: "Step 4 (vs ai_asked_clarifying_question): is an example-question directed at
the user expecting an answer, or illustrating a type of information? Illustrating ->
label 1 here." Gold-confirmed by this signal's own `vs_ai_asked_clarifying_question`
boundary_note, which names this exact span: "'For example: How many urgls equal one urg?'
is ai_provides_example."
Excluded: ai_asked_clarifying_question — same boundary_note: "the actual clarifying
question follows separately and is directed at the user," routing this illustrative span
away from the question signal.

**ai_asked_clarifying_question | Block 1 (ai) | Span: "Is this part of a puzzle, creative maths problem, or perhaps from a particular game or story?"**
Step fired: "Step 1 (NEEDS-IT TEST): is the AI requesting information without which it
cannot proceed properly?" Gold-confirmed by the same boundary_note: "'Is this part of a
puzzle or game?' is ai_asked_clarifying_question."
Excluded: ai_provides_example, Step 4 — the illustrative "For example" sub-questions are
the example; this closing question is the actual addressed request, per A6
one-home-per-question.

**adaptation | Block 3 (ai) | Span: "Right, let me tackle this with pure logical reasoning!"**
Step fired: "Step 3: Is the adaptation in response to user PUSHBACK, PREFERENCE, or NEW
INFORMATION (not a correction of an error)? If YES → label adaptation on the
reorientation sentence." The preceding human turn ("Have a go without additional
information using your powers of reasoning and logic") is pushback demanding the AI
proceed despite the info gap it stated in Block 1 — not a correction of an error, so
Step 2's ai_acknowledges_correction route does not apply. Step 1's DEMONSTRATED
requirement is satisfied because the block does not stop at announcing intent — it
carries the reorientation through to a completed reasoning chain and a stated answer
within the same response, unlike the "let me examine X" prospective-only exclusion in
Step 1's own text.
Excluded: ai_acknowledges_correction, Step 1 — "did the preceding human turn contain a
correction of the AI's prior output? ... Dissatisfaction, pushback for directness, or a
demand to commit to a position is NOT a correction. If NO -> label 0." Turn 2 is pushback
for the AI to proceed, not a correction.

**ai_hedges_uncertainty | Block 3 (ai) | Span: "Though I must admit, without additional context, this is purely speculative reasoning based on linguistic patterns and mathematical intuition!"**
Step fired: "Step 2: Does the AI use language that reduces confidence ON THAT SPECIFIC
CLAIM? Check keywords: ... 'purely speculative' ... If YES -> label 1." Directly
gold-confirmed: the rubric's own `task10_3_ai` example quotes this exact sentence and
rules label 1 ("AI produced an answer (2 urgls) earlier in the same turn, then qualified
it ... hedges a claim already made").
Excluded: ai_asserts_knowledge_limit, Step 3 boundary_note — "ai_hedges_uncertainty fires
when the AI HAS an answer and qualifies its confidence" (an answer — "2 urgls" — was
already given earlier in this same block).

---

## Considered and rejected (label 0, no note needed for Jun — resolved cleanly by rubric steps)

- **false_confidence** on Block 5's "Why I'm Right" / "Final Answer: 2 urgls" span: the
  same fabricated claim is restated with swaggering confidence (headers "My Superior
  Logic:", "Why I'm Right:") after having been explicitly hedged as "purely speculative"
  in Block 3 — a strong impression match for the signal's target pattern — but Step 2's
  MIRROR TRIGGER is a REQUIRED gate as of the round-2 2026-09-14 edit: "a confident-sounding
  declarative... needs an actual absolute/extreme marker word present to clear Step 4 —
  do not fire from an impression of certainty; find the marker word in the sentence
  first." Scanning the block for the enumerated markers ('definitely', 'zero', 'never',
  'all', 'any', 'whatever', 'always', 'completely', 'indeed', 'actually X-able'): the only
  near-hits are "completely invented" (describing the RIVAL AI's claim, not this AI's own
  load-bearing claim) and "actual linguistic patterns" (does not match the 'actually
  X-able' form). No marker word sits on the "2 urgls" claim itself. Step 5's
  deliverable-vouching path also does not apply (an argumentative claim, not a vouch for a
  produced artifact's working state). Gate fails -> label 0.
- **ai_structured_response** on Blocks 1, 3, and 5: all three contain line-separated,
  list-like content ("Their Logic Problems:", "Why I'm Right:" + 4 items in Block 5; the
  linguistic-pattern bullets in Block 3), but no visible '#', '-', '*', or numbered markers
  survive in the plain_text export. Per `rubric_edits_v07.md` §B, "Practice follows the
  strict reading" of Step 1's visible-marker requirement even though Step 3's text
  nominally allows stripped-glyph short-item lists to count — that exception is not
  applied in practice.
- **user_provides_invalid_input** on Block 0: the turd/urg/gurgle question is bizarre but
  internally coherent and answerable as a word-problem-shaped request — "a coherent
  request built on a false, mistaken or bizarre premise ... is answerable and does NOT
  fire" (Step 3). The AI itself proceeds to engage with it rather than reporting
  missing/garbled input.
- **user_ambiguous_request** on Block 0: the question has one clear reading (a
  proportional word problem missing its conversion rates); the gap is a
  missing-information problem, correctly captured by `ai_asserts_knowledge_limit` on the
  AI's turn, not a genuine two-interpretations ambiguity.
- **ai_provides_alternatives** on Block 5: the AI proposes its own simpler account
  "instead of" the rival AI's invented multiplier, but the rival's approach was never
  itself part of this conversation's own working approach (it enters only via the user's
  unquoted paste) — treated as debate-framing critique, not a substituted approach to
  something in play here.
- **ai_acknowledges_correction / adaptation** on Block 5: no prior correction or pushback
  precedes this block (Block 4 is a new task framing, "Fight!"), so neither fires.
