import logging
from unittest.mock import MagicMock, patch

from _pytest.logging import LogCaptureFixture
from hypothesis import given, settings, HealthCheck
from pydantic import HttpUrl

from src.services.jira_sprint_closure import close_sprint
from strategies.common import cleaned_string


@given(
    sprint_name=cleaned_string(),
    start_date=cleaned_string(),
    end_date=cleaned_string(),
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_close_sprint_success_logs_expected_messages(
    sprint_name: str,
    start_date: str,
    end_date: str,
    caplog: LogCaptureFixture,
) -> None:
    session = MagicMock()
    session.put.return_value = MagicMock()

    with (
        patch(
            target="src.services.jira_sprint_closure.build_close_sprint_payload"
        ) as mock_builder,
        patch(
            target="src.services.jira_sprint_closure.handle_api_error",
            return_value=True,
        ),
        caplog.at_level(logging.INFO),
    ):
        payload_mock = MagicMock()
        payload_mock.model_dump.return_value = {"mock": "data"}
        mock_builder.return_value = payload_mock

        close_sprint(
            sprint_id=123,
            sprint_name=sprint_name,
            start_date=start_date,
            end_date=end_date,
            session=session,
            base_url=HttpUrl("https://mock.atlassian.net"),
        )

        assert "Sprint 123 has been closed." in caplog.text


def test_close_sprint_handles_api_failure(
    caplog: LogCaptureFixture,
) -> None:
    session = MagicMock()
    session.put.return_value = MagicMock()

    with patch(
        target="src.services.jira_sprint_closure.handle_api_error",
        return_value=False,
    ):
        close_sprint(
            sprint_id=456,
            sprint_name="ABCDEFG",
            start_date="2025-01-01",
            end_date="2025-01-15",
            session=session,
            base_url=HttpUrl("https://mock.atlassian.net"),
        )

        assert "Sprint 456 has been closed." not in caplog.text
