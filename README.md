# 🧬 AfterMath: Retail Financial Intelligence, Live Alpha Terminal & MCP Server

> Quantitative alt-data terminal, Model Context Protocol (MCP) server, and forensic autopsy engine auditing social trading feeds, verified portfolios, and macro tape liquidity.
> 
> Production Terminal: **[https://ah.mphinance.com](https://ah.mphinance.com)**  
> Interactive Swagger API: **[https://ah.mphinance.com/docs](https://ah.mphinance.com/docs)**  
> MCP Web Portal: **[https://ah.mphinance.com/mcp](https://ah.mphinance.com/mcp)**  
> Remote MCP SSE: **[https://ah.mphinance.com/sse](https://ah.mphinance.com/sse)**  
> Partner Terminal: **[TraderMatrix Pro](https://www.tradermatrix.pro/?ref=MPHINANCE)**

[![Status](https://img.shields.io/badge/status-live%20production-brightgreen.svg)](https://ah.mphinance.com)
[![Swagger](https://img.shields.io/badge/docs-OpenAPI%203.1-blue.svg)](https://ah.mphinance.com/docs)
[![MCP](https://img.shields.io/badge/MCP-2024--11--05-purple.svg)](https://ah.mphinance.com/mcp)
[![Tracked Capital](https://img.shields.io/badge/tracked%20capital-%24169M%2B-gold.svg)](https://ah.mphinance.com/whales)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

---

## 🎯 What is AfterMath?

AfterMath is an institutional-grade intelligence platform that audits retail social trading platforms by math rather than vibe.

The ecosystem combines four engines:
1. **Live Alt-Data Terminal**: Real-time tracking of 500 verified securities, 64 ETFs, and 395 verified whale accounts holding **$169,001,648.72** in verified brokerage equity.
2. **Model Context Protocol (MCP) Server**: Zero-dependency remote SSE and direct JSON-RPC server connecting Claude Desktop, Cursor, and autonomous AI agents directly to retail positioning data.
3. **High-Performance Edge API**: Sub-25ms edge-cached REST endpoints and OpenAPI 3.1 explorer documenting all data feeds.
4. **Forensic Autopsy Engine**: Lifetime audit of 33,090 posts across 40 traders measuring disclosure filters, phantom exits, and mechanical signal flow.

---

## ⚡ Live Production Terminal (`ah.mphinance.com`)

The production web interface delivers instant quantitative filtering across four primary terminal views:

- **[Live Equities & ETFs Leaderboard](https://ah.mphinance.com/stonks)**: 500 securities enriched with verified owner counts, total platform equity, whale capital backing, conviction intensity ($/holder), and chatroom activity.
- **[ETF & Index Tracker](https://ah.mphinance.com/etfs)**: 64 index funds, leveraged ETFs (`TQQQ`, `MSTU`, `NVDL`), cash reserves (`SGOV`), and crypto vehicles (`IBIT`).
- **[Verified Whale Directory](https://ah.mphinance.com/whales)**: 395 verified portfolios with liquid dry powder cash balances, today's P&L, open profits, and granular position breakdowns.
- **[Shadow Whales / Clout Inversion Index](https://ah.mphinance.com/shadow)**: Whales ranked by **Shadow Ratio** (`total_value / followers`). Unmasks silent millionaires who post minimal social noise while managing eight-figure books.

---

## 🤖 Model Context Protocol (MCP) Server

Connect any LLM, agent framework, or IDE directly to live AfterHour alt-data:

```bash
# Instant connection via mcp-remote proxy
npx -y mcp-remote https://ah.mphinance.com/sse
```

### Complete MCP Tools Available

| Tool Name | Purpose | Key Inputs |
|---|---|---|
| `get_market_tape` | Macro tape liquidity, whale cash reserves, inflow leaders | None |
| `get_top_equities` | Filter and rank 500 stocks and ETFs by capital, conviction, or volume | `sort_by`, `min_owners`, `limit` |
| `get_etf_flows` | 64 index and thematic ETFs with whale capital and expense ratios | `sort_by`, `limit` |
| `get_whale_portfolio` | Inspect verified positions, cost basis, profit, and cash for any whale | `username` |
| `get_ticker_intel` | Security dossier, whale holders list, and 90-day daily OHLCV bars | `ticker`, `include_bars` |
| `get_conviction_screener` | High dollar-per-holder accumulation radar | `min_intensity`, `min_owners` |

For detailed connection examples (Claude Desktop, Cursor IDE, Antigravity CLI, Python scripts), read the full [MCP Server Documentation](file:///home/mpha/projects/aftermath/docs/MCP.md).

---

## 📡 Edge REST API & Documentation

All API endpoints are public, zero-auth, CORS-unrestricted (`*`), and cached at the edge:

- **Interactive Swagger UI**: [https://ah.mphinance.com/docs](https://ah.mphinance.com/docs)
- **OpenAPI 3.1 Spec**: [https://ah.mphinance.com/api/openapi.json](https://ah.mphinance.com/api/openapi.json)
- **Comprehensive API Guide**: [docs/API.md](file:///home/mpha/projects/aftermath/docs/API.md)

### Key Endpoints

```bash
# Live Market Radar
curl -sL https://ah.mphinance.com/api/market.json

# All 500 Equities and ETFs
curl -sL https://ah.mphinance.com/api/stonks.json

# 395 Verified Whales and Millionaires
curl -sL https://ah.mphinance.com/api/whales.json

# Granular Ticker Dossier (e.g. ASTS)
curl -sL https://ah.mphinance.com/api/ticker/ASTS.json

# Direct JSON-RPC MCP Tool Execution
curl -s -X POST https://ah.mphinance.com/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_market_tape","arguments":{}}}'
```

---

## 🔬 The Forensic Study: The Disclosure Gap

The foundation of AfterMath began by scraping the complete lifetime post history of 40 active retail traders using **Artemis** (autonomous device capture) and feed ingestion: 33,090 total posts.

When you audit what traders actually disclose in public versus what happens to their trades, the structural reality appears:

```text
Positions announced as buys          3,660
Ever closed in public                1,739   (47.5%)
Never mentioned again as an exit     1,921   (52.5%)

Entry-language posts                 7,682
Exit-language posts                  4,948   (1.55 entries per exit)

Posts tagged Gain                    2,765
Posts tagged Loss                      233   (11.87 gains per loss)
```

### 1. The Missing Exit (52.5% Phantom Rate)
52.5% of every position announced as a buy never receives a closing post. It is never sold, never stopped out, and never admitted. The trade goes quiet, which is the empirical signature of a bagholder.

### 2. The 11.87:1 Gain/Loss Illusion
Traders post 11.87 gains for every 1 loss. Across multi-year market cycles, retail traders are not 12 times better at trading than they are bad at it. That ratio is not a performance record: it is a disclosure filter.

### 3. The LLM Scoring Hallucination
When identical post archives were evaluated across frontier models, the mean absolute score disagreement was 32.3 points:

```text
                    First Pass    Second Pass    Delta
@RyanLP                 89            14          -75
@terridactil            84            24          -60
@MarketVictor           88            31          -57
@mphinance              92            58          -34
@Drone_Daddy            72            41          -31
@AtypicallyErect        64            34          -30
@883Ismygovtname        79            58          -21
@Legitimate_Risk        68            58          -10
@NewFishBigPond         24            24            0
@Freeballer             18            33          +15
@Dallaslongcall         12            34          +22
```

Across all 40 traders, the correlation between an AI confidence score and real-world follow-through was only **0.20**. An unconstrained LLM grading prompt measures how persuasive a trader writes, not whether they have edge.

### 4. What Survived: The Mechanical Ingestion Matrix
Subjective scores were discarded in favor of mechanical behavioral extraction:

```text
@Tiger_
Classification: FUNDAMENTAL_QUALITY_COMPOUNDER / LEVERAGED_CONTRARIAN_DIP_BUYER

INGEST    Auto-tag any ticker moved above 10% disclosed portfolio weight
          as a high-quality candidate for fundamental verification.
          Rare, explicit "leverage on" declarations act as a contrarian
          bottom signal on market-wide risk sentiment.
FADE      Fade trim and rotation timing specifically, not stock selection.
FIREWALL  Zero stop-loss discipline. Single names routinely run 20-50%
          of book value.
EXIT      Tiered mechanical trim: bank 1/3 at +50%, 1/3 at +100%, trail rest.
```

---

## 🏗️ Production Infrastructure & Coolify Runbook

The terminal and MCP server run on Coolify infrastructure:

- **Host**: `coolify` (`5.161.247.12`)
- **Webroot**: `/home/mph/apps/ah-portal`
- **Routing**: Traefik with automated LetsEncrypt SSL over HTTP/2.
- **Containers**:
  - `ah-mphinance`: High performance `nginx:alpine` serving static web pages, SPA routing (`try_files $uri $uri/ /index.html;`), Swagger explorer, and edge JSON.
  - `ah-mcp`: Python 3.12 Alpine container exposing HTTP/SSE port `8089` for `/sse`, `/messages`, and `/api/mcp`.

### Build & Deploy Commands

```bash
# 1. Rebuild static HTML terminal and JSON datasets
python3 build_github_pages.py

# 2. Sync to Coolify production webroot
rsync -avz --delete \
  --exclude '.git' --exclude '__pycache__' --exclude 'afterhour.zip' --exclude 'data/following' \
  index.html default.conf sitemap.xml mcp_server.py api all stonks etfs whales shadow sitemap docs mcp \
  coolify:/home/mph/apps/ah-portal/

# 3. Reload Nginx container
ssh coolify "docker restart ah-mphinance"
```

---

## 📂 Repository Layout

```text
aftermath/
├── docs/                        # Comprehensive documentation
│   ├── API.md                   # REST API and endpoint specifications
│   ├── MCP.md                   # Model Context Protocol integration guide
│   └── index.html               # Swagger UI explorer
├── mcp_server.py                # Multi-transport MCP server (stdio, SSE, JSON-RPC)
├── build_github_pages.py        # Static terminal builder & JSON generator
├── api/                         # Pre-computed edge JSON API feeds
│   ├── market.json              # Macro tape liquidity & radar
│   ├── stonks.json              # 500 verified equities & ETFs
│   ├── etfs.json                # 64 verified ETFs & index funds
│   ├── whales.json              # 395 verified portfolios ($169M+ equity)
│   ├── shadow.json              # Clout Inversion index
│   ├── openapi.json             # OpenAPI 3.1 specification
│   └── ticker/                  # 500 individual ticker dossiers with OHLCV bars
├── mcp/                         # MCP landing page and web guides
├── followthrough.py             # Forensic entry-vs-exit calculator
├── afterhour.py                 # Resilient feed scraper client
├── data/                        # Raw historical post archives
└── reports/                     # Forensic quant dossiers and analysis
```

---

## 📜 Policies & Licensing

1. **Read-Only Intelligence**: Artemis automation and AfterMath tools are strictly read-only. Automated posting or commenting to live social feeds is prohibited.
2. **Affiliate & Partner Funnel**: Public interfaces route to [TraderMatrix Pro](https://www.tradermatrix.pro/?ref=MPHINANCE).
3. **License**: MIT License.
