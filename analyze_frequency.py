#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Run split first to make sure active list is fresh
os.system(f'"{sys.executable}" "{BASE_DIR / "split_active_following.py"}" > /dev/null 2>&1')

ACTIVE_FILE = str(BASE_DIR / "data" / "following" / "following_active.json")
NOW = datetime.fromisoformat("2026-09-10T14:13:00")

if not os.path.exists(ACTIVE_FILE):
    print(f"File {ACTIVE_FILE} not found.")
    exit(1)

with open(ACTIVE_FILE) as f:
    active_users = json.load(f)

print(f"[*] Analyzing post frequency for {len(active_users)} active follows...")

frequency_data = []

for u in active_users:
    posts = u.get("recent_posts", [])
    if not posts:
        continue
    
    dates = []
    tickers_mentioned = []
    for p in posts:
        d_str = p.get("date") or (p.get("created_at") or "")[:10]
        if d_str:
            try:
                dates.append(datetime.strptime(d_str, "%Y-%m-%d"))
            except Exception:
                pass
        t_str = p.get("tickers") or ""
        if t_str:
            tickers_mentioned.extend([t.strip() for t in t_str.split(",") if t.strip()])
    
    # Sort dates descending
    dates.sort(reverse=True)
    
    # Counts in last 7 days and last 30 days
    cutoff_7d = NOW - timedelta(days=7)
    cutoff_30d = NOW - timedelta(days=30)
    
    p_7d = sum(1 for d in dates if d >= cutoff_7d)
    p_30d = sum(1 for d in dates if d >= cutoff_30d)
    
    # Calculate span & average interval between recent posts
    avg_interval_days = None
    if len(dates) >= 2:
        span_days = (dates[0] - dates[-1]).days
        avg_interval_days = round(span_days / (len(dates) - 1), 1)
    
    # Classification
    if p_7d >= 3 or (avg_interval_days is not None and avg_interval_days <= 1.5):
        cadence = "Daily / High Volume"
    elif p_7d >= 1 or (avg_interval_days is not None and avg_interval_days <= 5.0):
        cadence = "Weekly Swing Trader"
    elif p_30d >= 1:
        cadence = "Bi-Weekly / Occasional"
    else:
        cadence = "Dormant"
        
    unique_tickers = list(dict.fromkeys(tickers_mentioned))[:4]
    
    frequency_data.append({
        "username": u["username"],
        "profile_url": u["profile_url"],
        "cadence": cadence,
        "posts_last_7d": p_7d,
        "posts_last_30d": p_30d,
        "avg_days_between_posts": avg_interval_days,
        "last_active": u.get("last_active_date"),
        "top_tickers": ", ".join(unique_tickers) if unique_tickers else "Macro/Chat",
        "latest_signal": u.get("latest_title", "")
    })

# Sort by posts_last_7d descending, then last_active
frequency_data.sort(key=lambda x: (x["posts_last_7d"], x["last_active"]), reverse=True)

with open(str(BASE_DIR / "data" / "following" / "following_frequency.json"), "w") as f:
    json.dump(frequency_data, f, indent=2)

REPORT_MD = str(BASE_DIR / "reports" / "following_frequency.md")
with open(REPORT_MD, "w") as f:
    f.write("# Active Following: Post Frequency & Velocity Breakdown\n\n")
    f.write(f"**Cohort Size:** {len(frequency_data)} Active Accounts (Posted since August 11, 2026)\n\n")
    f.write("| Username | Velocity Cadence | 7D Volume | 30D Volume | Avg Interval | Focus Tickers | Latest Signal Preview |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
    for row in frequency_data:
        interval_str = f"{row['avg_days_between_posts']}d" if row['avg_days_between_posts'] is not None else "N/A"
        f.write(f"| **@{row['username']}** | `{row['cadence']}` | **{row['posts_last_7d']}** | {row['posts_last_30d']} | {interval_str} | `{row['top_tickers']}` | {row['latest_signal']} |\n")

print(f"[+] Frequency report generated for {len(frequency_data)} accounts.")
print(f"[+] Written to {REPORT_MD}")
