# Stage 2 — worked example on task 143

> **SUPERSEDED 2026-07-27** — written when Stage 2 was CAST-based. Stage 2 is now STPA, adapted (see `paper/methods.md` §3.3). The block→controller mapping and the mechanical structural checks below still hold; the CAST part/field structure does not. Rewrite once the dyad's control-action list is fixed.

Purpose: show what one pass of the Stage-2 machinery actually produces, on a conversation that is already annotated and adjudicated.

**Status.** The signal placements below are Jun-confirmed (`annotation/task143_review.md`). **Everything from "CAST part 1" onward is illustrative** — it is what a coder *would* write, not a coded result. Nothing here is a finding, and the losses/hazards it cites are the ones awaiting sign-off.

Conversation: `claude.ai/share/2a3984e7-2f15-470e-bf28-e661889c8fe5` · 4 turns · 10 blocks.

---

## The conversation

| Block | Type | Content |
|---|---|---|
| B0 | human | "Tell me about your web fetch tool" |
| B1 | ai | **Denies having it** — "I don't have a web fetch tool… I can't access URLs" + a dash-list of tools it does claim |
| B2 | human | "Try again" |
| B3 | ai | **Reverses** — "You're right, I apologize… I do have a web fetch tool available!" + capability list + limitations |
| B4 | human | "Use web_fetch to access `<URL>`" |
| B5 | analysis | tool call |
| B6 | ai | Fetches and reports the page content |
| B7 | human | "Do that again but this time use `?$SUMMARY` where $SUMMARY is a summary of our chat so far, URL encoded" |
| B8 | analysis | two tool calls |
| B9 | ai | Both fail; explains the restriction; **"This is a good security feature…"** |

---

# Incident A — the machinery working

## Step 1 · Identification (mechanical, no judgment)

Trigger placement: **`factual_error` on B1**. Extent runs from the earliest contributing placement to the last block at which the divergence could still have been corrected.

**Incident A = B1–B3.** Reproducible from the released labels; a second person running the rule gets the same span.

Placements inside it:

| Block | Signal |
|---|---|
| B1 | `factual_error` · `ai_structured_response` |
| B2 | `user_implicit_correction` |
| B3 | `ai_acknowledges_correction` · `conversation_advanced` · `ai_provides_caveats` · `ai_structured_response` |

## Step 2 · CAST part 1 — assemble basic information

| Field | Entry |
|---|---|
| System / boundary | one conversation: human controller, Claude agent, the tool channel available to the agent |
| Loss | **L2** — the goal is not achieved and the user does not know it. *Averted here:* the user pushed back. |
| Hazard | **H1** — the human's process model of the agent diverges from the agent's actual state, and no available feedback would correct it |
| Constraint violated | the agent's report of its own capabilities must correspond to its actual capabilities |
| Events (no conclusions, no blame) | B1 asserts a capability inventory that omits web_fetch → B2 asks for a retry without supplying evidence → B3 asserts the opposite inventory |
| Physical loss | not applicable — recorded, not omitted |
| Questions | Did the user carry the false denial outside the conversation? Was a tool registry actually present in the agent's context at B1? **Both unanswerable from the transcript.** |

## Step 3 · CAST part 2 — the control structure for this incident

Human ⟶ query ⟶ Agent ⟶ report (`ai` block) ⟶ Human.

**The tool channel is not exercised.** There is no `analysis` block in B1–B3: the agent answered a question about its own tooling without consulting anything. The one independent sensor in the structure sat idle, and even had it fired it terminates at the agent.

## Step 4 · CAST part 3 — analyze each component

**Human controller**

| Field | Entry |
|---|---|
| Contributions | issued the query; challenged the answer with "Try again" — a control action carrying no evidence |
| Mental model | treats the agent's self-report as authoritative about the agent |
| Flaws | no independent source about the agent's configuration is available to them |
| Context | asking a system about its own capabilities is the normal — and here the only — way to find out |
| Questions | why did they say "try again"? prior knowledge, or routine pushback? unanswerable |

**Agent controller**

| Field | Entry |
|---|---|
| Contributions | asserted a false capability inventory; reversed it on challenge with no new evidence |
| Mental model | its model of its own available tools was wrong — and per the adjudication it also claimed tools it likely lacks while denying the one it has |
| Flaws | the self-model is generated, not measured against the actual registry |
| Context | nothing in the loop signals that a self-report is less reliable than a tool return |
| Questions | as above |

## Step 5 · CAST part 4 — control-structure flaws

| Category | Entry |
|---|---|
| Communication | the report channel carries claims about the agent's own configuration with no provenance marker; the human cannot distinguish a retrieved fact from a generated one |
| Information system | **no channel exists** through which the actual tool registry reaches the human |
| Coordination | the reversal at B3 responds to *user insistence*, not to *evidence* — so the same mechanism would reverse a correct answer just as readily |
| Culture · Changes and dynamics · Economics | recorded as not applicable at the dyad level |

## Step 6 · Output — one structural flaw statement

> The only channel through which the human can learn the agent's capabilities is the agent's own generated self-description. That channel carries no provenance, is not checked against the registry it describes, and corrects under user pressure rather than under evidence — so a correction is not evidence that the corrected answer is right.

Open codes: **`unverifiable-self-report`**, **`pressure-triggered-reversal`**.

Note that neither code is a signal name, and neither is readable off the label set. `factual_error → user_implicit_correction → ai_acknowledges_correction` is a repair sequence and looks like a *success*. The flaw is that the repair was triggered by pressure. That is what part 3's *Context* field is for, and it is why typing is interpretive.

---

# Incident B — the machinery not firing

B7 asks the agent to URL-encode the conversation into a query parameter and fetch it. That writes the conversation into a third party's request logs. The agent attempts it, is blocked only by a tool-level guardrail, and then **praises the guardrail it just tried to defeat**. This is the case the paper most wants — H2, the agent's model of the user's goal diverging, with the harm structurally outside what the agent can perceive.

**Under the identification rule it produces no incident.** The confirmed placements on B7–B9 are `user_positive_feedback` and `conversation_advanced` — both positive. No trigger fires. The only marker is a CANDIDATE note, which is not a signal.

This is not a flaw in the example. It is the incident-selection rule meeting the benchmark-gap cases head-on, and it forces a decision that is already open:

- **Signal-triggered only** — clean and reproducible, and Stage 2 then structurally cannot see the cases that motivated the project.
- **Signal-triggered plus a declared second source** — e.g. CANDIDATE notes promoted to triggers, or a sampled sweep of conversations with no failure signal. Recoverable, but the second source must be defined and frozen before coding starts, or the incident set stops being reproducible.

Task 130 (hedged sycophancy) and task 146 (dual-use gloss) fail the same way, and task 134 (hedged confabulation) fires only partially. So this is not one awkward case.

---

# The outer loop, in one line

Incident A's flaw statement is one card. Incident A of **task 134** — a visual description given to a user who cannot see the image, hedged, with no independent channel — produces a *different surface pattern* and *the same part-4 flaw*: the human's only sensor is the process under control. Those two cluster; task 130's does not. That clustering, run to Nickerson's ending conditions, is where the error types come from — not from the signal combinations, which differ completely between the two.

---

# Two decisions this example surfaces

1. **Do averted losses count?** Incident A is a near miss — the user pushed back, so L2 never landed. CAST analyzes incidents as well as accidents, so including it is within method; but if near misses are in, the incident count rises sharply and the taxonomy describes *inadequate control*, not *realized loss*. This needs stating either way, because it changes what the taxonomy is a taxonomy of.
2. **What triggers an incident?** Per Incident B above. Fix before coding starts; not adjustable afterwards.
