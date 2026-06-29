"""Statistical analysis of the *predecessor* (Invisible Failures) annotations.

Read-only over the predecessor repo's data files. Reuses the predecessor's own
helpers (analysis_utils.pmi / observed_over_expected / get_archetype_tags) so our
co-occurrence / PPMI numbers match their figures.

Sections:
  1. Quality + failure-visibility headline (reproduces ~79% invisible)
  2. Archetype prevalence, co-occurrence (count/PPMI/prob), domain x archetype
  3. Depth analysis: invisible-rate vs turn count (the single-turn artifact)
  4. Walkaway deep-dive: how much of "invisible" is just user abandonment

Nothing here is our taxonomy or any coupling-coordinate bucketing (paused).
"""
from __future__ import annotations
import gzip, json, sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

PRED = Path("/data/wang/junh/githubs/bigspin-invisible-failure-archetypes")
sys.path.insert(0, str(PRED))
from analysis_utils import observed_over_expected, pmi  # noqa: E402  (predecessor helpers)

MAIN = PRED / "data" / "wildchat_annotations_opus_v2.json.gz"
SUMM = PRED / "data" / "interannotator" / "score_10k_opus_calibrated_transcripts.jsonl.gz"


def pct(n, d):
    return f"{n/d*100:.1f}%" if d else "n/a"


def archnames(lst):
    return sorted({a["archetype"] for a in lst}) if isinstance(lst, list) else []


# ── 1. headline ───────────────────────────────────────────────────────────
def headline_stats(df):
    """Pure: quality distribution + failure-visibility headline. Returns a dict."""
    N = len(df)
    q = df["quality"].value_counts()
    v = df["failure_visibility"].value_counts()
    none, inv, vis, mix = (int(v.get(k, 0)) for k in ("none", "invisible", "visible", "mixed"))
    fails = inv + vis + mix
    return {
        "N": int(N),
        "quality": {k: {"n": int(q.get(k, 0)), "pct": q.get(k, 0) / N * 100 if N else None}
                    for k in ["good", "acceptable", "poor", "critical"]},
        "visibility": {"none": none, "invisible": inv, "visible": vis, "mixed": mix},
        "fails": fails, "failure_rate_pct": fails / N * 100 if N else None,
        "invisible_pct_of_fails": inv / fails * 100 if fails else None,
        "visible_pct_of_fails": vis / fails * 100 if fails else None,
        "inv_mix_pct_of_fails": (inv + mix) / fails * 100 if fails else None,
    }


def headline(df):
    h = headline_stats(df)
    print(f"# Predecessor — {h['N']:,} conversations (condition C, opus tagger)\n")
    print("## Quality:", {k: f"{d['n']:,} ({d['pct']:.1f}%)" for k, d in h["quality"].items()})
    v = h["visibility"]
    print(f"## Failure visibility: none {v['none']:,} | invisible {v['invisible']:,} | "
          f"visible {v['visible']:,} | mixed {v['mixed']:,}")
    print(f"  failures = {h['fails']:,} ({h['failure_rate_pct']:.1f}%); "
          f"invisible/fail = {h['invisible_pct_of_fails']:.1f}% (<- ~79% headline); "
          f"visible/fail = {h['visible_pct_of_fails']:.1f}%; (inv+mix)/fail = {h['inv_mix_pct_of_fails']:.1f}%")
    return h["fails"]


# ── 2. archetypes ─────────────────────────────────────────────────────────
def archetype_stats(df, fails):
    """Pure: archetype prevalence, co-occurrence (PPMI), domain x archetype PPMI. Returns a dict."""
    N = len(df)
    names_per = df["archetypes"].apply(archnames)
    count = Counter(n for ns in names_per for n in ns)
    archs = [a for a, _ in count.most_common()]
    prevalence = [{"archetype": a, "n": int(count[a]),
                   "pct_of_fails": count[a] / fails * 100 if fails else None,
                   "pct_of_all": count[a] / N * 100 if N else None} for a in archs]

    archs_real = [a for a in archs if a != "none"]
    idx = {a: i for i, a in enumerate(archs_real)}
    M = np.zeros((len(archs_real), len(archs_real)))
    for ns in names_per:
        ns = [n for n in ns if n in idx]
        for a in ns:
            M[idx[a], idx[a]] += 1
        for a, b in combinations(ns, 2):
            M[idx[a], idx[b]] += 1
            M[idx[b], idx[a]] += 1
    co = pd.DataFrame(M, index=archs_real, columns=archs_real)
    ppmi = pmi(co.replace(0, 0.0))
    pairs = []
    for a, b in combinations(archs_real, 2):
        cnt = co.loc[a, b]
        if cnt == 0:
            continue
        pba = cnt / co.loc[a, a] if co.loc[a, a] else 0
        pairs.append((cnt, ppmi.loc[a, b], pba, a, b))
    cooccurrence = [{"a": a, "b": b, "count": int(cnt), "ppmi": float(pp), "p_b_given_a": float(pba)}
                    for cnt, pp, pba, a, b in sorted(pairs, reverse=True)[:10]]

    top_dom = df["primary_vertical"].value_counts().head(10).index.tolist()
    DM = pd.DataFrame(0.0, index=top_dom, columns=archs_real)
    for dom, ns in zip(df["primary_vertical"], names_per):
        if dom in top_dom:
            for n in ns:
                if n in archs_real:
                    DM.loc[dom, n] += 1
    dom_ppmi = pmi(DM)
    assoc = [(dom_ppmi.loc[d, a], d, a) for d in top_dom for a in archs_real if dom_ppmi.loc[d, a] > 0]
    domain_archetype = [{"domain": d, "archetype": a, "ppmi": float(v)}
                        for v, d, a in sorted(assoc, reverse=True)[:12]]
    return {"prevalence": prevalence, "cooccurrence": cooccurrence,
            "domain_archetype": domain_archetype}


def archetype_block(df, fails):
    res = archetype_stats(df, fails)
    print("\n## Archetype prevalence (% of failures)")
    for r in res["prevalence"]:
        print(f"  {r['archetype']:<26} {r['n']:>6,}  ({r['pct_of_fails']:.1f}% of fails, {r['pct_of_all']:.1f}% of all)")
    print("\n## Archetype co-occurrence — top pairs (raw count | PPMI | P(b|a))")
    for r in res["cooccurrence"]:
        print(f"  {r['a']:<22}+ {r['b']:<22} {r['count']:>6,} | PPMI {r['ppmi']:4.2f} | P(b|a) {r['p_b_given_a']:.2f}")
    print("\n## Domain x archetype — strongest positive associations (PPMI)")
    for r in res["domain_archetype"]:
        print(f"  {r['domain']:<24} ~ {r['archetype']:<24} PPMI {r['ppmi']:4.2f}")


# ── 3. depth: the single-turn artifact ────────────────────────────────────
def depth_stats(df):
    """Pure: invisible rate vs turn count. Returns a dict."""
    rows = []
    for label, sub in [("turns == 1", df[df["turns"] == 1]),
                       ("turns == 2", df[df["turns"] == 2]),
                       ("turns == 3", df[df["turns"] == 3]),
                       ("turns 4-9", df[(df["turns"] >= 4) & (df["turns"] <= 9)]),
                       ("turns >= 10", df[df["turns"] >= 10]),
                       ("multi-turn (>=2)", df[df["turns"] >= 2])]:
        vc = sub["failure_visibility"].value_counts()
        f = int(vc.get("invisible", 0) + vc.get("visible", 0) + vc.get("mixed", 0))
        i = int(vc.get("invisible", 0))
        rows.append({"label": label, "n": int(len(sub)),
                     "failure_rate_pct": f / len(sub) * 100 if len(sub) else None,
                     "invisible_pct_of_fails": i / f * 100 if f else None})
    return {
        "mean_turns": float(df["turns"].mean()), "median_turns": int(df["turns"].median()),
        "single_turn_pct": (df["turns"] == 1).sum() / len(df) * 100 if len(df) else None,
        "rows": rows,
    }


def depth_block(df):
    res = depth_stats(df)
    print("\n## Depth — invisible rate vs turn count (the single-turn artifact)")
    print(f"  overall: mean {res['mean_turns']:.2f} turns, median {res['median_turns']}, "
          f"single-turn {res['single_turn_pct']:.1f}%")
    for r in res["rows"]:
        fr = f"{r['failure_rate_pct']:.1f}%" if r["failure_rate_pct"] is not None else "n/a"
        iv = f"{r['invisible_pct_of_fails']:.1f}%" if r["invisible_pct_of_fails"] is not None else "n/a"
        print(f"  {r['label']:<18} n={r['n']:>6,}  failure_rate={fr:>6}  invisible/fail={iv:>6}")
    mt = next(r for r in res["rows"] if r["label"] == "multi-turn (>=2)")
    print(f"  >> multi-turn-only invisible/fail = {mt['invisible_pct_of_fails']:.1f}% "
          f"(vs 78.9% headline inflated by single-turn mass)")


# ── 4. walkaway deep-dive ─────────────────────────────────────────────────
def walkaway_stats(df, fails):
    """Pure: how much of 'invisible' is just user abandonment. Returns a dict."""
    names_per = df["archetypes"].apply(archnames)
    inv = df["failure_visibility"] == "invisible"
    n_inv = int(inv.sum())
    has_walk = names_per.apply(lambda ns: "the_walkaway" in ns)
    inv_walk = int((inv & has_walk).sum())
    only_walk = names_per.apply(lambda ns: set(ns) - {"none"} == {"the_walkaway"})
    inv_only_walk = int((inv & only_walk).sum())
    cnt = Counter(n for ns in names_per for n in ns if n not in ("none", "the_walkaway"))
    no_other = df["archetypes"].apply(lambda lst: not (set(archnames(lst)) - {"none", "the_walkaway"}))
    fail_mask = df["failure_visibility"].isin(["invisible", "visible", "mixed"])
    only_walk_fail = int((fail_mask & no_other).sum())
    return {
        "n_invisible": n_inv,
        "invisible_with_walkaway": inv_walk,
        "invisible_with_walkaway_pct": inv_walk / n_inv * 100 if n_inv else None,
        "invisible_walkaway_only": inv_only_walk,
        "invisible_walkaway_only_pct": inv_only_walk / n_inv * 100 if n_inv else None,
        "mix_excl_walkaway": [{"archetype": a, "n": int(c),
                               "pct_of_fails": c / fails * 100 if fails else None}
                              for a, c in cnt.most_common()],
        "failures_only_walkaway_or_none": only_walk_fail,
        "failures_only_walkaway_or_none_pct": only_walk_fail / fails * 100 if fails else None,
    }


def walkaway_block(df, fails):
    res = walkaway_stats(df, fails)
    print("\n## Walkaway deep-dive — is 'invisible' just user abandonment?")
    print(f"  invisible failures: {res['n_invisible']:,}")
    print(f"  ...with the_walkaway: {res['invisible_with_walkaway']:,} ({res['invisible_with_walkaway_pct']:.1f}% of invisible)")
    print(f"  ...walkaway-ONLY (no other failure archetype): {res['invisible_walkaway_only']:,} "
          f"({res['invisible_walkaway_only_pct']:.1f}% of invisible)")
    print("\n  Archetype mix among failures, EXCLUDING the_walkaway:")
    for r in res["mix_excl_walkaway"]:
        print(f"    {r['archetype']:<26} {r['n']:>6,}  ({r['pct_of_fails']:.1f}% of failures)")
    print(f"\n  failures whose ONLY signal is walkaway/none: "
          f"{res['failures_only_walkaway_or_none']:,} ({res['failures_only_walkaway_or_none_pct']:.1f}% of failures)")


# ── signal prevalence (10k summaries) ─────────────────────────────────────
def signal_stats():
    """Pure: top AI/user signal prevalence over the 10k summaries. Returns a dict."""
    n = 0
    ai, usr = Counter(), Counter()
    with gzip.open(SUMM, "rt") as fh:
        for line in fh:
            r = json.loads(line)
            n += 1
            for s in (r.get("ai_signal_summary") or {}):
                ai[s] += 1
            for s in (r.get("user_signal_summary") or {}):
                usr[s] += 1
    return {
        "n": n,
        "ai_top": [{"signal": s, "pct": c / n * 100 if n else None} for s, c in ai.most_common(10)],
        "user_top": [{"signal": s, "pct": c / n * 100 if n else None} for s, c in usr.most_common(8)],
    }


def signal_block():
    res = signal_stats()
    print("\n## Signal prevalence (10k calibrated opus summaries, conv-level) — DESCRIPTIVE, no buckets")
    print(f"  n={res['n']:,}. Top AI:", {r["signal"]: f"{r['pct']:.1f}%" for r in res["ai_top"]})
    print("  Top USER:", {r["signal"]: f"{r['pct']:.1f}%" for r in res["user_top"]})


def compute():
    """Pure: the full predecessor analysis as one dict (no printing)."""
    df = pd.read_json(MAIN)
    h = headline_stats(df)
    return {
        "headline": h,
        "archetypes": archetype_stats(df, h["fails"]),
        "depth": depth_stats(df),
        "walkaway": walkaway_stats(df, h["fails"]),
        "signals": signal_stats(),
    }


def main():
    df = pd.read_json(MAIN)
    fails = headline(df)
    archetype_block(df, fails)
    depth_block(df)
    walkaway_block(df, fails)
    signal_block()


if __name__ == "__main__":
    main()
