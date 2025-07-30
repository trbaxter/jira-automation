import os

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
