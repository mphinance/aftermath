# QUANT FORENSIC DOSSIER: @883Ismygovtname
### AfterHour Followed-Trader Autopsy — Artemis Engine Ingestion Report

| Field | Value |
|---|---|
| Handle | `@883Ismygovtname` (no stated real name; persona voice is consistently female — "hubby," "trad wife" jokes, "AH husband" bit) |
| Profile ID | `prf_494db31cac014f97888a761284ee1667` |
| Lifetime Posts Analyzed | 2,374 |
| Coverage Window | 2024-11-15 → 2026-09-10 (95.0 weeks / 665 days; posted on 549 of those days, 82.6%) |
| Source Files | `@883Ismygovtname_lifetime.md` (qualitative, full post text), `@883Ismygovtname_all_posts.json` (structured: `amount_k`, `tag`, `gain_loss`, `tickers`, `reaction_count`, `comment_count`, `view_count`) |
| Analyst | Sonnet 5, Artemis Quant Desk |
| Verdict (one line) | A genuinely disciplined, cash-only, multi-account **covered-call "wheel" income compounder** running a real, mechanically-defined premium-harvesting process across 360 tickers, layered under a small, openly-labeled "gambling money" satellite sleeve — the rare account in this cohort with a **reconcilable, credible capital trajectory** ($6–11K seed → ~$95K combined by month 21.5, contributions disclosed and separable from gains), whose actual weakness is not risk-blowup but a **structural "sell winners too early" leak** on her best speculative ideas (OPEN LEAP closed for 10% days before its 2025 meme run) — high value as an **income-mechanics and hedging-discipline template**, low-to-moderate value as a **directional stock-picking signal**. |

---

## 0. Data Provenance Note (read before trusting any number below)

This account is unusual among AfterHour "followed trader" archives in that its `amount_k` field is **real, auto-synced Robinhood portfolio data** for most of its life — not a disconnected metadata artifact. It tracks a rising account value from **$5.92K (Post #2, 2024-11-15) to $45.69K (Post #853, 2025-06-30)**, cleanly matching her own text-based dollar disclosures ("Cheating a little at the start with total 11k," Post #6) closely enough to be treated as trustworthy for that window.

**The sync then breaks, permanently, mid-archive.** Post #855 (2025-06-30, "Removed and Resyncing Port🤔") documents her disconnecting and reattaching the Robinhood integration; from Post #854 onward, `amount_k` reads exactly **`0.0` for the remaining 1,519 posts — 64% of the entire archive**, all the way to the 2026-09-10 close. This is a **structured-field outage, not a trading event** — do not read the zero as a portfolio wipeout. She continues to self-report account values manually and irregularly (full multi-account "Portfolio Review" posts at 2025-09-29, 2025-11-03, 2026-03-17, and 2026-08-28), which this dossier uses to reconstruct §1's post-breakage capital trajectory. **Any downstream Artemis ingestion of the raw `amount_k` field for this source must gate on `date < 2025-06-30`; treat every `0.0` after that date as missing data, never as a $0 balance.**

A second provenance note: the `tag`/`gain_loss` structured fields are **not** a P&L ledger for this trader. Only 4 posts are tagged `[Gain]` and 1 `[Loss]` in 2,374 posts — and all 5 are **social credit-giving posts thanking other AH traders for a tip** (§4), not her own trade closes. Her actual trade outcomes (hundreds of them) live entirely in unstructured free text ("bought back my covered call at 70% profit," "sold 25 shares," "STC $HOOD 40% profit") and must be extracted from post bodies, never from the `tag` field.

---

## 1. Executive Profile

**Trading philosophy (stated and, unusually for this cohort, actually followed):** She runs an explicit, three-layer, mechanically-defined system that she names consistently across nearly two years of posts:

1. **"100-Share Pony Farm" (taxable) / "Dream Team" (Traditional IRA)** — accumulate 100+ share "core" lots in a rotating list of small/mid-cap growth and income names, then run **cash-secured covered calls ("the Wheel")** against them continuously for premium income. Her own summary: *"These are my money generators. I don't plan to hold onto the stocks long-term. Just working premiums to DCA into my 100 share horses... That way I don't have to add capital to buy dips"* (Post #483, 2025-04-07) — i.e., the wheel is explicitly designed to **self-fund** the long-term core without new capital.
2. **A declared, ring-fenced "gambling money" bucket** for genuinely speculative bets — a leveraged-perpetuals experiment on BloFin, copy-trading two named traders (`Tawfeeq`, `MasterGroove`) — that she **self-terminated** after acknowledging it wasn't working: *"Maxed out gambling with making my own decisions. I will switch to paper trading/demo mode"* (Post #309, 2025-01-27). This is a rare, explicit instance in this cohort of a trader **downsizing a losing behavior on their own initiative**, not being forced out by a blow-up.
3. **A dividend/income sleeve inside the core** (SCHD, PFE, F, WEN, ET) with a stated target allocation ("25% $SCHD," later "200 shares $SCHD by year end") funded by automatic weekly $20–80 recurring buys.

**Hard risk rule, stated repeatedly and never violated in the sample: no margin.** *"I don't use margin. Cash only"* (Post, 2026 chop period); *"I'm always frightened by all the people getting margin called on this app"* (Post, mid-2026). Across 2,374 posts there is no instance of a margin call, a forced liquidation, or a "wiped out" event — a genuinely different risk profile from most of this cohort's high-cadence options accounts.

**Post cadence:** 2,374 posts / 95.0 weeks = **25.0 posts/week lifetime average (3.6/day)**, active on 82.6% of all days in the archive window — by far the highest-frequency account structure of this type in the pipeline (roughly 15× @dick's 1.63/wk). This is a running trade-and-life diary, not a curated tip feed.

| Phase | Approx. Posts | Span | Character |
|---|---|---|---|
| 2024-11 – 2024-12 (Genesis) | ~220 | 7 wk | Onboarding narrative — "lurking," learning covered calls, first $11K seed, horse/farm metaphor system crystallizes immediately (Post #6) |
| 2025-01 – 2025-03 (Wheel build-out + Sir Jack era) | ~240 | 13 wk | "$10M race" framing (borrowed from peer `Sir Jack`), BloFin leverage experiment opened and shut down, first documented drawdown (−27%, Feb–Mar) |
| 2025-04 (Tariff shock) | 111 | 4.4 wk | Calm, hedged response to the April 2025 "Liberation Day" tariff selloff — buys protective/speculative puts in both IRA and taxable, explicitly refuses to panic-sell |
| 2025-05 – 2025-06 (Peak synced growth) | ~280 | 8.6 wk | `amount_k` climbs to its final verified read, $45.69K (2025-06-30) |
| 2025-06-30 (Sync breaks) | — | — | Robinhood portfolio integration disconnected/reattached; auto-tracking never recovers (§0) |
| 2025-07 – 2025-12 (Post-sync, cadence still high) | ~830 | 26 wk | OPEN LEAP closed for only 10% profit (2025-07-08) days before Opendoor's 2025 meme run; manual portfolio-review posts resume ($52.4K Sep, $62.5K Nov) |
| 2026-01 – 2026-08 (Diversifying reach) | ~590 | 34 wk | View counts explode 10–200× (avg views 2.6 in Jan-26 → 946 in Jun-26) as she launches a YouTube channel and Spotify podcast; comment counts per post *fall* over the same window — the same "reach up, native engagement down" fingerprint documented on other monetizing AH accounts, though **she explicitly declines Discord and paid subscriptions** ("Still no discord... not paying for anything," Post #2344, 2026-08-28) — a materially different monetization posture than the Substack-funnel pattern seen elsewhere in this cohort |
| 2026-09 (archive tail) | 22 | 1.4 wk | Still fully active at archive close; hits a stated milestone (1,000 shares $SOFI, 25% target) on the final day |

**Active timeline:** No retirement, no extended silence longer than a few days anywhere in 665 days, no account closure. Last post (2026-09-10, archive end = "today") is an ordinary, in-process trade note (a $PBR trim, an $HPE cash-secured-put plan) — this is a **live, ongoing account**, not a closed case study.

**Verified capital trajectory:** This is the most reconstructable capital record encountered in this dossier series, because she explicitly separates *contributed* capital from *account value* at multiple points:

| Date | Disclosed value | Source | Notes |
|---|---|---|---|
| 2024-11-15 | $5.92K–$6.07K | `amount_k` (auto-synced) | Seed; she separately claims "started with 11k" total intended capital (Post #6) |
| 2024-11-20 | $8.09K–$10.57K | `amount_k` | Fast initial ramp as remaining cash is deployed |
| 2025-02-24 | $31.63K | `amount_k` | Local peak before the Feb–Mar drawdown |
| 2025-03-14 | $22.85K | `amount_k` | Trough — a **−27.7% drawdown** from the Feb peak |
| 2025-06-30 | **$45.69K** | `amount_k` (last auto-synced reading — see §0) | Peak of the verified-by-structured-data era; ~7.5 months, seed-to-peak return **~+300–670%** depending on which seed figure is used |
| 2025-09-29 | $52.44K (combined, all accounts) | Manual "Portfolio Review" post #1276 | First post-breakage combined-account disclosure |
| 2025-11-03 | $62.54K (combined) | Post #1492 | |
| 2026-03-17 | $78.81K (combined: Investing $60.31K + IRA $17.00K + Pineapple $1.50K) | Post #2014 | |
| 2026-08-26 | **$94.99K** (combined: Investing $74.67K + IRA $18.16K + Pineapple $2.17K) | Post #2344, full audited breakdown | Most detailed disclosure in the archive — itemized share counts, options, crypto, per-account buying power |

**Contribution reconciliation (why this trajectory is credible, not just self-reported):** She repeats a standing disclaimer across dozens of posts: *"My trading port is locked. I don't import money in for trading. Started with 11k. Robinhood IRA added 7k 2024, 6–7k 2025 to be max contribution"* (Posts #6599–#8233 and recurring). That means of the ~$27K in known cash contributed over 21.5 months (~$11K seed + ~$14K in IRA max-contributions + modest weekly $20–80 SCHD/BTC DCA), the account grew to **~$95K** — implying the *un-contributed*, organic gain is on the order of **$65–68K**, concentrated almost entirely in the untouched taxable "Pony Farm" account (~$11K → $74.67K, roughly **+580%** with zero new capital by her own account). This is a genuinely differentiating data point for Artemis: **most self-reported AH capital trajectories in this pipeline cannot be separated from contributions; this one explicitly can.**

**Drawdown history:** One clean, quantified drawdown (−27.7%, Feb 24 → Mar 14 2025, general market chop) with a documented recovery inside 6 weeks and no capitulation selling. One calmly-hedged macro shock (April 2025 tariff selloff — bought puts, held core, explicitly refused to panic-sell). One severe but **dollar-unquantified** single-position loss disclosed near the archive's end: *"Obviously, I took a very big loss on ASTS calls... I should have sold earlier"* (Post #2347, 2026-08-30) — the most candid loss admission in the archive, paired with a stated (not yet delivered as of archive close) intent to record a podcast on her "eight biggest losses" ("Loss porn").

---

## 2. Ticker Universe & Catalysts

**Breadth:** **360 unique tickers** mentioned across 2,374 posts — an extremely sprawling universe by any standard, reflecting the wheel-strategy's core mechanic (continuously rotate 100-share lots in and out as calls get assigned).

**Top-mentioned tickers (post count):**

| Ticker | Mentions | Role |
|---|---|---|
| $ASTS (AST SpaceMobile) | 484 | Flagship long-held core position; wheeled continuously Dec 2024 → archive end (21+ months); largest single disclosed loss event is on ASTS calls (2026-08) |
| $SOFI | 332 | Second flagship core; explicit stated target of 25%-of-portfolio / 1,000 shares, achieved on the archive's final day (2026-09-09) |
| $HOOD | 263 | Core wheel name; also a running meta-joke ("Robin Hood" pun threads through the horse/pony branding) |
| $OPEN (Opendoor) | 200 | Sourced from peer `Sir Jack`; LEAP closed for only +10% five days before Opendoor's mid-2025 meme squeeze — the clearest "sold too early" case in the archive |
| $SOUN | 190 | Core wheel name since the archive's first week |
| $SCHD | 171 | Dedicated dividend/DRIP compounding sleeve, explicit target allocation and weekly auto-buy |
| $F, $PFE, $ET, $WEN | 150 / 132 / 101 / 94 | Secondary dividend/income sleeve names |
| $QBTS, $NVTS, $OKLO, $IREN | 131 / 123 / 103 / 91 | Thematic quantum-computing / power / nuclear / bitcoin-mining satellite names, generally peer-sourced |
| $BTC, $ETHA, $TSLL, $IBIT | 82 / 94 / 92 / 58 | Crypto/leveraged-ETF satellite sleeve, small weekly DCA discipline |

**Instrument mix:** Overwhelmingly **covered calls and cash-secured puts on a rotating equity base** — the "wheel" is the dominant, load-bearing strategy across virtually every ticker in the top 20. Layered on top: (a) a genuine long-term buy-and-hold core in ASTS/SOFI/OPEN/SOUN sized toward stated percentage targets; (b) a dividend-compounding sleeve (SCHD/PFE/F/WEN/ET) funded by automatic recurring buys; (c) occasional speculative LEAPS calls/puts on high-beta names (NVDA, NVDL, TSLA, AMC); (d) a small, explicitly labeled crypto satellite (BTC/ETH/IBIT/ETHA, $20–25/week DCA); (e) a short-lived, self-terminated leveraged-perpetuals experiment on BloFin. **Options are held in both the taxable account and the Traditional IRA** (calls, puts, and CSPs inside the IRA specifically to harvest premium tax-advantaged) — a more sophisticated account-structuring choice than typically seen in this cohort.

**What drives entries, in order of frequency:**
1. **Mechanical wheel-cycle reinvestment** — an assignment frees cash, which is immediately redeployed into the next "pony" at the day's best available entry; this is the dominant, highest-volume pattern and the actual engine of the account.
2. **Peer/community credit-tag calls** — she explicitly and repeatedly thanks named AH figures for specific ideas: `Sir Jack` (OPEN, and the original "$10M" goal framing itself), `@dick` (SNES — the account profiled elsewhere in this pipeline, also her running "AH husband" bit, §4), `Finkle` (OKLO), `freeballer` (HOOD), `MASTERGROOVE` (an NVDA put, "77% profit"). These credit posts are a genuine, checkable provenance trail for where her best ideas actually originate.
3. **Macro/calendar catalysts** — FOMC dates tracked explicitly and traded around (buying back calls ahead of a feared rate-hike surprise, Post #2349, 2026-08-31); the April 2025 tariff shock produced a deliberate, hedged repositioning (puts bought in both IRA and taxable) rather than a reactive one.
4. **Dividend/DRIP discipline** — SCHD/PFE/F/WEN/ET buys are scheduled and target-allocation-driven, not catalyst-driven at all; this is pure systematic compounding.
5. **Thematic/meme piggybacking, always small** — quantum computing (QBTS basket), bitcoin miners (IREN/MARA/RIOT), and nuclear (OKLO) names are added opportunistically off community chatter, but consistently sized as "gambling money" or single 100-share lots rather than concentrated bets.

---

## 3. Risk Management & PnL Reality

**Does she take profits, or hold bags? Overwhelmingly the former — this is the account's genuine, quantifiable edge.**

- **A real, stated, mechanical profit-taking rule on the wheel side**: *"I usually like to take profits around at least 70 if not 80 to 90% of my covered calls before I buy them back"* (Post #2349, 2026-08-31) — i.e., close a short call once ~70–90% of its extrinsic value has decayed, freeing capital to re-sell rather than waiting for worthless expiration. This is documented in dozens of posts across the archive (SOFI bought back at 77% and 50% profit, SMCI at ~70%, LYFT/OPEN calls in the IRA at ~70%) and is a **genuinely replicable, quantifiable exit heuristic** — the single most useful piece of process in this dossier.
- **Assignment-tolerant, not assignment-averse**: she lets shares get called away routinely (NIO, NOK both assigned during the April 2025 crash) without regret or attempts to roll defensively, then simply re-enters the wheel on the next name in rotation. Rolling is explicitly described as more effort than it's worth for her style (Post #10, 2024-11-21: *"rolling a call seems like a lot... I am a brand new horse trainer"*).
- **Real, disclosed hedging behavior** — a rarity in this cohort: during the April 2025 tariff selloff she bought puts in **both** the IRA and taxable accounts specifically as portfolio insurance/speculation on further downside (Post #483, 2025-04-07), while simultaneously stating *"I plan on staying in most of my positions if not buying more shares... full disclosure, I have no intention to sell out of my shares"* (Post #482) — hedge the tape, don't abandon the core.

**Documented wins vs. blow-ups:**
- **Zero margin calls, zero "wiped out"/"blew up" admissions, and no forced liquidation anywhere in 2,374 posts.** The account's structured `[Gain]`/`[Loss]` tags (4/1 respectively) are, as noted in §0, social credit-giving posts, not a self-curated highlight reel — this account does **not** perform the "at peak" survivorship-bias pattern documented on other AH feeds in this pipeline; instead it discloses hundreds of small, unglamorous, real-time trade outcomes (a $2,700 assignment, a $600 profit swept into SCHD, a $100 PBR trim) as a matter of routine, near-daily narration.
- **The account's real structural leak is the inverse of bag-holding: selling winners too early.** The clearest case: an OPEN LEAP bought 2025-07-03 (following `Sir Jack`) was closed for only **+10% profit** on 2025-07-08 — five days before Opendoor's mid-2025 meme-stock run, which continued for weeks and produced multiples of that return for anyone still holding. Her own words at the close: *"Being quite aggressive because it is a penny stock... that makes me nervous. So I'm happy with 10%"* (Post #890). A parallel pattern recurs on SOUN LEAPS (closed same day, same stated reasoning) and $OKTA ("Sold to early but... profits are profits. I'm such a paperhanded b!tch," Post, 2026-08).
- **The most severe loss in the archive is dollar-unquantified and self-admitted late**: "a very big loss on ASTS calls" surfaces only in a 2026-08-30 "P&L week and month" recap, alongside an explicit self-diagnosis ("It's my fault. I should have sold earlier") and a promised (undelivered as of archive close) "loss porn" retrospective on her eight biggest losses — an unusually candid gesture, but one that also means **the true magnitude of this loss cannot be reconstructed from the text alone.**
- **No disclosed stop-loss discipline on the long-term core** (ASTS, SOFI, OPEN, SOUN are held through drawdowns as a matter of policy — the wheel's premium income is the implicit "stop," not a price level) — consistent with, and the mirror image of, the profit-taking discipline on the option side.

**Net PnL reality assessment:** Because the wheel/covered-call mechanic generates continuous, small, real cash flow rather than lottery-ticket-sized wins, this account's numbers are structurally harder to overstate than a pure directional-picker's — there is no equivalent of an "at peak" boast to inflate, because there is no single flagship 10-bagger being marketed. The credible, contribution-adjusted account growth (~$27K contributed → ~$95K combined value, §1) stands as the strongest, most independently-supportable capital claim encountered in this dossier series to date.

---

## 4. Behavioral & Sentiment Signals

**Why is she posting?** Three stated, and largely consistent, motives:
1. **Explicit teaching/accountability, with an anti-guru stance repeated verbatim across the archive**: *"Posting for everyone to see and learn from my mistakes"* (Post #1, era); *"I don't ask for followers — just that you learn"*; *"I'm not selling anything... just learning out loud"* (Post, ~2025-Q1). This is corroborated by behavior: no Discord, no paid tier, no urgency-copy, across 2,374 posts and nearly two years — a materially different posture than the Substack-funnel pattern documented on comparable high-cadence AH accounts in this pipeline.
2. **A deliberately performed, self-aware relationship/drama persona** used to drive engagement — and she says so directly: *"In real life, I am divorced. But my husband did not leave me... it was an amicable divorce, but people on AH like drama, and I love to feed into it"* (Post, ~2025-05). The recurring "AH husband" bit is played out publicly with `@dick` (the subject of a separate dossier in this same pipeline — cross-reference: their accounts have a running public flirtation/rivalry dynamic, which functions as **mutual audience cross-promotion between two followed traders**, not as independent trading signal from either side) and with a rotating cast of "trad husband"/"trad wife" jokes.
3. **Platform diversification without monetization**, from 2026 onward: launches a YouTube channel and Spotify podcast to house weekly portfolio reviews, begins cross-posting to "Robinhood Social," but explicitly declines to gate any of it — *"Still no discord... I'm someone who's gonna stay away from paid subscriptions for now. Not putting one out. Not paying for anything"* (Post #2344, 2026-08-28). View counts still explode 10–200× over this period (avg. views per post: 2.6 in Jan-2026 → 946 in Jun-2026) even without a paywall, while comment counts per post decline — the same reach-up/native-engagement-down signature seen elsewhere in this cohort, but here it is a byproduct of cross-platform reach rather than a funnel mechanic.

**Recurring linguistic patterns:**
- **An extended, load-bearing horse/farm metaphor system**, present from Post #6 onward and never dropped: "ponies" = 100-share core positions, "the pasture/stable/farm" = the whole portfolio, "workhorse check" = a stated 100-share-position audit, "Dream Team" = the Traditional IRA, "Wheel of Fortune: Weekly plays" = the recurring covered-call rotation post. This is genuinely useful as a **parsing key** for Artemis's own ingestion — nearly every structural update post follows this template and can be regex-matched.
- **Reaction to red/volatile days: calm, "gentle non-panic reminder" tone, never capitulatory but also never defiantly bullish-bragging.** During the April 2025 tariff crash: *"You can sell whole shares for some stocks 24 hours on Robinhood... I plan on staying in most of my positions if not buying more shares... full disclosure, I have no intention to sell out of my shares"* (Post #482). This is a materially different sentiment fingerprint than the "market red, my pick green" bravado documented on other AH accounts — closer to "boring and mechanical" than "combative."
- **A self-aware risk-appetite downgrade over time, stated explicitly**: the original "$10 million" goal (Post #1, and repeated through 2025) is explicitly sourced to Reddit and to peer `Sir Jack`'s aggressive share-only run — but by late 2025 she revises it down in her own words: *"As I've learned more about myself, I've also realized I'm probably not the type to aggressively scale through risk. I prefer buying good companies and letting them work for me"* (Post #2087, 2025-Q4). **This is a rare instance in this cohort of a trader downgrading their own stated risk appetite over time rather than escalating it** — worth treating as a genuine maturation signal, not mere goal-drift.
- **Music-lyric post titles/intros** (Aloe Blacc "I Need a Dollar," Destiny's Child "Say My Name") used consistently as framing devices for portfolio-review and P&L posts — a stylistic tell, not a trading signal, but useful for automated post-classification.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

- **Primary: `COVERED_CALL_WHEEL_COMPOUNDER`** — a genuine, mechanically-defined, repeatable income-generation process (sell covered calls/CSPs against a rotating 100-share core, buy back at 70–90% profit decay, redeploy) run consistently across 21+ months, two account types (taxable + IRA), and hundreds of individual tickers. This is process, not thesis-driven stock-picking, and it is the account's real, harvestable edge.
- **Secondary: `DIVERSIFIED_SATELLITE_SPECULATOR`** — a small, explicitly labeled, and self-policed "gambling money" sleeve (leveraged crypto perps, copy-trading, meme-adjacent LEAPS on OPEN/SOUN/NVDL) that is genuinely ring-fenced from the core (never threatens the taxable/IRA balances) and was voluntarily downsized after underperforming — useful as a **sentiment/idea-sourcing lead only**, never for sizing.
- **Behavioral flag (non-trading, informational): `DUAL_ACCOUNT_PERSONA`** — deliberately performs a drama/relationship narrative (with `@dick`, among others) for AH engagement while disclosing this is a performance layered over a real, disciplined, undramatic underlying process; not a compliance risk (contrast with toxic-content flags elsewhere in this pipeline), but Artemis should not weight the persona content (romance bits, "trad wife" jokes, credit-tag flirtation) as trading signal of any kind.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 58 / 100**

Justification: this account scores meaningfully above the cohort median not because of stock-picking skill (her entries are mostly peer-sourced or purely mechanical wheel-rotation, and 360 tickers is too broad a net to claim genuine idea-generation edge) but because of **process quality and capital-trajectory credibility**, both of which are unusually strong for this population. **Upside contributors:** (a) a real, quantifiable, replicable profit-taking rule (buy back short calls at 70–90% decay) documented across dozens of instances; (b) a hard, never-violated no-margin policy; (c) a genuine, disclosed hedging action during the one real macro-shock event in the sample (April 2025 tariffs); (d) a capital trajectory that is **actually separable into contributions vs. organic gains** — a rarity in this dossier series — supporting a credible ~+580% organic return on the untouched taxable account over 21.5 months; (e) a self-terminated bad habit (BloFin leverage) rather than an externally-forced blow-up; (f) a self-aware, documented risk-appetite *downgrade* over time. **Downside contributors:** (a) a structural "sells winners too early" leak that has already cost her the single largest identifiable opportunity in the archive (the OPEN LEAP, closed for +10% five days before a multi-hundred-percent meme run); (b) the single largest disclosed loss in the archive (ASTS calls, 2026-08) is dollar-unquantified, meaning the account's true drawdown-adjusted return cannot be fully verified; (c) 360-ticker breadth dilutes any claim to genuine per-name conviction or edge — most names are wheel-fodder, not theses; (d) no disclosed sizing discipline or position-limit framework beyond loose percentage-of-portfolio targets (25% SOFI/SCHD) stated after the fact rather than planned in advance.

**Expectancy:** Two distinct regimes, and they should be scored and ingested separately:
- **Wheel/premium-harvesting expectancy (replicate the mechanic — sell covered calls/CSPs on a diversified core, close at 70–90% profit, redeploy): plausibly real and modestly positive, low-variance.** This is theta-harvesting, not direction-calling; it does not require agreeing with her stock selection to extract value from the process itself.
- **Directional/idea-sourcing expectancy (mirror her specific entries and exits): weak to negative on the option-buying side specifically**, because the demonstrated pattern is early profit-taking on her best ideas (OPEN, SOUN) — copying her *exits* on speculative LEAPS would have meant leaving the majority of 2025's Opendoor meme-run gains on the table. Copying her *core equity adds* (ASTS, SOFI at stated allocation targets) is closer to a disciplined DCA/accumulation signal and carries more replicable value than the options-timing side.

### 5.3 Signal Flow Ingestion Matrix

| Signal Type | Source Posts | Raw Reliability | Recommended Artemis Treatment | Weight |
|---|---|---|---|---|
| Covered-call buyback rule (close short calls at 70–90% profit decay, redeploy) | ~40+ posts across the full archive | High (mechanical, repeated, internally consistent) | **INGEST as a standalone exit heuristic** for any Artemis-run covered-call/wheel book, independent of her specific tickers | 0.6 |
| Multi-account "Portfolio Review" snapshots (itemized share counts, options, per-account values) | 4 major posts (2025-09-29, 2025-11-03, 2026-03-17, 2026-08-28) + `amount_k` pre-2025-06-30 | High (internally consistent, contribution-adjusted, cross-checkable against her own disclaimers) | **INGEST as the capital-trajectory ground truth** for this source — the most reliable such record in this dossier series | 0.7 |
| Peer/community credit-tag calls (Sir Jack → OPEN; Finkle → OKLO; freeballer → HOOD; MasterGroove → NVDA put) | ~10 explicit credit posts | Medium (dated, named, checkable, but reflects a second-hand idea, not her own research) | **INGEST as a secondary lead pointing to the *named peer's* account**, not as a first-order signal from this source | 0.3 |
| Hedging behavior during confirmed macro shocks (April 2025 tariff puts, both IRA and taxable) | ~15 posts, 2025-04-02 to 04-07 | Medium-High (real, timestamped, non-panic execution) | **INGEST the behavioral pattern** ("hedge with puts, hold the core, don't panic-sell") as a regime-response template, re-verify sizing independently | 0.4 |
| Dividend/DRIP compounding sleeve (SCHD/PFE/F/WEN/ET target allocations, recurring buys) | ~30 posts | Medium (systematic, low-conviction-required) | **INGEST as a passive income-sleeve template**, not as a stock-picking signal | 0.3 |
| Speculative LEAPS calls/puts on high-beta or meme-adjacent names (OPEN, SOUN, NVDL, NVDA puts) | ~25 posts | Low as an entry/exit-timing signal (demonstrated early-exit leak) | **DISCARD exit timing; retain only the entry ticker/date as a universe-discovery lead** to be independently re-timed | 0.15 (entry only) |
| BloFin leveraged-crypto / copy-trading experiment | ~15 posts, 2025-01 | None (self-terminated at a loss, explicitly disclosed as "maxed out gambling") | **DISCARD entirely** — she discarded it herself; do not resurrect it as a signal source | 0.0 |
| Relationship/drama/persona content ("AH husband," "trad wife" bits, music-lyric framing) | 100+ posts | None as trading signal | **DISCARD from all scoring**; may be used only for source-classification/parsing (post-type detection), never for conviction weighting | 0.0 |
| Structured `tag`/`gain_loss` fields | 5/2,374 posts populated meaningfully | None as a P&L record (§0) | **DISCARD** — extract P&L exclusively from free-text trade narration | 0.0 |
| `amount_k` field after 2025-06-30 | 1,519/2,374 posts (all read `0.0`) | None (broken sync, not a balance) | **DISCARD / mask as missing**, never interpret as $0 (§0) | N/A |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Implement the **70–90%-profit-decay covered-call buyback rule** as a standalone, ticker-agnostic exit heuristic inside any Artemis wheel/income module — this is the single most replicable, mechanically-sound piece of process in the archive and does not depend on trusting her stock selection.
2. Treat her **contribution-adjusted, multi-account portfolio-review disclosures** as the calibration baseline for what a disciplined, cash-only, no-margin retail wheel account can realistically compound to over ~2 years (~$27K contributed → ~$95K, primarily organic growth in the untouched taxable sleeve) — useful as a sanity-check benchmark for Artemis's own income-strategy backtests.
3. Log her **hedge-don't-flee response to the April 2025 tariff shock** (buy puts in both taxable and IRA, hold the equity core, explicit no-panic-sell stance) as a candidate regime-response template for genuine broad-market shocks, independently sized.
4. Route peer-credit-tag posts (Sir Jack, Finkle, freeballer, MasterGroove) to the **named peer's own account** as the primary lead, using her post only as a secondary, dated confirmation that the idea was circulating in the AH community at that time.

**Contrarian Fade Directives (when to fade her / the retail herd she represents):**
1. **Fade her own profit-taking on high-beta speculative LEAPS specifically** — her demonstrated pattern (OPEN, SOUN, OKTA) is exiting winners at the first double-digit percentage gain out of risk-aversion on volatile/penny-priced names; if Artemis independently holds conviction on a name she's exited early, her exit should not be read as new bearish information.
2. When her posts show a **rapid escalation of "gambling money" activity** (adding a new leveraged/copy-trading vehicle, upsizing a satellite speculative position) treat this as a **personal risk-appetite spike worth noting but not following** — her own text shows this behavior gets self-corrected within weeks, historically at a loss.
3. Do not treat her broad, 360-ticker universe as a diversified "buy list" — most names in it are one-off wheel-fodder with a single 100-share lot and no stated thesis; only the handful of names she assigns explicit percentage-of-portfolio targets (ASTS, SOFI, SCHD) carry genuine conviction weight.

**Mandatory Risk Blacklists & Firewalls:**
1. **Never interpret `amount_k = 0.0` for any post dated 2025-06-30 or later as a real account balance** — it is a broken-sync artifact, not a $0 or blow-up event (§0). Any automated capital-trajectory model for this source must explicitly mask this range.
2. **Never treat the `tag`/`gain_loss` structured fields as a P&L ledger for this source** — only 5 posts in 2,374 carry a meaningful value, and all 5 are social credit-giving posts about *other* traders' calls, not her own realized outcomes.
3. **Blacklist copying entry mechanics from the BloFin leveraged-crypto or copy-trading experiment** — self-disclosed as a "maxed out gambling" mistake and voluntarily shut down; no cost basis, sizing, or leverage ratio is ever cleanly disclosed for it.
4. **Do not weight relationship/persona-drama content ("AH husband," romantic bits with named peers) as trading signal** — she explicitly discloses this is a performed engagement device layered over her real, disciplined process.

**Exit Rules & Alpha Rectification:**
1. Any Artemis-run income/wheel strategy sourced from this account's process should implement the **70–90%-decay buyback rule** as its default short-option exit, independently backtested rather than assumed to transfer 1:1 to different underlyings or vol regimes.
2. For any speculative LEAPS/options idea traced to a peer-credit-tag post (Sir Jack/OPEN being the clearest case), Artemis should apply **its own trailing/scale-out logic rather than her exit timing** — her documented behavior is to take profits too early on exactly this instrument class, and mirroring her exit would have forfeited the OPEN position's subsequent multi-hundred-percent run.
3. Because the account's largest disclosed loss (ASTS calls, 2026-08) is dollar-unquantified, Artemis should **independently mark-to-market any ASTS options exposure sourced from this feed** rather than relying on her eventual "loss porn" retrospective (promised but undelivered as of archive close) to establish the real magnitude.
4. Re-verify this source's `COVERED_CALL_WHEEL_COMPOUNDER` classification periodically against her own future multi-account "Portfolio Review" posts (the clearest, highest-reliability checkpoint format she produces) rather than against post-level `amount_k`, which is permanently broken for this source.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone | Notes |
|---|---|---|
| 2024-11-15 | Archive begins — "Just a quick hello" | First post; establishes the "$10 million" aspirational goal and the Wendy's joke that gets called back 94 mentions later via $WEN |
| 2024-11-19 to 2024-11-20 | First covered call ($SOUN); "My starting gate" — ~$11K seed disclosed | Horse/farm/"pony" metaphor system crystallizes immediately and never changes for the rest of the archive |
| 2024-12-30 (approx.) | First disclosed IRA max-contribution ($7K, 2024) | Establishes the "trading port is locked, IRA gets fresh contributions" separation used throughout §1's capital reconciliation |
| 2025-01-27 | BloFin leveraged-crypto/copy-trading experiment opened, then self-diagnosed as "maxed out gambling," switched to paper-trading | Rare self-corrected bad-habit episode; never resumed at scale |
| **2025-02-24 → 2025-03-14** | **First and only clearly quantified drawdown: $31.63K → $22.85K (−27.7%)** | Recovered within ~6 weeks without capitulation selling |
| **2025-04-02 → 2025-04-07** | **"Liberation Day" tariff shock — calm, hedged response** | Buys puts in both IRA and taxable accounts; explicit "no intention to sell out of my shares" stance during a genuine broad drawdown |
| 2025-06-11 | $OKLO gain publicly credited to peer `Finkle` | First of several explicit peer-credit-tag posts |
| **2025-06-30** | **`$45.69K` — final verified `amount_k` reading; Robinhood portfolio sync removed and reattached same day, never recovers** | The critical data-provenance inflection point for the entire archive (§0) |
| **2025-07-03 → 2025-07-08** | **$OPEN LEAP (sourced from `Sir Jack`) bought, then closed for only +10% profit** | Five days before Opendoor's 2025 meme-stock run — the clearest "sold too early" case in the archive |
| 2025-07-24 | $SNES gain publicly credited to `@dick` | Cross-references the separate `@dick` dossier in this pipeline; establishes the recurring "AH husband" bit between the two accounts |
| 2025-09-27 | $HOOD "40% profit" credited to peer `freeballer` | Continues the credit-tag pattern into the post-sync-breakage era |
| 2025-09-29 | First post-breakage combined-account disclosure: **$52.44K** | Manual reconstruction of the capital trajectory begins |
| 2025-11-03 | Combined account value: **$62.54K** | |
| 2026-01-08 | NVDA put, "77% profit," credited to `MASTERGROOVE` | |
| 2026-02-16 → 2026-03-09 | Investing-account value dips to $59.02K then recovers to $61.10K | Minor chop, no drawdown language or panic |
| 2026-03-17 | Combined account value: **$78.81K** (Investing $60.31K + IRA $17.00K + Pineapple $1.50K) | First fully-itemized multi-account snapshot post-breakage |
| 2026-Q2 | View counts explode 10–200× (avg. views 2.6 → 946/post) as a YouTube channel and Spotify podcast launch | Explicitly declines Discord and paid subscriptions throughout — a different monetization posture than the Substack-funnel pattern documented elsewhere in this pipeline |
| **2026-08-26/28** | **Full audited "Portfolio Review": Combined Account Value $94,991.49** (Investing $74,669.42, IRA $18,155.03, Pineapple $2,167.04) | Most detailed capital disclosure in the archive; establishes the endpoint of §1's trajectory |
| **2026-08-30** | **"Say My Name: P&L week and month" — first explicit admission of "a very big loss on ASTS calls," self-blamed ("I should have sold earlier")** | Promises (undelivered as of archive close) a future "loss porn" podcast on her eight biggest losses |
| 2026-09-09 | Reaches 1,000 shares $SOFI — a long-stated allocation target ("25% of the portfolio... always my goal") | |
| 2026-09-10 | Archive ends — ordinary in-process trade notes ($PBR trim, $HPE cash-secured-put plan) | No indication of retirement, blow-up, or account closure; the account is live and active as of the last available post |

---

*End of dossier. Source data: `/home/mpha/artemis/afterhour/reports/posts/@883Ismygovtname_lifetime.md`, `/home/mpha/artemis/afterhour/data/following/@883Ismygovtname_all_posts.json`.*
