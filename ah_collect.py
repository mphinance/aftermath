#!/usr/bin/env python3
"""
ah_collect.py: archive the public AfterHour post stream and publish sentiment aggregates.

Public, unauthenticated GETs only (never posts, reacts, follows or sends auth headers).

  python3 ah_collect.py                  # one run: pull new posts, archive, publish
  python3 ah_collect.py --no-fetch       # republish from the archive
  python3 ah_collect.py --pages 5        # max feed pages per run (20 posts each)

Archive: data/ah_archive/posts.jsonl (gitignored, grows ~5-10MB/day).
Publishes (atomically, to $PUBLISH_DIR when set, else api/):
  api/sentiment.json   per-ticker aggregates for 24h / 72h / 7d, buzz baseline, daily series
  api/ah-posts.json    the most recent parsed posts (for get_ticker_posts)
"""
import argparse, json, os, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

import afterhour
import ah_sentiment as S

BASE = Path(__file__).resolve().parent
ARCH_DIR = BASE / "data" / "ah_archive"
ARCH = ARCH_DIR / "posts.jsonl"
API = BASE / "api"
FEED = "https://api.afterhour.com/social/feed"
PAGE = 20
RETAIN_DAYS = 30
WINDOWS = {"24h": 24, "72h": 72, "7d": 168}


def load_archive():
    posts, ids = [], set()
    if ARCH.exists():
        for line in ARCH.read_text(encoding="utf-8").splitlines():
            try:
                p = json.loads(line)
            except Exception:
                continue
            if p.get("id") not in ids:
                ids.add(p["id"])
                posts.append(p)
    return posts, ids


def pull_new(known, max_pages):
    """Walk newest-first until a full page is already known; return new parsed posts."""
    new, cursor, stale_pages = [], 0, 0
    for _ in range(max_pages):
        url = f"{FEED}?contentTypes=post&sortMethod=newest&take={PAGE}&cursor={cursor}"
        try:
            d = afterhour._get(url, retries=4, timeout=30)
        except Exception as e:
            print(f"[ah_collect] feed page failed ({e}); stopping this run", file=sys.stderr)
            break
        items = d.get("items", []) if isinstance(d, dict) else []
        if not items:
            break
        fresh = 0
        for it in items:
            p = S.parse_item(it)
            if p and p["id"] not in known:
                known.add(p["id"])
                new.append(p)
                fresh += 1
        stale_pages = stale_pages + 1 if fresh == 0 else 0
        if stale_pages >= 1:
            break
        cursor = d.get("cursor") or cursor + PAGE
        time.sleep(1.0)
    return new


def flagged_usernames():
    try:
        return {a["username"].lower() for a in json.load(open(BASE / "accounts.json")) if a.get("username")}
    except Exception:
        return set()


def atomic_write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"))
    os.replace(tmp, path)


def publish(posts, now):
    flagged = flagged_usernames()
    ts = [S._ts(p) for p in posts if S._ts(p)]
    out = {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://api.afterhour.com/social/feed (public posts)",
        "archive": {"posts": len(posts), "oldest": min(ts).isoformat() if ts else None,
                    "newest": max(ts).isoformat() if ts else None},
        "method": ("Direction only from explicit contract side (CALL/PUT, 765C) plus an open verb; closes, hindsight "
                   "and modal language are neutral. One vote per author per ticker per UTC day; identical titles "
                   "count once. Roughly a quarter of posts carry parseable direction."),
        "caveat": "Small, noisy sample of public posts. Not advice. Check flags before trusting a score.",
        "windows": {name: S.aggregate(posts, now, h, flagged) for name, h in WINDOWS.items()},
        "buzz": {name: S.buzz(posts, now, h) for name, h in (("24h", 24), ("72h", 72))},
        "daily": S.daily_series(posts, now, 14),
    }
    recent = sorted(posts, key=lambda p: p["ts"] or "", reverse=True)[:400]
    outdir = Path(os.environ["PUBLISH_DIR"]) if os.environ.get("PUBLISH_DIR") and Path(os.environ["PUBLISH_DIR"]).is_dir() else API
    atomic_write(outdir / "sentiment.json", out)
    atomic_write(outdir / "ah-posts.json", {"generated_at": out["generated_at"], "posts": recent})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--pages", type=int, default=5)
    a = ap.parse_args()
    now = datetime.now(timezone.utc)
    posts, ids = load_archive()
    added = 0
    if not a.no_fetch:
        new = pull_new(ids, a.pages)
        if new:
            ARCH_DIR.mkdir(parents=True, exist_ok=True)
            with open(ARCH, "a", encoding="utf-8") as f:
                for p in new:
                    f.write(json.dumps(p, separators=(",", ":")) + "\n")
            posts.extend(new)
            added = len(new)
    cut = now.timestamp() - RETAIN_DAYS * 86400
    posts = [p for p in posts if (S._ts(p) or now).timestamp() >= cut]
    out = publish(posts, now)
    print(f"[ah_collect] +{added} new, archive {len(posts)}, tickers(24h) {len(out['windows']['24h'])}")


if __name__ == "__main__":
    main()
