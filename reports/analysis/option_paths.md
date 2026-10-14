# Callout option paths: what the contract did after the call

1627 option opens with a parseable contract; 1544 scored from captured 5-minute bars.
Intraday calls: first 30 minutes after the call. Daily callouts (before the open, after the close, weekends): the whole next regular session. Fill = open of the first bar at or after the post (or the session open). Bars are trade prints (no bid/ask, no slippage or fees).

## Coverage
- scored: 1544
- no_bars: 64
- day_view: 10
- unscorable: 9

## intraday (n=1527)

- median MFE +18%, median MAE -23%, median end-of-window return -6%, mean -2%
- ended green: 544/1527 [0.333, 0.381]

| rule | TP first | SL first | neither | mean return |
|---|---:|---:|---:|---:|
| +50% / -50% | 304 [0.18, 0.22] | 298 | 925 | -3.2% |
| +100% / -50% | 125 [0.069, 0.097] | 322 | 1080 | -2.9% |
| +30% / -30% | 425 [0.256, 0.301] | 521 | 581 | -2.8% |

## daily (n=17)

- median MFE +22%, median MAE -39%, median end-of-window return -22%, mean -22%
- ended green: 6/17 [0.173, 0.587]

| rule | TP first | SL first | neither | mean return |
|---|---:|---:|---:|---:|
| +50% / -50% | 5 [0.133, 0.531] | 7 | 5 | -7.5% |
| +100% / -50% | 2 [0.033, 0.343] | 7 | 8 | -4.3% |
| +30% / -30% | 6 [0.173, 0.587] | 9 | 2 | -5.3% |

## Day view (coarse, n=10): contracts called in roughly the last week, judged on the contract's daily bar

Daily bars are not time-ordered. For calls posted during the session the day's high or low may predate the post, so peak is an UPPER bound and drawdown a LOWER bound. Reference price = the entry the channel quoted (the open when none was quoted).

- quoted entry inside that day's traded range (±10%): 5/6 [0.436, 0.97]
- day closed above the reference: 4/10 [0.168, 0.687]; median close return -24%
- day high reached +50% (upper bound): 5/10 [0.237, 0.763]; +100%: 4/10
- day low reached -50% (lower bound on drawdown): 6/10 [0.313, 0.832]
- thin (day volume under 20 contracts): 2/10

- intraday calls: n=10, median close return -24%, day high >= +50%: 5/10

