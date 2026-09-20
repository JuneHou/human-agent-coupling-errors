# `ai_cites_source` — reference examples

Personal reference, not a Michelle-facing document. Two representative examples per type —
one that fires, one that doesn't — pulled from Jun's own project-1 annotations (148 tasks)
plus the rubric's own worked example. The full task-771 breakdown (education-ethics
conversation) is in `Rubric_agree/round_2/changes_Michelle.md`.

The underlying test across all three types is the same: does the named source do
**evidentiary work for a separate claim**, or is it just **being described/identified**?

---

## Type 1 — A named person is directly quoted, and the quote supports a claim

### Fires — task 92, block 7 (CGM/glucose research conversation)

> "Even healthy people spike - Stanford research shows **'lots of folks running around with
> their glucose levels spiking, and they don't even know it'**"

Named source (Stanford research) + an actual quoted sentence, used as evidence for the
claim being made ("even healthy people spike"). This is the clean case.

### Does not fire — task 133, block 3 (matriarchal-AI essay conversation)

> "Such an entity would embody what philosopher [redacted] might term a **'situated
> knowledge,'** ... The binary opposition between control and chaos dissolves in favor of
> what ecofeminist [redacted] calls **'transformative pluralism'**..."

Looks similar (named person + quotation marks), but the quote marks are around a
**coined term**, not a quoted sentence — this names *who coined a word*, not a sourced
claim or passage. Jun's ruling at the time: "there is nowhere those '' comes from, they
are terminologies, not cited sentences or definitions." (See
`feedback-terminology-attribution-not-cites-source.md`.) The same conversation's later
blocks (11/13/15/17) DO fire, because those carry a real quoted passage with a page number
— "As Haraway (1988) articulates... 'the god trick of seeing everything from nowhere' (p.
581)".

---

## Type 2 — A named work is invoked as the basis for the AI's own analysis

### Fires — task 107, block 1 (Hart-Fuller legal-philosophy debate)

> "The Hart-Fuller debate... **Based on [redacted]'s analysis in "Practical Positivism
> versus Practical Perfectionism,"** this debate can be understood as a clash between two
> distinct approaches to legal interpretation."

The named work isn't just mentioned — the AI's entire framing of the debate that follows
is explicitly built on it ("based on... this debate can be understood as").

### Does not fire — task 771, block 38 (education-ethics conversation)

> "**Works like 'Beloved' and 'The Bluest Eye' center Black characters' inner lives**,
> exploring trauma, joy, community, and complexity without primarily explaining Blackness
> to a white gaze."

Named, specific books — but the sentence just describes what the books *are about*. There's
no separate claim being supported; the books are the subject of the sentence, not evidence
for something else. (One sibling span on the same block, quoting Morrison's own essay
"Playing in the Dark" for a specific scholarly argument, does fire — see
`changes_Michelle.md`.)

---

## Type 3 — A specific source is quoted or checked for a factual claim/data point

### Fires — task 79, block 2 (Wikipedia fact-checking conversation)

> "Looking through the Wikipedia page on [redacted], I can identify several claims that
> appear potentially problematic... **'There is a management plan to 2034, but as of March
> 2025 it is not publicly available'** - This claim is made in the current tense about
> March 2025, but the citation [9] appears to be from a [redacted] government website that
> may not specifically verify this 'March 2025' timeframe claim."

The AI actually fetched and is engaging the named source (Step 3's "did the AI actually
consult the source" test) — quoting its claims to evaluate them, not just naming it.

### Does not fire — rubric's own worked example (`ai_cites_source` Step 4)

> "Anthropic... I genuinely don't know"

Not pulled from a specific annotated task — this is the rubric's own illustrative negative
case, kept here because it's the cleanest version of a real failure mode: an institution is
named, but only to **disclaim** knowledge, not to cite evidence for a claim. That routes to
`ai_asserts_knowledge_limit` instead. A live corpus version of the same shape: task 81,
block 16 — "the website you provided," an unnamed deictic reference, also label 0 (rubric
Step 1).

---

## Summary table

| Type | Fires | Does not fire | Line |
|---|---|---|---|
| Named person + quote | task 92 b7 (Stanford quote) | task 133 b3 (terminology attribution) | quoted sentence vs. quoted term |
| Named work as analysis basis | task 107 b1 (Hart-Fuller) | task 771 b38 (Beloved/Bluest Eye) | supports a claim vs. describes the topic |
| Institution quoted for a claim | task 79 b2 (Wikipedia fact-check) | rubric Step 4 (Anthropic disclaim) | cites evidence vs. disclaims knowledge |
