# AfterMath Model Context Protocol (MCP) Server Reference

> Production-grade, zero-dependency MCP server providing direct AI agent access to verified retail and whale alt-data, conviction intensity ($/holder), portfolio holdings, ETF allocations, and real-time liquidity from the AfterHour social trading terminal.
> 
> Production SSE URL: **https://ah.mphinance.com/sse**  
> Direct JSON-RPC URL: **https://ah.mphinance.com/api/mcp**  
> Interactive Web Portal: **https://ah.mphinance.com/mcp**  
> REST API Reference: [API.md](file:///home/mpha/projects/aftermath/docs/API.md)  
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
        "/home/mpha/projects/aftermath/mcp_server.py"
      ]
    }
  }
}
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

Restart Cursor or click **Refresh** in Cursor Settings > MCP to discover all 6 tools.

---

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

Register the server once, using either the local stdio server or the remote
bridge:

```json
{
  "mcpServers": {
    "aftermath": {
      "command": "python3",
      "args": ["/home/mpha/projects/aftermath/mcp_server.py"]
    },
    "aftermath-remote": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://ah.mphinance.com/sse"]
    }
  }
}
```

- `aftermath` runs the repository copy directly over stdio (no Node required).
- `aftermath-remote` bridges the edge SSE endpoint to stdio via `mcp-remote`.

Native tool definitions are cached under `~/.gemini/antigravity-cli/mcp/aftermath/`.

#### Legacy `gemini` CLI (deprecated)

The `gemini` CLI still parses SSE servers, so `gemini mcp list` can report
`✓ aftermath ... (sse) - Connected`. That is a transport-level check only, and
it no longer implies the CLI is usable: interactive calls fail at
authentication because Google retired the personal Code Assist tier for this
client. Migrate to Antigravity, or authenticate the CLI with an API key
(`GEMINI_API_KEY`) instead of `oauth-personal`.

---

### 5. Direct JSON-RPC HTTP POST (No SSE Required)

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

The server exposes 6 quantitative analysis tools.

### 1. `get_market_tape`
Retrieve real-time macro tape overview and liquidity from the AfterHour social terminal.

- **Description**: Returns live total verified whale assets under management, dry powder cash balances, net day gain, open unrealized profit, equity vs ETF allocation ratios, retail breadth leaders, capital inflow leaders, and conviction leaders.
- **Parameters**: None.
- **Sample Call**:
  ```json
  {
    "name": "get_market_tape",
    "arguments": {}
  }
  ```
- **Return Fields**:
  - `macro`: Aggregate stats (`totalWhaleAum`, `whaleDryPowderCash`, `whaleNetGainToday`, `whaleUnrealizedProfit`, `trackedWhalesCount`, `allocation`).
  - `capitalInflowLeaders`: Top tickers by total dollar capital.
  - `retailBreadthLeaders`: Top tickers by number of verified accounts.
  - `convictionIntensityLeaders`: Top tickers by average dollars per holder.
  - `topTapeGainers`: Top positive percentage price movers.

---

### 2. `get_top_equities`
Filter, rank, and screen 500 verified stocks and ETFs.

- **Description**: Inspect securities tracked across verified portfolios with customizable sorting, thresholds, and asset filtering.
- **Parameters**:
  | Argument | Type | Default | Description |
  |---|---|---|---|
  | `limit` | integer | `20` | Maximum number of results to return (max 100). |
  | `min_whale_capital` | number | `0` | Minimum capital held by tracked whales in USD. |
  | `min_conviction` | number | `0` | Minimum conviction intensity in dollars per holder. |
  | `min_owners` | integer | `0` | Minimum number of verified retail holders. |
  | `asset_type` | string | `"all"` | Filter by `"all"`, `"stocks"`, or `"etfs"`. |
  | `sort_by` | string | `"whale_capital"` | Sort order: `"whale_capital"`, `"total_value"`, `"owners"`, `"conviction"`, or `"change_percent"`. |
- **Sample Call**:
  ```json
  {
    "name": "get_top_equities",
    "arguments": {
      "sort_by": "conviction",
      "min_owners": 25,
      "limit": 10
    }
  }
  ```

---

### 3. `get_etf_flows`
Inspect 64 verified ETFs and index funds ranked by capital, expense ratios, and holder breadth.

- **Description**: Analyze index trackers (`SPY`, `QQQ`, `VOO`), leveraged vehicles (`TQQQ`, `MSTU`, `NVDL`), crypto trusts (`IBIT`, `ETHE`), and cash vaults (`SGOV`).
- **Parameters**:
  | Argument | Type | Default | Description |
  |---|---|---|---|
  | `limit` | integer | `20` | Maximum number of ETFs to return (max 64). |
  | `sort_by` | string | `"whale_capital"` | Sort by `"whale_capital"`, `"total_value"`, `"owners"`, or `"change_percent"`. |
- **Sample Call**:
  ```json
  {
    "name": "get_etf_flows",
    "arguments": {
      "sort_by": "whale_capital",
      "limit": 15
    }
  }
  ```

---

### 4. `get_whale_portfolio`
Look up any verified whale account by username to inspect verified positions, cost basis, profit, and cash balances.

- **Description**: Full portfolio inspection for any of the 395 verified accounts controlling $169M+ in capital. If an exact handle match is not found, the tool returns up to 5 suggested partial matches.
- **Parameters**:
  | Argument | Type | Required | Description |
  |---|---|---|---|
  | `username` | string | Yes | Target AfterHour username (e.g. `"thealexperez"`, `"SirJackALot"`, `"mphinance"`). Leading `@` is optional. |
- **Sample Call**:
  ```json
  {
    "name": "get_whale_portfolio",
    "arguments": {
      "username": "thealexperez"
    }
  }
  ```
- **Return Fields**:
  - `username`: Verified account name.
  - `total_value`: Total equity balance.
  - `cash_balance`: Liquid uninvested cash (dry powder).
  - `profit_today`: Intraday P&L.
  - `profit_total`: Total unrealized gain or loss.
  - `followers`: Social follower count.
  - `shadow_ratio`: Dollars of equity per social follower.
  - `positions`: Array of verified positions sorted by value descending, with quantity, current value, cost basis, profit, and percentage weighting.

---

### 5. `get_ticker_intel`
Forensic intelligence on any ticker symbol with verified holders, conviction intensity, and 90-day daily OHLCV candlestick bars.

- **Description**: Look up any stock or ETF to inspect verified owner counts, whale holders, and historical price bars.
- **Parameters**:
  | Argument | Type | Required | Description |
  |---|---|---|---|
  | `ticker` | string | Yes | Stock or ETF symbol (e.g. `"NVDA"`, `"ASTS"`, `"RKLB"`, `"SPY"`). |
  | `include_bars` | boolean | No | Set to `true` to include full 90-day OHLCV candlestick bars. Default is `false`. |
- **Sample Call**:
  ```json
  {
    "name": "get_ticker_intel",
    "arguments": {
      "ticker": "ASTS",
      "include_bars": true
    }
  }
  ```

---

### 6. `get_conviction_screener`
Scan for asymmetric conviction where average position size per holder exceeds a target threshold.

- **Description**: Filters the equity universe for high dollar-per-holder concentration. Identifies high conviction accumulation before social volume spikes.
- **Parameters**:
  | Argument | Type | Default | Description |
  |---|---|---|---|
  | `min_intensity` | number | `50000` | Minimum conviction intensity in dollars per holder. |
  | `min_owners` | integer | `15` | Minimum number of verified retail holders. |
  | `limit` | integer | `20` | Maximum results to return. |
- **Sample Call**:
  ```json
  {
    "name": "get_conviction_screener",
    "arguments": {
      "min_intensity": 75000,
      "min_owners": 20,
      "limit": 10
    }
  }
  ```

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
