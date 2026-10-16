"""Twilio adapter: places outbound calls and builds the TwiML that drives them."""

from xml.sax.saxutils import escape

import httpx

from .call_flow import Action, ActionKind
from .config import Settings


async def place_call(settings: Settings, to_number: str, call_id: str) -> str:
    """Starts an outbound call. Returns the Twilio call SID."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Calls.json"
    data = {
        "To": to_number,
        "From": settings.twilio_from_number,
        "Url": f"{settings.public_base_url}/twilio/voice?call_id={call_id}",
        "StatusCallback": f"{settings.public_base_url}/twilio/status?call_id={call_id}",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            url,
            data=data,
            auth=(settings.twilio_account_sid, settings.twilio_auth_token),
        )
    response.raise_for_status()
    return response.json()["sid"]


def action_to_twiml(action: Action, call_id: str, base_url: str) -> str:
    """Turns a call-flow action into TwiML for Twilio to execute."""
    gather_url = f"{base_url}/twilio/gather?call_id={call_id}"
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<Response>"]

    if action.digits:
        parts.append(f'<Play digits="{escape(action.digits)}"/>')

    if action.kind == ActionKind.HANGUP:
        if action.say:
            parts.append(f"<Say>{escape(action.say)}</Say>")
        parts.append("<Hangup/>")
    else:
        parts.append(
            f'<Gather input="speech dtmf" speechTimeout="auto" timeout="6" action="{escape(gather_url)}">'
        )
        if action.say:
            parts.append(f"<Say>{escape(action.say)}</Say>")
        parts.append("</Gather>")

    parts.append("</Response>")
    return "".join(parts)
