# Quant Forensic Autopsy: Trader @TheRealChad

**Target Profile**: `@TheRealChad` (`prf_ca30bd0bafa44d3cb4347c7c2c3a2187`)
**Platform**: AfterHour (#20 Most Active Followed Trader)
**Dataset Analyzed**: 505 Lifetime Posts (2024-05-10 → 2026-08-27, 838 calendar days)
**Sources**: `@TheRealChad_all_posts.json` (raw telemetry) + `@TheRealChad_lifetime.md` (narrative archive)
**Analyst**: Claude Sonnet 5 / Artemis Engine Forensics

---

## 1. Executive Profile

### 1.1 Trader Philosophy & Archetype

`@TheRealChad` is a **reflective, family-oriented retail swing trader who runs multiple sub-accounts and operates primarily as a second-order signal amplifier** rather than an independent alpha generator. He is articulate, writes long-form DD and "Sunday Reflection" essays (parables, Charlie Munger quotes, personal-finance philosophy), and is unusually transparent about failure — he is one of the few traders in this cohort who **names and quantifies his own worst trades in public** ("possibly one of the worst trades of my life").

His trading identity is bimodal:
- **The Journal-Keeper**: disciplined profit-taker on his "normal" swing book — scales out of options in tranches ("sold half," "sold last runner"), rotates capital across four disclosed sub-accounts (shares-only, options+shares, and two small "challenge accounts"), and posts monthly self-graded performance report cards.
- **The Ideological Bagholder**: on a small number of thesis-driven, narrative-heavy names (OKLO nuclear SMRs, MTPLF Bitcoin-treasury arbitrage), he abandons the scale-out discipline entirely, doubles down into red, and rides concentration risk to 25%+ of the portfolio.

Critically, **he is largely a copy-trader**. By his own repeated admission, entries and exits on several of his largest and longest-held positions (UBER, RXRX, OKLO, CELH, TTD) were triggered by named AfterHour peers — most often **`@ThetaTard`** and **`@SirJack`** — not independent research:
> *"It is very hard to hold it when @ThetaTard exits with logic. I was influenced to take this position by him and it is only fitting that he influences the exit as well."* (2025-02-21, $UBER)
> *"When both @ThetaTard and @Bobdog are in. I am in!"* (2025-02-25, $TTD)
> *"His call was perfect... I remember buying this when it was ALCC when SirJack bought it."* (2024-12-17, $UBER DD)

He is a family man (references an infant daughter, born ~Sep 2024, and a COVID scare in Feb 2025), had parents who were victimized by a meme-coin scam, and cites a deceased mentor. Personal-life and market-philosophy content make up a meaningful share of his feed — this is not a pure trade-alert account (`is_hunt_post` is `false` on all 505 posts).

### 1.2 Post Cadence & Active Timeline

| Window | Posts | Duration | Cadence |
|---|---|---|---|
| **Full lifetime** | 505 | 838 days / 119.9 weeks | **4.2 posts/week** (blended, misleading — see below) |
| **Hot Window** (2024-12-13 → 2025-04-30) | 379 | 19.7 weeks | **19.2 posts/week** |
| **Peak month**: Feb 2025 | 191 posts | 28 days | **6.8 posts/day**, peaking at **20 posts on 2025-02-20 alone** |
| **Dark Period #1**: 2024-06-15 → 2024-12-04 | **0 posts** | 172 days (~24.6 weeks) | Total silence after account blowup |
| **Post-capitulation tail** (2026-02-13 → 2026-08-27) | 7 posts | 195 days | ~1 post every 4 weeks |

```
Post Volume by Month (May 2024 - Aug 2026)
2024-05:  39  ■■■■■■■■■■■■■■■■■■■■
2024-06:   3  ■■
2024-07..11:  0  (SILENT — post-blowup disappearance)
2024-12:  44  ■■■■■■■■■■■■■■■■■■■■■■
2025-01:  65  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
2025-02: 191  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
2025-03:  67  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
2025-04:  16  ■■■■■■■■
2025-05:   3  ■  (brief unlink: "emotions are settled")
2025-06:  24  ■■■■■■■■■■■■
2025-07:   4  ■■
2025-08:   3  ■
2025-09:   3  ■
2025-10:  16  ■■■■■■■■  (MTPLF drama peak)
2025-11:   9  ■■■■■  (MTPLF capitulation)
2025-12:   3  ■
2026-01:   5  ■■
2026-02:   3  ■  (final loss disclosure + port unlink)
2026-03..08: 4 total, scattered single spectator posts
```

**Cadence is a volatility/anxiety signal, not a steady journal.** The Feb 2025 spike (191 posts, 38% of his lifetime output in one month) coincides with a real tariff/growth-scare equity correction — his post rate roughly *triples* in the days market drawdown accelerates (16 posts on 2/27, 16 on 2/28, 20 on 2/20). This pattern repeats at smaller scale around the Oct–Nov 2025 MTPLF/BTC-treasury unwind. Silence, conversely, correlates with **shame after large losses** (172 days dark after the Jun 2024 blowup) or **deliberate emotional withdrawal** ("Sorry was gone for a while there. My emotions are settled," 2025-05-23).

### 1.3 Verified Capital Trajectory & Drawdown History

`amount_k` is a live brokerage-sync balance (in $ thousands) embedded per post, with sub-cent jitter for anonymization — confirmed by his own language: **`0.0` = portfolio unlinked/not synced**, not a literal zero balance (he explicitly states "I have unlinked the port" on 2026-02-12).

```
Equity Curve (Verified Sync Points, $K)
$280K |            ▲ Jun 11 '24: $278.5K
      |           /|
      |          / |  ▼ Jun 14 '24: $2.28K  ("TSLA YOLO — either
      |         /  |                          prints or I lose everything")
$150K | ●0.86K /   |
      |───────/    |          ░░░░░░░░░░░░░░░░░░░░░░░░ 172-DAY BLACKOUT ░░░░░░░
$0K   |            └─────────────────────────────────┐
      |                                               ▼ Dec '24 relink: $0→$140K
$210K |                                                    ▲ Jan '26 ATH: ~$208K
      |                                                   /│\
$150K |                                    ┌─────────────/ │ \___
      |                              ┌─────┘               │     \___ ▼ Feb '26: $149-155K
$0K   |______________________________|______________________________\___[UNLINKED — "Life is
       May'24  Jun'24    Dec'24   ...  2025 (choppy, 8 sub-peaks)  ...  Jan-Feb'26   too short..."]
```

**Milestone A — The OKLO "Complacency" Lesson (May 2024).** Opening act of the archive: builds a 3,000-share OKLO position plus short calls while it's crashing ("$OKLO is scary... I have detached myself emotionally"), writes a full DD thread, then trims: *"a valuable learning lesson in being complacent and risk management."* Balance at this point: ~$17K–$31K.

**Milestone B — The June 2024 Blowup.** Balance rockets from ~$31K to a verified **$278,535** on 2024-06-11 ("I could have made 200K today but settled for 50K instead"). Three days later, on a leveraged TSLA "**either prints or I lose everything**" YOLO he explicitly deferred to a peer's (`@neverpullover`) instincts on, the synced balance reads **$2,275** — a **~99.2% collapse in 72 hours**, one of the most severe single verified drawdown events in this trader cohort. He then vanishes from the platform for **172 consecutive days**.

**Milestone C — The Rebuild (Dec 2024).** Posts resume 2024-12-05 with the port unlinked (`$0.0`); by 2024-12-13, once relinked, the balance reads **$140,844**. Whether this reflects fresh capital, a rebuilt account, or a previously-untracked account being connected to AfterHour for the first time cannot be fully verified from the data — but the disclosed arc is a genuine, fast comeback from near-total ruin.

**Milestone D — Choppy 2025 Grind.** Balance oscillates through 2025 in the $124K–$220K band across at least 8 local peaks/troughs, briefly touching $44K in a May 2025 dip (coincident with a stated emotional-withdrawal micro-hiatus), then recovering to a **legitimate ATH of ~$205–208K around October 2025–January 2026** (per his own retrospective: *"Final portfolio value as of today $155K, ATH was at 205K"*).

**Milestone E — The MTPLF-Driven Unwind & Voluntary Exit (Oct 2025 – Feb 2026).** A single concentrated position (Metaplanet, ticker `MTPLF`, a Bitcoin-treasury proxy) grows to **26% of the entire portfolio** by mid-Oct 2025, gets averaged down repeatedly ("loaded the boat," 15K→17K shares, avg $4.97–$5.00), then is capitulated on 2025-11-19 at **-55% realized loss** ("possibly one of the worst trades of my life"). Combined with broader Jan–Feb 2026 market weakness, the account round-trips from its ~$205–208K ATH down to **$149,309** by 2026-02-06 ("I am officially set back to Feb 2025" — a full **year of gains erased**, ≈**-27% peak-to-trough**). On 2026-02-12 he **voluntarily de-risks to 40%+ cash** (buys `FXAIX`, `SGOV`), unlinks the portfolio permanently, and announces an indefinite hiatus: *"Paper money doesn't nourish the soul or the body."* Unlike the 2024 blowup, this exit is **proactive and rules-adjacent** (stated a discretionary "damage control mode"), not a forced wipeout — a modest sign of behavioral maturation over the ~26-month arc, even though the trigger was still emotional exhaustion rather than a pre-committed stop.

**Net verifiable outcome**: Starting near-zero (2024-05) → catastrophic ~99% blowup (2024-06) → full rebuild to $140K (2024-12) → ATH ~$208K (early 2026) → voluntary retirement at $149-155K (2026-02), i.e., roughly **+7-11% net vs. the post-rebuild Dec-2024 baseline**, achieved only by walking through two severe drawdown events (-99% and -27%) that a risk-controlled process would not have permitted.

---

## 2. Ticker Universe & Catalysts

### 2.1 Frequency Matrix

| Tier | Tickers (post mentions) | Instrument Mix | Role |
|---|---|---|---|
| **Tier 1 — Core Convictions** | `$UBER` (35) `$OKLO` (8) `$RXRX` (9) `$OXY` (8) `$TTD` (10) | Shares (multi-thousand-share core) + covered calls/leaps for income | Long-held, DD-backed, largely copy-sourced from `@ThetaTard`/`@SirJack` |
| **Tier 2 — Mega-Cap Trading Vehicles** | `$NVDA` (31) `$AAPL` (6) `$TSLA` (7) `$PLTR` (7) `$AVGO` (7) `$AMD` (3) `$GOOGL` (5) | Directional calls/puts around earnings and macro prints | Tactical vehicles, not conviction holds |
| **Tier 3 — Index / Volatility Overlay** | `$SPY` (61, top ticker) `$VXX` (4) `$GLD` (2) `$TLT` | Weekly puts/calls, hedges, market-commentary anchor | Sentiment barometer + tactical hedge book |
| **Tier 4 — Ideological / Speculative Bags** | `$MTPLF` (16) `$LCID` (8) `$ACHR` (5) `$LUNR` (4) `$ONDS` (3) `$KULR` (3) `$RIVN` (4) `$CVNA` (3) | Concentrated equity, averaged down aggressively | Bagholder graveyard — MTPLF is the single worst position of his career |

### 2.2 Options vs. Equities

Roughly balanced hybrid, skewing toward defined tactics: **"call" appears 163×, "shares" 165×, "put" 61×, "covered call" 14×, "leaps" 8×, "theta" 19×**. He runs a genuine income overlay on core longs (RXRX covered calls: *"These are at 50% profit now. Theta working for me"*; OXY covered calls sold into earnings) while using naked directional options (SPY puts/calls, NVDA/AMD earnings gambles, CELH/OKLO YOLO calls) for tactical alpha and adrenaline trades tagged `Yolo` (31 posts carry this tag).

### 2.3 What Drives Entries

1. **Social copy-trading (dominant driver)** — `@ThetaTard` (10 direct @-mentions, cited as the reason for entering/exiting UBER, RXRX, TTD) and `@SirJack` (13 mentions, cited for OKLO, CELH, the UBER/ALCC predecessor trade) function as his primary signal sources.
2. **Earnings/catalyst timing** — ER gambles on AMD, DXCM, AVGO, GOOGL; explicit catalyst dates tracked (OKLO's 5/15 and 5/26 regulatory dates).
3. **Macro/technical overlay** — Fed/rate-cut commentary (9 mentions), tariff and China-policy anxiety (8+13 mentions), hedge-fund positioning calls (*"Be ready for pull back... because of the amount Hedge Funds positioned short,"* his 9th-most-reacted post), RSI/monthly-chart breakout levels on UBER.
4. **Thematic/fundamental DD (self-generated, but poorly risk-managed once committed)** — OKLO's NRC/SMR nuclear regulatory thesis and MTPLF's Bitcoin-treasury mNAV-discount thesis are both genuinely researched, multi-post DD efforts; the failure mode isn't idea generation, it's **position sizing and exit discipline** once the thesis is underwater.

---

## 3. Risk Management & PnL Reality

### 3.1 Does He Take Profits or Hold Bags? **Both — split cleanly by ticker type.**

**On "normal" swing names, he is a disciplined scaler.** Feb 2025 alone shows the pattern repeatedly: *"Sold half of $SPY puts for 100%," "Sold last $GLD runner call for 140%," "sold 4 calls, leaving 1 runner"* ($OXY), *"Sold $UBER. Big gains % are taken not given"* (Apr 2025). He explicitly self-labels this style: *"What a move! I like selling to strength. Call it my weakness."*

**On ideological/thematic names, discipline collapses entirely.** MTPLF is the case study: bought May 2025, "loaded the boat" to 15K shares in Oct, added another 2,000 shares *below mNAV* the same week BTC-treasury insiders were reportedly adding shorts, grew to **26% of the portfolio ("making it my largest hold")**, and was held through a stated "see you all in 2030 or in Valhalla" bravado post — before capitulating five weeks later at **-55%**. His own post-mortem (2026-01-18) diagnoses the mechanism precisely: *"DCA down is worse than DCA up... My position was about 17000 shares with an average of 4.97. I capitulated at 2.15... It has recovered to 3.8"* — he sold within shouting distance of the local bottom, the single most common retail capitulation error.

### 3.2 Managing Losing Positions

Three distinct failure/recovery modes appear in the archive:
1. **Sleep-deprived impulse trades**: *"Sold the call for $220 loss... Lesson learned: Sleep and get enough rest or you take stupid trades. One bad trade needed 3 good ones to recover."* (2025-03-06, post-AVGO "debacle")
2. **Averaging into a falling knife until forced capitulation** (MTPLF, above) — the account's single largest verified loss event.
3. **A full account wipeout followed by disappearance** (Jun 2024 TSLA YOLO, -99% in 72 hours, 172 days of silence) — the most severe pattern, effectively "blow up and ghost."

### 3.3 Documented Wins vs. Blow-Ups

- **Disclosed win rate**: 46 posts tagged `Gain` vs. 25 tagged `Loss` = **64.8% self-reported win rate** (only ~14% of all posts carry an explicit outcome tag — meaningful **self-report/survivorship bias**, as traders disproportionately post wins).
- **Best documented month**: February 2025 self-reported account report card — *"Shares only account +12%, Options+shares account +4%, Challenge account #1 +38%, Challenge account #2 +5%... SPY declined -2.39%"* — genuine, if small-sample, outperformance across all four of his disclosed sub-accounts in a down tape.
- **Worst documented events**: (a) the Jun 2024 ~99% single-account collapse; (b) the Nov 2025 MTPLF capitulation at -55% realized loss on a position sized at over a quarter of the portfolio; (c) the cumulative ~27% peak-to-trough portfolio drawdown (Jan 2026 ATH $208K → Feb 2026 exit $149K) that ended his active-trading era.

**Verdict**: he is a competent tactical scalp-and-scale trader wrapped around a chronic, unresolved weakness for concentrated, narrative-driven conviction bets that he cannot exit rationally once underwater.

---

## 4. Behavioral & Sentiment Signals

### 4.1 Why Is He Posting?

Three overlapping motives, in descending order of post volume:
1. **Processing volatility in real time.** Post rate roughly triples during drawdown weeks (Feb 2025, Oct–Nov 2025) — AfterHour functions as a stress-coping journal, not a curated alert feed.
2. **Community/social validation and copy-trade signaling.** Frequent tagging of `@ThetaTard`, `@SirJack`, `@Bobdog`, `@shortsqueeze`, `@DocHollywood` — he trades *with* a small in-group and narrates the group's consensus in real time ("When both @ThetaTard and @Bobdog are in. I am in!").
3. **Moral/philosophical reflection**, largely decoupled from trading ("Sunday Reflection" essays using parables — the "Chad and Brad" market-timing fable — Charlie Munger quotes, a PSA about infant RSV/COVID risk, a reflection on a road-rage-adjacent killing). These posts draw some of his highest engagement (top-reacted post overall is "INVESTING 101 — The cost of timing the market," 31 reactions; "PSA — COVID is still ravaging communities," 29 reactions).

### 4.2 Linguistic & Sentiment Fingerprints

- **Self-effacing confession as a recurring genre**: "Full disclosure- I goofed up on $AVGO" (41 comments, his most-commented post ever), "Hot potato 🥵 - This was dumb," "$HCTI It was a dumb yolo so never mentioned it," "Sorry for not being able to diamond hand." He is unusually willing to publicly own mistakes — a genuine positive trait for a research source, but also evidence he *knows* his risk discipline is weak and does it anyway.
- **Copy-trade language as a tic**: "If Bro is in, I am in," "Thanks @SirJack," "I trust @neverpullover instincts," "influenced me."
- **Bravado immediately before capitulation**: "See you all in 2030 or in Valhalla" (MTPLF, five weeks before he capitulated at -55%) — a reliable **local-bottom-adjacent overconfidence tell**.
- **Reaction to red days/volatility**: shifts from trade-execution posts to defensive/philosophical framing — "Nothing is going to zero," "Don't play levered bets... keep your inner peace," "damage control mode on," "the blood bath seems to have just begun" (all from the single Feb 6, 2026 post that preceded his exit).
- **Emotional withdrawal as a coping mechanism**: two distinct multi-month "ghosting" events (172 days in 2024, a shorter one in May 2025, and finally a permanent unlink in 2026) — always following stress/loss, never following a win.

---

## 5. Quantitative Verdict for TraderMatrix

```
+-----------------------------------------------------------------------------------+
|                           TRADERMATRIX CLASSIFICATION                             |
|                                                                                    |
|   PRIMARY TAG:      COPY_TRADE_SIGNAL_AMPLIFIER                                   |
|   SECONDARY TAG:     CONCENTRATED_THEME_BAGHOLDER                                 |
|   TERTIARY TAGS:     SWING_OPTIONS_SCALER / VOLATILITY_ANXIETY_POSTER             |
|   ALPHA STATUS:      Bimodal — Positive Tactical Alpha / Negative Concentration   |
|                       Alpha                                                       |
|   ALGORITHMIC ALPHA SCORE:   32 / 100                                             |
|   RECOMMENDED FIT:    Retail-Sentiment Barometer & Contrarian-Extreme Fade Source |
|                       — NOT a direct mirror-trading candidate                     |
+-----------------------------------------------------------------------------------+
```

### 5.1 Algorithmic Classification Tags & Expectancy

- **Primary**: `COPY_TRADE_SIGNAL_AMPLIFIER` — his highest-conviction, longest-held names (UBER, OKLO, RXRX, TTD, CELH) trace to `@ThetaTard`/`@SirJack` entries and exits, not independent research.
- **Secondary**: `CONCENTRATED_THEME_BAGHOLDER` — repeated willingness to size a single narrative bet (MTPLF) to >25% of NAV and average down through a -50%+ drawdown before capitulating near the low.
- **Supporting tags**: `SWING_OPTIONS_SCALER` (genuine, positive-expectancy scale-out discipline on non-ideological names), `VOLATILITY_ANXIETY_POSTER` (post cadence is a leading indicator of his own stress, not of market direction), `BOOM_BUST_ACCOUNT_HISTORY` (one verified ~99% blowup, one verified ~27% voluntary-exit drawdown in 26 months).

**Algorithmic Alpha Score: 32 / 100.**
- +Credit for a real, if narrow, tactical edge on scale-outs (Feb 2025 self-reported account report card beat SPY across all four sub-accounts in a down month).
- +Credit for early, well-sourced DD (OKLO NRC regulatory thesis, MTPLF mNAV-arbitrage thesis) that was directionally correct in the fullness of time (MTPLF later recovered from $2.15 to $3.80 — after he had already sold).
- −Heavy penalty for a verified ~99% single-account blowup event (Jun 2024) that would have been fatal to any real capital allocation.
- −Heavy penalty for chronic reliance on peer signals rather than independent edge, meaning his "alpha" is fundamentally a **lagged, diluted copy** of `@ThetaTard`/`@SirJack` — ingesting his calls directly means ingesting stale, second-hand signal.
- −Penalty for concentration-risk blindness on ideological names and a sunk-cost-driven capitulation pattern (sells near lows, not on a rules-based stop).

**Estimated Expectancy**: On his disclosed tactical swing/scale-out book (excluding the two catastrophic concentration events), the self-reported win rate (~65% on tagged outcomes) and consistent partial-profit-taking behavior suggest a **modestly positive per-trade expectancy, roughly +0.2R to +0.3R** on that subset. However, once the MTPLF capitulation (-55% on a 26%-weighted position, a portfolio-level drawdown of several R) and the 2024 blowup (-99% of account NAV) are folded back in, **blended, capital-weighted expectancy across his full trading life is approximately flat to mildly negative** — a case study in how a single oversized, thesis-anchored position can erase years of otherwise-sound tactical edge.

### 5.2 Signal Flow Ingestion Matrix

```
                  ┌───────────────────────────────────────────────┐
                  │        @TheRealChad Raw Signal Stream          │
                  └───────────────────────┬───────────────────────┘
                                          │
      ┌───────────────────────┬──────────┼──────────────┬────────────────────────┐
      ▼                       ▼                          ▼                        ▼
┌──────────────┐   ┌───────────────────┐    ┌──────────────────────┐   ┌──────────────────────┐
│ Signal 1:    │   │ Signal 2:          │    │ Signal 3:             │   │ Signal 4:             │
│ SCALE-OUT    │   │ ORIGIN TRACE       │    │ CONCENTRATION ALARM   │   │ SENTIMENT/CADENCE     │
│ MECHANICS    │   │ (Copy-Trade Flag)  │    │ (Bagholder Detector)  │   │ (Anxiety Proxy)       │
├──────────────┤   ├───────────────────┤    ├──────────────────────┤   ├──────────────────────┤
│ "sold half/  │   │ Any post citing    │    │ Single ticker >15%   │   │ Post-rate spike       │
│ runner/left  │   │ @ThetaTard/@SirJack│    │ of NAV + "loaded the │   │ (>3x baseline) = his  │
│ 1" language  │   │ = re-route to their│    │ boat"/"see you in..."│   │ own account is likely │
│ Action:      │   │ ORIGINAL post, not │    │ bravado language     │   │ under real drawdown   │
│ MIRROR EXIT  │   │ Chad's lagged copy │    │ Action: CONTRARIAN   │   │ stress               │
│ TIMING ONLY  │   │ Action: DISCARD /  │    │ FADE + hard trim     │   │ Action: RETAIL-HERD   │
│              │   │ TRACE UPSTREAM     │    │ alert                │   │ STRESS BAROMETER      │
│ Weight: +0.55│   │ Weight: -0.60      │    │ Weight: -0.80        │   │ Weight: +0.40 (fade)  │
└──────────────┘   └───────────────────┘    └──────────────────────┘   └──────────────────────┘
```

### 5.3 Execution Directives for the Artemis Engine

**A. Ingestion Directives (genuine edge to harvest)**
1. **Harvest scale-out cadence, not entries.** His partial-profit language ("sold half," "leaving 1 runner," "sold last runner") on non-ideological tickers is a decent proxy for *when a crowded retail momentum trade is losing steam* — useful as a soft trim signal on correlated names, not as a standalone buy trigger.
2. **Use his DD posts as an idea-sourcing net, then re-verify independently.** OKLO (NRC/SMR regulatory) and MTPLF (BTC-treasury mNAV) theses were fundamentally sound and monetizable by disciplined operators — the failure was execution, not idea quality. Ingest the *ticker + catalyst*, discard his *sizing and timing*.
3. **Treat his four-sub-account monthly report cards as a lightweight retail-cohort performance benchmark** (e.g., his Feb 2025 +4%–+38% range vs. SPY -2.39%) for calibrating how much retail alpha exists in a given volatility regime.

**B. Contrarian Fade Directives (when to fade him / the retail herd)**
1. **Fade concentration bravado.** Any post where a single ticker crosses ~20-25% of his disclosed portfolio accompanied by triumphalist language ("see you all in 2030 or in Valhalla," "loaded the boat") should trigger a **local-top/blow-off-top alert on that ticker among the retail cohort** — the pattern preceded his single worst trade by exactly five weeks.
2. **Fade his post-cadence spikes as a crowd-panic proxy.** A 3x+ jump in his (and likely correlated retail traders') post frequency during a drawdown week is a decent tactical marker for **retail capitulation exhaustion nearing completion**, not for continued directional conviction.
3. **Fade, don't follow, his @ThetaTard/@SirJack-sourced entries directly** — by the time he posts, the signal is at minimum one full hop removed from its origin and has already been priced in the underlying's move that prompted his post.

**C. Mandatory Risk Blacklists & Firewalls**
1. **Hard position-size cap firewall**: never let a `COPY_TRADE_SIGNAL_AMPLIFIER`-tagged source's single-ticker conviction call exceed **5% of simulated NAV** in Artemis, regardless of how his own sizing behaves (he ran MTPLF to 26%).
2. **Blacklist "diamond hand"/no-exit-plan language as an entry trigger**: any post using "either prints or I lose everything," "diamond hand," or "see you in [distant year]" framing should be excluded from ingestion entirely — historically a precursor to his largest drawdowns (TSLA 2024, MTPLF 2025).
3. **Blacklist thinly-traded/illiquid narrative micro-caps sourced from this account without independent liquidity/fundamental verification** (MTPLF, KULR, LUNR, ONDS-tier names) — these are where his discipline collapses most completely.
4. **Firewall on sleep-deprived/fatigue-driven trades**: his own post-mortem on the AVGO loss ("Sleep and get enough rest or you take stupid trades") is a useful internal governance reminder for Artemis's own overnight/late-session order flow — a bad late trade required 3 good trades to recover, a poor risk/reward ratio worth avoiding structurally (e.g., no new discretionary-style position entries flagged from this source between 00:00–06:00 local).

**D. Exit Rules & Alpha Rectification**
1. **Enforce systematic, not discretionary, profit-taking** on any position ingested from this source: scale out 33/33/33 at +25%/+75%/+150% rather than relying on his ad hoc "sold half," "left a runner" judgment calls, which work until they don't.
2. **Time-box thematic conviction trades.** Any DD-sourced idea from this account (nuclear SMR, BTC-treasury arbitrage, eVTOL, etc.) gets a hard 90-day thesis-review checkpoint; if the position is down >20% and the checkpoint has passed, force liquidation regardless of narrative conviction — this single rule would have prevented both his 2024 and 2025 catastrophic losses.
3. **Mirror his exhaustion-driven de-risking behavior structurally, not emotionally.** His Feb 2026 move to 40%+ cash (FXAIX/SGOV) after a ~27% drawdown from ATH is a reasonable defensive posture — Artemis should encode an automatic "reduce gross exposure by 40% after any 25% peak-to-trough drawdown" rule rather than waiting for a human-style burnout event to trigger it.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Event | Capital Context |
|---|---|---|
| 2024-05-10 | Opens the archive with an OKLO position built into weakness; first "diamond hand vs. sell" internal conflict | ~$0.86K |
| 2024-05-11 | Full OKLO DD thread (NRC regulatory case, Aurora reactor economics) — genuine, well-sourced fundamental research | ~$35K |
| 2024-05-13 | Trims OKLO "after listening to Sir Jack" — first explicit self-diagnosis of "complacency and risk management" lesson | ~$0 (trim) |
| 2024-06-03 | $DELL lotto put — small speculative side bet | $30.7K |
| 2024-06-11 | **"Tempered trading" post — verified balance spikes to $278.5K** on a trade he chose to trim rather than diamond-hand | $278.5K (verified ATH #1) |
| 2024-06-14 | **TSLA "either prints or I lose everything" YOLO**, deferring to `@neverpullover`'s instincts | $2.28K (**-99.2% in 72h**) |
| 2024-06-15 → 2024-12-04 | **172-day total blackout** — no posts at all | Unknown/rebuilding |
| 2024-12-05 | Returns to the platform, port unlinked | $0.0 (unlinked) |
| 2024-12-13 | Port relinked; UBER position update reveals a rebuilt account | $140.8K |
| 2024-12-17 | UBER DD (Part 1-2), reveals SirJack/ALCC origin of the thesis | $174K |
| 2025-01-25 → 02-28 | **Hot Window** — 191 posts in February alone; tariff/growth-scare volatility drives post-rate to 3x baseline | $130K → $150K range |
| 2025-02-06 | RXRX covered-call income strategy at 50% profit ("Theta working for me") | $134K |
| 2025-02-11 | Opens two "Challenge Accounts" (small speculative side books) | — |
| 2025-02-19 | OKLO Gain post credits "SirJack was ahead of the curve" | $161.8K |
| 2025-02-20 → 02-21 | Peak scale-out week: SPY puts +100%/+230%, CELH yolo call +220%, VXX, ANET puts all closed for gains | $157-161K |
| 2025-02-28 | Self-reported February report card: 4 sub-accounts +4% to +38% vs. SPY -2.39% | $149.9K |
| 2025-03-05/06 | "Full disclosure — I goofed up on $AVGO" (41 comments, most-commented post ever); sleep-deprivation post-mortem | $154-199K |
| 2025-04-09 | "Sold $UBER. Big gains % are taken not given" — core thesis position partially monetized | $154.3K |
| 2025-05-01 | Personal disclosure: parents scammed on meme coins; "826 followers" milestone, SirJack tribute | $44.2K (brief trough) |
| 2025-05-23 | "Port connected again... my emotions are settled" — first mid-cycle emotional withdrawal and return | $166K |
| 2025-05-23 → 09-09 | Builds MTPLF (Metaplanet) position from initial buy to "doubled my position" | $155-182K |
| 2025-10-08 | "$MTPLF loaded the boat" — 15K shares, reduces average further | $202.5K |
| 2025-10-14 | MTPLF hits 26% of portfolio ("making it my largest hold"); BTC-treasury insider shorts reported | $213-218K |
| 2025-10-17 | Bravado peak: "See you all in 2030 or in Valhalla" | $183.2K |
| 2025-11-19 | **MTPLF capitulation at -55% realized loss** — "possibly one of the worst trades of my life" | $163.1K |
| 2026-01-18 | Post-mortem: "DCA down is worse than DCA up" — diagnoses he sold near the local bottom | $214.8K |
| 2026-01-25 → 01-29 | "Sunday Reflection" on VC-style investing; RR position update; sells RR on negative catalyst | $184.6-208.9K (near ATH ~$208K) |
| 2026-02-06 | **"I am officially set back to Feb 2025" — a full year of gains erased** | $149.3K |
| 2026-02-12 | **Voluntary de-risking and permanent port unlink**: exits ACHR, BITF, NFLX, ARSMF fully; buys FXAIX/SGOV; 40%+ cash; announces indefinite hiatus | $155K (final tracked value) |
| 2026-03 → 08 | Sporadic spectator posts only (7 total), no further disclosed positions or capital sync | Unlinked |

---

*Autopsy compiled from `@TheRealChad_all_posts.json` (505-post raw telemetry) and `@TheRealChad_lifetime.md` (narrative archive). `amount_k` interpreted as live brokerage-sync NAV in $ thousands per the subject's own "port linked/unlinked" language; percentages and win/loss counts are self-reported by the subject and carry standard social-media survivorship bias. Certified for Artemis Engine / TraderMatrix ingestion.*
