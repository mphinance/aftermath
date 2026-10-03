# AfterMath Quantitative Alt-Data API Reference

> Sub-millisecond, edge-cached alternative financial intelligence API tracking verified retail & whale equity, conviction intensity ($/holder), whale dry powder cash, and macro tape liquidity from the AfterHour social terminal.
> 
> Production URL: **https://ah.mphinance.com**  
> Interactive Swagger Explorer: **https://ah.mphinance.com/docs**  
> OpenAPI 3.1 Specification: **https://ah.mphinance.com/api/openapi.json**  
> Model Context Protocol (MCP) Server: **https://ah.mphinance.com/mcp**

---

## ⚡ Global API Characteristics

- **Zero Authentication Required**: All endpoints are public and open.
- **Edge Cached**: Hosted on Coolify high-performance Nginx with HTTP/2 and gzip compression.
- **Unrestricted CORS**: `Access-Control-Allow-Origin: *` is enabled across all endpoints for direct browser, Node.js, Python, and agent loop execution.
- **Sub-Millisecond Response**: Pre-computed static and dynamic JSON edge files return in ~10 to 25ms globally.

---

## 📡 Endpoints Catalog

### 1. Real-Time Alt-Data Market Radar
- **Path**: `GET /api/market.json` (alias: `GET /api/market-summary.json`)
- **Description**: Returns live macro tape overview, whale dry powder cash reserves, net intraday profit/loss, asset class allocation ratio (Equities vs. ETFs), and leaders across capital inflows, retail breadth, and conviction intensity.
- **Sample Request**:
  ```bash
  curl -sL https://ah.mphinance.com/api/market.json
  ```
- **Response Structure**:
  ```json
  {
    "version": "1.0.0",
    "timestamp": "2026-10-02T23:15:00Z",
    "source": "https://ah.mphinance.com",
    "macro": {
      "whaleDryPowderCash": 8984781.39,
      "whaleNetGainToday": 3487492.28,
      "whaleUnrealizedProfit": 21893412.10,
      "totalWhaleAum": 169340582.45,
      "trackedWhalesCount": 395,
      "allocation": {
        "equityValue": 88523910.12,
        "equityPercent": 79.9,
        "etfValue": 22284109.80,
        "etfPercent": 20.1
      }
    },
    "capitalInflowLeaders": [
      { "ticker": "AAPL", "name": "Apple Inc.", "totalValue": 19355088.19, "whaleCapital": 18421012.00, "owners": 179 }
    ],
    "retailBreadthLeaders": [
      { "ticker": "NVDA", "name": "NVIDIA Corporation", "owners": 321, "totalValue": 13495819.00 }
    ],
    "convictionIntensityLeaders": [
      { "ticker": "ANET", "name": "Arista Networks Inc.", "convictionPerHolder": 188752.00, "owners": 18 }
    ],
    "topTapeGainers": [
      { "ticker": "RKLB", "name": "Rocket Lab USA Inc.", "changePercent": 4.90 }
    ]
  }
  ```

---

### 2. All 500 Verified Equities & ETFs
- **Path**: `GET /api/stonks.json`
- **Description**: Complete leaderboard of 500 securities enriched with verified owner counts, total value on app, whale capital backing, conviction intensity ($/sub), session price changes, and chatroom activity.
- **Sample Request**:
  ```bash
  curl -sL https://ah.mphinance.com/api/stonks.json
  ```
- **Key Fields per Security**:
  - `ticker`: Stock or ETF ticker symbol (e.g. `NVDA`, `ASTS`).
  - `name`: Clean resolved company or asset name.
  - `price`: Live session last price.
  - `changePercent`: 24-hour percentage price change.
  - `isETF`: Boolean flag segregating ETFs from equities.
  - `whalesValue`: Aggregate capital held by verified tracked whales in USD.
  - `totalValue`: Platform-wide aggregate equity tracked on AfterHour in USD.
  - `owners`: Verified accounts holding this ticker.
  - `intensity`: Conviction Intensity metric (`totalValue / owners`) representing average position size per holder.
  - `chatroomMembers`: Active members in the ticker's chatroom.

---

### 3. All 64 Verified ETFs & Index Funds
- **Path**: `GET /api/etfs.json`
- **Description**: Segregated catalog of 64 index funds, leveraged ETFs, thematic plays, and crypto trusts (`SPY`, `QQQ`, `VOO`, `IBIT`, `SMH`, `SGOV`, `MSTU`, etc.).
- **Sample Request**:
  ```bash
  curl -sL https://ah.mphinance.com/api/etfs.json
  ```

---

### 4. 395 Verified Whales & Millionaires
- **Path**: `GET /api/whales.json`
- **Description**: Full directory of 395 verified portfolios controlling **$169,001,648.72** in verified tracked equity, including 31 verified millionaires.
- **Sample Request**:
  ```bash
  curl -sL https://ah.mphinance.com/api/whales.json
  ```
- **Whale Profile Schema**:
  - `username`: Clean username without `@`.
  - `total_value`: Broker-verified equity balance in USD.
  - `cash_balance`: Uninvested cash reserves (dry powder).
  - `profit_today`: Intraday net P&L.
  - `profit`: Total unrealized gain/loss across open positions.
  - `followers`: Social follower count on the app.
  - `shadow_ratio`: The Clout Inversion metric (`total_value / followers`).
  - `all_positions`: Array of all verified holdings (ticker, company name, quantity, value, cost basis, profit).

---

### 5. Shadow Whales (Clout Inversion Index)
- **Path**: `GET /api/shadow.json`
- **Description**: Ranked directory of whales sorted by **Shadow Ratio** (`total_value / followers`). Unmasks quiet capital: accounts holding millions of dollars with single/double-digit followers.
- **Sample Request**:
  ```bash
  curl -sL https://ah.mphinance.com/api/shadow.json
  ```

---

### 6. Granular Ticker Intelligence & 90-Day Daily Bars
- **Path**: `GET /api/ticker/:symbol.json` (e.g. `/api/ticker/NVDA.json`, `/api/ticker/ASTS.json`)
- **Description**: Granular security dossier containing:
  1. Detailed profile and quantitative metrics.
  2. List of verified whale accounts holding the ticker (shares, value, cost basis, profit).
  3. 90-day daily OHLCV candlestick price bars (`open`, `high`, `low`, `close`, `volume`, `volumeWeightedAveragePrice`, `timestamp`).
- **Sample Request**:
  ```bash
  curl -sL https://ah.mphinance.com/api/ticker/ASTS.json
  ```

---

### 7. Direct JSON-RPC MCP Endpoint
- **Path**: `POST /api/mcp`
- **Description**: Direct JSON-RPC 2.0 endpoint for executing Model Context Protocol tools without needing an SSE connection.
- **Sample Request**:
  ```bash
  curl -s -X POST https://ah.mphinance.com/api/mcp \
    -H "Content-Type: application/json" \
    -d '{
      "jsonrpc": "2.0",
      "id": 1,
      "method": "tools/call",
      "params": {
        "name": "get_ticker_intel",
        "arguments": { "ticker": "ASTS" }
      }
    }'
  ```

---

### 8. Remote Model Context Protocol (MCP) SSE Transport
- **SSE Stream**: `GET https://ah.mphinance.com/sse`
- **Message Receiver**: `POST https://ah.mphinance.com/messages?sessionId=<session_id>`
- **Description**: Full bidirectional SSE transport conforming to MCP specification `2024-11-05`. Compatible with `mcp-remote`, Cursor, Claude Desktop, and Antigravity.
- **Client Connect**:
  ```bash
  npx -y mcp-remote https://ah.mphinance.com/sse
  ```

---

### 9. Health & MCP Status Check
- **Path**: `GET /health` (aliases: `GET /api/health`, `GET /status`, `HEAD /health`)
- **Description**: Returns server health, uptime in seconds, supported MCP protocol versions (`2025-06-18`, `2025-03-26`, `2024-11-05`), endpoints manifest, and registered tools count.
- **Sample Request**:
  ```bash
  curl -sL https://ah.mphinance.com/health
  ```
- **Response**:
  ```json
  {
    "status": "ok",
    "server": "aftermath-altdata",
    "version": "1.1.0",
    "protocols": ["2025-06-18", "2025-03-26", "2024-11-05"],
    "endpoints": {
      "streamable_http": "/api/mcp",
      "sse": "/sse",
      "messages": "/messages?sessionId={id}",
      "direct_rpc": "/api/mcp",
      "health": "/health"
    },
    "uptime_seconds": 42.5,
    "tools_count": 6
  }
  ```

---

### 10. OpenAPI Specification & MCP Tool Schemas
- `GET /api/openapi.json`: Complete OpenAPI 3.1.0 JSON document.
- `GET /api/mcp-schema.json`: Complete Model Context Protocol tool and resource manifest.
- `GET /sitemap.xml`: Standard XML sitemap with 616 indexed routes.

