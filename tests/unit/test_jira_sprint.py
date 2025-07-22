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
from tests.constants.test_constants import (
    ACTIVE,
    FUTURE,
    LOCALHOST,
    MOCK_BOARD_NAME,
    MOCK_SPRINT_END,
    MOCK_SPRINT_NAME,
    MOCK_SPRINT_START
)
from tests.constants.patch_targets import (
    JSPRINT_GET_CONFIG,
    JSPRINT_HANDLE_ERROR,
    JSPRINT_PARSE_RESPONSE,
    JSPRINT_POST_PAYLOAD
)

SPRINT_URL = "https://stuff/rest/agile/1.0/sprint/123"
POST_URL = "https://localhost/rest/agile/1.0/sprint"
BOARD_ID = 42


@pytest.fixture
def sample_payload() -> SprintPayload:
    return {
        "name": MOCK_SPRINT_NAME,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END,
        "originBoardId": BOARD_ID
    }


def test_build_sprint_payload(sample_payload: SprintPayload) -> None:
    result = build_sprint_payload(
        MOCK_SPRINT_NAME,
        datetime(2025, 7, 21, 0, 0),
        datetime(2025, 8, 4, 0, 0),
        BOARD_ID
    )
    assert result == sample_payload


def test_parse_json_response_success() -> None:
    response = MagicMock(requests.Response)
    response.json.return_value = {
        "id": 123,
        "self": SPRINT_URL,
        "state": FUTURE,
        "name": MOCK_SPRINT_NAME,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END,
        "originBoardId": BOARD_ID
    }

    result = parse_json_response(response)
    assert isinstance(result, dict)
    assert result["id"] == 123
    assert result["self"] == SPRINT_URL
    assert result["state"] == FUTURE
    assert result["name"] == MOCK_SPRINT_NAME
    assert result["startDate"] == MOCK_SPRINT_START
    assert result["endDate"] == MOCK_SPRINT_END
    assert result["originBoardId"] == BOARD_ID


def test_parse_json_response_failure(caplog: LogCaptureFixture) -> None:
    response = MagicMock(requests.Response)
    response.json.side_effect = (
        requests.exceptions.JSONDecodeError("Invalid", "", 0)
    )
    response.text = "Invalid JSON"

    with caplog.at_level(logging.ERROR):
        result = parse_json_response(response)

    assert result is None
    assert "Failed to parse JSON" in caplog.text
    assert "Invalid JSON" in caplog.text


@patch(JSPRINT_GET_CONFIG)
@patch(JSPRINT_POST_PAYLOAD)
@patch(JSPRINT_PARSE_RESPONSE)
@patch(JSPRINT_HANDLE_ERROR, return_value=True)
def test_create_sprint_success(
        mock_handle_error: MagicMock,
        mock_parse_response: MagicMock,
        mock_post_payload: MagicMock,
        mock_get_config: MagicMock,
        sample_payload: SprintPayload
) -> None:
    session = MagicMock()
    mock_get_config.return_value = {
        "board_id": 42,
        "base_url": LOCALHOST,
        "board_name": MOCK_BOARD_NAME
    }
    mock_post_payload.return_value = MagicMock(spec=requests.Response)

    expected_response: SprintCreateResponse = {
        "id": 123,
        "name": MOCK_SPRINT_NAME,
        "state": FUTURE,
        "originBoardId": BOARD_ID,
        "self": SPRINT_URL,
        "startDate": MOCK_SPRINT_START,
        "endDate": MOCK_SPRINT_END,
    }

    mock_parse_response.return_value = expected_response

    result = create_sprint(
        MOCK_BOARD_NAME,
        MOCK_SPRINT_NAME,
        datetime(2025, 7, 21),
        datetime(2025, 8, 4),
        session
    )

    assert result is not None
    assert result == expected_response
    mock_handle_error.assert_called_once()
    mock_get_config.assert_called_once_with(
        MOCK_BOARD_NAME,
        "board_config.yaml"
    )


@patch(JSPRINT_HANDLE_ERROR, return_value=False)
@patch(JSPRINT_GET_CONFIG)
@patch(JSPRINT_POST_PAYLOAD)
def test_create_sprint_handles_api_error(
        mock_post_payload: MagicMock,
        mock_get_config: MagicMock,
        mock_handle_error: MagicMock
) -> None:
    session = MagicMock()
    mock_get_config.return_value = {
        "board_id": 99,
        "base_url": LOCALHOST,
        "board_name": MOCK_BOARD_NAME
    }
    mock_post_payload.return_value = MagicMock(spec=requests.Response)

    result = create_sprint(
        MOCK_BOARD_NAME,
        MOCK_SPRINT_NAME,
        datetime(2025, 7, 21),
        datetime(2025, 8, 4),
        session
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


@patch(JSPRINT_HANDLE_ERROR, return_value=True)
def test_get_sprint_by_state_success(mock_handle_error) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)

    response.json.return_value = {
        "values": [{
            "id": 123,
            "name": MOCK_SPRINT_NAME,
            "state": ACTIVE,
            "originBoardId": BOARD_ID,
            "startDate": MOCK_SPRINT_START,
            "endDate": MOCK_SPRINT_END,
            "self": "https://example.atlassian.net/rest/agile/1.0/sprint/123"
        }]
    }
    session.get.return_value = response

    config: BoardConfig = {
        "board_id": BOARD_ID,
        "base_url": "https://example.atlassian.net/",
        "board_name": MOCK_BOARD_NAME
    }

    result = get_sprint_by_state(session, config, ACTIVE)
    assert result is not None
    assert result["id"] == 123
    assert result["name"] == MOCK_SPRINT_NAME
    assert result["state"] == ACTIVE
    assert result["originBoardId"] == BOARD_ID
    assert result["startDate"] == MOCK_SPRINT_START
    assert result["endDate"] == MOCK_SPRINT_END
    mock_handle_error.assert_called_once()


@patch(JSPRINT_HANDLE_ERROR, return_value=False)
def test_get_sprint_by_state_api_error(mock_handle_error) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    session.get.return_value = response

    config: BoardConfig = {
        "board_id": 5,
        "base_url": "https://example.atlassian.net",
        "board_name": MOCK_BOARD_NAME
    }

    result = get_sprint_by_state(session, config, FUTURE)
    assert result is None
    mock_handle_error.assert_called_once()


@patch(JSPRINT_HANDLE_ERROR, return_value=True)
def test_get_sprint_by_state_empty_result(_mock_handle_error) -> None:
    session = MagicMock(spec=requests.Session)
    response = MagicMock(spec=requests.Response)
    response.json.return_value = {"values": []}
    session.get.return_value = response

    config: BoardConfig = {
        "board_id": 27,
        "base_url": "https://example.atlassian.net",
        "board_name": MOCK_BOARD_NAME
    }

    result = get_sprint_by_state(session, config, ACTIVE)
    assert result is None