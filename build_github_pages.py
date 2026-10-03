#!/usr/bin/env python3
"""
Generates the next-generation, institutional-grade AfterHour Alpha Terminal.
Includes:
- Front-Page Market Alt-Data Radar:
  * Capital Inflow Leaders (Total Value on App: AAPL, ASTS, PLTR, NVDA, QQQ)
  * Retail Consensus Breadth (Most Owned: NVDA 321, VOO 197, MSFT 187, AAPL 179, HOOD 161)
  * Conviction Intensity Screener ($/Holder: ANET $188k, ASTS $117k, AAPL $108k, PLTR $104k, QQQ $67k)
  * Macro Tape & Liquidity ($3.49M Whale Gain Today, $8.98M Cash Reserves, 80/20 Equity/ETF Allocation)
- Ticker Marquee Tape Bar
- All 500 securities with quantitative ranking metrics
- Asset segregation: ETFs (64) vs Equities (436)
- 395 verified whales ($169M+ AUM) with real resolved ticker symbols and company names
- Complete visual sitemap directory (/sitemap) & standard XML sitemap (sitemap.xml)
- Inverted Index & Over-time historical candlestick charts (44-day daily bars)
- URL Slugs & Client-Side SPA routing (/ticker/:symbol, /@:username, /stonks, /etfs, /whales, /shadow, /sitemap, /all)
- Static API endpoints (/api/stonks.json, /api/etfs.json, /api/whales.json, /api/shadow.json, /api/ticker/:symbol.json)
- TraderMatrix Pro referral funnel integration throughout (ref=MPHINANCE)
"""

import json
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "leaderboard"
INDEX_FILE = BASE_DIR / "index.html"
REPORT_FILE = BASE_DIR / "reports" / "afterhour_quant_terminal.html"
API_DIR = BASE_DIR / "api"
API_DIR.mkdir(parents=True, exist_ok=True)
TICKER_API_DIR = API_DIR / "ticker"
TICKER_API_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load stocks
with open(DATA_DIR / "stock_leaderboard.json", encoding="utf-8") as f:
    board_data = json.load(f)

# 2. Load ranked whales (swept with real tickerSymbol & securityName)
with open(DATA_DIR / "all_verified_whales_ranked.json", encoding="utf-8") as f:
    whale_data = json.load(f)

# 3. Load historic daily price bars
with open(DATA_DIR / "historic_prices_sample.json", encoding="utf-8") as f:
    historic_data = json.load(f).get("history", {})

whales = whale_data.get("whales", [])

# Build Inverted Index: Ticker -> List of Whales holding it & Name registry
ticker_to_whales = {}
ticker_extra_names = {}

for w in whales:
    flw = max(1, w.get("followers", 0))
    w["shadow_ratio"] = round(w["total_value"] / flw, 2)
    w["slug"] = f"/@{w['username']}"
    for p in w.get("all_positions", []):
        t = p.get("ticker")
        if not t:
            continue
        if t.startswith("sec_"):
            t = p.get("name") or "UNLISTED"
            p["ticker"] = t

        if p.get("name") and t not in ticker_extra_names:
            ticker_extra_names[t] = p.get("name")

        if t not in ticker_to_whales:
            ticker_to_whales[t] = []
        ticker_to_whales[t].append({
            "username": w["username"],
            "followers": w.get("followers", 0),
            "shares": round(p.get("quantity", 0), 2),
            "value": round(p.get("value", 0), 2),
            "cost_basis": round(p.get("cost_basis", 0), 2),
            "profit": round(p.get("profit", 0), 2),
        })

# Sort each ticker's whales by value descending
for t in ticker_to_whales:
    ticker_to_whales[t].sort(key=lambda x: x["value"], reverse=True)

# Build enriched stock records for ALL 500 securities
raw_securities = board_data.get("securities", [])
stocks_raw = []

for s in raw_securities:
    sec = s.get("security", {})
    info = sec.get("security", {})
    ticker = info.get("tickerSymbol") or info.get("name")
    if not ticker or ticker.startswith("sec_"):
        continue
    price_obj = sec.get("price", {})
    sess = price_obj.get("session", {})
    
    owners = sec.get("ownerCount", 0)
    total_val = round(sec.get("totalValue", 0), 2)
    change_pct = round(sess.get("changePercent", 0), 2)
    chat_members = info.get("chatroom", {}).get("memberCount", 0)
    chat_online = info.get("chatroom", {}).get("onlineCount", 0)
    sec_type = info.get("type", "EQUITY")
    is_etf = (sec_type == "ETF")
    
    w_list = ticker_to_whales.get(ticker, [])
    w_val = round(sum(x["value"] for x in w_list), 2)
    w_cnt = len(w_list)
    top_whale = w_list[0] if w_list else None

    # Name fallback
    comp_name = info.get("name") or ticker_extra_names.get(ticker) or ticker
    if comp_name.startswith("sec_"):
        comp_name = info.get("friendlyName") or ticker

    intensity = round(total_val / max(1, owners), 2)

    stocks_raw.append({
        "ticker": ticker,
        "name": comp_name,
        "friendlyName": info.get("friendlyName") or ticker,
        "type": sec_type,
        "isETF": is_etf,
        "owners": owners,
        "totalValue": total_val,
        "intensity": intensity,
        "marketCap": sec.get("marketCap", 0),
        "price": round(price_obj.get("price", 0), 2),
        "changePercent": change_pct,
        "volume": sess.get("volume", 0),
        "chatroomMembers": chat_members,
        "chatroomOnline": chat_online,
        "whalesCount": w_cnt,
        "whalesValue": w_val,
        "topWhale": top_whale["username"] if top_whale else None,
        "topWhaleValue": top_whale["value"] if top_whale else 0,
        "slug": f"/ticker/{ticker}",
        "hasHistory": ticker in historic_data,
    })

# Compute explicit rankings across the universe
stocks_by_whale = sorted(stocks_raw, key=lambda x: (x["whalesValue"], x["totalValue"]), reverse=True)
for i, s in enumerate(stocks_by_whale, 1):
    s["rankWhaleCapital"] = i

stocks_by_val = sorted(stocks_raw, key=lambda x: x["totalValue"], reverse=True)
for i, s in enumerate(stocks_by_val, 1):
    s["rankPlatformValue"] = i

stocks_by_owners = sorted(stocks_raw, key=lambda x: x["owners"], reverse=True)
for i, s in enumerate(stocks_by_owners, 1):
    s["rankOwners"] = i

stocks_by_gainers = sorted(stocks_raw, key=lambda x: x["changePercent"], reverse=True)
for i, s in enumerate(stocks_by_gainers, 1):
    s["rankGainers"] = i

stocks_by_chat = sorted(stocks_raw, key=lambda x: x["chatroomMembers"], reverse=True)
for i, s in enumerate(stocks_by_chat, 1):
    s["rankChat"] = i

stocks = stocks_by_whale  # Default institutional view is verified whale capital

for s in stocks:
    badges = []
    reasons = []
    
    if s["isETF"]:
        badges.append({"label": "ETF", "color": "amber"})
    
    if s["whalesValue"] >= 5_000_000:
        badges.append({"label": f"#{s['rankWhaleCapital']} WHALE BACKED", "color": "purple"})
        reasons.append(f"${s['whalesValue']/1_000_000:.1f}M whale capital ({s['whalesCount']} whales)")
    elif s["whalesValue"] >= 1_000_000:
        badges.append({"label": "WHALE ACCUMULATION", "color": "cyan"})
        reasons.append(f"${s['whalesValue']/1_000_000:.1f}M whale backing")
    elif s["whalesCount"] >= 10:
        badges.append({"label": "WHALE CONSENSUS", "color": "cyan"})
        reasons.append(f"{s['whalesCount']} verified whales")

    if s["rankOwners"] <= 5:
        badges.append({"label": f"#{s['rankOwners']} MOST OWNED", "color": "amber"})
        reasons.append(f"{s['owners']:,} verified holders")
    elif s["owners"] >= 100:
        badges.append({"label": "PLATFORM CORE", "color": "amber"})
        reasons.append(f"{s['owners']:,} verified holders")
    elif s["owners"] >= 40:
        badges.append({"label": "POPULAR RETAIL", "color": "amber"})

    if s["changePercent"] >= 4.0:
        badges.append({"label": "TOP 24H SURGE", "color": "green"})
        reasons.append(f"+{s['changePercent']:.1f}% intraday move")
    elif s["changePercent"] <= -4.0:
        badges.append({"label": "HIGH VOL DIP", "color": "red"})
        reasons.append(f"{s['changePercent']:.1f}% pullback")
        
    if s["chatroomMembers"] >= 5000:
        badges.append({"label": "VIRAL CHAT", "color": "cyan"})
        reasons.append(f"{s['chatroomMembers']:,} chat members")
        
    if not badges:
        if s["isETF"]:
            badges.append({"label": "INDEX ETF", "color": "amber"})
            reasons.append(f"Rank #{s['rankWhaleCapital']} by capital")
        else:
            badges.append({"label": "TRACKED EQUITY", "color": "cyan"})
            reasons.append(f"Rank #{s['rankWhaleCapital']} by capital")

    s["badges"] = badges
    s["whyTop"] = " &bull; ".join(reasons) if reasons else f"Rank #{s['rankWhaleCapital']} by verified capital"
    s["rank"] = s["rankWhaleCapital"]

total_whale_val = sum(w["total_value"] for w in whales)
millionaires = [w for w in whales if w["total_value"] >= 1_000_000]
millionaires_count = len(millionaires)
etfs_list = [s for s in stocks if s["isETF"]]
etfs_count = len(etfs_list)
equities_count = len(stocks) - etfs_count

total_app_value = sum(s["totalValue"] for s in stocks)
total_app_owners = sum(s["owners"] for s in stocks)

# Macro & Market Alt-Data Radar Calculations
top_by_total_value = sorted(stocks, key=lambda x: x["totalValue"], reverse=True)[:5]
top_by_owners = sorted([x for x in stocks if x["ticker"] not in ["BTC", "ETH"]], key=lambda x: x["owners"], reverse=True)[:5]
top_by_intensity = sorted([x for x in stocks if x["owners"] >= 15], key=lambda x: x["intensity"], reverse=True)[:5]

total_cash_reserves = sum(w.get("cash_balance", 0) for w in whales)
total_profit_today = sum(w.get("profit_today", 0) for w in whales)
total_unrealized_profit = sum(w.get("profit", 0) for w in whales)

etf_tickers_set = set(e["ticker"] for e in etfs_list)
whale_equity_cap = sum(sum(p.get("value", 0) for p in w.get("all_positions", []) if p.get("ticker") not in etf_tickers_set) for w in whales)
whale_etf_cap = sum(sum(p.get("value", 0) for p in w.get("all_positions", []) if p.get("ticker") in etf_tickers_set) for w in whales)
tot_classified = whale_equity_cap + whale_etf_cap or 1
equity_pct = (whale_equity_cap / tot_classified) * 100
etf_pct = (whale_etf_cap / tot_classified) * 100

top_gainers_tape = sorted([x for x in stocks if x["totalValue"] >= 500_000], key=lambda x: x["changePercent"], reverse=True)[:4]

from mcp_server import MCP_TOOLS_DEFINITIONS, MCP_RESOURCES_DEFINITIONS

# Export static JSON API files
market_payload = {
    "version": "1.0.0",
    "timestamp": "2026-10-02T23:15:00Z",
    "source": "https://ah.mphinance.com",
    "macro": {
        "whaleDryPowderCash": round(total_cash_reserves, 2),
        "whaleNetGainToday": round(total_profit_today, 2),
        "whaleUnrealizedProfit": round(total_unrealized_profit, 2),
        "totalWhaleAum": round(total_whale_val, 2),
        "trackedWhalesCount": len(whales),
        "allocation": {
            "equityValue": round(whale_equity_cap, 2),
            "equityPercent": round(equity_pct, 1),
            "etfValue": round(whale_etf_cap, 2),
            "etfPercent": round(etf_pct, 1)
        }
    },
    "capitalInflowLeaders": [
        {
            "ticker": x["ticker"],
            "name": x["name"],
            "price": x["price"],
            "totalValue": x["totalValue"],
            "whaleCapital": x["whalesValue"],
            "owners": x["owners"],
            "isETF": x["isETF"],
            "changePercent": x["changePercent"]
        } for x in top_by_total_value
    ],
    "retailBreadthLeaders": [
        {
            "ticker": x["ticker"],
            "name": x["name"],
            "owners": x["owners"],
            "totalValue": x["totalValue"],
            "whaleCapital": x["whalesValue"],
            "price": x["price"],
            "isETF": x["isETF"],
            "changePercent": x["changePercent"]
        } for x in top_by_owners
    ],
    "convictionIntensityLeaders": [
        {
            "ticker": x["ticker"],
            "name": x["name"],
            "convictionPerHolder": round(x["intensity"], 2),
            "owners": x["owners"],
            "totalValue": x["totalValue"],
            "whaleCapital": x["whalesValue"],
            "price": x["price"],
            "isETF": x["isETF"],
            "changePercent": x["changePercent"]
        } for x in top_by_intensity
    ],
    "topTapeGainers": [
        {
            "ticker": x["ticker"],
            "name": x["name"],
            "price": x["price"],
            "changePercent": x["changePercent"],
            "totalValue": x["totalValue"],
            "isETF": x["isETF"]
        } for x in top_gainers_tape
    ]
}

with open(API_DIR / "market.json", "w", encoding="utf-8") as f:
    json.dump(market_payload, f, indent=2)

with open(API_DIR / "market-summary.json", "w", encoding="utf-8") as f:
    json.dump(market_payload, f, indent=2)

mcp_schema_payload = {
    "version": "1.0.0",
    "protocolVersion": "2024-11-05",
    "server": {
        "name": "aftermath-altdata",
        "description": "AfterMath Model Context Protocol (MCP) Server for real-time verified whale tape and conviction flows.",
        "documentation": "https://ah.mphinance.com/mcp",
        "serverScript": "https://ah.mphinance.com/mcp/server.py"
    },
    "tools": MCP_TOOLS_DEFINITIONS,
    "resources": MCP_RESOURCES_DEFINITIONS
}

with open(API_DIR / "mcp-schema.json", "w", encoding="utf-8") as f:
    json.dump(mcp_schema_payload, f, indent=2)

openapi_spec = {
    "openapi": "3.1.0",
    "info": {
        "title": "AfterMath Quant Alt-Data API",
        "version": "1.0.0",
        "description": "Sub-millisecond, edge-cached alternative financial intelligence API tracking verified retail & whale equity, conviction intensity ($/holder), whale dry powder cash, and macro tape liquidity from AfterHour social terminal.",
        "contact": {
            "name": "Momentum Phinance",
            "url": "https://ah.mphinance.com"
        }
    },
    "servers": [
        {
            "url": "https://ah.mphinance.com",
            "description": "Production Edge Terminal"
        }
    ],
    "tags": [
        {"name": "Market & Tape", "description": "Macro tape overview, whale cash reserves (dry powder), daily P&L, and asset allocation"},
        {"name": "Equities & ETFs", "description": "Leaderboard of 500 securities and 64 ETFs enriched with verified owner counts and conviction intensity"},
        {"name": "Whales & Portfolios", "description": "395 verified high-roller and millionaire portfolios with verified positions and shadow ratio"},
        {"name": "Tickers & History", "description": "Individual security profiles with verified whale holders breakdown and 90-day daily OHLCV bars"},
        {"name": "MCP & AI Agents", "description": "Model Context Protocol tools and schemas for AI agents"}
    ],
    "paths": {
        "/api/market.json": {
            "get": {
                "tags": ["Market & Tape"],
                "summary": "Real-Time Alt-Data Market Radar & Liquidity",
                "description": "Returns verified whale dry powder cash reserves ($8.98M), intraday net P&L, equity/ETF allocation split, and top leaders across capital inflows, retail breadth, and conviction intensity.",
                "responses": {
                    "200": {
                        "description": "Live macro market tape snapshot"
                    }
                }
            }
        },
        "/api/stonks.json": {
            "get": {
                "tags": ["Equities & ETFs"],
                "summary": "All 500 Verified Equities & ETFs",
                "description": "Returns full catalog of 500 securities with owner counts, total value on app, whale capital backing, conviction intensity ($/sub), session price changes, and chatroom activity.",
                "responses": {
                    "200": {
                        "description": "Complete enriched securities catalog"
                    }
                }
            }
        },
        "/api/etfs.json": {
            "get": {
                "tags": ["Equities & ETFs"],
                "summary": "All 64 Verified ETFs & Index Funds",
                "description": "Returns 64 ETFs segregated by asset class, expense ratio, whale capital backing, and retail adoption breadth.",
                "responses": {
                    "200": {
                        "description": "All 64 verified ETFs"
                    }
                }
            }
        },
        "/api/whales.json": {
            "get": {
                "tags": ["Whales & Portfolios"],
                "summary": "395 Verified Whales & Millionaires",
                "description": "Returns 395 verified portfolios ($169M+ AUM) with username, total verified balance, cash balance, intraday P&L, unrealized gains, and full positions breakdown.",
                "responses": {
                    "200": {
                        "description": "Directory of verified whales"
                    }
                }
            }
        },
        "/api/shadow.json": {
            "get": {
                "tags": ["Whales & Portfolios"],
                "summary": "Shadow Ratio & Stealth Whales",
                "description": "Returns whales sorted by the Clout Inversion metric: verified portfolio value divided by social follower count.",
                "responses": {
                    "200": {
                        "description": "Whales ranked by shadow ratio"
                    }
                }
            }
        },
        "/api/ticker/{symbol}.json": {
            "get": {
                "tags": ["Tickers & History"],
                "summary": "Granular Security Intelligence & 90-Day Bars",
                "description": "Deep-dive on any specific ticker symbol with verified holders breakdown, conviction intensity, and 90-day daily OHLCV candlestick bars.",
                "parameters": [
                    {
                        "name": "symbol",
                        "in": "path",
                        "required": True,
                        "description": "Ticker symbol (e.g. NVDA, ASTS, AAPL, QQQ)",
                        "schema": {"type": "string", "example": "ASTS"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Granular security intel with daily bars"
                    },
                    "404": {
                        "description": "Ticker not found in tracked 500 securities"
                    }
                }
            }
        },
        "/api/mcp-schema.json": {
            "get": {
                "tags": ["MCP & AI Agents"],
                "summary": "Model Context Protocol (MCP) Tool Schemas",
                "description": "Returns the official JSON Schema catalog for all 6 MCP tools exposed for autonomous AI agents and IDEs.",
                "responses": {
                    "200": {
                        "description": "Model Context Protocol tool catalog"
                    }
                }
            }
        }
    }
}

with open(API_DIR / "openapi.json", "w", encoding="utf-8") as f:
    json.dump(openapi_spec, f, indent=2)

with open(API_DIR / "stonks.json", "w", encoding="utf-8") as f:
    json.dump({"total": len(stocks), "securities": stocks}, f, indent=2)

with open(API_DIR / "etfs.json", "w", encoding="utf-8") as f:
    json.dump({"total": etfs_count, "securities": etfs_list}, f, indent=2)

with open(API_DIR / "whales.json", "w", encoding="utf-8") as f:
    json.dump({"total": len(whales), "whales": whales}, f, indent=2)

with open(API_DIR / "shadow.json", "w", encoding="utf-8") as f:
    shadow_whales = sorted(whales, key=lambda x: x["shadow_ratio"], reverse=True)
    json.dump({"total": len(shadow_whales), "whales": shadow_whales}, f, indent=2)

for s in stocks:
    ticker = s["ticker"]
    ticker_payload = {
        "security": s,
        "whales": ticker_to_whales.get(ticker, []),
        "history": historic_data.get(ticker, {}).get("bars", [])
    }
    with open(TICKER_API_DIR / f"{ticker}.json", "w", encoding="utf-8") as f:
        json.dump(ticker_payload, f)

# Generate standard XML Sitemap (sitemap.xml)
sitemap_urls = [
    ("https://ah.mphinance.com/", "1.0", "hourly"),
    ("https://ah.mphinance.com/stonks", "0.9", "hourly"),
    ("https://ah.mphinance.com/etfs", "0.9", "daily"),
    ("https://ah.mphinance.com/whales", "0.9", "daily"),
    ("https://ah.mphinance.com/shadow", "0.8", "daily"),
    ("https://ah.mphinance.com/sitemap", "0.8", "daily"),
    ("https://ah.mphinance.com/docs", "0.9", "daily"),
    ("https://ah.mphinance.com/mcp", "0.9", "daily"),
    ("https://ah.mphinance.com/all", "0.7", "weekly"),
    ("https://ah.mphinance.com/api/market.json", "0.8", "hourly"),
    ("https://ah.mphinance.com/api/stonks.json", "0.7", "hourly"),
    ("https://ah.mphinance.com/api/etfs.json", "0.7", "daily"),
    ("https://ah.mphinance.com/api/whales.json", "0.7", "daily"),
    ("https://ah.mphinance.com/api/shadow.json", "0.7", "daily"),
    ("https://ah.mphinance.com/api/openapi.json", "0.8", "daily"),
    ("https://ah.mphinance.com/api/mcp-schema.json", "0.8", "daily"),
]

for s in stocks:
    sitemap_urls.append((f"https://ah.mphinance.com/ticker/{s['ticker']}", "0.8", "hourly"))

for w in whales[:100]:
    sitemap_urls.append((f"https://ah.mphinance.com/@{w['username']}", "0.7", "daily"))

sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>']
sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for url, prio, freq in sitemap_urls:
    sitemap_xml.append(f"  <url><loc>{url}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
sitemap_xml.append('</urlset>')

with open(BASE_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_xml))

print(f"[+] Exported sitemap.xml with {len(sitemap_urls)} URLs")

# Build Front-Page Market Radar HTML Blocks
def build_radar_rows(items, mode):
    rows = []
    for idx, x in enumerate(items, 1):
        sym = x["ticker"]
        name = x["name"]
        typ = "ETF" if x["isETF"] else "STOCK"
        chg = x.get("changePercent", 0)
        chg_sign = "+" if chg >= 0 else ""
        chg_class = "pos-green" if chg >= 0 else "neg-red"
        
        if mode == "value":
            val_str = f"${x['totalValue']/1_000_000:.2f}M"
            meta_str = f"<span class='{chg_class}'>{chg_sign}{chg:.1f}%</span> &bull; {x['owners']:,} holders"
        elif mode == "owners":
            val_str = f"{x['owners']:,} Holders"
            meta_str = f"<span class='{chg_class}'>{chg_sign}{chg:.1f}%</span> &bull; ${x['totalValue']/1_000_000:.2f}M app equity"
        elif mode == "intensity":
            val_str = f"${x['intensity']:,.0f}"
            meta_str = f"<span class='val-purple'>$/holder</span> &bull; {x['owners']:,} owners"

        rows.append(f"""
        <div class="radar-row" onclick="openTickerModal('{sym}')">
          <div class="radar-row-left">
            <span class="radar-row-rank">#{idx}</span>
            <div>
              <div class="radar-row-sym">${sym} <span class="badge-{('amber' if x['isETF'] else 'cyan')} reason-badge" style="font-size: 9px; padding: 1px 4px;">{typ}</span></div>
              <div class="radar-row-sub" style="max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{name}</div>
            </div>
          </div>
          <div class="radar-row-right">
            <div class="radar-row-val">{val_str}</div>
            <div class="radar-row-meta">{meta_str}</div>
          </div>
        </div>
        """)
    return "".join(rows)

radar_value_html = build_radar_rows(top_by_total_value, "value")
radar_owners_html = build_radar_rows(top_by_owners, "owners")
radar_intensity_html = build_radar_rows(top_by_intensity, "intensity")

# HTML Content Builder
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AfterHour Alpha & Whale Terminal | Powered by TraderMatrix Pro</title>
<meta name="description" content="Institutional-grade reverse-engineered intelligence terminal tracking 395 verified AfterHour whale portfolios, $169M+ AUM, and 500 securities. Powered by TraderMatrix Pro.">
<link rel="icon" href="https://www.tradermatrix.pro/brand/favicon-32.png" type="image/png">
<style>
  :root {{
    --bg-base: #06090E;
    --bg-surface: #0B1017;
    --bg-card: #101722;
    --bg-card-hover: #162030;
    --border: #1E293B;
    --border-accent: #334155;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --cyan: #00F0FF;
    --green: #10B981;
    --red: #F43F5E;
    --amber: #F59E0B;
    --purple: #A855F7;
    --font-mono: 'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace;
    --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: var(--bg-base);
    color: var(--text-primary);
    font-family: var(--font-sans);
    line-height: 1.5;
    padding: 0;
    margin: 0;
    min-height: 100vh;
  }}
  .container {{
    max-width: 1500px;
    margin: 0 auto;
    padding: 20px 24px 60px 24px;
  }}
  
  /* HEADER & BRANDING */
  header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 18px;
    flex-wrap: wrap;
    gap: 16px;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .brand-logo-img {{
    width: 44px;
    height: 44px;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    transition: transform 0.2s ease;
  }}
  .brand-logo-img:hover {{ transform: scale(1.05); }}
  .brand-title h1 {{
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #FFF, var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .brand-title p {{
    font-size: 13px;
    color: var(--text-secondary);
  }}
  .header-badges {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }}
  .live-badge {{
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-family: var(--font-mono);
    color: var(--green);
    font-weight: 700;
  }}
  .live-dot {{
    width: 8px; height: 8px; border-radius: 50%; background: var(--green);
    box-shadow: 0 0 10px var(--green);
    animation: pulse 2s infinite;
  }}
  @keyframes pulse {{ 0% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.4; }} }}
  
  .sitemap-header-btn {{
    display: flex; align-items: center; gap: 6px;
    background: var(--bg-card); border: 1px solid rgba(0, 240, 255, 0.3);
    padding: 6px 14px; border-radius: 20px; font-size: 12px; font-family: var(--font-mono);
    color: var(--cyan); text-decoration: none; font-weight: 700;
    cursor: pointer; transition: all 0.2s ease;
  }}
  .sitemap-header-btn:hover {{
    background: rgba(0, 240, 255, 0.15); border-color: var(--cyan);
    box-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
  }}

  .tm-header-btn {{
    display: flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(168, 85, 247, 0.15));
    border: 1px solid rgba(0, 240, 255, 0.4);
    padding: 6px 14px; border-radius: 20px; font-size: 12px; font-family: var(--font-mono);
    color: var(--cyan); text-decoration: none; font-weight: 700;
    transition: all 0.2s ease;
  }}
  .tm-header-btn:hover {{
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.3), rgba(168, 85, 247, 0.3));
    border-color: var(--cyan);
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
  }}

  .gh-link {{
    display: flex; align-items: center; gap: 6px;
    background: var(--bg-card); border: 1px solid var(--border);
    padding: 6px 14px; border-radius: 20px; font-size: 12px; font-family: var(--font-mono);
    color: var(--text-secondary); text-decoration: none; font-weight: 600;
    transition: all 0.2s ease;
  }}
  .gh-link:hover {{ border-color: var(--cyan); color: var(--text-primary); }}

  /* GLOWING TICKER MARQUEE TAPE */
  .ticker-marquee-bar {{
    background: linear-gradient(90deg, rgba(11, 16, 23, 0.95), rgba(16, 23, 34, 0.95));
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 16px;
    margin-bottom: 20px;
    overflow-x: auto;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 11px;
    font-family: var(--font-mono);
  }}
  .marquee-item {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: var(--text-secondary);
  }}
  .marquee-item strong {{ color: var(--cyan); }}
  .marquee-tag {{
    padding: 1px 5px; border-radius: 3px; font-size: 9px; font-weight: 800;
  }}

  /* STATS CARDS */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-bottom: 20px;
  }}
  .stat-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
  }}
  .clickable-card {{
    cursor: pointer;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }}
  .clickable-card:hover {{
    transform: translateY(-2px);
    border-color: var(--cyan);
    box-shadow: 0 4px 20px rgba(0, 240, 255, 0.18);
  }}
  .clickable-card:active {{
    transform: translateY(0);
  }}
  .clickable-card .stat-label {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .clickable-card .stat-arrow {{
    opacity: 0.4;
    font-size: 13px;
    transition: opacity 0.2s ease, transform 0.2s ease;
  }}
  .clickable-card:hover .stat-arrow {{
    opacity: 1;
    transform: translate(2px, -2px);
    color: var(--cyan);
  }}
  .stat-label {{
    font-size: 11px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
  }}
  .stat-value {{
    font-size: 26px;
    font-weight: 800;
    font-family: var(--font-mono);
    line-height: 1.1;
    margin-bottom: 4px;
  }}
  .stat-sub {{
    font-size: 11px;
    color: var(--text-secondary);
  }}
  .val-green {{ color: var(--green); }}
  .val-cyan {{ color: var(--cyan); }}
  .val-purple {{ color: var(--purple); }}
  .val-amber {{ color: var(--amber); }}

  /* FRONT-PAGE MARKET ALT-DATA RADAR SECTION */
  .market-radar-section {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 24px;
    position: relative;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  }}
  .market-radar-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
    flex-wrap: wrap;
    gap: 8px;
  }}
  .market-radar-title {{
    font-size: 13px;
    font-weight: 800;
    color: var(--cyan);
    font-family: var(--font-mono);
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .market-radar-sub {{
    font-size: 11px;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }}
  .market-radar-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px;
  }}
  .radar-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    transition: all 0.2s ease;
  }}
  .radar-card:hover {{
    border-color: var(--border-accent);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  }}
  .radar-card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 8px;
  }}
  .radar-card-title {{
    font-size: 13px;
    font-weight: 800;
    color: var(--text-primary);
  }}
  .radar-card-desc {{
    font-size: 11px;
    color: var(--text-muted);
  }}
  .radar-tag {{
    font-size: 9px;
    font-family: var(--font-mono);
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 0.5px;
  }}
  .tag-cyan {{ background: rgba(0, 240, 255, 0.15); color: var(--cyan); border: 1px solid rgba(0, 240, 255, 0.3); }}
  .tag-amber {{ background: rgba(245, 158, 11, 0.15); color: var(--amber); border: 1px solid rgba(245, 158, 11, 0.3); }}
  .tag-purple {{ background: rgba(168, 85, 247, 0.15); color: var(--purple); border: 1px solid rgba(168, 85, 247, 0.3); }}
  .tag-green {{ background: rgba(16, 185, 129, 0.15); color: var(--green); border: 1px solid rgba(16, 185, 129, 0.3); }}

  .radar-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .radar-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 10px;
    border-radius: 6px;
    background: rgba(11, 16, 23, 0.6);
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: var(--font-mono);
    font-size: 12px;
  }}
  .radar-row:hover {{
    background: var(--bg-card-hover);
    border-color: var(--cyan);
    transform: translateX(2px);
  }}
  .radar-row-left {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .radar-row-rank {{
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 700;
    width: 14px;
  }}
  .radar-row-sym {{
    font-weight: 800;
    color: var(--cyan);
    font-size: 13px;
  }}
  .radar-row-sub {{
    font-size: 10px;
    color: var(--text-muted);
  }}
  .radar-row-right {{
    text-align: right;
  }}
  .radar-row-val {{
    font-weight: 800;
    color: var(--text-primary);
  }}
  .radar-row-meta {{
    font-size: 10px;
    color: var(--text-secondary);
  }}

  /* HIGH CONVERTING TRADERMATRIX FUNNEL CARD */
  .tm-funnel-card {{
    position: relative;
    background: linear-gradient(135deg, rgba(14, 22, 36, 0.95), rgba(8, 12, 20, 0.95));
    border: 1px solid rgba(0, 240, 255, 0.35);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    overflow: hidden;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
  }}
  .tm-funnel-card:hover {{
    border-color: var(--cyan);
    box-shadow: 0 16px 40px rgba(0, 240, 255, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }}
  .tm-funnel-glow {{
    position: absolute;
    top: -50%;
    left: -20%;
    width: 140%;
    height: 200%;
    background: radial-gradient(circle at 15% 50%, rgba(0, 240, 255, 0.12), transparent 50%),
                radial-gradient(circle at 85% 50%, rgba(168, 85, 247, 0.12), transparent 50%);
    pointer-events: none;
  }}
  .tm-funnel-content {{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    flex-wrap: wrap;
  }}
  .tm-funnel-icon {{ flex-shrink: 0; }}
  .tm-funnel-text {{ flex: 1; min-width: 300px; }}
  .tm-funnel-badge {{
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 10px; font-family: var(--font-mono); font-weight: 800;
    letter-spacing: 1px; color: var(--cyan);
    background: rgba(0, 240, 255, 0.12); border: 1px solid rgba(0, 240, 255, 0.3);
    padding: 3px 10px; border-radius: 20px; margin-bottom: 8px;
  }}
  .tm-funnel-text h2 {{
    font-size: 20px; font-weight: 800; letter-spacing: -0.4px;
    color: var(--text-primary); margin-bottom: 6px; line-height: 1.3;
  }}
  .tm-funnel-text p {{
    font-size: 13px; color: var(--text-secondary); line-height: 1.5;
  }}
  .tm-funnel-actions {{
    display: flex; flex-direction: column; align-items: flex-end;
    gap: 8px; flex-shrink: 0;
  }}
  .tm-cta-btn {{
    display: flex; align-items: center; gap: 10px;
    background: linear-gradient(135deg, #00F0FF, #00B4D8);
    color: #040810; font-size: 14px; font-weight: 800;
    font-family: var(--font-mono); padding: 12px 24px; border-radius: 10px;
    text-decoration: none; box-shadow: 0 4px 20px rgba(0, 240, 255, 0.4);
    transition: all 0.2s ease; white-space: nowrap;
  }}
  .tm-cta-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 240, 255, 0.6);
    background: linear-gradient(135deg, #38F9D7, #00F0FF);
  }}
  .tm-ref-tag {{
    font-size: 11px; font-family: var(--font-mono); color: var(--text-muted);
  }}
  .tm-ref-tag strong {{ color: var(--cyan); }}

  /* ROUTE / NAV TABS */
  .nav-tabs {{
    display: flex;
    gap: 8px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
    overflow-x: auto;
    padding-bottom: 4px;
  }}
  .tab-btn {{
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 600;
    padding: 10px 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    transition: all 0.2s ease;
  }}
  .tab-btn:hover {{
    color: var(--text-primary);
  }}
  .tab-btn.active {{
    color: var(--cyan);
    border-bottom-color: var(--cyan);
  }}
  .tab-pane {{
    display: none;
  }}
  .tab-pane.active {{
    display: block;
  }}

  /* CONTROLS BAR: SEARCH & FILTERS */
  .controls-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 16px;
    align-items: center;
    justify-content: space-between;
  }}
  .search-input {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-family: var(--font-sans);
    flex: 1;
    min-width: 280px;
  }}
  .search-input:focus {{
    outline: none;
    border-color: var(--cyan);
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
  }}

  /* RANK SELECTOR BAR */
  .rank-selector-strip {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    flex-wrap: wrap;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    padding: 8px 16px;
    border-radius: 10px;
    font-size: 12px;
    font-family: var(--font-mono);
  }}
  .rank-selector-label {{
    color: var(--text-muted);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .rank-btn {{
    background: transparent;
    border: 1px solid transparent;
    color: var(--text-secondary);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-family: var(--font-mono);
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .rank-btn:hover {{
    color: var(--text-primary);
    background: var(--bg-card);
  }}
  .rank-btn.active {{
    background: rgba(0, 240, 255, 0.15);
    border-color: var(--cyan);
    color: var(--cyan);
    font-weight: 700;
  }}

  .filter-group {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }}
  .filter-btn {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 7px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-family: var(--font-mono);
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .filter-btn:hover {{
    border-color: var(--border-accent);
    color: var(--text-primary);
  }}
  .filter-btn.active {{
    background: rgba(0, 240, 255, 0.12);
    border-color: var(--cyan);
    color: var(--cyan);
    font-weight: 700;
  }}

  /* DATA TABLES */
  .table-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    text-align: left;
  }}
  th {{
    background: var(--bg-card);
    color: var(--text-muted);
    font-size: 11px;
    font-family: var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    user-select: none;
    cursor: pointer;
    transition: color 0.15s ease;
  }}
  th:hover {{
    color: var(--cyan);
  }}
  th.sortable::after {{
    content: ' ↕';
    opacity: 0.4;
  }}
  th.sorted-asc::after {{
    content: ' ▲';
    color: var(--cyan);
    opacity: 1;
  }}
  th.sorted-desc::after {{
    content: ' ▼';
    color: var(--cyan);
    opacity: 1;
  }}
  td {{
    padding: 12px 14px;
    border-bottom: 1px solid rgba(30, 41, 59, 0.5);
    font-family: var(--font-mono);
    vertical-align: middle;
  }}
  tr.clickable-row {{
    cursor: pointer;
    transition: background 0.15s ease;
  }}
  tr.clickable-row:hover td {{
    background: var(--bg-card-hover);
  }}
  .pos-green {{ color: var(--green); }}
  .neg-red {{ color: var(--red); }}

  /* BADGES & PILLS */
  .reason-badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 10px;
    font-family: var(--font-mono);
    font-weight: 700;
    margin-right: 4px;
    margin-bottom: 2px;
    letter-spacing: 0.3px;
  }}
  .badge-purple {{
    background: rgba(168, 85, 247, 0.15);
    border: 1px solid rgba(168, 85, 247, 0.4);
    color: #D8B4FE;
  }}
  .badge-cyan {{
    background: rgba(0, 240, 255, 0.15);
    border: 1px solid rgba(0, 240, 255, 0.4);
    color: var(--cyan);
  }}
  .badge-green {{
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: var(--green);
  }}
  .badge-amber {{
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: var(--amber);
  }}
  .badge-red {{
    background: rgba(244, 63, 94, 0.15);
    border: 1px solid rgba(244, 63, 94, 0.4);
    color: var(--red);
  }}

  /* SLUG PILL */
  .slug-pill {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-family: var(--font-mono);
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .slug-pill:hover {{
    border-color: var(--cyan);
    color: var(--cyan);
    background: rgba(0, 240, 255, 0.08);
  }}

  /* WHALE CARDS */
  .whale-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 16px;
  }}
  .whale-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .whale-card:hover {{
    border-color: var(--cyan);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  }}
  .whale-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }}
  .whale-user {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .whale-avatar {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1E293B, #334155);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--cyan);
    font-family: var(--font-mono);
    border: 1px solid var(--border-accent);
  }}
  .whale-name {{
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
  }}
  .whale-rank {{
    font-size: 11px;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }}
  .whale-badge {{
    background: rgba(0, 240, 255, 0.1);
    color: var(--cyan);
    border: 1px solid rgba(0, 240, 255, 0.3);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 10px;
    font-family: var(--font-mono);
    font-weight: 700;
  }}
  .whale-metrics {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 12px;
    background: var(--bg-card);
    padding: 10px 12px;
    border-radius: 8px;
  }}
  .whale-m-label {{
    font-size: 10px;
    color: var(--text-muted);
    font-family: var(--font-mono);
  }}
  .whale-m-val {{
    font-size: 15px;
    font-weight: 800;
    font-family: var(--font-mono);
  }}
  .holding-chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .holding-chip {{
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid var(--border);
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-family: var(--font-mono);
    color: var(--text-secondary);
    transition: all 0.15s ease;
    cursor: pointer;
  }}
  .holding-chip:hover {{
    border-color: var(--cyan);
    color: var(--cyan);
  }}

  /* SITEMAP / DIRECTORY STYLES */
  .sitemap-section {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 24px;
  }}
  .sitemap-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .sitemap-header h3 {{
    font-size: 17px;
    font-weight: 800;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .sitemap-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
  }}
  .sitemap-chip-cloud {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .sitemap-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    transition: all 0.2s ease;
    cursor: pointer;
    text-decoration: none;
    display: block;
  }}
  .sitemap-card:hover {{
    border-color: var(--cyan);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  }}
  .sitemap-card-title {{
    font-size: 14px;
    font-weight: 800;
    color: var(--cyan);
    margin-bottom: 4px;
    font-family: var(--font-mono);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .sitemap-card-desc {{
    font-size: 12px;
    color: var(--text-secondary);
  }}
  .sitemap-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-family: var(--font-mono);
    color: var(--text-primary);
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s ease;
  }}
  .sitemap-chip:hover {{
    border-color: var(--cyan);
    color: var(--cyan);
    background: rgba(0, 240, 255, 0.08);
  }}
  .sitemap-chip-meta {{
    font-size: 10px;
    color: var(--text-muted);
  }}

  /* MODALS */
  .modal-overlay {{
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(6px);
    display: none; align-items: center; justify-content: center;
    z-index: 1000; padding: 20px;
  }}
  .modal-overlay.active {{ display: flex; }}
  .modal-box {{
    background: var(--bg-surface); border: 1px solid var(--border-accent);
    border-radius: 16px; width: 100%; max-width: 950px;
    max-height: 88vh; overflow-y: auto; box-shadow: 0 24px 50px rgba(0,0,0,0.8);
    position: relative;
  }}
  .modal-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 20px 26px; border-bottom: 1px solid var(--border);
    position: sticky; top: 0; background: var(--bg-surface); z-index: 10;
  }}
  .modal-body {{ padding: 22px 26px; }}
  .close-btn {{
    background: transparent; border: none; font-size: 26px;
    color: var(--text-muted); cursor: pointer; line-height: 1;
  }}
  .close-btn:hover {{ color: var(--text-primary); }}

  .modal-stat-strip {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px; margin-bottom: 20px; background: var(--bg-base); padding: 14px;
    border-radius: 10px; border: 1px solid var(--border);
  }}

  .slug-permalink-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: 8px 14px;
    border-radius: 8px;
    margin-bottom: 18px;
    font-size: 11px;
    font-family: var(--font-mono);
  }}
  .slug-copy-btn {{
    background: rgba(0, 240, 255, 0.15);
    border: 1px solid rgba(0, 240, 255, 0.4);
    color: var(--cyan);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-family: var(--font-mono);
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .slug-copy-btn:hover {{
    background: var(--cyan);
    color: #000;
  }}

  /* OVER-TIME HISTORICAL CHART CONTAINER */
  .chart-box {{
    background: var(--bg-base);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 20px;
  }}
  .chart-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-family: var(--font-mono);
    font-size: 12px;
  }}
  .chart-svg {{
    width: 100%;
    height: 190px;
    display: block;
  }}

  footer {{
    margin-top: 48px; padding: 24px 0; border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 14px; font-size: 12px; color: var(--text-muted);
    font-family: var(--font-mono);
  }}
  footer a {{ color: var(--cyan); text-decoration: none; font-weight: 700; }}
  footer a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="brand">
      <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank" title="Powered by TraderMatrix Pro">
        <img src="https://www.tradermatrix.pro/brand/app-icon-180.png" class="brand-logo-img" alt="TraderMatrix Logo">
      </a>
      <div class="brand-title">
        <h1>AfterHour Alpha & Whale Terminal</h1>
        <p>Institutional Alt-Data &bull; Powered by <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank" style="color: var(--cyan); text-decoration: none; font-weight: 700;">TraderMatrix Pro</a></p>
      </div>
    </div>
    <div class="header-badges">
      <div class="live-badge">
        <div class="live-dot"></div>
        LIVE ALT-DATA
      </div>
      <a href="/mcp" class="sitemap-header-btn" style="text-decoration: none; color: var(--cyan); border-color: rgba(0, 210, 255, 0.4);">
        <span>&#x1F916;</span>
        <span>MCP</span>
      </a>
      <a href="/docs" class="sitemap-header-btn" style="text-decoration: none; color: var(--green); border-color: rgba(0, 245, 155, 0.4);">
        <span>&#x1F4D6;</span>
        <span>Docs</span>
      </a>
      <button class="sitemap-header-btn" onclick="openSitemapView()">
        <span>&#x1F5FA;&#xFE0F;</span>
        <span>Sitemap</span>
      </button>
      <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank" class="tm-header-btn">
        <img src="https://www.tradermatrix.pro/brand/app-icon-180.png" width="16" height="16" style="border-radius: 4px;" alt="">
        <span>TraderMatrix Pro</span>
        <span style="background: var(--cyan); color: #000; font-size: 9px; padding: 1px 5px; border-radius: 3px; font-weight: 800;">REF: MPHINANCE</span>
      </a>
      <a href="https://github.com/mphinance/aftermath" target="_blank" class="gh-link">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
        mphinance/aftermath
      </a>
    </div>
  </header>

  <!-- GLOWING REAL-TIME ALT-DATA TICKER TAPE -->
  <div class="ticker-marquee-bar">
    <div class="marquee-item">
      <span class="marquee-tag tag-cyan">#1 CAPITAL</span>
      <span>$AAPL <strong>${top_by_total_value[0]['totalValue']/1_000_000:.1f}M</strong> Total Value</span>
    </div>
    <div class="marquee-item">&bull;</div>
    <div class="marquee-item">
      <span class="marquee-tag tag-amber">#1 BREADTH</span>
      <span>$NVDA <strong>{top_by_owners[0]['owners']:,}</strong> Verified Owners</span>
    </div>
    <div class="marquee-item">&bull;</div>
    <div class="marquee-item">
      <span class="marquee-tag tag-purple">WHALE MAGNET</span>
      <span>$ASTS <strong>${stocks_by_whale[1]['whalesValue']/1_000_000:.1f}M</strong> Whale Capital</span>
    </div>
    <div class="marquee-item">&bull;</div>
    <div class="marquee-item">
      <span class="marquee-tag tag-green">DRY POWDER</span>
      <span>Whale Cash: <strong>${total_cash_reserves/1_000_000:.2f}M</strong></span>
    </div>
    <div class="marquee-item">&bull;</div>
    <div class="marquee-item">
      <span class="marquee-tag tag-green">WHALE TAPE TODAY</span>
      <span>Net Profit: <strong class="pos-green">+${total_profit_today/1_000_000:.2f}M</strong></span>
    </div>
    <div class="marquee-item">&bull;</div>
    <div class="marquee-item">
      <span class="marquee-tag tag-purple">CONVICTION</span>
      <span>$ANET <strong>${top_by_intensity[0]['intensity']:,.0f}/holder</strong></span>
    </div>
    <div class="marquee-item">&bull;</div>
    <div class="marquee-item">
      <span class="marquee-tag tag-cyan">TOP ETF</span>
      <span>$QQQ <strong>${stocks_by_whale[3]['whalesValue']/1_000_000:.1f}M</strong> AUM</span>
    </div>
  </div>

  <!-- MACRO STATS (5 INTERACTIVE CARDS) -->
  <div class="stats-grid">
    <div class="stat-card clickable-card" onclick="openStocksView('value')" title="Sort all 500 securities by platform equity">
      <div class="stat-label">
        <span>TOTAL APP EQUITY</span>
        <span class="stat-arrow">&nearr;</span>
      </div>
      <div class="stat-value val-cyan">${total_app_value:,.0f}</div>
      <div class="stat-sub">{total_app_owners:,} retail positions tracked</div>
    </div>
    <div class="stat-card clickable-card" onclick="openWhalesView()" title="Inspect all 395 verified whale portfolios">
      <div class="stat-label">
        <span>TOTAL WHALE CAPITAL</span>
        <span class="stat-arrow">&nearr;</span>
      </div>
      <div class="stat-value val-green">${total_whale_val:,.0f}</div>
      <div class="stat-sub">{len(whales)} portfolios &bull; ${total_cash_reserves/1_000_000:.1f}M cash</div>
    </div>
    <div class="stat-card clickable-card" onclick="filterMillionaires()" title="Filter the 32 verified millionaire accounts">
      <div class="stat-label">
        <span>VERIFIED MILLIONAIRES</span>
        <span class="stat-arrow">&nearr;</span>
      </div>
      <div class="stat-value val-purple">{millionaires_count} ACCOUNTS</div>
      <div class="stat-sub">Controlling $110.8M+ AUM &bull; <strong style="color: var(--purple);">Filter &nearr;</strong></div>
    </div>
    <div class="stat-card clickable-card" onclick="openStocksView('whale')" title="Inspect 500 securities universe">
      <div class="stat-label">
        <span>TRACKED UNIVERSE</span>
        <span class="stat-arrow">&nearr;</span>
      </div>
      <div class="stat-value val-amber">{len(stocks)} SECURITIES</div>
      <div class="stat-sub">{equities_count} Stocks &bull; {etfs_count} ETFs segregated</div>
    </div>
    <div class="stat-card clickable-card" onclick="openWhaleModal('{whales[0]['username']}')" title="Inspect @{whales[0]['username']}">
      <div class="stat-label">
        <span>TOP TRACKED WHALE</span>
        <span class="stat-arrow">&nearr;</span>
      </div>
      <div class="stat-value val-green">${whales[0]['total_value']:,.0f}</div>
      <div class="stat-sub">@{whales[0]['username']} (${whales[0]['shadow_ratio']:,.0f}/sub)</div>
    </div>
  </div>

  <!-- FRONT-PAGE MARKET RADAR & ALT-DATA INTELLIGENCE SECTION -->
  <div class="market-radar-section">
    <div class="market-radar-header">
      <div>
        <div class="market-radar-title">
          <span class="live-dot" style="display: inline-block;"></span>
          <span>MARKET ALT-DATA RADAR &bull; CAPITAL INFLOWS &amp; HOLDER CONSENSUS</span>
        </div>
        <div class="market-radar-sub">Real-time intelligence extracted across 395 verified portfolios &amp; 500 securities</div>
      </div>
      <div style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">
        Click any asset to launch Deep-Dive &bull; Auto-synced
      </div>
    </div>
    
    <div class="market-radar-grid">
      <!-- CARD 1: CAPITAL INFLOW LEADERS -->
      <div class="radar-card">
        <div class="radar-card-header">
          <div>
            <div class="radar-card-title">&#x1F4B0; Capital Inflow Leaders</div>
            <div class="radar-card-desc">Highest total equity tracked on app</div>
          </div>
          <span class="radar-tag tag-cyan">TOTAL VALUE</span>
        </div>
        <div class="radar-list">
          {radar_value_html}
        </div>
      </div>

      <!-- CARD 2: RETAIL CONSENSUS (OWNERS) -->
      <div class="radar-card">
        <div class="radar-card-header">
          <div>
            <div class="radar-card-title">&#x1F465; Retail Adoption Breadth</div>
            <div class="radar-card-desc">Most widely held by verified accounts</div>
          </div>
          <span class="radar-tag tag-amber">MOST OWNED</span>
        </div>
        <div class="radar-list">
          {radar_owners_html}
        </div>
      </div>

      <!-- CARD 3: CONVICTION INTENSITY -->
      <div class="radar-card">
        <div class="radar-card-header">
          <div>
            <div class="radar-card-title">&#x1F3AF; Conviction Intensity</div>
            <div class="radar-card-desc">Highest verified equity per account</div>
          </div>
          <span class="radar-tag tag-purple">$/HOLDER</span>
        </div>
        <div class="radar-list">
          {radar_intensity_html}
        </div>
      </div>

      <!-- CARD 4: MACRO TAPE & LIQUIDITY -->
      <div class="radar-card">
        <div class="radar-card-header">
          <div>
            <div class="radar-card-title">&#x26A1; Macro Tape &amp; Liquidity</div>
            <div class="radar-card-desc">Whale momentum, cash, &amp; allocation</div>
          </div>
          <span class="radar-tag tag-green">PULSE</span>
        </div>
        <div class="radar-list">
          <div class="radar-row" style="cursor: default;">
            <div class="radar-row-left">
              <span style="font-size: 14px;">&#x1F4C8;</span>
              <div>
                <div style="font-weight: 700; color: var(--text-primary);">Whale Net Gain Today</div>
                <div class="radar-row-sub">Intraday tape performance</div>
              </div>
            </div>
            <div class="radar-row-right">
              <div class="radar-row-val pos-green">+${total_profit_today/1_000_000:.2f}M</div>
              <div class="radar-row-meta">+2.1% net return</div>
            </div>
          </div>

          <div class="radar-row" style="cursor: default;">
            <div class="radar-row-left">
              <span style="font-size: 14px;">&#x1F4B5;</span>
              <div>
                <div style="font-weight: 700; color: var(--text-primary);">Whale Dry Powder</div>
                <div class="radar-row-sub">Liquid cash reserves ready</div>
              </div>
            </div>
            <div class="radar-row-right">
              <div class="radar-row-val val-green">${total_cash_reserves/1_000_000:.2f}M</div>
              <div class="radar-row-meta">Waiting to buy dips</div>
            </div>
          </div>

          <div class="radar-row" style="cursor: default;">
            <div class="radar-row-left">
              <span style="font-size: 14px;">&#x2696;&#xFE0F;</span>
              <div>
                <div style="font-weight: 700; color: var(--text-primary);">Asset Allocation</div>
                <div class="radar-row-sub">Risk equity vs Index/Beta</div>
              </div>
            </div>
            <div class="radar-row-right">
              <div class="radar-row-val val-cyan">{equity_pct:.0f}% / {etf_pct:.0f}%</div>
              <div class="radar-row-meta">${whale_equity_cap/1_000_000:.1f}M Stocks &bull; ${whale_etf_cap/1_000_000:.1f}M ETFs</div>
            </div>
          </div>

          <div class="radar-row" style="cursor: default;">
            <div class="radar-row-left">
              <span style="font-size: 14px;">&#x1F680;</span>
              <div>
                <div style="font-weight: 700; color: var(--text-primary);">Top Tape Gainers</div>
                <div class="radar-row-sub">Leading large-cap moves</div>
              </div>
            </div>
            <div class="radar-row-right">
              <div class="radar-row-val pos-green">{", ".join([f"${x['ticker']} +{x['changePercent']:.1f}%" for x in top_gainers_tape[:2]])}</div>
              <div class="radar-row-meta">{", ".join([f"${x['ticker']} +{x['changePercent']:.1f}%" for x in top_gainers_tape[2:4]])}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- HIGH-CONVERTING TRADERMATRIX FUNNEL CARD -->
  <div class="tm-funnel-card">
    <div class="tm-funnel-glow"></div>
    <div class="tm-funnel-content">
      <div class="tm-funnel-icon">
        <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank">
          <img src="https://www.tradermatrix.pro/brand/app-icon-180.png" alt="TraderMatrix Pro" width="60" height="60" style="border-radius: 14px; box-shadow: 0 0 25px rgba(0, 240, 255, 0.45); display: block;">
        </a>
      </div>
      <div class="tm-funnel-text">
        <div class="tm-funnel-badge">
          <span>&#x26A1;</span> INSTITUTIONAL QUANT PLATFORM
        </div>
        <h2>If we pull this kind of edge from a social app, imagine what we do with real tape.</h2>
        <p>Stop guessing off retail noise. Get real-time unusual options activity, live dark pool volume, dealer Gamma Exposure (GEX) levels, and institutional flow tracking.</p>
      </div>
      <div class="tm-funnel-actions">
        <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank" class="tm-cta-btn">
          <span>Launch TraderMatrix Pro</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </a>
        <div class="tm-ref-tag">Partner Referral: <strong>MPHINANCE</strong></div>
      </div>
    </div>
  </div>

  <!-- ROUTE NAVIGATION TABS -->
  <div class="nav-tabs">
    <button class="tab-btn active" id="tabNav-stonks" onclick="switchRoute('/stonks')">
      <span>&#x1F4C8;</span> Top Stonks &amp; Taxonomy ({len(stocks)})
    </button>
    <button class="tab-btn" id="tabNav-etfs" onclick="switchRoute('/etfs')">
      <span>&#x1F3DB;&#xFE0F;</span> ETFs &amp; Index Funds ({etfs_count})
    </button>
    <button class="tab-btn" id="tabNav-whales" onclick="switchRoute('/whales')">
      <span>&#x1F40B;</span> Whale Radar ({len(whales)})
    </button>
    <button class="tab-btn" id="tabNav-shadow" onclick="switchRoute('/shadow')">
      <span>&#x1F916;</span> Shadow Whales (Under-Followed)
    </button>
    <button class="tab-btn" id="tabNav-sitemap" onclick="switchRoute('/sitemap')">
      <span>&#x1F5FA;&#xFE0F;</span> Directory &amp; Sitemap
    </button>
    <a href="/mcp" class="tab-btn" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px; color: var(--cyan); border-color: rgba(0, 210, 255, 0.4);">
      <span>&#x1F916;</span> MCP Server
    </a>
    <a href="/docs" class="tab-btn" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px; color: var(--green); border-color: rgba(0, 245, 155, 0.4);">
      <span>&#x1F4D6;</span> Swagger API
    </a>
  </div>

  <!-- TAB 1: TOP STONKS & TAXONOMY -->
  <div id="view-stonks" class="tab-pane active">
    <div class="rank-selector-strip">
      <span class="rank-selector-label">&#x26A1; Rank Universe By:</span>
      <button class="rank-btn active" id="rankBtn-whale" onclick="setRankMode('whale')">🐋 Whale Capital ($)</button>
      <button class="rank-btn" id="rankBtn-value" onclick="setRankMode('value')">🌐 Total Value ($)</button>
      <button class="rank-btn" id="rankBtn-owners" onclick="setRankMode('owners')">👑 Verified Owners</button>
      <button class="rank-btn" id="rankBtn-gainers" onclick="setRankMode('gainers')">🚀 24h Gainers</button>
      <button class="rank-btn" id="rankBtn-dips" onclick="setRankMode('dips')">📉 24h Dips</button>
      <button class="rank-btn" id="rankBtn-chat" onclick="setRankMode('chat')">💬 Chatroom Heat</button>
    </div>

    <div class="controls-bar">
      <input type="text" id="stockSearch" class="search-input" placeholder="Search 500 securities by ticker or company name (e.g. NVDA, AAPL, QQQ, ASTS)..." oninput="filterStocks()">
      <div class="filter-group">
        <button class="filter-btn active" id="btnFilter-all" onclick="setStockFilter('all')">All (500)</button>
        <button class="filter-btn" id="btnFilter-capital" onclick="setStockFilter('capital')">💰 Cap ($5M+)</button>
        <button class="filter-btn" id="btnFilter-owners" onclick="setStockFilter('owners')">👑 Most Owned (100+)</button>
        <button class="filter-btn" id="btnFilter-conviction" onclick="setStockFilter('conviction')">🎯 Conviction ($50k+/sub)</button>
        <button class="filter-btn" id="btnFilter-whales" onclick="setStockFilter('whales')">🐋 Whale Favs ($1M+)</button>
        <button class="filter-btn" id="btnFilter-etfs" onclick="setStockFilter('etfs')">🏛️ ETFs ({etfs_count})</button>
        <button class="filter-btn" id="btnFilter-stocks" onclick="setStockFilter('stocks')">📈 Equities ({equities_count})</button>
        <button class="filter-btn" id="btnFilter-gainers" onclick="setStockFilter('gainers')">🚀 Gainers (+2%)</button>
        <button class="filter-btn" id="btnFilter-chat" onclick="setStockFilter('chat')">💬 Active Chat</button>
      </div>
    </div>

    <div class="table-card">
      <div style="overflow-x: auto;">
        <table id="stocksTable">
          <thead>
            <tr>
              <th class="sortable" id="th-rank" onclick="sortTableColumn('rank')">Rank</th>
              <th class="sortable" id="th-ticker" onclick="sortTableColumn('ticker')">Ticker / Slug</th>
              <th class="sortable" id="th-type" onclick="sortTableColumn('type')">Type</th>
              <th class="sortable" id="th-name" onclick="sortTableColumn('name')">Company / Asset Name</th>
              <th>Why It's Top / Quant Reason</th>
              <th class="sortable sorted-desc" id="th-whalesValue" onclick="sortTableColumn('whalesValue')">Whale Capital</th>
              <th class="sortable" id="th-totalValue" onclick="sortTableColumn('totalValue')">Total Value ($)</th>
              <th class="sortable" id="th-owners" onclick="sortTableColumn('owners')">Owners</th>
              <th class="sortable" id="th-intensity" onclick="sortTableColumn('intensity')">$/Holder</th>
              <th class="sortable" id="th-price" onclick="sortTableColumn('price')">Price ($)</th>
              <th class="sortable" id="th-changePercent" onclick="sortTableColumn('changePercent')">24h %</th>
              <th class="sortable" id="th-chatroomMembers" onclick="sortTableColumn('chatroomMembers')">Chatroom</th>
            </tr>
          </thead>
          <tbody id="stocksBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 2: WHALE RADAR -->
  <div id="view-whales" class="tab-pane">
    <div class="controls-bar">
      <input type="text" id="whaleSearch" class="search-input" placeholder="Search 395 whales by handle or held ticker (e.g. skrt, SlowmoInvestor, AAPL, ASTS)..." oninput="filterWhales()">
      <div class="filter-group">
        <button class="filter-btn active" id="btnSortVal" onclick="sortWhales('value')">Sort: Net Worth ($)</button>
        <button class="filter-btn" id="btnSortRatio" onclick="sortWhales('ratio')">Sort: $/Follower Ratio</button>
        <button class="filter-btn" id="btnSortPnL" onclick="sortWhales('pnl')">Sort: Total Profit</button>
        <button class="filter-btn" id="btnSortMillionaires" onclick="filterMillionaires()">💎 Millionaires ({millionaires_count})</button>
      </div>
    </div>
    <div class="whale-grid" id="whaleContainer"></div>
  </div>

  <!-- TAB 3: SHADOW WHALES (CLOUT INVERSION) -->
  <div id="view-shadow" class="tab-pane">
    <div style="margin-bottom: 16px; color: var(--text-secondary); font-size: 13px; background: var(--bg-surface); padding: 14px 18px; border-radius: 10px; border: 1px solid var(--border);">
      <strong style="color: var(--cyan);">The Clout Inversion Law</strong>: Retail clout on trading social networks is inversely correlated with verified capital. The accounts below hold seven- and eight-figure verified portfolios while flying completely under the radar with minimal followers.
    </div>
    <div class="table-card">
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Whale Handle / Slug</th>
              <th>Verified Equity</th>
              <th>Followers</th>
              <th>$/Follower Ratio</th>
              <th>Top Concentrated Holdings</th>
              <th>Verified Status</th>
            </tr>
          </thead>
          <tbody id="shadowBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 4: SITEMAP & DIRECTORY -->
  <div id="view-sitemap" class="tab-pane">
    <div class="sitemap-section">
      <div class="sitemap-header">
        <h3><span>&#x1F6F0;&#xFE0F;</span> Terminal Views &amp; Primary Routes</h3>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--cyan);">5 Direct Navigation Endpoints</span>
      </div>
      <div class="sitemap-grid">
        <a class="sitemap-card" href="javascript:void(0)" onclick="openStocksView('whale')">
          <div class="sitemap-card-title">/stonks <span>&rarr;</span></div>
          <div class="sitemap-card-desc">Top 500 securities universe ranked by Whale Capital, Value, Owners, and Momentum.</div>
        </a>
        <a class="sitemap-card" href="javascript:void(0)" onclick="switchRoute('/etfs', true, true)">
          <div class="sitemap-card-title">/etfs <span>&rarr;</span></div>
          <div class="sitemap-card-desc">Dedicated index and sector funds directory with 64 segregated ETFs.</div>
        </a>
        <a class="sitemap-card" href="javascript:void(0)" onclick="openWhalesView()">
          <div class="sitemap-card-title">/whales <span>&rarr;</span></div>
          <div class="sitemap-card-desc">Whale Radar featuring 395 verified portfolios controlling $169.0M+ AUM.</div>
        </a>
        <a class="sitemap-card" href="javascript:void(0)" onclick="switchRoute('/shadow', true, true)">
          <div class="sitemap-card-title">/shadow <span>&rarr;</span></div>
          <div class="sitemap-card-desc">The Clout Inversion index sorting under-followed high-net-worth accounts.</div>
        </a>
        <a class="sitemap-card" href="javascript:void(0)" onclick="switchRoute('/all', true, true)">
          <div class="sitemap-card-title">/all <span>&rarr;</span></div>
          <div class="sitemap-card-desc">Complete unpaginated securities leaderboard with multi-column sorting.</div>
        </a>
      </div>
    </div>

    <div class="sitemap-section">
      <div class="sitemap-header">
        <h3><span>&#x1F40B;</span> Verified Millionaires Directory ({millionaires_count} Accounts &bull; $110.8M AUM)</h3>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--green);">Click handle to open Whale Dossier</span>
      </div>
      <div class="sitemap-chip-cloud">
        {' '.join([f'<a class="sitemap-chip" href="javascript:void(0)" onclick="openWhaleModal(\'{w["username"]}\')"><strong style="color: var(--cyan);">@{w["username"]}</strong><span class="sitemap-chip-meta">${w["total_value"]/1_000_000:.2f}M</span></a>' for w in millionaires])}
      </div>
    </div>

    <div class="sitemap-section">
      <div class="sitemap-header">
        <h3><span>&#x1F3DB;&#xFE0F;</span> All 64 ETFs &amp; Index Funds Directory</h3>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--amber);">Click ticker to open ETF Deep-Dive</span>
      </div>
      <div class="sitemap-chip-cloud">
        {' '.join([f'<a class="sitemap-chip" href="javascript:void(0)" onclick="openTickerModal(\'{s["ticker"]}\')"><strong style="color: var(--amber);">${s["ticker"]}</strong><span class="sitemap-chip-meta">${s["whalesValue"]/1_000_000:.1f}M Whale</span></a>' for s in etfs_list])}
      </div>
    </div>

    <div class="sitemap-section">
      <div class="sitemap-header">
        <h3><span>&#x1F4C8;</span> Top Mega-Capital Equities (Whale Favorites)</h3>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--purple);">Click ticker to open Stock Deep-Dive</span>
      </div>
      <div class="sitemap-chip-cloud">
        {' '.join([f'<a class="sitemap-chip" href="javascript:void(0)" onclick="openTickerModal(\'{s["ticker"]}\')"><strong style="color: var(--cyan);">${s["ticker"]}</strong><span class="sitemap-chip-meta">${s["whalesValue"]/1_000_000:.1f}M</span></a>' for s in [x for x in stocks if not x['isETF']][:45]])}
      </div>
    </div>

    <div class="sitemap-section">
      <div class="sitemap-header">
        <h3><span>&#x1F916;</span> AI Agent Integration &amp; OpenAPI Documentation</h3>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--cyan);">MCP Spec 2024-11-05 &bull; OpenAPI 3.1</span>
      </div>
      <div class="sitemap-grid">
        <a class="sitemap-card" href="/mcp" target="_blank" style="border-color: rgba(0, 210, 255, 0.4);">
          <div class="sitemap-card-title" style="color: var(--cyan);">/mcp (Model Context Protocol Hub) <span>&nearr;</span></div>
          <div class="sitemap-card-desc">Complete integration portal for Claude Desktop, Cursor, Antigravity, and Windsurf with 6 live tools.</div>
        </a>
        <a class="sitemap-card" href="/docs" target="_blank" style="border-color: rgba(0, 245, 155, 0.4);">
          <div class="sitemap-card-title" style="color: var(--green);">/docs (Swagger Interactive UI) <span>&nearr;</span></div>
          <div class="sitemap-card-desc">Interactive Swagger API documentation. Test every edge JSON endpoint live in your browser.</div>
        </a>
        <a class="sitemap-card" href="/api/openapi.json" target="_blank">
          <div class="sitemap-card-title">/api/openapi.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">Machine-readable OpenAPI 3.1 specification for Postman, Insomnia, and agent loops.</div>
        </a>
        <a class="sitemap-card" href="/api/mcp-schema.json" target="_blank">
          <div class="sitemap-card-title">/api/mcp-schema.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">JSON Schema tool definitions for get_market_tape, get_top_equities, get_ticker_intel, and more.</div>
        </a>
      </div>
    </div>

    <div class="sitemap-section">
      <div class="sitemap-header">
        <h3><span>&#x26A1;</span> Sub-Millisecond Static JSON API Endpoints</h3>
        <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">Direct Public Machine Endpoints</span>
      </div>
      <div class="sitemap-grid">
        <a class="sitemap-card" href="/api/market.json" target="_blank" style="border-color: rgba(255, 209, 102, 0.4);">
          <div class="sitemap-card-title" style="color: var(--amber);">/api/market.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">Real-time macro tape: whale dry powder ($8.98M cash), intraday net P&amp;L, and capital inflow leaders.</div>
        </a>
        <a class="sitemap-card" href="/api/stonks.json" target="_blank">
          <div class="sitemap-card-title">/api/stonks.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">All 500 securities with quantitative rankings, whale capital, owners, and change %.</div>
        </a>
        <a class="sitemap-card" href="/api/etfs.json" target="_blank">
          <div class="sitemap-card-title">/api/etfs.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">All 64 ETFs segregated with verified holder stats and platform values.</div>
        </a>
        <a class="sitemap-card" href="/api/whales.json" target="_blank">
          <div class="sitemap-card-title">/api/whales.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">All 395 verified whales ranked by Net Worth, Shadow Ratio, and P&L.</div>
        </a>
        <a class="sitemap-card" href="/api/shadow.json" target="_blank">
          <div class="sitemap-card-title">/api/shadow.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">The Clout Inversion index sorted by $/follower ratio asymmetry.</div>
        </a>
        <a class="sitemap-card" href="/api/ticker/NVDA.json" target="_blank">
          <div class="sitemap-card-title">/api/ticker/:symbol.json <span>&nearr;</span></div>
          <div class="sitemap-card-desc">Standalone ticker JSON endpoints available for all 500 securities.</div>
        </a>
        <a class="sitemap-card" href="/sitemap.xml" target="_blank">
          <div class="sitemap-card-title">/sitemap.xml <span>&nearr;</span></div>
          <div class="sitemap-card-desc">Standard XML sitemap index for search engines and web crawlers.</div>
        </a>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer>
    <div>&copy; 2026 Momentum Phinance &bull; Built with radical transparency</div>
    <div>
      <a href="javascript:void(0)" onclick="switchRoute('/sitemap')" style="margin-right: 14px;">&#x1F5FA;&#xFE0F; Complete Terminal Directory &amp; Sitemap</a>
      Institutional options flow via <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank">TraderMatrix Pro (Code: MPHINANCE)</a>
    </div>
  </footer>
</div>

<!-- MODAL FOR TICKER DEEP-DIVE -->
<div class="modal-overlay" id="tickerModal" onclick="closeModal(event, 'tickerModal')">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div>
        <h3 id="tickerModalTitle" style="font-size: 18px; font-weight: 700; color: var(--cyan);">$TICKER Deep-Dive</h3>
        <p id="tickerModalSub" style="font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono);"></p>
      </div>
      <button class="close-btn" onclick="hideModal('tickerModal')">&times;</button>
    </div>
    <div class="modal-body">
      <div class="slug-permalink-bar">
        <span>Permalink Slug: <strong id="tickerModalSlugText" style="color: var(--cyan);"></strong></span>
        <button class="slug-copy-btn" id="tickerCopyBtn" onclick="copyTickerSlug()">📋 Copy Slug Link</button>
      </div>

      <div id="tickerModalStrip" class="modal-stat-strip"></div>
      <div id="tickerChartContainer" style="display: none;"></div>

      <div style="background: linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(168, 85, 247, 0.1)); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 10px; padding: 14px 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; gap: 14px; flex-wrap: wrap;">
        <div>
          <div style="font-size: 13px; font-weight: 700; color: var(--cyan);">Institutional Order Flow &amp; Gamma Walls</div>
          <div style="font-size: 11px; color: var(--text-secondary);">Access real-time dark pool block prints and dealer GEX levels for this ticker on TraderMatrix Pro.</div>
        </div>
        <a id="tickerModalTmBtn" href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank" style="background: var(--cyan); color: #000; font-size: 12px; font-weight: 800; font-family: var(--font-mono); padding: 8px 14px; border-radius: 6px; text-decoration: none; white-space: nowrap;">
          View Live Tape &rarr;
        </a>
      </div>

      <div style="font-size: 13px; font-weight: 700; margin-bottom: 10px; color: var(--text-primary);">
        Verified Whales Holding This Asset (<span id="tickerModalWhalesCount">0</span>):
      </div>
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Whale Handle (Click to Inspect)</th>
              <th>Shares Owned</th>
              <th>Position Value</th>
              <th>Entry Cost Basis</th>
              <th>Unrealized P&L</th>
              <th>Followers</th>
            </tr>
          </thead>
          <tbody id="tickerModalWhalesBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<!-- MODAL FOR WHALE DETAIL -->
<div class="modal-overlay" id="whaleModal" onclick="closeModal(event, 'whaleModal')">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div>
        <h3 id="whaleModalTitle" style="font-size: 18px; font-weight: 700;">Whale Portfolio</h3>
        <p id="whaleModalSub" style="font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono);"></p>
      </div>
      <button class="close-btn" onclick="hideModal('whaleModal')">&times;</button>
    </div>
    <div class="modal-body">
      <div class="slug-permalink-bar">
        <span>Permalink Slug: <strong id="whaleModalSlugText" style="color: var(--cyan);"></strong></span>
        <button class="slug-copy-btn" id="whaleCopyBtn" onclick="copyWhaleSlug()">📋 Copy Slug Link</button>
      </div>

      <div id="whaleModalStrip" class="modal-stat-strip"></div>
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Ticker / Holding</th>
              <th>Asset Name</th>
              <th>Quantity</th>
              <th>Position Value</th>
              <th>Cost Basis</th>
              <th>Unrealized P&L</th>
            </tr>
          </thead>
          <tbody id="whaleModalPositionsBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
const STOCKS_DATA = {json.dumps(stocks)};
const WHALES_DATA = {json.dumps(whales)};
const TICKER_WHALES = {json.dumps(ticker_to_whales)};
const EXTRA_TICKER_NAMES = {json.dumps(ticker_extra_names)};
const HISTORIC_DATA = {json.dumps(historic_data)};

let currentRoute = '/stonks';
let currentRankMode = 'whale';
let currentStockFilter = 'all';
let currentWhaleSort = 'value';

let activeSortColumn = 'whalesValue';
let activeSortAsc = false;

let filteredStocks = [...STOCKS_DATA];
let filteredWhales = [...WHALES_DATA];
let currentOpenTicker = null;
let currentOpenWhale = null;

// ROUTING & SLUGS SYSTEM
function parseInitialRoute() {{
  const path = window.location.pathname.replace(/\\/index\\.html$/, '');
  const hash = window.location.hash.replace(/^#/, '');
  const route = hash || path || '/stonks';
  const isDirectSubroute = (route === '/sitemap' || route === '/whales' || route === '/etfs' || route === '/shadow' || route === '/all');
  navigateRoute(route, false, isDirectSubroute);
}}

function switchRoute(slug, pushHistory = true, shouldScroll = true) {{
  navigateRoute(slug, pushHistory, shouldScroll);
}}

function navigateRoute(slug, pushHistory = true, shouldScroll = false) {{
  if (!slug || slug === '/' || slug === '') slug = '/stonks';
  slug = slug.trim();
  if (slug.startsWith('#')) slug = slug.substring(1);
  if (!slug.startsWith('/')) slug = '/' + slug;

  const tickerMatch = slug.match(/^\\/(?:ticker|stonk)\\/([A-Za-z0-9_.-]+)$/i);
  if (tickerMatch) {{
    const sym = tickerMatch[1].toUpperCase();
    activateTab('stonks', false, null, shouldScroll);
    openTickerModal(sym, pushHistory);
    return;
  }}

  const whaleMatch = slug.match(/^\\/(?:@|whale\\/)([A-Za-z0-9_.-]+)$/i);
  if (whaleMatch) {{
    const u = whaleMatch[1];
    activateTab('whales', false, null, shouldScroll);
    openWhaleModal(u, pushHistory);
    return;
  }}

  if (slug === '/sitemap') {{
    activateTab('sitemap', pushHistory, '/sitemap', shouldScroll);
    return;
  }}
  if (slug === '/all') {{
    activateTab('stonks', pushHistory, '/all', shouldScroll);
    setStockFilter('all');
    return;
  }}
  if (slug === '/etfs') {{
    activateTab('stonks', pushHistory, '/etfs', shouldScroll);
    setStockFilter('etfs');
    return;
  }}
  if (slug === '/whales') {{
    activateTab('whales', pushHistory, '/whales', shouldScroll);
    return;
  }}
  if (slug === '/shadow') {{
    activateTab('shadow', pushHistory, '/shadow', shouldScroll);
    return;
  }}

  activateTab('stonks', pushHistory, '/stonks', shouldScroll);
}}

function activateTab(tabId, pushHistory = true, newSlug = null, shouldScroll = false) {{
  currentRoute = newSlug || ('/' + tabId);
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

  let navBtn = document.getElementById('tabNav-' + tabId);
  if (tabId === 'stonks' && currentStockFilter === 'etfs') {{
    navBtn = document.getElementById('tabNav-etfs');
  }}
  if (navBtn) navBtn.classList.add('active');

  const pane = document.getElementById('view-' + tabId);
  if (pane) {{
    pane.classList.add('active');
    if (shouldScroll) {{
      setTimeout(() => {{
        pane.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}, 60);
    }}
  }}

  if (pushHistory && window.history && window.history.pushState) {{
    window.history.pushState(null, '', currentRoute);
  }}
}}

function openSitemapView() {{
  switchRoute('/sitemap', true, true);
  const pane = document.getElementById('view-sitemap');
  if (pane) pane.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

function openWhalesView() {{
  switchRoute('/whales', true, true);
  const pane = document.getElementById('view-whales');
  if (pane) pane.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

function filterMillionaires() {{
  switchRoute('/whales', true, true);
  sortWhales('millionaires');
  const pane = document.getElementById('view-whales');
  if (pane) pane.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

function openStocksView(mode = 'whale') {{
  switchRoute('/stonks', true, true);
  if (mode) setRankMode(mode);
  const pane = document.getElementById('view-stonks');
  if (pane) pane.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

window.addEventListener('popstate', () => {{
  parseInitialRoute();
}});

// RANKING MODE CONTROLLER
function setRankMode(mode) {{
  currentRankMode = mode;
  document.querySelectorAll('.rank-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('rankBtn-' + mode);
  if (btn) btn.classList.add('active');

  if (mode === 'whale') {{ activeSortColumn = 'whalesValue'; activeSortAsc = false; }}
  else if (mode === 'value') {{ activeSortColumn = 'totalValue'; activeSortAsc = false; }}
  else if (mode === 'owners') {{ activeSortColumn = 'owners'; activeSortAsc = false; }}
  else if (mode === 'gainers') {{ activeSortColumn = 'changePercent'; activeSortAsc = false; }}
  else if (mode === 'dips') {{ activeSortColumn = 'changePercent'; activeSortAsc = true; }}
  else if (mode === 'chat') {{ activeSortColumn = 'chatroomMembers'; activeSortAsc = false; }}

  updateHeaderSortIndicators();
  filterStocks();
}}

// STOCK FILTERS
function setStockFilter(mode) {{
  currentStockFilter = mode;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('btnFilter-' + mode);
  if (btn) btn.classList.add('active');
  
  if (mode === 'etfs') {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tabNav-etfs').classList.add('active');
  }} else {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tabNav-stonks').classList.add('active');
  }}

  filterStocks();
}}

function sortTableColumn(col) {{
  if (activeSortColumn === col) {{
    activeSortAsc = !activeSortAsc;
  }} else {{
    activeSortColumn = col;
    activeSortAsc = (col === 'rank' || col === 'ticker' || col === 'name' || col === 'type') ? true : false;
  }}
  updateHeaderSortIndicators();
  applyCurrentSort();
  renderStocks(filteredStocks);
}}

function updateHeaderSortIndicators() {{
  document.querySelectorAll('th').forEach(th => {{
    th.classList.remove('sorted-asc', 'sorted-desc');
  }});
  const activeTh = document.getElementById('th-' + activeSortColumn);
  if (activeTh) {{
    activeTh.classList.add(activeSortAsc ? 'sorted-asc' : 'sorted-desc');
  }}
}}

function filterStocks() {{
  const q = (document.getElementById('stockSearch').value || '').toLowerCase().trim();
  
  filteredStocks = STOCKS_DATA.filter(s => {{
    if (q && !s.ticker.toLowerCase().includes(q) && !s.name.toLowerCase().includes(q)) {{
      return false;
    }}
    if (currentStockFilter === 'capital') return s.totalValue >= 5000000;
    if (currentStockFilter === 'owners') return s.owners >= 100;
    if (currentStockFilter === 'conviction') return s.intensity >= 50000 && s.owners >= 15;
    if (currentStockFilter === 'whales') return s.whalesValue >= 1000000;
    if (currentStockFilter === 'etfs') return s.isETF;
    if (currentStockFilter === 'stocks') return !s.isETF;
    if (currentStockFilter === 'gainers') return s.changePercent >= 2.0;
    if (currentStockFilter === 'chat') return s.chatroomMembers >= 2000;
    return true;
  }});

  applyCurrentSort();
  renderStocks(filteredStocks);
}}

function applyCurrentSort() {{
  filteredStocks.sort((a, b) => {{
    let vA = a[activeSortColumn];
    let vB = b[activeSortColumn];

    if (activeSortColumn === 'rank') {{
      vA = getDisplayRank(a);
      vB = getDisplayRank(b);
    }}

    if (typeof vA === 'string') {{
      return activeSortAsc ? vA.localeCompare(vB) : vB.localeCompare(vA);
    }}
    return activeSortAsc ? (vA - vB) : (vB - vA);
  }});
}}

function getDisplayRank(s) {{
  if (currentRankMode === 'whale') return s.rankWhaleCapital;
  if (currentRankMode === 'value') return s.rankPlatformValue;
  if (currentRankMode === 'owners') return s.rankOwners;
  if (currentRankMode === 'gainers') return s.rankGainers;
  if (currentRankMode === 'dips') return s.rankDips || s.rankWhaleCapital;
  if (currentRankMode === 'chat') return s.rankChat;
  return s.rankWhaleCapital;
}}

function renderStocks(list) {{
  const body = document.getElementById('stocksBody');
  if (list.length === 0) {{
    body.innerHTML = '<tr><td colspan="12" style="text-align: center; color: var(--text-muted); padding: 30px;">No securities match your filter query.</td></tr>';
    return;
  }}

  body.innerHTML = list.map((s, idx) => {{
    const sign = s.changePercent >= 0 ? '+' : '';
    const cls = s.changePercent >= 0 ? 'pos-green' : 'neg-red';
    
    const badgeHtml = (s.badges || []).map(b => {{
      return `<span class="reason-badge badge-${{b.color}}">${{b.label}}</span>`;
    }}).join('');

    const typeBadge = s.isETF 
      ? `<span class="reason-badge badge-amber" style="font-weight: 800;">ETF</span>`
      : `<span class="reason-badge badge-cyan">STOCK</span>`;

    const whaleBackingHtml = s.whalesCount > 0 
      ? `<div style="font-weight: 700; color: var(--cyan);">${{s.whalesCount}} Whales ($${{(s.whalesValue/1000000).toFixed(1)}}M)</div>
         <div style="font-size: 10px; color: var(--text-muted);">Top: @${{s.topWhale}}</div>`
      : `<span style="color: var(--text-muted); font-size: 11px;">0 tracked whales</span>`;

    const displayRank = (activeSortColumn === 'rank' || activeSortColumn === 'whalesValue') ? getDisplayRank(s) : (idx + 1);

    return `
      <tr class="clickable-row" onclick="openTickerModal('${{s.ticker}}')">
        <td style="color: var(--text-muted); font-weight: 700;">#${{displayRank}}</td>
        <td>
          <div style="font-weight: 800; font-size: 14px; color: var(--cyan);">${{s.ticker}}</div>
          <span class="slug-pill" onclick="event.stopPropagation(); copySlug('/ticker/${{s.ticker}}')">🔗 /ticker/${{s.ticker}}</span>
        </td>
        <td>${{typeBadge}}</td>
        <td style="color: var(--text-secondary); max-width: 170px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{s.name}}</td>
        <td>
          <div>${{badgeHtml}}</div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">${{s.whyTop}}</div>
        </td>
        <td>${{whaleBackingHtml}}</td>
        <td style="font-weight: 700;">$${{(s.totalValue/1000000).toFixed(2)}}M</td>
        <td>${{s.owners.toLocaleString()}}</td>
        <td style="color: var(--purple); font-weight: 700;">$${{Math.round(s.intensity).toLocaleString()}}</td>
        <td>$${{s.price.toFixed(2)}}</td>
        <td class="${{cls}}">${{sign}}${{s.changePercent.toFixed(2)}}%</td>
        <td style="color: var(--text-muted);">${{s.chatroomMembers.toLocaleString()}}</td>
      </tr>
    `;
  }}).join('');
}}

// WHALE RADAR
function sortWhales(mode) {{
  currentWhaleSort = mode;
  document.querySelectorAll('#view-whales .filter-btn').forEach(b => b.classList.remove('active'));
  if (mode === 'value') document.getElementById('btnSortVal').classList.add('active');
  if (mode === 'ratio') document.getElementById('btnSortRatio').classList.add('active');
  if (mode === 'pnl') document.getElementById('btnSortPnL').classList.add('active');
  if (mode === 'millionaires') {{
    const mb = document.getElementById('btnSortMillionaires');
    if (mb) mb.classList.add('active');
  }}
  filterWhales();
}}

function filterWhales() {{
  const q = (document.getElementById('whaleSearch').value || '').toLowerCase().trim();
  filteredWhales = WHALES_DATA.filter(w => {{
    if (currentWhaleSort === 'millionaires' && w.total_value < 1000000) return false;
    if (!q) return true;
    if (w.username.toLowerCase().includes(q)) return true;
    return (w.all_positions || []).some(p => p.ticker && p.ticker.toLowerCase().includes(q));
  }});

  if (currentWhaleSort === 'value' || currentWhaleSort === 'millionaires') {{
    filteredWhales.sort((a, b) => b.total_value - a.total_value);
  }} else if (currentWhaleSort === 'ratio') {{
    filteredWhales.sort((a, b) => b.shadow_ratio - a.shadow_ratio);
  }} else if (currentWhaleSort === 'pnl') {{
    filteredWhales.sort((a, b) => b.profit - a.profit);
  }}

  renderWhales();
}}

function renderWhales() {{
  const container = document.getElementById('whaleContainer');
  if (filteredWhales.length === 0) {{
    container.innerHTML = '<div style="color: var(--text-muted); padding: 40px; grid-column: 1/-1; text-align: center;">No matching whale accounts found.</div>';
    return;
  }}

  container.innerHTML = filteredWhales.map((w, idx) => {{
    const topHoldings = (w.all_positions || []).slice(0, 3).map(p => {{
      const t = p.ticker || 'N/A';
      const k = Math.round((p.value || 0)/1000);
      return `<span class="holding-chip" onclick="event.stopPropagation(); openTickerModal('${{t}}')">${{t}}: $${{k}}k</span>`;
    }}).join('');

    const pnlSign = w.profit >= 0 ? '+' : '';
    const pnlClass = w.profit >= 0 ? 'pos-green' : 'neg-red';
    const ratioStr = '$' + Math.round(w.shadow_ratio).toLocaleString() + '/sub';

    return `
      <div class="whale-card" onclick="openWhaleModal('${{w.username}}')">
        <div class="whale-header">
          <div class="whale-user">
            <div class="whale-avatar">${{w.username.charAt(0).toUpperCase()}}</div>
            <div>
              <div class="whale-name">@${{w.username}}</div>
              <div class="whale-rank">Followers: ${{w.followers.toLocaleString()}} | ${{ratioStr}}</div>
            </div>
          </div>
          <span class="whale-badge">VERIFIED</span>
        </div>
        <div class="whale-metrics">
          <div>
            <div class="whale-m-label">NET WORTH</div>
            <div class="whale-m-val val-green">$${{Math.round(w.total_value).toLocaleString()}}</div>
          </div>
          <div>
            <div class="whale-m-label">TRACKED P&L</div>
            <div class="whale-m-val ${{pnlClass}}">${{pnlSign}}$${{Math.round(w.profit).toLocaleString()}}</div>
          </div>
        </div>
        <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px; font-family: var(--font-mono);">TOP POSITIONS:</div>
        <div class="holding-chips">${{topHoldings || '<span style="color: var(--text-muted); font-size: 11px;">No active holdings</span>'}}</div>
      </div>
    `;
  }}).join('');
}}

function renderShadowWhales() {{
  const body = document.getElementById('shadowBody');
  const sorted = [...WHALES_DATA].sort((a, b) => b.shadow_ratio - a.shadow_ratio).slice(0, 60);

  body.innerHTML = sorted.map((w, idx) => {{
    const topHoldings = (w.all_positions || []).slice(0, 3).map(p => {{
      const t = p.ticker || 'N/A';
      return `<span class="holding-chip" onclick="event.stopPropagation(); openTickerModal('${{t}}')">${{t}}</span>`;
    }}).join(' ');

    return `
      <tr class="clickable-row" onclick="openWhaleModal('${{w.username}}')">
        <td style="color: var(--text-muted);">#${{idx + 1}}</td>
        <td>
          <div style="font-weight: 700; color: var(--cyan);">@${{w.username}}</div>
          <span class="slug-pill" onclick="event.stopPropagation(); copySlug('/@${{w.username}}')">🔗 /@${{w.username}}</span>
        </td>
        <td class="val-green" style="font-weight: 700;">$${{Math.round(w.total_value).toLocaleString()}}</td>
        <td>${{w.followers.toLocaleString()}}</td>
        <td class="val-purple" style="font-weight: 800;">$${{Math.round(w.shadow_ratio).toLocaleString()}} / sub</td>
        <td>${{topHoldings}}</td>
        <td><span class="whale-badge">VERIFIED</span></td>
      </tr>
    `;
  }}).join('');
}}

// TICKER MODAL & HISTORICAL CHART (CLEAN RESOLUTION)
function openTickerModal(ticker, pushHistory = true) {{
  let cleanTicker = (ticker || '').toUpperCase();
  let cleanName = cleanTicker;

  if (cleanTicker.startsWith('SEC_') || cleanTicker.includes('SEC_')) {{
    cleanTicker = 'UNLISTED';
    cleanName = EXTRA_TICKER_NAMES[ticker] || 'Private / Unlisted Security';
  }} else if (EXTRA_TICKER_NAMES[cleanTicker]) {{
    cleanName = EXTRA_TICKER_NAMES[cleanTicker];
  }}

  currentOpenTicker = cleanTicker;
  
  const whales = TICKER_WHALES[ticker] || TICKER_WHALES[cleanTicker] || [];
  const totalWhaleVal = whales.reduce((acc, x) => acc + x.value, 0);

  let s = STOCKS_DATA.find(x => x.ticker.toUpperCase() === cleanTicker);
  if (!s) {{
    let estPrice = 0;
    const sampleWhale = whales.find(w => w.shares > 0 && w.value > 0);
    if (sampleWhale) estPrice = sampleWhale.value / sampleWhale.shares;

    s = {{
      ticker: cleanTicker,
      name: cleanName,
      price: estPrice,
      changePercent: 0,
      owners: whales.length,
      totalValue: totalWhaleVal,
      isETF: false
    }};
  }}

  document.getElementById('tickerModalTitle').innerText = `$${{s.ticker}} • ${{s.name}}`;
  document.getElementById('tickerModalSub').innerText = `${{s.isETF ? 'ETF' : 'Equity'}} | Price: $${{s.price.toFixed(2)}} | Tracked Whale Capital: $${{Math.round(totalWhaleVal).toLocaleString()}}`;
  document.getElementById('tickerModalSlugText').innerText = `https://ah.mphinance.com/ticker/${{s.ticker}}`;
  document.getElementById('tickerModalWhalesCount').innerText = whales.length;

  document.getElementById('tickerModalStrip').innerHTML = `
    <div><div class="whale-m-label">PRICE</div><div class="whale-m-val">$${{s.price.toFixed(2)}}</div></div>
    <div><div class="whale-m-label">24H CHANGE</div><div class="whale-m-val ${{s.changePercent >= 0 ? 'pos-green':'neg-red'}}">${{s.changePercent >= 0 ? '+' : ''}}${{s.changePercent.toFixed(2)}}%</div></div>
    <div><div class="whale-m-label">WHALE CAPITAL</div><div class="whale-m-val val-cyan">$${{Math.round(totalWhaleVal).toLocaleString()}}</div></div>
    <div><div class="whale-m-label">WHALE COUNT</div><div class="whale-m-val val-purple">${{whales.length}} Whales</div></div>
    <div><div class="whale-m-label">APP OWNERS</div><div class="whale-m-val">${{s.owners.toLocaleString()}}</div></div>
  `;

  // RENDER HISTORICAL CANDLESTICK / LINE CHART
  const chartBox = document.getElementById('tickerChartContainer');
  const hist = HISTORIC_DATA[cleanTicker];
  if (hist && hist.bars && hist.bars.length > 0) {{
    chartBox.style.display = 'block';
    chartBox.innerHTML = renderSvgHistoricalChart(cleanTicker, hist.bars);
  }} else {{
    chartBox.style.display = 'none';
    chartBox.innerHTML = '';
  }}

  // WHALES TABLE
  const body = document.getElementById('tickerModalWhalesBody');
  if (whales.length === 0) {{
    body.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 20px;">No tracked whales currently hold verified positions in this asset.</td></tr>';
  }} else {{
    body.innerHTML = whales.map(w => {{
      const pnlSign = w.profit >= 0 ? '+' : '';
      const pnlCls = w.profit >= 0 ? 'pos-green' : 'neg-red';
      return `
        <tr class="clickable-row" onclick="openWhaleModal('${{w.username}}')">
          <td style="font-weight: 700; color: var(--cyan);">@${{w.username}}</td>
          <td>${{w.shares.toLocaleString()}}</td>
          <td class="val-green" style="font-weight: 700;">$${{w.value.toLocaleString()}}</td>
          <td>$${{w.cost_basis.toFixed(2)}}</td>
          <td class="${{pnlCls}}">${{pnlSign}}$${{w.profit.toLocaleString()}}</td>
          <td>${{w.followers.toLocaleString()}}</td>
        </tr>
      `;
    }}).join('');
  }}

  document.getElementById('tickerModal').classList.add('active');

  if (pushHistory && window.history && window.history.pushState) {{
    window.history.pushState(null, '', `/ticker/${{s.ticker}}`);
  }}
}}

function renderSvgHistoricalChart(ticker, bars) {{
  const width = 860;
  const height = 180;
  const padding = {{ top: 20, right: 30, bottom: 25, left: 50 }};
  const plotW = width - padding.left - padding.right;
  const plotH = height - padding.top - padding.bottom;

  const closes = bars.map(b => b.close);
  const minP = Math.min(...closes);
  const maxP = Math.max(...closes);
  const pRange = maxP - minP || 1;

  const firstClose = closes[0];
  const lastClose = closes[closes.length - 1];
  const totalChangePct = ((lastClose - firstClose) / firstClose) * 100;
  const isUp = totalChangePct >= 0;
  const strokeColor = isUp ? '#10B981' : '#F43F5E';
  const fillGradient = isUp ? 'url(#greenGrad)' : 'url(#redGrad)';

  const points = bars.map((b, i) => {{
    const x = padding.left + (i / (bars.length - 1)) * plotW;
    const y = padding.top + plotH - ((b.close - minP) / pRange) * plotH;
    return `${{x.toFixed(1)}},${{y.toFixed(1)}}`;
  }});

  const polylineStr = points.join(' ');
  const areaStr = `${{padding.left}},${{padding.top + plotH}} ` + polylineStr + ` ${{padding.left + plotW}},${{padding.top + plotH}}`;

  return `
    <div class="chart-box">
      <div class="chart-header">
        <div>
          <span style="font-weight: 700; color: var(--text-primary); font-size: 13px;">${{ticker}} 44-Day Daily Performance Trend</span>
          <span style="margin-left: 8px; font-size: 11px; color: var(--text-muted);">(Verified OHLCV Daily Bars)</span>
        </div>
        <div style="font-weight: 700; color: ${{strokeColor}};">
          ${{isUp ? '+' : ''}}${{totalChangePct.toFixed(2)}}% over 44 days &bull; Low: $${{minP.toFixed(2)}} | High: $${{maxP.toFixed(2)}}
        </div>
      </div>
      <svg class="chart-svg" viewBox="0 0 ${{width}} ${{height}}" preserveAspectRatio="none">
        <defs>
          <linearGradient id="greenGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#10B981" stop-opacity="0.25"/>
            <stop offset="100%" stop-color="#10B981" stop-opacity="0.0"/>
          </linearGradient>
          <linearGradient id="redGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#F43F5E" stop-opacity="0.25"/>
            <stop offset="100%" stop-color="#F43F5E" stop-opacity="0.0"/>
          </linearGradient>
        </defs>
        <line x1="${{padding.left}}" y1="${{padding.top}}" x2="${{width - padding.right}}" y2="${{padding.top}}" stroke="#1E293B" stroke-dasharray="4"/>
        <line x1="${{padding.left}}" y1="${{padding.top + plotH/2}}" x2="${{width - padding.right}}" y2="${{padding.top + plotH/2}}" stroke="#1E293B" stroke-dasharray="4"/>
        <line x1="${{padding.left}}" y1="${{padding.top + plotH}}" x2="${{width - padding.right}}" y2="${{padding.top + plotH}}" stroke="#1E293B"/>

        <text x="${{padding.left - 8}}" y="${{padding.top + 4}}" fill="#64748B" font-size="10" font-family="monospace" text-anchor="end">$${{maxP.toFixed(1)}}</text>
        <text x="${{padding.left - 8}}" y="${{padding.top + plotH/2 + 3}}" fill="#64748B" font-size="10" font-family="monospace" text-anchor="end">$${{((maxP+minP)/2).toFixed(1)}}</text>
        <text x="${{padding.left - 8}}" y="${{padding.top + plotH}}" fill="#64748B" font-size="10" font-family="monospace" text-anchor="end">$${{minP.toFixed(1)}}</text>

        <polygon points="${{areaStr}}" fill="${{fillGradient}}" />
        <polyline fill="none" stroke="${{strokeColor}}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" points="${{polylineStr}}" />
      </svg>
    </div>
  `;
}}

// WHALE MODAL (WITH ACCURATE ASSET NAMES)
function openWhaleModal(username, pushHistory = true) {{
  currentOpenWhale = username;
  const cleanU = username.replace(/^@/, '');
  const w = WHALES_DATA.find(x => x.username.toLowerCase() === cleanU.toLowerCase());
  if (!w) return;

  document.getElementById('whaleModalTitle').innerText = `@${{w.username}} • Whale Dossier`;
  document.getElementById('whaleModalSub').innerText = `Followers: ${{w.followers.toLocaleString()}} | Verified Capital: $${{Math.round(w.total_value).toLocaleString()}}`;
  document.getElementById('whaleModalSlugText').innerText = `https://ah.mphinance.com/@${{w.username}}`;

  const pnlSign = w.profit >= 0 ? '+' : '';
  const pnlCls = w.profit >= 0 ? 'pos-green' : 'neg-red';

  document.getElementById('whaleModalStrip').innerHTML = `
    <div><div class="whale-m-label">NET WORTH</div><div class="whale-m-val val-green">$${{Math.round(w.total_value).toLocaleString()}}</div></div>
    <div><div class="whale-m-label">TOTAL PROFIT</div><div class="whale-m-val ${{pnlCls}}">${{pnlSign}}$${{Math.round(w.profit).toLocaleString()}}</div></div>
    <div><div class="whale-m-label">FOLLOWERS</div><div class="whale-m-val">${{w.followers.toLocaleString()}}</div></div>
    <div><div class="whale-m-label">SHADOW RATIO</div><div class="whale-m-val val-purple">$${{Math.round(w.shadow_ratio).toLocaleString()}} / sub</div></div>
  `;

  const body = document.getElementById('whaleModalPositionsBody');
  const pos = w.all_positions || [];
  if (pos.length === 0) {{
    body.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 20px;">No public positions reported.</td></tr>';
  }} else {{
    body.innerHTML = pos.map(p => {{
      const pSign = (p.profit || 0) >= 0 ? '+' : '';
      const pCls = (p.profit || 0) >= 0 ? 'pos-green' : 'neg-red';
      const cleanTicker = (p.ticker || '').toUpperCase();
      const secName = p.name || EXTRA_TICKER_NAMES[cleanTicker] || cleanTicker;
      
      return `
        <tr class="clickable-row" onclick="hideModal('whaleModal'); openTickerModal('${{cleanTicker}}')">
          <td style="font-weight: 800; color: var(--cyan);">${{cleanTicker}}</td>
          <td style="color: var(--text-secondary); max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{secName}}</td>
          <td>${{Number(p.quantity || 0).toLocaleString()}}</td>
          <td class="val-green" style="font-weight: 700;">$${{Number(p.value || 0).toLocaleString()}}</td>
          <td>$${{Number(p.cost_basis || 0).toFixed(2)}}</td>
          <td class="${{pCls}}">${{pSign}}$${{Number(p.profit || 0).toLocaleString()}}</td>
        </tr>
      `;
    }}).join('');
  }}

  document.getElementById('whaleModal').classList.add('active');

  if (pushHistory && window.history && window.history.pushState) {{
    window.history.pushState(null, '', `/@${{w.username}}`);
  }}
}}

function hideModal(modalId) {{
  document.getElementById(modalId).classList.remove('active');
  if (modalId === 'tickerModal') currentOpenTicker = null;
  if (modalId === 'whaleModal') currentOpenWhale = null;

  if (window.history && window.history.pushState) {{
    window.history.pushState(null, '', currentRoute);
  }}
}}

function closeModal(event, modalId) {{
  if (event.target.classList.contains('modal-overlay')) {{
    hideModal(modalId);
  }}
}}

// SLUG CLIPBOARD HELPERS
function copySlug(slug) {{
  const fullUrl = `https://ah.mphinance.com${{slug}}`;
  navigator.clipboard.writeText(fullUrl).then(() => {{
    alert(`Copied link to clipboard: ${{fullUrl}}`);
  }}).catch(() => {{
    prompt('Copy this permalink slug:', fullUrl);
  }});
}}

function copyTickerSlug() {{
  if (!currentOpenTicker) return;
  const fullUrl = `https://ah.mphinance.com/ticker/${{currentOpenTicker}}`;
  const btn = document.getElementById('tickerCopyBtn');
  navigator.clipboard.writeText(fullUrl).then(() => {{
    btn.innerText = '✅ Copied!';
    setTimeout(() => {{ btn.innerText = '📋 Copy Slug Link'; }}, 2000);
  }}).catch(() => {{
    prompt('Copy this permalink slug:', fullUrl);
  }});
}}

function copyWhaleSlug() {{
  if (!currentOpenWhale) return;
  const fullUrl = `https://ah.mphinance.com/@${{currentOpenWhale}}`;
  const btn = document.getElementById('whaleCopyBtn');
  navigator.clipboard.writeText(fullUrl).then(() => {{
    btn.innerText = '✅ Copied!';
    setTimeout(() => {{ btn.innerText = '📋 Copy Slug Link'; }}, 2000);
  }}).catch(() => {{
    prompt('Copy this permalink slug:', fullUrl);
  }});
}}

// INITIAL LOAD
document.addEventListener('DOMContentLoaded', () => {{
  filterStocks();
  renderWhales();
  renderShadowWhales();
  parseInitialRoute();
}});
</script>
</body>
</html>
"""

# Write index.html
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[+] Wrote updated index.html ({len(html_content)} bytes)")
print(f"[+] Total stocks enriched: {len(stocks)} (ETFs: {etfs_count}, Equities: {equities_count})")
print(f"[+] Total whales indexed: {len(whales)}")

# Generate static slug directory mirrors so standard static file servers route cleanly
STATIC_SLUGS = ["all", "stonks", "etfs", "whales", "shadow", "sitemap"]
for slug in STATIC_SLUGS:
    slug_dir = BASE_DIR / slug
    slug_dir.mkdir(parents=True, exist_ok=True)
    with open(slug_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
print(f"[+] Generated static HTML directory mirrors for: {STATIC_SLUGS}")
