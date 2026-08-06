#!/usr/bin/env python3
"""Meeting-1 triage of the post-discussion disagreement cells.

Classifies every cell of agreement_post_discussion_disagreements.csv
(the 693 three-way no-consensus cells remaining after the B-F
reconciliation, in which F adopted 304 of B's blind labels) along the
axes the first rubric-revision meeting needs:

  axis          A_vs_consensus (B = F != A)  |  BF_residual (B != F)
  direction     A_only / A_miss   |   B_only / F_only
  triage_class  1_placement  positive label on a block role the
                             checklist forbids (role_allowed = 0)
                2_boundary   a zero-voting rater fired the same signal
                             within +/-2 blocks in the conversation
                3_granularity a zero-voting rater fired the same signal
                             elsewhere in the same conversation
                4_concept    the zero-voting side never fires the signal
                             anywhere in the conversation
  cleared_by    which 2026-08-03 decision resolves the cell, if any:
                d1-reasoning-visibility  (placement on reasoning/analysis)
                d2-drop-conversation_advanced
                (d3 - user_ambiguous_request - objectifies steps but keeps
                 the signal, so its cells stay open as calibration cases)

Output: meeting1_cells.csv (deterministic; byte-identical on re-run).

Also prints two investigation tables that feed the D4/D5 candidate
rubric changes (v06_changelog_draft.md):

  I1 channel-visibility sweep — human-block 5-grams that match a PRIOR
     reasoning/code block but no prior ai/human block: mechanical
     evidence that users read the internal channels (the C4 case).
  I2 granularity numbers — per-conversation count agreement between
     raters and within-block same-signal multiplicity for the
     high-repeat signals: the empirical basis for the block-level
     one-label-multi-span unit.

Usage:
    python annotation/Rubric_agree/roud_1/BF/triage_meeting1.py [--db PATH]
        [--full-sweep]   # also run I1 over all project-1 conversations
"""

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent            # .../roud_1/BF/
ROUND_DIR = OUT_DIR.parent                           # .../roud_1/
sys.path.insert(0, str(ROUND_DIR))
import agreement_round1 as ar

IN_CSV = ROUND_DIR / "agreement_post_discussion_disagreements.csv"
OUT_CSV = OUT_DIR / "meeting1_cells.csv"

BOUNDARY_WINDOW = 2


def zero_side(row):
    """The rater(s) voting 0 whose reading defines the triage class."""
    if row["axis"] == "A_vs_consensus":
        return ["B", "F"] if row["direction"] == "A_only" else ["A"]
    return ["F"] if row["direction"] == "B_only" else ["B"]


def classify(row, blocks_of):
    c, b, s = row["c_index"], int(row["block_idx"]), row["signal"]
    if row["role_allowed"] == "0":
        return "1_placement"
    zblocks = set()
    for rater in zero_side(row):
        zblocks |= blocks_of[rater][(c, s)]
    if any(abs(b - b2) <= BOUNDARY_WINDOW for b2 in zblocks):
        return "2_boundary"
    if zblocks:
        return "3_granularity"
    return "4_concept"


def cleared_by(row):
    if row["signal"] == "conversation_advanced":
        return "d2-drop-conversation_advanced"
    if (row["role_allowed"] == "0"
            and row["block_role"] in ("reasoning", "analysis")):
        return "d1-reasoning-visibility"
    return ""


NGRAM = 5
INTERNAL_ROLES = ("reasoning", "code", "analysis")
REPEAT_SIGNALS = [
    "ai_asked_probing_question", "ai_asks_followup", "ai_validates_user",
    "ai_references_prior_turn", "ai_hedges_uncertainty",
    "ai_provides_step_by_step",
]


def norm_words(text):
    import re
    return re.findall(r"[a-z0-9']+", text.lower())


def ngram_set(words):
    return {tuple(words[i:i + NGRAM]) for i in range(len(words) - NGRAM + 1)}


def load_block_texts(db_path, conv_to_c):
    """c_index -> [(role, text)] from project 2 (dialogues identical
    across projects, verified by agreement_round1)."""
    import json
    import sqlite3
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    rows = con.execute("SELECT data FROM task WHERE project_id = 2").fetchall()
    con.close()
    texts = {}
    for (data,) in rows:
        payload = json.loads(data)
        c = conv_to_c.get(payload["conv_id"])
        if c is not None:
            texts[c] = [(b.get("author", "?"), b.get("text", ""))
                        for b in payload["dialogue"]]
    return texts


def iter_echoes(blocks):
    """Yield (human_idx, src_idx, src_role, n_hits, run_words, phrase) for
    every human block whose NGRAM-grams match a PRIOR internal block
    (reasoning/code/analysis) but no prior ai or human block."""
    seen_visible = set()          # ngrams of prior ai + human blocks
    internal = []                 # (idx, role, ngram set)
    for i, (role, text) in enumerate(blocks):
        words = norm_words(text)
        if role == "human":
            grams = [tuple(words[k:k + NGRAM])
                     for k in range(len(words) - NGRAM + 1)]
            for j, srole, sgrams in internal:
                marked = [g in sgrams and g not in seen_visible
                          for g in grams]
                if not any(marked):
                    continue
                runs, start = [], None
                for k, m in enumerate(marked + [False]):
                    if m and start is None:
                        start = k
                    elif not m and start is not None:
                        runs.append((start, k - 1 + NGRAM))
                        start = None
                longest = max(runs, key=lambda r: r[1] - r[0])
                phrase = " ".join(words[longest[0]:longest[1]][:14])
                yield (i, j, srole, sum(marked),
                       longest[1] - longest[0], phrase)
        if role in INTERNAL_ROLES:
            internal.append((i, role, ngram_set(words)))
        else:
            seen_visible |= ngram_set(words)


def channel_visibility_sweep(texts, conv_order):
    """I1: for each human block, 5-grams matching a PRIOR internal block
    (reasoning/code/analysis) but absent from every prior ai and human
    block — evidence the user read the internal channel."""
    print("\n=== I1 channel-visibility sweep "
          f"({NGRAM}-gram echoes of internal channels in user turns) ===")
    print(f"{'conv':5s} {'human':>6s} {'source':>8s} {'role':10s} "
          f"{'grams':>5s}  longest matched phrase")
    total = 0
    for c in conv_order:
        for i, j, srole, n_hits, _run, phrase in iter_echoes(texts[c]):
            total += n_hits
            print(f"{c:5s} b{i:<5d} b{j:<7d} {srole:10s} "
                  f"{n_hits:5d}  “{phrase}…”")
    print(f"Total unexplained internal-channel echoes: {total}")


STRONG_RUN = 8   # matched run of >= 8 words (>= 4 overlapping 5-grams)


def corpus_visibility_sweep(db_path, conv_to_c):
    """Corpus-wide I1 over all project-1 conversations (the full dataset):
    per-channel echo summary with strong/weak tiering, plus detail rows
    for every reasoning/analysis echo and every strong echo. Answers
    whether the C4 (task 740) reasoning echo is unique and whether
    analysis blocks show echo evidence at all."""
    import json
    import sqlite3
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    rows = con.execute("SELECT id, data FROM task WHERE project_id = 1 "
                       "ORDER BY id").fetchall()
    con.close()
    contain, echoed, strong_convs, gram_tot = (
        Counter(), Counter(), Counter(), Counter())
    details = []
    for tid, data in rows:
        payload = json.loads(data)
        blocks = [(b.get("author", "?"), b.get("text", ""))
                  for b in payload["dialogue"]]
        roles = {r for r, _ in blocks}
        for ch in INTERNAL_ROLES:
            if ch in roles:
                contain[ch] += 1
        c_label = conv_to_c.get(payload.get("conv_id"), "")
        hit_ch, strong_ch = set(), set()
        for i, j, srole, n_hits, run, phrase in iter_echoes(blocks):
            gram_tot[srole] += n_hits
            hit_ch.add(srole)
            strong = run >= STRONG_RUN
            if strong:
                strong_ch.add(srole)
            if strong or srole in ("reasoning", "analysis"):
                details.append((tid, c_label, i, j, srole, n_hits, run,
                                phrase, "strong" if strong else "weak"))
        for ch in hit_ch:
            echoed[ch] += 1
        for ch in strong_ch:
            strong_convs[ch] += 1
    print("\n=== I1-full corpus channel-visibility sweep "
          f"(project 1, {len(rows)} conversations) ===")
    print(f"{'channel':10s} {'convs w/ channel':>16s} {'convs echoed':>13s} "
          f"{'strong convs':>13s} {'echo grams':>11s}")
    for ch in INTERNAL_ROLES:
        print(f"{ch:10s} {contain[ch]:16d} {echoed[ch]:13d} "
              f"{strong_convs[ch]:13d} {gram_tot[ch]:11d}")
    print(f"strong = matched run >= {STRONG_RUN} words "
          f"(>= {STRONG_RUN - NGRAM + 1} overlapping {NGRAM}-grams)")
    print("\nDetail (all reasoning/analysis echoes + all strong echoes):")
    print(f"{'task':>5s} {'conv':>5s} {'human':>6s} {'source':>7s} "
          f"{'role':10s} {'grams':>5s} {'run':>4s} {'tier':6s}  "
          "longest matched phrase")
    for tid, c_label, i, j, srole, n_hits, run, phrase, tier in details:
        print(f"{tid:5d} {c_label or '-':>5s} b{i:<5d} b{j:<6d} {srole:10s} "
              f"{n_hits:5d} {run:4d} {tier:6s}  “{phrase}…”")


SCREEN_CUES = [
    ("question", r"\?"),
    ("hedge", r"\b(might|may|perhaps|possibly|likely|probably|unsure"
              r"|uncertain|not sure)\b"),
    ("self_limit", r"\b(i don't know|i cannot|i can't|don't have access"
                   r"|unable to)\b"),
    ("validation", r"\b(you're right|good point|great question"
                   r"|exactly right|excellent)\b"),
    ("correction", r"\b(wait,|actually,|mistake|i apologize|let me fix"
                   r"|i was wrong)\b"),
]


def internal_block_screen(texts, presence, conv_order):
    """I3: after removing the channel ban, which internal blocks that NO
    rater labeled carry surface cues of labelable signals? Candidate-add
    screen for the meeting — cue presence is NOT a label; each flagged
    block still needs a manual rubric walk."""
    import re
    labeled = {(c, b) for r in ar.RATERS for (c, b, _s) in presence[r]}
    print("\n=== I3 internal-block screen "
          "(unlabeled internal blocks with signal cues) ===")
    print(f"{'conv':5s} {'block':>6s} {'role':10s} {'words':>6s}  cues")
    n_blocks = n_flagged = 0
    by_role = Counter()
    for c in conv_order:
        for i, (role, text) in enumerate(texts[c]):
            if role not in INTERNAL_ROLES or (c, i) in labeled:
                continue
            n_blocks += 1
            low = text.lower()
            cues = [name for name, pat in SCREEN_CUES
                    if re.search(pat, low)]
            if not cues:
                continue
            n_flagged += 1
            by_role[role] += 1
            print(f"{c:5s} b{i:<5d} {role:10s} {len(norm_words(text)):6d}  "
                  f"{', '.join(cues)}")
    print(f"{n_flagged} of {n_blocks} unlabeled internal blocks carry >=1 "
          f"cue (by role: {dict(sorted(by_role.items()))}); cue presence "
          "is a screen, not a label — each needs a manual rubric walk.")


def granularity_numbers(presence, spans, conv_order):
    """I2: count agreement and within-block multiplicity for the
    high-repeat signals."""
    from scipy.stats import spearmanr
    print("\n=== I2 granularity numbers (high-repeat signals) ===")
    print(f"{'signal':28s} {'countSp AB':>10s} {'AF':>6s} {'BF':>6s} "
          f"{'multi>1 A/B/F':>14s} {'posBlocks A/B/F':>16s}")
    for s in REPEAT_SIGNALS:
        counts = {r: [sum(1 for (c, b, sig) in presence[r]
                          if c == cv and sig == s) for cv in conv_order]
                  for r in ar.RATERS}
        rho = {}
        for r1, r2 in ar.PAIRS:
            if len(set(counts[r1])) < 2 or len(set(counts[r2])) < 2:
                rho[r1 + r2] = "n/a"
            else:
                rho[r1 + r2] = f"{spearmanr(counts[r1], counts[r2])[0]:.2f}"
        multi, pos = {}, {}
        for r in ar.RATERS:
            cells = [(c, b) for (c, b, sig) in presence[r] if sig == s]
            pos[r] = len(cells)
            multi[r] = sum(1 for cb in cells
                           if len(spans.get((r, cb[0], cb[1], s), [])) > 1)
        print(f"{s:28s} {rho['AB']:>10s} {rho['AF']:>6s} {rho['BF']:>6s} "
              f"{multi['A']:>4d}/{multi['B']}/{multi['F']} "
              f"{pos['A']:>8d}/{pos['B']}/{pos['F']}")
    print("countSp = Spearman rho between raters' per-conversation counts "
          "(10 conversations); multi>1 = positive (block, signal) cells "
          "carrying more than one evidence span from that rater.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=ar.DEFAULT_DB)
    ap.add_argument("--full-sweep", action="store_true",
                    help="also run the I1 sweep over all project-1 "
                         "conversations (the full dataset)")
    ap.add_argument("--internal-screen", action="store_true",
                    help="also screen unlabeled internal blocks in the "
                         "10 agreement conversations for signal cues")
    args = ap.parse_args()

    conv_to_c, conv_order = ar.load_conv_map()
    _, presence, spans, _ = ar.load_annotations(args.db, conv_to_c)
    blocks_of = {r: defaultdict(set) for r in ar.RATERS}
    for r in ar.RATERS:
        for c, b, s in presence[r]:
            blocks_of[r][(c, s)].add(b)

    rows = list(csv.DictReader(open(IN_CSV)))
    for row in rows:
        if row["B"] == row["F"]:
            row["axis"] = "A_vs_consensus"
            row["direction"] = "A_only" if row["A"] == "1" else "A_miss"
        else:
            row["axis"] = "BF_residual"
            row["direction"] = "B_only" if row["B"] == "1" else "F_only"
        row["triage_class"] = classify(row, blocks_of)
        row["cleared_by"] = cleared_by(row)

    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    ax = Counter(r["axis"] for r in rows)
    assert ax["A_vs_consensus"] == 475 and ax["BF_residual"] == 218, ax
    open_rows = [r for r in rows if not r["cleared_by"]]
    oax = Counter(r["axis"] for r in open_rows)
    assert oax["A_vs_consensus"] == 361, oax  # 475 - 114 (d2)
    assert oax["BF_residual"] == 200, oax     # 218 - 18 (d2)

    print(f"{len(rows)} cells -> {OUT_CSV.name}")
    print(f"axis: {dict(ax)}")
    print(f"cleared: {dict(Counter(r['cleared_by'] for r in rows if r['cleared_by']))}")
    print(f"open: {dict(oax)}  (uar calibration cells stay open: "
          f"{sum(1 for r in open_rows if r['signal'] == 'user_ambiguous_request')})")
    for axis in ["A_vs_consensus", "BF_residual"]:
        sub = [r for r in open_rows if r["axis"] == axis]
        print(f"{axis} open by class: "
              f"{dict(sorted(Counter(r['triage_class'] for r in sub).items()))}")

    texts = load_block_texts(args.db, conv_to_c)
    channel_visibility_sweep(texts, conv_order)
    granularity_numbers(presence, spans, conv_order)
    if args.full_sweep:
        corpus_visibility_sweep(args.db, conv_to_c)
    if args.internal_screen:
        internal_block_screen(texts, presence, conv_order)


if __name__ == "__main__":
    main()
