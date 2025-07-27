import pytest
from hypothesis import given, settings

from src.auth.credentials import get_jira_credentials
from tests.strategies.common import clean_string


@given(email=clean_string, token=clean_string)
@settings(max_examples=100)
def test_get_jira_credentials_success(email: str, token: str) -> None:
    env_vars = {"JIRA_EMAIL": email, "JIRA_API_TOKEN": token}
    getenv = lambda key: env_vars.get(key)

    creds = get_jira_credentials(getenv=getenv)

    assert creds.email == email
    assert creds.token == token


# @pytest.mark.parametrize("missing_key", ["JIRA_EMAIL", "JIRA_API_TOKEN"])
# def test_get_jira_credentials_missing_key(missing_key: str) -> None:
#     def getenv(key):
#         env = {
#             "JIRA_EMAIL": "test@example.com" if key != "JIRA_EMAIL" else None,
#             "JIRA_API_TOKEN": "abcd1234" if key != "JIRA_API_TOKEN" else None
#         }
#         return env.get(key)
#
#     with pytest.raises(MissingSecretsError) as e:
#         get_jira_credentials(getenv=getenv)
#
#     assert missing_key in str(e.value)