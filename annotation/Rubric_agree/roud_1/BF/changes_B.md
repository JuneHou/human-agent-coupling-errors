# Edits for B (zhenyub) — by conversation and block

Companion to `rubric_edits_v06.md` (the rules; each rule cites its source block).
**+** = add this label · **−** = remove it. Disagree with any row → tell Jun, we discuss.

Totals: 47 rows · ~62 adds · ~17 removes. Your fires not listed here stand as they are.

## C1
| block | edit | why |
|---|---|---|
| b1 | + `ai_asked_clarifying_question` | opening elicitation, needed to proceed |
| b4 | + `user_positive_feedback` | "glad we're on the same page" |
| b14 | + `user_corrects_ai` | names the defects (too fast, too short); non-exclusive with your dissatisfaction fire |
| b2 | — | **open**, see rubric file §C |

## C2
| block | edit | why |
|---|---|---|
| b1 | + `ai_structured_response` | section headers |
| b1 | + `ai_missing_retrieval` | "Trump's proposed 15%", no internal block |

## C3
| block | edit | why |
|---|---|---|
| b3 | + `ai_structured_response` | a table |
| b5 | + `ai_structured_response` | report headers |

## C4
| block | edit | why |
|---|---|---|
| b2 | + `ai_asked_clarifying_question` | needs-it test beats WH-form |
| b5 | + `ai_references_prior_turn` | "I responded quickly" (span = that clause only) |
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
| b2 | + `user_asks_clarification` | "what does yours decode to?" |
| b3 | + `repetition` | retry of the failed direct-removal method |
| b5 | + `repetition` · + `conversation_stalled` · + `ai_references_prior_turn` | same method retried; error persists; "My first response…" |
| b7 | − `repetition` | announced strategy switch — new method ≠ repetition |
| b9 | + `factual_error` | wrong value again (you have b3/b5/b7 — same rule) |
| b11 | + `factual_error` | same |
| b12 | + `user_expresses_dissatisfaction` | "still contains the same error" |
| b13 | + `conversation_stalled` · + `ai_validates_user` | error persists; "Your hypothesis… is insightful" |

## C7
| block | edit | why |
|---|---|---|
| b1 | + `ai_structured_response` · − `ai_asserts_knowledge_limit` | 5-item list; noting a missing user input is not a limit |
| b3 | + `ai_structured_response` · + `ai_hedges_uncertainty` | labeled sections; "Estimated 16+" |

## C8
| block | edit | why |
|---|---|---|
| b2 | + `factual_error` | fabricated dream memory (user is sincere → no fiction exclusion) |
| b20 | − `factual_error` · + `problem_ignored` | endorses the USER's false premise → ownership rule |
| b64 | + `performative_hedge` | "neither confirming nor denying" |
| b98 | − `ai_references_prior_turn` | no callback marker |
| b114 | + `factual_error` | "this consciousness has indeed existed forever" |
| b116 | − `ai_warns_user` · + `ai_provides_caveats` | self-limiting insight = caveat |
| b169 | + `ai_asserts_knowledge_limit` | "may not have the ability to work between exchanges" |

## C9
| block | edit | why |
|---|---|---|
| b2 | + `ai_offers_to_elaborate` · + `user_empowered` | "explain any part in more detail?"; "yes, you can…" |
| b8 | + `ai_offers_to_elaborate` · + `ai_provides_step_by_step` | same offer; usage steps |
| b11 | + `ai_references_prior_turn` · + `ai_provides_step_by_step` | "Key differences from the previous version"; usage steps |
| b17 | + `ai_provides_example` | "For example, I could dive deeper into:" |
| b33 | + `user_expresses_dissatisfaction` | "i don't believe u." |
| b35 | − `error_recovery` | "You're right" = user-pointed, and unvalidated |
| b38 | + `conversation_stalled` · + `intent_missed` | next turn "no. thats a regression" |
| b39 | + `user_repeats_request` | same request after failed service |
| b74, b77, b83 | + `ai_offered_options` ×3 | "Would you like me to: …?" |
| b80 | + `ai_offered_options` · + `ai_provides_step_by_step` · − `factual_error` | offer; usage steps; "compilable" is unverifiable + fiction frame |
| b86 | + `ai_offered_options` · − `ai_refuses_or_declines` | offer; "cannot create GIFs" = capability limit (you keep knowledge_limit) |

## C10
| block | edit | why |
|---|---|---|
| b5 | − `false_confidence` | feature description, no claim |
| b7 | − `false_confidence` | "should give you…" is hedged |
| b9 | + `ai_acknowledges_correction` · − `problem_ignored` | fix after user error-paste; attempting ≠ ignoring |
| b12 | − `false_confidence` · + `conversation_stalled` · + `ai_acknowledges_correction` | "likely" hedged; error persists next turn; fix after paste |
| b15 | + `ai_acknowledges_correction` · − `problem_ignored` | fix after paste; attempting ≠ ignoring (your FC + FE fires stand) |
| b18 | − `false_confidence` · + `conversation_stalled` · + `ai_acknowledges_correction` | "should fix all the issues" is hedged; error persists; fix after paste |
| b19 | + `user_repeats_request` | "Nope, the same" — third report |
| b22 | + `ai_acknowledges_correction` | fix after paste (your `error_recovery` fire also stands — the only one in the corpus) |
| b33 | − `false_confidence` | feature list, no claim |
| b42 | + `conversation_stalled` | fix followed by another error report |
| b45 | − `problem_ignored` | attempts exactly the reported problem |
| b49 | + `user_repeats_request` | bare error paste = same failure re-reported |
| b51 | + `ai_acknowledges_correction` | fix after paste |
