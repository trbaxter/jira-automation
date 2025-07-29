import logging
from datetime import datetime

import requests
from pydantic import HttpUrl

from src.fieldtypes.common import SAFE_STR, INT_GT_0
from src.logging_config.error_handling import handle_api_error
from src.utils.payload_builder import build_start_sprint_payload


def start_sprint(
        new_sprint_id: INT_GT_0,
        sprint_name: SAFE_STR,
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
    payload = build_start_sprint_payload(
        sprint_name=sprint_name,
        start_date=start_date,
        end_date=end_date
    )

    response = session.put(url=url, json=payload.model_dump())
    context = f"starting sprint {new_sprint_id}"
    if not handle_api_error(response=response, context=context):
        return

    logging.info(msg=f"\nSprint {new_sprint_id} is now active.")
    logging.info(msg="\nSprint automation process complete.")
