# Funnel callouts parsed from public Telegram posts

14118 archived posts -> 8958 ticker records; 2600 are echoes (same contract, same channel or another one, same day) and are excluded below.

Unique option/spread calls: 4278 (2068 opens, 1471 closes, 739 mentions). Opens with a clean contract (strike, side, expiry, entry price all present): 1422.

Closes (any kind) that quote a result: 1714; positive: 1573/1714; mean quoted +114.2%. Quoted results are the channel's own claims, not verified fills.

## Option calls by channel
- t.me/bob_signalsfreealert: 546
- t.me/bzjzhzhzuzzu: 449
- t.me/bincofreealert: 359
- t.me/moonwalkertrades2: 339
- t.me/crestedgeroom: 330
- t.me/queen_free_entries: 286
- t.me/ajfreealart32: 278
- t.me/blockwave10: 224
- t.me/apextraderkoryphae: 191
- t.me/mrquickerfreealert: 181
- t.me/blackcardfreechannel: 174
- t.me/de_gainers_free_circle: 159

## Most-opened tickers
- $SPX: 274
- $SPY: 272
- $QQQ: 209
- $TSLA: 131
- $MU: 73
- $NVDA: 66
- $AMZN: 58
- $AAPL: 52
- $META: 48
- $IWM: 45
- $AMD: 32
- $SPCX: 31
- $GOOGL: 29
- $SNDK: 24
- $MSFT: 20

## Parse flags (all records)
- no_expiry: 2320
- result_claim: 2052
- duplicate_echo: 1874
- index_option: 1309
- recap_item: 1101
- cross_channel_echo: 726
- entry_unknown: 681
- entry_from_tail: 477
- pct_unlabelled: 432
- contract_unknown: 419
- price_update: 416
- list_item: 370
- posted_date_suspect: 359
- expiry_0dte_tag: 317
- tp_sl_present: 230
- ticker_list: 216
- recap_holding: 214
- no_strike: 213
- has_summary: 201
- unrealized_pct: 147
- alias_spxw: 132
- exit_price_only: 110
- expiry_far: 64
- crypto: 52
- hindsight: 52
- expiry_dte_tag: 36
- loss_no_pct: 34
- expiry_before_post: 26
- date_dmy: 26
- entry_implausible: 20
- spread: 18
- date_dmy_possible: 13
- pct_mismatch: 7
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
