# Funnel callouts parsed from public Telegram posts

2886 archived posts -> 1948 ticker records; 401 are echoes (same contract, same channel or another one, same day) and are excluded below.

Unique option/spread calls: 958 (494 opens, 337 closes, 127 mentions). Opens with a clean contract (strike, side, expiry, entry price all present): 342.

Closes (any kind) that quote a result: 411; positive: 369/411; mean quoted +97.6%. Quoted results are the channel's own claims, not verified fills.

## Option calls by channel
- t.me/bob_signalsfreealert: 137
- t.me/blackcardfreechannel: 120
- t.me/bzjzhzhzuzzu: 86
- t.me/ajfreealart32: 69
- t.me/trexfreecircle: 51
- t.me/vertexpublic: 50
- t.me/axisalgorithmictrade: 46
- t.me/crestedgeroom: 44
- t.me/bincofreealert: 41
- t.me/de_gainers_free_circle: 38
- t.me/queen_free_entries: 36
- t.me/blockwave10: 35

## Most-opened tickers
- $SPY: 75
- $SPX: 56
- $QQQ: 43
- $AMZN: 22
- $NVDA: 19
- $TSLA: 17
- $MU: 13
- $AAPL: 12
- $SPCX: 10
- $IWM: 9
- $GOOGL: 9
- $META: 7
- $AMD: 7
- $AVGO: 7
- $MSFT: 7

## Parse flags (all records)
- result_claim: 480
- no_expiry: 412
- duplicate_echo: 288
- recap_item: 219
- index_option: 212
- posted_date_suspect: 185
- entry_from_tail: 162
- entry_unknown: 136
- contract_unknown: 136
- cross_channel_echo: 113
- ticker_list: 96
- recap_holding: 92
- expiry_0dte_tag: 91
- pct_unlabelled: 87
- tp_sl_present: 71
- no_strike: 60
- expiry_far: 38
- unrealized_pct: 37
- price_update: 27
- has_summary: 26
- list_item: 25
- exit_price_only: 22
- expiry_dte_tag: 15
- loss_no_pct: 13
- date_dmy: 11
- spread: 11
- hindsight: 10
- alias_spxw: 10
- crypto: 8
- entry_implausible: 6
- expiry_before_post: 3
- date_dmy_possible: 2
- pct_mismatch: 1
- spread_suspect: 1

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
