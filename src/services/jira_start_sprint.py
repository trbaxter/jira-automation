import logging
from datetime import datetime

import requests
from pydantic import HttpUrl

from src.constants.shared import SAFE_STR, INT_GT_0
from src.logs.error_handling import handle_api_error
from src.utils.payload_builder import build_start_sprint_payload


def start_sprint(
    new_sprint_id: INT_GT_0,
    sprint_name: SAFE_STR,
    start_date: datetime,
    end_date: datetime,
    session: requests.Session,
    base_url: HttpUrl,
) -> None:
    url = f"{base_url}/rest/agile/1.0/sprint/{new_sprint_id}"
    payload = build_start_sprint_payload(sprint_name, start_date, end_date)

    response = session.put(url, json=payload.model_dump())
    context = f"starting sprint {new_sprint_id}"
    if not handle_api_error(response, context):
        return

    logging.info(f"\nActivating sprint: {sprint_name}")
    logging.info("\nSprint automation process complete.")
