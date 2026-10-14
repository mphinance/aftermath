#!/bin/bash
# Daily Telegram-funnel run (Coolify host cron, 13:15 UTC). Passive: public t.me previews, public AfterHour
# profile API and Yahoo public price bars only. Called by /home/mph/apps/aftermath-watch/run_watch.sh after it
# fast-forwards the checkout. Publishes four JSON files to the live webroot, validated and swapped atomically.
# Every step after tg_watch is failure-tolerant: a failed step keeps the previous data and never aborts the publish.
set -u
cd "$(dirname "$0")/.." || exit 1
PUBLISH_DIR="${PUBLISH_DIR:-/home/mph/apps/ah-portal/api}"
mkdir -p data/telegram_funnel reports/analysis api
timeout 3000 python3 tg_watch.py        # snapshot, diff vs previous, archive new public posts, parse callouts
timeout 2400 python3 tg_outcomes.py >/dev/null || echo "tg_outcomes failed or timed out (keeping previous outcomes)"
python3 funnel_tickers.py >/dev/null || echo "funnel_tickers failed"
python3 build_funnel_calls.py || echo "build_funnel_calls failed"
timeout 1500 python3 tg_fx_signals.py >/dev/null || echo "tg_fx_signals failed or timed out (keeping previous fx signals)"
python3 build_funnel_scorecard.py || echo "build_funnel_scorecard failed"
if [ -d "$PUBLISH_DIR" ]; then
  # file:key that must be a non-empty list for the file to be published
  for spec in funnel-calls.json:count funnel-tickers.json:count funnel-scorecard.json:scorecard funnel-fx-signals.json:count; do
    f="${spec%%:*}"; key="${spec##*:}"
    if python3 - "api/$f" "$key" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
if sys.argv[2] == "scorecard":
    # both halves must be populated, so a failed tg_fx_signals run cannot replace a good live scorecard with an FX-less one
    ok = (bool(d.get("generated_at")) and (d.get("options", {}).get("pooled") or {}).get("n_scored", 0) > 0
          and (d.get("fx", {}).get("pooled") or {}).get("n_signals_scored", 0) > 0)
else:
    ok = d.get("count", 0) > 0
sys.exit(0 if ok else 1)
PY
    then
      cp "api/$f" "$PUBLISH_DIR/.$f.tmp" && mv "$PUBLISH_DIR/.$f.tmp" "$PUBLISH_DIR/$f" && echo "published $f"
    else
      echo "skip publish $f (empty or invalid)"
    fi
  done
fi
