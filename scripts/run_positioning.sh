#!/bin/bash
# Daily verified-owner leaderboard snapshot (Coolify host cron, Mon-Fri 21:05 UTC, after the close).
# Writes data/ah_archive/positioning/YYYY-MM-DD.json.gz, then publishes the 3+-owner aggregate as positioning.json
# (PUBLISH_DIR, like run_sentiment.sh). Raw snapshots stay on the server.
set -u
export PUBLISH_DIR="${PUBLISH_DIR:-/home/mph/apps/ah-portal/api}"
cd "$(dirname "$0")/.." || exit 1
exec 9>/tmp/aftermath-positioning.lock
flock -n 9 || exit 0
timeout 600 python3 ah_positioning.py && python3 ah_positioning_export.py
