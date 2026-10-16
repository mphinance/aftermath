import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ah_whales as W


def leg(sym, q, px=10.0, **kw):
    base = {"accountId": "a1", "tickerSymbol": sym, "rootTickerSymbol": kw.pop("root", sym), "type": kw.pop("type", "EQUITY"),
            "quantity": q, "price": px, "value": q * px}
    base.update(kw)
    return base


def agg(*legs):
    return W.aggregate_legs(list(legs))


def test_open_add_trim_close():
    old = agg(leg("AAA", 100), leg("BBB", 100), leg("CCC", 100))
    new = agg(leg("AAA", 150), leg("BBB", 50), leg("DDD", 10))
    got = {c["symbol"]: c for c in W.diff_legs(old, new, "2026-10-16", 100000)}
    assert got["AAA"]["action"] == "ADD" and got["AAA"]["notional_delta"] == 500.0
    assert got["BBB"]["action"] == "TRIM" and got["BBB"]["notional_delta"] == -500.0
    assert got["CCC"]["action"] == "CLOSE" and got["DDD"]["action"] == "OPEN"
    assert got["AAA"]["pct_of_portfolio"] == 0.5


def test_noise_below_threshold_ignored():
    old = agg(leg("MF", 1000.0000))
    assert W.diff_legs(old, agg(leg("MF", 1000.0004)), "2026-10-16") == []
    assert W.diff_legs(old, agg(leg("MF", 1010.0)), "2026-10-16")[0]["action"] == "ADD"


def test_expired_option_not_close_and_contracts():
    o = leg("ASTS261015C00050000", 500, type="DERIVATIVE", rootTickerSymbol="ASTS", optionsContractType="CALL",
            optionsStrikePrice=50, optionsExpirationDate="2026-10-15T00:00:00.000Z", optionsSharesPerContract=100)
    c = W.diff_legs(agg(o), {}, "2026-10-16")[0]
    assert c["action"] == "EXPIRED" and c["contracts_delta"] == -5.0 and c["root"] == "ASTS"


def test_roll_heuristic_and_merged_flag():
    mk = lambda sym, exp, **kw: leg(sym, 100, type="DERIVATIVE", rootTickerSymbol="SPY", optionsContractType="CALL",
                                    optionsStrikePrice=700, optionsExpirationDate=exp, **kw)
    old = agg(mk("SPY_A", "2026-11-20T00:00:00.000Z", isMerged=True))
    new = agg(mk("SPY_B", "2026-12-18T00:00:00.000Z"))
    cs = W.diff_legs(old, new, "2026-10-16")
    assert all(c.get("possible_roll") for c in cs)
    assert next(c for c in cs if c["action"] == "CLOSE")["lot_ambiguous"] is True


def test_same_ticker_in_one_account_sums():
    assert agg(leg("AAA", 10), leg("AAA", 5))["a1|AAA|EQUITY"]["q"] == 15


def test_flip():
    assert W.diff_legs(agg(leg("S", 100)), agg(leg("S", -100)), "2026-10-16")[0]["action"] == "FLIP"
