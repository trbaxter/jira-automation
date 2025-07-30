import base64
from unittest.mock import patch

import pytest
from hypothesis import given
from pydantic import ValidationError

from src.auth.credentials import (
    get_jira_credentials,
    make_basic_auth_token,
    get_auth_header,
)
from src.models.credentials import Credentials
from tests.strategies.common import cleaned_string

EMAIL = "JIRA_EMAIL"
TOKEN = "JIRA_API_TOKEN"


@given(email=cleaned_string(), token=cleaned_string())
def test_get_jira_credentials_success(email: str, token: str) -> None:
    env_vars = {EMAIL: email, TOKEN: token}
    getenv = lambda key: env_vars.get(key)

    creds = get_jira_credentials(getenv)

    assert creds.email == email
    assert creds.token == token


@given(email=cleaned_string(), token=cleaned_string())
@pytest.mark.parametrize("missing_key", [EMAIL, TOKEN])
def test_get_jira_credentials_missing_key(
    email: str, missing_key: str, token: str
) -> None:
    def getenv(key):
        env = {
            EMAIL: email if key != EMAIL else None,
            TOKEN: token if key != TOKEN else None,
        }
        return env.get(key)

    env_key_to_field = {EMAIL: "email", TOKEN: "token"}

    with pytest.raises(ValidationError) as error:
        get_jira_credentials(getenv)

    assert env_key_to_field[missing_key] in str(error.value)


def test_get_jira_credentials_missing_both_keys() -> None:
    def getenv(_key: str) -> str | None:
        return None

    with pytest.raises(ValidationError) as error:
        get_jira_credentials(getenv)

    message = str(error.value)
    assert "email" in message
    assert "token" in message


@given(email=cleaned_string(), token=cleaned_string())
def test_make_basic_auth_token_success(email: str, token: str) -> None:
    auth_token = make_basic_auth_token(email, token)

    decoded = base64.b64decode(auth_token).decode("utf-8")

    assert isinstance(auth_token, str)
    assert decoded == f"{email}:{token}"


@given(email=cleaned_string(), token=cleaned_string())
def test_get_auth_header_success(email: str, token: str) -> None:
    creds = Credentials(email=email, token=token)
    expected_token = base64.b64encode(f"{email}:{token}".encode()).decode(
        "utf-8"
    )

    with patch("src.auth.credentials.get_jira_credentials", return_value=creds):
        header = get_auth_header()

    assert isinstance(header, dict)
    assert set(header.keys()) == {"Authorization", "Content-Type"}
    assert header["Authorization"] == f"Basic {expected_token}"
    assert header["Content-Type"] == "application/json"
