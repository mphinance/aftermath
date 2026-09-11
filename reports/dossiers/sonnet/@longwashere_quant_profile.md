# Quant Forensic Autopsy: Trader @longwashere
**Target Profile**: `@longwashere` (`prf_7c539a287e524223b1713c2c78479330`)
**Platform**: AfterHour (#17 Most Active Followed Trader)
**Alias**: "Wallstreet Dragon" / "Dongwashere" / "Scamwashere" (self-applied, contextual)
**Dataset Analyzed**: 584 Lifetime Posts (2024-04-04 to 2026-09-09)
**Analyst**: Sam the Quant Ghost (`Momentum Phinance / Artemis Engine`)

---

## 1. Executive Profile & Portfolio Capital Trajectory

### 1.1 Trader Philosophy & Archetype

`@longwashere` is a self-described retired/laid-off software engineer (HBCU IT degree, per his own repost of a Grok query about himself) who reinvented himself as AfterHour's resident shock-jock entertainer-trader. His stated philosophy, in his own words:

> *"To be honest, I rather be funny on here than make any of yall money... I'm already rich... you're no one to me, and I don't owe you anything."* (2025-07-19)

He is explicitly **not** a technical trader — he says so directly and repeatedly:

> *"I don't do any research. I don't believe in technical analysis. My dd is literally just staring at the graph and manifesting it to life."* (2024-10-17)
>
> *"Pessimists sound smart. Optimists make money."* (2025-06-05)
>
> *"Hot take: pure technical traders will always come out behind in the end... [ranking] Technical trading < swing trading <= theta gang <= fundamental investing < value investing."* (2025-02-16)

His actual process is **catalyst-reactive macro/news trading** wrapped in absurdist comedy — a running gag where he claims his erections ("the indicator," "my rod," "flaccid days") predict SPY direction, used as a satirical stand-in for "I trade on vibes and headlines, not charts." Underneath the bit is a genuinely fast, headline-driven trader who front-runs Fed speakers, CPI prints, tariff announcements, earnings, and geopolitical flashpoints (Iran, SoCal wildfires, government shutdowns) with options.

He runs **two parallel trading identities simultaneously**:
1. A **concentrated, multi-year "long-term" conviction book** (China leveraged ETFs, then overwhelmingly Robinhood/HOOD stock) that he almost never actively manages or hedges — pure buy-and-forget bag-holding at extreme size.
2. A rotating cast of **publicly-linked "100k → 1m" challenge accounts** used as content generators — aggressive day/swing trading, margin, spreads, cash-secured puts, and 0-1 DTE index lottos, restarted from scratch whenever the prior one blows up or gets platform-restricted.

**Verdict on philosophy**: Entertainer-first, trader-second. Genuine catalyst-timing skill exists (see §2), but it is delivered through a persona explicitly engineered to maximize engagement, not signal fidelity — and he says as much himself.

### 1.2 Timeline & Posting Cadence

- **Operational Window**: April 4, 2024 → September 9, 2026 (888 calendar days / 126.9 weeks).
- **Total Posts**: 584.
- **Lifetime Mean Cadence**: **4.6 posts/week** — but this average badly understates a collapsed pattern. Cadence is a **volume-decay story**, not a steady drip.

```
Posts per Quarter (884-day window):
2024-Q2  ■■■■■■■■■■■■■■■■■■■■■■  44   (3.4/wk)   -- launch / birthday YOLO
2024-Q3  ■■■■■■■■■■              21   (1.6/wk)   -- summer lull
2024-Q4  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■  87   (6.7/wk)  -- election, NVDA, DJT
2025-Q1  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■  84   (6.5/wk)  -- tariff-war SPY puts era
2025-Q2  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■  126  (9.7/wk)  ***PEAK***
2025-Q3  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■  101  (7.8/wk)
2025-Q4  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■         73   (5.6/wk)
2026-Q1  ■■■■■■■■■■                                  22   (1.7/wk)  -- 100k acct post-mortem
2026-Q2  ■■■■■■■■■■                                  21   (1.6/wk)
2026-Q3  ■■                                            5   (0.4/wk)  *** near-dormant ***
```

- **Peak Velocity**: June 2025, 55 posts (~13/week) — the height of the Webull "100k → 1m" challenge-account content machine.
- **Collapse**: By 2026-Q3 (Jul–Sep), cadence is **0.38 posts/week** — a **96% decline from peak**. August 2026 and September 2026 each produced exactly **one** post.
- **Reading**: This is not noise. It tracks his own account history almost exactly — heavy posting while a linked challenge account is alive and printing content (2024's 100k→7m run, 2025's Webull run), then a hard drop-off whenever an account is killed by a day-trade restriction, blown up, or simply abandoned without a closing post. The 2026 near-silence coincides with the undisclosed fate of the "Super Car Fund" (see 1.3) and a pivot of his energy to Twitter/X and a crypto-perps platform ("Legend").

### 1.3 Verified Capital Trajectory & Forensic Drawdown Analysis

**Data-quality caveat**: the raw JSON's `amount_k` field is not a clean linked-portfolio time series for this trader — it fluctuates by 10-50x between adjacent posts (e.g., $20.4M then $171k the next entry) because it is picking up whichever dollar-shaped figure appears in a post's title/body rather than a consistent account-sync value, and `@longwashere` runs **three or more accounts simultaneously** (a "long-term" personal book, sequential public challenge accounts, and a personal trust). A naive average of this field is meaningless. The trajectory below is instead reconstructed from his own explicit, dated numeric claims, cross-checked against the qualitative narrative.

**Track A — Public "Challenge" Accounts (linked, screenshot/Kinfo-verified, the auditable track record):**

```
Challenge Acct #1 (Robinhood, started May 2024, $100k seed)
  $100k --> $164k (wk2) --> $184k (wk3) --> $1.6M (Nov 2024) --> $7M (closed Mar 10 2025, peaked $11M)
  Result: +6,900% to +10,900% peak. Closed VOLUNTARILY (to pay taxes) after a Robinhood
  day-trade-call restriction started costing him fills. SINGLE BEST VERIFIED RESULT IN THE DATASET.

Challenge Acct #2 (Webull, started ~Mar 22 2025, ~$180k seed)
  $180k --> $517k (Jul 17 2025) --> $540k (Jul 30 2025) --> [migrated back to RH, Aug 2025 restriction]
  --> peaked ~$490k in the account's own later self-audit --> $400k --> $170k (Dec 2025)
  --> CLOSED as a stated "failure," Feb 11 2026, at ~$50k.
  Self-reported full curve (his words, 2026-02-11):
     "180k -> 300k -> 220k -> 490k -> 300k -> 180k -> 50k"
  Result: peak +172% (~$490k), final -72% vs. seed / -90% peak-to-trough. FIRST ADMITTED
  PUBLIC-ACCOUNT BLOWUP.
  Note: two days later (2026-02-13) he re-summarizes this same account as "150k -> 45k in 8 months" —
  a different start and end figure than his own post 48 hours prior. His "verified" numbers do not
  reconcile with each other; treat all of his self-reported figures as directional, not exact.

Challenge Acct #3 "Super Car Fund" (Robinhood, started Feb 13 2026, $140k seed)
  $140k --> ~$210k (+50%, reported May 22 2026) --> [NO FURTHER PUBLIC UPDATE through Sep 9 2026]
  Result: UNKNOWN / UNDISCLOSED. Given his own admission that he stopped disclosing losses in
  2025 ("Never showing my losses on here again... just assume I have them," 2025-06-23) and that
  his posting cadence craters right before/during account failures, the silence itself should be
  read as a soft negative signal, not a neutral one.

1k "Hyper-Aggressive" Perps Account (Legend/Hyperliquid, started Jun 16 2026, 20x leverage)
  No further update posted. Explicitly framed as "keeping it small... hyper degenerate."
```

**Track B — "Long-Term" Personal Book (self-reported only, NEVER linked/screenshotted, unauditable):**

This is the most important finding in the entire report. Buried inside otherwise throwaway posts, `@longwashere` discloses a personal long-term book of a scale that dwarfs every public challenge account by 1-2 orders of magnitude:

- Cost-basis YINN (China 3x bull ETF) position, ~54,000+ shares @ $18.20 basis (~$980k cost) — partial close for "**2m gains**" (Oct 2024), additional 5M position re-added Mar 2025.
- Nov 22, 2025: *"My robn bags **6m -> 60m -> 35m**. I will never financially recover from this."* (ROBN = Robinhood stock, held in a personal trust, 580,000 shares disclosed separately.)
- Dec 2, 2025: *"My long port went from **10m > 80m > 40m** this year."*
- Nov 20, 2025: *"Down another **40m+** in my long term holding from ath."*
- Feb 19, 2026: walks it back somewhat — *"I'm still up 100% on them. My cost basis is ~10... got a 1.5m dividend recently. Only lost the unrealized gains."*

**Quant ruling on Track B**: these numbers describe a real, extreme single-name concentration bet (Robinhood common stock) that rode a genuine multi-year bull thesis from single-digit millions to a claimed ~$80M peak, then gave back roughly half into a ~$40M mark. There is **no AfterHour position card, no brokerage screenshot, and no third-party corroboration for any figure in Track B** — it is presented purely as text. TraderMatrix must **never treat Track B numbers as verified equity** for scoring purposes; they are included here only because they are the dominant driver of his real financial outcome and his behavioral risk profile (see §3).

**Consolidated Picture**: one clean, fully-verified 2024 triumph (+6,900%+ on disclosed seed capital); one clean, fully-admitted 2025-2026 public failure (-72 to -90%); and a much larger, completely unverifiable "whale" book that appears to have suffered a real ~50% drawdown on paper from a concentrated bet in the same window the public accounts were also struggling. The pattern across **both** the verified and unverified tracks is identical: **extreme concentration, no active hedging of the core position, and large round-trip drawdowns following large run-ups.**

---

## 2. Ticker Universe & Catalysts

### 2.1 Core Asset Universe

Only 65 of 584 posts (11%) carry a structured ticker tag in the archive metadata — the true universe, reconstructed by reading the full text corpus, is far broader. Consolidated by tier:

| Tier | Tickers | Role |
| :--- | :--- | :--- |
| **Tier 1 — Career Conviction (multi-year, largest $ at risk)** | **$HOOD** (Robinhood) | By far the single most-repeated name in the archive (15 tagged mentions, dozens more in prose). Calls, puts, spreads, shares, covered calls, day-trades, and the entire undisclosed Track-B mega-position. Thesis has run continuously since 2024 ("100b market cap was my price target this year. It's already here"), correctly called SPY 500 inclusion (Sep 2026) roughly a year ahead ("had a good hunch about hood joining the sp500... my penis was right," Jun 2025). |
| **Tier 2 — Macro/Thematic Longs** | **$YINN** (China 3x bull), **$RIVN**, **$MSTR** | Multi-month conviction holds tied to a macro thesis (China stimulus/recovery called correctly in Apr 2024, ~5-6 months ahead of the move), rather than technical entries. |
| **Tier 3 — Earnings/Event Swing Names** | **$TSM, $NVDA, $NVDL, $DELL, $SMCI, $AMZN, $META, $GOOGL, $AEO, $INTC, $INTU, $LDI, $Z(illow), $OSCR** | Bread-and-butter short-hold swing trades timed to earnings, Fed events, or specific news catalysts (Blackwell overheating rumor → DELL/SMCI pair trade for $600k, Nov 2024; NVDA "Cosmos" earnings event contract for 28%, Aug 2025). |
| **Tier 4 — Meme / Low-Float "Cum Biscuit" Plays** | **$CLBR, $NEGG, $RXRX, $GME, $DOGE, $PEW** | Explicitly framed by him as jokes/pumps, not conviction ("I love me a game of cum biscuit"). Self-aware pump-and-dump participation, often admittedly triggered by a follower tag or a literal typo ("fell down the stairs and bought $300k of $CLBR"). |
| **Tier 5 — Macro Hedges / Index / Geopolitical** | **$SPY / SPX (0-1 DTE)**, **$SQQQ, $USO, Gold, $EIX/$PCG** (SoCal wildfire pair trade) | Fast, catalyst-timed directional bets around Fed speakers, CPI, tariff headlines, and geopolitical flashpoints (Iran strikes, SoCal fires). This bucket contains his single largest verified win. |

### 2.2 What Actually Drives His Entries

Reading the corpus in order, entries cluster into five repeatable triggers, in descending order of real signal value:

1. **Macro/Political Headline Reaction (highest documented edge)** — Fed speakers, CPI prints, tariff announcements, government shutdown mechanics. His Jan–Feb 2025 tariff-war SPY put thesis is the best-documented trade in the archive: called it in writing on Jan 25 2025 ("Bearish on America... for the next month or so"), sized into $900k+ of SPY puts on Jan 31, and updated the same post as gains compounded to **$1M → $1.5M → $3.5M** by Feb 3, 2025, explicitly timestamped and screenshotted at each stage specifically to pre-empt "posted-after-the-fact" accusations.
2. **Earnings-Adjacent Options Flow** — buys/sells around known earnings dates (HOOD, TSM, AMZN, META), frequently same-day or next-day exits.
3. **Geopolitical Tail Events** — SoCal wildfires → short the local utility (EIX, -then -flip long PCG on an oversold-bounce thesis that cost him $90k), Iran strikes → USO calls then puts on the same thesis reversed weeks later.
4. **Platform/Community Momentum** — follower tags, bets, and dares are a real, disclosed source of entries ("@jaythefknsavage called me a pussy so I threw a milly into doge"; "@squeezekid complimented me, so I bought 300k in calls for rxrx"). This is a genuine behavioral tell: his size is sometimes driven by social provocation, not thesis.
5. **The "Erection Indicator" (zero signal value, pure content)** — a running joke since March 2025 where his libido allegedly predicts SPY direction. Explicitly labeled non-serious by him but posted with enough frequency (10+ instances) that a careless observer could mistake it for an actual signal feed.

---

## 3. Risk Management & PnL Reality

### 3.1 Does He Take Profits or Hold Bags? Both — Bimodally, by Account.

- **Public/challenge accounts**: genuinely active. Frequent same-day/next-day exits, "closed for X gains" posts, systematic use of covered calls for yield, cash-secured puts, and debit/put spreads to define risk. He states a real rule: *"I've never oversold, but I know when to book 20% early on large port positions"* (paraphrased across multiple posts) — and then documents breaking it himself repeatedly:
  > *"Called it right on Sunday... broke my rule of selling for profit early 20% at Monday close when playing with a large port position. It was bad on bad on bad."* (2025-05-21)
- **Long-term/Track-B book**: pure, unhedged bag-holding at extreme concentration. No covered calls, no protective puts, no trimming disclosed anywhere in the corpus for the core ROBN/HOOD stake, despite it swinging by tens of millions of dollars. His own words on the philosophy: *"Only diversify when there are multiple opportunities, not as a precaution... if you diversify because you're scared of losing money, you're a cuck."* (2025-02-18) This is the direct cause of the ~50% Track-B drawdown in late 2025.

### 3.2 Losing-Position Management

- **Admitted pattern**: cut some losses fast (PCG, -$90k, cut same week after doubling down once), hold others indefinitely hoping for recovery ("Small nvidia loss porn... Holding till green," Dec 2025).
- **Selective disclosure is explicit and confirmed by the data.** He stated the policy outright:
  > *"Never showing my losses on here again btw. Just assume I have them... Yeah I lost 20k on that trade… but I made 700k on the 4 trades before that."* (2025-06-23)
  The tag metadata confirms the resulting bias precisely: **87 posts self-tagged `Gain` vs. 15 tagged `Loss`** — a **5.8:1 disclosed win ratio** that the trader himself admits is not representative of his true hit rate. Any ingestion engine treating his `Gain`/`Loss` tag distribution as a real win rate will be badly miscalibrated.
- **The one full-cycle exception**: the 2025 Webull challenge account is the single instance where he disclosed a complete failure, start to finish, including a formal post-mortem ("2025 100k account was a failure. Will be writing a post mortem about it soon," 2026-02-11). This is valuable precisely because it is rare — it is the only place in the dataset where his real, unfiltered win/loss ratio over a full account lifecycle is visible, and it was a net loser.

### 3.3 Documented Wins vs. Blow-Ups

| Category | Amount | Date | Notes |
| :--- | :--- | :--- | :--- |
| **Biggest verified win** | SPY/SPX 1-DTE puts, $1M → $3.5M | Jan 31–Feb 3, 2025 | Tariff-war macro thesis, screenshotted at each stage. |
| **Biggest verified account result** | $100k → $7M (peak $11M) | May 2024–Mar 2025 | Challenge Acct #1, closed voluntarily. |
| Dell/SMCI Blackwell pair trade | +$600k | Nov 18, 2024 | Correctly read a supply-chain rumor before it was priced in. |
| NVDA calls (pre-Dow-inclusion) | +$800k–$950k combined | Nov 2024 | Two separate NVDA call tranches. |
| **Biggest admitted blow-up (verified account)** | $490k peak → $50k | 2025 (full year) | Challenge Acct #2; -90% peak-to-trough, formally closed as a failure. |
| **Biggest claimed drawdown (unverified)** | ~$80M peak → ~$40M | 2025 (full year) | Track-B "long port," self-reported only, no linkage. |
| Meta birthday YOLO | -$1,000,000 | Apr 25, 2024 | Explicitly self-labeled "blind/hardly any dd coin flip." |
| Roaring Kitty GME re-entry | -$40,000 | May 2024 | Explicitly stated he doesn't normally trade meme stocks. |
| PCG oversold-bounce thesis | -$90,000 | Jan 24, 2025 | Thesis was directionally reasonable, timing was wrong twice. |
| Intel short-thesis reversal | -$20,000 net (-$10k after offsetting gains) | Apr 30, 2026 | One of the only 2026 posts with a disclosed loss at all. |

---

## 4. Behavioral & Sentiment Signals

### 4.1 Why Is He Posting?

The engagement data answers this cleanly. Ranking his top 10 posts by reaction count, **eight of the ten are non-trading, human-interest narrative posts** — not trade calls, not gain screenshots:

| Reactions | Comments | Date | Post |
| :--- | :--- | :--- | :--- |
| 526 | 126 | 2025-02-21 | "I woke up to this LinkedIn message" (paying-it-forward karma story) |
| 478 | 243 | 2025-01-31 | "1 milly in profit screen shot on spy FD puts" *(the one trade-content outlier)* |
| 400 | 157 | 2025-05-16 | "I teared up today" (follower gift-giving story) |
| 391 | 257 | 2025-03-22 | "Yall wanna see how to trade 100kish to a million?" |
| 386 | 97 | 2024-12-21 | "I paid it forward today" (Venmo/Zelle to an old acquaintance) |
| 378 | 153 | 2025-05-25 | "Before the AfterHour fame..." (personal origin story) |
| 371 | 162 | 2025-02-03 | "Spy puts update: up 3.5 million in profit" *(trade content)* |
| 311 | 97 | 2025-08-22 | "I adopted a homeless man" (personal story) |
| 303 | 254 | 2025-07-19 | "I rather be funny than make you money" (persona manifesto) |
| 245 | 142 | 2025-08-27 | "Best tip on how to use this app" (community meta-commentary) |

**Total lifetime engagement**: 40,620 reactions / 27,398 comments across 584 posts (mean 69.6 reactions, 46.9 comments per post). The clear takeaway: **his audience rewards narrative and persona, not trade calls.** He is optimizing for exactly that — his own words confirm it is a deliberate strategy, not an accident.

### 4.2 Recurring Linguistic Patterns

- **The dragon mythos**: 🐉/🐲 emoji and "Wallstreet Dragon" branding used as a consistent visual signature across nearly every post since day one.
- **"Erection/flaccid indicator"**: recurring pseudo-technical bit (Mar 2025 onward) where sexual innuendo stands in for "vibes-based" macro calls. Zero informational content, extremely high frequency.
- **"Cum biscuit"**: his slang for a low-float short-squeeze/pump play. Signals he is fully aware these are speculative pumps, not investments.
- **"Soup kitchen" / "put the fries in the bag"**: self-deprecating shorthand for a losing position or for mocking followers he considers unsophisticated.
- **Self-aware persona toggling**: "longwashere" (winning) vs. "Dongwashere" (celebratory) vs. "scamwashere" (mocking himself after a platform-verification bug briefly cast doubt on his linked-account legitimacy, Jul 2025).
- **Community feuds as content**: recurring beefs and bits with named AfterHour peers (@x52x, @wtf, @flawssy, @squeezekid, @zenn_ — the last accused outright of faking trades with a linked paper account).

### 4.3 Reaction to Volatility / Red Days

- On red days he leans into **gallows humor and persona ("FLACCID," "soup kitchen," "generational bags secured")** rather than substantive risk commentary.
- He is explicitly and repeatedly **contrarian-bullish at local fear peaks**: *"We are in the ath zone. In the next 6 months 20% of yall will blow up your port"* (2025-07-24, buy-the-dip framing); *"Global market sell off for a poor or a stale reason? Best time to leverage in right now"* (2026-06-22).
- He also self-identifies euphoria as a top signal, unprompted: *"Bought 2oz gold @ 3370... Top signal"* (2025-08-20) — a rare moment of genuine, quotable self-awareness that is directly usable as a contrarian marker (see §5).

---

## 5. Quantitative Verdict for TraderMatrix

```
+-----------------------------------------------------------------------------------+
|                           TRADERMATRIX CLASSIFICATION                             |
|                                                                                     |
|   PRIMARY TAG:      MACRO_CATALYST_SWING_TRADER                                   |
|   SECONDARY TAG:     CONCENTRATED_BAGHOLDER (single-name, unhedged, multi-year)   |
|   TERTIARY TAG:      RETAIL_SENTIMENT_ENTERTAINER / CONTRARIAN_FADE_SOURCE        |
|   ALPHA STATUS:      Bimodal — real catalyst-timing edge, near-zero exit          |
|                       discipline, severe self-report bias                         |
|   RECOMMENDED FIT:   Macro-Catalyst Alert Feed + Contrarian Euphoria Sensor       |
+-----------------------------------------------------------------------------------+
```

### 5.1 Algorithmic Alpha Score & Expectancy

**Algorithmic Alpha Score: 41 / 100**

Justification: one genuinely exceptional, fully-verified account result (+6,900%, Acct #1) is offset by a fully-admitted account failure in the very next public cycle (-90% peak-to-trough, Acct #2), an unverifiable but plausible ~50% giveback on his largest disclosed position (Track B), an explicitly admitted 5.8:1 self-reported win-bias that overstates his true hit rate, and a 96%-from-peak collapse in posting cadence that coincides with an undisclosed account outcome. The catalyst-timing skill embedded in specific trade classes (macro/tariff SPY plays, earnings-adjacent options, supply-chain rumor plays) is real and separable from the noise — hence a moderate rather than low score — but the account-level track record, taken whole and including the parts he tried to stop showing, nets out closer to breakeven-with-high-variance than to "consistently profitable."

**Expectancy (qualitative)**: Positive but fat-tailed and negatively skewed at the account level once losing cycles are included — large, catalyst-driven wins punctuated by rare, severe, slow-bleed drawdowns from unhedged concentration. Per-trade expectancy on the isolated "catalyst options" subclass (Fed/CPI/tariff/earnings 0-5 DTE trades) is materially better than his account-level expectancy, because that subclass is where his documented, timestamped hit rate is genuinely strong (SPY tariff puts, DELL/SMCI, NVDA pre-Dow, EIX wildfire short). The gap between subclass expectancy and account expectancy **is** the risk-management failure documented in §3.

### 5.2 Signal Flow Ingestion Matrix

```
                    ┌───────────────────────────────────────────────────┐
                    │           @longwashere Raw Signal Stream           │
                    └───────────────────────┬───────────────────────────┘
                                            │
      ┌──────────────────────┬──────────────┼──────────────┬───────────────────────┐
      ▼                      ▼               ▼              ▼                       ▼
┌───────────────┐  ┌──────────────────┐ ┌───────────────┐ ┌───────────────┐ ┌────────────────┐
│ 1. MACRO/     │  │ 2. HOOD LONG-    │ │ 3. EARNINGS/  │ │ 4. MEME/LOW-  │ │ 5. EUPHORIA /  │
│ CATALYST      │  │ TERM CONVICTION  │ │ EVENT SWINGS  │ │ FLOAT PUMPS   │ │ "INDICATOR"    │
│ (Fed/CPI/     │  │ (multi-year      │ │ (TSM, NVDA,   │ │ (CLBR, NEGG,  │ │ NOISE (dick/   │
│ tariff/geo)   │  │ thesis)          │ │ AMZN, META)   │ │ RXRX, GME)    │ │ boner posts)   │
├───────────────┤  ├──────────────────┤ ├───────────────┤ ├───────────────┤ ├────────────────┤
│ Action:       │  │ Action: TRACK    │ │ Action:       │ │ Action:       │ │ Action:        │
│ ALERT TRIGGER │  │ THEME, CAP SIZE  │ │ MIRROR SETUP, │ │ BLACKLIST /   │ │ DISCARD — but  │
│ (event-driven,│  │ (never full      │ │ SHORT HOLD    │ │ IGNORE        │ │ USE AS A       │
│ not directional)│ position-size    │ │ WINDOW ONLY   │ │ ENTIRELY      │ │ CONTRARIAN     │
│ Weight: +0.75 │  │ mirror)          │ │ Weight: +0.55 │ │ Weight: 0.00  │ │ EUPHORIA FLAG  │
│ (Tactical)    │  │ Weight: +0.30    │ │ (Tactical)    │ │               │ │ Weight: -0.50  │
└───────────────┘  └──────────────────┘ └───────────────┘ └───────────────┘ └────────────────┘
```

### 5.3 Execution Directives for the Artemis Engine

#### A. Ingestion Directives — Genuine Edge to Harvest
1. **Macro/Catalyst Timing Feed**: Treat any `@longwashere` post reacting to a Fed speaker, CPI/jobs print, tariff headline, government-shutdown development, or acute geopolitical event (Iran, wildfires) as an **alert-priority trigger**, not a copy-trade instruction. His genuine skill is *speed of reaction and correct qualitative direction*, not position construction.
2. **Supply-Chain / Rumor-Arbitrage Pattern**: His DELL/SMCI Blackwell-overheating trade is a template worth encoding generically — "hardware/supply-chain rumor → pair trade the two named counterparties" — regardless of his own execution quality.
3. **HOOD as a Long-Running Theme Ticker**: His multi-year HOOD conviction (SP500 inclusion called ~1 year early, growth thesis since 2024) is a legitimate thematic signal worth tracking as a sentiment weight — capped hard (see Blacklist C below) given his own concentration failure on the same name.
4. **Options-Mechanics Templates**: His stated (if inconsistently applied) covered-call and cash-secured-put mechanics against core share positions are sound, generic yield techniques worth ingesting as templates independent of his own track record.

#### B. Contrarian Fade Directives — When to Fade Him / The Retail Herd
1. **Euphoria Cluster Fade**: When a string of `Gain`-tagged posts (3+ in a short window) is followed by a self-aware "top signal" joke, an all-caps victory-lap post, or a "we can't go tits up" framing, treat it as a **local-top alert** — trim, don't add.
2. **Silence-as-Signal**: A sharp, unexplained drop in his posting cadence following a period of high-frequency account updates (as seen Aug 2025→2026) should be read as a probable **undisclosed drawdown in progress** on whichever public account was last active, given his own admitted policy of hiding losses.
3. **Numeric Reconciliation Check**: Any of his self-reported account totals should be treated as **directional only**. He has restated the same account's start/end figures inconsistently within a 48-hour window (see §1.3, Acct #2). Never backfill a precise position size from his prose.

#### C. Mandatory Risk Blacklists & Firewalls
1. **BLACKLIST — Low-float/meme "cum biscuit" plays** (CLBR, NEGG, RXRX-style pumps, meme coins): explicitly admitted by him to be jokes/pumps, not conviction. Zero ingestion.
2. **BLACKLIST — 0-1 DTE lottos and gambling gimmicks** ("Nightingale," "martingale," "inDICKator" series): self-labeled *"not a signal, just pure degeneracy... do not follow."* Take him at his word.
3. **FIREWALL — Single-Name Concentration**: Never mirror position *size* on his conviction names (HOOD, ROBN, YINN). His own >98%-of-net-worth concentration events are the direct cause of both his verified (-90%) and claimed (-50%) drawdowns.
4. **FIREWALL — Unverified Track-B Claims**: Any account-value figure attached to his "long-term"/personal-trust book must be excluded from quantitative scoring. It is narrative color, not data.
5. **FIREWALL — Platform-Restriction Chaos**: Repeated day-trade-call restrictions across three brokerages (Robinhood, Webull, back to Robinhood) indicate trading volume/leverage inconsistent with disclosed account size. Do not scale position sizing upward in proportion to his claimed AUM.

#### D. Exit Rules & Alpha Rectification
1. **Enforce the Rule He States But Breaks**: He explicitly names a 20%-at-first-target profit-taking rule for large positions and documents breaking it as his direct cause of loss ("broke my rule of selling for profit early... it was bad on bad on bad," 2025-05-21). TraderMatrix should **hard-code this exact rule** on any harvested setup sourced from him: scale out a fixed 20-50% at first profit target, no discretion.
2. **Time-Box All Harvested Trades**: His genuine edge is in short-duration, catalyst-driven trades (same-day to ~1 week holds). Any signal sourced from his macro/earnings reactions should carry a hard time-stop consistent with his own turnover — do not extend into LEAPS-style long-dated exposure the way he does with his core bags.
3. **Mandatory Hedge Overlay on Any Ingested Conviction Theme**: If HOOD or another of his long-running theme tickers is ingested as a sentiment weight, require a standing covered-call or protective-put overlay at the portfolio level — the one risk control he inconsistently uses himself and that would have meaningfully reduced both of his documented drawdowns.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Event |
| :--- | :--- |
| 2024-04-04 | First AfterHour post ("250k on tsm"). Pre-existing large linked portfolio already visible. |
| 2024-04-14 | China-recovery thesis published ("Play China 🇨🇳... park my money into a triple bull China etf") — ~6 months ahead of the move. |
| 2024-04-25 | Meta-birthday YOLO: -$1,000,000, self-labeled a blind coin flip. |
| 2024-05-01 | Publicly launches Challenge Account #1 on Robinhood, $100k seed. |
| 2024-05-14 | Roaring Kitty/GME re-entry, -$40k, explicitly off-thesis. |
| 2024-10-02 | China thesis vindication post: YINN closed for **+$2M** (18-month-old original call). |
| 2024-11-06 | Trump election win reaction; NVDA calls +$400k the same week. |
| 2024-11-08 | NVDA calls, second tranche, **+$800k**. |
| 2024-11-13 | Challenge Acct #1 crosses **$1.6M**, ranks top-7 on Kinfo leaderboards. |
| 2024-11-18 | DELL/SMCI Blackwell-overheating pair trade, **+$600k**. |
| 2025-01-13 | SoCal-wildfire short (EIX puts), +150-200%. |
| 2025-01-24 | PCG oversold-bounce long, cut for **-$90k**. |
| 2025-01-25 | "Bearish on America" — the opening call of the tariff-war SPY-put thesis. |
| 2025-01-31 | $900k+ SPY 1-DTE puts entered on Canada/Mexico tariff bet; first $1M profit screenshot. |
| 2025-02-03 | SPY puts thesis updated: **+$3.5M**, position closed. Best fully-verified single trade in the archive. |
| 2025-03-10 | Challenge Acct #1 formally closed: **$100k → $7M (peaked $11M)**, 10 months. |
| 2025-03-22 | Challenge Acct #2 (Webull) launched, ~$180k seed. |
| 2025-06-23 | Explicit policy change: stops disclosing losses publicly going forward. |
| 2025-07-17 | Challenge Acct #2 hits **$517k**. |
| 2025-08-08 | Trade-restricted on Webull; migrates account back to Robinhood. |
| 2025-09 | SPY500-inclusion call on HOOD ("had a good hunch... my penis was right," originally posted Jun 2025) confirmed correct. |
| 2025-11-20/22 | Track-B long-term book disclosed: ROBN bags **"6m → 60m → 35m"**; long port **"down another 40m+ from ath."** |
| 2025-12-02 | Track-B full-year figure disclosed: **"10m > 80m > 40m this year."** Challenge Acct #2 reported at $400k→$170k. |
| 2026-02-11 | Challenge Acct #2 formally closed as a **failure**: "180k -> 300k -> 220k -> 490k -> 300k -> 180k -> 50k." |
| 2026-02-13 | Challenge Acct #3 "Super Car Fund" launched, $140k seed (contradicts prior post's $180k start figure for Acct #2). |
| 2026-02-19 | Track-B walkback: ROBN cost basis ~$10, "still up 100%... only lost the unrealized gains," plus a disclosed $1.5M dividend. |
| 2026-04-30 | Rare 2026 loss disclosure: Intel short, net -$20k. |
| 2026-05-22 | Super Car Fund reported up 50% for the month — **last disclosed performance figure for any public account** in the dataset. |
| 2026-06-16 | Pivots to a 20x-leverage crypto perps account ("Legend/Hyperliquid"), $1k seed, explicitly "hyper degenerate." |
| 2026-07 – 2026-09 | Posting volume collapses to 1 post/month; no further account performance disclosed. |

---

## 7. Summary Scorecard

| Metric | Score / Rating | Quantitative Commentary |
| :--- | :--- | :--- |
| **Macro/Catalyst Timing** | **8.0 / 10** | Genuinely fast and directionally correct on Fed/CPI/tariff/geopolitical reactions; the SPY tariff-put run (+$3.5M, fully verified) is elite-tier execution. |
| **Conviction/Theme Discovery** | **7.0 / 10** | China-recovery (2024) and HOOD (2024-2026, incl. SP500 call ~1yr early) theses were both directionally right, multiple months to a year ahead of consensus. |
| **Risk Management** | **2.0 / 10** | States real rules, breaks them constantly; zero hedging on his largest disclosed position; caused both his verified (-90%) and claimed (-50%) drawdowns via unhedged concentration. |
| **Disclosure Integrity** | **2.5 / 10** | Explicitly admits to suppressing losses; self-reported figures for the same account contradict each other within 48 hours; largest claimed numbers (Track B) are entirely unverifiable. |
| **Emotional Discipline** | **3.5 / 10** | High-conviction persona masks genuine oversleeping/fat-finger/FOMO errors he documents himself; euphoria and despair are both performed for engagement, complicating any read of true sentiment. |
| **Community/Content Value** | **8.5 / 10** | Top-decile engagement driven almost entirely by narrative/persona content rather than trade calls; useful as a sentiment/attention barometer for the AfterHour retail cohort. |
| **Overall TraderMatrix Role** | **Tactical Macro-Alert Source + Contrarian Euphoria Sensor** | **Harvest catalyst-timing and theme discovery; hard-firewall position sizing, concentration mirroring, and all self-reported account totals.** |

---
*Report compiled autonomously by Sam the Quant Ghost (`Momentum Phinance / Artemis Engine`). Data verified via raw post/telemetry fields in `@longwashere_all_posts.json` (`tag`, `gain_loss`, `amount_k`, `tickers`, `reaction_count`, `comment_count`) cross-referenced against the full 584-post lifetime markdown archive. The `amount_k` field was found to be an unreliable proxy for linked-account equity for this trader (see §1.3) and was excluded from the capital-trajectory reconstruction in favor of his own dated, quoted claims.*
