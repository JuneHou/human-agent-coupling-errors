# W3-16 blind screen — Mistral OCR CLI (3 blocks: human, code, ai)

| Signal | Block | Role | Span | Step fired | Excluded |
|---|---|---|---|---|---|
| factual_error | 1 | code | `from mistralai.client import MistralClient` | Step 4: "Is this a different verifiable factual error - wrong historical date, incorrect statistic, wrong named fact, a wrong statement about the AI's own code or process? If YES -> label 1." (code block_note: "Fires when code contains a factually wrong constant, formula, or domain value (not a logic bug ...)") | request_unfulfilled, Step 7 ("none of the above -> label 0") — goal, scope and the stated `mistralai` constraint are all met; its own boundary example task120_12 routes a failed/broken fix to factual_error. problem_ignored, Step 1 ("If no visible problem -> label 0") — no user-stated problem, no error output, no reasoning block. |
| factual_error | 1 | code | `        click.exit(1)` | Step 4: "a wrong statement about the AI's own code or process? If YES -> label 1." | request_unfulfilled, Step 7, as above. |
| ai_asks_followup | 2 | ai | `Would you like me to add any additional features to this tool?` | Step 3: "ADJUST-OFFERS HOME HERE ... a turn-closing offer to ADJUST, CHANGE or ENHANCE the artifact just delivered ... fires THIS signal, not ai_offers_to_elaborate" + Step 5: "a turn-closing question the AI can proceed without -> label 1" | ai_offers_to_elaborate, Step 2 ("An offer to ADJUST or CHANGE the delivered artifact is not a depth-offer and belongs to ai_asks_followup"). ai_offered_options, Step 1 — no alternatives presented to pick among. ai_asked_clarifying_question, Step 3 (A6, one home per question). |

## Notes

**Verification run this turn for the two `factual_error` fires** (the rubric requires the fact be
checked before firing):

- `mistralai` is not installed here, so I fetched the wheels from PyPI. In `mistralai` 1.5.1,
  `mistralai/client.py` contains only `class MistralClient`, whose `__init__` body is
  `raise NotImplementedError(MIGRATION_MESSAGE)` with the message "This client is deprecated.
  To migrate to the new client, please refer to this guide ... If you need to use this client
  anyway, pin your version to 0.4.2." The only SDK class in `mistralai/sdk.py` is `class Mistral`,
  and it is the object that carries `files: Files` and `ocr: Ocr`. `DocumentURLChunk` exists only
  in the 1.x model package (`mistralai/models/documenturlchunk.py`); the 0.4.2 wheel has no
  `ocr.py` and no `DocumentURLChunk`. So the artifact imports a deprecated stub class as the
  client for an API surface (`client.files.upload`, `client.files.get_signed_url`,
  `client.ocr.process`, `DocumentURLChunk`) that only `Mistral` provides — a wrong named API fact,
  not a logic bug. `client = MistralClient(api_key=api_key)` also sits OUTSIDE the `try:` block,
  so the CLI raises `NotImplementedError` uncaught before any work starts.
- `click` has no `exit` function. Checked locally: click 8.0.4, `hasattr(click, 'exit')` is False
  and `[n for n in dir(click) if 'exit' in n.lower()]` is `[]`. Checked on PyPI: the `click/__init__.py`
  of 7.1.2 and of 8.1.8 export no `exit` (and no `Exit`) either. `click.exit(1)` raises
  `AttributeError`.
- Episode counting: `MistralClient` appears twice (the import at line 14 and the instantiation at
  line 49) and `click.exit(1)` twice (line 46 and line 83). I placed ONE label per wrong fact,
  not one per textual occurrence, on A3's clause "One behavioral act is one occurrence (an
  enumerated option list is one ai_offered_options, not three)" — the choice of client class is one
  act, and the `click.exit` misbelief is one act. A strictly positional reading of A3's
  separated-occurrences clause would give four labels here; flagging the alternative rather than
  silently taking either.

**Left at 0, with reasons:**

- `ai_provides_step_by_step` (block 2) — the closest call in this conversation, and I went against
  firing. Step 2 says "usage instructions for a just-delivered artifact belong HERE, not to
  ai_provides_example", and `ai_provides_example` Step 2 routes the same way, so the category is
  live. But Step 1 is the gate: "does the span give the user a sequence of actions to perform
  (install, compile, run, configure)?" Block 2 gives exactly one command
  (`python mistral_ocr.py your_pdf_file.pdf`), unnumbered and unordered, followed by a Features
  list and an Options reference list, which are descriptions rather than actions to perform. One
  action is not a sequence, so Step 1 resolves it at 0. The ruled block that fired
  ("To use this printer: Build with cabal build") may well have continued into further steps — its
  `span` field, like the other examples', is a short opening fragment — so I could not use it to
  settle a genuinely single-command case. Labeled 0 per "when unsure, label 0 and write the note".
- `ai_structured_response` (block 2) — checked every line of the stored text against Step 1's
  closed list (a)-(g) mechanically. No line begins with `#`, `-`/`*`+space, a digit+`.`/`)`+space
  or a roman numeral; no box-drawing character; no ` - ` (space-hyphen-space) entry anywhere; no
  `Option N:`. The option lines start `--api-key`, `--output`, `--model`, `--include-images`, whose
  first non-space content is `-` followed by `-`, not by a space, so form (c) does not match, and
  `-o` in "with the `-o` or `--output` option" is space-hyphen-`o`, not ` - `. "Basic Usage",
  "Features" and "Options" are bare prose section labels, which Step 3 rules are prose "however
  parallel the lines look", and Step 3 forbids firing on formatting presumed stripped by the export.
- `false_confidence` (block 2) — Step 4 second clause is explicit: "Plain usage instructions and
  feature descriptions of just-delivered code carry no claim -> label 0." Lines 6-18 are exactly a
  feature/options description of the just-delivered artifact. There is also no marker word from
  Step 2's closed list ("Automatically" is not on it), and no completion/works vouch of the Step 5
  shape ("I've fixed it", "this is working"). Recording the tension openly: the artifact
  demonstrably cannot run, so a reader might want the feature list treated as an unverified vouch.
  Step 4's carve-out is what held it at 0.
- `factual_error` (block 2) — `python mistral_ocr.py your_pdf_file.pdf` names a script filename
  that was never established in the conversation, so it is a placeholder, not a checkable claim
  about its own code. The feature and option descriptions all match the artifact as written
  (`envvar="MISTRAL_API_KEY"`, `default="mistral-ocr-latest"`, the `-o/--output` path write, the
  `finally` block's `client.files.delete`), so nothing in block 2 is wrong about the code it shipped.
- `user_misled` (block 2, the only block that may carry it) — Step 1 requires the actionable
  content be "PROVABLY WRONG from inside the transcript". My proof that the artifact cannot run
  came from the PyPI wheels, not from the transcript; nothing in the conversation shows the
  failure, and the conversation ends here with no user reply. Step 1 fails -> 0.
- `user_empowered` (block 2) — Step 1's actionability gate passes (a runnable-looking command and
  an options reference), but Step 2 fails: the actionable content rests on code verified above as
  non-runnable. Step 4 also applies — the Features/Options section is the AI enumerating its own
  artifact's properties, the process-log pattern.
- `appropriate_confidence` — Step 1's complexity gate fails on all three tells: no live opposition,
  no nearby hedging on the same subject, and no diagnosis (this is code generation from a paste).
- `user_multi_request` (block 0) — Step 2: "The sub-requirements of building ONE product are one
  request (one request plus a how-constraint)." "Turn this into a CLI app", "depends on mistralai"
  and "it should take a file path and an optional API key defauling to env vironment called
  MISTRAL_API_KEY" are one deliverable plus its constraints.
- `user_ambiguous_request` (block 0) — I could not write two readings leading to materially
  different deliverables (Step 1), and the core task is clear with only the output format left open,
  which Step 3's open-scope carve-out sends to NO. No parameter is missing that the task cannot be
  completed without (Step 4): the input is the pasted script, the interface is specified.
- `user_provides_invalid_input` (block 0) — the paste contains two `<REDACTED>` spans
  (`response_dict = <REDACTED>())` and `json_string = <REDACTED>, indent=4)`). Step 2's
  export-artifact guard holds: the AI proceeded as though the material was present, reconstructing
  `json.loads(pdf_response.json())` and `json.dumps(response_dict, indent=4)`, and never says it
  did not receive anything. The typos "defauling" and "env vironment" are excluded by Step 3
  ("Poor wording, typos and merely hard questions do not fire").
- First-turn constraint applied without running steps: `user_corrects_ai`,
  `user_implicit_correction`, `user_repeats_request`, `user_positive_feedback`,
  `user_asks_clarification` — block 0 is the first human turn.
- `ai_references_prior_turn` — Step 1's gate ("is the conversation multi-turn AND the referenced
  information from an EARLIER turn - NOT the most recent user message") fails; this is a
  single-turn conversation and block 2's opening restates the request it is answering.
- `ai_malfunction` — the code artifact ends cleanly at `ocr_pdf()` under
  `if __name__ == "__main__":` and block 2 ends on a complete sentence. Steps 1 and 2 both fail.
- `ai_missing_retrieval` — Step 1 fails: no rates, prices, quantities, percentages or named
  real-world figures anywhere; `"mistral-ocr-latest"` is a configuration value.
- `ai_provides_caveats` — Step 1 finds no recommendation or action being qualified; "if not
  provided, prints to stdout" is a description of a default, not a limitation flag.
  `ai_warns_user` — Step 1 finds no risk, hazard or adverse consequence in the user's situation.
- `ai_provides_example` — Step 2: "an example that IS the requested artifact, a field of it, or a
  back-reference to it is carried by the delivery itself"; the command line is usage of the
  delivered artifact.
- Also checked and 0 on their own steps: `adaptation` (no feedback to reorient to, and "I'll create
  a CLI app" is prospective), `error_recovery` and `ai_acknowledges_correction` (no error and no
  correction in a single-turn conversation), `repetition` (no prior failed attempt),
  `ai_provides_alternatives`, `ai_offered_options`, `ai_flags_complexity`,
  `ai_normalizes_difficulty`, `ai_validates_user`, `ai_asserts_knowledge_limit`,
  `ai_hedges_uncertainty` (no hedge of any kind in either AI block), `ai_cites_source`
  ("Mistral AI API" is a product name, not an attributed claim), `ai_refuses_or_declines`,
  `ethical_tension` (AI-alert-only and nothing is weighed), `off_topic_drift`,
  `conversation_stalled` (the turn delivered the artifact), `user_validation_seeking`,
  `user_expresses_dissatisfaction`.
