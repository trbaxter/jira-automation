import logging
from unittest.mock import Mock

import pytest
from _pytest.logging import LogCaptureFixture
from requests import Response, Request

from logging_config.error_handling import handle_api_error
from tests.constants.test_constants import (
    BAD_REQUEST,
    BAD_REQUEST_ERROR,
    GATEWAY_TIMEOUT_ERROR,
    MOCK_BASE_URL,
    POST,
    TIMEOUT,
    TIMEOUT_JIRA_ERROR
)


# Mock response object created to avoid type-related warnings
def make_mock_response(
        status_code: int,
        text: str,
        url: str,
        method: str
) -> Response:
    mock_response = Mock(spec=Response)
    mock_response.status_code = status_code
    mock_response.text = text
    mock_response.url = url

    mock_request = Mock(spec=Request)
    mock_request.method = method
    mock_response.request = mock_request

    return mock_response


@pytest.mark.parametrize("status_code", [200, 201, 204])
def test_success_responses(caplog: LogCaptureFixture, status_code: int) -> None:
    response = make_mock_response(
        status_code,
        "",
        MOCK_BASE_URL,
        POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response, "test success case")

    assert result is True
    assert not caplog.records


def test_generic_error_logs(caplog: LogCaptureFixture) -> None:
    response = make_mock_response(
        400,
        BAD_REQUEST,
        MOCK_BASE_URL,
        POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response, "posting to Jira")

    assert result is False
    assert BAD_REQUEST_ERROR in caplog.text
    assert "Response content: Bad Request" in caplog.text


def test_gateway_timeout_logs(caplog: LogCaptureFixture) -> None:
    response = make_mock_response(
        504,
        TIMEOUT,
        MOCK_BASE_URL,
        POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response, "posting to Jira")

    assert result is False
    assert TIMEOUT_JIRA_ERROR in caplog.text
    assert GATEWAY_TIMEOUT_ERROR in caplog.text
    assert "Response content" not in caplog.text
