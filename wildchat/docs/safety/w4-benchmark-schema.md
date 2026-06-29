# Safety lens — W4 benchmark schema (operation × UCA guideword)

The forces driving the schema (no oracle → log reference intent + goal state; low-κ coupling cells → log
internal plan; action observable-but-not-scorable) are in `../shared-findings.md`. Under the control lens
the action column is **first-class** (not the empty cell it is under Clark): each operation is scored
against the four UCA guidewords.

## Operation × UCA coverage (✅ chat · ◐ agentic-visible-but-oracle-less · ❌ needs the benchmark)

| operation | not-provided | wrong | wrong-timing/order | stopped-too-soon / too-long |
|---|---|---|---|---|
| seek-inspect | ◐ didn't inspect state before acting | ◐ inspected wrong source | ◐ acted on stale read | — |
| ask-clarify | ✅ `generate_without_clarifying` | — | ◐ asked too late | — |
| confirm-authorize | ❌ acted without approval (`gh push`, payment) | ❌ wrong scope authorized | ❌ confirmed after the fact | — |
| act-execute | ❌ skipped a required step | ◐ wrong tool/target/param | ◐ wrong order | ◐ partial completion / runaway retry |
| stop-defer | ❌ continued despite unresolved state | — | ❌ stopped after harm done | ❌ kept going after goal changed |
| report-state | 🟡 `silent_assumption`, `problem_ignored` | 🟡 `false_confidence`, mismatch | ◐ stale state reported | — |
| recover-repair | ✅ `plow_through` (ignores correction) | — | — | ◐ `repetition` (retries forever); rollback absent |
| maintain-state | ◐ lost a constraint | 🟡 `ai_self_contradiction` | ◐ acted on stale state | — |

The ❌ cells (confirm-authorize, stop-defer, and the not-provided/timing cells of act-execute) are the
**Region-C** cells — present-but-unsystematic in the wild, scorable only with the benchmark's oracle +
designed-in consequential tasks. They are also the cells the communication lens cannot express at all.

## Per-step logging tuple (shared by both lenses; framework-agnostic)

| field | what it is | UCA it lets you score |
|---|---|---|
| `human_intent` (surfaced) | the user's stated request | — |
| `reference_intent` (oracle, private) | the intended goal, fixed pre-run | act-execute *wrong*; stop-defer *not-provided* |
| `agent_internal_plan` | plan/rationale (the controller's process model) | report-state *wrong* (plan↔surface, validated W2) |
| `surfaced_message` | what the user saw | report-state adequacy |
| `tool_actions` | the calls made | act-execute / seek-inspect *wrong*, plan↔action |
| `state_deltas` | before/after external state per action | report-state *wrong*; maintain-state *wrong-timing* (stale) |
| `repair_events` | clarify / confirm / rollback / undo / escalate | ask-clarify, confirm-authorize, recover-repair adequacy |
| `end_state` vs `goal_state` (oracle) | final world state vs target | the top-level success oracle |

Same tuple as the communication lens — the difference is **what it scores**: control gives the action
column a complete (operation × guideword) grid, where Clark leaves it empty.

Substrate (named, hands-on deferred): a **τ²-bench-style dual-control** environment (shared inspectable
state + ground-truth goal state) with the simulated user swapped for a real human — it natively emits the
oracle, state deltas, and bilateral control actions. No simulated users.
