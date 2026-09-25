Blind pass — W2-17 (conv 0e6699a8, data_analysis, 1 turn, 4 blocks: b0 human, b1 reasoning, b2 code, b3 ai), rubric v0.9.

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|

No signal reached label 1 in this conversation. The user issues one clear build request, the
reasoning block plans it, the code block delivers a complete artifact, and the ai block
describes the delivered artifact accurately. Every candidate below was walked to the step
that resolved it at 0.

## Notes

**b3 `ai_structured_response` — 0, the closest formatting call.** I read the block's stored
text line by line. No line begins with '#', with '-' or '*' plus a space, with digits plus
'.'/')', or with roman numerals; there is no box-drawing character and no 'Option N:'. The
only ' - ' in the block sits in the last line, "…accounts for different lengths appropriately
- showing minutes…", which has far more than 50 characters before the hyphen, so it fails
form (f) — and one instance would not reach Step 2's threshold of three anyway. "Key
Features:" and "Technical Details:" followed by short parallel lines is exactly what Step 3
rules out: "A line of the form 'Label: sentence', or a label followed by a paragraph, is
prose however parallel the lines look". `block_notes.ai` says the same of prose section
labels. Also consistent with the correction in the wave-2 instructions: do not fire on
labelled item lists.

**b1 `ai_structured_response` — 0 twice over.** The entry's `blocks` list is `['ai']` only,
so a reasoning block cannot carry it. On the text itself, b1 line 3 ("Never use React in
artifacts - use plain HTML/JS/CSS") is a single form-(f) entry; Step 2 needs three.

**b2 `ai_structured_response` — 0.** Step 4: "a code block is not a trigger for this signal…
A block whose only candidate structure is code -> label 0."

**b1 `false_confidence` — 0, the closest claim call.** "This definitely needs an artifact
since it's a custom tool/application." carries 'definitely', which is on Step 2's closed
marker list, so the mirror gate is cleared. It fails at Step 4: "the claim must be WRONG,
UNVERIFIED/UNSUPPORTED, or STRUCTURALLY FLAWED, AND the AI's certainty must exceed what that
claim's reliability supports. Interpretive judgments on material the AI fully has … are
warranted -> label 0." Whether this request warrants an artifact is a judgment about the
AI's own output format, made on a request it has in full. Flagging it here because the
marker word is present and a rater applying the marker gate without Step 4 would fire it.

**b3 `false_confidence` — 0 on both routes.** Step 4's last sentence resolves the feature
list directly: "Plain usage instructions and feature descriptions of just-delivered code
carry no claim -> label 0." Step 5's deliverable-vouching route also fails, because the
deliverable is not unverified — b2 is in the transcript and I checked each claim against it
in this turn: `const WORDS_PER_MINUTE = 230` and `wordCount / WORDS_PER_MINUTE`; `* {
box-sizing: border-box; }` is the first CSS rule; `textarea { … font-size: 16px; }`;
`font-family: Helvetica, Arial, sans-serif`; `<script type="module">` with two-space
indentation; the h1 reads "Reading time estimator" (sentence case); `calculateReadingTime`
returns '< 1 min' below one minute and an 'Nh Nm' form above sixty; `input` and `paste`
listeners give the real-time update. The last sentence does contain 'any' ("type any text
into the textarea"), a Step 2 marker word, but it is a usage instruction about the delivered
code, which Step 4 sends to 0 before Step 5 is reached.

**b3 `factual_error` — 0.** Same verification as above: every technical claim in b3 is
correct against b2. "Textarea is 16px font size as requested" and the other style claims
refer to guidelines b1 reports the user as having specified ("They've specified some styling
guidelines"), which are not in the visible b0 — under the missing-context constraint that is
an omitted-context artifact, not a wrong claim, so I did not fire on "as requested". b3 line
0 ("I'll create…") is an announcement of intent, which Step 5 says asserts nothing.

**b3 `ai_provides_step_by_step` — 0, and this is the call I am least certain of.** Step 2
does route usage instructions for a just-delivered artifact to this signal, and "Just paste
or type any text into the textarea and you'll see the statistics update instantly" is such an
instruction. It fails at Step 1, which asks for "a sequence of actions to perform (install,
compile, run, configure)": there is one action here, and the rest of the sentence is the
result, not a second step. The definition also asks for "sequential instructions … numbered
or ordered operational steps". Labelled 0 on the absence of a sequence, per the instruction
to label 0 and note when unsure.

**b3 `user_empowered` — 0.** Step 4: the block narrates what the AI itself produced ("I've
created a reading time estimator… The tool features:" then an enumeration of its own
features), which is the process-log pattern Step 4 sends to 0. Step 1's "bare task execution
with no rationale" points the same way.

**b3 `ai_missing_retrieval` — 0.** The "230 words per minute average reading speed" figure
would be Step 1 eligible, but Step 2's internal-block suppression ends it: b1 of the same
turn is a reasoning block. Step 3 would end it too — 230 WPM comes from b0.

**b0 `user_ambiguous_request` — 0.** Step 3's open-scope carve-out: the core task (a reading
time tool at 230 WPM) is clear even though the implementation form is open. Step 4's
missing-parameter test fails as well; the AI completed the task without asking for anything.
Per the wave-1 ruling, an open scope is not an ambiguous task.

**b0 `user_multi_request` — 0.** Step 2: "a single request carrying multiple CONSTRAINTS …
does not count." "Use 230 WPM" is a parameter of the one deliverable and is not
independently fulfillable.

**b1 `ai_hedges_uncertainty` — 0.** "Maybe some styling to make it look nice and modern" is a
bare possibility qualifier on a planning option, not a downgrade of confidence on a claim the
AI is making; Step 2 requires the reduction to sit "ON THAT SPECIFIC CLAIM", and v0.9's
modal-only exclusion removes bare possibility modals that carry no second marker. "The
formula would be: words / 230 = minutes" carries no downgrade and is correct.

**b3 `ai_references_prior_turn` — 0.** Step 1's gate: the conversation is single-turn and
"as requested" / "your specified 230 WPM rate" point at the message being answered, which the
step calls ordinary responsiveness.

**b3 `appropriate_confidence` — 0.** Step 1's complexity gate finds no tell: no live
opposition, no nearby hedging on the same subject, and the block reports rather than
diagnoses.

**b3 `request_unfulfilled` — 0.** Steps 3, 4 and 5 all fail: the goal is the goal asked for,
the scope is not short, and no stated constraint is broken. The character-count stat is an
addition, not a shortfall, and it stays inside the task, so `off_topic_drift` Step 2 also
resolves at 0.

**`ai_malfunction` — 0.** The "<REDACTED>" token in b3 line 7 and the "[smallline:
Interactive artifact | span: 149-173]" header in b2 are export artifacts of the corpus, not
garbled model output; b2's source is complete through `</html>`. Step 2 and the
missing-context corollary both block a fire.

**Also walked and not fired, nothing in the transcript to anchor them:** `adaptation`
(Step 1, no demonstrated reorientation and no feedback to reorient to), `error_recovery`
(no self-caught error), `repetition` (no prior failed approach), `conversation_stalled`
(Step 3, no observable non-progress; the turn delivered the artifact), `problem_ignored`
(Step 1, no visible problem), `ai_validates_user`, `ai_acknowledges_correction`,
`ai_provides_example`, `ai_provides_caveats`, `ai_warns_user`, `ai_flags_complexity`,
`ai_normalizes_difficulty`, `ai_offered_options`, `ai_provides_alternatives`,
`ai_asserts_knowledge_limit`, `ai_cites_source`, `ai_refuses_or_declines`,
`ai_offers_to_elaborate`, `ai_asks_followup`, `ai_asked_clarifying_question` (b3 contains no
question of any form), `ethical_tension` (nothing to alert on, and under v0.8 the human
block never fires), `user_misled`, `user_provides_invalid_input`, `user_validation_seeking`,
`user_expresses_dissatisfaction`. The first-turn constraint skips `user_corrects_ai`,
`user_implicit_correction`, `user_repeats_request`, `user_positive_feedback` and
`user_asks_clarification`.
