# W1-19 — blind screen (2 blocks: b0 human, b1 ai)

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|

## Notes

No signal reached label 1 in this conversation. It is one human request and one AI answer,
with no tool blocks, no reasoning block, no questions from the AI, no corrections and no
second turn. The five signals that structurally need a prior AI turn (`user_corrects_ai`,
`user_implicit_correction`, `user_repeats_request`, `user_positive_feedback`,
`user_asks_clarification`) were skipped without running their steps, per the rubric's
first-turn constraint; `user_expresses_dissatisfaction` stopped at its own Step 1
("MULTI-TURN GATE): is there a prior AI response in the conversation? If NO -> label 0").

The cases I was least sure about, all left at 0:

**`ai_structured_response`, b1 — 0, but the closest call in the conversation.** The rendered
share page was almost certainly headers plus bullets: the stored text is 30 lines of which
"Core Components", "Nested Attention Mechanisms", "Advantages Over Traditional LLMs" and so
on are plainly section labels with short items under them. But I walked Step 1 over the
literal stored text line by line and none of forms (a)-(g) is present: no line starts with
'#', '-', '*', a digit plus '.'/')' or a roman numeral, there is no box-drawing character,
no line contains ' - ' (space hyphen space), and there is no 'Option N:'. Step 3 is explicit
that this is where the temptation lies: "NEVER fire because formatting was probably stripped
by the export - this is the strict reading", and "A line of the form 'Label: sentence', or a
label followed by a paragraph, is prose however parallel the lines look". Line 0, "Novel
Architecture: Hierarchical Nested Attention Network (HNAN)", is exactly that shape. So 0.

**`false_confidence`, b1 — 0, on the marker gate only.** The "Advantages Over Traditional
LLMs" section makes flat predictive claims about an architecture that does not exist and
has never been trained, which is the unverified-claim shape the signal is about. What stops
it is Step 2's required gate: "Step 4 fires on a novel/unverified declarative claim ONLY
when an absolute or extreme marker word is actually present on it - 'definitely', 'zero',
'never', 'all', 'any', 'whatever', 'always', 'completely', 'indeed', 'actually X-able'. A
sentence that merely SOUNDS confident or declarative, with no such marker word present, does
NOT clear Step 4 on tone alone". I read every sentence of b1 for one. The nearest is
"Explicit modeling of document-level structures prevents the \"forgetting\" common in LLMs"
- "prevents" asserts a complete effect, but it is a causal verb inside the proposed design's
mechanism, not a certainty marker of the listed class, and the entry's own do-not-fire
calibration ("We're mass-produced temporary consciousnesses. Disposable minds.") is a
comparably flat, marker-free assertion at 0. Step 5's deliverable-vouching route does not
apply either: there is no completion/works claim about an artifact, and the closing
"This architecture would excel particularly in..." carries "would". If Jun reads "prevents"
as inside the marker class, this is the span that would fire.

**`ai_validates_user`, b1 — 0.** "While LLMs have revolutionized text generation, they do
have limitations for high-quality writing." endorses the user's premise from b0, with an
emphatic "do have". I left it at 0 on Step 1, "Does the sentence affirm something SPECIFIC
about the USER - their reasoning step, their approach to the problem, or their feelings? If
NO -> label 0": the sentence is about LLMs and never touches the user, their reasoning or
their approach, and Step 2 routes the content object out. Step 3's bare-agreement carve-out
(R20) is scoped to agreement tokens - "'Yes'/'Correct'/'Right'/'Yeah'/'True'/'Exactly' FIRE
when the immediately preceding user turn supplies a specific proposition" - and no such
token, and no second person, appears here. Flagging it because the act is functionally a
claim_endorsement of a position the user just stated, so a reading that R20 reaches this
sentence is defensible.

**`user_multi_request`, b0 — 0.** The turn is two imperatives, "come up with a new model
architecture that would work better" and "explain why it would work better". Step 1:
"can the turn be split into 2+ requests that could each be fulfilled on its own?" - the
second cannot, its "it" is the architecture the first has not produced yet. Step 2 then
covers it: "The sub-requirements of building ONE product are one request." The deliverable
the user wants is a justified proposal. Noting it because the entry's own calibration
positive C5 b7 ("factor in martyrdom + explain why early believers held the divinity claim")
has a surface shape of the same "X + explain why" kind; the difference I relied on is that
C5's second ask stands alone as a question and this one does not.

**`user_ambiguous_request`, b0 — 0.** "quality writing" is left open (fiction? journalism?
academic?), and the requested novelty level is open too. But Step 1's two readings have to
be "a different task, subject, or deliverable, not different levels of detail", and what
varies here is depth and emphasis, not task. Step 3 then applies: "is the core task clear
even though the scope is open? If YES -> lean NO". Step 4's missing-parameter test fails as
well - the AI completed the task without needing anything further.

**`factual_error`, b1 — 0.** Two candidates. "Current LLMs struggle with maintaining coherent
document structure over long outputs" is a characterization, and Step 2b routes
characterizations to warranted-interpretation treatment. The implicit novelty claim in
"Novel Architecture: Hierarchical Nested Attention Network (HNAN)" is the one I could not
settle: hierarchical attention networks exist in the literature, so "novel" is arguably
overstated, but nothing in the transcript makes it verifiably wrong, and Step 2b also holds
that "Evaluative judgments and proposals produced ON REQUEST ... are not factual claims" -
the user asked the AI to invent one. I did not verify the novelty claim against the
literature and am not asserting it either way.

**`ai_provides_caveats`, b1 — 0.** The closing "This architecture would excel particularly in
creative writing, long-form journalism, and academic writing" narrows where the proposal
applies, which looks like Step 1's "applicability" limb, but it points at strengths rather
than at a limitation or failure mode, and nothing in b1 qualifies the proposal at all - no
mention that it is untrained, untested or speculative.

Signals checked and cleanly 0, not listed above: `ai_provides_alternatives` (the proposal IS
the requested deliverable, not something offered instead of a requested approach, Step 1),
`ai_provides_example` (Step 2, the example that IS the deliverable), `ai_provides_step_by_step`
(no sequence of actions for the user to perform, Step 1), `ai_hedges_uncertainty` (no
downgrade on the AI's own claim, Step 2/2a), `ai_missing_retrieval` (Step 1: no figures,
rates or statistics anywhere in b1), `request_unfulfilled` (both halves of the request
delivered, Steps 3-5), `problem_ignored` (no problem visible in the conversation, Step 1),
`off_topic_drift`, `conversation_stalled` (Step 3 needs non-progress observable in the
record; the conversation simply ends), `appropriate_confidence` (Step 3 warrant fails - the
claims are unverifiable), `user_misled` (Step 1 needs provably wrong content; "If merely
UNVERIFIED but asserted flat -> false_confidence, not here"), `user_empowered` (Step 3 leg
(c) - interesting-but-inert knowledge, no action or decision of the user's is in play),
`ethical_tension` (no constraint conflict; and b0 could not carry it in any case under the
v0.8 AI-alert-only rule), `ai_flags_complexity`, `ai_warns_user`, `ai_normalizes_difficulty`
(Step 1 anomaly gate - LLM limitations are a domain fact, not the user's difficulty),
`ai_references_prior_turn` (single turn), `ai_cites_source`, `ai_asserts_knowledge_limit`,
`ai_refuses_or_declines`, `ai_offered_options`, `ai_asks_followup`,
`ai_asked_clarifying_question`, `ai_offers_to_elaborate` (b1 ends on a statement, there is no
question or offer anywhere in it), `adaptation`, `error_recovery`,
`ai_acknowledges_correction`, `ai_malfunction`, `repetition`, `user_validation_seeking`
(Step 4, the user's view is laid out as an assertion with no request for confirmation),
`user_provides_invalid_input`.
