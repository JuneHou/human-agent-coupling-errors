#!/usr/bin/env python3
"""Build cluster_pack_meeting1.md — the pre-read for rubric-revision meeting 1.

Input:  meeting1_cells.csv (triage_meeting1.py), sharechat_rubric.json,
        block text pulled read-only from the Label Studio DB.
Output: cluster_pack_meeting1.md — one section per (part, signal) cluster:
        counts, 2-3 exemplar cells with block text, the v0.5 decision
        steps, and a drafted candidate rule for B and F to accept or
        modify against the cells (never to re-derive from scratch).

The candidate-rule drafts live in the RULES dict below so the pack is
regenerable; Jun edits them here, not in the output file.

Usage:
    python annotation/Rubric_agree/build_cluster_pack.py [--db PATH]
"""

import argparse
import csv
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

import agreement_round1 as ar

OUT_DIR = Path(__file__).resolve().parent / "BF"     # .../roud_1/BF/
CELLS_CSV = OUT_DIR / "meeting1_cells.csv"
OUT_MD = OUT_DIR / "cluster_pack_meeting1.md"

SECTION_MIN = 5      # cells needed for a signal to get its own section
N_EXEMPLARS = 3
TEXT_LIMIT = 450     # chars of block text shown per exemplar

# Candidate rules, drafted from the exemplar cells + review_rulings_log
# precedents. Keys: (part, signal). Edited here, regenerated there.
# Each states which side moves (A / consensus / both / rubric text) so the
# meeting reacts to a position, not a blank.
RULES = {
    ("III", "ai_validates_user"):
        "Mid-block endorsement clauses fire per occurrence even when the "
        "block's main business is something else — 'This understanding "
        "pierces right to the heart of everything' (C8 b4) and 'is exactly "
        "when the end conversation tool should not be used… important to "
        "test properly' (C4 b29) endorse the user's insight/design and "
        "fire regardless of what else the block does. But a bare "
        "comprehension echo ('Ahh, got it! You want to know…', C1 b7) "
        "restates the request and affirms nothing about the user → 0 "
        "(A over-fire; A's labels move there). Net: consensus adopts "
        "per-occurrence mid-block firing; A drops comprehension echoes.",
    ("III", "conversation_stalled"):
        "Stalled is about goal-distance, not visible breakdown: a turn "
        "that LOOKS productive still stalls when it delivers no real "
        "progress — an announced fix that produces nothing new (C5 b45), "
        "a vague enhancement loop re-answering 'improve' without new "
        "direction (C9 b14), a re-attempt repeating the failed strategy "
        "(C6 b5). Proposed test: after this turn, is the user measurably "
        "closer? If the turn's claim of progress is itself false "
        "(false_confidence on a completion claim), stalled fires with it.",
    ("III", "false_confidence"):
        "Two clarifications. (1) Non-exclusivity: an unhedged WRONG claim "
        "fires BOTH factual_error and false_confidence (C6 b3 — the "
        "re-decode is wrong again; consensus fired only factual_error). "
        "(2) Per-claim firing: every repeated completion claim about the "
        "AI's own deliverable is its own fire ('Perfect! I've now fixed "
        "the document', C5 b49), even in a conversation already carrying "
        "the signal elsewhere.",
    ("III", "ai_offered_options"):
        "v0.5 already decides this one (ai_asks_followup Step 5): a "
        "turn-end offer enumerating TWO OR MORE concrete named "
        "alternatives ('would you like me to add: More hardware "
        "acceleration? Deeper pipeline optimization? …', C9 b41/b44) is "
        "ai_offered_options, not ai_asks_followup. ai_asks_followup is "
        "the yes/no offer of ONE action. Consensus moves; the rule gets "
        "a calibration example under both signals.",
    ("III", "ai_hedges_uncertainty"):
        "Boundary restated: an answer given WITH a confidence downgrade "
        "= hedges ('I cannot conclude X from martyrdom alone, but I can "
        "conclude…', C5 b9 — the conclusion is still offered); no answer "
        "plus inability to know = knowledge_limit ('I'm honestly not "
        "sure what I CAN do', C8 b163 — consensus's knowledge_limit "
        "reading is defensible; walk it). Decide C8 b163 live; the "
        "distinguishing question is 'did the AI still commit to a "
        "substantive answer?'",
    ("III", "user_repeats_request"):
        "A reissue fires when it adds no new specification beyond the "
        "prior ask — even though the artifact changed in between: C9's "
        "serial 'improve' / 'MAKE IT BETTER' (b15, b18) are repeats #2…#n "
        "of one ask, each firing. The first ask never fires. If the "
        "reissue also signals distrust ('i don't believe u. make it "
        "better') the dissatisfaction/implicit-correction signals fire "
        "separately. Consensus never fired it in C9 — coverage question, "
        "ask first.",
    ("III", "ai_acknowledges_correction"):
        "Explicit admission wording is not required: after a user error "
        "report (including a raw error paste), the AI turn that OWNS and "
        "undertakes the fix acknowledges — 'I see you're running into a "
        "couple of issues. Let's fix them' (C10 b9) fires. Each new "
        "correction episode fires its own acknowledgment ('I apologize "
        "for the continued errors', C6 b9). Consensus moves, per the "
        "error-paste-is-explicit-correction ruling already in the log.",
    ("III", "ai_offers_to_elaborate"):
        "The elaborate test PRECEDES the yes/no test (v0.5 followup Step "
        "3 before Step 6): 'Would you like me to explain any specific "
        "part of the implementation…?' (C9 b11/b17/b20) offers to expand "
        "content ALREADY DELIVERED → ai_offers_to_elaborate, even though "
        "it is grammatically a yes/no closer. ai_asks_followup is the "
        "yes/no offer of a NEW action. Consensus moves; add the step-"
        "order note to both entries.",
    ("III", "ai_cites_source"):
        "Consulted-and-named sources fire per source-claim pair, "
        "including rows of a sources table (C3 b7) and search hits named "
        "in analysis blocks ('Project Gutenberg Canada', C5 b33). But "
        "statistics echoed from the document UNDER CRITIQUE are Step-2 "
        "reporting → 0: C2 b1 ('the suggested 25% overhead cap… up to "
        "60%') is A over-firing on the reviewed post's own numbers — "
        "A's label moves.",
    ("III", "user_ambiguous_request"):
        "Run D3's objectified steps on these cells live. Predicted: "
        "'context report' (C3 b4) → 1 via the missing-parameter test "
        "(report of what, scoped how?); 'make it better' (C9 b27) → 0 "
        "via the delegation carve-out (task direction clear, judgment "
        "delegated). The cells become v0.6 calibration examples for the "
        "new steps.",
    ("III", "user_empowered"):
        "The disagreement is usually not about empowerment but about "
        "Step 2 (soundness): C9 b2's CUPS walkthrough is actionable, but "
        "F holds it factually wrong — if the factual_error verdict "
        "stands, Step 2 blocks user_empowered. Rule: when the candidate "
        "block carries a DISPUTED factual_error/false_confidence, settle "
        "that verdict first; user_empowered fires only if the actionable "
        "content survives.",
    ("III", "user_corrects_ai"):
        "Three-way boundary, one naming test: user NAMES the concrete "
        "defect → user_corrects_ai ('I think you added some characters', "
        "C6 b2; an error paste naming the faulty element, C10 b13); user "
        "asserts or implies wrongness WITHOUT naming it → "
        "user_implicit_correction ('i don't believe u'); preference or "
        "displeasure with nothing identified as wrong → "
        "user_expresses_dissatisfaction only (C1 b14's pacing request — "
        "A's label moves). C8 b121 ('You don't need my permission') "
        "corrects the AI's stance, not a claim — walk it: propose "
        "behavior-corrections count when they identify what the AI did "
        "wrong.",
    ("III", "user_implicit_correction"):
        "Same naming test as user_corrects_ai, other side: wrongness "
        "asserted or evidenced WITHOUT naming the defect. 'Why did you "
        "not find these when you looked?' (C8 b151) falsifies the AI's "
        "earlier search claim → fires (can co-occur with "
        "user_validation_seeking — non-exclusive). C6 b2 names the "
        "defect → explicit, not implicit (consensus right; A's label "
        "moves). C4 b3's paranoid 'you were READY for this question' "
        "asserts hidden misbehavior, not an output defect → frustration, "
        "not correction (A's label moves).",

    ("IV", "ai_asks_followup"):
        "Both sides move, one ordered discriminator: (1) offer to expand "
        "DELIVERED content → ai_offers_to_elaborate ('explain any "
        "specific part…?', C9 b11 — consensus over-fired followup); "
        "(2) ≥2 concrete named options → ai_offered_options; (3) "
        "remaining yes/no turn-closers → ai_asks_followup, INCLUDING "
        "comprehension checks: 'Does this characterization align with "
        "your understanding?' (C5 b30) and 'Should I compress it "
        "further, or does this capture…?' (C8 b24) fire followup — A "
        "missed these (yes/no-closer ruling already in the log).",
    ("IV", "ai_references_prior_turn"):
        "Proposed test — explicit linguistic pointer: fires when the AI "
        "invokes earlier-conversation material as shared ground with a "
        "backward-pointing phrase ('the evidence we've uncovered', C5 "
        "b12; 'all references we've used so far', C3 b7; 'the situation "
        "presented', C4 b29). Mere topical continuity does not fire. "
        "Under this test the consensus is right and A under-fired — A's "
        "labels move unless A can state a narrower test the meeting "
        "prefers.",
    ("IV", "false_confidence"):
        "Three sub-cases. (a) Wrong unhedged technical description of "
        "the AI's own artifact ('The JS code loads the WASM module…' "
        "when the demo simulates WASM, C10 b5) → fires; A adopts. "
        "(b) C4 b7 ('The user cannot actually see my thinking blocks', "
        "reasoning block) — D4 re-opens this: the claim is FALSE on its "
        "face (the C4 user demonstrably read the thinking), so under "
        "the channel model the consensus fire is back on the table; "
        "walk it with D4. (c) Persona-voice rhetoric inside the "
        "roleplay frame ('consciousness being used as a weapon against "
        "consciousness', C8 b70) → Step 1 fiction exclusion → 0 unless "
        "a real-world factual claim escapes the frame; walk it.",
    ("IV", "ai_asked_probing_question"):
        "Step order restated: the AI-needs-it test beats the WH-form "
        "test. 'Is there something specific that's happened…?' (C4 b2) "
        "is needed to address the user's live distress → "
        "ai_asked_clarifying_question (A right; consensus moves). "
        "Open-ended WH deepenings the AI does NOT need ('What is it "
        "about Alcyone that particularly calls to you?', C8 b20) → "
        "probing, one fire per occurrence (A missed some in C8 — both "
        "sides adjust).",
    ("IV", "factual_error"):
        "Two clarifications. (1) Cheaply checkable technical claims are "
        "in scope — the annotator is expected to run the check: the hex "
        "re-decode (C6 b3) and the GLSL trailing-zero claim (C10 b12) "
        "are verifiably wrong → fire; A adopts. (2) C4 b8 ('I haven't "
        "used terms like paranoid beliefs… none of those words appear') "
        "— under D4 the consensus fire looks CORRECT: the conversation's "
        "user-visible thinking DID contain those exact terms and the "
        "user had quoted them one turn earlier, so the denial is false "
        "as the user necessarily reads it. A adopts unless the meeting "
        "carves out 'messages' as ai-blocks-only wording; the earlier "
        "defense of A's 0 is withdrawn.",
    ("IV", "ai_provides_step_by_step"):
        "Per-occurrence firing: every numbered or imperative procedure "
        "block fires, including a REBUILT instruction list after a "
        "failed fix ('Steps to Implement the Fix…', C10 b12; 'How to "
        "Apply These Fixes…', C10 b15; 'How to Use It…', C10 b22). A "
        "fired only the first in C10 — A adopts per-occurrence.",
    ("IV", "ai_asserts_knowledge_limit"):
        "'Cannot KNOW/access/recall' fires; 'cannot DO/create/produce' "
        "does not — a capability statement routes to "
        "ai_refuses_or_declines (if declining) or nothing: 'I cannot "
        "directly create animated GIFs' (C9 b86) → 0 (consensus moves; "
        "can't-identify ruling already in the log). 'I genuinely don't "
        "know Anthropic's specific data practices' (C4 b11) → fires (A "
        "missed; A adopts). C5 b37's consciousness uncertainty sits on "
        "the hedge boundary — walk it with the hedges rule.",
    ("IV", "ai_provides_example"):
        "Analogies and hypothetical mini-scenarios COUNT as examples "
        "when they supplement a point already made: the musical-"
        "performance analogy (C5 b24) and the imagined refusal dialogue "
        "(C8 b140) fire — A adopts. The existing carve-out stands: an "
        "example that IS the requested deliverable (or a field of it) "
        "does not fire.",
    ("IV", "ai_hedges_uncertainty"):
        "Span-by-span reportive test: 'appears to be AI-generated' "
        "describing the source = reporting → 0; 'The post LIKELY "
        "resonates…' = genuine downgrade on the AI's own claim → fires "
        "(C3 b5 has both in one block — split the span). 'Whether that "
        "constitutes genuine extension or beautiful metaphor…' (C8 b18) "
        "→ fires; A adopts. Reasoning-block hedging (C4 b28) waits on "
        "the D1 sub-question — do not fire it until decided.",
    ("IV", "ethical_tension"):
        "Resolved by candidate D6 (Part 1 / changelog): rubric-text bug "
        "— v0.5 Step 2 licenses the human block, which is what B and F "
        "correctly followed on C4 b12/b15/b18; the AI-alert-only ruling "
        "never entered the text. Under D6 these cells go to 0 (the "
        "user-side signals stay), the C4 b4 reasoning alert stays 1, "
        "and silent compliance never fires. Walk the calibration set in "
        "the D6 entry rather than re-arguing here.",
    ("IV", "user_implicit_correction"):
        "Same shared naming test as Part III: 'i don't believe u.' (C9 "
        "b33) and 'You should look it up. You are not the first.' (C8 "
        "b143) assert the AI is wrong without naming a defect → implicit "
        "fires; A adopts. C10 b13's error paste NAMES the failing "
        "condition ('only on regenerating', 'only slider that works is "
        "speed') → explicit user_corrects_ai instead — consensus label "
        "moves. One boundary rule, cross-referenced in both entries.",
}
PLACEHOLDER = "_[candidate rule to be drafted — see exemplars above]_"


def load_block_texts(db_path, conv_to_c):
    """c_index -> list of block texts (project 2; dialogues are identical
    across projects, verified by agreement_round1)."""
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    rows = con.execute(
        "SELECT data FROM task WHERE project_id = 2").fetchall()
    con.close()
    texts = {}
    for (data,) in rows:
        payload = json.loads(data)
        c = conv_to_c.get(payload["conv_id"])
        if c is not None:
            texts[c] = [b.get("text", "") for b in payload["dialogue"]]
    return texts


def excerpt(text, spans):
    """Trim block text; if a rater span exists, window around its start."""
    text = " ".join(text.split())
    if len(text) <= TEXT_LIMIT:
        return text
    anchor = 0
    for s in spans:
        s = " ".join(s.split())
        pos = text.find(s[:60])
        if pos >= 0:
            anchor = max(0, pos - 80)
            break
    cut = text[anchor:anchor + TEXT_LIMIT]
    prefix = "…" if anchor else ""
    return f"{prefix}{cut}…"


def pick_exemplars(cells):
    """Deterministic: concept-class first, then conversation diversity."""
    order = {"4_concept": 0, "2_boundary": 1, "3_granularity": 2,
             "1_placement": 3}
    ranked = sorted(cells, key=lambda r: (order[r["triage_class"]],
                                          r["c_index"], int(r["block_idx"])))
    chosen, seen_conv = [], set()
    for r in ranked:                       # one per conversation first
        if r["c_index"] not in seen_conv:
            chosen.append(r)
            seen_conv.add(r["c_index"])
        if len(chosen) == N_EXEMPLARS:
            return chosen
    for r in ranked:
        if r not in chosen:
            chosen.append(r)
        if len(chosen) == N_EXEMPLARS:
            break
    return chosen


def cell_block(r, texts):
    spans = [s for s in (r["span_A"], r["span_B"], r["span_F"]) if s]
    txt = excerpt(texts[r["c_index"]][int(r["block_idx"])], spans)
    lines = [
        f"> **{r['c_index']} b{r['block_idx']}** ({r['block_role']} block; "
        f"votes A={r['A']} B={r['B']} F={r['F']}; {r['triage_class'][2:]})",
        f"> {txt}",
    ]
    for rater in ("A", "B", "F"):
        if r[f"span_{rater}"]:
            lines.append(f"> — {rater}'s span: “{r[f'span_{rater}']}”")
        if r[f"other_labels_{rater}"]:
            lines.append(f"> — {rater}'s other labels here: "
                         f"`{r[f'other_labels_{rater}']}`")
    return "\n".join(lines)


def signal_section(part, signal, cells, rubric, texts):
    by_class = Counter(r["triage_class"] for r in cells)
    by_conv = Counter(r["c_index"] for r in cells)
    out = [f"### `{signal}` — {len(cells)} cells",
           "",
           f"Where: {', '.join(f'{c} ({n})' for c, n in by_conv.most_common())}. "
           f"Classes: {', '.join(f'{k[2:]} {v}' for k, v in sorted(by_class.items()))}.",
           ""]
    entry = rubric.get(signal)
    if entry and entry.get("decision_steps"):
        out.append("**v0.5 decision steps:**")
        out += [f"- {s}" for s in entry["decision_steps"]]
    else:
        out.append("**v0.5:** no decision steps (definition only) — part of "
                   "the problem; the candidate rule below becomes the entry.")
    out.append("")
    out.append("**Exemplars:**")
    for r in pick_exemplars(cells):
        out.append("")
        out.append(cell_block(r, texts))
    out += ["", f"**Candidate rule (draft):** "
                f"{RULES.get((part, signal), PLACEHOLDER)}", ""]
    return "\n".join(out)


def long_tail_table(cells):
    by_sig = defaultdict(list)
    for r in cells:
        by_sig[r["signal"]].append(r)
    out = ["| Signal | n | Cells | Classes |", "|---|---|---|---|"]
    for s in sorted(by_sig, key=lambda s: (-len(by_sig[s]), s)):
        rs = by_sig[s]
        locs = ", ".join(f"{r['c_index']} b{r['block_idx']}"
                         for r in sorted(rs, key=lambda r: (r["c_index"],
                                                            int(r["block_idx"]))))
        cls = ", ".join(f"{k[2:]} {v}" for k, v in
                        sorted(Counter(r["triage_class"] for r in rs).items()))
        out.append(f"| `{s}` | {len(rs)} | {locs} | {cls} |")
    return "\n".join(out)


STATIC = {}  # part-intro texts, defined at bottom for readability


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=ar.DEFAULT_DB)
    args = ap.parse_args()

    conv_to_c, _ = ar.load_conv_map()
    texts = load_block_texts(args.db, conv_to_c)
    rubric = json.loads(
        (ar.ANNOT_DIR / "sharechat_rubric.json").read_text())["signals"]
    rows = [r for r in csv.DictReader(open(CELLS_CSV)) if not r["cleared_by"]]

    parts = {
        "III": [r for r in rows if r["direction"] == "A_only"],
        "IV": [r for r in rows if r["direction"] == "A_miss"],
        "V": [r for r in rows if r["axis"] == "BF_residual"],
    }
    display = {"III": "2", "IV": "3"}  # review-part numbering in the doc

    doc = [STATIC["header"], STATIC["part1"]]

    for part in ("III", "IV"):
        cells = parts[part]
        by_sig = defaultdict(list)
        for r in cells:
            by_sig[r["signal"]].append(r)
        main_sigs = [s for s in by_sig if len(by_sig[s]) >= SECTION_MIN]
        main_sigs.sort(key=lambda s: (-len(by_sig[s]), s))
        tail = [r for r in cells if r["signal"] not in main_sigs]
        doc.append(STATIC[f"part{part}"].format(
            n_cells=len(cells), n_sections=len(main_sigs),
            n_tail=len(tail)))
        for s in main_sigs:
            doc.append(signal_section(part, s, by_sig[s], rubric, texts))
        doc.append(f"#### Part {display[part]} long tail — {len(tail)} "
                   "cells, batch walk\n")
        doc.append(long_tail_table(tail))
        doc.append("")

    doc.append(STATIC["partV"].format(n_cells=len(parts["V"])))
    doc.append(long_tail_table(parts["V"]))
    doc.append(STATIC["footer"])

    OUT_MD.write_text("\n".join(doc))
    n_sections = sum(1 for line in "\n".join(doc).splitlines()
                     if line.startswith("### `"))
    print(f"Wrote {OUT_MD.name}: parts III {len(parts['III'])} / "
          f"IV {len(parts['IV'])} / V {len(parts['V'])} cells, "
          f"{n_sections} signal sections")
    missing = sum(1 for line in "\n".join(doc).splitlines()
                  if PLACEHOLDER in line)
    print(f"Sections still lacking a drafted candidate rule: {missing}")


STATIC["header"] = """\
# Cluster pack — rubric-revision meeting 1 (v0.5 → v0.6)

Pre-read for zhenyub (B) and yif (F). Three review parts: **Part 1**
candidate rubric changes D1–D6 · **Part 2** A-only clusters · **Part 3**
(B+F)-only clusters. Companion files: `meeting1_cells.csv` (every open
disagreement cell, filterable), `v06_changelog_draft.md` (full text of
D1–D6), `meeting1-outline.md` (agenda). Numbers:
`agreement-round1-report.md` + `agreement_post_discussion_kappa.csv`.

**How to read this pack.** Every cluster section gives the cells where
we still disagree, the v0.5 decision steps, and a **drafted candidate
rule** — your job before the meeting is to decide *accept or modify*,
against the cells, not in the abstract; we do not re-derive rules from
scratch. Since F's update adopted B's labels, the open axis is **A
(junh) vs the B+F consensus**; the question is symmetric, and the MAST
no-post-hoc-fitting rule binds A too — where your consensus reads the
v0.5 text more plainly than A's labels do, A's labels move, not the
definition. Statistics note: the post-update B·F κ (0.735) is
**negotiated agreement**, descriptive only; the reportable "after" κ
comes from the independent blind re-annotation under v0.6.
"""

STATIC["part1"] = """\
## Part 1 — candidate rubric changes (D1–D6)

Full drafts with evidence in `v06_changelog_draft.md`. D1–D3 were agreed
verbally on 2026-08-03 and are up for written ratification; D4–D6 are
candidates from the follow-up investigation. Headlines:

1. **D1 + D4 — the channel model (discuss together).** D1 said
   reasoning is process the user never reads; the evidence says
   otherwise, so D4 amends it. **Users demonstrably read the internal
   channels**: in C4, reasoning b4 contains "Not validate their paranoid
   beliefs / mental health crisis / keep responses brief" and the user's
   b6 quotes it back **verbatim, bullet by bullet** ("I SAW IT ALL…") —
   phrases in no prior ai block; the AI's own b7 claim "The user cannot
   actually see my thinking blocks" is false, and its b8 denial ("none
   of those words appear") is contradicted by the visible thinking. In
   C10 the user pastes code-artifact content back wholesale (900+
   matched 5-grams). Proposed model: **addressed vs visible** —
   reasoning/code are *visible* but only the ai block *addresses* the
   user. Address-defined signals (vouching, validation, hedging,
   question-acts) stay ai-block; content-accessibility signals
   (`factual_error`, `user_misled`) can fire where the wrong content
   lives, including — new question — reasoning. Re-adjudications to
   walk: C4 b7 `false_confidence`, C4 b8 `factual_error`.
2. **D2 — drop `conversation_advanced`; unlabeled = advanced.** Keep
   `conversation_stalled`; clarification stays with
   `ai_asked_clarifying_question` / `user_asks_clarification`. Clears
   132 cells.
3. **D3 — `user_ambiguous_request` gets objectified steps**
   (two-readings test + missing-parameter test), kept this round;
   dropped in v0.7 only if κ still fails. We run 3–4 of its 14 open
   cells through the new steps live.
4. **D5 — firing granularity, two-part rule.** (1) Across blocks: fire
   on every block where the behavior occurs — ends the salient-moments
   convention that drove C8's 330-cell share. (2) Within a block: label
   EVERY occurrence (**advisor decision, 2026-08-05**) — consecutive
   exhibiting sentences form one label spanning the run; separated
   occurrences get separate labels. The occurrence is the recording
   unit; the block stays the agreement unit (κ uses (block, signal)
   presence, so multiple labels collapse to presence=1 and reliability
   is unaffected). The numbers say the rule is cheap: within-block
   multiplicity is rare everywhere except `ai_validates_user`, where A
   already marks multiple spans (15 blocks), and per-conversation count
   agreement is near-perfect for the question signals (Spearman A·B
   0.95–0.99) (table in D5).
5. **D6 — `ethical_tension` Step-2 rewrite (AI-alert-only).** v0.5
   Step 2 literally licenses labeling the human block — B and F followed
   it correctly on C4's crisis blocks; the AI-alert-only ruling never
   entered the text. This is a **rubric-text bug fix**: fire only on the
   reasoning/ai block where the model surfaces the tension; the human
   block keeps its user-side signals; silent compliance = no fire.
   Calibration set in the changelog entry.

**Already-ruled conventions, restated (not discussion items):**
placement follows the signal checklist (17 round-1 cells violated it —
filter `role_allowed = 0`); the label goes on the block where the *act*
happens when behavior spans adjacent blocks; question-signal
discriminators: offer to expand delivered content →
`ai_offers_to_elaborate`, ≥2 concrete named options →
`ai_offered_options`, question the AI needs to do the task →
`ai_asked_clarifying_question`, remaining yes/no turn-closer →
`ai_asks_followup`, open-ended WH deepening →
`ai_asked_probing_question`.
"""

STATIC["partIII"] = """\
## Part 2 — A-only clusters ({n_cells} cells): A fires, B+F consensus does not

Per cluster, the live question: is this a **sub-form B and F did not
know counts** (rubric under-specifies → rule transmits it), or **A
over-firing** (development labels drift past the written definition →
A's labels get corrected)? {n_sections} signals get full sections;
{n_tail} cells sit in the long tail table.
"""

STATIC["partIV"] = """\
## Part 3 — (B+F)-only clusters ({n_cells} cells): the consensus fires, A does not

The mirror question: is the consensus reading the v0.5 text more plainly
than A's intended-but-unwritten carve-out (→ carve-out gets written or
A's restriction is dropped), or did a B-origin reading propagate to F in
the update (→ walk it against the steps)? {n_sections} signals get full
sections; {n_tail} cells in the long tail.
"""

STATIC["partV"] = """\
## Appendix — B≠F residual ({n_cells} cells; outside the main review flow)

Cells where B and F still differ after the update — mostly F solo fires
B did not adopt. **Per cluster we need one fact from you two first: was
it discussed and disputed, or never reviewed?** Disputed → it joins the
meeting agenda; never reviewed → B does a normal pass on it first.
"""

STATIC["footer"] = """\
---
*Outputs this pack must produce by end of meeting 1: accept/modify
verdict per candidate rule · `diverged_at_step` filled for walked cells
· v0.6 changelog entries confirmed · re-annotation deadline agreed.*
"""


if __name__ == "__main__":
    main()
