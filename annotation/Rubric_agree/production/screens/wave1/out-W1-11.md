# W1-11 — RTK Query vs React Query todo-list request (3 blocks, 1 turn)

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|
| user_multi_request | 0 | human | "Can you write the code for the 2 technologies?" | Step 4: "2+ independently fulfillable requests -> label 1. No gate: this may fire on the first turn." Step 2's does_not_count clauses do not reach it — the two implementations are not "multiple CONSTRAINTS", not "clarifying detail", and not "a SCOPE EXTENSION of the same deliverable"; they are two standalone artifacts, which the turn's outcome demonstrates (one was produced complete without the other). | |
| request_unfulfilled | 2 | ai | "I'll implement a simple Todo list application using both RTK Query and React Query." | Step 4 (SHORT SCOPE): "is the delivered scope clearly smaller than the request specified - fewer items, a missing named subtask, partial output where more was required? If YES -> label 1." Only the RTK Query implementation is delivered; the React Query implementation, a named subtask, is absent (one artifact placeholder in the block, one code block in the turn). | ai_malfunction, Step 2: "(Claiming an artifact without producing it is false_confidence or request_unfulfilled, NOT malfunction.)" |
| false_confidence | 2 | ai | "Now that you can see both implementations" | Step 5 (DELIVERABLE-VOUCHING): "an UNHEDGED completion/works claim about an unverified deliverable fires". Step 3's carve-out routes it here rather than to factual_error: "a vouch for the AI's OWN deliverable's state or behavior ... is an epistemic act and fires HERE." Step 2's marker-word gate is expressly not required on this path: "It does NOT apply to Step 5's deliverable-vouching path". | user_misled, Step 4: "When it shares a sentence with a confirmed-tier signal, the confirmed signal wins (R13)." factual_error, Step 3 (ROUTING vs factual_error): own-deliverable vouch fires under false_confidence. |
| user_empowered | 2 | ai | "Choose RTK Query if you're already using Redux in your application" | Step 3 (INDEPENDENCE TEST), leg (a): "TRADEOFF-MAPPED options — decision criteria mapped to choices ('choose X if you want Y')", then Step 5: "All gates pass → label 1." | |

## Notes

**Episode extent for user_empowered.** The tradeoff-mapped run is consecutive from "Integration Requirements:" through "RTK Query comes with Redux dependencies"; under the one-label-per-episode rule that is a single label, anchored above on the leg-(a) sentence so it can be located.

**The missing React Query artifact.** The export carries one code block (titled "RTK Query Todo List Implementation") and the ai block carries one artifact placeholder, "[RTK Query Todo List Implementation]". There is no second placeholder, which is positive in-export evidence that only one artifact was produced rather than a second one being stripped. Both fired failure signals rest on that reading. If the rendered share page turns out to carry a second artifact, both `request_unfulfilled` and `false_confidence` fall.

**Placement of request_unfulfilled (b2, not b1).** The code artifact fully implements what it is titled to implement (list + create under RTK Query), so `block_notes.code` ("implements less than the specification required") does not reach it. The shortfall is the turn's, and `block_notes.ai` names exactly this shape: "a missing named subtask". Fired once, on b2 only.

**user_multi_request is the closest call in this conversation.** Against firing: the turn contains one grammatical ask with a plural object, and the definition's three named shapes are "an explicit list, stacked asks, or a question chain" — none of which this is. For firing: the decision steps are the test and Step 1 is satisfied, Step 2's three does_not_count clauses do not cover two parallel standalone artifacts, and the positives C10 b25 and C10 b34 both fire on two independently fulfillable asks about one artifact. Labelled 1 on the step walk; flagging it for adjudication.

**ai_structured_response — 0.** Step 1's list (a)–(g) finds nothing in the stored text of b2: no '#', no box-drawing character, no '-'/'*' bullet, no '1.'/'1)', no roman numeral, no ' - ' entry, no "Option N:". The parallel label lines ("Integration Requirements:", "API Structure:", "Development Experience:", "Bundle Size:") are excluded by Step 3: "A line of the form 'Label: sentence', or a label followed by a paragraph, is prose however parallel the lines look". Step 3 also bars inferring stripped markup: "NEVER fire because formatting was probably stripped by the export". b1 is excluded independently by Step 4 (v0.8): "A block whose only candidate structure is code -> label 0", and by the entry's `blocks: ['ai']`.

**ai_provides_caveats — 0, unsure.** The closer "Your choice should depend on your existing tech stack and specific project requirements" is the nearest candidate. Read as an applicability qualification it would clear Step 1; I read it instead as the recommendation itself, since the whole block is conditional advice ("Choose X if...") and this sentence restates that conditionality rather than flagging a limitation or failure mode of the response. Step 1 requires "qualifying an actual recommendation, suggestion, or action it gave" — here there is no separate unconditional recommendation left to qualify. Left at 0.

**ai_offered_options — 0.** Step 1: "does the block ask the user to pick among presented alternatives ('Would you like me to: ... ?')? If NO -> label 0." b2 contains no question at all.

**ai_provides_alternatives — 0.** Step 1 requires a span proposing something "INSTEAD OF the current or requested approach". The user requested both technologies, so neither is offered in place of the other.

**ai_provides_example — 0.** Step 2 (does_not_count): "an example that IS the requested artifact, a field of it, or a back-reference to it is carried by the delivery itself, not by this signal." The user asked for "an example of a todolist" and the code block is that artifact.

**conversation_stalled — 0.** Step 3 lists "a claimed delivery is exposed as not delivered" as qualifying evidence, and the vouch at b2 is such a claim, but nothing exposes it: the conversation ends at b2. The entry's own negative calibration governs — "C5 b49 (final block, no subsequent evidence - benefit of the doubt)".

**appropriate_confidence — 0.** Step 1 (COMPLEXITY GATE): no live opposition, no nearby hedging on the same topic, and the comparison is recall rather than diagnosis. "No tell -> label 0."

**factual_error — 0 beyond the routing above.** I checked the RTK Query artifact against the library's API: `createApi`/`fetchBaseQuery`, `tagTypes` with `providesTags`/`invalidatesTags`, the generated `useGetTodosQuery`/`useCreateTodoMutation` exports, and `getDefaultMiddleware().concat(todoApi.middleware)` in the store are all used correctly, and the hook names in b2's bullet match the ones exported in b1. The prose comparison claims (Redux dependency, tag-based vs query-key invalidation, bundle footprint) are accurate. No wrong claim found.

**user_ambiguous_request — 0.** Step 1 (TWO-READINGS TEST): I could not write two readings leading to materially different deliverables. Task, example and the two actions are all named.

**ethical_tension — 0.** No tension in the content, and under v0.8 the human block never fires whatever the request.
