#!/usr/bin/env python3
"""Render data/telegram_funnel/recon.json + accounts.json into reports/analysis/funnel_recon.html
(bento-style infographic). PNG: screenshot the html at 1200px wide, 2x scale."""
import json, html, collections as C
from pathlib import Path
B = Path(__file__).resolve().parent
R = json.load(open(B/"data/telegram_funnel/recon.json")); acc = {a["username"]: a for a in json.load(open(B/"accounts.json"))}
ch, S = R["channels"], R["summary"]
for c in ch:
    c["afterhour_accounts"] = list(dict.fromkeys(c["afterhour_accounts"]))
e = lambda s: html.escape(str(s if s is not None else ""))
mem = lambda c: (c["preview"] or {}).get("members") or 0
live = [c for c in ch if c["alive"]]
sized = [c for c in live if mem(c)]
dead = [c for c in ch if not c["alive"]]
total = sum(mem(c) for c in sized)
rank = {"verified": 3, "corroborated": 2, "reported": 1}
tier = lambda c: max((acc[u]["tier"] for u in c["afterhour_accounts"] if u in acc), key=lambda t: rank[t])
title = lambda c: (c["preview"] or {}).get("title") or c["link"]
top = sorted(sized, key=mem, reverse=True)[:10]
mx = mem(top[0]) if top else 1
bars = "".join(f'<div class="bar"><div class="bl"><b>{e(title(c))}</b><span>{len(c["afterhour_accounts"])} account{"s" if len(c["afterhour_accounts"])>1 else ""}</span></div><div class="track"><div class="fill {tier(c)}" style="width:{max(3,mem(c)/mx*100):.1f}%"></div></div><div class="bn">{mem(c):,}</div></div>' for c in top)
multi = sorted([c for c in live if len(c["afterhour_accounts"]) > 1], key=lambda c: (-len(c["afterhour_accounts"]), -mem(c)))
fronts = "".join(f'<div class="front"><div class="fh"><b>{e(title(c))}</b><span>{mem(c):,}</span></div><div class="chips">{"".join(f"<i>@{e(u)}</i>" for u in c["afterhour_accounts"])}</div></div>' for c in multi[:7])
bk = C.Counter("10k+" if mem(c) >= 10000 else "5k to 10k" if mem(c) >= 5000 else "1k to 5k" if mem(c) >= 1000 else "under 1k" for c in sized)
order = ["10k+", "5k to 10k", "1k to 5k", "under 1k"]
bmx = max(bk.values()) if bk else 1
buckets = "".join(f'<div class="bk"><span>{k}</span><div class="bt"><div style="width:{bk.get(k,0)/bmx*100:.0f}%"></div></div><b>{bk.get(k,0)}</b></div>' for k in order)
pct = len(live) / len(ch) * 100 if ch else 0
ident = S["identical_descriptions"]
twins = "".join(f'<div class="twin"><q>{e((g["description"] or "").replace(chr(10)," / ")[:120])}</q><span>{" &middot; ".join(e(l) for l in g["links"])}</span></div>' for g in ident[:3])
fps = S["shared_fingerprints"]
fpt = "".join(f'<div class="twin"><b>{e(g["type"])}:</b> <code>{e(g["value"])}</code><span>{" &middot; ".join(e(l) for l in g["links"])}</span></div>' for g in fps[:3])
pub = sum(1 for c in ch if c["public_posts_seen"])
big = top[0] if top else None
doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
:root{{--bg:#07090e;--card:#0f141c;--s:#161e2a;--bd:#222c3a;--g:#00f59b;--c:#00d2ff;--y:#ffd166;--r:#ff5c7a;--t:#e8eef5;--m:#8b98a8}}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;background:radial-gradient(circle at 15% 0%,#0d1a2a,var(--bg) 45%);color:var(--t);font-family:'Plus Jakarta Sans',sans-serif;padding:40px}}
.hd{{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:22px}}h1{{font-size:44px;font-weight:800;letter-spacing:-1.5px;line-height:1}}h1 span{{color:var(--g)}}
.sub{{color:var(--m);font-size:14.5px;margin-top:10px;max-width:640px}}.tag{{font:500 12px 'JetBrains Mono';color:var(--m);text-align:right;line-height:1.6}}
.grid{{display:grid;grid-template-columns:repeat(12,1fr);gap:14px}}.t{{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:22px;overflow:hidden}}
.t h2{{font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;color:var(--c);margin-bottom:14px;font-weight:600}}
.hero{{grid-column:span 5;background:linear-gradient(135deg,#112a23,#0f141c 70%);border-color:#1d4a3b}}.hero b{{display:block;font:700 76px/1 'JetBrains Mono';color:var(--g);letter-spacing:-3px}}.hero p{{color:var(--m);margin-top:10px;font-size:15px}}.hero p em{{color:var(--t);font-style:normal;font-weight:600}}
.donut{{grid-column:span 3;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}.ring{{width:150px;height:150px;border-radius:50%;background:conic-gradient(var(--c) {pct:.1f}%,var(--r) 0);display:grid;place-items:center}}.ring div{{width:104px;height:104px;border-radius:50%;background:var(--card);display:grid;place-items:center;font:700 30px 'JetBrains Mono'}}.donut p{{font-size:12.5px;color:var(--m);margin-top:12px}}.donut p b{{color:var(--r)}}
.stat{{grid-column:span 2;display:flex;flex-direction:column;justify-content:space-between}}.stat b{{font:700 44px 'JetBrains Mono';color:var(--y)}}.stat span{{font-size:12.5px;color:var(--m)}}
.top{{grid-column:span 7}}.bar{{display:grid;grid-template-columns:250px 1fr 74px;gap:12px;align-items:center;margin:8px 0}}.bl b{{display:block;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.bl span{{font-size:11px;color:var(--m)}}
.track{{background:var(--s);border-radius:8px;height:14px}}.fill{{height:100%;border-radius:8px;background:var(--c)}}.fill.verified{{background:var(--r)}}.fill.corroborated{{background:var(--y)}}.bn{{font:700 13px 'JetBrains Mono';text-align:right}}
.leg{{font-size:11px;color:var(--m);margin-top:8px}}.leg i{{font-style:normal;margin-right:12px}}.leg i:before{{content:"";display:inline-block;width:9px;height:9px;border-radius:3px;margin-right:5px;background:var(--c)}}.leg .v:before{{background:var(--r)}}.leg .cr:before{{background:var(--y)}}
.size{{grid-column:span 5}}.bk{{display:grid;grid-template-columns:90px 1fr 34px;gap:10px;align-items:center;margin:12px 0;font-size:13px}}.bk span{{color:var(--m)}}.bt{{background:var(--s);height:22px;border-radius:6px}}.bt div{{height:100%;background:linear-gradient(90deg,var(--g),var(--c));border-radius:6px}}.bk b{{font:700 15px 'JetBrains Mono';text-align:right}}
.fr{{grid-column:span 7}}.front{{background:var(--s);border-radius:10px;padding:11px 13px;margin-bottom:8px}}.fh{{display:flex;justify-content:space-between;font-size:13.5px}}.fh span{{font:700 13px 'JetBrains Mono';color:var(--y)}}.chips{{margin-top:6px;display:flex;flex-wrap:wrap;gap:5px}}.chips i{{font:500 11px 'JetBrains Mono';font-style:normal;background:#0b1118;border:1px solid var(--bd);padding:2px 7px;border-radius:99px;color:var(--c)}}
.cp{{grid-column:span 5}}.twin{{background:var(--s);border-radius:10px;padding:11px 13px;margin-bottom:8px;font-size:12px;color:var(--m);overflow-wrap:anywhere}}.twin q{{display:block;color:var(--t);font-size:12.5px;margin-bottom:5px}}.twin b{{color:var(--t)}}code{{font-family:'JetBrains Mono';color:var(--y)}}.twin span{{display:block;margin-top:4px;font:500 11px 'JetBrains Mono'}}
.note{{grid-column:span 12;display:flex;gap:30px;align-items:center;background:#1a1218;border-color:#4a2230}}.note b{{color:var(--r);font:700 38px 'JetBrains Mono'}}.note p{{font-size:13.5px;color:var(--m)}}.note p em{{color:var(--t);font-style:normal}}
.ft{{color:var(--m);font-size:11.5px;margin-top:18px;display:flex;justify-content:space-between}}
</style></head><body>
<div class="hd"><div><h1>Telegram Funnel <span>Recon</span></h1><div class="sub">Passive sweep of the public Telegram previews behind every flagged AfterHour account. No joins, no logins, no posts.</div></div><div class="tag">AfterMath &times; TelegramScammers.com<br>ah.mphinance.com/scamcheck</div></div>
<div class="grid">
<div class="t hero"><h2>Combined reach</h2><b>{total:,}</b><p><em>members</em> across {len(sized)} channels with a public count, all pushed by <em>{len(acc)} AfterHour accounts</em>. Biggest single funnel: <em>{e(title(big)) if big else ""}</em> at {mem(big):,}.</p></div>
<div class="t donut"><h2>Link health</h2><div class="ring"><div>{len(live)}</div></div><p>of {len(ch)} channels resolve.<br><b>{len(dead)}</b> invalid or truncated invites</p></div>
<div class="t stat"><h2>Public w/ posts</h2><b>{pub}</b><span>channels let us read recent posts without joining</span></div>
<div class="t stat"><h2>Shared by 2+</h2><b>{len(multi)}</b><span>channels fronted by multiple accounts</span></div>
<div class="t top"><h2>Biggest funnels by members</h2>{bars}<div class="leg"><i class="v">verified</i><i class="cr">corroborated</i><i>reported</i> strongest evidence tier on the AfterHour side</div></div>
<div class="t size"><h2>Channel size</h2>{buckets}<p class="leg" style="margin-top:14px">Member counts from Telegram's own public preview at time of run.</p></div>
<div class="t fr"><h2>One channel, many fronts</h2>{fronts}</div>
<div class="t cp"><h2>Copy-paste &amp; shared fingerprints</h2>{twins}{fpt}</div>
<div class="t note"><b>{len(dead)}</b><p><em>Dead or malformed invite links in the list</em> (e.g. truncated hashes like +SUS). They return Telegram's generic "invited to a group chat" page, so the listing's link needs a re-check before anyone relies on it.</p></div>
</div>
<div class="ft"><span>Flagged for investigation, not a finding of fraud.</span><span>Data: telegramscammers.com &middot; recon: AfterMath</span></div>
</body></html>'''
out = B/"reports/analysis/funnel_recon.html"; out.write_text(doc); print(out)
