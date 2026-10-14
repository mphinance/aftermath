#!/usr/bin/env python3
"""
tg_calls.py: extract trade callouts (ticker, option strike/side/expiry, entry price, results) from the
public Telegram posts archived by tg_watch.py. Offline, stdlib only; no network.

  python3 tg_calls.py   -> data/telegram_funnel/calls.jsonl, reports/analysis/funnel_calls.md

One record per ticker anchor in a post. Anchors are cashtags ($SPY, any case), bare tickers glued to an option
spec (SPY 777C, HOOD 10/16 112C), "XXX TRADE CALL/UPDATE" headlines, and a few core tickers in "spy puts @ 20%"
style trim lines. Raw text is kept so anything odd can be re-parsed. Calls are promo copy.

Fields (original, unchanged): id channel posted ticker kind side strike expiry entry_price action result_pct text
  kind        option | stock (no contract details) | spread (multi-leg; strike is null, see strikes)
  action      open | close | mention. Recap lists (CLOSED TRADES, daily recaps) emit close for lines that quote a
              result and mention for holdings/narrative; they never emit opens. A close wins over a later "Opened"
              line in the same post.
  entry_price the PREMIUM paid, only when stated as an entry (@ on an open, "Entry:", "avg", "from X", "X -> Y",
              a bare trailing price like "SPX 7795C .60", "e.68"). On a close, "@ 3.62" is the EXIT price, not the entry.
  result_pct  only a realised-looking result claim attached to THIS ticker's own text (signed %, or "N% return/gain").
              Never TP/SL targets, summary totals, "up N%" / "now" unrealised figures, or hindsight talk.
Fields added: exit_price, strikes (spread legs), expiry_raw, open_id/open_link (closes linked to an earlier open
  from the same channel: "contract" = same strike/side, "ticker_day" = only contract opened that day), dup_of,
  parse_flags. Filter on parse_flags downstream; the parser prefers a flag or a null to a confident wrong value.
  Flags:
  expiry   no_expiry, expiry_0dte_tag / expiry_dte_tag (0DTE / 1DTE word; expiry = posted ET date / +N business days),
           expiry_far (>45d out), expiry_before_post (open dated before the post: expiry nulled, expiry_raw kept;
           date_dmy_possible if day/month could be swapped), date_dmy (13/10 read as 10/13)
  price    entry_from_tail (bare trailing price, no @), entry_unknown, exit_price_only (close with no known entry),
           entry_implausible (premium >= 8% of strike: nulled), price_ge_strike, pct_mismatch (quoted % vs prices)
  contract spread / spread_suspect (strike null, see strikes), no_strike, contract_unknown (ticker only),
           index_option, alias_spxw, crypto
  context  recap_item / recap_holding (recap lists: never opens), has_summary (Trade Summary tail dropped),
           result_claim, loss_no_pct, unrealized_pct / pct_unlabelled (percent seen but not a result), hindsight,
           price_update + list_item ("7700C @ 11 from 5.1" mark-to-market lines: mention, not a new entry),
           ticker_list (6+ bare cashtags, no contracts: pitch/watchlist), tp_sl_present
  quality  duplicate_echo (same contract+action+prices, same channel, same ET day), cross_channel_echo (same, other
           channel), posted_date_suspect (6+ archived posts of the channel share one timestamp: backfilled)
Known gaps: bare ticker AFTER the percent ("TRIM / 90% MSFT"), "QQQ calls 730C" prose, tickers with no cashtag and no
contract in the same line, strike lists with no ticker, dates split from the strike by prose, expiry-less posts
(no_expiry; downstream decides whether to assume same-day).
"""
import json, re, collections as C
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover
    ET = timezone(timedelta(hours=-4))
B = Path(__file__).resolve().parent
ARCH = B/"data/telegram_funnel/posts_archive.jsonl"
OUT = B/"data/telegram_funnel/calls.jsonl"
MONS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
MON = {m: i for i, m in enumerate(MONS, 1)}
STOP = set("""A B C D E F G H I J K L M N O P Q R S T U V W X Y Z IT ON ALL ARE FOR NOW AI CEO USD USDT ATH PM AM EOD IV OTM ITM
ATM TP SL TG VIP BTO STC STO BTC OPEN OPENED CLOSE CLOSED SWING AVG ENTRY RISK STOP TARGET TAKE CALL PUT CALLS PUTS EXIT SOLD
SELL BUY LONG SHORT ADD ADDED OUT NEW UP DOWN BIG LOTTO DAY WEEK TRADE ALERT UPDATE SCALP RUNNER RUNNERS HOLD HOLDING DTE ODTE
THE AND BUT YOU WE IS IN TO OF AT BE OR AN IF SO NO GO HIGH LOW EOW DD YOLO PNL ROI WIN LOSS BE TRIM FREE VIP USA ET EST CST
JAN FEB MAR APR MAY JUN JUL AUG SEP SEPT OCT NOV DEC MON TUE WED THU FRI SAT SUN MORNING GOOD HUGE LOCK NICE""".split())
CORE = set("SPY QQQ IWM DIA SPX SPXW NDX RUT VIX XSP AAPL MSFT NVDA TSLA AMZN GOOGL GOOG META AMD MU PLTR HOOD COIN MSTR NFLX AVGO SMCI CRWD SOFI TGT BA UBER ORCL INTC".split())
CRYPTO = set("BTC ETH SOL NEAR XRP DOGE ADA LINK AVAX BNB SUI APT ARB TON PEPE SHIB WIF BONK".split())
INDEX = {"SPX", "SPXW", "NDX", "RUT", "VIX", "XSP"}

NUM = r"\d+(?:\.\d+)?"
def DATE(n, dm=False):
    s = (rf"(?:(?<![\d.$])(?P<mo{n}>\d{{1,2}})[/-](?P<dy{n}>\d{{1,2}})(?:[/-](?P<yr{n}>\d{{4}}|\d{{2}}))?(?!\d)"
         rf"|(?P<mn{n}>{'|'.join(MONS)})[A-Z]*[\s/.-]{{0,2}}(?P<md{n}>\d{{1,2}})(?!\d)")
    if dm: s += rf"|(?<![\d.$])(?P<dd{n}>\d{{1,2}})[/\s-]{{0,2}}(?P<nm{n}>{'|'.join(MONS)})(?![A-Za-z0-9])"
    return s + ")"
SEP = r"[\s,|:·\-–—]*"
SIDEP = r"(?:\s*(?P<sw>CALLS?|PUTS?)|(?P<sl>[CP])|\s(?P<sl2>[CP])(?=\s*(?:@|\$?\.?\d|$)))\b"
P1 = re.compile(rf"(?:{DATE(1, True)}{SEP})?\$?\s?(?P<k>{NUM}(?:/{NUM})?){SIDEP}(?:{SEP}{DATE(2, True)})?", re.I)
P2 = re.compile(rf"(?:{DATE(1, True)}{SEP})?(?P<sw>CALLS?|PUTS?)\s*\$?\s*(?P<k>{NUM})(?![\d%]|\s*%)(?:{SEP}{DATE(2, True)})?", re.I)
P3 = re.compile(rf"\$?(?P<k>{NUM})\s+(?P<dy1>\d{{1,2}})\s+(?P<mn1>{'|'.join(MONS)})[A-Z]*\s+(?P<yr1>\d{{2,4}})\s+(?:\(\w\)\s+)?(?P<sw>CALLS?|PUTS?)\b", re.I)
P3B = re.compile(rf"(?P<dy1>\d{{1,2}})\s+(?P<mn1>{'|'.join(MONS)})[A-Z]*\s+(?P<yr1>\d{{2,4}})\s+\$?(?P<k>{NUM})\s*(?:\(\w\)\s*)?(?P<sw>CALLS?|PUTS?)\b", re.I)
LISTITEM = re.compile(r"(?m)^[^\w\n]*(\d{2,5}(?:\.\d+)?)\s?([CP])?\b[^\n@]{0,12}@\s*\$?(\d*\.\d+|\d+)\s+from\s+\$?(\d*\.\d+|\d+)", re.I)
HEAD_DATE = re.compile(DATE(1, True), re.I)
LEAD_DATE = re.compile(rf"{DATE(1)}[\W_]*$", re.I)
SIDE_ONLY = re.compile(r"^[\W_]{0,6}(CALLS?|PUTS?)\b(?!\s+(?:wall|above|below|side))", re.I)
SPREAD_W = re.compile(r"\b(CDS|PDS|CCS|PCS|(?:call|put|debit|credit|vertical|calendar)\s+spread|spread|iron\s+condor|butterfly|straddle|strangle)\b", re.I)

CASH = re.compile(r"(?<![\w$])\$([A-Za-z]{1,5})\b(?![\w])")
BARE_CONTRACT = re.compile(r"(?<![\w$@])([A-Za-z]{2,5})(?=\s+(?:(?:\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|\d{1,2}\s+(?i:" + "|".join(MONS) + r")[a-z]*|(?i:" + "|".join(MONS) + r")[a-z]*[\s/]\d{1,2})\s+)?\$?\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?(?:[CcPp]\b|\s?(?i:calls?|puts?)\b|\s[CcPp]\s*(?:@|\d|$)))")
LIST_HEAD = re.compile(rf"(?m)^[^\w\n$]*([A-Z]{{2,5}})\s+(?:{DATE(1, True)}\s+)?(?:CALLS?|PUTS?)[^\w\n]*$")
BARE_SIDE = re.compile(r"(?<![\w$@])([A-Za-z]{2,5})\s+(?:calls?|puts?)\b(?=[^\n]{0,14}?(?:\d+(?:\.\d+)?\s*%|LOSS|WIN))", re.I)
BARE_PCT = re.compile(r"(?<![\w$@])([A-Z]{2,5})\s+(?=[+-]?\d+(?:\.\d+)?\s*%)")
HEADLINE = re.compile(r"(?<![\w$])([A-Z]{2,5})\s+(?:\d?DTE\s+)?TRADE\s+(?:CALL|UPDATE|ALERT)\b")

OPEN_RE = re.compile(r"\b(?:open(?:ed|ing)?\b(?!\s*:)|entry|buy|bought|bto|adding|added|add|new trade|trade call|alert|locked in|(?:going|went|got) long|long (?:from|at|above))", re.I)
LONG_RE = re.compile(r"\bLONG\b(?!\s*[- ]?term)")
CLOSE_RE = re.compile(r"\b(?:closed|closing|exit(?:ed)?|sold|sell(?:ing)?|stc|trim(?:med|ming)?|took profits?|tak(?:e|ing|en) profits?|profits? tak(?:en|ing)|tp hit|stopped(?: out)?|all out|cut(?:ting)?)\b"
                      r"|(?:^|\n)\s*[^\w\n]*close\b(?!\s+(?:to|under|above|below|over|at))|\bclose\s+(?:out|all|half|rest|remaining)\b", re.I)
MODAL = re.compile(r"\b(?:might|maybe|may|if|could|should|plan(?:ning)? to|looking (?:to|for)|will|going to|want to|wanna|for|to|when|once)\s+(?:\S+\s+){0,2}$", re.I)
WATCH_RE = re.compile(r"\bwatch(?:ing|list)?\b|\bideas?\b", re.I)
HINDSIGHT = re.compile(r"should(?:'|’)?ve|could(?:'|’)?ve|would(?:'|’)?ve|would have|if anyone|if you|had you|missed", re.I)
TPSL = re.compile(r"\b(?:TP|SL|targets?|stop(?:\s?loss)?|take(?:\s?profit)?)\b(?!\s*(?:hit|reached|done))[^\n]*", re.I)
PCTN = r"(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
SIGNED_ADJ = re.compile(r"(?<![A-Za-z0-9.])([+\-])" + PCTN + r"\s*%")
SIGNED_SP = re.compile(r"(?<=[|:(])\s*([+\-])\s" + PCTN + r"\s*%")
GAINPCT = re.compile(r"(?<![\d,.])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\s*%[^\n\w]{0,8}(?:RETURN|GAINS?|GAINER|PROFITS?)\b|\b(?:RETURN|GAIN|PROFIT)\s*:?\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\s*%", re.I)
DTE_RE = re.compile(r"\b(?:(\d{1,2})\s?DTE|(odte)|zero[\s-]?dte|zero[\s-]day)\b", re.I)
BTO_PREFIX = re.compile(r"^\W*(?:(?:BTO|STO|BTC|STC|TRADE\s+(?:UPDATE|CALL|ALERT)|UPDATE)\b\W*)+", re.I)
UPNOW = re.compile(r"\b(?:up|now|currently)\s*:?\s*[+-]?\d[\d,.]*\s*%|\d[\d,.]*\s*%\s*(?:up|now)\b", re.I)
DATE_AFTER = re.compile(rf"^[^\n\dA-Za-z]{{0,3}}\$?(?:\d*\.\d+|\d+)\s*{DATE(3, True)}", re.I)
ANYPCT = re.compile(r"\d+(?:\.\d+)?\s*%")
UNREAL = re.compile(r"\b(?:currently|now|so far|right now|down|up)\W{0,3}$", re.I)
ODTE = re.compile(r"\b(?:0\s?dte|odte|zero\s?dte|same[- ]day)\b", re.I)
FROM = re.compile(r"\$?\s*(\d*\.\d+|\d+)\s+from\s+(?:our\s+|my\s+)?\$?\s*(\d*\.\d+|\d+)", re.I)
ARROW = re.compile(r"\$?\s*(\d*\.\d+|\d+)\s*(?:→|->|=>|➡️?|⇒)\s*\$?\s*(\d*\.\d+|\d+)")
LABEL = re.compile(r"\b(?:entry(?:\s*price)?|avg(?:\.|erage)?(?:\s*(?:price|entry|cost))?|(?:filled|fill|bought|entered|in)\s+at|cost|basis)\s*[:=@\-]?\s*\$?\s*(\d*\.\d+|\d+)(?!\d|\s*%)", re.I)
ATP = re.compile(r"@\s*\$?\s*(\d*\.\d+|\d+)(?![\d.]|\s*%)")
EPRICE = re.compile(r"\be\s*[:=]?\s*(\.\d+|\d+\.\d+)(?![\d%])", re.I)
TAIL = re.compile(r"^[\s|:·\-–—]*\$?\s?(\.\d+|\d+\.\d{1,2})(?![\d%/]|\s*(?:%|x\b|k\b|c\b|dte|dollars))", re.I)
GOT = re.compile(r"\bgot\s+\$?(\d*\.\d+|\d+)\b|\b(?:puts?|calls?)\s+got\s+\$?(\d*\.\d+|\d+)\b", re.I)
RECAP_HEAD = re.compile(r"recap|closed trades|still holding|trade review|position update", re.I)
POSITION_HEAD = re.compile(r"position update", re.I)
HOLD_HEAD = re.compile(r"still holding|active setups?|open positions?|holding:", re.I)
CLOSED_HEAD = re.compile(r"closed trades|^\s*results?:?\s*$", re.I | re.M)
SUMMARY_HEAD = re.compile(r"^\s*trade summary\b", re.I | re.M)


def posted_et(posted):
    try:
        d = datetime.fromisoformat(posted.replace("Z", "+00:00"))
        if d.tzinfo is None: d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(ET).date()
    except Exception:
        return None


def _grp(m, n):
    """(month, day, year-or-None, raw) for date group n of match m, or None."""
    g = m.groupdict()
    if g.get(f"mn{n}") and g.get(f"md{n}"):
        return MON[g[f"mn{n}"].upper()], int(g[f"md{n}"]), None, m.group(0).strip()
    if g.get(f"nm{n}") and g.get(f"dd{n}"):
        return MON[g[f"nm{n}"].upper()], int(g[f"dd{n}"]), None, f"{g[f'dd{n}']}/{g[f'nm{n}']}"
    if g.get(f"mo{n}") and g.get(f"dy{n}"):
        yr = g.get(f"yr{n}")
        if yr: yr = 2000 + int(yr) if len(yr) == 2 else int(yr)
        return int(g[f"mo{n}"]), int(g[f"dy{n}"]), yr, f"{g[f'mo{n}']}/{g[f'dy{n}']}" + (f"/{g[f'yr{n}']}" if g.get(f"yr{n}") else "")
    return None


def resolve_expiry(parts, pd, is_open, flags):
    """parts=(mo, dy, yr, raw). Returns ISO date or None; adds flags. Opens dated before the post are nulled."""
    if not parts: return None
    mo, dy, yr, raw = parts
    if mo > 12 and dy <= 12:
        mo, dy = dy, mo
        flags.add("date_dmy")
    base = pd or date.today()
    y = yr or base.year
    try: d = date(y, mo, dy)
    except ValueError: return None
    if yr is None and d < base - timedelta(days=60):
        try: d = date(y + 1, mo, dy)
        except ValueError: return None
    if is_open and pd and d < pd:
        flags.add("expiry_before_post")
        if mo <= 12 and dy <= 12 and mo != dy: flags.add("date_dmy_possible")
        return None
    if pd and d > pd + timedelta(days=45): flags.add("expiry_far")
    return d.isoformat()


def add_bdays(d, n):
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5: n -= 1
    return d


def _f(x):
    try: return float(x)
    except (TypeError, ValueError): return None


def _pct(g_sign, g_num):
    return float(g_num.replace(",", "")) * (-1 if g_sign == "-" else 1)


def find_anchors(t):
    """(start, end, ticker, src) per ticker mention; src: cash | bare | side | pct | head."""
    A = []
    for m in CASH.finditer(t): A.append((m.start(), m.end(), m.group(1).upper(), "cash"))
    for m in BARE_CONTRACT.finditer(t):
        if m.group(1).isupper() or m.group(1).upper() in CORE: A.append((m.start(1), m.end(1), m.group(1).upper(), "bare"))
    for m in LIST_HEAD.finditer(t): A.append((m.start(1), m.end(1), m.group(1), "list"))
    for m in BARE_SIDE.finditer(t):
        if m.group(1).upper() in CORE: A.append((m.start(1), m.end(1), m.group(1).upper(), "side"))
    for m in BARE_PCT.finditer(t):
        if m.group(1) in CORE: A.append((m.start(1), m.end(1), m.group(1), "pct"))
    heads = [(m.start(1), m.end(1), m.group(1), "head") for m in HEADLINE.finditer(t)]
    A.sort(key=lambda a: (a[0], a[1]))
    out = []
    for a in A:
        if out and a[0] < out[-1][1]: continue  # overlap
        if a[2] in STOP and not (len(a[2]) == 1 and a[3] == "cash" and find_contract(t[a[1]:a[1] + 60])): continue
        out.append(a)
    have = {a[2] for a in out}
    out += [h for h in heads if h[2] not in have and h[2] not in STOP]
    out.sort(key=lambda a: a[0])
    return out


def find_contract(seg):
    """Contract spec at the start of seg. Returns dict(kind, side, strike, strikes, dparts, end) or None."""
    best = None
    for rx in (P1, P2, P3, P3B):
        m = rx.search(seg[:120])
        if not m or re.search(r"[A-Za-z0-9]", seg[:m.start()]): continue
        if best is None or m.start() < best[1].start(): best = (rx, m)
    if not best: return None
    rx, m = best
    g = m.groupdict()
    sw = g.get("sw") or ("CALL" if (g.get("sl") or g.get("sl2") or "").upper() == "C" else "PUT")
    c = {"side": "call" if sw.upper().startswith("C") else "put", "end": m.end(), "kind": "option", "strike": None, "strikes": None}
    if "/" in g["k"]:
        c.update(kind="spread", strikes=[_f(x) for x in g["k"].split("/")])
    else:
        c["strike"] = _f(g["k"])
    if rx in (P3, P3B):
        yr = int(g["yr1"]); yr = 2000 + yr if yr < 100 else yr
        c["dparts"] = (MON[g["mn1"].upper()], int(g["dy1"]), yr, m.group(0))
    else:
        c["dparts"] = _grp(m, 2) or _grp(m, 1)
    return c


def parse(p):
    t = (p.get("text") or "").replace("​", "").replace("\xa0", " ")
    posted = p.get("date") or ""
    pd = posted_et(posted)
    flags_post = set()
    sm = SUMMARY_HEAD.search(t)
    if sm:  # a "Trade Summary" tail aggregates the day; only the part above it is this post's own call
        t = t[:sm.start()]
        flags_post.add("has_summary")
    recap = bool(RECAP_HEAD.search(t))
    position_update = bool(POSITION_HEAD.search(t))
    anchors = find_anchors(t)
    n_contracts = 0
    recs, seen = [], set()
    for i, (a0, a1, tk, src) in enumerate(anchors):
        nxt = anchors[i + 1][0] if i + 1 < len(anchors) else len(t)
        seg = t[a1:min(nxt, a1 + 260)]
        if recap: seg = seg.split("\n", 1)[0]
        ls = t.rfind("\n", 0, a0) + 1
        same = t[ls:a0]
        lead = same[-60:]
        if not same.strip():  # a short tag line right above ("SWING OPEN", "TRIM") belongs to this ticker
            prev = [x for x in t[:ls].split("\n") if x.strip()]
            if prev and len(prev[-1].strip()) <= 30 and not any(prev[-1].strip() in t[h[0]:h[1] + 40] for h in anchors):
                lead = prev[-1] + "\n" + lead
        flags = set(flags_post)
        items = list(LISTITEM.finditer(seg))
        if items:  # "$SPX CALLS / 9/24 CALLS / 7700C @ 11.00 from 5.10": one price update per strike line
            hdr = t[a0:a1] + seg[:items[0].start()]
            hs = re.search(r"\b(CALLS?|PUTS?)\b", hdr, re.I)
            hd = HEAD_DATE.search(hdr)
            dparts = _grp(hd, 1) if hd else None
            for it in items:
                sd = it.group(2) or (hs.group(1) if hs else None)
                if not sd: continue
                fl = set(flags) | {"price_update", "list_item"}
                ex = resolve_expiry(dparts, pd, False, fl) if dparts else None
                if ex is None: fl.add("no_expiry")
                if tk in INDEX: fl.add("index_option")
                recs.append({"id": p["id"], "channel": p["channel"], "posted": posted, "ticker": "SPX" if tk == "SPXW" else tk, "kind": "option",
                             "side": "call" if sd.upper().startswith("C") else "put", "strike": _f(it.group(1)), "expiry": ex,
                             "entry_price": _f(it.group(4)), "action": "mention", "result_pct": None, "text": t[:240],
                             "exit_price": _f(it.group(3)), "strikes": None, "expiry_raw": dparts[3] if dparts else None, "parse_flags": sorted(fl)})
            continue
        if src == "list": continue
        # ---- DTE tags and BTO-style prefixes are noise for the contract regexes
        dte = None
        for dm in DTE_RE.finditer(same[-30:] + " " + seg[:80]):
            dte = int(dm.group(1)) if dm.group(1) else 0
        seg = DTE_RE.sub(" ", seg, count=2)
        seg = BTO_PREFIX.sub(" ", seg, count=1)
        # ---- contract
        c = find_contract(seg)
        kind, side, strike, strikes, dparts, cend = "stock", None, None, None, None, 0
        if c:
            kind, side, strike, strikes, dparts, cend = c["kind"], c["side"], c["strike"], c["strikes"], c["dparts"], c["end"]
            if kind == "spread": flags.add("spread")
        else:
            so = SIDE_ONLY.search(seg[:30])
            if so: side = "call" if so.group(1).upper().startswith("C") else "put"
            elif src == "side": side = "call" if re.search(r"calls?", seg[:14], re.I) else "put"
        if c and not dparts:
            lm = LEAD_DATE.search(same)
            if lm: dparts = _grp(lm, 1)
        if kind == "option" and SPREAD_W.search(seg[:80]):
            kind, strikes, strike = "spread", [strike], None
            flags.update(("spread", "spread_suspect"))
        if kind in ("option", "spread"): n_contracts += 1
        # ---- text pieces
        after = seg[cend:] if c else seg
        stripped = TPSL.sub("", after)
        stripped_seg = TPSL.sub("", seg)
        if stripped != after or stripped_seg != seg: flags.add("tp_sl_present")
        holding = False
        if position_update: holding = True
        elif recap:
            before = t[:a0]
            h, cl = [m.end() for m in HOLD_HEAD.finditer(before)], [m.end() for m in CLOSED_HEAD.finditer(before)]
            holding = bool(h) and (not cl or h[-1] > cl[-1])
        # ---- result claim (signed %, "N% return", recap lines, trim lines); never TP/SL or summary text
        pct, unrealized, claim = None, False, False
        first_line = seg.split("\n", 1)[0]
        loss_word = bool(re.search(r"\bLOSS\b|❌", first_line if recap else seg[:60], re.I))
        for rx in (SIGNED_ADJ, SIGNED_SP):
            for m in rx.finditer(stripped_seg):
                if UNREAL.search(stripped_seg[:m.start()][-16:]): unrealized = True; continue
                pct, claim = _pct(m.group(1), m.group(2)), True
                break
            if claim: break
        if not claim:
            m = GAINPCT.search(stripped_seg)
            if m: pct, claim = float((m.group(1) or m.group(2)).replace(',', '')), True
        if not claim and recap:
            m = re.search(r"(-?\d+(?:\.\d+)?)\s*%", TPSL.sub("", first_line))
            if m: pct, claim = float(m.group(1)), True
        def _close(s):
            return any(not MODAL.search(s[max(0, m.start() - 24):m.start()]) for m in CLOSE_RE.finditer(s))
        lead_close = _close(lead)
        if not claim and (src in ("side", "pct") or lead_close):  # "TRIM / $AMZN 30% here", "spy puts @ 20%"
            m = re.match(r"[^\n\d]{0,16}(\d+(?:\.\d+)?)\s*%", seg)
            if m: pct, claim = float(m.group(1)), True
        unlabeled = not claim and bool(ANYPCT.search(stripped_seg[:120]))
        up_now = not claim and bool(UPNOW.search(stripped_seg[:120]))
        mf, ma = FROM.search(TPSL.sub("", after)), ARROW.search(TPSL.sub("", after))
        # ---- action
        hind = bool(HINDSIGHT.search(seg[:200]))
        lead_open = bool(OPEN_RE.search(lead) or LONG_RE.search(lead))
        seg_close = _close(seg[:200])
        seg_open = bool(OPEN_RE.search(stripped_seg[:100]) or LONG_RE.search(stripped_seg[:100]))
        contract = kind in ("option", "spread")
        if recap:
            action = "mention" if holding or not (claim or loss_word) else "close"
            flags.add("recap_holding" if holding else "recap_item")
        elif lead_close: action = "close"
        elif lead_open: action = "open"
        elif hind:
            action = "mention"; flags.add("hindsight")
        elif WATCH_RE.search(lead + seg[:60]) and not claim: action = "mention"
        elif (mf or ma) and not (seg_open or seg_close or claim):  # "7700C @ 11 from 5.1": a mark-to-market update, not a new entry
            action = "mention"; flags.add("price_update")
        elif up_now and not (seg_open or seg_close or ATP.search(stripped_seg)): action = "mention"
        elif seg_close or claim: action = "close"
        elif contract or seg_open: action = "open"
        else: action = "mention"
        if src == "pct" and not (action == "close" and (lead_close or seg_close)): continue  # bare "TSLA 15%" / "PLTR -50%" is not a sale
        if src == "side" and not (claim or loss_word or action == "close"): continue
        if src == "head" and kind == "stock" and action == "mention": continue
        # ---- prices: FROM/ARROW name both legs; "@ x" is the entry on an open and the exit on a close
        entry = exitp = None
        if mf: entry, exitp = _f(mf.group(2)), _f(mf.group(1))
        elif ma: entry, exitp = _f(ma.group(1)), _f(ma.group(2))
        else:
            ml = LABEL.search(stripped)
            if ml: entry = _f(ml.group(1))
        plain, tail = None, False
        for rx in (ATP, EPRICE):
            mm = rx.search(stripped)
            if mm: plain = _f(mm.group(1)); break
        if plain is None and contract:
            mt = TAIL.match(after[:40])
            if mt:
                v, ref = _f(mt.group(1)), (strike or (strikes[0] if strikes else None))
                if v is not None and (ref is None or v < ref * 0.3): plain, tail = v, True
        if plain is None and action == "close":
            mg = GOT.search(stripped)
            if mg: plain = _f(mg.group(1) or mg.group(2))
            else:
                ml2 = re.search(r"\b(?:got|sold(?: at)?|out)\s+\$?(\d*\.\d+|\d+)\s+on\s*$", same, re.I)  # "Got 3.3 on $SPX puts"
                if ml2: plain = _f(ml2.group(1))
        if not (mf or ma):
            if action == "open" and entry is None and plain is not None:
                entry = plain
                if tail: flags.add("entry_from_tail")
            elif action == "close" and plain is not None:
                exitp = plain
        if action == "close" and exitp is not None and entry is None: flags.add("exit_price_only")
        if action == "mention" and not (mf or ma): entry = exitp = None
        ref = strike or (strikes[0] if strikes else None)
        if action == "open" and entry is not None and ref and entry >= ref * 0.08 and tk not in INDEX:
            flags.add("entry_implausible"); entry = None
        # ---- expiry
        exp, rawexp = None, None
        if contract and not dparts:
            md = DATE_AFTER.match(after[:40])
            if md: dparts = _grp(md, 3)
        if contract:
            if dparts:
                exp, rawexp = resolve_expiry(dparts, pd, action == "open", flags), dparts[3]
            if exp is None and dte is not None and pd:
                exp = (add_bdays(pd, dte) if dte else pd).isoformat(); flags.add("expiry_0dte_tag" if dte == 0 else "expiry_dte_tag")
                flags.discard("expiry_before_post")
            if exp is None and "expiry_before_post" not in flags: flags.add("no_expiry")
        elif side or claim or src in ("side", "pct", "head"):
            flags.add("no_strike" if side else "contract_unknown")
            if src in ("side", "pct"): flags.add("contract_unknown")
        if claim and action == "close": flags.add("result_claim")
        if unrealized or up_now: flags.add("unrealized_pct")
        elif unlabeled: flags.add("pct_unlabelled")
        if recap and action == "close" and pct is None: flags.add("loss_no_pct")
        if action == "open" and entry is None: flags.add("entry_unknown")
        if tk in INDEX: flags.add("index_option")
        if tk in CRYPTO: flags.add("crypto")
        if tk == "SPXW": flags.add("alias_spxw")
        if entry and exitp and pct is not None and abs((exitp / entry - 1) * 100 - pct) > 6: flags.add("pct_mismatch")
        if action != "close": pct = None
        tkn = "SPX" if tk == "SPXW" else tk
        if contract:
            key = (tkn, side, strike, tuple(strikes) if strikes else None, exp, action) + ((pct,) if recap else ())
            if key in seen: continue
        elif recap: key = (tkn, side, pct, action)
        elif any(r["ticker"] == tkn for r in recs): continue
        else: key = (tkn, None, None, None, None, action)
        seen.add(key)
        recs.append({"id": p["id"], "channel": p["channel"], "posted": posted, "ticker": tkn, "kind": kind, "side": side,
                     "strike": strike, "expiry": exp, "entry_price": entry, "action": action, "result_pct": pct,
                     "text": t[:240], "exit_price": exitp, "strikes": strikes, "expiry_raw": rawexp, "parse_flags": sorted(flags)})
    # a long list of bare cashtags with no contracts is a watchlist / pitch, never a set of calls
    if len(recs) >= 6 and n_contracts == 0 and not recap:
        for r in recs:
            if r["action"] != "close": r["action"] = "mention"
            r["parse_flags"] = sorted(set(r["parse_flags"]) - {"entry_unknown"} | {"ticker_list"})
    return recs


def annotate(recs):
    """Echo flags and close->open links. Mutates recs (sorted by posted)."""
    first, first_x = {}, {}
    for r in recs:
        if r["action"] not in ("open", "close") or (r["kind"] == "stock" and r["action"] == "open" and r["entry_price"] is None and not r["side"]):
            if not (r["action"] == "open" and r["kind"] == "stock"): continue
        day = (posted_et(r["posted"]) or r["posted"][:10])
        k = (r["ticker"], r["side"], r["strike"], tuple(r["strikes"] or ()), r["expiry"], r["action"], r["entry_price"], r["exit_price"], r["result_pct"], str(day))
        if (r["channel"],) + k in first:
            r["parse_flags"] = sorted(set(r["parse_flags"]) | {"duplicate_echo"}); r["dup_of"] = first[(r["channel"],) + k]
        elif k in first_x:
            r["parse_flags"] = sorted(set(r["parse_flags"]) | {"cross_channel_echo"}); r["dup_of"] = first_x[k]
            first[(r["channel"],) + k] = r["id"]
        else:
            first[(r["channel"],) + k] = r["id"]; first_x[k] = r["id"]
    opens = [r for r in recs if r["action"] == "open" and "duplicate_echo" not in r["parse_flags"]]
    for r in recs:
        if r["action"] != "close": continue
        cand = [o for o in opens if o["channel"] == r["channel"] and o["ticker"] == r["ticker"] and o["posted"] <= r["posted"]
                and (posted_et(r["posted"]) - posted_et(o["posted"])).days <= 3]
        if r["strike"] is not None:
            exact = [o for o in cand if o["strike"] == r["strike"] and o["side"] == r["side"] and (r["expiry"] in (None, o["expiry"]) or o["expiry"] is None)]
            if exact: r["open_id"], r["open_link"] = exact[-1]["id"], "contract"; continue
        day = [o for o in cand if posted_et(o["posted"]) == posted_et(r["posted"]) and (r["side"] in (None, o["side"]))]
        if len({(o["strike"], o["expiry"], o["side"]) for o in day}) == 1:
            r["open_id"], r["open_link"] = day[-1]["id"], "ticker_day"
    return recs


def main():
    P = [json.loads(l) for l in ARCH.open() if l.strip()] if ARCH.exists() else []
    recs = [r for p in P for r in parse(p)]
    recs.sort(key=lambda r: r["posted"])
    annotate(recs)
    # a channel whose archived posts share one timestamp (backfilled / bulk-forwarded) has no usable posted date
    same_ts = C.Counter((p["channel"], p.get("date")) for p in P)
    for r in recs:
        if same_ts[(r["channel"], r["posted"])] >= 6: r["parse_flags"] = sorted(set(r["parse_flags"]) | {"posted_date_suspect"})
    with OUT.open("w") as f:
        for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    uniq = [r for r in recs if not {"duplicate_echo", "cross_channel_echo"} & set(r["parse_flags"])]
    opt = [r for r in uniq if r["kind"] in ("option", "spread")]
    opens = [r for r in opt if r["action"] == "open"]
    closes = [r for r in uniq if r["action"] == "close"]
    byc = C.Counter(r["channel"] for r in opt)
    tk = C.Counter(r["ticker"] for r in opens)
    wins = [r["result_pct"] for r in closes if r["result_pct"] is not None]
    fl = C.Counter(f for r in recs for f in r["parse_flags"])
    clean = [r for r in opens if r["expiry"] and r["entry_price"] is not None and r["kind"] == "option" and not {"spread_suspect", "expiry_far"} & set(r["parse_flags"])]
    L = ["# Funnel callouts parsed from public Telegram posts", "",
         f"{len(P)} archived posts -> {len(recs)} ticker records; {len(recs) - len(uniq)} are echoes (same contract, same channel or another one, same day) and are excluded below.", "",
         f"Unique option/spread calls: {len(opt)} ({len(opens)} opens, {sum(1 for r in opt if r['action'] == 'close')} closes, "
         f"{sum(1 for r in opt if r['action'] == 'mention')} mentions). Opens with a clean contract (strike, side, expiry, entry price all present): {len(clean)}.", "",
         f"Closes (any kind) that quote a result: {len(wins)}" + (f"; positive: {sum(1 for w in wins if w > 0)}/{len(wins)}; mean quoted {sum(wins)/len(wins):+.1f}%" if wins else "") +
         ". Quoted results are the channel's own claims, not verified fills.", "",
         "## Option calls by channel", *[f"- {c}: {n}" for c, n in byc.most_common(12)], "",
         "## Most-opened tickers", *[f"- ${t}: {n}" for t, n in tk.most_common(15)], "",
         "## Parse flags (all records)", *[f"- {f}: {n}" for f, n in fl.most_common()], "",
         "## Sample opens"] + [f"- {r['posted'][:10]} {r['channel']}: ${r['ticker']} {r['strike']}{(r['side'] or '?')[0].upper()} exp {r['expiry']} @ {r['entry_price']}" for r in opens[-12:]]
    (B/"reports/analysis/funnel_calls.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
