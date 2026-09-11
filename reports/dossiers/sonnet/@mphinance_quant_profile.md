# Quant Forensic Dossier: @mphinance

**Subject:** AfterHour trader `@mphinance` (Profile ID `prf_1d3e45fbdb93461eb593f842fccdc990`)
**Rank:** #11 most-active followed trader by lifetime post count
**Sample size:** 1,174 lifetime posts, 2024-12-19 → 2026-08-05 (593 days / 84.7 weeks); **35 days silent as of report date**
**Sources:** `@mphinance_lifetime.md` (formatted archive), `@mphinance_all_posts.json` (raw, incl. `amount_k` portfolio snapshots, tags, engagement counters), cross-tabulated programmatically (ticker extraction, cadence, tag distribution, keyword frequency, engagement trend, capital-trajectory reconstruction)
**Analyst:** Artemis Forensic Desk · 2026-09-10

> **Headline finding:** @mphinance is a former institutional-finance/accounting professional turned professional retail options income trader turned **fintech founder** — his lifetime post history is, in effect, the origin log of a real trading-tools business (Substack "Momentum Phinance," an LLC, custom screeners, TradingView indicators, a "TraderDaddy"/"Sam" bot product line, and — in his final active month — a public tool that scrapes AfterHour's own undocumented API to run AI-generated behavioral dossiers on 25 named traders, **himself included**). This is the same category of artifact this report is. His tracked `amount_k` field is **not one account**: the raw series is cleanly bimodal — 600 readings cluster under $200K, 464 cluster between $203K and $1.66M, switching abruptly and repeatedly with zero narrative acknowledgment of a 20-40x swing. Cross-referenced against his own posts, this reflects at least three real, distinct capital pools sharing one sync field: (1) his own small, actively-narrated options-wheel account ($1K–$50K), (2) his **father's ~$750K–$1M+ retirement rollover**, which he manages and posts about, and (3) volatile prop "funded challenge" trading accounts he explicitly describes killing "in one afternoon." **Any drawdown or return computed from the raw `amount_k` series without this decomposition is not a measurement of this trader's risk-taking — it is a measurement of his father's asset allocation.** Layered on top of the financial forensics is a second, load-bearing thread: this is an openly recovering alcoholic/addict and felon (DUI) who lost his corporate job over the conviction, now builds his identity and his highest-engagement content around recovery, mentorship, and radical transparency — traits that directly shape a trading style built on small, mechanical, income-generating repetition rather than the boom/bust momentum chasing typical of this cohort.

---

## 1. Executive Profile

### Philosophy
@mphinance presents, and largely behaves, as a **disciplined, mechanically-minded options-income trader with a wide, low-conviction speculative satellite book**, not a momentum gambler. His own framing of the strategy, from his one-year AMA:

> *"The philosophy is simple: control what you can (risk, entry, exit) and let go of what you can't (Mr. Market & everything else)."* (2025-10-28)

> *"The secret? The same damn thing that got me through my worst: showing up and cutting the losers instantly. I lose trades all the f*cking time, but my reaction to losing — to admitting when I'm wrong — makes all the difference."* (2025-10-28)

The account opens (Post #1, 2024-12-19) not with a trade but with him launching a small, real-money ($800, rising to $2,000) Fidelity basket replicating another trader's ("@squeezekid") "AfterHour Naughty List" — a 30-stock speculative basket he tracks and reports on for months. From there the throughline is **the wheel** (cash-secured puts → assignment → covered calls → repeat) as the income engine, run simultaneously across small-cap, mega-cap, and high-yield ETF ("YieldMax": $ULTY, $MSTY) underlyings, financed by relentless, granular position-sizing (buying 5, 19, 34, 100 shares at a time) rather than one-shot leverage. Around it he runs a much wider, low-size speculative satellite book (867 unique tickers touched across the sample) that functions more as public research/content than as core PnL.

By late 2025 the account's second identity takes over: **professional trading as a second act after a corporate career ended by a felony conviction.**

> *"Turns out, a white-collar felon with institutional experience is an enigma: overqualified for the skillset, yet instantly disqualified due to the sensitivity of the data I used to process... so I built my own path."* (2025-10-28)

> *"I am a high net worth felon with a background in institutional finance. I cannot fly under the radar. I have to be squeaky clean... That is why I just registered Momentum Phinance LLC."* (2025-11-27)

By early 2026 the account's third identity emerges: **fintech builder.** He ships custom TradingView indicators, Streamlit apps, an options screener, a "TraderDaddy"/"Sam" AI trading-assistant bot, weekly signal reports, and — in his last active week on the platform (Aug 2026) — publishes the undocumented AfterHour API endpoint publicly and runs it against 25 named traders (himself included) through a "no manners, then a second model told to distrust the first draft" AI pipeline, publishing the result at `mphinance.com/ah/`. **This is directly relevant to Artemis: the subject has independently built a competing version of this exact analysis, and has publicly demonstrated the platform's lack of API authentication — a fact Artemis's own ingestion pipeline should treat as an operational note, not merely trivia.**

### Post Cadence
| Metric | Value |
|---|---|
| Total posts | 1,174 |
| Active date range | 2024-12-19 → 2026-08-05 (593 days / 84.7 weeks) |
| **Average lifetime cadence** | **13.9 posts/week** (≈ 2.0/day) — roughly half of the more content-driven accounts in this cohort |
| Peak cadence | Jan 2026: 136 posts/month (≈31.7/wk); Aug 2025: 136; Dec 2025: 118 — a sustained ~120-post/month plateau from Aug 2025 through Jan 2026 |
| **Cadence collapse** | Feb 2026: **1 post**. Mar–May 2026 stabilizes at a much lower 19–25 posts/month. Jun–Jul 2026: **0 posts**. Aug 2026: 3 posts, last on Aug 5. |
| Days silent as of report date | **35** (last post 2026-08-05; report date 2026-09-10) |
| Posting-hour distribution (UTC) | Bimodal: 12:00–15:00 UTC (US premarket/open) and 00:00–03:00 UTC (evening/late-night US) are the two clear peaks — consistent with a full-time trader posting around the open and writing long-form at night |
| Day-of-week | Fairly even (Fri highest at 220, Mon lowest of weekdays at 135); weekends (Sat 133, Sun 143) are *not* meaningfully quieter than weekdays — atypical for a "day job" trader, consistent with his self-described full-time/no-9-to-5 status from Dec 2024 onward |

The Feb-2026 cliff is not organic fatigue — it is **dated to a specific, explicit platform-trust rupture** (§6), and the subsequent silence coincides with a deliberate migration of "serious" content to a paid Substack ("Momentum Phinance") and a trading-tools product line, with AfterHour relegated to "short-form thoughts, vibes, and quick interactions" that, in practice, mostly stopped happening.

### Verified Capital Trajectory (platform-tracked `amount_k`, total account value)
*Methodological note: `amount_k` is a total-account-value snapshot stamped on every post. For this subject it is demonstrably **not a single account**. The raw series (1,064 non-zero readings) splits cleanly into two clusters — 600 readings under $200K, 464 between $203K and $1.66M — that switch back and forth within a single day, repeatedly, over 14 months, with zero acknowledgment anywhere in the text of a corresponding 20–40x trading gain or loss. He explicitly discusses managing (a) his own personal options account, (b) his **father's** ~$750K→$1M+ retirement rollover ("ANOTHER MILLIONAIRE JOINS THE RANKS," 2025-08-16 — describing his father's three consolidated $250K retirement pots, now under Michael's management), and (c) short-lived prop "funded" accounts he "killed... in one afternoon." **Treat the low band (<$200K) as the reliable proxy for the subject's own, personally-narrated trading risk. Treat the high band (≥$200K) as unattributed — most likely his father's account or a funded-account balance, not the subject's own capital at risk — and never compute a "drawdown" across the combined series.***

| Date | Event | Tracked value | Note |
|---|---|---|---|
| 2024-12-19 | First post (AH Naughty List basket) | $0 (basket funded outside platform at $800, real cash) | Starting point; first `amount_k` reading (Dec 21) is $118.11K |
| 2025-05-21 | "THE MILLIONAIRE HATTRICK" | $620.32K, sandwiched between $150.11K readings minutes apart | High-band excursion; unremarked in text as a real gain |
| 2025-06-04 | Real, narrated collapse | $147.24K (Jun 2) → **$2.23K** (Jun 4) | **Genuine, personal-account drawdown of ~-98% in 2 days**, in his own low band; no single named cause in-text, but immediately followed by the account's most personal post (§4) five days later |
| Jun–Sep 2025 | Low-band rebuild | $2K → $22K → $38–45K by end of Sep | Real, gradual, wheel-driven recovery — matches his own account of small-cap scalping/funded-account activity this period |
| 2025-06-21 to 06-26 | High-band excursion #2 | $833K, sustained 5 days, then reverts to $22K on 06-27 | Same signature as the TRON "Port Jesus" glitch pattern, but sustained multi-day — consistent with a distinct linked account rather than a momentary sync bug |
| 2025-08-16 | "ANOTHER MILLIONAIRE JOINS THE RANKS" | $585K | **Confirmed to be describing his father's retirement account**, not his own — explicit textual confirmation of a second real capital pool under this handle |
| 2025-09-19 → 2026-01-07 | Sustained high-band plateau | $900K → **peak $1,656.76K** (2025-12-20, "MY 1 YEAR ANNIVERSARY") → $1,638K (2026-01-07) | Longest sustained high-band stretch; coincides with LLC formation ("BROKERS FOR LLCs," 11-29) and Substack fund launch ("QUIT MY JOB TO TRADE," 11-27) |
| 2026-01-09 | Sudden high→low collapse | $1,638K (Jan 7) → **$80.58K** (Jan 9) | Same-day as "CONTENT WARNING: FEELINGS AHEAD" — a real personal-crisis post (loss of a loved one, a dependent's health crisis, and unspecified "paperwork... finality"). **Do not read this as a trading loss; the coincident text is about a life event, not a position.** |
| 2026-01-21 → 01-29 | High-band re-appears, oscillates | $1,107K → $995K → $983K → $1,006K (`$ONDS` re-enters heavily here) | Volatile but internally consistent multi-day plateau, not a single-day spike |
| **2026-02-04** | **"THE HOUSE THAT JACK BUILT"** — platform-trust departure post | **$50.89K** | Low band resumes and **never returns to the high band again** through the end of the sample |
| Feb–May 2026 | Low-band stabilization | $44–50K, tight range | The most credible, single-account-consistent stretch in the whole series — small, real, wheel-income trading (`$BTG`, `$OUST`, `$HOOD`, `$GOOGL` LEAPS), fully congruent with his granular, transaction-level "I made $591 wheeling a $5 stock" accounting |
| 2026-08-02 → 08-05 | Final posts before silence | $40.11K → $41.22K | Stable, low-band, real; last tracked value of the sample |

**Verdict on "returns": do not report a single lifetime return or drawdown number for this subject.** The only defensible read is: **his own, personally-managed trading capital moved from a ~$118–158K starting range (Dec 2024–May 2025) through a real, catastrophic ~-98% drawdown in June 2025 ($147K→$2K), rebuilt to a $40–50K plateau by late 2025, and has remained flat in that $40–50K band through the last tracked post (Aug 2026)** — i.e., his real, own-money trading capital is still roughly **-65% to -70% below its original 2024–2025 baseline** eighteen months later, even though the LLC/father's-account/funded-account excursions visible in the same feed reach into seven figures. The two stories are opposite in sign and must never be blended.

---

## 2. Ticker Universe & Catalysts

### Core universe (by raw `$TICKER` mention count, full history; 867 unique tickers touched)
| Ticker | Mentions | Role |
|---|---|---|
| $BULL (Webull) | 82 | Brokerage-as-ticker; both a trading platform reference and a traded stock; heavy weekly-options CSP underlying |
| $NVDA | 81 | Mega-cap AI proxy — earnings plays, LEAPS, macro-breadth commentary |
| $GLXY (Galaxy Digital) | 81 | Core crypto-proxy conviction name; recurring TA/Elliott-wave/fundamental deep dives |
| $HIMS | 73 | Small/mid-cap momentum + wheel underlying, repeat "buying the dip" name |
| $HOOD | 63 | Retail-sentiment proxy + wheel/LEAPS underlying |
| $ULTY (YieldMax Ultra Income ETF) | 63 | Core high-yield income vehicle; recurring NAV-erosion analysis and "beat ULTY" wheel comparisons |
| $AVGO | 53 | Mega-cap AI/semis long, notably the position that helped push his father's rollover past $1M |
| $ONDS | 49 | Speculative drone/defense name — present but a *minor* position relative to peers in this cohort (cf. `@TRON`'s 335 mentions); explicitly traded tactically ("DON'T TELL TRON WHAT I DID WITH $ONDS" — scalping LEAPS rather than diamond-handing) |
| $SPY | 43 | Index-level hedging/benchmarking reference, not a primary trading vehicle |
| $MSTR / $BTC / $COIN / $IBIT | 40 / 40 / 36 / 19 | Crypto-proxy cluster; includes a documented bad-timing sale of cold-storage BTC to fund $MSTY income (§3) |
| $TSLA, $NIO, $RDDT, $PLTR, $RXRX, $OKLO, $RKLB, $UBER, $ASTS, $AMD | 20–38 each | The AH-Naughty-List-era speculative/momentum tail — largely inherited from the community basket, not independently sourced conviction |
| $MSTY (YieldMax MSTR Income ETF) | 24 | Secondary income vehicle; also the subject of a self-described "mistake" (selling BTC to buy it near a local top) |
| $GLD / $GDX | 21 / 19 | Explicit macro hedge / uncorrelated-return sleeve — a genuinely distinct behavior vs. peers, including a live "trailing stop formula" experiment on GLD (§6) |

### Options vs. equities
- **300 of 1,174 posts (25.6%) contain explicit options language**; **290 posts (24.7%) specifically reference the wheel, CSPs, or covered calls** — this is not a side activity, it is the account's dominant, load-bearing strategy.
- **LEAPS: 63 posts (5.4%)** — used for core long convictions ($GOOGL, $NVDA), not for degen upside.
- **0DTE: only 14 posts (1.2%)** — explicitly *not* an index-scalping account, a meaningful contrast with several peers in this cohort who pivoted into 0DTE post-drawdown.
- **Yolo-tagged: 65 posts (5.5%)** — self-labeled speculative plays, kept to a stated minority by design ("the YOLOs are few").

### What drives entries — ranked by frequency
1. **Premium/theta harvesting mechanics** — strike/delta selection, IV rank, assignment management, weekly income targets. This is the single largest driver of post volume and the actual PnL engine.
2. **Community-basket inheritance** — the "AfterHour Naughty List," a 30-name speculative basket he did not originate but adopted and tracked publicly for most of a year; explains the enormous 867-ticker long tail and the 86 posts containing >10 tickers at once.
3. **Macro/rate/crypto-cycle commentary** — Fed policy, treasury yields, BTC/crypto-ETF flows, gold — used to frame both the income book (which underlyings to wheel) and the growth sleeve (mega-cap AI, $AVGO, $NVDA).
4. **Tooling/automation as a trading signal source** — custom TradingView indicators, Streamlit screeners, and (from 2026) an actual product ("TraderDaddy," "Sam"/"TraderLady" bot, TickerTrace) built to generate his own entries; a distinctive, additive edge no other subject in this cohort has demonstrated.
5. **Earnings reactions** — real but secondary, mostly used to time covered-call strikes around known volatility events, not as a standalone catalyst play.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags?
**Mostly, he takes profits — mechanically, on a schedule, by construction of the strategy itself.** The wheel structurally forces profit-taking (calls assigned away, puts assigned into shares he wanted anyway) and he documents this discipline in granular, auditable detail:

> *"May 11: BTG was above $5. Two of my calls got assigned. 200 shares called away at $5.00... The wheel doing exactly what it is supposed to do. I let them go, no FOMO."* (2026-05-17)

This is the single most reproducible, mechanical edge in the entire dossier: **a documented, multi-month, transaction-by-transaction wheel log on a sub-$5 stock producing $591.22 of realized income on ~$6,590 of capital deployed**, with explicit share counts, strikes, and dates. It is real, auditable, and repeatable — the opposite of the vague conviction-language that dominates most of this cohort's "wins."

Where he does *not* take profits cleanly: the wide speculative satellite book (the inherited 30-stock basket, the LEAPS/YOLO tail) is held with far less discipline and is not marked-to-market anywhere near as carefully as the wheel positions.

### Documented wins vs. blow-ups
- **13 self-tagged `[Loss]` posts vs. 61 `[Gain]` posts (≈4.7:1)** — a far more balanced, credible self-tagging ratio than this cohort's norm (cf. `@TRON`'s 101:1), consistent with his stated philosophy of "showing up and cutting the losers instantly" and naming them publicly.
- **The one real, catastrophic, own-money blow-up is the June 2025 collapse**: $147.24K → $2.23K in 48 hours (low band, personally narrated). No single post names the cause directly, but it lands five days before his most vulnerable public post to date (the sobriety-anniversary confession, §4) and coincides with his own later description of a funded-account "rocket ship" period that he "killed... in one afternoon."
- **A second, real but much smaller documented mistake**: selling BTC out of cold storage to fund $MSTY income in a liquidity crunch — "I sold the hardest asset right before it climbed and bought a yield trap right before it slid" — explicitly labeled "silly" and analyzed with the tax and opportunity-cost consequences laid out in full (2025-11-27).
- **Documented tax-loss harvesting sophistication**: "HOW TO PROPERLY DO $BULL-SH1T LOSS HARVESTING, WASH SALES RULES, PORTFOLIO CONDOMS" (2025-11-20) — losses here are treated as a planning input, not a trauma to hide.

### How does he manage losing positions?
The wheel structure itself is the risk-management system: a losing equity position simply becomes covered-call collateral, and premium collected reduces cost basis every cycle rather than requiring a discretionary "cut" decision. Outside the wheel, his stated rule — cut fast, admit the error publicly, move on — is corroborated by the tag data (real Loss-tagged posts spread across the whole timeline, not clustered/hidden) and by direct quotes ("Not regretting getting out for sure," re: a failed $COIN short, 2025-06-21).

---

## 4. Behavioral & Sentiment Signals

### Why is he posting?
The tag distribution shows a genuinely different profile from most peers in this cohort:

| Tag | Count | Share |
|---|---|---|
| (untagged / plain commentary) | 591 | 50.3% |
| `Chart` | 142 | 12.1% |
| `Discuss` | 130 | 11.1% |
| `Funny` | 76 | 6.5% |
| `Yolo` | 65 | 5.5% |
| `Gain` | 61 | 5.2% |
| `News` | 58 | 4.9% |
| `Dd` | 26 | 2.2% |
| `Loss` | 13 | 1.1% |
| `Poll`, `Contest` | 12 combined | 1.0% |

This is a **teaching/analysis-weighted account** (Chart + Discuss + Dd = 25.4% of tagged volume, well above the community-humor share). But the engagement data tells a sharper story: his **eight most-reacted and most-commented posts are almost entirely personal, not trade-related.**

| Post | Reactions | Comments | Content |
|---|---|---|---|
| "MY NAME IS MICHAEL AND I AM AN ALCOHOLIC, ADDICT, TRADER, FELON..." | 141 | 121 | 1-year sobriety anniversary; addiction/incarceration disclosure |
| "THE HOUSE THAT JACK BUILT" | 92 | 133 | Platform-trust departure/farewell post |
| "I SEE FIELDS OF GREEN" | 103 | 96 | A Green Bay Packers selfie — zero trading content |
| "CONTENT WARNING: FEELINGS AHEAD" | 95 | 58 | Personal-crisis post, written entirely in trading metaphor |
| "QUIT MY JOB TO TRADE... HERE'S WHAT I BROKE." | 77 | 102 | Career/felony/LLC-launch narrative |
| "I LOVE YOU, PAT :'(" | 75 | 40 | Tribute to a recovery-community mentor who died |

**His audience engages with him as a person and recovery figure first, and as a trader a close second.** This is the account's most important behavioral signal: the highest-conviction, highest-engagement content is never a ticker call.

### Recurring linguistic patterns
- **Trading-as-metaphor for real life, not the reverse** — grief, illness, and legal "paperwork" are described in options/portfolio language ("a trade you actually believed in get halted mid-session," "rebalance... trim exposure to regret"). This is a distinctive, consistent authorial voice across the whole sample, not a one-off.
- **Radical, dated transparency about personal history** — addiction, incarceration ("previous residence" = county jail, where he now leads recovery meetings), a felony DUI, job loss, and financial hardship are disclosed repeatedly and specifically, not vaguely alluded to.
- **Self-deprecating, pun-heavy humor as an explicit coping mechanism**: *"I use humor as a defense mechanism. Same way a trader uses overly complicated option structures... taking reality fully unhedged can wipe you out."* (2026-01-09)
- **Meta-awareness of the platform itself**: he is the only subject in this cohort who has publicly reverse-engineered AfterHour's own API, published it, and run an AI behavioral-profiling pass on 25 traders including himself — i.e., he has already produced a version of this exact document.
- **Reaction to red days / volatility**: unusually calm and process-oriented rather than emotional; volatility is treated as raw material for content ("THE VIX FIRST AID KIT," "6/10 THETA SELLING TO DEGENS") rather than a threat.
- **A documented, sourced distrust of the platform** that directly explains the Feb-2026 cadence collapse: *"If the house has a direct feed into your brokerage visuals and your community momentum playbooks, they don't need to guess... I'm standing near the exit now."* (2026-02-04)

---

## 5. Quantitative Verdict for TraderMatrix

### Primary and Secondary Algorithmic Classification Tags
- **Primary: `SYSTEMATIC_THETA_HARVESTER`** — the wheel (CSP → assignment → covered call → repeat) is the account's real, mechanical, auditable edge, documented down to individual contract fills across multiple sub-$5 and sub-$10 underlyings.
- **Secondary: `MULTI_ENTITY_CAPITAL_NOISE`** — a structural data-integrity flag, not a trading style: this handle's tracked `amount_k` conflates at least three distinct real capital pools (own account, father's retirement account, funded-challenge accounts). Any downstream model must decompose before use.
- **Tertiary: `RECOVERY_NARRATIVE_CREATOR`** — his highest-engagement content and much of his platform value is personal/community-mentorship, not trade-calling; this materially affects how his "signal" should be weighted (see matrix below).

### Algorithmic Alpha Score & Expectancy
**Alpha Score: 58 / 100**

Rationale: genuine, demonstrated **execution alpha** in a narrow, mechanical, income-generating strategy (the wheel), documented with real trade-by-trade granularity that most of this cohort never provides — this is a rare, positive signal. It is materially discounted by (a) a real, catastrophic personal-account drawdown in June 2025 (-98% in 48 hours) that is never fully explained or fully recovered eighteen months later, and (b) a satellite speculative book (867 tickers, largely inherited from a community basket) that is wide, low-conviction, and not independently a source of edge. The score sits meaningfully above the momentum/YOLO-dominant profiles in this cohort because the core strategy is genuinely systematic and auditable, but well short of "high-conviction alpha" because his own real trading capital has not grown net of the June 2025 collapse.

**Expectancy characterization:** **Small, positive, high-frequency expectancy on the wheel sleeve** (premium collection on liquid, dividend-paying, low-priced underlyings, documented at roughly 11.6% over 9 weeks / ~67% annualized on the BTG example, unlevered) — a genuinely harvestable, low-drama edge. **Neutral-to-negative expectancy on the speculative satellite sleeve**, which is better read as content/community material than as a signal source. **The high-band capital swings carry no expectancy information for this subject at all** — they are not his trades.

### Signal Flow Ingestion Matrix

| Signal Type | Example Trigger | Artemis Action | Confidence |
|---|---|---|---|
| A granular, dated, multi-fill wheel log on a specific low-priced underlying ("I've Made $X Wheeling a $Y Stock") | `$BTG` wheel breakdown, 2026-05-17 | **Ingest as a strategy template** — strike/delta selection, roll timing, and assignment handling are real and reproducible; suitable for a low-priced, dividend-paying, options-liquid screener rule | High |
| `amount_k` reading ≥ $200K on this specific handle | Any post in the high band | **Discard entirely for return/drawdown calculations.** Do not attribute to the subject's personal risk-taking without independent confirmation of which account is live | High (structural, confirmed via 464 vs. 600 bimodal split) |
| A wide, multi-ticker "basket dump" post (>10 tickers) | AH Naughty List updates | **Treat as inherited community content, not original idea generation** — low signal value for ticker selection, but useful as a sentiment/attention proxy for what the broader AH community is watching | Low-Medium |
| Personal/recovery/life-event post, however trading-metaphor-laden | "CONTENT WARNING," "THE HOUSE THAT JACK BUILT" | **Do not interpret coincident `amount_k` moves as trading signals.** Flag the post itself as a likely marker of reduced posting/trading activity for the following weeks | High |
| Explicit macro-hedge experiment framed as a rule ("Golden Trailing Stops": `((ATR×1.5)+(IV×1.5))/2`) | $GLD trailing-stop post, 2026-01-21 | **Ingest as a candidate exit-rule formula** for a backtest — his own framing is exploratory ("let's see"), so validate independently before deployment | Medium |
| A stated pivot toward building his own trading tools/signals (TradingView indicators, screeners, TraderDaddy/Sam) | 2026 Q1–Q2 posts | **Track as a meta-signal of platform sophistication**, not a trade call — useful context for interpreting the *quality* of his other signals, which should be weighted upward relative to this cohort's median | Medium |
| Any post referencing the AfterHour public-API disclosure or his own AH analysis tool | "EVERY SKELETON, EVERY CLOSET" | **Operational note for Artemis's own ingestion pipeline**, not a trading signal — confirms the data source has no authentication and is fully scrapeable, which is both an opportunity (cheap ingestion) and a risk (other agents may already be doing the same thing, crowding any edge found here) | High |

### Specific Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. **Mirror the wheel methodology, not the specific tickers.** His documented approach (sell CSPs on dividend-paying, options-liquid, sub-$10 names; accept assignment; sell covered calls at or near cost basis; reload on dips; repeat) is a real, reproducible, low-drama income strategy independent of any single underlying.
2. **Use his gold/macro-hedge commentary and trailing-stop experiments as candidate risk-overlay rules** for a backtest, not as live signals — validate the `(ATR×1.5 + IV×1.5)/2` formula independently before any deployment.
3. **Treat his tooling output (screeners, indicators, TraderDaddy/Sam signal reports) as a second-order data source** worth periodically checking for genuinely new screening logic, given his demonstrated technical sophistication relative to this cohort.

**Contrarian Fade Directives (when to fade him / the retail herd around him):**
1. **Fade the inherited community-basket names** (the AH Naughty List tail) when they spike in his post volume — this reflects community momentum, not his own independent conviction, and is the least differentiated part of his content.
2. **Do not treat a high `amount_k` reading on this handle as bullish confirmation of anything.** It is very likely not his trade.
3. **Be skeptical of any single-name conviction call made during a documented high-cadence content-production burst** (Aug 2025–Jan 2026, ~120 posts/month) — volume that high correlates with business-building activity (LLC formation, fund launch, AMA) more than with newly-discovered trading edge.

**Mandatory Risk Blacklists & Firewalls:**
1. **Never compute a lifetime return, Sharpe ratio, or drawdown from the raw `amount_k` series for this handle.** It must first be split at the ~$200K boundary, and even the sub-$200K band should be treated as approximate given at least one multi-day glitch/alternate-account excursion inside it (2025-05-21, "Millionaire Hattrick").
2. **Toxic-instrument flag: none identified at the position level** — this is a meaningful, positive contrast with peers in this cohort. His one clearly self-labeled "mistake" (selling BTC to fund $MSTY) was small in absolute dollar terms and fully disclosed with numbers.
3. **Do not use his self-applied `[Gain]`/`[Loss]` tags as a naive backtest ground truth without noting the June 2025 collapse is untagged** (no `[Loss]` post exists for the $147K→$2K move) — his tagging is far more honest than this cohort's norm but still incomplete for the single largest drawdown in his history.
4. **Firewall: any signal sourced from a post coincident with a personal-crisis disclosure** (grief, health, platform-trust rupture) should be down-weighted or excluded — cognitive load during these windows is explicitly high by his own account.

**Exit Rules & Alpha Rectification:**
1. **For any wheel-style position mirrored from his content, adopt his own documented rule set directly**: sell calls at/near cost basis, let assignment happen without FOMO, reload on dips, roll rather than chase — this is the one part of his behavior worth copying mechanically rather than fading.
2. **Impose an external circuit breaker on the speculative satellite sleeve** (basket-inherited names, LEAPS, Yolo-tagged plays) independent of his own holding behavior, since this sleeve is not run with the same discipline as the wheel and produced the one real catastrophic drawdown in the sample.
3. **Re-evaluate exposure to any name entering his content during a high-cadence burst period** — treat sudden volume spikes in his posting as a crowding proxy on the underlying theme, not a conviction signal.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone |
|---|---|
| 2024-12-19 | **First post** — launches a real-money ($800, later $2K) Fidelity basket replicating @squeezekid's "AfterHour Naughty List"; `amount_k` baseline ≈$118K by 12-21 |
| 2024-12(implied) | Loses his corporate accounting/institutional-finance job — later revealed to be tied to a felony DUI conviction surfacing in a background check |
| 2025-01 to 05 | Low-band capital climbs steadily, ~$118K → ~$158K, running wheel + AH Naughty List basket + macro/VIX commentary |
| 2025-03 | "By March, I was exhausted" — corporate job-search abandoned; pivots fully into trading, initially via funded/prop accounts ("named after planets") |
| Spring 2025 | Funded-account momentum scalping produces stated 160–200%+ monthly returns — "unsustainable... I killed it, until I didn't, all in one afternoon" |
| **2025-06-04** | **Real, personally-narrated capital collapse: $147.24K → $2.23K in 48 hours** — the sample's one genuine, own-money catastrophic drawdown |
| 2025-06-09 | **"MY NAME IS MICHAEL AND I AM AN ALCOHOLIC, ADDICT, TRADER, FELON..."** — 1-year sobriety anniversary confession; lifetime-high engagement (141 reactions, 121 comments) |
| 2025-06-21 to 06-26 | High-band excursion to $833K, sustained 5 days, unremarked — likely a second/alternate-account sync artifact |
| 2025-07 to 09 | Low-band rebuild, $22K → $45K, driven by granular wheel activity across small caps and YieldMax ETFs |
| 2025-08-16 | "ANOTHER MILLIONAIRE JOINS THE RANKS" — reveals he now manages his **father's** ~$750K→$1M+ retirement rollover; explains a real, distinct high-band capital source |
| 2025-09-20/21 | "I LOVE YOU, PAT" and "I SEE FIELDS OF GREEN" — two of his three highest-engagement posts, both non-trading, personal/community content |
| 2025-09-19 → 2026-01-07 | Sustained high-band plateau, climbing to a **peak of $1,656.76K on 2025-12-20** ("MY 1 YEAR AfterHour ANNIVERSARY") |
| 2025-10-28 | "AMA: 1 YEAR PRO. STILL $1M & YET BROKE" — first-person account of the funded-account boom/bust, wheel philosophy, and felony-related career barriers |
| 2025-11-27 | **"QUIT MY JOB TO TRADE... HERE'S WHAT I BROKE."** — discloses the BTC-for-$MSTY liquidity mistake, formally announces Momentum Phinance LLC and a Substack-based transparent public fund; states AfterHour will shift to short-form only |
| 2025-11-29 | "BROKERS FOR LLCs" — live poll choosing tastytrade vs. IBKR for the new LLC's brokerage account |
| 2026-01-09 | **"CONTENT WARNING: FEELINGS AHEAD"** — personal-crisis post (loss/illness/legal "finality"), coincident with a same-day $1,638K → $80.58K `amount_k` collapse that should **not** be read as a trading loss |
| 2026-01-21 | "GOLDEN TRAILING STOPS" — live `(ATR×1.5+IV×1.5)/2` trailing-stop experiment on $GLD |
| **2026-02-04** | **"THE HOUSE THAT JACK BUILT"** — platform-trust departure post, alleging AfterHour's brokerage-sync/AI integration risks user data being harvested as a training/extraction product; announces a full pivot to Substack. Second-highest comment count in the sample (133). `amount_k` returns to and stays in the low band ($44–51K) for the rest of the sample. |
| Feb–May 2026 | Cadence collapses to 1–25 posts/month; content shifts to TradingView tooling, a "TraderDaddy"/"Sam" (TraderLady) bot product, weekly signal reports, and granular wheel-transaction logs (e.g., $BTG, $OUST) |
| 2026-05-24 | "Options Field Manual - Now Free" — releases an options-education resource; second-highest lifetime view count (2,707) |
| Jun–Jul 2026 | **Zero posts** — longest silence in the sample prior to the final gap |
| 2026-08-02 | **"EVERY SKELETON, EVERY CLOSET"** — publicly discloses AfterHour's unauthenticated public API, publishes a scraping tool and a dual-AI-pass behavioral-analysis site (`mphinance.com/ah/`) profiling 25 named AfterHour traders, himself included |
| 2026-08-05 | **Last post in sample** ("IV IMPACT"); `amount_k` = $41.22K |
| 2026-09-10 | Report date — **35 days silent**, no posts since 2026-08-05 |

---

*End of dossier. Prepared for the Artemis Engine signal-ingestion pipeline. Before any downstream backtest or capital-tracking model uses this subject's `amount_k` series, apply the sub-/super-$200K split documented in §1 and discard the high band entirely unless independently reconciled against a named account.*
