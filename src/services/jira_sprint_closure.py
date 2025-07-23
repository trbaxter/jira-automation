import logging

import requests

from src.helpers.payload_builder import build_close_sprint_payload
from src.logging_config.error_handling import handle_api_error


def close_sprint(
        sprint_id: int,
        sprint_name: str,
        start_date: str,
        end_date: str,
        session: requests.Session,
        base_url: str
) -> None:
    """
    Closes a sprint using the JIRA API.

    Args:
        sprint_id: The ID of the sprint to close.
        sprint_name: The name of the sprint.
        start_date: The sprint's start date.
        end_date: The sprint's end date.
        session: An authenticated requests session.
        base_url: The base URL to the sprint board.

    Returns:
        None. Logs success or failure.
    """
    url = f"{base_url}/rest/agile/1.0/sprint/{sprint_id}"
    payload = build_close_sprint_payload(sprint_name, start_date, end_date)

    response = session.put(url, json=payload)

    if not handle_api_error(response, f"closing sprint {sprint_id}"):
        return

    logging.info(f"Sprint {sprint_id} has been closed.")
