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
Exposes 11 production tools: `get_market_tape`, `get_top_equities`, `get_etf_flows`, `get_whale_portfolio`, `get_ticker_intel`, `get_conviction_screener`, `screen_whales`, `get_shadow_whales`, `get_price_history`, `get_social_feed`, and `get_funnel_accounts` (Telegram-funnel lookup; data from https://telegramscammers.com, built by `build_funnel.py` from `accounts.json`).

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

- **Pipeline order**: `tg_calls.py` -> `tg_outcomes.py` -> `funnel_tickers.py` -> `analyze_funnel.py` -> `build_funnel.py` -> `build_funnel_calls.py` (the last two also run by `build_github_pages.py`). `tg_outcomes.py` scores callouts by hold-to-expiry intrinsic vs Yahoo public bars; small sample, channel quotes are unverified.
- **Served**: `/scamcheck`, `/api/funnel.json`, `/api/funnel-tickers.json`, `/api/funnel-calls.json`, MCP tools `get_funnel_accounts`, `get_funnel_callouts`, `get_funnel_tickers` (13 tools total).
- **UI rule**: scamcheck hides outcome rates until 100 callouts are scored.
- **Server cron**: `tg_watch.py` daily 13:15 UTC on Coolify, checkout `/home/mph/apps/aftermath-watch` (outside the webroot, sparse: `tg_recon.py tg_watch.py tg_calls.py accounts.json reports/analysis/funnel_watch.md`). New dependencies of `tg_watch.py` must be added to the sparse list. Merge its archive locally with `tg_merge_archive.py`.
- **Deploy**: the documented `--delete` rsync is unsafe here (webroot has unrelated files). Copy only touched files, back up to `.bak_overnight` first, then `docker restart ah-mcp ah-mphinance` (`ah-mcp` serves `mcp_server.py`).
- **Never public**: `candidates_*.json`, `recon_candidates.json`, `recon_pivot.json`, `handoff_private/`, `posts_archive.jsonl`, snapshots, price cache. Unreviewed third-party accounts may be innocent.
- **Never**: post, follow, comment, or join Telegram channels from automation.
