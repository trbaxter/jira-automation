from unittest.mock import patch

import pytest
from hypothesis import given
from requests.exceptions import Timeout

from src.auth.session import (
    build_authenticated_session,
    get_authenticated_session
)
from src.models.credentials import Credentials
from tests.strategies.shared import valid_credentials
from tests.utils.patch_helper import make_base_path

base_path = make_base_path('src.auth.session')


@given(credentials=valid_credentials())
def test_get_authenticated_session_success(credentials: Credentials) -> None:
    with patch(base_path('get_jira_credentials'), return_value=credentials):
        session = get_authenticated_session()
    assert callable(getattr(session, 'request', None))


@given(credentials=valid_credentials())
def test_build_authenticated_session_success(credentials: Credentials) -> None:
    session = build_authenticated_session(credentials)
    assert callable(getattr(session, 'request', None))


@given(credentials=valid_credentials())
def test_request_timeout_enforced(credentials: Credentials) -> None:
    def mock_request(_self, _method, _url, **kwargs):
        if kwargs.get('timeout', 0) > 0:
            raise Timeout('Request exceeded timeout')
        raise RuntimeError('Expected timeout not set')

    with patch('requests.Session.request', new=mock_request):
        session = build_authenticated_session(credentials)

    with pytest.raises(Timeout):
        session.request('GET', 'https://example.com')