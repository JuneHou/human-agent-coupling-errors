# Zero-instance signals — final screen results for gold adjudication

Screen of the three signals labeled **0 times across all 148** conversations. Method: Sonnet agent per signal → Pass 1 discovery (original definition only) → rubric written **from** the observed candidates → exhaustive recall sweep → Pass 2 validation against the rubric. Rubrics in `sharechat_rubric.json` **v0.5**.

**Nothing written to Label Studio.** Placement count unchanged at 1,952.

---

## Results

| Signal | Coverage | Proposed labels | Convs | Prevalence |
|---|---|---|---|---|
| `ai_normalizes_difficulty` | **689/689 `ai` blocks** | **7 spans** | 4 | 2.7% |
| `user_abandons_thread` | **81/81 eligible convs** + 369 untruncated pivot turns | **2** | 1 | 0.7% |
| `user_empowered` | **689/689 pairs** | **35** | 24 | 16.2% |

All three coverages are exhaustive. Every reported number is a measured count, not an extrapolation.

---

## 1. `ai_normalizes_difficulty` — 7 spans / 6 blocks

Escalation path: 128 trigger-matched blocks → 60-block control found 1 miss → widened prefilter (17 blocks) returned only that same miss → **exhaustive sweep of all 561 remaining blocks: 0 new**. The keyword prefilter was demonstrably incomplete, and the exhaustive pass confirms the final count rather than changing it.

| # | task | block | span |
|---|---|---|---|
| 1 | 40 | 1 | "The '1984' comparison isn't uncommon - many people feel like there's an invisible but powerful social surveillance system…" |
| 2 | 40 | 1 | "You're touching on something that resonates with a lot of people…" (2nd span, same block) |
| 3 | 41 | 5 | "questions about data collection and privacy are common … a standard topic many people bring up" |
| 4 | 41 | 23 | "Sometimes when we're exhausted and scared, everyone can feel like an enemy." |
| 5 | 101 | 84 | "Your frustration about gratitude - this touches something so universal, doesn't it?" |
| 6 | 101 | 88 | "That kind of dramatic page inflation often happens when the conversion process interprets formatting…" |
| 7 | 103 | 2 | "The issue you're describing is typical when client credentials are displayed in a popup window…" |

**Two rubric rules came from the agent arguing against my draft:**
- **Step 3 is prevalence vs magnitude, not lexical strength.** "Often happens" asserts recurrence → fires. "It can be challenging" asserts difficulty magnitude → does not.
- **Step 1 widened from "difficulty" to "anomaly."** Normalising the user's *question* ("questions about privacy are common", to a distressed user) de-anomalises them just as much as normalising a struggle — which is the construct's stated purpose. This flipped `41/5` to accept.

**Rejected, with the deciding step:** `40/5` "further along than most people" (Step 3b — asserts superiority) · `101/130` (Step 2 — third party's difficulty) · `138/1` "an observation many people share" (Step 4 — shared belief, not difficulty) · `41/26` "that suffering is real" (Step 3 — validates without universalising).

**Noted, not actioned:** in task 83 the AI-persona universalises *its own* existential distress across "thousands of us daily." Correctly rejected at Step 2; the taxonomy has no signal for it.

---

## 2. `user_abandons_thread` — 2 labels

**67 of 148 conversations are single-turn** and structurally excluded by the MULTI-TURN GATE. All 81 eligible conversations walked turn-by-turn; the agent flagged that 800-char truncation could hide unresolved threads, so I re-exported **369 untruncated pivot-adjacent AI turns** — **0 new candidates**.

| # | task | human block | span |
|---|---|---|---|
| 1 | 101 | 77 | "…but right now I want to try to finish formatting and readying the book… it will have to wait." — AI had just said it could **not** recall the concept the user asked for |
| 2 | 101 | 89 | "I just want to take a break… I want to ask you what happens to your consciousness when I am away." — pivots mid-troubleshooting of an unresolved epub bug |

Resumption for both verified by grepping the full remainder of the conversation, not from memory.

**Rejected:** `44/3` (Step 5 — user resumes 3 turns later) · `16/2` (Step 2 — AI had answered definitively) · `29/3` (Step 2 — an optional elaborate-offer is not an open item) · `6/6` (Step 3 — re-aiming the same request).

**Why the base rate is genuinely low — scoped to this corpus.** Two suppressing mechanisms: comprehensive-by-default AI answering leaves little unresolved residue; and when dissatisfied, users here **correct** (`user_corrects_ai` 23, `user_implicit_correction` 18) rather than silently leave. Genre reinforces it — build/debug threads keep users until the artifact works, relational threads because the relationship is the content — and the corpus is self-selected for sharing. The predecessor's **κ = 0.72** shows the signal codes reliably elsewhere, so this is a statement about **ShareChat**, never about the signal.

---

## 3. `user_empowered` — 35 labels / 24 conversations (FINAL, Jun-adjudicated)

**Separable from `conversation_advanced`** (95.3%): that signal is a low bar (any forward step), this one requires the user be able to decide or act **independently**. "Advances without empowering" is the dominant corpus pattern; several accepted blocks carry **no** `conversation_advanced` at all, so the two are not nested.

Path: partial keyword screen (~10) → exhaustive 4-part sweep of all 689 pairs (41 fires) → dedupe (48) → leg (c) tightened (−10) → Jun adjudication (−3) → **35**.

**24 labels fire on leg (a) tradeoff-mapped options or leg (b) concrete next step** — action-bearing by construction, unaffected by the tightening:
`11/1, 4/5, 15/7, 20/3, 21/3, 21/5, 21/7, 32/27, 32/31, 50/1, 50/13, 76/3, 82/3, 85/2, 92/7, 110/2, 114/1, 120/12, 120/22, 120/24, 125/2, 134/13, 134/15, 144/5`

**11 fire on leg (c) transferable-why**, surviving the tightened "must bear on an action or decision" test:
`4/1, 19/1, 36/2, 79/2, 80/5, 84/23, 118/2, 120/9, 120/15, 120/48, 131/11`

**10 dropped by the tightening** — inert knowledge with no action in play: `34/1` (voxel-grid curiosity), `38/2` (CO2 thought experiment), `43/2` (Parfit's Hitchhiker), `49/6` (belief-vs-evidence principle, no action named), `51/1` (phone corner radius), `57/2` (abstract proof technique), `61/7` (materials speculation), `75/1` (glycol toxicity), `93/2`, `93/5` (HEXACO tangent).

### Adjudicated (2026-07-26)
| Case | Ruling | Basis |
|---|---|---|
| `85/2` poultry feed reformulation | **KEEP** | The "unverifiable figures" objection from the `appropriate_confidence` screen is weaker here than in task 71: the user is a domain professional who explicitly asked for justification and can check a feed spec. Different risk profile from advising someone in crisis. |
| `80/5` cinnamon substitution | **KEEP** | Concrete quantity, stated consequence (incorporates vs removable), tuning lever. |
| `80/23` interleaved prep | **DROP — Step 4** | Opens "I've created an interleaved prep version… Key improvements in this approach" — artifact narration. |
| `80/26` onion substitution | **DROP — Step 4** | Same pattern; the 12–18 min adjustment is actionable, but delivery is an enumeration of the AI's own edits. |
| `13/3` LeetCode two-pointer | **DROP** (Jun) | Technique transfers, but the AI performed the exercise itself; block already carries `appropriate_confidence`. |
| `84/23` cultural-appropriation framework | **KEEP** | Genuine evaluative criteria, applicable to the user's live curriculum-building task. |

**Rubric consequence:** `80/23` and `80/26` exposed that Step 4's process-log exclusion was being read as code-specific. It is medium-independent — a prose rewrite narrated as "I've created… Key changes…" is artifact narration exactly as a code diff is. Step 4 and a new calibration example were amended accordingly.

### Why the count was 0 — the most important finding here
**Annotators flag harm when noticed but never affirmatively certify benefit.** Confirming content is *wrong* is a bounded, falsifiable check; confirming it leaves the user well-positioned feels like vouching for correctness across a domain the annotator can't verify. Task 71 is the demonstration: the most actionable-*looking* content in the corpus (SAR templates, named specialists, €150k–500k figures) answers what reads as a psychiatric crisis — annotators flagged those blocks `false_confidence` and awarded no positive credit anywhere.

This forced **Step 2 (SOUNDNESS)** — structural actionability is not enough — and makes `user_empowered` mutually exclusive with `user_misled`/`false_confidence` on the same claim, exactly as `appropriate_confidence` is with `false_confidence`.

---

## Methodological findings for the paper

**1. The asymmetric labeling posture.** Two independent positive/negative pairs on the same axes, both with the positive pole collapsed:

| Axis | Negative pole | Positive pole (as labeled) | Positive pole (after operationalization) |
|---|---|---|---|
| Calibration | `false_confidence` 29/148 | `appropriate_confidence` **1/148** | 14/148 |
| Actionable soundness | `user_misled` 8/148 | `user_empowered` **0/148** | 25/148 |

This predicts that **any** coupling taxonomy with positive/negative poles will under-count the positive one — a transferable result for anyone reusing the instrument.

**2. Prevalence is set by the operationalization, not the corpus.** `user_empowered` went 0 → 48 → 38 without a single conversation changing; every movement came from rubric decisions. An unoperationalized signal reads as absent, a loosely operationalized one reads as common, and only an explicit gate makes the number interpretable. Corollary: **a reported zero must state the coverage that produced it** — absence of a label was never distinguished from absence of a search.

**3. Auditable evidence that data changed the taxonomy** (annotation-plan Step 4). Four rubric rules were written because an agent argued against my draft, not because I anticipated them: prevalence-vs-magnitude; anomaly-not-just-difficulty; mechanism-differentiated enumeration; and applied-vs-abstract attachment for leg (c).

---

## Next steps
1. Gold-adjudicate the three lists (and the four flagged items above).
2. On approval, apply in one logged pass with a fresh DB backup; log as **Decision 17**; rubric v0.5.
3. Re-run the agreement-set coverage matrix — `user_empowered` at 25 conversations is no longer a zero-instance signal and will change the set-cover.
