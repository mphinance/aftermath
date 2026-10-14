"""
Regression tests for tg_calls.py (offline Telegram callout parser).

The gold file holds hand-labelled posts (tests/fixtures/tg_calls_gold.json): a stratified random sample of the
archive ("sample"), a second batch checked after the first round of fixes ("holdout", "blind") and posts from
reported data-quality problems ("regression"). `expected` lists the correct records per post; each expected
field is compared exactly (null means "must be null", e.g. a close must not carry the exit price as entry).
No network, no archive file needed.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import tg_calls

GOLD = json.loads((Path(__file__).parent / "fixtures" / "tg_calls_gold.json").read_text())
FIELDS = ["ticker", "side", "strike", "expiry", "entry_price", "action", "result_pct"]
OPTIONAL = ["exit_price", "kind", "strikes"]
# Known, documented parser gaps (see docs/FUNNEL.md): bare ticker AFTER the percent, and "QQQ calls 730C" prose.
KNOWN_GAPS = {"ajfreealart32/492", "legacypublicroom/324"}


def post(text, date="2026-10-13T14:00:00+00:00", pid="t/1", channel="t.me/t"):
    return {"id": pid, "channel": channel, "date": date, "text": text}


def run(g):
    return tg_calls.parse(post(g["text"], g["date"], g["id"], g["channel"]))


def match(expected, out):
    """Pair each expected record with the best unused parser record of the same ticker."""
    used, pairs = set(), []
    for e in expected:
        best = None
        for j, o in enumerate(out):
            if j in used or o["ticker"] != e["ticker"]: continue
            score = (o["strike"] == e["strike"]) * 2 + (o["side"] == e["side"])
            if best is None or score > best[0]: best = (score, j)
        if best: used.add(best[1])
        pairs.append((e, out[best[1]] if best else None))
    return pairs, [o for j, o in enumerate(out) if j not in used]


@pytest.mark.parametrize("g", GOLD, ids=[g["id"] for g in GOLD])
def test_gold_post(g):
    if g["id"] in KNOWN_GAPS:
        pytest.xfail("documented gap")
    out = run(g)
    pairs, extra = match(g["expected"], out)
    assert not extra, f"spurious records: {[(o['ticker'], o['side'], o['strike'], o['action']) for o in extra]}"
    for e, o in pairs:
        assert o is not None, f"missing {e}"
        for f in FIELDS + [k for k in OPTIONAL if k in e]:
            assert o[f] == e[f], f"{g['id']} {e['ticker']} {f}: expected {e[f]!r}, got {o[f]!r}"


def test_gold_precision_recall_floor():
    tp = {f: 0 for f in FIELDS}; pn = dict(tp); gn = dict(tp)
    for g in GOLD:
        if g["id"] in KNOWN_GAPS: continue
        out = run(g)
        pairs, _ = match(g["expected"], out)
        for f in FIELDS:
            gn[f] += sum(1 for e in g["expected"] if e[f] is not None)
            pn[f] += sum(1 for o in out if o[f] is not None)
            tp[f] += sum(1 for e, o in pairs if o and e[f] is not None and o[f] == e[f])
    for f in FIELDS:
        assert tp[f] / pn[f] >= 0.97, f"{f} precision {tp[f]}/{pn[f]}"
        assert tp[f] / gn[f] >= 0.97, f"{f} recall {tp[f]}/{gn[f]}"


def test_schema_is_backward_compatible():
    r = tg_calls.parse(post("$SPY 777C 10/14 @ .50"))[0]
    for k in ["id", "channel", "posted", "ticker", "kind", "side", "strike", "expiry", "entry_price", "action", "result_pct", "text"]:
        assert k in r
    assert isinstance(r["parse_flags"], list)


def test_empty_and_textless_posts():
    assert tg_calls.parse(post("")) == []
    assert tg_calls.parse({"id": "x", "channel": "c", "date": "", "text": None}) == []


def test_close_exit_price_is_not_entry():
    r = tg_calls.parse(post("Exit · $PLTR 10/02 195C @ $3.62 · +11%\nALL OUT · $3.25 → $3.62"))[0]
    assert (r["action"], r["entry_price"], r["exit_price"], r["result_pct"]) == ("close", 3.25, 3.62, 11.0)
    r = tg_calls.parse(post("Queen\nTrim\n\n$AAPL 10/9 340c @ 1.25"))[0]
    assert r["action"] == "close" and r["entry_price"] is None and r["exit_price"] == 1.25


def test_tp_sl_lines_are_not_entry_or_result():
    r = tg_calls.parse(post("🟢 Entry · $SMCI 10/02 44C @ $1.38 · small\n🎯 Recommended TP ~$2.18 (+58%) · SL 0.80"))[0]
    assert r["action"] == "open" and r["entry_price"] == 1.38 and r["result_pct"] is None
    assert "tp_sl_present" in r["parse_flags"]


def test_close_to_itm_is_not_a_close():
    r = tg_calls.parse(post("$TX close to ITM, these can 10x"))[0]
    assert r["action"] == "mention"


def test_close_wins_over_later_opened_line():
    r = tg_calls.parse(post("Closed 150 $SPX 7800C 10/08\n@ $4.70 (Entry: $3.80) | Gain: +23.7%\nOpened: 9:47 AM ET\nTrade Summary\nTotal Profit: $+13500.00"))
    assert len(r) == 1 and r[0]["action"] == "close" and r[0]["entry_price"] == 3.8 and r[0]["exit_price"] == 4.7
    assert "has_summary" in r[0]["parse_flags"]


def test_recap_never_opens_and_pct_stays_on_its_line():
    txt = "TRADE RECAP\n\nCLOSED TRADES\n\n🟢 $QQQ 750P — +95%\n🟢 $SPY 778C — +1,200%\n🔴 $TSLA 390C — -94%\n\nSTILL HOLDING\n\n👀 $HOOD 112C\n\nWin Rate: 80%\nCombined: +175.38%"
    r = tg_calls.parse(post(txt))
    assert [x["action"] for x in r] == ["close", "close", "close", "mention"]
    assert [x["result_pct"] for x in r] == [95.0, 1200.0, -94.0, None]


def test_spread_is_not_emitted_as_single_leg():
    r = tg_calls.parse(post("🚀 $SPCX 10/16 170/172.5C CDS @ $0.55"))[0]
    assert (r["kind"], r["strike"], r["strikes"], r["entry_price"], r["expiry"]) == ("spread", None, [170.0, 172.5], 0.55, "2026-10-16")
    r = tg_calls.parse(post("$XYZ 50C debit spread @ 1.00"))[0]
    assert r["kind"] == "spread" and r["strike"] is None and "spread_suspect" in r["parse_flags"]


def test_entry_formats():
    for txt, px in [("$NFLX 70P @.02", .02), ("$AAPL 352.50 Calls 10/14 $0.32 Entry", .32), ("$SPX 7795C .60 LOTTO SIZE", .60),
                    ("$ESNT BTO\nOCT/08\n65C e:0.70", .70), ("$HELE 25 CALL 12/15 avg .30", .30), ("$X 10/16 50C Entry: $3.80", 3.80),
                    ("$SPY OCT/13 777PUT e.68 ODTE", .68), ("$BRZE 16 OCT 26 $25 CALL $0.95", .95)]:
        r = tg_calls.parse(post(txt))[0]
        assert r["entry_price"] == px, txt


def test_expiry_formats_and_flags():
    r = tg_calls.parse(post("$REPX 50 Call 10/16.35🚨"))[0]
    assert r["expiry"] == "2026-10-16" and r["entry_price"] == 0.35  # '.35' is a price, not a year
    r = tg_calls.parse(post("$SPY 778.83 put 13/10"))[0]
    assert r["expiry"] == "2026-10-13" and "date_dmy" in r["parse_flags"]
    r = tg_calls.parse(post("$SPY 777C 0.47 Odte", date="2026-10-08T13:48:00+00:00"))[0]
    assert r["expiry"] == "2026-10-08" and "expiry_0dte_tag" in r["parse_flags"]
    r = tg_calls.parse(post("$SPY 745C @.32 lotto"))[0]
    assert r["expiry"] is None and "no_expiry" in r["parse_flags"]
    r = tg_calls.parse(post("$AMZN 252.5P 09/10 @.38", date="2026-10-08T14:00:00+00:00"))[0]
    assert r["expiry"] is None and r["expiry_raw"] == "09/10" and "expiry_before_post" in r["parse_flags"]
    r = tg_calls.parse(post("6/12 $TGT 133c @.16", date="2026-06-09T14:00:00+00:00"))[0]
    assert r["expiry"] == "2026-06-12"
    r = tg_calls.parse(post("$GOOGL 357.5 CALL 12/10 @.25"))[0]
    assert r["expiry"] == "2026-12-10" and "expiry_far" in r["parse_flags"]


def test_multi_contract_prices_stay_on_their_own_ticker():
    r = tg_calls.parse(post("BTO $QQQ 10/13 741p .69  \n\nBTO $SPX 10/13 7785p @ 2.5"))
    assert [(x["ticker"], x["entry_price"]) for x in r] == [("QQQ", .69), ("SPX", 2.5)]
    r = tg_calls.parse(post("Got 3.3 on $SPX puts for +27% Gains\n\n$QQQ puts got .8 for +10% Gains\n\nSold last on this bounce"))
    assert [(x["ticker"], x["result_pct"]) for x in r] == [("SPX", 27.0), ("QQQ", 10.0)]


def test_index_alias_and_bare_ticker_calls():
    r = tg_calls.parse(post("Closed 10 SPXW 7805C 10/09 @ $3.70 (Entry: $3.80) | Gain: -2.6%"))[0]
    assert r["ticker"] == "SPX" and r["strike"] == 7805.0 and r["result_pct"] == -2.6
    r = tg_calls.parse(post("🚨 TER TRADE CALL 🚨\n\n🚀 $TER 10/16 420/425C CDS @ $1.30"))
    assert len(r) == 1 and r[0]["ticker"] == "TER"


def test_uppercase_words_are_not_tickers():
    assert tg_calls.parse(post("OPEN 5 CALLS ON THE CLOSE TODAY. ALL IN. TP 2.50 SL 0.80")) == []
    assert tg_calls.parse(post("Good morning family, BIG DAY, 10 C of coffee")) == []


def test_ticker_list_is_never_an_open():
    txt = "50 trending stocks:\n" + "\n".join(f"${t} long term story" for t in ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"])
    r = tg_calls.parse(post(txt))
    assert r and all(x["action"] == "mention" and "ticker_list" in x["parse_flags"] for x in r)


def test_hindsight_and_unrealised_are_not_results():
    r = tg_calls.parse(post("Those NVDA 227.50P are at 2.60 from .72 should've held runners +261% if anyone decided to degen"))[0]
    assert r["action"] == "mention" and r["result_pct"] is None and r["entry_price"] == .72
    r = tg_calls.parse(post("$SDRL UP 200% ☢️"))[0]
    assert r["action"] == "mention" and r["result_pct"] is None
    r = tg_calls.parse(post("Contract: QQQ 9/29 737P\n\nUp 55%🔥🔥"))[0]
    assert r["action"] == "mention" and r["result_pct"] is None


def test_annotate_flags_echoes_and_links_closes():
    base = dict(kind="option", side="put", strike=778.83, strikes=None, expiry="2026-10-13", entry_price=None, exit_price=None,
                result_pct=None, parse_flags=[], text="", ticker="SPY")
    a = dict(base, id="c/1", channel="c", posted="2026-10-13T13:00:00+00:00", action="open")
    b = dict(base, id="c/2", channel="c", posted="2026-10-13T13:01:00+00:00", action="open")
    x = dict(base, id="d/1", channel="d", posted="2026-10-13T13:02:00+00:00", action="open")
    cl = dict(base, id="c/3", channel="c", posted="2026-10-13T15:00:00+00:00", action="close", result_pct=30.0, kind="stock", side=None, strike=None, expiry=None)
    out = tg_calls.annotate([a, b, x, cl])
    assert "duplicate_echo" in out[1]["parse_flags"] and out[1]["dup_of"] == "c/1"
    assert "cross_channel_echo" in out[2]["parse_flags"]
    assert out[3]["open_id"] == "c/1" and out[3]["open_link"] == "ticker_day"
    d1 = dict(a, id="c/9", entry_price=0.5)
    assert "duplicate_echo" not in tg_calls.annotate([a, d1])[1]["parse_flags"]  # different fill is a different trade
