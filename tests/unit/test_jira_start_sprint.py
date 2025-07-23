from datetime import datetime
from unittest.mock import patch, MagicMock

import requests

from src.services.jira_start_sprint import start_sprint
from tests.constants.patch_targets import (
    JSTART_HANDLE_ERROR,
    PAYLOAD_BUILDER_FORMAT_DATE
)
from tests.constants.test_constants import (
    ACTIVE,
    JIRA_DATE_FORMAT,
    MOCK_BASE_URL,
    MOCK_SPRINT_END,
    MOCK_SPRINT_START
)


@patch(JSTART_HANDLE_ERROR, return_value=True)
@patch(
    PAYLOAD_BUILDER_FORMAT_DATE,
    side_effect=lambda dt: dt.strftime(JIRA_DATE_FORMAT)
)
def test_start_sprint_success(
        _mock_handle_error: MagicMock,
        _mock_format: MagicMock
) -> None:
    session_mock = MagicMock(spec=requests.Session)
    mock_response = MagicMock(spec=requests.Response)
    session_mock.put.return_value = mock_response

    new_sprint_id = 123
    sprint_name = "Test Sprint"
    start_date = datetime(2025, 7, 21, 0, 0)
    end_date = datetime(2025, 8, 4, 0, 0)

    start_sprint(
        new_sprint_id,
        sprint_name,
        start_date,
        end_date,
        session_mock,
        MOCK_BASE_URL
    )

    expected_payload = {
        "state": ACTIVE,
        "name": sprint_name,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END
    }

    session_mock.put.assert_called_once_with(
        f"{MOCK_BASE_URL}/rest/agile/1.0/sprint/{new_sprint_id}",
        json=expected_payload
    )


@patch(JSTART_HANDLE_ERROR, return_value=False)
@patch(
    PAYLOAD_BUILDER_FORMAT_DATE,
    side_effect=lambda dt: dt.strftime(JIRA_DATE_FORMAT)
)
def test_start_sprint_failure(
        _mock_format: MagicMock,
        _mock_handle_error: MagicMock
) -> None:
    session_mock = MagicMock(spec=requests.Session)
    mock_response = MagicMock(spec=requests.Response)
    session_mock.put.return_value = mock_response

    new_sprint_id = 456
    sprint_name = "Failed Sprint"
    start_date = datetime(2025, 7, 21, 0, 0)
    end_date = datetime(2025, 8, 4, 0, 0)

    start_sprint(
        new_sprint_id,
        sprint_name,
        start_date,
        end_date,
        session_mock,
        MOCK_BASE_URL
    )

    expected_payload = {
        "state": ACTIVE,
        "name": sprint_name,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END
    }

    session_mock.put.assert_called_once_with(
        f"{MOCK_BASE_URL}/rest/agile/1.0/sprint/{new_sprint_id}",
        json=expected_payload
    )
