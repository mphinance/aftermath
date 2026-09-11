#!/usr/bin/env python3
"""
Pulls 100% of the lifetime posts for a single user, normalizes them,
and writes both a raw JSON dump and a clean chronological Markdown archive.
"""
import sys
import os
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
from afterhour import fetch_all_posts, profile_id, normalize

if len(sys.argv) < 2:
    print("Usage: download_single_trader_lifetime.py <username>")
    sys.exit(1)

username = sys.argv[1].lstrip("@")
print(f"[*] Resolving @{username}...")
pid = None

# Check cache first
for cache_file in [
    str(BASE_DIR / "data" / "following" / "following_active.json"),
    str(BASE_DIR / "data" / "following" / "following_intel.json"),
]:
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                cdata = json.load(f)
                for item in cdata:
                    if item.get("username", "").lower() == username.lower() and item.get("profile_id"):
                        pid = item["profile_id"]
                        break
        except Exception:
            pass
    if pid:
        break

if not pid:
    try:
        pid = profile_id(username)
    except Exception as e:
        print(f"[-] Profile lookup failed: {e}")
        sys.exit(1)

print(f"[+] Found profile ID: {pid}")

RAW_JSON = str(BASE_DIR / "data" / "following" / f"@{username}_all_posts.json")
RAW_MD = str(BASE_DIR / "reports" / "posts" / f"@{username}_lifetime.md")

def progress(current, total):
    print(f"[*] Fetched {current}/{total} posts...", end="\r", flush=True)

print(f"[*] Downloading 100% lifetime post history for @{username}...")
raw_items = fetch_all_posts(pid, progress_cb=progress)
print(f"\n[+] Total items fetched: {len(raw_items)}")

# Normalize and sort chronological ascending (earliest to latest)
normalized = [normalize(it) for it in raw_items]
normalized.sort(key=lambda x: x.get("created_at") or x.get("date") or "")

with open(RAW_JSON, "w", encoding="utf-8") as f:
    json.dump(normalized, f, indent=2)

with open(RAW_MD, "w", encoding="utf-8") as f:
    f.write(f"# Complete Lifetime Post Archive: @{username}\n\n")
    f.write(f"- **Profile**: [https://afterhour.com/{username}](https://afterhour.com/{username})\n")
    f.write(f"- **Profile ID**: `{pid}`\n")
    f.write(f"- **Total Lifetime Posts**: {len(normalized)}\n")
    if normalized:
        f.write(f"- **Date Range**: {normalized[0].get('date')} to {normalized[-1].get('date')}\n\n")
    f.write("---\n\n")
    
    for idx, p in enumerate(normalized, 1):
        date = (p.get("created_at") or p.get("date") or "")[:16].replace("T", " ")
        tickers = p.get("tickers") or ""
        tag = p.get("tag") or ""
        gl = p.get("gain_loss") or ""
        title = p.get("title") or ""
        body = p.get("body") or ""
        url = p.get("share_url") or ""
        
        tag_str = f" `[{tag}]`" if tag else ""
        gl_str = f" `[{gl}]`" if gl else ""
        ticker_str = f" — `${tickers.replace(',', ', $')}`" if tickers else ""
        
        f.write(f"### Post #{idx}: {date}{ticker_str}{tag_str}{gl_str}\n\n")
        if title:
            f.write(f"**{title}**\n\n")
        if body:
            f.write(f"{body}\n\n")
        if url:
            f.write(f"*Link: {url}*\n\n")
        f.write("---\n\n")

print(f"[+] Successfully saved {len(normalized)} lifetime posts to:")
print(f"    - {RAW_JSON}")
print(f"    - {RAW_MD}")
