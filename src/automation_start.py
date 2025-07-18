import base64
import logging
import os

import certifi
import requests

# Configure logging
logging.basicConfig(level = logging.INFO, format = "%(message)s")

# Load JIRA credentials from repo secrets
EMAIL = os.getenv("JIRA_EMAIL", "")
API_TOKEN = os.getenv("JIRA_API_TOKEN", "")

# Validate repository secrets.
if not EMAIL or not API_TOKEN:
    raise EnvironmentError("Error: Repository secret not found.")

# JIRA API token config
basic_auth = f"{EMAIL}:{API_TOKEN}"
encoded_token = base64.b64encode(basic_auth.encode()).decode("utf-8")

# Reuse the HTTPS session to optimize requests
session = requests.Session()
session.verify = certifi.where()
session.headers.update(
    {
        "Authorization": f"Basic {encoded_token}",
        "Content-Type": "application/json"
    }
)


# Format the start/end dates of generated sprints
def format_jira_date(date) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S.000+0000")

# Dynamically generate sprint name if needed
def generate_sprint_name(start_date, end_date) -> str:
    sprint_name = (f"Sprint_Name {start_date.strftime("%y%m%d")} "
                   f"({start_date.strftime("%m/%d")}-"
                   f"{end_date.strftime('%m/%d')}")
    return sprint_name


# Log errors in workflow during calls to Jira API
def handle_api_error(response, context) -> bool:
    if response.status_code not in [200, 201, 204]:
        logging.error(
            f"\nError during {context}. Status Code: {response.status_code}"
        )

        if response.status_code == 504:
            logging.error("Gateway timeout occurred.")

        else:
            logging.error(f"Response content: {response.text}")

        return False
    return True


# Sends JSON payload to create sprint
def create_sprint(sprint_name, start_date, end_date, config) -> None:
    url = f"{config.base_url}/rest/agile/1.0/sprint"
    payload = {
        "name": sprint_name,
        "startDate": format_jira_date(start_date),
        "endDate": format_jira_date(end_date),
        "originBoardId": config.board_id
    }

    response = session.post(url, json = payload)
    if not handle_api_error(response, "creating sprint"):
        return None

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        logging.error("Error: Failed to parse JSON response.")
        logging.error(f"Response Content: {response.text}")
        return None