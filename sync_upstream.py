#!/usr/bin/env python3
"""
sync_upstream.py: pull the flag list from https://telegramscammers.com/accounts.json into accounts.json.

The upstream site owner curates the list and is the source of truth; we never edit it by hand. A plain public GET,
validated before anything is written: a bad or truncated download never replaces a good file.

  python3 sync_upstream.py              # update accounts.json if upstream changed
  python3 sync_upstream.py --dry-run    # show what would change
Exit codes: 0 ok (changed or unchanged), 2 validation failed or download failed (accounts.json untouched).
"""
import argparse, json, sys, urllib.request
from pathlib import Path

URL = "https://telegramscammers.com/accounts.json"
BASE = Path(__file__).resolve().parent
TIERS = {"reported", "corroborated", "verified"}
REQUIRED = {"username", "listing_id", "tier", "telegram_links"}


def norm_link(link):
    """'https://www.t.me/Foo?x=1/' -> 't.me/foo' (matching form; invite hashes lose case HERE ONLY, keep telegram_links raw)."""
    l = (link or "").strip().lower()
    for p in ("https://", "http://"):
        if l.startswith(p): l = l[len(p):]
    l = l.replace("www.", "", 1) if l.startswith("www.") else l
    l = l.replace("telegram.me/", "t.me/", 1) if l.startswith("telegram.me/") else l
    return l.split("?")[0].split("#")[0].rstrip("/")


def fill_derived(up):
    """Rows added by hand upstream can lack derived fields; add them (never overwrite his values)."""
    for a in up:
        if not a.get("telegram_links_norm"):
            a["telegram_links_norm"] = [norm_link(l) for l in a.get("telegram_links") or []]
        if not a.get("telegram_handles"):
            a["telegram_handles"] = [l.rstrip("/").split("/")[-1] for l in a.get("telegram_links") or []]
        if "num_followers" not in a and "followers" in a:
            a["num_followers"] = a["followers"]
        a.setdefault("profile_id", None)
    return up


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (sync_upstream; public read-only)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def validate(up, current_count):
    if not isinstance(up, list) or not up:
        return "upstream is not a non-empty list"
    names, ids = set(), set()
    for a in up:
        if not isinstance(a, dict) or not REQUIRED <= set(a):
            return f"row missing required keys: {a.get('username') if isinstance(a, dict) else a!r}"
        if a["tier"] not in TIERS:
            return f"unknown tier {a['tier']!r} for {a['username']}"
        k = a["username"].lower()
        if k in names or a["listing_id"] in ids:
            return f"duplicate username or listing_id: {a['username']} / {a['listing_id']}"
        names.add(k); ids.add(a["listing_id"])
    if current_count and len(up) < 0.8 * current_count:
        return f"upstream shrank from {current_count} to {len(up)} (more than 20%), refusing to overwrite"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--file", default=str(BASE / "accounts.json"))
    a = ap.parse_args()
    path = Path(a.file)
    mine = json.load(open(path)) if path.exists() else []
    try:
        up = fetch(a.url)
    except Exception as e:
        print(f"sync_upstream: download failed: {e}", file=sys.stderr); return 2
    bad = validate(up, len(mine))
    if not bad:
        up = fill_derived(up)
    if bad:
        print(f"sync_upstream: validation failed: {bad}", file=sys.stderr); return 2
    mm = {x["username"].lower(): x for x in mine}
    um = {x["username"].lower(): x for x in up}
    new = [um[k]["username"] for k in um if k not in mm]
    gone = [mm[k]["username"] for k in mm if k not in um]
    tier = [(um[k]["username"], mm[k]["tier"], um[k]["tier"]) for k in um if k in mm and mm[k]["tier"] != um[k]["tier"]]
    changed = json.dumps(up, sort_keys=True) != json.dumps(mine, sort_keys=True)
    print(f"upstream {len(up)} accounts (local {len(mine)}): {len(new)} new, {len(gone)} removed, {len(tier)} tier changes"
          + ("" if changed else "; no changes"))
    for n in new[:20]: print("  + " + n)
    for n in gone[:20]: print("  - " + n)
    for u, o, n in tier[:20]: print(f"  ~ {u}: {o} -> {n}")
    if changed and not a.dry_run:
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(up, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        tmp.replace(path)
        print(f"wrote {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
