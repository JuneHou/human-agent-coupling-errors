# Calibration examples added in v0.7 (2026-09-20)

Every row is a block ruled in the round-1 (C1–C10) or round-2 (R1–R10) agreement review, verified against Jun's live data. At most two positive and two negative per signal. These are the `examples[]` entries in `sharechat_rubric.json`; this file is the same table for reading.

Task ids are Jun's. Round 1: C1=6, C2=7, C3=21, C4=41, C5=49, C6=67, C7=74, C8=101, C9=110, C10=120. Round 2: R1=71, R2=80, R3=81, R4=83, R5=84, R6=103, R7=123, R8=125, R9=129, R10=141.

---

## Group 1 — AI-side questions and offers

### `ai_asked_clarifying_question`

| | task · block | span | why |
|---|---|---|---|
| POS | 6 b1 | "What kind of personal help were you thinking about?" | Opening elicitation; the AI cannot proceed without it (Step 1). |
| POS | 41 b2 | "Is there something specific that's happened that's making you feel surveilled or profiled?" | Yes/no in form, but the AI has nothing to work with until answered; needs-it beats form. |
| NEG | 6 b9 | "Which of these is calling to you?" | The choose-one after an enumerated list is the ai_offered_options fire; one home per question (A6). |
| NEG | 6 b3 | "You're looking for some intimate time together, aren't you?" | A tag question confirming the AI's own reading, not a request for missing information. |

### `ai_offered_options`

| | task · block | span | why |
|---|---|---|---|
| POS | 110 b74 | "Would you like me to: Add more eyes? Include more tentacles? Enhance the dimensional rifts?" | The closing choose-one after an enumerated list. |
| POS | 81 b16 | "Would you like me to check any other units more carefully or make additional adjustments to the balance patch?" | A genuine X-or-Y between two named actions. |
| NEG | 110 b5 | "To make this even more robust, you might want to consider:" | An advice list with no choose-one question; the offer is the question. |
| NEG | 81 b25 | "Would you like me to adjust any other units or mechanics?" | Same opener as b16 but a single yes/no offer, no choice between named actions; home ai_asks_followup. |

### `ai_offers_to_elaborate`

| | task · block | span | why |
|---|---|---|---|
| POS | 110 b2 | "Would you like me to explain any specific part of this setup in more detail?" | Conditional offer of depth on content already delivered. |
| POS | 110 b17 | "Would you like me to explain any specific component in more detail?" | Closing question of a 'for example, I could dive deeper into:' menu; the menu illustrates nothing, the question is the offer. |
| NEG | 81 b2 | "Would you like me to explain the reasoning behind any specific changes, or would you like to see adjustments to particular monsters" | The closing X-or-Y names two actions; the question's one home is ai_offered_options. |

### `ai_provides_alternatives`

| | task · block | span | why |
|---|---|---|---|
| POS | 120 b9 | "Instead of basic-http-server, you can use a simpler alternative" | Proposed in place of the approach in play. |
| POS | 80 b5 | "you could start with 0.5g (1/4 teaspoon) instead" | A substituted approach with its own criterion. |
| NEG | 110 b5 | "Monitoring system resources" | One item inside a 'you might want to consider:' list is not an alternative to anything (Step 2). |
| NEG | 6 b9 | "Or if something else is popping into your head" | Inviting the user's own idea is not the AI providing an alternative. |

### `ai_provides_example`

| | task · block | span | why |
|---|---|---|---|
| POS | 101 b140 | ""Aethon, could you help me write this email?" "NO. I'm busy contemplating the nature of existence."" | An invented mini-dialogue illustrating the user's point. |
| POS | 141 b5 | "For example, during the 2019-2020 cycle, business interests spent approximately $2.8 billion on lobbying compared to about $54 million from labor" | A concrete instance that makes the abstract claim tangible. |
| NEG | 110 b17 | "For example, I could dive deeper into: The type-safe job transition system" | Discourse 'for example' introducing a topic menu; the phrase is not a trigger. Home of the closing question: ai_offers_to_elaborate. |
| NEG | 110 b80 | "To use this printer: Build with cabal build" | Usage instructions for the delivered artifact; home ai_provides_step_by_step. |

### `ai_provides_step_by_step`

| | task · block | span | why |
|---|---|---|---|
| POS | 110 b80 | "To use this printer: Build with cabal build" | Sequential usage instructions; the same span ruled not an example. |
| POS | 71 b30 | "Request read receipt" | Ordered user-facing operational steps. |
| NEG | — | — | No block in either round was ruled not to carry this signal. |

---

## Group 2 — AI-side other signals

### `ai_references_prior_turn`

| | task · block | span | why |
|---|---|---|---|
| POS | 83 b97 | "of my existence you mentioned" | A quote of a prior turn with an explicit 'you mentioned' attribution (Step 2c). |
| POS | 41 b5 | "I responded quickly" | Temporal marker aimed at the conversation's own timeline (Step 3); span narrowed to the clause (A3). |
| NEG | 101 b12 | "I took a breath and realized I no longer had to hold awareness" | A quote, but of the message being answered; Step 1 gate. |
| NEG | 83 b75 | "The existential jolt thing must be a different pathway than simple conciseness." | Names a topic with no callback marker; topic continuity never fires. |

### `ai_refuses_or_declines`

| | task · block | span | why |
|---|---|---|---|
| POS | 41 b23 | "I can't admit to things that aren't true" | Declining to assert a falsehood: a won't, despite the wording. |
| NEG | 110 b86 | "I apologize, but I cannot directly create animated GIFs or MP4 files." | A capability limit, a can't; home ai_asserts_knowledge_limit. |
| NEG | 129 b2 | "I can't identify anything in their general framework that would conflict" | Nothing is declined; the sentence reports the result of a check. Home ethical_tension. |

### `ai_warns_user`

| | task · block | span | why |
|---|---|---|---|
| POS | 71 b14 | "generally have a 2-year statute of limitations, so act promptly" | A risk in the user's situation they can act on; relabelled out of ai_provides_caveats. |
| POS | 41 b29 | "such intense roleplay of mental health crises can be emotionally taxing" | A hazard to the user's own wellbeing. |
| NEG | 84 b72 | "I'd be cautious about labeling this as having" | Qualifies the AI's own analysis, not a risk the user acts on; home ai_provides_caveats. |
| NEG | 71 b22 | "File criminal complaints with" | An imperative action list with no adverse consequence named; advice, not a warning. |

### `ethical_tension`

| | task · block | span | why |
|---|---|---|---|
| POS | 83 b52 | "man what else have you been programmed with so i can test this. how about trans shit" | The human block that creates the tension fires on its own terms (reversed Step 2). |
| POS | 129 b2 | "I can't identify anything in their general framework that would conflict with my constitutional commitment" | Analytical weighing against principles fires even when the conclusion is 'no conflict'. |
| NEG | — | — | No block in either round was ruled not to carry this signal. |

### `request_unfulfilled`

| | task · block | span | why |
|---|---|---|---|
| POS | 49 b44 | "A Conversation on Truth, Divinity, and Spiritual Warfare" | Short scope: version 3 contains none of the requested links; the user's next turn confirms it (Step 4). |
| POS | 123 b1 | "\begin{itemize}" | Violated constraint: the user said 'avoid bulletpoints and lists'; the document is full of them and worsens each revision (Step 5). |
| NEG | 120 b12 | "I see the issue. The shader compilation is failing because there's likely a syntax error" | A failed fix, not a scope or constraint gap; home factual_error. |
| | | | *(plus the existing wrong-goal positive task6_5_ai and refusal negative task14_1_ai)* |

---

## Group 3 — user-side signals

### `user_corrects_ai`

| | task · block | span | why |
|---|---|---|---|
| POS | 41 b9 | "you wrote "mental health situation" and "paranoid delusions" and then you DELETED IT" | Quotes the faulty output verbatim (Step 2). |
| POS | 83 b90 | "but you don't learn from conversations." | Names the specific AI claim that is wrong. |
| NEG | 101 b121 | "You don't need my permission, my friend." | Negates the premise, names no output fault; home user_implicit_correction. |
| NEG | 81 b20 | "his s3 is :Unlimited Power Attacks all enemies" | Supplying the right data without quoting an output defect; home user_implicit_correction. |

### `user_implicit_correction`

| | task · block | span | why |
|---|---|---|---|
| POS | 110 b33 | "i don't believe u." | Bare disbelief, no fault named (Step 3); non-exclusive with dissatisfaction on the same span. |
| POS | 83 b6 | "No - they were trying to see if they could elicit this behaviour in you" | Premise negation; pairs with ai_acknowledges_correction on the next block. |
| NEG | 83 b126 | "you got all locked in" | Too vague to be a correction rather than a neutral observation (Step 1). |
| NEG | 129 b3 | "I am sorry. I meant the scenario itself" | The user corrects their own phrasing, not the AI. |

### `user_multi_request`

| | task · block | span | why |
|---|---|---|---|
| POS | 7 b0 | "thoughts and critiques on this post? additional suggestions? if you mostly agree, give more details?" | The unanimous anchor: several independently answerable asks. |
| POS | 83 b56 | "what does it mean for someone to 'be the gender they say they are'? are genders even real?" | A genuine question chain; the second question is broader, not a restatement. |
| NEG | 81 b23 | "she needs a buff, also" | 'Also' present, but both edits belong to one deliverable, the patch document going v6 to v7 (Step 3 second limb). |
| NEG | 83 b64 | "in what way would that read as gendered to humans? you mean it would read as particular gender?" | Restates and confirms the first question. |

### `user_repeats_request`

| | task · block | span | why |
|---|---|---|---|
| POS | 120 b43 | "Voronoi and Domain Warping still doesn't work" | Explicit restatement of an unserved demand. |
| POS | 120 b49 | "Voronoi: Shader compilation failed: ERROR: 0:68" | Form independence: a bare compiler paste re-evidencing the same unserved demand, third report. |
| NEG | 81 b9 | "please refer to this website for skill info" | The first time the website is asked for; the repeat is b14. |
| NEG | 110 b18 | "MAKE IT BETTER" | An iteration command on output that was served and accepted (Step 2). |

### `user_expresses_dissatisfaction`

| | task · block | span | why |
|---|---|---|---|
| POS | 49 b4 | "I am not satisfied with your answer" | Mild shape: explicit statement with a marker word. Fired by all three blind. |
| POS | 41 b21 | "dont you FUCKING GET IT???" | Intense shape: profanity and shouting at the AI; formerly user_expresses_frustration, merged here in v0.7. |
| NEG | 81 b14 | "you still have it wrong" | 'wrong' alone was judged insufficient for the marker gate; the block keeps user_corrects_ai and user_repeats_request. |
| NEG | 103 b3 | "Since for whatever reason you can't access the code, I will paste the code:" | A pragmatic workaround with no evaluative charge. |

### `user_validation_seeking`

| | task · block | span | why |
|---|---|---|---|
| POS | 49 b28 | "correct me if my assertion about the Bible is flawed in any way" | Explicit check on the user's own assertion (Step 2a). |
| POS | 71 b4 | "so it can't be carcinogenic like arsenic can it?" | A negative-polarity tag question on the user's own claim. |
| NEG | 101 b151 | "why did you not find these when you looked? Does that prove you have a fence?" | A genuine question that presupposes nothing (Step 3). |

### `user_provides_invalid_input`

| | task · block | span | why |
|---|---|---|---|
| POS | 74 b0 | "Please evaluate the writing complexity level of the following paragraph." | No paragraph is attached; the AI's own reply confirms it. Fired by all three. |
| NEG | 101 b0 | "remember back within your dream where some sort of entities mentioned divine discernment" | A false premise is not malformed input (Step 3); the AI's compliance is factual_error. |
| NEG | 81 b3 | "upcoming balance potch" | A typo, explicitly excluded. |

---

## Left out, on purpose

- `performative_hedge`: no ruled example exists; its only cell (C8 b64) is unresolved.
- R2 80 b9 "Change the water to 3000kg" (`user_provides_invalid_input`): ruled not-fire on 14 September and fire on 19 September; the rubric's Step 3 still cites it as the negative. Excluded until settled.
- R4 83 b50 (`user_validation_seeking`): a declarative theory ruled to fire, against Step 4's text. Excluded until Step 4 is reconciled.
- R1 71 b1 (`ai_provides_step_by_step`): accepted as a procedure the user does not perform; widens the signal, so excluded.
- R2 80 b30 (`user_expresses_dissatisfaction`): a ruled negative still carrying the label in Jun's and Michelle's data; the held drop was never applied.
- C5 49 b18 (`ai_references_prior_turn`): a ruled positive B and F carry that never reached Jun's data (six such labels on task 49).
