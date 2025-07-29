import base64
import os

from src.fieldtypes.common import SAFE_STR
from src.models.credentials import Credentials
from src.models.env_reader import EnvReader


def get_jira_credentials(getenv: EnvReader = os.getenv) -> Credentials:
    """
    Retrieves Jira credentials (email and API token) from repository secrets.

    Returns:
        The values of the email and API token.

    Raises:
        MissingCredentialsError: If credentials are missing from the repository.
    """
    email = getenv("JIRA_EMAIL")
    token = getenv("JIRA_API_TOKEN")
    return Credentials(email=email, token=token)


def make_basic_auth_token(email: SAFE_STR, token: SAFE_STR) -> str:
    """
    Creates an encoded token.

    Uses values of the email and API token repository secrets to generate a
    base-64 encoded token required for authentication by the Jira API.

    Args:
        email: Email address of Jira admin capable of making sprint changes.
        token: API token assigned to the above email address.

    Returns:
        String containing the base-64 encoded token.
    """
    credentials = f"{email}:{token}"
    return base64.b64encode(credentials.encode()).decode("utf-8")


def get_auth_header() -> dict[str, str]:
    """
    Constructs the HTTP authorization header for Jira API requests.

    Retrieves the credentials, encodes them using base64, and formats the
    header as required for Basic Authentication.

    Returns:
        A dictionary containing the Authorization and Content-Type headers to
        include in an HTTP request.
    """
    credentials = get_jira_credentials()
    email = credentials.email
    token = credentials.token

    encoded_token = make_basic_auth_token(email=email, token=token)

    return {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }
