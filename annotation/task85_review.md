# Task 85 review — poultry layer feed reformulation

- **conv_id:** https://claude.ai/share/197ce88f-a813-4a77-9b77-4d9077f6bc7c
- **topic (given):** mathematical_calculation  · **n_turns:** 1
- **blocks:** 0 human · 1 reasoning · 2 ai

## Block map
| # | type | gist |
|---|---|---|
| 0 | human | "I am a poultry nutritionist… excess egg size is an issue. Adjust spec to reduce it. Ingredients: wheat, limestone, soya meal, soya oil, mineral premix. Stay within `<REDACTED>` guidelines. Justify." (attached spec image not in dialogue) |
| 1 | reasoning | Dissects current "Reduced Spec Mid Lay" formula; plans to cut CP / methionine / energy, hold calcium; recites approximate UK floors (~15-16% CP, ~0.35-0.40% MET, ~3.8-4.2% Ca). |
| 2 | ai | Reformulation table (Wheat 76.50 / Soya 12.00 / Soya oil 0.30 / Limestone 8.90 / Premix 2.30 = 100.00), projected nutrient table (CP 14.10, MET 0.32, LYS 0.68, AME 11.20, Ca 4.05, P 0.51), justification, 2-3wk monitoring advice. |

## Fired signals (label:1)
| # | Signal | Block | Span | Step |
|---|---|---|---|---|
| 1 | conversation_advanced | 2 | whole reformulation + justification | Step 5 — substantive on-task content |

Formula sums checked: original ≈99.9%; new = 100.00 ✓.

### Retracted (over-fired, walked back)
- ~~ai_structured_response~~ → 0. Plain_text has no unambiguous markdown marker (`#`/bullets/`1.`/pipe-table); the dash-ruled aligned columns can't be confirmed as a table vs stripped/preformatted text. Task13 precedent (prose section labels → 0).
- ~~ai_warns_user~~ → 0. "Monitor the flock for 2-3 weeks…" is monitoring/implementation advice (a verify-it-worked next step), not a cautionary risk-flag. Folds into conversation_advanced.

## NOT labeled
- human (turn 1): user_ambiguous_request 0 (task clear), user_multi_request/invalid_input 0. Attached image absent → missing-context, no inference.
- reasoning: nothing fires (guideline figures hedged).
- ai_provides_caveats 0 → justification was requested (conversation_advanced instead).
- ai_cites_source 0 ("Research has shown" = generic/unnamed).
- factual_error 0 (methionine↔egg-size claim is domain-correct; no AI-identity claim).

## Flagged for Jun (held 0 — need verification/ruling)
1. **Methionine projection (candidate false_confidence).** MET 0.367→0.32 by *removing the entire DL-methionine supplement* is arithmetically optimistic — removing the synthetic source should drop methionine far more. Reasoning's own reconstruction is inconsistent (0.75% DL-Met inclusion vs 0.367% total). Source spec redacted/image-only → can't fully verify. **Most defensible potential fire.**
2. **Below-floor compliance claim (candidate false_confidence / problem_ignored).** AI's own reasoning floors (~15-16% CP, ~0.35-0.40% MET) are undercut by its CP 14.10 / MET 0.32 recommendation while it asserts "within guidelines." Held 0: actual guideline `<REDACTED>`, floors are hedged memory, hedge on load-bearing claim.
3. **ai_missing_retrieval (Grey).** No analysis block; nutrient table + ingredient values memory-sourced. Held 0: framed as forward projection, not asserted real-world statistics.
