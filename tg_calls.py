#!/usr/bin/env python3
"""
tg_calls.py: extract trade callouts (ticker, option strike/side/expiry, entry price, results) from the
public Telegram posts archived by tg_watch.py. Offline; no network.

  python3 tg_calls.py   -> data/telegram_funnel/calls.jsonl, reports/analysis/funnel_calls.md

One record per ticker mention in a post. action: open | close | mention. Parsing is regex-based and
deliberately conservative: raw text is kept so anything odd can be re-parsed. Calls are promo copy.
"""
import json, re, collections as C
from datetime import datetime
from pathlib import Path
B = Path(__file__).resolve().parent
ARCH = B/"data/telegram_funnel/posts_archive.jsonl"
OUT = B/"data/telegram_funnel/calls.jsonl"
MON = {m: i for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), 1)}
TK = r"\$([A-Z]{1,5})\b"
STOP = {"A","I","S","K","B","C","IT","ON","ALL","ARE","FOR","NOW","AI","CEO","USD","USDT","ATH","PM","AM","EOD","IV","OTM","ITM","TP","SL","TG","VIP"}
OPT_A = re.compile(TK + r"\s+(?:(\d{1,2}/\d{1,2}(?:/\d{2,4})?)\s+)?(\d+(?:\.\d+)?)\s*(C|P|CALLS?|PUTS?)\b(?:\s+(\d{1,2}/\d{1,2}(?:[/.]\d{2,4})?))?", re.I)
OPT_B = re.compile(TK + r"\s+(\d{1,2})\s+([A-Za-z]{3})\s+(\d{2,4})\s+\$?(\d+(?:\.\d+)?)\s*(CALLS?|PUTS?)\b", re.I)
PRICE = re.compile(r"(?:@|at|entry:?|in at)\s*\$?\s*(\d*\.\d+|\d+)", re.I)
TAILP = re.compile(r"(?:CALLS?|PUTS?)\s+\$(\d*\.\d+|\d+)", re.I)
PCT = re.compile(r"([+-]\s?\d+(?:\.\d+)?)\s*%")
OPEN = re.compile(r"\b(open(?:ed|ing)?|entry|buy|bought|bto|adding|add|new trade|trade call|alert|long)\b", re.I)
CLOSE = re.compile(r"\b(clos(?:e|ed|ing)|exit(?:ed)?|sold|sell|stc|trim(?:med)?|take profit|tp hit|profit|stopped)\b|\+\s?\d+(?:\.\d+)?\s*%", re.I)


def iso_exp(raw, posted):
    if not raw: return None
    y = int(posted[:4]) if posted else datetime.utcnow().year
    m = re.match(r"(\d{1,2})[/.](\d{1,2})(?:[/.](\d{2,4}))?$", raw)
    if not m: return None
    yy = m.group(3)
    yy = (2000 + int(yy) if len(yy) == 2 else int(yy)) if yy else y
    try: return datetime(yy, int(m.group(1)), int(m.group(2))).date().isoformat()
    except ValueError: return None


def parse(p):
    t, posted = p["text"], p.get("date") or ""
    recs, seen = [], set()
    def add(tk, side, strike, exp, price, kind):
        if tk in STOP: return
        key = (tk, side, strike, exp)
        if key in seen: return
        seen.add(key)
        head = t[max(0, t.find("$" + tk) - 40): t.find("$" + tk) + 90]
        action = "close" if CLOSE.search(head) and not re.search(r"\bopen", head, re.I) else "open" if OPEN.search(t[:200]) or price else "mention"
        pct = PCT.search(t)
        recs.append({"id": p["id"], "channel": p["channel"], "posted": posted, "ticker": tk, "kind": kind, "side": side,
                     "strike": strike, "expiry": exp, "entry_price": price, "action": action,
                     "result_pct": float(pct.group(1).replace(" ", "")) if pct and action == "close" else None,
                     "text": t[:240]})
    def price_after(span_end):
        seg = t[span_end: span_end + 60]
        m = PRICE.search(seg) or TAILP.search(t[span_end - 12: span_end + 40])
        try: return float(m.group(1)) if m else None
        except ValueError: return None
    for m in OPT_B.finditer(t):
        exp = None
        try: exp = datetime(2000 + int(m.group(4)) if int(m.group(4)) < 100 else int(m.group(4)), MON[m.group(3).upper()], int(m.group(2))).date().isoformat()
        except (KeyError, ValueError): pass
        add(m.group(1).upper(), "call" if m.group(6).upper().startswith("C") else "put", float(m.group(5)), exp, price_after(m.end()), "option")
    for m in OPT_A.finditer(t):
        side = "call" if m.group(4).upper().startswith("C") else "put"
        add(m.group(1).upper(), side, float(m.group(3)), iso_exp(m.group(2) or m.group(5), posted), price_after(m.end()), "option")
    for m in re.finditer(TK, t):
        tk = m.group(1)
        if tk not in STOP and not any(r["ticker"] == tk for r in recs):
            add(tk, None, None, None, None, "stock")
    return recs


def main():
    P = [json.loads(l) for l in ARCH.open() if l.strip()] if ARCH.exists() else []
    recs = [r for p in P for r in parse(p)]
    recs.sort(key=lambda r: r["posted"])
    with OUT.open("w") as f:
        for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    opt = [r for r in recs if r["kind"] == "option"]
    opens = [r for r in opt if r["action"] == "open"]
    closes = [r for r in opt if r["action"] == "close"]
    byc = C.Counter(r["channel"] for r in opt)
    tk = C.Counter(r["ticker"] for r in opens)
    wins = [r["result_pct"] for r in closes if r["result_pct"] is not None]
    L = ["# Funnel callouts parsed from public Telegram posts", "",
         f"{len(P)} archived posts -> {len(recs)} ticker records ({len(opt)} option calls: {len(opens)} opens, {len(closes)} closes, "
         f"{len(opt) - len(opens) - len(closes)} other).", "",
         f"Closes that quote a result: {len(wins)}" + (f"; all positive: {sum(1 for w in wins if w > 0)}/{len(wins)}; mean quoted {sum(wins)/len(wins):+.1f}%" if wins else "") +
         ". Quoted results are the channel's own claims, not verified fills.", "",
         "## Option calls by channel", *[f"- {c}: {n}" for c, n in byc.most_common(12)], "",
         "## Most-opened tickers", *[f"- ${t}: {n}" for t, n in tk.most_common(15)], "",
         "## Sample opens"] + [f"- {r['posted'][:10]} {r['channel']}: ${r['ticker']} {r['strike']}{(r['side'] or '?')[0].upper()} exp {r['expiry']} @ {r['entry_price']}" for r in opens[-12:]]
    (B/"reports/analysis/funnel_calls.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
