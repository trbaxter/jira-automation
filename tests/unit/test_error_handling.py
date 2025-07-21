import logging
import pytest
from unittest.mock import Mock
from requests import Response, Request
from _pytest.logging import LogCaptureFixture
from logging_config.error_handling import handle_api_error


URL = "http://some.fake.url"
POST = "POST"
JIRA_ERROR = "Error during posting to Jira"


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
        status_code=status_code,
        text="",
        url=URL,
        method=POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response, "test success case")

    assert result is True
    assert not caplog.records


def test_generic_error_logs(caplog: LogCaptureFixture) -> None:
    response = make_mock_response(
        status_code=400,
        text="Bad Request",
        url=URL,
        method=POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response, "posting to Jira")

    assert result is False
    assert "Error during posting to Jira. Status Code: 400" in caplog.text
    assert "Response content: Bad Request" in caplog.text


def test_gateway_timeout_logs(caplog: LogCaptureFixture) -> None:
    response = make_mock_response(
        status_code=504,
        text="Timeout",
        url=URL,
        method=POST
    )

    with caplog.at_level(logging.ERROR):
        result = handle_api_error(response, "posting to Jira")

    assert result is False
    assert "Error during posting to Jira. Status Code: 504" in caplog.text
    assert "Gateway timeout occurred." in caplog.text
    assert "Response content" not in caplog.text
