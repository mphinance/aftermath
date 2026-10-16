#!/usr/bin/env python3
"""Docs consistency checks. Exit nonzero on any failure.

  python3 scripts/check_docs.py

Checks:
  1. every spec path with a local file validates against its component schema
  2. every api/*.json is in the spec or ALLOWLIST
  3. mcp_server.TOOLS_MAP names == api/mcp-schema.json names == MCP_TOOLS_DEFINITIONS names
  4. every "N tools" / "N production tools" string matches the real tool count
  5. forbidden strings are absent from api/, docs/, mcp/
Stdlib only; uses jsonschema when installed.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = ROOT / "api"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

ALLOWLIST = set()   # api/*.json files intentionally not in the spec
FORBIDDEN = ["/_ah/admin", "/mjolnir", "ah-user-id", "afterhour-openapi"]
FORBIDDEN_DIRS = ["api", "docs", "mcp"]
COUNT_FILES = ["README.md", "CLAUDE.md", "mcp_server.py", "mcp/index.html"]  # plus docs/*.md
OWNED = {"docs/API.md", "docs/MCP.md", "mcp/index.html"}  # files the docs overhaul owns; others are reported only
COUNT_RE = re.compile(r"\b(\d+)\s+(?:(?:production|live|quantitative|MCP|analysis)\s+)*tools\b", re.I)


# ------------------------------------------------------------------ validation
def _types(s):
    t = s.get("type")
    return None if t is None else (t if isinstance(t, list) else [t])


def _is(v, t):
    return {
        "null": v is None,
        "boolean": isinstance(v, bool),
        "integer": isinstance(v, int) and not isinstance(v, bool),
        "number": isinstance(v, (int, float)) and not isinstance(v, bool),
        "string": isinstance(v, str),
        "array": isinstance(v, list),
        "object": isinstance(v, dict),
    }[t]


def validate(v, s, spec, path="$", errs=None, limit=10):
    """Structural validator: $ref, type, required, properties, additionalProperties, items."""
    errs = [] if errs is None else errs
    if len(errs) >= limit:
        return errs
    if "$ref" in s:
        node = spec
        for part in s["$ref"].lstrip("#/").split("/"):
            node = node[part]
        return validate(v, node, spec, path, errs, limit)
    ts = _types(s)
    if ts and not any(_is(v, t) for t in ts):
        errs.append(f"{path}: expected {ts}, got {type(v).__name__}")
        return errs
    if isinstance(v, dict):
        for k in s.get("required", []):
            if k not in v:
                errs.append(f"{path}: missing required '{k}'")
        props = s.get("properties", {})
        ap = s.get("additionalProperties")
        for k, x in v.items():
            if k in props:
                validate(x, props[k], spec, f"{path}.{k}", errs, limit)
            elif isinstance(ap, dict):
                validate(x, ap, spec, f"{path}.{k}", errs, limit)
    elif isinstance(v, list) and "items" in s and s["items"]:
        for i, x in enumerate(v):
            validate(x, s["items"], spec, f"{path}[{i}]", errs, limit)
            if len(errs) >= limit:
                break
    return errs


def check_schemas(spec):
    out = []
    try:
        import jsonschema  # type: ignore
    except ImportError:
        jsonschema = None
    import gen_openapi
    for path, ops in spec["paths"].items():
        op = ops.get("get")
        if not op:
            continue
        ref = ((op["responses"]["200"].get("content") or {}).get("application/json") or {}).get("schema", {}).get("$ref")
        if not ref:
            continue
        rel = next((e[4] for e in gen_openapi.ENDPOINTS if e[0] == path), None)
        src = gen_openapi.resolve_source(rel) if rel else None
        if src is None:
            out.append(f"{path}: spec path has no local source file")
            continue
        data = json.load(open(src, encoding="utf-8"))
        if rel == "openapi.json":
            continue
        schema = {"$ref": ref}
        if jsonschema:
            full = {"$ref": ref, "components": spec["components"]}
            try:
                jsonschema.validate(data, full)
            except jsonschema.ValidationError as e:
                out.append(f"{path}: {e.message[:200]}")
        else:
            for e in validate(data, schema, spec):
                out.append(f"{path}: {e}")
    return out


# ------------------------------------------------------------------ checks
def check_api_coverage(spec):
    in_spec = {p.rsplit("/", 1)[-1] for p in spec["paths"]}
    out = []
    for f in sorted(API.iterdir()):
        if f.is_file() and f.suffix in (".json", ".csv") and f.name not in in_spec and f.name not in ALLOWLIST:
            out.append(f"api/{f.name} is neither in the OpenAPI spec nor the allowlist")
    return out


def check_tool_names():
    import mcp_server
    server = sorted(mcp_server.TOOLS_MAP)
    defs = sorted(t["name"] for t in mcp_server.MCP_TOOLS_DEFINITIONS)
    schema = sorted(t["name"] for t in json.load(open(API / "mcp-schema.json"))["tools"])
    out = []
    if server != schema:
        out.append(f"TOOLS_MAP vs mcp-schema.json differ: only in server {sorted(set(server) - set(schema))}, only in schema {sorted(set(schema) - set(server))}")
    if defs != server:
        out.append(f"MCP_TOOLS_DEFINITIONS vs TOOLS_MAP differ: {sorted(set(defs) ^ set(server))}")
    return out, len(server)


def count_targets():
    files = list(COUNT_FILES) + [f"docs/{p.name}" for p in sorted((ROOT / "docs").glob("*.md"))]
    return [f for f in dict.fromkeys(files) if (ROOT / f).exists()]


def check_counts(n):
    """Returns list of (file, message). Skips the generated blocks."""
    out = []
    for rel in count_targets():
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"<!-- BEGIN GENERATED -->.*?<!-- END GENERATED -->", "", text, flags=re.S)
        for i, line in enumerate(text.splitlines(), 1):
            for m in COUNT_RE.finditer(line):
                if int(m.group(1)) != n:
                    out.append((rel, f"{rel}: says '{m.group(0)}' but the server has {n} tools (~line {i})"))
    return out


def check_forbidden():
    out = []
    for d in FORBIDDEN_DIRS:
        for f in (ROOT / d).rglob("*"):
            if not f.is_file() or f.suffix in (".png", ".jpg", ".ico", ".zip", ".gz"):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for s in FORBIDDEN:
                if s in text:
                    out.append(f"{f.relative_to(ROOT)} contains forbidden string {s!r}")
    return out


def run():
    """Returns (owned_failures, reported_only)."""
    spec = json.load(open(API / "openapi.json"))
    fails, reports = [], []
    fails += check_schemas(spec)
    fails += check_api_coverage(spec)
    name_errs, n = check_tool_names()
    fails += name_errs
    for rel, msg in check_counts(n):
        (fails if rel in OWNED or rel.startswith("docs/") else reports).append(msg)
    fails += check_forbidden()
    return fails, reports, n


def main():
    fails, reports, n = run()
    print(f"tool count: {n}")
    for r in reports:
        print("REPORT (file not owned by docs overhaul):", r)
    for f in fails:
        print("FAIL:", f)
    bad = len(fails) + len(reports)
    print("OK" if not bad else f"{len(fails)} failure(s), {len(reports)} reported mismatch(es)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
