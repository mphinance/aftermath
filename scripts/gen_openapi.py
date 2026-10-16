#!/usr/bin/env python3
"""Generate api/openapi.json, api/mcp-schema.json and the generated sections of
docs/API.md + docs/MCP.md from the real built api/*.json and mcp_server's tool list.

Source of truth: ENDPOINTS below (path, tag, summary, description, source file).
Response schemas are inferred from the built files. Counts come from data.
Registry entries whose source file is absent are skipped, so new collectors
(api/sentiment*.json etc.) appear automatically once the file exists.

Usage: python3 scripts/gen_openapi.py [--check-only]
Stdlib only.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = ROOT / "api"
SERVER = "https://ah.mphinance.com"
MAX_ITEMS = 100000     # array items merged when inferring a schema
EXAMPLE_ITEMS = 1     # array items kept in an example
MAX_DEPTH = 7

TAGS = [
    ("Market", "Macro tape: whale cash, daily P&L, allocation split and leaders."),
    ("Securities", "Equities and ETFs ranked by verified whale capital, owners and conviction."),
    ("Whales", "Verified high-capital portfolios and the clout-inversion (shadow) index."),
    ("Telegram Funnel", "Telegram channels linked to flagged accounts: callouts, scoring, live feed. Flag list curated by telegramscammers.com; flagged for investigation, not a finding of fraud."),
    ("MCP", "Model Context Protocol: live JSON-RPC endpoint and the tool catalog."),
]

# (path, tag, summary, description, source file relative to api/ or None, content type)
ENDPOINTS = [
    ("/api/market.json", "Market", "Macro tape",
     "Whale dry powder cash, intraday net P&L, equity/ETF/options allocation and the capital-inflow, retail-breadth, conviction and gainer leaders.",
     "market.json", None),
    ("/api/market-summary.json", "Market", "Macro tape (alias)",
     "Same payload as `/api/market.json`, kept as a stable alias.", "market-summary.json", None),
    ("/api/sentiment.json", "Market", "Sentiment",
     "Social sentiment from the AfterHour post archive: per-window summaries, buzz leaders and daily mention series.", "sentiment.json", None),
    ("/api/ah-posts.json", "Market", "Recent AfterHour posts",
     "Recent public community posts collected from the AfterHour app. Published when the collector has produced it.",
     "ah-posts.json", None),
    ("/api/whale-changes.json", "Whales", "Reported whale position changes",
     "Quantity changes (OPEN, ADD, TRIM, CLOSE, EXPIRED, FLIP) detected between polls of public whale portfolios, with notional and percent of portfolio. Positions are the last broker sync marked to live prices, so changes are rare.",
     "whale-changes.json", None),
    ("/api/whale-sync.json", "Whales", "Whale data freshness",
     "How fresh the whale position data is: whales tracked, recently polled, newest and oldest broker sync.",
     "whale-sync.json", None),
    ("/api/stonks.json", "Securities", "All tracked securities",
     "Every tracked security with owner counts, total platform value, whale capital, conviction intensity ($ per holder), session change and chatroom activity.",
     "stonks.json", None),
    ("/api/etfs.json", "Securities", "ETFs",
     "ETFs segregated from equities, with asset class, expense ratio and whale backing.", "etfs.json", None),
    ("/api/ticker/{symbol}.json", "Securities", "Ticker deep dive",
     "One security: its row, the verified whale holders, and daily OHLCV history bars. One file per tracked ticker.",
     "ticker/{symbol}.json", None),
    ("/api/whales.json", "Whales", "Verified whale portfolios",
     "High-capital portfolios with broker-verified positions, cash, P&L and shadow ratio. Large file (several MB uncompressed).",
     "whales.json", None),
    ("/api/shadow.json", "Whales", "Shadow whales (clout inversion)",
     "The same whales sorted by verified dollars per follower: big capital, tiny following. Large file.", "shadow.json", None),
    ("/api/funnel.json", "Telegram Funnel", "Flagged accounts",
     "Accounts on the telegramscammers.com flag list, enriched with public Telegram recon. Wording: flagged for investigation, not a finding of fraud.",
     "funnel.json", None),
    ("/api/funnel-tickers.json", "Telegram Funnel", "Funnel ticker rankings",
     "Tickers most mentioned across funnel channels.", "funnel-tickers.json", None),
    ("/api/funnel-calls.json", "Telegram Funnel", "Parsed callouts (recent)",
     "Parsed trade callouts from funnel channels. Quoted results are channel claims, unverified.", "funnel-calls.json", None),
    ("/api/funnel-calls-full.json", "Telegram Funnel", "Parsed callouts (full archive, JSON)",
     "Full callout archive including scoring fields. Large file.", "funnel-calls-full.json", None),
    ("/api/funnel-calls-full.csv", "Telegram Funnel", "Parsed callouts (full archive, CSV)",
     "The full callout archive as CSV, one row per callout. Large file.", "funnel-calls-full.csv", "text/csv"),
    ("/api/funnel-option-paths.json", "Telegram Funnel", "Option price paths",
     "What each called option contract did after the post (5-minute trade bars), with sample sizes and coverage.",
     "funnel-option-paths.json", None),
    ("/api/funnel-scorecard.json", "Telegram Funnel", "Scorecard",
     "Pooled and per-channel scoring: option paths, hold-to-expiry, and forex/gold/index TP1-first vs SL-first, with Wilson 95% ranges beside every rate.",
     "funnel-scorecard.json", None),
    ("/api/funnel-fx-signals.json", "Telegram Funnel", "Forex / gold / index signals",
     "Parsed and scored forex, gold and index signals from funnel channels.", "funnel-fx-signals.json", None),
    ("/api/funnel-live.json", "Telegram Funnel", "Live feed",
     "Last 72 hours of parsed, unscored callouts and hot tickers. Refreshed every few minutes on market days.",
     "funnel-live.json", None),
    ("/api/mcp-schema.json", "MCP", "MCP tool and resource catalog",
     "Tool definitions (name, description, inputSchema) and resources, generated from the server code.", "mcp-schema.json", None),
    ("/api/openapi.json", "MCP", "This OpenAPI document",
     "The OpenAPI 3.1 specification, generated by `scripts/gen_openapi.py` from the built files.", "openapi.json", None),
]


# --------------------------------------------------------------------------- inference
def _type_of(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "integer"
    if isinstance(v, float):
        return "number"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        return "array"
    return "object"


def _merge_types(a, b):
    s = set(a) | set(b)
    if "integer" in s and "number" in s:
        s.discard("integer")
    return sorted(s)


_MAPKEY = re.compile(r"[A-Z0-9][A-Z0-9.\-^=/]{0,11}|\d{4}-\d\d-\d\d")


def _is_map(keys):
    """Dict keyed by data (tickers, dates) rather than fixed field names."""
    return len(keys) >= 5 and all(_MAPKEY.fullmatch(k) for k in keys)


def infer(values, depth=0):
    """Infer one schema from a list of sample values."""
    types, props, req, item_samples = [], {}, None, []
    obj_samples = []
    for v in values:
        t = _type_of(v)
        types = _merge_types(types, [t])
        if t == "object":
            obj_samples.append(v)
        elif t == "array":
            item_samples.extend(v[:MAX_ITEMS])
    schema = {"type": types[0] if len(types) == 1 else types}
    if obj_samples and depth < MAX_DEPTH:
        keys = {}
        for o in obj_samples:
            for k, v in o.items():
                keys.setdefault(k, []).append(v)
        # only dict keys that look like data fields (not 500 unique symbols)
        if _is_map(keys):
            vals = [v for o in obj_samples for v in o.values()]
            schema["additionalProperties"] = infer(vals[:MAX_ITEMS], depth + 1)
        else:
            schema["properties"] = {k: infer(v, depth + 1) for k, v in keys.items()}
            n = len(obj_samples)
            req = [k for k, v in keys.items() if len(v) == n]
            if req:
                schema["required"] = req
    if item_samples and depth < MAX_DEPTH:
        schema["items"] = infer(item_samples[:MAX_ITEMS], depth + 1)
    elif "array" in types and depth < MAX_DEPTH:
        schema["items"] = {}
    return schema


def truncate(v, depth=0):
    """Small, real example: first array item, long strings clipped."""
    if isinstance(v, list):
        return [truncate(x, depth + 1) for x in v[:EXAMPLE_ITEMS]]
    if isinstance(v, dict):
        if depth > 5:
            return {}
        n = 2 if _is_map(v) else 40
        return {k: truncate(x, depth + 1) for k, x in list(v.items())[:n]}
    if isinstance(v, str) and len(v) > 160:
        return v[:157] + "..."
    return v


# --------------------------------------------------------------------------- mcp
def load_mcp():
    sys.path.insert(0, str(ROOT))
    import mcp_server  # noqa: WPS433
    return list(mcp_server.MCP_TOOLS_DEFINITIONS), list(mcp_server.MCP_RESOURCES_DEFINITIONS)


def build_mcp_schema(tools, resources):
    return {
        "version": "1.0.0",
        "protocolVersion": "2024-11-05",
        "server": {
            "name": "aftermath-altdata",
            "description": "AfterMath Model Context Protocol (MCP) Server for verified whale tape, conviction flows and Telegram-funnel scoring.",
            "documentation": SERVER + "/mcp",
            "serverScript": SERVER + "/mcp/server.py",
            "endpoint": SERVER + "/api/mcp",
        },
        "toolCount": len(tools),
        "tools": tools,
        "resources": resources,
    }


def example_args(tool):
    """Valid-looking example arguments from the tool's inputSchema."""
    out = {}
    schema = tool.get("inputSchema") or {}
    for name, p in (schema.get("properties") or {}).items():
        if "default" in p:
            val = p["default"]
        elif p.get("enum"):
            val = p["enum"][0]
        elif p.get("examples"):
            val = p["examples"][0]
        elif p.get("type") == "integer":
            val = p.get("minimum", 10)
        elif p.get("type") == "number":
            val = p.get("minimum", 1.0)
        elif p.get("type") == "boolean":
            val = False
        elif p.get("type") == "array":
            val = []
        elif p.get("type") == "object":
            val = {}
        else:
            val = {"ticker": "NVDA", "symbol": "NVDA", "username": "skrt"}.get(name, "example")
        if name in (schema.get("required") or []) or "default" in p or name in ("limit", "ticker", "symbol", "username"):
            out[name] = val
    return out


def pick_example_tool(tools):
    for t in tools:
        if t["name"] == "get_market_tape":
            return t
    return tools[0] if tools else {"name": "get_market_tape", "inputSchema": {}}


# --------------------------------------------------------------------------- spec
def schema_name(path):
    base = path.rsplit("/", 1)[-1].replace("{symbol}", "ticker")
    base = re.sub(r"\.(json|csv)$", "", base)
    return "".join(p.capitalize() for p in re.split(r"[-_]", base)) or "Root"


def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def resolve_source(rel):
    """Return a Path to the real file for a registry source, or None if absent."""
    if "{symbol}" in rel:
        sym = sample_symbol()
        p = API / rel.replace("{symbol}", sym)
        return p if p.exists() else None
    p = API / rel
    return p if p.exists() else None


def sample_symbol():
    try:
        sec = load_json(API / "stonks.json")["securities"]
        for s in sec:
            if (API / "ticker" / f"{s['ticker']}.json").exists():
                return s["ticker"]
    except Exception:
        pass
    files = sorted((API / "ticker").glob("*.json")) if (API / "ticker").exists() else []
    return files[0].stem if files else "NVDA"


def count_phrase(rel, data):
    """Data-derived size note for descriptions, e.g. '500 securities'."""
    if isinstance(data, dict):
        for k in ("securities", "whales", "signals", "calls", "accounts"):
            if isinstance(data.get(k), list):
                return f"{len(data[k])} {k}"
        if isinstance(data.get("total"), int):
            return f"{data['total']} records"
        if isinstance(data.get("count"), int):
            return f"{data['count']} records"
    return None


def build_openapi(tools=None, resources=None):
    if tools is None:
        tools, resources = load_mcp()
    schemas, paths, used_tags = {}, {}, set()
    sym = sample_symbol()

    for path, tag, summary, desc, rel, ctype in ENDPOINTS:
        src = resolve_source(rel)
        if src is None:
            continue
        used_tags.add(tag)
        op = {"tags": [tag], "summary": summary, "operationId": "get_" + re.sub(r"\W+", "_", path).strip("_")}
        if ctype == "text/csv":
            size_note = f"{sum(1 for _ in open(src, 'rb')) - 1} rows"
            op["description"] = f"{desc} Currently {size_note}."
            op["responses"] = {"200": {"description": "CSV file", "content": {"text/csv": {"schema": {"type": "string"}}}}}
        else:
            data = load_json(src)
            if rel == "openapi.json":
                data = {"openapi": "3.1.0", "info": {}, "paths": {}, "components": {}}
            note = count_phrase(rel, data)
            op["description"] = desc + (f" Currently {note}." if note else "")
            name = schema_name(path)
            sch = infer([data])
            sch["description"] = f"Inferred from the built file api/{rel.replace('{symbol}', sym)}."
            schemas[name] = sch
            op["responses"] = {"200": {"description": "OK", "content": {"application/json": {
                "schema": {"$ref": f"#/components/schemas/{name}"},
                "example": truncate(data)}}}}
        if "{symbol}" in path:
            op["parameters"] = [{"name": "symbol", "in": "path", "required": True,
                                 "description": "Ticker symbol, upper case (any ticker listed in /api/stonks.json).",
                                 "schema": {"type": "string"}, "example": sym}]
            op["responses"]["404"] = {"description": "Ticker not tracked"}
        paths[path] = {"get": op}

    # MCP JSON-RPC
    tool = pick_example_tool(tools)
    args = example_args(tool)
    names = ", ".join(f"`{t['name']}`" for t in tools)
    rpc_ex = {
        "tools_list": {"summary": "List all tools", "value": {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}},
        "tools_call": {"summary": f"Call {tool['name']}", "value": {
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": tool["name"], "arguments": args}}},
        "initialize": {"summary": "Initialize", "value": {
            "jsonrpc": "2.0", "id": 0, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "curl", "version": "1.0"}}}},
    }
    schemas["JsonRpcRequest"] = {
        "type": "object", "required": ["jsonrpc", "method"],
        "properties": {
            "jsonrpc": {"type": "string", "enum": ["2.0"]},
            "id": {"type": ["integer", "string", "null"]},
            "method": {"type": "string", "description": "initialize, tools/list, tools/call, resources/list, resources/read, ping"},
            "params": {"type": "object"}}}
    schemas["JsonRpcResponse"] = {
        "type": "object", "required": ["jsonrpc"],
        "properties": {"jsonrpc": {"type": "string"}, "id": {"type": ["integer", "string", "null"]},
                       "result": {"type": "object"},
                       "error": {"type": "object", "properties": {"code": {"type": "integer"}, "message": {"type": "string"}}}}}
    paths["/api/mcp"] = {"post": {
        "tags": ["MCP"], "summary": "MCP JSON-RPC 2.0 (live)", "operationId": "post_api_mcp",
        "description": f"Stateless Streamable-HTTP MCP endpoint. Send JSON-RPC 2.0 `tools/list` or `tools/call`. {len(tools)} tools: {names}. Not a static file: this one runs the live server code.",
        "requestBody": {"required": True, "content": {"application/json": {
            "schema": {"$ref": "#/components/schemas/JsonRpcRequest"}, "examples": rpc_ex}}},
        "responses": {"200": {"description": "JSON-RPC response", "content": {"application/json": {
            "schema": {"$ref": "#/components/schemas/JsonRpcResponse"}}}}}}}
    used_tags.add("MCP")

    return {
        "openapi": "3.1.0",
        "info": {
            "title": "AfterMath Alt-Data API",
            "version": "1.0.0",
            "description": ("Public, keyless JSON over HTTPS plus a live MCP endpoint. "
                            "Verified whale and retail positioning from the AfterHour social trading app, "
                            "and public scoring of Telegram trade callouts. Generated from the built data files; "
                            "not investment advice."),
            "contact": {"name": "Momentum Phinance", "url": SERVER},
        },
        "servers": [{"url": SERVER, "description": "Production"}],
        "tags": [{"name": n, "description": d} for n, d in TAGS if n in used_tags],
        "paths": paths,
        "components": {"schemas": schemas},
    }


# --------------------------------------------------------------------------- markdown
BEGIN, END = "<!-- BEGIN GENERATED -->", "<!-- END GENERATED -->"


def md_api(spec):
    out = []
    by_tag = {}
    for p, ops in spec["paths"].items():
        for m, op in ops.items():
            by_tag.setdefault(op["tags"][0], []).append((m.upper(), p, op))
    n = 1
    for tag in [t["name"] for t in spec["tags"]]:
        out.append(f"### {tag}\n")
        for m, p, op in by_tag.get(tag, []):
            out.append(f"#### {n}. {op['summary']}\n")
            out.append(f"- **Path**: `{m} {p}`")
            out.append(f"- **Description**: {op['description']}")
            if m == "GET":
                url = SERVER + p.replace("{symbol}", "NVDA")
                out.append(f"- **Request**: `curl -sL {url}`")
                ref = op["responses"]["200"]["content"].get("application/json", {}).get("schema", {}).get("$ref")
                if ref:
                    sch = spec["components"]["schemas"][ref.rsplit("/", 1)[-1]]
                    props = sch.get("properties") or {}
                    if props:
                        out.append("- **Top-level fields**: " + ", ".join(
                            f"`{k}` ({_t(v)})" for k, v in props.items()))
            else:
                ex = op["requestBody"]["content"]["application/json"]["examples"]["tools_call"]["value"]
                out.append("- **Request**:\n  ```bash\n  curl -s -X POST " + SERVER + "/api/mcp \\\n    -H 'Content-Type: application/json' \\\n    -d '" + json.dumps(ex) + "'\n  ```")
            out.append("")
            n += 1
    out.append("_Generated by `scripts/gen_openapi.py` from the built files. Full schemas: [/api/openapi.json](" + SERVER + "/api/openapi.json) or the [Swagger UI](" + SERVER + "/docs)._")
    return "\n".join(out)


def _t(s):
    t = s.get("type", "any")
    return "/".join(t) if isinstance(t, list) else t


def md_mcp(tools, resources):
    out = [f"**{len(tools)} tools**, generated from `mcp_server.py` (`api/mcp-schema.json`).\n"]
    for i, t in enumerate(tools, 1):
        out.append(f"### {i}. `{t['name']}`\n")
        out.append(t.get("description", "").strip() + "\n")
        props = (t.get("inputSchema") or {}).get("properties") or {}
        req = set((t.get("inputSchema") or {}).get("required") or [])
        if props:
            out.append("| Parameter | Type | Required | Description |")
            out.append("|---|---|---|---|")
            for k, v in props.items():
                d = (v.get("description") or "").replace("|", "\\|").replace("\n", " ")
                if v.get("enum"):
                    d += f" One of: {', '.join('`%s`' % e for e in v['enum'])}."
                if "default" in v:
                    d += f" Default `{json.dumps(v['default'])}`."
                out.append(f"| `{k}` | {_t(v)} | {'yes' if k in req else 'no'} | {d.strip()} |")
        else:
            out.append("_No parameters._")
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                           "params": {"name": t["name"], "arguments": example_args(t)}})
        out.append("\n```bash\ncurl -s -X POST " + SERVER + "/api/mcp -H 'Content-Type: application/json' \\\n  -d '" + body + "'\n```\n")
    if resources:
        out.append("### Resources\n")
        out.append("| URI | Name | Description |")
        out.append("|---|---|---|")
        for r in resources:
            out.append(f"| `{r['uri']}` | {r['name']} | {r.get('description', '')} |")
    return "\n".join(out)


def splice(path, body):
    text = path.read_text(encoding="utf-8")
    block = f"{BEGIN}\n{body}\n{END}"
    if BEGIN in text and END in text:
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda m: block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def write_all():
    tools, resources = load_mcp()
    (API / "mcp-schema.json").write_text(json.dumps(build_mcp_schema(tools, resources), indent=2), encoding="utf-8")
    spec = build_openapi(tools, resources)
    (API / "openapi.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
    splice(ROOT / "docs" / "API.md", md_api(spec))
    splice(ROOT / "docs" / "MCP.md", md_mcp(tools, resources))
    print(f"[+] openapi.json: {len(spec['paths'])} paths, {len(spec['components']['schemas'])} schemas; mcp-schema.json: {len(tools)} tools")
    return spec


if __name__ == "__main__":
    write_all()
