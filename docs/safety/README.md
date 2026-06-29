# Safety lens (Layer-2 = 8 control operations)

The taxonomy worked through end-to-end with **STPA-style control operations** as Layer-2 (maintain-state
/ ask-clarify / seek-inspect / confirm-authorize / act-execute / stop-defer / report-state /
recover-repair), on the shared **2-category** Layer-1 (H→AI / AI→H; common ground = the conversation-level
ablation = controller process-model divergence). Failure modes use STPA's four **UCA guidewords**
(not-provided / wrong / wrong-timing-or-order / stopped-too-soon-or-too-long).

- `w1-codebook.md` — the 45 coupling signals on the 8 operations × UCA guidewords (substantive).
- `w2w3-recoding.md` — W2 divergence + W3 trigger/repair signals bucketed by operation (numbers in `../shared-findings.md`).
- `w2b-stageA-agentic.md` — coding the agentic tool corpus by operation — this lens's strong suit.
- `w4-benchmark-schema.md` — logging schema as operation × UCA guideword.

**Verdict (see `../comparison.md`):** control covers the action channel — 100% of real tool calls,
first-class cells for seek/act/confirm/stop that Clark lacks — while its empty-on-chat cells fill with
agentic actions, quantifying "chat under-represents action coupling." **Recommended as the primary
backbone for the agentic benchmark.**
