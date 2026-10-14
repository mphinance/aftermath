#!/bin/bash
# Daily Telegram-funnel run (Coolify host cron, 13:15 UTC). Passive: public t.me previews, public AfterHour
# profile API and Yahoo public price bars only. Called by /home/mph/apps/aftermath-watch/run_watch.sh after it
# fast-forwards the checkout. Publishes two JSON files to the live webroot, validated and swapped atomically.
set -u
cd "$(dirname "$0")/.." || exit 1
PUBLISH_DIR="${PUBLISH_DIR:-/home/mph/apps/ah-portal/api}"
mkdir -p data/telegram_funnel reports/analysis api
timeout 3000 python3 tg_watch.py        # snapshot, diff vs previous, archive new public posts, parse callouts
timeout 2400 python3 tg_outcomes.py >/dev/null || echo "tg_outcomes failed or timed out (keeping previous outcomes)"
python3 funnel_tickers.py >/dev/null || echo "funnel_tickers failed"
python3 build_funnel_calls.py || echo "build_funnel_calls failed"
if [ -d "$PUBLISH_DIR" ]; then
  for f in funnel-calls.json funnel-tickers.json; do
    if python3 -c "import json,sys; d=json.load(open('api/$f')); sys.exit(0 if d.get('count',0)>0 else 1)"; then
      cp "api/$f" "$PUBLISH_DIR/.$f.tmp" && mv "$PUBLISH_DIR/.$f.tmp" "$PUBLISH_DIR/$f" && echo "published $f"
    else
      echo "skip publish $f (empty or invalid)"
    fi
  done
fi
