import pytest
from hypothesis import given

from src.auth.credentials import get_jira_credentials
from tests.strategies.shared import cleaned_string

EMAIL = 'JIRA_EMAIL'
TOKEN = 'JIRA_API_TOKEN'


@given(cleaned_string(), cleaned_string())
def test_get_jira_credentials_success(email, token) -> None:
    env_vars = {EMAIL: email, TOKEN: token}
    getenv = lambda key: env_vars.get(key)
    creds = get_jira_credentials(getenv)

    assert creds.email == email and creds.token == token



@given(email=cleaned_string(), token=cleaned_string())
@pytest.mark.parametrize('missing_key', [EMAIL, TOKEN])
def test_get_jira_credentials_missing_key(email, missing_key, token) -> None:
    def getenv(key):
        env = {
            EMAIL: email if key != EMAIL else None,
            TOKEN: token if key != TOKEN else None,
        }
        return env.get(key)

    with pytest.raises(ValueError) as error:
        get_jira_credentials(getenv)

    assert 'Missing or invalid' in str(error.value)



def test_get_jira_credentials_missing_both_keys() -> None:
    def getenv(_key) -> str | None:
        return None

    with pytest.raises(ValueError) as error:
        get_jira_credentials(getenv)

    assert 'Missing or invalid' in str(error.value)
