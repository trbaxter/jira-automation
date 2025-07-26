import base64
import os
from typing import runtime_checkable, Protocol

from pydantic import BaseModel, constr, ValidationError

from src.exceptions.missing_secrets_error import MissingSecretsError


class Credentials(BaseModel):
    email: constr(strip_whitespace=True, min_length=1)
    token: constr(strip_whitespace=True, min_length=1)


@runtime_checkable
class EnvReader(Protocol):
    """
    Serves as a type-safe contract for injecting environment values rather
    than relying on hard-coded usages of 'os.getenv'. Uses '...' to indicate
    that no class body is required to function.
    """

    def __call__(self, key: str) -> str: ...


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

    try:
        return Credentials(email=email, token=token)
    except ValidationError:
        missing = []
        if not email:
            missing.append("JIRA_EMAIL")
        if not token:
            missing.append("JIRA_API_TOKEN")
        raise MissingSecretsError(missing)


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
    credentials = get_jira_credentials()
    encoded_token = make_basic_auth_token(credentials.email, credentials.token)
    return {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }
