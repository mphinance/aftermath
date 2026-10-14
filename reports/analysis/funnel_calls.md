# Funnel callouts parsed from public Telegram posts

25365 archived posts -> 14706 ticker records; 4232 are echoes (same contract, same channel or another one, same day) and are excluded below.

Unique option/spread calls: 7033 (3525 opens, 2097 closes, 1411 mentions). Opens with a clean contract (strike, side, expiry, entry price all present): 2493.

Closes (any kind) that quote a result: 2496; positive: 2343/2496; mean quoted +125.6%. Quoted results are the channel's own claims, not verified fills.

## Option calls by channel
- t.me/bob_signalsfreealert: 1265
- t.me/crestedgeroom: 817
- t.me/moonwalkertrades2: 762
- t.me/bzjzhzhzuzzu: 740
- t.me/de_gainers_free_circle: 552
- t.me/bincofreealert: 353
- t.me/apextraderkoryphae: 321
- t.me/blockwave10: 316
- t.me/queen_free_entries: 283
- t.me/ajfreealart32: 278
- t.me/mrquickerfreealert: 266
- t.me/blackcardfreechannel: 174

## Most-opened tickers
- $SPX: 491
- $SPY: 420
- $QQQ: 381
- $TSLA: 239
- $MU: 111
- $NVDA: 109
- $META: 91
- $AMZN: 82
- $IWM: 78
- $AAPL: 77
- $SNDK: 51
- $MSFT: 48
- $AMD: 42
- $GOOGL: 41
- $SPCX: 40

## Parse flags (all records)
- no_expiry: 3149
- result_claim: 3018
- duplicate_echo: 2943
- index_option: 2234
- cross_channel_echo: 1289
- recap_item: 1227
- entry_unknown: 1083
- price_update: 851
- contract_unknown: 775
- list_item: 773
- entry_from_tail: 710
- pct_unlabelled: 702
- posted_date_suspect: 483
- unrealized_pct: 394
- expiry_0dte_tag: 389
- ticker_list: 337
- has_summary: 310
- tp_sl_present: 292
- no_strike: 269
- alias_spxw: 256
- recap_holding: 230
- exit_price_only: 215
- expiry_far: 102
- hindsight: 98
- crypto: 55
- expiry_dte_tag: 48
- entry_implausible: 41
- loss_no_pct: 38
- spread: 38
- expiry_before_post: 35
- date_dmy: 26
- date_dmy_possible: 18
- pct_mismatch: 16
- spread_suspect: 2

## Sample opens
- 2026-10-14 t.me/ajfreealart32: $TSLA 365.0P exp None @ 1.78
- 2026-10-14 t.me/tradevisionst: $SPY 771.0P exp 2026-10-14 @ 0.51
- 2026-10-14 t.me/dannycwaynetradingroom: $SPY 775.0P exp None @ 1.04
- 2026-10-14 t.me/bzjzhzhzuzzu: $PENG 80.0C exp 2026-11-20 @ 5.6
- 2026-10-14 t.me/bzjzhzhzuzzu: $NVDA 222.5P exp 2026-10-14 @ 0.42
- 2026-10-14 t.me/queen_free_entries: $SPY 773.0C exp 2026-10-15 @ 2.33
- 2026-10-14 t.me/bzjzhzhzuzzu: $AAPL 350.0C exp 2026-10-16 @ 0.84
- 2026-10-14 t.me/trexfreecircle: $RPRX 60.0C exp 2026-10-16 @ 0.25
- 2026-10-14 t.me/bzjzhzhzuzzu: $MCD 250.0C exp 2026-11-20 @ 2.88
- 2026-10-14 t.me/bzjzhzhzuzzu: $SPCX 160.0C exp 2026-10-19 @ 0.8
- 2026-10-14 t.me/bzjzhzhzuzzu: $GL 170.0C exp 2026-10-16 @ 0.75
- 2026-10-14 t.me/mrquickerfreealert: $GL 170.0C exp 2026-10-16 @ 0.0
