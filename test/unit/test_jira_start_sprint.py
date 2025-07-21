from unittest.mock import patch, MagicMock
from datetime import datetime
import requests

from src.services.jira_start_sprint import start_sprint

JIRA_DATE = "src.helpers.payload_builder.format_jira_date"
JIRA_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000+0000"
JIRA_START = "src.services.jira_start_sprint"
MOCK_URL_BASE = "https://test"

@patch(f"{JIRA_START}.handle_api_error", return_value=True)
@patch(JIRA_DATE, side_effect=lambda dt: dt.strftime(JIRA_DATE_FORMAT))
def test_start_sprint_success(
        _mock_handle_error: MagicMock,
        _mock_format: MagicMock
) -> None:
    session_mock = MagicMock(spec=requests.Session)
    mock_response = MagicMock(spec=requests.Response)
    session_mock.put.return_value = mock_response

    new_sprint_id = 123
    sprint_name = "Test Sprint"
    start_date = datetime(2025, 7, 22, 9, 0)
    end_date = datetime(2025, 8, 5, 17, 0)

    start_sprint(
        new_sprint_id=new_sprint_id,
        sprint_name=sprint_name,
        start_date=start_date,
        end_date=end_date,
        session=session_mock,
        base_url=MOCK_URL_BASE
    )

    expected_payload = {
        "state": "active",
        "name": sprint_name,
        "startDate": "2025-07-22T09:00:00.000+0000",
        "endDate": "2025-08-05T17:00:00.000+0000"
    }

    session_mock.put.assert_called_once_with(
        f"{MOCK_URL_BASE}/rest/agile/1.0/sprint/{new_sprint_id}",
        json=expected_payload
    )


@patch(f"{JIRA_START}.handle_api_error", return_value=False)
@patch(JIRA_DATE, side_effect=lambda dt: dt.strftime(JIRA_DATE_FORMAT))
def test_start_sprint_failure(
        _mock_format: MagicMock,
        _mock_handle_error: MagicMock
) -> None:
    session_mock = MagicMock(spec=requests.Session)
    mock_response = MagicMock(spec=requests.Response)
    session_mock.put.return_value = mock_response

    new_sprint_id = 456
    sprint_name = "Failed Sprint"
    start_date = datetime(2025, 9, 1, 10, 0)
    end_date = datetime(2025, 9, 15, 18, 0)

    start_sprint(
        new_sprint_id=new_sprint_id,
        sprint_name=sprint_name,
        start_date=start_date,
        end_date=end_date,
        session=session_mock,
        base_url=MOCK_URL_BASE
    )

    expected_payload = {
        "state": "active",
        "name": sprint_name,
        "startDate": "2025-09-01T10:00:00.000+0000",
        "endDate": "2025-09-15T18:00:00.000+0000"
    }

    session_mock.put.assert_called_once_with(
        f"{MOCK_URL_BASE}/rest/agile/1.0/sprint/{new_sprint_id}",
        json=expected_payload
    )
