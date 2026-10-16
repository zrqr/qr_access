# Phone assistant (voice service)

A small service that places outbound phone calls for simple inquiries and
works through automated phone menus (IVR) to reach a person. Speech is turned
into text and back into speech over Twilio.

Each call opens by identifying the assistant as the caller's assistant and
stating the goal. Check the rules where you are before using it, since
recording and automated-calling laws vary.

## How it works

1. `POST /calls` with the number, the caller's name, the goal and an optional
   menu plan. The service places the call through Twilio.
2. Twilio requests `/twilio/voice`, which introduces the assistant and listens.
3. What the other side says or presses is posted to `/twilio/gather`.
   - If it matches a menu option, the matching keypad digits are sent.
   - When a person answers, the goal is stated.
   - The call ends politely after the goal is stated and nothing else matches,
     or after `max_turns`.
4. `GET /calls/{call_id}` returns the transcript.

## Configuration

| Variable | Purpose |
|---|---|
| `VOICE_API_TOKEN` | Bearer token required to start and read calls |
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` | Twilio credentials |
| `TWILIO_FROM_NUMBER` | Your Twilio phone number, E.164 format |
| `PUBLIC_BASE_URL` | Public HTTPS address Twilio can reach, e.g. `https://voice.example.com` |

## Run

```bash
cd backend/voice_service
pip install -r requirements.txt
export VOICE_API_TOKEN=... TWILIO_ACCOUNT_SID=... TWILIO_AUTH_TOKEN=...
export TWILIO_FROM_NUMBER=+1... PUBLIC_BASE_URL=https://your-host
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Start a call:

```bash
curl -X POST https://your-host/calls \
  -H "Authorization: Bearer $VOICE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"to_number":"+15552223333","caller_name":"Pedro",
       "goal":"the opening hours for next week",
       "menu":[{"keywords":["billing"],"digits":"2"},
               {"keywords":["representative","agent"],"digits":"0"}]}'
```

## Tests

```bash
pip install -r requirements.txt
pytest
```

## Limitations

- Calls need a public HTTPS address for Twilio's webhooks, so the service must
  run somewhere reachable from the internet. The Claude Code container cannot
  receive inbound connections, so run it on your own server.
- Session state is in memory and is lost on restart. Use a database if calls
  must survive restarts.
- Menu matching is keyword-based. Speech recognition quality depends on
  Twilio. Better voices or an LLM-based decision step can replace
  `call_flow.py` and `telephony.py`.
- Keep `VOICE_API_TOKEN` secret. Anyone with it can place calls on your account.
