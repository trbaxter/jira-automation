import base64
from unittest.mock import patch

import requests
from hypothesis import given

from src.auth.session import get_authenticated_session
from strategies.common import cleaned_string


@given(cleaned_string(), cleaned_string())
def test_get_authenticated_session_success(email: str, token: str) -> None:
    credentials_str = f"{email}:{token}"
    encoded_token = base64.b64encode(credentials_str.encode()).decode("utf-8")

    expected_header = {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json",
    }

    with patch(
        "src.auth.session.get_auth_header", return_value=expected_header
    ):
        session = get_authenticated_session()

    assert isinstance(session, requests.Session)
    assert isinstance(session.verify, str) and session.verify
    assert {"Authorization", "Content-Type"}.issubset(session.headers.keys())
    assert session.headers["Authorization"] == f"Basic {encoded_token}"
    assert session.headers["Content-Type"] == "application/json"
