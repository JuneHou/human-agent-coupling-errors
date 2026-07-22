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

from signal_stats import DEFAULT_DB, load_annotations

SIGNAL = "ai_validates_user"

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
    ai_block_total = 0
    tasks = set()

    for task_id, dialogue, result in load_annotations(db_path):
        tasks.add(task_id)

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

    return candidates, labeled_spans, labeled_blocks, ai_block_total, tasks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--out", default="/tmp/validation_sweep.json")
    args = ap.parse_args()

    cands, spans, labeled_blocks, ai_total, tasks = sweep(args.db)

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

    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
