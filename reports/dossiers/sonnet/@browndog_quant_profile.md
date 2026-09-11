# Forensic Quant Autopsy: @browndog

**Subject:** AfterHour trader `@browndog` (`prf_a863ed09ecd445ecbbf3cbdca40ce3ae`)
**Rank:** #32 most-active followed trader — 152 lifetime posts
**Coverage:** 2025-10-11 → 2026-09-05 (329 days / ~47.0 weeks)
**Sources:** `@browndog_lifetime.md` (full text, 152 posts), `@browndog_all_posts.json` (structured metadata: `tag`, `gain_loss`, `amount_k`, `tickers`, engagement)
**Analyst:** Artemis Engine — Sonnet dossier pass
**Methodology note:** `amount_k` is AfterHour's platform-captured snapshot of his primary linked account value (in $ thousands) at the moment of each post — this is the closest thing to a *verified* equity curve in the dataset, not a self-reported brag figure, and it is the backbone of §1 below. It should still be read with two caveats: (1) it tracks only his **primary/margin account** — a separate $500 "Browndog5" leverage experiment (opened 2026-02-27) is narrated independently and is **not** reflected in these numbers; (2) he explicitly discloses withdrawing capital from this account for **non-trading reasons** (business cash-flow crisis, 2026-01-07) — so part of the decline documented below is capital flight, not only trading losses. Free-text PnL claims (%, contract counts) are self-reported and unverified against a brokerage statement; treat them as directionally informative, not audited.

---

## 1. Executive Profile

### Who he is
A **51-year-old** (self-dated, Post #79) small-business owner who has "owned a franchise of the largest restoration company in the US for 15 years" (Post #46) — a homeowners'-insurance-claims/property-restoration business operating across **Arkansas/Tennessee/Mississippi**. Family man with a wife, a minor son, and a beloved dog also named "Browndog" (the account's namesake — a running personal-life thread throughout the archive, including two medical scares in Jan and May 2026). Physically banged up (four joint surgeries, a failed distal-bicep repair, ankle and knee problems) and in active recovery from past alcohol misuse ("California sober now," "alcohol is poison," Posts #79/#121). Started "actively trading" only in **March 2025** per his own account (Post #25) — this is a genuinely novice trader, roughly 7 months into the craft when the archive opens. Subject to **Pattern Day Trader (PDT) restrictions** for most of the archive (small account, sub-$25K), a structural handicap he references repeatedly and resents ("I quit," "PDT restriction got my hands tied," Posts #20/#24).

### Trading philosophy
There is no coherent, stated framework — this is the single biggest structural difference from a disciplined trend-following or mean-reversion voice. His own words are the best summary: *"My open options 100% reflect my ADD"* (Post #40). The closest thing to a philosophy is a **reactive, headline/momentum-chasing, small-account lotto approach**, run simultaneously across:
- Earnings-week binary options bets (F, DELL, NVDA, HIMS, NRGV, APLD) — explicitly framed as coin-flips ("it will jump. Or tank. One or the other," Post #33).
- Short-dated OTM SPY 0DTE/weekly "lottos" timed to macro/political headline risk (Trump/Truth Social posts, FOMC-adjacent days) — his most repeated, most self-aware pattern: *"one win will usually cover 5 losses"* (Post #83).
- A single-ticker obsession (**$ONDS** — Ondas Holdings, drone/defense) that dominates 22 of 152 posts and evolves from small share position → CSPs → naked calls → **leveraged ETF stacking** (`$ONDL`/`$ONDG`), producing his worst documented drawdowns.
- A late-archive pivot toward outsourcing idea-generation to AI: a Grok-generated trade thesis on $F (Post #11, Oct 2025) and, notably, building a Claude-based "signal agent" in June 2026 that he intended to connect live to a Robinhood account (Post #133) — a genuinely forward-looking behavior worth flagging given this dossier's own purpose.
- One disciplined counter-example: the **"Browndog5" 2x-leveraged experiment account** (Posts #94/#95/#106/#107/#137), opened separately with only $500, equal-weighted, explicitly stop-loss-governed going forward — his best-run, most transparent, and most profitable sleeve in the entire archive (+30% week one, +28% by March, ~+50% by mid-June).

### Post cadence
- **Overall average:** 152 posts / 47.0 weeks ≈ **3.2 posts/week** — nearly identical cadence to peer accounts in this cohort, but the shape of the curve tells the real story.
- **Hot months:** Oct 2025 (19, onboarding + Trump/SPY volatility), Jan 2026 (23) and Feb 2026 (23) — the peak of the $ONDS/leveraged-ETF obsession and the worst drawdown stretch.
- **Cold/collapsing months:** Apr 2026 (4), Jul 2026 (7), Aug 2026 (4), Sep 2026 (2, archive closes here).
- **Interpretation — a "posting death spiral," not a volatility proxy:** unlike a trader whose cadence tracks market volatility, browndog's posting frequency tracks **his own account size**. Compare posts/month to `amount_k`: 23 posts in Feb 2026 while the account collapses from ~$9K to ~$5.8K; only 4 posts in Aug 2026 as the account bleeds its final ~$3K to $0. He explicitly narrates this disengagement himself: *"I've been sitting on my hands lately and not doing a lot of trading day to day, so haven't had much to post"* (Post #111, May 2026), and *"Today's moves consist of me closing the app and just ignoring my port"* (Post #126, June 2026). **Silence here is defeat, not discipline.**

### Verified capital trajectory & drawdown history

| Date | `amount_k` | Milestone |
|---|---|---|
| 2025-10-11 | $11.46K | Archive opens |
| 2025-11-15 | **$17.93K** | **Peak of the archive** — ironically posted under the title "Bent over: I fucked myself today" |
| 2025-12-18 | $4.71K | **-74% off peak in 5 weeks** ("Fucking mess... the past week") |
| 2026-01-09 | $13.77K | Partial recovery (still -23% off peak) |
| 2026-02-05 | $5.76K–$6.64K | Second collapse — "Marriage" post: down 63% on $ONDL/$ONDG since entry; near-margin-call anxiety ("Ugh") |
| 2026-03-06 | $8.05K | Brief stabilization |
| 2026-04-03 | $4.89K | Resumed bleed |
| 2026-05-16 | $8.71K | Best mid-2026 recovery, driven by a disciplined $ONDS calls campaign (Post #117) |
| 2026-06-16 | $4.29K | Renewed decline despite "Browndog leverage account... up almost 50%" same window (side account, not reflected here) |
| 2026-07-16 | $2.00K | -89% off peak |
| 2026-08-30 | **$0.00** | **Total wipeout of tracked account** |
| 2026-09-05 | $0.00 | Archive closes; final post is a GoFundMe share for a friend's family, not a trade |

**Net read:** a **-100% drawdown from peak to zero over 9.5 months**, with two distinct violent drawdown legs (Nov→Dec 2025, -74%; and a slower bleed from May 2026 onward with no recovery). This is compounded — not purely caused — by a **real-life cash crisis**: he explicitly states he "already emptied 90% of my cash account to keep my business afloat due to slow and non-payments" (Post #55, Jan 2026), meaning at least part of the observed decline is a small-business owner raiding his trading account for payroll/working capital, not a pure trading-losses story. Both readings matter for classification: as a **trading process**, this account shows no capital-preservation discipline; as a **person**, this is a business-cash-flow victim using a trading account as an emergency fund — a dangerous combination Artemis should flag, not just his option entries.

---

## 2. Ticker Universe & Catalysts

### Core assets (mention frequency across 152 posts)

| Ticker | Mentions | Role |
|---|---|---|
| $ONDS | 22 | **Obsession ticker.** Ondas Holdings (drone/defense, "Skynet" thesis). Cycles through shares → CSPs → naked calls → leveraged ETFs over 10+ months. Source of his single largest cumulative time/capital drain. |
| $SPY | 17 | Primary lotto vehicle — 0DTE and weekly OTM calls/puts, timed to Fed/political headline risk |
| $PEW | 7 | **Toxic SPAC, never traded live in-window but referenced as his "most costly trade" for months** — a scar tissue ticker, not an active position |
| $NVDA | 7 | Recurring earnings/LEAPS conviction name that "burns him every time" by his own admission (Post #127) |
| $ONDL | 6 | 3x-leveraged $ONDS bull ETF — his primary leverage-stacking instrument |
| $GLD, $HOOD, $ONDG, $SLV, $HIMS | 4 each | $GLD/$SLV = inflation/debasement hedge sleeve (his best clean win rate); $HOOD = brokerage-as-instrument (options + natural-gas futures via Robinhood); $ONDG = second $ONDS-leveraged product; $HIMS = earnings-vol/IV-crush play |
| $HOVR, $F, $AMZN, $BULL, $IXHL, $CCCX, $MSTR, $HIMZ, $UVIX | 2 each | Smaller speculative/one-off positions |

**89 of 152 posts (58.6%) carry an explicit ticker tag** — meaning over 40% of his output is off-topic (personal life, community drama, music, health) even though this is nominally a trading account. **38 posts (25%) use explicit options terminology** (calls/puts/LEAPS/CSP/0DTE) vs. only **13 posts (8.5%)** mentioning plain shares — this is an **options-dominant, equities-light book**.

### Options vs. equities vs. macro/technical drivers
Overwhelmingly **options-first, short-dated, and catalyst-timed**:
1. **Earnings-week binaries** — F (Grok-generated thesis, Post #11), DELL, NVDA, HIMS, NRGV, APLD — entered specifically for the implied-move pop, explicitly treated as coin flips.
2. **Macro/political headline lottos** — SPY 0DTE/weekly OTM calls timed to Trump/Truth Social posting patterns (Post #99: *"tomorrow is the time for the pres to make a market fueling post"*) and Fed-week volatility.
3. **Single-name conviction with no exit discipline** — $ONDS is bought, sold, DCA'd, hedged, and leveraged with no consistent thesis beyond "believer" status and defense-sector narrative ("everyone does realize $ONDS is building Skynet," Post #98).
4. **Commodity/hedge sleeve** — $GLD and $SLV calls around metals momentum, his cleanest, most consistently profitable trade type (100%+ realized gains cited twice, Posts #76/#81).
5. **Niche/DD-driven single stock picks** — $LTRX (defense-AI microcap, +158% unrealized when posted, Post #73) and $IXHL (FDA fast-track sleep-apnea catalyst caught in real time, Post #36) — his two best examples of genuine, ahead-of-the-crowd catalyst research.
6. **AI-assisted idea generation** — outsourced a full trade thesis to Grok (Post #11, Oct 2025) and later built a Claude-based signal agent intended for live Robinhood execution (Post #133, Jun 2026) — a nascent, still-unverified behavior worth monitoring, not yet a track record.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags? Both — and inconsistently, by his own repeated admission
- **Sells winners too early:** SPY 0DTE puts cashed at **266% profit** that would have closed at **1,100-1,200%** if held (Post #132, self-titled "Classic me"); $MSTR call sold-too-late-not-too-early in the other direction — he flags being up 48% one day and failing to sell, then red the next (Post #71).
- **Holds losers / DCAs into structural weakness:** the entire $ONDS position history is one long averaging-down campaign — panic-sold shares after a dilution (June 2025), bought back in September, DCA'd through Jan-Aug 2026 regardless of price action, eventually landing on $12c's bought "about the time it went under $10" and DCA'd "until I quit throwing money at it. And it just kept sliding" (Post #147, Aug 2026) — a **year-long, unresolved bag-holding pattern** in a single name.
- **Leverage-stacking without stops (until forced to learn):** bought $ONDL/$ONDG (2x/3x $ONDS ETFs) without a stop loss, rode them to **-63%** (Post #86, "Marriage") and a separate **-46% off a +68% high** (Post #100) before stating, post-hoc, that "future buys of any significant amount will be accompanied by a stop loss" (Post #100) — a lesson stated but not consistently applied afterward.

### How he manages losing positions
- **No systematic stop-loss discipline** for most of the archive — stop losses are mentioned in only 5 of 152 posts, almost always reactively (after a loss, not before).
- **One competent hedge example:** bought protective puts against $ONDS share profits ahead of a level (Post #37, Dec 2025) — the single cleanest piece of options-as-insurance risk management in the archive.
- **Rolling losers instead of cutting them:** rolled an underwater $ONDS $10c to a further-out, higher-strike $12c rather than close (Post #87) — a classic loss-deferral move, not a loss-realization one.
- **The Browndog5 exception:** the $500 leveraged side-account is explicitly run with declared stop-loss intentions and equal-weight position sizing from inception — markedly more disciplined than the main book, and it is also the only sleeve with a clean, unbroken positive track record in the data (+30% wk1 → +28% Mar → ~+50% by mid-June).

### Documented wins vs. blow-ups

| Category | Evidence |
|---|---|
| **Best documented wins** | $IXHL FDA fast-track catch, doubled position ahead of the news (Dec 2025); $LTRX +158% unrealized on a niche defense-AI DD call (Feb 2026); $SLV calls +100%+ twice (Feb 2026); $ONDS 5/15 $10c campaign — 30 contracts @ 24.5¢ avg, sold half to cover cost + 33% return, ran the rest with a stop (Post #117, May 2026); SPY 0DTE swings up to 266-1100% (variance, not repeatability); Browndog5 leveraged sleeve, ~+50% in under 4 months on $500 |
| **Worst documented blow-ups** | $PEW — never detailed in-archive but referenced 7 times as his single costliest trade, still unresolved emotionally a year later; $ONDL/$ONDG — two separate leveraged-ETF drawdowns (-63%, -46% off a local high) inside 6 weeks; the primary account's **-100% drawdown from an $17.93K peak (Nov 2025) to $0 (Aug 2026)**; $LCID — pre-reverse-split option contracts rendered worthless/untradeable by corporate action, called "garbage" (Post #142) — a structural-mechanics loss, not a thesis failure |

**Bottom line:** this is a trader with **occasional genuine catalyst-spotting skill** (IXHL, LTRX, SLV timing) wrapped inside **zero durable risk-management process** — no consistent stop-loss usage, no position-sizing framework, chronic averaging-down into a single structurally-volatile name, and leverage-stacking without hedges. The account went from a five-figure peak to zero inside a single year, with the small, disciplined side-experiment (Browndog5) standing as the one proof-of-concept that he *can* execute well under constraints — he just doesn't apply that discipline to the primary book.

---

## 4. Behavioral & Sentiment Signals

### Why is he posting?
Three motives, shifting in weight over the archive's lifespan:
1. **Real-time emotional processing** — a large share of posts are pure venting with no trade content at all ("Fuck me," "Bent over," "Ugh," "Bipolar," "Unrealized losses") — this reads as authentic distress, escalating in frequency through the worst drawdown months (Dec 2025-Feb 2026), then fading into disengagement rather than resolution.
2. **Community and personal-life sharing, not alpha generation** — 16 of 152 posts (10.5%) are entirely off-market: his dog's two medical scares, his elbow/shoulder injury saga, a viral State Farm insurance-industry rant (his single highest-view non-trade post, 2,040 views / 22 comments), a Grateful Dead/Bobby Weir tribute, a beach-condo crowdsourcing ask, and — in the final post of the archive — a GoFundMe share for a friend's family, not a trade idea at all.
3. **Occasional genuine idea-sharing / community reciprocity** — tags niche defense-tech finds to specialists (`@Drone_Daddy`, `@TRON`, `@mphinance` on $LTRX, Post #73), calls out a suspected grifter charging a "$2,900 membership" while soliciting donations (`@x52x`, Post #41) — an anti-guru, transparency-leaning stance similar to other AH voices in this cohort.

### Recurring linguistic patterns
- **Profanity as emotional release, not bravado** — present in 25 of 152 posts (16.4%), almost always attached to losses or frustration ("Fuck you $ONDS," "fucking bullshit," "fucking mess," "fucking terrible") rather than winner-flexing.
- **Self-diagnosed impulsivity** — explicitly names his own pattern: *"My open options 100% reflect my ADD"* (Post #40); self-describes trades as done by "sometimes being retarded" (Post #120) — concerning, casual self-deprecation language that should be read as a genuine tell of impulse-control awareness without behavior change.
- **$ONDS as a love-hate relationship, narrated almost anthropomorphically** — "these 20-30% daily swings really stress me out," "I've really grown to hate this stock. It's like having a bitch of an ex with gold between her legs" (Post #129) — the single most emotionally-loaded ticker relationship in the archive.
- **Substance-use references, ambiguous tone** — "gonna get high now. Alcohol is poison," "California sober now" (recovery framing, Post #79), and a flagged, dark-humor "taking an hour or so fentanyl nap. See you on the other side" (Post #109) — this last one drew his second-highest reaction count (15) and should be treated by any human moderator/wellness layer as a genuine risk signal worth a check-in, not just trading color.
- **PDT/margin as a recurring villain** — "I quit," "PDT restriction got my hands tied," near-margin-call anxiety (Post #85) — a structurally undercapitalized trader whose account size actively prevents him from executing his own stated strategies.

### Reaction to volatility / red days
- **Mechanical red days (single-name drawdowns, options decay):** relatively calm, often self-deprecating humor ("Loss porn," "Ray of sunshine" — sarcastic captions on losing screenshots) — he has built some emotional callus here, explicitly stating "I've seen enough ebb and flow to not have panic attacks any more. Still can be a tough pill to swallow" (Post #45).
- **Margin/liquidity-threat volatility (Feb 2026 drawdown):** visibly more anxious and less composed — "Ugh... barely into margin and face potential margin calls," genuine distress language, a clear escalation beyond his baseline.
- **Broad market/macro red days:** treated opportunistically, not fearfully — 0DTE lotto buys are specifically timed to *use* red-day discounts ("thanks for the little after hours discount on $SPY calls," Post #5).

### Engagement profile
Average **2.87 reactions / 2.13 comments / 225 views** per post — a small, low-reach account (bottom of this cohort's engagement tier). His two highest-engagement moments were **not trade calls**: a prediction-market gambling post (28 reactions/33 comments) and the State Farm insurance-industry rant (2,040 views/22 comments) — his audience responds to his personality and grievances, not his trading signal.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

**Primary:** `UNDISCIPLINED_LOTTO_GAMBLER` — short-dated, high-variance options (0DTE/weekly SPY, earnings binaries) sized and exited with no consistent rule; the strategy that produced both his best single-day multiples and the bulk of his capital erosion via decay/expiry.

**Secondary:** `SINGLE_TICKER_BAGHOLDER_ONDS` — a full-year, unresolved averaging-down relationship with one structurally volatile name, escalated into leveraged-ETF stacking with no stop-loss until after two separate 45-65% drawdowns forced the lesson.

**Tertiary (positive, narrow):** `SMALL_CAP_CATALYST_SNIPER` — a genuine, if inconsistent, ability to find under-the-radar binary catalysts ahead of the crowd ($IXHL FDA fast-track, $LTRX defense-AI partnership build-out) — his only repeatable edge in the data.

**Watch tag:** `AI_ASSISTED_EXECUTION_EMERGING` — outsourced trade ideation to Grok (Oct 2025) and built a Claude signal agent intended for live execution (Jun 2026); unverified, zero track record inside this archive, but a behavior worth monitoring going forward given where this analysis originates.

**Blacklist tag (for his own book, not to copy):** `LEVERAGED_ETF_STACKER_NO_STOP` — $ONDL/$ONDG/$UVIX positions taken at meaningful size with no pre-defined exit, twice producing 45%+ single-position drawdowns.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 21 / 100**

Rationale:
- **+ (genuine catalyst-spotting, ~14 pts):** $IXHL (FDA fast-track, caught live and doubled down correctly), $LTRX (niche defense-AI microcap DD ahead of consensus), $SLV/$GLD macro-hedge timing (two clean 100%+ exits) — real, if occasional, edge.
- **+ (a working, disciplined counter-example exists, ~8 pts):** the Browndog5 side-account proves he *can* run equal-weighted, stop-governed positions profitably when he deliberately constrains himself — evidence the failure mode is behavioral, not a total absence of skill.
- **− (catastrophic, unmitigated drawdown, ~35 pts):** primary tracked account goes from a $17.93K peak to **$0** over 9.5 months — a complete account failure, the single most negative fact in this dossier and worse than any peer profile reviewed in this cohort to date.
- **− (no risk-management process on the primary book, ~15 pts):** stop losses appear in only 5 of 152 posts, almost always after the fact; chronic DCA-into-weakness on $ONDS; leverage-stacking without hedges twice in six weeks.
- **− (structural undercapitalization, ~4 pts):** PDT-restricted for most of the archive, meaning his own stated strategies are frequently unexecutable — this is a capital-adequacy problem the platform/Engine cannot fix by following his calls.

**Expectancy: NEGATIVE, in aggregate, on the primary book.** The `amount_k` series is close to a full, continuous equity curve for this trader (rare in this cohort) and it resolves to a clean, unambiguous answer: **total capital destruction**. Narrowly filtered to his catalyst-DD calls (IXHL/LTRX-style) and metals-hedge timing (GLD/SLV), expectancy is plausibly **modestly positive** and worth harvesting as an idea-generation layer — but never as a sizing or exit template.

### 5.3 Signal Flow Ingestion Matrix

| Post Signature | Underlying Signal Type | Reliability | Artemis Action |
|---|---|---|---|
| Niche microcap DD call-outs (e.g. $LTRX defense-AI partnerships, $IXHL FDA catalyst) | Ahead-of-consensus fundamental catalyst spotting | Moderate-High (small sample, but both hits were early and correct) | **INGEST** as raw research tips for independent verification |
| $GLD/$SLV commodity-hedge entries and exits | Macro debasement/inflation-hedge timing | Moderate-High (two clean 100%+ round trips) | **INGEST** as a timing overlay on the Engine's own metals-flow module |
| Earnings-week binary options entries (F, DELL, NVDA, HIMS, NRGV, APLD) | Discretionary volatility gamble | Low — explicitly self-described as coin flips | **DO NOT COPY** — sentiment color only |
| $ONDS position updates (any form: shares, calls, CSPs, $ONDL/$ONDG) | Single-name emotional over-attachment | Low — negative expectancy, a full-year unresolved drawdown | **FADE / BLACKLIST** — treat any fresh $ONDS conviction post from him as a contrarian tell, not a follow signal |
| SPY 0DTE/weekly lotto entries timed to political/Fed headline risk | Discretionary macro-headline gamble | Low-Moderate, extremely high variance | **DO NOT COPY sizing**; may be logged as a retail-crowd-positioning data point only |
| Leveraged-ETF entries ($ONDL/$ONDG/$UVIX) without a stated stop | Undisciplined leverage-stacking | Very Low — confirmed 45-65% drawdown pattern, twice | **FIREWALL** — never ingest a leveraged-ETF entry from this account without an independent stop-loss overlay |
| Browndog5 (small, stop-governed, equal-weight leveraged experiment) updates | Disciplined process, small sample | Moderate (short track record, but internally consistent and transparent) | **WATCH-LIST** — a genuinely different behavioral mode; worth re-evaluating if he scales it |
| AI-assisted idea generation posts (Grok trade thesis, Claude signal agent) | Meta-signal about retail AI-tool adoption | N/A for trading, informative for platform strategy | **LOG, do not trade** — track as a leading indicator of retail AI-agent adoption trends |
| Off-topic personal/health/business posts | Not a trading signal | N/A | **IGNORE for trading**; flag fentanyl/substance-reference posts for a wellness-review layer if one exists |
| "Loss porn" / self-deprecating red-day posts | Emotional venting | N/A | **IGNORE** for signal; usable only as a retail-sentiment-temperature data point |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Pull his **early-stage microcap/DD call-outs** ($LTRX-style: niche defense/AI names with real partnership or contract catalysts, posted well ahead of broad coverage) as raw research tips for independent fundamental verification — this is his one demonstrated area of genuine pattern-recognition value.
2. Use his **$GLD/$SLV entry and exit timing** as a soft overlay signal on the Engine's own metals/inflation-hedge module — small sample, but both documented round trips were clean and well-timed.
3. Log any future **AI-assisted signal-generation posts** (he has already built one Claude-based agent) as a leading indicator of retail-side AI-agent adoption — informational for platform strategy, not a trading input.

**Contrarian Fade Directives (when to fade him / the retail herd):**
1. **Treat any fresh $ONDS conviction post as a contrarian signal, not a follow signal** — a full year of unresolved, escalating bag-holding in this single name is the strongest, most consistent negative-expectancy pattern in the entire archive.
2. **Fade his earnings-week binary option entries directly** — he self-describes these as coin flips; his actual fills carry no demonstrated edge.
3. When he posts a **leveraged-ETF position with no stated stop-loss**, treat that specific absence as the risk signal itself — it has preceded 45%+ single-position drawdowns twice.

**Mandatory Risk Blacklists & Firewalls:**
1. **Blacklist $ONDS-adjacent leveraged products ($ONDL, $ONDG) from any copy-signal pipeline sourced from this account** — confirmed, repeated, undhedged drawdown source.
2. **Never size a position off his self-reported percentage returns** (e.g., "266% profit," "+50%") — base amounts are inconsistently disclosed and several figures reference a separate, undertracked side-account.
3. **Firewall any signal sourced from this trader during a documented margin/liquidity-stress window** (his Feb 2026 near-margin-call period) — decision quality visibly degrades under his own financial stress, per his own admission.
4. **Do not treat post-cadence as a volatility proxy for this trader** — unlike disciplined-process peers, his silence correlates with capital destruction and disengagement, not calm markets; a drop in his posting frequency is not itself informative for market-state inference.

**Exit Rules & Alpha Rectification:**
1. Any idea sourced from his microcap DD call-outs should carry a **hard, pre-defined stop-loss and profit-take band set by the Engine**, never inherited from him — his own exit discipline is the weakest link in every one of his winning trades (sold too early on SPY 0DTE puts, too late on $MSTR calls).
2. If the Browndog5-style small, equal-weighted, stop-governed pattern ever reappears at scale on his primary account, re-score this profile — it is the only evidence in the archive that this trader's process, not just his instincts, can be net-positive under the right constraints.
3. Apply a **hard account-level circuit breaker analog** in any Engine logic inspired by this profile: the single clearest lesson of this dossier is that an undercapitalized account with no stop-loss discipline and real-life cash-flow bleed can go from a five-figure peak to zero in under a year — position-size and total-exposure caps should be non-negotiable defaults, not optional overlays.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone / Catalyst | Notes |
|---|---|---|
| 2025-10-11 | First archive post ("Shopping" — $ASTS/$HOVR/$JEDI) | Account already active pre-archive; self-reports trading "since March 2025" |
| 2025-10-13 to 10-15 | Early SPY options wins; $HOVR +30% day; $SMCI earnings speculation | Establishes the earnings/momentum-lotto pattern from week one |
| 2025-10-30 to 10-31 | $ONDS position opened; $PEW losses first referenced ("wish in one hand"); $AMZN/$NVDA earnings wins (+25% cash-account day) | $PEW becomes a recurring scar-tissue reference for the rest of the archive |
| 2025-11-05 to 11-07 | PDT-restriction frustration ("I quit"); $ONDS "DD" panic post predicting $0 shares | First sign of the $ONDS emotional volatility pattern |
| 2025-11-15 | **Archive peak: $17.93K tracked account value** | Posted under the title "Bent over: I fucked myself today" — peak coincides with a loss narrative, an early tell that the account's real trajectory and his real-time mood are not synced |
| 2025-11-25 | $DELL and $NVDA LEAPS entries | Broadens into semis/AI-adjacent conviction names |
| 2025-12-03 | $IXHL FDA fast-track catalyst caught live, position doubled | Best documented catalyst-spotting trade in the archive |
| 2025-12-18 | Account at $4.71K — **-74% off the Nov 15 peak in five weeks** | "Fucking mess" post; first explicit acknowledgment of accumulated pain |
| 2026-01-02 | $ONDS profits taken across shares/calls; sells into CSPs/puts to reduce exposure | A rare example of proactive de-risking |
| 2026-01-07 | **Discloses draining 90% of cash account for business cash-flow needs** | Critical confound for reading the rest of the equity curve as pure trading performance |
| 2026-01-09 | 500-contract prediction-market wager posted (28 reactions/33 comments — highest engagement of the archive) | Gambling behavior extends beyond equities/options into prediction markets |
| 2026-01-30 to 02-05 | $ONDL/$ONDG leveraged-ETF drawdown to **-63%**; near-margin-call anxiety ("Ugh," "Marriage") | Second major drawdown leg; first explicit margin-stress language |
| 2026-02-02 | $LTRX niche defense-AI DD call-out, +158% unrealized at post time | Second-best catalyst-spotting trade in the archive |
| 2026-02-27 | **"Browndog5" $500 2x-leveraged experiment account opened** (PTIR/ONDL/CONL/ASTX/UVIX, equal-weighted) | His most disciplined, most transparent trading initiative — explicitly stop-loss-oriented from inception |
| 2026-03-06 to 04-03 | Browndog5 updates: +30% week one, +28% by end of March; $UVIX sold for 68% | Clean, positive, small-sample track record on the side account |
| 2026-05-11 to 05-14 | $ONDS 5/15 $10c campaign — DCA'd 30 contracts, sold half to lock in cost + 33%, ran the rest with a stop | His most process-disciplined single trade on the primary account |
| 2026-06-09 | **Starts building a Claude-based "signal agent"**, intends to connect it live to a Robinhood account with $500 | First documented AI-assisted-execution experiment |
| 2026-06-16 | Browndog leverage-account update: **up almost 50%** (highest-viewed post in the archive, 7,032 views) | Side-account success draws by far his largest audience — bigger than any primary-account content |
| 2026-06-22 | Viral State Farm insurance-industry rant (2,040 views/22 comments) | Confirms his audience engages with his personality/grievances over his trading calls |
| 2026-07-16 | Primary account at $2.00K — **-89% off the Nov 2025 peak** | "Losing day? Still a winner." — dark humor as the account nears zero |
| 2026-08-03 | Final $ONDS position update — still DCA'd into a stock that "just kept sliding" | Closes out the year-long $ONDS bag-holding thread on an unresolved, unprofitable note |
| 2026-08-30 | **Primary tracked account reaches $0.00** | No explicit "I'm done" post — the wipeout is visible only in the structured data, not narrated |
| 2026-09-04 | Final trade post: "$40 to the wind," five contracts at $0.09 with stops at $0.05 — explicitly labeled "Retarded" | Degenerate, self-aware, tiny-size lotto play — the account's terminal state in miniature |
| 2026-09-05 | Archive closes on a GoFundMe share for a friend's family, not a trade | The account's final post is entirely non-financial |

---

*End of dossier. Prepared from `@browndog_lifetime.md` (152 posts, full text) and `@browndog_all_posts.json` (structured metadata) with no external data sources.*
