import logging
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from _pytest.logging import LogCaptureFixture
from hypothesis import given, settings, HealthCheck
from pydantic import HttpUrl

from src.constants.field_types import SAFE_STR
from src.services.jira_start_sprint import start_sprint
from strategies.shared import cleaned_string, valid_datetime_range


@pytest.fixture
def mock_session() -> MagicMock:
    session = MagicMock()
    session.put.return_value = MagicMock()
    return session


@given(sprint_name=cleaned_string(), start_date=valid_datetime_range())
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_start_sprint_success_logs_expected_messages(
    sprint_name: SAFE_STR, start_date: datetime, caplog: LogCaptureFixture
) -> None:
    end_date = start_date + timedelta(days=14)
    mock_session = MagicMock()
    mock_session.put.return_value = MagicMock()

    with (
        patch(
            "src.services.jira_start_sprint.build_start_sprint_payload"
        ) as mock_builder,
        patch(
            "src.services.jira_start_sprint.handle_api_error", return_value=True
        ),
        caplog.at_level(logging.INFO),
    ):
        payload_mock = MagicMock()
        payload_mock.model_dump.return_value = {"mock": "data"}
        mock_builder.return_value = payload_mock

        start_sprint(
            42,
            sprint_name,
            start_date,
            end_date,
            mock_session,
            HttpUrl("https://mock.atlassian.net"),
        )

        assert "Sprint 42 is now active." in caplog.text
        assert "Sprint automation process complete." in caplog.text


def test_start_sprint_handles_api_failure(
    caplog: LogCaptureFixture, mock_session: MagicMock
) -> None:
    with patch(
        "src.services.jira_start_sprint.handle_api_error", return_value=False
    ):
        start_sprint(
            999,
            "Z",
            datetime(2025, 1, 1),
            datetime(2025, 1, 14),
            mock_session,
            HttpUrl("https://mock.atlassian.net"),
        )

        assert "Sprint 999 is now active." not in caplog.text
