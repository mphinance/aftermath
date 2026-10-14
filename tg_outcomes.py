#!/usr/bin/env python3
"""Score Telegram funnel option callouts against the real underlying tape.

Input : data/telegram_funnel/calls.jsonl (from tg_calls.py)
Output: data/telegram_funnel/outcomes.jsonl, reports/analysis/funnel_outcomes.md

ASSUMPTIONS (read these before trusting any number)
  * No option price history is available. Option P&L is therefore the
    HOLD-TO-EXPIRY INTRINSIC number: (max(0, S-K) or max(0, K-S) at the
    expiry-date close minus the quoted entry premium) * 100 per contract.
    That is the clean, reproducible figure. It is not what a trader who exited
    early would have booked.
  * 'touched_breakeven' = the underlying's high (calls) / low (puts) on any bar
    between the post and expiry reached strike+entry (calls) / strike-entry
    (puts). This is an OPTIMISTIC UPPER BOUND (assumes a perfect exit at the
    extreme and ignores time value/IV/spread). It is not a P&L.
  * Entry premium is taken as quoted (a fill nobody can verify). Slippage on
    cheap 0DTE lottos is ignored, which flatters the channels.
  * Expiry null: tg_calls.py leaves it null on 0DTE-style posts; treated as the
    post date (UTC date of the post, which equals the ET date for market-hours
    posts). Posts made after the close or on a non-trading day roll to the next
    trading session's bar.
  * SPX/SPXW priced off ^GSPC (cash index, cash-settled). Others off the
    ticker itself. Prices are split/dividend UNADJUSTED where the source allows.
  * Dedupe: one scored row per (channel, ticker, side, strike, expiry, posted
    date). Pooled 'distinct contracts' further collapse across channels on
    (ticker, side, strike, expiry, posted date).
  * Records whose text is actually a close (parser tagged it 'open') are
    marked unscorable, not scored.

Price source order: local files (api/ticker/<SYM>.json history,
data/leaderboard/historic_prices_sample.json) if they cover the bars needed,
else Yahoo Finance public chart endpoint (stdlib urllib, serial, >=0.3s sleep,
read-only). 5m bars are used for the breakeven window when the post is within
the last ~58 days (Yahoo's 5m limit is 60 days); otherwise daily bars.
Fetched bars are cached in data/telegram_funnel/price_cache/.
"""
import json, os, re, sys, time, statistics, collections, urllib.request, urllib.parse
from datetime import datetime, date, timedelta, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
CALLS = os.path.join(ROOT, "data/telegram_funnel/calls.jsonl")
OUT_JSONL = os.path.join(ROOT, "data/telegram_funnel/outcomes.jsonl")
OUT_MD = os.path.join(ROOT, "reports/analysis/funnel_outcomes.md")
CACHE = os.path.join(ROOT, "data/telegram_funnel/price_cache")
TODAY = date.fromisoformat(os.environ.get("TG_TODAY", "2026-10-14"))
MIN_N = 5
YMAP = {"SPX": "^GSPC", "SPXW": "^GSPC", "NDX": "^NDX", "RUT": "^RUT", "VIX": "^VIX"}
UA = {"User-Agent": "Mozilla/5.0"}
_last = [0.0]
_mem = {}


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def http_json(url):
    wait = 0.4 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def yahoo(sym, interval):
    """Return list of bars {t (epoch), d (exchange date iso), o,h,l,c} or None."""
    key = (sym, interval)
    if key in _mem:
        return _mem[key]
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "%s_%s.json" % (sym.replace("^", "_"), interval))
    bars = None
    if os.path.exists(path):
        c = json.load(open(path))
        if c.get("fetched") == TODAY.isoformat() or c.get("bars") is None and c.get("fetched") == TODAY.isoformat():
            bars = c["bars"]
            _mem[key] = bars
            return bars
    p1 = int(datetime(2026, 5, 28, tzinfo=timezone.utc).timestamp())
    if interval != "1d":
        p1 = int((datetime.now(timezone.utc) - timedelta(days=58)).timestamp())
    p2 = int(datetime.now(timezone.utc).timestamp()) + 86400
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?%s" % (
        urllib.parse.quote(sym), urllib.parse.urlencode(
            {"period1": p1, "period2": p2, "interval": interval, "includePrePost": "false"}))
    try:
        j = http_json(url)
        res = j["chart"]["result"][0]
        off = res["meta"].get("gmtoffset", -14400)
        q = res["indicators"]["quote"][0]
        bars = []
        for i, t in enumerate(res.get("timestamp") or []):
            if q["close"][i] is None or q["high"][i] is None:
                continue
            d = datetime.fromtimestamp(t + off, tz=timezone.utc).date().isoformat()
            bars.append({"t": t, "d": d, "o": q["open"][i], "h": q["high"][i],
                         "l": q["low"][i], "c": q["close"][i]})
    except Exception as e:
        print("  price fetch failed %s %s: %s" % (sym, interval, e), file=sys.stderr)
        bars = None
    json.dump({"fetched": TODAY.isoformat(), "source": "yahoo", "bars": bars}, open(path, "w"))
    _mem[key] = bars
    return bars


def local_daily(sym):
    """Daily bars from local files, or None."""
    out = []
    for p in (os.path.join(ROOT, "api/ticker/%s.json" % sym),):
        if os.path.exists(p):
            try:
                h = json.load(open(p)).get("history")
                rows = h.get("bars") if isinstance(h, dict) else h
                for b in rows or []:
                    out.append(b)
            except Exception:
                pass
    if not out:
        try:
            d = json.load(open(os.path.join(ROOT, "data/leaderboard/historic_prices_sample.json")))
            out = d["history"].get(sym, {}).get("bars", [])
        except Exception:
            pass
    bars = []
    for b in out:
        try:
            ts = b.get("timestamp") or b.get("t") or b.get("date")
            bars.append({"t": 0, "d": str(ts)[:10], "o": b["open"], "h": b["high"], "l": b["low"], "c": b["close"]})
        except Exception:
            pass
    return bars or None


def daily_bars(sym, need_from, need_to):
    ysym = YMAP.get(sym, sym)
    if ysym == sym:  # local only for plain equities/ETFs
        lb = local_daily(sym)
        if lb and lb[0]["d"] <= need_from and lb[-1]["d"] >= need_to:
            return lb, "local"
    b = yahoo(ysym, "1d")
    return b, "yahoo"


def rolling_expiry(x):
    """Effective expiry date or (None, reason). Parser-computed expiry is trusted.
    Null expiry is same-day only when the parser tagged expiry_0dte_tag."""
    fl = set(x.get("parse_flags") or [])
    if x["expiry"]:
        return date.fromisoformat(x["expiry"]), None
    if "expiry_0dte_tag" in fl:
        return parse_ts(x["posted"]).date(), "expiry null with 0DTE tag, same day"
    return None, "no expiry (unknown, not assumed 0DTE)"


SKIP_FLAGS = ["duplicate_echo", "cross_channel_echo", "expiry_before_post", "entry_implausible",
              "posted_date_suspect", "spread_suspect", "ticker_list", "expiry_far", "entry_below_intrinsic"]


def entry_below_intrinsic(g, bars):
    """Impossible quote screen. If, even at the best print of the post day (day low for calls, day high for puts),
    the contract's intrinsic value exceeds the quoted premium by more than a wide margin, the quote cannot be a real
    fill for that strike: it is a mis-parsed strike (1750 read as 175), a wrong ticker or a replayed old post. Such rows
    would otherwise score as 200x winners and dominate the mean. Conservative: premium below intrinsic is an arbitrage."""
    day = next((b for b in bars if b["d"] == g["posted"][:10]), None)
    if day is None or g.get("entry_price") is None:
        return False
    K, e = g["strike"], g["entry_price"]
    intr = (day["l"] - K) if g["side"] == "call" else (K - day["h"])
    return intr > 1.5 * e + 0.5


def is_close_text(t):
    return bool(re.match(r"^\W*(closed|exit|exited|sold|stopped)\b", t, re.I))


def score_group(g, bars, src):
    K, side, entry = g["strike"], g["side"], g["entry_price"]
    exp = date.fromisoformat(g["expiry_effective"])
    post = parse_ts(g["posted"])
    ebar = None
    for b in bars:
        if b["d"] == exp.isoformat():
            ebar = b
    if ebar is None:
        return {"status": "unscorable", "reason": "no underlying bar on expiry date %s" % exp}
    S = ebar["c"]
    intr = max(0.0, S - K) if side == "call" else max(0.0, K - S)
    r = {"status": "scored", "price_source": src, "underlying_close_at_expiry": round(S, 4),
         "intrinsic": round(intr, 4), "worthless": intr == 0.0}
    # breakeven-touch window
    be = None
    if entry is not None:
        be = K + entry if side == "call" else K - entry
        r["breakeven_level"] = round(be, 4)
        r["pnl_per_contract"] = round((intr - entry) * 100, 2)
        r["return_multiple"] = round(intr / entry, 4) if entry > 0 else None
        r["return_pct"] = round((intr / entry - 1) * 100, 2) if entry > 0 else None
        r["win"] = intr > entry
        # window
        ysym = YMAP.get(g["ticker"], g["ticker"])
        intra = None
        if (TODAY - post.date()).days <= 55:
            intra = yahoo(ysym, "5m")
        touched, win_src = None, "daily"
        if intra:
            seg = [b for b in intra if b["t"] >= post.timestamp() - 300 and b["d"] <= exp.isoformat()]
            if seg:
                win_src = "5m"
                touched = (max(b["h"] for b in seg) >= be) if side == "call" else (min(b["l"] for b in seg) <= be)
        if touched is None:
            seg = [b for b in bars if post.date().isoformat() <= b["d"] <= exp.isoformat()]
            if seg:
                touched = (max(b["h"] for b in seg) >= be) if side == "call" else (min(b["l"] for b in seg) <= be)
        r["touched_breakeven_optimistic"] = touched
        r["touch_window"] = win_src
    else:
        r["reason"] = "no entry_price: intrinsic scored, P&L not computable"
    return r


def med(v):
    return statistics.median(v) if v else None


def mean(v):
    return statistics.fmean(v) if v else None


def stats(rows):
    """rows = scored rows with entry_price (return_pct present)."""
    pr = [r for r in rows if r.get("return_pct") is not None]
    n = len(pr)
    if not n:
        return {"n": 0}
    rets = [r["return_pct"] for r in pr]
    return {"n": n, "win": sum(1 for r in pr if r["win"]) / n,
            "med": med(rets), "mean": mean(rets),
            "zero": sum(1 for r in pr if r["worthless"]) / n,
            "touch": (sum(1 for r in pr if r.get("touched_breakeven_optimistic")) /
                      max(1, sum(1 for r in pr if r.get("touched_breakeven_optimistic") is not None))),
            "pnl_sum": sum(r["pnl_per_contract"] for r in pr)}


def fmt(x, p=1, pct=False):
    if x is None:
        return "-"
    return ("%.*f%%" % (p, x * 100)) if pct else ("%.*f" % (p, x))


def main():
    recs = [json.loads(l) for l in open(CALLS) if l.strip()]
    opens = [x for x in recs if x["action"] == "open" and x["kind"] == "option"]
    # group
    groups = collections.OrderedDict()
    rows_pre = []
    rec_key = {}  # open record id -> group key (for pairing closes)
    for x in sorted(opens, key=lambda r: r["posted"]):
        fl = set(x.get("parse_flags") or [])
        exp, note = rolling_expiry(x)
        base = {"ids": [x["id"]], "channel": x["channel"], "ticker": x["ticker"], "side": x["side"],
                "strike": x["strike"], "expiry_effective": exp.isoformat() if exp else None, "expiry_note": note,
                "posted": x["posted"], "entry_price": x["entry_price"], "n_posts": 1, "text": x["text"][:140],
                "parse_flags": sorted(fl)}
        hit = [f for f in SKIP_FLAGS if f in fl]
        if hit:
            base.update(status="excluded", reason="parse_flag: " + hit[0], exclude_flag=hit[0])
            rows_pre.append(base)
            continue
        if is_close_text(x["text"]):
            base.update(status="unscorable", reason="text is a close, parser tagged it open")
            rows_pre.append(base)
            continue
        if x["strike"] is None or x["side"] is None:
            base.update(status="unscorable", reason="missing strike/side")
            rows_pre.append(base)
            continue
        if exp is None:
            base.update(status="unscorable", reason=note, exclude_flag="no_expiry")
            rows_pre.append(base)
            continue
        if x["entry_price"] is None:
            base.update(status="unscorable", reason="missing entry_price")
            rows_pre.append(base)
            continue
        if exp >= TODAY:
            base.update(status="pending", reason="expiry %s not yet passed" % exp)
        key = (x["channel"], x["ticker"], x["side"], x["strike"], exp.isoformat(), x["posted"][:10])
        rec_key[x["id"]] = key
        if key in groups:
            g = groups[key]
            g["ids"].append(x["id"])
            g["n_posts"] += 1
            continue
        groups[key] = base
    out = rows_pre + list(groups.values())
    # score
    need = [g for g in out if "status" not in g]

    syms = sorted({g["ticker"] for g in need})
    print("scoring %d groups across %d tickers" % (len(need), len(syms)))
    for g in need:
        exp = g["expiry_effective"]
        bars, src = daily_bars(g["ticker"], g["posted"][:10], exp)
        if not bars:
            g.update(status="unscorable", reason="no price data for %s" % g["ticker"])
            continue
        if exp < g["posted"][:10]:
            g.update(status="unscorable", reason="expiry %s before post date (parser/typo)" % exp)
            continue
        if entry_below_intrinsic(g, bars):
            g.update(status="excluded", reason="quoted premium below intrinsic value at post time (impossible fill: mis-parsed strike, wrong ticker or replayed post)",
                     exclude_flag="entry_below_intrinsic")
            continue
        g.update(score_group(g, bars, src))
        if g["status"] == "scored" and g["entry_price"] is None:
            g["status"] = "scored_no_entry"
    os.makedirs(os.path.dirname(OUT_JSONL), exist_ok=True)
    with open(OUT_JSONL, "w") as f:
        for g in out:
            f.write(json.dumps(g) + "\n")

    scored = [g for g in out if g["status"] in ("scored", "scored_no_entry")]
    sc_e = [g for g in scored if g.get("return_pct") is not None]
    # distinct contracts across channels
    dc = collections.OrderedDict()
    for g in sc_e:
        k = (g["ticker"], g["side"], g["strike"], g["expiry_effective"], g["posted"][:10])
        dc.setdefault(k, g)  # earliest post (list sorted by time within groups order)
    # quoted results: closes with result_pct, deduped
    qd = {}
    for x in recs:
        if x["action"] == "close" and x.get("result_pct") is not None:
            qd[(x["channel"], x["ticker"], x["posted"][:10], x["result_pct"])] = x
    quoted = collections.defaultdict(list)
    for k, x in qd.items():
        quoted[x["channel"]].append(x["result_pct"])

    by_ch = collections.defaultdict(list)
    for g in sc_e:
        by_ch[g["channel"]].append(g)
    big = {c: v for c, v in by_ch.items() if len(v) >= MIN_N}
    small_rows = [g for c, v in by_ch.items() if len(v) < MIN_N for g in v]
    small_quoted = [q for c in quoted if c not in big for q in quoted[c]]

    cnt = collections.Counter(g["status"] for g in out)
    unreasons = collections.Counter(g["reason"] for g in out if g["status"] == "unscorable")
    L = []
    A = L.append
    A("# Funnel callouts vs the tape: outcomes\n")
    A("Generated %s from `calls.jsonl` (%d records). Source: `tg_outcomes.py`.\n" % (TODAY, len(recs)))
    n_sc = len(sc_e)
    if n_sc < 100:
        A("> **SMALL SAMPLE WARNING.** Only %d opens are scored (threshold for confidence: 100). Most are short-dated "
          "index/ETF/mega-cap trades over a few weeks of tape. Treat every percentage below as anecdote, not a rate.\n" % n_sc)
    else:
        A("> Scored n = %d. Still a short window of tape; expiry-day moves dominate results.\n" % n_sc)
    A("## Method and assumptions\n")
    A("- No option price history exists here. **Headline number = hold-to-expiry intrinsic**: (max(0,S-K) call / max(0,K-S) put at the expiry-date close, minus quoted entry) x 100.")
    A("- **'Touched breakeven' is optimistic**: underlying high (calls) / low (puts) after the post reached strike+entry / strike-entry. It assumes a perfect exit at the extreme; it is an upper bound, not a P&L.")
    A("- Entry premiums are the channel's own quoted fills, unverifiable. No slippage applied (flatters channels).")
    A("- Null expiry is NOT assumed same-day: only parser-tagged 0DTE (expiry_0dte_tag) posts are; others are unscorable. Parser-computed expiry is trusted. SPX priced off ^GSPC. Underlying bars: Yahoo public daily bars; 5m bars for the touch window when the post is within 55 days.")
    A("- Dedupe: one row per (channel, ticker, side, strike, expiry, post date); 'distinct contracts' also collapses echoes across channels.\n")
    A("## Coverage funnel\n")
    n_open_rec = len(opens)
    exc = collections.Counter(g["exclude_flag"] for g in out if g["status"] == "excluded")
    n_noexp = sum(1 for g in out if g.get("exclude_flag") == "no_expiry")
    n_unsc_other = cnt["unscorable"] - n_noexp
    A("| Stage | Count |\n|---|---|")
    A("| Option open records (action=open, kind=option) | %d |" % n_open_rec)
    for f in SKIP_FLAGS:
        if exc[f]:
            A("| minus excluded by parse flag `%s` | %d |" % (f, exc[f]))
    A("| minus no expiry (unknown, not assumed 0DTE) | %d |" % n_noexp)
    A("| minus other unscorable (missing strike/side/entry, parser close, no price data) | %d |" % n_unsc_other)
    A("| Remaining after same-channel/day dedupe | %d |" % (cnt["pending"] + len(scored)))
    A("| Pending (expiry not yet passed) | %d |" % cnt["pending"])
    A("| **Scored** (intrinsic at expiry, entry price present) | %d |" % len(sc_e))
    A("| Distinct contracts among scored (across channels) | %d |" % len(dc))
    A("")
    A("Echoes (`duplicate_echo` + `cross_channel_echo`, %d records) are not scored; the first post of each contract is." % (exc["duplicate_echo"] + exc["cross_channel_echo"]))
    other = [g["reason"] for g in out if g["status"] == "unscorable" and g.get("exclude_flag") != "no_expiry"]
    if other:
        A("Other unscorable reasons: " + "; ".join("%s (%d)" % kv for kv in collections.Counter(other).most_common()) + "\n")
    s_ch = stats(sc_e)
    s_dc = stats(list(dc.values()))
    A("## Pooled results (hold to expiry)\n")
    A("| Basis | n | Win rate (P&L>0) | Median return | Mean return | Worth zero at expiry | Touched BE (optimistic) | Sum P&L, 1 contract each |\n|---|---|---|---|---|---|---|---|")
    for lab, s in (("Channel-level (deduped per channel)", s_ch), ("Distinct contracts", s_dc)):
        if s["n"]:
            A("| %s | %d | %s | %s | %s | %s | %s | $%s |" % (lab, s["n"], fmt(s["win"], 0, True), fmt(s["med"], 0) + "%",
              fmt(s["mean"], 0) + "%", fmt(s["zero"], 0, True), fmt(s["touch"], 0, True), fmt(s["pnl_sum"], 0)))
    A("\nReturn = intrinsic/entry - 1; -100% means expired worthless. Mean is dragged by a few multi-baggers; median is the typical open.\n")
    ranked = sorted(dc.values(), key=lambda g: g["pnl_per_contract"], reverse=True)

    def crow(g):
        return "| %s | %s %s %s %s | %s | $%s | $%s | %s | %s |" % (
            g["channel"].replace("t.me/", ""), g["ticker"], g["strike"], g["side"][0].upper(), g["expiry_effective"],
            g["posted"][:16].replace("T", " "), fmt(g["entry_price"], 2), fmt(g["pnl_per_contract"], 0),
            fmt(g["return_multiple"], 2) + "x", "yes" if g.get("touched_breakeven_optimistic") else "no")
    hdr = "| Channel | Contract | Posted (UTC) | Entry | P&L/contract | Multiple | Touched BE |\n|---|---|---|---|---|---|---|"
    A("## Top 5 distinct contracts by P&L per contract\n")
    A(hdr)
    for g in ranked[:5]:
        A(crow(g))
    A("\n## Bottom 5\n")
    A(hdr)
    for g in ranked[-5:][::-1]:
        A(crow(g))
    A("\n## Survivorship test: channel's quoted results vs real hold-to-expiry\n")
    A("Quoted = `result_pct` on close posts (deduped by channel/ticker/day/value; includes stock and option closes, as quoted). "
      "Real = every scored open from the same channel, held to expiry. Channels with fewer than %d scored opens are pooled." % MIN_N)
    A("\n| Channel | Quoted closes n | Quoted median | Quoted mean | Scored opens n | Real win rate | Real median | Real mean | Worth zero | Gap (quoted mean - real mean) |\n|---|---|---|---|---|---|---|---|---|---|")

    def line(name, rows, q):
        s = stats(rows)
        if not s["n"] and not q:
            return
        gap = (mean(q) - s["mean"]) if (q and s["n"]) else None
        A("| %s | %d | %s | %s | %d | %s | %s | %s | %s | %s |" % (
            name, len(q), fmt(med(q), 0) + "%" if q else "-", fmt(mean(q), 0) + "%" if q else "-", s["n"],
            fmt(s.get("win"), 0, True) if s["n"] else "-", fmt(s.get("med"), 0) + "%" if s["n"] else "-",
            fmt(s.get("mean"), 0) + "%" if s["n"] else "-", fmt(s.get("zero"), 0, True) if s["n"] else "-",
            (fmt(gap, 0) + " pts") if gap is not None else "-"))
    for c in sorted(big, key=lambda c: -len(big[c])):
        line(c.replace("t.me/", ""), big[c], quoted.get(c, []))
    line("small channels (pooled, %d ch)" % len({g["channel"] for g in small_rows}), small_rows, small_quoted)
    allq = [q for v in quoted.values() for q in v]
    line("**ALL channels pooled**", sc_e, allq)
    A("\nQuoted closes include only trades the channel chose to announce a result for; real column includes every scored open, including those never followed up. "
      "Gap is in percentage points of return. Quoted and real are not the same trades, so this compares reporting, not individual fills.\n")
    # paired trade-level comparison
    gmap = {}
    for g in sc_e:
        for i in g["ids"]:
            gmap[i] = g
    pairs, seen = [], set()
    for x in recs:
        if x["action"] != "close" or x.get("result_pct") is None or not x.get("open_id"):
            continue
        k = (x["open_id"], x["result_pct"], x["posted"][:10])
        if k in seen:
            continue
        seen.add(k)
        og = gmap.get(x["open_id"])
        if og is None:
            continue
        pairs.append((x, og))
    A("## Trade-level: quoted close vs same contract held to expiry\n")
    for lab, sel in (("link = contract (exact contract match)", [p for p in pairs if p[0].get("open_link") == "contract"]),
                     ("all links incl. ticker_day (looser match)", pairs)):
        if not sel:
            A("- %s: n=0" % lab)
            continue
        # one row per (open group, close)
        q = [p[0]["result_pct"] for p in sel]
        rl = [p[1]["return_pct"] for p in sel]
        qw = sum(1 for v in q if v > 0)
        rw = sum(1 for p in sel if p[1]["win"])
        flip = sum(1 for p in sel if p[0]["result_pct"] > 0 and not p[1]["win"])
        A("- %s: n=%d pairs over %d contracts. Quoted: win %s, median %s%%, mean %s%%. Same contracts held to expiry: win %s, median %s%%, mean %s%%. "
          "Quoted winners that expired worthless/loss if held: %d of %d." % (
              lab, len(sel), len({id(p[1]) for p in sel}), fmt(qw / len(q), 0, True), fmt(med(q), 0), fmt(mean(q), 0),
              fmt(rw / len(sel), 0, True), fmt(med(rl), 0), fmt(mean(rl), 0), flip, qw))
    A("\nCaveat: a close is an early exit and the real column is hold-to-expiry, so a quoted win that would have expired worthless "
      "is not a lie, it is a different trade. The comparison shows how much of a quoted edge depends on exiting at the right time. "
      "Pairs depend on the parser's open_id link; `ticker_day` links are weaker than `contract` links. Only closes whose paired open was scored appear here.\n")
    A("## Caveats\n")
    A("- n = %d scored opens over a short window (posts from %s to %s); a few trending days move the whole table. Per-channel rows with n under 30 are noisy." % (n_sc, min(g["posted"][:10] for g in sc_e), max(g["posted"][:10] for g in sc_e)))
    A("- Hold-to-expiry ignores that a trader may have exited early at a better (or worse) price; touch-breakeven is the optimistic bound for that.")
    A("- Quoted entry premiums are unverified; real fills on illiquid strikes are typically worse.")
    A("- Echo posts (same trade reposted by several channels) are collapsed for the distinct-contract numbers but each channel counts it once in its own row.")
    A("- Parser issues affecting this run: see `reports/analysis/outcomes_parser_notes.md`.")
    A("- Pending opens (%d) are excluded; longer-dated swings are not yet resolved." % cnt["pending"])
    A("- `expiry_far` records (%d) are reported, not scored." % exc["expiry_far"])
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
