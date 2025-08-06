import logging
from datetime import datetime
from unittest.mock import MagicMock

from freezegun import freeze_time

from src.orchestration.sprint_orchestration import automate_sprint
from tests.utils.patch_helper import make_base_path
from tests.utils.simple_lambda_return import lambda_return

base_path = make_base_path('src.orchestration.sprint_orchestration')


# Helper function to avoid writing 'monkeypatch.attr' multiple times per test
def patch_all(monkeypatch, **target_name_pairs) -> None:
    for target, name in target_name_pairs.items():
        monkeypatch.setattr(base_path(target), name)


def test_create_new_sprint_if_none_found(
        test_config,
        test_session,
        monkeypatch
) -> None:
    create_sprint_mock = MagicMock(return_value={'id': 1, 'name': 'test'})

    patch_all(
        monkeypatch,
        get_all_future_sprints=lambda_return([]),
        create_sprint=create_sprint_mock,
        get_sprint_by_state=lambda_return(None),
        start_sprint=lambda_return(None),
    )

    automate_sprint(test_session, test_config)
    create_sprint_mock.assert_called_once()


@freeze_time('2025-07-28')
def test_uses_existing_dart_sprint(
        test_session,
        test_config,
        monkeypatch,
        caplog
) -> None:
    sprint_date = MagicMock(start=datetime(2025, 7, 28))
    sprint_name = 'DART 250728 (07/28-08/11)'

    future_sprints = [{'name': sprint_name, 'id': 42}]

    patch_all(
        monkeypatch,
        get_all_future_sprints=lambda_return(future_sprints),
        parse_dart_sprint=lambda name: sprint_date,
        get_sprint_by_state=lambda_return(None),
        start_sprint=lambda_return(None),
    )

    with caplog.at_level(logging.INFO):
        automate_sprint(test_session, test_config)

    assert f'Upcoming DART sprint found: {sprint_name}.' in caplog.text
    assert 'Proceeding with automation process.' in caplog.text


def test_skips_closing_if_no_active_sprint(
        test_session,
        test_config,
        monkeypatch
) -> None:

    patch_all(
        monkeypatch,
        get_all_future_sprints=lambda_return([]),
        create_sprint=lambda_return({'id': 123, 'name': 'NewSprint'}),
        get_sprint_by_state=lambda_return(None),
        start_sprint=lambda_return(None),
    )

    automate_sprint(test_session, test_config)


def test_returns_early_if_create_sprint_fails(
        test_session,
        test_config,
        monkeypatch
) -> None:

    start_sprint = MagicMock()

    patch_all(
        monkeypatch,
        get_all_future_sprints=lambda_return([]),
        create_sprint=lambda_return(None),
        start_sprint=start_sprint,
    )

    automate_sprint(test_session, test_config)


def test_full_orchestration_path(
        test_session,
        test_config,
        monkeypatch
) -> None:
    new_sprint = {'id': 12, 'name': 'DART 241218 (12/18-01/01)'}
    active_sprint = {
        'id': 99,
        'name': 'DART 250101 (01/01-01/15)',
        'startDate': '2025-01-01',
        'endDate': '2025-01-15',
    }

    patch_all(
        monkeypatch,
        get_all_future_sprints=lambda_return([]),
        create_sprint=lambda_return(new_sprint),
        get_sprint_by_state=lambda_return(active_sprint),
        get_incomplete_stories=lambda_return([{'key': 'JIRA-1'}]),
        parse_issue=(lambda issue: {'key': issue['key'], 'fields': {}}),
        close_sprint=lambda_return(None),
        move_issues_to_new_sprint=lambda_return(None),
        start_sprint=lambda_return(None),
    )

    automate_sprint(test_session, test_config)
