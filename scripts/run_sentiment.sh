#!/bin/bash
# AfterHour post archive + sentiment publish (Coolify host cron, every 5 minutes, all hours: the feed never sleeps).
# Publishes only api/sentiment.json and api/ah-posts.json into $PUBLISH_DIR (the webroot) when set.
set -u
export PUBLISH_DIR="${PUBLISH_DIR:-/home/mph/apps/ah-portal/api}"
cd "$(dirname "$0")/.." || exit 1
exec 9>/tmp/aftermath-sentiment.lock
flock -n 9 || exit 0
timeout 240 python3 ah_collect.py --pages 5
