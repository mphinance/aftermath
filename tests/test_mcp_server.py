"""
Regression tests for the AfterMath MCP server.

Guards the two things that silently broke the Google Antigravity (and other
2025-era) clients:

1. ``initialize`` must echo a supported ``protocolVersion``. Antigravity requires
   ``>= 2025-03-26`` and closes the connection ("invalid request") when the
   server hard-codes the legacy ``2024-11-05``.
2. ``tools/list`` must expose the full tool registry.
3. Streamable HTTP (``/api/mcp``) must answer requests with JSON and
   notification-only messages with an empty ``202``.

No network: everything runs against ``handle_jsonrpc`` in-process or an
ephemeral local HTTP server.
"""
from __future__ import annotations

import http.server
import json
import os
import sys
import threading
import urllib.error
import urllib.request

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mcp_server  # noqa: E402


def _initialize(version):
    return mcp_server.handle_jsonrpc(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": version, "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}},
        }
    )


@pytest.mark.parametrize("version", mcp_server.SUPPORTED_PROTOCOL_VERSIONS)
def test_initialize_echoes_supported_protocol_version(version):
    assert _initialize(version)["result"]["protocolVersion"] == version


def test_initialize_falls_back_to_newest_for_unknown_version():
    assert _initialize("1999-01-01")["result"]["protocolVersion"] == mcp_server.DEFAULT_PROTOCOL_VERSION


def test_initialize_never_downgrades_a_2025_client():
    # The exact regression Antigravity hit: ask for a modern version, get it back.
    negotiated = _initialize("2025-06-18")["result"]["protocolVersion"]
    assert negotiated >= "2025-03-26"


def test_tools_list_returns_every_registered_tool():
    resp = mcp_server.handle_jsonrpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    assert {t["name"] for t in resp["result"]["tools"]} == set(mcp_server.TOOLS_MAP)


def test_prompts_list_and_get():
    resp = mcp_server.handle_jsonrpc({"jsonrpc": "2.0", "id": 3, "method": "prompts/list", "params": {}})
    prompts = resp["result"]["prompts"]
    assert len(prompts) >= 3
    assert {p["name"] for p in prompts} >= {"whale_dossier", "conviction_hunt", "shadow_whale_intel"}

    # Test prompts/get for whale_dossier
    get_resp = mcp_server.handle_jsonrpc({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "prompts/get",
        "params": {"name": "whale_dossier", "arguments": {"username": "SIRJACK"}}
    })
    assert "messages" in get_resp["result"]
    assert "SIRJACK" in get_resp["result"]["messages"][0]["content"]["text"]


def test_resources_templates_empty():
    resp = mcp_server.handle_jsonrpc({"jsonrpc": "2.0", "id": 5, "method": "resources/templates/list", "params": {}})
    assert resp["result"]["resourceTemplates"] == []


def test_resources_list_and_read():
    resp = mcp_server.handle_jsonrpc({"jsonrpc": "2.0", "id": 6, "method": "resources/list", "params": {}})
    uris = {r["uri"] for r in resp["result"]["resources"]}
    assert "aftermath://market-tape" in uris
    assert "aftermath://shadow-whales" in uris
    assert "aftermath://social-feed" in uris


def test_notifications_get_no_response():
    assert mcp_server.handle_jsonrpc({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_mixed_batch_drops_notifications_but_answers_requests():
    payload, had_response = mcp_server.handle_jsonrpc_payload(
        [
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 7, "method": "ping"},
        ]
    )
    assert had_response is True
    assert payload == [{"jsonrpc": "2.0", "id": 7, "result": {}}]


def test_notification_only_batch_produces_no_response():
    payload, had_response = mcp_server.handle_jsonrpc_payload(
        [{"jsonrpc": "2.0", "method": "notifications/initialized"}]
    )
    assert had_response is False
    assert payload is None


@pytest.fixture
def http_base():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), mcp_server.McpHttpHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _post(base, payload):
    req = urllib.request.Request(
        base + "/api/mcp",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    return urllib.request.urlopen(req, timeout=10)


def test_streamable_http_answers_request_with_negotiated_version(http_base):
    with _post(
        http_base,
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26"}},
    ) as resp:
        assert resp.status == 200
        body = json.loads(resp.read())
    assert body["result"]["protocolVersion"] == "2025-03-26"


def test_streamable_http_acknowledges_notification_with_202(http_base):
    with _post(http_base, {"jsonrpc": "2.0", "method": "notifications/initialized"}) as resp:
        assert resp.status == 202
        assert resp.read() == b""


def test_streamable_http_get_reports_405_not_404(http_base):
    with pytest.raises(urllib.error.HTTPError) as excinfo:
        urllib.request.urlopen(http_base + "/api/mcp", timeout=10)
    assert excinfo.value.code == 405


@pytest.mark.parametrize("path", ["/health", "/status", "/api/health", "/api/mcp/health"])
def test_health_endpoint_returns_json_status(http_base, path):
    req = urllib.request.Request(http_base + path)
    with urllib.request.urlopen(req, timeout=10) as resp:
        assert resp.status == 200
        assert "application/json" in resp.headers.get("Content-Type", "")
        data = json.loads(resp.read().decode("utf-8"))
    assert data["status"] == "ok"
    assert data["server"] == "aftermath-altdata"
    assert "uptime_seconds" in data
    assert "protocols" in data


def test_head_method_supported_on_health_and_sse(http_base):
    for path, expected_status in [("/health", 200), ("/api/health", 200), ("/api/mcp", 405)]:
        req = urllib.request.Request(http_base + path, method="HEAD")
        if expected_status == 405:
            with pytest.raises(urllib.error.HTTPError) as excinfo:
                urllib.request.urlopen(req, timeout=10)
            assert excinfo.value.code == 405
        else:
            with urllib.request.urlopen(req, timeout=10) as resp:
                assert resp.status == expected_status



# --- funnel callouts / tickers -------------------------------------------------

_CALLS = {
    "credit": "https://telegramscammers.com", "disclaimer": "Flagged for investigation, not a finding of fraud.",
    "quoted_results_are_channel_claims": "note", "small_sample_warning": "small", "total_parsed": 3,
    "calls": [
        {"channel": "t.me/alpha", "ticker": "SPY", "action": "open", "posted": "2026-10-02"},
        {"channel": "t.me/alpha", "ticker": "SPY", "action": "close", "posted": "2026-10-03", "result_pct": 50.0},
        {"channel": "t.me/beta", "ticker": "NVDA", "action": "open", "posted": "2026-10-04"},
    ],
}
_TICKERS = {"credit": "https://telegramscammers.com", "disclaimer": "d",
            "tickers": [{"ticker": "SPY", "tg_posts": 5}, {"ticker": "QQQ", "tg_posts": 2}]}


def _patch_fetch(monkeypatch, files):
    monkeypatch.setattr(mcp_server, "fetch_json", lambda name: files.get(name))


def test_funnel_tools_registered_and_defined():
    names = {t["name"] for t in mcp_server.MCP_TOOLS_DEFINITIONS}
    assert {"get_funnel_callouts", "get_funnel_tickers", "get_funnel_scorecard"} <= names
    assert len(mcp_server.TOOLS_MAP) == len(mcp_server.MCP_TOOLS_DEFINITIONS) == 14


def test_funnel_callouts_happy_path(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-calls.json": _CALLS})
    out = mcp_server.tool_get_funnel_callouts({"ticker": "$spy", "limit": 1})
    assert out["matched"] == 2 and len(out["callouts"]) == 1
    assert out["ticker_counts"] == {"SPY": 2}
    assert out["source"] == "https://telegramscammers.com"
    assert "not a finding of fraud" in out["disclaimer"]
    only_close = mcp_server.tool_get_funnel_callouts({"action": "close", "channel": "t.me/alpha"})
    assert only_close["matched"] == 1


def test_funnel_callouts_empty_match(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-calls.json": _CALLS})
    out = mcp_server.tool_get_funnel_callouts({"ticker": "ZZZZ"})
    assert out["matched"] == 0 and out["callouts"] == [] and out["ticker_counts"] == {}
    assert out["source"] == "https://telegramscammers.com"


def test_funnel_callouts_missing_file(monkeypatch):
    _patch_fetch(monkeypatch, {})
    assert "error" in mcp_server.tool_get_funnel_callouts({})


def test_funnel_tickers_happy_path_and_limit(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-tickers.json": _TICKERS})
    out = mcp_server.tool_get_funnel_tickers({"limit": 1})
    assert out["total_tickers"] == 2 and [t["ticker"] for t in out["tickers"]] == ["SPY"]
    assert out["source"] == "https://telegramscammers.com"


def test_funnel_tickers_empty_and_missing(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-tickers.json": {"tickers": []}})
    out = mcp_server.tool_get_funnel_tickers({})
    assert out["tickers"] == [] and out["source"] == "https://telegramscammers.com"
    _patch_fetch(monkeypatch, {})
    assert "error" in mcp_server.tool_get_funnel_tickers({})


_SCORE = {
    "credit": "https://telegramscammers.com", "disclaimer": "flagged for investigation, not a finding of fraud",
    "generated_at": "2026-10-14T00:00:00Z", "methodology": "https://ah.mphinance.com/scorecard",
    "options": {"pooled": {"n_scored": 10}, "by_channel": [{"channel": "t.me/alpha", "n_scored": 6}, {"channel": "t.me/beta", "n_scored": 4}]},
    "fx": {"pooled": {"market_fill_n": 5}, "by_channel": [{"channel": "t.me/alpha"}, {"channel": "t.me/beta"}],
           "weekly_by_channel": [{"channel": "t.me/alpha"}], "content_timeline": [{"channel": "t.me/beta"}],
           "touch_variant": {"n": 1, "by_channel": [{"channel": "t.me/alpha"}]}},
}


def test_funnel_scorecard_sections_and_channel_filter(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-scorecard.json": _SCORE})
    both = mcp_server.tool_get_funnel_scorecard({})
    assert "options" in both and "fx" in both and both["source"] == "https://telegramscammers.com"
    assert "not a finding of fraud" in both["disclaimer"] and both["methodology"].endswith("/scorecard")
    only = mcp_server.tool_get_funnel_scorecard({"section": "OPTIONS", "channel": "https://t.me/ALPHA"})
    assert "fx" not in only and [r["channel"] for r in only["options"]["by_channel"]] == ["t.me/alpha"]
    fx = mcp_server.tool_get_funnel_scorecard({"section": "fx", "channel": "beta"})
    assert "options" not in fx and fx["fx"]["weekly_by_channel"] == [] and len(fx["fx"]["content_timeline"]) == 1
    assert fx["fx"]["touch_variant"]["by_channel"] == []


def test_funnel_scorecard_robust_inputs_and_missing(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-scorecard.json": _SCORE})
    out = mcp_server.tool_get_funnel_scorecard({"section": 5, "channel": ["x"]})
    assert out["section"] == "all"
    out = mcp_server.tool_get_funnel_scorecard({"section": None, "channel": None})
    assert out["channel_filter"] is None
    _patch_fetch(monkeypatch, {})
    assert "error" in mcp_server.tool_get_funnel_scorecard({})


_PATHS = {
    "credit": "https://telegramscammers.com", "disclaimer": "flagged for investigation, not a finding of fraud",
    "generated_at": "2026-10-14T00:00:00Z",
    "pooled": {"intraday": {"n": 30}, "daily": {"n": 2}},
    "by_channel": [{"channel": "t.me/alpha", "n": 20}, {"channel": "t.me/beta", "n": 10}],
}


def test_funnel_scorecard_paths_section_and_all(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-option-paths.json": _PATHS, "funnel-scorecard.json": _SCORE})
    p = mcp_server.tool_get_funnel_scorecard({"section": "PATHS", "channel": "@Beta"})
    assert p["section"] == "paths" and "options" not in p and "fx" not in p
    assert [r["channel"] for r in p["paths"]["by_channel"]] == ["t.me/beta"] and p["paths"]["pooled"]["intraday"]["n"] == 30
    assert "not a finding of fraud" in p["disclaimer"]
    both = mcp_server.tool_get_funnel_scorecard({})
    assert {"paths", "options", "fx"} <= set(both)


def test_funnel_scorecard_paths_missing_and_odd_inputs(monkeypatch):
    _patch_fetch(monkeypatch, {"funnel-scorecard.json": _SCORE})
    assert "error" in mcp_server.tool_get_funnel_scorecard({"section": "paths"})
    both = mcp_server.tool_get_funnel_scorecard({})                       # paths file missing: other sections still served
    assert "error" in both["paths"] and "options" in both
    _patch_fetch(monkeypatch, {"funnel-option-paths.json": _PATHS})
    out = mcp_server.tool_get_funnel_scorecard({"section": "paths", "channel": ["x"]})
    assert out["section"] == "paths" and "paths" in out
    assert "error" in mcp_server.tool_get_funnel_scorecard({"section": ["paths"], "channel": 7})            # odd type falls back to all
    assert "error" in mcp_server.tool_get_funnel_scorecard({"section": "all"})                              # scorecard file missing
    assert "error" in mcp_server.tool_get_funnel_scorecard(None)
