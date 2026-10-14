# Funnel callouts vs the tape: outcomes

Generated 2026-10-14 from `calls.jsonl` (14706 records). Source: `tg_outcomes.py`.

> Scored n = 2134. Still a short window of tape; expiry-day moves dominate results.

## Method and assumptions

- No option price history exists here. **Headline number = hold-to-expiry intrinsic**: (max(0,S-K) call / max(0,K-S) put at the expiry-date close, minus quoted entry) x 100.
- **'Touched breakeven' is optimistic**: underlying high (calls) / low (puts) after the post reached strike+entry / strike-entry. It assumes a perfect exit at the extreme; it is an upper bound, not a P&L.
- Entry premiums are the channel's own quoted fills, unverifiable. No slippage applied (flatters channels).
- Null expiry is NOT assumed same-day: only parser-tagged 0DTE (expiry_0dte_tag) posts are; others are unscorable. Parser-computed expiry is trusted. SPX priced off ^GSPC. Underlying bars: Yahoo public daily bars; 5m bars for the touch window when the post is within 55 days.
- Dedupe: one row per (channel, ticker, side, strike, expiry, post date); 'distinct contracts' also collapses echoes across channels.

## Coverage funnel

| Stage | Count |
|---|---|
| Option open records (action=open, kind=option) | 6995 |
| minus excluded by parse flag `duplicate_echo` | 2477 |
| minus excluded by parse flag `cross_channel_echo` | 1010 |
| minus excluded by parse flag `expiry_before_post` | 25 |
| minus excluded by parse flag `entry_implausible` | 32 |
| minus excluded by parse flag `posted_date_suspect` | 45 |
| minus excluded by parse flag `expiry_far` | 36 |
| minus excluded by parse flag `entry_below_intrinsic` | 23 |
| minus no expiry (unknown, not assumed 0DTE) | 621 |
| minus other unscorable (missing strike/side/entry, parser close, no price data) | 314 |
| Remaining after same-channel/day dedupe | 2275 |
| Pending (expiry not yet passed) | 140 |
| **Scored** (intrinsic at expiry, entry price present) | 2134 |
| Distinct contracts among scored (across channels) | 2030 |

Echoes (`duplicate_echo` + `cross_channel_echo`, 3487 records) are not scored; the first post of each contract is.
Other unscorable reasons: missing entry_price (280); no price data for NDXP (10); no price data for APPL (5); no price data for XSP (4); no price data for VSCO (2); no price data for PTLR (2); no underlying bar on expiry date 2026-03-31 (1); no underlying bar on expiry date 2026-04-01 (1); no underlying bar on expiry date 2026-04-17 (1); no underlying bar on expiry date 2026-05-07 (1); no price data for SATS (1); no underlying bar on expiry date 2026-08-15 (1); no underlying bar on expiry date 2026-08-29 (1); no underlying bar on expiry date 2026-09-18 (1); no price data for AAIO (1); no price data for ABDE (1); no price data for APPLE (1)

## Pooled results (hold to expiry)

| Basis | n | Win rate (P&L>0) | Median return | Mean return | Worth zero at expiry | Touched BE (optimistic) | Sum P&L, 1 contract each |
|---|---|---|---|---|---|---|---|
| Channel-level (deduped per channel) | 2134 | 18% | -100% | -10% | 77% | 43% | $-65072 |
| Distinct contracts | 2030 | 17% | -100% | -9% | 77% | 43% | $-56158 |

Return = intrinsic/entry - 1; -100% means expired worthless. Mean is dragged by a few multi-baggers; median is the typical open.

## Top 5 distinct contracts by P&L per contract

| Channel | Contract | Posted (UTC) | Entry | P&L/contract | Multiple | Touched BE |
|---|---|---|---|---|---|---|
| moonwalkertrades2 | SPX 7550.0 C 2026-08-05 | 2026-07-31 16:50 | $6.80 | $16675 | 25.52x | yes |
| bzjzhzhzuzzu | SPX 7550.0 C 2026-08-05 | 2026-08-03 14:03 | $6.80 | $16675 | 25.52x | yes |
| blockwave10 | SPX 7300.0 C 2026-06-11 | 2026-06-11 15:10 | $12.50 | $8180 | 7.54x | yes |
| blockwave10 | SPX 7300.0 C 2026-06-09 | 2026-06-09 17:03 | $9.80 | $7685 | 8.84x | yes |
| ajfreealart32 | SNDK 1720.0 C 2026-09-18 | 2026-09-18 13:38 | $2.20 | $6962 | 32.65x | yes |

## Bottom 5

| Channel | Contract | Posted (UTC) | Entry | P&L/contract | Multiple | Touched BE |
|---|---|---|---|---|---|---|
| crestedgeroom | NDX 29050.0 C 2026-07-22 | 2026-07-22 13:45 | $65.20 | $-6520 | 0.00x | yes |
| bob_signalsfreealert | MU 900.0 C 2026-07-17 | 2026-07-17 13:58 | $65.00 | $-6500 | 0.00x | no |
| blockwave10 | NDX 29550.0 C 2026-09-09 | 2026-09-09 14:01 | $45.20 | $-4520 | 0.00x | no |
| vertexpublic | SPX 7000.0 P 2026-07-17 | 2026-06-27 09:19 | $27.80 | $-2780 | 0.00x | no |
| crestedgeroom | SNDK 1900.0 C 2026-08-21 | 2026-08-17 13:40 | $23.31 | $-2331 | 0.00x | no |

## Survivorship test: channel's quoted results vs real hold-to-expiry

Quoted = `result_pct` on close posts (deduped by channel/ticker/day/value; includes stock and option closes, as quoted). Real = every scored open from the same channel, held to expiry. Channels with fewer than 5 scored opens are pooled.

| Channel | Quoted closes n | Quoted median | Quoted mean | Scored opens n | Real win rate | Real median | Real mean | Worth zero | Gap (quoted mean - real mean) |
|---|---|---|---|---|---|---|---|---|---|
| crestedgeroom | 434 | 39% | 75% | 380 | 20% | -100% | -19% | 73% | 95 pts |
| bzjzhzhzuzzu | 7 | 128% | 333% | 328 | 12% | -100% | -20% | 86% | 353 pts |
| moonwalkertrades2 | 163 | 53% | 159% | 323 | 15% | -100% | 9% | 82% | 150 pts |
| bob_signalsfreealert | 300 | 63% | 134% | 220 | 19% | -100% | -24% | 75% | 158 pts |
| blockwave10 | 116 | 42% | 84% | 177 | 29% | -100% | 28% | 66% | 56 pts |
| de_gainers_free_circle | 334 | 60% | 95% | 122 | 25% | -100% | 52% | 61% | 43 pts |
| queen_free_entries | 89 | 50% | 88% | 103 | 15% | -100% | -12% | 77% | 101 pts |
| ajfreealart32 | 113 | 53% | 106% | 72 | 15% | -100% | -17% | 81% | 123 pts |
| novatrade02 | 51 | 240% | 410% | 67 | 6% | -100% | -83% | 91% | 493 pts |
| blackcardfreechannel | 115 | 26% | 35% | 54 | 13% | -100% | -30% | 76% | 65 pts |
| apextraderkoryphae | 15 | 166% | 286% | 50 | 18% | -100% | 4% | 80% | 283 pts |
| bincofreealert | 256 | 50% | 120% | 48 | 19% | -100% | -52% | 77% | 173 pts |
| mrquickerfreealert | 345 | 60% | 93% | 47 | 15% | -100% | -16% | 74% | 109 pts |
| mrfortunefreeflow | 70 | 44% | 70% | 41 | 27% | -100% | -20% | 59% | 90 pts |
| spymaster8 | 26 | 424% | 692% | 29 | 14% | -100% | -44% | 79% | 736 pts |
| tradevisionst | 1 | 24% | 24% | 21 | 14% | -100% | -5% | 71% | 29 pts |
| vanguardstockupdates68 | 2 | 45% | 45% | 10 | 10% | -100% | -78% | 90% | 123 pts |
| axisalgorithmictrade | 34 | 37% | 141% | 8 | 25% | -100% | -23% | 75% | 165 pts |
| gpt2136 | 22 | 98% | 359% | 8 | 12% | -100% | -70% | 75% | 430 pts |
| vertexpublic | 7 | 7% | 18% | 7 | 0% | -100% | -100% | 100% | 118 pts |
| mavericksroom | 1 | 26% | 26% | 5 | 20% | -100% | -54% | 80% | 80 pts |
| small channels (pooled, 5 ch) | 138 | 100% | 253% | 14 | 29% | -100% | 56% | 57% | 196 pts |
| **ALL channels pooled** | 2639 | 50% | 123% | 2134 | 18% | -100% | -10% | 77% | 133 pts |

Quoted closes include only trades the channel chose to announce a result for; real column includes every scored open, including those never followed up. Gap is in percentage points of return. Quoted and real are not the same trades, so this compares reporting, not individual fills.

## Trade-level: quoted close vs same contract held to expiry

- link = contract (exact contract match): n=739 pairs over 480 contracts. Quoted: win 93%, median 42%, mean 71%. Same contracts held to expiry: win 27%, median -100%, mean 41%. Quoted winners that expired worthless/loss if held: 492 of 684.
- all links incl. ticker_day (looser match): n=930 pairs over 562 contracts. Quoted: win 93%, median 43%, mean 85%. Same contracts held to expiry: win 27%, median -100%, mean 39%. Quoted winners that expired worthless/loss if held: 628 of 868.

Caveat: a close is an early exit and the real column is hold-to-expiry, so a quoted win that would have expired worthless is not a lie, it is a different trade. The comparison shows how much of a quoted edge depends on exiting at the right time. Pairs depend on the parser's open_id link; `ticker_day` links are weaker than `contract` links. Only closes whose paired open was scored appear here.

## Caveats

- n = 2134 scored opens over a short window (posts from 2026-05-26 to 2026-10-13); a few trending days move the whole table. Per-channel rows with n under 30 are noisy.
- Hold-to-expiry ignores that a trader may have exited early at a better (or worse) price; touch-breakeven is the optimistic bound for that.
- Quoted entry premiums are unverified; real fills on illiquid strikes are typically worse.
- Echo posts (same trade reposted by several channels) are collapsed for the distinct-contract numbers but each channel counts it once in its own row.
- Parser issues affecting this run: see `reports/analysis/outcomes_parser_notes.md`.
- Pending opens (140) are excluded; longer-dated swings are not yet resolved.
- `expiry_far` records (36) are reported, not scored.
