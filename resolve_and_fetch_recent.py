#!/usr/bin/env python3
import sys
import os
import json
import time
import urllib.request
import urllib.error
import re

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
from afterhour import profile_id, normalize, _get, API_BASE

INPUT_NAMES = str(BASE_DIR / "data" / "following" / "following_usernames.txt")
OUTPUT_JSON = str(BASE_DIR / "data" / "following" / "following_intel.json")
OUTPUT_MD = str(BASE_DIR / "reports" / "following_directory.md")

with open(INPUT_NAMES) as f:
    candidates = [line.strip() for line in f if line.strip()]

print(f"[*] Loaded {len(candidates)} candidate handles from OCR.")

def try_resolve(name):
    variations = [
        name,
        name.replace("l", "I"),
        name.replace("I", "l"),
        name.replace("0", "O"),
        name.replace("O", "0"),
    ]
    seen = set()
    for v in variations:
        if v in seen:
            continue
        seen.add(v)
        try:
            pid = profile_id(v)
            return v, pid
        except Exception:
            continue
    return name, None

results = []
resolved_count = 0

print("[*] Resolving profiles and fetching latest 5 posts per user...")
for i, name in enumerate(candidates):
    clean_name, pid = try_resolve(name)
    if not pid:
        continue
    
    resolved_count += 1
    profile_url = f"https://afterhour.com/{clean_name}"
    api_url = f"{API_BASE}?take=5&contentTypes=post&authorId={pid}"
    
    # Fetch recent posts (only top 5)
    recent_posts = []
    try:
        page = _get(api_url, retries=2, timeout=10)
        items = page.get("items", []) if isinstance(page, dict) else []
        for item in items[:5]:
            recent_posts.append(normalize(item))
    except Exception as e:
        pass
    
    user_entry = {
        "username": clean_name,
        "profile_id": pid,
        "profile_url": profile_url,
        "feed_api_url": api_url,
        "recent_post_count": len(recent_posts),
        "recent_posts": recent_posts
    }
    results.append(user_entry)
    
    if resolved_count % 10 == 0 or i == len(candidates) - 1:
        print(f"[*] [{resolved_count}] Resolved @{clean_name} ({pid}) - {len(recent_posts)} recent posts")
        # Save intermediate snapshot
        with open(OUTPUT_JSON, "w") as f:
            json.dump(results, f, indent=2)

print(f"\n[+] Successfully resolved {len(results)} active profiles out of {len(candidates)} candidates.")

# Generate summary Markdown
with open(OUTPUT_MD, "w") as f:
    f.write("# AfterHour Following Directory & Recent Signals\n\n")
    f.write(f"**Total Verified Following Profiles:** {len(results)}\n\n")
    f.write("| Username | Profile Link | API Endpoint | Latest Post Title | Tickers |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    for u in results:
        latest = u["recent_posts"][0] if u["recent_posts"] else {}
        title = (latest.get("title") or latest.get("body", ""))[:45].replace("|", "-").replace("\n", " ")
        tickers = latest.get("tickers", "")
        f.write(f"| **@{u['username']}** | [Profile]({u['profile_url']}) | [API]({u['feed_api_url']}) | {title} | `{tickers}` |\n")

print(f"[+] Written full directory to {OUTPUT_JSON} and {OUTPUT_MD}")
