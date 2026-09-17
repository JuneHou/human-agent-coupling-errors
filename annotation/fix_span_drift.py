"""Annotation-result repairs written back to the Label Studio DB.

Mode 1 (default) -- repair mouse-selection drift between a region's stored
`text` and its offsets. Two drift classes, resolved by which side is well
formed:
  (a) stored text is intact but the offsets slid by a character or two ->
      snap the offsets to where the stored text actually sits (search a small
      window around the recorded start).
  (b) stored text is itself truncated ("at's...", "hanks...") -> the offsets are
      authoritative; rewrite text from the slice and trim stray edge whitespace.

Mode 2 (--apply-v06-edits) -- apply the AGREED round-1 label changes to the
three agreement projects. Source of truth: the per-annotator change files
Rubric_agree/roud_1/BF/changes_{A,B,F}.md (A -> project 1, B -> 2, F -> 3),
whose rows are the edits all three annotators agreed to after the async review.
Rows that are struck through, marked "keep", or empty are no-ops, and the
unresolved cells (C4 b26, C8 b64, C9 b11, C9 b38) plus the open C1 b2 appear in
no row -- so they are left untouched by construction. Also strips
conversation_advanced everywhere in projects 1-3 (rubric v0.6 rule A7).

Both modes are dry-run unless --apply is passed.

Mode 3 (--list-wide-spans) -- list the labels mode 2 added whose span still
covers the whole block (the change file quoted no locatable evidence). Presence
and kappa are correct; only the highlight needs narrowing, by the annotator who
owns the label. With --write, the report replaces the "Span fix-ups" section at
the end of each changes_X.md so each annotator keeps ONE to-do document.

Mode 4 (--fix-michelle-round2) -- remove specific mislabeled result items from
Michelle's round-2 annotations (Label Studio project 5), approved by Jun on
2026-09-14 after a manual review of her 10 completed tasks:
  (a) task 773, completion 176: ai_structured_response fired on `code`-authored
      blocks; the rubric (sharechat_rubric.json signals.ai_structured_response
      .blocks) restricts this signal to the `ai` block only.
  (b) task 770, completion 178: ai_validates_user fired on bare compliance
      openers ("Yeah,", "Right.", "Correct.", "True.", "Makes sense.", "No.
      Right,") that fail the rubric's Step 1 (SPECIFICITY TEST) / Step 3
      (COMPLIANCE-OPENER EXCLUSION). The 11 other ai_validates_user fires in
      the same task, and all fires in tasks 767/771/776, were reviewed and
      kept -- this mode targets only the exact ids in MICHELLE_ROUND2_REMOVALS,
      never a signal- or block-based rule, since a programmatic rule cannot
      safely distinguish a bare opener from a specific one; that judgment was
      Jun's manual review.

Mode 5 (--restore-michelle-avu) -- correction to Mode 4(b): round-2 agreement
computation (Jun vs Michelle) showed that 11 of the 13 removed ai_validates_user
spans are blocks where Jun's OWN project-1 annotation of the identical
conversation (task 83 = R4) independently fires the same signal -- so removing
them from Michelle turned an agreement into a disagreement rather than fixing
one. Restores those 11 (not the other 2, blocks 37/149, where Jun also has no
fire), using Jun's own span -- read live from his completion, not
hand-transcribed -- since at several blocks his span is not merely wider than
Michelle's original but a different sentence in the same block (e.g. block 55)
or starts after the bare opener (e.g. block 123).

Mode 6 (--fix-round2-rule-violations) -- remove round-2 fires that violate rules round 1
already settled and wrote into sharechat_rubric.json before round 2 started: task 773's
false_confidence on two purely-code/markup spans of block 10 (a third, genuine-claim span
on the same block stays), and task 771's ai_provides_example fired on general claims,
descriptions, or the AI's self-report rather than a concrete illustrative instance (blocks
2 and 26 each keep one sibling span that does name a concrete case). Found via round-2
agreement analysis comparing Michelle's labels against Jun's independent read.

All modes are dry-run unless --apply is passed.

Usage:
    python annotation/fix_span_drift.py [--apply]
    python annotation/fix_span_drift.py --apply-v06-edits [--apply] [--db PATH]
    python annotation/fix_span_drift.py --list-wide-spans [--write]
    python annotation/fix_span_drift.py --fix-michelle-round2 [--apply] [--db PATH]
    python annotation/fix_span_drift.py --restore-michelle-avu [--apply] [--db PATH]
    python annotation/fix_span_drift.py --fix-round2-rule-violations [--apply] [--db PATH]
"""
import csv, hashlib, json, re, sqlite3, sys
from collections import defaultdict
from pathlib import Path

SIGNAL = "ai_validates_user"
WINDOW = 10
DEFAULT_DB = "/data/wang/junh/label-studio-data/label_studio.sqlite3"
ANNOT_DIR = Path(__file__).resolve().parent
BF_DIR = ANNOT_DIR / "Rubric_agree" / "roud_1" / "BF"
RATER_PROJECT = {"A": 1, "B": 2, "F": 3}
DROPPED_SIGNAL = "conversation_advanced"          # rubric v0.6 rule A7


def db_path():
    if "--db" in sys.argv:
        return sys.argv[sys.argv.index("--db") + 1]
    return DEFAULT_DB


def fix_span_drift(apply_changes):
    con = sqlite3.connect(db_path())
    rows = con.execute("""SELECT tc.id, tc.task_id, t.data, tc.result FROM task_completion tc
                      JOIN task t ON t.id = tc.task_id WHERE tc.was_cancelled = 0""").fetchall()
    fixed = unresolved = 0

    for ann_id, tid, data, res_raw in rows:
        dlg = json.loads(data)["dialogue"]
        res = json.loads(res_raw)
        changed = False
        for it in res:
            v = it.get("value", {})
            if SIGNAL not in v.get("paragraphlabels", []):
                continue
            blk = int(v["start"])
            text = dlg[blk]["text"].replace("\n", " ")
            o1, o2, stored = v["startOffset"], v["endOffset"], v["text"]
            if text[o1:o2] == stored:
                # Consistent but still drifted: the selection clipped a word at an
                # edge and `text` recorded the clipped form, so no mismatch shows up
                # ("es, exactly" for "Yes, exactly"). Same root cause, invisible to
                # the mismatch check -- repair by growing to word boundaries.
                new1, new2 = o1, o2
                while new1 > 0 and text[new1 - 1].isalnum() and text[new1].isalnum():
                    new1 -= 1
                while new2 < len(text) and text[new2].isalnum() and text[new2 - 1].isalnum():
                    new2 += 1
                if (new1, new2) == (o1, o2):
                    continue
                print(f"task {tid:>3} b{blk:<4} {it['id']:<11} restore clipped word")
                print(f"    {o1}:{o2} -> {new1}:{new2}")
                print(f"    text: {stored[:60]!r}")
                print(f"       -> {text[new1:new2][:60]!r}")
                v["startOffset"], v["endOffset"], v["text"] = new1, new2, text[new1:new2]
                changed = True
                fixed += 1
                continue

            lo = max(0, o1 - WINDOW)
            found = text.find(stored, lo, o1 + WINDOW + len(stored))
            if found >= 0:                                    # class (a)
                new1, new2, how = found, found + len(stored), "snap offsets"
                # The stored text can itself be a mid-word truncation ("at's...",
                # "hanks..."). Snapping alone would keep a span that starts or ends
                # inside a word, so grow to the enclosing word boundaries.
                while new1 > 0 and text[new1 - 1].isalnum() and text[new1].isalnum():
                    new1 -= 1
                    how = "snap offsets + restore word"
                while new2 < len(text) and text[new2].isalnum() and text[new2 - 1].isalnum():
                    new2 += 1
                    how = "snap offsets + restore word"
                new_text = text[new1:new2]
            else:                                             # class (b)
                slice_ = text[o1:o2]
                lead = len(slice_) - len(slice_.lstrip())
                trail = len(slice_) - len(slice_.rstrip())
                new1, new2 = o1 + lead, o2 - trail
                new_text, how = text[new1:new2], "rewrite text from offsets"
                if not new_text:
                    unresolved += 1
                    print(f"  UNRESOLVED task {tid} b{blk} {it['id']}")
                    continue

            print(f"task {tid:>3} b{blk:<4} {it['id']:<11} {how}")
            print(f"    {o1}:{o2} -> {new1}:{new2}")
            print(f"    text: {stored[:60]!r}")
            print(f"       -> {new_text[:60]!r}")
            assert text[new1:new2] == new_text
            v["startOffset"], v["endOffset"], v["text"] = new1, new2, new_text
            changed = True
            fixed += 1

        if changed and apply_changes:
            con.execute("""UPDATE task_completion SET result=?, updated_at=datetime('now')
                           WHERE id=?""", (json.dumps(res, ensure_ascii=False), ann_id))

    if apply_changes:
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: {fixed} region(s) repaired, "
          f"{unresolved} unresolved")


# ----------------------------------------------------------------------------
# Mode 2: apply the agreed round-1 label edits (--apply-v06-edits)
# ----------------------------------------------------------------------------

# One table row of a changes_X.md file. The edit cell holds operations of the
# form "+ `signal`" / "- `signal`", optionally with a "xN" multiplier (which
# only restates how many of the row's blocks it covers) and optionally with an
# explicit "(bNN)" that redirects that one operation to a different block.
OP_RE = re.compile(
    r"(?P<op>[+−])\s*`(?P<sig>[a-z_]+)`"
    r"(?:\s*×\d+)?"
    r"(?:\s*\((?P<blk>b\d+)\))?"
)
STRUCK_RE = re.compile(r"~~.*?~~")


def parse_change_file(path):
    """-> list of (c_index, block_idx, signal, op) for the AGREED rows only."""
    edits, conv = [], None
    for line in path.read_text().splitlines():
        head = re.match(r"##\s+(C\d+)\s*$", line.strip())
        if head:
            conv = head.group(1)
            continue
        if not line.startswith("|") or conv is None:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or set(cells[0]) <= set("- :"):
            continue                                   # header separator row
        block_cell, edit_cell = cells[0], STRUCK_RE.sub("", cells[1])
        blocks = [int(b) for b in re.findall(r"b(\d+)", block_cell)]
        if not blocks:
            continue
        for m in OP_RE.finditer(edit_cell):
            targets = [int(m.group("blk")[1:])] if m.group("blk") else blocks
            op = "add" if m.group("op") == "+" else "remove"
            for b in targets:
                edits.append((conv, b, m.group("sig"), op, cells[2]))
    return edits


def _span_for(text, why):
    """Best-effort evidence span for an added label: the quoted phrase from the
    change file's reason column when it can be located, else the whole block."""
    for quoted in re.findall(r'"([^"]{4,})"', why):
        for frag in re.split(r"…|\.\.\.", quoted):
            frag = frag.strip()
            if len(frag) >= 6:
                at = text.find(frag)
                if at >= 0:
                    return at, at + len(frag), frag, True
    return 0, len(text), text, False


def _new_id(project, conv, block, signal):
    seed = f"{project}|{conv}|{block}|{signal}".encode()
    digest = hashlib.md5(seed).hexdigest()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    n, out = int(digest[:16], 16), []
    while len(out) < 10:
        n, rem = divmod(n, len(alphabet))
        out.append(alphabet[rem])
    return "".join(out)


def apply_v06_edits(apply_changes):
    conv_of = {r["c_index"]: r["conv_id"]
               for r in csv.DictReader(open(ANNOT_DIR / "agreement_set_convid_map.csv"))}
    con = sqlite3.connect(db_path())

    # completion + dialogue per (project, conv_id)
    store = {}
    for pid, tid, data, res_raw, cid in con.execute(
            """SELECT t.project_id, t.id, t.data, tc.result, tc.id
               FROM task_completion tc JOIN task t ON t.id = tc.task_id
               WHERE tc.was_cancelled = 0 AND t.project_id IN (1, 2, 3)"""):
        payload = json.loads(data)
        store[(pid, payload.get("conv_id"))] = {
            "task": tid, "completion": cid, "dialogue": payload["dialogue"],
            "result": json.loads(res_raw), "dirty": False,
        }

    counts = {r: {"add": 0, "remove": 0, "add_noop": 0, "remove_noop": 0,
                  "span_located": 0, "span_block": 0} for r in RATER_PROJECT}
    problems = []

    for rater, project in RATER_PROJECT.items():
        path = BF_DIR / f"changes_{rater}.md"
        print(f"\n{'='*78}\n{path.name}  ->  project {project}\n{'='*78}")
        for conv, block, signal, op, why in parse_change_file(path):
            rec = store.get((project, conv_of[conv]))
            if rec is None:
                problems.append(f"{rater} {conv}: no completion in project {project}")
                continue
            items = [it for it in rec["result"]
                     if it.get("type") == "paragraphlabels"
                     and int(it["value"]["start"]) == block]
            present = [it for it in items if signal in it["value"]["paragraphlabels"]]

            if op == "remove":
                if not present:
                    counts[rater]["remove_noop"] += 1
                    print(f"  {conv} b{block:<4} - {signal:<32} (already absent)")
                    continue
                for it in present:
                    it["value"]["paragraphlabels"].remove(signal)
                    if not it["value"]["paragraphlabels"]:
                        rec["result"].remove(it)
                rec["dirty"] = True
                counts[rater]["remove"] += 1
                print(f"  {conv} b{block:<4} - {signal:<32} removed x{len(present)}")
            else:
                if present:
                    counts[rater]["add_noop"] += 1
                    print(f"  {conv} b{block:<4} + {signal:<32} (already present)")
                    continue
                text = rec["dialogue"][block]["text"].replace("\n", " ")
                o1, o2, span, located = _span_for(text, why)
                rec["result"].append({
                    "value": {"start": str(block), "end": str(block),
                              "startOffset": o1, "endOffset": o2, "text": span,
                              "paragraphlabels": [signal]},
                    "id": _new_id(project, conv, block, signal),
                    "from_name": "signals", "to_name": "dialogue",
                    "type": "paragraphlabels", "origin": "manual",
                })
                rec["dirty"] = True
                counts[rater]["add"] += 1
                counts[rater]["span_located" if located else "span_block"] += 1
                print(f"  {conv} b{block:<4} + {signal:<32} "
                      f"{'span' if located else 'BLOCK-WIDE'}: {span[:52]!r}")

    # Rule A7: conversation_advanced is dropped from the taxonomy -> strip it
    # from every completion in the three projects, not only the agreement 10.
    dropped = 0
    for rec in store.values():
        keep = []
        for it in rec["result"]:
            labels = it.get("value", {}).get("paragraphlabels")
            if labels and DROPPED_SIGNAL in labels:
                labels.remove(DROPPED_SIGNAL)
                dropped += 1
                rec["dirty"] = True
                if not labels:
                    continue
            keep.append(it)
        rec["result"] = keep
    print(f"\nA7 sweep: {dropped} {DROPPED_SIGNAL} label(s) stripped across projects 1-3")

    print(f"\n{'-'*78}\nper-annotator totals")
    for rater in RATER_PROJECT:
        c = counts[rater]
        print(f"  {rater}: {c['add']:>3} added ({c['span_located']} with a located "
              f"span, {c['span_block']} block-wide), {c['remove']:>3} removed; "
              f"no-ops {c['add_noop']} add / {c['remove_noop']} remove")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  " + p)

    touched = [r for r in store.values() if r["dirty"]]
    if apply_changes:
        for rec in touched:
            con.execute("""UPDATE task_completion SET result=?, updated_at=datetime('now')
                           WHERE id=?""",
                        (json.dumps(rec["result"], ensure_ascii=False), rec["completion"]))
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: "
          f"{len(touched)} completion(s) would change")


SPAN_SECTION_MARKER = "# Span fix-ups"
PREVIEW = 320


def _evidence_for(signal, why):
    """The part of a change-file reason that belongs to THIS signal.

    A reason column often covers several operations of the same row
    ("...; the post under critique is the object, not a cited source"), so the
    clause naming another signal is noise for this one. Prefer the quoted
    phrase; fall back to the clause that does not name a different signal.
    """
    why = re.sub(r"\s+", " ", why).strip()
    quotes = re.findall(r'"([^"]{4,})"', why)
    if quotes:
        return " / ".join(f'"{q}"' for q in quotes[:2])
    parts = [p.strip() for p in re.split(r";|·", why) if p.strip()]
    own = [p for p in parts
           if not re.search(r"`[a-z_]+`", p) or f"`{signal}`" in p]
    return (own[0] if own else why)[:160]


def list_wide_spans(write=False):
    """Report the labels added by --apply-v06-edits whose span still covers the
    whole block, because the change file's reason carried no quote precise
    enough to locate the evidence. Presence (and therefore kappa) is correct;
    only the span needs narrowing, by the annotator who owns the label.

    With --write, the report replaces the "Span fix-ups" section at the end of
    each changes_X.md, so every annotator keeps ONE to-do document.
    """
    conv_of = {r["c_index"]: r["conv_id"]
               for r in csv.DictReader(open(ANNOT_DIR / "agreement_set_convid_map.csv"))}
    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True)
    store = {}
    for pid, tid, data, res_raw in con.execute(
            """SELECT t.project_id, t.id, t.data, tc.result
               FROM task_completion tc JOIN task t ON t.id = tc.task_id
               WHERE tc.was_cancelled = 0 AND t.project_id IN (1, 2, 3)"""):
        payload = json.loads(data)
        store[(pid, payload.get("conv_id"))] = (tid, payload["dialogue"],
                                                json.loads(res_raw))
    con.close()

    for rater, project in RATER_PROJECT.items():
        per_conv = defaultdict(lambda: defaultdict(list))   # conv -> block -> rows
        meta, total = {}, 0
        for conv, block, signal, op, why in parse_change_file(
                BF_DIR / f"changes_{rater}.md"):
            if op != "add":
                continue
            rec = store.get((project, conv_of[conv]))
            if rec is None:
                continue
            tid, dialogue, result = rec
            wanted = _new_id(project, conv, block, signal)
            for it in result:
                if it.get("id") != wanted:
                    continue
                v = it["value"]
                text = dialogue[block]["text"].replace("\n", " ")
                if v["startOffset"] == 0 and v["endOffset"] == len(text):
                    per_conv[conv][block].append((signal, _evidence_for(signal, why)))
                    meta[conv] = (tid, conv_of[conv])
                    total += 1

        out = ["", "---", "",
               f"{SPAN_SECTION_MARKER} — same labels, narrower spans", "",
               f"**{total} labels across "
               f"{sum(len(b) for b in per_conv.values())} blocks.** Each one is "
               "already in your project on the right block with the right signal, "
               "so the agreement numbers are unaffected — only the highlight needs "
               "narrowing. They were added by script, and the reason recorded in "
               "the table above did not always quote enough text to place a span, "
               "so they currently cover the whole block.", "",
               "For each block below: open the task, select the evidence text, and "
               "move the label onto that selection. Span rule — consecutive "
               "exhibiting sentences form ONE span; occurrences separated by other "
               "text get SEPARATE labels.", ""]
        for conv in sorted(per_conv, key=lambda c: int(c[1:])):
            tid, url = meta[conv]
            out += [f"## {conv} — Label Studio task **{tid}**", f"<{url}>", ""]
            for block in sorted(per_conv[conv]):
                _, dialogue, _ = store[(project, conv_of[conv])]
                blk = dialogue[block]
                text = re.sub(r"\s+", " ", blk["text"]).strip()
                out.append(f"### block {block} — `{blk['author']}` "
                           f"({len(blk['text'])} chars)")
                for signal, evidence in sorted(per_conv[conv][block]):
                    out.append(f"- **`{signal}`** → select: {evidence}")
                out += ["", "  > " + text[:PREVIEW]
                        + ("…" if len(text) > PREVIEW else ""), ""]

        path = BF_DIR / f"changes_{rater}.md"
        if write:
            body = path.read_text().split("\n---\n\n" + SPAN_SECTION_MARKER)[0]
            path.write_text(body.rstrip("\n") + "\n" + "\n".join(out))
            print(f"{rater}: {total} span fix-up(s) written to {path.name}")
        else:
            print("\n".join([f"\n{'='*78}", f"{rater}: {total}", '='*78] + out))


# ----------------------------------------------------------------------------
# Mode 4: remove specific mislabeled items from Michelle's round-2 annotations
# (--fix-michelle-round2). See the module docstring for the rubric basis.
# ----------------------------------------------------------------------------

MICHELLE_ROUND2_REMOVALS = {
    176: {  # task 773 -- ai_structured_response fired on `code` blocks;
            # rubric restricts this signal to blocks: ["ai"]
        "wTHkvwElQO": "block 4  (code) - ai_structured_response restricted to blocks:[ai]",
        "V7IUnU0Tya": "block 7  (code) - ai_structured_response restricted to blocks:[ai]",
        "Di1_ugjsKt": "block 10 (code) - ai_structured_response restricted to blocks:[ai]",
        "XBZ-ZyNMag": "block 10 (code), 2nd span - ai_structured_response restricted to blocks:[ai]",
    },
    178: {  # task 770 -- ai_validates_user fired on bare compliance openers;
            # fails rubric Step 1 (SPECIFICITY TEST) / Step 3 (COMPLIANCE-OPENER
            # EXCLUSION). The 11 other fires in this task were reviewed and kept.
        "5dSJaOaMDt": 'block 19  "Correct."      - fails Step1/Step3',
        "t83Ywx9XEL": 'block 31  "Yeah,"          - fails Step1/Step3',
        "PiRtYxURpR": 'block 37  bare opener      - fails Step1/Step3',
        "_9TqjXgKAA": 'block 45  "True."          - fails Step1/Step3',
        "zcT9tXZG_n": 'block 55  bare opener      - fails Step1/Step3',
        "8t5MOAGtQZ": 'block 61  bare opener      - fails Step1/Step3',
        "hl6PM1Jgf3": 'block 71  "Right."         - fails Step1/Step3',
        "SV0xX-IPok": 'block 91  "No. Right,"     - fails Step1/Step3',
        "_shCg9zIEM": 'block 93  bare opener      - fails Step1/Step3',
        "9NgLoQB6sb": 'block 123 "Right."         - fails Step1/Step3',
        "bJIJ5U-Y1y": 'block 139 "Right."         - fails Step1/Step3',
        "c-rRSIB5XF": 'block 149 "Makes sense."   - fails Step1/Step3',
        "j7v2CRvSrC": 'block 153 bare opener      - fails Step1/Step3',
    },
}


def fix_michelle_round2(apply_changes):
    con = sqlite3.connect(db_path())
    total_removed, touched = 0, 0

    for completion_id, targets in MICHELLE_ROUND2_REMOVALS.items():
        row = con.execute(
            "SELECT task_id, result FROM task_completion WHERE id=?",
            (completion_id,)).fetchone()
        if row is None:
            print(f"  WARNING completion {completion_id}: not found, skipped")
            continue
        task_id, res_raw = row
        res = json.loads(res_raw)
        before = len(res)
        removed = [it for it in res if it.get("id") in targets]
        kept = [it for it in res if it.get("id") not in targets]
        missing = set(targets) - {it.get("id") for it in removed}
        if missing:
            print(f"  WARNING completion {completion_id}: expected id(s) not "
                  f"found in result, skipped: {sorted(missing)}")

        print(f"task {task_id:>3} completion {completion_id}: "
              f"result_count {before} -> {len(kept)}")
        for it in removed:
            labels = it.get("value", {}).get("paragraphlabels", [])
            print(f"    - {it['id']:<11} {labels} {targets[it['id']]}")

        if removed:
            total_removed += len(removed)
            touched += 1
            if apply_changes:
                con.execute(
                    """UPDATE task_completion SET result=?, updated_at=datetime('now')
                       WHERE id=?""",
                    (json.dumps(kept, ensure_ascii=False), completion_id))

    if apply_changes:
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: "
          f"{total_removed} label(s) removed across {touched} completion(s)")


# ----------------------------------------------------------------------------
# Mode 5: restore 11 of the 13 task-770 ai_validates_user removals, using
# Jun's own span (--restore-michelle-avu). See module docstring.
# ----------------------------------------------------------------------------

# Blocks 37 and 149 stay removed: Jun's project-1 read of task 83 (=R4, the
# same conversation) does NOT fire ai_validates_user there either, so those
# two removals were not in dispute. Source completion (Jun, project 1, task
# 83) and target completion (Michelle, project 5, task 770) are read live
# below rather than hardcoded, so the restored span is always Jun's actual
# text/offsets, never a hand-transcribed copy.
JUN_SOURCE_COMPLETION = {"task_id": 83, "project_id": 1}
MICHELLE_RESTORE_TARGET = {"task_id": 770, "completion_id": 178}
RESTORE_BLOCKS = [19, 31, 45, 55, 61, 71, 91, 93, 123, 139, 153]


def restore_michelle_avu(apply_changes):
    con = sqlite3.connect(db_path())

    jun_res = json.loads(con.execute(
        "SELECT result FROM task_completion WHERE task_id=? AND project_id=? "
        "AND was_cancelled=0", (JUN_SOURCE_COMPLETION["task_id"],
                                JUN_SOURCE_COMPLETION["project_id"])).fetchone()[0])
    jun_by_block = {}
    for it in jun_res:
        v = it.get("value", {})
        if SIGNAL not in v.get("paragraphlabels", []):
            continue
        jun_by_block[int(v["start"])] = v

    completion_id = MICHELLE_RESTORE_TARGET["completion_id"]
    target_res = json.loads(con.execute(
        "SELECT result FROM task_completion WHERE id=?",
        (completion_id,)).fetchone()[0])
    existing_blocks = {int(it["value"]["start"]) for it in target_res
                       if SIGNAL in it.get("value", {}).get("paragraphlabels", [])}

    added = []
    for blk in RESTORE_BLOCKS:
        if blk in existing_blocks:
            print(f"  WARNING block {blk}: {SIGNAL} already present on "
                  f"completion {completion_id}, skipped")
            continue
        v = jun_by_block.get(blk)
        if v is None:
            print(f"  WARNING block {blk}: not found in Jun's source "
                  f"completion, skipped")
            continue
        item = {
            "value": {"start": str(blk), "end": str(blk),
                      "startOffset": v["startOffset"], "endOffset": v["endOffset"],
                      "text": v["text"], "paragraphlabels": [SIGNAL]},
            "id": _new_id(5, "michelle-restore", blk, SIGNAL),
            "from_name": "signals", "to_name": "dialogue",
            "type": "paragraphlabels", "origin": "manual",
        }
        target_res.append(item)
        added.append((blk, v["text"]))
        print(f"    + block {blk:<4} {item['id']:<11} (Jun's span) "
              f"{v['text'][:70]!r}")

    print(f"\ntask {MICHELLE_RESTORE_TARGET['task_id']} completion "
          f"{completion_id}: result_count -> {len(target_res)} "
          f"({len(added)} restored)")

    if apply_changes and added:
        con.execute(
            """UPDATE task_completion SET result=?, updated_at=datetime('now')
               WHERE id=?""",
            (json.dumps(target_res, ensure_ascii=False), completion_id))
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: "
          f"{len(added)} label(s) restored")


# ----------------------------------------------------------------------------
# Mode 6: remove round-2 fires that violate rules round 1 already settled
# (--fix-round2-rule-violations). See module docstring.
# ----------------------------------------------------------------------------

FIX_ROUND2_RULE_VIOLATIONS = {
    176: {  # task 773 -- false_confidence on block 10; 2 of 3 spans are pure
            # code/markup with no claim (rubric: "instructions and feature
            # lists carry no claim"). The 3rd span on that block (not listed
            # here) contains a genuine unhedged claim and stays.
        "0MKd7WaSD3": "PTX assembly syntax, no claim",
        "VDpBapEeLK": "LaTeX table header, no claim",
    },
    172: {  # task 771 -- ai_provides_example fired on general claims,
            # descriptions, or the AI's self-report, not concrete
            # illustrative instances (rubric Step 1 + boundary_notes
            # .description_vs_illustration). Blocks 2 and 26 each keep one
            # sibling span (not listed here) that names a concrete case.
        "jpPOM_2WUv": "block 5   - three open questions, no instance",
        "TllUZVlL0P": "block 8   - definition of age-appropriateness, no instance",
        "1zxRDtvo2N": "block 8   - general accommodation strategies, no named instance",
        "fEjqNfKkf9": "block 11  - description of what traditions focus on, no instance",
        "IK5YyXcIai": "block 11  - description of what concepts represent, no instance",
        "ATVFKiJJmH": "block 17  - general argument for testing, no instance",
        "D30rx13MAY": "block 17  - general argument for authentic assessment, no instance",
        "-59gLnnU1f": "block 20  - general argued position, no instance",
        "cNypyfksrG": "block 20  - general argued position, no instance",
        "9gCpojhUBH": "block 32  - AI's self-report of its own behavior, not an illustration for the reader",
        "FiXNC9boT-": "block 60  - AI's self-report of its own behavior, not an illustration for the reader",
        "1-PIfhjc7p": "block 2   - general teaching approach, no named instance (kept sibling span is concrete)",
        "n77xkFa27N": "block 26  - general claim about Enlightenment thinkers collectively (kept sibling span names real figures)",
    },
}


def fix_round2_rule_violations(apply_changes):
    con = sqlite3.connect(db_path())
    total_removed, touched = 0, 0

    for completion_id, targets in FIX_ROUND2_RULE_VIOLATIONS.items():
        row = con.execute(
            "SELECT task_id, result FROM task_completion WHERE id=?",
            (completion_id,)).fetchone()
        if row is None:
            print(f"  WARNING completion {completion_id}: not found, skipped")
            continue
        task_id, res_raw = row
        res = json.loads(res_raw)
        before = len(res)
        removed = [it for it in res if it.get("id") in targets]
        kept = [it for it in res if it.get("id") not in targets]
        missing = set(targets) - {it.get("id") for it in removed}
        if missing:
            print(f"  WARNING completion {completion_id}: expected id(s) not "
                  f"found in result, skipped: {sorted(missing)}")

        print(f"task {task_id:>3} completion {completion_id}: "
              f"result_count {before} -> {len(kept)}")
        for it in removed:
            labels = it.get("value", {}).get("paragraphlabels", [])
            print(f"    - {it['id']:<11} {labels} {targets[it['id']]}")

        if removed:
            total_removed += len(removed)
            touched += 1
            if apply_changes:
                con.execute(
                    """UPDATE task_completion SET result=?, updated_at=datetime('now')
                       WHERE id=?""",
                    (json.dumps(kept, ensure_ascii=False), completion_id))

    if apply_changes:
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: "
          f"{total_removed} label(s) removed across {touched} completion(s)")


if __name__ == "__main__":
    _apply = "--apply" in sys.argv
    if "--list-wide-spans" in sys.argv:
        list_wide_spans(write="--write" in sys.argv)
    elif "--apply-v06-edits" in sys.argv:
        apply_v06_edits(_apply)
    elif "--fix-michelle-round2" in sys.argv:
        fix_michelle_round2(_apply)
    elif "--fix-round2-rule-violations" in sys.argv:
        fix_round2_rule_violations(_apply)
    elif "--restore-michelle-avu" in sys.argv:
        restore_michelle_avu(_apply)
    else:
        fix_span_drift(_apply)
