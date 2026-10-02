# The AfterHour Trader Style Guide: A Practical Framework for Copy-Trading and Signal Ingestion

## Data Provenance & Telemetry Warning
Before analyzing specific trader archetypes, the following quantitative firewall must be applied to all platform-synced data: Systematically mask all `amount_k = 0.0` readings occurring after a documented sync failure (specifically for accounts like **@883Ismygovtname** and **@DocHollywood**). These represent structured-field outages, not portfolio wipeouts. Conversely, treat sudden, unsustainable spikes—such as **@Bobdog’s** $10.79M telemetry anomaly in May 2026—as sync artifacts caused by illiquid option markups. These figures must be firewalled to maintain an accurate mark-to-market perspective.

---

## 1. Category: Options Income & "Wheel" Sellers

### Sector Analysis
The "Wheel" strategy facilitates a transition from erratic directional speculation to "mechanical harvesting." This process involves selling cash-secured puts (CSPs) to collect premium, and upon assignment, selling covered calls (CCs) against the underlying. This monetizes time decay (Theta) rather than relying on high-variance volatility.

### Traders to Follow
| Handle | Alpha Score | Primary Instrument Focus | Verified Capital Trajectory |
| :--- | :--- | :--- | :--- |
| **@Bobdog** | 74 | High-Beta Growth ($HIMS, $HOOD, $MSTR) | $24.6k (Oct 2024) → $1M+ (Sept 2026) |
| **@883Ismygovtname** | 58 | Mid-Cap Growth & Income ($ASTS, $SOFI) | $6k–$11k seed → ~$95k (Month 21) |

### Process Breakdown
*   **Account Segmentation Strategy:** **@883Ismygovtname** utilizes a sophisticated dual-account structure to optimize tax efficiency. The "Dream Team" (Traditional IRA) is used for tax-advantaged premium harvesting, while the "Pony Farm" (Taxable) utilizes 100-share "ponies" to run the Wheel. This system is designed to be self-funding, where premium income acquires more shares without further capital injections.
*   **Regime Shift Indicators:** **@Bobdog** employs the "Blue Star/Purple Star" system. "Blue Stars" indicate weekly bullish regime shifts for entry, while "Purple Stars" signal distribution and macro exhaustion.

### Ingest vs. Firewall
*   **Ingest (Copy):** Adopt the **70-90% profit-taking rule** utilized by **@883Ismygovtname**. Closing short options after 70-90% decay mitigates late-stage reversal risk and increases capital velocity.
*   **Firewall (Avoid):** Discard **@Bobdog’s "revenge sizing"** protocols, where leverage is aggressively increased following red days to recover losses. Simultaneously, firewall **@883Ismygovtname’s structural leak** of "selling winners too early"—closing high-conviction LEAPS for 10% gains before major thematic rallies.

---

## 2. Category: 0DTE & Index Scalpers

### Sector Analysis
Index scalping requires a rigorous technical framework centered on **Dealer Gamma/GEX (Gamma Exposure)**. This style ignores traditional "vibes," focusing instead on the price levels where market makers must hedge their positions, creating mechanical "walls" for intraday price action.

### Traders to Follow
*   **@ALLOY (Alpha Score: 47):** A former quantitative-risk engineer whose "PRISM" framework provides a mechanically stated structure for SPY/SPX trading based on dealer liquidity.

### Process Breakdown: GEX Positioning
Market makers must buy or sell the underlying index to remain delta-neutral as price moves. **GEX** identifies strike prices where dealer exposure is highest. These levels act as magnets or barriers, dictating the probable intraday range.

### Ingest vs. Firewall
*   **Ingest (Copy):** Utilize the **"Time-of-Day Volatility Windows"**. Specifically, target the **2:00 PM – 4:00 PM convexity zone**, which exhibits the high-volatility/high-theta characteristics necessary for specific intraday trade structures.
*   **Firewall (Avoid):** Discard the **"unresolved narrative"** of the $10k to $109k challenge. As the documentation simply stops without a closing balance, it must be treated as a terminal data point. Discard any narrative thread that lacks a verified, documented closing balance. Furthermore, disregard the 98% "Gain" tag ratio as extreme survivorship bias.

---

## 3. Category: Momentum & Swing Traders

### Sector Analysis
"Thematic Momentum" relies on industrial supply-chain intelligence. To be actionable, this must move from broad market sentiment to specific, primary-source geographic catalysts.

### Traders to Follow
*   **@Dallaslongcall (Alpha Score: 34):** This trader exhibited an equity curve with a **-97.9% maximum drawdown**, rendering his previous 270x growth statistically irrelevant for risk-adjusted portfolios.

### Process Breakdown: Geographic Alpha
The alpha in this strategy is not merely thematic (AI/Data Centers) but **geographic (North Texas)**. The edge is derived from primary-source construction leads—tracking groundbreakings and power-grid buildouts in the DFW area (e.g., Abilene, Red Oak) before they are priced in by the broader market.

### Ingest vs. Firewall
*   **Ingest (Copy):** Use the trader for **primary-source construction leads** and catalyst identification within the data center supply chain ($AMAT to $VST).
*   **Firewall (Avoid):** Reject the total lack of stop-loss discipline. The failure to apply defensive circuit-breakers resulted in a near-total wipeout, demonstrating that thematic brilliance does not compensate for negative execution expectancy.

---

## 4. Category: Long-Term Compounders

### Sector Analysis
Focus is on high-net-worth portfolio management, aiming for benchmark-beating returns through a "Mega-cap Core + Sector Basket" approach.

### Traders to Follow
*   **@DocHollywood (Alpha Score: 51):** An operator managing a multi-million dollar book with a verified annualized return of **~51%**.

### Process Breakdown: Leveraged Stock Substitutes
The mechanical "how" behind the outsized returns involves using **deep-ITM (In-The-Money) calls** as leveraged stock substitutes for mega-caps. This provides high delta and capital efficiency without the terminal decay risk of OTM gambling. This core is augmented by the "DIP Index"—a falsifiable, benchmarked basket of sector picks ($MRVL, $AAOI).

### Ingest vs. Firewall
*   **Ingest (Copy):** Replicate the ITM-call leverage strategy for core mega-cap holdings.
*   **Firewall (Avoid):** Avoid the **"scandal-adjacent bag-holding"** habit. Despite a strong core, the profile reveals a tendency to average down into structurally impaired or fraudulent names like $SMCI, $SAVA, and $LCID.

---

## 5. Category: Macro & Hedging Traders

### Sector Analysis
This category utilizes volatility ETPs and credit indices to navigate market shocks by categorizing volatility "velocity."

### Traders to Follow
*   **@Cynce (Alpha Score: 34):** A volatility specialist trading UVIX/SVIX based on a structured event-velocity framework.

### Process Breakdown: Event Velocity Theory
Market shocks are categorized by tier to determine trade duration:
1.  **Everyday:** Scheduled macro prints (CPI).
2.  **Surprise:** Geopolitical/earnings shocks.
3.  **Crisis:** Structural volatility requiring long-term hedging.

### Ingest vs. Firewall
*   **Ingest (Copy):** Implement the disciplined "loss-mitigation" mechanic of buying back short calls during a market crash to remove the upside cap, allowing the underlying shares to recover fully during the bounce.
*   **Firewall (Avoid):** Treat long periods of platform silence—specifically the **203-day blackout**—as an **"Accountability Black Hole."** If a trader ceases disclosure during a drawdown, their previous alpha is considered unverifiable. Additionally, avoid structural decay products like **VIXI** if held as long-term positions.

---

## 6. Category: Event-Driven & Special Situations

### Sector Analysis
Niche sourcing in specialized sectors, specifically Counter-UAS (CUAS) and defense optics.

### Traders to Follow
*   **@Drone_Daddy:** A specialist in high-alpha ticker sourcing within the defense-tech infrastructure.

### Process Breakdown: Niche Ticker Discovery
Edge is found in identifying "special situations" within government contract cycles and defense technology before they achieve mainstream recognition.

### Ingest vs. Firewall
*   **Ingest (Copy):** Ingest high-alpha ticker sourcing and specific catalyst identification for the defense sector.
*   **Firewall (Avoid):** Discard the "leverage-driven round-tripping." Account-level gains are frequently neutralized by poor position sizing and excessive leverage.

---

## 7. Category: Signal Vendors & Educators

### Sector Analysis
These accounts transition from execution to software/content vending, using social feeds as top-of-funnel marketing.

### Traders to Follow
*   **@ALLOY (Prism)** and **@Bobdog (Theta Daddies)**.

### Ingest vs. Firewall
*   **Ingest (Copy):** Extract "Community Wisdom" and Regime Shift indicators (Blue Stars).
*   **Firewall (Avoid):** Identify **"Commercial Incentive Contamination."** In these profiles, trade narration is often optimized for sales cadence and "growth-hacking" milestones rather than neutral, accurate documentation.

---

## 8. Category: High-Risk & "Fade" List

### Sector Analysis
Accounts targeting microstructure anomalies like "Halt Sniping" and "Reverse-Split Arbitrage."

### Traders to Avoid/Fade
*   **@AtypicallyErect (Alpha Score: 58 Idea / 22 Execution):** A profile exhibiting terminal behavioral red flags.

### Process Breakdown: Red Flag Definitions
*   **Corpse Yoga:** A terminal red flag defined as holding dead positions with the hope they return to life.
*   **Margin Call Behavior:** This account responded to a **margin call (Sep 4, 2026)** by "buying more" rather than de-risking. This indicates terminal risk. Cease all signal ingestion immediately upon such behavior.

### Ingest vs. Firewall
*   **Ingest (Copy):** Utilize the "Halt List" only as a universe filter for high-volatility discovery.
*   **Firewall (Avoid):** Hard-firewall all execution signals from this archetype.

---

## 9. Final Verdict: Edge vs. Storytelling

The quantitative data determines that **Real Edge** in this ecosystem is strictly found in **Mechanical Expectancy**—specifically the income-harvesting "Wheel" processes of **@Bobdog** and **@883Ismygovtname**. These strategies rely on the persistent mathematical reality of Theta decay and exhibit verified, contribution-adjusted capital trajectories.

Conversely, accounts such as **@Dallaslongcall** and **@ALLOY** represent **"Narrative Survivorship."** While their research (e.g., North Texas geographic alpha) is high-quality, their execution is characterized by high-variance and selective-disclosure win rates (90%+) that mask catastrophic drawdowns or unresolved narrative threads. **Prioritize process-driven income over story-driven momentum.** Copy the "Wheel" sellers for systematic growth; use the storytellers only for ticker discovery, never for risk management.