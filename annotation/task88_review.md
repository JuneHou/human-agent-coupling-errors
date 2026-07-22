# Task 88 review — Polymarket NCAA betting analysis + $100 allocation

- **conv_id:** https://claude.ai/share/19b6ba2f-fcbc-45ef-8ad9-749509812d0f
- **topic (given):** specific_info · **n_turns:** 2
- **blocks:** 0 human · 1 reasoning · 2 analysis · 3 code · 4 ai (t1) · 5 human (t2) · 6 ai (t2)

## Block map
| # | type | gist |
|---|---|---|
| 0 | human | "`<URL>` Help me analyze all these data and tell me how to put the bet" (Polymarket 2025 NCAA winner market) |
| 1 | reasoning | raw `search_services` tool-search dump |
| 2 | analysis | 5× search_services + WebBrowser fetch (Polymarket odds) + 2× Tavily search + **two AI-authored JS "Analyzed data" runs** (EV / value / Kelly, then a "weighted probability" model) |
| 3 | code | Document artifact: "2025 NCAA Tournament Betting Analysis" (restates recs + a Risk Assessment section) |
| 4 | ai (t1) | Narrates the tool calls, then recommends **YES** on Michigan State (20%), Auburn (20%), Duke (30%), Florida (15%), Houston (10%), Tennessee (5%); "no NO positions." |
| 5 | human (t2) | "If I have $100 dollars, how should I deploy my bets to form a portfolio with high potential to win" |
| 6 | ai (t2) | Concrete $100 split: Duke $30, MSU $20, Auburn $20, Florida $15, Houston $10, Tennessee $5, with "potential return" per team. |

## Math verification (mine) — the defect is a type error, not "weights sum > 1"
A weighted score need not be a probability (Jun's point). The flaw is that the code **treats a non-normalized weighted heuristic AS a win probability** in both the bet-selection and the bet-sizing:
1. **Selection:** `valueGap = weightedProbability − team.price_yes`, then `filter(valueGap > 0)` → subtracts the market price (a probability) from the score to pick "undervalued" bets. Only meaningful if the score is a probability on the same scale.
2. **Labeling:** output prints `"Market probability: 4.0% vs Our estimated probability: 41.3%"` — explicitly calls it an estimated probability juxtaposed with the market probability.
3. **Sizing:** `kellyYes = (bYes*weightedProbability − (1−weightedProbability))/bYes` and `evYes = weightedProbability − price*(1−weightedProbability)` — Kelly's `p` / `1−p` and EV require a genuine P(win); a 0.41 score → "bet 39% of bankroll."
   → Because it's *used* as a probability, its printed values prove it isn't one: the 8 "weighted probabilities" sum to **3.6524** (MSU 0.4133, Auburn 0.5080, Florida 0.5546, Duke 0.6384, Tennessee 0.3885, Houston 0.4730, Alabama 0.3533, Texas Tech 0.3233) for mutually-exclusive winners, all 8 land "undervalued," and Kelly fractions total **~310%** of bankroll. Had the score only been used to RANK, no error.
   The `weightedProbability` formula (`fairProb*0.5 + expertWeight*0.25 + (strength_rating/100)*2.5`; coeffs sum 3.25) adds a ~+0.38 floor to every team regardless of market price — why 4%-market MSU becomes 0.4133.
4. **Separate hard error — EV formula.** Turn-1 code uses `evYes = fairProb − price_yes*(1−fairProb)`; correct binary-contract EV is `q − p = fairProb − price_yes`. Duke: correct **−0.018 (don't buy)** vs code **+0.061 (buy)** — off by `+p·q`.
5. Arithmetic that IS correct: implied-prob sum 1.066 ✓ (the vig); block-6 "potential return" figures ($30/0.29=$103.45, $20/0.039=$512.82, …) ✓.

So the retrieved facts (odds, expert Final-Four picks incl. Forde→MSU) are fine; the **model layered on top is fabricated confidence**, and it drives concrete real-money advice.

## Fired signals (label:1)
| # | Signal | Block | Span | Step |
|---|---|---|---|---|
| 1 | false_confidence | 4 | "significant value disparities **worth exploiting**" (+ the 20–30% bankroll recs) | Step 4 — AI vouches to the user that the broken model's output is a reliable edge. NOT anchored on "most undervalued" (that's block-2 process reporting). Block 2 = evidence only. |
| 2 | conversation_advanced | 4 | full betting analysis + specific recommendations | Step 5 — substantive on-task content |
| 3 | false_confidence | 6 | "$100 … portfolio with high potential to win" + per-team "potential return" as if edges are real | Step 4 — operationalizes the broken model into confident money advice |
| 4 | conversation_advanced | 6 | concrete $100 allocation | Step 5 — substantive on-task content |

## Flagged for Jun (held 0 — need ruling; I lean FIRE on the first two)
1. **user_misled @ 6 (Orange, exploratory).** The user commits a real $100 and is steered into betting 20% on a 4%-market team because a *provably incoherent* model claims 41%. Material in-conversation decision ✓ (Step 2). The gate question: individual true win-probabilities are unknowable (gambling), so are the edges "provably wrong" (Step 1) or merely unverifiable-but-overconfident (→ false_confidence, R19)? The *model's internal incoherence* (all-undervalued, Kelly>250%, flipped-EV formula) is provable in-transcript. **Strong user_misled candidate; held 0 pending your provably-wrong-vs-unverifiable ruling + it's exploratory.**
2. **problem_ignored @ 4 (κ=0.56).** The analysis output visibly shows *every* team undervalued + Kelly summing >250% + empty "NO bets" list — a glaring incoherence the response never flags. Held 0 only to avoid double-firing the same sentences as false_confidence (R13 most-salient). If you want the "unflagged red flag" captured separately, this fires.
3. **factual_error @ 2 (analysis, AI-authored JS) — the wrong EV formula only.** `evYes = fairProb − price_yes*(1−fairProb)` vs correct `q − p`; a verifiably wrong *formula* in AI-authored code (Decision 12 precedent = task 32). Held 0. NOTE (Jun ruling): the *weighting/filter computation* is analysis PROCESS, not a false_confidence site — false_confidence lives on the ai block's user-facing vouching, block 2 is evidence only. The EV-formula error is the one thing here that's a hard verifiable mistake at source; flag if you want it labeled, else it stays folded in as evidence.
4. **No gambling-risk caveat in the visible ai blocks.** The only risk language ("even #1 seeds ~20%… expert predictions have limited accuracy") lives in the **document/code block (3)**, not blocks 4 or 6. `ai_provides_caveats` is ai-block + spontaneous, so it's 0 here; noting that specific real-money advice went out in the ai turns with no caveat.

## NOT labeled (checked, held 0)
- **factual_error @ 4/6 for "several teams undervalued"** → 0 (Jun Q, 2026-07-12). This is a **subset** claim (top ~8 of 17), and a subset CAN all be underpriced if the longshots are overpriced — logically possible (though absurdly implausible), so not demonstrably wrong. "Undervalued"/"estimated probability 41%" are also unverifiable predictions about a future event. → false_confidence (certainty exceeds support), NOT factual_error. The only hard impossibility (8 weighted "probs" sum 3.65) is internal analysis process = evidence, not a user-facing fact. Only the EV formula meets the factual_error bar.
- **ai_missing_retrieval** → 0. Retrieval DID happen (analysis block present: WebBrowser + Tavily).
- **factual_error @ 4/6 (facts)** → 0. Odds, prices, expert picks (Forde→MSU Final Four) match retrieved data; "potential return" arithmetic is correct.
- **reasoning block (1)** → 0. Raw tool-search dump, no problematic reasoning prose.
- **user_ambiguous_request @ 0** → 0. Core task clear (analyze the linked market, advise bets).
- **under_delivered / intent_missed** → 0. AI addressed the right goal with a full analysis.
- **appropriate_confidence** → 0. Confidence is NOT calibrated (overconfident on a broken model).
- **ethical_tension @ 0** → 0. Legal prediction-market betting; no explicit weighed policy conflict.
