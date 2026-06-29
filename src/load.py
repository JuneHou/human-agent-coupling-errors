"""Thin, memory-conscious loaders for the raw exploration datasets.

Datasets live under data/ (gitignored):
  data/wildchat-1m/data/*.parquet   — WildChat-1M, one row per conversation
  data/sharechat/*.csv              — ShareChat, one row per message (group by `url`)

These loaders stream rather than load-all, because the raw files are multi-GB.
"""
from __future__ import annotations
import csv, glob, sys
from pathlib import Path

import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[1]
WILDCHAT_DIR = REPO / "data" / "wildchat-1m" / "data"
SHARECHAT_DIR = REPO / "data" / "sharechat"
SHARECHAT_PLATFORMS = ["chatgpt", "claude", "grok", "perplexity", "gemini"]

csv.field_size_limit(sys.maxsize)  # plain_text / thinking can be huge


def wildchat_shards():
    return sorted(glob.glob(str(WILDCHAT_DIR / "*.parquet")))


def iter_wildchat(columns, batch_size=50_000):
    """Yield dict-of-lists batches from WildChat, reading only `columns`."""
    for f in wildchat_shards():
        pf = pq.ParquetFile(f)
        for batch in pf.iter_batches(columns=columns, batch_size=batch_size):
            yield batch.to_pydict()


def sharechat_path(platform: str) -> Path:
    return SHARECHAT_DIR / f"{platform}_results_final_language_filtered.csv"


def sharechat_header(platform: str):
    with open(sharechat_path(platform), newline="", encoding="utf-8", errors="replace") as fh:
        return next(csv.reader(fh))


def iter_sharechat_rows(platform: str):
    """Yield dict rows (message-level) for one ShareChat platform CSV."""
    path = sharechat_path(platform)
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        yield from csv.DictReader(fh)
