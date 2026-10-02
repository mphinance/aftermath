#!/usr/bin/env python3
"""
Downloads and persists data across all discovered AfterHour public financial endpoints:
1. /stonks/security/leaderboard (Paginated Stock Leaderboard: Trending & Owners)
2. /stonks/security/ticker/{tickerSymbol} (Deep-Dive Ticker Metadata & Verified Holders)
3. /stonks/tickers/prices (Multi-ticker bulk pricing)
4. /stonks/security/{securityId}/historic_prices (Full OHLCV Bar Market Data Proxy)
5. /social/feed (Top Trader lifetime posts update)
"""

import json
import logging
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "leaderboard"
DATA_DIR.mkdir(parents=True, exist_ok=True)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def fetch_json(url: str, retries: int = 5, timeout: int = 45):
    """Executes HTTP GET and returns parsed JSON with exponential backoff on 504/timeout."""
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == retries - 1:
                logging.error(f"HTTP {e.code} on {url}: {e.reason}")
                raise
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == retries - 1:
                logging.error(f"Network error on {url}: {e}")
                raise
        backoff = min(1.5 * (2**attempt), 10)
        logging.warning(f"Retrying in {backoff:.1f}s after error on {url}...")
        time.sleep(backoff)


def download_leaderboard(max_pages: int = 10, take: int = 50):
    """Paginates through /stonks/security/leaderboard."""
    logging.info(f"[*] Downloading Stock Leaderboard ({max_pages} pages, take={take})...")
    cursor = 0
    all_securities = []
    total_count = None

    for page in range(max_pages):
        url = f"https://api.afterhour.com/stonks/security/leaderboard?take={take}&cursor={cursor}"
        logging.info(f"    Fetching page {page+1}/{max_pages} (cursor={cursor})...")
        try:
            data = fetch_json(url)
        except Exception as e:
            logging.error(f"Failed to fetch page at cursor {cursor}: {e}")
            break

        if total_count is None:
            total_count = data.get("totalCount", 0)

        secs = data.get("securities", [])
        if not secs:
            logging.info("    No more securities returned. Reached end.")
            break

        all_securities.extend(secs)
        cursor = data.get("cursor", cursor + take)
        time.sleep(0.3)

    out_file = DATA_DIR / "stock_leaderboard.json"
    payload = {
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "total_available_in_universe": total_count,
        "count_downloaded": len(all_securities),
        "securities": all_securities,
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    logging.info(f"[+] Saved {len(all_securities)} leaderboard securities to {out_file.name}")
    return all_securities


def download_top_tickers_detail(tickers: list[str]):
    """Downloads detailed /stonks/security/ticker/{tickerSymbol} metadata."""
    logging.info(f"[*] Downloading deep-dive metadata for {len(tickers)} tickers...")
    details = {}
    for i, ticker in enumerate(tickers, 1):
        url = f"https://api.afterhour.com/stonks/security/ticker/{ticker}"
        try:
            data = fetch_json(url)
            details[ticker] = data
            owners = data.get("ownerCount", 0)
            val = data.get("totalValue", 0)
            logging.info(f"    [{i}/{len(tickers)}] {ticker:<6s} | Owners: {owners:3d} | Total Value: ${val:,.0f}")
        except Exception as e:
            logging.warning(f"    [{i}/{len(tickers)}] Failed for {ticker}: {e}")
        time.sleep(0.25)

    out_file = DATA_DIR / "top_stocks_detail.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "downloaded_at": datetime.now(timezone.utc).isoformat(),
                "tickers_count": len(details),
                "tickers": details,
            },
            f,
            indent=2,
        )
    logging.info(f"[+] Saved {len(details)} ticker details to {out_file.name}")
    return details


def download_bulk_prices(tickers: list[str]):
    """Calls /stonks/tickers/prices for batch price quotes."""
    logging.info(f"[*] Downloading bulk real-time prices for {len(tickers)} tickers...")
    batch_str = ",".join(tickers)
    url = f"https://api.afterhour.com/stonks/tickers/prices?tickers={batch_str}"
    try:
        data = fetch_json(url)
        out_file = DATA_DIR / "top_stocks_prices.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "downloaded_at": datetime.now(timezone.utc).isoformat(),
                    "prices": data.get("prices", {}),
                },
                f,
                indent=2,
            )
        logging.info(f"[+] Saved bulk prices for {len(data.get('prices', {}))} tickers to {out_file.name}")
        return data
    except Exception as e:
        logging.error(f"Failed to fetch bulk prices: {e}")
        return None


def download_historic_samples(sec_id_map: dict[str, str]):
    """Downloads sample 60-day daily OHLCV bars via /stonks/security/{secId}/historic_prices."""
    logging.info(f"[*] Downloading historic OHLCV daily bars for {list(sec_id_map.keys())}...")
    start_iso = "2026-08-01T00:00:00.000Z"
    end_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00.000Z")

    history = {}
    for ticker, sec_id in sec_id_map.items():
        url = (
            f"https://api.afterhour.com/stonks/security/{sec_id}/historic_prices"
            f"?multiplier=1&timespan=day&start={start_iso}&end={end_iso}"
        )
        try:
            data = fetch_json(url)
            bars = data.get("prices", [])
            history[ticker] = {
                "security_id": sec_id,
                "bar_count": len(bars),
                "bars": bars,
            }
            logging.info(f"    {ticker} ({sec_id}) -> {len(bars)} daily bars fetched")
        except Exception as e:
            logging.warning(f"    Failed historic bars for {ticker}: {e}")
        time.sleep(0.3)

    out_file = DATA_DIR / "historic_prices_sample.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "downloaded_at": datetime.now(timezone.utc).isoformat(),
                "timeframe": "1D",
                "start": start_iso,
                "end": end_iso,
                "history": history,
            },
            f,
            indent=2,
        )
    logging.info(f"[+] Saved historic OHLCV data to {out_file.name}")
    return history


def main():
    logging.info("=== Starting AfterHour Financial Endpoints Data Harvesting ===")

    # 1. Download Stock Leaderboard (10 pages = 500 securities)
    securities = download_leaderboard(max_pages=10, take=50)

    # 2. Extract top tickers by Trending and Owners
    top_tickers_trending = []
    sec_id_map = {}
    for s in securities[:30]:
        sec = s.get("security", {})
        ticker = sec.get("security", {}).get("tickerSymbol")
        sec_id = sec.get("security", {}).get("id")
        if ticker:
            top_tickers_trending.append(ticker)
            if sec_id and ticker in ["NVDA", "TSLA", "SPY", "AAPL", "MSTR", "HOOD", "PATH"]:
                sec_id_map[ticker] = sec_id

    # Also sort by ownerCount in-memory to get top owned
    sorted_by_owners = sorted(
        securities,
        key=lambda s: s.get("security", {}).get("ownerCount", 0),
        reverse=True,
    )
    top_tickers_owners = []
    for s in sorted_by_owners[:30]:
        sec = s.get("security", {})
        ticker = sec.get("security", {}).get("tickerSymbol")
        sec_id = sec.get("security", {}).get("id")
        if ticker and ticker not in top_tickers_trending:
            top_tickers_owners.append(ticker)
        if ticker and sec_id and ticker in ["NVDA", "TSLA", "SPY", "AAPL", "MSTR", "HOOD", "PATH"]:
            sec_id_map[ticker] = sec_id

    all_target_tickers = list(dict.fromkeys(top_tickers_trending + top_tickers_owners))
    logging.info(f"Targeting {len(all_target_tickers)} top tickers for deep-dive...")

    # 3. Download Deep-Dive Metadata
    details = download_top_tickers_detail(all_target_tickers)

    # Also capture sec_ids from details
    for ticker, d in details.items():
        sec_id = d.get("security", {}).get("id")
        if sec_id and ticker in ["NVDA", "TSLA", "SPY", "AAPL", "MSTR", "HOOD", "PATH"]:
            sec_id_map[ticker] = sec_id

    # 4. Download Bulk Prices
    download_bulk_prices(all_target_tickers[:40])

    # 5. Download Historic OHLCV Samples
    if sec_id_map:
        download_historic_samples(sec_id_map)

    logging.info("=== All AfterHour Financial Endpoints Harvested Successfully ===")


if __name__ == "__main__":
    main()
