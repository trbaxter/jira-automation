import certifi
import requests
from requests.auth import HTTPBasicAuth

from src.auth.credentials import get_jira_credentials


def get_authenticated_session() -> requests.Session:
    """
    Create and return a pre-configured Session object for authenticated
    access to the Jira API.

    The session ncludes:
        • HTTP Basic Authentication using Jira credentials (email + API token)
        • Certificate verification via certifi
        • Default JSON content headers

    Returns:
        A configured Session object.
    """
    creds = get_jira_credentials()
    session = requests.Session()
    session.auth = HTTPBasicAuth(creds.email, creds.token)
    session.verify = certifi.where()
    session.headers.update({"Content-Type": "application/json"})
    return session
