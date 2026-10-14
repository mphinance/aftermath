#!/usr/bin/env python3
"""
tg_option_paths.py: capture real option PRICE PATHS for the contracts Telegram channels call out, so callouts can be
judged by what the contract actually did after the call (peak, drawdown, time to targets), not by hold-to-expiry.

Why capture: Yahoo's chart endpoint serves option contract bars, but 5-minute bars exist only while a contract is live
and on its expiry day; the next day they are gone, and daily bars vanish after roughly a week. So history cannot be
recovered later; this job must run every trading day AFTER THE CLOSE (cron 20:30 UTC, Mon-Fri) and keeps its own archive.

  python3 tg_option_paths.py capture            # fetch bars for every called-out contract still on Yahoo, merge into the archive
  python3 tg_option_paths.py capture --symbol SPXW261014C07735000
  python3 tg_option_paths.py backfill           # Alpaca historical bars for every call's evaluation session (needs .env_alpaca; local only)
  python3 tg_option_paths.py score
Archive: data/telegram_funnel/option_bars/<SYMBOL>.json  {symbol, b5:{epoch:[o,h,l,c,v]}, b1d:{epoch:[o,h,l,c,v]}, first_seen, last_fetched}
Public Yahoo chart endpoint only, serial with a delay, read-only.
"""
import argparse, json, sys, time, urllib.request, urllib.error
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
TF = BASE / "data" / "telegram_funnel"
ARCH = TF / "option_bars"
ROOTS = {"SPX": "SPXW", "NDX": "NDXP"}
ECHO = {"duplicate_echo", "cross_channel_echo"}


def occ(c):
    """Yahoo/OCC symbol for a parsed callout, or None."""
    if c.get("kind") != "option" or not (c.get("strike") and c.get("side") and c.get("expiry")):
        return None
    root = ROOTS.get(c["ticker"], c["ticker"])
    return f"{root}{c['expiry'].replace('-', '')[2:]}{'C' if c['side'] == 'call' else 'P'}{int(round(float(c['strike']) * 1000)):08d}"


def chart(sym, rng, interval):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval={interval}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (tg_option_paths; public read-only)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                res = json.load(r)["chart"]["result"]
            if not res:
                return {}
            q = res[0]["indicators"]["quote"][0]
            out = {}
            for i, t in enumerate(res[0].get("timestamp") or []):
                row = [q[k][i] if k in q and i < len(q[k]) else None for k in ("open", "high", "low", "close", "volume")]
                if row[3] is not None:
                    out[str(t)] = row
            return out
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10 * (attempt + 1)); continue
            return {}
        except Exception:
            time.sleep(1 + attempt)
    return {}


def candidates(today):
    calls = []
    for line in (TF / "calls.jsonl").open():
        if line.strip():
            c = json.loads(line)
            if c["kind"] == "option" and c["action"] == "open" and not (ECHO & set(c.get("parse_flags") or [])):
                calls.append(c)
    keep = {}
    for c in calls:
        s = occ(c)
        # still on Yahoo: not expired more than 1 day ago (5m bars) ; daily bars last ~a week, fetch those a little longer
        if s and c["expiry"] >= (today - timedelta(days=7)).isoformat():
            keep[s] = max(keep.get(s, ""), c["expiry"])
    return keep


def capture(only=None, delay=0.4):
    ARCH.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date()
    syms = {only: ""} if only else candidates(today)
    n5 = n1 = fresh = 0
    # contracts expiring today or tomorrow first: their 5m bars disappear within a day
    order = sorted(syms.items(), key=lambda kv: (abs((date.fromisoformat(kv[1]) - today).days) > 1 if kv[1] else False, kv[1], kv[0]))
    for i, (s, exp) in enumerate(order, 1):
        f = ARCH / f"{s}.json"
        cur = json.load(open(f)) if f.exists() else {"symbol": s, "b5": {}, "b1d": {}, "first_seen": today.isoformat()}
        b5 = chart(s, "5d", "5m"); time.sleep(delay)
        b1 = chart(s, "1mo", "1d"); time.sleep(delay)
        before = (len(cur["b5"]), len(cur["b1d"]))
        cur["b5"].update(b5); cur["b1d"].update(b1)
        cur["last_fetched"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if (len(cur["b5"]), len(cur["b1d"])) != before:
            fresh += 1
            f.write_text(json.dumps(cur, separators=(",", ":")))
        n5 += len(b5); n1 += len(b1)
        if i % 25 == 0:
            print(f"[{i}/{len(syms)}] {fresh} contracts updated", file=sys.stderr, flush=True)
    print(f"captured {len(syms)} contracts: {fresh} gained new bars ({n5} 5m, {n1} daily bars seen); archive holds {len(list(ARCH.glob('*.json')))}")


# ----------------------------------------------------------------------------- Alpaca historical backfill
import os


def alpaca_headers():
    """Credentials from env vars or ./.env_alpaca (KEY=value lines). Never printed, never committed (.env* is gitignored)."""
    kid, sec = os.environ.get("ALPACA_API_KEY_ID"), os.environ.get("ALPACA_API_SECRET_KEY")
    p = BASE / ".env_alpaca"
    if (not kid or not sec) and p.exists():
        kv = dict(l.strip().split("=", 1) for l in p.open() if "=" in l and not l.lstrip().startswith("#"))
        kid, sec = kv.get("ALPACA_API_KEY_ID"), kv.get("ALPACA_API_SECRET_KEY")
    return {"APCA-API-KEY-ID": kid, "APCA-API-SECRET-KEY": sec, "User-Agent": "tg_option_paths (read-only market data)"} if kid and sec else None


def alpaca_bars(headers, symbols, start_iso, end_iso, timeframe="5Min"):
    """{symbol: [bar,...]} for a list of OCC symbols (read-only historical option bars, paginated)."""
    out, token = {}, None
    while True:
        q = f"symbols={','.join(symbols)}&timeframe={timeframe}&start={start_iso}&end={end_iso}&limit=10000" + (f"&page_token={token}" if token else "")
        res = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(urllib.request.Request("https://data.alpaca.markets/v1beta1/options/bars?" + q, headers=headers), timeout=60) as r:
                    res = json.load(r); break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(8 * (attempt + 1)); continue
                print(f"alpaca HTTP {e.code} for {len(symbols)} symbols", file=sys.stderr); return out
            except Exception:
                time.sleep(2 + attempt)
        if res is None:
            return out
        for sym, bars in (res.get("bars") or {}).items():
            out.setdefault(sym, []).extend(bars)
        token = res.get("next_page_token")
        if not token:
            return out


def needed_day(c):
    """Which session a callout is judged on (same rule as scoring)."""
    t = datetime.fromisoformat(c["posted"].replace("Z", "+00:00")).astimezone(ET)
    s0 = sess(t.date())
    return t.date() if (s0 and s0[0] <= t.timestamp() < s0[1]) else next_session_date(t)


def capture_alpaca(delay=0.35, batch=60):
    hd = alpaca_headers()
    if not hd:
        print("no Alpaca credentials (.env_alpaca or ALPACA_API_* env vars)", file=sys.stderr); return
    ARCH.mkdir(parents=True, exist_ok=True)
    need = {}                                   # session date -> {symbol: [alt symbols]}
    for line in (TF / "calls.jsonl").open():
        if not line.strip():
            continue
        c = json.loads(line)
        if c["kind"] != "option" or c["action"] != "open" or (ECHO & set(c.get("parse_flags") or [])):
            continue
        s = occ(c)
        if not s:
            continue
        d = needed_day(c)
        if c["expiry"] < d.isoformat():
            continue
        f = ARCH / f"{s}.json"
        have = set()
        if f.exists():
            for t in json.load(open(f))["b5"]:
                have.add(datetime.fromtimestamp(int(t), timezone.utc).astimezone(ET).date().isoformat())
        if d.isoformat() in have:
            continue
        alt = s.replace("SPXW", "SPX", 1) if s.startswith("SPXW") else None
        need.setdefault(d.isoformat(), {})[s] = alt
    total = sum(len(v) for v in need.values())
    print(f"alpaca backfill: {total} contract-sessions over {len(need)} days", file=sys.stderr)
    got = miss = 0
    for di, (day, syms) in enumerate(sorted(need.items()), 1):
        d = date.fromisoformat(day); o, cl = sess(d)
        start = datetime.fromtimestamp(o, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        end = datetime.fromtimestamp(cl, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        keys = list(syms)
        for i in range(0, len(keys), batch):
            chunk = keys[i:i + batch]
            res = alpaca_bars(hd, chunk, start, end); time.sleep(delay)
            missing = [k for k in chunk if k not in res and syms[k]]
            if missing:                           # SPX monthlies use the SPX root, not SPXW
                alt = alpaca_bars(hd, [syms[k] for k in missing], start, end); time.sleep(delay)
                for k in missing:
                    if syms[k] in alt:
                        res[k] = alt[syms[k]]
            for k in chunk:
                bars = res.get(k)
                if not bars:
                    miss += 1; continue
                f = ARCH / f"{k}.json"
                cur = json.load(open(f)) if f.exists() else {"symbol": k, "b5": {}, "b1d": {}, "first_seen": day}
                for b in bars:
                    ts = int(datetime.fromisoformat(b["t"].replace("Z", "+00:00")).timestamp())
                    cur["b5"][str(ts)] = [b["o"], b["h"], b["l"], b["c"], b.get("v")]
                cur["source"] = "alpaca+yahoo"; cur["last_fetched"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                f.write_text(json.dumps(cur, separators=(",", ":"))); got += 1
        if di % 10 == 0:
            print(f"[{di}/{len(need)} days] {got} contract-sessions stored, {miss} without bars", file=sys.stderr, flush=True)
    print(f"alpaca backfill done: {got} stored, {miss} had no bars (not traded that session or not listed)")


# ----------------------------------------------------------------------------- scoring
from zoneinfo import ZoneInfo
import math, statistics, collections
ET = ZoneInfo("America/New_York")
WINDOW_MIN = 30                      # intraday calls: judge the first 30 minutes after the call
MAX_FILL_GAP_MIN = 15                # no print within 15 min of the post = illiquid, not scored
RULES = [("tp50_sl50", 0.50, 0.50), ("tp100_sl50", 1.00, 0.50), ("tp30_sl30", 0.30, 0.30)]
OPEN_T, CLOSE_T = (9, 30), (16, 0)


def sess(d):
    """Regular session [open, close) in epoch seconds for date d (ET), or None on weekends."""
    if d.weekday() >= 5:
        return None
    o = datetime(d.year, d.month, d.day, *OPEN_T, tzinfo=ET).timestamp()
    c = datetime(d.year, d.month, d.day, *CLOSE_T, tzinfo=ET).timestamp()
    return o, c


def next_session_date(t_et):
    d = t_et.date()
    s0 = sess(d)
    if s0 and t_et.timestamp() < s0[0]:
        return d                      # before the open: today's session
    d += timedelta(days=1)
    while sess(d) is None:
        d += timedelta(days=1)
    return d


def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(max(0, c - h), 3), round(min(1, c + h), 3)]


def path_metrics(bars, fill, quoted):
    """bars: [(start, o, h, l, c, v)] in time order, the evaluation window. Fill = open of the first bar."""
    hi = max(b[2] for b in bars); lo = min(b[3] for b in bars)
    out = {"fill": fill, "mfe_pct": round((hi / fill - 1) * 100, 1), "mae_pct": round((lo / fill - 1) * 100, 1),
           "end_ret_pct": round((bars[-1][4] / fill - 1) * 100, 1), "n_bars": len(bars),
           "volume": sum(b[5] or 0 for b in bars)}
    for name, tp, sl in RULES:
        res, ret = "none", out["end_ret_pct"]
        for b in bars:
            hit_sl, hit_tp = b[3] <= fill * (1 - sl), b[2] >= fill * (1 + tp)
            if hit_sl:                # same-bar tie counts as the stop (conservative)
                res, ret = "sl", -sl * 100; break
            if hit_tp:
                res, ret = "tp", tp * 100; break
        out[name] = res; out[name + "_ret"] = round(ret, 1)
    if quoted:
        out["quoted_vs_fill_pct"] = round((quoted / fill - 1) * 100, 1)
    return out


def score(delay_bars=0, write=True, hold_window=False):
    """hold_window=True: with a fill delay, keep the exposure at WINDOW_MIN minutes after the delayed fill (not post+WINDOW_MIN)."""
    calls = []
    for line in (TF / "calls.jsonl").open():
        if line.strip():
            c = json.loads(line)
            if c["kind"] == "option" and c["action"] == "open" and not (ECHO & set(c.get("parse_flags") or [])):
                calls.append(c)
    rows = []
    for c in calls:
        s = occ(c)
        f = ARCH / f"{s}.json" if s else None
        if not s:
            continue
        r = {"id": c["id"], "channel": c["channel"], "posted": c["posted"], "ticker": c["ticker"], "side": c["side"],
             "strike": c["strike"], "expiry": c["expiry"], "quoted_entry": c.get("entry_price"), "symbol": s}
        if not f.exists():
            r.update(status="no_bars", reason="contract not captured (older than Yahoo retains, or not listed)"); rows.append(r); continue
        b5 = sorted((int(t), *v) for t, v in json.load(open(f))["b5"].items())
        t = datetime.fromisoformat(c["posted"].replace("Z", "+00:00")).astimezone(ET)
        s0 = sess(t.date())
        intraday = bool(s0 and s0[0] <= t.timestamp() < s0[1])
        if intraday:
            r["category"] = "intraday"; start = t.timestamp(); end = start + WINDOW_MIN * 60
            day = t.date()
        else:
            r["category"] = "daily"; day = next_session_date(t); o, cl = sess(day); start, end = o, cl
        if c["expiry"] < day.isoformat():
            r.update(status="unscorable", reason="contract expired before the evaluation session"); rows.append(r); continue
        win = [b for b in b5 if start <= b[0] < end]
        if not win:
            # coarse fallback: the contract's DAILY bar for that session (Yahoo keeps these about a week). Not time-ordered:
            # for intraday calls the day's high/low may predate the post, so MFE is an upper bound and MAE a lower bound.
            b1d = json.load(open(f))["b1d"]
            dbar = None
            for tk, v in b1d.items():
                if datetime.fromtimestamp(int(tk), timezone.utc).astimezone(ET).date() == day:
                    dbar = v
            if dbar and dbar[1] is not None and dbar[2] is not None:
                o_, h_, l_, c_, vol = dbar
                q = c.get("entry_price")
                ref = q if q else o_
                r.update(status="day_view", session=day.isoformat(), d_open=o_, d_high=h_, d_low=l_, d_close=c_, d_volume=vol,
                         ref=ref, ref_is_quote=bool(q), quoted_in_day_range=(bool(q) and l_ * 0.9 <= q <= h_ * 1.1),
                         d_close_ret_pct=round((c_ / ref - 1) * 100, 1), d_mfe_upper_pct=round((h_ / ref - 1) * 100, 1),
                         d_mae_lower_pct=round((l_ / ref - 1) * 100, 1), thin=bool((vol or 0) < 20))
            else:
                r.update(status="no_bars", reason=f"no bars for the session {day} (older than Yahoo retains, or no trades)")
            rows.append(r); continue
        gap = (win[0][0] - start) / 60 if intraday else (win[0][0] - start) / 60
        if gap > MAX_FILL_GAP_MIN:
            r.update(status="unscorable", reason=f"illiquid: first print {gap:.0f} min after {'the post' if intraday else 'the open'}"); rows.append(r); continue
        if delay_bars:                    # a follower acts a few minutes after the post: fill on a later bar
            if hold_window and len(win) > delay_bars:
                t0 = win[delay_bars][0]
                lim = min(t0 + WINDOW_MIN * 60, sess(day)[1])
                win = [b for b in b5 if t0 <= b[0] < lim]
            else:
                win = win[delay_bars:]
            if not win:
                r.update(status="unscorable", reason="no bars after the fill delay"); rows.append(r); continue
        fill = win[0][1]
        gap_s = int(win[0][0] - start) if not delay_bars else None
        if not fill:
            r.update(status="unscorable", reason="no fill price"); rows.append(r); continue
        r.update(status="scored", session=day.isoformat(), fill_gap_s=(gap_s if intraday else None), truncated=(win[-1][0] + 300 < end - 300), **path_metrics(win, fill, c.get("entry_price")))
        rows.append(r)
    if not write:
        return rows
    with (TF / "option_paths.jsonl").open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    sc = [r for r in rows if r["status"] == "scored"]
    L = ["# Callout option paths: what the contract did after the call", "",
         f"{len(rows)} option opens with a parseable contract; {len(sc)} scored from captured 5-minute bars.",
         "Intraday calls: first 30 minutes after the call. Daily callouts (before the open, after the close, weekends): the whole next regular session. "
         "Fill = open of the first bar at or after the post (or the session open). Bars are trade prints (no bid/ask, no slippage or fees).", "",
         "## Coverage", *[f"- {k}: {v}" for k, v in collections.Counter(r["status"] for r in rows).most_common()], ""]
    for cat in ("intraday", "daily"):
        g = [r for r in sc if r["category"] == cat]
        if not g:
            continue
        L += [f"## {cat} (n={len(g)})", "",
              f"- median MFE {statistics.median(r['mfe_pct'] for r in g):+.0f}%, median MAE {statistics.median(r['mae_pct'] for r in g):+.0f}%, "
              f"median end-of-window return {statistics.median(r['end_ret_pct'] for r in g):+.0f}%, mean {statistics.mean(r['end_ret_pct'] for r in g):+.0f}%",
              f"- ended green: {sum(r['end_ret_pct'] > 0 for r in g)}/{len(g)} {wilson(sum(r['end_ret_pct'] > 0 for r in g), len(g))}",
              "", "| rule | TP first | SL first | neither | mean return |", "|---|---:|---:|---:|---:|"]
        for name, tp, sl in RULES:
            k = collections.Counter(r[name] for r in g)
            L.append(f"| +{int(tp*100)}% / -{int(sl*100)}% | {k['tp']} {wilson(k['tp'], len(g))} | {k['sl']} | {k['none']} | {statistics.mean(r[name + '_ret'] for r in g):+.1f}% |")
        L.append("")
    dv = [r for r in rows if r["status"] == "day_view"]
    if dv:
        n = len(dv); qd = [r for r in dv if r["ref_is_quote"]]
        gr = lambda xs, f: sum(1 for x in xs if f(x))
        L += [f"## Day view (coarse, n={n}): contracts called in roughly the last week, judged on the contract's daily bar", "",
              "Daily bars are not time-ordered. For calls posted during the session the day's high or low may predate the post, so peak is an UPPER bound and drawdown a LOWER bound. "
              "Reference price = the entry the channel quoted (the open when none was quoted).", "",
              f"- quoted entry inside that day's traded range (±10%): {gr(qd, lambda r: r['quoted_in_day_range'])}/{len(qd)} {wilson(gr(qd, lambda r: r['quoted_in_day_range']), len(qd))}",
              f"- day closed above the reference: {gr(dv, lambda r: r['d_close_ret_pct'] > 0)}/{n} {wilson(gr(dv, lambda r: r['d_close_ret_pct'] > 0), n)}; median close return {statistics.median(r['d_close_ret_pct'] for r in dv):+.0f}%",
              f"- day high reached +50% (upper bound): {gr(dv, lambda r: r['d_mfe_upper_pct'] >= 50)}/{n} {wilson(gr(dv, lambda r: r['d_mfe_upper_pct'] >= 50), n)}; +100%: {gr(dv, lambda r: r['d_mfe_upper_pct'] >= 100)}/{n}",
              f"- day low reached -50% (lower bound on drawdown): {gr(dv, lambda r: r['d_mae_lower_pct'] <= -50)}/{n} {wilson(gr(dv, lambda r: r['d_mae_lower_pct'] <= -50), n)}",
              f"- thin (day volume under 20 contracts): {gr(dv, lambda r: r['thin'])}/{n}", ""]
        for cat in ("intraday", "daily"):
            g = [r for r in dv if r["category"] == cat]
            if g:
                L.append(f"- {cat} calls: n={len(g)}, median close return {statistics.median(r['d_close_ret_pct'] for r in g):+.0f}%, day high >= +50%: {gr(g, lambda r: r['d_mfe_upper_pct'] >= 50)}/{len(g)}")
        L.append("")
    (BASE / "reports" / "analysis" / "option_paths.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["capture", "backfill", "score"])
    ap.add_argument("--symbol", default="")
    ap.add_argument("--delay-bars", type=int, default=0, help="score with the fill N five-minute bars after the post")
    a = ap.parse_args()
    capture(a.symbol or None) if a.cmd == "capture" else capture_alpaca() if a.cmd == "backfill" else score(a.delay_bars)
