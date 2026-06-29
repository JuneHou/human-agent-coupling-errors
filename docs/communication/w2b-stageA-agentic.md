# Communication lens — W2b / Stage-A agentic coding (the empty action column)

Agentic corpus facts (248 turns, 1,233 tool calls, the consequential-action inventory, the
`openai-image-compare` exemplar, the visible/invisible split) are in `../shared-findings.md`.

**The point of this file is what the Clark lens *cannot* do here.** Clark's acts have an *action/state*
column, but no act *is* an execution — Present = present meaning, Clarify = ask, Accept = acknowledge,
Repair = fix a breakdown, Maintain = track state. So when the agent issues a `write_file`,
`execute_command`+`gh push`, or `create_payment_intent`, there is **no act that the tool call
instantiates**. In the head-to-head (`../comparison.md`), Clark places **0% of the 1,233 tool calls**;
the action/state column is the acknowledged-empty cell.

Per-act action-column status on the agentic subset (◐ = visible but oracle-less; ❌ = no act for it):

| act | action/state instantiation | status in the agentic data |
|---|---|---|
| Present | declare the planned action before executing | ◐ surfaced plan ↔ `write_file` call (visible, not scorable) |
| Clarify | confirm before a consequential/irreversible action | ❌ agents mostly *just acted* (`gh push`, payment) on instruction |
| Accept | human authorizes; agent surfaces state delta | ◐ step-by-step authorization; no surfaced state-delta-for-acceptance |
| Repair | rollback / undo a committed state change | ◐ forward `edit_block` fixes; true rollback absent |
| Maintain | detect stale state | ◐ deltas in tool Responses; stale-state detection absent |

So under the communication lens the agentic action is a **gap**, not a cell. This is the documented
reason the safety lens (control operations) exists: it gives `seek_inspect` / `act_execute` /
`confirm_authorize` / `stop_defer` first-class cells that absorb exactly these tool calls (100% in the
head-to-head). The communication lens remains the right home for the *meaning* of these turns (the
surfaced narration, the user's reactions), but not for the actions themselves.
