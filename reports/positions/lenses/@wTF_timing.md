# @wTF — Timing & Market Context Lens

Scope: when @wTF acted relative to price, earnings, and market regime — not position structure or P&L (those are the other lenses' jobs). Data window: position snapshots run **2024-02-07 → 2025-04-02**; the account-value series runs **2023-12-22 → 2025-04-05** (its final reading). Price/earnings history covers 2023-08 → 2025-09 for every underlying that has bars.

## Method, in brief (full detail in "Methodology" section below)

Every OPEN/ADD/TRIM/CLOSE/EXPIRED/FLIP event in `data/positions/@wTF_positions.json` (`changes` array, 414 rows) was anchored to a trading day and scored against `data/prices/@wTF_prices.json`: % below/above the trailing-20-trading-day high/low, prior 5d/20d return, and forward 5d/10d/20d return of the underlying. Each event also got a **window** = (last time this root ticker appeared in *any* post, → this event's timestamp), because the snapshot data only shows a diff, not the exact trade time. **283 of 410 events with price data (69%) qualify** as either a first-ever sighting of that ticker or a window ≤3 trading days; the numbers below use that qualifying subset unless stated otherwise. 4 events (BA×1 CFLT, RIVN/SPR×3) have no price bars and are excluded.

---

## Headline findings

1. **Directional bets were overwhelmingly bullish: 231 bullish vs. 32 bearish OPEN/ADD/FLIP events (88%/12%)**, concentrated in long calls and short puts on BA (70 opens/adds) and UBER (45).

2. **Bullish entries were bought on weakness, not chased on strength.** Qualifying bullish OPEN/ADD events sat at a median 32.6th percentile of the trailing 20-day range (mean −9.3% off the 20d high) vs. a same-ticker baseline of the 48th percentile / −10.0% off high — and the average prior-5-day return at entry was **−0.5% vs. +0.5% baseline**. BA (median entry in the bottom 30% of its range, prior-5d −1.75%) and RIVN (bottom 16% of range, prior-5d −8.0%) drove this; UBER entries were closer to trend-neutral (56th percentile, prior-5d +1.45%).

3. **Bearish bets were the opposite: they were entered at extremes, chasing a fade.** Qualifying bearish OPEN/ADD events sat at a median 84th percentile of the 20-day range after an average **+15.2% prior-5-day pop and +13.9% prior-20-day run** — a textbook "fade the rip" pattern, clearest in TSLA (8 of 10 TSLA opens/adds were bearish, entered after +16.4% avg 5-day gains, at the 85th percentile of range).

4. **The TSLA fade worked, but only because they didn't hold it.** After TSLA's post-earnings +22% single-day pop (2024-10-24), @wTF opened long $240/$250 puts and short $300 calls that same day, then **added into further pain** as TSLA kept ripping to $273 over the next four sessions (unrealized losses of $200–290K per leg by 10/25–10/28). They closed most of it by 10/31 as TSLA rolled over −8.5% from the highs, converting to profits of +$116K to +$339K per leg. Cohort-wide, bearish adds' forward returns confirm the logic: avg fwd-5d **−3.4%** (thesis working) but avg fwd-20d **+3.4%** (thesis reversing) — the data says these fades only paid if closed inside ~1–2 weeks, which is what happened here.

5. **Trims/closes leaned toward selling into strength, and it was good selling.** 97 qualifying TRIM/CLOSE events averaged the 61st percentile of the 20-day range and a +2.1% prior-5-day return at the sell. Split by prior-return sign: the 64 sold-into-strength exits were followed by **avg fwd-10d −4.7%, fwd-20d −5.3%** in the underlying (they got out before real weakness); the 36 sold-into-weakness exits were followed by **avg fwd-10d +1.8%, fwd-20d +3.4%** (mild "sold the bottom" cost, though medians are much smaller — a few sharp rebounds, e.g. RIVN/BA, skew the mean).

6. **They were fully invested and adding risk into the April 2025 tariff crash, not de-risking ahead of it.** Cash balance fell to **$1** on 2025-04-01 (vs. $16.9M on 3/26). On 2025-03-21 and 2025-03-28 they opened/added **240,000 shares of QQQ $500 calls** (a fresh, sized-up index-level bullish bet, QQQ then at ~$481, i.e. ~4% OTM). The account's last reading, 2025-04-05 (Saturday, marking Friday 4/4 closes), showed **total value $33.2M vs. $58.2M just three days earlier (4/2)** — a 43% drop in 3 days — and down ~65% from the account's **all-time-high of $95.1M on 2024-03-28**. One partial exception: on 2025-03-19 they flipped a BA short put to long and bought 140,000 BA Dec-2025 $180 puts — real hedging, but on a single name, not portfolio-wide.

7. **August 2024 is a total blackout in this dataset** — zero position snapshots and no usable account readings between 2024-07-26 and 2024-09-09 — so the Aug 5, 2024 vol-shock (VIX briefly >60) cannot be assessed at all for this trader. This is a hole in the data, not a finding about behavior.

8. **The Dec 2024 / Jan 2025 mini-shocks show tactical, not strategic, reaction.** On the Dec 18, 2024 FOMC hawkish-cut selloff (VIX 17.4→27.6 same day), they closed one BA call the same day but then **added** RIVN shares, ZGN shares and UBER calls over the following 48 hours — i.e., bought the vol spike. On the Jan 27, 2025 "DeepSeek" selloff (SPY −1.4%, QQQ −2.9%), they cut their single largest position — UBER $80 calls — by **74% (4.69M → 1.20M share-equiv) same day**, a real, fast de-risking move.

---

## OPEN/ADD/FLIP timing: bullish vs. bearish (qualifying events, n=183 of 261)

| | n | Median 20d range position | Avg % from 20d high | Avg prior 5d ret | Avg prior 20d ret | Avg fwd 5d | Avg fwd 10d | Avg fwd 20d |
|---|---|---|---|---|---|---|---|---|
| **Bullish adds/opens** | 158 | 0.33 (33rd pct) | −9.3% | **−0.5%** | −1.8% | +0.9% | −0.3% | +0.5% |
| **Bearish adds/opens** | 25 | 0.84 (84th pct) | −5.6% | **+15.2%** | +13.9% | −3.4% | +0.8% | +3.4% |
| Baseline, same tickers (all days) — bullish set | — | ~0.48 | −10.0% | +0.5% | +2.2% | +0.3% | +0.6% | +1.4% |
| Baseline, same tickers (all days) — bearish set | — | ~0.46 | −10.8% | +0.1% | +0.1% | 0.0% | −0.1% | −0.5% |

Reading it: bullish entries were dip-bought (below baseline range position, negative prior returns vs. a positive baseline) but the median forward return over 10–20 days was **negative** (median fwd-10d −2.7%, fwd-20d −2.1%) even though the mean is roughly flat — a few large winners (mostly UBER, see below) offset a larger number of adds that kept bleeding for weeks (mostly BA and RIVN, both persistent 2024 downtrends). Bearish entries chased extremes and the initial fade direction was usually right (avg fwd-5d −3.4%), but by fwd-20d the average bearish bet was underwater on the market (+3.4%) — consistent with these being short-dated tactical fades, not trend bets, and consistent with how quickly @wTF actually closed them (see TSLA case above).

### By underlying (qualifying OPEN/ADD only)

| Root | n bull / bear | Bull: median range pos | Bull: prior 5d | Bull: fwd 10d / 20d | Bear: median range pos | Bear: prior 5d | Bear: fwd 10d / 20d |
|---|---|---|---|---|---|---|---|
| BA | 68 / 2 | 0.30 (dip-buy) | −1.8% | −2.8% / −3.5% | 0.54 | +0.6% | +0.2% / −3.7% |
| UBER | 38 / 7 | 0.56 (trend-neutral) | +1.5% | +0.8% / +2.3% | 0.69 | +6.1% | +6.6% / +4.5% |
| RIVN | 10 / 0 | 0.16 (deep dip-buy) | −8.0% | −3.5% / −2.6% | — | — | — |
| TSLA | 2 / 8 | 0.87 (breakout chase, n=2) | +18.9% | +23.7% / +29.7% | 0.85 (fade-the-rip) | +16.4% | +23.2% / +30.9% |
| HOOD | 3 / 0 | 0.70 (n=3, thin) | +5.2% | +3.7% / +7.7% | — | — | — |

BA is the clearest, largest-sample dip-buying book (n=68) and it's the one where forward returns stayed negative through 20 days — @wTF was consistently early into a name that kept falling through most of 2024 (BA didn't bottom and sustain a recovery until the Nov–Dec 2024 window; see the earnings section). UBER is the best-timed book: entries closer to trend-neutral, and the only one of the four with positive average forward returns at every horizon. TSLA's tiny bullish sample (n=2) sits in what looks like breakout-chase territory but is too small to read anything into.

---

## Trims and closes: strength-selling vs. capitulation

Qualifying decrease events (TRIM/CLOSED/EXPIRED, n=100, windows ≤3 trading days or root's first appearance):

| Cohort | n | Avg fwd 5d | Avg fwd 10d | Avg fwd 20d | Median fwd 10d | Median fwd 20d |
|---|---|---|---|---|---|---|
| Sold into strength (prior 5d ret > 0) | 64 | −0.4% | **−4.7%** | **−5.3%** | −4.1% | −3.9% |
| Sold into weakness (prior 5d ret ≤ 0) | 36 | +2.3% | +1.8% | +3.4% | −3.0% | +0.1% |

TRIM+CLOSED only (n=97, excludes EXPIRED): avg entry-to-exit context was the 61st percentile of the 20-day range, +2.1% prior-5d / +4.5% prior-20d return — i.e. **the modal exit was a trim into a rally**, not a stop-out. And those strength-sells were, on average, well-timed: the underlying kept falling for the next 2–4 weeks more often than not (avg −5.3% at 20 days). The weakness-sells (capitulation-flavored exits) show a mean bounce afterward (+3.4% at 20d) that looks like "sold some bottoms," but the **median** for that same cohort is only +0.1% at 20 days — the mean is pulled by a handful of sharp V-shaped recoveries (RIVN's Feb–Mar 2025 bounce, BA's Nov–Dec 2024 recovery), not a systematic pattern of dumping right before every low.

Net read: trimming discipline was one of the stronger parts of this trader's process — they took profits ahead of pullbacks more often than they panic-sold bottoms, on this data.

---

## Earnings positioning: UBER, BA, RIVN, HOOD, TSLA

Coverage caveat up front: the position-snapshot data only shows what was posted, and there are long silent stretches for some names (HOOD in particular: no HOOD post between 2024-03-28 and 2025-02-25 — 11 months — so the 2024-05-08, 2024-08-07, 2024-10-30 [−16.7% day], and 2025-02-12 [+14.1% day] HOOD earnings are all **invisible**; we only know they were still long 431,420 shares at the start of that gap and 0.4 shares — i.e. essentially flat/closed — by the time it reopens). Earnings dates after the dataset's last snapshot (2025-04-02) are out of scope entirely.

### UBER

| Earnings date | Day-of move | Next-day move | What they did in the ±10 trading days |
|---|---|---|---|
| 2024-10-31 | −9.3% | +1.7% | Opened a small ($78c, 49,100 sh-equiv) long-call flyer 2 days before; it expired worthless by the 11/8 expiry (well OTM after the drop). |
| 2025-02-05 | **−7.6%** | **+8.6%** | Heavy, active management: 36 changes in the ±10-day window (see UBER deep-dive below). Not a "hold through" — continuous spread restructuring before, during and after the print. |

**IV-crush signature (UBER, Feb 2025):** comparing the last pre-print snapshot (2/4) to the first post-print snapshot (2/5, after the −7.6% day-of drop), several deep-OTM, long-dated legs lost more value than the stock move alone would explain — e.g. the UBER $85c 2025-06-20 fell from $2.39 to $2.07 (−13.4%) and the $75c 2025-06-20 fell from $5.05 to $4.45 (−11.9%), both June-dated and far enough from the money that delta shouldn't explain a >10% drop on a single-day, partially-reversing stock move. Read as an estimate, not a computed Greek (no IV series in this dataset) — but it's consistent with a real vol crush on the June book that day.

### BA

| Earnings date | Day-of move | Next-day move | What they did |
|---|---|---|---|
| 2024-10-23 | −1.8% | −1.2% | No position beforehand (last BA post was 2024-03-28). **Bought the post-earnings weakness**: opened BA shares (7,100) and long $165c/$175c calls, plus short $135p/$140p puts, over 10/29–11/1, after BA had already fallen from ~$160 to ~$148–155. BA fell further to $140.19 by 11/15 (a further −9% from the entry cluster) before recovering to $173 by mid-December — the add worked, but only after another leg down. |
| 2025-01-28 | +1.5% | −2.3% | Very active: 20 changes in the window — rolling short puts up ($160p→$170p, $175p), trimming/closing calls, adding new short puts at $175/$180. Net effect was raising directional exposure (more short puts = more bullish) into a stock that was mid-recovery (BA ran from ~$148 in Nov to ~$175 by late Jan, ~+18%). |

### RIVN

| Earnings date | Day-of move | Next-day move | What they did |
|---|---|---|---|
| 2024-02-21 | −3.2% | **−25.6%** | Held 100,000 shares through the print (opened 2024-02-07). Did **not** sell into the crash; instead **added 930,001 shares on 2024-02-29** (qty 100,000→1,030,001) at $11.22, roughly where the stock had already fallen to after the −28% two-day drop. That dip-buy chopped for two months, fell a further −18% to $9.21 by May 1, then round-tripped back to ~$11.40 by early June — a rough, not-immediately-rewarded add. |
| 2025-02-20 | −2.3% | −4.7% | Added shares into the print (2/10), then on earnings day itself trimmed shares (193,720→153,720) while opening $14c calls (swapping some stock delta for leveraged upside), then added shares aggressively on 2/24 and 2/26 as the stock kept falling — another dip-buy-into-weakness pattern. |

### HOOD

Only the account-opening entry (2024-02-07, 309,160 shares) sits inside an earnings window with visibility: HOOD's 2024-02-13 print moved +13.0% next-day and they simply held through it (confirmed unchanged 309,160 shares before/after) — a lucky hold given the timing coincidence, not an active earnings bet. Every other HOOD print from May 2024 through Feb 2025 falls inside the 11-month silent gap noted above.

### TSLA

No TSLA position existed heading into the 2023-10-18, 2024-01-24, 2024-04-23, or 2024-07-23 prints (first TSLA activity in this dataset is 2024-10-24, the day after the 2024-10-23 report). The 2024-10-23 earnings is the TSLA "fade the +22% pop" trade detailed in headline finding #4. No TSLA position is visible around the 2025-01-29 print (last touch was 2024-10-31, next is a stale snapshot).

---

## Market regime overlay

Monthly account-value checkpoints (last reading of each month) against SPY/VIX:

| Month | Account value | SPY | VIX |
|---|---|---|---|
| 2023-12 | $57.4M | 473.65 | 13.0 |
| 2024-01 | $52.3M | 482.88 | 14.4 |
| 2024-02 | $83.1M | 508.08 | 13.4 |
| 2024-03 | **$95.1M (ATH)** | 523.07 | 13.0 |
| 2024-04 | $78.4M | 518.43 | 16.0 |
| 2024-05 – 2024-06 | *no readings* | | |
| 2024-07 | *bad/null reading only* | 544.44 | 16.4 |
| 2024-08 | *no readings — total blackout* | | |
| 2024-09 | $51.0M | 571.47 | 17.0 |
| 2024-10 | $54.4M | 568.64 | 23.2 |
| 2024-11 | $53.9M | 576.70 | 20.5 |
| 2024-12 | $48.2M | 586.08 | 17.4 |
| 2025-01 | $62.7M | 601.82 | 16.4 |
| 2025-02 | $67.9M | 585.05 | 21.1 |
| 2025-03 | $60.1M | 555.66 | 21.7 |
| 2025-04-05 (final) | **$33.2M** | ~505 (4/4 close) | ~45.3 (4/4 close) |

Notes on the gaps: between the account's all-time high ($95.1M, 2024-03-28) and the next usable reading ($51.0M, 2024-09-27) there is essentially no visibility for five months, including the entire Aug 2024 vol event — so we cannot say whether the ~$44M (−46%) decline over that stretch was a controlled drawdown, a single bad trade, or several. This is the single biggest visibility gap in the dataset for the regime question.

**April 2025 tariff crash, day by day (the only regime event with full data density):**

| Date | Account value | Cash | SPY | QQQ | VIX | Note |
|---|---|---|---|---|---|---|
| 2025-03-27 | $66.3M | $16.9M | 567.08 | 481.62 | 18.7 | Local peak |
| 2025-03-28 | $60.1M | $14.6M | 555.66 | 468.94 | 21.7 | −9.3% |
| 2025-04-01 | $46.1M | **$1** | 560.97 | 472.70 | 21.8 | Fully invested, no cash cushion |
| 2025-04-02 | $58.2M | $12.4M | 564.52 | 476.15 | 21.5 | "Liberation Day" tariffs announced after this close |
| 2025-04-05 (Sat, marks 4/4 close) | **$33.2M** | $12.1M | ~505 | ~423 | ~45.3 | Final observed reading, −50% from 3/27 peak |

Positioning into this window (legs as of 3/26–4/2): large long-call stacks in UBER (calls spanning $72.5–$105 strikes across Apr/Jun/Aug 2025 expiries, plus 210,000 UBER shares) and BA (long $165c/$185c calls, 950,000 share-equiv by 4/1, plus short $170p/$175p puts), plus a newly opened XYZ (formerly SQ) position on 3/26 — 30,000 shares and 300,000 share-equiv of $65c (6/20 exp). On 2025-03-21 they opened 70,000 QQQ $500 calls (2025-05-16 expiry) and added to 240,000 on 3/28 — sizing *up* a fresh bullish index bet in the same week the market was already rolling over from its Feb 2025 high. The lone hedge: 2025-03-19, flipped a short BA $170 put to long (−70,000 → +230,000 contracts-equiv) and bought 140,000 BA Dec-2025 $180 puts — real protection, but on one name, three business days before the broader selloff accelerated, and it didn't stop the QQQ call add nine days later. **Overall: caught leveraged and long, not de-risked.**

---

## UBER deep-dive: position vs. price, earnings marked

| Date | UBER close | Event |
|---|---|---|
| 2024-10-29 | $79.21 | OPEN LONG $78c (11/8 exp), 49,100 sh-equiv — opened 2 days before earnings, near what was then a local high |
| 2024-10-31 | $72.05 | **Earnings: −9.3% day-of.** No adjustment recorded; the $78c ran to its 11/8 expiry OTM |
| 2024-12-11 | $61.18 | *(no UBER position visible 11/9–12/10)* — Massive book opened at essentially the bottom of a 6-week, −24% slide from the 10/30 high ($79.43): OPEN $80c ×2 expiries (709,800 + 570,000→2,165,000 after same-day add), OPEN $85c (256,000→413,500), OPEN $75c (337,500), OPEN 32,000 shares, plus short $100c/$60p/$62.5p — first full spread structure |
| 2024-12-13 | $59.93 | ADD shares 32,000→65,000 @ $59.93 — the actual low of the move, bought within 2% of the bottom |
| 2025-01-02 – 01-27 | $63–69 | Continued adding $80c (up to 4,692,300 by 1/2), then **TRIMMED $80c by 74% on 1/27** (4,692,300→1,201,600) — the Jan 27 "DeepSeek" selloff day, ahead of earnings |
| 2025-02-03 – 02-12 | $67–79 | **Earnings 2/5: −7.6% day-of, +8.6% next-day.** Heavy restructuring straddling the print (see earnings table above) — new $72.5c/$75c/$80c/$85c longs, $62.5p/$75p/$80c/$85c/$100c/$105c shorts, shares added 65,000→95,000 through 2/12 as price recovered from $64.48 (2/5) to $79.35 (2/12) |
| 2025-02-18 | $81.49 | Local high for the position's life; continued adding calls into strength |
| 2025-02-24 – 03-04 | $75–76 | Trimming/closing shorter-dated calls as price pulled back ~8% off the 2/18 high |
| 2025-03-20 – 03-26 | $74–76 | ADD shares 100,000→210,000 @ $75.84 (3/22) — doubling the equity leg; continued rolling the June call book higher (adds at $80c/$85c) |
| 2025-04-02 | $74.50 | Last visible UBER snapshot — still net long ~210,000 shares plus a large multi-strike June/Aug call book, partially capped by short $100c/$105c |
| 2025-04-03 – 04-04 | $69.85 → $64.62 | **Tariff crash hits UBER too: −13.3% in 2 sessions.** No visibility into any UBER-specific action here — dataset ends 4/2 for legs, 4/5 for account total. |

The UBER book is the clearest example in this dataset of genuine buy-the-dip discipline (Dec 2024 entries within a couple percent of a 6-week low) combined with a large, actively-managed options overlay through an earnings print — and it's also the position most exposed, unhedged, when the dataset goes dark right as the April 2025 crash hits.

---

## Early era (Oct 2023 – Mar 2024): a brief note from post text

Position snapshots barely exist before Feb 2024, but the post archive (`reports/posts/@wTF_lifetime.md`) shows the same "add into pain" instinct already present with $SQ in Oct–Nov 2023: buying more on the way down ("And somehow I kept loading up on options, but $SQ kept going down" — 2023-10-2x), doubling down after a rough earnings reaction ("Sad ($SQ)"), and an admitted mis-click around the Nov 2023 SQ print ("Also I could have swore I had pressed the sell button after the $SQ earnings call but I guess it was the buy?" — 2023-11-07). This is qualitative, not counted in any statistic above — flagging it because it's consistent with the quantitative pattern found later (BA/RIVN dip-buys that kept bleeding, TSLA fade sized up into further pain).

---

## Methodology

- **Windowing**: for each `changes` row, `window_start` = the timestamp of the last prior post that tagged the same root ticker (any leg), `window_end` = the change's own timestamp. If no prior post tagged that root, it's flagged `first_observation` (37 of 414 events) and treated as a point-in-time read on `window_end`.
- **Qualifying subset**: `first_observation` OR `window_trading_days` ≤ 3 (computed off each ticker's own trading calendar). 283 of 410 priced events (69%) qualify; all headline tables use this subset unless noted. 375 events had both bounds known; of those, 248 (66%) were ≤3 trading days.
- **Anchor date**: the trading day on or before `window_end`'s calendar date.
- **20-day high/low**: trailing 20 trading days ending on the anchor day, inclusive.
- **Prior/forward returns**: close-to-close, 5/20 trading days back and 5/10/20 trading days forward from the anchor.
- **Baseline**: for each ticker, every trading day between 2024-02-07 and 2025-04-05 (the position-data window) scored the same way, then averaged; "baseline for the bullish/bearish set" is the equal-weighted average of the per-ticker baselines for the tickers that appear in that cohort.
- **Direction classification**: long stock/long call/short put = bullish; short stock/short call/long put = bearish. For OPEN/ADD, direction is the sign of the delta (the increment); for TRIM/CLOSED/EXPIRED, direction is the sign of the pre-existing position (`qty_before`); FLIP events use the post-flip sign.
- **Ticker mapping**: `SQ` root maps to price ticker `XYZ` (the company's post-rename symbol) per the task brief.
- **Excluded for missing price data**: CFLT (1 event), SPR (3 events) — not present in `data/prices/@wTF_prices.json`.
- Full per-event output: `reports/positions/lenses/@wTF_timing_events.json` (414 rows, one per change event).
- Scratch scripts used to build this: `/tmp/claude-1000/-home-mpha-projects-aftermath/5355fcb9-2520-4395-8e3e-6796abb45fed/scratchpad/*.py` (not part of the repo).
