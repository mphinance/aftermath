#!/usr/bin/env python3
"""Build api/funnel-scorecard.json and api/funnel-fx-signals.json (public scoring results).

Stdlib only. Degrades gracefully: any missing or empty input yields empty sections, never a crash.

Inputs (all optional), under data/telegram_funnel/ unless noted:
  outcomes.jsonl   option opens scored by tg_outcomes.py (hold-to-expiry intrinsic vs quoted entry)
  calls.jsonl      parsed callouts (option opens/closes, open_id/open_link pairs, stock mentions)
  fx_signals.jsonl forex/gold/index signals scored by tg_fx_signals.py
  fx_claims.jsonl  channel follow-up claims (counted only)
  reports/analysis/fx_signals.md   read for assumptions text and the basis-sensitivity table only

Conventions in the output: rates and shares are fractions 0..1; *_ci are Wilson 95% intervals [lo, hi];
option returns are percent (-100.0 = expired worthless); FX R values are multiples of the stop distance.
Only public channels appear (private invite links are dropped). Nothing here is advice and nothing is an
accusation: the accounts and channels are flagged for investigation by https://telegramscammers.com, not
found to be fraud."""
import collections
import json
import math
import re
import statistics
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
API = BASE / "api"
TF = BASE / "data" / "telegram_funnel"
FX_REPORT = BASE / "reports" / "analysis" / "fx_signals.md"
SITE = "https://telegramscammers.com"
DISCLAIMER = ("Analysis of public posts. Channels and accounts here are flagged for investigation, not a finding of "
              f"fraud. Flag list curated by {SITE}. Statistical description of what the tape shows under stated "
              "assumptions, with sample sizes and 95% ranges; not advice.")
SMALL_N = 5          # per-channel rows under this are flagged small
FX_WEEKLY_MIN = 30   # channels with at least this many scored FX signals get a weekly table
BULK_N = 6           # same channel + exact timestamp on this many posts or more = bulk dump
SIGNAL_TEXT_LEN = 400
METHOD_DOC = "https://ah.mphinance.com/scorecard"
DOC_PATH = "docs/FUNNEL.md"

OPTION_ASSUMPTIONS = [
    "No option price history exists in the public data used here. Each option callout is scored by holding it to expiry: intrinsic value at the expiry-date close of the underlying (Yahoo public daily bars) minus the entry premium the channel itself quoted. A 'win' means intrinsic value at expiry was above the quoted entry; -100% means it expired worthless.",
    "Channels usually post an early exit, not a hold to expiry. Held-to-expiry is a different trade from the one a channel may have closed, so it is a stress test of the callouts, not a record of anyone's P&L.",
    "Entry premiums are the channels' own quoted fills and cannot be verified. Slippage, spreads and fees are ignored, which flatters the callouts.",
    "A missing expiry is treated as unknown, not as same-day, unless the parser saw an explicit 0DTE tag. Records without an expiry or an entry price are not scored.",
    "Reposts of the same trade are collapsed (one row per channel, ticker, side, strike, expiry and post day); 'distinct contracts' is keyed on ticker, side, strike and expiry alone, so it also collapses the same contract posted on different days or by several channels; 'contract-days' keeps one row per contract per post day.",
    "Posts whose timestamp is shared by 6 or more posts in one channel (bulk history dumps), implausible entries and far-dated expiries are excluded rather than scored.",
    "Impossible quotes are excluded: if even the best print of the post day (day low for calls, day high for puts) leaves the contract's intrinsic value more than 1.5 times the quoted premium plus 0.5 above that premium, the quote cannot be a real fill for that strike (a mis-parsed strike, a wrong ticker or a replayed old post), so it is not scored. The count is in the coverage funnel.",
    "The mean return is dominated by a few multi-baggers, so the median and the share expired worthless describe the typical call better; the file also gives the mean without the 5 largest returns.",
    "Pending options (expiry not yet passed) are not scored. The window is short and a few trending days move the totals.",
]
FX_ASSUMPTIONS = [
    "Pips: gold 1 pip = 0.10, indices 1 point, FX 0.0001 (JPY pairs 0.01). Pip-denominated targets are measured from the fill price and flagged; if a channel meant a different pip size, those targets are scored too near or too far.",
    "Tape: Yahoo public 5-minute bars. XAUUSD spot is not available there, so gold uses COMEX futures (GC=F). The futures-to-spot basis (about 30 dollars on gold) is estimated from the channel's own stated entries (a time-varying fit of stated entry minus tape at post time) and added back. The basis estimate is the largest uncertainty: it is the same size as a typical 10 dollar stop. The sensitivity table below rescored every signal with other basis assumptions.",
    "Fill rule: the market variant fills at the close of the 5-minute bar containing the post when the market is inside the stated entry zone (widened by a 0.25 R tolerance). When the market is away from the entry, the touch variant waits up to 4 hours for the entry zone to trade. The two variants are never pooled.",
    "No spread, slippage or commission, and no break-even or trailing management. Every R figure is therefore optimistic on costs; exiting everything at the last target is a harsh all-or-nothing reading, exiting at TP1 the generous one.",
    "Same-bar tie: if the stop and a target both trade inside one 5-minute bar, the stop is counted first. Targets are sorted by distance from the fill, so TP1 is always the nearest.",
    "Horizon: 24 hours after the fill. Signals whose window runs past the last available bar are not scored. 'TP1 first' means TP1 traded before the stop inside the horizon; 'SL first' means the stop traded before TP1.",
    "Reposts within 60 minutes with identical levels are collapsed to the first copy. Posts sharing one exact timestamp with 5 or more others in the same channel (bulk history dumps) are not scored because their original post time is unknown.",
    "Posts with no stop or no target, obvious price typos (levels far from the market), and signals older than Yahoo's roughly 60-day 5-minute history are reported in the funnel but not scored.",
]


# ------------------------------------------------------------------ helpers
def wilson(k, n, z=1.96):
    """Wilson score interval for k successes in n trials; [None, None] when n == 0."""
    if not n:
        return [None, None]
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def rate(k, n):
    return round(k / n, 4) if n else None


def mean(v):
    v = [x for x in v if x is not None]
    return round(statistics.fmean(v), 4) if v else None


def median(v):
    v = [x for x in v if x is not None]
    return round(statistics.median(v), 4) if v else None


def read_jsonl(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                if isinstance(r, dict):
                    rows.append(r)
    except OSError:
        pass
    return rows


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def is_public(channel):
    c = (channel or "").strip().lower()
    return bool(c) and "/+" not in c and "joinchat" not in c


def clean(s, n=None):
    s = (s or "").replace("\u2014", ",").replace("\u2013", "-")
    s = s.strip()
    if n and len(s) > n:
        s = s[: n - 3].rstrip() + "..."
    return s


def parse_date(s):
    try:
        return date.fromisoformat((s or "")[:10])
    except ValueError:
        return None


def week_monday(s):
    d = parse_date(s)
    return (d - timedelta(days=d.weekday())).isoformat() if d else None


def fnum(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


# ------------------------------------------------------------------ options
def opt_stats(rows):
    """rows: scored option groups that carry return_pct."""
    n = len(rows)
    wins = sum(1 for r in rows if r.get("win"))
    zero = sum(1 for r in rows if r.get("worthless"))
    rets = [r["return_pct"] for r in rows]
    touched = [r.get("touched_breakeven_optimistic") for r in rows if r.get("touched_breakeven_optimistic") is not None]
    return {
        "n_scored": n,
        "win_rate": rate(wins, n), "win_ci": wilson(wins, n),
        "median_return": median(rets), "mean_return": mean(rets),
        "worthless_share": rate(zero, n), "worthless_ci": wilson(zero, n),
        "touched_breakeven_optimistic_share": rate(sum(1 for t in touched if t), len(touched)),
        "max_return": max(rets) if rets else None,
        # the mean is dominated by a handful of multi-baggers; this shows it without the 5 largest returns
        "mean_return_excl_top5": mean(sorted(rets)[:-5]) if len(rets) > 10 else None,
    }


def dte_bucket(g):
    e, p = parse_date(g.get("expiry_effective")), parse_date(g.get("posted"))
    if not e or not p:
        return None
    d = (e - p).days
    if d <= 0:
        return "0 days (same day)"
    if d <= 2:
        return "1 to 2 days"
    if d <= 7:
        return "3 to 7 days"
    if d <= 30:
        return "8 to 30 days"
    return "31 days or more"


DTE_ORDER = ["0 days (same day)", "1 to 2 days", "3 to 7 days", "8 to 30 days", "31 days or more"]


def build_options(calls, outcomes):
    opens = [c for c in calls if c.get("action") == "open" and c.get("kind") == "option" and is_public(c.get("channel"))]
    outs = [o for o in outcomes if is_public(o.get("channel"))]
    if not outs:
        return {"available": False, "note": "No scored option data yet.", "pooled": {"n_scored": 0}, "coverage_funnel": [],
                "by_dte_bucket": [], "by_ticker": [], "by_channel": [], "paired": {"n_pairs": 0}}
    scored = [o for o in outs if o.get("status") in ("scored", "scored_no_entry") and fnum(o.get("return_pct")) is not None]
    scored.sort(key=lambda o: o.get("posted") or "")
    dc = collections.OrderedDict()    # one row per contract (ticker, side, strike, expiry), earliest post
    dcd = collections.OrderedDict()   # one row per contract per post day
    for g in scored:
        k = (g.get("ticker"), g.get("side"), g.get("strike"), g.get("expiry_effective"))
        dc.setdefault(k, g)
        dcd.setdefault(k + ((g.get("posted") or "")[:10],), g)
    pooled = opt_stats(scored)
    dates = [(g.get("posted") or "")[:10] for g in scored if g.get("posted")]
    pooled.update({
        "n_distinct_contracts": len(dc),
        "n_contract_days": len(dcd),
        "contract_days": {k: v for k, v in opt_stats(list(dcd.values())).items() if k != "n_scored"},
        "distinct_contracts": {k: v for k, v in opt_stats(list(dc.values())).items() if k != "n_scored"},
        "window_start": min(dates) if dates else None, "window_end": max(dates) if dates else None,
        "return_unit": "percent of quoted entry premium, held to expiry; -100 = expired worthless",
        "win_definition": "intrinsic value at expiry above the quoted entry premium",
        "hold_to_expiry_assumptions": OPTION_ASSUMPTIONS,
    })

    # coverage funnel
    exc = collections.Counter(o.get("exclude_flag") for o in outs if o.get("status") == "excluded")
    n_noexp = sum(1 for o in outs if o.get("status") == "unscorable" and o.get("exclude_flag") == "no_expiry")
    n_unsc = sum(1 for o in outs if o.get("status") == "unscorable") - n_noexp
    pend = [o for o in outs if o.get("status") == "pending"]
    sc_all = [o for o in outs if o.get("status") in ("scored", "scored_no_entry")]
    merged = sum(max(0, len(o.get("ids") or [1]) - 1) for o in outs if o.get("status") in ("pending", "scored", "scored_no_entry"))
    n_open = len(opens) or sum(len(o.get("ids") or [1]) for o in outs)
    flag_label = {
        "duplicate_echo": "excluded: same trade reposted in the same channel",
        "cross_channel_echo": "excluded: same trade already posted by another channel",
        "expiry_before_post": "excluded: parsed expiry is before the post date",
        "entry_implausible": "excluded: implausible entry price",
        "posted_date_suspect": "excluded: bulk history dump (post date not trusted)",
        "spread_suspect": "excluded: looks like a spread",
        "ticker_list": "excluded: ticker list, not a single call",
        "expiry_far": "excluded: expiry far in the future",
        "entry_below_intrinsic": "excluded: quoted premium below intrinsic value at post time (impossible fill)",
    }
    funnel = [{"stage": "option open callouts parsed", "n": n_open, "kind": "start"}]
    for f, lab in flag_label.items():
        if exc.get(f):
            funnel.append({"stage": lab, "flag": f, "n": exc[f], "kind": "removed"})
    for f in sorted(set(exc) - set(flag_label)):
        if f:
            funnel.append({"stage": "excluded: " + f, "flag": f, "n": exc[f], "kind": "removed"})
    funnel.append({"stage": "unknown expiry (not assumed same-day)", "n": n_noexp, "kind": "removed"})
    funnel.append({"stage": "other unscorable (missing entry price, strike or side, no price data)", "n": n_unsc, "kind": "removed"})
    funnel.append({"stage": "merged same-channel same-day repeats", "n": merged, "kind": "removed"})
    funnel.append({"stage": "pending (expiry not yet passed)", "n": len(pend), "kind": "removed"})
    funnel.append({"stage": "scored at expiry", "n": len(scored), "kind": "end"})
    if len(sc_all) != len(scored):
        funnel.append({"stage": "scored but return not computable (entry price zero)", "n": len(sc_all) - len(scored), "kind": "note"})

    # by DTE bucket
    bk = collections.defaultdict(list)
    for g in scored:
        b = dte_bucket(g)
        if b:
            bk[b].append(g)
    by_dte = [dict(bucket=b, **opt_stats(bk[b])) for b in DTE_ORDER if bk.get(b)]

    # by ticker (top 15 by scored n)
    bt = collections.defaultdict(list)
    for g in scored:
        bt[g.get("ticker")].append(g)
    top = sorted(bt.items(), key=lambda kv: (-len(kv[1]), str(kv[0])))[:15]
    by_ticker = [dict(ticker=t, **opt_stats(v)) for t, v in top]

    # quoted closes per channel (deduped by channel, ticker, day, value)
    qd = {}
    for x in calls:
        if x.get("action") == "close" and fnum(x.get("result_pct")) is not None and is_public(x.get("channel")):
            qd[(x.get("channel"), x.get("ticker"), (x.get("posted") or "")[:10], x["result_pct"])] = x
    quoted = collections.defaultdict(list)
    for k, x in qd.items():
        quoted[k[0]].append(x["result_pct"])
    bc = collections.defaultdict(list)
    for g in scored:
        bc[g["channel"]].append(g)
    by_channel = []
    for ch, v in bc.items():
        q = quoted.get(ch, [])
        by_channel.append(dict(channel=ch, **opt_stats(v), quoted_closes=len(q), quoted_mean_result=mean(q),
                               quoted_median_result=median(q), small=len(v) < SMALL_N))
    by_channel.sort(key=lambda r: (-r["n_scored"], r["channel"]))

    # paired: channel-quoted close vs the same trade held to expiry
    gmap = {}
    for g in scored:
        for i in g.get("ids") or []:
            gmap[i] = g
    pairs, seen = [], set()
    for x in calls:
        if x.get("action") != "close" or fnum(x.get("result_pct")) is None or not x.get("open_id"):
            continue
        if not is_public(x.get("channel")):
            continue
        k = (x["open_id"], x["result_pct"], (x.get("posted") or "")[:10])
        if k in seen:
            continue
        seen.add(k)
        og = gmap.get(x["open_id"])
        if og is not None:
            pairs.append((x, og))

    def pair_stats(sel):
        n = len(sel)
        if not n:
            return {"n_pairs": 0, "n_contracts": 0}
        q = [p[0]["result_pct"] for p in sel]
        h = [p[1]["return_pct"] for p in sel]
        qw = sum(1 for v in q if v > 0)
        hw = sum(1 for p in sel if p[1].get("win"))
        flip = sum(1 for p in sel if p[0]["result_pct"] > 0 and not p[1].get("win"))
        return {"n_pairs": n, "n_contracts": len({id(p[1]) for p in sel}),
                "quoted_win_rate": rate(qw, n), "quoted_win_ci": wilson(qw, n), "quoted_median": median(q), "quoted_mean": mean(q),
                "held_win_rate": rate(hw, n), "held_win_ci": wilson(hw, n), "held_median": median(h), "held_mean": mean(h),
                "quoted_winners": qw, "quoted_winners_that_would_have_lost": flip,
                "quoted_winners_that_would_have_lost_ci": wilson(flip, qw)}
    paired = pair_stats([p for p in pairs if p[0].get("open_link") == "contract"])
    paired["link_rule"] = "exact contract match between the close post and an earlier scored open from the same channel"
    paired["all_links"] = pair_stats(pairs)
    paired["all_links"]["link_rule"] = "contract match plus the looser same-ticker same-day match"
    paired["caveat"] = ("A channel's close is an early exit; the held column is the same contract held to expiry. A quoted win that "
                        "would have expired worthless is a different trade, not a false statement. The comparison shows how much of "
                        "a quoted result depends on the exit being at the right moment. Quoted results are the channel's own, "
                        "unverified claims and only trades the channel chose to announce; only closes whose paired open was scored "
                        "appear. Pairs depend on the parser's open link.")
    return {"available": True, "pooled": pooled, "coverage_funnel": funnel, "by_dte_bucket": by_dte,
            "by_ticker": by_ticker, "by_channel": by_channel, "paired": paired}


# ------------------------------------------------------------------ fx
def fx_stats(rows):
    n = len(rows)
    if not n:
        return None
    tp1 = [r for r in rows if r.get("tp1_hit")]
    multi = [r for r in rows if (r.get("n_tp") or 0) >= 2]
    tp2 = [r for r in multi if (r.get("tps_hit") or 0) >= 2]
    sl = [r for r in rows if r.get("sl_first")]
    unres = [r for r in rows if not r.get("resolved")]
    tgt = [r["r_tp1_target"] for r in tp1 if fnum(r.get("r_tp1_target")) is not None]
    avgwin = (sum(tgt) / len(tgt)) if tgt else None
    times = [r["minutes_to_first_event"] for r in rows if r.get("resolved") and fnum(r.get("minutes_to_first_event")) is not None]
    return {
        "n": n,
        "tp1_hit_rate": rate(len(tp1), n), "tp1_ci": wilson(len(tp1), n),
        "sl_first_rate": rate(len(sl), n), "sl_first_ci": wilson(len(sl), n),
        "unresolved_rate": rate(len(unres), n),
        "tp2plus_rate": rate(len(tp2), len(multi)), "tp2plus_n": len(tp2), "tp2plus_denominator": len(multi),
        "tp2plus_ci": wilson(len(tp2), len(multi)),
        "mean_r_tp1": mean([r.get("r_tp1") for r in rows]), "mean_r_last": mean([r.get("r_last") for r in rows]),
        "avg_tp1_distance_r": mean([r.get("r_tp1_target") for r in rows]),
        "avg_winning_tp1_r": round(avgwin, 4) if avgwin is not None else None,
        "breakeven_tp1_rate": round(1 / (1 + avgwin), 4) if avgwin else None,
        "median_minutes_to_first_event": median(times),
        "ambiguous_same_bar": sum(1 for r in rows if r.get("ambiguous")),
    }


def parse_sensitivity(md):
    """Pull the basis-sensitivity table (section 4c) from fx_signals.md; None when absent."""
    if not md or "### 4c" not in md:
        return None
    sec = md.split("### 4c", 1)[1]
    sec = re.split(r"\n#{2,3} ", sec, maxsplit=1)[0] if "\n#" in sec else sec
    cell = re.compile(r"n=(\d+)(?:, (-?\d+)%, (-?[\d.]+)(?:, (-?[\d.]+))?)?")

    def parse_cell(s):
        m = cell.search(s)
        if not m:
            return None
        n = int(m.group(1))
        out = {"n": n}
        if m.group(2) is not None:
            out["tp1_hit_rate"] = int(m.group(2)) / 100
            out["mean_r_tp1"] = float(m.group(3))
            if m.group(4) is not None:
                out["mean_r_last"] = float(m.group(4))
        return out
    rows = []
    for line in sec.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "basis mode" in line:
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 4:
            continue
        rows.append({"mode": c[0], "gold_market": parse_cell(c[1]), "gold_touch": parse_cell(c[2]), "all_market": parse_cell(c[3]),
                     "skipped_typo": int(c[4]) if len(c) > 4 and c[4].isdigit() else None})
    if not rows:
        return None
    shifted = [r for r in rows if r["gold_market"] and r["gold_market"].get("tp1_hit_rate") is not None
               and not r["mode"].lower().startswith("none")]
    rng = None
    if shifted:
        t = [r["gold_market"]["tp1_hit_rate"] for r in shifted]
        rr = [r["gold_market"]["mean_r_tp1"] for r in shifted]
        nn = [r["gold_market"]["n"] for r in shifted]
        rng = {"scope": "gold, market-fill variant, across the basis assumptions in the table (excluding the no-basis row)",
               "tp1_hit_rate": [min(t), max(t)], "mean_r_tp1": [min(rr), max(rr)], "n": [min(nn), max(nn)],
               "mean_r_tp1_same_sign": (max(rr) < 0 or min(rr) > 0)}
    return {"rows": rows, "range": rng,
            "note": "Each row rescored the same posts with a different assumption about the futures-to-spot basis. 'None' uses raw futures prices and is shown for completeness."}


def parse_report_assumptions(md):
    if not md or "## 9." not in md:
        return []
    sec = md.split("## 9.", 1)[1]
    return [clean(l[2:].strip()) for l in sec.splitlines() if l.startswith("- ")]


def classify_stock(c):
    return c.get("kind") in ("option", "stock", "spread")


def build_content_timeline(calls, fx_rows):
    """Per channel: first/last dates of forex/gold/index signal posts versus stock/option posts, plus bulk-dump groups."""
    per = collections.defaultdict(lambda: {"fx": [], "st": [], "ids_by_ts": collections.defaultdict(dict)})
    for r in fx_rows:
        ch = r.get("channel")
        if not is_public(ch) or not r.get("date"):
            continue
        if r.get("skip_reason") == "no_levels":
            continue
        per[ch]["fx"].append(r)
        per[ch]["ids_by_ts"][r["date"]][r["id"]] = "fx"
    for c in calls:
        ch = c.get("channel")
        if not is_public(ch) or not c.get("posted") or not classify_stock(c):
            continue
        per[ch]["st"].append(c)
        per[ch]["ids_by_ts"][c["posted"]].setdefault(c["id"], "stock")
    out = []
    for ch, d in per.items():
        bulk_ts = {ts for ts, ids in d["ids_by_ts"].items() if len(ids) >= BULK_N}
        fx_all = sorted(r["date"] for r in d["fx"])
        fx_ok = sorted(r["date"] for r in d["fx"] if r["date"] not in bulk_ts and not r.get("bulk_timestamp"))
        st_posts = {}
        for c in d["st"]:
            st_posts[c["id"]] = c
        st_all = sorted(c["posted"] for c in st_posts.values())
        st_ok = sorted(c["posted"] for c in st_posts.values()
                       if c["posted"] not in bulk_ts and "posted_date_suspect" not in (c.get("parse_flags") or []))
        groups = []
        for ts in sorted(bulk_ts):
            ids = d["ids_by_ts"][ts]
            groups.append({"timestamp": ts, "posts": len(ids), "fx_signal_posts": sum(1 for v in ids.values() if v == "fx"),
                           "stock_option_posts": sum(1 for v in ids.values() if v == "stock")})
        weeks = collections.defaultdict(lambda: {"fx": 0, "stock": 0})
        for x in fx_all:
            weeks[week_monday(x)]["fx"] += 1
        for x in st_all:
            weeks[week_monday(x)]["stock"] += 1
        if not fx_all and not st_all:
            continue
        out.append({
            "channel": ch,
            "fx_posts": len(fx_all), "fx_first": fx_all[0][:10] if fx_all else None, "fx_last": fx_all[-1][:10] if fx_all else None,
            "fx_first_outside_bulk": fx_ok[0][:10] if fx_ok else None, "fx_last_outside_bulk": fx_ok[-1][:10] if fx_ok else None,
            "stock_option_posts": len(st_all), "stock_first": st_all[0][:10] if st_all else None, "stock_last": st_all[-1][:10] if st_all else None,
            "stock_first_outside_bulk": st_ok[0][:10] if st_ok else None, "stock_last_outside_bulk": st_ok[-1][:10] if st_ok else None,
            "stock_option_posts_in_bulk_groups": sum(1 for c in st_posts.values() if c["posted"] in bulk_ts),
            "bulk_groups": groups[:30], "bulk_group_count": len(groups),
            "weeks": [dict(week=w, **weeks[w]) for w in sorted(k for k in weeks if k)],
        })
    out.sort(key=lambda r: -(r["fx_posts"] + r["stock_option_posts"]))
    # keep only channels that show both kinds of content, or at least FX signals (the page explains the rest)
    return out


def fx_concentration(mk):
    """How concentrated the pooled market-fill sample is, and how many of its signals are plausibly the same setup.
    Reposts inside 60 minutes are already collapsed upstream; this counts same channel + instrument + side + day groups
    as a proxy for independent observations, and gives the standard error of the mean R so its sign can be judged."""
    n = len(mk)
    if not n:
        return None
    ch = collections.Counter(r.get("channel") for r in mk)
    ins = collections.Counter(r.get("instrument") for r in mk)
    groups = {(r.get("channel"), r.get("instrument"), r.get("side"), (r.get("date") or "")[:10]) for r in mk}
    rs = [r["r_tp1"] for r in mk if fnum(r.get("r_tp1")) is not None]
    m = sum(rs) / len(rs) if rs else None
    se = None
    if len(rs) > 2:
        var = sum((x - m) ** 2 for x in rs) / (len(rs) - 1)
        se = (var / len(rs)) ** 0.5
    dates = sorted((r.get("date") or "")[:10] for r in mk if r.get("date"))
    wd = None
    d0, d1 = parse_date(dates[0]) if dates else None, parse_date(dates[-1]) if dates else None
    if d0 and d1:
        wd = (d1 - d0).days + 1
    top_ch, top_ch_n = ch.most_common(1)[0]
    top_in, top_in_n = ins.most_common(1)[0]
    return {"n": n, "n_channels": len(ch), "top_channel": top_ch, "top_channel_n": top_ch_n,
            "top_instrument": top_in, "top_instrument_n": top_in_n,
            "n_same_day_setup_groups": len(groups), "window_days": wd,
            "mean_r_tp1_se": round(se, 3) if se is not None else None,
            "mean_r_tp1_range95": [round(m - 1.96 * se, 3), round(m + 1.96 * se, 3)] if se is not None else None,
            "mean_r_sign_established": bool(se is not None and (m - 1.96 * se > 0 or m + 1.96 * se < 0)),
            "caveat": (f"{top_ch_n} of {n} market-fill signals come from one channel ({top_ch}) and {top_in_n} are {top_in}; "
                       f"they fall in {len(groups)} same-day channel/instrument/side groups, so they are not {n} independent observations "
                       f"and the ranges understate the uncertainty. The window is {wd} days." if wd else "")}


def build_fx(fx_rows, claims, md, calls=()):
    rows = [r for r in fx_rows if is_public(r.get("channel"))]
    scored = [r for r in rows if r.get("status") == "scored" and r.get("variant") in ("market", "touch")]
    mk = [r for r in scored if r["variant"] == "market"]
    tc = [r for r in scored if r["variant"] == "touch"]
    if not rows:
        return {"available": False, "note": "No scored forex/gold/index signals yet.", "pooled": {"n_signals_scored": 0},
                "by_instrument": [], "by_channel": [], "weekly_by_channel": [], "touch_variant": {"n": 0},
                "sensitivity": None, "assumptions": FX_ASSUMPTIONS, "content_timeline": [], "coverage_funnel": []}
    ms = fx_stats(mk) or {}
    dates = sorted((r.get("date") or "")[:10] for r in scored if r.get("date"))
    pooled = {"n_signals_scored": len(scored), "market_fill_n": len(mk), "touch_fill_n": len(tc),
              "window_start": dates[0] if dates else None, "window_end": dates[-1] if dates else None,
              "outcome_definitions": {
                  "tp1_hit_rate": "TP1 traded before the stop within 24 hours of the fill (share of market-fill signals)",
                  "sl_first_rate": "the stop traded before TP1 within 24 hours (share of market-fill signals)",
                  "tp2plus_rate": "TP2 traded before the stop, among signals that list two or more targets",
                  "mean_r_tp1": "mean result in R (stop distance = 1R) if every trade exits at TP1 or the stop; unresolved marked to the last close",
                  "mean_r_last": "mean result in R if every trade holds for the last target or the stop",
                  "breakeven_tp1_rate": "1 / (1 + average winning TP1 R): the TP1 hit rate needed to break even before costs, for resolved trades"}}
    pooled.update(ms)
    pooled.pop("n", None)
    pooled["variant"] = "market-fill"
    pooled["concentration"] = fx_concentration(mk)

    ids_by = collections.defaultdict(list)
    for r in mk:
        ids_by[r.get("instrument")].append(r)
    touch_by = collections.Counter(r.get("instrument") for r in tc)
    by_instrument = []
    for ins in sorted(set(ids_by) | set(touch_by), key=lambda i: (-len(ids_by.get(i, [])), str(i))):
        st = fx_stats(ids_by.get(ins, [])) or {"n": 0}
        by_instrument.append(dict(instrument=ins, touch_n=touch_by.get(ins, 0), small=st["n"] < SMALL_N, **st))
    ch_mk = collections.defaultdict(list)
    for r in mk:
        ch_mk[r["channel"]].append(r)
    ch_tc = collections.Counter(r["channel"] for r in tc)
    by_channel = []
    for ch in sorted(set(ch_mk) | set(ch_tc), key=lambda c: (-len(ch_mk.get(c, [])), c)):
        st = fx_stats(ch_mk.get(ch, [])) or {"n": 0}
        by_channel.append(dict(channel=ch, touch_n=ch_tc.get(ch, 0), small=st["n"] < SMALL_N, **st))

    # weekly table for channels with enough scored signals
    weekly = []
    by_ch_all = collections.defaultdict(list)
    for r in scored:
        by_ch_all[r["channel"]].append(r)
    for ch, v in sorted(by_ch_all.items(), key=lambda kv: -len(kv[1])):
        if len(v) < FX_WEEKLY_MIN:
            continue
        weeks = sorted({week_monday(r["date"]) for r in rows if r["channel"] == ch and r.get("date")} - {None})
        wrows = []
        for wk in weeks:
            posted = [r for r in rows if r["channel"] == ch and week_monday(r.get("date")) == wk
                      and r.get("skip_reason") not in ("no_levels", "bulk_timestamp", "duplicate_repost", "no_sl", "no_tp")]
            a = [r for r in mk if r["channel"] == ch and week_monday(r["date"]) == wk]
            b = [r for r in tc if r["channel"] == ch and week_monday(r["date"]) == wk]
            st = fx_stats(a)
            wrows.append({"week_start": wk, "distinct_signals_posted": len(posted), "market_n": len(a),
                          "stats": st, "touch_n": len(b), "touch_tp1_hit_rate": rate(sum(1 for r in b if r.get("tp1_hit")), len(b))})
        weekly.append({"channel": ch, "n_scored": len(v), "weeks": wrows,
                       "note": "Week starts Monday (UTC); the last week may be partial. Weekly cells are small: read the range, not the point estimate."})

    touch = {"n": len(tc),
             "note": "Fill-on-touch signals: limit or stop style entries away from the market at post time, filled when price traded into the zone within 4 hours. Reported separately, never pooled with the market-fill variant.",
             "pooled": fx_stats(tc)}
    tb = collections.defaultdict(list)
    for r in tc:
        tb[r.get("instrument")].append(r)
    touch["by_instrument"] = [dict(instrument=i, **fx_stats(v)) for i, v in sorted(tb.items(), key=lambda kv: -len(kv[1]))]
    tcb = collections.defaultdict(list)
    for r in tc:
        tcb[r["channel"]].append(r)
    touch["by_channel"] = [dict(channel=c, small=len(v) < SMALL_N, **fx_stats(v)) for c, v in sorted(tcb.items(), key=lambda kv: -len(kv[1]))]
    skip = collections.Counter(r.get("skip_reason") or r.get("outcome") for r in rows if r.get("status") != "scored")
    funnel = [{"stage": "posts naming an instrument and a side", "n": len(rows)},
              {"stage": "scored: market fill", "n": len(mk)}, {"stage": "scored: touch fill", "n": len(tc)}]
    for k, v in skip.most_common():
        funnel.append({"stage": "not scored: " + str(k), "n": v})
    cl = [c for c in claims if is_public(c.get("channel"))]
    return {"available": True, "pooled": pooled, "by_instrument": by_instrument, "by_channel": by_channel,
            "weekly_by_channel": weekly, "touch_variant": touch, "sensitivity": parse_sensitivity(md),
            "assumptions": FX_ASSUMPTIONS, "assumptions_report": parse_report_assumptions(md),
            "content_timeline": build_content_timeline(calls, rows),
            "coverage_funnel": funnel, "follow_up_claims_not_scored": len(cl)}


def signal_rows(fx_rows):
    out = []
    for r in fx_rows:
        if r.get("status") != "scored" or not is_public(r.get("channel")):
            continue
        out.append({
            "id": r.get("id"), "channel": r.get("channel"), "date": r.get("date"), "instrument": r.get("instrument"),
            "side": r.get("side"), "entry_lo": r.get("entry_lo"), "entry_hi": r.get("entry_hi"), "sl": r.get("sl"),
            "tps": [t.get("v") if isinstance(t, dict) else t for t in (r.get("tps") or [])],
            "variant": r.get("variant"), "outcome": r.get("outcome"), "r_tp1": r.get("r_tp1"), "r_last": r.get("r_last"),
            "minutes_to_first_event": r.get("minutes_to_first_event"), "tps_hit": r.get("tps_hit"),
            "text": clean(" ".join((r.get("text") or "").split()), SIGNAL_TEXT_LEN),
        })
    out.sort(key=lambda r: r.get("date") or "", reverse=True)
    return out


def main():
    API.mkdir(exist_ok=True)
    calls = read_jsonl(TF / "calls.jsonl")
    outcomes = read_jsonl(TF / "outcomes.jsonl")
    fx_rows = read_jsonl(TF / "fx_signals.jsonl")
    claims = read_jsonl(TF / "fx_claims.jsonl")
    md = read_text(FX_REPORT)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sig = signal_rows(fx_rows)
    card = {
        "generated_at": now, "credit": SITE, "disclaimer": DISCLAIMER,
        "source": "AfterMath analysis of public Telegram channel posts against the real tape (Yahoo public bars); passive and read-only",
        "methodology": METHOD_DOC, "methodology_doc": DOC_PATH,
        "conventions": "rates are fractions 0..1; *_ci are Wilson 95% intervals [low, high]; option returns are percent; FX results are in R (stop distance = 1R)",
        "small_sample_rule": f"channel or instrument rows with n under {SMALL_N} are flagged small and hidden by default on the page; they remain in this file",
        "options": build_options(calls, outcomes),
        "fx": build_fx(fx_rows, claims, md, calls),
    }
    fxout = {"generated_at": now, "credit": SITE, "disclaimer": DISCLAIMER, "methodology": METHOD_DOC,
             "count": len(sig), "signals": sig}
    (API / "funnel-scorecard.json").write_text(json.dumps(card, indent=1, ensure_ascii=False))
    (API / "funnel-fx-signals.json").write_text(json.dumps(fxout, indent=1, ensure_ascii=False))
    o, f = card["options"]["pooled"], card["fx"]["pooled"]
    print(f"api/funnel-scorecard.json: options n={o.get('n_scored')}, fx scored={f.get('n_signals_scored')} "
          f"(market {f.get('market_fill_n')}); api/funnel-fx-signals.json: {len(sig)} signals")


if __name__ == "__main__":
    main()
