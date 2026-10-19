#!/usr/bin/env python3
"""
ah_positioning.py: daily snapshot of AfterHour's verified-owner leaderboard, kept as a time series.

Why: research/retail_signal_eval.py could test POSTING but not POSITIONING, because only two
hand-run leaderboard scrapes existed (2026-10-02, 2026-10-13). This builds the history that lets
"does verified-owner / dollars-held growth lead the stock?" be tested later. It reads; it publishes nothing.

  python3 ah_positioning.py               # today's snapshot (top --pages x 15 securities, in AfterHour's own trending order)
  python3 ah_positioning.py --pages 2     # quick check

Source : GET /stonks/security/leaderboard (public, unauthenticated; the gateway caps take at 15)
Output : data/ah_archive/positioning/YYYY-MM-DD.json.gz   (one file per UTC day; gitignored, server keeps history)
Order  : the leaderboard is AfterHour's trending order, NOT sorted by owners or value, so a name can drop out
         of the top 1,200 and reappear. A missing ticker on a day means "not captured", never "zero owners".
Rows   : rank, ticker, security id, type, ownerCount, totalValue (verified $ held), chatroom members, close,
         changePercent, marketCap. Owner samples (named people) are deliberately NOT stored.
A rerun on the same day overwrites that day's file. A run that comes back with fewer than 100 rows
does not write (a gateway hiccup must never read as "the crowd left").
"""
import argparse, gzip, json, os, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

import afterhour

BASE = Path(__file__).resolve().parent
OUT_DIR = BASE / "data" / "ah_archive" / "positioning"
URL = "https://api.afterhour.com/stonks/security/leaderboard?take=15&cursor={cursor}"
MIN_ROWS = 100


def row(item, rank):
    s = item.get("security") or {}
    sec = s.get("security") or {}
    px = s.get("price") or {}
    sess = px.get("session") or {}
    return {
        "rank": rank,
        "ticker": sec.get("tickerSymbol"),
        "id": sec.get("id"),
        "type": sec.get("type"),
        "owners": s.get("ownerCount"),
        "value": round(s["totalValue"], 2) if isinstance(s.get("totalValue"), (int, float)) else None,
        "chat_members": (sec.get("chatroom") or {}).get("memberCount"),
        "close": sess.get("close", px.get("price")),
        "chg_pct": sess.get("changePercent"),
        "mcap": s.get("marketCap"),
        "lb_change": item.get("change"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=80, help="15 securities per page (80 -> top 1,200, about 2 minutes)")
    args = ap.parse_args()

    rows, total = [], None
    for page in range(args.pages):
        try:
            d = afterhour._get(URL.format(cursor=page * 15))
        except Exception as e:  # keep what we have; the row floor decides whether it is usable
            print(f"page {page} failed: {e}", file=sys.stderr)
            break
        secs = (d or {}).get("securities") or []
        total = d.get("totalCount", total)
        if not secs:
            break
        base = len(rows)
        rows.extend([row(x, base + i + 1) for i, x in enumerate(secs)])
        time.sleep(0.8)

    seen, uniq = set(), []
    for r in rows:  # the gateway can repeat a security across page boundaries if the order shifts mid-run
        if r["ticker"] and r["id"] not in seen:
            seen.add(r["id"])
            uniq.append(r)
    dupes = len(rows) - len(uniq)
    rows = uniq
    now = datetime.now(timezone.utc)
    if len(rows) < min(MIN_ROWS, args.pages * 15):
        print(f"only {len(rows)} rows, not writing", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{now.date().isoformat()}.json.gz"
    payload = {"as_of": now.isoformat(timespec="seconds"), "source": "afterhour /stonks/security/leaderboard",
               "leaderboard_total": total, "n": len(rows), "dupes_dropped": dupes, "rows": rows}
    fd, tmp = tempfile.mkstemp(dir=OUT_DIR, suffix=".tmp")
    with os.fdopen(fd, "wb") as f, gzip.GzipFile(fileobj=f, mode="wb") as g:
        g.write(json.dumps(payload, separators=(",", ":")).encode())
    os.chmod(tmp, 0o644)
    os.replace(tmp, out)
    print(f"wrote {out.name}: {len(rows)} rows ({dupes} dupes dropped), leaderboard_total={total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
