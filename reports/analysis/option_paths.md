# Callout option paths: what the contract did after the call

1627 option opens with a parseable contract; 13 scored from captured 5-minute bars.
Intraday calls: first 30 minutes after the call. Daily callouts (before the open, after the close, weekends): the whole next regular session. Fill = open of the first bar at or after the post (or the session open). Bars are trade prints (no bid/ask, no slippage or fees).

## Coverage
- no_bars: 1331
- day_view: 283
- scored: 13

## intraday (n=13)

- median MFE +25%, median MAE -32%, median end-of-window return +4%, mean +7%
- ended green: 8/13 [0.355, 0.823]

| rule | TP first | SL first | neither | mean return |
|---|---:|---:|---:|---:|
| +50% / -50% | 1 [0.014, 0.333] | 3 | 9 | -2.2% |
| +100% / -50% | 0 [0, 0.228] | 3 | 10 | -8.4% |
| +30% / -30% | 2 [0.043, 0.422] | 7 | 4 | -11.7% |

## Day view (coarse, n=283): contracts called in roughly the last week, judged on the contract's daily bar

Daily bars are not time-ordered. For calls posted during the session the day's high or low may predate the post, so peak is an UPPER bound and drawdown a LOWER bound. Reference price = the entry the channel quoted (the open when none was quoted).

- quoted entry inside that day's traded range (±10%): 213/221 [0.93, 0.982]
- day closed above the reference: 93/283 [0.277, 0.385]; median close return -22%
- day high reached +50% (upper bound): 143/283 [0.447, 0.563]; +100%: 98/283
- day low reached -50% (lower bound on drawdown): 149/283 [0.468, 0.584]
- thin (day volume under 20 contracts): 21/283

- intraday calls: n=283, median close return -22%, day high >= +50%: 143/283

