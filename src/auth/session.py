import certifi
import requests

from src.auth.jira_auth import get_auth_header


def get_authenticated_session() -> requests.Session:
    """
    Creates & configures an authenticated HTTP session for Jira API access.

    Initializes a Session object with trusted certificate authorities and
    attaches headers required for authenticating with the Jira API.

    Returns:
        requests.Session: A configured session object with
                          authentication headers.
    """
    session = requests.Session()
    session.verify = certifi.where()
    session.headers.update(get_auth_header())
    return session
