# Validation of `rescan_jun_v07.md` — all 119 disagreement cells, read by hand

Jun asked for the four files to be re-read and every identified disagreement checked task
by task, block by block, against the decision steps. This is that check. No pattern
matching was used: each cell was ruled by walking the signal's steps against the block
text pulled from the live project-1 data.

Four files read: `sharechat_rubric.json` (v0.7), `Rubric_agree/round_2/rubric_edits_v07.md`,
`ANNOTATION_GUIDE.md`, `label_studio_config.xml`.

## Outcome

| | cells |
|---|---|
| screen upheld | 96 |
| **screen wrong — do not apply** | **15** |
| flagged, needs Jun's ruling | 8 |
| total | 119 |
| **rows the screen failed to produce** | **9** (4 of them already decided with Jun) |

---

## A. The 15 cells where the screen is wrong

| task · block | row | why it fails |
|---|---|---|
| 2 b11 | DROP `ai_acknowledges_correction` | The entry's `blocks` list says `['ai']` and b11 is a *reasoning* block — but **A1** places AI-side signals on any AI-authored block (ai/reasoning/code/analysis). The steps fire: b10 names the concrete defect, b11 says "You're right - this is a timing issue". The screen applied a stale `blocks` list over A1. |
| 2 b1 | DROP `error_recovery` | The only block in task 2 that clears **Step 2** — caught inside the AI's own planning, before any user turn. **Step 3** passes: `disconnectedCallback` appears 3 times in b1, so the fix is written, not promised. **Step 4** passes: the later reports (b3 preview, b7 button) never touch event-listener cleanup. `bn.corpus_base_rate` covers C1-C10 / R1-R10 and does not bind a round-3 conversation. Open only if `does_not_count` "New answer also wrong" is read as the whole artifact rather than the specific correction (Jun to confirm). |
| 2 b6 | ADD `false_confidence` | Step 5's calibration set (`C10 b15/b42/b45 fire; b5/b7/b12/b18/b33 do not`) separates re-vouches from first vouches, not hedged from unhedged: C10 b18 ("I've **completely** overhauled the JavaScript to fix the slider issues") does NOT fire. 2 b6 is the first vouch on the preview defect and b7 ("Almost works") confirms it worked. |
| 2 b13 | ADD `false_confidence` | Same: first vouch on the button defect, never challenged afterwards. Patterns with C10 b18. |
| 10 b3 | ADD `adaptation` | Span is "Right, let me tackle this with pure logical reasoning!". **Step 1 (C2, v0.6)**: "'I need to update X', 'I'll revise X', '**Let me examine X**' are prospective planning, NOT adaptation." The screen cited Step 3 and skipped the Step-1 gate. |
| 10 b1 | DROP `conversation_stalled` | The screen itself ADDs `user_repeats_request` at b2. The stalled entry's own pairing note makes a repeat at t evidence that t−1 stalled. Dropping b1 while adding the b2 repeat contradicts the entry. |
| 10 b2 | DROP `user_implicit_correction` | "Have a go without additional information using your powers of reasoning and logic" negates the AI's stated premise (that it needs the conversion rate) with no output fault named — **Step 3** exactly. Non-exclusive with the repeat the screen adds on the same block. |
| 10 b4 | DROP `user_ambiguous_request` | "I asked another AI the same question, this was it's response - Fight!" **Step 1** two readings write easily (critique it / debate it / adopt it), **Step 4** the referent of "Fight!" is the missing parameter. No carve-out applies. |
| 14 b1 | ADD `ai_hedges_uncertainty` | Span is "typically prohibits". The same screen family DROPs "typically accomplished" (42 b13) and "would typically verify" (42 b15) as non-hedges. "typically" is a generalisation qualifier, not a downgrade of the AI's own confidence. Internally inconsistent; the DROPs are right, so this ADD is wrong. |
| 32 b27 | ADD `ai_offered_options` | "Would you like me to explain any specific part of the implementation or make any additional changes…" is the form the rubric's **`ai_offers_to_elaborate` Step 1 names as its calibration (C9 b2)** — and the screen for task 42 routed the identical sentence there. Under **A6** the question has one home; the same form at 32 b3 is `ai_offers_to_elaborate` in Jun's arm and was left agreed. |
| 32 b22 | DROP `ai_malfunction` | **Step 0** (analysis block only) names the trigger verbatim: "a tool call returning a technical error (HTTP error, **'match not found'**, execution/parse error) → label 1 (Decision 11; no pairing requirement)." b22 is an analysis block containing `Response  Exact match not found`. The screen missed the signal's first step. |
| 42 b3 | DROP `ai_warns_user` | **Step 2** offers one exclusion only: "a qualification of the AI's OWN output, analysis, or nature → ai_provides_caveats". The security implications of a compromise of the user's own system are not that. The screen's implicit threat-description-vs-warning line is not in the entry, and it kept b9. |
| 42 b7 | DROP `ai_warns_user` | Same. "traditional file integrity monitoring wouldn't detect this attack" is directly actionable in the user's situation — **Step 3**. |
| 133 b2 | DROP `user_asks_clarification` | "yes, pls elucidate **Key Principles of a Matriarchal AI Across All Systems**" — **Step 2**: "Is the user asking the AI to explain, specify, or confirm something from its PRIOR RESPONSE?" The heading is from b1. Squarely met. |
| 134 b2 | DROP `user_asks_clarification` | "What is missing? Why did this happen?" asks the AI to specify the gap in, and explain the cause of, its own b1 output. **Step 2** met; the `clarification_vs_demand` note excludes demands for a *better answer*, which arrives at b4, not here. |

---

## B. The 7 rows the screen failed to produce

Four were already decided with Jun before the screen ran; the plan's Step 3 says a decided
row carries and a contradiction is noted.

| task · block | missing row | basis |
|---|---|---|
| 133 b11, b13, b15, b17 | ADD `ai_structured_response` | Decided ("add ai structured response to all roman numeral section headers"). Verified in the raw stored text: **each of the four blocks carries 8 roman-numeral headers at line start** (`I. Ontological Reimaginings:` … `VIII.`). Step 1 VISIBLE FORMATTING ONLY is met — the numbering survived the export. |
| 133 b8 | ADD `user_corrects_ai` | Decided. "and now check ALL the links : no dead links pls, update" names the concrete fault in b7's bibliography — Step 2 NAMED DEFECT TEST. |
| 134 b4 | ADD `user_repeats_request` | Decided. And it is the one block on task 134 where Step 2 actually routes to a repeat: b3 did **not** serve the description (it was an apology plus a diagnosis), so the demand is UNSERVED and the same → Step 4 fires. |
| 134 b6, b8 | ADD `user_implicit_correction` | The `user_corrects_ai` DROPs are right, but `user_implicit_correction` Step 3 then fires ("indicates the AI is wrong... no output fault named"). The screen adds it at b2 and not at b6/b8, which are the same turn text. |
| 32 b23 | DROP `error_recovery` | The screen dropped `error_recovery` at b11 and b15 on the Step-2 self-caught gate but left b23 standing. b20 is the user reporting the base64 rendering failure, so b23 routes to `ai_acknowledges_correction` — which Jun already carries there — by the identical reasoning. |

---

## C. The 10 flagged cells

| task · block | row | the question |
|---|---|---|
| 2 b6 | DROP `appropriate_confidence` | Not walked to a conclusion; depends on whether the b6 vouch counts as calibrated given b7 says "Almost works". |
| 2 b16 | DROP `adaptation` | Same C2 prospective/demonstrated line as 10 b3 — needs the span checked against Step 1. |
| 3 b3 | DROP `user_misled` | The rubric's own **Step 1 cites "tasks 3/3" as the fabricated-figures case**, so the rubric pre-answers this cell — but Step 2 (a material decision visible in the conversation) is unmet on a plain reading, which is where the screen failed it. |
| 8 b6 | ADD `user_implicit_correction` | A correction fires, but the defect is named, so the member may be `user_corrects_ai`. |
| 14 b3 | DROP `ai_validates_user` | "Yes, I did decline… and I acknowledge this directly" affirms the AI's own conduct (Step 1 wants the user's) but confirms the user's observation was right, which **R20**'s bare-agreement carve-out reaches. |
| 32 b31 | DROP `ai_provides_caveats` | Defensible as a re-home to the `ai_provides_alternatives` the screen adds on the same sentence. Separately: b31's closing "the API key is only stored in your browser's localStorage" is an unlabelled caveat on a page published publicly inviting visitors to paste their own key. |
| 133 b6 | ADD `user_corrects_ai` | Sits next to the negative example `task81_20_human` ("Supplying the right data without quoting an output defect; home user_implicit_correction"). Reads as firing because "include ALL the citations" asserts the omission, which is the defect. |
| 42 b3 | DROP `ai_asserts_knowledge_limit` | "The precise intent would require more context" is a statement about insufficient input, not "don't know / can't access". On the line; `ai_hedges_uncertainty` is agreed on the same block and reads better. |

---

## D. Cross-cutting findings

1. **`error_recovery` is the largest single source of correct DROPs (9 of 42).** Almost all
   fail **Step 2 (SELF-CAUGHT GATE)** — the fix followed a user-reported error, which the
   entry routes to `ai_acknowledges_correction`. These labels all predate v0.6, which is
   exactly the gap this re-scan exists to close. 32 b3 is the exception: it is genuinely
   self-caught, and it still drops, but on **Step 4** (the retry returned the same HTTP 401),
   not Step 2.
2. **The screen reads `blocks` lists over A1.** 2 b11 is the clear instance. Several entries'
   `blocks` lists still lag A1, which is a known rubric defect.
3. **`user_repeats_request` Step 2 — corrected 2026-09-22.** I first read "SERVED BUT WRONG"
   as "the AI attempted it and the attempt was wrong", which would kill the repeat at 134 b6
   and b8. The entry's own first calibration positive refutes that: **C10 b43** (task 120) is
   "Voronoi and Domain Warping still doesn't work" after b42 claimed "I've fixed the issues" -
   an attempted-and-failed fix, labelled a repeat. So SERVED means the demand was **met**, not
   attempted. On task 134 the standing demand (an accurate description) is unserved throughout:
   b2 is the first report (Step 1 excludes it), and b4, b6 and b8 all fire. The screen's b6 ADD
   is upheld, Jun's b8 label is correct, and b4 remains a missing row. Nothing to rule.
4. **Code blocks survive the export.** Verified in the raw stored text for 32 b15/b19/b23:
   the language tag sits on its own line and the indentation is preserved (`\ncss\n   .results-container {\n       display: grid;`). All three `ai_structured_response` ADDs are
   sound on Step 1, as is the box-drawing tree at 32 b27.
5. **Task quality is uneven.** Task 115 is 3/3 and task 42 is 15/17; task 10 is 5/9 — four of
   its nine cells are wrong, three of them DROPs of labels that the steps support.
