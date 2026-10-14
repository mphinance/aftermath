#!/usr/bin/env python3
"""Build api/funnel.json from accounts.json (curated by telegramscammers.com) plus our
post-history pass in data/telegram_funnel/. Run standalone or from build_github_pages.py."""
import json, re, collections as C
from pathlib import Path
BASE = Path(__file__).resolve().parent
SITE = "https://telegramscammers.com"
TF = BASE / "data" / "telegram_funnel"


def jload(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default


def jsonl(path):
    out = []
    try:
        for line in open(path):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    except Exception:
        pass
    return out


accts = json.load(open(BASE / "accounts.json"))
recon = {}
for ch in (jload(TF / "recon.json", {}) or {}).get("channels", []):
    if ch.get("link"):
        recon[ch["link"].strip().lower()] = ch
rows, links = [], C.defaultdict(list)
for a in accts:
    f = BASE / "data" / "telegram_funnel" / f"{a['username']}.json"
    P = json.load(open(f)) if f.exists() else []
    tick = C.Counter(t for p in P for t in (p.get("tickers") or "").split(",") if t)
    dup = C.Counter(p.get("body", "").strip() for p in P if p.get("body", "").strip())
    alll = []
    for l in a.get("telegram_links_norm") or []:
        if l and l not in alll:
            alll.append(l)
    link = alll[0] if alll else None
    for l in alll:
        if a["username"] not in links[l]:
            links[l].append(a["username"])
    chans = []
    for l in alll:
        rc = recon.get(l.lower())
        if not rc:
            continue
        pv = rc.get("preview") or {}
        chans.append({"link": l, "channel_title": pv.get("title") or None,
                      "channel_members": pv.get("members"), "channel_alive": bool(rc.get("alive")),
                      "public_posts_seen": rc.get("public_posts_seen") or 0})
    first = chans[0] if chans else {}
    rows.append({
        "listing_id": a["listing_id"], "username": a["username"], "tier": a["tier"],
        "telegram_link": link, "telegram_links": alll,
        "channel_title": first.get("channel_title"), "channel_members": first.get("channel_members"),
        "channel_alive": first.get("channel_alive"), "public_posts_seen": first.get("public_posts_seen"),
        "channels": chans, "cluster_key": a.get("cluster_key"),
        "bio": a.get("bio"), "created_at": a.get("created_at"),
        "num_followers": a.get("num_followers"), "post_count": len(P),
        "posts_mentioning_telegram": sum(1 for p in P if re.search(r"t\.me|telegram", p.get("body", ""), re.I)),
        "max_duplicate_post": max(dup.values(), default=0),
        "top_tickers": [t for t, _ in tick.most_common(3)],
        "tickers_pushed": [t for t, _ in tick.most_common(3)],
        "risk_score": a.get("risk_score"), "risk_factors": a.get("risk_factors"), "age_days": a.get("age_days"),
        "afterhour_url": f"https://afterhour.com/{a['username']}",
        "listing_url": f"{SITE}/database",
    })
clusters = [{"link": l, "accounts": u} for l, u in sorted(links.items(), key=lambda x: -len(x[1])) if len(u) > 1]
tk = jload(BASE / "reports" / "analysis" / "funnel_tickers.json", [])
tickers = [{k: t.get(k) for k in ("ticker", "ah_accounts", "ah_posts", "tg_channels", "tg_posts")}
           for t in (tk if isinstance(tk, list) else [])[:15]]

calls = jsonl(TF / "calls.jsonl")
outs = jsonl(TF / "outcomes.jsonl")
scored = [o for o in outs if o.get("status") == "scored" and o.get("return_pct") is not None]
n = len(scored)
rets = sorted(o["return_pct"] for o in scored)
med = None
if n:
    med = rets[n // 2] if n % 2 else (rets[n // 2 - 1] + rets[n // 2]) / 2
posted = sorted((o.get("posted") or "")[:10] for o in scored if o.get("posted"))
outcomes = {
    "n_scored": n,
    "window_start": posted[0] if posted else None,
    "window_end": posted[-1] if posted else None,
    "win_rate": round(sum(1 for o in scored if o.get("win")) / n, 4) if n else None,
    "median_return": round(med, 2) if med is not None else None,
    "share_worth_zero": round(sum(1 for o in scored if o.get("worthless")) / n, 4) if n else None,
    "sample_warning": ("Sample too small to publish rates; need 100 scored callouts." if n < 100
                       else "Callouts from public channels only, scored at expiry vs underlying close; survivorship and parser limits apply."),
}
callouts = {
    "option_opens": sum(1 for c in calls if c.get("kind") == "option" and c.get("action") == "open"),
    "option_closes": sum(1 for c in calls if c.get("kind") == "option" and c.get("action") == "close"),
    "channels_covered": len({c.get("channel") for c in calls if c.get("channel")}),
    "outcomes": outcomes,
}

out = {
    "source": "TelegramScammers.com open data, enriched by AfterMath post-history pass",
    "credit": SITE, "database": f"{SITE}/database", "network": f"{SITE}/network",
    "submit_intel": f"{SITE}/submit", "upstream_json": f"{SITE}/accounts.json",
    "disclaimer": "Flagged for investigation, not a finding of fraud. Tiers: reported (single observation), corroborated (shared Telegram link across accounts), verified (proof captured and admin-checked).",
    "count": len(rows), "tiers": dict(C.Counter(r["tier"] for r in rows)),
    "shared_link_clusters": clusters, "tickers": tickers, "callouts": callouts, "accounts": rows,
}
(BASE / "api" / "funnel.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(f"api/funnel.json: {len(rows)} accounts, {len(clusters)} shared-link clusters")
