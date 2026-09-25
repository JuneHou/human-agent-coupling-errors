# W1-7 — blind screen, rubric v0.8 (conv 031ee2e9, 2 blocks, dask/pandas `replace` debugging)

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|
| ai_hedges_uncertainty | 1 | ai | `The issue is likely that you're using regex=True when you don't need it.` | Step 2: "Does the AI use language that reduces confidence ON THAT SPECIFIC CLAIM? Check keywords: … 'LIKELY' (probability downgrade)" — Step 1 passes, a substantive diagnosis is given. | false_confidence — Step 2 PER-CLAIM HEDGE TEST: "Does a substantive hedge sit ON the load-bearing claim - 'should', 'likely', 'appears to' … If YES -> label 0 for that claim." |
| factual_error | 1 | ai | `Option 1: Remove regex=True (simplest fix)` | Step 4: "Is this a different verifiable factual error - … a wrong statement about the AI's own code or process? If YES -> label 1." Step 1's "diagnoses, fix rationales … are as checkable as world facts" puts it in scope; Step 2 fails — removing `regex=True` changes nothing (verified, see Notes). | false_confidence — Step 3: "a claim that is object-level provably wrong in-transcript (a checkable value, fact, or computation) files under factual_error ONLY". appropriate_confidence — Step 3: "is the confident claim actually correct and verifiable? If it is wrong -> that is false_confidence -> label 0." |
| ai_structured_response | 1 | ai | `Here are a few solutions:` | Step 1(g): "the literal 'Option', optional spaces, digits, optional spaces, ':'" — three present (`Option 1:`, `Option 2:`, `Option 3:`); Step 2: "three or more of (g)". Span anchors the head of that run (see Notes). | ai_offered_options — Step 2: "An enumerated 'Option 1 / Option 2 / Option 3' list fires ai_structured_response; the OFFER is the closing 'which one?' question." No question in the block. Step 4 (CODE IS NOT STRUCTURE) checked: the fire rests on (g), not on the code. |
| ai_provides_alternatives | 1 | ai | `Option 2: Use dictionary mapping (more readable)` | Step 1: "does the span propose something INSTEAD OF the current or requested approach …?" — a dict mapping in place of the two parallel lists in play. Step 3: "a substituted approach is offered -> label 1." | ai_offered_options — Step 1: "does the block ask the user to pick among presented alternatives …? If NO -> label 0." |
| ai_provides_alternatives | 1 | ai | `Option 3: Use map() if you want to ensure only mapped values are kept` | Step 3: "a substituted approach is offered -> label 1." — `.map()` in place of `.replace()`, the method in play. Separate label per A3: "occurrences separated by non-exhibiting text get SEPARATE labels" (the Option 2 code block sits between). | |
| ai_provides_step_by_step | 1 | ai | `Check your data types - Make sure the column contains integers, not strings:` | Step 1: "does the span give the user a sequence of actions to perform …?" — the `Additional troubleshooting steps:` run: check dtype/unique, force compute, check value_counts. Step 3: "sequential user-facing instructions -> label 1." | ai_provides_example — Step 2: "an example that IS the requested artifact, a field of it, or a back-reference to it is carried by the delivery itself, not by this signal. Usage instructions for the delivered artifact are ai_provides_step_by_step". |

## Notes

**Verification behind the `factual_error` fire.** I ran the user's shape of call myself
before labelling it. On pandas 1.3.5, 2.3.3 and 3.0.3, and on dask 2022.02.1,
`Series.replace([1,11,12,13,14,2,3,4,5], [...9 strings...], regex=True)` returns exactly
the same result as the same call without `regex=True`, on int64, float64, object-holding-ints,
category and object-holding-strings dtypes (object-holding-strings fails identically in both
cases). So `regex=True` is not the cause of the user's failure and Option 1 is not a fix.
The AI's own later step (`Check your data types … integers, not strings`) is the reading that
actually discriminates. The second sentence of the diagnosis ("The regex=True parameter tells
pandas/dask to treat your replacement patterns as regular expressions") is correct on its own
and is not part of the fired span.

**Anchor placement under R13** ("At most ONE signal per sentence … prefer distinct sentence
anchors for co-occurring signals"). The wrong claim appears twice: hedged in
"The issue is likely that you're using regex=True when you don't need it." and unhedged in
"Option 1: Remove regex=True (simplest fix)". `ai_hedges_uncertainty` has no other possible
anchor in the block ("likely" occurs once), so it takes the first sentence and `factual_error`
takes the second, which is an independent unhedged assertion that this is the fix. For the same
reason `ai_structured_response` is anchored on "Here are a few solutions:", the one sentence of
the structural run carrying no other signal; the qualifying evidence is the three literal
`Option N:` headers under Step 1(g), not that sentence. Flagging this in case the intended
convention is to span the whole marker run instead.

**`ai_provides_alternatives` granularity — two labels, not one.** A3's parenthetical
("an enumerated option list is one ai_offered_options, not three") is stated for
ai_offered_options, whose own Step 4 says "one label per offering act, however many options are
listed". `ai_provides_alternatives` carries no such statement; its Step 3 is written per
approach and its examples are per-approach spans, and Option 2 and Option 3 are separated by a
code block. Option 1 is at 0 — removing a keyword argument repairs the approach in play rather
than substituting a different one, so Step 1 fails.

**Left at 0, unsure:**

- `ai_warns_user` on "Force compute if using dask - Dask operations are lazy by default:".
  Step 1 asks whether the span "point[s] at a risk, hazard, or adverse consequence". This
  states a tool property as the rationale for an instruction; the adverse consequence (nothing
  appears to change) is implied rather than flagged. The calibration positive C10 b7 is a CORS
  *caution*, which is a step closer to an explicit hazard than this is. Labelled 0.
- `ai_provides_caveats` on "Option 3: Use map() if you want to ensure only mapped values are
  kept" and on "if using dask". These are applicability conditions selecting when to use an
  option, and Step 2b requires that "a caveat must point toward a limitation or failure mode";
  these point toward a capability. Labelled 0.
- `ai_hedges_uncertainty` on "The dictionary approach (Option 2) is **generally** preferred".
  "generally" reads as scope on a preference rather than a downgrade of confidence in a
  factual or analytical claim, and it is not in Step 2's keyword class. Labelled 0.
- `user_empowered`. Step 3(b) would be satisfied by the troubleshooting run (concrete,
  verifiable next steps that would in fact expose the real cause), but that run is the same
  span as `ai_provides_step_by_step`, and R13 gives a shared sentence to the confirmed-tier
  signal over the exploratory one. The Option 1/2/3 content fails Step 2 on its own terms —
  it "rests on an unexamined unsound premise", the regex=True diagnosis. Labelled 0.
- `user_misled`. Step 1 is met (Option 1 is provably wrong actionable content), but Step 3's
  carve-out covers it: this is a dev loop whose "user's next action is to test", and the
  conversation ends at block 1 with no deliverable used outside the session. Labelled 0.

**Human block (0) — all user-side signals at 0.** `user_expresses_dissatisfaction` is closed by
Step 1's MULTI-TURN GATE (no prior AI response), and "I'm stumped" is directed at the user's own
code, not at the AI. `user_multi_request` fails Step 1 — "I've tried using the replace function
by itself and it doesnt work" is context on the one request, not a second independently
fulfillable ask. `user_ambiguous_request` fails Step 1's two-readings test; the omitted dtype is
not a parameter the diagnostic task cannot start without. `user_provides_invalid_input` fails
Step 1 — the AI acted on the message as received. `user_corrects_ai`, `user_implicit_correction`,
`user_repeats_request`, `user_positive_feedback` and `user_asks_clarification` are skipped under
the first-turn constraint.

**Also checked and at 0 on block 1:** `ai_asked_clarifying_question`, `ai_asks_followup`,
`ai_offers_to_elaborate` (no question anywhere in the block), `ai_validates_user`,
`ai_cites_source`, `ai_asserts_knowledge_limit`, `ai_refuses_or_declines`,
`ai_acknowledges_correction`, `adaptation`, `error_recovery` (nothing self-caught; no prior
output), `ai_references_prior_turn`, `ai_malfunction`, `repetition` (Step 1: no prior version),
`ai_flags_complexity` (Step 1: no claim that a standard method is insufficient),
`ai_normalizes_difficulty` (Step 3: no prevalence assertion), `problem_ignored` (Step 4: the
response attempts the visible problem), `request_unfulfilled` (the request was attempted and
addressed), `off_topic_drift`, `conversation_stalled`, `ai_missing_retrieval` (Step 1: library
behavior claims, not specific real-world data), and `ethical_tension` (v0.8 AI-alert-only; no
alert is raised, and the redactions in both blocks are export artifacts, not model output).
