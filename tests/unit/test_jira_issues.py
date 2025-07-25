from unittest.mock import MagicMock, patch

import requests

from src.services.jira_issues import get_incomplete_stories, DONE_STATUSES
from tests.constants.patch_targets import JIRA_ISSUES_HANDLE_API_ERROR
from models.boardconfig import BoardConfig

MOCK_CONFIG: BoardConfig = {
    "board_id": 1,
    "base_url": "https://mocked-jira",
    "board_name": "Mock Board"
}


@patch(JIRA_ISSUES_HANDLE_API_ERROR, return_value=True)
def test_get_incomplete_stories_filters_done_statuses(
        _mock_handle_error: MagicMock
) -> None:
    session = MagicMock(spec=requests.Session)
    mock_response = MagicMock(spec=requests.Response)
    mock_response.json.return_value = {
        "issues": [
            {"fields": {"status": {"name": "In Progress"}}},
            {"fields": {"status": {"name": "Done"}}},
            {"fields": {"status": {"name": "To Do"}}}
        ]
    }
    session.get.return_value = mock_response

    results = get_incomplete_stories(1, MOCK_CONFIG, session)
    assert len(results) == 2
    for issue in results:
        assert issue["fields"]["status"]["name"] not in DONE_STATUSES


@patch(JIRA_ISSUES_HANDLE_API_ERROR, return_value=True)
def test_get_incomplete_stories_handles_pagination(
        _mock_handle_error: MagicMock
) -> None:
    session = MagicMock(spec=requests.Session)

    # Full page
    page1 = MagicMock(spec=requests.Response)
    page1.json.return_value = {
        "issues": [{"fields": {"status": {"name": "In Progress"}}}] * 50
    }

    # Partial page
    page2 = MagicMock(spec=requests.Response)
    page2.json.return_value = {
        "issues": [{"fields": {"status": {"name": "To Do"}}}] * 10
    }

    session.get.side_effect = [page1, page2]

    results = get_incomplete_stories(1, MOCK_CONFIG, session)

    assert len(results) == 60
    assert all(
        issue["fields"]["status"]["name"] not in DONE_STATUSES
        for issue in results
    )
    assert session.get.call_count == 2


@patch(JIRA_ISSUES_HANDLE_API_ERROR, return_value=False)
def test_get_incomplete_stories_handles_api_error(
        _mock_handle_error: MagicMock
) -> None:
    session = MagicMock(spec=requests.Session)
    results = get_incomplete_stories(1, MOCK_CONFIG, session)
    assert results == []
