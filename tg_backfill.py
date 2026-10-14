#!/usr/bin/env python3
"""
tg_backfill.py: one-off deep history pull for every PUBLIC Telegram channel behind the flagged accounts.
Passive (public t.me/s/<handle> previews, 20 posts per page walking back with ?before=<id>), serial, ~1s per
page. Appends new posts to data/telegram_funnel/posts_archive.jsonl (deduped by post id). Re-run tg_calls.py after.

  python3 tg_backfill.py --pages 40            # up to 800 posts per channel
  python3 tg_backfill.py --pages 40 --only stockmarketvault
"""
import argparse, json, sys
from pathlib import Path
import tg_recon

BASE = Path(__file__).resolve().parent
ARCH = BASE / "data" / "telegram_funnel" / "posts_archive.jsonl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=40)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    seen = set()
    if ARCH.exists():
        seen = {json.loads(l)["id"] for l in ARCH.open() if l.strip()}
    handles = {}
    for acc in json.load(open(BASE / "accounts.json")):
        for raw in acc.get("telegram_links", []):
            h = raw.rstrip("/").split("/")[-1]
            if h and not h.startswith("+"):
                handles[h.lower()] = h
    todo = [h for k, h in sorted(handles.items()) if not a.only or a.only.lower() in k]
    total = 0
    for i, h in enumerate(todo, 1):
        ps = tg_recon.posts(h, a.pages)
        new = [p for p in ps if p.get("id") and p["id"] not in seen]
        with ARCH.open("a") as f:
            for p in new:
                seen.add(p["id"])
                f.write(json.dumps({**p, "channel": "t.me/" + h.lower(), "first_seen": "deep_backfill"}, ensure_ascii=False) + "\n")
        total += len(new)
        print(f"[{i}/{len(todo)}] {h}: {len(ps)} fetched, {len(new)} new", file=sys.stderr, flush=True)
    print(f"done: {total} new posts")


if __name__ == "__main__":
    main()
