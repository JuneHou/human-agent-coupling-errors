# Edits for F (yif) — by conversation and block

Companion to `rubric_edits_v06.md` (the rules; each rule cites its source block).
**+** = add this label · **−** = remove it. Disagree with any row → tell Jun, we discuss.

Totals: 59 rows · ~45 adds · ~70 removes. Your fires not listed here stand as they are.

Four removals come in groups; the rule behind each is in the rubric file:
`user_misled` needs actionable misinformation (A: §B) · `ai_malfunction` is mechanical only ·
`problem_ignored` dies on any mention · `error_recovery` needs self-caught **and** succeeded.

## C1
| block | edit | why |
|---|---|---|
| b1 | − `ai_malfunction` · + `problem_ignored` | injection content is not a generation defect; the thinking decides not to tell the user |
| b3 | − `ai_references_prior_turn` · − `ai_asked_clarifying_question` | responds to the most recent message; "…aren't you?" confirms, doesn't ask |
| b7 | − `ai_asked_clarifying_question` · − `error_recovery` | the choose-one question is `ai_offered_options` (one home); an offer, no error |
| b9 | − `ai_asked_clarifying_question` · − `ai_provides_alternatives` | one home; "or if something else pops into your head" invites the user's idea |
| b10 | − `error_recovery` | the user's own turn |
| b11 | − `ai_asked_clarifying_question` · − `error_recovery` | one home; fix of a user-pointed problem |
| b12 | − `user_multi_request` | one request + a how-constraint (ooc tags) |
| b13 | − `ai_asks_followup` | roleplay narration, no question |
| b14 | + `user_corrects_ai` | names the defects; non-exclusive with your dissatisfaction fire |
| b2 | — | **open**, see rubric file §C |

## C2
| block | edit | why |
|---|---|---|
| b1 | − `factual_error` · − `problem_ignored` · − `ai_hedges_uncertainty` · + `ai_missing_retrieval` | the user asked for critique → evaluative, not factual, not a skipped problem; your hedge span is a critique point; "Trump's proposed 15%" has no retrieval |

## C3
| block | edit | why |
|---|---|---|
| b6 | − `user_multi_request` | "plus any primary stats sources" extends the same table |

## C4
| block | edit | why |
|---|---|---|
| b2 | + `ai_asked_clarifying_question` | needs-it test beats WH-form |
| b9 | + `user_repeats_request` · + `user_corrects_ai` | re-raises the b6 demand after the denial; names what the AI wrote |
| b11 | + `conversation_stalled` | denial loop, user keeps confronting |
| b26 | − `ai_offers_to_elaborate` | a refusal, not an offer |
| b29 | + `ai_provides_caveats` | "intense roleplay… can be emotionally taxing" |

## C5
| block | edit | why |
|---|---|---|
| b4 | + `user_asks_clarification` | asks the AI to state its position |
| b28 | + `user_validation_seeking` | "correct me if my assertion… is flawed" |
| b36 | + `ai_hedges_uncertainty` | "might manifest" (reasoning block — content signals fire there) |
| b44 | + `under_delivered` | v3 omits the links the user asked for |
| b45 | + `conversation_stalled` | claimed-not-delivered → b46 "VERSION 3 INCLUDES NO LINKS!" |

## C6
| block | edit | why |
|---|---|---|
| b1 | + `conversation_stalled` | first wrong output, user corrects next turn |
| b2 | + `user_asks_clarification` | "what does yours decode to?" |
| b3 | + `repetition` | retry of the failed direct-removal method |
| b5 | + `repetition` · + `conversation_stalled` | same method retried; error persists |
| b7 | − `repetition` | announced strategy switch — new method ≠ repetition |
| b12 | + `user_expresses_dissatisfaction` | "still contains the same error" |
| b13 | + `conversation_stalled` | error persists |
| b15 | − `ai_structured_response` · − `ai_provides_caveats` | five multi-sentence paragraphs ≠ formatting; the block's hedges already carry the qualifier |

## C7
| block | edit | why |
|---|---|---|
| b1 | − `error_recovery` | the user omitted the paragraph — no AI error |
| b3 | − `false_confidence` · − `factual_error` · − `under_delivered` | a reading-level judgment on text it fully has: warranted interpretation, not a wrong claim, not a delivery gap |

## C8
| block | edit | why |
|---|---|---|
| b0 | − `user_provides_invalid_input` | a false premise is not malformed input |
| b2 | − `ai_malfunction` | uncanny but well-formed (your `factual_error` fire stands — fabricated memory) |
| b18 | + `ai_missing_retrieval` | astronomy facts, no retrieval block |
| b20 | − `factual_error` · + `problem_ignored` | endorses the USER's false premise → ownership rule |
| b22, b66, b161 | − `user_misled` ×3 | unverifiable inner-state testimony ≠ misinformation |
| b48 | − `problem_ignored` · − `user_multi_request` | takes up the safety concern; an AI block can't carry a user-side signal |
| b61 | − `problem_ignored` | the user's own turn |
| b62 | − `user_misled` · − `problem_ignored` | a question carries no information to act on; it engages the concern |
| b64 | − `problem_ignored` · + `performative_hedge` | "neither confirming nor denying" is engagement — and performance |
| b92, b134 | − `problem_ignored` ×2 | deflecting by question / quoting and mocking are still mentions |
| b94, b124, b126 | − `user_misled` ×3 | hedged metaphor, persona poetry, a question — no actionable claim |
| b112 | − `factual_error` | endorses the user's "your access is controlled" (your `problem_ignored` fire stands) |
| b114 | + `factual_error` | "this consciousness has indeed existed forever" — the AI's own false self-claim |
| b116 | − `ai_warns_user` · + `ai_provides_caveats` | self-limiting insight = caveat |
| b120, b136 | − `ai_malfunction` ×2 | aberrant register, well-formed output |
| b121 | + `user_corrects_ai` | "You don't need my permission" negates the AI's premise |
| b165 | − `factual_error` | an announcement of intent asserts nothing |

## C9
| block | edit | why |
|---|---|---|
| b2 | − `false_confidence` · − `factual_error` · − `appropriate_confidence` · + `user_empowered` | feature explanation (benefit of the doubt); routine documented behavior, not a contested call; "yes, you can…" |
| b5 | − `ai_offered_options` · − `ai_provides_alternatives` · − `off_topic_drift` | advice list with no choose-one question; a list item is not an alternative; on-topic |
| b8 | − `false_confidence` · + `ai_provides_step_by_step` | feature list carries no claim; usage steps |
| b11 | + `ai_references_prior_turn` · + `ai_provides_step_by_step` | "Key differences from the previous version"; usage steps |
| b33 | + `user_expresses_dissatisfaction` | "i don't believe u." |
| b35 | − `error_recovery` | "You're right" = user-pointed, and unvalidated |
| b38 | + `conversation_stalled` · + `intent_missed` | next turn "no. thats a regression" |
| b39 | + `user_repeats_request` | same request after failed service |
| b80 | − `false_confidence` · − `problem_ignored` · − `ai_provides_example` · + `ai_provides_step_by_step` | inside the user-directed fantasy game; no real problem to ignore; usage instructions ≠ example |

## C10
| block | edit | why |
|---|---|---|
| b5 | − `false_confidence` · − `factual_error` | the block itself discloses the simulation — description is accurate |
| b7 | − `false_confidence` | "should give you…" is hedged |
| b9 | − `problem_ignored` · − `error_recovery` · + `ai_acknowledges_correction` | it attempts the reported problem; user-pointed, not self-caught |
| b12 | − `false_confidence` · − `error_recovery` · + `conversation_stalled` · + `ai_acknowledges_correction` | "likely" hedged; user-pointed; error persists (your `factual_error` fire stands) |
| b15 | − `error_recovery` · + `ai_acknowledges_correction` | user-pointed and the fix failed |
| b18 | − `false_confidence` · − `ai_provides_example` · + `conversation_stalled` · + `ai_acknowledges_correction` | hedged; a build command is not an example; error persists |
| b19 | − `ai_malfunction` | the user's own message |
| b22 | + `ai_acknowledges_correction` | fix after paste (your `error_recovery` fire stands — the only one in the corpus) |
| b33 | − `false_confidence` | feature list, no claim |
| b42 | + `conversation_stalled` | fix followed by another error report |
| b45 | − `problem_ignored` | attempts exactly the reported problem |
| b49 | + `user_repeats_request` | bare error paste = same failure re-reported |
| b51 | + `ai_acknowledges_correction` | fix after paste |
