import logging
from datetime import datetime
from typing import Any, Callable, Tuple
from unittest.mock import MagicMock

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from freezegun import freeze_time

from src.orchestration.sprint_orchestration import automate_sprint

TARGET_BASE = "src.orchestration.sprint_orchestration"


# Helper function to shorten target names
def function(name: str) -> str:
    return f"{TARGET_BASE}.{name}"


# Helper function to silently return some value
def return_value(val) -> Callable[..., Any]:
    return lambda *_, **__: val


# Helper function for configuration setup required for each test
def setup() -> Tuple[MagicMock, MagicMock]:
    session = MagicMock()
    config = MagicMock(base_url="https://mock.atlassian.net", board_id=1)
    return session, config


# Helper function to avoid writing "monkeypatch.attr" multiple times per test
def patch_all(
    monkeypatch: MonkeyPatch, **target_name_pairs: Callable[..., Any]
) -> None:
    for target, name in target_name_pairs.items():
        monkeypatch.setattr(target=function(target), name=name)


def test_creates_new_sprint_if_none_found(monkeypatch: MonkeyPatch) -> None:
    session, config = setup()
    create_sprint_mock = MagicMock(return_value={"id": 1, "name": "test"})

    patch_all(
        monkeypatch,
        load_config=(lambda: config),
        get_all_future_sprints=return_value([]),
        create_sprint=create_sprint_mock,
        get_sprint_by_state=return_value(None),
        start_sprint=return_value(None),
    )

    automate_sprint(session)
    create_sprint_mock.assert_called_once()


@freeze_time("2025-07-28")
def test_uses_existing_dart_sprint(
    monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    session, config = setup()

    sprint_date = MagicMock(start=datetime(year=2025, month=7, day=28))
    sprint_name = "DART 250728 (07/28-08/11)"

    future_sprints = [{"name": sprint_name, "id": 42}]

    patch_all(
        monkeypatch,
        load_config=(lambda: config),
        get_all_future_sprints=return_value(future_sprints),
        parse_dart_sprint=lambda name: sprint_date,
        get_sprint_by_state=return_value(None),
        start_sprint=return_value(None),
    )

    with caplog.at_level(logging.INFO):
        automate_sprint(session)

    assert f"Upcoming DART sprint found: {sprint_name}." in caplog.text
    assert "Proceeding with automation process." in caplog.text


def test_skips_closing_if_no_active_sprint(monkeypatch: MonkeyPatch) -> None:
    session, config = setup()

    patch_all(
        monkeypatch,
        load_config=(lambda: config),
        get_all_future_sprints=return_value([]),
        create_sprint=return_value({"id": 123, "name": "NewSprint"}),
        get_sprint_by_state=return_value(None),
        start_sprint=return_value(None),
    )

    automate_sprint(session)


def test_returns_early_if_create_sprint_fails(monkeypatch: MonkeyPatch) -> None:
    session, config = setup()
    start_sprint = MagicMock()

    patch_all(
        monkeypatch,
        load_config=(lambda: config),
        get_all_future_sprints=return_value([]),
        create_sprint=return_value(None),
        start_sprint=start_sprint,
    )

    automate_sprint(session)
    start_sprint.assert_not_called()


def test_full_orchestration_path(monkeypatch: MonkeyPatch) -> None:
    session, config = setup()
    new_sprint = {"id": 12, "name": "DART 241218 (12/18-01/01)"}
    active_sprint = {
        "id": 99,
        "name": "DART 250101 (01/01-01/15)",
        "startDate": "2025-01-01",
        "endDate": "2025-01-15",
    }

    patch_all(
        monkeypatch,
        load_config=(lambda: config),
        get_all_future_sprints=return_value([]),
        create_sprint=return_value(new_sprint),
        get_sprint_by_state=return_value(active_sprint),
        get_incomplete_stories=return_value([{"key": "JIRA-1"}]),
        parse_issue=(lambda issue: {"key": issue["key"], "fields": {}}),
        close_sprint=return_value(None),
        move_issues_to_new_sprint=return_value(None),
        start_sprint=return_value(None),
    )

    automate_sprint(session)
