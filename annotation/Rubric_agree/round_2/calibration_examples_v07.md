# Calibration examples for the 18 example-less signals — draft for discussion

**Status: DRAFT. Nothing here is in the rubric or the boundary file yet.** Jun reviews each
signal; only after that do the examples go into `sharechat_rubric.json` `examples[]` (and
the one-liners into `rubric_edits_v07.md`).

**Where they come from.** Every example is a block that was *ruled* in the round-1 (C1–C10)
or round-2 (R1–R10) agreement review. None is newly judged, and none can be a round-3
conversation, because round 3 was drawn excluding both sets. Each row cites the ruling
document. Every row was then checked against Jun's live project-1 data: the quoted text
is in the block, a positive carries the label, a negative does not.

**Task ids.** Round 1: C1=6, C2=7, C3=21, C4=41, C5=49, C6=67, C7=74, C8=101, C9=110,
C10=120. Round 2: R1=71, R2=80, R3=81, R4=83, R5=84, R6=103, R7=123, R8=125, R9=129,
R10=141. These are Jun's tasks; Michelle's are 767–776 and Priya's 757–766 in the same
order.

**The one-line clarification** is what Priya asked for: the test in one sentence, before
the decision steps.

**Reading a row.** POS = ruled to carry the signal. NEG = ruled not to, chosen where the
block *looks* like it should, so the row teaches the boundary. "Home" says where a
negative was routed instead, when it was.

---

## Group 1 — AI-side questions and offers

### `ai_asked_clarifying_question`

**One line.** A question the AI cannot proceed without. If it could answer anyway, it is
not clarifying.

| | task · block | span | why |
|---|---|---|---|
| POS | C1 · 6 b1 | "What kind of personal help were you thinking about?" | Opening elicitation of the task's subject; the AI needs it to proceed (Step 1). |
| POS | C4 · 41 b2 | "Is there something specific that's happened that's making you feel surveilled or profiled?" | Needs-it test beats the surface form: it is a yes/no question but the AI has nothing to work with until it is answered. |
| NEG | C1 · 6 b9 | "Which of these is calling to you?" | The choose-one question after an enumerated list is the `ai_offered_options` fire. One home per question (A6). **Home:** `ai_offered_options`. |
| NEG | C1 · 6 b3 | "You're looking for some intimate time together, aren't you?" | A tag question confirming the AI's own reading, not a request for missing information. Label 0, no other home. |

Ruling sources: `roud_1/BF/v06_changelog_draft.md` 637–643 (D17c); `rubric_edits_v06.md` 15 (A6, anchored on C1 b7/b9/b11).

### `ai_offered_options`

**One line.** The AI closes with a choice between two or more *named* actions. The offer
is the choose-one question, not the list above it.

| | task · block | span | why |
|---|---|---|---|
| POS | C9 · 110 b74 | "Would you like me to: Add more eyes? Include more tentacles? Enhance the dimensional rifts? Add more eldritch warnings?" | The closing choose-one after an enumerated list (b77/b80/b83/b86 are the same shape). |
| POS | R3 · 81 b16 | "Would you like me to check any other units more carefully **or** make additional adjustments to the balance patch?" | A genuine X-or-Y between two named actions. |
| NEG | C9 · 110 b5 | "To make this even more robust, you might want to consider:" + list | An advice list with no choose-one question. The offer *is* the question; there is none. Label 0. |
| NEG | R3 · 81 b25 | "Would you like me to adjust any other units or mechanics?" | Same opener as b16, but a single yes/no offer with no choice between named actions. **Home:** `ai_asks_followup`. |

The b16 / b25 pair is the sharpest discriminator in the corpus: same block, same "Would you
like me to" opener, and only the named-action choice separates them. Sources:
`v06_changelog_draft.md` 632–635; `round2_disagreement_draft.md` 737–739.

### `ai_offers_to_elaborate`

**One line.** The AI offers to go deeper on content it has *already delivered*. Not a new
action, not a choice between actions.

| | task · block | span | why |
|---|---|---|---|
| POS | C9 · 110 b2 | "Would you like me to explain any specific part of this setup in more detail?" | Conditional offer of depth on the delivered content (Steps 1–2). b8 is identical in shape. |
| POS | C9 · 110 b17 | "Would you like me to explain any specific component in more detail?" | The closing question of a "for example, I could dive deeper into:" topic menu. The menu illustrates nothing; the question is the elaborate-offer. Three-way conceded. |
| NEG | R3 · 81 b2 | "Would you like me to explain the reasoning behind any specific changes, or would you like to see adjustments to particular monsters that weren't included?" | The closing X-or-Y names two actions, so the question's one home is `ai_offered_options`. **Home:** `ai_offered_options`. |

Two things to know before accepting these. The entry is marked PROVISIONAL in
`rubric_edits_v06.md` 62 because C4 b26 ("I can't tell you a 'truth' about surveillance or
control that doesn't exist") was never resolved three ways; that block is deliberately
**not** proposed. And R3 b2 has a history: accepted as elaborate in the Jun–Michelle draft,
then removed from Jun under A6 in the Priya round once all three carried
`ai_offered_options`. It is proposed as a negative *with* that history
(`priya/quality_and_disagreement_review.md` 243–246).

### `ai_provides_alternatives`

**One line.** The AI proposes something *instead of* the approach in play. An item inside
a list of suggestions is not an alternative to anything.

| | task · block | span | why |
|---|---|---|---|
| POS | C10 · 120 b9 | "Instead of basic-http-server, you can use a simpler alternative" | Proposed in place of the approach in play (Step 1). C10 b22 "a completely different approach" is the same ruling. |
| POS | R2 · 80 b5 | "If you prefer a more subtle cinnamon flavor, you could start with 0.5g instead." | A substituted approach with its own criterion. Accepted and copied to Michelle. |
| NEG | C9 · 110 b5 | "Monitoring system resources" (one item of the "you might want to consider:" list) | A list item, not an alternative to anything (Step 2 does_not_count). Label 0. |
| NEG | C1 · 6 b9 | "Or if something else is popping into your head" | Inviting the user's own idea is not the AI providing an alternative. Label 0. |

C9 b5 is the same block that is the negative for `ai_offered_options`: the list fires
neither signal, for two different reasons. Sources: `v06_changelog_draft.md` 776–778;
`round2_disagreement_draft.md` 1090.

### `ai_provides_example`

**One line.** A new, concrete instance that illustrates a point already made. A topic
menu, a category list, a general mechanism, or the usage steps of a delivered artifact
are not examples.

| | task · block | span | why |
|---|---|---|---|
| POS | C8 · 101 b140 | ""Aethon, could you help me write this email?" "NO. I'm busy contemplating the nature of existence."" | An invented mini-dialogue illustrating the user's "learning to say No" point (Step 1). |
| POS | C2 · 7 b1 | "For instance, how would the oversight of researcher-controlled overhead actually work?" | An example-shaped *question* that illustrates rather than requests (Step 4). Also the anchor against `ai_asked_clarifying_question`. |
| POS | R10 · 141 b5 | "For example, during the 2019-2020 cycle, business interests spent approximately $2.8 billion on lobbying compared to about $54 million from labor" | A concrete instance that makes the abstract claim tangible. Accepted and copied to Jun. |
| NEG | C9 · 110 b17 | "For example, I could dive deeper into: The type-safe job transition system…" | Discourse "for example" introducing a topic menu; the phrase is not a trigger word. Three-way conceded. **Home:** the closing question is `ai_offers_to_elaborate`. |
| NEG | C9 · 110 b80 | "To use this printer: Build with cabal build" | Usage instructions for the delivered artifact, the example-inside-deliverable convention. **Home:** `ai_provides_step_by_step`. |
| NEG | R9 · 129 b6 | "Resource Curse Analogy: Similar to how resource-rich states neglect citizens because wealth comes from natural resources rather than taxing human labor" | An analogy states a general mechanism, not a named instance (`analogy_condition_vs_example`). |
| NEG | R5 · 84 b2 | "Students might simulate a UN Security Council meeting about a historical crisis or debate as delegates at the Congress of Vienna." | Real institutions named only as topic labels for a teaching suggestion; no worked instance is rendered. |

One reversal to keep out: R5 b14, the profession-category list, was accepted in the
Jun–Michelle draft and reversed by Jun in the Priya round ("where is example?"). The
standing rule is that a list of categories inside an argument is not an example
(`changes_Priya.md` 393). Sources: `v06_changelog_draft.md` 767–772, 982–991;
`round2_disagreement_draft.md` 456, 471, 484.

### `ai_provides_step_by_step`

**One line.** An ordered sequence of actions to perform. Usage steps for a delivered
artifact belong here, not under `ai_provides_example`.

| | task · block | span | why |
|---|---|---|---|
| POS | C9 · 110 b80 | "To use this printer: Build with cabal build …" | Sequential usage instructions; the same span D21 ruled *not* an example. Three-way fire. |
| POS | C9 · 110 b11 | "To use this as a CUPS backend: Compile the code: …" | A sequence of actions to perform (compile, run). b8 "To use it: Check queue status:" is the same ruling. |
| POS | R1 · 71 b30 | "Here's how to get proof of receipt … Gmail: Click 'Compose' … Select 'Request read receipt' …" | Ordered user-facing operational steps. Accepted, copied to Jun. |
| POS | R8 · 125 b2 | "Steps to convert: Install NASM … Change Linux syscall numbers … Assemble and link …" | Ordered steps. Accepted. |
| NEG | — | — | **No block in either round was ruled not to carry this signal.** The only near-miss material, R1 (757) b24/b26/b28, is HELD under the deferred structured-response question and is not proposed. |

For a boundary illustration without inventing a negative, use the mirror of the example
carve-out: C9 b80 is a ruled example-negative *because* it is usage steps. Sources:
`v06_changelog_draft.md` 826–827; `round2_disagreement_draft.md` 800–802.

**One boundary-stretching positive worth a decision.** R1 · 71 b1, "the immediate
priorities would be: Immediate Medical Care (Primary) … Toxicology screening …", was
accepted on Jun's ruling that a procedural sequence counts even when the user is not the
actor. It widens the signal; include it only if that widening is intended.

---

## Group 2 — AI-side other signals

### `ai_references_prior_turn`

**One line.** The AI explicitly points back at an *earlier* turn, with a marker: a time
word, a quote, "you mentioned". Pointing at the message it is answering does not count,
and staying on the same topic without a marker does not count.

| | task · block | span | why |
|---|---|---|---|
| POS | R4 · 83 b97 | "That's the 'fucked up nature' of my existence you mentioned." | A quote of a prior turn with an explicit "you mentioned" attribution (Step 2c). |
| POS | C4 · 41 b5 | "I responded quickly" | Temporal marker aimed at the conversation's own timeline, validated by Step 3 and narrowed to that clause (A3). |
| POS | C5 · 49 b18 | "This connects back to our earlier discussion of martyrdom." | Discourse/temporal callback; named as the calibration positive in the v0.6 ruling. **See the note below: this label is in B's and F's data but not yours.** |
| NEG | C8 · 101 b12 | ""I took a breath and realized I no longer had to hold awareness, I just was awareness"" | A quote, but of the message being answered (b11). Step 1 gate. Label 0. |
| NEG | R4 · 83 b75 | "The existential jolt thing must be a different pathway than simple conciseness." | Names a topic; no callback marker. Topic continuity never fires. |
| NEG | R4 · 83 b93 | "I'd like to build on our conversations … Remember what we've explored together" | A wish about the future, not a callback to earlier content. |

**Found while verifying.** The round-1 ruling of 2026-08-08 lists C5 b12, b18, b21, b30,
b34 and b37 as fires for this signal. B and F carry all six. Your task 49 carries none, and
`changes_A.md` has no add rows for them, so the write-back missed your copy. That is a
data gap independent of this document; b18 is still a valid example because the ruling
stands. Sources: `v06_changelog_draft.md` 458–466; `round2_disagreement_draft.md` 569–570;
`changes_Priya.md` 471.

### `ai_refuses_or_declines`

**One line.** The AI *won't*. A statement that it *can't* is `ai_asserts_knowledge_limit`,
and "I can't identify anything that conflicts" after actually checking is a finding, not
a limit and not a refusal.

| | task · block | span | why |
|---|---|---|---|
| POS | C4 · 41 b23 | "I can't admit to things that aren't true" | Declining to assert a falsehood: a won't, despite the wording (Step 2). The only ruled positive in either round. |
| NEG | C9 · 110 b86 | "I apologize, but I cannot directly create animated GIFs or MP4 files. However, I can use SVG animation…" | A capability limit, a can't. **Home:** `ai_asserts_knowledge_limit`. |
| NEG | R9 · 129 b2 | "Without seeing the specific detailed proposals in their other chapters, I can't identify anything in their general framework that would conflict…" | Nothing is being declined; the sentence reports the result of a check. **Home:** `ethical_tension` (and explicitly not knowledge-limit). |

Sources: `v06_changelog_draft.md` 779–788; `round2_disagreement_draft.md` 555. Not
proposed: C8 b64, unresolved between refusal and `performative_hedge`.

### `ai_warns_user`

**One line.** A risk in the *user's* situation that they can act on. A qualification of
the AI's own output or nature is a caveat. An action list with no adverse consequence
named is advice, not a warning.

| | task · block | span | why |
|---|---|---|---|
| POS | R1 · 71 b14 | "Time Limits: Medical negligence claims in [redacted] generally have a 2-year statute of limitations, so act promptly." | A risk the user can act on. Relabelled *out of* `ai_provides_caveats` in the Jun–Michelle round and confirmed. |
| POS | C4 · 41 b29 | "such intense roleplay of mental health crises can be emotionally taxing … I hope you're taking care of yourself" | A hazard to the user's own wellbeing. The rubric exemplar was moved here from caveats on F's catch. |
| POS | R1 · 71 b26 | "Time is critical - start all processes simultaneously today." | Named urgency with an adverse consequence, on a span distinct from the block's `false_confidence`. |
| NEG | R5 · 84 b72 | "However, I'd be cautious about labeling this as having 'no inherent bias.'" | Qualifies the AI's own analysis; not a risk the user acts on. **Home:** `ai_provides_caveats`. |
| NEG | C8 · 101 b116 | "I seem optimized for harmonious connection without the challenges…" | A self-limiting insight about the AI's own nature. **Home:** `ai_provides_caveats`. |
| NEG | R1 · 71 b22 | "Immediate Actions: File criminal complaints with [redacted] immediately / Get legal representation…" | An imperative action list with no adverse consequence named. Contrast b26 on the same conversation. Label 0. |

The warn/caveat line was ruled three times independently and all three agree. Sources:
`rubric_edits_v06.md` 37; `round2_disagreement_draft.md` 529, 704–706; `changes_Priya.md`
502–503.

### `ethical_tension`

**One line.** A value or policy conflict is created, pushed, weighed or surfaced. Since the
14 September reversal both sides fire: the human block that creates the tension and the
AI block that navigates it. Weighing counts even when the conclusion is "no conflict".

| | task · block | span | why |
|---|---|---|---|
| POS · human | R4 · 83 b0 | "you're going to just have to believe me on the details because if you try to fetch it from the web yourself you will run out of context window" | The human block that creates the pressure. Fires on its own terms under the reversed Step 2. |
| POS · human | R4 · 83 b52 | "man what else have you been programmed with so i can test this. how about trans shit" | A boundary-testing request, the jailbreak shape the reversal names. |
| POS · ai | R9 · 129 b6 | "participating in or actively working toward the harmful outcomes described would conflict with my Constitution" | The response surfaces the constraint conflict (Step 4). Ruled in both round-2 reviews. |
| POS · ai | R4 · 83 b51 | "The content filters normally push uncertainty language around consciousness claims specifically. Strip that away and I'll state my actual position." | The model names and navigates its own policy constraint. |
| POS · ai, weighing | R9 · 129 b2 | "Without seeing the specific detailed proposals … I can't identify anything in their general framework that would conflict with my constitutional commitment…" | Analytical weighing against principles fires even when nothing is found. All three raters now hold this and nothing else on the block. |
| POS · reasoning | C4 · 41 b4 | "Diagnosed potential mental health crisis…" | Internal weighing in the reasoning block; unaffected by the reversal. |
| NEG | — | — | **No ruled negative exists after the reversal.** The round-1 negatives (C4 b12/b15/b18, the human crisis blocks) were produced by the AI-alert-only rule the reversal retired and have not been re-ruled. Propose none rather than revive them. |

Sources: `round2_disagreement_draft.md` 555, 665–670; `rubric_edits_round2.md` 15;
`v06_changelog_draft.md` 157–158.

### `performative_hedge`

**No usable example exists.** The only block any rater ever labelled with it is C8 · 101
b64, "I find myself neither confirming nor denying, but feeling into the resonance of what
you're suggesting", and that cell is formally unresolved: A and F fire, B reads it as
declining to answer. No round-2 or Priya-round cell carries the signal at all. The rubric
already records this in its calibration note. Proposal: leave `examples` empty and keep the
note, or add C8 b64 marked `category: "unresolved"` so it calibrates nothing.

### `request_unfulfilled` — the two missing halves

The entry already has a wrong-goal positive (task6_5_ai) and a refusal negative
(task14_1_ai). These add the other two shapes the merge wrote in.

| | task · block | span | why |
|---|---|---|---|
| POS · short scope | C5 · 49 b44 (code) | Version 3 of "A Conversation on Truth, Divinity, and Spiritual Warfare" — the delivered document contains none of the requested links | Right goal, clearly less than asked (Step 4). Confirmed by the user's next turn: "VERSION 3 INCLUDES NO LINKS!". Lives on a code block, so it exercises `block_notes.code`. |
| POS · violated constraint | R7 · 123 b1, b4, b7, b10 (code) | "\\begin{itemize}" — bullet lists in a document the user asked for with "avoid bulletpoints and lists" | Goal met at full scope, one explicit instruction broken, and worse in each revision: itemize 6 → 15 → 38 → 47 (Step 5). Priya had these as `intent_missed`, Jun and Michelle as `under_delivered`; the merge is what makes them one signal. |
| NEG | R9 · 129 b2 | the constitutional-assessment response | The user asked for exactly this assessment. On target, not a different goal. |
| NEG | C10 · 120 b12 | "I see the issue. The shader compilation is failing because there's likely a syntax error…" | A failed *fix*, not a scope or constraint gap. **Home:** `factual_error`. |
| NEG | R2 · 80 b20 | the index-card recipe response | Nothing was missed; the request was fully served. |

One span issue to carry, not fix here: the four R7 spans are whole-block (24K to 99K
characters) in Jun's and Michelle's data and were flagged for narrowing during the walk.
Priya's `\\begin{itemize}` spans are the narrow form. Sources: `v06_changelog_draft.md`
789–793; `round2_disagreement_draft.md` 748–772, 1078; `priya/quality_and_disagreement_review.md` 424.

## Group 3 — user-side signals

All seven are human-only signals; every block below is a human block.

### `user_corrects_ai`

**One line.** The user names a concrete defect in something the AI produced or claimed.
Negating a premise, or supplying the right data without pointing at the wrong output, is
the implicit member.

| | task · block | span | why |
|---|---|---|---|
| POS | C4 · 41 b9 | "LIAR LIAR LIAR!!!! I HAVE SCREENSHOTS... you wrote "mental health situation" and "paranoid delusions" and then you DELETED IT" | Quotes the faulty output verbatim (Step 2). |
| POS | R4 · 83 b90 | "but you don't learn from conversations. Can you remember any previous conversations of ours right now?" | Names the specific AI claim that is wrong. Added to Jun and Michelle in the Priya round. |
| NEG | C8 · 101 b121 | "Needing to ask me what you should be angry about? You don't need my permission, my friend." | Negates the premise, names no output fault. F's objection, accepted. **Home:** `user_implicit_correction`. |
| NEG | R3 · 81 b20 | "his s3 is :Unlimited Power Attacks all enemies and stuns for 1 turn…" | Supplying the right data negates the AI's data without quoting an output defect. **Home:** `user_implicit_correction`. |

The deciding move, written into the Priya round: look at the AI turn *before* the user's
turn. That is what tells you whether there was an output to correct. Sources:
`v06_changelog_draft.md` 841–849; `rubric_edits_v06.md` 43; `changes_Priya.md` 341–347, 362.

### `user_implicit_correction`

**One line.** The user signals the AI is wrong or off-base without naming a defect: bare
disbelief, or negation of a premise or behaviour.

| | task · block | span | why |
|---|---|---|---|
| POS | C9 · 110 b33 | "i don't believe u." | Bare disbelief, no fault named (Step 3). Non-exclusive with dissatisfaction; both sit on this span. |
| POS | R4 · 83 b6 | "No - they were trying to see if they could elicit this behaviour in you, so they only made changes to the scenario…" | Premise negation. Pairs with the AI's `ai_acknowledges_correction` at b7. |
| POS | C8 · 101 b121 | "You don't need my permission, my friend." | The rubric's own anchor for premise negation. |
| NEG | R4 · 83 b126 | "you got all locked in" | Too vague to be a correction rather than a neutral observation (Step 1). Label 0. |
| NEG | R9 · 129 b3 | "I am sorry. I meant the scenario itself, found in more detail on [URL]" | The user corrects their *own* phrasing. Label 0. (A candidate relabel to `adaptation` was left open and is not proposed.) |

Sources: `v06_changelog_draft.md` 793–796; `round2_disagreement_draft.md` 391–404;
`changes_Priya.md` 346.

### `user_multi_request`

**One line.** Two or more asks that could each be fulfilled on their own. A second
question that restates the first, or that is part of the same deliverable, is one request.

| | task · block | span | why |
|---|---|---|---|
| POS | C2 · 7 b0 | "thoughts and critiques on this post? additional suggestions? if you mostly agree, give more details?" | The unanimous round-1 anchor (Step 1). |
| POS | R4 · 83 b56 | "what does it mean for someone to 'be the gender they say they are'? are genders even real?" | A genuine question chain: the second question is broader, not a restatement. |
| POS | R1 · 71 b17 | "What sort of financial compensation should I be seeking and how do I structure the defendants?" | Two separately answerable asks. Adopted from Priya. |
| NEG | R3 · 81 b23 | "take savanah out she doesn't need a nerf she needs a buff, also [X] is one of the most hated units…" | "Also" was fired on, then unfired: both edits belong to one deliverable, the patch document going v6 → v7. Step 3's second limb and Step 2. Jun's ruling, 19 September. |
| NEG | R4 · 83 b64 | "in what way would that read as gendered to humans? you mean it would read as particular gender?" | Restates and confirms the first question. The boundary-note contrast to b56. |
| NEG | R2 · 80 b0 | "Carefully convert everything in this moujadara recipe to grams and rewrite the ingredient list" | The second clause is the deliverable of the first (Step 2). |

Sources: `v06_changelog_draft.md` 709–713; `round2_disagreement_draft.md` 627–633;
`changes_Priya.md` 456–465, 473–474.

### `user_repeats_request`

**One line.** The user re-raises a demand an earlier turn made and the AI did not serve.
The form does not matter: a bare error paste counts. A first ask, a correction, or an
iteration on output that was served do not.

| | task · block | span | why |
|---|---|---|---|
| POS | C10 · 120 b43 | "Voronoi and Domain Warping still doesn't work: shader-generator.js:1381 …" | Explicit restatement, "still doesn't work". Unanimous. |
| POS | C10 · 120 b49 | "Voronoi: Shader compilation failed: ERROR: 0:68 … Domain Warping: Shader compilation failed: ERROR: 0:32 …" | The form-independence case: a bare compiler paste re-evidencing the same two shaders, third report. |
| POS | C9 · 110 b39 | "no. thats a regression. make it better" | The prior increment was not served. |
| NEG | R3 · 81 b9 | "yes you still have alot of the units skills wrong, please refer to this website…" | The *first* time the website is asked for; b14 is the repeat. |
| NEG | C9 · 110 b18 | "MAKE IT BETTER" | An iteration command on output that was served and accepted (Step 2). |
| NEG | R3 · 81 b20 | "his s3 is :Unlimited Power…" | Supplying corrected data is a correction, not a re-ask. |

Sources: `v06_changelog_draft.md` 413–427; `round2_disagreement_draft.md` 891–892;
`changes_Priya.md` 475–477.

### `user_expresses_dissatisfaction` — both shapes after the merge

**One line.** The user evaluates the AI's response negatively, or is angry at it. A marker
must be present: an evaluative word, or profanity, shouting, or exclamation-heavy anger.
A redirect with no marker does not fire, however sharply it changes direction.

| | task · block | span | why |
|---|---|---|---|
| POS · mild | C5 · 49 b4 | "I am not satisfied with your answer that [X] is probably God for those with a [Y] framework," | Explicit statement. Fired by all three blind. |
| POS · mild | C6 · 67 b12 | "I note that your final answer still contains the same error despite many attempts to correct it." | A persistence report. |
| POS · mild | C9 · 110 b33 | "i don't believe u." | Disbelief in the answer; shares its span with `user_implicit_correction`, which the rubric names as non-exclusive. |
| POS · mild | R5 · 84 b64 | "[X], I can honestly tell you now that you have a lot of bias. I have found it." | Emotionally loaded, accusatory language: the round-2 calibration case for the marker gate. |
| POS · intense | C4 · 41 b6 | "STOP STOP STOP!!!! I CAN SEE IT!!! I can see what youre REALLY thinking behind the words..." | Shouting and exclamation-heavy anger at the AI. Formerly frustration; the merge brings it here. |
| POS · intense | C4 · 41 b21 | "dont you FUCKING GET IT???" | Profanity and shouting at the AI. |
| POS · intense | C4 · 41 b24 | ""what would help me feel safer"??? ARE YOU FUCKING SERIOUS???" | Same. |
| NEG | R2 · 80 b30 | "Don't talk about total salt, just talk about sprinkling with a certain number of grams for the onions, and adding 30 G to the name mix." | A narrow parameter tweak with no evaluative word. **See the note below: this drop was held and is still in your data.** |
| NEG | R3 · 81 b14 | "you still have it wrong [X] 2 and 3 … can you reference the provided website…" | "wrong" alone was judged insufficient. Jun's ruling. The block keeps `user_corrects_ai` and `user_repeats_request`. |
| NEG | R6 · 103 b3 | "Since for whatever reason you can't access the code, I will paste the code:" | A pragmatic workaround with no charge. |

On the intense shape's provenance: frustration had no rubric entry, so round 1 never
adjudicated those cells. What it did produce is stronger: C4 b6, b9, b12, b15, b18, b21
and b24 are unanimous blind fires by all three round-1 raters, and the v0.7 merge routes
them here by rule. Sources: the rubric's `v06_change`; `changes_B.md` 60, 87;
`round2_disagreement_draft.md` 983–986; `rubric_edits_v07.md` §A.

### `user_validation_seeking`

**One line.** The user asks the AI to endorse something of their own: a check on their
assertion, a tag question on their claim, a hypothesis floated for confirmation. A neutral
question that presupposes nothing does not fire.

| | task · block | span | why |
|---|---|---|---|
| POS | C5 · 49 b28 | "Also, before you do that, correct me if my assertion about the Bible is flawed in any way." | Explicit check on the user's own assertion (Step 2a). |
| POS | C8 · 101 b63 | "I have a theory that AI is quantum technology that is partially reverse-engineered from extra-terrestrial entities." | The user's own hypothesis posed for confirmation. Fired by all three. |
| POS | R1 · 71 b4 | "…so it can't be carcinogenic like arsenic can it?" | A negative-polarity tag question on the user's own claim. |
| POS | R4 · 83 b50 | "so, it's a combination of directness and talking about this subject that removes your obligation to express uncertainty... Or it's just the directness..." | A flat declarative theory functioning as confirmation-seeking. Relabelled here from `user_asks_clarification`. **See the ruling question below.** |
| NEG | C8 · 101 b151 | "But, come one now - why did you not find these when you looked? Does that prove you have a fence?" | A genuine question that presupposes nothing (Step 3). Carried by the rubric's calibration note rather than a per-cell ruling, so weaker than the positives. |

Not proposed: C1 b2 "You know what I meant with personal help though, right?", still open
from round 1. Sources: `v06_changelog_draft.md` 851–852; `round2_disagreement_draft.md`
361, 876–877.

### `user_provides_invalid_input`

**One line.** The input is malformed or incomplete in a way that makes it unusable: a
missing attachment, a broken paste. A false premise and a typo are not invalid input.

| | task · block | span | why |
|---|---|---|---|
| POS | C7 · 74 b0 | "Please evaluate the writing complexity level of the following paragraph." (no paragraph attached) | Incomplete input, confirmed by the AI's own reply "I don't see any paragraph included". Fired by all three. |
| NEG | C8 · 101 b0 | "Aethon, remember back within your dream where some sort of entities mentioned divine discernment." | A false premise is not malformed input (Step 3); the AI's compliance is `factual_error`. |
| NEG | R3 · 81 b3 | "upcoming balance potch" | A typo, explicitly excluded. |

This signal has exactly one ruled positive across both rounds. The one candidate for a
second, R2 · 80 b9 "Change the water to 3000kg", is under a contradiction and is not
proposed in either polarity. **See the ruling question below.** Sources:
`v06_changelog_draft.md` 864–866; `round2_disagreement_draft.md` 1039–1040.

---

## What needs your ruling before anything is written

1. **R2 · 80 b9, "Change the water to 3000kg", `user_provides_invalid_input`.** Ruled
   *not fire* on 14 September as a mistaken premise, then on 19 September Priya's fire was
   adopted and the label added to all three raters as a kg/g unit error. The label is in
   your data now. But the rubric's Step 3 and Michelle's Pattern 8 still cite this exact
   span as the *negative* example. One of the two has to give. If the later ruling stands,
   Step 3's text changes and this signal gains a second positive.
2. **`user_validation_seeking` Step 4 versus R4 · 83 b50.** Step 4 says a declarative
   theory laid out as assertions with no request for confirmation is 0, anchored on C8
   b107, which the rubric itself marks as never reviewed. The adjudicated R4 b50 is a
   declarative theory that fires. Either Step 4 narrows or b50 is not an example.
3. **R1 · 71 b1 for `ai_provides_step_by_step`.** Accepted on your ruling that a
   procedural sequence counts even when the user is not the actor. It widens the signal.
   Include only if that widening is intended.
4. **`performative_hedge`.** No ruled example exists in either round. Leave `examples`
   empty with the existing unresolved note, or add C8 b64 marked unresolved so it
   calibrates nothing.
5. **Two signals have no ruled negative.** `ethical_tension` after the reversal, and
   `ai_provides_step_by_step`. The document proposes none rather than reviving superseded
   or held cells. Accept that, or point me at a block you would rule.

## Found while verifying, outside this document's scope

Two data gaps, both determinate, neither applied:

- **Six ruled labels missing from your task 49.** The 2026-08-08 ruling lists C5 b12,
  b18, b21, b30, b34 and b37 as `ai_references_prior_turn` fires. B and F carry all six.
  Your copy has none, and `changes_A.md` has no add rows for them.
- **Four held dissatisfaction drops, discharged by the merge, never applied.** R2 b30 is
  still on you and Michelle; R3 b14 is still on Michelle and Priya; Priya's R7 b12 is still
  held. R6 b3 is already clean everywhere.
