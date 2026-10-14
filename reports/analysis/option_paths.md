# Callout option paths: what the contract did after the call

2846 option opens with a parseable contract; 2727 scored from captured 5-minute bars.
Intraday calls: first 30 minutes after the call. Daily callouts (before the open, after the close, weekends): the whole next regular session. Fill = open of the first bar at or after the post (or the session open). Bars are trade prints (no bid/ask, no slippage or fees).

## Coverage
- scored: 2727
- no_bars: 98
- unscorable: 11
- day_view: 10

## intraday (n=2696)

- median MFE +18%, median MAE -22%, median end-of-window return -6%, mean -2%
- ended green: 975/2696 [0.344, 0.38]

| rule | TP first | SL first | neither | mean return |
|---|---:|---:|---:|---:|
| +50% / -50% | 531 [0.182, 0.212] | 504 | 1661 | -3.2% |
| +100% / -50% | 213 [0.069, 0.09] | 541 | 1942 | -2.7% |
| +30% / -30% | 758 [0.265, 0.298] | 898 | 1040 | -2.6% |

## daily (n=31)

- median MFE +42%, median MAE -30%, median end-of-window return -17%, mean +44%
- ended green: 14/31 [0.292, 0.622]

| rule | TP first | SL first | neither | mean return |
|---|---:|---:|---:|---:|
| +50% / -50% | 14 [0.292, 0.622] | 10 | 7 | +4.8% |
| +100% / -50% | 10 [0.186, 0.499] | 10 | 11 | +19.2% |
| +30% / -30% | 16 [0.348, 0.68] | 13 | 2 | +2.9% |

## Day view (coarse, n=10): contracts called in roughly the last week, judged on the contract's daily bar

Daily bars are not time-ordered. For calls posted during the session the day's high or low may predate the post, so peak is an UPPER bound and drawdown a LOWER bound. Reference price = the entry the channel quoted (the open when none was quoted).

- quoted entry inside that day's traded range (±10%): 5/6 [0.436, 0.97]
- day closed above the reference: 4/10 [0.168, 0.687]; median close return -24%
- day high reached +50% (upper bound): 5/10 [0.237, 0.763]; +100%: 4/10
- day low reached -50% (lower bound on drawdown): 6/10 [0.313, 0.832]
- thin (day volume under 20 contracts): 2/10

- intraday calls: n=10, median close return -24%, day high >= +50%: 5/10

