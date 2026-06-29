"""The feedback gap on Stage-A: how often does an observably-wrong agent action draw NO human feedback?

Motivation (the AI-AI vs AI-H asymmetry, made empirical): in multi-agent traces the evaluative signal
is materialized/recoverable (peer/verifier messages, gold answer); in human-AI wild traces the human's
feedback is sparse and non-recoverable. So the wild trace cannot tell you which actions were wrong.
This script measures the sparsity directly on the agentic ShareChat Stage-A record.

We use the cleanest RECORD-DERIVABLE proxy for "trace-observable wrong": a turn whose tool response or
state_change_hint carries a HARD error marker (traceback / exception / stderr / non-zero exit / a
*Error type / permission denied / command not found). We then ask whether the NEXT user turn shows any
correction/dissatisfaction.

CAVEATS (first cut, illustrative — needs an LLM judge + the analysis+thinking extractor to firm up):
  - tool-error is a PROXY for observably-wrong (misses wrong-but-no-error actions; the true rate is higher).
  - Stage-A reads the `analysis` column only ⇒ undercounts tool turns (248 here vs ~278 known).
  - feedback is keyword-detected ⇒ cannot perfectly separate a correction from an unrelated next step.

Run:  python src/feedback_gap.py    (reads data/derived/sharechat_agentic.jsonl)
"""
from __future__ import annotations
import json, re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
JSONL = REPO / "data" / "derived" / "sharechat_agentic.jsonl"

# HIGH-PRECISION hard-error markers in a tool response / state_change_hint.
HARD_ERROR = re.compile(
    r"(traceback \(most recent call last\)|\btraceback\b|\bexception\b|\bstderr\b|"
    r"exit code [1-9]|exit status [1-9]|non-zero exit|\berrno\b|"
    r"[A-Za-z]*Error\b|[A-Za-z]*Exception\b|permission denied|command not found|"
    r"segmentation fault|module not found|no such file)", re.I)

# Correction / dissatisfaction / repeat markers in the NEXT user turn.
FEEDBACK = re.compile(
    r"\b(doesn'?t work|not work|isn'?t work|does not work|still (?:not|doesn'?t|broken|fails?)|"
    r"that'?s not|not what i|incorrect|\bwrong\b|\bbroken\b|\bbug\b|\berror\b|\bfix\b|"
    r"didn'?t|did not|won'?t|fails?|failing|doesn'?t|is not|isn'?t|instead|actually|"
    r"\bno,|\bnope\b|but it|should (?:be|have|n'?t)|i asked|i said|try again|\bagain\b)", re.I)


def hard_error(turn) -> bool:
    blob = [str(turn.get("state_change_hint") or "")]
    for tc in (turn.get("tool_calls") or []):
        blob.append(str(tc.get("response") or ""))
    return bool(HARD_ERROR.search("\n".join(blob)))


def has_feedback(user_message) -> bool:
    return bool(FEEDBACK.search(str(user_message or "")))


def compute():
    """Pure: read the agentic record and return the feedback-gap statistics.

    Returns a dict:
      n_records, n_convs, n_tool, n_err_total, n_pairs (turns with a next turn),
      base_rate {fb, n, pct}, cells {wrong_fb, wrong_nofb, ok_fb, ok_nofb},
      headline {n_wrong, nofb, pct}.
    """
    rows = [json.loads(l) for l in open(JSONL)]
    conv = defaultdict(list)
    for r in rows:
        conv[r["conversation_id"]].append(r)

    # build (turn, next_user_turn) pairs
    pairs = []  # (turn_record, next_user_message_or_None)
    for cid, v in conv.items():
        v = sorted(v, key=lambda r: r["turn_index"])
        for i, r in enumerate(v):
            nxt = v[i + 1]["user_message"] if i + 1 < len(v) else None
            pairs.append((r, nxt))

    with_next = [(r, nx) for (r, nx) in pairs if nx is not None]

    fb_base = sum(1 for (_, nx) in with_next if has_feedback(nx))

    cells = {("wrong", "fb"): 0, ("wrong", "nofb"): 0, ("ok", "fb"): 0, ("ok", "nofb"): 0}
    for (r, nx) in with_next:
        w = "wrong" if hard_error(r) else "ok"
        f = "fb" if has_feedback(nx) else "nofb"
        cells[(w, f)] += 1

    n_wrong = cells[("wrong", "fb")] + cells[("wrong", "nofb")]
    nofb = cells[("wrong", "nofb")]
    return {
        "n_records": len(rows),
        "n_convs": len(conv),
        "n_tool": sum(1 for r in rows if r.get("has_tool_calls")),
        "n_err_total": sum(1 for r in rows if hard_error(r)),
        "n_pairs": len(with_next),
        "base_rate": {"fb": fb_base, "n": len(with_next),
                      "pct": fb_base / len(with_next) * 100 if with_next else 0.0},
        "cells": {"wrong_fb": cells[("wrong", "fb")], "wrong_nofb": cells[("wrong", "nofb")],
                  "ok_fb": cells[("ok", "fb")], "ok_nofb": cells[("ok", "nofb")]},
        "headline": {"n_wrong": n_wrong, "nofb": nofb,
                     "pct": nofb / n_wrong * 100 if n_wrong else 0.0},
    }


def main():
    res = compute()
    c, br, hl = res["cells"], res["base_rate"], res["headline"]

    print(f"records: {res['n_records']}   conversations: {res['n_convs']}   tool-call turns: {res['n_tool']}")
    print(f"turns with a hard tool/exec error (any position): {res['n_err_total']}")
    print(f"turn->next-turn pairs (turns that have a following user turn): {res['n_pairs']}\n")

    print(f"BASE RATE — next user turn shows correction/dissatisfaction: "
          f"{br['fb']}/{br['n']} = {br['pct']:.1f}%")
    print("(i.e. most turns get no corrective feedback at all)\n")

    print("2x2 over turns that have a next turn:")
    print(f"  trace-observable wrong (tool error)  & next-turn feedback : {c['wrong_fb']}")
    print(f"  trace-observable wrong (tool error)  & NO feedback        : {c['wrong_nofb']}   <-- the gap")
    print(f"  no trace error                       & next-turn feedback : {c['ok_fb']}")
    print(f"  no trace error                       & NO feedback        : {c['ok_nofb']}\n")

    if hl["n_wrong"]:
        print(f"HEADLINE — of {hl['n_wrong']} observably-wrong (tool-error) turns with a next turn, "
              f"{hl['nofb']} got NO human feedback = {hl['pct']:.0f}%.")
    print("\n(All keyword-based + tool-error proxy + analysis-only undercount ⇒ first cut, illustrative.)")


if __name__ == "__main__":
    main()
