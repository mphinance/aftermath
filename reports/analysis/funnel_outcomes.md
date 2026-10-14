# Funnel callouts vs the tape: outcomes

Generated 2026-10-14 from `calls.jsonl` (8630 records). Source: `tg_outcomes.py`.

> Scored n = 1146. Still a short window of tape; expiry-day moves dominate results.

## Method and assumptions

- No option price history exists here. **Headline number = hold-to-expiry intrinsic**: (max(0,S-K) call / max(0,K-S) put at the expiry-date close, minus quoted entry) x 100.
- **'Touched breakeven' is optimistic**: underlying high (calls) / low (puts) after the post reached strike+entry / strike-entry. It assumes a perfect exit at the extreme; it is an upper bound, not a P&L.
- Entry premiums are the channel's own quoted fills, unverifiable. No slippage applied (flatters channels).
- Null expiry is NOT assumed same-day: only parser-tagged 0DTE (expiry_0dte_tag) posts are; others are unscorable. Parser-computed expiry is trusted. SPX priced off ^GSPC. Underlying bars: Yahoo public daily bars; 5m bars for the touch window when the post is within 55 days.
- Dedupe: one row per (channel, ticker, side, strike, expiry, post date); 'distinct contracts' also collapses echoes across channels.

## Coverage funnel

| Stage | Count |
|---|---|
| Option open records (action=open, kind=option) | 4093 |
| minus excluded by parse flag `duplicate_echo` | 1563 |
| minus excluded by parse flag `cross_channel_echo` | 535 |
| minus excluded by parse flag `expiry_before_post` | 19 |
| minus excluded by parse flag `entry_implausible` | 13 |
| minus excluded by parse flag `posted_date_suspect` | 34 |
| minus excluded by parse flag `expiry_far` | 19 |
| minus excluded by parse flag `entry_below_intrinsic` | 17 |
| minus no expiry (unknown, not assumed 0DTE) | 393 |
| minus other unscorable (missing strike/side/entry, parser close, no price data) | 160 |
| Remaining after same-channel/day dedupe | 1284 |
| Pending (expiry not yet passed) | 137 |
| **Scored** (intrinsic at expiry, entry price present) | 1146 |
| Distinct contracts among scored (across channels) | 1092 |

Echoes (`duplicate_echo` + `cross_channel_echo`, 2098 records) are not scored; the first post of each contract is.
Other unscorable reasons: missing entry_price (144); no price data for APPL (5); no price data for NDXP (3); no underlying bar on expiry date 2026-03-31 (1); no underlying bar on expiry date 2026-04-01 (1); no underlying bar on expiry date 2026-04-17 (1); no underlying bar on expiry date 2026-05-07 (1); no underlying bar on expiry date 2026-08-29 (1); no price data for AAIO (1); no price data for ABDE (1); no price data for APPLE (1)

## Pooled results (hold to expiry)

| Basis | n | Win rate (P&L>0) | Median return | Mean return | Worth zero at expiry | Touched BE (optimistic) | Sum P&L, 1 contract each |
|---|---|---|---|---|---|---|---|
| Channel-level (deduped per channel) | 1146 | 19% | -100% | 6% | 73% | 44% | $24297 |
| Distinct contracts | 1092 | 19% | -100% | 7% | 74% | 44% | $24732 |

Return = intrinsic/entry - 1; -100% means expired worthless. Mean is dragged by a few multi-baggers; median is the typical open.

## Top 5 distinct contracts by P&L per contract

| Channel | Contract | Posted (UTC) | Entry | P&L/contract | Multiple | Touched BE |
|---|---|---|---|---|---|---|
| moonwalkertrades2 | SPX 7550.0 C 2026-08-05 | 2026-07-31 16:50 | $6.80 | $16675 | 25.52x | yes |
| bzjzhzhzuzzu | SPX 7550.0 C 2026-08-05 | 2026-08-03 14:03 | $6.80 | $16675 | 25.52x | yes |
| ajfreealart32 | SNDK 1720.0 C 2026-09-18 | 2026-09-18 13:38 | $2.20 | $6962 | 32.65x | yes |
| moonwalkertrades2 | SNDK 1729.0 C 2026-09-18 | 2026-09-18 15:46 | $2.20 | $6062 | 28.55x | yes |
| crestedgeroom | AMD 570.0 C 2026-10-02 | 2026-09-16 13:35 | $6.40 | $5751 | 9.99x | yes |

## Bottom 5

| Channel | Contract | Posted (UTC) | Entry | P&L/contract | Multiple | Touched BE |
|---|---|---|---|---|---|---|
| blockwave10 | NDX 29550.0 C 2026-09-09 | 2026-09-09 14:01 | $45.20 | $-4520 | 0.00x | no |
| vertexpublic | SPX 7000.0 P 2026-07-17 | 2026-06-27 09:19 | $27.80 | $-2780 | 0.00x | no |
| crestedgeroom | SNDK 1900.0 C 2026-08-21 | 2026-08-17 13:40 | $23.31 | $-2331 | 0.00x | no |
| apextraderkoryphae | WDC 410.0 P 2026-09-18 | 2026-09-15 13:53 | $22.72 | $-2272 | 0.00x | no |
| crestedgeroom | MU 1050.0 C 2026-08-28 | 2026-08-18 13:36 | $18.18 | $-1818 | 0.00x | no |

## Survivorship test: channel's quoted results vs real hold-to-expiry

Quoted = `result_pct` on close posts (deduped by channel/ticker/day/value; includes stock and option closes, as quoted). Real = every scored open from the same channel, held to expiry. Channels with fewer than 5 scored opens are pooled.

| Channel | Quoted closes n | Quoted median | Quoted mean | Scored opens n | Real win rate | Real median | Real mean | Worth zero | Gap (quoted mean - real mean) |
|---|---|---|---|---|---|---|---|---|---|
| bzjzhzhzuzzu | 7 | 128% | 333% | 208 | 17% | -100% | 24% | 79% | 310 pts |
| moonwalkertrades2 | 85 | 48% | 112% | 147 | 16% | -100% | 53% | 79% | 59 pts |
| blockwave10 | 67 | 47% | 78% | 137 | 30% | -100% | 28% | 62% | 50 pts |
| crestedgeroom | 186 | 39% | 47% | 135 | 22% | -100% | 2% | 69% | 45 pts |
| queen_free_entries | 89 | 50% | 88% | 105 | 14% | -100% | -13% | 76% | 101 pts |
| ajfreealart32 | 113 | 53% | 106% | 72 | 15% | -100% | -17% | 81% | 123 pts |
| blackcardfreechannel | 115 | 26% | 35% | 54 | 13% | -100% | -30% | 76% | 65 pts |
| bob_signalsfreealert | 232 | 62% | 116% | 50 | 32% | -100% | 21% | 62% | 94 pts |
| bincofreealert | 256 | 50% | 120% | 48 | 19% | -100% | -52% | 77% | 173 pts |
| mrquickerfreealert | 201 | 55% | 95% | 43 | 14% | -100% | -31% | 74% | 126 pts |
| mrfortunefreeflow | 70 | 44% | 70% | 41 | 27% | -100% | -20% | 59% | 90 pts |
| axisalgorithmictrade | 34 | 37% | 141% | 24 | 29% | -100% | 1% | 71% | 140 pts |
| tradevisionst | 1 | 24% | 24% | 21 | 14% | -100% | -5% | 71% | 29 pts |
| apextraderkoryphae | 13 | 166% | 274% | 15 | 20% | -100% | -19% | 73% | 293 pts |
| vanguardstockupdates68 | 2 | 45% | 45% | 10 | 10% | -100% | -78% | 90% | 123 pts |
| gpt2136 | 22 | 98% | 359% | 8 | 12% | -100% | -70% | 75% | 430 pts |
| vertexpublic | 7 | 7% | 18% | 7 | 0% | -100% | -100% | 100% | 118 pts |
| de_gainers_free_circle | 129 | 45% | 76% | 6 | 0% | -73% | -66% | 50% | 142 pts |
| blue_falcon_capital | 4 | 109% | 239% | 5 | 60% | 77% | 36% | 40% | 203 pts |
| small channels (pooled, 4 ch) | 78 | 160% | 380% | 10 | 10% | -100% | 51% | 70% | 329 pts |
| **ALL channels pooled** | 1711 | 50% | 110% | 1146 | 19% | -100% | 6% | 73% | 104 pts |

Quoted closes include only trades the channel chose to announce a result for; real column includes every scored open, including those never followed up. Gap is in percentage points of return. Quoted and real are not the same trades, so this compares reporting, not individual fills.

## Trade-level: quoted close vs same contract held to expiry

- link = contract (exact contract match): n=492 pairs over 324 contracts. Quoted: win 90%, median 41%, mean 67%. Same contracts held to expiry: win 21%, median -100%, mean 2%. Quoted winners that expired worthless/loss if held: 344 of 443.
- all links incl. ticker_day (looser match): n=601 pairs over 365 contracts. Quoted: win 91%, median 42%, mean 78%. Same contracts held to expiry: win 22%, median -100%, mean 5%. Quoted winners that expired worthless/loss if held: 417 of 545.

Caveat: a close is an early exit and the real column is hold-to-expiry, so a quoted win that would have expired worthless is not a lie, it is a different trade. The comparison shows how much of a quoted edge depends on exiting at the right time. Pairs depend on the parser's open_id link; `ticker_day` links are weaker than `contract` links. Only closes whose paired open was scored appear here.

## Caveats

- n = 1146 scored opens over a short window (posts from 2026-06-08 to 2026-10-13); a few trending days move the whole table. Per-channel rows with n under 30 are noisy.
- Hold-to-expiry ignores that a trader may have exited early at a better (or worse) price; touch-breakeven is the optimistic bound for that.
- Quoted entry premiums are unverified; real fills on illiquid strikes are typically worse.
- Echo posts (same trade reposted by several channels) are collapsed for the distinct-contract numbers but each channel counts it once in its own row.
- Parser issues affecting this run: see `reports/analysis/outcomes_parser_notes.md`.
- Pending opens (137) are excluded; longer-dated swings are not yet resolved.
- `expiry_far` records (19) are reported, not scored.
