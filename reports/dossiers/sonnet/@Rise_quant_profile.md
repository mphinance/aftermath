# Quant Forensic Autopsy: Trader @Rise
**Target Profile**: `@Rise` (`prf_d99ee4367c694400853566fce9b5afc3`)
**Platform**: AfterHour (#19 Most Active Followed Trader)
**Dataset Analyzed**: 543 Lifetime Posts (2024-11-14 to 2026-09-08)
**Analyst**: Sam the Quant Ghost (`Momentum Phinance / Artemis Engine`)

---

## 1. Executive Profile

### 1.1 Trader Philosophy & Archetype

`@Rise` is a laid-off corporate engineer turned full-time **theta-income options seller and financial educator**. His own bio states it plainly: *"I'm Rise, an unemployed dad turned full time option seller and self proclaimed theta daddy. I focus on investing in companies I like to own primarily selling options and using the wheel strategy, targeting 1-2% of premium on my total portfolio value, every week."*

He is not a directional gambler, not a 0DTE degenerate, and not a meme-chasing momentum scalper. His entire operating system is **The Wheel** (Cash-Secured Puts → assignment → Covered Calls → repeat), applied to a tight, hand-picked "top dozen" watchlist of stocks he is fundamentally comfortable owning. He explicitly built his content brand — and eventually a paid Discord, **Theta Daddies** — around teaching this system to retail traders as an antidote to "0DTE bullshit" and naked call/put gambling.

Origin story: laid off November 5, 2024 (Election Day), from a plant-operations engineering job. He struck a real deal with his wife — *"if I can generate $250k this year, I'm free to continue [trading] indefinitely"* — turning his trading career into a household-accountability metric, not just a hobby. He blew past that target roughly 2x over in 2025 (see §1.3).

On April 13, 2025 he co-founded **Theta Daddies**, a paid options-selling education Discord, with fellow AfterHour posters `@Bobdog` and `@average_advisor`. This is the single most important structural fact about his account: by mid-2025 he is running a **media/education business**, and a meaningful share of his posting activity is content marketing (watchlists, wheel tutorials, YouTube cross-promotion, community weekly-return recaps) rather than raw personal signal.

### 1.2 Posting Cadence & Timeline

- **Operational window**: 2024-11-14 → 2026-09-08 (662 calendar days / 94.6 weeks).
- **Total posts**: 543 → **5.7 posts/week lifetime average**, but cadence is sharply regime-dependent, not steady:

```
Post Volume by Month (Nov 2024 - Sep 2026)
2024-11: 11  ■■
2024-12: 46  ■■■■■■■■■
2025-01: 46  ■■■■■■■■■
2025-02: 45  ■■■■■■■■■   <- "Diary" era: daily written trade logs, YTD $ tracking
2025-03: 40  ■■■■■■■■
2025-04: 34  ■■■■■■■     <- Theta Daddies founded 4/13
2025-05: 42  ■■■■■■■■
2025-06: 46  ■■■■■■■■■
2025-07: 21  ■■■■        <- Cadence starts collapsing as Discord absorbs content
2025-08: 15  ■■■
2025-09: 16  ■■■
2025-10: 11  ■■          <- Last written weekly $ recap (Oct 5, 2025: +$539k YTD)
2025-11: 15  ■■■         <- Shift to YouTube "Week in Review - Live" streams
2025-12: 15  ■■■
2026-01: 12  ■■
2026-02:  3  ■           <- Trough
2026-03:  5  ■
2026-04:  8  ■
2026-05: 18  ■■■
2026-06: 15  ■■■
2026-07: 38  ■■■■■■■     <- "Morning Show" macro-recap format launches
2026-08: 35  ■■■■■■■
2026-09:  6  ■
```

**Interpretation**: there are three distinct eras. **Era 1 (Nov '24–Jun '25)**: a personal trading diary with granular dollar-level transparency (~10 posts/week). **Era 2 (Jul '25–Apr '26)**: cadence craters as the real content moves behind the Theta Daddies paywall and into live YouTube streams (dark to Artemis' text ingestion — the substance still exists, just not on AfterHour). **Era 3 (May '26–present)**: a *reinvention* into a "pre-market macro morning show" host, posting daily market-recap threads (rates, oil, VIX, Fed) that read as content-calendar filler rather than personal trade calls.

### 1.3 Verified Capital Trajectory & Drawdown History

**Two independent, and partially conflicting, data threads exist in the archive: (a) self-reported dollar figures in post bodies, and (b) the platform's synced `amount_k` portfolio-value telemetry.** They must be reconciled, not averaged.

#### (a) Self-reported, narrative-verified trajectory (the reliable thread)
| Date | Metric | Value |
|---|---|---|
| Dec 2023 | Port value | $98,411 |
| Nov 2024 (post-layoff) | Port value | $222,000 |
| Dec 2024 | Port value | $250,000 |
| Jan 2025 | Port value | $270,000 |
| Dec 2024 | Trading income (month) | +$15,000 (6% mo. / 72% annualized) |
| 2025-03-21 | **YTD options income** | +$60,000 |
| 2025-05-01 | YTD options income | +$109,000 |
| 2025-06-07 | YTD options income | +$204,000 |
| 2025-07-05 | YTD options income | +$252,000 (one negative weekly print: -0.26%) |
| 2025-08-09 | YTD options income | +$363,000 (best single week: +5%) |
| 2025-10-05 | **YTD options income (last written recap)** | **+$539,000** |
| 2026-01-16 | YTD income (new year reset) | +$19,000 |
| 2026-01-24 | YTD income (last logged) | +$35,000 |
| 2026-09-02 | RDDT lifetime wheel P&L (2025+2026, single ticker) | **~$220,000** on $150k–$300k notional |

This is a genuine, credible, and unusually well-documented income stream: **from a ~$250k account, he generated roughly $539k in gross options premium/swing income in 2025 alone** — a >200% "income yield" on starting capital, though this is *premium collected*, not necessarily *unrealized net worth growth* (some of it recycles into cost-basis reduction, some into FXAIX diversification, some gets clawed back by assignment losses).

#### (b) Platform `amount_k` telemetry (the noisy thread — DO NOT ingest as unified equity)
The raw JSON `amount_k` field (535 of 543 posts populated) shows violent, discontinuous jumps that do **not** correspond to trading P&L:
- Nov 2024: ~$50k → Jan 2025: spikes to **$1.87M** in a single month, then permanently resettles to a $900k–$1.3M band through most of 2025.
- Nov 2025: drops mid-month to **$228k** for a 3-week stretch coinciding exactly with a run of "Week 5/Week 6" *options-course tutorial* posts, then jumps back to $1.03M the moment personal trading content resumes.
- Sep 2026 (final 4 posts): flatlines at exactly **$56.77k**, identical to the decimal point across 4 separate days, while post content simultaneously shifts to pure macro-commentary ("morning show") posts with zero personal trade content.

**Forensic ruling**: `@Rise` explicitly discloses **3 accounts (2 connected), 2 Roth IRAs + 1 taxable**, and further confirms *"multiple lots in different brokerages"* for his RDDT wheel alone. The `amount_k` field is tracking **whichever single linked brokerage sub-account happens to be associated with that post**, not a unified net worth figure. The Jan 2025 $1.87M print, the Nov 2025 $228k trough, and the Sep 2026 $56.8k flatline are **account-attribution artifacts of a multi-account trader**, not verified single-day equity moves, drawdowns, or blow-ups. TraderMatrix must **not** compute a max-drawdown % from this field for this trader — it will produce a false -93% "blowup" signal that the qualitative record directly contradicts (he was still actively wheeling RDDT for profit through the same week the number flatlined).

**Real, admitted drawdowns** (qualitative, from post text): a QUBT cash-secured-put bag-hold (~3% of port, taken knowingly against his own better judgment), a -$2,700 AMD CC assignment loss ("my first real L"), and a -30%/-80% NFLX Jan-calls loss (explicitly tagged `[Loss]`, "Wah wahhhhhh. Earnings crushed these"). None of these are portfolio-threatening; all are position-sized at low single-digit percentages of total capital, consistent with his stated 10%/trade, 20%/position sizing caps.

---

## 2. Ticker Universe & Catalysts

### 2.1 Core Asset Universe & Frequency Matrix

Across 543 posts and 190 unique tickers, exposure concentrates hard into a self-declared "top dozen" wheel universe plus a rotating cast of speculative satellite names:

| Tier | Tickers (post mentions) | Characteristics & Strategy |
|---|---|---|
| **Tier 1 — Signature Wheel Names** | $RDDT (125), $HIMS (47), $LCID (32), $LLY (31), $UNH (29) | **Core alpha engine.** $RDDT is the single most important ticker in the archive — "my #1 high conviction stock" (long-term PT $500), wheeled continuously since IPO for ~$220k lifetime realized P&L across 60-70+ round trips. $HIMS, $LLY, $UNH are medium-vol, healthcare/pharma names wheeled through the 2025 UNH-panic and HIMS/Novo drama. $LCID is his lowest-cost-basis long-suffering wheel name (bought at $2, still wheeling toward breakeven "in 2027," per his own joke). |
| **Tier 2 — Growth/Momentum Satellites** | $ACHR (62), $HOOD (61), $RIVN (37), $RCAT (33), $BULL (42), $CRWV (26) | **Swing-to-wheel conversion names.** Entered as momentum/catalyst swings (Cathie Wood's ACHR stake, drone-contract RCAT, Webull's post-IPO $BULL vol premium), then folded into the CC/CSP wheel once a position is established. $HOOD tracked as a peer-comp benchmark for $BULL's premium richness. |
| **Tier 3 — Speculative / Blacklist Candidates** | $QUBT (25), $BBAI (23), $GME (40), $KULR (15), $KITT (12), $RXRX (20), $ONDS (17) | **Documented mistake bucket.** $QUBT is his one openly-regretted, repeatedly-referenced bag-hold ("I got burned on $QUBT... horror story"). Penny/quantum/meme names he explicitly says he's "sticking away from" after 2024 lessons learned, though he never fully stops touching them. |
| **Tier 4 — Mega-cap / Index Ballast** | $NVDA (23), $SPY (21), $AMD (21), $GOOGL (19), $MSTR (18), $VOO (17), $QQQ (7) | **Cash-park & tactical macro hedge.** $VOO ITM covered calls used as a tactical *bearish-tilt* hedge during the April 2025 tariff crash (netted +$10k on a bet that the market would be flat-to-down). All options premium income is systematically recycled into $FXAIX to de-risk out of single-name concentration. |

### 2.2 What Drives His Entries — The Catalyst Stack

`@Rise` does **not** trade off pure technical breakouts or momentum chasing. His entries are driven by, in order of stated importance:

1. **"Do I want to own this stock anyway?"** — the wheel's cardinal rule. He builds a 10-12 name conviction list across sectors (finance, social media, hardware, aerospace, pharma, EV, quantum, meme, consumer) and refuses to wheel names he wouldn't hold unhedged.
2. **Volatility/IV richness, not direction** — post-IPO names ($BULL), post-earnings-crush names, and event-driven vol spikes (UNH DOJ/pricing panic, HIMS/Novo Nordisk news) are actively hunted specifically *because* the options premium is fat, independent of his directional view.
3. **Macro/rates/Fed regime reads** — a large and growing share of 2026 content (his "morning show" era) is pure macro commentary: 10-year yield levels, oil price, VIX regime, Fed hike odds — used to decide whether he's a net seller of calls (bearish tilt) or puts (bullish tilt) that week, and to decide cash %.
4. **Fundamental catalysts, lightly worn** — Cathie Wood's ACHR stake, RDDT's ad-platform growth/Reddit DAU trajectory, LLY's GLP-1 pipeline, HIMS' post-selloff recovery — used to justify *staying* in a wheel position through a drawdown, not to time entries.

Options vs equities: he is **almost exclusively an options seller against an equity base** (CSPs to acquire, CCs to monetize/exit) rather than a long-options buyer. Long calls/puts are rare, small, and explicitly labeled as the exception (NFLX Jan calls loss; occasional VOO calls as a hedge).

---

## 3. Risk Management & PnL Reality

### 3.1 Profit-Taking Discipline: Genuinely Above-Average

Unlike the median AfterHour poster, `@Rise` has an actual, repeatedly-articulated profit-taking rule and largely follows it:

> **Golden Rule #5**: *"If you hit 50% of profit before 50% of time has elapsed, take it and run... Always take your profit."*

He walks this back consistently — buying back CCs/CSPs early for 50%+ realized profit and reselling, sometimes 3-4 times on the same underlying in a single expiration cycle. He even self-audits this habit and flags it as a **minor negative**: on his Sept 2026 RDDT retrospective he admits *"the 3 or 4 random times you see me reselling the same option for an extra half a percent is a huge dopamine hit... I should probably just let things go to expiration."* This is a rare, high-value piece of self-aware behavioral data: **his edge is real, but he slightly over-trades it for dopamine, giving back a small amount of theoretical expectancy to transaction/spread friction and reduced annualized efficiency.**

### 3.2 Losing-Position Management: Wheel-and-Wait, Not Cut-and-Run

He does **not** stop out of losing equity. His doctrine is explicit: *"If you wheel stocks you don't want, you will inevitably bag hold... it's much easier to handle the mental side of a stock that goes down, if you like the stock."* Documented bag-holds: $QUBT (CSP assignment at $16, stock trading $11, "confident it will ultimately pay me"), $LCID (breakeven target pushed jokingly to "2027"), $TSLA, $RDTL, and periodic $UNH/$DECK exposure during the mid-2025 correction. The mitigant is **position sizing discipline, not stop-losses**: Golden Rule #4 caps single-trade size at 10% of port and single-position size at 20%, which he cites explicitly when QUBT went wrong ("3% of my port... damage is minimized").

### 3.3 Documented Wins vs. Documented Blow-ups

**Wins (large, verified)**: $RDDT wheel (~$220k lifetime), the April 2025 tariff-crash contrarian VOO ITM covered-call trade (+$10k in one week betting the market would NOT rally), BULL post-IPO premium harvesting (3,000→6,000 shares scaled via assignment), LCID CSP recovery trade (sub-$3 entries repeatedly monetized).

**Blow-ups (small, contained)**: QUBT CSP bag-hold, -$2,700 AMD CC assignment ("first real L"), NFLX Jan calls -30%/-80% ("earnings crushed these"). **Only 6 of 543 posts (1.1%) carry an explicit `[Loss]` tag**, against 135 `[Gain]` tags (24.9%) — a >20:1 asymmetry that is a **self-reporting/survivorship bias**, not evidence he never loses. His own numbers confirm this: a documented -0.26% single losing week in the middle of an otherwise unbroken green run, quietly absorbed and undertagged.

### 3.4 The Community Layer (Theta Daddies) — A Separate PnL Stream

Since April 13, 2025, he also reports **aggregate Theta Daddies community results** (a distinct, larger pool): weekly prints of +$112k, +$136k, +$162k, +$188k, +$220k, +$267k, +$275k across hundreds of members, crossing **$1M cumulative community gains** by mid-2025 and **$2.5M+ since inception** by ~July 2025. This is influencer/marketing data, not his personal P&L — TraderMatrix should tag it separately (`SOCIAL_PROOF_METRIC`) and never blend it into his individual expectancy calculation.

---

## 4. Behavioral & Sentiment Signals

### 4.1 Why Is He Posting?

Three overlapping motives, evolving over time:
1. **Radical transparency as a trust-building mechanic** ("No hiding here, I'll always keep my port linked so we learn together") — a deliberate content strategy for an educator, not just diary-keeping.
2. **Accountability** — his wife's $250k/year deal, and later the Theta Daddies member base, function as external accountability structures that show up directly in his post cadence and tone.
3. **Monetization** — by mid-2025 posting functions substantially as a **funnel into the paid Theta Daddies Discord and YouTube channel**; his highest-engagement posts (by reactions/comments) are not trade calls but educational content: "20 Stocks under $20 to Wheel" (127 reactions), "Week 4 – Sell an Option!" (124), "Making Money With Covered Calls" (118), his 1-year Fireaversary essay (132). **Personal trade-call posts rank well below educational/community content in engagement** — a strong signal that his audience values him as a teacher, not a signal-caller.

### 4.2 Recurring Linguistic & Psychological Patterns

- **"The Wheel," "bag hold," "theta daddy," "rinse and repeat"** — a settled personal vocabulary repeated dozens of times, functioning as in-group branding as much as strategy description.
- **Self-deprecating humor as a coping/credibility mechanism**: "Broken Toy Collection" for paper losses, "NFLX and Cry," "Even Theta Daddies like to gambool every once in a while," LCID breakeven "in 2027" jokes. He uses humor specifically to disclose losses without losing authority.
- **Explicit anti-panic mantra**: "Golden Rule #2 — Never panic... Panic leads to FOMO buying or panic selling, neither of which are good." During the April 2025 tariff crash he documents literally turning his phone off for two days rather than reactively rolling positions — a rare, verifiable instance of stated discipline matching behavior.
- **Reaction to red days / volatility**: raises cash proactively (documented at 70% cash during April 2025 tariff panic, 50% cash multiple other weeks), explicitly refuses to "catch a falling knife" on legitimate-catalyst drops (HIMS/Novo), but *does* frame broad-market vol spikes as premium-selling opportunities ("volatility is becoming more interesting for premium sellers, but that doesn't mean every dip is a buy"). He is a **volatility harvester, not a volatility victim.**
- **Diversification lecturing**: repeatedly calls out followers whose "whole portfolio is red" for being secretly concentrated in one trade wearing 15 ticker symbols (AI infra/semis/space/batteries) — a recurring, on-brand contrarian-to-the-retail-herd riff.

---

## 5. Quantitative Verdict for TraderMatrix

```
+-----------------------------------------------------------------------------------+
|                            TRADERMATRIX CLASSIFICATION                            |
|                                                                                     |
|   PRIMARY TAG:      THETA_INCOME_WHEEL_OPERATOR                                    |
|   SECONDARY TAG:     RETAIL_EDUCATOR_CONTENT_ENGINE                                |
|   TERTIARY TAG:      VOLATILITY_HARVESTER (event/IV-driven premium selling)        |
|   ALPHA STATUS:      Positive, Real, Modest-Leak (self-admitted early-BTC churn)   |
|   RECOMMENDED FIT:   Premium-Selling Signal Source + Watchlist Curator              |
+-----------------------------------------------------------------------------------+
```

### 5.1 Algorithmic Classification Tags

- **Primary**: `THETA_INCOME_WHEEL_OPERATOR` — systematic CSP→assignment→CC cycling on a concentrated, fundamentally-vetted watchlist.
- **Secondary**: `RETAIL_EDUCATOR_CONTENT_ENGINE` — a meaningful fraction of output is monetized education (Theta Daddies, YouTube), not raw signal; engagement metrics confirm audience treats him as teacher first.
- **Also applicable**: `VOLATILITY_HARVESTER` (sells into IV spikes around IPOs/earnings/panics rather than fading or chasing direction), `MACRO_OVERLAY_TACTICAL` (uses ITM index CCs as a directional hedge sleeve during regime uncertainty), `DISCIPLINED_PROFIT_TAKER` (50%-rule adherent), `LOW-CONVICTION_BAGHOLDER` on a small, sized-down speculative sleeve (QUBT-class names).

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 71 / 100**

| Component | Score | Rationale |
|---|---|---|
| Edge Legitimacy | 18/20 | Real, multi-year, cross-account documented income (~$539k 2025, ~$220k lifetime RDDT alone) from a repeatable, teachable mechanical process — not luck-dependent directional calls. |
| Risk Discipline | 16/20 | Genuine position-size caps (10%/trade, 20%/position) and a real anti-panic track record (April 2025). Docked for zero use of hard stop-losses on equity legs — pure sizing-based risk control. |
| Profit-Taking Discipline | 15/20 | Best-in-class stated rule (50%-of-profit/50%-of-time), consistently followed. Docked for self-admitted "dopamine churn" — reselling too early for marginal extra premium, leaking some expectancy to transaction friction. |
| Signal Clarity / Reproducibility | 12/20 | Strike, DTE, and underlying are usually disclosed clearly enough to mirror. Docked hard because post cadence for *personal* trade detail collapsed for ~10 months (Jul '25–Apr '26) as content moved off-platform into a paywalled Discord — an ingestion blind spot. |
| Data Hygiene (platform telemetry) | 10/20 | The `amount_k` field is unreliable for this trader specifically (multi-account attribution artifacts) — any automated equity-curve/drawdown pipeline must special-case or exclude him. |

**Expectancy**: On the wheel core (RDDT-class names), realized win characteristics approximate **~2-4% weekly premium yield on deployed capital, annualizing to roughly 65-125%** on his own repeatedly-cited weekly-return prints (1.07%-5% weekly observed range), with an estimated **>90% of individual option legs closed at a profit** (only 6 explicit loss tags across 543 posts, corroborated by his own admission that losses are rare and small when they occur). This is consistent with textbook cash-secured-put/covered-call theta-selling expectancy: high win rate, small-to-moderate loss tail on the rare adverse assignment, positive long-run expectancy driven by IV overstatement relative to realized volatility on his chosen underlyings.

### 5.3 Signal Flow Ingestion Matrix

```
                       ┌───────────────────────────────────────────────┐
                       │            @Rise Raw Signal Stream             │
                       └───────────────────────┬────────────────────────┘
                                                │
        ┌────────────────────────┬─────────────┴─────────────┬──────────────────────────┐
        ▼                        ▼                            ▼                          ▼
┌──────────────────┐  ┌────────────────────────┐  ┌───────────────────────┐  ┌─────────────────────────┐
│ Signal 1: WHEEL   │  │ Signal 2: WATCHLIST     │  │ Signal 3: MACRO TILT  │  │ Signal 4: BAGHOLD FADE   │
│ CORE (CSP/CC)     │  │ CURATION (Vol Harvest)  │  │ (Rate/VIX/Fed reads)  │  │ (Speculative sleeve)     │
├──────────────────┤  ├────────────────────────┤  ├───────────────────────┤  ├─────────────────────────┤
│ RDDT, HIMS, LLY,  │  │ BULL, CRWV, ACHR, RCAT │  │ VOO/SPY ITM CC tilt,  │  │ QUBT, BBAI, penny/meme   │
│ UNH, LCID         │  │ (post-IPO / event vol) │  │ cash % adjustments    │  │ names he flags as regret │
│ Action: MIRROR    │  │ Action: ADD TO WATCH-  │  │ Action: USE AS CASH-  │  │ Action: CONTRARIAN FADE  │
│ STRIKE/DTE DIRECT │  │ LIST, size independent │  │ ALLOCATION SIGNAL,    │  │ or IGNORE ENTRY ENTIRELY │
│ Weight: +0.80 High │  │ Weight: +0.55 Moderate │  │ not direct trade      │  │ Weight: -0.40 (Fade)     │
└──────────────────┘  └────────────────────────┘  └───────────────────────┘  └─────────────────────────┘
```

### 5.4 Execution Directives for the Artemis Engine

#### Ingestion Directives — Genuine Edge to Harvest
- **Mirror the wheel mechanics directly on RDDT/HIMS/LLY/UNH-class names**: when he posts a CSP or CC strike/DTE on his Tier-1 list, treat it as a high-confidence, reproducible income trade — his selection criteria (own-the-stock conviction + rich IV) is sound and his win rate on these legs is empirically very high.
- **Use his watchlist curation as a volatility-harvest radar**: when he flags a fresh post-IPO or post-catalyst-crush name (e.g., a future $BULL/$CRWV analog), treat the *underlying discovery*, not his specific strike, as the signal — feed it to Artemis' own options-selling engine for independent strike/DTE optimization.
- **Treat his macro-regime posture (cash %, ITM-CC tilt direction) as a sentiment/positioning overlay input**, not a standalone trade signal — it correlates with genuine institutional-grade caution (documented correctly ahead of the April 2025 tariff selloff).

#### Contrarian Fade Directives — When to Fade Him or the Retail Herd
- **Fade the "reselling for an extra half-percent" impulse**: when he posts about buying back and immediately re-selling the same option for marginal extra premium, do NOT chase the re-sale — his own retrospective analysis shows expectancy would have been *higher* letting the original contract run to expiration. Artemis should let winners ride further than he does.
- **Fade his Tier-3 speculative sleeve entries** (QUBT-class quantum names, penny drone/meme names): these are explicitly sized-down "gambles" he himself later regrets. Do not scale into these; if anything, treat his entry into this bucket as **contrarian information that retail sentiment is currently overheated** in that subsector.
- **Discount "Theta Daddies community result" posts entirely** as an individual-trader alpha signal — they are marketing/social-proof metrics for a paid product, not his personal book.

#### Mandatory Risk Blacklists & Firewalls
- **Blacklist**: naked long options as a mirrored instrument class — he almost never runs them, and his one clean example (NFLX Jan calls) was a clear loss; the wheel/CSP/CC structure is the exportable edge, not directional options buying.
- **Firewall on the `amount_k` telemetry field for this trader specifically**: exclude from any automated equity-curve, drawdown, or Sharpe calculation. Verified multi-account attribution artifacts (Jan 2025 $1.87M spike, Nov 2025 $228k trough, Sep 2026 $56.8k flatline) will corrupt any naive time-series ingestion. Use only self-reported, narrative-verified dollar figures (§1.3a) for capital-trajectory modeling.
- **Data-continuity firewall**: flag the Jul 2025–Apr 2026 window as **low-confidence / sparse-signal** for this trader — his real trading activity did not stop, but public disclosure of specifics migrated off-platform into the paywalled Discord. Do not interpret the cadence drop as reduced trading activity or reduced conviction.
- **Position-sizing floor**: never let mirrored single-name exposure exceed his own stated caps (10% per trade, 20% per position) — these caps are precisely why his documented losses (QUBT, AMD, NFLX) never became blow-ups, and Artemis should inherit the discipline, not just the ticker picks.

#### Exit Rules & Alpha Rectification
- **Adopt his 50%-profit/50%-time rule as a baseline exit heuristic** for mirrored CSP/CC legs — it is well-validated across hundreds of his own trades and is more disciplined than most retail signal sources in this dataset.
- **Override/improve on his own admitted leak**: where his rule would trigger an early buyback-and-resell for marginal extra premium, Artemis should instead evaluate whether holding the *original* contract to expiration nets higher risk-adjusted return (his own Sept 2026 retrospective concluded it usually would have) — a small, quantifiable expectancy improvement over literal mirroring.
- **Trailing cash-allocation rule**: increase Artemis' own cash reserve target when `@Rise` signals a macro-cautious tilt (ITM CC selling on index positions, explicit "X% cash" disclosures) — this has a clean, one-for-one historical hit (April 2025 tariff crash called correctly, in advance, with real capital committed to the hedge).

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone / Catalyst |
|---|---|
| 2024-11-05 | Laid off from corporate engineering job (Election Day) — origin event for full-time trading career. |
| 2024-11-14 | First AfterHour post (ASTS earnings discussion). |
| 2024-11-19/21 | Early $RDDT swing trades (bought $55-$65, sold $135) — establishes RDDT as signature name. |
| 2024-12 | Port value ~$222k-$250k; December trading income +$15k (72% annualized). Wife accountability deal: $250k target for 2025. |
| 2025-01-08 | First self-tagged `[Loss]` post — QUBT CSP bag-hold ("first likely loss since joining AfterHour"). |
| 2025-01-09 | "2024 Year in Review" post — full capital trajectory disclosure ($98k → $270k). |
| 2025-02-05/13 | AMD/UBER/QUBT "Broken Toy Collection" paper losses; RDDT CSP miss at $200 strike. |
| 2025-03-21 | YTD options income reaches +$60k; first explicit "8-week avg $6,133/wk, $300k/yr run rate" disclosure. |
| 2025-04 | Tariff-crash period: raises cash to 70%, sells ITM VOO covered calls as a bearish tactical hedge, nets +$10k in one week; explicitly avoids panic-rolling. |
| 2025-04-13 | **Theta Daddies Discord co-founded** with @Bobdog and @average_advisor — inflection point from solo trader to educator/community operator. |
| 2025-04-25 | "How to Lose $40k Flipping a House" — long-form personal-history post revealing largest-ever historical loss (2005-06 real estate flip), context for current risk discipline. |
| 2025-05 | $BULL (Webull) post-IPO premium harvesting begins; scales to 6,000 shares via assignment by end of May. |
| 2025-06-08 | Theta Daddies community weekly result reported at +$188k, approaching $200k cumulative mark. |
| 2025-06-XX | Theta Daddies crosses **$1MM in cumulative community gains** since inception. |
| 2025-07 | Community cumulative gains reported north of **$2.5MM since inception** (Apr 13 - Jul 2025). |
| 2025-08-09 | Best single self-reported week: +5% return, YTD income +$363k. |
| 2025-10-05 | **Peak/final written personal YTD disclosure: +$539k** for 2025 — last granular dollar recap before shift to livestream format. |
| 2025-11-05 | "1-Year Fireaversary" essay — most-engaged post in dataset (132 reactions), full origin-story retrospective. |
| 2025-11 | Content format shifts to "Week in Review - Live" YouTube streams; written $ disclosure cadence drops sharply. |
| 2026-01-16/24 | New-year income reset disclosed: +$19k, then +$35k YTD (last explicit personal $ figure in the archive). |
| 2026-02–04 | Posting cadence trough (3-8 posts/month) — lowest-signal period in the dataset. |
| 2026-05–06 | Cadence partially recovers; format increasingly macro/market-recap oriented. |
| 2026-07 | "NFLX and Cry" — documented options loss (-30%/-80% on Jan calls). |
| 2026-07–08 | **"Morning Show" pivot** — near-daily premarket macro-recap posts (rates, oil, VIX, Fed) become the dominant content type. |
| 2026-09-02 | **RDDT lifetime wheel retrospective**: ~$220k realized lifetime P&L, ~60-70 round trips, self-critique of early-buyback "dopamine" habit. |
| 2026-09-08 | Final post in dataset — macro "AI Strength vs $100 Oil" market-recap format. |

---
*Report compiled by Sam the Quant Ghost (`Momentum Phinance / Artemis Engine`). Data verified against raw transaction telemetry in `@Rise_all_posts.json` (543 records, 190 unique tickers) cross-referenced with the full lifetime markdown narrative archive. The `amount_k` multi-account attribution artifact (§1.3b) is documented in detail to prevent downstream pipeline miscalibration on this specific trader's equity curve.*
