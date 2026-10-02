# TraderMatrix: Style-Tagged Trader Dataset

Merged forensic dataset for the AfterMath project. One row per AfterHour trader, combining the Sonnet-model quant dossier verdict, the mechanical entry/exit follow-through audit, and observed posting cadence. Use this to match a trading style to the best-fit trader(s).

| Handle | Style Tags | Primary Classification | Secondary Classification | Alpha Score | Follow-through % | Gain:Loss Tag Ratio | Cadence | Top Tickers |
|---|---|---|---|---|---|---|---|---|
| @Bobdog | Options Income / Wheel, Momentum / Swing | THETA_WHEEL_OPERATOR | HIGH_BETA_MOMENTUM_SPECULATOR | 74 | 41.8 | 3.74 | — | — |
| @Rise | Options Income / Wheel, Signal Vendor / Educator / Aggregator | THETA_INCOME_WHEEL_OPERATOR | RETAIL_EDUCATOR_CONTENT_ENGINE | 71 | 76.1 | 22.5 | Daily Regular (3-9/week) | QQQ, APP, RDDT, SPY |
| @Tiger_ | Long-Term Compounder, High-Risk / Gambler (caution) | FUNDAMENTAL_QUALITY_COMPOUNDER | LEVERAGED_CONTRARIAN_DIP_BUYER | 68 | 27.2 | 0.62 | Occasional Swing (1-3/mo) | DIS, RDDT, TBBB, CRWV |
| @DocHollywood | Macro / Hedging, High-Risk / Gambler (caution) | MACRO_NARRATIVE_MEGACAP_CORE | SCANDAL_ADJACENT_BAGHOLDER | 61 | 57.8 | 37.0 | Weekly Swing (1-2/week) | META, AVGO, GLD, UEC |
| @883Ismygovtname | Options Income / Wheel, Long-Term Compounder | COVERED_CALL_WHEEL_COMPOUNDER | DIVERSIFIED_SATELLITE_SPECULATOR | 58 | 79.1 | 4.0 | Hyperactive Machine (>1/day) | PBR, HPE, SOFI, ASTS |
| @Legitimate_Risk | Momentum / Swing, Long-Term Compounder, Signal Vendor / Educator / Aggregator | QUALITY_PYRAMID_SWING_ACCUMULATOR | SIGNAL_AGGREGATOR_COPY_TRADER | 58 | 17.8 | 4.9 | Hyperactive Machine (>1/day) | CRWV, NTR, ORCL, BTC |
| @YungEmber | Momentum / Swing | CONCENTRATED_STORY_STOCK_HODLER | DD_DRIVEN_MOMENTUM_SWINGER | 58 | 39.5 | 8.67 | Weekly Swing (1-2/week) | ONDS, ONDL, CLWT, PLTR |
| @internetdialup | 0DTE / Index Scalping, Momentum / Swing, Long-Term Compounder | LEAPS_EXERCISE_ACCUMULATOR | MOMENTUM_SWING_SCALPER | 58 | 72.0 | 17.5 | Occasional Swing (1-3/mo) | FIG, HOOD, PL, SNDK |
| @mphinance | Options Income / Wheel | SYSTEMATIC_THETA_HARVESTER | MULTI_ENTITY_CAPITAL_NOISE | 58 | 51.6 | 4.69 | — | — |
| @dick | Momentum / Swing, Signal Vendor / Educator / Aggregator | THEMATIC_MULTIBAGGER_HUNTER | SURVIVORSHIP_BIASED_CONTENT_FUNNEL | 51 | 38.9 | — | Occasional Swing (1-3/mo) | HYPE, AMPG, ADEA, AAOI |
| @ALLOY | 0DTE / Index Scalping, Macro / Hedging, Signal Vendor / Educator / Aggregator | GEX_POSITIONING_OPERATOR | SIGNAL_VENDOR_GURU | 47 | 24.3 | 60.65 | Daily Regular (3-9/week) | URA, SPY, IREN, CRCL |
| @SE83 | 0DTE / Index Scalping, Event-Driven / Special Situations | MANIPULATION_THESIS_CONTRARIAN | EVENT_DRIVEN_GAMMA_SCALPER | 46 | 19.2 | 3.75 | Weekly Swing (1-2/week) | NVDA, RXRX, VERI, TTD |
| @TRON | Momentum / Swing, High-Risk / Gambler (caution) | THEMATIC_MOMENTUM_DISCOVERY | CONCENTRATED_OPTIONS_BAGHOLDER | 46 | 41.7 | 101.0 | Hyperactive Machine (>1/day) | INFQ, NVDA, ADBE, SNDK |
| @RoyaltyTradez | 0DTE / Index Scalping, Momentum / Swing, Signal Vendor / Educator / Aggregator | LEVEL_BASED_INDEX_SCALPER | MOMENTUM_MEGA_CAP_SWING | 42 | 33.6 | 0.0 | Hyperactive Machine (>1/day) | MSTR, META, BA, UNH |
| @Drone_Daddy | Momentum / Swing, Event-Driven / Special Situations | THEMATIC_SUPPLY_CHAIN_DD_CONCENTRATOR | — | 41 | 59.4 | 29.25 | Daily Regular (3-9/week) | GLD, VIX, NKE, LULU |
| @longwashere | Momentum / Swing, Macro / Hedging, High-Risk / Gambler (caution) | MACRO_CATALYST_SWING_TRADER | CONCENTRATED_BAGHOLDER | 41 | 35.3 | 5.8 | Weekly Swing (1-2/week) | AEO, SOXL, META, USO |
| @moloch | Momentum / Swing | THEMATIC_MOMENTUM_ROTATOR | QUANT_TOOLING_HOBBYIST | 39 | 0.0 | — | Occasional Swing (1-3/mo) | DGXX, ABAT, UNH, AS |
| @RM20252029 | Options Income / Wheel, High-Risk / Gambler (caution) | THETA_WHEEL_INCOME | COMPULSIVE_OPTIONS_GAMBLER | 38 | 26.6 | 7.17 | Weekly Swing (1-2/week) | JD, META, MSFT, AAPL |
| @ThetaMaestro | Momentum / Swing, Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution) | MOMENTUM_SWING_LEAPS_TRADER | NARRATIVE_CULT_BAGHOLDER | 38 | 58.0 | 8.25 | Weekly Swing (1-2/week) | TSWCF, MTPLF, BTC, MSTR |
| @Trading_with_Art | Options Income / Wheel, Signal Vendor / Educator / Aggregator | CSP_WHEEL_INCOME_SELLER_DISCLOSED_WINDOW | SAAS_FOUNDER_CONTENT_MARKETER | 38 | 57.6 | — | Weekly Swing (1-2/week) | NVDA, CRM, ADBE, NOW |
| @AtypicallyErect | Momentum / Swing, Event-Driven / Special Situations, High-Risk / Gambler (caution) | MICROCAP_HALT_SNIPER | QUANTUM_THEMATIC_BAGHOLDER | 34 | 25.4 | 11.05 | Daily Regular (3-9/week) | CYPH, OMEX, RGTI, INFH |
| @Cynce | Options Income / Wheel, Macro / Hedging | INCOME_OVERWRITER | VOL_ARB_SPECULATOR | 34 | 0.0 | 0.5 | Occasional Swing (1-3/mo) | UNH, UNHG, MTPLF, ALT |
| @Dallaslongcall | Momentum / Swing, Event-Driven / Special Situations | THEMATIC_MOMENTUM_LONG_CALLS | REGIONAL_SUPPLY_CHAIN_RESEARCHER | 34 | 57.6 | 13.0 | Hyperactive Machine (>1/day) | AMAT, CAMT, NVDA, CRM |
| @The_Golden_Calf | 0DTE / Index Scalping, Momentum / Swing, Event-Driven / Special Situations | DILUTION_BOUNCE_SCALPER | NARRATIVE_MOMENTUM_CHASER | 34 | 32.1 | 3.85 | Occasional Swing (1-3/mo) | BSX, ONDS, HURA, ORBS |
| @Freeballer | 0DTE / Index Scalping, Signal Vendor / Educator / Aggregator | COMMUNITY_TICKER_EVANGELIST_ONDS | 0DTE_SPX_SPY_SCALPER_RULES_BASED | 33 | 37.5 | — | Hyperactive Machine (>1/day) | WEN, AAPL, TSLA, SPY |
| @TheRealChad | Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution) | COPY_TRADE_SIGNAL_AMPLIFIER | CONCENTRATED_THEME_BAGHOLDER | 32 | 66.7 | 1.84 | Occasional Swing (1-3/mo) | GOOGL, MSFT, OKLO, ONDS |
| @MarketVictor | Options Income / Wheel | MECHANICAL_PREMIUM_SELLER | CONCEALED_CONCENTRATION_RISK | 31 | 57.7 | 21.75 | Daily Regular (3-9/week) | SPY, AXTI, PANW, AVGO |
| @SonnySide | Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution) | CONVICTION_BAGHOLDER | RETAIL_IR_PROMOTER | 29 | 43.5 | 25.5 | Weekly Swing (1-2/week) | TAKOF, RCAT, XTIA, ONDS |
| @NewFishBigPond | Momentum / Swing | RETAIL_MOMENTUM_AMPLIFIER | LATE_STAGE_ILLIQUIDITY_CHASER | 24 | 37.4 | 5.15 | Hyperactive Machine (>1/day) | DBGI, NFLX, TNON, KOPN |
| @gr8_ripple | Options Income / Wheel, High-Risk / Gambler (caution) | RETAIL_NARRATIVE_BAGHOLDER | NOVICE_THETA_WHEEL_FARMER | 24 | 60.0 | 1.0 | Occasional Swing (1-3/mo) | TE, ACHR, DDD, SPY |
| @terridactil | Momentum / Swing, Signal Vendor / Educator / Aggregator | EDUCATOR_MOMENTUM_NARRATOR | THEMATIC_SPECULATIVE_SWING_TAGGER | 24 | 31.8 | — | Hyperactive Machine (>1/day) | RDW, ESE, GD, HII |
| @trynamakeit | 0DTE / Index Scalping, Momentum / Swing | SPY_INDEX_OPTIONS_TA_SCALPER | MOMENTUM_THEME_CHASER | 24 | 39.5 | — | Hyperactive Machine (>1/day) | SPY, QQQ, BE, HOOD |
| @daren | Momentum / Swing, Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution) | HERD_SENTIMENT_AGGREGATOR | MOMENTUM_FOMO_HOLDER | 22 | 23.7 | 4.33 | Daily Regular (3-9/week) | XTND, ASTS, KEEL, GLXY |
| @wallhawk | Momentum / Swing, High-Risk / Gambler (caution) | RETAIL_MOMENTUM_CHASER | SOCIAL_SIGNAL_RELAY | 22 | 20.0 | 26.0 | Weekly Swing (1-2/week) | HPE, NIO, PUSA, INFQ |
| @browndog | High-Risk / Gambler (caution) | UNDISCIPLINED_LOTTO_GAMBLER | SINGLE_TICKER_BAGHOLDER_ONDS | 21 | 53.3 | 5.0 | Weekly Swing (1-2/week) | ONDS, LCID, SPY, NVDA |
| @WarrenBuffett | High-Risk / Gambler (caution) | SERIAL_ACCOUNT_BLOWUP | OVERLEVERAGED_OPTIONS_GAMBLER | 19 | 44.3 | 12.3 | Occasional Swing (1-3/mo) | BTC, NKE |
| @Mikki4Shikki | High-Risk / Gambler (caution) | NARRATIVE_BAGHOLDER_NO_STOPS | SOCIAL_AMPLIFIER_LOW_ORIGINATION | 18 | 33.3 | 0.92 | Weekly Swing (1-2/week) | ONDS, ONDL, MTPLF, CVU |
| @RyanLP | Options Income / Wheel, High-Risk / Gambler (caution) | PREMIUM_SELLER_MECHANICAL | UNDEFINED_RISK_TAIL_GAMBLER | 14 | 73.2 | 8.5 | Daily Regular (3-9/week) | CAT, AVGO, KOOL, NVDA |
| @smartguyac | Momentum / Swing, Macro / Hedging, High-Risk / Gambler (caution) | DEGENERATE_MOMENTUM_GAMBLER | VIBES_BASED_MACRO_CALLER | 14 | 25.0 | — | Occasional Swing (1-3/mo) | HOOD, LHX, LDI, SPY |
| @x52x | Momentum / Swing, Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution) | EXTREME_LEVERAGE_MOMENTUM_GAMBLER | SERIAL_BOOM_BUST_CYCLICAL | 14 | 52.2 | 2.43 | Weekly Swing (1-2/week) | SPCX, DASH, HOOD, SPY |
| @Tradeless | Momentum / Swing, Macro / Hedging, Signal Vendor / Educator / Aggregator | PERMA_BEAR_MACRO_HEDGER | THEMATIC_LIST_AGGREGATOR | 12 | 1.9 | 2.0 | Weekly Swing (1-2/week) | NKE, SNDK, DCO, LUNR |

## Per-Trader Directives (Ingest / Fade / Firewall)

### @Bobdog — alpha 74
Style: Options Income / Wheel, Momentum / Swing
Classification: THETA_WHEEL_OPERATOR / HIGH_BETA_MOMENTUM_SPECULATOR
**Ingest (copy this):**
- Harvest his thematic asset discovery radar
- Use his Blue Star weekly regime shifts as a trend-continuation bias overlay for equity and crypto swing portfolios
**Fade (do the opposite):**
- Fade his emotional revenge-trading declarations
- Fade short-dated earnings option gambles
**Firewall (never mirror):**
- Hard Firewall against unverified multi-account Plaid telemetry
- Blacklist directional long call purchases exceeding 30 DTE without a defined exit stop
- Zero-Margin Firewall: Strictly enforce his own stated rule: never deploy portfolio margin on speculative growth names

### @Rise — alpha 71
Style: Options Income / Wheel, Signal Vendor / Educator / Aggregator
Classification: THETA_INCOME_WHEEL_OPERATOR / RETAIL_EDUCATOR_CONTENT_ENGINE
**Ingest (copy this):**
- Treat his macro-regime posture (cash %, ITM-CC tilt direction) as a sentiment/positioning overlay input, not a standalone trade signal
**Fade (do the opposite):**
- Fade his Tier-3 speculative sleeve entries (QUBT-class quantum names, penny drone/meme names): these are explicitly sized-down "gambles" he himself later regrets
- Discount "Theta Daddies community result" posts entirely as an individual-trader alpha signal
**Firewall (never mirror):**
- Blacklist: naked long options as a mirrored instrument class
- Firewall on the amount_k telemetry field for this trader specifically: exclude from any automated equity-curve, drawdown, or Sharpe calculation
- Data-continuity firewall: flag the Jul 2025–Apr 2026 window as low-confidence / sparse-signal for this trader
- Position-sizing floor: never let mirrored single-name exposure exceed his own stated caps (10% per trade, 20% per position)

### @Tiger_ — alpha 68
Style: Long-Term Compounder, High-Risk / Gambler (caution)
Classification: FUNDAMENTAL_QUALITY_COMPOUNDER / LEVERAGED_CONTRARIAN_DIP_BUYER
**Ingest (copy this):**
- Auto-tag any ticker he moves into "Untouchable" tier or above 10% disclosed portfolio weight as a high-quality long candidate for independent fundamental verification
- Treat his rare, explicit "leverage/margin ON" statements as a high-conviction contrarian-bottom signal on broad risk sentiment
- His 2026 short theses are catalyst-anchored (launch dates, earnings, funding-gap analyses)
**Fade (do the opposite):**
- Fade his trim/rotation timing specifically, not his stock selection
**Firewall (never mirror):**
- No stop-loss discipline exists in this trader's process
- Leverage/margin usage is real and has hit 120% gross on a single name
- Concentration risk is structural to his style (single names routinely 20–50% of book)
- His short book (2026) is new, small-sample, and philosophically inconsistent with 8+ years of stated long-only fundamental discipline
- Self-admitted history of catastrophic loss chasing low-quality, cash-burning names (2021/22)

### @DocHollywood — alpha 61
Style: Macro / Hedging, High-Risk / Gambler (caution)
Classification: MACRO_NARRATIVE_MEGACAP_CORE / SCANDAL_ADJACENT_BAGHOLDER
**Ingest (copy this):**
- Track the DIP Index basket live (currently: MU, NVDA, TSM, MRVL, AVGO, AAPL, LITE, COHR, CLS, AAOI as of the May 2026 update) as a standing thematic-rotation signal
- Whenever a rare, specific, self-disclosed loss/transparency post appears (the "Portfolio L's" format), ingest it at high priority
**Fade (do the opposite):**
- Fade fresh conviction posts on structurally-impaired or scandal-adjacent names
- Discount his self-applied Gain tag
- Treat his reassurance-during-panic posts ("DO NOT PANIC") as a crowd-sentiment indicator, not a trading signal
**Firewall (never mirror):**
- Firewall any signal sourced from this account on a name carrying an active fraud, accounting-restatement, or research-misconduct headline
- Never size a position off his self-reported percentage performance claims (DIP Index returns, podcast trade recaps) without independent price verification
- Do not treat a gap or absence in his posting as a market-calm signal

### @883Ismygovtname — alpha 58
Style: Options Income / Wheel, Long-Term Compounder
Classification: COVERED_CALL_WHEEL_COMPOUNDER / DIVERSIFIED_SATELLITE_SPECULATOR
**Ingest (copy this):**
- Implement the 70–90%-profit-decay covered-call buyback rule as a standalone, ticker-agnostic exit heuristic inside any Artemis wheel/income module
**Fade (do the opposite):**
- Fade her own profit-taking on high-beta speculative LEAPS specifically
- Do not treat her broad, 360-ticker universe as a diversified "buy list"
**Firewall (never mirror):**
- Never interpret amount_k = 0.0 for any post dated 2025-06-30 or later as a real account balance
- Never treat the tag/gain_loss structured fields as a P&L ledger for this source
- Blacklist copying entry mechanics from the BloFin leveraged-crypto or copy-trading experiment
- Do not weight relationship/persona-drama content ("AH husband," romantic bits with named peers) as trading signal

### @Legitimate_Risk — alpha 58
Style: Momentum / Swing, Long-Term Compounder, Signal Vendor / Educator / Aggregator
Classification: QUALITY_PYRAMID_SWING_ACCUMULATOR / SIGNAL_AGGREGATOR_COPY_TRADER
**Ingest (copy this):**
- Ingest his entry ticker + price + stated rationale the day it posts
- Track his trailing-stop exits as a secondary confirmation signal for names Artemis already holds
- Use his named-source attributions (BobDog, Tron, MASTERGROOVE, Freeballer, Madam_Dee) as a pointer graph
- His quality/dividend large-cap sleeve (JNJ, LLY, ASML, DAL, FDX, COKE) is his most defensible, differentiated basket relative to the more herd-driven small-cap momentum names
**Fade (do the opposite):**
- Fade his cash-timing calls when they persist past 2 quarters
- Discount any "3-year journey" or aggregate net-worth milestone post by default
**Firewall (never mirror):**
- Do not inherit his income/yield-product exposure uncritically (MSTY, ULTY, similar synthetic-covered-call income ETFs)
- Do not treat his self-reported win rate (70–75%, sourced from his own AI assistant) as validated
- Firewall all posts dated 2026-03 onward that contain subscriber/pricing/testimonial language from any performance-attribution model
- Do not copy his loss-realization timing

### @YungEmber — alpha 58
Style: Momentum / Swing
Classification: CONCENTRATED_STORY_STOCK_HODLER / DD_DRIVEN_MOMENTUM_SWINGER
**Ingest (copy this):**
- Treat every new @YungEmber multi-part DD series launch as a research trigger, not a trade trigger
- His catalyst timing on dilution/cash-runway events is worth tracking as a leading indicator even when his own directional call is wrong
- Options contract/strike disclosures on his core names are usable as real-time retail options-flow confirmation for names already on an Artemis watchlist
**Fade (do the opposite):**
- Fade any "conviction unchanged" or address-the-ticker-directly post made during a >20% drawdown from a recent peak in that name
- Fade micro-float/extreme-SI squeeze entries (HUBC-type)
- Fade "up $X since last update" milestone posts as a near-term top signal, not a momentum-continuation signal
**Firewall (never mirror):**
- Never size-mirror his position disclosures
- Blacklist sub-$1 / sub-2M-float squeeze names sourced from his posts (HUBC-class)
- Do not treat "sold X to buy Y" rotation posts as risk-off signals
- Firewall his prediction-market / entertainment-gambling disclosures entirely

### @internetdialup — alpha 58
Style: 0DTE / Index Scalping, Momentum / Swing, Long-Term Compounder
Classification: LEAPS_EXERCISE_ACCUMULATOR / MOMENTUM_SWING_SCALPER
**Fade (do the opposite):**
- Fade clusters of high rocket/moon-emoji, "we only go up," blow-off-top language
- Fade "buy the dip / discount season" calls specifically when they appear during a structural macro break (tariff/geopolitical shock) rather than routine chop
- Treat his self-tagged 94.6% "Gain" ratio as a sentiment/selection-bias artifact, not a real win rate
**Firewall (never mirror):**
- Blacklist sizing/leverage inheritance entirely
- Firewall the 2025-09-10 → 2025-10-11 amount_k readings ($2.78K–$4.27K) from all trend and drawdown calculations
- Hard-blacklist the meme-coin/hype-instrument class (TRUMP/MELANIA inauguration coin YOLO)
- Do not treat his self-built "Diamondhands" auto-trading bot (2026) as a validated signal source
- Do not inherit his "exercise into shares" behavior wholesale

### @mphinance — alpha 58
Style: Options Income / Wheel
Classification: SYSTEMATIC_THETA_HARVESTER / MULTI_ENTITY_CAPITAL_NOISE
**Ingest (copy this):**
- Mirror the wheel methodology, not the specific tickers
- Use his gold/macro-hedge commentary and trailing-stop experiments as candidate risk-overlay rules for a backtest, not as live signals
**Fade (do the opposite):**
- Fade the inherited community-basket names (the AH Naughty List tail) when they spike in his post volume
- Do not treat a high amount_k reading on this handle as bullish confirmation of anything
- Be skeptical of any single-name conviction call made during a documented high-cadence content-production burst (Aug 2025–Jan 2026, ~120 posts/month)
**Firewall (never mirror):**
- Never compute a lifetime return, Sharpe ratio, or drawdown from the raw amount_k series for this handle
- Toxic-instrument flag: none identified at the position level
- Do not use his self-applied [Gain]/[Loss] tags as a naive backtest ground truth without noting the June 2025 collapse is untagged (no [Loss] post exists for the $147K→$2K move)
- Firewall: any signal sourced from a post coincident with a personal-crisis disclosure (grief, health, platform-trust rupture) should be down-weighted or excluded

### @dick — alpha 51
Style: Momentum / Swing, Signal Vendor / Educator / Aggregator
Classification: THEMATIC_MULTIBAGGER_HUNTER / SURVIVORSHIP_BIASED_CONTENT_FUNNEL
**Ingest (copy this):**
- Use his rivalry-driven picks (anything explicitly framed as a response to @sirjack or another named AH peer) as a lower-confidence tertiary lead only
**Fade (do the opposite):**
- Fade the "at peak" framing specifically
**Firewall (never mirror):**
- Never treat any self-reported performance statistic (Year-in-Review, DICKINDEX™️ update, "up X% YTD," "+X% at peak") as a verified capital or P&L data point
- Discard the amount_k structured field entirely for this source
- Blacklist copying entry mechanics, size, or cost basis from the options-swing disclosures (BBWI, LDI, BITF calls)
- Do not weight monetization-adjacent posts (anything containing "subscribe," "kindly," "dolla a day," "spots left," or similar funnel language) as trading signal

### @ALLOY — alpha 47
Style: 0DTE / Index Scalping, Macro / Hedging, Signal Vendor / Educator / Aggregator
Classification: GEX_POSITIONING_OPERATOR / SIGNAL_VENDOR_GURU
**Ingest (copy this):**
- Treat @ALLOY's GEX sign, gamma-flip level, and OI-wall calls as a candidate cross-validation input against Artemis's own dealer-positioning module
**Fade (do the opposite):**
- Never treat a "Gain"-tagged bragpost as evidence of a repeatable edge
- Treat unresolved narrative threads (a big account, a bold prediction) that simply stop being mentioned as an implicit "this went badly"
- Discount macro/geopolitical mega-theses for direct trade sizing
**Firewall (never mirror):**
- Never size any position off his self-reported dollar or percentage PnL
- Firewall any signal sourced from a post that also contains Prism promotional content (giveaways, "ask me about Prism," scarcity countdowns)
- Do not treat his post cadence as a market-volatility proxy

### @SE83 — alpha 46
Style: 0DTE / Index Scalping, Event-Driven / Special Situations
Classification: MANIPULATION_THESIS_CONTRARIAN / EVENT_DRIVEN_GAMMA_SCALPER
**Ingest (copy this):**
- Pull his insider Form-4 cluster call-outs as raw tips for independent SEC-filing verification
- Track his gap-fill and 200-SMA levels on SPY/QQQ/mega-caps as candidate support/resistance inputs, re-verified against the Engine's own technical stack before acting
- Log his NVDA post-earnings-fade thesis as a standing seasonal bias flag around NVDA earnings dates, weighted lightly
**Fade (do the opposite):**
- Fade his individual options entries directly
- Fade any RXRX/OPEN/VERI/TTD-style distressed bottom-fish call he makes
- Treat his high-engagement "called it" / validation posts as retail-crowd euphoria markers, not alpha
**Firewall (never mirror):**
- Never size a position off his self-reported percentage returns (e.g. "+1000%," "+650%")
- Blacklist copy-trading his penny/distressed single-name calls (RXRX, OPEN, VERI, and similar sub-institutional-quality names he self-identifies as a weakness)
- Do not ingest his futures (MNQ) setups into live execution without independent backtesting
- Firewall geopolitical/war-headline posts entirely from the trading pipeline

### @TRON — alpha 46
Style: Momentum / Swing, High-Risk / Gambler (caution)
Classification: THEMATIC_MOMENTUM_DISCOVERY / CONCENTRATED_OPTIONS_BAGHOLDER
**Ingest (copy this):**
- Treat @TRON as a discovery/screener feed for small-cap thematic and SPAC-conversion names, not an execution model
**Fade (do the opposite):**
- Fade any "rolled my calls further out" or "diamond-handing" post in his flagship name of the moment
- Fade retail herd enthusiasm when his engagement metrics spike (reactions/comments materially above his trailing average) on a single ticker
- Fade, don't follow, any post where he says he "added on the way down" / "not really worried"
**Firewall (never mirror):**
- Never size a position to match his stated conviction language ("all in," "would sell my whole port," "tattoo if it hits $100")
- Never mirror options duration extensions (rolls) as a reason to add
- Treat his self-applied [Gain]/[Loss] tags as unreliable for backtesting
- The amount_k series itself must be sanitized before use
- Toxic instrument flag: $ONDS options, specifically

### @RoyaltyTradez — alpha 42
Style: 0DTE / Index Scalping, Momentum / Swing, Signal Vendor / Educator / Aggregator
Classification: LEVEL_BASED_INDEX_SCALPER / MOMENTUM_MEGA_CAP_SWING
**Ingest (copy this):**
- Ingest his daily SPY/QQQ/IWM pre-market level calls as one weighted input into a multi-trader consensus/breadth signal
- Ingest explicit, fully-specified options callouts (ticker + strike + expiry + entry price + SL) only
- Harvest his loss-recovery percentage table and 30%-cut rule as a static risk-management module (correct, reusable, source-agnostic)
- Treat elevated posting cadence spikes (e.g., 150+ posts/month) as a crude retail-attention/volatility proxy
**Fade (do the opposite):**
- Fade "discount" framing at climactic extension, not at initial pullback
- Fade parabolic long-tail momentum names (ASTS, SPCX, SKHY, MRAM, ONDS-style bursts) once his post frequency on a single small/mid-cap ticker spikes within a short window
- Discount % return claims made in hindsight (post-facto "up 300%" framing without a prior disclosed entry)
**Firewall (never mirror):**
- BLACKLIST the amount_k / platform-verified-PnL field entirely for this trader
- BLACKLIST any inference of "verified" performance
- FIREWALL Kingdom/Patreon promotional posts from any signal-scoring pipeline
- FIREWALL Topstep/prop-futures posts

### @Drone_Daddy — alpha 41
Style: Momentum / Swing, Event-Driven / Special Situations
Classification: THEMATIC_SUPPLY_CHAIN_DD_CONCENTRATOR / None
**Ingest (copy this):**
- Treat @Drone_Daddy as a specialist screener for the drone/CUAS/defense-optics/onshoring supply chain
- His defense-policy catalyst tracking (Sec Def actions, NDAA/China-parts restrictions, FAA rule changes) is a genuine, sourced macro-thematic input
**Fade (do the opposite):**
- Fade euphoric/meme-tagged posts at or near a stated local account high
- Fade any post that pre-announces a further average-down level ("Last average down will occur at $9")
- Fade retail herd enthusiasm cross-amplified across his pod (@TRON, @YungEmber, @Drone_Daddy simultaneously promoting the same $ONDS/$UMAC names)
**Firewall (never mirror):**
- Never size a mirrored position to his stated conviction or LEAPS-concentration levels in $ONDS, $UMAC, or $LPTH
- Treat his Gain/Loss self-tags as unreliable for backtesting or performance-attribution models
- Exclude any content carrying a ?ref= link, a paid-service/Substack/Discord mention, or a livestream promotion from signal ingestion
- Toxic pattern flag: prolonged silence following a loud, high-conviction thematic call
- The amount_k series must be used only as the "Challenge Port" sleeve it is

### @longwashere — alpha 41
Style: Momentum / Swing, Macro / Hedging, High-Risk / Gambler (caution)
Classification: MACRO_CATALYST_SWING_TRADER / CONCENTRATED_BAGHOLDER
**Ingest (copy this):**
- Supply-Chain / Rumor-Arbitrage Pattern: His DELL/SMCI Blackwell-overheating trade is a template worth encoding generically
**Fade (do the opposite):**
- Numeric Reconciliation Check: Any of his self-reported account totals should be treated as directional only

### @moloch — alpha 39
Style: Momentum / Swing
Classification: THEMATIC_MOMENTUM_ROTATOR / QUANT_TOOLING_HOBBYIST
**Ingest (copy this):**
- Auto-flag any ticker he rotates into on the same day he abandons a bad-news large-cap
- Treat his "[Chart]"/"[Dd]" proprietary-level calls as a leading indicator of an eventual large move, with an expected adverse excursion first
- Use his LPPLS/bubble-oscillator research as a pointer to a legitimate quant technique (Sornette log-periodic power law) worth Artemis independently implementing and backtesting
**Fade (do the opposite):**
- Fade any "[Gain]"-tagged post as an entry trigger
- Fade the basket-diversification instinct, not the underlying names
- Fade anything he explicitly labels "chance play" or "hunch." He is telling you, in his own words, that the thesis has no depth
- Fade retail momentum-chasing into his named microcaps after a big printed run
**Firewall (never mirror):**
- Sub-$5 / low-float microcaps sourced from this trader require independent liquidity, float, and short-interest screening before any auto-sizing
- Never treat his silence as a hold signal
- Firewall the amount_k portfolio-value series from being read as a clean, deposit-adjusted return stream
- Cap any options/leverage replication at a symbolic sleeve size
- Out-of-scope: Kalshi/prediction-market and crypto exposure

### @RM20252029 — alpha 38
Style: Options Income / Wheel, High-Risk / Gambler (caution)
Classification: THETA_WHEEL_INCOME / COMPULSIVE_OPTIONS_GAMBLER
**Ingest (copy this):**
- Log the wheel's structural parameters as a strategy template, not a copy-trade signal: weekly ITM/ATM CSP/CC cycling, $50K-$500K capital bands, mentor-sourced discipline
- Track his weekly realized-P&L cadence as a account-health proxy only
**Fade (do the opposite):**
- Fade any pre-announced "going heavy on YOLO/leaps/buying options" post immediately and completely
- Fade the "cores stay put till they break even" framing as a top/bottom-agnostic risk signal, not a bullish one
- Treat his syndicated mega-cap DD posts (AAPL/TSLA/META/NVDA) as retail-consensus noise, not proprietary insight
**Firewall (never mirror):**
- Never mirror the undisclosed wheel underlyings speculatively
- Never inherit his selective-disclosure pattern

### @ThetaMaestro — alpha 38
Style: Momentum / Swing, Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution)
Classification: MOMENTUM_SWING_LEAPS_TRADER / NARRATIVE_CULT_BAGHOLDER
**Ingest (copy this):**
- Harvest his covered-call-income and earnings-straddle tactics as standalone, reusable options structures independent of his ticker theses
- Use his mega-cap/large-cap momentum entries (NVDA, UBER, WMT, TTD-class names) as a secondary confirming signal only when catalyst-driven and options-based
**Fade (do the opposite):**
- Fade continuation on any post exhibiting the 🚀🌕💎🙌 emoji cluster combined with single-name concentration language ("core holding," "multi-year hold," "keep cooking")
- Fade/heavily discount any post that is substantively a reposted company press release (BTC-acquisition announcements, "Yield %" stats)
- Treat hostile, insult-laden defenses of an underwater position ("braindead," "low IQ," "stfu") as a high-confidence local-top/capitulation-proximity signal
**Firewall (never mirror):**
- Blacklist NAV-premium Bitcoin-treasury micro-caps as a category for position mirroring (MTPLF, and by extension KULR/similar names he championed pre-MTPLF)
- Never mirror leverage-funding proposals
- Firewall single-instrument concentration above the trader's own stated rules
- Discount aggregated/imported DD

### @Trading_with_Art — alpha 38
Style: Options Income / Wheel, Signal Vendor / Educator / Aggregator
Classification: CSP_WHEEL_INCOME_SELLER_DISCLOSED_WINDOW / SAAS_FOUNDER_CONTENT_MARKETER
**Fade (do the opposite):**
- Fade the "Power 5" broad sector-dump content
- Discount any market commentary explicitly sourced from "Trader Daddy Pro" / TraderMatrix from 2026-03-10 onward
**Firewall (never mirror):**
- Never size off this account's PnL for any date after 2026-03-26
- Firewall all TraderDaddy Pro / TraderMatrix / Vespryx-branded content as commercially motivated; do not treat platform-sourced data citations as independent third-party validation
- Net the disclosed misses against the disclosed wins before crediting the CSP-wheel strategy
- Do not credit the Feb 2026 "-14% drawdown, survived on position sizing" narrative as proof of disciplined risk management in isolation

### @AtypicallyErect — alpha 34
Style: Momentum / Swing, Event-Driven / Special Situations, High-Risk / Gambler (caution)
Classification: MICROCAP_HALT_SNIPER / QUANTUM_THEMATIC_BAGHOLDER
**Ingest (copy this):**
- Mirror the halt-list scan, not the halt-list buy
- Harvest his stock-lending-fee methodology as a standing squeeze-candidate signal
- Treat his 2026 OSINT/macro theses as an idea-generation feed, independently underwritten
- Log the reverse-split rounding-arbitrage mechanism as a standing structural watchlist rule, not a copy-trade signal
**Fade (do the opposite):**
- Fade escalating superlative language as a local-top proxy
- Fade "no stop loss" declarations specifically
- Treat his persecution/manipulation narratives as noise, not signal
- Discount post-disconnection PnL claims to near-zero evidentiary weight
**Firewall (never mirror):**
- Hard blacklist: copying his position sizing
- Hard blacklist: copying his margin behavior
- Toxic-habit flag: "algorithm did it" claims with no disclosed methodology
- Toxic-habit flag: his own disclaimers ("NFA," "🎲 Responsibly!") are inversely correlated with actual risk control in this trader's specific case

### @Cynce — alpha 34
Style: Options Income / Wheel, Macro / Hedging
Classification: INCOME_OVERWRITER / VOL_ARB_SPECULATOR
**Ingest (copy this):**
- Treat his NAV/sum-of-parts DD (KSS real-estate-vs-operations breakdown) as a template methodology for screening hated/complex-structure names
**Fade (do the opposite):**
- Fade his covered-call strike selection into strength
- Fade "hate the company, love the stock" contrarian buys as a possible value trap unless independently confirmed
- Fade averaging-down language dressed as conviction ("💎✋ don't sell," doubling a position after a binary catalyst crash)
**Firewall (never mirror):**
- Cap or exclude levered/inverse VIX-futures ETPs (UVIX/SVIX/VIXI) from any mirrored allocation beyond a short-tactical-hedge sleeve
- Firewall the entire 2025-09-22 → 2026-04-13 silent window and all content from the Substack-pivot era from being scored as trading signal
- Exclude single-share "DD-only" positions (e.g., his 1-share KSS post) from position-following logic entirely

### @Dallaslongcall — alpha 34
Style: Momentum / Swing, Event-Driven / Special Situations
Classification: THEMATIC_MOMENTUM_LONG_CALLS / REGIONAL_SUPPLY_CHAIN_RESEARCHER
**Ingest (copy this):**
- Treat his AI-data-center power/supply-chain DD posts (AMAT/AXTI/AAOI/LITE/COHR/AVGO/ANET/CRDO/VST/NVTS/VRT/APLD/FRMI) as a standing watchlist-generation source
- Log his GLD "safe/inelastic" hedge entries as a soft de-risking timing signal, particularly when they appear shortly after a documented drawdown in his own account
**Fade (do the opposite):**
- A sudden multi-week spike in his post cadence (materially above his ~9-11/wk baseline) should be read as a possible late-cycle/euphoria signal, not rising conviction
- Never weight a Gain-tagged post as evidence of a working strategy
- Fade broad, undiversified concentration signals
**Firewall (never mirror):**
- Never inherit his position sizing or total thematic exposure
- Never treat a Gain/Loss tag as ground truth for performance scoring
- Firewall any signal sourced from this account during a documented multi-week cadence spike
- Do not copy his exit timing

### @The_Golden_Calf — alpha 34
Style: 0DTE / Index Scalping, Momentum / Swing, Event-Driven / Special Situations
Classification: DILUTION_BOUNCE_SCALPER / NARRATIVE_MOMENTUM_CHASER
**Ingest (copy this):**
- Harvest his first DD post on any new ticker as an early retail-flow timestamp
- Track his thematic series launches (a self-branded multi-post DD arc, e.g. "Drone Summer," "Space Summer") as a sector-rotation early-warning flag with a 2-4 week lead
- Use his congressional/insider-trade-sourced biotech screens as one input into a broader politician-trade cross-reference model
- His tranche-based profit-taking style (scale out 50-75% into strength, hold a small runner) is worth encoding as a rule, decoupled from his specific tickers
**Fade (do the opposite):**
- Fade "always buy under $X" mechanical dip calls once the underlying breaks that level with volume
- Fade continued conviction posts on a name he has held >90 days underwater (HURA is the canonical case)
- Fade retail enthusiasm at "Wonderful week" / milestone-follower posts
**Firewall (never mirror):**
- Blacklist any mirroring of naked/uncovered option-selling
- Blacklist copy-sizing off his position language ("I have almost $4K of $AIRO," "3K+ shares... over half my portfolio")
- Firewall micro-cap serial-diluters (HURA, UMAC, CLBR-class names) from any auto-hold logic
- Firewall any position he has held longer than his own median hold time on a "catalyst" name (biotech binary events especially) once the catalyst date has already slipped once

### @Freeballer — alpha 33
Style: 0DTE / Index Scalping, Signal Vendor / Educator / Aggregator
Classification: COMMUNITY_TICKER_EVANGELIST_ONDS / 0DTE_SPX_SPY_SCALPER_RULES_BASED
**Ingest (copy this):**
- Treat his named scam/pump callouts as a standing contrarian-fade watchlist input
**Fade (do the opposite):**
- Fade specific $ONDS price targets ($15/$20/$25-style calls) as promotional rather than analytical
- Discount any bullish thesis that coincides with a CEO-interview or webinar announcement for the same name
**Firewall (never mirror):**
- Never size a position off his self-reported SPX/SPY dollar "receipts"
- Firewall any $ONDS-specific signal sourced from this account from being treated as independent
- Do not attribute commentary on $BYND/$ORBS/$HUBC/$SPCX/$PUSA to him as trading positions
- Do not treat post-cadence spikes as a volatility or opportunity proxy for this trader

### @TheRealChad — alpha 32
Style: Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution)
Classification: COPY_TRADE_SIGNAL_AMPLIFIER / CONCENTRATED_THEME_BAGHOLDER
**Ingest (copy this):**
- Harvest scale-out cadence, not entries
- Use his DD posts as an idea-sourcing net, then re-verify independently
- Treat his four-sub-account monthly report cards as a lightweight retail-cohort performance benchmark (e.g., his Feb 2025 +4%–+38% range vs
**Fade (do the opposite):**
- Fade concentration bravado
- Fade his post-cadence spikes as a crowd-panic proxy
- Fade, don't follow, his @ThetaTard/@SirJack-sourced entries directly
**Firewall (never mirror):**
- Blacklist thinly-traded/illiquid narrative micro-caps sourced from this account without independent liquidity/fundamental verification (MTPLF, KULR, LUNR, ONDS-tier names)

### @MarketVictor — alpha 31
Style: Options Income / Wheel
Classification: MECHANICAL_PREMIUM_SELLER / CONCEALED_CONCENTRATION_RISK
**Ingest (copy this):**
- Harvest the daily AVWAP-Q / SMA-stack / Heikin-Ashi scorecard as a reusable, legible technical regime filter
- Use the Fair Value / FCF / Cash-to-Debt / Debt-to-EBITDA / Interest Coverage checklist as a standalone fundamental pre-screen for any CSP or long-hold candidate universe
**Fade (do the opposite):**
- Fade the implied safety of any "I'm freed up / fully de-risked" claim from this trader
- Fade paid-product launch/relaunch posts as a cyclical-top marker, not a credibility signal
- Do not treat his stated refusal to sell "long-term holdings" during a flagged macro-risk window as a bullish conviction signal
**Firewall (never mirror):**
- Firewall any "Weekly Trade Summary" win-rate/P&L figure from being read as whole-account performance
- Blacklist copy-signal usage of his "long-term holdings" / conviction-hold positions entirely
- Never surface his self-reported "Total YTD Profit" figure to end users without an appended note that it excludes his largest, least-transparent position bucket
- Flag any month where his self-reported win rate is rising or flat while amount_k is falling (documented Dec 2025

### @SonnySide — alpha 29
Style: Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution)
Classification: CONVICTION_BAGHOLDER / RETAIL_IR_PROMOTER
**Ingest (copy this):**
- Auto-flag any ticker he posts within 48h of first mention with an unusned-volume/insider-buy rationale
- Relay filed-catalyst posts (13F/13G, earnings, contracts) as verified-news pass-through only
- Log his options-structure choices (LEAPS entry, CSP-to-wheel pivot) as strategy templates to evaluate on Artemis's own risk engine, decoupled from his position sizing
**Fade (do the opposite):**
- Fade escalating combativeness on an existing large position
- Fade "good news, still down" sequences
- Fade the "$500 Challenge"/gamified-small-account posts as a herd-sentiment proxy
**Firewall (never mirror):**
- Never mirror single-name concentration
- Blacklist thinly-traded sub-$10 tickers sourced purely from his "insider buying" or "most actives" call-outs (e.g., $LOOP, $TRUG, $VRME, $BURU, $SWMR) from any automated ingestion
- Firewall anything tagged with ZHG/community/meetup context
- Never inherit his options-assignment passivity

### @NewFishBigPond — alpha 24
Style: Momentum / Swing
Classification: RETAIL_MOMENTUM_AMPLIFIER / LATE_STAGE_ILLIQUIDITY_CHASER
**Ingest (copy this):**
- Auto-flag any sub-$5 or newly-IPO'd ticker he posts within the first 24-48h of a premarket-volume or short-interest citation (Fintel-sourced)
- Build a relay network map: when he credits a named user for a call, log that user as a potential independent signal source
- Treat his 20-30%-options-exit rule itself (not his execution of it) as a usable default profit-target parameter for any Artemis strategy trading similar short-dated momentum names
**Fade (do the opposite):**
- Fade "diamond hands"/defiance posts during an active drawdown on his largest position
- Fade escalating combative/defensive posts
- Fade breakout-chase posts on names already up double digits intraday ($BYND at $4.20 after-hours, momentum names post-pop)
- Fade the retail-herd effect of his follower-milestone/engagement-bait content as a standalone signal
**Firewall (never mirror):**
- Hard cap single-name concentration at 5-8% in any Artemis-derived basket sourced from his content, full stop
- Blacklist averaging-down as a mirrored behavior
- Firewall all gambling-adjacent content (sports parlays, roulette/numerology posts) from any ingestion pipeline
- Blacklist illiquid sub-$2 "hot garbage" penny stocks sourced purely from his premarket volume call-outs without independent float/liquidity verification
- Treat any period of amount_k telemetry blackout as an automatic risk-off flag for that trader's entire content stream until sync resumes

### @gr8_ripple — alpha 24
Style: Options Income / Wheel, High-Risk / Gambler (caution)
Classification: RETAIL_NARRATIVE_BAGHOLDER / NOVICE_THETA_WHEEL_FARMER
**Ingest (copy this):**
- Treat any post where he names a specific AI copilot tool + a specific trade (strikes, expiry, entry rationale) as a distinct, higher-confidence signal class
- Independently verify and ingest the underlying catalyst data behind his deepest original DD (insider/board appointments, 13F/institutional stake changes on small-caps)
- Use his disclosed CSP/CC strikes on speculative small-caps (ONDS, ACHR, DDD, TE) as a retail floor-support tell
- Crawl the named mentors and communities he credits (Theta Daddies/Ripple Report, The Kingdom, TRON, Bobdog, mygreenknight, FridgeFinancials, CarlyBme) as upstream sources
**Fade (do the opposite):**
- Fade his panic-exits on names he has stated high conviction on
- Fade his FOMO second-guessing, not his original exit
- Never treat his own technical commentary as an independent confirming signal
- Discount any theoretical AI-generated hedge basket he discusses but does not fund (MSTY/BITI/SHY/KBWD)
**Firewall (never mirror):**
- 0DTE index options
- Long-dated VIX "hedge" calls
- Single-stock option-income ETFs (YieldMax-style, e.g., MSTY)
- Years-held, thesis-stale legacy bags (the INMB pattern: no fresh catalyst, sunk-cost holding)
- The 2025-12-19 amount_k step-change (401k→IRA rollover) and the 2025-08-10/08-20 anomaly must be excluded from any automated NAV/return/Sharpe computation on this trader

### @terridactil — alpha 24
Style: Momentum / Swing, Signal Vendor / Educator / Aggregator
Classification: EDUCATOR_MOMENTUM_NARRATOR / THEMATIC_SPECULATIVE_SWING_TAGGER
**Ingest (copy this):**
- Calendar feed only
- Congressional-trade correlation leads
- Defined-level swing triggers
- Thematic watchlist seeding
**Fade (do the opposite):**
- Fade the "already moved" post
- Discount high-volume/high-drama weeks
- Fade retail-herd euphoria clusters
**Firewall (never mirror):**
- Never mirror her actual options entries/exits
- Blacklist copy-trading of SPX/SPY/NVDA short-dated ("lotto") options
- Ignore all no-trigger predictive/thesis content (e.g., "SpaceX becomes the largest S&P company," Anthropic-vs-Nvidia valuation musings, "which stock survives 69 more years" polls)
- Hard-filter the 61% untagged lifestyle/motivational corpus out of any ticker-universe or sentiment-scoring pipeline entirely
- Never scale position size off her disclosed dollar figures
- Flag joint-attribution risk

### @trynamakeit — alpha 24
Style: 0DTE / Index Scalping, Momentum / Swing
Classification: SPY_INDEX_OPTIONS_TA_SCALPER / MOMENTUM_THEME_CHASER
**Ingest (copy this):**
- Track his thematic rotation basket (uranium/UEC, space/ASTS, nuclear/OKLO, rare earth/MP, AI infra/NOW) as an early theme-discovery watchlist
**Fade (do the opposite):**
- Fade posts that frame active drawdowns as pure community opportunity ("Kingdom Smells Blood," "Elevator mode," toasting 🥂 through red days)
- Fade his "who else caught that" retroactive victory-lap posts
- Fade single-name conviction calls sourced from Kingdom-member tips (e.g., CLOV/VIVK "brought to my attention by a member")
**Firewall (never mirror):**
- Blacklist any position-sizing inference drawn from his account
- Firewall his self-tagged Gain/loss-free track record from any trust or reputation scoring
- Blacklist "no stop loss" behavior as practiced, not preached
- Do not surface promotional/discount-code content to any downstream consumer as trading signal under any circumstance

### @daren — alpha 22
Style: Momentum / Swing, Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution)
Classification: HERD_SENTIMENT_AGGREGATOR / MOMENTUM_FOMO_HOLDER
**Ingest (copy this):**
- Harvest the weekly poll-winner feed as a standalone retail-sentiment product
- Track his personal "I FOMO'd into X" posts as lagging momentum-confirmation events
**Fade (do the opposite):**
- Fade the crowd
- Fade any of his own trade mentions that immediately follow a documented multi-week silence during a falling amount_k trend
- Discount his [Gain] milestone posts as marketing, not performance evidence
**Firewall (never mirror):**
- Blacklist copying his simultaneous multi-directional single-name positioning (the FFIE pattern: long shares + long calls + long puts on one ticker at once)
- Firewall the "8.5 mil of Sir Jack's money" paper-account posts entirely from any real-capital modeling
- Blacklist "averaging down on a leveraged option" as a pattern
- Never surface a poll-winner ticker as a "Daren conviction call" without explicitly labeling it as crowd-sourced

### @wallhawk — alpha 22
Style: Momentum / Swing, High-Risk / Gambler (caution)
Classification: RETAIL_MOMENTUM_CHASER / SOCIAL_SIGNAL_RELAY
**Ingest (copy this):**
- When he explicitly credits a named third party, route the signal to that person's own tracked profile (e.g., @RoyaltyTradez, @trynamakeit) rather than crediting wallhawk
**Fade (do the opposite):**
- Fade any no-thesis, hype-only single-ticker post ("let's ride," "feeling frisky," "🚀🌙" with no catalyst) on a micro-cap
- Fade the "squeeze?" framing specifically (used on $LDI, $CGC, $BYND)
- Treat his binary-catalyst straddles as evidence the retail herd around a given event has no real directional conviction
**Firewall (never mirror):**
- No sizing off his lotto/short-dated OTM options structures ($TQQQ 90P bought one day pre-expiry, $MDB $5→$200 lotto)
- Discount his self-reported win-rate entirely
- Exclude all Phase 2 posts (2025-11-07 onward) from quantitative ingestion
- Firewall against his politically-motivated catalyst framing bleeding into position sizing

### @browndog — alpha 21
Style: High-Risk / Gambler (caution)
Classification: UNDISCIPLINED_LOTTO_GAMBLER / SINGLE_TICKER_BAGHOLDER_ONDS
**Ingest (copy this):**
- Use his $GLD/$SLV entry and exit timing as a soft overlay signal on the Engine's own metals/inflation-hedge module
- Log any future AI-assisted signal-generation posts (he has already built one Claude-based agent) as a leading indicator of retail-side AI-agent adoption
**Fade (do the opposite):**
- Treat any fresh $ONDS conviction post as a contrarian signal, not a follow signal
- Fade his earnings-week binary option entries directly
- When he posts a leveraged-ETF position with no stated stop-loss, treat that specific absence as the risk signal itself
**Firewall (never mirror):**
- Blacklist $ONDS-adjacent leveraged products ($ONDL, $ONDG) from any copy-signal pipeline sourced from this account
- Never size a position off his self-reported percentage returns (e.g., "266% profit," "+50%")
- Firewall any signal sourced from this trader during a documented margin/liquidity-stress window (his Feb 2026 near-margin-call period)
- Do not treat post-cadence as a volatility proxy for this trader

### @WarrenBuffett — alpha 19
Style: High-Risk / Gambler (caution)
Classification: SERIAL_ACCOUNT_BLOWUP / OVERLEVERAGED_OPTIONS_GAMBLER
**Ingest (copy this):**
- Options-Mechanics Templates: His "Poor Man's Covered Call" and debit-spread structuring posts are mechanically sound, generic templates (high community engagement confirms clarity)

### @Mikki4Shikki — alpha 18
Style: High-Risk / Gambler (caution)
Classification: NARRATIVE_BAGHOLDER_NO_STOPS / SOCIAL_AMPLIFIER_LOW_ORIGINATION
**Ingest (copy this):**
- Use her amplification posts purely as routing pointers
- Flag any future $CVU-style original DD (sourced financials, named contracts, explicit backlog figures, self-aware uncertainty framing) for an independent Artemis fundamental screen
- Her plain-share, no-options disclosure style makes any position size she reveals easy to verify against price action
**Fade (do the opposite):**
- Fade any post where she addresses a held ticker emotionally ("why do you hate me," "toying with my emotions," "everything is fine")
- Fade "buying the dip as a silver lining" framing ($ONDS at $9.33, Feb '26)
- Fade crowd-sourced "sell or hold?" posts as evidence the underlying name has an unusually large contingent of framework-less retail holders, not as a read on fair value
**Firewall (never mirror):**
- Never mirror her position sizing or averaging-down behavior
- Firewall all broker-affiliate/gamified-promo content sourced from her posts ($HOOD Holidays, "Alpha" app referral)
- Blacklist simultaneous common+leveraged product pairing ($ONDS+$ONDL) as a sizing cue
- Treat any extended portfolio-link blackout as a hidden-drawdown flag, not a data gap to ignore

### @RyanLP — alpha 14
Style: Options Income / Wheel, High-Risk / Gambler (caution)
Classification: PREMIUM_SELLER_MECHANICAL / UNDEFINED_RISK_TAIL_GAMBLER
**Ingest (copy this):**
- Harvest his IV Rank / IV-mean-reversion framework as a generic vol-regime heuristic (sell premium when IVR is elevated, buy when depressed)
- Track his 1256-contract / SPAN-margin instrument selection (SPX/XSP, index and ag futures) as a curated liquid-underlying watchlist
- Use his weekly "Opened/Managed/Closed/Open Positions" counts as a rough activity/leverage-creep gauge for the wider Kingdom cohort he represents
**Fade (do the opposite):**
- Fade any post where he sells undefined-risk premium into a stated "bloodbath" or "welcome the volatility" framing
- Fade his single-name "conviction" buys sourced from vibes/AI summaries (SRFM, MNMD, HIMS-style narrative longs)
**Firewall (never mirror):**
- Blacklist "manage at 21 DTE" as practiced (i.e., roll-forever)
- Firewall his Portfolio Margin leverage regime from any position-sizing model Artemis derives from his stated 1-3%/5% rules
- Do not surface his weekly recap PnL headline numbers to end users without an appended verified-drawdown disclaimer

### @smartguyac — alpha 14
Style: Momentum / Swing, Macro / Hedging, High-Risk / Gambler (caution)
Classification: DEGENERATE_MOMENTUM_GAMBLER / VIBES_BASED_MACRO_CALLER
**Ingest (copy this):**
- When this account posts a named-indicator technical setup (Bollinger compression, MACD/signal cross, short-interest divergence, options-flow debit-spread reads)
- Treat any call-out crediting an external source (e.g., "@dick" on $BITF) as a pointer to that source, not to this trader
**Fade (do the opposite):**
- Fade euphoric/relief milestone posts as a near-term top signal
- Fade "just a feeling" directional calls outright
**Firewall (never mirror):**
- Never size-mirror anything from this account
- Blacklist all politically-framed narrative posts (Trump/Xi, MAGA rate-cut framing, "Don would approve," Fed-speech memes) as non-actionable noise
- Blacklist all social-drama/grievance posts as trading inputs entirely
- Hard-stop ingestion once linked balance reads $0.00 for two or more consecutive posts (as occurred Aug 2026)
- Do not use the tickers structured field alone for this account

### @x52x — alpha 14
Style: Momentum / Swing, Signal Vendor / Educator / Aggregator, High-Risk / Gambler (caution)
Classification: EXTREME_LEVERAGE_MOMENTUM_GAMBLER / SERIAL_BOOM_BUST_CYCLICAL
**Ingest (copy this):**
- Treat @x52x as a leading momentum-entry indicator, not a position to mirror
- Use his amount_k series as a live volatility/euphoria thermometer for the broader retail options crowd he represents, not as a return template
- Log every "post-silence restart" event (100+ day gap followed by a small new deposit) as a discrete, dateable behavioral marker
**Fade (do the opposite):**
- Fade continued size-adds into an already-large, already-extended position
- Fade "Universe"/round-number target posts as directional signals entirely
- Treat "I'm #1 on the leaderboard" posts as a local-top marker for retail conviction, not as validation to add
**Firewall (never mirror):**
- Never size a position off his stated dollar amounts or account percentages
- Zero weight on his options structures specifically (no stops used, continuous rolling into strength, no LEAPs, near-100% short-dated concentration)
- Discount his self-reported win framing on any post that omits a subsequent resolution
- Exclude all monetization-link posts (Patreon/Discord/Twitch/etc.) from quantitative ingestion

### @Tradeless — alpha 12
Style: Momentum / Swing, Macro / Hedging, Signal Vendor / Educator / Aggregator
Classification: PERMA_BEAR_MACRO_HEDGER / THEMATIC_LIST_AGGREGATOR
**Ingest (copy this):**
- Scrape his thematic sector/ticker list posts as a free, timely universe-expansion feed for the internal screener stack
- Backtest the disclosed "ABC FOMC" fade-then-follow-the-presser framework as a standalone, mechanically testable strategy
**Fade (do the opposite):**
- Treat a cluster of his bearish index-put disclosures during an uptrend as a sentiment-extreme tell
**Firewall (never mirror):**
- Blacklist any signal generated during or after a TILT_REVENGE_BLOWUP state
- Never ingest sizing, entry mechanics, or stop-loss placement from his disclosed trades
- Hard-blacklist instrument class: uncapped-size 0DTE index options used as a directional hedge/gamble
- Treat any post containing "tips please," "tip me," or similar monetization prompts as a conflict-of-interest flag on the surrounding content's objectivity
