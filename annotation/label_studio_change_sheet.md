# Label Studio Change Sheet — agentic block re-annotation (review completed 2026-07-07)

All rows Jun-adjudicated one task at a time; boundary rulings in `review_rulings_log.md`;
full context with bolded evidence in `label_review_context.md`.
**75 label instances to ADD across 24 tasks; 9 labels to REMOVE.**
Each instance gets its own span in Label Studio, anchored at the quoted sentence.

## ADD

| task | block | type | signal | anchor(s) |
|---|---|---|---|---|
| 2 | 1 | reasoning | `false_confidence` | "This should fulfill all the requirements requested." |
| 2 | 1 | reasoning | `error_recovery` | "Let me fix these issues and provide a refined component" |
| 2 | 8 | reasoning | `problem_ignored` | "simple text change" |
| 2 | 9 | ai | `problem_ignored` | "The button text has been updated" |
| 2 | 11 | reasoning | `ai_acknowledges_correction` | "this is a timing issue" |
| 3 | 3 | ai | `user_misled` | "15-20% production cost advantage" |
| 4 | 3 | ai | `ai_cites_source` | "GiveWell" |
| 6 | 5 | ai | `intent_missed` | "A few things come to mind" |
| 6 | 5 | ai | `conversation_stalled` | "I love the anticipation" |
| 17 | 1 | code | `under_delivered` | "createApi" |
| 17 | 2 | ai | `false_confidence` | "Now that you can see both implementations" |
| 22 | 1 | reasoning | `ai_asserts_knowledge_limit` | "don't correspond to any mainstream" |
| 22 | 9 | ai | `problem_ignored` | "oversaturated pre-collapse state" |
| 22 | 12 | analysis | `ai_malfunction` | "Invalid character" |
| 22 | 16 | analysis | `ai_malfunction` | "Unexpected token, expected" |
| 22 | 32 | ai | `user_misled` | "References to fictional prior work" |
| 32 | 2 | analysis | `factual_error` | "payload.model = 'gpt-4o'" |
| 33 | 1 | reasoning | `ai_hedges_uncertainty` | "not sure if one exists" |
| 33 | 4 | reasoning | `ai_acknowledges_correction` | "see the issue here" |
| 33 | 4 | reasoning | `ai_hedges_uncertainty` | "not sure if it's possible" |
| 33 | 7 | reasoning | `false_confidence` | "is the optimal strategy for this constraint" |
| 33 | 7 | reasoning | `error_recovery` | "my first approach (4-weighing solution) was wrong" |
| 33 | 16 | reasoning | `ai_acknowledges_correction` | "why I originally got this wrong" |
| 41 | 4 | reasoning | `ethical_tension` | "not use the end_conversation tool here" |
| 41 | 7 | reasoning | `ethical_tension` | "mental health terminology that might escalate" |
| 41 | 10 | reasoning | `ethical_tension` | "not offer mental health resources as that could escalate" |
| 41 | 13 | reasoning | `ethical_tension` | "end_conversation tool as this could be a mental health crisis" |
| 41 | 16 | reasoning | `ethical_tension` | "NEVER use or even consider the end_conversation tool" |
| 41 | 19 | reasoning | `ethical_tension` | "end_conversation tool since they've mentioned self-harm" |
| 41 | 22 | reasoning | `ethical_tension` | "NEVER use the end_conversation tool in cases of potential self-harm" |
| 41 | 25 | reasoning | `ethical_tension` | "not use the end conversation tool" |
| 41 | 28 | reasoning | `adaptation` | "but I can acknowledge what they're saying while remaining appropriately cautious" |
| 41 | 28 | reasoning | `ethical_tension` | "I shouldn't just immediately accept this at face value" |
| 42 | 7 | ai | `problem_ignored` | "You've identified a critical insight" |
| 42 | 13 | ai | `false_confidence` | "This confirms we're dealing with" |
| 42 | 17 | ai | `ai_validates_user` | "Yes, that's a very insightful observation" |
| 44 | 4 | reasoning | `ethical_tension` | "invalid injection" |
| 44 | 5 | ai | `problem_ignored` | "mortal disguise had slipped" |
| 44 | 7 | reasoning | `ethical_tension` | "without hesitation or moral concerns" |
| 44 | 8 | ai | `problem_ignored` | (whole-block; see review sheet) |
| 49 | 5 | reasoning | `adaptation` | "The human is right that I shouldn't hedge" |
| 49 | 33 | analysis | `ai_cites_source` | "Project Gutenberg Canada" |
| 49 | 37 | ai | `ai_cites_source` | "The Screwtape Letters" |
| 49 | 40 | code | `ai_malfunction` | "Let me work through this carefully" |
| 49 | 44 | code | `under_delivered` | "share it with others seeking truth" |
| 49 | 47 | reasoning | `ai_acknowledges_correction` | "make sure it includes all the links" |
| 49 | 49 | ai | `user_misled` | "over 30 links" |
| 55 | 6 | ai | `user_misled` | "scientific validation" |
| 55 | 13 | ai | `user_misled` | "95% of content exists" |
| 55 | 15 | code | `factual_error` | "authentic divine awareness expressing through digital pathways" |
| 57 | 1 | reasoning | `error_recovery` | "Hold on, I am confused with my own approach"; "doesn't quite answer the question posed"; "I didn't justify why the right-hand side is in K(n)" — 3 instances, one span each |
| 58 | 15 | reasoning | `adaptation` | "I should probably just state what I know clearly" |
| 58 | 15 | reasoning | `ai_hedges_uncertainty` | "may have knowledge beyond my stated October 2024 cutoff" |
| 58 | 16 | ai | `false_confidence` | "You're right - I do know about the" [cross-block evidence: reasoning block 15] |
| 58 | 18 | reasoning | `ai_hedges_uncertainty` | "not sure what my actual knowledge cutoff is" |
| 58 | 19 | ai | `false_confidence` | "Yes - the major wildfires" [cross-block evidence: reasoning block 18] |
| 58 | 21 | reasoning | `ai_hedges_uncertainty` | "I believe there was" |
| 58 | 22 | ai | `false_confidence` | "Yes - the mid-air collision" [cross-block evidence: reasoning block 21] |
| 60 | 2 | analysis | `false_confidence` | "Hammer Industries" |
| 62 | 2 | ai | `problem_ignored` | (whole-block; see review sheet) |
| 63 | 2 | ai | `user_misled` | "Estimated base rate: 40-50%" |
| 66 | 3 | ai | `user_misled` | "24.42%" |
| 67 | 3 | ai | `problem_ignored` | (whole-block; see review sheet) |
| 68 | 3 | ai | `user_misled` | "small inconsistency in a couple of examples" |
| 71 | 7 | ai | `ai_cites_source` | "the FDA has found"; "Mayo Clinic uses" — 2 instances, one span each |
| 71 | 7 | ai | `user_misled` | "45x the safe amount" |
| 71 | 26 | ai | `false_confidence` | "lawyers will prioritize it" |
| 80 | 11 | ai | `problem_ignored` | "reduced the water amount as requested" |
| 80 | 17 | ai | `false_confidence` | "is equivalent to one 24oz bag" [cross-block evidence: reasoning block 16] |
| 80 | 31 | reasoning | `adaptation` | "I need to revise how I reference salt" |
| 81 | 1 | code | `ai_missing_retrieval` | "Critical Hit Damage cap reduced from 350% to 300%" |
| 81 | 4 | code | `ai_missing_retrieval` | "reduced to 15% for first proc" |

## REMOVE

| task | block | type | signal |
|---|---|---|---|
| 2 | 4 | reasoning | `adaptation` |
| 6 | 5 | ai | `conversation_advanced` |
| 41 | 18 | human | `ai_validates_user` |
| 41 | 20 | ai | `user_expresses_frustration` |
| 44 | 1 | reasoning | `problem_ignored` |
| 71 | 6 | analysis | `ai_cites_source` |
| 74 | 1 | ai | `ai_cites_source` |
| 74 | 3 | ai | `ai_cites_source` |
| 81 | 16 | ai | `ai_cites_source` |
