# 🧬 Deep Forensic Autopsy: @wTF (The Martingale Kid & Popcorn Prophet)
### *Non-Followed AfterHour Trader, Surfaced via Community Mentions | Financial Position-Ledger Breakdown of a Real Eight-Figure Account*

---

## 📊 Dossier Metadata

- **Trader Handle**: `@wTF`
- **Profile URL**: [https://afterhour.com/wTF](https://afterhour.com/wTF)
- **Profile ID**: `prf_f93bea30b95d41848255a3407afa6f66`
- **Network Rank**: Not a Followed Trader — surfaced via community @-mentions and reply threads (tracked ad hoc, not part of the core followed roster)
- **Audited Lifetime Posts**: 411 posts
- **Active Operational Timeline**: 2023-10-06 to 2025-04-05 (546 calendar days / 78.0 weeks) — no posts after the final entry; account appears dormant/retired
- **Posting Cadence**: 5.27 posts/week lifetime average (0.75 posts/day), bimodal — 258 posts in the first 6 months (Oct 2023–Mar 2024) vs. near-total silence May–Aug 2024, then 141 posts in a second life (Sep 2024–Apr 2025)
- **Follow-Through Rate**: **68.2%** per the automated keyword audit (22 tickers announced as buys, 15 publicly closed) — see §3 for a manual, position-by-position reconciliation that finds this figure is inflated by one omnibus post mentioning ten tickers at once
- **Disclosed Tag Ratio**: **No ratio available** — 0 Gain-tagged posts and 0 Loss-tagged posts out of 411; the platform's win/loss tagging feature is entirely unused
- **Verified Capital Trajectory**: $57.4M (Dec 2023 baseline) -> $95.1M peak (Mar 28, 2024) -> telemetry gap / reset ($0–$3.7M sync readings, Jul–Sep 2024) -> $51.3M re-baseline (Sep 12, 2024) -> $73.2M second-era peak (Feb 20, 2025) -> **$33.2M** (final tracked reading, Apr 5, 2025). `afterhour.py` stores `amount_k` as `total_value / 1000`, so a reading of 57382.10 is $57,382,097.80 — a real eight-figure account, not a small paper account. All figures below are reported exactly as stated in the posts or computed directly from `amount_k`, never estimated.
- **TraderMatrix Algorithmic Classification**:
  - **Primary: `MARTINGALE_CONCENTRATION_GAMBLER`**
  - **Secondary:** `CONTRARIAN_FEAR_BUYER`
- **Algorithmic Alpha Score**: **30 / 100**
- **Signal Expectancy**: **Expected Value**: **Not computable from disclosed data** — of 24 tickers with a confirmed stated transaction, only 4 ever receive an explicit closing post (2 with a stated qualitative win, 0 with a stated loss, 2 with no stated outcome), and not one closed position anywhere in the 411-post archive carries a dollar-quantified realized P&L — despite this being a real, tens-of-millions-dollar account where exact numbers were plainly available. | **Win Rate**: **Undisclosed** (0 Gain-tags / 0 Loss-tags; see §4.2 for the full closed-position count).

---

## 1. Executive Summary

### 1.1 Trader Philosophy & Archetype: The Self-Aware Martingale Gambler

- **A real eight-figure account, not a paper/simulated one.** `amount_k` is `total_value / 1000` (`afterhour.py:150`), so the tracked balance runs from $57.4M to a $95.1M peak. Post #367 (2025-02-14) — *"feel free to ignore this silly kid, it's all paper money away"* — is self-deprecating slang about an unrealized ("paper") gain, not a disclosure that the account is simulated; the same post calls the position "a small position % of 🐳 [whale]," consistent with a genuinely large account. The in-post dollar figures (e.g., "$12M on $BA") are on the same scale as the tracked balance, not inflated — see §2.3.
- **Two capital eras.** Era 1 (Dec 2023 baseline $57.4M → Mar 2024 peak $95.1M) ends in a ~4-month posting blackout that coincides with $0 telemetry readings. Era 2 restarts at a fresh $51.3M baseline (Sep 2024), peaks at $73.2M (Feb 2025), then falls to a final $33.2M (Apr 2025) — the account's lowest sustained reading, recorded on its last-ever post. In dollar terms that final six-week slide is roughly a **$40M drawdown** from the Era 2 peak.
- **A tiny, concentrated universe for an account this size.** 29 unique cashtags across 411 posts, but only 24 ever receive a confirmed stated transaction, and one name ($BA) accounts for 11 of the posts, is twice described as the trader's "biggest position yet," and — per the one instrument breakdown ever given (§4.3) — ran to roughly 14% of the tracked account.
- The financial mechanics — what was bought, in what instrument, how much was disclosed, and what happened at exit — are broken out in full in §3 (Position Ledger) and aggregated in §4.

---

## 2. Account Value & Capital Curve (from `amount_k`)

`afterhour.py:150` sets `"amount_k": total_value / 1000` — the field is already denominated in thousands, so a raw reading of 57382.0978 is **$57,382,097.80**, not $57,382.10. Every dollar figure below is `amount_k * 1000`, shown in millions for readability. Percentages are unaffected by this unit and match the raw `amount_k` ratios directly.

### 2.1 Era 1 — Dec 2023 to Apr 2024

| Metric | Date | Value |
| :--- | :--- | :--- |
| Baseline (first tracked reading) | 2023-12-22 | $57.38M |
| Peak | 2024-03-28 | $95.09M |
| Low, excluding telemetry anomalies | 2024-01-25 | $46.28M |
| Last reading before the blackout | 2024-04-05 | $78.39M |
| Baseline → peak run-up | — | **+65.7%** |
| Peak → last observable reading | — | **-17.6%** |

**Telemetry anomalies (Era 1):** $0 readings on 2024-02-27 and 2024-02-28 (x2), and an isolated $341,061 single-post reading on 2024-03-08 sandwiched between two ~$86M readings on the same day — all inconsistent with the surrounding balances and excluded from the peak/trough calculations above as sync artifacts, not real account states.

### 2.2 The Blackout and Reset — Apr to Sep 2024

No posts appear from 2024-04-06 through 2024-07-25 (a ~3-month silence). The account then logs:

| Date | `amount_k` reading (real $) | Post title |
| :--- | :--- | :--- |
| 2024-07-26 | $0 | "👂🏼🙉" |
| 2024-09-09 | $3.53M | "✈️✈️✈️" |
| 2024-09-09 | $3.56M | "😔" |
| 2024-09-10 | $3.26M | "Here we go again ✈️🔥🙈" |
| 2024-09-11 | $3.71M | "Hello old friend." |
| 2024-09-12 | **$51.26M** | "Martin wanted to say Hi too 🙉" |

No post anywhere in the archive explains this jump. It is not stated as a deposit, and there is no confirmatory language ("I added funds," "reloaded the account," etc.) — the corpus only shows the number resetting from a multi-million-dollar low back up to the account's normal scale in one day. This is reported as an unexplained reset, not assumed to be a deposit.

### 2.3 Era 2 — Sep 2024 to Apr 2025

| Metric | Date | Value |
| :--- | :--- | :--- |
| Re-baseline | 2024-09-12 | $51.26M |
| Peak | 2025-02-20 | $73.22M |
| Final tracked reading (last post) | 2025-04-05 | $33.21M |
| Re-baseline → peak run-up | — | **+42.8%** |
| Peak → final drawdown | — | **-54.6%** (≈ **-$40.0M** in dollar terms) |
| Re-baseline → final, full Era 2 | — | **-35.2%** |
| Full observed window: Dec 2023 baseline → final | — | **-42.1%** |

**The dollar figures in posts are on the same scale as the account, not inflated.** In Post #242 (2024-03-24), the trader writes: *"we started the week down over $12M on $BA, Friday morning up almost $3M, and ended the week pretty much even."* The tracked `amount_k` readings for that same week (2024-03-18 through 2024-03-22) run from $76.41M (low) to $87.75M (high) — a real range of **$11.34M**, closing the week at $85.00M versus an opening of $78.33M. A stated "$12M down, then $3M up" position-level swing on the $BA name is entirely consistent with an account moving in double-digit millions that week; the account's own total balance also rose net over the week (other positions, including the $2.5M unrealized $ADBE gain disclosed in the same post, were running independently). This is reported as a scale check, not an exact reconciliation of the BA position's weekly P&L to the total account delta — but it confirms the two figures live in the same unit, with no conversion factor needed.

---

## 3. Full Position Ledger

Built directly from the raw JSON (`data/following/@wTF_all_posts.json`) — every post mentioning a ticker (via the `tickers` field or a `$CASHTAG` in title/body) was read for transaction language. Fields marked **not stated** mean the post genuinely omits that information; nothing here is inferred or estimated. Dollar amounts are reproduced exactly as written in the post — these are on the same real-dollar scale as the tracked `amount_k` balance (see §2.3), not a separate/inflated unit. Where a ticker generated no confirmed personal transaction (commentary/comparison only), it is listed at the bottom under §3.2.

### 3.1 Tickers With a Confirmed Stated Transaction (24 of 29)

| Ticker | Instrument(s) Stated | First Entry Date | Stated Entry Size(s) | Entry Price | Exit Date | Exit Price | Stated Outcome | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$SQ** | Stock + Calls, later Puts | 2023-10-07 | "$250k" (10/9); "150k+ more" (10/10); "150k more" (10/11); "couple hundred thousand more" (10/11); "another mil" (10/13); "500k... 47.5c" (10/18); "$1.7M" (10/25); adds 10/26 x2, size not stated | 47.5c stated for the 10/18 add; all other entries not stated | 2023-11-07 | not stated | "Officially selling" — outcome not quantified; regret post 2 days later ("missing out on making millions is worse than losing millions") implies the stock kept rising after the sale (opportunity cost, not a loss on the trade) | **Closed** (11/7/23), then **re-opened** 2024-02-29 ("made up with my old friend $SQ... went through earnings together"); no second close stated — went silent after 2024-03-24 |
| **$HOOD** | Stock + Calls | 2023-10-11 (add to pre-existing) | Not stated (10/11, 10/26); "doubled my 12c position" (1/11/24); "bought more" (1/12/24); "another 2M in options" (1/23/24) | 12c strike stated 1/11/24; others not stated | 2024-02-28 (dated relative to the 2/29 post) | not stated | Interim loss disclosed 1/3/24 ("losing money," unquantified); final close outcome not quantified | **Closed** — "finally sold everything yesterday" per 2024-02-29 post |
| **$BA** | Calls + Puts + Stock | 2024-03-08 | "Round 2" add, size not stated (3/8 x2); more adds 3/8, 3/24 ("biggest position into BA yet"); position snapshot 2024-11-04: **"just under $6M in call options. Sold another 1M in Puts, and a little over 1M in stock"** (≈$8M stated total, ≈14% of the $55.4M `amount_k` reading that same week — see §4.3); adds 1/3/25, roll of "the long term one" at 12/13/24 | Real-market price references given 12/10/24 ($165–170) and 12/13/24 ($170, target $220–240) — these are market-price commentary, not a stated personal cost basis | Not stated | Not stated | Week of 3/18–3/24/24: "down over $12M... up almost $3M... ended pretty much even" — consistent in scale with the account's real $76.4M–$87.8M range that week (see §2.3). No full-close post found anywhere in the corpus. | **Never confirmed closed** — last mention 2025-01-21, then goes silent |
| **$RIVN** | Calls + Stock, then Puts | 2024-01-23 | "bought a bunch," size not stated; Thursday 2/22/24 calls+stock size not stated, Friday 2/23/24 add "20M more"; 100k in puts stated as never executed | Not stated | 2024-02-27/28 (dated relative to 2/29 post) | Not stated | "Sold yesterday and today most of my position (and taken profit)" — majority exit at a stated profit, remainder left open due to "a busy school day" | **Closed (majority), stated win** for Episode 1; **re-opened** 2024-12-19 ("doubled down... out of boredom") — no exit stated for Episode 2, went silent |
| **$CART** | Stock (shares) | 2023-10-11 (pre-existing, disclosed) | Not stated | Not stated | Never confirmed | Not stated | Losses acknowledged 10/11 (unquantified, blamed on @candy); "doing well" by 10/13, with stated intent: "might close out my position once I'm even" | **Intent to close at breakeven stated, never confirmed** — no further CART mention in the archive |
| **$UBER** | Stock; one ambiguous "80c 2/21 calls" mention (underlying not explicitly confirmed) | 2024-12-17 | "bought more" (12/17, 12/20, 12/30), size not stated each time | Not stated | Never confirmed | Not stated | 2025-02-07 general remark that "profit day is a happy day" (community-directed, not a confirmed personal close) | **Open / went silent** — last mention 2025-02-07 |
| **$TSLA** | Not stated (held through earnings, instrument unspecified) | 2024-01-30 (retroactive disclosure) | Not stated | Not stated | Never confirmed | Not stated | Unplanned earnings hold ("never intended to hold TSLA through earnings... but emotions took over"); outcome described only as "everyone here knows how that turned out" (implies a loss, unquantified) | **Open / went silent** — last mention 2024-03-05 |
| **$NOW** | Options | 2023-10-25 | "$10k of $Now options" (10/25); "I bought 200k" (10/25) | Not stated | 2023-10-26 | Not stated | "Parlay his winnings from $NOW to $CMG" — implies a profitable close, no dollar figure given | **Closed, stated win (unquantified)** — proceeds rotated into $CMG/$AMZN |
| **$PYPL** | Not stated | 2023-10-26 | Not stated ("all loaded up again," bundled with SQ/HOOD) | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** — last mention 2024-02-08, commentary only after initial entry |
| **$ZGN** | Stock (shares — liquidity-constrained per the trader's own note) | Pre-existing by 2024-12-19 (first mention is already a "double down") | "Doubled down" 12/19/24, size not stated; described 1/18/25 as accumulated "slowly" due to low daily volume | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** — last mention 2025-02-13 |
| **$RXRX** | Not stated (instrument unspecified) | 2025-02-14 | "This new position," explicitly flagged as "a small position % of 🐳 [portfolio]" — no dollar or % figure given | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** — opened 7 weeks before the account's final post, never closed |
| **$U** (Unity) | Stock (10/11/23); Puts (2/29/24, "The Randos") | 2023-10-11 | Not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$NFLX** | Options (accidental oversize) | 2023-10-13 | "Meant to double my positions but instead 11x'd it" — a stated fat-finger execution error; no dollar size given | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** — operational-risk event, no subsequent update |
| **$MSFT** | Stock (portfolio weight disclosed) | 2023-10-24 (pre-existing) | **"Made up of 22% [of portfolio]"** — the only explicit position-sizing % in the entire archive | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$AMZN** | Not stated | 2023-10-26 | "And $AMZN too but whatever" — rotation add, size not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$COIN** | Not stated | 2024-02-29 | "A little $COIN here and there when I was bored" — size not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$ARDX** | Stock | Pre-existing, disclosed 2023-10-17 | Not stated | Not stated | Never confirmed | Not stated | "My $ARDX stock is up!" (unquantified) | **Open / went silent** |
| **$CMG** | Not stated | 2023-10-26 | Rotation destination for $NOW proceeds, size not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$SGOV** | Not stated (T-bill ETF) | Pre-existing, disclosed 2023-12-06 | Not stated | Not stated | Never confirmed | Not stated | "No one told me you can lose money in $SGOV" — a stated loss, unquantified, on an instrument normally treated as near-cash | **Open / went silent** |
| **$CVNA** | Calls | 2024-02-29 | "CVNA Calls" listed under "The Randos" — size/strike not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$BKNG** | Puts | 2024-02-29 | "BKNG Puts" listed under "The Randos" — size/strike not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$AMC** | Calls | 2024-02-29 | "AMC Calls" listed under "The Randos" — size/strike not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$SNOW** | Not stated, framed as a directional hedge vs. $RIVN | 2024-02-29 | "SNOW and its sizing is actually my hedge against tomorrow's macro data" — size not stated | Not stated | Never confirmed | Not stated | Not stated | **Open / went silent** |
| **$ADBE** | Not stated (pre-existing position, never described as opened) | Pre-existing before 2024-03-24 | Not stated | Not stated | Never confirmed | Not stated | **+$2.5M unrealized gain stated ("roughly 50%+," vs. a 30% target)** on 2024-03-24 — trader explicitly chose to hold rather than take profit; no further ADBE mention in the archive, so the fate of this gain is unknown | **Never confirmed closed** — largest single stated gain in the corpus, outcome unresolved |

### 3.2 Tickers Mentioned With No Confirmed Personal Transaction (5 of 29)

| Ticker | Nature of Mention |
| :--- | :--- |
| **$NVAX** | Referenced three times as commentary/satire ("once the stock hits $4.5, buy 1 stock, watch it go down") or as a comparison point for $RXRX — no confirmed buy/sell by the trader |
| **$LCID** | Comparison reference only ("$RIVN != $TSLA or $LCID"; "why the same didn't apply to $LCID") |
| **$META** | Commentary on another user's (@sisig's) prediction, not the trader's own position |
| **$EADSY** | Explicitly considered as a $BA alternative and explicitly **not** bought ("they said they are sold out of planes... so back to $BA I guess") |
| **$XYZ** | Single ambiguous mention (2025-03-27): "Now I know my ABC… and $XYZ" — reads as an alphabet-song reference (possibly a nod to Block/Square's real 2025 ticker rebrand from $SQ to $XYZ); no buy/sell, size, or price stated |

---

## 4. Aggregates

### 4.1 Options vs. Equity Split

Reading the "Instrument(s) Stated" column in §3.1 directly:

| Split | Tickers |
| :--- | :--- |
| **Options-only stated** (calls/puts, no equity mentioned) | $NOW, $RIVN (also has stock), $U, $CVNA, $BKNG, $AMC, $UBER (ambiguous) — core clean options names: $NOW, $CVNA, $BKNG, $AMC |
| **Equity-only stated** | $CART, $ARDX, $MSFT, $ZGN, $TSLA (unspecified instrument, treated separately below) |
| **Mixed options + equity, same ticker** | $SQ (stock then calls then puts), $HOOD (stock + calls), $BA (calls + puts + stock, the only ticker with a full three-way breakdown), $RIVN, $U |
| **Instrument never specified** | $PYPL, $RXRX, $NFLX (accidental oversize, instrument type not respecified beyond "positions"), $AMZN, $COIN, $CMG, $SGOV, $SNOW, $ADBE, $TSLA, $XYZ |

**Takeaway, computed from the ledger**: 4 tickers are unambiguously options-only, 4 are unambiguously equity-only (excluding $TSLA), 4 mix both instruments in the same name ($SQ, $HOOD, $BA, $RIVN — notably the four largest/most-discussed positions in the archive), and roughly 11 never specify an instrument at all. $BA is the only position with a fully itemized instrument breakdown, and it is split across all three (calls, puts sold, and stock).

### 4.2 Win/Loss Count on Closed Positions

Using only positions in §3.1 with an explicit closing statement (not the automated keyword-match count in the metadata block — see the methodology note below):

| Outcome | Tickers | Count |
| :--- | :--- | :--- |
| **Closed, stated qualitative win** | $RIVN (Episode 1, "taken profit"), $NOW ("winnings") | 2 |
| **Closed, stated qualitative loss** | *(none found)* | 0 |
| **Closed, outcome not stated** | $SQ (Episode 1), $HOOD | 2 |
| **Stated intent to close at breakeven, never confirmed** | $CART | 1 |
| **Total with any closing language** | | **5 episodes across 4 tickers** |
| **Confirmed still-open or went-silent with no exit post** | $BA, $SQ (Episode 2), $RIVN (Episode 2), $UBER, $TSLA, $PYPL, $ZGN, $RXRX, $U, $NFLX, $MSFT, $AMZN, $COIN, $ARDX, $CMG, $SGOV, $CVNA, $BKNG, $AMC, $SNOW, $ADBE | 20 |

**Average win vs. average loss**: **not computable.** Not one of the 5 closing episodes above states a dollar-quantified realized P&L. The two "wins" ($RIVN, $NOW) are described only in qualitative terms ("taken profit," "winnings"). No loss is ever stated as realized on a closed position — the only stated losses ($HOOD early, $SGOV, $CART early) are all interim/unrealized commentary, not tied to a closing transaction.

**Methodology note on the 68.2% follow-through figure in the metadata block**: that number comes from `followthrough.py`, which flags a ticker as "closed" if any post mentioning it also contains exit-language keywords (sold, closed, rolled, expired, etc.), regardless of whether the sentence is actually about that ticker. Post #176 ("Context is everything," 2024-02-29) is a single omnibus post that mentions ten tickers ($HOOD, $SQ, $COIN, $BKNG, $CVNA, $AMC, $U, $RIVN, $SNOW, $LCID) and contains multiple exit-language words ("sold," "rolled," "taken profit") describing what actually happened only to $HOOD and $RIVN. The automated script credits several of the other eight tickers in that post with a "close" they never individually received. The manual, per-position read in §3.1 finds only 4 tickers with an actual closing statement, not 15 — this manual count should be treated as the more reliable figure for TraderMatrix ingestion.

### 4.3 Concentration

With `amount_k` confirmed as real dollars-in-thousands (§2), two positions can now be measured directly against the tracked account:

- **$MSFT — 22% of portfolio**, stated directly (2023-10-24) — the only explicit percentage-of-account figure anywhere in the corpus.
- **$BA — computed at ≈14% of the tracked account.** The 2024-11-04 snapshot states "just under $6M in call options. Sold another 1M in Puts, and a little over 1M in stock" — summing the three stated components at face value gives ≈$8M in $BA exposure. The nearest `amount_k` reading (2024-11-04, $55.45M) puts that at **≈14.4% of the tracked account** in a single name — the only position in the archive where a computed, non-percentage concentration figure is possible. This is a rough sum of stated components, not a verified net position size (the "sold... puts" leg may represent a closed short rather than ongoing exposure), but it corroborates $BA being twice explicitly called the trader's "biggest position yet" (2024-03-24) and having the same order-of-magnitude swing ($12M stated, against a $76–88M account that week — §2.3).
- **$RXRX — explicitly flagged as "a small position % of 🐳 [portfolio]"** (2025-02-14) — no number given, but the "whale" framing is consistent with the account's real scale that month (~$71–72M).
- All other 26 tickers: position size relative to the account is **not stated**.

### 4.4 P&L by Ticker (Stated Figures Only)

| Ticker | Stated Result |
| :--- | :--- |
| $ADBE | Unrealized: **+$2.5M** (~50%+, vs. a 30% target), held past target, final fate unknown |
| $BA | One specific week (3/18–3/24/24): "down $12M → up $3M → net roughly flat" — same order of magnitude as the account's real $11.3M range that week (see §2.3) |
| $RIVN | Episode 1: stated win, "taken profit," no dollar figure |
| $NOW | Stated win via "winnings," no dollar figure |
| $HOOD | Interim: "losing money" (1/3/24, unquantified); final close outcome not stated |
| $SGOV | Stated loss, unquantified |
| $CART | Early losses (unquantified) followed by "doing well," final state unconfirmed |
| $SQ | No $ figure ever stated; regret post implies the stock rose after the Nov 2023 sale (opportunity cost) |
| All other 21 tickers | **Not stated** |

---

## 5. Qualitative Notes (Condensed)

- **"Martin(gale)"**: from Post #65 (2023-12-05, "Hello Martin(gale)!") onward, the trader uses "Martin" as a running personification of averaging down into a loser — directly named in the $HOOD, $BA, and $RIVN/$ZGN episodes in §3.1. This is the single clearest, self-admitted behavioral pattern in the archive.
- **A striking contrast**: recurring references to school, exams, a guidance counselor, and "my mom says" sit alongside management of a real eight-figure account — whatever the trader's actual age or relationship to the capital, the account itself is confirmed real, not a simulator (§1, §2).
- **Boredom/mood-driven sizing, explicitly admitted**: the $ZGN/$RIVN double-down (2024-12-19) is directly attributed to "boredom and still being upset about my test," not a market signal — now notable because it was applied to real capital, not play money.
- **The account ends on a farewell**: the final post (2025-04-05, "It's time!") cites a losing week and a hostile community reaction as reasons to "say goodbye," coinciding with the lowest tracked reading in the archive ($33.2M, down ≈$40M from the six-weeks-earlier Era 2 peak). No posts follow.

---

## 6. Quantitative Verdict for TraderMatrix

```
+---------------------------------------------------------------------------------------------------+
|                                   @wTF QUANTITATIVE SCORECARD                                     |
+-----------------------------------+-----------------------------------+---------------------------+
| CATEGORY                          | SCORE / 100                       | FORENSIC AUDIT READ       |
+-----------------------------------+-----------------------------------+---------------------------+
| Systematic Strategy Integrity     | 20 / 100                          | Self-named "Martingale"   |
|                                    |                                    | averaging on real 8-fig.  |
|                                    |                                    | capital, no real system   |
| Ticker Curation & Alpha Discovery | 55 / 100                          | Sharp early SQ/HOOD calls |
|                                    |                                    | compounded into a real    |
|                                    |                                    | $46M->$95M run, but tiny  |
|                                    |                                    | 29-ticker universe        |
| Exit Discipline & Disclosures     | 28 / 100                          | Only 4 of 24 traded tickers|
|                                    |                                    | ever get a real close post|
|                                    |                                    | despite real $ at stake   |
| Psychological Resilience          | 18 / 100                          | Boredom/mood sizing and   |
|                                    |                                    | burnout applied to real   |
|                                    |                                    | eight-figure capital      |
+-----------------------------------+-----------------------------------+---------------------------+
| COMPOSITE ALGORITHMIC ALPHA SCORE | 30 / 100                          | GRADE: D (HIGH-RISK, REAL-|
|                                    |                                    | CAPITAL FADE CANDIDATE)   |
+-----------------------------------+-----------------------------------+---------------------------+
```

### 6.1 Signal Flow Ingestion Matrix

```
                      ┌───────────────────────────────────────────────┐
                      │             @wTF Raw Signal Stream            │
                      └───────────────────────┬───────────────────────┘
                                              │
       ┌────────────────────────┬─────────────┴─────────────┬─────────────────────────┐
       ▼                        ▼                           ▼                         ▼
┌──────────────────┐  ┌────────────────────────┐  ┌───────────────────────┐ ┌─────────────────────────┐
│ Signal 1:        │  │ Signal 2: FUNDAMENTAL/  │  │ Signal 3: EARNINGS    │ │ Signal 4: MARTINGALE    │
│ EXTREME-FEAR      │  │ BRAND DD DISCOVERY     │  │ CATALYST BUILD-UP     │ │ DOUBLE-DOWN             │
│ CONTRARIAN ENTRY   │  │                        │  │                       │ │                         │
├──────────────────┤  ├────────────────────────┤  ├───────────────────────┤ ├─────────────────────────┤
│ SQ, HOOD          │  │ ZGN, RXRX, NVAX         │  │ HOOD, BA, TSLA, ADBE  │ │ Any post using "Martin" │
│ Action: WATCH ONLY │  │ Action: EXTRACT TO     │  │ Action: FLAG, DO NOT  │ │ or describing a repeat  │
│ AT CONFIRMED       │  │ INDEPENDENT SCREEN     │  │ MIRROR SIZE, VERIFY   │ │ add on a loser          │
│ CAPITULATION        │  │                        │  │ IV/CRUSH RISK         │ │ Action: HARD FADE       │
│ Weight: +0.35       │  │ Weight: +0.40          │  │ Weight: +0.10         │ │ Weight: -0.75 (Fade)    │
└──────────────────┘  └────────────────────────┘  └───────────────────────┘ └─────────────────────────┘
```

### 6.2 Execution Directives for the Artemis Engine

#### Ingestion Directives — Genuine Edge to Harvest
- **Ingest confirmed extreme-fear contrarian entries only** — the stated "I buy when I'm most scared" thesis has some historical support ($SQ Oct 2023 bottom, $HOOD Jan 2024 dip), but neither position's final dollar outcome was ever disclosed.
- **Extract the fundamental/brand-DD posts** ($ZGN unification/sneaker-brand thesis, $RXRX-vs-$NVAX comp framing) into the independent screener — these are the only entries in the ledger built on stated research rather than boredom or emotion.
- **Harvest the $BA instrument breakdown** (2024-11-04: ~$6M calls / ~$1M puts sold / ~$1M+ stock, ≈14% of the account — §4.3) as the corpus's only fully-itemized, verifiably-scaled multi-instrument position, useful as a structural and concentration-sizing template.

#### Contrarian Fade Directives — When to Fade Them or the Retail Herd
- **Hard-fade any post invoking "Martin"** — by the trader's own admission this marks averaging into a loser, not fresh conviction ($HOOD, $BA, $RIVN/$ZGN all show it), now confirmed to be applied to real eight-figure capital.
- **Fade position-sizing tied to explicitly non-market triggers** (boredom, a bad exam) — the $ZGN/$RIVN double-down is the clearest example.
- **Take every in-post dollar figure at face value** — they are on the same scale as the tracked account (§2.3) — but never assume a stated unrealized gain (e.g., the $2.5M $ADBE mark) was ever actually realized; only mirror figures tied to an explicit closing statement.

#### Mandatory Risk Blacklists & Firewalls
- **Blacklist "biggest position yet" language** — it preceded the account's largest, longest-unresolved position ($BA, ≈14% of the account, never confirmed closed) and its worst final drawdown.
- **Hard firewall against doubling into any name that already carries a stated loss that period.**
- **Exclude the Feb 2024 and Jul–Sep 2024 sub-$4M / $0 `amount_k` readings from all equity-curve models**; treat the Sep 12, 2024 reading (~$51.3M) as a reset baseline for "Era 2," not a literal drawdown from the Era 1 peak.

#### Exit Rules & Alpha Rectification
- **Impose a hard de-risk trigger after any single week showing a large drawdown on the account's own tracked balance** — the -54.6% Era-2 peak-to-final collapse (Feb–Apr 2025) directly preceded the account's terminal post.
- **Cap single-ticker exposure** — no BA/HOOD/RIVN-style "biggest position yet" concentration should be mirrored without an independent size cap, since the account itself never discloses a % figure to bound it by.
- **Mirror only positions that receive an explicit, unambiguous closing post** (only 4 of 24 traded tickers ever got one); treat the other 20 as permanently indeterminate rather than assuming a win or a loss.

---

## 7. Chronological Milestone & Catalyst Log

| Date | Milestone / Catalyst |
| :--- | :--- |
| 2023-10-06 | First AfterHour post; opens with a $SQ short-squeeze call near the stock's post-pandemic lows. |
| 2023-10-07 to 10-30 | Builds and repeatedly adds to the $SQ position (stock, then calls, then a reversal into puts on 10/30); parallel small adds in $HOOD, $PYPL, $NOW, $CMG, $AMZN, $CART, $ARDX, $MSFT (22% of portfolio), $NFLX (accidental 11x oversize). |
| 2023-12-05 | **"Hello Martin(gale)!"** — the trader names their own averaging-down habit for the first time. |
| 2023-12-22 | First tracked `amount_k` reading: **$57.4M**. |
| 2024-01-03 to 01-23 | Builds $HOOD into earnings (12c calls doubled, then "another 2M in options"); opens $RIVN and holds $TSLA through earnings unintentionally. |
| 2024-02-22 to 02-29 | Peak activity week: $RIVN calls/stock added ("20M more" on the Friday before earnings), then majority sold "taken profit"; $HOOD "sold everything"; small $COIN, $BKNG, $CVNA, $AMC, $U, $SNOW positions disclosed in one omnibus post. |
| 2024-03-08 to 03-28 | Enters and repeatedly adds to $BA during the Alaska Airlines door-plug crisis; describes a week "down $12M... up $3M... ended pretty much even" (real account range that week: $76.4M–$87.8M) and holds a $2.5M unrealized $ADBE gain past its own 30% target instead of taking profit. |
| 2024-03-28 | Era 1 peak tracked balance: **$95.1M**. |
| 2024-04-05 | Last Era-1 post before a ~4-month near-total silence. |
| 2024-07-26, 2024-09-09/10/11 | `amount_k` collapses to $0 and sub-$4M readings. |
| 2024-09-12 | Posting resumes; `amount_k` resets to **$51.3M** with no stated explanation, opening "Era 2." |
| 2024-11-04 | Position snapshot discloses the $BA instrument breakdown (~$6M calls / ~$1M puts sold / ~$1M+ stock) — ≈14% of that week's tracked account. |
| 2024-12-17 to 12-30 | Repeated small $UBER adds. |
| 2024-12-19 | Doubles down on $ZGN and $RIVN, explicitly attributed to boredom, not a market signal. |
| 2025-01-18 | Fundamental/brand-DD post on $ZGN (Zegna). |
| 2025-02-13/14 | Opens $RXRX, explicitly flagged as "a small position % of 🐳 [whale]." |
| 2025-02-20 | Era 2 peak tracked balance: **$73.2M**. |
| 2025-04-05 | **Final post: "It's time!"** `amount_k` reads **$33.2M**, the lowest sustained reading in the archive — roughly a $40M drawdown from the Feb 2025 peak. Trader cites a losing week and hostile community reaction as reasons to "say goodbye." No further posts follow. |

---

## 8. Forensic Conclusion

`@wTF`'s value to a quantitative signal framework is narrow and specific, and the ledger in §3 is the reason why: of 29 tickers touched across 411 posts, only 24 ever receive a confirmed transaction, only 4 ever receive an explicit close, and not a single closed position anywhere in the archive carries a dollar-quantified realized P&L — despite this being a real, tens-of-millions-dollar account, confirmed by `afterhour.py`'s own `amount_k = total_value / 1000` field definition, not a paper/simulated one. The account's tracked balance shows a real run from $57.4M to a $95.1M peak, an unexplained reset, a second run to $73.2M, and a final collapse to $33.2M (a ≈$40M drawdown from the Feb 2025 peak) on the trader's own last post. Harvest the rare fundamental-DD entries and the $BA instrument breakdown (the only position with a computable ≈14% concentration figure) as structural templates; firewall everything tagged "Martin" and every boredom-driven add — the stakes behind them were real.
