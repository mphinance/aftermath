# In Data We Trust

*AI 40% | Research 35% | Mindset 25%*

Have you ever decided somebody could trade based on one screenshot? Have you ever unfollowed a guy over a bad call, in a week you were also wrong? Have you ever trusted the loudest account in the room because he was funny on a green day?

I've said yes to all of these. So I stopped grading people by vibe and built something that grades everybody the same way, whether I like them or not.

Then it told me the one thing I was most sure of was the thing I couldn't prove.

## What I actually did

I pulled the complete public post history of **40 traders** off AfterHour. Not a sample. Not the good months. Every post from the first one to the most recent, **33,090** of them.

The feed is public and unauthenticated. It's the same data you see when you open somebody's profile in a browser. I just took all of it at once instead of scrolling for two hours.

```
https://api.afterhour.com/social/feed?take=50&contentTypes=post&authorId=<prf_id>
```

`take` is capped at 100, and 100 does not work. The first page comes back fine, then every cursor page after it returns a 504. **50** is the largest page size that actually paginates, and even then about **one request in seven** times out and needs the same cursor retried.

Then one AI agent per trader, isolated, no memory of the last one, handed the same prompt every single time.

## Everybody got the same prompt

This is the whole design. Not the scraping, not the charts. This:

```text
You are a senior quantitative trading analyst conducting a deep forensic
autopsy on AfterHour trader @{username} (#{rank} most active followed
trader with {lifetime_posts} lifetime posts).

Read through his lifetime posts and conduct a quantitative, mechanical,
and psychological breakdown:

1. Executive Profile: Trader philosophy, post cadence (posts/week),
   active timeline, verified capital trajectory and drawdown history.
2. Ticker Universe & Catalysts: Core assets traded, options vs equities,
   macro vs technical setups. What drives his trade entries?
3. Risk Management & PnL Reality: Does he take profits or hold bags? How
   does he manage losing positions? Documented wins vs blow-ups?
4. Behavioral & Sentiment Signals: Why is he posting? Decode his
   recurring linguistic patterns, sentiment calls, and how he reacts to
   market volatility/red days.
5. Quantitative Verdict:
   - Primary and Secondary Algorithmic Classification Tags
   - Algorithmic Alpha Score (0 to 100) & Expectancy
   - Signal Flow Ingestion Matrix
   - Specific Execution Directives:
     * Ingestion Directives (what genuine edge to harvest)
     * Contrarian Fade Directives (when to fade his calls or the herd)
     * Mandatory Risk Blacklists & Firewalls (bad habits to filter out)
     * Exit Rules & Alpha Rectification (profit-taking, trailing stops)
6. Chronological Milestone & Catalyst Log.
```

Three things change between runs: the handle, the rank, the post count. That's it.

Nobody I like got a softer question. Nobody who's dunked on me got a meaner one. The guy with 2,682 posts and the guy with 57 posts got the identical six-part interrogation.

Then I threw the first pass out and ran all of them again, because the prompt had been identical the whole time but the runs weren't. Some dossiers came back from a fast cheap model and some didn't, and I'd been about to publish a leaderboard built on that. Same prompt, same model, all of them, including the ones that already had a writeup I liked.

That fixed the wrong problem. The real one was in line 1 of the prompt.

## The part of the prompt that was lying

Look at what I asked for. "Verified capital trajectory and drawdown history."

Verified by whom?

AfterHour syncs to your brokerage and shows an account value. It glitches. Illiquid options get marked at midpoint on a weekend and an account "gains" 30% on a Saturday. Unlink and relink and the curve falls off a cliff that nobody traded. And the number is a total account value, not a profit, so a deposit looks exactly like a great month.

The app flags this itself. I knew it. I wrote a whole section warning you about it, and then I asked a machine for a "verified capital trajectory" anyway, and the machine did what machines do: it answered confidently.

Every dollar figure in this post is gone for that reason. Not because the traders lied. Because the number was never load-bearing enough to put somebody's name next to.

So I threw out the money and asked what's actually provable from the posts themselves.

## The number I do trust

Nobody's brokerage is involved in this one. It's just: did you say you bought something, and did you ever say you got out of it?

Across all 40 traders and 33,090 posts:

```
Positions announced as buys        3,660
Ever closed in public              1,739   (47.5%)
Never mentioned again as an exit   1,921   (52.5%)

Entry-language posts               7,682
Exit-language posts                4,948   (1.55 entries per exit)

Posts tagged Gain                  2,765
Posts tagged Loss                    233   (11.87 gains per loss)
```

**Eleven point eight seven gains for every loss.** Across two and a half years and thirty three thousand posts by people who are, on average, not eleven times better at this than they are bad at it.

That ratio is not a trading record. It's a disclosure rate.

And **52.5%** of every position announced as a buy simply never gets a closing post. It doesn't get sold, it doesn't get stopped out, it doesn't get admitted. It stops being mentioned. The trade doesn't end, it just goes quiet, which is exactly how a losing position feels from the inside.

The individual numbers are worse than the average. One trader announced buys in **52** different tickers and publicly closed **one** of them. Another has **2,682** posts, 47 of them tagged as gains, and zero tagged as a loss. Not one, ever.

The best follow-through in the entire set, **79.1%**, belongs to a covered-call seller, and I don't think that's a character difference. The wheel closes positions mechanically whether you feel like discussing it or not. Her strategy takes the decision away from her ego. That's the actual lesson in the whole dataset and it took a scraper to find it.

## Two models, thirty two points apart

Eleven traders got scored by both models on the identical prompt, off the identical posts.

```
                    first pass    second pass
@RyanLP                 89            14        -75
@terridactil            84            24        -60
@MarketVictor           88            31        -57
@mphinance              92            58        -34
@Drone_Daddy            72            41        -31
@AtypicallyErect        64            34        -30
@883Ismygovtname        79            58        -21
@Legitimate_Risk        68            58        -10
@NewFishBigPond         24            24          0
@Freeballer             18            33        +15
@Dallaslongcall         12            34        +22

mean absolute disagreement: 32.3 points
```

**Thirty two points** of average disagreement on a hundred point scale. One model called @RyanLP a top-tier signal source at 89. The other put him fourth from the bottom at 14. Neither of them hedged. Neither said "low confidence." Both produced a tidy two-digit number and a paragraph of reasoning to go under it.

It isn't a simple case of one model being harsher, either. Two traders scored materially higher on the second pass. The number just moves.

If I had run this once and published, I'd have shipped whichever answer I happened to get.

Then I checked the scores against the one thing in this whole project I can actually verify: whether these people close their positions in public. Across all 40, the correlation between a trader's alpha score and their real follow-through rate is **0.20**. Basically nothing.

@RyanLP scored a 14 and closes **73.2%** of what he announces, one of the best disclosure rates in the set. @Legitimate_Risk scored a 58 and closes **17.8%**.

The score is not measuring the behavior. It's measuring how convincing the writeup was.

## What actually survived

The scores went in the bin. This did not:

```
@Tiger_
FUNDAMENTAL_QUALITY_COMPOUNDER / LEVERAGED_CONTRARIAN_DIP_BUYER

INGEST    Auto-tag any ticker he moves above 10% disclosed portfolio
          weight as a high-quality long candidate for independent
          fundamental verification.
          Treat his rare, explicit "leverage on" statements as a
          contrarian-bottom signal on broad risk sentiment.
FADE      Fade his trim and rotation timing specifically, not his
          stock selection.
FIREWALL  No stop-loss discipline exists in this trader's process.
          Concentration is structural: single names routinely run
          20 to 50% of the book.
EXIT      Tiered trim on anything sourced from him: bank a portion
          at +50%, more at +100%, remainder on a trailing stop.
```

"Fade his trim and rotation timing specifically, not his stock selection."

That sentence is worth more than every alpha score I generated. It doesn't need a verified P&L, it doesn't need his account value, and it survives being wrong about how rich he is. It comes from reading what he wrote across hundreds of posts and noticing that his ideas and his exits have different quality.

Here's the same treatment on the trader who blew up:

```
@Tradeless
PERMA_BEAR_MACRO_HEDGER / THEMATIC_LIST_AGGREGATOR

INGEST    Scrape his thematic sector lists as a free, timely
          universe-expansion feed for the screener stack.
FADE      Treat a cluster of his bearish index-put disclosures
          during an uptrend as a sentiment-extreme tell.
FIREWALL  Never ingest sizing, entry mechanics, or stop-loss
          placement from his disclosed trades.
          Hard-blacklist the instrument class: uncapped-size 0DTE
          index options used as a directional hedge.
```

"Harvest his watchlist, never his sizing" is a usable instruction. "He scored a 12" is a slur with a decimal point.

## The part where you should get a little uncomfortable

I did all of this with a public endpoint, no login, and a laptop.

Now go think about what the app itself has.

I can see what you posted. It can see what you typed and deleted. I can count the trades you announced. It knows about the ones you didn't. I get a Gain tag you selected for yourself; it gets whatever the brokerage actually said underneath. I can measure that half your positions never get a closing post. It can see which ones are still open and red.

That gap between what I could reconstruct and what they hold is the entire business model of every free app you've ever signed into. In data we trust is a fine motto right up until you ask who's holding it, and what they had to synchronize to get it.

## Then I pointed it at myself

Same prompt, same model, my handle in the blank where everybody else's went.

The first pass gave me a **92**. The second pass, same posts, same question, gave me a **58**. I got to watch my own grade drop 34 points for no reason except that a different machine read it, which is a useful thing to have happen to you before you go telling other people what their number is.

I close about **half** of what I announce, **51.6%**, which is a hair above the group and nothing to put on a business card. I've tagged **61** posts as gains and **13** as losses. That's roughly **4.7 to 1**, which is better than the 11.87 average and still nowhere near the real ratio of anybody's trading, including mine.

I'm not going to tell you what my account did over that period, because the number I'd be quoting comes from the same sync I just spent a section telling you not to believe. I'd rather show you the ratio I can actually prove and let it be less impressive.

## The version of this you can do tonight

You don't need 40 traders and a fleet of agents. You need to count your own zero.

Go find the last ten positions you told somebody about, in a group chat, on a podcast, out loud at dinner. Count how many of those ten you also announced getting out of. That fraction is your real disclosure rate, and if it's anywhere near the 47.5% in this dataset, then your memory of how you trade is running on the half of the record that felt good to type.

The fix is the least exciting thing available. Same fields, every trade, filled in on the red ones with the same detail as the green ones. Computed, not remembered.

In the rooms, the fourth step is a searching and fearless moral inventory, and the reason it works is that nobody gets to write their own prompt for it. Everybody answers the same questions. The ones you'd skip are the ones with your name on them.

Turns out that's also just good methodology.

~ Michael
