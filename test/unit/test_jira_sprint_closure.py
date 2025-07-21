from unittest.mock import MagicMock, patch
import requests

from src.services.jira_sprint_closure import close_sprint


JIRA_SPRINT_CLOSURE = "src.services.jira_sprint_closure"
MOCK_URL = "https://mocked-jira"
MOCK_SPRINT_ID = 99
MOCK_NAME = "Sprint 99"
MOCK_START = "2025-08-01T00:00:00.000Z"
MOCK_END = "2025-08-15T00:00:00.000Z"


@patch(f"{JIRA_SPRINT_CLOSURE}.handle_api_error", return_value=True)
@patch(f"{JIRA_SPRINT_CLOSURE}.build_close_sprint_payload")
def test_close_sprint_success(
        mock_build_payload: MagicMock,
        _mock_handle_error: MagicMock
) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    session.put.return_value = response

    dummy_payload = {
        "state": "closed",
        "name": MOCK_NAME,
        "startDate": MOCK_START,
        "endDate": MOCK_END
    }
    mock_build_payload.return_value = dummy_payload

    close_sprint(
        sprint_id=MOCK_SPRINT_ID,
        sprint_name=MOCK_NAME,
        start_date=MOCK_START,
        end_date=MOCK_END,
        session=session,
        base_url=MOCK_URL
    )

    session.put.assert_called_once_with(
        f"{MOCK_URL}/rest/agile/1.0/sprint/{MOCK_SPRINT_ID}",
        json=dummy_payload
    )
    mock_build_payload.assert_called_once_with(
        MOCK_NAME,
        MOCK_START,
        MOCK_END
    )


@patch(f"{JIRA_SPRINT_CLOSURE}.handle_api_error", return_value=False)
@patch(f"{JIRA_SPRINT_CLOSURE}.build_close_sprint_payload")
def test_close_sprint_logs_error_and_returns_early(
        mock_build_payload: MagicMock,
        _mock_handle_error: MagicMock
) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    session.put.return_value = response

    mock_build_payload.return_value = {
        "state": "closed",
        "name": MOCK_NAME,
        "startDate": MOCK_START,
        "endDate": MOCK_END
    }

    close_sprint(
        sprint_id=MOCK_SPRINT_ID,
        sprint_name=MOCK_NAME,
        start_date=MOCK_START,
        end_date=MOCK_END,
        session=session,
        base_url=MOCK_URL
    )

    # Ensure we didn't proceed beyond error
    session.put.assert_called_once()
    mock_build_payload.assert_called_once()