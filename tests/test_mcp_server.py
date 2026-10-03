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


def test_empty_capability_probes_return_empty_lists():
    for method, key in (
        ("prompts/list", "prompts"),
        ("resources/templates/list", "resourceTemplates"),
    ):
        resp = mcp_server.handle_jsonrpc({"jsonrpc": "2.0", "id": 3, "method": method, "params": {}})
        assert resp["result"][key] == []


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

