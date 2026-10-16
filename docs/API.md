# AfterMath Quantitative Alt-Data API Reference

> Edge-cached alternative financial intelligence API tracking verified retail & whale equity, conviction intensity ($/holder), whale dry powder cash, and macro tape liquidity from the AfterHour social terminal.
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
- **Fast Static Responses**: Pre-computed JSON files, gzip-compressed with ETag/Last-Modified. Small files (`market.json`, `/api/ticker/*`) return in roughly 250 to 350ms; `whales.json` and `shadow.json` are ~3.8MB uncompressed, so expect 600ms+.

---

## 📡 Endpoints Catalog

The list below is generated from the built `api/*.json` files by `scripts/gen_openapi.py`; hand-written notes follow it.

<!-- BEGIN GENERATED -->
### Market

#### 1. Macro tape

- **Path**: `GET /api/market.json`
- **Description**: Whale dry powder cash, intraday net P&L, equity/ETF/options allocation and the capital-inflow, retail-breadth, conviction and gainer leaders.
- **Request**: `curl -sL https://ah.mphinance.com/api/market.json`
- **Top-level fields**: `version` (string), `timestamp` (string), `source` (string), `macro` (object), `capitalInflowLeaders` (array), `retailBreadthLeaders` (array), `convictionIntensityLeaders` (array), `topTapeGainers` (array)

#### 2. Macro tape (alias)

- **Path**: `GET /api/market-summary.json`
- **Description**: Same payload as `/api/market.json`, kept as a stable alias.
- **Request**: `curl -sL https://ah.mphinance.com/api/market-summary.json`
- **Top-level fields**: `version` (string), `timestamp` (string), `source` (string), `macro` (object), `capitalInflowLeaders` (array), `retailBreadthLeaders` (array), `convictionIntensityLeaders` (array), `topTapeGainers` (array)

#### 3. Sentiment

- **Path**: `GET /api/sentiment.json`
- **Description**: Social sentiment from the AfterHour post archive: per-window summaries, buzz leaders and daily mention series.
- **Request**: `curl -sL https://ah.mphinance.com/api/sentiment.json`
- **Top-level fields**: `generated_at` (string), `source` (string), `archive` (object), `method` (string), `caveat` (string), `windows` (object), `buzz` (object), `daily` (object)

#### 4. Recent AfterHour posts

- **Path**: `GET /api/ah-posts.json`
- **Description**: Recent public community posts collected from the AfterHour app. Published when the collector has produced it.
- **Request**: `curl -sL https://ah.mphinance.com/api/ah-posts.json`
- **Top-level fields**: `generated_at` (string), `posts` (array)

### Securities

#### 5. All tracked securities

- **Path**: `GET /api/stonks.json`
- **Description**: Every tracked security with owner counts, total platform value, whale capital, conviction intensity ($ per holder), session change and chatroom activity. Currently 500 securities.
- **Request**: `curl -sL https://ah.mphinance.com/api/stonks.json`
- **Top-level fields**: `total` (integer), `securities` (array)

#### 6. ETFs

- **Path**: `GET /api/etfs.json`
- **Description**: ETFs segregated from equities, with asset class, expense ratio and whale backing. Currently 64 securities.
- **Request**: `curl -sL https://ah.mphinance.com/api/etfs.json`
- **Top-level fields**: `total` (integer), `securities` (array)

#### 7. Ticker deep dive

- **Path**: `GET /api/ticker/{symbol}.json`
- **Description**: One security: its row, the verified whale holders, and daily OHLCV history bars. One file per tracked ticker. Currently 90 whales.
- **Request**: `curl -sL https://ah.mphinance.com/api/ticker/NVDA.json`
- **Top-level fields**: `security` (object), `whales` (array), `history` (array)

### Whales

#### 8. Reported whale position changes

- **Path**: `GET /api/whale-changes.json`
- **Description**: Quantity changes (OPEN, ADD, TRIM, CLOSE, EXPIRED, FLIP) detected between polls of public whale portfolios, with notional and percent of portfolio. Positions are the last broker sync marked to live prices, so changes are rare. Currently 0 records.
- **Request**: `curl -sL https://ah.mphinance.com/api/whale-changes.json`
- **Top-level fields**: `generated_at` (string), `count` (integer), `changes` (array)

#### 9. Whale data freshness

- **Path**: `GET /api/whale-sync.json`
- **Description**: How fresh the whale position data is: whales tracked, recently polled, newest and oldest broker sync.
- **Request**: `curl -sL https://ah.mphinance.com/api/whale-sync.json`
- **Top-level fields**: `generated_at` (string), `whales_tracked` (integer), `polled_last_hour` (integer), `never_polled` (integer), `newest_broker_sync` (string), `oldest_broker_sync` (string), `synced_within_30d` (integer), `note` (string), `whales` (object)

#### 10. Verified whale portfolios

- **Path**: `GET /api/whales.json`
- **Description**: High-capital portfolios with broker-verified positions, cash, P&L and shadow ratio. Large file (several MB uncompressed). Currently 395 whales.
- **Request**: `curl -sL https://ah.mphinance.com/api/whales.json`
- **Top-level fields**: `total` (integer), `whales` (array)

#### 11. Shadow whales (clout inversion)

- **Path**: `GET /api/shadow.json`
- **Description**: The same whales sorted by verified dollars per follower: big capital, tiny following. Large file. Currently 395 whales.
- **Request**: `curl -sL https://ah.mphinance.com/api/shadow.json`
- **Top-level fields**: `total` (integer), `whales` (array)

### Telegram Funnel

#### 12. Flagged accounts

- **Path**: `GET /api/funnel.json`
- **Description**: Accounts on the telegramscammers.com flag list, enriched with public Telegram recon. Wording: flagged for investigation, not a finding of fraud. Currently 150 accounts.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel.json`
- **Top-level fields**: `source` (string), `credit` (string), `database` (string), `network` (string), `submit_intel` (string), `upstream_json` (string), `disclaimer` (string), `count` (integer), `tiers` (object), `shared_link_clusters` (array), `tickers` (array), `callouts` (object), `accounts` (array)

#### 13. Funnel ticker rankings

- **Path**: `GET /api/funnel-tickers.json`
- **Description**: Tickers most mentioned across funnel channels. Currently 676 records.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-tickers.json`
- **Top-level fields**: `source` (string), `generated_at` (string), `credit` (string), `disclaimer` (string), `small_sample_warning` (string), `count` (integer), `tickers` (array)

#### 14. Parsed callouts (recent)

- **Path**: `GET /api/funnel-calls.json`
- **Description**: Parsed trade callouts from funnel channels. Quoted results are channel claims, unverified. Currently 1000 calls.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-calls.json`
- **Top-level fields**: `source` (string), `generated_at` (string), `credit` (string), `disclaimer` (string), `small_sample_warning` (string), `quoted_results_are_channel_claims` (string), `total_parsed` (integer), `count` (integer), `calls_with_scored_outcome` (integer), `calls` (array)

#### 15. Parsed callouts (full archive, JSON)

- **Path**: `GET /api/funnel-calls-full.json`
- **Description**: Full callout archive including scoring fields. Large file. Currently 14706 calls.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-calls-full.json`
- **Top-level fields**: `generated_at` (string), `credit` (string), `disclaimer` (string), `quoted_results_are_channel_claims` (string), `path_note` (string), `note` (string), `count` (integer), `scored_count` (integer), `path_count` (integer), `window_start` (string), `window_end` (string), `calls` (array)

#### 16. Parsed callouts (full archive, CSV)

- **Path**: `GET /api/funnel-calls-full.csv`
- **Description**: The full callout archive as CSV, one row per callout. Large file. Currently 14706 rows.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-calls-full.csv`

#### 17. Option price paths

- **Path**: `GET /api/funnel-option-paths.json`
- **Description**: What each called option contract did after the post (5-minute trade bars), with sample sizes and coverage.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-option-paths.json`
- **Top-level fields**: `generated_at` (string), `credit` (string), `disclaimer` (string), `methodology` (object), `window_start` (string), `window_end` (string), `small_n_threshold` (integer), `coverage` (object), `pooled` (object), `delay_sensitivity` (object), `fill_gap` (object), `robustness` (object), `by_channel` (array), `by_ticker` (array), `by_session_hour` (array), `n_channels` (integer)

#### 18. Scorecard

- **Path**: `GET /api/funnel-scorecard.json`
- **Description**: Pooled and per-channel scoring: option paths, hold-to-expiry, and forex/gold/index TP1-first vs SL-first, with Wilson 95% ranges beside every rate.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-scorecard.json`
- **Top-level fields**: `generated_at` (string), `credit` (string), `disclaimer` (string), `source` (string), `methodology` (string), `methodology_doc` (string), `conventions` (string), `small_sample_rule` (string), `options` (object), `fx` (object)

#### 19. Forex / gold / index signals

- **Path**: `GET /api/funnel-fx-signals.json`
- **Description**: Parsed and scored forex, gold and index signals from funnel channels. Currently 63 signals.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-fx-signals.json`
- **Top-level fields**: `generated_at` (string), `credit` (string), `disclaimer` (string), `methodology` (string), `count` (integer), `signals` (array)

#### 20. Live feed

- **Path**: `GET /api/funnel-live.json`
- **Description**: Last 72 hours of parsed, unscored callouts and hot tickers. Refreshed every few minutes on market days. Currently 310 calls.
- **Request**: `curl -sL https://ah.mphinance.com/api/funnel-live.json`
- **Top-level fields**: `source` (string), `generated_at` (string), `disclaimer` (string), `market` (string), `window_hours` (integer), `refresh_hint_sec` (integer), `channels_polled` (integer), `channels_total` (integer), `new_posts_this_run` (integer), `live_note` (string), `count` (integer), `hot_tickers` (array), `calls` (array)

### MCP

#### 21. MCP tool and resource catalog

- **Path**: `GET /api/mcp-schema.json`
- **Description**: Tool definitions (name, description, inputSchema) and resources, generated from the server code.
- **Request**: `curl -sL https://ah.mphinance.com/api/mcp-schema.json`
- **Top-level fields**: `version` (string), `protocolVersion` (string), `server` (object), `toolCount` (integer), `tools` (array), `resources` (array)

#### 22. This OpenAPI document

- **Path**: `GET /api/openapi.json`
- **Description**: The OpenAPI 3.1 specification, generated by `scripts/gen_openapi.py` from the built files.
- **Request**: `curl -sL https://ah.mphinance.com/api/openapi.json`
- **Top-level fields**: `openapi` (string), `info` (object), `paths` (object), `components` (object)

#### 23. MCP JSON-RPC 2.0 (live)

- **Path**: `POST /api/mcp`
- **Description**: Stateless Streamable-HTTP MCP endpoint. Send JSON-RPC 2.0 `tools/list` or `tools/call`. 16 tools: `get_market_tape`, `get_top_equities`, `get_etf_flows`, `get_whale_portfolio`, `get_ticker_intel`, `screen_whales`, `get_shadow_whales`, `get_social_feed`, `get_funnel_accounts`, `get_funnel_callouts`, `get_funnel_scorecard`, `get_market_session`, `get_live_quotes`, `get_leaderboard`, `get_security_chart`, `get_retail_sentiment`. Not a static file: this one runs the live server code.
- **Request**:
  ```bash
  curl -s -X POST https://ah.mphinance.com/api/mcp \
    -H 'Content-Type: application/json' \
    -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_market_tape", "arguments": {}}}'
  ```

_Generated by `scripts/gen_openapi.py` from the built files. Full schemas: [/api/openapi.json](https://ah.mphinance.com/api/openapi.json) or the [Swagger UI](https://ah.mphinance.com/docs)._
<!-- END GENERATED -->

---

## 🔌 Transports, Health & Specs

### MCP SSE Transport
- **SSE Stream**: `GET https://ah.mphinance.com/sse`
- **Message Receiver**: `POST https://ah.mphinance.com/messages?sessionId=<session_id>`
- **Description**: Full bidirectional SSE transport conforming to MCP specification `2024-11-05`. Compatible with `mcp-remote`, Cursor, Claude Desktop, and Antigravity.
- **Client Connect**:
  ```bash
  npx -y mcp-remote https://ah.mphinance.com/sse
  ```

---

### Health & MCP Status Check
- **Path**: `GET /health` (aliases: `GET /api/health`, `GET /status`, `HEAD /health`)
- **Description**: Returns server health, uptime in seconds, supported MCP protocol versions (`2025-06-18`, `2025-03-26`, `2024-11-05`), endpoints manifest, and the registered tool count (`tools_count`).
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
    "uptime_seconds": 42.5
  }
  ```

---

### OpenAPI Specification & MCP Tool Schemas
- `GET /api/openapi.json`: Complete OpenAPI 3.1.0 JSON document.
- `GET /api/mcp-schema.json`: Complete Model Context Protocol tool and resource manifest.
- `GET /sitemap.xml`: Standard XML sitemap covering every public route.

---

## 🛡️ Telegram Funnel Field Notes

### Accounts (`/api/funnel.json`)
- **Path**: `GET /api/funnel.json`
- **Description**: AfterHour accounts flagged for funneling traders into Telegram channels, with evidence tier (`reported`, `corroborated`, `verified`), shared-link clusters and posting stats. Data curated by [TelegramScammers.com](https://telegramscammers.com). Flagged for investigation, not a finding of fraud.
- **Lookup UI**: `https://ah.mphinance.com/scamcheck`. **MCP tool**: `get_funnel_accounts`.
- See [FUNNEL.md](FUNNEL.md).

### Ticker rankings (`/api/funnel-tickers.json`)
- **Path**: `GET /api/funnel-tickers.json`
- **Description**: Tickers called out by flagged AfterHour accounts and their public Telegram channels, ranked, with `ah_accounts`, `ah_posts`, `tg_channels`, `tg_posts`. Credit: [TelegramScammers.com](https://telegramscammers.com). Flagged for investigation, not a finding of fraud.
- **MCP tool**: `get_funnel_tickers`.

### Callouts (`/api/funnel-calls.json`)
- **Path**: `GET /api/funnel-calls.json`
- **Description**: The 300 most recent parsed trade callouts from public Telegram channels: `channel`, `posted`, `ticker`, `kind`, `side`, `strike`, `expiry`, `entry_price`, `action`, `result_pct`, text truncated to 160 characters, optional `parse_flags`, and an `outcome` object when the callout has been scored against the real tape. `result_pct` is the channel's own claim (see `quoted_results_are_channel_claims`); the sample is small. Generated by `build_funnel_calls.py`.
- **MCP tool**: `get_funnel_callouts` (`ticker`, `channel`, `action`, `limit`).

### Scorecard (`/api/funnel-scorecard.json`)
- **Path**: `GET /api/funnel-scorecard.json`
- **Description**: Public scoring of trade callouts from public Telegram channels against the real tape. `options` (held to expiry, the secondary view; the main option view is `/api/funnel-option-paths.json`): `pooled` (n, win rate with Wilson 95% interval, median and mean return, share expired worthless, window, assumptions), `coverage_funnel`, `by_dte_bucket`, `by_ticker` (top 15), `by_channel` (every channel with at least one scored open, `small` = n under 5), `paired` (channel-quoted close versus the same contract held to expiry). `fx`: `pooled` (market-fill: TP1 first rate, SL first rate, TP2 or later, mean R, break-even TP1 rate), `by_instrument`, `by_channel`, `weekly_by_channel` (channels with 30 or more scored signals), `touch_variant` (reported separately, never pooled), `sensitivity` (basis-shift rows and range), `assumptions`, `content_timeline` (per channel: forex/gold/index versus stock/option post date ranges and bulk-dump groups). Rates are fractions 0..1, `*_ci` are Wilson 95% intervals, option returns are percent, FX results are in R. Includes `generated_at`, `credit`, `disclaimer`. Generated by `build_funnel_scorecard.py`. Analysis of public posts, not advice; flagged for investigation, not a finding of fraud.
- **Page**: `https://ah.mphinance.com/scorecard`. **MCP tool**: `get_funnel_scorecard` (`section`: paths, options, fx or all; `channel` substring).

### Option price paths (`/api/funnel-option-paths.json`)
- **Path**: `GET /api/funnel-option-paths.json`
- **Description**: What each option contract called out in public Telegram channels did AFTER the post, from the contract's own 5-minute trade bars. Calls posted in the regular session get the next 30 minutes; daily callouts (before the open, after the close, weekends) get the whole next session; fill = open of the first bar at or after the post. Keys: `methodology` (`windows`, `fill_rule`, `rules`, `assumptions[]`, `limitations[]`), `coverage` (funnel: option opens, parseable contract, no bars, unscorable by reason, scored, intraday versus daily), `pooled.intraday` and `pooled.daily` (`n`, `ended_green` {k, n, rate, ci}, `peak_pct`, `drawdown_pct`, `end_return_pct` {median, mean}, `rules[]` for +50/-50, +100/-50 and +30/-30 with `tp_first`, `sl_first`, `neither`, rates, Wilson ranges and `mean_return_pct`, `liquidity`, `quoted_entry_realism`), `delay_sensitivity.rows` (fill 0, 5, 10, 15 minutes later), `by_channel` (every channel with a scored call; `small` = n under 25), `by_ticker` (top 15), `by_session_hour` (ET hour of the post), `window_start`, `window_end`. Returns are percent of the fill, rates are fractions 0..1, `*_ci` are Wilson 95% ranges. Bars are trade prints: spread and slippage are not modelled, so real results would be worse. Built by `build_funnel_paths.py` from `tg_option_paths.py score` output; rebuilt locally only (the bar archive never leaves this machine) and deployed by rsync. Analysis of public posts, not advice; flagged for investigation, not a finding of fraud.
- **Page**: `https://ah.mphinance.com/scorecard`. **MCP tool**: `get_funnel_scorecard` with `section=paths`.
- **Export**: scored option opens in `/api/funnel-calls-full.json` carry a nested `path` object (`category`, `fill`, `mfe_pct`, `mae_pct`, `end_ret_pct`, `volume`, `tp50_sl50`, `tp50_sl50_ret`, `quoted_vs_fill_pct`) and `/api/funnel-calls-full.csv` the flat `path_*` columns. They are present only when the export is built locally.

### FX signals (`/api/funnel-fx-signals.json`)
- **Path**: `GET /api/funnel-fx-signals.json`
- **Description**: Every scored forex, gold or index signal from public channels: `id`, `channel`, `date`, `instrument`, `side`, `entry_lo`, `entry_hi`, `sl`, `tps`, `variant` (`market` or `touch`), `outcome`, `r_tp1`, `r_last`, `minutes_to_first_event`, `tps_hit`, and `text` (the original post, truncated to 400 characters). Newest first. Generated by `build_funnel_scorecard.py` from `tg_fx_signals.py` output.
