#!/usr/bin/env python3
"""
tg_watch.py: track changes in the Telegram funnel over time. Passive, no account, no joins.

Each run: (1) snapshots every channel via tg_recon.py, (2) re-checks every flagged AfterHour
profile via the public profile API, (3) diffs both against the previous snapshot, and
(4) appends new public posts to a de-duplicated archive. Writes reports/analysis/funnel_watch.md.

  python3 tg_watch.py            # run once (schedule with cron, e.g. daily)
  python3 tg_watch.py --no-fetch # re-diff the two newest snapshots, no network

Signals worth acting on: link rotation (bio link changed), deleted accounts, dead or revived
channels, member jumps, description rewrites, new wallets/prices/admins, new cross-promoted
channels, and new accounts landing on a known invite link.
"""
import argparse, json, subprocess, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
SNAP = BASE / "data" / "telegram_funnel" / "snapshots"
ARCHIVE = BASE / "data" / "telegram_funnel" / "posts_archive.jsonl"
REPORT = BASE / "reports" / "analysis" / "funnel_watch.md"
UA = "Mozilla/5.0 (tg_watch passive research)"


def profile(username):
    try:
        req = urllib.request.Request(f"https://api.afterhour.com/public/profile?username={username}", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        return {"exists": True, "link_in_bio": d.get("linkInBio"), "bio": d.get("bio"), "followers": d.get("numFollowers")}
    except urllib.error.HTTPError as e:
        return {"exists": False} if e.code == 404 else None
    except Exception:
        return None


def snapshot(stamp):
    SNAP.mkdir(parents=True, exist_ok=True)
    rec = SNAP / f"recon_{stamp}.json"
    subprocess.run([sys.executable, str(BASE / "tg_recon.py"), "--known", str(BASE / "accounts.json"), "--out", str(rec)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    prof = {}
    for a in json.load(open(BASE / "accounts.json")):
        p = profile(a["username"])
        if p is not None:
            prof[a["username"]] = p
        time.sleep(0.35)
    (SNAP / f"profiles_{stamp}.json").write_text(json.dumps(prof, indent=1))
    # archive new public posts (dedupe on post id)
    seen = set()
    if ARCHIVE.exists():
        seen = {json.loads(l)["id"] for l in ARCHIVE.open() if l.strip()}
    new = 0
    with ARCHIVE.open("a") as f:
        for c in json.load(open(rec))["channels"]:
            for p in c.get("recent_posts", []):
                if p.get("id") and p["id"] not in seen:
                    seen.add(p["id"]); new += 1
                    f.write(json.dumps({**p, "channel": c["link"], "first_seen": stamp}, ensure_ascii=False) + "\n")
    return new


def latest_two():
    r = sorted(SNAP.glob("recon_*.json"))
    return (r[-2], r[-1]) if len(r) >= 2 else (None, r[-1] if r else None)


def diff(old_rec, new_rec):
    ts_old, ts_new = old_rec.stem[6:], new_rec.stem[6:]
    O = {c["link"]: c for c in json.load(open(old_rec))["channels"]}
    N = {c["link"]: c for c in json.load(open(new_rec))["channels"]}
    out = []
    for l, n in N.items():
        o = O.get(l)
        if not o:
            out.append(f"- NEW channel in list: {l} ({(n['preview'] or {}).get('title')})"); continue
        if o["alive"] != n["alive"]:
            out.append(f"- {'REVIVED' if n['alive'] else 'WENT DEAD'}: {l} ({(o['preview'] or {}).get('title')})")
        om, nm = (o["preview"] or {}).get("members"), (n["preview"] or {}).get("members")
        if om and nm and abs(nm - om) >= max(100, om * 0.1):
            out.append(f"- members {om:,} -> {nm:,} ({nm - om:+,}): {l} ({(n['preview'] or {}).get('title')})")
        od, nd = (o["preview"] or {}).get("description"), (n["preview"] or {}).get("description")
        if o["alive"] and n["alive"] and od != nd:
            out.append(f"- description rewritten: {l}")
        if (o["preview"] or {}).get("title") != (n["preview"] or {}).get("title") and o["alive"] and n["alive"]:
            out.append(f"- renamed: {l}: {(o['preview'] or {}).get('title')!r} -> {(n['preview'] or {}).get('title')!r}")
        for k, vals in n["fingerprints"].items():
            fresh = set(vals) - set(o["fingerprints"].get(k, []))
            if fresh and k not in ("urls",):
                out.append(f"- NEW {k} on {l}: {', '.join(sorted(fresh))[:160]}")
    s_old, s_new = json.load(open(old_rec))["summary"], json.load(open(new_rec))["summary"]
    for t in set(s_new["cross_promoted_unknown_channels"]) - set(s_old["cross_promoted_unknown_channels"]):
        out.append(f"- NEW cross-promoted channel not on the list: {t}")
    po_f, pn_f = SNAP / f"profiles_{ts_old}.json", SNAP / f"profiles_{ts_new}.json"
    if po_f.exists() and pn_f.exists():
        po, pn = json.load(open(po_f)), json.load(open(pn_f))
        for u, n in pn.items():
            o = po.get(u)
            if not o:
                continue
            if o.get("exists") and not n.get("exists"):
                out.append(f"- ACCOUNT GONE: @{u} (deleted or banned)")
            elif o.get("link_in_bio") != n.get("link_in_bio") and n.get("exists"):
                out.append(f"- LINK ROTATED: @{u}: {o.get('link_in_bio')} -> {n.get('link_in_bio')}")
    return ts_old, ts_new, out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--no-fetch", action="store_true"); a = ap.parse_args()
    new_posts = 0
    if not a.no_fetch:
        new_posts = snapshot(datetime.now(timezone.utc).strftime("%Y%m%d_%H%M"))
    old, new = latest_two()
    if not new:
        print("no snapshots"); return
    if not old:
        print(f"first snapshot saved ({new.name}); run again later to diff"); return
    ts_old, ts_new, ch = diff(old, new)
    lines = [f"# Funnel watch: {ts_old} -> {ts_new}", "", f"{len(ch)} change(s); {new_posts} new public post(s) archived.", ""] + (ch or ["- no changes"])
    REPORT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
