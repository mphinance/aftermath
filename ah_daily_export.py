#!/usr/bin/env python3
"""
ah_daily_export.py: one-off export of the full post archive as per-ticker, per-day counts.

  python3 ah_daily_export.py > ah-daily-history.json

Same shape as the `daily` block in sentiment.json (date, posts, bull, bear, net), for every day since the
archive began. Counts only: no text, no authors. Ticker-days with fewer than 3 distinct authors are dropped,
the same floor the consumer applies. Reads data/ah_archive/posts.jsonl directly, so the 30-day in-memory
trim in ah_collect.py does not apply.
"""
import json, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import ah_sentiment as S

ARCH = Path(__file__).resolve().parent / "data" / "ah_archive" / "posts.jsonl"
MIN_AUTHORS = 3


def export(posts, now):
    daily = S.daily_series(posts, now, days=36500)
    authors = defaultdict(set)  # (ticker, day) -> distinct authors, used only for the floor, never emitted
    for p in posts:
        for tk in p["tickers"]:
            authors[(tk, (p["ts"] or "")[:10])].add(p["author"])
    out = {}
    for tk, rows in daily.items():
        kept = [r for r in rows if len(authors[(tk, r["date"])]) >= MIN_AUTHORS]
        if kept:
            out[tk] = kept
    return {"generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "daily": out}


def main():
    posts, seen = [], set()
    for line in ARCH.read_text(encoding="utf-8").splitlines():
        try:
            p = json.loads(line)
        except Exception:
            continue
        if p.get("id") not in seen:
            seen.add(p["id"])
            posts.append(p)
    json.dump(export(posts, datetime.now(timezone.utc)), sys.stdout, separators=(",", ":"))


if __name__ == "__main__":
    main()
