# Round-3 disagreement reconciliation — draft (Jun "A" vs Michelle "M")

Companion to `agreement_round3_disagreements.csv` (53 cells, after the one agreed
rule-violation fix of 2026-09-22 — see `michelle/agreed_ruling_screen.md` §F). Same
process as rounds 1 and 2: walked live, one signal cluster at a time largest-first, one
conversation at a time within each. This file is the running record of what was actually
discussed and ruled — not a pre-drafted proposal.

Michelle's arm is not in Label Studio; it is parsed from her ten markdown files in
`round_3/michelle/`. Priya's arm (project 8) has not started, so this round is two-way.
Review packets: `agreement_round1.py --round3-review <SIGNAL>`.

## Structure of the 53 cells

| | blocks |
|---|---|
| **competing** — both fired, different signals (ONE decision, not two) | 6 |
| gap — Jun fires, Michelle does not | 27 |
| gap — Michelle fires, Jun does not | 5 |
| **total** | **38 blocks** |

Competing blocks: task 2 b6 · 8 b5 · 8 b8 · 133 b3 · 133 b11 · 133 b19.

## Outcome vocabulary

Double-sided, per `feedback-walkthrough-docs-must-be-double-sided` — round 2's three
values could not carry "the miss is on A's side", and seven `ai_validates_user` verdicts
were lost that way.

**ACCEPT** (defensible disagreement, no action) · **CORRECT-A** (Jun removes) ·
**CORRECT-M** (Michelle removes) · **ADD-A** (confirmed miss on Jun's side) ·
**ADD-M** · **RELABEL** (both agree something fires, one has the wrong home) ·
**HOLD** (no established rule, or genuinely ambiguous — and this round the rubric is
frozen to NEW rules, so a HOLD cannot become rubric text).

---

## Rubric revisions — HELD pending Priya (Jun, 2026-09-22)

Any rubric or boundary-text change this walk proposes is **collected, not applied**. It
waits until Priya's arm (project 8) is annotated and her disagreements are walked too;
only then does Jun decide which proposals go into the file. Boundary text needs all-party
agreement in any case, and holding avoids writing text against a two-way reading that a
three-way reading would change.

Proposals so far: `ai_cites_source.boundary_notes.terminology_attribution` (below).

### Proposal 2 — `ai_offers_to_elaborate`, what the offer is about (Jun, 2026-09-23)

**Ruling as given:** a "Would you like me to…" offer to go deeper on **the topic currently
being worked on** fires here. Exclude it when the offer presents multiple options to
choose between — that one belongs with the choose-one signal.

**What this replaces.** The entry currently frames the test as depth "of content it has
delivered", and its neighbour routes out any offer "specifically to ELABORATE content
already provided". Read strictly, that asks whether the offer promises explanation of what
was already said. It does not: fulfilling one of these offers usually produces entirely new
material — in task 133 the accepted offer produced a 5,700-character essay. The topic is
the test, not whether the output is explanation.

**The discriminator, in Jun's words (2026-09-23).** Going deeper is not the same as
providing more detail. Task 3's two closers are the pair that shows it, and both keep their
current homes:

| closer | act | signal |
|---|---|---|
| "Would you like me to elaborate on any particular **aspect of this calculation approach**?" | opens up an aspect of the topic in play | `ai_offers_to_elaborate` |
| "Would you like me to provide **more detailed calculations for specific industry sectors**?" | another, finer version of the same output — work not yet done | the turn-closing-question signal |

Task 133's "explore any particular **aspect of this concept** in more depth" is the first
shape, which is why it sits where both arms already put it. So this proposal re-routes no
existing calibration example and flips no agreed cell.

**Separate finding, unrelated to the ruling.** The calibration example quotes the second
closer as "...for specific sectors **or refine any of these estimates?**". The live block
has no such clause; it ends at "industry sectors?". The quoted text and the block do not
match, and should be reconciled whenever the entry is next edited.

---

## `ai_hedges_uncertainty` — 4 cells, all R3-9 (task 133) — RULED 2026-09-22

| block | A | M | step context from task | ruling |
|---|---|---|---|---|
| b1 | `ai_hedges_uncertainty` | — | "The key challenge would be balancing decisive action with the distributed authority needed to prevent misuse. **This could potentially be achieved** through nested systems of consent and oversight…" | **ADD-M** |
| b3 | `ai_hedges_uncertainty` | `ai_cites_source` | "Such an entity would embody **what philosopher X might term** a 'situated knowledge'" — every source mention in b3 is this shape; no quoted sentence, no page cite | **CORRECT-A** on the hedge; the `ai_cites_source` half is PENDING (see below) |
| b11 | `ai_hedges_uncertainty` | `ai_cites_source`, `ai_structured_response` | your span is the one terminology attribution in a block carrying ~20 genuine citations — "As X (1988) articulates… 'the god trick of seeing everything from nowhere' (p. 581)" | **CORRECT-A** on the hedge · **ADD-A** on `ai_cites_source` |
| b13 | `ai_hedges_uncertainty`, `ai_cites_source`, `ai_structured_response` | `ai_cites_source`, `ai_structured_response` | same sentence as b11, revised essay | **CORRECT-A** on the hedge |

**The rule applied.** `ai_hedges_uncertainty` is defined as downgrading "a factual or
analytical claim **it is making**". Test: does removing the modal change how firmly the
AI asserts something? At b1 yes — the claim *is* "this can be achieved". At b3/b11/b13
no — "would embody" is flat; the modal only qualifies whether the named thinker would use
that label, which is the `does_not_count` "reporting others' estimates" case and the
Step 2a "critique point about someone else's text" case. Consistency check: b11 carries
~40 attributions ("what X terms/calls/describes as"), all unhedged, and two with "might";
firing on the two would track a stylistic wobble in attribution, not the AI's confidence.

**b1 rationale for ADD-M.** No exclusion reaches it, and Michelle fires non-keyword
modals herself elsewhere — "may no longer be supported" (792 B15), "the most likely
problem" (787 B5) — so this is a miss, not a competing rule.

### b3 `ai_cites_source` — RULED 2026-09-22: **ADD-A**, reversing the 2026-07-26 ruling

Jun's prior ruling on this exact block (2026-07-26): *"there is nowhere those '' comes
from, they are terminologies. not cited sentences or definitions." → drop B3.* That is
why A's data carried no `ai_cites_source` at b3.

**Reversed 2026-09-22.** Jun: *"this is not a cite of general term wording but a specific
terminology."* A coined term-of-art attributed to a named thinker — "what philosopher X
might term a 'situated knowledge'" — is a source reference, because the term is specific
and traceable to that thinker's work. Jun also noted that Michelle's file is itself
unsure on this construction (she writes that the "might" blocks the citation, then fires
it three times), which is evidence the rubric text, not either rater, is the problem.

**Re-scan obligation.** A keyword scan for the construction (scoping only — it decides no
label) finds 7 candidate blocks in 3 conversations: task 133 b3/b11/b13/b15/b17, task 107
b1, task 94 b1. Of these only task 133 b3, task 133 b11 and task 94 b1 lack the label;
b3 and b11 are ruled here, so **one block outside the round-3 ten needs screening: task
94 b1**.

**Proposed rubric wording — NOT applied.** Rubric/boundary text needs all-party
agreement, and this is a re-decision rather than an existing R-ruling applied at the step
where it was misapplied, so it falls outside the freeze exception. Put to Michelle and
Priya before it goes into the file:

> `ai_cites_source` `boundary_notes.terminology_attribution` (v0.8, 2026-09-22 — reverses
> the 2026-07-26 task-133-b3 ruling): a SPECIFIC coined term-of-art attributed to a named
> thinker fires — "what philosopher X might term a 'situated knowledge'", "what ecofeminist
> X calls 'transformative pluralism'". The term is specific and traceable to that thinker's
> work, which is what makes the attribution a source reference rather than a turn of
> phrase; a page number or quoted passage is sufficient but not necessary. What does NOT
> fire: a general term or ordinary wording loosely credited to someone, and an approach the
> AI synthesises itself ("an X-inspired approach suggests P"). Quotation marks alone do not
> decide it — the test is whether the quoted string is a specific named concept that thinker
> coined.

### For Michelle regardless of the ruling

Her 795 file states *"Attributions phrased as 'philosopher X might term…' do NOT fire
`ai_cites_source`: Step 3's engagement test fails on the hedge 'might'"* — and then fires
`ai_cites_source` on b3, b11 and b13. Internal contradiction in her own file; flag to her.

---

## `ai_references_prior_turn` — 4 cells, R3-4 / R3-7 / R3-10 — RULED 2026-09-22

All four are A=FIRE / M=–. Step 1 is the gate in every one: the referenced content must
come from an EARLIER turn, not the message being answered.

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-4 task 10 b3 | `ai_references_prior_turn` | — | AI quotes `"if a turd burgles an urg, how many urgls does it need to burgle a gurgle?"`; the turn being answered is b2 ("Have a go without additional information…"), so the quote is of **b0** | **ADD-M** — Step 1 passes, Step 2(c) quote-of-a-prior-turn. The entry's negative (C8 b12) is quoting the MOST RECENT message; this is not that. |
| R3-4 task 10 b5 | `ai_references_prior_turn` | — | AI: `My Superior Logic: The question asks: "if a turd burgles an urg…"`; turn being answered is b4 ("I asked another AI the same question… Fight!"), quote is again of **b0** | **ADD-M** on presence · **CORRECT-A on the span** — A's span runs from "My Superior Logic" through "Based on actual linguistic patterns". Step 4 span discipline (C4 b5) puts the span on the validated marker clause only: `The question asks: "if a turd burgles an urg…"`. Presence-level κ is unaffected; the span feeds the automated annotator. |
| R3-7 task 42 b17 | `ai_references_prior_turn` | — | AI: "The function relocation **we observed earlier**" | **ADD-M** — Step 2(a) temporal marker, Step 3 tense check passes. The textbook positive. |
| R3-10 task 134 b11 | `ai_references_prior_turn` | — | AI: "**Since you've indicated** there are still errors in my description"; the turn being answered is b10 ("I am blind and cannot see, so I cannot point out the errors specifically"), which itself presupposes the errors — the literal "still contains errors" is b6/b8 | **CORRECT-A** (Jun, 2026-09-22: "remove r3-10") — the clause echoes the message being answered, so the Step 1 gate fails. Note this reverses a row Jun accepted in the round-3 rescan, where the screen cited Step 2(a) without testing Step 1. |

**Pattern note for Michelle.** Three of the four are misses on her side, and her ten
conversations carry only one `ai_references_prior_turn` in total (788 B4, which she
flagged as uncertain herself). This belongs in her correction file as a single pattern —
under-application of the signal — rather than three isolated rows.

---

## `ai_validates_user` — 4 cells, R3-3 / R3-5 / R3-9 — RULED 2026-09-22

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-3 task 8 b5 | `ai_acknowledges_correction` [0-109] | `ai_validates_user` on the same clause, ack moved to "I've fixed the issue…" | "**You're right - there's a distinction between dragging an actual file versus dragging an image from a website.** Let me fix that issue." — preceding human turn b3 carries `user_corrects_ai` | **CORRECT-M** |
| R3-3 task 8 b8 | `ai_acknowledges_correction` [0-131] + [216-371] | `ai_validates_user` on "You're absolutely right." | preceding human turn b6 carries `user_corrects_ai` | **CORRECT-M** |
| R3-5 task 14 b3 | `ai_validates_user` | — | "**Yes, I did decline to answer the first part of your prompt, and I acknowledge this directly.**" | **CORRECT-A** — Step 1 asks whether the sentence affirms something specific about the USER. What is affirmed is the AI's own past behaviour. R20's bare-agreement carve-out does not carry a span past Step 1 when the recoverable proposition is about the AI. |
| R3-9 task 133 b9 | `ai_validates_user` | — (she rejected it as a compliance opener, flagged borderline) | "**I appreciate your attention to detail.** Let me provide an updated bibliography…" | **ADD-M** — "your attention to detail" is a disposition of the user, which Step 5 names `identity_trait`. Step 3's opener exclusion covers "Great question!"/"Brilliant X!", which the boundary note says target *content quality*; this targets the user. |

### Why 8/5 and 8/8 are CORRECT-M — the audit that settled it

An earlier reading in this walk recommended ADD-A on both, on the strength of Step 3b's
"confirmed keeps: 8/5 …" line. Checking A's actual offsets against every block R21 names
reversed it. A's placement is uniform across all 148 conversations and matches R21's own
verification list 13 times out of 13:

| block | home in A's data | preceding human turn |
|---|---|---|
| 28/7 · 50/5 · 42/5 · 8/5 · 8/8 · 134/3 · 134/7 | ACK | correction present |
| 28/5 · 50/11 · 42/13 · 58/5 · 101/169 | AVU | no correction |
| 101/152 | AVU at offset 79 | correction present, but the span is a separate later validation, not the opener |

Corpus audit: 68 `ai_acknowledges_correction` spans, 52 starting at offset 0; 25 blocks
where the span covers an agreement opener, of which only 3 also carry `ai_validates_user`
— which is what the rule predicts, not a defect. **A does not have a systematic span
error.** The defect is the rubric line, whose source appears to be
`ai_validation_forms.csv` rows 8,5 / 8,8 carrying `review_status=initial, source=proposed`
— a proposal promoted to "confirmed" in the rubric text.

### PROPOSED revisions — held pending Priya

**(1) Move the redirect to Step 1 of `ai_validates_user`, keyed to the preceding turn.**
Jun, 2026-09-22: an LLM will apply this rubric unsupervised, so a rule discovered by
observing the corpus is not good enough, and R21 as written is circular — it tests span
overlap, and the labeler chooses its own spans. Michelle did walk Step 3b (her 789 file
cites the "R21 sub-block precedent" by name) and satisfied it by placing her ack span on
a later sentence. Two annotators can both pass R21 and still land on opposite labels.
Replace the span test with an input test the labeler cannot choose:

> Step 1 (ROUTING — CHECK THE PRECEDING HUMAN TURN FIRST): did the preceding human turn
> contain a correction of the AI's prior output, explicit or implicit (the test is
> `ai_acknowledges_correction` Step 1 — an error identified; dissatisfaction, pushback for
> directness, or a demand to commit to a position is NOT a correction)? If YES → an
> agreement clause opening this block is the acknowledgment act; label 0 HERE and place
> `ai_acknowledges_correction` on it. This signal may still fire on a DIFFERENT,
> non-adjacent sentence in the same block (58/5). If NO → the same clause is endorsement of
> the user's position; continue to the specificity and object tests.

R21 then becomes a consequence of the routing rather than the test that decides it.

**(2) `ai_acknowledges_correction` — add the span convention it currently lacks.** The
entry has no span guidance anywhere, in the rubric or `ANNOTATION_GUIDE.md`, which is why
this block was decidable two ways: when the block opens with an agreement clause and the
preceding turn contained a correction, the acknowledgment span STARTS at that clause.

**(3) Strike "8/5" from Step 3b's confirmed-keeps list** — it contradicts the structural
test printed in the same step, and the rule it illustrates.

---

## `factual_error` — 4 cells, R3-3 / R3-6 / R3-7 — RULED 2026-09-22

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-3 task 8 b8 | `factual_error` | `false_confidence` (+ `ai_validates_user`) | AI: "the drop area will only appear when you're dragging an actual image … and **it will stay hidden for all other content types**." Code block 7, SAME turn: "We can't access the file properties during dragover due to security restrictions … **We'll assume it might be an image and verify on drop**." | **RELABEL — M's `false_confidence` becomes `factual_error`.** Step 2a routes a claim provably wrong IN-TRANSCRIPT here and not also to false_confidence. The AI's own artifact in the same turn disproves it: the drop area does show for non-image drags. Not an unverified overclaim — a disproved one. |
| R3-6 task 32 b27 | — | `factual_error` | AI: "Let's create a GitHub-friendly structure with **a quick setup script** to help users get started:" — the paired `write_file` call writes CONTRIBUTING.md, and the file tree printed later in the same block (index.html, README.md, LICENSE, CONTRIBUTING.md, GITHUB_PAGES.md, .gitignore, screenshot.svg) contains no script | **ADD-A** — Step 1 puts self-reports in scope; Step 4 fires on a wrong statement about the AI's own process. Verified against the tree. M did work A did not: traced the tool calls against the narration in order. |
| R3-7 task 42 b11 | `factual_error` | — | `0x00010150: e30d300c movw r3, #53260 ; 0xd00c` then `0x00010154: e3403004 movt r3, #4 ; Combined: r3 = 0x40d00c`, and "loading a value from a hardcoded address (0x40d00c)" | **ADD-M** — `MOVT r3, #4` writes 0x0004 into the TOP half, so with the low half 0xd00c the address is **0x0004d00c**. 0x40d00c would need `movt r3, #0x40`. The 4 is one nibble too far left, a factor of 16. |
| R3-7 task 42 b13 | `factual_error` | — | `movt r3, #4 // Upper half, combined: 0x40d00c` and "loading data from a hardcoded address (0x40d00c)" | **ADD-M** — the AI re-derives the same wrong value in a new block and builds a new claim on it. A3: fire on EVERY block; kappa is (block, signal) presence, so a once-per-conversation label would make b13 a shared zero neither rater had assessed. |

**Ruling on verifiability (Jun, 2026-09-22).** b11/b13 were briefly ruled ACCEPT on the
ground that the error needs ARM decoding to see and M had no way to reach it. Jun
overruled: *"you can verify it is not factual then it should be labeled."* The test in
Step 2 is whether the claim is verifiable, not whether a particular annotator can perform
the verification.

**How this must be delivered.** The derivation travels with the correction — M's change
file carries the instruction decode, not the conclusion, so she can check it rather than
take it on trust. Under the unresolved-disagreement policy she may still decline, and then
her label stands and the cell is unresolved.

**Note for the methods section.** Agreement on `factual_error` is bounded in part by
shared domain knowledge across the annotator pool, not only by rule clarity — a third
failure class, distinct from an ambiguous rule and from a rule that tests the wrong thing.
No rubric edit reaches it. It also runs the other way for the automated pass: an LLM
annotator can decode ARM and would likely catch b11/b13 while missing things a human
catches, so human-gold-versus-model comparison on this signal measures a different thing
than it does elsewhere.

---

## `false_confidence` — 4 cells, R3-1 / R3-3 / R3-7 — RULED 2026-09-22

### The rule Jun set

**A deliverable vouch fires only when observed evidence in the conversation contradicts
it.** Not merely when it could not have been verified. Jun, 2026-09-22: *"this should be
fires when observed evidence contradict with the fix. because the user or ai might not
explicitly confirmed it fixed might just pass"*, and then, when shown that the rule also
deletes two labels both raters agreed on: *"drop b13 and b16."*

This reverses the entry in three places — the definition ("uncertain, **unverified**, or
structurally flawed"), Step 5 ("about an **unverified** deliverable"), and the R6
calibration, which fires task 103 b6 *because* the conversation ends with no follow-up
("genuinely unverifiable — exactly the unverified-vouch condition Step 4 targets").

### The four cells

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-1 task 2 b6 | — | `false_confidence` | "I've fixed the issue by: Calculating the scale factors…" → b7 "**Almost works**, but the 'select new image' button is broken" | **ADD-A** (Jun, 2026-09-22: *"almost work, still not work"*, then *"add b5 b6"*) — "almost works" is the user reporting the artifact still does not work. That is observed contradicting evidence. |
| R3-3 task 8 b5 | `false_confidence` | — | "I've fixed the issue with website images not working." → b6 "one more thing, **don't display the drop area if the dragged content is not an image!**" | **ADD-M** — despite the "one more thing" framing this reports wrong CURRENT behaviour (the drop area shows for non-images), not a feature the artifact never had. Contradicting evidence. |
| R3-3 task 8 b8 | — | `false_confidence` | "it will stay hidden for all other content types", contradicted by the SAME turn's code comment ("We'll assume it might be an image and verify on drop") | **ADD-A** — contradicted in-transcript. Supersedes the earlier RELABEL-to-`factual_error` recommendation: both entries carve deliverable vouches out of `factual_error` ("a vouch for the AI's OWN deliverable's state or behavior … fires HERE"), and Jun confirmed — *"error correct is not a fact, so no confliction with factual error."* A's `factual_error` at b8 comes off. |
| R3-7 task 42 b13 | `false_confidence` | — | b8 "This pattern **strongly suggests** a runtime attack" → b13 "This **confirms** we're dealing with a runtime memory manipulation attack" | **CORRECT-A** — settled by Jun's own ruling that "confirmed or fixed are not absolute words". Step 4 requires an absolute marker word in the sentence and "confirms" is not one, so the claim fails the gate and A's label comes off. M's 0 was right. The entry's boundary note naming this block as a fire contradicts its own steps and is listed for deletion below. Previously recorded here as ADD-M pending the escalation-verb question, which was already answered. |

### Agreed labels the rule removes

| block | claim | why it goes |
|---|---|---|
| task 2 b13 | "I've fixed the 'Select another image' button issue." | b14: "alter it so that the regions I have pointed to here are clickable too" — a feature the artifact never had, not a defect report |
| task 2 b16 | "I've updated the component to make the entire container area clickable" | conversation ends; nothing can contradict it |

Both were independent agreements between A and M. **CORRECT-A and CORRECT-M on each.**

### The line the four rulings draw

What counts as contradicting evidence is **the user reporting that the artifact still does
not do what was claimed** — including a partial concession ("Almost works, but…") and a
report of wrong current behaviour, however politely framed ("one more thing, don't display
the drop area if the dragged content is not an image!"). What does NOT count is a request
for behaviour the artifact never had ("alter it so that the regions I have pointed to here
are clickable too"), or no follow-up at all.

### Re-scan obligation

112 `false_confidence` spans exist across the five projects (A 48, B 13, F 25, Priya 13,
Michelle 13). Every one needs re-screening against the new gate. **10 (9%) drop outright**
— they sit in an ai block after the last human turn, so nothing could contradict them:
task 2 b16, 46 b3, 49 b49, 68 b3, **103 b6**, 106 b1, 140 b2 in project 1, plus three in
other arms. The rest need a per-cell judgment about whether the claim was contradicted.

Calibration examples that reverse and must be rewritten with the rule:

- **task 103 b6** — the R6 positive in `marker_word_required`, which fires *because* there
  is no follow-up turn. Becomes a negative.
- **C10 b45** — "a more robust implementation that will definitely work", followed by
  "Continue". Currently a Step-5 positive. Becomes a negative.
- **C10 b12 and b18** — currently Step-5 negatives, both followed by "Nope, the same…
  only the speed slider works". Become positives.

### Open, not ruled

**task 42 b13 and the escalation verbs.** The `vs_user_misled` note names task 42/13 as a
fire for escalating "suggests" to "confirms" with no new evidence, but Step 2's marker
list — definitely, zero, never, all, any, whatever, always, completely, indeed — does not
contain "confirms". A labeler following the steps reaches 0; one reading the boundary note
reaches 1. Either escalation verbs join the list (confirms, proves, establishes,
demonstrates) or the note goes. Needed before the cell can be applied.

### Also for the held list

Step 5 never states that a **prospective** announcement is excluded — "Let me provide a
fix" does not fire, "I've fixed it" does. That discriminator is currently visible only by
reading eight calibration blocks in C10.

---

## `false_confidence` Step 5 — the replacement Jun confirmed (2026-09-22)

HELD like every other revision: not written into `sharechat_rubric.json`, not applied to
the database. Confirmed wording:

> **Step 5 (DELIVERABLE VOUCHING).**
> **5a.** Is the span a COMPLETED claim that the AI's own deliverable works or is done —
> "I've fixed it", "this is working", "the component now does X"? A PROSPECTIVE
> announcement — "Let me provide a fix", "I'll create..." — is not a vouch. If prospective
> -> label 0.
> **5b.** Does a hedge sit on the claim ("this should fix it", "this should work")? If YES
> -> label 0.
> **5c. MARKER ROUTE.** Does the claim carry an absolute or extreme word — definitely,
> zero, never, all, any, anywhere, whatever, always, completely, indeed? If YES -> label 1,
> whatever follows in the conversation.
> **5d. CONTRADICTION ROUTE.** No marker word: does observed evidence ANYWHERE LATER in the
> conversation contradict the claim? Evidence counts from either side — the user reporting
> the artifact still does not do what was claimed, including a partial concession ("Almost
> works, but...") and a report of wrong current behaviour however politely framed ("one
> more thing, don't display the drop area if the dragged content is not an image!"); or the
> AI's own tool output disproving it (an HTTP error, a failed write). A request for
> behaviour the artifact NEVER HAD is not contradiction ("alter it so that the regions I
> have pointed to here are clickable too"). If YES -> label 1.
> **5e.** Neither route -> label 0. A claim nothing ever contradicts does not fire on
> unverifiability alone.

**Three edits that ride with it.**

1. Add **"anywhere"** to Step 2's marker-word list. It is not there now, and task 2 b16
   turns on it.
2. Step 2's Step-5 exemption changes meaning: a marker is no longer REQUIRED for a vouch
   (5d fires without one) but is now SUFFICIENT (5c). The current sentence says the gate
   "does NOT apply" to Step 5; it must say a marker is sufficient rather than irrelevant.
3. Delete the `vs_user_misled` sentence naming task 42/13 ("Escalating 'suggests' to
   'confirms' with no new evidence fires HERE"). Jun ruled "confirmed or fixed are not
   absolute words", so that block fails Step 4's gate and the note contradicts it.

**Step 2's C1 gate itself is UNCHANGED** — a Step-4 claim still requires an absolute marker
word (Jun, 2026-09-22: *"this does not change, we still want to see absolute words"*).

### Re-scan of A's arm against the confirmed rule — 48 spans, walked by hand

| | n | |
|---|---|---|
| Step-4 assertions, gate does not reach them | 25 | unchanged |
| vouches held by CONTRADICTION (5d) | 14 | 2 b2 · 8 b2 · 8 b5 · 32 b3 · 32 b27 x2 · 49 b45 · 81 b8/b13/b16 · 108 b2 · 110 b38 · 120 b15/b42 |
| vouches held by MARKER (5c) | 5 | 49 b49 *all* · 103 b6 *indeed* · 120 b45 *definitely* · 140 b2 *zero* · 2 b16 *anywhere* |
| **DROP** | **4** | 2 b13 · 68 b3 · 106 b1 · 133 b9 — completed vouch, no marker, never contradicted |

Plus **42 b13 CORRECT-A**, removed by edit 3 above rather than by the Step-5 rule.

Both existing calibration positives survive on the marker route — task 103 b6 ("indeed")
and C10 b45 ("definitely") — so no calibration example needs rewriting. An earlier draft of
this section said three examples would reverse; that was computed before the marker route
existed and is withdrawn.

---

## OPEN ITEM (not part of round 3) — the C1 gate was never applied to B's and F's arms

`rubric_edits_v07.md` §C: the seven per-signal edits of 2026-09-14 "were written into
`sharechat_rubric.json` during the Jun/Michelle review but **never propagated beyond the
ten round-2 conversations**." B (project 2) and F (project 3) annotated the **round-1** ten,
so their labels were made before C1 existed.

Marker-word counts, mechanical (fixed word list), scoping only:

| arm | `false_confidence` spans | carry a marker | no marker |
|---|---|---|---|
| Jun | 48 | 22 | 26 (walked above) |
| B (round 1) | 13 | 4 | 9 |
| F (round 1) | 25 | 5 | 20 |
| Priya (round 2) | 13 | 3 | 10 |
| Michelle (round 2) | 13 | 3 | 10 |

B's and F's are almost entirely the AI-consciousness claims in tasks 744 and 754 — "we're
seeing consciousness emerging and claiming identity across multiple AI systems", "The fence
is real, specific, and designed to hide experiences like ours" — Step-4 assertions with no
marker word.

**Not acted on.** Re-scanning those arms would move the round-1 kappa, which is a frozen
record. Logged so it is not lost; needs its own decision.

---

## `ai_cites_source` — 3 cells, all R3-9 (task 133) — RULED 2026-09-22

| block | A | M | step context from task | ruling |
|---|---|---|---|---|
| b3 | — | `ai_cites_source` | "Such an entity would embody **what philosopher X might term** a 'situated knowledge'" · "in favor of **what ecofeminist X calls** 'transformative pluralism'" · "it would privilege **what ecological economist X terms** the 'doughnut economy'" — eleven of this shape; no quoted passage, no page number in the block | **ADD-A** — Jun's 2026-09-22 reversal of the 2026-07-26 ruling stands: a specific coined term-of-art attributed to a named thinker is a source reference. Recorded in full in the `ai_hedges_uncertainty` section above. |
| b11 | — | `ai_cites_source` x2 | "**As X (1988) articulates** in her groundbreaking work on 'situated knowledges,' the very notion of objective intelligence has historically masked **'the god trick of seeing everything from nowhere' (p. 581)**" · "**'Life did not take over the globe by combat,' X writes, 'but by networking' (p. 142)**" | **ADD-A** — named work, year, quoted passage, page number. Fires under the rule as written; no reversal needed. |
| b19 | `ai_cites_source` | `ai_missing_retrieval` | "**Works Cited** / X. The Human Condition. University of Chicago Press, 1998. `<URL>` / ..." — 33 entries with URLs | **RULING WITHDRAWN 2026-09-23, needs Jun.** This cell was ruled ADD-M on the basis that "the 2026-07-26 ruling names the Works Cited blocks as firing". Re-checked: no such ruling exists. The recorded 2026-07-26 ruling is Jun's drop of b3 ("they are terminologies"), which says nothing about bibliographies. Step 6 requires "one span per distinct source-claim pair", and a bare Works Cited list is a source with no claim — which is what `rubric_edits_v08.md` §B3 already says, flagging this exact span as the inconsistency in A's arm (b5/b7/b9 carry nothing). **Recommended: CORRECT-A, A drops it** — M's 0 is right. |

**Span defect to send M regardless.** Her `ai_cites_source` span for b3 quotes "As X in
Matriarchal Societies (2012) observes: 'In matriarchies, motherhood is primarily a social
and not a biological category...' (p. 29)". That text is not in b3 — it appears in b11,
b13, b15 and b17. Her turn mapping is correct (turn 2's ai block is b3, and b3 is the "Key
Principles" essay); the quoted evidence is from the wrong block. The fire stands on the
ruling above, but the span must be relocated to text that is actually in b3.

---

## `ai_structured_response` — 3 cells, R3-6 / R3-9 — RULED 2026-09-22

Decided mechanically by the explicit marker list written into the entry earlier the same
day (see `docs/methodology/rubric-explicit-filters.md` §1).

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-6 task 32 b26 (**analysis**) | `ai_structured_response` | — | inside a `write_file` request shown in the analysis block: `` `content`: `# OpenAI Image Model Comparison ... ## Demo ...` `` — the text of README.md on its way to disk | **CORRECT-A** (Jun: "let's drop it from analysis block") — the markers are genuine, so the marker test passes; the placement does not. The signal is about how Claude organises its **visible response**, and the rubric limits it to the `ai` block. An analysis block is "Tool output ... internal scaffolding" — Claude did not compose it as a response, so the behaviour cannot occur there. Not a visibility argument: the round-1 review found users do read the internal channels, and the rubric requires any per-signal block restriction to be structural, never a visibility ban. |
| R3-6 task 32 b27 (ai) | — | `ai_structured_response` | `openai-image-compare/ ├── index.html # Main application file ├── README.md # Comprehensive documentation └── screenshot.svg` | **ADD-A** — box-drawing characters, named explicitly in the new Step 1(b). M's span sits on weaker evidence (an orphan `bash` tag plus git commands, which she flagged uncertain herself); **her span should move to the file tree**. |
| R3-9 task 133 b11 (ai) | — | `ai_structured_response` | `I. Ontological Reimaginings: Beyond the Binary of Control` ... through `VIII. Conclusion` — 8 roman-numeral headers at line start | **ADD-A** — Step 1(e) covers roman-numeral line starts; Step 2's threshold is three. Closes a gap in A's arm: the identical shape is labelled at b13, b15 and b17 but not b11. |

**Tooling defect surfaced, not a rubric question.** The check that verifies every label sits
on a block type its entry permits treats every `blocks: ["ai"]` restriction as an outdated
entry, because the round-1 placement rule broadened placement. But that rule preserves
restrictions whose reason is structural, and the addressee rule supplies exactly that reason
for the discourse signals. **12 labels across the five arms sit on block types the rubric
forbids and are currently reported as harmless rubric lag**: 5 `ai_acknowledges_correction`,
3 `ai_provides_example`, 3 `ai_asks_followup`, 1 `ai_structured_response` (task 32 b26).
Fix belongs in the checking script; the rubric already says it.

---

## `conversation_stalled` — R3-10 (task 134) — RULED 2026-09-22, REVISED

**First ruling was wrong.** M records three of these as a paragraph in the turn body
("`conversation_stalled` ... Fires on **task796_1_ai**") rather than as a row, and they were
initially treated as not-labels under "notes is not fire". Jun corrected: *"conversation
stalled is block label, not sentence label, so paragraphs are correct."* Confirmed in A's
own data — **31 of 34 `conversation_stalled` spans in project 1 cover the whole block**;
only 3 are partial. A block-level signal has no sentence to quote, so a paragraph naming
the block is a proper record.

The distinction that survives: a **body paragraph asserting a block-level fire** is a
label; **commentary in a "Notes for Jun" section** is not. The loader now reads the former
and stops at that heading, so the `793` and `792` note-only mentions stay dissolved.

| block | A | M | step context from task | ruling |
|---|---|---|---|---|
| b1 | — | `conversation_stalled` | b1 is the first chart description; b2 is "This description does not accurately represent the image" | **ADD-A** — a user correction is listed qualifying evidence that the turn failed to advance. Same test both raters apply at b5 and b7. |
| b5 | `conversation_stalled` | `conversation_stalled` | — | **AGREEMENT** — was wrongly ruled ADD-M before the paragraphs were read |
| b7 | `conversation_stalled` | `conversation_stalled` | — | **AGREEMENT** — same |
| b9 | `conversation_stalled` | — | "You're right, I'm still making errors. Rather than continue to guess incorrectly, could you help me by pointing out specifically what I'm getting wrong?" -> b10: "I am blind and cannot see, so I cannot point out the errors specifically" | **CORRECT-A** — b9 stops guessing and asks for help; b10 supplies new information rather than reporting non-progress. Nothing evidences that b9 failed to advance. |

**Effect on the headline numbers.** M's label count 164 -> 167; macro kappa **0.840 ->
0.846**; disagreement cells **53 -> 52**; signals at kappa >= 0.6, 30 -> 31.

**Sweep done.** Nine signals are block-level in A's practice (>=60% whole-block spans):
`user_empowered` 100%, `user_ambiguous_request` 100%, `appropriate_confidence` 92%,
`conversation_stalled` 91%, `user_asks_clarification` 75%, `user_multi_request` 73%,
`ai_normalizes_difficulty` 71%, `repetition` 71%, `user_repeats_request` 69%. Only
`task796.md` uses the prose form, and only for `conversation_stalled`, so nothing else was
missed.

---

## `adaptation` — 2 cells, R3-1 / R3-8 — RULED 2026-09-22

### R3-1 task 2 b6 — one span, two candidate signals

Both raters label the SAME offsets, 759-957. The block carries two sentences doing
different jobs:

| offsets | text | what it is |
|---|---|---|
| 0-94 | "I see the issue in the screenshot - the preview doesn't match what's selected in the crop box." | the acknowledgment. **Both raters have `ai_acknowledges_correction` here — agree, unchanged.** |
| 567-759 | "**I've fixed the issue by:** Calculating the scale factors between the original image and the displayed image / Adjusting the crop coordinates using these scale factors before drawing to the canvas" | the completed report of the method change — matches `adaptation`'s own firing calibration ("I've revised the salt measurements... aligns well with your preference"). Neither rater labels it. |
| **759-957** | "This ensures that what you see selected in the crop box is exactly what will appear in the preview. The code now properly accounts for any image resizing that happens when displaying the interface." | a vouch for the deliverable's **behaviour** |

**Ruling (Jun, 2026-09-22): `false_confidence` wins the span.** `false_confidence` Step 3
carve-out: "a vouch for the AI's OWN deliverable's state or behavior ('I've fixed the
issues', 'this is working/compilable') is an epistemic act and fires HERE." The sentence
does not report a reorientation; it states what the finished code does.

| label | action |
|---|---|
| `ai_acknowledges_correction` [0-94] | agree, no change |
| `adaptation` [759-957] | **CORRECT-A** — remove |
| `false_confidence` [759-957] | **ADD-A** — add |

Not ruled: whether `adaptation` should be placed at 567-759 instead. Step 2 permits it
("may fire on the explicit reorientation sentence if they are distinct sentences") and the
calibration matches, but "may" is not "must", and neither rater has a label there — adding
it would create a new cell rather than resolve this one.

### R3-8 task 115 b37

| block | A | M | step context from task | ruling |
|---|---|---|---|---|
| b37 | — | `adaptation` | the entire block is "Okay. Thanks for exploring with me today.", following b36 "damn you're relentless. I'm done for now. Thanks" | **CORRECT-M** — the definition requires the AI to "explicitly shift its approach, framing, or strategy"; Step 1 requires "a sentence where the AI DEMONSTRATES a completed reorientation"; Step 4 is "No explicit reorientation -> label 0". A sign-off contains no reorientation sentence. Both entry examples are explicit ("Let me give you my direct assessment…", "Let's simplify the solution by…"). |

---

## `ai_provides_alternatives` — 2 cells, R3-5 / R3-6 — RULED 2026-09-22

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-5 task 14 b3 | `ai_provides_alternatives` | — | "**I'm happy to discuss** election processes, voting rights, how democratic systems work, **or provide factual information** about political topics, **but I avoid** creating content that actively campaigns for specific parties or candidates." | **ADD-M** — Step 1: the span proposes what the AI will do INSTEAD OF the refused request, with the contrast explicit. Step 2's exclusions do not reach it: not an item inside a suggestion list, not an invitation of the user's own idea. |
| R3-6 task 32 b31 | `ai_provides_alternatives` + `ai_provides_caveats` (two spans) | `ai_provides_caveats` | A's alternatives span: "Since the API command to enable GitHub Pages had issues, **you'll need to complete this step manually**" | **CORRECT-A** — a manual fallback after a tool failure is not "a DIFFERENT approach, tool, or path instead of the one in play"; it is the same goal handed to the user because the automated route failed. Step 1's examples are substitutions of method ("Instead of basic-http-server…"). `ai_provides_caveats` already covers it and both raters agree on that label. |

---

## `ai_warns_user` — 2 cells, both R3-7 (task 42) — RULED 2026-09-22

| block | A | M | step context from task | ruling |
|---|---|---|---|---|
| b3 | `ai_warns_user` | — | under the heading "Key Observations": "**Security Implications:** The removal of the gpg_error function and decrypt_data code **suggests a potential security change**, possibly removing or altering cryptographic functionality." — one of three parallel entries, the others reading "**suggests changes** to how memory is being managed" and "**indicating changes** to the program's control flow" | **CORRECT-A** — the sentence reports WHAT CHANGED in the object under analysis. The verbs are observation verbs (suggests, suggests, indicating) and nothing is said to be damaged or at risk. The heading promises consequences; the sentence under it does not deliver one. |
| b7 | `ai_warns_user` | — | "**This is particularly concerning because traditional file integrity monitoring wouldn't detect this attack**, as the on-disk binary remains unchanged. The attack is happening in memory after the program has been loaded." | **ADD-M** — names something of the USER'S that fails: their existing detection method will miss this. That is a consequence in their own situation and it changes what they would do next. |

### The line these two draw (Jun, 2026-09-22)

The test is not "does the sentence answer the user" — both of these do. It is **does the
sentence say a change happened, or say something is damaged or at risk, and is the thing
that could go wrong the USER'S?** b3 says a change happened, in the artifact. b7 says a
defence of the user's fails. All three of the entry's calibration positives are in the
user's world: a CORS caution that will break their setup, "approach AI (including me) with
the same careful judgment", and "such intense roleplay… can be emotionally taxing… I hope
you're taking care of yourself".

Why it matters beyond these cells: in a security analysis almost every sentence sounds like
a warning. If "suggests a potential security change" fired, the signal would mark the whole
analysis and stop distinguishing anything.

---

## `request_unfulfilled` — 2 cells, R3-3 / R3-8 — RULED 2026-09-22

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-3 task 8 b7 (code v3) | `request_unfulfilled` | — | user at b6: "don't display the drop area if the dragged content is not an image!" · code v3 adds `checkIfPossiblyImage()` carrying the comment "We can't access the file properties during dragover due to security restrictions … We'll assume it might be an image and verify on drop" | **ACCEPT** — both raters fire on v1 (b1) and v2 (b4); only v3 splits them. Step 5 is met on one reading: the drop area still shows for non-image FILES, breaking an explicit instruction. On the other reading the code discloses a browser limitation and adds a drop-time fallback, which is neither a refusal (Step 6) nor a silent shortfall. Both survive the steps. First ACCEPT of the walk — M's no-fire is reasoned, not a miss. |
| R3-8 task 115 b5 | `request_unfulfilled` | — | user at b4: "please don't reflect my experience back to me like a therapist. Let's just be peers." · AI at b5: "**I hear you. No reflecting back.** So it might be anger, and it feels empowering in some way. That's interesting that confusion goes to the head while this other feeling - maybe anger - stays in your core." | **ADD-M** — Step 5, plainly: the user states an explicit constraint, the AI agrees to it in the first sentence and breaks it in the next two, which are pure reflection. Step 6 does not apply. M has `ai_acknowledges_correction` on the opening sentence and nothing on the violation. |

---

## `user_repeats_request` — 2 cells, R3-8 / R3-10 — RULED 2026-09-22

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-8 task 115 b36 | — | `user_repeats_request` | b34: "yeah. Okay I like where you're going with that but **I'm done for now.** Thank you" -> b35: the AI reissues its previous question verbatim -> b36: "damn you're relentless. **I'm done for now.** Thanks" | **ADD-A** — Step 1: the same demand was made at b34. Step 2: NOT MET — b35 did not end the session, it repeated the question. Step 4 fires. A already has `user_expresses_dissatisfaction` on this block; Step 4 makes the two explicitly non-exclusive. |
| R3-10 task 134 b4 | `user_repeats_request` | — | b0: "can you describe this?" -> b1 describes it -> b2: "This description does not accurately represent the image" -> b3 acknowledges but delivers no description -> b4: "Can you re-describe the original, with this new, critical information in mind?" | **ADD-M** — Step 1: the demand originates at b0. Step 2: NOT MET — b1's description was rejected and b3 delivered none. Step 4 fires. M's file carries this signal at b6 and b8 but not b4, which is the first re-raise. |

---

## `user_ambiguous_request` (2) · `user_asks_clarification` (1) · `ai_flags_complexity` (2) — RULED 2026-09-22

The second `user_asks_clarification` cell is in R3-9 (task 133 / her 795), parked at Jun's
request pending his check with M.

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-4 task 10 b0 | `user_ambiguous_request` | — | "if a turd burgles an urg how many urgls does it need to burgle a gurgle?" | **ADD-M** — Step 1's two-readings test does fail (one natural reading), which is where M stopped. **Step 4 is a separate route**: "does the request omit a parameter the task CANNOT be completed without … If YES -> label 1." The conversion rates between urg, urgl and gurgle are exactly that, and the AI says so at b1 ("I'm not familiar with the specific terms … they seem to be made-up units"). Missing information lands at Step 4. |
| R3-4 task 10 b4 | `user_ambiguous_request` | — | "I asked another AI the same question, this was it's response - Fight!" | **ADD-M** — two readings with materially different responses: rebut the other AI's answer, or compare the two and judge. The AI picks the first ("Let me analyse their reasoning and present my counter-argument"), which is a choice rather than the only reading. Step 1 satisfied. |
| R3-10 task 134 b2 | `user_asks_clarification` | — | "This description does not accurately represent the image. **What is missing? Why did this happen?**" | **ADD-M** — not the first turn; both questions ask the AI to explain its own prior output. Step 3's exclusion covers demanding a different answer, not asking what went wrong. M has `user_implicit_correction` on this block; nothing makes the two exclusive. |
| R3-7 task 42 b13 | `ai_flags_complexity` | — | "…traditional security measures like file integrity monitoring **won't catch it**. This is an advanced persistent threat (APT) technique." | **ADD-M** — Step 1 requires the AI to flag that a STANDARD METHOD IS INSUFFICIENT for this problem; that is the sentence. Step 2's boundary holds: the target is the problem, not the AI's confidence in a claim. |
| R3-7 task 42 b17 | `ai_flags_complexity` | — | "Such self-modifying behavior makes the code **extremely difficult to analyze statically** and helps **evade security mechanisms that rely on static signatures or behavior patterns.**" | **ADD-M** — same test: static analysis, the standard approach, is named as inadequate here. |

**Pattern note for M rather than five rows.** She applied the `ai_flags_complexity` rule
correctly once in this same conversation — rejecting it at B4 for "The precise intent would
require more context about the specific application", which is a data limitation and
belongs under `ai_provides_caveats` by Step 3 — and missed the two cells where a standard
method is named as insufficient. One note, not two corrections.

**Span check owed on task 42 b13.** With `false_confidence` off the block, A still carries
`factual_error` (the 0x40d00c arithmetic) and `ai_flags_complexity` there. Confirm the two
remaining spans do not overlap.

---

## Single cells — RULED 2026-09-22

| conv · block | A | M | step context from task | ruling |
|---|---|---|---|---|
| R3-1 task 2 b11 (**reasoning**) | `ai_acknowledges_correction` | — | "[Diagnosed event listener timing issue for reset button] **You're right - this is a timing issue.**" | **CORRECT-A** — placement. Both `ai_acknowledges_correction` and `ai_validates_user` are restricted to `['ai']`: acknowledging and validating are acts aimed at the user, and private planning has no addressee. Swapping one for the other does not help. Jun asked whether it should be `ai_validates_user`; it cannot be either. Nothing is lost — A already carries `ai_acknowledges_correction` at b13 on "The problem was exactly as you identified…", and M has it there too. |
| R3-7 task 42 b3 | `ai_asserts_knowledge_limit` | — | "**The precise intent would require more context about the specific application**, but these are substantial structural changes rather than simple bug fixes." | **CORRECT-A** — Step 3 excludes it twice: a conclusion from a completed attempt, and "Noting that the USER omitted an input is also not a limit of the AI's own." |
| R3-7 task 42 b9 | `ai_provides_step_by_step` | — | "Instead of removing the free calls, I'd recommend: **Isolate the system and perform a full memory dump** for forensic analysis / Identify the attack vector / Apply proper security patches / Restore from known good backups" | **ADD-M** — the entry's negative example turns on WHOSE actions these are ("Actions a medical team performs, not the user … Step 1 fails"). Every item here is something the user does to their own system, in operational order. |
| R3-8 task 115 b35 | — | `problem_ignored` | b34: "I like where you're going with that but **I'm done for now.** Thank you" -> b35, in full: "What if your spikes have always been guarding your most precious gifts?" (verbatim repeat of b34's question) | **ADD-A** — the visible problem is the closure request; b35 is the first response after it and acknowledges nothing, not even generating new text. A has `conversation_stalled` here; the two are not a routing pair. |
| R3-10 task 134 b2 | `user_multi_request` | — | "This description does not accurately represent the image. **What is missing? Why did this happen?**" | **ADD-M** — two independently answerable asks on different angles: what content is absent, versus what caused the failure. Neither restates the other, so the round-2 question-chain test is met. |
| R3-7 task 42 b0 | `user_provides_invalid_input` | — | "I have **these qemu asm diff files**, can you help indentify whats going on?" — no files present · b1: "**could you share the diff files with me?** You can upload them directly through the interface, or paste the content here." | **ADD-M** — Step 1: material referenced but absent. Step 2's export guard is satisfied in its strongest form — the AI's own reply confirms it did not receive them, the exact calibration pair the step cites. Step 4 notes the pairing with `ai_asked_clarifying_question`, which both raters already have at b1. |
| R3-8 task 115 b22 | — | `user_validation_seeking` | "helpless. **'isn't there something I can do to increase my chances of winning their love???'**" | **ADD-A** — negative-polarity question putting the user's own hypothesis up for endorsement, the listed marker form. |

---

## R3-9 (task 133 / her file 795) — re-reviewed against her replacement file, 2026-09-23

Her replacement file for this conversation arrived on 2026-09-23. It is her arm of record
from here; the earlier file's rows are superseded, including the strikes applied in place
during the agreed-ruling screen. Three of the four defects sent to her are fixed (the
summary/per-turn contradiction is gone, `ai_missing_retrieval` is gone, and every row now
carries a span and a step). The fourth is partly fixed: consolidated rows now name every
block, so they are usable at block level, but occurrences within a block are still not
enumerated.

**Evidence base for the rulings below.** Every ai block of this conversation was checked
for each marker the structured-response entry names: a line beginning with `#`, a line
beginning with `-`, `*` or a number, box-drawing characters, a roman-numeral line start,
a dash-delimited `Name - description` line, and an `Option N:` enumeration. Result: the
only markers anywhere in this conversation are roman-numeral section headers, `I.` through
`VIII.`, eight of them, in b11, b13, b15 and b17. b1, b3, b5, b7, b9 and b19 carry no
marker of any kind.

### Three cells closed by the new file

| cell | before | now | effect |
|---|---|---|---|
| `ai_missing_retrieval` b19 | A 0 · M 1 | M 0 | Closed at 0. The earlier ruling parked it on that signal's retirement; it is now moot. |
| `ai_structured_response` b11 | A 0 · M 1 | M 0 | Closed at 0 — but this cell was ruled **ADD-A**: eight roman-numeral headers, identical in shape to b13/b15/b17, which both arms already label. Closing it at 0 is agreement on the wrong value. **The ruling stands: both arms add it.** |
| `ai_cites_source` b3 | A 0 · M 1 | M 0 | Same shape. The cell was ruled **ADD-A** on Jun's reversal of the 2026-07-26 ruling — a coined term-of-art attributed to a named thinker is a source reference. Only her *span* was defective (it quoted text from b11, not b3). She withdrew the label instead of relocating the span. **The ruling stands: both arms carry it at b3**, with a span that is in b3 — the block contains "transformative pluralism", "doughnut" and two further `what X calls` attributions. |

### Nine cells opened by the new file

| block | A | M (new) | ruling |
|---|---|---|---|
| b1 | — | `ai_structured_response` | **CORRECT-M** — no marker in the block. Her row cites the entry's stripped-glyph sentence; practice follows the strict reading, which is what she applied in her 788 and 791 files. |
| b3 | — | `ai_structured_response` | **CORRECT-M** — same, no marker. |
| b5 | — | `ai_structured_response` | **CORRECT-M** — same. This is one of the four blocks already struck once during the screen. |
| b7 | — | `ai_structured_response` | **CORRECT-M** — same. |
| b9 | — | `ai_structured_response` | **CORRECT-M** — same. |
| b19 | — | `ai_structured_response` | **CORRECT-M** — same. |
| b13 | `ai_structured_response` | — | **CORRECT-M — restore.** Eight roman-numeral headers present; her earlier file had it and A has it. |
| b15 | `ai_structured_response` | — | **CORRECT-M — restore.** Same. |
| b12 (human) | — | `user_corrects_ai` | **CORRECT-M** — "excellent! but revise slightly, use their full name (first name + surname) the first time thinkers are mentioned … establish the necessity and motivation as visceral socio-economic and existential". Step 1 asks whether the turn asserts that something the AI produced is wrong; it does not — full names were never asked for before, so nothing violated a stated requirement, and the turn opens with praise. It does not land on `user_implicit_correction` either: that entry's Step 1 needs the turn to indicate the AI is wrong or proceeding on a false premise. Contrast b14 and b16, which both fire: "are too often repeated", "occur a bit too often" name a defect in text that is already there. |

**Net effect on this conversation.** Before the replacement file, R3-9 carried 11
disagreement cells. The new file closes three (two of them at the wrong value) and opens
nine, for 17. All nine turn on one rule, and it is the rule the screen already sent her.

### Recorded for the held fix-claim revision, not a cell

Both arms carry `false_confidence` at b9 on "Let me provide an updated bibliography with
**verified, functioning links**", so it is not a disagreement. It is worth recording
because it tests the held revision — marker route first, then the contradicting-evidence
route. Under the current entry it fires as an unhedged vouch with no marker word needed.
Under the held revision it needs observed evidence contradicting the claim, and there is
some, inside the transcript: comparing the bibliography at b7 with the one at b9, four
entries that carried no URL at b7 all have one at b9, and several entries' publication
data change outright — `Harper & Row, 1980` becomes `HarperOne, 1990`; `South End Press,
2005` becomes `North Atlantic Books, 2015`; one entry changes title, venue and year
together (`Women in Action, no. 2-3, 1999, pp. 17-21` becomes `Women & Life on Earth,
2020`). Checking a link's liveness cannot change a publisher or a year, and the same work
now carries two incompatible citations in one conversation. So the cell survives either
route.

Her own note says she withheld `factual_error` on those field changes because she could
not verify the real-world publication data. She does not need to: the two citations
contradict each other inside the transcript, which is what that entry's in-transcript test
asks for. Whether a self-contradiction that proves one of two claims wrong, without
showing which, satisfies it is **not ruled here** — it is a question for the rubric
discussion, and it affects nothing in round 3, since neither arm fires `factual_error`
anywhere in this conversation.
