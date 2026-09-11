# Quant Forensic Dossier: @Drone_Daddy

**Subject:** AfterHour trader `@Drone_Daddy` (Profile ID `prf_c17113f31d1c4646bbe68badc6742876`)
**Rank:** #14 most-active followed trader by lifetime post count
**Sample size:** 988 lifetime posts, 2024-12-17 → 2026-09-10 (631 days), including a **123-day total silence** (2025-02 through 2025-06) — a continuous but *not* uninterrupted history
**Sources:** `@Drone_Daddy_lifetime.md` (formatted archive), `@Drone_Daddy_all_posts.json` (raw, incl. `amount_k` account-value snapshots, tags, engagement counters), cross-tabulated programmatically (ticker extraction, cadence, drawdown reconstruction, keyword/monetization scan)
**Analyst:** Artemis Forensic Desk · 2026-09-10

> **Headline finding:** @Drone_Daddy is not primarily a trader who posts — he is a **single-name research/content business (Hidden Gems Research LLC, launched Nov 2025) built on top of a trader** who has run his flagship position ($ONDS and its two satellite tickers, $UMAC/$LPTH) through **two separate ~90%+ boom-bust cycles on the same tracked account** while his follower count and engagement climbed the entire time. His self-tagged win rate (117 `Gain` vs. 4 `Loss`, 29:1) is worthless as ground truth: the tracked account went **$77,290 → $2,848 (−96.3%) between 2025-08-10 and 2025-09-25**, and a second time **$34,729 (2026-01-03) → ~$4,000 (April–May 2026, −88%)**, with almost no `Loss` tags attached to either collapse. Most tellingly, he went **completely silent for four months (Feb–May 2025)** while $ONDS fell from $2.80 to $0.60 — then resurfaced loudly once the position turned. As of September 2026 he is also a **paid, ref-linked (`?ref=HGR`) affiliate promoter of TraderMatrix / TD Pro itself**, which means any praise of this platform's own tools in his recent posts is commercial speech, not independent validation, and must be excluded from any "organic testimonial" signal Artemis might otherwise harvest.

---

## 1. Executive Profile

### Philosophy
@Drone_Daddy is a **single-ecosystem catalyst-DD trader whose entire identity (handle, content brand, and portfolio) is built around one thesis: U.S. onshoring of drone/counter-UAS/defense-optics supply chains, expressed almost entirely through $ONDS (Ondas Holdings) and two names he treats as its extended supply chain — $UMAC (Unusual Machines) and $LPTH (LightPath Technologies)**. Unlike a generalist momentum poster, he presents as a **fundamentals-first micro-cap analyst**: 48.9% of his posts are self-tagged `Dd` (due diligence) — by far the highest DD-tag share of any comparable dossier subject in this batch — and his DD posts run longer (568 characters avg.) than his other content (421 avg.), tracing defense-policy catalysts, dilution history, contract announcements, and 13F/institutional price-target moves in granular, source-cited detail.

But the DD-analyst persona sits on top of a second, more consequential identity that emerged over the sample: **a monetized research/content operation.** In November 2025 he launched **"Hidden Gems Research LLC,"** a Substack with free and paid tiers, an "8-chapter options guide," a transparent public "$10,000 Gem Vault" challenge port, giveaway contests, and — by mid-2026 — a live-stream schedule and an **explicit paid affiliate relationship with TraderMatrix/TD Pro** (referral links tagged `?ref=HGR` appear in at least 6 posts from May–September 2026, alongside phrases like "Made about 40x the monthly fee this week"). His stated goal, posted at age "under 30," is **"7 figures in 2 years."**

The core trading behavior underneath both personas is textbook **concentrated conviction-holding with periodic silence during pain**: he DCAs into $ONDS through a falling knife ($2.80 → $0.60 over H1 2025) while off-platform, resurfaces once it turns, rides it via LEAPS/short-dated calls to spectacular paper gains, refuses to systematically de-risk, and eventually gives back the bulk of the gain in a single-digit-week collapse — twice, on the same instrument, in the same 14-month window.

### Post Cadence
| Metric | Value |
|---|---|
| Total posts | 988 |
| Full date range | 2024-12-17 → 2026-09-10 (631 days / 90.1 weeks) |
| **Raw average cadence** | **10.96 posts/week** across the full span — but this average is misleading (see below) |
| **Silent period** | **2025-02-01 → 2025-06-01: zero posts, 4 straight months**, spanning exactly the window $ONDS fell from ~$2.80 to ~$0.60 |
| **Active-era cadence** (2025-08-01 onward, post-silence, post-ramp) | **16.9 posts/week** — this is his real, sustained content-creator cadence |
| Busiest single month | 2026-01 (145 posts) — coincides with the Hidden Gems Research LLC launch aftermath and a second capital run-up |
| Peak posting hours (UTC) | 13:00–23:00 (roughly 8am–6pm ET, U.S. market hours through evening recap/livestream slot) |
| Days silent as of report date | 0 — posted same-day, 2026-09-10 ("Thanks for 5000 Followers!") |

The 2024-12 → 2025-01 stretch (15 posts) reads as an early, exploratory phase. The four-month silence that follows is the single most diagnostic cadence fact in this dossier: **his posting frequency is not correlated with market activity, it is anti-correlated with his own drawdown.** He posts prolifically while winning or flat, and goes dark while bleeding.

### Verified Capital Trajectory (platform-tracked `amount_k`)
*Methodological note — read before using this series for backtesting:* Cross-referencing his own prose against the `amount_k` field shows it tracks **a specific small leveraged options account he variously calls his "Challenge Port," "LEAPS Challenge Port," or "RH [Robinhood] Challenge Port" — NOT his full net worth.** He explicitly, repeatedly separates this from a much larger claimed **self-directed 401(k)** ("3Xed my self directed 401(k)... Officially 3Xed... Goal is 7 figures in 2 years," 2025-09-23; "$43,000~ to new ATHs above $150,000... in one of my Self directed 401(k)s," 2026-01-03) and from a separate **"Gem Vault"** community-facing $10,000 demonstration port launched with Hidden Gems Research in Dec 2025–Jan 2026. **None of those larger, unverified account claims appear anywhere in `amount_k`.** Any consumer of this data must not conflate the tracked series below with his "real" trading results — it is one leveraged sleeve, and it is the sleeve he shows the most raw, least curated numbers for.

| Date | Event | Tracked value (`amount_k`) | Note |
|---|---|---|---|
| 2024-12-18 | First tracked value | $13,712 | Starting baseline (Challenge Port inception, pre-naming) |
| 2025-01 → 2025-06 | Silent period bridges a decline | $15.7k (Jan) → $10.3k (Jun 2, "Almost back at my average purchase price for ONDS!") | Confirms he was underwater and DCA'ing through the $2.80→$0.60 ONDS collapse while off-platform |
| 2025-07 | Return to posting, $ONDS "on an absolute tear" | $16.6k → $19.6k | Options plan posts begin; covered calls sold "underwater" from being called away too early |
| **2025-08-10** | **"How life feels when you bought into $ONDS at $.60"** | **$77,291 — lifetime tracked peak** | Tagged `Funny`, not `Gain` — a euphoria post at the exact top |
| 2025-09-19 | "Options Challenge Port 1 Month Review (+177%)" | ~$24.3k (adjacent posts) | Self-reported best month ever; rolling gains into $ACHR/$RKLB/$TTD |
| 2025-09-23 | "+300% since March 2025 (6 months)" | $22.4k | This figure refers to the **separate 401(k)**, not the tracked port — a good example of the conflation risk above |
| **2025-09-25, 04:34** | Trough begins | $3,003 | Two days after a $22.4k print — an intraday/48-hour collapse |
| **2025-09-25, 14:03** | **"2 Candles"** (`Funny` tag) — **lifetime tracked trough** | **$2,848 — a −96.3% drawdown from the Aug-10 peak, in 46 days** | Captioned "Player 2 joined the party $ONDS @TRON" — a joking acknowledgment that a pod-mate (@TRON, a separate dossier subject, #3 most-active) suffered a correlated $ONDS-driven loss around the same window |
| 2025-10 → 2025-12 | Rebuild via LEAPS, $UMAC/$LPTH basket | $2.8k → $34.7k | No stop discipline visible; rebuild driven by re-adding to the same three-name basket |
| **2026-01-03** | "PSA: DO NOT PAY FOR A DISCORD..." | $34,729 | Second local peak on the tracked port (see §4 for the irony of this post's timing) |
| 2026-02-02 | **"$ONDS Loss Porn Conviction"** (`Loss` tag) | $10,811 | Explicitly plans a further add: *"Last average down will occur at $9."* Projects the position to be worth $350–400k by end of 2026. |
| 2026-03 → 2026-05 | Continued bleed despite the above plan | $10.8k → $4.0k (April low) | Confirms the "Loss Porn" post did not mark a bottom in discipline or price |
| **2026-09-10** | Report date (current) | **$12,059** | Stabilized in the $10–14k band since July 2026 |

**Net lifetime trajectory on the tracked vehicle: $13,712 → $12,059 over 631 days (−12.1%)** — despite passing through **two independent round-trips exceeding 25x peak-to-trough compression** ($13.7k → $77.3k → $2.8k, then $2.8k → $34.7k → ~$4.0k). The tracked account is, net, **flat-to-slightly-down after 21 months of aggressive options leverage on a single ecosystem**, even as he publicly claims outsized separate-account gains that this data cannot verify. **This is the single most important number in the dossier: the leveraged, single-ticker sleeve he shows his work on has not compounded — it has round-tripped twice and given nearly all of it back both times.**

---

## 2. Ticker Universe & Catalysts

### Core universe (by raw `$TICKER` mention count; 96 unique tickers, 1,313 total mentions)
| Ticker | Mentions | Role |
|---|---|---|
| **$ONDS** (Ondas Holdings) | 502 (38.2% of all ticker mentions) | **The entire thesis.** Drone/CUAS/defense-telemetry small-cap; held from ~$2.80 in 2024 down to $0.60 and back; the subject of both tracked-account blow-ups. |
| **$UMAC** (Unusual Machines) | 164 | Drone-components maker; explicitly linked to $ONDS via a joint strategic investment in $LPTH; entered his universe July 2025, became a second leg of the same thesis |
| **$LPTH** (LightPath Technologies) | 142 | Infrared-optics maker; entered via an $8M joint $ONDS/$UMAC strategic investment (Sep 2025) for "black diamond" germanium-free lens tech — a genuine, sourced supply-chain angle, not a random add |
| $AMPX (Amprius Technologies) | 50 | Battery tech, drone/defense-adjacent power-density thesis |
| $ACHR (Archer Aviation) | 33 | eVTOL — cross-pod name shared with @TRON/@YungEmber |
| $SRFM (Surf Air Mobility) | 33 | Regional/electric aviation, entered Dec 2025 as a shares-only (no options chain) position |
| $RCAT (Red Cat Holdings) | 28 | Earlier-era drone name, largely superseded by $ONDS after 2024 |
| $PLTR | 13 | Cited as a benefactor of the same defense-AI theme, not a core holding |
| $LMT, $RR, $KOPN, $SIDU, $DPRO, $ONDL, $PUSA, $UAVS | 5–18 each | Long tail of the drone/defense/CUAS micro-cap basket, largely thematic overflow from the $ONDS thesis |
| $SPY, $NVDA, $TSLA, $HOOD, $LULU, $CVNA, $HIMS, $OKLO, $COIN | scattered, 5–10 each, concentrated 2026 | Post-2026 diversification into mega-cap/momentum swing plays, coinciding with his adoption of TD Pro/TraderMatrix order-flow tooling |

**Concentration is extreme even by micro-cap-trader standards:** $ONDS + $UMAC + $LPTH together account for **62.5% of every ticker mention in 988 posts.** This is not diversified thematic momentum (contrast @TRON's broader drone/eVTOL/AI/SPAC basket) — it is **one supply chain, tracked with real depth, at concentration levels that make the account's fate almost entirely a bet on one company's execution.**

### Options vs. equities
- **379 of 988 posts (38.4%)** contain explicit options language (calls, puts, LEAPS, strikes, CSPs, covered calls, rolls, ITM/OTM).
- Self-identifies as **LEAPS-first** ("leveraging the power of LEAPS over shares giving me more control with less capital") with an occasional, self-labeled `Yolo` short-dated gamble (11 posts total — $PEW earnings lottos, a $SOFI pre-earnings play, a $CVNA earnings play).
- Does show **some real profit-realization mechanics** absent from purely bag-holding peers: sells covered calls against core LEAPS positions, takes "partial profit... +104%," closes runners at "+214%," and uses a self-described "wave strategy" (selling into strength, buying red days) — a genuinely more mechanical, less purely-diamond-hands approach than the median subject in this batch. The mechanism exists; it simply hasn't been sized or applied early enough to prevent either collapse.
- **2026 shift:** starting May 2026, adopts **TD Pro/TraderMatrix order-flow and "Apex Levels" (gamma/dealer-positioning) signals** as an explicit input ("Screenshot is from TD Pro which I've been massively leveraging for options plays"), and begins trading mega-cap swing names ($TSLA, $OKLO, $COIN, $AVGO, $NET) alongside the drone basket for the first time — a real, dated tool-adoption and universe-broadening event.

### What drives entries — ranked by frequency
1. **Defense/onshoring policy catalysts** — Secretary of Defense "red tape" removal for domestic drone production, NDAA-compliance/China-parts-ban news, congressional defense-spending signals, FAA waivers. This is his single deepest and most genuinely differentiated research lane.
2. **Supply-chain/partnership mapping** — actively traces who supplies whom ($LPTH's germanium-free optics feeding $ONDS/$UMAC), frames new tickers as extensions of an existing thesis rather than fresh ideas.
3. **Dilution-ladder technicals** — a distinctive, quantifiable framework unique to this account: tracks $ONDS's historical dilution print levels ($1.25, $3, $5, projecting $7, then $9) and uses them as forward technical levels — a real, falsifiable, semi-repeatable micro-cap-specific edge.
4. **Institutional/analyst price-target moves** — treats new sell-side PT raises as confirmation ("institutions are understanding — they've loaded their yacht. Retail will soon catch on").
5. **Unusual options volume / "someone knows something"** — a recurring, conspiracy-adjacent framing where elevated call volume in $UMAC/$ONDS is read as insider foreknowledge of an imminent catalyst. Sometimes right (news follows within days), sometimes just narrative-fitting after the fact — cannot be distinguished from confirmation bias without independent verification.
6. **Cross-pod amplification** — explicitly credits/echoes @TRON and @YungEmber calls ("This play was signaled yesterday, if you're not following @TRON and I you should be"), confirming a **coordinated small pod of AfterHour drone-thesis promoters**, not an independent signal source.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags?
**Both — inconsistently, and the inconsistency is the risk.** He is genuinely more mechanically active than a pure bagholder: he sells covered calls, banks partial profits on runners, and has articulated a "wave strategy" (buy red days, sell into strength). But on the position that matters most — his core $ONDS LEAPS stack — the record shows the same pattern as every other dossier in this batch: **rolling and adding, not trimming, as size grows past any stated risk limit**, followed by a collapse he narrates with humor rather than a stop.

- **Pre-committed averaging-down levels, stated in his own words:** *"Last average down will occur at $9"* (2026-02-02, "$ONDS Loss Porn Conviction," posted the same day he tags a post `Loss` for one of only four times in 988 posts). This is not a stop-loss plan — it is an **add-more-if-it-drops plan**, explicitly bounded but still a plan to increase exposure into weakness.
- **Rationalization via "house money":** *"I'm also playing with a lot of house money from last years success and don't need this money for years so keep that in mind"* — the exact cognitive move that permits oversized risk-taking after a prior win.
- **Rolling instead of trimming, at a local top:** *"$ONDS has been on an absolute tear... sent my sold covered calls underwater. I've decided not to roll my calls..."* (2025-07-17) — a rare instance of him actually choosing NOT to roll, but the account's subsequent August peak/September collapse shows this discipline was not durable across the position as a whole.

### Documented wins vs. blow-ups
- **Documented wins:** Real, frequent, and specific — 117 `Gain`-tagged posts, several independently plausible against the `amount_k` series (the Aug-2025 run to $77k; "+177%" one-month Challenge Port review; individual option closes at "+214%," "+104%," "+268%" on $TSLA). His **catalyst-timing on $LPTH specifically is genuinely impressive**: he called a swing play on earnings the day before a confirmed +30%+ EPS-driven pop, then flagged $UMAC unusual call volume the day before a +40% single-day move on a domestic-drone-ban headline.
- **Documented blow-ups:** Only **4 of 988 posts (0.4%) are tagged `Loss`**, and none of them is tagged on the actual dates of either major collapse (2025-09-25 is tagged `Funny`; 2026-02-02's `Loss` tag applies to an ongoing bleed, not the sharpest drop). **The −96.3% Aug-to-Sep-2025 collapse and the ~−88% Jan-to-May-2026 second collapse together represent the account's two largest events by dollar magnitude and carry almost no `Loss` tags between them.** Any signal-performance backtest using his self-applied tags as ground truth will systematically overstate his real win rate.

### How does he manage losing positions?
The pattern, repeated across both collapses: **(1) concentrate further into the thesis as it runs (adding $UMAC and $LPTH as "extensions" of the $ONDS bet rather than diversification away from it); (2) go silent when the position is underwater for an extended period** (the 4-month 2025 silence is the clearest example, but shorter silences recur around both drawdowns); **(3) resurface with humor, not urgency, once price stabilizes or turns** ("2 Candles," "Player 2 joined the party"); **(4) pre-announce a further add level rather than a stop** ("Last average down will occur at $9"). He does **not** show the "diamond hands"/never-flinch rhetoric of some peers — his prose is calmer and more self-aware than most — but the underlying behavior (concentration, silence-during-pain, add-not-cut) produces the same outcome.

---

## 4. Behavioral & Sentiment Signals

### Why is he posting?
The tag distribution and the account's own trajectory make the answer explicit: **he is building a research/media business, and the trading account is both the product demo and the marketing asset.**

| Tag | Count | Share |
|---|---|---|
| `Dd` (due diligence) | 483 | 48.9% |
| `News` | 129 | 13.1% |
| `Gain` | 117 | 11.8% |
| `Discuss` | 104 | 10.5% |
| `Funny` | 82 | 8.3% |
| (untagged) | 25 | 2.5% |
| `Chart` | 18 | 1.8% |
| `Yolo` | 11 | 1.1% |
| `Contest` | 11 | 1.1% |
| `Loss` | 4 | 0.4% |
| `Poll` | 4 | 0.4% |

**48.9% `Dd` is the highest due-diligence self-tag rate observed in this dossier batch by a wide margin** (compare @TRON's 0.9%). This is a real, distinguishing feature of the account — he genuinely does write sourced, catalyst-cited research, not just reaction and memes. But the DD output funnels directly into monetization: **Nov 2025 — "Hidden Gems Research LLC IS NOW LIVE"** (Substack, free/premium tiers, an "8 Chapter... guide," a public "$10,000 Gem Vault" demonstration port); **contest/giveaway cadence** (11 `Contest`-tagged posts, mostly Nov 2025 launch-window promotions); **by mid-2026, an active livestream schedule and a paid affiliate partnership with TraderMatrix/TD Pro** (`?ref=HGR` links, "Made about 40x the monthly fee this week," "over 400 members in the discord now").

### A documented self-contradiction worth flagging explicitly
On **2026-01-03**, with his own tracked account near a local peak ($34,729), he posted: *"PSA: DO NOT PAY FOR A DISCORD OR SERVICE FROM SOMEONE ON HERE UNLESS THEY SHOW PROOF OF PROFITABILITY... I could count the amount of paid services/discords I could vouch for based on profitable data on 1 hand — including my own."* This was posted **six weeks after he launched his own paid Hidden Gems Research service**, and **one month before his own tracked account began the second ~88% bleed** described above. The PSA is not necessarily insincere — but it is a useful marker: **his own confidence in his paid-service track record is not a leading indicator of his account's forward performance.**

### Recurring linguistic patterns
- **💎 (diamond) emoji density** — appears in a majority of posts, used both for conviction ("💎👏") and, distinctively, as his own brand mark (nearly every Hidden Gems Research / Gem Vault post).
- **"Someone knows something"** — his signature phrase for reading elevated options volume as insider foreknowledge; recurs across the $ONDS/$UMAC complex whenever unusual volume appears.
- **Dismissiveness toward short-term traders** — repeatedly frames swing traders "trying to flip the stock" as lacking conviction/understanding, positions himself as the patient "long term investor," even while running short-dated `Yolo` plays himself.
- **"We ride the wave" / "wave strategy"** — his self-branded buy-red-sell-green framework, referenced as both a trading method and a teaching product.
- **Calm, dry humor on red days** — "2 Candles," "Everybody panic! Just kidding," "Player 2 joined the party" — he does not panic-post or go silent-through-anger; he jokes, briefly acknowledges, and moves the narrative forward toward the next catalyst.

### Engagement arc — a real leading indicator
| Period | Avg. reactions/post | Avg. comments/post | Context |
|---|---|---|---|
| 2024-Q4 – 2025-Q2 | 1.2 – 5.0 | 0.0 – 1.0 | Pre-monetization, low-visibility phase |
| 2025-Q3 | 12.1 | 6.3 | Coincides with the $77k peak AND the −96.3% collapse — both happen inside this quarter |
| 2025-Q4 | 22.5 | 14.6 | Hidden Gems Research LLC launches (Nov 2025); engagement climbs through the account's second worst stretch |
| **2026-Q1** | **27.8 (lifetime peak)** | **14.2** | Coincides with the second local peak (Jan 3, $34.7k) *and* the subsequent "Loss Porn" post and renewed bleed |
| 2026-Q2 – Q3 | 17.9 – 23.9 | 6.2 – 10.1 | Moderating as the account stabilizes in the $10–14k band |

**His audience grew fastest during and immediately after his two largest drawdowns, not during clean uptrends.** This confirms the same pattern seen in this batch's other subjects: engagement tracks content/narrative intensity and monetization launches, not risk-adjusted performance — and should never be read by Artemis as a performance-quality signal.

---

## 5. Quantitative Verdict for TraderMatrix

### Primary and Secondary Algorithmic Classification Tags
- **Primary: `THEMATIC_SUPPLY_CHAIN_DD_CONCENTRATOR`** — genuinely deep, sourced, catalyst-driven research within one supply chain (drone/CUAS/defense-optics, anchored on $ONDS), with a real, quantifiable proprietary framework (the dilution-ladder levels) worth independent verification and watchlisting.
- **Secondary: `LEVERAGED_SINGLE-NAME_ROUND-TRIPPER`** — runs LEAPS/options leverage on a single 3-ticker ecosystem through repeated ~90%+ boom-bust cycles on the tracked account; shows partial profit-taking mechanics but not enough, early enough, to prevent either collapse.
- **Tertiary: `AFFILIATE_MONETIZER`** — operates a paid research business (Hidden Gems Research LLC) and, as of 2026, a paid TraderMatrix/TD Pro referral partnership (`?ref=HGR`). **Any of his commentary that promotes a paid product or service — including this platform's own — must be flagged and excluded from "organic user validation" signal; it is marketing, not testimony.**

### Algorithmic Alpha Score & Expectancy
**Alpha Score: 41 / 100**

Rationale: **Real, differentiated selection/catalyst alpha exists** in a narrow lane — his supply-chain mapping ($ONDS→$UMAC→$LPTH), defense-policy catalyst tracking, and dilution-ladder technical framework have produced genuinely correct, ahead-of-price calls ($LPTH earnings swing, $UMAC unusual-volume-to-+40%-move). But that alpha is **concentrated in a single ecosystem to a degree that makes account-level outcomes almost entirely dependent on one company's stock path**, has **twice produced a ~90%+ drawdown on the tracked leveraged sleeve within a 14-month window**, and his output is **increasingly commercially motivated** (paid research service, paid platform affiliate). The score sits below @TRON's comparable 46 because @Drone_Daddy's concentration is narrower (one ecosystem vs. a broader thematic basket) and his monetization/affiliate incentive is more advanced and more directly relevant to TraderMatrix's own product credibility.

**Expectancy characterization:** **Positive idea-generation expectancy within the drone/CUAS/defense-optics niche specifically; deeply negative account-level expectancy when followed at his own concentration and leverage.** His individual catalyst calls, taken independently and exited on discipline, likely carry real edge. His tracked account, followed at his own sizing, has round-tripped twice to near-total loss of gains. **Artemis should harvest the ticker/catalyst discovery and discard the position-sizing entirely.**

### Signal Flow Ingestion Matrix

| Signal Type | Example Trigger | Artemis Action | Confidence |
|---|---|---|---|
| New supply-chain-linked ticker in the $ONDS ecosystem (`Dd`-tagged, sourced to a named contract/partnership) | "$ONDS and $UMAC Strategic investment in $LPTH" | **Ingest → watchlist**, independently verify the contract/filing before sizing | Medium-High |
| Dilution-ladder level call ("next logical dilution level is $X") | The $1.25/$3/$5/$7/$9 $ONDS ladder | **Track as a technical reference level**, not an entry/exit trigger on its own — cross-check against actual filed S-1/S-3 activity | Medium |
| "Someone knows something" / unusual-options-volume framing | Pre-catalyst $UMAC/$ONDS volume spikes | **Watch, don't trade** — flag the ticker for independent flow verification (e.g. via TD Pro's own unusual-activity tool); his framing alone is unfalsifiable | Medium |
| Euphoric peak-tagged-as-`Funny` post at a local account high | "How life feels when you bought into $ONDS at $.60" (posted at the tracked-account's lifetime peak) | **Contrarian fade candidate** — treat celebratory/meme framing at a stated high-water mark as a crowding signal in that specific name | Medium-High |
| Extended silence (14+ days) after a prior high-engagement bullish run | The Feb–Jun 2025 4-month silence, bridging a 2.80→0.60 collapse | **Do not read silence as "no position" or "all clear."** Treat prolonged silence following a loud conviction call as a probable undisclosed drawdown in that name | High |
| Pre-announced "next average-down level" | "Last average down will occur at $9" | **Do not mirror the add.** Log as a toxic-averaging-down disclosure; if following the underlying thesis, size and stop independently | High |
| Any post carrying a `?ref=` affiliate link or naming a paid service/discord/Substack tier | TraderMatrix/TD Pro `?ref=HGR` links, Hidden Gems Research promos | **Exclude from signal entirely.** Commercial content, zero independent trade information; do not count as customer validation for internal product metrics either | High |
| `Gain`/`Loss` self-tags | 117:4 ratio | **Discard as ground truth for backtesting.** Reconcile against the `amount_k` series instead, with the account-identity caveat in §1 applied first | High |

### Specific Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Treat @Drone_Daddy as a **specialist screener for the drone/CUAS/defense-optics/onshoring supply chain** — his first mention of a new name tied to $ONDS/$UMAC/$LPTH by contract, filing, or partnership is worth an independent watchlist add.
2. His **defense-policy catalyst tracking** (Sec Def actions, NDAA/China-parts restrictions, FAA rule changes) is a genuine, sourced macro-thematic input — cross-reference against `theme-detector` and `sector-analyst` rather than trading standalone.
3. His **dilution-ladder framework** is a real, falsifiable, ticker-specific technical model worth encoding and back-testing independently on $ONDS and comparable serial-diluting micro-caps.

**Contrarian Fade Directives (when to fade him / the retail herd around him):**
1. **Fade euphoric/meme-tagged posts at or near a stated local account high** — his own "How life feels when you bought $ONDS at $.60" post landed on the exact day of the tracked account's lifetime peak, 46 days before a −96.3% collapse.
2. **Fade any post that pre-announces a further average-down level** ("Last average down will occur at $9") — this is a plan to add into weakness, not a risk-managed conviction signal.
3. **Fade retail herd enthusiasm cross-amplified across his pod** (@TRON, @YungEmber, @Drone_Daddy simultaneously promoting the same $ONDS/$UMAC names) — correlated conviction across multiple high-follower accounts on the same instrument is a crowding signal, not independent confirmation.

**Mandatory Risk Blacklists & Firewalls:**
1. **Never size a mirrored position to his stated conviction or LEAPS-concentration levels in $ONDS, $UMAC, or $LPTH** — this basket alone produced two ~90%+ drawdowns on his own tracked account in 14 months.
2. **Treat his `Gain`/`Loss` self-tags as unreliable for backtesting or performance-attribution models** — 117:4 is not a real win/loss ratio; reconcile against `amount_k` with the account-identity caveat applied.
3. **Exclude any content carrying a `?ref=` link, a paid-service/Substack/Discord mention, or a livestream promotion from signal ingestion.** This applies with particular force to any post praising TraderMatrix/TD Pro itself post-2026-05 — it is paid affiliate content, not neutral product feedback, and must not be cited internally as organic customer validation.
4. **Toxic pattern flag: prolonged silence following a loud, high-conviction thematic call.** His 4-month 2025 silence bridged the exact window his flagship position fell ~79% — silence should be treated as a probable undisclosed-drawdown signal, not an absence of position.
5. **The `amount_k` series must be used only as the "Challenge Port" sleeve it is** — never conflate it with his separately claimed (and unverifiable in this data) self-directed 401(k) or "Gem Vault" community-port figures.

**Exit Rules & Alpha Rectification:**
1. **Impose an external, staged profit-take rule on any idea sourced from him** (e.g., trim 25% at +50%, another 25% at +100%) — he demonstrates the mechanism (covered calls, partial closes) inconsistently and not early enough on his largest positions.
2. **Impose a hard stop (e.g., −25% from entry) on any mirrored $ONDS/$UMAC/$LPTH position**, independent of his own plan — his documented pattern is to plan further adds, not exits, as a position deteriorates.
3. **Treat "someone knows something" / unusual-volume posts as a watch-list trigger only**, requiring independent flow confirmation (e.g., via TD Pro's own unusual-activity or dealer-positioning tools) before any action.
4. **Re-run this dossier's affiliate-content filter (§Ingestion/Firewall #3) on a rolling basis** — his commercial relationship with TraderMatrix is new (2026) and likely to deepen; content classification rules should be revisited as his monetization model evolves.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone |
|---|---|
| 2024-12-17 | **First post** ($MU earnings/rate-cut combo); tracked account baseline established |
| 2024-12-18 | First self-reflective loss post: "the importance of taking wins" — a -40% short-DTE-calls reversal, and an early (unheeded) stop-loss resolution |
| 2024-12-25 – 2025-01 | $RCAT/$ONDS/$ONDS-adjacent drone thesis forms; $ONDS enters as a "next $RCAT" thesis with a $10 price target |
| **2025-02-01 → 2025-06-01** | **123-day total silence** — bridges $ONDS's fall from ~$2.80 to ~$0.60; DCA'd through it off-platform |
| 2025-06-02 | Returns to posting: "Almost back at my average purchase price for ONDS!" — DCA thesis beginning to validate |
| 2025-07 | Content ramp resumes; covered calls sold "underwater" as $ONDS runs; decides not to roll them |
| 2025-07-11 | "Red tape is gone for $ONDS and other drone stocks" — Sec Def policy catalyst call; $UMAC enters universe same day, credited jointly to @TRON |
| 2025-09-15 | $LPTH enters universe via a sourced $8M $ONDS/$UMAC strategic-investment announcement — the supply-chain-mapping edge in its purest form |
| **2025-08-10** | **Tracked-account lifetime peak, $77,291** ("How life feels when you bought $ONDS at $.60," tagged `Funny`) |
| 2025-09-19 | "Options Challenge Port 1 Month Review (+177%)" — best-ever monthly return self-reported |
| 2025-09-23 | "+300% since March 2025" — a *separate* 401(k) claim, not reflected in `amount_k` |
| **2025-09-25** | **Collapse: tracked account falls to $2,848, a −96.3% drawdown from the Aug-10 peak in 46 days** ("2 Candles," referencing a correlated @TRON loss) |
| 2025-09-29 | Resumes aggressive DD posting on $LPTH/$UMAC within days of the trough — no visible reduction in conviction or sizing |
| 2025-11-21 | **"Hidden Gems Research LLC IS NOW LIVE"** — monetization pivot: Substack, premium tiers, 8-chapter guide |
| 2025-12-09 | "$ONDS Returns YTD: +$116,341.43" — a large, separate real-money claim, unverifiable against `amount_k` |
| 2026-01-03 | **"PSA: DO NOT PAY FOR A DISCORD OR SERVICE... UNLESS THEY SHOW PROOF"** — posted at a second local tracked-account peak ($34,729), six weeks after launching his own paid service |
| **2026-02-02** | **"$ONDS Loss Porn Conviction"** — one of only 4 lifetime `Loss` tags; pre-commits to a further average-down at $9 and a $350–400k year-end price target |
| 2026-03 → 2026-05 | Tracked account continues bleeding to a **~$4,000 low** despite the Feb plan — second ~88% drawdown confirmed |
| 2026-05-06 → 2026-06 | Adopts TD Pro/TraderMatrix order-flow tooling; begins swing-trading mega-caps ($TSLA, $OKLO, $COIN) for the first time; first `?ref=HGR` affiliate links appear |
| 2026-07-08 | Promotes TraderMatrix's newly-released "Apex Levels" dealer-positioning tool by name during a Labor Day sale push — explicit paid-affiliate content |
| 2026-09-10 | Report date — active same-day ("Thanks for 5000 Followers!"), tracked account stabilized at $12,059 |

---

*End of dossier. Prepared for the Artemis Engine signal-ingestion pipeline. Before any downstream backtest uses this subject's content: (1) exclude all `?ref=` / paid-service-promoting posts, (2) reconcile the `amount_k` "Challenge Port" series against the account-identity caveat in §1 rather than his prose claims of separate-account gains, and (3) discard self-applied `Gain`/`Loss` tags as ground truth.*
