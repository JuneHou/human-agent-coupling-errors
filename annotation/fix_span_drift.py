"""Repair mouse-selection drift between a region's stored `text` and its offsets.

Two drift classes, resolved by which side is well formed:
  (a) stored text is intact but the offsets slid by a character or two ->
      snap the offsets to where the stored text actually sits (search a small
      window around the recorded start).
  (b) stored text is itself truncated ("at's...", "hanks...") -> the offsets are
      authoritative; rewrite text from the slice and trim stray edge whitespace.
"""
import sqlite3, json, sys

SIGNAL = "ai_validates_user"
WINDOW = 10
apply_changes = "--apply" in sys.argv

con = sqlite3.connect("label_studio.sqlite3")
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
print(f"\n{'APPLIED' if apply_changes else 'DRY RUN'}: {fixed} region(s) repaired, {unresolved} unresolved")
