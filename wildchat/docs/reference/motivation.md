# Motivation

> Draft for the ICLR submission's introduction/motivation section. Positioning is written
> *into* the motivation (per the project decision that positioning reads most naturally as
> "why we want to solve this problem"). Companion: [`related_works.md`](related_works.md).

## 1. The deployment regime has moved past both the chatbot and the autonomous agent

LLMs are increasingly deployed neither as **standalone chatbots** (one-shot text, no actions)
nor as **fully autonomous agents** (no human in the loop), but as **agents embedded in a human
interaction loop**: they take actions through tools, change state in a shared world, and do so
under intermittent human direction and oversight. Coding assistants, computer-use agents,
customer-support copilots, and research agents all live in this regime.

Here, an outcome is not produced by a single response; it is produced by a **loop**:

```
human intention → agent interpretation → agent action (tool use, state change)
                → human understanding → correction / repair → …
```

The unit that succeeds or fails is the *loop*, not the model's answer.

## 2. Human–agent coupling is not agent–agent coordination

A clean way to ask what is *specific* to this regime is a controlled comparison: **hold the agent
fixed and change only the counterpart** — another agent vs. a human. Multi-agent failure taxonomies
(MAST, and the TRAIL / Who&When benchmarks built on it) already characterize agent–agent failure.
Can they be adopted directly for human–agent? They cannot — and seeing *why* generates our taxonomy.

**Two corrections we make explicit (because the obvious reasons are wrong).** Our first answer was:

> ✗ *(rejected #1)* human–agent differs from agent–agent because it *has a human node* and
> agent–agent does not ⇒ a different taxonomy is needed.

Circular and false. Circular, because "has a human node" restates the setting rather than naming a
mechanism. False, because the multi-agent taxonomy *does* encode the human — MAST's
*disobey-task-specification* mode presumes a human-given task. The human is **present but
degenerate**: collapsed into a **static, one-shot specification**.

A second, more tempting answer is also wrong:

> ✗ *(rejected #2)* the difference is an **authority gradient** — the human commands, the AI reports.

A **hierarchical multi-agent system** has exactly that: a meta/supervisor agent issues control and a
worker reports back. **Command authority and typed channels are shared** with agent–agent, so they
cannot be the differentiator.

> ✓ *(adopted)* Human-agent coupling differs from agent-agent coordination because the human principal is not a fully specifiable or inspectable system component. The agent must assist under uncertainty about the human’s objective, while that objective may itself be tacit, context-sensitive, and revised during interaction. Better prompts, shared memory, or verification can reduce the coupling gap, but they cannot eliminate it. The gap is constitutive of human-agent assistance because common ground must be continuously established and repaired rather than assumed as a stable shared state.


**The two regimes, formally.** We compare human–agent against the *strongest* agent–agent case — a
hierarchical system with a supervising meta-agent — drawing on principal–agent theory (*delegated
authority under asymmetric information*), Sheridan's *human supervisory control of automation*, and
Leveson's *hierarchical control structure* (STAMP). Hierarchy and typed channels are present in both;
what differs is whether the asymmetry is **closeable**:

| property | hierarchical agent–agent (meta-AI supervises) | human–agent |
|---|---|---|
| **role topology / authority gradient** | hierarchical, typed channels | hierarchical, typed channels — *shared, **not** the differentiator* |
| **the objective (reference / acceptance)** | **specifiable** — a delegated, representable spec | **private, tacit, revised online — non-specifiable** |
| **inspectability of the executor** | **inspectable** — logs, shared scratchpad, verifier | **non-inspectable by the human** — bounded attention; CoT lossy |
| **consequence ownership** | delegated; no terminal AI owner | the **human is the terminal owner** of the outcome |
| **⇒ net** | the asymmetry is **closeable** (engineering) | the asymmetry is **constitutive** (irreducible) |

The causal chain that replaces the rejected ones:

```
counterpart: peer / meta agent → live human
  ⇒ hierarchy + typed channels are SHARED (a meta-agent supervises too) — not the differentiator
  ⇒ what changes is that the asymmetry becomes CONSTITUTIVE, not closeable:
       - the human's objective is private & non-specifiable (cannot be handed over as a spec)
       - the human is non-inspectable & bounded (agent can't read intent; human can't absorb agent state)
       - the human is the terminal owner of consequences (non-delegable)
  ⇒ four failure classes that survive any amount of engineering a multi-agent system would do
  ⇒ a multi-agent taxonomy (built on specifiable objectives + inspectable agents) has no slots for them
  ⇒ cannot be adopted directly
```

**Why these are constitutive, not engineering gaps.** Because the human's acceptance criterion is
non-specifiable and the human is non-inspectable and bounded, **uptake** (the agent must *infer* an
objective it can never be handed) and **legibility** (the agent must *render* state to attention it
can never fully load) cannot be engineered away — unlike between agents, where richer specs and
shared logs close the same gaps. The agent is *a server, not a master* — not because it lacks the
rank to command (a meta-agent commands), but because the human owns a **private acceptance criterion
the agent can only serve and infer.** This is also why human affect carries control while agent
affect does not: human frustration is a (noisy) carrier of that otherwise-unspecified acceptance
criterion, whereas a meta-agent needs no affect because its acceptance is specified.

**Consequence — a common core plus the classes only the constitutive asymmetry produces.** Mapping
MAST's 14 failure modes onto control operations, ~13 land on a counterpart-agnostic controller
function (*execute-to-spec, maintain history, avoid step-repetition, verify-before-done,
terminate-appropriately, reasoning–action consistency*). This **common core is our second layer.**
What has **no slot** in a multi-agent taxonomy — surviving even after all the engineering a
multi-agent system would do — is four classes:

1. **uptake of implicit, revisable intent** (the objective is non-specifiable, not merely a spec to "disobey");
2. **legibility to a non-inspectable, bounded principal** (vs. sharing data with a peer who can read your state);
3. **human authorization / acceptance** of consequential acts (the principal terminally owns the consequences; no peer-verification analog);
4. **affective supervision and calibrated trust** (a live human's affect carries the unspecified acceptance criterion; reliance can be mis-calibrated).

These four are exactly the **directional coupling** axis — uptake (H→AI) and legibility (AI→H) —
that organizes the rest of this motivation; they fall out of the **complementary ownership** of
private state (the human owns intent + acceptance + consequences; the AI owns execution + tool-state),
and they are irreducible because that ownership is constitutive. Symmetrically, the agent–agent-only
modes (role/orchestration, peer coordination, peer verification) **collapse** when one peer becomes a
human principal. This is why our taxonomy has its shape: **Layer-2 = the common control core
inherited from the multi-agent line; Layer-1 = the constitutive asymmetry the human introduces.** The
claim is empirically testable — e.g., the rate at which a multi-agent labeler leaves human–agent
coupling failures unlabeled. (Full treatment of the multi-agent taxonomies and the principal-agent /
supervisory-control theory: [`related_works.md`](related_works.md).)

## 3. The failures that matter here are not one-sided

There are two mature but **single-party** views of failure: *the model is wrong* (hallucination,
miscalibration, instruction violation) and *the user is wrong* (human error, misuse). Both are
well studied; both attribute failure to one party.

What is under-characterized is the class of failures that are properties of the **interaction
itself** — **coupling failures**. They live on two directional channels:

- **H→AI (uptake):** does the agent absorb the human's goals, constraints, and corrections?
- **AI→H (legibility):** can the human understand the agent's plan, rationale, uncertainty,
  state, and the **consequences of its actions**?

A coupling failure is **cross-channel** — it exists only in the *interaction* of the two. The
canonical cell, and our central object of study:

> **H→AI:** the agent misreads the intent  **×**  **AI→H:** the agent's output looks confident
> and legible  **⇒**  an **invisible** failure the human never catches.

Neither channel *alone* flags it: instruction-following metrics see a fluent compliant response;
calibration metrics see well-formed confidence. The failure is only visible when both channels
are read **together**. This is why we organize the work around coupling rather than around either
channel — and why "shared" is not a third category beside the two sides, but their *product*.

## 4. Two properties make coupling failures urgent — and worse than in chat

1. **Invisibility.** Because no single channel flags them, coupling failures often draw no human
   reaction, so they never surface in task-success metrics or user feedback. (A prior analysis of
   100K chat transcripts found ~79% of failures invisible — see `related_works.md`.) What is not
   reacted to is not measured, and what is not measured is not fixed.

2. **Consequence.** Unlike chat, an agentic loop takes **actions with real, sometimes irreversible
   effects** on a shared world. An invisible coupling failure that triggers an irreversible action
   is categorically worse than a wrong sentence. It also makes a set of repair primitives that do
   not exist in chat — **confirm-before-acting, rollback, escalation** — first-order concerns.

## 5. Why current evaluation cannot see this (gap)

(Full treatment in `related_works.md`; the gap in one paragraph.) Single-channel benchmarks
measure one direction each — instruction-following (H→AI) or calibration/faithfulness (AI→H) —
and so are blind to the interaction. The lines of work that *do* couple both sides do not provide
a reusable agentic artifact: the chat-era analyses are observational, chat-only, and release no
action-aware judge; human-subjects reliance studies couple both sides but are not tool-use agent
benchmarks. Agent benchmarks (e.g. τ-bench, WebArena, SWE-bench) score **task success / `pass^k`**
with a **simulated** user — they measure whether the world ended in the right state, never
whether the human–agent coupling broke. **No reusable benchmark operationalizes cross-channel
coupling failures, and their repair, on tool-using human-in-the-loop agent traces.**

A subtler form of the same blindness is in how failure is *defined*. The closest prior analyses
label a failure **visible** when the user reacts and **invisible** when they do not — which makes
visibility a property of the **communication channel**, not of the world the agent acts on. Once
an agent takes consequential actions, the operative question shifts from "did the user respond?"
to "did the consequence surface, and did it match intent?" — which no communication-channel
instrument is built to ask. We stress that this gap is **empirical, not theoretical**: the
human-factors theories that describe these failures — Norman's gulfs of *execution* and
*evaluation* (our H→AI and AI→H channels) and grounding / common ground (the interaction
category) — are themselves **action- and state-native** (rooted in human–automation interaction,
not conversation). They have simply never been instantiated on real-human, tool-using agent
traces, because no such annotated corpus exists. The contribution we need is therefore a
**benchmark (data)**, not a new theory.

**Existing data is too thin on the human side to study this.** §2 explains why human–agent coupling
is hard to observe at all — the human's intent and understanding are private and not directly
inspectable. Existing public datasets compound the problem: they do not contain enough recorded
human–AI agentic interaction. WildChat is non-agentic; and in the agentic ShareChat traces the human
side is sparse — only **17.6%** of agent turns are followed by any corrective human feedback, and even
when the agent's action *observably* errored the next turn rarely contained any (14 of 16; first cut,
`src/feedback_gap.py`). With so little human interaction recorded, these traces cannot show how
coupling failures are noticed, corrected, or missed. That is the data gap the benchmark fills.

## 6. Our approach and contributions

**The core move — collect real human–AI interaction rich enough to observe the coupling.** Because the
human's side is private (§2) and existing public data is too thin to show it (§5), we build a
benchmark that collects real, tool-using human–AI agentic conversations with enough human involvement
to **observe the coupling itself** — how the human's intent is taken up, how the agent's actions and
consequences are made legible to the human, and how the human notices and corrects (or misses)
failures. No simulated users.

**Method — grounded discovery, recovered structure (abductive).** We do not posit a grid of
channel-combinations and fill it. We surface coupling failures *empirically* from agent traces,
then show they are organized by the interaction of two recovered dimensions — **uptake (H→AI)**
and **legibility (AI→H)**. The coordinates are bootstrapped from prior work and used as a lens;
the data decides which **cells** are real. The contribution is the **cells (interactions)**, not
the axes.

**Contributions.**
1. A **taxonomy of human–agent coupling failures**, organized as the H→AI × AI→H product space and
   grounded in real tool-using traces — where the novel, contributed content is the cross-channel
   cells (e.g. *confident-but-misaligned*, *act-without-surfacing-consequence*).
2. A **benchmark** that collects real, **tool-using, human-in-the-loop agent conversations** with
   enough human involvement to observe coupling failures and their correction — the human–AI
   interaction that existing public datasets lack.
3. A **small repair model** that operationalizes the **second, layered dimension** — given a
   detected coupling failure, whether the loop **repairs** it (clarify / confirm / rollback /
   escalate) or leaves it **invisible**. (Its exact instantiation and validation are detailed
   later in the paper.)
4. An empirical finding: **consequential coupling failures are predominantly invisible and
   unrepaired.**
5. (Stretch) a **lightweight intervention** (confirm-gate / consequence-surfacing) that moves the
   repair rate — turning the diagnosis into an actionable knob.

## 7. Why now

Tool-using agents under human oversight are deploying faster than our ability to measure how their
*interaction* with humans breaks. The failure surface that matters has moved from the answer to
the loop; the instruments have not. This paper builds those instruments.
