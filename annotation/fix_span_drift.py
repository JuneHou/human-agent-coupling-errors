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

Usage:
    python annotation/fix_span_drift.py [--apply]
    python annotation/fix_span_drift.py --apply-v06-edits [--apply] [--db PATH]
    python annotation/fix_span_drift.py --list-wide-spans [--write]
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


if __name__ == "__main__":
    _apply = "--apply" in sys.argv
    if "--list-wide-spans" in sys.argv:
        list_wide_spans(write="--write" in sys.argv)
    elif "--apply-v06-edits" in sys.argv:
        apply_v06_edits(_apply)
    else:
        fix_span_drift(_apply)
