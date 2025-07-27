import pytest
from hypothesis import given, settings
from pydantic import ValidationError

from src.auth.credentials import get_jira_credentials
from tests.strategies.common import clean_string

EMAIL = "JIRA_EMAIL"
TOKEN = "JIRA_API_TOKEN"


@given(email=clean_string, token=clean_string)
@settings(max_examples=1000)
def test_get_jira_credentials_success(email: str, token: str) -> None:
    env_vars = {EMAIL: email, TOKEN: token}
    getenv = lambda key: env_vars.get(key)

    creds = get_jira_credentials(getenv=getenv)

    assert creds.email == email
    assert creds.token == token


@given(email=clean_string, token=clean_string)
@settings(max_examples=1000)
@pytest.mark.parametrize("missing_key", [EMAIL, TOKEN])
def test_get_jira_credentials_missing_key(
        email: str,
        missing_key: str,
        token: str
) -> None:
    def getenv(key):
        env = {
            EMAIL: email if key != EMAIL else None,
            TOKEN: token if key != TOKEN else None
        }
        return env.get(key)

    env_key_to_field = {EMAIL: "email", TOKEN: "token"}

    with pytest.raises(ValidationError) as e:
        get_jira_credentials(getenv=getenv)

    assert env_key_to_field[missing_key] in str(e.value)