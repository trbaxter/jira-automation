import requests
from requests.auth import HTTPBasicAuth, AuthBase

from src.auth.credentials import get_jira_credentials
from src.models.credentials import Credentials

DEFAULT_TIMEOUT = 10

def enforce_request_timeout(session: requests.Session, timeout: int) -> None:
    original = session.request
    def with_timeout(*args, **kwargs):
        kwargs.setdefault("timeout", timeout)
        return original(*args, **kwargs)
    session.request = with_timeout


def build_authenticated_session(
        credentials: Credentials,
        auth: AuthBase | None = None
) -> requests.Session:
    session = requests.Session()
    session.auth = auth or HTTPBasicAuth(credentials.email, credentials.token)
    session.headers.update({"Content-Type": "application/json"})
    enforce_request_timeout(session, DEFAULT_TIMEOUT)
    return session


def get_authenticated_session() -> requests.Session:
    creds = get_jira_credentials()
    return build_authenticated_session(creds)
