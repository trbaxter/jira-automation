import os

from pydantic import ValidationError

from src.models.credentials import Credentials
from src.models.env_reader import EnvReader


def get_jira_credentials(getenv: EnvReader = os.getenv) -> Credentials:
    """
    Retrieve Jira credentials (email and API token) from environment variables.

    Environment Variables:
        - JIRA_EMAIL
        - JIRA_API_TOKEN

    Parameters:
        getenv: A callable that accepts a key string and returns an
                environment value or None. Defaults to os.getenv.

    Returns:
        A validated Credentials object containing the Jira email and API token.

    Raises:
        ValueError: If either variable is missing or invalid.
    """
    try:
        return Credentials(
            email=getenv("JIRA_EMAIL"),
            token=getenv("JIRA_API_TOKEN"),
        )
    except ValidationError as e:
        raise ValueError("Missing or invalid environment variables.") from e
