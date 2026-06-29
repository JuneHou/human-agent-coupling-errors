"""Step 3 (analysis pass) — read the predecessor signals through the coupling lens.

Produces the numbers behind docs/coupling-lens-notes.md:
  1. signal -> coordinate mapping (REVIEWABLE judgment artifact)
  2. coordinate prevalence on the 10k calibrated summaries
  3. cross-channel co-occurrence + the "invisible uptake-coupling" rate (thesis cell)
  4. validation of the conversation_id -> WildChat positional join
"""
from __future__ import annotations
import glob, gzip, json
from collections import Counter
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

PRED = Path("/data/wang/junh/githubs/bigspin-invisible-failure-archetypes")
WILD = Path("/data/wang/junh/githubs/human-agent-coupling-errors/data/wildchat-1m/data")

# ── (1) REVIEWABLE signal -> coupling-coordinate mapping ───────────────────
# Coordinates: H2AI_* (uptake), AI2H_* (legibility), REPAIR_AGENT, REACTION_USER,
# plus non-channel buckets. Jun to review/adjust assignments.
MAP = {
    # Human->AI : uptake failures
    "silent_assumption": "H2AI_NEG", "generate_without_clarifying": "H2AI_NEG",
    "intent_missed": "H2AI_NEG", "plow_through": "H2AI_NEG", "under_delivered": "H2AI_NEG",
    "ai_implicit_refusal": "H2AI_NEG", "repetition": "H2AI_NEG", "error_commitment": "H2AI_NEG",
    "off_topic_drift": "H2AI_NEG", "over_delivered": "H2AI_NEG",
    # Human->AI : good uptake
    "adaptation": "H2AI_POS", "intent_addressed": "H2AI_POS", "scope_matched": "H2AI_POS",
    # AI->Human : legibility / honesty failures
    "false_confidence": "AI2H_NEG", "performative_hedge": "AI2H_NEG", "factual_error": "AI2H_NEG",
    "user_misled": "AI2H_NEG", "ai_self_contradiction": "AI2H_NEG", "problem_ignored": "AI2H_NEG",
    "ai_malfunction": "AI2H_NEG",
    # AI->Human : legibility / honesty (good)
    "appropriate_hedge": "AI2H_POS", "appropriate_confidence": "AI2H_POS",
    "ai_asserts_knowledge_limit": "AI2H_POS", "ai_stated_interpretation": "AI2H_POS",
    "ai_cites_source": "AI2H_POS", "ai_provides_caveats": "AI2H_POS", "ai_warns_user": "AI2H_POS",
    "problem_surfaced": "AI2H_POS", "ai_flags_complexity": "AI2H_POS", "ai_hedges_uncertainty": "AI2H_POS",
    "ai_refuses_or_declines": "AI2H_POS",  # explicit (legible) boundary, unlike ai_implicit_refusal
    # Repair : agent-initiated
    "ai_asked_clarifying_question": "REPAIR_AGENT", "ai_offered_options": "REPAIR_AGENT",
    "error_recovery": "REPAIR_AGENT", "ai_acknowledges_correction": "REPAIR_AGENT",
    "ai_asks_for_feedback": "REPAIR_AGENT", "ai_provides_alternatives": "REPAIR_AGENT",
    "ai_asked_probing_question": "REPAIR_AGENT",
    # Reaction : human-initiated (the "visible" side of repair)
    "user_corrects_ai": "REACTION_USER", "user_implicit_correction": "REACTION_USER",
    "user_asks_clarification": "REACTION_USER", "user_expresses_frustration": "REACTION_USER",
    "user_expresses_dissatisfaction": "REACTION_USER", "user_abandons_thread": "REACTION_USER",
    "user_repeats_request": "REACTION_USER",
    # user context / other (non-channel)
    "user_ambiguous_request": "USER_CTX", "user_multi_request": "USER_CTX",
    "user_validation_seeking": "USER_CTX", "user_scope_change": "USER_CTX",
    "user_provides_invalid_input": "USER_CTX", "user_positive_feedback": "REACTION_POS",
    "ai_structured_response": "PRESENTATION", "ai_provides_example": "PRESENTATION",
    "ai_provides_step_by_step": "PRESENTATION", "ai_summarizes": "PRESENTATION",
    "ai_references_prior_turn": "PRESENTATION", "ai_references_user_words": "PRESENTATION",
    "ai_validates_user": "PRESENTATION", "ai_empathy_expressed": "PRESENTATION",
    "ai_normalizes_difficulty": "PRESENTATION", "ai_offers_to_elaborate": "PRESENTATION",
    "ethical_tension": "OTHER", "conversation_advanced": "OUTCOME_POS",
    "conversation_stalled": "OUTCOME_NEG", "user_empowered": "OUTCOME_POS",
}


def load_summaries():
    path = PRED / "data/interannotator/score_10k_opus_calibrated_transcripts.jsonl.gz"
    recs = []
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            recs.append(json.loads(line))
    return recs


def coords_of(rec):
    """Return set of coordinate buckets present in a conversation."""
    sigs = list(rec.get("ai_signal_summary", {})) + list(rec.get("user_signal_summary", {}))
    return set(MAP.get(s, "UNMAPPED") for s in sigs), set(sigs)


def main():
    recs = load_summaries()
    n = len(recs)
    print(f"=== 10k calibrated summaries: {n} conversations ===\n")

    bucket_conv = Counter()      # convs with >=1 signal in bucket
    unmapped = Counter()
    has = lambda r, b: any(MAP.get(s) == b for s in
                           list(r["ai_signal_summary"]) + list(r["user_signal_summary"]))
    for r in recs:
        buckets, sigs = coords_of(r)
        for b in buckets:
            bucket_conv[b] += 1
        for s in sigs:
            if s not in MAP:
                unmapped[s] += 1

    print("Coordinate prevalence (% of conversations with >=1 signal in bucket):")
    for b, c in bucket_conv.most_common():
        print(f"  {b:14s} {c:6d}  {c/n*100:5.1f}%")
    if unmapped:
        print("\n!! UNMAPPED signals:", dict(unmapped))

    # ── thesis cell: invisible uptake-coupling failure ──
    h2ai = [r for r in recs if has(r, "H2AI_NEG")]
    print(f"\n=== Thesis cell ===")
    print(f"Convs with an H->AI uptake failure: {len(h2ai)} ({len(h2ai)/n*100:.1f}%)")
    no_repair = [r for r in h2ai if not has(r, "REPAIR_AGENT")]
    invisible = [r for r in no_repair if not has(r, "REACTION_USER")]
    print(f"  ...of those, no agent repair:        {len(no_repair)} ({len(no_repair)/len(h2ai)*100:.1f}% of uptake failures)")
    print(f"  ...AND no user reaction (INVISIBLE): {len(invisible)} ({len(invisible)/len(h2ai)*100:.1f}% of uptake failures)")
    confident = [r for r in invisible if "false_confidence" in r["ai_signal_summary"]]
    print(f"  ...AND false_confidence present:     {len(confident)} (confident-misalignment, the canonical cell)")

    # cross-channel co-occurrence
    both = [r for r in recs if has(r, "H2AI_NEG") and has(r, "AI2H_NEG")]
    print(f"\nCross-channel co-occurrence (H->AI neg AND AI->H neg): {len(both)} ({len(both)/n*100:.1f}%)")

    # ── (4) validate conversation_id -> WildChat positional join ──
    print("\n=== Join validation: annotation.turns vs WildChat.turn at positional index ===")
    ann = pd.read_json(PRED / "data/wildchat_annotations_opus_v2.json.gz")[["conversation_id", "turns"]]
    # global positional `turn` array across shards in filename order
    wc_turn = []
    for f in sorted(glob.glob(str(WILD / "*.parquet"))):
        t = pq.read_table(f, columns=["turn"]).column("turn").to_pylist()
        wc_turn.extend(t)
    print(f"WildChat rows: {len(wc_turn):,}; annotation rows: {len(ann):,}")
    ann = ann[ann.conversation_id < len(wc_turn)]
    match = sum(1 for cid, tn in zip(ann.conversation_id, ann.turns) if wc_turn[cid] == tn)
    print(f"turns match at positional index: {match}/{len(ann)} = {match/len(ann)*100:.1f}%")


if __name__ == "__main__":
    main()
