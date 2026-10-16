#!/usr/bin/env python3
"""
ah_whales.py: detect reported position changes in verified PUBLIC whale portfolios.

Public, unauthenticated GETs only. Positions are the last broker sync marked to live prices; most whales'
`lastSyncedAt` is weeks or months old, so real quantity changes are rare and every result carries it.

  python3 ah_whales.py                 # one rotation (<= --budget whales), diff, publish
  python3 ah_whales.py --budget 400    # initial baseline sweep (about 1.2s per whale)
  python3 ah_whales.py --no-fetch      # republish from state

State  : data/ah_archive/whales_state.json   (last snapshot per whale, gitignored)
Changes: data/ah_archive/whale_changes.jsonl (append-only, gitignored)
Publishes api/whale-changes.json and api/whale-sync.json (atomically; $PUBLISH_DIR when set).
Only financialDataPrivacyMode == PUBLIC whales are polled; anyone else is purged.
"""
import argparse, json, os, sys, tempfile, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import afterhour

BASE = Path(__file__).resolve().parent
ARCH_DIR = BASE / "data" / "ah_archive"
STATE = ARCH_DIR / "whales_state.json"
CHANGES = ARCH_DIR / "whale_changes.jsonl"
API = BASE / "api"
PORTFOLIO = "https://api.afterhour.com/stonks/public/portfolio/{pid}/summary/live"
PROFILE = "https://api.afterhour.com/public/profile?username={u}"
TOP_N = 40
TOP_EVERY_H = 0.5
REST_EVERY_H = 12.0
PRIVACY_EVERY_H = 24.0
KEEP_DAYS = 30
MIN_REL = 0.005


def leg_key(p):
    return f"{p.get('accountId') or ''}|{p.get('tickerSymbol')}|{p.get('type')}"


def compact_leg(p):
    spc = p.get("optionsSharesPerContract") or 100
    return {
        "k": leg_key(p), "sym": p.get("tickerSymbol"), "root": p.get("rootTickerSymbol") or p.get("tickerSymbol"),
        "type": p.get("type"), "q": p.get("quantity") or 0.0, "px": p.get("price"), "val": p.get("value"),
        "opt": p.get("optionsContractType"), "strike": p.get("optionsStrikePrice"),
        "exp": (p.get("optionsExpirationDate") or "")[:10] or None,
        "spc": spc if p.get("optionsContractType") else None, "merged": bool(p.get("isMerged")),
    }


def aggregate_legs(positions):
    """Collapse to one leg per key (the same ticker can appear in several lots/accounts)."""
    legs = {}
    for p in positions or []:
        c = compact_leg(p)
        if c["k"] in legs:
            o = legs[c["k"]]
            o["q"] += c["q"]
            o["val"] = (o["val"] or 0) + (c["val"] or 0)
            o["merged"] = True
        else:
            legs[c["k"]] = c
    return legs


def diff_legs(old, new, today, total_value=None):
    """old/new: {key: compact leg}. Returns change dicts (quantity only; price moves are noise)."""
    out = []
    for k in sorted(set(old) | set(new)):
        o, n = old.get(k), new.get(k)
        if o and n:
            dq = n["q"] - o["q"]
            if abs(dq) < max(MIN_REL * abs(o["q"]), 1e-3):
                continue
            action = "ADD" if (dq > 0) == (o["q"] >= 0) else "TRIM"
            if o["q"] * n["q"] < 0:
                action = "FLIP"
            ref = n
        elif n:
            dq, action, ref = n["q"], "OPEN", n
        else:
            dq, ref = -o["q"], o
            action = "EXPIRED" if o.get("exp") and o["exp"] < today else "CLOSE"
        px = ref.get("px") or 0
        notional = dq * px
        c = {"key": k, "symbol": ref["sym"], "root": ref["root"], "type": ref["type"], "action": action,
             "qty_before": o["q"] if o else 0.0, "qty_after": n["q"] if n else 0.0,
             "notional_delta": round(notional, 2),
             "pct_of_portfolio": round(abs(notional) / total_value * 100, 3) if total_value else None,
             "lot_ambiguous": bool((o and o.get("merged")) or (n and n.get("merged")))}
        if ref.get("opt"):
            c.update(option=ref["opt"], strike=ref["strike"], expiry=ref["exp"],
                     contracts_delta=round(dq / (ref.get("spc") or 100), 4))
        out.append(c)
    # heuristic: option CLOSE/OPEN on the same root in one diff looks like a roll
    opens = {c["root"] for c in out if c["action"] == "OPEN" and c.get("option")}
    for c in out:
        if c["action"] == "CLOSE" and c.get("option") and c["root"] in opens:
            c["possible_roll"] = True
    for c in out:
        if c["action"] == "OPEN" and c.get("option") and any(x["action"] == "CLOSE" and x["root"] == c["root"] and x.get("option") for x in out):
            c["possible_roll"] = True
    return out


def load_state():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {}


def atomic_write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"))
    os.replace(tmp, path)


def roster():
    src = API / "whales.json"
    if not src.exists() and os.environ.get("PUBLISH_DIR"):  # server checkout is sparse; the census lives in the webroot
        src = Path(os.environ["PUBLISH_DIR"]) / "whales.json"
    ws = json.load(open(src))["whales"]
    ws = sorted(ws, key=lambda w: w.get("total_value") or 0, reverse=True)
    return [{"username": w["username"], "pid": w["profile_id"], "rank": i} for i, w in enumerate(ws) if w.get("profile_id")]


def due(w, st, now):
    last = (st.get(w["username"]) or {}).get("polled_at")
    if not last:
        return 9e9
    age_h = (now - datetime.fromisoformat(last)).total_seconds() / 3600
    every = TOP_EVERY_H if w["rank"] < TOP_N else REST_EVERY_H
    return age_h / every if age_h >= every else -1


def poll_one(w, st, now, today):
    u = w["username"]
    s = st.get(u) or {}
    pr = s.get("privacy_at")
    if not pr or (now - datetime.fromisoformat(pr)).total_seconds() > PRIVACY_EVERY_H * 3600:
        prof = afterhour._get(PROFILE.format(u=u), retries=3, timeout=30)
        s["privacy"], s["privacy_at"] = prof.get("financialDataPrivacyMode"), now.isoformat()
        time.sleep(0.6)
    if s.get("privacy") != "PUBLIC":
        st.pop(u, None)  # revoked or never public: drop everything we hold
        return [], "purged"
    d = afterhour._get(PORTFOLIO.format(pid=w["pid"]), retries=3, timeout=60)
    positions = d.get("positionSnapshots") or []
    new = aggregate_legs(positions)
    old = s.get("legs")
    changes, status = [], "ok"
    if old is not None and not new and old:
        status = "suspect_empty"  # an empty snapshot must never read as 'closed everything'
    else:
        if old is not None:
            changes = diff_legs(old, new, today, d.get("totalValue"))
        s["legs"] = new
    s.update(polled_at=now.isoformat(), last_synced_at=d.get("lastSyncedAt"), total_value=d.get("totalValue"),
             cash=d.get("cashBalance"), n_positions=len(new))
    st[u] = s
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    for c in changes:
        c.update(ts=stamp, username=u, last_synced_at=d.get("lastSyncedAt"))
    return changes, status


def publish(st, now):
    cut = (now - timedelta(days=KEEP_DAYS)).isoformat()
    rows = []
    if CHANGES.exists():
        for line in CHANGES.read_text().splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r["ts"] >= cut[:19] and r["username"] in st:
                rows.append(r)
    rows.sort(key=lambda r: r["ts"], reverse=True)
    gen = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    syncs = [s.get("last_synced_at") for s in st.values() if s.get("last_synced_at")]
    health = {
        "generated_at": gen, "whales_tracked": len(st),
        "polled_last_hour": sum(1 for s in st.values() if s.get("polled_at") and (now - datetime.fromisoformat(s["polled_at"])).total_seconds() < 3600),
        "never_polled": 0,
        "newest_broker_sync": max(syncs) if syncs else None, "oldest_broker_sync": min(syncs) if syncs else None,
        "synced_within_30d": sum(1 for x in syncs if x >= (now - timedelta(days=30)).isoformat()),
        "note": ("Positions are the last broker sync marked to live prices. A whale's quantities only change when the "
                 "broker link syncs, which for most whales was weeks or months ago. 'Reported position changes', "
                 "not trades, and never advice."),
        "whales": {u: {"last_synced_at": s.get("last_synced_at"), "polled_at": s.get("polled_at"),
                       "n_positions": s.get("n_positions"), "total_value": s.get("total_value")} for u, s in st.items()},
    }
    outdir = Path(os.environ["PUBLISH_DIR"]) if os.environ.get("PUBLISH_DIR") and Path(os.environ["PUBLISH_DIR"]).is_dir() else API
    atomic_write(outdir / "whale-changes.json", {"generated_at": gen, "count": len(rows), "changes": rows[:1000]})
    atomic_write(outdir / "whale-sync.json", health)
    return health, len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=12)
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args()
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    st = load_state()
    n_changes = n_fail = n_done = 0
    if not a.no_fetch:
        ws = [w for w in roster() if due(w, st, now) >= 0]
        ws.sort(key=lambda w: due(w, st, now), reverse=True)
        fails = 0
        for w in ws[: a.budget]:
            if fails >= 3:
                print("[ah_whales] circuit open (3 failures); stopping run", file=sys.stderr)
                break
            try:
                changes, status = poll_one(w, st, now, today)
                fails = 0
                n_done += 1
                if changes:
                    ARCH_DIR.mkdir(parents=True, exist_ok=True)
                    with open(CHANGES, "a", encoding="utf-8") as f:
                        for c in changes:
                            f.write(json.dumps(c, separators=(",", ":")) + "\n")
                    n_changes += len(changes)
                if status != "ok":
                    print(f"[ah_whales] {w['username']}: {status}", file=sys.stderr)
            except Exception as e:
                fails += 1
                n_fail += 1
                print(f"[ah_whales] {w['username']} failed: {str(e)[:80]}", file=sys.stderr)
            time.sleep(1.2)
        atomic_write(STATE, st)
    health, nrows = publish(st, now)
    print(f"[ah_whales] polled {n_done}, failed {n_fail}, +{n_changes} changes, tracking {health['whales_tracked']}, feed {nrows}")


if __name__ == "__main__":
    main()
