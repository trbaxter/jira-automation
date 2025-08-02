from unittest.mock import patch

from hypothesis import given

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

    assert callable(getattr(session, "request", None))
