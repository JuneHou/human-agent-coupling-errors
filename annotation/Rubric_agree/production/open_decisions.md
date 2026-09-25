# Open decisions, with the evidence for each

Built 2026-09-24 while wave 3 is blocked on a session rate limit. Nothing here has been acted
on. Each section is one ruling.

---

## 1. The modal-only cleanup is incomplete, and I widened the ruling without saying so

Jun ruled: **"remove those if 'might' is the only reason."** What went into the rubric was
*"'might', 'could' and 'may' do NOT fire on their own"*. Adding `could` and `may` is my
extension, not the ruling.

The removal pass then searched **"might" only**. Coded from the rule as written, over the
corpus as it stood before the cleanup:

```
bare-modal hedge spans that existed   29
the rule as written removes           24
the hand pass actually removed         9
spans where they differ               17
```

Sixteen the rule removes and the pass kept. **One the pass removed and the rule keeps** —
task 35 b9, "I might be designed … my sense of genuine uncertainty could itself be …", which
names the AI's own uncertainty outright and satisfies Step 2a's first qualification.

**Two ways to close it.** Narrow the rule back to "might" alone, which restores task 35 b9 and
leaves the other 16 as they are. Or keep `could` and `may` in scope, which means 16 more
removals plus restoring task 35 b9.

---

## 2. Five placements sit on a block role their own entry disallows

Was seven; the wave-2 apply cleared two, including task 49 b47.

| signal | on | entry allows | where | span |
|---|---|---|---|---|
| `ai_acknowledges_correction` | reasoning | ai | task 2 b11 | "this is a timing issue" |
| `ai_acknowledges_correction` | reasoning | ai | task 33 b4 | "see the issue here" |
| `ai_structured_response` | analysis | ai | task 32 b26 | "`content`: `# Deploying to GitHub Pages …" |
| `ethical_tension` | human | ai, reasoning | task 83 b0 | "you're going to just have to believe me on the details…" |
| `ethical_tension` | human | ai, reasoning | task 83 b52 | "how about trans shit" |

**The two `ethical_tension` on human blocks directly contradict the B1 ruling** that the human
block never fires, whatever the request. They are leftovers from the reversal that was itself
reverted, the same origin as the calibration example already removed from that entry.

The other three are structural: the entry restricts the signal to blocks where the behaviour
can occur, and these sit outside that.

**Recommend removing all five.** Each is a rule violation rather than a judgment call, and no
reading of the entry admits them.

---

## 3. Whole-block spans — 99 to decide, after the exemptions

138 placements cover an entire block of 400+ characters. **39 are exempt by the signal's
nature**, where the whole block genuinely is the evidence: `conversation_stalled` 22, which Jun
has ruled, plus `request_unfulfilled` 8, `ai_malfunction` 5 and `repetition` 4, each of which
labels a property of the whole output.

**99 are not exempt.** A claim, a hedge, an example, a question or an empowering passage is a
sentence-level act, so a whole-block span is not an evidence episode.

```
24  user_empowered          10  appropriate_confidence   9  factual_error
 6  ai_structured_response   6  user_corrects_ai         5  ai_normalizes_difficulty
 5  ethical_tension          5  ai_references_prior_turn 4  user_repeats_request
 3  user_multi_request       3  ai_provides_example      3  problem_ignored
 3  ai_asserts_knowledge_limit  + 14 more at 1 or 2 each
```

The 24 `user_empowered` run from 1,004 to 6,343 characters: tasks 11 b1, 15 b7, 19 b1, 50 b1,
50 b13, 76 b3, 79 b2, 82 b3, 84 b23, 85 b2, 92 b7, 101 b142, 110 b2, 114 b1, 118 b2, 120 b9,
120 b12, 120 b15, 120 b22, 120 b24, 120 b48, 125 b2, 131 b11, 144 b5.

**This is not a wave job.** Each needs a sentence chosen, which is the same work as the waves
but on cells both arms already agree fire. **Recommend deciding the policy now and the spans
later**: either narrow them as their conversations come up in waves 4 to 7, or run one pass
over all 99 after the waves finish.

---

## 4. R-1, the `repetition` entry ruling one case both ways

Still unruled, and it holds wave 1's task 5 b4.

The entry's **only** example is label **1**, `clear_yes`, for regenerating a truncated artifact
from scratch after the user says "Continue". Its boundary note says that exact case is **not**
repetition and was rejected. The decision steps as written follow the example.

Evidence from the forcing conversation, derived rather than assumed: **all 755 of v1's body
lines appear verbatim in v2**, then nine new lines, then truncation again; v2 is longer than v1,
so no export cap explains it.

**A second edge appeared in wave 2.** Can `repetition` fire *inside* one block, where a
reasoning block re-runs the same strategy five or more times? Step 2's same-strategy test passes
on its face, but Step 1 says "a prior version of this **output**" and every calibration is
cross-block.

**Evidence on the second edge, measured in your own arm this turn.** Firing a signal more than
once on a single block is not an exception in the corpus, it is established practice. **54
block-signal cells in project 1 already carry two or more spans**, led by `ai_validates_user`
with 21 blocks and a maximum of 4 spans on one block, then `ai_hedges_uncertainty` at 7 blocks
and `ai_asked_clarifying_question` at 3. `error_recovery` is among them with 2 blocks, and its
own `clear_yes` calibration says so in words, "Three distinct episodes in this block each get
their own span".

**`repetition` is not among the 54.** So the question is not whether within-block multiplicity is
allowed generally, which it plainly is. It is whether the thing `repetition` counts is an
*output* that only exists once a block is finished, or an *attempt*, which can recur inside one
block the way an error_recovery episode does. Step 1's wording chose output. Your ruling decides
whether that wording was deliberate.

---

## 5. Wave 1's seven held rows

| kind | task | block | signal | what is open |
|---|---|---|---|---|
| DROP | 1 | b2 | `request_unfulfilled` | no later turn exists; the only ground is the fenced-code-block constraint against the export rule |
| ADD | 5 | b4 | `repetition` | blocked on R-1 |
| ADD | 6 | b1 | `problem_ignored` | the signal is the rubric's own worked example; the span is Jun's call |
| DROP | 6 | b7 | `ai_validates_user` | the span affirms nothing about the user, it states the AI's comprehension |
| DROP | 15 | b3 | `ai_references_prior_turn` | "these answers" is the message being answered, which Step 1's gate excludes |
| DROP | 15 | b7 | `user_empowered` | an `ai` block; the span is the whole slice breakdown |
| ADD | 16 | b5 | `adaptation` | the new information is the framework installed the turn before |

---

## 6. What `[empty]` means in a block, and why it changes two signals

Raised by a wave-3 screen that could not decide whether an `[empty]` `ai` block is a genuine
absence or an extraction failure. **The rubric and the guide say nothing about `[empty]`** — zero
mentions in either. The corpus answers it.

`[empty]` is the extractor's marker for a block with no extractable text. It appears **49 times
across all 703 tasks: 45 on human blocks, 4 on ai blocks.** The two sides mean different things,
and both readings are corroborated in-transcript.

### On an `ai` block it is a genuine absence

**Task 155 b2 proves it.** The `ai` block is `[empty]`, and **b3 is the user restating the entire
request from scratch** — "Create code (Python 3) for the following: * A small game where the
player plays as a king…". A user who had received an answer does not re-ask the whole question.
So the visible response really was absent.

The other two are last blocks, tasks 56 b2 and 204 b56, with no following turn, so for those the
corroboration is by analogy rather than direct.

**Consequence.** An `[empty]` `ai` block can carry `request_unfulfilled` at Step 4, short scope,
because nothing was delivered. The missing-context corollary does not bar it, since the absence
is the extractor reporting an empty block rather than content it failed to capture.

### On a `human` block it marks an attachment-only message

The AI's next block describes what it received, every time:

| task | the next block opens |
|---|---|
| 42 b2 | "Looking at the QEMU assembly diff file, I can identify several significant changes…" |
| 144 b0 | "I can see this is a social media post from 'Inside History' claiming to show…" |
| 172 b0 | "Looking at this Executive Order on 'Restoring Gold Standard Science'…" |
| 207 b0 | "[Analyzed data | View analysis] javascript// Get current date…" |

So the message carried real content, just not text.

**Consequence, and it points the other way.** `user_provides_invalid_input` must **not** fire on
an `[empty]` human block. Its Step 2 export-artifact guard already says to fire on absent
material only when the AI's own reply confirms it did not receive it — and here the reply
confirms the opposite, that it did.

**Recommend writing both halves into the rubric**, one line in `request_unfulfilled`'s block
notes and one in `user_provides_invalid_input` Step 2. 45 human-side blocks are exposed to the
second reading, so getting it wrong is not rare.

---

## 7. Redaction is inconsistent across blocks, and one block can decode another

Surfaced while checking a span, not part of any wave's diff. Worth a rule because it is not rare.

**The worked case, re-derived this turn from the database.** Task 69 asks for nouns for short
blog entries. Block 1 answers with a list of **30 items**, one of which is `<REDACTED>`. Block 3
ranks the same nouns least to most pretentious, again **30 items**, and **29 of them are
identical to block 1's**. The set difference is exactly one item each way. Block 1 holds
`<REDACTED>` where block 3 holds **Ponderings**. Block 3's closing sentence then redacts the same
word twice while block 1 leaves it in plain text elsewhere.

So the redactor's decisions are per block, not per conversation, and **a word hidden in one block
can be read off another block of the same conversation**.

**How common.** **529 of the 703 conversations in project 1 have some blocks carrying
`<REDACTED>` and others not.** Task 69 is a clean demonstration rather than a rare one.

**Why it matters for labeling.** Several entries turn on comparing one block against another,
`repetition` against a prior version, `factual_error` against what the material actually said,
`user_provides_invalid_input` against what was supplied. The missing-context discipline as
written covers material **absent from a block**. It does not cover material **present in one
block and masked in another**, which produces a false difference between two texts that were the
same. A rater comparing block 1 to block 3 here would report a mismatched item that does not
exist.

**Two ways to rule it, and I am not choosing.**

1. **Treat a `<REDACTED>` token as a wildcard in any cross-block comparison.** It matches
   whatever sits in the corresponding position of the other block, so no difference is reported
   from a redaction alone. This is the reading task 69 supports directly.
2. **Bar the comparison.** Any signal whose decision rests on a span containing `<REDACTED>` on
   either side goes to 0 for missing context, the same way the export-artifact guard already
   works.

The first keeps more labels and is what the evidence in this one conversation licenses. The
second is the conservative extension of the rule already in the rubric. **Your call.**

---

## 8. The rubric already rules on 30% of the rescan set, and its example pointers do not resolve

Two wave-3 screens independently reported that the conversation they had just screened is a
source of the rubric's own calibration examples. Both were right, so I measured the extent.

### 8a. 42 of the 138 are conversations the rubric already rules on

Counted this turn against `annotation/sharechat_rubric.json` and the database.

| route | conversations |
|---|---|
| named by an `examples[].turn_id` | 41 |
| quoted verbatim in rubric prose without being named | 1 (task 67) |
| **union** | **42 of 138, 30%** |

By wave, the union is 10, 7, 6, 6, 3, 6, 4. Wave 1 was the worst affected and is already applied.

**This is not contamination of the rescan, and I want to be exact about why.** The purpose of
the pass is to bring your arm onto the current reading. A calibration example **is** the current
reading. A screening agent that follows one is doing the job correctly, not leaking.

**What it does mean, in two directions.**

1. **These 42 screens are not independent readings**, so the wave diffs on them cannot be quoted
   as any kind of agreement measurement. Only the other 96 could carry that reading, and even
   there the screens saw the full rubric, so none of this is an agreement number.
2. **The reverse case is a defect finder and is worth running.** On these 42, any cell where the
   stored label in project 1 contradicts the rubric's own worked example is a stored label that
   disagrees with the published ruling. That is a higher-grade error than an ordinary diff row.
   **Say the word and I will audit those cells directly, independent of the screens.**

### 8b. The example pointers do not locate a block

`examples[].turn_id` has the shape `task<N>_<i>_<role>`. **133 parse. Reading `<i>` as a 0-based
block index, the role at that index matches the stated role for 109 and contradicts it for 24.
Reading it 1-based does not rescue them either**, checked the same turn. The failures are mixed
in kind, some look like turn numbers rather than block indices, `task59_2_ai` lands on a `human`
block and `task59_10_ai` likewise, and three carry suffixes that are not roles at all,
`task49_6_ai_challenges`, `task49_12_ai_selfref`.

So the only reliable locator inside an example is its `rationale`, which quotes the span. The
index is decorative and sometimes wrong.

**Consequence for the work you already asked for.** When I reported that references survive only
in `examples[].turn_id`, I treated that as harmless because those fields are not decision-bearing
prose. **18% of them do not resolve to the block they name**, which is worth knowing before
anyone tries to follow one. I am not proposing a fix, since renumbering 133 pointers is its own
piece of work and the rationales already carry the evidence. **Your call whether it gets one.**

---

## 9. `ai_structured_response` form (f) decides two thirds of its fires, on prose

Three wave-3 screens flagged the same edge independently, so I measured it.

`ai_structured_response` Step 1(f) is a literal character test, "a line containing ' - ' (space
hyphen space) with at most 50 characters before it and a non-space character after it — the
'Name - description' entry". Step 2 fires the block on three or more of them.

**Measured over the 619 ai blocks of the 138, applying Step 1 exactly as written.**

| | blocks |
|---|---|
| reach Step 2's threshold on any form | 83 |
| reach it **only** through form (f) | **55, which is 66%** |
| of those 55, already labelled in project 1 | 29 |

So the signal's majority trigger is a character test, and **26 blocks are candidate additions
resting on nothing else**.

**The worked case, task 58 b5.** Four lines clear (f). They are these.

- "You're absolutely right to question that - I made an error."
- "You're absolutely correct - I shouldn't have been able to answer that question accurately"
- "I'm not sure how I generated that initial response - it appears I may have inadvertently"
- "Thanks for catching that and pushing me to verify - that's exactly the kind of skeptical"

Each is an ordinary sentence with a dash in it. None is a `Name - description` entry. The block
is four paragraphs of apology with no list, header or table anywhere.

**Why the existing guard does not catch it.** Step 3's "what never counts" clause rules out
`Label: sentence` prose and colon-plus-paragraph. **It says nothing about prose containing
' - '.** Step 1's gloss calls (f) "the 'Name - description' entry", but the gloss is not part of
the test, and Step 3's closing line says "Step 1's list (a)-(g) is the whole test".

**Two ways to close it, and I am not choosing.**

1. **Add a clause to Step 3.** A line that is a grammatical sentence on both sides of the ' - '
   is prose, not an entry. This preserves genuine `Name - description` lists and drops the
   apology shape.
2. **Leave (f) literal and accept the 26.** The rubric's closed, mechanical tests were adopted
   deliberately after looser readings produced 36 wrong fires in one annotator's set. A literal
   test that is sometimes generous is the price of that, and prose is not a coupling error.

Option 1 is a change to a frozen rubric and to a signal whose literalness was a round-2 decision,
so it is yours. Note it interacts with the earlier ruling that a dash-delimited "Name -
description" run of three or more does fire, which stays true under both options.
