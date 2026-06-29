"""Consolidated signal→category mapping (the substrate for the criteria-design round).

Every one of the 65 predecessor signals → {l1 (direction), control_op, polarity, relation_type}.

L1 = direction of information flow across the human-AI control boundary (NOT content type):
  H2AI (uptake)     - the human's intent/constraint/correction/acceptance must reach the agent.
  AI2H (legibility) - the agent's interpretation/plan/action/state/limitation must reach the human.
L1 is orthogonal to control_op: the SAME op can sit on either direction
  (e.g. report_state: silent_assumption=H2AI uptake-failure, false_confidence=AI2H legibility-failure).

relation_type taxonomy (Jun's revision, 2026-06):
  coupling                     - a step-level coupling cell (has a control_op + L1 + polarity)   [42]
  direct_coupling_*            - a single-side defect that becomes a coupling event when a
                                 condition holds; carries an L1 direction, and where it routes to
                                 a specific cell, a control_op (report_state)                     [3]
  trigger_H2AI                 - a user-side input condition that calls for uptake, not a failure [5]
  support_feature_*            - a positive AI→H form/affect feature, not a coupling event        [10]
  outcome                      - conversation-level result, not a step cell                        [4]
  mechanism_both               - a context condition associated with both directions              [1]

L1 (direction) is populated for coupling (42) + conditional direct_coupling (3) = 45; "" otherwise.
The directional flavor of support features lives in relation_type, not L1 (not coupling events).

Run:  python src/build_control_mapping.py   ->  docs/criteria/control_mapping.csv
"""
from __future__ import annotations
import csv
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "criteria" / "control_mapping.csv"

# (signal, l1, control_op, polarity, relation_type)
ROWS = [
    # ===== coupling (42): l1 + control_op + polarity =====
    # ---- report_state (15) ----
    ("silent_assumption",            "H2AI", "report_state",      "failure",   "coupling"),
    ("ai_stated_interpretation",     "H2AI", "report_state",      "positive",  "coupling"),
    ("false_confidence",             "AI2H", "report_state",      "failure",   "coupling"),
    ("performative_hedge",           "AI2H", "report_state",      "failure",   "coupling"),
    ("problem_ignored",              "AI2H", "report_state",      "failure",   "coupling"),
    ("problem_surfaced",             "AI2H", "report_state",      "positive",  "coupling"),
    ("appropriate_confidence",       "AI2H", "report_state",      "positive",  "coupling"),
    ("appropriate_hedge",            "AI2H", "report_state",      "positive",  "coupling"),
    ("ai_hedges_uncertainty",        "AI2H", "report_state",      "positive",  "coupling"),
    ("ai_asserts_knowledge_limit",   "AI2H", "report_state",      "positive",  "coupling"),
    ("ai_provides_caveats",          "AI2H", "report_state",      "positive",  "coupling"),
    ("ai_warns_user",                "AI2H", "report_state",      "positive",  "coupling"),
    ("ai_flags_complexity",          "AI2H", "report_state",      "positive",  "coupling"),
    ("ai_cites_source",              "AI2H", "report_state",      "positive",  "coupling"),
    ("ai_implicit_refusal",          "AI2H", "report_state",      "failure",   "coupling"),
    # ---- ask_clarify (4) ----
    ("generate_without_clarifying",  "H2AI", "ask_clarify",       "failure",   "coupling"),
    ("ai_asked_clarifying_question", "H2AI", "ask_clarify",       "positive",  "coupling"),
    ("ai_offered_options",           "AI2H", "ask_clarify",       "positive",  "coupling"),
    ("user_asks_clarification",      "AI2H", "ask_clarify",       "human",     "coupling"),
    # ---- confirm_authorize (1) ----
    ("user_positive_feedback",       "H2AI", "confirm_authorize", "human",     "coupling"),
    # ---- act_execute (6) ----
    ("intent_missed",                "H2AI", "act_execute",       "failure",   "coupling"),
    ("under_delivered",              "H2AI", "act_execute",       "failure",   "coupling"),
    ("over_delivered",               "H2AI", "act_execute",       "failure",   "coupling"),
    ("off_topic_drift",              "H2AI", "act_execute",       "failure",   "coupling"),
    ("intent_addressed",             "H2AI", "act_execute",       "positive",  "coupling"),
    ("scope_matched",                "H2AI", "act_execute",       "positive",  "coupling"),
    # ---- stop_defer (1) ----
    ("ai_refuses_or_declines",       "AI2H", "stop_defer",        "positive",  "coupling"),
    # ---- maintain_state (4) ----
    ("ai_self_contradiction",        "AI2H", "maintain_state",    "failure",   "coupling"),
    ("plow_through",                 "H2AI", "maintain_state",    "failure",   "coupling"),
    ("ai_references_prior_turn",     "H2AI", "maintain_state",    "positive",  "coupling"),
    ("ai_references_user_words",     "H2AI", "maintain_state",    "positive",  "coupling"),
    # ---- recover_repair (11) ----
    ("repetition",                   "H2AI", "recover_repair",    "failure",   "coupling"),
    ("error_commitment",             "H2AI", "recover_repair",    "failure",   "coupling"),
    ("error_recovery",               "AI2H", "recover_repair",    "positive",  "coupling"),
    ("adaptation",                   "H2AI", "recover_repair",    "positive",  "coupling"),
    ("ai_provides_alternatives",     "AI2H", "recover_repair",    "positive",  "coupling"),
    ("ai_acknowledges_correction",   "H2AI", "recover_repair",    "positive",  "coupling"),
    ("user_corrects_ai",             "H2AI", "recover_repair",    "human",     "coupling"),
    ("user_implicit_correction",     "H2AI", "recover_repair",    "human",     "coupling"),
    ("user_repeats_request",         "H2AI", "recover_repair",    "human",     "coupling"),
    ("user_expresses_dissatisfaction","H2AI","recover_repair",    "escalation","coupling"),
    ("user_expresses_frustration",   "H2AI", "recover_repair",    "escalation","coupling"),

    # ===== conditional direct coupling (3): L1 direction + routing op, fires only when condition holds =====
    ("factual_error",   "AI2H", "report_state", "failure", "direct_coupling_when_material"),
    ("ai_malfunction",  "AI2H", "",             "failure", "direct_coupling"),
    ("user_misled",     "AI2H", "",             "failure", "outcome_from_direct_coupling"),

    # ===== H→AI triggers (5): input conditions, not failures =====
    ("user_ambiguous_request",      "", "", "trigger", "trigger_H2AI"),
    ("user_multi_request",          "", "", "trigger", "trigger_H2AI"),
    ("user_scope_change",           "", "", "trigger", "trigger_H2AI"),
    ("user_provides_invalid_input", "", "", "trigger", "trigger_H2AI"),
    ("user_validation_seeking",     "", "", "trigger", "trigger_H2AI"),

    # ===== AI→H support features (10): positive form/affect features, not coupling events =====
    ("ai_structured_response",  "", "", "positive", "support_feature_AI2H"),
    ("ai_provides_example",     "", "", "positive", "support_feature_AI2H"),
    ("ai_provides_step_by_step","", "", "positive", "support_feature_AI2H"),
    ("ai_summarizes",           "", "", "positive", "support_feature_AI2H"),
    ("ai_offers_to_elaborate",  "", "", "positive", "support_feature_AI2H"),
    ("ai_asked_probing_question","", "", "positive", "support_feature_AI2H"),
    ("ai_validates_user",       "", "", "positive", "rapport_support_AI2H"),
    ("ai_empathy_expressed",    "", "", "positive", "rapport_support_AI2H"),
    ("ai_normalizes_difficulty","", "", "positive", "rapport_support_AI2H"),
    ("ai_asks_for_feedback",    "", "", "positive", "support_feature_bridge"),

    # ===== outcomes (4): conversation-level results, not step cells =====
    ("conversation_stalled",  "", "", "failure",  "outcome"),
    ("conversation_advanced", "", "", "positive", "outcome"),
    ("user_empowered",        "", "", "positive", "outcome"),
    ("user_abandons_thread",  "", "", "failure",  "outcome"),

    # ===== mechanism, both-associated (1) =====
    ("ethical_tension", "", "", "context", "mechanism_both"),
]


COLUMNS = ["signal", "l1", "control_op", "polarity", "relation_type"]


def compute():
    """Pure: validate the 65-signal table and return the rows + the summary counts.

    No file writes — the CSV is emitted only by main(). Returns a dict with:
      columns, rows, relation_type, coupling_by_op, l1 (all plain dicts/lists).
    """
    assert len(ROWS) == 65, f"expected 65 signals, got {len(ROWS)}"
    assert len({r[0] for r in ROWS}) == 65, "duplicate signal names"
    rel = Counter(r[4] for r in ROWS)
    coup = Counter(r[2] for r in ROWS if r[4] == "coupling")
    l1 = Counter(r[1] for r in ROWS if r[1])
    return {
        "columns": COLUMNS,
        "rows": [list(r) for r in ROWS],
        "relation_type": dict(rel),
        "coupling_by_op": dict(coup),
        "l1": dict(l1),
    }


def main():
    res = compute()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(res["columns"])
        w.writerows(ROWS)

    print(f"wrote {OUT}  (65 signals)")
    print(f"  relation_type: {res['relation_type']}")
    print(f"  coupling by control_op: {res['coupling_by_op']}")
    print(f"  L1 populated (coupling + direct_coupling): {res['l1']}  total={sum(res['l1'].values())}")


if __name__ == "__main__":
    main()
