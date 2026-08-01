# Questions for the advisor — Stage-2 open coding

Stage 2 is STPA, adapted: enumerate the control actions available to the human and to the agent, cross each with STPA's four conditions to find unsafe control actions, then open-code the explanations into coupling-error types. Only unsafe control actions witnessed in the corpus are reported.

1. **Sign-off on what counts as a coupling error.** Proposed: a control action is an error when it leaves one party's understanding out of step with what is actually the case and nothing later in the conversation corrects it — in two directions, agent-to-human and human-to-agent. Without this "unsafe control action" has no referent. It is ours, not the theory's, and everything downstream traces to it.

2. **What are the control actions of the human and the agent?** The whole enumeration rests on this list — provisionally, on the human side: issue request, constrain, accept, correct, terminate; on the agent side: answer, call tool, report result, refuse, ask. Is this the right cut?

3. **When do we stop, and how much evidence makes a type?** Nickerson's ending conditions test whether the taxonomy is well built, not whether we have coded enough. Do we add a saturation rule — *k* consecutive occurrences with no new code? The current bar for a type is occurrences from more than one conversation, and codes seen once have no home.

4. **Are these the right reflexive questions?** Proposed: what was each party attempting to control · what feedback was available at each decision point · where could control or intervention be exercised · what state was asymmetrically visible · what relevant feature falls outside these questions. Recorded per occurrence.

5. **Confirm coders are blind to the prediction.** We predict agent-to-human divergence is repaired less often than human-to-agent; the coder assigns the direction and also sees whether repair happened.
