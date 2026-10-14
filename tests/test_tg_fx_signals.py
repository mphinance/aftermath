"""
Regression tests for tg_fx_signals.py (forex / gold / index signal parser and scorer).

tests/fixtures/tg_fx_gold.json holds hand-labelled real posts from the archive (47 posts: gold zones and singles,
US30, NAS100, EURUSD, GBPCHF limit, AVAX/USD, BTC, pips-denominated TPs, emoji and math-bold decorations, the
missing-digit US30 typo, the abbreviated zone 4348-46, and non-signals). No network, no archive file needed.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import tg_fx_signals as T

GOLD = json.loads((Path(__file__).parent / "fixtures" / "tg_fx_gold.json").read_text())
POSTS = GOLD["posts"]


def test_fixture_size():
    assert len(POSTS) >= 30
    assert sum(1 for p in POSTS if p["expected"]) >= 30


@pytest.mark.parametrize("p", POSTS, ids=[p["id"] for p in POSTS])
def test_parse(p):
    got = T.parse_signal(p["text"])
    exp = p["expected"]
    if exp is None:
        # either not signal-shaped at all or no SL/TP levels
        assert got is None or not got["has_levels"] or p["id"].endswith("/2857")
        if p["id"].endswith("/2857"):
            assert got is None  # documented gap: instrument never named
        return
    assert got is not None and got["has_levels"]
    assert got["instrument"] == exp["instrument"]
    assert got["side"] == exp["side"]
    assert got["order_type"] == exp["order_type"]
    assert [got["entry_lo"], got["entry_hi"]] == exp["entry"]
    assert got["sl"] == exp["sl"]
    assert [[t["v"], "pips" if t["pips"] else "px"] for t in got["tps"]] == exp["tps"]


def test_pips_flag():
    p = next(x for x in POSTS if x["id"].endswith("/2369"))
    assert "tp_pips_assumed" in T.parse_signal(p["text"])["flags"]
    q = next(x for x in POSTS if x["id"].endswith("/2445"))
    assert "tp_pips_assumed" not in T.parse_signal(q["text"])["flags"]


def test_open_ended_tp_flag():
    p = next(x for x in POSTS if x["id"].endswith("/2909"))
    assert "tp_open_ended" in T.parse_signal(p["text"])["flags"]


def test_zone_vs_single_kind():
    byid = {p["id"].split("/")[-1]: T.parse_signal(p["text"]) for p in POSTS if p["expected"]}
    assert byid["2354"]["entry_kind"] == "zone"
    assert byid["2445"]["entry_kind"] == "single"
    assert byid["2982"]["entry_kind"] == "now"


@pytest.mark.parametrize("c", GOLD["typo_cases"], ids=[c["id"] for c in GOLD["typo_cases"]])
def test_typo_check(c):
    text = next(p["text"] for p in POSTS if p["id"] == c["id"])
    flags = T.typo_check(T.parse_signal(text), c["market"])
    assert set(c["expect"]) <= set(flags)
    if not c["expect"]:
        assert flags == []


@pytest.mark.parametrize("c", GOLD["claims"])
def test_claims(c):
    got = T.parse_claim(c["text"])
    if c["kinds"] is None:
        assert got is None
    else:
        assert got["kinds"] == c["kinds"]
        assert got["pips"] == c["pips"] and got["tp_n"] == c["tp_n"]


def test_norm_strips_decorations():
    assert T.norm("ㅤXAUUSD ㅤ ￴ 4390 ✅") == "XAUUSD 4390"
    assert T.norm("\U0001d653\U0001d63c\U0001d650\U0001d650\U0001d64e\U0001d63f BUY") == "XAUUSD BUY"
    assert T.norm("TP¹  4390") == "TP1 4390"


def test_stock_posts_are_not_signals():
    for t in ["$ARW 230 CALL 5/15 avg .30", "$SPY put 13/10", "OVERNIGHT SWING\n\n$NVDA 200C 10/16 @1.10 SL 0.50 TP 2.00"]:
        assert T.parse_signal(t) is None


# ----------------------------------------------------------------- dedupe

def _row(i, ts, **kw):
    r = {"id": "c/%d" % i, "channel": "t.me/c", "instrument": "XAUUSD", "side": "buy", "entry_lo": 4000.0, "entry_hi": 4000.0,
         "sl": 3990.0, "tps": [{"v": 4010.0, "pips": False}], "ts": ts, "status": "pending", "skip_reason": None}
    r.update(kw)
    return r


def test_dedupe_chain_and_changed_level():
    rows = [_row(1, 0), _row(2, 5), _row(3, 50 * 60), _row(4, 100 * 60),            # chain: each within 60 min of the previous
            _row(5, 400 * 60), _row(6, 401 * 60, sl=3985.0),                         # later copy kept; changed SL is a new signal
            _row(7, 10, channel="t.me/other")]                                       # same levels, other channel: kept
    T.dedupe_reposts(rows)
    st = {r["id"]: r["skip_reason"] for r in rows}
    assert st == {"c/1": None, "c/2": "duplicate_repost", "c/3": "duplicate_repost", "c/4": "duplicate_repost",
                  "c/5": None, "c/6": None, "c/7": None}
    assert rows[3]["dup_of"] == "c/1"


# ----------------------------------------------------------------- scoring on synthetic bars

def bars_from(path, start=1_000_000 - (1_000_000 % 300)):
    """path: list of (open, high, low, close) five-minute bars starting at `start`."""
    ts = [start + i * 300 for i in range(len(path))]
    return {"ts": ts, "o": [b[0] for b in path], "h": [b[1] for b in path], "l": [b[2] for b in path], "c": [b[3] for b in path]}, ts


CFG = {"horizon_hours": 1.0, "touch_hours": 1.0}
B = 4000.0      # gold-like price level so the 1% risk plausibility cap is not hit by 10-dollar stops


def sig(side="buy", lo=B, hi=B, sl=B - 10, tps=(B + 5, B + 10), ts=None, instrument="XAUUSD", **kw):
    s = {"instrument": instrument, "side": side, "order_type": "market", "entry_lo": lo, "entry_hi": hi, "entry_kind": "single",
         "sl": sl, "tps": [{"v": v, "pips": False} for v in tps], "flags": [], "ts": ts}
    s.update(kw)
    return s


def flat(n, p=B):
    return [(p, p + 0.2, p - 0.2, p)] * n


def test_market_buy_hits_tp1_then_tp2():
    path = flat(3) + [(B, B + 5.5, B - 0.1, B + 5.2), (B + 5.2, B + 10.5, B + 5, B + 10.2)] + flat(20, B + 10)
    b, ts = bars_from(path)
    r = T.score_one(sig(ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["status"] == "scored" and r["variant"] == "market"
    assert r["outcome"] == "tp2" and r["tp1_hit"] and r["last_tp_hit"] and not r["sl_first"]
    assert r["R_price"] == pytest.approx(10.0)
    assert r["r_tp1"] == pytest.approx(0.5) and r["r_last"] == pytest.approx(1.0)


def test_stop_first_and_ambiguous_bar_counts_sl():
    path = flat(2) + [(B, B + 0.3, B - 11, B - 9)] + flat(20, B - 9)
    b, ts = bars_from(path)
    r = T.score_one(sig(ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["outcome"] == "sl" and r["sl_first"] and r["r_tp1"] == -1.0 and r["r_last"] == -1.0 and not r["ambiguous"]
    # same bar contains both TP1 and SL: stop wins and the row is marked ambiguous
    path = flat(2) + [(B, B + 5.5, B - 11, B)] + flat(20, B)
    b, ts = bars_from(path)
    r = T.score_one(sig(ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["outcome"] == "sl" and r["ambiguous"] is True and not r["tp1_hit"]


def test_sell_side_mirrors():
    path = flat(2) + [(B, B + 0.2, B - 5.2, B - 5.0)] + flat(20, B - 5)
    b, ts = bars_from(path)
    r = T.score_one(sig(side="sell", sl=B + 10, tps=(B - 5, B - 10), ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["tp1_hit"] and r["outcome"] == "tp1" and r["r_tp1"] == pytest.approx(0.5)


def test_unresolved_is_marked_to_market():
    path = flat(2) + [(B, B + 2.0, B - 1, B + 2.0)] + flat(20, B + 2)
    b, ts = bars_from(path)
    r = T.score_one(sig(ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["outcome"] == "open" and not r["resolved"]
    assert r["r_tp1"] == pytest.approx(0.2) and r["r_last"] == pytest.approx(0.2)


def test_zone_far_from_market_uses_touch_fill_and_cancels_when_tp_comes_first():
    # buy zone B-8 to B-7, market B: price must drop to B-7 first
    path = flat(2) + [(B, B + 0.2, B - 7.1, B - 6.0)] + [(B - 6.0, B + 3.6, B - 6.1, B + 3.2)] + flat(20, B + 3)
    b, ts = bars_from(path)
    s = sig(lo=B - 8, hi=B - 7, sl=B - 14, tps=(B + 3,), ts=ts[0] + 10, entry_kind="zone")
    r = T.score_one(s, b, 0.0, CFG, "X")
    assert r["variant"] == "touch" and r["entry_not_at_market"] and r["fill_price"] == B - 7
    assert r["status"] == "scored" and r["tp1_hit"]
    # TP1 reached before the zone is touched: cancelled
    path = flat(2) + [(B, B + 4.0, B - 0.1, B + 3.5)] + flat(20, B + 3.5)
    b, ts = bars_from(path)
    r = T.score_one(dict(s, ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["status"] == "skipped" and r["skip_reason"] == "cancelled_tp_before_fill"


def test_market_inside_tolerance_is_market_variant():
    # zone B+0.5..B+1.5 around market B: tol = 0.25 * |B+1 - (B-10)| = 2.75 so the market counts as at-market
    b, ts = bars_from(flat(25))
    r = T.score_one(sig(lo=B + 0.5, hi=B + 1.5, ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["variant"] == "market"


def test_pips_use_pip_size_from_fill():
    path = flat(2) + [(B, B + 1.2, B - 0.1, B + 1.0)] + flat(20, B + 1)
    b, ts = bars_from(path)
    s = sig(tps=(), ts=ts[0] + 10)
    s["tps"] = [{"v": 5.0, "pips": True}, {"v": 10.0, "pips": True}]   # gold: 5 pips = 0.50, 10 pips = 1.00
    r = T.score_one(s, b, 0.0, CFG, "X")
    assert r["tp_levels"] == [pytest.approx(B + 0.5), pytest.approx(B + 1.0)]
    assert r["tps_hit"] == 2


def test_typo_signal_is_flagged_not_scored():
    b, ts = bars_from(flat(25))
    r = T.score_one(sig(lo=B / 10, hi=B / 10, sl=B / 10 - 10, tps=(B / 10 + 5,), ts=ts[0] + 10), b, 0.0, CFG, "X")
    assert r["status"] == "skipped" and r["skip_reason"] == "typo_flagged"
    assert any(f.startswith("typo_magnitude") for f in r["flags_add"])


def test_no_bar_at_post_time_is_unpriced():
    b, ts = bars_from(flat(5))
    r = T.score_one(sig(ts=ts[-1] + 3600), b, 0.0, CFG, "X")
    assert r["skip_reason"] == "no_price_at_post"


def test_horizon_incomplete_is_excluded():
    b, ts = bars_from(flat(5))
    r = T.score_one(sig(ts=ts[0] + 10), b, 0.0, {"horizon_hours": 24.0, "touch_hours": 1.0}, "X")
    assert r["skip_reason"] == "horizon_incomplete"


def test_basis_offset_shifts_tape():
    b, ts = bars_from(flat(25, B - 30))                     # futures tape B-30, stated entry B: offset +30 puts spot at B
    r = T.score_one(sig(ts=ts[0] + 10), b, 30.0, CFG, "X")
    assert r["variant"] == "market" and r["fill_price"] == pytest.approx(B)


def test_wilson_interval():
    lo, hi = T.wilson(5, 10)
    assert 0.23 < lo < 0.25 and 0.75 < hi < 0.78
    assert T.wilson(0, 0) == (None, None)
