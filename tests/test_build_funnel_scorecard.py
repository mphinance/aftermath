"""Tests for build_funnel_scorecard.py (synthetic fixtures only)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build_funnel_scorecard as bs  # noqa: E402


def test_wilson_known_values():
    lo, hi = bs.wilson(5, 10)
    assert abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3
    assert bs.wilson(0, 0) == [None, None]
    lo, hi = bs.wilson(0, 10)
    assert lo == 0.0 and 0.25 < hi < 0.32
    lo, hi = bs.wilson(10, 10)
    assert hi == 1.0 and lo > 0.68


def _opt(i, ch, win, ret, ticker="SPY"):
    return {"ids": [f"{ch}/{i}"], "channel": f"t.me/{ch}", "ticker": ticker, "side": "call", "strike": 100.0 + i,
            "expiry_effective": "2026-09-10", "posted": "2026-09-10T14:00:00+00:00", "entry_price": 1.0,
            "status": "scored", "return_pct": ret, "win": win, "worthless": ret == -100.0}


def test_small_n_flag_and_every_channel_listed():
    outs = [_opt(i, "big", i < 2, 50.0 if i < 2 else -100.0) for i in range(6)] + [_opt(1, "tiny", False, -100.0)]
    res = bs.build_options([], outs)
    by = {r["channel"]: r for r in res["by_channel"]}
    assert set(by) == {"t.me/big", "t.me/tiny"}
    assert by["t.me/tiny"]["small"] is True and by["t.me/big"]["small"] is False
    assert res["pooled"]["n_scored"] == 7
    assert by["t.me/big"]["win_ci"][0] is not None


def test_private_channels_dropped():
    outs = [_opt(1, "+abcdef", True, 10.0), _opt(2, "pub", True, 10.0)]
    outs[0]["channel"] = "t.me/+abcdef"
    res = bs.build_options([], outs)
    assert [r["channel"] for r in res["by_channel"]] == ["t.me/pub"]


def test_missing_inputs_degrade(tmp_path, monkeypatch):
    monkeypatch.setattr(bs, "API", tmp_path / "api")
    monkeypatch.setattr(bs, "TF", tmp_path / "nope")
    monkeypatch.setattr(bs, "FX_REPORT", tmp_path / "nope.md")
    bs.main()
    card = json.loads((tmp_path / "api" / "funnel-scorecard.json").read_text())
    sig = json.loads((tmp_path / "api" / "funnel-fx-signals.json").read_text())
    assert card["options"]["pooled"]["n_scored"] == 0 and card["fx"]["pooled"]["n_signals_scored"] == 0
    assert sig["signals"] == [] and "telegramscammers.com" in card["credit"]
    assert "not a finding of fraud" in card["disclaimer"]
    assert "—" not in json.dumps(card, ensure_ascii=False)


def _fx(i, hit, variant="market", ch="t.me/x"):
    return {"id": f"x/{i}", "channel": ch, "date": "2026-09-15T10:00:00+00:00", "text": "Gold buy—now", "instrument": "XAUUSD",
            "side": "buy", "entry_lo": 1.0, "entry_hi": 1.0, "sl": 0.9, "tps": [{"v": 1.1, "pips": False}], "status": "scored",
            "variant": variant, "n_tp": 1, "tps_hit": 1 if hit else 0, "tp1_hit": hit, "sl_first": not hit, "resolved": True,
            "ambiguous": False, "r_tp1": 1.0 if hit else -1.0, "r_last": 1.0 if hit else -1.0, "r_tp1_target": 1.0,
            "minutes_to_first_event": 10.0, "outcome": "tp1" if hit else "sl"}


def test_fx_stats_and_touch_not_pooled():
    rows = [_fx(i, i % 2 == 0) for i in range(4)] + [_fx(9, True, "touch")]
    res = bs.build_fx(rows, [], "")
    p = res["pooled"]
    assert p["market_fill_n"] == 4 and p["touch_fill_n"] == 1 and p["tp1_hit_rate"] == 0.5
    assert p["breakeven_tp1_rate"] == 0.5 and p["mean_r_tp1"] == 0.0
    assert res["touch_variant"]["n"] == 1
    assert res["weekly_by_channel"] == []  # fewer than 30 scored


def test_signal_rows_truncate_and_scrub():
    r = _fx(1, True)
    r["text"] = "x" * 900
    out = bs.signal_rows([r, {"status": "skipped", "channel": "t.me/x"}])
    assert len(out) == 1 and len(out[0]["text"]) <= bs.SIGNAL_TEXT_LEN and out[0]["tps"] == [1.1]
    assert "—" not in bs.clean("a—b")


def test_sensitivity_parse():
    md = ("### 4c. Sensitivity\n\n| basis mode | g | t | a | s |\n|---|---|---|---|---:|\n"
          "| auto | n=44, 52%, -0.17, -0.18 | n=11, 36%, -0.39, -0.41 | n=51, 51%, -0.20 | 7 |\n"
          "| const | n=42, 45%, -0.29, -0.10 | n=14, 36%, -0.32, -0.14 | n=49, 45%, -0.31 | 7 |\n"
          "| none (raw) | n=0 | n=0 | n=3, 67%, -0.18 | 7 |\n\n## 5. next\n")
    s = bs.parse_sensitivity(md)
    assert len(s["rows"]) == 3 and s["range"]["tp1_hit_rate"] == [0.45, 0.52] and s["range"]["mean_r_tp1_same_sign"]
    assert bs.parse_sensitivity("") is None
