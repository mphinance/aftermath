#!/usr/bin/env python3
"""
crawl.py: find AfterHour accounts funneling to Telegram that aren't in your accounts.json yet.

Zero dependencies (Python 3.9+). Read-only: only GETs public AfterHour endpoints,
never posts, follows, or touches Telegram. Serial requests with a delay.

  python3 crawl.py --known accounts.json --pages 200 --out candidates.json

Output rows use the same schema as accounts.json minus listing_id/tier, plus
`evidence` (the post that exposed it) and `shares_link_with` (known accounts on
the same normalized link: the strongest signal, since operators reuse invite links).
"""
import argparse, json, re, sys, time, urllib.request, urllib.error
from datetime import date

FEED = "https://api.afterhour.com/social/feed"
UA = "Mozilla/5.0 (crawl.py; read-only research)"
TME = re.compile(r"(?:https?://)?(?:www\.)?(?:t\.me|telegram\.me)/(\+?[A-Za-z0-9_\-]{4,})", re.I)
HYPE = re.compile(r"free (alerts?|signals?|channel|group|community)|tap in|join (us|the|my|our)|vip|"
                  r"telegram|inbox|dm me", re.I)


def get(url, retries=5, timeout=60):
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout) as r:
                body = r.read().decode("utf-8", "replace")
                return json.loads(body) if r.headers.get("content-type", "").startswith("application/json") else body
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == retries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if i == retries - 1:
                raise
        time.sleep(min(1.5 * 2 ** i, 12))


def norm(link):
    m = TME.search(link or "")
    return "t.me/" + m.group(1).lower() if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--known", default="accounts.json")
    ap.add_argument("--pages", type=int, default=200, help="feed pages to sweep")
    ap.add_argument("--take", type=int, default=50)
    ap.add_argument("--delay", type=float, default=0.4)
    ap.add_argument("--out", default="candidates.json")
    a = ap.parse_args()

    known = json.load(open(a.known))
    known_names = {k["username"].lower() for k in known}
    by_link = {}
    for k in known:
        for l in k.get("telegram_links_norm", []):
            by_link.setdefault(l, []).append(k["username"])

    seen, cand, cursor = set(), {}, None
    for page in range(a.pages):
        url = f"{FEED}?take={a.take}&contentTypes=post" + (f"&cursor={cursor}" if cursor else "")
        try:
            d = get(url)
        except Exception as e:
            print(f"page {page}: {e}", file=sys.stderr)
            break
        items = d.get("items", [])
        if not items:
            break
        for it in items:
            au, post = it.get("author") or {}, it.get("post") or {}
            name = au.get("username")
            if not name or name.lower() in known_names:
                continue
            seen.add(name)
            text = " ".join(str(x) for x in (post.get("title"), post.get("body")) if x)
            bio = au.get("bio") or ""
            in_bio, in_post = TME.search(bio), TME.search(text) or ("telegram" in text.lower() and HYPE.search(text))
            if not (in_bio or in_post):
                continue
            c = cand.setdefault(name, {"au": au, "ev": []})
            if in_post and len(c["ev"]) < 3:
                c["ev"].append({"post": post.get("shareUrl"), "text": text[:200]})
        cursor = d.get("cursor")
        print(f"page {page + 1}: {len(seen)} new authors scanned, {len(cand)} candidates", file=sys.stderr)
        if not cursor:
            break
        time.sleep(a.delay)

    out = []
    for name, c in cand.items():
        au = c["au"]
        text = (au.get("bio") or "") + " " + " ".join(e["text"] for e in c["ev"])
        links = sorted({norm(m.group(0)) for m in TME.finditer(text)} - {None})
        out.append({
            "username": name, "profile_id": au.get("id"), "bio": au.get("bio"),
            "telegram_links_norm": links, "telegram_links": ["https://" + l for l in links],
            "telegram_handles": [l.split("/", 1)[1] for l in links],
            "created_at": (au.get("createdAt") or "")[:10] or None, "num_followers": au.get("numFollowers"),
            "platform": "afterhour", "destination_platform": "telegram",
            "source": f"crawl.py {date.today()}", "evidence": c["ev"],
            "shares_link_with": sorted({u for l in links for u in by_link.get(l, [])}),
        })
    out.sort(key=lambda r: (not r["shares_link_with"], not r["telegram_links_norm"], r["num_followers"] or 0))
    json.dump(out, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{len(out)} candidates -> {a.out} ({sum(1 for r in out if r['shares_link_with'])} share a known link)")


if __name__ == "__main__":
    main()
