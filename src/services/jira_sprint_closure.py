import logging

import requests
from pydantic import HttpUrl

from src.constants.field_types import SAFE_STR, INT_GT_0
from src.logs.error_handling import handle_api_error
from src.utils.payload_builder import build_close_sprint_payload


def close_sprint(
    sprint_id: INT_GT_0,
    sprint_name: SAFE_STR,
    start_date: SAFE_STR,
    end_date: SAFE_STR,
    session: requests.Session,
    base_url: HttpUrl,
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
        sprint_name=sprint_name, start_date=start_date, end_date=end_date
    )

    response = session.put(url=url, json=payload.model_dump())
    context = f"closing sprint {sprint_id}"

    if not handle_api_error(response=response, context=context):
        return

    logging.info(msg=f"Sprint {sprint_id} has been closed.")
