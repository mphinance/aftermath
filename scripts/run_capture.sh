#!/bin/bash
# After-close capture of option price paths for called-out contracts (Coolify cron, Mon-Fri 20:30 UTC = 4:30pm ET).
# Yahoo serves 5-minute option bars for the CURRENT session only, and a contract's bars vanish the day after it
# expires, so this must run every trading day shortly after the close; the archive it builds cannot be rebuilt later.
# Called by /home/mph/apps/aftermath-watch/run_capture.sh after it fast-forwards the checkout. Passive, read-only.
set -u
cd "$(dirname "$0")/.." || exit 1
mkdir -p data/telegram_funnel reports/analysis api
echo "=== capture $(date -u +%FT%TZ) ==="
timeout 900 python3 tg_backfill.py --pages 6 >/dev/null || echo "post refresh failed or timed out"   # newest posts of every public channel
python3 tg_calls.py >/dev/null || echo "tg_calls failed"
timeout 1500 python3 tg_option_paths.py capture || echo "capture failed or timed out"
python3 tg_option_paths.py score >/dev/null || echo "score failed"
