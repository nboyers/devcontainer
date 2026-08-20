"""A dependency-free Python app for testing the Dev Container setup."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
            return

        if self.path == "/config":
            self.send_json(200, {"some_env_var": os.getenv("SOME_ENV_VAR", "unset")})
            return

        if self.path == "/":
            body = """<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>Coder Dev Container</title></head>
  <body>
    <h1>Python is running inside the Dev Container</h1>
    <p>Try <a href="/health">/health</a> or <a href="/config">/config</a>.</p>
  </body>
</html>
"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body.encode())))
            self.end_headers()
            self.wfile.write(body.encode())
            return

        self.send_json(404, {"error": "not found"})

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), AppHandler)
    print("Example app listening on http://0.0.0.0:8000")
    server.serve_forever()