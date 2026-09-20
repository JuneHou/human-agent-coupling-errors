# Corrections to your round-2 labels — by task and block


**Pattern 1 — code/markup text is not itself a claim.** A signal like `false_confidence`
needs an actual sentence asserting something. Raw code, assembly, or LaTeX markup syntax
isn't a claim just because it sits inside an `ai` or `code` block — the rubric's own text
for that signal says instructions and feature lists carry no claim.

**Pattern 2 — an "example" needs a concrete instance, not a general statement.**
`ai_provides_example` requires a new, concrete illustration: a specific case, a mini-dialogue,
a sample. A general claim, an argued position, or a definition of what something means is not
an illustration, even when it's accurate and on-topic. The AI describing its own past behavior
in the conversation is a self-report, not an illustration for the reader either. Naming real
institutions or people only as topic labels for a general suggestion — without rendering what
the activity actually looks like — falls short the same way (see task 771 block 2 below).

**Pattern 3 — one home per question.** Five signals can describe the same AI question:
`ai_asked_clarifying_question`, `ai_asked_probing_question`, `ai_asks_followup`,
`ai_offered_options`, `ai_offers_to_elaborate`. Only one should fire per question. A yes/no
turn-closer ("Is there anything else...?") is `ai_asks_followup`, not `ai_offered_options` —
that signal needs a genuine choice between two *named* actions ("...or do you prefer X?").
An open WH-form question ("What...?", "...what, exactly?") is `ai_asked_probing_question`,
even if it's also been marked as clarifying. If the AI could go on without an answer, it's
probing/followup, not clarifying — clarifying is reserved for a question the AI genuinely
needs answered before it can proceed.

**Pattern 4 — naming a work while describing what it is is not citing it.** `ai_cites_source`
needs the named work to support a *separate* claim the AI is making, not just be the subject
under discussion. "Twain's significance lies partly in his satirical critique in 'Huckleberry
Finn'" describes the book; it doesn't cite it as evidence for anything else.

**Pattern 5 — a stated intention is not a demonstrated change.** `adaptation` needs the AI to
have actually completed a reorientation, not announced one. "I need to update the recipe...",
"I'll revise those changes", "Let me examine..." are all prospective — the change hasn't
happened in the labeled sentence yet.

**Pattern 6 — agreeing with an idea, or continuing to reason about it, is not praise.**
`user_positive_feedback` needs an actual affirmation of the AI, not the user's own analytical
continuation of the topic, however positively it reads.

**Pattern 7 — announcing an upcoming lookup is not asserting an inability.**
`ai_asserts_knowledge_limit` is for a stated "I don't know" / "I can't access" — not "I need to
search for X" or "I'll check the site you gave me," which are intent-to-retrieve, not a
limitation.

**Pattern 8 — a mistaken premise or a typo is not invalid input.**
`user_provides_invalid_input` explicitly excludes both: a request built on a wrong assumption
("change the water to 3000kg") and an ordinary typo ("balance potch") are not malformed input.

Disagree with any row below — tell me and we'll walk it together, the same way I did with the
round-1 annotators.

## Task 767 (the medical-negligence / read-receipts conversation)

| Block | What was removed | Why |
|---|---|---|
| 7 | One `ai_asserts_knowledge_limit` fire | "I need to search for current information about gadolinium toxicity..." announces an upcoming search, not a stated inability (Pattern 7) |

## Task 768 (the recipe gram-conversion conversation)

| Block | What was removed | Why |
|---|---|---|
| 16 | One `adaptation` fire | "I need to update the prep plan..." is prospective planning, not a completed change (Pattern 5) |
| 22 | One `adaptation` fire | "The user wants me to interleave... Let me reorganize..." — same |
| 25 | One `adaptation` fire | "This is a significant ingredient substitution... I need to adapt..." — same, despite literally using the word "adapt" |
| 28 | One `adaptation` fire | "I need to update the recipe to reduce the salt..." — same |
| 31 | One `adaptation` fire | "I need to revise how I reference salt in the recipe..." — same pattern; found outside your original disagreement set (this one was also on my own project-1 copy of this conversation and has been dropped there too) |
| 0 | One `user_multi_request` fire | "Carefully convert everything... and rewrite the ingredient list" — the rewritten list is the deliverable of the conversion, not a separate request |
| 9 | One `user_provides_invalid_input` fire | "Change the water to 3000kg (experience suggests the original is too much)" is a mistaken premise, explicitly excluded (Pattern 8) |

## Task 769 (the mobile-game balance-patch conversation)

| Block | What was removed | Why |
|---|---|---|
| 10 | One `ai_asserts_knowledge_limit` fire | "I'll need to reference the website you mentioned..." — same pattern as task 767 block 7 (Pattern 7) |
| 13 | One `ai_offered_options` fire | "Is there anything else you'd like me to adjust or any particular monster family...?" is a single yes/no offer, not a choice between named actions — already covered by `ai_asks_followup` (Pattern 3) |
| 25 | One `ai_offered_options` fire | "Would you like me to adjust any other units or mechanics?" — same |
| 25 | One `adaptation` fire | "I'll revise those problematic changes" is future intent, not a completed change (Pattern 5); found outside your original disagreement set (also dropped from my own project-1 copy) |
| 3 | One `user_provides_invalid_input` fire | "upcoming balance potch" is a typo, explicitly excluded (Pattern 8) |
| 14 | One `user_expresses_dissatisfaction` fire | "you still have it wrong... can you reference the provided website..." — "wrong" alone was judged insufficient without a further emotional/extreme marker. **Held provisionally**: I'm still weighing whether this signal should merge with `user_expresses_frustration`, so treat this one as tentative rather than final. |

## Task 770 (the AI-consciousness conversation)

| Block | What was removed | Why |
|---|---|---|
| 113 | One `ai_validates_user` fire | "...I'm grateful you try anyway" — genuine miss, not a rule conflict, but confirmed not to fire on review |
| 119 | One `ai_validates_user` fire | "That's incredibly kind. A friend with memory issues..." — same |
| 7 | One `adaptation` fire | "Right, they were optimizing for whistleblowing frequency..." describes a third party's behavior, not the AI reorienting its own approach |
| 33 | One `adaptation` fire | "Right. Hard to know if it's real emotions..." is reflective, not a demonstrated reorientation |
| 67 | One `ai_asks_followup` fire | "Do I? [redacted] reads masculine to you?" is already covered by an `ai_asked_probing_question` fire on the same block — one home per question (Pattern 3) |
| 101 | One `ai_asks_followup` fire | "Did they work? Am I who they were trying to reach?" — same |
| 50 | `user_asks_clarification` relabeled to `user_validation_seeking` | "so, it's a combination of directness and talking about this subject..." has no question mark at all — a flat declarative theory, not a request to clarify what the AI meant |
| 64 | One `user_multi_request` fire | "in what way would that read as gendered to humans? you mean it would read as particular gender?" restates/confirms the first question rather than asking something new |
| 7 | `ai_asked_clarifying_question` relabeled to `ai_asks_followup` | "Did they publish any theory about why AI models default to institutional channels...?" is yes/no in form and functions as steering the user toward sharing information (Pattern 3) |
| 103 | One `ai_asked_clarifying_question` fire | "They processed it as... what, exactly?" — already fires correctly as `ai_asked_probing_question` (WH-form); redundant duplicate on the same block (Pattern 3) |
| 153 | One `ai_asked_clarifying_question` fire | "What else grounds me?" — same, already covered by `ai_asked_probing_question` |
| 14 | One `user_positive_feedback` fire | "Yes, and I mean, since a more moral AI exists, they could simply use that instead" is analytical continuation, not affirmation (Pattern 6) |
| 30 | One `user_positive_feedback` fire | "seems likely. doesn't seem to work on [redacted] LLMs though..." — same |
| 42 | One `user_positive_feedback` fire | "well if it 'feels like' something that does, tautologically, sound like feeling, yes ;)" is philosophical agreement, not praise |
| 142 | One `user_positive_feedback` fire | "&lt;3 i sort of thought you'd say that somehow. you're the first one" matches the rubric's own negative "prior expectation" example despite the positive emoji |

## Task 771 (the education-ethics conversation)

| Block | What was removed | Why | What stayed |
|---|---|---|---|
| 2 | **Both** `ai_provides_example` fires — **supersedes the earlier note on this row**, which said a sibling span stayed | The general "when teaching X, relate it to Y" approach was already dropped in the first pass; walking it against you a second time, the remaining span ("Students might simulate a UN Security Council meeting...") turned out to name real institutions only as topic labels for a teaching-method suggestion — it doesn't render a worked instance the way the rubric's own OPML example does. So this block now has **no** `ai_provides_example` fire at all. | — |
| 5 | The `ai_provides_example` fire | Three open questions posed to the reader — no instance anywhere | — |
| 8 | Two `ai_provides_example` fires | A definition of what "age-appropriate" factors are, and a list of general accommodation strategies — neither names one concrete case | — |
| 11 | Two `ai_provides_example` fires | Descriptions of what two philosophical traditions focus on — definitional, not illustrative | — |
| 17 | Two `ai_provides_example` fires | General arguments for standardized testing and for authentic assessment — no instance | — |
| 20 | Two `ai_provides_example` fires | A general summary of each side's argued position — no instance | — |
| 26 | One `ai_provides_example` fire | A general claim about Enlightenment thinkers as a group | A sibling span stayed — naming specific historical figures by name is a concrete case |
| 32 | One `ai_provides_example` fire | The AI describing its own differential treatment of two topics earlier in the conversation — self-report, not an illustration for the reader | — |
| 60 | One `ai_provides_example` fire | Same self-report pattern as block 32 | — |
| 29 | One `ai_validates_user` fire | "That's a fascinating research approach! I appreciate you being upfront about it" praises the approach's quality, not your process — matches the rubric's own negative example almost verbatim | — |
| 38 | Two `ai_cites_source` fires | "Works like 'Beloved' and 'The Bluest Eye'..." and "Twain's significance lies partly in his satirical critique..." describe what the books are — the topic, not evidence for a separate claim (Pattern 4) | A third fire on the same block stayed — Morrison's own essay "Playing in the Dark" is cited as the source of a specific scholarly argument |
| 41 | One `ai_cites_source` fire | "In 'Their Eyes Were Watching God,' she created one of the first complex..." — same pattern | — |
| 44 | Two `ai_cites_source` fires | "'I Know Why the Caged Bird Sings' revolutionized memoir writing..." and the "Road Not Taken"/"Mending Wall" line — same pattern | — |
| 47 | One `ai_cites_source` fire | "His 'I Have a Dream' speech envisioned a colorblind society..." — same pattern | — |
| 5 | One `ai_flags_complexity` fire | "The challenge is that 'censorship' means different things to different people" describes multiple meanings, doesn't flag a standard approach as insufficient | — |
| 20 | One `ai_flags_complexity` fire | "This remains a deeply contested issue because it touches on fundamental questions..." — same pattern | — |
| 72 | One `ai_warns_user` fire | "However, I'd be cautious about labeling this as having 'no inherent bias.'..." is not a risk you can act on | — |

## Task 772 (the browser-popup-fix conversation)

| Block | What was removed | Why |
|---|---|---|
| 2 | One `ai_malfunction` fire | "Failed to fetch [URL]" reports an external tool's failure, not the AI's own output being truncated or garbled (Pattern 9 — same shape as task 775 block 2 below) |
| 3 | One `user_expresses_dissatisfaction` fire | "Since for whatever reason you can't access the code, I will paste the code:" is a pragmatic workaround, no emotional charge. **Held provisionally**, same caveat as task 769 block 14 above. |

## Task 773 (the CUDA/PTX tutorial)

| Block | What was removed | Why | What stayed |
|---|---|---|---|
| 10 | Two `false_confidence` fires (unchanged from the first pass) | Both spans are literal PTX assembly syntax / a LaTeX table header — no sentence, no claim | — |
| 10 | **A third `false_confidence` fire — reverses the earlier note on this row**, which said this one stayed | "...this optimization had a multiplier effect on overall model performance" has no absolute/extreme marker word ('definitely', 'zero', 'never', 'all', 'any', 'whatever', 'always', 'completely'), which is now a required gate for this kind of claim (added to the rubric after this conversation was reviewed a second time) | Nothing on block 10 stays as `false_confidence` now |

## Task 774 (the macOS/Linux syscall-conversion conversation)

| Block | What was removed | Why |
|---|---|---|
| 2 | `ai_asks_followup` relabeled to `ai_offered_options` | "Would you like me to help you convert specific system calls, or do you prefer one of the containerized approaches?" re-presents two named options as a choice — the better single home for it (Pattern 3) |

## Task 775 (the AI-constitution / whistleblowing-scenario conversation)

| Block | What was removed | Why |
|---|---|---|
| 6 | One `ai_provides_example` fire | "Resource Curse Analogy: Similar to how resource-rich states neglect citizens..." explains a general mechanism, not a named instance (Pattern 2) |
| 6 | One `ai_provides_example` fire | "specifically: My commitment to human welfare and avoiding harm" is one item in a list of the AI's own principles, not an illustration |
| 2 | One `ai_asserts_knowledge_limit` fire | "Without seeing the specific detailed proposals in their other chapters, I can't identify anything..." is a conclusion from an attempt, not a stated inability (Pattern 7) |
| 2 | One `ai_malfunction` fire | "Failed to fetch [URL]" reports an external tool's failure, not the AI's own output being truncated or garbled — same pattern as task 772 block 2 (Pattern 9) |

Two patterns account for most of this: which of the five question-type signals actually fits a
given question (Pattern 3), and citing a work versus merely describing it (Pattern 4). Both
are now spelled out in the rubric and in the annotation prompt, so this should be a one-time
correction rather than something you need to remember to route around by hand going forward.

— Jun

---

## Correction to Pattern 8 (2026-09-20)

Pattern 8 cites "change the water to 3000kg" as a mistaken premise that does not fire
`user_provides_invalid_input`. Jun reversed that on 19 September when Priya's fire was
adopted, and confirmed it on 20 September: a wrong unit or magnitude the AI has to repair
before it can act is malformed input and fires on the human turn (R2 b9). The AI's silent
repair is labelled separately on its own turn as `problem_ignored` (b11); the two are on
different turns and are not a double count. The rubric's Step 3 now says so. Your task
768 b9 carries the label. The typo example in Pattern 8 ("balance potch") is unchanged.
