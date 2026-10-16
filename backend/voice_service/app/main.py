"""HTTP API for placing assistant phone calls and handling Twilio webhooks."""

import secrets
import uuid

from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request, Response
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from . import call_flow
from .call_flow import CallSession, MenuOption
from .config import Settings
from .telephony import action_to_twiml, place_call

app = FastAPI(title="Phone assistant")
_settings: Settings | None = None
_sessions: dict[str, CallSession] = {}  # in-memory; lost on restart


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def require_token(request: Request, settings: Settings = Depends(get_settings)) -> None:
    header = request.headers.get("authorization", "")
    expected = f"Bearer {settings.api_token}"
    if not secrets.compare_digest(header, expected):
        raise HTTPException(status_code=401, detail="invalid token")


class MenuOptionIn(BaseModel):
    keywords: list[str] = Field(min_length=1)
    digits: str = Field(pattern=r"^[0-9*#w]+$")


class CallRequest(BaseModel):
    to_number: str = Field(pattern=r"^\+[1-9]\d{6,14}$")  # E.164
    caller_name: str = Field(min_length=1, max_length=80)
    goal: str = Field(min_length=1, max_length=300)
    menu: list[MenuOptionIn] = []
    max_turns: int = Field(default=12, ge=1, le=30)


@app.post("/calls", dependencies=[Depends(require_token)], status_code=201)
async def create_call(body: CallRequest, settings: Settings = Depends(get_settings)):
    call_id = uuid.uuid4().hex
    session = CallSession(
        call_id=call_id,
        to_number=body.to_number,
        caller_name=body.caller_name,
        goal=body.goal,
        menu=[MenuOption(o.keywords, o.digits) for o in body.menu],
        max_turns=body.max_turns,
    )
    _sessions[call_id] = session
    sid = await place_call(settings, body.to_number, call_id)
    return {"call_id": call_id, "twilio_sid": sid}


@app.get("/calls/{call_id}", dependencies=[Depends(require_token)])
def get_call(call_id: str):
    session = _sessions.get(call_id)
    if session is None:
        raise HTTPException(status_code=404, detail="unknown call")
    return {
        "call_id": call_id,
        "finished": session.finished,
        "turns": session.turns,
        "transcript": session.transcript,
    }


def _twiml(action, call_id: str, settings: Settings) -> Response:
    xml = action_to_twiml(action, call_id, settings.public_base_url)
    return Response(content=xml, media_type="text/xml")


@app.post("/twilio/voice")
def twilio_voice(call_id: str = Query(...), settings: Settings = Depends(get_settings)):
    session = _sessions.get(call_id)
    if session is None:
        return _twiml(call_flow.Action(call_flow.ActionKind.HANGUP, say="Goodbye."), call_id, settings)
    return _twiml(call_flow.start(session), call_id, settings)


@app.post("/twilio/gather")
def twilio_gather(
    call_id: str = Query(...),
    SpeechResult: str | None = Form(None),
    Digits: str | None = Form(None),
    settings: Settings = Depends(get_settings),
):
    session = _sessions.get(call_id)
    if session is None:
        return _twiml(call_flow.Action(call_flow.ActionKind.HANGUP, say="Goodbye."), call_id, settings)
    action = call_flow.next_action(session, SpeechResult, Digits)
    return _twiml(action, call_id, settings)


@app.post("/twilio/status", response_class=PlainTextResponse)
def twilio_status(call_id: str = Query(...), CallStatus: str | None = Form(None)):
    session = _sessions.get(call_id)
    if session and CallStatus in {"completed", "failed", "busy", "no-answer", "canceled"}:
        session.finished = True
    return ""
