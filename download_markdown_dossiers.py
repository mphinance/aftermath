#!/usr/bin/env python3
"""
Sequential Markdown Dossier Generator for Active AfterHour Following
Pulls recent 50 posts one-by-one and formats clean, searchable Markdown journals.
"""
import sys
import os
import json
import time

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
from afterhour import _get, API_BASE, normalize, profile_id

INPUT_FILE = str(BASE_DIR / "data" / "following" / "following_frequency_accurate.json")
POSTS_DIR = str(BASE_DIR / "reports" / "posts")
INDEX_FILE = os.path.join(POSTS_DIR, "README.md")

os.makedirs(POSTS_DIR, exist_ok=True)

with open(INPUT_FILE) as f:
    active_users = json.load(f)

print(f"[*] Starting sequential Markdown export for {len(active_users)} active accounts...")

index_entries = []

for idx, u in enumerate(active_users, 1):
    username = u["username"]
    print(f"[{idx}/{len(active_users)}] Downloading recent posts for @{username}...")
    
    # We already have profile_id or look it up
    try:
        pid = profile_id(username)
    except Exception:
        continue

    url = f"{API_BASE}?take=50&contentTypes=post&authorId={pid}"
    
    try:
        page = _get(url, retries=3, timeout=12)
        items = page.get("items", []) if isinstance(page, dict) else []
    except Exception as e:
        print(f"  [!] Failed to download posts for @{username}: {e}")
        continue

    # Format Markdown
    md_filename = f"@{username}.md"
    md_filepath = os.path.join(POSTS_DIR, md_filename)
    
    with open(md_filepath, "w", encoding="utf-8") as out:
        out.write(f"# Trader Dossier: @{username}\n\n")
        out.write(f"- **Profile**: [{u['profile_url']}]({u['profile_url']})\n")
        out.write(f"- **Profile ID**: `{pid}`\n")
        out.write(f"- **Cadence**: `{u['cadence']}`\n")
        out.write(f"- **7-Day Volume**: **{u['posts_7d']} posts**\n")
        out.write(f"- **30-Day Volume**: **{u['posts_30d']} posts**\n")
        out.write(f"- **Lifetime Total**: **{u['lifetime_posts']} posts**\n")
        out.write(f"- **Core Tickers**: `{u['top_tickers']}`\n\n")
        out.write("---\n\n")
        out.write("## Recent Posts & Signals (Chronological)\n\n")
        
        if not items:
            out.write("*No recent posts available.*\n")
        
        for item in items:
            norm = normalize(item)
            title = norm.get("title") or ""
            body = norm.get("body") or ""
            date = norm.get("created_at") or norm.get("date") or "Unknown Date"
            tickers = norm.get("tickers") or ""
            tag = norm.get("tag") or ""
            gain_loss = norm.get("gain_loss") or ""
            comments = norm.get("comment_count", 0)
            reactions = norm.get("reaction_count", 0)
            views = norm.get("view_count", 0)
            share_url = norm.get("share_url") or ""
            
            # Format header
            tag_str = f" `[{tag}]`" if tag else ""
            gl_str = f" `[{gain_loss}]`" if gain_loss else ""
            ticker_str = f" — `${tickers.replace(',', ', $')}`" if tickers else ""
            
            out.write(f"### {date[:16].replace('T', ' ')}{ticker_str}{tag_str}{gl_str}\n\n")
            if title:
                out.write(f"**{title}**\n\n")
            if body:
                # Indent quotes or clean block
                clean_body = body.replace("\r\n", "\n")
                out.write(f"{clean_body}\n\n")
            
            meta_parts = []
            if views:
                meta_parts.append(f"👁️ {views} views")
            if reactions:
                meta_parts.append(f"❤️ {reactions} reactions")
            if comments:
                meta_parts.append(f"💬 {comments} comments")
            if share_url:
                meta_parts.append(f"[Direct Link]({share_url})")
            
            if meta_parts:
                out.write(f"*Stats: {' · '.join(meta_parts)}*\n\n")
            
            out.write("---\n\n")
            
    index_entries.append({
        "rank": idx,
        "username": username,
        "cadence": u["cadence"],
        "posts_7d": u["posts_7d"],
        "file": md_filename,
        "tickers": u["top_tickers"]
    })
    
    # Polite delay between requests to keep AfterHour gateway happy
    time.sleep(0.3)

# Build Index README
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write("# AfterHour Active Follows: Markdown Archives\n\n")
    f.write(f"**Total Dossiers:** {len(index_entries)} active trader archives generated.\n\n")
    f.write("| Rank | Trader | 7D Volume | Cadence | Focus Tickers | Markdown Dossier |\n")
    f.write("| :---: | :--- | :---: | :--- | :--- | :--- |\n")
    for row in index_entries:
        f.write(f"| {row['rank']} | **@{row['username']}** | **{row['posts_7d']}** | `{row['cadence']}` | `{row['tickers']}` | [View Posts](./{row['file']}) |\n")

print(f"\n[+] Successfully generated all {len(index_entries)} Markdown dossiers in {POSTS_DIR}!")
