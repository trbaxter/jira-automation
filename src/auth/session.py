from __future__ import annotations

from typing import Final

import requests
from requests.auth import HTTPBasicAuth, AuthBase

from src.auth.credentials import get_jira_credentials
from src.models.credentials import Credentials

DEFAULT_TIMEOUT: Final[float] = 10.0


def _validate_timeout(timeout: float | tuple[float, float]) -> None:
    if isinstance(timeout, tuple):
        connect, read = timeout
        if connect <= 0 or read <= 0:
            raise ValueError("Timeout values must be > 0 seconds.")
    else:
        if timeout <= 0:
            raise ValueError("Assigned timeout value must be > 0 seconds.")


class TimeoutSession(requests.Session):
    """requests.Session that applies a default timeout to every request."""
    def __init__(self, timeout: float | tuple[float, float]) -> None:
        super().__init__()
        _validate_timeout(timeout)
        self._timeout = timeout

    def request(self, *args, **kwargs):
        kwargs.setdefault("timeout", self._timeout)
        return super().request(*args, **kwargs)


def build_authenticated_session(
        credentials: Credentials,
        auth: AuthBase | None = None,
        timeout: float | tuple[float, float] = DEFAULT_TIMEOUT
) -> requests.Session:
    session = TimeoutSession(timeout)
    session.auth = auth or HTTPBasicAuth(credentials.email, credentials.token)
    session.headers.update({'Content-Type': 'application/json'})
    return session


def get_authenticated_session() -> requests.Session:
    credentials = get_jira_credentials()
    return build_authenticated_session(credentials)
