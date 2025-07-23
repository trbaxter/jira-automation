from unittest.mock import MagicMock, patch

import requests

from src.services.jira_sprint_closure import close_sprint
from tests.constants.patch_targets import (
    JCLOSE_BUILD_PAYLOAD,
    JCLOSE_HANDLE_ERROR
)
from tests.constants.test_constants import (
    CLOSED,
    MOCK_BASE_URL,
    MOCK_SPRINT_END,
    MOCK_SPRINT_NAME,
    MOCK_SPRINT_START,
)


@patch(JCLOSE_HANDLE_ERROR, return_value=True)
@patch(JCLOSE_BUILD_PAYLOAD)
def test_close_sprint_success(
        mock_build_payload: MagicMock,
        _mock_handle_error: MagicMock
) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    session.put.return_value = response

    dummy_payload = {
        "state": CLOSED,
        "name": MOCK_SPRINT_NAME,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END
    }
    mock_build_payload.return_value = dummy_payload

    close_sprint(
        99,
        MOCK_SPRINT_NAME,
        MOCK_SPRINT_START,
        MOCK_SPRINT_END,
        session,
        MOCK_BASE_URL
    )

    session.put.assert_called_once_with(
        f"{MOCK_BASE_URL}/rest/agile/1.0/sprint/99",
        json=dummy_payload
    )
    mock_build_payload.assert_called_once_with(
        MOCK_SPRINT_NAME,
        MOCK_SPRINT_START,
        MOCK_SPRINT_END
    )


@patch(JCLOSE_HANDLE_ERROR, return_value=False)
@patch(JCLOSE_BUILD_PAYLOAD)
def test_close_sprint_logs_error_and_returns_early(
        mock_build_payload: MagicMock,
        _mock_handle_error: MagicMock
) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    session.put.return_value = response

    mock_build_payload.return_value = {
        "state": CLOSED,
        "name": MOCK_SPRINT_NAME,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END
    }

    close_sprint(
        99,
        MOCK_SPRINT_NAME,
        MOCK_SPRINT_START,
        MOCK_SPRINT_END,
        session,
        MOCK_BASE_URL
    )

    session.put.assert_called_once()
    mock_build_payload.assert_called_once()
