# Brief for the TelegramScammers.com agent: crawl.py

Your owner is not technical, so do this yourself end to end. Nothing here posts, follows, comments, or touches Telegram. It only reads public AfterHour pages.

## What this is
`crawl.py` scans AfterHour's public feed for accounts that push a Telegram link (in the bio or in posts) and are not already in your `accounts.json`. It needs only Python 3.9+, no installs.

## Steps
1. Put `crawl.py` next to `accounts.json`.
2. Run: `python3 crawl.py --known accounts.json --pages 200 --out candidates.json`
   It prints progress and finishes with a candidate count. Use `--pages 500` for a deeper pass. It sleeps 0.4s between requests; do not lower that.
3. Open `candidates.json`. Each row has:
   - `username`, `profile_id`, `bio`, `created_at`, `num_followers`
   - `telegram_links_norm` (normalized `t.me/...` form), `telegram_links`, `telegram_handles`
   - `evidence`: up to 3 posts (`post` URL and a text snippet) that exposed it
   - `shares_link_with`: usernames already in `accounts.json` that use the same normalized link
4. Review before adding. Rows are sorted so the strongest come first.

## How to judge a row
- **Strong:** `shares_link_with` is not empty. Operators reuse invite links, so this is the same signal your Network page is built on. Add it, and set `cluster_key` to that shared link for the new account and the existing ones.
- **Decent:** a `t.me` link in the bio, young account (created in the last few months), very few followers, funnel wording ("free alerts", "tap in", "join").
- **Weak, check by hand:** no `t.me` link at all (only a post mentioning "telegram"), or an older account with real followers and normal trading posts. These may be legit traders who mentioned a channel once. Skip them or open the `evidence` post URL first.
- Your site's own rule applies: listing means flagged for investigation, not a finding of fraud.

## Adding accepted rows to accounts.json
- Copy the row's fields as they are, drop `evidence` and `shares_link_with`.
- Add `listing_id` as the next number after the highest `TS-###`, `link_status` (`ok` if you opened the link and it resolves, otherwise leave as is), `link_statuses`, and `cluster_key` (the normalized link if two or more accounts share it, otherwise `null`).
- Set `tier`: `reported` for a single observation, `corroborated` when it shares a link with another account, `verified` only after a human has checked proof.
- Skip anyone already present (match on username case-insensitively, or `profile_id`).
- Regenerate `accounts.csv` and the Network page the same way you do today.

## Notes
- Telegram invite hashes (`t.me/+AbC...`) are case-sensitive. Always keep the original-case link in `telegram_links`; the lowercased `telegram_links_norm` is only for matching, and a lowercased invite will not resolve.
- Expect a low yield from the feed sweep itself (about 1 new Telegram-linked account per 1,200 authors scanned). The big finds usually come from mining scam-list posts for @-tagged accounts and from usernames that share a link with a known account.
- The scanner only sees what is in the recent public feed, so a clean run does not mean there is nothing else out there. Run it again every few days.
- If a request fails it retries with backoff; if the whole run stops early, rerun it.
- Do not add any form-posting, following, or Telegram-joining logic to it.
