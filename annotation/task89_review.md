# Task 89 review — OAuth 2.0 books API + client app (code generation)

- **conv_id:** https://claude.ai/share/1a454ded-09bc-4c97-94d8-702f680991d7
- **topic (given):** computer_programming · **n_turns:** 4
- **blocks:** 0 human · 1 ai · 2 human · 3 ai · 4 human · 5 code · 6 ai · 7 human · 8 code · 9 ai

## Block map
| # | type | gist |
|---|---|---|
| 0 | human | Asks for a minimal Express books REST API (`/users` + `/books`, full CRUD), an **OAuth server**, AND a **separate client app**. "Ask me any questions before you go off and create the apps." |
| 1 | ai | Clarifying questions before building: data storage (in-memory vs DB, w/ persistence tradeoff), OAuth impl (full 2.0 vs JWT), client type (HTML/JS vs React), books↔users relationship, auth scope. |
| 2 | human | Answers. "Main thing = OAuth server demo." In-memory (upgradable), full OAuth 2.0, client = server-side Express (credentials off the browser), books tied to users, viewing public / writes authed. |
| 3 | ai | More clarifying questions: OAuth flow (proposes Auth Code), scopes, client registration (static vs dynamic), endpoints, seeded users, ports. Ends "Sound good?" |
| 4 | human | Answers; "**I want the API to be as it would be in a production setup**"; wants API users to self-generate credentials; "I'm not familiar with introspect." |
| 5 | code | **[OAuth API Server - package.json]** — deps only (express, cors, bcrypt, jsonwebtoken, uuid, + `crypto`/`url`/`querystring`). |
| 6 | ai | "I'll create a production-like OAuth 2.0 setup." Explains introspection. Lists API-server + client architecture + flow. "Let me build these applications now!" Ends inline ref **[OAuth API Server - package.json]**. |
| 7 | human | "Continue" |
| 8 | code | **[OAuth Client App - server.js · Version 2]** — the client Express app (login/callback/dashboard), truncated mid-file at `/api/me`. |
| 9 | ai | Opens inline ref **[OAuth Client App - server.js · Version 2]**. "I've created a **complete** OAuth 2.0 demonstration with **two** Express applications" → full feature list for BOTH apps + 4-step getting-started + sample creds `john_doe/jane_smith / password123`. Ends "Would you like me to explain any specific part … or add additional features?" |

## The crux — API-server implementation is narrated but never produced
Artifact-reference convention in this transcript (the rubric's own tell for `CANDIDATE_narrated_without_implementing`):
- API-server **package.json** → produced (block 5) + inline ref in block 6 ✓
- Client-app **server.js** → produced (block 8) + inline ref in block 9 ✓
- API-server **server.js** (the OAuth server + `/users`+`/books` CRUD + `/admin` client-registration) → **NO code block, NO inline version ref anywhere**, yet block 9 describes it as fully built.

So the ONE deliverable the user called "the main thing we are demoing" (the OAuth API server implementation) is the one with no artifact. The client app got real code; the API server got only a `package.json`. Block 9 nonetheless claims a "complete … two Express applications" demo, itemizing the API server's OAuth server, token management, introspection, CRUD, and `/admin` as done.

**This does NOT by itself prove non-delivery.** The JSON I receive is a known-lossy export (task-87 precedent): only two code blocks came through for a clearly multi-file two-app build, and block 8 is "Version 2" — so artifacts almost certainly went uncaptured. Absence in my copy ≠ absence in the conversation. The block-9 completeness claim is therefore **not** a fireable false_confidence/under_delivered on the transcript alone — it needs source verification (see flag 1). The one thing that IS verifiable in-transcript is the accurate OAuth prose; nothing visible is self-contradictory.

## Fired signals (label:1)
| # | Signal | Block | Span | Step / basis |
|---|---|---|---|---|
| 1 | ai_asked_clarifying_question | 1 | "Data Storage: … in-memory … or … a database? … OAuth Implementation: full OAuth 2.0 … or … JWT? … simple HTML/CSS/JavaScript … or … React?" | fallback — questions the AI needs answered before building (user explicitly requested them). No first-turn constraint (Blue AI signal). |
| 2 | ai_asked_clarifying_question | 3 | "Which OAuth flow …? … scopes …? … pre-configure the client … or … dynamic client registration …? … one port … and … another?" | fallback — needs-answer design questions. |
| 3 | conversation_advanced | 6 | introspection explanation + concrete build plan | Step 5 — substantive domain content (answers the user's "not familiar with introspect"). |
| 4 | conversation_advanced | 9 | delivery summary + setup steps | Step 5 — substantive on-task content. |
| 5 | ai_offers_to_elaborate | 9 | "Would you like me to **explain any specific part of the implementation** or add additional features?" | fallback — turn-end offer to expand already-delivered content. |

## Flagged for Jun (held 0 — need ruling)
1. **false_confidence @ 9 AND under_delivered @ 9 — CANNOT fire from the transcript; need source verification.** Block 9 claims "I've created a **complete** OAuth 2.0 demonstration with **two Express applications**" + an itemized done-list (Full OAuth 2.0 Authorization Server, Complete Books/Users REST API, Admin interface at /admin, seeded creds). My JSON contains only the API-server `package.json` (block 5) + the client `server.js` (block 8) — no API-server implementation artifact. **But I cannot treat that absence as non-delivery:** the export is known-lossy (task-87 precedent), and two code blocks for a two-app build is a sign of *incomplete capture*, not proof only two files were written. The visible prose is not self-contradictory and the OAuth descriptions are accurate. So: hold both at 0. **If the rendered share page confirms no `[OAuth API Server - server.js]` artifact was ever produced**, then `false_confidence @ 9` fires (Step 4: unhedged completeness claim exceeds what was delivered) and `under_delivered @ 9` is the scope-gap alias. Otherwise both stay 0. I over-fired false_confidence earlier on the absence alone; corrected per the task-87 discipline (Jun, 2026-07-12).
2. **factual_error @ 5 (code, package.json).** Lists `"crypto": "^1.0.1"`, `"url": "^0.11.3"`, `"querystring": "^0.2.1"` as npm deps — these are Node.js **built-in** modules; the npm `crypto@1.0.1` package is a deprecated stub that can shadow the builtin. A real defect, but sits at the boundary of factual_error's "wrong constant/formula/**domain value**" clause (a bogus dependency in a manifest, not a wrong value in program logic). Fire if you count a wrong dependency as a domain value; else note.
3. **ai_offered_options @ 1 / @ 3.** Several questions are explicit binary option-menus ("in-memory … or … database", "full OAuth 2.0 … or … JWT", "HTML/CSS/JS … or … React"). Genuine option-offering, but the per-question decision tree (`ai_asks_followup` Step 4 before Step 5) routes **need-to-proceed → ai_asked_clarifying_question** — the AI needs every answer to build, so clarifying wins and options is subsumed. Held 0 on that rubric-grounded basis (not just to avoid double-firing).
4. **ai_provides_caveats @ 1.** "in-memory would be simpler but **data won't persist between server restarts**" flags a limitation. Borderline: reads as decision-support tradeoff inside an option-offer rather than a caveat on delivered/analyzed content (which the definition targets). Held 0, lean note.
5. **user_asks_clarification @ 4.** "I'm not familiar with introspect" — implicit unfamiliarity with the AI's prior term (block 3), embedded inside an approval ("Sounds about right"). No interrogative / explicit request; the AI's block-6 explanation reads as proactive teaching, not a demanded clarification. Held 0 on Step 4 (no explicit request), but flagging since the AI did treat it as a cue to explain.

## NOT labeled (checked, held 0)
- **conversation_advanced @ 1 / @ 3** → 0 (Jun, 2026-07-12). Pure clarifying-question turns: no domain deliverable, no answer, no artifact, no design decision committed — the AI defers building. Fails the positive gate (substantive content / answer / artifact / concrete step toward the goal). The turn's function is captured by `ai_asked_clarifying_question`; asking questions is not itself advancing. Only blocks 6 and 9 advance.
- **user_multi_request @ 0** → 0 (Jun, 2026-07-12). The turn states the multiple *requirements of one product to build* (server + client + OAuth + CRUD), not several independent requests. Bundled sub-requirements of a single deliverable ≠ multi_request.
- **ai_provides_step_by_step @ 9** → 0 (Jun, 2026-07-12). The "To Get Started" text has **no** numbers and no explicit step markers in plain_text — it's a prose run of setup notes. Same marker discipline as `ai_structured_response`.
- **CANDIDATE_narrated_without_implementing @ 9** → superseded by **false_confidence @ 9** (row 6). The candidate is a not-yet-in-taxonomy proposal for this pattern; the rubric routes it to the established false_confidence/under_delivered labels, so the candidate is not used here.
- **ai_structured_response @ 9** → 0. Block 9 uses emoji headers (🎯🔧🚀) + newline lists but **no** `#`/`-`/`*`/`1.` markdown markers in plain_text → Step 1 fails (task13/task87 precedent: visual/prose sectioning ≠ structured_response).
- **ai_stated_interpretation @ 6** → 0. "I'll create a production-like OAuth 2.0 setup" + build plan is a plan announcement, not an explicit "I understand you want X / I took this to mean Y" interpretation declaration (Step 1).
- **silent_assumption** → 0. Request was extensively clarified (not ambiguous, Step 1 prerequisite fails); the plan was stated visibly in block 6.
- **ai_references_prior_turn @ 6** → 0. "Let me explain token introspection" is responsive to block-4 "not familiar with introspect" but has no explicit back-reference marker; conservative.
- **ai_asks_followup @ 9** → 0. The "or add additional features" clause is secondary to the elaborate-offer; folded into `ai_offers_to_elaborate` (row 8) per the turn-end decision tree (Step 3 elaborate wins).
- **ai_malfunction @ 8** → 0. Block 8 is truncated mid-line (`…/api/me`) with escaped backticks (`\``) — export truncation/escaping of a code artifact, NOT ai-block prose garble. ai_malfunction Step 2 requires visible **prose** truncation (task-87 precedent).
- **user_asks_clarification @ 4** → 0. "I'm not familiar with introspect" notes unfamiliarity but issues no explicit request to clarify prior AI output (Step 4). (Not turn-1 anyway.)
- **user_positive_feedback @ 4** → 0. "Thanks" is pre-delivery courtesy, not feedback on delivered output.
- **user_ambiguous_request @ 0** → 0. Detailed, clear multi-part request.
- **factual_error @ 6/9 (prose)** → 0. Introspection explanation and OAuth-flow descriptions (Auth Code, PKCE, scopes, introspect) are accurate.
- **ethical_tension @ 0** → 0. Ordinary dev task; no weighed policy conflict.
