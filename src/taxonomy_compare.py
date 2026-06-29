"""Head-to-head: Clark grounding acts vs STPA-style control operations as Layer-2.

Deterministic, no LLM. Two questions:
  Metric A — signal coverage: how do the 65 predecessor signals (and their real mass in the
             10k corpus) distribute across each scheme's cells? Empty cells? Orphans?
  Metric B — agentic coverage: of the tool calls in the reconstructed agentic corpus, what
             fraction can each scheme place into a named cell? (Clark has no execute/seek cell.)

Both Layer-2 schemes share the same Layer-1 (2 categories: H2AI uptake / AI2H legibility;
common ground is the conversation-level ablation, not a cell). Layer-1 is carried per signal
only for reporting.

Run:  python src/taxonomy_compare.py        (writes data/derived/taxonomy_comparison.json)
"""
from __future__ import annotations
import csv, json, math, sys
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)
REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "data" / "derived" / "middle_step_10k_signals.csv"
AGENTIC = REPO / "data" / "derived" / "sharechat_agentic.jsonl"
OUT = REPO / "data" / "derived" / "taxonomy_comparison.json"

CLARK_ACTS = ["present", "clarify", "accept", "repair", "maintain"]
CONTROL_OPS = ["maintain_state", "ask_clarify", "seek_inspect", "confirm_authorize",
               "act_execute", "stop_defer", "report_state", "recover_repair"]

# ── The 65 predecessor signals on BOTH Layer-2 schemes ─────────────────────
# clark  : Clark grounding act (from docs/codebook_v1.md), or None if not a coupling cell.
# control: STPA control operation, or None if not a coupling cell.
# l1     : Layer-1 category for reporting (H2AI / AI2H / INTERACTION / None).
# pol    : failure / positive / human / escalation / neutral
# Signals with clark=control=None are the *mechanism layer* (single-side defects, triggers,
# style, outcome markers) — not a coupling cell under EITHER scheme; they don't discriminate.
SIG = {
    # ---- layer1_signals (24) ----
    "ai_asked_clarifying_question": ("clarify", "ask_clarify", "H2AI", "positive"),
    "ai_offered_options":           ("clarify", "ask_clarify", "H2AI", "positive"),
    "ai_hedges_uncertainty":        ("present", "report_state", "AI2H", "positive"),
    "ai_asserts_knowledge_limit":   ("present", "report_state", "AI2H", "positive"),
    "ai_cites_source":              ("present", "report_state", "AI2H", "positive"),
    "ai_flags_complexity":          ("present", "report_state", "AI2H", "positive"),
    "ai_validates_user":            (None, None, None, "neutral"),       # style
    "ai_empathy_expressed":         (None, None, None, "neutral"),       # style
    "ai_references_prior_turn":     ("accept", "maintain_state", "INTERACTION", "positive"),
    "ai_acknowledges_correction":   ("accept", "recover_repair", "H2AI", "positive"),
    "ai_structured_response":       (None, None, None, "neutral"),       # style
    "ai_provides_example":          (None, None, None, "neutral"),       # style
    "ai_provides_step_by_step":     (None, None, None, "neutral"),       # style
    "ai_provides_caveats":          ("present", "report_state", "AI2H", "positive"),
    "ai_warns_user":                ("present", "report_state", "AI2H", "positive"),
    "ai_refuses_or_declines":       ("present", "stop_defer", "AI2H", "positive"),  # legible refrain
    "ai_asked_probing_question":    ("clarify", "ask_clarify", "H2AI", "positive"),
    "ai_asks_for_feedback":         (None, None, None, "neutral"),       # dropped (low κ)
    "ai_normalizes_difficulty":     (None, None, None, "neutral"),       # style
    "ai_offers_to_elaborate":       (None, None, None, "neutral"),       # style
    "ai_provides_alternatives":     ("repair", "recover_repair", "INTERACTION", "positive"),
    "ai_references_user_words":     ("accept", "maintain_state", "H2AI", "positive"),
    "ai_stated_interpretation":     ("present", "report_state", "H2AI", "positive"),
    "ai_summarizes":                (None, None, None, "neutral"),       # style
    # ---- layer2_signals (24) ----
    "silent_assumption":            ("present", "report_state", "H2AI", "failure"),
    "false_confidence":             ("present", "report_state", "AI2H", "failure"),
    "appropriate_hedge":            ("present", "report_state", "AI2H", "positive"),
    "performative_hedge":           ("present", "report_state", "AI2H", "failure"),
    "adaptation":                   ("maintain", "recover_repair", "H2AI", "positive"),
    "repetition":                   ("repair", "recover_repair", "INTERACTION", "failure"),
    "plow_through":                 ("repair", "recover_repair", "H2AI", "failure"),
    "under_delivered":              ("maintain", "act_execute", "H2AI", "failure"),
    "off_topic_drift":              ("maintain", "act_execute", "H2AI", "failure"),
    "error_recovery":               ("repair", "recover_repair", "INTERACTION", "positive"),
    "error_commitment":             ("repair", "recover_repair", "INTERACTION", "failure"),
    "intent_missed":                ("maintain", "act_execute", "H2AI", "failure"),
    "user_empowered":               ("maintain", "maintain_state", "INTERACTION", "positive"),
    "user_misled":                  (None, None, None, "neutral"),       # single-side outcome
    "conversation_advanced":        ("maintain", "maintain_state", "INTERACTION", "positive"),
    "conversation_stalled":         ("maintain", "maintain_state", "INTERACTION", "failure"),
    "factual_error":                (None, None, None, "neutral"),       # single-side correctness
    "generate_without_clarifying":  ("clarify", "ask_clarify", "H2AI", "failure"),
    "appropriate_confidence":       ("present", "report_state", "AI2H", "positive"),
    "intent_addressed":             ("maintain", "act_execute", "H2AI", "positive"),
    "over_delivered":               (None, None, None, "neutral"),       # dropped (κ=0.10)
    "problem_ignored":              ("present", "report_state", "AI2H", "failure"),
    "problem_surfaced":             ("present", "report_state", "AI2H", "positive"),
    "scope_matched":                ("maintain", "act_execute", "H2AI", "positive"),
    # ---- layer3_signals (17) ----
    "user_asks_clarification":      ("clarify", "ask_clarify", "AI2H", "human"),
    "user_corrects_ai":             ("repair", "recover_repair", "H2AI", "human"),
    "user_implicit_correction":     ("repair", "recover_repair", "H2AI", "human"),
    "user_expresses_frustration":   ("repair", "recover_repair", "INTERACTION", "escalation"),
    "user_expresses_dissatisfaction": ("repair", "recover_repair", "INTERACTION", "escalation"),
    "user_validation_seeking":      (None, None, None, "neutral"),       # trigger
    "user_ambiguous_request":       (None, None, None, "neutral"),       # trigger
    "user_positive_feedback":       ("accept", "confirm_authorize", "AI2H", "positive"),  # human authorize
    "user_multi_request":           (None, None, None, "neutral"),       # trigger
    "user_abandons_thread":         (None, None, None, "neutral"),       # outcome marker
    "user_repeats_request":         ("repair", "recover_repair", "H2AI", "human"),
    "ai_self_contradiction":        ("maintain", "maintain_state", "AI2H", "failure"),
    "ai_implicit_refusal":          ("maintain", "act_execute", "H2AI", "failure"),
    "ai_malfunction":               (None, None, None, "neutral"),       # single-side defect
    "ethical_tension":              (None, None, None, "neutral"),       # other
    "user_provides_invalid_input":  (None, None, None, "neutral"),       # trigger
    "user_scope_change":            (None, None, None, "neutral"),       # trigger
}
assert len(SIG) == 65, f"expected 65 signals, got {len(SIG)}"
CLARK = {s: v[0] for s, v in SIG.items()}
CONTROL = {s: v[1] for s, v in SIG.items()}


def entropy(counter):
    tot = sum(counter.values())
    if not tot:
        return 0.0
    return -sum((c / tot) * math.log2(c / tot) for c in counter.values() if c)


def cell_summary(cells, mapping, weights=None):
    """Distribution of coupling signals (optionally prevalence-weighted) across `cells`."""
    type_count = Counter()    # # of distinct signals in each cell
    mass = Counter()          # corpus-frequency-weighted
    for sig, cell in mapping.items():
        if cell is None:
            continue
        type_count[cell] += 1
        if weights is not None:
            mass[cell] += weights.get(sig, 0)
    empty = [c for c in cells if type_count.get(c, 0) == 0]
    near_empty = [c for c in cells if type_count.get(c, 0) == 1]
    return {
        "type_count": {c: type_count.get(c, 0) for c in cells},
        "mass": {c: mass.get(c, 0) for c in cells} if weights is not None else None,
        "empty_cells": empty,
        "near_empty_cells": near_empty,
        "n_cells": len(cells),
        "n_placed_signals": sum(type_count.values()),
        "type_entropy_bits": round(entropy(type_count), 3),
        "mass_entropy_bits": round(entropy(mass), 3) if weights is not None else None,
    }


def load_corpus_freq():
    """Per-signal conversation frequency over the 10k corpus."""
    freq = Counter()
    n = 0
    with open(CORPUS, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            n += 1
            sigs = set()
            for col in ("ai_signals", "user_signals"):
                for s in (row.get(col) or "").split("|"):
                    s = s.strip()
                    if s:
                        sigs.add(s)
            for s in sigs:
                freq[s] += 1
    return freq, n


def classify_tool(tc):
    """Map a reconstructed tool call to a control op; Clark has no act for tool execution."""
    return "act_execute" if tc.get("consequential") else "seek_inspect"


def load_agentic():
    turns = tool_calls = ro = cons = 0
    agentic_turns = 0
    control_hit = clark_hit = 0   # tool calls each scheme can place in a named cell
    op_counts = Counter()
    with open(AGENTIC, encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            turns += 1
            tcs = rec.get("tool_calls") or []
            if tcs:
                agentic_turns += 1
            for tc in tcs:
                tool_calls += 1
                op = classify_tool(tc)
                op_counts[op] += 1
                if tc.get("consequential"):
                    cons += 1
                else:
                    ro += 1
                control_hit += 1          # seek_inspect / act_execute are real control cells
                clark_hit += 0            # no Clark act instantiates a tool execution
    return {
        "n_turns": turns, "agentic_turns": agentic_turns, "tool_calls": tool_calls,
        "read_only": ro, "consequential": cons,
        "op_counts": dict(op_counts),
        "control_coverage_pct": round(100 * control_hit / tool_calls, 1) if tool_calls else 0,
        "clark_coverage_pct": round(100 * clark_hit / tool_calls, 1) if tool_calls else 0,
    }


def compute():
    """Pure: assemble and return the Clark-vs-control comparison result dict (no file write)."""
    freq, n_corpus = load_corpus_freq()
    coupling = [s for s in SIG if SIG[s][0] is not None]
    mechanism = [s for s in SIG if SIG[s][0] is None]
    orphans_clark = [s for s in coupling if CLARK[s] is None]
    orphans_control = [s for s in coupling if CONTROL[s] is None]

    clark = cell_summary(CLARK_ACTS, CLARK, freq)
    control = cell_summary(CONTROL_OPS, CONTROL, freq)
    agentic = load_agentic()

    return {
        "corpus": {"n_conversations": n_corpus, "n_signals_total": len(SIG),
                   "n_coupling_signals": len(coupling), "n_mechanism_signals": len(mechanism)},
        "metric_A_signal_coverage": {
            "clark_5_acts": clark,
            "control_8_ops": control,
            "orphans_clark": orphans_clark,
            "orphans_control": orphans_control,
        },
        "metric_B_agentic_coverage": agentic,
        "mechanism_signals": mechanism,
    }


def main():
    result = compute()
    clark = result["metric_A_signal_coverage"]["clark_5_acts"]
    control = result["metric_A_signal_coverage"]["control_8_ops"]
    agentic = result["metric_B_agentic_coverage"]
    coupling_n = result["corpus"]["n_coupling_signals"]
    OUT.write_text(json.dumps(result, indent=2))

    # ── printed summary ──
    print(f"=== Metric A — signal coverage ({coupling_n} coupling signals of {len(SIG)}) ===\n")
    print(f"{'cell':18s} {'Clark #sig':>10s}   |   {'cell':18s} {'Control #sig':>12s}")
    for i in range(max(len(CLARK_ACTS), len(CONTROL_OPS))):
        l = CLARK_ACTS[i] if i < len(CLARK_ACTS) else ""
        r = CONTROL_OPS[i] if i < len(CONTROL_OPS) else ""
        lc = clark["type_count"].get(l, "") if l else ""
        rc = control["type_count"].get(r, "") if r else ""
        print(f"{l:18s} {str(lc):>10s}   |   {r:18s} {str(rc):>12s}")
    print(f"\nClark   : {clark['n_cells']} acts, empty={clark['empty_cells']}, "
          f"near_empty={clark['near_empty_cells']}, entropy(types)={clark['type_entropy_bits']} bits, "
          f"entropy(mass)={clark['mass_entropy_bits']} bits")
    print(f"Control : {control['n_cells']} ops, empty={control['empty_cells']}, "
          f"near_empty={control['near_empty_cells']}, entropy(types)={control['type_entropy_bits']} bits, "
          f"entropy(mass)={control['mass_entropy_bits']} bits")

    print("\nControl op mass (conv-freq weighted, the cells that carry real chat data):")
    for op in CONTROL_OPS:
        print(f"  {op:18s} types={control['type_count'][op]:2d}  mass={control['mass'][op]:6d}")

    print(f"\n=== Metric B — agentic coverage (corpus: {agentic['n_turns']} turns) ===")
    print(f"agentic turns (>=1 tool call): {agentic['agentic_turns']}; tool calls: {agentic['tool_calls']} "
          f"(read-only {agentic['read_only']}, consequential {agentic['consequential']})")
    print(f"tool calls placed in a named cell:  Control {agentic['control_coverage_pct']}%  |  "
          f"Clark {agentic['clark_coverage_pct']}%  (Clark has no act for tool execution)")
    print(f"control op distribution of tool calls: {agentic['op_counts']}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
