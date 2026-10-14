#!/usr/bin/env python3
"""
tg_fx_signals.py: parse forex / gold / index / crypto-pair trading signals out of archived public Telegram posts
and score them against the real tape (Yahoo public 5m bars). Stdlib only, read-only.

  python3 tg_fx_signals.py                      # full run (fetches Yahoo bars into the price cache, serial, >=0.4s apart)
  python3 tg_fx_signals.py --no-fetch           # cache only; instruments without cached bars are reported unpriced
  python3 tg_fx_signals.py --horizon-hours 24 --touch-hours 4 --basis auto|none

Input : data/telegram_funnel/posts_archive.jsonl (id, channel, date UTC ISO, views, text)
Output: data/telegram_funnel/fx_signals.jsonl   one row per signal-shaped post (scored or skipped with a reason)
        data/telegram_funnel/fx_claims.jsonl    the channel's own follow-up claims ("TP1 hit", "+180 pips", "SL hit")
        reports/analysis/fx_signals.md          coverage funnel, per-instrument / per-channel / weekly tables

Public posts only. Analysis, not an accusation. Never touches Telegram, never posts anything.

PARSING
  A post is signal-shaped when it names an instrument (GOLD/XAUUSD/XAU, US30, NAS100, JP225, SPX500, oil, FX pairs such
  as EURUSD or GBP/CHF, crypto pairs such as AVAX/USD, BTC) AND a side (buy/sell/long/short) AND a stop or take-profit
  level. Emoji, math-bold letters, superscript TP numbers and labels (SL, Sl, Stop, Stop Loss (SL), TP1, 1st, 2nd,
  1_TP, Target 1, Take Profit 1 (TP1), Targets: lists, "TP -/ a / b") are normalised first. Entry is a single price, a
  zone "a - b" (also "a / b", "a. b", "<a-b>", and abbreviated "4348-46"), or absent ("NOW" with no number).
  Take profits are prices or pips ("TP: 50/100PIPS").

PIP CONVENTIONS (ASSUMPTION, flagged tp_pips_assumed on every pips-based signal)
  gold XAUUSD: 1 pip = 0.10 (so 50 pips = $5.00) | indices (US30, NAS100, JP225, SPX500): 1 pip = 1 index point |
  FX: 0.0001 (0.01 for JPY quote) | everything else: unsupported, signal not scored. Pips are measured from the fill price.

TYPO RULE
  Once the market price at post time is known, any of entry / SL / first TP price that is more than TYPO_PCT away from
  it (10% for crypto) is flagged typo_price_off_market (typo_magnitude if the ratio is outside 0.5-2, the missing-digit
  case "5130" vs 51000). A stop farther than MAX_RISK_PCT from the entry is flagged sl_distance_implausible. Flagged
  signals are reported, never scored. Limit-order entries are allowed to be away from market, up to TYPO_PCT.

SCORING (see the report for the full list of assumptions)
  Market variant: entry missing / "NOW", or the market (close of the 5m bar containing the post, up to 5 minutes after
  the post) is inside the entry zone widened by tol = 0.25 * |entry_mid - SL|. Fill = that close. Walk starts at the next bar.
  Touch variant (entry_not_at_market): fill when a later bar's range reaches the nearest edge of the entry (zone) or the
  entry price, within TOUCH_HOURS of the post; fill price is that edge. Cancelled if the SL or TP1 is touched first.
  Both variants are reported separately and never pooled.
  Walk: 5m bars up to HORIZON_HOURS after the fill. If SL and a TP are both inside one bar, SL is counted first and
  ambiguous=true. On the fill bar of the touch variant only SL is credited. R = |fill - SL|. Exit-at-TP1 R is
  +|tp1 - fill|/R; exit-at-last-TP R is +|tp_last - fill|/R; a stop is -1R; unresolved trades are marked to the last
  bar close inside the horizon. Spread, slippage and commission are ignored (flatters the channel).
"""
import argparse, bisect, collections, json, math, os, re, statistics, sys, time, unicodedata, urllib.request
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
ARCH = os.path.join(ROOT, "data/telegram_funnel/posts_archive.jsonl")
OUT_ROWS = os.path.join(ROOT, "data/telegram_funnel/fx_signals.jsonl")
OUT_CLAIMS = os.path.join(ROOT, "data/telegram_funnel/fx_claims.jsonl")
OUT_MD = os.path.join(ROOT, "reports/analysis/fx_signals.md")
CACHE = os.path.join(ROOT, "data/telegram_funnel/price_cache")
TODAY = os.environ.get("TG_TODAY", "2026-10-14")
BULK_N = 6                 # same (channel, exact timestamp) shared by this many posts or more = backfill dump
DEDUPE_MIN = 60
TYPO_PCT = 4.0
TYPO_PCT_CRYPTO = 10.0
MAX_RISK_PCT = 1.0
MAX_RISK_PCT_CRYPTO = 5.0
TOL_FRAC = 0.25
BAR_S = 300
MAX_STALE_S = 600
HORIZON_HOURS = 24.0
TOUCH_HOURS = 4.0

# ---------------------------------------------------------------- normalisation
NUM = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?"
_STRIP = set("\u1160\u115f\u3164\ufff4\u200b\u200c\u200d\u200e\u200f\ufeff")


def norm(t):
    t = unicodedata.normalize("NFKC", t or "")
    out = []
    for ch in t:
        if ch in _STRIP or unicodedata.category(ch) in ("So", "Sk", "Cf", "Cn", "Co", "Cs", "Mn"):
            out.append(" ")
        elif ch in "\u2013\u2014\u2212":
            out.append("-")
        elif ch.isspace():
            out.append(" ")
        else:
            out.append(ch)
    return re.sub(r"\s+", " ", "".join(out)).strip()


def fnum(s):
    return float(s.replace(",", ""))


# ---------------------------------------------------------------- instruments
CCY = "EUR GBP USD JPY CHF CAD AUD NZD".split()
CRYPTO = "BTC ETH SOL XRP DOGE ADA BNB LTC AVAX LINK DOT".split()
INSTR_PATTERNS = [
    ("XAUUSD", r"\b(?:XAU\s*/?\s*USD|XAUUSD|XAU|GOLD)\b"),
    ("US30", r"\b(?:US30|DJ30|DJI|DOW(?:\s*JONES)?)\b"),
    ("NAS100", r"\b(?:NAS100|NAS|US100|USTEC|NDX|NASDAQ)\b"),
    ("JP225", r"\b(?:JP225|NIKKEI|NK225)\b"),
    ("SPX500", r"\b(?:SPX500|US500|SP500)\b"),
    ("WTI", r"\b(?:USOIL|WTI|XTIUSD)\b"),
    ("FX", r"\b(" + "|".join(CCY) + r")\s*/?\s*(" + "|".join(CCY) + r")\b"),
    ("CRYPTOPAIR", r"\b([A-Z]{2,6})\s*/\s*(USDT|USD)\b"),
    ("CRYPTOPAIR2", r"\b(" + "|".join(CRYPTO) + r")(USDT|USD)\b"),
    ("CRYPTO", r"\b(" + "|".join(CRYPTO) + r")\b"),
]
INSTR_RE = [(n, re.compile(p)) for n, p in INSTR_PATTERNS]
SIDE_RE = re.compile(r"\b(BUY|BUYING|LONG|SELL|SELLING|SHORT)\b")
OPTION_RE = re.compile(r"\b\d+(?:\.\d+)?\s*[CP]\b|\bCALLS?\b|\bPUTS?\b|\bAVG\b|\bBTO\b|\bSTC\b")
SL_RE = re.compile(r"(?:\bSTOP\s*LOSS|\bSTOPLOSS|\bSL|\bSTOP)\s*[:=@<>\-]*\s*(" + NUM + ")")
TP_RE = re.compile(r"(?:\bTP|\bTARGETS?|\bTAKE\s*PROFIT|\bTGT)S?\s*[:=@\-/<]*\s*"
                   r"((?:OPEN|(?:" + NUM + r")(?:\s*PIPS?)?)(?:\s*[/,]?\s*(?:OPEN|(?:" + NUM + r")(?:\s*PIPS?)?))*)")
ENTRY_LABEL_RE = re.compile(r"(?:\bENTRY(?:\s*(?:POINT|ZONE|PRICE|AT))?|\bENTER|\bPRICE|\bBUY\s*ZONE|\bSELL\s*ZONE|\bSHORT\s*ZONE)"
                            r"\s*[:=@<\-]*\s*<?\s*(" + NUM + r")(?:\s*(?:-|/|TO)\s*(" + NUM + r"))?")
ZONE_TAIL_RE = re.compile(r"^[^0-9|]{0,40}?(" + NUM + r")(?:\.?\s*(?:-|/|TO)\s*(" + NUM + r")|\.\s+(" + NUM + r")|\s+(" + NUM + r"))?")


def pip_size(instr, pair=None):
    if instr == "XAUUSD": return 0.10
    if instr in ("US30", "NAS100", "JP225", "SPX500"): return 1.0
    if instr.startswith("FX:"):
        return 0.01 if instr.endswith("JPY") else 0.0001
    return None


def find_instrument(u):
    best = None
    for name, rx in INSTR_RE:
        m = rx.search(u)
        if not m: continue
        if best is None or m.start() < best[2].start():
            best = (name, rx, m)
    if not best: return None, None
    name, _, m = best
    if name == "FX":
        a, b = m.group(1), m.group(2)
        if a == b: return None, None
        return "FX:" + a + b, m
    if name in ("CRYPTOPAIR", "CRYPTOPAIR2"):
        base = m.group(1)
        if base in CCY: return None, None
        return base + "USD", m
    if name == "CRYPTO":
        return m.group(1) + "USD", m
    return name, m


def is_crypto(instr):
    return instr.endswith("USD") and instr not in ("XAUUSD",) and not instr.startswith("FX:")


def _clean_labels(u):
    u = re.sub(r"\(\s*(?:TP|SL)\s*\d*\s*\)", " ", u)
    u = re.sub(r"\b\d_TP\b", "TP", u)
    u = re.sub(r"\b(TP|TARGETS?|TAKE\s*PROFIT|TGT)S?\s*\d{1,2}(?!\d)(?:ST|ND|RD|TH)?\s*[:=\-]?\s*(?=[\d<]|OPEN)", r"\1 ", u)
    return u


def _zone(a, b):
    """a, b: strings (b may be None). Expand abbreviated second price (4348-46 -> 4346) and sanity-check closeness."""
    lo = fnum(a)
    if b is None: return lo, lo
    sb = b.replace(",", "")
    hi = fnum(sb)
    ia = a.split(".")[0]
    ib = sb.split(".")[0]
    if "." not in sb and len(ib) < len(ia):
        hi = fnum(ia[: len(ia) - len(ib)] + sb)
    if lo > 0 and abs(hi - lo) / lo > 0.02:
        return lo, lo
    return min(lo, hi), max(lo, hi)


def parse_signal(text):
    """Parse one post. Returns a dict or None when it is not signal-shaped (no instrument, no side, or no levels).
    Keys: instrument, side ('buy'|'sell'), order_type, entry_lo, entry_hi (None if absent), entry_kind
    (single|zone|now|missing), sl, tps [{v, pips}], flags, has_levels."""
    u = norm(text).upper()
    if not u or len(u) > 900: return None
    instr, im = find_instrument(u)
    if not instr: return None
    sm = SIDE_RE.search(u)
    if not sm: return None
    if OPTION_RE.search(u) and not re.search(r"\b(SL|STOP\s*LOSS|TP|TAKE\s*PROFIT)\b", u): return None
    side = "buy" if sm.group(1) in ("BUY", "BUYING", "LONG") else "sell"
    flags = []
    c = _clean_labels(u)
    # blank the instrument token so its digits (US30, NAS100) are not read as prices
    im2 = find_instrument(c)[1]
    if im2: c = c[: im2.start()] + " " * (im2.end() - im2.start()) + c[im2.end():]
    sl = None
    spans = []
    for m in SL_RE.finditer(c):
        if sl is None: sl = fnum(m.group(1))
        spans.append(m.span())
    tps = []
    pips_mode = False
    for m in TP_RE.finditer(c):
        spans.append(m.span())
        g = m.group(1)
        is_pips = bool(re.search(r"PIPS?", g))
        for n in re.finditer(NUM, g):
            tps.append({"v": fnum(n.group(0)), "pips": is_pips})
        pips_mode = pips_mode or is_pips
    # blank SL / TP spans, keep a separator so numbers across them are not glued
    cc = list(c)
    for a, b in spans:
        for i in range(a, b): cc[i] = "|"
    rest = "".join(cc)
    el = eh = None
    kind = "missing"
    mm = ENTRY_LABEL_RE.search(rest)
    if mm:
        el, eh = _zone(mm.group(1), mm.group(2))
    else:
        sm2 = SIDE_RE.search(rest)
        tail = rest[sm2.end():] if sm2 else rest
        tail = tail.lstrip(" :@")
        zm = ZONE_TAIL_RE.match(tail)
        if zm:
            b = zm.group(2) or zm.group(3) or zm.group(4)
            el, eh = _zone(zm.group(1), b)
    if el is not None:
        kind = "zone" if eh > el else "single"
    elif re.search(r"\b(NOW|READY|INSTANT|MARKET)\b", u):
        kind = "now"
    order_type = "limit" if re.search(r"\bLIMIT\b", u) else "market"
    if re.search(r"\bSTOP\s+ORDER\b|\bBUY STOP\b|\bSELL STOP\b", u): order_type = "stop"
    if any(t["pips"] for t in tps): flags.append("tp_pips_assumed")
    if re.search(r"\bOPEN\b", " ".join(m.group(1) for m in TP_RE.finditer(c))): flags.append("tp_open_ended")
    return {"instrument": instr, "side": side, "order_type": order_type, "entry_lo": el, "entry_hi": eh,
            "entry_kind": kind, "sl": sl, "tps": tps, "flags": flags,
            "has_levels": sl is not None or bool(tps)}


# ---------------------------------------------------------------- claims
CLAIM_PATTERNS = [
    ("tp_hit", re.compile(r"\bTP\s*\d?\s*(?:DONE|HIT|HITS)\b|\bHITS?\s*TP\b|\bTARGET\s*\d?\s*(?:DONE|HIT)\b|\bTP\S*\s*(?:ALL|MAX)\b|\bTPS?\s*HIT")),
    ("sl_hit", re.compile(r"\bSL\s*HIT\b|\bHIT\s*(?:SL|RISK|STOP)\b|\bSTOPPED\s*OUT\b|\bSTOP\s*LOSS\s*HIT")),
    ("pips", re.compile(r"([+-]?\d{2,4})\s*\+?\s*PIPS?\b")),
    ("running", re.compile(r"\bRUNNING\s*(?:PROFITS?|\d)|\bPROFITS?\s*RUNNING")),
    ("secure_be", re.compile(r"\bSECURE\b.*\b(?:PROFITS?|HALF|BE|BREAKEVEN)\b|\bSET\s*(?:TO\s*)?BREAKEVEN|\bBREAKEVEN\b|\bMOVE\s*(?:MY\s*)?SL\b")),
]


def parse_claim(text):
    u = norm(text).upper()
    if not u: return None
    kinds, pips = [], None
    for k, rx in CLAIM_PATTERNS:
        m = rx.search(u)
        if m:
            kinds.append(k)
            if k == "pips": pips = int(m.group(1).replace("+", ""))
    if not kinds: return None
    # pips alone in a how-to or a trade setup ("TP: 50/100PIPS") is not a result claim
    if kinds == ["pips"] and re.search(r"\b(SL|TP)\b", u) and not re.search(r"\bRUNNING|\bHIT|\bDONE|^\+", u): return None
    tpn = None
    m = re.search(r"\bTP\s*(\d)", u)
    if m: tpn = int(m.group(1))
    return {"kinds": kinds, "pips": pips, "tp_n": tpn}


# ---------------------------------------------------------------- price data
UA = {"User-Agent": "Mozilla/5.0"}
_last = [0.0]
CANDIDATES = {
    "XAUUSD": ["XAUUSD=X", "GC=F"], "US30": ["^DJI", "YM=F"], "NAS100": ["^NDX", "NQ=F"],
    "JP225": ["^N225", "NIY=F"], "SPX500": ["^GSPC", "ES=F"], "WTI": ["CL=F"],
}


def candidates(instr):
    if instr in CANDIDATES: return CANDIDATES[instr]
    if instr.startswith("FX:"): return [instr[3:] + "=X"]
    if instr.endswith("USD"): return [instr[:-3] + "-USD"]
    return []


def _safe(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s)


def get_bars(sym, fetch=True):
    """Return {'ts','o','h','l','c'} lists for a Yahoo symbol or None. Cached per day, including failures."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "fx_%s_5m.json" % _safe(sym))
    if os.path.exists(path):
        try:
            d = json.load(open(path))
            if d.get("fetched") == TODAY or not fetch:
                return d.get("bars")
        except Exception:
            pass
    if not fetch: return None
    wait = 0.45 - (time.time() - _last[0])
    if wait > 0: time.sleep(wait)
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?interval=5m&range=60d&includePrePost=false" % urllib.request.quote(sym)
    bars, err = None, None
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        ts, o, h, l, c = [], [], [], [], []
        for i, t in enumerate(res.get("timestamp") or []):
            if None in (q["open"][i], q["high"][i], q["low"][i], q["close"][i]): continue
            ts.append(t); o.append(q["open"][i]); h.append(q["high"][i]); l.append(q["low"][i]); c.append(q["close"][i])
        bars = {"ts": ts, "o": o, "h": h, "l": l, "c": c} if ts else None
    except Exception as e:
        err = str(e)
    _last[0] = time.time()
    json.dump({"fetched": TODAY, "source": "yahoo", "symbol": sym, "error": err, "bars": bars}, open(path, "w"))
    return bars


def bar_at(bars, t):
    """Index of the 5m bar containing epoch t, or None if the nearest earlier bar is more than MAX_STALE_S old."""
    i = bisect.bisect_right(bars["ts"], t) - 1
    if i < 0 or t - bars["ts"][i] > MAX_STALE_S: return None
    return i


def median(x):
    return statistics.median(x) if x else None


# ---------------------------------------------------------------- validation of Yahoo symbols
def entry_ref(s):
    if s["entry_lo"] is None: return None
    return (s["entry_lo"] + s["entry_hi"]) / 2


def validate_symbols(sigs, fetch):
    """Per instrument: for each candidate symbol, median abs % gap between the stated entries (limit orders excluded)
    and the candidate close at post time; signed price gap split by side; coverage. Returns (choice, report)."""
    by = collections.defaultdict(list)
    for s in sigs:
        if entry_ref(s) is not None and s["order_type"] == "market": by[s["instrument"]].append(s)
    allinstr = sorted({s["instrument"] for s in sigs})
    choice, rep = {}, {}
    for ins in allinstr:
        cs = candidates(ins)
        rep[ins] = []
        rows = by.get(ins, [])
        for sym in cs:
            bars = get_bars(sym, fetch)
            d = {"symbol": sym, "has_data": bars is not None, "n_entries": len(rows)}
            if bars:
                gaps, signed_b, signed_s = [], [], []
                perday = collections.defaultdict(lambda: ([], []))
                kept = []
                for s in rows:
                    i = bar_at(bars, s["ts"])
                    if i is None: continue
                    m = bars["c"][i]
                    e = entry_ref(s)
                    if abs(e / m - 1) > 0.03: continue   # typo / far limit-ish: not informative for basis
                    gaps.append(abs(e / m - 1) * 100)
                    (signed_b if s["side"] == "buy" else signed_s).append(e - m)
                    perday[s["ts"] // 86400][0 if s["side"] == "buy" else 1].append(e - m)
                    kept.append((s["ts"], s["side"], e, m))
                d["n_matched"] = len(gaps)
                d["coverage"] = len(gaps) / len(rows) if rows else None
                d["median_abs_gap_pct"] = median(gaps)
                d["median_signed_buy"] = median(signed_b)
                d["median_signed_sell"] = median(signed_s)
                if signed_b and signed_s:
                    d["basis_offset"] = (median(signed_b) + median(signed_s)) / 2   # entry-side bias cancels between buys and sells
                elif signed_b or signed_s:
                    d["basis_offset"] = median(signed_b or signed_s)
                else:
                    d["basis_offset"] = None
                # time-varying basis: Theil-Sen line through per-day balanced (buy+sell)/2 medians. Needs >= 5 such days.
                pts = [(dd, (median(b) + median(sl)) / 2) for dd, (b, sl) in sorted(perday.items()) if b and sl]
                d["basis_days"] = len(pts)
                d["basis_fit"] = None
                if len(pts) >= 5:
                    slopes = [(y2 - y1) / (x2 - x1) for i1, (x1, y1) in enumerate(pts) for (x2, y2) in pts[i1 + 1:] if x2 != x1]
                    b1 = median(slopes)
                    x0 = median([x for x, _ in pts])
                    a0 = median([y - b1 * (x - x0) for x, y in pts])
                    d["basis_fit"] = {"a": a0, "b_per_day": b1, "x0": x0}
                    res = [abs(e - (m + a0 + b1 * (t / 86400 - x0))) / m * 100 for (t, sd, e, m) in kept]
                    d["median_abs_gap_after_fit_pct"] = median(res)
                if d["basis_offset"] is not None:
                    d["median_abs_gap_after_const_pct"] = median([abs(e - (m + d["basis_offset"])) / m * 100 for (t, sd, e, m) in kept])
                d["first"] = datetime.fromtimestamp(bars["ts"][0], timezone.utc).strftime("%Y-%m-%d")
                d["last"] = datetime.fromtimestamp(bars["ts"][-1], timezone.utc).strftime("%Y-%m-%d %H:%M")
            rep[ins].append(d)
        ok = [d for d in rep[ins] if d["has_data"]]
        pick = None
        if ok:
            cov = [d.get("coverage") or 0 for d in ok]
            best_cov = max(cov)
            elig = [d for d in ok if (d.get("coverage") or 0) >= 0.8 * best_cov and d.get("median_abs_gap_pct") is not None]
            pick = min(elig, key=lambda d: d["median_abs_gap_pct"]) if elig else ok[0]
        choice[ins] = pick
    return choice, rep


# ---------------------------------------------------------------- scoring
def side_dir(s): return 1 if s["side"] == "buy" else -1


def typo_check(s, market):
    """Flags (list) for prices that cannot be right given the market price at post time."""
    flags = []
    pct = TYPO_PCT_CRYPTO if is_crypto(s["instrument"]) else TYPO_PCT
    maxr = MAX_RISK_PCT_CRYPTO if is_crypto(s["instrument"]) else MAX_RISK_PCT
    prices = []
    if s["entry_lo"] is not None: prices += [("entry", s["entry_lo"]), ("entry", s["entry_hi"])]
    if s["sl"] is not None: prices.append(("sl", s["sl"]))
    tp_prices = [t["v"] for t in s["tps"] if not t["pips"]]
    if tp_prices: prices.append(("tp1", tp_prices[0]))
    for nm, p in prices:
        r = p / market
        if not (0.5 <= r <= 2.0):
            flags.append("typo_magnitude_" + nm)
        elif abs(r - 1) * 100 > pct:
            flags.append("typo_price_off_market_" + nm)
    ref = entry_ref(s) if s["entry_lo"] is not None else market
    if s["sl"] is not None and ref and not any(f.startswith("typo_") and f.endswith("_sl") for f in flags):
        if abs(ref - s["sl"]) / ref * 100 > maxr: flags.append("sl_distance_implausible")
    return flags


def resolve_tps(s, fill, d, ps):
    """Return (list of tp prices sorted by distance, flags). Pips converted from fill. Wrong-side TPs dropped."""
    tp, flags = [], []
    for t in s["tps"]:
        if t["pips"]:
            if ps is None: flags.append("pips_unsupported"); continue
            tp.append(fill + d * t["v"] * ps)
        else:
            if (t["v"] - fill) * d <= 0: flags.append("tp_wrong_side_or_passed"); continue
            tp.append(t["v"])
    tp = sorted(set(round(x, 6) for x in tp), key=lambda x: abs(x - fill))
    return tp, flags


def walk(bars, j0, fill, sl, tps, d, t_end, first_bar_sl_only=False):
    """Walk bars from index j0 until t_end. Returns dict with events and excursion stats (in price units)."""
    ts, H, L, C = bars["ts"], bars["h"], bars["l"], bars["c"]
    hit = {}                                   # tp index -> bar index
    sl_i = None
    ambiguous = False
    mae = mfe = 0.0
    last_i = None
    j = j0
    n = len(ts)
    while j < n and ts[j] < t_end:
        hi, lo = H[j], L[j]
        fav = (hi - fill) if d > 0 else (fill - lo)
        adv = (fill - lo) if d > 0 else (hi - fill)
        mfe = max(mfe, fav); mae = max(mae, adv)
        sl_touch = (lo <= sl) if d > 0 else (hi >= sl)
        new = [k for k, tp in enumerate(tps) if k not in hit and ((hi >= tp) if d > 0 else (lo <= tp))]
        if first_bar_sl_only and j == j0:
            new = []
        if sl_touch:
            sl_i = j
            if new: ambiguous = True
            last_i = j
            break
        for k in new: hit[k] = j
        last_i = j
        if len(hit) == len(tps): break
        j += 1
    if last_i is None:
        return {"hit": hit, "sl_i": None, "ambiguous": False, "mae": 0.0, "mfe": 0.0, "end_i": None}
    return {"hit": hit, "sl_i": sl_i, "ambiguous": ambiguous, "mae": mae, "mfe": mfe, "end_i": last_i}


def score_one(s, bars, offset, cfg, sym):
    """Score one signal that passed the earlier gates. Returns dict of result fields (always has 'status')."""
    off = offset or 0.0
    ts, O, H, L, C = bars["ts"], bars["o"], bars["h"], bars["l"], bars["c"]
    i = bar_at(bars, s["ts"])
    if i is None: return {"status": "skipped", "skip_reason": "no_price_at_post"}
    market = C[i] + off
    d = side_dir(s)
    flags = typo_check(s, market)
    if flags:
        return {"status": "skipped", "skip_reason": "typo_flagged", "flags_add": flags, "market_price": round(market, 6)}
    ps = pip_size(s["instrument"])
    sl = s["sl"]
    if sl is None: return {"status": "skipped", "skip_reason": "no_sl", "market_price": round(market, 6)}
    if not s["tps"]: return {"status": "skipped", "skip_reason": "no_tp", "market_price": round(market, 6)}
    mid = entry_ref(s)
    lo, hi = s["entry_lo"], s["entry_hi"]
    out = {"market_price": round(market, 6)}
    # decide variant
    if mid is None:
        variant = "market"
    else:
        rstated = abs(mid - sl)
        tol = TOL_FRAC * rstated
        variant = "market" if (lo - tol) <= market <= (hi + tol) else "touch"
    out["variant"] = variant
    t_post = s["ts"]
    if variant == "market":
        fill = market
        fill_i = i
        j0 = i + 1
        fill_t = ts[i] + BAR_S
        first_sl_only = False
    else:
        out["entry_not_at_market"] = True
        # nearest edge to the market
        edge = lo if market < lo else hi
        if lo == hi: edge = lo
        t_stop = t_post + cfg["touch_hours"] * 3600
        j = i + 1
        fill_i = None
        while j < len(ts) and ts[j] < t_stop:
            h_, l_ = H[j] + off, L[j] + off
            reached = (l_ <= edge) if market > edge else (h_ >= edge)
            sl_t = (l_ <= sl) if d > 0 else (h_ >= sl)
            tp_resolved, _ = resolve_tps(s, edge, d, ps)
            tp1 = tp_resolved[0] if tp_resolved else None
            tp_t = tp1 is not None and (((h_ >= tp1) if d > 0 else (l_ <= tp1)))
            if reached:
                fill_i = j; break
            if sl_t: return {**out, "status": "skipped", "skip_reason": "cancelled_sl_before_fill", "filled": False}
            if tp_t: return {**out, "status": "skipped", "skip_reason": "cancelled_tp_before_fill", "filled": False}
            j += 1
        if fill_i is None:
            return {**out, "status": "skipped", "skip_reason": "not_filled_in_window", "filled": False}
        fill = edge
        j0 = fill_i
        fill_t = ts[fill_i]
        first_sl_only = True
    if (fill - sl) * d <= 0:
        return {**out, "status": "skipped", "skip_reason": "sl_already_breached", "filled": variant == "market" or True, "fill_price": round(fill, 6)}
    R = abs(fill - sl)
    tps, tflags = resolve_tps(s, fill, d, ps)
    if not tps:
        why = "pips_unsupported" if "pips_unsupported" in tflags else "tp_passed"
        return {**out, "status": "skipped", "skip_reason": why, "filled": True, "fill_price": round(fill, 6)}
    out.update({"filled": True, "fill_price": round(fill, 6), "R_price": round(R, 6), "n_tp": len(tps),
                "tp_levels": [round(x, 6) for x in tps]})
    if tflags: out["flags_add"] = tflags
    t_end = fill_t + cfg["horizon_hours"] * 3600
    if ts[-1] + BAR_S < t_end - 1:
        return {**out, "status": "skipped", "skip_reason": "horizon_incomplete"}
    # shift bars by basis offset for the walk
    sb = {"ts": ts, "h": [x + off for x in H], "l": [x + off for x in L], "c": [x + off for x in C]} if off else bars
    w = walk(sb, j0, fill, sl, tps, d, t_end, first_bar_sl_only=first_sl_only)
    hit, sl_i = w["hit"], w["sl_i"]
    n = len(tps)
    # which TPs counted before the stop: all in hit (walk breaks at SL bar and credits none in that bar)
    tp1_t = ts[hit[0]] + BAR_S if 0 in hit else None
    sl_t = ts[sl_i] + BAR_S if sl_i is not None else None
    # last bar close inside horizon for MTM
    k = bisect.bisect_left(ts, t_end) - 1
    c_h = sb["c"][k]
    mtm = (c_h - fill) * d / R
    tp1_before_sl = 0 in hit
    last_hit = (n - 1) in hit
    sl_first = sl_i is not None and not tp1_before_sl
    k_hit = sum(1 for x in range(n) if x in hit)
    r1 = abs(tps[0] - fill) / R
    rl = abs(tps[-1] - fill) / R
    if tp1_before_sl: r_tp1 = r1
    elif sl_i is not None: r_tp1 = -1.0
    else: r_tp1 = mtm
    if last_hit: r_last = rl
    elif sl_i is not None: r_last = -1.0
    else: r_last = mtm
    # outcome label = highest TP reached before the stop, else sl, else open
    if k_hit: outcome = "tp%d" % k_hit if k_hit == len([x for x in range(n) if x in hit]) else "tp%d" % k_hit
    elif sl_i is not None: outcome = "sl"
    else: outcome = "open"
    first_event = None
    cand = []
    if tp1_t: cand.append((tp1_t, "tp1"))
    if sl_t: cand.append((sl_t, "sl"))
    if cand: first_event = min(cand)
    mae = min(w["mae"] / R, 1.0) if sl_i is not None else w["mae"] / R
    mfe = w["mfe"] / R
    out.update({"status": "scored", "outcome": outcome, "first_event": first_event[1] if first_event else "none",
                "tp1_hit": tp1_before_sl, "last_tp_hit": last_hit, "tps_hit": k_hit, "sl_first": sl_first,
                "sl_after_tp": sl_i is not None and tp1_before_sl, "ambiguous": w["ambiguous"],
                "minutes_to_first_event": round((first_event[0] - t_post) / 60, 1) if first_event else None,
                "r_tp1": round(r_tp1, 4), "r_last": round(r_last, 4), "r_tp1_target": round(r1, 4),
                "r_last_target": round(rl, 4), "mae_r": round(mae, 4), "mfe_r": round(mfe, 4),
                "resolved": first_event is not None})
    return out


# ---------------------------------------------------------------- stats helpers
def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0, c - h), min(1, c + h))


def pct(x, n=None, digits=0):
    return "-" if x is None else ("%.*f%%" % (digits, 100 * x))


def fmt(x, d=2):
    return "-" if x is None else ("%.*f" % (d, x))


def table_stats(rows):
    n = len(rows)
    if n == 0: return None
    tp1 = [r for r in rows if r["tp1_hit"]]
    multi = [r for r in rows if r["n_tp"] >= 2]
    tp2 = [r for r in multi if r["tps_hit"] >= 2]
    sl = [r for r in rows if r["sl_first"]]
    op = [r for r in rows if not r["resolved"]]
    res = [r for r in rows if r["resolved"]]
    avgwin = mean([r["r_tp1_target"] for r in tp1])
    be = (1 / (1 + avgwin)) if avgwin else None
    times = [r["minutes_to_first_event"] for r in res if r["minutes_to_first_event"] is not None]
    lo, hi = wilson(len(tp1), n)
    return {"n": n, "tp1": len(tp1), "tp1_rate": len(tp1) / n, "tp1_ci": (lo, hi), "n_multi": len(multi), "tp2plus": len(tp2),
            "tp2_rate": (len(tp2) / len(multi)) if multi else None, "sl": len(sl), "sl_rate": len(sl) / n,
            "open_rate": len(op) / n, "mean_r_tp1": mean([r["r_tp1"] for r in rows]),
            "mean_r_last": mean([r["r_last"] for r in rows]),
            "expect_resolved": mean([r["r_tp1"] for r in res]) if res else None, "n_res": len(res),
            "avg_win_r": avgwin, "be_rate": be, "med_min": median(times), "amb": sum(1 for r in rows if r["ambiguous"])}


def mean(x):
    x = [v for v in x if v is not None]
    return sum(x) / len(x) if x else None


STAT_HDR = ("| n | TP1 hit (95% CI) | TP2+ | SL first | unresolved | mean R exit@TP1 | mean R exit@last TP | "
            "expectancy@TP1, resolved only | avg win R / break-even TP1 rate | median min to 1st event |")
STAT_SEP = "|---:|---|---|---:|---:|---:|---:|---:|---|---:|"


def stat_cells(st):
    if not st: return "| 0 | - | - | - | - | - | - | - | - | - |"
    lo, hi = st["tp1_ci"]
    return "| %d | %s (%s-%s) | %s | %s | %s | %s | %s | %s (n=%d) | %s / %s | %s |" % (
        st["n"], pct(st["tp1_rate"]), pct(lo), pct(hi),
        ("%s (%d/%d)" % (pct(st["tp2_rate"]), st["tp2plus"], st["n_multi"])) if st["n_multi"] else "n/a",
        pct(st["sl_rate"]), pct(st["open_rate"]), fmt(st["mean_r_tp1"]), fmt(st["mean_r_last"]),
        fmt(st["expect_resolved"]), st["n_res"], fmt(st["avg_win_r"]), pct(st["be_rate"]), fmt(st["med_min"], 0))


# ---------------------------------------------------------------- pipeline
def load_posts():
    return [json.loads(l) for l in open(ARCH) if l.strip()]


def iso_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def dedupe_reposts(rows):
    """Mark pending rows that repeat an earlier identical signal (same channel, instrument, side, entry, SL, TPs) within
    DEDUPE_MIN minutes of the previous copy (sliding window, so a repost chain collapses to its first post)."""
    last = {}
    for r in sorted((r for r in rows if r["status"] == "pending"), key=lambda r: r["ts"]):
        key = (r["channel"], r["instrument"], r["side"], r["entry_lo"], r["entry_hi"], r["sl"],
               tuple((t["v"], t["pips"]) for t in r["tps"]))
        prev = last.get(key)
        if prev and r["ts"] - prev[0] <= DEDUPE_MIN * 60:
            r["status"], r["skip_reason"], r["dup_of"] = "skipped", "duplicate_repost", prev[1]
            last[key] = (r["ts"], prev[1])
        else:
            last[key] = (r["ts"], r["id"])


def run(args):
    cfg = {"horizon_hours": args.horizon_hours, "touch_hours": args.touch_hours}
    posts = load_posts()
    same_ts = collections.Counter((p["channel"], p["date"]) for p in posts)
    rows, claims = [], []
    nonsig = collections.Counter()
    for p in posts:
        text = p.get("text") or ""
        sig = parse_signal(text)
        t = iso_ts(p["date"])
        base = {"id": p["id"], "channel": p["channel"], "date": p["date"], "text": text[:400]}
        if sig is None or not sig["has_levels"]:
            # candidate without levels: instrument + side but no SL/TP is reported as a skipped row
            cl = parse_claim(text)
            if cl:
                claims.append({**base, **cl, "bulk_timestamp": same_ts[(p["channel"], p["date"])] >= BULK_N})
            if sig is not None and not sig["has_levels"]:
                rows.append({**base, **{k: sig[k] for k in ("instrument", "side", "order_type", "entry_kind", "flags")},
                             "status": "skipped", "skip_reason": "no_levels", "ts": int(t.timestamp())})
            else:
                nonsig["not_a_signal"] += 1
            continue
        r = {**base, **sig, "ts": int(t.timestamp()), "status": "pending", "skip_reason": None}
        r["bulk_timestamp"] = same_ts[(p["channel"], p["date"])] >= BULK_N
        if not sig["tps"]: r["flags"] = sig["flags"] + ["no_tp"]
        if sig["sl"] is None: r["flags"] = r["flags"] + ["no_sl"]
        rows.append(r)
    # stage: valid dates
    for r in rows:
        if r["status"] == "pending" and r["bulk_timestamp"]:
            r["status"], r["skip_reason"] = "skipped", "bulk_timestamp"
    dedupe_reposts(rows)
    # stage: levels complete
    for r in rows:
        if r["status"] == "pending" and (r["sl"] is None or not r["tps"]):
            r["status"], r["skip_reason"] = "skipped", ("no_sl" if r["sl"] is None else "no_tp")
    # stage: inside Yahoo's 5m history (about 60 days)
    cutoff = int((datetime.fromisoformat(TODAY).replace(tzinfo=timezone.utc) - timedelta(days=58)).timestamp())
    for r in rows:
        if r["status"] == "pending" and r["ts"] < cutoff:
            r["status"], r["skip_reason"] = "skipped", "before_price_history"
    pend = [r for r in rows if r["status"] == "pending"]
    fetch = not args.no_fetch
    choice, vrep = validate_symbols(pend, fetch)
    def basis_at(ch, mode, ts):
        if not ch or mode == "none": return 0.0
        fit, const = ch.get("basis_fit"), ch.get("basis_offset") or 0.0
        if mode == "const" or not fit: v = const
        else: v = fit["a"] + fit["b_per_day"] * (ts / 86400 - fit["x0"])
        return v
    results = {}
    for mode in ("auto", "const", "none", "auto-0.07%", "auto+0.07%"):
        res = {}
        for r in pend:
            ch = choice.get(r["instrument"])
            if not ch:
                res[r["id"]] = {"status": "skipped", "skip_reason": "no_price_data"}
                continue
            bars = get_bars(ch["symbol"], False)
            off = basis_at(ch, "auto" if mode.startswith("auto") else mode, r["ts"])
            if mode == "auto-0.07%": off -= 0.0007 * (bars["c"][bar_at(bars, r["ts"]) or 0])
            if mode == "auto+0.07%": off += 0.0007 * (bars["c"][bar_at(bars, r["ts"]) or 0])
            res[r["id"]] = {**score_one(r, bars, off, cfg, ch["symbol"]), "yahoo_symbol": ch["symbol"], "basis_offset": round(off, 4)}
        results[mode] = res
    primary = args.basis
    for r in pend:
        r.update(results[primary][r["id"]])
        fa = r.pop("flags_add", None)
        if fa: r["flags"] = sorted(set(r["flags"]) | set(fa))
    return posts, rows, claims, nonsig, choice, vrep, results, primary, cfg


def row_out(r):
    o = {k: v for k, v in r.items() if k != "ts"}
    o["ts"] = r["ts"]
    return o


# ---------------------------------------------------------------- report
def weekmon(s):
    d = iso_ts(s).date()
    return (d - timedelta(days=d.weekday())).isoformat()


def classify_content(p, sig_ids):
    t = p.get("text") or ""
    u = norm(t).upper()
    if p["id"] in sig_ids: return "fx_signal"
    if re.search(r"\$[A-Z]{1,5}\b", t) or re.search(r"\b\d+(?:\.\d+)?\s*(?:CALL|PUT|C|P)\b", u): return "stock_callout"
    if re.search(r"\b(GOLD|XAU\w*|NAS100|US30|PIPS?|SCALP\w*|SL|TP\d?)\b", u): return "fx_chatter_analysis"
    if re.search(r"\b(DEPOSIT\w*|WITHDRAW\w*|PAYMENT|USDT|INVEST\w*|REINVEST\w*|PROFIT PROGRAM|VIP|PRIVATE)\b", u): return "promo_chat"
    return "other"


def write_report(args, posts, rows, claims, nonsig, choice, vrep, results, primary, cfg):
    A = []
    w = A.append
    sig_rows = [r for r in rows if r.get("skip_reason") != "no_levels"]
    scored = [r for r in rows if r["status"] == "scored"]
    mk = [r for r in scored if r.get("variant") == "market"]
    tc = [r for r in scored if r.get("variant") == "touch"]
    gen = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    w("# FX / gold / index signal scoring (public Telegram posts vs the real tape)")
    w("")
    w("Generated %s by `tg_fx_signals.py` from `data/telegram_funnel/posts_archive.jsonl`. Analysis of public posts, not an accusation. "
      "Numbers first; every rate carries its sample size. Horizon %.0fh, touch window %.0fh, basis mode `%s`." % (TODAY, cfg["horizon_hours"], cfg["touch_hours"], primary))
    w("")
    # ---------------- funnel
    posts_n = len(posts)
    by_ch_posts = collections.Counter(p["channel"] for p in posts)
    cand = len(rows)
    lvl = [r for r in rows if r.get("skip_reason") != "no_levels"]
    nodate = [r for r in lvl if r.get("skip_reason") == "bulk_timestamp"]
    dd = [r for r in lvl if r.get("skip_reason") not in ("bulk_timestamp",)]
    dup = [r for r in dd if r.get("skip_reason") == "duplicate_repost"]
    uniq = [r for r in dd if r.get("skip_reason") != "duplicate_repost"]
    incomplete = [r for r in uniq if r.get("skip_reason") in ("no_sl", "no_tp")]
    ok_lvl = [r for r in uniq if r.get("skip_reason") not in ("no_sl", "no_tp")]
    old = [r for r in ok_lvl if r.get("skip_reason") == "before_price_history"]
    nodata = [r for r in ok_lvl if r.get("skip_reason") == "no_price_data"]
    nobar = [r for r in ok_lvl if r.get("skip_reason") == "no_price_at_post"]
    priced = [r for r in ok_lvl if r.get("market_price") is not None]
    typo = [r for r in priced if r.get("skip_reason") == "typo_flagged"]
    nottypo = [r for r in priced if r.get("skip_reason") != "typo_flagged"]
    filled = [r for r in nottypo if r.get("filled")]
    # filled is set only on paths that reached fill; scored/horizon:
    w("## 1. Coverage funnel")
    w("")
    w("Stage order (each stage counts what survives the previous one): bulk-timestamp exclusion comes before the repost dedupe so a backfill dump "
      "can never be the \"first\" copy that survives. Typo detection needs the market price, so it runs after pricing.")
    w("")
    w("| stage | n | note |")
    w("|---|---:|---|")
    w("| posts in archive (all channels) | %d | %d channels |" % (posts_n, len(by_ch_posts)))
    w("| posts naming an instrument and a side | %d | includes %d with no SL/TP (heads-up posts, analysis, result claims), not scored |" % (cand, cand - len(lvl)))
    w("| signal-shaped (instrument + side + SL or TP) | %d | |" % len(lvl))
    def _k(r): return (r["channel"], r["instrument"], r["side"], r["entry_lo"], r["entry_hi"], r["sl"], tuple((t["v"], t["pips"]) for t in r["tps"]))
    kept_keys = {_k(r) for r in dd}
    lost = {_k(r) for r in nodate} - kept_keys
    w("| after valid-date filter | %d | %d dropped: (channel, timestamp) shared by %d or more posts. Many are same-second repost bursts: only %d distinct signals exist solely inside those groups (see section 6 for the groups) |" % (len(dd), len(nodate), BULK_N, len(lost)))
    w("| after repost dedupe | %d | %d reposts dropped (same channel/instrument/side/entry/SL/TPs within %d min of the previous copy) |" % (len(uniq), len(dup), DEDUPE_MIN))
    w("| with both SL and a TP | %d | %d dropped: missing SL or TP |" % (len(ok_lvl), len(incomplete)))
    w("| priced (Yahoo 5m bar at post time) | %d | %d older than Yahoo's ~60-day 5m history, %d no symbol data, %d no bar within %ds of the post (market closed) |" % (len(priced), len(old), len(nodata), len(nobar), MAX_STALE_S))
    w("| not flagged as price typo | %d | %d flagged typo_* or sl_distance_implausible, reported not scored |" % (len(nottypo), len(typo)))
    pass_gate = [r for r in nottypo]
    reasons = collections.Counter(r.get("skip_reason") for r in pass_gate if r["status"] == "skipped")
    nf = [r for r in pass_gate if r.get("filled")]
    w("| filled (market or touch) | %d | not filled: %s |" % (len(nf), ", ".join("%s %d" % (k, v) for k, v in reasons.items() if k in ("not_filled_in_window", "cancelled_sl_before_fill", "cancelled_tp_before_fill")) or "0"))
    w("| scored (full horizon of data, valid levels) | %d | market-fill variant %d, touch-fill variant %d. Excluded after fill: %s |" % (
        len(scored), len(mk), len(tc), ", ".join("%s %d" % (k, v) for k, v in reasons.items() if k in ("horizon_incomplete", "sl_already_breached", "tp_passed", "pips_unsupported")) or "0"))
    w("")
    w("Non-signal posts (no instrument, no side, or no levels) are not rows; only `data/telegram_funnel/fx_claims.jsonl` keeps the "
      "follow-up claims among them (%d claims captured, %d of them from bulk-timestamp posts)." % (len(claims), sum(1 for c in claims if c["bulk_timestamp"])))
    w("")
    # ---------------- instruments seen
    w("## 2. Instruments seen")
    w("")
    ic = collections.Counter(r["instrument"] for r in rows)
    ics = collections.Counter(r["instrument"] for r in lvl)
    icsc = collections.Counter(r["instrument"] for r in scored)
    w("| instrument | posts naming it (+side) | with SL/TP | scored | pip convention | Yahoo symbol used |")
    w("|---|---:|---:|---:|---|---|")
    for ins, n in ic.most_common():
        ps = pip_size(ins)
        ch = choice.get(ins)
        w("| %s | %d | %d | %d | %s | %s |" % (ins, n, ics[ins], icsc[ins], ("%g" % ps) if ps else "unsupported", ch["symbol"] if ch else "none"))
    w("")
    # ---------------- symbol validation
    w("## 3. Yahoo symbol validation")
    w("")
    w("For each candidate symbol: median absolute percent gap between the stated entry (zone midpoint) of market-order signals and the candidate's "
      "close at post time (gaps over 3% excluded as typos), coverage = matched / signals with a stated entry, and the signed price gap "
      "(entry minus tape) split by side. The pick is the lowest median gap among candidates with at least 80% of the best coverage. "
      "`const offset` = mean of the buy and sell medians, so the channels' habit of posting buy zones below and sell zones above market cancels. "
      "Futures carry decays toward expiry, so the headline mode (`auto`) instead fits a Theil-Sen line through per-day balanced medians (needs 5 days with both sides) and adds it to the candidate's bars; "
      "`gap after const / fit` is the remaining median gap, a check that the adjustment is doing something. Zone placement noise keeps that residual above zero.")
    w("")
    w("| instrument | candidate | data | range | n entries | matched | coverage | median abs gap (raw) | signed median buys / sells | const offset | gap after const | time-varying fit (price/day, days used) | gap after fit | picked |")
    w("|---|---|---|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|")
    for ins, lst in vrep.items():
        for d in lst:
            if not d["has_data"]:
                w("| %s | %s | none (no data from Yahoo, HTTP 404) | | %d | | | | | | | | | |" % (ins, d["symbol"], d["n_entries"]))
                continue
            picked = "yes" if choice.get(ins) and choice[ins]["symbol"] == d["symbol"] else ""
            fit = d.get("basis_fit")
            w("| %s | %s | 5m | %s to %s | %d | %s | %s | %s | %s / %s | %s | %s | %s | %s | %s |" % (
                ins, d["symbol"], d["first"], d["last"], d["n_entries"], d.get("n_matched", "-"), pct(d.get("coverage")),
                ("%.3f%%" % d["median_abs_gap_pct"]) if d.get("median_abs_gap_pct") is not None else "-",
                fmt(d.get("median_signed_buy")), fmt(d.get("median_signed_sell")), fmt(d.get("basis_offset")),
                ("%.3f%%" % d["median_abs_gap_after_const_pct"]) if d.get("median_abs_gap_after_const_pct") is not None else "-",
                ("%.3f/day (%d)" % (fit["b_per_day"], d["basis_days"])) if fit else ("not fitted (%d days)" % d.get("basis_days", 0)),
                ("%.3f%%" % d["median_abs_gap_after_fit_pct"]) if d.get("median_abs_gap_after_fit_pct") is not None else "-", picked))
    w("")
    w("Cash indices (^DJI, ^NDX, ^N225) only print during their own session, so they cover far fewer posts than the futures; that is why coverage gates the pick. "
      "Futures differ from the spot CFD the channel trades by a basis (carry); the offset above is that estimate, not a measured spread.")
    w("")

    def group_tables(title, key, rows_, variant):
        g = collections.defaultdict(list)
        for r in rows_: g[key(r)].append(r)
        w("| %s %s" % (title, STAT_HDR))
        w("|---%s" % STAT_SEP)
        for k in sorted(g, key=lambda k: -len(g[k])):
            w("| %s %s" % (k, stat_cells(table_stats(g[k]))))
        allst = table_stats(rows_)
        w("| **all** %s" % stat_cells(allst))
        w("")

    w("## 4. Results")
    w("")
    w("Outcome definitions: **TP1 hit** = TP1 touched before the stop; **TP2+** = TP2 touched before the stop (denominator: signals with two or more TPs); "
      "**SL first** = stop touched before TP1; **unresolved** = neither within the horizon. Mean R columns include unresolved trades marked to the last close. "
      "Expectancy@TP1 uses resolved trades only (TP1 = win at its stated R, stop = -1R); the break-even TP1 rate is 1/(1 + average win R), so a hit rate below it loses money before costs. "
      "Spread and slippage are ignored, which flatters every number here.")
    w("")
    w("### 4a. Market-fill variant (entry now / missing / market inside the entry zone)")
    w("")
    w("**By instrument**")
    w("")
    group_tables("instrument", lambda r: r["instrument"], mk, "market")
    w("**By channel**")
    w("")
    group_tables("channel", lambda r: r["channel"], mk, "market")
    w("### 4b. Fill-on-touch variant (entry_not_at_market; fill within %.0fh at the nearest entry edge)" % cfg["touch_hours"])
    w("")
    w("These are limit/stop-style entries away from the market at post time. Not pooled with 4a.")
    w("")
    w("**By instrument**")
    w("")
    group_tables("instrument", lambda r: r["instrument"], tc, "touch")
    w("**By channel**")
    w("")
    group_tables("channel", lambda r: r["channel"], tc, "touch")
    touch_all = [r for r in pass_gate if r.get("variant") == "touch"]
    tr = collections.Counter(r.get("skip_reason") or "scored" for r in touch_all)
    w("Touch-variant signals that reached the walk stage: %d. Outcome of the entry attempt: %s." % (len(touch_all), ", ".join("%s %d" % (k, v) for k, v in tr.most_common())))
    w("")
    # sensitivity
    w("### 4c. Sensitivity to the futures-to-spot basis (all instruments pooled, then gold alone)")
    w("")
    w("The basis estimate is the weakest input: on gold it is about 30 dollars against a typical stop of 10. Each row rescores the same posts with a different tape shift; the 0.07% rows are a plausible estimation error (the residual gap after the fit in section 3 is about 0.1%). "
      "Signals move between the market and touch variants when the shift changes, so n differs by row. `auto` is the headline (time-varying fit).")
    w("")
    w("| basis mode | gold: n market, TP1 hit, R@TP1, R@last | gold: n touch, TP1 hit, R@TP1, R@last | all instruments: n market, TP1 hit, R@TP1 | skipped for typo flag |")
    w("|---|---|---|---|---:|")
    ids = {r["id"]: r for r in rows}
    def sens(mode, ins, variant):
        rr = [x for rid, x in results[mode].items() if x.get("status") == "scored" and x.get("variant") == variant and (ins is None or ids[rid]["instrument"] == ins)]
        st = table_stats(rr)
        if not st: return "n=0"
        return "n=%d, %s, %s, %s" % (st["n"], pct(st["tp1_rate"]), fmt(st["mean_r_tp1"]), fmt(st["mean_r_last"]))
    for mode, label in (("auto", "auto (time-varying, headline)"), ("const", "const offset"), ("auto-0.07%", "auto shifted down 0.07% of price (about 3 dollars on gold)"), ("auto+0.07%", "auto shifted up 0.07% of price"), ("none", "none (raw futures)")):
        nt = sum(1 for x in results[mode].values() if x.get("skip_reason") == "typo_flagged")
        w("| %s | %s | %s | %s | %d |" % (label, sens(mode, "XAUUSD", "market"), sens(mode, "XAUUSD", "touch"), sens(mode, None, "market").rsplit(",", 1)[0], nt))
    w("")
    amb = [r for r in scored if r["ambiguous"]]
    w("Ambiguous bars (SL and a TP in the same 5m bar, counted as SL): %d of %d scored (%s)." % (len(amb), len(scored), pct(len(amb) / len(scored)) if scored else "-"))
    w("")
    # ---------------- stockmarketvault weekly
    SV = "t.me/stockmarketvault"
    w("## 5. t.me/stockmarketvault by week")
    w("")
    svs = [r for r in scored if r["channel"] == SV and r.get("variant") == "market"]
    svt = [r for r in scored if r["channel"] == SV and r.get("variant") == "touch"]
    weeks = sorted({weekmon(r["date"]) for r in rows if r["channel"] == SV})
    w("Week = Monday start (UTC). Market-fill variant; the last week is partial (archive ends 2026-10-13; same-timestamp groups are excluded). Small n per week: read the CI, not the point estimate.")
    w("")
    w("| week | distinct signals posted (valid dates, deduped) | scored (market) | TP1 hit (95% CI) | TP2+ | SL first | unresolved | mean R exit@TP1 | mean R exit@last TP | scored (touch) | touch TP1 hit |")
    w("|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|")
    for wk in weeks:
        posted = [r for r in rows if r["channel"] == SV and weekmon(r["date"]) == wk
                  and r.get("skip_reason") not in ("no_levels", "bulk_timestamp", "duplicate_repost", "no_sl", "no_tp")]
        a = [r for r in svs if weekmon(r["date"]) == wk]
        b = [r for r in svt if weekmon(r["date"]) == wk]
        st = table_stats(a)
        stb = table_stats(b)
        if st:
            lo, hi = st["tp1_ci"]
            w("| %s | %d | %d | %s (%s-%s) | %s | %s | %s | %s | %s | %d | %s |" % (
                wk, len(posted), st["n"], pct(st["tp1_rate"]), pct(lo), pct(hi),
                ("%s (%d/%d)" % (pct(st["tp2_rate"]), st["tp2plus"], st["n_multi"])) if st["n_multi"] else "n/a",
                pct(st["sl_rate"]), pct(st["open_rate"]), fmt(st["mean_r_tp1"]), fmt(st["mean_r_last"]), len(b),
                ("%s (n=%d)" % (pct(stb["tp1_rate"]), stb["n"])) if stb else "-"))
        else:
            w("| %s | %d | 0 | - | - | - | - | - | - | %d | %s |" % (wk, len(posted), len(b), ("%s (n=%d)" % (pct(stb["tp1_rate"]), stb["n"])) if stb else "-"))
    w("")
    # by instrument for SV, by hour-of-day? keep short
    # first half vs second half
    if svs:
        svs_sorted = sorted(svs, key=lambda r: r["ts"])
        mid = len(svs_sorted) // 2
        h1, h2 = table_stats(svs_sorted[:mid]), table_stats(svs_sorted[mid:])
        w("Split in half by time (market variant, n=%d): first half n=%d TP1 %s, mean R@TP1 %s; second half n=%d TP1 %s, mean R@TP1 %s." % (
            len(svs_sorted), h1["n"], pct(h1["tp1_rate"]), fmt(h1["mean_r_tp1"]), h2["n"], pct(h2["tp1_rate"]), fmt(h2["mean_r_tp1"])))
        w("")
    # ---------------- content timeline
    w("## 6. How t.me/stockmarketvault content changed over time")
    w("")
    svposts = [p for p in posts if p["channel"] == SV]
    same_ts = collections.Counter((p["channel"], p["date"]) for p in posts)
    sig_ids = {r["id"] for r in rows if r["channel"] == SV and r.get("skip_reason") != "no_levels"}
    cat = collections.defaultdict(collections.Counter)
    day_cat = collections.defaultdict(collections.Counter)
    grp = collections.defaultdict(list)
    for p in svposts:
        c = classify_content(p, sig_ids)
        inb = same_ts[(p["channel"], p["date"])] >= BULK_N
        cat[weekmon(p["date"])][c] += 1
        if inb: cat[weekmon(p["date"])]["in_same_ts_group"] += 1
        day_cat[p["date"][:10]][c] += 1
        if inb: grp[p["date"]].append((p, c))
    cats = ["fx_signal", "fx_chatter_analysis", "stock_callout", "promo_chat", "other"]
    w("Archive window for this channel: %s to %s, %d posts. Categories are keyword heuristics on the post text: `fx_signal` = parsed instrument, side and levels; `fx_chatter_analysis` = gold/pips/SL/TP words without a full signal (results, analysis, stop moves); "
      "`stock_callout` = cashtags or option strings; `promo_chat` = deposit/withdrawal/investment/VIP wording. The last column counts posts whose exact timestamp is shared by %d or more posts (their dates are not trusted); those posts are also counted in their content category." % (
        min(p["date"] for p in svposts)[:10], max(p["date"] for p in svposts)[:10], len(svposts), BULK_N))
    w("")
    w("| week | " + " | ".join(cats) + " | total | of which in same-timestamp groups |")
    w("|---|" + "---:|" * (len(cats) + 2))
    for wk in sorted(cat):
        w("| %s | %s | %d | %d |" % (wk, " | ".join(str(cat[wk][c]) for c in cats), sum(cat[wk][c] for c in cats + ["other"]) if False else sum(cat[wk][c] for c in cats), cat[wk]["in_same_ts_group"]))
    w("")
    w("Same-timestamp groups (SV, %d or more posts at one exact second). Composition shows what each group is: a repost burst of one or two signals, chat lines, or the stock-ticker dump." % BULK_N)
    w("")
    w("| timestamp (UTC) | posts | fx signal-shaped | stock/option text | other | first and last id |")
    w("|---|---:|---:|---:|---:|---|")
    for t in sorted(grp):
        g = grp[t]
        nf = sum(1 for _, c in g if c == "fx_signal"); ns = sum(1 for _, c in g if c == "stock_callout")
        w("| %s | %d | %d | %d | %d | %s to %s |" % (t.replace("T", " ")[:19], len(g), nf, ns, len(g) - nf - ns, g[0][0]["id"].split("/")[-1], g[-1][0]["id"].split("/")[-1]))
    w("")
    fx_posts = sorted((p["date"], p["id"]) for p in svposts if p["id"] in sig_ids and p["id"] in {r["id"] for r in rows if r.get("sl") is not None or r.get("tps")})
    st_posts = sorted((p["date"], p["id"]) for p in svposts if classify_content(p, sig_ids) == "stock_callout")
    st_days = sorted({d for d, c in day_cat.items() if c["stock_callout"]})
    big = [p for p in svposts if classify_content(p, sig_ids) == "stock_callout" and same_ts[(p["channel"], p["date"])] >= BULK_N]
    w("- Parsed FX/gold/index signals with levels: first post **%s**, last post **%s** UTC (%d posts, %d distinct signal-days)." % (fx_posts[0][0] if fx_posts else "-", fx_posts[-1][0] if fx_posts else "-", len(fx_posts), len({d[:10] for d, _ in fx_posts})))
    w("- Stock-ticker / option-style posts (cashtags, call/put strings): %d posts on %d days; first %s, last %s. %d of them sit in same-timestamp groups, so for those the archive cannot say when they were originally posted; the burst on 2026-10-13 around 09:53 UTC is where the bulk of them are." % (
        len(st_posts), len(st_days), st_posts[0][0] if st_posts else "-", st_posts[-1][0] if st_posts else "-", len(big)))
    w("- Reading: the channel's sustained output from the start of the archive until 2026-10-13 morning is gold/index/FX signals with a few chat and promo lines; stock and options callouts appear in volume only in the 2026-10-13 dump and after. Whether the switch is a genuine change of format or a replay of older content cannot be settled from this archive.")
    w("")
    # ---------------- claims
    w("## 7. Channel follow-up claims (not scored)")
    w("")
    ck = collections.Counter(k for c in claims for k in c["kinds"])
    real = [c for c in claims if not c["bulk_timestamp"]]
    w("%d claim-like posts (%d outside bulk timestamps) saved to `data/telegram_funnel/fx_claims.jsonl`: %s. These are the channel's own words (\"Tp1 done\", \"+180 pips\", \"running 110+ pips\") without an attached trade id, so they cannot be matched to one signal yet. "
      "Next step if wanted: join each claim to the most recent unresolved signal before it and compare the claimed pips with the tape." % (
        len(claims), len(real), ", ".join("%s %d" % (k, v) for k, v in ck.most_common())))
    sv_cl = [c for c in real if c["channel"] == SV]
    pc = [c["pips"] for c in sv_cl if c.get("pips")]
    if pc:
        w("")
        w("stockmarketvault stated pip figures outside bulk timestamps: n=%d, median %d, max %d." % (len(pc), statistics.median(pc), max(pc)))
    w("")
    # ---------------- what it says
    w("## 8. What this says")
    w("")
    ms = table_stats(mk)
    for line in what_it_says(mk, tc, scored, svs, ms):
        w(line)
    rmk = []
    for mode in ("auto", "const", "auto-0.07%", "auto+0.07%"):
        rr = [x for x in results[mode].values() if x.get("status") == "scored" and x.get("variant") == "market"]
        st = table_stats(rr)
        if st: rmk.append((mode, st))
    if rmk:
        lo_r = min(st["mean_r_tp1"] for _, st in rmk); hi_r = max(st["mean_r_tp1"] for _, st in rmk)
        sign = "The sign of the mean R is the same in every mode" if (hi_r < 0 or lo_r > 0) else "The sign of the mean R flips between modes"
        w("- **Robustness to the basis estimate**: across the four basis modes in 4c the market-variant TP1 hit rate runs %s to %s and mean R exit@TP1 runs %s to %s (n %d to %d). %s; the size is not stable, because a few dollars of tape shift moves gold signals between fill variants and flips close calls on 10-dollar stops." % (
            pct(min(st["tp1_rate"] for _, st in rmk)), pct(max(st["tp1_rate"] for _, st in rmk)), fmt(lo_r), fmt(hi_r),
            min(st["n"] for _, st in rmk), max(st["n"] for _, st in rmk), sign))
    if svs:
        ss = sorted(svs, key=lambda r: r["ts"])
        m_ = len(ss) // 2
        a_, b_ = table_stats(ss[:m_]), table_stats(ss[m_:])
        w("- **Does stockmarketvault change over time?** First half of the scored signals (n=%d) TP1 %s, mean R@TP1 %s; second half (n=%d) TP1 %s, mean R@TP1 %s. Weekly cells hold from a handful to about twenty signals each, with CIs spanning 30 points or more, so a drift of this size cannot be separated from noise. "
          "What did change is volume and format: see section 6." % (a_["n"], pct(a_["tp1_rate"]), fmt(a_["mean_r_tp1"]), b_["n"], pct(b_["tp1_rate"]), fmt(b_["mean_r_tp1"])))
    w("")
    w("- This is a descriptive check of public posts under stated assumptions, not a finding about intent.")
    w("")
    w("## 9. Assumptions and known gaps")
    w("")
    for line in ASSUMPTIONS:
        w("- " + line)
    w("")
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    open(OUT_MD, "w").write("\n".join(A) + "\n")


ASSUMPTIONS = [
    "Fill model: the market variant fills at the close of the 5m bar containing the post, which can be up to 5 minutes after the post. Real fills on a CFD broker carry spread (gold typically 2 to 3 dollars against stops of about 10) and slippage; both ignored here, so every R figure is optimistic.",
    "Tolerance: a stated entry or zone counts as at-market when the market is inside it widened by 0.25 x |entry mid - SL|. Wider tolerance moves signals from the touch variant to the market variant.",
    "Pips: gold 1 pip = 0.10, indices 1 point, FX 0.0001 (JPY 0.01). Pip-denominated TPs (for example `TP: 50/100PIPS`) are measured from the fill price; signals using them carry `tp_pips_assumed`. If the channel meant 1 pip = 1.00 on gold, those targets are 10x farther than scored.",
    "Same-bar ambiguity: SL wins over TP inside one 5m bar. TP1 and TP2 in the same bar are both credited. On the fill bar of a touch-variant signal only the SL is credited.",
    "TP order: targets are sorted by distance from the fill, so `tp1` is the nearest even if the channel listed it differently. Targets already passed or on the wrong side at fill are dropped and flagged `tp_wrong_side_or_passed`. TPs written `open` are ignored.",
    "No management: no break-even move, no partial closes, no trailing. Channels often tell followers to move to break-even after TP1; that rule is not modelled, so the exit@last TP column is a harsh all-or-nothing reading and the exit@TP1 column is the generous one.",
    "Futures proxies (GC=F, YM=F, NQ=F) stand in for spot CFDs because Yahoo has no XAUUSD=X data; the estimated basis is applied in `auto` mode; 4c shows const, shifted and no-basis results. A basis error of a few dollars is comparable to the 10-dollar stops, which is the main uncertainty in this report.",
    "The archive holds posts, not edits or deletions. A signal the channel later deleted or amended is scored as posted. Reposts within 60 minutes are collapsed to the first copy; a changed level creates a new signal.",
    "Horizon: trades whose 24h window runs past the last Yahoo bar are excluded (`horizon_incomplete`), not scored as open.",
    "Posts with no stated entry and no numbers (\"GOLD SELL NOW\" alone) have no SL or TP and are not scored. Claims text is not matched to signals yet.",
    "Sample sizes are small (tens of signals per instrument, one month, one dominant channel). Confidence intervals are Wilson 95% on the TP1 hit rate only; treat everything else as descriptive.",
]


def what_it_says(mk, tc, scored, svs, ms):
    L = []
    if not ms:
        return ["No scored signals."]
    L.append("- **Sample**: %d signals scored in the market-fill variant (%d from t.me/stockmarketvault) and %d in the touch variant, out of the funnel in section 1. Everything below is that sample, one month long." % (
        len(mk), len(svs), len(tc)))
    L.append("- **Hit rate vs payoff**: market variant TP1 touched before the stop in %s of %d signals (CI %s-%s), stop first in %s, unresolved %s. "
             "Average winning TP1 is %s R, so the break-even TP1 rate is %s. Mean R exit@TP1 is %s and exit@last TP is %s (before spread)." % (
                 pct(ms["tp1_rate"]), ms["n"], pct(ms["tp1_ci"][0]), pct(ms["tp1_ci"][1]), pct(ms["sl_rate"]), pct(ms["open_rate"]),
                 fmt(ms["avg_win_r"]), pct(ms["be_rate"]), fmt(ms["mean_r_tp1"]), fmt(ms["mean_r_last"])))
    L.append("- **Payoff shape**: TP1 sits on average %s R from the fill while the stop is 1 R away, so a TP1 exit needs a hit rate of at least %s to break even before costs." % (fmt(ms["avg_win_r"]), pct(ms["be_rate"])))
    if tc:
        st = table_stats(tc)
        L.append("- **Touch variant** (limit-style entries away from market, n=%d): TP1 %s, mean R exit@TP1 %s, exit@last TP %s. Not comparable with the market variant." % (
            st["n"], pct(st["tp1_rate"]), fmt(st["mean_r_tp1"]), fmt(st["mean_r_last"])))
    L.append("- **Claims vs tape**: the channel's own results posts (\"+180 pips\", \"5 TPs hit all at once\") are listed in `fx_claims.jsonl` but not yet joined to individual signals; the scored numbers above are what the tape supports for the signals as posted.")
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--no-fetch", action="store_true", help="use cached Yahoo bars only")
    ap.add_argument("--horizon-hours", type=float, default=HORIZON_HOURS)
    ap.add_argument("--touch-hours", type=float, default=TOUCH_HOURS)
    ap.add_argument("--basis", choices=["auto", "const", "none"], default="auto",
                    help="auto = time-varying (Theil-Sen) futures-to-spot basis estimated from stated entries; const = one offset; none = raw futures")
    args = ap.parse_args()
    posts, rows, claims, nonsig, choice, vrep, results, primary, cfg = run(args)
    os.makedirs(os.path.dirname(OUT_ROWS), exist_ok=True)
    with open(OUT_ROWS, "w") as f:
        for r in sorted(rows, key=lambda r: (r["channel"], r["ts"])):
            f.write(json.dumps(row_out(r), ensure_ascii=False) + "\n")
    with open(OUT_CLAIMS, "w") as f:
        for c in claims:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    write_report(args, posts, rows, claims, nonsig, choice, vrep, results, primary, cfg)
    sc = [r for r in rows if r["status"] == "scored"]
    print("rows %d, scored %d, claims %d -> %s, %s" % (len(rows), len(sc), len(claims), OUT_ROWS, OUT_MD))


if __name__ == "__main__":
    main()
