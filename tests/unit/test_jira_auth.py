from unittest.mock import patch

import pytest

from src.errors.missing_credentials_error import MissingCredentialsError
from src.auth.credentials import (
    Credentials,
    get_jira_credentials,
    make_basic_auth_token,
    get_auth_header
)
from tests.constants.patch_targets import (JAUTH_GET_CREDS, JAUTH_MAKE_TOKEN)

EMAIL = "JIRA_EMAIL"
TOKEN = "JIRA_API_TOKEN"


def test_get_jira_credentials_success() -> None:
    fake_env = {EMAIL: "abc123", TOKEN: "def456"}.get
    creds = get_jira_credentials(fake_env)
    assert creds == Credentials("abc123", "def456")


def test_get_jira_credentials_both_missing() -> None:
    fake_env = {EMAIL: None, TOKEN: None}.get
    with pytest.raises(MissingCredentialsError) as error:
        get_jira_credentials(fake_env)

    error_msg = str(error.value)
    assert EMAIL in error_msg
    assert TOKEN in error_msg


def test_get_jira_credentials_email_missing() -> None:
    fake_env = {EMAIL: None, TOKEN: "abc123"}.get
    with pytest.raises(MissingCredentialsError) as error:
        get_jira_credentials(fake_env)

    error_msg = str(error.value)
    assert EMAIL in error_msg
    assert TOKEN not in error_msg


def test_get_jira_credentials_token_missing() -> None:
    fake_env = {EMAIL: "abc123", TOKEN: None}.get
    with pytest.raises(MissingCredentialsError) as error:
        get_jira_credentials(fake_env)

    error_msg = str(error.value)
    assert TOKEN in error_msg
    assert EMAIL not in error_msg


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
