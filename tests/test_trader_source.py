"""Trader-post source: parser, builder and puller. No network."""
import json
from pathlib import Path

import afterhour
import build_trader_signals as B
import pull_trader_posts as P

FIX = Path(__file__).parent / "fixtures" / "trader_feed_items.json"


def sig(body, title=""):
    return B.extract_signal({"title": title, "body": body, "id": "x", "date": "2026-01-01"})


def lv(s):
    return [(l["token"], l["value"]) for l in s["levels"]]


def test_range_and_second_token():
    s = sig("20-25VIX, 130 VVIX")
    assert lv(s) == [("VIX", 20.0), ("VIX", 25.0), ("VVIX", 130.0)]
    assert s["levels"][0]["context"] == "20-25VIX"
    assert s["instruments"] == ["VIX", "VVIX"]


def test_no_vol_token_no_signal():
    assert sig("Holding RIOT 2000 shares, 50/50 CC.") is None


def test_short_vol_direction_no_levels():
    s = sig("I would short vol here")
    assert s["direction"] == "short" and s["levels"] == []
    assert s["quote"] == "I would short vol here"


def test_number_near_non_vol_word_is_not_a_level():
    s = sig("VIX is interesting. Bought 500 shares of RIOT at 12 today.")
    assert s["levels"] == []
    assert sig("VIX up 5%")["levels"] == []


def test_vxx_not_double_counted_as_vx():
    s = sig("VXX 15 is where I add")
    assert s["instruments"] == ["VXX"]
    assert lv(s) == [("VXX", 15.0)]


def test_bare_vx_and_vxm():
    s = sig("/VX 18.5 and /VXM")
    assert s["instruments"] == ["VX", "VXM"] and lv(s) == [("VX", 18.5)]


def test_direction_rules():
    assert sig("Bought SVIX on the dip")["direction"] == "long"
    assert sig("Sold UVIX at open")["direction"] == "short"
    assert sig("Bought SVIX and sold UVIX")["direction"] == "none"
    assert sig("VIX looks high.")["direction"] == "none"
    assert sig("I sold my car. VIX is high.")["direction"] == "none"  # different sentence


def test_lowercase_move_is_not_a_token():
    assert sig("time to move on") is None
    assert sig("MOVE index at 95")["instruments"] == ["MOVE"]


def test_quote_truncated_to_280():
    s = sig("VIX " + "x" * 400)
    assert len(s["quote"]) == 280 and s["quote"].startswith("VIX")


def _posts():
    return sorted((afterhour.normalize(i) for i in json.loads(FIX.read_text())), key=lambda p: p["created_at"])


def test_builder_from_fixture(tmp_path):
    d = tmp_path / "cynce"
    d.mkdir()
    (d / "posts.json").write_text(json.dumps({"handle": "Cynce", "profile_id": "prf_1", "fetched_at": "t", "total": 2, "posts": _posts()}))
    out = tmp_path / "api" / "trader-signals.json"
    res = B.build(tmp_path, out)
    assert json.loads(out.read_text()) == res
    t = res["traders"][0]
    assert (t["handle"], t["post_count"], t["vol_post_count"]) == ("Cynce", 2, 1)
    assert (t["first_post"], t["last_post"]) == ("2025-02-02", "2026-03-10")
    s = t["signals"][0]
    assert s["id"] == "p2" and s["direction"] == "short" and s["share_url"].endswith("vol-check")
    assert ("VVIX", 130.0) in lv(s)


def test_puller_maps_normalize_output(tmp_path, monkeypatch):
    items = json.loads(FIX.read_text())
    seen = []
    monkeypatch.setattr(afterhour, "fetch_all_posts", lambda pid, *a, **k: seen.append(pid) or items)
    monkeypatch.setattr(afterhour, "profile_id", lambda h: (_ for _ in ()).throw(AssertionError("resolver used")))
    P.pull_trader({"handle": "Cynce", "profile_id": "prf_1", "kind": "volatility"}, tmp_path)
    assert seen == ["prf_1"]
    data = json.loads((tmp_path / "cynce" / "posts.json").read_text())
    assert (data["handle"], data["profile_id"], data["total"]) == ("Cynce", "prf_1", 2)
    assert [p["id"] for p in data["posts"]] == ["p1", "p2"]  # sorted by created_at
    assert data["posts"][1] == afterhour.normalize(items[0])
    assert data["fetched_at"]


def test_puller_dry_run_limit_and_isolation(tmp_path, monkeypatch, capsys):
    items = json.loads(FIX.read_text())
    monkeypatch.setattr(afterhour, "fetch_all_posts", lambda pid, *a, **k: items)
    r = P.pull_trader({"handle": "A", "profile_id": "p"}, tmp_path, dry_run=True)
    assert r["total"] == 2 and r["written"] == 0 and not list(tmp_path.iterdir())
    P.pull_trader({"handle": "A", "profile_id": "p"}, tmp_path, limit=1)
    assert len(json.loads((tmp_path / "a" / "posts.json").read_text())["posts"]) == 1

    def fake(pid, *a, **k):
        if pid == "bad":
            raise RuntimeError("boom")
        return items
    monkeypatch.setattr(afterhour, "fetch_all_posts", fake)
    wl = tmp_path / "wl.json"
    wl.write_text(json.dumps([{"handle": "Bad", "profile_id": "bad"}, {"handle": "Good", "profile_id": "ok"}]))
    rc = P.main(["--all", "--watchlist", str(wl), "--out", str(tmp_path / "o")])
    assert rc == 1 and (tmp_path / "o" / "good" / "posts.json").exists()
