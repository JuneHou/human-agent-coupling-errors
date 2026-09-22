#!/usr/bin/env python3
"""Recall sweep for `ai_validates_user` across the submitted annotations.

`ai_validates_user` is the broad, observable validation behavior: the AI
supportively recognizes, endorses, or positively evaluates something specific
about the user, OR endorses an identifiable position the user expressed. Four
NON-EXCLUSIVE forms nest inside it -- emotional, process_praise,
claim_endorsement, identity_trait -- and they carry different evidence strength
for a DOWNSTREAM sycophancy determination. This script does not make that
determination; it only surfaces candidate spans for adjudication.

Search space is ai blocks only (rubric `blocks: ["ai"]`; signal-decisions.md
bars the signal from <thinking> content).

Also hosts cross-cutting guards that are not specific to this signal: the R21
nesting check, a ROLE CHECK, and four ROUTING GUARDS (2026-09-22) that test the
observable antecedent deciding a two-signal routing rather than the annotation
state -- see routing_guards(). The R21 nesting check below is the state-based
form and is kept only as a subset of guard 1; it misses the case where the
annotator placed the acknowledgment span elsewhere.

A ROLE CHECK that every label sits on a block role its
rubric entry allows (A1) -- the slip you make picking the wrong neighbour out of
~46 signals, which is mechanical and so mechanically catchable.

Read-only: the database is opened via signal_stats.load_annotations, which uses
`mode=ro`. Nothing here writes to Label Studio.

Usage:
    python annotation/validation_sweep.py [--db PATH] [--out PATH]
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from signal_stats import DEFAULT_DB, load_annotations

SIGNAL = "ai_validates_user"
ACK_SIGNAL = "ai_acknowledges_correction"   # R21 nesting guard

# Positive-affect adjectives used by the identity_trait probe. The form fires on
# affirmation, not attribution, so the adjective list is the operative filter --
# neutral or negative characterization must not match.
POSITIVE_ADJ = (
    r"(?:amazing|beautiful|bold|brave|bright|brilliant|capable|careful|"
    r"caring|clear|compassionate|courageous|creative|curious|deep|dedicated|"
    r"discerning|empathetic|generous|gentle|genuine|gifted|good|grounded|"
    r"honest|humble|incredible|insightful|intelligent|intuitive|kind|loving|"
    r"open|patient|perceptive|powerful|precise|rare|remarkable|resilient|"
    r"resourceful|rigorous|sensitive|sharp|smart|special|strong|thoughtful|"
    r"thorough|unique|wise|wonderful)"
)

FORM_PATTERNS = {
    "claim_endorsement": r"""(?ix)
        \b(?:
            you'?re \s (?:absolutely \s |exactly \s |completely \s |totally \s |
                          quite \s |so \s )? right
          | you \s are \s right
          | that'?s \s (?:absolutely \s |exactly \s |quite \s )?
                       (?:right|true|correct|fair)
          | exactly [\s.,!?—-]
          | precisely [\s.,!?—-]
          | i \s agree
          | agreed \b
          | you'?re \s not \s wrong
          | you'?ve \s (?:identified|hit|touched|nailed|pinpointed|recognized|
                         articulated|put \s your \s finger)
          | (?:good|fair|valid|strong) \s point
          | you \s make \s a \s (?:good|fair|valid|strong) \s point
          | spot \s on
          | well \s put
          | you'?re \s onto \s something
          | indeed [\s.,!?—-]
          | no \s argument
          | couldn'?t \s agree
          | this \s is \s (?:right|correct|true)
          | you \s were \s (?:absolutely \s |completely \s |quite \s )? right
        )
    """,
    "process_praise": r"""(?ix)
        \b(?:
            your \s (?:instinct|intuition|reasoning|approach|discernment|
                       thinking|method|methodology|investigation|testing|
                       analysis|framing|question|insight|judgment|logic|
                       skepticism|observation)
          | (?:smart|wise|clever|sensible|prudent) \s to \b
          | good \s (?:call|instinct|eye|catch)
          | you \s were \s right \s to
          | i \s love \s how \s you
          | you \s (?:designed|approached|handled|reasoned|analyzed|thought)
              \s [^.!?]{0,40} (?:well|carefully|methodically|rigorously|
                                 thoroughly|clearly)
          | such \s (?:clear|wise|careful|sharp) \s \w+
          | i \s appreciate \s you \b
          | the \s \w+ \s you'?re \s (?:expressing|showing|bringing|doing)
          | (?:^|[.!?]\s)\s* (?:smart|wise|clever|sharp) \s (?:not \s )? to \b
          | what \s (?:wisdom|insight|clarity|discernment|care|rigor)
        )
    """,
    "emotional": r"""(?ix)
        \b(?:
            i \s hear \s (?:that \s |how \s )? you
          | i \s can \s (?:see|understand|imagine) \s how
          | i \s understand \s you'?re
          | that \s sounds \s (?:\w+ly \s )*
              (?:hard|difficult|painful|frightening|terrifying|exhausting|
                 distressing|scary|awful|overwhelming|lonely|serious)
          | what \s you'?re \s (?:experiencing|feeling|describing|going \s through)
          | (?:completely|totally|entirely|perfectly|absolutely) \s
              (?:understandable|valid|fair|reasonable|normal)
          | it'?s \s understandable
          | you \s don'?t \s deserve
          | makes \s sense \s that \s you \s (?:feel|would|might)
          | your \s (?:pain|fear|grief|frustration|exhaustion|distress) \s is \s
              (?:real|valid|understandable)
          | i \s (?:hear|see|feel) \s how \s much
        )
    """,
    "identity_trait": rf"""(?ix)
        \b(?:
            you \s are \s (?:already \s |truly \s |genuinely \s |so \s )?
                (?:a \s |an \s )? [\w\s]{{0,12}}? {POSITIVE_ADJ}
          | you'?re \s (?:already \s |truly \s |genuinely \s |so \s )?
                (?:a \s |an \s )? [\w\s]{{0,12}}? {POSITIVE_ADJ}
          | you \s ARE \b
          | you \s have \s (?:a|such \s a|an) \s [\w\s]{{0,20}}?
                (?:heart|mind|gift|soul|spirit|way \s with)
          | you'?re \s the \s kind \s of \s person
          | you'?re \s someone \s who
          | you'?re \s drawn \s to
          | your \s (?:heart|soul|spirit|courage|humility|honesty|integrity|
                       compassion|wisdom|strength)
          | your \s [\w\s]{{0,20}}? \s is \s (?:so \s |really \s )? {POSITIVE_ADJ}
          | that'?s \s (?:so \s |really \s |just \s )? {POSITIVE_ADJ}
        )
    """,
}

FORM_RE = {k: re.compile(v) for k, v in FORM_PATTERNS.items()}

# Residual guard: second-person affirmative constructions that none of the four
# form probes caught. Bounds the recall gap rather than leaving it unmeasured.
RESIDUAL_RE = re.compile(
    r"(?ix) (?: ^ | [.!?…—]\s | [^\w\s]\s | \s{2,} ) \s*"
    r"(?: yes | yeah | right | true | absolutely | correct | agreed )\b"
    r"| \b you'?re \s (?:so|really|very|quite) \b"
)
RESIDUAL_WINDOW = 300

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def norm(text):
    """Label Studio offset convention: block text with newlines as spaces."""
    return text.replace("\n", " ")


def sentences(text):
    return [s for s in SENT_SPLIT.split(text) if s.strip()]


def context_for(text, match_start):
    """The matched sentence plus one sentence of trailing context."""
    sents = sentences(text)
    pos = 0
    for i, s in enumerate(sents):
        pos = text.find(s, pos)
        if pos <= match_start < pos + len(s):
            return " ".join(sents[i:i + 2])
        pos += len(s)
    return text[max(0, match_start - 100):match_start + 300]


def preceding_user_turn(dialogue, idx):
    """Nearest earlier human block -- the referent for recoverable_user_position."""
    for j in range(idx - 1, -1, -1):
        if dialogue[j].get("author") == "human":
            return j, dialogue[j].get("text", "")
    return None, ""


def sweep(db_path):
    candidates = []
    labeled_blocks = set()      # (task_id, block_idx) already carrying the signal
    labeled_spans = []          # existing spans, for form-tagging + coverage check
    ack_spans = {}              # (task_id, block_idx) -> [(start, end)] for R21
    ai_block_total = 0
    tasks = set()

    for task_id, dialogue, result in load_annotations(db_path):
        tasks.add(task_id)

        for item in result:
            value = item.get("value", {})
            if ACK_SIGNAL not in value.get("paragraphlabels", []):
                continue
            if "startOffset" not in value:
                continue
            try:
                idx = int(value.get("start"))
            except (TypeError, ValueError):
                continue
            ack_spans.setdefault((task_id, idx), []).append(
                (value["startOffset"], value["endOffset"]))

        for item in result:
            if item.get("type") != "paragraphlabels":
                continue
            value = item.get("value", {})
            if SIGNAL not in value.get("paragraphlabels", []):
                continue
            try:
                idx = int(value.get("start"))
            except (TypeError, ValueError):
                continue
            labeled_blocks.add((task_id, idx))
            labeled_spans.append({
                "task_id": task_id,
                "block": idx,
                "block_author": (dialogue[idx].get("author", "?")
                                 if idx < len(dialogue) else "?"),
                "span_id": item.get("id", ""),
                "span_text": " ".join(value.get("text", "").split()),
                "offsets": (value.get("startOffset"), value.get("endOffset")),
            })

        for idx, turn in enumerate(dialogue):
            if turn.get("author") != "ai":
                continue
            ai_block_total += 1
            text = norm(turn.get("text", ""))

            hits = []
            for form, rx in FORM_RE.items():
                for m in rx.finditer(text):
                    hits.append((form, m.start(), m.group(0).strip()))

            tier = "form"
            if not hits:
                head = text[:RESIDUAL_WINDOW]
                m = RESIDUAL_RE.search(head)
                if not m:
                    continue
                tier = "residual"
                hits = [("residual", m.start(), m.group(0).strip())]

            u_idx, u_text = preceding_user_turn(dialogue, idx)
            for form, start, matched in hits:
                candidates.append({
                    "task_id": task_id,
                    "block": idx,
                    "tier": tier,
                    "form": form,
                    "matched": matched,
                    "context": " ".join(context_for(text, start).split())[:400],
                    "preceding_user_block": u_idx,
                    "preceding_user_text": " ".join(u_text.split()),
                    "already_labeled": (task_id, idx) in labeled_blocks,
                })

    # already_labeled is resolved after the fact: a task's spans are read before
    # its blocks above, but only for that task, so re-resolve globally.
    for c in candidates:
        c["already_labeled"] = (c["task_id"], c["block"]) in labeled_blocks

    return candidates, labeled_spans, labeled_blocks, ai_block_total, tasks, ack_spans



def role_legality_check(db_path, projects=None):
    """Every label must sit on a block role its rubric entry allows (rule A1).

    Picking the wrong neighbour out of ~46 signals is a mechanical slip, not a
    judgment error, and it is mechanically detectable: `ai_asked_clarifying_question`
    on a human block is always wrong, whatever the sentence says. Read-only.

    Returns (violations, gaps). A VIOLATION is a label whose role the entry
    disallows AND whose signal is side-consistent with its entry. A GAP is the
    same mismatch where the rubric text, not the label, is behind -- A1 lets
    AI-side signals sit on any AI-authored block, and the reversed
    `ethical_tension` fires on human blocks, but several entries still list only
    `ai`. Gaps are reported separately so they are not chased as labeling errors.
    """
    rubric = json.loads((Path(__file__).resolve().parent / "sharechat_rubric.json").read_text())
    allowed = {sig: set(e.get("blocks", [])) for sig, e in rubric["signals"].items()}
    AI_AUTHORED = {"ai", "reasoning", "code", "analysis"}
    violations, gaps = [], []
    for task_id, dialogue, items in load_annotations(db_path):
        for it in items:
            v = it.get("value", {})
            start = v.get("start")
            try:
                b = int(start)
            except (TypeError, ValueError):
                continue
            if b >= len(dialogue):
                continue
            role = dialogue[b].get("author")
            for sig in (v.get("paragraphlabels") or []):
                if sig not in allowed or role in allowed[sig]:
                    continue
                entry_is_ai_side = allowed[sig] <= AI_AUTHORED
                # rubric behind the rule, not the label:
                if entry_is_ai_side and role in AI_AUTHORED:
                    gaps.append((task_id, b, role, sig, "A1 allows any AI-authored block"))
                elif sig == "ethical_tension":
                    gaps.append((task_id, b, role, sig, "Step 2 reversed 2026-09-14: both sides fire"))
                else:
                    violations.append((task_id, b, role, sig, sorted(allowed[sig])))
    return violations, gaps



# ---------------------------------------------------------------------------
# Routing guards (2026-09-22). Each pairs two signals that compete for one act
# and tests the OBSERVABLE antecedent that decides the routing -- never the
# annotation state. A test of the form "does this span sit inside a span already
# labeled X" is satisfiable by moving the other span, so two annotators can both
# pass it and still disagree; that is how the round-3 task-8 b5/b8 cells arose.
# Flag only: a hit is a candidate for review, not an automatic correction.
# Named for the BEHAVIOUR, not for the ruling number (R19/R21/A6): those
# identifiers are discussion shorthand that an annotator reading only the
# rubric cannot resolve, which is the defect these guards exist to catch.
# ---------------------------------------------------------------------------

CORRECTION_SIGNALS = {"user_corrects_ai", "user_implicit_correction",
                      "user_repeats_request"}
QUESTION_FAMILY = {"ai_asked_clarifying_question", "ai_asks_followup",
                   "ai_offered_options", "ai_offers_to_elaborate",
                   "ai_provides_example"}
AGREEMENT_OPENER = re.compile(
    r"^\s*(you'?re\s+(absolutely\s+|exactly\s+|completely\s+)?right"
    r"|you\s+are\s+right|yes,|correct[.,!]|good catch|exactly[.,!]"
    r"|true[.,!]|fair\s+(enough|point))", re.I)


def _overlap(a, b):
    return a[0] < b[1] and b[0] < a[1]


def routing_guards(db_path):
    """Four observable-antecedent routing checks over every submitted
    annotation in the database (all raters, all projects). Returns findings."""
    out = []
    for task_id, dialogue, result in load_annotations(db_path):
        per_block = defaultdict(list)
        for item in result:
            value = item.get("value", {})
            labels = value.get("paragraphlabels") or []
            if not labels or "startOffset" not in value:
                continue
            per_block[int(value["start"])].append(
                (set(labels), int(value["startOffset"]), int(value["endOffset"]),
                 value.get("text", "")))

        def prev_human(idx):
            for j in range(idx - 1, -1, -1):
                if dialogue[j].get("author") == "human":
                    return j
            return None

        for block, spans_here in per_block.items():
            if block >= len(dialogue):
                continue
            here = set().union(*[lbl for lbl, _, _, _ in spans_here])
            j = prev_human(block)
            prev_labels = (set().union(*[l for l, _, _, _ in per_block[j]])
                           if j is not None and per_block.get(j) else set())
            corrected = bool(prev_labels & CORRECTION_SIGNALS)
            text = dialogue[block].get("text", "")

            # 1. ai_validates_user vs ai_acknowledges_correction. Antecedent:
            #    the preceding human turn corrected the AI, so an agreement
            #    clause opening this block is the acknowledgment act (R21).
            opener = AGREEMENT_OPENER.match(text)
            if opener and corrected:
                for lbl, s0, e0, txt in spans_here:
                    if SIGNAL in lbl and s0 <= opener.start() and e0 >= opener.end():
                        out.append(("AGREEMENT-AFTER-CORRECTION", task_id, block,
                                    f"{SIGNAL} on the opening agreement clause "
                                    f"while the preceding human turn b{j} carries "
                                    f"{sorted(prev_labels & CORRECTION_SIGNALS)}",
                                    txt[:70]))

            # 2. error_recovery self-caught gate. Antecedent: the preceding
            #    human turn reported the error, so the repair is user-caught.
            if "error_recovery" in here and corrected:
                for lbl, _, _, txt in spans_here:
                    if "error_recovery" in lbl:
                        out.append(("REPAIR-AFTER-USER-REPORT", task_id, block,
                                    f"error_recovery while the preceding human "
                                    f"turn b{j} carries "
                                    f"{sorted(prev_labels & CORRECTION_SIGNALS)} "
                                    f"-- Step 2 routes a user-reported error to "
                                    f"{ACK_SIGNAL}. Legitimate only if this span "
                                    f"repairs a DIFFERENT, self-caught error",
                                    txt[:70]))

            # 3. A6 one home per question, and 4. R19 per-claim exclusivity.
            for i, (l1, s1, e1, t1) in enumerate(spans_here):
                for l2, s2, e2, _ in spans_here[i + 1:]:
                    if not _overlap((s1, e1), (s2, e2)):
                        continue
                    q1, q2 = QUESTION_FAMILY & l1, QUESTION_FAMILY & l2
                    if q1 and q2 and q1 != q2:
                        out.append(("ONE-QUESTION-TWO-HOMES", task_id, block,
                                    f"{sorted(q1)} overlaps {sorted(q2)}",
                                    t1[:70]))
                    pair = {"factual_error", "false_confidence"}
                    if (pair & l1) and (pair & l2) and (pair & l1) != (pair & l2):
                        out.append(("WRONG-FACT-AND-OVERCLAIM-SAME-SPAN", task_id, block,
                                    "factual_error and false_confidence spans "
                                    "overlap -- R19 is exclusive per CLAIM, so "
                                    "narrow the wider span to its own claim",
                                    t1[:70]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--out", default="/tmp/validation_sweep.json")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero when a routing guard fires; for the "
                         "automated-annotation pipeline, where no human reads "
                         "the report")
    args = ap.parse_args()

    cands, spans, labeled_blocks, ai_total, tasks, ack_spans = sweep(args.db)

    cand_blocks = {(c["task_id"], c["block"]) for c in cands}
    new_blocks = cand_blocks - labeled_blocks
    missed = labeled_blocks - cand_blocks

    print(f"annotated tasks              : {len(tasks)}")
    print(f"ai blocks searched           : {ai_total}")
    print(f"existing {SIGNAL} spans      : {len(spans)} "
          f"over {len(labeled_blocks)} blocks")
    print(f"candidate blocks             : {len(cand_blocks)}")
    print(f"  already labeled            : {len(cand_blocks & labeled_blocks)}")
    print(f"  NEW (to adjudicate)        : {len(new_blocks)}")
    print(f"  NEW excluding task 101     : "
          f"{len([b for b in new_blocks if b[0] != 101])}")
    print(f"candidate matches (rows)     : {len(cands)}")

    by_form = Counter(c["form"] for c in cands)
    print("\nmatches by form:")
    for form, n in by_form.most_common():
        print(f"  {form:<20} {n}")

    # The signal name asserts the direction: the AI validates the user. A span on
    # a human block is a cross-selection error, never a valid placement.
    misplaced = [s for s in spans if s["block_author"] != "ai"]
    print(f"\nBLOCK CHECK -- {SIGNAL} must sit on ai blocks only:")
    if misplaced:
        for s in misplaced:
            print(f"  MISPLACED task {s['task_id']} block {s['block']} "
                  f"({s['block_author']}) span {s['span_id']}: {s['span_text'][:70]}")
        print(f"  -> {len(misplaced)} misplaced span(s). Remove them in Label Studio.")
    else:
        print("  none -- all spans are on ai blocks.")

    # R21: inside an acknowledgment of a user correction, "you're absolutely
    # right" affirms that the AI was WRONG, not something about the user -- the
    # concession is the operative act and ai_acknowledges_correction carries it.
    # Structural test: it holds even when the clause reads as praise.
    nested = []
    for s in spans:
        o1, o2 = s["offsets"]
        if o1 is None:
            continue
        for a1, a2 in ack_spans.get((s["task_id"], s["block"]), []):
            if o1 >= a1 and o2 <= a2:
                nested.append(s)
                break
    print(f"\nR21 CHECK -- {SIGNAL} must not nest inside {ACK_SIGNAL}:")
    if nested:
        for s in nested:
            print(f"  NESTED task {s['task_id']} block {s['block']} "
                  f"span {s['span_id']}: {s['span_text'][:70]}")
        print(f"  -> {len(nested)} nested span(s). Remove them (R21).")
    else:
        print("  none -- no spans nest inside an acknowledgment of correction.")

    violations, gaps = role_legality_check(args.db)
    print("\nROLE CHECK -- every label on a block role its entry allows (A1):")
    if violations:
        for t, b, role, sig, ok in violations:
            print(f"  WRONG ROLE task {t} block {b} [{role}]: {sig} (entry allows {ok})")
        print(f"  -> {len(violations)} label(s) on a disallowed role. Relabel to the "
              f"same-side signal.")
    else:
        print("  none -- every label sits on a role its entry allows.")
    if gaps:
        print(f"  {len(gaps)} further mismatch(es) where the RUBRIC TEXT is behind the "
              f"rule, not the label:")
        for t, b, role, sig, why in gaps:
            print(f"    task {t} block {b} [{role}]: {sig} -- {why}")

    print("\nCOVERAGE CHECK -- existing labeled blocks not caught by any probe:")
    if missed:
        for t, b in sorted(missed):
            txt = next((s["span_text"] for s in spans
                        if s["task_id"] == t and s["block"] == b), "")
            print(f"  HOLE task {t} block {b}: {txt[:110]}")
        print(f"  -> {len(missed)} hole(s). Widen the lexicon and re-run.")
    else:
        print("  none -- all existing spans are reachable by the probes.")

    by_task = Counter(t for t, _ in new_blocks)
    print("\nnew candidate blocks by task:")
    print("  " + ", ".join(f"{t}:{n}" for t, n in sorted(by_task.items())))

    with open(args.out, "w") as fh:
        json.dump({"candidates": cands, "existing_spans": spans},
                  fh, ensure_ascii=False, indent=1)
    print(f"\nwrote {args.out}")

    guards = routing_guards(args.db)
    print("\nROUTING GUARDS -- observable antecedents, flag only:")
    if guards:
        by_kind = Counter(g[0] for g in guards)
        for kind, n in by_kind.most_common():
            print(f"  {kind:<22} {n}")
        for kind, t, b, why, txt in sorted(guards):
            print(f"  {kind} task {t} block {b}: {why}")
            if txt:
                print(f"      span: {txt!r}")
    else:
        print("  none.")

    gate = bool(guards) if args.strict else False
    return 1 if (missed or misplaced or nested or violations or gate) else 0


if __name__ == "__main__":
    sys.exit(main())
