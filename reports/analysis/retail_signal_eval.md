# Does AfterHour retail activity predict the next move?

Script: `research/retail_signal_eval.py` · numbers: `retail_signal_eval.json` · first run 2026-10-19, audited the same night

**Short answer: not proven. Every arm leans toward a fade (names trail after the crowd arrives), but once the comparison is matched fairly, no arm clears zero. The crowding arm comes closest: −2.6 percentage points over 20 sessions, with a 95% CI of −5.7 to +0.1. That is a lead to keep measuring, not a signal to ship.**

An earlier draft headlined a −5.7% "abnormal return" for attention. That was mostly **regression to the mean**. These traders post about names that have just had a strong run (trailing excess about 6% versus about 3.5% on random days), and a high trailing mean falls back on its own. Subtracting it makes any arm look like a fade. The matched comparison below removes that effect.

## Data
- 17,221 ticker-bearing posts from 42 tracked traders (`data/following`), 2023-04 → 2026-10.
- 953 tickers named on ≥3 days; 888 priced (yfinance daily, adjusted); 65 unpriceable and dropped.
- Returns ≤ −95% or ≥ +1000% over a window are dropped as bad microcap or reverse-split prints.
- Entry = open of the first session that starts after the post. Exit = close h−1 sessions later. Excess = minus SPY over the same window.

## Headline: arm vs placebo, matched on the trailing run (20 sessions)
Placebo = a random session of the same ticker, at least 20 sessions from any post, within ±250 sessions. Both sets are binned into quintiles of the ticker's trailing excess (entries 120 to 21 sessions before). Raw excess is compared within each bin and weighted by the arm's counts. CIs come from a bootstrap over 2-month blocks.

| arm | n | gap vs placebo (mean) | 95% CI | median gap |
|---|---|---|---|---|
| attention (any post naming the ticker) | 21,206 | −1.9 pp | −4.8 to +0.6 | −0.3 pp |
| **crowded** (≥3 traders within 3 sessions, first fire) | 1,159 | **−2.6 pp** | −5.7 to +0.1 | −0.3 pp |
| brag (Gain / Yolo tag) | 2,217 | +0.2 pp | −2.9 to +2.3 | +1.0 pp |
| directional bull (live `get_retail_sentiment` parser) | 215 | −2.2 pp | −6.4 to +0.1 | +1.6 pp |

The mean gaps lean negative, but the medians sit near zero. Whatever is there comes from the left tail (a minority of names that fall hard after the crowd arrives), not a broad drift.

## Secondary: the pre-window "abnormal" figures (flattered, shown for transparency)
| arm | n | mean | 95% CI | winsorized 1/99 | raw vs SPY |
|---|---|---|---|---|---|
| attention | 21,572 | −5.3% | −8.5 to −1.6 | −5.6% | +0.4% |
| crowded | 1,176 | −6.6% | −10.7 to −1.9 | −6.6% | −0.3% |
| directional bull | 217 | −7.3% | −11.0 to −2.4 | −6.9% | +0.1% |
| directional bear (signed: negative means the bear call was wrong) | 131 | −0.4% | −7.5 to +7.5 | −0.1% | — |
| placebo | 16,366 | +1.3% | −2.1 to +4.5 | +0.8% | +2.8% |

By year (attention, pre-window): 2023 −1.9% (n=93), 2024 +1.2%, 2025 −6.8% (CI excludes 0), 2026 −4.6% (CI −8.2 to +0.3). Only 2025 is clearly away from zero.

## Known biases (stated, not fixed)
- **Survivorship and selection:** the 42 traders were picked in 2026 from accounts still active and followed. The price source drops delisted names.
- These are mostly options posts. This measures the underlying, not the contract.
- The live sentiment parser fires on ~2% of this corpus (348 votes), so the directional arms are thin.
- Ticker extraction trusts the post's ticker field plus cashtags, and was not hand-audited for false positives.
- Real independence is about 18 two-month blocks, not 21k events.

## What would settle it
1. **Daily archive of `stonks.json` (owners / whale capital per ticker).** Only 2 snapshots exist today, so the positioning question (as opposed to posting) cannot be tested at all yet.
2. Re-run on the broad AfterHour population (`/social/feed` + `ah_archive`) rather than 42 followed accounts.
3. Out of sample: freeze this method and read it on posts from 2026-10-19 onward. Re-run monthly; the first meaningful read is about 2027-01. Do not tune the crowding threshold on the in-sample numbers above.
