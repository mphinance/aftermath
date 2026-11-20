#!/bin/bash
# Trader-source refresh (Coolify host cron). Passive: public AfterHour API reads only (no auth, no posting).
# Pulls every entry in trader_watchlist.json, rebuilds api/trader-signals.json, publishes it atomically to the webroot.
# Mirrors scripts/run_watch.sh: hard reset to origin/main, own PATH, log under reports/, non-zero exit on failure.
# Run from a checkout of this repo (server: /home/mph/apps/aftermath-watch); the checkout is hard-reset every run,
# so never hand-edit it. Needs in the sparse list: pull_trader_posts.py build_trader_signals.py afterhour.py
# trader_watchlist.json scripts/run_traders.sh (plus whatever build_trader_signals.py imports).
set -u
export PATH="/usr/local/bin:/usr/bin:/bin:${PATH:-}"
cd "$(dirname "$0")/.." || exit 1
PUBLISH_DIR="${PUBLISH_DIR:-/home/mph/apps/ah-portal/api}"
mkdir -p reports/traders data/traders api
LOG="reports/traders/run_traders.log"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }
fail() { log "FAIL: $*"; exit 1; }

# One run at a time (own lock, same pattern as the other cron wrappers)
exec 9>/tmp/aftermath-traders.lock
flock -n 9 || { log "another run holds the lock, skipping"; exit 0; }

log "start"
# Hard reset to origin/main (skipped when SKIP_RESET=1, e.g. local test runs)
if [ "${SKIP_RESET:-0}" != "1" ]; then
  git fetch --quiet origin main >>"$LOG" 2>&1 || fail "git fetch"
  git reset --hard --quiet origin/main >>"$LOG" 2>&1 || fail "git reset"
fi

# Freshness stamp: only publish a file built by THIS run, never the committed copy from the reset
STAMP="$(mktemp)"; trap 'rm -f "$STAMP"' EXIT

timeout 1800 python3 pull_trader_posts.py --all >>"$LOG" 2>&1 || fail "pull_trader_posts.py (exit $?)"
python3 build_trader_signals.py >>"$LOG" 2>&1 || fail "build_trader_signals.py (exit $?)"

OUT="api/trader-signals.json"
[ "$OUT" -nt "$STAMP" ] || fail "$OUT not rebuilt by this run"
python3 - "$OUT" "$PUBLISH_DIR/trader-signals.json" >>"$LOG" 2>&1 <<'PY' || fail "publish gate (invalid, empty or shrank vs live)"
import json, sys
def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None
new, live = load(sys.argv[1]), load(sys.argv[2])
if not isinstance(new, dict) or not new.get("traders"):
    print("new file invalid or has no traders"); sys.exit(1)
if isinstance(live, dict) and len(new["traders"]) < len(live.get("traders") or []):
    print("would drop traders: live", len(live["traders"]), "-> new", len(new["traders"])); sys.exit(1)
PY

if [ -d "$PUBLISH_DIR" ]; then
  cp "$OUT" "$PUBLISH_DIR/.trader-signals.json.tmp" && mv "$PUBLISH_DIR/.trader-signals.json.tmp" "$PUBLISH_DIR/trader-signals.json" \
    || fail "publish copy"
  log "published trader-signals.json"
else
  log "PUBLISH_DIR $PUBLISH_DIR missing, built only"
fi
log "done"
