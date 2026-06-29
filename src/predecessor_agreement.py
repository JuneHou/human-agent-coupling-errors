"""Inter-annotator agreement (Cohen's kappa) over the predecessor's interannotator files.

Tells us which of the ~50 signals / 8 archetypes / the failure_visibility label are
reliable enough to *reuse* as features. Read-only over the predecessor repo.

Three reports:
  A. failure_visibility kappa  — pairwise, per condition (A/B/C), all annotator pairs
  B. archetype kappa           — per-archetype + macro/micro, condition C (the headline condition)
  C. signal kappa              — per-signal, opus vs gpt5 calibrated transcripts (the key table)

Annotators: A = {opus, gpt5}; B,C = {opus, gpt5, sonnet}.
"""
from __future__ import annotations
import gzip, json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

PRED = Path("/data/wang/junh/githubs/bigspin-invisible-failure-archetypes")
INTER = PRED / "data" / "interannotator"


def load_quality(condition, annotator):
    p = INTER / f"score_10k_quality_{condition}_{annotator}.jsonl.gz"
    if not p.exists() or p.stat().st_size < 1000:
        return None
    with gzip.open(p, "rt") as f:
        rows = [json.loads(l) for l in f]
    return pd.DataFrame(rows).set_index("conversation_id")


def arch_set(lst):
    return {a["archetype"] for a in lst} if isinstance(lst, list) else set()


# ── A. failure_visibility kappa ───────────────────────────────────────────
def failure_visibility_kappa():
    """Pure: pairwise failure_visibility kappa per condition. Returns list of dicts."""
    out = []
    for cond in ["A", "B", "C"]:
        dfs = {a: load_quality(cond, a) for a in ["opus", "gpt5", "sonnet"]}
        dfs = {a: d for a, d in dfs.items() if d is not None}
        for a, b in combinations(dfs, 2):
            s = dfs[a]["failure_visibility"].dropna()
            t = dfs[b]["failure_visibility"].dropna()
            j = s.index.intersection(t.index)
            s, t = s.loc[j], t.loc[j]
            out.append({"condition": cond, "pair": f"{a}/{b}", "n": int(len(j)),
                        "kappa": float(cohen_kappa_score(s, t)),
                        "agreement": float((s.values == t.values).mean())})
    return out


def failure_visibility_report():
    print("## A. failure_visibility kappa (multiclass), by condition & annotator pair")
    print(f"   {'cond':<5}{'pair':<16}{'n':>7}{'kappa':>8}{'agreement':>11}")
    for r in failure_visibility_kappa():
        print(f"   {r['condition']:<5}{r['pair']:<16}{r['n']:>7,}{r['kappa']:>8.2f}{r['agreement']:>10.1%}")


# ── B. archetype kappa (condition C) ──────────────────────────────────────
def archetype_kappa(cond="C"):
    """Pure: per-archetype + macro/micro kappa (opus vs gpt5). Returns a dict."""
    o, g = load_quality(cond, "opus"), load_quality(cond, "gpt5")
    j = o.index.intersection(g.index)
    os_, gs_ = o.loc[j, "archetypes"].apply(arch_set), g.loc[j, "archetypes"].apply(arch_set)
    labels = sorted({x for s in os_ for x in s} | {x for s in gs_ for x in s})
    per, all_o, all_g, ks = [], [], [], []
    for lab in labels:
        ov = os_.apply(lambda s: lab in s)
        gv = gs_.apply(lambda s: lab in s)
        k = cohen_kappa_score(ov, gv)
        ks.append(k)
        all_o.append(ov); all_g.append(gv)
        per.append({"archetype": lab, "kappa": float(k),
                    "agreement": float((ov.values == gv.values).mean()),
                    "opus_prev": float(ov.mean()), "gpt5_prev": float(gv.mean())})
    AO, AG = pd.concat(all_o), pd.concat(all_g)
    return {"condition": cond, "per_archetype": per,
            "macro": float(np.mean(ks)), "micro": float(cohen_kappa_score(AO, AG)),
            "micro_agreement": float((AO.values == AG.values).mean())}


def archetype_report(cond="C"):
    res = archetype_kappa(cond)
    print(f"\n## B. archetype kappa — condition {cond}, opus vs gpt5 (per-archetype)")
    print(f"   {'archetype':<28}{'kappa':>8}{'agreement':>11}{'opus%':>8}{'gpt5%':>8}")
    for r in res["per_archetype"]:
        print(f"   {r['archetype']:<28}{r['kappa']:>8.2f}{r['agreement']:>10.1%}"
              f"{r['opus_prev']:>8.1%}{r['gpt5_prev']:>8.1%}")
    print(f"   {'MACRO':<28}{res['macro']:>8.2f}")
    print(f"   {'MICRO':<28}{res['micro']:>8.2f}{res['micro_agreement']:>10.1%}")


# ── C. signal kappa (the key reliability table) ───────────────────────────
def load_signals(annotator):
    p = INTER / f"score_10k_{annotator}_calibrated_transcripts.jsonl.gz"
    rows = {}
    with gzip.open(p, "rt") as f:
        for line in f:
            r = json.loads(line)
            ai = set((r.get("ai_signal_summary") or {}).keys())
            us = set((r.get("user_signal_summary") or {}).keys())
            rows[r["conversation_id"]] = ai | us
    return rows


def signal_kappa():
    """Pure: per-signal kappa (opus vs gpt5). Returns a dict with rows + summary."""
    o, g = load_signals("opus"), load_signals("gpt5")
    j = sorted(set(o) & set(g))
    sigs = sorted({s for cid in j for s in o[cid]} | {s for cid in j for s in g[cid]})
    rep = []
    for s in sigs:
        ov = np.array([s in o[c] for c in j])
        gv = np.array([s in g[c] for c in j])
        prev = (ov.mean() + gv.mean()) / 2
        if max(ov.mean(), gv.mean()) < 0.005:   # skip near-absent signals
            continue
        k = cohen_kappa_score(ov, gv) if ov.any() or gv.any() else float("nan")
        rep.append({"signal": s, "kappa": float(k), "prev": float(prev),
                    "opus_prev": float(ov.mean()), "gpt5_prev": float(gv.mean())})
    rep.sort(key=lambda r: r["kappa"], reverse=True)
    ks = [r["kappa"] for r in rep]
    return {"n_shared": len(j), "rows": rep,
            "n_signals": len(rep), "median_kappa": float(np.median(ks)) if ks else float("nan"),
            "tiers": {"ge_0.6": sum(k >= 0.6 for k in ks),
                      "0.4_0.6": sum(0.4 <= k < 0.6 for k in ks),
                      "lt_0.4": sum(k < 0.4 for k in ks)}}


def signal_report():
    res = signal_kappa()
    print("\n## C. signal kappa — opus vs gpt5 calibrated transcripts (presence per conversation)")
    print(f"   shared conversations: {res['n_shared']:,}")
    print(f"   {'signal':<32}{'kappa':>7}{'prev':>7}{'opus%':>7}{'gpt5%':>7}")
    for r in res["rows"]:
        print(f"   {r['signal']:<32}{r['kappa']:>7.2f}{r['prev']:>7.1%}{r['opus_prev']:>7.1%}{r['gpt5_prev']:>7.1%}")
    t = res["tiers"]
    print(f"\n   signals: {res['n_signals']} | median kappa {res['median_kappa']:.2f} | "
          f">=0.6: {t['ge_0.6']} | 0.4-0.6: {t['0.4_0.6']} | <0.4: {t['lt_0.4']}")


def compute():
    """Pure: all three reliability reports as one dict (no printing)."""
    return {
        "failure_visibility": failure_visibility_kappa(),
        "archetype": archetype_kappa("C"),
        "signals": signal_kappa(),
    }


if __name__ == "__main__":
    failure_visibility_report()
    archetype_report("C")
    signal_report()
