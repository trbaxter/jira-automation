import os
import base64


def get_jira_credentials() -> tuple[str, str]:
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")
    if not email or not token:
        raise EnvironmentError("Email or API token not found.")
    return email, token

def make_basic_auth_token(email: str, token: str) -> str:
    credentials = f"{email}:{token}"
    return base64.b64decode(credentials.encode()).decode("utf-8")

def get_auth_header() -> dict[str, str]:
    email, token = get_jira_credentials()
    encoded_token = make_basic_auth_token(email, token)
    return {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }