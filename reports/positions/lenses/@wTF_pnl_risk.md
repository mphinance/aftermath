# @wTF — P&L Attribution & Risk Lens

Scope: where the money was made and lost, and how much risk was on, across the ~16-month
tracked window (2023-12-22 to 2025-04-05, 338 account snapshots, 1,186 leg-rows, 414 diffed
position changes). All figures are derived from `data/positions/@wTF_positions.json` and
`data/prices/@wTF_prices.json`. Every number below states its method; estimates are labeled.

## Headline findings

1. **Account peaked at $95.09M on 2024-03-28**, up +65.7% from the first snapshot ($57.38M on
   2023-12-22) — versus SPY +10.4% and QQQ +8.7% over the same span. One week later
   (2024-04-05, last reliable reading before a data gap) the account was already down to
   $78.39M, a **-17.6% pullback in 8 days** while SPY/QQQ moved less than -1%.

2. **The account curve has a real, unrepairable hole between 2024-04-06 and 2024-09-11.**
   Inside it: a literal $0 balance on 2024-07-26 and $3.3M–$4.1M readings on Sep 9/10/11/26,
   which then jump to $51.3M on 2024-09-12 (a >1,400% one-day "recovery"). That pattern is not
   a plausible real trading swing — it is treated as a sync/reset artifact per the brief. The true
   trough inside the gap is unknown; the first trustworthy post-gap reading is $51.26M
   (2024-09-12), implying a real drawdown of **at least -34.6%** from the $78.39M pre-gap mark
   (probably more, since the account never shows a plausible bridge between $78M and $51M).

3. **The Feb→Apr 2025 slide is real, continuous data, and it hurt: $73.22M (2025-02-20) →
   $33.21M (2025-04-05), a -54.6% drawdown in ~6.5 weeks**, versus SPY -17.2% and QQQ -21.3%
   over the identical dates — the book lost roughly **2.5–3x the market's decline**, all of it
   organic (no artifact flags in this window).

4. **Beta vs SPY ≈ 3.6 (corr 0.61, n=131 snapshot-to-snapshot return pairs, artifact window
   excluded); vs QQQ ≈ 2.75 (corr 0.57).** Estimated annualized volatility of the account's
   return series is **~119% vs SPY's ~20%** — about 6x market vol. This is a directionally
   market-correlated but heavily levered/optioned book, not a hedged one.

5. **BA is the single largest loss campaign by a wide margin: -$9.12M realized** across 31
   closed/expired legs (20 wins, 11 losses — a 65% win rate) — net-negative only because
   average losers (**-$1.82M**) ran roughly **3.3x bigger** than average winners (**+$544K**).
   BA was also the largest concentration risk: **44.1% of account value** in BA notional alone
   on 2024-03-24 ($51.6M gross on an $85.0M account).

6. **Largest identified winning campaigns: HOOD +$3.13M realized** (2 legs, both winners,
   including a $15c 2024-05-17 call that expired deep ITM for +$3.04M) and **QQQ +$1.59M**
   across 8 small closed calls, all wins. UBER nets to roughly **+$713K** (a modest realized
   +$160K plus +$553K unrealized at the last snapshot), despite being the single biggest gross
   position late in the sample.

7. **Short-put assignment exposure got extreme in the book's final months.** Aggregate short-put
   strike×shares notional peaked at **$124.4M on 2025-02-27**, against a $67.9M account
   (183% of account value). The single worst leg was a short BA $170 put, 3,500 contracts
   (350,000 sh) = **$59.5M of assignment notional on a $61.0M account** (2025-01-29) — a put
   assignment there would have required essentially the entire account in cash.

8. **Aggregate win/loss on all closed/expired legs with a known outcome (n=65 of 68; 3
   settlements unknown/estimated):** 44 wins (avg **+$385K**), 21 losses (avg **-$1.03M**),
   **profit factor 0.79** — won more often than lost (67.7% win rate) but lost $1.27 for every
   $1.00 won, driven almost entirely by BA's loss sizing.

9. **20% overnight gap-down stress test on the peak UBER position** (2025-03-22, $22.6M gross
   UBER notional, 35.3% of a $64.0M account): repricing every leg to intrinsic value at UBER
   -20% (≈$75.84 → $60.67) produces an **estimated -$9.87M mark-to-market hit, -15.4% of
   account value**, driven mainly by the short $75-strike June puts going deep in the money.
   This is an intrinsic-only estimate — it ignores IV expansion on the still-short puts and time
   value lost on long calls, so it likely understates the real gap-down loss.

## 1. Account curve, drawdowns, and the data gap

| Point | Date | Total value | Note |
|---|---|---|---|
| First snapshot | 2023-12-22 | $57.38M | — |
| **Peak** | **2024-03-28** | **$95.09M** | +65.7% from first snapshot |
| Last reliable pre-gap reading | 2024-04-05 | $78.39M | -17.6% off peak in 8 days |
| Data artifact: literal zero | 2024-07-26 | $0 | sync/reset gap |
| Data artifact: degraded reads | 2024-09-09/10/11/26 | $3.26M–$4.09M | implausible if real (see below) |
| First reliable post-gap reading | 2024-09-12 | $51.26M | +1,400%+ jump from prior-day $3.7M read |
| Local peak | 2025-02-20 | $73.22M (also $73.29M intraday same window) | recovery leg after the gap |
| **Trough (continuous, non-artifact data)** | **2025-04-05** | **$33.21M** | last snapshot in dataset |

**Why the Jul–Sep 2024 stretch is treated as an artifact, not real trading:** a real account
cannot legitimately go from $78.4M to $0 to ~$3.5M and then to $51.3M within a single day
(2024-09-11 → 2024-09-12) without a matching leg-level trade blotter that would explain a
+1,400% one-day gain — and no such leg activity is in the `changes` log for that date. The
brief's own caveat flags this window; the data supports it. **Practical implication:** the true
peak-to-trough drawdown of the March–September 2024 leg cannot be measured precisely. The
floor is -34.6% (peak-adjacent $78.39M → first-trustworthy $51.26M); it is very likely worse,
since $51.26M itself looks like a snapback rather than a smooth landing.

The **February–April 2025 drawdown is not in question** — it's built from a dense run of daily
snapshots with no zero/jump artifacts: **-54.6% in 6.5 weeks**, the single worst confirmed
drawdown in the tracked data.

### Benchmark comparison (SPY / QQQ, same calendar windows)

| Window | Account | SPY | QQQ |
|---|---|---|---|
| 2023-12-22 → 2024-03-28 (inception → peak) | **+65.7%** | +10.4% | +8.7% |
| 2024-03-28 → 2024-04-05 (peak → last pre-gap) | **-17.6%** | -0.9% | -0.8% |
| 2024-04-05 → 2024-09-12 (spans the data-artifact gap) | -34.6%* | +7.8% | +7.4% |
| 2024-09-12 → 2025-02-20 (post-gap recovery) | **+41.4%** | +9.2% | +13.5% |
| **2025-02-20 → 2025-04-05 (the 73M→33M slide)** | **-54.6%** | -17.2% | -21.3% |
| Full sample, 2023-12-22 → 2025-04-05 | **-42.1%** | +6.7% | +3.5% |

\* Understates the real move; see gap discussion above. The market was flat-to-up while the
account state was unreadable/artifacted.

**Net:** over the full 16 months, @wTF's account is down 42% while SPY is up 7% and QQQ up
3.5% — despite an early +66% run that dramatically outpaced both indices. The account gave back
the entire outperformance and then some, concentrated in two drawdown legs (the unmeasurable
spring/summer 2024 one and the fully-measured Feb–Apr 2025 one).

### Beta / volatility (methodology and caveats)

Computed from log returns between consecutive *real* (non-artifact) snapshot days, dropping any
gap wider than 10 calendar days and excluding the 2024-04-06→2024-09-11 artifact window
entirely (n=131 return pairs). An earlier attempt using forward-filled daily values produced a
nonsensical negative beta — forward-filling manufactures zero-return days on the many days
between weekly-ish snapshots, which swamps the true signal. The snapshot-to-snapshot method is
more honest but still noisy (irregular timing, options gamma/theta contaminate the "market
beta" reading) — treat as directional, not precise.

- **Beta vs SPY: ~3.6x**, correlation 0.61 (n=131)
- **Beta vs QQQ: ~2.75x**, correlation 0.57 (n=131)
- **Beta vs ^VIX: ~-0.35x**, correlation -0.50 (n=131) — moves inversely with vol spikes, as
  expected for a long-biased book
- **Annualized volatility proxy** (daily-return std × √252): account ≈ **119%**, SPY ≈ 20% — a
  ~6x vol multiple

## 2. Campaign P&L by underlying

Method: **realized** = sum of `last_seen_profit` from the `changes` log's CLOSED and
EXPIRED/GONE events for that root ticker (the platform's last mark before the leg vanished —
labeled by the brief as an estimate, not an exact fill price). **Unrealized at data end** = sum
of the `profit` field across all legs for that root still open in the very last snapshot
(2025-04-05). **This under-counts total money made/lost**: per the data caveats, a root's legs
can quietly drop out of the tracked snapshots (because @wTF stopped tagging posts about that
ticker) without a matching CLOSED event, so campaigns that were fully exited off-camera are
invisible to this method. Where that's likely, it's flagged.

| Root | Realized (from closes) | Unrealized @ 2025-04-05 | **Total est.** | Closed legs (W/L) | Best mark seen | Worst mark seen |
|---|---:|---:|---:|---|---|---|
| **BA** | **-$9,122,715** | $0 | **-$9,122,715** | 31 (20W/11L) | +$6.53M (2025-03-21) | **-$11.92M (2024-03-19)** |
| **HOOD** | +$3,131,095 | $0 | +$3,131,095 | 2 (2W/0L) | +$4.53M (2024-03-27) | -$24K (2024-03-05) |
| **QQQ** | +$1,594,091 | $0 | +$1,594,091 | 8 (8W/0L) | +$958K (2024-04-02) | -$180K (2025-03-21) |
| **UBER** | +$160,234 | +$553,222 | +$713,456 | 13 (8W/5L) | +$5.87M (2025-02-18) | -$2.25M (2024-12-13) |
| **TSLA** | +$523,883 | $0 | +$523,883 | 3 (3W/0L) | +$595K (2024-10-31) | -$682K (2024-10-25) |
| **RIVN** | -$884,954 | $0 | -$884,954 | 5 (1W/4L) | +$2.04M (2024-03-07) | -$651K (2025-03-04) |
| RXRX | +$17,941 | $0 | +$17,941 | 2 (2W/0L) | +$43K | $0 |
| AAPL | -$2,366 | $0 | -$2,366 | 1 (0W/1L) | -$68K (2024-03-01) | -$318K (2024-03-05) |
| ADBE | — (no CLOSED event; last leg-mark +$1.24M on 2024-03-25) | — | not resolvable | — | +$1.24M | -$545K |
| SQ/XYZ | — | — | not resolvable | — | +$351K | -$158K |
| ZS | — | — | not resolvable | — | -$704K | -$1.23M |

**Read on the biggest three:**

- **BA is the story of the book's overall loss.** Its worst single-snapshot unrealized mark was
  **-$11.92M on 2024-03-19** (a huge call position under water right before the March 2024
  peak), and even though the majority of BA closes were profitable (20 of 31), the losers were
  so much bigger (avg -$1.82M vs avg win +$544K) that the campaign net to -$9.12M realized.
  BA also reappears as a large short-put writer in Jan–Mar 2025 (see §3) — that's a second,
  separate source of BA risk layered on top of the directional-call losses.
- **HOOD and QQQ were clean, profitable, low-complexity campaigns** — HOOD's gain is
  concentrated almost entirely in one $15c 2024-05-17 call tranche that expired in the money for
  +$3.04M (an EXPIRED/GONE event on 2025-02-25, well after the actual May-2024 expiry —
  the settlement estimate used the platform's last mark, consistent with the brief's guidance).
- **UBER nets small and mixed** despite carrying the single largest gross dollar exposure late
  in the sample (§3) — it was a high-turnover, delta-neutral-ish options book (many offsetting
  short/long strikes across three expiries simultaneously; see the option-structures lens for
  the strategy shape) rather than a simple directional bet, so its P&L stayed contained relative
  to its notional.

**Reconciliation gap, stated plainly:** summing every identified campaign's total_estimate
above nets to roughly **-$4.0M**, far short of the ~$62M peak-to-trough decline in the account
curve (§1). The difference is not an error — it lives almost entirely in (a) the unmeasurable
spring/summer 2024 gap, and (b) positions that closed without a matching CLOSED/EXPIRED event
in the snapshot-diff log (silently dropped tickers, or losses realized between two snapshots
where the position also changed size, which the diff tool may not always classify as a clean
"close"). Treat the campaign table as a **partial, best-effort attribution**, not a full
reconciliation of the account curve.

## 3. Leverage, margin, and concentration

**Gross notional vs account value** (legs' `value` field, i.e., current market value, summed;
snapshots with account_value < $10M excluded as data-artifact noise):

| Date | Account value | Gross notional | Gross/Account | Top name | Top name % of acct |
|---|---:|---:|---:|---|---:|
| **2024-03-24** | $85.0M | $51.6M | **0.61x** | BA | **44.1%** |
| 2024-03-25 | $92.4M | $53.0M | 0.57x | BA | 40.4% |
| 2025-03-26 | $64.1M | $36.1M | 0.56x | UBER | 34.0% |
| 2025-03-21 | $63.8M | $34.0M | 0.53x | BA | 24.6% |
| 2025-03-04 | $57.9M | $27.8M | 0.48x | UBER | 24.5% |
| 2025-01-06/07 | $53.3–53.6M | $24.3–24.5M | 0.46x | UBER | ~30% |

Gross notional (at-market value, not max-loss) never exceeded ~0.6x account value in this
dataset — this is not a book carrying 3–5x gross leverage in the traditional sense. The real
leverage lives in **option convexity and short-option obligations**, not raw notional (see
below), plus margin borrowing.

**Margin (cash_balance):** cash_balance went as negative as **-$24.48M on 2024-03-15**
(account value $77.28M then — about 32% of account value funded on margin), during the run-up
into the March 2024 BA/HOOD peak. Cash balance oscillated between roughly -$25M and +$55M
across the sample; deep negative readings cluster around position-building pushes in March 2024
and late 2024/Q1 2025.

**Short-put assignment exposure (strike × shares, the real tail risk in this book):**

| Date | Aggregate short-put assignment notional | Account value | % of account |
|---|---:|---:|---:|
| **2025-02-27** | **$124.42M** | $67.90M | **183%** |
| 2025-01-29 (single BA $170p, 3,500 ct) | $59.5M (this leg alone) | $61.0M | 97.5% (this leg alone) |

An aggregate assignment obligation of 183% of account value means that if every short put in
the book had gone in the money simultaneously, @wTF would have owed nearly **twice the account's
entire value** in stock purchases — a scenario that would force either a massive margin call or
a forced unwind. This is the single clearest "risk of ruin" signal in the position data: not
gross notional (which stayed under 1x), but **contingent obligations from short options**,
which don't show up in a simple notional/account ratio.

## 4. Risk of ruin: stress scenarios

**20% overnight gap down in UBER, peak position (2025-03-22, $22.6M gross UBER notional /
35.3% of a $64.0M account):**

Repricing every UBER leg to intrinsic value at UBER $75.84 → $60.67 (-20%):

| Leg type | Now (marked) | Shock (intrinsic @ -20%) |
|---|---:|---:|
| 210,000 sh equity | $15.93M | $12.74M |
| Long calls (6 strikes/expiries) | +$5.12M | $0 (all OTM after -20%) |
| Short calls (3 strikes/expiries) | -$0.50M | $0 (all OTM, short side benefits) |
| Short puts (5 strikes/expiries, incl. $75-strike June puts) | -$1.02M | **-$3.09M** (deep ITM) |
| **Total book value** | **$19.52M** | **$9.65M** |

**Estimated P&L impact: -$9.87M, or -15.4% of account value**, in a single overnight gap —
concentrated almost entirely in the short $75-strike June-2025 puts (139,400 sh short, -$0.75M
now → -$2.00M intrinsic value after the shock). This is an **intrinsic-only estimate**: it
ignores implied-vol expansion (short puts would mark even worse as IV spikes on a real gap) and
time value erosion on the long calls (which would also cost more than shown), so the true loss
in a real gap-down is probably somewhat larger than -15.4%.

**Same exercise, sized for BA's peak concentration (2024-03-24, 44.1% of account, $51.6M
gross):** BA's book at that point was overwhelmingly long calls ($200 and $210 strikes, see
§2), so a -20% gap would have wiped out most of the option premium — directionally consistent
with the -$11.92M worst BA mark actually recorded five days later (2024-03-19 in the P&L
table above straddles this window). The realized history already shows this risk materializing:
BA's calls did in fact crater in March 2024 (see the CLOSED events for the $200c 5/17 tranche
going from +$282K to -$10.74M across three snapshots in March 2024).

## 5. Win/loss on closed and expired legs

From the `changes` log, all CLOSED and EXPIRED/GONE events (n=68 total; 65 have a known
`last_seen_profit`, 3 do not — see estimate note below):

| Metric | Value |
|---|---:|
| Closed/expired legs with known P&L | 65 |
| Wins | 44 (67.7%) |
| Losses | 21 (32.3%) |
| Average win | +$385,410 |
| Average loss | -$1,025,754 |
| Gross win | $16,958,052 |
| Gross loss | $21,540,844 |
| **Profit factor** | **0.79** |

**By underlying:**

| Root | n closed | W / L | Sum P&L | Avg win | Avg loss |
|---|---:|---|---:|---:|---:|
| BA | 31 | 20 / 11 | -$9,122,715 | +$543,890 | -$1,818,228 |
| HOOD | 2 | 2 / 0 | +$3,131,095 | +$1,565,547 | — |
| QQQ | 8 | 8 / 0 | +$1,594,091 | +$199,261 | — |
| UBER | 13 | 8 / 5 | +$160,234 | +$94,031 | -$118,403 |
| TSLA | 3 | 3 / 0 | +$523,883 | +$174,628 | — |
| RXRX | 2 | 2 / 0 | +$17,941 | +$8,970 | — |
| AAPL | 1 | 0 / 1 | -$2,366 | — | -$2,366 |
| RIVN | 5 | 1 / 4 | -$884,954 | +$61,000 | -$236,489 |

**Pattern:** high win rate (67.7% overall, 65% even in BA specifically) combined with a
sub-1.0 profit factor is the classic signature of **cutting winners early relative to losers
being allowed to run or being scaled into while underwater** — visible directly in BA, where
loss size (avg -$1.82M) is 3.3x win size (avg +$544K). RIVN shows the same shape at smaller
scale (1 win averaging +$61K vs. 4 losses averaging -$236K).

**3 unresolved settlements** (last_seen_profit was null in the source diff, so a P&L delta
can't be computed from the change log alone): BA $170p 2025-03-21 (230,000 sh, FLIP into this
leg, then expired — settlement estimate: intrinsic $0, BA closed 2025-03-21 at $178.11, above
the $170 strike), BA $210c 2025-06-20 (10,000 sh — settlement estimate: intrinsic $0, BA closed
2025-06-20 at $198.75, below strike), and UBER $75c 2025-03-21 (110,000 sh — settlement
estimate: intrinsic **$92,400**, UBER closed 2025-03-21 at $75.84, just above strike). These are
**settlement values, not P&L deltas** (entry cost basis for these specific tranches isn't
separable from the leg's running total in the source data), so they're reported as estimates
and excluded from the profit-factor calculation above.

## Data caveats applied in this lens

- Treated 2024-04-06 through 2024-09-11 as a data-artifact window (see §1) for all curve,
  drawdown, benchmark, and beta calculations. Leg-level campaign attribution still uses any real
  leg rows inside that window where present, since individual leg snapshots can be more reliable
  than the account-total rollup.
- All "realized" P&L is the platform's `last_seen_profit` (last observed mark before a leg
  vanished from the snapshot log), not a confirmed fill price — per the brief, labeled as an
  estimate throughout.
- EXPIRED/GONE settlements with a null last-seen-profit were estimated from intrinsic value at
  the expiry-date close (price bars), explicitly labeled, and excluded from win/loss stats.
- Gross notional and concentration figures use `value` (current mark), not max-loss; short-put
  assignment notional (strike × shares) is reported separately as the more meaningful tail-risk
  metric for a book that sells options.
- Campaign P&L is a partial attribution (see reconciliation-gap note in §2) — it does not sum to
  the full account drawdown, and that gap is explained rather than papered over.

## Files

- Full chartable series (account curve, leverage series, short-put assignment series, campaign
  P&L, win/loss, benchmark windows, beta): `reports/positions/lenses/@wTF_pnl_series.json`
- Scratch scripts used for this analysis (not part of the deliverable):
  `/tmp/claude-1000/-home-mpha-projects-aftermath/5355fcb9-2520-4395-8e3e-6796abb45fed/scratchpad/pnl_risk_main.py`,
  `pnl_risk_part2.py`, `build_output_json.py`
