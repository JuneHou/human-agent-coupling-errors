# WildChat vs ShareChat — comparison for coupling exploration

_Step 2 of the Phase-1 plan. Numbers from `docs/dataset-stats.md` / `dataset-stats.json`._

## Side by side

| | WildChat-1M | ShareChat (5 platforms) |
|---|---|---|
| Conversations | 837,989 | 129,584 |
| Unit in raw file | one row / conversation | one row / **message** (group by `url`) |
| Mean turns/conv | 2.34 | 1.66 (Perplexity) – 5.25 (ChatGPT) |
| Single-turn share | 60.4% | 41–62% by platform |
| Languages | 74 | 29–143 by platform |
| Time span | 2023-04 → 2024-04 | 2023 → 2025 |
| Models | GPT-3.5 / GPT-4 only | ChatGPT, Claude, Grok, Perplexity, Gemini |
| AI internal state | none | **`thinking` (Claude ~29%; Grok ~0.3%)** |
| Sampling | unsolicited, unfiltered | post-hoc **shared URLs** |

Per-platform ShareChat: ChatGPT 94,086 convs (mean 5.25 turns), Perplexity 14,612 (1.66),
Grok 13,149 (3.76), Gemini 6,826 (4.96), Claude 911 (4.59).

## What actually differs (and the confounds)

1. **Platform is entangled with time period.** ShareChat's non-ChatGPT platforms are largely
   2025-era; WildChat is entirely 2023–24 GPT-3.5/4. Any failure-rate or behavior difference
   between the corpora conflates **model/platform** with **calendar time** (frontier models
   improved a lot in between — the predecessor itself found failure rates dropped with newer
   models). ⇒ Do **not** read cross-corpus differences as caused by either factor alone.

2. **Length skew is bimodal, not "short snippets."** ShareChat has a large single-turn mass
   (41–62%) *and* a heavier multi-turn tail than WildChat (higher means; max 851/1337 turns).
   Shared sessions skew toward either quick showcases or substantive long sessions, not the
   middle. WildChat is flatter and shorter (mean 2.34, 60% single-turn). (Corrects an earlier
   "short showcase" note in `dataset-stats.md`.)

3. **Selection bias differs in kind.** WildChat captures whatever real users did (incl. boring,
   failed, abandoned sessions). ShareChat captures what users *chose to publish* — a filter
   plausibly correlated with *success/impressiveness* and against *quiet failure*. This directly
   threatens the visible/invisible-failure ratio (the predecessor's headline), so ShareChat is
   **not** a safe substrate for estimating failure prevalence.

4. **Language coverage** is broader on ShareChat-ChatGPT (143 langs) but the data is
   language-*filtered* (8,842 convs dropped); WildChat spans 74 with English 57% / Chinese 14% /
   Russian 10%.

## Coupling-relevance: what each corpus is good for

- **WildChat = the human-side & repair workhorse.** Real users at scale, with genuine
  corrections, frustration, abandonment, and multi-turn repair — and it already carries the
  predecessor's annotations (conversation-level on 100k; per-conversation signal summaries on the
  ~10k calibration set). Best substrate for the **Human→AI** and **shared-control/repair** axes,
  caveated to 2023-era models.
- **ShareChat = the AI-internal-state probe.** Its unique asset is Claude **`thinking`** traces:
  the only place we can compare what the model *reasoned* against what it *surfaced* — the
  **AI→Human** disclosure gap. This is a **small, qualitative, Claude-only** sample: the Claude CSV
  is **8,364 rows** (4,182 user + 4,182 llm; **not** 123.8k), and the `thinking` column is a
  python-repr dict whose `content` is **either** Claude.ai's *summarized* extended-thinking **or** a
  tool / web-search Request/Response dump. The genuine-reasoning subset is **1,008 turns across 254
  conversations** — good for close reading, not large-scale statistics. **CORRECTION (2026-06):** the
  earlier "reasons ~2× as much as it surfaces (ratio 2.02; 74.9%)" measure was an artifact of counting
  the tool-JSON blobs as reasoning. On the genuine-reasoning content the median reasoning/surfaced
  ratio is **0.84** (only 43% reason longer than they surface) — the disclosure gap is a **content**
  gap, not a length gap, and is measured directly in W2 (`../shared-findings.md`). Secondary value:
  multi-platform behavior contrast (with the time confound noted). A non-trivial slice is genuinely
  **agentic** — **278 tool-using turns across 162 convs** (W2b, `../shared-findings.md`), including
  **consequential / irreversible** actions (`write_file`, `execute_command`+`gh push`,
  `create_payment_intent`, Cloudflare DB mutations, `deploy_app`). This is a small real-world preview
  of the tool-using target where the codebook's action column is *visible but oracle-less*.

## Implications for Phase 1

- Use **WildChat + predecessor signal summaries** as the primary corpus for coupling-lens reading
  (Step 3, Human→AI and repair).
- Use the **ShareChat Claude `thinking` subset** as a targeted qualitative probe of the AI→Human
  disclosure gap (Step 3).
- Treat any WildChat↔ShareChat numeric difference as **descriptive only** — never causal — given
  the platform×time confound and shared-URL selection bias.
- Neither corpus has tool actions / shared state ⇒ the action/consequence axis stays empty here,
  feeding directly into the Step 5 collection requirements.
