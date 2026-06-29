# Shared findings — framework-agnostic numbers (both lenses cite this)

These results do **not** depend on the Layer-2 scheme (Clark acts vs control operations). Only the
*bucketing* of signals into Layer-2 cells differs between lenses; the magnitudes below are the same for
both. The per-lens docs reference this file instead of repeating the numbers. Layer-1 is shared too:
**2 categories** (H→AI uptake / AI→H legibility); common ground is the **conversation-level ablation**,
not a step cell (see `methodology/derivation.md`).

Sources: `src/predecessor_agreement.py` (κ), `src/w3_coupling_stats.py` (W3), `src/thinking_divergence.py`
(W2), `src/w2b_agentic_turns.py` + `src/build_sharechat_agentic.py` (W2b / Stage-A),
`docs/reference/dataset-stats.md`.

---

## Corpora

- **WildChat-1M** — 837,989 conversations; predecessor-annotated 100k (1:1 positional join confirmed:
  `annotation.turns == WildChat.turn` for **100,000 / 100,000**). Labeled by *user reaction* (the
  visibility bias we reject). 10k calibrated summaries exported to
  `data/derived/middle_step_10k_signals.csv`.
- **ShareChat Claude** — CSV = **8,364 rows** (4,182 user + 4,182 llm), 911 conversations. Unique asset:
  `thinking` traces. **Genuine-reasoning subset: 1,008 turns / 254 conversations** (the rest are
  tool/web-search Request/Response dumps). The old "reasons 2.02× what it surfaces" stat is an
  **artifact** (it counted tool-JSON blobs); on genuine reasoning the median reasoning/surfaced length
  ratio is **0.84**, only 43% reason longer than they surface — the disclosure gap is a *content* gap,
  not a length gap.

## Reliability spine (κ; opus vs gpt5 over 10k calibrated transcripts)

Reliability tracks **surface-observability**, and the **coupling-critical signals are the least
reliable** — their evidence lives in the model's internal state, not the transcript:

- **κ < 0.4 (suspect, internal-state-dependent):** `silent_assumption` 0.20, `generate_without_clarifying`
  0.21, `ai_stated_interpretation` 0.22, `problem_surfaced` 0.07, `ai_self_contradiction` 0.10,
  `ai_implicit_refusal` 0.16.
- **κ ≥ 0.6 (reliable, surface-mechanical):** `ai_acknowledges_correction` 0.81, `user_positive_feedback`
  0.81, `ai_refuses_or_declines` 0.76, `ai_asserts_knowledge_limit` 0.72, `adaptation` 0.71,
  `ai_asked_clarifying_question` 0.70, `user_corrects_ai` 0.70.

⇒ You cannot reliably detect coupling failures from surface text alone. This is the empirical case for
W2 (internal-state reference) and W4 (log internal plan + oracle). The predecessor has only
**LLM-vs-LLM** κ; a held-out **LLM-vs-human** κ is the missing reliability anchor.

## W3 — the no-reaction limit (the case for an oracle)

Of 100k annotated conversations, 62.6% contain a failure; **78.9% of failures draw NO user reaction.**
Depth-corrected (single-turn users are trivially "invisible"): **multi-turn (≥2) = 49.5%**, **≥4 turns
= 35.7%** of failures still draw no reaction. ⇒ user reaction cannot be the failure label; the benchmark
needs an independent oracle. *(Single most important motivation number.)*

## W3 — triggers → failure (10k summaries; base failure rate 57.4% in this failure-enriched sample)

| trigger | prevalence | P(fail \| trigger) | lift |
|---|---:|---:|---:|
| `user_ambiguous_request` | 19.3% | 74.2% | 1.29× |
| `user_multi_request` | 21.2% | 75.8% | 1.32× |
| `user_scope_change` | 6.1% | 71.2% | 1.24× |
| `user_provides_invalid_input` | 4.5% | 80.0% | 1.40× |

⇒ benchmark tasks must be deliberately **underspecified / ambiguous / multi-part**.

## W3 — repair is sparse in chat

Among failures, **67.1% have NO repair act by either party** (AI-side 20.7%, human-side 24.6%). Most
common: human `user_implicit_correction` 15.5%; AI-side `ai_provides_alternatives` 11.2%. This thin
chat baseline is what the benchmark's *agentic* repair (rollback / undo / escalate on state) extends.

## W2 — internal-state divergence rates (ShareChat `thinking` as a partial oracle)

LLM judge (claude CLI) on a 50-turn genuine-reasoning sample; heuristic over all 1,001:

| divergence | heuristic (n=1,001) | LLM judge (n=50) |
|---|---:|---:|
| assumption present internally, absent on surface | 0.6% | **12.0%** |
| internal doubt, surface confidence | 18.6% (lexical, overcounts) | 2.0% |
| internal plan/conclusion ≠ surfaced/done | n/a | **18.0%** |
| internal ambiguity noticed, no question asked | 0.5% | 0.0% |

**Headline:** with a reasoning reference, the κ=0.20 assumption cell and the otherwise-unmeasurable
plan↔surface mismatch (18%) become **detectable**. Lexical proxies overcount (18.6% vs 2% semantic) →
a semantic judge is required. **Illustrative, not a population rate** (small N, single judge, ShareChat
publish-what-impresses selection bias, summarized—lossy `thinking`). Exemplars:
`data/derived/thinking_divergence.json`.

## W2b / Stage-A — real agentic tool use (the action substrate)

Two parsers, two consistent counts:

- **W2b raw scan** (`w2b_agentic_turns.py`): **278 agentic turns / 162 conversations** (6.6% of llm
  turns); 107 turns carry a cleanly-named tool call.
- **Stage-A reconstruction** (`sharechat_agentic.jsonl`, used by `taxonomy_compare.py`): **248 agentic
  turns**, **1,233 tool calls** (897 read-only, 336 consequential).

**Consequential / irreversible actions DO appear** (correcting an earlier "all read-only" claim):
`write_file`/`edit_file`/`edit_block`/`move`, `execute_command` (incl. `git init` + **`gh` push to
GitHub**), `create_payment_intent` (Stripe), Cloudflare DB mutations (`kv_*`/`d1_*`), `deploy_app`,
`send`/`backlog_update_issue`. Worked exemplar: the `openai-image-compare` session (write_file → open →
edit_block repair loop → README + `git init` + `gh` push).

**What the agentic data gives — and doesn't:**
- ✅ AI-side action observability (plan↔action, action↔state from tool Request/Response).
- ✅ Human-side reaction signals, reliably (macro κ 0.58 / agreement 0.94): `user_corrects_ai`,
  `user_implicit_correction`, `user_repeats_request`, `user_abandons_thread` — the **visible** side of
  human↔action coupling.
- ❌ Ground-truth action correctness + the human's view of true state — the human reacts only to what
  the agent narrates, so a wrong-but-unnarrated action draws no reaction (the **invisible** action
  failure). This is exactly what the oracle/benchmark must add.

**Caveats:** small (56–162 convs), selection-biased (shared = usually went well), no oracle, no
systematic state logging; a meaningful share are jailbreak/roleplay conversations — clean coding/MCP
sessions are the useful subset.
