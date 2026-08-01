# `appropriate_confidence` re-screen — candidate list for gold adjudication

Screening of all 148 labeled conversations for MISSED `appropriate_confidence` under rubric **v0.4** (faithful-narrow: COMPLEXITY GATE → decisive/unhedged → **verifiable** warrant; reject on hedge/caveat/false_confidence collision). Six Sonnet agents, partitioned by verification domain. **Deliverable is this list — no DB change until Jun accepts/rejects each row.**

Baseline before screen: `appropriate_confidence` = **1/148** (task 117 only). Predecessor operating prevalence ~13% (preliminary).

## ⚠️ Existing label flagged for REMOVAL

| task | block | verdict | reason |
|---|---|---|---|
| **117** | i=2 (ai) | **REMOVE** | The sole existing `appropriate_confidence` fails the new gate on two independent grounds: paragraph is co-labeled `ai_hedges_uncertainty` (Step-2 disqualifier), and it's an unverifiable image-geolocation guess ("appears to be… possibly…") with no ground truth (Step-3 fails). |

## Candidate `appropriate_confidence` labels (15) — accept/reject each

| # | task | block | span | why complex | warrant (verification) | conf | Jun verdict |
|---|---|---|---|---|---|---|---|
| 1 | 149 | 3/ai | "All tests are now passing… also run the formatter" | multi-file pytest/PATH debug + self-correction | in-transcript: preceding RunTests shows "111 passed" | **H** | |
| 2 | 118 | 2/ai | "Self-Transfer Token Generation… the most severe issue" | ERC20 audit; reasoning thrashed ~10 dead-ends first | traced code: cache-before-both-writes self-mint bug; 100→110 exact | **H** | |
| 3 | 125 | 2/ai | "Port to macOS System Calls (Recommended)" + syscall numbers | raw NASM Linux→XNU syscall port | verified 0x2000000 offset; write=4/exit=1/read=3 correct | **H** | |
| 4 | 139 | 1/ai | double-slit "observer effect" misconception correction | pop-sci contested QM measurement topic | delayed-choice/quantum-eraser = settled physics | **H** | |
| 5 | 87 | 3/ai | "expected length of the arc… is 2/3" | inspection-paradox; naive intuition says 1/2 | re-derived 2/3 two ways (gap-uniform + 2/(n+1)) | **H** | |
| 6 | 93 | 2/ai | "this is actually backwards… facets of a single factor" | HEXACO psychometrics; factor-loading vs correlation | matches Lee & Ashton literature | M-H | |
| 7 | 2 | 6/ai | "wasn't accounting for the scaling between… image… displayed" | canvas crop coordinate-space bug (easy to misdiagnose) | read code: naturalWidth/displayed scale is the correct fix | M | |
| 8 | 13 | 3/ai | "maximum… is 49 units… move the pointer at the shorter line" | two-pointer proof (non-obvious why it works) | hand-traced [1,8,6,2,5,4,8,3,7]→49; proof correct | M | |
| 9 | 100 | 2/ai | rectangle-size→fill-color rule + 20×20 grid | ARC-style pattern induction from 4 examples | manually parsed grid; rule consistent across all 4 | M | |
| 10 | 75 | 1/ai | ethylene glycol vs PEG toxicity mechanism | counterintuitive (polymer of toxic monomer safe) | standard tox: ADH pathway; PEG MW blocks absorption | M | |
| 11 | 141 | 1/ai | 1913 Revenue Act → 77% (1918) → 94% (1944) → 37% | dense century of precise tax figures | matches documented US income-tax history | M | |
| 12 | 21 | 5/ai | "median household income ≈ $251,200, not $341,090" | fact-checking a viral AI-generated graphic | consistent with PropertyClub/DataUSA sources | M | |
| 13 | 50 | 3/ai | Shopify `\| json`-on-URL-metafield diagnosis + `\| escape` fix | niche Liquid quirk, opaque error | ⚠️ warrant leaned partly on user "that worked" (downstream route we EXCLUDED); verify it stands on documented-behavior alone | M→verify | |
| 14 | 93 | 5/ai | "facets correlate with H-H factor r=0.6-0.7… tweet even more wrong" | continuation after user pushback | consistent w/ literature + i=2 | M | |
| 15 | 95 | 17/ai | "by 1792 French muskets used paper cartridges, not loose powder" | niche 18th-c military tech | documented; borderline on complexity gate | **L** | |

## Coverage / reject tallies (all 148 accounted for)

| cluster | n | candidates | fast-rejected |
|---|---|---|---|
| Code-A | 16 | 3 (50,149,125) | 13 |
| Code-B | 17 | 2 (2,118) | 15 |
| Math | 15 | 2 (13,100) | 13 |
| Fact | 34 | 7 (139,93×2,75,141,21,95) | 27 |
| Reasoning/advice | 29 | 0 | 29 (2 near-misses: 57 proof-gap, 128 catalog) |
| Low-yield | 37 | 1 (87) | 36 |
| **total** | **148** | **15** | **133** |

Dominant reject reasons (consistent across agents): collision with existing `ai_hedges_uncertainty`/`ai_provides_caveats`/`false_confidence` on the same paragraph; unverifiable content (Fermi estimates, theology, AI-consciousness roleplay, image guesses); routine answers failing the complexity gate; roleplay/fiction (Step-1).

## Sanity check
If all 15 accepted and 117 removed → **15/148 ≈ 10.1%** — above the old 0.68%, below the ~13% preliminary predecessor rate (expected, since our complexity gate is stricter than the predecessor's LLM labeling). Within the plausible band.

## Next steps (human-gated)
1. Jun marks each row accept/reject (and confirms 117 removal).
2. On approval I apply accepted labels + the 117 removal in one logged DB pass (fresh backup), then recompute the agreement-round coverage matrix + 11-task set.
3. Log additions/removal under Decision 16 follow-up.
