# Telegram Funnel Tracking

AfterHour accounts that funnel traders into Telegram channels, how we track them, and how the data is served.

> **Data credit:** the flag list (`accounts.json`) is curated by [TelegramScammers.com](https://telegramscammers.com) and published there as open data (`/accounts.json`, `/accounts.csv`). AfterMath adds post-history analysis, passive Telegram recon, an MCP tool and a lookup page. All listings mean **flagged for investigation, not a finding of fraud.**

## What is served

| Surface | What it is |
|---|---|
| `https://ah.mphinance.com/scamcheck` | "Check before you join": paste a `t.me` link or AfterHour username, get a match or no match. Static page, reads `api/funnel.json` in the browser. |
| `https://ah.mphinance.com/api/funnel.json` | All flagged accounts with tier, shared-link clusters, posting stats. |
| MCP tool `get_funnel_accounts` | Same lookup for AI agents. Inputs: `username`, `telegram_link`, `tier`, `limit`. |
| `https://ah.mphinance.com/api/funnel-tickers.json` | Ranked tickers called out by flagged accounts and their channels (`ah_accounts`, `ah_posts`, `tg_channels`, `tg_posts`). MCP tool `get_funnel_tickers` (`limit`). |
| `https://ah.mphinance.com/api/funnel-calls.json` | 300 most recent parsed callouts from public channels, with scored `outcome` where available. Quoted results are channel claims; small sample. MCP tool `get_funnel_callouts` (`ticker`, `channel`, `action`, `limit`). |

Evidence tiers (set by TelegramScammers.com): `reported` single observation, `corroborated` shared Telegram link across accounts, `verified` proof captured and admin-checked.

## Pipeline

```bash
python3 pull_funnel_posts.py     # full post history per account -> data/telegram_funnel/<user>.json
python3 analyze_funnel.py        # cadence, ticker bait, copy-paste spam -> reports/analysis/funnel_accounts.{json,md}
python3 build_funnel.py          # accounts.json + post stats -> api/funnel.json (also run by build_github_pages.py)
python3 tg_recon.py              # passive Telegram previews -> data/telegram_funnel/recon.json
python3 tg_watch.py              # snapshot + diff over time (link rotation, dead channels, member jumps, new wallets) -> reports/analysis/funnel_watch.md; schedule daily
python3 tg_calls.py                # parse trade callouts (ticker, strike, side, expiry, entry, quoted result) from archived Telegram posts -> data/telegram_funnel/calls.jsonl, reports/analysis/funnel_calls.md (run by tg_watch)
python3 tg_outcomes.py             # score option callouts vs the real tape (Yahoo public daily/5m bars) -> data/telegram_funnel/outcomes.jsonl, reports/analysis/funnel_outcomes.md
python3 funnel_tickers.py          # tickers called out (AfterHour posts + archived Telegram posts) -> reports/analysis/funnel_tickers.md
python3 build_funnel_calls.py      # calls.jsonl + funnel_tickers.json + outcomes.jsonl -> api/funnel-calls.json, api/funnel-tickers.json (public channels only; also run by build_github_pages.py; missing inputs degrade to empty lists)
python3 tg_merge_archive.py <remote_posts_archive.jsonl>   # merge the server's post archive into the local one (idempotent), then rerun tg_calls.py
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

**Sparse checkout list** must include every script `tg_watch.py` imports or runs. Current set: `/tg_recon.py /tg_watch.py /tg_calls.py /accounts.json /reports/analysis/funnel_watch.md` (plus `run_watch.sh`). When a new script becomes a dependency of `tg_watch.py`, add it on the server: `git sparse-checkout set --no-cone <paths>`, then `git fetch -q --depth 1 origin main && git reset -q --hard origin/main`, and confirm the file exists. A missing script fails silently in `watch.log`.

**Merging server history into local** (the two archives grow separately): `rsync -az coolify:/home/mph/apps/aftermath-watch/data/telegram_funnel/posts_archive.jsonl /tmp/remote_archive.jsonl`, then `python3 tg_merge_archive.py /tmp/remote_archive.jsonl` (de-duplicates by post id, local rows win, safe to rerun; `--dry-run` previews), then `python3 tg_calls.py`. Pull snapshots with rsync into a temp dir, never over local files.

### `tg_calls.py` (callout extraction)
Offline, stdlib-only parser over `posts_archive.jsonl`. One record per ticker mention: `action` (open, close, mention), `kind` (option, stock, spread), option `side`/`strike`/`expiry`, `entry_price`, `exit_price`, `result_pct`, plus `parse_flags` and, for closes, `open_id`/`open_link` pointing at the earlier open from the same channel. Docstring in the script lists every flag.

- Formats handled: `$NFLX 70P @.02`, `Opened 10 $SPX 7790C 10/08 @ $7.71`, `$BRZE 16 OCT 26 $25 CALL $0.95`, `SPY 777C 0.47 Odte`, `$REPX 50 Call 10/16.35` (date then price), `6/12 $TGT 133c @.16`, `$ESNT BTO / OCT/08 / 65C e:0.70`, `Entry: $3.80`, `avg .30`, `@1.10 from 0.90`, `$3.25 -> $3.62`, `Exit ... @ $3.62 · +11%`, `13/10` (day first), `1DTE`, bare tickers glued to a contract (`HOOD 10/16 112C`), `XXX TRADE CALL` headlines, `SPXW` (stored as SPX).
- On an open, `@ x` is the entry; on a close it is the **exit** (`exit_price`), and `entry_price` is only set when the post states it (`Entry:`, `from`, arrow). Older output put the exit price in `entry_price`.
- Never becomes an open: recap lists (`TRADE RECAP`, `CLOSED TRADES`, daily recap lines, `Position update`), the `Trade Summary` tail, `price_update` lines (`7700C @ 11 from 5.1`), hindsight talk, `Up 55%` marks, TP/SL/Take/Stop lines, `close to ITM`, bare-cashtag lists. A `Closed ...` line beats a later `Opened: 10:17 AM` line.
- Multi-leg (`170/172.5C CDS`, `spread`) is `kind: spread` with `strike` null and `strikes` set; downstream scorers that only handle single legs should skip them.
- `result_pct` is attached only to the ticker's own text, with comma thousands (`+1,200%`) handled. Quoted results are the channel's own claims; winners dominate (survivorship), so measure outcomes against the real tape.
- Filter on `parse_flags` before scoring: at minimum drop `duplicate_echo`, `spread*`, `expiry_before_post`, `entry_implausible`, `posted_date_suspect`; treat `no_expiry` as unknown (not same-day) unless `expiry_0dte_tag` is present.
- Accuracy (hand-labelled posts in `tests/fixtures/tg_calls_gold.json`, run by `tests/test_tg_calls.py`): on a stratified 110-post sample the old parser scored precision/recall of 0.88/0.49 on entry price, 0.67/0.54 on action and 0.50/0.35 on result_pct; the current one is at or near 1.00 on all fields on the sample it was tuned on and 0.97+ recall on the later batches. Add a gold post whenever a new failure shows up.
- `tg_watch.py` walks 6 pages (120 posts) back per public channel each run so busy channels are not missed between daily runs; `tg_recon.py --post-pages N` controls depth.

### `tg_outcomes.py` (callouts vs the tape)
Scores option callouts from `calls.jsonl` against the underlying's real price, using Yahoo's public chart endpoint (daily bars, 5m bars for posts within 55 days; no key, read-only GETs). No option price history exists, so the headline is **hold-to-expiry intrinsic** value minus the channel's quoted entry premium. "Touched breakeven" is an optimistic upper bound, not P&L. Entry premiums are the channels' own unverifiable fills and slippage is ignored, which flatters them. Null expiry is not assumed 0DTE unless the parser tagged it; echoes (same trade reposted) are collapsed; pending, far-dated and implausible records are reported but not scored. The sample is small and covers a short window, and expiry-day moves dominate. Assumptions and parser caveats: `reports/analysis/funnel_outcomes.md`, `reports/analysis/outcomes_parser_notes.md`.

**UI gate:** `scamcheck` shows outcome rates ("Callouts vs the tape") only when `callouts.outcomes.n_scored` is 100 or more; below that it shows "Collecting data" with no percentages. `api/funnel.json` always carries the numbers. Wording stays "flagged for investigation, not a finding of fraud", with credit to TelegramScammers.com.

### `/signals` (callout feed page) and daily auto-publish
`signals/index.html` is a static page at https://ah.mphinance.com/signals reading `api/funnel-calls.json`: newest-first callouts (time in ET, channel, ticker, strike, side, expiry, entry, open or close), filters (ticker, channel, type, scored-only, repeat posts), a scored-at-expiry chip per option open, and the channel's own claimed result on closes. Repeat posts are hidden by default. The feed shows its `generated_at` stamp. Four views over the same filters: Feed (cards), Table (click-to-sort columns), Group (group by one or two of ticker, channel, day, weekday, hour, call/put, action, outcome status, days to expiry, with count, channels, tickers, scored, win rate, median and mean return, worthless share, average entry and claimed result), and Pivot (rows by columns with a selectable cell metric and heat shading). Export CSV downloads the filtered rows. Win rates and returns use scored option opens only; empty cells mean none scored.
The Coolify cron (`scripts/run_watch.sh`, called by the server's `run_watch.sh` wrapper after it fast-forwards the checkout) runs `tg_watch.py`, `tg_outcomes.py`, `funnel_tickers.py` and `build_funnel_calls.py`, validates the two JSON files and atomically publishes `api/funnel-calls.json` and `api/funnel-tickers.json` into `/home/mph/apps/ah-portal/api/`. It does not rebuild `api/funnel.json` (accounts, clusters, outcome summary); that still needs a manual `build_funnel.py` plus deploy.

### `tg_backfill.py` (one-off deep history)
Walks back up to `--pages` pages (20 posts each) of every public channel's `t.me/s/<handle>` preview and appends new posts to the archive, deduped by post id. The daily run only walks 6 pages, so a busy channel can lose posts between runs; run this after adding channels or after a gap, then `python3 tg_calls.py`. Serial, about 1 second per page. Note some channels re-post history in bulk (many posts sharing one exact timestamp); `tg_calls.py` flags those as `posted_date_suspect` and the scorers skip them.

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
