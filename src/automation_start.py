import logging
import requests
from datetime import datetime
from src.utils.datetime_format import format_jira_date


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
    done_statuses = {
        "Done",
        "Cancelled",
        "Existing Solution",
        "Abandoned"
    }

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
