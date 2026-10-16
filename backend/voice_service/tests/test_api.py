from fastapi.testclient import TestClient

from app import main
from app.config import Settings

SETTINGS = Settings(
    api_token="secret",
    twilio_account_sid="AC123",
    twilio_auth_token="token",
    twilio_from_number="+15551230000",
    public_base_url="https://voice.example.com",
)


async def fake_place_call(settings, to_number, call_id):
    return "CA_fake"


def client(monkeypatch):
    monkeypatch.setattr(main, "_settings", SETTINGS)
    monkeypatch.setattr(main, "place_call", fake_place_call)
    main._sessions.clear()
    return TestClient(main.app)


BODY = {
    "to_number": "+15552223333",
    "caller_name": "Pedro",
    "goal": "the opening hours",
    "menu": [{"keywords": ["billing"], "digits": "2"}],
}


def test_create_call_requires_token(monkeypatch):
    api = client(monkeypatch)
    response = api.post("/calls", json=BODY)
    assert response.status_code == 401


def test_create_call_rejects_bad_number(monkeypatch):
    api = client(monkeypatch)
    response = api.post(
        "/calls",
        json={**BODY, "to_number": "not-a-number"},
        headers={"Authorization": "Bearer secret"},
    )
    assert response.status_code == 422


def test_create_call_then_twiml_flow(monkeypatch):
    api = client(monkeypatch)
    headers = {"Authorization": "Bearer secret"}

    created = api.post("/calls", json=BODY, headers=headers)
    assert created.status_code == 201
    call_id = created.json()["call_id"]

    greeting = api.post(f"/twilio/voice?call_id={call_id}")
    assert "Pedro's assistant" in greeting.text
    assert "<Gather" in greeting.text

    menu = api.post(f"/twilio/gather?call_id={call_id}", data={"SpeechResult": "for billing say two"})
    assert '<Play digits="2"/>' in menu.text

    status = api.get(f"/calls/{call_id}", headers=headers).json()
    assert status["turns"] == 1
    assert "other: for billing say two" in status["transcript"]


def test_unknown_call_hangs_up(monkeypatch):
    api = client(monkeypatch)
    response = api.post("/twilio/voice?call_id=missing")
    assert "<Hangup/>" in response.text
