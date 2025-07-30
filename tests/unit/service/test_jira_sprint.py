from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
import requests
from hypothesis import given
from hypothesis.strategies import datetimes, integers, tuples

from src.models.sprint_payload import SprintPayload
from src.services.jira_sprint import (
    build_sprint_payload,
    post_sprint_payload,
    parse_json_response,
    create_sprint,
    get_sprint_by_state,
    get_all_future_sprints,
)
from strategies.shared import cleaned_string


@given(
    cleaned_string(),
    tuples(
        datetimes(datetime.now(), datetime.now() + timedelta(days=14)),
        datetimes(datetime.now(), datetime.now() + timedelta(days=14)),
    ).filter(lambda pair: pair[0] < pair[1]),
    integers(1, 9999),
)
def test_build_sprint_payload_returns_valid_model(
    name: str, start_end: datetime, board_id: int
):
    start, end = start_end
    payload = build_sprint_payload(name, start, end, board_id)

    assert isinstance(payload, SprintPayload)
    assert payload.name == name
    assert payload.originBoardId == board_id
    assert payload.startDate in payload.model_dump().values()
    assert payload.endDate in payload.model_dump().values()


def test_post_sprint_payload_sends_correct_request():
    session = MagicMock()
    session.post.return_value = MagicMock(status_code=200)

    payload = MagicMock()
    payload.model_dump.return_value = {"mock": "data"}

    response = post_sprint_payload(session, "https://mock/api", payload)
    assert response.status_code == 200


def test_parse_json_response_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": 1,
        "self": "...",
        "name": "Sprint A",
    }

    result = parse_json_response(mock_response)
    assert result is not None


def test_parse_json_response_logs_and_returns_none_on_decode_error(caplog):
    mock_response = MagicMock()
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
        "bad", "", 0
    )
    mock_response.text = "not json"

    result = parse_json_response(mock_response)

    assert result is None
    assert "Failed to parse JSON" in caplog.text


def test_create_sprint_successfully_returns_parsed_response():
    session = MagicMock()
    fake_response = MagicMock()
    fake_response.json.return_value = {"id": 1, "self": "...", "name": "Sprint"}
    fake_response.json.return_value = {"id": 1, "self": "...", "name": "Sprint"}

    with (
        patch("src.services.jira_sprint.load_config") as mock_cfg,
        patch("src.services.jira_sprint.handle_api_error", return_value=True),
        patch(
            "src.services.jira_sprint.parse_json_response",
            return_value="parsed",
        ) as _mock_parse,
        patch(
            "src.services.jira_sprint.post_sprint_payload",
            return_value=fake_response,
        ),
    ):

        mock_cfg.return_value.board_id = 1
        mock_cfg.return_value.base_url = "https://mock"

        result = create_sprint(
            "Test Sprint",
            datetime.now(),
            datetime.now() + timedelta(days=14),
            session,
        )

        assert result == "parsed"


def test_create_sprint_aborts_on_api_failure():
    session = MagicMock()
    with (
        patch("src.services.jira_sprint.load_config") as mock_cfg,
        patch("src.services.jira_sprint.handle_api_error", return_value=False),
    ):

        mock_cfg.return_value.board_id = 1
        mock_cfg.return_value.base_url = "https://mock"

        result = create_sprint(
            "Sprint",
            datetime.now(),
            datetime.now() + timedelta(days=14),
            session,
        )
        assert result is None


def test_get_sprint_by_state_returns_first_result():
    session = MagicMock()
    config = MagicMock()
    config.base_url = "https://mock"
    config.board_id = 10
    session.get.return_value.json.return_value = {"values": ["sprint_1"]}

    with patch("src.services.jira_sprint.handle_api_error", return_value=True):
        result = get_sprint_by_state(session, config, "active")

        assert result == "sprint_1"


def test_get_sprint_by_state_returns_none_on_error_or_empty():
    session = MagicMock()
    config = MagicMock()
    config.base_url = "https://mock"
    config.board_id = 10

    with patch("src.services.jira_sprint.handle_api_error", return_value=False):
        assert get_sprint_by_state(session, config, "future") is None

    with patch("src.services.jira_sprint.handle_api_error", return_value=True):
        session.get.return_value.json.return_value = {"values": []}
        assert get_sprint_by_state(session, config, "closed") is None


def test_get_all_future_sprints_handles_pagination():
    session = MagicMock()
    config = MagicMock()
    config.board_id = 1
    config.base_url = "https://mock"

    session.get.side_effect = [
        MagicMock(
            status_code=200, json=lambda: {"values": ["a"], "isLast": False}
        ),
        MagicMock(
            status_code=200, json=lambda: {"values": ["b"], "isLast": True}
        ),
    ]

    result = get_all_future_sprints(session, config)

    assert result == ["a", "b"]


def test_get_all_future_sprints_raises_on_non_200():
    session = MagicMock()
    config = MagicMock()
    config.board_id = 1
    config.base_url = "https://mock"

    session.get.return_value.status_code = 500
    session.get.return_value.text = "Internal Server Error"

    with pytest.raises(
        expected_exception=RuntimeError,
        match="Error while fetching future " "sprints",
    ):
        get_all_future_sprints(session, config)
