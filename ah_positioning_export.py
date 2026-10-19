#!/usr/bin/env python3
"""
ah_positioning_export.py: publish the positioning snapshots as api/positioning.json.

Reads data/ah_archive/positioning/*.json.gz (written by ah_positioning.py) and writes one aggregate file:
  { "generated_at": ..., "days": { "YYYY-MM-DD": { "NVDA": {owners, total_value, rank, chatroom_members, change_pct} } } }
Only tickers with 3+ owners. A ticker missing on a day means "not captured", never zero.
No usernames, ids, or owner samples: only the five fields above leave the archive.
"""
import gzip, json, os, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
SRC = BASE / "data" / "ah_archive" / "positioning"
MIN_OWNERS = 3


def build(src=SRC, now=None):
    days = {}
    for f in sorted(src.glob("*.json.gz")):
        try:
            rows = json.loads(gzip.open(f).read())["rows"]
        except Exception as e:  # one bad day must not hide the rest
            print(f"skip {f.name}: {e}", file=sys.stderr)
            continue
        day = {}
        for r in rows:
            owners = r.get("owners")
            if not r.get("ticker") or not isinstance(owners, int) or owners < MIN_OWNERS:
                continue
            day[r["ticker"]] = {"owners": owners, "total_value": r.get("value"), "rank": r.get("rank"),
                                "chatroom_members": r.get("chat_members"), "change_pct": r.get("chg_pct")}
        if day:
            days[f.name.removesuffix(".json.gz")] = day
    now = now or datetime.now(timezone.utc)
    return {"generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "days": days}


def main():
    out = build()
    if not out["days"]:
        print("no snapshots, not writing", file=sys.stderr)
        return 1
    # same publish dir as ah_collect.py; falls back to api/
    pub = os.environ.get("PUBLISH_DIR")
    outdir = Path(pub) if pub and Path(pub).is_dir() else BASE / "api"
    outdir.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=outdir, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))
    os.chmod(tmp, 0o644)  # nginx container must read it
    os.replace(tmp, outdir / "positioning.json")
    print(f"wrote positioning.json: {len(out['days'])} days")
    return 0


if __name__ == "__main__":
    sys.exit(main())
