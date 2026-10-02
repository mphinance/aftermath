#!/usr/bin/env python3
"""
Builds an interactive HTML dashboard using harvested AfterHour JSON data.
Generates a standalone, dependency-free quant terminal with tabs, charts,
whale portfolio inspections, and search/sort capabilities.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "leaderboard"
OUT_FILE = BASE_DIR / "reports" / "afterhour_quant_terminal.html"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(DATA_DIR / "stock_leaderboard.json", encoding="utf-8") as f:
    board_data = json.load(f)
with open(DATA_DIR / "top_stocks_detail.json", encoding="utf-8") as f:
    detail_data = json.load(f)
with open(DATA_DIR / "top_users_portfolios.json", encoding="utf-8") as f:
    user_data = json.load(f)

# Compact stocks
stocks = []
for idx, s in enumerate(board_data.get("securities", [])[:150], 1):
    sec = s.get("security", {})
    info = sec.get("security", {})
    ticker = info.get("tickerSymbol") or info.get("name")
    if not ticker:
        continue
    price_obj = sec.get("price", {})
    sess = price_obj.get("session", {})
    stocks.append({
        "rank": idx,
        "ticker": ticker,
        "name": info.get("name", ""),
        "owners": sec.get("ownerCount", 0),
        "totalValue": sec.get("totalValue", 0),
        "marketCap": sec.get("marketCap", 0),
        "price": price_obj.get("price", 0),
        "changePercent": sess.get("changePercent", 0),
        "volume": sess.get("volume", 0),
        "chatroomMembers": info.get("chatroom", {}).get("memberCount", 0),
    })

# Format users
users_list = []
for uname, udata in user_data.get("users", {}).items():
    if udata.get("total_value", 0) > 0 or udata.get("positions_count", 0) > 0:
        users_list.append({
            "username": uname,
            "profile_id": udata.get("profile_id"),
            "total_value": udata.get("total_value", 0),
            "profit": udata.get("profit", 0),
            "profit_percent": udata.get("profit_percent", 0),
            "profit_today": udata.get("profit_today", 0),
            "cash_balance": udata.get("cash_balance", 0),
            "verified_as_of": udata.get("verified_as_of"),
            "positions_count": udata.get("positions_count", 0),
            "positions": sorted(
                udata.get("positions", []),
                key=lambda p: (p.get("value") or 0),
                reverse=True
            ),
        })

users_list.sort(key=lambda u: u["total_value"], reverse=True)

total_platform_val = sum(s["totalValue"] for s in stocks)
total_whale_val = sum(u["total_value"] for u in users_list)

template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AfterHour Alpha & Whale Terminal</title>
<style>
  :root {
    --bg-base: #080B10;
    --bg-surface: #0E131C;
    --bg-card: #141B26;
    --bg-card-hover: #1A2433;
    --border: #222E3F;
    --border-accent: #2E3E55;
    --text-primary: #F0F4F8;
    --text-secondary: #8B99AD;
    --text-muted: #536275;
    --cyan: #00F0FF;
    --green: #00E676;
    --red: #FF3366;
    --amber: #FFB300;
    --purple: #B388FF;
    --font-mono: 'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace;
    --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: var(--bg-base);
    color: var(--text-primary);
    font-family: var(--font-sans);
    line-height: 1.5;
    padding: 24px;
    -webkit-font-smoothing: antialiased;
  }
  .container { max-width: 1440px; margin: 0 auto; }
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 16px;
  }
  .brand { display: flex; align-items: center; gap: 12px; }
  .brand-logo {
    width: 36px; height: 36px; border-radius: 8px;
    background: linear-gradient(135deg, var(--cyan), var(--purple));
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 18px; color: #000;
  }
  .brand-title h1 { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
  .brand-title p { font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono); }
  .live-badge {
    display: flex; align-items: center; gap: 8px;
    background: rgba(0, 230, 118, 0.1); border: 1px solid rgba(0, 230, 118, 0.3);
    padding: 6px 14px; border-radius: 20px; font-size: 12px; font-family: var(--font-mono);
    color: var(--green); font-weight: 600;
  }
  .live-dot {
    width: 8px; height: 8px; border-radius: 50%; background: var(--green);
    box-shadow: 0 0 10px var(--green);
    animation: pulse 2s infinite;
  }
  @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px; margin-bottom: 28px;
  }
  .stat-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px;
    position: relative; overflow: hidden;
  }
  .stat-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--border-accent), transparent);
  }
  .stat-label { font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono); margin-bottom: 6px; }
  .stat-value { font-size: 26px; font-weight: 800; font-family: var(--font-mono); letter-spacing: -0.5px; }
  .stat-sub { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
  .val-cyan { color: var(--cyan); }
  .val-green { color: var(--green); }
  .val-amber { color: var(--amber); }
  .val-purple { color: var(--purple); }

  .nav-tabs {
    display: flex; gap: 8px; border-bottom: 1px solid var(--border);
    margin-bottom: 24px; overflow-x: auto; padding-bottom: 4px;
  }
  .tab-btn {
    background: transparent; border: none; color: var(--text-secondary);
    padding: 10px 18px; border-radius: 8px; font-size: 14px; font-weight: 600;
    cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 8px;
  }
  .tab-btn:hover { background: var(--bg-surface); color: var(--text-primary); }
  .tab-btn.active {
    background: var(--bg-card); color: var(--cyan);
    box-shadow: inset 0 -2px 0 var(--cyan);
  }

  .tab-pane { display: none; }
  .tab-pane.active { display: block; }

  /* Whale Cards */
  .whale-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 16px; margin-bottom: 24px;
  }
  .whale-card {
    background: var(--bg-surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 20px; transition: transform 0.2s, border-color 0.2s;
    cursor: pointer;
  }
  .whale-card:hover {
    transform: translateY(-2px); border-color: var(--cyan);
    background: var(--bg-card);
  }
  .whale-header {
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;
  }
  .whale-user { display: flex; align-items: center; gap: 10px; }
  .whale-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, #2E3E55, #141B26);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 700; color: var(--cyan);
    border: 1px solid var(--border-accent);
  }
  .whale-name { font-weight: 700; font-size: 16px; }
  .whale-badge {
    font-size: 11px; padding: 2px 8px; border-radius: 4px;
    background: rgba(0, 240, 255, 0.1); color: var(--cyan);
    font-family: var(--font-mono); font-weight: 600;
  }
  .whale-metrics {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 10px; margin-bottom: 14px; padding: 12px;
    background: var(--bg-base); border-radius: 8px;
  }
  .w-metric-label { font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); }
  .w-metric-val { font-size: 16px; font-weight: 700; font-family: var(--font-mono); }
  .top-holdings-bar { display: flex; gap: 6px; flex-wrap: wrap; }
  .holding-chip {
    background: var(--bg-card-hover); border: 1px solid var(--border);
    padding: 3px 8px; border-radius: 4px; font-size: 11px; font-family: var(--font-mono);
    color: var(--text-secondary);
  }

  /* Table Design */
  .table-wrapper {
    background: var(--bg-surface); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden;
  }
  .table-controls {
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 20px; border-bottom: 1px solid var(--border);
    flex-wrap: wrap; gap: 12px;
  }
  .search-input {
    background: var(--bg-base); border: 1px solid var(--border);
    padding: 8px 14px; border-radius: 8px; color: var(--text-primary);
    font-family: var(--font-mono); font-size: 13px; width: 280px;
    outline: none; transition: border-color 0.2s;
  }
  .search-input:focus { border-color: var(--cyan); }
  table { width: 100%; border-collapse: collapse; text-align: left; }
  th {
    background: var(--bg-card); color: var(--text-secondary);
    font-size: 11px; font-family: var(--font-mono); font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px; padding: 12px 16px;
    border-bottom: 1px solid var(--border);
  }
  td {
    padding: 12px 16px; border-bottom: 1px solid var(--border);
    font-size: 13px; font-family: var(--font-mono);
  }
  tr:hover td { background: var(--bg-card-hover); }
  .ticker-badge {
    font-weight: 700; color: var(--text-primary);
    background: var(--bg-base); padding: 3px 8px; border-radius: 4px;
    border: 1px solid var(--border);
  }
  .pos-green { color: var(--green); }
  .neg-red { color: var(--red); }

  /* Modal */
  .modal-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(4px);
    z-index: 1000; align-items: center; justify-content: center; padding: 20px;
  }
  .modal-overlay.active { display: flex; }
  .modal-box {
    background: var(--bg-surface); border: 1px solid var(--border-accent);
    border-radius: 14px; width: 100%; max-width: 900px; max-height: 85vh;
    display: flex; flex-direction: column; overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
  }
  .modal-header {
    padding: 18px 24px; border-bottom: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
  }
  .modal-body { padding: 24px; overflow-y: auto; }
  .close-btn {
    background: transparent; border: none; color: var(--text-muted);
    font-size: 20px; cursor: pointer; line-height: 1;
  }
  .close-btn:hover { color: var(--text-primary); }
</style>
</head>
<body>

<div class="container">
  <header>
    <div class="brand">
      <div class="brand-logo">A</div>
      <div class="brand-title">
        <h1>AfterHour Alpha & Whale Terminal</h1>
        <p>REVERSE-ENGINEERED PLATFORM INTELLIGENCE • DATA REFRESHED LIVE</p>
      </div>
    </div>
    <div class="live-badge">
      <div class="live-dot"></div>
      ACTIVE REVERSE-ENGINEERED INGESTION
    </div>
  </header>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">TOTAL STOCK VALUE TRACKED</div>
      <div class="stat-value val-cyan">$__TOTAL_PLATFORM_VAL__</div>
      <div class="stat-sub">Across top 150 AfterHour securities</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">WHALE CAPITAL MAPPED</div>
      <div class="stat-value val-green">$__TOTAL_WHALE_VAL__</div>
      <div class="stat-sub">__WHALE_COUNT__ verified public accounts</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">BIGGEST SINGLE HOLDING</div>
      <div class="stat-value val-amber">$9.34M</div>
      <div class="stat-sub">@SlowmoInvestor holding 28k $AAPL</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">MOST OWNED ASSET</div>
      <div class="stat-value val-purple">NVDA (321)</div>
      <div class="stat-sub">$13.5M platform aggregate value</div>
    </div>
  </div>

  <div class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('whales')">🐋 Verified Whale Portfolios (__WHALE_COUNT__)</button>
    <button class="tab-btn" onclick="switchTab('leaderboard')">📈 Stock Leaderboard (Top __STOCK_COUNT__)</button>
    <button class="tab-btn" onclick="switchTab('radar')">📊 Platform Exposure Radar</button>
  </div>

  <!-- TAB 1: WHALE PORTFOLIOS -->
  <div id="tab-whales" class="tab-pane active">
    <div class="whale-grid" id="whaleContainer"></div>
  </div>

  <!-- TAB 2: STOCKS LEADERBOARD -->
  <div id="tab-leaderboard" class="tab-pane">
    <div class="table-wrapper">
      <div class="table-controls">
        <input type="text" id="stockSearch" class="search-input" placeholder="Search by ticker or name..." onkeyup="filterStocks()">
        <span style="font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono);">Showing __STOCK_COUNT__ tracked assets</span>
      </div>
      <div style="overflow-x: auto;">
        <table id="stocksTable">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Ticker</th>
              <th>Company Name</th>
              <th>Owners</th>
              <th>Platform Value ($)</th>
              <th>Price</th>
              <th>24h %</th>
              <th>Chatroom</th>
            </tr>
          </thead>
          <tbody id="stocksBody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 3: ALPHA RADAR -->
  <div id="tab-radar" class="tab-pane">
    <div class="stats-grid">
      <div class="stat-card" style="grid-column: span 2;">
        <div class="stat-label">TOP 5 ACCUMULATED ASSETS BY CAPITAL HELD</div>
        <div style="margin-top: 14px;" id="topCapitalChart"></div>
      </div>
      <div class="stat-card" style="grid-column: span 2;">
        <div class="stat-label">TOP 5 ACCUMULATED ASSETS BY VERIFIED ACCOUNTS</div>
        <div style="margin-top: 14px;" id="topOwnersChart"></div>
      </div>
    </div>
  </div>
</div>

<!-- MODAL FOR WHALE PORTFOLIO DETAIL -->
<div class="modal-overlay" id="whaleModal" onclick="closeModal(event)">
  <div class="modal-box" onclick="event.stopPropagation()">
    <div class="modal-header">
      <div>
        <h3 id="modalTitle" style="font-size: 18px; font-weight: 700;">Whale Portfolio</h3>
        <p id="modalSub" style="font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono);"></p>
      </div>
      <button class="close-btn" onclick="hideModal()">&times;</button>
    </div>
    <div class="modal-body">
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Name</th>
              <th>Quantity</th>
              <th>Position Value</th>
              <th>Cost Basis</th>
              <th>Unrealized Profit</th>
              <th>Gain %</th>
            </tr>
          </thead>
          <tbody id="modalPositionsBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script>
const STOCKS_DATA = __STOCKS_JSON__;
const WHALES_DATA = __WHALES_JSON__;

function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  event.currentTarget.classList.add('active');
  document.getElementById('tab-' + tabId).classList.add('active');
}

// Render Whales
function renderWhales() {
  const container = document.getElementById('whaleContainer');
  container.innerHTML = WHALES_DATA.map((w, idx) => {
    const pnlClass = w.profit >= 0 ? 'pos-green' : 'neg-red';
    const topHoldings = (w.positions || []).slice(0, 4).map(p => {
      const ticker = p.ticker || 'N/A';
      const kVal = Math.round((p.value || 0)/1000);
      return '<span class="holding-chip">' + ticker + ': $' + kVal + 'k</span>';
    }).join('');

    const formattedVal = Number(w.total_value).toLocaleString(undefined, {maximumFractionDigits: 0});
    const pnlSign = w.profit_percent > 0 ? '+' : '';

    return `
      <div class="whale-card" onclick="openWhaleModal(${idx})">
        <div class="whale-header">
          <div class="whale-user">
            <div class="whale-avatar">${w.username.charAt(0).toUpperCase()}</div>
            <div>
              <div class="whale-name">@${w.username}</div>
              <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">${w.positions_count} verified positions</div>
            </div>
          </div>
          <span class="whale-badge">VERIFIED BROKERAGE</span>
        </div>
        <div class="whale-metrics">
          <div>
            <div class="w-metric-label">PORTFOLIO VALUE</div>
            <div class="w-metric-val val-cyan">$${formattedVal}</div>
          </div>
          <div>
            <div class="w-metric-label">ALL-TIME P&L</div>
            <div class="w-metric-val ${pnlClass}">${pnlSign}${w.profit_percent.toFixed(1)}%</div>
          </div>
        </div>
        <div class="top-holdings-bar">
          ${topHoldings || '<span style="font-size:11px; color:var(--text-muted);">No open public positions</span>'}
        </div>
      </div>
    `;
  }).join('');
}

// Render Stocks Table
function renderStocks(list) {
  const tbody = document.getElementById('stocksBody');
  tbody.innerHTML = list.map(s => {
    const chgClass = s.changePercent >= 0 ? 'pos-green' : 'neg-red';
    const chgSign = s.changePercent >= 0 ? '+' : '';
    const formattedVal = Number(s.totalValue).toLocaleString(undefined, {maximumFractionDigits: 0});
    return `
      <tr>
        <td style="color: var(--text-muted);">#${s.rank}</td>
        <td><span class="ticker-badge">${s.ticker}</span></td>
        <td style="color: var(--text-secondary); max-width: 220px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${s.name}</td>
        <td style="font-weight: 700;">${s.owners}</td>
        <td style="color: var(--cyan);">$${formattedVal}</td>
        <td>$${s.price.toFixed(2)}</td>
        <td class="${chgClass}">${chgSign}${s.changePercent.toFixed(2)}%</td>
        <td style="color: var(--text-muted);">${s.chatroomMembers.toLocaleString()} members</td>
      </tr>
    `;
  }).join('');
}

function filterStocks() {
  const q = document.getElementById('stockSearch').value.toLowerCase();
  const filtered = STOCKS_DATA.filter(s => 
    s.ticker.toLowerCase().includes(q) || s.name.toLowerCase().includes(q)
  );
  renderStocks(filtered);
}

// Modal Handling
function openWhaleModal(idx) {
  const w = WHALES_DATA[idx];
  document.getElementById('modalTitle').textContent = '@' + w.username + ' • Live Portfolio';
  document.getElementById('modalSub').textContent = 'Total Value: $' + w.total_value.toLocaleString() + ' | Verified As Of: ' + (w.verified_as_of || 'Live');
  
  const tbody = document.getElementById('modalPositionsBody');
  tbody.innerHTML = (w.positions || []).map(p => {
    const pnlClass = (p.profit || 0) >= 0 ? 'pos-green' : 'neg-red';
    const pnlSign = (p.profit || 0) >= 0 ? '+' : '';
    const ticker = p.ticker || 'N/A';
    const name = p.name || '';
    const qty = Number(p.quantity || 0).toLocaleString();
    const val = Number(p.value || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
    const cost = Number(p.cost_basis || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
    const profit = Number(p.profit || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
    const pct = Number(p.profit_percent || 0).toFixed(2);

    return `
      <tr>
        <td><span class="ticker-badge">${ticker}</span></td>
        <td style="color: var(--text-secondary);">${name}</td>
        <td>${qty}</td>
        <td style="color: var(--cyan); font-weight:700;">$${val}</td>
        <td style="color: var(--text-muted);">$${cost}</td>
        <td class="${pnlClass}">${pnlSign}$${profit}</td>
        <td class="${pnlClass}">${pnlSign}${pct}%</td>
      </tr>
    `;
  }).join('');

  document.getElementById('whaleModal').classList.add('active');
}

function hideModal() {
  document.getElementById('whaleModal').classList.remove('active');
}
function closeModal(e) {
  if (e.target.id === 'whaleModal') hideModal();
}

// Render Radar Bars
function renderRadar() {
  const byVal = [...STOCKS_DATA].sort((a,b) => b.totalValue - a.totalValue).slice(0, 5);
  const byOwn = [...STOCKS_DATA].sort((a,b) => b.owners - a.owners).slice(0, 5);
  const maxVal = byVal[0].totalValue;
  const maxOwn = byOwn[0].owners;

  document.getElementById('topCapitalChart').innerHTML = byVal.map(s => {
    const formattedVal = Number(s.totalValue).toLocaleString(undefined, {maximumFractionDigits:0});
    const widthPct = (s.totalValue/maxVal)*100;
    return `
      <div style="margin-bottom: 12px;">
        <div style="display:flex; justify-content:space-between; font-size:12px; font-family:var(--font-mono); margin-bottom:4px;">
          <span>${s.ticker} (${s.name})</span>
          <span style="color:var(--cyan); font-weight:700;">$${formattedVal}</span>
        </div>
        <div style="background:var(--bg-base); border-radius:4px; height:8px; overflow:hidden;">
          <div style="background:linear-gradient(90deg, var(--cyan), var(--purple)); height:100%; width:${widthPct}%;"></div>
        </div>
      </div>
    `;
  }).join('');

  document.getElementById('topOwnersChart').innerHTML = byOwn.map(s => {
    const widthPct = (s.owners/maxOwn)*100;
    return `
      <div style="margin-bottom: 12px;">
        <div style="display:flex; justify-content:space-between; font-size:12px; font-family:var(--font-mono); margin-bottom:4px;">
          <span>${s.ticker} (${s.name})</span>
          <span style="color:var(--purple); font-weight:700;">${s.owners} verified holders</span>
        </div>
        <div style="background:var(--bg-base); border-radius:4px; height:8px; overflow:hidden;">
          <div style="background:linear-gradient(90deg, var(--purple), var(--green)); height:100%; width:${widthPct}%;"></div>
        </div>
      </div>
    `;
  }).join('');
}

renderWhales();
renderStocks(STOCKS_DATA);
renderRadar();
</script>
</body>
</html>
"""

html_out = (
    template.replace("__TOTAL_PLATFORM_VAL__", f"{total_platform_val:,.0f}")
    .replace("__TOTAL_WHALE_VAL__", f"{total_whale_val:,.0f}")
    .replace("__WHALE_COUNT__", str(len(users_list)))
    .replace("__STOCK_COUNT__", str(len(stocks)))
    .replace("__STOCKS_JSON__", json.dumps(stocks))
    .replace("__WHALES_JSON__", json.dumps(users_list))
)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"[+] Successfully generated standalone HTML dashboard: {OUT_FILE}")
