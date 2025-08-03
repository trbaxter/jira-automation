import os

from pydantic import ValidationError

from src.models.credentials import Credentials
from src.models.env_reader import EnvReader


def get_jira_credentials(getenv: EnvReader = os.getenv) -> Credentials:
    try:
        return Credentials(
            email=getenv("JIRA_EMAIL"),
            token=getenv("JIRA_API_TOKEN"),
        )
    except ValidationError as e:
        raise ValueError("Missing or invalid environment variables.") from e
