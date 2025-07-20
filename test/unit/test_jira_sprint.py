import logging
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
import requests
from _pytest.logging import LogCaptureFixture

from src.services.jira_sprint import (
    build_sprint_payload,
    create_sprint,
    get_sprint_by_state,
    parse_json_response,
    post_sprint_payload
)
from src.type_defs.payload import SprintPayload
from src.type_defs.sprint_create_response import SprintCreateResponse
from type_defs.boardconfig import BoardConfig

SPRINT_NAME = "Test Sprint Name"
SPRINT_START = "2025-07-21T00:00:00.000+0000"
SPRINT_END = "2025-08-04T00:00:00.000+0000"
SPRINT_URL = "https://stuff/rest/agile/1.0/sprint/123"
LOCALHOST = "https://localhost"
FUTURE = "future"
ACTIVE = "active"
POST_URL = "https://localhost/rest/agile/1.0/sprint"
BOARD_ID = 42

GET_BOARD_CONFIG = "src.services.jira_sprint.get_board_config"
POST_SPRINT_PAYLOAD = "src.services.jira_sprint.post_sprint_payload"
PARSE_JSON_RESPONSE = "src.services.jira_sprint.parse_json_response"
HANDLE_API_ERROR = "src.services.jira_sprint.handle_api_error"


@pytest.fixture
def sample_payload() -> SprintPayload:
    return {
        "name": SPRINT_NAME,
        "startDate": SPRINT_START,
        "endDate": SPRINT_END,
        "originBoardId": BOARD_ID
    }


def test_build_sprint_payload(sample_payload: SprintPayload) -> None:
    result = build_sprint_payload(
        sprint_name=SPRINT_NAME,
        sprint_start=datetime(2025, 7, 21, 0, 0),
        sprint_end=datetime(2025, 8, 4, 0, 0),
        board_id=BOARD_ID
    )
    assert result == sample_payload


def test_parse_json_response_success() -> None:
    response = MagicMock(spec=requests.Response)
    response.json.return_value = {
        "id": 123,
        "self": SPRINT_URL,
        "state": FUTURE,
        "name": SPRINT_NAME,
        "startDate": SPRINT_START,
        "endDate": SPRINT_END,
        "originBoardId": BOARD_ID
    }

    result = parse_json_response(response)
    assert isinstance(result, dict)
    assert result["id"] == 123
    assert result["self"] == SPRINT_URL
    assert result["state"] == FUTURE
    assert result["name"] == SPRINT_NAME
    assert result["startDate"] == SPRINT_START
    assert result["endDate"] == SPRINT_END
    assert result["originBoardId"] == BOARD_ID


def test_parse_json_response_failure(caplog: LogCaptureFixture) -> None:
    response = MagicMock(spec=requests.Response)
    response.json.side_effect = (
        requests.exceptions.JSONDecodeError("Invalid", "", 0)
    )
    response.text = "Invalid JSON"

    with caplog.at_level(logging.ERROR):
        result = parse_json_response(response)

    assert result is None
    assert "Failed to parse JSON" in caplog.text
    assert "Invalid JSON" in caplog.text


@patch(GET_BOARD_CONFIG)
@patch(POST_SPRINT_PAYLOAD)
@patch(PARSE_JSON_RESPONSE)
@patch(HANDLE_API_ERROR, return_value=True)
def test_create_sprint_success(
        mock_handle_error: MagicMock,
        mock_parse_response: MagicMock,
        mock_post_payload: MagicMock,
        mock_get_config: MagicMock,
        sample_payload: SprintPayload
) -> None:
    session = MagicMock()
    mock_get_config.return_value = {
        "id": 42,
        "base_url": LOCALHOST,
        "name": "Some Board"
    }
    mock_post_payload.return_value = MagicMock(spec=requests.Response)

    expected_response: SprintCreateResponse = {
        "id": 123,
        "name": SPRINT_NAME,
        "state": FUTURE,
        "originBoardId": BOARD_ID,
        "self": SPRINT_URL,
        "startDate": SPRINT_START,
        "endDate": SPRINT_END,
    }

    mock_parse_response.return_value = expected_response

    result = create_sprint(
        board_name="Some Board",
        sprint_name=SPRINT_NAME,
        start_date=datetime(2025, 7, 21),
        end_date=datetime(2025, 8, 4),
        session=session
    )

    assert result is not None
    assert result == expected_response
    mock_handle_error.assert_called_once()
    mock_get_config.assert_called_once_with(
        "Some Board",
        "board_config.yaml"
    )


@patch(HANDLE_API_ERROR, return_value=False)
@patch(GET_BOARD_CONFIG)
@patch(POST_SPRINT_PAYLOAD)
def test_create_sprint_handles_api_error(
        mock_post_payload: MagicMock,
        mock_get_config: MagicMock,
        mock_handle_error: MagicMock
) -> None:
    session = MagicMock()
    mock_get_config.return_value = {
        "id": 99,
        "base_url": LOCALHOST,
        "name": "ErrorBoard"
    }
    mock_post_payload.return_value = MagicMock(spec=requests.Response)

    result = create_sprint(
        board_name="error_board",
        sprint_name="error",
        start_date=datetime(2025, 7, 21),
        end_date=datetime(2025, 8, 4),
        session=session
    )

    assert result is None
    mock_handle_error.assert_called_once()


def test_post_sprint_payload_executes_post_call(
        sample_payload: SprintPayload
) -> None:
    session = MagicMock(spec=requests.Session)
    fake_response = MagicMock(spec=requests.Response)
    session.post.return_value = fake_response

    result = post_sprint_payload(session, POST_URL, sample_payload)
    session.post.assert_called_once_with(POST_URL, json=sample_payload)
    assert result == fake_response


@patch(HANDLE_API_ERROR, return_value=True)
def test_get_sprint_by_state_success(mock_handle_error) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)

    response.json.return_value = {
        "values": [{
            "id": 123,
            "name": SPRINT_NAME,
            "state": ACTIVE,
            "originBoardId": BOARD_ID,
            "startDate": SPRINT_START,
            "endDate": SPRINT_END,
            "self": "https://example.atlassian.net/rest/agile/1.0/sprint/123"
        }]
    }
    session.get.return_value = response

    config: BoardConfig = {
        "id": BOARD_ID,
        "name": "Test Board",
        "base_url": "https://example.atlassian.net/"
    }

    result = get_sprint_by_state(session, config, ACTIVE)
    assert result is not None
    assert result["id"] == 123
    assert result["name"] == SPRINT_NAME
    assert result["state"] == ACTIVE
    assert result["originBoardId"] == BOARD_ID
    assert result["startDate"] == SPRINT_START
    assert result["endDate"] == SPRINT_END
    mock_handle_error.assert_called_once()


@patch(HANDLE_API_ERROR, return_value=False)
def test_get_sprint_by_state_api_error(mock_handle_error) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    session.get.return_value = response

    config: BoardConfig = {
        "id": 5,
        "name": "Test Board",
        "base_url": "https://example.atlassian.net"
    }

    result = get_sprint_by_state(session, config, FUTURE)
    assert result is None
    mock_handle_error.assert_called_once()


@patch(HANDLE_API_ERROR, return_value=True)
def test_get_sprint_by_state_empty_result(mock_handle_error) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    response.json.return_value = {"values": []}
    session.get.return_value = response

    config: BoardConfig = {
        "id": 27,
        "name": "Test",
        "base_url": "https://example.atlassian.net"
    }

    result = get_sprint_by_state(session, config, ACTIVE)
    assert result is None