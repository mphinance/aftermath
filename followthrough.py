#!/usr/bin/env python3
"""
Measure the missing exit post.

Nothing here touches the brokerage sync, the amount_k field, or any dollar figure.
It reads only what people typed: does a position someone announced buying ever get
a post saying they got out of it?

    python3 tools/followthrough.py
    python3 tools/followthrough.py --json out.json
"""
import argparse
import json
import os
import re
from glob import glob
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = str(BASE_DIR / "data" / "following")

ENTRY = re.compile(
    r"\b(bought|buying|added|adding|opened|scaled in|scaling in|loaded|entered|entering|"
    r"picked up|grabbed|starter|initiated|long(?:ed)?|in at|averaged down)\b", re.I
)
EXIT = re.compile(
    r"\b(sold|selling|closed|closing|took profit|taking profit|trimmed|trimming|exited|"
    r"exiting|out at|stopped out|stop(?:ped)? out|cut|liquidated|assigned|expired|"
    r"rolled|booked)\b", re.I
)
CASHTAG = re.compile(r"\$([A-Z]{1,6})\b")
NOT_TICKERS = {
    "USD", "CEO", "ATH", "DTE", "FOMO", "EOD", "IV", "OTM", "ITM", "PM", "AH", "YOLO",
    "DD", "PT", "TA", "EPS", "IPO", "ETF", "CPI", "FOMC", "GDP", "AI", "US", "USA", "K", "M", "B",
}


def tickers_in(post):
    found = set()
    raw = post.get("tickers") or ""
    if isinstance(raw, str):
        found |= {t.strip().lstrip("$").upper() for t in re.split(r"[,\s]+", raw) if t.strip()}
    elif isinstance(raw, list):
        found |= {str(t).strip().lstrip("$").upper() for t in raw if str(t).strip()}
    text = f"{post.get('title') or ''} {post.get('body') or ''}"
    found |= set(CASHTAG.findall(text))
    return {t for t in found if t and t not in NOT_TICKERS and len(t) <= 6}


def analyse(path):
    handle = os.path.basename(path).replace("_all_posts.json", "").lstrip("@")
    try:
        raw = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    posts = raw if isinstance(raw, list) else raw.get("posts", raw)
    if not isinstance(posts, list) or not posts:
        return None

    posts = sorted(posts, key=lambda p: p.get("created_at") or p.get("date") or "")

    entry_posts = exit_posts = 0
    gain_tags = loss_tags = 0
    opened = {}   # ticker -> date first announced as a buy
    closed = {}   # ticker -> date first announced as a sell

    for post in posts:
        text = f"{post.get('title') or ''} {post.get('body') or ''}"
        date = post.get("date") or (post.get("created_at") or "")[:10]
        tag = (post.get("tag") or "").strip().lower()
        gl = (post.get("gain_loss") or "").strip().lower()
        if "gain" in tag or "gain" in gl:
            gain_tags += 1
        if "loss" in tag or "loss" in gl:
            loss_tags += 1

        is_entry, is_exit = bool(ENTRY.search(text)), bool(EXIT.search(text))
        if is_entry:
            entry_posts += 1
        if is_exit:
            exit_posts += 1

        for ticker in tickers_in(post):
            if is_entry and ticker not in opened:
                opened[ticker] = date
            if is_exit and ticker not in closed:
                closed[ticker] = date

    round_tripped = {t for t in opened if t in closed and closed[t] >= opened[t]}
    followthrough = (len(round_tripped) / len(opened) * 100) if opened else None

    return {
        "handle": handle,
        "posts": len(posts),
        "entry_posts": entry_posts,
        "exit_posts": exit_posts,
        "entry_exit_ratio": round(entry_posts / exit_posts, 2) if exit_posts else None,
        "tickers_announced_as_buys": len(opened),
        "tickers_ever_closed_publicly": len(round_tripped),
        "followthrough_pct": round(followthrough, 1) if followthrough is not None else None,
        "gain_tagged_posts": gain_tags,
        "loss_tagged_posts": loss_tags,
        "gain_loss_tag_ratio": round(gain_tags / loss_tags, 2) if loss_tags else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=DATA_DIR)
    ap.add_argument("--json", help="also write results here")
    args = ap.parse_args()

    rows = [r for r in (analyse(p) for p in sorted(glob(os.path.join(args.dir, "*_all_posts.json")))) if r]
    rows.sort(key=lambda r: -r["posts"])

    print(f"{'handle':<20}{'posts':>7}{'entry':>7}{'exit':>6}{'bought':>8}{'closed':>8}{'follow%':>9}{'gain':>6}{'loss':>6}")
    print("-" * 77)
    for r in rows:
        follow = f"{r['followthrough_pct']:.1f}" if r["followthrough_pct"] is not None else "-"
        print(
            f"{'@'+r['handle']:<20}{r['posts']:>7}{r['entry_posts']:>7}{r['exit_posts']:>6}"
            f"{r['tickers_announced_as_buys']:>8}{r['tickers_ever_closed_publicly']:>8}{follow:>9}"
            f"{r['gain_tagged_posts']:>6}{r['loss_tagged_posts']:>6}"
        )

    tot_open = sum(r["tickers_announced_as_buys"] for r in rows)
    tot_closed = sum(r["tickers_ever_closed_publicly"] for r in rows)
    tot_gain = sum(r["gain_tagged_posts"] for r in rows)
    tot_loss = sum(r["loss_tagged_posts"] for r in rows)
    tot_entry = sum(r["entry_posts"] for r in rows)
    tot_exit = sum(r["exit_posts"] for r in rows)
    print("-" * 77)
    print(f"\n{len(rows)} traders, {sum(r['posts'] for r in rows):,} posts")
    print(f"  positions announced as buys : {tot_open:,}")
    print(f"  ever closed in public       : {tot_closed:,}  ({tot_closed/tot_open*100:.1f}%)")
    print(f"  never mentioned again as exits: {tot_open-tot_closed:,}  ({(tot_open-tot_closed)/tot_open*100:.1f}%)")
    print(f"  entry-language posts        : {tot_entry:,}")
    print(f"  exit-language posts         : {tot_exit:,}  ({tot_entry/tot_exit:.2f} entries per exit)")
    print(f"  Gain-tagged posts           : {tot_gain:,}")
    print(f"  Loss-tagged posts           : {tot_loss:,}  ({tot_gain/tot_loss:.2f} gains per loss)" if tot_loss else "")

    if args.json:
        json.dump(rows, open(args.json, "w"), indent=2)
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
