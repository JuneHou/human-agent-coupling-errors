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
import random
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
RATER_USER_ID_R1 = {"A": 1, "B": 2, "F": 3}  # htx_user.id per round-1 rater
ROUND1_CONV_MAP = ANNOT_DIR / "agreement_set_convid_map.csv"
SPAN_TEXT_LIMIT = 160

# Round 2 (2026-09-14): Jun ("A") vs Michelle ("M"). Unlike round 1's one
# dedicated LS project per rater, "A" here is Jun's own solo annotation of
# these 10 conversations inside project 1 (the shared 703-conversation
# corpus), filtered down by conv_id the same way project 1's other 693 tasks
# are already filtered out in load_annotations below -- so project id and
# user id are not the same thing here and RATER_USER_ID makes that explicit
# rather than relying on the round-1 completed_by == project_id coincidence.
RATER_BY_PROJECT_R2 = {1: "A", 5: "M"}
RATERS_R2 = ["A", "M"]
RATER_USER_ID_R2 = {"A": 1, "M": 5}
ROUND2_DIR = OUT_DIR.parent / "round_2"          # .../Rubric_agree/round_2/
ROUND2_CONV_MAP = ROUND2_DIR / "agreement_set_round2.csv"

# Priya (2026-09-19): same 10-conversation round-2 set, project 4 instead of
# project 5. Only a subset is completed at any given time, so --priya reads
# ROUND2_PRIYA_CONV_MAP (a hand-kept subset of ROUND2_CONV_MAP's rows,
# regenerated as she finishes more) rather than the full 10.
RATER_BY_PROJECT_PRIYA = {1: "A", 4: "P"}
RATERS_PRIYA = ["A", "P"]
RATER_USER_ID_PRIYA = {"A": 1, "P": 4}
ROUND2_PRIYA_CONV_MAP = ROUND2_DIR / "agreement_set_round2_priya_done.csv"


def load_conv_map(path=None):
    """c_index -> conv_id (verbatim, incl. any query string) and back.

    Round-1's map (default) has no comment lines; round-2's has 2 leading
    `#` lines before the header -- both are tolerated by skipping any line
    starting with `#`.
    """
    path = path or ANNOT_DIR / "agreement_set_convid_map.csv"
    rows = list(csv.DictReader(l for l in open(path) if not l.startswith("#")))
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


def load_annotations(db_path, conv_to_c, raters=None, rater_by_project=None,
                     rater_user_id=None):
    """Read the raters' submitted annotations for the given conversation set.

    Defaults reproduce round 1 (A/B/F, projects 1-3, completed_by == project_id).
    For round 2, pass raters=RATERS_R2, rater_by_project=RATER_BY_PROJECT_R2,
    rater_user_id=RATER_USER_ID_R2 -- see the module-level comment above those.

    Returns:
      dialogues: c_index -> list of author roles (verified identical
                 across raters)
      presence:  rater -> set of (c_index, block_idx, signal)
      spans:     (rater, c_index, block_idx, signal) -> list of span texts
      counts:    rater -> {"spans": int, "labels": int}
    """
    raters = raters or RATERS
    rater_by_project = rater_by_project or RATER_BY_PROJECT
    rater_user_id = rater_user_id or RATER_USER_ID_R1
    project_ids = tuple(rater_by_project)

    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    placeholders = ",".join("?" * len(project_ids))
    rows = con.execute(
        f"""SELECT t.project_id, tc.completed_by_id, t.data, tc.result
           FROM task_completion tc JOIN task t ON t.id = tc.task_id
           WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL
             AND t.project_id IN ({placeholders})""", project_ids
    ).fetchall()
    con.close()

    dialogues = {}
    presence = {r: set() for r in raters}
    spans = defaultdict(list)
    counts = {r: {"spans": 0, "labels": 0} for r in raters}

    for project_id, completed_by, data, result in rows:
        rater = rater_by_project[project_id]
        assert completed_by == rater_user_id[rater], (
            f"project {project_id} ({rater}) annotated by user {completed_by}, "
            f"expected {rater_user_id[rater]}")
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


def signal_row(signal, cells, presence, mask_cells, conv_order, raters):
    """All statistics for one signal. cells = ordered (c, block) universe."""
    pairs = list(combinations(raters, 2))
    vec = {r: [int((c, b, signal) in presence[r]) for c, b in cells]
           for r in raters}
    row = {"signal": signal, "n_cells": len(cells)}
    for r in raters:
        row[f"n_pos_{r}"] = sum(vec[r])

    kappas = []
    for r1, r2 in pairs:
        k = pairwise_kappa(vec[r1], vec[r2])
        row[f"kappa_{r1}{r2}"] = round(k, 3) if k is not None else ""
        row[f"po_{r1}{r2}"] = round(percent_agreement(vec[r1], vec[r2]), 3)
        if k is not None:
            kappas.append(k)
    row["kappa_mean"] = round(sum(kappas) / len(kappas), 3) if kappas else ""
    row["kappa_min"] = round(min(kappas), 3) if kappas else ""

    fk = fleiss([vec[r] for r in raters])
    row["fleiss_kappa"] = round(fk, 3) if fk is not None else ""

    # Sensitivity (a): conversation-level presence, 10 units.
    convs = conv_order
    cvec = {r: [int(any((c, b, signal) in presence[r]
                        for c, b in cells if c == cv)) for cv in convs]
            for r in raters}
    ck = [k for r1, r2 in pairs
          if (k := pairwise_kappa(cvec[r1], cvec[r2])) is not None]
    row["conv_kappa_mean"] = round(sum(ck) / len(ck), 3) if ck else ""

    # Sensitivity (b): eligibility-masked, checklist-allowed blocks only.
    mcells = mask_cells[signal]
    if mcells:
        mvec = {r: [int((c, b, signal) in presence[r]) for c, b in mcells]
                for r in raters}
        mk = [k for r1, r2 in pairs
              if (k := pairwise_kappa(mvec[r1], mvec[r2])) is not None]
        row["masked_kappa_mean"] = round(sum(mk) / len(mk), 3) if mk else ""
    else:
        row["masked_kappa_mean"] = ""
    row["masked_n_cells"] = len(mcells)
    return row


def disagreement_rows(signals, cells, dialogues, presence, spans,
                      allowed_blocks, rubric_index, raters):
    """One row per (conversation, block, signal) cell without full consensus
    among `raters`."""
    block_labels = {r: defaultdict(set) for r in raters}
    for r in raters:
        for c, b, s in presence[r]:
            block_labels[r][(c, b)].add(s)

    rows = []
    for signal in signals:
        for c, b in cells:
            votes = {r: int((c, b, signal) in presence[r]) for r in raters}
            if len(set(votes.values())) == 1:
                continue
            role = dialogues[c][b]
            rub = rubric_index.get(signal)
            row = {
                "signal": signal, "c_index": c, "block_idx": b,
                "block_role": role,
                "role_allowed": int(role in allowed_blocks.get(signal, set())),
            }
            row.update({r: votes[r] for r in raters})
            row["pattern"] = "".join(str(votes[r]) for r in raters)
            for r in raters:
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


def draw_round2(db_path, seed, size=10, min_blocks=0, strategy="random",
                write=True):
    """Draw the round-2 blind set from the 148 conversations A has annotated,
    excluding the round-1 agreement 10, and report the statistics Jun reviews
    before any Label Studio setup: block structure per conversation and the
    signal coverage implied by A's existing v0.5 labels.

    Read-only. Deterministic for a given seed (the seed is recorded in the
    output file header, so a redraw is auditable).
    """
    conv_to_c, _ = load_conv_map()
    round1 = set(conv_to_c)

    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    rows = con.execute(
        """SELECT t.data, tc.result FROM task_completion tc
           JOIN task t ON t.id = tc.task_id
           WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL
             AND t.project_id = 1"""
    ).fetchall()
    con.close()

    pool = {}
    for data, result in rows:
        payload = json.loads(data)
        cid = payload.get("conv_id")
        authors = [b.get("author", "?") for b in payload["dialogue"]]
        fired = {s for item in json.loads(result)
                 if item.get("type") == "paragraphlabels"
                 for s in item.get("value", {}).get("paragraphlabels", [])}
        n_labels = sum(len(item.get("value", {}).get("paragraphlabels", []))
                       for item in json.loads(result)
                       if item.get("type") == "paragraphlabels")
        pool[cid] = {"authors": authors, "signals": fired, "labels": n_labels}

    signals = set(load_signals())
    candidates = sorted(cid for cid in pool if cid not in round1
                        and len(pool[cid]["authors"]) >= min_blocks)
    rng = random.Random(seed)
    if strategy == "coverage":
        # Greedy set cover over the signals A fired, so the round-2 set exercises
        # as many of the v0.6 rules as 10 conversations can. Ties (and the tail,
        # once nothing new is left to cover) are broken by a seeded shuffle, so
        # the choice is still not hand-picked per conversation.
        shuffled, drawn, covered = candidates[:], [], set()
        rng.shuffle(shuffled)
        while len(drawn) < size and shuffled:
            best = max(shuffled, key=lambda c: (
                len((pool[c]["signals"] & signals) - covered),
                len(pool[c]["authors"])))
            drawn.append(best)
            covered |= pool[best]["signals"] & signals
            shuffled.remove(best)
        drawn = sorted(drawn)
    else:
        drawn = sorted(rng.sample(candidates, size))

    def coverage(cids):
        seen = set()
        for cid in cids:
            seen |= pool[cid]["signals"]
        return seen & signals

    def role_counts(cids):
        roles = defaultdict(int)
        for cid in cids:
            for a in pool[cid]["authors"]:
                roles[a] += 1
        return roles

    r1_present = [c for c in round1 if c in pool]
    print(f"ROUND-2 DRAW  seed={seed}  size={size}  strategy={strategy}  "
          f"min_blocks={min_blocks}")
    print(f"pool: {len(candidates)} eligible conversations "
          f"(A-annotated, not in the round-1 {len(round1)}"
          f"{f', >= {min_blocks} blocks' if min_blocks else ''})\n")

    print("drawn conversations")
    print(f"  {'#':<3} {'conv_id':<40} {'blocks':>6} {'human':>6} {'ai':>4} "
          f"{'reas':>5} {'code':>5} {'anly':>5} {'labels':>7} {'signals':>8}")
    for i, cid in enumerate(drawn, 1):
        rec = pool[cid]
        rc = defaultdict(int)
        for a in rec["authors"]:
            rc[a] += 1
        print(f"  R{i:<2} {cid[:40]:<40} {len(rec['authors']):>6} "
              f"{rc['human']:>6} {rc['ai']:>4} {rc['reasoning']:>5} "
              f"{rc['code']:>5} {rc['analysis']:>5} {rec['labels']:>7} "
              f"{len(rec['signals'] & signals):>8}")

    drawn_roles, r1_roles = role_counts(drawn), role_counts(r1_present)
    print(f"\n{'':<22}{'round-2 draw':>14}{'round-1 set':>14}{'138 pool':>12}")
    print(f"  {'conversations':<20}{len(drawn):>14}{len(r1_present):>14}"
          f"{len(candidates):>12}")
    print(f"  {'blocks':<20}{sum(drawn_roles.values()):>14}"
          f"{sum(r1_roles.values()):>14}"
          f"{sum(len(pool[c]['authors']) for c in candidates):>12}")
    for role in ("human", "ai", "reasoning", "code", "analysis"):
        print(f"  {'  ' + role:<20}{drawn_roles[role]:>14}{r1_roles[role]:>14}"
              f"{sum(1 for c in candidates for a in pool[c]['authors'] if a == role):>12}")
    print(f"  {'A labels (v0.5)':<20}{sum(pool[c]['labels'] for c in drawn):>14}"
          f"{sum(pool[c]['labels'] for c in r1_present):>14}"
          f"{sum(pool[c]['labels'] for c in candidates):>12}")

    cov_draw, cov_r1, cov_pool = (coverage(drawn), coverage(r1_present),
                                  coverage(candidates))
    print(f"\nsignal coverage (signals A fired at least once; universe "
          f"{len(signals)} after the v0.6 drop)")
    print(f"  {'in the round-2 draw':<28}{len(cov_draw):>4}")
    print(f"  {'in the round-1 set':<28}{len(cov_r1):>4}")
    print(f"  {'anywhere in the 138 pool':<28}{len(cov_pool):>4}")
    missing = sorted(cov_pool - cov_draw)
    print(f"\n  present in the pool but NOT in the draw ({len(missing)}) — these "
          f"signals get no round-2 evidence:")
    for s in missing:
        n = sum(1 for c in candidates if s in pool[c]["signals"])
        print(f"    {s:<34} (in {n}/{len(candidates)} pool conversations)")
    never = sorted(signals - cov_pool)
    if never:
        print(f"\n  never fired by A anywhere in the pool ({len(never)}): "
              f"{', '.join(never)}")
    only_r1 = sorted(cov_r1 - cov_draw)
    if only_r1:
        print(f"\n  covered in round 1 but not in this draw ({len(only_r1)}): "
              f"{', '.join(only_r1)}")

    if not write:
        return
    out_dir = OUT_DIR.parent / "round_2"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "agreement_set_round2.csv"
    with open(out_path, "w", newline="") as f:
        f.write(f"# round-2 blind agreement set; drawn from the {len(candidates)} "
                f"project-1 conversations A annotated, excluding the round-1 10\n")
        f.write(f"# seed={seed} size={size} rubric=v0.6\n")
        w = csv.writer(f)
        w.writerow(["c_index", "conv_id"])
        for i, cid in enumerate(drawn, 1):
            w.writerow([f"R{i}", cid])
    print(f"\nwrote {out_path}")

    # Import-ready task file for the two round-2 Label Studio projects. The
    # projects themselves are created through the UI (the project row carries
    # derived fields - parsed_label_config, label_config_hash, control_weights -
    # that only the UI regenerates correctly), then this file is uploaded to
    # each of them unchanged, so B and F see byte-identical tasks.
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    payloads = {}
    for data, in con.execute(
            "SELECT data FROM task WHERE project_id = 1"):
        payload = json.loads(data)
        if payload.get("conv_id") in set(drawn):
            payloads[payload["conv_id"]] = payload
    con.close()
    tasks = [{"data": payloads[cid]} for cid in drawn]
    tasks_path = out_dir / "tasks_round2.json"
    tasks_path.write_text(json.dumps(tasks, ensure_ascii=False, indent=1) + "\n")
    n_blocks = sum(len(t["data"]["dialogue"]) for t in tasks)
    print(f"wrote {tasks_path}  ({len(tasks)} tasks, {n_blocks} blocks) "
          f"- upload to BOTH round-2 projects")


def compute_agreement(db_path, raters, rater_by_project, rater_user_id,
                      conv_map_path, out_dir, out_prefix):
    """Load annotations for `raters` and write the kappa + disagreement CSVs.

    conv_map_path=None reproduces round 1's default conv map. Shared by both
    the round-1 (--round2 unset) and round-2 (--round2) CLI paths in main().
    """
    conv_to_c, conv_order = load_conv_map(conv_map_path)
    signals = load_signals()
    allowed_blocks = load_allowed_blocks()
    rubric_index = load_rubric_index()

    dialogues, presence, spans, counts = load_annotations(
        db_path, conv_to_c, raters, rater_by_project, rater_user_id)
    assert sorted(dialogues) == sorted(conv_order)

    # The block universe: every content block of every agreement conversation.
    cells = [(c, b) for c in conv_order for b in range(len(dialogues[c]))]
    mask_cells = {s: [(c, b) for c, b in cells
                      if dialogues[c][b] in allowed_blocks.get(s, set())]
                  for s in signals}

    print("Extraction totals (spans / label instances):")
    for r in raters:
        print(f"  {r}: {counts[r]['spans']} / {counts[r]['labels']}")
    role_totals = defaultdict(int)
    for c in conv_order:
        for role in dialogues[c]:
            role_totals[role] += 1
    print(f"Universe: {len(cells)} blocks x {len(signals)} signals; "
          f"roles: {dict(sorted(role_totals.items()))}")

    out_of_vocab = {s for r in raters for _, _, s in presence[r]
                    if s not in signals}
    assert not out_of_vocab, f"labels outside the signal set: {out_of_vocab}"

    out_dir.mkdir(exist_ok=True)

    kappa_rows = [signal_row(s, cells, presence, mask_cells, conv_order, raters)
                  for s in signals]
    kappa_path = out_dir / f"{out_prefix}_kappa.csv"
    with open(kappa_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(kappa_rows[0]))
        writer.writeheader()
        writer.writerows(kappa_rows)

    dis_rows = disagreement_rows(signals, cells, dialogues, presence, spans,
                                 allowed_blocks, rubric_index, raters)
    dis_path = out_dir / f"{out_prefix}_disagreements.csv"
    if dis_rows:
        with open(dis_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(dis_rows[0]))
            writer.writeheader()
            writer.writerows(dis_rows)
    else:
        dis_path.write_text("")

    # Console summary.
    measured = [r for r in kappa_rows if r["kappa_mean"] != ""]
    print(f"\nSignals with a defined pairwise kappa: {len(measured)}"
          f" of {len(signals)}")
    for label, key in [("pairwise mean", "kappa_mean"),
                       ("pairwise min", "kappa_min")]:
        vals = [r[key] for r in measured]
        print(f"Macro-average of {label}: {sum(vals) / len(vals):.3f}")
    for r1, r2 in combinations(raters, 2):
        pair = f"{r1}{r2}"
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
    print(f"Disagreement cells (no full consensus): {len(dis_rows)}")
    print(f"Wrote {kappa_path.name}, {dis_path.name}")


def review_packet(signal, db_path=DEFAULT_DB, raters=None, rater_by_project=None,
                  rater_user_id=None, conv_map_path=None):
    """Print every disagreement cell for one signal with full, untruncated
    context: the block's full text, each rater's full highlighted span (not
    the 160-char SPAN_TEXT_LIMIT slice used in the disagreement CSV), and the
    signal's full decision_steps + boundary_notes text from the rubric.

    Self-contained -- does its own DB read rather than extending
    load_annotations()'s return shape, so existing callers (main()'s round-1
    path, triage_meeting1.py's `_, presence, spans, _ = ar.load_annotations(...)`
    4-value unpack) are completely unaffected.

    Defaults to the round-2 rater set (Jun "A" vs Michelle "M"); pass the
    round-1 RATERS/RATER_BY_PROJECT/RATER_USER_ID_R1/conv map to review a
    round-1 signal instead.
    """
    raters = raters or RATERS_R2
    rater_by_project = rater_by_project or RATER_BY_PROJECT_R2
    rater_user_id = rater_user_id or RATER_USER_ID_R2
    conv_map_path = conv_map_path or ROUND2_CONV_MAP
    project_ids = tuple(rater_by_project)

    conv_to_c, conv_order = load_conv_map(conv_map_path)
    rubric = json.loads((ANNOT_DIR / "sharechat_rubric.json").read_text())
    entry = rubric.get("signals", {}).get(signal)

    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    placeholders = ",".join("?" * len(project_ids))
    rows = con.execute(
        f"""SELECT t.project_id, tc.completed_by_id, t.data, tc.result
           FROM task_completion tc JOIN task t ON t.id = tc.task_id
           WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL
             AND t.project_id IN ({placeholders})""", project_ids
    ).fetchall()
    con.close()

    block_texts = {}   # c_index -> [block text, ...]
    block_roles = {}   # c_index -> [author, ...]
    full_spans = defaultdict(list)   # (rater, c_index, block, signal) -> [full text]
    presence = {r: set() for r in raters}

    for project_id, completed_by, data, result in rows:
        rater = rater_by_project[project_id]
        assert completed_by == rater_user_id[rater], (
            f"project {project_id} ({rater}) annotated by user {completed_by}, "
            f"expected {rater_user_id[rater]}")
        payload = json.loads(data)
        c_index = conv_to_c.get(payload.get("conv_id"))
        if c_index is None:
            continue
        if c_index not in block_texts:
            block_texts[c_index] = [b.get("text", "") for b in payload["dialogue"]]
            block_roles[c_index] = [b.get("author", "?") for b in payload["dialogue"]]
        for item in json.loads(result):
            if item.get("type") != "paragraphlabels":
                continue
            value = item.get("value", {})
            idx = int(value["start"])
            labels = value.get("paragraphlabels", [])
            if signal not in labels:
                continue
            text = (value.get("text") or "").replace("\n", " ").strip()
            presence[rater].add((c_index, idx))
            full_spans[(rater, c_index, idx)].append(text)

    cells = sorted({cell for r in raters for cell in presence[r]},
                   key=lambda cb: (int(cb[0][1:]), cb[1]))
    # a cell is a disagreement whenever it's not the case that every rater fired it
    disagreements = [(c, b) for c, b in cells
                     if not all((c, b) in presence[r] for r in raters)]

    print(f"{'='*90}\n{signal}  ({len(disagreements)} disagreement cell(s) "
          f"across {len(set(c for c, b in disagreements))} conversation(s))\n{'='*90}")
    if entry:
        print(f"\ndecision_steps:")
        for step in entry.get("decision_steps", []):
            print(f"  - {step}")
        if entry.get("boundary_notes"):
            print(f"\nboundary_notes:")
            for k, v in entry["boundary_notes"].items():
                print(f"  {k}: {v}")
    else:
        print("\n(no rubric entry for this signal)")

    by_conv = defaultdict(list)
    for c, b in disagreements:
        by_conv[c].append(b)
    for c in sorted(by_conv, key=lambda x: int(x[1:])):
        print(f"\n--- {c} ({len(by_conv[c])} cell(s)) ---")
        for b in sorted(by_conv[c]):
            role = block_roles[c][b]
            votes = {r: (c, b) in presence[r] for r in raters}
            print(f"  block {b} [{role}]  " +
                  "  ".join(f"{r}={'FIRE' if votes[r] else '-'}" for r in raters))
            for r in raters:
                if votes[r]:
                    for t in full_spans[(r, c, b)]:
                        print(f"    {r}: {t!r}")
            print(f"    block text: {block_texts[c][b][:500]!r}"
                  f"{'...' if len(block_texts[c][b]) > 500 else ''}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--draw-round2", type=int, metavar="SEED",
                    help="draw the round-2 blind set and print its statistics "
                         "(read-only; does not touch the frozen round-1 CSVs)")
    ap.add_argument("--size", type=int, default=10)
    ap.add_argument("--min-blocks", type=int, default=0,
                    help="restrict the pool to conversations of at least this "
                         "many blocks (the 138-pool has a long tail of 2-block "
                         "single exchanges)")
    ap.add_argument("--strategy", choices=["random", "coverage"],
                    default="random",
                    help="random = uniform sample; coverage = seeded greedy "
                         "set cover over the signals A fired")
    ap.add_argument("--no-write", action="store_true",
                    help="print the statistics without writing the set file")
    ap.add_argument("--round2", action="store_true",
                    help="compute round-2 agreement (Jun 'A' vs Michelle 'M', "
                         "projects 1+5) instead of round-1's three-way A/B/F")
    ap.add_argument("--priya", action="store_true",
                    help="compute round-2 agreement (Jun 'A' vs Priya 'P', "
                         "projects 1+4) restricted to whichever conversations "
                         "in agreement_set_round2_priya_done.csv are complete")
    ap.add_argument("--out-suffix", default="",
                    help="appended to round-2 output filenames (e.g. _before/"
                         "_after) for comparing agreement across DB snapshots "
                         "via --db; round-2 only")
    ap.add_argument("--round2-review", metavar="SIGNAL",
                    help="print every round-2 disagreement cell for SIGNAL with "
                         "full untruncated context and the rubric's decision_steps "
                         "+ boundary_notes (read-only; no CSVs written)")
    ap.add_argument("--priya-review", metavar="SIGNAL",
                    help="same as --round2-review but for Jun 'A' vs Priya 'P' "
                         "on whichever conversations she's completed")
    ap.add_argument("--priya-review3", metavar="SIGNAL",
                    help="three-way Jun 'A' / Michelle 'M' / Priya 'P' packet "
                         "(projects 1/5/4) for SIGNAL on the round-2 set -- shows "
                         "Michelle's vote beside each Jun-vs-Priya cell")
    ap.add_argument("--round1-review", metavar="SIGNAL",
                    help="same as --round2-review but for round-1's three-way "
                         "Jun/B/F (projects 1/2/3) on the frozen C1-C10 set")
    args = ap.parse_args()

    if args.round2_review:
        review_packet(args.round2_review, db_path=args.db)
        return

    if args.priya_review3:
        review_packet(args.priya_review3, db_path=args.db, raters=["A", "M", "P"],
                      rater_by_project={1: "A", 5: "M", 4: "P"},
                      rater_user_id={"A": 1, "M": 5, "P": 4},
                      conv_map_path=ROUND2_PRIYA_CONV_MAP)
        return

    if args.round1_review:
        review_packet(args.round1_review, db_path=args.db, raters=RATERS,
                      rater_by_project=RATER_BY_PROJECT,
                      rater_user_id=RATER_USER_ID_R1,
                      conv_map_path=ROUND1_CONV_MAP)
        return

    if args.priya_review:
        review_packet(args.priya_review, db_path=args.db, raters=RATERS_PRIYA,
                      rater_by_project=RATER_BY_PROJECT_PRIYA,
                      rater_user_id=RATER_USER_ID_PRIYA,
                      conv_map_path=ROUND2_PRIYA_CONV_MAP)
        return

    if args.draw_round2 is not None:
        draw_round2(args.db, args.draw_round2, size=args.size,
                    min_blocks=args.min_blocks, strategy=args.strategy,
                    write=not args.no_write)
        return

    if args.round2:
        compute_agreement(args.db, RATERS_R2, RATER_BY_PROJECT_R2,
                          RATER_USER_ID_R2, ROUND2_CONV_MAP, ROUND2_DIR,
                          f"agreement_round2{args.out_suffix}")
        return

    if args.priya:
        compute_agreement(args.db, RATERS_PRIYA, RATER_BY_PROJECT_PRIYA,
                          RATER_USER_ID_PRIYA, ROUND2_PRIYA_CONV_MAP,
                          ROUND2_DIR, f"agreement_priya_partial{args.out_suffix}")
        return

    compute_agreement(args.db, RATERS, RATER_BY_PROJECT, RATER_USER_ID_R1,
                      None, OUT_DIR, "agreement_round1")


if __name__ == "__main__":
    main()
