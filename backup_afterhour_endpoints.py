#!/usr/bin/env python3
"""
Full-fidelity backup and archival of all upstream AfterHour public financial endpoints.
Saves raw JSON responses across:
1. Leaderboard (10 pages, 500 securities, full universe counts)
2. Bulk Prices (All 500 tickers via ?symbols=)
3. Ticker Deep-Dives (Top 60 assets by capital & volume)
4. Historic OHLCV Daily Bars (Major market benchmarks & movers)
5. Whale Portfolios (All public connected portfolios & millionaires)
6. Social Feed (Global live stream + top whale trade logs)
"""

import json
import logging
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

TIMESTAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
ARCHIVE_DIR = DATA_DIR / f"archive_{TIMESTAMP}"
LATEST_SYMLINK = DATA_DIR / "archive_latest"

HEADERS_DESKTOP = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
}
HEADERS_MOBILE = {
    "User-Agent": "okhttp/4.12.0",
    "Accept": "application/json",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def fetch_raw(url: str, headers: dict = None, retries: int = 5, timeout: int = 25):
    """Executes HTTP GET and returns raw bytes, parsed JSON, status code, and latency."""
    if headers is None:
        headers = HEADERS_DESKTOP
    t0 = time.time()
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                raw_bytes = resp.read()
                latency = round(time.time() - t0, 3)
                parsed = json.loads(raw_bytes.decode("utf-8", "replace"))
                return {
                    "ok": True,
                    "status": status,
                    "latency": latency,
                    "bytes": raw_bytes,
                    "json": parsed,
                    "url": url,
                }
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == retries - 1:
                return {
                    "ok": False,
                    "status": e.code,
                    "error": str(e),
                    "latency": round(time.time() - t0, 3),
                    "url": url,
                }
        except Exception as e:
            if attempt == retries - 1:
                return {
                    "ok": False,
                    "status": 0,
                    "error": str(e),
                    "latency": round(time.time() - t0, 3),
                    "url": url,
                }
        backoff = min(1.2 * (2**attempt), 8)
        time.sleep(backoff)


def main():
    logging.info(f"=== Initiating AfterHour API Endpoint Archival -> {ARCHIVE_DIR.name} ===")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    dir_leaderboard = ARCHIVE_DIR / "leaderboard"
    dir_prices = ARCHIVE_DIR / "bulk_prices"
    dir_tickers = ARCHIVE_DIR / "tickers"
    dir_ohlcv = ARCHIVE_DIR / "historic_ohlcv"
    dir_whales = ARCHIVE_DIR / "whales_portfolios"
    dir_feed = ARCHIVE_DIR / "social_feed"

    for d in [dir_leaderboard, dir_prices, dir_tickers, dir_ohlcv, dir_whales, dir_feed]:
        d.mkdir(parents=True, exist_ok=True)

    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "archive_folder": ARCHIVE_DIR.name,
        "sections": {},
    }

    # -------------------------------------------------------------
    # 1. LEADERBOARD (10 Pages = 500 Securities)
    # -------------------------------------------------------------
    logging.info("[1/6] Harvesting Leaderboard (10 pages, take=50)...")
    leaderboard_pages = []
    all_securities = []
    sec_id_to_ticker = {}
    users_to_fetch = {}
    cursor = 0

    for page_idx in range(10):
        url = f"https://api.afterhour.com/stonks/security/leaderboard?take=50&cursor={cursor}"
        res = fetch_raw(url, headers=HEADERS_DESKTOP)
        if not res["ok"]:
            logging.error(f"  Leaderboard page {page_idx} failed: {res.get('error')}")
            break

        data = res["json"]
        page_file = dir_leaderboard / f"leaderboard_page_{page_idx:02d}_cursor_{cursor}.json"
        with open(page_file, "wb") as f:
            f.write(res["bytes"])

        secs = data.get("securities", [])
        all_securities.extend(secs)
        leaderboard_pages.append({
            "page": page_idx,
            "cursor": cursor,
            "count": len(secs),
            "file": page_file.name,
            "latency_s": res["latency"],
        })

        for s in secs:
            sec_obj = s.get("security", {}).get("security", {})
            sid = sec_obj.get("id")
            sym = sec_obj.get("tickerSymbol")
            if sid and sym:
                sec_id_to_ticker[sid] = sym

            # Collect users from ownersSample
            for u in s.get("security", {}).get("ownersSample", []):
                uid = u.get("id")
                uname = u.get("username")
                if uid and uname and uname not in users_to_fetch:
                    users_to_fetch[uname] = u

        cursor = data.get("cursor", cursor + 50)
        time.sleep(0.15)

    # Save consolidated leaderboard
    consolidated_file = dir_leaderboard / "leaderboard_all_500.json"
    with open(consolidated_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_downloaded": len(all_securities),
            "securities": all_securities,
        }, f, indent=2)

    manifest["sections"]["leaderboard"] = {
        "pages_downloaded": len(leaderboard_pages),
        "total_securities": len(all_securities),
        "unique_users_found": len(users_to_fetch),
        "files": [p["file"] for p in leaderboard_pages] + [consolidated_file.name],
    }
    logging.info(f"  [+] Saved {len(all_securities)} securities & discovered {len(users_to_fetch)} users.")

    # -------------------------------------------------------------
    # 2. BULK PRICES (?symbols=)
    # -------------------------------------------------------------
    logging.info("[2/6] Harvesting Multi-Ticker Bulk Prices...")
    all_symbols = [s.get("security", {}).get("security", {}).get("tickerSymbol") for s in all_securities]
    all_symbols = [sym for sym in all_symbols if sym]

    # Batch into chunks of 60 symbols
    chunk_size = 60
    bulk_prices_collected = {}
    price_batches_meta = []

    for i in range(0, len(all_symbols), chunk_size):
        chunk = all_symbols[i:i + chunk_size]
        symbols_param = ",".join(chunk)
        url = f"https://api.afterhour.com/stonks/tickers/prices?symbols={symbols_param}"
        res = fetch_raw(url, headers=HEADERS_DESKTOP)
        batch_idx = (i // chunk_size) + 1
        if res["ok"]:
            p_data = res["json"]
            batch_file = dir_prices / f"prices_batch_{batch_idx:02d}.json"
            with open(batch_file, "wb") as f:
                f.write(res["bytes"])
            prices_list = p_data.get("prices", [])
            for p in prices_list:
                sym = p.get("symbol")
                if sym:
                    bulk_prices_collected[sym] = p
            price_batches_meta.append({
                "batch": batch_idx,
                "symbols_count": len(chunk),
                "prices_returned": len(prices_list),
                "file": batch_file.name,
            })
        else:
            logging.warning(f"  Prices batch {batch_idx} failed: {res.get('error')}")
        time.sleep(0.1)

    consolidated_prices_file = dir_prices / "prices_all_tickers.json"
    with open(consolidated_prices_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_priced": len(bulk_prices_collected),
            "prices": bulk_prices_collected,
        }, f, indent=2)

    manifest["sections"]["bulk_prices"] = {
        "batches": len(price_batches_meta),
        "total_priced": len(bulk_prices_collected),
        "files": [b["file"] for b in price_batches_meta] + [consolidated_prices_file.name],
    }
    logging.info(f"  [+] Saved real-time quotes for {len(bulk_prices_collected)} symbols.")

    # -------------------------------------------------------------
    # 3. TICKER DEEP-DIVES (/stonks/security/ticker/{ticker})
    # -------------------------------------------------------------
    logging.info("[3/6] Harvesting Ticker Deep-Dive Metadata & Chatrooms (Top 60 assets)...")
    # Rank tickers by totalValue & ownerCount
    def ticker_rank_score(s):
        sec = s.get("security", {})
        val = sec.get("totalValue", 0) or 0
        owners = sec.get("ownerCount", 0) or 0
        return val + (owners * 10000)

    ranked_securities = sorted(all_securities, key=ticker_rank_score, reverse=True)
    target_tickers = []
    sec_id_map = {}
    for s in ranked_securities[:60]:
        sec = s.get("security", {}).get("security", {})
        sym = sec.get("tickerSymbol")
        sid = sec.get("id")
        if sym and sym not in target_tickers:
            target_tickers.append(sym)
            if sid:
                sec_id_map[sym] = sid

    # Ensure major benchmarks are present
    anchors = ["NVDA", "TSLA", "AAPL", "SPY", "QQQ", "MSTR", "AMD", "AMZN", "PLTR", "HOOD", "PATH", "COIN", "IWM"]
    for a in anchors:
        if a not in target_tickers:
            target_tickers.append(a)

    ticker_files_meta = []
    def fetch_ticker_job(sym):
        url = f"https://api.afterhour.com/stonks/security/ticker/{sym}"
        res = fetch_raw(url, headers=HEADERS_DESKTOP)
        if res["ok"]:
            fn = dir_tickers / f"{sym}.json"
            with open(fn, "wb") as f:
                f.write(res["bytes"])
            sec_id = res["json"].get("security", {}).get("id")
            return {"symbol": sym, "ok": True, "file": fn.name, "sec_id": sec_id, "latency": res["latency"]}
        return {"symbol": sym, "ok": False, "error": res.get("error")}

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_ticker_job, sym): sym for sym in target_tickers}
        for fut in as_completed(futures):
            res_meta = fut.result()
            if res_meta["ok"]:
                ticker_files_meta.append(res_meta)
                if res_meta.get("sec_id"):
                    sec_id_map[res_meta["symbol"]] = res_meta["sec_id"]

    manifest["sections"]["tickers"] = {
        "targeted": len(target_tickers),
        "downloaded": len(ticker_files_meta),
        "files": [t["file"] for t in ticker_files_meta],
    }
    logging.info(f"  [+] Saved {len(ticker_files_meta)} ticker deep-dive endpoints.")

    # -------------------------------------------------------------
    # 4. HISTORIC DAILY OHLCV BARS (/stonks/security/{secId}/historic_prices)
    # -------------------------------------------------------------
    logging.info("[4/6] Harvesting Historic OHLCV Daily Bars for Key Anchors...")
    start_iso = "2026-07-01T00:00:00.000Z"
    end_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00.000Z")
    ohlcv_files_meta = []

    ohlcv_targets = ["NVDA", "TSLA", "AAPL", "SPY", "QQQ", "MSTR", "HOOD", "PATH", "PLTR", "AMD", "AMZN", "COIN"]
    for sym in ohlcv_targets:
        sid = sec_id_map.get(sym)
        if not sid:
            continue
        url = (
            f"https://api.afterhour.com/stonks/security/{sid}/historic_prices"
            f"?multiplier=1&timespan=day&start={start_iso}&end={end_iso}"
        )
        res = fetch_raw(url, headers=HEADERS_DESKTOP)
        if res["ok"]:
            bars = res["json"].get("prices", [])
            fn = dir_ohlcv / f"{sym}_{sid}_daily.json"
            with open(fn, "wb") as f:
                f.write(res["bytes"])
            ohlcv_files_meta.append({
                "symbol": sym,
                "security_id": sid,
                "bars_count": len(bars),
                "file": fn.name,
            })
        time.sleep(0.15)

    manifest["sections"]["historic_ohlcv"] = {
        "targets": len(ohlcv_files_meta),
        "files": [o["file"] for o in ohlcv_files_meta],
    }
    logging.info(f"  [+] Saved {len(ohlcv_files_meta)} historic OHLCV daily bar series.")

    # -------------------------------------------------------------
    # 5. WHALE PORTFOLIOS (/stonks/public/portfolio/{uid}/summary/live)
    # -------------------------------------------------------------
    logging.info(f"[5/6] Harvesting Live Broker-Verified Portfolios ({len(users_to_fetch)} users)...")
    whales_meta = []

    def fetch_whale_job(u_item):
        uname, u = u_item
        uid = u["id"]
        url = f"https://api.afterhour.com/stonks/public/portfolio/{uid}/summary/live"
        res = fetch_raw(url, headers=HEADERS_MOBILE, timeout=12)
        if res["ok"]:
            data = res["json"]
            val = data.get("totalValue") or data.get("value") or 0.0
            pos_count = len(data.get("positionSnapshots", []))
            # Clean filename
            safe_name = "".join(c for c in uname if c.isalnum() or c in ("_", "-"))
            fn = dir_whales / f"{safe_name}_{uid}.json"
            with open(fn, "wb") as f:
                f.write(res["bytes"])
            return {
                "username": uname,
                "profile_id": uid,
                "total_value": val,
                "positions_count": pos_count,
                "file": fn.name,
                "ok": True,
            }
        return {"username": uname, "profile_id": uid, "ok": False, "error": res.get("error")}

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_whale_job, item): item[0] for item in users_to_fetch.items()}
        for fut in as_completed(futures):
            res_meta = fut.result()
            if res_meta["ok"]:
                whales_meta.append(res_meta)

    whales_meta.sort(key=lambda w: w.get("total_value", 0), reverse=True)
    whales_summary_file = dir_whales / "all_whales_summary.json"
    with open(whales_summary_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_scanned": len(users_to_fetch),
            "total_active_live": len(whales_meta),
            "whales": whales_meta,
        }, f, indent=2)

    manifest["sections"]["whale_portfolios"] = {
        "users_scanned": len(users_to_fetch),
        "portfolios_saved": len(whales_meta),
        "millionaires_count": sum(1 for w in whales_meta if w.get("total_value", 0) >= 1_000_000),
        "summary_file": whales_summary_file.name,
    }
    logging.info(f"  [+] Saved {len(whales_meta)} live portfolios (Millionaires: {manifest['sections']['whale_portfolios']['millionaires_count']}).")

    # -------------------------------------------------------------
    # 6. SOCIAL FEED (Global Stream + Top Whale Post Logs)
    # -------------------------------------------------------------
    logging.info("[6/6] Harvesting Social Feed (Global + Top Whale Logs)...")
    feed_files_meta = []

    # Global Feed (3 pages)
    feed_cursor = None
    for p in range(3):
        url = f"https://api.afterhour.com/social/feed?take=50&contentTypes=post"
        if feed_cursor:
            url += f"&cursor={feed_cursor}"
        res = fetch_raw(url, headers=HEADERS_DESKTOP)
        if res["ok"]:
            items = res["json"].get("items", [])
            fn = dir_feed / f"feed_global_page_{p+1}.json"
            with open(fn, "wb") as f:
                f.write(res["bytes"])
            feed_cursor = res["json"].get("cursor")
            feed_files_meta.append({
                "type": "global",
                "page": p + 1,
                "items_count": len(items),
                "file": fn.name,
            })
            if not feed_cursor:
                break
        time.sleep(0.2)

    # Top Whale Feeds (Top 10 Whales)
    top_whales_for_feed = whales_meta[:10]
    for w in top_whales_for_feed:
        uname = w["username"]
        uid = w["profile_id"]
        url = f"https://api.afterhour.com/social/feed?take=50&contentTypes=post&authorId={uid}"
        res = fetch_raw(url, headers=HEADERS_MOBILE)
        if res["ok"]:
            items = res["json"].get("items", [])
            safe_name = "".join(c for c in uname if c.isalnum() or c in ("_", "-"))
            fn = dir_feed / f"feed_whale_{safe_name}_{uid}.json"
            with open(fn, "wb") as f:
                f.write(res["bytes"])
            feed_files_meta.append({
                "type": "whale",
                "username": uname,
                "items_count": len(items),
                "file": fn.name,
            })
        time.sleep(0.15)

    manifest["sections"]["social_feed"] = {
        "feeds_downloaded": len(feed_files_meta),
        "files": [f["file"] for f in feed_files_meta],
    }
    logging.info(f"  [+] Saved {len(feed_files_meta)} social feed dumps.")

    # -------------------------------------------------------------
    # 7. MANIFEST & DISK FOOTPRINT SUMMARY
    # -------------------------------------------------------------
    total_files = sum(len(list(d.glob("*"))) for d in [dir_leaderboard, dir_prices, dir_tickers, dir_ohlcv, dir_whales, dir_feed])
    total_bytes = sum(f.stat().st_size for f in ARCHIVE_DIR.rglob("*") if f.is_file())

    manifest["total_files"] = total_files
    manifest["total_bytes"] = total_bytes
    manifest["total_megabytes"] = round(total_bytes / (1024 * 1024), 2)

    manifest_file = ARCHIVE_DIR / "manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # Update latest symlink
    try:
        if LATEST_SYMLINK.is_symlink() or LATEST_SYMLINK.exists():
            LATEST_SYMLINK.unlink()
        LATEST_SYMLINK.symlink_to(ARCHIVE_DIR.name)
        logging.info(f"[+] Symlink updated: data/archive_latest -> {ARCHIVE_DIR.name}")
    except Exception as e:
        logging.warning(f"Could not create symlink: {e}")

    logging.info(f"=== Backup Completed Successfully! ===")
    logging.info(f"Total Files: {total_files}")
    logging.info(f"Total Size:  {manifest['total_megabytes']} MB")
    logging.info(f"Directory:   {ARCHIVE_DIR}")


if __name__ == "__main__":
    main()
