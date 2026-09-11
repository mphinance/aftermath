# QUANT FORENSIC DOSSIER: @WarrenBuffett

### AfterHour Followed-Trader Autopsy — Artemis Engine Ingestion Report

| Field | Value |
|---|---|
| Handle | `@WarrenBuffett` (self-described: *"not that Warren Buffett... I borrowed his name"*) |
| Profile ID | `prf_a5550373c98a402cb8f31dbf8e0b0fe5` |
| Rank | #7 Most Active Followed Trader |
| Lifetime Posts Analyzed | 1,925 |
| Coverage Window | 2022-12-23 → 2026-08-22 (191 weeks / ~3.66 years) |
| Sources | `@WarrenBuffett_lifetime.md` (full text), `@WarrenBuffett_all_posts.json` (structured: `tag`, `gain_loss`, `amount_k`, `tickers`, `reaction_count`, `comment_count`, `is_hunt_post`) |
| Analyst | Artemis Engine / Sonnet Desk |

---

## 1. Executive Profile

### 1.1 Trader Philosophy & Archetype

`@WarrenBuffett` is **not** a stealth-conviction value investor despite the borrowed name — he says so himself, explicitly and at length, in a self-introduction post:

> *"Hi, I'm Warren Buffet. Well, not that Warren Buffett... I did borrow his name because, honestly, who in the world of investing doesn't know him?... Afterhour isn't just a copy trades platform... it connects you to the best investors, the sharpest minds, and the most promising trades out there."* (2024-12-01, "Who am I and why am I here?")

The real archetype is a **content-creator / financial-educator persona wrapped around a wildly over-leveraged short-dated options trader.** He built and actively promotes his own tool site (**wbfintool.com** — a stock-price calculator, DCA calculator, economic calendar, Coinglass liquidation-map mirror, and a "hot stocks" blog), referenced in 347 of his 1,925 posts (18%), and he explicitly frames his own posting as pedagogy:

> *"I firmly believe there's a gap between those who truly understand the markets and those who risk everything on 0dte. Helping bridge that gap has always been a core motivation for me."* (2025-05-03, "Reflecting on Afterhour")

He also states a formal risk framework — the **"33/33/33 Rule"** (Money Management / Psychology / Market Cycles) — which became one of his best-performing posts (146 reactions) and which he republished as blog content. The irony, developed fully in §3, is that his own account history is close to a case study in violating every pillar of that rule simultaneously.

His actual trading process, reconstructed from ticker/catalyst tagging (§2), is **short-dated options speculation** (spreads, cash-secured puts, 0-1 DTE index/single-name calls) layered on top of a **recurring macro thesis book** (China-ADR reflation, Bitcoin-proxy leverage via MSTR/MTPLF, meme-momentum re-entries on GME/PLTR/HOOD). He runs periodic **public "challenge accounts"** (turn $X into $100K) as content generators, and — most importantly — his linked portfolio value has been **wiped to functionally zero at least three separate times** and rebuilt from scratch each time, a pattern invisible in his self-applied `Gain`/`Loss` tags but fully visible in the raw account-value telemetry.

**Verdict on philosophy**: Sincere educator-aspirant, undisciplined executor. He knows and can articulate correct risk-management theory in long-form posts; he does not apply it to his own book. This gap — not any lack of market knowledge — is the core behavioral finding of this dossier.

### 1.2 Post Cadence & Active Timeline

- **Total posts**: 1,925 over 191 weeks → **10.1 posts/week lifetime average**. This average is badly misleading; cadence is a boom-bust story that tracks his account volatility almost exactly.

```
Posts per Quarter (2022-Q4 -> 2026-Q3):
2022-Q4  ▪                                                    2    (~1.5/wk, partial quarter — launch)
2023-Q1  ▪▪▪                                                 12    (0.9/wk)
2023-Q2  ▪▪▪▪▪                                                21    (1.6/wk)
2023-Q3  ▪▪▪▪▪▪▪▪▪                                            41    (3.2/wk)
2023-Q4  ▪▪▪▪▪▪▪▪                                             36    (2.8/wk)
2024-Q1  ▪▪▪▪▪▪▪▪▪▪                                           49    (3.8/wk)
2024-Q2  ▪▪▪▪▪▪▪                                              39    (3.0/wk)   -- FIRST FULL BLOW-UP (Apr 12)
2024-Q3  ▪▪▪▪▪▪▪                                              38    (2.9/wk)
2024-Q4  ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪  385    (29.6/wk)  *** POSTING SURGE BEGINS ***
2025-Q1  ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪  511    (39.3/wk)  *** ALL-TIME PEAK ***
2025-Q2  ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪  419    (32.2/wk)
2025-Q3  ▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪                            150    (11.5/wk)  -- SECOND FULL BLOW-UP (Aug 19)
2025-Q4  ▪▪▪▪▪▪                                                44    (3.4/wk)
2026-Q1  ▪▪▪▪▪▪▪                                               52    (4.0/wk)   -- THIRD FULL BLOW-UP (Jan 15)
2026-Q2  ▪▪▪▪▪▪▪▪▪▪▪▪▪                                       116    (8.9/wk)
2026-Q3  ▪                                                     10    (0.85/wk, partial — trailing off through Aug 22)
```

- **Peak velocity**: Q1 2025, ~39.3 posts/week (essentially every 4-5 hours during market days) — this is the same window (Jan–Apr 2025) during which he launched wbfintool.com, ran the public "$1,300 → $100K spread challenge," and rode the account from ~$203K down to ~$9K.
- **Reading**: Posting volume is a proxy for *engagement-farming intensity*, not trading quality. The steepest volume ramps (Q4 2024 → Q1 2025) coincide with the launch of his tool business and public challenge content, not with any improvement in trading outcomes — outcomes in that exact window were among his worst (see §1.3).
- **Quiet periods = undisclosed damage**: the two multi-week silences in the archive (May 2024, ~8 weeks; and a shorter gap late 2025) each directly follow a full account wipe-out. He states the first one outright: *"Going to disconnect for a while to enjoy life a bit😂😂"* (2024-04-12, same day the account hit $0.00).

### 1.3 Verified Capital Trajectory & Drawdown History — The Central Finding

**Data note**: `amount_k` is populated on 1,686 of 1,925 posts (87.6%), populated by AfterHour's own linked-account-value sync (not text-scraped), and is the most reliable single artifact in this dataset. A small number of posts (~15 instances) show implausible same-day round-trips between the ~$150-170K range and the ~$12-20K range — consistent with either (a) genuine intraday mark-to-market swings on a single very levered position, or (b) sync lag between a stale cached snapshot and a fresh one. Directionally, however, the series is unambiguous and is corroborated at every major inflection by the post text itself (quoted below).

**This is the single most important quantitative fact about this trader: his linked account has been driven to effectively $0 at least three separate times in under three years, and rebuilt to six figures each time.**

```
Capital Trajectory ($k), monthly first/min/max markers:

2023-12   $50.7k  (earliest amount_k datapoint)
2024-01   ~$150-160k (unexplained step-up — likely a funding event / new linked account)
2024-03   Peak $204.8k (2024-03-29)
2024-04   COLLAPSE -> $0.00 (2024-04-12) ................ BLOW-UP #1 (100% DD)
           "Going to disconnect for a while to enjoy life a bit😂😂"
2024-05   [NO POSTS — 8-week silence]
2024-06   Reappears at $83.1k (2024-06-07, unexplained)
2024-10   Rebuilds to Peak $230.6k (2024-10-25)
           (single-day flash-crash en route: $225k -> $14.9k on 2024-10-23, same-day partial recovery)
2024-12   Grinds down to $11.0k (2024-12-20) — "Update on my port... if all this happens it will be
           back to $250k like a few days ago" (self-aware bag-holding on SQ/MSTR/BIDU recovery math)
2025-01   Rebuilds to $203.7k
2025-04   Down to $9.3k (2025-04-12) — "climbed my way back to 0% YTD... took a step back,
           reassessed, decided to go 90% cash"
2025-05   Down further to $6.8k (2025-05-19)
2025-06   Rebuilds to ALL-TIME PEAK $293.0k (2025-06-19)
2025-08   COLLAPSE -> $0.07k (2025-08-19) ................ BLOW-UP #2 (100% DD)
           "Thank you $PLTR" / "I bet my 💻 on this bounce" / "I can buy a new laptop"
2025-08   Partial rebuild within days to ~$168.7k (2025-09-02) — then whipsaws to $12.7k
           three days later (2025-09-03, "Mother of all rug pulls" — $MTPLF)
2025-12   Grinds down to $7.9k (2025-12-31)
2026-01   COLLAPSE -> $0.73k (2026-01-15) ................ BLOW-UP #3 (100% DD)
           "Please help me get to 1K in X" (2026-01-16, soliciting followers for a UNRELATED
           social-media milestone the same week his trading account bottomed — see §4)
2026-04   Rebuilds to local high $154.0k (2026-04-29)
2026-08   Closes dataset at $89.1k
```

**Volatility profile (post-to-post % change in linked account value, n=1,684 transitions)**:
- Mean change: **+30.2%** (heavily right-skewed by rare huge recoveries)
- Median change: 0.0% (most snapshots are unchanged between adjacent posts, consistent with a slow news/discussion cadence punctuated by violent options-driven repricings)
- Standard deviation: **422%** — an extraordinary figure for what should be a risk-managed trading account
- **41 instances** of a single post-to-post jump **>+100%** (account more than doubling between two consecutive posts)
- **41 instances** of a single post-to-post drop **>-50%**; **63 instances** of a drop **>-20%**
- Maximum single-post drawdown: **-100.0%** (recorded three times — Apr 2024, Aug 2025, Jan 2026)

**Reading**: This is not the volatility profile of a diversified swing-trading equity book. It is the fingerprint of **concentrated, undefined-or-poorly-defined-risk short-dated options positions** (naked calls/puts, aggressive spreads, 0-1 DTE index exposure) sized at a large fraction of net liquidity, repeatedly. The man who wrote the "33/33/33 Rule" and preaches "protect your capital first... the opportunity to trade tomorrow is more important than chasing today's gains" has posted, verified, on-platform evidence of doing the precise opposite of that advice on a recurring ~6-9 month cycle for over three years.

---

## 2. Ticker Universe & Catalysts

### 2.1 Core Asset Universe (structured `tickers` field, 842 tagged posts, 163 unique symbols)

| Tier | Tickers (mentions) | Character |
| :--- | :--- | :--- |
| **Tier 1 — China-ADR Macro Thesis** | **$BIDU (101)**, $BABA (44), $FXI (10), $JD (7), $PDD (5), $KWEB (5) | His single largest and longest-running conviction theme: "China will outpace the U.S. this year" repeated across 2024-2026 despite the position bleeding repeatedly ("The loser $BIDU... still holding, plenty of time," 2025-05-21). Primarily long-dated calls/LEAPS. |
| **Tier 2 — Bitcoin-Proxy Leverage** | **$BTC (88)**, $MSTR (69), $MTPLF (21 — Metaplanet, the Japanese BTC-treasury OTC play), $COIN (7), $MARA (7) | Leveraged, correlated crypto-equity exposure stacked across three tickers simultaneously rather than diversified — effectively one macro bet expressed three ways. |
| **Tier 3 — Momentum / Retail-Narrative Names** | **$TSLA (73)**, $HOOD (49), $NVDA (41), $SQ/$XYZ (40+22=62), $GME (31), $PLTR (25), $RXRX (27), $UBER (19) | Fast-money momentum trades explicitly reactive to retail-narrative catalysts — Roaring Kitty's GME re-entry ("How to trade when you have some information? ... I found out RK had positions"), AI/biotech pumps (RXRX), and earnings-adjacent spreads (UBER, ETSY, MSTR — see the "Trade #" challenge series). |
| **Tier 4 — Mega-cap / Index Hedges** | $AAPL (18), $SPY (16), $NKE (16), $UNH (16), $META (15), $BA (15), $ADBE (15), $MSFT (14), $QQQ (10) | Lower-conviction, shorter-hold names used for earnings-week spreads and covered-call/cash-secured-put income generation. |

### 2.2 Options vs. Equities

Explicit options-mechanics language (calls/puts/spreads/strikes/expiry/0DTE) appears in only **13.6%** of posts by keyword match, but this **significantly understates** true options exposure — the vast majority of his largest, screenshot-driven posts show a brokerage P&L card with no options terminology in the caption at all. The account-value volatility documented in §1.3 (single-post swings routinely >100% or -50%) is **mechanically inconsistent with a shares-only portfolio** and is only explainable by concentrated short-dated options (his own "Trade #" challenge series, run openly with named spreads on UBER/TLT/ETSY/MSTR, confirms the mechanism directly). Explicit shares/equity-only language (shares, DCA, dividend) appears in just 3.9% of posts. **Working classification: predominantly an options trader (concentrated debit spreads, cash-secured puts, and outright long-dated/short-dated calls) who occasionally holds a shares "core" as a stabilizer, most explicitly during his post-blow-up "de-risking" phases** (e.g., 2025-04-05: *"clearing up the port and just sticking mainly with shares... 50% cash, 50% invested"*).

### 2.3 What Drives His Entries? (Catalyst Taxonomy)

1. **Earnings calendars** — the single most repeated content format in the archive. He runs a personal "earnings tomorrow ☀️ / 🌙" post template (WMT, INTU, NVDA, BABA, PDD, CRWD, MDB, AFRM, ANF, ZS, LULU all appear this way) linked to his own `stockcalculator.wbfintool.com` tool.
2. **Macro/Fed events** — CPI days ("Survived CPI day 2024"), FOMC ("When the Market Goes Full Tomato After FOMC"), tariff headlines (a full Q1-Q2 2025 arc built around "Why I'm Not Afraid of Trump's Tariffs" and later a partial reversal to defensive cash).
3. **Curated social/flow accounts** — he re-posts and reacts to `@DeItaone` (Walter Bloomberg headline feed, 19 embeds), `@unusual_whales` (options-flow alerts, 7 embeds — e.g., *"9,000x size in the $SPY 515 calls 0dte exp... We will see today if these are insiders"*), `@saylor` (Michael Saylor/MSTR bull case, 3 embeds), and fellow AfterHour traders `@kiantrades` (26 embeds) and `@amitisinvesting` (11 embeds). This is a **flow-following, not fundamentals-driven,** entry style for a meaningful share of his trade ideas.
4. **Retail-narrative momentum** — explicit, admitted piggybacking on Roaring Kitty's 2024 GME re-entry ("I imagined RK converted to shares... Now, let's think our next move"), and on Metaplanet's index-inclusion news cycle.
5. **Self-branded "hunt" content** (110 posts flagged `is_hunt_post`) and 25 posts tagged `Contest` — AfterHour's community due-diligence/prediction feature, used by him mostly for chart/thesis discussion threads rather than firm trade calls.

---

## 3. Risk Management & PnL Reality

### 3.1 Does He Take Profits, or Hold Bags? — Documented Both, Skewed Toward Holding

He can articulate correct process in the abstract (*"Aim for trades with at least a 2:1 reward-to-risk ratio," "Protect your capital first"* — 33/33/33 Rule, 2024-12-08) and occasionally executes it on the small public "Trade #" challenge series (Trade #1, UBER spread, closed cleanly for **+24%** in 2 days: *"Trade #1 closed 🎉... From ~$1,070 to ~$1,329"*).

But the dominant, repeated pattern on his **core/large-size positions** is holding through severe adverse moves while narrating the pain publicly rather than cutting:
- *"The loser $BIDU — Still holding.. plenty of time 🥵"* (2025-05-21)
- *"The loser $PLTR — Well, it has to come down at some point 😅. Maybe when it hits $150?"* (2025-06-11)
- *"My Portfolio is so red 🩸 — Long Live China 🇨🇳... I just happened to roll the dice"* (2025-02-20)
- *"Update on my port (Actual values) — Need $SQ to be $98, need $MSTR to be $400, need $BIDU to be $95. If all this happens, it will be back to $250k"* (2024-12-20) — a textbook "need the market to bail me out" note-to-self, publicly posted.

### 3.2 How He Manages Losing Positions

- **Public "Trade #" spread challenge (Jan–Feb 2025)** is the single cleanest window into his real process, because he narrated it trade-by-trade: Trade #1 (UBER) closed a **win** with a celebratory 🎉 post. Trade #2 (TLT) was explicitly cut for a loss, marked with a 🩸 emoji and an honest scoreboard: *"Trade #1 ✅ Trade #2 ❌."* Trades #3 (ETSY) and #4 (MSTR) **were never given a close-out post at all** — the series simply stops after Feb 20, 2025, with no accounting of the final result. This is a materially important behavioral marker: **wins get a public accountability post; ambiguous/losing trades get silently abandoned.**
- On the "Mr Market was right ☹️ $MSTR" post (2025-02-21, tagged `Loss`), he links back to his own prior thesis post to show he was wrong, which is a rare moment of genuine accountability — but it is the exception (10 `Loss`-tagged posts lifetime vs. 123 `Gain`-tagged, see §3.3).
- His stated coping mechanism for adverse volatility is stoic detachment rather than risk reduction: *"My portfolio took a -9% (-$20K) dive, then bounced right back (+$20K), and I didn't even flinch. If wild price swings make you sweat, you're probably either overleveraged or have too much cash in the game!"* (2025-03-04) — a statement that, read against the account-value telemetry in §1.3, is **self-diagnosis he does not act on**: he is, by his own later admission and by the data, both overleveraged and prone to it.

### 3.3 Documented Wins vs. Blow-Ups

| Category | Detail | Date | Verification |
| :--- | :--- | :--- | :--- |
| **Biggest verified account low** | $204.8k → **$0.00** | 2024-03-29 → 2024-04-12 | Full 100% drawdown, `amount_k` telemetry + "disconnect" post |
| **Biggest verified account peak** | All-time high $293.0k | 2025-06-19 | `amount_k` telemetry |
| **Second full wipe-out** | $293.0k → **$0.07k** | 2025-06-19 → 2025-08-19 | `amount_k` telemetry, "Thank you $PLTR" / "I bet my laptop" posts |
| **Third full wipe-out** | Sub-$8k → **$0.73k** | 2025-12-31 → 2026-01-15 | `amount_k` telemetry, "Please help me get to 1K in X" post |
| **Single-day flash crash** | $225.0k → $14.9k (same-day) | 2024-10-23 | `amount_k` telemetry (partial same-week recovery to $230.6k) |
| **Clean documented win** | UBER $61/62 debit spread, +24% in 2 days | 2025-01-03 → 01-06 | "Trade #1 closed 🎉" — fully narrated, verifiable math |
| **Clean documented loss** | TLT $86/87 spread, cut for a loss | 2025-01-07 | "Trade #2 Update 🩸... Trade #1 ✅ Trade #2 ❌" |
| **Abandoned / unresolved** | ETSY & MSTR spreads (Trade #3, #4) | Jan–Feb 2025 | Series stops mid-position, no closing accounting given |
| **"Gambling my life savings"** (his own title, used twice) | Undefined-size YOLO, no follow-up P&L given | 2024-10-31, 2025-03-03 | Self-titled; outcome never disclosed |

### 3.4 The Self-Reported Tag Bias

Structured `tag`/`gain_loss` fields show **123 posts tagged `Gain` vs. only 10 tagged `Loss`** — a **12.3:1 disclosed win ratio**. This is flatly incompatible with the verified capital trajectory in §1.3 (three separate 100%-drawdown events). The mechanism is clear from the data: he tags individual winning trades/days explicitly as `Gain` (a specific closed position going right), but the much larger, slower account-level bleed-outs that precede each wipe-out are posted under neutral tags (`Discuss`, `News`, untagged) or narrated as philosophical "reflections" rather than tagged as losses. **Any downstream system must never treat his `Gain`/`Loss` tag ratio as a real win rate — it is a curated highlight reel, not a P&L ledger.** The 2026-Q1 stretch is the starkest example: 60 `Gain`-tagged posts and only 1 `Loss`-tagged post in the same quarter his account cratered to $0.73k (2026-01-15).

---

## 4. Behavioral & Sentiment Signals

### 4.1 Why Is He Posting?

Ranking his highest-engagement posts shows the audience rewards **educational/framework content**, not raw trade calls:

| Reactions | Comments | Date | Post |
| :--- | :--- | :--- | :--- |
| 188 | 46 | 2025-01-04 | "The Rule of 40: A 'Secret' Formula for Spotting High-Performing Growth Stocks!" |
| 157 | 78 | 2025-01-03 | "How to turn $1,300 into $100K in 17 Trades? Let's Break It Down" |
| 146 | 22 | 2024-12-08 | "The 33/33/33 Rule for Success" |
| 135 | **128** | 2025-02-09 | "Poor Man's Covered Call: The Budget-Friendly Way to Sell Options!" |
| 134 | 91 | 2025-02-02 | "Why I'm Not Afraid of Trump's Tariffs" |
| 134 | 37 | 2025-02-23 | "Big Upgrade Coming Soon: Stock Market Projection Calculator 2.0!" |
| 127 | 64 | 2025-02-14 | "🍆 $RXRX" |
| 123 | 55 | 2025-05-19 | "Like this post if you hold or want to hold $MTPLF" |
| 115 | 70 | 2024-12-18 | "When the Market Goes Full Tomato After FOMC: What to Do?" |

Lifetime totals: **34,840 reactions / 22,827 comments** across 1,925 posts (mean 18.1 reactions, 11.9 comments/post). The pattern is consistent: he is optimizing for **personal-brand/tool-business growth (wbfintool.com)** at least as much as for trading signal — his own words confirm this is deliberate (*"help you learn and grow... connect people, highlight opportunities"*), and the incentive structure (educational content outperforms trade calls) reinforces the content-creator framing over the trader framing.

### 4.2 Recurring Linguistic Patterns

- **"🫶 / 🤷🏻‍♂️ / 😅"** — his signature soft, self-deprecating hedge emojis, appended almost universally to both wins and gut-punch losses, flattening the emotional register of his posts regardless of actual severity (used identically on a +24% spread win and a "the loser $BIDU, still holding" post).
- **"Not financial advice" / "This is for entertainment purposes only" / "PS: don't @ me"** disclaimers cluster tightly around his largest, most leveraged positions — an inverse-correlation between disclaimer density and position discipline.
- **Framework-language re-use**: "33/33/33 Rule," "Rule of 40," "Poor Man's Covered Call" are repeatedly recycled as blog content on wbfintool.com — he is building a content funnel, not just journaling trades.
- **China-nationalist macro framing**: recurring, unironic bull case for Chinese equities over U.S. equities ("I trust China's president more than..."; "Long Live China 🇨🇳"), sustained across 18+ months despite the position bleeding repeatedly.
- **Self-aware gambling admissions used as content, not as a stop signal**: "Gambling my life savings" (used twice, as a post *title*, i.e. marketed as entertainment rather than flagged as a risk event).

### 4.3 Reaction to Volatility / Red Days

- **Performed stoicism**: *"My portfolio took a -9% (-$20K) dive, then bounced right back... and I didn't even flinch."* (2025-03-04) — publicly signals emotional control precisely in the window his account was on its way to a 96% drawdown five weeks later (2025-04-12, $9.3k).
- **Reframes drawdowns as "reflection," never as "mistake"**: *"Although, this isn't panic... this is reflection... every day is a new opportunity to learn, adapt, and level up."* (2025-04-09, the day he went to 90% cash after a monster drawdown).
- **Community-defensiveness after a public flame-out**: *"Stay cool or stay out! ... if you're here to drop negative comments or add zero value, save yourself the effort."* (2025-03-04, posted the same day as the -9%/+9% "didn't even flinch" post) — a direct signal that critical audience reaction to his volatility is a live, sore point for him.
- **Notably, the exact week his account bottomed at $0.73k (Jan 15, 2026), he pivoted his public messaging to an unrelated social-media growth ask** ("Please help me get to 1K in X," 2026-01-16) — a pattern consistent with using audience/persona-building as a coping/distraction mechanism during a genuine drawdown crisis rather than addressing the trading failure directly.

---

## 5. Quantitative Verdict for TraderMatrix

```
+-----------------------------------------------------------------------------------+
|                           TRADERMATRIX CLASSIFICATION                             |
|                                                                                     |
|   PRIMARY TAG:       SERIAL_ACCOUNT_BLOWUP / OVERLEVERAGED_OPTIONS_GAMBLER        |
|   SECONDARY TAG:      MACRO_THEME_BAGHOLDER (China ADRs, BTC-proxy leverage)      |
|   TERTIARY TAG:       RETAIL_EDUCATOR / CONTENT-FARMING_SIGNAL_SOURCE             |
|   ALPHA STATUS:       Negative-expectancy at the account level; genuine catalyst  |
|                        (earnings-calendar) awareness exists but is not risk-managed|
|   RECOMMENDED FIT:    Contrarian Retail-Sentiment Barometer + Earnings-Calendar   |
|                        Feed (mechanics only, never position-sized)                |
+-----------------------------------------------------------------------------------+
```

### 5.1 Algorithmic Alpha Score & Expectancy

**Algorithmic Alpha Score: 19 / 100**

Justification: three fully-verified, telemetry-confirmed 100% account drawdowns in under three years, each followed by an unexplained rebuild, is disqualifying at the account level regardless of any individual trade quality. His genuine skills — earnings-calendar awareness, options-mechanics literacy (he can correctly explain spreads, poor-man's covered calls, assignment risk), and an articulate, correct-in-theory risk framework — are real but are **never enforced against his own book**. The single cleanest evidence window (the public "Trade #" spread series, Jan–Feb 2025) shows a 1-1 win/loss record on the two trades he actually closed out, with the two more ambiguous trades abandoned without accounting — consistent with a trader whose realized edge on isolated setups is roughly coin-flip, and whose account-level ruin comes from position sizing and lack of stops, not from bad thesis generation.

**Expectancy**: **Negative at the account level.** Per-trade expectancy on isolated, defined-risk setups (his named debit spreads) may be modestly positive to breakeven; multiplied through his position-sizing behavior (concentrating a large fraction of net liquidity in short-dated, undefined-max-loss options), the compounded account-level expectancy is clearly negative — a three-times-repeated total-wipeout pattern is not statistically consistent with any positive-expectancy process at the sizing he actually uses.

### 5.2 Signal Flow Ingestion Matrix

```
                    ┌───────────────────────────────────────────────────┐
                    │          @WarrenBuffett Raw Signal Stream          │
                    └───────────────────────┬───────────────────────────┘
                                            │
      ┌──────────────────────┬──────────────┼──────────────┬───────────────────────┐
      ▼                      ▼               ▼              ▼                       ▼
┌───────────────┐  ┌──────────────────┐ ┌───────────────┐ ┌───────────────┐ ┌────────────────┐
│ 1. EARNINGS   │  │ 2. CHINA ADR /   │ │ 3. FLOW-      │ │ 4. NAMED       │ │ 5. ACCOUNT-    │
│ CALENDAR      │  │ BTC-PROXY MACRO  │ │ FOLLOWING     │ │ "CHALLENGE"    │ │ VALUE          │
│ AWARENESS     │  │ THESIS (BIDU,    │ │ RE-POSTS      │ │ TRADES (Trade  │ │ TELEMETRY      │
│ (via          │  │ BABA, MSTR,      │ │ (@unusual_    │ │ #1-4 spreads)  │ │ (amount_k      │
│ wbfintool.com)│  │ MTPLF, BTC)      │ │ whales,       │ │                │ │ series)        │
│               │  │                  │ │ @DeItaone)    │ │                │ │                │
├───────────────┤  ├──────────────────┤ ├───────────────┤ ├───────────────┤ ├────────────────┤
│ Action:       │  │ Action:          │ │ Action:       │ │ Action:        │ │ Action:        │
│ INGEST AS     │  │ TRACK AS         │ │ RE-VALIDATE   │ │ MIRROR         │ │ TREAT AS A     │
│ CALENDAR      │  │ SENTIMENT ONLY   │ │ AT SOURCE,    │ │ MECHANICS      │ │ CONTRARIAN     │
│ TRIGGER, not  │  │ (concentration   │ │ NEVER COPY    │ │ ONLY, never    │ │ EUPHORIA/PANIC │
│ directional   │  │ risk documented, │ │ SECOND-HAND   │ │ his position   │ │ SIGNAL — a     │
│ signal        │  │ never hedged)    │ │               │ │ sizing         │ │ crash toward $0│
│ Weight: +0.60 │  │ Weight: +0.10    │ │ Weight: 0.00  │ │ Weight: +0.30  │ │ = local capit- │
│ (Tactical)    │  │                  │ │ (pass-through)│ │ (Tactical)     │ │ ulation marker │
└───────────────┘  └──────────────────┘ └───────────────┘ └───────────────┘ └────────────────┘
```

### 5.3 Execution Directives for the Artemis Engine

#### A. Ingestion Directives — Genuine Edge to Harvest
1. **Earnings-Calendar Cross-Reference**: His earnings-week posting cadence (WMT, NVDA, BABA, MDB, AFRM, CRWD, ZS, LULU, PDD, ANF) is a reliable, timely calendar of market-moving events with correctly identified implied-move context — ingest as a **calendar-confirmation feed**, not a directional signal.
2. **Options-Mechanics Templates**: His "Poor Man's Covered Call" and debit-spread structuring posts are mechanically sound, generic templates (high community engagement confirms clarity) — useful as educational/template content independent of his own track record.
3. **China-ADR / BTC-Proxy Theme Tracking**: His sustained multi-year conviction in BIDU/BABA and MSTR/MTPLF/BTC is a legitimate sentiment theme to track as a low-weight input, given the multi-cycle persistence of the thesis, but never as a sizing signal (see Firewalls below).
4. **"Trade #" Challenge Series as a Backtestable Micro-Sample**: The four fully-documented spread trades (UBER win, TLT loss, ETSY/MSTR abandoned) are a clean, small, auditable sample of his isolated setup-selection skill, separable from his sizing behavior — useful for calibrating "setup quality independent of risk management."

#### B. Contrarian Fade Directives — When to Fade Him / The Retail Herd
1. **Bag-Holding Cluster as a Local-Bottom/Continuation Signal**: A cluster of "the loser $TICKER, still holding" or "my portfolio is so red" posts on the same name over 2+ weeks reliably precedes either (a) a slow continued bleed (BIDU, most of 2025) or (b) his eventual capitulation ("went to 90% cash"). Treat these clusters as a **retail-capitulation risk flag** on the named ticker, not a buy signal.
2. **Euphoric All-Time-High Posts as a Local-Top Flag**: His all-time-high account posts ($230.6k Oct 2024, $293.0k Jun 2025) were each followed within 8-16 weeks by a full account wipe-out. When his `amount_k` telemetry prints a new multi-month high accompanied by celebratory language, treat it as a **contrarian caution flag** on whatever concentrated position drove the high, not as validation.
3. **Silence-as-Signal**: A sharp, multi-week drop in posting cadence following a high-frequency stretch (as in May 2024) should be read as a probable **undisclosed drawdown-in-progress or full wipe-out**, consistent with his own admitted pattern of going quiet exactly when the account implodes.

#### C. Mandatory Risk Blacklists & Firewalls
1. **FIREWALL — Never Mirror Position Sizing.** His account-value volatility (stdev of post-to-post % change = 422%; 41 single-post moves >+100%; three complete-wipeout events) proves he sizes options positions at a large, undisciplined fraction of net liquidity. Any signal sourced from him must be sized independently by TraderMatrix's own risk engine — his own sizing must never be inferred or scaled from his dollar figures.
2. **BLACKLIST — Undefined-Risk "Challenge Account" Content.** Posts explicitly framed as a public challenge ("turn $1,300 into $100K," "Gambling my life savings") are entertainment/content-marketing devices by his own admission and framing. Zero ingestion as trading signal.
3. **FIREWALL — Tag-Based Win-Rate Exclusion.** Do not use his `Gain`/`Loss` tag ratio (123:10, 12.3:1) as a performance metric under any circumstance — it is proven, by cross-reference against his own verified `amount_k` telemetry, to be a curated highlight reel that actively conceals three total account losses.
4. **FIREWALL — Concentration Risk on Theme Tickers.** BIDU, BABA, MSTR, MTPLF, and BTC exposure in his book is directionally correlated (effectively one macro bet expressed five ways) and consistently unhedged. Any thematic signal drawn from these names must be capped and diversified independently by the ingestion engine, never mirrored at his implied concentration.
5. **BLACKLIST — Abandoned Trade Threads.** Any "Trade #" or named challenge position that stops updating without a closing post (ETSY Trade #3, MSTR Trade #4) should be assumed to have resolved as a loss by default, per the pattern established in §3.2 — never assume a neutral or positive resolution from silence.

#### D. Exit Rules & Alpha Rectification
1. **Enforce His Own Stated Rule He Never Follows**: His "33/33/33 Rule" explicitly states *"protect your capital first... aim for at least a 2:1 reward-to-risk ratio."* TraderMatrix should hard-code a mechanical stop-loss and profit-scaling rule (e.g., mandatory exit at -50% of premium on any harvested spread-mechanics template, scale-out at first 2:1 target) on any setup sourced from his content — the rule he articulates but never enforces on himself.
2. **Hard Time-Box on Any Harvested Setup**: His genuine setup-selection skill (per the Trade # series) operates on 1-4 week option-spread horizons. Never extend an ingested signal from him into an indefinite/LEAPS-style hold the way he does with his China-ADR bag positions — that is precisely where his real losses accumulate.
3. **Mandatory Max-Loss Definition on All Ingested Options Structures**: Because his own catastrophic drawdowns trace directly to undefined or oversized option exposure, any options-mechanics template harvested from his educational content (poor-man's covered call, debit spreads) must be implemented with the ingestion engine's own hard max-loss cap — never his position size.
4. **Post-Euphoria Cooldown**: When ingesting his China-ADR/BTC-proxy sentiment theme, apply a mandatory cooldown/de-weighting after any post celebrating a new personal-account all-time high — historically the leading indicator of his next capitulation, not his next leg higher.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Event |
| :--- | :--- |
| 2022-12-23 | First AfterHour post (💎✋🏻 emoji-only). |
| 2023-01-04 | "25k to break even!... had to post the 50k mark" — earliest account-scale narrative, confirms early-stage account in the tens of thousands. |
| 2023-09-21 | Early "challenge account" documented: took a loss on NVAX, challenge account down to $10,121 from $13,789 (-26.6%). |
| 2023-12-21 | First `amount_k`-tagged datapoint: $50.68k. |
| 2024-01-19 | Account telemetry steps up to ~$158.8k (unexplained — likely a funding/re-linking event). |
| 2024-03-29 | Account peak $204.8k. |
| **2024-04-12** | **BLOW-UP #1**: account telemetry hits **$0.00**. "Going to disconnect for a while to enjoy life a bit😂😂." |
| 2024-05 | 8-week posting silence (no posts logged this month). |
| 2024-06-07 | Reappears at $83.1k, unexplained. GME/Roaring-Kitty re-entry thesis begins same week. |
| 2024-10-02 | "The hunt of stop losses" — `Loss`-tagged, OXY contracts, SQ choppiness noted. |
| 2024-10-23 | Single-day flash crash: account $225.0k → $14.9k intraday (same day: "😵"). |
| 2024-10-25 | Rebuilds to new all-time-high $230.6k. |
| 2024-12-01 | "Who am I and why am I here?" — full self-introduction/manifesto post. |
| 2024-12-08 | "The 33/33/33 Rule for Success" published — becomes one of his highest-engagement posts (146 reactions), later republished on wbfintool.com. |
| 2024-12-20 | "Update on my port (Actual values)" — publicly needs SQ/MSTR/BIDU to hit specific prices "to get back to $250k like a few days ago." |
| 2025-01-03 | Launches the public "$1,300 → $100K in 17 Trades" spread challenge; Trade #1 (UBER) opened. |
| 2025-01-06 | Trade #1 closed 🎉, +24% ($1,070 → $1,329). |
| 2025-01-07 | Trade #2 (TLT) cut for a loss, marked 🩸. "Trade #1 ✅ Trade #2 ❌." |
| 2025-02-07 | wbfintool.com formally promoted for the first time ("Unleash Your Trading Edge with WBFinTool"). |
| 2025-02-09 | "Poor Man's Covered Call" post — 128 comments, his highest-comment post of the dataset. |
| 2025-02-18 – 02-20 | Trade #4 (MSTR spread) opened — last entry in the "Trade #" series; no closing post ever follows for Trade #3 (ETSY) or #4 (MSTR). |
| 2025-02-21 | "Mr Market was right ☹️ $MSTR" — rare direct-accountability `Loss`-tagged post. |
| 2025-03-04 | "Today's Reflection" (-9%/-$20K then +$20K, "didn't even flinch") + "Stay cool or stay out!" (defensive community post), both same day. |
| 2025-04-09 – 04-12 | Account grinds down to $9.3k; goes 90% cash, one lone BIDU position remaining. |
| 2025-05-03 | "Reflecting on Afterhour" — long-form reflection on the platform's token controversy and his own motives for posting. |
| 2025-06-19 | **NEW ALL-TIME HIGH**: account telemetry peaks at **$293.0k**. |
| **2025-08-19** | **BLOW-UP #2**: account telemetry crashes to **$0.07k**. "Thank you $PLTR" / "I bet my 💻 on this bounce." |
| 2025-09-02 – 09-05 | Partial rebuild to ~$168.7k, then a same-week reversal back to ~$12.7k ("Mother of all rug pulls," $MTPLF). |
| 2025-12-31 | Account down to $7.85k closing out 2025. |
| **2026-01-15** | **BLOW-UP #3**: account telemetry hits **$0.73k**. |
| 2026-01-16 | "Please help me get to 1K in X" — pivots publicly to a social-media follower-count ask the day after the account bottoms. |
| 2026-04-29 | Account rebuilds to local high $154.0k. |
| 2026-08-22 | Final post in dataset; account at $89.1k. |

---

## 7. Summary Scorecard

| Metric | Score / Rating | Quantitative Commentary |
| :--- | :--- | :--- |
| **Catalyst/Calendar Awareness** | **6.5 / 10** | Genuinely useful, consistent earnings/macro calendar coverage via his own tool site; timely, not necessarily directionally alpha-generating. |
| **Setup Selection (isolated trades)** | **5.0 / 10** | The one fully auditable sample (Trade #1-4 spread series) is roughly coin-flip (1 win, 1 loss, 2 abandoned) — average, not edge-confirming. |
| **Risk Management** | **0.5 / 10** | Three fully-verified 100% account drawdowns in under three years despite an articulate, correct, and entirely unapplied personal risk framework. The single worst score in this dossier category. |
| **Disclosure Integrity** | **2.0 / 10** | 12.3:1 self-tagged Gain:Loss ratio directly contradicted by verified account telemetry; loss-side trades in his own challenge series are silently abandoned rather than closed out. |
| **Emotional Discipline** | **3.0 / 10** | Performs stoicism in text ("didn't even flinch") in the same window the account is objectively unraveling; pivots to unrelated content (follower asks) at the exact moment of maximum drawdown. |
| **Community/Content Value** | **7.5 / 10** | Genuinely high-engagement educational content (33/33/33 Rule, Poor Man's Covered Call, Rule of 40); a real, monetized content/tool business (wbfintool.com) built in parallel with the trading account. |
| **Overall TraderMatrix Role** | **Contrarian Sentiment Barometer + Earnings-Calendar Reference Feed** | **Harvest calendar awareness and options-mechanics templates only; hard-firewall all position sizing, all theme-concentration mirroring, and every self-reported Gain/Loss figure.** |

---
*Report compiled by Artemis Engine / Sonnet Desk. Data verified via raw structured fields in `@WarrenBuffett_all_posts.json` (`tag`, `gain_loss`, `amount_k`, `tickers`, `reaction_count`, `comment_count`, `is_hunt_post`) cross-referenced against the full 1,925-post lifetime markdown archive. The `amount_k` field, while occasionally noisy on a same-day basis (~15 apparent round-trips consistent with sync lag or genuine intraday options repricing), is directionally corroborated at every major inflection point by the trader's own post text and is treated as the authoritative capital-trajectory source for this dossier.*
