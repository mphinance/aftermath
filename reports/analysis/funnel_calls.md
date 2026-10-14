# Funnel callouts parsed from public Telegram posts

13478 archived posts -> 8571 ticker records; 2518 are echoes (same contract, same channel or another one, same day) and are excluded below.

Unique option/spread calls: 4125 (1993 opens, 1399 closes, 733 mentions). Opens with a clean contract (strike, side, expiry, entry price all present): 1377.

Closes (any kind) that quote a result: 1621; positive: 1490/1621; mean quoted +112.1%. Quoted results are the channel's own claims, not verified fills.

## Option calls by channel
- t.me/bob_signalsfreealert: 543
- t.me/bzjzhzhzuzzu: 442
- t.me/bincofreealert: 359
- t.me/moonwalkertrades2: 339
- t.me/crestedgeroom: 327
- t.me/queen_free_entries: 284
- t.me/ajfreealart32: 277
- t.me/blockwave10: 226
- t.me/apextraderkoryphae: 191
- t.me/mrquickerfreealert: 180
- t.me/blackcardfreechannel: 174
- t.me/de_gainers_free_circle: 154

## Most-opened tickers
- $SPX: 273
- $SPY: 268
- $QQQ: 207
- $TSLA: 127
- $MU: 73
- $NVDA: 62
- $AMZN: 56
- $AAPL: 50
- $META: 48
- $IWM: 45
- $AMD: 32
- $SPCX: 29
- $GOOGL: 29
- $SNDK: 24
- $MSFT: 20

## Parse flags (all records)
- no_expiry: 2245
- result_claim: 1952
- duplicate_echo: 1801
- index_option: 1294
- recap_item: 1033
- cross_channel_echo: 717
- entry_unknown: 615
- entry_from_tail: 464
- pct_unlabelled: 414
- price_update: 411
- contract_unknown: 389
- list_item: 370
- posted_date_suspect: 330
- expiry_0dte_tag: 312
- tp_sl_present: 224
- recap_holding: 214
- ticker_list: 207
- no_strike: 204
- has_summary: 201
- unrealized_pct: 144
- alias_spxw: 132
- exit_price_only: 108
- expiry_far: 64
- crypto: 50
- hindsight: 49
- expiry_dte_tag: 33
- loss_no_pct: 30
- expiry_before_post: 26
- date_dmy: 26
- entry_implausible: 19
- spread: 18
- date_dmy_possible: 13
- pct_mismatch: 5
- spread_suspect: 2

## Sample opens
- 2026-10-13 t.me/tradevisionst: $SPY 777.0P exp 2026-10-13 @ 0.68
- 2026-10-13 t.me/trexfreecircle: $GRMN 290.0C exp 2026-10-16 @ 0.3
- 2026-10-13 t.me/trexfreecircle: $GRMN 290.0C exp 2026-10-16 @ None
- 2026-10-13 t.me/apextraderkoryphae: $IDA 140.0C exp 2026-10-16 @ 0.4
- 2026-10-13 t.me/dannycwaynetradingroom: $IDA 140.0C exp 2026-10-16 @ 0.35
- 2026-10-13 t.me/stockmarketvault: $SPY 778.83P exp 2026-10-13 @ None
- 2026-10-13 t.me/trexfreecircle: $TX 60.0C exp 2026-10-16 @ 0.4
- 2026-10-13 t.me/trexfreecircle: $REPX 50.0C exp 2026-10-16 @ 0.2
- 2026-10-13 t.me/trexfreecircle: $REPX 50.0C exp 2026-10-16 @ None
- 2026-10-13 t.me/crestedgeroom: $AAPL 347.5C exp 2026-10-16 @ 1.35
- 2026-10-13 t.me/queen_free_entries: $NVDA 10.0C exp None @ None
- 2026-10-13 t.me/bzjzhzhzuzzu: $NVDA 230.0C exp 2026-10-19 @ 2.65
