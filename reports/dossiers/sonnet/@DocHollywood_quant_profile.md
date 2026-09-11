# Forensic Quant Autopsy: @DocHollywood

**Subject:** AfterHour trader `@DocHollywood` (`prf_fff16302673f42b2bb22c598947aaac0`)
**Rank:** #10 most-active followed trader — 1,186 lifetime posts
**Coverage:** 2024-04-23 → 2026-09-10 (869 days / ~124.1 weeks, still active as of report date)
**Sources:** `@DocHollywood_lifetime.md` (full text, 1,186 posts), `@DocHollywood_all_posts.json` (structured metadata: `tag`, `gain_loss`, `amount_k`, `tickers`, engagement)
**Analyst:** Artemis Engine — Sonnet dossier pass

**Methodology note — read this before the numbers below:** `amount_k` is AfterHour's platform-captured snapshot (in $ thousands) of a *linked* brokerage account at post time, and it is the backbone of §1. Three caveats matter more here than in most profiles in this cohort:
1. **He runs three linked accounts, interleaved in one feed.** His own words, Post #1: *"I have my safe mostly smart money one and my risky mostly dumb money one. I also have one with meme bags."* The `amount_k` series therefore saws between a ~$1.2M–$3.5M cluster (the primary/"smart money" account, used throughout this dossier as his verified equity curve) and a ~$150K–$900K cluster (the smaller/"dumb money" day-trade sleeve, thinly tracked and effectively abandoned in the data after mid-2025).
2. **The sync feed glitches, and he flags it himself.** A single-post spike to **$20.74M** on 2025-08-09 is his own account glitching — he wrote *"after hour glitch on my portfolio. I'll pretend I got $20m lol"* in the same post. A second isolated spike to $4.29M on 2026-04-12 fully reverts within one post and is treated the same way. A sustained stretch from **2026-01-21 to 2026-03-06** shows implausible $8K–$42K readings (briefly negative: -$22.4K, -$121.4K) that he explicitly narrates as **"Portfolio sync issues getting worse"** — not real trading losses. All of the above are excluded from the drawdown/return math below; the exclusions are listed so the calculation is auditable.
3. **The feed has been fully broken since 2026-08-15** ("Portfolio sync stopped working," his words) through the end of the archive — every post since then reads `amount_k = 0.0`. His last verified balance is **$3.14M on 2026-08-04**; everything after that is unverified self-report only.

Free-text PnL claims (%, dollar figures in prose) are self-reported and unverified against a brokerage statement; treated as directionally informative, not audited.

---

## 1. Executive Profile

### Who he is
"Doc Hollywood" (username, likely a persona/movie reference — nothing in 1,186 posts confirms he is an actual physician) is a **high-net-worth, multi-account retail trader turned finfluencer**. He opened his AfterHour account in April 2024 already sitting on a **~$1.2M primary portfolio** plus a separate day-trading sleeve and a "meme bags" account — this is not a small-account growth story, it is a large-book operator narrating his process publicly. Over the archive he builds out a full media operation around the trading: the **"Doc's Investing Rx" podcast** (11 episodes, Feb–Sep 2025, guests drawn from the AfterHour community, topics spanning tariffs, "7 investing mistakes," option-selling income strategies, and the wheel strategy), a **Season 2 pivot to "Broke to Wealth"** (Sep 2025 onward, a beginner-friendly "$100 to $1,000" personal-finance series), and a paid community/website, **The Clinic** (`theinvestingclinic.com`), with a Discord, educational modules, a stated "all profits donated to charity" model (self-reported: "$17K of a $50K goal" for a school donation, Aug 2026), and a scholarship track for members who can't pay. **He is running a business on top of a trading account**, and that changes how every post in this archive should be read — some of it is alpha, a meaningful share of it is marketing.

### Trading philosophy
No single dogma — a **large-cap-core-plus-satellite-speculation** book, stated most cleanly in his own words: *"Be patient, don't gamble. Get rich quick usually ends [up] getting broke quick"* (Post, 2025-08-09). In practice this resolves into three distinct, coexisting behaviors:
- **A mega-cap/quality core** (AAPL, MSFT, META, NVDA, AMZN, GOOG) held mostly as shares or deep-ITM calls used as a leveraged stock substitute — his most consistently profitable sleeve.
- **A self-constructed, publicly tracked sector basket** — the **"DIP Index" (Doc's Investing Picks)**, launched 2026-02-19 around the AI/semiconductor-optical supply chain (MU, NVDA, TSM, MRVL, AVGO, AAPL, LITE, COHR, CLS, later swapping NFLX out for AAOI) — his single best-documented, most falsifiable source of edge (detailed in §2).
- **A chronic satellite sleeve of structurally-impaired, scandal-adjacent, or perpetual-decliner names bought and held through deterioration** — SMCI (through its 2024 accounting-fraud collapse), SAVA (through a lead scientist's federal fraud indictment), TLRY, SPCE, and a **68-post, 2+ year overweight in LCID (Lucid Motors)** that he himself flagged as too large ("I think I have too much $LCID," Nov 2024) and that a year-later retrospective confirms was down **-62% pre-split** over the trailing year. This sleeve is his largest, most consistent capital drag (quantified in §3).
- **Options used conservatively, not degenerately**: "deep ITM" call mentions (15) and "covered call" mentions (24) dwarf "0DTE" (2) — he uses options mainly as stock-substitute leverage and premium-selling income (the explicit subject of Podcast Episodes 9–10: cash-secured puts, covered calls, credit spreads, the wheel), not as a lotto vehicle. One notable self-owned exception: *"Went degen with options last few weeks... $SMCI and $NVDA just cut me dry... Focused on shares only in the big players"* (2024-09-11) — a documented, self-corrected relapse into short-dated options speculation.

### Post cadence
- **Overall average:** 1,186 posts / 124.1 weeks ≈ **9.6 posts/week** — one of the highest-volume accounts in this cohort, but volume is not the same as signal (see caveat below).
- **By year:** 2024 (Apr–Dec) ≈ **11.2 posts/week**; 2025 ≈ **10.2 posts/week**; 2026 (Jan–Sep, partial) ≈ **6.9 posts/week** — a real, sustained deceleration, sharpest in the final stretch (Jun 15, Jul 18, Aug 20, Sep 3 posts respectively) that coincides with both a stated risk-off posture ("Took a lot of risk off the table today," 2026-08-18) and the portfolio-sync outage.
- **Composition matters more than count:** only **463 of 1,186 posts (39.0%)** carry a structured ticker tag. By self-applied content tag, **906 posts (76.4%) carry no tag at all** (general commentary), **169 (14.25%) are tagged `News`** (headline relay: CPI/PPI prints, Fed speakers, earnings-of-the-day summaries), and only **8 posts (0.67%) are tagged `Dd`** (actual due-diligence writeups). **This is substantially a market-commentary and community-leadership feed, not a trade-call feed** — his highest-engagement posts (below) confirm the audience treats him that way too.

### Verified capital trajectory & drawdown history

Cleaned series = primary ("smart money") account cluster, glitch points excluded per the Methodology note above.

| Date | `amount_k` (clean) | Milestone |
|---|---|---|
| 2024-04-29 | $1.23M | Archive-verified opening balance |
| 2024-08-14 | ~$1.88M | Peak of the 2024 uptrend leg |
| 2024-12-18 | ~$2.03M–$2.08M | Year-end level (2024 return: **+65-70%** on the primary account) |
| **2025-01-07** | **$2.228M — first major peak** | Pre-tariff-crash high |
| **2025-04-07** | **$1.34M — trough** | **-39.9% drawdown**, coincides exactly with the "Liberation Day" reciprocal-tariff shock (Apr 2-9, 2025); he bought the dip aggressively via **3x-leveraged $SOXL**, then rotated into NVDA/AAPL — a full V-shaped recovery back to ~$1.6-1.7M inside three weeks |
| 2025-09-01 to 09-20 | ~$2.27M–$2.43M | 2025 high-water mark; explicitly discloses a large **realized tax bill** ("Uncle Sam gonna get a fat donation," 09-16) — evidence of genuine, taxable, realized profit-taking, not paper gains |
| 2025-10 to 2026-01 | Grinds down to ~$1.64M–$1.93M | Slow bleed, no single catalyst post identified; overlaps the DIP Index's pre-launch research period |
| 2026-02-19 | DIP Index launched | Public, falsifiable stock-picking track record begins (see §2) |
| 2026-04 to 06 | $2.2M → **$3.47M (archive peak)** | Fastest, largest verified expansion in the dataset — driven almost entirely by DIP Index names (MRVL, AAOI, COHR, CLS) |
| 2026-08-04 | **$3.14M — last verified reading** | Portfolio sync breaks 11 days later; no verified balance since |

**Net verified result (Apr 2024 → Aug 2026, clean series):** **+155% total return, ≈ +51%/yr annualized**, over 2.26 years, with one documented, real, catalyst-explained **-40% drawdown** (Jan-Apr 2025) that was actively traded through and fully recovered rather than panic-exited. This is a materially better verified equity curve than most profiles in this cohort — but it excludes the satellite bag-holding sleeve quantified below, which never shows up as a drawdown in `amount_k` because it is small relative to a multi-million-dollar book, even though the dollar amounts lost are large in absolute terms.

---

## 2. Ticker Universe & Catalysts

### Core assets (structured `tickers` field, 463 tagged posts)

| Ticker | Mentions | Role |
|---|---|---|
| $NVDA | 78 | Core mega-cap AI conviction name; also his most-cited "burned me" name in the 2024 options-relapse post |
| $AAPL | 53 | Core long-term holding, "new ATHs" posts recur through 2026 |
| $TSLA | 50 | Long-running earnings/news commentary name; both long shares and tactical puts (Apr 2025) |
| $MSFT | 41 | Core mega-cap; rotated out for NVDA during the Apr 2025 tariff dip |
| $AVGO | 39 | DIP Index anchor name |
| $META | 36 | Core mega-cap; subject of a running "value" thesis in mid-2026 ("Update on $META," Sep 2026) |
| $SPY | 32 | Benchmark for the DIP Index comparisons; occasional puts/leveraged hedges |
| $PLTR | 25 | Recurring watch/discussion name, mixed record (present in his one tagged `Loss` post) |
| $LCID | 24 (structured) / **68 (all-mentions)** | **Longest-running, largest emotional overweight in the archive** — see §1 and §3 |
| $AMZN | 22 | Core mega-cap |
| $SNOW, $VST, $NFLX | 18 each | $SNOW = documented ~$28K 2024 loss (§3); $VST = power/AI-datacenter theme; $NFLX = original DIP Index member, later swapped out |
| $MU, $GLD, $LITE | 17 / 14 / 14 | $MU/$LITE = DIP Index; $GLD = his cleanest, most consistently "Gain"-tagged macro hedge (3 of his 37 self-tagged wins) |
| $MRNA, $QQQ, $U, $BA, $GME, $SMCI, $UNH, $MRVL, $COHR | 12-13 each | $MRNA/$U/$BA/$SMCI = documented 2024 losses; $MRVL/$COHR = DIP Index's best 2026 performers |

### Options vs. equities, macro vs. technical
- **Macro-narrative-driven, not chart-pattern-driven.** Keyword frequency across the full 1,186-post archive: `tariff` (62), `inflation` (61), `fed` (36), `rate cut` (29), `cpi` (26) dwarf pure technical vocabulary. He is, functionally, a **financial-news aggregator with position color attached** — 169 posts are formally tagged `News` and relay CPI/PPI/FOMC/earnings headlines verbatim before adding a line of interpretation.
- **Catalyst hierarchy, in order of how much of his output they drive:** (1) scheduled macro prints (CPI, PPI, GDP, Fed speakers) and geopolitical headlines (tariffs, Iran/Israel, Trump policy) — his highest-engagement content; (2) mega-cap earnings prints, summarized same-day; (3) his own DIP Index rebalances and performance updates; (4) individual technical setups (support/resistance levels, breakouts) — present but a minority of total volume, mostly on LCID and NVDA.
- **Options usage is conservative and income/leverage-oriented**, not speculative-gambling: deep-ITM calls as a stock substitute, covered calls for premium (with one self-owned mistake, "Lesson: don't sell covered calls on 🚀" — capped $AAOI/$MRVL upside during the 2026 semis run), and cash-secured puts/credit spreads/the wheel taught explicitly on the podcast. Tactical directional shorts (NVDA puts May 2024, TSLA $285 puts Apr 2025, an SNDK short Jan 2026, an RCL short still open Apr 2026) appear occasionally but are small and opportunistic against an overwhelmingly long-biased book.
- **The DIP Index is his standout, differentiated catalyst-driven product**: a public, dated, benchmark-compared basket. Self-reported performance snapshots (unverified against a broker, but internally consistent and specific enough to be falsifiable): **+24% by 2026-04-13** (vs. SPY flat, QQQ +2%), **+38% by 2026-04-22** (vs. SPY +3.8%, QQQ +8.4%), **~+55% average by 2026-05-01** (vs. SPY +5.8%, QQQ +11.8%), with $MRVL (+106.7%) and $AAOI (+262.6%, after being swapped in for NFLX in March) as standout single names. This is the most concrete evidence of genuine sector-rotation skill in the archive.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags? **Both, in two visibly different books.**

**On the mega-cap core and the DIP Index: disciplined, realized, and taxed.** He explicitly discloses a large tax bill from summer 2025 gains ("Uncle Sam gonna get a fat donation") — real, realized, reportable profit. He rebalances the DIP Index on a stated rule (swapped NFLX for AAOI after a 20% bounce, per the 2026-04-13 update), takes partial profits into strength ("Added some $CVX today after selling at the highs," 2026-04-08), and openly logs his own execution mistakes on this book ("Lesson: don't sell covered calls on 🚀" after AAOI/MRVL ran through his short strikes).

**On the satellite/speculative sleeve: chronic bag-holding, quantified in his own words.** The single most important document in this archive is a self-authored transparency post, **"Portfolio L's" (2024-10-14)**, in which he voluntarily discloses dollar losses:

| Category | Names (2024 YTD, self-reported) | Disclosed loss |
|---|---|---|
| Realized/cut losses | $SMCI ~$100K, $SNOW ~$28K, $BA ~$21K, $U ~$8K, $MRNA ~$7K, $NKE ~$3K | **~$167K** |
| Fully exited at a loss | $SAVA ~$80K, $TLRY ~$103K | **~$183K** |
| Unrealized, still holding | $MRNA ~$30K, $LCID ~$49K, $SPCE ~$20K | **~$99K** |
| **Total disclosed drag** | | **~$449K in under 10 months of 2024** |

Every one of these names is a **structurally-impaired or scandal-adjacent decliner**, not a bad-timing entry on an otherwise sound company: $SMCI was mid-collapse from its 2024 accounting/auditor-resignation scandal ("$SMCI Slaughter... trying to HODL through this," 2024-08-26); $SAVA's lead scientist was federally indicted for research-grant fraud while he held the stock (2024-06-28: "F me ☠️☠️☠️"); $TLRY and $SPCE are multi-year secular decliners; and **$LCID is a 68-post, two-year overweight** he flagged as oversized in real time ("I think I have too much $LCID," Nov 2024) and confirmed, a year later, was down -62% (pre-split) over the trailing year — and he was still trading it into 2026 earnings.

### How he manages losing positions
- **On names he believes in structurally, he averages down and holds through deterioration** rather than cutting — the LCID/SMCI/SAVA pattern above.
- **He does set and raise stops on his winners** ("Raising the stop loss for my earlier call," Jan 2025) and does discuss stop-loss discipline on the podcast, but self-corrects only after a relapse into losing behavior, not proactively — the Sept 2024 "went degen with options" post is the clearest example: he names the mistake, states the fix ("focused on shares only in the big players"), and the fix holds going forward.
- **He is a vocal "don't panic sell" evangelist for others** during red days (§4) while his own book shows he does not always apply that patience selectively — he holds losers unconditionally, including scandal-driven ones, rather than distinguishing "temporary drawdown" from "broken thesis."

### Documented wins vs. blow-ups

| Category | Evidence |
|---|---|
| **Best documented wins** | DIP Index basket, +38-55%+ vs. SPY/QQQ single digits over the same Feb-May 2026 window ($AAOI +262.6%, $MRVL +106.7%); primary account +155% verified over 2.26 years with one real drawdown, fully recovered; realized, taxed summer-2025 gains (an actual tax bill, not a brag figure); V-shaped Apr 2025 tariff-crash recovery via SOXL/NVDA/AAPL rotation |
| **Worst documented blow-ups** | ~$449K in disclosed single-name losses in 2024 alone (SMCI, SAVA, TLRY, SPCE, MRNA, SNOW, BA, NKE, U) — concentrated in scandal-hit or structurally-declining names, several bought or held *through* the negative catalyst rather than ahead of or clear of it; a 2+ year, still-unresolved LCID overweight confirmed down -62% pre-split over one measured year; a self-admitted short-term relapse into "degen" options trading on SMCI/NVDA (Sep 2024) |

**Bottom line:** this is a **two-book trader** whose flagship, publicly-tracked products (mega-cap core, DIP Index) show genuine, falsifiable, benchmark-beating skill, sitting alongside an under-disclosed satellite sleeve of falling-knife catches in scandal-adjacent and structurally-declining names that has cost hundreds of thousands of dollars and has never been fully unwound. The overall `amount_k` curve looks clean because the winning sleeve is larger — that does not mean the losing sleeve's process is fixed.

---

## 4. Behavioral & Sentiment Signals

### Why is he posting?
Three motives, increasingly commercial over the archive's lifespan:
1. **Community leadership / anti-panic reassurance** — a large share of his highest-engagement posts are calm-the-room content during red days: *"DO NOT PANIC... take a walk, shut down the app... You will be ok"* (2025-02-25, 337 reactions, his highest of the archive); *"You didn't panic sell right?"*; *"Don't panic."* He explicitly positions himself as the steady hand for his followers, independent of his own book's performance that day.
2. **Monetized education** — the podcast (11 S1 episodes + an ongoing "Broke to Wealth" S2), The Clinic membership/Discord, and 39 separate mentions of Patreon. The DIP Index itself functions partly as **marketing collateral** for The Clinic ("Want to learn more? Join The Clinic... all profits are donated," 2026-05-01) — a real conflict of interest to flag: he has a commercial incentive to publicize his best-performing basket loudly and his worst-performing satellite names not at all (only one, in 1,186 posts, is self-tagged `Loss`; see below).
3. **Macro/news curation for the community** — 169 `News`-tagged posts and heavy CPI/PPI/Fed/tariff/geopolitical (Iran/Israel/Trump policy) commentary; several of his highest-engagement posts are pure geopolitical analysis, not trade calls (e.g., a ~251-comment "Pre-emptive strike" post, a 198-comment Iran "open letter" breakdown).

### Recurring linguistic patterns
- **Self-tagging is heavily curated: 37 `Gain`-tagged posts vs. just 1 `Loss`-tagged post in 1,186 (a 37:1 ratio)**, despite ~$449K in self-disclosed dollar losses documented in a single 2024 post and a real, catalyst-driven -40% account drawdown in early 2025. **His own tag field is not a reliable signal of his actual win rate — treat it as marketing, not data** (this is the single most important behavioral finding for how Artemis should weight his self-reported wins).
- **Medical/culinary metaphor family, consistently applied to winners**: "cooking" / "keep cooking 🧑🍳🔥" (DIP Index updates), "prescriptions" / "the Clinic has the prescriptions" — persona-consistent branding language, never applied to losers.
- **Self-deprecating accountability on wrong meme calls**: a running "one year later" retrospective format (Dec 2025, Dec 2024) that grades his own prior year-end meme-stock polls with poop emojis for the losers (GME -31%, MSTR -47%, LCID -62%, RXRX -44%) alongside the winners (ASTS +241%) — genuine, public accountability that partially offsets the self-tagging bias above, though it is annual and retrospective rather than real-time.
- **Humor as a pressure valve, not bravado**: running gags (Pokémon cards as a joke "cash out" plan, "Save me space in your bunker Zuck boy," "the higher you climb, the farther you fall...") — lighter in tone than the profanity-and-distress register common elsewhere in this cohort; consistent with a trader whose absolute dollar base means individual red days are less existential.

### Reaction to market volatility / red days
- **Calm, prescriptive, other-directed.** His signature red-day post type is a reassurance post aimed at his followers, not a confession about his own position — "DO NOT PANIC," "you didn't panic sell right?," explicit instructions to move out of options/leveraged ETFs into shares during drawdowns.
- **Opportunistic on macro shocks.** The Apr 2025 tariff crash produced not a retreat but an aggressive, leveraged buy (3x $SOXL) — he treats broad-market fear as a buying signal on his core book, consistent with his stated philosophy.
- **Notably absent: real-time distress language on his own satellite losses.** The SMCI/SAVA/TLRY losses are disclosed in a single retrospective transparency post (2024-10-14), not narrated as they happened in near-real-time the way his gains are — a pattern consistent with the self-tagging bias above.

### Engagement profile
Average **24.6 comments / 28.4 reactions** per post (well above typical for this cohort). His single highest-engagement moments are **not his own trade calls** — a `Contest`-tagged NVDA price-guessing game (383 comments, his highest), a panic-management post (337 reactions), and tariff/geopolitical explainers (200-250 comments each). His audience engages with him as a **community anchor and news translator** more than as a signal source.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

**Primary:** `MACRO_NARRATIVE_MEGACAP_CORE` — a large-cap/mega-cap-plus-thematic-basket core (AAPL/MSFT/META/NVDA/AMZN plus the AI-semiconductor "DIP Index"), position-managed around scheduled macro catalysts (CPI, PPI, Fed, tariffs) rather than chart patterns, held mostly as shares or deep-ITM calls. This is the sleeve producing his verified +155% / 2.26yr account growth.

**Secondary:** `SCANDAL_ADJACENT_BAGHOLDER` — a chronic pattern of buying and holding through negative structural catalysts (accounting fraud, research-fraud indictments, secular decline) in a recurring cast of names (SMCI, SAVA, TLRY, SPCE, LCID), never fully unwound, and self-disclosed at ~$449K in losses for 2024 alone in a single transparency post.

**Tertiary (positive, differentiated):** `SECTOR_ROTATION_BASKET_BUILDER` — the DIP Index is a genuinely rare artifact in this cohort: a dated, public, benchmark-compared, rules-based (documented swap-out logic) equity basket with a real, specific, falsifiable track record (+38-55%+ vs. single-digit SPY/QQQ over the same window).

**Watch tag:** `FINFLUENCER_COMMERCIAL_BIAS` — a paid community (The Clinic), a podcast, and a Patreon sit behind his posting; his self-tagged Gain:Loss ratio (37:1) is far more skewed than his account's actual documented history, meaning **what he chooses to publicize is shaped by what sells a membership**, not only by what happened in his book.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 61 / 100**

Rationale:
- **+ (verified, multi-year, catalyst-survived account growth, ~28 pts):** +155% total return / ~+51% annualized over 2.26 years on a >$1M starting base, with one real, macro-explained -40% drawdown that was actively traded through (leveraged-ETF dip-buy) and fully recovered within weeks, not panic-exited.
- **+ (genuine, falsifiable, differentiated sector-rotation skill, ~20 pts):** the DIP Index is dated, public, benchmark-compared, and rules-based (documented swap logic) — a rare, concrete edge in this cohort, not just a self-reported brag figure.
- **+ (realized, taxed profit-taking, ~8 pts):** explicitly discloses a large tax bill from realized 2025 gains — evidence against a pure paper-gains narrative.
- **− (large, disclosed, unresolved dollar losses in scandal/decline names, ~25 pts):** ~$449K in self-reported 2024 losses concentrated in SMCI/SAVA/TLRY/SPCE/LCID, several bought or held through the negative catalyst itself; a two-year LCID overweight confirmed down -62% and still open.
- **− (severe self-report/tagging bias, ~10 pts):** a 37:1 self-tagged Gain:Loss ratio despite the above — his platform-visible "win" signal is not trustworthy on its own and requires the `amount_k` series or explicit prose disclosures to correct for it.
- **− (signal density, ~2 pts):** only 39% of posts carry a ticker, only 0.67% are formal DD writeups — high volume, comparatively low actionable-signal density per post.

**Expectancy: Positive on the primary/core book (verified), materially eroded but not reversed by a persistent negative-expectancy satellite sleeve.** The `amount_k` series proves the net outcome is a strong, real compounding curve; the "Portfolio L's" disclosure proves that outcome is despite, not because of, a recurring falling-knife-catching habit in structurally broken names. Filtered to the DIP Index and mega-cap core alone, expectancy is clearly and demonstrably positive and worth harvesting; filtered to his scandal-adjacent/secular-decliner picks, expectancy is clearly negative.

### 5.3 Signal Flow Ingestion Matrix

| Post Signature | Underlying Signal Type | Reliability | Artemis Action |
|---|---|---|---|
| DIP Index rebalance / performance updates | Rules-based sector-rotation basket (AI-semiconductor/optical supply chain) | High (dated, public, benchmark-compared, internally consistent) | **INGEST** as a tracked thematic-basket overlay; verify current constituents against his live post before acting |
| Mega-cap core commentary (AAPL/MSFT/META/NVDA/AMZN) | Long-term conviction, share/deep-ITM-call positioning | Moderate-High (matches his best-performing, longest-held sleeve) | **INGEST** as a sentiment/conviction data point on names the Engine already covers |
| Macro/news relay posts (CPI, PPI, Fed, tariff, geopolitical) | Headline curation, minimal proprietary analysis | Low-Moderate for alpha; useful for retail-sentiment timing | **LOG for sentiment/timing context only** — not a standalone trade trigger |
| "Portfolio L's"-style transparency/loss disclosures | Rare, high-value ground truth on satellite-book behavior | High when it appears (self-disclosed, specific dollar figures) — but **very rare** (1 such post in 1,186) | **INGEST immediately when it recurs** — this post type is the single best corrective to his tag-bias problem |
| New satellite/single-name conviction posts on scandal-adjacent or secularly-declining names (pattern names: SMCI, SAVA, TLRY, SPCE, LCID-style profiles) | Falling-knife catch, no distinguishing "temporary dip" from "broken thesis" | Low — confirmed, repeated, large-dollar negative-expectancy pattern | **FADE / DO NOT COPY** — treat fresh conviction on a structurally-impaired name from this account as a contrarian tell |
| Self-tagged `Gain` posts | Marketing-curated highlight reel | Low as a standalone win-rate signal (37:1 self-tag bias vs. documented reality) | **DO NOT weight his `tag=Gain` field as ground truth**; cross-check against `amount_k` trend instead |
| Contest/Poll posts (price-guess games, year-end meme picks) | Community engagement, not a trade signal | N/A for trading | **IGNORE for signal**; usable only as a retail-crowd-attention data point |
| Podcast/Clinic/Patreon promotional posts | Commercial marketing | N/A for trading | **IGNORE for trading**; log as evidence of ongoing commercial incentive bias in his other posts |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Track the **DIP Index basket live** (currently: MU, NVDA, TSM, MRVL, AVGO, AAPL, LITE, COHR, CLS, AAOI as of the May 2026 update) as a standing thematic-rotation signal — this is his most credible, most differentiated, most falsifiable edge, and it is public and dated by design.
2. Weight his **mega-cap conviction commentary (AAPL/MSFT/META/NVDA/AMZN)** as a moderate-confidence sentiment overlay, particularly around his stated entry/exit rotations (e.g., swapping MSFT for NVDA during the Apr 2025 dip).
3. Whenever a rare, specific, self-disclosed **loss/transparency post** appears (the "Portfolio L's" format), ingest it at high priority — it is the single most reliable corrective data point his feed produces.

**Contrarian Fade Directives (when to fade him / the retail herd):**
1. **Fade fresh conviction posts on structurally-impaired or scandal-adjacent names** — his own 2024 disclosure shows this exact pattern (SMCI, SAVA, TLRY, SPCE) cost ~$449K, and the LCID position remains open and still down double digits two years in. A new "I'm buying the dip" post on a name already under a fraud, accounting, or secular-decline cloud should be read as a contrarian signal, not a follow signal.
2. **Discount his self-applied `Gain` tag** — with a 37:1 self-tagged Gain:Loss ratio against a documented reality of large, real losses, his tagging behavior is closer to marketing curation than performance reporting.
3. **Treat his reassurance-during-panic posts ("DO NOT PANIC") as a crowd-sentiment indicator, not a trading signal** — useful for gauging retail fear level among his followers, not for timing the Engine's own entries/exits.

**Mandatory Risk Blacklists & Firewalls:**
1. **Firewall any signal sourced from this account on a name carrying an active fraud, accounting-restatement, or research-misconduct headline** — his own history (SMCI, SAVA) shows he will hold and even add through exactly this catalyst rather than exit.
2. **Never size a position off his self-reported percentage performance claims** (DIP Index returns, podcast trade recaps) without independent price verification — these are directionally useful but come from an account with a commercial incentive to overstate.
3. **Do not treat a gap or absence in his posting as a market-calm signal** — his 2026 cadence decline correlates with a stated deliberate risk reduction ("Took a lot of risk off the table today") and a broken portfolio-sync feed, not with reduced market volatility; the two should not be conflated.
4. **Do not rely on `amount_k` readings during his self-acknowledged sync-outage windows** (2025-08-09 isolated spike; 2026-01-21 to 2026-03-06 sustained corruption, including negative readings; 2026-08-15 onward total outage) — any Engine process consuming this feed programmatically needs an outlier/outage filter matching the exclusions documented in this dossier's Methodology note.

**Exit Rules & Alpha Rectification:**
1. Any idea sourced from his **DIP Index** should still carry the Engine's own independent stop-loss and rebalance rules, not his — he has a documented history of letting a covered-call cap his upside on a running winner ("Lesson: don't sell covered calls on 🚀," AAOI/MRVL, Apr 2026), meaning even his best sleeve has an exit-discipline gap worth correcting for.
2. Apply a **hard "scandal/decline-catalyst" filter** to any idea attributed to this account: if the underlying name has an active fraud, restatement, or multi-year-secular-decline flag, do not ingest regardless of his stated conviction — this single filter would have avoided the majority of his ~$449K disclosed 2024 losses.
3. Re-score this profile positively if he ever publishes a second "Portfolio L's"-style transparency post with an updated satellite-sleeve tally — a recurring, not one-off, loss disclosure would meaningfully upgrade confidence in using his self-reported figures directly.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone / Catalyst | Notes |
|---|---|---|
| 2024-04-23 | First archive post ("Long time lurker...") | Discloses the three-account structure (safe/smart-money, risky/dumb-money, meme bags) that shapes the entire `amount_k` series |
| 2024-04-29 | First verified `amount_k` reading: **$1.23M** | Establishes the primary account's starting point |
| 2024-06-28 | $SAVA lead scientist charged with federal grant fraud | "F me ☠️☠️☠️" — held the position through the news |
| 2024-08-26 | "$SMCI Slaughter" — holding through the accounting-scandal crash | "Trying to HODL through this" |
| 2024-09-11 | Self-admitted "degen" options relapse on SMCI/NVDA | States the fix ("shares only, big players") and holds to it going forward |
| **2024-10-14** | **"Portfolio L's" — voluntary full loss disclosure** | ~$449K in 2024 YTD losses across SMCI/SNOW/BA/U/MRNA/NKE/SAVA/TLRY/SPCE/LCID — the single most important document in the archive |
| 2024-11-04 | "I think I have too much $LCID" | Self-flagged concentration risk, never meaningfully reduced |
| 2024-12-18/19 | `amount_k` sync glitch (excluded from clean series) | Same-day round-trip, not real |
| **2025-01-07** | **Verified peak: $2.228M** | Pre-tariff-crash high |
| 2025-02-24 | "Doc's Investing Rx" podcast launches | Begins the media/monetization build-out that runs through the rest of the archive |
| 2025-02-25 | "DO NOT PANIC" — highest-engagement post of the archive (337 reactions) | Establishes his community-anchor role |
| **2025-04-02 to 04-09** | "Liberation Day" reciprocal-tariff shock | Real macro catalyst; drives the account's largest verified drawdown |
| **2025-04-07** | **Verified trough: $1.34M (-39.9% from Jan peak)** | Responds by loading 3x-leveraged $SOXL and rotating MSFT→NVDA/AAPL |
| 2025-04-25 to 05 | Recovery to ~$1.6-1.7M | V-shaped, inside three weeks of the trough |
| 2025-08-09 | `amount_k` sync glitch: **$20.74M** (excluded) | Self-flagged in the same post: "I'll pretend I got $20m lol" |
| 2025-09-16 | Discloses a large **realized tax bill** from summer gains | Confirms real, realized, taxable profit — not a paper-gains narrative |
| 2025-09 | "Doc's Investing Rx" pivots to Season 2, "Broke to Wealth" | Shift toward beginner personal-finance content; deepens the commercial/education angle |
| **2026-01-21 to 03-06** | Sustained portfolio-sync corruption (readings $8K-$42K, briefly negative) | Self-disclosed as a platform bug, not real trading losses |
| **2026-02-19** | **DIP Index (Doc's Investing Picks) launched** | His most credible, differentiated, publicly-tracked source of alpha begins here |
| 2026-03-24 | DIP Index swaps NFLX for AAOI | Documented, rules-based rebalance |
| 2026-04-08 to 05-01 | DIP Index compounds from +6.5% to **+55% average** vs. SPY/QQQ single digits | AAOI (+262.6%) and MRVL (+106.7%) are the standout names |
| 2026-04-12 | `amount_k` sync glitch: **$4.29M** (excluded) | Reverts to ~$2.5M the next post |
| 2026-04-20 | "Lesson: don't sell covered calls on 🚀" | Self-owned exit-discipline mistake on his best-performing sleeve |
| **2026-06** | **Verified archive peak: $3.47M** | Fastest expansion in the dataset, DIP-Index-driven |
| 2026-08-15 | **"Portfolio sync stopped working"** | Discloses The Clinic's charity progress ($17K of $50K goal) in the same post; `amount_k` reads $0.0 from here to the end of the archive |
| 2026-08-18 | "Took a lot of risk off the table today" | Explicit, stated de-risking ahead of continued macro/geopolitical volatility (oil, Iran/Israel) |
| 2026-09-09/10 | Final posts of the archive: META update, PPI print commentary | Still active, macro-commentary cadence intact; capital state unverified since 08-04 |

---

*End of dossier. Prepared from `@DocHollywood_lifetime.md` (1,186 posts, full text) and `@DocHollywood_all_posts.json` (structured metadata) with no external data sources.*
