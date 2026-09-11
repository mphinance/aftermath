# QUANT FORENSIC DOSSIER: @internetdialup
### AfterHour Followed-Trader Autopsy — Artemis Engine Ingestion Report

| Field | Value |
|---|---|
| Handle | `@internetdialup` |
| Profile ID | `prf_58738c0ec7c14b4e8121f576ec2c5513` |
| Rank | #31 most active followed trader |
| Lifetime Posts Analyzed | 154 |
| Coverage Window | 2024-05-28 → 2026-08-11 (~115 weeks / ~27 months) |
| Source Files | `@internetdialup_lifetime.md` (qualitative), `@internetdialup_all_posts.json` (structured: `amount_k`, `tag`, `tickers`, `reaction_count`, `comment_count`) |
| Analyst | Sonnet 5, Artemis Quant Desk |
| Verdict (one line) | A self-taught, disabled Chicago product-design-engineer who ran his account from $200 (Nov 2023) to a documented, 1099-corroborated six-figure book primarily by exercising discount-window LEAPS on HOOD/NVDA/HIMS into core equity, then visibly matured — post margin-call — into a lower-frequency, discipline-first swing trader and finally a passive/ballast investor. One of the rare accounts in this cohort with a **positive, survivable, still-growing arc** rather than a blow-up; the caveats are heavy self-report bias, a chunk of edge that is really community-copied conviction, and a real data-integrity gap in the capital series. |

---

## 0. Data Provenance Note (read before trusting any number below)

The JSON field `amount_k` (account value, $ thousands) tracks a consistent, coherent series from **$23.6K (2024-05-28) up to $149.6K (2025-09-21)** — tight, plausible day-to-day steps throughout. Then, for **four consecutive posts spanning 2025-09-10 → 2025-10-11**, the value collapses to **$2.78K–$4.27K**, before jumping straight back to **$104.4K on 2025-11-19** with no drawdown narrative anywhere in the post text to justify a real ~97% wipeout. This is corroborated by the poster's own words in the same window: Post #118 ("AH is [not] syncing my RH correctly") and Post #119 ("I can't connect my RH anymore it just keeps glitching"). **Verdict: this is a brokerage-sync/tracking outage, not a real capital event.** All four readings in that window are excluded from trend and drawdown math below and flagged inline. A handful of other posts (2024-12-18, 2025-01-01, 2025-02-22, 2026-01-21, 2026-03-17 ×1, 2026-03-27 ×1, 2026-04-08 ×2, 2026-04-10) carry `null` amount_k — treated as missing, not zero.

---

## 1. Executive Profile

**Trading philosophy (stated and, unusually for this cohort, largely followed):** He describes himself explicitly as "more of an investor trader" (Post #106) whose signature mechanic is buying **long-dated, deep-discount calls during red days ("discount season," "clearance rack")** and then **exercising them into core share positions** rather than flipping premium — a strategy he traces directly to his single biggest documented lesson: getting greedy and giving back 50%+ of an NVDA call's value in June 2024 (Post #11) for not selling into strength. From that point forward the account shows a genuine behavioral arc: FOMO/YOLO degen in the first ~6 months → a March 2025 margin call → explicit rule-writing on profit-taking and mental health (Posts #57, #92) → a 2026 pivot to "I don't trade options anymore as I'm more passively investing" (Post #140) → building a personal Robinhood-MCP auto-trading CLI as a hobby project (Posts #150–151). This is a **maturation arc**, not a static style, and should be modeled as a time-varying signal, not a single tag.

**Post cadence** (154 posts / ~115 weeks = **1.34 posts/week lifetime average**), heavily front-loaded and correlated with both trading activity and disclosed health crises:

| Quarter | Posts | Avg reactions | Avg comments | Context |
|---|---|---|---|---|
| 2024-Q2 (onboarding) | 20 | 4.8 | 1.9 | Degen options era begins |
| 2024-Q3 | 7 | 5.1 | 1.9 | Summer lull |
| 2024-Q4 | 21 | 14.0 | 9.0 | $40K→$70K run, Robinhood Legend hype, peak engagement |
| 2025-Q1 | 21 | 13.2 | 5.6 | $100K milestone, then DeepSeek crash + margin call |
| 2025-Q2 | 31 | 9.5 | 5.1 | Tariff-crash drawdown & recovery, highest-volume quarter |
| 2025-Q3 | 17 | 10.4 | 6.4 | ATH $149.6K, then sync outage begins, hospitalization (blood clot/sepsis) |
| 2025-Q4 | 13 | 8.8 | 4.8 | Recovery to $95-116K, ASTS/PL space rally, infusion cycle disclosed |
| 2026-Q1 | 13 | 11.1 | 3.5 | New job (AI startup), $100K+ cross-brokerage milestone |
| 2026-Q2 | 8 | 4.6 | 2.9 | Builds "Diamondhands" auto-trade bot, cadence collapsing |
| 2026-Q3 | 3 | 5.7 | 1.7 | Self-described "lurker," content/lifestyle posts only |

Cadence decays steadily from ~2.4 posts/wk (2024-Q4) to ~0.2 posts/wk (2026-Q3) even as reported capital keeps climbing — this is a **shift from social-trading participant to quiet passive holder**, not tilt/withdrawal (contrast with the collapse-into-silence pattern seen in blown-up accounts in this cohort).

**Active timeline / verified capital trajectory** (clean series, sync-outage excluded):

- **2024-05-28** (archive start): **$23.6K** — already grown from a stated $200 opened Nov 2023 (per Post #3), i.e., the +11,700% early run predates this dataset and is unverifiable here.
- **2024-10-10**: **$37.4K**, self-reported "$200 in November to 40k" milestone post.
- **2024-12-19 → 2025-02-14**: **$70.3K → $100.4K**, "100K gang in 14 months" milestone (Post #62), the single most information-dense post in the archive — includes a **1099-sourced, third-party-verifiable figure**: net $89K in 2024 trading profit, $8.4K in trading losses, $600 in wash sales. This is the one number in the whole dossier with tax-document backing rather than self-report.
- **2025-02-14 → 2025-04-04**: **$100.4K → $75.8K**, a **-24.5% drawdown** coincident with the Trump tariff crash; he documents both directional shorting ("Spoils of War," profiting off SPY puts) and premature dip-buying ("discount season," "clearance rack") during the same window — mixed adaptive/non-adaptive response (see §3).
- **2025-03-18**: **margin call event** (Post #67), value $85.1K, down from a local $93.0K eight days earlier — the account's one disclosed leverage/risk-control failure.
- **2025-04-04 → 2025-09-21**: steady recovery and new highs, **$75.8K → $149.6K ATH**, driven by HOOD/FIG/space-sector gains.
- **2025-09-10 → 2025-10-11**: **data-integrity gap** (readings of $2.78–4.27K — excluded, see §0).
- **2025-11-19 → 2026-06-05**: **$104.4K → $142.9K** (new clean-series high), with a January 2026 milestone post citing **"across all my brokerages I'm up 100k+ investment wise"** (Post #132) — i.e., the tracked account is a subset of a larger, multi-brokerage net worth.
- **2026-08-11** (archive end): **$133.3K**, a modest -6.7% pullback off the June high, alongside a stated pivot to "stabler stocks," "less high beta swings," "stacking cash" ahead of anticipated IPOs (OA/Anthropic).

**Verified drawdown (clean series):** worst peak-to-trough is **-24.5%** (Feb–Apr 2025, tariff shock). No account-destroying event anywhere in the archive — a materially different risk outcome than most of this cohort.

---

## 2. Ticker Universe & Catalysts

**Core, repeat-traded names** (by mention count across 154 posts):

| Ticker | Mentions | Role |
|---|---|---|
| $HOOD | 13 | Core swing vehicle — calls around every product launch/earnings ("Legend," gold card, managed portfolios, custodial accounts); largest and most repeated realized-gain disclosures (700% leap, $1.3K, $830 swing) |
| $NVDA | 9 | Core LEAPS-exercise name; the June 2024 greed-loss lesson originates here |
| $U (Unity) | 8 | Long-running short bias (ATH $50 → ATL $13) that flips to a bullish exercise/hold thesis by 2025 — the account's clearest sunk-cost/bagholding case study |
| $SPY | 8 | Short-duration directional vehicle (0DTE/1DTE calls and puts), used both long (momentum) and short ("Spoils of War" during the tariff crash) |
| $HIMS | 6 | LEAPS-exercise name (15c → 100 shares), long-term bullish thesis on GLP-1/telehealth |
| $LUNR / $ASTS / $PL / $OKLO | 4 / 2 / 2 / — | Space/satellite/nuclear thematic basket, bought on government-contract headlines; recurring "$PL is the next $ASTS" pattern-matching |
| $FIG (Figma) | 4 | Occupational-conviction IPO play — he is a product designer/design engineer by trade, discloses building a personal Figma widget project |

**Long tail (1–2 mentions each):** dividend/ballast sleeve ($KO, $UNH, $LMT, $NOC, $KKR, $VHT), gaming thesis ($TTWO, $EA — GTA6 catalyst), late-cycle diversifiers ($WM, $XOM, $FDX, $SNDK, $CAT-adjacent), one-off IPO/momentum plays ($PLTR, $SPCE, $GRAB, $CRWD short), and a single pure-gambling meme-coin YOLO ($TRUMP/$MELANIA, inauguration week, self-tagged `[Yolo]`).

**Options vs. equities — a real regime shift, not a static mix:** 2024–mid-2025 is options-heavy (weekly/1DTE calls and puts, LEAPS bought to exercise); by Post #140 (2026-03-17) he states plainly **"I don't trade options anymore as I'm more passively investing."** By Post #154 (the archive's last post, 2026-08-11) he describes shifting to "Quant algo trading" and building a personal auto-trade bot — the account's terminal state is algorithmic/passive, not discretionary-options.

**What drives entries (stated, ranked by frequency):**
1. **Company-specific catalysts** — earnings, product launches (HOOD Legend, managed portfolios, custodial accounts), IPO filings (Figma), government contracts (LUNR/OKLO/PL).
2. **Red-day/volatility-driven dip-buying** — "discount season," "clearance rack," explicitly framed as buy-the-dip regardless of macro cause (DeepSeek shock, tariff shock).
3. **Macro calendar awareness** — FOMC, CPI, retail sales, tariff headlines — used mostly to time *when to sit out* short-dated options ("be cautious with those 0DTE") rather than to construct macro trades.
4. **Options-flow/greeks-assisted timing** (2026 era) — explicitly describes feeding ChatGPT screenshots of "gamma, delta, charm, options flow, and vanna" data before entries (Post #134), a meaningfully more quantitative approach than the 2024 "chatter says it'll hit X" era.
5. **Community signal-following, filtered** — cites Allie's AAPL DeepSeek-dip call by name (Post #59) but explicitly instructs followers (and, by his own account, himself) to "look at the data... track the 5 min candle... cross check with QD" before entering — a partial, not blind, copy-trade behavior.
6. **Occupational-domain conviction** — Figma, as a working product designer, is the one name where his edge claim has genuine (if unverifiable) informational basis.

---

## 3. Risk Management & PnL Reality

**Does he take profits or hold bags? Both, in sequence — a genuine before/after split around the June 2024 lesson and the March 2025 margin call:**
- **Before:** Post #11 (2024-06-06) — an NVDA call drops from $7K to $3K in value because he waited for $1,300 instead of selling; explicitly self-diagnosed as "being greedy." Post #39 shows multi-year Unity bagholding from ATH $50 down to ATL $13 with an explicit admission he "should've sold in December."
- **After:** Post #92 (2025-06-04) codifies the fix — "don't diamond hand... if you're in the green at like 94% just take the win" — and he discloses following exactly that rule on a same-day SPY 1DTE trade. Post #146 (2026-04-08) repeats the discipline on a 700%-gain HOOD leap ("TP b4 💎🙏").

**How he manages losing positions:** mostly by **not disclosing them** rather than by a documented exit process. The self-tagged sample is extremely skewed — **35 `[Gain]`-tagged posts vs. 2 `[Loss]`-tagged posts (94.6% self-reported win rate)** — a textbook survivorship/selection bias in what gets posted at all. The two `[Loss]` tags that do exist are both minimal/rhetorical (a -$5 SPY call he jokes about, and a sarcastic macro-prediction post with no dollar figure attached) — real losing trades are almost never narrated with the same specificity as wins.

**Documented wins (verifiable, ranked):**
1. **2024 tax year: $89K net trading profit** (1099-sourced, Post #62) — the one number in the archive with third-party corroboration.
2. **$200 → $100K+ in ~14 months** (Nov 2023 → Feb 2025), further compounding to a **$149.6K clean-series peak** by Sep 2025 and **$142.9K** by Jun 2026.
3. Repeated LEAPS-into-shares exercises at deep discounts: HIMS $15c, NVDA $100c, HOOD $20c/$69c/$80c — a repeatable, disclosed mechanic rather than one-off luck.
4. HOOD swing trades: $1.3K (83c), $830 same-day swing, 700% gain on a $69 two-week leap.

**Blow-ups / risk failures (ranked by severity):**
1. **March 2025 margin call** (Post #67) — the account's only disclosed leverage-control failure; no pre-trade sizing rule is ever described for this period.
2. **Feb–Apr 2025 tariff drawdown, -24.5%** — mixed response: he correctly shorted SPY into the crash ("Spoils of War," ~$400/day, ~$1K/week realized) but his simultaneous "discount season, buy the dip" calls (Posts #65, #68, #69) were **premature by 2–4 weeks** — the account kept falling for multiple posts after each "buy the dip" call before actually bottoming.
3. **June 2024 NVDA greed hold**, -~50% intraday value round-trip on a single call — the formative loss that produced his later take-profit discipline.
4. **Unity multi-year bagholding**, ATH $50 → ATL $13 — a genuine, admitted sunk-cost failure to cut a loser, later "resolved" only because the stock happened to recover, not because of active risk management.

---

## 4. Behavioral & Sentiment Signals

**Why is he posting?** Three motives that shift weight over the archive's life:
- **Early (2024):** pure trade-call sharing and community-building — tags a consistent ~15-name "OA" (Orangutan Army) mentor/squad list in nearly every substantive post (Posts #56, #57, #59, #60, #61, #62), a strong group-identity signal.
- **Middle (2025):** **teaching/mentorship** — a long, sincere essay on the mental-health side of trading (Post #57: "you are not the exit liquidity," FOMO/revenge-trading/gambling-addiction warnings) and repeated tactical tips (morning setup, London-hour execution, TP discipline).
- **Late (2025–2026):** **personal-brand/content** — mentions launching a blog, an Instagram handle, hosting an NYC design-systems workshop, and open-sourcing a personal trading CLI on GitHub. Trading disclosure becomes secondary to lifestyle/identity content as cadence falls.

**Recurring linguistic patterns:**
- **Contrarian-bullish reframing of red days**: "discount season," "clearance rack," "buy the dip" — used consistently regardless of whether the drawdown is routine chop or a structural break (the tariff crash). This is a **bull-market-only playbook** dressed as universal wisdom.
- **"I am the exit liquidity" / "You are not the exit liquidity"** — a self-aware retail-trader meme used both as humor and as genuine warning to followers.
- **"Spoils of war"** — his label for profiting via shorts during a crash, paired with self-aware guilt ("real people's livelihoods will be impacted while us keyboard warriors are profiting off the misery," Post #73).
- **"Kangaroo market"** for choppy/volatile tape; **"TACO Tuesday"** tariff-reversal meme; cat photos and "touch grass" as stress-coping and community-bonding devices on red days.
- **Heavy rocket/moon emoji density clustering near local tops** — "We only go up in UPTOBER," "Boss battle ATH LFG" — a retail-euphoria tell worth flagging as a contrarian signal in its own right (see §5.3).

**Reaction to volatility/red days:** a consistent two-track response — (a) reflexive "buy the dip" messaging framed as timeless wisdom, and (b) occasional genuine tactical adaptation (shorting SPY into the tariff crash, taking a break from active trading in Mar–Apr 2025 "as the market is too volatile at the moment for my liking," Post #68). Track (b) is the more valuable behavior to extract; track (a) is retail-sentiment noise.

**Context shaping cadence (not a trading signal, but explains gaps):** disclosed hospitalization for a blood clot and sepsis-causing pressure wound (Jul 2025, Post #110, describes himself as paralyzed/wheelchair-using), and a subsequent ~2-month, 3x-daily infusion regimen (Oct–Dec 2025, Posts #121, #130). Every major posting gap in the back half of the archive lines up with a disclosed health event or job transition, not with capital stress.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

- **Primary: `LEAPS_EXERCISE_ACCUMULATOR`** — buys long-dated, deep-discount calls on quality growth names during red days and exercises into core equity rather than flipping premium; the account's single most repeatable, verifiable mechanic (HIMS, NVDA, HOOD all documented multiple times).
- **Secondary: `MOMENTUM_SWING_SCALPER`** — short-duration (0DTE–2wk) directional options on HOOD/SPY/NVDA around catalysts, executed on a disciplined morning-setup/London-hour/quick-TP cadence established from mid-2025 onward.
- **Tertiary: `THEMATIC_CATALYST_CHASER`** — space/satellite/nuclear small-cap basket (LUNR/ASTS/PL/OKLO) bought on government-contract headlines with a recurring "next $X" pattern-match heuristic and thin disclosed DD.
- **Behavioral flag: `MATURING_DEGEN_TO_INVESTOR`** — a genuine, dated lifecycle transition (YOLO options degen → disciplined swing trader → passive/ballast investor) that should be modeled as a time-decaying weight on the options-related tags, not a fixed classification.
- **Secondary behavioral flag: `COMMUNITY_SIGNAL_FILTERER`** — echoes a named mentor group's calls but applies a partial independent filter (greeks/volume check) before acting; better than blind copy-trading, worse than independent alpha.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 58 / 100**

Justification: the score is meaningfully above this cohort's median because (a) the capital trajectory is real, large, and has one third-party-corroborated data point (the 2024 1099: $89K net profit); (b) the worst verified drawdown across ~27 months is -24.5%, with no account-destroying event, and a documented, dated behavioral fix (take-profit discipline) following his one big unforced error; (c) the account shows genuine strategy evolution toward lower-risk instruments over time rather than escalating leverage into a blow-up. It is capped well below 70 because (a) a large share of the disclosed "wins" are self-reported with essentially zero disclosed losses (94.6% Gain-tagged), so the true win rate is unverifiable and likely materially lower; (b) the thematic small-cap basket (LUNR/ASTS/PL/OKLO) is pattern-matched on thin DD ("the next $ASTS") rather than independently underwritten; (c) part of the demonstrated "edge" is really community-copied conviction (OA squad calls) rather than proprietary analysis; (d) the amount_k series has an unexplained multi-week integrity gap that reduces overall confidence in the capital series as an audit trail.

**Expectancy:** Positive and plausible on the LEAPS-exercise mechanic specifically (multiple repeated, disclosed successes at different strikes/names over 18+ months, consistent with a genuine buy-quality-dips-and-hold edge in a rising market). Expectancy on the short-duration swing sleeve is **unverifiable but directionally positive** given the capital curve, though entries are frequently vibes-based ("seems to be ripping") rather than rule-based. Expectancy on the thematic small-cap catalyst chases is **unknown/likely mixed** — no full round-trip P&L is ever disclosed for LUNR/ASTS/PL/OKLO specifically, only that he "made bank" in aggregate. **Net assessment: real, positive, moderate expectancy on the core LEAPS mechanic; treat the rest of the book as directionally informative but not independently tradable.**

### 5.3 Signal Flow Ingestion Matrix

| Signal Type | Source Posts | Raw Reliability | Recommended Artemis Treatment | Weight |
|---|---|---|---|---|
| Discount-window LEAPS entries on quality names (HIMS/NVDA/HOOD), later exercised into shares | ~8 posts | Medium-High (repeated, verified realized gains across 18+ months) | **INGEST the mechanic** — screen for genuine oversold-quality setups (independently defined, not his "vibes"), size as a defined-risk options entry, do not automatically inherit his "exercise into shares" step (see Exit Rules) | 0.5 |
| Short-duration HOOD/SPY/NVDA swing calls with morning-setup + quick-TP rule | ~15 posts | Medium (disciplined exit rule post-2025; entries largely narrative) | **INGEST the exit discipline** (TP at ~90%+ of realized move, no diamond-handing) as a standalone rule applicable to Artemis's own positions; do not inherit his entries | 0.3 |
| Space/satellite/gov-contract thematic basket ("next $ASTS" pattern) | ~10 posts | Low-Medium (real catalysts, thin DD, pattern-matching heuristic) | **INGEST as universe-discovery seed only** — verify contract awards/fundamentals independently before any allocation | 0.2 |
| Community-copied calls (named OA squad, e.g. Allie's AAPL DeepSeek-dip call) | ~6 posts | Medium (he applies a partial filter before acting) | **DO NOT ingest directly** — treat the underlying multi-trader consensus as a crowd-sentiment tell only | 0.1, sentiment-monitor only |
| "Buy the dip / discount season" reflex on every red day | ~10 posts | Regime-dependent (worked in the 2024–2026 melt-up sample; untested in a real bear market) | **FADE or DISCARD outside a confirmed uptrend regime**; his own April 2025 tariff-crash dip-calls were premature by weeks | -0.3 outside confirmed uptrend, +0.2 inside one |
| Occupational-domain conviction (Figma/$FIG as a working product designer) | 3 posts | Medium (genuine domain expertise, single name, unverifiable insider content) | **INGEST as a qualitative conviction multiplier** only for names where a poster has demonstrable professional domain expertise | 0.2, single-name only |
| Self-tagged `[Gain]`/`[Loss]` ratio (35:2) | 154 posts | Very Low as a P&L ledger (94.6% self-reported win rate) | **DISCARD as a literal win-rate metric**; treat only as evidence of strong self-report bias | 0.0 |
| `amount_k` capital trajectory | 154 data points, 4 flagged as a sync-outage artifact | Medium-High outside the flagged window (one 1099-corroborated data point) | **INGEST as the primary track-record verification signal**; exclude 2025-09-10→2025-10-11 readings entirely | monitor + weight 0.4 |
| Margin call / leverage decisions | 1 post | None (no sizing logic disclosed) | **BLACKLIST** — never inherit sizing or leverage from this account | 0.0 |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Harvest the **discount-window LEAPS mechanic** on quality growth names as a screenable pattern (deep pullback + fundamentally sound name + catalyst on the calendar), independently re-scored — his own "discount season" trigger is vibes-based, not a real oversold filter.
2. Harvest the **mechanical take-profit rule** (exit at ~90%+ of realized move, never diamond-hand a short-dated option) as a standalone exit policy applicable across Artemis's own options book, regardless of source.
3. Seed the **small-cap thematic screener** (space/satellite/nuclear/gov-contract names) from his ticker mentions, but require independent contract/fundamental verification before any position sizing — his DD depth on these names is consistently thin.
4. Weight single-name conviction upward, modestly, when a poster (like this one, a working product designer) demonstrates genuine professional domain expertise in the sector of the call.

**Contrarian Fade Directives (when to fade him / the retail herd he represents):**
1. Fade clusters of high rocket/moon-emoji, "we only go up," blow-off-top language — these cluster near local tops in this archive (Oct 2024, Jun–Jul 2025) and are a useful retail-euphoria contrarian tell.
2. Fade "buy the dip / discount season" calls specifically when they appear during a *structural* macro break (tariff/geopolitical shock) rather than routine chop — his own dip-calls during the April 2025 crash were early by 2–4 weeks.
3. Treat his self-tagged 94.6% "Gain" ratio as a sentiment/selection-bias artifact, not a real win rate — never size confidence in this account based on his own tagging.

**Mandatory Risk Blacklists & Firewalls:**
1. **Blacklist sizing/leverage inheritance entirely** — the account's one disclosed risk-control failure (March 2025 margin call) has no accompanying pre-trade sizing rule to learn from.
2. **Firewall the 2025-09-10 → 2025-10-11 `amount_k` readings** ($2.78K–$4.27K) from all trend and drawdown calculations — confirmed brokerage-sync outage, not a real capital event.
3. **Hard-blacklist the meme-coin/hype-instrument class** (TRUMP/MELANIA inauguration coin YOLO) — a single, self-tagged `[Yolo]` pure-gambling impulse with zero repeatable structure.
4. **Do not treat his self-built "Diamondhands" auto-trading bot** (2026) as a validated signal source — a single disclosed $14 trade result is statistically meaningless.
5. Do not inherit his **"exercise into shares"** behavior wholesale — it is how a well-defined-risk option (Unity, 2024) turned into an undefined-risk long-equity bagholding position that then round-tripped from $50 to $13.

**Exit Rules & Alpha Rectification:**
1. Any position sourced from his LEAPS-mechanic or thematic-catalyst ideas should carry Artemis's own hard invalidation level and trailing-stop logic from initiation — never inherit the "hold and hope for exercise" default.
2. Apply the harvested take-profit rule (≥90% of expected move → close) mechanically on any option position, independent of source.
3. Re-score the thematic small-cap basket quarterly; if "next $X" pattern-matched names show no fundamental follow-through (contract awards, revenue), downgrade the feed's freshness weight toward zero.
4. Treat a posting-cadence collapse to <1 post/month lasting 60+ days as a **data-availability flag requiring cross-verification**, not a tilt/blow-up kill-switch — in this account cadence gaps map to disclosed health events and job changes, not capital stress, unlike the pattern typically associated with account distress in this cohort.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone | Capital Context | Notes |
|---|---|---|---|
| 2024-05-28 | Archive begins | $23.6K | Already grown from a stated $200 (Nov 2023); options trading since Feb 2024 |
| 2024-06-06 | **First documented greed-loss**: NVDA call round-trips $7K→$3K in value for not selling into strength | ~$25-30K | Formative lesson later cited as the origin of his take-profit discipline |
| 2024-10-10 | "$200 in November to 40k" milestone | $37.4K | First major public track-record post |
| 2024-10-16 | Robinhood "Legend" desktop platform launch, "Hoodchella" event | $38-39K | First of several HOOD product-launch trades |
| 2024-11-15 | Establishes Unity ($U) short thesis (ATH $50 → then-current ~$13-20) | $58.6K | Later becomes the account's clearest bagholding case study |
| 2024-12-19 | "Happy camper — EOY report, 200 → 70K+" | $77.9K | Names the full OA mentor squad for the first time |
| 2025-01-20 | Meme-coin YOLO: buys $TRUMP/$MELANIA on inauguration hype | $83.2K | Only pure-gambling instrument in the archive, self-tagged `[Yolo]` |
| 2025-01-24 | Long-form essay on trading mental health, "you are not the exit liquidity" | $88.5K | Most substantive non-trade post in the archive; explicit anti-gambling-addiction messaging |
| 2025-01-27 | DeepSeek-news market shock; cites Allie's AAPL dip-buy call, discloses following it after independent verification | $83-86K | Best-documented example of filtered (not blind) community signal-following |
| **2025-02-14** | **"100K gang" milestone**, discloses 1099 figures: $89K net 2024 trading profit, $8.4K losses | **$100.4K (ATH #1)** | The one tax-document-corroborated number in the whole archive |
| **2025-03-18** | **Margin call** | $85.1K | Only disclosed leverage-control failure; no sizing rule ever attached |
| 2025-04-02 to 04-09 | Trump tariff crash: shorts SPY ("Spoils of War") while also calling premature "buy the dip" bottoms | $75.8-83K | Mixed adaptive (shorting) / non-adaptive (early dip-calls) response |
| 2025-04-21 | Explicitly steps back from active trading, cites excess volatility | ~$78K | Self-aware risk-avoidance, not forced by losses |
| 2025-06-04 | Codifies take-profit discipline ("don't diamond hand... 94% TP, take the win") | $97.5K | Direct behavioral fix traced back to the June 2024 lesson |
| 2025-07-12 | "+25k : 3M" milestone, discloses systematic rule: 2-5 trades/week, $250/wk recurring DCA into SPY/HOOD/NVDA/ULTY | $127.7K | Most mechanically explicit trading-rule post in the archive |
| **2025-09-21** | **Clean-series all-time high** | **$149.6K** | Last reading before the sync-outage window |
| 2025-09-10 to 10-11 | **Data-integrity gap** — readings collapse to $2.78-4.27K with no loss narrative, self-reported as an app/brokerage sync failure | *Excluded* | Do not treat as a real drawdown |
| 2025-07-31 | Hospitalized (blood clot, sepsis-causing pressure wound); discloses being paralyzed | n/a | Explains the reduced back-half posting cadence going forward |
| 2025-11-19 | Capital tracking resumes normally | $104.4K | Confirms the outage was a data artifact, not a real 97% loss |
| 2025-12-04 to 2026-01-15 | ASTS/PL/OKLO space-sector rally, multiple `[Gain]`-tagged posts | $107-123K | Peak period for the thematic small-cap catalyst-chasing pattern |
| 2025-12-29 | Finishes ~2-month, 3x-daily infusion regimen; starts new job at an AI company | $116.0K | Health/career context for cadence, not capital stress |
| 2026-01-09 | "Across all my brokerages I'm up 100k+" — clarifies the tracked account is a subset of broader net worth | $121.9K | Important scope caveat for the whole capital series |
| 2026-03-17 | States he "doesn't trade options anymore," shifts to pure investing | $105.1K | Marks the effective end of the options-trading era in the archive |
| **2026-06-05** | **Clean-series post-outage high** | **$142.9K** | Also discloses building "Diamondhands," a personal Robinhood-MCP auto-trading CLI |
| 2026-06-15 | First (only) disclosed auto-bot trade result: +$14 | $136.5K | Statistically negligible, hobby-stage project |
| 2026-08-11 | Archive ends | $133.3K | Self-described "lurker," pivoting to stable-income names (XOM, CAT, FedEx, WM) and cash-stacking for anticipated IPOs |

---

*End of dossier. Source data: `/home/mpha/artemis/afterhour/reports/posts/@internetdialup_lifetime.md`, `/home/mpha/artemis/afterhour/data/following/@internetdialup_all_posts.json`.*
