import os
import base64


def get_jira_credentials() -> tuple[str, str]:
    """
    Retrieves Jira credentials (email and API token) from repository secrets.

    Returns:
        tuple [str, str]: The values of the email and API token.

    Raises:
        EnvironmentError: If either credential is missing from the repository.
    """
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")
    if not email or not token:
        raise EnvironmentError("Email or API token not found.")
    return email, token


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
    return base64.b64encode(credentials.encode()).decode("utf-8") # correct?


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