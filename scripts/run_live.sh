#!/bin/bash
# Live callout feed (Coolify host cron, every 5 minutes Mon-Fri; tg_live.py itself skips outside 08:00-17:00 ET).
# Publishes only api/funnel-live.json; the daily/capture jobs own every other file.
set -u
cd "$(dirname "$0")/.." || exit 1
timeout 150 python3 tg_live.py --market-hours
