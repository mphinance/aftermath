"""
ah_sentiment.py: deterministic retail-sentiment scoring for public AfterHour posts.

Pure functions, no I/O. The collector (ah_collect.py) feeds feed items in and
publishes the aggregates to api/sentiment.json for the MCP tools.

Method (kept deliberately conservative; every output carries its sample size):
  * Direction comes only from explicit contract side (CALL/PUT, "765C", "40P") plus an
    open/close verb. A plain ticker mention is neutral. Closing a position is not a vote.
  * Hindsight and modal language ("should've", "might", "watching") is neutral.
  * One vote per author per ticker per UTC day (latest wins); identical normalized
    titles collapse to one vote across authors (copy-paste spam).
  * Roughly a quarter of posts carry parseable direction. Confidence is a function of
    distinct voting authors, never of post count.
"""
from __future__ import annotations

import hashlib
import math
import re
from collections import defaultdict
from datetime import datetime, timedelta

ALIASES = {"SPXW": "SPX"}

CASHTAG = re.compile(r"(?<![\w$])\$([A-Za-z]{1,5})\b")
SIDE_WORD = re.compile(r"\b(CALLS?|PUTS?)\b", re.I)
SIDE_SUFFIX = re.compile(r"(?<![\w.])\d{1,5}(?:\.\d+)?\s?([CP])\b(?!\w)")
OPEN_RE = re.compile(r"\b(?:open(?:ed|ing)?\b(?!\s*:)|entry|buy|bought|bto|adding|added|new trade|alert|locked in|loaded|grabbed|back in|in\s+(?:on|with))", re.I)
CLOSE_RE = re.compile(r"\b(?:closed|closing|exit(?:ed)?|sold|sell(?:ing)?|stc|trim(?:med|ming)?|took profits?|tak(?:e|ing|en) profits?|profits?|stopped(?: out)?|all out|cut|covered|banked|locked)\b", re.I)
MODAL = re.compile(r"\b(?:might|maybe|may|if|could|should|plan(?:ning)? to|looking (?:to|for)|will|going to|want to|wanna|watch(?:ing|list)?|ideas?)\b", re.I)
HINDSIGHT = re.compile(r"should(?:'|’)?ve|could(?:'|’)?ve|would(?:'|’)?ve|would have|if anyone|had you|missed", re.I)
PRICE_AT = re.compile(r"@\s*\$?\.?\d|(?:CALLS?|PUTS?|\d[CP])\b[^\n]{0,24}?\bentry\b[^\n]{0,6}\d|\b(?:CALLS?|PUTS?)\s+\$\d*\.?\d", re.I)

CONFIDENCE = ((30, "high"), (10, "medium"), (0, "low"))


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9$@. ]+", "", (t or "").lower()).strip()[:160]


def title_hash(t: str) -> str:
    return hashlib.sha1(norm_title(t).encode()).hexdigest()[:12]


def tickers_for(title: str, securities: list) -> list:
    out = []
    for s in securities or []:
        s = (s or "").upper()
        s = ALIASES.get(s, s)
        if s and s not in out:
            out.append(s)
    for m in CASHTAG.finditer(title or ""):
        s = ALIASES.get(m.group(1).upper(), m.group(1).upper())
        if s not in out and len(out) < 6:
            out.append(s)
    return out


def classify(title: str) -> dict:
    """Return {side, action, stance, basis}. stance in bull|bear|neutral."""
    t = title or ""
    side = None
    m = SIDE_WORD.search(t)
    if m:
        side = "call" if m.group(1).upper().startswith("C") else "put"
    else:
        m = SIDE_SUFFIX.search(t)
        if m:
            side = "call" if m.group(1).upper() == "C" else "put"
    if side is None:
        return {"side": None, "action": None, "stance": "neutral", "basis": "no_contract"}
    if HINDSIGHT.search(t):
        return {"side": side, "action": "hindsight", "stance": "neutral", "basis": "hindsight"}
    if MODAL.search(t) and not OPEN_RE.search(t):
        return {"side": side, "action": "watch", "stance": "neutral", "basis": "modal"}
    mo, mc = OPEN_RE.search(t), CLOSE_RE.search(t)
    # the first verb wins: "Closed 10 SPX 7710P (Entry: 8.00)" is a close, "Opened ... Gain" an open
    if mc and (not mo or mc.start() < mo.start()):
        return {"side": side, "action": "close", "stance": "neutral", "basis": "close_not_a_vote"}
    if mo or PRICE_AT.search(t):
        return {"side": side, "action": "open", "stance": "bull" if side == "call" else "bear",
                "basis": "open_verb" if mo else "alert_with_price"}
    return {"side": side, "action": "mention", "stance": "neutral", "basis": "side_only"}


def parse_item(item: dict) -> dict | None:
    """Reduce a /social/feed item to the compact record we archive."""
    post = item.get("post") or {}
    author = item.get("author") or post.get("author") or {}
    pid = post.get("id") or item.get("sourceId")
    if not pid:
        return None
    title = post.get("title") or ""
    secs = [s.get("tickerSymbol") for s in (item.get("securities") or []) if s.get("tickerSymbol")]
    share = post.get("shareUrl") or ""
    parts = [p for p in share.split("/") if p]
    h = parts[3] if len(parts) >= 4 and "afterhour.com" in parts[1] else None
    c = classify(title)
    return {
        "id": pid,
        "hash": h,
        "ts": post.get("createdAt") or item.get("createdAt"),
        "author": author.get("username"),
        "followers": author.get("numFollowers", 0),
        "privacy": author.get("financialDataPrivacyMode"),
        "bio_link": (author.get("linkInBio") or "")[:120],
        "title": title[:300],
        "topic": item.get("primaryTopicKey"),
        "tickers": tickers_for(title, secs),
        "views": post.get("viewCount", 0),
        "comments": item.get("commentCount", 0),
        "likes": (item.get("reactionCounts") or {}).get("thumbsUp", 0),
        "has_positions": bool(post.get("positionSnapshots")),
        "sig": title_hash(title),
        "side": c["side"], "action": c["action"], "stance": c["stance"], "basis": c["basis"],
    }


def _ts(p):
    try:
        return datetime.fromisoformat(p["ts"].replace("Z", "+00:00"))
    except Exception:
        return None


def _confidence(n_authors: int) -> str:
    return next(label for floor, label in CONFIDENCE if n_authors >= floor)


def aggregate(posts: list, now: datetime, hours: int, flagged: set | None = None) -> dict:
    """Per-ticker aggregates over the trailing window. flagged = lowercase usernames on the funnel list."""
    flagged = flagged or set()
    cut = now - timedelta(hours=hours)
    win = [p for p in posts if (_ts(p) or cut) >= cut]
    # copy-paste spam: identical normalized title text from different authors counts once
    sig_authors = defaultdict(set)
    for p in win:
        sig_authors[p["sig"]].add(p["author"])
    spam_sigs = {s for s, a in sig_authors.items() if len(a) >= 3}

    by = defaultdict(list)
    for p in win:
        for t in p["tickers"]:
            by[t].append(p)

    out = {}
    for t, ps in by.items():
        votes = {}  # (author, utc_day) -> post, latest wins
        seen_sigs = set()
        for p in sorted(ps, key=lambda x: x["ts"] or ""):
            if p["stance"] == "neutral":
                continue
            if p["sig"] in seen_sigs:
                continue
            seen_sigs.add(p["sig"])
            votes[(p["author"], (p["ts"] or "")[:10])] = p
        bull = sum(1 for p in votes.values() if p["stance"] == "bull")
        bear = sum(1 for p in votes.values() if p["stance"] == "bear")
        voters = {p["author"] for p in votes.values()}
        authors = {p["author"] for p in ps}
        n_dir = bull + bear
        calls = sum(1 for p in ps if p["action"] == "open" and p["side"] == "call")
        puts = sum(1 for p in ps if p["action"] == "open" and p["side"] == "put")
        topics = defaultdict(int)
        for p in ps:
            if p["topic"]:
                topics[p["topic"]] += 1
        flagged_hit = sorted({a for a in authors if a and a.lower() in flagged})
        funnel_link = sorted({p["author"] for p in ps if "t.me" in (p["bio_link"] or "").lower() and p["author"]})
        low_fol = sum(1 for a in authors if a) and sum(
            1 for a in {(p["author"], p["followers"]) for p in ps} if (a[1] or 0) < 35)
        top = sorted(ps, key=lambda p: (p["views"] or 0) + 5 * (p["comments"] or 0), reverse=True)[:5]
        out[t] = {
            "n_posts": len(ps), "n_authors": len(authors),
            "n_directional_votes": n_dir, "n_voting_authors": len(voters),
            "bull": bull, "bear": bear, "neutral_posts": len(ps) - n_dir,
            "net_score": round((bull - bear) / n_dir, 3) if n_dir else None,
            "confidence": _confidence(len(voters)),
            "calls_opened": calls, "puts_opened": puts,
            "call_put_ratio": round(calls / puts, 2) if puts else None,
            "by_topic": dict(topics),
            "views": sum(p["views"] or 0 for p in ps),
            "comments": sum(p["comments"] or 0 for p in ps),
            "flags": {
                "duplicate_text_posts": sum(1 for p in ps if p["sig"] in spam_sigs),
                "low_follower_author_share": round(low_fol / max(1, len(authors)), 2),
                "bio_telegram_authors": funnel_link[:10],
                "funnel_list_authors": flagged_hit[:10],
            },
            "top_posts": [{"id": p["id"], "hash": p["hash"], "author": p["author"], "followers": p["followers"],
                           "title": p["title"][:140], "stance": p["stance"], "topic": p["topic"], "ts": p["ts"]}
                          for p in top],
        }
    return out


def buzz(posts: list, now: datetime, hours: int, baseline_days: int = 7) -> dict:
    """Mentions in the window versus the trailing per-window baseline. z is None until the archive is deep enough."""
    cut = now - timedelta(hours=hours)
    base_cut = now - timedelta(days=baseline_days)
    cur, base = defaultdict(int), defaultdict(int)
    span = None
    for p in posts:
        t = _ts(p)
        if not t:
            continue
        span = t if span is None or t < span else span
        for tk in p["tickers"]:
            if t >= cut:
                cur[tk] += 1
            elif t >= base_cut:
                base[tk] += 1
    depth_days = (now - span).total_seconds() / 86400 if span else 0
    windows = max(1.0, (baseline_days * 24 - hours) / hours)
    res = {}
    for tk, n in cur.items():
        mean = base.get(tk, 0) / windows
        z = None
        if depth_days >= 3:
            sd = math.sqrt(max(mean, 1.0))  # Poisson-ish
            z = round((n - mean) / sd, 2)
        res[tk] = {"mentions": n, "baseline_mean": round(mean, 2), "z": z}
    return {"archive_depth_days": round(depth_days, 1), "tickers": res}


def daily_series(posts: list, now: datetime, days: int = 14) -> dict:
    cut = now - timedelta(days=days)
    acc = defaultdict(lambda: defaultdict(lambda: {"posts": 0, "bull": 0, "bear": 0}))
    seen = set()
    for p in sorted(posts, key=lambda x: x["ts"] or ""):
        t = _ts(p)
        if not t or t < cut:
            continue
        day = p["ts"][:10]
        for tk in p["tickers"]:
            d = acc[tk][day]
            d["posts"] += 1
            if p["stance"] != "neutral":
                key = (tk, day, p["author"])
                if key in seen or p["sig"] in seen:
                    continue
                seen.add(key)
                d["bull" if p["stance"] == "bull" else "bear"] += 1
    return {tk: [{"date": d, **v, "net": round((v["bull"] - v["bear"]) / (v["bull"] + v["bear"]), 2) if v["bull"] + v["bear"] else None}
                 for d, v in sorted(days_.items())] for tk, days_ in acc.items()}
