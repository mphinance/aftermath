#!/bin/bash
# Daily Telegram-funnel run (Coolify host cron, 13:15 UTC). Passive: public t.me previews, public AfterHour
# profile API and Yahoo public price bars only. Called by /home/mph/apps/aftermath-watch/run_watch.sh after it
# fast-forwards the checkout. Publishes four JSON files to the live webroot, validated and swapped atomically.
# Every step after tg_watch is failure-tolerant: a failed step keeps the previous data and never aborts the publish.
set -u
cd "$(dirname "$0")/.." || exit 1
PUBLISH_DIR="${PUBLISH_DIR:-/home/mph/apps/ah-portal/api}"
mkdir -p data/telegram_funnel reports/analysis api
# Freshness stamp: a file counts as built by THIS run only if it is newer than this marker. After the git reset the
# checkout holds committed copies of api/*.json; without this check a failed build would publish them over the live files.
STAMP="$(mktemp)"; trap 'rm -f "$STAMP"' EXIT
MODE="${1:-full}"   # full = morning run (13:15 UTC); capture = after-close run (Mon-Fri 20:30 UTC): newest posts, Yahoo bars for today's session
if [ "$MODE" = "capture" ]; then
  # Yahoo serves 5-minute option bars for the CURRENT session only, so this must run after every close; the archive it builds
  # (data/telegram_funnel/option_bars, merged by timestamp) also holds the Alpaca history seeded from the owner's machine.
  timeout 900 python3 tg_backfill.py --pages 6 >/dev/null || echo "post refresh failed or timed out"
  python3 tg_calls.py >/dev/null || echo "tg_calls failed"
  timeout 1500 python3 tg_option_paths.py capture || echo "option bar capture failed or timed out"
else
  python3 sync_upstream.py || echo "sync_upstream failed (keeping current accounts.json)"
  timeout 900 python3 pull_funnel_posts.py >/dev/null || echo "pull_funnel_posts failed or timed out"   # fetches history for NEW accounts only
  timeout 3000 python3 tg_watch.py        # snapshot, diff vs previous, archive new public posts, parse callouts
  timeout 2400 python3 tg_outcomes.py >/dev/null || echo "tg_outcomes failed or timed out (keeping previous outcomes)"
fi
# build_funnel.py reads data/telegram_funnel/recon.json: point it at the snapshot tg_watch just took
latest=$(ls -1 data/telegram_funnel/snapshots/recon_*.json 2>/dev/null | tail -1)
[ -n "$latest" ] && cp "$latest" data/telegram_funnel/recon.json
[ "$MODE" = "capture" ] || { python3 funnel_tickers.py >/dev/null || echo "funnel_tickers failed"; }
python3 build_funnel_calls.py || echo "build_funnel_calls failed"
if [ "$MODE" != "capture" ]; then
  timeout 1500 python3 tg_fx_signals.py >/dev/null || echo "tg_fx_signals failed or timed out (keeping previous fx signals)"
  python3 build_funnel_scorecard.py || echo "build_funnel_scorecard failed"
fi
python3 tg_option_paths.py score >/dev/null || echo "tg_option_paths score failed"
python3 build_funnel_paths.py || echo "build_funnel_paths failed"
python3 build_funnel.py || echo "build_funnel failed"
python3 build_funnel_export.py || echo "build_funnel_export failed"
if [ -d "$PUBLISH_DIR" ]; then
  # Publish gate, per file (FORCE_PUBLISH=1 skips the shrink check only, never the freshness check):
  #   1. fresh: built by this run (newer than $STAMP), so a failed build cannot republish the committed copy
  #   2. populated: count > 0 (scorecard: both options and FX halves)
  #   3. never shrinks (the path-enriched funnel-calls-full.json and funnel.json (callouts.paths n_scored) also must not lose their path count: price paths are built
  #      locally only, so a server rebuild cannot replace the local file; funnel-option-paths.json is published only when its pooled n does not shrink): against the file already live, options n_scored and callout totals must stay >= 80% and FX
  #      scored signals >= 50% (FX ages out of Yahoo's 60-day 5m window, options only accumulate). A run on a thin
  #      archive (e.g. the server's, which is smaller than the local one) therefore cannot replace a richer live file.
  for spec in funnel.json:funnel funnel-option-paths.json:paths funnel-calls-full.json:callsfull funnel-calls.json:count funnel-tickers.json:count funnel-scorecard.json:scorecard funnel-fx-signals.json:fx; do
    f="${spec%%:*}"; key="${spec##*:}"
    if [ ! "api/$f" -nt "$STAMP" ]; then echo "skip publish $f (not rebuilt by this run)"; continue; fi
    if python3 - "api/$f" "$PUBLISH_DIR/$f" "$key" "${FORCE_PUBLISH:-0}" <<'PY'
import json, sys
new_p, live_p, key, force = sys.argv[1:5]
def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None
def metrics(d, key):
    if key == "scorecard":
        return {"options n_scored": ((d.get("options") or {}).get("pooled") or {}).get("n_scored", 0),
                "fx n_signals_scored": ((d.get("fx") or {}).get("pooled") or {}).get("n_signals_scored", 0)}
    if key == "callsfull":      # path_count is only non-zero when built where the local bar archive exists (never on the server)
        return {"total": d.get("count", 0), "path_count": d.get("path_count", 0)}
    if key == "funnel":         # callouts.paths (the /scamcheck headline) only exists when built where the bar archive is (never on the server)
        return {"total": d.get("count", 0), "path_count": ((d.get("callouts") or {}).get("paths") or {}).get("n_scored", 0)}
    if key == "paths":          # price-path scoring: pooled intraday n_scored must never shrink below the live file
        return {"total": (((d.get("pooled") or {}).get("intraday")) or {}).get("n", 0)}
    return {"total": d.get("total_parsed") or d.get("count", 0)}
OPTIONAL = {"path_count"}       # may be zero in a new file, but must never drop below what is already live
MIN_KEEP = {"options n_scored": 0.8, "fx n_signals_scored": 0.5, "total": 0.5 if key == "fx" else 0.8, "path_count": 1.0}
new, live = load(new_p), load(live_p)
if not isinstance(new, dict):
    print("  invalid json"); sys.exit(1)
nm = metrics(new, key)
if not all(v > 0 for k, v in nm.items() if k not in OPTIONAL) or (key == "scorecard" and not new.get("generated_at")):
    print("  empty or half-populated:", nm); sys.exit(1)
if isinstance(live, dict) and force != "1":
    lm = metrics(live, key)
    for k, v in nm.items():
        if v < MIN_KEEP[k] * lm.get(k, 0):
            print(f"  would shrink {k}: live {lm.get(k)} -> new {v}"); sys.exit(1)
sys.exit(0)
PY
    then
      cp "api/$f" "$PUBLISH_DIR/.$f.tmp" && mv "$PUBLISH_DIR/.$f.tmp" "$PUBLISH_DIR/$f" && echo "published $f"
      if [ "$f" = "funnel-calls-full.json" ] && [ -f api/funnel-calls-full.csv ]; then cp api/funnel-calls-full.csv "$PUBLISH_DIR/.funnel-calls-full.csv.tmp" && mv "$PUBLISH_DIR/.funnel-calls-full.csv.tmp" "$PUBLISH_DIR/funnel-calls-full.csv" && echo "published funnel-calls-full.csv"; fi
    else
      echo "skip publish $f (empty, invalid or smaller than the live file)"
    fi
  done
fi
