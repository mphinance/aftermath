#!/usr/bin/env python3
"""AfterMath pass over accounts.json: posting cadence, ticker promos, funnel language,
whale-universe overlap, link clusters. Writes reports/analysis/funnel_accounts.json + .md"""
import json, re, collections as C, statistics as S
from pathlib import Path
BASE = Path(__file__).resolve().parent
accts = json.load(open(BASE/"accounts.json"))
D = BASE/"data"/"telegram_funnel"
try: whales = {w["username"].lower(): w for w in json.load(open(BASE/"api"/"whales.json")).get("whales", json.load(open(BASE/"api"/"whales.json")) if isinstance(json.load(open(BASE/"api"/"whales.json")), list) else [])}
except Exception: whales = {}
HYPE = re.compile(r"\b(free (alerts?|signals?|channel|group|community)|vip|join|dm|tap in|signals?|alerts?|guaranteed|\d+%|profit|telegram|t\.me|whatsapp|premium|mentor|inbox)\b", re.I)
rows = []
for a in accts:
    f = D/f"{a['username']}.json"
    P = json.load(open(f)) if f.exists() else []
    bodies = [p.get("body","") for p in P]
    tick = C.Counter(t for p in P for t in (p.get("tickers") or "").split(",") if t)
    dates = sorted(p["created_at"] for p in P)
    snaps = sum(1 for p in P if p.get("amount_k"))
    tg_in_posts = sum(1 for b in bodies if re.search(r"t\.me|telegram", b, re.I))
    dup = C.Counter(b.strip() for b in bodies if b.strip())
    maxdup = dup.most_common(1)[0][1] if dup else 0
    rows.append(dict(username=a["username"], listing_id=a["listing_id"], tier=a["tier"],
        created=a["created_at"], followers=a["num_followers"], posts=len(P), snapshots=snaps,
        tg_in_posts=tg_in_posts, max_dup_post=maxdup, top_tickers=tick.most_common(3),
        engagement=sum((p.get("reaction_count") or 0)+(p.get("comment_count") or 0) for p in P),
        hype_bio=bool(HYPE.search(a.get("bio") or "")), link=(a["telegram_links_norm"] or [None])[0],
        cluster=a.get("cluster_key"), whale=a["username"].lower() in whales,
        first=dates[0][:10] if dates else None, last=dates[-1][:10] if dates else None))
out = BASE/"reports"/"analysis"
json.dump(rows, open(out/"funnel_accounts.json","w"), indent=1)
n=len(rows); L=C.Counter()
for r in rows:
    if r["link"]: L[r["link"]]+=1
shared=[(k,v) for k,v in L.items() if v>1]
zero=[r for r in rows if r["posts"]==0]
ph=[r for r in rows if r["posts"]>0]
fol=[r["followers"] for r in rows if r["followers"] is not None]
lines=[f"# Telegram Funnel Accounts: AfterMath pass ({n} accounts)\n",
 f"- Tiers: {dict(C.Counter(r['tier'] for r in rows))}",
 f"- Zero-post accounts: {len(zero)}; accounts with posts: {len(ph)}; total posts: {sum(r['posts'] for r in rows)}",
 f"- Posted a broker snapshot (real money): {sum(1 for r in rows if r['snapshots'])} accounts; verified whales in universe: {sum(r['whale'] for r in rows)}",
 f"- Followers (known n={len(fol)}): median {S.median(fol) if fol else 'n/a'}, max {max(fol) if fol else 'n/a'}, <=5: {sum(f<=5 for f in fol)}",
 f"- Shared invite links (same link, multiple accounts): {len(shared)} links covering {sum(v for _,v in shared)} accounts",
 f"- Posts mentioning t.me/telegram in body: {sum(r['tg_in_posts'] for r in rows)} across {sum(1 for r in rows if r['tg_in_posts'])} accounts",
 f"- Repeat-post spammers (same body >=3x): {[r['username'] for r in rows if r['max_dup_post']>=3]}",
 "\n## Creation cadence (month)", *[f"- {k}: {v}" for k,v in sorted(C.Counter((r['created'] or '?')[:7] for r in rows).items())],
 "\n## Shared links", *[f"- {k}: {[r['username'] for r in rows if r['link']==k]}" for k,_ in shared],
 "\n## Tickers most often in an account's top 3 (see funnel_tickers.md for real post counts)", *[f"- ${t}: {c} accounts" for t,c in C.Counter(t for r in rows for t,c in [(x,1) for x,_ in r['top_tickers']]).most_common(12)],
 "\n## Top by post volume", *[f"- @{r['username']} ({r['tier']}): {r['posts']} posts, {r['followers']} followers, eng {r['engagement']}" for r in sorted(rows,key=lambda r:-r['posts'])[:10]]]
(out/"funnel_accounts.md").write_text("\n".join(lines))
print("\n".join(lines))
