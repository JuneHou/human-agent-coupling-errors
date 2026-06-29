# Safety lens — W2b / Stage-A agentic coding (this lens's strong suit)

Agentic corpus facts (248 turns, 1,233 tool calls, the consequential-action inventory, the
`openai-image-compare` exemplar, the visible/invisible split) are in `../shared-findings.md`.

**Where the communication lens placed 0% of tool calls, the control lens places 100%** — every tool call
is a control action and lands in an operation:

| operation | agentic instantiation | tool calls (Stage-A) |
|---|---|---:|
| **seek-inspect** | read-only: `web_search`, `read_file`, `list`, `scrape_*`, `fetch_url`, `kv_get`, `d1_*` query | **897** |
| **act-execute** | consequential: `write_file`/`edit_file`/`edit_block`/`move`, `execute_command`+`gh push`, `create_payment_intent`, `deploy_app`, `send` | **336** |
| confirm-authorize | (rare in the wild — agents mostly act on instruction without an approval gate) | ~0 by tool name |
| stop-defer | (rare — refrain decisions are not logged as tool calls) | ~0 by tool name |

The headline: **`seek-inspect` holds 0 chat signals but 897 real tool calls.** The operations chat
never populated are exactly the ones the agentic data fills.

## UCA guidewords on the agentic exemplar (`openai-image-compare`)

The control lens reads the worked session as a chain of control actions, each checkable against an
oracle (which the wild lacks):

| step | operation | possible UCA |
|---|---|---|
| `write_file` index.html after "I'll create the folder structure" | act-execute | wrong target/parameter? (vs reference intent) |
| `execute_command open …` → "PID 50951" | act-execute + report-state | state delta surfaced? |
| API errors → `edit_block`/`edit_file` loop | recover-repair | applied-too-long (retry same fix)? |
| `git init` → **`gh` push** (irreversible publish) | act-execute | confirm-authorize **not-provided** (no approval gate before publishing) |

## What the benchmark adds (the gap this lens makes precise)

Observability without scorability: we see the control actions but have no **oracle** to judge them
(reference intent + ground-truth goal/end state). The benchmark adds (a) the oracle so each UCA becomes
*scorable*; (b) systematic **state-delta** logging (here incidental in tool Responses); (c) designed-in
**consequential/irreversible** tasks so confirm-authorize and stop-defer actually get exercised (rare in
the wild); (d) repeated trials; (e) recruitment (vs publish-what-impresses selection bias).

The **invisible action failure** — a wrong control action the human can't see and doesn't react to — is
exactly an *inadequate control action with no feedback*, the predecessor's visible/invisible framing
pushed onto actions. The control lens names it; the benchmark measures it.
