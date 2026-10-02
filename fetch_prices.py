#!/usr/bin/env python3
"""
Daily OHLCV + earnings dates for every underlying a trader held or cashtagged,
so position changes can be read against what the stock was doing.

    python3 fetch_prices.py wTF [--start 2023-08-01 --end 2025-09-30] [--extra SPY QQQ ^VIX]

Needs yfinance (pip install yfinance). Writes data/prices/@<user>_prices.json.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yfinance as yf

BASE_DIR = Path(__file__).resolve().parent
NOT_TICKERS = {"USD", "CEO", "ATH", "DTE", "FOMO", "EOD", "IV", "OTM", "ITM", "PM", "AH", "YOLO",
               "DD", "PT", "TA", "EPS", "IPO", "ETF", "CPI", "FOMC", "GDP", "AI", "US", "USA"}


def tickers_for(username):
    found = set()
    pos = BASE_DIR / "data" / "positions" / f"@{username}_positions.json"
    if pos.exists():
        found |= {l["rootTickerSymbol"] for l in json.load(open(pos))["legs"] if l.get("rootTickerSymbol")}
    for p in json.load(open(BASE_DIR / "data" / "following" / f"@{username}_all_posts.json")):
        text = f"{p.get('title') or ''} {p.get('body') or ''}"
        found |= set(re.findall(r"\$([A-Z]{1,6})\b", text))
        found |= {t for t in (p.get("tickers") or "").split(",") if t}
    return sorted(found - NOT_TICKERS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("username")
    ap.add_argument("--start", default="2023-08-01")
    ap.add_argument("--end", default="2025-09-30")
    ap.add_argument("--extra", nargs="*", default=["SPY", "QQQ", "^VIX"])
    args = ap.parse_args()
    username = args.username.lstrip("@")

    out = {"start": args.start, "end": args.end, "bars": {}, "earnings": {}, "missing": []}
    for t in tickers_for(username) + args.extra:
        hist = yf.Ticker(t).history(start=args.start, end=args.end, auto_adjust=False)
        if hist.empty:
            out["missing"].append(t)
            print(f"[-] {t}: no data", file=sys.stderr)
            continue
        out["bars"][t] = [
            {"date": d.strftime("%Y-%m-%d"), "open": round(r.Open, 4), "high": round(r.High, 4),
             "low": round(r.Low, 4), "close": round(r.Close, 4), "volume": int(r.Volume)}
            for d, r in hist.iterrows()
        ]
        try:
            ed = yf.Ticker(t).get_earnings_dates(limit=16)
            if ed is not None:
                out["earnings"][t] = sorted(
                    d.strftime("%Y-%m-%d") for d in ed.index
                    if args.start <= d.strftime("%Y-%m-%d") <= args.end
                )
        except Exception:
            pass
        print(f"[+] {t}: {len(out['bars'][t])} bars, {len(out['earnings'].get(t, []))} earnings dates")

    dest = BASE_DIR / "data" / "prices" / f"@{username}_prices.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(dest, "w"))
    print(f"wrote {dest.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
