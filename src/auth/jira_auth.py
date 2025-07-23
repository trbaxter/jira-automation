import base64
import os
from typing import NamedTuple, runtime_checkable, Protocol, Optional

from errors.missing_credentials_error import MissingCredentialsError


# ──────────────────────────────────────────────────────────────────────────────
# Types
# ──────────────────────────────────────────────────────────────────────────────
class Credentials(NamedTuple):
    email: str
    token: str


@runtime_checkable
class EnvReader(Protocol):
    """
    Serves as a type-safe contract for injecting environment values rather
    than relying on hard-coded usages of 'os.getenv'. Uses '...' to indicate
    that no class body is required to function.
    """

    def __call__(self, key: str) -> Optional[str]: ...


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────
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

    missing = []
    if not email:
        missing.append("JIRA_EMAIL")
    if not token:
        missing.append("JIRA_API_TOKEN")

    if missing:
        raise MissingCredentialsError(missing)

    return Credentials(email, token)


def make_basic_auth_token(email: str, token: str) -> str:
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
    email, token = get_jira_credentials()
    encoded_token = make_basic_auth_token(email, token)
    return {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }
