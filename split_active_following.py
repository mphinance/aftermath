#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INTEL_FILE = str(BASE_DIR / "data" / "following" / "following_intel.json")
NOW = datetime.fromisoformat("2026-09-10T14:11:00")
CUTOFF = NOW - timedelta(days=30)
CUTOFF_STR = CUTOFF.strftime("%Y-%m-%d")

if not os.path.exists(INTEL_FILE):
    print(f"File {INTEL_FILE} not found yet.")
    exit(1)

with open(INTEL_FILE) as f:
    users = json.load(f)

active = []
inactive = []

for u in users:
    posts = u.get("recent_posts", [])
    if not posts:
        u["last_active_date"] = "Never / No Posts"
        inactive.append(u)
        continue
    
    # Sort posts by date descending just in case
    latest = posts[0]
    date_str = latest.get("date") or (latest.get("created_at") or "")[:10]
    u["last_active_date"] = date_str or "Unknown"
    u["latest_title"] = (latest.get("title") or latest.get("body") or "")[:60].replace("\n", " ").replace("|", "-")
    u["latest_tickers"] = latest.get("tickers", "")

    if date_str and date_str >= CUTOFF_STR:
        active.append(u)
    else:
        inactive.append(u)

# Sort active by most recent date descending
active.sort(key=lambda x: x.get("last_active_date", ""), reverse=True)
inactive.sort(key=lambda x: x.get("last_active_date", ""), reverse=True)

with open(str(BASE_DIR / "data" / "following" / "following_active.json"), "w") as f:
    json.dump(active, f, indent=2)

with open(str(BASE_DIR / "data" / "following" / "following_inactive.json"), "w") as f:
    json.dump(inactive, f, indent=2)

# Write Active Markdown
with open(str(BASE_DIR / "reports" / "following_active.md"), "w") as f:
    f.write(f"# Active Follows (Posted within last 30 days — Since {CUTOFF_STR})\n\n")
    f.write(f"**Count:** {len(active)} active accounts\n\n")
    f.write("| Username | Last Active | Tickers | Recent Signal / Post Preview | Links |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    for u in active:
        f.write(f"| **@{u['username']}** | `{u['last_active_date']}` | `{u.get('latest_tickers')}` | {u.get('latest_title')} | [Profile]({u['profile_url']}) · [API]({u['feed_api_url']}) |\n")

# Write Inactive Markdown
with open(str(BASE_DIR / "reports" / "following_inactive.md"), "w") as f:
    f.write(f"# Inactive / Dormant Follows (No posts since {CUTOFF_STR})\n\n")
    f.write(f"**Count:** {len(inactive)} dormant accounts\n\n")
    f.write("| Username | Last Active Date | Profile Link |\n")
    f.write("| :--- | :--- | :--- |\n")
    for u in inactive:
        f.write(f"| **@{u['username']}** | `{u['last_active_date']}` | [Profile]({u['profile_url']}) |\n")

print(f"[*] Analysis complete as of {len(users)} processed users:")
print(f"    🟢 Active (<= 30 days): {len(active)}")
print(f"    💤 Inactive / Dormant:  {len(inactive)}")
print(f"    Active Ratio: {len(active)/(len(users) or 1)*100:.1f}%")
