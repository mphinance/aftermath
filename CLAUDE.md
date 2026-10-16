# AfterMath & AfterHour Alpha Terminal

> Institutional-grade forensic scraper, quantitative intelligence engine, and live web terminal tracking the AfterHour social trading ecosystem.
> Live Production URL: **https://ah.mphinance.com**
> GitHub Repository: **https://github.com/mphinance/aftermath** (Branch: `main`)

---

## 🚀 Live Production & Coolify Deployment Details

The production web terminal and public API endpoints are hosted on our dedicated Coolify infrastructure.

### Server Connection
- **SSH Host Alias**: `coolify` (configured in `~/.ssh/config`)
- **Direct IP**: `5.161.247.12`
- **SSH User**: `mph`
- **Connect Command**:
  ```bash
  ssh coolify
  ```

### Production Webroot & Container
- **Host Webroot Directory**: `/home/mph/apps/ah-portal`
- **Docker Container Name**: `ah-mphinance`
- **Docker Image**: `nginx:alpine`
- **Docker Network**: `coolify` (attached to Traefik reverse proxy)
- **Container Volume Mounts**:
  - `/home/mph/apps/ah-portal:/usr/share/nginx/html:ro`
  - `/home/mph/apps/ah-portal/default.conf:/etc/nginx/conf.d/default.conf:ro`

### Traefik Reverse Proxy Configuration
The container is dynamically routed by Traefik using the following docker labels:
- `traefik.enable=true`
- `traefik.docker.network=coolify`
- `traefik.http.routers.ah-mphinance.rule=Host(\`ah.mphinance.com\`)`
- `traefik.http.routers.ah-mphinance.entrypoints=https`
- `traefik.http.routers.ah-mphinance.tls=true`
- `traefik.http.routers.ah-mphinance.tls.certresolver=letsencrypt`
- `traefik.http.routers.ah-mphinance.service=ah-mphinance`
- `traefik.http.services.ah-mphinance.loadbalancer.server.port=80`
- `traefik.http.routers.ah-mphinance-http.rule=Host(\`ah.mphinance.com\`)`
- `traefik.http.routers.ah-mphinance-http.entrypoints=http`
- `traefik.http.routers.ah-mphinance-http.middlewares=ah-mphinance-redirect`
- `traefik.http.middlewares.ah-mphinance-redirect.redirectscheme.scheme=https`
- `traefik.http.middlewares.ah-mphinance-redirect.redirectscheme.permanent=true`

### Nginx Routing (`default.conf`)
Located on host at `/home/mph/apps/ah-portal/default.conf` and in repo at `./default.conf`:
```nginx
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    # Prevent scheme/port downgrade on subdirectory redirects (e.g. /all -> /all/)
    absolute_redirect off;

    # High-performance Gzip compression for JSON APIs and static bundles
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        # HTML5 History API pushState support for URL slugs
        try_files $uri $uri/ /index.html;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

---

## 🧠 System Architecture & Quant Capabilities

AfterMath does not grade retail trading feeds by hype or self-reported broker screenshots; it operates on verified blockchain/broker data, inverted index mapping, and quantitative tape mechanics:

### 1. The Whale Census ($169M+ Tracked Capital)
- **Universe**: **395 verified portfolios** swept from platform-wide holdings.
- **Total Capital**: **$169,001,648.72** in verified tracked equity.
- **Verified Millionaires**: **31 accounts** controlling **$110,788,487.39**.
- **The Clout Inversion Law**: Proves retail follower count is inversely correlated with real capital. Accounts like `@skrt` ($33.8M verified) or `@BearHugger` ($1.45M verified) fly under the radar with single/double-digit followers ($100k+ to $700k+/follower shadow ratio), while retail influencers with 230k+ followers hold ~$53/follower.

### 2. The 500-Security Universe & Quantitative Ranking
Instead of arbitrary raw API pagination (where low-cap stocks like `PATH` with $22k appear first), the terminal ranks every asset across multiple quantitative dimensions:
- **Whale Capital ($)** *(Default Institutional Rank)*: Sorted by aggregate dollars held by verified whales (e.g. AAPL $18.4M, ASTS $16.4M, NVDA $10.9M, QQQ $7.6M, SPY $7.1M).
- **Total Platform Exposure ($)**: Platform-wide aggregate equity held.
- **Verified Owners Count**: Broad retail consensus (NVDA leads with 321 verified owners, VOO 197, MSFT 187, AAPL 179).
- **24h Intraday Momentum (% Gain / % Dip)**.
- **Matrix Chatroom Heat**: Member volume and active online users.

### 3. ETF vs. Equity Segregation
- **64 ETFs** (SPY, QQQ, VOO, SGOV, IBIT, SMH, etc.) cleanly separated from **436 Equities**.
- Filter pills allow instant toggle between `All (500)`, `🏛️ ETFs Only`, `📈 Equities Only`, `Whale Favs ($1M+)`, `Most Owned`, and `Gainers`.

### 4. Over-Time Historical OHLCV Daily Bars
- The ticker deep-dive modal pulls 44-day daily OHLCV bars across major tickers (`AAPL`, `ASTS`, `NVDA`, `SPY`, `TSLA`, `MSTR`, `AMZN`, `MSFT`, `QQQ`, `PLTR`, `AMD`, `META`, `GOOGL`, `HOOD`, `COIN`, `SOFI`, `VOO`, `IBIT`).
- Interactive SVG charts display the 44-day trajectory, percentage gain/loss, high/low envelopes, and volume benchmarks.

### 5. URL Slugs, Permalinks & Developer APIs
The terminal supports clean URL routing for web browsing, permalink sharing, OpenAPI documentation, and Model Context Protocol (MCP):
- **Web Views**: `https://ah.mphinance.com/stonks`, `/all`, `/etfs`, `/whales`, `/shadow`, `/sitemap`
- **Developer Documentation**:
  - `https://ah.mphinance.com/docs`: Interactive Swagger UI (OpenAPI 3.1) with live in-browser testing
  - `https://ah.mphinance.com/mcp`: Official Model Context Protocol (MCP) server portal & AI client integration guides
- **Stock Slugs**: `https://ah.mphinance.com/ticker/:symbol` (e.g. `/ticker/NVDA`, `/ticker/AAPL`)
- **Whale Slugs**: `https://ah.mphinance.com/@:username` (e.g. `/@skrt`, `/@SIRJACK`)
- **Static Edge JSON APIs & MCP Assets**:
  - `https://ah.mphinance.com/api/market.json`: Real-time macro tape, whale dry powder ($8.98M cash), intraday net P&L, allocation ratio
  - `https://ah.mphinance.com/api/stonks.json`: All 500 securities with owner counts, conviction intensity ($/sub), and whale capital
  - `https://ah.mphinance.com/api/etfs.json`: 64 ETFs segregated by asset class, expense ratio, and whale backing
  - `https://ah.mphinance.com/api/whales.json`: 395 verified high-roller and millionaire portfolios ($169M+ AUM)
  - `https://ah.mphinance.com/api/shadow.json`: Clout Inversion index sorted by $/follower ratio asymmetry
  - `https://ah.mphinance.com/api/ticker/:symbol.json`: 500 individual ticker deep dives with 90-day daily OHLCV candlestick bars
  - `https://ah.mphinance.com/api/openapi.json`: Full OpenAPI 3.1 JSON specification
  - `https://ah.mphinance.com/api/mcp-schema.json`: Model Context Protocol tool & resource catalog
  - `https://ah.mphinance.com/mcp/server.py`: Standalone zero-dependency Python MCP server script

### 6. Model Context Protocol (MCP) Server for AI Agents
Any AI assistant (Claude Desktop, Cursor IDE, Antigravity CLI, Windsurf) can connect to AfterMath in 30 seconds with **zero API keys** and **zero external dependencies**:
```json
{
  "mcpServers": {
    "aftermath": {
      "command": "python3",
      "args": [
        "-c",
        "import urllib.request; exec(urllib.request.urlopen('https://ah.mphinance.com/mcp/server.py').read().decode('utf-8'))"
      ]
    }
  }
}
```
Exposes 16 tools (the live list is `api/mcp-schema.json`, generated from `MCP_TOOLS_DEFINITIONS`; `scripts/check_docs.py` fails when a count in the docs drifts). Deliberately small: the user cut 34 to 16 (agents choose badly from long lists). Snapshot tools over the verified 500 and 395 whales; 3 Telegram-funnel tools (data from https://telegramscammers.com); LIVE tools that call `api.afterhour.com` directly (see below); one retail-sentiment tool with `view` modes. Add a tool only by retiring or merging another.

**Deploy gotcha:** the MCP runs in the separate `ah-mcp` container (`python3 mcp_server.py --port 8089`, webroot bind-mounted read-only at `/app`). Changes to `mcp_server.py` need `ssh coolify "docker restart ah-mcp"`, not just `ah-mphinance`. Rsync list must include `accounts.json`-derived `api/funnel.json` (already under `api/`) and `mcp_server.py`.

### 7. Institutional Partner Funnel: TraderMatrix Pro
Integrated throughout the terminal is the referral funnel to **TraderMatrix Pro**:
- **Referral Code**: `MPHINANCE`
- **URL**: `https://www.tradermatrix.pro/?ref=MPHINANCE`
- **Hook**: "If we pull this kind of edge from a social app, imagine what we do with real tape." Converts social alt-data lookers into institutional options flow, GEX dealer gamma, and dark pool tape subscribers.

---

## 🛠️ Build, Deploy & Sync Workflow

### One-Command Build & Deploy
```bash
# 1. Regenerate HTML bundle, static directory mirrors, OpenAPI spec, and JSON APIs
python3 build_github_pages.py

# 2. Sync to Coolify webroot
rsync -avz --delete \
  --exclude '.git' --exclude '__pycache__' --exclude 'afterhour.zip' --exclude 'data/following' \
  index.html default.conf sitemap.xml mcp_server.py api all stonks etfs whales shadow sitemap docs mcp \
  coolify:/home/mph/apps/ah-portal/

# 3. Restart container to ensure single-file bind mounts refresh
ssh coolify "docker restart ah-mphinance"

# 4. Commit and push changes to GitHub
git add -A
git commit -m "feat: update terminal, docs, and APIs"
git push origin main
```

### Forensic Autopsy Pipeline (Historical)
- `python3 download_single_trader_lifetime.py <username>`: Pulls complete post history into `data/following/@<u>_all_posts.json` and markdown report.
- `python3 followthrough.py --json reports/analysis/followthrough.json`: Audits entry-to-exit disclosure gaps.
- `python3 positions.py <u>`: Extracts broker-verified leg changes, diffs, and account value history.
- `python3 fetch_prices.py <u>`: Pulls daily historical price bars and earnings dates.

---

## ⚠️ Important Gotchas & Lessons Learned

1. **AfterHour Mobile Posting**:
   - **DO NOT attempt to post or submit forms to the live mobile app via automation**. Michael has directed to hold back from automated posting to prevent mobile account rate-limiting or shadowbanning.
2. **AfterHour API CORS**:
   - `api.afterhour.com` restricts browser CORS to `*.afterhour.com`. Direct browser calls from external origins fail. Pre-bundling the data or querying our static APIs (`ah.mphinance.com/api/...`) completely solves this.
3. **Nginx Directory Redirects**:
   - Always keep `absolute_redirect off;` in `default.conf`. Otherwise, requests to directory paths like `/all` redirect to `http://...` before hitting Traefik's HTTPS redirect.
4. **Broker Snapshot Position Math**:
   - In AfterHour's raw JSON, `amount_k` is account value in **thousands** of dollars (e.g. 57382 = $57.4M, not $57.4k). Option contract quantities represent underlying shares (contracts × 100).

5. **Price endpoint param**:
   - `/stonks/tickers/prices` takes `symbols=`, not `tickers=` (that silently returns `{"prices":[]}`), and `prices` is an array. The leaderboard `sortOrder` is an enum (`TRENDING|WATCHERS|OWNERS|GAINERS|LOSERS`); a bad value is a 400.
6. **Gateway flakiness**: `GAINERS` with a non-`DAY` `timeRange` 504s; the gateway also 504s ~1 request in 7. Retry with backoff (see `afterhour.py`).
7. **Do not poke the app's admin surface**: the app bundle references an `ah-user-id` impersonation header and `/_ah/admin/*`, `/mjolnir/*` routes. They are documented in `reverse-engineering/`, not tested, and stay untested.

---

## 🔬 App Reverse Engineering (`reverse-engineering/`)

Static analysis of the Android app (`com.afterhour` 4.6.4) plus unauthenticated GET probes. Contains the recovered OpenAPI 3.1 spec (`afterhour-openapi.yaml`, 152 operations), request/response models with evidence, the realtime WebSocket protocol, and a typed TS client (`client-ts/`). Start at `reverse-engineering/README.md`.
- It is **not** in the deploy rsync list on purpose. Do not add it: it documents internal routes.
- The APK, the 56MB Hermes decompile and jadx output are not committed; the README has the regen steps. Hermes bytecode needs `hermes-dec` (`hbc-decompiler`), jadx/apktool cannot read it. On a small box stream the decompile with grep/sed, never load it whole.
- `AFTERHOUR_API_SPEC.md` is the short public-data reference; on disagreement the RE spec wins.

---

## 🛡️ Telegram Funnel Tracking (`/scamcheck`, `api/funnel.json`)

Flag list `accounts.json` is curated by **https://telegramscammers.com** (the owner is a friend; we cannot touch his site, only send him data). We enrich it and serve it: `api/funnel.json`, MCP tool `get_funnel_accounts`, static page `scamcheck/index.html`. Full pipeline and gotchas in `docs/FUNNEL.md`.

- Rebuild: `python3 build_funnel.py` (also called by `build_github_pages.py`). `scamcheck/` and `mcp/index.html` are hand-written static pages, not generated.
- `tg_recon.py` is passive (public t.me previews only). Invite hashes are **case-sensitive**: use `telegram_links`, not the lowercased `telegram_links_norm`.
- `afterhour.com/<user>` 301s to www and the page scrape is dead; use `api.afterhour.com/public/profile?username=`.
- `data/telegram_funnel/candidates_*.json` and `recon_candidates.json` are unreviewed third-party accounts and are gitignored on purpose. Do not commit them.
- **Scheduled watcher:** `tg_watch.py` runs daily 13:15 UTC from `mph`'s crontab on the Coolify box, in `/home/mph/apps/aftermath-watch` (sparse clone, outside the webroot; `run_watch.sh` hard-resets to `origin/main` each run, so don't hand-edit there). Report: `ssh coolify cat /home/mph/apps/aftermath-watch/reports/analysis/funnel_watch.md`. Changes to `tg_recon.py`/`tg_watch.py`/`accounts.json` go live on the next run after a push.
- **Signals page:** `signals/index.html` (static) at /signals reads `api/funnel-calls.json`. The Coolify cron publishes fresh `funnel-calls.json` and `funnel-tickers.json` straight into the webroot daily via `scripts/run_watch.sh`; `api/funnel.json` is NOT auto-refreshed (run `build_funnel.py` and deploy it). Server sparse-checkout must include every script that file calls.
- Deploy only the touched files (the tree has many regenerated files); restart **both** `ah-mcp` and `ah-mphinance`.

---

## Telegram Funnel Tracking (scamcheck)

Full detail in `docs/FUNNEL.md`. Flag list is curated by https://telegramscammers.com (credit and link wherever shown); wording is always "flagged for investigation, not a finding of fraud".

- **Pipeline order**: `tg_calls.py` -> `tg_outcomes.py` -> `tg_fx_signals.py` -> `funnel_tickers.py` -> `analyze_funnel.py` -> `build_funnel.py` -> `build_funnel_calls.py` -> `build_funnel_scorecard.py` (the last three also run by `build_github_pages.py`). `tg_outcomes.py` scores callouts by hold-to-expiry intrinsic vs Yahoo public bars; small sample, channel quotes are unverified.
- **Served**: `/scamcheck`, `/signals`, `/scorecard` (all scoring is public by the owner's decision: pooled and per channel, options and forex/gold/index), `/api/funnel.json`, `/api/funnel-tickers.json`, `/api/funnel-calls.json`, `/api/funnel-scorecard.json`, `/api/funnel-option-paths.json`, `/api/funnel-fx-signals.json`, MCP tools `get_funnel_accounts`, `get_funnel_callouts`, `get_funnel_tickers`, `get_funnel_scorecard` (16 tools total, see `api/mcp-schema.json`). Scorecard wording: sample size and Wilson 95% range beside every rate, "held to expiry" for options, "TP1 first / SL first" for FX, never accusatory. Main option view = price paths after the call (`tg_option_paths.py` + `build_funnel_paths.py`, Alpaca 5-minute bars, local only; credentials in gitignored `.env_alpaca`, never on the server or in a commit); hold-to-expiry is the secondary section. Rebuild locally and rsync `api/funnel-option-paths.json`, `api/funnel-calls-full.*`; the server cron cannot build them and its gate will not overwrite them. `get_funnel_scorecard` has sections paths/options/fx/all.
- **UI rule**: scamcheck hides outcome rates until 100 callouts are scored.
- **Server cron** (two jobs, both via `scripts/run_watch.sh`): full run daily 13:15 UTC (`tg_watch.py`, sync of the upstream list, scoring) and `run_watch.sh capture` Mon-Fri 20:30 UTC (newest posts + Yahoo 5-minute option bars for the session that just ended, rescore paths). Checkout `/home/mph/apps/aftermath-watch` (outside the webroot, sparse: every script the two jobs call, i.e. `tg_*.py sync_upstream.py pull_funnel_posts.py afterhour.py funnel_tickers.py build_funnel*.py accounts.json`, `scripts/*.sh`, `data/telegram_funnel/*.json`; see docs/FUNNEL.md). Alpaca credentials (`.env_alpaca`) live only on the owner's machine; the server uses Yahoo for the daily bars. New dependencies of `tg_watch.py` must be added to the sparse list. Merge its archive locally with `tg_merge_archive.py`. The publish gate in `scripts/run_watch.sh` skips any file not rebuilt by the run or smaller than the live one (80% options/callouts, 50% FX); the server archive, option bars and `option_paths.jsonl` must be seeded from the local ones (rsync) before it can reproduce the live scorecard and paths.
- **Deploy**: the documented `--delete` rsync is unsafe here (webroot has unrelated files). Copy only touched files, back up to `.bak_overnight` first, then `docker restart ah-mcp ah-mphinance` (`ah-mcp` serves `mcp_server.py`).
- **Never public**: `candidates_*.json`, `recon_candidates.json`, `recon_pivot.json`, `handoff_private/`, `posts_archive.jsonl`, snapshots, price cache. Unreviewed third-party accounts may be innocent.
- **Live feed** (`/signals` polls `api/funnel-live.json` every 60s): `tg_live.py` scrapes page 1 of every ALIVE public channel (per `recon.json`), appends new posts to the archive, re-runs `tg_calls.py`, and publishes the last 72h of parsed, unscored callouts plus hot tickers. No Yahoo, no scoring. Cron on the Coolify box every 5 min Mon-Fri (`*/5 12-21 * * 1-5`, own lock `/tmp/aftermath-live.lock`, wrapper `/home/mph/apps/aftermath-watch/run_live.sh` -> `scripts/run_live.sh`), self-limited to 08:00-17:00 ET; log `aftermath-watch/live.log`. A run takes ~60-90s (dead channels are slow, so keep them out). `tg_live.py` and `scripts/run_live.sh` are in the server sparse-checkout list; new dependencies must be added there. Only this one file is published by the live job; the daily/capture jobs own everything else.
- **Never**: post, follow, comment, or join Telegram channels from automation.

---

## 📡 Live Tools, Sentiment & Whale Position Tracking

- **LIVE MCP tools** (`get_market_session`, `get_live_quotes`, `get_leaderboard`, `get_security_chart`; plus `get_ticker_intel` falling back to live data for tickers outside the 500, and `get_whale_portfolio` with `live=true`) call `api.afterhour.com` straight from `mcp_server.py` (`ah_get`: 3 retries, stale fallback, `{source, as_of, data}` envelope, max 3 concurrent). The `exec(urlopen(.../mcp/server.py))` client one-liner runs the server script on the *client's* machine, so it must stay one stdlib-only file. `mcp/server.py` is a copy: `cp mcp_server.py mcp/server.py` before deploy.
- **Sentiment**: `ah_collect.py` (cron `scripts/run_sentiment.sh`, every 5 min, own flock) pages the public feed, archives parsed posts to `data/ah_archive/posts.jsonl` (gitignored) and publishes `api/sentiment.json` + `api/ah-posts.json`. `ah_sentiment.py` scores deterministically: direction only from explicit CALL/PUT side + an open verb; closes, hindsight and modal words are neutral; one vote per author per ticker per day; identical titles count once. Only ~25% of posts carry direction, so every result carries voting-author count and confidence. Z-scores stay null until 3 days of archive exist.
- **Whale positions (DORMANT, no MCP tool, no cron)**: `ah_whales.py` (would run `scripts/run_whales.sh`; top 40 whales every 30 min, the rest every 12h) diffs quantities of **PUBLIC** whales from `/stonks/public/portfolio/{prf}/summary/live`, state in `data/ah_archive/whales_state.json`, publishes `api/whale-changes.json` + `api/whale-sync.json`. Parked because most whales' broker syncs are months old so there is almost nothing to report; revive only if that changes. First sweep of all 395 takes `--budget 400` (~8 min). **Gotcha:** `lastSyncedAt` on most whales is weeks or months old, so quantities rarely change; positions are broker-sync quantities marked to live prices, `pos_` ids change on every fetch (never key on them), an empty snapshot must never read as "closed everything". Privacy mode is re-checked daily and non-PUBLIC whales are purged.
- **Docs are generated**: `scripts/gen_openapi.py` (called by `build_github_pages.py`; rerun it by hand after adding tools or api files) writes `api/openapi.json`, `api/mcp-schema.json` and the generated blocks in `docs/API.md`/`docs/MCP.md`. `/mcp` renders from `mcp-schema.json`. `python3 scripts/check_docs.py` (and `tests/test_docs.py`) fail on drift, tool-count mismatches, or any `/_ah/admin`, `/mjolnir`, `ah-user-id` string in published files.
- **Deploying these**: the server sparse checkout needs `ah_collect.py ah_sentiment.py afterhour.py accounts.json scripts/run_sentiment.sh` (cron `*/5 * * * * cd /home/mph/apps/aftermath-watch && bash scripts/run_sentiment.sh >> sentiment.log 2>&1`); run with `PUBLISH_DIR=/home/mph/apps/ah-portal/api`. Restart both `ah-mcp` and `ah-mphinance` after changing `mcp_server.py`.
