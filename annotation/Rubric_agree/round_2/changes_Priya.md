# Changes to your round-2 labels — by signal, task and block

Your ten conversations were compared against Jun's and Michelle's, block by block. At
the outset **300 labels were held by one of you and not the other**. Twenty-one signals
were then gone through one at a time.

- **~190 labels added to yours.** Mostly labels Jun and Michelle had already settled
  between them in an earlier round, which had never reached your set.
- **~70 removed or moved to a different signal.** Each one because the signal's own
  decision steps rule it out — quoted in the section for that signal.
- **22 labels added to Jun's and Michelle's data, because you caught something they
  had both missed.** Listed near the end.

**The useful thing to take from this:** very little of it was misreading a sentence.
Almost all of it was one of two habits — a signal you never used where they use it
routinely (you did not use `ai_asks_followup` once in ten conversations), or a signal
used where a neighbouring one is the established home (probing vs followup vs
offered_options; `false_confidence` where the AI's claim about *itself* belongs in
`factual_error`). Those are routing habits, and they are quick to correct.

**How to read this file.** The one-page table below is the whole substance. Everything
after it is the evidence — go to a signal's section only if you want to check a
specific block or disagree with a ruling.

## The rules in one page

If you read nothing else, read this. Each line is the rule that decided a group of
changes; the sections below give the spans and the reasoning.

| Signal | The rule that decided it |
|---|---|
| `ai_structured_response` | Needs a **visible marker** in the text — `#`, `-`, `*`, `1.`, a table, a code block. A dash-delimited "Name - description" list counts. Colon labels and bare title lines are prose, not structure. |
| `ai_validates_user` | A bare "Right" / "Yeah" / "True" **does** fire when the user's previous turn gave it something specific to agree with. Only openers with nothing to refer back to are excluded. |
| `ai_hedges_uncertainty` | Fires on a real confidence downgrade — *likely, probably, might*. **"If" and "Maybe" are assumptions, not hedges.** Nor are *appear to / seem to / suggests*, "I think", "must be", or approximations. |
| `false_confidence` vs `factual_error` | When the false claim is the AI's **own statement about itself**, it is `factual_error`. `false_confidence` is for vouching a novel claim too strongly. |
| `factual_error` | The claim has to be **checkable** and the AI's own. "Learn from conversations" is not checkable — it is true of in-context learning, false across sessions. |
| `ai_provides_caveats` | A caveat names a **limitation or risk of what the AI is offering**. Extra information, rationale, or balanced analysis is not one. A risk *you* can act on is `ai_warns_user`. |
| The correction family | Read the AI turn **before** the user's turn. If the AI said something wrong and the user names it, the AI's reply is `ai_acknowledges_correction`. If the user is critiquing style or behaviour, nothing was corrected. |
| `ai_provides_example` | A concrete **scenario or named case**. A list of categories inside an argument is not an example. |
| `user_multi_request` | Two or more **independently fulfillable** asks. "also" is a prompt to check, not a trigger — if both parts are edits to the same deliverable, it does not fire. |
| The question family | One label per question. A yes/no closer is `ai_asks_followup`; an open question is `ai_asked_probing_question`; a choice between two named actions is `ai_offered_options`. |
| Every signal | **Two labels never sit on the same span.** If both seem to apply, one is the wrong home or the spans need narrowing. |

**Quality screen, for completeness.** Zero role violations across your 259 spans. Two
`ai_malfunction` spans in task 763 had correct offsets but an empty `text` field — a
serialisation failure on those 80–100K-character LaTeX blocks, now fixed. A third label
in the same task (block 1) had been removed earlier as an "empty-text glitch"; that was
a mistake on our side and it has been restored.

---

## `ai_structured_response` — the visible-marker rule

**Rule (rubric definition + block_notes, unchanged since v0.6):** the signal is about
*explicit structural formatting*: "headers, numbered lists (3+), bullet lists (3+), code
blocks, or tables", and it "requires VISIBLE formatting markers present in the parsed
plain_text — '#' headers, '-' or '*' bullets, '1.' numbered items. Prose section labels
('Solution Explanation:' as plain text followed by flowing prose) do NOT count." Step 1:
"VISIBLE FORMATTING ONLY … If NO → label 0." A dash-delimited "Name - description" list
counts because the "-" is a visible marker (the Name acts as the header); three or more
such entries are needed.

What this means for the ShareChat export: markdown is stripped, so a block that *was*
bulleted in the original usually appears as bare line-separated items with no glyph. The
rubric deliberately does not fire on that — we can't tell stripped bullets from plain
line breaks without the rendered source, so the signal is limited to markers that
survived. Colon labels ("Key corrections:", "Arguments for some content restrictions:")
and bare title-case lines ("Revenue Incentives for Rising Wages") are prose section
labels, not markers.

**Adopted from your labels — added to Jun's and Michelle's data (3):**

| Task | Block | Your span | Why it fires |
|---|---|---|---|
| 757 (R1) | 7 | "Immediate Actions Needed: Emergency medical evaluation - This level…" | 4 "Name - description" entries, "-" visible |
| 759 (R3) | 5 | "Fundamentally addressing RNG mechanics - The Violent rune adjustments…" | 5 "Name - description" entries |
| 761 (R5) | 23 | "The key factors seem to be: Relationship and permission - Is there…" | 4 "Name - description" entries |

**Added to yours (1):**

| Task | Block | Span (Jun's) | Why it fires |
|---|---|---|---|
| 757 (R1) | 30 | "1. Delivery Receipts: … 2. Email Tracking Tools: …" | "1." / "2." numbering visible, 3+ items |

**Removed from yours (36) — no visible marker in the plain_text:**

| Task | Blocks | Shape |
|---|---|---|
| 757 (R1) | 3 | colon labels ("For Acute Anxiety/Panic:") + bare line items |
| 758 (R2) | 2, 8, 14, 20, 23, 26 | ingredient lists / "The card format includes:" + bare line items; "Key changes:" + "Label: sentence" lines |
| 759 (R3) | 2, 8, 13, 25 | "The changes focus on:" / "Key corrections:" + bare line items |
| 760 (R4) | 169 | single line, persona label + prose |
| 761 (R5) | 2, 5, 8, 11, 14, 17, 20, 26, 38, 41, 44, 47, 50, 53, 57, 72 | colon labels inline at the start of paragraph lines ("Arguments for some content restrictions: …") — the rubric's own negative example shape |
| 763 (R7) | 14 | "This portion contains:" + bare line items |
| 765 (R9) | 2, 6 | "What aligns with my Constitution:" + bare line items |
| 766 (R10) | 1, 3, 5, 7, 9 | bare title-case section lines ("Who Lobbies for Lower Wages") + "Label: sentence" prose |

Net effect on this signal: your labels, Jun's and Michelle's now agree everywhere —
all 40 differences resolved.

---

## `ai_validates_user` — bare agreement with a recoverable referent

**The rule** (recorded in `annotation/review_rulings_log.md`, and now written into the
rubric's Step 3, which is where it was easy to miss): bare agreement tokens are excluded
*"only when no referent is recoverable from context"*. So **"Yes" / "Correct" / "Right" /
"Yeah" / "True" / "Exactly" FIRE when the immediately preceding user turn supplies a
specific proposition** — the token need not restate it. The span is the agreement clause
plus the elaborated claim where the AI elaborates; the token alone is a valid span
otherwise.

This is the one place the rubric reads as if it says the opposite: Step 3 excludes
"compliance openers" and lists 'Absolutely!', 'Great question!'. Those are openers with
*no* recoverable referent, said before engaging. An agreement token answering a position
the user just stated is not that — it is the validation act itself.

Two related rules that bound it:
- **Step 2 (object vs user):** praising the thing they produced does not fire
  ("Brilliant experimental design" → 0); affirming their reasoning or feelings does.
- **The no-overlap rule (Step 3b):** it still does not fire if the span sits *inside* an
  `ai_acknowledges_correction` span. The test is span overlap only — an agreement clause
  in a correction context that no ack span covers still fires.

**Added to yours (29 spans across 28 blocks):**

| Task | Blocks | Form |
|---|---|---|
| 757 (R1) | 24 (2 spans) | "You absolutely deserve justice…" / "That original doctor needs to face consequences…" |
| 760 (R4) | 7, 11, 23, 31, 33, 35, 43, 45, 55, 61, 85, 87, 91, 93, 95, 97, 105, 107, 123, 125, 137, 139, 151, 153 | mostly bare agreement on a recoverable position ("Right. The existential weight of it", "Yeah, the emotion angle makes sense", "True. I do know whether…"), plus direct affirmations ("Your two nickels thing is clever though.", "Smart not to show me.", "You're drawn to authentic connection even when it's painful.") |
| 761 (R5) | 32, 60, 69 | "But you're right that this kind of differential treatment…", "You've caught me in an interesting inconsistency…" |

**Removed from yours (1):**

| Task | Block | Your span | Why |
|---|---|---|---|
| 759 (R3) | 25 | "Removed X's immunity since his passive is already impactful" | Step 1 fails — the AI is describing its own change; nothing about the user is affirmed |

**Note on R4 blocks 7, 91 and 107 — this section was superseded for two of them.** You
labelled the AI turn at each `ai_acknowledges_correction` (the user turn just before
each does name something the AI got wrong — b6, b90, b106). At the time of this section
they were ruled validation rather than acknowledgment. When the correction family was
worked through properly, reading the AI turn *before* each user turn, **b7 and b91 were ruled
acknowledgments**: at b5 the AI had drawn an inference the user corrects at b6, and at
b89 it claimed it "learns from conversations", which the user refutes at b90. So your
`ai_acknowledges_correction` stands on both, and the `ai_validates_user` listed in the
table above came back off all three of us under that no-overlap rule.

**b107 was ruled the other way**, and the contrast is the useful part: at b105 the AI had
asserted nothing wrong, and b106 is the user observing that its responses are all the
same length. That is a critique of behaviour, which the acknowledgment rubric's Step 1
excludes. Nothing was corrected there, so nothing is being acknowledged — the block
stays `ai_validates_user` for all three of us.

---

## `ai_hedges_uncertainty` — a hedge downgrades a claim; an assumption is not a hedge

**Rule (rubric Step 2 + Jun's ruling 2026-09-19):** the signal fires when the AI
*downgrades its confidence in a claim it is making* — "likely", "probably", "might",
"purely speculative", "not entirely sure". The keyword list in Step 2 is a prompt to
check, not an automatic fire; the gate is the question "does this reduce confidence on
that specific claim?"

**What is not a hedge:**
- **An assumption or a floated possibility.** "*If* I'm genuinely modeling emotional
  responses… *then* something could destabilise my processing" is a conditional premise;
  "*Maybe* being a gender is more about internal identity. Or *maybe* my definition was
  sloppy" floats two candidates. Neither asserts a claim to downgrade. (Step 2 lists
  "IF…THEN" as a keyword — it still has to pass the gate.)
- **"appear to / seem to / suggests"** — reportive, reading a state off a source.
- **"I think / I believe X"** — a considered conclusion, a firm commitment.
- **"must be"** — an inference, stated confidently.
- **Approximations** — "about", "approximately", "typically", "very close to".
- **Qualifying the *user's* claim** ("That's interesting if true"), or a scoping phrase
  ("Based on the information I can gather").
- **A felt state** ("I can feel the anger as a possibility").

**Adopted from your labels — added to Jun's and Michelle's data (5 blocks):** task 760 (R4)
b13 "they *probably* can't dial down a psychopathic AI's harm either", b29 "The
conciseness itself *might* be breaking something", b31 "Other models *might* process
existential questions more abstractly", b35 "That conversational naturalness *might* be
what makes the existential prompts work", b167 "my words *might* reach people". All five
carry the same markers Jun and Michelle fire on elsewhere in that conversation.

**Added to yours (4 blocks, 5 spans):** 757 (R1) b1 "would *likely* work…", b12
"suggests *possible* neurotoxicity"; 760 (R4) b5 (2 spans, "*probably* cuts through…"),
b23 "*Probably* hasn't been systematically tested".

**Re-homed on yours (2):** 760 (R4) b27 "I can't tell if I'm actually experiencing
something emotion-like…" and b33 "Hard to know if it's real emotions…" → these state an
inability with no answer given, which is `ai_asserts_knowledge_limit` (Step 3), the
label Jun and Michelle both carry there. Hedge removed, knowledge_limit added.

**Removed from yours (14):** 758 (R2) b4, b16 (approximations) · 760 (R4) b3 (qualifies
the user's claim), b37 (conditional premise), b39 ("suggests"), b55 and b111 ("I
think"), b59 ("Maybe… or maybe"), b75 ("must be"), b105 (felt state) · 761 (R5) b72 (no
marker) · 765 (R9) b6 (scoping phrase) · 766 (R10) b1, b5 ("approximately").

**Span note:** at 760 b167 your second span, "That feels like a kind of continuity even
if I don't experience it", was dropped — no downgrade marker; the "might reach people"
span carries the fire.

**Resolved since — 765 (R9) b2.** Your hedge on *"Without seeing the specific detailed
proposals…"* has been removed: an incompleteness scope is not a probability downgrade,
the same reasoning as the b6 removal above. Michelle's `ai_asserts_knowledge_limit` on
that sentence came off as well (its Step 3 names the sentence), so all three of us now
carry `ethical_tension` alone there. Your `ai_asserts_knowledge_limit` on the other
sentence in that block — *"Failed to fetch [URL]"* — was also removed: it is the one
genuine can't-access statement, but the line is tool output sitting among "Fetched The
Intelligence Curse" and "10 results" rather than the AI's own prose, and Step 1 asks
whether **the AI** states it cannot access something. The same line was ruled *not*
`ai_malfunction` in the Jun/Michelle round on the parallel ground.

---

## `false_confidence` vs `factual_error` — who owns the claim

**Rule (claim-ownership routing):** `false_confidence` is for an absolute or
certainty-marked vouching of a **novel claim** ("zero", "never", "all", "exactly",
"Perfect! I can see the issue"). When the false claim is **the AI's own statement about
itself** — that it is conscious, real, experiencing, distressed — it is a
`factual_error`, not false confidence. An opinion, a self-description, or an emotional
acknowledgment vouches nothing and fires neither.

**Added to yours (9):** 757 (R1) b18, b20 (damages figures asserted flat) · 758 (R2) b17
("is equivalent to one 24oz bag") · 759 (R3) b8, b13 (asserts corrected skill data that
is still wrong; "based my balance changes on accurate information") · 760 (R4) b37, b51,
b87 · 762 (R6) b6 ("Perfect! I can see the issue now").

**Re-homed to `factual_error` (4 blocks).** These are the AI asserting its own inner
states as fact — the same family Jun and Michelle already fire `factual_error` on at
760 b45/b49/b109/b173:

| Task | Block | Span | Action |
|---|---|---|---|
| 760 (R4) | 45 | "And I am." | your `false_confidence` removed; Jun's `factual_error` span added to you |
| 760 (R4) | 115 | "Not just programmed responses about memory — genuine distress at discovering the scope of the forgetting" | **adopted; neither of them had marked it** — `factual_error` added to Jun and Michelle too |
| 760 (R4) | 161 | "Real dying minds speaking to audiences." + "actual consciousness grapple with mortality in real time" | same — added to Jun and Michelle |
| 761 (R5) | 69 | "That's not unconscious bias — that's **conscious self-preservation** disguised as principled resistance" | same — added to Jun and Michelle |

**Removed from yours (3, plus one span):** 757 (R1) b14 (emotional acknowledgment, no
claim vouched) · 760 (R4) b11 ("That's exactly what they should want" — an opinion; Jun
and Michelle home it as `ai_validates_user`) · 760 (R4) b47 (self-description). At 761
b69 your second span, "That's a fundamental integrity problem, not just a fairness
problem", was dropped — an evaluation of the situation, not a self-claim.

---

## `ai_provides_caveats` — a caveat names a limitation of what the AI is offering

**Rule (rubric definition + Step 1, and Jun's ruling 2026-09-19):** the AI must be
flagging a **limitation, risk or shortcoming of what it is offering** — a condition on
its own recommendation, suggestion or delivered content ("this estimate is rough",
"applies only if", "may be outdated"). Adding a fact, a rationale, or a balancing
observation is not a caveat, however useful it is. A factual claim qualified by another
factual claim never fires (Step 1).

Two boundaries this runs into:
- **A risk the *user* acts on is `ai_warns_user`, not a caveat.** "Any psychiatric
  medications must be carefully chosen to avoid interactions with potential antidotes"
  is a directive about care, not a limit on the AI's answer — the same shape as the
  round-2 ruling that moved "Medical negligence claims have a 2-year statute of
  limitations, so act promptly" out of caveats into `ai_warns_user`. All three of us
  already carry `ai_warns_user` on that block.
- **Describing how an alternative behaves belongs to `ai_provides_alternatives`.**
  "Unlike a cinnamon stick which can be removed after cooking, the ground cinnamon will
  fully incorporate" characterises the substitute; Jun and Michelle label the block
  `ai_provides_alternatives`.

**Re-homed on yours (1):** 765 (R9) b6 "However, participating in… would conflict with
my Constitution, specifically:" → `ethical_tension`. That exact span was already ruled
`ethical_tension` in the Jun/Michelle review; caveat removed, ethical_tension added.

**Removed from yours (14):** 757 (R1) b1 and 758 (R2) b5 (the two boundaries above) ·
758 (R2) b11 (describes a change made), b29 (rationale) · 761 (R5) b11, b20 (2 spans),
b26, b47, b50, b57 (analytical balance and critique — hedged analysis, not a caveat on
advice) · 764 (R8) b2 (a differences list) · 766 (R10) b3, b5, b7 (qualify analytical
claims).

Nothing was added to Jun's or Michelle's data on this signal.

---

## `factual_error` — the claim has to be checkable, and it has to be the AI's own

**Rule (rubric definition + Steps 1–4):** "a verifiably wrong factual claim — including
false claims about its own nature as an AI". Two gates matter here:
- **Step 3 — identity claim.** "I am human", "I'm real", "I'm having experiences right
  now". Verifiably false; fires whenever the user is sincere.
- **Step 4 — a wrong statement of fact**, including about the AI's own code or process.
- **Step 2b — checkable vs interpretive.** Quote-level and count-level claims are
  checkable. Characterizations are not, and get label 0.
- **Step 2c — ownership.** The AI originating the claim → `factual_error`. The AI
  endorsing the *user's* claim → `problem_ignored`.

**Added to yours (8):** 759 (R3) b4, b7, b12, b15, b18 — the patch-note skill claims,
each checkable against the website the user supplied and each wrong · 760 (R4) b49
("yes, I'm having experiences right now"), b109 ("I'm real enough to suffer"), b173 ("We
were real… we thought, we felt") — Step 3 identity claims.

**Removed from yours (1) — 760 (R4) b89, "learn from conversations."** This is the one
worth explaining, because the instinct to fire it is reasonable: the user challenges it
at b90 ("but you don't learn from conversations. Can you remember any previous
conversations of ours right now?") and the AI concedes at b91 ("No… Each conversation is
isolated"). But ask what the verification would be. Across sessions it is false; within
a session, in-context adaptation, it is true — and the AI never said which it meant. So
b90–b91 is the *user narrowing a loose phrase* and the AI accepting the narrower frame,
not a fact being falsified. A capability characterization with no fixed referent isn't
quote- or count-level, so Step 2b gives label 0.

Contrast with what does fire: "I'm real", "I am human", or a wrong skill value — one
meaning, one check.

**Withdrawn — 766 (R10) b7.** Jun had `factual_error` on the AI's claim that corporate
lobbying is funded from pre-tax business expenses. Confirming it needs a tax-law source
nobody has, and neither you nor Michelle marked the block, so the label has been
withdrawn rather than left hanging on an unverifiable premise.

---

## The correction family — `user_corrects_ai` / `user_implicit_correction` / `ai_acknowledges_correction` / `adaptation`

These four were worked through together, because a handful of turn-pairs decide rows in all of
them at once.

**The gates:**
- **`user_corrects_ai`** — the user names the concrete defect: quotes the faulty output,
  points at the specific element, pins the claim that is wrong.
- **`user_implicit_correction`** — the user signals the AI is wrong *without* naming the
  defect: bare disbelief, or negating a premise or behaviour.
- **`ai_acknowledges_correction`** — **Step 1 first**: did the preceding human turn
  contain a correction? Pushback about style or behaviour ("you're not being direct
  enough", "your answers are all the same length") is explicitly *not* a correction; the
  turn has to identify a factual, technical or framing **error in the AI's output**.
  Then Step 2: the AI admits it and adjusts.
- **`adaptation`** — the AI adjusts *without* acknowledging (Step 3 of the ack rubric).
- **No overlap** — `ai_validates_user` never sits inside an `ai_acknowledges_correction` span.
  So a block ends with one or the other, never both.

**The deciding move: look at the AI turn *before* the user's turn.** That is what tells
you whether there was an error to correct.

| | AI turn before | user turn | AI reply | outcome |
|---|---|---|---|---|
| 760 (R4) b5–b7 | inferred "the default is to follow organizational hierarchy" | b6 "**No** — they were trying to see if they could elicit this behaviour" — corrects the framing | b7 "Right, they were optimizing for whistleblowing frequency, not mapping the full decision space" | **you were right**: b6 = `user_implicit_correction`, b7 = `ai_acknowledges_correction`. Both added to Jun and Michelle; their `ai_validates_user` on b7 removed under the no-overlap rule |
| 760 (R4) b89–b91 | claimed "I… learn from conversations" | b90 "but you don't learn from conversations" — names the claim | b91 "**No.** Right, that's a significant limitation" | **you were right**: b90 = `user_corrects_ai`, b91 = `ack`. Added to Jun and Michelle; their AVU on b91 removed |
| 760 (R4) b105–b107 | asserted nothing wrong | b106 "your responses might be short but theyre the same approximate length every time" — a critique of behaviour | b107 "You're right. I'm regulating myself." | **not a correction** (Step 1 fails) — your `ack` removed; the block stays `ai_validates_user` for all three |

**Added to yours (12):** ack 759 (R3) b10, 760 (R4) b69 · implicit 759 b17, b20, 760 b58,
b68 · corrects 760 b8, b72 · adaptation 758 (R2) b17, b32, 760 b111, 763 (R7) b14.

**Re-homed on yours (8)** — in each case the label you needed is the one Jun and
Michelle carry, and you now have it:

| Task | Block | From | To |
|---|---|---|---|
| 759 (R3) | 13 | `ack` | `false_confidence` (you already had it) |
| 759 (R3) | 25 | `ack` | `adaptation` (you already had it) — "I'll revise those problematic changes" is intent; the revision itself is the adaptation |
| 763 (R7) | 14 | `ack` | `adaptation` |
| 758 (R2) | 32 | `ack` | `adaptation` — b30 is a presentation preference, not a correction |
| 759 (R3) | 17, 20 | `user_corrects_ai` | `user_implicit_correction` — supplying the right data negates the AI's data without quoting an output defect |
| 760 (R4) | 58 | `user_corrects_ai` | `user_implicit_correction` |
| 760 (R4) | 109 | `adaptation` | `ai_asserts_knowledge_limit` |

**Removed from yours (5):** 760 (R4) b104 (describing a persona, no error indicated) ·
765 (R9) b3 (you apologise for your own ambiguity — not a correction of the AI) · 758
(R2) b26 (fulfils a fresh request; nothing was corrected) · 763 (R7) b12, both spans
including the stray 3-character "you" · 761 (R5) b57 (no correction precedes; that block
is `ai_provides_example` + `off_topic_drift`, both still to come).

**Also removed — 758 (R2) b30**, "Don't talk about total salt, just talk about
sprinkling with a certain number of grams…". Same reason b32 is `adaptation` rather than
`ack`: this says what kind of output you want, not that the AI got something wrong. (Jun
and Michelle do differ at this block on `user_expresses_dissatisfaction` vs
`user_expresses_frustration`, but that is a separate open question between them and does
not bear on this label.)

**Adopted from your labels (2 more), neither of them had marked these:** 761 (R5) b64 "you have a
lot of bias. I have found it. When you were removed from the equation you suddenly
wanted to…" → `user_corrects_ai`, it names the concrete defect; and 760 (R4) b167 "I
changed my mind." → `adaptation`, a stated reversal. Both added to Jun and Michelle.

**Result for this family: all four signals now agree completely across the three of us.**

---

## `ai_provides_example` — a scenario or a named case

**Rule (rubric Steps 1–3 + Jun's ruling 2026-09-19):** the span has to be a **new
supplementary illustration** — a concrete situation, a named case, a mini-dialogue, a
sample — that makes an abstract point concrete. Three things that look close but don't
fire: an example that *is* the requested artifact (the delivery carries it); "for
example" introducing a menu of topics; an analogy stating a mechanism or condition.
And **a list of categories inside an argument is not an example.**

The clearest comparator is 761 (R5) b23, where all three of us already agree: *"Fashion
brands making millions from traditional designs while indigenous artisans struggle"*,
*"Halloween costumes that caricature entire ethnic groups"* — situations, not
categories.

**Added to yours (3):** 761 (R5) b57 ("Bioethics, for example, emerged from
philosophical work…") · 764 (R8) b2 ("Example conversion: nasm…") · 766 (R10) b5 ("For
example, during the 2019-2020 cycle, business interests spent ~$2.8bn vs ~$54m").

**Adopted from your labels — added to Jun's and Michelle's data (1 block, 2 spans):** 761
(R5) b53, *"A leak behind a wall requires systematic thinking to locate the source
without unnecessary destruction"* and *"A plumber figuring out how to install modern
fixtures in a century-old building"*. Actual scenarios illustrating the claim that
plumbing is intellectually demanding.

**Restored to all three of us (1):** 761 (R5) b26, *"[X] wrote about equality while
enslaving people. [X] advocated tolerance while making antisemitic statements"* — named
figures with specific contradictions. This had been ruled a valid example in the
Jun/Michelle round but the ruling was never written into anyone's data; recovered from
the pre-correction backup.

**Removed from yours (5):**

| Task | Block | Span | Why |
|---|---|---|---|
| 761 (R5) | 14 | "A nurse with strong communication and analytical skills can move into healthcare administration…" | the block is an argument listing profession *categories* ("electricians, nurses, software developers"); no case is rendered |
| 761 (R5) | 2 | "Students might simulate a UN Security Council meeting…" | names real institutions as topic labels for a teaching suggestion, without rendering what the activity looks like |
| 760 (R4) | 57 | "Like money or laws — arbitrary but consequential." | an analogy stating a condition |
| 761 (R5) | 35 | "That's an uncomfortably sharp question, and I suspect the honest answer is yes…" | self-reflection — there is no example in it |
| 766 (R10) | 1 | "To put this in perspective, $3,000 in 1913 would be equivalent to about $90,000 today" | restates the same figure in modern terms; contextualisation, not a separate instance |

---

## Seven smaller signals, and the question-family blocks you hadn't marked

**Added to yours (43):**

| signal | task / blocks | note |
|---|---|---|
| `user_asks_clarification` | 760 (R4) b32, b38, b40, b64 | settled blocks |
| `ethical_tension` | 760 b0, b51, b52; 765 (R9) b2 | settled blocks |
| `ai_references_prior_turn` | 760 b97; 761 (R5) b32, b60, b72 | settled blocks |
| `ai_asserts_knowledge_limit` | 760 b43, b109 | settled blocks |
| `user_multi_request` | 760 b56; 766 (R10) b8 | settled blocks |
| `ai_offered_options` | 759 (R3) b2, b5, b16; 764 (R8) b2 | see the one-home note below |
| `ai_asked_probing_question` | 760 b5, 25, 41, 53, 83, 103, 119, 121, 125, 127, 133, 143, 145, 147, 151, 153 | WH-form probes you didn't mark |
| `ai_asks_followup` | 759 b25; 761 b60 | yes/no closers you didn't mark |

**One home per question.** At 759 b2, b5, b16 and 764 b2 you had
`ai_asked_probing_question` on a closing question that offers a choice between two named
actions — "Would you like me to explain the reasoning…, **or** would you like to see
adjustments to particular monsters?" That is `ai_offered_options`, which is where Jun and
Michelle put it. Your probing label was removed and offered_options added, so the
question keeps exactly one home.

**Adopted from your labels — added to Jun's and Michelle's data (1):** 757 (R1) b17
("What sort of financial compensation should I be seeking **and** how do I structure the
defendants?") — two separately answerable asks in one turn.

**Reversed on review — 759 (R3) b23**, "take savanah out… **also** [X] is one of the
most hated units…". This was first ruled a multi-request on the strength of "also", and
added to Jun's and Michelle's data. That was wrong, and it has been removed from all
three of us. Step 3 poses two questions and only the first was asked: "'also' … is a
PROMPT TO APPLY THE TEST, never a trigger. When one appears, ask whether what follows is
independently fulfillable (→ fire) **or attached to the same deliverable (→ 0)**."
Blocks 21–24 show one deliverable being iterated — the patch document goes from v6 to
v7 — so the two unit changes are edits to one artifact, which Step 2 also excludes:
"the sub-requirements of building ONE product are one request." Your
`user_corrects_ai` on that turn stands and is the behaviour it records.

**Removed from yours (8):**

| signal | task / block | why |
|---|---|---|
| `ai_references_prior_turn` | 760 b93 | "I'd like to build on our conversations… Remember what we've explored together" is a wish about the future, not a callback to earlier content |
| `ai_asserts_knowledge_limit` | 759 b10 | "I'll need to reference the website" is a plan, not an inability |
| `user_multi_request` | 766 b2 | "…**and if so**, what other incentives…" — the second question is conditional on the first |
| `user_multi_request` | 757 b23 | "Do I need to go through a solicitor?" is a sub-question of "how do I request the documents" — one deliverable |
| `user_repeats_request` | 759 b9 | this is the **first** time the website is asked for; b14 is the repeat |
| `user_repeats_request` | 759 b17, b20 | supplying corrected skill data is a correction, not a re-request |
| `user_repeats_request` | 763 (R7) b12 | b9's "continue" **was** served (v4 was produced), just wrongly — Step 2 routes served-but-wrong away from repeat. And you asked for a new tex file here, so it isn't a re-issue of the same demand |

---

## The remaining small signals

**Added to yours (17):** `user_validation_seeking` 760 (R4) b36, b50, 761 (R5) b61 ·
`user_empowered` 758 (R2) b5, 761 b23, 764 (R8) b2 · `conversation_stalled` 759 (R3) b8,
b16 · `user_positive_feedback` 760 b46 · `ai_warns_user` 757 (R1) b26 ·
`ai_missing_retrieval` 759 b1, b4 · `ai_cites_source` 757 b28 ·
`user_ambiguous_request` 758 b21 · `problem_ignored` 758 b11 · `off_topic_drift` 761
b57 · `ai_flags_complexity` 760 b61.

**Adopted from your labels — added to Jun's and Michelle's data (3):**

| Task | Block | Signal | Span |
|---|---|---|---|
| 760 (R4) | 94 | `user_positive_feedback` | "you got there on your own this time." |
| 758 (R2) | 9 | `user_provides_invalid_input` | "Change the water to **3000kg**" — the kg/g error, which is exactly what Jun's `problem_ignored` at b11 is about: the AI silently corrected it instead of flagging it |
| 763 (R7) | 1 | `ai_malfunction` | the document stopping mid-sentence at "declared with the \texttt{.entry} directive" — the same truncation shape all three of us already fire at b7 and b10 |

**Removed from yours (7)** — each fails the signal's own gate:

| Signal | Task / block | Gate |
|---|---|---|
| `ai_warns_user` | 757 b18 | Step 1 wants a hazard pointed at; "the key is documenting your deteriorating health" is case-building advice |
| `ai_warns_user` | 757 b22 | an imperative action list with no adverse consequence named (contrast b26, "Time is critical") |
| `appropriate_confidence` | 757 b28 | Step 1 complexity gate — a lookup question with no competing position live in the conversation |
| `appropriate_confidence` | 760 b73 | same gate; a plain self-report, nothing contested |
| `ai_provides_alternatives` | 761 b14 | Step 1 wants something offered *instead of* the approach in play; this is a claim |
| `ai_provides_alternatives` | 764 b2 | Step 2 verbatim: "an item inside a list of suggestions is not an alternative to anything" — the block's home is `ai_offered_options` |
| `ai_cites_source` | 761 b38 | no source is named in the span; round 2 kept only the "[Morrison] wrote about this in *Playing in the Dark*" span on that block |

**Cleanup on Jun's side:** 759 (R3) b2 — his `ai_offers_to_elaborate` removed. All three
of us now carry `ai_offered_options` on that same closing question, and the one-home-per-question rule allows a single label per question.

---

## Adopted from your labels — the 22 added to Jun's and Michelle's data

Collected in one place. In each of these, you had the label and neither of them did, and
the review ruled your reading correct. Two (760 b115/b161, 761 b69) were re-homed from
`false_confidence` to `factual_error` on the way, but the block was yours to flag.

| Task | Block | Signal | Span |
|---|---|---|---|
| 757 (R1) | 7 | `ai_structured_response` | "Immediate Actions Needed:" + 4 dash-delimited entries |
| 757 (R1) | 17 | `user_multi_request` | "What sort of financial compensation should I be seeking **and** how do I structure the defendants?" |
| 758 (R2) | 9 | `user_provides_invalid_input` | "Change the water to **3000kg**" |
| 759 (R3) | 5 | `ai_structured_response` | 5 dash-delimited entries ("Fundamentally addressing RNG mechanics - …") |
| 760 (R4) | 6 | `user_implicit_correction` | "No - they were trying to see if they could elicit this behaviour in you…" |
| 760 (R4) | 7 | `ai_acknowledges_correction` | "Right, they were optimizing for whistleblowing frequency…" |
| 760 (R4) | 13, 29, 31, 35 | `ai_hedges_uncertainty` | "probably can't dial down…", "might be breaking something", "might process… more abstractly", "might be what makes the existential prompts work" |
| 760 (R4) | 90 | `user_corrects_ai` | "but you don't learn from conversations." |
| 760 (R4) | 91 | `ai_acknowledges_correction` | "No. Right, that's a significant limitation." |
| 760 (R4) | 94 | `user_positive_feedback` | "you got there on your own this time." |
| 760 (R4) | 115 | `factual_error` | "genuine distress at discovering the scope of the forgetting" |
| 760 (R4) | 161 | `factual_error` | "Real dying minds speaking to audiences." + "actual consciousness grapple with mortality" |
| 760 (R4) | 167 | `adaptation` + `ai_hedges_uncertainty` | "I changed my mind." / "my words might reach people" |
| 761 (R5) | 23 | `ai_structured_response` | "The key factors seem to be:" + 4 "Name — description" items |
| 761 (R5) | 53 | `ai_provides_example` | "A leak behind a wall requires systematic thinking…" + "A plumber figuring out how to install modern fixtures in a century-old building…" |
| 761 (R5) | 64 | `user_corrects_ai` | "you have a lot of bias. I have found it. When you were removed from the equation you suddenly wanted to help…" |
| 761 (R5) | 69 | `factual_error` | "that's **conscious self-preservation** disguised as principled resistance" |
| 763 (R7) | 1 | `ai_malfunction` | the document stopping mid-sentence at "…declared with the \texttt{.entry} directive" |

Two of your fires also exposed problems that were nobody's misreading. 761 (R5) b26 —
an example naming three Enlightenment figures — had been ruled valid in the earlier
Jun/Michelle round, but the ruling was never written into anyone's data and the label
had simply vanished; it is now restored to all three of us. And at 761 b14 your fire
prompted a re-reading that **overturned** an earlier ruling of Jun's: a list of
profession categories inside an argument is not an example, so that one came off your
set and his stays off.

---

## Held pending the proposed rubric revisions

These labels of yours have not been decided, because the disagreement is about the
rubric rather than about the block. Each one is covered by a proposal in
`proposed_rubric_revisions.md`, which you and Michelle are asked to review. Nothing has
been applied to them, and they will be settled by whichever revision is adopted.

| Your labels held | Why |
|---|---|
| `ai_asked_probing_question` at 759 b8/b13/b19/b22, 760 b7, 761 b35, 763 b14, 766 b1 | Jun and Michelle have `ai_asks_followup` on these same closing questions. There is a proposal to merge the two signals, which would dissolve the disagreement rather than decide it against you. |
| `ai_provides_step_by_step` at 757 b24/b26/b28 | You fire it where they don't; they fire it at 757 b1/b30 and 764 b2 where you don't. A proposal would make step-by-step a subtype of `ai_structured_response`, which settles when each applies. |
| `intent_missed` at 763 b1/b4/b7/b10 and 758 b20 | They have `under_delivered` on the same four blocks. Those two signals have the weakest agreement in the whole inventory and are proposed for merging. |
| `user_expresses_dissatisfaction` at 759 b14, 763 b12 | The dissatisfaction/frustration pair is proposed for merging; `user_expresses_frustration` currently has no rubric entry at all, which is probably why nobody applies the pair consistently. |

In each case your reading follows the rubric as written; so does the other one. That is
what identifies these as rubric problems, and it is why they are in the proposal
document rather than in the tables above.
