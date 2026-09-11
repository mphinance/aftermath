#!/usr/bin/env python3
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
from afterhour import _get, API_BASE, normalize

ACTIVE_FILE = str(BASE_DIR / "data" / "following" / "following_active.json")
OUTPUT_JSON = str(BASE_DIR / "data" / "following" / "following_frequency_accurate.json")
OUTPUT_MD = str(BASE_DIR / "reports" / "following_frequency.md")

with open(ACTIVE_FILE) as f:
    active_users = json.load(f)

NOW = datetime.fromisoformat("2026-09-10T14:17:00")
cutoff_7d = (NOW - timedelta(days=7)).strftime("%Y-%m-%d")
cutoff_30d = (NOW - timedelta(days=30)).strftime("%Y-%m-%d")

print(f"[*] Fetching true 50-post batches for all {len(active_users)} active follows...")

recalculated = []

for u in active_users:
    pid = u["profile_id"]
    username = u["username"]
    url = f"{API_BASE}?take=50&contentTypes=post&authorId={pid}"
    
    try:
        page = _get(url, retries=2, timeout=10)
        items = page.get("items", []) if isinstance(page, dict) else []
        total_lifetime = page.get("totalCount", len(items)) if isinstance(page, dict) else len(items)
        
        # Filter posts
        p_7d = 0
        p_30d = 0
        tickers_mentioned = []
        dates = []
        
        for item in items:
            p = item.get("post") or {}
            created_at = p.get("createdAt") or item.get("createdAt") or ""
            date_str = created_at[:10]
            if not date_str:
                continue
            
            try:
                dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
            except Exception:
                pass
                
            if date_str >= cutoff_7d:
                p_7d += 1
            if date_str >= cutoff_30d:
                p_30d += 1
                
            # extract tickers
            for s in (item.get("securities") or []):
                if s and s.get("tickerSymbol"):
                    tickers_mentioned.append(s["tickerSymbol"])
        
        # Interval
        avg_interval = None
        if len(dates) >= 2:
            span = (dates[0] - dates[-1]).days
            avg_interval = round(span / (len(dates) - 1), 1)
            
        unique_tickers = list(dict.fromkeys(tickers_mentioned))[:4]
        
        # Classification
        if p_7d >= 10:
            cadence = "Hyperactive Machine (>1/day)"
        elif p_7d >= 3:
            cadence = "Daily Regular (3-9/week)"
        elif p_7d >= 1:
            cadence = "Weekly Swing (1-2/week)"
        elif p_30d >= 1:
            cadence = "Occasional Swing (1-3/mo)"
        else:
            cadence = "Dormant / Cooldown"

        latest_title = u.get("latest_title", "")
        
        recalculated.append({
            "username": username,
            "cadence": cadence,
            "posts_7d": p_7d,
            "posts_30d": p_30d,
            "lifetime_posts": total_lifetime,
            "avg_interval_days": avg_interval,
            "top_tickers": ", ".join(unique_tickers) if unique_tickers else "Macro/Chat",
            "last_active": u.get("last_active_date"),
            "profile_url": u["profile_url"],
            "latest_signal": latest_title
        })
        print(f"[+] @{username:16} | 7D: {p_7d:2d} | 30D: {p_30d:2d} | Lifetime: {total_lifetime:4d} | {cadence}")
    except Exception as e:
        print(f"[-] Error fetching @{username}: {e}")

# Sort strictly by real 7-day post volume descending
recalculated.sort(key=lambda x: (x["posts_7d"], x["posts_30d"]), reverse=True)

with open(OUTPUT_JSON, "w") as f:
    json.dump(recalculated, f, indent=2)

with open(OUTPUT_MD, "w") as f:
    f.write("# Accurate Post Frequency & Velocity Breakdown\n\n")
    f.write(f"**Cohort Size:** {len(recalculated)} Verified Active Accounts\n\n")
    f.write("| Rank | Trader | Cadence Tier | 7-Day Volume | 30-Day Volume | Lifetime Posts | Focus Tickers | Latest Signal Preview |\n")
    f.write("| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |\n")
    for idx, row in enumerate(recalculated, 1):
        f.write(f"| {idx} | **@{row['username']}** | `{row['cadence']}` | **{row['posts_7d']}** | {row['posts_30d']} | {row['lifetime_posts']} | `{row['top_tickers']}` | {row['latest_signal']} |\n")

print("\n[+] Done recalculating true frequency.")
