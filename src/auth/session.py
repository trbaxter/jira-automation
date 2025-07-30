import certifi
import requests
from requests.auth import HTTPBasicAuth

from src.auth.credentials import get_jira_credentials


def get_authenticated_session() -> requests.Session:
    """
    Creates & configures an authenticated HTTP session for Jira API access.

    Initializes a Session object with trusted certificate authorities and
    attaches headers required for authenticating with the Jira API.

    Returns:
        A configured session object with authentication headers.
    """
    creds = get_jira_credentials()
    session = requests.Session()
    session.auth = HTTPBasicAuth(creds.email, creds.token)
    session.verify = certifi.where()
    session.headers.update({"Content-Type": "application/json"})
    return session
