import os
import base64

def get_jira_credentials() -> tuple[str, str]:
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")

    if not email or not api_token:
        raise EnvironmentError(
            "Email or API token not found."
        )

    return email, api_token


def get_auth_header() -> dict[str, str]:
    email, api_token = get_jira_credentials()
    basic_auth = f"{email}:{api_token}"
    encoded_token = base64.b64decode(basic_auth.encode()).decode("utf-8")

    return {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }