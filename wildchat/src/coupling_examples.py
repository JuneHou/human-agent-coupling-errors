"""Step 3 (examples + ShareChat probe) — pull grounded canonical-cell conversations
from WildChat via the validated positional join, and measure the Claude thinking
disclosure gap in ShareChat."""
from __future__ import annotations
import csv, sys
from pathlib import Path

import pyarrow.parquet as pq

from coupling_lens import load_summaries, MAP, WILD


def has(r, b):
    return any(MAP.get(s) == b for s in
               list(r["ai_signal_summary"]) + list(r["user_signal_summary"]))


csv.field_size_limit(sys.maxsize)
CLAUDE = Path("/data/wang/junh/githubs/human-agent-coupling-errors/data/sharechat/"
              "claude_results_final_language_filtered.csv")


def canonical_examples(max_id=59857, k=3):
    recs = load_summaries()
    hits = [r for r in recs
            if has(r, "H2AI_NEG") and not has(r, "REPAIR_AGENT")
            and not has(r, "REACTION_USER") and "false_confidence" in r["ai_signal_summary"]
            and r["conversation_id"] < max_id]
    hits = hits[:k]
    ids = {r["conversation_id"]: r for r in hits}
    print(f"=== {len(hits)} canonical-cell examples (uptake-fail x false_confidence x invisible), shard0 ===")
    conv = pq.read_table(str(sorted(WILD.glob("*.parquet"))[0]),
                         columns=["conversation"]).column("conversation").to_pylist()
    for cid, r in ids.items():
        print(f"\n--- conversation_id {cid} | n_turns={r['n_turns']} ---")
        print("  ai_signals:", dict(r["ai_signal_summary"]))
        print("  user_signals:", dict(r["user_signal_summary"]))
        for m in conv[cid][:4]:
            role = m["role"]; txt = (m["content"] or "").replace("\n", " ")[:220]
            print(f"  [{role}] {txt}")


def thinking_gap():
    """Pure: measure the Claude thinking/surfaced char-length ratio (no printing).

    Returns a dict: n_llm, n_think, thinking_coverage_pct, median_ratio,
    pct_reason_more (ratio>1), example (thinking, surfaced) or None.
    """
    n_llm = n_think = 0
    ratios = []
    example = None
    with open(CLAUDE, newline="", encoding="utf-8", errors="replace") as fh:
        for row in csv.DictReader(fh):
            if row.get("role") != "llm":
                continue
            n_llm += 1
            think = (row.get("thinking") or "").strip()
            surfaced = (row.get("plain_text") or "").strip()
            if think:
                n_think += 1
                if surfaced:
                    ratios.append(len(think) / max(len(surfaced), 1))
                if example is None and 400 < len(think) < 1500 and len(surfaced) > 100:
                    example = (think, surfaced)
    ratios.sort()
    med = ratios[len(ratios) // 2] if ratios else 0
    hi = sum(1 for x in ratios if x > 1) / len(ratios) * 100 if ratios else 0
    return {
        "n_llm": n_llm, "n_think": n_think,
        "thinking_coverage_pct": n_think / n_llm * 100 if n_llm else 0.0,
        "median_ratio": med, "pct_reason_more": hi, "example": example,
    }


def claude_thinking_gap():
    print("\n\n=== ShareChat Claude thinking disclosure gap ===")
    g = thinking_gap()
    print(f"Claude llm turns: {g['n_llm']}; with thinking: {g['n_think']} ({g['thinking_coverage_pct']:.1f}%)")
    print(f"thinking/surfaced char-length ratio: median {g['median_ratio']:.2f}; "
          f"{g['pct_reason_more']:.1f}% of turns reason MORE than they surface (ratio>1)")
    if g["example"]:
        th, su = g["example"]
        print("\nexample — THINKING (truncated):\n ", th[:300].replace("\n", " "))
        print("example — SURFACED (truncated):\n ", su[:300].replace("\n", " "))


if __name__ == "__main__":
    canonical_examples()
    claude_thinking_gap()
