# AfterMath Model Context Protocol (MCP) Server Reference

> Production-grade, zero-dependency MCP server providing direct AI agent access to verified retail and whale alt-data, conviction intensity ($/holder), portfolio holdings, ETF allocations, and real-time liquidity from the AfterHour social trading terminal.
> 
> Production SSE URL: **https://ah.mphinance.com/sse**  
> Direct JSON-RPC URL: **https://ah.mphinance.com/api/mcp**  
> Interactive Web Portal: **https://ah.mphinance.com/mcp**  
> REST API Reference: [API.md](API.md)  
> OpenAPI Specification: **https://ah.mphinance.com/api/openapi.json**

---

## ⚡ Architecture & Transports

AfterMath MCP supports multiple standard transports out of the box with zero external Python dependencies:

1. **Remote SSE (Server-Sent Events) via `mcp-remote`**:
   Legacy HTTP+SSE transport conforming to MCP specification `2024-11-05`. Connect any desktop or CLI agent over HTTPS without downloading code or running local daemons. Note: clients that dropped `2024-11-05` (such as Google Antigravity) must reach this through the `mcp-remote` stdio bridge rather than a native `url` config.
2. **Direct JSON-RPC over HTTP POST**:
   Send standard JSON-RPC 2.0 requests directly to `https://ah.mphinance.com/api/mcp` without maintaining long-lived SSE connections. Ideal for stateless agent loops, serverless functions, or quick terminal audits.
3. **Local Stdio Transport**:
   Run `python3 mcp_server.py` locally from the repository. Communicates directly over standard input/output using standard JSON-RPC 2.0 lines.
4. **Local HTTP / SSE Transport**:
   Run `python3 mcp_server.py --port 8089` to host your own local SSE proxy or development cluster.

---

## 🚀 Quick Connect & Configuration

### 1. Instant Connection via `mcp-remote`

The fastest way to test or attach AfterMath to your AI workflow:

```bash
npx -y mcp-remote https://ah.mphinance.com/sse
```

This proxy negotiates the remote SSE session and presents a clean stdio JSON-RPC interface to the calling process.

---

### 2. Claude Desktop Setup

Open your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the `aftermath` server definition:

```json
{
  "mcpServers": {
    "aftermath": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://ah.mphinance.com/sse"
      ]
    }
  }
}
```

#### Alternative: Local Stdio Setup (Repository Clone)

If you have cloned the repository locally:

```json
{
  "mcpServers": {
    "aftermath-local": {
      "command": "python3",
      "args": [
        "/absolute/path/to/aftermath/mcp_server.py"
      ]
    }
  }
}
```

---

### Claude Code

```bash
claude mcp add --transport http aftermath https://ah.mphinance.com/api/mcp
```

---

### 3. Cursor IDE Setup

In your project root or user config directory, create or edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aftermath": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://ah.mphinance.com/sse"
      ]
    }
  }
}
```

Restart Cursor or click **Refresh** in Cursor Settings > MCP to discover every tool (see the reference below).

---

### 4. Google Antigravity (AGY) Setup

> **Which client?** The standalone `gemini` CLI is on its way out: its free
> personal OAuth tier now fails with
> `IneligibleTierError: This client is no longer supported for Gemini Code Assist for individuals`.
> The supported successor is **Google Antigravity**, which reads a different
> config file and speaks different transports. The instructions below target
> Antigravity.

#### Transports Antigravity supports

Antigravity's MCP client supports **only** these two transports:

| Transport | Config key | Notes |
|---|---|---|
| **Stdio** | `command` + `args` | Local process speaking JSON-RPC on stdin/stdout. |
| **Streamable HTTP** (spec `2025-03-26`) | `url` | Remote endpoint, usually `/mcp`. |

**The legacy HTTP+SSE transport (spec `2024-11-05`, i.e. `/sse`) is NOT
supported.** Pointing `url` at `/sse` will fail. For a server that only speaks
legacy SSE, run the `mcp-remote` bridge as a **Stdio** server instead.

#### Protocol version negotiation

Antigravity requires a protocol version of **`2025-03-26` or newer**. The server
now echoes the client's requested `protocolVersion` when it is in
`{2025-06-18, 2025-03-26, 2024-11-05}` and otherwise replies with its newest
supported version. A server that hard-codes `2024-11-05` is rejected by
Antigravity with:

```
MCP server connection closed unexpectedly for aftermath: invalid request
```

#### Config file: `~/.gemini/config/mcp_config.json`

Register the server once. The cleanest option is the native Streamable HTTP
endpoint (no Node, no local process):

```json
{
  "mcpServers": {
    "aftermath": { "url": "https://ah.mphinance.com/api/mcp" }
  }
}
```

`/api/mcp` is a stateless Streamable HTTP endpoint: it answers requests with
`application/json`, acknowledges notification-only POSTs with an empty `202`,
and replies `405` to `GET` (no server-initiated stream).

Alternatives, if you would rather run locally or bridge the legacy SSE stream:

```json
{
  "mcpServers": {
    "aftermath-local": {
      "command": "python3",
      "args": ["/absolute/path/to/aftermath/mcp_server.py"]
    },
    "aftermath-remote": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://ah.mphinance.com/sse"]
    }
  }
}
```

- `aftermath-local` runs the repository copy directly over stdio (no Node required).
- `aftermath-remote` bridges the legacy edge SSE endpoint to stdio via `mcp-remote`.

Native tool definitions are cached under `~/.gemini/antigravity-cli/mcp/aftermath/`.

#### Legacy `gemini` CLI (deprecated)

The `gemini` CLI still parses SSE servers, so `gemini mcp list` can report
`✓ aftermath ... (sse) - Connected`. That is a transport-level check only, and
it no longer implies the CLI is usable: interactive calls fail at
authentication because Google retired the personal Code Assist tier for this
client. Migrate to Antigravity, or authenticate the CLI with an API key
(`GEMINI_API_KEY`) instead of `oauth-personal`.

---

### 5. Google Gemini Web App (`gemini.google.com`) Setup

Google Gemini now supports adding custom apps backed by Model Context Protocol (MCP) servers directly in the consumer web interface at [gemini.google.com](https://gemini.google.com).

#### Why "The MCP server could not be reached. Check the URL" Happened
1. **Gemini Web does NOT support SSE (`/sse`)**: Gemini Web exclusively uses the modern **Streamable HTTP** transport (spec `2025-03-26`). Entering `https://ah.mphinance.com/sse` fails immediately with *"The MCP server could not be reached. Check the URL."*
2. **Protocol version negotiation**: Gemini Web sends initialization probes expecting a negotiated protocol version (`2025-03-26` or `2025-06-18`). The live server at `https://ah.mphinance.com/api/mcp` now fully negotiates this.

#### Exact URL to Use in Gemini Web
```text
https://ah.mphinance.com/api/mcp
```

#### Step-by-Step Connection Guide
1. Navigate to **[gemini.google.com](https://gemini.google.com)** on your desktop browser.
2. At the bottom of the left sidebar, click **Settings & help** (or **Settings**).
3. Select **Connected Apps** (if not visible directly, look under **Personal Intelligence** > **Connected Apps**).
4. In the **Custom apps** section, click **Add a custom app**.
5. Paste the Streamable HTTP server URL:
   ```text
   https://ah.mphinance.com/api/mcp
   ```
6. Click **Next** / **Connect**. Since AfterMath is completely open, zero-auth financial intelligence, no OAuth or API keys are required.
7. Once connected, invoke the tools in your Gemini chats:
   - *"@aftermath What are the top 5 high-conviction stocks held by verified whales?"*
   - *"@aftermath What is the current dry powder cash across tracked whales?"*
   - *"@aftermath Show me the verified portfolio for @SirJackALot."*

---

### 6. Direct JSON-RPC HTTP POST (No SSE Required)

For autonomous scripts, curl, or serverless execution, execute tools directly:

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

## 🛠️ Complete Tools Reference

Generated from `mcp_server.py` by `scripts/gen_openapi.py`; never edit between the markers.

<!-- BEGIN GENERATED -->
**16 tools**, generated from `mcp_server.py` (`api/mcp-schema.json`).

### 1. `get_market_tape`

Retrieve real-time macro tape overview: whale cash reserves (dry powder), intraday net P&L, equity/ETF allocation split, and top capital inflow & retail breadth leaders from AfterHour terminal.

_No parameters._

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_market_tape", "arguments": {}}}'
```

### 2. `get_top_equities`

Filter and rank 500 verified stocks with customizable thresholds for whale capital, owner count, conviction intensity ($/holder), price movement, and asset type segregation.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Maximum number of items to return (default: 20, max: 100) Default `20`. |
| `min_whale_capital` | number | no | Minimum verified capital held by tracked whales in USD (e.g. 1000000 for $1M+) Default `0`. |
| `min_conviction` | number | no | Minimum verified position size per holder in USD (e.g. 50000 for $50k+/sub) Default `0`. |
| `min_owners` | integer | no | Minimum number of verified holders on the app Default `0`. |
| `asset_type` | string | no | Segregate by asset classification (default: 'all') One of: `all`, `stocks`, `etfs`. Default `"all"`. |
| `sort_by` | string | no | Metric to rank results by (default: 'whale_capital') One of: `whale_capital`, `total_value`, `owners`, `conviction`, `change_percent`. Default `"whale_capital"`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_top_equities", "arguments": {"limit": 20, "min_whale_capital": 0, "min_conviction": 0, "min_owners": 0, "asset_type": "all", "sort_by": "whale_capital"}}}'
```

### 3. `get_etf_flows`

Inspect 64 ETFs & index funds ranked by whale backing, expense ratios, asset classes (equity, broad market, thematic, crypto, fixed income), and retail crowd adoption.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | integer | no | Maximum ETFs to return (default: 20) Default `20`. |
| `sort_by` | string | no | Metric to rank ETFs by (default: 'whale_capital') One of: `whale_capital`, `owners`, `total_value`, `change_percent`. Default `"whale_capital"`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_etf_flows", "arguments": {"limit": 20, "sort_by": "whale_capital"}}}'
```

### 4. `get_whale_portfolio`

Look up any verified whale account by username (e.g. 'thealexperez', 'SirJackALot', 'MisterMonster') to inspect verified positions, cost basis, unrealized profit, cash balance, and shadow ratio. Set live=true for positions marked to current prices (60s cache, any PUBLIC portfolio); it includes last_synced_at, because quantities are only as fresh as the broker sync, often months old.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | string | yes | AfterHour username of the whale to audit (with or without '@') |
| `live` | boolean | no | Fetch current marked positions from AfterHour instead of the cached census Default `false`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_whale_portfolio", "arguments": {"username": "skrt", "live": false}}}'
```

### 5. `get_ticker_intel`

Forensic intelligence on any ticker ($NVDA, $ASTS, $AAPL, etc.) with verified holders, conviction intensity ($/sub), top whale holders breakdown, and optional 90-day daily OHLCV bars.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | yes | Stock or ETF ticker symbol (e.g. 'ASTS', 'NVDA', 'AAPL', 'QQQ') |
| `include_bars` | boolean | no | Set to true to include the 90-day daily OHLCV candlestick price bars series Default `false`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_ticker_intel", "arguments": {"ticker": "NVDA", "include_bars": false}}}'
```

### 6. `screen_whales`

Filter and rank 424 broker-verified whales and millionaires by net worth, cash reserves, unrealized profit, daily return, follower counts, and shadow ratio.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `min_net_worth` | number | no | Minimum verified portfolio value in USD (e.g. 1000000 for $1M+) Default `0`. |
| `min_cash` | number | no | Minimum uninvested cash balance in USD (dry powder) Default `0`. |
| `min_profit` | number | no | Minimum total unrealized profit in USD Default `0`. |
| `min_profit_pct` | number | no | Minimum profit percentage (e.g. 25 for +25%) Default `0`. |
| `min_followers` | integer | no | Minimum social followers on the platform Default `0`. |
| `max_followers` | integer | no | Maximum social followers (useful for filtering stealth whales) |
| `sort_by` | string | no | Metric to rank whales by (default: 'net_worth') One of: `net_worth`, `cash`, `profit`, `profit_percent`, `profit_today`, `followers`, `shadow_ratio`. Default `"net_worth"`. |
| `limit` | integer | no | Maximum number of whales to return (default: 20, max: 100) Default `20`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "screen_whales", "arguments": {"min_net_worth": 0, "min_cash": 0, "min_profit": 0, "min_profit_pct": 0, "min_followers": 0, "sort_by": "net_worth", "limit": 20}}}'
```

### 7. `get_shadow_whales`

Scan for Clout Inversions and stealth accounts: verified traders holding high capital ($500k+ to $15M+) with negligible retail followings (<500 followers).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `min_capital` | number | no | Minimum verified capital in USD (default: 500000) Default `500000`. |
| `max_followers` | integer | no | Maximum allowed follower count (default: 500) Default `500`. |
| `min_shadow_ratio` | number | no | Minimum verified capital divided by followers (default: 2000) Default `2000`. |
| `limit` | integer | no | Maximum number of shadow whales to return (default: 20) Default `20`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_shadow_whales", "arguments": {"min_capital": 500000, "max_followers": 500, "min_shadow_ratio": 2000, "limit": 20}}}'
```

### 8. `get_social_feed`

Retrieve real-time community posts, commentary, sentiment, and broker-verified trade snapshots from AfterHour traders.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | no | Filter posts mentioning a specific ticker (e.g. 'NVDA' or 'ASTS') |
| `username` | string | no | Filter posts authored by a specific trader handle |
| `limit` | integer | no | Maximum number of posts to return (default: 20, max: 50) Default `20`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_social_feed", "arguments": {"ticker": "NVDA", "username": "skrt", "limit": 20}}}'
```

### 9. `get_funnel_accounts`

Look up AfterHour accounts flagged for funneling traders into Telegram channels, with evidence tier (reported/corroborated/verified), shared invite-link clusters, and posting stats. Check a username or t.me link before you join. Flagged for investigation, not a finding of fraud. Curated by https://telegramscammers.com (database: /database, submit intel: /submit).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `username` | string | no | AfterHour username (substring match) |
| `telegram_link` | string | no | t.me link or handle to look up (e.g. 't.me/gammasphere47') |
| `tier` | string | no | Filter by evidence tier One of: `reported`, `corroborated`, `verified`. |
| `limit` | integer | no | Max accounts to return (default 25, max 100) Default `25`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_funnel_accounts", "arguments": {"username": "skrt", "limit": 25}}}'
```

### 10. `get_funnel_callouts`

Parsed trade callouts, plus the most called-out tickers overall when unfiltered (ticker, side, strike, expiry, entry, action, quoted result) from public Telegram channels linked to flagged AfterHour accounts, with an independent scored 'outcome' where available. Quoted results are the channel's own claims, and the sample is small. Flagged for investigation, not a finding of fraud. Curated by https://telegramscammers.com.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | no | Ticker symbol, e.g. 'SPY' |
| `channel` | string | no | Channel handle or t.me link (substring match) |
| `action` | string | no | Filter by callout action One of: `open`, `close`, `mention`. |
| `limit` | integer | no | Max callouts to return (default 25, max 100) Default `25`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_funnel_callouts", "arguments": {"ticker": "NVDA", "limit": 25}}}'
```

### 11. `get_funnel_scorecard`

Public scoring results for trade callouts posted by Telegram channels linked to flagged AfterHour accounts. Section 'paths' (the main view): what each called-out option contract did after the post, from its own 5-minute trade bars (calls posted in the session get the next 30 minutes, daily callouts the whole next session; fill = open of the first bar at or after the post): share that ended above the fill, median peak and drawdown, +50%/-50% TP-first versus SL-first, fill-delay sensitivity, unfillable-quote share, per channel, ticker and hour. Section 'options': the same callouts held to expiry (secondary view). Section 'fx': forex/gold/index signals (TP1 first versus SL first, mean R). Every rate carries its sample size and a Wilson 95% range; assumptions and limitations are included (trade prints, no spread or slippage). Analysis of public posts, not advice. Flagged for investigation, not a finding of fraud. Credit https://telegramscammers.com. Method: https://ah.mphinance.com/scorecard

| Parameter | Type | Required | Description |
|---|---|---|---|
| `section` | string | no | Which part to return: paths (price paths after the call), options (held to expiry), fx, or all (default all) One of: `paths`, `options`, `fx`, `all`. Default `"all"`. |
| `channel` | string | no | Channel handle or t.me link (substring match); filters the per-channel tables |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_funnel_scorecard", "arguments": {"section": "all"}}}'
```

### 12. `get_market_session`

LIVE (60s cache). Use for 'is the market open / what session is it / when does it close'. Returns current phase (pre, regular, after, overnight, closed), early-close flag, next transition and seconds until it, computed server-side in UTC.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | string | no | YYYY-MM-DD (default: today, US Eastern) |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_market_session", "arguments": {}}}'
```

### 13. `get_live_quotes`

LIVE (30s cache). Use for current price. Up to 25 symbols: last price, session change, pre-market and after-hours change, OHLC, volume. Percent fields are percent units (1.1 = 1.1%). Do NOT use for whale or conviction data (use get_ticker_intel).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbols` | array | yes | Ticker symbols, max 25 |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_live_quotes", "arguments": {"symbols": []}}}'
```

### 14. `get_leaderboard`

LIVE (2 min cache). Use for 'what is trending / most watched / top gainers / top losers' across the whole platform (~33k securities, crowd-ranked). Do NOT use for whale-capital ranking of the verified 500 (use get_top_equities). GAINERS only supports DAY. Percent fields are percent units.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sort` | string | no | One of: `TRENDING`, `WATCHERS`, `OWNERS`, `GAINERS`, `LOSERS`. Default `"TRENDING"`. |
| `time_range` | string | no | One of: `DAY`, `WEEK`, `MONTH`, `THREE_MONTH`, `YEAR_TO_DATE`. Default `"DAY"`. |
| `take` | integer | no | Max 50 Default `20`. |
| `cursor` | integer | no | Offset from a previous next_cursor Default `0`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_leaderboard", "arguments": {"sort": "TRENDING", "time_range": "DAY", "take": 20, "cursor": 0}}}'
```

### 15. `get_security_chart`

LIVE (5 min cache). OHLCV bars for any platform ticker at minute, hour, day, week or month resolution, up to 365 days back, last 500 bars. Use for any ticker's price history.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | yes |  |
| `timespan` | string | no | One of: `minute`, `hour`, `day`, `week`, `month`. Default `"day"`. |
| `multiplier` | integer | no | Bar size multiplier, max 60 Default `1`. |
| `days` | integer | no | Lookback in days, max 365 Default `30`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_security_chart", "arguments": {"symbol": "NVDA", "timespan": "day", "multiplier": 1, "days": 30}}}'
```

### 16. `get_retail_sentiment`

SNAPSHOT (refreshed every 5 min, public AfterHour posts). Retail stance. With a ticker: bull/bear votes, net score (-1..1), voting authors, confidence, calls vs puts opened, quality flags (duplicate text, low-follower share, Telegram-in-bio authors) and top posts. Without one, view=buzz ranks tickers by mention surge, view=divergence compares retail stance to verified whale capital, view=options_bias lists call/put activity. Direction comes only from explicit CALL/PUT plus an open verb, so most posts are neutral: always read n_voting_authors and confidence.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | no |  |
| `view` | string | no | One of: `ticker`, `buzz`, `divergence`, `options_bias`. |
| `window` | string | no | One of: `24h`, `72h`, `7d`. Default `"24h"`. |
| `limit` | integer | no | Default `15`. |

```bash
curl -s -X POST https://ah.mphinance.com/api/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_retail_sentiment", "arguments": {"ticker": "NVDA", "window": "24h", "limit": 15}}}'
```

### Resources

| URI | Name | Description |
|---|---|---|
| `aftermath://market-tape` | Live Market Tape & Liquidity | Real-time snapshot of whale cash reserves, net daily profit, and asset allocation. |
| `aftermath://top-stocks` | Top Verified Equities | Top 50 securities by verified whale capital. |
| `aftermath://etfs` | All 64 Verified ETFs | Complete list of ETFs with whale backing and asset classifications. |
| `aftermath://whales` | Top Verified Whales | Top 50 verified whales ranked by net worth. |
| `aftermath://shadow-whales` | Shadow Whales & Clout Inversions | Stealth traders with massive verified capital and minimal retail followings. |
| `aftermath://conviction` | Asymmetric Conviction Screener | Top securities ranked by verified position size per holder ($/sub). |
| `aftermath://social-feed` | Live Social Trade Feed | Recent verified community posts and live trade snapshots. |
<!-- END GENERATED -->

---

## 🐍 Python Agent Integration Example

Here is a lightweight Python snippet to call the AfterMath MCP server over HTTP JSON-RPC without installing any packages:

```python
import urllib.request
import json

def call_aftermath_mcp(tool_name: str, arguments: dict = None) -> dict:
    url = "https://ah.mphinance.com/api/mcp"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        if "error" in result:
            raise RuntimeError(result["error"].get("message"))
        return result.get("result", {})

# Example: Scan for highest conviction equities
data = call_aftermath_mcp("get_conviction_screener", {
    "min_intensity": 100000,
    "min_owners": 10,
    "limit": 5
})

for s in data.get("structuredContent", {}).get("results", []):
    print(f"{s['ticker']:<6} | Conviction: ${s['convictionPerHolder']:>10,.2f}/holder | Owners: {s['owners']}")
```

---

## 🔒 Security & Reliability

- **No Credentials Required**: All endpoints are public and read-only.
- **High Concurrency**: The live container runs in an isolated Python 3.12 Alpine environment fronted by Traefik and HTTP/2 SSL.
- **Safe Rate Limits**: Responses are edge cached with a 60-second in-memory TTL to prevent upstream load spikes.
