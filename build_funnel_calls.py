#!/usr/bin/env python3
"""Build api/funnel-tickers.json and api/funnel-calls.json from the parsed Telegram callouts.

Inputs (all optional, degrades gracefully): data/telegram_funnel/calls.jsonl,
reports/analysis/funnel_tickers.json, data/telegram_funnel/outcomes.jsonl.
Only public channels are exposed. Run standalone or from build_github_pages.py."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
API = BASE / "api"
SITE = "https://telegramscammers.com"
DISCLAIMER = ("Channels and accounts here are flagged for investigation, not a finding of fraud. "
              f"Flag list curated by {SITE}.")
CLAIMS_NOTE = ("quoted_results_are_channel_claims: result_pct is what the channel itself posted, "
               "not verified, and winners dominate quoted closes (survivorship). Use 'outcome' "
               "(scored against the real tape) where present.")
def sample_note(n, start, end):
    span = f" posted {start} to {end}" if start and end else ""
    return (f"Based on {n} scored option callouts{span} from public channels. Scores are hold-to-expiry intrinsic value "
            "against the entry price the channel quoted, with no slippage or fees; most are same-day index and large-cap "
            "options. Channels usually quote early exits, which are not what is scored here. A limited sample, not a "
            "settled rate, and not advice.")
MAX_CALLS = 1000
TEXT_LEN = 160
OUTCOME_KEYS = ["status", "reason", "expiry_effective", "expiry_note", "price_source",
                "underlying_close_at_expiry", "intrinsic", "worthless", "breakeven_level",
                "pnl_per_contract", "return_multiple", "return_pct", "win",
                "touched_breakeven_optimistic", "touch_window"]


def read_jsonl(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        pass
    return rows


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def is_public(channel):
    c = (channel or "").strip().lower()
    return bool(c) and "/+" not in c and "joinchat" not in c


def trunc(s, n=TEXT_LEN):
    s = " ".join((s or "").split()).replace(" \u2014 ", ", ").replace("\u2014", "-")
    return s if len(s) <= n else s[: n - 1].rstrip() + "..."


def main():
    API.mkdir(exist_ok=True)
    tf = BASE / "data" / "telegram_funnel"
    calls = [c for c in read_jsonl(tf / "calls.jsonl") if is_public(c.get("channel"))]
    outcomes = {}
    for o in read_jsonl(tf / "outcomes.jsonl"):
        for i in o.get("ids") or []:
            outcomes[i] = o
    tickers = read_json(BASE / "reports" / "analysis" / "funnel_tickers.json", [])
    if not isinstance(tickers, list):
        tickers = []

    calls.sort(key=lambda c: c.get("posted") or "", reverse=True)
    rows = []
    for c in calls[:MAX_CALLS]:
        r = {k: c.get(k) for k in ("channel", "posted", "ticker", "kind", "side", "strike",
                                   "expiry", "entry_price", "action", "result_pct")}
        r["text"] = trunc(c.get("text"))
        if c.get("parse_flags"):
            r["parse_flags"] = c["parse_flags"]
        o = outcomes.get(c.get("id"))
        if o:
            r["outcome"] = {k: o[k] for k in OUTCOME_KEYS if k in o}
        rows.append(r)

    sc = [o for o in read_jsonl(tf / "outcomes.jsonl") if o.get("status") == "scored" and o.get("return_pct") is not None]
    pd = sorted((o.get("posted") or "")[:10] for o in sc if o.get("posted"))
    from datetime import datetime, timezone
    common = {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "credit": SITE, "disclaimer": DISCLAIMER,
              "small_sample_warning": sample_note(len(sc), pd[0] if pd else None, pd[-1] if pd else None)}
    t_rows = [{k: t.get(k) for k in ("ticker", "ah_accounts", "ah_posts", "tg_channels", "tg_posts")}
              for t in sorted(tickers, key=lambda t: -(t.get("score") or 0))]
    tickers_out = {"source": "AfterMath analysis of flagged AfterHour accounts and public Telegram channels",
                   **common, "count": len(t_rows), "tickers": t_rows}
    calls_out = {"source": "AfterMath parser over public Telegram channel posts (passive, read-only)",
                 **common, "quoted_results_are_channel_claims": CLAIMS_NOTE,
                 "total_parsed": len(calls), "count": len(rows),
                 "calls_with_scored_outcome": sum(1 for r in rows if (r.get("outcome") or {}).get("status") == "scored"),
                 "calls": rows}
    (API / "funnel-tickers.json").write_text(json.dumps(tickers_out, indent=1, ensure_ascii=False))
    (API / "funnel-calls.json").write_text(json.dumps(calls_out, indent=1, ensure_ascii=False))
    print(f"api/funnel-tickers.json: {len(t_rows)} tickers; api/funnel-calls.json: {len(rows)} of {len(calls)} callouts")


if __name__ == "__main__":
    main()
