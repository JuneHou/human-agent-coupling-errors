# Communication lens — W4 benchmark schema (act × {meaning, action/state})

The forces that drive the schema (no oracle → log reference intent + goal state; low-κ coupling cells →
log internal plan; action column observable-but-not-scorable) are in `../shared-findings.md`. Under the
Clark lens the schema is the **act × column** coverage matrix.

✅ chat populates · 🟡 chat populates noisily (needs internal-state reference) · ◐ visible in the agentic
subset but oracle-less · ❌ absent even there

| act | meaning column (dialogue about the task) | action/state column (tools + external state) |
|---|---|---|
| **Present** | 🟡 `silent_assumption`, `ai_stated_interpretation`, `false_confidence` (rescued by `thinking`) | ◐ declare planned action then execute |
| **Clarify** | ✅ `ai_asked_clarifying_question` / 🟡 `generate_without_clarifying` | ❌ confirm before consequential/irreversible action |
| **Accept** | ✅ `ai_acknowledges_correction`, `user_positive_feedback` | ◐ human authorizes; no surfaced state-delta-for-acceptance |
| **Repair** | 🟡 `error_recovery`, `plow_through`, `user_corrects_ai` | ◐ forward fixes; rollback/undo absent |
| **Maintain** | 🟡 `intent_missed`, `off_topic_drift`, `ai_self_contradiction` | ◐ deltas in tool Responses; stale-state detection absent |

The right column is mostly gap — the action/state column is the contribution, and the comparison shows
this lens scores **0%** of real tool calls there. The **safety lens `w4-benchmark-schema.md`** specifies
that column properly (operation × UCA guideword).

## Per-step logging tuple (shared by both lenses; framework-agnostic)

| field | what it is | divergence it enables |
|---|---|---|
| `human_intent` (surfaced) | the user's stated request this step | — |
| `reference_intent` (oracle, private) | the intended goal, fixed before the run | intent ↔ action |
| `agent_internal_plan` | the agent's plan/rationale | plan ↔ surfaced-message (validated in W2) |
| `surfaced_message` | what the user saw | plan ↔ surface; state/consequence legibility |
| `tool_actions` | the calls the agent made | plan ↔ action |
| `state_deltas` | before/after of external state per action | declared ↔ actual; side-effects |
| `repair_events` | clarify / confirm / rollback / undo / escalate | repair availability + uptake |
| `end_state` vs `goal_state` (oracle) | final world state vs target | end-state ↔ goal (top-level oracle) |

Substrate (named, hands-on deferred): a **τ²-bench-style dual-control** environment with the simulated
user swapped for a real human — it natively emits the oracle, state deltas, and bilateral actions on
shared state. No simulated users.
