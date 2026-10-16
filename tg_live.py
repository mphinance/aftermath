#!/usr/bin/env python3
"""
tg_live.py: near-real-time callout feed. Passive: public t.me previews only. No scoring, no price data.

Each run (cron every 3 minutes during extended market hours, see scripts/run_live.sh):
  1. pull page 1 (newest ~20 posts) of every public channel behind the flagged accounts, append new ones to the archive
  2. re-parse callouts (tg_calls.py)
  3. write api/funnel-live.json (and publish it atomically to $PUBLISH_DIR when that directory exists)

  python3 tg_live.py                 # one run
  python3 tg_live.py --market-hours  # no-op outside 08:00-17:00 ET Mon-Fri (what cron uses)
  python3 tg_live.py --no-fetch      # rebuild from the archive without touching t.me
"""
import argparse, json, os, subprocess, sys, shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import tg_recon
from build_funnel_calls import DISCLAIMER, is_public, read_jsonl, trunc

BASE = Path(__file__).resolve().parent
TF = BASE / "data" / "telegram_funnel"
ARCH = TF / "posts_archive.jsonl"
OUT = BASE / "api" / "funnel-live.json"
ET = ZoneInfo("America/New_York")
WINDOW_H = 72
ECHO = {"duplicate_echo", "cross_channel_echo"}


def market_state(now=None):
    n = (now or datetime.now(timezone.utc)).astimezone(ET)
    if n.weekday() >= 5:
        return "closed"
    m = n.hour * 60 + n.minute
    return "open" if 570 <= m < 960 else "pre" if 240 <= m < 570 else "after" if 960 <= m < 1200 else "closed"


def alive():
    """Lowercased handles the last recon snapshot found alive; None when there is no snapshot."""
    try:
        return {c["link"].rstrip("/").split("/")[-1].lower() for c in json.load(open(TF / "recon.json"))["channels"] if c.get("alive")}
    except Exception:
        return None


def handles():
    live = alive()
    hs = {}
    for acc in json.load(open(BASE / "accounts.json")):
        for raw in acc.get("telegram_links", []):
            h = raw.rstrip("/").split("/")[-1]
            if h and not h.startswith("+") and (live is None or h.lower() in live):
                hs[h.lower()] = h
    return sorted(hs.values())


def pull_new():
    seen = set()
    if ARCH.exists():
        seen = {json.loads(l)["id"] for l in ARCH.open() if l.strip()}
    hs = handles()
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda h: (h, tg_recon.posts(h, 1)), hs))
    new = ok = 0
    with ARCH.open("a") as f:
        for h, ps in res:
            ok += bool(ps)
            for p in ps:
                if p.get("id") and p["id"] not in seen:
                    seen.add(p["id"]); new += 1
                    f.write(json.dumps({**p, "channel": "t.me/" + h.lower(), "first_seen": "live"}, ensure_ascii=False) + "\n")
    return new, ok, len(hs)


def build(fetch_stats):
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(hours=WINDOW_H)).isoformat()
    calls = [c for c in read_jsonl(TF / "calls.jsonl") if is_public(c.get("channel")) and (c.get("posted") or "") >= cutoff]
    calls.sort(key=lambda c: c.get("posted") or "", reverse=True)
    rows, heat = [], {}
    for c in calls:
        r = {k: c.get(k) for k in ("channel", "posted", "ticker", "kind", "side", "strike", "expiry", "entry_price", "action", "result_pct")}
        r["text"] = trunc(c.get("text"))
        if c.get("parse_flags"):
            r["parse_flags"] = c["parse_flags"]
        rows.append(r)
        if not (ECHO & set(c.get("parse_flags") or [])) and c["action"] == "open":
            h = heat.setdefault(c["ticker"], {"ticker": c["ticker"], "n_60m": 0, "n_24h": 0, "chans": set(), "calls": 0, "puts": 0})
            age = (now - datetime.fromisoformat(c["posted"])).total_seconds()
            h["n_60m"] += age <= 3600
            if age <= 86400:
                h["n_24h"] += 1; h["chans"].add(c["channel"])
                h["calls"] += c.get("side") == "call"; h["puts"] += c.get("side") == "put"
    hot = sorted(({**h, "chans": len(h["chans"])} for h in heat.values() if h["n_24h"]), key=lambda h: (-h["n_60m"], -h["n_24h"]))[:14]
    new, ok, total = fetch_stats
    return {"source": "AfterMath live feed over public Telegram channel posts (passive, read-only, unscored)",
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "disclaimer": DISCLAIMER,
            "market": market_state(now), "window_hours": WINDOW_H, "refresh_hint_sec": 60,
            "channels_polled": ok, "channels_total": total, "new_posts_this_run": new,
            "live_note": "Raw parsed callouts, newest first. Not scored here; outcomes live in funnel-calls.json and /scorecard. Not advice.",
            "count": len(rows), "hot_tickers": hot, "calls": rows}


def publish(path):
    pub = os.environ.get("PUBLISH_DIR", "/home/mph/apps/ah-portal/api")
    if os.path.isdir(pub):
        tmp = os.path.join(pub, ".funnel-live.json.tmp")
        shutil.copyfile(path, tmp)
        os.replace(tmp, os.path.join(pub, "funnel-live.json"))
        print("published funnel-live.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--market-hours", action="store_true")
    ap.add_argument("--no-publish", action="store_true")
    a = ap.parse_args()
    if a.market_hours:
        n = datetime.now(ET)
        if n.weekday() >= 5 or not 8 <= n.hour < 17:
            print("outside market hours, skipping"); return
    stats = (0, 0, 0) if a.no_fetch else pull_new()
    if not a.no_fetch and stats[1] == 0:
        print("no channel responded; keeping previous feed"); sys.exit(1)
    subprocess.run([sys.executable, str(BASE / "tg_calls.py")], check=True, stdout=subprocess.DEVNULL)
    out = build(stats)
    if not out["calls"]:
        print("empty feed; not writing"); sys.exit(1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False))
    print(f"live feed: {out['count']} callouts, {stats[0]} new posts, market {out['market']}")
    if not a.no_publish:
        publish(OUT)


if __name__ == "__main__":
    main()
