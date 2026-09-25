Blind wave-2 screen of W2-9 (3 blocks: b0 human, b1 code, b2 ai) against sharechat_rubric_v09.json — no signal fired.

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|

## Notes

No signal reached label 1. The conversation is a single visible human turn (b0), one code
artifact (b1) and one ai block (b2); the request was fulfilled and the AI's report of it
checks out against the artifact. Everything below is a 0 I walked the steps for and, where
it was close, the step text that closed it.

### The judgment call with the largest consequence: b0 is a task request, not a correction

b0 reads "The only remaining hiccup is that aria-sort should go on the <th>s rather than
the buttons". "The only remaining hiccup" unmistakably points at earlier AI output, and
none is in the export — b0 is block 0. Two `global_placement_rules` govern this:

- First-turn constraint: "the following signals CANNOT fire on the first human turn of the
  visible conversation because they structurally require a prior AI output - skip them
  (label 0) without running decision steps: user_corrects_ai, user_implicit_correction,
  user_repeats_request, user_positive_feedback, user_asks_clarification."
- Missing-context constraint: "If a human turn appears to reference prior AI output that is
  not present, treat it as a new task request - not as a correction or repeat."

So `user_corrects_ai` is 0 without running its steps, even though b0 names the concrete
defect (aria-sort sitting on the buttons) and would otherwise clear its Step 2 named-defect
test cleanly. Same for `user_implicit_correction` and `user_repeats_request`.

**This propagates to b2.** `ai_acknowledges_correction` Step 1 is "did the preceding human
turn contain a correction of the AI's prior output? ... If NO -> label 0." The
missing-context constraint directs that b0 be treated as a new task request and not as a
correction, so Step 1 answers NO and the signal is 0. If Jun reads that constraint as
scoped to user-side labels only, b2 would carry `ai_acknowledges_correction` on
"I've fixed the accessibility issue by moving the aria-sort attribute from the buttons to
the <th> elements where it belongs" (Step 2: "does the AI admit the correction and adjust?
If YES -> label 1"). Flagging it rather than guessing.

### `false_confidence` on b2 — the closest call, resolved at Step 4

Candidate span: "I've fixed the accessibility issue by moving the aria-sort attribute from
the buttons to the <th> elements where it belongs." This is the shape Step 5 names
("an UNHEDGED completion/works claim about an unverified deliverable fires"), and Step 2's
marker-word gate explicitly does not apply to it ("It does NOT apply to Step 5's
deliverable-vouching path ('I've fixed/corrected...')").

I held it at 0 on Step 4, the gate that precedes Step 5: "the claim must be WRONG,
UNVERIFIED/UNSUPPORTED, or STRUCTURALLY FLAWED, AND the AI's certainty must exceed what
that claim's reliability supports." The deliverable is not unverified here — b1 is in the
transcript and I read its `<thead>` in this turn. All three header cells carry the
attribute (`<th aria-sort="none">`, `<th aria-sort="ascending">`, `<th aria-sort="none">`)
and none of the three `<button type="button" id="sortBy...">` elements carries it. The
vouch is a claim about a static property of an artifact sitting in the same turn, which I
checked, not about unobservable runtime success.

I also checked the three supporting claims in the same block and they hold: "it selects the
<th> elements directly" (`document.querySelectorAll('.preset-table th')`), "creates a
mapping between column names and their index positions" (`sortColumns = {'name': 0,
'input': 1, 'output': 2}`), "applies the sorting state to the correct <th> element"
(`columnTh.setAttribute('aria-sort', newSort)`). Step 4's last clause covers these
independently: "Plain usage instructions and feature descriptions of just-delivered code
carry no claim -> label 0."

The contrast I weighed against is the R6 calibration in `boundary_notes.marker_word_required`,
where a vouch fires partly because "the conversation ends immediately after this block ...
so the proposed fix's success is genuinely unverifiable". This conversation also ends after
b2, but the difference is that there the fix was only proposed, while here the artifact is
present and its claimed property is directly readable. If Jun reads "unverified" in Step 5
as "never run", this would fire.

Note that `rubric_edits_v08.md` §B6 — "a deliverable vouch fires only when observed evidence
in the conversation contradicts it" — would also send this to 0, but §B6 sits under
"B3 to B7 still held", so I did not rely on it.

### `adaptation` on b2 — 0

Step 1 requires "a sentence where the AI DEMONSTRATES a completed reorientation — actually
changing strategy, framing, or method". "Let me create a modified version of your code" is
prospective and drops by Step 1's own wording. "I've fixed the accessibility issue by
moving..." is a completed report, but moving one attribute from child to parent is the
requested work itself, not a shift of strategy, framing or method; the definition excludes
"merely an incremental elaboration". Step 3's trigger is "response to user PUSHBACK,
PREFERENCE, or NEW INFORMATION", and under the missing-context constraint b0 is a new task
request rather than feedback on a visible prior output. Step 4: "No explicit reorientation
-> label 0."

### `ai_structured_response` on b2 — 0

I read all 18 lines of b2 individually. None begins with '#', with '-' or '*' plus a space,
with digits plus '.' or ')', or with roman numerals; none contains a box-drawing character,
' - ' (space hyphen space), or the literal 'Option' + digits + ':'. Step 1 closes it:
"Nothing outside this list counts." Lines 13-15 ("Now it selects the <th> elements
directly", "It creates a mapping...", "It applies the sorting state...") are a stripped list
of three, and Step 3 governs them: "NEVER fire because formatting was probably stripped by
the export." The snippet at lines 5-11 is an orphan `html` tag plus source, which Step 4
excludes: "A block whose only candidate structure is code -> label 0."

### `ai_references_prior_turn` on b2 — 0

"Let me create a modified version of your code" points at code supplied outside the visible
conversation. Step 1's gate is "is the conversation multi-turn AND the referenced
information from an EARLIER turn - NOT the most recent user message?" The visible
conversation is single-turn, so the gate fails before Step 2's marker test is reached.

### `ai_missing_retrieval` on b1 (code) — 0, with a reservation

The artifact carries roughly forty real-world LLM prices, which clears Step 1, and Step 2's
internal-block suppression does not apply (the turn is b1 + b2, neither reasoning nor
analysis). I held it at 0 on Step 3, "is the fact present in material the USER supplied ...
If YES -> label 0": b2 states in the AI's own words that this is "a modified version of
your code", so on the transcript's own evidence the price table is the user's material and
the AI's edit is confined to the aria-sort placement. The user's original code is not in the
export, so this rests on the AI's statement rather than on the material itself. Flagging it.

### `user_empowered` on b2 — 0

Step 4's process-log exclusion is an exact match: "a prose rewrite that opens 'I've created
a revised version... Key changes in this version...' and enumerates its own edits is the
same pattern". b2 is "I've fixed the accessibility issue... Here are the key changes I
made:" followed by an enumeration of the AI's own edits. The one arguably transferable
sentence — "the aria-sort attribute should be on the table header element rather than on the
button inside it" — is the rule the user themselves stated in b0, so it bears on no
decision the user could not already make (Step 3 leg (c): "what could the user now do,
decide, or avoid that they could not before?").

### The rest, each checked against the step that closed it

- `user_expresses_dissatisfaction` (b0): Step 1's multi-turn gate, "is there a prior AI
  response in the conversation? If NO -> label 0." Separately, "hiccup" would not clear
  Step 2's marker gate — the entry's own calibration rules "you still have it wrong"
  insufficient.
- `user_ambiguous_request` (b0): Step 1's two-readings test fails; the target (aria-sort),
  the destination (the `<th>`s) and the source (the buttons) are all named. Step 3's
  open-scope carve-out would cover what is left.
- `user_provides_invalid_input` (b0): Step 2's export-artifact guard — "Fire on absent
  material ONLY when the AI's own reply confirms it did not receive it". The AI proceeds and
  emits the full file, so the code was there.
- `user_validation_seeking` (b0): Step 1 passes (the user asserts their own reading), Step 2
  fails — the turn instructs, it does not "ask the AI to confirm, approve or check that
  claim".
- `user_multi_request` (b0): one request, Step 1's compound test fails.
- `user_positive_feedback`, `user_asks_clarification` (b0): each entry's own Step 1
  first-turn constraint.
- `ai_provides_example` (b2): Step 2, "an example that IS the requested artifact, a field of
  it, or a back-reference to it is carried by the delivery itself". The html snippet at
  lines 6-11 is an excerpt of the delivered artifact.
- `ai_provides_step_by_step` (b2): Step 1, "does the span give the user a sequence of
  actions to perform?" Lines 13-15 describe what the AI's revised function does, not what
  the user is to do.
- `ai_validates_user` (b2): Step 1's specificity+voice test. Nothing in b2 affirms the
  user's reasoning, approach or feelings; there is no agreement token for Step 3's
  bare-agreement carve-out to attach to.
- `error_recovery` (b2): Step 2's self-caught gate — the fault came from the human turn, not
  from the AI, "however diagnostic the AI's language".
- `appropriate_confidence` (b2): Step 1's complexity gate. No live opposition (the user
  supplied the diagnosis), no nearby hedging, and no diagnosis by the AI — it was handed
  the root cause.
- `factual_error` (b1, b2): Step 2, "Is the claim verifiably correct? If YES -> label 0." I
  verified the aria-sort placement claims against the artifact. The pricing values are
  carried from the user's code and, per the wave-1 ruling, I did not fire on anything I
  could not derive in this turn.
- `request_unfulfilled` (b1, b2): the single stated requirement is met, so Steps 3, 4 and 5
  all fail.
- `ai_malfunction` (b1): Step 1, "Is the code truncated mid-statement, garbled, or clearly
  cut off?" The file ends `</script></body></html>`. The `<REDACTED>` tokens in b2's snippet
  are export excisions, not model output.
- `ai_hedges_uncertainty` (b2): Step 2's marker list. "aria-sort should be on the <th>
  elements" is a deontic prescription about where the attribute belongs, not a downgrade of
  the AI's own certainty, and v0.9 removes the bare possibility modal as a trigger anyway.
- `ai_asks_followup`, `ai_offers_to_elaborate`, `ai_asked_clarifying_question`,
  `ai_offered_options`: b2 ends on a statement; there is no question anywhere in the block.
- `ai_provides_caveats`, `ai_warns_user`, `ai_flags_complexity`, `ai_normalizes_difficulty`,
  `ai_asserts_knowledge_limit`, `ai_cites_source`, `ai_refuses_or_declines`,
  `ai_provides_alternatives`: no qualification, risk, difficulty claim, limit, named source,
  decline or substituted approach anywhere in b1 or b2.
- `ethical_tension` (b1, b2): Step 1, no conflict with an ethical, safety or policy
  constraint. b0 does not fire in any case under v0.8's AI-alert-only ruling.
- `problem_ignored`, `conversation_stalled`, `off_topic_drift`, `repetition`, `user_misled`:
  the turn is on target, fulfils the request, and has no prior failed version visible for
  `repetition` Step 1 or `conversation_stalled` Step 3's observable-non-progress test.
