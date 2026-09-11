# Forensic Quant Autopsy: @ALLOY

**Subject:** AfterHour trader `@ALLOY` (`prf_c6537c7ac3d94bbbac7dc975bc263081`)
**Rank:** #5 most-active followed trader — 2,139 lifetime posts
**Coverage:** 2024-11-13 → 2026-09-06 (662 days / ~94.6 weeks / ~21.8 months)
**Sources:** `@ALLOY_lifetime.md` (full text, 2,139 posts), `@ALLOY_all_posts.json` (structured metadata: `tag`, `gain_loss`, `amount_k`, `tickers`, engagement)
**Analyst:** Artemis Engine — Sonnet dossier pass
**Methodology note:** the `amount_k` field is **not usable** as an equity curve for this trader — it carries a real, nonzero value in only 10 of 2,139 posts, all clustered in a 3-day window at account creation (2024-11-18 to 2024-11-21, values $62.4K–$63.5K), and is never populated again. Every capital figure in this dossier is therefore drawn from his own **self-reported, self-selected** narrative posts (the "Challenge Account" thread, follower-milestone posts, screenshots described in text). Treat dollar and percentage figures as directionally informative and internally consistent with his own story, not independently audited. This caveat matters more for @ALLOY than for any other profile in this cohort, because — as demonstrated in §3 and §4 below — he discloses losses in only **0.8% of posts**, making the archive itself a curated highlight reel rather than a full ledger.

---

## 1. Executive Profile

### Who he is
A self-described former **machine learning / quantitative-risk engineer** (per his own long-form origin story, Post #1399, 2026-01-13): a decade-plus of trading and investing, two prior startups, "many data scientist and machine learning researcher positions... at Fortune 100s," and equity from a technical-founder role at a "military/defense startup." The single most load-bearing biographical claim in the entire archive: **"At 25 I was mentored by Cem Karsan"** — a real, well-known institutional volatility/options-flow strategist (founder of Kai Volatility Advisors, a leading public voice on dealer gamma positioning). Whether or not the mentorship claim is independently verifiable, it is consistent with his output: @ALLOY is the only trader in this cohort whose core methodology is a genuine, technically coherent **dealer-gamma / GEX / open-interest positioning framework**, not chart pattern-matching or vibes. He is married with a young daughter, frames his trading as the vehicle that solved a real financial-precarity period in his 20s (his wife's cancer diagnosis, dropping out of college twice), and self-identifies explicitly as the "all caps," "flippant," "sometimes offensive" persona that is his public brand.

### Trading philosophy
Two philosophies running in parallel, and the tension between them is the central fact of this profile:
1. **A genuine, teachable, mechanically stated intraday framework** built on SPY/SPX dealer positioning — gamma flip levels, GEX sign (positive/negative dealer gamma), open-interest "walls," IV term structure, and time-of-day volatility windows. This is documented explicitly in structured, non-meme posts: the **"PRISM Day Trading Guide"** (Post #1209, 2025-11-22) breaks the trading day into four regimes (9:30–10:15 high-vol OTM window, 10:15–1:30 low-vol ATM decay zone, 1:30–2:00 transition, 2:00–4:00 high-vol/high-theta convexity zone) with explicit strike-selection rules for each. Multiple earlier "Dd"-tagged posts (e.g., the 2025-05-15 macro-event playbook) go further, publishing full quant-report tables with named metrics — **IV Ratio, GEX Ratio, OI Ratio, Fragility Score, Gamma Flip level** — organized into time-windowed trade structures with stops.
2. **A monetized influencer/content-creator operation** built on top of that framework, called **Prism** — starting as a personal modeling tool, opened to beta users (Feb 2025), converted into a $50/mo Discord (Jun 2025), and expanded into tiered "consulting" packages, merch, and (as of Sept 2026) a fully automated, timestamped daily SPY dealer-positioning report auto-posted to the public feed (`Generated: 2026-09-04 09:30:07 ET`, complete with GEX sign, OI walls, IV term structure, bull/bear intraday setups). **This is the most important classification fact in this dossier: @ALLOY is not primarily a trader posting his trades — he is a signal-and-software vendor whose public AfterHour feed functions as top-of-funnel marketing for a paid product**, layered underneath what is, when isolated from the sales copy, a legitimate and internally consistent gamma-positioning trading system.

### Post cadence
- **Overall average: 2,139 posts / 94.6 weeks ≈ 22.6 posts/week** — by a wide margin the highest-frequency, most content-creator-shaped cadence reviewed in this cohort to date (roughly 7x the cadence of a typical peer profile).
- **Volume bursts, not steady-state:** Feb–Mar 2025 (166, 161 posts — the Prism beta launch + $1M call + growth-hacking follower-milestone posts), Oct–Dec 2025 (147, 193, 126 — the run-up to the "Challenge Account" story), Jan–Mar 2026 (129, 119, 117 — the Challenge Account peak and its quiet fade), Jun–Jul 2026 (115, 144 — renewed macro-content push).
- **Cadence troughs correlate with life events and product-building, not losses:** Apr 2025 (96, but avg. post length collapses to 148 chars — quick hits only), Apr 2026 (43) and Aug 2026 (49) are his quietest months; nothing in the text explains these as drawdown-driven silence (contrast with the browndog pattern in this cohort, where cadence tracked account destruction) — they read as normal content-calendar troughs for an active commercial operator.
- **Post-length arc mirrors a strategic pivot:** average body length is short and punchy for most of the archive (131–320 characters/post most months) but **spikes to 1,738 characters/post in the final month (Sept 2026, n=8)** as he shifts to publishing fully automated, data-dense daily dealer-positioning reports — a real, recent, and probably durable format change worth monitoring going forward.
- **Posting rhythm tracks market hours tightly**: post timestamps cluster 13:00–22:00 UTC (roughly 8:30 AM–6:00 PM ET), consistent with live, real-time market commentary rather than batched/scheduled posting; only ~11.6% of posts fall on a weekend.

### Verified capital trajectory & drawdown history
No continuous, platform-verified equity curve exists (see methodology note above). What *is* documented, consistently and in detail across dozens of posts, is a single narrated account — the **"Challenge Account"** — that constitutes his best, most complete self-reported track record in the archive:

| Date | Reported Value | Notes |
|---|---|---|
| 2025-12-12 | **$10,000** | Stated start date of the Challenge Account (referenced retroactively) |
| 2025-12-19 | ~$21,000 | "10K now at 21K in 2.5 weeks" (Post #1314) |
| 2026-01-20 | **$75,000** | "10K->75K since Dec. 12 2025" (Post #1439) — +650% in ~5.5 weeks |
| 2026-01-27 | ~$60,000 | Pullback from the Jan 20 peak — "10K->60K 40 days" (Post #1476) |
| 2026-01-30 | ~$80,000 | Recovery — "10K->80K 45 days" (Post #1493) |
| 2026-01-31 | **$109,000** (from $81K that morning) | "Think I am done" (Post #1495) — single-day +34% swing on the account |
| 2026-02-02 | Withdrew **$50,000** | De-risking move — first and only disclosed profit-taking of size on this account |
| 2026-02-06 | ~$1,000 allocated to BTC | "Up 1200% in ~50 days" self-reported cumulative return since Dec 12 |
| 2026-02-23 | Still active (options positions referenced) | **Last dated reference to the Challenge Account in the archive** |

**Interpretation — a real, large, and *unresolved* result:** taking the narrative at face value, this is a genuinely exceptional short-term trading result: **$10K → $109K (+990%) in seven weeks**, followed by a partial, disciplined withdrawal ($50K, roughly the original stake plus a chunk of profit). That withdrawal is the single best piece of risk-management evidence anywhere in this dossier. But the thread then **simply stops** — no final wrap-up post, no year-end reconciliation, no explicit "here's what happened to the remaining ~$59K." Given the base-rate finding in §3 (98.4% of tagged posts are "Gain," only 0.8% are "Loss"), the most defensible reading is that this storyline was abandoned rather than concluded — consistent with a pattern (also visible in the abandoned "I will make $1M this year" claim from Feb 2025, never revisited by year-end) of **narrative threads disappearing quietly when they stop being flattering, rather than being closed out with a result.** Artemis should treat the $10K→$109K figure as a real, striking data point about his skill ceiling under favorable conditions, and simultaneously treat its unexplained disappearance as a hard behavioral tell about selection bias in everything else he reports.

---

## 2. Ticker Universe & Catalysts

### Core assets (3,026 total ticker mentions across 2,139 posts, 406 distinct tickers, 83.3% of posts carry at least one ticker tag)

| Ticker/Bucket | Mentions | Role |
|---|---|---|
| **$SPY** | 1,438 (47.5% of all ticker mentions) | Overwhelmingly his primary vehicle — 0DTE/weekly options traded against GEX/gamma-flip levels |
| **$QQQ** | 304 | Secondary index vehicle, same methodology |
| **Index/vol bucket (SPY+QQQ+IWM+SPX+VXX+UVXY+TLT)** | 1,876 (**62.0%** of all ticker mentions) | Confirms this is fundamentally an **index-derivatives, dealer-positioning book**, not a stock-picker's book |
| $SLV, $GLD, $USO | 51, 37, 18 | Commodity/macro-hedge sleeve (metals + energy), tied to his inflation/debasement macro thesis |
| $HOOD | 48 | Dual role — a trading vehicle (options) *and* his disclosed primary broker (Robinhood); source of at least one documented execution-error loss |
| $NVDA, $MSFT, $AMZN, $AAPL, $AMD, $GOOGL, $META, $ORCL, $PLTR, $TSLA | 14–35 each | Mega-cap/AI basket — earnings and macro-narrative driven, not core holdings |
| $LB, $SERV, $ACHR, $KULR, $RIVN, $PTON, $LUNR, $HIMS | 8–21 each | A recurring small-cap/momentum basket from the account's earliest days (Nov–Dec 2024) — his "shitposting" era tickers, largely abandoned as the account matures into the index-options/macro format |
| $ONDS, $OKLO, $SMR, $URA | 7–13 each | Defense/nuclear-energy thematic sleeve — long-duration, narrative-driven, low post-frequency but recurring |
| $BTC | 15 | Small allocation inside the Challenge Account, opportunistic dip-buy framing |

**406 distinct tickers with a long tail of 1-2 mention names** shows genuine broad market-scanning (DD-style posts touch many names), but the *trading* activity is concentrated almost entirely in SPY/QQQ options.

### Options vs. equities vs. macro/technical drivers
Predominantly **index-options, positioning-model-driven**, layered with three distinct catalyst types:
1. **Dealer-gamma/GEX mechanics** — the dominant, differentiated driver. Gamma flip level mentioned 35 times, "GEX" 96 times, "order flow" 51 times, put/call walls referenced explicitly. His entries are pinned to specific numeric levels (e.g., "602 is meaningful support... if buyers don't show up on order flow (Prism) then 598 is possible") rather than generic chart patterns.
2. **Macro/geopolitical event-timing** — Fed decisions, NFP/CPI prints, and (his single highest-engagement post ever, 235 reactions/339 comments) a sweeping geopolitical thesis connecting a Venezuela/Maduro headline to oil, Taiwan semiconductor risk, and multi-year positioning ("This Is Not About Oil. Oil Is The Excuse," Post #1393, 2026-01-03). These posts are long, well-written, and genuinely interesting reads — but resolve into vague, multi-year, largely unfalsifiable "trade implications" ("long energy infrastructure," "long Japan reshoring") rather than sized, dated trades.
3. **Options mechanics literacy is real but shallow beyond directional plays**: "call"/"put" appear 269/170 times, "strike" 92 times, but multi-leg structures are thin (straddle 14, strangle 9, spread 27, iron condor 4, CSP only 2, LEAPS only 5) — this is a **directional/short-premium 0DTE operator**, not a spreads-and-hedges options engineer, despite the sophisticated positioning *analysis* layered on top.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags?
The honest answer, given the data available, is **we cannot fully tell — and that itself is the finding.** The archive is structurally incapable of answering this question fairly:

| Tag | Count | % of tagged posts | Avg. reactions |
|---|---|---|---|
| `Gain` | 1,031 | 60.6% (98.4% of Gain+Loss posts) | 10.4 (lowest of any content tag) |
| `Loss` | 17 | 1.0% (1.6% of Gain+Loss posts) | 14.1 |
| `Dd` (analysis) | 509 | 29.9% | 18.7 |
| `Funny` | 194 | 11.4% | 19.1 |
| `Discuss` | 164 | 9.6% | 18.0 |
| `Contest` (giveaways) | 41 | 2.4% | 22.5 (highest) |

**A 61:1 Gain-to-Loss posting ratio is not a plausible reflection of any real trader's win rate on 0DTE index options** — it is a curated highlight reel. Two of his 17 loss posts are explicitly **prompted by followers calling him out** ("SHOW US THE LOSERS," Post #1136, Nov 2025; "ALLOY, SHOW UR LOSERS," Post #1588, Feb 2026) — meaning the visibility of losses in this archive is a function of audience pressure, not his own disclosure instinct. Note also that his `Gain`-tagged posts carry his *lowest* average engagement of any content category, while his analysis, jokes, and giveaways out-perform his brag posts — his audience is not primarily there to copy-trade his fills.

### How he manages losing positions
Genuine risk-management evidence exists, but is thin and self-selected:
- **The one clean, disciplined example:** the Challenge Account $50K withdrawal after a run to $109K (Feb 2026) — real profit-taking at size, the strongest piece of process evidence in the dossier.
- **The one disclosed execution failure:** a fat-fingered Robinhood order (bought a put meaning to buy a call) turned a "100% day into a measly 90% day" (Post #1588) — a mechanical/UX error, not a thesis failure, and notably reframed as still a big win.
- **No disclosed stop-loss discipline, position-sizing framework, or max-loss-per-trade rule appears anywhere in the archive** — striking, given how quantitatively literate his market-structure analysis is. The "Fragility Score"/GEX-table posts *include* stop guidance as advice to followers ("hard stops... stop out if underlying moves >1.5–2 points from short strike") but there is no evidence he narrates his own adherence to it.
- **The "I Was Wrong" post (Post #1610, 2026-02-26)** is the single most self-aware piece of writing in the archive: a public macro call (an Iran peace deal "within 2-3 weeks") that didn't materialize, met with a genuine, un-hedged "I am sorry to those I hurt. I will do better next time" — followed immediately by an acknowledgment that if the deal *does* happen late he'll "brag relentlessly" about it. This is honest in the moment but reveals the underlying incentive structure: outcomes get narrated when they're flattering, on a lag if necessary, and dropped if they simply don't resolve favorably.

### Documented wins vs. blow-ups

| Category | Evidence |
|---|---|
| **Best documented win** | Challenge Account: $10K → $109K in 7 weeks (Dec 2025–Jan 2026), +990%, with a genuine $50K withdrawal — his single best, most detailed, most internally-consistent result |
| **Best process evidence** | The PRISM Day Trading Guide and the GEX/Fragility-Score playbooks — mechanically sound, teachable, hedged with explicit stop guidance for followers |
| **Best "pure alpha" claim** | "Prism community made over 100K collectively just today" (undated aggregate claim, unverifiable, but consistent in tone with the rest of the promotional material) |
| **Only disclosed blow-up-adjacent event** | None found at position-level; the closest is the unexplained fade-out of the Challenge Account after Feb 23, 2026, and the quiet abandonment of the "$1M this year" claim from Feb 2025 |
| **Only disclosed hard loss** | The Robinhood fat-finger error (~$150 lost inside a much larger winning day) |

**Bottom line:** this trader almost certainly has genuine, above-average skill in short-dated SPY/QQQ options timed to dealer-gamma structure — the Challenge Account result and the mechanical sophistication of his GEX playbooks are hard to fake convincingly and consistently for 22 months. But the **archive itself is not designed to let anyone verify a real win rate or expectancy** — it is optimized for engagement and Prism conversion, and its own internal ratios (98.4% gain-tagged, narrative threads that vanish rather than resolve) are the strongest evidence of that design.

---

## 4. Behavioral & Sentiment Signals

### Why is he posting?
Three motives, and unlike most peer profiles in this cohort, they are **commercially organized, not incidental**:
1. **Top-of-funnel marketing for Prism** — the paid Discord/software product is referenced directly or indirectly in a large share of his highest-engagement posts (giveaways, "ask me about Prism while it's still in beta," "do u have Prism?," follower-milestone data-dump promises). The monetization arc is explicit and traceable: personal tool (undated, pre-archive) → public beta tease (Feb 2025) → $50/mo Discord with artificial scarcity — capped at 25 signups, Nintendo Switch giveaway (Jun 2025) → tiered consulting add-ons (Jun 2025 onward) → fully automated public daily reports as a taste of the paid product (Sept 2026).
2. **Genuine market-structure content and community-building** — the "Dd" tag (509 posts, 23.8% of the archive) is real, often technically dense, and consistently his second-most-engaged content category. This is not pure grift; there is substantive, teachable material here.
3. **Persona maintenance / parasocial brand-building** — recurring taglines ("END TRANSMISSION ❤️" x20, "GODSPEED" x12), heavy emoji signaling (💎 appears 102 times — his personal/Prism brand icon; 🚨 31 times), and a long-form origin-story post (Post #1399) that is pure brand-humanizing content, deployed strategically at a follower milestone.

### Recurring linguistic patterns
- **ALL CAPS as the default register** for nearly the entire archive — a stylistic choice he names and owns explicitly ("I type in all caps, I make jokes, I'm flippant... I'm very good at trading... I'm not afraid to rub it in anyone's face").
- **Anti-guru framing used to sell his own guru product** — "NEVER PAY FOR SIGNALS... I give the levels out for free... 'CAUSE I MAKE MONEY FROM THEM TOO" (Post #261, Feb 2025) is posted the *same day* he is actively driving signups to the Prism Discord beta launch (Post #260, hours earlier). He also explicitly warns followers off "FURUs" (fake gurus) twice while running his own paid membership funnel — this is not necessarily bad-faith (the free levels genuinely are free; Prism is sold as *tooling*, not "signals") but it is a real tension worth flagging.
- **Confidence is performative and load-bearing for the brand** — "I WILL MAKE 1 MILLION THIS YEAR" (Feb 2025), "I DON'T PLAN TO GO ANYWHERE BUT UP," and a bio literally framed as "the journey from 10K -> 1M" (Post #4, the account's fourth-ever post) — big, round, unfalsifiable-on-any-fixed-timeline numbers used as hooks.
- **Rare, notable moments of real vulnerability** — the origin story (illness, poverty, dropping out of college twice, his wife's cancer) and the "I Was Wrong" post are genuinely unguarded by comparison to his default register, and both landed among his highest-engagement content — his audience visibly rewards authenticity more than bragging (consistent with the Gain-tag engagement finding in §3).
- **Profanity is essentially absent** (5 case-insensitive hits for "fuck" in 2,139 posts) — a sharp contrast to venting-heavy peer profiles in this cohort; his tone is confident/declarative rather than emotionally reactive even under pressure.

### Reaction to volatility / red days
- **Market-structure red days are treated as pure information, not threat** — his framework explicitly *wants* volatility (the "2:00–4:00 PM high-vol/high-theta convexity zone" is presented as the day's best opportunity window, not something to fear).
- **Being publicly wrong is handled candidly but briefly** — the "I Was Wrong" post is honest in tone but short, and is not followed by a visible pattern of ongoing accountability tracking (no "how did that Iran call resolve" follow-up was found).
- **Platform/broker-level volatility (a Robinhood outage) is treated as a community-wide warning**, not a personal complaint ("RH Users Warning," Post #695) — consistent with his self-appointed role as a community resource, not just a solo trader.

### Engagement profile
Average reactions/comments are meaningfully higher than most peer profiles in this cohort and are **inversely weighted toward analysis and community content over bragging**: `Contest` (giveaways) posts average 22.5 reactions, `Funny` 19.1, `Dd` 18.7, `Discuss` 18.0 — all outperforming `Gain` posts (10.4 avg). His three highest-engagement posts of all time are a geopolitical macro essay (235 reactions/339 comments), his personal origin-story reveal (161/161), and a "100 likes for a market-health timeline" engagement-bait Dd post (150 reactions/2,962 views) — **his audience is buying the analyst and the person, not the trade alerts.**

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

**Primary:** `GEX_POSITIONING_OPERATOR` — a genuinely coherent, mechanically documented SPY/QQQ 0DTE-and-weekly options approach built on dealer-gamma sign, gamma-flip levels, open-interest walls, and time-of-day volatility regimes. The most technically legitimate options-flow methodology reviewed in this cohort to date.

**Secondary:** `SIGNAL_VENDOR_GURU` — the public feed is demonstrably structured as a marketing funnel for a paid product (Prism: $50/mo Discord, tiered consulting, and — as of Sept 2026 — automated public dashboard teasers). Content, cadence, and even the choice of which trades to narrate are shaped by monetization incentives, not neutral trade-journaling.

**Tertiary:** `MACRO_NARRATIVE_ENGAGEMENT_BAIT` — his highest-engagement content is long-form, unfalsifiable, multi-year geopolitical/macro theses ("This Is Not About Oil") that generate huge reach but resolve into vague, hard-to-size "trading implications" rather than dated, falsifiable calls.

**Watch tag:** `SURVIVORSHIP_CURATOR` — a 61:1 Gain:Loss post ratio, narrative threads (the $10K→$109K Challenge Account, the "$1M this year" pledge) that are dropped rather than resolved, and loss disclosures triggered mainly by follower callouts. Every dollar/percentage figure in this dossier should be read through this lens.

**Positive watch tag:** `AUTOMATED_DEALER_FLOW_DASHBOARD_EMERGING` — the Sept 2026 shift to fully automated, timestamped GEX/OI/IV daily reports is a real, recent capability upgrade (turning "Prism" from a personal tool into an actual productized data feed) worth re-scoring if it continues and scales.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 47 / 100**

Rationale:
- **+ (genuine, teachable methodology, ~22 pts):** the GEX/gamma-flip/OI-wall framework, the time-of-day volatility playbook, and the pedigree claim (Cem Karsan mentorship) are all internally consistent and technically literate in a way most retail-trader archives in this cohort are not. This is the single best "real methodology" case reviewed to date.
- **+ (one large, credible, and disciplined result, ~15 pts):** the Challenge Account's $10K→$109K run, capped by a genuine $50K withdrawal, is a concrete, dated, detailed result with an actual profit-taking action attached — rare in this cohort.
- **+ (high signal-to-noise on market-structure calls, ~5 pts):** GEX/OI/gamma-flip levels are specific, numeric, and timestamped — falsifiable in a way most sentiment-only posts are not.
- **− (severe survivorship/disclosure bias, ~25 pts):** a 98.4% self-reported win rate is not credible for any real 0DTE options book; the true expectancy of his personal trading is **unknowable** from this archive, and the unresolved disappearance of his best-documented account is a serious red flag for anyone tempted to size off his claims.
- **− (commercial incentive contamination, ~15 pts):** a meaningful share of post volume and timing is optimized for Prism conversion (giveaways, scarcity tactics, "ask me about Prism" calls-to-action embedded inside trade posts) rather than neutral trade documentation — his public feed is not a clean data source.
- **− (thin multi-leg options sophistication relative to the analytical layer, ~5 pts):** despite sophisticated *analysis*, his actual disclosed trade structures skew simple/directional (long calls/puts) with minimal spread/hedge construction — the mechanics of his execution lag the mechanics of his research.

**Expectancy: LIKELY POSITIVE on his core GEX-level/time-of-day methodology when applied with independent risk controls; UNKNOWABLE on his personally-reported trades** due to the extreme, structurally-incentivized survivorship bias in what gets posted. Treat the *framework* as the asset to extract, not his personal PnL claims.

### 5.3 Signal Flow Ingestion Matrix

| Post Signature | Underlying Signal Type | Reliability | Artemis Action |
|---|---|---|---|
| GEX/gamma-flip/OI-wall level calls with explicit numeric strikes (e.g., "602 support... 598 if order flow fails") | Dealer-positioning-derived support/resistance | Moderate-High — mechanically coherent, cross-checkable against Artemis's own GEX data | **INGEST** as a comparison/validation source against the Engine's own GEX module — flag material disagreements for review |
| Time-of-day volatility regime framework (9:30-10:15 OTM window, 10:15-1:30 ATM decay, 2:00-4:00 convexity zone) | Structural intraday options-timing rule | Moderate-High — internally consistent, teachable, not tied to his personal PnL claims | **INGEST** as a standing intraday execution-timing overlay, independent of any single trade call |
| Automated daily SPY dealer-positioning dashboards (GEX sign, OI walls, IV term structure — Sept 2026 format) | Productized quant data feed | Unproven (n=2 as of archive close) but format is promising | **WATCH-LIST** — monitor for continuation/scaling; if it persists, treat as a candidate low-cost cross-reference feed |
| "Gain"-tagged bragposts (dollar/percentage results, no methodology shown) | Curated highlight-reel PnL claim | Very Low — 98.4% of tagged outcomes are wins, a statistically implausible real win rate | **DO NOT INGEST as a performance signal; DO NOT size anything off self-reported % returns** |
| Macro/geopolitical narrative essays (e.g., Venezuela/oil, Taiwan-risk pieces) | Long-horizon, unfalsifiable macro thesis, high engagement | Low-for-trading, informative-for-sentiment | **LOG as retail-macro-narrative sentiment data; DO NOT translate directly into sized trades** |
| Prism/Discord promotional posts (giveaways, "ask me about Prism," consulting-tier announcements) | Commercial marketing content | N/A for trading signal | **IGNORE for signal**; useful only as a data point on retail signal-vendor monetization trends |
| The Challenge Account narrative arc ($10K→$109K→unexplained fade) | A single, detailed, but ultimately unresolved account-level result | Moderate (the documented portion is credible) but capped by the unresolved ending | **LOG as a positive skill-ceiling data point; do NOT treat as an ongoing, verified track record** |
| "I Was Wrong" / accountability posts | Rare self-corrective disclosure | Low sample, but genuine when it occurs | **WATCH-LIST** — an increase in the frequency of this post type would be a meaningful positive signal about disclosure quality improving |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Treat @ALLOY's **GEX sign, gamma-flip level, and OI-wall calls** as a candidate cross-validation input against Artemis's own dealer-positioning module — the methodology has real pedigree and internal consistency, and material disagreement between his numbers and the Engine's own is itself a useful anomaly flag.
2. Harvest the **time-of-day volatility regime framework** (OTM-favorable open, ATM-favorable midday chop, convexity-favorable close) as a standing execution-timing overlay for the Engine's own 0DTE/short-dated SPY logic — independent of anything he personally claims to have traded.
3. If the **automated daily dashboard format** (first seen Sept 2026) continues and scales, evaluate it as a low-cost, machine-readable third-party data feed worth ingesting directly rather than parsing from prose.

**Contrarian Fade Directives (when to fade him / the retail herd):**
1. **Never treat a "Gain"-tagged bragpost as evidence of a repeatable edge** — the 98.4% self-reported win rate is a curation artifact, not a performance statistic; use his gain posts only as retail-sentiment/crowd-positioning color.
2. **Treat unresolved narrative threads (a big account, a bold prediction) that simply stop being mentioned as an implicit "this went badly"** — the Challenge Account's silent fade after Feb 23, 2026 and the abandoned "$1M this year" pledge are the pattern to watch for; a sudden drop-off in updates on any of his named "big story" positions should be logged as a soft negative signal, not treated as neutral.
3. **Discount macro/geopolitical mega-theses for direct trade sizing** — they are his best engagement content and his weakest actionable content; fade the temptation to translate essay-length narrative into a position.

**Mandatory Risk Blacklists & Firewalls:**
1. **Never size any position off his self-reported dollar or percentage PnL** — no independent brokerage verification exists anywhere in the archive, and the disclosure bias is extreme and demonstrated.
2. **Firewall any signal sourced from a post that also contains Prism promotional content** (giveaways, "ask me about Prism," scarcity countdowns) — commercial incentive is actively present in that specific post and should not be treated as neutral trade documentation.
3. **Do not treat his post cadence as a market-volatility proxy** — his 22.6 posts/week average is driven by a content-creator publishing schedule and product-marketing cycles, not purely by market conditions.

**Exit Rules & Alpha Rectification:**
1. Any GEX-level or gamma-flip signal ingested from this account should carry the Engine's **own independently-derived stop and target levels** — his own playbooks (correctly) recommend hard stops for followers, but there is no visible evidence he consistently discloses hitting them himself.
2. If his automated dashboard format matures into a consistent, ongoing daily feed, **re-score this profile's Alpha Score upward** — a real, machine-generated, timestamped dealer-positioning feed with a track record would meaningfully change the risk/reliability calculus versus the current prose-based, curation-prone format.
3. Apply a **standing "unresolved narrative" audit rule**: whenever Artemis ingests a big, specific, dated claim from this account (an account balance, a macro prediction with a timeline), set a calendar check for the stated resolution date; if no resolution post appears, log it as a negative disclosure-quality data point rather than letting it silently expire.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone / Catalyst | Notes |
|---|---|---|
| 2024-11-13 | Archive opens: "2025 will be the year of..." ($EXAS/$TXG/$TWST/$RXRX/$CRSP) | Early-era shitposting/small-cap-basket format |
| 2024-11-15 | Bio positions the account as "the journey from 10K -> 1M" (Post #4) | The founding promotional hook for the entire archive — never explicitly resolved by year-end 2025 |
| 2024-11-18 to 11-21 | Only nonzero `amount_k` readings in the dataset (~$62-63K) | A stale account-linking snapshot, never updated again — not usable as an equity curve |
| 2024-12-21 | 1,000 followers | Start of a recurring "follower milestone → content/data-dump promise" growth-hacking pattern |
| 2025-01-18 | 2,000 followers | — |
| 2025-02-01 to 02-07 | 3,000–3,500 followers | Promises to publish IB/institutional Twitter lists; "Cat Face Reveal" persona content |
| 2025-02-08 | **"I WILL MAKE 1 MILLION THIS YEAR"** (Post #203) | Bold, unfalsifiable-on-a-fixed-date pledge; never explicitly revisited or reconciled later in the archive |
| 2025-02-21 | **Prism beta launches** via Discord invite, framed as "the best tool while it's still early" (Posts #258-260) | Same-day precursor to the "never pay for signals" post below |
| 2025-02-21/22 | **"NEVER PAY FOR SIGNALS"** post (Post #261) | Posted hours after actively driving Prism-beta signups — the archive's clearest tension between anti-guru branding and guru monetization |
| 2025-03-09 | 6,000 followers | — |
| 2025-05-14 | 7,000 followers; promises 1-year historical SPY options dataset | — |
| 2025-05-15 | First fully quantitative "Fragility Score / GEX Ratio / IV Ratio" playbook post appears | Shows the underlying Prism data engine already existed in usable form by mid-2025 |
| 2025-06-13 | **Prism converts to paid: $50/mo Discord**, capped at 25 signups, Nintendo Switch 2 giveaway | The formal monetization launch; consulting-tier add-ons introduced same week |
| 2025-11-22 | **"PRISM Day Trading Guide"** published (Post #1209) | His clearest, most teachable, most complete statement of trading methodology in the archive |
| 2025-12-06 | 10,000 followers | Growth had slowed sharply from the Q1 2025 pace (1K→7K in ~5 months vs. 7K→10K in ~7 months) |
| 2025-12-12 | **"Challenge Account" starts at $10,000** (retroactively dated) | Becomes the archive's single best documented trading result |
| 2026-01-03 | **"This Is Not About Oil. Oil Is The Excuse."** — highest-engagement post of the archive (235 reactions/339 comments) | Geopolitical macro essay (Venezuela/oil/Taiwan/semis); vague, long-horizon "trade implications," not sized calls |
| 2026-01-13 | **Origin-story reveal** ("The man behind the all-caps posts and Prism," Post #1399) — 2nd-highest engagement (161/161) | Discloses ML/quant background and the Cem Karsan mentorship claim; humanizes the brand at the 11K-follower mark |
| 2026-01-20 | Challenge Account hits **$75,000** (+650% since Dec 12) | — |
| 2026-01-31 | Challenge Account hits **$109,000** (from $81K that morning); "think I am done" | Peak of the documented run |
| 2026-02-02 | **Withdraws $50,000** from the Challenge Account | The single cleanest risk-management action in the entire dossier |
| 2026-02-06 | Allocates ~$1,000 to BTC inside the Challenge Account; claims +1,200% cumulative since Dec 12 | — |
| 2026-02-20 | "ALLOY, SHOW UR LOSERS" — a follower-prompted loss disclosure (a ~$150 Robinhood fat-finger error) | One of only 17 Loss-tagged posts in 2,139 |
| 2026-02-23 | **Last dated reference to the Challenge Account** | Thread ends without a wrap-up, final balance, or explanation — never revisited |
| 2026-02-26 | **"I Was Wrong"** — public accountability post on a failed Iran-peace-deal macro timeline call | The archive's most candid self-correction; still hedges with "if it happens late I'll brag relentlessly" |
| 2026-06-01 | "The List You Need To Outperform Markets For The Next 5 Years" ($CEG/$VST/$GEV/$ETN) — 5,300 views, his highest single-post view count | Long-duration energy-infrastructure thematic content |
| 2026-07-11 | "If This Gets 100 Likes I Will Share The Timeline For Risk And Market Health" — 3rd-highest engagement, engagement-bait format | Confirms the deliberate, gamified content strategy underlying his highest-reach posts |
| 2026-09-03 to 09-04 | **First fully automated, timestamped daily SPY dealer-positioning dashboard posts** (`Generated: [ET timestamp]`, GEX sign/OI walls/IV term structure/bull-bear setups) | A genuine format upgrade — Prism maturing from a personal tool into a productized, machine-generated public data feed |
| 2026-09-05 | Runs a giveaway, discovers a structural flaw in it, **publicly cancels it and refunds every purchase** same-day | A minor but real accountability data point — self-corrects when a commercial mechanism misfires |
| 2026-09-06 | **Archive closes** on a long-duration thematic call: "The more I learn and research $URA, the more I love nuclear for the next 10 years" | Ends on the same macro-thematic register the archive opened with, 22 months and 2,139 posts earlier |

---

*End of dossier. Prepared from `@ALLOY_lifetime.md` (2,139 posts, full text) and `@ALLOY_all_posts.json` (structured metadata) with no external data sources. All capital and percentage-return figures are self-reported by the subject and unverified against a brokerage statement or platform-captured account snapshot; the `amount_k` field, used successfully for capital-trajectory tracking in other profiles in this cohort, was not populated for this account beyond a 3-day window at account creation.*
