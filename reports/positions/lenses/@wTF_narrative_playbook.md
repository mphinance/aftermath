# @wTF — Narrative vs. Tape, and the Playbook

*Lens: what they said vs. what the broker-verified snapshots show, and what's transferable. Account ran ~$33M–$95M, Oct 2023 – Apr 2025 (411 posts, 338 account snapshots, 414 change events). All figures below are pulled directly from `data/following/@wTF_all_posts.json` and `data/positions/@wTF_positions.json`; quotes are verbatim with date and share_url.*

---

## Headline findings

- **The two biggest dollar-figure trade claims in the archive check out.** The 2024-03-24 "$12M down on $BA, up almost $3M, ended the week pretty much even" is confirmed almost to the dollar by the snapshots (BA book swung from roughly **‑$11.9M to +$0.8M unrealized**, 3/19→3/22 — a ~$12.7M swing). The 2024-11-04 "just under $6M in calls, sold another 1M in puts, a little over 1M in stock" is directionally accurate (calls **$5.43M** mark, short puts **$1.06M** in collected premium/cost basis, stock **$1.10M**) — a mild rounding-up on the calls, not a fabrication.
- **They never said the number that mattered most.** The account fell from a **$73.2M peak (2025-02-20) to $33.2M (2025-04-05) — a ‑$40M / ‑55% drawdown** — and the final post ("It's time!", 2025-04-05) only ever says *"I've lost as much as I have this week."* No dollar figure, no percentage, ever, for the single largest event in the account's life.
- **Post *frequency* held up through the drawdown; post *substance* collapsed.** January 2025 averaged 197 characters/post with 20/40 empty bodies; by March 2025 that was 40 characters/post with **11 of 21 posts having zero body text** — replaced by song-clip links, single emoji, and one-word titles. The words came back only in the very last two posts, both emotionally raw ("I'm sad," "It's time!").
- **The earlier text-only dossier's "only 4 of 24 closed" and implied "never really exits" reading is refuted by the position data.** The change log shows **88 OPEN LONG + 30 OPEN SHORT = 118 opens** against **53 CLOSED + 17 EXPIRED/GONE = 70 closes**, plus 143 ADDs and 81 TRIMs. $BA alone has ~180 individual leg-level open/add/trim/close/flip events across 14 months — this was a constantly re-legged, actively rolled book, not a buy-and-forget one.
- **The "Martingale" self-diagnosis is real, self-named, and never fixed.** They nicknamed averaging-down "Martin" as early as 2023-12-05 ("Hello Martin(gale)!"), explicitly diagnosed the danger in the $BA post-mortem ("the mistake I made was starting off with a big position... which limited Martin's ability to help when the stock further plummeted," 2024-03-24) — and then invoked "Martin" **eight more times in Feb–Apr 2025**, during the exact drawdown that ended the account.
- **The "I buy when I'm most scared" and "boredom" trades are traceable and mixed.** The Dec 19 2024 "doubled down... out of boredom" add to $RIVN was added to an *already-profitable* position (+$217k unrealized at the time), not a rescue of a loser — but by the March 2025 drawdown both $RIVN and $ZGN boredom-adds had round-tripped into red.
- **Self-stated identity is a self-consistent but internally-strained "kid" persona**: in school, has a guidance counselor, applying to Stanford (2025-01-08), mom is the moral authority ("my mom says"), and the account's origin story is $200,000 left by an absent father, grown by "silly kid" into a $30–95M book. The persona mixes a pre-algebra/middle-school register with college-application-senior content in the same school year — a real inconsistency in the self-narrative, noted here as evidence, not resolved.
- **The playbook is legible and mostly about structure, not stock-picking**: continuous options rolling/legging on a single thesis ($BA) sustained for 14 months, disciplined-sounding recycling language ("sold on up days, bought back on down days") that the tape mostly supports, and — critically — a stated risk rule ("don't start a position at max size") that was violated at the exact moment (Feb–Apr 2025) it would have mattered most.

---

## 1. Narrative vs. tape: trade-by-trade

### $BA — the $12M week (2024-03-24, "A (challenging) week in review")

> *"So we started the week down over $12M on $BA, Friday morning up almost $3M, and ended the week pretty much even... I go into next week with my biggest position into $BA yet."*
> — https://afterhour.com/wTF/dVO/a-challenging-week-in-review

Snapshot reconstruction of BA-only unrealized profit (equity + both call strikes), from the leg data:

| Date | BA equity P&L | BA $200c (5/17) P&L | BA $210c (6/21) P&L | BA total |
|---|---|---|---|---|
| 2024-03-19 | ‑$1,016,682 | ‑$10,743,800 | ‑$163,456 | **≈ ‑$11.92M** |
| 2024-03-22 (17:44) | ‑$188,064 | +$1,070,386 | ‑$83,096 | **≈ +$0.80M** |

That's a **~$12.7M swing**, matching "down over $12M... up almost $3M" (the post's "$3M" reads as the Friday-morning bounce specifically, not the full-week swing) almost exactly. Position size check: by 2024-03-24 the combined BA book (equity + both calls) was **$37.47M against an $84.99M account (44%)** — up from **~14% on 2024-03-11** ($11.56M / $83.88M). "Biggest position into $BA yet" is accurate and, if anything, understated the concentration.

### $BA — "just under $6M in calls" (2024-11-04, "Get out the vote!")

> *"I have: Just under $6M in call options. Sold another 1M in Puts, and a little over 1M in stock that $BA had gifted me."*
> — https://afterhour.com/wTF/jRA/get-out-the-vote

Snapshot at that post (2024-11-04T19:03Z):

| Leg | Market value | Cost basis (≈ premium) |
|---|---|---|
| BA shares | $1,103,695 | — |
| BA $165c Dec20 | $4,580,360 | $3,513,168 |
| BA $170c Dec20 | $218,580 | $491,952 |
| BA $175c Jan25 | $625,560 | $435,790 |
| BA $200c Jan25 | $1,561 | $17,248 |
| **Calls total** | **$5,426,061** | **$4,458,158** |
| BA $140p Dec20 (short) | ‑$232,083 | ‑$347,515 |
| BA $135p Jan25 (short) | ‑$480,240 | ‑$714,104 |
| **Puts total** | **‑$712,323** | **‑$1,061,619** |

Stock "a little over 1M" → **$1.10M, exact.** Puts "sold another 1M" → matches the **$1.06M in cost basis/premium collected**, exact. Calls "just under $6M" → the market value was **$5.43M**, about **10% short of $6M**; measured by cost basis it's **$4.46M**, about 26% short. This is the one place where the stated figure is a genuine overstatement, though modest and consistent with rounding a fast-moving multi-leg book rather than misrepresentation.

### $ADBE — the gain they didn't take (same 2024-03-24 post)

> *"my $ADBE position hit a 50%+ gain of roughly $2.5M (my goal was 30%), but instead of recycling it, I held. Why? Because $BA was down."*

Snapshot same day: ADBE equity ‑$146,372 unrealized (small loss at that exact tick — normal single-day noise around a position that had run up intraweek) plus ADBE $550c Jun21 ‑$160,553. This is a case where the post is describing an *intraweek high-water mark* ("hit a 50%+ gain") that isn't visible in the single end-of-week snapshot — consistent with, not contradicted by, the data; just not independently re-verifiable from the snapshot alone.

### $RIVN — "taken profit" (2024-02-29, referenced in "Context is everything")

> *"Calls of $RIVN leading up to D-day, and I then rolled those over to Puts in the final hour... On Thursday sold yesterday and today most of my position (and taken profit)"* (paraphrased from the 2/27–2/29 run; see https://afterhour.com/wTF/dmj/context-is-everything)

The RIVN share leg actually **grew** from 100,000 sh (2/8) to 1,030,001 sh by the 2/29 snapshot — the opposite direction of "sold most of my position." Per the stated data caveat, snapshots only capture legs on tagged posts, so an intraweek call-sale-and-share-reentry sequence between 2/8 and 2/29 is plausible but not visible in the tracked legs. **Flagged as unverifiable, not as a contradiction** — the tape simply doesn't have the resolution to confirm or deny this one.

### $SQ — the account's first trades (Oct 2023) are outside the verifiable window

Posts from 2023-10-07 through 2023-10-30 state specific dollar adds ("$250k," "$1.7M of $SQ," "$2M more in options"). **The first account/position snapshot in the dataset is 2023-12-22** — nearly two months later. None of the October 2023 SQ figures can be checked against broker data; they predate the tracked window entirely. This is a hard caveat on the whole "narrative vs tape" exercise for the account's first ~11 weeks.

### $HOOD — "finally sold everything" (2024-02-29)

The 2024-02-29 omnibus post says HOOD was fully exited. The change log shows a HOOD **CLOSED** event dated 2024-02-07 for the leg captured in that window (see `reports/positions/@wTF_position_changes.md`), consistent with the stated close, though HOOD reappears later in 2024 as a new episode — matching the "closed, then silent" pattern the change log captures well.

---

## 2. Disclosure: what got posted, what didn't

**Account trajectory, Feb–Apr 2025 (all from `data/positions/@wTF_positions.json` → `account`):**

| Date | Total value | Note |
|---|---|---|
| 2025-02-20 | $73,215,430 | Peak |
| 2025-02-27 | $67,896,209 | |
| 2025-03-10 | $53,022,027 | |
| 2025-03-27 | $66,279,557 | Local rebound |
| 2025-04-01 | $46,139,321 | Cash balance = **$1** that day |
| 2025-04-02 | $58,195,498 | Sharp one-day rebound (+$12.06M) |
| 2025-04-05 | $33,208,267 | Final snapshot. Profit field: **‑$14,986,220** |

Peak-to-trough: **‑$40.0M, ‑55%**, over ~6 weeks, with a day (4/1) where cash was fully deployed and a following day with a $12M swing back up — i.e., the book was being actively, aggressively traded through the entire collapse, not de-risked.

**What was posted, in order, during this window** (titles only tell the story):
`This was Up now it's down! 🎶` → `👋 Martin — 🛩️💥💥` → `Martin really does have all the fun!` → `Where was Martin when you needed him!` → `Another Red Day 😞` → `😱` → `Back to where it all started…` → `I should of sold this earlier 😞` → `Patience is a virtue` (x2) → `Bubble, Bubble, Pop!` (nursery rhyme lyrics, no market commentary) → `I'm sad 😞` (birthday complaint, not markets) → `🎢🛩️🔥⤴️?🤷🏽` → `It's time!` (farewell).

Two posts have real prose during the entire collapse: **"I'm sad"** (2025-03-28), which is about a forgotten birthday, not the drawdown; and **"It's time!"** (2025-04-05), the account's last post ever:

> *"A lot of folks on here seem to be happy that I've lost as much as I have this week, that tells me I've been doing something wrong. I went on here to try to be helpful and make some friends along the way. My guess is I've must of failed at both. So it might be time to say goodbye."*
> — https://afterhour.com/wTF/J12/its-time

No account value, no dollar loss, no percentage — ever — appears in that post or any post in the entire six-week collapse. The reader has to reconstruct the ‑$40M from the tracked snapshots; it is never stated.

**Post-substance metric** (avg body length / empty-body count by month):

| Month | Posts | Avg. body chars | Empty-body posts |
|---|---|---|---|
| 2025-01 | 40 | 197 | 20 |
| 2025-02 | 47 | 100 | 28 |
| 2025-03 | 21 | 40 | **11 (52%)** |
| 2025-04 | 3 | 211 | 1 |

Frequency didn't drop during the drawdown (Feb was actually the second-busiest month in the archive) — but the *content* thinned to near-nothing, then the account closed with two unusually long, emotionally explicit posts and stopped posting entirely.

---

## 3. Stated philosophy vs. practice

**"Martingale" / "Martin."** First named 2023-12-05 ("Hello Martin(gale)!"). Used as a running bit for the rest of the account's life — 25 posts reference "Martin" by name, personifying the averaging-down instinct as a character who "helps" or fails to. The clearest self-diagnosis is the 2024-03-24 post-mortem:

> *"the mistake I made was starting off with a big position as if I had already gotten the timing right, which limited Martin's ability to help when the stock further plummeted... I don't like having these big positions, regardless of the outcome."*

This is a stated rule: **don't enter at max size, leave room to average down.** It was violated repeatedly — BA's position kept growing to new "biggest yet" sizes through 2024, and in the fatal Feb–Apr 2025 stretch "Martin" is invoked constantly (`👋 Martin`, `Martin really does have all the fun!`, `Where was Martin when you needed him!`, `Fun with Martin over the weekend!`, `Martin & Friends!`, `In the meantime, Martin!`) right through the ‑55% drawdown — i.e., the diagnosed failure mode recurred, by name, at the moment it mattered most.

**Boredom sizing.** Explicitly named as the reason for trades at least 5 times (RIVN 1/23/24, HOOD 1/23/24 point 4, RIVN 12/19/24, ZGN 12/19/24, and generic "bored" posts asking what to buy). The traceable instance:

> *"Doubled down today on both $ZGN and $RIVN, but if I'm being honest it was mostly out of boredom and still being up set about my test, so not sure anyone else should do this."* (2024-12-19)

At the moment of that add, RIVN shares were **+$217,349 unrealized** — i.e., this was adding to a winner out of boredom, not rescuing a loser. Both positions were carried into the 2025 drawdown: ZGN went from **+$234,882 (12/16/24)** to **‑$137,832 by 2025-03-27**; RIVN oscillated and was **‑$229,824 by 2025-02-24**. The boredom trades weren't disastrous on their own, but they added exposure that was still on the book when the drawdown hit.

**Fear-buying.** 
> *"@vivian said something today that stuck with me: That I buy when she is most scared. But that is only partially true, I tend to buy when I'm most scared."* (2024-01-30, "Some silly thoughts")

Consistent with the BA behavior in March 2024 — adds happened on down days through the worst of the week (see the leg table above, adds on 3/11 through 3/19 while the position was increasingly underwater), which is exactly what "I buy when I'm most scared" describes. The same pattern (adding into weakness) recurs through the Feb–Mar 2025 BA legs and is a structural throughline, not a one-off line.

**"Patience is a virtue" (2025-03-19, 2025-03-20) — undercut by the tape.** The BA leg log for **2025-03-19 alone** shows: OPEN LONG BA $155c, ADD BA $165c, FLIP BA $170p, ADD BA $170p(Jun), OPEN LONG BA $180p, ADD BA $185c, FLIP BA $210c — seven distinct leg actions in one day. "Patience is a virtue" was posted on one of the single most active re-legging days in the entire BA campaign. The next day's sequel, "No patience required" (2025-03-21), is at least titled consistently with what the tape shows (CLOSED/TRIM across five legs that day).

**Emotion-as-noise.**
> *"emotion should not be your guide"* (2025-02-07, "🐭🪣❌") and *"Emotions are a silly thing, whether it be fear or greed, they get in the way of us making good decisions"* (2024-01-30) are stated repeatedly as a rule for followers. The account's own posting behavior during the 2025 drawdown — title-only posts, nursery rhyme lyrics, a birthday complaint, then a raw farewell — is the clearest evidence in the whole archive that the rule wasn't something the account itself could follow under real stress.

---

## 4. Who are they (self-stated only; they/them)

Everything below is what the account said about itself — no identity inference beyond the posts.

- **In school, self-described as a kid/teen.** References a "pre-algebra" exam and quiz (2024-02-13, 2024-12-10, 2024-12-13, 2024-12-17 — scored an 82), a "social studies test" (2024-03-07, 2024-12-20 — scored 104), a guidance counselor (2024-02-08, 2025-01-08), "Ms. Zachary"/"Mr. Sanchez" as teachers, and "extracurriculars."
- **Applying to college, specifically Stanford**, per the 2025-01-08 post "Help with App 📕," which includes a full draft of a Stanford application essay.
- **Origin story, in their own words** (2025-01-08): *"My dad hasn't been in the picture for as long as I can remember, but he left $200,000 for me to use for college one day... Instead of letting it sit in a bank, I thought, 'What if I could make it grow?'"* — i.e., the account's own stated founding narrative is a $200k inheritance grown into a $30–95M book.
- **"My mom" is the recurring moral/emotional authority** — cited at least 12 times, including "my mom says that's true outside of investing too" (2024-01-30) and the "I am me" post (2024-02-28) where a conversation with her is the entire content.
- **Self-label: "silly kid" / "dumb kid."** Used self-deprecatingly at least 5 times as a hedge before making a substantive point (e.g., "feel free to ignore this silly kid, it's all paper money away," 2025-02-14, on $RXRX).
- **"Whale," used once, self-referentially**: *"we'd all have a good laugh about how the whale set a few million on fire"* (2023-10-10) — an early, single instance of describing their own account size in third person.
- **Internal inconsistency worth flagging as evidence, not resolving:** pre-algebra is a normal middle-school course, while a Stanford application essay is a late-high-school/senior activity, and both appear within the same 2024–2025 school year in the posts. The persona is internally consistent in tone (kid voice, mom, school stress) but not in the specific grade-level details across the archive.
- **"It's all paper money"** (post referenced in the task brief, 2025-02-14 context and elsewhere) is explicitly a figure of speech for *unrealized* gains in a real account — confirmed by the fact that the account's cash balance, cost basis, and total value are tracked exactly like a real brokerage statement throughout, including going to **$1 in cash on 2025-04-01**, which would be meaningless in a simulated account.

---

## 5. The playbook — how an institutional-size retail trader actually did it

1. **Pick one name and run it as a campaign, not a trade.** $BA was opened 2024-02-29 and was still being actively re-legged on 2025-04-01, the account's second-to-last day — 14 months, ~180 leg-level events on one ticker. **Copy at small scale**: pick a thesis you'll actually revisit for a year instead of chasing a new ticker every week.
2. **Recycle a range instead of holding through it.** The stated method — "selling on up days and buying back on down days" within a big position — is directly supported by the BA leg log (constant TRIM/ADD pairs on the same strikes through March 2024 and March 2025). **Copy at small scale**: this is just scaling in/out around a core position; the mechanics don't require $50M, only the same discipline to actually take the trim.
3. **Use short puts to fund/hedge a long options book.** The Nov 2024 BA structure (long calls + short puts + shares) — a risk-reversal-style stack — recurs throughout the position data as short puts appear alongside long calls on nearly every BA leg date from late 2024 on. **Copy at small scale with real caution**: assignment risk on short puts is exactly the kind of thing that turns a bad week into a worse one; only works if you can actually take stock assignment, which needs capital most $50M+ accounts have and most small accounts don't.
4. **Name your own bad habit and watch it anyway.** "Martin(gale)" as a running joke is a genuinely useful self-monitoring device — it's a label attached to a real, recurring, named behavior (25 posts). **The lesson that doesn't transfer**: naming the habit did not stop it from recurring at the worst possible time (Feb–Apr 2025). Self-awareness without an enforced rule (e.g., a hard position-size cap) is not risk management.
5. **Don't start a position at the size you'd want if you were already right.** This is the account's own explicitly stated rule (2024-03-24) — and its own clearest violation. **Copy this rule, and copy the failure mode as a warning**: "biggest position yet" recurred as praise-worthy in the narrative multiple times, which is the opposite of following the rule.
6. **Boredom is a real, nameable source of unforced position sizing — don't wait for the loss to notice it.** The account caught itself doing this in real time ("doubled down... mostly out of boredom... not sure anyone else should do this," 2024-12-19) but kept the resulting position anyway. **Copy at any scale**: if you can *name* a trade as boredom-driven while making it, that's the moment to size it at zero, not the moment to caveat it.
7. **A drawdown doesn't have to be announced in dollars to be handled honestly with followers — but here it wasn't handled with dollars at all.** The account posted through the entire ‑55% collapse but never stated the size of the loss even once, even in the farewell post. **What only works at $50M+ (and maybe shouldn't)**: an institutional-size account can absorb social/reputational cost of silence about magnitude in a way a small account being copy-traded cannot — followers of a small account need the real number to size their own risk; here they never got it.
8. **Post frequency is not a proxy for post value — and it's a tell.** Frequency held steady through the worst month (Feb 2025, 47 posts) while substance collapsed (avg. 100 chars/post, dropping to 40 in March with half the posts empty). **Transferable lesson for anyone documenting their own trading**: track your own words-per-post or journal-completeness over time — a silent drawdown in your own commentary is an early warning sign worth watching for, in yourself, before the number does the talking for you.
9. **Multi-leg rolling across expiries keeps a thesis alive without repeatedly re-entering from scratch.** The BA book rolled from May/Jun 2024 strikes → Nov/Dec 2024 → Jan/Mar 2025 → May/Jun 2025 continuously, avoiding round-trip commissions/spread costs of fully closing and reopening. **Copy at small scale**: same mechanic works with a handful of contracts; it's capital-efficiency, not a size-dependent trick.
10. **A real account, however large, is still one person's emotional state.** The final six weeks — nursery-rhyme lyric posts, a birthday complaint, then a farewell citing follower reactions to the losses ("a lot of folks on here seem to be happy that I've lost as much as I have") — show that a $70M+ drawdown was, in the end, as much a social/emotional event as a financial one. **What doesn't scale down**: most retail traders don't have an audience reacting in real time to their losses, which was clearly a real additional stressor here, visible in the posts, distinct from the money itself.

---

## Collaboration note

I attempted to reach the other three lens agents (option structures, P&L & risk, timing & market context) via `SendMessage`, but this session has no working `ListAgents` tool to discover their live names, and a guessed name ("option structures") came back unreachable. I was not able to cross-check the playbook section against their findings before finishing. If the option-structures and P&L/risk lenses have findings on realized (not just unrealized) P&L for the BA campaign, or on how the short-put risk-reversal structure performed into the April 2025 collapse specifically, those would sharpen playbook items #3 and #7 above.

---

## Data caveats specific to this lens

- All October–early December 2023 posts (the account's first ~11 weeks, including all $SQ dollar-figure claims) **predate the first tracked account/position snapshot (2023-12-22)** and cannot be checked against broker data.
- Snapshots only capture legs for underlyings tagged on that specific post, so a stated intraday round-trip (buy-then-sell same day) on an untagged post can be invisible to the leg data even when the post is accurate (see the $RIVN "taken profit" case above).
- "Profit" fields in the leg/account data are unrealized mark-to-market at the snapshot timestamp, not realized P&L — narrative claims about realized gains/losses can't be fully reconciled to a single number from this data alone.
