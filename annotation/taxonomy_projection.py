"""
Midpoint / endpoint dry-run: project current annotations onto the taxonomy.

Answers "what do we get if we stopped now?" for the bottom-up chain
observation -> signal -> taxonomy:

  1. Mapping audit    — every live signal (label_studio_config.xml) must have a
                        row in docs/criteria/control_mapping.csv; orphans break
                        the chain.
  2. Role accounting  — placements split by taxonomy role (coupling core /
                        trigger / support / outcome / context).
  3. 16-cell table    — coupling placements per (control_op x direction),
                        split by polarity; EMPTY cells listed with the reason
                        (no live signal mapped vs. mapped-but-unfired).
  4. Saturation       — cumulative distinct signals fired by task order.
  5. Split-half drift — first-half vs second-half per-signal task frequencies
                        (Spearman rho) + largest per-signal shifts.

Usage:
    python annotation/taxonomy_projection.py
Reads the live Label Studio DB read-only.
"""

import csv
import json
import math
import re
import sqlite3
from collections import Counter, defaultdict

DB = "/data/wang/junh/label-studio-data/label_studio.sqlite3"
MAPPING = "docs/criteria/control_mapping.csv"
CONFIG = "annotation/label_studio_config.xml"
OPS = ["ask_clarify", "report_state", "seek_inspect", "confirm_authorize",
       "act_execute", "maintain_state", "recover_repair", "stop_defer"]


def role_of(row):
    rt = row["relation_type"]
    if rt.startswith("coupling") or rt.startswith("direct_coupling"):
        return "coupling"
    if rt.startswith("trigger"):
        return "trigger"
    if rt.startswith("support") or rt.startswith("rapport"):
        return "support"
    if rt.startswith("outcome"):
        return "outcome"
    return "context"


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


live = set(re.findall(r'value="([a-z_]+)"', open(CONFIG).read())) - {"dialogue"}
mapping = {r["signal"]: r for r in csv.DictReader(open(MAPPING))}

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
sig_counts, sig_tasks = Counter(), defaultdict(set)
per_task = defaultdict(set)
for tid, res in con.execute(
        "SELECT task_id, result FROM task_completion WHERE was_cancelled=0"):
    for item in json.loads(res):
        for lab in item["value"].get("paragraphlabels", []):
            sig_counts[lab] += 1
            sig_tasks[lab].add(tid)
            per_task[tid].add(lab)

total = sum(sig_counts.values())
tids = sorted(per_task)
print(f"Submitted tasks: {len(tids)}   placements: {total}")

# 1. mapping audit
orphans = sorted((live - set(mapping)) - {"CANDIDATE_SIGNAL"})
stale = sorted(set(mapping) - live)
print(f"\n== Mapping audit ==")
print(f"live signals: {len(live)}   orphans (live, unmapped): {len(orphans)}")
for s in orphans:
    print(f"  ORPHAN {s} (fires={sig_counts.get(s, 0)})")
print(f"stale mapping rows (non-live signals, e.g. kappa-excluded): {len(stale)}")

# 2. role accounting
roles = Counter()
for s, n in sig_counts.items():
    roles[role_of(mapping[s]) if s in mapping else "UNMAPPED"] += n
print("\n== Placements by taxonomy role ==")
for k, v in roles.most_common():
    print(f"  {k:<10} {v:>4}  ({v / total * 100:.0f}%)")

# 3. 16-cell coupling core
cell, cell_tasks, noop = defaultdict(Counter), defaultdict(set), []
for s, n in sig_counts.items():
    row = mapping.get(s)
    if row and role_of(row) == "coupling":
        if row["control_op"]:
            cell[(row["control_op"], row["l1"])][row["polarity"]] += n
            cell_tasks[(row["control_op"], row["l1"])] |= sig_tasks[s]
        else:
            noop.append((s, n, row["relation_type"]))

live_cells = defaultdict(list)   # cells a live signal COULD fill
for s in live:
    row = mapping.get(s)
    if row and role_of(row) == "coupling" and row["control_op"]:
        live_cells[(row["control_op"], row["l1"])].append(s)

print("\n== 16-cell coupling core (op x direction) ==")
print(f"{'operation':<18} {'dir':<5} {'fail':>5} {'pos':>5} {'human':>6} {'esc':>4} {'tasks':>6}")
for op in OPS:
    for l1 in ("H2AI", "AI2H"):
        c = cell.get((op, l1))
        if c:
            print(f"{op:<18} {l1:<5} {c.get('failure', 0):>5} {c.get('positive', 0):>5} "
                  f"{c.get('human', 0):>6} {c.get('escalation', 0):>4} {len(cell_tasks[(op, l1)]):>6}")
        else:
            why = ("no live signal mapped" if not live_cells.get((op, l1))
                   else f"mapped-but-unfired: {','.join(live_cells[(op, l1)])}")
            print(f"{op:<18} {l1:<5} {'EMPTY':^30} <- {why}")
print("coupling signals with no op (direct coupling):",
      ", ".join(f"{s}({n})" for s, n, _ in noop) or "none")

# 4. saturation
seen, curve = set(), []
for t in tids:
    seen |= per_task[t]
    curve.append(len(seen))
marks = sorted(set(list(range(9, len(tids), 10)) + [len(tids) - 1]))
print("\n== Saturation (cumulative distinct signals fired) ==")
print("  " + "  ".join(f"task{tids[i]}:{curve[i]}" for i in marks))

# 5. split-half drift
half = len(tids) // 2
c1, c2 = Counter(), Counter()
for t in tids[:half]:
    for s in per_task[t]:
        c1[s] += 1
for t in tids[half:]:
    for s in per_task[t]:
        c2[s] += 1
sigs = sorted(set(c1) | set(c2))
rho = spearman([c1.get(s, 0) for s in sigs], [c2.get(s, 0) for s in sigs])
print(f"\n== Split-half drift (tasks {tids[0]}-{tids[half - 1]} vs {tids[half]}-{tids[-1]}) ==")
print(f"  Spearman rho over {len(sigs)} signals: {rho:.3f}")
print(f"  {'largest shifts':<32} {'half1':>6} {'half2':>6}")
for s in sorted(sigs, key=lambda s: -abs(c1.get(s, 0) - c2.get(s, 0)))[:12]:
    print(f"  {s:<32} {c1.get(s, 0):>6} {c2.get(s, 0):>6}")
