# Quant Forensic Dossier: @TRON

**Subject:** AfterHour trader `@TRON` (Profile ID `prf_88299be98b6b4d8b83bb66f08411047c`)
**Rank:** #3 most-active followed trader by lifetime post count
**Sample size:** 2,401 lifetime posts, 2024-11-25 → 2026-09-10 (654 days / 93.4 weeks) — a full, continuous, still-active posting history
**Sources:** `@TRON_lifetime.md` (formatted archive), `@TRON_all_posts.json` (raw, incl. `amount_k` portfolio snapshots, tags, engagement counters), cross-tabulated programmatically (ticker extraction, cadence, engagement trend, drawdown reconstruction)
**Analyst:** Artemis Forensic Desk · 2026-09-10

> **Headline finding:** @TRON is the rarest thing on this platform — a poster whose prose is *more* honest than his self-tagging. He is the only trader in this batch who narrates his own catastrophic drawdown in real time, in his own words, while it is happening. And it didn't matter. Between 2025-10-09 and 2025-10-17 his tracked portfolio fell from **$596,487 to $40,954 — a real, independently reconstructable −93.1% collapse in eight days** — driven by a single concentrated, repeatedly-rolled, repeatedly-added-to options position in **$ONDS**. He diagnosed his own fatal flaw ("I'm the worst at taking profits") on **Post #3, day two of his entire posting history**, twenty-three months before it cost him what he himself estimated at "a house." He never fixed it. That gap — between self-awareness and self-correction — is the single most important thing for Artemis to model about him.

---

## 1. Executive Profile

### Philosophy
@TRON presents as a **retail small-business owner (general contractor — carpentry, masonry, concrete, "in the south") who day-trades and content-creates on the side, at a volume that rivals a full-time job.** He is not a chartist, not a systematic quant, and not primarily an earnings-flow trader. He is a **high-frequency thematic momentum poster**: he finds a name (usually small/mid-cap, usually attached to a defense/drone/eVTOL/robotics/AI narrative), builds a position with options leverage, evangelizes it to a community he treats as "brothers and sisters," and — critically — almost never sells a winner down or cuts a loser short. His stated 2025 New Year's resolution, written on his second-ever post, is the thesis statement for his entire career on the platform:

> *"I'm the worst at taking profits and I often wait until it is too late to take money off the table."* (Post #3, 2024-11-26)

He repeats variants of this self-diagnosis dozens of times over the next two years (*"take profits when you can," "diamond hands only means you have a vision,"* advice to followers to "have a stop-loss ready") without ever visibly adopting the discipline himself. He is self-aware, funny, community-oriented, and — by his own admission and by the data — structurally incapable of de-risking a winning position before it round-trips.

### Post Cadence
| Metric | Value |
|---|---|
| Total posts | 2,401 |
| Active date range | 2024-11-25 → 2026-09-10 (654 days / 93.4 weeks) — **still active as of report date** |
| **Average cadence** | **25.7 posts/week** (≈ 3.7/day) |
| Weekday vs weekend | Mon–Fri: 392–442 posts/day-of-week; Sat/Sun: 142–171 — active but throttled on weekends |
| Peak posting hour (UTC) | 13:00–15:00 UTC (8–10am ET) — U.S. market open |
| Busiest single month | June 2025 (204 posts) — the run-up into his eventual peak |
| Cadence after the Oct-2025 crash | Roughly halved: 2026-Feb/Mar/Apr average ~60 posts/month vs. a 110–170/month norm in 2025 |
| Days silent as of report date | 0 (posted same-day, 2026-09-10) |

This is not a trading journal kept for personal accountability — 25+ posts/week for 93 straight weeks is a **content-creation cadence**. A large share of volume is humor, memes, and community banter (see §4), not trade calls.

### Verified Capital Trajectory (platform-tracked `amount_k`, total account value)
*Methodological note, carried over from the tool's own documentation: `amount_k` is a **total account value snapshot from a brokerage sync**, not a P&L figure, and the source tool explicitly flags this sync as **known to glitch**. Tags (`Gain`/`Loss`/`Discuss`/etc.) are self-selected by the poster, not verified. Both caveats matter enormously for this specific subject — see below.*

| Date | Event | Tracked value | Note |
|---|---|---|---|
| 2024-11-25 | First post ("Intel is cooking") | $160,141 | Starting baseline |
| 2025-08-08 to 08-11 | **"I am now Port Jesus!"** cluster | **$4,671,223 – $4,755,880** | **Confirmed platform glitch**, not real capital. He names the bug ("this glitch. Thank you @SIRJACK"), jokes about his "new McGlitchy port value," and explicitly predicts ("I would probably be back to a modest number by Monday") — which happened. **Discard this cluster entirely; do not let it appear in any return calculation.** |
| 2025-10-02 | "My first $60k day!" | $460,815 | Real, options-leveraged single-day gain, credited to LEAPS |
| 2025-10-08 | "$ONDS Calls Rolled to 2027" | $577,207 | Rolled an already-huge ITM options position **out** rather than trimming it |
| **2025-10-09, 11:33 UTC** | **Lifetime real peak** ("China sets export limits...") | **$596,487** | True (non-glitch) high-water mark |
| 2025-10-09, 21:43 UTC | "Took a day away…market went red" | $264,466 | −55.6% intraday/next-print — he "added options on the way down" instead of cutting |
| **2025-10-17, 22:06 UTC** | **"Wow this week was rough"** | **$40,954** | **−93.1% from the Oct-9 peak in 8 days.** His own words: *"I'm down a house in gains... not a super nice house, but a house."* |
| 2025-11-13 | "$500 Degen Challenge" (separate side account) | $51,027 (main port, unrelated) | Only `[Loss]`-tagged post in his entire 2,401-post history — and it's from a $500 novelty side-challenge, not his real book |
| 2026-03-30 | "Still the best defense battery play $ULBI" | **$27,490 — lifetime absolute low** | Nearly 5 months after the crash, still bleeding out, well below even the post-crash bottom |
| 2026-06-02 – 06-15 | "Challenge back on ($35k to more)" | $33k → $120k in days | **Likely a fresh/reset tracked sub-account, not organic recovery** — he explicitly frames it as a new "challenge" starting from ~$35k, distinct from the crashed main book; conflating this with genuine recovery would be an analytical error |
| **2026-09-10** | Report date (current) | **$413,927** | Stable in the $410–420k band since ~July 2026 |

**Net lifetime trajectory (excluding the glitch): $160,141 → $413,927 over 654 days (+158.5%)** — a real, positive multi-year number, but one that passes through a documented **−93.1% peak-to-trough real-money drawdown** and at least one likely account-reset event that makes the "recovery" narrative less clean than the headline number suggests. **Do not report the +158.5% figure to a consumer without the drawdown context; it materially misrepresents the risk actually taken.**

---

## 2. Ticker Universe & Catalysts

### Core universe (by raw `$TICKER` mention count, full history)
| Ticker | Mentions | Role |
|---|---|---|
| **$ONDS** (Ondas Holdings) | 335 | **Flagship/core holding.** Grew from a self-described "2.7%... curiosity position" (Mar 2025) → "crazy man" overexposure (Jun 2025) → the position that produced the Oct-2025 blow-up. Never fully exited even after the crash — still his #1 mentioned name post-crash (130 mentions). |
| $NIO | 234 | China-EV macro/political theme (tariffs, delivery numbers, insurance-registration data-mining) |
| $PLTR | 229 | Core long-held conviction name, mega-cap AI/data theme, cited as a long-game "don't listen to the noise" hold since Post #9 |
| $ACHR | 170 | eVTOL/defense conviction name — "would sell my whole port and put it all in Archer... I'll get a tattoo if it hits $100" |
| $NVDA | 137 | Mega-cap AI proxy, used for both bull-thesis and market-breadth commentary |
| $HUMA | 87 | Small-cap healthtech, momentum/support-level trade |
| $BBAI | 70 | AI/defense-adjacent (BigBear.ai), paired thematically with PLTR |
| $TSLA | 69 | EV/macro proxy, mixed bull/skeptic |
| $HOOD | 64 | Retail-sentiment/political proxy ("retail is so back") |
| $DDD, $OUST, $HOVR, $JOBY, $INFQ, $VELO, $SIDU, $RCAT, $NNDM | 20–70 each | The long tail of the drone/eVTOL/robotics/defense-microcap basket |

### Options vs. equities
- **566 of 2,401 posts (23.6%)** contain explicit options language (calls, puts, LEAPS, strikes, ITM/OTM, rolling, IV).
- He self-identifies as **LEAPS-first with a self-imposed rate limit on short-dated gambles**: *"I'm mostly in leaps (with a tiny bit of YOLO)... I'm allowed 1 [YOLO] a month."*
- Post-crash (Oct 2025 onward), **$SPY appears in his top-15 mentioned tickers for the first time**, including **explicit same-day 0DTE SPY trades** by Sept 2026 ("Closed 0DTE $SPY," "If you ignored my $SPY calls today") — a genuine, dated behavioral shift toward index-level hedging/scalping that his pre-crash ticker mix never showed.

### What drives entries — ranked by frequency
1. **Thematic momentum + narrative** (drone/defense/eVTOL/robotics/AI — by far the dominant lens; the theme comes first, the ticker second)
2. **Macro/political catalysts** — Fed data, tariffs/China trade negotiations, DOGE/administration policy, defense spending ("War is what we do in the U.S. and it doesn't really matter who the president is")
3. **SPAC / shell-to-operating-company merger arbitrage** — a genuinely distinctive, recurring niche (182 posts reference S-4s, SPACs, shell companies, or mergers): Boxabl/$FGMC, $PUSA (former golf-course shell → drone company), $JFB (construction company → merger with Xtend Drones/$AGH), $AGL. He specifically hunts for small, under-the-radar shells about to re-domicile into a hot theme — this is a real, nameable, semi-repeatable edge, not noise.
4. **Community/influencer cross-pollination** — citing other AfterHour posters' calls, reposting "featured on Charlie's channel"-style validation
5. **Earnings/news reactions** — real but secondary; he is not primarily an earnings-flow trader

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags?
**He holds bags — and says so, repeatedly, years in advance.** This is the defining trait of the account. Unlike most self-reporting traders on this platform, @TRON is unusually candid in *prose* about losses and drawdowns; the dishonesty here is not narrative, it's **behavioral** — he correctly diagnoses the problem and never solves it.

- **Position-sizing creep on $ONDS, documented in his own words across 7 months:**
  - 2025-03-21: *"I do hold a super tiny position out of a curiosity in $ONDS... 2.7%... wouldn't recommend anyone take a large position."*
  - 2025-06-29: *"I was a crazy man in April. Not sure what I was drinking to buy this much of a penny stock."*
  - 2025-10-08: Rolls a large in-the-money options position **out to 2027** rather than trimming it — extending duration risk at the top rather than reducing exposure.
  - 2025-10-09, on the way down: *"I dropped about 6.6%. I added options on the way down. Nothing crazy... I'm not really worried."* — classic averaging-down into a losing, already-oversized position.
- **He advises followers to use stop-losses he does not use himself:** *"They will correct harder than most. Have a stop-loss ready"* (re: $BBAI, to his audience) — there is no instance anywhere in 2,401 posts of him describing a stop-loss triggering on his own book.

### Documented wins vs. blow-ups
- **Documented wins:** Real and frequent — 101 posts self-tagged `[Gain]`, including independently plausible ones ("My first $60k day!" backed by the amount_k print; early PLTR/ACHR conviction calls that were directionally correct for months). His **idea generation and early-discovery instinct is genuinely good** — he was in $ONDS as a curiosity position in March 2025, well before its 2025 breakout, and in $ACHR/$PLTR when both were still widely dismissed as meme stocks.
- **Documented blow-ups:** Exactly **one** self-tagged `[Loss]` post in the entire history — and it is a $500 novelty "Degen Challenge" side-account, not his real book. **The actual, dollar-material blow-up (the −93.1% Oct-2025 collapse) carries no `[Loss]` tag at all** — it is tagged `[Discuss]` ("Took a day away…market went red," "Wow this week was rough"). **This is the critical tagging distortion for Artemis to correct for: his self-applied tags dramatically understate his real loss history — 101:1 Gain:Loss — even though his prose does not.** Any model trained naively on his tags alone will conclude he almost never loses; the amount_k series proves the opposite.

### How does he manage losing positions?
The record shows a consistent three-step pattern, repeated across the ONDS episode and smaller ones: **(1) do not trim the position as it grows past any sane concentration limit; (2) when it turns, add to it ("nothing crazy," "not really worried"); (3) once the loss is realized and can no longer be avoided, narrate it publicly with dry humor and stoic resignation, then move on without a structural fix.** He does eventually **diversify the surviving basket** post-crash (SPY, DDD, INFQ, VELO, SIDU, NTDOY all enter his rotation for the first time after Oct 2025) and **adds index-level 0DTE hedging** he never used before — the one durable behavioral change the data shows.

---

## 4. Behavioral & Sentiment Signals

### Why is he posting?
At 25.7 posts/week for 93 consecutive weeks, this is not a trade log — it's a **parasocial community-building habit inseparable from his trading**. The tag distribution makes this explicit:

| Tag | Count | Share |
|---|---|---|
| (untagged / plain commentary) | 1,625 | 67.7% |
| `Funny` | 300 | 12.5% |
| `News` | 223 | 9.3% |
| `Discuss` | 112 | 4.7% |
| `Gain` | 101 | 4.2% |
| `Dd` (due diligence) | 21 | 0.9% |
| `Chart`, `Yolo`, `Poll`, `Contest`, `Loss` | 19 combined | 0.8% |

**Only 21 posts in 2,401 (0.9%) are tagged as genuine due-diligence write-ups.** The overwhelming majority is reaction, humor, and community engagement — he is a **personality/entertainer first, analyst a distant second.**

### Engagement arc — a real leading indicator
Average comments and reactions per post **climbed steadily from Dec-2024 through a clear peak in Aug–Oct 2025** (avg. reactions rising from ~6 to ~46/post) — **exactly coincident with the ONDS mania and his portfolio's real peak ($596k, Oct 9)** — then **declined and never fully recovered** (settling back to ~26–31/post through 2026). **His own audience engagement is a usable, dated proxy for when his flagship thesis was most crowded** — engagement peaking is a better real-time top signal than anything in his own text.

### Recurring linguistic patterns
- **Self-aware confession without correction:** "I'm the worst at taking profits," "I was a crazy man," repeated for two years, never resolved by action.
- **Community/kinship language:** "brothers and sisters," "for the new kids," treats followers as an in-group he is teaching, not selling to.
- **Self-deprecating, quasi-religious humor about his own account:** "Port Jesus," "McGlitchy port value," "It begins" — he mocks his own hype rather than amplifying it uncritically, which is a mild positive tell (less pure grift, more genuine hobbyist) but does not prevent the same overconfidence from wrecking his book.
- **Life/business grounding:** frequent, unprompted references to his construction business ("carpentry, masonry, and concrete work," arguing with a supplier over door widths, "installing faucets... finishing HVAC trim" during the week his portfolio cratered) — strong evidence he is a genuine small-business operator trading a side account, not a full-time trader whose livelihood depends on it. This explains both the volume (he's often on-site, posting in bursts) and the emotional flatness during the crash (he has an unrelated income floor).
- **Reaction to red days:** unusually calm and transparent by AfterHour standards — he posts *through* the crash rather than going dark (contrast with typical survivorship-biased accounts), using dry humor ("Know that if you felt pain from the red days, so did I... Life goes on") rather than panic, denial, or revenge-trading language. He does not, however, translate that calm into risk reduction — he stays in the position.

---

## 5. Quantitative Verdict for TraderMatrix

### Primary and Secondary Algorithmic Classification Tags
- **Primary: `THEMATIC_MOMENTUM_DISCOVERY`** — genuinely early, genuinely good at surfacing small-cap thematic names (drone/defense/eVTOL/AI, SPAC-to-operator conversions) before they're crowded.
- **Secondary: `CONCENTRATED_OPTIONS_BAGHOLDER`** — cannot trim winners, rolls losing/overextended options positions further out in time rather than de-risking, adds to losers on the way down.
- **Tertiary: `SELF_DIAGNOSED_NON_CORRECTOR`** — uniquely valuable behavioral flag: he *tells you in advance*, in writing, what his flaw is and when it will recur. Treat his own self-criticism as a forward-looking risk disclosure, not idle commentary.

### Algorithmic Alpha Score & Expectancy
**Alpha Score: 46 / 100**

Rationale: genuine positive **selection alpha** (early, correct thematic ticker discovery — ONDS, ACHR, PLTR all identified well ahead of their crowd-recognition phase) is real and reproducible enough to be worth harvesting as an idea-generation signal. But it is **almost entirely destroyed by negative execution alpha** — a documented −93.1% real drawdown in 8 days from a single unmanaged, rolled, averaged-into options position, with no stop discipline ever observed despite explicitly prescribing it to others. The score reflects: strong idea generation (would score 70+ alone) severely discounted by catastrophic, repeated, self-acknowledged risk-management failure.

**Expectancy characterization:** **Positive raw idea expectancy, deeply negative risk-adjusted (Kelly-violating) expectancy.** His picks, taken at first mention and exited on a disciplined rule, would likely show a positive edge. His picks, followed at his own sizing and holding period, have a fat left tail that erases years of gains in single-digit numbers of days. **Artemis must decouple the idea from the execution — this is the single most important design implication of this dossier.**

### Signal Flow Ingestion Matrix

| Signal Type | Example Trigger | Artemis Action | Confidence |
|---|---|---|---|
| First-ever mention of a new small-cap/SPAC ticker (`Dd`-tagged or a fresh `$TICKER` never used before) | "$PUSA," "$JFB," early "$ONDS" curiosity post | **Ingest → watchlist**, independent verification required before sizing | Medium-High |
| "Rolled my [options] to [further-dated expiry]" | "$ONDS Calls Rolled to 2027" | **Fade / red flag** — historically marks a local top in that name, not a reload signal | High (n=1 major event, but textbook pattern) |
| "Added [on the way down] / nothing crazy / not really worried" | Post-drawdown averaging language | **Do not mirror sizing.** Treat as a toxic-averaging-down tell; if ingesting the underlying thesis at all, size independently and smaller | High |
| Sudden spike in his engagement (reactions/comments 2x+ trailing average) on a single name | Aug–Sep 2025 ONDS mania cluster | **Contrarian fade candidate** — treat as a crowding/sentiment-extreme indicator for that specific name, not a buy confirmation | Medium |
| `[Funny]`, meme, or community-banter post | ~12.5% of volume | **Ignore for signal purposes** — engagement/personality content, zero trade information | High |
| `[Discuss]`-tagged post during a broad market red day | "Took a day away… market went red," "Wow this week was rough" | **Do not treat silence-then-Discuss as "all clear."** These are his highest-value *risk* disclosures; log the position/ticker mentioned as actively bleeding, independent of his tone | High |
| Macro/political news repost (`[News]` tag, 223 posts) | Fed data, tariff/trade headlines | **Low-value as alpha** — largely aggregation of publicly available headlines with his gloss; use only as a sentiment/attention proxy, not a fundamental input | Low |
| Self-critical/confessional statement about his own trading psychology | "I'm the worst at taking profits" | **Meta-signal, not trade signal** — log as a standing risk-management override: any position he is currently holding should be assumed *not* to have a working exit plan | High (structural, confirmed across 2 years) |

### Specific Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Treat @TRON as a **discovery/screener feed for small-cap thematic and SPAC-conversion names**, not an execution model. His first mention of a new ticker in the drone/defense/eVTOL/robotics/AI cluster, or any SPAC/S-4 name, is worth adding to an independent watchlist for Artemis's own technical/fundamental screen.
2. His **macro-political thematic framing** (which policy shift benefits which sector) is directionally useful as a narrative-tracking input, even when the specific ticker isn't investable — cross-reference against `theme-detector` and `sector-analyst` outputs rather than trading it standalone.

**Contrarian Fade Directives (when to fade him / the retail herd around him):**
1. **Fade any "rolled my calls further out" or "diamond-handing" post** in his flagship name of the moment — historically coincides with the top, not a reload point.
2. **Fade retail herd enthusiasm when his engagement metrics spike** (reactions/comments materially above his trailing average) on a single ticker — this dossier shows his community engagement peaking exactly at his portfolio's real peak.
3. **Fade, don't follow, any post where he says he "added on the way down" / "not really worried"** — this is the exact behavior that produced the -93.1% collapse; treat it as sentiment exhaustion in the name, not conviction.

**Mandatory Risk Blacklists & Firewalls:**
1. **Never size a position to match his stated conviction language** ("all in," "would sell my whole port," "tattoo if it hits $100") — these are entertainment rhetoric, not risk-managed sizing, and have preceded his worst drawdown.
2. **Never mirror options duration extensions (rolls) as a reason to add.** A roll-to-further-expiry post from this account should trigger a *reduce*, not *add*, signal in any Artemis position sourced from his content.
3. **Treat his self-applied `[Gain]`/`[Loss]` tags as unreliable for backtesting** — 101 self-tagged gains vs. 1 self-tagged loss is not a real win rate; his documented amount_k series shows at least one catastrophic, untagged loss. Any signal-performance backtest using his tags as ground truth must be discarded or reweighted against the amount_k series instead.
4. **The `amount_k` series itself must be sanitized before use** — hard-exclude the 2025-08-08→08-11 "Port Jesus" glitch cluster (values >$1M are categorically false for this account) and flag the 2026-06 "challenge" relaunch as a probable account reset, not organic recovery.
5. **Toxic instrument flag: $ONDS options, specifically.** This single position produced the entire documented blow-up. Any Artemis exposure sourced from his $ONDS commentary should carry a hard position-size cap and a mandatory stop, overriding his own stated plan.

**Exit Rules & Alpha Rectification:**
1. **Impose an external profit-take rule on any idea sourced from him**, since he provides none: e.g., trim 25–50% of a position at +50% and again at +100%, since he has never once demonstrated this discipline despite prescribing it to others.
2. **Impose a hard stop (e.g., −20% from entry) on any position inspired by his content**, independent of his own holding behavior — his documented pattern is to average down through at least a −55% single-session move before capitulating at −93%.
3. **Treat any options roll-to-further-expiry in his flagship name as a mandatory Artemis exit trigger** for a mirrored position, not a hold signal.
4. **Re-evaluate exposure whenever his community engagement metrics spike** — use it as a crowding/topping proxy to trim, not add to, correlated Artemis positions in the same name.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone |
|---|---|
| 2024-11-25 | **First post** ("Intel is cooking") — CHIPS Act/reshoring thesis on $INTC; portfolio baseline $160,141 |
| 2024-11-26 | **Self-diagnosis, Post #3:** "I'm the worst at taking profits and I often wait until it is too late to take money off the table." — the thesis statement for his entire career on the platform |
| 2024-12-03 | Early $PLTR conviction call ("still printing," "won't be selling a single share") |
| 2024-12-05 | Early $ACHR support-level call (~$7 range) |
| 2025-01 | Portfolio value climbing steadily ($174k → $217k across January) |
| 2025-03-21 | $ONDS enters his universe as a self-described "super tiny... 2.7%... curiosity position" |
| 2025-05–06 | Portfolio surges to ~$400–545k; posting cadence hits a lifetime high (204 posts in June alone) |
| 2025-06-29 | Confesses to having overloaded $ONDS since April ("I was a crazy man... not sure what I was drinking") |
| 2025-08-08 to 08-11 | **"Port Jesus" glitch** — brokerage sync bug briefly shows $4.7M; he correctly identifies and mocks it as fake |
| 2025-09–10 | Engagement (comments/reactions) hits its lifetime peak; portfolio climbs toward its real high |
| 2025-10-02 | "My first $60k day!" — LEAPS-driven single-day gain, portfolio at $460,815 |
| 2025-10-08 | Rolls his core $ONDS options position out to 2027 expiry at the top |
| **2025-10-09** | **Real lifetime peak, $596,487.** Same day, market turns red; he adds options "on the way down," calling it "nothing crazy" |
| 2025-10-09 → 10-17 | **The blow-up: −93.1% real drawdown, $596,487 → $40,954, in 8 days.** Narrated in real time via `[Discuss]`-tagged posts, culminating in "I'm down a house in gains." |
| 2025-10-21 | "I'm posting less plays for a reason" — explicit acknowledgment of chasing/discipline struggles, states he remains fully in $ONDS, $NIO, $AGL regardless |
| 2025-11-13 | "$500 Degen Challenge" — his only ever `[Loss]`-tagged post, on an unrelated $500 novelty account |
| 2025-11 → 2026-01 | Posting cadence and engagement both remain depressed relative to pre-crash norms; portfolio chops in the $27k–$165k range |
| **2026-03-30** | **Lifetime absolute low, $27,490** ("Still the best defense battery play $ULBI") |
| 2026-06-02 – 06-15 | Portfolio jumps $33k → $120k in days; explicitly framed as "Challenge back on ($35k to more)" — a probable account reset, not organic recovery |
| 2026-07 → 09 | Portfolio stabilizes in the $390–420k band; **first appearance of 0DTE $SPY trading** in his history — a durable post-crash behavioral shift toward index-level hedging |
| 2026-09-10 | Report date — active same-day, portfolio at $413,927, still core-long $ONDS |

---

*End of dossier. Prepared for the Artemis Engine signal-ingestion pipeline. Cross-reference the sanitized `amount_k` series (glitch-excluded, reset-flagged) before any downstream backtest uses this subject's tagged posts as ground truth.*
