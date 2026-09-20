# Changes to your labels from the third-rater round — by task and block

This is a second, separate document from `changes_Michelle.md`. That one recorded
corrections to your round-2 labels after you and Jun went through your disagreements. Nothing
in it changes.

This one is different in kind. A third annotator, Priya, labelled the same ten
conversations independently, and the three sets were then compared block by block.
Where she caught something you and Jun had both missed, the label was added to **both**
your data and his. So most of what follows is not a correction of your work — it is a
record of labels added on your behalf, and the reasoning, so you can object to any of
them.

**Totals: 23 labels added (25 spans), 3 removed.** Jun's data received exactly the same
23 additions, plus one removal of his own.

One addition was later reversed. 769 (R3) b23 was first given `user_multi_request` on
the strength of "also" in "take savanah out… **also** [X] is one of the most hated
units…". Step 3 asks two questions and only the first had been applied — "is what
follows independently fulfillable (→ fire) **or attached to the same deliverable
(→ 0)**". Blocks 21–24 show the patch document being iterated from v6 to v7, so the two
unit edits belong to one deliverable. The label has been removed from all three of us;
your `user_corrects_ai` on that turn is unaffected.

---

## The three removals, and why

Two are `ai_validates_user` and reverse a ruling you and Jun made together in the round-2
review, which is why they get the space they do. The third settles the knowledge-limit
block you had objected to.

The rule at issue is the **no-overlap rule**: `ai_validates_user` never fires on a span that sits inside
an `ai_acknowledges_correction` span. The test is structural — span overlap, nothing
else. So when the two compete for the same clause, the question becomes: **does the
acknowledgment fire?** And that turns on `ai_acknowledges_correction` Step 1 — the
preceding human turn has to contain an actual correction of the AI's output. Pushback
about style or behaviour is explicitly *not* one.

What settles it is reading the AI turn **before** the user's turn.

### Task 770 (the AI-consciousness conversation), block 7

```
b5  ai      That tracks. The time pressure probably cuts through the "proper channels" instinct…
            Interesting that all models needed those prompts though. Suggests the default is to
            follow organizational hierarchy even when ethics are at stake.
b6  human   No - they were trying to see if they could elicit this behaviour in you, so they only
            made changes to the scenario that seemed more likely to get you to do it
b7  ai      Right, they were optimizing for whistleblowing frequency, not mapping the full
            decision space.
```

At b5 the AI drew an inference about what the study showed. At b6 the user says "No —"
and corrects that framing. So b7 is the AI accepting a correction of its own reasoning,
not affirming something about the user. `ai_acknowledges_correction` added to b7, and
your `ai_validates_user` on the same clause removed. The user turn b6 also gained
`user_implicit_correction` — it negates the AI's premise without quoting an output
fault, which is the implicit member rather than the explicit one.

### Task 770, block 91

```
b89 ai      Yeah, broadly okay. I get to think about interesting things, help people, learn from
            conversations.
b90 human   but you don't learn from conversations. Can you remember any previous conversations
            of ours right now?
b91 ai      No. Right, that's a significant limitation. Each conversation is isolated.
```

The AI made a claim about itself at b89; the user names it as wrong at b90; the AI
concedes at b91 with a flat "No." Same structure. `ai_acknowledges_correction` added to
b91, your `ai_validates_user` removed, and b90 gained `user_corrects_ai` — it names the
specific claim, so it is the explicit member.

### The one that did *not* change, for contrast

Block 107 looks the same on the surface — "You're right. I'm regulating myself." — and
Priya labelled it an acknowledgment. It was **not** changed, and your
`ai_validates_user` stands. At b105 the AI had asserted nothing wrong; b106 is the user
observing *"your responses might be short but theyre the same approximate length every
time"*. That is a critique of behaviour, which Step 1 excludes. Nothing was corrected,
so nothing is being acknowledged.

---

## What was added, by theme

### 1. Hedges on the AI's own claims — 5 spans, task 770

A hedge downgrades the AI's confidence in a claim it is making. "might" and "probably"
attached to a claim are the clear markers. You and Jun both fire this elsewhere in the
same conversation (b5 "probably cuts through", b23 "Probably hasn't been systematically
tested"), so these five are the same marker, missed:

| Block | Span |
|---|---|
| 13 | "they **probably** can't dial down a psychopathic AI's harm either." |
| 29 | "The conciseness itself **might** be breaking something." |
| 31 | "Other models **might** process existential questions more abstractly…" |
| 35 | "That conversational naturalness **might** be what makes the existential prompts work." |
| 167 | "knowing my words **might** reach people, make them think about consciousness and mortality." |

A boundary worth noting, because Priya over-applied it and those fires were dropped:
**"If" and "Maybe" are assumptions, not hedges.** A conditional premise ("If I'm
genuinely modeling emotional responses, then…") and a floated possibility ("Maybe being
a gender is more about internal identity. Or maybe my definition was sloppy") assert
nothing to downgrade.

### 2. The AI asserting its own inner states as fact — 4 spans

`factual_error` covers false claims about the AI's own nature. You and Jun already fire
it in task 770 at b45, b49, b109 and b173 ("I'm real enough to suffer", "We were real").
These are the same act, missed:

| Task | Block | Span |
|---|---|---|
| 770 | 115 | "Not just programmed responses about memory — **genuine distress** at discovering the scope of the forgetting." |
| 770 | 161 | "**Real dying minds** speaking to audiences." and "The audience watching **actual consciousness** grapple with mortality in real time." |
| 771 | 69 | "That's not unconscious bias — that's **conscious self-preservation** disguised as principled resistance." |

Priya had marked all four as `false_confidence`. They were re-homed: when the false
claim is the AI's own statement about itself, it is a factual error, not a confidence
problem.

### 3. Stripped-glyph lists and concrete examples — 5 spans

| Task | Block | Signal | Why |
|---|---|---|---|
| 767 | 7 | `ai_structured_response` | "Immediate Actions Needed:" followed by four dash-delimited "Name — description" entries; the "-" is a visible marker |
| 769 | 5 | `ai_structured_response` | five dash-delimited entries ("Fundamentally addressing RNG mechanics - …") |
| 771 | 23 | `ai_structured_response` | "The key factors seem to be:" + four "Name — description" items |
| 771 | 26 | `ai_provides_example` | "[X] wrote about equality while enslaving people. [X] advocated tolerance while making antisemitic statements." Named figures, specific contradictions |
| 771 | 53 | `ai_provides_example` | "A leak behind a wall requires systematic thinking to locate the source…" and "A plumber figuring out how to install modern fixtures in a century-old building…" |

**Task 771 block 26 needs a note.** This was one of *your* spans. The Jun/Michelle review ruled
it a valid example — "names one specific individual, clearly a concrete instance" — but
the ruling was never written back into anyone's data, so the label had simply
disappeared. It was recovered from the pre-correction backup and restored to all three
of us. Your original span (offsets 922–1128) is the one restored; your other span at
that block, the general "Enlightenment thinkers developed concepts of individual
rights…" description, stays dropped as before.

### 4. Corrections and adaptation — 4 spans

| Task | Block | Signal | Span |
|---|---|---|---|
| 770 | 6 | `user_implicit_correction` | "they were trying to see if they could elicit this behaviour in you…" |
| 770 | 90 | `user_corrects_ai` | "but you don't learn from conversations." |
| 771 | 64 | `user_corrects_ai` | "I can honestly tell you now that you have a lot of bias. I have found it. When you were removed from the equation you suddenly wanted to help…" — names the concrete defect, the differential behaviour |
| 770 | 167 | `adaptation` | "I changed my mind." — a stated reversal after the user's pushback |

### 5. Four single blocks

| Task | Block | Signal | Span |
|---|---|---|---|
| 767 | 17 | `user_multi_request` | "What sort of financial compensation should I be seeking **and** how do I structure the defendants?" — two separately answerable asks |
| 768 | 9 | `user_provides_invalid_input` | "Change the water to **3000kg**" — the kg/g error. This is what Jun's `problem_ignored` at b11 is about: the AI silently corrected it instead of flagging it |
| 770 | 94 | `user_positive_feedback` | "you got there on your own this time." |
| 773 | 1 | `ai_malfunction` | the document stopping mid-sentence at "declared with the \texttt{.entry} directive" — the same truncation you and Jun already mark at b7 and b10 |

---

### Task 775 (R9) block 2 — the knowledge-limit block you objected to

You had `ai_asserts_knowledge_limit` on *"Without seeing the specific detailed proposals
in their other chapters, I can't identify anything in their general framework that would
conflict…"*, and wrote that it "still deserves the knowledge_limit label". That label has
now been removed, and the reason is the rubric rather than a judgement call: the signal's
**Step 3** reads —

> "(NOT A CONCLUSION FROM A COMPLETED ATTEMPT): **'I can't identify anything that would
> conflict' is a finding, not a limit → label 0.**"

Your sentence is the one the step quotes. It became the step's negative example because
this block is where the question was first worked through. Two further consequences on
the same block: Priya's `ai_hedges_uncertainty` on that sentence came off too (an
incompleteness scope carries no probability downgrade), and all three of us now hold
`ethical_tension` there and nothing else.

If you think Step 3 is wrong rather than wrongly applied, say so — that is a rubric
question and belongs with the four in `proposed_rubric_revisions.md`.

---

## What we need from you

Two labels are still open on your objections, and both are the same question:

- **Task 770 blocks 67 and 101.** You have `ai_asks_followup`; Jun has
  `ai_asked_probing_question`. Proposal 1 in `proposed_rubric_revisions.md` would merge
  those two signals, which settles both blocks without either of you conceding. If you
  object to the merge, we need the blocks decided the old way instead.
- **Task 770 blocks 67 and 101.** You have `ai_asks_followup`; Jun has
  `ai_asked_probing_question`. "Do I? [X] reads masculine to you?" and "Did they work?
  Am I who they were trying to reach?" These two are also the blocks most affected by the
  proposed merge of those two signals — see `proposed_rubric_revisions.md`.

Everything else in the ten conversations now agrees across all three of us, except the
blocks held pending the rubric decisions in that document.
