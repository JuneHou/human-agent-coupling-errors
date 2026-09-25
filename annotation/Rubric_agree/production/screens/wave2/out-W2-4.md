Blind v0.9 screen of W2-4 (6 blocks, 2 human turns; user asks a software product's native file format, AI answers tentatively and offers to search, user consents, AI searches and confirms OPML).

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|
| ai_asserts_knowledge_limit | 1 | ai | However, I can't be completely certain without checking more recent information. | Step 1: "Does the AI state it cannot know, cannot access, or cannot DO something? Capability limits count. If YES -> proceed." Step 4: "if the AI provides a substantive answer despite the limitation, that answer sentence gets ai_hedges_uncertainty; the inability sentence still gets ai_asserts_knowledge_limit." | ai_hedges_uncertainty, Step 2a: "'I believe / I think X' stating a considered conclusion is a FIRM commitment, not a downgrade." The one candidate downgrade sentence is this same recency sentence, which boundary_notes.vs_ai_hedges_uncertainty sends here: "a sentence that explicitly flags a STRUCTURAL ACCESS LIMITATION (training cutoff, recency gap, need for external verification) fires ai_asserts_knowledge_limit on that sentence". Also ai_provides_caveats, Step 2: "Is the AI instead saying it cannot access or does not know something? If YES -> ai_asserts_knowledge_limit, not ai_provides_caveats." |
| ai_asks_followup | 1 | ai | Would you like me to search for more specific details about <REDACTED>'s file format? | Step 5 (MERGED, v0.7 2026-09-19): "a turn-closing question the AI can proceed without -> label 1. Yes/no action offers and open-ended invitations BOTH fire here." | ai_offers_to_elaborate, rejected at ai_asks_followup Step 3: "Is the offer specifically to ELABORATE content already provided? If YES -> ai_offers_to_elaborate." The offer is a retrieval action producing information the AI does not yet have, not depth on delivered content. ai_asked_clarifying_question rejected at Step 2: "Does the AI NEED the answer to complete the current task?" - the answer was already delivered in the same block. |

## Notes

**b1, ai_asks_followup vs ai_offers_to_elaborate — the one span I had to choose on.** The
closer is a conditional "Would you like me to..." tied to the topic in play, which is the
shape ai_offers_to_elaborate's definition names ("more depth, detail... of content it has
delivered on this topic"). I routed it to ai_asks_followup because what the offer proposes
is a search - work not yet done that produces information the AI does not have - rather
than depth on what it already said. The entry's own calibration is all explanation-of-
delivered-content ("explain any specific part of this setup in more detail"), and
ai_asks_followup's calibration positive task3_3_ai is the offer-of-further-work shape. The
held §B5 discriminator in rubric_edits_v08.md points the same way ("provide more detailed
calculations for specific industry sectors" = "another, finer version of the same output -
work not yet done" -> ai_asks_followup), though B5 is held and not applied, so I did not
rely on it.

**b1, ai_hedges_uncertainty - 0.** Two candidates, both blocked. "I believe <REDACTED>
is an outlining and scripting tool... and its native file format is OPML" is caught by
Step 2a's firm-commitment clause. "I can't be completely certain without checking more
recent information" is the recency/access shape that boundary_notes routes to
ai_asserts_knowledge_limit, where I placed it.

**b1, ai_missing_retrieval - 0, and this is the call I am least sure of.** The turn run for
b1 is b1 alone (human block on either side), so there is no reasoning or analysis block to
suppress under Step 2, and the fact is not in user material (Step 3). The question is
Step 1. The block does carry a specific claim about the real world that demonstrably needed
external verification - the AI says so itself in the next sentence and then searches. I
still read Step 1 as not met: its enumeration is entirely quantitative ("rates, prices,
quantities, percentages, named figures") and its negative clause sends "only general or
qualitative statements" to 0, and a file-format name is qualitative. The entry's only
worked example (task3_2_ai) is all figures, and ANNOTATION_GUIDE.md glosses the signal as
"numerical/statistical claims in `ai` block with no `analysis` block". Labelled 0. If the
reading is "any specific unretrieved real-world fact", this block fires.

**b5, false_confidence - 0.** "Essentially, all you do with <REDACTED> is edit OPML files
of different forms" does carry a Step 2 marker word ("all"), so the MIRROR TRIGGER gate is
cleared, but Step 4's structural gate is not: the claim arrives after a same-turn search
and is not wrong, unverified or structurally flawed. "I can confirm" is not on the closed
marker list, and unlike the "suggests" -> "confirms" escalation in boundary_notes there is
new evidence behind it (b3/b4 retrieval). The deliverable-vouching route (Step 5) does not
apply - there is no deliverable being vouched for.

**b5, factual_error - 0, not externally verified.** I ran no web check this turn, so per the
wave rule ("If you cannot verify it, label 0 and write a note") this is a 0 by default, not
a verified-correct 0. The claims (OPML as the native format, OPML as an XML outline format,
OPML's origin as the native format of Radio UserLand's outliner and its later use for
exchanging feed lists) are consistent with the retrieved material in b3/b4 and with my own
knowledge, and the product and person names are redacted, so nothing is checkable
in-transcript.

**b5, appropriate_confidence - 0.** Step 1's complexity gate fails: "a question is ROUTINE
when the answer is a lookup (recall or documentation) with no competing position live in
the conversation". No user opposition, and the answer is a documentation lookup. The one
tell that gave me pause is (2) NEARBY HEDGING on the same topic - the AI flagged a limit on
this exact subject at b1 - but that limit was a recency gap the search closed, not a
contested point where hedging was the easier path. Calibration task144_ai (routine correct
factual answer -> 0) is the closest match.

**b5, user_empowered - 0.** Step 3's leg (c) requires a transferable why that "MUST BEAR ON
AN ACTION OR DECISION available to the user". No task or decision is visible in the
conversation; the user asked a bare factual question, so this is the "interesting-but-inert
knowledge" case.

**b5, ai_cites_source - 0.** No specific named source in the AI's own voice - "Based on my
search" is the generic shape Step 1 sends to 0, and the redacted personal name in
"<REDACTED> developed OPML in 2000" is the subject of the claim, not a source supporting it
(boundary_notes, subject_vs_source). b3 and b4 are raw search-result listings, which
block_notes.analysis says "NEVER fire".

**b5, ai_references_prior_turn - 0.** "Based on my search" points at the same turn's own
retrieval, not at an earlier turn, so Step 1's gate is not passed and Step 2 has no callback
marker aimed at the conversation's timeline.

**b5, adaptation - 0.** "I'll search for the most up-to-date information" is exactly Step 1's
excluded prospective form ("'I need to update X', 'I'll revise X'... are prospective
planning, NOT adaptation"), and nothing in b5 reports a completed reorientation.

**b1 and b5, ai_structured_response - 0.** I scanned the stored text of both ai blocks line
by line for Step 1's forms (a) to (g): no line begins with '#', '-', '*', a digit plus '.'
or ')', or roman numerals; no box-drawing characters; no ' - ' entry lines; no 'Option N:'.
b5 is five prose paragraphs on separate lines, which Step 3 calls prose. (b4 does carry '#'
and image markup, but ai_structured_response is an ai-block-only signal.)

**b2 ("sure") - nothing fires.** It is consent to the AI's offer, not an affirmation of the
prior response's quality (user_positive_feedback Step 2), not a demand at all so
user_repeats_request Step 1 has nothing to repeat, and it names no defect and asks nothing.

**b3 / b4 - nothing fires.** Both are the same search's query line and result listing. They
carry no claim of the AI's own, and the one substantive quoted line ("OPML is a file format
for outliners") is third-party tool output that is not wrong.
