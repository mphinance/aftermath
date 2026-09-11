# Forensic Quant Autopsy: @Freeballer

**Subject:** AfterHour trader `@Freeballer` (`prf_7ec37131fbb8496f940c10cafc6dd1c7`)
**Rank:** #2 most-active followed trader — 2,517 lifetime posts
**Coverage:** 2025-02-13 → 2026-09-10 (574 days / ~82.0 weeks; account is effectively dormant until 2025-07, so the meaningful working window is ~62.3 weeks)
**Sources:** `@Freeballer_lifetime.md` (full text, 2,517 posts), `@Freeballer_all_posts.json` (structured metadata: `tag`, `gain_loss`, `amount_k`, `tickers`, engagement)
**Analyst:** Artemis Engine — Sonnet dossier pass

**Methodology note — the structured PnL fields are dead for this account.** `gain_loss` is an empty string on all 2,517 posts (0% populated). `amount_k` is populated on 1,813 posts (range $0.0003K–$9.74K) but shows **no usable correlation** with post content, dollar figures mentioned in text, view/reaction/comment counts (r = 0.09–0.31 across all tested pairs), or a coherent account-equity shape — unlike the `browndog` dossier in this cohort, where `amount_k` was a legitimate account-value snapshot, here it reads as scraper noise (values cluster by post *volume* period, not by trading outcome; e.g., May 2026 posts about a Silver-Bar-Giveaway winner and a James-Charles meme carry the archive's two highest `amount_k` values, 9.74). **This dossier therefore relies entirely on qualitative full-text mining** (545 posts carry an explicit `tickers` tag; 510 posts, 20.3%, contain at least one `$CASHTAG` in free text) plus a handful of late-archive posts where he voluntarily typed dollar P&L into the post body. Treat every dollar figure below as self-reported and unaudited.

---

## 1. Executive Profile

### Who he is
A Pittsburgh-area small-business entrepreneur (self-described serial hustler — "flipping mopeds and Civics in High School," casino nights, "tax write-offs") in his mid-to-late 20s/30s range (peer posts reference a 25-year-old trader as younger than him), college-educated locally ("Let's go Pittsburgh! To my college alma mater," Post 2025-10-11). Disclosed a genuine health scare in Dec 2025–Jan 2026: a 13mm×18mm lung nodule with a PET-scan SUV of 27, worked up between "a cancer hospital in Pittsburgh" and a second opinion at The James in Columbus — serious enough that when accused by a rival poster of faking it, he posted a video of his actual scan to prove it (2026-01-19: *"I hope this helps clear the air about my 'fake' cancer"*). This episode also triggered a public falling-out with a fellow creator (`@newfishbigpond`) over feeling unsupported during it (2026-01-18 post).

He is **not primarily a trade-caller — he is a platform community figure who also trades.** He co-founded and runs **Pathfinders**, a Discord trading community ("almost 300 members" by Jan 2026) that hosts live daily trading sessions and — his single most distinctive, repeatable behavior in this entire cohort — **arranged and conducted direct interviews with the CEO of a publicly-traded small-cap he was simultaneously promoting to his following**: Eric Brock of Ondas Holdings ($ONDS), twice (Jan 23, 2026 live webinar; a second round originally slated April 3, 2026). He also partnered directly with `@mphinance` on a Pathfinders podcast series, "Getting to Know You" (Jan 25, 2026 livestream).

### Trading philosophy
There is a real, if buried, trading philosophy underneath a mountain of community content: **short-dated SPY/SPX 0DTE and weekly options scalping, run on explicit, teachable rules**, layered under a **single-name evangelist relationship with $ONDS** and a running **anti-scam vigilante persona** that is, by raw word-frequency, his single most consistent content type in the archive. In his own words, his three-part identity:
1. **The 0DTE mechanic** — a genuinely competent, rules-based short-options trader who published detailed, correct trading mechanics essays: *"My Rules for $SPY 0 Days"* (2025-12-16: gamma risk on small moves, theta crush concentrated after 3PM, spreads blowing out late day, "never average down on 0DTE," "close winners fast," size down on red/low-VIX days) and a three-part "How to Trade $SPY" series covering fill-vs-screen-profit illusions, low-volume premium decay vs. scalping opportunity, and open-interest psychology (2025-12-16/22/24). This is the closest thing in the whole cohort to a documented, internally consistent day-trading edge.
2. **The $ONDS evangelist** — 141 mentions of $ONDS across the archive (the single highest ticker-mention count of any name, by any trader, in this cohort's raw ticker frequency), running from a small share position (Oct 2025) through a year-long promotional campaign that culminated in arranging two CEO webinars and naming it "Stock of the Year for 2025." He does disclose profit-taking along the way (2026-01-05: *"$ONDS I'm taking some profit"*; 2025-11-24: *"the take profit portion of this SNL skit has started"*), which distinguishes him from a pure bag-holder, but the CEO-interview arrangement is a structural promotional entanglement Artemis must treat as a conflict-of-interest signal, independent of his sincerity.
3. **The scam sentinel** — "scam"/"scammer" appears in **630 of 2,517 posts (25%)**, more than every ticker mention in the archive combined except $ONDS. He repeatedly and by name calls out pump-and-dump promoters (`@squeezekid` on $ORBS and $RXRX, `@NeverPullOver` on $BYND, fake-follower accounts, "300% in a day" screenshot flexers with no fill proof), positioning himself as the platform's self-appointed fraud watchdog — a genuinely useful, verifiable function distinct from his own trading.

### Post cadence
- **Raw average:** 2,517 posts / 82.0 weeks ≈ **30.7 posts/week**, but the account is essentially dormant Feb–Jun 2025 (21 posts total). From first sustained activity (July 2025) the real cadence is **2,496 posts / 62.3 weeks ≈ 40.1 posts/week** — by a wide margin the highest-frequency account reviewed in this cohort, roughly **12x** `browndog`'s 3.2/week.
- **Only 21.7% of posts (545/2,517) carry a structured ticker tag**, and only 20.3% contain any `$CASHTAG` at all in free text — meaning **nearly 4 in 5 of his posts are not about a trade in any form.** This is the single most important classification fact: as a raw signal source, this account is extremely low-density; an ingestion pipeline built to treat every post as a signal candidate will drown in banter, platform politics, and off-topic content.
- **Peak months:** Dec 2025 (272 posts) and Jan 2026 (280 posts) — coincides with the $ONDS CEO-interview arc and a viral health-scare/scam-fraud news cycle. **Cadence roughly triples his own baseline** during high-community-drama windows, not during his highest-conviction trading windows — cadence here tracks *community engagement*, not *market opportunity*, the opposite of a pure signal-generation account.
- **Viral growth inflection:** view counts jump from single/low-double digits (through April 2026) to consistently 500–3,000+ (May 2026 onward) — the account visibly "made it" on the platform mid-archive, likely on the back of the $ONDS/Pathfinders/CEO-interview arc, independent of trading track record.

### Verified capital trajectory & drawdown history
**No verified equity curve exists for this account** (see Methodology note above — both `gain_loss` and `amount_k` are unusable). The qualitative record instead shows:
- A **$500-to-$5,000 SPX/SPY day-trading "Challenge Account"**, launched 2026-05-14, tracked with mixed transparency: same-day post discloses a "**591 loser** this AM" alongside a claim the broader account is still net up.
- A **run of five consecutive positive SPX day-trading "receipts" posts** at the very end of the archive (2026-08-31 to 2026-09-02): +390, +732.36, +974.10, +340, +888.44 (then +658 on 2026-09-02) — his most disciplined, most numerically explicit trading stretch in the entire archive, but a five-to-six-day window is not a track record, and there is no visible loss disclosure in that specific stretch (survivorship risk: does he post losing SPX days as consistently as winning ones? Earlier in the archive, yes — 2026-05-12 "I was down 55% in an SPX call," 2026-05-18 "I lost today," 2026-05-14 "591 loser" — but the terminal-archive run is all green, which is exactly the kind of "recency-biased highlight reel" Artemis should discount).
- **$ONDS price arc** (his single largest position by attention, not necessarily by dollars): ~$6 (Oct 2025) → $8.35–8.86 (Nov 2025) → $9.55 (Dec 2025) → **$11.00 (Feb 18, 2026)** → **$12.15 peak (Mar 2, 2026)** → back down to consolidate **$9.90–10.10 (Aug 2026)**. Net: roughly **+65–100% off the entry zone over ~10 months**, but his own repeatedly-promised $15 (by Mar 21, 2026), $20, and "$25 by June 2026" targets **did not materialize** — the stock round-tripped from its March peak back to essentially the same level it was near a year earlier.
- **$CAT (Caterpillar)** — his single cleanest, most repeatable documented win, entered as a data-center-backup-power thematic call: **$575 (posted 2025-12-21) → $925 (2026-05-06) → over $1,000 (2026-06-22)** — a well-timed, well-reasoned fundamental call with a **~74% run** fully documented in near-real-time, with no counter-narrative or reversal in the archive.
- **$TSLA** — his "most emotional and strongest hold" (his words), publicly bullish to $500 from mid-2025, but he **sold his longest-standing position in October 2025** and published a full thesis-reversal post the same week ("Electric Elephant... No Longer 500 EOY," 2025-10-29) — one of the few genuinely self-correcting, well-timed exits in the archive (TSLA subsequently softened into year-end per his own later commentary).

---

## 2. Ticker Universe & Catalysts

### Core assets (ticker-field mention frequency, 545 tagged posts)

| Ticker | Mentions | Role |
|---|---|---|
| $ONDS | 141 | **The obsession/evangelist ticker.** Drone/defense small-cap. Cycles shares → profit-taking → renewed conviction, wrapped in a full promotional apparatus (Pathfinders CEO webinars, "Stock of the Year" declarations, merchandise "swag"). |
| $SPY | 112 | Primary day-trading/scalping vehicle — 0DTE and weekly options, EOD/EOY level calls, published trading-mechanics essays |
| $SPX | 30 | Secondary/complementary 0DTE index vehicle — becomes the **primary** day-trading vehicle in the final 2 months of the archive, with explicit dollar "receipts" |
| $BTC | 26 | Macro commentary and "prediction market" style calls, generally skeptical/bearish framing ("a wish in one hand and a fart in the other") |
| $TSLA | 22 | Long-held, high-emotion conviction name; sold Oct 2025 with a documented thesis reversal |
| $HIMS | 21 | Earnings-week IV/options plays, GLP-1 sector thematic commentary |
| $BYND | 20 | **Not his own trade** — almost entirely mockery/commentary on other posters' Beyond Meat pump calls, positioned as entertainment/scam-adjacent content rather than his own thesis |
| $ORBS | 19 | **Anti-scam target**, not a position — repeated public takedowns of the $ORBS pump-and-dump narrative and its chief promoter |
| $NVDA | 15 | Earnings/index-driver commentary, semis-sector macro framing |
| $HUBC | 12 | Meme/pump commentary on a micro-cap runner ("$HUBC 7,500 shares... don't miss the fuck out") — speculative, self-aware "retarded stuff" framing |
| $SPCX | 10 | Late-archive speculative/momentum commentary |
| $CAT | 5 | **His best documented directional call** — data-center backup-power thematic long, $575→$1,000+ |
| $GME, $MSTR, $NIO, $AAPL, $OPEN, $HOOD, $PLTR | 5–8 each | Rotating commentary names, mostly reactive/news-driven, mixed conviction |

**Only 20.3% of all posts (510/2,517) contain any ticker at all** — this is an overwhelmingly non-trading content stream. Of the ticker-tagged subset, a large share is not his own position but commentary on *other people's* trades (BYND, ORBS, HUBC, SPCX) — an important parsing distinction: Artemis must not treat "Freeballer mentioned $XYZ" as "Freeballer is trading $XYZ."

### Options vs. equities vs. macro/technical drivers
1. **Short-dated index options (SPY/SPX 0DTE/weekly)** — his most technically competent activity. Entries and exits are timed to intraday gamma/theta mechanics, volume regime (low-volume = bad for swings, good for disciplined scalps, per his own published rules), and level-based support/resistance (e.g., repeated $680/$690/$700 SPY "psychological level" theses through Dec 2025–Jan 2026).
2. **Single-name promotional conviction with a real fundamental hook** — $ONDS (drone/defense contract flow, Vanguard institutional buy-in, DJI import ban tailwind) is the clearest example: real catalysts exist, but the promotional apparatus around them (CEO interviews he personally arranged) inflates the signal beyond what the fundamentals alone would justify.
3. **Earnings-week IV plays** — $HIMS, $NVDA, $HOOD entries timed to earnings prints, with post-earnings follow-through commentary (mixed record; called $HIMS to $67 EOY in May 2026 off a $9-puts-crowd-was-wrong narrative — an unverified forward claim).
4. **Thematic/fundamental long calls** — $CAT (data-center backup power) is his cleanest, best-documented example of getting ahead of a real theme with a real multi-month payoff.
5. **Anti-scam commentary, not trading** — $ORBS, $RXRX, and a large share of $BYND content exist purely to warn his following away from other posters' promotional schemes, not to establish his own position.
6. **Macro/political overlay** — Fed-week, PDT-rule-change (a real, correctly-anticipated regulatory catalyst: he covered the June 4, 2026 PDT threshold cut from $25K to $2K well ahead of time with a genuinely well-reasoned small-cap-volatility thesis, flagging it as bullish for retail-driven squeezes and bearish for undercapitalized traders) and Trump-administration headline-risk framing recur constantly as color for his SPY/SPX calls.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags? A genuine mixed record, better-disclosed than most peers in this cohort
- **Explicit profit-taking disclosures exist and are dated**, unlike pure bag-holder profiles: $ONDS "taking some profit" (2026-01-05); "scalped back a bit and took profit on ONDS" ahead of a CEO interview (referenced retrospectively, 2026-02-17); "the take profit portion of this SNL skit has started" (2025-11-24).
- **But the $ONDS promotional targets consistently failed to land**: "$15 by March 21, 2026" (a public bet made 2025-12-30, never resolved/acknowledged in-archive), "$20," "$25 by June 2026" (2026-01-01 roadmap post) — the stock peaked at $12.15 in March and was back to ~$10 by August. He does not appear to publicly walk back these specific numeric targets the way he does for TSLA/SPY, which is a real accountability gap relative to his own stated standard ("I encourage people... to hold folks accountable," 2026-03-06).
- **Self-correction culture is real and better than peer average**: publicly declared himself wrong on TSLA $500 (Oct 2025) and on SPY 700 by EOY 2025 ("we didn't exceed 694... I was soft, brave, and showed ownership," 2026-03-06) — and explicitly calls out other creators who don't do the same. This is a genuinely positive behavioral trait Artemis should note as differentiating from the cohort's typical silent-failure pattern.

### How he manages losing positions
- **0DTE-specific rules are explicit and correct**: "never average down on 0DTE — time decay punishes bag-holding harder than stocks," "close winners fast," "size down on red days," "hold past midday rarely pays" (2025-12-16 rules post) — genuinely sound short-options risk management, rare to see spelled out this clearly by any trader in this cohort.
- **But he does not always follow his own rule** — 2026-05-12: *"I was down 55% in an SPX call... and then dollar cost averaged myself out and bought another one"* — an explicit, self-labeled "very sloppy" DCA-into-a-losing-0DTE move, directly contradicting his own published "never average down on 0DTE" rule from five months earlier.
- **No visible stop-loss discipline on $ONDS** — the position is managed by narrative and vibes ("I do not have a crystal ball... 8.86 was my support number... this is unknown and not traced for me at this point," 2026-02-05), not by a predefined risk level.

### Documented wins vs. blow-ups

| Category | Evidence |
|---|---|
| **Best documented wins** | $CAT thematic long, $575→$1,000+ (~74%) over ~6 months, fully time-stamped and never reversed; TSLA thesis-reversal exit (Oct 2025) ahead of a documented later softening; SPX day-trading receipts run, 2026-08-31→09-02 (+390, +732, +974, +340, +888, +658 — five to six consecutive documented positive days); correctly anticipated the June 2026 PDT rule change and its small-cap volatility implications weeks in advance |
| **Worst documented blow-ups / failures** | $ONDS promotional price targets ($15/$20/$25) never realized within their stated windows despite a full CEO-interview promotional campaign; SPX 0DTE DCA-into-a-loser directly violating his own stated rule (-55%+ before averaging down, 2026-05-12); $500→$5,000 challenge account disclosing a "$591 loser" morning (2026-05-14) with no resolution/close-out documented in-archive; no verified equity curve exists at all — every "win" in this table is self-reported and none is independently auditable |

**Bottom line:** this is a trader whose **documented options mechanics knowledge is genuinely above cohort average** (the SPY 0DTE rules essay and three-part "How to Trade SPY" series are teachable, correct, and specific), and whose **one clean fundamental call ($CAT) is a real, well-timed piece of alpha** — but whose **actual risk-management behavior does not consistently match his own stated rules**, whose **flagship promotional relationship ($ONDS) carries an undisclosed structural conflict of interest** (he personally arranged and monetized-in-attention two CEO interviews for a stock he was simultaneously telling his community to buy), and whose **PnL claims are entirely unverifiable** — no linked brokerage snapshot, no consistent loss disclosure cadence, and a suspiciously clean all-green streak in the final days of the archive.

---

## 4. Behavioral & Sentiment Signals

### Why is he posting?
Three motives, and unlike most peers in this cohort, they are **explicitly stated by him**, repeatedly:
1. **Community leadership / platform stewardship** — running Pathfinders, arranging CEO interviews, "Let's Make AfterHour Great Again" rally posts (2026-04-18), and an extended, self-justifying essay on why the platform "wouldn't be what it is today" without his anti-scam work (2026-03-14). This is his dominant, most time-consuming activity by post volume.
2. **Anti-fraud vigilantism** — 630 posts (25% of the archive) reference scams/scammers. He names names (`@squeezekid`, `@NeverPullOver`), publishes forensic-style rebuttals of pump theses (the 2026-01-06 $ORBS buyback-math takedown is genuinely rigorous — cash balance, share count, implied market cap math), and frames this as his primary value-add to the platform, more than his trading calls.
3. **Genuine trading education, secondarily** — the SPY/SPX mechanics essays are real, specific, and correct, but they are a minority of his output and arrive in bursts (a concentrated run in Dec 2025, another in Aug-Sep 2026) rather than a continuous practice.

### Recurring linguistic patterns
- **Profanity as a stylistic signature, not just emotional release** — "fuck" appears in 365 posts (14.5%), used constantly regardless of P&L outcome (winning and losing posts both), functioning as brand voice rather than a stress tell — this differs from peers where profanity spikes specifically on red days.
- **"Retard/retarded" as in-group slang** (35 posts, 1.4%) — used affectionately toward followers and self-deprecatingly, consistent with the account's crude-but-inclusive tone; a moderation/brand-risk flag for any downstream product surfacing his raw text.
- **"Have you heard about $ONDS" as a running bit** — repeated verbatim or near-verbatim at least 8 times across 10 months, evolving from sincere evangelism into self-aware meme, but never actually stopping — a genuine tell of an unresolved, ongoing promotional relationship rather than a closed trade.
- **Receipt culture** — "receipt(s)" appears in 56 posts, almost always as a challenge to *other* posters ("no receipts = scroll on") before he began applying the same standard to his own SPX trades late in the archive — an accountability norm he pushed on the community before fully practicing it himself.
- **AI-assisted content, disclosed once** — the May 9, 2026 PDT-rule-change essay ends with *"This post was helped using ChatGPT to get my thoughts and convey them"* — a rare, explicit disclosure of AI-assisted content generation, worth tracking as a leading indicator of retail AI-tool adoption on the platform (consistent with a pattern already flagged in this cohort's `browndog` dossier).
- **Political/culture-war content bleeds constantly into market commentary** — Trump-administration framing recurs in nearly every SPY macro post ("if it was up to Trump we'd be 700"); standalone political posts (RIP Charlie Kirk, government-shutdown commentary, an explicit "fuck you to all the democrats" post) draw some of his highest engagement (55 and 54 reactions respectively) but carry zero trading signal.

### Reaction to volatility / red days
- **Mechanical single-name red days:** relatively composed, often reframed as buying opportunity narrative ("we simply cannot freak out, we go through dips," 2026-02-09 on $ONDS).
- **Broad-market red/volatile days:** treated as scalping opportunity per his own published rules, not fear — "the last 24 hours... 700 SPY + Steelers = Super Bowl" style bravado is common even into uncertain macro setups.
- **Personal-life stress (health scare) bled directly into market posting** — the Dec 2025–Jan 2026 stretch (his highest-volume months, 272 and 280 posts) directly overlaps with his lung-nodule workup, and several posts explicitly reference "going through a 6.5-week very well documented chapter of my life that scared the fuck out of me" as context for why he was less receptive to community criticism during that window — a real behavioral confound Artemis should weight when reading his conviction level in that period.

### Engagement profile
Average **360 views / 8.8 reactions / 8.8 comments** per post (materially higher than `browndog`'s cohort-bottom-tier ~2.9/2.1/225) — but his **highest-engagement moments are, almost without exception, platform-politics and community-drama posts, not trade calls**: an "Open Letter to @SIRJACK" (282 reactions, 2026-08-29, his all-time high), a second leadership letter (150 reactions, Jan 2026), viral posts titled "It's wild how life can change in an instant" (106 reactions) and "Hey, is everyone ok?" (79 reactions/101 comments) — his audience engages with his personality, platform advocacy, and community-crisis moments far more than with his tickers.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

**Primary:** `COMMUNITY_TICKER_EVANGELIST_ONDS` — a year-long, IR-adjacent promotional relationship with a single small-cap (two personally-arranged CEO webinars, repeated "Stock of the Year" framing, unfulfilled $15/$20/$25 price targets), run through a self-built Discord community (Pathfinders) rather than pure discretionary trading.

**Secondary:** `0DTE_SPX_SPY_SCALPER_RULES_BASED` — a genuinely competent, explicitly-documented short-dated index options practice (theta/gamma/spread mechanics correctly articulated) that visibly matures over the archive into disclosed-receipt day-trading by its final months, though inconsistently applied against his own stated rules (one documented DCA-into-a-0DTE-loser directly violating his own "never average down on 0DTE" rule).

**Tertiary (positive, high-value for the platform, not directly tradeable):** `RETAIL_FRAUD_SENTINEL` — 25% of his total output is anti-scam/anti-pump content, with at least one genuinely rigorous forensic takedown ($ORBS buyback math, 2026-01-06); this is his single most consistent, most verifiable, and most repeatable value-add, even though it produces no direct trading signal.

**Watch tag:** `AI_ASSISTED_CONTENT_EMERGING` — one explicit ChatGPT-assisted post (2026-05-09); track for expansion.

**Blacklist/conflict tag:** `ISSUER_PROMOTIONAL_ENTANGLEMENT` — the $ONDS CEO-interview relationship is a structural conflict of interest that should discount, not amplify, any bullish $ONDS signal sourced from this account, regardless of the poster's sincerity or the underlying company's real fundamentals.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 33 / 100**

Rationale:
- **+ (genuine, teachable trading mechanics knowledge, ~14 pts):** the SPY 0DTE rules essay and three-part "How to Trade SPY" series are specific, correct, and rare in this cohort's quality — real evidence of process, not just outcome-chasing.
- **+ (one clean, well-timed fundamental call, ~10 pts):** $CAT, $575→$1,000+, fully time-stamped, thematically sound (data-center backup power), never reversed or walked back.
- **+ (genuine self-correction culture, ~6 pts):** publicly declared wrong on TSLA $500 and SPY 700, and holds peers to the same standard — rare and valuable as a sentiment-calibration signal (when he says "I was wrong," take it at face value; most peers in this cohort never do).
- **+ (real, repeatable anti-fraud value, ~5 pts, capped — not directly tradeable):** the scam-detection content is genuinely useful as a *sentiment-fade* input (see §5.3) even though it generates no buy/sell signal of its own.
- **− (extreme signal dilution, ~15 pts):** only 20.3% of 2,517 posts contain any ticker at all; an ingestion pipeline treating this account as a dense signal source will be overwhelmingly fed banter, platform politics, and personal content.
- **− (unresolved promotional conflict of interest on the flagship name, ~15 pts):** two personally-arranged CEO webinars for $ONDS while simultaneously telling a paying-attention community to buy it, with unfulfilled $15/$20/$25 targets never publicly walked back the way his other misses are.
- **− (no verified PnL infrastructure at all, ~10 pts):** `gain_loss` 100% empty, `amount_k` unusable, self-reported dollar receipts appear only in a handful of late-archive posts, and the one visible streak (Aug 31–Sep 2, 2026) is suspiciously all-green relative to his own earlier loss-disclosure pattern.
- **− (stated-rule violations, ~2 pts):** one explicit, self-admitted DCA-into-a-losing-0DTE-position directly contradicting his own published "never average down on 0DTE" rule.

**Expectancy: UNVERIFIED / LIKELY NEUTRAL, with a narrow POSITIVE pocket.** No equity curve exists to resolve this quantitatively. The narrow, disclosed SPX/SPY 0DTE day-trading practice (when he is actually posting numeric receipts, both wins and losses, as in May and Aug–Sep 2026) plausibly carries a small positive expectancy consistent with his stated rules-based approach — but the $ONDS promotional arc, taken on its own, should be scored **negative-to-neutral** given the gap between promised targets and realized price action, and the bulk of the archive (BYND/ORBS/HUBC/SPCX commentary) is not his own trading at all and carries no expectancy claim either way.

### 5.3 Signal Flow Ingestion Matrix

| Post Signature | Underlying Signal Type | Reliability | Artemis Action |
|---|---|---|---|
| SPY/SPX 0DTE mechanics essays (theta/gamma/OI/spread rules) | Documented, rules-based short-options process | Moderate-High (internally consistent, teachable, rarely seen at this quality in-cohort) | **INGEST** as an educational/parameter-calibration input for the Engine's own 0DTE logic, not as individual trade signals |
| $CAT-style thematic fundamental calls (data-center infra, backup power) | Ahead-of-consensus sector thematic spotting | Moderate-High (single strong sample, well-timed, well-reasoned) | **INGEST** as a research tip for independent fundamental verification |
| SPX/SPY day-trading "receipts" posts with explicit $ figures | Self-reported intraday PnL | Low-Moderate (unverifiable, recency-biased green streak at archive end, but historically included honest loss disclosure too) | **LOG for sentiment-temperature tracking only; DO NOT size off these numbers** |
| $ONDS conviction/target posts (price targets, "Stock of the Year," CEO-interview promotion) | Single-name promotional evangelism with a structural conflict of interest | Low (targets have a documented history of non-realization; promotional entanglement discounts objectivity) | **FADE/DISCOUNT** — treat as retail-sentiment/crowd-positioning data, never as a standalone bullish signal |
| Anti-scam callouts (named promoters, forensic pump-thesis takedowns) | Fraud/pump-and-dump detection | Moderate-High (at least one rigorous, numerically-grounded takedown documented; directionally useful even when tone is crude) | **INGEST as a contrarian-fade trigger** — a name he flags as a pump target is a high-confidence signal to avoid or fade that name, independent of his own trading |
| Commentary/mockery on other posters' tickers (BYND, ORBS, HUBC, SPCX, PUSA) | Entertainment/observational, not his own position | N/A as a trade signal | **DO NOT attribute to him as a trade** — parse carefully to avoid false-positive signal attribution |
| Platform-politics posts (open letters, petitions, leadership callouts) | Community/platform-health commentary | N/A for trading | **IGNORE for trading signal**; may be useful as a platform-health/churn-risk indicator for AfterHour itself |
| Political/culture-war standalone posts | Not a trading signal | N/A | **IGNORE** entirely for trading purposes |
| AI-assisted content generation posts (disclosed ChatGPT use) | Meta-signal on retail AI-tool adoption | N/A for trading | **LOG, do not trade** — track as a leading indicator alongside the `browndog` precedent already in this cohort |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Extract the **documented 0DTE/SPX mechanics rules** (theta acceleration after 3PM, never average into a 0DTE loser, size down on low-VIX chop days, close winners fast, avoid late-day wide-spread fills) as calibration inputs for the Engine's own short-dated options execution logic — this is real, teachable process, independent of whether his own PnL is verifiable.
2. Pull **thematic fundamental calls in the $CAT mold** (infrastructure/backup-power/data-center adjacency plays, publicly reasoned well ahead of the move) as raw research tips for independent verification — his one clean, repeatable strength.
3. Treat his **named scam/pump callouts** as a standing contrarian-fade watchlist input — when he names a promoter or a pump target, log the ticker and the promoter for cross-reference against the Engine's own fraud/pump-detection heuristics.

**Contrarian Fade Directives (when to fade him / the retail herd):**
1. **Fade specific $ONDS price targets** ($15/$20/$25-style calls) as promotional rather than analytical — the archive shows a clean pattern of unrealized targets on this name specifically.
2. **Discount any bullish thesis that coincides with a CEO-interview or webinar announcement** for the same name — the promotional apparatus itself is the tell, regardless of underlying fundamentals.
3. When his posting cadence **spikes on community-drama/platform-politics content** rather than ticker content, treat that as a signal his attention (and reliability) is temporarily diverted from markets, not as a market-state signal itself.

**Mandatory Risk Blacklists & Firewalls:**
1. **Never size a position off his self-reported SPX/SPY dollar "receipts"** — no linked brokerage, no consistent loss-disclosure cadence, and a suspiciously all-green terminal streak in the archive's final days.
2. **Firewall any $ONDS-specific signal sourced from this account from being treated as independent** — his commercial/attention relationship with the company's CEO (two personally-arranged webinars) is an undisclosed-to-the-algorithm conflict of interest that must be flagged every time the ticker recurs.
3. **Do not attribute commentary on $BYND/$ORBS/$HUBC/$SPCX/$PUSA to him as trading positions** — the large majority of this content is observational/mockery of other posters, not his own book; misattribution here would create false signal density.
4. **Do not treat post-cadence spikes as a volatility or opportunity proxy for this trader** — his cadence tracks community-drama and platform-politics cycles (Dec 2025–Jan 2026 driven by a health scare and a fraud-investigation news cycle, not a trading-opportunity window).

**Exit Rules & Alpha Rectification:**
1. Any idea sourced from his $CAT-style thematic calls should still carry an **Engine-defined stop-loss and profit-take band**, never inherited from his own commentary, since his stated rules (never DCA a 0DTE loser) have at least one documented in-archive violation by his own account.
2. If he ever **publicly closes out and reconciles the $500-to-$5,000 SPX challenge account** with a full, dated equity curve, re-score this profile — a genuine, continuous, verifiable small-account day-trading track record would meaningfully raise this account's reliability tier.
3. Apply a standing **"promotional-entanglement discount"** as a reusable Engine heuristic wherever any influencer-tier account (in this cohort or beyond) is found to have arranged direct contact with an issuer's management team while promoting that issuer's stock to a paying-attention audience — this dossier is the clearest documented example of that pattern in the cohort to date.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone / Catalyst | Notes |
|---|---|---|
| 2025-02-13 | First (isolated) archive post ("Trump Delay") | Account effectively dormant until mid-2025 |
| 2025-07-01 to 07-02 | $RXRX anti-scam campaign begins; SPY commentary starts | Establishes the "scam sentinel" persona from week one of real activity |
| 2025-07-22 | First $NIO position disclosed ("Picked up some $NIO... if we win we win, if we lose we lose") | Early equities dabbling alongside options |
| 2025-10-01 to 10-27 | $BYND mania commentary (16 mentions in October alone) | Mostly mockery/observation of other posters' pumps, not his own position |
| 2025-10-29 | **$TSLA thesis reversal and exit** ("Electric Elephant... No Longer 500 EOY") | Sells his "most emotional hold" and publicly documents the reversal — one of his cleanest, best-timed calls |
| 2025-11-03 | First $ONDS post of the sustained campaign | Beginning of the year-long single-name evangelist arc |
| 2025-12-05 | **Lung nodule discovered** (13mm×18mm, PET SUV 27) | Personal health crisis begins, overlapping the archive's two highest-volume months |
| 2025-12-16 | **"My Rules for $SPY 0 Days"** published | His single most valuable, teachable trading-mechanics post in the archive |
| 2025-12-16/22/24 | Three-part "How to Trade $SPY" essay series | Fills-vs-screen-profit, low-volume premium decay, open-interest psychology — genuinely competent content |
| 2025-12-21 | **$CAT thematic long entered** ($575) | Data-center backup-power thesis; becomes his cleanest documented winner |
| 2025-12-30 | Public $ONDS "$15 by March 21, 2026" bet made | Never publicly resolved/acknowledged when unmet |
| 2026-01-16 | "90 Day Tip Fraud Investigation... 399,240 Fake Coins" callout | Peak of the anti-scam-vigilante content arc |
| 2026-01-18/19 | Public falling-out with a fellow creator over the health-scare period; posts proof-of-diagnosis video after being accused of faking it | Rare, raw personal-vulnerability content in an otherwise bravado-heavy archive |
| 2026-01-22/23 | **First Eric Brock ($ONDS CEO) live webinar**, arranged personally, hosted in Pathfinders Discord | The defining promotional-entanglement event of the archive |
| 2026-01-24 | Partners with `@mphinance` on a live Pathfinders podcast ("Getting to Know You") | Cross-promotion within the analyst's own network |
| 2026-02-18 | $ONDS crosses $11.00 | Approaching, but not yet at, the March peak |
| 2026-03-01 | "AfterHours got bought out" — platform ownership change referenced | Macro/platform-level event, not a trading catalyst for him specifically |
| 2026-03-02 | **$ONDS peaks at $12.15** | Highest price reached in the archive; subsequently fails to hold or extend toward the $15/$20/$25 targets |
| 2026-03-06 | Public self-accountability essay (TSLA $500 miss, SPY 700 miss acknowledged) | Genuine self-correction culture, rare in this cohort |
| 2026-04-05/06 | $RBLX "activist short" campaign (child-safety ethical framing, puts) | Distinct "moral crusade short" behavior pattern, outcome not resolved in-archive |
| 2026-05-06 | $CAT reaches $925 | ~61% realized from his Dec 2025 entry, still climbing |
| 2026-05-09 | PDT rule-change essay (June 4, 2026 threshold cut $25K→$2K), disclosed as **ChatGPT-assisted** | Well-reasoned, correctly-anticipated regulatory catalyst; first explicit AI-content disclosure |
| 2026-05-12/14 | $500-to-$5,000 SPX Challenge Account launched; discloses a "-55% before DCA" and a "$591 loser" morning | Genuine transparency on losses, contradicts his own "never DCA a 0DTE loser" rule |
| 2026-05 (mid-month) | **View counts inflect from single/double digits to 500–3,000+** | Account visibly "breaks out" in reach mid-archive |
| 2026-06-04 | PDT threshold rule change takes effect (real-world event he had covered a month in advance) | Validates his regulatory-catalyst call |
| 2026-06-22 | $CAT tops $1,000 | Final, fullest realization of his cleanest documented win (~74% off entry) |
| 2026-08-12/13 | $ONDS earnings-week volatility; stalls repeatedly at "9.90 wall" | Consolidating well below his own $15/$20/$25 promotional targets from 8-9 months earlier |
| 2026-08-29 | **"Open Letter to @SIRJACK"** — his all-time-high engagement post (282 reactions) | Confirms audience responds to platform advocacy far more than to trading calls |
| 2026-08-31 to 2026-09-02 | **Five-to-six-day run of positive, dollar-explicit SPX day-trading "receipts"** (+390 to +974 per session) | His most numerically disciplined trading stretch in the archive — but a suspiciously all-green terminal window relative to his own earlier loss-disclosure pattern |
| 2026-09-10 | Archive closes | No formal wrap-up, retrospective, or reconciled equity curve posted |

---

*End of dossier. Prepared from `@Freeballer_lifetime.md` (2,517 posts, full text) and `@Freeballer_all_posts.json` (structured metadata) with no external data sources. `gain_loss` and `amount_k` fields were tested and found unreliable for this account; all financial claims herein are self-reported by the subject and unverified against any brokerage record.*
