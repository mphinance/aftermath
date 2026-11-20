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
    """api/openapi.json must equal, byte for byte of content, what the generator makes today.

    The path set is declared in the generator (not discovered from disk), so this holds on a
    fresh clone as well as on a box with every gitignored runtime file present."""
    fresh = gen_openapi.build_openapi()
    assert fresh == SPEC
    assert "/api/mcp" in SPEC["paths"] and "post" in SPEC["paths"]["/api/mcp"]


def test_generated_docs_blocks_are_current():
    tools, resources = gen_openapi.load_mcp()
    spec = gen_openapi.build_openapi(tools, resources)
    for rel, body in (("docs/API.md", gen_openapi.md_api(spec)), ("docs/MCP.md", gen_openapi.md_mcp(tools, resources))):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert f"{gen_openapi.BEGIN}\n{body}\n{gen_openapi.END}" in text, f"{rel} generated block is stale: run scripts/gen_openapi.py"


def test_trader_signals_is_declared():
    assert "/api/trader-signals.json" in SPEC["paths"]


def test_runtime_artifacts_documented_without_reading_disk(tmp_path, monkeypatch):
    """A gitignored runtime file is in the spec with a fixed stub whether or not it exists."""
    monkeypatch.setattr(gen_openapi, "API", tmp_path)
    (tmp_path / "ticker").mkdir()
    for rel in gen_openapi.RUNTIME_ARTIFACTS:
        monkeypatch.setattr(gen_openapi, "ENDPOINTS", [e for e in gen_openapi.ENDPOINTS if e[4] in gen_openapi.RUNTIME_ARTIFACTS])
    spec = gen_openapi.build_openapi(tools=[{"name": "t", "inputSchema": {}}], resources=[])
    want = {e[0] for e in gen_openapi.ENDPOINTS if e[4] in gen_openapi.RUNTIME_ARTIFACTS}
    assert want and want <= set(spec["paths"])
    (tmp_path / "sentiment.json").write_text('{"x": 1}')
    assert gen_openapi.build_openapi(tools=[{"name": "t", "inputSchema": {}}], resources=[]) == spec


def test_missing_tracked_source_is_an_error(tmp_path, monkeypatch):
    """A declared, tracked endpoint whose file is gone must fail loudly, not silently drop the path."""
    import pytest
    monkeypatch.setattr(gen_openapi, "API", tmp_path)
    (tmp_path / "ticker").mkdir()
    with pytest.raises(FileNotFoundError):
        gen_openapi.build_openapi(tools=[{"name": "t", "inputSchema": {}}], resources=[])


def test_dormant_endpoints_are_not_published():
    assert not any(p.endswith(("whale-changes.json", "whale-sync.json")) for p in SPEC["paths"])


def test_inferrer_handles_mixed_types():
    s = gen_openapi.infer([{"a": 1, "b": None}, {"a": 2.5, "b": "x"}])
    assert s["properties"]["a"]["type"] == "number"
    assert set(s["properties"]["b"]["type"]) == {"null", "string"}
