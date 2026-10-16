#!/bin/bash
# Whale position-change rotation (Coolify host cron, every 10 minutes, all hours: broker syncs can land any time).
# Publishes only api/whale-changes.json and api/whale-sync.json into $PUBLISH_DIR (the webroot) when set.
set -u
cd "$(dirname "$0")/.." || exit 1
exec 9>/tmp/aftermath-whales.lock
flock -n 9 || exit 0
timeout 280 python3 ah_whales.py --budget 12
