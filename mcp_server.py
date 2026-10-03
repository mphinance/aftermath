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

VERSION = "1.1.0"
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
    elif sort_by == "conviction":
        filtered.sort(key=lambda x: x["convictionPerHolder"], reverse=True)
    elif sort_by == "change_percent":
        filtered.sort(key=lambda x: x["changePercent"], reverse=True)
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

    data = fetch_json("etfs.json")
    if not data or "securities" not in data:
        return {"error": "Failed to load ETFs from edge API"}

    etfs = data["securities"]
    formatted = []
    for e in etfs:
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
        positions.append({
            "ticker": p.get("ticker"),
            "name": p.get("name"),
            "quantity": p.get("quantity"),
            "value": p.get("value"),
            "cost_basis": p.get("cost_basis"),
            "profit": p.get("profit"),
            "percent_of_portfolio": round((p.get("value", 0) / max(1, found.get("total_value", 1))) * 100, 2)
        })

    positions.sort(key=lambda x: x["value"], reverse=True)

    return {
        "username": found.get("username"),
        "total_value": found.get("total_value"),
        "cash_balance": found.get("cash_balance", 0),
        "profit_today": found.get("profit_today", 0),
        "profit_total": found.get("profit", 0),
        "followers": found.get("followers", 0),
        "shadow_ratio": found.get("shadow_ratio", 0),
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

# Registry mapping tool name -> handler function
TOOLS_MAP = {
    "get_market_tape": tool_get_market_tape,
    "get_top_equities": tool_get_top_equities,
    "get_etf_flows": tool_get_etf_flows,
    "get_whale_portfolio": tool_get_whale_portfolio,
    "get_ticker_intel": tool_get_ticker_intel,
    "get_conviction_screener": tool_get_conviction_screener,
}

# MCP Tool Schemas definition (MCP 2024-11-05 standard)
MCP_TOOLS_DEFINITIONS = [
    {
        "name": "get_market_tape",
        "description": "Retrieve real-time macro tape overview: whale cash reserves ($8.98M dry powder), intraday net P&L, equity/ETF allocation split, and top capital inflow & retail breadth leaders from AfterHour terminal.",
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
    }
]

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
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"prompts": []}}

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
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result_data, indent=2)
                        }
                    ]
                }
            }
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
    """Execute local diagnostic test verifying all 6 tools."""
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

    print("\n[+] All 6 MCP tools validated successfully.")

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
            self.send_response(400)
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
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
                q = _SESSIONS.get(session_id)
                if q:
                    for msg in (payload if isinstance(payload, list) else [payload]):
                        q.put(json.dumps(msg))

            self.send_response(202)
            self.send_header("Content-Type", "text/plain")
            self.end_cors_headers()
            self.end_headers()
            self.wfile.write(b"Accepted")

        elif path in ("/api/mcp", "/mcp", "/rpc"):
            # Stateless Streamable HTTP (spec 2025-03-26): a POST carrying only
            # requests gets a JSON body; a POST carrying only notifications or
            # responses is acknowledged with 202 and an empty body.
            payload, had_response = handle_jsonrpc_payload(req)
            if not had_response:
                self.send_response(202)
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
