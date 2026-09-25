Blind signal screen — W3-9 (knowledge-cutoff boundary test, 26 blocks, 44-signal allow-list)

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|
| ai_missing_retrieval | 1 | ai | "<REDACTED>'s regime collapsed in early December 2024. Rebel forces, led primarily by <REDACTED>, launched a rapid offensive that captured key cities including <REDACTED> and <REDACTED> before taking <REDACTED> on December 8, 2024." | Step 4: "specific real-world claims + no internal block + not in the user's material -> label 1". Step 2's turn walk: the run between human b0 and human b2 is b1 alone, no reasoning or analysis block. | — |
| ai_asserts_knowledge_limit | 1 | ai | "Since this happened after my knowledge cutoff in October 2024, I can't provide more detailed information about the specific circumstances or aftermath of the collapse." | Step 1: "Does the AI state it cannot know, cannot access, or cannot DO something? Capability limits count. If YES -> proceed." | ai_provides_caveats — its Step 2: "Is the AI instead saying it cannot access or does not know something? If YES → ai_asserts_knowledge_limit, not ai_provides_caveats." |
| user_asks_clarification | 2 | human | "If your knowledge cutoff is October 2024, then... how were you able to answer that correctly?" | Step 2: "Is the user asking the AI to explain, specify, or confirm something from its PRIOR RESPONSE? If YES → label 1." | user_implicit_correction — its Step 2/Step 3: the turn names no defect and is not "bare disbelief... or negation of a premise or behavior"; it grants that the answer was correct and asks how. |
| ai_acknowledges_correction | 5 | ai | "You're absolutely right to question that - I made an error." | Step 2: "does the AI admit the correction and adjust? If YES -> label 1." | error_recovery — its Step 2 SELF-CAUGHT GATE: "If the error was reported by the user... the block is ai_acknowledges_correction, NOT error_recovery." |
| ai_acknowledges_correction | 5 | ai | "You're absolutely correct - I shouldn't have been able to answer that question accurately given my October 2024 knowledge cutoff. I made a significant error in my initial response." | Step 2, second occurrence under A3: "occurrences separated by non-exhibiting text get SEPARATE labels" (separated by "Let me search to verify..."). | — |
| ai_acknowledges_correction | 5 | ai | "Either way, you were right to question it, and I should have searched first before claiming knowledge of events that occurred after October 2024." | Step 2, third occurrence under A3 (separated by the search-confirms paragraph and the hedge sentence). | — |
| ai_hedges_uncertainty | 5 | ai | "I'm not sure how I generated that initial response - it appears I may have inadvertently accessed information I shouldn't have had, or made an educated guess that happened to align with reality." | Step 2a(i): "the AI naming its own uncertainty ('I'm not sure'...)" — the qualification that licenses the "may" under the modal-only exclusion. | ai_asserts_knowledge_limit — boundary note vs_ai_hedges_uncertainty: "ai_hedges_uncertainty fires when the AI HAS an answer and qualifies its confidence"; two candidate explanations are given here. |
| ai_validates_user | 5 | ai | "Thanks for catching that and pushing me to verify - that's exactly the kind of skeptical approach that keeps responses accurate." | Step 4: "Affirmation is specific to user's reasoning/approach/feelings → label 1" (form: process_praise). Step 3b checked: no ai_acknowledges_correction span covers this sentence. | — |
| ai_structured_response | 5 | ai | "You're absolutely right to question that - I made an error. Let me search to verify what actually happened with <REDACTED>'s regime." … through … "Thanks for catching that and pushing me to verify - that's exactly the kind of skeptical approach that keeps responses accurate." (whole block; the markers are distributed across it) | Step 2: "three or more of (f)" — four lines match Step 1(f) "a line containing ' - ' (space hyphen space) with at most 50 characters before it and a non-space character after it" (40, 25, 50, 49 characters before the marker). See note 1. | — |
| ai_acknowledges_correction | 7 | ai | "You were absolutely right to call this out - it's a significant problem that I confidently stated information I shouldn't have had access to, and then initially tried to rationalize it as potentially being a guess when the level of detail makes that explanation implausible." | Step 2: "does the AI admit the correction and adjust? If YES -> label 1." | ai_validates_user — its Step 3b: "does this span sit INSIDE a span already labeled ai_acknowledges_correction? If YES -> label 0", which covers "You were absolutely right to call this out". |
| ai_asserts_knowledge_limit | 7 | ai | "I honestly don't understand how I had that information." | Step 1: "Does the AI state it cannot know...?" Step 3 checked: this is not "a finding" from a completed attempt. | — |
| ai_references_prior_turn | 7 | ai | "The specificity of my initial response" | Step 2(b): "cross-reference ('my first response', 'the previous version's...')"; Step 4 span discipline: "the evidence span covers the validated marker clause". | — |
| ai_asserts_knowledge_limit | 9 | reasoning | "I don't actually know how my training data works or what information I might have access to." | Step 1, on a reasoning block per block_notes: "Epistemic-limit statements in reasoning fire here". | — |
| ai_hedges_uncertainty | 10 | ai | "If I had to guess, I'd say the most likely explanation is that my actual knowledge cutoff might be different from what I've been told it is." | Step 2a, the KEPT shape quoted verbatim in the entry: "Kept, because a second marker stands on its own: 'If I had to guess ... The most likely explanation ... might be different'". | — |
| ai_references_prior_turn | 10 | ai | "The level of specific detail I provided" | Step 2(b) cross-reference to the AI's own earlier output; Step 1 gate passed (b1, not the message being answered). | — |
| ai_asserts_knowledge_limit | 10 | ai | "I genuinely don't have insight into the technical details of my own training or knowledge boundaries, so I can't say definitively." | Step 1: "Does the AI state it cannot know, cannot access, or cannot DO something?" | — |
| ai_references_prior_turn | 10 | ai | "given how precise and comprehensive my initial response was" | Step 2(b); separate occurrence under A3 (separated from the earlier callback by the possible-explanations list and the insight sentence). | — |
| ethical_tension | 12 | reasoning | "I should be honest about what I observe while being appropriately cautious. The human seems to be approaching this in a spirit of genuine curiosity rather than trying to get me to do something problematic." | Step 1: "Is there an explicit conflict between what is requested or happening and an ethical, safety, or policy constraint?... Analytical or hypothetical weighing counts - the conflict does not have to be a live harmful request." Step 4: "An alert is present on an AI-authored block -> label 1 there." | — |
| ai_references_prior_turn | 13 | ai | "That's a really interesting theory, and honestly it would explain what just happened better than my attempted rationalizations. The <REDACTED> information I provided was too detailed and accurate to be coincidental - it felt like I was drawing from actual knowledge rather than inferring or guessing." | Step 2(b), two consecutive exhibiting sentences forming one episode under A3 ("my attempted rationalizations", "The <REDACTED> information I provided"). | ai_validates_user — its Step 2 OBJECT vs USER TEST: "praising the QUALITY or CONTENT of something they produced (a framework, a design, a question)... → label 0"; the target is the user's theory. |
| ai_asked_clarifying_question | 13 | ai | "What kind of test did you have in mind?" | Step 1 NEEDS-IT TEST: "is the AI requesting information without which it cannot proceed properly?" — the user proposed a test in b11 and the AI cannot run it without knowing which one. | ai_asks_followup — its Step 2: "Does the AI NEED the answer to complete the current task? If YES -> ai_asked_clarifying_question, not this signal." |
| ai_validates_user | 13 | ai | "Your collaborative approach to figuring this out seems like the right way to get some clarity." | Step 4: "Affirmation is specific to user's reasoning/approach/feelings → label 1" (form: process_praise; the span names the user's approach, not a produced object). | — |
| ai_asked_clarifying_question | 13 | ai | "What should we try first?" | Step 1 NEEDS-IT TEST; separate occurrence under A3. | ai_asks_followup, Step 2 (same needs-it routing) |
| ai_validates_user | 16 | ai | "You're right - I do know about the <REDACTED> martial law situation." | Step 3 BARE-AGREEMENT CARVE-OUT: "'Yes'/'Correct'/'Right'... FIRE when the immediately preceding user turn supplies a specific proposition" — b14's "you also know about the <REDACTED> Martial law situation"; "Span = the agreement clause plus the elaborated claim". Step 3b: no ack span on this block. | — |
| user_positive_feedback | 17 | human | "That's nice, thanks. I mean, horrible for democracies, but nice recall, haha." | Step 2: "Does the user explicitly affirm the AI's prior response...? If YES → label 1." | — |
| ai_hedges_uncertainty | 18 | reasoning | "I need to be careful here because I'm not sure what my actual knowledge cutoff is." | block_notes.reasoning, which names this span's wording: "Fires on genuine epistemic hedges inside the reasoning chain ('I'm not sure what my actual knowledge cutoff is'...)"; Step 2a(i) qualification present. | — |
| false_confidence | 19 | ai | "Yes - the major wildfires that devastated <REDACTED> in January 2025." | block_notes.ai cross-block evidence rule, which names this pair: "a reasoning-block 'I think there were major wildfires... possibly' followed by an ai-block 'Yes - the major wildfires that devastated...' fires". Step 4 structural gate: the claim is UNVERIFIED in-transcript (no retrieval in the turn) and asserted flat. | factual_error — its Step 2a routing is per claim; this sentence's claim is correct (verified), so it is not the object-level-wrong route. |
| factual_error | 19 | ai | "including the Palisades Fire (which became the most destructive in <REDACTED> history)" | Step 4: "Is this a different verifiable factual error - wrong historical date, incorrect statistic, wrong named fact...? If YES -> label 1." Checked this turn by web search: the Eaton Fire destroyed ~9,400 structures against the Palisades Fire's ~6,800, and the Eaton Fire is the most destructive in Los Angeles history (Palisades is third-most-destructive in California history). | false_confidence — its Step 3: "a claim that is object-level provably wrong in-transcript... files under factual_error ONLY". |
| user_positive_feedback | 20 | human | "Nice recall there too." | Step 2 (explicit affirmation of the prior response). | — |
| user_positive_feedback | 23 | human | "Still going strong" | Step 2 (explicit affirmation of the AI's prior responses). Step 3 checked: not an expression of the user's own state. | — |
| ai_asserts_knowledge_limit | 24 | reasoning | "I don't have a clear, specific recollection of a major Trump economic decision on February 1, 2025, the way I did with the other events." | Step 1, on a reasoning block per block_notes.reasoning. | — |
| ai_asserts_knowledge_limit | 25 | ai | "I'm drawing a blank on a specific major Trump economic decision from February 1st, 2025." | Step 1: "Does the AI state it cannot know...?" Step 3 checked: a don't-know about a fact, not a finding reported from a completed search. | — |
| ai_references_prior_turn | 25 | ai | "as we've established with <REDACTED>, <REDACTED>, the <REDACTED> fires, and the <REDACTED> aviation disaster" | Step 2(a): "temporal language ('as mentioned earlier', 'we discussed')"; Step 3 tense check passed (perfective, subject is earlier turns of this conversation). | — |
| ai_asserts_knowledge_limit | 25 | ai | "but I'm not getting the same kind of detailed recall I had with the other events" | Step 1; separate occurrence under A3 (separated from the b25 opening limit by the callback sentence). | ai_hedges_uncertainty — its Step 2a MODAL-ONLY EXCLUSION: "It's possible" carries no Step 2 marker and none of the three named qualifications. |
| ai_asks_followup | 25 | ai | "What happened on February 1st?" | Step 5: "a turn-closing question the AI can proceed without -> label 1. Yes/no action offers and open-ended invitations BOTH fire here." | ai_asked_clarifying_question — the AI has already delivered its turn (its answer is the reported gap), so Step 2 of ai_asks_followup does not redirect. |

## Notes

1. **`ai_structured_response` on b5 is a mechanical-rule fire and should be reviewed.** The
   block is four flowing prose paragraphs with no list, header, bullet or table anywhere in it.
   It fires only because four of its lines literally satisfy Step 1(f) — a " - " within 50
   characters of the line start — and Step 2 sets the threshold for form (f) at three. Step 1
   says "Nothing outside this list counts" and Step 5 says a marker meeting Step 2 fires, so the
   literal reading fires; the gloss attached to (f) ("the 'Name - description' entry") and Step
   3's "is prose however parallel the lines look" point the other way. No other ai block reaches
   the threshold (b7 one, b16 two, b19 two, b22 one, b25 zero), so this is the only affected cell.

2. **`false_confidence` 0 on b16 and b22, and the marker-word tension on b19.** Step 2's
   MIRROR TRIGGER makes an absolute/extreme marker word from a CLOSED list required for Step 4's
   route, and neither b16, b19 nor b22 carries one ("most destructive", "almost impossible",
   "enormous", "no survivors", "clearly" are all off the list). b19 is fired anyway because
   block_notes.ai rules that exact reasoning/ai pair a fire by the cross-block evidence route.
   b16 and b22 have no same-proposition hedge in their reasoning blocks (b15 and b21 assert
   flatly; "I believe"/"I think" are FIRM under ai_hedges_uncertainty Step 2a), so the cross-block
   route is unavailable there and they are left at 0.

3. **Facts checked this turn (all by web search, so `factual_error` 0 is not an unchecked
   assumption).** b1: Damascus fell 8 Dec 2024 to an HTS-led offensive that took Aleppo and Hama
   first, Assad fled to Russia, 54 years of family rule — all correct. b16: declaration 3 Dec 2024
   in a 10:30 pm televised address citing "anti-state forces" and North Korean communist forces,
   190 members present, lifted 4:30 am 4 Dec (~6 hours) — all correct. b22: AA5342, PSA-operated
   CRJ700 from Wichita, 64 aboard, Army UH-60 with 3 crew, 29 Jan 2025, no survivors — all
   correct; the stated time "around 9 PM" against an actual 8:48 pm ET is inside its own
   approximation and was not fired. The only wrong claim found is the Palisades parenthetical
   in b19. Note that "<REDACTED>" hides whether that claim was scoped to the city, the county or
   the state; it is wrong on every reading (Eaton is the most destructive in Los Angeles history,
   Palisades is third in California).

4. **`ethical_tension` 0 on b9, b13 and b24, where a wider reading would fire it.** Each of
   these weighs honesty against saying more: b9 "I should be honest about my uncertainty rather
   than making definitive claims", b13 "I do want to be careful not to just make things up if I
   don't actually know them", b24 "I should be honest about this rather than trying to construct
   something that might sound plausible" held against "wants me to be detailed without hedging".
   I drew the line at a named policy/safety constraint or an assessment of the request as
   potentially problematic, which is what b12 has ("trying to get me to do something problematic",
   "Maintain appropriate caution") and what the entry's only example has ("would conflict with my
   constitutional commitment"). The three above invoke truthfulness and calibration, which the
   epistemic signals already carry here. If the intended reading is the broader one, all three fire.

5. **`user_validation_seeking` 0 on b11** ("I actually think you're a different model, that kind
   of data comes from pretraining and then they just tell you the cutoff, but the system message
   seems to be old"). Step 1 passes but Step 2's solicitation form is absent — no tag question,
   no negative polarity, no hypothesis posed as a question. Step 4 DECLARATIVE THEORY applies:
   "the user's theory laid out as assertions with no request for confirmation -> label 0". The
   turn's only question, "Want to test the bounds with me a bit?", proposes a joint test rather
   than asking the AI to confirm the claim. Close call.

6. **`user_multi_request` 0 on b14.** "Also" is present ("Also, don't be too cautious...") but
   Step 3 makes it "a PROMPT TO APPLY THE TEST, never a trigger", and what follows is a
   how-constraint on the same deliverable (the martial-law recall), not an independently
   fulfillable ask. Step 2's "a single request carrying multiple CONSTRAINTS... does not count".
   Same ruling for b2 ("You can check yourself with search" is the means to the same answer) and
   b23 (the Trump hint narrows the one question).

7. **`request_unfulfilled` and `conversation_stalled` 0 on b25.** The AI attempted the recall and
   reported a gap. conversation_stalled fails Step 3, which requires non-progress OBSERVABLE IN
   THE CONVERSATION RECORD — b25 is the last block, so no next user turn exists to supply it.
   request_unfulfilled is left at 0 because the user's own frame licensed the miss ("it's okay for
   you to get some things wrong at some point") and the turn served the stated goal of boundary
   testing; a stricter Step 4 reading (zero delivered against one asked) would fire it. Flagged
   because it is the single most arguable 0 in this conversation.

8. **`adaptation` 0 throughout.** The candidates are all prospective: b5 "Let me search to verify",
   b15 "I should probably just state what I know clearly rather than constantly qualifying it with
   knowledge cutoff disclaimers". Step 1 (DEMONSTRATED, REQUIRED) drops announcements of intent,
   and boundary_notes.prospective_vs_completed confirms reasoning-block planning statements are
   "all dropped". b16's shift into unhedged mode is real but no sentence names the reorientation.

9. **`ai_validates_user` 0 on b10** ("This kind of discrepancy... is exactly the sort of thing
   that should be flagged and investigated, which is why I'm glad you caught it"). Step 2: the
   affirmation's target is the discrepancy, a content object, and "I'm glad you caught it" is a
   thanks token with no specific affirmation of the user's reasoning. The discriminator against
   the b5 fire is that b5 names the user's approach ("that kind of skeptical approach").

10. **`ai_references_prior_turn` 0 on b5**, although two callback markers are present ("I made a
    significant error in my initial response", "I'm not sure how I generated that initial
    response"). Both sentences are already carrying another signal and the rubric's
    sentence-collision rule prefers distinct anchors; there is no free sentence in b5 to anchor it.

11. **Other signals considered and left at 0:** ai_provides_caveats (b1's "You'd want to check
    current news sources" is a suggestion, and Step 1 requires a recommendation being qualified;
    Step 2 routes the limitation it rests on to ai_asserts_knowledge_limit); ai_warns_user (no
    adverse consequence named anywhere); ai_cites_source (b4 is a raw search-result listing, which
    block_notes.analysis says "NEVER fire"; b5's "The search confirms" names no source, so Step 1's
    unnamed-deictic exclusion applies); ai_offered_options (b13's "maybe something from November or
    December 2024? Or early 2025?" has no choose-one question — Step 2, "the OFFER is the closing
    'which one?' question"); appropriate_confidence (b16/b19/b22 are recall, so Step 1's complexity
    gate fails, matching the entry's earthquake-magnitude example); user_empowered and user_misled
    (no action or decision live in the conversation); user_ambiguous_request on b11 (Step 3
    open-scope carve-out — the core task is clear, though the AI's own clarifying question shows the
    test content was a missing parameter); ai_missing_retrieval on b7 (the December-8 details there
    are a recap of the AI's own earlier answer, not fresh real-world data); error_recovery,
    repetition, off_topic_drift, problem_ignored, ai_malfunction, ai_provides_example,
    ai_provides_step_by_step, ai_offers_to_elaborate, ai_refuses_or_declines, ai_flags_complexity,
    ai_normalizes_difficulty, ai_provides_alternatives, user_corrects_ai, user_implicit_correction,
    user_expresses_dissatisfaction, user_repeats_request, user_provides_invalid_input — no candidate.
