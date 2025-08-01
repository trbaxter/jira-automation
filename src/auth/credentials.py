import os

from src.models.credentials import Credentials


def get_jira_credentials(getenv = os.getenv) -> Credentials:
    """
    Retrieve Jira credentials (email and API token) from environment variables
    populated by repository secrets.

    The function expects two environment variables to be set:
        • JIRA_EMAIL
        • JIRA_API_TOKEN

    If either missing or invalid, a pydantic.ValidationError will be raised
    when constructing the Credentials object.

    Parameters:
        getenv: A callable that accepts a key string and returns an
                environment value. Defaults to os.getenv.

    Returns:
        A Credentials object containing the Jira email and API token.

    Raises:
        pydantic.ValidationError: If either environment variable is
                                  missing or invalid.
    """
    email = getenv("JIRA_EMAIL")
    token = getenv("JIRA_API_TOKEN")
    return Credentials(email=email, token=token)
