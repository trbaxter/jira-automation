import logging

import requests
from pydantic import conint, constr, HttpUrl

from src.logging_config.error_handling import handle_api_error
from src.utils.payload_builder import build_close_sprint_payload


def close_sprint(
        sprint_id: conint(gt=0),
        sprint_name: constr(strip_whitespace=True, max_length=1),
        start_date: str,
        end_date: str,
        session: requests.Session,
        base_url: HttpUrl
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
    payload = build_close_sprint_payload(
        sprint_name=sprint_name,
        start_date=start_date,
        end_date=end_date
    )

    response = session.put(url=url, json=payload.model_dump())

    if not handle_api_error(response, f"closing sprint {sprint_id}"):
        return

    logging.info(f"Sprint {sprint_id} has been closed.")
