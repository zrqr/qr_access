"""Relay for live browser screenshots. Run this on the EC2 instance behind HTTPS.

The browser pusher posts PNG frames to /push with a shared secret. Viewers open
/ and log in with the viewer token, then see the latest frame.
"""

import hmac
import os
import secrets
import threading
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

PUSH_SECRET = os.environ["PUSH_SECRET"]
VIEWER_TOKEN = os.environ["VIEWER_TOKEN"]
PORT = int(os.environ.get("PORT", "8080"))
SESSION = secrets.token_urlsafe(32)
_lock = threading.Lock()
_latest = {"png": b""}

LOGIN = b"""<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<body style="font-family:sans-serif;padding:16px"><h3>Browser view</h3>
<form method=post action=/login><input name=token type=password placeholder="Token" style="font-size:18px;width:100%">
<button style="font-size:18px;margin-top:8px">Open</button></form></body>"""

PAGE = b"""<!doctype html><meta name=viewport content="width=device-width,initial-scale=1">
<body style="margin:0;background:#111"><img id=s src="/latest.png" style="width:100%;display:block">
<script>setInterval(()=>{document.getElementById('s').src='/latest.png?'+Date.now()},2000)</script></body>"""


class Handler(BaseHTTPRequestHandler):
    def _authed(self):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        return "session" in cookie and hmac.compare_digest(cookie["session"].value, SESSION)

    def _send(self, code, body, ctype="text/html", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/login":
            return self._send(200, LOGIN)
        if not self._authed():
            return self._send(302, b"", extra={"Location": "/login"})
        if self.path.startswith("/latest.png"):
            with _lock:
                frame = _latest["png"]
            return self._send(200, frame, "image/png")
        return self._send(200, PAGE)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        if self.path == "/push":
            if not hmac.compare_digest(self.headers.get("X-Push-Secret", ""), PUSH_SECRET):
                return self._send(401, b"")
            with _lock:
                _latest["png"] = body
            return self._send(204, b"")
        if self.path == "/login":
            form = parse_qs(body.decode())
            if hmac.compare_digest(form.get("token", [""])[0], VIEWER_TOKEN):
                cookie = f"session={SESSION}; HttpOnly; Secure; SameSite=Strict; Path=/"
                return self._send(302, b"", extra={"Location": "/", "Set-Cookie": cookie})
            return self._send(401, LOGIN)
        return self._send(404, b"")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"relay listening on {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
