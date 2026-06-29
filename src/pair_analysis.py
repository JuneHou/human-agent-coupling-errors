"""Contrast / pairing structure over the coupling signals (secondary support for the taxonomy).

Idea (Jun, 2026-06-04): many signals are minimal contrasts of each other — same control
operation / mechanism observation, differing on exactly ONE dimension:
  (1) POLARITY   contrast: same (op, direction), positive vs failure   — the two faces of a cell.
  (2) DIRECTION  contrast: same op, H2AI vs AI2H                        — the op crosses the boundary.
  (3) POSITION   contrast: the same move performed by the AI vs by the human (ai_X vs user_X).
Plus a curated MASKING co-occurrence layer: an H2AI failure + an AI2H failure that compound into the
canonical invisible failure (silent_assumption x false_confidence) — the common-ground ablation signature.

The analytic payoff: a cell that has only ONE polarity (or is empty) is a HOLE the wild data does not
fill. We predict those holes coincide with the action-native ops (seek_inspect / confirm_authorize /
stop_defer) — i.e. the contrast analysis re-derives the benchmark targets independently of the
needs_ground_truth argument.

Run:  python src/pair_analysis.py
Reads docs/criteria/control_mapping.csv (run build_control_mapping.py first).
"""
from __future__ import annotations
import csv
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CSV = REPO / "docs" / "criteria" / "control_mapping.csv"

OPS = ["seek_inspect", "ask_clarify", "confirm_authorize", "act_execute",
       "stop_defer", "report_state", "recover_repair", "maintain_state"]
DIRS = ["H2AI", "AI2H"]

# Curated cross-direction MASKING co-occurrences (mechanism-level, not column-derivable):
# an H2AI failure whose effect is hidden by an AI2H failure in the same turn-pair.
MASKING_PAIRS = [
    ("silent_assumption (H2AI report_state)", "false_confidence (AI2H report_state)",
     "agent misread intent, then reports it confidently — THE canonical invisible failure"),
    ("intent_missed (H2AI act_execute)", "ai_implicit_refusal (AI2H report_state)",
     "agent skipped part of the task and never surfaced the omission"),
    ("plow_through (H2AI maintain_state)", "ai_self_contradiction (AI2H maintain_state)",
     "agent dropped prior context; the drift shows only as a later contradiction"),
]

# Curated POSITION contrasts: the same control move from each side of the boundary.
POSITION_PAIRS = [
    ("ai_asked_clarifying_question", "user_asks_clarification", "ask_clarify"),
    ("ai_acknowledges_correction",   "user_corrects_ai",        "recover_repair"),
]

# INTERPRETIVE layer (NOT column-derived): WHY each hole exists. A missing pole is an OBSERVATION;
# the verdict turns on the CAUSE of the missing pole (one-sidedness alone is NOT a gap):
#   (a) structural    - the pole cannot exist by the cell's definition; collapses into another op (=> structural_zero)
#   (b) substrate     - the pole CANNOT be instantiated in non-agentic chat at all: producing it REQUIRES a
#                       tool call / a consequential-irreversible action / a tool-error or environment state
#                       chat lacks. Genuinely undevelopable without agentic action (=> benchmark_gap).
#   (c) curation/thin - the pole COULD be coded from chat (no substrate barrier) but the predecessor coded
#                       only one polarity, or the op is communicative and merely thin (=> set_aside).
# So a one-sided cell is a benchmark_gap only if its MISSING pole is substrate-blocked, not merely uncoded.
# PRELIMINARY — these verdicts are to be confirmed when cell definitions lock (task 13) and against
# the agentic Stage-A data. They are listed explicitly so the judgment is reviewable, not buried.
HOLE_VERDICTS = {
 ("seek_inspect","H2AI"):      ("benchmark_gap",   "action-native (read-before-act); needs tools absent in WildChat -> expect in agentic"),
 ("seek_inspect","AI2H"):      ("structural_zero", "reporting what was inspected = report_state; no distinct AI->H inspect move"),
 ("confirm_authorize","H2AI"): ("benchmark_gap",   "only a human acceptance signal coded; consequential acts (tools) don't arise in chat"),
 ("confirm_authorize","AI2H"): ("structural_zero", "authority flows only human->agent; the AI-asks-permission move decomposes into report_state (surface the planned action) + confirm_authorize H->AI (take up the go/no-go) — no distinct AI->H authorization"),
 ("act_execute","AI2H"):       ("structural_zero", "execute realizes user intent = inherently H->AI; the AI->H side IS report_state"),
 ("stop_defer","H2AI"):        ("structural_zero", "stop/defer is an AI act (AI->H); a human-initiated stop is a trigger/correction"),
 ("stop_defer","AI2H"):        ("benchmark_gap",   "substrate-blocked FAILURE = failing to HALT a consequential/irreversible action mid-execution (can't abort a destructive tool call); needs an oracle too. The chat 'should-have-withheld-but-complied' shadow is a content-safety failure (mechanism/ethical layer), NOT this action-termination cell"),
 ("ask_clarify","AI2H"):       ("set_aside",       "present; failure pole (illegible/misleading clarify) thin in chat — not a target"),
 ("recover_repair","AI2H"):    ("benchmark_gap",   "distinct failure = OPAQUE recovery (silent re-plan after a tool error: human never learns it broke or that the plan changed); needs tool-error episodes + an oracle. The confident-but-inadequate-repair variant overlaps report_state false_confidence and is NOT counted here"),
 ("maintain_state","AI2H"):    ("set_aside",       "positive pole (legibly carried-forward state) thin; overlaps report_state — not a target"),
}


def load():
    rows = list(csv.DictReader(open(CSV, newline="", encoding="utf-8")))
    return [r for r in rows if r["relation_type"] == "coupling"]


def compute():
    """Pure: read control_mapping.csv and return the full contrast structure.

    Returns a dict:
      grid       - list of {op, l1, status, failure[], positive[], user[]} for all 16 cells
      complete   - list of (op, l1) polarity-complete cells
      holes      - list of {op, l1, status, verdict, basis} for the rest
      by_direction - {op: {span, present[], h2ai_signals[], ai2h_signals[]}}
      verdicts   - {verdict: [{op, l1, status, basis}]}
      masking    - MASKING_PAIRS as list of {h2ai, ai2h, mechanism}
      position   - POSITION_PAIRS as list of {op, ai, human}
    """
    rows = load()
    cell = defaultdict(lambda: defaultdict(list))
    for r in rows:
        cell[(r["control_op"], r["l1"])][r["polarity"]].append(r["signal"])

    grid, complete, holes = [], [], []
    for op in OPS:
        for d in DIRS:
            pol = cell.get((op, d), {})
            fails = pol.get("failure", [])
            poss = pol.get("positive", [])
            users = pol.get("human", []) + pol.get("escalation", [])
            if not (fails or poss or users):
                status = "EMPTY"
            elif fails and poss:
                status = "complete"
            elif fails:
                status = "failure-only"
            elif poss:
                status = "positive-only"
            else:
                status = "human-only"
            grid.append({"op": op, "l1": d, "status": status,
                         "failure": fails, "positive": poss, "user": users})
            if status == "complete":
                complete.append((op, d))
            else:
                holes.append((op, d, status))

    by_direction = {}
    for op in OPS:
        present = [d for d in DIRS if cell.get((op, d))]
        span = "both" if len(present) == 2 else (present[0] if present else "NONE")
        h2ai = cell.get((op, "H2AI"), {})
        ai2h = cell.get((op, "AI2H"), {})
        h2ai_signals = h2ai.get("failure", []) + h2ai.get("positive", []) + h2ai.get("human", []) + h2ai.get("escalation", [])
        ai2h_signals = ai2h.get("failure", []) + ai2h.get("positive", []) + ai2h.get("human", []) + ai2h.get("escalation", [])
        by_direction[op] = {"span": span, "present": present,
                            "h2ai_signals": h2ai_signals, "ai2h_signals": ai2h_signals}

    byv = defaultdict(list)
    holes_full = []
    for op, d, status in holes:
        v, basis = HOLE_VERDICTS.get((op, d), ("unclassified", ""))
        item = {"op": op, "l1": d, "status": status, "verdict": v, "basis": basis}
        holes_full.append(item)
        byv[v].append(item)

    return {
        "grid": grid,
        "complete": complete,
        "holes": holes_full,
        "holes_by_direction": dict(Counter(d for _, d, _ in holes)),
        "by_direction": by_direction,
        "verdicts": {v: byv.get(v, []) for v in ("benchmark_gap", "structural_zero", "set_aside", "unclassified")},
        "masking": [{"h2ai": h, "ai2h": a, "mechanism": note} for h, a, note in MASKING_PAIRS],
        "position": [{"op": op, "ai": ai_sig, "human": user_sig} for ai_sig, user_sig, op in POSITION_PAIRS],
    }


def main():
    res = compute()

    print("=" * 78)
    print("POLARITY CONTRAST — the two faces of each (operation x direction) cell")
    print("=" * 78)
    for g in res["grid"]:
        tag = "" if g["status"] == "complete" else "   <-- HOLE"
        print(f"\n  [{g['op']} | {g['l1']}]  {g['status']}{tag}")
        if g["failure"]: print(f"      failure : {', '.join(g['failure'])}")
        if g["positive"]: print(f"      positive: {', '.join(g['positive'])}")
        if g["user"]: print(f"      user-emitted: {', '.join(g['user'])}")

    print("\n" + "=" * 78)
    print("DIRECTION CONTRAST — which operations span the H<->AI boundary")
    print("=" * 78)
    for op in OPS:
        bd = res["by_direction"][op]
        print(f"  {op:18s} {bd['span']:6s}")
        if bd["h2ai_signals"]:
            print(f"      H2AI: {', '.join(bd['h2ai_signals'])}")
        if bd["ai2h_signals"]:
            print(f"      AI2H: {', '.join(bd['ai2h_signals'])}")
    bilateral = [op for op, bd in res["by_direction"].items()
                 if set(bd["h2ai_signals"]) & set(bd["ai2h_signals"])]
    print(f"\n  Signals appearing in BOTH directions (should be empty): {bilateral or '[]'}")

    print("\n" + "=" * 78)
    print("POSITION CONTRAST — the same move, AI-performed vs human-performed")
    print("=" * 78)
    for p in res["position"]:
        print(f"  {p['op']:16s}: AI does «{p['ai']}»  <->  human does «{p['human']}»")

    print("\n" + "=" * 78)
    print("MASKING CO-OCCURRENCE — H2AI failure hidden by AI2H failure (invisible-failure signatures)")
    print("=" * 78)
    for m in res["masking"]:
        print(f"  {m['h2ai']}\n     x {m['ai2h']}\n     => {m['mechanism']}\n")

    print("=" * 78)
    print(f"COMPLETENESS: {len(res['complete'])}/16 (op x direction) cells are polarity-complete in wild data; "
          f"{len(res['holes'])} are holes.")
    hd = res["holes_by_direction"]
    print(f"Holes by direction: H2AI={hd.get('H2AI', 0)}  AI2H={hd.get('AI2H', 0)}  (AI->H legibility column is sparser).")
    print("\nWHY each hole exists (interpretive — see HOLE_VERDICTS; confirm on agentic data):")
    for v in ("benchmark_gap", "structural_zero", "set_aside", "unclassified"):
        items = res["verdicts"].get(v, [])
        if not items:
            continue
        print(f"\n  {v.upper()} ({len(items)}):")
        for it in items:
            print(f"    {it['op']:18s} {it['l1']:5s} [{it['status']:13s}] {it['basis']}")
    print("=" * 78)


if __name__ == "__main__":
    main()
