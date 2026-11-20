#!/usr/bin/env python3
"""Pull the AfterHour posts of every trader in trader_watchlist.json (read-only, serial).

Writes data/traders/<handle-slug>/posts.json:
    {"handle", "profile_id", "fetched_at", "total", "posts": [...]}
Reuses afterhour.fetch_all_posts / normalize; the stored profile_id is preferred and the
page resolver (afterhour.profile_id) is only a logged fallback.

  python3 pull_trader_posts.py --all
  python3 pull_trader_posts.py --handle Cynce --dry-run
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import afterhour

BASE = Path(__file__).resolve().parent
WATCHLIST = BASE / "trader_watchlist.json"
OUT = BASE / "data" / "traders"


def slug(handle: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", handle.lower()).strip("-")


def load_watchlist(path: Path = WATCHLIST) -> list[dict]:
    return json.loads(Path(path).read_text())


def pull_trader(entry: dict, out_dir: Path = OUT, dry_run: bool = False, limit: int | None = None) -> dict:
    """Fetch and (unless dry_run) write one trader. Returns a summary dict."""
    handle = entry["handle"]
    pid = entry.get("profile_id")
    if not pid:
        print(f"[{handle}] no stored profile_id, falling back to resolver", file=sys.stderr)
        pid = afterhour.profile_id(handle)
    print(f"[{handle}] profile id: {pid}")
    items = afterhour.fetch_all_posts(pid)
    total = len(items)
    posts = sorted((afterhour.normalize(i) for i in items), key=lambda p: p.get("created_at") or "")
    if limit is not None:
        posts = posts[-limit:] if limit > 0 else []  # keep the newest N
    summary = {"handle": handle, "profile_id": pid, "total": total, "written": 0}
    if dry_run:
        print(f"[{handle}] feed total: {total}; dry run, nothing written")
        return summary
    payload = {
        "handle": handle,
        "profile_id": pid,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": total,
        "posts": posts,
    }
    d = Path(out_dir) / slug(handle)
    d.mkdir(parents=True, exist_ok=True)
    (d / "posts.json").write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    summary["written"] = len(posts)
    print(f"[{handle}] feed total: {total}; written: {len(posts)} -> {d / 'posts.json'}")
    return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--handle", help="pull one watchlisted trader")
    g.add_argument("--all", action="store_true", help="pull every watchlisted trader")
    ap.add_argument("--dry-run", action="store_true", help="resolve and count only, write nothing")
    ap.add_argument("--limit", type=int, help="keep only the newest N posts (smoke runs)")
    ap.add_argument("--watchlist", default=str(WATCHLIST))
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)

    entries = load_watchlist(Path(a.watchlist))
    if a.handle:
        entries = [e for e in entries if e["handle"].lower() == a.handle.lower()]
        if not entries:
            print(f"handle {a.handle!r} not in watchlist", file=sys.stderr)
            return 2
    failed = 0
    for e in entries:
        try:
            pull_trader(e, Path(a.out), a.dry_run, a.limit)
        except Exception as ex:  # one trader failing must not abort the others
            failed += 1
            print(f"[{e.get('handle')}] FAIL: {ex}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
