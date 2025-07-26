import logging
from datetime import datetime
from typing import Optional

import requests

from src.logging_config.error_handling import handle_api_error
from src.models.board_config import BoardConfig
from src.models.payload import SprintPayload
from src.models.sprint_create_response import SprintCreateResponse
from src.models.sprint_summary import SprintSummary
from src.utils.config_loader import load_config
from src.utils.datetime_format import format_jira_date
from src.utils.url_builder import build_sprint_state_query_url

SPRINT_CREATE = "/rest/agile/1.0/sprint"


def build_sprint_payload(
        sprint_name: str,
        sprint_start: datetime,
        sprint_end: datetime,
        board_id: int
) -> SprintPayload:
    """
    Assembles the JSON payload to send to the JIRA API.

    Args:
        sprint_name: Name of the sprint.
        sprint_start: Datetime of sprint start.
        sprint_end: Datetime of sprint end.
        board_id: ID of the JIRA board to attach the sprint to

    Returns:
        A dictionary conforming to the SprintPayload structure.
    """
    return SprintPayload(
        name=sprint_name,
        startDate=format_jira_date(sprint_start),
        endDate=format_jira_date(sprint_end),
        originBoardId=board_id
    )


def post_sprint_payload(
        session: requests.Session,
        url: str,
        payload: SprintPayload
) -> requests.Response:
    """
    Posts the sprint payload to the JIRA API.

    Args:
        session: An authenticated requests.Session instance.
        url: Full API endpoint for sprint creation.
        payload: The structured SprintPayload dictionary.

    Returns:
        The raw HTTP response from the JIRA API.
    """
    return session.post(url, json=payload)


def parse_json_response(
        response: requests.Response
) -> Optional[SprintCreateResponse]:
    """
    Parses the JSON response, handling decode errors with logging.

    Args:
        The HTTP response object.

    Returns:
        Parsed JSON as a dict if valid, otherwise None.
    """
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        logging.error("Error: Failed to parse JSON response.")
        logging.error(f"Response Content: {response.text}")
        return None


def create_sprint(
        sprint_name: str,
        start_date: datetime,
        end_date: datetime,
        session: requests.Session,
) -> Optional[SprintCreateResponse]:
    """
    Creates a new sprint in JIRA using the board config in the YAML file.

    Args:
        sprint_name: Desired sprint name.
        start_date: Datetime of sprint start.
        end_date: Datetime of sprint end.
        session: An authenticated request.Session object.

    Returns:
        Parsed JSON response if successful, otherwise None.
    """
    config = load_config()
    payload = build_sprint_payload(
        sprint_name,
        start_date,
        end_date,
        config.board_id
    )
    url = f"{config.base_url}{SPRINT_CREATE}"

    response = post_sprint_payload(session, url, payload)

    if not handle_api_error(response, "creating sprint"):
        return None

    return parse_json_response(response)


def get_sprint_by_state(
        session: requests.Session,
        config: BoardConfig,
        state: str
) -> Optional[SprintSummary]:
    url = build_sprint_state_query_url(
        config.base_url,
        config.board_id,
        state
    )
    response = session.get(url)

    if not handle_api_error(response, f"retrieving {state} sprint"):
        return None

    sprints = response.json().get("values", [])
    return sprints[0] if sprints else None


def get_all_future_sprints(
        session: requests.Session,
        config: BoardConfig
) -> list[SprintSummary]:
    board_id = config.board_id
    start_at = 0
    max_results = 50
    all_sprints = []
    url = f"{config.base_url}/rest/agile/1.0/board/{board_id}/sprint"

    while True:
        params = {
            "state": "future",
            "startAt": start_at,
            "maxResults": max_results
        }
        response = session.get(url, params=params)
        if response.status_code != 200:
            raise RuntimeError(
                f"\nError while fetching future sprints: {response.text}"
            )

        data = response.json()
        sprints = data.get("values", [])
        all_sprints.extend(sprints)

        if data.get("isLast", True):
            break

        start_at += max_results

    return all_sprints
