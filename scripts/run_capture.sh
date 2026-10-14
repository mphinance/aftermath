#!/bin/bash
# After-close capture (Coolify cron, Mon-Fri 20:30 UTC = 4:30pm ET). Thin wrapper: scripts/run_watch.sh in capture mode
# refreshes posts, reparses calls, captures Yahoo's 5-minute option bars for the session that just ended, rescored paths,
# and publishes through the same fresh / populated / never-shrinks gate. No credentials needed: Alpaca history is local only.
cd "$(dirname "$0")/.." || exit 1
exec bash scripts/run_watch.sh capture
