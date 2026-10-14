#!/bin/bash
# After-close capture of option price paths for called-out contracts. NOT scheduled anywhere: the server cron entry was removed and path scoring now
# uses Alpaca bars locally (tg_option_paths.py backfill). Yahoo serves 5-minute option bars for the CURRENT session only, and a contract's bars vanish the day after it
# expires, so if this is ever run it must run every trading day shortly after the close; the archive it builds cannot be rebuilt later.
# Historical note: it was once called by /home/mph/apps/aftermath-watch/run_capture.sh. Passive, read-only.
set -u
cd "$(dirname "$0")/.." || exit 1
mkdir -p data/telegram_funnel reports/analysis api
echo "=== capture $(date -u +%FT%TZ) ==="
timeout 900 python3 tg_backfill.py --pages 6 >/dev/null || echo "post refresh failed or timed out"   # newest posts of every public channel
python3 tg_calls.py >/dev/null || echo "tg_calls failed"
timeout 1500 python3 tg_option_paths.py capture || echo "capture failed or timed out"
python3 tg_option_paths.py score >/dev/null || echo "score failed"
