import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sync_upstream as su


def row(u, i, **kw):
    r = {"username": u, "listing_id": f"TS-{i:03d}", "tier": "reported", "telegram_links": [f"https://t.me/{u}chan"]}
    r.update(kw)
    return r


def test_validate_ok():
    assert su.validate([row("a", 1), row("b", 2)], 2) is None


def test_validate_rejects_duplicates_bad_tier_and_shrink():
    assert "duplicate" in su.validate([row("a", 1), row("A", 2)], 0)
    assert "duplicate" in su.validate([row("a", 1), row("b", 1)], 0)
    assert "tier" in su.validate([row("a", 1, tier="nope")], 0)
    assert "shrank" in su.validate([row("a", 1)], 10)
    assert su.validate([], 0) is not None and su.validate({"x": 1}, 0) is not None


def test_fill_derived_keeps_upstream_values():
    r = su.fill_derived([row("cont", 150, followers=7), row("b", 2, telegram_links_norm=["t.me/keep"], num_followers=3)])
    assert r[0]["telegram_links_norm"] == ["t.me/contchan"] and r[0]["num_followers"] == 7 and r[0]["profile_id"] is None
    assert r[1]["telegram_links_norm"] == ["t.me/keep"] and r[1]["num_followers"] == 3


def test_norm_link():
    assert su.norm_link("https://www.t.me/Foo/?x=1") == "t.me/foo"
    assert su.norm_link("https://telegram.me/+AbC") == "t.me/+abc"


def test_main_writes_only_when_valid(tmp_path, monkeypatch):
    f = tmp_path / "accounts.json"
    f.write_text(json.dumps([row("a", 1), row("b", 2)]))
    monkeypatch.setattr(su, "fetch", lambda url: [row("a", 1), row("b", 2), row("c", 3)])
    monkeypatch.setattr(sys, "argv", ["sync_upstream.py", "--file", str(f)])
    assert su.main() == 0 and len(json.loads(f.read_text())) == 3
    monkeypatch.setattr(su, "fetch", lambda url: [row("a", 1)])
    assert su.main() == 2 and len(json.loads(f.read_text())) == 3   # shrink refused, file untouched
    def boom(url): raise OSError("down")
    monkeypatch.setattr(su, "fetch", boom)
    assert su.main() == 2 and len(json.loads(f.read_text())) == 3
