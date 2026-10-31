"""Localhost-only demo server for VulnLab-App.

Binds to 127.0.0.1 only. Any other host is refused. This server exists
so the flaws can be seen in a browser; the unit tests are the
authoritative demonstration, and this server adds nothing beyond them.
"""

import argparse
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixed  # noqa: E402
import vuln  # noqa: E402


def make_handler(mode):
    search = vuln.search_users_vuln if mode == "vuln" else fixed.search_users_fixed
    render = vuln.render_greeting_vuln if mode == "vuln" else fixed.render_greeting_fixed
    get_record = vuln.get_record_vuln if mode == "vuln" else fixed.get_record_fixed

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # keep output quiet
            pass

        def do_GET(self):
            parsed = urlparse(self.path)
            qs = parse_qs(parsed.query)
            if parsed.path == "/search":
                name = qs.get("name", [""])[0]
                rows = search(name)
                body = "<br>".join(f"{n} — {d}" for n, d in rows) or "no matches"
                self._send(body)
            elif parsed.path == "/greet":
                self._send(render(qs.get("name", ["guest"])[0]))
            elif parsed.path == "/record":
                owner = qs.get("owner", [""])[0]
                caller = qs.get("caller", [""])[0]
                try:
                    self._send(str(get_record(owner, caller)))
                except PermissionError as exc:
                    self._send(str(exc), status=403)
            else:
                self._send(
                    "<h1>VulnLab-App (local lab only)</h1>"
                    "<p>Try /search?name=lab-alice, /greet?name=guest, "
                    "/record?owner=lab-bob&amp;caller=lab-alice</p>"
                    "<p>See docs/exercises.md. Never expose this server.</p>"
                )

        def _send(self, body, status=200):
            data = body.encode()
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return Handler


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["vuln", "fixed"], required=True)
    parser.add_argument("--port", type=int, default=12700)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args(argv)
    if args.host != "127.0.0.1":
        parser.error("this lab server binds to 127.0.0.1 only")
    print(f"WARNING: intentionally vulnerable lab server, mode={args.mode}, "
          f"listening on 127.0.0.1:{args.port} only. Do not expose it.")
    HTTPServer(("127.0.0.1", args.port), make_handler(args.mode)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
