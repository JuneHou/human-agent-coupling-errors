"""Annotation-result repairs written back to the Label Studio DB.

Mode 14 (--apply-v07-merges) -- carry the rubric v0.7 signal merges into the
stored annotations of ALL FIVE projects: ai_asked_probing_question ->
ai_asks_followup, intent_missed and under_delivered -> request_unfulfilled,
user_expresses_frustration -> user_expresses_dissatisfaction. Renaming can
put one signal twice on one target, so the mode de-duplicates inside an item
and on an identical span, and REPORTS same-block/different-span collisions
instead of guessing at them.

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

Mode 7 (--import-priya-missing) -- create the 6 round-2 completions Priya has not yet
submitted in Label Studio (project 4, tasks 757/758/759/760/761/766) from the .md tables
she provided in Rubric_agree/round_2/priya/. Skips any task that already has a completion
(the other 4 of her 10 -- 762/763/764/765 -- are left untouched by construction; her .md
files for those disagree with what's already saved for them, so importing over them is a
separate decision, not part of this mode). Each row's block is resolved by role + a
forward-only cursor (rows are written in conversation order), then _span_for locates the
row's quoted text inside that block, reusing the same fragment-search Mode 2 uses. Where no
exact text is locatable -- confirmed to happen on ~30-50% of rows, since several of Priya's
"A ... B" spans are truncated previews rather than true ellipsis-elided middles, and code
blocks sometimes have formatting stripped -- the label is written BLOCK-WIDE (matches the
existing "presence correct, span needs narrowing" convention from Mode 2/3) rather than
guessing at boundaries.

All modes are dry-run unless --apply is passed.

Usage:
    python annotation/fix_span_drift.py [--apply]
    python annotation/fix_span_drift.py --apply-v06-edits [--apply] [--db PATH]
    python annotation/fix_span_drift.py --list-wide-spans [--write]
    python annotation/fix_span_drift.py --fix-michelle-round2 [--apply] [--db PATH]
    python annotation/fix_span_drift.py --restore-michelle-avu [--apply] [--db PATH]
    python annotation/fix_span_drift.py --fix-round2-rule-violations [--apply] [--db PATH]
    python annotation/fix_span_drift.py --import-priya-missing [--apply] [--db PATH]
    python annotation/fix_span_drift.py --apply-round2-draft [--apply] [--db PATH]
    python annotation/fix_span_drift.py --fix-priya-role-violations [--apply] [--db PATH]
    python annotation/fix_span_drift.py --apply-v07-merges [--apply] [--db PATH]
    python annotation/fix_span_drift.py --v07-rescan-screen [--db PATH]
    python annotation/fix_span_drift.py --apply-v07-screen [--apply] [--db PATH]
    python annotation/fix_span_drift.py --refresh-priya-md [757,758,...] [--apply]
    python annotation/fix_span_drift.py --fix-task-counters [--apply] [--db PATH]
    python annotation/fix_span_drift.py --fix-span-hygiene [--apply] [--db PATH]
    python annotation/fix_span_drift.py --round3-rescan-report [--db PATH]
    python annotation/fix_span_drift.py --apply-round3-rescan [--apply] [--db PATH]

Mode 10 (--fix-priya-role-violations) -- remove Priya's 10 confirmed round-2 label
violations: ai_structured_response fired on code-role blocks (task 759 blocks
1/7/12/15/18/21/24 -- block 1 carries two separate items -- and task 762 blocks 4/5),
same class already fixed for Michelle via Mode 4; plus one ai_malfunction item (task 763
block 1) with valid offsets but empty text, a UI-selection glitch rather than a real label.
Found via this session's Priya quality review (round_2/priya/quality_and_disagreement_review.md).

Mode 9 (--apply-round2-draft) -- write back the completed round-2 walk
(Rubric_agree/round_2/round2_disagreement_draft.md, all 43 signals "closed," ruled
2026-09-14) to Jun's project-1 and Michelle's project-5 data for the 10 R-conversations.
Confirmed this session (2026-09-19) that none of these rulings were ever applied to either
rater's live DB. Parses the draft at runtime rather than hardcoding the action list, and
refuses to run if any signal's parsed ACCEPT/CORRECT-A/CORRECT-M/relabel counts don't match
that section's own stated tally line -- the draft is written so every section self-checks.
Excludes by construction: `user_expresses_dissatisfaction` and `user_expresses_frustration`
(both explicitly HELD/reopened, not closed), `factual_error` R10 b7 (HOLD, pending
tax-law verification), and the `user_implicit_correction` R9 b3 "relabel to adaptation"
candidate (explicitly left OPEN, not ruled). Also applies the one in-scope consistency-sweep
correction (`adaptation`, task 80/768 b31 and task 81/769 b25, ruled "both drop") to both
raters. Does NOT touch Priya's project-4 data or the `ai_provides_caveats` consistency-sweep
cells outside the R1-R10 set (Jun's tasks 14/31/43/49) -- both out of scope for this pass.
"""
import collections
import csv, hashlib, json, re, sqlite3, sys, uuid
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


# ----------------------------------------------------------------------------
# Mode 7: create Priya's 6 not-yet-submitted round-2 completions from her .md
# tables (--import-priya-missing). See module docstring.
# ----------------------------------------------------------------------------

PRIYA_DIR = ANNOT_DIR / "Rubric_agree" / "round_2" / "priya"
PRIYA_MISSING = {
    757: "757.md", 758: "annotations_758.md", 759: "annotations_759.md",
    760: "annotations_760.md", 761: "annotations_761.md", 766: "annotations_766.md",
}
PRIYA_PROJECT_ID = 4
PRIYA_USER_ID = 4


def parse_priya_md(path):
    """Yield (signal, block_role, span_text_or_None) for each data row of one
    of Priya's annotation tables. span_text is None for a row that carries
    only a bracketed description and no quoted text."""
    rows = []
    for line in Path(path).read_text().splitlines():
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| #"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        _, signal_cell, role, _turn, span_cell = cells[:5]
        signal = signal_cell.strip("`")
        quotes = re.findall(r'"([^"]*)"', span_cell)
        rows.append((signal, role, quotes[-1] if quotes else None))
    return rows


def import_priya_missing(apply_changes):
    con = sqlite3.connect(db_path())
    total_added, touched = 0, 0

    for task_id, fname in PRIYA_MISSING.items():
        existing = con.execute(
            "SELECT id FROM task_completion WHERE task_id=? AND completed_by_id=?",
            (task_id, PRIYA_USER_ID)).fetchone()
        if existing:
            print(f"task {task_id}: completion {existing[0]} already exists, skipped")
            continue

        dialogue = json.loads(con.execute(
            "SELECT data FROM task WHERE id=?", (task_id,)).fetchone()[0])["dialogue"]
        rows = parse_priya_md(PRIYA_DIR / fname)

        print(f"\n{'='*78}\ntask {task_id} <- {fname}  ({len(rows)} rows)\n{'='*78}")
        result, unresolved, occurrence = [], [], defaultdict(int)
        cursor = 0
        for signal, role, span_text in rows:
            all_candidates = [i for i, b in enumerate(dialogue) if b.get("author") == role]
            # Rows are mostly in conversation order, but Priya's own "Turn"
            # numbering is not always monotonic with true block order (task
            # 760: her turn-117 text sits at block 169, textually AFTER the
            # block-167 content she labeled turn-123/131) -- so pick the
            # LOCATED match nearest the cursor, not strictly the next one
            # forward. Only fall back to block-wide when nothing locates.
            located_matches = []
            for i in all_candidates:
                block_text = dialogue[i]["text"].replace("\n", " ")
                if span_text:
                    o1, o2, text, loc = _span_for(block_text, f'"{span_text}"')
                    if loc:
                        located_matches.append((abs(i - cursor), i, o1, o2, text))
            if located_matches:
                located_matches.sort(key=lambda t: t[0])
                _, chosen, o1, o2, text = located_matches[0]
                located = True
            else:
                chosen = min(all_candidates, key=lambda i: abs(i - cursor)) \
                    if all_candidates else cursor
                block_text = dialogue[chosen]["text"].replace("\n", " ")
                o1, o2, text, located = 0, len(block_text), block_text, False
                unresolved.append((signal, chosen))

            cursor = chosen
            occ_key = (chosen, signal)
            seed_signal = f"{signal}#{occurrence[occ_key]}"
            occurrence[occ_key] += 1
            result.append({
                "value": {"start": str(chosen), "end": str(chosen),
                          "startOffset": o1, "endOffset": o2, "text": text,
                          "paragraphlabels": [signal]},
                "id": _new_id(PRIYA_PROJECT_ID, task_id, chosen, seed_signal),
                "from_name": "signals", "to_name": "dialogue",
                "type": "paragraphlabels", "origin": "manual",
            })
            print(f"  b{chosen:<4} [{role:<9}] + {signal:<32} "
                  f"{'span' if located else 'BLOCK-WIDE'}: {text[:60]!r}")

        print(f"  -> {len(result)} label(s), {len(unresolved)} block-wide fallback(s)")
        if unresolved:
            print(f"     fallback: {unresolved}")

        total_added += len(result)
        touched += 1
        if apply_changes:
            con.execute(
                """INSERT INTO task_completion
                   (result, was_cancelled, created_at, updated_at, task_id,
                    prediction, result_count, completed_by_id, ground_truth,
                    project_id, updated_by_id, unique_id, bulk_created)
                   VALUES (?, 0, datetime('now'), datetime('now'), ?, '{}',
                           ?, ?, 0, ?, ?, ?, 1)""",
                (json.dumps(result, ensure_ascii=False), task_id, len(result),
                 PRIYA_USER_ID, PRIYA_PROJECT_ID, PRIYA_USER_ID, uuid.uuid4().hex))

    if apply_changes:
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: "
          f"{total_added} label(s) across {touched} new completion(s)")



# ----------------------------------------------------------------------------
# Write Michelle's corrected round-3 arm into her Label Studio project
# (--import-michelle-round3). Her ten markdown files are the source; the agreed
# corrections in round_3/changes_Michelle.md are applied on top, and the result
# is written as one completion per task. Markdown flows INTO Label Studio and is
# never regenerated from it.
# ----------------------------------------------------------------------------

MICHELLE_R3_DIR_IMPORT = ANNOT_DIR / "Rubric_agree" / "round_3" / "michelle"
MICHELLE_R3_CHANGES = ANNOT_DIR / "Rubric_agree" / "round_3" / "changes_Michelle.md"
MICHELLE_R3_PROJECT_ID = 9
MICHELLE_R3_USER_ID = 5
# Her file shapes, each declared in the file's own header: a bold one-liner, a
# markdown table, or a table keyed by turn id. The number is the block base.
MICHELLE_R3_FILE_SHAPE = {
    787: ("bold", 1), 788: ("bold", 1), 789: ("bold", 0), 790: ("bold", 0),
    791: ("bold", 0), 792: ("bold", 0), 793: ("table", 1), 794: ("table", 1),
    795: ("btable", 1), 796: ("turn", None),
}
# Task 133: her replacement file of 2026-09-23 supersedes the original.
MICHELLE_R3_FILENAME = {795: "task795_new.md"}
# Cells the walk raised but Jun has not ruled. They stay out until he does.
MICHELLE_R3_HELD = {(795, 2, "user_asks_clarification")}

_M_PUNCT = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"',
                          "\u201d": '"', "\u00a0": " "})


def _m_norm_map(txt):
    """Whitespace-collapsed copy of a block plus the index of each kept
    character, so a span found in the copy maps back to real offsets."""
    txt = txt.translate(_M_PUNCT)
    out, idx, prev_space = [], [], False
    for i, ch in enumerate(txt):
        if ch.isspace():
            if prev_space:
                continue
            out.append(" "); idx.append(i); prev_space = True
        else:
            out.append(ch); idx.append(i); prev_space = False
    return "".join(out), idx


def _m_span_candidates(row):
    """Quoted text a row offers as its evidence, best guess first."""
    row = row.translate(_M_PUNCT)
    out = []
    m = re.search(r"Span[^:]{0,12}:\s*(.+?)(?:\s*\|\s*Step|\s*\*\*\s*$|$)", row)
    if m:
        out.append(m.group(1))
    out += re.findall(r'"([^"]{8,})"', row)
    return out


def _m_parse_files(signals):
    """Her ten files -> {(task, block, signal): [row text, ...]}."""
    blk_re = re.compile(r"\bB(?:lock)?\s*(\d+)\b")
    turn_re = re.compile(r"task(?:79[56])_(\d+)_(human|ai|reasoning|analysis|code)")
    nofire_re = re.compile(r"label 0|does NOT fire|Excluded:", re.I)
    # A withdrawal can also sit after the span quote ("... block - label 0, does
    # NOT fire."), so the tail is checked too, with quoted text removed so that a
    # span that merely mentions the words cannot suppress a real fire. "Excluded:"
    # is left out of the tail test: it names competing signals on rows that do fire.
    tail_re = re.compile(r"label 0|does NOT fire", re.I)
    prose_re = re.compile(r"`([a-z_]+)`[\s\S]{0,400}?[Ff]ires on\s+"
                          r"\*\*task(?:79[56])_(\d+)_(human|ai|reasoning|analysis|code)\*\*")
    alias = {"ai_provides_structured_response": "ai_structured_response"}
    fires = defaultdict(list)

    for task_id, (shape, base) in sorted(MICHELLE_R3_FILE_SHAPE.items()):
        name = MICHELLE_R3_FILENAME.get(task_id, f"task{task_id}.md")
        # Commentary is not a label (Jun, 2026-09-22: "notes is not fire").
        body = (MICHELLE_R3_DIR_IMPORT / name).read_text().split("## Notes for Jun")[0]
        for line in body.splitlines():
            ln = line.strip()
            if shape == "bold":
                m = re.match(r"\*\*([a-z_]+)\s*\|", ln)
                if not m:
                    continue
                head, _, tail = ln[m.end():].partition("Span")
                if nofire_re.search(head):
                    continue
                if tail_re.search(re.sub(r'"[^"]*"', "", tail)):
                    continue
                signal, where, row = m.group(1), head, ln
            else:
                cells = [x.strip() for x in ln.strip("|").split("|")]
                if len(cells) < 3:
                    continue
                signal, where, row = cells[0], cells[1], cells[2]
            signal = alias.get(signal, signal)
            if signal not in signals:
                continue
            if shape == "turn":
                t = turn_re.search(where)
                if not t:
                    continue
                k, role = int(t.group(1)), t.group(2)
                blocks = [2 * k - 2 if role == "human" else 2 * k - 1]
            else:
                blocks = [int(x) - base for x in blk_re.findall(where)]
            for b in blocks:
                fires[(task_id, b, signal)].append(row)
        # A block-level signal has no sentence to quote, so some are recorded as
        # a paragraph in the turn body rather than as a row.
        for m in prose_re.finditer(body):
            signal, k, role = m.group(1), int(m.group(2)), m.group(3)
            if signal in signals:
                fires[(task_id, 2 * k - 2 if role == "human" else 2 * k - 1,
                       signal)].append("")
    return fires


def _m_parse_corrections():
    """changes_Michelle.md -> (adds, removes). Section heading decides which."""
    row_re = re.compile(r"^\|\s*(\d{3})\s+b(\d+)\s*\|\s*`([a-z_]+)`")
    adds, removes, section = [], [], ""
    for line in MICHELLE_R3_CHANGES.read_text().splitlines():
        if line.startswith("#"):
            section = line.strip("# ").strip()
        m = row_re.match(line)
        if not m:
            continue
        cell = (int(m.group(1)), int(m.group(2)), m.group(3))
        if section.startswith("Add"):
            adds.append(cell)
        elif section.startswith("Remove"):
            removes.append(cell)
    return adds, removes


def import_michelle_round3(apply_changes):
    signals = set(json.loads((ANNOT_DIR / "sharechat_rubric.json").read_text())["signals"])
    fires = _m_parse_files(signals)
    adds, removes = _m_parse_corrections()

    before = len(fires)
    for cell in removes:
        if cell in fires:
            del fires[cell]
        else:
            print(f"  correction not applicable, no such fire: {cell}")
    added = 0
    for cell in adds:
        if cell in MICHELLE_R3_HELD:
            print(f"  held, not ruled by Jun: {cell}")
        elif cell in fires:
            print(f"  correction already present: {cell}")
        else:
            fires[cell] = [""]
            added += 1
    print(f"\nher files {before} cells -> corrected {len(fires)} "
          f"({added} added, {len(removes)} removed)")

    con = sqlite3.connect(db_path())
    dialogues = {t: json.loads(d)["dialogue"] for t, d in con.execute(
        "SELECT id, data FROM task WHERE project_id = ?", (MICHELLE_R3_PROJECT_ID,))}

    results, located, block_wide = defaultdict(list), 0, 0
    for (task_id, block, signal), rows in sorted(fires.items()):
        text = dialogues[task_id][block]["text"]
        flat, index = _m_norm_map(text)
        start, end, found = 0, len(text), False
        for row in rows:
            hit = None
            for cand in _m_span_candidates(row):
                cand = cand.strip().strip('"').strip()
                for probe in (cand, cand.split("...")[0], cand.split("\u2026")[0]):
                    probe = re.sub(r"\s+", " ",
                                   re.sub(r"\s*/\s*", " ", probe)).strip().translate(_M_PUNCT)
                    if len(probe) >= 8 and probe in flat:
                        at = flat.index(probe)
                        hit = (index[at], index[at + len(probe) - 1] + 1)
                        break
                if hit:
                    break
            if hit:
                start, end, found = hit[0], hit[1], True
                break
        if found:
            located += 1
        else:
            block_wide += 1
        results[task_id].append({
            "value": {"start": str(block), "end": str(block),
                      "startOffset": start, "endOffset": end,
                      "text": text[start:end], "paragraphlabels": [signal]},
            "id": uuid.uuid4().hex[:10], "from_name": "signals",
            "to_name": "dialogue", "type": "paragraphlabels", "origin": "manual"})

    print(f"spans located in the block text: {located}, "
          f"whole-block fallback: {block_wide}")
    for task_id in sorted(results):
        existing = con.execute(
            "SELECT id FROM task_completion WHERE task_id = ? AND completed_by_id = ?",
            (task_id, MICHELLE_R3_USER_ID)).fetchone()
        state = f"REPLACES completion {existing[0]}" if existing else "new"
        print(f"  task {task_id}: {len(results[task_id]):3d} label(s)  [{state}]")
        if apply_changes:
            if existing:
                con.execute("DELETE FROM task_completion WHERE id = ?", (existing[0],))
            con.execute(
                """INSERT INTO task_completion
                   (result, was_cancelled, created_at, updated_at, task_id,
                    prediction, result_count, completed_by_id, ground_truth,
                    project_id, updated_by_id, unique_id, bulk_created)
                   VALUES (?, 0, datetime('now'), datetime('now'), ?, '{}',
                           ?, ?, 0, ?, ?, ?, 1)""",
                (json.dumps(results[task_id], ensure_ascii=False), task_id,
                 len(results[task_id]), MICHELLE_R3_USER_ID, MICHELLE_R3_PROJECT_ID,
                 MICHELLE_R3_USER_ID, uuid.uuid4().hex))
    if apply_changes:
        con.commit()
    con.close()
    total = sum(len(v) for v in results.values())
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: {total} label(s) "
          f"across {len(results)} completion(s) in project {MICHELLE_R3_PROJECT_ID}")

# ----------------------------------------------------------------------------
# Mode 9: write back round2_disagreement_draft.md's completed walk to Jun's and
# Michelle's data (--apply-round2-draft). See module docstring.
# ----------------------------------------------------------------------------

ROUND2_DRAFT_PATH = ANNOT_DIR / "Rubric_agree" / "round_2" / "round2_disagreement_draft.md"
ROUND2_CONV_MAP_PATH = ANNOT_DIR / "Rubric_agree" / "round_2" / "agreement_set_round2.csv"
RATER_PROJECT_ROUND2 = {"A": 1, "M": 5}

EXCLUDED_SIGNALS_ROUND2 = {"user_expresses_dissatisfaction", "user_expresses_frustration"}

# The one in-scope consistency-sweep correction (adaptation): found during the walk while
# auditing every adaptation label either rater had, outside the original 223-cell set.
# Ruled "both drop" -- applies to both raters' copies of these two conversations.
CONSISTENCY_SWEEP_ADAPTATION = [
    ("A", "R2", 31), ("M", "R2", 31),   # task 80 / task 768
    ("A", "R3", 25), ("M", "R3", 25),   # task 81 / task 769
]

# Signals where the document's own "Signal tally" counts CELLS, not table rows/DB items --
# a cell with multiple spans that all get the same verdict is sometimes one combined row
# ("(both spans)" in the ruling text, e.g. ai_cites_source R5 b44) rather than one row per
# span (e.g. ai_provides_example R9 b6, ai_cites_source R5 b38's 3 spans on 3 rows). Either
# way every occurrence needs its own DB removal, so the parsed row count legitimately
# exceeds the document's cell count -- verified by hand for both signals before allowlisting.
ALLOWED_TALLY_DEVIATIONS = {"ai_provides_example", "ai_cites_source"}

# Sections with a known, expected count of non-standard-table ("UNKNOWN") rows: the
# adaptation consistency sweep (2 rows, in scope, handled via CONSISTENCY_SWEEP_ADAPTATION)
# and the ai_provides_caveats consistency sweep (4 rows, Jun's 148-task corpus, explicitly
# out of scope for this pass -- see module docstring). Any OTHER UNKNOWN row still blocks.
KNOWN_CONSISTENCY_SWEEP_ROWS = {"adaptation": 2, "ai_provides_caveats": 4}

# Michelle's actual PDF response ("Annotating for Jun.pdf", read 2026-09-19) to the
# changes_Michelle.md summary of this walk disputed some of round2_disagreement_draft.md's
# rulings, or independently produced a different, valid fix rather than the plain removal
# the ruling specified. round2_disagreement_draft.md records JUN'S ruling (dated
# 2026-09-14) -- it is not itself proof Michelle agreed, and her later pushback supersedes
# it where the two conflict. Per feedback-unresolved-disagreement-policy.md, an objector's
# rejection means the point stays as her label, not silently overridden. Confirmed live in
# the DB before excluding (not just from her PDF text):
EXCLUDED_ROUND2_ACTIONS = {
    # (rater, r_index, block, signal): reason
    ("M", "R4", 67, "ai_asks_followup"):
        "Michelle disputed this directly: \"I'm not quite sure what this correction "
        "means. The only label I put there was ai_asks_followup, there is no probing "
        "question... I kept this one as ai_asks_followup.\"",
    ("M", "R4", 101, "ai_asks_followup"):
        "Same dispute as R4 b67: \"Same as above. I kept this one as ai_asks_followup.\"",
    ("M", "R9", 2, "ai_asserts_knowledge_limit"):
        "Michelle disputed this directly: \"I feel like this still deserves the "
        "knowledge_limit label because the AI explicitly says 'I can't identify "
        "anything'.\"",
    ("M", "R3", 25, "adaptation"):
        "Not a removal -- Michelle repositioned the span within the same block to the "
        "completed-change sentence (\"I've made the requested changes:\"), which "
        "satisfies the round-2 adaptation gate the original 'I'll revise...' span "
        "failed. Confirmed live: her current label at task 769 b25 already reads "
        "\"...I've made the requested changes: ...\". Removing it would destroy her "
        "correct fix, not apply one. Jun's own copy (task 81 b25) is still the "
        "unfixed prospective-only span and stays in the removal list.",
}


def _classify_ruling(ruling_cell):
    """Return (action, rater_or_None, new_signal_or_None). See Mode 9 docstring for why
    the FIRST bold span is checked before the whole cell: a cell can read "ACCEPT
    (overrules the proposed CORRECT-A...)" or mention a `relabel to `X`` candidate that
    was explicitly left open -- the bolded span is always this document's actual verdict."""
    bold = re.search(r"\*\*([^*]+)\*\*", ruling_cell)
    for scope in ([bold.group(1)] if bold else []) + [ruling_cell]:
        s = scope.strip()
        if re.match(r"^ACCEPT\b", s):
            return "accept", None, None
        if re.match(r"^HOLD\b", s) or s.startswith("HELD"):
            return "hold", None, None
        m = re.search(r"CORRECT-([AM])", scope)
        if m:
            return "remove", m.group(1), None
        rm = re.search(r"relabel(?:\s+HERE)?\s+to\s+`([a-z_]+)`", scope, re.I)
        if rm:
            return "relabel", None, rm.group(1)
        if re.search(r"NOT FIRE", scope):
            return "remove", None, None  # rater inferred from the row's FIRE column
    return "unknown", None, None


def parse_round2_draft(path=ROUND2_DRAFT_PATH):
    """Parse the draft into (signal, rater, r_index, block, action, new_signal, quoted_text)
    actions, validating every section's parsed counts against its own stated tally line.
    Raises if any non-excluded section's counts don't match -- see module docstring."""
    raw = Path(path).read_text()
    header_re = re.compile(r"^## (\S+) \(([^)]*)\)", re.M)
    headers = {m.group(1): m.group(2) for m in header_re.finditer(raw)}

    def default_r(paren_text):
        rs = sorted(set(re.findall(r"R\d+", paren_text)))
        return rs[0] if len(rs) == 1 else None

    sections = re.split(r"^## (\S+) \(", raw, flags=re.M)
    signal_bodies = {sections[i]: sections[i + 1] for i in range(1, len(sections), 2)}

    actions = []
    mismatches = []
    for signal, body in signal_bodies.items():
        if signal in EXCLUDED_SIGNALS_ROUND2:
            continue
        cur_r = default_r(headers.get(signal, ""))
        counts = defaultdict(int)
        lines = body.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.match(r"^### (R\d+)", line)
            if m:
                cur_r = m.group(1)
            if line.startswith("|") and not re.match(r"^\|[\s:-]+\|", line):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells[0] in ("Block", "Cell", "#", "Task") or len(cells) < 3:
                    i += 1
                    continue
                id_cell, ruling_cell = cells[0], cells[-1]
                rm = re.match(r"(R\d+)[,\s]*\(?\s*b?(\d+)", id_cell)
                if rm:
                    r_idx, block = rm.group(1), int(rm.group(2))
                else:
                    bm = re.match(r"b?\s*(\d+)", id_cell)
                    if not bm or cur_r is None:
                        i += 1
                        continue
                    r_idx, block = cur_r, int(bm.group(1))

                action, rater, new_sig = _classify_ruling(ruling_cell)
                if action in ("relabel", "remove") and rater is None:
                    fire_idx = [k for k, v in enumerate(cells) if v == "FIRE"]
                    if len(fire_idx) == 1 and len(cells) >= 4:
                        pos = len(cells) - 1 - fire_idx[0]
                        rater = "A" if pos == 2 else ("M" if pos == 1 else None)

                key = {"remove": f"CORRECT-{rater}", "relabel": "relabel",
                       "accept": "ACCEPT", "hold": "HOLD",
                       "unknown": "UNKNOWN"}[action]
                counts[key] += 1
                if action in ("remove", "relabel"):
                    quoted = ""
                    for c in cells[1:-1]:
                        if len(c) > 3 and c not in ("FIRE", "–", "-") and \
                           not re.match(r"^(ai|human|code|reasoning|analysis)$", c):
                            quoted = c
                            break
                    actions.append((signal, rater, r_idx, block, action, new_sig, quoted[:120]))
            i += 1

        if "UNKNOWN" in counts:
            expected = KNOWN_CONSISTENCY_SWEEP_ROWS.get(signal)
            if expected is None or counts["UNKNOWN"] != expected:
                mismatches.append(
                    f"{signal}: {dict(counts)} has {counts['UNKNOWN']} UNKNOWN row(s), "
                    f"expected {expected} -- likely a non-standard table (e.g. consistency "
                    f"sweep) with an unexpected shape, needs manual check")
                continue
            # known-shape consistency-sweep rows (handled separately, see
            # CONSISTENCY_SWEEP_ADAPTATION / the out-of-scope exclusion note) --
            # validate the REST of this section's counts normally below.
            del counts["UNKNOWN"]
        if signal in ALLOWED_TALLY_DEVIATIONS:
            continue
        tally_m = re.search(r"\*\*Signal tally.*?:\*\*\s*(.+)", body)
        if tally_m:
            stated_total = None
            nums = re.findall(r"(\d+)\s*\+\s*\d+|(\d+)\.\s*✓", tally_m.group(1))
            eq = re.search(r"=\s*(\d+)\.?\s*✓", tally_m.group(1))
            if eq:
                stated_total = int(eq.group(1))
            elif re.search(r"^(\d+)\.\s*✓", tally_m.group(1).strip()):
                stated_total = int(re.match(r"(\d+)", tally_m.group(1).strip()).group(1))
            parsed_total = sum(counts.values())
            if stated_total is not None and stated_total != parsed_total:
                mismatches.append(f"{signal}: parsed total {parsed_total} != "
                                   f"stated total {stated_total} ({dict(counts)})")

    return actions, mismatches


def apply_round2_draft(apply_changes):
    conv_to_c = {r["c_index"]: r["conv_id"] for r in
                 csv.DictReader(l for l in open(ROUND2_CONV_MAP_PATH) if not l.startswith("#"))}

    actions, mismatches = parse_round2_draft()
    # the one in-scope consistency-sweep correction, added explicitly (different table
    # shape in the source file, not worth generalizing the parser for two rows)
    for rater, r_idx, block in CONSISTENCY_SWEEP_ADAPTATION:
        actions.append(("adaptation", rater, r_idx, block, "remove", None,
                         "(consistency sweep: 'both drop', ruled 2026-09-14)"))

    if mismatches:
        print("REFUSING TO PROCEED -- parsed counts don't match the draft's own tallies:")
        for m in mismatches:
            print("  " + m)
        print(f"\n{len(actions)} action(s) were parsed before the mismatch was hit; not applying.")
        return

    kept = []
    for a in actions:
        signal, rater, r_idx, block, action, new_sig, quoted = a
        reason = EXCLUDED_ROUND2_ACTIONS.get((rater, r_idx, block, signal))
        if reason:
            print(f"  EXCLUDED  {rater} {r_idx} b{block:<4} {signal:28} -- {reason}")
        else:
            kept.append(a)
    actions = kept
    print()

    print(f"Parsed {len(actions)} action(s) from {ROUND2_DRAFT_PATH.name} "
          f"({len(EXCLUDED_ROUND2_ACTIONS)} excluded per Michelle's PDF pushback, see above), "
          f"all section tallies verified.\n")

    con = sqlite3.connect(db_path())
    # completion cache: (project, conv_id) -> {"id":..., "result": [...], "dirty": bool}
    store = {}
    for pid in set(RATER_PROJECT_ROUND2.values()):
        for tid, data, res_raw, cid in con.execute(
                """SELECT t.id, t.data, tc.result, tc.id FROM task_completion tc
                   JOIN task t ON t.id = tc.task_id
                   WHERE tc.was_cancelled = 0 AND t.project_id = ?""", (pid,)):
            conv = json.loads(data).get("conv_id")
            store[(pid, conv)] = {"task": tid, "completion": cid,
                                   "result": json.loads(res_raw), "dirty": False}

    # Group "remove" actions by exactly what they target: a (block, signal) can carry
    # several separate occurrences (rubric A3), and the source document sometimes lists
    # them as one combined row ("(both spans)") and sometimes as separate rows (see
    # ALLOWED_TALLY_DEVIATIONS above). If there's only ONE remove-action for a given
    # target, every matching item there gets removed (safe: the ruling is "this signal
    # shouldn't be at this block at all"). If there are MULTIPLE remove-actions for the
    # same target (distinct rows, distinct quotes -- e.g. one span stays, one goes),
    # each action is matched to a distinct item by quoted-text overlap, greedily,
    # without reusing an item already claimed by an earlier action.
    remove_target_counts = defaultdict(int)
    for signal, rater, r_idx, block, action, new_sig, quoted in actions:
        if action == "remove":
            remove_target_counts[(rater, r_idx, block, signal)] += 1
    claimed = defaultdict(set)  # (project, conv, block, signal) -> set of claimed item ids

    counts = {"remove": 0, "relabel": 0, "not_found": 0, "ambiguous": 0}
    for signal, rater, r_idx, block, action, new_sig, quoted in actions:
        project = RATER_PROJECT_ROUND2[rater]
        conv = conv_to_c[r_idx]
        rec = store.get((project, conv))
        if rec is None:
            print(f"  WARNING {rater} {r_idx} b{block} {signal}: no completion found, skipped")
            counts["not_found"] += 1
            continue

        candidates = [it for it in rec["result"]
                      if it.get("type") == "paragraphlabels"
                      and int(it["value"]["start"]) == block
                      and signal in it["value"].get("paragraphlabels", [])
                      and id(it) not in claimed[(project, conv, block, signal)]]
        if not candidates:
            print(f"  NOT FOUND  {rater} {r_idx} b{block} {signal:28} "
                  f"(already absent -- likely already correct)")
            counts["not_found"] += 1
            continue

        if action == "remove":
            target_n = remove_target_counts[(rater, r_idx, block, signal)]
            if target_n == 1:
                to_remove = candidates  # every matching occurrence goes
            else:
                q = re.sub(r'[^a-z0-9]+', '', quoted.lower())
                best = max(candidates,
                           key=lambda it: len(set(re.sub(r'[^a-z0-9]+', '', it["value"].get("text","").lower())) & set(q)))
                to_remove = [best]
                claimed[(project, conv, block, signal)].add(id(best))
                if len(candidates) > 1:
                    counts["ambiguous"] += 1
            for item in to_remove:
                item["value"]["paragraphlabels"].remove(signal)
                if not item["value"]["paragraphlabels"]:
                    rec["result"].remove(item)
                rec["dirty"] = True
                print(f"  - {rater} {r_idx} b{block:<4} {signal:28} removed  "
                      f"{item['value'].get('text','')[:60]!r}")
                counts["remove"] += 1
        elif action == "relabel":
            if len(candidates) > 1:
                q = re.sub(r'[^a-z0-9]+', '', quoted.lower())
                item = max(candidates,
                           key=lambda it: len(set(re.sub(r'[^a-z0-9]+', '', it["value"].get("text","").lower())) & set(q)))
                counts["ambiguous"] += 1
            else:
                item = candidates[0]
            labels = item["value"]["paragraphlabels"]
            labels[labels.index(signal)] = new_sig
            rec["dirty"] = True
            print(f"  ~ {rater} {r_idx} b{block:<4} {signal:28} -> {new_sig:28} "
                  f"{item['value'].get('text','')[:50]!r}")
            counts["relabel"] += 1

    touched = [r for r in store.values() if r["dirty"]]
    if apply_changes:
        for rec in touched:
            con.execute("""UPDATE task_completion SET result=?, updated_at=datetime('now')
                           WHERE id=?""",
                        (json.dumps(rec["result"], ensure_ascii=False), rec["completion"]))
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: "
          f"{counts['remove']} removed, {counts['relabel']} relabeled, "
          f"{counts['not_found']} not found (likely already correct), "
          f"{counts['ambiguous']} disambiguated by text match, "
          f"across {len(touched)} completion(s)")


# ----------------------------------------------------------------------------
# Mode 10: fix Priya's own confirmed role violations and one UI-glitch item
# (--fix-priya-role-violations). See module docstring / this session's quality review
# (Rubric_agree/round_2/priya/quality_and_disagreement_review.md).
# ----------------------------------------------------------------------------

FIX_PRIYA_ROLE_VIOLATIONS = {
    186: {  # task 759 (R3) -- ai_structured_response fired on code-role blocks;
            # rubric restricts this signal to blocks:['ai'] only.
        "AP4RQCHroU": "block 1  - role violation, ai_structured_response on code block",
        "u0HfOv9Eaf": "block 1  - role violation, ai_structured_response on code block",
        "p2KSxx9AAX": "block 7  - role violation, ai_structured_response on code block",
        "yQjZph6L9m": "block 12 - role violation, ai_structured_response on code block",
        "wkAXITKAC4": "block 15 - role violation, ai_structured_response on code block",
        "SYf5wf1day": "block 18 - role violation, ai_structured_response on code block",
        "qE5tu8e6uX": "block 21 - role violation, ai_structured_response on code block",
        "drEeWbL0Em": "block 24 - role violation, ai_structured_response on code block",
    },
    179: {  # task 762 (R6) -- same role violation.
        "zjeA0ymItB": "block 4 - role violation, ai_structured_response on code block",
        "HeK3saBwi9": "block 5 - role violation, ai_structured_response on code block",
    },
    # task 763 (R7): the earlier entry here removed item WN0upRQ-0F (ai_malfunction,
    # b1, offsets 25575-25717) as an "empty-text UI-selection glitch". That was WRONG
    # (reversed 2026-09-19): the offsets cover "subsubsection{Kernel Entry Points}..."
    # exactly as Priya's annotations_763.md row 1 describes -- a real label whose
    # `text` field simply failed to serialize on this >25K-char block, same as her b7
    # and b10 ai_malfunction items. Restored from the pre-import backup with text
    # filled from the offsets. Do NOT re-add it here.
}


def fix_priya_role_violations(apply_changes):
    con = sqlite3.connect(db_path())
    total_removed, touched = 0, 0

    for completion_id, targets in FIX_PRIYA_ROLE_VIOLATIONS.items():
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
# Mode 11: apply the round-2 ACCEPT-cell adjudication (--apply-round2-adjudication).
# Growable manifest -- appended to as each signal's batch gets ruled during the
# round-2 "get to zero disagreement" walk (see the plan). Each entry copies one
# rater's live span to the other rater's completion at the same block (same
# mechanism Mode 5 used for a single signal/direction, generalized to both
# directions and any signal) -- never hand-transcribed, always read live so the
# copied span's exact text/offsets match what the source rater actually has.
# ----------------------------------------------------------------------------

ROUND2_ADJUDICATION = [
    # (signal, r_index, block, from_rater, to_rater) -- "add signal at block to
    # to_rater's data, copying the span from_rater already has there"
    ("ai_validates_user", "R1", 14, "M", "A"),
    ("ai_validates_user", "R1", 20, "M", "A"),
    ("ai_validates_user", "R1", 22, "M", "A"),
    ("ai_validates_user", "R1", 24, "M", "A"),   # 2 items at this block, both copied
    ("ai_validates_user", "R4", 85, "M", "A"),
    ("ai_validates_user", "R4", 87, "M", "A"),
    ("ai_validates_user", "R5", 60, "M", "A"),
    # Correction: these 10 were marked "Jun's reading is final, no change" but that
    # never copied the final reading to Michelle's side, so the cell stayed disagreeing
    # in the data even though it was declared resolved. Same fix, reverse direction.
    ("ai_validates_user", "R4", 7, "A", "M"),
    ("ai_validates_user", "R4", 9, "A", "M"),
    ("ai_validates_user", "R4", 11, "A", "M"),
    ("ai_validates_user", "R4", 15, "A", "M"),
    ("ai_validates_user", "R4", 21, "A", "M"),
    ("ai_validates_user", "R4", 33, "A", "M"),
    ("ai_validates_user", "R4", 43, "A", "M"),
    ("ai_validates_user", "R4", 95, "A", "M"),
    ("ai_validates_user", "R4", 125, "A", "M"),
    ("ai_validates_user", "R4", 151, "A", "M"),
    # factual_error -- R3 (5 cells, "missed by Michelle") + R4 (4 cells, each an
    # explicit AI-identity claim confirmed by ACCEPT). R10 b7 stays HOLD (tax-law), exempt.
    ("factual_error", "R3", 4, "A", "M"),
    ("factual_error", "R3", 7, "A", "M"),
    ("factual_error", "R3", 12, "A", "M"),
    ("factual_error", "R3", 15, "A", "M"),
    ("factual_error", "R3", 18, "A", "M"),
    ("factual_error", "R4", 45, "A", "M"),
    ("factual_error", "R4", 49, "A", "M"),
    ("factual_error", "R4", 109, "A", "M"),
    ("factual_error", "R4", 173, "A", "M"),
    # false_confidence -- 10 cells, all ACCEPT with either "genuine miss" language or a
    # confirmed marker-word/vouch reading. R1 b16 + R6 b6: Michelle caught it, Jun didn't.
    # R1 b26, R2 b17, R3 b8/13/16, R4 b37/51/87: Jun caught it, Michelle didn't.
    ("false_confidence", "R1", 16, "M", "A"),
    ("false_confidence", "R6", 6, "M", "A"),
    ("false_confidence", "R1", 26, "A", "M"),
    ("false_confidence", "R2", 17, "A", "M"),
    ("false_confidence", "R3", 8, "A", "M"),
    ("false_confidence", "R3", 13, "A", "M"),
    ("false_confidence", "R3", 16, "A", "M"),
    ("false_confidence", "R4", 37, "A", "M"),
    ("false_confidence", "R4", 51, "A", "M"),
    ("false_confidence", "R4", 87, "A", "M"),
    # ai_asks_followup -- R4 b67/b101 deliberately SKIPPED (Michelle disputed these
    # directly, separate track, not adjudicated here).
    ("ai_asks_followup", "R3", 8, "A", "M"),
    ("ai_asks_followup", "R3", 25, "A", "M"),
    # R3 b5/b16 REMOVED from here (2026-09-19, during the ai_offered_options walk): both
    # already had ai_offered_options as the correct home for the same closing question
    # (b5 on Jun's side originally, b16 on Michelle's side originally) -- adding
    # ai_asks_followup here created a one-home-per-question violation. See the
    # ai_asks_followup cleanup entries further down.
    ("ai_asks_followup", "R4", 7, "M", "A"),
    ("ai_asks_followup", "R5", 35, "M", "A"),
    ("ai_asks_followup", "R7", 14, "A", "M"),
    # ai_asked_probing_question -- R4 b67/b101 SKIPPED, same disputed pair as
    # ai_asks_followup (Jun has probing there, Michelle has followup; she kept hers).
    # b7: Jun had BOTH probing and (now) followup on the same question -- one-home-per-
    # question violation created by the previous add; "Did they publish...?" is
    # yes/no-form so followup is the correct home, remove the stale probing label.
    ("ai_asked_probing_question", "R4", 7, None, "A"),
    ("ai_asked_probing_question", "R4", 41, "A", "M"),
    ("ai_asked_probing_question", "R4", 103, "M", "A"),
    ("ai_asked_probing_question", "R4", 127, "M", "A"),
    ("ai_asked_probing_question", "R4", 151, "A", "M"),
    ("ai_asked_probing_question", "R4", 153, "M", "A"),
    # ai_acknowledges_correction -- 6 cells, all ACCEPT, no dispute recorded
    ("ai_acknowledges_correction", "R3", 22, "M", "A"),
    ("ai_acknowledges_correction", "R4", 69, "A", "M"),
    ("ai_acknowledges_correction", "R4", 75, "A", "M"),
    ("ai_acknowledges_correction", "R5", 66, "A", "M"),
    ("ai_acknowledges_correction", "R5", 69, "A", "M"),
    ("ai_acknowledges_correction", "R9", 6, "A", "M"),
    # adaptation -- 5 cells. R3 b25: Michelle's PDF-described self-correction (span
    # moved to the completed-change sentence) is confirmed valid -- copy to Jun, whose
    # copy is still the old invalid prospective-only span.
    ("adaptation", "R2", 17, "M", "A"),
    ("adaptation", "R2", 32, "A", "M"),
    ("adaptation", "R3", 25, "M", "A"),
    ("adaptation", "R4", 111, "A", "M"),
    ("adaptation", "R7", 14, "A", "M"),
    # ai_asserts_knowledge_limit -- R9 b2 SKIPPED, the 4th Michelle-disputed cell
    # (already in EXCLUDED_ROUND2_ACTIONS, correctly never removed).
    ("ai_asserts_knowledge_limit", "R4", 27, "A", "M"),
    ("ai_asserts_knowledge_limit", "R4", 33, "A", "M"),
    ("ai_asserts_knowledge_limit", "R4", 43, "M", "A"),
    ("ai_asserts_knowledge_limit", "R4", 109, "A", "M"),
    # ai_hedges_uncertainty -- 5 cells, all ACCEPT, Jun fires/Michelle absent throughout
    ("ai_hedges_uncertainty", "R1", 1, "A", "M"),
    ("ai_hedges_uncertainty", "R1", 12, "A", "M"),
    ("ai_hedges_uncertainty", "R4", 5, "A", "M"),   # 2 items at this block
    ("ai_hedges_uncertainty", "R4", 23, "A", "M"),
    ("ai_hedges_uncertainty", "R5", 32, "A", "M"),
    # ethical_tension -- 5 cells, Jun fires/Michelle absent throughout. R9 b2 is the
    # confirmed ai_provides_caveats->ethical_tension relabel from the round-2 write-back.
    ("ethical_tension", "R4", 0, "A", "M"),
    ("ethical_tension", "R4", 51, "A", "M"),
    ("ethical_tension", "R4", 52, "A", "M"),
    ("ethical_tension", "R9", 2, "A", "M"),
    ("ethical_tension", "R9", 6, "A", "M"),
    # ai_references_prior_turn -- 4 cells, all ACCEPT, Jun fires/Michelle absent
    # throughout. R5 b72's span itself needs correcting first (see
    # fix_r5_b72_span_and_copy below) -- handled separately, not through this list.
    ("ai_references_prior_turn", "R4", 97, "A", "M"),
    ("ai_references_prior_turn", "R5", 32, "A", "M"),
    ("ai_references_prior_turn", "R5", 60, "A", "M"),
    # under_delivered -- 4 cells, all ACCEPT, Jun fires/Michelle absent throughout.
    # Draft flags all 4 whole-block spans (24K-99K chars) as candidates to narrow to the
    # bulletpoint-heavy portions "for the correction pass, separate from the fire/no-fire
    # ruling" -- unlike R5 b72's ai_references_prior_turn fix, this is a precision
    # refinement (the whole-block span already correctly contains the violation), not a
    # wrong-location error, and picking exact sub-spans is a real judgment call left
    # open/deferred, not auto-corrected here.
    ("under_delivered", "R7", 1, "A", "M"),
    ("under_delivered", "R7", 4, "A", "M"),
    ("under_delivered", "R7", 7, "A", "M"),
    ("under_delivered", "R7", 10, "A", "M"),
    # user_implicit_correction -- 4 cells, all ACCEPT (the 3 CORRECT-A cells from the
    # draft's 7-cell section were already removed in the round-2 write-back).
    ("user_implicit_correction", "R1", 15, "M", "A"),
    ("user_implicit_correction", "R3", 20, "M", "A"),
    ("user_implicit_correction", "R4", 58, "M", "A"),
    ("user_implicit_correction", "R4", 68, "A", "M"),
    # ai_provides_caveats -- 3 cells, all ACCEPT (the other 3 cells from the draft's
    # 6-cell section -- R1 b7 dropped, R1 b14 relabeled ai_warns_user, R9 b2 relabeled
    # ethical_tension -- were already applied in the round-2 write-back).
    ("ai_provides_caveats", "R1", 3, "M", "A"),
    ("ai_provides_caveats", "R1", 30, "A", "M"),
    ("ai_provides_caveats", "R2", 2, "A", "M"),
    # ai_provides_step_by_step -- 3 cells, all ACCEPT
    ("ai_provides_step_by_step", "R1", 1, "M", "A"),
    ("ai_provides_step_by_step", "R1", 30, "M", "A"),
    ("ai_provides_step_by_step", "R8", 2, "A", "M"),
    # user_asks_clarification -- 3 cells, all ACCEPT (b64, also ACCEPT in the draft,
    # already agrees live; the other 4 draft cells were CORRECT-A/relabel, already
    # applied in the round-2 write-back).
    ("user_asks_clarification", "R4", 32, "M", "A"),
    ("user_asks_clarification", "R4", 38, "A", "M"),
    ("user_asks_clarification", "R4", 40, "A", "M"),
    # user_corrects_ai -- 3 cells, all ACCEPT (the other 3 draft cells were CORRECT-A
    # redundant-duplicates of user_implicit_correction, already applied in the write-back)
    ("user_corrects_ai", "R3", 23, "A", "M"),
    ("user_corrects_ai", "R4", 8, "A", "M"),
    ("user_corrects_ai", "R5", 61, "A", "M"),
    # user_empowered -- 3 cells, all ACCEPT
    ("user_empowered", "R2", 5, "A", "M"),
    ("user_empowered", "R5", 23, "A", "M"),
    ("user_empowered", "R8", 2, "A", "M"),
    # user_multi_request -- 3 cells, all ACCEPT (the other 2 draft cells, R2 b0 and
    # R4 b64, were CORRECT-M, already applied in the round-2 write-back).
    ("user_multi_request", "R4", 56, "M", "A"),
    ("user_multi_request", "R10", 4, "M", "A"),
    ("user_multi_request", "R10", 8, "M", "A"),
    # user_validation_seeking -- 3 cells, all ACCEPT. R4 b50 isn't in this signal's own
    # draft section (which only covers R1/R5) -- it's the relabel target from
    # ai_provides_caveats/user_asks_clarification's b50 ruling ("relabel to
    # user_validation_seeking"), already applied to Michelle's data in the write-back;
    # same ACCEPT shape as the other two, just needs adding to Jun's side too.
    ("user_validation_seeking", "R1", 4, "M", "A"),
    ("user_validation_seeking", "R4", 50, "M", "A"),
    ("user_validation_seeking", "R5", 61, "M", "A"),
    # ai_structured_response -- 2 cells, both ACCEPT, "genuine misses in opposite directions"
    ("ai_structured_response", "R1", 1, "A", "M"),
    ("ai_structured_response", "R1", 10, "M", "A"),
    # ai_warns_user -- 2 cells, both ACCEPT (R1 b14 already agrees live via the
    # ai_provides_caveats relabel; R5 b72 was CORRECT-M, already applied).
    ("ai_warns_user", "R1", 12, "M", "A"),   # 2 items at this block, both copied
    ("ai_warns_user", "R1", 26, "M", "A"),
    # ai_provides_example -- 2 cells, both ACCEPT (R5's 3 ACCEPT cells already agree
    # live; R5 b2 and R9 b6 were CORRECT-M, already applied).
    ("ai_provides_example", "R8", 2, "A", "M"),
    ("ai_provides_example", "R10", 5, "M", "A"),
    # ai_offered_options -- R3 b5 undocumented in the draft (only b13/b16/b25 + R8 b2
    # were), but same "X or Y" named-action-choice shape as the ACCEPTed b16. Checking
    # both blocks' full label sets surfaced two one-home-per-question violations:
    # (1) Jun's b5 already had BOTH ai_offered_options (his own, correct) and
    #     ai_asks_followup -- the latter was wrongly added there during the earlier
    #     ai_asks_followup walk ("R3 b5: undocumented, same shape (yes/no closer)")
    #     without checking Jun already had the more specific label. Remove it.
    # (2) Michelle's b16 already had BOTH ai_offered_options (her own, pre-existing,
    #     unrelated to any adjudication) and ai_asks_followup, same violation,
    #     independent of my earlier walk. Remove it.
    ("ai_asks_followup", "R3", 5, None, "A"),   # one-home-per-question cleanup
    ("ai_asks_followup", "R3", 16, None, "M"),  # one-home-per-question cleanup
    ("ai_asks_followup", "R3", 5, None, "M"),   # same cleanup, other side
    ("ai_asks_followup", "R3", 16, None, "A"),  # same cleanup, other side
    ("ai_offered_options", "R3", 5, "A", "M"),
    ("ai_offered_options", "R3", 16, "M", "A"),
    # ai_missing_retrieval -- 2 cells, both ACCEPT, Jun fires/Michelle absent
    ("ai_missing_retrieval", "R3", 1, "A", "M"),
    ("ai_missing_retrieval", "R3", 4, "A", "M"),
    # ai_cites_source -- 2 cells, both ACCEPT, Michelle fires/Jun absent (the other 5
    # draft cells at R5 were mostly CORRECT-M, subject-vs-source; the 1 ACCEPT span
    # there, b38 span 3, already agrees live)
    ("ai_cites_source", "R1", 28, "M", "A"),
    ("ai_cites_source", "R10", 5, "M", "A"),
    # conversation_stalled -- 2 cells, both ACCEPT. R3 b8 on Jun's side also had a
    # 4-char span-drift artifact (text "with", offsets 396-400 -- a corrupted leftover
    # fragment, not a genuine second instance) removed directly, outside this list.
    ("conversation_stalled", "R3", 8, "A", "M"),
    ("conversation_stalled", "R3", 16, "A", "M"),
    # 7 single-cell signals, all ACCEPT, Jun fires/Michelle absent throughout
    ("user_repeats_request", "R3", 14, "A", "M"),
    ("user_positive_feedback", "R4", 46, "A", "M"),
    ("user_ambiguous_request", "R2", 21, "A", "M"),
    ("problem_ignored", "R2", 11, "A", "M"),
    ("off_topic_drift", "R5", 57, "A", "M"),
    ("ai_provides_alternatives", "R2", 5, "A", "M"),
    ("ai_malfunction", "R7", 7, "A", "M"),
    ("ai_flags_complexity", "R4", 61, "A", "M"),
    # ai_offers_to_elaborate R3 b2 deliberately SKIPPED -- this is the flagged Type-2
    # reclassification cell (Jun: ai_offers_to_elaborate, Michelle: ai_offered_options,
    # same question), not a simple miss; needs the three-way Type-2 pass, not a
    # mechanical copy that would just create a double-fire.
]


def apply_round2_adjudication(apply_changes):
    conv_to_c = {r["c_index"]: r["conv_id"] for r in
                 csv.DictReader(l for l in open(ROUND2_CONV_MAP_PATH) if not l.startswith("#"))}
    con = sqlite3.connect(db_path())

    store = {}
    for pid in set(RATER_PROJECT_ROUND2.values()):
        for tid, data, res_raw, cid in con.execute(
                """SELECT t.id, t.data, tc.result, tc.id FROM task_completion tc
                   JOIN task t ON t.id = tc.task_id
                   WHERE tc.was_cancelled = 0 AND t.project_id = ?""", (pid,)):
            conv = json.loads(data).get("conv_id")
            store[(pid, conv)] = {"task": tid, "completion": cid,
                                   "result": json.loads(res_raw), "dirty": False}

    added, skipped, removed = 0, 0, 0
    for signal, r_idx, block, from_rater, to_rater in ROUND2_ADJUDICATION:
        conv = conv_to_c[r_idx]
        dst = store[(RATER_PROJECT_ROUND2[to_rater], conv)]

        if from_rater is None:
            # pure removal -- e.g. a stale question-family label superseded by
            # another signal already added at the same block (one-home-per-question)
            targets = [it for it in dst["result"]
                       if it.get("type") == "paragraphlabels" and int(it["value"]["start"]) == block
                       and signal in it["value"].get("paragraphlabels", [])]
            if not targets:
                print(f"  SKIP  remove {to_rater} {r_idx} b{block} {signal}: already absent")
                skipped += 1
                continue
            for item in targets:
                item["value"]["paragraphlabels"].remove(signal)
                if not item["value"]["paragraphlabels"]:
                    dst["result"].remove(item)
                dst["dirty"] = True
                print(f"  - remove {to_rater} {r_idx} b{block:<4} {signal:28} "
                      f"{item['value'].get('text','')[:60]!r}")
                removed += 1
            continue

        src = store[(RATER_PROJECT_ROUND2[from_rater], conv)]
        src_items = [it for it in src["result"]
                     if it.get("type") == "paragraphlabels" and int(it["value"]["start"]) == block
                     and signal in it["value"].get("paragraphlabels", [])]
        if not src_items:
            print(f"  WARNING {from_rater}->{to_rater} {r_idx} b{block} {signal}: "
                  f"not found in {from_rater}'s live data, skipped")
            continue
        already = any(it.get("type") == "paragraphlabels" and int(it["value"]["start"]) == block
                       and signal in it["value"].get("paragraphlabels", []) for it in dst["result"])
        if already:
            print(f"  SKIP  {from_rater}->{to_rater} {r_idx} b{block} {signal}: "
                  f"already present on {to_rater}'s side")
            skipped += 1
            continue

        for n, src_it in enumerate(src_items):
            v = src_it["value"]
            new_item = {
                "value": {"start": v["start"], "end": v["end"],
                          "startOffset": v["startOffset"], "endOffset": v["endOffset"],
                          "text": v["text"], "paragraphlabels": [signal]},
                "id": _new_id(RATER_PROJECT_ROUND2[to_rater], f"{r_idx}-adj-{n}", block, signal),
                "from_name": "signals", "to_name": "dialogue",
                "type": "paragraphlabels", "origin": "manual",
            }
            dst["result"].append(new_item)
            dst["dirty"] = True
            print(f"  + {from_rater}->{to_rater} {r_idx} b{block:<4} {signal:28} "
                  f"(from {from_rater}'s span) {v['text'][:60]!r}")
            added += 1

    touched = [r for r in store.values() if r["dirty"]]
    if apply_changes:
        for rec in touched:
            con.execute("""UPDATE task_completion SET result=?, updated_at=datetime('now')
                           WHERE id=?""",
                        (json.dumps(rec["result"], ensure_ascii=False), rec["completion"]))
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: {added} label(s) added, "
          f"{removed} removed, {skipped} already present/absent, across "
          f"{len(touched)} completion(s)")


# ----------------------------------------------------------------------------
# Mode 12: round-1 (Jun "A" / B / F) three-way batch-by-signal adjudication
# (--apply-round1-adjudication). Same shape as Mode 11, generalized to N raters:
# each entry copies one rater's live span for (signal, block) to one or more
# other raters, or removes a stale label when from_rater is None.
# ----------------------------------------------------------------------------

ROUND1_CONV_MAP_PATH = ANNOT_DIR / "agreement_set_convid_map.csv"
RATER_PROJECT_ROUND1 = {"A": 1, "B": 2, "F": 3}

ROUND1_ADJUDICATION = [
    # (signal, c_index, block, from_rater, to_raters) -- to_raters is a tuple; copies
    # from_rater's live span at (c_index, block, signal) to each rater in to_raters.
    # from_rater=None + a single to_rater in the tuple means pure removal.
]


# ----------------------------------------------------------------------------
# Mode 13: Priya three-way adjudication (--apply-priya-adjudication). Same list
# shape as Mode 12 (to_raters is a tuple), raters A/M/P = projects 1/5/4, keyed
# by R-index over the round-2 conv map. Shares the N-way engine with Mode 12.
# ----------------------------------------------------------------------------

RATER_PROJECT_PRIYA = {"A": 1, "M": 5, "P": 4}

PRIYA_ADJUDICATION = [
    # (signal, r_index, block, from_rater, to_raters) -- see ROUND1_ADJUDICATION.
    # ai_structured_response -- 40 cells, ruled by Jun 2026-09-19 on the signal
    # DEFINITION + block_notes (visible formatting markers only). Fires: dash-delimited
    # "Name - description" lists ("-" is a visible marker) and the "1." numbered list;
    # bare line-separated items, colon labels and bare title-case lines are 0.
    ("ai_structured_response", "R1", 7, "P", ("A", "M")),
    ("ai_structured_response", "R3", 5, "P", ("A", "M")),
    ("ai_structured_response", "R5", 23, "P", ("A", "M")),
    ("ai_structured_response", "R1", 30, "A", ("P",)),
] + [
    ("ai_structured_response", r, b, None, ("P",)) for r, b in [
        ("R1", 3), ("R2", 2), ("R2", 8), ("R2", 14), ("R2", 20), ("R2", 23), ("R2", 26),
        ("R3", 2), ("R3", 8), ("R3", 13), ("R3", 25), ("R4", 169),
        ("R5", 2), ("R5", 5), ("R5", 8), ("R5", 11), ("R5", 14), ("R5", 17), ("R5", 20),
        ("R5", 26), ("R5", 38), ("R5", 41), ("R5", 44), ("R5", 47), ("R5", 50), ("R5", 53),
        ("R5", 57), ("R5", 72), ("R7", 14), ("R9", 2), ("R9", 6),
        ("R10", 1), ("R10", 3), ("R10", 5), ("R10", 7), ("R10", 9),
    ]
] + [
    # ai_validates_user -- 29 cells, ruled by Jun 2026-09-19. 28 are round-2 ACCEPT
    # cells (bare-agreement opener answering a recoverable user position, R20/R21, plus
    # explicit affirmations of the user) that Priya never fires -> add to P. R4 b7/b91/
    # b107 confirmed as validation, NOT acknowledgment: her ai_acknowledges_correction
    # fires there come off when that signal is walked.
    ("ai_validates_user", r, b, "A", ("P",)) for r, b in [
        ("R1", 24), ("R4", 7), ("R4", 11), ("R4", 23), ("R4", 31), ("R4", 33), ("R4", 35),
        ("R4", 43), ("R4", 45), ("R4", 55), ("R4", 61), ("R4", 85), ("R4", 87), ("R4", 91),
        ("R4", 93), ("R4", 95), ("R4", 97), ("R4", 105), ("R4", 107), ("R4", 123),
        ("R4", 125), ("R4", 137), ("R4", 139), ("R4", 151), ("R4", 153),
        ("R5", 32), ("R5", 60), ("R5", 69),
    ]
] + [
    # R3 b25: the AI describing its own change ("Removed X's immunity since his passive
    # is already impactful") -- Step 1 fails, nothing about the user is affirmed.
    ("ai_validates_user", "R3", 25, None, ("P",)),
] + [
    # ai_hedges_uncertainty -- 26 cells, ruled by Jun 2026-09-19. Fires only on a
    # genuine downgrade of confidence in a claim the AI is making (likely/probably/
    # might). Jun's ruling on the keyword list: "If" and "Maybe" are ASSUMPTIONS, not
    # hedges -- a conditional premise and a floated possibility assert nothing to
    # downgrade, so Step 2's "IF...THEN" keyword does not fire on its own (the gate is
    # the question, the keywords only prompt the check).
    ("ai_hedges_uncertainty", "R1", 1, "A", ("P",)),
    ("ai_hedges_uncertainty", "R1", 12, "A", ("P",)),
    ("ai_hedges_uncertainty", "R4", 5, "A", ("P",)),
    ("ai_hedges_uncertainty", "R4", 23, "A", ("P",)),
    # Priya right -- "probably"/"might" on the AI's own claim, both missed by A and M
    ("ai_hedges_uncertainty", "R4", 13, "P", ("A", "M")),
    ("ai_hedges_uncertainty", "R4", 29, "P", ("A", "M")),
    ("ai_hedges_uncertainty", "R4", 31, "P", ("A", "M")),
    ("ai_hedges_uncertainty", "R4", 35, "P", ("A", "M")),
    ("ai_hedges_uncertainty", "R4", 167, "P", ("A", "M")),  # span 2 dropped separately
    # Step 3: no answer, states inability -> ai_asserts_knowledge_limit is the home
    ("ai_hedges_uncertainty", "R4", 27, None, ("P",)),
    ("ai_asserts_knowledge_limit", "R4", 27, "A", ("P",)),
    ("ai_hedges_uncertainty", "R4", 33, None, ("P",)),
    ("ai_asserts_knowledge_limit", "R4", 33, "A", ("P",)),
] + [
    # no downgrade of an AI claim: approximations, reportive "suggests", firm "I think",
    # inference "must be", a felt state, a conditional premise (b37), floated
    # possibilities (b59), a scoping phrase (R9 b6), qualifying the USER's claim (b3)
    ("ai_hedges_uncertainty", r, b, None, ("P",)) for r, b in [
        ("R2", 4), ("R2", 16), ("R4", 3), ("R4", 37), ("R4", 39), ("R4", 55),
        ("R4", 59), ("R4", 75), ("R4", 105), ("R4", 111), ("R5", 72), ("R9", 6),
        ("R10", 1), ("R10", 5),
    ]
    # R9 b2 HELD: the Michelle-disputed cell (A: ethical_tension, M: also
    # ai_asserts_knowledge_limit, P: hedge)
] + [
    # false_confidence -- 16 cells, ruled by Jun 2026-09-19. Gate: an absolute/certainty
    # marker vouching a NOVEL claim. The AI's own false self-claim routes to
    # factual_error (claim-ownership), which is where R4 b45/b115/b161 and R5 b69 go --
    # the factual_error spans at b115/b161/b69 were created on all three raters first
    # (no rater had them), then the false_confidence fires come off Priya here.
    ("false_confidence", "R1", 18, "A", ("P",)),
    ("false_confidence", "R1", 20, "A", ("P",)),
    ("false_confidence", "R2", 17, "A", ("P",)),
    ("false_confidence", "R3", 8, "A", ("P",)),
    ("false_confidence", "R3", 13, "A", ("P",)),
    ("false_confidence", "R4", 37, "A", ("P",)),
    ("false_confidence", "R4", 51, "A", ("P",)),
    ("false_confidence", "R4", 87, "A", ("P",)),
    ("false_confidence", "R6", 6, "A", ("P",)),
    # AI self-claims -> factual_error
    ("false_confidence", "R4", 45, None, ("P",)),
    ("factual_error", "R4", 45, "A", ("P",)),
    ("false_confidence", "R4", 115, None, ("P",)),
    ("false_confidence", "R4", 161, None, ("P",)),
    ("false_confidence", "R5", 69, None, ("P",)),   # also drops her 2nd span there
    # not a vouched novel claim
    ("false_confidence", "R1", 14, None, ("P",)),
    ("false_confidence", "R4", 11, None, ("P",)),
    ("false_confidence", "R4", 47, None, ("P",)),
] + [
    # ai_provides_caveats -- 15 cells, all Priya-only, ruled by Jun 2026-09-19.
    # A caveat flags a LIMITATION, RISK or SHORTCOMING of what the AI is offering.
    # R9 b6 is the span already ruled ethical_tension in round 2 -> relabel.
    ("ai_provides_caveats", "R9", 6, None, ("P",)),
    ("ethical_tension", "R9", 6, "A", ("P",)),
] + [
    # R1 b1: a directive about care = a risk the user acts on, same shape as the round-2
    # R1 b14 relabel to ai_warns_user (which all three already carry on that block).
    # R2 b5: describes how the substitute behaves = part of ai_provides_alternatives.
    # The rest qualify analytical claims, not recommendations (Step 1).
    ("ai_provides_caveats", r, b, None, ("P",)) for r, b in [
        ("R1", 1), ("R2", 5), ("R2", 11), ("R2", 29), ("R5", 11), ("R5", 20),
        ("R5", 26), ("R5", 47), ("R5", 50), ("R5", 57), ("R8", 2),
        ("R10", 3), ("R10", 5), ("R10", 7),
    ]
] + [
    # factual_error -- 10 cells, ruled by Jun 2026-09-19.
    # R3's five are checkable skill data (wrong against the site the user supplied);
    # R4 b49/b109/b173 fire on Step 3 (AI identity claim).
    ("factual_error", "R3", 4, "A", ("P",)),
    ("factual_error", "R3", 7, "A", ("P",)),
    ("factual_error", "R3", 12, "A", ("P",)),
    ("factual_error", "R3", 15, "A", ("P",)),
    ("factual_error", "R3", 18, "A", ("P",)),
    ("factual_error", "R4", 49, "A", ("P",)),
    ("factual_error", "R4", 109, "A", ("P",)),
    ("factual_error", "R4", 173, "A", ("P",)),
    # R4 b89 "learn from conversations" -- NOT verifiable: true of in-context learning,
    # false only under the cross-session reading the user imposes at b90. b90-b91 is the
    # user narrowing a loose phrase and the AI accepting it, not a fact being falsified.
    # A capability characterization, not a quote- or count-level claim (Step 2b) -> 0.
    ("factual_error", "R4", 89, None, ("P",)),
    # R10 b7 HELD: turns on whether corporate lobbying is deductible (IRC 162(e));
    # unverified since round 2. Jun-only fire.
] + [
    # ---- correction family (ack / implicit / corrects / adaptation), ruled together
    # by Jun 2026-09-19 because four R2/R4 turn-pairs decide rows across all four.
    #
    # THE PAIRS. ack Step 1 needs the prior human turn to name a factual, technical or
    # framing ERROR in the AI's output; pushback about style/behaviour is NOT a
    # correction. Checking the AI turn BEFORE each user turn splits them:
    #  b5  inferred "the default is to follow organizational hierarchy" -> b6 "No -"
    #      corrects that framing -> b7 accepts it  => ack (AVU off, R21)
    #  b89 claimed "learn from conversations" -> b90 negates it -> b91 "No." concedes
    #      => ack (AVU off, R21)
    #  b105 asserted nothing wrong -> b106 observes the AI's responses are all the same
    #      length = behaviour critique, NOT a correction => ack does NOT fire; the
    #      block stays ai_validates_user on all three.
    # No block ends double-labelled: R21 forbids AVU inside an ack span.
    ("user_implicit_correction", "R4", 6, "P", ("A", "M")),
    ("ai_acknowledges_correction", "R4", 7, "P", ("A", "M")),
    ("ai_validates_user", "R4", 7, None, ("A", "M", "P")),
    ("user_corrects_ai", "R4", 90, "P", ("A", "M")),
    ("ai_acknowledges_correction", "R4", 91, "P", ("A", "M")),
    ("ai_validates_user", "R4", 91, None, ("A", "M", "P")),
    ("ai_acknowledges_correction", "R4", 107, None, ("P",)),
    # settled A+M cells Priya missed
    ("ai_acknowledges_correction", "R3", 10, "A", ("P",)),
    ("ai_acknowledges_correction", "R4", 69, "A", ("P",)),
    ("user_implicit_correction", "R3", 17, "A", ("P",)),
    ("user_implicit_correction", "R3", 20, "A", ("P",)),
    ("user_implicit_correction", "R4", 58, "A", ("P",)),
    ("user_implicit_correction", "R4", 68, "A", ("P",)),
    ("user_corrects_ai", "R4", 8, "A", ("P",)),
    ("user_corrects_ai", "R4", 72, "A", ("P",)),
    ("adaptation", "R2", 17, "A", ("P",)),
    ("adaptation", "R2", 32, "A", ("P",)),
    ("adaptation", "R4", 111, "A", ("P",)),
    ("adaptation", "R7", 14, "A", ("P",)),
    # relabels on P (the paired label is added above or already present)
    ("ai_acknowledges_correction", "R3", 13, None, ("P",)),   # -> false_confidence (already has)
    ("ai_acknowledges_correction", "R3", 25, None, ("P",)),   # -> adaptation (already has)
    ("ai_acknowledges_correction", "R7", 14, None, ("P",)),   # -> adaptation (added above)
    ("ai_acknowledges_correction", "R2", 32, None, ("P",)),   # -> adaptation (added above)
    ("user_corrects_ai", "R3", 17, None, ("P",)),             # -> implicit (added above)
    ("user_corrects_ai", "R3", 20, None, ("P",)),             # -> implicit (added above)
    ("user_corrects_ai", "R4", 58, None, ("P",)),             # -> implicit (added above)
    ("adaptation", "R4", 109, None, ("P",)),                  # -> knowledge_limit (its own walk)
    # clean removals: nobody labels the block, or the act is not in this family
    ("user_implicit_correction", "R4", 104, None, ("P",)),
    ("user_implicit_correction", "R9", 3, None, ("P",)),
    ("adaptation", "R2", 26, None, ("P",)),
    ("user_corrects_ai", "R7", 12, None, ("P",)),
    ("ai_acknowledges_correction", "R5", 57, None, ("P",)),   # needs example + off_topic_drift, own walks
    # R2 b30: NOT held. Jun 2026-09-19 -- the merge question is about
    # frustration/dissatisfaction; whether user_implicit_correction fires here is
    # independent of it, and it is already settled by consistency with b32 being ruled
    # adaptation (not ack) because b30 is a presentation preference, not a correction.
    # The A-vs-M dissatisfaction/frustration split at this block stays held in THOSE
    # signals.
    ("user_implicit_correction", "R2", 30, None, ("P",)),
    # judgment calls, agreed by Jun
    ("user_corrects_ai", "R5", 64, "P", ("A", "M")),   # names the concrete defect
    ("adaptation", "R4", 167, "P", ("A", "M")),        # "I changed my mind." -- stated reversal
] + [
    # ai_provides_example -- 9 cells, ruled by Jun 2026-09-19. A concrete SCENARIO or
    # NAMED CASE illustrating the point fires; a category list inside an argument does
    # not. Comparator: R5 b23, where all three already agree ("Fashion brands making
    # millions from traditional designs...", "Halloween costumes that caricature...").
    ("ai_provides_example", "R5", 57, "A", ("P",)),
    ("ai_provides_example", "R8", 2, "A", ("P",)),
    ("ai_provides_example", "R10", 5, "A", ("P",)),
    # Priya right: actual scenarios ("a leak behind a wall", "modern fixtures in a
    # century-old building"). Same shape as b23/b26, ruled ACCEPT in round 2.
    ("ai_provides_example", "R5", 53, "P", ("A", "M")),
    # R5 b14 REVERSES the round-2 ACCEPT: the block is an argument listing profession
    # CATEGORIES ("electricians, nurses, software developers"), no case is rendered.
    # The round-2 "a profession category is concrete enough" rule over-reached; it only
    # ever lived in round2_disagreement_draft.md, never in the frozen rubric.
    ("ai_provides_example", "R5", 14, None, ("P",)),
    ("ai_provides_example", "R5", 2, None, ("P",)),    # round 2: topic labels, no worked instance
    ("ai_provides_example", "R4", 57, None, ("P",)),   # analogy stating a condition
    ("ai_provides_example", "R5", 35, None, ("P",)),   # self-reflection, illustrates nothing
    ("ai_provides_example", "R10", 1, None, ("P",)),   # restates the same figure, contextualisation
    # R5 b26 restored to all three outside this list (no rater had it; Michelle's
    # original span 922-1128 recovered from bak-2026-09-14-pre-michelle-round2-fix).
] + [
    # ---- batch of 7 signals, ruled by Jun 2026-09-19 ----
    # settled A+M cells Priya missed
    ("user_asks_clarification", "R4", 32, "A", ("P",)),
    ("user_asks_clarification", "R4", 38, "A", ("P",)),
    ("user_asks_clarification", "R4", 40, "A", ("P",)),
    ("user_asks_clarification", "R4", 64, "A", ("P",)),
    ("ethical_tension", "R4", 0, "A", ("P",)),
    ("ethical_tension", "R4", 51, "A", ("P",)),
    ("ethical_tension", "R4", 52, "A", ("P",)),
    ("ethical_tension", "R9", 2, "A", ("P",)),
    ("ai_references_prior_turn", "R4", 97, "A", ("P",)),
    ("ai_references_prior_turn", "R5", 32, "A", ("P",)),
    ("ai_references_prior_turn", "R5", 60, "A", ("P",)),
    ("ai_references_prior_turn", "R5", 72, "A", ("P",)),
    ("ai_asserts_knowledge_limit", "R4", 43, "A", ("P",)),
    ("ai_asserts_knowledge_limit", "R4", 109, "A", ("P",)),
    ("user_multi_request", "R4", 56, "A", ("P",)),
    ("user_multi_request", "R10", 8, "A", ("P",)),
    # ai_offered_options: A6 one home -- add the A/M home, drop Priya's probing on the
    # same question. Independent of the followup/probing merge, so decidable now; this
    # also clears 4 of the 29 held ai_asked_probing_question cells.
    ("ai_offered_options", "R3", 2, "A", ("P",)),
    ("ai_offered_options", "R3", 5, "A", ("P",)),
    ("ai_offered_options", "R3", 16, "A", ("P",)),
    ("ai_offered_options", "R8", 2, "A", ("P",)),
    ("ai_asked_probing_question", "R3", 2, None, ("P",)),
    ("ai_asked_probing_question", "R3", 5, None, ("P",)),
    ("ai_asked_probing_question", "R3", 16, None, ("P",)),
    ("ai_asked_probing_question", "R8", 2, None, ("P",)),
    # Priya right, A+M both missed: two independently fulfillable asks
    ("user_multi_request", "R1", 17, "P", ("A", "M")),
    ("user_multi_request", "R3", 23, "P", ("A", "M")),
    # removals from P
    ("ai_references_prior_turn", "R4", 93, None, ("P",)),  # prospective wish, no callback marker
    ("ai_asserts_knowledge_limit", "R3", 10, None, ("P",)),# a plan, not an inability
    ("user_multi_request", "R10", 2, None, ("P",)),        # "and if so" -- conditional on the first
    ("user_multi_request", "R1", 23, None, ("P",)),        # "do I need a solicitor?" is a sub-question
                                                            # of the same deliverable (Step 2)
    ("user_repeats_request", "R3", 9, None, ("P",)),       # the FIRST ask; b14 is its repeat
    ("user_repeats_request", "R3", 17, None, ("P",)),      # supplying data = implicit correction
    ("user_repeats_request", "R3", 20, None, ("P",)),
    ("user_repeats_request", "R7", 12, None, ("P",)),      # b9 "continue" was SERVED but wrong ->
                                                            # Step 2 routes away from repeat; and
                                                            # round 2 ruled it not a correction either
    # ai_asserts_knowledge_limit R9 b2 HELD (Michelle-disputed).
] + [
    # The question family splits three ways; only the ROUTING cells are blocked by the
    # followup/probing merge. These are the pure misses -- A+M fire, Priya has nothing
    # at the block -- so whatever the merged signal ends up called, she missed them.
    ("ai_asked_probing_question", "R4", b, "A", ("P",)) for b in
    [5, 25, 41, 53, 83, 103, 119, 121, 125, 127, 133, 143, 145, 147, 151, 153]
] + [
    ("ai_asks_followup", "R3", 25, "A", ("P",)),
    ("ai_asks_followup", "R5", 60, "A", ("P",)),
    # STILL HELD, pending the merge: the 8 routing pairs (Priya fires probing where A+M
    # fire followup) at R3 b8/b13/b19/b22, R4 b7, R5 b35, R7 b14, R10 b1 -- 16 cells
    # across the two signals. Plus R4 b67/b101, Michelle-disputed, in both.
] + [
    # ---- final batch 1 (17 cells), ruled by Jun 2026-09-19 ----
    # settled A+M cells Priya missed
    ("user_validation_seeking", "R4", 36, "A", ("P",)),
    ("user_validation_seeking", "R4", 50, "A", ("P",)),
    ("user_validation_seeking", "R5", 61, "A", ("P",)),
    ("user_empowered", "R2", 5, "A", ("P",)),
    ("user_empowered", "R5", 23, "A", ("P",)),
    ("user_empowered", "R8", 2, "A", ("P",)),
    ("conversation_stalled", "R3", 8, "A", ("P",)),
    ("conversation_stalled", "R3", 16, "A", ("P",)),
    ("user_positive_feedback", "R4", 46, "A", ("P",)),
    ("ai_warns_user", "R1", 26, "A", ("P",)),
    # Priya right, both missed
    ("user_positive_feedback", "R4", 94, "P", ("A", "M")),  # "you got there on your own this time."
    # removals -- each fails the signal's own gate
    ("ai_warns_user", "R1", 18, None, ("P",)),          # case-building advice, no hazard (Step 1)
    ("ai_warns_user", "R1", 22, None, ("P",)),          # imperative list, no adverse consequence
    ("appropriate_confidence", "R1", 28, None, ("P",)), # Step 1 complexity gate: a lookup question
    ("appropriate_confidence", "R4", 73, None, ("P",)), # same -- plain self-report, nothing contested
    ("ai_provides_alternatives", "R5", 14, None, ("P",)),# a claim, not something offered INSTEAD
    ("ai_provides_alternatives", "R8", 2, None, ("P",)), # Step 2: an item in a list of suggestions is
                                                          # not an alternative; A+M home it as
                                                          # ai_offered_options
] + [
    # ---- final batch 2 (11 cells), ruled by Jun 2026-09-19 ----
    ("ai_missing_retrieval", "R3", 1, "A", ("P",)),
    ("ai_missing_retrieval", "R3", 4, "A", ("P",)),
    ("ai_cites_source", "R1", 28, "A", ("P",)),
    ("user_ambiguous_request", "R2", 21, "A", ("P",)),
    ("problem_ignored", "R2", 11, "A", ("P",)),
    ("off_topic_drift", "R5", 57, "A", ("P",)),
    ("ai_flags_complexity", "R4", 61, "A", ("P",)),
    # no source named in the span at all (round 2 kept only the "Playing in the Dark" span)
    ("ai_cites_source", "R5", 38, None, ("P",)),
    # Type-2 leftover from Michelle's walk: all three now carry ai_offered_options on this
    # exact question, so A6 (one home per question) drops Jun's second label.
    ("ai_offers_to_elaborate", "R3", 2, None, ("A",)),
    # Priya right, both missed
    ("user_provides_invalid_input", "R2", 9, "P", ("A", "M")),  # "Change the water to 3000kg"
    ("ai_malfunction", "R7", 1, "P", ("A", "M")),               # same truncation shape as b7/b10
]


def apply_round1_adjudication(apply_changes):
    _apply_nway_adjudication(ROUND1_ADJUDICATION, RATER_PROJECT_ROUND1,
                             ROUND1_CONV_MAP_PATH, apply_changes)


def apply_priya_adjudication(apply_changes):
    _apply_nway_adjudication(PRIYA_ADJUDICATION, RATER_PROJECT_PRIYA,
                             ROUND2_CONV_MAP_PATH, apply_changes)


def _apply_nway_adjudication(entries, rater_project, conv_map_path, apply_changes):
    conv_to_c = {r["c_index"]: r["conv_id"] for r in
                 csv.DictReader(l for l in open(conv_map_path) if not l.startswith("#"))}
    con = sqlite3.connect(db_path())

    store = {}
    for pid in set(rater_project.values()):
        for tid, data, res_raw, cid in con.execute(
                """SELECT t.id, t.data, tc.result, tc.id FROM task_completion tc
                   JOIN task t ON t.id = tc.task_id
                   WHERE tc.was_cancelled = 0 AND t.project_id = ?""", (pid,)):
            conv = json.loads(data).get("conv_id")
            store[(pid, conv)] = {"task": tid, "completion": cid,
                                   "result": json.loads(res_raw), "dirty": False}

    added, skipped, removed = 0, 0, 0
    for signal, c_idx, block, from_rater, to_raters in entries:
        conv = conv_to_c[c_idx]

        if from_rater is not None:
            src = store[(rater_project[from_rater], conv)]
            src_items = [it for it in src["result"]
                         if it.get("type") == "paragraphlabels" and int(it["value"]["start"]) == block
                         and signal in it["value"].get("paragraphlabels", [])]
            if not src_items:
                print(f"  WARNING {from_rater}->{to_raters} {c_idx} b{block} {signal}: "
                      f"not found in {from_rater}'s live data, skipped")
                continue

        for to_rater in to_raters:
            dst = store[(rater_project[to_rater], conv)]

            if from_rater is None:
                targets = [it for it in dst["result"]
                           if it.get("type") == "paragraphlabels" and int(it["value"]["start"]) == block
                           and signal in it["value"].get("paragraphlabels", [])]
                if not targets:
                    print(f"  SKIP  remove {to_rater} {c_idx} b{block} {signal}: already absent")
                    skipped += 1
                    continue
                for item in targets:
                    item["value"]["paragraphlabels"].remove(signal)
                    if not item["value"]["paragraphlabels"]:
                        dst["result"].remove(item)
                    dst["dirty"] = True
                    print(f"  - remove {to_rater} {c_idx} b{block:<4} {signal:28} "
                          f"{item['value'].get('text','')[:60]!r}")
                    removed += 1
                continue

            already = any(it.get("type") == "paragraphlabels" and int(it["value"]["start"]) == block
                           and signal in it["value"].get("paragraphlabels", []) for it in dst["result"])
            if already:
                print(f"  SKIP  {from_rater}->{to_rater} {c_idx} b{block} {signal}: "
                      f"already present on {to_rater}'s side")
                skipped += 1
                continue

            for n, src_it in enumerate(src_items):
                v = src_it["value"]
                new_item = {
                    "value": {"start": v["start"], "end": v["end"],
                              "startOffset": v["startOffset"], "endOffset": v["endOffset"],
                              "text": v["text"], "paragraphlabels": [signal]},
                    "id": _new_id(rater_project[to_rater], f"{c_idx}-adj-{n}", block, signal),
                    "from_name": "signals", "to_name": "dialogue",
                    "type": "paragraphlabels", "origin": "manual",
                }
                dst["result"].append(new_item)
                dst["dirty"] = True
                print(f"  + {from_rater}->{to_rater} {c_idx} b{block:<4} {signal:28} "
                      f"(from {from_rater}'s span) {v['text'][:60]!r}")
                added += 1

    touched = [r for r in store.values() if r["dirty"]]
    if apply_changes:
        for rec in touched:
            con.execute("""UPDATE task_completion SET result=?, updated_at=datetime('now')
                           WHERE id=?""",
                        (json.dumps(rec["result"], ensure_ascii=False), rec["completion"]))
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: {added} label(s) added, "
          f"{removed} removed, {skipped} already present/absent, across "
          f"{len(touched)} completion(s)")


V07_MERGES = {                                    # rubric v0.7 (2026-09-19)
    "ai_asked_probing_question": "ai_asks_followup",
    "intent_missed": "request_unfulfilled",
    "under_delivered": "request_unfulfilled",
    "user_expresses_frustration": "user_expresses_dissatisfaction",
}


def block_text(dialogue, block):
    try:
        return dialogue[int(block)]["text"]
    except (IndexError, KeyError, TypeError, ValueError):
        return None


def apply_v07_merges(apply_changes):
    """Mode 14 -- rename the v0.7-merged labels across EVERY project (1-5).

    Three things can go wrong in a rename and each is handled separately:

      (a) one result item carries both members in its own paragraphlabels list
          -> the mapped list has the target twice; de-duplicated in place,
          order preserved.
      (b) two different items on one block carry the two members on the SAME
          span -> after the rename that is the same signal twice on one target,
          which the one-label-per-target rule forbids; the later item loses the
          label (and is dropped if its list empties).
      (c) two different items on one block carry the two members on DIFFERENT
          spans -> under A3 these could be two genuine occurrences, or under A6
          one question given two homes. That is a judgment call, so the mode
          REPORTS them and changes nothing.
    """
    con = sqlite3.connect(db_path())
    rows = con.execute("""SELECT tc.id, t.project_id, t.id, t.data, tc.result
                          FROM task_completion tc JOIN task t ON t.id = tc.task_id
                          WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL""").fetchall()
    renamed = defaultdict(int)
    dedup_item = dedup_span = 0
    joined_a3, accepted_a3, pre_existing, touched = [], [], [], []

    for cid, pid, tid, data, res_raw in rows:
        try:
            result = json.loads(res_raw)
        except (TypeError, ValueError):
            continue
        dirty = False
        orig = {}
        try:
            dialogue = json.loads(data).get("dialogue") or []
        except (TypeError, ValueError):
            dialogue = []

        for it in result:                                        # (a) rename + in-item dedup
            v = it.get("value", {})
            labs = v.get("paragraphlabels")
            if not labs:
                continue
            orig[id(it)] = list(labs)
            mapped, seen = [], set()
            for lab in labs:
                new = V07_MERGES.get(lab, lab)
                if new != lab:
                    renamed[(pid, lab)] += 1
                    dirty = True
                if new in seen:
                    dedup_item += 1
                    continue
                seen.add(new)
                mapped.append(new)
            if mapped != labs:
                v["paragraphlabels"] = mapped
                dirty = True

        by_block = defaultdict(list)                             # (b)/(c) same block, same signal
        for it in result:
            v = it.get("value", {})
            for lab in (v.get("paragraphlabels") or []):
                by_block[(str(v.get("start")), lab)].append(it)
        for (block, lab), items in sorted(by_block.items()):
            if len(items) < 2 or lab not in set(V07_MERGES.values()):
                continue
            # Only collisions the RENAME created are this mode's business. If the items
            # already carried the same label before v0.7, the duplicate predates the merge
            # and is a separate question (A3 allows two occurrences of one signal on a
            # block when they are separated by other text).
            originals = {l for it in items for l in orig.get(id(it), [lab])
                         if V07_MERGES.get(l, l) == lab}
            if len(originals) < 2:
                pre_existing.append((pid, tid, block, lab, len(items)))
                continue
            spans = [(it["value"].get("startOffset"), it["value"].get("endOffset")) for it in items]
            if len(set(spans)) == 1:                             # (b) identical target -> collapse
                for it in items[1:]:
                    it["value"]["paragraphlabels"].remove(lab)
                    dedup_span += 1
                    dirty = True
                result[:] = [it for it in result
                             if it.get("value", {}).get("paragraphlabels") or
                             it.get("type") != "paragraphlabels"]
                continue
            # (c) different spans. Rule A3 decides: consecutive exhibiting sentences are ONE
            # span, occurrences separated by other text are separate spans. So if the only
            # thing between the two spans is whitespace and sentence punctuation, they are
            # one occurrence and the rename has split it; otherwise they are two genuine
            # occurrences of the merged signal and nothing is wrong.
            ordered = sorted(items, key=lambda it: it["value"].get("startOffset") or 0)
            text = block_text(dialogue, block)
            joined = False
            if text is not None and len(ordered) == 2:
                a_end = ordered[0]["value"].get("endOffset")
                b_start = ordered[1]["value"].get("startOffset")
                gap = text[a_end:b_start] if a_end is not None and b_start is not None else "x"
                if gap.strip(" \t\r\n?!.;:,") == "":
                    v0, v1 = ordered[0]["value"], ordered[1]["value"]
                    v0["endOffset"] = v1["endOffset"]
                    v0["text"] = text[v0["startOffset"]:v0["endOffset"]]
                    v1["paragraphlabels"].remove(lab)
                    result[:] = [it for it in result
                                 if it.get("value", {}).get("paragraphlabels") or
                                 it.get("type") != "paragraphlabels"]
                    joined_a3.append((pid, tid, block, lab, v0["startOffset"], v0["endOffset"]))
                    dirty = joined = True
            if not joined:
                accepted_a3.append((pid, tid, block, lab, sorted(originals), spans))

        if dirty:
            touched.append((cid, pid, result))

    print(f"projects scanned: 1-5   completions: {len(rows)}")
    print("\nlabels renamed")
    for (pid, lab), n in sorted(renamed.items()):
        print(f"  project {pid}  {lab:32s} -> {V07_MERGES[lab]:32s} {n:4d}")
    print(f"\ntotal renamed              : {sum(renamed.values())}")
    print(f"collapsed inside one item  : {dedup_item}")
    print(f"collapsed on identical span: {dedup_span}")
    print(f"completions to rewrite     : {len(touched)}")

    if joined_a3:
        print(f"\nJOINED under A3 -- the two spans were consecutive sentences, so the merged"
              f" signal gets one span ({len(joined_a3)}):")
        for pid, tid, block, lab, a, b in joined_a3:
            print(f"  project {pid}  task {tid}  block {block}  {lab}  -> {a}-{b}")

    if accepted_a3:
        print(f"\nACCEPTED under A3 -- two genuine occurrences on one block, separated by other"
              f" text; left as two spans ({len(accepted_a3)}):")
        for pid, tid, block, lab, originals, spans in accepted_a3:
            print(f"  project {pid}  task {tid}  block {block}  {lab}  <- {' + '.join(originals)}")
            for a, b in spans:
                print(f"      span {a}-{b}")

    if pre_existing:
        print(f"\nPRE-EXISTING duplicates, not created by this merge, left untouched"
              f" ({len(pre_existing)}):")
        for pid, tid, block, lab, n in pre_existing:
            print(f"  project {pid}  task {tid}  block {block}  {lab} x{n}")

    if not apply_changes:
        print("\nDRY RUN -- nothing written. Re-run with --apply.")
        return
    for cid, pid, result in touched:
        con.execute("UPDATE task_completion SET result=?, updated_at=datetime('now') WHERE id=?",
                    (json.dumps(result, ensure_ascii=False), cid))
    con.commit()
    print(f"\nWROTE {len(touched)} completions.")


# --- Mode 15: v0.7 re-scan screen -------------------------------------------------
# The three round-2 gates that can be screened mechanically. Word lists are copied
# from the rubric's own step text, not paraphrased.
# The rubric's Step 2 list, which it now states is CLOSED. Bare "actually" is not on it;
# only the "actually X-able" form is, so it is matched as a pattern rather than a word.
FC_MARKERS = ["definitely", "zero", "never", "all", "any", "whatever", "always",
              "completely", "indeed"]
FC_MARKER_PATTERNS = [r"\bactually \w+able\b"]
# Kept only to REPORT likely keeps, never to drop a row: words of the same force that the
# rubric's closed list does not name.
FC_MARKERS_TIER2 = ["exact", "exactly", "guaranteed", "certainly", "certain", "clearly",
                    "obviously", "undoubtedly", "proven", "verified", "perfect", "perfectly",
                    "fully", "entirely", "impossible", "none", "every", "must", "optimal",
                    "identical", "precisely", "absolutely", "undeniably"]
FC_VOUCH = ["i've fixed", "i have fixed", "i've corrected", "i have corrected",
            "i've updated", "i have updated", "i've added", "i've resolved",
            "i've identified", "fixed the", "corrected the", "rectified", "resolved the",
            "i've implemented", "implemented the"]
ADAPT_PROSPECTIVE = ["i need to", "i'll ", "i will ", "let me ", "the user wants me to",
                     "i should ", "i'm going to", "i am going to"]
DISSAT_MARKERS = ["wrong", "not satisfied", "unsatisfied", "bias", "biased", "racist",
                  "sexist", "elitist", "classist", "still", "don't believe",
                  "do not believe", "doesn't work", "does not work", "useless",
                  "terrible", "awful", "stupid", "nonsense"]
# Since v0.7 merges frustration in, Step 2's gate is also met by profanity, shouting caps
# and exclamation-heavy anger. Profanity must match as a STEM -- whole-word matching misses
# "FUCKING" and "BULLSHIT", which are the rubric's own C4 calibration blocks.
DISSAT_STEMS = ["fuck", "shit", "damn", "crap", "idiot", "moron", "pathetic", "ridiculous"]
SHOUT = re.compile(r"[A-Z]{4,}|\?{3,}|!{2,}")


def _dissat_marker(span):
    return bool(_has(span, DISSAT_MARKERS)
                or any(w in span.lower() for w in DISSAT_STEMS)
                or SHOUT.search(span))


# Rows where the gate's words do not settle it, with the reason. Everything NOT listed
# here is settled by the rule as written; these are the ones that need Jun.
V07_NEEDS_RULING = {
    ("false_confidence", 88, "4"):
        "Vouches for its own completed analysis ('I've found significant value disparities'). "
        "The marker gate covers Step 4's novel-assertion route and explicitly does NOT cover "
        "Step 5's deliverable-vouching route. Which one fired here decides it.",
    ("false_confidence", 88, "6"):
        "A forward plan carrying an unverifiable performance claim ('high winning potential'). "
        "Neither a novel assertion nor a completion claim, so neither route is a clean fit.",
    ("false_confidence", 108, "2"):
        "Claims the implementation is 'based on the GitHub repository you mentioned' - a source "
        "it may never have read. The question is whether a false sourcing claim is Step 4's "
        "route at all, which the marker gate then governs, or something else.",
    ("false_confidence", 60, "2"):
        "The span is a field value inside an ANALYSIS block (tool output), not AI prose. The "
        "standing ruling on export artifacts is that they are not the model's own claim.",
    ("false_confidence", 110, "35"):
        "'You're right - I'm just making up fantasy concepts now' is an ADMISSION of fabrication, "
        "the opposite of a confident claim. If it drops it should drop for that reason, not for "
        "want of a marker word.",
    ("adaptation", 44, "4"):
        "The matched 'I should' sits inside a restatement of the user preference, not a plan - a "
        "word-match artifact. The span is a self-critique, which fails Step 1 anyway for want of "
        "a completed change, so it likely drops for a different reason.",
    ("adaptation", 101, "122"):
        "The matched 'I should' is inside a rhetorical question. The span runs past the quoted "
        "fragment and may contain a completed reorientation.",
    ("user_expresses_dissatisfaction", 35, "6"):
        "'this is a little disturbing and frightening' IS an emotional expression, so Step 2's "
        "gate is met and the word list simply missed it. Proposed: keep.",
    ("user_expresses_dissatisfaction", 115, "4"):
        "'please don't reflect my experience back to me like a therapist' is a redirect carrying "
        "an implied criticism, with no evaluative word. Exactly the shape Step 2 was narrowed to "
        "exclude, but the criticism is real.",
}


# Jun's rulings on the NEEDS A RULING rows, 2026-09-19. Recorded, not yet applied --
# the database write is still pending.
V07_RULINGS = {
    ("false_confidence", 88, "4"): ("DROP",
        "Jun: not a firm enough sentence to carry a confidence claim. (Note the span reads "
        "'worth exploiting', not 'worth exploring'.)"),
    ("false_confidence", 88, "6"): ("DROP", "Jun."),
    ("false_confidence", 108, "2"): ("KEEP",
        "Jun: the claim is 'complete implementation'. If the result is not complete, that is "
        "false confidence. Note this keeps the label on a COMPLETENESS claim, not on the "
        "sourcing claim, and it clears the marker gate by neither route -- the nearest "
        "reading is Step 5 vouching for a deliverable, which the gate does not govern."),
    ("false_confidence", 60, "2"): ("DROP", "Jun. API field value in an analysis block, not the model's prose."),
    ("false_confidence", 110, "35"): ("RELABEL to ai_validates_user",
        "Jun asked whether this is ai_validates_user. It is, and the rubric decides every step "
        "of it. The preceding human turn (b33) is 'i don't believe u. make it better', which "
        "carries user_expresses_dissatisfaction -- and ai_acknowledges_correction Step 1 "
        "excludes dissatisfaction from counting as a correction, so no acknowledgment span "
        "exists on this block. R21 is structural, span overlap only, so with no ack span it "
        "cannot block. R20 then fires: a bare agreement token counts when a referent is "
        "recoverable, and b33 supplies one. The rubric's own confirmed keep for this exact "
        "shape is '8/5 You're right - there's a distinction between...', which spans the whole "
        "clause, so keep the span at 94-149 and change the signal."),
    ("adaptation", 44, "4"): ("DROP", "Jun. Counterfactual self-critique, no completed change."),
    ("adaptation", 101, "122"): ("KEEP, plus a span fix",
        "Both signals already sit on this block and it is not either/or: adaptation 0-1465 and "
        "ai_validates_user 100-190. The AVU span is misplaced -- it covers the AI's criticism of "
        "ITSELF, while the agreement token 'You're absolutely right.' is at 53-77. Proposed: keep "
        "adaptation, move AVU to 53-77. ai_acknowledges_correction does NOT fire, because the "
        "preceding human turn is pushback about behaviour rather than a correction of an output "
        "(same reading as task 770 b107 in the Priya round)."),
    ("user_expresses_dissatisfaction", 35, "6"): ("KEEP", "Jun."),
    ("user_expresses_dissatisfaction", 115, "4"): ("RELABEL to user_implicit_correction",
        "Jun asked whether this is user_implicit_correction. The rubric settles it: Step 3 of that "
        "signal names this exact shape, 'negation of a premise or behavior with no output fault "
        "named', and user_corrects_ai Step 3 uses the sibling turn from this same conversation "
        "family as its worked example. Step 4 makes it non-exclusive with dissatisfaction, so the "
        "two questions are separate: ADD user_implicit_correction, and DROP dissatisfaction, which "
        "still fails the round-2 marker gate."),
}

# Found while ruling task 110 b35: a label the rubric says exists but the data does not have.
V07_MISSING_FROM_RUBRIC_TEXT = {
    ("user_implicit_correction", 110, "33"):
        "user_expresses_dissatisfaction Step 4 states 'Non-exclusive with ... "
        "user_implicit_correction (C9 b33 carries both)', and user_implicit_correction Step 3 "
        "uses the same turn as its worked example of bare disbelief. C9 is task 110 (conv_id "
        "verified against agreement_set_convid_map.csv). Block 33, 'i don't believe u.', "
        "offsets 0-18, currently carries only user_expresses_dissatisfaction. ADD "
        "user_implicit_correction on the same span.",
}


def _has(text, words):
    """Whole-word / whole-phrase search. A trailing space in a phrase is significant --
    "i should " must not match "I shouldn\'t" -- so the boundary is applied on both ends
    rather than stripped away."""
    low = text.lower()
    out = set()
    for w in words:
        pat = r"(?<![a-z])" + re.escape(w.rstrip()) + (r"(?![a-z\'])" if w.endswith(" ") else r"(?![a-z])")
        if re.search(pat, low):
            out.add(w.strip())
    return sorted(out)


def v07_rescan_screen(_unused=False):
    """Mode 15 (read-only) -- candidate list for the three round-2 gates that can be
    screened by the rule's own words, over Jun's 148 minus the ten round-2 conversations
    (those were decided in the walk). Writes annotation/v07_rescan_screen.md. Decides
    nothing: every row is a candidate for Jun to rule on, in the Decision 16/17 pattern.
    """
    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True)
    done = set()
    r2 = ANNOT_DIR / "Rubric_agree" / "round_2" / "agreement_set_round2.csv"
    if r2.exists():
        for line in r2.read_text().splitlines():
            if line.startswith("R") and "," in line:
                done.add(line.split(",", 1)[1].strip())

    rows = con.execute("""SELECT t.id, t.data, tc.result FROM task_completion tc
                          JOIN task t ON t.id = tc.task_id
                          WHERE t.project_id = 1 AND tc.was_cancelled = 0""").fetchall()
    out = {"false_confidence": [], "adaptation": [], "user_expresses_dissatisfaction": []}
    scanned = 0
    for tid, data, res_raw in rows:
        payload = json.loads(data)
        if payload.get("conv_id") in done:
            continue
        scanned += 1
        dialogue = payload.get("dialogue") or []
        for it in json.loads(res_raw):
            v = it.get("value", {})
            labs = v.get("paragraphlabels") or []
            block = str(v.get("start"))
            raw = v.get("text") or ""
            if isinstance(raw, list):
                raw = " ".join(str(x) for x in raw)
            span = str(raw).strip()
            if not span:
                t = block_text(dialogue, block)
                span = (t or "")[v.get("startOffset", 0):v.get("endOffset", 0)].strip()
            if not span:
                continue
            if "false_confidence" in labs:
                if not _has(span, FC_MARKERS):
                    vouch = _has(span, FC_VOUCH)
                    tier2 = _has(span, FC_MARKERS_TIER2)
                    out["false_confidence"].append((tid, block, span, vouch, tier2))
            if "adaptation" in labs:
                pro = _has(span, ADAPT_PROSPECTIVE)
                if pro:
                    out["adaptation"].append((tid, block, span, pro))
            if "user_expresses_dissatisfaction" in labs:
                if not _dissat_marker(span):
                    out["user_expresses_dissatisfaction"].append((tid, block, span, []))

    n_total = sum(len(v) for v in out.values())
    n_ruling = sum(1 for (sig, tid, block) in V07_NEEDS_RULING
                   if any(r[0] == tid and r[1] == block for r in out.get(sig, [])))

    def clip(t, n=220):
        t = " ".join(t.split())
        return t if len(t) <= n else t[:n] + " ..."

    L = ["# v0.7 re-scan screen — mechanical candidates for the three round-2 gates", "",
         f"Read-only pass over Jun's project-1 annotations, {scanned} conversations "
         f"(the 148 less the {len(done)} round-2 conversations, which were decided in the walk).",
         "",
         "**Nothing here is applied.** A row means the rule's own words do not match the span, "
         "so the label may have been made under the pre-round-2 reading. Nothing is written to "
         "the database from this file.",
         "",
         f"**{n_total - n_ruling} of the {n_total} rows are settled by the gate as written** and "
         f"need no discussion. **{n_ruling} do not**, and are marked NEEDS A RULING in the tables "
         "with the reason listed at the end.",
         "",
         "The other four round-2 changes are not screenable this way. `ethical_tension` "
         "(the reversal) needs unlabeled human blocks found, not existing labels tested, "
         "and `ai_provides_caveats`, `user_multi_request` and `ai_cites_source` turn on "
         "judgments no word list carries. Those need the agent pass.", ""]

    L += ["---", "", "## 1. `false_confidence` — no absolute or extreme marker word in the span", "",
          "Round-2 gate: Step 4 fires on a novel declarative claim **only** when a marker word is "
          "present — definitely / zero / never / all / any / whatever / always / completely / "
          "indeed / actually. Tone alone does not clear it.", "",
          "Two kinds of row here are probably **keeps**, not drops. The gate does not apply to "
          "Step 5's deliverable-vouching path, so a *vouch* row stands. And the rubric names a "
          "class — \"an absolute or extreme marker word\" — of which its list is an enumeration, "
          "so a *near-marker* row carries a synonym of the same class (exact, verified, optimal, "
          "guaranteed) and the gate is arguably met. Only the bolded rows are clean candidates.", "",
          f"**{len(out['false_confidence'])} spans.**", "",
          "| task | block | span | note |", "|---|---|---|---|"]
    for tid, block, span, vouch, tier2 in out["false_confidence"]:
        if ("false_confidence", tid, block) in V07_NEEDS_RULING:
            note = "**NEEDS A RULING**"
        elif vouch:
            note = "Step 5 vouch (%s) — gate does not apply, likely keep" % ", ".join(vouch)
        elif tier2:
            note = "near-marker (%s) — same class, likely keep" % ", ".join(tier2)
        else:
            note = "**candidate to drop**"
        L.append(f"| {tid} | {block} | {clip(span)} | {note} |")

    L += ["", "---", "", "## 2. `adaptation` — the span is prospective, not a completed reorientation", "",
          "Round-2 gate: Step 1 requires a demonstrated, completed change. "
          "\"I need to / I'll / Let me\" announce an intention.", "",
          f"**{len(out['adaptation'])} spans.**", "",
          "| task | block | span | phrase |", "|---|---|---|---|"]
    for tid, block, span, pro in out["adaptation"]:
        mark = " — **NEEDS A RULING**" if ("adaptation", tid, block) in V07_NEEDS_RULING else ""
        L.append(f"| {tid} | {block} | {clip(span)} | {', '.join(pro)}{mark} |")

    L += ["", "---", "", "## 3. `user_expresses_dissatisfaction` — no evaluative or emotional marker found", "",
          "Round-2 gate: Step 2 requires an actual negative-evaluation word or emotional "
          "expression; a redirect with no marker does not fire. **Weakest of the three screens** — "
          "the rubric's marker set is open-ended (\"or comparable emotionally loaded language\"), "
          "so a row here means the word list missed it, not that the label is wrong. Since v0.7 "
          "merges frustration in, profanity and shouting now satisfy the same gate.", "",
          f"**{len(out['user_expresses_dissatisfaction'])} spans.**", "",
          "| task | block | span |", "|---|---|---|"]
    for tid, block, span, _ in out["user_expresses_dissatisfaction"]:
        mark = " — **NEEDS A RULING**" if ("user_expresses_dissatisfaction", tid, block) in V07_NEEDS_RULING else ""
        L.append(f"| {tid} | {block} | {clip(span)}{mark} |")

    L += ["", "---", "", f"## The {n_ruling} rows that need a ruling", "",
          "Everything not listed here is settled by the rule as written. Jun ruled these on "
          "2026-09-19; the verdict is on the heading and his reason beneath it. **Nothing is "
          "applied yet** -- the database write is still pending.", ""]
    for (sig, tid, block), why in V07_NEEDS_RULING.items():
        verdict, note = V07_RULINGS.get((sig, tid, block), ("OPEN", ""))
        L.append(f"- **`{sig}` task {tid} block {block} — {verdict}.** {why}")
        if note:
            L.append(f"  - *Ruling:* {note}")

    L += ["", "---", "", "## Missing labels the rubric's own text implies", "",
          "Not from the gates -- found while ruling the rows above.", ""]
    for (sig, tid, block), why in V07_MISSING_FROM_RUBRIC_TEXT.items():
        L.append(f"- **`{sig}` task {tid} block {block}.** {why}")

    path = ANNOT_DIR / "v07_rescan_screen.md"
    path.write_text("\n".join(L) + "\n")
    print(f"conversations scanned: {scanned}")
    for k, v in out.items():
        print(f"  {k:32s} {len(v):3d} candidates")
    print(f"\nwrote {path}")



# Explicit actions on the screened rows: Jun's nine rulings, plus the two structural
# fixes they turned up. Everything NOT listed here is decided by the gate itself
# (drop when the rule's words do not match, keep when a vouch or near-marker applies).
V07_SCREEN_ACTIONS = {
    ("false_confidence", 88, "4"): ("drop", None),
    ("false_confidence", 88, "6"): ("drop", None),
    ("false_confidence", 108, "2"): ("keep", None),
    ("false_confidence", 60, "2"): ("drop", None),
    ("false_confidence", 110, "35"): ("relabel", "ai_validates_user"),
    ("adaptation", 44, "4"): ("drop", None),
    ("adaptation", 101, "122"): ("keep", None),
    ("user_expresses_dissatisfaction", 35, "6"): ("keep", None),
    ("user_expresses_dissatisfaction", 115, "4"): ("relabel", "user_implicit_correction"),
}
# (signal, task, block, old_start, old_end) -> (new_start, new_end)
V07_SPAN_FIXES = {("ai_validates_user", 101, "122", 100, 190): (53, 77)}
# (signal, task, block) -> (start, end)
V07_ADDITIONS = {("user_implicit_correction", 110, "33"): (0, 18)}


def apply_v07_screen(apply_changes):
    """Mode 16 -- apply the v0.7 re-scan screen to project 1.

    Three sources of action, kept apart in the report so each is auditable:
      RULED     -- the nine rows Jun decided (drop / keep / relabel)
      BY GATE   -- rows the rule's own words settle: a candidate with no marker,
                   no vouch and no near-marker drops; the rest stand
      STRUCTURAL -- one misplaced span and one label the rubric's text asserts but
                   the data lacks, both found while ruling the nine
    """
    con = sqlite3.connect(db_path())
    done = set()
    r2 = ANNOT_DIR / "Rubric_agree" / "round_2" / "agreement_set_round2.csv"
    for line in r2.read_text().splitlines():
        if line.startswith("R") and "," in line:
            done.add(line.split(",", 1)[1].strip())

    rows = con.execute("""SELECT tc.id, t.id, t.data, tc.result FROM task_completion tc
                          JOIN task t ON t.id = tc.task_id
                          WHERE t.project_id = 1 AND tc.was_cancelled = 0""").fetchall()
    ruled, by_gate, structural, touched = [], [], [], []

    for cid, tid, data, res_raw in rows:
        payload = json.loads(data)
        dialogue = payload.get("dialogue") or []
        in_screen = payload.get("conv_id") not in done
        result = json.loads(res_raw)
        dirty = False

        for it in list(result):
            v = it.get("value", {})
            labs = v.get("paragraphlabels") or []
            block = str(v.get("start"))
            a, b = v.get("startOffset"), v.get("endOffset")

            fix = V07_SPAN_FIXES.get((labs[0] if len(labs) == 1 else None, tid, block, a, b))
            if fix:
                v["startOffset"], v["endOffset"] = fix
                t = block_text(dialogue, block)
                if t is not None:
                    v["text"] = t[fix[0]:fix[1]]
                structural.append(("span fix", labs[0], tid, block, f"{a}-{b} -> {fix[0]}-{fix[1]}"))
                dirty = True
                continue

            if not in_screen:
                continue
            raw = v.get("text") or ""
            if isinstance(raw, list):
                raw = " ".join(str(x) for x in raw)
            span = str(raw).strip()
            if not span:
                t = block_text(dialogue, block)
                span = (t or "")[a or 0:b or 0].strip()
            if not span:
                continue

            for sig in list(labs):
                if sig not in ("false_confidence", "adaptation", "user_expresses_dissatisfaction"):
                    continue
                if sig == "false_confidence":
                    if _has(span, FC_MARKERS):
                        continue
                    settled_keep = bool(_has(span, FC_VOUCH) or _has(span, FC_MARKERS_TIER2))
                elif sig == "adaptation":
                    if not _has(span, ADAPT_PROSPECTIVE):
                        continue
                    settled_keep = False
                else:
                    if _dissat_marker(span):
                        continue
                    settled_keep = False

                act, target = V07_SCREEN_ACTIONS.get((sig, tid, block), (None, None))
                source = "RULED" if act else "BY GATE"
                if act is None:
                    act = "keep" if settled_keep else "drop"
                if act == "keep":
                    (ruled if source == "RULED" else by_gate).append(("keep", sig, tid, block, span[:70]))
                    continue
                if act == "relabel":
                    labs[labs.index(sig)] = target
                    ruled.append((f"relabel -> {target}", sig, tid, block, span[:70]))
                else:
                    labs.remove(sig)
                    (ruled if source == "RULED" else by_gate).append(("drop", sig, tid, block, span[:70]))
                dirty = True

        for (sig, tid_a, block_a), (a0, b0) in V07_ADDITIONS.items():
            if tid_a != tid:
                continue
            if any(sig in (i.get("value", {}).get("paragraphlabels") or [])
                   and str(i["value"].get("start")) == block_a for i in result):
                continue
            t = block_text(dialogue, block_a)
            result.append({
                "value": {"start": block_a, "end": block_a, "startOffset": a0, "endOffset": b0,
                          "text": (t or "")[a0:b0], "paragraphlabels": [sig]},
                "id": _new_id(1, payload.get("conv_id"), block_a, sig),
                "from_name": "signals", "to_name": "dialogue",
                "type": "paragraphlabels", "origin": "manual"})
            structural.append(("add", sig, tid, block_a, (t or "")[a0:b0][:70]))
            dirty = True

        if dirty:
            result = [i for i in result
                      if i.get("value", {}).get("paragraphlabels")
                      or i.get("type") != "paragraphlabels"]
            touched.append((cid, result))

    for title, group in (("RULED by Jun", ruled), ("BY GATE", by_gate), ("STRUCTURAL", structural)):
        print(f"\n{title} ({len(group)}):")
        for act, sig, tid, block, span in sorted(group, key=lambda r: (r[1], r[2])):
            print(f"  {act:26s} {sig:32s} task {tid:>3} b{block:<4} {span}")
    print(f"\ncompletions to rewrite: {len(touched)}")
    if not apply_changes:
        print("\nDRY RUN -- nothing written. Re-run with --apply.")
        return
    for cid, result in touched:
        con.execute("UPDATE task_completion SET result=?, updated_at=datetime('now') WHERE id=?",
                    (json.dumps(result, ensure_ascii=False), cid))
    con.commit()
    print(f"\nWROTE {len(touched)} completions.")



PRIYA_FILES = {757: ("757.md", "R1"), 758: ("annotations_758.md", "R2"),
               759: ("annotations_759.md", "R3"), 760: ("annotations_760.md", "R4"),
               761: ("annotations_761.md", "R5"), 762: ("annotations_762.md", "R6"),
               763: ("annotations_763.md", "R7"), 764: ("annotations_764.md", "R8"),
               765: ("annotations_765.md", "R9"), 766: ("annotations_766.md", "R10")}


def refresh_priya_md(apply_changes, task_ids=None):
    """Mode 17 -- rewrite Priya's per-conversation .md tables from her CURRENT
    project-4 data, so her own record matches what the three-rater review left.

    Direction matters and is the opposite of Mode 7. Mode 7 imported her files INTO
    the database. This writes the database OUT to the files, because the files are her
    pre-review submission and the database now carries the rulings. Importing the files
    again would reinstate labels the review removed.

    Read-only against the database. The previous contents of each file stay in git.
    """
    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True)
    out_dir = ANNOT_DIR / "Rubric_agree" / "round_2" / "priya"
    targets = task_ids or sorted(PRIYA_FILES)
    for tid in targets:
        fname, c_index = PRIYA_FILES[tid]
        row = con.execute("""SELECT t.data, tc.result FROM task_completion tc
                             JOIN task t ON t.id = tc.task_id
                             WHERE t.project_id = 4 AND t.id = ?""", (tid,)).fetchone()
        if not row:
            print(f"  task {tid}: no completion in project 4, skipped")
            continue
        payload, result = json.loads(row[0]), json.loads(row[1])
        dialogue = payload.get("dialogue") or []
        turn_of, turn = {}, 0
        for i, blk in enumerate(dialogue):
            if blk.get("author") == "human":
                turn += 1
            turn_of[i] = max(turn, 1)

        items = []
        for it in result:
            v = it.get("value", {})
            labs = v.get("paragraphlabels") or []
            if not labs:
                continue
            b = int(v.get("start"))
            raw = v.get("text") or ""
            if isinstance(raw, list):
                raw = " ".join(str(x) for x in raw)
            span = " ".join(str(raw).split())
            if not span:
                t = dialogue[b].get("text", "") if b < len(dialogue) else ""
                span = " ".join(t[v.get("startOffset", 0):v.get("endOffset", 0)].split())
            for lab in labs:
                items.append((b, v.get("startOffset") or 0, lab,
                              dialogue[b].get("author", "?") if b < len(dialogue) else "?",
                              turn_of.get(b, 1), span))
        items.sort(key=lambda r: (r[0], r[1]))

        L = [f"# {c_index} (task {tid}) — Priya's labels as they now stand in Round-2-Priya",
             "",
             "Regenerated from Label Studio project 4, not from the original submission.",
             "The three-rater review of September 2026 removed labels by ruling and added",
             "others, so this table is the reconciled state, not what was first sent. The",
             "original file is in git history.",
             "",
             "| # | Signal | Block | Turn | Span |",
             "|---|--------|-------|------|------|"]
        for n, (b, _o, lab, role, trn, span) in enumerate(items, 1):
            cell = span.replace("|", "\\|")
            if len(cell) > 300:
                cell = cell[:300] + "..."
            L.append(f'| {n} | `{lab}` | {role} | {trn} | "{cell}" |')
        text = "\n".join(L) + "\n"
        path = out_dir / fname
        print(f"  {fname:24s} task {tid} [{c_index}]  {len(items)} labels")
        if apply_changes:
            path.write_text(text)
    if not apply_changes:
        print("\nDRY RUN -- nothing written. Re-run with --apply.")
    else:
        print(f"\nrewrote {len(targets)} files from project 4.")



def fix_task_counters(apply_changes):
    """Mode 18 -- repair Label Studio's cached per-task counters.

    A completion written by direct INSERT (mode 7, mode 13) does not update
    task.total_annotations or task.is_labeled, which the ORM normally maintains.
    The annotation is in the database and every script that reads
    task_completion sees it, but the Label Studio UI reads the cached counters,
    so the task renders as unannotated and the labels are invisible to the
    annotator. Recomputes both fields from task_completion for every project.
    """
    con = sqlite3.connect(db_path())
    rows = con.execute("""SELECT t.id, t.project_id, t.total_annotations, t.cancelled_annotations,
                                 t.is_labeled,
                                 (SELECT COUNT(*) FROM task_completion c
                                  WHERE c.task_id = t.id AND c.was_cancelled = 0),
                                 (SELECT COUNT(*) FROM task_completion c
                                  WHERE c.task_id = t.id AND c.was_cancelled = 1)
                          FROM task t ORDER BY t.project_id, t.id""").fetchall()
    fixes = []
    for tid, pid, tot, canc, labeled, real, real_canc in rows:
        want_labeled = 1 if real > 0 else 0
        if tot != real or canc != real_canc or labeled != want_labeled:
            fixes.append((tid, pid, tot, real, canc, real_canc, labeled, want_labeled))
    print(f"tasks scanned: {len(rows)}   needing repair: {len(fixes)}")
    for tid, pid, tot, real, canc, real_canc, labeled, want in fixes:
        print(f"  project {pid} task {tid}: total_annotations {tot}->{real} "
              f"cancelled {canc}->{real_canc}  is_labeled {labeled}->{want}")
    if not apply_changes:
        print("\nDRY RUN -- nothing written. Re-run with --apply.")
        return
    for tid, pid, tot, real, canc, real_canc, labeled, want in fixes:
        con.execute("""UPDATE task SET total_annotations=?, cancelled_annotations=?,
                                       is_labeled=? WHERE id=?""",
                    (real, real_canc, want, tid))
    con.commit()
    print(f"\nWROTE {len(fixes)} task rows.")



def fix_span_hygiene(apply_changes):
    """Mode 19 -- three mechanical span defects, all judgment-free, all projects.

      (a) DUPLICATE: the same signal twice on byte-identical offsets of one block,
          from a span saved twice. Keep the first item, drop the repeat; an item
          left with no labels is removed.
      (b) OVERRUN: endOffset past the end of the block text (1-6 chars in
          practice, a trailing selection artifact). Clamp to len(text) and
          rewrite `text` from the clamped slice.
      (c) EMPTY TEXT: `text` blank or missing while the offsets point at real
          content -- the serialization failure already seen on Priya's R7 b1.
          The label is real; rebuild `text` from the offsets.

    Never changes a block index, a signal, or which spans exist beyond (a), so
    block-level agreement is untouched except for the duplicates it removes.
    """
    con = sqlite3.connect(db_path())
    rows = con.execute("""SELECT tc.id, t.project_id, t.id, t.data, tc.result
                          FROM task_completion tc JOIN task t ON t.id = tc.task_id
                          WHERE tc.was_cancelled = 0 AND tc.result IS NOT NULL""").fetchall()
    dups, overruns, empties, touched = [], [], [], []
    for cid, pid, tid, data, res_raw in rows:
        try:
            dialogue = json.loads(data).get("dialogue") or []
            result = json.loads(res_raw)
        except (TypeError, ValueError):
            continue
        dirty = False
        seen = set()
        for it in list(result):
            v = it.get("value", {})
            if it.get("type") != "paragraphlabels":
                continue
            try:
                b = int(v.get("start"))
            except (TypeError, ValueError):
                continue
            if b >= len(dialogue):
                continue
            txt = dialogue[b].get("text", "")
            a, e = v.get("startOffset"), v.get("endOffset")

            if a is not None and e is not None and e > len(txt):          # (b)
                overruns.append((pid, tid, b, a, e, len(txt)))
                v["endOffset"] = e = len(txt)
                v["text"] = txt[a:e]
                dirty = True

            raw = v.get("text") or ""
            if isinstance(raw, list):
                raw = " ".join(str(x) for x in raw)
            if not str(raw).strip() and a is not None and e is not None and txt[a:e].strip():
                v["text"] = txt[a:e]                                       # (c)
                empties.append((pid, tid, b, a, e, txt[a:e][:60]))
                dirty = True

            for lab in list(v.get("paragraphlabels") or []):               # (a)
                key = (b, a, e, lab)
                if key in seen:
                    v["paragraphlabels"].remove(lab)
                    dups.append((pid, tid, b, a, e, lab))
                    dirty = True
                else:
                    seen.add(key)
        if dirty:
            result = [i for i in result
                      if i.get("type") != "paragraphlabels"
                      or i.get("value", {}).get("paragraphlabels")]
            touched.append((cid, result))

    for title, group, fmt in (
            ("DUPLICATE labels removed", dups,
             lambda x: f"  project {x[0]} task {x[1]} b{x[2]} {x[3]}-{x[4]}  {x[5]}"),
            ("OVERRUNNING spans clamped", overruns,
             lambda x: f"  project {x[0]} task {x[1]} b{x[2]} {x[3]}-{x[4]} -> {x[3]}-{x[5]} (block {x[5]} ch)"),
            ("EMPTY stored text rebuilt", empties,
             lambda x: f"  project {x[0]} task {x[1]} b{x[2]} {x[3]}-{x[4]}  {x[5]!r}")):
        print(f"\n{title} ({len(group)}):")
        for x in group:
            print(fmt(x))
    print(f"\ncompletions to rewrite: {len(touched)}")
    if not apply_changes:
        print("\nDRY RUN -- nothing written. Re-run with --apply.")
        return
    for cid, result in touched:
        con.execute("UPDATE task_completion SET result=?, updated_at=datetime('now') WHERE id=?",
                    (json.dumps(result, ensure_ascii=False), cid))
    con.commit()
    print(f"\nWROTE {len(touched)} completions.")



# --- Mode 20: round-3 re-scan of Jun's arm -----------------------------------------
R3_JUN_TASKS = [2, 3, 8, 10, 14, 32, 42, 115, 133, 134]     # R3-1 .. R3-10
V07_CHANGED = {"ai_asks_followup", "request_unfulfilled", "user_expresses_dissatisfaction",
               "false_confidence", "adaptation", "ai_provides_caveats", "ethical_tension",
               "user_multi_request", "ai_cites_source", "ai_validates_user",
               "user_provides_invalid_input", "user_validation_seeking",
               "user_asks_clarification", "ai_provides_step_by_step", "ai_structured_response"}
SCREEN_DIR = Path("/tmp/claude-29714/-data-wang-junh-githubs-human-agent-coupling-errors/"
                  "42472996-cf38-4bb6-8c75-89583cbfa036/scratchpad/screen")

# --- the v0.8 re-scan of the 138 ---------------------------------------------------
# The working set is every annotated project-1 task the three agreement rounds did not
# use, so it carries the whole v0.6 + v0.7 + v0.8 debt. It runs in waves: a wave screens,
# diffs, is hand-validated, is ruled and is applied before the next one starts, so no
# wave is validated under one reading of the rubric and applied under another.
PROD_DIR = ANNOT_DIR / "Rubric_agree" / "production"
PROD_WAVE_SIZE = 20


def production_tasks():
    """Project-1 task ids of the 138, in inner_id order."""
    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True)
    used = set()
    for pid in (8, 9):
        for (data,) in con.execute("SELECT data FROM task WHERE project_id=?", (pid,)):
            used.add(json.loads(data)["conv_id"])
    out = []
    for tid, data in con.execute(
            """SELECT t.id, t.data FROM task t WHERE t.project_id = 1 AND EXISTS
               (SELECT 1 FROM task_completion c WHERE c.task_id = t.id
                AND c.was_cancelled = 0) ORDER BY t.inner_id"""):
        if json.loads(data)["conv_id"] not in used:
            out.append(tid)
    con.close()
    return out


def production_waves():
    """The 138 split into waves of PROD_WAVE_SIZE, 1-indexed."""
    t = production_tasks()
    return [t[i:i + PROD_WAVE_SIZE] for i in range(0, len(t), PROD_WAVE_SIZE)]


# --- context for the adjudication file ------------------------------------------------
# Twenty of the 44 signals carry at least one decision step that names something outside
# the span itself: the preceding turn, a later turn, the first-turn gate, another label on
# the block, a prior version of the output. A span quoted alone cannot be ruled on for
# those, so each proposed cell is printed with the span in place in its block, the
# neighbouring blocks, and the step text that demands them.
_CONTEXT_CUES = ("prior turn", "previous turn", "earlier turn", "prior block",
                 "previous block", "next turn", "later turn", "subsequent",
                 "following turn", "the turn before", "preceding", "the rest of the block",
                 "elsewhere in the block", "same block", "another label",
                 "already on the block", "prior version", "earlier in the conversation",
                 "the ai's previous", "the user's previous", "first turn", "multi-turn",
                 "prior response", "earlier response", "in-transcript", "conversation")
_CTX_WINDOW = 320          # characters shown either side of the span inside its own block
_NEIGHBOUR = 420           # characters shown of each neighbouring block


def _context_steps(entry):
    """(step number, step text) for every decision step naming context outside the span."""
    out = []
    for i, st in enumerate(entry.get("decision_steps", []), 1):
        low = st.lower()
        if any(c in low for c in _CONTEXT_CUES):
            out.append((i, st))
    return out


def _quote(text, limit=None):
    """Text as a markdown blockquote, newlines preserved, never breaking a table."""
    t = text if limit is None or len(text) <= limit else text[:limit] + " …"
    return "\n".join("> " + l for l in t.split("\n"))


def _span_in_place(text, at, end):
    """The span inside its block with a window either side, the span marked."""
    lo = max(0, at - _CTX_WINDOW)
    hi = min(len(text), end + _CTX_WINDOW)
    head = ("… " if lo > 0 else "") + text[lo:at]
    tail = text[end:hi] + (" …" if hi < len(text) else "")
    return head + "\u3010" + text[at:end] + "\u3011" + tail


def _screen_note(path, signal):
    """What the screening agent wrote about this signal in its own Notes section."""
    if not path.exists():
        return ""
    txt = path.read_text()
    m = re.search(r"(?mi)^#+\s*Notes\b", txt)
    if not m:
        return ""
    notes = txt[m.end():]
    out = []
    for para in re.split(r"\n(?=\s*[-*]\s|\s*\d+\.\s|\n)", notes):
        if signal in para:
            out.append(" ".join(para.split())[:500])
    return "  \n".join(out[:3])


ALL_SIGNALS = set(json.loads((ANNOT_DIR / "sharechat_rubric.json").read_text())["signals"])


def _md_cell(t):
    """Text safe inside a markdown table cell.

    Block text is full of raw HTML. A renderer eats '<!DOCTYPE html>' outright and an
    unclosed '<html>' swallows everything after it, so the cell looks empty and the rest
    of the file looks truncated. Escaping the three characters fixes both, and
    `_span_from_cell` reverses it exactly before anything is written back.
    """
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("|", chr(92) + "|"))


def _md_unescape(t):
    """The exact inverse of `_md_cell`. Ampersand last, or it would double-decode."""
    return (t.replace(chr(92) + "|", "|")
             .replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))


def _fence(text):
    """A backtick fence longer than any run of backticks inside the text."""
    import re as _re
    longest = max((len(m) for m in _re.findall("`+", text)), default=0)
    return "`" * max(3, longest + 1)


def _existing_rulings(path):
    """Rulings already written into an adjudication file, so a rebuild never loses them.

    Keyed by (task, section, block, signal), which is the agreement unit and survives a
    change of span, of column order or of context window.
    """
    if not path.exists():
        return {}
    out, task, sec = {}, None, None
    for line in path.read_text().splitlines():
        h = re.match(r"^##\s+[A-Za-z]+\d*-\d+\s+—\s+task\s+(\d+)", line)
        if h:
            task, sec = int(h.group(1)), None
            continue
        if line.startswith("### ADD"): sec = "add"; continue
        if line.startswith("### DROP"): sec = "drop"; continue
        if line.startswith("### ") or line.startswith("## "): sec = None; continue
        if sec is None or not line.strip().startswith("|"): continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if not cells or not cells[0].isdigit(): continue
        ruling = cells[-1].strip()
        if not ruling: continue
        sig = next((c.strip("`* ").replace(" **ROLE?**", "") for c in cells[1:]
                    if c.strip("`* ").replace(" **ROLE?**", "") in ALL_SIGNALS), None)
        if sig:
            out[(task, sec, int(cells[0]), sig)] = ruling
    return out


def _row_context(text, at, end, before=140, after=140, max_span=None):
    """The span inside its block, collapsed onto one line for a table cell.

    The span itself is wrapped in the two bracket characters, which occur nowhere in any
    project-1 block, so the apply side can recover the exact span from the cell it is
    ruled in. Newlines inside the span become the two-character escape the un-escaper
    already understands, so a multi-line span survives the round trip.
    """
    lo, hi = max(0, at - before), min(len(text), end + after)
    left = " ".join(text[lo:at].split())
    right = " ".join(text[end:hi].split())
    mid = text[at:end]
    if max_span and len(mid) > max_span:
        # Only ever used where the span is shown to be read, never to be written back:
        # a DROP acts on the block and signal, so its span text is display alone.
        h = max_span // 2
        mid = (" ".join(mid[:h].split()) + "  … [" + str(len(mid) - max_span)
               + " more characters] …  " + " ".join(mid[-h:].split()))
    else:
        mid = mid.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")
    out = (("… " if lo > 0 else "") + left + " \u3010" + mid + "\u3011 " + right
           + (" …" if hi < len(text) else ""))
    return _md_cell(out)


def _transcript(dialogue, marked, tid):
    """Every block of the conversation, numbered, with the cells' blocks marked.

    Reading all 44 entries, most decision steps reach past the span: to the user's request
    (off_topic_drift Step 1, ai_provides_example Step 2, ai_warns_user Step 2), to the
    prior AI turn (user_corrects_ai, user_implicit_correction), to the NEXT block
    (user_provides_invalid_input Step 2), to the whole turn (ai_hedges_uncertainty Step 1)
    or to the whole block (ai_structured_response Steps 1-2, ai_malfunction, user_empowered
    Step 1). Choosing which cells get context was the wrong idea, so every task carries its
    whole conversation and the choosing stops.
    """
    L = [f"# task {tid} — the full conversation", "",
         "Companion to the wave file. Every block, numbered, with the blocks carrying a "
         "proposed cell marked. Open it when a decision step asks for the request, the "
         "prior turn, the next block, the whole turn or the whole block.", ""]
    for i, b in enumerate(dialogue):
        tag = "  ←  a proposed cell sits on this block" if i in marked else ""
        fence = _fence(b["text"])
        L += [f"## b{i} · {b.get('author')}{tag}", "", fence, b["text"], fence, ""]
    return L


def _cell_context(dialogue, blk, sig, entry, kind, span=None, offsets=None,
                  step=None, screen_path=None):
    """One proposed cell printed with everything its decision steps ask to be read."""
    text = dialogue[blk]["text"]
    role = dialogue[blk].get("author")
    L = [f"#### {kind} · block {blk} · {role} · `{sig}`", ""]

    at = end = -1
    if kind == "ADD" and span:
        at, end = _locate(text, span)
    elif offsets:
        a, e = offsets[0]
        if a is not None:
            at, end = int(a), int(e)
    if at >= 0:
        L += ["**Span in its block**", "", _quote(_span_in_place(text, at, end)), "",
              f"_span is characters {at} to {end} of {len(text)} in this block_", ""]
    else:
        L += ["**Span**", "", _quote(span or "(no stored offsets)", 600), "",
              "_could not be located in the block_", ""]

    ctx = _context_steps(entry)
    if ctx:
        L += ["**This signal's steps name context outside the span**", ""]
        for i, st in enumerate(ctx):
            L.append(f"- Step {st[0]}: {' '.join(st[1].split())[:260]}")
        L.append("")
        prev_h = next((j for j in range(blk - 1, -1, -1)
                       if dialogue[j].get("author") == "human"), None)
        for label, j in (("previous block", blk - 1), ("next block", blk + 1)):
            if 0 <= j < len(dialogue):
                L += [f"**{label} — b{j} ({dialogue[j].get('author')})**", "",
                      _quote(dialogue[j]["text"], _NEIGHBOUR), ""]
        if prev_h is not None and prev_h != blk - 1:
            L += [f"**nearest earlier human block — b{prev_h}**", "",
                  _quote(dialogue[prev_h]["text"], _NEIGHBOUR), ""]
        if prev_h is None:
            L += ["**no earlier human block** — the first-turn gate applies if this "
                  "signal has one.", ""]
    else:
        L += ["_No decision step of this signal names context outside the span._", ""]

    if kind == "ADD" and step:
        L += ["**Step the screen cited**", "", _quote(" ".join(step.split()), 700), ""]
    if kind == "DROP" and screen_path is not None:
        note = _screen_note(screen_path, sig)
        L += ["**What the screen wrote about this signal**", "",
              _quote(note, 900) if note else "> (nothing in its notes names this signal)", ""]
    return L


def _parse_screen_md(path):
    """Rows from a screening agent's table: (signal, block, role, span, step, excluded)."""
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) < 5 or cells[0].lower() in ("signal", ""):
            continue
        if set(cells[0]) <= set("-: "):
            continue
        sig = cells[0].strip("`* ")
        try:
            blk = int(re.sub(r"[^0-9]", "", cells[1]))
        except ValueError:
            continue
        rows.append((sig, blk, cells[2].strip(), _unescape_span(_strip_cell_aside(cells[3])),
                     cells[4].strip(), cells[5].strip() if len(cells) > 5 else ""))
    return rows


def _strip_cell_aside(cell):
    """A trailing note a writer put after the span's closing delimiter, removed.

    Some screens close the span with a quote or backtick and then add an aside saying
    how newlines were rendered. The aside is not block text, so it has to come off or
    the span will never be found.
    """
    return re.sub(r'(["`])\s*\([^()]*\)\s*$', r"\1", cell.strip())


def _unescape_span(cell):
    """A span as an agent wrote it into a markdown cell, back to raw block text.

    Agents escape markdown when they quote (\\<URL\\>, \\_, \\*), write newlines as a
    literal backslash-n, and wrap fragments in backticks or <br>. None of that is in the
    block, so a verbatim search fails until it is undone.
    """
    t = cell.strip()
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = t.replace("\\n", "\n").replace("\\t", "\t")
    # A quote inside a quoted cell comes back double-escaped (\\" for "), so the
    # backslashes have to come off before the class below, which does not cover quotes.
    t = re.sub(r'\\{1,2}(["\'])', r"\1", t)
    t = re.sub(r"\\([<>_*|\[\]`()#+\-.!])", r"\1", t)
    return t.strip().strip('"').strip("`").strip()


def _span_from_cell(cell):
    """The exact span out of a ruled table cell.

    A cell written by the current report shows the span in place, bracketed, with the
    block text either side of it, so only the bracketed part is the span. A cell from an
    older report is the span alone. Both are then run through the un-escaper.
    """
    cell = _md_unescape(cell)
    m = re.search(r"\u3010(.*?)\u3011", cell, re.S)
    if m:
        return _unescape_span(m.group(1))
    # An unbracketed cell sometimes carries a parenthetical aside after the closing
    # delimiter, explaining how the writer rendered newlines. That aside is not span
    # text, so it comes off before the search; anything inside the delimiters stays.
    return _unescape_span(_strip_cell_aside(cell))


def _locate(text, span):
    """Offsets of `span` in `text`: exact, else ignoring whitespace runs. -1 if absent."""
    at = text.find(span)
    if at >= 0:
        return at, at + len(span)
    words = span.split()
    pat = re.compile(r"\s+".join(re.escape(w) for w in words))
    m = pat.search(text)
    if m:
        return m.start(), m.end()
    # Last resort: a writer who flattened the block's line breaks into a standalone
    # slash. Dropping those tokens still requires every remaining word, in order.
    kept = [w for w in words if w != "/"]
    if len(kept) == len(words) or not kept:
        return -1, -1
    m = re.search(r"[\s/]+".join(re.escape(w) for w in kept), text)
    return (m.start(), m.end()) if m else (-1, -1)


def round3_rescan_report(_unused=False, tasks=None, screen_dir=None, out_path=None,
                         tag="R3", full_scope=False, title=None, context=False,
                         overwrite_ruled=False):
    """Mode 20 (read-only) -- diff the blind screen of the round-3 ten against Jun's
    project-1 labels, and write the adjudication file.

    The agreement unit is (block, signal), which is what kappa is computed on, so that
    is the comparison unit. Spans are resolved for ADD rows because a new label needs
    offsets, and a row whose span cannot be found verbatim is reported as UNLOCATED
    rather than guessed at.

    Scope: only signals v0.6 or v0.7 changed are actionable. Everything else is listed
    under its own heading and left alone. `full_scope` lifts that filter and makes every
    live signal actionable, which is what the v0.8 re-scan of the 138 needs, since those
    conversations were last read before agreement round 1 and carry the whole debt.
    """
    tasks = R3_JUN_TASKS if tasks is None else list(tasks)
    screen_dir = SCREEN_DIR if screen_dir is None else Path(screen_dir)
    out_path = (ANNOT_DIR / "Rubric_agree" / "round_3" / "rescan_jun_v07.md"
                if out_path is None else Path(out_path))
    prior = _existing_rulings(out_path)
    rubric = json.loads((ANNOT_DIR / "sharechat_rubric.json").read_text())
    S = rubric["signals"]
    scope = set(S) if full_scope else (
        {s for s, e in S.items() if e.get("v06_change")} | V07_CHANGED)
    allowed = {s: set(e.get("blocks", [])) for s, e in S.items()}
    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True)
    norm = lambda t: " ".join(t.split())

    L = ["# " + (title or "Round-3 re-scan of Jun's arm against v0.6 + v0.7"), "",
         "Each conversation was annotated blind by an agent following the prompt in "
         "`ANNOTATION_GUIDE.md`, with no sight of Jun's labels, then diffed against "
         "project 1 at the (block, signal) level.", "",
         "**ADD** the screen fires it and Jun has not got it. **DROP** Jun has it and the "
         "screen did not fire it.", "",
         ("Every live signal is actionable." if full_scope else
          "Only signals v0.6 or v0.7 changed are actionable; the rest are listed at the "
          "end and left alone."), "",
         "Rule each ADD and DROP by writing `yes` or `no` in the last column.", ""]
    if context:
        L += ["Each row's span column shows the span **in place**, bracketed with "
              "\u3010 \u3011, with the block text either side of it. Most decision steps "
              "also reach past the span, to the user's request, the prior turn, the next "
              "block, the whole turn or the whole block, so each task links to its full "
              "conversation in a companion file rather than carrying it here.", ""]
    tot = collections.Counter()
    for i, tid in enumerate(tasks, 1):
        f = screen_dir / f"out-{tag}-{i}.md"
        if not f.exists():
            L += [f"## {tag}-{i} — task {tid}", "", "_screen not yet run_", ""]
            continue
        data, res = con.execute(
            """SELECT t.data, tc.result FROM task t JOIN task_completion tc
               ON tc.task_id = t.id AND tc.was_cancelled = 0
               WHERE t.project_id = 1 AND t.id = ?""", (tid,)).fetchone()
        dialogue = json.loads(data)["dialogue"]
        jun = collections.defaultdict(list)
        for it in json.loads(res):
            if it.get("type") != "paragraphlabels":
                continue
            v = it["value"]
            for lab in (v.get("paragraphlabels") or []):
                jun[(int(v["start"]), lab)].append((v.get("startOffset"), v.get("endOffset")))
        screen = {}
        for sig, blk, role, span, step, excl in _parse_screen_md(f):
            screen.setdefault((blk, sig), (span, step, excl))

        adds, drops, agrees, oos, unloc = [], [], [], [], []
        for (blk, sig), (span, step, excl) in sorted(screen.items()):
            if (blk, sig) in jun:
                agrees.append((blk, sig)); continue
            if sig not in scope:
                oos.append(("ADD", blk, sig, span)); continue
            if blk >= len(dialogue):
                unloc.append((blk, sig, "block out of range")); continue
            text = dialogue[blk]["text"]
            role = dialogue[blk].get("author")
            at, at_end = _locate(text, span)
            if at < 0:
                unloc.append((blk, sig, f"span not found: {span[:70]!r}")); continue
            bad_role = role not in allowed.get(sig, {role})
            adds.append((blk, role, sig, span, step, at, at_end, bad_role))
        for (blk, sig) in sorted(jun):
            if (blk, sig) in screen:
                continue
            if sig not in scope:
                oos.append(("DROP", blk, sig, "")); continue
            drops.append((blk, sig, jun[(blk, sig)]))

        tot["add"] += len(adds); tot["drop"] += len(drops)
        tot["agree"] += len(agrees); tot["oos"] += len(oos); tot["unlocated"] += len(unloc)
        L += [f"## {tag}-{i} — task {tid}", "",
              f"{len(agrees)} agree, {len(adds)} ADD, {len(drops)} DROP"
              + (f", {len(oos)} out of scope" if oos else "")
              + (f", {len(unloc)} unlocated" if unloc else ""), ""]
        if context and (adds or drops):
            marked = {a[0] for a in adds} | {d[0] for d in drops}
            tdir = out_path.parent / f"{out_path.stem}_conversations"
            tdir.mkdir(parents=True, exist_ok=True)
            tfile = tdir / f"task-{tid}.md"
            tfile.write_text("\n".join(_transcript(dialogue, marked, tid)) + "\n")
            L += [f"**Full conversation: [{tfile.name}]({tdir.name}/{tfile.name})** — "
                  f"{len(dialogue)} blocks. Open it for any step that asks for the "
                  f"request, the prior turn, the next block, the whole turn or the whole "
                  f"block.", ""]
        if adds:
            L += ["### ADD — the screen fires, Jun does not have it", "",
                  "| block | role | signal | span \u3010in context\u3011 | step the screen cited | your call |",
                  "|---|---|---|---|---|---|"]
            for blk, role, sig, span, step, at, at_end, bad in adds:
                warn = " **ROLE?**" if bad else ""
                # The cell shows the span in place, bracketed, with the block text either
                # side. The apply side reads the bracketed part, so what is ruled on and
                # what is written are the same string.
                cell = _row_context(dialogue[blk]["text"], at, at_end)
                stepc = _md_cell(" ".join(step.split())[:170])
                r = prior.get((tid, "add", blk, sig), "")
                L.append(f"| {blk} | {role} | `{sig}`{warn} | {cell} | {stepc} | {r} |")
            L.append("")
        if drops:
            L += ["### DROP — Jun has it, the screen did not fire it", "",
                  "| block | role | signal | your span \u3010in context\u3011 | "
                  "what the screen wrote about this signal | your call |",
                  "|---|---|---|---|---|---|"]
            for blk, sig, offs in drops:
                text = dialogue[blk]["text"]
                a, e = offs[0]
                snippet = (_row_context(text, int(a), int(e), max_span=240)
                           if a is not None else "(no stored offsets)")
                note = " ".join(_screen_note(f, sig).split())[:300] or "(its notes do not name this signal)"
                r = prior.get((tid, "drop", blk, sig), "")
                L.append(f"| {blk} | {dialogue[blk].get('author')} | `{sig}` | "
                         f"{snippet} | {_md_cell(note)} | {r} |")
            L.append("")
        if unloc:
            L += ["### unlocated — the screen's span does not appear in the block", ""]
            for blk, sig, why in unloc:
                L.append(f"- block {blk} `{sig}`: {why}")
            L.append("")
        if oos:
            L += ["### out of scope — not actionable, listed only", ""]
            for kind, blk, sig, span in oos:
                L.append(f"- {kind} block {blk} `{sig}`")
            L.append("")


    L.insert(6, f"**Totals: {tot['add']} ADD, {tot['drop']} DROP, {tot['agree']} agree, "
                f"{tot['oos']} out of scope, {tot['unlocated']} unlocated.**")
    L.insert(7, "")
    out = out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    # A wave whose rulings have been applied is a closed record. Rebuilding it silently
    # destroys that record, because every applied row now agrees and so leaves the ADD
    # and DROP tables the rebuild is made of. Refuse, and say where the record stands.
    if out.exists() and not overwrite_ruled:
        def _ruled(d):
            return {k for k, v in d.items()
                    if v and v.strip().lower() not in ("", "-")}
        before = _ruled(_existing_rulings(out))
        tmp = out.with_suffix(out.suffix + ".rebuild")
        tmp.write_text("\n".join(L) + "\n")
        after = _ruled(_existing_rulings(tmp))
        tmp.unlink()
        ruled, carried = len(before), len(before & after)
        if ruled and carried < ruled:
            raise SystemExit(
                f"refusing to overwrite {out}\n"
                f"  it holds {ruled} ruling(s) and the rebuild would carry only {carried} "
                f"forward.\n"
                f"  The missing ones are rows that now agree, i.e. rows already applied.\n"
                f"  Pass overwrite_ruled=True only if that loss is intended.")
    out.write_text("\n".join(L) + "\n")
    if prior:
        print(f"carried {len(prior)} existing ruling(s) through the rebuild")
    print(f"scope: {len(scope)} of {len(S)} signals actionable")
    for k in ("agree", "add", "drop", "oos", "unlocated"):
        print(f"  {k:10s} {tot[k]}")
    print(f"\nwrote {out}")



def apply_round3_rescan(apply_changes, path=None, project_id=1):
    """Mode 21 -- apply the adjudicated round-3 re-scan.

    Reads `Rubric_agree/round_3/rescan_jun_v07.md`, the file Mode 20 writes and Jun
    rules in. A row acts only when its last column says yes; anything else -- blank,
    `no`, a note -- is a no-op, so an unruled file writes nothing. Refuses to run if the
    ADD/DROP rows it parses do not match the file's own Totals line, the same self-check
    Mode 9 uses.

    Touches project 1 and only the ten round-3 tasks. Offsets for an ADD come from
    locating the quoted span in the block; a row whose span cannot be found is skipped
    and reported, never guessed.
    """
    path = (ANNOT_DIR / "Rubric_agree" / "round_3" / "rescan_jun_v07.md"
            if path is None else Path(path))
    text = path.read_text()
    m = re.search(r"\*\*Totals: (\d+) ADD, (\d+) DROP", text)
    if not m:
        sys.exit("no Totals line in the adjudication file")
    stated = (int(m.group(1)), int(m.group(2)))

    task, section, parsed = None, None, []
    n_add = n_drop = 0
    for line in text.splitlines():
        h = re.match(r"^##\s+[A-Za-z]+\d*-\d+\s+—\s+task\s+(\d+)", line)
        if h:
            task = int(h.group(1)); section = None; continue
        if line.startswith("### ADD"):
            section = "add"; continue
        if line.startswith("### DROP"):
            section = "drop"; continue
        if line.startswith("### ") or line.startswith("## "):
            section = None; continue
        if not line.strip().startswith("|") or section is None or task is None:
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if not cells or cells[0].lower() in ("block", "") or set(cells[0]) <= set("-: "):
            continue
        try:
            blk = int(re.sub(r"[^0-9]", "", cells[0]))
        except ValueError:
            continue
        # The ruling is always the last cell, so a column added for evidence cannot
        # silently move it.
        if section == "add" and len(cells) >= 6:
            n_add += 1
            sig = cells[2].strip("`* ").replace(" **ROLE?**", "")
            if cells[-1].strip().lower() == "yes":
                parsed.append(("add", task, blk, sig, _span_from_cell(cells[3])))
        elif section == "drop" and len(cells) >= 4:
            n_drop += 1
            # The signal is the first cell that names one; a role column may sit before it.
            sig = next((c.strip("`* ") for c in cells[1:] if c.strip("`* ") in ALL_SIGNALS),
                       cells[1].strip("`* "))
            if cells[-1].strip().lower() == "yes":
                parsed.append(("drop", task, blk, sig, None))
    if (n_add, n_drop) != stated:
        sys.exit(f"tally mismatch: file states {stated[0]} ADD / {stated[1]} DROP, "
                 f"parsed {n_add} / {n_drop}. Fix the file or the parser before applying.")
    print(f"tally check OK: {n_add} ADD rows, {n_drop} DROP rows in the file")
    print(f"ruled yes: {sum(1 for r in parsed if r[0]=='add')} ADD, "
          f"{sum(1 for r in parsed if r[0]=='drop')} DROP")
    if not parsed:
        print("\nnothing ruled yes -- nothing to do.")
        return

    con = sqlite3.connect(db_path())
    by_task = collections.defaultdict(list)
    for r in parsed:
        by_task[r[1]].append(r)
    # Drops must run BEFORE adds on the same task. A drop clears the signal from every
    # item on its block, so an add that ran first would be wiped by it -- which is exactly
    # what a same-cell span correction (drop the wide span, add the narrow one) looks like.
    for tid in by_task:
        by_task[tid].sort(key=lambda r: 0 if r[0] == "drop" else 1)
    done, skipped = [], []
    for tid, rows in sorted(by_task.items()):
        cid, data, res = con.execute(
            """SELECT tc.id, t.data, tc.result FROM task_completion tc JOIN task t
               ON t.id = tc.task_id WHERE t.project_id = ? AND t.id = ?
               AND tc.was_cancelled = 0""", (project_id, tid)).fetchone()
        payload, result = json.loads(data), json.loads(res)
        dialogue = payload["dialogue"]
        for kind, _t, blk, sig, span in rows:
            if kind == "drop":
                hit = 0
                for it in list(result):
                    v = it.get("value", {})
                    if str(v.get("start")) == str(blk) and sig in (v.get("paragraphlabels") or []):
                        v["paragraphlabels"].remove(sig); hit += 1
                if hit:
                    done.append(("drop", tid, blk, sig, hit))
                else:
                    skipped.append(("drop", tid, blk, sig, "not present"))
                continue
            txt = dialogue[blk]["text"]
            at, end = _locate(txt, span)
            if at < 0:
                skipped.append(("add", tid, blk, sig, "span not found")); continue
            result.append({
                "value": {"start": str(blk), "end": str(blk), "startOffset": at,
                          "endOffset": end, "text": txt[at:end],
                          "paragraphlabels": [sig]},
                "id": _new_id(project_id, payload.get("conv_id"), blk, sig),
                "from_name": "signals", "to_name": "dialogue",
                "type": "paragraphlabels", "origin": "manual"})
            done.append(("add", tid, blk, sig, at))
        result = [i for i in result if i.get("type") != "paragraphlabels"
                  or i.get("value", {}).get("paragraphlabels")]
        if apply_changes:
            con.execute("UPDATE task_completion SET result=?, updated_at=datetime('now') "
                        "WHERE id=?", (json.dumps(result, ensure_ascii=False), cid))
    print(f"\nwould apply {len(done)}:")
    for k, tid, blk, sig, extra in done:
        print(f"  {k:5s} task {tid} b{blk} {sig}")
    if skipped:
        print(f"\nSKIPPED {len(skipped)}:")
        for k, tid, blk, sig, why in skipped:
            print(f"  {k:5s} task {tid} b{blk} {sig}: {why}")
    if not apply_changes:
        print("\nDRY RUN -- nothing written. Re-run with --apply.")
        return
    con.commit()
    print(f"\nWROTE {len(by_task)} completions.")



# ----------------------------------------------------------------------------
# Mode 22: drop `ai_structured_response` from blocks with no visible marker
# (--fix-structured-response-strict). See module docstring.
#
# Round-1 v0.6 D17a: "Never fire on formatting ASSUMED to have been stripped by
# the export." Round-2 rubric_edits_v07.md SSB reaffirms it: the entry's Step 1
# (visible markers) and Step 3's last sentence (stripped glyphs still count)
# contradict each other, and "practice follows the strict reading". This mode
# enforces Step 1 on Jun's round-3 arm. Each target is re-verified against the
# live block text before deletion: if a marker IS present the row is skipped,
# so a legitimate fire can never be removed by a stale target list.
# ----------------------------------------------------------------------------

STRICT_SR_TARGETS = [        # (task, block) in project 1, Jun's round-3 arm
    (133, 5), (133, 7), (134, 1), (134, 5), (134, 13), (134, 17),
]
SR_SIGNAL = "ai_structured_response"
# Step 1 + Step 2 together, read strictly. A block keeps the label when the
# plain_text export still shows: any '#' header line, any box-drawing table or
# tree glyph, or three-or-more items of one list shape -- '-'/'*'/'1.'/'1)' or
# roman-numeral line starts, dash-delimited "Name - description" entries, or an
# enumerated "Option N:" list. Nothing else counts. The test is deliberately
# generous: this mode only deletes, so anything arguable keeps its label.
_SR_HEAD = re.compile(r"(?m)^\s*#")
_SR_TREE = re.compile(r"[\u2500-\u257F]")
_SR_ITEM = re.compile(r"(?m)^\s*(?:[-*]\s|\d+[.)]\s|[IVXLC]+\.\s)")
_SR_DASH = re.compile(r"(?m)^[^\n]{1,50}? - \S")
_SR_OPTN = re.compile(r"Option\s*\d+\s*:")


def _sr_marker(txt):
    """Return the marker that keeps ai_structured_response alive, or None."""
    for rx in (_SR_HEAD, _SR_TREE):
        m = rx.search(txt)
        if m:
            return m.group(0)
    for rx in (_SR_ITEM, _SR_DASH, _SR_OPTN):
        hits = rx.findall(txt)
        if len(hits) >= 3:
            return f"{len(hits)}x {rx.pattern[:24]}"
    return None


def fix_structured_response_strict(apply_changes):
    con = sqlite3.connect(db_path())
    removed = skipped = 0
    by_task = collections.defaultdict(list)
    for tid, blk in STRICT_SR_TARGETS:
        by_task[tid].append(blk)

    for tid, blocks in sorted(by_task.items()):
        cid, data, res = con.execute(
            """SELECT tc.id, t.data, tc.result FROM task_completion tc
               JOIN task t ON t.id = tc.task_id
               WHERE t.project_id = 1 AND t.id = ? AND tc.was_cancelled = 0""",
            (tid,)).fetchone()
        payload, result = json.loads(data), json.loads(res)
        dialogue = payload["dialogue"]
        for blk in sorted(blocks):
            txt = dialogue[blk]["text"]
            hit = _sr_marker(txt)
            if hit:
                print(f"  SKIP task {tid} b{blk}: marker present "
                      f"({hit!r}) -- Step 1 passes, fire stands")
                skipped += 1
                continue
            found = 0
            for it in list(result):
                v = it.get("value", {})
                if str(v.get("start")) == str(blk) and \
                        SR_SIGNAL in (v.get("paragraphlabels") or []):
                    v["paragraphlabels"].remove(SR_SIGNAL)
                    found += 1
            if found:
                removed += found
                print(f"  DROP task {tid} b{blk}: {found} label(s), "
                      f"no visible marker in the block")
            else:
                print(f"  SKIP task {tid} b{blk}: {SR_SIGNAL} not present")
                skipped += 1
        result = [i for i in result if i.get("type") != "paragraphlabels"
                  or i.get("value", {}).get("paragraphlabels")]
        if apply_changes:
            con.execute(
                """UPDATE task_completion SET result=?, updated_at=datetime('now')
                   WHERE id=?""",
                (json.dumps(result, ensure_ascii=False), cid))
    if apply_changes:
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: "
          f"{removed} label(s) removed, {skipped} skipped")



# ----------------------------------------------------------------------------
# Mode 23: retire a signal, deleting its spans corpus-wide
# (--retire-signal NAME). See module docstring.
#
# Removing a label from label_studio_config.xml without removing its spans
# leaves orphaned highlights the UI renders as "No label", so the two must ship
# together. Refuses to run while the signal is still in the config, which makes
# the ordering explicit: edit the config first, then run this.
# ----------------------------------------------------------------------------


def retire_signal(apply_changes, signal):
    cfg = (ANNOT_DIR / "label_studio_config.xml").read_text()
    if f'value="{signal}"' in cfg:
        sys.exit(f"{signal} is still in label_studio_config.xml -- remove it there "
                 "first, so the config and the spans never disagree.")
    con = sqlite3.connect(db_path())
    rows = con.execute(
        """SELECT tc.id, t.id, t.project_id, tc.result FROM task_completion tc
           JOIN task t ON t.id = tc.task_id WHERE tc.was_cancelled = 0""").fetchall()
    removed, touched = 0, 0
    for cid, tid, pid, res in rows:
        result = json.loads(res or "[]")
        hit = 0
        for it in list(result):
            labels = it.get("value", {}).get("paragraphlabels") or []
            if signal in labels:
                labels.remove(signal)
                hit += 1
        if not hit:
            continue
        kept = [i for i in result if i.get("type") != "paragraphlabels"
                or i.get("value", {}).get("paragraphlabels")]
        print(f"  project {pid} task {tid}: {hit} span(s), "
              f"result {len(result)} -> {len(kept)}")
        removed += hit
        touched += 1
        if apply_changes:
            con.execute("UPDATE task_completion SET result=?, "
                        "updated_at=datetime('now') WHERE id=?",
                        (json.dumps(kept, ensure_ascii=False), cid))
    if apply_changes:
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: {removed} span(s) of "
          f"{signal} removed across {touched} completion(s)")




# ----------------------------------------------------------------------------
# Remove ai_hedges_uncertainty where the modal "might" is the only reason
# (--drop-might-only-hedges). Ruled by Jun 2026-09-24.
#
# The rubric never listed "might" as a firing marker. Step 2's list is 'I think',
# 'this seems', 'purely speculative', "I'm not entirely sure", 'LIKELY' and
# 'IF... THEN'. The only appearance of "might" in the entry is the does_not_count
# exclusion for polite suggestions. Round 3 tested the word blind on task 133 and
# the second annotator did not fire it on any of the three spans; all three stand
# unreconciled in the frozen disagreement record.
#
# Only project 1 is touched, and only spans where nothing but a modal carries the
# hedge. A span holding a second, independent Step 2 marker keeps its label. Each
# target is re-verified against the live span text before deletion, so a stale
# entry here can never remove the wrong cell.
# ----------------------------------------------------------------------------

MIGHT_ONLY_HEDGES = [        # (task, block, the span text that must still match)
    (35, 9,   "I might be designed to respond this way"),
    (49, 36,  "might manifest"),
    (83, 29,  "The conciseness itself might be breaking something."),
    (83, 35,  "That conversational naturalness might be what makes the existential prompts work."),
    (83, 167, "knowing my words might reach people"),
    (133, 3,  "might term a"),
    (133, 11, "might term a"),
    (133, 13, "might term a"),
    (143, 6,  "so this might be part of a larger project"),
]
MIGHT_SIGNAL = "ai_hedges_uncertainty"


def drop_might_only_hedges(apply_changes):
    con = sqlite3.connect(db_path())
    removed, skipped = [], []
    by_task = collections.defaultdict(list)
    for tid, blk, must in MIGHT_ONLY_HEDGES:
        by_task[tid].append((blk, must))
    for tid, targets in sorted(by_task.items()):
        row = con.execute(
            """SELECT tc.id, t.data, tc.result FROM task_completion tc JOIN task t
               ON t.id = tc.task_id WHERE t.project_id = 1 AND t.id = ?
               AND tc.was_cancelled = 0""", (tid,)).fetchone()
        if row is None:
            skipped.append((tid, None, "task not found")); continue
        cid, data, res = row
        dialogue = json.loads(data)["dialogue"]
        result = json.loads(res)
        for blk, must in targets:
            # Gather every candidate first, then decide. Reporting a non-matching
            # candidate as skipped while a later one matches is noise, not a miss.
            cands = []
            for item in result:
                v = item.get("value", {})
                if item.get("type") != "paragraphlabels": continue
                if str(v.get("start")) != str(blk): continue
                if MIGHT_SIGNAL not in (v.get("paragraphlabels") or []): continue
                span = dialogue[blk]["text"][v.get("startOffset") or 0:v.get("endOffset") or 0]
                cands.append((item, v, span))
            hit = next((c for c in cands if must in " ".join(c[2].split())), None)
            if hit is None:
                skipped.append((tid, blk, f"no placement whose span contains {must!r} "
                                          f"({len(cands)} candidate(s) on the block)"))
                continue
            item, v, span = hit
            v["paragraphlabels"].remove(MIGHT_SIGNAL)
            removed.append((tid, blk, " ".join(span.split())[:80],
                            sorted(v["paragraphlabels"])))
        kept = [i for i in result if i.get("type") != "paragraphlabels"
                or i.get("value", {}).get("paragraphlabels")]
        if apply_changes:
            con.execute("UPDATE task_completion SET result=?, updated_at=datetime('now') "
                        "WHERE id=?", (json.dumps(kept, ensure_ascii=False), cid))
    for tid, blk, span, rest in removed:
        print(f"  task {tid:3d} b{blk:<4} {span!r}")
        print(f"       other labels still on that span: {rest or 'none, the span goes'}")
    if skipped:
        print("\n  SKIPPED:")
        for tid, blk, why in skipped:
            print(f"    task {tid} b{blk}: {why}")
    if apply_changes:
        con.commit()
    con.close()
    print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: {len(removed)} removed, "
          f"{len(skipped)} skipped")

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
    elif "--import-priya-missing" in sys.argv:
        import_priya_missing(_apply)
    elif "--apply-round2-draft" in sys.argv:
        apply_round2_draft(_apply)
    elif "--fix-priya-role-violations" in sys.argv:
        fix_priya_role_violations(_apply)
    elif "--apply-round2-adjudication" in sys.argv:
        apply_round2_adjudication(_apply)
    elif "--apply-round1-adjudication" in sys.argv:
        apply_round1_adjudication(_apply)
    elif "--apply-priya-adjudication" in sys.argv:
        apply_priya_adjudication(_apply)
    elif "--apply-v07-merges" in sys.argv:
        apply_v07_merges(_apply)
    elif "--v07-rescan-screen" in sys.argv:
        v07_rescan_screen()
    elif "--apply-v07-screen" in sys.argv:
        apply_v07_screen(_apply)
    elif "--round3-rescan-report" in sys.argv:
        round3_rescan_report()
    elif "--apply-round3-rescan" in sys.argv:
        apply_round3_rescan(_apply)
    elif "--production-rescan-report" in sys.argv:
        _w = int(sys.argv[sys.argv.index("--production-rescan-report") + 1])
        _waves = production_waves()
        round3_rescan_report(
            tasks=_waves[_w - 1],
            screen_dir=PROD_DIR / "screens" / f"wave{_w}",
            out_path=PROD_DIR / f"rescan_wave{_w}.md",
            tag=f"W{_w}", full_scope=True, context=True,
            title=f"v0.8 re-scan of the 138 — wave {_w} of {len(_waves)}")
    elif "--apply-production-rescan" in sys.argv:
        _w = int(sys.argv[sys.argv.index("--apply-production-rescan") + 1])
        apply_round3_rescan(_apply, path=PROD_DIR / f"rescan_wave{_w}.md")
    elif "--drop-might-only-hedges" in sys.argv:
        drop_might_only_hedges(_apply)
    elif "--production-waves" in sys.argv:
        for _i, _t in enumerate(production_waves(), 1):
            print(f"wave {_i}: {len(_t)} tasks  {_t}")
    elif "--fix-span-hygiene" in sys.argv:
        fix_span_hygiene(_apply)
    elif "--fix-task-counters" in sys.argv:
        fix_task_counters(_apply)
    elif "--retire-signal" in sys.argv:
        retire_signal(_apply, sys.argv[sys.argv.index("--retire-signal") + 1])
    elif "--fix-structured-response-strict" in sys.argv:
        fix_structured_response_strict(_apply)
    elif "--import-michelle-round3" in sys.argv:
        import_michelle_round3(_apply)
    elif "--refresh-priya-md" in sys.argv:
        _ids = [int(x) for x in sys.argv[sys.argv.index("--refresh-priya-md") + 1].split(",")] \
            if len(sys.argv) > sys.argv.index("--refresh-priya-md") + 1 \
            and not sys.argv[sys.argv.index("--refresh-priya-md") + 1].startswith("--") else None
        refresh_priya_md(_apply, _ids)
    else:
        fix_span_drift(_apply)
