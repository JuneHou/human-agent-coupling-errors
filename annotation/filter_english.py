"""
Filter ShareChat Claude conversations to English-majority subset.

Two-step filter:

  Step 1 — Remove conversations excluded by the ShareChat authors for
            unsupported languages (filtered_out_conversations_non_target_languages.json).

  Step 2 — Among remaining conversations, retain only those where BOTH:
              - user turns:  ≥50% of word content is from English-detected rows
              - llm turns:   ≥50% of word content is from English-detected rows
            Word content = whitespace-split from plain_text; language from
            detected_language_final. Both sides must independently pass the
            50% threshold.

Inputs:
  data/sharechat/claude_results_final_language_filtered.csv
  data/sharechat/ShareChat/filtered_out_conversations_non_target_languages.json

Output:
  annotation/data/english_conversations.csv   — filtered, all original columns retained
  annotation/data/filter_report.txt           — step-by-step counts
"""

import json
import os
import pandas as pd

CSV       = "data/sharechat/claude_results_final_language_filtered.csv"
EXCL_JSON = "data/sharechat/ShareChat/filtered_out_conversations_non_target_languages.json"
OUT_CSV   = "annotation/data/english_conversations.csv"
OUT_REPORT = "annotation/data/filter_report.txt"

# ── Step 1: load ──────────────────────────────────────────────────────────────
df = pd.read_csv(CSV)
n_rows_raw = len(df)
n_conv_raw = df["url"].nunique()

# ── Step 2: remove ShareChat-excluded conversations ───────────────────────────
with open(EXCL_JSON) as f:
    excluded_urls = set(c["url"] for c in json.load(f)["claude"])

n_excluded_in_json = len(excluded_urls)
n_excluded_in_csv  = len(excluded_urls & set(df["url"]))

df = df[~df["url"].isin(excluded_urls)].copy()
n_rows_after_excl = len(df)
n_conv_after_excl = df["url"].nunique()

# ── Step 3: compute English word-content ratio per conversation ───────────────
df["word_count"] = df["plain_text"].fillna("").astype(str).str.split().str.len()

def english_ratio_by_role(grp):
    for role in ("user", "llm"):
        sub   = grp[grp["role"] == role]
        total = sub["word_count"].sum()
        eng   = sub.loc[sub["detected_language_final"] == "English", "word_count"].sum()
        ratio = eng / total if total > 0 else float("nan")
        yield role, total, eng, ratio

def conv_english_stats(grp):
    stats = {}
    for role, total, eng, ratio in english_ratio_by_role(grp):
        stats[f"{role}_total_words"]   = total
        stats[f"{role}_english_words"] = eng
        stats[f"{role}_english_ratio"] = ratio
    return pd.Series(stats)

conv_stats = df.groupby("url", sort=False).apply(conv_english_stats)

def passes(row):
    return (
        (row["user_english_ratio"] >= 0.5 or pd.isna(row["user_english_ratio"])) and
        (row["llm_english_ratio"]  >= 0.5 or pd.isna(row["llm_english_ratio"]))
    )

english_urls     = set(conv_stats[conv_stats.apply(passes, axis=1)].index)
non_english_urls = set(conv_stats[~conv_stats.apply(passes, axis=1)].index)
nan_urls         = set(
    conv_stats[conv_stats["user_english_ratio"].isna() & conv_stats["llm_english_ratio"].isna()].index
)

df_english = df[df["url"].isin(english_urls)].copy()
df_english = df_english.drop(columns=["word_count"])

n_conv_english     = len(english_urls)
n_conv_non_english = len(non_english_urls)
n_conv_nan         = len(nan_urls)
n_rows_english     = len(df_english)

# ── Step 4: write output ──────────────────────────────────────────────────────
os.makedirs("annotation/data", exist_ok=True)
df_english.to_csv(OUT_CSV, index=False)

report_lines = [
    "ShareChat Claude — English filter report",
    "=" * 50,
    "",
    "Step 1 — Raw CSV",
    f"  Rows         : {n_rows_raw:,}",
    f"  Conversations: {n_conv_raw:,}",
    "",
    "Step 2 — Remove ShareChat-excluded conversations",
    f"  Excluded in JSON (claude)  : {n_excluded_in_json:,}",
    f"  Of those found in CSV      : {n_excluded_in_csv:,}",
    f"  Conversations remaining    : {n_conv_after_excl:,}",
    f"  Rows remaining             : {n_rows_after_excl:,}",
    "",
    "Step 3 — 50% English word-content threshold (user ≥50% AND llm ≥50%)",
    f"  English (both sides >=50%) : {n_conv_english:,}  ← annotation input",
    f"  Non-English (either <50%)  : {n_conv_non_english:,}",
    f"  Ratio undefined (no text)  : {n_conv_nan:,}",
    "",
    "Output",
    f"  {OUT_CSV}",
    f"  Conversations : {n_conv_english:,}",
    f"  Rows          : {n_rows_english:,}",
]

with open(OUT_REPORT, "w") as f:
    f.write("\n".join(report_lines) + "\n")

for line in report_lines:
    print(line)
