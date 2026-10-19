#!/bin/bash
# Daily verified-owner leaderboard snapshot (Coolify host cron, Mon-Fri 21:05 UTC, after the close).
# Writes data/ah_archive/positioning/YYYY-MM-DD.json.gz only; publishes nothing. History lives on the server.
set -u
cd "$(dirname "$0")/.." || exit 1
exec 9>/tmp/aftermath-positioning.lock
flock -n 9 || exit 0
timeout 600 python3 ah_positioning.py
