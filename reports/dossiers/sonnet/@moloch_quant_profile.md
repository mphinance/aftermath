# Quant Forensic Dossier: @moloch

**Subject:** AfterHour trader `@moloch` (Profile ID `prf_3393b1a6f40040e98eb4268039c6d6cd`)
**Rank:** #40 most-active followed trader — by lifetime post *count*, not activity
**Sample size:** 10 lifetime posts, 2024-12-14 → 2026-08-26 (620 days)
**Sources:** `@moloch_lifetime.md` (formatted archive), `@moloch_all_posts.json` (raw), cross-verified against live OHLCV history for `$ABAT` and `$DGXX`
**Analyst:** Artemis Forensic Desk · 2026-09-10

> **Headline finding:** @moloch is not a signal *feed* — he is a signal *fossil*. Ten posts across 20 months is not a trading log, it is a highlight reel. Every disclosed win is real and independently verifiable against market data; every loss, exit, stop-out, and drawdown is completely absent. That asymmetry — not his ticker picks — is the primary thing Artemis needs to model.

---

## 1. Executive Profile

### Philosophy
@moloch presents as a **technically literate retail quant hobbyist** who trades a mix of (a) diversified thematic/political "hunch" baskets, (b) opportunistic single-name rotations off breaking news, and (c) home-built systematic tools (Pine Script indicators, an Alpaca paper-trading bot, a self-hosted "stock vibe app," a Kalshi prediction-market API integration). He is explicit that his baskets are *not* high-conviction ("This goes slightly against picking one stock and going in with full conviction, but it's entertaining") and treats most individual names as low-stakes experiments rather than theses he'll defend.

His most technically serious post (two-part, Jan 2026) describes backtesting an **LPPLS ("Log-Periodic Power Law Singularity") bubble/crash oscillator** in Pine Script — an actual academic econophysics model (Sornette et al.) used to time speculative bubble tops/bottoms — and concludes it's tradeable only as a **quarterly, leveraged, direction-agnostic options bet around volatility "earthquakes,"** not as a compounding long-term strategy. This is a materially more sophisticated framework than the median AfterHour poster uses, but it is presented as a work-in-progress, not a live, sized strategy.

### Post Cadence
| Metric | Value |
|---|---|
| Total posts | 10 |
| Active date range | 2024-12-14 → 2026-08-26 (620 days / 88.6 weeks) |
| **Average cadence** | **0.11 posts/week** (≈ 1 post every 62 days) |
| Median gap between posts | 64 days |
| Longest silence | 217 days (2026-01-21 → 2026-08-26) |
| Shortest burst | 3 posts in 48 hours (2026-01-19 → 2026-01-21) |
| Days silent as of report date (2026-09-10) | 15 (current status: dormant) |

The cadence is **bimodal**: long dormancy (64–217 days) punctuated by tight bursts when he's excited about a new tool or a fresh call (the LPPLS/DGXX cluster). This is the posting pattern of someone documenting side-project enthusiasm, not running a disciplined trading journal.

### Verified Capital Trajectory (platform-tracked `amount_k`)
| Date | Post | Tracked Portfolio Value | Δ from prior snapshot |
|---|---|---|---|
| 2024-12-14 | "Year Long Port Breakdown" | $10,000 (stated, not yet platform-tracked) | — |
| 2025-06-04 | "June checkin" | **$15,410** | +54.1% over ~5.5 months |
| 2025-09-18 | "$ABAT" `[Gain]` | **$68,848** | +346.8% over ~3.5 months |
| 2026-01-19/20/21 | "Good read" / "LPPLS" | **$161,888** | +135.2% over ~4 months |
| 2026-01-21 | "$DGXX" `[Chart]` | *null* (not tagged to the tracked port) | — |
| 2026-08-26 | "Kalshi API sharding update" | $0.0 (untagged, non-equity post) | *tracking goes dark* |

**Cumulative claimed return: $10,000 → $161,888 (+1,519%) in 13 months**, per the platform's own snapshots.

**Forensic caveats (critical):**
1. **Zero drawdown ever recorded.** Four consecutive tracked snapshots, all monotonically higher, while trading small/microcap high-beta names. That is not what a real unmanaged high-beta book looks like over 13 months — it is what a *survivorship-biased disclosure pattern* looks like (he only posts a portfolio update when it's up).
2. **Deposits are not distinguished from returns.** He states in the June 2025 post: *"I've left the original port but added and changed things"* — "added" is never clarified as added capital vs. added positions. The $10k → $161.9k series should **not** be treated as a clean, deposit-adjusted return stream.
3. **The trail goes cold at the peak.** The last dollar figure recorded is $161,888 in January 2026. There is no subsequent portfolio update — positive or negative — in the following 7+ months, even though (per independent price data below) his flagship holding gave back the majority of its gains in that window.

---

## 2. Ticker Universe & Catalysts

| Ticker | Post(s) | Instrument | Catalyst Type |
|---|---|---|---|
| $RIVN, $QTUM, $VRT, $RXRX, $BKSY | #1 | Equity | Averaging-down / vague bullish reading / "chance play" |
| $UPS | #1 | Equity | **Political** — DOGE (Musk/Ramaswamy) gutting USPS creating a private-carrier vacuum |
| $ONDS, $DPRO | #1, #3 | Equity | **Political/regulatory** — anticipated Trump-era drone deregulation |
| $RDDT | #1 | Equity | **Structural/AI theme** — Reddit as licensed AI-training data supply |
| $HOOD | #1, #3 | Equity | **Political/sentiment** — "retail is so back" under incoming administration |
| $AS (Amer Sports) | #2, #3 | Equity | **Seasonal/consumer** — spring/summer sporting-goods demand cycle |
| $UNH | #5 | Equity (faded, not bought) | **Earnings/news** — Q4 miss cited via Seeking Alpha link |
| $ABAT | #5, #6 | Equity | **Rotation off bad news** — sold the UNH idea, bought ABAT instead, day of |
| $DGXX | #9 | Equity | **Proprietary technical timing** — "Timed at $2.91," own indicator-driven |
| (unnamed) | #7, #8 | N/A — strategy/tooling | **Quant/systematic** — LPPLS bubble oscillator research |
| (Kalshi — crypto contracts) | #10 | **Prediction market**, not equity | **Infrastructure** — exchange API migration notice |

**Options vs. equities:** Every *actual* named position in the archive is a cash equity. Options appear exactly once, and only as a hypothetical framework ("leveraged... calls / puts") attached to the still-experimental LPPLS strategy — there is no disclosed options trade anywhere in his history.

**What drives entries — ranked by frequency:**
1. **Macro/political narrative** (4 of 10 posts reference an administration policy or regulatory shift as the thesis — USPS/DOGE, drone deregulation, "retail is so back")
2. **News-driven rotation** (ABAT/UNH — fading one name's bad print into an unrelated small-cap the same session)
3. **Seasonal/consumer-calendar logic** (Amer Sports — sporting-goods seasonality)
4. **Proprietary technical/quant signals** (LPPLS oscillator, DGXX "timed" level)
5. **Platform/thematic content generation** ("I mean I'm on this app aren't I" for $RXRX — a joke-tier thesis)

He is a **macro-narrative-and-news-driven discretionary trader with a growing systematic/quant side project**, not a chartist and not an earnings-flow trader in the traditional sense.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags?
**Unknown — and that is itself the finding.** In 10 posts across 20 months, there is not a single sentence describing a sale, a trim, a stop-out, a scale-out, or a loss. The only PnL-flavored post in the entire archive is a two-word victory lap: *"It begins."* We independently pulled OHLCV history for his two most specific, verifiable calls to test what actually happened after he went silent:

**$ABAT** — post #5 (2025-07-16): *"Was debating $UNH at open yesterday. Went $ABAT instead. So far, so good."*
- His entry window (July 15, 2025): stock traded $1.65–$1.89.
- Post #6, "It begins" (2025-09-18): stock closed **$3.00** that day — already **+59% to +76%** from his entry, *before* he even announced the win. A follower buying on the announcement itself would already be chasing a stale move.
- What he never mentioned: $ABAT then went fully parabolic, spiking to an intraday high of **$11.49 on 2025-10-15** (+~500% from his entry) on a huge volume blow-off (55M shares vs. a typical 3–8M), then **crashed to $4.76 within two trading days** (2025-10-17) — a ~59% collapse from peak in 48 hours.
- By the time his tracked portfolio value hit its high-water mark of $161,888 (Jan 2026), $ABAT had settled back to the **$4.60–$4.90** range — still a real, substantial gain from his entry, but nowhere near the October peak.
- As of 2026-09-10 (report date), $ABAT trades at **$2.56** — *below* his implied entry range on a nominal basis, and down **~77% from the October 2025 peak.** He never posted about the top, the crash, or the current level. Total silence for 12 months on his one documented "Gain"-tagged position.

**$DGXX** — post #9 (2026-01-21): *"Timed at $2.91. Never underestimate indicators."*
- His called level ($2.91) sat right at that day's intraday low ($2.895); the close was $3.06.
- What he never mentioned: the stock **fell through his called level to $2.15 by 2026-02-05** (a ~26% adverse move against the "timed" bottom), chopped in a $2.20–$3.00 range for two more months, then **exploded from a $3.37 close (Apr 30) to a $9.20 peak (May 13, 2026)** — a violent, gap-driven +173% move on 115M-share and 31M-share volume days (30–100x normal turnover), consistent with a short-squeeze/news event, not a slow trend.
- By 2026-09-10, $DGXX has round-tripped most of that spike, trading back down to **$3.70**.
- He never posted again about $DGXX — not at the -26% drawdown, not at the +216%-from-call peak, not at the round trip back to roughly where he "timed" it.

### How does he manage losing positions?
There is no visible evidence he manages them at all — because he never discloses having one. Given that both of his most specific, verifiable calls independently went through double-digit-percent adverse excursions *before* their eventual (also undisclosed) resolution, the most defensible read is: **either he has a real, silent exit discipline he simply doesn't write about, or he holds through drawdowns and only surfaces when the position happens to be green.** Both are plausible; neither is confirmed; and Artemis must not assume either as ground truth.

### Documented wins vs. blow-ups
- **Documented wins:** 1 explicit ("$ABAT — It begins"), independently corroborated as a real, sizeable, correctly-timed rotation call.
- **Documented blow-ups:** **Zero.** Not one loss, in any post, in 20 months, across instruments (small-cap equities, particularly) with realized volatility this extreme. This is a textbook **survivorship-biased self-report** — the archive is not evidence he doesn't lose; it is evidence he doesn't *publish* losing.

---

## 4. Behavioral & Sentiment Signals

**Why is he posting?** Three distinct motives recur, in descending frequency:
1. **Documenting a side project** he's proud of (the Alpaca-driven "stock vibe app," the LPPLS Pine Script research, the Kalshi API note) — these are the most detailed, highest-effort posts in the archive, and none of them are trade calls.
2. **A quarterly-ish accountability ritual** for the original $10k basket ("will check back in periodically... other than quarterly checkins") — a ritual he explicitly sets up and then **fails to keep** (the actual gaps are 65, 106, and 123 days, and eventually a 217-day disappearance).
3. **Opportunistic flexes** when a specific, timed call worked ("It begins," "Never underestimate indicators") — always brief, always declarative, always devoid of a forward level or a risk plan.

**Recurring linguistic patterns:**
- **Hedge language as a permanent feature, not an exception:** "chance play," "hunch," "we'll see," "should've been in this sooner tbh," "so far, so good," "doing... ok?," "at least captivating." He almost never states a hard thesis without immediately softening it.
- **Retrospective regret over concentration, not over losses:** *"Really should've all-ined $AS (added in Feb) or $HOOD..."* — his self-criticism is about under-sizing winners, never about a bad trade. This is a **strong tell that his real behavioral flaw is diversification-into-mediocrity, not poor stock-picking** — he picks well often enough that his biggest documented regret is not going big enough on his own best ideas.
- **Detached, cerebral tone under volatility, never emotional:** even his most enthusiastic posts ("It begins," "Interesting stuff," "It's at least captivating") read as an engineer admiring a system working, not a trader sweating a position. There is no red-day language anywhere in the archive — no panic, no capitulation, no revenge-trade signal. Either he genuinely doesn't experience/post through drawdowns, or — more likely given the data above — he simply doesn't write when things are red.
- **Self-aware humility about content quality:** *"I mean I'm on this app aren't I"* (justifying an $RXRX position) is a joke acknowledging the post is filler-tier reasoning — useful context for weighting how much thesis-depth to expect from his basket names generally.

**Reaction to market volatility / red days:** Not observable directly — no post is written during or immediately after a documented drawdown in his own book. The nearest proxy is his framing of the $UNH "bad news" post: he treats *someone else's* red day as an opportunity to rotate into a name he liked better, same session — a fast, opportunistic, unsentimental reflex, not a defensive one.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

| Tier | Tag | Rationale |
|---|---|---|
| **Primary** | `THEMATIC_MOMENTUM_ROTATOR` | Builds diversified political/seasonal thematic baskets, then opportunistically rotates single names off same-day news (UNH→ABAT) |
| **Secondary** | `QUANT_TOOLING_HOBBYIST` | Genuine systematic-methods exposure (Pine Script, LPPLS bubble model, Alpaca paper-trading bot, Kalshi API) not yet proven to translate into disclosed, sized, risk-managed trades |
| Flag | `SURVIVORSHIP_BIASED_DISCLOSURE` | 100% of PnL-adjacent posts are wins; 0% are losses, across 20 months and multiple high-beta names |
| Flag | `SILENT_EXIT_RISK` | Both verifiable flagship calls (ABAT, DGXX) go completely dark at the exact moment the position's fate becomes ambiguous (post-parabola, post-drawdown) |
| Flag | `LOW_CADENCE_UNRELIABLE_FEED` | 0.11 posts/week average; gaps up to 217 days; cannot function as a timely signal source |
| Flag | `MICROCAP_GAP_RISK_MAGNET` | Both disclosed named single-ticker calls involve sub-$5, low-float names with 10x–30x volume spikes and 50–75% multi-day round trips |

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 39 / 100 — "Speculative Tail-Watch" tier.**

| Component | Weight | Score | Basis |
|---|---|---|---|
| Directional hit rate (disclosed single-ticker calls) | 25 | 20/25 | 2/2 verifiable calls (ABAT, DGXX) were directionally correct at time of and after posting — but n=2 is statistically meaningless |
| Post cadence / usability as a live feed | 15 | 3/15 | 0.11 posts/week; up to 217-day dark stretches |
| Risk-management transparency | 20 | 2/20 | Zero disclosed losses, zero disclosed stops, zero disclosed sizing after the initial basket |
| Exit discipline / profit-taking evidence | 15 | 2/15 | Never once documents an exit; goes silent at both flagship positions' peak ambiguity |
| Repeatability / thesis depth | 15 | 5/15 | Several names explicitly self-labeled "chance play" / "hunch"; basket construction later regretted by the author himself |
| Infrastructure & quant sophistication | 10 | 7/10 | Real Pine/LPPLS/algo-backtesting and Kalshi API work — above median for the cohort, though not yet shown to convert into disclosed P&L |
| **Total** | **100** | **39** | |

**Expectancy: Not statistically computable — flagged INDETERMINATE at n=2 named single-ticker calls.** The two disclosed calls bracket an enormous, entirely undisclosed range depending on assumed (unverified) exit timing:

| Ticker | Entry (from post text) | Post-announcement peak | Peak-implied return | Subsequent round-trip |
|---|---|---|---|---|
| $ABAT | ~$1.70–$1.89 (2025-07-15) | $11.49 (2025-10-15) | **+507% to +575%** if held to peak | -77% from peak to 2026-09-10 ($2.56) |
| $DGXX | $2.91 "timed" (2026-01-21) | $9.20 (2026-05-13) | **+216%** if held to peak, after a -26% adverse excursion first | -60% from peak to 2026-09-10 ($3.70) |

The honest expectancy statement for Artemis: **@moloch's calls have, so far, pointed in the right direction before an enormous, uncaptured (as far as the record shows) move — and then given almost all of it back before he ever mentions the ticker again.** Treat any single-name harvest from this source as requiring Artemis's *own* exit discipline layered on top, never his.

### 5.3 Signal Flow Ingestion Matrix

```
┌─────────────────────────────┬──────────────────────────────┬───────────────────────┬──────────────────────────────────────────┬────────────┐
│ Signal Type                 │ Trigger Pattern               │ Historical Reliability│ Ingest Action                              │ Confidence │
├─────────────────────────────┼──────────────────────────────┼───────────────────────┼──────────────────────────────────────────┼────────────┤
│ News-driven same-day rotation│ Fades a bad-news large-cap    │ 1/1 verified: +59-76% │ Auto-flag the destination ticker for a     │ MEDIUM     │
│ (e.g. UNH→ABAT)              │ into a thematically-adjacent  │ within 2 months        │ 24h volume/technical scan                  │            │
│                              │ small/microcap, same session  │                        │                                             │            │
├─────────────────────────────┼──────────────────────────────┼───────────────────────┼──────────────────────────────────────────┼────────────┤
│ Proprietary-indicator timing │ "[Chart]"/"[Dd]" tags citing a│ 1/1 verified: -26%     │ Flag ticker for elevated IV/gamma/squeeze   │ MEDIUM-LOW │
│ call (LPPLS, "Timed at $X")  │ specific numeric level from   │ drawdown first, then   │ scan; do NOT enter on the level itself —   │            │
│                              │ his own model                 │ +216% eventual peak    │ expect an adverse move before any payoff   │            │
├─────────────────────────────┼──────────────────────────────┼───────────────────────┼──────────────────────────────────────────┼────────────┤
│ Diversified thematic basket  │ 8-10 tickers bundled on a     │ Regretted by author    │ Log as low-conviction watchlist adds only; │ LOW        │
│ launch                       │ political/seasonal narrative  │ himself (should've     │ never auto-size                            │            │
│                              │                                │ concentrated instead)  │                                             │            │
├─────────────────────────────┼──────────────────────────────┼───────────────────────┼──────────────────────────────────────────┼────────────┤
│ "[Gain]"-tagged victory-lap  │ Posted only after the move    │ Definitionally lagging │ IGNORE for entry. Use only to backtest his │ NONE       │
│ post                         │ already happened, no forward  │ (move already +59-76%  │ historical hit rate offline                │ (lagging)  │
│                              │ price level given              │ by time of post)       │                                             │            │
├─────────────────────────────┼──────────────────────────────┼───────────────────────┼──────────────────────────────────────────┼────────────┤
│ Self-labeled "chance play" / │ Explicit low-confidence       │ N/A — author-disclaimed│ Fade/ignore entirely; do not mirror sizing │ NONE       │
│ "hunch" tickers               │ language in the post itself    │                        │                                             │            │
├─────────────────────────────┼──────────────────────────────┼───────────────────────┼──────────────────────────────────────────┼────────────┤
│ Post-call silence >90 days   │ No follow-up after a named    │ Correlates with 60-77% │ Treat as a WARNING, not a hold signal —    │ N/A        │
│                               │ ticker call                    │ peak-to-current givebacks│ time-box and force independent re-confirm │            │
│                              │                                │ in both verified cases │                                             │            │
├─────────────────────────────┼──────────────────────────────┼───────────────────────┼──────────────────────────────────────────┼────────────┤
│ Tooling/infrastructure posts │ Describes own bot/indicator/  │ N/A — not a trade call │ Ingest as background intel only (his stated│ INFRA-ONLY │
│ (Alpaca bot, Kalshi API)     │ API, not a position             │                        │ edge thesis = "volume is the main thing to │            │
│                              │                                │                        │ scalp")                                     │            │
└─────────────────────────────┴──────────────────────────────┴───────────────────────┴──────────────────────────────────────────┴────────────┘
```

### 5.4 Execution Directives for the Artemis Engine

**A. Ingestion Directives — genuine edge to harvest**
1. Auto-flag any ticker he rotates *into* on the same day he abandons a bad-news large-cap — this pattern (UNH→ABAT) is his single best-verified, fastest-resolving signal type.
2. Treat his "[Chart]"/"[Dd]" proprietary-level calls as a **leading indicator of an eventual large move, with an expected adverse excursion first** — queue for elevated-volatility/squeeze monitoring, not immediate entry.
3. Mine his own stated edge thesis literally: *"the longer I've traded short term, the more I believe volume is basically the main thing to scalp."* Weight abnormal-volume-on-low-float as the closest mechanical proxy Artemis has to his real method.
4. Use his LPPLS/bubble-oscillator research as a pointer to a legitimate quant technique (Sornette log-periodic power law) worth Artemis independently implementing and backtesting — the idea has more standalone merit than his personal track record of using it.

**B. Contrarian Fade Directives — when to fade his calls or the retail herd around him**
1. **Fade any "[Gain]"-tagged post as an entry trigger.** By construction it is stale — the move it celebrates has already happened.
2. **Fade the basket-diversification instinct, not the underlying names.** His own biggest regret is under-concentrating in winners he already owned (AS, HOOD) — Artemis should treat his multi-name baskets as a sourcing list to re-rank by independent conviction, not a sizing template.
3. **Fade anything he explicitly labels "chance play" or "hunch."** He is telling you, in his own words, that the thesis has no depth.
4. **Fade retail momentum-chasing into his named microcaps after a big printed run** — both $ABAT (Oct 2025) and $DGXX (May 2026) posted 30x-normal-volume blow-off spikes immediately followed by 50-75% round trips. Anyone piling in on the spike headline is buying the top of a pump, not the start of a trend.

**C. Mandatory Risk Blacklists & Firewalls**
1. **Sub-$5 / low-float microcaps sourced from this trader require independent liquidity, float, and short-interest screening before any auto-sizing** — his two verified names both showed classic pump-and-dump tape (intraday ranges of 30-40%, single-day volume 10-30x average).
2. **Never treat his silence as a hold signal.** Absence of a loss post is not evidence of no loss — his feed is 100% survivorship-biased by his own posting behavior. Blacklist his feed as a standalone risk-management reference.
3. **Firewall the `amount_k` portfolio-value series from being read as a clean, deposit-adjusted return stream.** He explicitly admits to adding/changing the book; treat $10k→$161.9k as a headline number, not an audited return.
4. **Cap any options/leverage replication at a symbolic sleeve size.** His only leverage commentary (LPPLS post) is aspirational — "leveraged... calls / puts" — with zero disclosed options trade history to back it.
5. **Out-of-scope: Kalshi/prediction-market and crypto exposure.** One post, no track record, no equity-relevant edge — do not extend his equity classification tags to this asset class.

**D. Exit Rules & Alpha Rectification**
1. **Impose a mechanical trailing stop (20-25% off post-entry high) on any position sourced from a @moloch signal**, since Artemis cannot rely on him to ever disclose an exit. Both verified names gave back the majority of their gains with zero warning from the source.
2. **Scale out in tranches** (e.g., trim 1/3 at +50%, 1/3 at +100%, trail the remainder) rather than mirroring an assumed buy-and-hold — his own regret pattern shows he under-manages winners, and Artemis should not assume better discipline exists off-camera.
3. **Time-box the thesis: 90 days of silence = stale.** If no follow-up post and no independent technical confirmation arrives within 90 days of a named call, de-weight or exit regardless of price action.
4. **Never buy the "[Gain]" post itself.** Treat it as the closing bell on the trade idea, and instead open a monitoring ticket for a pullback re-entry with fresh, independent confirmation.

---

## 6. Chronological Milestone & Catalyst Log

| # | Date | Tag(s) | Tickers | Event | Independently Verified Market Reaction |
|---|---|---|---|---|---|
| 1 | 2024-12-14 | `[Discuss]` | RIVN, QTUM, UPS, DPRO, ONDS, VRT, RXRX, BKSY, HOOD, RDDT | Launches a $10,000, 10-name "Year Long Port" on political/thematic/seasonal hunches; explicitly frames it as entertainment over conviction | — |
| 2 | 2025-02-17 | `[Discuss]` | AS | Opens a discussion post floating $AS (Amer Sports) as a seasonal consumer play, no position size given | — |
| 3 | 2025-06-04 | — | AS, ONDS, HOOD | "June checkin" — first tracked portfolio value: **$15,410** (+54.1% from stated $10k start); admits regret at not concentrating in AS or HOOD | — |
| 4 | 2025-06-28 | — | — | Reveals a self-built "stock vibe app" (Alpaca-paper-trading command-line tool); states his core edge thesis: *"volume is basically the main thing to scalp"* | — |
| 5 | 2025-07-16 | `[News]` | ABAT, UNH | Fades UNH's bad Q4 print same-day, rotates into ABAT instead ("So far, so good") | ABAT trading $1.65–$1.89 entry window (7/15/25) |
| 6 | 2025-09-18 | `[Gain]` `[Gain]` | ABAT | Two-word victory post: "It begins." Portfolio value now **$68,848** (+346.8% since June) | ABAT closed **$3.00** that day — already +59-76% from his entry, *before* announcement. Stock then spiked to **$11.49** (10/15/25, unmentioned) before crashing to $4.76 within 48h (also unmentioned) |
| 7 | 2026-01-19 | `[Dd]` | — | "Good read" — describes researching LPPLS bubble-oscillator strategies in Pine Script off outside reading. Portfolio value **$161,888** (+135.2% since Sep) | — |
| 8 | 2026-01-20 | `[Dd]` | — | "LPPLS" follow-up — frames the model as a once-a-quarter, leveraged, direction-agnostic options bet around volatility "earthquakes," not a compounding strategy. Same **$161,888** snapshot | — |
| 9 | 2026-01-21 | `[Chart]` | DGXX | "Timed at $2.91. Never underestimate indicators." — a specific, numeric technical call | DGXX closed $3.06 that day, then **fell to $2.15 by 2/5/26** (-26% from call), before eventually spiking to **$9.20** on 5/13/26 (+216% from call, on 30-100x normal volume) — both moves unmentioned by him |
| 10 | 2026-08-26 | `[Crypto]` | — (Kalshi) | 217 days of silence broken by an operational note: Kalshi's exchange-sharding update tripped up his API trading. No equity/portfolio update accompanies it | — |

**Current status (as of 2026-09-10): dormant, 15 days since last post.** No portfolio value, position, or performance update has been given since the $161,888 snapshot in January 2026 — a period spanning both the confirmed 77% ABAT peak-to-trough decline and the confirmed DGXX round trip. This is the single most important open item in his file: **the last thing Artemis knows for certain is a 13-month, unverified, possibly deposit-inflated +1,519% headline, followed by seven-plus months of complete silence through two large, independently confirmed reversals in his named holdings.**
