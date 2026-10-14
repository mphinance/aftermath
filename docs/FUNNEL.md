# Telegram Funnel Tracking

AfterHour accounts that funnel traders into Telegram channels, how we track them, and how the data is served.

> **Data credit:** the flag list (`accounts.json`) is curated by [TelegramScammers.com](https://telegramscammers.com) and published there as open data (`/accounts.json`, `/accounts.csv`). AfterMath adds post-history analysis, passive Telegram recon, an MCP tool and a lookup page. All listings mean **flagged for investigation, not a finding of fraud.**

## What is served

| Surface | What it is |
|---|---|
| `https://ah.mphinance.com/scamcheck` | "Check before you join": paste a `t.me` link or AfterHour username, get a match or no match. Static page, reads `api/funnel.json` in the browser. |
| `https://ah.mphinance.com/api/funnel.json` | All flagged accounts with tier, shared-link clusters, posting stats. |
| MCP tool `get_funnel_accounts` | Same lookup for AI agents. Inputs: `username`, `telegram_link`, `tier`, `limit`. |

Evidence tiers (set by TelegramScammers.com): `reported` single observation, `corroborated` shared Telegram link across accounts, `verified` proof captured and admin-checked.

## Pipeline

```bash
python3 pull_funnel_posts.py     # full post history per account -> data/telegram_funnel/<user>.json
python3 analyze_funnel.py        # cadence, ticker bait, copy-paste spam -> reports/analysis/funnel_accounts.{json,md}
python3 build_funnel.py          # accounts.json + post stats -> api/funnel.json (also run by build_github_pages.py)
python3 tg_recon.py              # passive Telegram previews -> data/telegram_funnel/recon.json
python3 tg_watch.py              # snapshot + diff over time (link rotation, dead channels, member jumps, new wallets) -> reports/analysis/funnel_watch.md; schedule daily
python3 funnel_tickers.py          # tickers called out (AfterHour posts + archived Telegram posts) -> reports/analysis/funnel_tickers.md
python3 render_recon.py          # recon.json -> reports/analysis/funnel_recon.html (PNG: screenshot at 1200px, 2x)
```

### `tg_recon.py` (passive, no login, no joining)
Fetches only the public web previews Telegram serves to anyone: `t.me/<handle>` (title, description, member count), `t.me/+<hash>` (same, for private invites without joining) and `t.me/s/<handle>` (recent public posts). Extracts operator fingerprints (wallets, PayPal and cashtag handles, emails, prices, cross-promoted `t.me` links, `@mentions`) and clusters channels by identical description copy or shared fingerprint. It never posts, never uses an account, and sleeps between requests.

- Invite hashes are **case-sensitive**. Always use the original-case links (`telegram_links`), never the lowercased `telegram_links_norm`, or Telegram returns a generic "invalid invite" page.
- A generic "You are invited to a group chat" page means the invite is invalid, revoked or truncated; the script marks it `alive: false`.
- `--reanalyze` re-runs filters and clustering on an existing output with no network.
- Stock tickers (`$SPY`) are filtered out of the cashtag fingerprint.

### `tg_watch.py` (change tracking)
Runs `tg_recon.py` plus a re-check of every flagged AfterHour profile, saves a timestamped snapshot under `data/telegram_funnel/snapshots/` (gitignored), diffs against the previous one, and archives new public posts (deduped) to `posts_archive.jsonl`. Flags: bio link rotated, account gone, channel dead or revived, member jump (100 or 10%), description rewritten, renamed, new wallets/prices/admins, new cross-promoted channels. `--no-fetch` re-diffs the two newest snapshots offline. Public channel history beyond the newest ~20 posts is not paged yet (`t.me/s/<handle>?before=<id>` would do it).

#### Scheduled run (Coolify host)
`tg_watch.py` runs daily at **13:15 UTC (9:15 ET)** from `mph`'s crontab on the Coolify box (`ssh coolify`). Checkout: `/home/mph/apps/aftermath-watch` (sparse, partial clone of this repo, deliberately **outside** the nginx webroot so snapshots are never served). `run_watch.sh` does `git fetch` + `reset --hard origin/main`, then `python3 tg_watch.py`. Output: `watch.log` and `reports/analysis/funnel_watch.md` in that directory; snapshots live in its `data/telegram_funnel/snapshots/` and the post archive in `data/telegram_funnel/posts_archive.jsonl`. The server keeps its own history, separate from the local one. Because of the hard reset, never edit files in that checkout by hand. Read the latest report with `ssh coolify cat /home/mph/apps/aftermath-watch/reports/analysis/funnel_watch.md`.

### Handoff for the list owner
`handoff/crawl.py` (zero-dependency feed sweeper) and `handoff/AGENT_BRIEF.md` (instructions for his agent). The feed sweep is low-yield: ~1 new Telegram-linked account per 1,200 authors scanned. Mining existing scam-list posts and shared-link pivots finds far more.

## Findings snapshot (2026-10-13)
- 85 flagged accounts, 69 distinct Telegram links, 11 shared-link clusters covering 26 accounts.
- Median follower count 1; 38 of 44 known counts are 5 or fewer. Only 1 of 85 ever posted a broker snapshot; none are in the whale universe.
- 48 of 82 dated accounts were created in Sept or Oct 2026.
- Recon: 62 of 69 links resolve, 132,267 combined members on the 55 channels with a public count.

## Gotchas
- `afterhour.com/<user>` now 301-redirects to `www`, so scraping the profile page no longer works. Use `https://api.afterhour.com/public/profile?username=<name>` (returns `id`, `bio`, `linkInBio`, `numFollowers`). `afterhour.profile_id()` does this first.
- The global feed embeds each post's `author` (bio, followers, id, created date), so one request per page is enough for a sweep.
- Many flagged accounts show `post_count` 0: the platform appears to purge funnel posts and leave profile shells.
- Candidate files (`data/telegram_funnel/candidates_*.json`, `recon_candidates.json`) are **unreviewed and gitignored**. Some candidates may be innocent or impersonation targets; they go to the list owner for review, not into the public repo.
- Never post, comment or follow from automation (see CLAUDE.md), and never join Telegram channels without an explicit decision: mass joining gets accounts limited and exposes the joining number to operators.
