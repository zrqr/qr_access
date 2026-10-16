from app.call_flow import ActionKind, CallSession, MenuOption, match_option, next_action, start


def make_session(**overrides):
    values = dict(
        call_id="c1",
        to_number="+15550000000",
        caller_name="Pedro",
        goal="the opening hours for next week",
        menu=[MenuOption(["billing", "bill"], "2"), MenuOption(["representative", "agent"], "0")],
    )
    values.update(overrides)
    return CallSession(**values)


def test_start_identifies_itself_as_the_callers_assistant():
    session = make_session()
    action = start(session)
    assert action.kind == ActionKind.GATHER
    assert "Pedro's assistant" in action.say
    assert "the opening hours for next week" in action.say


def test_menu_speech_presses_matching_digits():
    session = make_session()
    action = next_action(session, "For billing press 2", None)
    assert action.digits == "2"
    assert action.kind == ActionKind.GATHER


def test_person_answering_gets_the_goal():
    session = make_session()
    action = next_action(session, "Hello, how can I help?", None)
    assert "opening hours for next week" in action.say
    assert session.asked_for_person is True


def test_goal_stated_then_unrelated_speech_hangs_up():
    session = make_session()
    next_action(session, "Hello", None)
    action = next_action(session, "Please hold", None)
    assert action.kind == ActionKind.HANGUP
    assert session.finished is True


def test_empty_speech_asks_to_continue():
    session = make_session()
    action = next_action(session, None, None)
    assert action.kind == ActionKind.GATHER
    assert "did not hear" in action.say


def test_max_turns_ends_the_call():
    session = make_session(max_turns=2)
    next_action(session, "Hi", None)
    next_action(session, "Hi", None)
    action = next_action(session, "Hi", None)
    assert action.kind == ActionKind.HANGUP
    assert session.finished is True


def test_finished_session_stays_finished():
    session = make_session(finished=True)
    assert next_action(session, "Hello", None).kind == ActionKind.HANGUP


def test_transcript_records_both_sides():
    session = make_session()
    start(session)
    next_action(session, "Billing department", "")
    assert session.transcript[0].startswith("assistant:")
    assert "other: Billing department" in session.transcript


def test_match_option_prefers_most_keyword_hits():
    menu = [MenuOption(["sales"], "1"), MenuOption(["billing", "payments"], "2")]
    assert match_option(menu, "billing and payments").digits == "2"
    assert match_option(menu, "something else") is None
