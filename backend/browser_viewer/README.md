# Browser viewer

Shows the assistant's Playwright browser on a page you can open from your
phone. The browser runs where `pusher.py` runs (this container, or any machine
that can reach the relay). The relay runs on your EC2 instance and serves the
page behind a token.

```
[container: pusher.py] --POST screenshots--> [EC2: relay.py] <--HTTPS, token-- [your phone]
```

## 1. Relay on EC2

Put it behind HTTPS (for example Caddy or nginx with a certificate) so the
login cookie and token are not sent in plain text.

```bash
PUSH_SECRET=<long random string> VIEWER_TOKEN=<another long string> PORT=8080 \
  python3 relay.py
```

Use a different value for each secret. `PUSH_SECRET` is what the pusher sends;
`VIEWER_TOKEN` is what you type on the login page. Open `https://<your-host>/`
on your phone.

## 2. Pusher where the browser runs

```bash
pip install playwright && playwright install chromium   # or point CHROMIUM_PATH at one
RELAY_URL=https://<your-host> PUSH_SECRET=<same as relay> START_URL=https://example.com \
  python3 pusher.py
```

`FRAME_SECONDS` sets how often a frame is sent (default 2).

## Security notes

- Anyone with `VIEWER_TOKEN` can see the browser. Keep it private and rotate it
  by restarting the relay with a new value.
- Use HTTPS only. The relay sets its cookie as `Secure`, so it won't work over
  plain HTTP.
- The browser may show pages you're logged into. Only point it at sites you're
  happy to expose to the viewer.
