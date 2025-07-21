from unittest.mock import MagicMock, patch

import requests

from src.constants.jira_statuses import DONE_STATUSES
from src.services.jira_issues import get_incomplete_stories
from type_defs.boardconfig import BoardConfig

JIRA_ISSUES = "src.services.jira_issues"
MOCK_CONFIG: BoardConfig = {
    "id": 1,
    "name": "Mock Board",
    "base_url": "https://mocked-jira"
}


@patch(f"{JIRA_ISSUES}.handle_api_error", return_value=True)
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


@patch(f"{JIRA_ISSUES}.handle_api_error", return_value=True)
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
