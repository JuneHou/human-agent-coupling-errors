"""W3 — WildChat under the new buckets: triggers, repair primitives, and the no-reaction limit.

Read-only over the predecessor annotations. Produces the numbers for docs/coupling-lens-notes.md:
  1. THE HEADLINE: share of failures with NO user reaction (the case for an oracle), overall AND
     multi-turn-only (the predecessor's single-turn artifact deflates the honest number).
  2. Triggers: P(failure | human-only trigger) vs base rate, for ambiguity / multi-request / scope.
  3. Repair primitives: prevalence of AI-side and human-side grounding-repair acts among failures.

Buckets per docs/codebook_v1.md. "Reaction" is NOT a coordinate here — it is the deprecated
visibility covariate, used only to quantify how often failures are invisible.
"""
from __future__ import annotations
import gzip, json
from collections import Counter
from pathlib import Path

import pandas as pd

PRED = Path("/data/wang/junh/githubs/bigspin-invisible-failure-archetypes")
MAIN = PRED / "data" / "wildchat_annotations_opus_v2.json.gz"
SUMM = PRED / "data" / "interannotator" / "score_10k_opus_calibrated_transcripts.jsonl.gz"

FAILS = ["invisible", "visible", "mixed"]
# human-side reaction signals = the deprecated "visible" channel (for the no-reaction count)
HUMAN_REACTION = {"user_corrects_ai", "user_implicit_correction", "user_repeats_request",
                  "user_asks_clarification", "user_expresses_frustration",
                  "user_expresses_dissatisfaction", "user_abandons_thread"}
TRIGGERS = ["user_ambiguous_request", "user_multi_request", "user_scope_change",
            "user_provides_invalid_input"]
AI_REPAIR = ["ai_asked_clarifying_question", "ai_offered_options", "ai_acknowledges_correction",
             "error_recovery", "ai_provides_alternatives"]
HUMAN_REPAIR = ["user_corrects_ai", "user_implicit_correction", "user_repeats_request",
                "user_asks_clarification"]


def pct(n, d):
    return f"{n/d*100:.1f}%" if d else "n/a"


def load_summaries():
    recs = {}
    with gzip.open(SUMM, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            sigs = set((r.get("ai_signal_summary") or {})) | set((r.get("user_signal_summary") or {}))
            recs[r["conversation_id"]] = {"sigs": sigs, "n_turns": r.get("n_turns") or 0}
    return recs


def headline_stats(df):
    """Pure: the no-reaction limit (overall + depth-corrected). Returns a dict."""
    N = len(df)
    vc = df["failure_visibility"].value_counts()
    fails = sum(vc.get(k, 0) for k in FAILS)
    inv = vc.get("invisible", 0)
    depth = []
    for label, sub in [("multi-turn (turns>=2)", df[df["turns"] >= 2]),
                       ("turns>=4", df[df["turns"] >= 4])]:
        v = sub["failure_visibility"].value_counts()
        f = sum(v.get(k, 0) for k in FAILS)
        depth.append({"label": label, "n": int(len(sub)), "fails": int(f),
                      "invisible": int(v.get("invisible", 0)),
                      "no_reaction_pct": v.get("invisible", 0) / f * 100 if f else None})
    return {
        "N": int(N), "fails": int(fails),
        "failure_rate_pct": fails / N * 100 if N else None,
        "invisible": int(inv), "visible": int(vc.get("visible", 0)),
        "invisible_pct_of_fails": inv / fails * 100 if fails else None,
        "visible_pct_of_fails": vc.get("visible", 0) / fails * 100 if fails else None,
        "depth": depth,
    }


def triggers_repair_stats(df, recs):
    """Pure: trigger lifts + repair-primitive prevalence among failures. Returns a dict."""
    fv = df.set_index("conversation_id")["failure_visibility"].to_dict()
    rows = [(cid, d["sigs"], d["n_turns"], fv.get(cid)) for cid, d in recs.items() if cid in fv]
    n = len(rows)
    base_fail = sum(1 for _, _, _, v in rows if v in FAILS)
    base_rate = base_fail / n if n else 0

    triggers = []
    for t in TRIGGERS:
        sub = [r for r in rows if t in r[1]]
        if not sub:
            continue
        f = sum(1 for _, _, _, v in sub if v in FAILS)
        triggers.append({"trigger": t, "prev_pct": len(sub) / n * 100,
                         "p_fail_pct": f / len(sub) * 100,
                         "lift": (f / len(sub)) / base_rate if base_rate else 0})

    fail_rows = [r for r in rows if r[3] in FAILS]
    ai_acts = {a: sum(1 for r in fail_rows if a in r[1]) / base_fail * 100 for a in AI_REPAIR} if base_fail else {}
    hu_acts = {a: sum(1 for r in fail_rows if a in r[1]) / base_fail * 100 for a in HUMAN_REPAIR} if base_fail else {}
    any_ai = sum(1 for r in fail_rows if r[1] & set(AI_REPAIR))
    any_hu = sum(1 for r in fail_rows if r[1] & set(HUMAN_REPAIR))
    neither = sum(1 for r in fail_rows if not (r[1] & (set(AI_REPAIR) | set(HUMAN_REPAIR))))
    return {
        "n_joined": n, "base_fail": base_fail, "base_rate_pct": base_rate * 100,
        "triggers": triggers,
        "ai_repair_pct": ai_acts, "human_repair_pct": hu_acts,
        "no_repair_pct": neither / base_fail * 100 if base_fail else None,
        "ai_repair_present_pct": any_ai / base_fail * 100 if base_fail else None,
        "human_repair_present_pct": any_hu / base_fail * 100 if base_fail else None,
    }


def compute():
    """Pure: load the predecessor annotations and return the W3 headline + triggers/repair."""
    df = pd.read_json(MAIN)
    recs = load_summaries()
    return {"headline": headline_stats(df), "triggers_repair": triggers_repair_stats(df, recs)}


def headline(df):
    h = headline_stats(df)
    print("## 1. THE NO-REACTION LIMIT (the case for an oracle)")
    print(f"  N={h['N']:,}; failures={h['fails']:,} ({h['failure_rate_pct']:.1f}%)")
    print(f"  failures with NO user reaction (invisible) = {h['invisible']:,} = {h['invisible_pct_of_fails']:.1f}% of failures")
    print(f"  failures the user DID react to (visible)    = {h['visible']:,} = {h['visible_pct_of_fails']:.1f}% of failures")
    for d in h["depth"]:
        nr = f"{d['no_reaction_pct']:.1f}%" if d["no_reaction_pct"] is not None else "n/a"
        print(f"  [{d['label']}] no-reaction/fail = {nr}  (n={d['n']:,}, fails={d['fails']:,})")
    print("  >> Even depth-corrected, a large majority of failures draw no user reaction ->"
          " reaction cannot be the failure label; the benchmark needs an independent oracle.")
    return h["fails"]


def triggers_and_repair(df, recs):
    t = triggers_repair_stats(df, recs)
    print(f"\n## 2. TRIGGERS -> failure (joined 10k summaries x failure status; n={t['n_joined']:,})")
    print(f"  base failure rate = {t['base_rate_pct']:.1f}%")
    for r in t["triggers"]:
        print(f"  {r['trigger']:28s} prev={r['prev_pct']:5.1f}%  P(fail|trigger)={r['p_fail_pct']:5.1f}%  lift={r['lift']:.2f}x")
    print(f"\n## 3. REPAIR PRIMITIVES among failures (the chat-side baseline; n_fail={t['base_fail']:,})")
    print("  AI-initiated repair/clarify acts:")
    for a, v in t["ai_repair_pct"].items():
        print(f"    {a:30s} {v:5.1f}% of failures")
    print("  human-initiated repair acts (the visible side):")
    for a, v in t["human_repair_pct"].items():
        print(f"    {a:30s} {v:5.1f}% of failures")
    print(f"  >> failures with NO repair act by either party: {t['no_repair_pct']:.1f}% "
          f"(AI-repair present {t['ai_repair_present_pct']:.1f}%, human-repair present {t['human_repair_present_pct']:.1f}%)")


def main():
    df = pd.read_json(MAIN)
    headline(df)
    recs = load_summaries()
    triggers_and_repair(df, recs)


if __name__ == "__main__":
    main()
