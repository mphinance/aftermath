#!/usr/bin/env python3
"""Build api/trader-signals.json from data/traders/*/posts.json.

Extraction is deterministic keyword-plus-adjacent-number only: no model calls, no NLP, no
inference. Rules:
  * vol tokens: VIX VVIX VX VXM VXX UVXY SVIX UVIX MOVE COR1M SKEW (case-insensitive, whole
    letter-run match, so VXX/VXM never count as VX) and the phrases short/long vol(atility).
    MOVE is matched upper-case only, because lower-case "move" is an ordinary English word.
  * a post with at least one vol token is a vol_post; only vol posts become signals.
  * a level is a number within 12 chars of a symbol token, assigned to the NEAREST token, inside
    one sentence. Numbers followed by % are dropped (percent of what is ambiguous). Phrase
    tokens never get levels. Ambiguity is dropped, never guessed.
  * direction: short only from short/shorting/short it/sold/sell/fade, long only from
    long/bought/buy/long it, in a sentence that contains a vol token. Both or neither -> none.
  * quote: the first sentence containing a vol token, verbatim, at most 280 chars.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
TRADERS = BASE / "data" / "traders"
OUT = BASE / "api" / "trader-signals.json"

NEAR = 12
QUOTE_MAX = 280

PHRASES = ["short volatility", "long volatility", "short vol", "long vol"]
SYMBOLS = ["COR1M", "UVXY", "SVIX", "UVIX", "VVIX", "SKEW", "VXM", "VXX", "VIX", "VX"]
_LET = r"(?<![A-Za-z])"
_LET_END = r"(?![A-Za-z])"
TOKEN_RE = re.compile(
    "(?:" + _LET + "(?P<phrase>" + "|".join(p.replace(" ", r"\s+") for p in PHRASES) + ")" + _LET_END + ")"
    + "|(?:" + _LET + "(?P<sym>" + "|".join(SYMBOLS) + ")" + _LET_END + ")"
    + r"|(?:(?<![A-Za-z])(?P<move>MOVE)(?![A-Za-z]))",
    re.IGNORECASE,
)
# MOVE is case-sensitive: IGNORECASE above would also match it, so it is filtered after the match.
NUM_RE = re.compile(r"(?<![\d.])\d+(?:\.\d+)?(?![\d.]*\d)")
SENT_RE = re.compile(r"(?<=[.!?])\s+|\n+")
SHORT_RE = re.compile(r"\b(?:short(?:ing)?|short it|sold|sell|fade)\b", re.I)
LONG_RE = re.compile(r"\b(?:long|long it|bought|buy)\b", re.I)


def _tokens(text: str) -> list[dict]:
    out = []
    for m in TOKEN_RE.finditer(text):
        if m.group("phrase"):
            name, kind = re.sub(r"\s+", " ", m.group("phrase").lower()), "phrase"
        elif m.group("sym"):
            name, kind = m.group("sym").upper(), "sym"
        else:
            if m.group("move") != "MOVE":
                continue
            name, kind = "MOVE", "sym"
        out.append({"name": name, "kind": kind, "start": m.start(), "end": m.end()})
    return out


def _levels(sent: str, toks: list[dict]) -> list[dict]:
    syms = [t for t in toks if t["kind"] == "sym"]
    if not syms:
        return []
    levels, seen = [], set()
    for m in NUM_RE.finditer(sent):
        s, e = m.span()
        if any(t["start"] < e and s < t["end"] for t in toks):  # inside a token (COR1M)
            continue
        if sent[e:e + 1] == "%":
            continue
        best = None
        for t in toks:
            gap = t["start"] - e if t["start"] >= e else (s - t["end"] if s >= t["end"] else 0)
            if best is None or gap < best[0]:
                best = (gap, t)
        gap, t = best
        if gap > NEAR or t["kind"] != "sym":
            continue
        lo, hi = min(s, t["start"]), max(e, t["end"])
        if re.search(r"[.!?]\s", sent[lo:hi]):
            continue
        key = (t["name"], float(m.group()))
        if key in seen:
            continue
        seen.add(key)
        # context: the number, the gap and the token, e.g. "20-25VIX" for the range 20, 25
        # extend to a directly attached range partner ("20-25VIX" -> context covers both numbers)
        rng = re.search(r"\d+(?:\.\d+)?\s*[-–/]\s*\d+(?:\.\d+)?\s*" + re.escape(sent[t["start"]:t["end"]]), sent[max(0, lo - 14):hi + 1])
        context = sent[lo:hi]
        if rng and rng.group().strip() and m.group() in rng.group():
            context = rng.group().strip()
        levels.append({"token": t["name"], "value": float(m.group()), "context": context})
    return levels


def extract_signal(post: dict) -> dict | None:
    """Return a signal dict for a vol post, else None."""
    text = "\n".join(x for x in (post.get("title") or "", post.get("body") or "") if x)
    sents = [s for s in SENT_RE.split(text) if s and s.strip()]
    instruments, levels, quote = [], [], None
    shorts = longs = False
    for sent in sents:
        toks = _tokens(sent)
        if not toks:
            continue
        for t in toks:
            if t["name"] not in instruments:
                instruments.append(t["name"])
        for lv in _levels(sent, toks):
            if lv not in levels:
                levels.append(lv)
        shorts = shorts or bool(SHORT_RE.search(sent))
        longs = longs or bool(LONG_RE.search(sent))
        if quote is None:
            quote = sent.strip()[:QUOTE_MAX]
    if not instruments:
        return None
    direction = "short" if shorts and not longs else "long" if longs and not shorts else "none"
    return {
        "date": post.get("date") or (post.get("created_at") or "")[:10],
        "id": post.get("id"),
        "share_url": post.get("share_url", ""),
        "title": post.get("title", ""),
        "instruments": instruments,
        "direction": direction,
        "levels": levels,
        "quote": quote,
    }


def build_trader(data: dict) -> dict:
    posts = sorted(data.get("posts", []), key=lambda p: p.get("created_at") or "")
    signals = [s for s in (extract_signal(p) for p in posts) if s]
    dates = [p.get("date") for p in posts if p.get("date")]
    return {
        "handle": data.get("handle"),
        "profile_id": data.get("profile_id"),
        "post_count": len(posts),
        "first_post": dates[0] if dates else None,
        "last_post": dates[-1] if dates else None,
        "vol_post_count": len(signals),
        "signals": signals,
    }


def build(traders_dir: Path = TRADERS, out: Path = OUT) -> dict:
    traders = []
    for f in sorted(Path(traders_dir).glob("*/posts.json")):
        traders.append(build_trader(json.loads(f.read_text())))
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "traders": traders}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    p = build()
    for t in p["traders"]:
        print(f"{t['handle']}: {t['post_count']} posts, {t['vol_post_count']} vol posts")
    print(f"api/trader-signals.json: {len(p['traders'])} traders")
