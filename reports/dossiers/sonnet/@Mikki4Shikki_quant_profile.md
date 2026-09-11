# QUANT PROFILE DOSSIER: @Mikki4Shikki

**Classification:** Forensic Trader Autopsy — Artemis Signal Ingestion Program
**Subject Rank:** #36 Most-Active Followed Trader (AfterHour)
**Sample:** 85 lifetime posts, 2025-01-27 → 2026-09-03 (584 days / ~83.4 weeks)
**Sources:** `@Mikki4Shikki_lifetime.md` (posts/reports), `@Mikki4Shikki_all_posts.json` (raw, incl. Kinfo-linked `amount_k` verified portfolio snapshots)
**Analyst:** Sonnet — Artemis Engine
**Date Compiled:** 2026-09-10

---

## 0. TL;DR Verdict Box

| Field | Value |
|---|---|
| Primary Tag | `NARRATIVE_BAGHOLDER_NO_STOPS` |
| Secondary Tag | `SOCIAL_AMPLIFIER_LOW_ORIGINATION` |
| Tertiary Tag | `RETAIL_SENTIMENT_BAROMETER` (contrarian utility only) |
| Alpha Score | **18 / 100** |
| Expectancy | **Negative and documented** — verified capital -57.4% lifetime (peak-to-trough -64.8%), with zero occurrences of "trim," "stop loss," or "took profit" across 85 posts |
| Verified Capital (start → peak → trough → current) | $107.9K → $118.8K → $41.8K → $45.96K |
| Max Drawdown | **-64.8%** (Feb 19 '25 peak → Jul 16 '26 trough, ~17 months, no single event — a slow bleed) |
| Edge Type | Minimal/negative — she is a discovery *node*, not a signal source; her rare original DD (`$CVU`) is competent, everything else is reactive or copied |
| Fatal Flaw | Zero exit discipline + averages down into concentrated losers (`$MTPLF` 895→1,600 shares while the position is collapsing 76.5%) + disappears from portfolio verification during the worst drawdowns |
| Recommended Posture | **Do not ingest her calls directly. Fade her anthropomorphizing/"why do you hate me" posts as local-top tells. Use her as a routing pointer to the traders she amplifies (`@Freeballer`, `@LANDO`, `@ThetaTard`), not as a source herself.** |

---

## 1. Executive Profile

### Philosophy (stated vs. revealed)
She posted one piece of stated philosophy in 85 posts (2026-02-05): *"I don't chase narratives. I learn structure. If the market feels rigged, it's because you're trading blind... no hype, no fear, just the hard facts Wall Street doesn't explain."* This reads as generic trading-guru copy (0 comments engaging with any actual "structure," 28 reactions on a post with no body text) rather than a genuine methodology statement — and it is **directly contradicted by every other post in the archive**. The revealed philosophy across the full sample is: buy small/micro-cap story stocks and meme names on hype or a friend's tip, anthropomorphize the position emotionally through every swing, ask the crowd what to do when it moves against her, and hold through the collapse without a plan. This is a **narrative-chasing, crowd-dependent retail account wearing a "disciplined structure" slogan**, not living it.

### Post Cadence
- **85 posts / 584 days ≈ 1.02 posts/week** lifetime average — among the lowest-frequency accounts in the followed-trader set, and heavily front-loaded.
- 25 of 85 posts (29%) land in the first 13 weeks (Jan-Mar 2025) — an enthusiastic launch phase.
- Cadence decays hard afterward: 2/month in Aug-Sep 2025, a **3-month total silence Mar-May 2026**, and a second silence in Aug 2026 (0 posts) before a single closing post on Sep 3, 2026. December 2025 is the one late-life spike (9 posts) — driven almost entirely by a Robinhood referral-giveaway thread, not trading activity (see §4).
- This is a disengagement curve, not a steady-cadence trader: enthusiasm → emotional attrition → near-silence, tracking the capital trajectory in §1 below almost exactly.

### Verified Capital Trajectory (Kinfo-linked `amount_k`, in $K)
```
$120K |  .*  (118.8 peak, Feb 19 '25)
$110K | *  *
$100K |*     * .        *  (97.7, Aug 19 '25 — last clean read before blackout)
 $90K |        *  * *  *
 $80K |          *        *              [ PORT DISCONNECTED, Sep-Dec '25 ]
 $70K |                                              *  (71.3, Jan '26 reconnect)
 $60K |                                                 *  *
 $50K |                                                        * (54.4)      *  (46.0, current — Sep '26)
 $40K |                                                            * * *  *  (41.8, Jul 16 '26 — lifetime low)
      +-----------------------------------------------------------------------------------
       Jan'25   Mar'25   May'25   Jul'25   [blackout]  Jan'26   Mar'26 [gap]  Jun'26  Sep'26
```
- **Lifetime**: **-57.4%** net (107.9K → 45.96K) over 19 months.
- **Peak-to-trough (clean readings only)**: -64.8% (118.83K, Feb 19 '25 → 41.82K, Jul 16 '26).
- **The "verified capital blackout" pattern**: from Aug 19, 2025 through Dec 31, 2025 (~4.5 months), every `amount_k` reading is 0.0, near-zero (0.08, 1.03, 1.35, 2.74), or `null` — a broken Kinfo portfolio link, confirmed in her own words across three separate posts: *"Since my port is still not connecting correctly, here are screenshots"* (Jul 21 '25), *"Are we still working on the port connection issues?"* (Sep 5 '25), *"If my port would actually connect, you'd see the damage"* (Oct 10 '25). She reconnects Jan 1, 2026 (*"Whoa! Port is connected!"*) at **$61.78K–63.62K — 36.8% below the last clean pre-blackout reading of $97.68K.** The blackout is not random: it spans exactly the period she was still holding a collapsing `$MTPLF` position (which she confirms cost her ~$12,000 realized, see §3) and coincides with zero self-tagged `[Loss]` posts during the entire stretch — the worst of the damage happened while the account was unverifiable and undisclosed.
- A second, shorter mixed-reliability stretch appears Jan 22–Feb 5, 2026 (several 0.0 readings interleaved with valid $59-71K reads) — likely ordinary sync noise rather than a deliberate pattern, but it reinforces that this trader's linked-portfolio data is only ~65% reliable across the sample and every reading should be sanity-checked against adjacent posts before being trusted as a milestone.

---

## 2. Ticker Universe & Catalysts

### Concentration
| Ticker | Mentions (posts) | Role |
|---|---|---|
| `$ONDS` / `$ONDL` (Ondas Holdings + leveraged product) | 11 (#32,52,60,62,64,70,73,75,77,81,83,84) | Core Era-2 conviction position (late 2025→2026); holds **both** the common and the leveraged product simultaneously ("LFG Loooong") |
| `$MTPLF` (Metaplanet, BTC-treasury proxy) | 8 (#29,30,33,35,36,41,53,69) | Core Era-1 conviction position; averaged **up** in size (895→1,600 shares) into a documented -76.5% / -$12,000 loss |
| `$ICCT` | 3 (#22,31,44) | Small-float speculative flier; one quick YOLO win (+$1,092 on 575 shares), then a second entry held for 3+ months hoping for "a faint heartbeat" before capitulating ("I just want OUT") |
| `$NVDA` | 5 (#1,4,5,12,52) | Anthropomorphized "love/hate" mega-cap holding, early-2025 focus |
| `$HOOD` | 6 (#56-59,61,65) | Not a trade — a multi-post referral/gamified-giveaway thread (see §4) |
| `$HIMS`, `$ACHR`, `$RGTI`, `$DGLY`, `$PLTR`, `$POET`, `$OPEN`, `$FIG`, `$BYND`, `$AVGO`, `$SMCI`, `$CVU`, `$BTC` | 1-2 each | Long tail of momentum/meme/story names, mostly single-post reactions |

### Options vs. Equities
**Pure equities, no derivatives.** No occurrence of "call," "put," "LEAPS," "strike," or "contracts" anywhere in 85 posts. Positions are disclosed in plain share counts (575 `ICCT`, 895→1,600 `MTPLF`, 50 `OPEN`). This is a **long-only, cash-account-style retail equity trader**, not an options trader — de-risks the tail-risk profile relative to leveraged-options accounts, but the leveraged-ETF pairing on `$ONDS`/`$ONDL` reintroduces convexity she does not appear to price in.

### Macro vs. Technical vs. Narrative
Almost entirely **narrative/reactive, not technical or macro**. There is exactly one attempt at macro commentary (`$BTC`, Jun 27 '25) and it's a repost of someone else's X thread, not original analysis. Two corporate-news reposts (`$SMCI` 10-K filing, `$AVGO` buyback announcement) are headline shares with zero interpretation. The **one genuine piece of original analysis in the entire archive** is the `$CVU` post (Jan 8 '26): a well-organized, sourced small-cap defense DD (Raytheon-tied contracts, $509M backlog, funded-vs-unfunded backlog distinction) — competent work, self-aware about its own limits ("I'm just learning so I could be waaaay wrong"), and never repeated at that quality again. Everything else is: emotional reaction to her own P&L, or amplification of someone else's call (`@Freeballer`'s `$ONDS` DD, `@LANDO`'s trading philosophy, `@ThetaTard`'s `$MTPLF` stock-rig thesis, `@nuomena`'s BTC piece).

### What Drives Entries
1. **Social proof / community tips** — `$MTPLF`, `$ONDS`, and `$ICCT` all trace to other named traders' posts, not independent screening.
2. **Meme/hype momentum** — `$DGLY` ("Pre-Market Insanity... WTF moment"), `$BYND` ("did we all buy this meme stock today?"), `$OPEN` — all entered on visible price action/social buzz, not fundamentals.
3. **Sunk-cost re-engagement** — repeatedly returns to the same wounded names (`$ICCT` three times over 4 months, `$NVDA` five times, `$ONDS` eleven times) rather than diversifying into new ideas.
4. **Crowd-sourced decision-making** — the `$HIMS` "sell and secure the profit or hold it?" post (53 comments, 12 reactions) is a literal outsourcing of a hold/sell decision to the AfterHour crowd, not an internal framework.

---

## 3. Risk Management & PnL Reality

**Verdict: No exit discipline exists. She holds bags and narrates the pain in real time.**

Full-corpus keyword scan (85 posts):
- `"trim"` / `"trimmed"`: **0 occurrences**
- `"stop loss"` / `"stop-loss"`: **0 occurrences**
- `"took profit"` / `"take profit"` / `"sold half"`: **0 occurrences**
- `"hold"` / `"holding"`: **9 occurrences**, always about whether to keep an existing bag, never about position construction
- `"sell"`: **4 occurrences**, three of which are questions to the crowd, not decisions

### The averaging-down tell
`$MTPLF`: 895 shares (May 22 '25, "I'm dying here" as it "inches up slowly") → 1,600 shares (Nov 25 '25, down 76.5% / -$12,000). She **added ~79% more shares to a position that was actively collapsing** rather than cutting it — the single clearest quantified bag-holding data point in the archive.

### Documented Wins
- `$ICCT` (Apr 1 '25): bought 575 shares pre-market at $3.10, sold at $5.00 — a clean, disciplined day-trade win (+$1,092, +61%). Notably her **only** example of actually executing a plan start-to-finish.
- `$OPEN` (Jul 21 '25): 50 shares, unspecified gain, self-described as small ("Unfortunately this was not one I YOLOed, it's only 50 shares. I still count it as a WIN!").
- `$ONDS` (Dec 29 '25 - Jan '26): "Look who's GREEN," bought back in and rode a genuine rally on `@Freeballer`'s catalyst call.

### Documented Blow-ups
- **`$MTPLF`, -76.5% / -$12,000 realized-or-marked loss** on 1,600 shares (confirmed Nov 25 '25) — the single largest quantified loss in the archive, self-tagged `[Funny]`, not `[Loss]` — she minimizes the size of this loss with humor rather than flagging it as risk.
- **The Aug '25-Dec '25 blackout drawdown**: verified capital fell an implied 36.8% (97.7K → 61.8K) during the exact window her portfolio link was broken — the worst damage happened off the record.
- **`$ICCT` slow bleed**: entered a second time (May 28 '25, "I think I see a faint heartbeat"), held through Aug 5 '25 ("What's going on here?! I just want OUT!") with no evidence of ever actually exiting cleanly.
- **`$ONDS` "buy the dip" reframe** (Feb 4 '26): bought more at $9.33 framed as a silver lining during a loss-tagged post — the stock, and her overall capital, continued down into the Jul '26 lifetime low.

**Net PnL Reality**: Wins are small, quick, and enthusiastically declared (`[Gain]` tag used 12 times). Losses are larger, slower, and either downplayed with humor or hidden behind a disconnected portfolio link (`[Loss]` tag used 13 times — nearly balanced tag count, but the two categories are not remotely balanced in dollar terms). This is the textbook **asymmetric retail pattern: cut winners early, let losers compound, and stop looking when it gets bad.**

---

## 4. Behavioral & Sentiment Signals

### Why she posts
1. **Emotional processing / community catharsis, not signal-sharing.** Her single highest-engagement posts are *not* trade calls: "Please tell me at least 1 thing you're thankful for" (64 comments, a suicide-prevention/gratitude PSA, Nov 27 '25), "Indiana Norther Lights" typo joke (41 reactions, highest of the sample), "🛑 FUCKING STOP 🛑" political-division PSA (49 comments, Dec 31 '25). She functions as a **community-glue / mental-health-aware figure** first, trader second.
2. **Amplification of other traders**, not origination: unprompted shout-outs to `@LANDO` ("a 17 year old but he knows his $h!t"), `@Freeballer` ("Did it again!" x2 on `$ONDS` calls), `@Tron` (fundraising ask), `@SonnySide` ("for the ladies of AH"). She is a node in the community graph, not a hub of original ideas.
3. **Susceptibility to gamified broker promotions.** Six posts (Dec 27 '25 - Jan 1 '26) are consumed entirely by a Robinhood "HOOD Holidays" referral/clicking game — she doesn't know what she agreed to ("I hit 'count me in' for something but I don't know what?!"), keeps engaging anyway, and separately shares an "Alpha" AI-app referral link (Feb 3 '26, "Just got my Alpha"). Zero trading content, pure affiliate-loop engagement — a real behavioral vulnerability to gamification/FOMO mechanics distinct from her equity trading.

### Linguistic tics (recurring)
- **Anthropomorphizing every position as a relationship**: "We have a love/hate relationship" (`$NVDA`), "toying with my emotions?! Or is it just like my ex boyfriend" (green day), "WHY do you hate me?!" (`$NVDA` loss), "today kinda feels like... but it's fine, everything is fine" (`$ONDS` loss). This language reliably appears *during* drawdowns in a name she's holding — never during a clean, planned entry.
- Excessive punctuation/emoji stacking as an anxiety marker (multiple `?!` and `😳`/`🩸` on loss days), a "pretend I'm holding my shit together" self-awareness (Mar 4 '25) about performing composure for the community.
- Feminine self-identification is consistent throughout ("ladies of AH," 🤦🏼‍♀️, "my ex boyfriend").

### Reaction to volatility / red days
She posts through red days but the content shifts from analysis to venting or crowd-polling — never a stated risk decision. "Pre-game's not looking good. I wish you all luck" and "exactly how long do I have to pretend I'm holding my shit together" (both Feb-Mar '25 red-day posts) show she absorbs market stress publicly and performs resilience for an audience rather than acting on a plan.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

| Priority | Tag | Rationale |
|---|---|---|
| **Primary** | `NARRATIVE_BAGHOLDER_NO_STOPS` | Zero stop-loss/trim vocabulary across 85 posts; averages down into a collapsing concentrated position (`$MTPLF` 895→1,600 shares, -76.5%); documented -57.4% lifetime capital erosion |
| **Secondary** | `SOCIAL_AMPLIFIER_LOW_ORIGINATION` | Core positions (`$MTPLF`, `$ONDS`, `$ICCT`) traced to other named traders' calls; only one original, competently-sourced DD (`$CVU`) in the full sample |
| **Tertiary** | `RETAIL_SENTIMENT_BAROMETER` | Anthropomorphizing/exasperation language ("why do you hate me," "I just want OUT") is a reliable emotional-extreme marker, usable only as a contrarian timing tell, never as a directional signal to copy |
| Watch-flag | `GAMIFIED_PROMO_SUSCEPTIBLE` | Engages heavily and uncritically with broker referral/affiliate gimmicks (`$HOOD` giveaway, "Alpha" app link) — zero signal value, flag as noise source |

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 18 / 100**

| Component | Score (/25) | Notes |
|---|---|---|
| Idea Generation / Catalyst ID | 6/25 | Almost entirely reactive or copied from other traders; the one original DD (`$CVU`) is genuinely good but is a single data point in 85 posts |
| Risk-Adjusted Execution | 2/25 | Zero stop-loss/trim vocabulary; documented averaging-down into a -76.5% loser; no evidence of a single planned, complete exit outside the one `$ICCT` day-trade |
| Consistency / Repeatability | 6/25 | The *failure* mode is highly consistent (anthropomorphize → hold → capitulate), which makes her fadeable, but there is no consistent positive process to harvest |
| Capital Discipline | 4/25 | Verified lifetime capital down -57.4%, with the largest damage occurring during a self-reported portfolio-link blackout that coincides with her worst loss |

**Expectancy**: **Negative and verified.** Unlike accounts that show a fat-tailed but net-positive lifetime curve, this account's `amount_k` series is a **sustained bleed** from $107.9K to $45.96K with no full recovery at any point after the Feb '25 peak. There is no dollar-weighted evidence of a repeatable edge to harvest directly from her trades.

### 5.3 Signal Flow Ingestion Matrix

| Signal Type | Example Trigger | Ingest? | Action | Confidence |
|---|---|---|---|---|
| Repost/amplification of a named trader's DD | "`@Freeballer` did it again!" (`$ONDS`) | ✅ YES (indirect) | Route the **original** trader's post to Artemis, not her repost — she is a discovery pointer only | Medium |
| Rare original fundamental DD | `$CVU` backlog/Raytheon post | ✅ YES | Flag ticker for independent screen — competent, sourced, worth a second look | Medium-High |
| Anthropomorphizing/relationship language about a held position | "Why do you hate me?!", "toying with my emotions" | 🚫 FADE | Log as an emotional-extreme marker in that name; historically clusters near local tops or capitulation lows, not mid-trend | High (contrarian) |
| Averaging down into a losing concentrated position | `$MTPLF` 895→1,600 shares while down | 🚫 BLACKLIST | Never mirror sizing; log as bag-holding continuation, not conviction | High |
| Crowd-sourced "sell or hold?" poll on her own position | `$HIMS` sell/hold dilemma | 🚫 DO NOT MIRROR | Signals absence of an internal framework; treat the resulting crowd sentiment as noisy, not predictive | Low |
| Broker referral / gamified promo thread | `$HOOD` Holidays giveaway, "Alpha" app link | 🚫 FIREWALL | Zero trading signal; exclude from any engagement-weighted sentiment score | N/A |
| Portfolio-link "blackout" (0.0/null `amount_k` readings) | Aug-Dec '25 stretch | ⚠️ FADE-WATCH | Treat as a hidden-drawdown flag — reconnection value has historically landed materially below the last clean pre-blackout mark | Medium (timing tell) |
| Capitulation/exhaustion language on a long-held loser | "I just want OUT!" (`$ICCT`, 3+ months held) | ⚠️ CONTRARIAN NIBBLE ONLY | Retail capitulation can mark local exhaustion; small, hard-capped size only, never a full position | Low-Medium |
| Leveraged + common product held simultaneously | `$ONDS` + `$ONDL` "LFG Loooong" | 🚫 BLACKLIST | Convexity/decay risk not being priced by the source; never scale exposure off this disclosure | N/A |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest)**
1. Use her amplification posts purely as **routing pointers** — when she shouts out `@Freeballer`, `@LANDO`, or `@ThetaTard`, pull the *cited trader's original post* into the pipeline, not hers.
2. Flag any future `$CVU`-style original DD (sourced financials, named contracts, explicit backlog figures, self-aware uncertainty framing) for an independent Artemis fundamental screen — rare, but real when it appears.
3. Her plain-share, no-options disclosure style makes any position size she reveals easy to verify against price action — useful as a low-cost retail-positioning proxy for the tickers she names, never as a sizing template.

**Contrarian Fade Directives**
1. **Fade any post where she addresses a held ticker emotionally** ("why do you hate me," "toying with my emotions," "everything is fine") — this language is a documented marker of being underwater in a position with no plan, not a read on the ticker itself.
2. **Fade "buying the dip as a silver lining" framing** (`$ONDS` at $9.33, Feb '26) — historically precedes further downside in-sample rather than a bottom.
3. **Fade crowd-sourced "sell or hold?" posts** as evidence the underlying name has an unusually large contingent of framework-less retail holders, not as a read on fair value.

**Mandatory Risk Blacklists & Firewalls**
1. **Never mirror her position sizing or averaging-down behavior** — the `$MTPLF` 895→1,600-share add into a -76.5% loss is the single clearest disqualifying data point in the archive.
2. **Firewall all broker-affiliate/gamified-promo content** sourced from her posts (`$HOOD` Holidays, "Alpha" app referral) — zero trading signal, pure viral-loop engagement; exclude from any sentiment-weighting model entirely.
3. **Blacklist simultaneous common+leveraged product pairing** (`$ONDS`+`$ONDL`) as a sizing cue — she does not articulate leverage/decay awareness, and mirroring the combined exposure inherits undisclosed convexity risk.
4. **Treat any extended portfolio-link blackout as a hidden-drawdown flag**, not a data gap to ignore — in this profile the reconnection reading landed 36.8% below the last clean pre-blackout mark.

**Exit Rules & Alpha Rectification**
1. Because zero exit-discipline vocabulary appears anywhere in 85 posts, any strategy referencing her tickers **must run its own independent exit logic** — e.g., a hard -15% trailing stop from entry and a mechanical trim schedule (25% at +25%, 25% at +50%) — since her own realized outcome (-57.4% lifetime) proves the absence of exit discipline, not idea selection, is the dominant driver of her underperformance.
2. Use her rare, genuine capitulation language ("I just want OUT," 3+ months into a held loser) as a **small, hard-capped contrarian entry trigger** only — never a full-size position, and only after independent confirmation the name has stopped making new lows.
3. Any position opened on the back of her `$ONDS` amplification of `@Freeballer`'s calls should carry an explicit leverage firewall — never also hold the paired leveraged product (`$ONDL`) she discloses running alongside it.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Portfolio ($K) | Event |
|---|---|---|
| 2025-01-27 | 107.9 | First observed post — `$NVDA` reaction, account already funded |
| 2025-02-14 | 117.0 | `$HIMS` "sell and secure the profit or hold it?" — outsources a hold/sell call to the crowd (53 comments) |
| 2025-02-19 | **118.83 (lifetime peak)** | `$PLTR` community-sentiment repost — top of the observed range |
| 2025-03-04 | 100.6 | "Exactly how long do I have to pretend I'm holding my shit together???" — first explicit stress-performance admission |
| 2025-04-01 | 99.0 | `$ICCT` day-trade: bought 575sh @ $3.10 pre-market, sold @ $5 — the one clean, complete win in the archive |
| 2025-05-22 | 78.7 | `$MTPLF`, 895 shares, "I'm dying here" — early bag-holding tell on the position that later blows up |
| 2025-07-21 | 0.0 (artifact) | `$OPEN` win post; first explicit mention of the broken portfolio link ("port still not connecting correctly") |
| 2025-08-19 | **97.68 (last clean pre-blackout read)** | `$ACHR` — "why is this so low today??" |
| 2025-09 → 2025-12 | 0.0 / null (blackout) | ~4.5-month portfolio-link outage; worst documented loss (`$MTPLF` -76.5% / -$12,000, Nov 25) occurs entirely inside this unverified window |
| 2025-11-25 | 2.7 (artifact) | `$MTPLF`, 1,600 shares, down 76.5% over $12,000 — largest single quantified loss in the archive, tagged `[Funny]` |
| 2025-11-27 | 0.0 (artifact) | Suicide-prevention/gratitude PSA — highest-comment post of the sample (64) |
| 2025-12-27 → 2026-01-01 | 0.0 (artifact) | Six-post `$HOOD` Holidays referral-giveaway thread — zero trading content |
| 2026-01-01 | **61.78 (post-blackout reconnect)** | "Whoa! Port is connected!" — reconnection lands 36.8% below the last clean pre-blackout mark |
| 2026-01-08 | 71.5-71.6 | `$CVU` original DD post (Raytheon-tied backlog) — the one genuine analytical post in the sample |
| 2026-02-04 | 61.4 | `$ONDS` bought at $9.33 during a loss-tagged post, framed as a silver lining |
| 2026-02-05 | 0.0 (artifact) | "I don't chase narratives, I learn structure" — stated philosophy directly contradicted by the surrounding record |
| 2026-02-14 | **59.68 (local low)** | Quiet Valentine's Day post |
| 2026-03 → 2026-05 | n/a | **3-month total posting silence** — no trading activity disclosed |
| 2026-06-13 | 54.4 | "My how things have changed…" (`[Gain]` tag, unclear underlying trade) |
| 2026-07-16 | **41.82 (lifetime low, clean reading)** | `$ONDS`/`$ONDL` chart post, "This week…" — tagged `[Funny]` despite being the deepest verified drawdown point of the sample |
| 2026-08 | n/a | No posts |
| 2026-09-03 | **45.96 (most recent)** | Final observed post — community shout-out to `@SonnySide`, no trade content |

---

*End of dossier. Compiled by Sonnet for the Artemis Engine, TraderMatrix ingestion pipeline.*
