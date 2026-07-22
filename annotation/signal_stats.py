#!/usr/bin/env python3
"""Per-(signal x block) statistics from the Label Studio SQLite database.

The taxonomy unit is the (signal, block) cell, never the signal name alone
(same signal in different blocks = different cells). Reads submitted
annotations from task_completion, resolves each labeled span's block type
via the task's dialogue authors, and compares observed cells against the
cells defined in signal_checklist.csv.

Usage:
    python annotation/signal_stats.py [--db PATH] [--csv PATH] [--rare N]
"""

import argparse
import csv
import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_DB = "/data/wang/junh/label-studio-data/label_studio.sqlite3"
DEFAULT_CSV = Path(__file__).parent / "signal_checklist.csv"
DEFAULT_CONFIG = Path(__file__).parent / "label_studio_config.xml"
BLOCK_ORDER = ["human", "reasoning", "analysis", "code", "ai"]


def load_config_signals(xml_path):
    """The final signal set = labels present in the Label Studio config.
    Signals excluded by the kappa pre-screening (kappa < 0.4) are not in the
    config and must not appear in any statistic."""
    text = Path(xml_path).read_text()
    return set(re.findall(r'<Label value="([^"]+)"', text))


def load_defined_cells(csv_path, config_signals):
    """(block, signal) cells defined in the checklist, restricted to the
    final signal set. CSV rows for excluded signals are dropped (the CSV
    does not mark exclusion status itself)."""
    cells, dropped = {}, set()
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            if row["signal"] not in config_signals:
                dropped.add(row["signal"])
                continue
            cells[(row["block"], row["signal"])] = {
                "layer": row.get("layer", ""),
                "tier": row.get("tier", ""),
            }
    return cells, dropped


def load_annotations(db_path):
    """Yield (task_id, dialogue, result_items) for each submitted annotation."""
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    rows = con.execute(
        """SELECT tc.task_id, t.data, tc.result
           FROM task_completion tc JOIN task t ON t.id = tc.task_id
           WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL"""
    ).fetchall()
    con.close()
    for task_id, data, result in rows:
        dialogue = json.loads(data).get("dialogue", [])
        yield task_id, dialogue, json.loads(result)


def collect_counts(db_path):
    """Count signal placements per (block, signal) cell.

    Each labeled span counts once per signal it carries; the block type is
    the author of the span's start turn.
    """
    cell_counts = Counter()
    cell_tasks = defaultdict(set)
    blocks_present = Counter()
    unresolved = []
    n_annotations = 0

    for task_id, dialogue, result in load_annotations(db_path):
        n_annotations += 1
        for turn in dialogue:
            blocks_present[turn.get("author", "?")] += 1
        for item in result:
            if item.get("type") != "paragraphlabels":
                continue
            value = item.get("value", {})
            try:
                idx = int(value.get("start"))
                block = dialogue[idx].get("author", "?")
            except (TypeError, ValueError, IndexError):
                unresolved.append((task_id, value.get("start")))
                continue
            for signal in value.get("paragraphlabels", []):
                cell_counts[(block, signal)] += 1
                cell_tasks[(block, signal)].add(task_id)

    return {
        "n_annotations": n_annotations,
        "cell_counts": cell_counts,
        "cell_tasks": cell_tasks,
        "blocks_present": blocks_present,
        "unresolved": unresolved,
    }


def block_sort_key(block):
    return BLOCK_ORDER.index(block) if block in BLOCK_ORDER else len(BLOCK_ORDER)


def report(stats, defined_cells, dropped_signals, config_signals,
           rare_threshold):
    counts = stats["cell_counts"]
    tasks = stats["cell_tasks"]
    lines = []
    w = lines.append

    w(f"Submitted annotations: {stats['n_annotations']}")
    w(f"Final signal set (label_studio_config.xml): {len(config_signals)} signals")
    w(f"Total signal placements: {sum(counts.values())}")
    not_in_config = {s for (_, s) in counts if s not in config_signals}
    if not_in_config:
        w(f"WARNING: fired signals NOT in the final set: {sorted(not_in_config)}")
    if dropped_signals:
        w(f"CSV rows dropped (excluded signals, not in config): "
          f"{sorted(dropped_signals)}")
    if stats["unresolved"]:
        w(f"WARNING: {len(stats['unresolved'])} spans had unresolvable block "
          f"indices: {stats['unresolved'][:10]}")
    w("")

    w("== Block coverage (blocks present across annotated tasks vs. placements) ==")
    placements_per_block = Counter()
    for (block, _), n in counts.items():
        placements_per_block[block] += n
    for block in sorted(set(stats["blocks_present"]) | set(placements_per_block),
                        key=block_sort_key):
        w(f"  {block:<10} blocks={stats['blocks_present'].get(block, 0):<6}"
          f" placements={placements_per_block.get(block, 0)}")
    w("")

    w("== Per-(signal x block) cell counts ==")
    w(f"  {'block':<10} {'signal':<34} {'fires':>5} {'tasks':>5}  defined")
    for (block, signal), n in sorted(
            counts.items(), key=lambda kv: (block_sort_key(kv[0][0]), -kv[1])):
        defined = "yes" if (block, signal) in defined_cells else "NO <- outside checklist"
        w(f"  {block:<10} {signal:<34} {n:>5} {len(tasks[(block, signal)]):>5}  {defined}")
    w("")

    zero = [c for c in defined_cells if c not in counts]
    w(f"== Zero-fire defined cells ({len(zero)} of {len(defined_cells)}) ==")
    for block, signal in sorted(zero, key=lambda c: (block_sort_key(c[0]), c[1])):
        meta = defined_cells[(block, signal)]
        w(f"  {block:<10} {signal:<34} layer={meta['layer']} tier={meta['tier']}")
    w("")

    rare = [(c, n) for c, n in counts.items() if n < rare_threshold]
    w(f"== Rare cells (< {rare_threshold} fires, {len(rare)} cells) ==")
    for (block, signal), n in sorted(rare, key=lambda kv: (kv[1], kv[0])):
        w(f"  {block:<10} {signal:<34} {n}")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--rare", type=int, default=5)
    args = ap.parse_args()

    config_signals = load_config_signals(args.config)
    defined_cells, dropped = load_defined_cells(args.csv, config_signals)
    stats = collect_counts(args.db)
    print(report(stats, defined_cells, dropped, config_signals, args.rare))


if __name__ == "__main__":
    main()
