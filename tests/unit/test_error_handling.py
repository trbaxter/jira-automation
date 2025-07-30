import logging
from unittest.mock import Mock

import pytest
from _pytest.logging import LogCaptureFixture
from pydantic import conint, HttpUrl
from requests import Response, Request

from src.fieldtypes.common import SAFE_STR
from src.logging_config.error_handling import handle_api_error

CONTEXT = "posting to Jira"
INT_HTTP = conint(ge=100, le=599)
POST = "POST"
MOCK_BASE_URL = HttpUrl("https://fake.jira.com/")


# Mock response object created to avoid type-related warnings
def make_mock_response(
        status_code: INT_HTTP,
        text: SAFE_STR,
        url: HttpUrl,
        method: SAFE_STR
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
def test_success_responses(
        caplog: LogCaptureFixture,
        status_code: INT_HTTP
) -> None:
    response = make_mock_response(
        status_code=status_code,
        text="",
        url=MOCK_BASE_URL,
        method=POST
    )

    with caplog.at_level(level=logging.ERROR):
        result = handle_api_error(response=response, context=CONTEXT)

    assert result is True
    assert not caplog.records


def test_generic_error_logs(caplog: LogCaptureFixture) -> None:
    response = make_mock_response(
        status_code=400,
        text="Bad Request",
        url=MOCK_BASE_URL,
        method=POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response=response, context=CONTEXT)

    expected_messages = [
        "Error during posting to Jira",
        "Status Code: 400",
        "Bad Request"
    ]

    assert result is False
    assert all(msg in caplog.text for msg in expected_messages)


def test_gateway_timeout_logs(caplog: LogCaptureFixture) -> None:
    response = make_mock_response(
        status_code=504,
        text="Timeout",
        url=MOCK_BASE_URL,
        method=POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response=response, context=CONTEXT)

    expected_messages = [
        "Error during posting to Jira",
        "Status Code: 504",
        "Gateway timeout occurred"
    ]

    assert result is False
    assert "Response content" not in caplog.text
    assert all(msg in caplog.text for msg in expected_messages)
