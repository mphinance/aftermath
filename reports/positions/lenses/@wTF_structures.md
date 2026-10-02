# @wTF — Position Construction & Option Structures

**Lens:** what wTF actually built, structurally — spreads, risk reversals, ladders, and how they were sized, rolled, and unwound. Data window: 2023-12-22 through 2025-04-05 (last account snapshot). 1,186 leg-rows across 29 underlyings; 963 (81%) derivative legs, 218 (18%) equity legs.

---

## Headline findings

1. **UBER and BA are the book.** 991 of 1,186 leg-rows (84%) belong to just two names — UBER (628 legs, Oct 2024–Apr 2025) and BA (363 legs, Feb 2024–Apr 2025). Every other underlying (RIVN, HOOD, TSLA, QQQ, ZGN, ADBE, etc.) is a side position of ≤49 legs. This lens is therefore built around a deep dive on those two, with a short survey of the rest.

2. **The signature structure is a "seagull" (long call / short higher call / short lower put), and it was built independently on four separate UBER expiries at once.** By Feb 2025 wTF was simultaneously running near-identical seagulls on UBER's Mar-21 (75C/85C, later collapsed to a bare spread), Apr-17 (72.5C/80C/62.5P), Jun-20 (75-85C/100C/62.5P), and Aug-15 (70C/85C/52.5P) expiries — same architecture, laddered by *time*, not by strike. This is a repeated, deliberate template, not one-off improvisation.

3. **No collars and no true covered calls anywhere in the book.** Despite holding a stock anchor in BA (10k–15k sh most of 2024–25), UBER (32k–210k sh), RIVN and HOOD, short calls were never sized to the share count — BA's short-call notional ran 6–40x the share position. These are naked/leveraged short calls funding long calls, not stock protection. Puts bought against long stock (a real collar's other leg) essentially never appear either.

4. **Naked short puts are the account's financing engine.** On 2024-12-10 BA's book (from leg `costBasis`) shows −$1,412,076 cost basis (i.e., credit received) on the short $145P (Mar-21) alone, plus −$1,562,798 on the short $140P (Dec-19-25) — **$2.97M combined credit** from just those two puts (a third short put, $155P Jan-17, has no costBasis captured) — against **$2.24M** total cost basis on the long call ladder ($170/$175/$195C) held the same day: the short puts more than fully financed the long calls that day. UBER shows the same mechanic but only partial funding: on 2024-12-11 the two short puts (60P, 62.5P) carry **−$621,507** combined cost basis (credit) against **$2.12M** cost basis on the long calls held that day (one call leg's costBasis wasn't captured) — puts covering roughly 29% of the visible call cost. Both figures are `costBasis` sums from the raw leg data, not reconstructed fill prices, and are likely undercounts where a leg's costBasis field is null.

5. **Strikes are opened well out of the money on the long side, close to the money on the short-put side.** Across 24 UBER option opens, long/short calls opened averaging **+22.6% OTM** (median DTE 110 days); the 7 put opens averaged **-4.5%** (near-the-money, i.e., maximum premium collection). BA's 38 opens: calls averaged **+10.1% OTM**, puts **-3.7%**. Median DTE at open: UBER 110 days, BA 94 days — a 3–4 month base tenor, but both names layer in far-dated LEAPS (BA to Dec-2025, 374 DTE) and 2-day tactical options at the same time.

6. **Delta-notional leverage swung between ~0.3x and >2x account value.** Using Black-Scholes deltas (30-day realized vol, r=4.5%, method below), UBER's share-equivalent exposure peaked at **2.21x account value on 2025-01-16** (px $68.58, $52.2M account) after a call-heavy build, then fell to 0.31x by Feb 10 after a fast de-risking. BA peaked at **2.01x on 2025-04-01**. Both names spent most of their history in the 0.4x–1.0x band.

7. **Adds are frequent but modest; the account almost never pyramids in one shot.** UBER: 34 ADD events, median size 1,000 contracts (vs. 1,200-contract median for fresh opens) across 26 distinct trading days of activity. BA: 66 ADD events, median 340 contracts, across 52 distinct days. The exception proves the rule: on 2025-01-27 wTF trimmed 34,907 of 46,923 UBER $80C (Mar-21) contracts in one print — a 74% single-day unwind, the single largest one-day size change in either name.

8. **Two structural oddities stand out: an ITM call exercised into stock, and BA's twin same-day FLIPs.** On 2025-03-21 UBER's $75C (Mar-21 expiry) closed ITM (UBER $75.84) and 1,100 contracts (110,000 sh) were let ride to expiry and exercised rather than sold — equity jumped from 100,000 to 210,000 shares overnight (2025-03-22), while the paired short $85C (856 ct) expired worthless and was simply kept. Separately, on 2025-03-19 ("Patience is a virtue ✈️✈️✈️") BA had the dataset's only two FLIP events same day: the 2-DTE $170P (Mar-21) flipped from net short 700 to net long 2,300 contracts (a same-day reversal into $23M of put notional two days before expiry), plus a small $210C (Jun-20) flip from short 100 to long 100.

---

## Method notes

- **Moneyness** = (strike − underlying close on/just before the trade date) / underlying close, from `data/prices/@wTF_prices.json` bars. Positive = call struck above spot (OTM call) or put struck above spot (ITM put, rare here); for puts I report strike below spot as negative (OTM put).
- **DTE at open** = expiration date − trade date (calendar days), taken from the `changes` file's OPEN LONG/OPEN SHORT events. This is the exact snapshot date the change was first observed, not necessarily the fill date (per the standing caveat that changes happen *between* snapshots).
- **Delta / leverage** is an *estimate*: Black–Scholes delta using 30-trading-day realized (close-to-close) volatility as of each snapshot date, r = 4.5%, T in calendar days /365. This is not the account's actual IV surface and will understate/overstate true delta around earnings or skew events — labelled everywhere as an estimate. Share-equivalent exposure = Σ(contracts×100×delta) + equity shares; leverage = (exposure × underlying px) / account total_value at that snapshot.
- **Data-quality caveat:** the account snapshot on 2024-09-09 through 2024-09-11 shows `total_value` collapsing to ~$3.3–3.7M (from ~$50M the days before and after) — this is almost certainly a vendor/API glitch (a partial account pull), not a real 93% one-day drawdown followed by a same-scale recovery. I excluded snapshots with account_value < $5M from leverage stats. Also: HOOD shows a residual 0.39849-share "position" worth ~$15–19 from late Feb–Mar 2025 after the 309,160-share position was fully exited — a rounding/DRIP dust artifact, not a real position.

---

## 1. Structures across the account — taxonomy with dated examples

| Structure | Where seen | Example (date, legs) |
|---|---|---|
| **Stock + long calls (stacking, not covered)** | BA Feb–Sep 2024; RIVN Mar 2025 | BA 2024-03-13: +90,500 sh stock, +305 ct $200C (May-17), +4 ct $210C (Jun-21) — buying more upside on top of stock, calls far too small to be "covered" against anything |
| **Naked short put ladder financing long call ladder** | BA Oct 2024→; UBER Dec 2024→ | BA 2024-12-10: short $140P (Dec-19-25), $145P (Mar-21), $155P (Jan-17) simultaneously vs. long $170C/$175C/$195C — three tenors of short puts funding three tenors of long calls |
| **Seagull (long call / short higher call / short lower put)** | UBER Jun-20 & Aug-15 2025 expiries from Dec 2024 on; Apr-17 expiry from Feb 2025 | UBER 2024-12-30: +200 $80C, and Jun-20 book = +2,560 $85C / −2,560 $100C / −650 $62.5P (textbook seagull) |
| **Bull call ladder (2 long strikes vs. 1 short strike)** | BA Dec 2024 Mar-21 book | BA 2024-12-10: +1,000 $170C, +600 $175C vs. −1,600 $200C — two stacked verticals sharing a short leg |
| **Put spread + naked short call (bearish-tilted combo)** | TSLA, 6 days only (Oct 24–31, 2024, right after Tesla's Oct-23 earnings pop) | TSLA 2024-10-28: +2,700 $250P (Nov-29), and Dec-20 book: −1,250 $300C / −1,650 $210P / +2,250 $240P — a bear put spread (240/210) stacked with a naked short call, no stock; fully closed within a week |
| **Naked short strangle-ish opener, quickly abandoned** | BA 2024-09-09 | +400 $155C, +700 $165C, −1 $165P (Nov-15) — the day the whole Feb–Sep-2024 book was reset; short put here is a 1-lot toe-in, not a real position |
| **Covered call / collar (long stock + short call sized to shares, or + long put)** | **Not observed anywhere in the dataset** | — |

The account does not run clean, single-named textbook structures for long stretches. What repeats is the *seagull template* on UBER and the *short-put-ladder-funds-long-call-ladder* template on both names — both are "sell what's cheap and OTM on the downside, buy convexity upside, sell some of the upside back" logic, executed across multiple simultaneous expiries rather than one clean spread per name.

## 2. Strike selection & DTE

| Underlying | Opens (n) | Avg DTE at open | Median DTE | Avg call moneyness (open) | Avg put moneyness (open) |
|---|---|---|---|---|---|
| UBER | 24 | 128.2 days | 110.5 days | +22.6% OTM (n=17) | −4.5% (n=7) |
| BA | 38 | 122.3 days | 94.0 days | +10.1% OTM (n=24) | −3.7% (n=14) |

Reading this: **long calls are bought as cheap, far-OTM convexity** (UBER especially — nearly a quarter of spot away on average), while **short puts are sold close to the money** where premium is richest. This is consistent across both names and is the mechanical reason the "short put funds long call" framing in finding #4 works at all — the puts are priced for maximum time value, the calls are priced for maximum leverage per dollar.

**Laddering by expiry, not by strike.** At peak (2025-02-03) UBER carried live option structures on **5 simultaneous expiries at once** (Feb-21, Mar-21, Apr-17, Jun-20, Aug-15); BA peaked at **4 simultaneous expiries** (2025-01-03: Jan-17, Mar-21, Jun-20, Dec-19-25). **Rolling** is visible but partial — e.g., UBER's Feb-21 book (67.5C/70C/80C) was fully closed 2025-02-05/06 as Mar-21 and Apr-17 books were simultaneously built up, which reads as "let the front book expire/close, already have the next one on" rather than a mechanical roll of the same strike forward.

## 3. Scaling — how positions get built and unwound

| Underlying | OPEN events (option) | Median open size | ADD events | Median add size | Max single add | TRIM/CLOSE events | Largest single unwind |
|---|---|---|---|---|---|---|---|
| UBER | 24 | 1,200 ct | 34 | 1,000 ct | 15,950 ct (2024-12-11, $80C Mar-21) | 27 TRIM + 11 CLOSED + 3 EXPIRED | **34,907 ct trimmed 2025-01-27** ($80C Mar-21, 74% of the then-46,923-ct position, in one print) |
| BA | 38 | 720 ct | 66 | 340 ct | 5,700 ct (2024-11-05, $165C Dec-20) | 26 TRIM + 32 CLOSED + 3 EXPIRED + 2 FLIP | 4,100 ct closed 2024-10-29 ($165C Nov-15, full exit of that leg) |

Equity adds are lumpier and rarer: UBER's stock position built in 7 discrete tranches (32,000 / 33,000 / 15,000 / 10,000 / 5,000 / 5,000 / **110,000** sh — the last one being the call-exercise event in finding #8, not a purchase). BA's stock built in 13 tranches from 5,000 to 35,500 sh, then was fully liquidated in one shot (−74,001 sh, 2024-09-09) before the account rebuilt a much smaller (10k–15k sh) BA stock anchor from Oct 2024 on.

Net read: **the account adds in modest, frequent increments (medians well under the size of a fresh open) and unwinds the same way — except for occasional large single-print de-risking trims** (the UBER Jan-27 74% trim being the standout), which look like decisive "I'm wrong, cut it" moves rather than scaled-out exits.

## 4. Exposure & leverage over time

Estimated delta-share-equivalent exposure (BS delta, 30d realized vol) × underlying price, divided by account `total_value` at that snapshot:

| Date | Underlying | Px | Net call ct | Net put ct | Equity sh | Δ-share-equiv (est.) | Account value | Leverage (est.) |
|---|---|---|---|---|---|---|---|---|
| 2024-10-29 | UBER | $79.21 | +491 | 0 | 0 | 30,224 | $55.1M | 0.04x |
| 2024-12-11 | UBER | $61.18 | +30,323 | −2,025 | 32,000 | 710,060 | $49.8M | 0.87x |
| 2025-01-16 | UBER | $68.58 | +59,884 | −2,315 | 65,000 | **1,681,736** | $52.2M | **2.21x (peak)** |
| 2025-02-10 | UBER | $78.63 | −3,703 | −2,340 | 90,000 | 273,988 | $69.6M | 0.31x |
| 2025-03-26 | UBER | $74.18 | +9,148 | −4,234 | 210,000 | 825,610 | $64.1M | 0.96x |
| 2024-02-29 | BA | $203.72 | +12.8 | 0 | 10,000 | 10,744 | $82.5M | 0.03x |
| 2024-11-05 | BA | $151.00 | +16,259 | −2,665 | 7,100 | 443,762 | $53.9M | 1.24x |
| 2025-03-21 | BA | $178.11 | +6,400 | −2,700 | 15,370 | 505,415 | $64.0M | 0.85x |
| 2025-04-01 | BA | $168.17 | +10,300 | −2,700 | 15,370 | 551,460 | $46.1M | **2.01x (peak)** |

Both names spent most of their lives in a 0.3x–1.0x delta-notional band relative to account value, with two clear leverage spikes — UBER in mid-January 2025 (call-heavy build into a rally) and BA at the very end of the observed window (early April 2025). The UBER spike was de-risked hard within about three weeks (2.21x → 0.31x between Jan-16 and Feb-10), coincident with the $80C Mar-21 trims and the shift toward the multi-expiry seagull structure.

## 5. Deep dive — $UBER (Oct 2024 – Apr 2025)

The entire UBER campaign in this dataset runs Oct 29, 2024 → Apr 2, 2025 (628 legs, 100 change events, 42 snapshots) — this *is* the full history AfterHour captured for wTF in the name.

**Phase 1 — single lotto call (2024-10-29).** Opens with one position: +491 ct $78C exp 2024-11-08 (10 DTE, 1.5% OTM), bought at $4.15. Expires worthless 12 days later.

**Phase 2 — the book gets built, Dec 11 2024 ("Twenty Thousand Leagues Under the Seas 🚕🤖").** In one session wTF opens: −2,560 $100C (Jun-20), −1,375 $60P (Mar-21), −650 $62.5P (Jun-20), +7,098 $80C (Feb-21), +5,700 $80C (Mar-21, added to 21,650 same day), +2,560 $85C (Jun-20, added to 4,135), plus 32,000 shares at $61.66. This single day establishes the multi-expiry seagull/ladder architecture that persists for the rest of the campaign. UBER closed $61.18 that day — the $80C strikes were bought ~31% OTM.

**Phase 3 — build-out through year-end (Dec 12–30, 2024).** Adds shares to 65,000 (three tranches), adds more $80C across Feb-21 and Mar-21 (by 2024-12-30 the Mar-21 $80C alone reaches 39,742 ct), opens the Aug-15 tenor (+225 $70C / −225 $85C / −190 $52.5P — a fourth simultaneous seagull), and a new short $60P (Aug-15). By Jan 2 the Mar-21 $80C position peaks near 46,923 contracts (4.69M share-equivalent notional) — the single largest strike concentration in the whole UBER campaign.

**Phase 4 — the big cut (2025-01-27).** With UBER around $68.77, 34,907 of those 46,923 Mar-21 $80C contracts are trimmed in one print (−74%) at $1.11 — down from cost bases mostly under $1.00, a modest win taken off a position that had grown too large. This is the single biggest one-day de-risking move in the dataset for any underlying.

**Phase 5 — earnings-week churn (Feb 3–7, 2025, UBER earnings Feb-5).** A flurry of activity: opens a new Apr-17 seagull (+1,200 $72.5C / −1,200 $80C / −1,200 $62.5P), fully closes the Feb-21 $80C and Mar-21 $80C legs, adds 15,000 more shares at $64.48 into the earnings drop, then rebuilds call exposure the next several sessions as UBER rips from $64.48 (2/5) to $80.29 (2/13). Leverage swings accordingly (0.44x on 2/5 up toward 0.85x by 2/26).

**Phase 6 — steady multi-book carry (Feb 19 – Mar 20, 2025).** Runs concurrent Mar-21, Apr-17, Jun-20, and Aug-15 seagulls/ladders with modest adds and trims; opens a naked short $75P (Jun-20, 1,394 ct) and a second short $75P (Apr-17, 500 ct) on Feb-19/24 — the closest-to-the-money puts sold in the whole UBER campaign (−7.6% and −1.9% OTM respectively) — while UBER chops $74–81.

**Phase 7 — expiry and exercise (Mar 21–22, 2025).** The Mar-21 $75C (1,100 ct) expires in the money (UBER $75.84 close) and is exercised into 110,000 shares rather than sold for cash — equity jumps from 100,000 to 210,000 shares overnight. The paired short $85C (856 ct) expires worthless and the premium is kept.

**Phase 8 — final build before the data ends (Mar 26 – Apr 2, 2025).** Adds meaningfully to the Jun-20 book (+4,000 $75C, +2,500 $80C, +5,368 $85C total by Apr-2, while trimming/closing the $100C short and closing out both remaining short puts, 52.5P and 60P, for gains). The dataset ends 2025-04-02 with UBER carrying live Apr-17 (72.5C/62.5P/75P — three-leg short-put/long-call combo, no more short call on this tenor) and Jun-20 (large multi-strike call ladder, short puts closed) books plus 210,000 shares.

## 6. Deep dive — $BA (Feb 2024 – Apr 2025)

BA has two distinct eras separated by a full account reset on 2024-09-09.

**Era 1 — stock + long calls, whipsaw trading (Feb 29 – Mar 28, 2024).** Starts with +10,000 sh + small long calls ($200C May-17, $210C Jun-21). Over the next month wTF repeatedly opens and closes the *same* $200C/$210C pair — five full open/close round trips between Mar-13 and Mar-22 alone, each time re-entering near where the last one closed, while stock is built from 10,000 to 100,500 shares (peak, 2024-03-26) then trimmed back to 65,000 by month end. This reads as active day/swing trading of a single call pair layered on a growing stock core, not a structured position — no shorts at all in this era. The whole book (stock + calls) is fully liquidated by 2024-09-09 (−74,001 sh, calls expired), a hard reset.

**Era 2 — multi-expiry short-put-funded call ladders (Sep 2024 – Apr 2025).** Restarts 2024-09-09 with a small toe-in ($155C/$165C long, 1-lot $165P short) and quickly escalates: by 2024-10-29 wTF is short 925 $140P (Dec-20) against a growing $165C book, and by 2024-12-10 the full architecture is in place — simultaneous short puts at $140 (Dec-19-25), $145 (Mar-21), $155 (Jan-17) funding long calls at $170/$175 (Mar-21) and $195 (Dec-19-25), plus a short $200C (Mar-21) capping the Mar-21 book into a call ladder. This is the day the account's most complex single BA structure exists — 3 simultaneous expiries (Jan-17, Mar-21, Dec-19-25), 7 distinct strikes.

**Rolling the short puts up (Jan–Feb 2025).** As BA grinds from $164 (Dec-10) to $180 (late Feb), the short puts are systematically rolled up in strike: $145P→$160P (2025-01-03), $160P→$170P (2025-01-25), and a new $180P (Dec-19-25) opened 2025-02-03 — each roll captures the stock's rise by re-striking closer to the money for more premium, the clearest "roll" behavior in either name (contrast with UBER, where expiring books were mostly let go rather than rolled).

**The two FLIPs (2025-03-19, "Patience is a virtue ✈️✈️✈️").** With BA at $172.62 and the $170P (Mar-21) two days from expiry, wTF reverses the position same-day from net short 700 to net long 2,300 contracts (+3,000 ct traded, $1.89), plus a much smaller $210C (Jun-20) flip from short 100 to long 100 (+200 ct, $1.85). This is the only FLIP behavior anywhere in the dataset and reads as a sharp, short-dated defensive/speculative pivot right at expiry rather than routine position management — the $170P book is fully closed two days later on expiry (2025-03-21).

**Final build (Mar 26 – Apr 1, 2025, data ends).** Adds heavily to $185C (Jun-20): +1,800 (3/26) then +4,100 (4/1) — the largest BA add in the whole dataset — pushing the estimated delta-leverage to its campaign peak of 2.01x account value on 2025-04-01, the last BA snapshot in the data.

## 7. Other underlyings (brief)

- **RIVN** (49 legs, Feb 2024–Mar 2025): long-held stock core (100k→261k→351k→151k sh) with occasional long calls stacked on top (+1,500 $14C, +4,068 $11C) — same stacking pattern as BA's Era 1, no shorts.
- **HOOD** (25 legs): single large stock position (309,160 sh) held from Feb 2024, fully exited by early 2025 (leaves the 0.398-share dust noted above).
- **TSLA** (23 legs, Oct 24–31 2024 only, 6 days): the one clearly event-driven trade — a bear put spread ($240P/$210P, Dec-20) plus a naked short $300C, opened the week after Tesla's Oct-23 earnings beat, fully closed within a week.
- **QQQ, ZGN, ADBE, RXRX, SQ, AAPL** and others are single-digit-legs, mostly simple long calls or (ZGN) a pure stock accumulation — no repeatable structure to report.

---

## Summary for handback (10 lines)

1. UBER + BA are 84% of all position legs; everything else is minor.
2. wTF's repeated template is the **seagull** (long call / short higher call / short lower put), run on 4 UBER expiries at once.
3. **No collars or covered calls** anywhere — short calls/puts are naked, not stock-hedged, despite a stock anchor being held throughout.
4. Naked short puts are the financing leg: BA sold 3 strikes of puts in one day (2024-12-10, ~$2.1M-ish credit territory) to fund a long-call ladder.
5. Calls are opened far OTM (UBER +22.6% avg, BA +10.1% avg); puts are sold near the money (−4.5% / −3.7% avg) for maximum premium.
6. Median DTE at open: UBER 110 days, BA 94 days, but both run simultaneous 2-day and 300+ day tenors at once.
7. Estimated delta-notional leverage (BS/realized-vol) ranged 0.03x–2.21x account value; peaks were UBER 2025-01-16 (2.21x) and BA 2025-04-01 (2.01x).
8. Adds are small and frequent (medians ~1,000 ct UBER / ~340 ct BA); the exception is a single 74% one-day trim of UBER's $80C Mar-21 book on 2025-01-27.
9. Two standout mechanics: a 1,100-ct UBER $75C position was let ride to ITM expiry and **exercised into 110,000 shares** (2025-03-22); BA had its only two FLIP events, both same-day, on 2025-03-19, reversing a 2-DTE put position from net short to net long.
10. Data caveat: BA's account_value glitches to ~$3.3–3.7M for three snapshots around 2024-09-09/11 (vs ~$50M around it) — excluded from leverage stats as a likely vendor artifact.

Files: analysis scripts in scratchpad (`analyze.py`, `exposure.py`); snapshot/exposure JSON dumps also in scratchpad for reproducibility (not committed to repo).
