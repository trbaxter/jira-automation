import pytest
from unittest.mock import patch
from src.auth.jira_auth import (
    get_jira_credentials,
    make_basic_auth_token,
    get_auth_header
)
from tests.constants.test_constants import (
    GET_ENV,
    MOCK_EMAIL,
    MOCK_API_TOKEN,
    SECRETS_MISSING
)
from tests.constants.patch_targets import (JAUTH_GET_CREDS, JAUTH_MAKE_TOKEN)

def test_get_jira_credentials_returns_mocked_values() -> None:
    with patch(GET_ENV) as mock_getenv:
        mock_getenv.side_effect = lambda key: {
            "JIRA_EMAIL": MOCK_EMAIL,
            "JIRA_API_TOKEN": MOCK_API_TOKEN
        }[key]
        email, token = get_jira_credentials()
        assert email == MOCK_EMAIL
        assert token == MOCK_API_TOKEN


def test_get_jira_credentials_raises_exception_if_missing() -> None:
    with patch(GET_ENV, return_value=None):
        with pytest.raises(EnvironmentError, match=SECRETS_MISSING):
            get_jira_credentials()


# noinspection SpellCheckingInspection
def test_make_basic_auth_token_encodes_correctly() -> None:
    email = "fred"
    token = "fred"
    result = make_basic_auth_token(email, token)
    expected = "ZnJlZDpmcmVk"
    assert result == expected


def test_get_auth_header_returns_expected_structure() -> None:
    with (
        patch(JAUTH_GET_CREDS, return_value=("mock@abc.com", "mock-token")),
        patch(JAUTH_MAKE_TOKEN, return_value="encoded123")
    ):
        result = get_auth_header()
        assert result["Authorization"] == "Basic encoded123"
        assert result["Content-Type"] == "application/json"