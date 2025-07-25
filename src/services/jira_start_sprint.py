import logging
from datetime import datetime
from pydantic import HttpUrl

import requests

from utils.payload_builder import build_start_sprint_payload
from src.logging_config.error_handling import handle_api_error


def start_sprint(
        new_sprint_id: int,
        sprint_name: str,
        start_date: datetime,
        end_date: datetime,
        session: requests.Session,
        base_url: HttpUrl
) -> None:
    """
    Activates a new sprint in JIRA by sending a PUT
    request with the appropriate payload.

    Args:
        new_sprint_id: ID of the sprint to activate.
        sprint_name: Name of the sprint.
        start_date: Start datetime of the sprint.
        end_date: End datetime of the sprint.
        session: Authenticated requests session.
        base_url: Base URL of the JIRA API.

    Returns:
        None. Logs the result.
    """
    url = f"{base_url}/rest/agile/1.0/sprint/{new_sprint_id}"
    payload = build_start_sprint_payload(sprint_name, start_date, end_date)

    response = session.put(url, json=payload)
    if not handle_api_error(
            response,
            f"starting sprint {new_sprint_id}"
    ):
        return

    logging.info(f"\nSprint {new_sprint_id} is now active.")
    logging.info("\nSprint automation process complete.")
