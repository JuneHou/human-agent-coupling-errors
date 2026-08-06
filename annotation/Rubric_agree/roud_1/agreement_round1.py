#!/usr/bin/env python3
"""Round-1 three-annotator agreement analysis (Stage 1 signal annotation).

Computes pre-refinement inter-annotator agreement on the 10-conversation
agreement set (C1-C10, 441 content blocks, 50 signals) between:

  A = junh    (Label Studio project 1, ShareChat-Test; development labels)
  B = zhenyub (project 2, ShareChat-Agreement-B)
  F = yif     (project 3, ShareChat-Agreement-F)

Unit: binary presence of each signal per content block (methods.md 3.2.4).
Primary statistic: per-signal pairwise Cohen's kappa for the three pairs,
with pairwise mean and minimum (sklearn.metrics.cohen_kappa_score).
Supplementary: per-signal Fleiss' kappa over the 441x3 rating matrix
(statsmodels.stats.inter_rater.aggregate_raters + fleiss_kappa).
Sensitivity: (a) conversation-level presence kappa (10 units);
(b) eligibility-masked kappa restricted to blocks whose author role the
signal checklist allows for that signal.

Kappa is reported as n/a (empty cell) for a pair whenever either rater's
vector is constant; observed agreement P_o and per-rater positive counts
are always reported, so unmeasurable signals stay visible.

Outputs (deterministic; no timestamps):
  agreement_round1_kappa.csv          per-signal statistics
  agreement_round1_disagreements.csv  every (conversation, block, signal)
                                      cell where the three raters diverge

Usage:
    python annotation/Rubric_agree/agreement_round1.py [--db PATH]
"""

import argparse
import csv
import json
import re
import sqlite3
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.inter_rater import aggregate_raters, fleiss_kappa

DEFAULT_DB = "/data/wang/junh/label-studio-data/label_studio.sqlite3"
# annotation/ located by name so the script survives reorganisation below it.
ANNOT_DIR = next(p for p in Path(__file__).resolve().parents
                 if p.name == "annotation")
OUT_DIR = Path(__file__).resolve().parent        # .../Rubric_agree/roud_1/

RATER_BY_PROJECT = {1: "A", 2: "B", 3: "F"}
RATERS = ["A", "B", "F"]
PAIRS = list(combinations(RATERS, 2))  # AB, AF, BF
SPAN_TEXT_LIMIT = 160


def load_conv_map():
    """C1-C10 -> conv_id (verbatim, incl. any query string) and back."""
    rows = list(csv.DictReader(open(ANNOT_DIR / "agreement_set_convid_map.csv")))
    by_conv = {r["conv_id"]: r["c_index"] for r in rows}
    order = [r["c_index"] for r in rows]
    return by_conv, order


def load_signals():
    """The 50-signal universe = labels in the Label Studio config."""
    text = (ANNOT_DIR / "label_studio_config.xml").read_text()
    return sorted(set(re.findall(r'<Label value="([^"]+)"', text)))


def load_allowed_blocks():
    """signal -> set of block author roles the checklist defines for it."""
    allowed = defaultdict(set)
    for r in csv.DictReader(open(ANNOT_DIR / "signal_checklist.csv")):
        allowed[r["signal"]].add(r["block"])
    return dict(allowed)


def load_rubric_index():
    """signal -> (allowed blocks per rubric, number of decision steps)."""
    rubric = json.loads((ANNOT_DIR / "sharechat_rubric.json").read_text())
    index = {}
    for name, entry in rubric.get("signals", {}).items():
        index[name] = {
            "blocks": entry.get("blocks", []),
            "n_steps": len(entry.get("decision_steps", [])),
        }
    return index


def load_annotations(db_path, conv_to_c):
    """Read the three raters' submitted annotations for C1-C10.

    Returns:
      dialogues: c_index -> list of author roles (verified identical
                 across the three projects)
      presence:  rater -> set of (c_index, block_idx, signal)
      spans:     (rater, c_index, block_idx, signal) -> list of span texts
      counts:    rater -> {"spans": int, "labels": int}
    """
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    rows = con.execute(
        """SELECT t.project_id, tc.completed_by_id, t.data, tc.result
           FROM task_completion tc JOIN task t ON t.id = tc.task_id
           WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL
             AND t.project_id IN (1, 2, 3)"""
    ).fetchall()
    con.close()

    dialogues = {}
    presence = {r: set() for r in RATERS}
    spans = defaultdict(list)
    counts = {r: {"spans": 0, "labels": 0} for r in RATERS}

    for project_id, completed_by, data, result in rows:
        rater = RATER_BY_PROJECT[project_id]
        assert completed_by == project_id, (
            f"project {project_id} annotated by user {completed_by}; "
            "attribution assumption broken")
        payload = json.loads(data)
        c_index = conv_to_c.get(payload.get("conv_id"))
        if c_index is None:
            continue  # project 1 holds 148 tasks; keep only the 10
        authors = [b.get("author", "?") for b in payload["dialogue"]]
        if c_index in dialogues:
            assert dialogues[c_index] == authors, (
                f"{c_index}: dialogue differs between projects")
        else:
            dialogues[c_index] = authors

        for item in json.loads(result):
            if item.get("type") != "paragraphlabels":
                continue  # drop the 'notes' textarea control
            value = item.get("value", {})
            idx = int(value["start"])
            assert int(value["end"]) == idx, (
                f"{c_index}: cross-block span at block {idx}")
            labels = value.get("paragraphlabels", [])
            counts[rater]["spans"] += 1
            counts[rater]["labels"] += len(labels)
            text = (value.get("text") or "").replace("\n", " ").strip()
            for signal in labels:
                presence[rater].add((c_index, idx, signal))
                spans[(rater, c_index, idx, signal)].append(
                    text[:SPAN_TEXT_LIMIT])

    return dialogues, presence, spans, counts


def pairwise_kappa(x, y):
    """Cohen's kappa; None (n/a) when either vector is constant."""
    if len(set(x)) < 2 or len(set(y)) < 2:
        return None
    return float(cohen_kappa_score(x, y))


def percent_agreement(x, y):
    return sum(a == b for a, b in zip(x, y)) / len(x)


def fleiss(vectors):
    """Fleiss' kappa over subjects x raters; None when degenerate."""
    subjects = list(zip(*vectors))
    if len({v for row in subjects for v in row}) < 2:
        return None
    table, _ = aggregate_raters(subjects, n_cat=2)
    k = fleiss_kappa(table, method="fleiss")
    return None if k != k else float(k)  # NaN guard


def signal_row(signal, cells, presence, mask_cells, conv_order):
    """All statistics for one signal. cells = ordered (c, block) universe."""
    vec = {r: [int((c, b, signal) in presence[r]) for c, b in cells]
           for r in RATERS}
    row = {"signal": signal, "n_cells": len(cells)}
    for r in RATERS:
        row[f"n_pos_{r}"] = sum(vec[r])

    kappas = []
    for r1, r2 in PAIRS:
        k = pairwise_kappa(vec[r1], vec[r2])
        row[f"kappa_{r1}{r2}"] = round(k, 3) if k is not None else ""
        row[f"po_{r1}{r2}"] = round(percent_agreement(vec[r1], vec[r2]), 3)
        if k is not None:
            kappas.append(k)
    row["kappa_mean"] = round(sum(kappas) / len(kappas), 3) if kappas else ""
    row["kappa_min"] = round(min(kappas), 3) if kappas else ""

    fk = fleiss([vec[r] for r in RATERS])
    row["fleiss_kappa"] = round(fk, 3) if fk is not None else ""

    # Sensitivity (a): conversation-level presence, 10 units.
    convs = conv_order
    cvec = {r: [int(any((c, b, signal) in presence[r]
                        for c, b in cells if c == cv)) for cv in convs]
            for r in RATERS}
    ck = [k for r1, r2 in PAIRS
          if (k := pairwise_kappa(cvec[r1], cvec[r2])) is not None]
    row["conv_kappa_mean"] = round(sum(ck) / len(ck), 3) if ck else ""

    # Sensitivity (b): eligibility-masked, checklist-allowed blocks only.
    mcells = mask_cells[signal]
    if mcells:
        mvec = {r: [int((c, b, signal) in presence[r]) for c, b in mcells]
                for r in RATERS}
        mk = [k for r1, r2 in PAIRS
              if (k := pairwise_kappa(mvec[r1], mvec[r2])) is not None]
        row["masked_kappa_mean"] = round(sum(mk) / len(mk), 3) if mk else ""
    else:
        row["masked_kappa_mean"] = ""
    row["masked_n_cells"] = len(mcells)
    return row


def disagreement_rows(signals, cells, dialogues, presence, spans,
                      allowed_blocks, rubric_index):
    """One row per (conversation, block, signal) cell without 3-way consensus."""
    block_labels = {r: defaultdict(set) for r in RATERS}
    for r in RATERS:
        for c, b, s in presence[r]:
            block_labels[r][(c, b)].add(s)

    rows = []
    for signal in signals:
        for c, b in cells:
            votes = {r: int((c, b, signal) in presence[r]) for r in RATERS}
            if len(set(votes.values())) == 1:
                continue
            role = dialogues[c][b]
            rub = rubric_index.get(signal)
            row = {
                "signal": signal, "c_index": c, "block_idx": b,
                "block_role": role,
                "role_allowed": int(role in allowed_blocks.get(signal, set())),
                "A": votes["A"], "B": votes["B"], "F": votes["F"],
                "pattern": "".join(str(votes[r]) for r in RATERS),
            }
            for r in RATERS:
                row[f"span_{r}"] = " | ".join(
                    spans.get((r, c, b, signal), []))
                others = sorted(block_labels[r][(c, b)] - {signal})
                row[f"other_labels_{r}"] = ";".join(others)
            row["rubric_entry"] = (
                f"sharechat_rubric.json v0.5, {rub['n_steps']} decision steps"
                if rub else "no rubric entry (v0.5)")
            row["diverged_at_step"] = ""  # filled during reconciliation
            rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    conv_to_c, conv_order = load_conv_map()
    signals = load_signals()
    allowed_blocks = load_allowed_blocks()
    rubric_index = load_rubric_index()

    dialogues, presence, spans, counts = load_annotations(args.db, conv_to_c)
    assert sorted(dialogues) == sorted(conv_order)

    # The block universe: every content block of every agreement conversation.
    cells = [(c, b) for c in conv_order for b in range(len(dialogues[c]))]
    mask_cells = {s: [(c, b) for c, b in cells
                      if dialogues[c][b] in allowed_blocks.get(s, set())]
                  for s in signals}

    print("Extraction totals (spans / label instances):")
    for r in RATERS:
        print(f"  {r}: {counts[r]['spans']} / {counts[r]['labels']}")
    role_totals = defaultdict(int)
    for c in conv_order:
        for role in dialogues[c]:
            role_totals[role] += 1
    print(f"Universe: {len(cells)} blocks x {len(signals)} signals; "
          f"roles: {dict(sorted(role_totals.items()))}")

    out_of_vocab = {s for r in RATERS for _, _, s in presence[r]
                    if s not in signals}
    assert not out_of_vocab, f"labels outside the 50-signal set: {out_of_vocab}"

    kappa_rows = [signal_row(s, cells, presence, mask_cells, conv_order)
                  for s in signals]
    kappa_path = OUT_DIR / "agreement_round1_kappa.csv"
    with open(kappa_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(kappa_rows[0]))
        writer.writeheader()
        writer.writerows(kappa_rows)

    dis_rows = disagreement_rows(signals, cells, dialogues, presence, spans,
                                 allowed_blocks, rubric_index)
    dis_path = OUT_DIR / "agreement_round1_disagreements.csv"
    with open(dis_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(dis_rows[0]))
        writer.writeheader()
        writer.writerows(dis_rows)

    # Console summary.
    measured = [r for r in kappa_rows if r["kappa_mean"] != ""]
    print(f"\nSignals with a defined pairwise kappa: {len(measured)}"
          f" of {len(signals)}")
    for label, key in [("pairwise mean", "kappa_mean"),
                       ("pairwise min", "kappa_min")]:
        vals = [r[key] for r in measured]
        print(f"Macro-average of {label}: {sum(vals) / len(vals):.3f}")
    for pair in ["AB", "AF", "BF"]:
        vals = [r[f"kappa_{pair}"] for r in kappa_rows
                if r[f"kappa_{pair}"] != ""]
        print(f"kappa_{pair}: defined for {len(vals)} signals, "
              f"macro-average {sum(vals) / len(vals):.3f}")
    bands = {">=0.6": 0, "0.4-0.6": 0, "<0.4": 0, "n/a": 0}
    for r in kappa_rows:
        k = r["kappa_mean"]
        if k == "":
            bands["n/a"] += 1
        elif k >= 0.6:
            bands[">=0.6"] += 1
        elif k >= 0.4:
            bands["0.4-0.6"] += 1
        else:
            bands["<0.4"] += 1
    print(f"Bands (pairwise mean): {bands}")
    print(f"Disagreement cells (no 3-way consensus): {len(dis_rows)}")
    print(f"Wrote {kappa_path.name}, {dis_path.name}")


if __name__ == "__main__":
    main()
