# Quantitative & Behavioral Autopsy: @RoyaltyTradez

**Platform**: AfterHour (`https://afterhour.com/RoyaltyTradez`) | **Profile ID**: `prf_a45d9c10826f4a88a88bd40c0c1fc4a6`
**Network Rank**: #6 Most Active Followed Trader | **Lifetime Posts Analyzed**: 2,076
**Coverage Window**: 2024-04-27 → 2026-09-10 (867 days / ~124 weeks)
**Sources**: `@RoyaltyTradez_lifetime.md` (full text archive), `@RoyaltyTradez_all_posts.json` (structured fields)

---

## 1. Executive Profile

### 1.1 Who He Is
@RoyaltyTradez is a Louisiana-based, self-taught retail options trader who works a full-time job at the **United States Postal Service** and trades as a side hustle turned content business. In his own words (autobiographical post, 2024-10-10, *"It's been a week of Reflection for me"*):

> *"Trading for me started off as a side hustle in 2018... I became self taught and eventually started calling signals in my own discord... Jan 2022, I lost my younger cousin to gun violence... I introduced him to stocks... our dream was for us to be the Batman and Robin of trading... I'm not a full time trader because I don't have the desire to right now, I have an amazing job with the post office... I don't have a gimmick, I don't do this for fun, I do this [to] help change someone's financial situation."*

Note: a second origin post (2025-03-15, *"Story time w/RoyaltyTradez"*) instead dates his start to **2020**, triggered by pandemic-stimulus YouTube hype (buying `$JNUG`, `$VXX`, `$MRNA`) before joining a paid mentor group ("Aristotle Trading Group," ~$100/mo). The two years-since-start claims (2018 vs. 2020) are internally inconsistent — flag as unverifiable biographical noise, not a data point to trust literally.

**Philosophy**: Community-first, "family" branding, explicitly anti-hype ("Don't follow stocks like it's ya fav team"), and increasingly religious/motivational in later periods (2026 "👑 Royal Word for the Day" scripture-adjacent posts, "The Kingdom" branding). He is unambiguously running a **content + subscription business** layered on top of discretionary trading — Patreon (2024) → "The Kingdom" Discord/podcast/"University" (2025–26), with recurring paid-tier promotions, referral shoutouts, and a live YouTube "Round Table Talk" podcast.

### 1.2 Post Cadence
- **Total**: 2,076 posts over 867 days → **~16.8 posts/week** lifetime average (2.4/day).
- Cadence is **highly volatility- and engagement-driven, not constant**:

| Period | Posts/mo (peak) | Character |
|---|---|---|
| 2024-05 | 172 | Onboarding surge — high-frequency chart-callouts, building audience |
| 2024-09/10 | 138 / 159 | Peak "Pre Market Analysis" + "Dd"-tag daily routine (NVDA/AI mania) |
| 2025-04/05/08 | 41/34/29 | Sharp pullback — coincides with "sidelines," Topstep pivot, burnout posts |
| 2025-11 – 2026-03 | 27–79 (choppy) | Shift toward "Kingdom" ecosystem content, less raw chart spam |
| 2026-08 | 97 | Late resurgence, high engagement ("$1M milestone" shoutouts, AVGO/NVDA/TSLA) |

The 2024-11 → 2025-08 stretch shows a structural cadence decline (~50→80/mo down to ~30/mo) coinciding with explicit "watching from sidelines," a Topstep futures-account detour, and a self-described "obsession"/burnout confession (2025-08-08: *"you're up all night thinking about the stock market... you know the only way to walk away is thru therapy"*). Cadence partially recovers in 2026 alongside the "Kingdom" monetization push.

### 1.3 Capital Trajectory & Verification — CRITICAL CAVEAT
**There is no verified, broker-linked P&L for this trader.** The structured `amount_k` field is functionally noise (1,037 non-zero entries, all clustered at **~$0.00–$0.00027k**, i.e. fractions of a dollar) — this is a platform telemetry artifact, not real capital, and must not be used as a performance metric.

What *is* documented, directly from post bodies:
- **Position sizing is small and retail-scale.** Every dollar-denominated risk figure found in the corpus is in the **$25–$60 per-contract risk** range (e.g., "AAPL 222.5C 09/20 @1.15 SL .90 (-$25)"; "NVDA 108p... SL $1.05 (-$30 risk)"). This is lunch-money-sized options trading, consistent with someone trading a small personal account alongside a day job — not a funded professional book.
- **A "Small Account Challenge"** series (Nov 2024 – Apr 2025) explicitly frames trading as compounding a small starting balance for followers to mimic.
- **Prop-firm futures detours**: a **50K Topstep** evaluation account (June 2025: *"Dug myself out of this $400 hole"*), an attempted scale to **150K** (June 2025), and a second Topstep restart in **Nov 2025** with a stated **$9K profit goal** — i.e., he never demonstrably passed and stayed funded; each mention is a fresh restart, not a continuation.
- **One (1) formally tagged loss** in the entire 2,076-post corpus (`tag: "Loss"`, 2024-08-28, `$AAPL`, "SL triggered -$60"). Every other post is untagged — **he does not use the platform's own loss-tagging feature**, which means realized losses are systematically under-reported in structured fields and only recoverable by reading body text.
- **Win claims are narrative, not audited**: percentage call-outs like "+300% on $TSLA," "+400% on $PLTR," "+100% on $MSFT calls" appear regularly in 2026, but as retrospective text claims tied to entries he also posted — not broker screenshots or platform-verified fills. Treat as **directionally indicative of a real edge in entry timing**, not as an audited return series.

**Verdict**: capital trajectory is **unverifiable and structurally survivorship-biased toward winners** (round-number risk disclosures early on stopped after Sept 2024; later periods almost never disclose $ risk, only % return on the tickers that worked).

---

## 2. Ticker Universe & Catalysts

### 2.1 Core Assets (by post-tag frequency, n=2,076 posts, 246 unique tickers)

| Rank | Ticker | Mentions | Rank | Ticker | Mentions |
|---|---|---|---|---|---|
| 1 | SPY | 338 | 9 | AMZN | 44 |
| 2 | NVDA | 332 | 9 | META | 44 |
| 3 | QQQ | 307 | 11 | AMD | 43 |
| 4 | TSLA | 235 | 12 | PLTR | 42 |
| 5 | MSTR | 100 | 13 | SQQQ | 41 |
| 6 | AAPL | 99 | 14 | COIN | 30 |
| 7 | GOOGL | 65 | 14 | IWM | 30 |
| 8 | XOM | 58 | 16 | GME | 26 |
| 8 | MSFT | 56 | 17 | ASTS | 23 |

- **Index/ETF vehicles dominate** (`SPY`+`QQQ`+`IWM`+`SQQQ` = 716 tags, ~24% of all ticker-tags) — this is a **level-to-level index trader first**, single-name trader second. `SPY`/`QQQ` "Pre Market Analysis" is his structural daily anchor post (172 posts explicitly titled "Pre Market Analysis").
- **Mag-7 concentration**: NVDA, TSLA, AAPL, GOOGL, MSFT, AMZN, META together = 875 tags (~30% of all tags) — squarely mega-cap tech/AI momentum.
- **MSTR/BTC/COIN cluster** (100 + 47 + 30 = 177, plus broader crypto-adjacent language in 191 posts) is a persistent secondary theme — he treats `MSTR` as a leveraged BTC proxy and trades both directions on it (see §6, Sept 2026 puts).
- **XOM** (58 mentions) stands out as his one consistent non-tech "sector rotation" name — used explicitly as a hedge/rotation play ("play sector rotations out of tech when the market decided to cool down").
- **Futures**: `NQ`/`ES`/Topstep referenced in 30 posts — a minority, opportunistic sleeve, not a core strategy.
- **Long-tail speculative names** (ASTS, RXRX, GME, SOUN, LUNR, CORZ, SKHY, SPCX, MRAM, ONDS) appear in short clusters tied to momentum/social-media attention — classic retail "hot ticker of the week" rotation, each with a burst of 3–10 posts then abandonment.

### 2.2 Instrument Mix
- **Options-dominant**: "calls" appears in 257 posts, "puts" in 158 (202 calls-only / 146 puts-only / 49 both-sided posts by title+body classification) → **~58% long-call bias / 42% put-side**, i.e., genuinely two-sided, not a permabull.
- **Equity/shares language** (110 posts referencing "shares," "long term," or "LEAPS") shows a secondary buy-and-hold sleeve, mostly for building followers' "portfolios" via fixed levels rather than his own primary vehicle.
- **0DTE explicit** only 10 mentions — he is NOT a 0DTE degenerate-options poster; his options horizon is typically **weekly-to-2-week dated contracts**.

### 2.3 What Drives Entries
Overwhelmingly **classical technical analysis**, not macro or fundamentals:
- Horizontal support/resistance ("levels"), supply/demand zone flips, gap fills, trend-line breaks, 200 SMA, break-of-structure (BOS) / change-of-character (ChoCH) language, Gann levels (later period).
- "support" appears **1,060 times**, "resistance" **217**, "breakout" **175**, "hold" **605** in the corpus — level-based tape reading is by far the dominant lexical signature.
- Macro triggers are reactive, not predictive: FOMC/Powell/CPI/rate-cut language totals only ~40 mentions combined — he reacts to macro prints (tariff selloffs, Fed days) with level updates rather than pre-positioning on macro theses.
- Earnings-driven setups are common (141 "earnings" mentions) — pre-earnings trend plays and post-earnings gap fades (AAPL, AMD, DELL, SNOW, AVGO patterns visible in Aug–Sep 2026).
- Crowd/flow awareness: he frequently references what "everybody" is chasing and positions contrarian to obvious retail crowding (see §4).

---

## 3. Risk Management & PnL Reality

### 3.1 Stated Risk Framework (Genuine, Reusable Content)
He has published an internally consistent, mathematically correct **options loss-recovery framework**, taught explicitly inside paid content ("The Kingdom University") and shared publicly twice (2024-05-11, 2025-07-09):

| Drawdown on premium | Required gain to breakeven |
|---|---|
| 10% | 11% |
| 20% | 25% |
| 30% | 43% |
| 40% | 67% |
| 50% | 100% |
| 60% | 150% |
| 70% | 233% |
| 80% | 400% |
| 90% | 900% |

Stated rule: **cut by ~30%** ("after 30% the price action has to work significantly harder... CASH IS ALWAYS A POSITION"). This is a legitimate, textbook-correct convexity-of-losses lesson — rare to see stated this precisely on a retail social platform, and it is his single most exportable piece of genuine trading knowledge.

### 3.2 Profit-Taking Behavior
- Consistently **urges trimming into strength** rather than holding for max upside: "Start securing the mf bag," "cash it," "lock in profits," "profit is profit but we closed out TSLA a bit early." This is a de-risking, not a bag-holding, posture.
- Repeated messaging that small, frequent wins compound better than home-run swings ("Small wins like this allows small accounts to become bigger accounts... compound gains day after day").
- **Explicit stop-loss discipline in named trades** when he chooses to disclose ($25–60 risk per contract, SL prices stated to the cent) — but this behavior is concentrated almost entirely in a short window (Sept–Oct 2024); disclosed SL-with-price-and-risk posts drop off sharply after that, replaced by vaguer post-hoc "SL triggered" or "stopped out" mentions without figures.

### 3.3 Losing-Position Handling
- No documented account blow-up, margin call, or "wiped out" admission anywhere in 2,076 posts.
- Losses are acknowledged **narratively and briefly**, then immediately reframed as a "discount"/re-entry opportunity, not dwelled on. This is consistent (helpful for follower morale, unhelpful for auditing real risk-adjusted performance).
- The Topstep prop-account restarts (funded-eval → drawdown → restart, at least twice across 2025) are the closest thing to a documented "blow-up" pattern in the corpus — he does not explicitly say he failed the evaluations, but the repeated "back to Topstep, starting over" framing across 5+ months strongly implies non-passing outcomes each time.
- **Systematic under-tagging of losses** (1 of 2,076 posts tagged `Loss`) is itself a risk-management/behavioral red flag for signal consumers: the public record is structurally curated toward wins.

### 3.4 Documented Wins vs. Blow-Ups Summary

| Category | Evidence density | Reliability |
|---|---|---|
| Small, disclosed-risk options wins/losses (Sep–Oct 2024) | High detail, $ figures given | High — directly quotable |
| % return call-outs (2026 era: +100–400% on TSLA/PLTR/MSTR/MSFT) | Frequent, narrative only | Medium — plausible given his level-calling skill, but unaudited |
| Topstep prop account cycles | 3 distinct posts across 5 months | Medium — implies repeated failure to scale, not stated outright |
| Catastrophic loss / margin call / "blew up" | Zero instances found | N/A — either genuinely avoided or simply never disclosed |

---

## 4. Behavioral & Sentiment Signals

### 4.1 Why He Posts
Three overlapping motives, in descending order of textual evidence:
1. **Community/monetization funnel** — AfterHour posts function as top-of-funnel marketing for Patreon → "The Kingdom" (Discord + podcast + "University" courses + livestream). Discount promos ("50% Off Weekends," "One & Done Tier") and follower-milestone posts ("Congrats @geo21208 For His $1M Milestone!!!!!") recur throughout 2025–26.
2. **Genuine educational mission**, rooted in the cousin's-death origin story — teaching "correct" options mechanics (Greeks, SL sizing, loss-recovery math) to retail followers who remind him of his late cousin.
3. **Personal-brand/identity maintenance** — "Royal Family," "👑" branding, motivational/scripture-adjacent posts ("Royal Word for the Day"), and periodic public reconciliation of drama (2024-10-23 "Lemme Apologize to the Family," 2025-07-11 "Officially Banned From The Kingdom" — an internal community banning post).

### 4.2 Recurring Linguistic Patterns
- Signature openers: *"What's good Family/Fam🫡"*, *"Royal Family👑"*, closings with 🫡💯🚀.
- Emoji-as-punctuation sentiment markers: 🩸 = bearish/selloff, 🚀 = bullish breakout, 💰 = profit/opportunity, 👑 = Kingdom-branded/paid-tier content (introduced ~2026).
- Signature phrases: *"CASH IS ALWAYS A POSITION"*, *"secure the bag"*, *"don't chase,"* *"follow the money not the ticker,"* *"discounts"* (his preferred euphemism for a red/selloff day — reframes drawdowns as buying opportunities for followers).
- Self-branding as "The Crowned Edge Setup" / "Royalty Radar" for his callout methodology.

### 4.3 Reaction to Volatility / Red Days
Consistently **composed and opportunistic, not panicked**, across every major volatility event captured in the archive:
- **Aug 2024 BTC/carry-trade unwind**: pre-positioned bearish on BTC/MSTR/COIN the day before, calm follow-through commentary.
- **April 2025 tariff crash** (Trump reciprocal-tariff selloff): daily "Pre Market Analysis" continued uninterrupted; explicitly reduced size and shortened hold times ("Beginner Options Trader Strategy," "keep the trades limited and the contracts cheap"); pivoted to an explicit morale post mid-crash (*"Somebody Needs This Positivity In There Life"* — his 2nd-highest-engagement post ever, 115 reactions/71 comments) rather than doubling down or going silent.
- **General posture**: sell-offs are consistently reframed as "discounts," reinforcing a **buy-the-dip / mean-reversion bias layered on top of his level-based TA**, and he explicitly self-identifies this compulsive relationship with the market (2025-08-08, *"This is Now Your Obsession"* — describes trading as an addiction he's made peace with, "flawless victory or bloody defeat... I face this market with full conviction").

### 4.4 Sentiment Calls
He runs a **persistent SPY/QQQ pre-market bias call** (172 dedicated posts) that functions as a daily directional weathervane for his following — a genuinely trackable, timestamped, high-frequency signal stream suitable for backtesting call/put accuracy if cross-referenced against next-session price action.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags
- **Primary**: `LEVEL_BASED_INDEX_SCALPER` (SPY/QQQ/IWM pre-market horizontal-level caller, weekly-dated options, high cadence)
- **Secondary**: `MOMENTUM_MEGA_CAP_SWING` (NVDA/TSLA/MSTR directional swing overlay, both calls and puts)
- **Tertiary**: `RETAIL_SENTIMENT_AGGREGATOR` (community-funnel content creator whose posting volume itself is a crowd-attention proxy, independent of his trade accuracy)

### 5.2 Algorithmic Alpha Score & Expectancy
**Alpha Score: 42 / 100**

Rationale:
- (+) Genuinely competent, high-frequency, timestamped level-calling on the most liquid instruments (SPY/QQQ/NVDA/TSLA) — real potential signal value in the *direction and levels*, independently verifiable against OHLC data.
- (+) Correct, teachable risk math (loss-recovery table, 30% cut discipline) — rare quality signal.
- (–) **No audited P&L.** `amount_k` telemetry is broken/negligible; win claims are unaudited narrative; only 1 of 2,076 posts carries a `Loss` tag — structurally biased sample.
- (–) Position sizing disclosed (when disclosed at all) is trivial ($25–60/trade) — not evidence of scalable, capital-efficient edge.
- (–) Content-business incentives (Kingdom/Patreon upsells) create a structural motive to over-report winners and under-report/soften losers.
- (–) Two Topstep funded-account restarts within 5 months suggest inability to consistently scale size without blowing the account's drawdown limit.

**Expectancy**: Cannot be computed to a defensible confidence level from public data — treat any inferred expectancy as **qualitative-only** ("more often directionally right on liquid index/mega-cap levels than wrong, based on engagement and follow-through screenshots, but magnitude and consistency are unverifiable"). Do not feed a numeric expectancy into position-sizing models built on this trader's claimed returns.

### 5.3 Signal Flow Ingestion Matrix

| Signal Type | Frequency | Tickers | Reliability | Ingest? |
|---|---|---|---|---|
| Daily Pre-Market SPY/QQQ level call | ~2–3x/wk | SPY, QQQ, IWM | Medium-High (timestamped, backtestable) | **YES** — as a directional-bias input, weighted, not standalone |
| Named options entry w/ strike, exp., SL | Rare after Oct 2024 | Mixed | High when present (verifiable strike/price) | **YES** — only when strike+price+SL is explicit |
| "% return" retrospective claims | Frequent (2026) | TSLA/MSTR/PLTR/NVDA | Low (unaudited, hindsight-framed) | **NO** — narrative only, exclude from scoring |
| "Discount"/buy-the-dip reframes during red days | Frequent | SPY, QQQ, mega-caps | Medium (genuine contrarian instinct, but talks his book for Kingdom signups) | **CONTRARIAN-FADE CANDIDATE** |
| Topstep/futures account posts | Sporadic | NQ, ES | Low (no completed track record shown) | **NO** |
| Kingdom/Patreon promo posts | Frequent | N/A | N/A (marketing, not signal) | **FILTER OUT** |
| Long-tail hype tickers (ASTS, SPCX, SKHY, MRAM, ONDS) | Bursty | Various small/mid-cap | Low-Medium (momentum/social-attention driven, high variance) | **CONTRARIAN-FADE CANDIDATE at extension** |
| Loss-recovery / risk-management commentary | Rare but high-quality | N/A | High (correct options math) | **YES** — ingest as a rules/education layer, not a trade signal |

### 5.4 Execution Directives for the Artemis Engine

**A. Ingestion Directives (genuine edge to harvest)**
1. Ingest his **daily SPY/QQQ/IWM pre-market level calls** as one weighted input into a multi-trader consensus/breadth signal — his level-based S/R and gap-fill framework is internally consistent and testable against realized OHLC.
2. Ingest **explicit, fully-specified options callouts** (ticker + strike + expiry + entry price + SL) only — these are the rare instances with enough structure to backtest cleanly. Discard vague callouts lacking all four fields.
3. Harvest his **loss-recovery percentage table** and **30%-cut rule** as a static risk-management module (correct, reusable, source-agnostic) — not trader-specific alpha, but valid education content to encode into Artemis's own risk gates.
4. Treat elevated posting **cadence spikes** (e.g., 150+ posts/month) as a crude retail-attention/volatility proxy — correlates historically with high-realized-vol regimes (Sept–Oct 2024 AI mania, Apr 2025 tariff crash).

**B. Contrarian Fade Directives (when to fade his calls / the retail herd)**
1. **Fade "discount" framing at climactic extension**, not at initial pullback — his buy-the-dip reflex is a genuine instinct at moderate pullbacks but becomes a herd-following bias when he's simultaneously running a "half off" or "one & done" Kingdom promo (i.e., when marketing incentive to keep followers bullish/engaged is highest, weight his bullish bias down).
2. **Fade parabolic long-tail momentum names** (ASTS, SPCX, SKHY, MRAM, ONDS-style bursts) once his post frequency on a single small/mid-cap ticker spikes within a short window — this pattern historically precedes exhaustion/mean-reversion in these low-float, social-attention-driven names.
3. **Discount % return claims made in hindsight** (post-facto "up 300%" framing without a prior disclosed entry) — these are marketing artifacts for the Kingdom funnel, not tradeable signals, and should never be scored as track record.
4. When he **stops disclosing $ risk and strike specifics** (post-Oct-2024 pattern) on a name, treat subsequent directional claims on that name as **lower-confidence, retrospective narrative** by default.

**C. Mandatory Risk Blacklists & Firewalls**
1. **BLACKLIST the `amount_k` / platform-verified-PnL field entirely** for this trader — it is broken telemetry (max value $0.27), never reflects real capital, and must never be used to size confidence weighting.
2. **BLACKLIST any inference of "verified" performance** — 1 of 2,076 posts carries a `Loss` tag; treat his entire public record as **survivorship-curated toward winners** and discount win-rate assumptions accordingly (apply a conservative haircut, e.g., assume true win rate materially below what post-count-of-wins-vs-losses implies).
3. **FIREWALL Kingdom/Patreon promotional posts** from any signal-scoring pipeline — these are marketing content, not trade ideas, and should be filtered at ingestion (detectable via "Kingdom," "Patreon," "% off," "tier," "University," "Podcast" keyword matches).
4. **FIREWALL Topstep/prop-futures posts** — no completed, passed evaluation is documented; repeated restarts indicate this is not a repeatable, scalable sleeve of his trading and should not be used to infer futures-market skill.
5. Flag **biographical/timeline inconsistencies** (2018 vs. 2020 start-date claims) as a general signal that self-reported trader history on this platform should be treated as marketing narrative, cross-check against post timestamps rather than trader claims wherever the two conflict.

**D. Exit Rules & Alpha Rectification**
1. Where Artemis ingests his named options callouts, **apply his own stated rule mechanically and consistently**: exit/reduce at ~30% adverse move on premium (his own documented threshold), rather than trusting his in-the-moment "hold" language, which is inconsistently applied.
2. **Cap position confidence decay** on any of his callouts after 2 dated-contract expiries pass with no follow-up post — silence is his de facto "this didn't work" signal (losses are rarely announced, they're just not mentioned again).
3. For consensus-signal purposes, weight his SPY/QQQ pre-market bias **higher on trend-continuation days** and **lower on reversal/gap-fade days** — his framework (support/resistance/gap-fill) is structurally biased toward continuation reads and has historically been slower to flag reversals in the corpus (e.g., April 2025 tariff whipsaws required multiple days of "pivot" language before he adjusted).

---

## 6. Chronological Milestone & Catalyst Log

| Date | Event |
|---|---|
| 2024-04-27 | First post (`$NVDA` bulls call) — platform onboarding |
| 2024-05-11 | Publishes Options Loss Recovery Guide (30%→43% breakeven math) — first appearance of his signature risk framework |
| 2024-06-18 | Announces move toward accessibility/Patreon-style paid group |
| 2024-08-04/05 | BTC/MSTR/COIN bearish pre-positioning ahead of the Aug-5 volatility spike |
| 2024-08-28 | Sole formally `Loss`-tagged post in 2,076-post history (`$AAPL`, SL -$60) |
| 2024-09 – 2024-10 | Peak disclosed-risk posting era — named strikes, expiries, SL prices, $ risk consistently shown (largely disappears after this window) |
| 2024-09-04 | 700+ follower milestone |
| 2024-10-10 | Autobiographical "week of Reflection" post — origin story, cousin's death, USPS job, non-full-time framing |
| 2024-10-16 | First "Mentorship Inquiries" post — formalizing paid mentorship |
| 2024-10-23 | Public spat with another trader; issues community apology |
| 2024-11 – 2025-04 | "Small Account Challenge" series for followers |
| 2025-02-08 | Launches "The Kingdom Podcast" (Ep. 1/2) |
| 2025-03-15 | "Story time" post — alternate origin narrative (2020 start, pandemic stimulus trades) |
| 2025-04-01 – 04-10 | Tariff-crash coverage — reduced size, "positivity" morale post (2nd-highest engagement of lifetime) |
| 2025-05-01 | "Watching from sidelines" — explicit activity pullback amid volatile/downtrending tape |
| 2025-06-13 | First documented Topstep 50K funded-account attempt ("dug myself out of $400 hole") |
| 2025-07-09 | Re-publishes Loss Recovery Chart explicitly as "Kingdom University" curriculum material |
| 2025-07-11 | "Officially Banned From The Kingdom" — internal community discipline/drama post |
| 2025-08-01 | "Kingdom University" formally launches |
| 2025-08-08 | "This is Now Your Obsession" — self-aware confession of trading addiction (92 reactions) |
| 2025-11-06 | Second Topstep restart, stated $9K profit goal |
| 2026-01 – 03 | "👑 Royal Word for the Day" motivational/scripture-adjacent series begins |
| 2026-06 – 07 | Family vacation break (Panama City Beach); "new RoyaltyTradez" joke post on return |
| 2026-06/07/08 | Multiple 100–300%+ option-return claims (TSLA, MRNA, GOOGL, MSTR, MSFT) — highest density of win-claim posts in corpus |
| 2026-08-27 | Shoutout post congratulating a follower's "$1M Milestone" — strongest social-proof marketing beat in the archive |
| 2026-09-08 – 09-10 | Final posts in archive — `$MSTR` puts called "starting to print," bearish into period end |

---

*End of report. Compiled from structured JSON (2,076 records) and full-text Markdown archive. All direct quotes verified against source `body`/`title` fields.*
