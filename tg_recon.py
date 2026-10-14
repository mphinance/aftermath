#!/usr/bin/env python3
"""
tg_recon.py: passive, no-login, no-join recon of the Telegram links in accounts.json.

Only fetches the public web previews Telegram itself serves to anyone:
  https://t.me/<handle>     title, description, member count, type
  https://t.me/+<hash>      same, for private invite links (no joining)
  https://t.me/s/<handle>   recent public posts (public channels with web preview on)
Never joins, never posts, never uses an account. Serial, polite delay.

Extracts operator fingerprints (wallets, payment handles, prices, outbound t.me links,
@mentions, emails) and clusters channels that share description copy or fingerprints.

  python3 tg_recon.py --known accounts.json --out data/telegram_funnel/recon.json
"""
import argparse, collections as C, hashlib, html, json, re, sys, time, urllib.error, urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) tg_recon/1.0 (passive research)"
FP = {
    "eth": re.compile(r"\b0x[a-fA-F0-9]{40}\b"),
    "btc": re.compile(r"\b(?:bc1[a-z0-9]{25,60}|[13][a-km-zA-HJ-NP-Z1-9]{25,34})\b"),
    "tron": re.compile(r"\bT[1-9A-HJ-NP-Za-km-z]{33}\b"),
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "cashapp": re.compile(r"(?<![\w$])\$[A-Za-z][A-Za-z0-9_]{2,19}\b(?!\s*(?:calls?|puts?))"),
    "paypal": re.compile(r"paypal\.me/[\w.-]+", re.I),
    "price": re.compile(r"\$\s?\d{2,5}(?:\.\d\d)?\s*(?:/|per|a)?\s*(?:mo|month|week|wk|lifetime|year)?", re.I),
}
TME = re.compile(r"(?:https?://)?(?:t\.me|telegram\.me)/(?!s/)(\+?[A-Za-z0-9_\-]{4,})", re.I)
MENTION = re.compile(r"(?<![\w/])@([A-Za-z][A-Za-z0-9_]{4,31})")
URL = re.compile(r"https?://[^\s<>\"']+", re.I)


def fetch(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(15 * (i + 1)); continue
            if e.code in (404, 403):
                return None
            if i == tries - 1:
                return None
        except Exception:
            if i == tries - 1:
                return None
        time.sleep(2 ** i)
    return None


def meta(h, prop):
    m = re.search(rf'<meta property="{prop}" content="(.*?)"\s*/?>', h, re.S)
    return html.unescape(m.group(1)).strip() if m else None


def strip(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def preview(handle):
    h = fetch(f"https://t.me/{handle}")
    if not h:
        return None
    title = strip(re.search(r'tgme_page_title[^>]*>(.*?)</div>', h, re.S).group(1)) if 'tgme_page_title' in h else meta(h, "og:title")
    extra = re.search(r'tgme_page_extra[^>]*>(.*?)</div>', h, re.S)
    extra = strip(extra.group(1)) if extra else ""
    n = re.search(r"([\d\s,.]+)\s*(subscribers?|members?)", extra)
    desc = re.search(r'tgme_page_description[^>]*>(.*?)</div>', h, re.S)
    kind = "channel" if n and "subscriber" in n.group(2) else "group" if n else ("user_or_bot" if "tgme_page_context_link" in h or "Send Message" in h else "unknown")
    return {"title": title, "description": strip(desc.group(1)) if desc else meta(h, "og:description"),
            "members": int(re.sub(r"\D", "", n.group(1))) if n and re.sub(r"\D", "", n.group(1)) else None,
            "kind": kind, "extra": extra}


def posts(handle):
    h = fetch(f"https://t.me/s/{handle}")
    if not h or "tgme_widget_message" not in h:
        return []
    out = []
    for blk in re.split(r'(?=<div class="tgme_widget_message_wrap)', h)[1:]:
        t = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', blk, re.S)
        d = re.search(r'<time[^>]*datetime="([^"]+)"', blk)
        v = re.search(r'tgme_widget_message_views">([^<]+)<', blk)
        pid = re.search(r'data-post="([^"]+)"', blk)
        out.append({"id": pid.group(1) if pid else None, "date": d.group(1) if d else None,
                    "views": v.group(1) if v else None, "text": strip(t.group(1)) if t else ""})
    return out


def fingerprints(text, own):
    f = {k: sorted(set(rx.findall(text))) for k, rx in FP.items()}
    f["cashapp"] = [c for c in f["cashapp"] if not re.fullmatch(r"\$[A-Z]{1,5}", c)]  # drop stock tickers
    f["price"] = sorted({p.strip() for p in f["price"] if p.strip() not in ("$",)})[:12]
    f["tme"] = sorted({"t.me/" + m.lower() for m in TME.findall(text)} - {own})
    f["mentions"] = sorted({m.lower() for m in MENTION.findall(text)})
    f["urls"] = sorted({u.rstrip(".,)") for u in URL.findall(text) if "t.me/s/" not in u})[:15]
    return {k: v for k, v in f.items() if v}


def is_alive(pv):
    """Telegram serves a generic 'invited to a group chat' page for invalid/revoked invites."""
    if not pv or not pv.get("title"):
        return False
    return not (pv["title"].startswith("Join group chat") and pv.get("members") is None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--known", default="accounts.json")
    ap.add_argument("--out", default="data/telegram_funnel/recon.json")
    ap.add_argument("--delay", type=float, default=1.5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--reanalyze", action="store_true", help="re-run filters/clustering on existing --out, no network")
    a = ap.parse_args()
    accts = json.load(open(a.known))
    by_link, orig = C.defaultdict(list), {}
    for x in accts:
        for l, raw in zip(x.get("telegram_links_norm", []), x.get("telegram_links", [])):
            by_link[l].append(x["username"])
            orig.setdefault(l, raw)  # invite hashes are case-sensitive, keep the original
    links = sorted(by_link)[: a.limit or None]
    res = []
    if a.reanalyze:
        res = json.load(open(a.out))["channels"]
        for r in res:
            r["alive"] = is_alive(r["preview"])
            r["fingerprints"]["cashapp"] = [c for c in r["fingerprints"].get("cashapp", []) if not re.fullmatch(r"\$[A-Z]{1,5}", c)]
            if not r["fingerprints"]["cashapp"]:
                r["fingerprints"].pop("cashapp")
        links = []
    for i, link in enumerate(links, 1):
        handle = re.split(r"(?:t\.me|telegram\.me)/", orig.get(link, link), flags=re.I)[-1].split("?")[0].strip("/")
        pv = preview(handle); time.sleep(a.delay)
        ps = [] if handle.startswith("+") else posts(handle)
        if not handle.startswith("+"):
            time.sleep(a.delay)
        text = " ".join([(pv or {}).get("description") or ""] + [p["text"] for p in ps])
        row = {"link": link, "afterhour_accounts": by_link[link], "alive": is_alive(pv),
               "preview": pv, "public_posts_seen": len(ps), "fingerprints": fingerprints(text, link),
               "recent_posts": ps}
        res.append(row)
        print(f"[{i}/{len(links)}] {link}: {(pv or {}).get('title')!r} members={(pv or {}).get('members')} posts={len(ps)}", file=sys.stderr, flush=True)

    # clustering: same description copy, same fingerprint value
    def norm(s): return re.sub(r"\W+", " ", (s or "").lower()).strip()
    desc_groups = C.defaultdict(list)
    fp_groups = C.defaultdict(list)
    for r in res:
        if not r["alive"]:
            continue
        d = norm((r["preview"] or {}).get("description"))
        if len(d) > 25:
            desc_groups[hashlib.md5(d.encode()).hexdigest()].append(r["link"])
        for k, vals in r["fingerprints"].items():
            if k in ("price", "urls"):
                continue
            for v in vals:
                fp_groups[(k, v)].append(r["link"])
    summary = {
        "channels": len(res), "alive": sum(r["alive"] for r in res),
        "public_with_posts": sum(1 for r in res if r["public_posts_seen"]),
        "identical_descriptions": [{"description": (next(r for r in res if r["link"] == g[0])["preview"] or {}).get("description"), "links": g} for g in desc_groups.values() if len(g) > 1],
        "shared_fingerprints": [{"type": k, "value": v, "links": sorted(set(g))} for (k, v), g in fp_groups.items() if len(set(g)) > 1],
        "cross_promoted_unknown_channels": sorted({t for r in res for t in r["fingerprints"].get("tme", []) if t not in by_link})[:100],
    }
    json.dump({"summary": summary, "channels": res}, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in summary.items()}, indent=1))


if __name__ == "__main__":
    main()
