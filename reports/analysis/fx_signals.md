# FX / gold / index signal scoring (public Telegram posts vs the real tape)

Generated 2026-10-14 by `tg_fx_signals.py` from `data/telegram_funnel/posts_archive.jsonl`. Analysis of public posts, not an accusation. Numbers first; every rate carries its sample size. Horizon 24h, touch window 4h, basis mode `auto`.

## 1. Coverage funnel

Stage order (each stage counts what survives the previous one): bulk-timestamp exclusion comes before the repost dedupe so a backfill dump can never be the "first" copy that survives. Typo detection needs the market price, so it runs after pricing.

| stage | n | note |
|---|---:|---|
| posts in archive (all channels) | 13478 | 27 channels |
| posts naming an instrument and a side | 386 | includes 107 with no SL/TP (heads-up posts, analysis, result claims), not scored |
| signal-shaped (instrument + side + SL or TP) | 279 | |
| after valid-date filter | 224 | 55 dropped: (channel, timestamp) shared by 6 or more posts. Many are same-second repost bursts: only 16 distinct signals exist solely inside those groups (see section 6 for the groups) |
| after repost dedupe | 122 | 102 reposts dropped (same channel/instrument/side/entry/SL/TPs within 60 min of the previous copy) |
| with both SL and a TP | 113 | 9 dropped: missing SL or TP |
| priced (Yahoo 5m bar at post time) | 108 | 5 older than Yahoo's ~60-day 5m history, 0 no symbol data, 0 no bar within 600s of the post (market closed) |
| not flagged as price typo | 101 | 7 flagged typo_* or sl_distance_implausible, reported not scored |
| filled (market or touch) | 63 | not filled: cancelled_tp_before_fill 30, cancelled_sl_before_fill 6, not_filled_in_window 2 |
| scored (full horizon of data, valid levels) | 63 | market-fill variant 51, touch-fill variant 12. Excluded after fill: 0 |

Non-signal posts (no instrument, no side, or no levels) are not rows; only `data/telegram_funnel/fx_claims.jsonl` keeps the follow-up claims among them (93 claims captured, 3 of them from bulk-timestamp posts).

## 2. Instruments seen

| instrument | posts naming it (+side) | with SL/TP | scored | pip convention | Yahoo symbol used |
|---|---:|---:|---:|---|---|
| XAUUSD | 290 | 214 | 55 | 0.1 | GC=F |
| US30 | 25 | 24 | 2 | 1 | YM=F |
| BTCUSD | 23 | 2 | 1 | unsupported | BTC-USD |
| XRPUSD | 9 | 7 | 0 | unsupported | none |
| SOLUSD | 9 | 4 | 0 | unsupported | none |
| ETHUSD | 7 | 5 | 0 | unsupported | ETH-USD |
| NAS100 | 5 | 5 | 3 | 1 | NQ=F |
| FX:GBPCHF | 3 | 3 | 0 | 0.0001 | GBPCHF=X |
| HBARUSD | 2 | 2 | 0 | unsupported | none |
| MTLUSD | 2 | 2 | 0 | unsupported | none |
| SUIUSD | 2 | 2 | 0 | unsupported | none |
| ONGUSD | 2 | 2 | 0 | unsupported | none |
| LINKUSD | 2 | 2 | 0 | unsupported | none |
| AVAXUSD | 1 | 1 | 1 | unsupported | AVAX-USD |
| FX:EURUSD | 1 | 1 | 0 | 0.0001 | none |
| FX:USDCAD | 1 | 1 | 1 | 0.0001 | USDCAD=X |
| ACTUSD | 1 | 1 | 0 | unsupported | none |
| DOGEUSD | 1 | 1 | 0 | unsupported | none |

## 3. Yahoo symbol validation

For each candidate symbol: median absolute percent gap between the stated entry (zone midpoint) of market-order signals and the candidate's close at post time (gaps over 3% excluded as typos), coverage = matched / signals with a stated entry, and the signed price gap (entry minus tape) split by side. The pick is the lowest median gap among candidates with at least 80% of the best coverage. `const offset` = mean of the buy and sell medians, so the channels' habit of posting buy zones below and sell zones above market cancels. Futures carry decays toward expiry, so the headline mode (`auto`) instead fits a Theil-Sen line through per-day balanced medians (needs 5 days with both sides) and adds it to the candidate's bars; `gap after const / fit` is the remaining median gap, a check that the adjustment is doing something. Zone placement noise keeps that residual above zero.

| instrument | candidate | data | range | n entries | matched | coverage | median abs gap (raw) | signed median buys / sells | const offset | gap after const | time-varying fit (price/day, days used) | gap after fit | picked |
|---|---|---|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|
| AVAXUSD | AVAX-USD | 5m | 2026-08-16 to 2026-10-14 10:30 | 1 | 1 | 100% | 0.937% | - / 0.09 | 0.09 | 0.000% | not fitted (0 days) | - | yes |
| BTCUSD | BTC-USD | 5m | 2026-08-16 to 2026-10-14 10:30 | 1 | 1 | 100% | 2.196% | -1744.31 / - | -1744.31 | 0.000% | not fitted (0 days) | - | yes |
| ETHUSD | ETH-USD | 5m | 2026-08-16 to 2026-10-14 10:37 | 3 | 2 | 67% | 0.351% | - / -8.64 | -8.64 | 0.275% | not fitted (0 days) | - | yes |
| FX:GBPCHF | GBPCHF=X | 5m | 2026-07-22 to 2026-10-14 10:30 | 0 | 0 | - | - | - / - | - | - | not fitted (0 days) | - | yes |
| FX:USDCAD | USDCAD=X | 5m | 2026-07-22 to 2026-10-14 10:30 | 0 | 0 | - | - | - / - | - | - | not fitted (0 days) | - | yes |
| NAS100 | ^NDX | 5m | 2026-07-21 to 2026-10-13 20:00 | 3 | 2 | 67% | 0.059% | - / 2.65 | 2.65 | 0.059% | not fitted (0 days) | - |  |
| NAS100 | NQ=F | 5m | 2026-08-05 to 2026-10-14 10:20 | 3 | 3 | 100% | 0.925% | - / -282.75 | -282.75 | 0.019% | not fitted (0 days) | - | yes |
| US30 | ^DJI | 5m | 2026-07-21 to 2026-10-13 20:00 | 11 | 4 | 36% | 0.222% | 21.60 / 70.24 | 45.92 | 0.132% | not fitted (0 days) | - |  |
| US30 | YM=F | 5m | 2026-08-05 to 2026-10-14 10:20 | 11 | 10 | 91% | 0.634% | -384.00 / 12.00 | -186.00 | 0.380% | not fitted (0 days) | - | yes |
| XAUUSD | XAUUSD=X | none (no data from Yahoo, HTTP 404) | | 85 | | | | | | | | | |
| XAUUSD | GC=F | 5m | 2026-08-05 to 2026-10-14 10:20 | 85 | 84 | 99% | 0.741% | -34.40 / -30.07 | -32.24 | 0.108% | 0.513/day (13) | 0.098% | yes |

Cash indices (^DJI, ^NDX, ^N225) only print during their own session, so they cover far fewer posts than the futures; that is why coverage gates the pick. Futures differ from the spot CFD the channel trades by a basis (carry); the offset above is that estimate, not a measured spread.

## 4. Results

Outcome definitions: **TP1 hit** = TP1 touched before the stop; **TP2+** = TP2 touched before the stop (denominator: signals with two or more TPs); **SL first** = stop touched before TP1; **unresolved** = neither within the horizon. Mean R columns include unresolved trades marked to the last close. Expectancy@TP1 uses resolved trades only (TP1 = win at its stated R, stop = -1R); the break-even TP1 rate is 1/(1 + average win R), so a hit rate below it loses money before costs. Spread and slippage are ignored, which flatters every number here.

### 4a. Market-fill variant (entry now / missing / market inside the entry zone)

**By instrument**

| instrument | n | TP1 hit (95% CI) | TP2+ | SL first | unresolved | mean R exit@TP1 | mean R exit@last TP | expectancy@TP1, resolved only | avg win R / break-even TP1 rate | median min to 1st event |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---:|
| XAUUSD | 44 | 52% (38%-66%) | 30% (13/43) | 48% | 0% | -0.17 | -0.18 | -0.17 (n=44) | 0.59 / 63% | 44 |
| NAS100 | 3 | 33% (6%-79%) | 0% (0/3) | 67% | 0% | -0.61 | -1.00 | -0.61 (n=3) | 0.18 / 85% | 19 |
| BTCUSD | 1 | 0% (0%-79%) | n/a | 100% | 0% | -1.00 | -1.00 | -1.00 (n=1) | - / - | 89 |
| AVAXUSD | 1 | 0% (0%-79%) | n/a | 100% | 0% | -1.00 | -1.00 | -1.00 (n=1) | - / - | 360 |
| US30 | 1 | 100% (21%-100%) | 100% (1/1) | 0% | 0% | 0.48 | 4.83 | 0.48 (n=1) | 0.48 / 67% | 15 |
| FX:USDCAD | 1 | 100% (21%-100%) | 100% (1/1) | 0% | 0% | 0.35 | 0.85 | 0.35 (n=1) | 0.35 / 74% | 77 |
| **all** | 51 | 51% (38%-64%) | 31% (15/48) | 49% | 0% | -0.20 | -0.15 | -0.20 (n=51) | 0.56 / 64% | 43 |

**By channel**

| channel | n | TP1 hit (95% CI) | TP2+ | SL first | unresolved | mean R exit@TP1 | mean R exit@last TP | expectancy@TP1, resolved only | avg win R / break-even TP1 rate | median min to 1st event |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---:|
| t.me/stockmarketvault | 50 | 52% (39%-65%) | 31% (15/48) | 48% | 0% | -0.19 | -0.13 | -0.19 (n=50) | 0.56 / 64% | 40 |
| t.me/dennis1btc1 | 1 | 0% (0%-79%) | n/a | 100% | 0% | -1.00 | -1.00 | -1.00 (n=1) | - / - | 89 |
| **all** | 51 | 51% (38%-64%) | 31% (15/48) | 49% | 0% | -0.20 | -0.15 | -0.20 (n=51) | 0.56 / 64% | 43 |

### 4b. Fill-on-touch variant (entry_not_at_market; fill within 4h at the nearest entry edge)

These are limit/stop-style entries away from the market at post time. Not pooled with 4a.

**By instrument**

| instrument | n | TP1 hit (95% CI) | TP2+ | SL first | unresolved | mean R exit@TP1 | mean R exit@last TP | expectancy@TP1, resolved only | avg win R / break-even TP1 rate | median min to 1st event |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---:|
| XAUUSD | 11 | 36% (15%-65%) | 20% (2/10) | 64% | 0% | -0.39 | -0.41 | -0.39 (n=11) | 0.67 / 60% | 48 |
| US30 | 1 | 100% (21%-100%) | 100% (1/1) | 0% | 0% | 0.23 | 3.85 | 0.23 (n=1) | 0.23 / 81% | 66 |
| **all** | 12 | 42% (19%-68%) | 27% (3/11) | 58% | 0% | -0.34 | -0.05 | -0.34 (n=12) | 0.58 / 63% | 57 |

**By channel**

| channel | n | TP1 hit (95% CI) | TP2+ | SL first | unresolved | mean R exit@TP1 | mean R exit@last TP | expectancy@TP1, resolved only | avg win R / break-even TP1 rate | median min to 1st event |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---:|
| t.me/stockmarketvault | 12 | 42% (19%-68%) | 27% (3/11) | 58% | 0% | -0.34 | -0.05 | -0.34 (n=12) | 0.58 / 63% | 57 |
| **all** | 12 | 42% (19%-68%) | 27% (3/11) | 58% | 0% | -0.34 | -0.05 | -0.34 (n=12) | 0.58 / 63% | 57 |

Touch-variant signals that reached the walk stage: 50. Outcome of the entry attempt: cancelled_tp_before_fill 30, scored 12, cancelled_sl_before_fill 6, not_filled_in_window 2.

### 4c. Sensitivity to the futures-to-spot basis (all instruments pooled, then gold alone)

The basis estimate is the weakest input: on gold it is about 30 dollars against a typical stop of 10. Each row rescores the same posts with a different tape shift; the 0.07% rows are a plausible estimation error (the residual gap after the fit in section 3 is about 0.1%). Signals move between the market and touch variants when the shift changes, so n differs by row. `auto` is the headline (time-varying fit).

| basis mode | gold: n market, TP1 hit, R@TP1, R@last | gold: n touch, TP1 hit, R@TP1, R@last | all instruments: n market, TP1 hit, R@TP1 | skipped for typo flag |
|---|---|---|---|---:|
| auto (time-varying, headline) | n=44, 52%, -0.17, -0.18 | n=11, 36%, -0.39, -0.41 | n=51, 51%, -0.20 | 7 |
| const offset | n=42, 45%, -0.29, -0.10 | n=14, 36%, -0.32, -0.14 | n=49, 45%, -0.31 | 7 |
| auto shifted down 0.07% of price (about 3 dollars on gold) | n=47, 55%, -0.10, -0.30 | n=8, 38%, -0.34, -0.49 | n=54, 54%, -0.15 | 7 |
| auto shifted up 0.07% of price | n=45, 44%, -0.27, -0.16 | n=9, 33%, -0.46, 0.05 | n=51, 45%, -0.28 | 7 |
| none (raw futures) | n=0 | n=0 | n=3, 67%, -0.18 | 7 |

Ambiguous bars (SL and a TP in the same 5m bar, counted as SL): 0 of 63 scored (0%).

## 5. t.me/stockmarketvault by week

Week = Monday start (UTC). Market-fill variant; the last week is partial (archive ends 2026-10-13; same-timestamp groups are excluded). Small n per week: read the CI, not the point estimate.

| week | distinct signals posted (valid dates, deduped) | scored (market) | TP1 hit (95% CI) | TP2+ | SL first | unresolved | mean R exit@TP1 | mean R exit@last TP | scored (touch) | touch TP1 hit |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| 2026-09-14 | 12 | 3 | 67% (21%-94%) | 50% (1/2) | 33% | 0% | -0.06 | 0.52 | 1 | 0% (n=1) |
| 2026-09-21 | 33 | 19 | 53% (32%-73%) | 32% (6/19) | 47% | 0% | -0.10 | -0.07 | 3 | 33% (n=3) |
| 2026-09-28 | 25 | 13 | 62% (36%-82%) | 38% (5/13) | 38% | 0% | -0.15 | -0.01 | 1 | 0% (n=1) |
| 2026-10-05 | 31 | 12 | 50% (25%-75%) | 27% (3/11) | 50% | 0% | -0.19 | -0.29 | 7 | 57% (n=7) |
| 2026-10-12 | 3 | 3 | 0% (0%-56%) | 0% (0/3) | 100% | 0% | -1.00 | -1.00 | 0 | - |

Split in half by time (market variant, n=50): first half n=25 TP1 52%, mean R@TP1 -0.15; second half n=25 TP1 52%, mean R@TP1 -0.23.

## 6. How t.me/stockmarketvault content changed over time

Archive window for this channel: 2026-09-17 to 2026-10-13, 720 posts. Categories are keyword heuristics on the post text: `fx_signal` = parsed instrument, side and levels; `fx_chatter_analysis` = gold/pips/SL/TP words without a full signal (results, analysis, stop moves); `stock_callout` = cashtags or option strings; `promo_chat` = deposit/withdrawal/investment/VIP wording. The last column counts posts whose exact timestamp is shared by 6 or more posts (their dates are not trusted); those posts are also counted in their content category.

| week | fx_signal | fx_chatter_analysis | stock_callout | promo_chat | other | total | of which in same-timestamp groups |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-09-14 | 22 | 7 | 0 | 16 | 20 | 65 | 14 |
| 2026-09-21 | 66 | 29 | 0 | 11 | 38 | 144 | 21 |
| 2026-09-28 | 83 | 40 | 0 | 22 | 70 | 215 | 56 |
| 2026-10-05 | 55 | 32 | 0 | 19 | 37 | 143 | 28 |
| 2026-10-12 | 23 | 7 | 63 | 8 | 52 | 153 | 142 |

Same-timestamp groups (SV, 6 or more posts at one exact second). Composition shows what each group is: a repost burst of one or two signals, chat lines, or the stock-ticker dump.

| timestamp (UTC) | posts | fx signal-shaped | stock/option text | other | first and last id |
|---|---:|---:|---:|---:|---|
| 2026-09-20 11:31:06 | 7 | 0 | 0 | 7 | 2426 to 2432 |
| 2026-09-20 11:33:04 | 7 | 0 | 0 | 7 | 2433 to 2439 |
| 2026-09-21 06:28:59 | 6 | 2 | 0 | 4 | 2441 to 2447 |
| 2026-09-22 17:22:18 | 7 | 0 | 0 | 7 | 2518 to 2524 |
| 2026-09-27 18:31:31 | 8 | 0 | 0 | 8 | 2634 to 2641 |
| 2026-09-28 06:10:15 | 8 | 6 | 0 | 2 | 2646 to 2653 |
| 2026-09-29 09:06:05 | 8 | 2 | 0 | 6 | 2685 to 2692 |
| 2026-09-29 09:06:06 | 9 | 0 | 0 | 9 | 2693 to 2701 |
| 2026-10-01 14:50:36 | 15 | 15 | 0 | 0 | 2796 to 2810 |
| 2026-10-02 17:59:05 | 6 | 0 | 0 | 6 | 2873 to 2878 |
| 2026-10-03 21:00:54 | 10 | 0 | 0 | 10 | 2886 to 2895 |
| 2026-10-05 12:50:04 | 8 | 0 | 0 | 8 | 2931 to 2938 |
| 2026-10-06 09:40:17 | 7 | 0 | 0 | 7 | 2970 to 2976 |
| 2026-10-07 06:11:06 | 6 | 0 | 0 | 6 | 2992 to 2997 |
| 2026-10-10 13:35:22 | 7 | 0 | 0 | 7 | 3059 to 3065 |
| 2026-10-12 09:28:52 | 16 | 7 | 0 | 9 | 3071 to 3088 |
| 2026-10-13 06:56:16 | 17 | 13 | 0 | 4 | 3093 to 3109 |
| 2026-10-13 09:53:04 | 19 | 0 | 16 | 3 | 3113 to 3131 |
| 2026-10-13 09:53:05 | 25 | 0 | 10 | 15 | 3132 to 3156 |
| 2026-10-13 09:53:06 | 32 | 0 | 24 | 8 | 3157 to 3188 |
| 2026-10-13 09:53:07 | 20 | 0 | 6 | 14 | 3189 to 3212 |
| 2026-10-13 18:10:16 | 13 | 0 | 7 | 6 | 3214 to 3226 |

- Parsed FX/gold/index signals with levels: first post **2026-09-18T06:29:50+00:00**, last post **2026-10-13T07:16:06+00:00** UTC (249 posts, 19 distinct signal-days).
- Stock-ticker / option-style posts (cashtags, call/put strings): 63 posts on 1 days; first 2026-10-13T09:53:04+00:00, last 2026-10-13T18:10:16+00:00. 63 of them sit in same-timestamp groups, so for those the archive cannot say when they were originally posted; the burst on 2026-10-13 around 09:53 UTC is where the bulk of them are.
- Reading: the channel's sustained output from the start of the archive until 2026-10-13 morning is gold/index/FX signals with a few chat and promo lines; stock and options callouts appear in volume only in the 2026-10-13 dump and after. Whether the switch is a genuine change of format or a replay of older content cannot be settled from this archive.

## 7. Channel follow-up claims (not scored)

93 claim-like posts (90 outside bulk timestamps) saved to `data/telegram_funnel/fx_claims.jsonl`: secure_be 53, sl_hit 24, pips 10, tp_hit 9, running 8. These are the channel's own words ("Tp1 done", "+180 pips", "running 110+ pips") without an attached trade id, so they cannot be matched to one signal yet. Next step if wanted: join each claim to the most recent unresolved signal before it and compare the claimed pips with the tape.

stockmarketvault stated pip figures outside bulk timestamps: n=7, median 180, max 590.

## 8. What this says

- **Sample**: 51 signals scored in the market-fill variant (50 from t.me/stockmarketvault) and 12 in the touch variant, out of the funnel in section 1. Everything below is that sample, one month long.
- **Hit rate vs payoff**: market variant TP1 touched before the stop in 51% of 51 signals (CI 38%-64%), stop first in 49%, unresolved 0%. Average winning TP1 is 0.56 R, so the break-even TP1 rate is 64%. Mean R exit@TP1 is -0.20 and exit@last TP is -0.15 (before spread).
- **Payoff shape**: TP1 sits on average 0.56 R from the fill while the stop is 1 R away, so a TP1 exit needs a hit rate of at least 64% to break even before costs.
- **Touch variant** (limit-style entries away from market, n=12): TP1 42%, mean R exit@TP1 -0.34, exit@last TP -0.05. Not comparable with the market variant.
- **Claims vs tape**: the channel's own results posts ("+180 pips", "5 TPs hit all at once") are listed in `fx_claims.jsonl` but not yet joined to individual signals; the scored numbers above are what the tape supports for the signals as posted.
- **Robustness to the basis estimate**: across the four basis modes in 4c the market-variant TP1 hit rate runs 45% to 54% and mean R exit@TP1 runs -0.31 to -0.15 (n 49 to 54). The sign of the mean R is the same in every mode; the size is not stable, because a few dollars of tape shift moves gold signals between fill variants and flips close calls on 10-dollar stops.
- **Does stockmarketvault change over time?** First half of the scored signals (n=25) TP1 52%, mean R@TP1 -0.15; second half (n=25) TP1 52%, mean R@TP1 -0.23. Weekly cells hold from a handful to about twenty signals each, with CIs spanning 30 points or more, so a drift of this size cannot be separated from noise. What did change is volume and format: see section 6.

- This is a descriptive check of public posts under stated assumptions, not a finding about intent.

## 9. Assumptions and known gaps

- Fill model: the market variant fills at the close of the 5m bar containing the post, which can be up to 5 minutes after the post. Real fills on a CFD broker carry spread (gold typically 2 to 3 dollars against stops of about 10) and slippage; both ignored here, so every R figure is optimistic.
- Tolerance: a stated entry or zone counts as at-market when the market is inside it widened by 0.25 x |entry mid - SL|. Wider tolerance moves signals from the touch variant to the market variant.
- Pips: gold 1 pip = 0.10, indices 1 point, FX 0.0001 (JPY 0.01). Pip-denominated TPs (for example `TP: 50/100PIPS`) are measured from the fill price; signals using them carry `tp_pips_assumed`. If the channel meant 1 pip = 1.00 on gold, those targets are 10x farther than scored.
- Same-bar ambiguity: SL wins over TP inside one 5m bar. TP1 and TP2 in the same bar are both credited. On the fill bar of a touch-variant signal only the SL is credited.
- TP order: targets are sorted by distance from the fill, so `tp1` is the nearest even if the channel listed it differently. Targets already passed or on the wrong side at fill are dropped and flagged `tp_wrong_side_or_passed`. TPs written `open` are ignored.
- No management: no break-even move, no partial closes, no trailing. Channels often tell followers to move to break-even after TP1; that rule is not modelled, so the exit@last TP column is a harsh all-or-nothing reading and the exit@TP1 column is the generous one.
- Futures proxies (GC=F, YM=F, NQ=F) stand in for spot CFDs because Yahoo has no XAUUSD=X data; the estimated basis is applied in `auto` mode; 4c shows const, shifted and no-basis results. A basis error of a few dollars is comparable to the 10-dollar stops, which is the main uncertainty in this report.
- The archive holds posts, not edits or deletions. A signal the channel later deleted or amended is scored as posted. Reposts within 60 minutes are collapsed to the first copy; a changed level creates a new signal.
- Horizon: trades whose 24h window runs past the last Yahoo bar are excluded (`horizon_incomplete`), not scored as open.
- Posts with no stated entry and no numbers ("GOLD SELL NOW" alone) have no SL or TP and are not scored. Claims text is not matched to signals yet.
- Sample sizes are small (tens of signals per instrument, one month, one dominant channel). Confidence intervals are Wilson 95% on the TP1 hit rate only; treat everything else as descriptive.

