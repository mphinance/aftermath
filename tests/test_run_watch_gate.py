"""The publish gate embedded in scripts/run_watch.sh: fresh, populated, never shrinks."""
import json, re, subprocess, sys
from pathlib import Path

SRC = (Path(__file__).resolve().parent.parent / "scripts" / "run_watch.sh").read_text()
GATE = re.search(r"<<'PY'\n(.*?)\nPY\n", SRC, re.S).group(1)


def run(tmp, new, live, key, force="0"):
    n, l = tmp / "new.json", tmp / "live.json"
    n.write_text(json.dumps(new))
    if live is not None:
        l.write_text(json.dumps(live))
    elif l.exists():
        l.unlink()
    return subprocess.run([sys.executable, "-c", GATE, str(n), str(l), key, force], capture_output=True, text=True).returncode


def sc(o, f):
    return {"generated_at": "2026-10-14T00:00:00Z", "options": {"pooled": {"n_scored": o}}, "fx": {"pooled": {"n_signals_scored": f}}}


def test_thin_server_scorecard_does_not_replace_rich_live(tmp_path):
    assert run(tmp_path, sc(252, 3), sc(1146, 63), "scorecard") == 1


def test_growth_and_fx_ageout_are_allowed(tmp_path):
    assert run(tmp_path, sc(1300, 40), sc(1146, 63), "scorecard") == 0


def test_first_publish_and_empty_halves(tmp_path):
    assert run(tmp_path, sc(10, 2), None, "scorecard") == 0
    assert run(tmp_path, sc(10, 0), None, "scorecard") == 1


def test_calls_total_shrink_blocked_force_overrides(tmp_path):
    live = {"count": 1000, "total_parsed": 8571}
    new = {"count": 1000, "total_parsed": 2019}
    assert run(tmp_path, new, live, "count") == 1
    assert run(tmp_path, new, live, "count", force="1") == 0


def test_server_rebuild_cannot_strip_price_paths_from_full_export(tmp_path):
    live = {"count": 8958, "path_count": 1544}
    stripped = {"count": 9000, "path_count": 0}
    assert run(tmp_path, stripped, live, "callsfull") == 1
    assert run(tmp_path, {"count": 9000, "path_count": 1544}, live, "callsfull") == 0
    assert run(tmp_path, stripped, {"count": 8958}, "callsfull") == 0        # live has no paths yet: allowed
    assert run(tmp_path, stripped, None, "callsfull") == 0
    assert run(tmp_path, {"count": 0, "path_count": 0}, None, "callsfull") == 1
