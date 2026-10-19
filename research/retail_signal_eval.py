"""
retail_signal_eval.py: does AfterHour retail activity predict the underlying's next move?

Event study over the lifetime post history in data/following/*_all_posts.json
(the tracked traders, Dec 2022 onward). Read-only; writes reports/analysis/retail_signal_eval.{json,md}.

Arms
  attention    any post naming a ticker -> unsigned forward return (does retail attention lead or lag?)
  crowded      >=3 distinct tracked authors on the ticker inside 3 trading days (first day only)
  brag         posts tagged Gain or Yolo (bragging after a run: the "brag top" hypothesis)
  placebo_attention  random non-event session of the same ticker within +/-250 sessions, one per
               attention event: the effect has to beat THIS, not zero
  directional  ah_sentiment.classify() open+side votes, SIGNED (bear votes negated). Same parser
               as the live get_retail_sentiment tool, so this arm grades the live method.

Measurement (no lookahead in the entry)
  entry  = open of the first regular session that starts AFTER the post (pre-9:30 ET post -> same day open)
  exit   = close h-1 sessions after the entry session, h in (1, 5, 20)
  excess = ticker return - SPY return over the same open->close window
  abnormal (three controls, read together):
    pre_window    = excess - the ticker's mean excess over entries 120..21 sessions BEFORE the post (past data
                    only, but posts fire on names with a HIGH trailing mean, which regresses on its own,
                    so this subtraction flatters every arm; read it beside the matched gap)
    full_span     = excess - that ticker's mean excess over every session in the study span with the same
             entry->exit shape (mean-adjusted market model; uses future sessions, baseline only)
    month_matched = excess - mean excess of the ticker's non-event sessions in the same calendar month
                    (absorbs regime drift, but its windows include the pre-post run-up, so it flatters)
  HEADLINE = *_vs_placebo: arm minus placebo RAW excess within quintiles of the trailing control
             (matched_gap). That is the number that survives the regression-to-mean trap.
  CIs: 2,000-draw bootstrap that resamples 2-calendar-month blocks (a 20-session window overlaps ~4 weeks, so shorter blocks run narrow).
  Floor: a cell with n < 40 is reported but marked underpowered.

Known biases, stated rather than fixed
  * The trader list was picked in 2026 from people still active (survivorship).
  * Posts are mostly options trades; this measures the UNDERLYING, not the contract.
  * Tickers yfinance cannot price (delisted, OTC, crypto) are dropped and counted.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from ah_sentiment import classify, tickers_for  # noqa: E402

ET = ZoneInfo("America/New_York")
HORIZONS = (1, 5, 20)
FLOOR = 40
SKIP = {"SPY", "QQQ", "BTC", "ETH", "SOL", "DOGE", "XRP", "SPX", "NDX", "VIX", "IWM", "DIA"}
BOOT = 2000


def load_posts():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data/following/*_all_posts.json"))):
        author = os.path.basename(f).split("_all_posts")[0].lstrip("@")
        for p in json.load(open(f)):
            ts = p.get("created_at")
            if not ts:
                continue
            title = p.get("title") or ""
            secs = [t.strip() for t in (p.get("tickers") or "").split(",") if t.strip()]
            tks = [t for t in tickers_for(title, secs) if t.isalpha() and t not in SKIP]
            if not tks:
                continue
            out.append({
                "author": author,
                "ts": datetime.fromisoformat(ts.replace("Z", "+00:00")),
                "tag": p.get("tag") or "",
                "tickers": tks,
                "cls": classify(title),
            })
    return out


def fetch_prices(tickers, start, cache):
    if os.path.exists(cache):
        px = pd.read_pickle(cache)
        missing = [t for t in tickers if t not in px.columns.get_level_values(0)]
    else:
        px, missing = None, list(tickers)
    if missing:
        import yfinance as yf
        frames = []
        for i in range(0, len(missing), 100):
            chunk = missing[i:i + 100]
            d = yf.download(chunk, start=start, auto_adjust=True, group_by="ticker",
                            progress=False, threads=True)
            if len(chunk) == 1:
                d.columns = pd.MultiIndex.from_product([chunk, d.columns])
            frames.append(d)
        new = pd.concat(frames, axis=1)
        px = new if px is None else pd.concat([px, new], axis=1)
        px.to_pickle(cache)
    return px


def entry_index(ts: datetime, sessions: pd.DatetimeIndex) -> int | None:
    et = ts.astimezone(ET)
    d = pd.Timestamp(et.date())
    before_open = (et.hour, et.minute) < (9, 30)
    i = sessions.searchsorted(d, side="left" if before_open else "right")
    return int(i) if i < len(sessions) else None


def block_bootstrap(vals, weeks, rng):
    by = defaultdict(list)
    for v, w in zip(vals, weeks):
        by[w].append(v)
    keys = list(by)
    means = []
    for _ in range(BOOT):
        s = [x for k in rng.choices(keys, k=len(keys)) for x in by[k]]
        means.append(float(np.mean(s)))
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def matched_gap(arm, placebo, rng, h=20, bins=5):
    """Arm minus placebo RAW excess, matched on the trailing pre-window control.

    Events fire on tickers whose trailing excess is high, and a high trailing mean regresses on its
    own, so subtracting it flatters any arm selected on it. Instead: bin both sets on the trailing
    control (quintiles of the arm's distribution), compare raw excess within each bin, and weight the
    bins by the arm's counts. CI = block bootstrap of the weighted gap.
    """
    a = [x for x in arm if x.get(f"pab{h}") is not None]
    p = [x for x in placebo if x.get(f"pab{h}") is not None]
    if len(a) < FLOOR or len(p) < FLOOR:
        return {"n_arm": len(a), "n_placebo": len(p), "underpowered": True}
    ctrl = lambda x: x[f"ex{h}"] - x[f"pab{h}"]  # the trailing control itself
    edges = np.percentile([ctrl(x) for x in a], np.linspace(0, 100, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf

    def binned(rows):
        out = defaultdict(list)
        for x in rows:
            out[int(np.searchsorted(edges, ctrl(x), side="right") - 1)].append(x)
        return out

    def gap(ab, pb, stat):
        tot, w = 0.0, 0
        for k in range(bins):
            if ab.get(k) and pb.get(k):
                tot += len(ab[k]) * (stat([x[f"ex{h}"] for x in ab[k]]) - stat([x[f"ex{h}"] for x in pb[k]]))
                w += len(ab[k])
        return tot / w if w else float("nan")

    ab, pb = binned(a), binned(p)
    per_bin = [round(100 * (float(np.mean([x[f"ex{h}"] for x in ab[k]])) - float(np.mean([x[f"ex{h}"] for x in pb[k]]))), 2)
               if ab.get(k) and pb.get(k) else None for k in range(bins)]
    ablk, pblk = defaultdict(list), defaultdict(list)
    for x in a:
        ablk[x["week"]].append(x)
    for x in p:
        pblk[x["week"]].append(x)
    keys = sorted(set(ablk) & set(pblk))
    draws = []
    for _ in range(BOOT // 4):
        pick = rng.choices(keys, k=len(keys))
        draws.append(gap(binned([x for k in pick for x in ablk[k]]), binned([x for k in pick for x in pblk[k]]), np.mean))
    lo, hi = np.nanpercentile(draws, [2.5, 97.5])
    return {"horizon": h, "n_arm": len(a), "n_placebo": len(p), "blocks": len(keys),
            "mean_gap_pct": round(100 * gap(ab, pb, np.mean), 3),
            "ci95_pct": [round(100 * float(lo), 3), round(100 * float(hi), 3)],
            "median_gap_pct": round(100 * gap(ab, pb, np.median), 3),
            "per_quintile_mean_gap_pct": per_bin}


def summarize(rows, rng):
    out = {}
    for h in HORIZONS:
        r = [x for x in rows if x.get(f"ab{h}") is not None]
        if not r:
            out[h] = {"n": 0}
            continue
        ab = [x[f"ab{h}"] for x in r]
        ex = [x[f"ex{h}"] for x in r]
        lo, hi = block_bootstrap(ab, [x["week"] for x in r], rng)
        out[h] = {
            "n": len(r),
            "weeks": len({x["week"] for x in r}),
            "mean_abnormal_pct": round(100 * float(np.mean(ab)), 3),
            "ci95_pct": [round(100 * lo, 3), round(100 * hi, 3)],
            "median_abnormal_pct": round(100 * float(np.median(ab)), 3),
            "beat_control_rate": round(float(np.mean([a > 0 for a in ab])), 3),
            "mean_excess_vs_spy_pct": round(100 * float(np.mean(ex)), 3),
            "underpowered": len(r) < FLOOR,
        }
        lo_w, hi_w = np.percentile(ab, [1, 99])
        out[h]["winsorized_mean_abnormal_pct"] = round(100 * float(np.mean(np.clip(ab, lo_w, hi_w))), 3)
        m = [x for x in r if x.get(f"mab{h}") is not None]
        if m:
            lo2, hi2 = block_bootstrap([x[f"mab{h}"] for x in m], [x["week"] for x in m], rng)
            out[h]["month_matched"] = {"n": len(m),
                                       "mean_abnormal_pct": round(100 * float(np.mean([x[f"mab{h}"] for x in m])), 3),
                                       "ci95_pct": [round(100 * lo2, 3), round(100 * hi2, 3)]}
        pm = [x for x in r if x.get(f"pab{h}") is not None]
        if pm:
            lo3, hi3 = block_bootstrap([x[f"pab{h}"] for x in pm], [x["week"] for x in pm], rng)
            out[h]["pre_window"] = {"n": len(pm),
                                    "mean_abnormal_pct": round(100 * float(np.mean([x[f"pab{h}"] for x in pm])), 3),
                                    "median_abnormal_pct": round(100 * float(np.median([x[f"pab{h}"] for x in pm])), 3),
                                    "beat_control_rate": round(float(np.mean([x[f"pab{h}"] > 0 for x in pm])), 3),
                                    "ci95_pct": [round(100 * lo3, 3), round(100 * hi3, 3)]}
            pv = np.array([x[f"pab{h}"] for x in pm])
            a_, b_ = np.percentile(pv, [1, 99])
            out[h]["pre_window"]["winsorized_mean_pct"] = round(100 * float(np.mean(np.clip(pv, a_, b_))), 3)
        per_t = defaultdict(list)
        for x in r:
            per_t[x["t"]].append(x[f"ab{h}"])
        out[h]["ticker_equal_weight_pct"] = round(100 * float(np.mean([np.mean(v) for v in per_t.values()])), 3)
        out[h]["tickers"] = len(per_t)
        top = sorted(per_t, key=lambda k: -len(per_t[k]))[:10]
        rest = [x[f"ab{h}"] for x in r if x["t"] not in top]
        out[h]["ex_top10_tickers_pct"] = round(100 * float(np.mean(rest)), 3) if rest else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/ah_eval_prices.pkl")
    ap.add_argument("--min-days", type=int, default=3, help="ticker must be named on >= N distinct days")
    args = ap.parse_args()
    rng = random.Random(7)

    posts = load_posts()
    days = defaultdict(set)
    for p in posts:
        for t in p["tickers"]:
            days[t].add(p["ts"].astimezone(ET).date())
    universe = sorted(t for t, d in days.items() if len(d) >= args.min_days)
    start = min(p["ts"] for p in posts).date().isoformat()
    px = fetch_prices(universe + ["SPY"], start, args.cache)

    spy = px["SPY"].dropna(subset=["Open", "Close"])
    sessions = spy.index
    so, sc = spy["Open"].to_numpy(), spy["Close"].to_numpy()

    priced, dropped = {}, []
    for t in universe:
        if t not in px.columns.get_level_values(0):
            dropped.append(t)
            continue
        d = px[t].reindex(sessions)
        if d["Close"].notna().sum() < 60:
            dropped.append(t)
            continue
        priced[t] = (d["Open"].to_numpy(), d["Close"].to_numpy())

    # control: mean excess for every entry session of the ticker, per horizon
    def excess(t, i, h):
        o, c = priced[t]
        j = i + h - 1
        if j >= len(sessions) or np.isnan(o[i]) or np.isnan(c[j]) or o[i] <= 0 or c[j] <= 0:
            return None
        r = c[j] / o[i] - 1
        if r <= -0.95 or r >= 10:  # bad microcap / reverse-split / delisting prints, not economic moves
            return None
        return r - (sc[j] / so[i] - 1)

    control = {}
    for t, (o, c) in priced.items():
        for h in HORIZONS:
            n = len(sessions) - h + 1
            ex = (c[h - 1:] / o[:n] - 1) - (sc[h - 1:] / so[:n] - 1)
            control[(t, h)] = float(np.nanmean(ex)) if np.isfinite(ex).any() else None

    months = sessions.strftime("%Y-%m")
    month_idx = defaultdict(list)
    for k, m in enumerate(months):
        month_idx[m].append(k)
    mcache = {}

    def month_control(t, i, h):
        key = (t, months[i], h)
        if key not in mcache:
            vals = [excess(t, k, h) for k in month_idx[months[i]] if k not in event_sessions[t]]
            vals = [v for v in vals if v is not None]
            mcache[key] = float(np.mean(vals)) if len(vals) >= 5 else None
        return mcache[key]

    def pre_control(t, i, h):
        # textbook estimation window: entries in [i-120, i-21], so every control window closes
        # before the event and before any run-up in the 20 sessions that led to the post
        vals = [excess(t, k, h) for k in range(max(0, i - 120), max(0, i - 20)) if k + h - 1 < i]
        vals = [v for v in vals if v is not None]
        return float(np.mean(vals)) if len(vals) >= 40 else None

    def event(t, i, sign=1):
        d = sessions[i]
        row = {"t": t, "i": i, "week": f"{d.year}-{(d.month - 1) // 2}"}  # block = 2 calendar months (h20 windows span ~4 weeks)
        for h in HORIZONS:
            e = excess(t, i, h)
            cm = control.get((t, h))
            mm = month_control(t, i, h)
            pc = pre_control(t, i, h)
            if e is None or cm is None:
                row[f"ex{h}"] = row[f"ab{h}"] = row[f"mab{h}"] = row[f"pab{h}"] = None
            else:
                row[f"ex{h}"] = sign * e
                row[f"ab{h}"] = sign * (e - cm)
                row[f"mab{h}"] = None if mm is None else sign * (e - mm)
                row[f"pab{h}"] = None if pc is None else sign * (e - pc)
        return row

    # build per (ticker, entry session) aggregates
    seen = defaultdict(lambda: {"authors": set(), "brag": False, "votes": {}})
    for p in posts:
        i = entry_index(p["ts"], sessions)
        if i is None:
            continue
        for t in p["tickers"]:
            if t not in priced:
                continue
            s = seen[(t, i)]
            s["authors"].add(p["author"])
            if p["tag"] in ("Gain", "Yolo"):
                s["brag"] = True
            if p["cls"]["action"] == "open":
                s["votes"][p["author"]] = p["cls"]["stance"]  # one vote per author per ticker-session

    event_sessions = defaultdict(set)
    for (t, i) in seen:
        event_sessions[t].add(i)

    arms = defaultdict(list)
    crowd_last = {}
    for (t, i), s in sorted(seen.items(), key=lambda kv: kv[0][1]):
        arms["attention"].append(event(t, i))
        if s["brag"]:
            arms["brag"].append(event(t, i))
        for st in set(s["votes"].values()):  # one row per (ticker, session, stance)
            arms[f"directional_{st}"].append(event(t, i, 1 if st == "bull" else -1))
            arms["directional_signed"].append(event(t, i, 1 if st == "bull" else -1))
        # crowding: >=3 distinct authors within the trailing 3 sessions, first fire only
        window = set().union(*(seen[(t, k)]["authors"] for k in range(i - 2, i + 1) if (t, k) in seen))
        if len(window) >= 3 and crowd_last.get(t, -99) < i - 2:
            arms["crowded"].append(event(t, i))
        if len(window) >= 3:
            crowd_last[t] = i

    # placebo: same ticker, a random NON-event session within +/-250 sessions of each attention event,
    # same controls. If the placebo shows the same abnormal, the effect is the ticker's own mean
    # reversion, not the crowd showing up.
    event_near = {t: {k for i in ks for k in range(i - 20, i + 21)} for t, ks in event_sessions.items()}
    for r0 in list(arms["attention"]):
        t, i = r0["t"], r0["i"]
        near = event_near[t]
        pool = [k for k in range(max(140, i - 250), min(len(sessions) - 21, i + 250)) if k not in near]
        if pool:
            arms["placebo_attention"].append(event(t, rng.choice(pool)))

    report_extra = {"attention_vs_placebo": matched_gap(arms["attention"], arms["placebo_attention"], rng),
                    "crowded_vs_placebo": matched_gap(arms["crowded"], arms["placebo_attention"], rng),
                    "brag_vs_placebo": matched_gap(arms["brag"], arms["placebo_attention"], rng),
                    "directional_bull_vs_placebo": matched_gap(arms["directional_bull"], arms["placebo_attention"], rng)}

    by_year = defaultdict(list)
    for r in arms["attention"]:
        by_year[sessions[r["i"]].year].append(r)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "posts_with_tickers": len(posts),
        "authors": len({p["author"] for p in posts}),
        "span": [start, sessions[-1].date().isoformat()],
        "universe": len(universe),
        "priced": len(priced),
        "dropped_unpriceable": len(dropped),
        "floor_n": FLOOR,
        "arms": {k: summarize(v, rng) for k, v in sorted(arms.items())},
        **report_extra,
        "attention_by_year": {str(y): summarize(v, rng) for y, v in sorted(by_year.items())},
    }
    os.makedirs(os.path.join(ROOT, "reports/analysis"), exist_ok=True)
    with open(os.path.join(ROOT, "reports/analysis/retail_signal_eval.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
