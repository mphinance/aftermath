#!/usr/bin/env python3
"""
Generates the next-generation, institutional-grade AfterHour Alpha Terminal.
Includes:
- 395 verified whales ($169M+ AUM)
- 250 securities with explicit 'Why It's Top' taxonomy (Whale Capital, Most Owned, Gainers, Chat)
- Full Inverted Index: Every stock lists all verified whales who own it
- Bi-directional navigation: Click stock -> see whales; Click whale -> see positions -> click stock
- TraderMatrix Pro referral funnel integration throughout
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "leaderboard"
INDEX_FILE = BASE_DIR / "index.html"
REPORT_FILE = BASE_DIR / "reports" / "afterhour_quant_terminal.html"

# Load stocks
with open(DATA_DIR / "stock_leaderboard.json", encoding="utf-8") as f:
    board_data = json.load(f)

# Load ranked whales
with open(DATA_DIR / "all_verified_whales_ranked.json", encoding="utf-8") as f:
    whale_data = json.load(f)

whales = whale_data.get("whales", [])

# Build Inverted Index: Ticker -> List of Whales holding it
ticker_to_whales = {}
for w in whales:
    flw = max(1, w.get("followers", 0))
    w["shadow_ratio"] = round(w["total_value"] / flw, 2)
    for p in w.get("all_positions", []):
        t = p.get("ticker")
        if not t:
            continue
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

# Build compact and enriched stock records
stocks = []
for idx, s in enumerate(board_data.get("securities", [])[:250], 1):
    sec = s.get("security", {})
    info = sec.get("security", {})
    ticker = info.get("tickerSymbol") or info.get("name")
    if not ticker:
        continue
    price_obj = sec.get("price", {})
    sess = price_obj.get("session", {})
    
    owners = sec.get("ownerCount", 0)
    total_val = round(sec.get("totalValue", 0), 2)
    change_pct = round(sess.get("changePercent", 0), 2)
    chat_members = info.get("chatroom", {}).get("memberCount", 0)
    
    w_list = ticker_to_whales.get(ticker, [])
    w_val = round(sum(x["value"] for x in w_list), 2)
    w_cnt = len(w_list)
    top_whale = w_list[0] if w_list else None
    
    # Determine explicit 'Why It's Top' reason & badges
    badges = []
    reasons = []
    
    if w_val >= 5_000_000:
        badges.append({"label": "MEGA WHALE ACCUMULATION", "color": "purple"})
        reasons.append(f"${w_val/1_000_000:.1f}M+ verified whale capital")
    elif w_val >= 1_000_000:
        badges.append({"label": "WHALE ACCUMULATION", "color": "cyan"})
        reasons.append(f"${w_val/1_000_000:.1f}M whale backing")
        
    if owners >= 300:
        badges.append({"label": "PLATFORM HEAVYWEIGHT", "color": "amber"})
        reasons.append(f"{owners:,} verified holders")
    elif owners >= 50:
        badges.append({"label": "POPULAR RETAIL", "color": "amber"})
        
    if change_pct >= 4.0:
        badges.append({"label": "TOP 24H SURGE", "color": "green"})
        reasons.append(f"+{change_pct:.1f}% intraday move")
    elif change_pct <= -4.0:
        badges.append({"label": "HIGH VOL DIP", "color": "red"})
        reasons.append(f"{change_pct:.1f}% intraday selloff")
        
    if chat_members >= 3000:
        badges.append({"label": "VIRAL CHATROOM", "color": "cyan"})
        reasons.append(f"{chat_members:,} chat participants")
        
    if not badges:
        badges.append({"label": "TRENDING LEADERBOARD", "color": "cyan"})
        reasons.append(f"Rank #{idx} on AfterHour Trending")

    stocks.append({
        "rank": idx,
        "ticker": ticker,
        "name": info.get("name", ""),
        "owners": owners,
        "totalValue": total_val,
        "marketCap": sec.get("marketCap", 0),
        "price": round(price_obj.get("price", 0), 2),
        "changePercent": change_pct,
        "volume": sess.get("volume", 0),
        "chatroomMembers": chat_members,
        "whalesCount": w_cnt,
        "whalesValue": w_val,
        "topWhale": top_whale["username"] if top_whale else None,
        "topWhaleValue": top_whale["value"] if top_whale else 0,
        "badges": badges,
        "whyTop": " &bull; ".join(reasons) if reasons else "Trending security on AfterHour",
    })

total_platform_val = sum(s["totalValue"] for s in stocks)
total_whale_val = sum(w["total_value"] for w in whales)
millionaires_count = len([w for w in whales if w["total_value"] >= 1_000_000])

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AfterHour Alpha & Whale Terminal | Powered by TraderMatrix Pro</title>
<meta name="description" content="Institutional-grade reverse-engineered intelligence terminal tracking 395 verified AfterHour whale portfolios, $169M+ AUM, and 250 securities. Powered by TraderMatrix Pro.">
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
    padding: 20px;
    -webkit-font-smoothing: antialiased;
  }}
  .container {{ max-width: 1440px; margin: 0 auto; }}
  
  header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 18px;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 16px;
  }}
  .brand {{ display: flex; align-items: center; gap: 14px; }}
  .brand-logo-img {{
    width: 44px; height: 44px; border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    transition: transform 0.2s ease;
    display: block;
  }}
  .brand-logo-img:hover {{ transform: scale(1.05); }}
  .brand-title h1 {{ font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }}
  .brand-title p {{ font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono); }}
  
  .header-badges {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .live-badge {{
    display: flex; align-items: center; gap: 8px;
    background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 6px 14px; border-radius: 20px; font-size: 12px; font-family: var(--font-mono);
    color: var(--green); font-weight: 600;
  }}
  .live-dot {{
    width: 8px; height: 8px; border-radius: 50%; background: var(--green);
    box-shadow: 0 0 10px var(--green);
    animation: pulse 2s infinite;
  }}
  @keyframes pulse {{ 0% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.4; }} }}
  
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

  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px; margin-bottom: 24px;
  }}
  .stat-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px;
    position: relative; overflow: hidden;
  }}
  .stat-card::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--border-accent), transparent);
  }}
  .stat-label {{ font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); font-weight: 600; letter-spacing: 0.5px; margin-bottom: 6px; }}
  .stat-value {{ font-size: 24px; font-weight: 800; font-family: var(--font-mono); letter-spacing: -0.5px; }}
  .stat-sub {{ font-size: 12px; color: var(--text-secondary); margin-top: 4px; }}
  .val-cyan {{ color: var(--cyan); }}
  .val-green {{ color: var(--green); }}
  .val-amber {{ color: var(--amber); }}
  .val-purple {{ color: var(--purple); }}

  .nav-tabs {{
    display: flex; gap: 8px; border-bottom: 1px solid var(--border);
    margin-bottom: 20px; overflow-x: auto; padding-bottom: 4px;
  }}
  .tab-btn {{
    background: transparent; border: none; color: var(--text-secondary);
    padding: 10px 18px; border-radius: 8px; font-size: 14px; font-weight: 600;
    cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 8px;
    white-space: nowrap;
  }}
  .tab-btn:hover {{ background: var(--bg-surface); color: var(--text-primary); }}
  .tab-btn.active {{
    background: var(--bg-card); color: var(--cyan);
    border: 1px solid var(--border-accent);
  }}

  .controls-bar {{
    display: flex; justify-content: space-between; align-items: center;
    gap: 12px; margin-bottom: 20px; flex-wrap: wrap;
  }}
  .search-input {{
    background: var(--bg-surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 10px 16px; font-size: 13px;
    color: var(--text-primary); font-family: var(--font-mono);
    min-width: 280px; flex: 1; outline: none; transition: border-color 0.2s ease;
  }}
  .search-input:focus {{ border-color: var(--cyan); }}
  
  .filter-group {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
  .filter-btn {{
    background: var(--bg-surface); border: 1px solid var(--border);
    color: var(--text-secondary); padding: 8px 14px; border-radius: 6px;
    font-size: 12px; font-family: var(--font-mono); font-weight: 600;
    cursor: pointer; transition: all 0.2s ease;
  }}
  .filter-btn:hover {{ color: var(--text-primary); border-color: var(--border-accent); }}
  .filter-btn.active {{ background: var(--cyan); color: #000; border-color: var(--cyan); font-weight: 700; }}

  .tab-pane {{ display: none; }}
  .tab-pane.active {{ display: block; }}

  /* TAXONOMY REASON BADGES */
  .reason-badge {{
    display: inline-block; font-size: 10px; font-family: var(--font-mono); font-weight: 800;
    padding: 2px 7px; border-radius: 4px; letter-spacing: 0.3px; margin-right: 4px; margin-bottom: 3px;
  }}
  .badge-purple {{ background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.4); color: var(--purple); }}
  .badge-cyan {{ background: rgba(0, 240, 255, 0.15); border: 1px solid rgba(0, 240, 255, 0.4); color: var(--cyan); }}
  .badge-amber {{ background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); color: var(--amber); }}
  .badge-green {{ background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: var(--green); }}
  .badge-red {{ background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4); color: var(--red); }}

  /* WHALE CARDS GRID */
  .whale-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 14px;
  }}
  .whale-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 18px;
    transition: all 0.2s ease; cursor: pointer;
    display: flex; flex-direction: column; justify-content: space-between;
  }}
  .whale-card:hover {{
    background: var(--bg-card);
    border-color: var(--cyan);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  }}
  .whale-header {{
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 12px;
  }}
  .whale-user {{ display: flex; align-items: center; gap: 10px; }}
  .whale-avatar {{
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, #1E293B, #334155);
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 15px; color: var(--cyan);
    border: 1px solid var(--border-accent);
  }}
  .whale-name {{ font-weight: 700; font-size: 15px; }}
  .whale-rank {{ font-size: 11px; font-family: var(--font-mono); color: var(--text-muted); }}
  .whale-badge {{
    background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3);
    color: var(--cyan); font-size: 10px; font-family: var(--font-mono);
    padding: 3px 8px; border-radius: 4px; font-weight: 700;
  }}
  
  .whale-metrics {{
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 10px; margin-bottom: 14px;
    background: var(--bg-base); padding: 12px; border-radius: 8px;
    border: 1px solid var(--border);
  }}
  .w-metric-label {{ font-size: 10px; color: var(--text-muted); font-family: var(--font-mono); }}
  .w-metric-val {{ font-size: 16px; font-weight: 800; font-family: var(--font-mono); margin-top: 2px; }}
  
  .holdings-row {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }}
  .holding-chip {{
    background: var(--bg-base); border: 1px solid var(--border);
    padding: 4px 8px; border-radius: 4px; font-size: 11px;
    font-family: var(--font-mono); color: var(--text-secondary);
    transition: all 0.15s ease;
  }}
  .holding-chip:hover {{
    border-color: var(--cyan); color: var(--cyan); background: var(--bg-surface);
  }}

  /* DATA TABLE */
  .table-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden;
  }}
  table {{ width: 100%; border-collapse: collapse; text-align: left; }}
  th {{
    background: var(--bg-base); color: var(--text-muted);
    font-size: 11px; font-family: var(--font-mono); text-transform: uppercase;
    padding: 12px 16px; font-weight: 600; border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }}
  td {{
    padding: 12px 16px; border-bottom: 1px solid var(--border);
    font-size: 13px; font-family: var(--font-mono);
  }}
  tr.clickable-row {{ cursor: pointer; transition: background 0.15s ease; }}
  tr.clickable-row:hover td {{ background: var(--bg-card); }}
  .pos-green {{ color: var(--green); }}
  .neg-red {{ color: var(--red); }}

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
    border-radius: 16px; width: 100%; max-width: 900px;
    max-height: 85vh; overflow-y: auto; box-shadow: 0 24px 50px rgba(0,0,0,0.8);
    position: relative;
  }}
  .modal-header {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 22px 26px; border-bottom: 1px solid var(--border);
    position: sticky; top: 0; background: var(--bg-surface); z-index: 10;
  }}
  .modal-body {{ padding: 22px 26px; }}
  .close-btn {{
    background: transparent; border: none; font-size: 26px;
    color: var(--text-muted); cursor: pointer; line-height: 1;
  }}
  .close-btn:hover {{ color: var(--text-primary); }}

  .modal-stat-strip {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px; margin-bottom: 20px; background: var(--bg-base); padding: 14px;
    border-radius: 10px; border: 1px solid var(--border);
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
        <h1>AfterHour Alpha Terminal</h1>
        <p>Institutional Alt-Data &bull; Powered by <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank" style="color: var(--cyan); text-decoration: none; font-weight: 700;">TraderMatrix Pro</a></p>
      </div>
    </div>
    <div class="header-badges">
      <div class="live-badge">
        <div class="live-dot"></div>
        LIVE ALT-DATA
      </div>
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

  <!-- MACRO STATS -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">TOTAL VERIFIED WHALE CAPITAL</div>
      <div class="stat-value val-green">${total_whale_val:,.0f}</div>
      <div class="stat-sub">{len(whales)} active verified portfolios</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">VERIFIED MILLIONAIRES</div>
      <div class="stat-value val-cyan">{millionaires_count} ACCOUNTS</div>
      <div class="stat-sub">Controlling $110.8M+ AUM</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">TOP TRACKED WHALE</div>
      <div class="stat-value val-purple">${whales[0]['total_value']:,.0f}</div>
      <div class="stat-sub">@{whales[0]['username']} ({", ".join([p['ticker'] for p in whales[0]['top_positions'][:2]])})</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">SECURITIES TRACKED</div>
      <div class="stat-value val-amber">{len(stocks)} TICKERS</div>
      <div class="stat-sub">Enriched with verified whale ownership</div>
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

  <!-- NAVIGATION TABS -->
  <div class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('stocks')">
      <span>&#x1F4C8;</span> Top Stonks &amp; Taxonomy ({len(stocks)})
    </button>
    <button class="tab-btn" onclick="switchTab('whales')">
      <span>&#x1F40B;</span> Whale Radar ({len(whales)})
    </button>
    <button class="tab-btn" onclick="switchTab('shadow')">
      <span>&#x1F916;</span> Shadow Whales (Under-Followed)
    </button>
  </div>

  <!-- TAB 1: TOP STOCKS & TAXONOMY -->
  <div id="tab-stocks" class="tab-pane active">
    <div class="controls-bar">
      <input type="text" id="stockSearch" class="search-input" placeholder="Search stocks by ticker or company name (e.g. NVDA, Apple, ASTS)..." oninput="filterStocks()">
      <div class="filter-group">
        <button class="filter-btn active" id="btnStockAll" onclick="setStockFilter('all')">All (250)</button>
        <button class="filter-btn" id="btnStockWhales" onclick="setStockFilter('whales')">🐋 Whale Favorites ($1M+)</button>
        <button class="filter-btn" id="btnStockOwners" onclick="setStockFilter('owners')">👑 Most Owned on App</button>
        <button class="filter-btn" id="btnStockGainers" onclick="setStockFilter('gainers')">🚀 Top Gainers</button>
        <button class="filter-btn" id="btnStockChat" onclick="setStockFilter('chat')">💬 Active Chatrooms</button>
      </div>
    </div>
    <div class="table-card">
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Ticker</th>
              <th>Company Name</th>
              <th>Why It's Top / Category</th>
              <th>Verified Whale Backing</th>
              <th>App Owners</th>
              <th>Price ($)</th>
              <th>24h %</th>
              <th>Chatroom</th>
            </tr>
          </thead>
          <tbody id="stocksBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 2: WHALE RADAR -->
  <div id="tab-whales" class="tab-pane">
    <div class="controls-bar">
      <input type="text" id="whaleSearch" class="search-input" placeholder="Search by handle or ticker (e.g. SlowmoInvestor, AAPL, ASTS)..." oninput="filterWhales()">
      <div class="filter-group">
        <button class="filter-btn active" id="btnSortVal" onclick="sortWhales('value')">Sort: Net Worth ($)</button>
        <button class="filter-btn" id="btnSortRatio" onclick="sortWhales('ratio')">Sort: $/Follower Ratio</button>
        <button class="filter-btn" id="btnSortPnL" onclick="sortWhales('pnl')">Sort: Total Profit</button>
      </div>
    </div>
    <div class="whale-grid" id="whaleContainer"></div>
  </div>

  <!-- TAB 3: SHADOW WHALES -->
  <div id="tab-shadow" class="tab-pane">
    <div style="margin-bottom: 16px; color: var(--text-secondary); font-size: 13px;">
      <strong>The Clout Inversion Thesis</strong>: Retail follower counts on trading social apps are heavily disconnected from actual capital. The accounts below hold seven and eight-figure portfolios while flying under the radar with minimal followers.
    </div>
    <div class="table-card">
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Handle</th>
              <th>Verified Equity</th>
              <th>Followers</th>
              <th>$/Follower Ratio</th>
              <th>Top Concentrated Holdings</th>
              <th>Verified Since</th>
            </tr>
          </thead>
          <tbody id="shadowBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer>
    <div>&copy; 2026 Momentum Phinance &bull; Built with radical transparency</div>
    <div>Institutional options flow &amp; GEX data via <a href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank">TraderMatrix Pro (Code: MPHINANCE)</a></div>
  </footer>
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
      <div id="whaleModalStrip" class="modal-stat-strip"></div>
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Ticker (Click to View)</th>
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
      <div id="tickerModalStrip" class="modal-stat-strip"></div>
      
      <!-- TraderMatrix Pro contextual CTA inside modal -->
      <div style="background: linear-gradient(135deg, rgba(0, 240, 255, 0.1), rgba(168, 85, 247, 0.1)); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 10px; padding: 12px 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; gap: 14px; flex-wrap: wrap;">
        <div>
          <div style="font-size: 12px; font-weight: 700; color: var(--cyan);">Track Institutional Order Flow &amp; GEX Levels</div>
          <div style="font-size: 11px; color: var(--text-secondary);">See real-time dark pool block trades and dealer gamma walls for this ticker on TraderMatrix.</div>
        </div>
        <a id="tickerModalTmBtn" href="https://www.tradermatrix.pro/?ref=MPHINANCE" target="_blank" style="background: var(--cyan); color: #000; font-size: 12px; font-weight: 800; font-family: var(--font-mono); padding: 8px 14px; border-radius: 6px; text-decoration: none; white-space: nowrap;">
          View on TraderMatrix &rarr;
        </a>
      </div>

      <div style="font-size: 13px; font-weight: 700; margin-bottom: 10px; color: var(--text-primary);">
        Verified AfterHour Whales Holding This Stock:
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

<script>
const STOCKS_DATA = {json.dumps(stocks)};
const WHALES_DATA = {json.dumps(whales)};
const TICKER_WHALES = {json.dumps(ticker_to_whales)};

let currentStockFilter = 'all';
let currentWhaleSort = 'value';
let filteredWhales = [...WHALES_DATA];
let filteredStocks = [...STOCKS_DATA];

function switchTab(tabId) {{
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  event.currentTarget.classList.add('active');
  document.getElementById('tab-' + tabId).classList.add('active');
}}

// STOCK FILTERS
function setStockFilter(mode) {{
  currentStockFilter = mode;
  document.querySelectorAll('#tab-stocks .filter-btn').forEach(b => b.classList.remove('active'));
  if (mode === 'all') document.getElementById('btnStockAll').classList.add('active');
  if (mode === 'whales') document.getElementById('btnStockWhales').classList.add('active');
  if (mode === 'owners') document.getElementById('btnStockOwners').classList.add('active');
  if (mode === 'gainers') document.getElementById('btnStockGainers').classList.add('active');
  if (mode === 'chat') document.getElementById('btnStockChat').classList.add('active');
  filterStocks();
}}

function filterStocks() {{
  const q = (document.getElementById('stockSearch').value || '').toLowerCase().trim();
  filteredStocks = STOCKS_DATA.filter(s => {{
    if (q && !s.ticker.toLowerCase().includes(q) && !s.name.toLowerCase().includes(q)) {{
      return false;
    }}
    if (currentStockFilter === 'whales') return s.whalesValue >= 1000000;
    if (currentStockFilter === 'owners') return s.owners >= 100;
    if (currentStockFilter === 'gainers') return s.changePercent >= 2.0;
    if (currentStockFilter === 'chat') return s.chatroomMembers >= 2000;
    return true;
  }});

  // Sort according to category filter
  if (currentStockFilter === 'whales') {{
    filteredStocks.sort((a, b) => b.whalesValue - a.whalesValue);
  }} else if (currentStockFilter === 'owners') {{
    filteredStocks.sort((a, b) => b.owners - a.owners);
  }} else if (currentStockFilter === 'gainers') {{
    filteredStocks.sort((a, b) => b.changePercent - a.changePercent);
  }} else if (currentStockFilter === 'chat') {{
    filteredStocks.sort((a, b) => b.chatroomMembers - a.chatroomMembers);
  }} else {{
    filteredStocks.sort((a, b) => a.rank - b.rank);
  }}

  renderStocks(filteredStocks);
}}

function renderStocks(list) {{
  const body = document.getElementById('stocksBody');
  if (list.length === 0) {{
    body.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--text-muted); padding: 30px;">No stocks match your filter query.</td></tr>';
    return;
  }}

  body.innerHTML = list.map(s => {{
    const sign = s.changePercent >= 0 ? '+' : '';
    const cls = s.changePercent >= 0 ? 'pos-green' : 'neg-red';
    
    const badgeHtml = (s.badges || []).map(b => {{
      return `<span class="reason-badge badge-${{b.color}}">${{b.label}}</span>`;
    }}).join('');

    const whaleBackingHtml = s.whalesCount > 0 
      ? `<div style="font-weight: 700; color: var(--cyan);">${{s.whalesCount}} Whales ($${{(s.whalesValue/1000000).toFixed(1)}}M)</div>
         <div style="font-size: 11px; color: var(--text-muted);">Top: @${{s.topWhale}}</div>`
      : `<span style="color: var(--text-muted); font-size: 11px;">0 tracked whales</span>`;

    return `
      <tr class="clickable-row" onclick="openTickerModal('${{s.ticker}}')">
        <td style="color: var(--text-muted);">${{s.rank}}</td>
        <td style="font-weight: 800; font-size: 14px; color: var(--cyan);">${{s.ticker}}</td>
        <td style="color: var(--text-secondary); max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{s.name}}</td>
        <td>
          <div>${{badgeHtml}}</div>
          <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">${{s.whyTop}}</div>
        </td>
        <td>${{whaleBackingHtml}}</td>
        <td>${{s.owners.toLocaleString()}}</td>
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
  document.querySelectorAll('#tab-whales .filter-btn').forEach(b => b.classList.remove('active'));
  if (mode === 'value') document.getElementById('btnSortVal').classList.add('active');
  if (mode === 'ratio') document.getElementById('btnSortRatio').classList.add('active');
  if (mode === 'pnl') document.getElementById('btnSortPnL').classList.add('active');
  filterWhales();
}}

function filterWhales() {{
  const q = (document.getElementById('whaleSearch').value || '').toLowerCase().trim();
  filteredWhales = WHALES_DATA.filter(w => {{
    if (!q) return true;
    if (w.username.toLowerCase().includes(q)) return true;
    return (w.top_positions || []).some(p => p.ticker && p.ticker.toLowerCase().includes(q));
  }});

  if (currentWhaleSort === 'value') {{
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
    const topHoldings = (w.top_positions || []).slice(0, 3).map(p => {{
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
            <div class="w-metric-label">VERIFIED VALUE</div>
            <div class="w-metric-val val-green">$${{Math.round(w.total_value).toLocaleString()}}</div>
          </div>
          <div>
            <div class="w-metric-label">ALL-TIME P&L</div>
            <div class="w-metric-val ${{pnlClass}}">${{pnlSign}}$${{Math.round(w.profit).toLocaleString()}}</div>
          </div>
        </div>
        <div class="holdings-row">
          ${{topHoldings || '<span class="holding-chip">Cash Only</span>'}}
        </div>
      </div>
    `;
  }}).join('');
}}

function renderShadowTable() {{
  const body = document.getElementById('shadowBody');
  const sorted = [...WHALES_DATA].sort((a, b) => b.shadow_ratio - a.shadow_ratio).slice(0, 35);
  body.innerHTML = sorted.map((w, idx) => {{
    const topAssets = (w.top_positions || []).slice(0, 3).map(p => {{
      return `<span style="color: var(--cyan); cursor: pointer;" onclick="event.stopPropagation(); openTickerModal('${{p.ticker}}')">${{p.ticker}}</span>`;
    }}).join(', ');

    return `
      <tr class="clickable-row" onclick="openWhaleModal('${{w.username}}')">
        <td style="color: var(--text-muted);">#${{idx + 1}}</td>
        <td style="font-weight: 700; color: var(--cyan);">@${{w.username}}</td>
        <td style="font-weight: 700; color: var(--green);">$${{Math.round(w.total_value).toLocaleString()}}</td>
        <td>${{w.followers.toLocaleString()}}</td>
        <td style="font-weight: 700; color: var(--purple);">$${{Math.round(w.shadow_ratio).toLocaleString()}} / sub</td>
        <td>${{topAssets || 'Cash'}}</td>
        <td style="color: var(--text-muted); font-size: 11px;">${{w.verified_as_of ? w.verified_as_of.slice(0, 10) : 'N/A'}}</td>
      </tr>
    `;
  }}).join('');
}}

// MODAL CONTROLS
function openWhaleModal(username) {{
  hideModal('tickerModal');
  const w = WHALES_DATA.find(x => x.username === username);
  if (!w) return;
  document.getElementById('whaleModalTitle').innerText = '@' + w.username + ' Portfolio';
  document.getElementById('whaleModalSub').innerText = 'Verified Net Worth: $' + Math.round(w.total_value).toLocaleString() + ' | Followers: ' + w.followers.toLocaleString();
  
  const strip = document.getElementById('whaleModalStrip');
  const pnlSign = w.profit >= 0 ? '+' : '';
  const pnlCls = w.profit >= 0 ? 'pos-green' : 'neg-red';
  strip.innerHTML = `
    <div><div class="w-metric-label">VERIFIED VALUE</div><div class="w-metric-val val-green">$${{Math.round(w.total_value).toLocaleString()}}</div></div>
    <div><div class="w-metric-label">UNREALIZED PROFIT</div><div class="w-metric-val ${{pnlCls}}">${{pnlSign}}$${{Math.round(w.profit).toLocaleString()}}</div></div>
    <div><div class="w-metric-label">SHADOW RATIO</div><div class="w-metric-val val-purple">$${{Math.round(w.shadow_ratio).toLocaleString()}}/sub</div></div>
    <div><div class="w-metric-label">POSITIONS</div><div class="w-metric-val val-cyan">${{w.positions_count || 0}}</div></div>
  `;

  const body = document.getElementById('whaleModalPositionsBody');
  const positions = w.all_positions || w.top_positions || [];
  if (positions.length === 0) {{
    body.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No open equity positions reported (Cash / Index).</td></tr>';
  }} else {{
    body.innerHTML = positions.map(p => {{
      const pnl = p.profit || 0;
      const pnlSign = pnl >= 0 ? '+' : '';
      const pnlCls = pnl >= 0 ? 'pos-green' : 'neg-red';
      return `
        <tr class="clickable-row" onclick="openTickerModal('${{p.ticker}}')">
          <td style="font-weight: 800; color: var(--cyan); text-decoration: underline;">${{p.ticker}}</td>
          <td>${{Number(p.quantity).toLocaleString(undefined, {{maximumFractionDigits: 2}})}}</td>
          <td>$${{Math.round(p.value || 0).toLocaleString()}}</td>
          <td>$${{Math.round(p.cost_basis || 0).toLocaleString()}}</td>
          <td class="${{pnlCls}}">${{pnlSign}}$${{Math.round(pnl).toLocaleString()}}</td>
        </tr>
      `;
    }}).join('');
  }}
  document.getElementById('whaleModal').classList.add('active');
}}

function openTickerModal(ticker) {{
  hideModal('whaleModal');
  const stock = STOCKS_DATA.find(s => s.ticker === ticker) || {{
    ticker: ticker,
    name: ticker + ' Security',
    price: 0,
    changePercent: 0,
    owners: 0,
    chatroomMembers: 0,
    whalesValue: 0
  }};
  
  const whalesHolding = TICKER_WHALES[ticker] || [];
  const totalWhaleVal = whalesHolding.reduce((acc, x) => acc + x.value, 0);

  document.getElementById('tickerModalTitle').innerText = '$' + ticker + ' &bull; ' + (stock.name || '');
  document.getElementById('tickerModalSub').innerText = (stock.whyTop || 'Security detail and verified whale roster');
  
  const strip = document.getElementById('tickerModalStrip');
  const sign = stock.changePercent >= 0 ? '+' : '';
  const cls = stock.changePercent >= 0 ? 'pos-green' : 'neg-red';
  strip.innerHTML = `
    <div><div class="w-metric-label">PRICE</div><div class="w-metric-val">$${{stock.price ? stock.price.toFixed(2) : 'N/A'}}</div></div>
    <div><div class="w-metric-label">24H CHANGE</div><div class="w-metric-val ${{cls}}">${{sign}}${{stock.changePercent ? stock.changePercent.toFixed(2) : '0.00'}}%</div></div>
    <div><div class="w-metric-label">VERIFIED WHALE AUM</div><div class="w-metric-val val-green">$${{Math.round(totalWhaleVal).toLocaleString()}}</div></div>
    <div><div class="w-metric-label">WHALE HOLDERS</div><div class="w-metric-val val-cyan">${{whalesHolding.length}} Accounts</div></div>
    <div><div class="w-metric-label">APP OWNERS</div><div class="w-metric-val val-amber">${{stock.owners ? stock.owners.toLocaleString() : 'N/A'}}</div></div>
  `;

  const body = document.getElementById('tickerModalWhalesBody');
  if (whalesHolding.length === 0) {{
    body.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 20px;">No whales in our 395-ledger currently hold this stock.</td></tr>';
  }} else {{
    body.innerHTML = whalesHolding.map(w => {{
      const pnl = w.profit || 0;
      const pnlSign = pnl >= 0 ? '+' : '';
      const pnlCls = pnl >= 0 ? 'pos-green' : 'neg-red';
      return `
        <tr class="clickable-row" onclick="openWhaleModal('${{w.username}}')">
          <td style="font-weight: 800; color: var(--cyan); text-decoration: underline;">@${{w.username}}</td>
          <td>${{Number(w.shares).toLocaleString(undefined, {{maximumFractionDigits: 2}})}}</td>
          <td style="font-weight: 700; color: var(--green);">$${{Math.round(w.value).toLocaleString()}}</td>
          <td>$${{Math.round(w.cost_basis).toLocaleString()}}</td>
          <td class="${{pnlCls}}">${{pnlSign}}$${{Math.round(pnl).toLocaleString()}}</td>
          <td style="color: var(--text-muted);">${{w.followers.toLocaleString()}}</td>
        </tr>
      `;
    }}).join('');
  }}

  document.getElementById('tickerModal').classList.add('active');
}}

function hideModal(modalId) {{
  document.getElementById(modalId).classList.remove('active');
}}

function closeModal(e, modalId) {{
  if (e.target.id === modalId) hideModal(modalId);
}}

// Initialize
renderStocks(STOCKS_DATA);
renderWhales();
renderShadowTable();
</script>
</body>
</html>
"""

# Write to root index.html
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[+] Successfully wrote {INDEX_FILE} ({len(html_content):,} bytes)")

# Also write to reports/afterhour_quant_terminal.html
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[+] Successfully wrote {REPORT_FILE}")
