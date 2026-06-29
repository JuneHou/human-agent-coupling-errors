# Layer-2 head-to-head: Clark grounding acts vs control operations

**Question.** Layer-1 is settled (2 categories: H→AI uptake / AI→H legibility; common ground = the
conversation-level ablation, not a cell). Layer-2 is the open fork — two candidates:

- **Communication lens** — Clark's 5 grounding acts: *present / clarify / accept / repair / maintain*.
- **Safety lens** — 8 STPA-style control operations: *maintain-state / ask-clarify / seek-inspect /
  confirm-authorize / act-execute / stop-defer / report-state / recover-repair*.

Rather than argue, we **applied both** to the real data and measured fit. All numbers below come from
`src/taxonomy_compare.py` → `data/derived/taxonomy_comparison.json` (deterministic, no LLM). The 65
predecessor signals are the shared substrate; 45 are coupling cells, 20 are mechanism-layer
(single-side defects / triggers / style / outcome markers — not a coupling cell under *either* scheme).

---

## Metric A — signal coverage (45 coupling signals; mass = conversation frequency over the 10k corpus)

| Clark act | #signals | | Control operation | #signals | corpus mass |
|---|--:|---|---|--:|--:|
| present | 15 | | maintain_state | 6 | 12,073 |
| clarify | 5 | | ask_clarify | 5 | 5,441 |
| accept | 4 | | **seek_inspect** | **0** | **0** |
| repair | 10 | | **confirm_authorize** | **1** | **55** |
| maintain | 11 | | act_execute | 6 | 21,508 |
| | | | **stop_defer** | **1** | **420** |
| | | | report_state | 14 | 16,021 |
| | | | recover_repair | 12 | 6,271 |

- **Clark:** all 5 acts populated — **0 empty, 0 near-empty**; type-entropy 2.17 bits, mass-entropy 1.75.
- **Control:** **`seek_inspect` empty**, **`confirm_authorize` & `stop_defer` near-empty (1 signal each)**;
  type-entropy 2.40 bits, mass-entropy 2.20. The three thin cells carry **~1.4%** of total chat mass
  (0 + 55 + 420 of ~61.8k); the chat signals concentrate in report_state, act_execute, maintain_state.
- **Orphans:** none — every coupling signal lands in exactly one cell under *both* schemes.

**Reading.** Clark fits the chat-era signals *because it was built for communication* — it spreads them
evenly with no gaps. Control's gaps are not a defect: the three empty/near-empty cells are precisely the
**action-native** operations (inspect-before-acting, get-approval-before-acting, refrain-when-unresolved),
which **communication signals structurally cannot exercise.** The chat taxonomy is *blind* to those
operations; Clark cannot even name them.

## Metric B — agentic coverage (reconstructed agentic corpus, `sharechat_agentic.jsonl`)

4,182 turns; **248 agentic turns** (≥1 tool call); **1,233 tool calls** (897 read-only, 336 consequential).

| scheme | tool calls placed in a named cell | how |
|---|--:|---|
| **Control** | **100.0%** | 897 → `seek_inspect`, 336 → `act_execute` |
| **Clark** | **0.0%** | no grounding act instantiates a tool execution |

The single most telling number: **`seek_inspect` holds 0 chat signals (0 mass) but 897 real tool calls.**
The control operations that chat never populated are exactly the ones the agentic data fills — and Clark
has no cell for them at all. (Clark's "action column" is acknowledged-empty by design in
`communication/w1-codebook.md`; this 0% is that acknowledged gap, quantified — not a failure of coding.)

---

## Verdict

The two schemes are **complementary, not rivals**:

- **Clark wins on the communication channel** — it cleanly, evenly absorbs the 45 chat coupling signals
  (the meaning column), with no empty cells.
- **Control wins on the action channel** — it has first-class cells for the agentic operations (seek /
  act / confirm / stop) that Clark cannot represent and that chat data never reached, and it codes 100%
  of real tool calls.

**Recommendation (consistent with the ICLR positioning).** Adopt **control operations as the primary
Layer-2 backbone** for the agentic benchmark — it is action-native, covers the tool-use coupling Clark
misses, and its empty-on-chat cells (now shown to fill with real agentic actions) are the quantified
argument that *chat under-represents action coupling*. **Retain Clark as the communication-channel
sub-model** for the meaning column, where it strictly dominates. The data does not support flattening to
the two directions alone: act/seek/confirm/stop carry distinct, separately-populated mass.

**Honest caveats.** (1) The mappings are author-assigned; the *direction* of the result (control's action
cells empty on chat, full on agentic) follows from the predecessor signals being communication-era
signals, not from mapping choices — but the exact per-cell counts depend on a handful of borderline
placements (e.g. `ai_refuses_or_declines` → stop_defer; `intent_missed` → act_execute as
"response-as-action"). (2) `act_execute` is heavily populated in *chat* (mass 21,508) only because the
utterance is treated as the action; its agentic meaning (real tool execution) is the novel part. (3) No
oracle: agentic coverage measures whether a scheme *can place* a tool call, not whether the action was
*correct* — that gap is what the benchmark adds. Reproduce: `python src/taxonomy_compare.py`.
