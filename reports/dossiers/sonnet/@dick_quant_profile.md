# QUANT FORENSIC DOSSIER: @dick
### AfterHour Followed-Trader Autopsy — Artemis Engine Ingestion Report

| Field | Value |
|---|---|
| Handle | `@dick` ("Dick Capital LLC" / "Mr. Dick" / "Lord Dick") |
| Profile ID | `prf_5855459672424abf9ad7c8eda9e4b5c0` |
| Lifetime Posts Analyzed | 175 |
| Coverage Window | 2024-08-01 → 2026-08-23 (107.4 weeks) |
| Source Files | `@dick_lifetime.md` (qualitative, full post text), `@dick_all_posts.json` (structured: `amount_k`, `tag`, `gain_loss`, `tickers`, `reaction_count`, `comment_count`, `view_count`) |
| Analyst | Sonnet 5, Artemis Quant Desk |
| Verdict (one line) | A genuinely early, thematic microcap/small-cap idea-generator (NBIS, RCAT, GRRR, SPCB, TEM, POET all timestamped well ahead of consensus) who packages real thesis-sourcing skill inside a slur-laden self-promotion persona, reports only cherry-picked at-peak returns with zero verified P&L or disclosed losses, and has fully monetized the feed into a $1/day Substack funnel — high value as a **thematic/universe-discovery** signal, near-zero value as a **risk-management or execution** template, and carrying **real compliance/brand-safety liability** in its raw form. |

---

## 0. Data Provenance Note (read before trusting any number below)

Unlike other AfterHour dossiers in this pipeline, **@dick's `amount_k` field cannot be used as a capital trajectory.** It is populated on only 66/175 posts (38%), the values (0.10–0.14, then 0.45–0.69, then 7.8–10.5) never once match a dollar figure he states in the same post's body text (he separately discloses "$100k goal," "20,000 RCAT shares," "$82.5k into a 5-cent stock," "over $1 million in $SPCB alone"), and there is not a single portfolio-screenshot post anywhere in the 175-post archive. Whatever `amount_k` is measuring here, it is not a self-reported account balance — treat it as **non-interpretable metadata noise**, not signal.

This absence is itself the headline data point for §3: in two years and 175 posts, **@dick has never once posted a brokerage screenshot, a P&L statement, or a dollar-verified account balance.** Every performance claim in this dossier is a *price-return-since-mention* claim (self-calculated, self-reported, and — per his own "Year in Review" posts — always reported "at peak," i.e., the best possible price the stock ever traded after he mentioned it, not his actual entry, exit, or size). This dossier treats his numbers accordingly: as **evidence of idea quality**, never as **evidence of realized personal P&L**.

**Content warning:** the raw archive contains recurring ethnic/racial and sexist stereotyping used as a running "bit" to structure his stock coverage (see §4). This dossier discusses that pattern only insofar as it bears on signal reliability and ingestion risk; direct quotation is minimized below and confined to what is necessary to substantiate the finding.

---

## 1. Executive Profile

**Trading philosophy (stated vs. revealed):** He brands himself, repeatedly and explicitly, as a **"long-only, fundamentals-based investor"** with an **18-month minimum holding period** ("Long-only, hold for 18 months minimum FTW," Post #80; "there is no Discord, Dick Cap is a long-only fundamentals based investor. There is no paid service, nor will there ever be," Post #53, 2025-01-07). Both halves of that promise are broken inside the sample:
- **"18-month hold" is real for his top convictions** (NBIS held from 2024-11-22 through the end of the archive, +1,015% unrealized per his own Post #170; SPCB held 2024-08-12 → 2026, through a round-trip from $3 to $43 back to $6 and up again) but is routinely abandoned for a fast-growing side-book of **short-dated single-name options** ("slapped" BBWI 20c, LDI 2c/5c, BITF 2c/5c) that he swings for 28–197% gains in days-to-weeks — a completely different risk profile than the branding admits.
- **"No paid service, nor will there ever be"** flips within 8 months: Dick Capital Substack launches 2025-09-27 (Post #99) at "a dolla a day," and from that date forward **59 of the remaining 77 posts (77%)** exist primarily to drive Substack subscriptions, with the free AfterHour feed increasingly repurposed as a paywall-teaser channel ("removing the paywall off this article," "kindly subscribe for unlimited, unprecedented alpha" appears dozens of times).

His genuine, demonstrated edge is **thematic pattern recognition ahead of consensus**: he is on record naming defense-drone plays (RCAT, Aug 2024, months before the SRR army contract), AI-neocloud infrastructure (NBIS, Nov 22 2024 — publicly timestamped weeks before Nvidia/Accel's participation and Citron's bullish note pushed it into the mainstream, Post #41), the Trump-election GSE trade (FNMA, Nov 6 2024, night of the election), a detention/deportation-policy basket (TH, Jan 2025), an advanced-packaging/power-semiconductor sector call (Jan/Feb 2026, 10 and 14 names respectively, both baskets independently up 60–120% within months per his own recap in Post #168), and a 2026 gold/copper-miner rotation (ATEX, Faraday, VMET) — a wide, credible, and *early* thematic net.

**Post cadence:** 175 posts / 107.4 weeks = **1.63 posts/week lifetime average**, but this masks a structural break: a manic-hype phase, a genuine break/quiet-research phase, and a monetized-content phase.

| Phase | Posts | Span | Posts/wk | Character |
|---|---|---|---|---|
| 2024-Q3 (AH launch, "RCAT RCAT RCAT" era) | 19 | 8.7 wk | 2.2 | Copy-paste ticker spam, all-caps hype, near-zero fundamentals |
| 2024-Q4 (Year 1 hot streak) | 30 | 13 wk | 2.3 | GRRR/NBIS/FNMA all initiated; "Told U" catchphrase and "Dick Capital LLC" branding crystallize |
| 2025-Q1 (DICKINDEX™️ era) | 21 | 13 wk | 1.6 | Peak engagement (avg 78 comments/post); SPCB becomes a near-single-stock obsession |
| 2025-Q2–Q3 | 31 | 26 wk | 1.2 | **Cadence craters** — a 6-week silent gap (Feb 25 → Apr 24 2025) then another near-3-month gap (Jul 18 → Aug 6); only re-emerges to launch LDI, JCAP |
| 2025-Q4 → Substack launch (Sep 27) | 13 | 13 wk | 1.0 | Pivot post; monetization begins |
| 2026-Q1–Q2 (content-funnel era) | 60 | 26 wk | 2.3 | Cadence *recovers* but composition flips — options-swing disclosures (BBWI, BTQ, UAMY) and "subscribe" CTAs dominate; view counts jump 10–30x (Substack referral traffic) while AH-native comments/reactions per post fall by ~60% vs. the free era |
| 2026-Q3 (archive tail) | 7 | 13 wk | 0.5 | Cadence fades again post-monetization peak |

**Engagement arc corroborates the phase model**: avg reactions/post rise from 7.5 (2024-Q3) to a peak of 109.8 (2025-Q3), then *decline* through 2026 (36.9 → 24.0 → 23.6) even as avg views *explode* (22 → 136 → 2,603 → 2,554) — the account has scaled reach (via Substack cross-promotion, orange-checkmark verification, X account launch in Post #166) while native AfterHour community engagement per post has fallen by more than half. This is the fingerprint of a personal trading-Discord-style feed **converting into a media/newsletter business**, not of a trader's engagement growing with their track record.

**Active timeline:** First post 2024-08-01 ($RCAT). Two multi-week silences (2025-02-25 → 2025-04-24, ~8 weeks; 2025-07-18 → 2025-08-06, ~3 weeks) that he attributes to "months of intensive research" (Post #47) — plausible given the quality of what follows each gap (CFLT, LDI, JCAP are all substantive, well-sourced write-ups), but also consistent with the pattern of a part-time content creator batching output. Archive is current through 2026-08-23 with no indication of retirement or blow-up; last post is a still-active gold/miners thesis.

**Verified capital trajectory / drawdown history:** **Cannot be established.** No screenshots, no consistent self-reported balance, and the one structured field that might carry this (`amount_k`) does not reconcile with anything in the text (§0). What *can* be reconstructed from text-only self-disclosure: he mentions "$100k goal" on RCAT (Aug 2024), "$82.5k" into an unnamed 5-cent stock (May 2025), "over $1 million in $SPCB alone... on AH alone" (Feb 2025, implying multiple accounts/followers, not necessarily his own capital), and by June 2026 describes "holding 30+ stocks at any given time" in a portfolio "up 55% YTD" (Post #133) and later "+133% YTD" (Post #170) — but these YTD figures are **also unaudited, self-reported, and never reconciled against a starting balance.** Treat the entire capital narrative as **unverifiable and likely favorably-selected.**

---

## 2. Ticker Universe & Catalysts

**Core, sustained convictions (mentioned across the widest date spans — his real "book," not one-off content):**

| Ticker | First mention | Span held (per posts) | Peak self-reported return | Character |
|---|---|---|---|---|
| $NBIS (Nebius) | 2024-11-22 | 2024-11-22 → ongoing (2026-06) | "+1,015%" unrealized (Post #170) | Flagship pick; AI-infrastructure/neocloud thesis; genuinely early (pre-Nvidia participation, pre-Citron note) |
| $SPCB (SuperCom) | 2024-08-12 (informal) / 2024-12-30 (formal) | 2024-08 → 2026-06 | Round-tripped 3 → 43 → 6 → 9–10+ | Longest-running single-stock obsession; micro-cap ($20–40M mkt cap), IR-meeting access, "DICKINDEX™️" flagship |
| $RCAT (Red Cat) | 2024-08-01 | 2024-08-01 → 2024-11-19 (exited) | "+528% at peak"; personally "sold it in the 2s" (self-admitted early exit) | Drone-defense thesis; first pick, sets the template |
| $GRRR (Gorilla Tech) | 2024-09-20 | 2024-09-20 → 2024-09-30 (exited) | "+567% at peak" | Sold in full within 10 days of initiation — largest gap between "at peak" boast and actual holding period in the archive |
| $TEM (Tempus AI) | 2025-01-03 | 2025-01 → ongoing | "+100%," later "+263%"-class updates | AI/healthcare-diagnostics theme |
| $LDI (loanDepot) | 2025-07-18 | 2025-07 → 2026-06 | Peaked "+150%+", later "slightly in the red" (Post #170) | Rate-cycle call option; the one position explicitly disclosed round-tripping from big green to red without an exit |
| $POET (POET Technologies) | 2025-06-25 | 2025-06 → 2026-04 | "+263% ... 10 months later" | Optical-interconnect/photonics theme; explicit "it pays to wait" patience narrative |
| $FNMA | 2024-11-06 (election night) | 2024-11 → 2025-05+ | "+270–300%" | Pure political-catalyst trade (Trump GSE-privatization thesis) |

**Instrument mix:** Overwhelmingly **long common equity** in micro/small/mid-cap names (sub-$1B market cap dominates: SPCB, GRRR, DEFT, KRKNF, FTEK, SNES, TGEN, SKYT, IPWR, AMPG, BTQ, UAMY), with a **growing short-dated options overlay from mid-2025 onward** — LDI 2c/5c calls, BBWI 20c calls (sold in tranches for +28% then +140%), BITF 2c/5c calls. No puts, no shorts, no hedges are ever disclosed anywhere in the archive — this is a **purely long, purely bullish** book across 175 posts and roughly 55 unique named tickers (49 captured in post metadata, dozens more named only in free-text portfolio-update posts from 2026 onward that lack ticker tags in the structured data).

**Macro vs. technical vs. catalyst-driven:** His stated process (Post #47, Year-in-Review) is explicitly **fundamentals-first**: "reviewing financials, listening to podcasts, capturing any and all info on every corner of the internet... critically reviewing leadership teams, and actually going out and getting the word on the street." This is corroborated by the write-ups themselves — the SPCB thesis tracks state-by-state government-contract wins with linked press releases over 18 months; the ADEA thesis (Post #164) is a genuine, patent-and-hybrid-bonding-literate semiconductor-supply-chain argument; the FOA thesis (Post #45) models a specific floating-rate reverse-mortgage spread. **What drives entries, in order of frequency:**
1. **Underfollowed micro/small-cap names with a specific, checkable near-term catalyst** (a government contract, an activist/insider stake, a management turnaround, a patent moat) — the dominant and highest-quality pattern.
2. **Macro/political catalysts** — Trump-election trades (FNMA, TH, ANF/retail-reopening), tariff/reshoring narratives (US Steel/$X, rare earths/UAMY), Fed-rate-cycle bets (LDI).
3. **Sector-theme baskets published as standalone research pieces** (Advanced Packaging — 10 names, Power Semiconductors — 14 names, Physical AI/Robotics — 36 names) — increasingly the dominant format post-Substack-launch; these read as genuine, labor-intensive thematic screens, not one-off tips.
4. **Copycat/rivalry dynamics** with a specific named AH peer (`@sirjack`) — several picks (GRRR vs. LPSN "penny stonk battle," CFLT, U) are explicitly framed as a personal one-upmanship contest rather than pure conviction, which is a useful tell that a subset of his picks are **content/rivalry-driven, not thesis-driven**.

---

## 3. Risk Management & PnL Reality

**Does he take profits, or hold bags? Both — and the pattern is legible once you separate "flagship long-term convictions" from "tactical swings."**

- **Tactical swing book (2025-12 onward): disciplined, profit-taking behavior is real and documented.** BBWI calls sold in two tranches for +28% then +140% (Posts #112, #120); RDW swung twice for +69% and then +104% on a re-entry (Post #157/#170); KEEL trimmed 40% for +197%, balance let ride (Post #162); AAOI and CRDO swings closed for +30–42% and +30% respectively (Post #108, #170); SKYT sold in full for +90% (Post #127); AMPG trimmed one-third for "nearly 150%" after averaging down through a ~50% drawdown (Post #170). This is a real, repeatable **scale-out** pattern on the swing side.
- **Flagship-conviction book: bag-holding is the norm, framed as conviction.** NBIS, SPCB, TEM, LDI, POET are all held through their full round-trips (up and back down) with no disclosed trims at highs. **LDI is the clearest documented case**: "We were up more than 150% on the stock at one point and are now slightly in the red" (Post #170, 2026-06-28) — a full, admitted round-trip on a top-3 flagship pick, with the position still held, not cut. BTQ is admitted to have been "down roughly 50% at one point" before recovering (Post #170) — again, held through the drawdown rather than stopped out.
- **He has explicitly, retrospectively regretted selling winners too early** — a self-admitted structural leak on the upside, not the downside: RCAT "sold it in the 2s" near the start of its run (Post #20); GRRR sold in full 10 days after initiation, before its "+567% at peak" was even reached (Post #19); TSSI "sold TSSI way too early... had 10k shares at 2" (Post #82). **His single biggest disclosed process error is cutting winners too soon, not riding losers too long** — the inverse of the classic retail failure mode, and worth noting precisely because it's unusual.

**Documented wins vs. blow-ups:**
- **Zero self-tagged losses across 175 posts.** The `[Gain]` tag appears 31 times (18% of posts); no `[Loss]` tag exists anywhere in the structured data, and no post is ever titled or framed around an admitted losing trade. The only two disclosed drawdowns in the entire archive (LDI to "slightly red," BTQ to "-50% at one point") are both mentioned **only in the context of an eventual recovery**, inside a bullish "comprehensive review" post — i.e., losses are disclosed exclusively when they can be immediately reframed as a vindicated-conviction story. This is a **selectively-reported track record, not an audited one.**
- **"Year in Review" and portfolio-recap posts (the closest thing to formal performance reporting) report only "at peak" or "unrealized" returns, never a blended realized P&L.** Post #47 (2024 Year in Review): "+567%," "+528%," "+522%" *at peak* for GRRR/RCAT/APP, despite his own posts confirming he had already exited GRRR and RCAT well before those peaks. Post #104 (Oct 2025): "+130% average... +214% average... at peak" across 34 names. Post #170 (June 2026): a long list of "unrealized" gains (NBIS +1,015%, AMT.V +236%, KEEL +184%...) presented alongside realized gains (RKLB +1,415%, CIFR +130%...) with no denominator, no losers listed, and no account-level total. **A stock that goes quiet (like $TH, last mentioned 2025-02-14 at -11% and never given a formal exit post) simply disappears from later recaps** rather than being marked closed — the track record is curated by omission.
- **Never discloses position sizing, stop-loss levels, or a cost basis on the majority of positions** (UAMY's "$8.82 average" after averaging up, Post #124, is the rare exception). No disclosed stop-loss discipline exists anywhere in the archive — the operative risk control, where one exists at all, is "wait 18 months" or "average down/up on conviction," never a predefined exit.

**Net PnL reality assessment:** The idea-generation record (see §5.2) is plausibly strong and partially externally corroborable — NBIS, RCAT, GRRR, TEM, SPCB, and POET are all real, publicly-traded names whose broad multi-hundred-percent moves in the windows he claims are independently verifiable market history, not fabricated. What is **not** verifiable, and should never be assumed, is that his own realized, dollar-weighted personal PnL matches the headline percentages — his own text shows him exiting several of his best ideas (RCAT, GRRR, TSSI) well before the peaks he later cites as his track record.

---

## 4. Behavioral & Sentiment Signals

**Why is he posting?** Three motives, and they change weight over the archive's life:
1. **Establishing a public, timestamped claim to being early** ("Told U," used well over 150 times across the archive, is the single most repeated phrase in the corpus) — this is a status/reputation-building behavior, not incidental color commentary. He frequently returns to old posts months later purely to link back to the timestamp ("Told U buy $NBIS on Nov 24, 2024," Post #87, posted 8+ months after the original call, solely to re-litigate priority).
2. **Positioning himself as the alpha (in both senses) of the AfterHour community** — recurring rhetorical devices: rating himself ("Dick Capital Rating: buy buy buy"), demanding followers publicly affirm him ("comment 'All your words are alpha,'" Post #84), renaming himself mid-archive ("no tagging me as @dick anymore… I shall be referred to as Mr. Dick," Post #47; later "Lord Dick"), and open, unprompted claims to being "the best long-only stock picker on AH... and one of the best long-only stock pickers in the entire world" (Posts #77, #79). This is a persistent grandiosity pattern, not occasional bravado.
3. **From 2025-09-27 onward, direct monetization** — Substack subscription CTAs appear in 59 of the last 77 posts. The free AfterHour feed becomes structurally a **loss-leader/teaser funnel**: paywalled articles get "de-paywalled" on AH only after the move has already happened ("removing paywall off this article... stock is up 161% since," Post #145), which means the *public, free, timestamped* record is systematically biased toward showcasing wins after the fact while the real-time calls stay behind the paywall and out of this dataset's reach.

**Recurring linguistic patterns:**
- **Ethnic/racial and misogynistic framing used as a running structural device for stock coverage** — this is the dossier's most important brand-safety flag. He explicitly organizes several theses around nationality/ethnicity stereotypes as a rhetorical hook ("Jews know how to make money" for $SPCB/$U/$JCAP; a bribery stereotype for $GRRR's Indian management; a stereotype-laden framing for $VLERF's Thai ownership base; a slur used in the $TH/prison-detention thesis tied to Trump-era deportation policy, Post #58). This is not incidental profanity — it is a repeated, load-bearing organizing device across multiple, otherwise well-researched theses, and it appears consistently enough (at least 6 distinct posts across 18 months) that it must be treated as a durable feature of the account, not a one-off lapse. **Any automated ingestion of this feed's raw text must strip or firewall this content before it reaches any downstream system, report, or user-facing surface** — see §5.4.
- **"Told U" / "Fold U" / "Love U" wordplay** as the account's signature verbal tic, used both as a victory lap and, increasingly in 2026, as a subscription-funnel sign-off.
- **Self-deprecating admission of ADHD and disorganization** ("I have ADHD," Post #74; "forgot to post it," Post #88) used to explain gaps and missed posts — genuine and consistent with the archive's real cadence gaps.
- **Reaction to red/volatile days: consistently bullish-defiant, never capitulatory.** "Market Red, $RCAT green" (Post #2), "Market dying but DICKINDEX™️ booming" (Post #54), "SPY -0.8% / QQQ -1.4% / UAMY +15%" (Post #121) — the recurring move on down-tape days is to spotlight whichever single holding is bucking the tape, not to acknowledge broad exposure or de-risk. There is no example anywhere in the archive of him posting caution, reduced exposure, or a defensive rotation during a red day — the account's tone is uniformly, unconditionally bullish across two full years spanning multiple real drawdown episodes (Feb 2025 chop, early-2026 volatility).
- **Volatility is never treated as risk, only as a buying opportunity for conviction names** ("if you can take short-term pain... payoffs can be massive," Post #71 on SPCB; "stuck to our thesis and even averaged down," Post #170 on AMPG) — consistent with the "hold through drawdowns" pattern in §3, and consistent with never having disclosed a stop-loss.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

- **Primary: `THEMATIC_MULTIBAGGER_HUNTER`** — a genuine, repeatable pattern of identifying underfollowed micro/small/mid-cap names tied to a specific, checkable catalyst (government contract, activist stake, management turnaround, patent moat, macro/political event) meaningfully ahead of mainstream coverage. NBIS (Nov 2024, pre-Nvidia/Citron), RCAT (Aug 2024, pre-SRR contract), FNMA (election night 2024), and the Jan/Feb 2026 Advanced Packaging / Power Semiconductor sector baskets are the strongest, most independently-checkable instances.
- **Secondary: `SURVIVORSHIP_BIASED_CONTENT_FUNNEL`** — a self-promotional media operation (peaking in the 2025-09-27 Substack launch) that reports exclusively at-peak/unrealized returns, discloses zero explicit losses in 175 posts, quietly drops underperforming names from recaps rather than closing them out on the record, and has a direct monetary incentive ($1/day subscription, "20 spots left" urgency copy, price-lock countdown timers) to keep the public hype level maximal regardless of the underlying book's real state.
- **Behavioral risk flag (non-trading): `TOXIC_CONTENT_RISK`** — recurring ethnic/racial/sexist framing used as a coverage device (§4). Not a trading-behavior tag, but a hard gate on any raw-text ingestion, quotation, or user-facing surfacing of this source.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 51 / 100**

Justification: the score sits at the midpoint because the two halves of this trader's record pull in opposite directions with roughly equal weight. **Upside contributors:** (a) an independently-verifiable pattern of being *early* on names that later became widely-covered, multi-hundred-percent movers (NBIS, RCAT, GRRR, TEM, FNMA, POET, the Jan/Feb-2026 semiconductor-packaging baskets) — this is real information value, not luck-shaped noise, because the theses are specific, dated, and checkable against public price history; (b) a demonstrated, real profit-taking discipline on the tactical-swing side of the book (documented scale-outs at +28%, +90%, +104%, +140%, +150%, +197%) that is genuinely usable as a process template. **Downside contributors:** (a) zero verified capital or P&L — every headline number is self-reported, unaudited, and reported "at peak" rather than realized; (b) a documented pattern of exiting his own best ideas (RCAT, GRRR, TSSI) well before the returns he later cites as his track record, meaning the "at peak" boasts materially overstate what following him and holding to his own stated horizon would have realized in several of his flagship cases; (c) zero disclosed losses across 175 posts is not evidence of a clean record — combined with the LDI/BTQ drawdown admissions buried inside otherwise-bullish recap posts, it is evidence of **selective disclosure**; (d) a heavy promotional/monetization overlay from late 2025 onward that creates a standing incentive to inflate; (e) the toxic-content pattern in §4, which is a standalone reputational/compliance liability independent of trading quality.

**Expectancy:** Two distinct expectancy regimes must be scored separately:
- **Idea-sourcing expectancy (buy the ticker at time of mention, apply independent risk management): plausibly strongly positive.** The specific, dated tickers he was early on (NBIS Nov-2024, RCAT Aug-2024, FNMA Nov-2024, the two 2026 semiconductor baskets) moved the direction and rough magnitude he called, independently of his own account behavior — this is a real, harvestable universe-discovery signal.
- **Copy-the-trade expectancy (mirror his disclosed entries, sizing, and exits): unverifiable and likely inferior to the idea-sourcing expectancy**, because (a) no sizing or stop discipline is ever disclosed on the conviction book, (b) his own realized exits on several flagship names materially underperform the "at peak" numbers he later publicizes, and (c) the 2025-2026 options-swing disclosures arrive with no entry cost-basis, size, or Greeks context, making them un-replicable as stated.

### 5.3 Signal Flow Ingestion Matrix

| Signal Type | Source Posts | Raw Reliability | Recommended Artemis Treatment | Weight |
|---|---|---|---|---|
| Early-stage, catalyst-specific microcap/small-cap theses (govt. contract, activist stake, turnaround, patent moat) | ~25 initiation posts (RCAT, NBIS, GRRR, SPCB, FOA, TH, ANF, LDI, JCAP, ADEA, IPWR, AMPG) | Medium-High (specific, dated, independently checkable) | **INGEST as a universe-discovery seed** — feed the named ticker + catalyst into internal fundamental/flow screens; verify independently before sizing | 0.5 |
| Published sector/theme basket articles (Advanced Packaging 10-name, Power Semiconductors 14-name, Physical AI/Robotics 36-name) | 3 major basket posts + recap updates | Medium-High (labor-intensive, diversified, self-reported basket returns of +60-120% partially external-checkable) | **INGEST as a diversified thematic-universe scan**, weight individual names by independent screen scores rather than trusting the basket uniformly | 0.4 |
| Tactical options-swing disclosures with documented scale-outs (BBWI, RDW, KEEL, AAOI, CRDO, SKYT, AMPG) | ~12 posts, 2025-12 onward | Medium (real profit-taking behavior, but no entry cost-basis/size disclosed) | **INGEST the exit-discipline pattern only** (scale out in tranches at strength) — do not copy entries, no basis to size or time them | 0.2 |
| "At peak" / "unrealized" performance recap posts (Year-in-Review, DICKINDEX™️ updates, portfolio-update links) | ~15 posts | Low as a P&L record (selectively reported, no losses ever shown, "at peak" ≠ realized) | **DISCARD as performance evidence; retain only the underlying ticker list** for universe purposes | 0.0 (ticker list only) |
| Macro/political catalyst trades (FNMA election trade, TH deportation-policy trade, ANF retail-reopening trade) | ~5 posts | Medium (correctly timed relative to the political catalyst, though thesis-quality varies) | **INGEST directionally as a political/regulatory-catalyst hypothesis**, re-verify against the actual policy timeline independently | 0.3 |
| Self-promotional / "best trader on AH" / subscription-funnel copy | ~50+ posts, especially 2025-09-27 onward | None | **DISCARD entirely**, exclude from all scoring; treat density of this content as an inverse signal-to-noise indicator for the surrounding post | 0.0 |
| Ethnic/racial/sexist stereotyping framing used as coverage device | 6+ posts across 18 months | None; compliance/brand-safety hazard | **HARD FIREWALL** — never surface raw quotes; scrub before any downstream use; flag source posts for human review, not automated ingestion | 0.0 / blocked |
| `amount_k` structured field | 66/175 posts | None (does not reconcile with any disclosed dollar figure in text; no portfolio screenshots exist anywhere in archive) | **DISCARD** — do not use as a capital-trajectory or sizing proxy | 0.0 |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Treat every catalyst-specific microcap/small-cap initiation post as a **timestamped universe-discovery lead**: extract ticker + stated catalyst (government contract, activist stake, management change, patent/IP moat, macro-policy tailwind) and route it into Artemis's independent fundamental/flow screening stack rather than acting on the post directly.
2. Ingest his published sector-basket articles (Advanced Packaging, Power Semiconductors, Physical AI/Robotics, and any future basket-format Substack pieces surfaced via AH teaser posts) as **diversified thematic universes** — these are his highest-effort, most-verifiable content format and the closest thing in the archive to genuine, repeatable research process.
3. Log the **exit-discipline pattern from his tactical-swing book** (scale out roughly a third to half of a position into a fast +30-100%+ move, let the remainder ride) as a candidate profit-taking heuristic worth backtesting independently — it is the one piece of *process*, as opposed to *thesis*, that recurs reliably across the sample.
4. Use his rivalry-driven picks (anything explicitly framed as a response to `@sirjack` or another named AH peer) as a **lower-confidence tertiary lead only** — flag for independent verification before any weight is assigned, since the motivation is documented to be one-upmanship rather than pure conviction.

**Contrarian Fade Directives (when to fade him / the retail herd he represents):**
1. **Fade the "at peak" framing specifically** — when he or his followers cite a return figure, assume it materially overstates any realistically achievable entry/exit; his own text shows him exiting several of his best-performing ideas (RCAT, GRRR, TSSI) well before the peaks he later cites. Never size a position off an "at peak" number.
2. When a **DICKINDEX™️-style basket concentrates hard into one or two names with escalating urgency language** ("20 spots left," "last chance," countdown-timer pricing, repeated all-caps ticker spam), treat this as a **late-cycle retail-crowding tell on that specific name**, not a fresh entry signal — the promotional intensity is a function of the subscription funnel's needs, not the thesis's freshness.
3. Treat sustained, unconditionally bullish commentary through a red-tape day (no example of caution or de-risking exists anywhere in the archive) as a **sentiment-extreme retail-long tell** during genuine broad drawdowns — useful as a contrarian input to Artemis's own breadth/sentiment composites, not as a reason to add exposure alongside him.

**Mandatory Risk Blacklists & Firewalls:**
1. **Hard firewall on raw-text ingestion of ethnic/racial/sexist stereotyping content (§4).** No automated pipeline may surface, quote, paraphrase, or route this language downstream; source posts containing it should be flagged for human review only, and any thesis embedded in them (e.g., $SPCB, $TH, $VLERF, $U, $JCAP) should be re-derived from independent, neutral research before any signal value is extracted.
2. **Never treat any self-reported performance statistic (Year-in-Review, DICKINDEX™️ update, "up X% YTD," "+X% at peak") as a verified capital or P&L data point.** No portfolio screenshot, brokerage statement, or reconciled account balance exists anywhere in the 175-post archive.
3. **Discard the `amount_k` structured field entirely for this source** — it does not reconcile with any dollar amount disclosed in post text and should not be used as a sizing, capital, or drawdown proxy (contrast with other AfterHour sources where this field is a usable OCR'd screenshot value).
4. **Blacklist copying entry mechanics, size, or cost basis from the options-swing disclosures** (BBWI, LDI, BITF calls) — these posts ("slapped the ask") never include strike-relative cost basis, contract count, or position-sizing-as-percent-of-book, making them structurally un-replicable as risk-managed trades.
5. **Do not weight monetization-adjacent posts (anything containing "subscribe," "kindly," "dolla a day," "spots left," or similar funnel language) as trading signal** — flag their density as an inverse data-quality indicator for whatever ticker is mentioned alongside them.

**Exit Rules & Alpha Rectification:**
1. Any position sourced from a @dick catalyst-lead should carry a **hard, independently-derived stop-loss at initiation** — nothing in his own disclosed practice provides one, and his flagship-conviction book (NBIS, SPCB, LDI, TEM) shows a consistent pattern of holding through full round-trips rather than defending gains.
2. Apply Artemis's own trailing-stop / scale-out logic on any name sourced from this feed, informed by (but not copied from) his tactical-swing book's real scale-out pattern (~30-50% trimmed into a fast, large move, remainder trailed) — this is the one piece of his own process worth partially inheriting.
3. Because his public track record is curated by omission (names quietly disappear from recaps rather than being marked closed — see $TH), Artemis must **independently track and mark closed** any ticker sourced from this feed once its thesis window has clearly expired, rather than relying on the source ever publishing a formal exit/loss post.
4. Re-score the `THEMATIC_MULTIBAGGER_HUNTER` weighting quarterly against **independently verified** price outcomes (not his self-reported figures) for the specific tickers and dates he named — if the hit rate on independently-checked, dated calls degrades, downgrade ingestion weight toward the `SURVIVORSHIP_BIASED_CONTENT_FUNNEL` floor.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone | Notes |
|---|---|---|
| 2024-08-01 | Archive begins — $RCAT initiation | First post; establishes the drone/defense thesis and the "$100k goal" framing; template for every future initiation post |
| 2024-08-12 | $KRKNF (Kraken Robotics) and informal first mention of what becomes $SPCB-adjacent commentary begins | Early defense-supply-chain thematic net widening beyond RCAT |
| 2024-09-13 to 2024-09-20 | "Dick Capital" persona and "Told U" catchphrase crystallize; $GRRR vs. $LPSN "penny stonk battle" vs. `@sirjack` | First explicit rivalry-framed pick; GRRR sold in full within 10 days, well before its eventual "+567% at peak" |
| 2024-11-06 | $FNMA initiated on election night | Pure political-catalyst trade; later claimed "+270-300%" |
| **2024-11-22** | **$NBIS initiated at ~$21** | The single most credible, independently-checkable "early" call in the archive — weeks ahead of Nvidia/Accel private-placement participation and a bullish Citron note (both referenced in his own Post #41, Dec 4 2024) |
| 2024-12-25 | First "Dick Capital LLC Year in Review" | Establishes the "at peak" reporting convention that persists for the rest of the archive; retroactively credits himself with GRRR/RCAT/APP peaks he had already exited |
| 2024-12-30 | $SPCB formally endorsed ("let the Jews make you money") | Becomes the account's longest-running single-stock obsession and the first instance of the ethnic-stereotype coverage device flagged in §4 |
| 2025-01-10 | "DICKINDEX™️" branded basket launched (SPCB, NBIS, TEM, FOA) | First formal "index" product; escalating urgency/superiority language begins |
| 2025-01-15 | $TH (detention/deportation-policy trade) initiated | Contains the archive's most severe ethnic-slur usage as a coverage device, tied explicitly to Trump-era immigration policy |
| 2025-01-29 to 2025-03-07 | $SPCB IR outreach, CEO call arranged and recapped | Genuine micro-cap-analyst behavior (direct company access, third-party analyst brought onto the call) — one of the highest-effort pieces of process in the archive |
| **2025-02-14** | $TH marked "-11%" in a DICKINDEX™️ update | Last explicit performance figure ever given for TH; the position/thesis is never formally closed out on the record — it simply stops being mentioned (see §5.4 exit-rectification directive) |
| 2025-02-25 → 2025-04-24 | **First extended silence (~8 weeks)** | Attributed to "intensive research"; followed by a substantive CFLT initiation, consistent with the stated (if unverifiable) research process |
| 2025-05-07 | Self-admits selling $TSSI "way too early... had 10k shares at 2" | Clearest self-diagnosed process error in the archive: cutting a multibagger winner too soon, not riding a loser too long |
| 2025-06-25 | $POET initiated | Later becomes a patience/conviction case study ("it pays to wait bros," +263% ten months later) |
| 2025-07-18 → 2025-08-06 | Second extended silence (~3 weeks) | Followed by the $LDI initiation — his most extensively-argued single-name thesis in the archive |
| **2025-07-18** | $LDI initiated | Eventually the clearest documented full round-trip on a flagship conviction (+150%+ at one point, later "slightly in the red," Post #170, still held) |
| **2025-09-27** | **Dick Capital Substack launches** | Structural pivot point: the "no paid service, nor will there ever be" pledge (Post #53, Jan 2025) is broken; from here forward, 77% of AH posts exist primarily as a subscription funnel |
| 2025-09-28 | Substack "tops the charts" on Day 1 | First monetization-success milestone |
| 2026-01 | $BTQ (quantum) and $UAMY (rare earths) initiated | New thematic verticals (quantum computing, critical-minerals/rare-earths) added to the rotation; both later disclosed as having drawn down ~50% before recovering |
| 2026-01-06 | "Advanced Packaging" 10-name sector basket published | By 2026-05-10, independently tracked at +103% average; by 2026-06-16, +120% average — his strongest basket-format call |
| 2026-02 | "Power Semiconductors" 14-name sector basket published | +60% average by 2026-05-10 per his own recap |
| 2026-03-16 | Cites third-party (WSB/Reddit) validation: "+8% across 44 picks in the last 60 days" | External corroboration of high pick-diversification (44 concurrent names), though the source itself is unaudited |
| 2026-04-17 | Claims "+55% YTD... holding 30+ stocks at any given time" | First explicit portfolio-level percentage claim; no starting balance or reconciliation ever provided |
| 2026-05 | "Physical AI, Robotics, and Edge Computing" 36-ticker basket published | Largest single thematic basket in the archive; described as "over a month" of research |
| 2026-05-27 | Substack hits #1 New Bestseller / #1 Rising in Finance, "solid orange checkmark" | Monetization peak; subscription-urgency copy ("20 spots left," price-lock countdowns) intensifies through late May–June |
| 2026-06-28 | "Comprehensive review" post (#170) — full unrealized/realized ledger published | Most complete self-reported performance snapshot in the archive (+133% YTD claimed); also the source of the only two admitted drawdowns (LDI to red, BTQ/AMPG to ~-50%) in 175 posts |
| 2026-06-14 | First X/Twitter account launched | Cross-platform reach expansion continues alongside Substack |
| 2026-08-23 | Archive ends — gold/miners thesis ($15,000 gold PT, ATEX/Agnico/LunR) | No indication of retirement, blow-up, or account closure; active thematic rotation continues into mining/precious-metals as of the last available post |

---

*End of dossier. Source data: `/home/mpha/artemis/afterhour/reports/posts/@dick_lifetime.md`, `/home/mpha/artemis/afterhour/data/following/@dick_all_posts.json`.*
