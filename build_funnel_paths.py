#!/usr/bin/env python3
"""Build api/funnel-option-paths.json: how the option contracts called out in public Telegram channels traded AFTER the call.

Input: data/telegram_funnel/option_paths.jsonl (written by `python3 tg_option_paths.py score` from real 5-minute option
trade bars; the bars are local only). The delay sensitivity re-runs the scorer in-process (tg_option_paths.score) and
needs the local bar archive; when bars or the scorer are missing it reuses the previous output file's block instead.
Missing input entirely: the previous output is left untouched. Stdlib only. Every number is computed from the data.

Run order: python3 tg_option_paths.py score; python3 build_funnel_paths.py
"""
import collections
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
OUT = BASE / "api" / "funnel-option-paths.json"
ROWS = BASE / "data" / "telegram_funnel" / "option_paths.jsonl"
CALLS = BASE / "data" / "telegram_funnel" / "calls.jsonl"
SITE = "https://telegramscammers.com"
DISCLAIMER = ("Analysis of public posts. The channels and accounts are flagged for investigation, not a finding of fraud. "
              f"Flag list curated by {SITE}. Statistical description under stated assumptions, not advice.")
SMALL_N = 25          # channel / ticker / hour rows under this many scored calls are flagged small
UNFILLABLE_PCT = 25   # quoted entry this far below the contract's price at the post cannot have been filled
THIN_VOLUME = 20      # window volume (contracts) under this counts as thin
DELAYS = (0, 1, 2, 3)

try:
    import tg_option_paths as TP
    WINDOW_MIN = TP.WINDOW_MIN
    MAX_GAP = TP.MAX_FILL_GAP_MIN
    RULES = list(TP.RULES)
except Exception:                                  # scorer unavailable: static copy of its constants, for text only
    TP = None
    WINDOW_MIN, MAX_GAP = 30, 15
    RULES = [("tp50_sl50", 0.50, 0.50), ("tp100_sl50", 1.00, 0.50), ("tp30_sl30", 0.30, 0.30)]
HEADLINE_RULE = RULES[0][0]


def wilson(k, n, z=1.96):
    """Wilson score interval for k successes in n trials; [None, None] when n == 0."""
    if not n:
        return [None, None]
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def is_public(channel):
    c = (channel or "").strip().lower()
    return bool(c) and "/+" not in c and "joinchat" not in c


def read_jsonl(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except ValueError:
                        continue
    except OSError:
        pass
    return rows


def _med(xs):
    return round(statistics.median(xs), 1) if xs else None


def _mean(xs):
    return round(statistics.mean(xs), 1) if xs else None


def _share(k, n):
    return {"k": k, "n": n, "rate": round(k / n, 4) if n else None, "ci": wilson(k, n)}


def rule_table(rows):
    """Per rule: tp_first / sl_first / neither counts, rates with Wilson ranges, mean return (percent of the fill)."""
    n = len(rows)
    out = []
    for name, tp, sl in RULES:
        c = collections.Counter(r.get(name) for r in rows)
        rets = [r[name + "_ret"] for r in rows if r.get(name + "_ret") is not None]
        out.append({"rule": name, "take_profit_pct": round(tp * 100), "stop_loss_pct": round(sl * 100), "n": n,
                    "tp_first": c["tp"], "sl_first": c["sl"], "neither": c["none"],
                    "tp_first_rate": round(c["tp"] / n, 4) if n else None, "tp_first_ci": wilson(c["tp"], n),
                    "sl_first_rate": round(c["sl"] / n, 4) if n else None, "sl_first_ci": wilson(c["sl"], n),
                    "neither_rate": round(c["none"] / n, 4) if n else None,
                    "mean_return_pct": _mean(rets)})
    return out


def realism(rows):
    q = [r["quoted_vs_fill_pct"] for r in rows if r.get("quoted_vs_fill_pct") is not None]
    n = len(q)
    within = sum(1 for x in q if abs(x) <= UNFILLABLE_PCT)
    below = sum(1 for x in q if x < -UNFILLABLE_PCT)
    above = sum(1 for x in q if x > UNFILLABLE_PCT)
    return {"n": n, "median_quoted_vs_fill_pct": _med(q),
            "within_25pct": _share(within, n), "unfillable_quote_more_than_25pct_below_fill": _share(below, n),
            "quoted_more_than_25pct_above_fill": _share(above, n)}


def liquidity(rows):
    v = [r.get("volume") or 0 for r in rows]
    n = len(v)
    return {"n": n, "median_window_volume": _med(v), "thin_under_20_contracts": _share(sum(1 for x in v if x < THIN_VOLUME), n)}


def block(rows, full=True):
    """Compact stats for one group of scored rows."""
    n = len(rows)
    green = sum(1 for r in rows if r["end_ret_pct"] > 0)
    mfe = [r["mfe_pct"] for r in rows]
    mae = [r["mae_pct"] for r in rows]
    end = [r["end_ret_pct"] for r in rows]
    out = {"n": n, "ended_green": _share(green, n),
           "peak_pct": {"median": _med(mfe), "mean": _mean(mfe)},
           "drawdown_pct": {"median": _med(mae), "mean": _mean(mae)},
           "end_return_pct": {"median": _med(end), "mean": _mean(end)},
           "rules": rule_table(rows)}
    hr = next((x for x in out["rules"] if x["rule"] == HEADLINE_RULE), None)
    if hr:
        out["headline_rule"] = {k: hr[k] for k in ("rule", "tp_first", "sl_first", "neither", "tp_first_rate", "sl_first_rate",
                                                   "tp_first_ci", "sl_first_ci", "mean_return_pct")}
    if full:
        out["liquidity"] = liquidity(rows)
        out["quoted_entry_realism"] = realism(rows)
    return out


def row_for(key, name, rows):
    """Flat row for the by-channel / by-ticker / by-hour tables."""
    n = len(rows)
    green = sum(1 for r in rows if r["end_ret_pct"] > 0)
    hr = next((x for x in rule_table(rows) if x["rule"] == HEADLINE_RULE), None) if rows else None
    q = [r["quoted_vs_fill_pct"] for r in rows if r.get("quoted_vs_fill_pct") is not None]
    out = {key: name, "n": n, "small": n < SMALL_N,
           "green_rate": round(green / n, 4) if n else None, "green_ci": wilson(green, n),
           "median_peak_pct": _med([r["mfe_pct"] for r in rows]), "median_drawdown_pct": _med([r["mae_pct"] for r in rows]),
           "median_end_return_pct": _med([r["end_ret_pct"] for r in rows]), "mean_end_return_pct": _mean([r["end_ret_pct"] for r in rows]),
           "tp_first_rate": hr["tp_first_rate"] if hr else None, "tp_first_ci": hr["tp_first_ci"] if hr else [None, None],
           "sl_first_rate": hr["sl_first_rate"] if hr else None, "sl_first_ci": hr["sl_first_ci"] if hr else [None, None],
           "rule_mean_return_pct": hr["mean_return_pct"] if hr else None,
           "median_window_volume": _med([r.get("volume") or 0 for r in rows]),
           "unfillable_quote_rate": round(sum(1 for x in q if x < -UNFILLABLE_PCT) / len(q), 4) if q else None,
           "unfillable_quote_n": len(q)}
    return out


def et_hour(posted):
    try:
        from zoneinfo import ZoneInfo
        t = datetime.fromisoformat(posted.replace("Z", "+00:00")).astimezone(ZoneInfo("America/New_York"))
        return t.hour
    except Exception:
        return None


def hour_label(h):
    return f"{h:02d}:{30 if h == 9 else 0:02d} to {h:02d}:59 ET"   # the session opens at 9:30


def reason_bucket(reason):
    r = (reason or "").lower()
    if r.startswith("illiquid"):
        return "illiquid: first print more than %d minutes after the post or the open" % MAX_GAP
    if "expired before" in r:
        return "contract expired before the evaluation session"
    if "no bars after the fill delay" in r:
        return "no bars after the fill delay"
    if "no fill" in r:
        return "no fill price"
    return reason or "other"


def coverage(rows, total_opens):
    """Funnel: option opens -> parseable contract -> bars -> scored, with unscorable reasons and the intraday / daily split."""
    st = collections.Counter(r.get("status") for r in rows)
    reasons = collections.Counter(reason_bucket(r.get("reason")) for r in rows if r.get("status") == "unscorable")
    nobars = collections.Counter(r.get("category") or "unknown" for r in rows if r.get("status") == "no_bars")
    sc = [r for r in rows if r.get("status") == "scored"]
    stages = []
    if total_opens is not None:
        stages.append({"stage": "Option open callouts (repeat posts removed)", "n": total_opens})
    stages += [
        {"stage": "With a parseable contract (ticker, side, strike, expiry)", "n": len(rows)},
        {"stage": "No bars for the evaluation window (not captured, not listed, or no trades)", "n": st["no_bars"]},
        {"stage": "Unscorable (see reasons)", "n": st["unscorable"]},
        {"stage": "Coarse day view only (no 5-minute bars; not in the headline)", "n": st["day_view"]},
        {"stage": "Scored from 5-minute bars", "n": len(sc)},
        {"stage": "  of which intraday (30-minute window)", "n": sum(1 for r in sc if r.get("category") == "intraday")},
        {"stage": "  of which daily callout (whole next session)", "n": sum(1 for r in sc if r.get("category") == "daily")},
    ]
    return {"stages": stages, "unscorable_by_reason": [{"reason": k, "n": v} for k, v in reasons.most_common()],
            "no_bars_by_category": dict(nobars), "status_counts": dict(st)}


def count_total_opens():
    """Option opens in calls.jsonl, echoes removed (same filter as the scorer); None when the file is not available."""
    if not CALLS.exists():
        return None
    echo = {"duplicate_echo", "cross_channel_echo"}
    n = 0
    for c in read_jsonl(CALLS):
        if c.get("kind") == "option" and c.get("action") == "open" and not (echo & set(c.get("parse_flags") or [])) and is_public(c.get("channel")):
            n += 1
    return n


def delay_row(d, rows):
    g = [r for r in rows if r.get("status") == "scored" and r.get("category") == "intraday" and is_public(r.get("channel"))]
    n = len(g)
    green = sum(1 for r in g if r["end_ret_pct"] > 0)
    hr = next((x for x in rule_table(g) if x["rule"] == HEADLINE_RULE), None) if g else None
    return {"delay_bars": d, "delay_minutes": d * 5, "n": n, "green_rate": round(green / n, 4) if n else None,
            "green_ci": wilson(green, n), "mean_end_return_pct": _mean([r["end_ret_pct"] for r in g]),
            "tp_first_rate": hr["tp_first_rate"] if hr else None, "sl_first_rate": hr["sl_first_rate"] if hr else None,
            "rule_mean_return_pct": hr["mean_return_pct"] if hr else None}


def delay_sensitivity(base_rows, previous):
    """Fill N five-minute bars later. Needs the local bar archive; otherwise the previous file's block is reused."""
    note = "Re-scored from the local bar archive with the fill moved N five-minute bars after the post (intraday calls only)."
    if TP is not None:
        try:
            out = []
            for d in DELAYS:
                rows = base_rows if d == 0 else TP.score(d, write=False)
                out.append(delay_row(d, rows))
            if out[0]["n"] > 0:
                return {"rows": out, "note": note, "rule": HEADLINE_RULE, "reused_from_previous": False}
        except Exception as e:                      # missing calls.jsonl or bars
            print(f"delay sensitivity unavailable ({type(e).__name__}); reusing previous block", file=sys.stderr)
    prev = (previous or {}).get("delay_sensitivity")
    if prev and prev.get("rows"):
        prev = dict(prev)
        prev["reused_from_previous"] = True
        prev["note"] = note + " Reused from the previous build because the bar archive is not available here."
        return prev
    return {"rows": [], "note": note + " Not available: no bar archive on this machine and no previous block.", "rule": HEADLINE_RULE,
            "reused_from_previous": False}


def methodology():
    rule_txt = "; ".join(f"+{round(tp * 100)}% / -{round(sl * 100)}%" for _, tp, sl in RULES)
    return {
        "windows": {
            "intraday": f"Calls posted during the regular session (9:30 to 16:00 ET): the {WINDOW_MIN} minutes of 5-minute bars after the call.",
            "daily": "Daily callouts (posted before the open, after the close, or on a weekend): the whole next regular session.",
        },
        "fill_rule": ("The fill is the open of the first 5-minute bar at or after the post (or the session open for daily callouts). "
                      f"If no trade printed within {MAX_GAP} minutes of the post (or the open) the call is unscorable as illiquid, not scored."),
        "rules": {
            "list": rule_txt,
            "definition": ("A rule is take-profit / stop-loss measured from the fill. TP first means the take-profit level traded before the stop; "
                           "SL first means the stop traded first; neither means neither level traded inside the window and the position is valued at the last bar's close. "
                           "A bar that touches both levels counts as the stop. The headline rule is " + f"+{round(RULES[0][1] * 100)}% / -{round(RULES[0][2] * 100)}%."),
        },
        "ended_green_definition": "Ended green means the last bar's close in the window was above the fill price. It is not a trading win rate.",
        "assumptions": [
            "Every called-out contract is judged by its own traded price after the post, not by the underlying and not at expiry.",
            f"Intraday calls get {WINDOW_MIN} minutes because these channels post quick scalps; daily callouts get the whole next regular session.",
            "Fill is the open of the first 5-minute trade bar at or after the post, so it is a trade print, not a quote you could have hit.",
            "Peak is the highest traded price in the window relative to the fill; drawdown is the lowest, relative to the fill.",
            "Repost de-duplication: the same trade posted again (same channel, or copied across channels) is collapsed to the first post before scoring.",
            "A post is scored once per contract. The channel's own quoted entry is shown only to test whether it could have been filled.",
            "Only public channels are scored. Parsing is automatic and can be wrong.",
        ],
        "limitations": [
            "Bars are trade prints, not bid and ask. Spread and slippage are NOT modelled, so true results for someone trading these calls would be worse, most of all on wide-spread, low-priced contracts.",
            "Option bars come from an indicative data feed; some venues or prints may be missing and a bar's open may differ from what was available at the second of the post.",
            f"The {WINDOW_MIN}-minute window is short by design. It describes what happened right after a call, not what a different exit rule or a longer hold would have done.",
            "A same-bar tie between the take-profit and stop-loss levels counts as the stop, which is conservative; the true order inside a 5-minute bar is unknown.",
            "A quoted entry far below the contract's traded price at the post could not have been filled; those are counted and shown rather than removed.",
            "The sample covers a limited date range and a few busy channels; rates describe this sample and are not settled estimates.",
            "Calls with no bars, thin trading or an illiquid first print are excluded from the scored sample (see the coverage funnel), which can flatter or penalise the result.",
            "Not advice. Flagged for investigation, not a finding of fraud.",
        ],
    }


def build(rows, previous=None, total_opens=None, generated_at=None):
    rows = [r for r in rows if is_public(r.get("channel"))]
    scored = [r for r in rows if r.get("status") == "scored"]
    intr = [r for r in scored if r.get("category") == "intraday"]
    daily = [r for r in scored if r.get("category") == "daily"]
    posted = sorted((r.get("posted") or "")[:10] for r in scored if r.get("posted"))

    chans = sorted({r["channel"] for r in scored})
    by_channel = []
    for c in chans:
        i = [r for r in intr if r["channel"] == c]
        row = row_for("channel", c, i)
        row["n_daily"] = sum(1 for r in daily if r["channel"] == c)
        by_channel.append(row)
    by_channel.sort(key=lambda r: (-r["n"], r["channel"]))

    tk = collections.Counter(r["ticker"] for r in intr)
    by_ticker = [row_for("ticker", t, [r for r in intr if r["ticker"] == t]) for t, _ in tk.most_common(15)]

    hours = collections.defaultdict(list)
    for r in intr:
        h = et_hour(r.get("posted") or "")
        if h is not None:
            hours[h].append(r)
    by_hour = []
    for h in sorted(hours):
        row = row_for("hour", hour_label(h), hours[h])
        row["hour_et"] = h
        by_hour.append(row)

    out = {
        "generated_at": generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "credit": SITE, "disclaimer": DISCLAIMER,
        "methodology": methodology(),
        "window_start": posted[0] if posted else None, "window_end": posted[-1] if posted else None,
        "small_n_threshold": SMALL_N,
        "coverage": coverage(rows, total_opens),
        "pooled": {"intraday": block(intr), "daily": block(daily)},
        "delay_sensitivity": delay_sensitivity(rows, previous),
        "by_channel": by_channel, "by_ticker": by_ticker, "by_session_hour": by_hour,
        "n_channels": len(chans),
    }
    return out


def main():
    rows = read_jsonl(ROWS)
    if not rows and TP is not None:
        try:
            rows = TP.score(0, write=False)
        except Exception:
            rows = []
    if not rows:
        print("no option_paths.jsonl and no bars: leaving the previous api/funnel-option-paths.json untouched")
        return 0
    try:
        previous = json.load(open(OUT, encoding="utf-8"))
    except (OSError, ValueError):
        previous = None
    out = build(rows, previous, count_total_opens())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    i = out["pooled"]["intraday"]
    print(f"api/funnel-option-paths.json: intraday n={i['n']}, daily n={out['pooled']['daily']['n']}, {out['n_channels']} channels, "
          f"{out['window_start']} to {out['window_end']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
