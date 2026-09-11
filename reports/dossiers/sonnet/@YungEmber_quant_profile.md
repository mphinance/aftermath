# QUANT PROFILE DOSSIER: @YungEmber

**Classification:** Forensic Trader Autopsy — Artemis Signal Ingestion Program
**Subject Rank:** #22 Most-Active Followed Trader (AfterHour)
**Sample:** 448 lifetime posts, 2025-04-04 → 2026-09-09 (522 days)
**Sources:** `@YungEmber_lifetime.md` (posts/reports), `@YungEmber_all_posts.json` (raw, incl. Kinfo-linked `amount_k` verified portfolio snapshots)
**Analyst:** Sonnet — Artemis Engine
**Date Compiled:** 2026-09-10

---

## 0. TL;DR Verdict Box

| Field | Value |
|---|---|
| Primary Tag | `CONCENTRATED_STORY_STOCK_HODLER` |
| Secondary Tag | `DD_DRIVEN_MOMENTUM_SWINGER` |
| Tertiary Tag | `MEME_SQUEEZE_TOURIST` (minor, opportunistic) |
| Alpha Score | **58 / 100** |
| Expectancy | **Positive but fat-tailed** — verified capital +145% lifetime, but round-trips ~40-64% drawdowns twice without systematic profit-taking |
| Verified Capital (start → peak → current) | $768K → $3,110K → $1,882K |
| Max Drawdown | **-63.8%** (Oct 6 2025 → Nov 6 2025, ONDS/HUMA collapse) |
| Edge Type | Genuine — early catalyst identification + high-effort fundamental DD on small/micro-cap names |
| Fatal Flaw | Zero documented profit-taking discipline; converts unrealized gains back into unrealized losses on the same 2-3 tickers, repeatedly |
| Recommended Posture | **Selective ingest of entry theses; hard fade on his "still holding," "conviction unchanged," and post-peak silence signals** |

---

## 1. Executive Profile

### Philosophy (in his own words, evolving)
Two distinct eras are visible in the data:

- **Era 1 — "Macro Generalist" (Apr–Jun 2025).** Opens with a genuinely diversified, thesis-driven global-macro book: `$MP` (rare earths), `$VNM`/`$INDA`/`$SMIN`/`$EWW`/`$EWM`/`$EWS` (China+1 nearshoring basket), `$SGOL` (gold hedge), `$MSTR`/`$MSTY` (BTC proxy + income overlay). Self-description: *"Positioned, not predicting."* This is the most risk-aware version of the account.
- **Era 2 — "Concentrated Story-Stock Gambler" (Jul 2025 → present).** The diversified basket is abandoned in favor of 2-4 concentrated, highly volatile small/micro-cap "narrative" positions (`$ONDS`, `$HUMA`, `$NRGV`, later `$HUBC`). Position sizing balloons — six-figure share counts (300K `HUMA` shares, 1,000 `HUMA` option contracts, 22K `ONDS` shares) become normal. Philosophy shifts from portfolio construction to single-name conviction-holding, evangelized almost religiously (*"You are doing so good! It doesn't matter that no one is talking about you. They just don't understand you like I do."* — talking to his own `$NRGV` position).

### Post Cadence
- **448 posts / 522 days ≈ 6.0 posts/week** lifetime average — but cadence is extremely lumpy, tracking his own P&L intensity, not a fixed schedule.
- Cadence peaks (>45 posts/month) coincide with active DD campaigns or violent price action: Jun 2025 (58), Oct 2025 (49, the HUMA 16-part DD series), Jan 2026 (74, highest ever).
- Cadence has **collapsed in the most recent quarter**: Jul 2026 (4 posts), Aug 2026 (5 posts), Sep 2026 (1 post through the 9th) — a >90% falloff from the Jan 2026 peak. This directly follows the HUBC-squeeze-mania drawdown (see §1 Drawdown History) and is a classic burnout/disengagement tell, not a change in trading activity per se.
- Posting clusters at 13:00-23:00 UTC (~9am-7pm ET, spilling into evening), consistent with live market-hours reaction plus after-market recap posting.

### Verified Capital Trajectory (Kinfo-linked `amount_k`, in $K)
```
$3,200 |                                    .*.  (3,110 peak, Jun 2 '26 — HUBC mania)
$3,000 |                                   *   *
$2,800 |                    .* (2,803 — Oct 6 '25)
$2,600 |                   *  *
$2,400 |                  *    *
$2,200 |     *           *      *
$2,000 |    * *    *    *        *                    * (1,882, Sep 9 '26 — current)
$1,800 |   *   *  * *  *          *                  *
$1,600 |  *     **   **            *                *
$1,400 | *                          *              *
$1,200 |*                            *            *
$1,000 |                              * (1,015 — Nov 6 '25 trough, -63.8% in 31 days)
  $800 |*  (768 — first observed, Apr '25)
       +------------------------------------------------------------------
        Apr'25   Aug'25    Oct'25   Jan'26    Apr'26   Jun'26   Sep'26
```
- **Lifetime**: +145% net (768K → 1,882K) over 17 months — the headline number is genuinely good.
- **But it masks two full round-trips**: he has been *higher* than his current mark **twice** (Oct '25 @ 2,803K, Jun '26 @ 3,110K) and given almost all of both peaks back. As of this writing he sits below where he was 11 months ago at the Oct 2025 peak.
- **Anomaly flag**: two posts (2025-08-09, 2025-08-11) and one (2025-08-13) show `amount_k` briefly negative (-$154K to -$164K) sandwiched between +$1,600K readings the day before and after. Content of those posts is unrelated commentary about a *different* trader's ("The Viking vs. The Grifter") blown-up challenge and routine ONDS DD — not his own blowup. This is almost certainly a **Kinfo sync/data artifact**, not a real capital event; treat as noise, not signal.

---

## 2. Ticker Universe & Catalysts

### Concentration
Of ~366 total ticker mentions across 448 posts, **three names account for 44%**:

| Ticker | Mentions | % of Universe | Role |
|---|---|---|---|
| `$ONDS` (Ondas Holdings) | 76 | 20.8% | Core conviction position, drone/comms defense story, held since ~mid-2025 |
| `$HUMA` (Humacyte) | 56 | 15.3% | Core conviction position, biotech/med-device, subject of a 16-part DD series (Oct '25–Jun '26) |
| `$MP` (MP Materials) | 30 | 8.2% | Legacy Era-1 rare-earth thesis, largely rotated out by mid-2025 |
| `$HUBC` (BlackSwan Tech) | 17 | 4.6% | Opportunistic micro-float squeeze chase (May–Jun 2026), ~9,000% reported SI on a ~1.2M share float |
| `$NRGV` (Energy Vault) | 15 | 4.1% | Secondary conviction name, energy storage narrative |
| `$OSS`/`$TSLA`/`$UNH`/`$MSTY`/`$MSTR` | 12/11/11/10/10 | ~2-3% each | Options-income overlay names (covered calls) + occasional macro plays |

Long tail (30+ additional tickers, 1-8 mentions each) is almost entirely small/micro-cap speculative names: `$ONDL`, `$LPTH`, `$UUUU`, `$ACHR`, `$LTBR`, `$BKSY`, `$UMAC`, `$OPTT`, `$DDD`, `$SOC` — a coherent thematic cluster of **drones/defense, critical minerals, and energy-transition micro-caps**.

### Options vs. Equities
Heavy options usage — `calls` (45 mentions), `puts` (19), `LEAPS` (17), `covered calls` (18), `options` (47). Two distinct option behaviors:
1. **Speculative directional leverage** on core names (1,000 `HUMA` contracts, `ONDS` LEAPS, `HUMA` Jan 2028/2029 LEAPS as a share-to-option position conversion after selling stock).
2. **Income overlay** via covered calls on large, liquid names (`$MSTR`, `$TSLA`, and his own `$ONDS`/`$HUMA` stock once positions get large — e.g., 1,000 `$5` covered calls on `ONDS` when it was sub-$2, later rolled to $17 strike).

### What Drives Entries
- **Fundamental/catalyst-driven DD**, not chart-technical. Multi-thousand-word due-diligence essays (the 16-part `$HUMA` series covers pricing power, FDA timeline, insider Form-4 mechanics, manufacturing margins, bear case, analyst snapshot). This is real analytical effort, not a shallow gambler's pitch.
- **Macro/thematic overlays** early on (China-decoupling, rare earths, tariff policy, credit-rating downgrades) — largely abandoned as the book concentrated.
- **Dilution/cash-runway tracking as a bullish *and* bearish signal** — 32 mentions of "dilution," often reading a capital raise as "they're about to light the fuse on something big" (bullish reframing of a red flag).
- **Social/momentum chasing** for the `HUBC` squeeze — entry rationale here is thin ("This is dumb" / "still dumb but less dumb"), self-aware that the fundamental case doesn't hold, purely riding float-lock/short-interest mechanics.
- **Red-day reactivity**: multiple posts explicitly timed to market-wide drawdowns ("On big red days," "If we have another red day tomorrow," "Correction was needed") — he posts *more*, not less, into volatility, largely to reassure himself and his following.

---

## 3. Risk Management & PnL Reality

**Verdict: He does not take systematic profits. He holds bags, articulately.**

Textual evidence across all 448 posts:
- `"trim"` / `"trimmed"`: **1 occurrence total**
- `"sold half"`: **1 occurrence**
- `"take profit"`: **1 occurrence**
- `"stop loss"` / `"stop-loss"`: **0 occurrences**
- `"hold"`: **88 occurrences**
- `"conviction"`: **19 occurrences**, always used to justify *staying* in a position through drawdown, never to size into strength before scaling out

The `Loss`-tagged posts (only 3 self-tagged in 448 — he almost never labels his own posts as losses) are revealing precisely because of how he frames drawdowns:
1. *"Port is up $50K today and I'm still salty"* — a genuine gain framed with a loss tag because a rival position lagged.
2. *TSLA robotaxi play* — sold covered calls "to mitigate the pain" after a bad entry, then **bought more shares at the low** (averaging into weakness rather than cutting).
3. *"Time will tell if this was a good move"* — sold 300K shares of `HUMA` (his largest position) after a prolonged decline, immediately redeployed 100% into `$ONDL` and pledged to rebuild the `HUMA` exposure via 2028 LEAPS. Net effect: capital never actually de-risks, it just rotates vehicle.

### Documented Wins
- Apr 28 → Jun 3 2025: +$275K in 5 weeks (957K → 1,155.9K), attributed to the Era-1 macro basket plus early `HUMA`/`ONDS` entries.
- Oct 3 2025: *"Up $1M YTD. 49 days later and I'm now up $2M YTD"* — the single best-documented stretch, driven by `ONDS` (+$275K in one day, "Lambo Day") and `HUMA` options (1,000 contracts +50% in a day).
- May 28–Jun 2 2026: `HUBC` squeeze positioning + `ONDS` strength pushes the account to its lifetime peak, $3,109.8K.

### Documented Blow-ups
- **Oct 6 → Nov 6, 2025: -63.8% drawdown** ($2,803K → $1,015K) in 31 days. Driven almost entirely by `$ONDS` and `$HUMA` giving back the September/early-October run — he kept publishing the HUMA DD series *through* the entire decline (parts 8-16 all posted while the portfolio was cratering), never pausing to reduce size. Tone shifts from triumphant ("Lambo Day") to profane venting at the ticker itself ("Hey $ONDS, here's a movie rec for your bitch ass. Chill out and stop being a ho.") — anger displacement onto the position rather than a risk decision.
- **May 29 → Jul 14, 2026: -42.5% drawdown** ($3,110K → $1,788K). Follows the `HUBC` squeeze failing to materialize as scripted ("Still not a squeeze; not even close" at the exact top) plus renewed `HUMA`/`ONDS` weakness (another dilutive raise in June: *"This won't be the last raise... Expect another raise before the finish line"* — he correctly forecasts the dilution but keeps buying LEAPS into it anyway).
- Post-Jul-2026 the account partially stabilizes in the $1,800-2,450K band but never revisits the $3,110K peak; cadence collapse suggests disengagement rather than resolution.

**Net PnL Reality**: The lifetime trend line is up, but almost entirely due to two explosive momentum windows (Sep-Oct '25, May-Jun '26) that he then gives back 40-64% of because there is no exit discipline. This is a **positive-expectancy idea generator wrapped in negative-expectancy position management.**

---

## 4. Behavioral & Sentiment Signals

### Why he posts
Three overlapping motives, in descending order of post volume:
1. **Community entertainment/status** — 44 `Funny`-tagged posts, running bits ("Praise Be" to "The Algo," "The Characters of AfterHour" satire, self-mocking "💅" as a verbal tic on good days), a self-funded $3,000 stock-picking contest for three followers (Dec 2025) — he's a de facto community figure, not just a poster.
2. **Public accountability / DD-as-content** — the 16-part `HUMA` series and equivalent `NRGV`/macro essays are clearly written to build a reputation as the platform's serious fundamental analyst, distinct from the meme crowd.
3. **Emotional processing of drawdowns** — posting *increases* during red days and personal drawdowns rather than decreasing, functioning as public venting/self-reassurance ("the louder they get, the stronger my conviction becomes").

### Linguistic tics (recurring)
- Feminine pronoun for his own tickers when they move ("She movin' this morning," "Let's see if she finishes above $9").
- "💅" as a sign-off emoji specifically on days he's up big or being flippant about risk.
- Direct venting *at* his own positions when they underperform ("bitch ass," "little bitch," "chill out and stop being a ho").
- "Imma" / AAVE-inflected casual register throughout, contrasted sharply with the formal, cited, spreadsheet-precise tone of his DD posts — a deliberate two-register style (shitpost voice vs. analyst voice).
- Recurring antagonists/allies named directly: `@RagnarL`, `@Zennn`, `@ecaz`, `@bobdog`, `@TexasThumps`, `@SirJack` — feud and camaraderie content is a real driver of engagement (his single highest-comment post, 126 comments, is drama-adjacent: *"Since a duel is illegal and logistically challenging…"*).

### Reaction to volatility / red days
Explicitly contemptuous of panic-sellers and fair-weather critics: *"Funny how they go silent on green days... your red day is the highlight of their week."* He frames holding through drawdowns as a moral/psychological virtue rather than a risk decision — this is the same instinct that produces the -63.8% and -42.5% drawdowns. He does not distinguish between "conviction that should be held" and "sunk cost that should be cut."

### Side-gambling tell
Dec 19, 2025 (`Yolo` tag, the only one in 448 posts): took profits from `$ONDS` calls specifically to fund a **Jake Paul fight prediction-market bet** plus "a few other smaller prediction market plays." The one time he explicitly banks options profits, the capital is redeployed into unrelated entertainment gambling rather than compounded or de-risked — reinforcing that "taking profit" for this trader means "funding the next bet," not "reducing exposure."

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

| Priority | Tag | Rationale |
|---|---|---|
| **Primary** | `CONCENTRATED_STORY_STOCK_HODLER` | 44% of ticker mentions in 3 names; documented refusal to trim through two >40% drawdowns |
| **Secondary** | `DD_DRIVEN_MOMENTUM_SWINGER` | Entries are catalyst/fundamental-driven, not technical; genuine multi-week research cycles precede size-up |
| **Tertiary** | `MEME_SQUEEZE_TOURIST` | Opportunistic, self-aware, small-book excursions into extreme micro-float names (`HUBC`) when one is trending |
| Watch-flag | `OPTIONS_INCOME_OVERLAY` | Secondary behavior — sells covered calls against large winners (`ONDS`, `HUMA`, `MSTR`, `TSLA`) once positions get large, which caps upside but also signals when he considers a name "core" |

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 58 / 100**

| Component | Score (/25) | Notes |
|---|---|---|
| Idea Generation / Catalyst ID | 21/25 | Genuinely early and well-researched on `ONDS`/`HUMA`; macro thematic calls in Era 1 were directionally sound |
| Risk-Adjusted Execution | 9/25 | No stop-loss vocabulary, near-zero profit-taking, two documented 40-64% drawdowns on concentrated single names |
| Consistency / Repeatability | 14/25 | Same failure mode both times (holds through the DD series while price craters); pattern is mechanical enough to model and fade |
| Capital Discipline | 14/25 | Verified lifetime capital is up +145%, a real result — but achieved despite process, not because of it; degrading engagement (posting collapse) since the last drawdown |

**Expectancy**: Positive over the observed 522-day sample (net capital growth), but with a **fat left tail** — two round-trip drawdowns of comparable magnitude to the total gain. A strategy that mechanically **copies his entries but imposes exogenous exit discipline** (see §5.4) would very likely outperform his own realized return.

### 5.3 Signal Flow Ingestion Matrix

| Signal Type | Example Trigger | Ingest? | Action | Confidence |
|---|---|---|---|---|
| New multi-part DD series launch on a small/micro-cap | `$HUMA Series Post 1: ...` | ✅ YES | Flag ticker for independent fundamental review; treat as early-catalyst radar, not a buy signal | Medium-High |
| "Buying more" / conviction reaffirmation during a drawdown | *"They just don't understand you like I do"* re: `$NRGV` | ⚠️ FADE-WATCH | Do not follow the add; log as a bagholding continuation signal, watch for capitulation | High (contrarian) |
| Options flow disclosure (contract count + strike) | "1,000 $HUMA contracts... up 50%" | ✅ YES | Useful real-time confirmation of retail options flow crowding into a name | Medium |
| Micro-float / extreme-SI squeeze post | `$HUBC`, "600%+ SI," sub-$1 stock | 🚫 BLACKLIST | Do not ingest as directional signal; log only as a retail-herd sentiment extreme | Low (noise) |
| Portfolio milestone / "up $X since last update" | "Up $1M YTD... now up $2M YTD" | ⚠️ NEUTRAL | Confirms momentum is real and recent; do not extrapolate — historically precedes a round-trip within 4-8 weeks both times observed | Medium (timing tell) |
| Silence / posting-cadence collapse after a drawdown | Jul-Sep 2026 (4, 5, 1 posts) | ⚠️ FADE-WATCH | Historically marks the bottom-ish stabilization zone for HIM, but is a lagging, low-conviction signal for the engine | Low |
| Dilution/raise commentary framed bullishly | "diluting again... about to light the fuse" | ⚠️ FADE-WATCH | His bullish reframe of dilution has a mixed hit rate (`ONDS` worked once, `HUMA` raises have generally preceded further downside) | Low-Medium |
| Sold-position-into-new-position rotation | Sold `HUMA` shares → 100% into `$ONDL` | 🚫 DO NOT MIRROR | Represents an un-derisked lateral rotation, not a real risk reduction; following it inherits his concentration risk under a new ticker | N/A |
| Covered-call strike/roll disclosure on a core name | Rolled `ONDS` CCs $5→$17 strike | ✅ YES | Genuine, verifiable data point on his true cost basis and conviction level in that name | Medium |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest)**
1. Treat every new @YungEmber multi-part DD series launch as a **research trigger, not a trade trigger** — route the named ticker to an independent Artemis fundamental screen within 24 hours of the first post in a series.
2. His **catalyst timing on dilution/cash-runway events** is worth tracking as a leading indicator even when his own directional call is wrong — he reliably surfaces the *event* (raise size, use of proceeds, runway math) before it's widely discussed.
3. Options contract/strike disclosures on his core names are usable as **real-time retail options-flow confirmation** for names already on an Artemis watchlist — corroborating signal, not primary.

**Contrarian Fade Directives (when to fade him / the retail herd around him)**
1. **Fade any "conviction unchanged" or address-the-ticker-directly post made *during* a >20% drawdown from a recent peak in that name.** This is his single most consistent tell (`ONDS` Nov 2025, `HUMA` throughout the 16-part series decline) and has a documented 100% hit rate in-sample for "further downside or prolonged chop before recovery."
2. **Fade micro-float/extreme-SI squeeze entries (`HUBC`-type)** — these are opportunistic, thesis-light, and his own copy ("still dumb," "can't make sense of this ticker") signals he knows it's not a real edge; treat his participation as a retail-herd extreme, not alpha.
3. **Fade "up $X since last update" milestone posts as a near-term top signal**, not a momentum-continuation signal — both of his largest verified peaks (Oct '25 $2.8M, Jun '26 $3.1M) were reached within days of a self-congratulatory milestone post and were followed by 40%+ drawdowns within 4-8 weeks.

**Mandatory Risk Blacklists & Firewalls**
1. **Never size-mirror his position disclosures.** His share/contract counts reflect a concentrated, high-risk-tolerance account (300K shares of a single biotech name, 1,000 options contracts on a sub-$5 stock) inappropriate for a diversified signal-following strategy.
2. **Blacklist sub-$1 / sub-2M-float squeeze names sourced from his posts** (`HUBC`-class) — his own commentary admits the fundamental case is absent; short-interest figures he cites from social sources (9,000% SI on a 13K-share float) are unverifiable and should never trigger position sizing.
3. **Do not treat "sold X to buy Y" rotation posts as risk-off signals.** Verified pattern: he rotates capital laterally between correlated speculative names (`HUMA` → `ONDL`, shares → LEAPS) without ever reducing net thematic exposure. The engine should log these as concentration-risk *persistence*, not reduction.
4. **Firewall his prediction-market / entertainment-gambling disclosures entirely** — one-off, not a repeatable pattern, zero relevance to equity/options signal generation.

**Exit Rules & Alpha Rectification**
1. Because he has no observed profit-taking discipline, any Artemis strategy that ingests his entries **must impose its own exit logic** — a hard trailing-stop or scaled-profit-taking rule (e.g., trim 25% at +30%, 25% at +60%, trail the remainder) should be bolted on to any signal sourced from this trader, since his realized returns are provably worse than his unrealized peak returns twice over.
2. Use his **peak-milestone posts as the trim trigger** for any position the engine is running in a name he's also concentrated in — his own psychology makes him a reliable late-cycle buyer/holder, so his celebration posts are usable as a distribution-phase proxy.
3. Cap any single-name exposure sourced from his DD at a **fraction of what he discloses** (e.g., 10-20% of his position-scaled equivalent) precisely because his position sizing is calibrated to a risk tolerance that has produced two 40-64% account drawdowns.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Portfolio ($K) | Event |
|---|---|---|
| 2025-04-04 | 768.0 | First observed post; account already funded (references "two linked accounts") |
| 2025-04-17 | ~840 | "How I'm positioned" — diversified Era-1 macro basket (rare earths, China+1 EM basket, gold, MSTR/MSTY) |
| 2025-04-28 | 957.0 | Milestone: +$80K since transparency post |
| 2025-06-03 | 1,155.9 | Milestone: +$195K since Apr 28 |
| 2025-08-09/11/13 | -154 to -164 (anomalous) | Data-artifact dip coinciding with unrelated commentary on another trader's blown-up challenge — not a real drawdown |
| 2025-09 | 1,570 → 2,297 | Sharp run-up begins, `ONDS`/`HUMA` become dominant positions |
| 2025-10-02/03 | 2,494 → 2,636 | "Lambo Day" (+$275K on `ONDS` in one day); "Decent timing" (`HUMA` options +50% in a day); "Up $1M YTD... now up $2M YTD" |
| 2025-10-06 | **2,803.2 (local peak #1)** | "Buying some $ZG options" — top of the first major run |
| 2025-10-21 → 11-05 | 1,887 → 1,432 | 16-part `$HUMA` Definitive DD Series published *while the position bleeds* |
| 2025-11-06 | **1,015.3 (trough #1, -63.8% from peak #1)** | "Hey $ONDS, here's a movie rec for your bitch ass" — venting at the position |
| 2025-11-18 | 1,725.4 | Partial recovery |
| 2025-12-12 | ~1,900 | Self-funds a $3,000 ($1K x3) "Funded Portfolio Manager Challenge" for followers |
| 2025-12-19 | ~1,950 | Only `Yolo`-tagged post: takes `ONDS` options profit to bet on a Jake Paul fight + prediction markets |
| 2026-01 | 1,945 → 2,879 | Highest-cadence month (74 posts); steady climb |
| 2026-02-05 | 2,124.9 | Sells remaining 300K `HUMA` shares, rotates 100% into `$ONDL`; plans to rebuild `HUMA` via 2028 LEAPS |
| 2026-03-06 | ~2,300 | "The Characters of AfterHour" — self-aware community satire post |
| 2026-05-11 | 2,200.5 | Opens `$HUBC` position (25K shares) — "This is dumb" |
| 2026-05-27 | 2,699.4 | `$HUBC` "calculation error" post — ~9,000% SI claimed on a 13K-share float |
| 2026-05-29 → 06-02 | 2,855 → **3,109.8 (lifetime peak)** | `$HUBC` squeeze mania + `$ONDS` strength; "Still not a squeeze; not even close" posted at the exact top |
| 2026-06-11 | 2,290.8 | Correctly forecasts another `HUMA` dilutive raise ("This won't be the last raise") — buys LEAPS into it anyway |
| 2026-06-18 | n/a | Rotates 22K `ONDS` shares → 18K `ONDL` shares |
| 2026-07-14 | **1,787.7 (trough #2, -42.5% from peak #2)** | "Follow me on Legend" — signals platform migration/disengagement |
| 2026-08-14 | 2,269.3 | "Why is AfterHour in a State of Decline" — highest-view post of the sample (3,001 views), reflective/community-decline essay |
| 2026-09-09 | 1,881.7 | Most recent post: "Last PR was August 18 for $ONDS" — cadence has collapsed to ~1 post/month, waiting on a catalyst |

---

*End of dossier. Compiled by Sonnet for the Artemis Engine, TraderMatrix ingestion pipeline.*
