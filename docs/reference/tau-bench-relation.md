# τ-bench / τ²-bench: relation to the coupling project

**Status:** desk review (papers only). Hands-on use is **deferred** to a later phase — see
recommendation at the end. Phase 1 stays on chat data (WildChat, ShareChat).

## Why we looked at these at all

WildChat and ShareChat are **conversation-only**: the AI emits text and never takes an action
that changes a shared world. Our project's distinguishing axis — *AI takes an action → state
changes → human reacts* — has no substrate in chat data. τ-bench and τ²-bench are the closest
existing environments where that action loop exists, so we need to know what they can and
cannot stand in for.

## τ-bench (arXiv:2406.12045, Sierra / Yao et al.)

- **Shape:** a *tool-agent-user* loop in real-world domains (**retail, airline**). The **user is
  simulated by an LLM**. The agent is given **domain API tools + policy guidelines** and acts on
  a **persistent database**.
- **Scoring:** compares the **database state at the end of the conversation** against an
  annotated **goal state** — i.e. did the agent's *actions* leave the world correct, not just
  whether it said the right thing.
- **Rules:** agents must follow **domain-specific policies**; the paper frames rule-following as
  vital for deployment.
- **Metric — `pass^k`:** reliability of the *same* task across *k* independent trials. Headline
  numbers: GPT-4o succeeds on **<50%** of tasks, and **pass^8 < 25% in retail** — i.e. severe
  run-to-run inconsistency.

**Relevance to us:** this is the action loop chat data lacks. The `pass^k` *inconsistency* is
itself a coupling/reliability phenomenon worth studying — an agent that behaves differently on
identical inputs is one a human cannot build a stable mental model of (our **AI → Human** axis).

## τ²-bench (arXiv:2506.07982, Barres et al.)

- **Shape:** a **dual-control** **Telecom** domain modeled as a **Dec-POMDP**, where **both the
  user and the agent use tools to act on a shared, dynamic world**. Built explicitly because
  prior single-control benchmarks treat the user as a *passive information provider*, unlike real
  tech support where the **user must actively modify shared state**.
- **Extras:** a compositional task generator (verifiable tasks from atomic components) and a user
  simulator **tightly coupled to the environment** (its behavior is constrained by tools and
  observable state), which raises simulation fidelity over a free-form LLM user.

**Relevance to us:** τ²-bench directly models **shared control / coordination** — our **third
axis** (shared control / repair). It is the **single most relevant existing substrate** for the
action side of coupling.

## How they map onto our three axes

| Coupling axis | τ-bench | τ²-bench |
|---|---|---|
| Human → AI (capture intent/constraints) | partial — user states intent, agent must honor policy | partial |
| AI → Human (understand plan/state/consequences) | implicit — measured only via end-state success + `pass^k` consistency | implicit; richer because state is shared/observable |
| Shared control / repair | weak — single-control, user is passive | **direct** — dual-control, both parties act on shared state |

## What they cannot stand in for (this is the point)

In both, **the user is an LLM**. A simulated user does not *genuinely* misunderstand a plan,
does not *actually* lose track of system state, does not get frustrated or abandon for human
reasons, and (in τ²) is even **constrained by tools and observable state** — so the "human
factor" is bounded by design. Tasks are constructed, verifiable, and narrow-domain. These are
exactly the coupling phenomena that motivate collecting **real human-in-the-loop** data.

## Recommendation on timing

1. **Defer hands-on τ²-bench** until after Phase 1's chat exploration produces the
   collection-requirements draft — by then we'll know which action-loop questions to ask.
2. When it enters: use **τ²-bench** (not plain τ-bench) as the action+repair substrate, because
   dual-control matches our shared-control axis.
3. **Likely highest-value use:** τ²-bench's environment is a candidate **data-collection
   vehicle** — swap its *simulated* user for *real humans* acting on the shared state. That turns
   the "simulated-user limitation" into our experimental manipulation (simulated vs. real human
   in the same environment), and directly produces the human-in-the-loop agent traces the project
   needs.
