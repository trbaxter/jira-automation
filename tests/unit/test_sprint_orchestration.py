import logging
from datetime import datetime
from unittest.mock import MagicMock

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from freezegun import freeze_time

from src.orchestration.sprint_orchestration import automate_sprint

CLOSE_SPRINT = "src.orchestration.sprint_orchestration.close_sprint"
CREATE_SPRINT = "src.orchestration.sprint_orchestration.create_sprint"
DATETIME = "src.orchestration.sprint_orchestration.datetime"
LOAD_CONFIG = "src.orchestration.sprint_orchestration.load_config"
GET_ALL_FUTURE_SPRINTS = (
    "src.orchestration.sprint_orchestration.get_all_future_sprints"
)
GET_INCOMPLETE_STORIES = (
    "src.orchestration.sprint_orchestration.get_incomplete_stories"
)
GET_SPRINT_BY_STATE = (
    "src.orchestration.sprint_orchestration.get_sprint_by_state"
)
MOVE_ISSUES = "src.orchestration.sprint_orchestration.move_issues_to_new_sprint"
PARSE_ISSUE = "src.orchestration.sprint_orchestration.parse_issue"
SPRINT_PARSER = "src.orchestration.sprint_orchestration.parse_dart_sprint"
START_SPRINT = "src.orchestration.sprint_orchestration.start_sprint"


def test_creates_new_sprint_if_none_found(monkeypatch: MonkeyPatch):
    session = MagicMock()
    config = MagicMock(base_url="https://mock.atlassian.net", board_id=1)

    monkeypatch.setattr(target=LOAD_CONFIG, name=(lambda: config))
    monkeypatch.setattr(target=GET_ALL_FUTURE_SPRINTS, name=(lambda *_: []))
    create_sprint_mock = MagicMock(
        return_value={"id": 123, "name": "DART 250101"}
    )
    monkeypatch.setattr(target=CREATE_SPRINT, name=create_sprint_mock)
    monkeypatch.setattr(target=GET_SPRINT_BY_STATE, name=(lambda *_: None))
    monkeypatch.setattr(target=START_SPRINT, name=(lambda *_: None))

    automate_sprint(session)

    create_sprint_mock.assert_called_once()


@freeze_time("2025-07-28")
def test_uses_existing_dart_sprint(
    monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    session = MagicMock()
    config = MagicMock(base_url="https://mock.atlassian.net", board_id=1)

    sprint_name = "DART 250728 (07/28-08/11)"
    future_sprints = [{"name": sprint_name, "id": 42}]

    monkeypatch.setattr(target=LOAD_CONFIG, name=(lambda: config))
    monkeypatch.setattr(
        target=GET_ALL_FUTURE_SPRINTS, name=(lambda *_: future_sprints)
    )
    monkeypatch.setattr(
        target=SPRINT_PARSER,
        name=(
            lambda name: MagicMock(start=datetime(year=2025, month=7, day=28))
        ),
    )
    monkeypatch.setattr(target=GET_SPRINT_BY_STATE, name=(lambda *_: None))
    monkeypatch.setattr(target=START_SPRINT, name=(lambda *_: None))

    with caplog.at_level(logging.INFO):
        automate_sprint(session)

    assert f"Upcoming DART sprint found: {sprint_name}." in caplog.text
    assert "Proceeding with automation process." in caplog.text


def test_skips_closing_if_no_active_sprint(monkeypatch: MonkeyPatch):
    session = MagicMock()
    config = MagicMock(base_url="https://mock.atlassian.net", board_id=1)

    monkeypatch.setattr(target=LOAD_CONFIG, name=(lambda: config))
    monkeypatch.setattr(target=GET_ALL_FUTURE_SPRINTS, name=(lambda *_: []))
    monkeypatch.setattr(
        target=CREATE_SPRINT, name=(lambda *_: {"id": 123, "name": "NewSprint"})
    )
    monkeypatch.setattr(target=GET_SPRINT_BY_STATE, name=(lambda *_: None))
    monkeypatch.setattr(target=START_SPRINT, name=(lambda *_: None))

    automate_sprint(session)


def test_returns_early_if_create_sprint_fails(monkeypatch: MonkeyPatch):
    session = MagicMock()
    config = MagicMock(base_url="https://mock.atlassian.net", board_id=1)

    monkeypatch.setattr(target=LOAD_CONFIG, name=(lambda: config))
    monkeypatch.setattr(target=GET_ALL_FUTURE_SPRINTS, name=(lambda *_: []))
    monkeypatch.setattr(target=CREATE_SPRINT, name=(lambda *_: None))
    start_sprint = MagicMock()
    monkeypatch.setattr(target=START_SPRINT, name=start_sprint)

    automate_sprint(session)

    start_sprint.assert_not_called()


def test_full_orchestration_path(monkeypatch: MonkeyPatch):
    session = MagicMock()
    config = MagicMock(base_url="https://mock.atlassian.net", board_id=1)

    monkeypatch.setattr(target=LOAD_CONFIG, name=(lambda: config))
    monkeypatch.setattr(target=GET_ALL_FUTURE_SPRINTS, name=(lambda *_: []))
    monkeypatch.setattr(
        target=CREATE_SPRINT, name=(lambda *_: {"id": 123, "name": "DART X"})
    )
    monkeypatch.setattr(
        target=GET_SPRINT_BY_STATE,
        name=(
            lambda *_: {
                "id": 99,
                "name": "DART 123456",
                "startDate": "2025-01-01",
                "endDate": "2025-01-15",
            }
        ),
    )
    monkeypatch.setattr(
        target=GET_INCOMPLETE_STORIES, name=(lambda *_: [{"key": "JIRA-1"}])
    )
    monkeypatch.setattr(
        target=PARSE_ISSUE,
        name=(lambda issue: {"key": issue["key"], "fields": {}}),
    )
    monkeypatch.setattr(target=CLOSE_SPRINT, name=(lambda *_: None))
    monkeypatch.setattr(target=MOVE_ISSUES, name=(lambda *_: None))
    monkeypatch.setattr(target=START_SPRINT, name=(lambda *_: None))

    automate_sprint(session)
