import logging
from unittest.mock import MagicMock, patch

from _pytest.logging import LogCaptureFixture
from hypothesis import given, settings, HealthCheck
from pydantic import HttpUrl

from src.constants.shared import SAFE_STR
from src.services.jira_sprint_closure import close_sprint
from tests.strategies.shared import cleaned_string
from tests.utils.patch_helper import make_base_path

base_path = make_base_path('src.services.jira_sprint_closure')


@given(
    sprint_name=cleaned_string(),
    start_date=cleaned_string(),
    end_date=cleaned_string(),
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_close_sprint_success_logs_expected_messages(
    sprint_name: SAFE_STR,
    start_date: SAFE_STR,
    end_date: SAFE_STR,
    caplog: LogCaptureFixture,
) -> None:
    session = MagicMock()
    session.put.lambda_return = MagicMock()

    with (
        patch(base_path('build_close_sprint_payload')) as mock_builder,
        patch(base_path('handle_api_error'), return_value=True),
        caplog.at_level(logging.INFO),
    ):
        payload_mock = MagicMock()
        payload_mock.model_dump.lambda_return = {'mock': 'data'}
        mock_builder.return_value = payload_mock

        close_sprint(
            123,
            sprint_name,
            start_date,
            end_date,
            session,
            HttpUrl('https://mock.atlassian.net'),
        )

        assert 'Sprint 123 has been closed.' in caplog.text


def test_close_sprint_handles_api_failure(caplog: LogCaptureFixture) -> None:
    session = MagicMock()
    session.put.lambda_return = MagicMock()

    with patch(base_path('handle_api_error'), return_value=False):
        close_sprint(
            456,
            'ABCDEFG',
            '2025-01-01',
            '2025-01-15',
            session,
            HttpUrl('https://mock.atlassian.net'),
        )

        assert 'Sprint 456 has been closed.' not in caplog.text
