#!/usr/bin/env python3
"""Build api/funnel.json from accounts.json (curated by telegramscammers.com) plus our
post-history pass in data/telegram_funnel/. Run standalone or from build_github_pages.py."""
import json, re, collections as C
from pathlib import Path
BASE = Path(__file__).resolve().parent
SITE = "https://telegramscammers.com"
accts = json.load(open(BASE / "accounts.json"))
rows, links = [], C.defaultdict(list)
for a in accts:
    f = BASE / "data" / "telegram_funnel" / f"{a['username']}.json"
    P = json.load(open(f)) if f.exists() else []
    tick = C.Counter(t for p in P for t in (p.get("tickers") or "").split(",") if t)
    dup = C.Counter(p.get("body", "").strip() for p in P if p.get("body", "").strip())
    link = (a.get("telegram_links_norm") or [None])[0]
    if link:
        links[link].append(a["username"]) if a["username"] not in links[link] else None
    rows.append({
        "listing_id": a["listing_id"], "username": a["username"], "tier": a["tier"],
        "telegram_link": link, "cluster_key": a.get("cluster_key"),
        "bio": a.get("bio"), "created_at": a.get("created_at"),
        "num_followers": a.get("num_followers"), "post_count": len(P),
        "posts_mentioning_telegram": sum(1 for p in P if re.search(r"t\.me|telegram", p.get("body", ""), re.I)),
        "max_duplicate_post": max(dup.values(), default=0),
        "top_tickers": [t for t, _ in tick.most_common(3)],
        "afterhour_url": f"https://afterhour.com/{a['username']}",
        "listing_url": f"{SITE}/database",
    })
clusters = [{"link": l, "accounts": u} for l, u in sorted(links.items(), key=lambda x: -len(x[1])) if len(u) > 1]
out = {
    "source": "TelegramScammers.com open data, enriched by AfterMath post-history pass",
    "credit": SITE, "database": f"{SITE}/database", "network": f"{SITE}/network",
    "submit_intel": f"{SITE}/submit", "upstream_json": f"{SITE}/accounts.json",
    "disclaimer": "Flagged for investigation, not a finding of fraud. Tiers: reported (single observation), corroborated (shared Telegram link across accounts), verified (proof captured and admin-checked).",
    "count": len(rows), "tiers": dict(C.Counter(r["tier"] for r in rows)),
    "shared_link_clusters": clusters, "accounts": rows,
}
(BASE / "api" / "funnel.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(f"api/funnel.json: {len(rows)} accounts, {len(clusters)} shared-link clusters")
