from unittest.mock import MagicMock, patch

import pytest
from hypothesis import given
from hypothesis.strategies import text, one_of, sampled_from, lists, just
from pydantic import HttpUrl

from src.models.board_config import BoardConfig
from src.services.jira_issues import DONE_STATUSES, get_incomplete_stories


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def mock_config() -> BoardConfig:
    return BoardConfig(
        board_id=123,
        base_url=HttpUrl("https://example.atlassian.net"),
        board_name="TEST",
    )


non_done_statuses = text(min_size=1).filter(
    lambda string: string not in DONE_STATUSES
)

status_name_strategy = one_of(
    sampled_from(list(DONE_STATUSES)), non_done_statuses
)


# helper function specifically for testing purposes
def filter_incomplete_issues(issues: list[dict]) -> list[dict]:
    return [
        issue
        for issue in issues
        if issue.get("fields", {}).get("status", {}).get("name")
           not in DONE_STATUSES
    ]


@given(
    lists(
        status_name_strategy.map(
            lambda name: {"fields": {"status": {"name": name}}}
        )
    )
)
def test_filter_incomplete_issues_correctly(issues) -> None:
    result = filter_incomplete_issues(issues)

    for issue in result:
        status = issue["fields"]["status"]["name"]
        assert status not in DONE_STATUSES

    done_issues = [
        i for i in issues if i["fields"]["status"]["name"] in DONE_STATUSES
    ]
    assert len(issues) == len(result) + len(done_issues)


@given(
    issues=lists(
        one_of(
            just({}),
            just({"fields": {}}),
            just({"fields": {"status": {}}}),
            just({"fields": {"status": {"name": None}}}),
            just({"fields": {"status": {"name": "To Do"}}}),
            just({"fields": {"status": {"name": "Done"}}}),
            just({"fields": {"status": {"name": "Random"}}}),
            just({"fields": {"status": {"name": "Cancelled"}}}),
            just({"fields": {"status": {"name": "In Progress"}}}),
            just({"fields": {"status": {"name": "Abandoned"}}}),
            just({"fields": {"status": {"name": "Existing Solution"}}}),
            just({"fields": {"status": {"name": "Blocked"}}}),
            just(
                {"fields": {"status": {"name": text(min_size=1, max_size=20)}}}
            ),
        )
    )
)
def test_filter_ignores_malformed_issues(issues: list[dict]) -> None:
    try:
        result = filter_incomplete_issues(issues=issues)
    except Exception as error:
        assert (
            False
        ), f"Function should not raise on malformed issues. Raised: {error}"

    for issue in result:
        name = issue.get("fields", {}).get("status", {}).get("name")
        assert name not in DONE_STATUSES


def test_returns_empty_list_if_api_error_detected(
        mock_session: MagicMock, mock_config: BoardConfig
) -> None:
    mock_session.get.return_value = MagicMock()
    with patch(
            target="src.services.jira_issues.handle_api_error",
            return_value=False
    ):
        result = get_incomplete_stories(
            sprint_id=42, config=mock_config, session=mock_session
        )
        assert result == []


def test_returns_incomplete_stories_across_pages(
        mock_session: MagicMock, mock_config: BoardConfig
) -> None:
    page1_issues = [{"fields": {"status": {"name": "To Do"}}}] * 49 + [
        {"fields": {"status": {"name": "Done"}}}
    ]
    page2_issues = [{"fields": {"status": {"name": "In Progress"}}}]

    page1 = {"issues": page1_issues}
    page2 = {"issues": page2_issues}

    mock_session.get.side_effect = [
        MagicMock(json=lambda: page1),
        MagicMock(json=lambda: page2),
    ]

    with patch(
            target="src.services.jira_issues.handle_api_error",
            return_value=True
    ):
        result = get_incomplete_stories(
            sprint_id=123, config=mock_config, session=mock_session
        )

    assert len(result) == 50


def test_stops_fetching_when_results_less_than_max(
        mock_session: MagicMock, mock_config: BoardConfig
) -> None:
    response_data = {
        "issues": [
            {"fields": {"status": {"name": "To Do"}}},
            {"fields": {"status": {"name": "Done"}}},
            {"fields": {"status": {"name": "In Progress"}}},
        ]
    }

    mock_response = MagicMock()
    mock_response.json.return_value = response_data
    mock_session.get.return_value = mock_response

    with patch(
            target="src.services.jira_issues.handle_api_error",
            return_value=True
    ):
        result = get_incomplete_stories(
            sprint_id=99, config=mock_config, session=mock_session
        )

    assert result == [
        {"fields": {"status": {"name": "To Do"}}},
        {"fields": {"status": {"name": "In Progress"}}},
    ]

    called_params = mock_session.get.call_args.kwargs["params"]
    assert called_params["startAt"] == 0
