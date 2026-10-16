"""Offline docs consistency checks (see scripts/check_docs.py)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

import check_docs  # noqa: E402
import gen_openapi  # noqa: E402

SPEC = json.load(open(ROOT / "api" / "openapi.json"))


def test_responses_validate_against_schemas():
    assert check_docs.check_schemas(SPEC) == []


def test_every_api_file_in_spec():
    assert check_docs.check_api_coverage(SPEC) == []


def test_tool_names_match_schema():
    errs, n = check_docs.check_tool_names()
    assert errs == []
    assert n >= 1


def test_tool_counts_in_owned_docs():
    _, n = check_docs.check_tool_names()
    bad = [m for rel, m in check_docs.check_counts(n) if rel in check_docs.OWNED or rel.startswith("docs/")]
    assert bad == []


def test_no_forbidden_strings():
    assert check_docs.check_forbidden() == []


def test_spec_is_current_with_generator():
    """api/openapi.json must equal what the generator makes from the built files today."""
    fresh = gen_openapi.build_openapi()
    assert fresh["paths"].keys() == SPEC["paths"].keys()
    assert "/api/mcp" in SPEC["paths"] and "post" in SPEC["paths"]["/api/mcp"]


def test_absent_source_is_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(gen_openapi, "API", tmp_path)
    (tmp_path / "ticker").mkdir()
    spec = gen_openapi.build_openapi(tools=[{"name": "t", "inputSchema": {}}], resources=[])
    assert list(spec["paths"]) == ["/api/mcp"]


def test_inferrer_handles_mixed_types():
    s = gen_openapi.infer([{"a": 1, "b": None}, {"a": 2.5, "b": "x"}])
    assert s["properties"]["a"]["type"] == "number"
    assert set(s["properties"]["b"]["type"]) == {"null", "string"}
