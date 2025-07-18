import base64
import logging
import os
import certifi
import requests
from datetime import datetime
from src.utils.datetime_format import format_jira_date



# Configure logging
logging.basicConfig(level = logging.INFO, format = "%(message)s")


# Load JIRA credentials from repo secrets
EMAIL = os.getenv("JIRA_EMAIL", "")
API_TOKEN = os.getenv("JIRA_API_TOKEN", "")


# # Validate repository secrets.
if not EMAIL or not API_TOKEN:
    raise EnvironmentError("Error: Repository secret not found.")


# # JIRA API token config
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
def create_sprint(
        sprint_name: str,
        start_date: datetime,
        end_date: datetime,
        config) -> None:
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


# Retrieves a sprint for the board by state (e.g., 'active', 'future').
def get_sprint_by_state(config, state):
    url = (
        f"{config.base_url}/rest/agile/1.0/board/"
        f"{config.board_id}/sprint?state={state}"
    )
    response = session.get(url)
    if not handle_api_error(response, f"retrieving {state} sprint"):
        return None

    sprints = response.json().get("values", [])
    return sprints[0] if sprints else None


# Get incomplete stories from active sprint
def get_incomplete_stories(sprint_id, config):
    incomplete_stories = []
    start_at = 0
    max_results = 50
    done_statuses = {"Done", "Cancelled", "Existing Solution", "Abandoned"}

    while True:
        url = f"{config.base_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
        params = {"startAt": start_at, "maxResults": max_results}
        response = session.get(url, params = params)

        if not handle_api_error(
                response, f"retrieving issues from sprint {sprint_id}"
        ):
            break

        data = response.json()
        issues = data.get("issues", [])

        logging.info(
            f"Fetched {len(issues)} issues from page starting at {start_at}."
        )

        incomplete_stories.extend(
            issue for issue in issues
            if issue["fields"]["status"]["name"] not in done_statuses
        )

        if len(issues) < max_results:
            break

        start_at += max_results

    logging.info(
        f"\n{len(incomplete_stories)} incomplete stories found "
        f"in active sprint {sprint_id}."
    )
    return incomplete_stories
