import logging
from datetime import datetime
from typing import Optional

import requests

from src.helpers.config_accessor import get_board_config
from src.logging_config.error_handling import handle_api_error
from src.type_defs.payload import SprintPayload
from src.type_defs.sprint_create_response import SprintCreateResponse
from src.type_defs.sprint_summary import SprintSummary
from src.type_defs.boardconfig import BoardConfig
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
    return {
        "name": sprint_name,
        "startDate": format_jira_date(sprint_start),
        "endDate": format_jira_date(sprint_end),
        "originBoardId": board_id
    }


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
        response: requests.Response) -> Optional[SprintCreateResponse]:
    """
    Parses the JSON response, handling decode errors with logging.

    Args:
        response: The HTTP response object.

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
        board_name: str,
        sprint_name: str,
        start_date: datetime,
        end_date: datetime,
        session: requests.Session,
        config_path: str = "board_config.yaml"
) -> Optional[SprintCreateResponse]:
    """
    Creates a new sprint in JIRA using the board config in the YAML file.

    Args:
        board_name: Alias of the board as set in the YAML config.
        sprint_name: Desired sprint name.
        start_date: Datetime of sprint start.
        end_date: Datetime of sprint end.
        session: An authenticated request.Session object.
        config_path: Optional path to the YAML config file.
                     Defaults to 'board_config.yaml'.

    Returns:
        Parsed JSON response if successful, otherwise None.
    """
    config: BoardConfig = get_board_config(board_name, config_path)
    payload = build_sprint_payload(
        sprint_name,
        start_date,
        end_date,
        config["id"]
    )
    url = f"{config['base_url']}{SPRINT_CREATE}"

    response = post_sprint_payload(session, url, payload)

    if not handle_api_error(response, "creating sprint"):
        return None

    return parse_json_response(response)


def get_sprint_by_state(
        session: requests.Session,
        config: BoardConfig,
        state: str
) -> Optional[SprintSummary]:
    url = build_sprint_state_query_url(config["base_url"], config["id"], state)
    response = session.get(url)

    if not handle_api_error(response, f"retrieving {state} sprint"):
        return None

    sprints = response.json().get("values", [])
    return sprints[0] if sprints else None