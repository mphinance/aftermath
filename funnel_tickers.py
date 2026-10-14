#!/usr/bin/env python3
"""Tickers called out by flagged funnel accounts: AfterHour post history + archived public Telegram posts.
Writes reports/analysis/funnel_tickers.{json,md}"""
import json, re, collections as C
from pathlib import Path
B = Path(__file__).resolve().parent
accts = json.load(open(B/"accounts.json")); D = B/"data/telegram_funnel"
CASH = re.compile(r"\$([A-Z]{1,5})\b")
# not tickers: common cashtag false hits in promo copy
STOP = {"A","I","S","K","B","C","IT","ON","ALL","ARE","FOR","NOW","AI","CEO","USD","USDT","ATH","PM","AM","EOD","IV","OTM","ITM","TP","SL","TG","VIP"}
ah_posts, ah_accts, ah_first = C.Counter(), C.defaultdict(set), {}
for a in accts:
    f = D/f"{a['username']}.json"
    if not f.exists(): continue
    for p in json.load(open(f)):
        ts = set(t for t in (p.get("tickers") or "").split(",") if t) | set(CASH.findall(p.get("body","") + " " + (p.get("title") or "")))
        for t in ts - STOP:
            ah_posts[t] += 1; ah_accts[t].add(a["username"])
            d = p.get("date") or ""
            ah_first[t] = min(ah_first.get(t, d), d) if d else ah_first.get(t)
tg_posts, tg_chan = C.Counter(), C.defaultdict(set)
arch = D/"posts_archive.jsonl"
if arch.exists():
    for l in arch.open():
        if not l.strip(): continue
        p = json.loads(l)
        for t in set(CASH.findall(p.get("text",""))) - STOP:
            tg_posts[t] += 1; tg_chan[t].add(p["channel"])
allt = set(ah_posts) | set(tg_posts)
rows = sorted(({"ticker": t, "ah_posts": ah_posts[t], "ah_accounts": len(ah_accts[t]), "tg_posts": tg_posts[t], "tg_channels": len(tg_chan[t]),
                "score": ah_posts[t] + tg_posts[t]} for t in allt), key=lambda r: (-r["ah_accounts"] - len(tg_chan[r["ticker"]]), -r["score"]))
json.dump(rows, open(B/"reports/analysis/funnel_tickers.json","w"), indent=1)
L = ["# Tickers called out by flagged funnel accounts", "",
     f"Sources: {sum(ah_posts.values())} AfterHour ticker mentions, {sum(tg_posts.values())} cashtag mentions in archived public Telegram posts.",
     "Ranked by breadth (distinct accounts + distinct channels), then volume. Calls are promo copy, not recommendations.", "",
     "| Ticker | AH accounts | AH posts | TG channels | TG posts |", "|---|---:|---:|---:|---:|"]
L += [f"| ${r['ticker']} | {r['ah_accounts']} | {r['ah_posts']} | {r['tg_channels']} | {r['tg_posts']} |" for r in rows[:40]]
(B/"reports/analysis/funnel_tickers.md").write_text("\n".join(L)+"\n"); print("\n".join(L[:34]))
