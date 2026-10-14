# Funnel callouts vs the tape: outcomes

Generated 2026-10-14 from `calls.jsonl` (1948 records). Source: `tg_outcomes.py`.

> Scored n = 253. Still a short window of tape; expiry-day moves dominate results.

## Method and assumptions

- No option price history exists here. **Headline number = hold-to-expiry intrinsic**: (max(0,S-K) call / max(0,K-S) put at the expiry-date close, minus quoted entry) x 100.
- **'Touched breakeven' is optimistic**: underlying high (calls) / low (puts) after the post reached strike+entry / strike-entry. It assumes a perfect exit at the extreme; it is an upper bound, not a P&L.
- Entry premiums are the channel's own quoted fills, unverifiable. No slippage applied (flatters channels).
- Null expiry is NOT assumed same-day: only parser-tagged 0DTE (expiry_0dte_tag) posts are; others are unscorable. Parser-computed expiry is trusted. SPX priced off ^GSPC. Underlying bars: Yahoo public daily bars; 5m bars for the touch window when the post is within 55 days.
- Dedupe: one row per (channel, ticker, side, strike, expiry, post date); 'distinct contracts' also collapses echoes across channels.

## Coverage funnel

| Stage | Count |
|---|---|
| Option open records (action=open, kind=option) | 799 |
| minus excluded by parse flag `duplicate_echo` | 237 |
| minus excluded by parse flag `cross_channel_echo` | 79 |
| minus excluded by parse flag `expiry_before_post` | 3 |
| minus excluded by parse flag `entry_implausible` | 5 |
| minus excluded by parse flag `posted_date_suspect` | 14 |
| minus excluded by parse flag `expiry_far` | 3 |
| minus no expiry (unknown, not assumed 0DTE) | 81 |
| minus other unscorable (missing strike/side/entry, parser close, no price data) | 38 |
| Remaining after same-channel/day dedupe | 325 |
| Pending (expiry not yet passed) | 71 |
| **Scored** (intrinsic at expiry, entry price present) | 253 |
| Distinct contracts among scored (across channels) | 243 |

Echoes (`duplicate_echo` + `cross_channel_echo`, 316 records) are not scored; the first post of each contract is.
Other unscorable reasons: missing entry_price (38)

## Pooled results (hold to expiry)

| Basis | n | Win rate (P&L>0) | Median return | Mean return | Worth zero at expiry | Touched BE (optimistic) | Sum P&L, 1 contract each |
|---|---|---|---|---|---|---|---|
| Channel-level (deduped per channel) | 253 | 17% | -100% | -36% | 77% | 43% | $-27118 |
| Distinct contracts | 243 | 16% | -100% | -37% | 77% | 44% | $-27059 |

Return = intrinsic/entry - 1; -100% means expired worthless. Mean is dragged by a few multi-baggers; median is the typical open.

## Top 5 distinct contracts by P&L per contract

| Channel | Contract | Posted (UTC) | Entry | P&L/contract | Multiple | Touched BE |
|---|---|---|---|---|---|---|
| bzjzhzhzuzzu | AMD 600.0 C 2026-10-02 | 2026-09-25 15:23 | $3.70 | $3021 | 9.16x | yes |
| blackcardfreechannel | MRNA 170.0 C 2026-09-25 | 2026-09-21 13:42 | $4.00 | $2488 | 7.22x | yes |
| blackcardfreechannel | META 715.0 C 2026-09-21 | 2026-09-21 14:57 | $1.90 | $2434 | 13.81x | yes |
| blockwave10 | SPX 7720.0 C 2026-09-25 | 2026-09-25 13:37 | $11.40 | $1201 | 2.05x | yes |
| blackcardfreechannel | AMD 550.0 C 2026-09-18 | 2026-09-17 13:43 | $2.10 | $772 | 4.68x | yes |

## Bottom 5

| Channel | Contract | Posted (UTC) | Entry | P&L/contract | Multiple | Touched BE |
|---|---|---|---|---|---|---|
| vertexpublic | SPX 7000.0 P 2026-07-17 | 2026-06-27 09:19 | $27.80 | $-2780 | 0.00x | no |
| blackcardfreechannel | DELL 575.0 C 2026-09-18 | 2026-09-16 13:36 | $13.52 | $-1352 | 0.00x | yes |
| apextraderkoryphae | WDC 470.0 C 2026-09-25 | 2026-09-23 16:05 | $10.30 | $-1030 | 0.00x | no |
| crestedgeroom | SPX 7770.0 P 2026-10-07 | 2026-10-07 13:37 | $9.70 | $-970 | 0.00x | no |
| axisalgorithmictrade | SPX 7720.0 C 2026-09-30 | 2026-09-30 14:03 | $9.69 | $-969 | 0.00x | no |

## Survivorship test: channel's quoted results vs real hold-to-expiry

Quoted = `result_pct` on close posts (deduped by channel/ticker/day/value; includes stock and option closes, as quoted). Real = every scored open from the same channel, held to expiry. Channels with fewer than 5 scored opens are pooled.

| Channel | Quoted closes n | Quoted median | Quoted mean | Scored opens n | Real win rate | Real median | Real mean | Worth zero | Gap (quoted mean - real mean) |
|---|---|---|---|---|---|---|---|---|---|
| bzjzhzhzuzzu | 2 | 139% | 139% | 38 | 13% | -100% | -47% | 82% | 186 pts |
| blackcardfreechannel | 83 | 26% | 36% | 35 | 14% | -100% | -12% | 77% | 48 pts |
| ajfreealart32 | 28 | 40% | 60% | 28 | 14% | -100% | -64% | 82% | 123 pts |
| blockwave10 | 2 | 38% | 38% | 28 | 18% | -100% | -65% | 82% | 103 pts |
| axisalgorithmictrade | 27 | 32% | 120% | 26 | 19% | -100% | -52% | 69% | 171 pts |
| crestedgeroom | 22 | 40% | 42% | 20 | 15% | -100% | -42% | 80% | 84 pts |
| bob_signalsfreealert | 80 | 60% | 104% | 10 | 50% | -47% | 31% | 50% | 74 pts |
| moonwalkertrades2 | 15 | 40% | 44% | 10 | 0% | -100% | -97% | 90% | 141 pts |
| tradevisionst | 0 | - | - | 9 | 11% | -100% | 46% | 67% | - |
| mrquickerfreealert | 25 | 51% | 80% | 8 | 0% | -100% | -100% | 100% | 180 pts |
| vanguardstockupdates68 | 2 | 45% | 45% | 7 | 14% | -100% | -69% | 86% | 114 pts |
| apextraderkoryphae | 10 | 212% | 324% | 7 | 43% | -32% | 74% | 43% | 250 pts |
| queen_free_entries | 19 | 35% | 80% | 7 | 14% | -100% | -64% | 86% | 144 pts |
| bincofreealert | 24 | 36% | 67% | 7 | 14% | -100% | -85% | 86% | 152 pts |
| blue_falcon_capital | 4 | 109% | 239% | 5 | 60% | 77% | 36% | 40% | 203 pts |
| small channels (pooled, 3 ch) | 75 | 60% | 171% | 8 | 12% | -100% | 84% | 75% | 87 pts |
| **ALL channels pooled** | 418 | 42% | 97% | 253 | 17% | -100% | -36% | 77% | 133 pts |

Quoted closes include only trades the channel chose to announce a result for; real column includes every scored open, including those never followed up. Gap is in percentage points of return. Quoted and real are not the same trades, so this compares reporting, not individual fills.

## Trade-level: quoted close vs same contract held to expiry

- link = contract (exact contract match): n=122 pairs over 74 contracts. Quoted: win 86%, median 30%, mean 41%. Same contracts held to expiry: win 17%, median -100%, mean -40%. Quoted winners that expired worthless/loss if held: 87 of 105.
- all links incl. ticker_day (looser match): n=156 pairs over 94 contracts. Quoted: win 88%, median 36%, mean 58%. Same contracts held to expiry: win 21%, median -100%, mean -28%. Quoted winners that expired worthless/loss if held: 109 of 138.

Caveat: a close is an early exit and the real column is hold-to-expiry, so a quoted win that would have expired worthless is not a lie, it is a different trade. The comparison shows how much of a quoted edge depends on exiting at the right time. Pairs depend on the parser's open_id link; `ticker_day` links are weaker than `contract` links. Only closes whose paired open was scored appear here.

## Caveats

- n = 253 scored opens over a short window (posts from 2026-06-08 to 2026-10-13); a few trending days move the whole table. Per-channel rows with n under 30 are noisy.
- Hold-to-expiry ignores that a trader may have exited early at a better (or worse) price; touch-breakeven is the optimistic bound for that.
- Quoted entry premiums are unverified; real fills on illiquid strikes are typically worse.
- Echo posts (same trade reposted by several channels) are collapsed for the distinct-contract numbers but each channel counts it once in its own row.
- Parser issues affecting this run: see `reports/analysis/outcomes_parser_notes.md`.
- Pending opens (71) are excluded; longer-dated swings are not yet resolved.
- `expiry_far` records (3) are reported, not scored.
