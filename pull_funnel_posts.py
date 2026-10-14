#!/usr/bin/env python3
"""Pull full post history for every account in accounts.json (read-only API, serial)."""
import json, sys, time
from pathlib import Path
from afterhour import fetch_all_posts, normalize

BASE = Path(__file__).resolve().parent
OUT = BASE / "data" / "telegram_funnel"
OUT.mkdir(parents=True, exist_ok=True)
accts = json.load(open(BASE / "accounts.json"))
for a in accts:
    f = OUT / f"{a['username']}.json"
    if f.exists():
        continue
    pid = a.get("profile_id")
    if not pid:
        print("no pid", a["username"]); continue
    try:
        posts = [normalize(i) for i in fetch_all_posts(pid)]
    except Exception as e:
        print("FAIL", a["username"], e); continue
    json.dump(posts, open(f, "w"))
    print(a["username"], len(posts), flush=True)
    time.sleep(0.3)
