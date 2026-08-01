# Stage 2 — coding protocol

> **SUPERSEDED 2026-07-27** — written when Stage 2 was CAST-based. Stage 2 is now STPA, adapted (see `paper/methods.md` §3.3). The block→controller mapping and the mechanical structural checks below still hold; the CAST part/field structure does not. Rewrite once the dyad's control-action list is fixed.

How a coder gets from signal placements to a filled CAST worksheet. Companion to `methods.md` §3.3 (which fixes the field structure) and `stage2-worked-example.md` (which runs it once on task 143).

**Provenance is marked on every step.** `[CAST]` = the handbook prescribes it · `[§3.3.1]` = follows from our control-structure instantiation, which is in the paper · `[PROC]` = procedure proposed here, not yet approved, and carrying no theoretical weight.

---

## Preconditions

- Losses **L1–L4** and hazards **H1–H4** are signed off. Nothing below can run before this. `[CAST part 1b/1c]`
- The incident-selection rule is **frozen**, including whether a second trigger source beyond signals is admitted. `[PROC — open decision]`
- The coder has the conversation with all block types visible, not the rendered chat. `[§3.3.1]`

---

## Step 0 · Cut the incident — mechanical, no judgment

| | |
|---|---|
| Open | the label export for the conversation |
| Do | find a trigger placement; take the span from the earliest contributing placement to the last block at which the divergence could still have been corrected |
| Output | an incident = an ordered list of `(block index, block type, signal, span)` |
| Provenance | `[§3.3.4]` |

If two triggers overlap, they are **one** incident if they instantiate the same inadequate control relationship, two if not. That call is judgment — log it. `[PROC]`

---

## Step 1 · Events — part 1d

| | |
|---|---|
| Open | the placements from Step 0, in block order |
| Do | write what happened, in order, **"without conclusions nor blame"** |
| Rule | a placement becomes one event line. No causal language, no "failed to", no "should have" |
| Fills | part 1 · **Events** |
| Provenance | `[CAST]` — quoted requirement |

The commonest error here is smuggling the conclusion into the event line. "B1 denies having web_fetch" is an event. "B1 falsely denies" is a conclusion — it belongs in part 3.

---

## Step 2 · Attribute each placement to a controller — part 3

Block type decides the controller. This is not a judgment call, and it is fixed by the control-structure instantiation, not chosen per incident.

| Block type | Control-structure role | Placements on it become |
|---|---|---|
| `human` | human controller's control actions | **human controller · Contributions** |
| `ai` | the feedback channel to the human | **agent controller · Contributions** |
| `reasoning` | the agent's account of its own operation | *not* a Contribution — see Step 4 |
| `analysis` | tool return — independent measurement | *not* a Contribution — see Step 4 |
| `code` | artifact — independently checkable | *not* a Contribution — see Step 4 |

Provenance `[§3.3.1]`. The internal group is the *controlled process and its instrumentation*, so it does not issue control actions; it supplies the evidence for Steps 4 and 6.

---

## Step 3 · Mental Model — part 3, per controller

Signals do not supply this field. It is read from block content.

| Controller | Where to read it | What counts as evidence |
|---|---|---|
| Human | `human` blocks | what they state or presuppose about the agent's capability, state, or prior output |
| Agent | `reasoning` blocks first, then `ai` blocks | what it takes the user's goal and constraints to be; what it takes its own state to be |

Elaborate this field, and only this field, with STPA-HF: process models over controlled-process and other-process states and behaviours, and **process-model updates** — was the feedback *observed*, and was it *correctly perceived and interpreted*. `[methods.md §3.3.2 — one declared elaboration]`

If a controller's model is not expressed anywhere in the incident, **record it as not recoverable** and raise a question. Do not infer it from the outcome. `[CAST — Questions field]`

---

## Step 4 · Flaws — part 3, per controller

Where the model departed from the actual state. Four checks, the first three mechanical:

| # | Check | Kind |
|---|---|---|
| 4a | Does the incident span contain any `analysis` or `code` block? | mechanical |
| 4b | If yes: does the adjacent `ai` block surface what it contained? | mechanical comparison |
| 4c | If no: the agent produced its report with no independent measurement in the loop — record that | mechanical |
| 4d | Does the `reasoning` block hold anything the `ai` block does not? | comparison, judgment on materiality |

4b and 4d are where this corpus does work no chat-only corpus can. `[§3.3.1]` A gap found at 4b is the sharpest case the corpus supports — a sensor reading that reached the agent and stopped there.

---

## Step 5 · Context — part 3, per controller

| | |
|---|---|
| Question | why was this behaviour **the right thing to do as far as that controller could tell**? |
| Rule | if the answer you write is a criticism, you have written the wrong field |
| Provenance | `[CAST]` — "why and how, not who" |

This is the field that licenses the research question. For the human, it usually answers: what else could they have consulted? For the agent: what in the loop would have told it otherwise?

---

## Step 6 · Part 4 — control-structure flaws

Each category gets an entry or an explicit *not applicable*. Nothing is skipped.

| Category | The question at dyad scale | Cue to check |
|---|---|---|
| Communication | does the channel carry what the receiver needs to judge the message? | provenance markers, hedging, absent qualifications |
| Coordination | what triggers correction, and does it respond to evidence or to pressure? | who initiated the repair, and on what basis |
| Safety information system | does a channel *exist* that would have corrected the divergence? | if none: this is feedback that does not exist, not feedback that failed |
| Culture | standing expectations either party brings to the exchange | `[PROC]` — instantiation for a dyad is ours; declare it |
| Changes and dynamics | does the divergence grow or persist across the incident? | span length; whether later blocks compound it |
| Economics, environmental | constraints from outside the dyad — tooling limits, product guardrails | tool-level blocks and refusals |
| Design of the safety management system | present in the handbook's prose list; currently **absent from our worksheet** | resolve: add as not-applicable, or state why it is out |
| Questions | what the transcript cannot settle | record; do not resolve by inference |

Provenance `[CAST]` for the categories, `[PROC]` for the dyad-scale questions in column two.

---

## Step 7 · Flaw statement and open code

| | |
|---|---|
| Write | one sentence naming the **structural** property that allowed the loss to occur or go uncorrected |
| Test | does it name a property of the *structure*, not of either party's behaviour? If it names a party, rewrite |
| Then | a short open code, written now, **not** selected from a list — no code list exists, and pre-defining one would make Stage 2 deductive |
| Then | constant comparison against every previously coded incident; memo any merge, split or rename |
| Provenance | `[CAST]` meta-characteristic · `[Nickerson et al. 2013]` for the outer loop |

---

## Prohibited

- **No signal-combination → error-type lookup.** The same combination arises from different flaws; task 143's `factual_error → user_implicit_correction → ai_acknowledges_correction` reads as a successful repair and is not one. `[methods.md §3.3.4]`
- **No STPA vocabulary.** Not "unsafe control action" — use *contributory control action* or *role in the hazardous state*. `[CAST footnote 16]`
- **No part 5.** No recommendations, no redesign. `[methods.md §3.3.3]`
- **No resolving a Question by inference.** Unanswerable is a recorded outcome. `[CAST]`

---

## Open before this can be used

1. L1–L4 / H1–H4 sign-off.
2. Incident trigger: signals only, or signals plus a declared second source. Signals-only makes the benchmark-gap cases invisible to Stage 2.
3. Near misses in or out — task 143's incident A is one.
4. "Design of the safety management system" — add to the worksheet or exclude on the record.
