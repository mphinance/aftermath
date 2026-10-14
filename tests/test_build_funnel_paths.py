"""Tests for build_funnel_paths.py (synthetic rows only)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build_funnel_paths as bp  # noqa: E402


def _row(i, ch="t.me/big", end=10.0, mfe=20.0, mae=-5.0, rule="none", cat="intraday", status="scored", quoted=0.0, vol=100,
         posted="2026-09-10T14:00:00+00:00"):
    r = {"id": f"{ch}/{i}", "channel": ch, "posted": posted, "ticker": "SPY", "status": status, "category": cat}
    if status == "scored":
        r.update(end_ret_pct=end, mfe_pct=mfe, mae_pct=mae, volume=vol, quoted_vs_fill_pct=quoted)
        for name, tp, sl in bp.RULES:
            ret = {"tp": tp * 100, "sl": -sl * 100}.get(rule, end)
            r[name] = rule
            r[name + "_ret"] = ret
    return r


def test_wilson_known_values():
    lo, hi = bp.wilson(5, 10)
    assert abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3
    assert bp.wilson(0, 0) == [None, None]
    lo, hi = bp.wilson(10, 10)
    assert hi == 1.0 and lo > 0.68


def test_rule_tallies_and_headline():
    rows = [_row(1, rule="tp"), _row(2, rule="tp"), _row(3, rule="sl", end=-50), _row(4, rule="none", end=-10), _row(5, rule="none", end=30)]
    t = {x["rule"]: x for x in bp.rule_table(rows)}["tp50_sl50"]
    assert (t["tp_first"], t["sl_first"], t["neither"]) == (2, 1, 2)
    assert t["tp_first_rate"] == 0.4 and t["tp_first_ci"][0] < 0.4 < t["tp_first_ci"][1]
    assert t["mean_return_pct"] == round((50 + 50 - 50 - 10 + 30) / 5, 1)
    b = bp.block(rows)
    assert b["n"] == 5 and b["ended_green"]["k"] == 3 and b["headline_rule"]["tp_first"] == 2
    assert len(b["rules"]) == 3


def test_small_flag_every_channel_and_private_dropped():
    rows = [_row(i, "t.me/big") for i in range(bp.SMALL_N)] + [_row(1, "t.me/tiny")] + [_row(2, "t.me/+hash")]
    rows.append(_row(3, "t.me/nobars", status="no_bars"))
    out = bp.build(rows, None, total_opens=10)
    by = {r["channel"]: r for r in out["by_channel"]}
    assert set(by) == {"t.me/big", "t.me/tiny"}
    assert by["t.me/tiny"]["small"] is True and by["t.me/big"]["small"] is False
    assert out["pooled"]["intraday"]["n"] == bp.SMALL_N + 1
    stages = {s["stage"]: s["n"] for s in out["coverage"]["stages"]}
    assert stages["Option open callouts (repeat posts removed)"] == 10 and stages["Scored from 5-minute bars"] == bp.SMALL_N + 1
    assert "+hash" not in json.dumps(out)


def test_quoted_realism_and_liquidity():
    rows = [_row(1, quoted=-40), _row(2, quoted=-10), _row(3, quoted=60), _row(4, quoted=0, vol=5)]
    r = bp.realism(rows)
    assert r["n"] == 4 and r["unfillable_quote_more_than_25pct_below_fill"]["k"] == 1
    assert r["within_25pct"]["k"] == 2 and r["quoted_more_than_25pct_above_fill"]["k"] == 1
    assert bp.liquidity(rows)["thin_under_20_contracts"]["k"] == 1


def test_daily_split_and_hours():
    rows = [_row(1), _row(2, cat="daily"), _row(3, posted="2026-09-10T13:35:00+00:00")]
    out = bp.build(rows, None)
    assert out["pooled"]["intraday"]["n"] == 2 and out["pooled"]["daily"]["n"] == 1
    hours = {h["hour_et"]: h["n"] for h in out["by_session_hour"]}
    assert hours == {10: 1, 9: 1}
    assert out["by_session_hour"][0]["hour"].startswith("09:30")


def test_empty_input_does_not_crash():
    out = bp.build([], None)
    assert out["pooled"]["intraday"]["n"] == 0 and out["pooled"]["intraday"]["ended_green"]["rate"] is None
    assert out["by_channel"] == []


def test_missing_input_leaves_previous_file(tmp_path, monkeypatch):
    prev = tmp_path / "prev.json"
    prev.write_text('{"keep": true}')
    monkeypatch.setattr(bp, "ROWS", tmp_path / "missing.jsonl")
    monkeypatch.setattr(bp, "OUT", prev)
    monkeypatch.setattr(bp, "TP", None)
    assert bp.main() == 0
    assert json.load(open(prev)) == {"keep": True}


def test_delay_sensitivity_reuses_previous_without_bars(monkeypatch):
    monkeypatch.setattr(bp, "TP", None)
    prev = {"delay_sensitivity": {"rows": [{"delay_bars": 0, "n": 3}], "note": "x"}}
    out = bp.delay_sensitivity([], prev)
    assert out["reused_from_previous"] is True and out["rows"][0]["n"] == 3
    assert bp.delay_sensitivity([], None)["rows"] == []


def test_robustness_counts_clustering_and_same_minute_repeats():
    rows = [_row(i, posted=f"2026-09-{10 + i % 7:02d}T14:{i % 50:02d}:00+00:00") for i in range(40)]
    rows.append(dict(rows[0], id="t.me/other/1"))          # same contract and minute as rows[0], other channel
    rb = bp.robustness(rows, rows)
    assert rb["n"] == 41 and rb["distinct_days"] == 7
    assert rb["extra_rows_same_contract_same_minute"] >= 1
    assert rb["without_same_minute_duplicates"]["n"] == 41 - rb["extra_rows_same_contract_same_minute"]
    lo, hi = rb["cluster_by_day_95_range"]["ended_green"]
    assert lo is not None and lo <= hi
    assert bp.fill_gap([dict(r, fill_gap_s=g) for r, g in zip(rows, range(100, 141))])["median_s"] == 120
