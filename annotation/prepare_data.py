"""
Convert english_conversations.csv to Label Studio JSON for Step 1 annotation.

Input : annotation/data/english_conversations.csv
Output: annotation/data/annotation_input.json    — JSON array, one task per conversation
        annotation/data/parse_log.jsonl           — one line per skipped/errored field
        annotation/data/prepare_stats.txt         — summary counts

Label Studio import format: JSON array of task objects, each with a "data" key.
JSONL only works for cloud storage imports; local file upload requires a JSON array.

CSV column decisions (see plan for full rationale):
  USED   : url, turns_count, message_index, role, plain_text,
            thinking, code, analysis, topic
  SKIPPED: platform (always "claude"), version (always []),
            detected_language_final (used by filter_english.py, not needed here)

Not in CSV (scraper readme fields not released on HuggingFace):
  plain_text_md, aggregated_text, warning, layout, title, shared_by, versions

Parsing rule — no silent information loss:
  raw empty (NaN / None / "None" / "nan" / "[]") → skip, log raw_empty
  non-empty but ast.literal_eval fails            → raise ValueError (stop, log parse_error)
  parses OK but result is empty list/string       → skip, log parsed_empty
  parses OK with content                          → include in dialogue
"""

import ast
import json
import os
import pandas as pd
import numpy as np

CSV       = "annotation/data/english_conversations.csv"
OUT_JSON  = "annotation/data/annotation_input.json"
OUT_LOG   = "annotation/data/parse_log.jsonl"
OUT_STATS = "annotation/data/prepare_stats.txt"

os.makedirs("annotation/data", exist_ok=True)
log_events = []


def log(url, field, event, raw_preview=None):
    entry = {"url": url, "field": field, "event": event}
    if raw_preview is not None:
        entry["raw_preview"] = str(raw_preview)[:120]
    log_events.append(entry)


def is_raw_empty(val):
    if val is None:
        return True
    if isinstance(val, float) and np.isnan(val):
        return True
    s = str(val).strip()
    return s in ("", "None", "nan", "[]")


_PII_TAGS = ["<REDACTED>", "<DATE_TIME>", "<URL>", "<NAME>", "<EMAIL>", "<PHONE>"]


def _repair_pii(raw):
    """
    Fix unescaped single quotes introduced by ShareChat PII redaction into Python repr
    strings.  Three patterns observed in the data:

      B: <TAG>}   — tag ate closing quote + closing brace of meta dict value
                    e.g. 'time': '2m, <DATE_TIME>}  →  'time': '2m, <DATE_TIME>'}
      A: <TAG>'X  — tag before apostrophe mid-string (possessive, contraction, URL suffix)
                    e.g. <REDACTED>'s  →  <REDACTED>\'s
                    Negative lookahead (?!}) avoids re-escaping Pattern-B results.
      C: <TAG>, 'key'  — tag ate closing quote, comma+key follows
                    e.g. <REDACTED>, 'content_md'  →  <REDACTED>', 'content_md'
    """
    import re
    r = raw
    for tag in _PII_TAGS:
        t = re.escape(tag)
        # B: <TAG>} — tag ate closing quote + closing brace
        r = re.sub(t + r"(\})", tag + r"'\1", r)
        # A: <TAG>'X — quote after tag, NOT before } (avoids touching Pattern-B results)
        r = re.sub(t + r"'(?!\})", tag + r"\\'", r)
        # C: <TAG>, 'key — tag ate closing quote, comma+key follows
        r = re.sub(t + r"(,\s*'[a-z_])", tag + r"'\1", r)
    return r


def _extract_thinking_content(raw):
    """
    Regex fallback: extract 'content' from a thinking Python-repr dict when
    ast.literal_eval fails even after PII repair.  Uses greedy matching to find
    the last possible closing quote before ', 'content_md''.
    """
    import re
    m = re.search(r"'content'\s*:\s*'(.+)'\s*,\s*'content_md'", raw, re.DOTALL)
    if not m:
        return None
    # Unescape the most common sequences so the content is readable
    content = m.group(1)
    content = content.replace("\\'", "'").replace("\\n", "\n").replace("\\t", "\t")
    return {"content": content}


def _safe_literal_eval(raw):
    """
    ast.literal_eval with targeted fallbacks for known ShareChat CSV artifacts.

    Attempt 1 — standard ast.literal_eval.
    Attempt 2 — fix invalid \\u/\\U unicode escapes (e.g. LaTeX \\url{}).
    Attempt 3 — repair PII-redaction quote breaks (_repair_pii).
    Attempt 4 — regex content extraction when full parse is unrecoverable.

    Raises SyntaxError / ValueError if all four attempts fail.
    """
    import re

    # Attempt 1
    try:
        return ast.literal_eval(raw)
    except (SyntaxError, ValueError):
        pass

    # Attempt 2: invalid unicode escapes
    try:
        safe = re.sub(
            r'\\u(?![0-9a-fA-F]{4})|\\U(?![0-9a-fA-F]{8})',
            lambda m: m.group(0).replace('\\', '\\\\'),
            raw,
        )
        return ast.literal_eval(safe)
    except (SyntaxError, ValueError):
        pass

    # Attempt 3: PII-redaction quote repair
    try:
        return ast.literal_eval(_repair_pii(raw))
    except (SyntaxError, ValueError):
        pass

    # Attempt 4: regex content extraction (partial recovery)
    result = _extract_thinking_content(raw)
    if result is not None:
        return result
    raise SyntaxError("all parse attempts failed")


def parse_field(raw, url, field):
    """
    Parse a Python-repr string from the CSV.
    Returns (parsed_value, ok) where ok=False means raw was empty.
    Raises ValueError on parse failure of non-empty raw.
    """
    if is_raw_empty(raw):
        log(url, field, "raw_empty")
        return None, False
    try:
        parsed = _safe_literal_eval(str(raw))
    except Exception as e:
        # Upstream data corruption (e.g. ShareChat PII redaction broke Python repr
        # escaping by inserting <REDACTED> mid-string, leaving unescaped quotes).
        # Log every case fully and skip this field — do not raise, as raising would
        # halt processing of all subsequent conversations.
        log(url, field, "parse_error", raw)
        return None, False
    # check if result is empty after parse
    if parsed is None or parsed == [] or parsed == "" or parsed == {}:
        log(url, field, "parsed_empty")
        return None, False
    return parsed, True


def extract_thinking(raw, url):
    """
    Returns the full thinking text with ALL fields from the thinking dict:
      [header: ...]  [time: ...]
      <content>
      [content_md]   (only if it differs from content)
    """
    parsed, ok = parse_field(raw, url, "thinking")
    if not ok:
        return None
    if not isinstance(parsed, dict):
        log(url, "thinking", "parsed_empty")
        return None
    content = parsed.get("content", "").strip()
    if not content:
        log(url, "thinking", "parsed_empty")
        return None
    meta     = parsed.get("meta", {}) or {}
    header   = (meta.get("header") or "").strip()
    time_val = (meta.get("time")   or "").strip()

    lines = []
    if header or time_val:
        tag = " | ".join(x for x in [header, time_val] if x)
        lines.append(f"[{tag}]")
    lines.append(content)
    # content_md is the same thinking with markdown escaping only — omitted to avoid
    # duplicate display; original value is preserved in english_conversations.csv
    return "\n".join(lines)


def extract_code(raw, url):
    """
    Returns one text block per artifact with ALL fields:
      [title | version | labels]
      [smallline: ...]  [preview_header: ...]  [right_title: ...]  [span: X-Y]
      <right_content>
    """
    parsed, ok = parse_field(raw, url, "code")
    if not ok:
        return []
    if not isinstance(parsed, list):
        log(url, "code", "parsed_empty")
        return []
    artifacts = []
    for artifact in parsed:
        meta          = artifact.get("meta", {}) or {}
        title         = (meta.get("title")     or "").strip()
        version       = (meta.get("version")   or "").strip()
        labels        = (meta.get("labels")    or "").strip()
        smallline     = (meta.get("smallline") or "").strip()
        preview_hdr   = (artifact.get("preview_header") or "").strip()
        right_title   = (artifact.get("right_title")    or "").strip()
        right_content = (artifact.get("right_content")  or "").strip()
        span          = artifact.get("span")

        if not right_content:
            continue

        header_parts = [x for x in [title or "artifact", version, labels] if x]
        lines = [f"[{' | '.join(header_parts)}]"]
        meta_tags = []
        if smallline:
            meta_tags.append(f"smallline: {smallline}")
        if preview_hdr and preview_hdr != title:
            meta_tags.append(f"preview_header: {preview_hdr}")
        if right_title:
            meta_tags.append(f"right_title: {right_title}")
        if span:
            meta_tags.append(f"span: {span[0]}-{span[1]}")
        if meta_tags:
            lines.append("[" + " | ".join(meta_tags) + "]")
        lines.append(right_content)
        artifacts.append("\n".join(lines))

    if not artifacts:
        log(url, "code", "parsed_empty")
    return artifacts


def extract_analysis(raw, url):
    """
    Returns all analysis sections with ALL fields:
      [span: X-Y]
      ## <section header>
      <text_md>
    """
    parsed, ok = parse_field(raw, url, "analysis")
    if not ok:
        return None
    if not isinstance(parsed, list):
        log(url, "analysis", "parsed_empty")
        return None
    parts = []
    for block in parsed:
        span = block.get("span")
        if span:
            parts.append(f"[span: {span[0]}-{span[1]}]")
        for section in block.get("sections", []):
            header = (section.get("header") or "").strip()
            text   = (section.get("text_md") or "").strip()
            if header:
                parts.append(f"## {header}")
            if text:
                parts.append(text)
    if not parts:
        log(url, "analysis", "parsed_empty")
        return None
    return "\n\n".join(parts)


# ── Load and group ────────────────────────────────────────────────────────────
df = pd.read_csv(CSV)
df = df.sort_values(["url", "message_index"])

documents = []

for url, conv in df.groupby("url", sort=False):
    conv = conv.sort_values("message_index")
    dialogue = []

    for _, row in conv.iterrows():
        role = str(row["role"]).strip().lower()
        idx  = int(row["message_index"])

        if role == "user":
            text = str(row["plain_text"]).strip() if not is_raw_empty(row["plain_text"]) else "[empty]"
            dialogue.append({"author": "human", "text": text})

        elif role == "llm":
            # 1. reasoning (thinking) — all fields included
            thinking_text = extract_thinking(row["thinking"], url)
            if thinking_text:
                dialogue.append({"author": "reasoning", "text": thinking_text})

            # 2. analysis (tool call sections) — all fields included
            analysis_text = extract_analysis(row["analysis"], url)
            if analysis_text:
                dialogue.append({"author": "analysis", "text": analysis_text})

            # 3. code artifacts (one paragraph per artifact) — all fields included
            for artifact_text in extract_code(row["code"], url):
                dialogue.append({"author": "code", "text": artifact_text})

            # 4. AI response (always)
            text = str(row["plain_text"]).strip() if not is_raw_empty(row["plain_text"]) else "[empty]"
            dialogue.append({"author": "ai", "text": text})

    # conversation-level metadata (flat — no "data" wrapper so Label Studio
    # maps $dialogue directly to task.data.dialogue)
    topic_vals = conv["topic"].dropna()
    topic    = str(topic_vals.iloc[0]).strip() if len(topic_vals) else ""
    n_turns  = conv["turns_count"].iloc[0]
    platform = str(conv["platform"].iloc[0]).strip() if "platform" in conv.columns else ""

    documents.append({
        "data": {
            "dialogue": dialogue,
            "conv_id":  url,
            "n_turns":  int(n_turns),
            "topic":    topic,
            "platform": platform,
        }
    })

# ── Write outputs ─────────────────────────────────────────────────────────────
with open(OUT_JSON, "w") as f:
    json.dump(documents, f, ensure_ascii=False)

with open(OUT_LOG, "w") as f:
    for entry in log_events:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# ── Stats ─────────────────────────────────────────────────────────────────────
n_docs = len(documents)
para_counts = [len(d["data"]["dialogue"]) for d in documents]
has_reasoning = sum(any(p["author"] == "reasoning" for p in d["data"]["dialogue"]) for d in documents)
has_analysis  = sum(any(p["author"] == "analysis"  for p in d["data"]["dialogue"]) for d in documents)
has_code      = sum(any(p["author"] == "code"      for p in d["data"]["dialogue"]) for d in documents)

log_summary = {}
for e in log_events:
    log_summary[e["event"]] = log_summary.get(e["event"], 0) + 1

stats_lines = [
    "prepare_data.py — output statistics",
    "=" * 50,
    f"Conversations (documents) : {n_docs:,}",
    f"",
    "Paragraphs per document:",
    f"  Min    : {min(para_counts)}",
    f"  Median : {sorted(para_counts)[len(para_counts)//2]}",
    f"  Mean   : {sum(para_counts)/len(para_counts):.1f}",
    f"  Max    : {max(para_counts)}",
    f"",
    "Documents with each author type:",
    f"  human     : {n_docs:,}  (all)",
    f"  ai        : {n_docs:,}  (all)",
    f"  reasoning : {has_reasoning:,}  ({has_reasoning/n_docs*100:.1f}%)",
    f"  analysis  : {has_analysis:,}  ({has_analysis/n_docs*100:.1f}%)",
    f"  code      : {has_code:,}  ({has_code/n_docs*100:.1f}%)",
    f"",
    "Parse log summary:",
]
for event, count in sorted(log_summary.items()):
    stats_lines.append(f"  {event:<20} : {count:,}")
if not log_summary:
    stats_lines.append("  (no events)")

with open(OUT_STATS, "w") as f:
    f.write("\n".join(stats_lines) + "\n")

for line in stats_lines:
    print(line)
print(f"\nWritten: {OUT_JSON}")
print(f"Log   : {OUT_LOG}  ({len(log_events):,} events)")
