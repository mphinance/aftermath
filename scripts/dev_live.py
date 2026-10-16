#!/usr/bin/env python3
"""Local dev server for /live: serves the repo and mimics the nginx /ah/ whitelist proxy (GET only, no auth forwarded).

  python3 scripts/dev_live.py [port]    # default 8770, then open http://localhost:8770/live/
"""
import http.server, re, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOW = re.compile(r"^(social/feed|stonks/tickers/prices|stonks/security/(?:leaderboard|trending)|stonks/market/hours/[0-9-]+|"
                   r"stonks/security/ticker/[A-Za-z0-9.^=-]+|stonks/security/sec_[0-9a-f]{32}/historic_prices|public/profile|"
                   r"public/post/[A-Za-z0-9]+|stonks/public/portfolio/prf_[0-9a-f]{32}/summary/live)$")
_cache = {}


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def do_GET(self):
        if self.path.startswith("/ah/"):
            path, _, qs = self.path[4:].partition("?")
            if not ALLOW.match(path):
                self.send_error(404)
                return
            url = f"https://api.afterhour.com/{path}" + (f"?{qs}" if qs else "")
            hit = _cache.get(url)
            if hit and time.time() - hit[0] < 3:
                body, code = hit[1], 200
            else:
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "AfterMath-Live-dev/1.0"})
                    with urllib.request.urlopen(req, timeout=25) as r:
                        body, code = r.read(), r.status
                    _cache[url] = (time.time(), body)
                except urllib.error.HTTPError as e:
                    body, code = e.read(), e.code
                except Exception:
                    body, code = b'{"message":"upstream error"}', 502
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/mcp":
            self.send_error(404)
            return
        import json
        sys.path.insert(0, str(ROOT))
        import mcp_server
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        payload, ok = mcp_server.handle_jsonrpc_payload(json.loads(body or b"{}"))
        out = json.dumps(payload).encode() if ok else b""
        self.send_response(200 if ok else 202)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8770
    print(f"http://localhost:{port}/live/")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
