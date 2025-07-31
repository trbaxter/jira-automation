from unittest.mock import patch

import requests
from hypothesis import given
from requests.auth import HTTPBasicAuth

from src.auth.session import get_authenticated_session
from src.models.credentials import Credentials
from tests.strategies.shared import cleaned_string
from tests.utils.patch_helper import make_base_path

base_path = make_base_path("src.auth.session")


@given(cleaned_string(), cleaned_string())
def test_get_authenticated_session_success(email: str, token: str) -> None:
    creds = Credentials(email=email, token=token)

    with patch(base_path("get_jira_credentials"), return_value=creds):
        session = get_authenticated_session()

    assert isinstance(session, requests.Session)
    assert isinstance(session.verify, str) and session.verify
    assert session.headers["Content-Type"] == "application/json"

    # Proper type narrowing
    assert isinstance(session.auth, HTTPBasicAuth)
    assert session.auth.username == email
    assert session.auth.password == token
