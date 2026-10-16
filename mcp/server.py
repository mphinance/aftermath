#!/usr/bin/env python3
"""
AfterMath Model Context Protocol (MCP) Server
============================================
Zero-dependency, production-grade MCP server exposing real-time AfterHour alt-data,
whale holdings, conviction intensity, and macro tape liquidity to AI agents
(Claude Desktop, Cursor IDE, Antigravity CLI, Windsurf, custom autonomous loops).

Protocol: Model Context Protocol (MCP) Specification (2025-06-18 / 2025-03-26 / 2024-11-05)
Transport: stdio (JSON-RPC 2.0), legacy HTTP+SSE, and stateless Streamable HTTP
Endpoints Source: https://ah.mphinance.com/api
Dependencies: None (Standard Python 3.8+ library only)
"""

import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse
import http.server
import uuid
import queue
import threading
from pathlib import Path

VERSION = "1.3.0"
SERVER_NAME = "aftermath-altdata"
BASE_URL = "https://ah.mphinance.com/api"

# Protocol versions this server understands, newest first. We echo the client's
# requested version when we support it (required by the MCP spec: "If the server
# supports the requested protocol version, it MUST respond with the same
# version"). Clients such as Google Antigravity require >= 2025-03-26 and will
# drop the connection if the server answers with the legacy 2024-11-05.
SUPPORTED_PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
DEFAULT_PROTOCOL_VERSION = SUPPORTED_PROTOCOL_VERSIONS[0]

# Local fallback cache directory if available
SCRIPT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
LOCAL_API_DIR = SCRIPT_DIR / "api"

# In-memory cache for API payloads (60-second TTL)
_CACHE = {}
_CACHE_LOCK = threading.Lock()
_CACHE_TTL = 60.0

# In-memory SSE message sessions
_SESSIONS = {}
_SESSIONS_LOCK = threading.Lock()
SERVER_START_TIME = time.time()

def debug_log(msg: str):
    """Write debug log message to stderr (never stdout to avoid corrupting JSON-RPC)."""
    sys.stderr.write(f"[{SERVER_NAME}] {msg}\n")
    sys.stderr.flush()

def fetch_json(endpoint: str):
    """Fetch JSON from local disk if available, otherwise fetch from edge API with cache."""
    now = time.time()
    with _CACHE_LOCK:
        if endpoint in _CACHE:
            data, ts = _CACHE[endpoint]
            if now - ts < _CACHE_TTL:
                return data

    # 1. Try local repository file
    local_path = LOCAL_API_DIR / endpoint
    if local_path.exists():
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                with _CACHE_LOCK:
                    _CACHE[endpoint] = (data, now)
                return data
        except Exception as e:
            debug_log(f"Local file read failed for {endpoint}: {e}")

    # 2. Try remote API
    url = f"{BASE_URL}/{endpoint}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": f"AfterMath-MCP/{VERSION} (+https://ah.mphinance.com/mcp)",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            with _CACHE_LOCK:
                _CACHE[endpoint] = (data, now)
            return data
    except Exception as e:
        debug_log(f"Remote fetch failed for {url}: {e}")
        return None


# ==============================================================================
# TOOL IMPLEMENTATIONS
# ==============================================================================

def tool_get_market_tape(args: dict) -> dict:
    """Retrieve real-time macro tape overview and liquidity."""
    data = fetch_json("market.json")
    if not data:
        # Fallback to computing from stonks.json and whales.json
        stonks_data = fetch_json("stonks.json") or {}
        whales_data = fetch_json("whales.json") or {}
        return {
            "error": "market.json currently synchronizing",
            "source": BASE_URL,
            "stonks_count": stonks_data.get("total", 0),
            "whales_count": whales_data.get("total", 0)
        }
    return data

def tool_get_top_equities(args: dict) -> dict:
    """Filter and rank 500 verified stocks with customizable thresholds."""
    limit = int(args.get("limit", 20))
    min_whale_capital = float(args.get("min_whale_capital", 0))
    min_conviction = float(args.get("min_conviction", 0))
    min_owners = int(args.get("min_owners", 0))
    min_price = float(args.get("min_price", 0))
    max_price = float(args.get("max_price", 0))
    min_volume = float(args.get("min_volume", 0))
    asset_type = args.get("asset_type", "all").lower()
    sort_by = args.get("sort_by", "whale_capital").lower()

    data = fetch_json("stonks.json")
    if not data or "securities" not in data:
        return {"error": "Failed to load securities from edge API"}

    securities = data["securities"]

    # Filter
    filtered = []
    for s in securities:
        if asset_type == "stocks" and s.get("isETF"):
            continue
        if asset_type == "etfs" and not s.get("isETF"):
            continue
        if s.get("whalesValue", 0) < min_whale_capital:
            continue
        if s.get("intensity", 0) < min_conviction:
            continue
        if s.get("owners", 0) < min_owners:
            continue
        price = float(s.get("price") or 0.0)
        if min_price > 0 and price < min_price:
            continue
        if max_price > 0 and price > max_price:
            continue
        vol = float(s.get("volume") or 0)
        if min_volume > 0 and vol < min_volume:
            continue

        filtered.append({
            "ticker": s.get("ticker"),
            "name": s.get("name"),
            "price": s.get("price"),
            "changePercent": s.get("changePercent"),
            "isETF": s.get("isETF"),
            "whaleCapital": s.get("whalesValue"),
            "totalValue": s.get("totalValue"),
            "owners": s.get("owners"),
            "convictionPerHolder": round(s.get("intensity", 0), 2),
            "chatroomMembers": s.get("chatroomMembers"),
            "whyTop": s.get("whyTop")
        })

    # Sort
    if sort_by == "total_value":
        filtered.sort(key=lambda x: x["totalValue"], reverse=True)
    elif sort_by == "owners":
        filtered.sort(key=lambda x: x["owners"], reverse=True)
    elif sort_by in ("conviction", "conviction_intensity"):
        filtered.sort(key=lambda x: x["convictionPerHolder"], reverse=True)
    elif sort_by in ("change_percent", "price_change_pct"):
        filtered.sort(key=lambda x: x["changePercent"], reverse=True)
    elif sort_by == "price":
        filtered.sort(key=lambda x: x["price"] or 0, reverse=True)
    else:  # whale_capital
        filtered.sort(key=lambda x: x["whaleCapital"], reverse=True)

    return {
        "total_matched": len(filtered),
        "limit": limit,
        "results": filtered[:limit]
    }

def tool_get_etf_flows(args: dict) -> dict:
    """Inspect 64 ETFs ranked by whale backing, expense ratios, asset classes, and crowd breadth."""
    limit = int(args.get("limit", 20))
    sort_by = args.get("sort_by", "whale_capital").lower()
    asset_class = (args.get("asset_class") or "all").lower()

    data = fetch_json("etfs.json")
    if not data or "securities" not in data:
        return {"error": "Failed to load ETFs from edge API"}

    etfs = data["securities"]
    formatted = []
    for e in etfs:
        ac = (e.get("assetClass") or "").lower()
        if asset_class != "all" and asset_class not in ac:
            continue

        formatted.append({
            "ticker": e.get("ticker"),
            "name": e.get("name"),
            "price": e.get("price"),
            "changePercent": e.get("changePercent"),
            "whaleCapital": e.get("whalesValue"),
            "totalValue": e.get("totalValue"),
            "owners": e.get("owners"),
            "convictionPerHolder": round(e.get("intensity", 0), 2),
            "expenseRatio": e.get("expenseRatio"),
            "assetClass": e.get("assetClass"),
            "category": e.get("category")
        })

    if sort_by == "owners":
        formatted.sort(key=lambda x: x["owners"], reverse=True)
    elif sort_by == "total_value":
        formatted.sort(key=lambda x: x["totalValue"], reverse=True)
    elif sort_by == "change_percent":
        formatted.sort(key=lambda x: x["changePercent"], reverse=True)
    elif sort_by == "conviction":
        formatted.sort(key=lambda x: x["convictionPerHolder"], reverse=True)
    elif sort_by == "expense_ratio":
        formatted.sort(key=lambda x: x["expenseRatio"] or 0)
    else:
        formatted.sort(key=lambda x: x["whaleCapital"], reverse=True)

    return {
        "total_etfs": len(formatted),
        "limit": limit,
        "results": formatted[:limit]
    }

def tool_get_whale_portfolio(args: dict) -> dict:
    """Look up any verified whale account by username to inspect verified positions, cost basis, profit, and cash balance."""
    target_username = (args.get("username") or "").strip().lstrip("@").lower()
    if not target_username:
        return {"error": "Username argument is required (e.g. 'thealexperez' or 'SirJackALot')"}

    min_pos_val = float(args.get("min_position_value", 0))

    data = fetch_json("whales.json")
    if not data or "whales" not in data:
        return {"error": "Failed to load whales directory from edge API"}

    whales = data["whales"]
    found = None
    for w in whales:
        if w.get("username", "").lower() == target_username:
            found = w
            break

    if not found:
        # Search for partial match
        matches = [w.get("username") for w in whales if target_username in w.get("username", "").lower()][:5]
        return {
            "error": f"Whale '@{target_username}' not found in 395 verified portfolios",
            "suggested_matches": matches
        }

    positions = []
    for p in found.get("all_positions", []):
        val = p.get("value", 0)
        if val < min_pos_val:
            continue
        positions.append({
            "ticker": p.get("ticker"),
            "name": p.get("name"),
            "quantity": p.get("quantity"),
            "value": val,
            "cost_basis": p.get("cost_basis"),
            "profit": p.get("profit"),
            "percent_of_portfolio": round((val / max(1, found.get("total_value", 1))) * 100, 2)
        })

    positions.sort(key=lambda x: x["value"], reverse=True)

    return {
        "username": found.get("username"),
        "total_value": found.get("total_value"),
        "cash_balance": found.get("cash_balance", 0),
        "cost_basis": found.get("cost_basis", 0),
        "profit_total": found.get("profit", 0),
        "profit_percent": found.get("profit_percent", 0),
        "profit_today": found.get("profit_today", 0),
        "followers": found.get("followers", 0),
        "following": found.get("following", 0),
        "total_likes": found.get("total_likes", 0),
        "shadow_ratio": found.get("shadow_ratio", 0),
        "verified_as_of": found.get("verified_as_of"),
        "position_count": len(positions),
        "positions": positions
    }

def tool_get_ticker_intel(args: dict) -> dict:
    """Forensic intelligence on any ticker with verified holders, conviction, and 90-day daily OHLCV bars."""
    ticker = (args.get("ticker") or "").strip().upper()
    if not ticker:
        return {"error": "Ticker symbol is required (e.g. 'NVDA', 'ASTS', 'AAPL')"}

    include_bars = bool(args.get("include_bars", False))

    data = fetch_json(f"ticker/{ticker}.json")
    if not data:
        # Try fetching from stonks.json
        stonks_data = fetch_json("stonks.json") or {}
        sec = next((s for s in stonks_data.get("securities", []) if s.get("ticker") == ticker), None)
        if not sec:
            return {"error": f"Ticker '{ticker}' not found in tracked 500 securities"}
        return {
            "ticker": ticker,
            "security": sec,
            "whales": [],
            "note": "Granular ticker file currently synchronizing"
        }

    sec = data.get("security", {})
    whales = data.get("whales", [])
    history = data.get("history", [])

    result = {
        "ticker": ticker,
        "name": sec.get("name"),
        "price": sec.get("price"),
        "changePercent": sec.get("changePercent"),
        "isETF": sec.get("isETF"),
        "totalValueOnApp": sec.get("totalValue"),
        "whaleCapitalBacking": sec.get("whalesValue"),
        "verifiedOwnersCount": sec.get("owners"),
        "convictionIntensityPerHolder": round(sec.get("intensity", 0), 2),
        "chatroomMembers": sec.get("chatroomMembers"),
        "whaleHoldersCount": len(whales),
        "topWhaleHolders": whales[:15]
    }

    if include_bars:
        result["dailyBarsCount"] = len(history)
        result["dailyBars"] = history
    else:
        result["dailyBarsCount"] = len(history)
        result["barsNote"] = "Set 'include_bars': true to receive full 90-day OHLCV candlestick series."

    return result

def tool_get_conviction_screener(args: dict) -> dict:
    """Scan for asymmetric high conviction where average position per holder exceeds a given threshold."""
    min_intensity = float(args.get("min_intensity", 50000))
    min_owners = int(args.get("min_owners", 15))
    limit = int(args.get("limit", 20))

    data = fetch_json("stonks.json")
    if not data or "securities" not in data:
        return {"error": "Failed to load securities from edge API"}

    results = []
    for s in data["securities"]:
        intensity = s.get("intensity", 0)
        owners = s.get("owners", 0)
        if intensity >= min_intensity and owners >= min_owners:
            results.append({
                "ticker": s.get("ticker"),
                "name": s.get("name"),
                "convictionPerHolder": round(intensity, 2),
                "owners": owners,
                "whaleCapital": s.get("whalesValue"),
                "totalValue": s.get("totalValue"),
                "price": s.get("price"),
                "changePercent": s.get("changePercent"),
                "isETF": s.get("isETF")
            })

    results.sort(key=lambda x: x["convictionPerHolder"], reverse=True)

    return {
        "filter": {
            "min_intensity": min_intensity,
            "min_owners": min_owners
        },
        "total_matched": len(results),
        "limit": limit,
        "results": results[:limit]
    }

def tool_screen_whales(args: dict) -> dict:
    """Filter and rank all 424 verified whales by net worth, cash reserves, profit %, or social clout."""
    min_net_worth = float(args.get("min_net_worth", 0))
    min_cash = float(args.get("min_cash", 0))
    min_profit = float(args.get("min_profit", 0))
    min_profit_pct = float(args.get("min_profit_pct", 0))
    min_followers = int(args.get("min_followers", 0))
    max_followers = int(args.get("max_followers")) if args.get("max_followers") is not None else None
    sort_by = args.get("sort_by", "net_worth").lower()
    limit = int(args.get("limit", 20))

    data = fetch_json("whales.json")
    if not data or "whales" not in data:
        return {"error": "Failed to load whales directory from edge API"}

    whales = data["whales"]
    filtered = []
    for w in whales:
        val = float(w.get("total_value", 0) or 0)
        cash = float(w.get("cash_balance", 0) or 0)
        profit = float(w.get("profit", 0) or 0)
        profit_pct = float(w.get("profit_percent", 0) or 0)
        followers = int(w.get("followers", 0) or 0)

        if val < min_net_worth:
            continue
        if cash < min_cash:
            continue
        if profit < min_profit:
            continue
        if profit_pct < min_profit_pct:
            continue
        if followers < min_followers:
            continue
        if max_followers is not None and followers > max_followers:
            continue

        shadow_ratio = round(val / max(1, followers), 2)
        filtered.append({
            "username": w.get("username"),
            "total_value": val,
            "cash_balance": cash,
            "cost_basis": w.get("cost_basis", 0),
            "profit": profit,
            "profit_percent": profit_pct,
            "profit_today": w.get("profit_today", 0),
            "followers": followers,
            "following": w.get("following", 0),
            "shadow_ratio": shadow_ratio,
            "positions_count": w.get("positions_count", 0),
            "top_positions": w.get("top_positions", [])[:5]
        })

    if sort_by in ("cash", "cash_balance"):
        filtered.sort(key=lambda x: x["cash_balance"], reverse=True)
    elif sort_by in ("profit", "pnl"):
        filtered.sort(key=lambda x: x["profit"], reverse=True)
    elif sort_by in ("profit_percent", "pnl_pct"):
        filtered.sort(key=lambda x: x["profit_percent"], reverse=True)
    elif sort_by in ("profit_today", "today_pnl"):
        filtered.sort(key=lambda x: x["profit_today"], reverse=True)
    elif sort_by == "followers":
        filtered.sort(key=lambda x: x["followers"], reverse=True)
    elif sort_by in ("shadow_ratio", "shadow"):
        filtered.sort(key=lambda x: x["shadow_ratio"], reverse=True)
    else:  # net_worth / total_value
        filtered.sort(key=lambda x: x["total_value"], reverse=True)

    return {
        "total_matched": len(filtered),
        "limit": limit,
        "whales": filtered[:limit]
    }

def tool_get_shadow_whales(args: dict) -> dict:
    """Scan for Clout Inversions / Shadow Whales: accounts with immense capital and minimal social following."""
    min_capital = float(args.get("min_capital", 500000))
    max_followers = int(args.get("max_followers", 500))
    min_shadow_ratio = float(args.get("min_shadow_ratio", 2000))
    limit = int(args.get("limit", 20))

    data = fetch_json("shadow.json")
    if not data or "whales" not in data:
        data = fetch_json("whales.json")
        if not data or "whales" not in data:
            return {"error": "Failed to load shadow whales dataset"}

    whales = data["whales"]
    matched = []
    for w in whales:
        val = float(w.get("total_value", 0) or 0)
        followers = int(w.get("followers", 0) or 0)
        ratio = float(w.get("shadow_ratio", round(val / max(1, followers), 2)) or 0)

        if val >= min_capital and followers <= max_followers and ratio >= min_shadow_ratio:
            matched.append({
                "username": w.get("username"),
                "total_value": val,
                "cash_balance": w.get("cash_balance", 0),
                "followers": followers,
                "shadow_ratio": ratio,
                "profit": w.get("profit", 0),
                "profit_percent": w.get("profit_percent", 0),
                "top_positions": w.get("top_positions", [])[:3]
            })

    matched.sort(key=lambda x: x["shadow_ratio"], reverse=True)
    return {
        "total_matched": len(matched),
        "limit": limit,
        "whales": matched[:limit]
    }

def tool_get_price_history(args: dict) -> dict:
    """Retrieve 60-day daily OHLCV candlestick price bars and returns for core market benchmarks and equities."""
    ticker = (args.get("ticker") or "").strip().upper()
    if not ticker:
        return {"error": "Ticker symbol is required (e.g. 'NVDA', 'TSLA', 'SPY')"}
    limit = int(args.get("limit", 60))

    # 1. Try granular ticker file
    data = fetch_json(f"ticker/{ticker}.json")
    bars = []
    if data and "history" in data:
        bars = data.get("history", [])

    # 2. Try historic_prices_sample.json locally
    if not bars:
        hist_sample = LOCAL_API_DIR.parent / "data" / "leaderboard" / "historic_prices_sample.json"
        if hist_sample.exists():
            try:
                with open(hist_sample, encoding="utf-8") as f:
                    hdata = json.load(f)
                    bars = hdata.get("history", {}).get(ticker, {}).get("bars", [])
            except Exception:
                pass

    if not bars:
        return {
            "error": f"Daily OHLCV bars not found for '{ticker}'. Available core tickers: AAPL, ASTS, NVDA, SPY, TSLA, MSTR, AMZN, MSFT, QQQ, PLTR, AMD, META, GOOGL, HOOD, COIN, SOFI, VOO, IBIT."
        }

    # Calculate summary metrics
    closes = [b.get("close") for b in bars if b.get("close") is not None]
    highs = [b.get("high") for b in bars if b.get("high") is not None]
    lows = [b.get("low") for b in bars if b.get("low") is not None]
    volumes = [b.get("volume") for b in bars if b.get("volume") is not None]

    latest_close = closes[-1] if closes else 0
    first_close = closes[0] if closes else 0
    pct_return = round(((latest_close - first_close) / first_close) * 100, 2) if first_close else 0

    return {
        "ticker": ticker,
        "timeframe": "1D",
        "total_bars_available": len(bars),
        "bars_returned": min(limit, len(bars)),
        "summary": {
            "latest_close": latest_close,
            "high_period": max(highs) if highs else 0,
            "low_period": min(lows) if lows else 0,
            "period_return_percent": pct_return,
            "average_volume": int(sum(volumes) / len(volumes)) if volumes else 0
        },
        "bars": bars[-limit:]
    }

def tool_get_funnel_accounts(args: dict) -> dict:
    """AfterHour accounts flagged for funneling traders into Telegram channels (data: telegramscammers.com)."""
    data = fetch_json("funnel.json")
    if not data:
        return {"error": "funnel.json currently synchronizing"}
    user = str(args.get("username") or "").strip().lstrip("@").lower()
    tier = str(args.get("tier") or "").strip().lower()
    link = str(args.get("telegram_link") or "").strip().lower().replace("https://", "").replace("http://", "")
    try:
        limit = max(1, min(int(args.get("limit", 25)), 100))
    except (TypeError, ValueError):
        limit = 25
    rows = data.get("accounts", [])
    if user:
        rows = [r for r in rows if user in r["username"].lower()]
    if tier:
        rows = [r for r in rows if r["tier"] == tier]
    if link:
        rows = [r for r in rows if r.get("telegram_link") and link.lstrip("/") in r["telegram_link"]]
    return {
        "source": data.get("credit"), "database": data.get("database"), "disclaimer": data.get("disclaimer"),
        "total_flagged": data.get("count"), "matched": len(rows), "accounts": rows[:limit],
        "shared_link_clusters": data.get("shared_link_clusters") if not (user or tier or link) else None,
    }

FUNNEL_CREDIT = "https://telegramscammers.com"
FUNNEL_DISCLAIMER = ("Flagged for investigation, not a finding of fraud. "
                     "Quoted results are the channel's own claims; small sample, not statistically meaningful.")


def tool_get_funnel_callouts(args: dict) -> dict:
    """Parsed trade callouts from public Telegram channels linked to flagged accounts (data: telegramscammers.com)."""
    data = fetch_json("funnel-calls.json")
    if not data:
        return {"error": "funnel-calls.json currently synchronizing"}
    ticker = str(args.get("ticker") or "").strip().lstrip("$").upper()
    channel = str(args.get("channel") or "").strip().lower().replace("https://", "").replace("http://", "").lstrip("@/")
    action = str(args.get("action") or "").strip().lower()
    try:
        limit = max(1, min(int(args.get("limit", 25)), 100))
    except (TypeError, ValueError):
        limit = 25
    rows = data.get("calls", [])
    if ticker:
        rows = [r for r in rows if (r.get("ticker") or "").upper() == ticker]
    if channel:
        rows = [r for r in rows if channel in (r.get("channel") or "").lower()]
    if action:
        rows = [r for r in rows if r.get("action") == action]
    counts: dict = {}
    for r in rows:
        counts[r.get("ticker")] = counts.get(r.get("ticker"), 0) + 1
    return {
        "source": data.get("credit") or FUNNEL_CREDIT, "disclaimer": data.get("disclaimer") or FUNNEL_DISCLAIMER,
        "quoted_results_are_channel_claims": data.get("quoted_results_are_channel_claims"),
        "small_sample_warning": data.get("small_sample_warning"),
        "total_parsed": data.get("total_parsed"), "matched": len(rows),
        "ticker_counts": dict(sorted(counts.items(), key=lambda kv: -kv[1])),
        "callouts": rows[:limit],
    }


def tool_get_funnel_tickers(args: dict) -> dict:
    """Tickers most called out by flagged AfterHour accounts and their Telegram channels (data: telegramscammers.com)."""
    data = fetch_json("funnel-tickers.json")
    if not data:
        return {"error": "funnel-tickers.json currently synchronizing"}
    try:
        limit = max(1, min(int(args.get("limit", 25)), 100))
    except (TypeError, ValueError):
        limit = 25
    rows = data.get("tickers", [])
    return {
        "source": data.get("credit") or FUNNEL_CREDIT, "disclaimer": data.get("disclaimer") or FUNNEL_DISCLAIMER,
        "total_tickers": len(rows), "tickers": rows[:limit],
    }


def tool_get_funnel_scorecard(args: dict) -> dict:
    """Public scoring of trade callouts from public Telegram channels: how option contracts traded after the call ('paths', the main view), options held to expiry, and forex/gold/index signals (TP1 first vs SL first)."""
    args = args if isinstance(args, dict) else {}
    section = str(args.get("section") or "all").strip().lower()
    if section not in ("paths", "options", "fx", "all"):
        section = "all"
    channel = str(args.get("channel") or "").strip().lower().replace("https://", "").replace("http://", "").lstrip("@/")
    data = fetch_json("funnel-scorecard.json") if section != "paths" else None
    paths = fetch_json("funnel-option-paths.json") if section in ("paths", "all") else None
    if section == "paths" and not isinstance(paths, dict):
        return {"error": "funnel-option-paths.json currently synchronizing"}
    if section != "paths" and not isinstance(data, dict):
        return {"error": "funnel-scorecard.json currently synchronizing"}
    base = paths if section == "paths" else data

    def keep(rows):
        rows = rows if isinstance(rows, list) else []
        if not channel:
            return rows
        return [r for r in rows if isinstance(r, dict) and channel in (r.get("channel") or "").lower()]

    out = {
        "source": base.get("credit") or FUNNEL_CREDIT, "disclaimer": base.get("disclaimer") or FUNNEL_DISCLAIMER,
        "generated_at": base.get("generated_at"), "conventions": data.get("conventions") if data else None,
        "methodology": (data or {}).get("methodology") or "https://ah.mphinance.com/scorecard",
        "methodology_doc": (data or {}).get("methodology_doc"),
        "section": section, "channel_filter": channel or None,
    }
    if section in ("paths", "all"):
        if isinstance(paths, dict):
            pp = {k: v for k, v in paths.items() if k not in ("credit", "disclaimer", "generated_at")}
            if channel:
                pp["by_channel"] = keep(pp.get("by_channel"))
            out["paths"] = pp
        else:
            out["paths"] = {"error": "funnel-option-paths.json currently synchronizing"}
    if section in ("options", "all"):
        o = dict(data.get("options") or {})
        if channel:
            o["by_channel"] = keep(o.get("by_channel"))
        out["options"] = o
    if section in ("fx", "all"):
        f = dict(data.get("fx") or {})
        if channel:
            f["by_channel"] = keep(f.get("by_channel"))
            f["weekly_by_channel"] = keep(f.get("weekly_by_channel"))
            f["content_timeline"] = keep(f.get("content_timeline"))
            tv = dict(f.get("touch_variant") or {})
            tv["by_channel"] = keep(tv.get("by_channel"))
            f["touch_variant"] = tv
        out["fx"] = f
    return out


def tool_get_social_feed(args: dict) -> dict:
    """Retrieve live community posts, commentary, and broker-verified trade snapshots from AfterHour."""
    target_ticker = (args.get("ticker") or "").strip().upper()
    target_username = (args.get("username") or "").strip().lstrip("@").lower()
    limit = int(args.get("limit", 20))

    # 1. Try feed.json
    data = fetch_json("feed.json")
    posts = []
    if data and "posts" in data:
        posts = data["posts"]

    # 2. Try loading from local archive if feed.json not yet written
    if not posts:
        feed_dir = LOCAL_API_DIR.parent / "data" / "archive_latest" / "social_feed"
        if not feed_dir.exists():
            archives = list(LOCAL_API_DIR.parent.glob("data/archive_*/social_feed"))
            if archives:
                feed_dir = archives[-1]

        if feed_dir and feed_dir.exists():
            for fn in sorted(feed_dir.glob("*.json")):
                try:
                    with open(fn, encoding="utf-8") as f:
                        fd = json.load(f)
                        for item in fd.get("items", []):
                            post = item.get("post") or {}
                            author = item.get("author") or {}
                            snap = item.get("portfolioSnapshot") or {}
                            secs = [s.get("tickerSymbol") for s in item.get("securities", []) if s.get("tickerSymbol")]
                            posts.append({
                                "id": post.get("id") or item.get("id"),
                                "author": author.get("username"),
                                "author_followers": author.get("numFollowers", 0),
                                "created_at": post.get("createdAt") or item.get("createdAt"),
                                "title": post.get("title", ""),
                                "share_url": post.get("shareUrl", ""),
                                "securities": secs,
                                "view_count": item.get("viewCount", 0),
                                "comment_count": item.get("commentCount", 0),
                                "verified_snapshot": {
                                    "total_value": snap.get("totalValue", 0),
                                    "cash_balance": snap.get("cashBalance", 0),
                                    "positions_count": len(snap.get("positionSnapshots", [])),
                                    "verified_as_of": snap.get("verifiedAsOf")
                                } if snap.get("totalValue") else None
                            })
                except Exception:
                    pass

    # Filter
    filtered = []
    for p in posts:
        if target_ticker and target_ticker not in [s.upper() for s in p.get("securities", [])]:
            continue
        if target_username and (p.get("author") or "").lower() != target_username:
            continue
        filtered.append(p)

    return {
        "total_matched": len(filtered),
        "limit": limit,
        "posts": filtered[:limit]
    }

# ==============================================================================
# LIVE TOOLS (direct, unauthenticated GETs against the public AfterHour API)
# ==============================================================================
# Freshness is the value here, so every result is wrapped as
# {"source": "live"|"cache"|"stale", "as_of": iso, "data": ...}. Upstream 504s
# (~1 in 7) are retried with backoff; if all retries fail we serve a stale copy
# (source "stale") or a retryable error object, never a raw gateway error.

import re
import datetime as _dt

AH_API = "https://api.afterhour.com"
_AH_CACHE = {}
_AH_LOCK = threading.Lock()
_AH_SLOTS = threading.BoundedSemaphore(3)  # max 3 concurrent upstream calls
_AH_STALE_MAX = 3600.0

_SYM_RE = re.compile(r"^[A-Za-z0-9.\-^=]{1,12}$")
_USER_RE = re.compile(r"^[A-Za-z0-9_.\-]{1,40}$")
_HASH_RE = re.compile(r"^[A-Za-z0-9]{3,12}$")


class UpstreamError(Exception):
    pass


def _iso(ts: float) -> str:
    return _dt.datetime.fromtimestamp(ts, _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ah_get(path: str, params: dict = None, ttl: float = 60.0, retries: int = 3):
    """GET api.afterhour.com. Returns (data, source, as_of_ts). Raises UpstreamError."""
    qs = urllib.parse.urlencode({k: v for k, v in (params or {}).items() if v is not None})
    url = f"{AH_API}{path}" + (f"?{qs}" if qs else "")
    now = time.time()
    with _AH_LOCK:
        hit = _AH_CACHE.get(url)
    if hit and now - hit[1] < ttl:
        return hit[0], "cache", hit[1]

    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": f"AfterMath-MCP/{VERSION} (+https://ah.mphinance.com/mcp)",
                "Accept": "application/json",
            })
            with _AH_SLOTS:
                with urllib.request.urlopen(req, timeout=20.0) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            ts = time.time()
            with _AH_LOCK:
                _AH_CACHE[url] = (data, ts)
                if len(_AH_CACHE) > 400:  # crude bound
                    for k in sorted(_AH_CACHE, key=lambda k: _AH_CACHE[k][1])[:100]:
                        _AH_CACHE.pop(k, None)
            return data, "live", ts
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (400, 401, 403, 404):  # not retryable
                break
        except Exception as e:  # timeouts, resets, bad JSON
            last = str(e)[:120]
        time.sleep(1.0 * (2 ** attempt))

    if hit and now - hit[1] < _AH_STALE_MAX:
        return hit[0], "stale", hit[1]
    raise UpstreamError(last or "upstream unavailable")


def _live(path, params=None, ttl=60.0, shape=None):
    """Run ah_get and wrap in the standard freshness envelope."""
    try:
        data, source, ts = ah_get(path, params, ttl)
    except UpstreamError as e:
        return {"error": f"AfterHour upstream unavailable ({e})", "retryable": True}
    return {"source": source, "as_of": _iso(ts), "data": shape(data) if shape else data}


def _bad(msg):
    return {"error": msg, "retryable": False}


def _pick(d, keys):
    return {k: d.get(k) for k in keys if d.get(k) is not None}


def _price_view(p):
    """Trim a SecurityPrice to the fields agents need. Percent fields are percent units."""
    if not p:
        return None
    s = p.get("session") or {}
    return {
        "price": p.get("price"),
        "as_of": p.get("asOf"),
        "change_pct": s.get("changePercent"),
        "premarket_change_pct": s.get("earlyTradingChangePercent"),
        "afterhours_change_pct": s.get("lateTradingChangePercent"),
        "open": s.get("open"), "high": s.get("high"), "low": s.get("low"),
        "previous_close": s.get("previousClose"), "volume": s.get("volume"),
    }


def _overview_view(o):
    sec = o.get("security") or {}
    chat = sec.get("chatroom") or {}
    return {
        "ticker": sec.get("tickerSymbol"),
        "name": sec.get("friendlyName") or sec.get("name"),
        "type": sec.get("type"),
        "price": _price_view(o.get("price")),
        "owner_count": o.get("ownerCount"),
        "total_value_held": o.get("totalValue"),
        "market_cap": o.get("marketCap"),
        "chatroom_members": chat.get("memberCount"),
        "chatroom_online": chat.get("onlineCount"),
        "sample_owners": [
            _pick(p, ["username", "numFollowers", "financialDataPrivacyMode"])
            for p in (o.get("ownersSample") or [])[:5]
        ],
    }


def tool_get_market_session(args: dict) -> dict:
    date = (args.get("date") or "").strip()
    if not date:
        try:
            from zoneinfo import ZoneInfo
            date = _dt.datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d")
        except Exception:
            date = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return _bad("date must be YYYY-MM-DD")

    def shape(h):
        now = _dt.datetime.now(_dt.timezone.utc)

        def parse(s):
            return _dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=_dt.timezone.utc)

        phase, edges = "closed", []
        for name in ("overnight", "preMarket", "regular", "afterHours"):
            w = h.get(name)
            if not w:
                continue
            a, b = parse(w["start"]), parse(w["end"])
            edges += [(a, f"{name}_open"), (b, f"{name}_close")]
            if a <= now <= b:
                phase = {"preMarket": "pre", "regular": "regular", "afterHours": "after", "overnight": "overnight"}[name]
        nxt = min((e for e in edges if e[0] > now), default=None, key=lambda e: e[0])
        return {
            "date": date, "status": h.get("status"), "phase_now": phase,
            "early_close": h.get("status") == "early-close",
            "next_transition": nxt[1] if nxt else None,
            "next_transition_at": nxt[0].strftime("%Y-%m-%dT%H:%M:%SZ") if nxt else None,
            "seconds_to_next": int((nxt[0] - now).total_seconds()) if nxt else None,
            "windows": {k: h.get(k) for k in ("preMarket", "regular", "afterHours", "overnight") if h.get(k)},
        }

    return _live(f"/stonks/market/hours/{date}", ttl=60.0, shape=shape)


def tool_get_live_quotes(args: dict) -> dict:
    syms = args.get("symbols") or []
    if isinstance(syms, str):
        syms = [s for s in re.split(r"[,\s]+", syms) if s]
    syms = [s.strip().upper() for s in syms][:25]
    if not syms:
        return _bad("symbols is required, e.g. ['NVDA','SPY'] (max 25)")
    if not all(_SYM_RE.match(s) for s in syms):
        return _bad("symbols must be plain ticker symbols")

    def shape(d):
        rows = {p["symbol"]: _price_view(p) for p in (d.get("prices") or []) if p}
        return {"quotes": {s: rows.get(s) for s in syms},
                "unknown": [s for s in syms if s not in rows]}

    return _live("/stonks/tickers/prices", {"symbols": ",".join(syms)}, ttl=30.0, shape=shape)


_LB_SORTS = ("TRENDING", "WATCHERS", "OWNERS", "GAINERS", "LOSERS")
_LB_RANGES = ("DAY", "WEEK", "MONTH", "THREE_MONTH", "YEAR_TO_DATE")


def tool_get_leaderboard(args: dict) -> dict:
    sort = (args.get("sort") or "TRENDING").upper()
    rng = (args.get("time_range") or "DAY").upper()
    if sort not in _LB_SORTS:
        return _bad(f"sort must be one of {list(_LB_SORTS)}")
    if rng not in _LB_RANGES:
        return _bad(f"time_range must be one of {list(_LB_RANGES)}")
    take = max(1, min(int(args.get("take", 20)), 50))
    cursor = max(0, int(args.get("cursor", 0)))
    note = None
    if sort == "GAINERS" and rng != "DAY":
        rng, note = "DAY", "GAINERS only works with DAY upstream (504 otherwise); used DAY"
    if sort == "LOSERS" and rng in ("THREE_MONTH", "YEAR_TO_DATE"):
        rng, note = "DAY", "LOSERS is empty for that range upstream; used DAY"

    def shape(d):
        rows = []
        for i, e in enumerate(d.get("securities") or []):
            v = _overview_view(e.get("security") or e)
            v["rank"] = cursor + i + 1
            for k in ("followCount", "changePricePercentage"):
                if e.get(k) is not None:
                    v[{"followCount": "watchers", "changePricePercentage": "range_change_pct"}[k]] = e[k]
            rows.append(v)
        out = {"sort": sort, "time_range": rng, "total_universe": d.get("totalCount"),
               "next_cursor": d.get("cursor"), "results": rows}
        if note:
            out["note"] = note
        return out

    return _live("/stonks/security/leaderboard", {"sortOrder": sort, "timeRange": rng, "take": take, "cursor": cursor},
                 ttl=120.0, shape=shape)


def tool_get_ticker_live(args: dict) -> dict:
    sym = (args.get("symbol") or "").strip().upper()
    if not _SYM_RE.match(sym):
        return _bad("symbol is required, e.g. 'NVDA'")
    return _live(f"/stonks/security/ticker/{urllib.parse.quote(sym)}", ttl=120.0, shape=_overview_view)


def tool_get_profile_live(args: dict) -> dict:
    u = (args.get("username") or "").strip().lstrip("@")
    if not _USER_RE.match(u):
        return _bad("username is required")

    def shape(p):
        return {
            **_pick(p, ["username", "bio", "createdAt", "numFollowers", "numFollowing", "numTotalLikes",
                        "hasConnectedItems", "financialDataPrivacyMode", "appReleaseChannel", "badgeKeys",
                        "linkInBio", "socialHandleX", "socialHandleDiscord", "socialHandleReddit"]),
            "profile_number": p.get("profileNumber"),
        }

    return _live("/public/profile", {"username": u}, ttl=300.0, shape=shape)


def tool_get_post_permalink(args: dict) -> dict:
    raw = (args.get("hash") or args.get("url") or "").strip()
    h = raw
    if "afterhour.com" in raw:  # https://afterhour.com/<user>/<hash>/<slug>
        parts = [p for p in urllib.parse.urlparse(raw).path.split("/") if p]
        h = parts[1] if len(parts) >= 2 else ""
    if not _HASH_RE.match(h):
        return _bad("pass the post hash (e.g. 'bx5Y') or its afterhour.com share URL")
    ct = max(0, min(int(args.get("comments", 5)), 10))

    def shape(p):
        post = p.get("post") or p
        author = post.get("author") or p.get("author") or {}
        snaps = []
        for s in (post.get("positionSnapshots") or p.get("positionSnapshots") or [])[:15]:
            snaps.append(_pick(s, ["tickerSymbol", "type", "quantity", "value", "profitPercent",
                                   "optionsContractType", "optionsStrikePrice", "optionsExpirationDate"]))
        comments = []
        for c in (p.get("comments") or post.get("comments") or [])[:ct]:
            comments.append({"author": (c.get("author") or {}).get("username"), "body": (c.get("body") or "")[:500],
                             "created_at": c.get("createdAt")})
        return {
            **_pick(post, ["id", "title", "createdAt", "shareUrl", "viewCount"]),
            "comment_count": post.get("commentCount"), "reaction_counts": post.get("reactionCounts"),
            "author": _pick(author, ["username", "numFollowers"]),
            "position_snapshots": snaps, "comments": comments,
        }

    return _live(f"/public/post/{h}", {"commentsTake": ct}, ttl=600.0, shape=shape)


def tool_get_security_chart(args: dict) -> dict:
    sym = (args.get("symbol") or "").strip().upper()
    if not _SYM_RE.match(sym):
        return _bad("symbol is required, e.g. 'NVDA'")
    timespan = (args.get("timespan") or "day").lower()
    if timespan not in ("minute", "hour", "day", "week", "month"):
        return _bad("timespan must be minute|hour|day|week|month")
    mult = max(1, min(int(args.get("multiplier", 1)), 60))
    days = max(1, min(int(args.get("days", 30)), 365))
    try:
        ov, _, _ = ah_get(f"/stonks/security/ticker/{urllib.parse.quote(sym)}", ttl=3600.0)
        sid = (ov.get("security") or {}).get("id")
    except UpstreamError as e:
        return {"error": f"AfterHour upstream unavailable ({e})", "retryable": True}
    if not sid:
        return _bad(f"ticker '{sym}' not found")
    end = _dt.datetime.now(_dt.timezone.utc)
    start = end - _dt.timedelta(days=days)
    fmt = "%Y-%m-%dT%H:%M:%SZ"

    def shape(d):
        bars = [{"t": b.get("timestamp"), "o": b.get("open"), "h": b.get("high"), "l": b.get("low"),
                 "c": b.get("close"), "v": b.get("volume"), "vwap": b.get("volumeWeightedAveragePrice")}
                for b in (d.get("prices") or [])]
        return {"symbol": sym, "timespan": timespan, "multiplier": mult, "bar_count": len(bars),
                "previous_close": d.get("previousClose"), "bars": bars[-500:]}

    return _live(f"/stonks/security/{sid}/historic_prices",
                 {"multiplier": mult, "timespan": timespan, "start": start.strftime(fmt), "end": end.strftime(fmt)},
                 ttl=300.0, shape=shape)


def tool_get_app_status(args: dict) -> dict:
    return _live("/app-info", {"appId": "com.afterhour", "version": "4.6.4", "platform": "android", "buildNumber": 88},
                 ttl=300.0)


def tool_compare_tickers(args: dict) -> dict:
    syms = args.get("symbols") or []
    if isinstance(syms, str):
        syms = [s for s in re.split(r"[,\s]+", syms) if s]
    syms = [s.strip().upper() for s in syms][:5]
    if len(syms) < 2:
        return _bad("pass 2 to 5 symbols")
    stonks = {s.get("ticker"): s for s in (fetch_json("stonks.json") or {}).get("securities", [])}
    rows, missing = [], []
    for sym in syms:
        s = stonks.get(sym)
        if not s:
            missing.append(sym)
            continue
        ret30 = None
        t = fetch_json(f"ticker/{sym}.json") or {}
        h = t.get("history") or []
        if len(h) >= 2 and h[0].get("close") and h[-1].get("close"):
            win = h[-31:]
            ret30 = round((win[-1]["close"] / win[0]["close"] - 1) * 100, 2)
        rows.append({
            "ticker": sym, "name": s.get("name"), "price": s.get("price"), "change_pct_24h": s.get("changePercent"),
            "return_pct_30d": ret30, "whale_capital": s.get("whalesValue"), "whale_holders": s.get("whalesCount"),
            "verified_owners": s.get("owners"), "platform_value": s.get("totalValue"),
            "conviction_per_holder": round(s.get("intensity", 0), 2),
            "top_whale": s.get("topWhale"), "is_etf": s.get("isETF"),
        })
    return {"source": "snapshot", "universe": "verified 500", "compared": rows,
            "not_tracked": missing or None,
            "note": "Snapshot of the verified 500 (rebuilt on deploy). For tickers outside it use get_ticker_live."}


LIVE_TOOLS_MAP = {
    "get_market_session": tool_get_market_session,
    "get_live_quotes": tool_get_live_quotes,
    "get_leaderboard": tool_get_leaderboard,
    "get_ticker_live": tool_get_ticker_live,
    "get_profile_live": tool_get_profile_live,
    "get_post_permalink": tool_get_post_permalink,
    "get_security_chart": tool_get_security_chart,
    "get_app_status": tool_get_app_status,
    "compare_tickers": tool_compare_tickers,
}

LIVE_TOOL_DEFINITIONS = [
    {
        "name": "get_market_session",
        "description": "LIVE (60s cache). Use for 'is the market open / what session is it / when does it close'. Returns current phase (pre, regular, after, overnight, closed), early-close flag, next transition and seconds until it, computed server-side in UTC.",
        "inputSchema": {"type": "object", "properties": {
            "date": {"type": "string", "description": "YYYY-MM-DD (default: today, US Eastern)"}},
            "additionalProperties": False},
    },
    {
        "name": "get_live_quotes",
        "description": "LIVE (30s cache). Use for current price. Up to 25 symbols: last price, session change, pre-market and after-hours change, OHLC, volume. Percent fields are percent units (1.1 = 1.1%). Do NOT use for whale or conviction data (use get_ticker_intel).",
        "inputSchema": {"type": "object", "properties": {
            "symbols": {"type": "array", "items": {"type": "string"}, "description": "Ticker symbols, max 25"}},
            "required": ["symbols"], "additionalProperties": False},
    },
    {
        "name": "get_leaderboard",
        "description": "LIVE (2 min cache). Use for 'what is trending / most watched / top gainers / top losers' across the whole platform (~33k securities, crowd-ranked). Do NOT use for whale-capital ranking of the verified 500 (use get_top_equities). GAINERS only supports DAY. Percent fields are percent units.",
        "inputSchema": {"type": "object", "properties": {
            "sort": {"type": "string", "enum": list(_LB_SORTS), "default": "TRENDING"},
            "time_range": {"type": "string", "enum": list(_LB_RANGES), "default": "DAY"},
            "take": {"type": "integer", "description": "Max 50", "default": 20},
            "cursor": {"type": "integer", "description": "Offset from a previous next_cursor", "default": 0}},
            "additionalProperties": False},
    },
    {
        "name": "get_ticker_live",
        "description": "LIVE (2 min cache). Any ticker on the platform: price, owner count, total value held, market cap, chatroom activity, sample owners. Use when get_ticker_intel says the ticker is not in the verified 500. No whale breakdown or OHLCV.",
        "inputSchema": {"type": "object", "properties": {
            "symbol": {"type": "string", "description": "e.g. 'NVDA'"}},
            "required": ["symbol"], "additionalProperties": False},
    },
    {
        "name": "get_profile_live",
        "description": "LIVE (5 min cache). Public profile for any AfterHour handle, including non-whales: bio, followers, join date, whether a brokerage is linked, privacy mode. No portfolio data (use get_whale_portfolio for the 395 verified).",
        "inputSchema": {"type": "object", "properties": {
            "username": {"type": "string", "description": "AfterHour username, with or without @"}},
            "required": ["username"], "additionalProperties": False},
    },
    {
        "name": "get_post_permalink",
        "description": "LIVE (10 min cache). Use when you already have a post link or hash: returns the body, author, attached position snapshots and the first comments. Do NOT use to browse (use get_social_feed).",
        "inputSchema": {"type": "object", "properties": {
            "hash": {"type": "string", "description": "Post hash (e.g. 'bx5Y') or full afterhour.com share URL"},
            "comments": {"type": "integer", "description": "Comments to include, max 10", "default": 5}},
            "required": ["hash"], "additionalProperties": False},
    },
    {
        "name": "get_security_chart",
        "description": "LIVE (5 min cache). OHLCV bars for any platform ticker at minute, hour, day, week or month resolution, up to 365 days back, last 500 bars. Superset of get_price_history, which is limited to 18 tickers of daily bars.",
        "inputSchema": {"type": "object", "properties": {
            "symbol": {"type": "string"},
            "timespan": {"type": "string", "enum": ["minute", "hour", "day", "week", "month"], "default": "day"},
            "multiplier": {"type": "integer", "description": "Bar size multiplier, max 60", "default": 1},
            "days": {"type": "integer", "description": "Lookback in days, max 365", "default": 30}},
            "required": ["symbol"], "additionalProperties": False},
    },
    {
        "name": "get_app_status",
        "description": "LIVE (5 min cache). AfterHour app remote config: feature flags and forced/recommended-update gate for the tracked Android build. Use to detect that the app shipped a change.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "compare_tickers",
        "description": "SNAPSHOT (verified 500, rebuilt on deploy). Side-by-side table for 2 to 5 tickers: price, 24h and 30d move, whale capital and holders, verified owners, conviction per holder. For tickers outside the 500 use get_ticker_live.",
        "inputSchema": {"type": "object", "properties": {
            "symbols": {"type": "array", "items": {"type": "string"}, "description": "2 to 5 tickers"}},
            "required": ["symbols"], "additionalProperties": False},
    },
]



# ==============================================================================
# RETAIL SENTIMENT TOOLS (read api/sentiment.json built by ah_collect.py)
# ==============================================================================

_SENT_WINDOWS = ("24h", "72h", "7d")
_SENT_NOTE = ("Deterministic and conservative: direction only from explicit contract side (CALL/PUT, 765C) plus an "
              "open verb; closes, hindsight and modal language are neutral. One vote per author per ticker per day; "
              "identical titles count once. About a quarter of public posts carry parseable direction. Not advice.")


def _sent_load(window):
    window = (window or "24h").lower()
    if window not in _SENT_WINDOWS:
        return None, None, _bad(f"window must be one of {list(_SENT_WINDOWS)}")
    d = fetch_json("sentiment.json")
    if not d:
        return None, None, {"error": "sentiment data not yet published", "retryable": True}
    return d, window, None


def _sent_env(d, window, body):
    gen = d.get("generated_at")
    age = None
    try:
        age = int(time.time() - _dt.datetime.strptime(gen, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc).timestamp())
    except Exception:
        pass
    return {"as_of": gen, "age_s": age, "stale": (age is not None and age > 1800), "window": window,
            "archive": d.get("archive"), "method": _SENT_NOTE, **body}


def tool_get_retail_sentiment(args: dict) -> dict:
    d, window, err = _sent_load(args.get("window"))
    if err:
        return err
    tk = (args.get("ticker") or "").strip().upper().lstrip("$")
    if not tk:
        return _bad("ticker is required")
    row = d["windows"][window].get(tk)
    if not row:
        return _sent_env(d, window, {"ticker": tk, "n_posts": 0, "note": "No public posts mention this ticker in the window."})
    return _sent_env(d, window, {"ticker": tk, **row})


def tool_get_retail_options_bias(args: dict) -> dict:
    d, window, err = _sent_load(args.get("window"))
    if err:
        return err
    tk = (args.get("ticker") or "").strip().upper().lstrip("$")
    rows = d["windows"][window]
    if tk:
        r = rows.get(tk) or {}
        return _sent_env(d, window, {"ticker": tk, "calls_opened": r.get("calls_opened", 0),
                                     "puts_opened": r.get("puts_opened", 0), "call_put_ratio": r.get("call_put_ratio")})
    lim = max(1, min(int(args.get("limit", 15)), 50))
    lst = [{"ticker": t, "calls_opened": r["calls_opened"], "puts_opened": r["puts_opened"],
            "call_put_ratio": r["call_put_ratio"], "n_voting_authors": r["n_voting_authors"]}
           for t, r in rows.items() if r["calls_opened"] + r["puts_opened"] > 0]
    lst.sort(key=lambda x: x["calls_opened"] + x["puts_opened"], reverse=True)
    return _sent_env(d, window, {"tickers": lst[:lim]})


def tool_get_retail_buzz(args: dict) -> dict:
    d, window, err = _sent_load(args.get("window"))
    if err:
        return err
    if window == "7d":
        return _bad("buzz supports window 24h or 72h")
    lim = max(1, min(int(args.get("limit", 20)), 50))
    b = (d.get("buzz") or {}).get(window) or {}
    rows = d["windows"][window]
    lst = []
    for t, v in (b.get("tickers") or {}).items():
        r = rows.get(t, {})
        lst.append({"ticker": t, "mentions": v["mentions"], "baseline_mean": v["baseline_mean"], "z": v["z"],
                    "n_authors": r.get("n_authors"), "net_score": r.get("net_score"), "confidence": r.get("confidence")})
    lst.sort(key=lambda x: (x["z"] if x["z"] is not None else -9e9, x["mentions"]), reverse=True)
    if all(x["z"] is None for x in lst):
        lst.sort(key=lambda x: x["mentions"], reverse=True)
    return _sent_env(d, window, {"archive_depth_days": b.get("archive_depth_days"),
                                 "z_note": "z is null until the archive holds 3+ days of posts; ranked by mentions until then.",
                                 "tickers": lst[:lim]})


def tool_get_retail_vs_whale(args: dict) -> dict:
    d, window, err = _sent_load(args.get("window") or "72h")
    if err:
        return err
    min_voters = max(1, int(args.get("min_voting_authors", 2)))
    lim = max(1, min(int(args.get("limit", 15)), 50))
    stonks = {s["ticker"]: s for s in (fetch_json("stonks.json") or {}).get("securities", [])}
    ranked = sorted((s for s in stonks.values() if s.get("whalesValue")), key=lambda s: s["whalesValue"], reverse=True)
    n = max(1, len(ranked))
    wrank = {s["ticker"]: i for i, s in enumerate(ranked)}
    out = []
    for t, r in d["windows"][window].items():
        if r["n_voting_authors"] < min_voters or r["net_score"] is None or t not in stonks:
            continue
        s = stonks[t]
        whale_pct = 1 - wrank[t] / n if t in wrank else 0.0  # 1 = most whale capital
        retail = r["net_score"]  # -1..1
        label = ("retail bullish, little whale capital" if retail > 0.3 and whale_pct < 0.5 else
                 "retail bearish, heavy whale capital" if retail < -0.3 and whale_pct > 0.7 else
                 "retail bullish, whales heavy (aligned)" if retail > 0.3 else "mixed")
        out.append({"ticker": t, "retail_net_score": retail, "retail_voting_authors": r["n_voting_authors"],
                    "confidence": r["confidence"], "whale_capital": s.get("whalesValue"),
                    "whale_holders": s.get("whalesCount"), "whale_capital_percentile": round(whale_pct, 2),
                    "label": label})
    out.sort(key=lambda x: abs(x["retail_net_score"]) * (1 - x["whale_capital_percentile"] if x["retail_net_score"] > 0 else x["whale_capital_percentile"]), reverse=True)
    return _sent_env(d, window, {
        "tickers": out[:lim],
        "caveat": "Whale capital is a size ranking from the verified 500, not a whale direction. The label compares retail stance with how much verified capital sits in the name; it is a prompt to look closer, not a signal."})


def tool_get_sentiment_flags(args: dict) -> dict:
    d, window, err = _sent_load(args.get("window"))
    if err:
        return err
    tk = (args.get("ticker") or "").strip().upper().lstrip("$")
    r = d["windows"][window].get(tk)
    if not r:
        return _sent_env(d, window, {"ticker": tk, "n_posts": 0})
    return _sent_env(d, window, {"ticker": tk, "n_posts": r["n_posts"], "n_authors": r["n_authors"], "flags": r["flags"],
                                 "note": "Authors on the funnel list are flagged for investigation, not a finding of fraud (list curated by https://telegramscammers.com). Check these before trusting a score."})


def tool_get_ticker_posts(args: dict) -> dict:
    d = fetch_json("ah-posts.json")
    if not d:
        return {"error": "post archive not yet published", "retryable": True}
    tk = (args.get("ticker") or "").strip().upper().lstrip("$")
    user = (args.get("username") or "").strip().lstrip("@").lower()
    lim = max(1, min(int(args.get("limit", 20)), 50))
    rows = [p for p in d.get("posts", []) if (not tk or tk in p["tickers"]) and (not user or (p["author"] or "").lower() == user)]
    return {"as_of": d.get("generated_at"), "matched": len(rows), "posts": [
        {k: p[k] for k in ("id", "hash", "ts", "author", "followers", "title", "topic", "tickers", "stance", "action", "views", "comments")}
        for p in rows[:lim]]}


def tool_get_sentiment_trend(args: dict) -> dict:
    d = fetch_json("sentiment.json")
    if not d:
        return {"error": "sentiment data not yet published", "retryable": True}
    tk = (args.get("ticker") or "").strip().upper().lstrip("$")
    days = max(1, min(int(args.get("days", 7)), 14))
    series = (d.get("daily") or {}).get(tk, [])[-days:]
    return _sent_env(d, f"{days}d", {"ticker": tk, "series": series,
                                     "note": "Daily post counts and net score; days with no directional votes have net null. Archive depth limits how far back this goes."})


SENTIMENT_TOOLS_MAP = {
    "get_retail_sentiment": tool_get_retail_sentiment,
    "get_retail_options_bias": tool_get_retail_options_bias,
    "get_retail_buzz": tool_get_retail_buzz,
    "get_retail_vs_whale": tool_get_retail_vs_whale,
    "get_sentiment_flags": tool_get_sentiment_flags,
    "get_ticker_posts": tool_get_ticker_posts,
    "get_sentiment_trend": tool_get_sentiment_trend,
}

_W = {"type": "string", "enum": list(_SENT_WINDOWS), "default": "24h"}
SENTIMENT_TOOL_DEFINITIONS = [
    {"name": "get_retail_sentiment",
     "description": "SNAPSHOT (refreshed every 5 min). Retail stance on one ticker from public AfterHour posts: bull/bear votes, net score (-1..1), distinct voting authors, confidence tier, topic mix, top posts and quality flags. Direction comes only from explicit CALL/PUT plus an open verb, so most posts are neutral. Always read n_voting_authors and flags.",
     "inputSchema": {"type": "object", "properties": {"ticker": {"type": "string"}, "window": _W}, "required": ["ticker"], "additionalProperties": False}},
    {"name": "get_retail_options_bias",
     "description": "SNAPSHOT. Calls versus puts opened in public AfterHour posts: for one ticker, or the most active tickers when none given. The highest-precision sentiment signal because contract side is explicit. Sample is small.",
     "inputSchema": {"type": "object", "properties": {"ticker": {"type": "string"}, "window": _W, "limit": {"type": "integer", "default": 15}}, "additionalProperties": False}},
    {"name": "get_retail_buzz",
     "description": "SNAPSHOT. Which tickers retail is suddenly posting about: mentions versus trailing baseline (z-score once 3+ days of archive exist, else ranked by mentions). Use for 'what is the crowd talking about'. Not a direction signal.",
     "inputSchema": {"type": "object", "properties": {"window": {"type": "string", "enum": ["24h", "72h"], "default": "24h"}, "limit": {"type": "integer", "default": 20}}, "additionalProperties": False}},
    {"name": "get_retail_vs_whale",
     "description": "SNAPSHOT. Tickers where retail stance and verified whale capital pull apart (retail bullish where little whale money sits, or bearish where a lot does). A prompt to investigate, not a signal: whale capital is size, not direction. Needs at least min_voting_authors voters.",
     "inputSchema": {"type": "object", "properties": {"window": {"type": "string", "enum": list(_SENT_WINDOWS), "default": "72h"}, "min_voting_authors": {"type": "integer", "default": 2}, "limit": {"type": "integer", "default": 15}}, "additionalProperties": False}},
    {"name": "get_sentiment_flags",
     "description": "SNAPSHOT. Quality flags for a ticker's retail sentiment: copy-paste duplicate posts, low-follower author share, authors with a Telegram link in bio, authors on the funnel list. Call before trusting get_retail_sentiment. Flagged for investigation, not a finding of fraud.",
     "inputSchema": {"type": "object", "properties": {"ticker": {"type": "string"}, "window": _W}, "required": ["ticker"], "additionalProperties": False}},
    {"name": "get_ticker_posts",
     "description": "SNAPSHOT of the most recent ~400 archived public posts, parsed (stance, action, tickers). Filter by ticker or username. Use to read the posts behind a sentiment score. For one post by link use get_post_permalink.",
     "inputSchema": {"type": "object", "properties": {"ticker": {"type": "string"}, "username": {"type": "string"}, "limit": {"type": "integer", "default": 20}}, "additionalProperties": False}},
    {"name": "get_sentiment_trend",
     "description": "SNAPSHOT. Daily post count and net retail score for a ticker over up to 14 days of archive. Depth is limited by how long the archive has been running.",
     "inputSchema": {"type": "object", "properties": {"ticker": {"type": "string"}, "days": {"type": "integer", "default": 7}}, "required": ["ticker"], "additionalProperties": False}},
]



# ==============================================================================
# WHALE POSITION TOOLS (live portfolio proxy + changes archived by ah_whales.py)
# ==============================================================================

_WHALE_NOTE = ("Positions are the last broker sync marked to live prices. Most whales' last_synced_at is weeks or months "
               "old, so quantities rarely change. These are reported position changes, not trades. Public portfolios only. Not advice.")


def _whale_pid(username):
    for w in (fetch_json("whales.json") or {}).get("whales", []):
        if (w.get("username") or "").lower() == username.lower():
            return w.get("profile_id"), w.get("username")
    return None, None


def tool_get_live_portfolio(args: dict) -> dict:
    u = (args.get("username") or "").strip().lstrip("@")
    if not _USER_RE.match(u):
        return _bad("username is required")
    pid, name = _whale_pid(u)
    if not pid:
        try:
            prof, _, _ = ah_get("/public/profile", {"username": u}, ttl=300.0)
        except UpstreamError as e:
            return {"error": f"AfterHour upstream unavailable ({e})", "retryable": True}
        if prof.get("financialDataPrivacyMode") != "PUBLIC" or not prof.get("hasConnectedItems"):
            return _bad("no public portfolio for that user")
        pid, name = prof.get("id"), prof.get("username")
    min_value = float(args.get("min_value", 0))
    inc_opt = bool(args.get("include_options", True))

    def shape(d):
        rows = []
        tv = d.get("totalValue") or 0
        for p in d.get("positionSnapshots") or []:
            opt = p.get("optionsContractType")
            if opt and not inc_opt:
                continue
            if (p.get("value") or 0) < min_value:
                continue
            spc = p.get("optionsSharesPerContract") or 100
            r = {"symbol": p.get("tickerSymbol"), "root": p.get("rootTickerSymbol"), "type": p.get("type"),
                 "quantity": p.get("quantity"), "price": p.get("price"), "value": p.get("value"),
                 "pct_of_portfolio": round((p.get("value") or 0) / tv * 100, 2) if tv else None,
                 "cost_basis": p.get("costBasis"), "profit_pct": p.get("profitPercent"),
                 "profit_today_pct": p.get("profitPercentToday"), "is_merged": bool(p.get("isMerged"))}
            if opt:
                r.update(option=opt, strike=p.get("optionsStrikePrice"), expiry=(p.get("optionsExpirationDate") or "")[:10],
                         contracts=round((p.get("quantity") or 0) / spc, 4))
            rows.append(r)
        rows.sort(key=lambda r: r["value"] or 0, reverse=True)
        return {"username": name, "total_value": d.get("totalValue"), "cash": d.get("cashBalance"),
                "profit_today": d.get("profitToday"), "profit_today_pct": d.get("profitTodayPercent"),
                "prices_as_of": d.get("verifiedAsOf"), "last_synced_at": d.get("lastSyncedAt"),
                "positions": rows, "note": _WHALE_NOTE}

    return _live(f"/stonks/public/portfolio/{pid}/summary/live", ttl=60.0, shape=shape)


def _whale_changes(since_days):
    d = fetch_json("whale-changes.json")
    if not d:
        return None, None
    cut = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return d, [c for c in d.get("changes", []) if c["ts"] >= cut]


def tool_get_position_changes(args: dict) -> dict:
    d, rows = _whale_changes(max(1, min(int(args.get("since_days", 7)), 30)))
    if d is None:
        return {"error": "whale change feed not yet published", "retryable": True}
    u = (args.get("username") or "").strip().lstrip("@").lower()
    tk = (args.get("ticker") or "").strip().upper().lstrip("$")
    min_n = float(args.get("min_notional", 0))
    min_p = float(args.get("min_pct_of_portfolio", 0))
    act = (args.get("action") or "").upper()
    lim = max(1, min(int(args.get("limit", 50)), 200))
    rows = [c for c in rows
            if (not u or c["username"].lower() == u) and (not tk or c["root"] == tk or c["symbol"] == tk)
            and abs(c["notional_delta"]) >= min_n and (c["pct_of_portfolio"] or 0) >= min_p and (not act or c["action"] == act)]
    keep = ("ts", "username", "action", "symbol", "root", "qty_before", "qty_after", "notional_delta", "pct_of_portfolio",
            "option", "strike", "expiry", "contracts_delta", "lot_ambiguous", "possible_roll", "last_synced_at")
    return {"as_of": d.get("generated_at"), "matched": len(rows), "note": _WHALE_NOTE,
            "changes": [{k: c[k] for k in keep if k in c} for c in rows[:lim]]}


def tool_get_ticker_whale_flow(args: dict) -> dict:
    tk = (args.get("symbol") or "").strip().upper().lstrip("$")
    if not tk:
        return _bad("symbol is required")
    d, rows = _whale_changes(max(1, min(int(args.get("since_days", 7)), 30)))
    if d is None:
        return {"error": "whale change feed not yet published", "retryable": True}
    rows = [c for c in rows if c["root"] == tk]
    net = sum(c["notional_delta"] for c in rows)
    return {"symbol": tk, "as_of": d.get("generated_at"), "net_notional_delta": round(net, 2), "changes": len(rows),
            "adds_opens": sum(1 for c in rows if c["action"] in ("ADD", "OPEN")),
            "trims_closes": sum(1 for c in rows if c["action"] in ("TRIM", "CLOSE", "EXPIRED")),
            "whales": sorted({c["username"] for c in rows}), "note": _WHALE_NOTE}


def tool_get_whale_sync_health(args: dict) -> dict:
    d = fetch_json("whale-sync.json")
    if not d:
        return {"error": "whale sync health not yet published", "retryable": True}
    return {k: d[k] for k in d if k != "whales"}


WHALE_TOOLS_MAP = {
    "get_live_portfolio": tool_get_live_portfolio,
    "get_position_changes": tool_get_position_changes,
    "get_ticker_whale_flow": tool_get_ticker_whale_flow,
    "get_whale_sync_health": tool_get_whale_sync_health,
}
WHALE_TOOL_DEFINITIONS = [
    {"name": "get_live_portfolio",
     "description": "LIVE (60s cache). Current positions of a PUBLIC AfterHour portfolio marked to live prices: value, share of portfolio, P&L today, options with strike, expiry and contracts. Includes last_synced_at: quantities are only as fresh as the broker sync, often months old. Use get_whale_portfolio for the cached census view.",
     "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}, "min_value": {"type": "number", "default": 0}, "include_options": {"type": "boolean", "default": True}}, "required": ["username"], "additionalProperties": False}},
    {"name": "get_position_changes",
     "description": "SNAPSHOT (polled every few minutes for top whales, twice a day for the rest). Reported quantity changes in public whale portfolios: OPEN, ADD, TRIM, CLOSE, EXPIRED, FLIP, with notional and percent of portfolio. Filter by user, ticker, action or size. Changes are rare because broker syncs are infrequent. Reported changes, not trades.",
     "inputSchema": {"type": "object", "properties": {"username": {"type": "string"}, "ticker": {"type": "string"}, "action": {"type": "string", "enum": ["OPEN", "ADD", "TRIM", "CLOSE", "EXPIRED", "FLIP"]}, "since_days": {"type": "integer", "default": 7}, "min_notional": {"type": "number", "default": 0}, "min_pct_of_portfolio": {"type": "number", "default": 0}, "limit": {"type": "integer", "default": 50}}, "additionalProperties": False}},
    {"name": "get_ticker_whale_flow",
     "description": "SNAPSHOT. Net reported whale position change in one ticker over recent days: net notional, adds/opens versus trims/closes, which whales. Options roll up to the underlying.",
     "inputSchema": {"type": "object", "properties": {"symbol": {"type": "string"}, "since_days": {"type": "integer", "default": 7}}, "required": ["symbol"], "additionalProperties": False}},
    {"name": "get_whale_sync_health",
     "description": "SNAPSHOT. How trustworthy the whale position data is right now: whales tracked, polled in the last hour, newest and oldest broker sync, count synced within 30 days. Check before reading get_position_changes.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
]


# Registry mapping tool name -> handler function
TOOLS_MAP = {
    "get_market_tape": tool_get_market_tape,
    "get_top_equities": tool_get_top_equities,
    "get_etf_flows": tool_get_etf_flows,
    "get_whale_portfolio": tool_get_whale_portfolio,
    "get_ticker_intel": tool_get_ticker_intel,
    "get_conviction_screener": tool_get_conviction_screener,
    "screen_whales": tool_screen_whales,
    "get_shadow_whales": tool_get_shadow_whales,
    "get_price_history": tool_get_price_history,
    "get_social_feed": tool_get_social_feed,
    "get_funnel_accounts": tool_get_funnel_accounts,
    "get_funnel_callouts": tool_get_funnel_callouts,
    "get_funnel_tickers": tool_get_funnel_tickers,
    "get_funnel_scorecard": tool_get_funnel_scorecard,
}

# MCP Tool Schemas definition (MCP 2024-11-05 standard)
MCP_TOOLS_DEFINITIONS = [
    {
        "name": "get_market_tape",
        "description": "Retrieve real-time macro tape overview: whale cash reserves (dry powder), intraday net P&L, equity/ETF allocation split, and top capital inflow & retail breadth leaders from AfterHour terminal.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
    {
        "name": "get_top_equities",
        "description": "Filter and rank 500 verified stocks with customizable thresholds for whale capital, owner count, conviction intensity ($/holder), price movement, and asset type segregation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of items to return (default: 20, max: 100)",
                    "default": 20
                },
                "min_whale_capital": {
                    "type": "number",
                    "description": "Minimum verified capital held by tracked whales in USD (e.g. 1000000 for $1M+)",
                    "default": 0
                },
                "min_conviction": {
                    "type": "number",
                    "description": "Minimum verified position size per holder in USD (e.g. 50000 for $50k+/sub)",
                    "default": 0
                },
                "min_owners": {
                    "type": "integer",
                    "description": "Minimum number of verified holders on the app",
                    "default": 0
                },
                "asset_type": {
                    "type": "string",
                    "enum": ["all", "stocks", "etfs"],
                    "description": "Segregate by asset classification (default: 'all')",
                    "default": "all"
                },
                "sort_by": {
                    "type": "string",
                    "enum": ["whale_capital", "total_value", "owners", "conviction", "change_percent"],
                    "description": "Metric to rank results by (default: 'whale_capital')",
                    "default": "whale_capital"
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_etf_flows",
        "description": "Inspect 64 ETFs & index funds ranked by whale backing, expense ratios, asset classes (equity, broad market, thematic, crypto, fixed income), and retail crowd adoption.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum ETFs to return (default: 20)",
                    "default": 20
                },
                "sort_by": {
                    "type": "string",
                    "enum": ["whale_capital", "owners", "total_value", "change_percent"],
                    "description": "Metric to rank ETFs by (default: 'whale_capital')",
                    "default": "whale_capital"
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_whale_portfolio",
        "description": "Look up any verified whale account by username (e.g. 'thealexperez', 'SirJackALot', 'MisterMonster') to inspect verified positions, cost basis, unrealized profit, cash balance, and shadow ratio.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "AfterHour username of the whale to audit (with or without '@')"
                }
            },
            "required": ["username"],
            "additionalProperties": False
        }
    },
    {
        "name": "get_ticker_intel",
        "description": "Forensic intelligence on any ticker ($NVDA, $ASTS, $AAPL, etc.) with verified holders, conviction intensity ($/sub), top whale holders breakdown, and optional 90-day daily OHLCV bars.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock or ETF ticker symbol (e.g. 'ASTS', 'NVDA', 'AAPL', 'QQQ')"
                },
                "include_bars": {
                    "type": "boolean",
                    "description": "Set to true to include the 90-day daily OHLCV candlestick price bars series",
                    "default": False
                }
            },
            "required": ["ticker"],
            "additionalProperties": False
        }
    },
    {
        "name": "get_conviction_screener",
        "description": "Scan for asymmetric high conviction where average equity per holder exceeds a given threshold (e.g. $50,000+ or $100,000+), unmasking institutional accumulation before retail headlines.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "min_intensity": {
                    "type": "number",
                    "description": "Minimum average position size per holder in USD (default: 50000)",
                    "default": 50000
                },
                "min_owners": {
                    "type": "integer",
                    "description": "Minimum verified owners to eliminate illiquid micro-caps (default: 15)",
                    "default": 15
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tickers to return (default: 20)",
                    "default": 20
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "screen_whales",
        "description": "Filter and rank 424 broker-verified whales and millionaires by net worth, cash reserves, unrealized profit, daily return, follower counts, and shadow ratio.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "min_net_worth": {
                    "type": "number",
                    "description": "Minimum verified portfolio value in USD (e.g. 1000000 for $1M+)",
                    "default": 0
                },
                "min_cash": {
                    "type": "number",
                    "description": "Minimum uninvested cash balance in USD (dry powder)",
                    "default": 0
                },
                "min_profit": {
                    "type": "number",
                    "description": "Minimum total unrealized profit in USD",
                    "default": 0
                },
                "min_profit_pct": {
                    "type": "number",
                    "description": "Minimum profit percentage (e.g. 25 for +25%)",
                    "default": 0
                },
                "min_followers": {
                    "type": "integer",
                    "description": "Minimum social followers on the platform",
                    "default": 0
                },
                "max_followers": {
                    "type": "integer",
                    "description": "Maximum social followers (useful for filtering stealth whales)",
                },
                "sort_by": {
                    "type": "string",
                    "enum": ["net_worth", "cash", "profit", "profit_percent", "profit_today", "followers", "shadow_ratio"],
                    "description": "Metric to rank whales by (default: 'net_worth')",
                    "default": "net_worth"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of whales to return (default: 20, max: 100)",
                    "default": 20
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_shadow_whales",
        "description": "Scan for Clout Inversions and stealth accounts: verified traders holding high capital ($500k+ to $15M+) with negligible retail followings (<500 followers).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "min_capital": {
                    "type": "number",
                    "description": "Minimum verified capital in USD (default: 500000)",
                    "default": 500000
                },
                "max_followers": {
                    "type": "integer",
                    "description": "Maximum allowed follower count (default: 500)",
                    "default": 500
                },
                "min_shadow_ratio": {
                    "type": "number",
                    "description": "Minimum verified capital divided by followers (default: 2000)",
                    "default": 2000
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of shadow whales to return (default: 20)",
                    "default": 20
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_price_history",
        "description": "Retrieve daily OHLCV candlestick price bars and returns for core market benchmarks and equities (NVDA, TSLA, SPY, AAPL, QQQ, MSTR, ASTS, etc.).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock or ETF ticker symbol (e.g. 'NVDA', 'ASTS', 'SPY')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of daily bars to return (default: 60, max: 120)",
                    "default": 60
                }
            },
            "required": ["ticker"],
            "additionalProperties": False
        }
    },
    {
        "name": "get_social_feed",
        "description": "Retrieve real-time community posts, commentary, sentiment, and broker-verified trade snapshots from AfterHour traders.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Filter posts mentioning a specific ticker (e.g. 'NVDA' or 'ASTS')"
                },
                "username": {
                    "type": "string",
                    "description": "Filter posts authored by a specific trader handle"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of posts to return (default: 20, max: 50)",
                    "default": 20
                }
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_funnel_accounts",
        "description": "Look up AfterHour accounts flagged for funneling traders into Telegram channels, with evidence tier (reported/corroborated/verified), shared invite-link clusters, and posting stats. Check a username or t.me link before you join. Flagged for investigation, not a finding of fraud. Curated by https://telegramscammers.com (database: /database, submit intel: /submit).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "AfterHour username (substring match)"},
                "telegram_link": {"type": "string", "description": "t.me link or handle to look up (e.g. 't.me/gammasphere47')"},
                "tier": {"type": "string", "enum": ["reported", "corroborated", "verified"], "description": "Filter by evidence tier"},
                "limit": {"type": "integer", "description": "Max accounts to return (default 25, max 100)", "default": 25}
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_funnel_callouts",
        "description": "Parsed trade callouts (ticker, side, strike, expiry, entry, action, quoted result) from public Telegram channels linked to flagged AfterHour accounts, with an independent scored 'outcome' where available. Quoted results are the channel's own claims, and the sample is small. Flagged for investigation, not a finding of fraud. Curated by https://telegramscammers.com.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Ticker symbol, e.g. 'SPY'"},
                "channel": {"type": "string", "description": "Channel handle or t.me link (substring match)"},
                "action": {"type": "string", "enum": ["open", "close", "mention"], "description": "Filter by callout action"},
                "limit": {"type": "integer", "description": "Max callouts to return (default 25, max 100)", "default": 25}
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_funnel_tickers",
        "description": "Tickers most called out by flagged AfterHour accounts and the Telegram channels they link to, ranked, with account, channel and post counts. Flagged for investigation, not a finding of fraud. Curated by https://telegramscammers.com.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "Max tickers to return (default 25, max 100)", "default": 25}
            },
            "additionalProperties": False
        }
    },
    {
        "name": "get_funnel_scorecard",
        "description": "Public scoring results for trade callouts posted by Telegram channels linked to flagged AfterHour accounts. Section 'paths' (the main view): what each called-out option contract did after the post, from its own 5-minute trade bars (calls posted in the session get the next 30 minutes, daily callouts the whole next session; fill = open of the first bar at or after the post): share that ended above the fill, median peak and drawdown, +50%/-50% TP-first versus SL-first, fill-delay sensitivity, unfillable-quote share, per channel, ticker and hour. Section 'options': the same callouts held to expiry (secondary view). Section 'fx': forex/gold/index signals (TP1 first versus SL first, mean R). Every rate carries its sample size and a Wilson 95% range; assumptions and limitations are included (trade prints, no spread or slippage). Analysis of public posts, not advice. Flagged for investigation, not a finding of fraud. Credit https://telegramscammers.com. Method: https://ah.mphinance.com/scorecard",
        "inputSchema": {
            "type": "object",
            "properties": {
                "section": {"type": "string", "enum": ["paths", "options", "fx", "all"], "description": "Which part to return: paths (price paths after the call), options (held to expiry), fx, or all (default all)", "default": "all"},
                "channel": {"type": "string", "description": "Channel handle or t.me link (substring match); filters the per-channel tables"}
            },
            "additionalProperties": False
        }
    }
]

TOOLS_MAP.update(LIVE_TOOLS_MAP)
MCP_TOOLS_DEFINITIONS.extend(LIVE_TOOL_DEFINITIONS)
TOOLS_MAP.update(SENTIMENT_TOOLS_MAP)
MCP_TOOLS_DEFINITIONS.extend(SENTIMENT_TOOL_DEFINITIONS)
TOOLS_MAP.update(WHALE_TOOLS_MAP)
MCP_TOOLS_DEFINITIONS.extend(WHALE_TOOL_DEFINITIONS)

# MCP Resources (MCP 2024-11-05 standard)
MCP_RESOURCES_DEFINITIONS = [
    {
        "uri": "aftermath://market-tape",
        "name": "Live Market Tape & Liquidity",
        "description": "Real-time snapshot of whale cash reserves, net daily profit, and asset allocation.",
        "mimeType": "application/json"
    },
    {
        "uri": "aftermath://top-stocks",
        "name": "Top Verified Equities",
        "description": "Top 50 securities by verified whale capital.",
        "mimeType": "application/json"
    },
    {
        "uri": "aftermath://etfs",
        "name": "All 64 Verified ETFs",
        "description": "Complete list of ETFs with whale backing and asset classifications.",
        "mimeType": "application/json"
    },
    {
        "uri": "aftermath://whales",
        "name": "Top Verified Whales",
        "description": "Top 50 verified whales ranked by net worth.",
        "mimeType": "application/json"
    },
    {
        "uri": "aftermath://shadow-whales",
        "name": "Shadow Whales & Clout Inversions",
        "description": "Stealth traders with massive verified capital and minimal retail followings.",
        "mimeType": "application/json"
    },
    {
        "uri": "aftermath://conviction",
        "name": "Asymmetric Conviction Screener",
        "description": "Top securities ranked by verified position size per holder ($/sub).",
        "mimeType": "application/json"
    },
    {
        "uri": "aftermath://social-feed",
        "name": "Live Social Trade Feed",
        "description": "Recent verified community posts and live trade snapshots.",
        "mimeType": "application/json"
    }
]

# MCP Prompts (MCP 2024-11-05 / 2025-03-26 standard)
MCP_PROMPTS_DEFINITIONS = [
    {
        "name": "whale_dossier",
        "description": "Guided forensic audit of a verified whale portfolio: cash reserves, concentrated holdings, cost basis, unrealized P&L, and shadow ratio.",
        "arguments": [
            {
                "name": "username",
                "description": "AfterHour username of the whale to audit (e.g. 'SIRJACK' or 'TrogdorStrikesAgain')",
                "required": True
            }
        ]
    },
    {
        "name": "conviction_hunt",
        "description": "Screen for asymmetric institutional accumulation where average capital per verified holder ($/sub) spikes before price discovery occurs.",
        "arguments": [
            {
                "name": "min_conviction",
                "description": "Minimum position size per holder in USD (default: '50000')",
                "required": False
            },
            {
                "name": "asset_type",
                "description": "Asset classification ('all', 'stocks', 'etfs', default: 'all')",
                "required": False
            }
        ]
    },
    {
        "name": "shadow_whale_intel",
        "description": "Unmask stealth whales with massive verified net worth ($1M+ to $15M+) who trade quietly with minimal retail followings.",
        "arguments": [
            {
                "name": "min_capital",
                "description": "Minimum portfolio value in USD (default: '1000000')",
                "required": False
            },
            {
                "name": "max_followers",
                "description": "Maximum social followers to qualify as stealth (default: '250')",
                "required": False
            }
        ]
    }
]

# ==============================================================================
# JSON-RPC DISPATCHER
# ==============================================================================

def handle_jsonrpc(req: dict) -> dict:
    """Process a single JSON-RPC 2.0 request and return the response."""
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if not method:
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32600, "message": "Invalid Request: method is missing"}}

    # Handshake & Lifecycle
    if method == "initialize":
        requested = params.get("protocolVersion")
        # Echo the client's version when supported, otherwise fall back to our
        # newest supported version (never silently downgrade the client).
        if requested in SUPPORTED_PROTOCOL_VERSIONS:
            negotiated_version = requested
        else:
            negotiated_version = DEFAULT_PROTOCOL_VERSION
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": negotiated_version,
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                    "prompts": {"listChanged": False}
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": VERSION
                },
                "instructions": (
                    "Real-time AfterHour alt-data: verified whale portfolios, "
                    "conviction intensity, ETF flows, and the macro tape."
                )
            }
        }

    # Notifications never receive a response.
    if method.startswith("notifications/"):
        return None

    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    # Advertised-but-empty capabilities: 2025-* clients probe these at startup.
    if method == "prompts/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"prompts": MCP_PROMPTS_DEFINITIONS}}

    if method == "prompts/get":
        prompt_name = params.get("name")
        args = params.get("arguments", {})
        if prompt_name == "whale_dossier":
            u = args.get("username", "SIRJACK")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "description": f"Audit verified whale @{u}",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": f"Execute a deep forensic audit on @{u}. Call `get_whale_portfolio` with username='{u}' and `get_social_feed` with username='{u}'. Analyze cash allocation, risk posture, top concentrated bets, cost basis versus current price, and recent verified trade activity."
                            }
                        }
                    ]
                }
            }
        elif prompt_name == "conviction_hunt":
            min_c = args.get("min_conviction", "50000")
            asset_t = args.get("asset_type", "all")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "description": "Hunt for asymmetric conviction",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": f"Scan the AfterHour verified universe for high-conviction accumulation (min_conviction={min_c}, asset_type='{asset_t}'). Call `get_conviction_screener` and `get_top_equities` sorted by conviction. Identify tickers where small cohorts of verified whales have deployed massive capital per seat."
                            }
                        }
                    ]
                }
            }
        elif prompt_name == "shadow_whale_intel":
            min_cap = args.get("min_capital", "1000000")
            max_f = args.get("max_followers", "250")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "description": "Unmask stealth whales",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": f"Identify the top shadow whales on AfterHour. Call `get_shadow_whales` with min_capital={min_cap} and max_followers={max_f}. Detail their total net worth, follower count, shadow ratio, and top concentrated equity holdings."
                            }
                        }
                    ]
                }
            }
        else:
            return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32602, "message": f"Unknown prompt: {prompt_name}"}}

    if method == "resources/templates/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"resourceTemplates": []}}

    if method == "logging/setLevel":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    if method == "completion/complete":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"completion": {"values": []}}}

    # Tools
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": MCP_TOOLS_DEFINITIONS
            }
        }

    if method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        if tool_name not in TOOLS_MAP:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
            }

        try:
            handler = TOOLS_MAP[tool_name]
            result_data = handler(tool_args)
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result_data, indent=2)
                    }
                ]
            }
            if isinstance(result_data, dict):
                result["structuredContent"] = result_data
            return {"jsonrpc": "2.0", "id": msg_id, "result": result}
        except Exception as e:
            debug_log(f"Error calling {tool_name}: {e}")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "isError": True,
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({"error": str(e), "tool": tool_name})
                        }
                    ]
                }
            }

    # Resources
    if method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "resources": MCP_RESOURCES_DEFINITIONS
            }
        }

    if method == "resources/read":
        uri = params.get("uri")
        if uri == "aftermath://market-tape":
            payload = tool_get_market_tape({})
        elif uri == "aftermath://top-stocks":
            payload = tool_get_top_equities({"limit": 50})
        elif uri == "aftermath://etfs":
            payload = tool_get_etf_flows({"limit": 64})
        elif uri == "aftermath://whales":
            wdata = fetch_json("whales.json") or {}
            payload = wdata.get("whales", [])[:50]
        elif uri == "aftermath://shadow-whales":
            payload = tool_get_shadow_whales({"limit": 50})
        elif uri == "aftermath://conviction":
            payload = tool_get_conviction_screener({"min_intensity": 50000, "limit": 50})
        elif uri == "aftermath://social-feed":
            payload = tool_get_social_feed({"limit": 50})
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32602, "message": f"Unknown resource URI: {uri}"}
            }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(payload, indent=2)
                    }
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Method '{method}' not implemented"}
    }

def handle_jsonrpc_payload(req):
    """Dispatch a single JSON-RPC request or a batch (array).

    Returns ``(payload, had_response)`` where ``had_response`` is False when the
    payload contained only notifications/respondless messages (e.g. the MCP
    ``notifications/initialized`` handshake).
    """
    if isinstance(req, list):
        responses = [handle_jsonrpc(r) for r in req if isinstance(r, dict)]
        responses = [r for r in responses if r is not None]
        if not responses:
            return None, False
        return responses, True
    resp = handle_jsonrpc(req)
    if resp is None:
        return None, False
    return resp, True

# ==============================================================================
# MAIN STDIO LOOP & SELF-TEST
# ==============================================================================

def run_self_test():
    """Execute local diagnostic test verifying the tool registry."""
    print(f"=== {SERVER_NAME} v{VERSION} Diagnostic Test ===")
    
    print("\n1. Testing get_market_tape...")
    t1 = tool_get_market_tape({})
    print(f"   Tape Keys: {list(t1.keys())[:5]}")

    print("\n2. Testing get_top_equities (min_conviction=50k)...")
    t2 = tool_get_top_equities({"limit": 3, "min_conviction": 50000})
    for s in t2.get("results", []):
        print(f"   ${s['ticker']} - Conviction: ${s['convictionPerHolder']:,.0f} (Whale Cap: ${s['whaleCapital']:,.0f})")

    print("\n3. Testing get_etf_flows...")
    t3 = tool_get_etf_flows({"limit": 3})
    for e in t3.get("results", []):
        print(f"   ${e['ticker']} ({e['name']}) - Owners: {e['owners']}")

    print("\n4. Testing get_whale_portfolio (SIRJACK)...")
    t4 = tool_get_whale_portfolio({"username": "SIRJACK"})
    print(f"   SIRJACK Total Value: ${t4.get('total_value', 0):,.2f} across {t4.get('position_count', 0)} positions")

    print("\n5. Testing get_ticker_intel (ASTS)...")
    t5 = tool_get_ticker_intel({"ticker": "ASTS"})
    print(f"   $ASTS Owners: {t5.get('verifiedOwnersCount')}, Conviction: ${t5.get('convictionIntensityPerHolder', 0):,.0f}/sub")

    print("\n6. Testing get_conviction_screener ($100k+)...")
    t6 = tool_get_conviction_screener({"min_intensity": 100000, "limit": 3})
    for r in t6.get("results", []):
        print(f"   ${r['ticker']} - ${r['convictionPerHolder']:,.0f}/sub ({r['owners']} owners)")

    print("\n7. Testing screen_whales (min_net_worth=5M)...")
    t7 = tool_screen_whales({"min_net_worth": 5000000, "limit": 3})
    for w in t7.get("whales", []):
        print(f"   @{w['username']} - Net Worth: ${w['total_value']:,.2f}, Cash: ${w['cash_balance']:,.2f}")

    print("\n8. Testing get_shadow_whales (min_capital=1M, max_followers=300)...")
    t8 = tool_get_shadow_whales({"min_capital": 1000000, "max_followers": 300, "limit": 3})
    for s in t8.get("whales", []):
        print(f"   @{s['username']} - Capital: ${s['total_value']:,.2f} / {s['followers']} flw (Ratio: ${s['shadow_ratio']:,.0f}/flw)")

    print("\n9. Testing get_price_history (NVDA)...")
    t9 = tool_get_price_history({"ticker": "NVDA", "limit": 5})
    print(f"   $NVDA Bars: {t9.get('bars_returned')} returned, Latest Close: ${t9.get('summary', {}).get('latest_close')}")

    print("\n10. Testing get_social_feed (limit=3)...")
    t10 = tool_get_social_feed({"limit": 3})
    print(f"   Feed posts returned: {len(t10.get('posts', []))}")

    print(f"\n[+] All {len(TOOLS_MAP)} MCP tools registered.")

# ==============================================================================
# HTTP & SSE SERVER (FOR REMOTE MCP CLIENTS & MCP-REMOTE)
# ==============================================================================

class McpHttpHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Route server logs through debug_log (stderr)
        debug_log(f"HTTP {self.command} {self.path} - {format % args}")

    def end_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Expose-Headers", "*")

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if not path:
            path = "/"

        if path in ("/sse", "/mcp/sse"):
            session_id = uuid.uuid4().hex
            q = queue.Queue()
            with _SESSIONS_LOCK:
                _SESSIONS[session_id] = q

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self.end_cors_headers()
            self.end_headers()

            # MCP SSE spec: send endpoint event with URI to post messages to
            endpoint_msg = f"event: endpoint\r\ndata: /messages?sessionId={session_id}\r\n\r\n"
            try:
                self.wfile.write(endpoint_msg.encode("utf-8"))
                self.wfile.flush()
            except Exception as e:
                with _SESSIONS_LOCK:
                    _SESSIONS.pop(session_id, None)
                return

            debug_log(f"SSE client connected. Session: {session_id}")

            try:
                while True:
                    try:
                        msg = q.get(timeout=15.0)
                        if msg is None:
                            break
                        chunk = f"event: message\r\ndata: {msg}\r\n\r\n"
                        self.wfile.write(chunk.encode("utf-8"))
                        self.wfile.flush()
                    except queue.Empty:
                        # Send SSE keepalive comment
                        self.wfile.write(b": ping\r\n\r\n")
                        self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, Exception) as e:
                debug_log(f"SSE client disconnected {session_id}: {e}")
            finally:
                with _SESSIONS_LOCK:
                    _SESSIONS.pop(session_id, None)

        elif path in ("/api/mcp", "/mcp", "/rpc"):
            # Streamable HTTP allows the server to decline a server-initiated
            # stream; 405 is the spec-blessed response (a 404 reads as fatal to
            # some clients). Message delivery happens over POST instead.
            self.send_response(405)
            self.send_header("Allow", "POST, OPTIONS")
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(b"Method Not Allowed: POST JSON-RPC to this endpoint")

        elif path == "/api/mcp-schema.json":
            body = json.dumps({
                "version": "1.0.0",
                "server": {"name": "aftermath-altdata", "documentation": "https://ah.mphinance.com/mcp"},
                "tools": MCP_TOOLS_DEFINITIONS,
                "resources": MCP_RESOURCES_DEFINITIONS,
            }, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(body)

        elif path in ("/health", "/status", "/api/health", "/api/mcp/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_cors_headers()
            self.end_headers()
            res = {
                "status": "ok",
                "server": SERVER_NAME,
                "version": VERSION,
                "protocols": list(SUPPORTED_PROTOCOL_VERSIONS),
                "endpoints": {
                    "streamable_http": "/api/mcp",
                    "sse": "/sse",
                    "messages": "/messages?sessionId={id}",
                    "direct_rpc": "/api/mcp",
                    "health": "/health"
                },
                "uptime_seconds": round(time.time() - SERVER_START_TIME, 1),
                "tools_count": len(MCP_TOOLS_DEFINITIONS)
            }
            self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        if path in ("/health", "/status", "/api/health", "/api/mcp/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_cors_headers()
            self.end_headers()
        elif path == "/sse":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_cors_headers()
            self.end_headers()
        elif path in ("/api/mcp", "/mcp", "/rpc"):
            self.send_response(405)
            self.send_header("Allow", "POST, OPTIONS")
            self.end_cors_headers()
            self.end_headers()
        else:
            self.send_response(404)
            self.end_cors_headers()
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else ""

        try:
            req = json.loads(body) if body else {}
        except Exception as e:
            err = json.dumps({"jsonrpc": "2.0", "id": None,
                              "error": {"code": -32700, "message": "Parse error: invalid JSON"}}).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err)))
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(err)
            return

        if path in ("/messages", "/mcp/messages"):
            params = urllib.parse.parse_qs(parsed.query)
            session_id = params.get("sessionId", [None])[0] or params.get("session_id", [None])[0]
            if not session_id or session_id not in _SESSIONS:
                self.send_response(400)
                self.end_cors_headers()
                self.end_headers()
                self.wfile.write(b"Invalid or missing sessionId")
                return

            payload, had_response = handle_jsonrpc_payload(req)
            if had_response:
                with _SESSIONS_LOCK:
                    q = _SESSIONS.get(session_id)
                    if q:
                        for msg in (payload if isinstance(payload, list) else [payload]):
                            q.put(json.dumps(msg))

            self.send_response(202)
            self.send_header("Content-Type", "application/json")
            self.end_cors_headers()
            self.end_headers()

        elif path in ("/api/mcp", "/mcp", "/rpc"):
            # Stateless Streamable HTTP (spec 2025-03-26): a POST carrying only
            # requests gets a JSON body; a POST carrying only notifications or
            # responses is acknowledged with 202 and an empty body.
            payload, had_response = handle_jsonrpc_payload(req)
            if not had_response:
                self.send_response(202)
                self.send_header("Content-Type", "application/json")
                self.end_cors_headers()
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_http_server(port: int = 8088, host: str = "0.0.0.0"):
    """Run concurrent threaded HTTP + SSE MCP server."""
    server_addr = (host, port)
    httpd = http.server.ThreadingHTTPServer(server_addr, McpHttpHandler)
    debug_log(f"Starting {SERVER_NAME} HTTP+SSE server listening on http://{host}:{port}")
    debug_log(f"  Streamable HTTP:     http://{host}:{port}/api/mcp  (POST, stateless)")
    debug_log(f"  SSE endpoint:        http://{host}:{port}/sse")
    debug_log(f"  Messages endpoint:   http://{host}:{port}/messages?sessionId=<id>")
    debug_log(f"  Direct RPC endpoint: http://{host}:{port}/api/mcp")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        debug_log("HTTP server shutting down.")
    finally:
        httpd.server_close()

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--test", "-t", "test"):
        run_self_test()
        sys.exit(0)

    # Check for HTTP/SSE server mode
    port = None
    for idx, arg in enumerate(sys.argv):
        if arg in ("--port", "-p") and idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
        elif arg.startswith("--port="):
            port = int(arg.split("=")[1])
        elif arg in ("--serve", "--sse"):
            port = 8088

    if port:
        run_http_server(port=port)
        sys.exit(0)

    debug_log(f"Starting {SERVER_NAME} v{VERSION} in stdio mode (MCP spec 2024-11-05)")

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            req = json.loads(line)
            # Support JSON-RPC 2.0 batch requests (arrays) as well as singles;
            # notification-only batches intentionally produce no output.
            payload, had_response = handle_jsonrpc_payload(req)
            if had_response:
                out = json.dumps(payload)
                sys.stdout.write(out + "\n")
                sys.stdout.flush()
        except KeyboardInterrupt:
            break
        except BrokenPipeError:
            # Client closed the pipe (normal shutdown); exit quietly.
            break
        except Exception as e:
            debug_log(f"Loop exception (continuing): {e}")

if __name__ == "__main__":
    main()
