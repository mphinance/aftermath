# calls.jsonl data-quality notes (found while scoring, 2026-10-14)

1. Closes tagged as opens (2 of 83 option opens): `axisalgorithmictrade/191` ("Closed 150 $SPX 7800C ... Gain: +23.7%") and `CrestEdgeRoom/2434` ("Closed 1 $MU 1000C ... Gain: +23.6%"). The close post also contains the original "Opened ..." line further down the text, which probably triggers the open match. Close should win when the post starts with Closed/Exit/Sold.
2. Leading date misread as no expiry: `alphasyndicate11/365` "6/12 $TGT 133c @.16" has expiry null; the "6/12" is the expiry (post date 6/9). Scored as same-day 0DTE, which is wrong. Date-before-ticker form is not handled.
3. Wrong expiry year/order: `ApextraderKoryphae/1656` "$AMZN 252.5P 09/10 @.38" posted 2026-10-08 gives expiry 2026-09-10 (before the post). Likely 10/09 (DD/MM typo by the channel) or a stale date; parser should flag expiry < posted rather than emit it.
4. Entry price missing when labelled: `CrestEdgeRoom/2446` "$AAPL 347.5C 10/16 ... Entry Price: $1.35" has entry_price null.
5. Multi-contract posts misassign entry: `bincofreealert/5957` "BTO $QQQ 10/13 741p .69 / BTO $SPX 10/13 7785p @ 2.5" gives the QQQ put entry 2.5 (should be .69). The bare ".69" with no "@" is not captured, and the next "@" price is attached to the wrong ticker.
6. Same contract, different entries in one channel/day: BlockWave10 SPX 7805C 10/09 at $3.80 (14:35) and $4.90 (15:00); bzjzhzhzuzzu QQQ 746C 10/13 at $0.61 then $0.49 ("TRADE UPDATE"). Distinct fills, but the requested dedupe key (no entry) merges them to the first. UPDATE posts may be adds or re-quotes, not new opens.
7. Heavy reposts: tradevisionst posted MU 1010C 10/12 @ $0.43 eight times in 40 min, GOOGL 12/10 three times, DannyCWayne IDA 140C three times, in one case with different entry (0.40 vs 0.35 across channels). 83 open records collapse to 58 groups.
8. Null expiry on non-0DTE-labelled posts: e.g. "$SPY 745C @.32 lotto", "$AMZN 257.5C @.12", "$TSLA 387.50C @ $1.84", "$SPY 778 Call @ 0.81" have no date. Treated as same-day by spec; unverifiable, and `tradevisionst/323` "0DTE" is the only explicit tag. A channel that meant next-day or weekly would be mis-scored.
9. Close records are `kind: stock` with `side/strike` null even when the close is of an option (e.g. alphasyndicate11/366 "$TGT @.30 | +120%"), so closes cannot be matched to their open. A close-to-open link (same channel, ticker, nearest earlier open) is needed for a trade-level quoted-vs-real comparison.
10. Unusual underlying symbols that scored fine but are worth a sanity check: SPCX (165C 10/9, ticker resolves on Yahoo), MU strikes 1000-1100 (MU ~$990-1090 in this tape, plausible). Not-yet-expired: DRAM, IDA, SCHL, BRZE, EFOR, LRN, AVNT, AWI, HOOD, CRWD, NVDA, GOOGL (pending).

## Update after parser rewrite (calls.jsonl 1948 records, 799 option opens)

Fixed since the first pass: closes tagged as opens (now caught by flags), leading-date expiry, entry-price labels, echo flagging, open_id links on closes.

Remaining or new observations:
- Echo flags remove 316 of 799 opens (237 duplicate_echo, 79 cross_channel_echo). My own same-channel/day dedupe still merged 14 more groups that were not flagged (same contract re-quoted at a different entry price); worth deciding whether those are echoes or separate fills.
- no_expiry without a 0DTE tag: 81 unflagged-as-echo opens dropped as unscorable. Another 38 opens lack entry_price (entry_unknown / entry_from_tail cases).
- One scored open has entry_price 0 (return undefined, excluded from return stats). Entry of 0 should probably be flagged entry_implausible.
- Opens posted many weeks before expiry that passed all flags: axisalgorithmictrade CSCO and LZB, posted 2026-07-15, expiry 2026-08-21 (37 days). Probably genuine monthly expiries, but confirm they are not date-parse errors.
- bottom-5 example: vertexpublic SPX 7000P 2026-07-17, posted 2026-06-27 09:19 UTC at $27.80 (a Saturday post, SPX 7000 far from the money). Check whether posted_date_suspect should cover weekend timestamps.
- Quoted closes: 418 deduped quoted results include stock closes; only 122 pair to a scored open with open_link=contract. 94 contracts of 156 pairs rely on ticker_day links, which can pair a close with the wrong strike.
