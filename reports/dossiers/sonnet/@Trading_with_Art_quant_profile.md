# Forensic Quant Autopsy: @Trading_with_Art

**Subject:** AfterHour trader `@Trading_with_Art` (`prf_61eb70e387e64d7281e723dbb4784ea2`)
**Rank:** #34 most-active followed trader — 122 lifetime posts
**Coverage:** 2025-12-06 → 2026-09-04 (272 days / 38.9 weeks)
**Sources:** `@Trading_with_Art_lifetime.md` (full text, 122 posts), `@Trading_with_Art_all_posts.json` (structured metadata: `tag`, `gain_loss`, `amount_k`, `tickers`, engagement)
**Analyst:** Artemis Engine — Sonnet dossier pass

**Methodology note — this is one of the more genuinely verifiable accounts in the followed-trader cohort, with one large caveat.** `gain_loss` is populated on only 2/122 posts (both "Gain," no dollar figure attached to a loss ever appears in the structured field) and is not usable on its own. `amount_k`, however, is populated on 106/122 posts and — unusually for this cohort — tracks a coherent, internally consistent account-value curve for the first 16 weeks of the archive ($52.82K → $58.09K → $50.23K → $53.62K, see §1), cross-validated almost exactly by the subject's own narrated numbers ("up double digits on the year… down 14% at the worst point," "down 4.3% YTD," Post #93, 2026-02-07). **After 2026-03-26, `amount_k` reads a flat 0.0 on every remaining post through 2026-09-04** — not because the account went to zero, but because the scraper finds no dollar-denominated portfolio figure in the text at all: the subject stops disclosing any dated, dollar-denominated trade or portfolio update for the final 23 weeks of the archive (5+ months), a period that exactly coincides with his pivot from disclosed CSP-wheel trader to SaaS-platform founder/promoter (see §1, §3). Every dollar figure in this dossier before 2026-03-26 is self-reported but well-corroborated; every claim after that date is content, not disclosure, and should be read accordingly.

---

## 1. Executive Profile

### Who he is
A self-described **Senior/Lead Machine Learning Engineer** ("building AI agents by day"), based in Miami, who also instructs at "one of New York's top growing trading academies" (mentored 50+ people, paid for fewer than 10). He is not an anonymous retail poster: over the course of the archive he **co-founds a real, commercial options-flow SaaS platform — TraderDaddy Pro — with `@mphinance`** (launched 2026-03-10, relaunched/rebranded as **TraderMatrix** on 2026-09-01), and separately sold his own $6.99/month Pine Script indicator suite in February 2026. This is the single most important classification fact in this dossier: for roughly the back half of the archive, `@Trading_with_Art` is not primarily a trade-caller being observed for edge — he is a **platform founder using the account to build and sell a product**, in the same commercial cluster as `@mphinance`, `@Freeballer`, and `@Drone_Daddy` already flagged elsewhere in this cohort (Pathfinders, the ONDS CEO webinar, cross-affiliate promotion). Any downstream classification must weight his post-March-2026 content as marketing collateral first and market commentary second.

### Trading philosophy
In his own words (Post #1, first-ever post): **"Senior ML Engineer building AI agents by day. Premium seller + swing trader by night."** The stated system is explicit and mechanical:
- **Weekly cash-secured puts (CSPs), 7 DTE**, targeting **1% of portfolio per Friday** ($520/week on a $52K account), re-struck every week based on "systematic strike selection."
- Explicit aversion to assignment ("I actually hate being assigned… my goal is to almost never get assigned") but a stated fallback of running the **full wheel** (covered calls against assigned shares) when it happens.
- A secondary layer of **high-conviction swing trades on clean technical setups**, using custom TradingView indicators (Fibonacci/pivot overlay, buy/sell volume split, a 12-indicator weighted oscillator) that he later commercializes.
- A **stated Year-1 goal of $52K → $87K** (+67%) through compounding weekly 1% gains — an explicit, falsifiable target, which is rare in this cohort and makes this account unusually easy to grade against its own stated benchmark (see §3).

This genuine trading identity is real for roughly the first four months of the archive, then is substantially supplanted by a second identity: **SaaS founder and free-content marketer**, running a 31-day "give away free education" essay series (August 2026) and long-form weekly "Sunday DD" macro/options-structure breakdowns explicitly "sourced from Trader Daddy Pro," his own product.

### Post cadence
- **Raw average: 122 posts / 38.9 weeks ≈ 3.1 posts/week** across the full archive — but this number is meaningless without splitting the archive, because the shape is a steep decay, not a steady cadence.
- **The archive is almost entirely front-loaded.** 68 of 122 posts (56%) land in **December 2025 alone**; 91 of 122 (75%) land in Dec 2025–Jan 2026. From there: Feb 2026 = 8 posts, March 2026 = 10 posts, then **April and May 2026 = zero posts** (a 9.3-week total silence), then June–September 2026 = 13 posts total.
- **"Dense/disclosed" window: 2025-12-06 → 2026-03-26** (109 of 122 posts, 15.7 weeks, **≈6.9 posts/week**) — this is the entire disclosed-trading period and the only window with a verifiable equity curve.
- **"Post-pivot" window: 2026-06-01 → 2026-09-04** (13 posts, 13.6 weeks, **≈1.0 post/week**) — product launches, philosophy essays, and macro-structure content; zero dated trade or portfolio disclosures.
- **The engagement data inverts the intuitive read.** Views in the dense/disclosed trading window: **median 8, average 34, max 647** (n=109). Views in the post-pivot window: **median 1,647, average 2,069, max 4,967** (n=13) — roughly a **60–200x jump in reach** that occurred exactly when he stopped disclosing individual trades and started (a) marketing TraderDaddy Pro/TraderMatrix and (b) publishing free, non-positional "Sunday DD" macro essays. **His actual AfterHour audience was built by the content he produced after he stopped being a disclosed trader**, not by his CSP-wheel track record. Any signal-ingestion pipeline weighting this account by "engagement" will systematically overweight his least verifiable, most commercially-motivated period.

### Verified capital trajectory & drawdown history
This is a real, datable equity curve for the one window it exists (`amount_k`, thousands, cross-validated against narrated $ figures):

| Date | Account value | Note |
|---|---|---|
| 2025-12-06 | $52.82K | First post — stated Year-1 goal $52K → $87K |
| 2025-12-17 | $51.24K | Early dip (-3.0% from start) |
| 2026-01-01 | $54.43K | +3.0% since inception |
| **2026-01-24** | **$58.09K** | **Peak, +10.0% from inception** — coincides with the Freeballer-hosted $ONDS CEO (Eric Brock) webinar week |
| **2026-02-14** | **$50.23K** | **Trough, -13.5% off the Jan 24 peak, -4.9% off inception** — coincides in real time with his own "Markets Just Wiped $3.6 Trillion in 90 Minutes" post (2026-02-13) |
| 2026-03-10 | $54.15K | Recovery, coincides with the TraderDaddy Pro launch post |
| 2026-03-19 | $52.84K | Gives back most of the March bounce |
| **2026-03-26** | **$53.62K** | **Last disclosed figure in the entire archive.** Net change from inception: **+1.5% over 16.1 weeks**, against a stated pace (1%/week) that implies roughly **+17%** over the same span — a documented **~90% shortfall against his own stated target**, before disclosure stops entirely. |
| 2026-03-27 → 2026-09-04 | **No disclosure** | Zero dated, dollar-denominated trade or portfolio updates for the remaining 23 weeks of the archive |

**He self-narrates the drawdown directly and it matches the scraped curve closely** (Post #93, 2026-02-07): *"I watched my wheel strategy portfolio go from up double digits on the year to down 14% at the worst point... As of right now, I'm down 4.3% YTD."* The -14%-at-worst figure matches the -13.5% computed from `amount_k` almost exactly — a rare instance in this cohort where the structured PnL-adjacent field and the subject's own words agree, which raises confidence in everything he discloses *inside* this window and makes the total silence *outside* it more conspicuous by contrast, not less.

---

## 2. Ticker Universe & Catalysts

### Two structurally different behaviors, easily conflated
1. **The real book: a diversified, mechanical CSP-wheel rotation.** Structured `tickers` field populated on 65/122 posts, spanning **171 unique tickers** — but the actual weekly-income trades cluster on a repeatable small set of liquid mid-caps traded with real strikes, premiums, and expirations: `$HOOD` (6), `$ONDS` (6), `$ORCL` (6), `$PATH` (5), `$MRVL` (5), `$BBAI` (4), `$LULU` (4), `$TSLA` (4), `$ALAB` (4), `$AVGO` (4), `$RKT`, `$APLD`, `$SERV`, `$RR`, `$QCOM`, `$CRM`, `$ADBE`, `$UPS` (2 each). $SPY (9) and $QQQ/$NVDA/$SMH are index/macro-level commentary, not CSP underlyings.
2. **Content watchlists with no positions attached.** Dec 27–31, 2025: a 10-post **"Power 5 for 2026"** series (AI Infrastructure, Energy, Biotech, Aerospace/Space, Industrial Automation, Cybersecurity, AgriTech, Fintech, Mobility/EV, Quantum Computing) naming **50–70 additional tickers** with percentage-upside color commentary and zero entries, strikes, or sizes. **None of these names recur with a trade disclosure anywhere in the remaining 8-plus months of the archive.** This is pure idea-generation/content, not his book, and should never be attributed to him as a position.

### Options vs. equities vs. macro
- **CSP-wheel mechanics (his genuine, teachable core competency in the dense window):** weekly 7-DTE puts, explicit strike/premium/expiration disclosure (e.g., "$RKT 12/19 $18P — OPENED @ $0.23," "$BBAI 12/19 $6.5P — OPENED @ $0.28"), laddering strikes down on the same name, closing early for a partial-profit ("Closed my $MRVL $85 CSP… Bought back at $0.20 originally sold for $0.85"), and an explicit "wheel through it" plan on assignment (`$AVGO`, `$BBAI`).
- **Earnings-week IV plays:** `$ORCL`, `$AVGO`, `$LULU` CSPs timed to earnings prints, with a documented three-part "Understanding Earnings" educational series (2025-12-13).
- **Swing setups with defined risk (Chart-tagged posts):** `$UPS` (+3% target, defined stop, hit), `$HOOD` (near-miss on target), `$QCOM` (defined stop at $177.50), `$IRBT` (correctly flagged short-squeeze setup, +60% realized by other posters).
- **Macro/options-structure overlay (dominant content mode from Feb 2026 onward):** GEX/gamma-flip levels, put-wall/call-wall clustering, VIX-term-structure contango percentile analysis, dealer-hedging delta mechanics, credit-spread and MOVE-index cross-checks. Genuinely sophisticated and internally consistent (see §5), but consistently **presented without a corresponding position** — it is analysis-as-content, not disclosed trading.
- **$ONDS specifically** is **not an originated conviction call** from this account — it is amplification of the Freeballer-hosted Eric Brock (ONDS CEO) webinar (Post #88–90, 2026-01-22/23), already flagged in this cohort as a structural promotional-entanglement event. `@Trading_with_Art`'s role is explicitly secondary: promoting attendance ("this is our chance to go beyond the chart"), then publishing an "Understanding Exercisable Warrants" explainer the next day, framed as education rather than a trade call.

---

## 3. Risk Management & PnL Reality

### Does he take profits or hold bags? Genuinely mixed, well-disclosed early, then undisclosed entirely
- **Real profit-taking is documented with numbers:** `$MRVL` CSP closed at 65% of max profit to free capital; `$ORCL` earnings CSP closed "in profits" after a rough morning; `$BBAI` CSPs "closed... for about 65% profit collection" before re-laddering lower; `$UPS` swing hit its +3% target and was closed.
- **Real misses are disclosed too, at least early on** — consistent with his own stated promise ("Full transparency — I'll show the misses too"): Post #24/25 (2025-12-11), the week's 1% target is explicitly abandoned mid-week ("the 1% target for this week will not be hit… making about 0.20% this week now"); `$LULU`/`$ALAB` stopped out for a realized loss the same week ("I took the loss ❌… For transparency I am showing the loss").
- **This transparency does not survive the archive.** After 2026-03-26 there is no further weekly-target scorecard, no further disclosed stop-out, no further assignment update — the entire accountability loop he built his brand on in December simply stops, concurrent with the TraderDaddy Pro launch.

### How he manages losing positions
- **The wheel is used as intended risk-transfer mechanics on paper** (assignment → sell covered calls → work the cost basis down), correctly explained in a dedicated "Assignment Math Nobody Talks About" post (2025-12-16).
- **But the wheel is also used as a bagholding-with-a-plan mechanism in practice.** `$AVGO`, 100 shares @ $365.44, marked at -$4,096 (-11.2%) unrealized (Post #44, 2025-12-17), framed explicitly as **"Peace > Profit"** — a genuinely calm, non-panicked position update, but with no stated stop, no defined invalidation level, and no resolution documented anywhere later in the archive. "I have a plan to work my way out" is a philosophy, not a risk rule.
- **One explicit, self-admitted rule violation:** the `$HUMA` trade (Post #60, 2025-12-29) — *"I broke my own rules because I got caught up in the excitement... jumped in without doing proper DD... Result: -XX% loss."* He redacts the actual loss percentage even while publishing a full "don't be someone's exit liquidity" lecture on the same mistake — a real accountability gap between the standard he holds his readers to and the standard he applies to his own disclosure.
- **An undisciplined equity buy is admitted almost as a throwaway line** during the February drawdown post: *"bought 100 shares at $85 thinking wow this is great and then it went to $70 lol"* ($HOOD) — no stop, no size rationale, played for a laugh rather than analyzed. This directly undercuts the "position sizing saved me" framing in the same post.

### Documented wins vs. blow-ups

| Category | Evidence |
|---|---|
| **Best documented wins** | `$MRVL`, `$ORCL`, `$UPS` CSP/swing closes at or near target, fully dated with strikes/premiums; correctly flagged `$IRBT` short-squeeze setup a day before it ran 60%; survived a real, dated **-13.5% to -14% portfolio drawdown** (Feb 2026) without a margin call or forced liquidation, by his own and the scraped data's account |
| **Worst documented failures** | `$HUMA` rule-violation loss (magnitude redacted by the subject himself); `$AVGO` -11.2% unrealized position with no stated exit plan, never resolved in-archive; **net realized return of only +1.5% over the 16.1-week disclosed window against a self-stated 1%-weekly (~17%) target** — a ~90% shortfall against his own explicit, falsifiable goal; **total absence of any dated PnL disclosure for the archive's final 23 weeks (61% of its timeline)**, despite continued, increasingly high-reach posting |

**Bottom line:** in the one window where this account is actually auditable, the mechanics are genuine, the disclosure is honest (including of misses), and the result is a real but **modest, sub-target, round-tripped outcome** — a trader whose stated system underperformed its own explicit benchmark once a real drawdown hit, but who did not blow up. Everything after that window is unauditable by design, not by omission — the account's entire second half functions as content marketing for a real commercial product, with market commentary used to source and legitimize it ("this data I am sourcing from Trader Daddy Pro").

---

## 4. Behavioral & Sentiment Signals

### Why is he posting? Three sequential, overlapping motives
1. **Dec 2025–Mar 2026: build-in-public trader/educator.** The stated goal (Post #1) is to document a real CSP-wheel account transparently, including misses, and to teach mechanics (assignment math, CPI vs. Core CPI, quad witching, options-chain liquidity). This period is his most credible and highest-integrity content.
2. **Feb–Mar 2026: indicator-suite and platform launch.** The $6.99/month Pine indicator suite (2026-02-22, explicitly disclosed as partly AI-assisted code) and TraderDaddy Pro (2026-03-10, co-founded with `@mphinance`, 50% launch discount code, 40%-of-profits affiliate program) both launch inside the same window his trade disclosure quietly stops. He is candid about the commercial motive ("the reason I charge anything at all is simple... it's a commitment") but the effect on the account's content is the same regardless of sincerity: verifiable trading content is replaced by product content.
3. **Jun–Sep 2026: pure content marketing, dressed as generosity.** "True Success Grows in Silence" (2026-06-01, a $1-first-month flash sale with "250 slots... we won't ever do this again"), a competitor-response post (2026-07-26), a 31-day "free education" series that **stops at day 5** (2026-08-24 → 08-29, never resumes through the archive's close), and the TraderMatrix rebrand launch (2026-09-04, a "first 100 people only" $39.98/month bundle). The pattern of **announcing large public commitments and not completing them** — the 1%-weekly disclosure cadence (quietly dropped after week 3), the "31 days straight" series (stopped at day 5) — is a recurring behavioral tell independent of any single instance.

### Recurring linguistic patterns
- **"Full transparency" / "not financial advice" / "do your own research"** as a near-constant disclaimer prefix, most dense in the Dec 2025 dense window and largely absent from the post-pivot content, where the promotional framing ("this is a promotion post... skip ahead if not interested") is stated more plainly instead.
- **"Peace over profit" / psychological-acceptance framing** used specifically to narrate unrealized losses (`$AVGO`) — a legitimate emotional-regulation stance, but one that is never paired with a stated invalidation level, so it functions as a substitute for a stop-loss rather than a complement to one.
- **Weekend "life philosophy" essays** (money/character two-parter, Valentine's Day "role of men" post, the August "patience is a skill" series) recur on a roughly weekly cadence and consistently outperform his ticker-specific content on engagement in the post-pivot window — his audience responds to his voice and worldview more than to any specific call.
- **Anti-hype self-positioning used to sell hype-adjacent products** — repeated claims of "no upsells, no paywalls, no discord to join" sit directly alongside three successive paid product launches with artificial scarcity mechanics (a 50%-off code, a "250 slots, never again" flash sale, a "first 100 people only" bundle). The claim and the mechanic are in tension throughout the back half of the archive.
- **Explicit AI-tool disclosure**, twice: Pine Script indicator code ("a good chunk of the code was AI-assisted," 2026-02-22) and a standing recommendation to use Grok/ChatGPT for a 3-layer fundamental risk-diagnostic framework (2025-12-17) — consistent with the AI-content-adoption pattern already flagged for other accounts in this cohort (`browndog`, `Freeballer`).

### Reaction to volatility / red days
- **The one real, dated drawdown (Feb 2026) is narrated with unusual composure and honesty for this cohort** — explicit numbers, explicit "I'm down 4.3% YTD," explicit "if you need to take a break, take it" advice to followers, no bravado, no denial.
- **The very next post (2026-02-14) pivots directly to a long-form Valentine's Day essay on masculinity**, with zero further trade-level follow-up on the drawdown — the emotional processing happens, but the position-level accountability does not (no named ticker is confirmed closed, stopped, or held through, from that specific drawdown window).
- **The largest sustained volatility narrative in the archive (the Aug 2026 "Sunday DD" series: contango at the 99.6th percentile, VIX/Core-3M correlation break, margin debt at highs, a "fragile, not bearish" thesis)** is his most technically dense, best-received content by a wide margin (up to 4,967 views) — and is entirely non-positional. He calls the setup, not a trade.

---

## 5. Quantitative Verdict for TraderMatrix

### 5.1 Algorithmic Classification Tags

**Primary:** `CSP_WHEEL_INCOME_SELLER_DISCLOSED_WINDOW` — a genuine, mechanically documented weekly cash-secured-put income strategy (7 DTE, ~1% weekly target, systematic strike laddering, full-wheel-on-assignment), fully auditable for a 16.1-week window (2025-12-06 → 2026-03-26) via a cross-validated equity curve, but never resumed or re-disclosed for the remaining 61% of the archive's timeline.

**Secondary:** `SAAS_FOUNDER_CONTENT_MARKETER` — co-founder (with `@mphinance`) of a real commercial options-flow platform (TraderDaddy Pro → TraderMatrix, three successive paid launches with scarcity mechanics), whose account content transitions from disclosed trading to product marketing and non-positional macro/options-structure essays exactly at the point trade disclosure stops. This is the dominant mode for the back half of the archive and drove essentially all of the account's audience reach (60–200x the view count of the disclosed-trading period).

**Tertiary (genuinely useful, non-tradeable):** `OPTIONS_MECHANICS_EDUCATOR` — a real, teachable body of options-structure content (assignment math, quad witching, CPI/Core CPI, bid/ask/OI liquidity checklist, dealer delta-hedging mechanics, VIX-term-structure contango framework) that is internally consistent and well above typical retail-creator quality, independent of whether his own trading record is verifiable.

**Blacklist/conflict tag:** `FOUNDER_PRODUCT_ENTANGLEMENT` — from 2026-03-10 onward, this account is a promotional channel for a product this trader co-owns and profits from directly (not merely an affiliate relationship, as with the Freeballer/ONDS pattern already flagged in this cohort — a full ownership stake). Market commentary sourced "from Trader Daddy Pro" cannot be treated as an independent read once the platform is his own revenue line.

**Watch tag:** `DISCLOSURE_BLACKOUT_POST_2026-03-26` — flag that zero dated, dollar-denominated trade or portfolio disclosures exist anywhere in the final 23 weeks of the archive; any future post that resumes this format should trigger a dossier refresh.

### 5.2 Algorithmic Alpha Score & Expectancy

**Alpha Score: 38 / 100**

Rationale:
- **+ (genuine, teachable CSP-wheel mechanics, ~10 pts):** strike/premium/DTE disclosure, laddering, and full-wheel logic are specific, correct, and rare at this granularity in this cohort.
- **+ (rare, cross-validated equity curve, ~12 pts):** the `amount_k` trajectory and the subject's own narrated drawdown numbers ("-14% at the worst point," "-4.3% YTD") agree almost exactly — one of the few accounts in this cohort where the structured data and the qualitative claim corroborate each other for an extended window.
- **+ (honest early-period loss disclosure, ~8 pts):** explicit weekly-target misses, a named stop-out, and a self-admitted rule-violation loss (`$HUMA`) — better self-accountability than cohort average, for as long as it lasted.
- **+ (technically sound, internally consistent options-structure content, ~8 pts):** the Aug 2026 "Sunday DD" series (contango percentiles, gamma-flip levels, correlation-break framework) is genuinely well-constructed and usable as an options-mechanics literacy corpus.
- **− (total disclosure blackout for 61% of the archive's timeline, ~15 pts):** no verifiable PnL, position, or portfolio update of any kind exists after 2026-03-26, despite continued and increasingly high-reach posting.
- **− (documented, quantified underperformance vs. his own stated target, ~10 pts):** +1.5% realized over 16.1 weeks against a self-stated ~17% (1%/week) pace — a ~90% shortfall on his own explicit, falsifiable benchmark, before disclosure stops.
- **− (structural founder conflict of interest, ~12 pts):** three successive paid-product launches (indicator suite, TraderDaddy Pro, TraderMatrix) run through the same account that once disclosed trades, with market commentary now sourced from the product he sells.
- **− (broad, unfollowed-up sector-dump content, ~5 pts):** ~50-70 tickers across the "Power 5" series with zero subsequent entries anywhere in 8+ months — pure content dilution if mistaken for positioning.
- **− (pattern of abandoned public commitments, ~3 pts):** the 1%-weekly disclosure cadence and the "31 days straight" content series were both announced and both quietly dropped early, without acknowledgment.

**Expectancy: WEAKLY POSITIVE-TO-FLAT, materially below the subject's own stated target, for the one verifiable 16.1-week window (+1.5% net vs. a ~17% stated pace); UNVERIFIED / NOT APPLICABLE for the remaining 61% of the archive**, which contains commentary and product marketing but no disclosed trades to compute an expectancy from at all.

### 5.3 Signal Flow Ingestion Matrix

| Post Signature | Underlying Signal Type | Reliability | Artemis Action |
|---|---|---|---|
| Weekly CSP disclosures (strike/premium/DTE/assignment), Dec 2025–Mar 2026 | Documented, mechanical options-income process, cross-validated equity curve | Moderate-High (internally consistent, best-verified data in this account) | **INGEST** as calibration data for the Engine's own CSP/wheel strike-and-DTE selection logic; treat as a closed, historical case study, not a live feed |
| Assignment-then-wheel disclosures (`$AVGO`, `$BBAI`) | Bagholding absorbed into "the wheel" rather than actively risk-managed | Moderate | **LOG** as a case study of assignment-as-deferred-risk; do not treat wheel continuation as risk-neutral |
| "Power 5 for 2026" sector-dump series (10 posts, ~50-70 tickers, Dec 27–31) | Broad, unpositioned thematic watchlist | Low (zero follow-through in 8+ months) | **DO NOT** attribute as trading conviction; may seed independent screening only, with no weight from his endorsement |
| $ONDS content (Jan 2026) | Amplification of a Freeballer-hosted, promotionally-entangled CEO webinar | Low | **FADE/DISCOUNT** — same conflict-of-interest logic already applied to the Freeballer dossier; this is derivative, not original, conviction |
| "Sunday DD" macro/options-structure essays (Aug 2026 onward) | Sophisticated, internally consistent options-market-structure literacy content, non-positional | Moderate-High as education; Low as a directional signal | **INGEST** for options-mechanics calibration; **DO NOT** size off the directional "read" — no position or track record is attached to it |
| TraderDaddy Pro / TraderMatrix / Vespryx launch and relaunch posts | Founder self-promotion of an owned commercial product | N/A as a trading signal | **FIREWALL** — treat all commentary citing this platform as its data source as commercially motivated; do not treat as independent confirmation |
| Self-reported drawdown/PnL narrative (Feb 2026, "-14%," "-4.3% YTD") | Self-reported account performance, cross-validated against `amount_k` | Moderate (rare corroboration in this cohort) | **LOG** for sentiment/drawdown-tolerance calibration; still unaudited against any brokerage record |
| Psychology/life-philosophy essays (money/character, patience, Valentine's Day) | Not a trading signal | N/A | **IGNORE** for trading; may log posting cadence here as a meta-indicator that attention has shifted away from markets |

### 5.4 Execution Directives for the Artemis Engine

**Ingestion Directives (genuine edge to harvest):**
1. Extract the disclosed CSP-wheel parameters (7 DTE weekly rotation, ~1% weekly premium target, strike-laddering on the same underlying, full-wheel continuation on assignment) as calibration inputs for the Engine's own short-put income module — real, specific, teachable process from the one window it is verifiable.
2. Harvest the Aug-2026 options-market-structure essays (contango-percentile framework, VIX-vs-Core-3M correlation break, gamma-flip levels, the five-second bid/ask/OI liquidity checklist) as a distilled options-mechanics literacy layer, independent of the subject's own trading record.
3. Use the documented **~90% shortfall against his own stated 1%-weekly target** as a real-world base-rate check: even a numerate, mechanically disciplined seller undershoots a "simple" income target by a wide margin once a real drawdown hits — a useful sanity constraint against overpromising Engine-generated income targets downstream.

**Contrarian Fade Directives (when to fade him / the retail herd):**
1. Fade the "Power 5" broad sector-dump content — ~50-70 tickers with zero follow-through across 8+ months is content volume, not curated conviction.
2. Discount any market commentary explicitly sourced from "Trader Daddy Pro" / TraderMatrix from 2026-03-10 onward — distinguishing genuine market read from content marketing for his own product is not reliably possible from text alone.
3. Treat `$ONDS` content from this account as fully derivative of the Freeballer-hosted promotional arc already flagged in this cohort; do not double-count it as independent confirmation of that thesis.

**Mandatory Risk Blacklists & Firewalls:**
1. **Never size off this account's PnL for any date after 2026-03-26** — zero dated, dollar-denominated disclosures exist for the remaining 23 weeks of the archive, despite continued and higher-reach posting.
2. **Firewall all TraderDaddy Pro / TraderMatrix / Vespryx-branded content** as commercially motivated; do not treat platform-sourced data citations as independent third-party validation.
3. **Net the disclosed misses against the disclosed wins before crediting the CSP-wheel strategy** — the account's own numbers show a ~90% shortfall against its own stated target over the only fully auditable window; do not cite the "hit target" posts in isolation.
4. **Do not credit the Feb 2026 "-14% drawdown, survived on position sizing" narrative as proof of disciplined risk management in isolation** — the same window contains an admitted, unsized, un-stopped equity buy (`$HOOD`, "bought... thinking wow this is great and then it went to $70 lol").

**Exit Rules & Alpha Rectification:**
1. Any CSP-wheel parameters harvested from this account should still run through Engine-native strike/delta/DTE selection and position-sizing rules, never the subject's own stated targets — his realized result trailed his own target by a wide margin in the one window it can be checked.
2. **If dated, dollar-denominated trade disclosure ever resumes on this account, re-open this dossier** — a second verifiable window would allow an actual multi-period expectancy calculation instead of a single 16.1-week estimate.
3. Apply the same **founder/commercial-entanglement discount** already established for the Freeballer dossier, but at a higher severity tier: Freeballer's ONDS relationship was an arranged-access/affiliate entanglement; this account's TraderDaddy Pro/TraderMatrix relationship is a **direct ownership stake**, and should be discounted accordingly whenever the Engine encounters an account that both calls trades to an audience and sells that same audience a paid analytical product.

---

## 6. Chronological Milestone & Catalyst Log

| Date | Milestone / Catalyst | Notes |
|---|---|---|
| 2025-12-06 | **First post.** $52.82K account, weekly CSP + swing strategy disclosed in full mechanical detail; Year-1 goal stated as $52K → $87K | Most transparent, most falsifiable opening post in the archive |
| 2025-12-08 to 12-12 | `$ORCL`, `$LULU`, `$AVGO` earnings-week CSPs opened, closed, and one assignment (`$AVGO`) | Genuine, dated options-income mechanics on display |
| 2025-12-10 | `$IRBT` volume call flagged a day ahead of a 60% short-squeeze move | Best single directional call in the archive |
| 2025-12-11 | **`$LULU`/`$ALAB` stop-out disclosed** ("I took the loss"); weekly 1% target explicitly missed (0.20% realized) | Honest early-period loss/miss disclosure — does not recur later in the archive |
| 2025-12-16 | "The Assignment Math Nobody Talks About" published | Genuinely teachable wheel-mechanics content |
| 2025-12-17 | `$AVGO` position marked -11.2% unrealized, framed as "Peace > Profit," no stop stated | Never resolved or revisited later in the archive |
| 2025-12-27 to 12-31 | **"Power 5 for 2026" series** — 10 posts, ~50-70 tickers across 10 sectors, zero positions attached | Pure content/watchlist dump; none of these names recur with a trade disclosure |
| 2026-01-01 | $54.43K account value; "12 High-Conviction Plays for 2026" consolidated post | |
| **2026-01-22/23** | **$ONDS CEO (Eric Brock) webinar, hosted by `@Freeballer`** — this account promotes attendance and publishes a warrant-mechanics explainer the next day | Amplification, not origination, of an already-flagged promotional-entanglement event |
| **2026-01-24** | **Account value peaks at $58.09K (+10.0% from inception)** | Highest point of the entire disclosed equity curve |
| 2026-02-04 to 02-08 | Big-tech-selloff/defensive-rotation commentary; account value already declining toward $56.5K | |
| **2026-02-07** | **Explicit drawdown disclosure**: "up double digits on the year... down 14% at the worst point... down 4.3% YTD" | Rare, well-corroborated self-reported PnL narrative |
| **2026-02-13/14** | **"Markets Just Wiped $3.6 Trillion in 90 Minutes"** post, immediately followed by account trough at **$50.23K (-13.5% off the Jan 24 peak)** | Real, dated drawdown coincident with a genuine market-wide event he covered in real time |
| 2026-02-22 | Launches a $6.99/month Pine Script indicator suite, disclosing partial AI-assisted code | First commercial product; precedes the platform launch by 2.5 weeks |
| **2026-03-10** | **TraderDaddy Pro launched**, co-founded with `@mphinance`; $34.99/month, 50%-off launch code, 40%-profit affiliate program | The defining commercial pivot of the archive |
| **2026-03-26** | **Last dated, dollar-denominated trade/portfolio disclosure in the entire archive** ($53.62K, +1.5% net since inception) | All subsequent content is commentary or product marketing, never disclosed PnL |
| 2026-03-27 to 2026-05-31 | **Total posting silence** (9.3 weeks) | No explanation given in-archive at the time |
| **2026-06-01** | **"True Success Grows in Silence"** — reveals the silence was building TraderDaddy Pro; announces a "250 slots, $1 first month, never again" flash sale | First engagement-reach inflection point (2,677 views vs. a ~34-view dense-window average) |
| 2026-07-14, 07-26 | Macro/inflation commentary; a competitor-response post defending TraderDaddy Pro's pricing | Continued non-positional macro content |
| **2026-08-16 to 08-30** | **"Sunday DD" series begins**, then a self-declared "31 days straight of free educational posts" — **stops at day 5** (2026-08-29) and is never resumed | Highest-engagement, most technically sophisticated, and least verifiable-as-trading content in the archive (up to 4,967 views); the announced 31-day commitment is abandoned without acknowledgment |
| **2026-09-01** | **TraderDaddy Pro rebranded to TraderMatrix** | |
| **2026-09-04** | **"How To Escape The Matrix"** — TraderMatrix relaunch post, "first 100 people only" $39.98/month bundle including the "Vespryx" dealer-levels tool; archive closes | Final post is a product launch, not a trade disclosure |

---

*End of dossier. Prepared from `@Trading_with_Art_lifetime.md` (122 posts, full text) and `@Trading_with_Art_all_posts.json` (structured metadata) with no external data sources. The `amount_k` field was found unusually reliable and internally corroborated for the 2025-12-06 → 2026-03-26 window and unusable (flat 0.0, no signal) thereafter; all financial claims herein are self-reported by the subject and unaudited against any brokerage record, and the account's co-ownership of TraderDaddy Pro/TraderMatrix should be treated as a standing structural conflict of interest for all content dated 2026-03-10 or later.*
