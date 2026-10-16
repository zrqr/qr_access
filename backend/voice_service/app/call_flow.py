"""Decides what the assistant says or presses next during a phone call.

The flow is independent of the telephony and speech providers, so it can be
tested without a phone line.
"""

from dataclasses import dataclass, field
from enum import Enum
import re

DISCLOSURE = (
    "Hello, this is an automated assistant calling on behalf of {caller}. "
    "This call may be recorded."
)


class ActionKind(str, Enum):
    GATHER = "gather"  # say text, then listen for speech or keypad input
    HANGUP = "hangup"  # say text (optional) and end the call


@dataclass
class Action:
    kind: ActionKind
    say: str = ""
    digits: str = ""  # keys to press on the far end before speaking


@dataclass
class MenuOption:
    keywords: list[str]  # words that identify this option in speech
    digits: str  # keypad digits to press when the option matches


@dataclass
class CallSession:
    call_id: str
    to_number: str
    caller_name: str
    goal: str  # what to ask for, e.g. "the opening hours for next week"
    menu: list[MenuOption] = field(default_factory=list)
    max_turns: int = 12
    turns: int = 0
    asked_for_person: bool = False
    transcript: list[str] = field(default_factory=list)
    finished: bool = False


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())


def match_option(menu: list[MenuOption], speech: str) -> MenuOption | None:
    words = set(_normalize(speech).split())
    best, best_hits = None, 0
    for option in menu:
        hits = sum(1 for keyword in option.keywords if keyword.lower() in words)
        if hits > best_hits:
            best, best_hits = option, hits
    return best


def start(session: CallSession) -> Action:
    """First message of the call: disclosure, then the goal."""
    opening = DISCLOSURE.format(caller=session.caller_name)
    session.transcript.append(f"assistant: {opening}")
    return Action(ActionKind.GATHER, say=opening)


def next_action(session: CallSession, speech: str | None, digits: str | None) -> Action:
    """Chooses the reply to something the other side said or pressed."""
    if session.finished:
        return Action(ActionKind.HANGUP)

    session.turns += 1
    if speech:
        session.transcript.append(f"other: {speech}")
    if digits:
        session.transcript.append(f"other pressed: {digits}")

    if session.turns > session.max_turns:
        return _finish(session, "Thank you, I will call back later. Goodbye.")

    if not speech:
        return Action(ActionKind.GATHER, say="Sorry, I did not hear anything. Please continue.")

    # Automated menu: follow the option that matches what was said.
    option = match_option(session.menu, speech)
    if option is not None:
        return Action(ActionKind.GATHER, digits=option.digits)

    # A person has picked up: state the goal.
    if not session.asked_for_person and _sounds_like_person(speech):
        session.asked_for_person = True
        request = f"I am calling to ask about {session.goal}. Can you help with that?"
        session.transcript.append(f"assistant: {request}")
        return Action(ActionKind.GATHER, say=request)

    # Goal already stated and nothing matched: wrap up politely.
    if session.asked_for_person:
        return _finish(session, "Thank you for your help. Goodbye.")

    return Action(ActionKind.GATHER, say=f"I am calling about {session.goal}.")


def _sounds_like_person(speech: str) -> bool:
    words = set(_normalize(speech).split())
    return bool(words & {"hello", "hi", "yes", "speaking", "help", "how"})


def _finish(session: CallSession, message: str) -> Action:
    session.finished = True
    session.transcript.append(f"assistant: {message}")
    return Action(ActionKind.HANGUP, say=message)
