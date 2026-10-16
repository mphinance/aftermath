#!/usr/bin/env python3
"""
tg_live.py: near-real-time callout feed. Passive: public t.me previews and Yahoo public chart bars only.

Each run (cron every 3 minutes during extended market hours, see scripts/run_live.sh):
  1. pull page 1 (newest ~20 posts) of every public channel behind the flagged accounts, append new ones to the archive
  2. re-parse callouts (tg_calls.py)
  3. for the last WINDOW_H hours of callouts, attach live tape: option mark and path since the call, underlying move
  4. write api/funnel-live.json (and publish it atomically to $PUBLISH_DIR when that directory exists)

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
from build_funnel_calls import DISCLAIMER, OUTCOME_KEYS, is_public, read_jsonl, trunc
from tg_option_paths import chart, occ

BASE = Path(__file__).resolve().parent
TF = BASE / "data" / "telegram_funnel"
ARCH = TF / "posts_archive.jsonl"
OUT = BASE / "api" / "funnel-live.json"
ET = ZoneInfo("America/New_York")
WINDOW_H = 72
MAX_OPT = 150
MAX_UND = 80
ECHO = {"duplicate_echo", "cross_channel_echo"}
YSYM = {"SPX": "^SPX", "NDX": "^NDX", "VIX": "^VIX", "RUT": "^RUT", "DJX": "^DJI", "XSP": "^XSP"}


def market_state(now=None):
    n = (now or datetime.now(timezone.utc)).astimezone(ET)
    if n.weekday() >= 5:
        return "closed"
    m = n.hour * 60 + n.minute
    return "open" if 570 <= m < 960 else "pre" if 240 <= m < 570 else "after" if 960 <= m < 1200 else "closed"


def handles():
    hs = {}
    for acc in json.load(open(BASE / "accounts.json")):
        for raw in acc.get("telegram_links", []):
            h = raw.rstrip("/").split("/")[-1]
            if h and not h.startswith("+"):
                hs[h.lower()] = h
    return sorted(hs.values())


def pull_new():
    seen = set()
    if ARCH.exists():
        seen = {json.loads(l)["id"] for l in ARCH.open() if l.strip()}
    hs = handles()
    with ThreadPoolExecutor(6) as ex:
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


def bars_since(bars, t0):
    """Sorted [(epoch, close, high, low)] for bars at/after t0 (a bar covers the 5 minutes after its stamp)."""
    rows = sorted((int(k), v) for k, v in bars.items())
    return [(t, v[3], v[1] if v[1] is not None else v[3], v[2] if v[2] is not None else v[3]) for t, v in rows if t + 300 > t0]


def pct(a, b):
    return None if not a or not b else round((b / a - 1) * 100, 1)


def sample(xs, n=48):
    if len(xs) <= n:
        return xs
    step = (len(xs) - 1) / (n - 1)
    return [xs[round(i * step)] for i in range(n)]


def opt_live(c, bars, daily=None):
    t0 = datetime.fromisoformat(c["posted"]).timestamp()
    seg = bars_since(bars, t0)
    if not seg:     # no intraday bars (pre-open, or Yahoo only serves them on the live session): last daily close vs the quote
        last = sorted((int(k), v) for k, v in (daily or {}).items())
        if not last or not c.get("entry_price"):
            return None
        return {"now": round(last[-1][1][3], 2), "last_t": last[-1][0], "vs_quote_pct": pct(c["entry_price"], last[-1][1][3]), "daily_only": True}
    first, last = seg[0][1], seg[-1][1]
    hi, lo = max(s[2] for s in seg), min(s[3] for s in seg)
    out = {"now": round(last, 2), "at_call": round(first, 2), "chg_pct": pct(first, last),
           "peak_pct": pct(first, hi), "low_pct": pct(first, lo), "last_t": seg[-1][0],
           "path": [round(s[1], 2) for s in sample(seg)]}
    if c.get("entry_price"):
        out["vs_quote_pct"] = pct(c["entry_price"], last)
    return out


def und_live(c, bars):
    t0 = datetime.fromisoformat(c["posted"]).timestamp()
    seg = bars_since(bars, t0)
    if not seg:
        return None
    return {"now": round(seg[-1][1], 2), "at_call": round(seg[0][1], 2), "chg_pct": pct(seg[0][1], seg[-1][1]), "last_t": seg[-1][0]}


def build(fetch_stats):
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(hours=WINDOW_H)).isoformat()
    today = now.astimezone(ET).date().isoformat()
    calls = [c for c in read_jsonl(TF / "calls.jsonl") if is_public(c.get("channel")) and (c.get("posted") or "") >= cutoff]
    calls.sort(key=lambda c: c.get("posted") or "", reverse=True)
    outcomes = {}
    for o in read_jsonl(TF / "outcomes.jsonl"):
        for i in o.get("ids") or []:
            outcomes[i] = o

    opt_targets = [c for c in calls if c["kind"] == "option" and c["action"] == "open" and not (ECHO & set(c.get("parse_flags") or []))
                   and occ(c) and c["expiry"] >= today][:MAX_OPT]
    tickers = []
    for c in calls:
        if c.get("ticker") and c["ticker"] not in tickers:
            tickers.append(c["ticker"])
    jobs = [("o", occ(c)) for c in opt_targets] + [("u", t) for t in tickers[:MAX_UND]]
    jobs = list(dict.fromkeys(jobs))
    with ThreadPoolExecutor(8) as ex:
        got = dict(zip(jobs, ex.map(lambda j: chart(YSYM.get(j[1], j[1]) if j[0] == "u" else j[1], "5d", "5m"), jobs)))
    need = [j for j in jobs if j[0] == "o" and not got[j]]
    with ThreadPoolExecutor(8) as ex:
        daily = dict(zip(need, ex.map(lambda j: chart(j[1], "1mo", "1d"), need)))

    rows, heat = [], {}
    for c in calls:
        r = {k: c.get(k) for k in ("channel", "posted", "ticker", "kind", "side", "strike", "expiry", "entry_price", "action", "result_pct")}
        r["text"] = trunc(c.get("text"))
        if c.get("parse_flags"):
            r["parse_flags"] = c["parse_flags"]
        o = outcomes.get(c.get("id"))
        if o:
            r["outcome"] = {k: o[k] for k in OUTCOME_KEYS if k in o}
        live = {}
        if c["kind"] == "option" and c["action"] == "open" and occ(c) and ("o", occ(c)) in got:
            ol = opt_live(c, got[("o", occ(c))], daily.get(("o", occ(c))))
            if ol:
                live["opt"] = ol
        if ("u", c.get("ticker")) in got:
            ul = und_live(c, got[("u", c["ticker"])])
            if ul:
                live["und"] = ul
        if live:
            r["live"] = live
        rows.append(r)
        if not (ECHO & set(c.get("parse_flags") or [])) and c["action"] == "open":
            h = heat.setdefault(c["ticker"], {"ticker": c["ticker"], "n_60m": 0, "n_24h": 0, "chans": set(), "calls": 0, "puts": 0})
            age = (now - datetime.fromisoformat(c["posted"])).total_seconds()
            h["n_60m"] += age <= 3600
            if age <= 86400:
                h["n_24h"] += 1; h["chans"].add(c["channel"])
                h["calls"] += c.get("side") == "call"; h["puts"] += c.get("side") == "put"
    hot = sorted(({**h, "chans": len(h["chans"])} for h in heat.values() if h["n_24h"]), key=lambda h: (-h["n_60m"], -h["n_24h"]))[:14]
    for h in hot:
        u = next((r["live"]["und"] for r in rows if r["ticker"] == h["ticker"] and (r.get("live") or {}).get("und")), None)
        if u:
            h["und_now"] = u["now"]
    new, ok, total = fetch_stats
    return {"source": "AfterMath live feed over public Telegram channel posts and Yahoo public 5-minute bars (passive, read-only)",
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "disclaimer": DISCLAIMER,
            "market": market_state(now), "window_hours": WINDOW_H, "refresh_hint_sec": 60,
            "channels_polled": ok, "channels_total": total, "new_posts_this_run": new,
            "live_note": "Option 'now' and 'at_call' are the last and first traded 5-minute closes on Yahoo at or after the post, not the channel's quoted entry. Thin contracts can be stale; last_t is the last bar time. Not advice.",
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
    print(f"live feed: {out['count']} callouts, {sum(1 for r in out['calls'] if (r.get('live') or {}).get('opt'))} with option tape, {stats[0]} new posts, market {out['market']}")
    if not a.no_publish:
        publish(OUT)


if __name__ == "__main__":
    main()
